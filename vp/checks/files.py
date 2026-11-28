import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from vp.checks import CheckResult, register

SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schemas"


class _Loader(yaml.SafeLoader):
    """SafeLoader nhưng giữ ngày tháng dạng chuỗi (khớp JSON Schema)."""


_Loader.yaml_implicit_resolvers = {
    k: [r for r in v if r[0] != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def load_yaml(project: Path, rel: str):
    path = project / rel
    if not path.is_file():
        raise FileNotFoundError(2, "missing", rel)
    return yaml.load(path.read_text(encoding="utf-8"), Loader=_Loader)


@register("file_exists")
def file_exists(project: Path, params: dict) -> CheckResult:
    paths = params["paths"]
    if not isinstance(paths, list):
        raise TypeError("params.paths phải là danh sách")
    missing = [p for p in paths if not (project / p).exists()]
    if missing:
        return CheckResult("fail", "Thiếu: " + ", ".join(missing))
    return CheckResult("pass", "Có đủ: " + ", ".join(paths))


@register("yaml_schema")
def yaml_schema(project: Path, params: dict) -> CheckResult:
    rel, name = params["path"], params["schema"]
    data = load_yaml(project, rel)
    schema = json.loads((SCHEMA_DIR / f"{name}.schema.json").read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: list(e.path))
    if not errors:
        return CheckResult("pass", f"{rel} khớp schema '{name}'.")
    lines = [f"- tại `{'/'.join(map(str, e.path)) or '(gốc)'}`: {e.message}" for e in errors[:15]]
    more = f"\n… và {len(errors) - 15} lỗi khác" if len(errors) > 15 else ""
    return CheckResult("fail", f"{rel} sai schema '{name}' ({len(errors)} lỗi):\n" + "\n".join(lines) + more)


@register("brand_voice_valid")
def brand_voice_valid(project: Path, params: dict) -> CheckResult:
    """Giọng trong brand.voice phải là giọng có thật của engine (vd. VieNeu-TTS v3 Turbo), hoặc ghi rõ 'clone:'/'recording'."""
    b = load_yaml(project, params["path"])
    raw = str(b["brand"]["voice"])
    name = raw.split(":", 1)[1].strip() if ":" in raw else raw.strip()
    if raw.lower().startswith(("clone", "recording", "thu âm")):
        return CheckResult("pass", f"Giọng '{raw}' không dùng giọng dựng sẵn (nhân bản/thu âm) — kiểm đồng ý ở cổng voice.")
    lst = Path(__file__).resolve().parents[1] / "data" / params.get("list", "vieneu_v3_turbo_voices.txt")
    known = [ln.strip() for ln in lst.read_text(encoding="utf-8").splitlines() if ln.strip() and not ln.startswith("#")]
    if name in known:
        return CheckResult("pass", f"Giọng '{name}' có trong danh sách giọng dựng sẵn ({lst.name}).")
    return CheckResult("fail", f"Giọng '{name}' KHÔNG có trong {lst.name}. Giọng hợp lệ: {', '.join(known[:30])}…")


@register("brief_platforms")
def brief_platforms(project: Path, params: dict) -> CheckResult:
    """Nền tảng của brief có hồ sơ, cùng khung, brief.format trùng khung đó, thời lượng ≤ giới hạn từng nền tảng."""
    from vp import platforms as pf
    b = load_yaml(project, params["path"])
    pdir = params.get("platforms_dir")
    ids = b.get("platforms") or []
    if not ids:
        f = b.get("format") or {}
        return CheckResult("pass", f"Brief không chọn nền tảng: dùng khung brief.format {f.get('width')}×{f.get('height')} và lề an toàn 5% "
                                   f"(muốn kiểm vùng giao diện thì thêm platforms: {', '.join(pf.available(pdir))}).")
    bad = [i for i in ids if i not in pf.available(pdir)]
    if bad:
        return CheckResult("fail", f"Không có hồ sơ cho: {', '.join(bad)}. Hợp lệ: {', '.join(pf.available(pdir))}")
    try:
        c = pf.canvas(b, pdir)
    except pf.PlatformError as e:
        return CheckResult("fail", str(e))
    errs = []
    f = b.get("format") or {}
    if (f.get("width"), f.get("height"), f.get("fps")) != (c["width"], c["height"], c["fps"]):
        errs.append(f"brief.format {f.get('width')}×{f.get('height')}@{f.get('fps')} khác khung nền tảng {c['width']}×{c['height']}@{c['fps']}")
    dur = float(b.get("target_duration_s") or 0)
    for p in pf.profiles(b, pdir):
        if dur > p["max_duration_s"]:
            errs.append(f"{p['name']}: thời lượng {dur:g} giây > giới hạn {p['max_duration_s']:g} giây")
    if errs:
        return CheckResult("fail", "Nền tảng chưa khớp:\n" + "\n".join(f"- {e}" for e in errs))
    m = pf.safe_margins(b, pdir)
    names = ", ".join(p["name"] for p in pf.profiles(b, pdir))
    return CheckResult("pass", f"{names}: cùng khung {c['width']}×{c['height']}@{c['fps']}, {dur:g} giây trong giới hạn; "
                               f"lề an toàn trên {m['top']} · dưới {m['bottom']} · trái {m['left']} · phải {m['right']} px.")


@register("platform_profiles_fresh")
def platform_profiles_fresh(project: Path, params: dict) -> CheckResult:
    """Số đo vùng an toàn của các nền tảng đã đối chiếu trong vòng max_age_days (giao diện ứng dụng hay đổi)."""
    from datetime import date
    from vp import platforms as pf
    b = load_yaml(project, params["path"])
    pdir = params.get("platforms_dir")
    mx = int(params.get("max_age_days", 180))
    try:
        profs = pf.profiles(b, pdir)
    except pf.PlatformError as e:
        return CheckResult("fail", str(e))
    old = []
    for p in profs:
        age = (date.today() - date.fromisoformat(str(p["checked"]))).days
        if age > mx:
            old.append(f"{p['name']}: đối chiếu {p['checked']} ({age} ngày trước) — đo lại theo {p['source']['url']}")
    if old:
        return CheckResult("fail", f"Số đo vùng an toàn cũ hơn {mx} ngày:\n" + "\n".join(f"- {o}" for o in old))
    return CheckResult("pass", "Số đo vùng an toàn còn mới: " + ", ".join(f"{p['name']} {p['checked']}" for p in profs))
