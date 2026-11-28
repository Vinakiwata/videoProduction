import subprocess
import wave

import numpy as np
import pytest
import yaml

from conftest import write_yaml
from vp import voice
from vp.checks import run_check
from vp.checks.script import syllables

SR = 48000


class FakeEngine:
    """Giọng giả: âm sine 0,3 giây/âm tiết, kèm 0,5 giây lặng hai đầu; có thể chèn khoảng lặng giữa câu."""
    name = "fake"

    def __init__(self, gap_for=None, gap_s=0.0, sec_per_syl=0.3):
        self.calls = []
        self.gap_for, self.gap_s, self.spsyl = gap_for or set(), gap_s, sec_per_syl

    def synth(self, text, voice_name):
        self.calls.append((text, voice_name))
        n = syllables(text)
        t = np.arange(int(n * self.spsyl * SR)) / SR
        speech = 0.3 * np.sin(2 * np.pi * 180 * t) * (1 + 0.3 * np.sin(2 * np.pi * 3 * t))
        pad = np.zeros(int(0.5 * SR))
        parts = [pad, speech[: len(speech) // 2]]
        if any(k in text for k in self.gap_for):
            parts.append(np.zeros(int(self.gap_s * SR)))
        parts += [speech[len(speech) // 2:], pad]
        return np.concatenate(parts).astype(np.float32), SR


def gate_open(monkeypatch):
    monkeypatch.setattr(voice.review, "gate", lambda p, s: voice.review.GateStatus(True, "ĐẠT"))


def voice_segments(script):
    return [s for sc in script["scenes"] for s in sc["segments"] if s["kind"] == "voice"]


def test_prepare_text_pronunciation():
    pr = {"cacbonic": "các-bon-níc", "NASA": "na-sa"}
    assert voice.prepare_text("hoà tan khí Cacbonic, theo NASA.", pr) == "hoà tan khí các-bon-níc, theo na-sa."
    assert voice.prepare_text("cacbonicxyz", pr) == "cacbonicxyz"          # chỉ thay trọn từ
    assert voice.prepare_text("Nghe hay [cười] quá", {}) == "Nghe hay [cười] quá"


def test_voice_name_from_brand():
    assert voice.voice_name("VieNeu-TTS v3 Turbo: Hải Đăng") == "Hải Đăng"
    assert voice.voice_name("Hải Đăng") == "Hải Đăng"


def test_synth_all_writes_manifest_and_trims(project, monkeypatch, good_script):
    gate_open(monkeypatch)
    eng = FakeEngine()
    man = voice.synth_all(project, eng)
    segs = voice_segments(good_script)
    assert [m["id"] for m in man["segments"]] == [s["id"] for s in segs]
    first = man["segments"][0]
    n = syllables(segs[0]["text"])
    assert first["duration_s"] == pytest.approx(n * 0.3 + 0.16, abs=0.06)   # đã cắt 0,5 giây lặng, chừa 0,08 x2
    assert first["lead_s"] <= 0.12 and first["trail_s"] <= 0.12
    assert eng.calls[0][1] == "Hải Đăng"
    full = project / "04_voice" / "voice_full.wav"
    with wave.open(str(full)) as w:
        total = w.getnframes() / w.getframerate()
    assert total == pytest.approx(man["total_s"], abs=0.01)
    silent = sum(s["est_duration_s"] for sc in good_script["scenes"] for s in sc["segments"] if s["kind"] == "silent")
    assert man["total_s"] == pytest.approx(sum(m["duration_s"] for m in man["segments"]) + silent, abs=0.01)
    p = {"path": "04_voice/voice_manifest.yaml", "script": "01_script/script.yaml"}
    assert run_check("voice_manifest", project, p).status == "pass"
    q = {"path": "04_voice/voice_manifest.yaml"}
    r = run_check("voice_segment_quality", project, q)
    assert r.status == "pass", r.evidence
    r = run_check("audio_loudness", project, {"path": "04_voice/voice_full.wav", "target_lufs": -16,
                                              "tolerance": 1.5, "max_true_peak": -1.0})
    assert r.status == "pass", r.evidence


def test_manifest_stale_when_script_changes(project, monkeypatch, good_script):
    gate_open(monkeypatch)
    voice.synth_all(project, FakeEngine())
    good_script["scenes"][0]["segments"][0]["text"] = "Câu đã sửa sau khi tạo giọng."
    write_yaml(project / "01_script" / "script.yaml", good_script)
    r = run_check("voice_manifest", project, {"path": "04_voice/voice_manifest.yaml", "script": "01_script/script.yaml"})
    assert r.status == "fail" and "S01-01" in r.evidence


def test_manifest_detects_tampered_file(project, monkeypatch):
    gate_open(monkeypatch)
    voice.synth_all(project, FakeEngine())
    f = project / "04_voice" / "segments" / "S02-01.wav"
    f.write_bytes(f.read_bytes()[:-4800])
    r = run_check("voice_manifest", project, {"path": "04_voice/voice_manifest.yaml", "script": "01_script/script.yaml"})
    assert r.status == "fail" and "S02-01" in r.evidence


def test_quality_catches_internal_gap(project, monkeypatch):
    gate_open(monkeypatch)
    voice.synth_all(project, FakeEngine(gap_for={"Mặt Trời"}, gap_s=1.6))
    r = run_check("voice_segment_quality", project, {"path": "04_voice/voice_manifest.yaml", "max_gap_s": 1.0})
    assert r.status == "fail" and "S02-01" in r.evidence and "lặng giữa" in r.evidence


def test_takes_pick_best(project, monkeypatch):
    gate_open(monkeypatch)

    class Flaky(FakeEngine):
        def synth(self, text, voice_name):
            self.gap_for = {text} if len(self.calls) % 2 == 0 else set()   # lượt 1 lỗi, lượt 2 tốt
            self.gap_s = 1.6
            return FakeEngine.synth(self, text, voice_name)

    man = voice.synth_all(project, Flaky(), takes=2)
    assert all(m["max_gap_s"] < 1.0 for m in man["segments"])
    assert all(m["takes"] == 2 for m in man["segments"])


def test_only_resynthesizes_selected(project, monkeypatch):
    gate_open(monkeypatch)
    voice.synth_all(project, FakeEngine())
    eng = FakeEngine()
    voice.synth_all(project, eng, only={"S02-02"})
    assert len(eng.calls) == 1
    man = yaml.safe_load((project / "04_voice" / "voice_manifest.yaml").read_text(encoding="utf-8"))
    assert len(man["segments"]) == 5


def test_recording_engine_any_format(project, monkeypatch, good_script):
    gate_open(monkeypatch)
    rec = project / "04_voice" / "recordings"
    rec.mkdir(parents=True)
    for i, s in enumerate(voice_segments(good_script)):
        ext = "m4a" if i % 2 else "wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo:d=0.4",
                        "-f", "lavfi", "-i", f"sine=f=200:sample_rate=44100:d={s['est_duration_s']}",
                        "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo:d=0.4",
                        "-filter_complex", "[1]aformat=channel_layouts=stereo,volume=0.4[s];[0][s][2]concat=n=3:v=0:a=1",
                        str(rec / f"{s['id']}.{ext}")], check=True)
    man = voice.synth_all(project, voice.RecordingEngine(project))
    assert man["engine"] == "recording"
    assert man["segments"][0]["duration_s"] == pytest.approx(4.16, abs=0.1)


def test_recording_engine_missing_file(project, monkeypatch):
    gate_open(monkeypatch)
    with pytest.raises(voice.VoiceError, match="S01-01"):
        voice.synth_all(project, voice.RecordingEngine(project))


def test_vieneu_engine_explains_when_missing():
    with pytest.raises(voice.VoiceError, match="pip install vieneu"):
        voice.VieneuEngine()


def test_calibrate(project, monkeypatch, tmp_path):
    gate_open(monkeypatch)
    voice.synth_all(project, FakeEngine(sec_per_syl=0.25))
    ch = tmp_path / "channels"
    write_yaml(ch / "k" / "channel.yaml", {"voice_profile": {"syllables_per_second": 3.2}})
    b = yaml.safe_load((project / "00_brief" / "brief.yaml").read_text(encoding="utf-8"))
    b["channel_ref"] = "k"
    write_yaml(project / "00_brief" / "brief.yaml", b)
    res = voice.calibrate(project, apply=True, channels_dir=ch)
    assert 3.4 < res["measured_sps"] < 4.0          # 4 âm tiết/giây trừ phần đệm
    prof = yaml.safe_load((ch / "k" / "channel.yaml").read_text(encoding="utf-8"))["voice_profile"]
    assert prof["calibrated"] is True and prof["syllables_per_second"] == res["measured_sps"]


def test_to_animatic(project, monkeypatch):
    gate_open(monkeypatch)
    voice.synth_all(project, FakeEngine())
    n = voice.to_animatic(project)
    assert n == 5 and (project / "03_animatic" / "scratch_voice" / "S01-01.wav").is_file()


def test_recording_sheet(project):
    md = voice.recording_sheet(project).read_text(encoding="utf-8")
    assert "| `S01-01` | Bạn có bao giờ tự hỏi" in md and "04_voice/recordings/" in md


def test_recording_engine_multiple_takes(project, monkeypatch, good_script):
    gate_open(monkeypatch)
    rec = project / "04_voice" / "recordings"
    rec.mkdir(parents=True)
    for s in voice_segments(good_script):
        for k, gap in ((1, 1.6), (2, 0.0)):        # lượt 1 có khoảng lặng lạ, lượt 2 sạch
            a, sr = FakeEngine(gap_for={s["text"]} if gap else set(), gap_s=gap).synth(s["text"], "x")
            import vp.voice as V
            V._write_wav(rec / f"{s['id']}_t{k}.wav", a)
    eng = voice.RecordingEngine(project, name="vieneu-mac")
    man = voice.synth_all(project, eng, takes=2)
    assert man["engine"] == "vieneu-mac"
    assert all(m["max_gap_s"] < 1.0 for m in man["segments"])


def test_tempo_slows_voice(project, monkeypatch):
    gate_open(monkeypatch)
    m1 = voice.synth_all(project, FakeEngine())
    m2 = voice.synth_all(project, FakeEngine(), tempo=0.9)
    d1, d2 = m1["segments"][0]["duration_s"], m2["segments"][0]["duration_s"]
    assert d2 == pytest.approx(d1 / 0.9, rel=0.03)
    assert m2["tempo"] == 0.9 and m2["segments"][0]["sps"] < m1["segments"][0]["sps"]


def test_quality_relative_speed(project, monkeypatch):
    gate_open(monkeypatch)
    voice.synth_all(project, FakeEngine(sec_per_syl=0.2))              # ~5 âm tiết/giây đều nhau
    q = {"path": "04_voice/voice_manifest.yaml", "max_sps": 6.0, "max_rel_dev": 0.3}
    assert run_check("voice_segment_quality", project, q).status == "pass"
    man = yaml.safe_load((project / "04_voice" / "voice_manifest.yaml").read_text(encoding="utf-8"))
    man["segments"][0]["sps"] = round(man["segments"][0]["sps"] * 0.6, 2)   # một câu chậm bất thường (TTS kéo dài?)
    write_yaml(project / "04_voice" / "voice_manifest.yaml", man)
    r = run_check("voice_segment_quality", project, q)
    assert r.status == "fail" and "trung vị" in r.evidence


def test_split_sentences():
    assert voice.split_sentences("Sông đổ ra biển. Vậy mà mặn chát. Muối từ đâu ra?") == [
        "Sông đổ ra biển.", "Vậy mà mặn chát.", "Muối từ đâu ra?"]
    assert voice.split_sentences("Một câu, có dấu phẩy") == ["Một câu, có dấu phẩy"]


def test_per_sentence_pauses(project, monkeypatch, good_script):
    gate_open(monkeypatch)
    good_script["scenes"][0]["segments"][0]["text"] = "Trời xanh lắm. Vì sao vậy? Cùng tìm hiểu nhé."
    write_yaml(project / "01_script" / "script.yaml", good_script)
    eng = FakeEngine()
    man = voice.synth_all(project, eng, pause_sentence=0.35, pause_question=0.45)  # tham số tường minh
    first = man["segments"][0]
    assert first["sentences"] == 3
    assert [c[0] for c in eng.calls[:3]] == ["Trời xanh lắm.", "Vì sao vậy?", "Cùng tìm hiểu nhé."]
    assert 0.38 <= first["max_gap_s"] <= 0.5                # khoảng ngắt dài nhất ~0,45 giây sau câu hỏi
    n = syllables(good_script["scenes"][0]["segments"][0]["text"])
    assert first["duration_s"] == pytest.approx(n * 0.3 + 0.35 + 0.45 + 0.16, abs=0.08)
    assert man["pauses"]["question_s"] == 0.45


def test_recording_per_sentence_files(project, monkeypatch, good_script):
    gate_open(monkeypatch)
    good_script["scenes"][0]["segments"][0]["text"] = "Câu một ngắn. Câu hai ngắn."
    write_yaml(project / "01_script" / "script.yaml", good_script)
    rec = project / "04_voice" / "recordings"
    rec.mkdir(parents=True)
    import vp.voice as V
    for s in voice_segments(good_script):
        parts = voice.split_sentences(s["text"])
        for k, sent in enumerate(parts, 1):
            a, _ = FakeEngine().synth(sent, "x")
            V._write_wav(rec / f"{s['id']}_s{k}_t1.wav", a)
    man = voice.synth_all(project, voice.RecordingEngine(project), takes=1)
    assert man["segments"][0]["sentences"] == 2
