import copy

import pytest
import yaml

from conftest import FIXTURES, write_yaml
from vp.checks import run_check

SB = "02_design/storyboard.yaml"
P = {"path": SB, "script": "01_script/script.yaml", "brief": "00_brief/brief.yaml"}


@pytest.fixture
def sb():
    return yaml.safe_load((FIXTURES / "storyboard_good.yaml").read_text(encoding="utf-8"))


@pytest.fixture
def dproj(project, sb):
    write_yaml(project / SB, sb)
    return project


def put(project, sb):
    write_yaml(project / SB, sb)
    return project


def shot(sb, sid):
    return next(s for s in sb["shots"] if s["id"] == sid)


def test_schema(dproj):
    r = run_check("yaml_schema", dproj, {"path": SB, "schema": "storyboard"})
    assert r.status == "pass", r.evidence


def test_schema_rejects_unknown_anim(dproj, sb):
    shot(sb, "S01-01-a")["elements"][0]["enter"]["anim"] = "explode"
    r = run_check("yaml_schema", put(dproj, sb), {"path": SB, "schema": "storyboard"})
    assert r.status == "fail" and "explode" in r.evidence


def test_coverage_pass(dproj):
    r = run_check("storyboard_coverage", dproj, P)
    assert r.status == "pass", r.evidence


def test_coverage_missing_segment(dproj, sb):
    sb["shots"] = [s for s in sb["shots"] if s["segment"] != "S02-03"]
    r = run_check("storyboard_coverage", put(dproj, sb), P)
    assert r.status == "fail" and "S02-03" in r.evidence


def test_coverage_gap_and_overlap(dproj, sb):
    shot(sb, "S02-02-b")["span"] = [0.6, 1]
    r = run_check("storyboard_coverage", put(dproj, sb), P)
    assert r.status == "fail" and "hở" in r.evidence
    shot(sb, "S02-02-b")["span"] = [0.4, 1]
    r = run_check("storyboard_coverage", put(dproj, sb), P)
    assert r.status == "fail" and "chồng" in r.evidence


def test_coverage_thirds_float(dproj, sb):
    a = shot(sb, "S02-02-a"); b = shot(sb, "S02-02-b")
    a["span"] = [0, 0.333]; b["span"] = [0.333, 1]
    assert run_check("storyboard_coverage", put(dproj, sb), P).status == "pass"


def test_coverage_unknown_segment(dproj, sb):
    shot(sb, "S03-01-a")["segment"] = "S09-01"
    r = run_check("storyboard_coverage", put(dproj, sb), P)
    assert r.status == "fail" and "S09-01" in r.evidence


def test_refs(dproj, sb):
    assert run_check("storyboard_refs", dproj, P).status == "pass"
    s = shot(sb, "S01-01-a")
    s["elements"][0]["asset"] = "A-KHONGCO"
    s["focal"] = "e9"
    s["sfx"][0]["target"] = "e8"
    r = run_check("storyboard_refs", put(dproj, sb), P)
    assert r.status == "fail"
    for needle in ("A-KHONGCO", "e9", "e8"):
        assert needle in r.evidence


def test_refs_duplicate_shot_id(dproj, sb):
    shot(sb, "S02-02-b")["id"] = "S02-02-a"
    r = run_check("storyboard_refs", put(dproj, sb), P)
    assert r.status == "fail" and "S02-02-a" in r.evidence


def test_palette(dproj, sb):
    assert run_check("storyboard_palette", dproj, P).status == "pass"
    shot(sb, "S01-01-a")["elements"][2]["color"] = "#ffd23f"   # khác hoa/thường vẫn đúng
    assert run_check("storyboard_palette", put(dproj, sb), P).status == "pass"
    shot(sb, "S01-01-a")["background"] = "#FF0000"
    r = run_check("storyboard_palette", put(dproj, sb), P)
    assert r.status == "fail" and "#FF0000" in r.evidence and "S01-01-a" in r.evidence


def test_palette_must_match_brief(dproj, sb):
    sb["palette"].append("#123456")
    r = run_check("storyboard_palette", put(dproj, sb), P)
    assert r.status == "fail" and "#123456" in r.evidence


def test_text_size_words_and_time(dproj, sb):
    params = {**P, "min_px": 48, "min_title_px": 72, "max_words_per_line": 7, "s_per_word": 0.3, "base_s": 1.0}
    assert run_check("storyboard_text", dproj, params).status == "pass"
    e = shot(sb, "S01-01-a")["elements"][2]
    e["font_px"] = 60                                            # title < 72
    r = run_check("storyboard_text", put(dproj, sb), params)
    assert r.status == "fail" and "S01-01-a/e3" in r.evidence
    e["font_px"] = 96
    e["text"] = "một hai ba bốn năm sáu bảy tám"                    # 8 từ một dòng
    assert "8 từ" in run_check("storyboard_text", put(dproj, sb), params).evidence
    e["text"] = "một hai ba bốn\nnăm sáu bảy tám"                    # 2 dòng x 4 từ: ok số từ, nhưng 8 từ cần 3,4 giây
    e["enter"]["at"] = 0.5                                       # đoạn 4 giây -> hiện 2 giây
    r = run_check("storyboard_text", put(dproj, sb), params)
    assert r.status == "fail" and "3.4" in r.evidence


def test_contrast(dproj, sb):
    assert run_check("storyboard_contrast", dproj, {**P, "min_ratio": 4.5}).status == "pass"
    shot(sb, "S02-01-a")["background"] = "#FFFFFF"               # chữ trắng trên nền trắng
    r = run_check("storyboard_contrast", put(dproj, sb), {**P, "min_ratio": 4.5})
    assert r.status == "fail" and "S02-01-a/e2" in r.evidence and "1.00" in r.evidence


def test_safe_area(dproj, sb):
    params = {**P, "text_margin_pct": 5, "max_bleed_pct": 10}
    assert run_check("storyboard_safe_area", dproj, params).status == "pass"
    shot(sb, "S02-01-a")["elements"][1]["box"] = {"x": 80, "y": 70, "w": 30, "h": 8}   # chữ tràn phải
    shot(sb, "S01-01-a")["elements"][0]["box"] = {"x": -20, "y": 0, "w": 100, "h": 100}  # hình tràn 20%
    r = run_check("storyboard_safe_area", put(dproj, sb), params)
    assert r.status == "fail" and "S02-01-a/e2" in r.evidence and "S01-01-a/e1" in r.evidence


def test_sfx_density(dproj, sb):
    assert run_check("storyboard_sfx_density", dproj, {**P, "max_per_10s": 5}).status == "pass"
    s = shot(sb, "S01-01-a")
    s["sfx"] = [{"name": f"pop{i}", "target": "e2", "event": "enter"} for i in range(6)]
    r = run_check("storyboard_sfx_density", put(dproj, sb), {**P, "max_per_10s": 5})
    assert r.status == "fail" and "6" in r.evidence


def test_text_continues_across_shots(dproj, sb):
    params = {**P, "min_px": 48, "min_title_px": 72, "max_words_per_line": 7, "s_per_word": 0.3, "base_s": 1.0}
    e = shot(sb, "S01-01-a")["elements"][2]
    e["enter"]["at"] = 0.75                                     # 4 từ, hiện 1 giây ở S01-01 -> thiếu nếu đứng riêng
    r = run_check("storyboard_text", put(dproj, sb), params)
    assert r.status == "fail"
    shot(sb, "S01-02-a")["elements"].append(                    # chữ nối tiếp sang khung im lặng 1 giây
        {"id": "e2", "text": "Vì sao trời xanh?", "style": "title", "font_px": 96, "color": "#FFD23F",
         "box": {"x": 20, "y": 70, "w": 60, "h": 14}})
    r = run_check("storyboard_text", put(dproj, sb), params)
    assert r.status == "fail" and "2.0s" in r.evidence           # 1 + 1 = 2,0 giây < 2,2 giây
    e["enter"]["at"] = 0.7                                      # 1,2 + 1 = 2,2 giây: vừa đủ
    assert run_check("storyboard_text", put(dproj, sb), params).status == "pass"


def test_text_overflow_box(dproj, sb):
    params = {**P, "min_px": 48, "min_title_px": 72, "max_words_per_line": 7, "s_per_word": 0.3, "base_s": 1.0}
    e = shot(sb, "S01-01-a")["elements"][2]
    e["box"] = {"x": 40, "y": 70, "w": 12, "h": 14}             # 230px rộng cho tiêu đề 96px
    r = run_check("storyboard_text", put(dproj, sb), params)
    assert r.status == "fail" and "tràn hộp" in r.evidence


# ---- Cảnh minh hoạ màu tự nhiên (quyết định của chủ dự án 28/11/2026) ----
SCENE = ["#CDEBFA", "#7CC36A", "#3FA7E0"]


def _with_scene(project, sb):
    brief = yaml.safe_load((project / "00_brief" / "brief.yaml").read_text(encoding="utf-8"))
    brief["brand"]["scene_colors"] = SCENE
    write_yaml(project / "00_brief" / "brief.yaml", brief)
    sb["scene_palette"] = list(SCENE)
    sb["assets"][0].update(kind="scene", colors=["#CDEBFA", "#7CC36A", "#0B3D91"])
    sb["text_plate"] = {"color": "#1B1B1F", "opacity": 0.7}
    sb["palette"].append("#1B1B1F")
    brief["brand"]["colors"].append("#1B1B1F")
    write_yaml(project / "00_brief" / "brief.yaml", brief)
    return put(project, sb)


def test_scene_assets_may_use_scene_palette(dproj, sb):
    assert run_check("yaml_schema", _with_scene(dproj, sb), {"path": SB, "schema": "storyboard"}).status == "pass"
    assert run_check("storyboard_palette", dproj, P).status == "pass"


def test_icons_may_not_use_scene_palette(dproj, sb):
    _with_scene(dproj, sb)
    sb["assets"][1]["colors"] = ["#7CC36A"]                         # icon A-HOI dùng xanh lá
    r = run_check("storyboard_palette", put(dproj, sb), P)
    assert r.status == "fail" and "A-HOI" in r.evidence and "#7CC36A" in r.evidence


def test_scene_palette_must_match_brief(dproj, sb):
    _with_scene(dproj, sb)
    sb["scene_palette"].append("#123456")
    r = run_check("storyboard_palette", put(dproj, sb), P)
    assert r.status == "fail" and "#123456" in r.evidence


def test_text_and_background_stay_in_brand_palette(dproj, sb):
    _with_scene(dproj, sb)
    shot(sb, "S02-01-a")["elements"][1]["color"] = "#7CC36A"
    r = run_check("storyboard_palette", put(dproj, sb), P)
    assert r.status == "fail" and "S02-01-a/e2" in r.evidence


def test_contrast_text_over_scene_uses_plate(dproj, sb):
    _with_scene(dproj, sb)
    # chữ vàng e3 nằm trên cảnh A-TROI (có màu trời sáng #CDEBFA) -> phải tính trên tấm nền
    params = {**P, "min_ratio": 4.5}
    r = run_check("storyboard_contrast", put(dproj, sb), params)
    assert r.status == "pass", r.evidence
    del sb["text_plate"]
    r = run_check("storyboard_contrast", put(dproj, sb), params)
    assert r.status == "fail" and "S01-01-a/e3" in r.evidence and "#CDEBFA" in r.evidence
