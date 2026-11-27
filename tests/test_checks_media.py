import pytest

from conftest import make_video
from vp.checks import run_check

V = "08_render/video.mp4"


@pytest.fixture
def video(project):
    make_video(project / V, seconds=2)
    return project


def test_video_format_pass(video):
    r = run_check("video_format", video, {"path": V, "width": 1920, "height": 1080, "fps": 30})
    assert r.status == "pass", r.evidence


def test_video_format_wrong_size(project):
    make_video(project / V, size="1280x720")
    r = run_check("video_format", project, {"path": V, "width": 1920, "height": 1080, "fps": 30})
    assert r.status == "fail" and "1280x720" in r.evidence


def test_black_frames(project):
    make_video(project / V, seconds=3, black_first=1.0)
    r = run_check("black_frames", project, {"path": V, "max_black_s": 0.5})
    assert r.status == "fail" and "0.0" in r.evidence


def test_black_frames_pass(video):
    assert run_check("black_frames", video, {"path": V, "max_black_s": 0.5}).status == "pass"


def test_av_duration_match(video):
    r = run_check("av_duration_match", video, {"path": V, "max_diff_s": 0.1})
    assert r.status == "pass", r.evidence


def test_av_duration_no_audio(project):
    make_video(project / V, audio=False)
    r = run_check("av_duration_match", project, {"path": V, "max_diff_s": 0.1})
    assert r.status == "fail" and "âm thanh" in r.evidence


def test_audio_loudness_reports_lufs(video):
    r = run_check("audio_loudness", video,
                  {"path": V, "target_lufs": -14, "tolerance": 1.0, "max_true_peak": -1.0})
    assert r.status in ("pass", "fail")
    assert "LUFS" in r.evidence


def test_freeze_frames_on_static_video(project):
    # testsrc2 luôn chuyển động -> không đứng hình
    make_video(project / V, seconds=3)
    assert run_check("freeze_frames", project, {"path": V, "max_freeze_s": 1.0}).status == "pass"


def test_media_missing_file_error(project):
    assert run_check("video_format", project, {"path": V, "width": 1, "height": 1, "fps": 1}).status == "error"
