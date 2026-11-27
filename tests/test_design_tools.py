import json

import pytest
import yaml
from PIL import Image

from conftest import FIXTURES, write_yaml
from vp import design_tools as dt
from vp.checks import run_check

SB = "02_design/storyboard.yaml"


def gate_script_open(project, monkeypatch):
    monkeypatch.setattr(dt.review, "gate", lambda p, s: dt.review.GateStatus(True, "ĐẠT"))


def load(project):
    return yaml.safe_load((project / SB).read_text(encoding="utf-8"))


def test_init_requires_script_gate(project):
    with pytest.raises(dt.DesignToolError, match="script"):
        dt.init(project)


def test_init_scaffold(project, monkeypatch, good_script):
    gate_script_open(project, monkeypatch)
    good_script["scenes"][0]["segments"][0]["on_screen_text"] = "Vì sao?"
    good_script["scenes"][0]["segments"][0]["sfx"] = ["pop"]
    write_yaml(project / "01_script" / "script.yaml", good_script)
    dt.init(project)
    sb = load(project)
    assert sb["palette"] == ["#0B3D91", "#FFD23F", "#FFFFFF"]
    assert [s["segment"] for s in sb["shots"]] == ["S01-01", "S01-02", "S02-01", "S02-02", "S02-03", "S03-01"]
    first = sb["shots"][0]
    assert first["id"] == "S01-01-a" and first["span"] == [0, 1]
    assert first["purpose"].startswith("TODO")
    texts = [e for e in first["elements"] if "text" in e]
    assert texts and texts[0]["text"] == "Vì sao?"
    assert first["sfx"][0]["name"] == "pop"
    # còn TODO -> cổng chặn
    assert run_check("no_placeholders", project, {"path": SB}).status == "fail"
    # nhưng độ phủ đã đúng ngay từ đầu
    p = {"path": SB, "script": "01_script/script.yaml", "brief": "00_brief/brief.yaml"}
    assert run_check("storyboard_coverage", project, p).status == "pass"
    with pytest.raises(dt.DesignToolError, match="đã có"):
        dt.init(project)


@pytest.fixture
def dproj(project):
    (project / "02_design").mkdir(exist_ok=True)
    (project / SB).write_text((FIXTURES / "storyboard_good.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    return project


def test_view(dproj):
    md = dt.view(dproj).read_text(encoding="utf-8")
    assert "S02-02-b" in md and "match_cut" in md
    assert "Bạn có bao giờ tự hỏi" in md          # có lời đọc của đoạn
    assert "⭐" in md                               # đánh dấu điểm nhìn chính


def test_preview_and_sync(dproj):
    out = dt.preview(dproj)
    frames = sorted((dproj / "02_design" / "frames").glob("*.png"))
    assert len(frames) == 7
    assert Image.open(frames[0]).size == (960, 540)
    sheet = Image.open(out)
    assert sheet.width == 4 * 480 + 5 * 16
    man = json.loads((dproj / "02_design" / "frames" / "manifest.json").read_text())
    assert man["frames"] == [f.name for f in frames] or set(man["frames"]) == {f.name for f in frames}
    p = {"path": SB, "manifest": "02_design/frames/manifest.json"}
    assert run_check("storyboard_preview_in_sync", dproj, p).status == "pass"
    sb = load(dproj); sb["shots"][0]["purpose"] = "Đổi"
    write_yaml(dproj / SB, sb)
    r = run_check("storyboard_preview_in_sync", dproj, p)
    assert r.status == "fail" and "preview" in r.evidence


def test_preview_long_text_does_not_crash(dproj):
    sb = load(dproj)
    sb["shots"][0]["elements"][2]["text"] = "chữ rất dài " * 40
    write_yaml(dproj / SB, sb)
    dt.preview(dproj)


def test_lint_clean_on_fixture(dproj):
    dt.preview(dproj)
    bad = [(it["id"], r.evidence) for it, r in dt.lint(dproj) if r.status != "pass"]
    assert bad == []
