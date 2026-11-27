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
