"""Hồ sơ kênh: bộ nhận diện dùng chung cho mọi video của một kênh."""
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from vp.checks.files import SCHEMA_DIR, load_yaml

CHANNELS_DIR = Path(__file__).resolve().parents[1] / "channels"


class ChannelError(ValueError):
    pass


def load_channel(name: str, channels_dir: Path | None = None, validate: bool = True) -> dict:
    base = Path(channels_dir or CHANNELS_DIR)
    path = base / name / "channel.yaml"
    if not path.is_file():
        have = sorted(p.parent.name for p in base.glob("*/channel.yaml")) if base.is_dir() else []
        raise ChannelError(f"Không có hồ sơ kênh '{name}' ({path}). Kênh hiện có: {', '.join(have) or 'chưa có'}")
    data = load_yaml(base / name, "channel.yaml") or {}
    if validate:
        schema = json.loads((SCHEMA_DIR / "channel.schema.json").read_text(encoding="utf-8"))
        errs = list(Draft202012Validator(schema).iter_errors(data))
        if errs:
            raise ChannelError(f"Hồ sơ kênh '{name}' sai định dạng: " +
                               "; ".join(f"{'/'.join(map(str, e.path)) or '(gốc)'}: {e.message}" for e in errs))
    return data
