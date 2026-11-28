import json

import pytest
import yaml

from conftest import FIXTURES, write_yaml
from vp import animation_tools as at
from vp.checks import run_check

GOOD = {
    "A-TROI": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 225"><rect width="400" height="225" fill="#0B3D91"/>'
              '<g id="clouds"><ellipse cx="120" cy="60" rx="60" ry="22" fill="#FFFFFF"/></g></svg>',
    "A-HOI": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 160"><path d="M10 10h80v60H50v40H30V50h40V30H10z" fill="#ffd23f"/>'
             '<circle cx="40" cy="140" r="12" fill="#FFD23F"/></svg>',
    "A-TIA": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 200"><g id="beam"><path d="M0 100H200" stroke="#FFFFFF" stroke-width="8"/></g>'
             '<g id="waves"><path d="M200 100q20-30 40 0t40 0" stroke="#FFD23F" fill="none" stroke-width="6"/></g></svg>',
    "A-PHANTU": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="20" fill="#FFFFFF" fill-opacity="0.8"/></svg>',
}


@pytest.fixture
def aproj(project, monkeypatch):
    (project / "02_design").mkdir(exist_ok=True)
    (project / "02_design" / "storyboard.yaml").write_text(
        (FIXTURES / "storyboard_good.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    monkeypatch.setattr(at.review, "gate", lambda p, s: at.review.GateStatus(True, "ĐẠT"))
    at.init(project)
    d = project / "06_animation" / "assets"
    d.mkdir(parents=True, exist_ok=True)
    for k, v in GOOD.items():
        (d / f"{k}.svg").write_text(v, encoding="utf-8")
    man = yaml.safe_load((project / "06_animation" / "assets.yaml").read_text(encoding="utf-8"))
    for a in man["assets"]:
        if a["id"] == "A-TIA":
            a["layers"] = ["beam", "waves"]
    write_yaml(project / "06_animation" / "assets.yaml", man)
    return project


P = {"path": "06_animation/assets.yaml", "storyboard": "02_design/storyboard.yaml", "brief": "00_brief/brief.yaml"}


def test_init_scaffold(project, monkeypatch):
    (project / "02_design").mkdir(exist_ok=True)
    (project / "02_design" / "storyboard.yaml").write_text(
        (FIXTURES / "storyboard_good.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    with pytest.raises(at.AnimationToolError, match="timeline"):
        at.init(project)
    monkeypatch.setattr(at.review, "gate", lambda p, s: at.review.GateStatus(True, "ĐẠT"))
    at.init(project)
    man = yaml.safe_load((project / "06_animation" / "assets.yaml").read_text(encoding="utf-8"))
    assert [a["id"] for a in man["assets"]] == ["A-TROI", "A-HOI", "A-TIA", "A-PHANTU"]
    assert man["assets"][0]["file"] == "assets/A-TROI.svg" and man["assets"][0]["license"]
    with pytest.raises(at.AnimationToolError, match="đã có"):
        at.init(project)


def test_complete(aproj):
    assert run_check("animation_assets_complete", aproj, P).status == "pass"
    (aproj / "06_animation" / "assets" / "A-HOI.svg").unlink()
    r = run_check("animation_assets_complete", aproj, P)
    assert r.status == "fail" and "A-HOI" in r.evidence


def test_svg_valid(aproj):
    assert run_check("svg_valid", aproj, P).status == "pass"
    f = aproj / "06_animation" / "assets" / "A-PHANTU.svg"
    f.write_text('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 10 10">'
                 '<image href="https://example.com/a.png"/></svg>', encoding="utf-8")
    r = run_check("svg_valid", aproj, P)
    assert r.status == "fail" and "A-PHANTU" in r.evidence and "image" in r.evidence
    f.write_text("<svg><rect", encoding="utf-8")
    assert "XML" in run_check("svg_valid", aproj, P).evidence


def test_svg_text_font(aproj):
    f = aproj / "06_animation" / "assets" / "A-PHANTU.svg"
    f.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 40"><text font-family="Comic Sans MS" fill="#FFFFFF">Hi</text></svg>',
                 encoding="utf-8")
    r = run_check("svg_valid", aproj, P)
    assert r.status == "fail" and "Comic Sans" in r.evidence
    f.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 40"><text font-family="Be Vietnam Pro, sans-serif" fill="#FFFFFF">Hi</text></svg>',
                 encoding="utf-8")
    assert run_check("svg_valid", aproj, P).status == "pass"


def test_svg_palette(aproj):
    assert run_check("svg_palette", aproj, {**P, "max_colors": 4}).status == "pass"
    f = aproj / "06_animation" / "assets" / "A-HOI.svg"
    f.write_text(GOOD["A-HOI"].replace('fill="#ffd23f"', 'style="fill:#FF0000"'), encoding="utf-8")
    r = run_check("svg_palette", aproj, {**P, "max_colors": 4})
    assert r.status == "fail" and "#FF0000" in r.evidence and "A-HOI" in r.evidence


def test_svg_palette_max_colors(aproj):
    f = aproj / "06_animation" / "assets" / "A-TROI.svg"
    f.write_text(GOOD["A-TROI"].replace("</svg>", '<rect fill="#FFD23F"/></svg>'), encoding="utf-8")
    r = run_check("svg_palette", aproj, {**P, "max_colors": 2})
    assert r.status == "fail" and "3 màu" in r.evidence


def test_svg_layers(aproj):
    assert run_check("svg_layers", aproj, P).status == "pass"
    man = yaml.safe_load((aproj / "06_animation" / "assets.yaml").read_text(encoding="utf-8"))
    man["assets"][2]["layers"].append("sparkles")
    write_yaml(aproj / "06_animation" / "assets.yaml", man)
    r = run_check("svg_layers", aproj, P)
    assert r.status == "fail" and "sparkles" in r.evidence


def test_flash_safety(tmp_path):
    p = tmp_path / "p"
    write_yaml(p / "05_timeline" / "timeline.yaml", {"fps": 30, "cues": [
        {"shot": "S01-01-a", "element": "e1", "event": "loop", "anim": "pulse", "frame": 0, "period_frames": 15},
        {"shot": "S01-01-a", "element": "e2", "event": "loop", "anim": "bob", "frame": 0, "period_frames": 3}]})
    q = {"path": "05_timeline/timeline.yaml", "min_period_s": 0.4}
    assert run_check("animation_flash_safety", p, q).status == "pass"      # bob không phải nhấp nháy
    t = yaml.safe_load((p / "05_timeline" / "timeline.yaml").read_text())
    t["cues"][0]["period_frames"] = 6
    write_yaml(p / "05_timeline" / "timeline.yaml", t)
    r = run_check("animation_flash_safety", p, q)
    assert r.status == "fail" and "S01-01-a/e1" in r.evidence


def test_preview_and_sync(aproj):
    out = at.preview(aproj)
    from PIL import Image
    im = Image.open(out)
    assert im.width > 1000
    q = {"path": "06_animation/assets.yaml", "manifest": "06_animation/preview_manifest.json"}
    assert run_check("animation_preview_in_sync", aproj, q).status == "pass"
    f = aproj / "06_animation" / "assets" / "A-HOI.svg"
    f.write_text(f.read_text().replace("r=\"12\"", "r=\"14\""), encoding="utf-8")
    assert run_check("animation_preview_in_sync", aproj, q).status == "fail"


SCENE_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 225"><rect width="400" height="225" fill="#CDEBFA"/>'
             '<g id="clouds"><path d="M0 200H400V225H0Z" fill="#7CC36A"/><circle cx="50" cy="50" r="9" fill="#0B3D91"/></g></svg>')


def _scene(aproj):
    brief = yaml.safe_load((aproj / "00_brief" / "brief.yaml").read_text(encoding="utf-8"))
    brief["brand"]["scene_colors"] = ["#CDEBFA", "#7CC36A"]
    write_yaml(aproj / "00_brief" / "brief.yaml", brief)
    man = yaml.safe_load((aproj / "06_animation" / "assets.yaml").read_text(encoding="utf-8"))
    man["assets"][0]["kind"] = "scene"
    write_yaml(aproj / "06_animation" / "assets.yaml", man)
    (aproj / "06_animation" / "assets" / "A-TROI.svg").write_text(SCENE_SVG, encoding="utf-8")


def test_svg_palette_scene_uses_natural_colors(aproj):
    _scene(aproj)
    r = run_check("svg_palette", aproj, {**P, "max_colors": 4, "max_scene_colors": 16})
    assert r.status == "pass", r.evidence


def test_svg_palette_icon_still_brand_only(aproj):
    _scene(aproj)
    (aproj / "06_animation" / "assets" / "A-HOI.svg").write_text(GOOD["A-HOI"].replace("#ffd23f", "#7CC36A"), encoding="utf-8")
    r = run_check("svg_palette", aproj, {**P, "max_colors": 4, "max_scene_colors": 16})
    assert r.status == "fail" and "A-HOI" in r.evidence


def test_svg_palette_scene_color_cap(aproj):
    _scene(aproj)
    r = run_check("svg_palette", aproj, {**P, "max_colors": 4, "max_scene_colors": 2})
    assert r.status == "fail" and "A-TROI" in r.evidence and "3 màu" in r.evidence
