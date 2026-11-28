"""Kiểm tra tự động cho hoạt ảnh 2D (06_animation): file SVG, màu, lớp, an toàn nhấp nháy."""
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from vp.checks import CheckResult, register
from vp.checks.files import load_yaml

SVGNS = "{http://www.w3.org/2000/svg}"
COLOR_ATTRS = ("fill", "stroke", "stop-color", "flood-color", "color")
ALLOWED_KEYWORDS = {"none", "transparent", "currentcolor", "inherit"}
FORBIDDEN = {"image", "script", "foreignObject"}
FLASHY = {"pulse", "blink_slow", "shimmer"}


def _fmt(bad, head):
    return CheckResult("fail", head + "\n" + "\n".join(f"- {b}" for b in bad[:40]))


def _manifest(project, params):
    man = load_yaml(project, params["path"])
    base = (project / params["path"]).parent
    return man, base


def _tag(el):
    return el.tag.split("}", 1)[-1]


def _colors(el):
    """Màu khai ở thuộc tính và trong style="…"."""
    vals = [el.get(a) for a in COLOR_ATTRS if el.get(a)]
    style = el.get("style") or ""
    for decl in style.split(";"):
        if ":" in decl:
            k, v = decl.split(":", 1)
            if k.strip() in COLOR_ATTRS:
                vals.append(v.strip())
    return vals


def assets_hash(project: Path, params: dict) -> str:
    man, base = _manifest(project, params)
    h = hashlib.sha256()
    for a in man.get("assets") or []:
        f = base / a["file"]
        h.update(a["id"].encode())
        h.update(f.read_bytes() if f.is_file() else b"-")
    return h.hexdigest()


@register("animation_assets_complete")
def assets_complete(project: Path, params: dict) -> CheckResult:
    man, base = _manifest(project, params)
    sb = load_yaml(project, params.get("storyboard", "02_design/storyboard.yaml"))
    want = [a["id"] for a in sb.get("assets") or []]
    have = {a["id"]: a for a in man.get("assets") or []}
    bad = [f"{i}: chưa có trong assets.yaml" for i in want if i not in have]
    bad += [f"{i}: không có trong storyboard" for i in have if i not in want]
    for i, a in have.items():
        if not (base / a.get("file", "")).is_file():
            bad.append(f"{i}: thiếu file {a.get('file')}")
        for k in ("source", "license"):
            if not str(a.get(k) or "").strip():
                bad.append(f"{i}: thiếu '{k}'")
    if bad:
        return _fmt(bad, "Danh mục hình chưa đủ:")
    return CheckResult("pass", f"{len(have)} hình đủ file, có nguồn và giấy phép, khớp thư viện storyboard.")


@register("svg_valid")
def svg_valid(project: Path, params: dict) -> CheckResult:
    man, base = _manifest(project, params)
    brief = load_yaml(project, params.get("brief", "00_brief/brief.yaml"))
    fonts = [f.lower() for f in brief["brand"]["fonts"]]
    bad = []
    for a in man.get("assets") or []:
        f = base / a["file"]
        if not f.is_file() or a.get("kind") == "mascot":
            continue
        try:
            root = ET.fromstring(f.read_text(encoding="utf-8"))
        except ET.ParseError as e:
            bad.append(f"{a['id']}: XML không hợp lệ ({e})")
            continue
        if _tag(root) != "svg":
            bad.append(f"{a['id']}: phần tử gốc không phải <svg>")
        if not root.get("viewBox"):
            bad.append(f"{a['id']}: thiếu viewBox")
        for el in root.iter():
            t = _tag(el)
            if t in FORBIDDEN:
                bad.append(f"{a['id']}: có <{t}> (không cho phép ảnh/script/nhúng ngoài)")
            for k, v in el.attrib.items():
                if k.endswith("href") and v and not v.startswith("#"):
                    bad.append(f"{a['id']}: tham chiếu ra ngoài {k}={v[:60]}")
            if t == "text":
                fam = (el.get("font-family") or "").split(",")[0].strip().strip("'\"").lower()
                if fam not in fonts:
                    bad.append(f"{a['id']}: chữ dùng font '{el.get('font-family')}' ngoài bộ nhận diện {brief['brand']['fonts']}")
    if bad:
        return _fmt(bad, "File SVG không hợp lệ:")
    n = sum(1 for a in man.get("assets") or [] if a.get("kind") != "mascot")
    return CheckResult("pass", f"{n} file SVG hợp lệ, có viewBox, không ảnh/script/nguồn ngoài, chữ đúng font.")


@register("svg_palette")
def svg_palette(project: Path, params: dict) -> CheckResult:
    man, base = _manifest(project, params)
    brief = load_yaml(project, params.get("brief", "00_brief/brief.yaml"))
    pal = {c.upper() for c in brief["brand"]["colors"]}
    scene_pal = pal | {c.upper() for c in brief["brand"].get("scene_colors") or []}
    mx_icon = int(params.get("max_colors", 4))
    mx_scene = int(params.get("max_scene_colors", 16))
    bad, per = [], {}
    for a in man.get("assets") or []:
        if a.get("kind") == "mascot":
            continue
        is_scene = a.get("kind") == "scene"
        ok, mx = (scene_pal, mx_scene) if is_scene else (pal, mx_icon)
        f = base / a["file"]
        if not f.is_file():
            continue
        try:
            root = ET.fromstring(f.read_text(encoding="utf-8"))
        except ET.ParseError:
            continue
        used = set()
        for el in root.iter():
            for v in _colors(el):
                v2 = v.strip()
                if v2.lower() in ALLOWED_KEYWORDS or v2.startswith("url("):
                    continue
                m = re.fullmatch(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})", v2)
                if not m:
                    bad.append(f"{a['id']}: màu '{v2}' không phải mã hex (#RRGGBB)")
                    continue
                hx = v2.upper() if len(v2) == 7 else "#" + "".join(ch * 2 for ch in v2[1:]).upper()
                used.add(hx)
                if hx not in ok:
                    where = "bảng màu cảnh (brand.colors + brand.scene_colors)" if is_scene else f"bảng màu nhận diện {sorted(pal)}"
                    bad.append(f"{a['id']}: màu {v2} ngoài {where}")
        per[a["id"]] = len(used)
        if len(used) > mx:
            bad.append(f"{a['id']}: dùng {len(used)} màu > {mx}" + (" (cảnh)" if is_scene else ""))
    if bad:
        return _fmt(bad, "Màu SVG không đạt:")
    scenes = [k for k, a in ((a["id"], a) for a in man.get("assets") or []) if a.get("kind") == "scene"]
    icons = [v for k, v in per.items() if k not in scenes]
    sc = [v for k, v in per.items() if k in scenes]
    msg = f"Icon/chữ/nút chỉ dùng màu nhận diện, nhiều nhất {max(icons or [0])} màu/hình (≤ {mx_icon})"
    if sc:
        msg += f"; {len(sc)} cảnh dùng màu tự nhiên đã duyệt, nhiều nhất {max(sc)} màu/cảnh (≤ {mx_scene})"
    return CheckResult("pass", msg + ".")


@register("svg_layers")
def svg_layers(project: Path, params: dict) -> CheckResult:
    man, base = _manifest(project, params)
    bad, n = [], 0
    for a in man.get("assets") or []:
        f = base / a["file"]
        if not f.is_file() or not a.get("layers") or a.get("kind") == "mascot":
            continue
        try:
            root = ET.fromstring(f.read_text(encoding="utf-8"))
        except ET.ParseError:
            continue
        ids = {el.get("id") for el in root.iter() if _tag(el) == "g" and el.get("id")}
        for layer in a["layers"]:
            n += 1
            if layer not in ids:
                bad.append(f"{a['id']}: thiếu lớp <g id=\"{layer}\">")
    if bad:
        return _fmt(bad, "Thiếu lớp tách để làm chuyển động:")
    return CheckResult("pass", f"{n} lớp khai báo đều có trong file SVG.")


@register("animation_flash_safety")
def flash_safety(project: Path, params: dict) -> CheckResult:
    t = load_yaml(project, params["path"])
    fps = float(t["fps"])
    mn = float(params.get("min_period_s", 0.4))
    bad, n = [], 0
    for c in t.get("cues") or []:
        if c.get("event") == "loop" and c.get("anim") in FLASHY:
            n += 1
            per = float(c.get("period_frames") or 0) / fps
            if per < mn:
                bad.append(f"{c['shot']}/{c['element']}: {c['anim']} chu kỳ {per:.2f}s < {mn}s ({1 / per if per else float('inf'):.1f} lần/giây)")
    if bad:
        return _fmt(bad, "Nguy cơ nhấp nháy (WCAG 2.3.1):")
    return CheckResult("pass", f"{n} vòng lặp sáng/tối đều có chu kỳ ≥ {mn}s (≤ {1 / mn:.1f} lần/giây).")


@register("animation_preview_in_sync")
def preview_in_sync(project: Path, params: dict) -> CheckResult:
    mp = project / params["manifest"]
    if not mp.is_file():
        return CheckResult("fail", "Chưa có tờ xem trước. Chạy: python -m vp animation preview <dự án>")
    if json.loads(mp.read_text(encoding="utf-8")).get("hash") != assets_hash(project, params):
        return CheckResult("fail", "Tờ xem trước đã cũ so với file SVG. Chạy lại: python -m vp animation preview <dự án>")
    return CheckResult("pass", "Tờ xem trước khớp các file SVG hiện tại.")


@register("mascot_png")
def mascot_png(project: Path, params: dict) -> CheckResult:
    """Linh vật PNG: nền trong suốt, trùng đúng bản gốc của kênh, không bị phóng to quá cỡ file khi lên hình."""
    from PIL import Image
    man, base = _manifest(project, params)
    brief = load_yaml(project, params.get("brief", "00_brief/brief.yaml"))
    sb = load_yaml(project, params.get("storyboard", "02_design/storyboard.yaml"))
    m = brief["brand"].get("mascot") or {}
    exprs = {e["id"]: e for e in m.get("expressions") or []}
    kinds = {a["id"]: a for a in sb.get("assets") or []}
    cw, ch = (sb.get("meta") or {}).get("canvas", {}).get("width", 1920), (sb.get("meta") or {}).get("canvas", {}).get("height", 1080)
    need = {}
    for sh in sb.get("shots") or []:
        for e in sh.get("elements") or []:
            if kinds.get(e.get("asset"), {}).get("kind") == "mascot":
                b = e["box"]
                need[e["asset"]] = max(need.get(e["asset"], 0), b["w"] * cw / 100, b["h"] * ch / 100)
    bad, n = [], 0
    for a in man.get("assets") or []:
        if a.get("kind") != "mascot":
            continue
        n += 1
        f = base / a["file"]
        if not f.is_file():
            continue
        im = Image.open(f)
        if im.format != "PNG" or im.mode != "RGBA":
            bad.append(f"{a['id']}: phải là PNG RGBA (đang {im.format} {im.mode})")
            continue
        al = im.getchannel("A")
        corners = [al.getpixel(p) for p in ((0, 0), (im.width - 1, 0), (0, im.height - 1), (im.width - 1, im.height - 1))]
        if max(corners) > 10 or al.getextrema()[0] > 10:
            bad.append(f"{a['id']}: nền chưa trong suốt (góc ảnh alpha {corners})")
        side = max(im.size)
        if need.get(a["id"], 0) > side * 1.0:
            bad.append(f"{a['id']}: lên hình {need[a['id']]:.0f} px nhưng file chỉ {side} px → bị phóng to, sẽ mờ")
        ex = exprs.get(kinds.get(a["id"], {}).get("expression"))
        if not ex:
            bad.append(f"{a['id']}: không tìm thấy biểu cảm trong brand.mascot")
            continue
        src = project.parents[1] / m["dir"] / ex["file"]
        if not src.is_file():
            bad.append(f"{a['id']}: thiếu bản gốc {m['dir']}/{ex['file']}")
        elif hashlib.sha256(src.read_bytes()).digest() != hashlib.sha256(f.read_bytes()).digest():
            bad.append(f"{a['id']}: file khác bản gốc của kênh ({m['dir']}/{ex['file']}) — chạy 'python -m vp animation sync'")
    if bad:
        return _fmt(bad, "Linh vật PNG chưa đạt:")
    return CheckResult("pass", f"{n} hình linh vật: PNG nền trong suốt, trùng bản gốc của kênh, không phóng to quá cỡ file.")
