"""Kiểm tra tự động cho timeline tổng (05_timeline)."""
import json
import re
from pathlib import Path

from vp.checks import CheckResult, register
from vp.checks.files import load_yaml
from vp.checks.script import segments as script_segments


def _fmt(bad, head):
    return CheckResult("fail", head + "\n" + "\n".join(f"- {b}" for b in bad[:30]))


@register("timeline_consistency")
def timeline_consistency(project: Path, params: dict) -> CheckResult:
    t = load_yaml(project, params["path"])
    script = load_yaml(project, params.get("script", "01_script/script.yaml"))
    man = load_yaml(project, params.get("voice", "04_voice/voice_manifest.yaml"))
    fps = float(t["fps"])
    bad = []
    order = [s["id"] for _, s in script_segments(script)]
    if [s["id"] for s in t["segments"]] != order:
        bad.append("thứ tự đoạn trong timeline khác kịch bản")
    dur = {m["id"]: float(m["duration_s"]) for m in man["segments"]}
    prev_end = 0
    for v in t["voice"]:
        n = v["end_frame"] - v["start_frame"]
        want = round(dur.get(v["segment"], -1) * fps)
        if abs(n - want) > 1:
            bad.append(f"{v['segment']}: giọng dài {n} khung ≠ manifest {want} khung")
        if v["start_frame"] < prev_end:
            bad.append(f"{v['segment']}: giọng chồng lên đoạn trước ({v['start_frame']} < {prev_end})")
        prev_end = v["end_frame"]
    shots = t["shots"]
    if shots and shots[0]["start_frame"] != 0:
        bad.append(f"khung đầu bắt đầu ở {shots[0]['start_frame']} thay vì 0")
    for a, b in zip(shots, shots[1:]):
        if b["start_frame"] > a["end_frame"]:
            bad.append(f"hở giữa {a['id']} và {b['id']} ({a['end_frame']} → {b['start_frame']})")
        elif b["start_frame"] < a["end_frame"]:
            bad.append(f"chồng giữa {a['id']} và {b['id']} ({a['end_frame']} > {b['start_frame']})")
    if shots and shots[-1]["end_frame"] != t["total_frames"]:
        bad.append(f"khung cuối kết thúc ở {shots[-1]['end_frame']} ≠ tổng {t['total_frames']}")
    by = {s["id"]: s for s in shots}
    for c in t["cues"]:
        s = by.get(c["shot"])
        if not s or not s["start_frame"] <= c["frame"] <= s["end_frame"]:
            bad.append(f"cue {c['shot']}/{c['element']}.{c['event']} ở khung {c['frame']} nằm ngoài khung hình")
    if abs(t["total_s"] - t["total_frames"] / fps) > 0.002:
        bad.append("total_s không khớp total_frames / fps")
    if bad:
        return _fmt(bad, "Timeline không nhất quán:")
    return CheckResult("pass", f"{len(t['segments'])} đoạn, {len(shots)} khung, {len(t['cues'])} cue, {len(t['sfx'])} SFX; "
                               f"tổng {t['total_frames']} khung = {t['total_s']}s @ {fps:g} fps; giọng khớp manifest ±1 khung.")


_TS = re.compile(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)")


def _sec(h, m, s, ms):
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


@register("subtitles_valid")
def subtitles_valid(project: Path, params: dict) -> CheckResult:
    raw = (project / params["path"]).read_text(encoding="utf-8")
    if not raw.strip():
        return CheckResult("fail", "Phụ đề rỗng.")
    script = load_yaml(project, params.get("script", "01_script/script.yaml"))
    mx_c, mx_l, mn = int(params.get("max_chars", 42)), int(params.get("max_lines", 2)), float(params.get("min_s", 1.0))
    bad, words, prev_end, n = [], [], 0.0, 0
    for block in re.split(r"\n\s*\n", raw.strip()):
        lines = block.strip().splitlines()
        if len(lines) < 3 or not _TS.match(lines[1]):
            bad.append(f"khối không đúng định dạng SRT: {lines[:2]}")
            continue
        n += 1
        g = _TS.match(lines[1]).groups()
        a, b = _sec(*g[:4]), _sec(*g[4:])
        text = lines[2:]
        if b - a + 1e-6 < mn:
            bad.append(f"#{lines[0]}: hiện {b - a:.2f}s < {mn}s")
        if a + 1e-6 < prev_end:
            bad.append(f"#{lines[0]}: chồng lên phụ đề trước")
        if len(text) > mx_l:
            bad.append(f"#{lines[0]}: {len(text)} dòng > {mx_l}")
        for ln in text:
            if len(ln) > mx_c:
                bad.append(f"#{lines[0]}: dòng {len(ln)} ký tự > {mx_c}")
            words += ln.split()
        prev_end = b
    want = " ".join(s["text"] for _, s in script_segments(script) if s.get("kind") == "voice").split()
    if words != want:
        i = next((k for k, (x, y) in enumerate(zip(words, want)) if x != y), min(len(words), len(want)))
        bad.append(f"chữ phụ đề khác lời kịch bản từ từ thứ {i + 1}: \"{' '.join(words[i:i + 5])}\" ≠ \"{' '.join(want[i:i + 5])}\"")
    if bad:
        return _fmt(bad, "Phụ đề có lỗi:")
    return CheckResult("pass", f"{n} cụm phụ đề: ≤ {mx_l} dòng, ≤ {mx_c} ký tự/dòng, ≥ {mn}s, không chồng; chữ khớp lời kịch bản.")


@register("timeline_in_sync")
def timeline_in_sync(project: Path, params: dict) -> CheckResult:
    from vp.timeline import input_hash
    mp = project / params["manifest"]
    if not mp.is_file():
        return CheckResult("fail", "Chưa dựng timeline. Chạy: python -m vp timeline build <dự án>")
    man = json.loads(mp.read_text(encoding="utf-8"))
    if man["hash"] != input_hash(project, man["params"]):
        return CheckResult("fail", "Timeline đã cũ so với kịch bản/storyboard/giọng/brief. Chạy lại: python -m vp timeline build <dự án>")
    return CheckResult("pass", "Timeline khớp đầu vào hiện tại.")
