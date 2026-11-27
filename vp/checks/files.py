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
