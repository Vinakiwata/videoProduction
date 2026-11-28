"""render/mix/final: kích thước khung lấy từ brief (format_from), không ghi cứng 1920×1080."""
import yaml

from conftest import make_video, write_yaml
from vp.checks import run_check

V = "08_render/video_silent.mp4"
P = {"path": V, "format_from": "00_brief/brief.yaml", "codec": "h264", "pix_fmt": "yuv420p"}


def _brief(project, w, h, platforms=None):
    b = yaml.safe_load((project / "00_brief" / "brief.yaml").read_text(encoding="utf-8"))
    b["format"] = {"width": w, "height": h, "fps": 30}
    b.pop("platforms", None)
    if platforms:
        b["platforms"] = platforms
    write_yaml(project / "00_brief" / "brief.yaml", b)


def test_video_format_from_brief(project):
    make_video(project / V, size="1080x1920")
    _brief(project, 1080, 1920, ["youtube_shorts", "tiktok", "reels"])
    assert run_check("video_format", project, P).status == "pass"
    _brief(project, 1920, 1080)
    r = run_check("video_format", project, P)
    assert r.status == "fail" and "1920x1080" in r.evidence


def test_video_format_animatic_size_from_storyboard(project):
    """Animatic = nửa canvas storyboard + dải phụ đề (96 ngang / 160 dọc)."""
    write_yaml(project / "02_design" / "storyboard.yaml", {"meta": {"title": "T", "canvas": {"width": 1080, "height": 1920, "fps": 30}}})
    A = "03_animatic/animatic.mp4"
    make_video(project / A, size="540x1120", fps=15)
    prm = {"path": A, "animatic_from": "02_design/storyboard.yaml", "fps": 15}
    assert run_check("video_format", project, prm).status == "pass"
    make_video(project / A, size="960x636", fps=15)
    assert run_check("video_format", project, prm).status == "fail"
