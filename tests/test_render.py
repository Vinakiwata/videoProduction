"""Tool 08 — render khung hình từ trang trình chiếu (07) ra MP4."""
import json
import shutil
import subprocess

import pytest

from vp import presentation_tools as pt
from vp import render_tools as rt
from test_presentation import pproj  # noqa: F401  — dự án Tool 07 mẫu (2 khung hình, 120 khung)

NEED = pytest.mark.skipif(not all(shutil.which(x) for x in ("google-chrome", "node", "ffmpeg", "ffprobe")),
                          reason="cần Chrome + Node + ffmpeg")


def _probe(path, *extra):
    r = subprocess.run(["ffprobe", "-v", "error", *extra, "-show_streams", "-of", "json", str(path)],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)["streams"]


@pytest.fixture
def built(pproj):
    pt.build(pproj)
    return pproj


@NEED
def test_render_builds_exact_frames_bt709(built):
    out = rt.build(built, check_gate=False)
    assert out == built / "08_render" / "video_silent.mp4" and out.is_file()
    v = _probe(out, "-count_frames", "-select_streams", "v:0")[0]
    assert int(v["nb_read_frames"]) == 120 and (v["width"], v["height"]) == (1920, 1080)
    assert v["codec_name"] == "h264" and v["pix_fmt"] == "yuv420p" and v.get("color_space") == "bt709"
    man = json.loads((built / "08_render" / "manifest.json").read_text(encoding="utf-8"))
    assert man["frames"] == 120 and man["build_hash"] == pt.build_hash(built) and man["crf"] == 18
    kinds = {s["codec_type"] for s in _probe(built / "08_render" / "preview_voice.mp4")}
    assert kinds == {"video", "audio"}


def test_render_requires_presentation_gate(built, monkeypatch):
    monkeypatch.setattr(rt.review, "gate", lambda p, s: rt.review.GateStatus(False, "chưa duyệt"))
    with pytest.raises(rt.RenderError) as e:
        rt.build(built)
    assert "presentation" in str(e.value)


@NEED
def test_render_aborts_on_page_error(built):
    d = built / "07_presentation" / "data.js"
    d.write_text(d.read_text(encoding="utf-8") + "\nwindow.addEventListener('load', () => { throw new Error('hỏng'); });\n",
                 encoding="utf-8")
    with pytest.raises(rt.RenderError) as e:
        rt.build(built, check_gate=False)
    assert "hỏng" in str(e.value)
    assert not (built / "08_render" / "video_silent.mp4").exists()
    assert not list((built / "08_render").glob("*.tmp.mp4"))


def test_cli_render_error_clean(built, monkeypatch):
    from vp.__main__ import main
    real = shutil.which
    monkeypatch.setattr(rt.shutil, "which", lambda n: None if n == "google-chrome" else real(n))
    monkeypatch.setattr(rt.review, "gate", lambda p, s: rt.review.GateStatus(True, "ĐẠT"))
    with pytest.raises(SystemExit) as e:
        main(["render", "build", str(built)])
    assert str(e.value.code).startswith("LỖI") and "Chrome" in str(e.value.code)
