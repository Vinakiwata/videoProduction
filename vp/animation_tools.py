"""Tool 6 — Hoạt ảnh 2D: danh mục hình SVG, xem trước, kiểm nhanh. Xem spec 2026-11-28-tool-hoat-anh-design.md."""
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

from vp import review
from vp.checklist import load_checklist
from vp.checks import CheckResult, run_check
from vp.checks.animation import assets_hash
from vp.checks.files import load_yaml
from vp.design_preview import _font, _text_in_box
from vp.project import dump_yaml

DIR = "06_animation"
CELL, PAD, COLS, CAP = 300, 14, 4, 70


class AnimationToolError(RuntimeError):
    pass


def _entry(a: dict) -> dict:
    if a["kind"] == "mascot":
        return {"id": a["id"], "file": f"assets/{a['id']}.png", "kind": "mascot", "description": a["description"], "layers": [],
                "source": f"Bộ nhận diện kênh — linh vật, biểu cảm '{a.get('expression')}' (chép từ brand.mascot, không sửa)",
                "license": "Thuộc chủ dự án (bộ nhận diện do chủ dự án cung cấp)", "notes": ""}
    return {"id": a["id"], "file": f"assets/{a['id']}.svg", "kind": a["kind"], "description": a["description"],
            "layers": [], "source": "Thiết kế gốc — SVG viết bằng code trong dây chuyền videoProduction",
            "license": "Thuộc chủ dự án (không dùng tài nguyên bên thứ ba)", "notes": ""}


def _copy_mascots(project: Path, sb: dict) -> list[str]:
    """Chép PNG linh vật từ kho của kênh (brand.mascot.dir) vào 06_animation/assets — luôn là bản gốc, không sửa."""
    brief = load_yaml(project, "00_brief/brief.yaml")
    m = brief["brand"].get("mascot")
    out = []
    if not m:
        return out
    ex = {e["id"]: e for e in m["expressions"]}
    for a in sb.get("assets") or []:
        if a["kind"] != "mascot":
            continue
        e = ex.get(a.get("expression"))
        if not e:
            raise AnimationToolError(f"{a['id']}: biểu cảm '{a.get('expression')}' không có trong brand.mascot")
        src = project.parents[1] / m["dir"] / e["file"]
        if not src.is_file():
            raise AnimationToolError(f"{a['id']}: không thấy {src}")
        dst = project / DIR / "assets" / f"{a['id']}.png"
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        out.append(a["id"])
    return out


def init(project: Path, force: bool = False) -> Path:
    project = Path(project)
    g = review.gate(project, "timeline")
    if not g.ok:
        raise AnimationToolError(f"Cổng 'timeline' chưa mở: {g.message}")
    dst = project / DIR / "assets.yaml"
    if dst.exists() and not force:
        raise AnimationToolError(f"{dst} đã có. Dùng --force nếu thật sự muốn tạo lại.")
    sb = load_yaml(project, "02_design/storyboard.yaml")
    man = {"assets": [_entry(a) for a in sb.get("assets") or []]}
    (project / DIR / "assets").mkdir(parents=True, exist_ok=True)
    _copy_mascots(project, sb)
    return dump_yaml(dst, man)


def sync(project: Path) -> Path:
    """Khớp assets.yaml với storyboard sau khi storyboard đổi: thêm asset mới, bỏ asset đã xoá,
    cập nhật kind/mô tả; GIỮ nguyên layers, notes và các khoá khác (motion_defaults); chép lại PNG linh vật."""
    project = Path(project)
    dst = project / DIR / "assets.yaml"
    sb = load_yaml(project, "02_design/storyboard.yaml")
    man = load_yaml(project, f"{DIR}/assets.yaml") if dst.exists() else {}
    old = {a["id"]: a for a in man.get("assets") or []}
    new = []
    for a in sb.get("assets") or []:
        e = _entry(a)
        if a["id"] in old:
            keep = dict(old[a["id"]])
            keep.update(kind=e["kind"], description=e["description"], file=e["file"])
            if e["kind"] == "mascot":
                keep.update(source=e["source"], license=e["license"])
            e = keep
        new.append(e)
    man["assets"] = new
    _copy_mascots(project, sb)
    return dump_yaml(dst, man)


def _render_svg(svg: Path, size: int) -> Image.Image:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "a.png"
        subprocess.run(["rsvg-convert", "-a", "-w", str(size), "-h", str(size), "-o", str(out), str(svg)],
                       check=True, capture_output=True)
        return Image.open(out).convert("RGBA").copy()


def preview(project: Path) -> Path:
    """Mỗi hình dựng trên nửa nền tối (#1B1B1F) và nửa nền xanh (#0B3D91) để thấy rõ trên cả hai nền đang dùng."""
    project = Path(project)
    params = {"path": f"{DIR}/assets.yaml"}
    man = load_yaml(project, params["path"])
    brief = load_yaml(project, "00_brief/brief.yaml")
    cols = brief["brand"]["colors"]
    bg_a, bg_b = (cols[3] if len(cols) > 3 else "#1B1B1F"), cols[0]
    assets = man.get("assets") or []
    rows = max(1, (len(assets) + COLS - 1) // COLS)
    W = COLS * CELL + (COLS + 1) * PAD
    H = rows * (CELL + CAP) + (rows + 1) * PAD + 44
    sheet = Image.new("RGB", (W, H), (40, 40, 44))
    d = ImageDraw.Draw(sheet)
    d.text((PAD, 12), f"Hình SVG — {project.name} ({len(assets)} hình) · nền trái {bg_a}, nền phải {bg_b}",
           font=_font(20, True), fill=(255, 255, 255))
    for i, a in enumerate(assets):
        r, c = divmod(i, COLS)
        x, y = PAD + c * (CELL + PAD), 44 + PAD + r * (CELL + CAP + PAD)
        cell = Image.new("RGB", (CELL, CELL), bg_a)
        ImageDraw.Draw(cell).rectangle([CELL // 2, 0, CELL, CELL], fill=bg_b)
        f = project / DIR / a["file"]
        if f.is_file():
            try:
                if f.suffix.lower() == ".png":
                    im = Image.open(f).convert("RGBA"); im.thumbnail((CELL - 20, CELL - 20))
                else:
                    im = _render_svg(f, CELL - 20)
                cell.paste(im, ((CELL - im.width) // 2, (CELL - im.height) // 2), im)
            except subprocess.CalledProcessError:
                ImageDraw.Draw(cell).text((10, 10), "LỖI DỰNG SVG", font=_font(18, True), fill=(255, 60, 60))
        else:
            ImageDraw.Draw(cell).text((10, 10), "CHƯA CÓ FILE", font=_font(18, True), fill=(255, 60, 60))
        sheet.paste(cell, (x, y))
        d.text((x, y + CELL + 4), a["id"], font=_font(15, True), fill=(255, 210, 63))
        _text_in_box(d, [x, y + CELL + 24, x + CELL, 0], a.get("description", ""), _font(11), (210, 210, 210), CAP - 26)
    out = project / DIR / "assets_preview.png"
    sheet.save(out, optimize=True)
    (project / DIR / "preview_manifest.json").write_text(
        json.dumps({"hash": assets_hash(project, params)}, indent=2), encoding="utf-8")
    return out


def lint(project: Path, checklist_dir: Path | None = None) -> list[tuple[dict, CheckResult]]:
    cl = load_checklist("animation", checklist_dir)
    return [(it, run_check(it["check"], Path(project), it.get("params")))
            for it in cl["items"] if it["method"] == "auto"]
