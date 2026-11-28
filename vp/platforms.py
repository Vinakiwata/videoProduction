"""Hồ sơ nền tảng đăng video (platforms/<id>.yaml): khung, độ dài tối đa, vùng an toàn, vùng giao diện che.
Cùng một file video đăng lên mọi nền tảng của brief → lề an toàn là lề CHẶT NHẤT từng cạnh.
Thiết kế: docs/superpowers/specs/2026-11-28-khung-doc-9-16-design.md"""
from __future__ import annotations

from pathlib import Path

import yaml

PLATFORMS_DIR = Path(__file__).resolve().parents[1] / "platforms"
SCHEMA = Path(__file__).resolve().parent / "schemas" / "platform.schema.json"
SIDES = ("top", "bottom", "left", "right")
LEGACY_PCT = 0.05


class PlatformError(ValueError):
    pass


def available(platforms_dir: Path | None = None) -> list[str]:
    return sorted(p.stem for p in Path(platforms_dir or PLATFORMS_DIR).glob("*.yaml"))


def load(pid: str, platforms_dir: Path | None = None) -> dict:
    p = Path(platforms_dir or PLATFORMS_DIR) / f"{pid}.yaml"
    if not p.is_file():
        raise PlatformError(f"Không có hồ sơ nền tảng '{pid}'. Hợp lệ: {', '.join(available(platforms_dir))}")
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def profiles(brief: dict, platforms_dir: Path | None = None) -> list[dict]:
    return [load(pid, platforms_dir) for pid in brief.get("platforms") or []]


def _wh(c: dict) -> str:
    return f"{c['width']}×{c['height']}"


def canvas(brief: dict, platforms_dir: Path | None = None) -> dict:
    """Khung chung của các nền tảng trong brief; brief không có platforms → brief.format."""
    profs = profiles(brief, platforms_dir)
    if not profs:
        f = brief["format"]
        return {"width": f["width"], "height": f["height"], "fps": f["fps"]}
    sizes = {_wh(p["canvas"]) for p in profs}
    if len(sizes) > 1:
        raise PlatformError("Các nền tảng của brief khác khung: " +
                            ", ".join(f"{p['name']} {_wh(p['canvas'])}" for p in profs) + ". Một video chỉ có một khung.")
    c = profs[0]["canvas"]
    return {"width": c["width"], "height": c["height"], "fps": c["fps"]}


def safe_margins(brief: dict, platforms_dir: Path | None = None) -> dict:
    """Lề an toàn (px) chặt nhất từng cạnh; `by` = nền tảng quyết định cạnh đó. Không có platforms → 5% khung."""
    profs = profiles(brief, platforms_dir)
    if not profs:
        c = canvas(brief, platforms_dir)
        mh, mv = round(c["width"] * LEGACY_PCT), round(c["height"] * LEGACY_PCT)
        return {"top": mv, "bottom": mv, "left": mh, "right": mh, "by": {}}
    canvas(brief, platforms_dir)   # báo lỗi nếu khác khung
    out, by = {}, {}
    for s in SIDES:
        best = max(profs, key=lambda p: p["safe_margins_px"][s])
        out[s], by[s] = best["safe_margins_px"][s], best["id"]
    out["by"] = by
    return out


def name(pid: str, platforms_dir: Path | None = None) -> str:
    try:
        return load(pid, platforms_dir)["name"]
    except PlatformError:
        return pid


def ui_zones(pid: str, platforms_dir: Path | None = None) -> list[dict]:
    return list(load(pid, platforms_dir)["ui_zones"])
