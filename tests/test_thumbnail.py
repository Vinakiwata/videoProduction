"""Khung thumbnail (chủ dự án duyệt 28/11/2026): khung ĐẦU TIÊN có `thumbnail: true` được miễn
thời gian đọc (DSN-A07) và không tính vào số lần linh vật phản ứng (DSN-A11). Khung khác đánh dấu thì trượt."""
import yaml

from conftest import write_yaml
from vp.checks import run_check

P = "projects/vi-sao-nuoc-bien-man"


def _sample(project, mark_first=True, mark_other=False):
    from pathlib import Path
    root = Path(__file__).resolve().parents[1] / P
    for rel in ("00_brief/brief.yaml", "01_script/script.yaml", "02_design/storyboard.yaml"):
        (project / rel).parent.mkdir(parents=True, exist_ok=True)
        (project / rel).write_text((root / rel).read_text(encoding="utf-8"), encoding="utf-8")
    sb = yaml.safe_load((project / "02_design/storyboard.yaml").read_text(encoding="utf-8"))
    assert sb["shots"][0]["id"] == "S01-00-a"
    sb["shots"][0].pop("thumbnail", None)
    if mark_first:
        sb["shots"][0]["thumbnail"] = True
    if mark_other:
        sb["shots"][3]["thumbnail"] = True
    write_yaml(project / "02_design/storyboard.yaml", sb)
    return project


def _params(check):
    from vp.checklist import load_checklist
    return next(it["params"] for it in load_checklist("design")["items"] if it.get("check") == check)


def test_thumbnail_exempt_from_read_time(project):
    _sample(project, mark_first=False)
    r = run_check("storyboard_text", project, _params("storyboard_text"))
    assert r.status == "fail" and "S01-00-a/e2" in r.evidence
    _sample(project)
    r = run_check("storyboard_text", project, _params("storyboard_text"))
    assert "S01-00-a" not in r.evidence or r.status == "pass", r.evidence


def test_thumbnail_mascot_not_counted(project):
    _sample(project, mark_first=False)
    assert run_check("storyboard_mascot", project, _params("storyboard_mascot")).status == "fail"
    _sample(project)
    r = run_check("storyboard_mascot", project, _params("storyboard_mascot"))
    assert r.status == "pass" and "3 lần" in r.evidence


def test_thumbnail_only_allowed_on_first_shot(project):
    _sample(project, mark_other=True)
    r = run_check("storyboard_text", project, _params("storyboard_text"))
    assert r.status == "fail" and "thumbnail" in r.evidence
