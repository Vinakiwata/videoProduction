"""Kiểm tra tự động cho giọng đọc (04_voice)."""
import hashlib
import wave
from pathlib import Path

from vp.checks import CheckResult, register
from vp.checks.files import load_yaml
from vp.checks.script import segments as script_segments


def _fmt(bad, head):
    return CheckResult("fail", head + "\n" + "\n".join(f"- {b}" for b in bad))


@register("voice_manifest")
def voice_manifest(project: Path, params: dict) -> CheckResult:
    from vp.voice import prepare_text
    man = load_yaml(project, params["path"])
    script = load_yaml(project, params.get("script", "01_script/script.yaml"))
    pron = (script.get("meta") or {}).get("pronunciation") or script.get("pronunciation") or {}
    base = (project / params["path"]).parent
    want = {s["id"]: s for _, s in script_segments(script) if s.get("kind") == "voice"}
    have = {e["id"]: e for e in man.get("segments") or []}
    bad = [f"{i}: chưa có giọng" for i in want if i not in have]
    bad += [f"{i}: có giọng nhưng kịch bản không còn đoạn này" for i in have if i not in want]
    for i, e in have.items():
        if i not in want:
            continue
        spoken = prepare_text(want[i]["text"], pron)
        if e.get("spoken_text") != spoken:
            bad.append(f"{i}: văn bản đã đọc khác kịch bản hiện tại → tạo lại giọng (đọc: \"{str(e.get('spoken_text'))[:50]}…\")")
        f = base / e["file"]
        if not f.is_file():
            bad.append(f"{i}: thiếu file {e['file']}")
            continue
        if hashlib.sha256(f.read_bytes()).hexdigest() != e.get("sha256"):
            bad.append(f"{i}: file {e['file']} đã bị thay đổi sau khi ghi manifest")
        with wave.open(str(f), "rb") as w:
            d = w.getnframes() / w.getframerate()
        if abs(d - float(e["duration_s"])) > 0.01:
            bad.append(f"{i}: thời lượng file {d:.3f}s ≠ manifest {e['duration_s']}s")
    if bad:
        return _fmt(bad, "Manifest giọng không khớp kịch bản/file:")
    total = sum(float(e["duration_s"]) for e in have.values())
    return CheckResult("pass", f"{len(have)} đoạn giọng ({man.get('engine')}, {man.get('voice')}), tổng lời {total:.1f}s, "
                               f"tốc độ trung vị {man.get('measured_sps_median')} âm tiết/giây; khớp kịch bản và file.")


@register("voice_segment_quality")
def voice_segment_quality(project: Path, params: dict) -> CheckResult:
    man = load_yaml(project, params["path"])
    mx_peak = float(params.get("max_peak_dbfs", -1.0))
    mx_edge = float(params.get("max_edge_silence_s", 0.35))
    mx_gap = float(params.get("max_gap_s", 1.0))
    lo, hi = float(params.get("min_sps", 2.0)), float(params.get("max_sps", 5.0))
    bad = []
    for e in man.get("segments") or []:
        i = e["id"]
        if e["peak_dbfs"] > mx_peak:
            bad.append(f"{i}: đỉnh {e['peak_dbfs']} dBFS > {mx_peak} (nguy cơ vỡ tiếng)")
        if e["lead_s"] > mx_edge or e["trail_s"] > mx_edge:
            bad.append(f"{i}: lặng đầu {e['lead_s']}s / cuối {e['trail_s']}s > {mx_edge}s")
        if e["max_gap_s"] > mx_gap:
            bad.append(f"{i}: lặng giữa câu {e['max_gap_s']}s > {mx_gap}s (TTS ngắt lạ/nuốt chữ?)")
        if not lo <= e["sps"] <= hi:
            bad.append(f"{i}: tốc độ {e['sps']} âm tiết/giây ngoài {lo}–{hi} (câu bị cắt hoặc đọc lỗi?)")
    if bad:
        return _fmt(bad, "Đoạn giọng có dấu hiệu lỗi:")
    segs = man.get("segments") or []
    return CheckResult("pass", f"{len(segs)} đoạn: đỉnh ≤ {mx_peak} dBFS, lặng hai đầu ≤ {mx_edge}s, "
                               f"lặng giữa câu ≤ {mx_gap}s, tốc độ trong {lo}–{hi} âm tiết/giây.")
