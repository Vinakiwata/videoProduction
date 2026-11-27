"""Nạp và kiểm tra tính hợp lệ của checklist (checklists/<stage>.yaml)."""
from pathlib import Path

import yaml

from vp.checks import REGISTRY

CHECKLIST_DIR = Path(__file__).resolve().parents[1] / "checklists"
SEVERITIES = ("chan", "nghiem_trong", "nhe")
METHODS = ("auto", "ai")


class ChecklistError(ValueError):
    pass


def load_checklist(stage: str, checklist_dir: Path | None = None) -> dict:
    path = Path(checklist_dir or CHECKLIST_DIR) / f"{stage}.yaml"
    if not path.is_file():
        raise ChecklistError(f"Không có checklist cho công đoạn '{stage}' ({path}).")
    cl = yaml.safe_load(path.read_text(encoding="utf-8"))
    errs = []
    if cl.get("stage") != stage:
        errs.append(f"stage = {cl.get('stage')!r}, phải là {stage!r}")
    for key in ("version", "title", "items"):
        if not cl.get(key):
            errs.append(f"thiếu '{key}'")
    cl.setdefault("artifacts", [])
    seen = set()
    for i, it in enumerate(cl.get("items") or []):
        where = f"items[{i}] ({it.get('id', '?')})"
        for key in ("id", "group", "title", "severity", "method"):
            if not it.get(key):
                errs.append(f"{where}: thiếu '{key}'")
        if it.get("id") in seen:
            errs.append(f"{where}: trùng id")
        seen.add(it.get("id"))
        if it.get("severity") not in SEVERITIES:
            errs.append(f"{where}: severity phải thuộc {SEVERITIES}")
        if it.get("method") == "auto":
            if it.get("check") not in REGISTRY:
                errs.append(f"{where}: kiểm tra tự động '{it.get('check')}' chưa đăng ký")
        elif it.get("method") == "ai":
            if not str(it.get("guidance") or "").strip():
                errs.append(f"{where}: mục 'ai' phải có 'guidance' (tiêu chí ĐẠT/TRƯỢT)")
        else:
            errs.append(f"{where}: method phải thuộc {METHODS}")
        it.setdefault("allow_na", False)
        it.setdefault("params", {})
    if errs:
        raise ChecklistError(f"Checklist {path.name} không hợp lệ:\n- " + "\n- ".join(errs))
    return cl
