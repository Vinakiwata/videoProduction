"""Tool 3 — lệnh hỗ trợ storyboard: init, view, preview, lint."""
from pathlib import Path

from vp import review
from vp.checklist import load_checklist
from vp.checks import CheckResult, run_check
from vp.checks.files import load_yaml
from vp.checks.script import segments
from vp.design_preview import render_all
from vp.project import dump_yaml

SB = "02_design/storyboard.yaml"
VIEW = "02_design/storyboard.md"


class DesignToolError(RuntimeError):
    pass


def init(project: Path, force: bool = False) -> Path:
    project = Path(project)
    g = review.gate(project, "script")
    if not g.ok:
        raise DesignToolError(f"Cổng 'script' chưa mở: {g.message}")
    dst = project / SB
    if dst.exists() and not force:
        raise DesignToolError(f"{dst} đã có. Dùng --force nếu thật sự muốn tạo lại.")
    brief = load_yaml(project, "00_brief/brief.yaml")
    script = load_yaml(project, "01_script/script.yaml")
    colors = list(brief["brand"]["colors"])
    bg, accent = colors[0], (colors[1] if len(colors) > 1 else colors[0])
    font = (brief["brand"].get("fonts") or ["Be Vietnam Pro"])[0]
    shots = []
    for _, seg in segments(script):
        sh = {
            "id": f"{seg['id']}-a", "segment": seg["id"], "span": [0, 1],
            "purpose": "TODO: khung này cho người xem thấy/hiểu điều gì",
            "background": bg, "focal": "e1", "camera": {"move": "static"}, "transition_in": "cut",
            "elements": [{"id": "e1", "asset": "A-TODO", "box": {"x": 25, "y": 20, "w": 50, "h": 55},
                          "enter": {"anim": "fade", "at": 0, "dur_s": 0.4, "ease": "ease_out"},
                          "notes": f"TODO: thiết kế theo mô tả: {seg.get('visual', '')}"}],
        }
        if seg.get("on_screen_text"):
            sh["elements"].append({"id": "e2", "text": seg["on_screen_text"], "style": "label", "font_px": 64,
                                   "color": accent, "box": {"x": 10, "y": 78, "w": 80, "h": 12},
                                   "enter": {"anim": "fade", "at": 0.2, "dur_s": 0.3, "ease": "ease_out"}})
        if seg.get("sfx"):
            sh["sfx"] = [{"name": n, "target": "e1", "event": "enter"} for n in seg["sfx"]]
        shots.append(sh)
    sb = {
        "meta": {"title": script["meta"]["title"], "canvas": dict(brief["format"])},
        "palette": colors,
        "fonts": {"title": font, "body": font},
        "style": brief["brand"].get("style") or "TODO: phong cách hình",
        "assets": [{"id": "A-TODO", "kind": "illustration", "description": "TODO: thay bằng các asset thật",
                    "colors": [accent]}],
        "shots": shots,
    }
    return dump_yaml(dst, sb)


def _cell(v):
    return str(v if v is not None else "").replace("|", "\\|").replace("\n", " / ")


def render_view(project: Path) -> str:
    sb = load_yaml(project, SB)
    script = load_yaml(project, "01_script/script.yaml")
    assets = {a["id"]: a for a in sb.get("assets") or []}
    by_seg = {}
    for sh in sb.get("shots") or []:
        by_seg.setdefault(sh["segment"], []).append(sh)
    out = [f"# Storyboard — {sb['meta']['title']}", "",
           "> Sinh tự động từ `storyboard.yaml` bằng `python -m vp design view`. Ảnh phác thảo: `storyboard.png`, `frames/`.",
           "", f"- **Bảng màu:** {', '.join(sb['palette'])}", f"- **Font:** {sb['fonts']['title']} / {sb['fonts']['body']}",
           f"- **Phong cách:** {sb['style']}", "", "## Thư viện asset", "", "| Mã | Loại | Mô tả | Màu |", "|---|---|---|---|"]
    out += [f"| {a['id']} | {a['kind']} | {_cell(a['description'])} | {', '.join(a['colors'])} |" for a in assets.values()]
    out.append("")
    for sc in script.get("scenes") or []:
        out += [f"## {sc['id']} · {sc['title']}", ""]
        for seg in sc.get("segments") or []:
            spoken = seg.get("text") or "*(im lặng)*"
            out += [f"### {seg['id']} — {spoken}", ""]
            for sh in sorted(by_seg.get(seg["id"], []), key=lambda s: s["span"][0]):
                out += [f"**{sh['id']}** · span {sh['span']} · vào: `{sh['transition_in']}` · camera: `{sh['camera']['move']}` · nền {sh['background']}",
                        f"*Mục đích:* {sh['purpose']}", "",
                        "| Phần tử | Nội dung | Hộp (x,y,w,h %) | Vào | Lặp | Ra |", "|---|---|---|---|---|---|"]
                for e in sh.get("elements") or []:
                    star = "⭐ " if e["id"] == sh["focal"] else ""
                    what = (f"chữ \"{_cell(e['text'])}\" ({e['style']}, {e['font_px']}px, {e['color']})" if "text" in e
                            else f"{e['asset']}")
                    b = e["box"]
                    fmt = lambda m: f"{m['anim']} @{m['at']:g}" + (f" {m['dur_s']:g}s" if m.get("dur_s") else "") if m else ""
                    out.append(f"| {star}{e['id']} | {what} | {b['x']:g},{b['y']:g},{b['w']:g},{b['h']:g} "
                               f"| {fmt(e.get('enter'))} | {(e.get('loop') or {}).get('anim', '')} | {fmt(e.get('exit'))} |")
                if sh.get("sfx"):
                    out.append("")
                    out.append("🔊 " + "; ".join(f"{x['name']} ← {x["target"]}.{x['event']}" for x in sh["sfx"]))
                if sh.get("notes"):
                    out += ["", f"*Ghi chú:* {sh['notes']}"]
                out.append("")
    return "\n".join(out)


def view(project: Path) -> Path:
    out = Path(project) / VIEW
    out.write_text(render_view(Path(project)), encoding="utf-8")
    return out


def preview(project: Path) -> Path:
    return render_all(Path(project))


def lint(project: Path, checklist_dir: Path | None = None) -> list[tuple[dict, CheckResult]]:
    cl = load_checklist("design", checklist_dir)
    return [(it, run_check(it["check"], Path(project), it.get("params")))
            for it in cl["items"] if it["method"] == "auto"]
