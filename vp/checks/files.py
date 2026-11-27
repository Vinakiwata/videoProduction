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
