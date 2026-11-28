"""Sổ đăng ký các kiểm tra tự động.

Mỗi kiểm tra nhận (thư mục dự án, params) và trả CheckResult.
status: pass | fail | error. 'error' = không chạy được kiểm tra -> tính như trượt.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass
class CheckResult:
    status: str
    evidence: str


REGISTRY: dict[str, Callable[[Path, dict], CheckResult]] = {}


def register(name: str):
    def deco(fn):
        REGISTRY[name] = fn
        return fn
    return deco


def run_check(name: str, project: Path, params: dict | None) -> CheckResult:
    fn = REGISTRY.get(name)
    if fn is None:
        return CheckResult("error", f"Không có kiểm tra tự động tên '{name}'.")
    try:
        return fn(Path(project), dict(params or {}))
    except FileNotFoundError as e:
        return CheckResult("error", f"Thiếu file: {e.filename or e}")
    except Exception as e:  # kiểm tra lỗi không được làm sập cả lần duyệt
        return CheckResult("error", f"Kiểm tra '{name}' lỗi khi chạy: {type(e).__name__}: {e}")


# Nạp các module để chúng tự đăng ký.
from vp.checks import files, script, media, design, voice, timeline  # noqa: E402,F401
