"""Ảnh phác thảo (wireframe) cho storyboard: mỗi khung 1 ảnh + 1 tờ tổng hợp."""
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from vp.checks.design import Ctx, _overflow, contrast_ratio
from vp.checks.files import load_yaml

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
W, H = 960, 540
THUMB_W, THUMB_H, GAP, COLS, CAPTION_H = 480, 270, 16, 4, 96


def content_hash(project: Path, sb_rel: str, script_rel: str) -> str:
    data = {"sb": load_yaml(project, sb_rel), "script": load_yaml(project, script_rel)}
    return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()


def _font(size, bold=False):
    try:
        return ImageFont.truetype(FONT_B if bold else FONT, max(8, int(size)))
    except OSError:
        return ImageFont.load_default()


def _rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def _ink_for(bg_hex):
    """Màu nét phụ (nhãn, khung) dễ thấy trên nền."""
    return "#FFFFFF" if contrast_ratio("#FFFFFF", bg_hex) >= contrast_ratio("#1B1B1F", bg_hex) else "#1B1B1F"


def _wrap(draw, text, font, width):
    out = []
    for para in str(text).split("\n"):
        line = ""
        for w in para.split():
            t = f"{line} {w}".strip()
            if draw.textlength(t, font=font) <= width or not line:
                line = t
            else:
                out.append(line); line = w
        out.append(line)
    return out


def _text_in_box(draw, xy, text, font, fill, max_h, spacing=1.15):
    x0, y0, x1, _ = xy
    lh = font.size * spacing
    y = y0
    for ln in _wrap(draw, text, font, max(10, x1 - x0)):
        if y + lh > y0 + max_h + 1:
            break
        draw.text((x0, y), ln, font=font, fill=fill)
        y += lh


def render_frame(shot: dict, assets: dict, canvas: dict | None = None) -> Image.Image:
    im = Image.new("RGB", (W, H), _rgb(shot["background"]))
    d = ImageDraw.Draw(im, "RGBA")
    ink = _ink_for(shot["background"])
    m = 0.05
    d.rectangle([W * m, H * m, W * (1 - m), H * (1 - m)], outline=_rgb(ink) + (60,), width=1)
    els = sorted(enumerate(shot.get("elements") or []), key=lambda p: (p[1].get("z", 0), p[0]))
    for _, e in els:
        b = e["box"]
        box = [W * b["x"] / 100, H * b["y"] / 100, W * (b["x"] + b["w"]) / 100, H * (b["y"] + b["h"]) / 100]
        focal = e["id"] == shot.get("focal")
        if "text" in e:
            f = _font(e["font_px"] * W / 1920, bold=e["style"] == "title")
            _text_in_box(d, box, e["text"], f, _rgb(e["color"]), box[3] - box[1])
            over = _overflow(e, canvas or {"width": 1920, "height": 1080})
            d.rectangle(box, outline=(255, 60, 60, 255) if over else _rgb(ink) + (90,), width=3 if over else 1)
        else:
            a = assets.get(e["asset"], {"colors": ["#888888"], "description": e["asset"]})
            fill = _rgb(a["colors"][0]) + (150,)
            edge = _rgb(a["colors"][1] if len(a["colors"]) > 1 else ink) + (230,)
            d.rounded_rectangle(box, radius=10, fill=fill, outline=edge, width=2)
            lab = _ink_for(a["colors"][0])
            pad = 6
            _text_in_box(d, [box[0] + pad, box[1] + pad, box[2] - pad, box[3]], e["asset"], _font(15, True),
                         _rgb(lab), max(0, box[3] - box[1] - 2 * pad))
            _text_in_box(d, [box[0] + pad, box[1] + pad + 20, box[2] - pad, box[3]], a["description"], _font(12),
                         _rgb(lab) + (220,), max(0, box[3] - box[1] - 2 * pad - 20))
        motion = []
        if e.get("enter"):
            motion.append(f"▶{e['enter']['anim']}@{e['enter']['at']:g}")
        if e.get("loop"):
            motion.append(f"↻{e['loop']['anim']}")
        if e.get("exit"):
            motion.append(f"■{e['exit']['anim']}@{e['exit']['at']:g}")
        tag = (f"★ {e['id']}" if focal else e["id"]) + (" " + " ".join(motion) if motion else "")
        f = _font(12, focal)
        tw = d.textlength(tag, font=f)
        tx, ty = max(0, min(box[0], W - tw - 4)), max(0, min(box[3] - 16, H - 16))
        d.rectangle([tx, ty, tx + tw + 4, ty + 15], fill=(0, 0, 0, 150))
        d.text((tx + 2, ty), tag, font=f, fill=(255, 210, 63) if focal else (255, 255, 255))
        if focal:
            d.rectangle(box, outline=(255, 210, 63, 255), width=3)
    head = f"{shot['id']}  ·  vào: {shot['transition_in']}  ·  camera: {shot['camera']['move']}"
    f = _font(14, True)
    d.rectangle([0, 0, d.textlength(head, font=f) + 12, 22], fill=(0, 0, 0, 170))
    d.text((6, 3), head, font=f, fill=(255, 255, 255))
    return im


def render_all(project: Path, sb_rel="02_design/storyboard.yaml", script_rel="01_script/script.yaml") -> Path:
    project = Path(project)
    c = Ctx(project, {"path": sb_rel, "script": script_rel})
    assets = {a["id"]: a for a in c.sb.get("assets") or []}
    out_dir = project / "02_design" / "frames"
    out_dir.mkdir(parents=True, exist_ok=True)
    shots = c.sb.get("shots") or []
    names = []
    thumbs = []
    for sh in shots:
        im = render_frame(sh, assets, c.sb["meta"]["canvas"])
        name = f"{sh['id']}.png"
        im.save(out_dir / name, optimize=True)
        names.append(name)
        thumbs.append((sh, im.resize((THUMB_W, THUMB_H))))
    for old in out_dir.glob("*.png"):
        if old.name not in names:
            old.unlink()

    rows = max(1, (len(thumbs) + COLS - 1) // COLS)
    sheet_w = COLS * THUMB_W + (COLS + 1) * GAP
    sheet_h = rows * (THUMB_H + CAPTION_H) + (rows + 1) * GAP + 50
    sheet = Image.new("RGB", (sheet_w, sheet_h), (24, 24, 28))
    d = ImageDraw.Draw(sheet)
    d.text((GAP, 14), f"Storyboard — {c.sb['meta']['title']}  ({len(shots)} khung, ~{c.total:.1f}s)",
           font=_font(22, True), fill=(255, 255, 255))
    for i, (sh, th) in enumerate(thumbs):
        r, col = divmod(i, COLS)
        x = GAP + col * (THUMB_W + GAP)
        y = 50 + GAP + r * (THUMB_H + CAPTION_H + GAP)
        sheet.paste(th, (x, y))
        seg = c.seg.get(sh["segment"], {})
        t0 = c.shot_start(sh)
        cap = f"{sh['id']}  {int(t0 // 60):02d}:{t0 % 60:04.1f}  ({c.shot_dur(sh):.1f}s)"
        d.text((x, y + THUMB_H + 4), cap, font=_font(14, True), fill=(255, 210, 63))
        spoken = seg.get("text") or "(im lặng)"
        _text_in_box(d, [x, y + THUMB_H + 24, x + THUMB_W, 0], f"Lời: {spoken}" if seg.get("text") else spoken,
                     _font(13), (220, 220, 220), CAPTION_H - 26)
    out = project / "02_design" / "storyboard.png"
    sheet.save(out, optimize=True)
    (out_dir / "manifest.json").write_text(json.dumps(
        {"hash": content_hash(project, sb_rel, script_rel), "frames": names}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    return out
