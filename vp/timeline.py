"""Tool Timeline tổng — khoá mọi mốc thời gian thành khung hình nguyên. Xem spec 2026-11-27-tool-timeline-design.md."""
import hashlib
import json
import re
from pathlib import Path

from vp import review
from vp.checks.files import load_yaml
from vp.checks.script import segments as script_segments
from vp.checks.script import syllables
from vp.project import dump_yaml

DIR = "05_timeline"
BREAK_BEFORE = {"và", "thì", "là", "như", "khi", "nếu", "để", "của", "cho", "bị", "sẽ", "rồi", "nhưng", "với",
                "mà", "vì", "nên", "đang", "vẫn", "đã", "các", "những", "một", "trong", "trên", "dưới", "còn"}


class TimelineError(RuntimeError):
    pass


# ---------- phụ đề ----------

def split_lines(text: str, max_chars: int = 42) -> list[str]:
    """Tách thành dòng ≤ max_chars: ưu tiên dấu câu, rồi trước từ nối, cuối cùng theo độ dài."""
    phrases = [p.strip() for p in re.split(r"(?<=[,.!?;:…])\s+", text.strip()) if p.strip()]
    out = []
    for ph in phrases:
        words = ph.split()
        while words:
            line = " ".join(words)
            if len(line) <= max_chars:
                out.append(line); break
            best, score = 1, 1e9
            for i in range(1, len(words)):
                left = " ".join(words[:i])
                if len(left) > max_chars:
                    break
                sc = (max_chars - len(left)) + (0 if words[i].lower() in BREAK_BEFORE else 8)
                if sc < score:
                    best, score = i, sc
            out.append(" ".join(words[:best]))
            words = words[best:]
    # gộp dòng ngắn liền kề nếu vừa
    merged = []
    for ln in out:
        if merged and len(merged[-1]) + 1 + len(ln) <= max_chars and not merged[-1].endswith((".", "!", "?")):
            merged[-1] = f"{merged[-1]} {ln}"
        else:
            merged.append(ln)
    return merged


def _srt_time(frame: int, fps: float) -> str:
    ms = int(round(frame / fps * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _subtitle_cues(seg: dict, fps: float, max_chars: int, max_lines: int, min_frames: int) -> list[dict]:
    lines = split_lines(seg["text"], max_chars)
    groups = [lines[i:i + max_lines] for i in range(0, len(lines), max_lines)]
    total_syl = max(1, sum(syllables(" ".join(g)) for g in groups))
    span = seg["speech_end_frame"] - seg["start_frame"]
    cues, f = [], seg["start_frame"]
    for i, g in enumerate(groups):
        n = round(span * syllables(" ".join(g)) / total_syl)
        end = seg["speech_end_frame"] if i == len(groups) - 1 else f + n
        cues.append({"start": f, "end": end, "lines": g})
        f = end
    # cụm quá ngắn: gộp với cụm trước nếu còn chỗ dòng
    fixed = []
    for c in cues:
        if fixed and c["end"] - c["start"] < min_frames and len(fixed[-1]["lines"]) + len(c["lines"]) <= max_lines:
            fixed[-1]["end"] = c["end"]; fixed[-1]["lines"] += c["lines"]
        else:
            fixed.append(c)
    # vẫn ngắn: dời ranh giới — mượn từ cụm sau, rồi cụm trước; cụm cuối được kéo vào khoảng thở
    for i, c in enumerate(fixed):
        need = min_frames - (c["end"] - c["start"])
        if need <= 0:
            continue
        if i + 1 < len(fixed):
            nx = fixed[i + 1]
            give = min(need, max(0, (nx["end"] - nx["start"]) - min_frames))
            c["end"] += give; nx["start"] += give; need -= give
        if need > 0 and i > 0:
            pv = fixed[i - 1]
            give = min(need, max(0, (pv["end"] - pv["start"]) - min_frames))
            pv["end"] -= give; c["start"] -= give; need -= give
        if need > 0 and i == len(fixed) - 1:
            c["end"] = min(seg["end_frame"], c["end"] + need)
    return fixed


# ---------- dựng ----------

def input_hash(project: Path, params: dict) -> str:
    h = hashlib.sha256()
    for rel in ("01_script/script.yaml", "02_design/storyboard.yaml", "04_voice/voice_manifest.yaml", "00_brief/brief.yaml"):
        h.update(json.dumps(load_yaml(project, rel), sort_keys=True, ensure_ascii=False, default=str).encode())
    h.update(json.dumps(params, sort_keys=True).encode())
    return h.hexdigest()


def build(project: Path, breath: float = 0.35, breath_question: float = 0.45, max_chars: int = 42,
          max_lines: int = 2, min_sub_s: float = 1.0, check_gate: bool = True) -> Path:
    project = Path(project)
    if check_gate:
        g = review.gate(project, "voice")
        if not g.ok:
            raise TimelineError(f"Cổng 'voice' chưa mở: {g.message}")
    brief = load_yaml(project, "00_brief/brief.yaml")
    script = load_yaml(project, "01_script/script.yaml")
    sb = load_yaml(project, "02_design/storyboard.yaml")
    man = load_yaml(project, "04_voice/voice_manifest.yaml")
    fps = float(brief["format"]["fps"])
    vdur = {m["id"]: m for m in man["segments"]}
    order = [s for _, s in script_segments(script)]

    segs, voice_track, f = [], [], 0
    for i, s in enumerate(order):
        if s.get("kind") == "voice":
            if s["id"] not in vdur:
                raise TimelineError(f"{s['id']} chưa có giọng trong voice_manifest.yaml")
            n = round(float(vdur[s["id"]]["duration_s"]) * fps)
            nxt = order[i + 1] if i + 1 < len(order) else None
            b = 0.0
            if nxt is not None and nxt.get("kind") == "voice":
                b = breath_question if s["text"].rstrip().endswith(("?", "!")) else breath
        else:
            n = round(float(s.get("est_duration_s") or 0) * fps)
            b = 0.0
        bf = round(b * fps)
        rec = {"id": s["id"], "kind": s.get("kind"), "text": s.get("text"), "start_frame": f, "speech_end_frame": f + n,
               "end_frame": f + n + bf, "breath_s": b}
        segs.append(rec)
        if s.get("kind") == "voice":
            voice_track.append({"segment": s["id"], "file": f"04_voice/{vdur[s['id']]['file']}",
                                "start_frame": f, "end_frame": f + n})
        f += n + bf
    total = f
    by_seg = {s["id"]: s for s in segs}

    shots, cues, sfx = [], [], []
    for sh in sb.get("shots") or []:
        sg = by_seg[sh["segment"]]
        a, b = sh["span"]
        cf = sg["speech_end_frame"] - sg["start_frame"]
        cs = sg["start_frame"] + round(a * cf)
        ce = sg["start_frame"] + round(b * cf)
        end = sg["end_frame"] if b >= 1 - 1e-9 else ce
        shots.append({"id": sh["id"], "segment": sh["segment"], "start_frame": cs, "end_frame": end,
                      "content_end_frame": ce, "transition_in": sh["transition_in"], "camera": sh["camera"]})
        n = ce - cs
        evf = {}
        for e in sh.get("elements") or []:
            for ev in ("enter", "exit"):
                m = e.get(ev)
                if m:
                    fr = cs + round(m["at"] * n)
                    evf[(e["id"], ev)] = fr
                    cues.append({"shot": sh["id"], "element": e["id"], "event": ev, "frame": fr, "anim": m["anim"],
                                 "dur_frames": round(float(m.get("dur_s", 0.3)) * fps), "ease": m.get("ease", "ease_out")})
            if e.get("loop"):
                fr = evf.get((e["id"], "enter"), cs)
                evf[(e["id"], "loop")] = fr
                cues.append({"shot": sh["id"], "element": e["id"], "event": "loop", "frame": fr,
                             "anim": e["loop"]["anim"], "period_frames": round(float(e["loop"].get("period_s", 1.5)) * fps)})
        for x in sh.get("sfx") or []:
            fr = evf.get((x["target"], x["event"]), cs if x["event"] != "exit" else end)
            sfx.append({"name": x["name"], "shot": sh["id"], "target": x["target"], "event": x["event"], "frame": fr})
    shots.sort(key=lambda s: s["start_frame"])
    cues.sort(key=lambda c: (c["frame"], c["shot"], c["element"]))
    sfx.sort(key=lambda x: x["frame"])

    out = project / DIR
    out.mkdir(parents=True, exist_ok=True)
    tl = {"fps": fps, "total_frames": total, "total_s": round(total / fps, 3),
          "params": {"breath_s": breath, "breath_question_s": breath_question},
          "segments": segs, "voice": voice_track, "shots": shots, "cues": cues, "sfx": sfx, "music": []}
    dump_yaml(out / "timeline.yaml", tl)

    srt, k = [], 1
    for sg in segs:
        if sg["kind"] != "voice":
            continue
        for c in _subtitle_cues(sg, fps, max_chars, max_lines, round(min_sub_s * fps)):
            srt += [str(k), f"{_srt_time(c['start'], fps)} --> {_srt_time(c['end'], fps)}", *c["lines"], ""]
            k += 1
    (out / "subtitles.srt").write_text("\n".join(srt), encoding="utf-8")
    params = {"breath": breath, "breath_question": breath_question, "max_chars": max_chars, "max_lines": max_lines,
              "min_sub_s": min_sub_s}
    (out / "manifest.json").write_text(json.dumps({"hash": input_hash(project, params), "params": params},
                                                  ensure_ascii=False, indent=2), encoding="utf-8")
    return out / "timeline.yaml"
