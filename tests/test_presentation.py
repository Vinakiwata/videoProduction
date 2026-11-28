import json

import pytest
import yaml

from conftest import write_yaml
from vp import presentation_tools as pt

SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><g id="waves"><rect width="100" height="100" fill="#0B3D91"/></g></svg>'


@pytest.fixture
def pproj(project, monkeypatch):
    """Dự án nhỏ: 2 khung hình, 1 cảnh SVG, 1 linh vật PNG, 1 chữ; cổng animation coi như ĐẠT."""
    p = project
    write_yaml(p / "02_design" / "storyboard.yaml", {
        "meta": {"title": "T", "canvas": {"width": 1920, "height": 1080, "fps": 30}},
        "palette": ["#0B3D91", "#FFC907", "#FFFFFF"], "fonts": {"title": "Be Vietnam Pro", "body": "Be Vietnam Pro"},
        "style": "phẳng", "text_plate": {"color": "#0B3D91", "opacity": 0.9, "always": True},
        "assets": [{"id": "A-BIEN", "kind": "scene", "description": "bãi biển có sóng", "colors": ["#0B3D91"]},
                   {"id": "A-KHI", "kind": "mascot", "expression": "vui", "description": "Khỉ vui mừng", "colors": ["#FFC907"]}],
        "shots": [
            {"id": "S01-01-a", "segment": "S01-01", "span": [0, 1], "purpose": "mở", "background": "#0B3D91",
             "camera": {"move": "zoom_in", "amount": 0.1}, "transition_in": "cut",
             "elements": [{"id": "e1", "asset": "A-BIEN", "box": {"x": 0, "y": 0, "w": 100, "h": 100}, "loop": {"anim": "bob"}},
                          {"id": "e2", "text": "Xin chào", "style": "title", "font_px": 80, "color": "#FFC907",
                           "box": {"x": 10, "y": 70, "w": 80, "h": 15}, "enter": {"anim": "fade", "at": 0.2}}]},
            {"id": "S01-02-a", "segment": "S01-02", "span": [0, 1], "purpose": "kết", "background": "#0B3D91",
             "camera": {"move": "static"}, "transition_in": "crossfade",
             "elements": [{"id": "e1", "asset": "A-KHI", "box": {"x": 40, "y": 20, "w": 20, "h": 40},
                           "enter": {"anim": "pop", "at": 0, "ease": "back_out"},
                           "exit": {"anim": "scale_out", "at": 0.9}}]}]})
    write_yaml(p / "05_timeline" / "timeline.yaml", {
        "fps": 30, "total_frames": 120, "total_s": 4.0, "params": {}, "segments": [], "music": None, "sfx": [],
        "voice": [{"segment": "S01-01", "file": "04_voice/segments/S01-01.wav", "start_frame": 0, "end_frame": 60}],
        "shots": [{"id": "S01-01-a", "segment": "S01-01", "start_frame": 0, "end_frame": 60, "content_end_frame": 60,
                   "transition_in": "cut", "camera": {"move": "zoom_in", "amount": 0.1}},
                  {"id": "S01-02-a", "segment": "S01-02", "start_frame": 60, "end_frame": 120, "content_end_frame": 120,
                   "transition_in": "crossfade", "camera": {"move": "static"}}],
        "cues": [{"shot": "S01-01-a", "element": "e1", "event": "loop", "frame": 0, "anim": "bob", "period_frames": 75},
                 {"shot": "S01-01-a", "element": "e2", "event": "enter", "frame": 12, "anim": "fade", "dur_frames": 9, "ease": "ease_out"},
                 {"shot": "S01-02-a", "element": "e1", "event": "enter", "frame": 60, "anim": "pop", "dur_frames": 12, "ease": "back_out"},
                 {"shot": "S01-02-a", "element": "e1", "event": "exit", "frame": 114, "anim": "scale_out", "dur_frames": 6, "ease": "ease_out"}]})
    d = p / "06_animation" / "assets"
    d.mkdir(parents=True, exist_ok=True)
    (d / "A-BIEN.svg").write_text(SVG, encoding="utf-8")
    from PIL import Image
    Image.new("RGBA", (64, 64), (0, 0, 0, 0)).save(d / "A-KHI.png")
    write_yaml(p / "06_animation" / "assets.yaml", {
        "motion_defaults": {"enter": {"fade": "ease_out"}, "exit": {"scale_out": "back_in"}},
        "assets": [{"id": "A-BIEN", "file": "assets/A-BIEN.svg", "kind": "scene", "description": "x", "layers": ["waves"],
                    "motion": [{"layer": "waves", "recipe": "bob", "amp": 6, "period_s": 2.5}], "source": "s", "license": "l"},
                   {"id": "A-KHI", "file": "assets/A-KHI.png", "kind": "mascot", "description": "x", "layers": [], "source": "s", "license": "l"}]})
    import wave
    import numpy as np
    seg = p / "04_voice" / "segments" / "S01-01.wav"
    seg.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(seg), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(48000)
        w.writeframes((np.zeros(48000)).astype(np.int16).tobytes())
    monkeypatch.setattr(pt.review, "gate", lambda pr, s: pt.review.GateStatus(True, "ĐẠT"))
    return p


def test_compile_shots_and_frames(pproj):
    c = pt.compile_presentation(pproj)
    assert c["canvas"] == {"width": 1920, "height": 1080, "fps": 30} and c["total_frames"] == 120
    s1, s2 = c["shots"]
    assert (s1["start"], s1["end"], s2["start"]) == (0, 60, 60)
    assert s2["transition"] == {"type": "crossfade", "frames": 8} and s1["transition"]["frames"] == 0
    assert s1["camera"] == {"move": "zoom_in", "amount": 0.1}


def test_compile_elements_motion(pproj):
    c = pt.compile_presentation(pproj)
    e_scene, e_text = c["shots"][0]["elements"]
    assert e_scene["asset"] == "A-BIEN" and e_scene["file"] == "assets/A-BIEN.svg" and e_scene["z"] == 0
    assert e_scene["loop"] == {"anim": "bob", "start": 0, "period": 75} and e_scene["layer_motion"] is True
    assert e_text["text"] == "Xin chào" and e_text["enter"] == {"anim": "fade", "start": 12, "dur": 9, "ease": "ease_out"}
    m = c["shots"][1]["elements"][0]
    assert m["kind"] == "mascot" and m["enter"]["ease"] == "back_out"          # storyboard ghi rõ -> giữ
    assert m["exit"] == {"anim": "scale_out", "start": 114, "dur": 6, "ease": "back_in"}   # không ghi -> motion_defaults
    assert c["assets"]["A-BIEN"]["motion"][0]["recipe"] == "bob"
    assert c["text_plate"] == {"color": "#0B3D91", "opacity": 0.9, "always": True}


def test_compile_hash_changes_with_inputs(pproj):
    h1 = pt.compile_presentation(pproj)["input_hash"]
    (pproj / "06_animation" / "assets" / "A-BIEN.svg").write_text(SVG.replace("#0B3D91", "#FFFFFF"), encoding="utf-8")
    assert pt.compile_presentation(pproj)["input_hash"] != h1


def test_build_writes_selfcontained_page(pproj):
    out = pt.build(pproj)
    d = pproj / "07_presentation"
    assert out == d / "index.html" and out.is_file()
    for f in ("presentation.json", "player.js", "player.css", "data.js", "assets/A-BIEN.svg", "assets/A-KHI.png", "audio/voice.wav"):
        assert (d / f).is_file(), f
    data = (d / "data.js").read_text(encoding="utf-8")
    assert data.startswith("window.VP_DATA") and "<svg" in data          # SVG nhúng sẵn: mở file:// không cần fetch
    html = out.read_text(encoding="utf-8")
    assert "data.js" in html and "player.js" in html


def test_build_requires_animation_gate(pproj, monkeypatch):
    monkeypatch.setattr(pt.review, "gate", lambda pr, s: pt.review.GateStatus(False, "chưa duyệt"))
    with pytest.raises(pt.PresentationError, match="animation"):
        pt.build(pproj)


def test_key_frames_cover_start_mid_end_and_transition(pproj):
    c = pt.compile_presentation(pproj)
    k = {x["frame"]: x["role"] for x in pt.key_frames(c)}
    assert k[0] == "start" and k[29] == "mid" and k[59] == "end"
    assert k[64] == "transition" and k[89] == "mid" and k[119] == "end"   # crossfade 8 khung → giữa = 60+4


def _fake_manifest(p, **over):
    from vp.checks import run_check
    d = p / pt.DIR / "check"
    d.mkdir(parents=True, exist_ok=True)
    row = {"frame": 30, "role": "mid", "shot": "S01-01-a", "file": "check/f00030.jpg", "size": [1920, 1080],
           "sha256": "x", "stddev": 40.0, "max": 255, "issues": []}
    man = {"build_hash": pt.build_hash(p), "contact_build_hash": None, "frames": [row], "errors": [], "console": [],
           "fonts": [], "determinism": {"checked": 1, "mismatch": []}}
    for k, v in over.items():
        if k in row:
            row[k] = v
        else:
            man[k] = v
    man["contact_build_hash"] = man["build_hash"]
    (d / "check_manifest.json").write_text(json.dumps(man), encoding="utf-8")
    return lambda name: run_check(name, p, {})


def test_checks_pass_on_clean_manifest(pproj):
    pt.build(pproj)
    chk = _fake_manifest(pproj)
    for name in ("presentation_input_hash", "presentation_assets", "presentation_render", "presentation_deterministic",
                 "presentation_text_fit", "presentation_motion", "presentation_check_in_sync"):
        assert chk(name).status == "pass", name


def test_checks_catch_problems(pproj):
    pt.build(pproj)
    assert _fake_manifest(pproj, errors=["thiếu lớp waves"])("presentation_render").status == "fail"
    assert _fake_manifest(pproj, stddev=0.5)("presentation_render").status == "fail"          # khung giữa trống
    assert _fake_manifest(pproj, stddev=0.5, role="settled")("presentation_render").status == "pass"
    assert _fake_manifest(pproj, determinism={"checked": 1, "mismatch": [30]})("presentation_deterministic").status == "fail"
    assert _fake_manifest(pproj, issues=["S01/e2: chữ tràn hộp"])("presentation_text_fit").status == "fail"
    assert _fake_manifest(pproj, build_hash="cũ")("presentation_check_in_sync").status == "fail"
    assert _fake_manifest(pproj)("presentation_fonts").status == "fail"                       # chưa có file font


def test_scene_loop_without_layer_motion_fails(pproj):
    a = yaml.safe_load((pproj / "06_animation" / "assets.yaml").read_text(encoding="utf-8"))
    del a["assets"][0]["motion"]
    write_yaml(pproj / "06_animation" / "assets.yaml", a)
    pt.build(pproj)
    r = _fake_manifest(pproj)("presentation_motion")
    assert r.status == "fail" and "chưa khai motion" in r.evidence


@pytest.mark.skipif(not (__import__("shutil").which("google-chrome") and __import__("shutil").which("node")),
                    reason="cần Chrome + Node")
def test_check_in_real_chrome_is_deterministic(pproj):
    pt.build(pproj)
    man = json.loads(pt.check(pproj).read_text(encoding="utf-8"))
    assert man["errors"] == [] and man["determinism"]["mismatch"] == []
    assert all(r["size"] == [1920, 1080] for r in man["frames"])
    assert pt.preview(pproj).is_file()


# ---------------- khung dọc 9:16 + nền tảng ----------------
@pytest.fixture
def vproj(pproj):
    """Như pproj nhưng khung dọc 1080×1920, brief đăng cả ba nền tảng."""
    b = yaml.safe_load((pproj / "00_brief" / "brief.yaml").read_text(encoding="utf-8"))
    b["format"] = {"width": 1080, "height": 1920, "fps": 30}
    b["platforms"] = ["youtube_shorts", "tiktok", "reels"]
    write_yaml(pproj / "00_brief" / "brief.yaml", b)
    sb = yaml.safe_load((pproj / "02_design" / "storyboard.yaml").read_text(encoding="utf-8"))
    sb["meta"]["canvas"] = {"width": 1080, "height": 1920, "fps": 30}
    write_yaml(pproj / "02_design" / "storyboard.yaml", sb)
    return pproj


def test_compile_vertical_margins(vproj):
    c = pt.compile_presentation(vproj)
    m = c["safe_margins"]
    assert c["canvas"]["width"] == 1080 and c["canvas"]["height"] == 1920
    assert (m["top"], m["bottom"], m["left"], m["right"]) == (220, 461, 65, 173)
    assert [p["id"] for p in c["platforms"]] == ["youtube_shorts", "tiktok", "reels"]
    assert all(len(p["ui_zones"]) == 3 and p["name"] for p in c["platforms"])
    assert "safe_area" not in c


def test_compile_legacy_margins(pproj):
    c = pt.compile_presentation(pproj)
    m = c["safe_margins"]
    assert (m["top"], m["bottom"], m["left"], m["right"]) == (54, 54, 96, 96) and c["platforms"] == []


def test_render_check_uses_canvas_size(vproj):
    pt.build(vproj)
    r = _fake_manifest(vproj, size=[1920, 1080])("presentation_render")
    assert r.status == "fail" and "1080×1920" in r.evidence
    assert _fake_manifest(vproj, size=[1080, 1920])("presentation_render").status == "pass"


@pytest.mark.skipif(not (__import__("shutil").which("google-chrome") and __import__("shutil").which("node")),
                    reason="cần Chrome + Node")
def test_check_vertical_canvas_real_chrome(vproj):
    sb = yaml.safe_load((vproj / "02_design" / "storyboard.yaml").read_text(encoding="utf-8"))
    sb["shots"][0]["elements"][1]["box"] = {"x": 10, "y": 6, "w": 80, "h": 6}     # chữ ở y 115–230 px: Reels che (220)
    write_yaml(vproj / "02_design" / "storyboard.yaml", sb)
    pt.build(vproj)
    man = json.loads(pt.check(vproj).read_text(encoding="utf-8"))
    assert man["errors"] == [] and man["determinism"]["mismatch"] == []
    assert all(r["size"] == [1080, 1920] for r in man["frames"])
    issues = [i for r in man["frames"] for i in r["issues"]]
    assert any("Reels" in i for i in issues), issues
    out = pt.preview(vproj)
    assert out.is_file() and (out.parent / "contact_ui.png").is_file()
