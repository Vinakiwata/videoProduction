"""Kiểm tra tự động cho web trình chiếu (07_presentation). Phần đo trên trình duyệt do
`python -m vp presentation check` thực hiện và ghi vào check/check_manifest.json; ở đây chỉ đọc và chấm."""
import hashlib
import json
import re
from pathlib import Path

from vp.checks import CheckResult, register
from vp.checks.files import load_yaml

DIR = "07_presentation"
BLANK_STDDEV = 2.0     # độ lệch chuẩn điểm ảnh dưới mức này = khung một màu


def _fmt(bad, head):
    return CheckResult("fail", head + "\n" + "\n".join(f"- {b}" for b in bad[:40]))


def _comp(project):
    p = project / DIR / "presentation.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None


def _manifest(project):
    p = project / DIR / "check" / "check_manifest.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None


NO_BUILD = CheckResult("fail", "Chưa có bản dựng. Chạy: python -m vp presentation build <dự án>")
NO_CHECK = CheckResult("fail", "Chưa có tờ kiểm. Chạy: python -m vp presentation check <dự án>")


@register("presentation_input_hash")
def input_in_sync(project: Path, params: dict) -> CheckResult:
    from vp.presentation_tools import input_hash
    comp = _comp(project)
    if comp is None:
        return NO_BUILD
    if comp.get("input_hash") != input_hash(project):
        return CheckResult("fail", "presentation.json đã cũ so với timeline/storyboard/hình/giọng. Chạy lại: python -m vp presentation build <dự án>")
    return CheckResult("pass", f"presentation.json khớp đầu vào: {len(comp['shots'])} khung hình, {comp['total_frames']} khung.")


@register("presentation_assets")
def assets_match(project: Path, params: dict) -> CheckResult:
    comp = _comp(project)
    if comp is None:
        return NO_BUILD
    bad = []
    for i, a in comp["assets"].items():
        src, dst = project / "06_animation" / a["file"], project / DIR / a["file"]
        if not dst.is_file():
            bad.append(f"{i}: thiếu {a['file']} trong 07_presentation")
        elif not src.is_file() or hashlib.sha256(src.read_bytes()).digest() != hashlib.sha256(dst.read_bytes()).digest():
            bad.append(f"{i}: khác bản ở 06_animation")
    if bad:
        return _fmt(bad, "Hình trong bản dựng không khớp 06_animation:")
    return CheckResult("pass", f"{len(comp['assets'])} hình có trong assets/ và trùng hash với 06_animation.")


@register("presentation_fonts")
def fonts_ok(project: Path, params: dict) -> CheckResult:
    comp = _comp(project)
    if comp is None:
        return NO_BUILD
    fams = sorted({v for v in (comp.get("fonts") or {}).values() if v})
    fdir = project / DIR / "fonts"
    files = comp.get("font_files") or []
    bad = []
    if not files:
        bad.append(f"Chưa có file font nhận diện ({', '.join(fams)}). Đặt file vào channels/<kênh>/brand/fonts/ rồi dựng lại.")
    if files and not any(fdir.glob(p) for p in ("OFL*", "LICENSE*", "license*", "*.txt")):
        bad.append("Thiếu file giấy phép font (OFL.txt) cạnh file font.")
    css = (project / DIR / "fonts.css")
    css = css.read_text(encoding="utf-8") if css.is_file() else ""
    for fam in fams:
        if not re.search(r"font-family:\s*'" + re.escape(fam) + "'", css):
            bad.append(f"fonts.css chưa khai '{fam}'.")
    man = _manifest(project)
    if man is not None and not bad:
        loaded = {re.sub(r"\s+\d+$", "", f) for f in man.get("fonts", [])}
        miss = [f for f in fams if f not in loaded]
        if miss:
            bad.append(f"Trình duyệt không nạp được font: {', '.join(miss)} (lần chụp kiểm gần nhất).")
    if bad:
        return _fmt(bad, "Font nhận diện chưa đạt:")
    return CheckResult("pass", f"Font {', '.join(fams)}: {len(files)} file kèm giấy phép, trình duyệt đã nạp.")


@register("presentation_render")
def render_ok(project: Path, params: dict) -> CheckResult:
    man = _manifest(project)
    if man is None:
        return NO_CHECK
    bad = [f"lỗi JS: {e}" for e in man["errors"]] + [f"console: {c}" for c in man["console"]]
    for r in man["frames"]:
        if r["size"] != [1920, 1080]:
            bad.append(f"khung {r['frame']}: cỡ {r['size'][0]}×{r['size'][1]}, phải 1920×1080")
        if r["max"] == 0:
            bad.append(f"khung {r['frame']} ({r['shot']}): đen toàn bộ")
        elif r["stddev"] < BLANK_STDDEV and r["role"] in ("mid", "end"):   # đầu khung hình được phép trống trước lượt vào đầu tiên
            bad.append(f"khung {r['frame']} ({r['shot']}, {r['role']}): trống, chỉ một màu")
    if bad:
        return _fmt(bad, "Dựng thử chưa sạch:")
    return CheckResult("pass", f"Dựng thử {len(man['frames'])} khung mốc 1920×1080: không lỗi JS hay console, không khung đen/trống.")


@register("presentation_deterministic")
def deterministic(project: Path, params: dict) -> CheckResult:
    man = _manifest(project)
    if man is None:
        return NO_CHECK
    det = man["determinism"]
    if det["mismatch"]:
        return _fmt([f"khung {f}" for f in det["mismatch"]], "Tua ngược cho ảnh khác tua xuôi (không tất định):")
    return CheckResult("pass", f"Tất định: {det['checked']} khung chụp xuôi rồi ngược trùng hash điểm ảnh.")


@register("presentation_text_fit")
def text_fit(project: Path, params: dict) -> CheckResult:
    man = _manifest(project)
    if man is None:
        return NO_CHECK
    bad = [f"khung {r['frame']}: {i}" for r in man["frames"] for i in r["issues"]]
    if bad:
        return _fmt(sorted(set(bad)), "Chữ tràn box hoặc ra ngoài vùng an toàn 5% (đo trong DOM):")
    return CheckResult("pass", f"Chữ nằm gọn trong box và trong vùng an toàn 5% ở {len(man['frames'])} khung mốc.")


@register("presentation_motion")
def motion_known(project: Path, params: dict) -> CheckResult:
    from vp.presentation_tools import ELEMENT_LOOPS, RECIPES
    comp = _comp(project)
    if comp is None:
        return NO_BUILD
    bad = []
    for aid, a in comp["assets"].items():
        f = project / DIR / a["file"]
        ids = set(re.findall(r'\sid="([^"]+)"', f.read_text(encoding="utf-8"))) if f.suffix == ".svg" and f.is_file() else set()
        for m in a.get("motion") or []:
            if m.get("recipe") not in RECIPES:
                bad.append(f"{aid}: công thức lạ '{m.get('recipe')}'")
            for lay in (m.get("layer"), m.get("paths_from")):
                if lay and lay not in ids:
                    bad.append(f"{aid}: không có lớp '{lay}' trong SVG")
            if m.get("recipe") == "along" and not (m.get("path") or m.get("paths_from") or m.get("paths")):
                bad.append(f"{aid}: along thiếu đường (path/paths_from/paths)")
    for s in comp["shots"]:
        for e in s["elements"]:
            lp = e.get("loop")
            if not lp:
                continue
            if lp["anim"] not in ELEMENT_LOOPS:
                bad.append(f"{s['id']}/{e['id']}: vòng lặp lạ '{lp['anim']}'")
            if e.get("kind") == "scene" and not e.get("layer_motion"):
                bad.append(f"{s['id']}/{e['id']}: cảnh {e.get('asset')} có loop '{lp['anim']}' nhưng asset chưa khai motion lớp")
    if bad:
        return _fmt(bad, "Chuyển động chưa có công thức tương ứng:")
    n = sum(len(a.get("motion") or []) for a in comp["assets"].values())
    return CheckResult("pass", f"Mọi vòng lặp phần tử và {n} chuyển động lớp đều có công thức; cảnh có loop đều chạy bằng lớp.")


@register("presentation_check_in_sync")
def check_in_sync(project: Path, params: dict) -> CheckResult:
    from vp.presentation_tools import build_hash
    man = _manifest(project)
    if man is None:
        return NO_CHECK
    if man.get("build_hash") != build_hash(project):
        return CheckResult("fail", "Tờ kiểm đã cũ so với bản dựng. Chạy lại: python -m vp presentation check <dự án>")
    if man.get("contact_build_hash") != man["build_hash"]:
        return CheckResult("fail", "Chưa có tờ ảnh khung mốc cho bản dựng này. Chạy: python -m vp presentation preview <dự án>")
    return CheckResult("pass", "Tờ kiểm và tờ ảnh khung mốc khớp bản dựng hiện tại.")
