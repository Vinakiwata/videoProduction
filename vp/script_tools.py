"""Tool 1 — lệnh hỗ trợ viết kịch bản: nhập bản thảo, ước thời lượng, kiểm nhanh, bản đọc."""
import math
import re
from pathlib import Path

from vp.channel import ChannelError, load_channel
from vp.checklist import load_checklist
from vp.checks import CheckResult, run_check
from vp.checks.files import load_yaml
from vp.checks.script import segments, syllables
from vp.project import dump_yaml
from vp.script_view import render_view

SCRIPT = "01_script/script.yaml"
VIEW = "01_script/script.md"
DEFAULT_SPS = 3.2
SPLIT_AT = 200
TODO_VISUAL = "TODO: mô tả hình"
TODO_PURPOSE = "TODO: mục đích cảnh"
SILENT = re.compile(r"^\((?:im lặng|nghỉ)\s*([\d.,]+)\s*(?:s|giây)?\)$", re.I)


class ScriptToolError(RuntimeError):
    pass


# ---------- ước lượng ----------

def estimate_seconds(text: str, sps: float) -> float:
    """Âm tiết / tốc độ, làm tròn lên 0,1 giây, tối thiểu 0,5 giây."""
    return max(0.5, math.ceil(syllables(text) / sps * 10 - 1e-9) / 10)


def resolve_sps(project: Path, sps: float | None, channels_dir: Path | None = None) -> float:
    if sps:
        return float(sps)
    brief = project / "00_brief" / "brief.yaml"
    if brief.is_file():
        ref = (load_yaml(project, "00_brief/brief.yaml") or {}).get("channel_ref")
        if ref:
            try:
                return float(load_channel(ref, channels_dir, validate=False)["voice_profile"]["syllables_per_second"])
            except (ChannelError, KeyError):
                pass
    return DEFAULT_SPS


def estimate(project: Path, sps: float | None = None, channels_dir: Path | None = None) -> int:
    project = Path(project)
    rate = resolve_sps(project, sps, channels_dir)
    s = load_yaml(project, SCRIPT)
    n = 0
    for _, seg in segments(s):
        if seg.get("kind") == "voice" and seg.get("text"):
            seg["est_duration_s"] = estimate_seconds(seg["text"], rate)
            n += 1
    dump_yaml(project / SCRIPT, s)
    return n


# ---------- nhập bản thảo ----------

def _split_sentences(par: str) -> list[str]:
    return [x.strip() for x in re.split(r"(?<=[.!?…])\s+", par.strip()) if x.strip()]


def _split_long(sentence: str, limit: int) -> list[str]:
    if len(sentence) <= limit:
        return [sentence]
    pieces = [p.strip() for p in re.split(r"(?<=[,;:])\s+", sentence)]
    out, cur = [], ""
    for p in pieces:
        if len(p) > limit:  # một vế vẫn quá dài -> tách theo từ
            words, buf = p.split(), ""
            for w in words:
                if buf and len(buf) + 1 + len(w) > limit:
                    out.append(buf); buf = w
                else:
                    buf = f"{buf} {w}".strip()
            p = buf
        if cur and len(cur) + 1 + len(p) > limit:
            out.append(cur); cur = p
        else:
            cur = f"{cur} {p}".strip()
    if cur:
        out.append(cur)
    return out


def _group(sentences: list[str], limit: int) -> list[str]:
    """Gộp câu ngắn liền nhau trong một đoạn văn cho tới ngưỡng, tách câu dài."""
    out, cur = [], ""
    for sen in sentences:
        for part in _split_long(sen, limit):
            if cur and len(cur) + 1 + len(part) > limit:
                out.append(cur); cur = part
            else:
                cur = f"{cur} {part}".strip()
    if cur:
        out.append(cur)
    return out


def import_draft(project: Path, src: Path, force: bool = False, limit: int = SPLIT_AT,
                 sps: float | None = None, channels_dir: Path | None = None) -> Path:
    project = Path(project)
    dst = project / SCRIPT
    if dst.exists() and not force:
        raise ScriptToolError(f"{dst} đã có. Dùng --force nếu thật sự muốn ghi đè.")
    brief = load_yaml(project, "00_brief/brief.yaml")
    rate = resolve_sps(project, sps, channels_dir)

    scenes: list[dict] = []

    def scene(title):
        sc = {"id": f"S{len(scenes) + 1:02d}", "title": title, "purpose": TODO_PURPOSE, "segments": []}
        scenes.append(sc)
        return sc

    def add(sc, seg):
        seg = {"id": f"{sc['id']}-{len(sc['segments']) + 1:02d}", **seg}
        sc["segments"].append(seg)
        return seg

    cur, last, para = None, None, []

    def flush():
        nonlocal cur, last, para
        if not para:
            return
        cur = cur or scene("Mở đầu")
        for text in _group(_split_sentences(" ".join(para)), limit):
            last = add(cur, {"kind": "voice", "text": text, "est_duration_s": estimate_seconds(text, rate),
                             "visual": TODO_VISUAL})
        para = []

    for raw in Path(src).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            flush(); continue
        if line.startswith("#"):
            flush(); cur = scene(line.lstrip("#").strip() or f"Cảnh {len(scenes) + 1}"); last = None; continue
        if line.startswith(">"):
            flush()
            note = line.lstrip(">").strip()
            if last is not None:
                last["visual"] = note if last["visual"] == TODO_VISUAL else f"{last['visual']}; {note}"
            continue
        m = SILENT.match(line)
        if m:
            flush(); cur = cur or scene("Mở đầu")
            last = add(cur, {"kind": "silent", "est_duration_s": float(m.group(1).replace(",", ".")),
                             "visual": TODO_VISUAL})
            continue
        para.append(line)
    flush()
    scenes = [sc for sc in scenes if sc["segments"]]
    if not scenes:
        raise ScriptToolError(f"Bản thảo {src} không có lời đọc nào.")

    script = {
        "meta": {"title": brief["title"], "language": "vi", "target_duration_s": brief["target_duration_s"],
                 "audience": brief["audience"], "goal": brief["goal"]},
        "sources": [],
        "scenes": scenes,
    }
    return dump_yaml(dst, script)


# ---------- bản đọc & kiểm nhanh ----------

def view(project: Path) -> Path:
    project = Path(project)
    out = project / VIEW
    out.write_text(render_view(load_yaml(project, SCRIPT)), encoding="utf-8")
    return out


def lint(project: Path, checklist_dir: Path | None = None) -> list[tuple[dict, CheckResult]]:
    """Chạy các mục tự động của checklist 'script' — không mở lần duyệt, không ghi nhật ký."""
    cl = load_checklist("script", checklist_dir)
    return [(it, run_check(it["check"], Path(project), it.get("params")))
            for it in cl["items"] if it["method"] == "auto"]
