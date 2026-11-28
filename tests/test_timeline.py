import pytest
import yaml

from conftest import FIXTURES, write_yaml
from test_voice import FakeEngine
from vp import timeline as tl
from vp import voice
from vp.checks import run_check

TP = {"path": "05_timeline/timeline.yaml", "script": "01_script/script.yaml",
      "voice": "04_voice/voice_manifest.yaml", "storyboard": "02_design/storyboard.yaml"}


@pytest.fixture
def tproj(project, monkeypatch):
    (project / "02_design").mkdir(exist_ok=True)
    (project / "02_design" / "storyboard.yaml").write_text(
        (FIXTURES / "storyboard_good.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    monkeypatch.setattr(voice.review, "gate", lambda p, s: voice.review.GateStatus(True, "ĐẠT"))
    voice.synth_all(project, FakeEngine())
    return project


def load(p):
    return yaml.safe_load((p / "05_timeline" / "timeline.yaml").read_text(encoding="utf-8"))


def test_voice_track_and_breaths(tproj):
    tl.build(tproj, check_gate=False)
    t = load(tproj)
    man = yaml.safe_load((tproj / "04_voice" / "voice_manifest.yaml").read_text(encoding="utf-8"))
    dur = {m["id"]: m["duration_s"] for m in man["segments"]}
    segs = {s["id"]: s for s in t["segments"]}
    fps = t["fps"]
    assert fps == 30 and segs["S01-01"]["start_frame"] == 0
    # S01-01 kết thúc bằng '?', nhưng đoạn sau là im lặng -> không chèn thở
    assert segs["S01-01"]["breath_s"] == 0
    assert segs["S01-02"]["start_frame"] == round(dur["S01-01"] * fps)
    # hai đoạn giọng cùng cảnh -> ngắt 0,6 giây; sang cảnh mới (S02-03 -> S03-01) -> 0,9 giây
    assert segs["S02-01"]["breath_s"] == pytest.approx(0.60)
    gap = segs["S02-02"]["start_frame"] - segs["S02-01"]["speech_end_frame"]
    assert gap == round(0.60 * fps)
    assert segs["S02-03"]["breath_s"] == pytest.approx(0.90)
    expected = sum(dur.values()) + 1 + 0.60 * 2 + 0.90      # 1 giây im lặng S01-02
    assert t["total_frames"] == pytest.approx(expected * fps, abs=2)


def test_shots_contiguous_and_cues_inside(tproj):
    tl.build(tproj, check_gate=False)
    t = load(tproj)
    shots = t["shots"]
    assert shots[0]["start_frame"] == 0 and shots[-1]["end_frame"] == t["total_frames"]
    for a, b in zip(shots, shots[1:]):
        assert a["end_frame"] == b["start_frame"]
    by = {s["id"]: s for s in shots}
    for c in t["cues"]:
        s = by[c["shot"]]
        assert s["start_frame"] <= c["frame"] <= s["end_frame"]
    # cue tính theo phần lời, không gồm khoảng thở: S01-01-a/e3 enter at 0.3
    segs = {s["id"]: s for s in t["segments"]}
    e3 = next(c for c in t["cues"] if c["shot"] == "S01-01-a" and c["element"] == "e3" and c["event"] == "enter")
    s0 = segs["S01-01"]
    assert e3["frame"] == round(0.3 * s0["speech_end_frame"])


def test_sfx_track(tproj):
    tl.build(tproj, check_gate=False)
    t = load(tproj)
    names = [x["name"] for x in t["sfx"]]
    assert names == ["pop", "whoosh"]
    pop = t["sfx"][0]
    e2 = next(c for c in t["cues"] if c["shot"] == "S01-01-a" and c["element"] == "e2" and c["event"] == "enter")
    assert pop["frame"] == e2["frame"]


def test_subtitles(tproj):
    tl.build(tproj, check_gate=False)
    p = {"path": "05_timeline/subtitles.srt", "script": "01_script/script.yaml", "max_chars": 42, "max_lines": 2, "min_s": 1.0}
    r = run_check("subtitles_valid", tproj, p)
    assert r.status == "pass", r.evidence
    srt = (tproj / "05_timeline" / "subtitles.srt").read_text(encoding="utf-8")
    assert srt.startswith("1\n00:00:00,000 --> ")
    # sửa chữ phụ đề -> phải bị bắt
    (tproj / "05_timeline" / "subtitles.srt").write_text(srt.replace("bầu trời", "bầu trơi", 1), encoding="utf-8")
    r = run_check("subtitles_valid", tproj, p)
    assert r.status == "fail" and "khác lời" in r.evidence


def test_split_lines():
    lines = tl.split_lines("Khi đi qua khí quyển, ánh sáng xanh có bước sóng ngắn bị các phân tử khí tán xạ mạnh hơn nhiều.", 42)
    assert all(len(x) <= 42 for x in lines)
    assert " ".join(lines).split() == "Khi đi qua khí quyển, ánh sáng xanh có bước sóng ngắn bị các phân tử khí tán xạ mạnh hơn nhiều.".split()
    assert lines[0].endswith(",")          # ưu tiên ngắt ở dấu câu


def test_consistency_and_sync(tproj):
    tl.build(tproj, check_gate=False)
    assert run_check("timeline_consistency", tproj, TP).status == "pass"
    assert run_check("timeline_in_sync", tproj, {**TP, "manifest": "05_timeline/manifest.json"}).status == "pass"
    t = load(tproj)
    t["shots"][2]["start_frame"] += 3                                  # tạo khe hở
    write_yaml(tproj / "05_timeline" / "timeline.yaml", t)
    r = run_check("timeline_consistency", tproj, TP)
    assert r.status == "fail" and "hở" in r.evidence
    sb = (tproj / "02_design" / "storyboard.yaml").read_text(encoding="utf-8")
    (tproj / "02_design" / "storyboard.yaml").write_text(sb.replace("Đặt câu hỏi", "Đặt câu hỏi mới"), encoding="utf-8")
    r = run_check("timeline_in_sync", tproj, {**TP, "manifest": "05_timeline/manifest.json"})
    assert r.status == "fail" and "build" in r.evidence


def test_consistency_detects_voice_mismatch(tproj):
    tl.build(tproj, check_gate=False)
    t = load(tproj)
    v = t["voice"][1]
    v["end_frame"] += 5
    write_yaml(tproj / "05_timeline" / "timeline.yaml", t)
    r = run_check("timeline_consistency", tproj, TP)
    assert r.status == "fail" and v["segment"] in r.evidence


def test_build_requires_voice_gate(project):
    with pytest.raises(tl.TimelineError, match="voice"):
        tl.build(project)
