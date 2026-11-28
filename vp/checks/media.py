"""Kiểm tra tự động cho file media, dựa trên ffprobe/ffmpeg."""
import json
import re
import subprocess
from fractions import Fraction
from pathlib import Path

from vp.checks import CheckResult, register


def _file(project: Path, rel: str) -> Path:
    p = project / rel
    if not p.is_file():
        raise FileNotFoundError(2, "missing", rel)
    return p


def probe(path: Path) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", str(path)],
        capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def ffmpeg_filter_log(path: Path, args: list[str]) -> str:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), *args, "-f", "null", "-"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-500:])
    return r.stderr


def _stream(info, kind):
    return next((s for s in info["streams"] if s.get("codec_type") == kind), None)


@register("video_format")
def video_format(project: Path, params: dict) -> CheckResult:
    p = _file(project, params["path"])
    v = _stream(probe(p), "video")
    if v is None:
        return CheckResult("fail", "Không có luồng hình.")
    if params.get("format_from"):
        # khung lấy từ brief (hồ sơ nền tảng nếu có), không ghi cứng trong checklist
        from vp import platforms as pf
        from vp.checks.files import load_yaml
        c = pf.canvas(load_yaml(project, params["format_from"]))
        params = {**params, "width": c["width"], "height": c["height"], "fps": params.get("fps", c["fps"])}
    if params.get("animatic_from"):
        # animatic: nửa canvas của storyboard + dải phụ đề riêng (vp.animatic.caption_h)
        from vp.animatic import caption_h
        from vp.checks.files import load_yaml
        from vp.design_preview import preview_size
        w, h = preview_size(load_yaml(project, params["animatic_from"])["meta"]["canvas"])
        params = {**params, "width": w, "height": h + caption_h((w, h))}
    fps = float(Fraction(v["r_frame_rate"]))
    got = f"{v['width']}x{v['height']} @ {fps:g} fps, {v['codec_name']}, {v.get('pix_fmt')}"
    problems = []
    if (v["width"], v["height"]) != (params["width"], params["height"]):
        problems.append(f"kích thước {v['width']}x{v['height']} ≠ {params['width']}x{params['height']}")
    if abs(fps - float(params["fps"])) > 0.01:
        problems.append(f"fps {fps:g} ≠ {params['fps']}")
    for key in ("codec", "pix_fmt"):
        want = params.get(key)
        have = v["codec_name"] if key == "codec" else v.get("pix_fmt")
        if want and have != want:
            problems.append(f"{key} {have} ≠ {want}")
    if problems:
        return CheckResult("fail", f"Thực tế: {got}. Sai: " + "; ".join(problems))
    return CheckResult("pass", f"Đúng định dạng: {got}.")


@register("black_frames")
def black_frames(project: Path, params: dict) -> CheckResult:
    p = _file(project, params["path"])
    mx = float(params.get("max_black_s", 0.5))
    log = ffmpeg_filter_log(p, ["-vf", "blackdetect=d=0.04:pix_th=0.10", "-an"])
    spans = [(float(a), float(b), float(d)) for a, b, d in
             re.findall(r"black_start:([\d.]+) black_end:([\d.]+) black_duration:([\d.]+)", log)]
    bad = [s for s in spans if s[2] > mx]
    if bad:
        return CheckResult("fail", "Khung đen dài quá {:g}s: ".format(mx) +
                           "; ".join(f"{a:.1f}s→{b:.1f}s ({d:.2f}s)" for a, b, d in bad))
    return CheckResult("pass", f"Không có đoạn đen > {mx:g}s ({len(spans)} đoạn đen ngắn).")


@register("freeze_frames")
def freeze_frames(project: Path, params: dict) -> CheckResult:
    p = _file(project, params["path"])
    mx = float(params.get("max_freeze_s", 2.0))
    log = ffmpeg_filter_log(p, ["-vf", f"freezedetect=n=-60dB:d={mx}", "-an"])
    starts = re.findall(r"freeze_start: ([\d.]+)", log)
    durs = re.findall(r"freeze_duration: ([\d.]+)", log)
    if starts:
        spans = [f"từ {float(s):.1f}s" + (f" ({float(d):.1f}s)" if i < len(durs) else " đến hết")
                 for i, (s, d) in enumerate(zip(starts, durs + [""] * len(starts)))]
        return CheckResult("fail", f"Hình đứng yên quá {mx:g}s: " + "; ".join(spans))
    return CheckResult("pass", f"Không có đoạn đứng hình > {mx:g}s.")


@register("audio_loudness")
def audio_loudness(project: Path, params: dict) -> CheckResult:
    p = _file(project, params["path"])
    if _stream(probe(p), "audio") is None:
        return CheckResult("fail", "Không có luồng âm thanh.")
    log = ffmpeg_filter_log(p, ["-af", "ebur128=peak=true", "-vn"])
    summary = log[log.rfind("Summary:"):]
    lufs = float(re.search(r"I:\s+(-?[\d.]+) LUFS", summary).group(1))
    tp = float(re.search(r"True peak:\s+Peak:\s+(-?[\d.]+|-inf) dBFS", summary).group(1))
    target, tol = float(params.get("target_lufs", -14)), float(params.get("tolerance", 1.0))
    max_tp = float(params.get("max_true_peak", -1.0))
    msg = f"Độ to {lufs:.1f} LUFS (mục tiêu {target:g}±{tol:g}), đỉnh thực {tp:.1f} dBTP (tối đa {max_tp:g})."
    ok = abs(lufs - target) <= tol and tp <= max_tp
    return CheckResult("pass" if ok else "fail", msg)


@register("av_duration_match")
def av_duration_match(project: Path, params: dict) -> CheckResult:
    p = _file(project, params["path"])
    info = probe(p)
    v, a = _stream(info, "video"), _stream(info, "audio")
    if v is None or a is None:
        return CheckResult("fail", "Thiếu luồng " + ("hình" if v is None else "âm thanh") + ".")
    dv, da = float(v["duration"]), float(a["duration"])
    mx = float(params.get("max_diff_s", 0.1))
    msg = f"Hình {dv:.3f}s, tiếng {da:.3f}s, lệch {abs(dv - da):.3f}s (tối đa {mx:g}s)."
    if "expected_s" in params:
        exp = float(params["expected_s"])
        msg += f" Kỳ vọng {exp:g}s."
        if abs(dv - exp) > mx:
            return CheckResult("fail", msg)
    return CheckResult("pass" if abs(dv - da) <= mx else "fail", msg)


@register("animatic_in_sync")
def animatic_in_sync(project: Path, params: dict) -> CheckResult:
    from vp.animatic import input_hash
    mp = project / params["manifest"]
    if not mp.is_file() or not (project / params["path"]).is_file():
        return CheckResult("fail", "Chưa dựng animatic. Chạy: python -m vp animatic build <dự án>")
    man = json.loads(mp.read_text(encoding="utf-8"))
    if man.get("hash") != input_hash(project, man.get("fps", 15)):
        return CheckResult("fail", "Animatic đã cũ so với kịch bản/storyboard/giọng nháp. Chạy lại: python -m vp animatic build <dự án>")
    return CheckResult("pass", f"Animatic khớp đầu vào hiện tại (nguồn lời: {man.get('voice_source')}, {man.get('fps')} fps).")


@register("animatic_duration")
def animatic_duration(project: Path, params: dict) -> CheckResult:
    from vp.checks.files import load_yaml
    p = _file(project, params["path"])
    total = float(load_yaml(project, params["timing"])["total_s"])
    v = _stream(probe(p), "video")
    dv = float(v["duration"])
    mx = float(params.get("max_diff_s", 0.1))
    msg = f"Video {dv:.3f}s, timing {total:.3f}s, lệch {abs(dv - total):.3f}s (tối đa {mx:g}s)."
    return CheckResult("pass" if abs(dv - total) <= mx else "fail", msg)
