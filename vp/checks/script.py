"""Kiểm tra tự động cho kịch bản (01_script/script.yaml)."""
import re
from collections import Counter
from pathlib import Path

from vp.checks import CheckResult, register
from vp.checks.files import load_yaml

# Thẻ cảm xúc VieNeu-TTS là hợp lệ, không phải chỗ trống.
EMOTION_TAGS = {"cười", "thở dài", "hắng giọng"}
PLACEHOLDER = re.compile(r"\b(TODO|TBD|FIXME|XXX|lorem ipsum)\b|\?\?\?|\.\.\.\.|\{\{|\}\}", re.I)
BRACKET = re.compile(r"\[([^\]]*)\]")


def segments(script):
    for scene in script.get("scenes") or []:
        for seg in scene.get("segments") or []:
            yield scene, seg


def spoken(text: str) -> str:
    """Bỏ thẻ cảm xúc để còn lại phần được đọc thành tiếng."""
    return BRACKET.sub(lambda m: "" if m.group(1).strip() in EMOTION_TAGS else m.group(0), text)


def syllables(text: str) -> int:
    return sum(1 for tok in spoken(text).split() if re.search(r"\w", tok))


def _fmt(bad: list[str], head: str) -> CheckResult:
    return CheckResult("fail", head + "\n" + "\n".join(f"- {b}" for b in bad))


@register("script_unique_ids")
def unique_ids(project: Path, params: dict) -> CheckResult:
    s = load_yaml(project, params["path"])
    ids = [sc["id"] for sc in s.get("scenes", [])] + [seg["id"] for _, seg in segments(s)]
    dup = [i for i, n in Counter(ids).items() if n > 1]
    if dup:
        return _fmt(dup, "Mã cảnh/đoạn bị trùng:")
    return CheckResult("pass", f"{len(ids)} mã cảnh/đoạn, không trùng.")


@register("script_source_refs")
def source_refs(project: Path, params: dict) -> CheckResult:
    s = load_yaml(project, params["path"])
    known = {src["id"] for src in s.get("sources") or []}
    bad = [f"{seg['id']} trỏ tới nguồn không có: {sid}"
           for _, seg in segments(s) for sid in seg.get("source_ids") or [] if sid not in known]
    if bad:
        return _fmt(bad, "Tham chiếu nguồn bị hỏng:")
    used = sum(1 for _, seg in segments(s) if seg.get("source_ids"))
    return CheckResult("pass", f"{len(known)} nguồn, {used} đoạn có trích nguồn, mọi tham chiếu hợp lệ.")


def _walk(node, label):
    """Duyệt mọi chuỗi; nhãn dùng mã 'id' gần nhất nếu có (vd. S01-01.text)."""
    if isinstance(node, dict):
        base = node.get("id", label) if isinstance(node.get("id"), str) else label
        for k, v in node.items():
            yield from _walk(v, f"{base}.{k}" if base else str(k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from _walk(v, f"{label}[{i}]")
    elif isinstance(node, str):
        yield label, node


@register("no_placeholders")
def no_placeholders(project: Path, params: dict) -> CheckResult:
    data = load_yaml(project, params["path"])
    bad = []
    for label, val in _walk(data, ""):
        m = PLACEHOLDER.search(val)
        if m:
            bad.append(f"{label}: '{m.group(0)}'")
        if label.endswith(".text"):
            for tag in BRACKET.findall(val):
                if tag.strip() not in EMOTION_TAGS:
                    bad.append(f"{label}: '[{tag}]' (không phải thẻ cảm xúc hợp lệ)")
    if bad:
        return _fmt(bad, "Còn chỗ trống/đánh dấu tạm:")
    return CheckResult("pass", f"{params['path']}: không còn chỗ trống hay đánh dấu tạm.")


@register("script_segment_length")
def segment_length(project: Path, params: dict) -> CheckResult:
    s = load_yaml(project, params["path"])
    mx = int(params.get("max_chars", 300))
    bad = [f"{seg['id']}: {len(seg['text'])} ký tự"
           for _, seg in segments(s) if seg.get("kind") == "voice" and len(seg.get("text", "")) > mx]
    if bad:
        return _fmt(bad, f"Đoạn giọng dài quá {mx} ký tự (TTS dễ đọc sai, khó căn thời gian), cần tách:")
    return CheckResult("pass", f"Mọi đoạn giọng ≤ {mx} ký tự.")


@register("script_reading_speed")
def reading_speed(project: Path, params: dict) -> CheckResult:
    s = load_yaml(project, params["path"])
    lo, hi = float(params.get("min_sps", 2.5)), float(params.get("max_sps", 4.0))
    bad, rates = [], []
    for _, seg in segments(s):
        if seg.get("kind") != "voice":
            continue
        n, d = syllables(seg["text"]), float(seg["est_duration_s"])
        rate = n / d if d > 0 else float("inf")
        rates.append(rate)
        if not lo <= rate <= hi:
            bad.append(f"{seg['id']}: {n} âm tiết / {d:g}s = {rate:.2f} âm tiết/giây")
    if bad:
        return _fmt(bad, f"Tốc độ đọc ngoài khoảng {lo}–{hi} âm tiết/giây:")
    if not rates:
        return CheckResult("pass", "Không có đoạn giọng.")
    return CheckResult("pass", f"{len(rates)} đoạn giọng, tốc độ {min(rates):.2f}–{max(rates):.2f} âm tiết/giây.")


@register("script_total_duration")
def total_duration(project: Path, params: dict) -> CheckResult:
    s = load_yaml(project, params["path"])
    tol = float(params.get("tolerance", 0.15))
    target = float(s["meta"]["target_duration_s"])
    total = sum(float(seg.get("est_duration_s", 0)) for _, seg in segments(s))
    diff = abs(total - target) / target
    msg = f"Tổng ước tính {total:g}s so với mục tiêu {target:g}s (lệch {diff:.0%}, cho phép {tol:.0%})."
    return CheckResult("pass" if diff <= tol else "fail", msg)


@register("script_view_in_sync")
def view_in_sync(project: Path, params: dict) -> CheckResult:
    from vp.script_view import render_view
    s = load_yaml(project, params["path"])
    vpath = project / params["view"]
    if not vpath.is_file():
        return CheckResult("fail", f"Chưa có bản đọc {params['view']}. Chạy: python -m vp script view <dự án>")
    if vpath.read_text(encoding="utf-8") != render_view(s):
        return CheckResult("fail", f"{params['view']} đã cũ so với {params['path']}. Chạy lại: python -m vp script view <dự án>")
    return CheckResult("pass", f"{params['view']} khớp {params['path']}.")


@register("script_pronunciation_format")
def pronunciation_format(project: Path, params: dict) -> CheckResult:
    """Cách đọc trong meta.pronunciation phải là các âm tiết tiếng Việt viết RỜI bằng dấu cách.
    Gạch nối, chữ số, ký hiệu làm TTS đọc sai (vd. 'các-bon-níc' bị đọc thành 'cacbon-i-c')."""
    s = load_yaml(project, params["path"])
    pr = (s.get("meta") or {}).get("pronunciation") or s.get("pronunciation") or {}
    bad = [f"'{k}' → '{v}': chỉ dùng chữ cái và dấu cách (không gạch nối, số, ký hiệu)"
           for k, v in pr.items() if not re.fullmatch(r"[^\W\d_]+( [^\W\d_]+)*", str(v).strip())]
    if bad:
        return _fmt(bad, "Cách đọc sai định dạng — viết rời từng âm tiết, vd. 'các bô níc':")
    return CheckResult("pass", f"{len(pr)} mục phát âm đúng định dạng (âm tiết viết rời)." if pr else "Không có mục phát âm.")
