"""Khung dọc 9:16: xem trước theo khung của storyboard, vùng an toàn theo nền tảng (DSN-A08 v5)."""
import yaml

from conftest import write_yaml
from vp import design_preview as dp
from vp.checks import run_check

V = {"width": 1080, "height": 1920, "fps": 30}
PARAMS = {"path": "02_design/storyboard.yaml", "brief": "00_brief/brief.yaml", "max_bleed_pct": 10,
          "strict_kinds": ["mascot", "ui"]}


def _sb(project, elements, canvas=V, assets=None):
    write_yaml(project / "02_design" / "storyboard.yaml", {
        "meta": {"title": "T", "canvas": canvas},
        "assets": assets or [{"id": "A-KHI", "kind": "mascot", "description": "Khỉ", "colors": ["#FFC907"]},
                             {"id": "A-CANH", "kind": "scene", "description": "cảnh", "colors": ["#4A98D6"]}],
        "shots": [{"id": "S01-01-a", "segment": "S01-01", "span": [0, 1], "background": "#0B3D91",
                   "camera": {"move": "static"}, "transition_in": "cut", "elements": elements}]})


def _vertical(project, platforms=("youtube_shorts", "tiktok", "reels")):
    b = yaml.safe_load((project / "00_brief" / "brief.yaml").read_text(encoding="utf-8"))
    b["format"] = dict(V)
    b["platforms"] = list(platforms)
    write_yaml(project / "00_brief" / "brief.yaml", b)


def _txt(x, y, w=40, h=8):
    return {"id": "e1", "text": "Xin chào", "style": "label", "font_px": 64, "color": "#FFC907",
            "box": {"x": x, "y": y, "w": w, "h": h}}


def test_preview_size_vertical():
    assert dp.preview_size(V) == (540, 960)
    assert dp.preview_size({"width": 1920, "height": 1080}) == (960, 540)


def test_render_frame_vertical_size():
    shot = {"id": "S", "background": "#0B3D91", "transition_in": "cut", "camera": {"move": "static"},
            "elements": [_txt(20, 30)]}
    assert dp.render_frame(shot, {}, V).size == (540, 960)


def test_legacy_margins_5pct(project):
    H = {"width": 1920, "height": 1080, "fps": 30}
    _sb(project, [_txt(5, 50)], canvas=H)
    assert run_check("storyboard_safe_area", project, PARAMS).status == "pass"
    _sb(project, [_txt(4, 50)], canvas=H)
    assert run_check("storyboard_safe_area", project, PARAMS).status == "fail"


def test_text_outside_vertical_safe_fails(project):
    _vertical(project)
    _sb(project, [_txt(20, 10)])                    # y = 192 px < 220 (Reels)
    r = run_check("storyboard_safe_area", project, PARAMS)
    assert r.status == "fail" and "Reels" in r.evidence
    _sb(project, [_txt(20, 12)])                    # y = 230 px
    assert run_check("storyboard_safe_area", project, PARAMS).status == "pass"


def test_mascot_under_right_rail_fails_names_platform(project):
    _vertical(project)
    _sb(project, [{"id": "e2", "asset": "A-KHI", "box": {"x": 70, "y": 40, "w": 20, "h": 20}}])   # x1 = 972 > 907
    r = run_check("storyboard_safe_area", project, PARAMS)
    assert r.status == "fail" and "YouTube Shorts" in r.evidence


def test_scene_full_bleed_ok(project):
    _vertical(project)
    _sb(project, [{"id": "e3", "asset": "A-CANH", "box": {"x": 0, "y": 0, "w": 100, "h": 100}}])
    assert run_check("storyboard_safe_area", project, PARAMS).status == "pass"
