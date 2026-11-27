import json
import wave

import numpy as np
import pytest
import yaml

from conftest import FIXTURES
from vp import animatic as an
from vp.checks import run_check
from vp.checks.media import probe


@pytest.fixture
def aproj(project):
    (project / "02_design").mkdir(exist_ok=True)
    (project / "02_design" / "storyboard.yaml").write_text(
        (FIXTURES / "storyboard_good.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    return project


def write_wav(path, seconds, sr=48000, freq=220.0):
    path.parent.mkdir(parents=True, exist_ok=True)
    t = np.arange(int(seconds * sr)) / sr
    data = (0.3 * np.sin(2 * np.pi * freq * t) * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(data.tobytes())


def test_timing_from_estimates(aproj):
    tm = an.compute_timing(aproj)
    assert tm["total_s"] == pytest.approx(29.0)
    seg = {s["id"]: s for s in tm["segments"]}
    assert seg["S01-01"]["source"] == "estimate"
    assert seg["S01-02"]["start_s"] == pytest.approx(4.0) and seg["S01-02"]["source"] == "silent"
    shots = {s["id"]: s for s in tm["shots"]}
    assert shots["S02-02-b"]["start_s"] == pytest.approx(11 + 3.5)
    assert shots["S02-02-b"]["dur_s"] == pytest.approx(3.5)
    saved = yaml.safe_load((aproj / "03_animatic" / "timing.yaml").read_text(encoding="utf-8"))
    assert saved["total_s"] == pytest.approx(29.0)


def test_timing_prefers_scratch_voice(aproj):
    write_wav(aproj / "03_animatic" / "scratch_voice" / "S01-01.wav", 5.5)
    tm = an.compute_timing(aproj)
    seg = {s["id"]: s for s in tm["segments"]}
    assert seg["S01-01"]["dur_s"] == pytest.approx(5.5, abs=1e-3) and seg["S01-01"]["source"] == "scratch"
    assert seg["S01-02"]["start_s"] == pytest.approx(5.5, abs=1e-3)
    assert tm["total_s"] == pytest.approx(30.5, abs=1e-3)


def test_audio_length_and_sfx_position(aproj):
    tm = an.compute_timing(aproj)
    sr = 48000
    audio = an.build_audio(aproj, tm, sr=sr)
    assert len(audio) == round(tm["total_s"] * sr)
    # S01-01-a: pop gắn với e2 enter at 0.1 của khung 4 giây -> 0,4 giây
    peak_window = np.abs(audio[int(0.35 * sr):int(0.6 * sr)]).max()
    quiet = np.abs(audio[int(2.0 * sr):int(3.0 * sr)]).max()
    assert peak_window > 0.05 and quiet < 1e-4


def test_audio_places_scratch_voice(aproj):
    write_wav(aproj / "03_animatic" / "scratch_voice" / "S02-01.wav", 6.0)
    tm = an.compute_timing(aproj)
    audio = an.build_audio(aproj, tm, sr=48000)
    start = int(5.0 * 48000)  # S02-01 bắt đầu ở 5,0 giây
    assert np.abs(audio[start + 4800:start + 9600]).max() > 0.1


def test_frame_visibility_follows_enter(aproj):
    sb = yaml.safe_load((aproj / "02_design" / "storyboard.yaml").read_text(encoding="utf-8"))
    shot = sb["shots"][0]        # S01-01-a, e2 enter at 0.1, e3 enter at 0.3 (khung 4 giây)
    assert an.element_alpha(shot["elements"][2], t=0.5, dur=4.0) == 0.0
    assert an.element_alpha(shot["elements"][2], t=1.2 + 0.3, dur=4.0) == 1.0
    mid = an.element_alpha(shot["elements"][2], t=1.2 + 0.15, dur=4.0)
    assert 0 < mid < 1
    ex = {"enter": {"at": 0, "dur_s": 0.2}, "exit": {"at": 0.5, "dur_s": 0.2}}
    assert an.element_alpha(ex, t=2.5, dur=4.0) == 0.0


def test_build_video_and_checks(aproj):
    out = an.build(aproj, fps=5)
    info = probe(out)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    a = next(s for s in info["streams"] if s["codec_type"] == "audio")
    assert (v["width"], v["height"]) == (960, 636)   # hình 540 + dải phụ đề 96 bên dưới
    assert float(v["duration"]) == pytest.approx(29.0, abs=0.25)
    assert float(a["duration"]) == pytest.approx(29.0, abs=0.1)
    p = {"path": "03_animatic/animatic.mp4", "timing": "03_animatic/timing.yaml",
         "manifest": "03_animatic/manifest.json", "max_diff_s": 0.25}
    assert run_check("animatic_in_sync", aproj, p).status == "pass"
    assert run_check("animatic_duration", aproj, p).status == "pass"
    sb = (aproj / "02_design" / "storyboard.yaml").read_text(encoding="utf-8")
    (aproj / "02_design" / "storyboard.yaml").write_text(sb.replace("Đặt câu hỏi", "Đặt câu hỏi gấp"), encoding="utf-8")
    r = run_check("animatic_in_sync", aproj, p)
    assert r.status == "fail" and "build" in r.evidence
    man = json.loads((aproj / "03_animatic" / "manifest.json").read_text())
    assert man["voice_source"] == "estimate"
