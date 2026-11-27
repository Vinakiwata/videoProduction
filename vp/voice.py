"""Tool giọng đọc — tạo/nhập giọng cho từng đoạn, xử lý, đo, ghi manifest. Xem spec 2026-11-27-tool-giong-doc-design.md."""
from __future__ import annotations

import hashlib
import re
import shutil
import statistics
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np

from vp import review
from vp.channel import CHANNELS_DIR
from vp.checks.files import load_yaml
from vp.checks.script import segments as script_segments
from vp.checks.script import syllables
from vp.project import dump_yaml

DIR = "04_voice"
SR = 48000
PAD_S = 0.08
SIL_DB = -45.0
FRAME_S = 0.02


class VoiceError(RuntimeError):
    pass


# ---------- văn bản ----------

def prepare_text(text: str, pronunciation: dict | None) -> str:
    """Áp từ điển phát âm (thay trọn từ, không phân biệt hoa thường)."""
    out = text
    for k, v in (pronunciation or {}).items():
        out = re.sub(rf"(?<!\w){re.escape(k)}(?!\w)", v, out, flags=re.IGNORECASE)
    return out


def voice_name(brand_voice: str) -> str:
    return brand_voice.split(":", 1)[1].strip() if ":" in brand_voice else brand_voice.strip()


# ---------- engine ----------

class VieneuEngine:
    name = "vieneu"

    def __init__(self, **kwargs):
        try:
            from vieneu import Vieneu  # type: ignore
        except ImportError as e:
            raise VoiceError(
                "Chưa cài VieNeu-TTS. Cần mạng để: pip install vieneu (CPU) — lần chạy đầu sẽ tải mô hình từ HuggingFace. "
                "Hoặc dùng --engine recording với file thu âm trong 04_voice/recordings/.") from e
        self.tts = Vieneu(**kwargs)

    def synth(self, text: str, voice_name_: str):
        audio = self.tts.infer(text, voice=voice_name_)
        return np.asarray(audio, dtype=np.float32), int(getattr(self.tts, "sample_rate", SR))


def _decode(path: Path) -> np.ndarray:
    """Giải mã mọi định dạng ffmpeg đọc được -> float32 48 kHz mono."""
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float32).copy()


class RecordingEngine:
    """Giọng người thu: 04_voice/recordings/<mã đoạn>.<bất kỳ định dạng ffmpeg đọc được>."""
    name = "recording"

    def __init__(self, project: Path):
        self.dir = Path(project) / DIR / "recordings"
        self.current_id = None

    def synth(self, text: str, voice_name_: str):
        files = sorted(self.dir.glob(f"{self.current_id}.*")) if self.dir.is_dir() else []
        if not files:
            raise VoiceError(f"Thiếu file thu âm cho {self.current_id} trong {self.dir} (vd. {self.current_id}.m4a).")
        return _decode(files[0]), SR


# ---------- xử lý & đo ----------

def _resample(a: np.ndarray, sr: int) -> np.ndarray:
    if sr == SR:
        return a.astype(np.float32)
    x = np.linspace(0, len(a), int(round(len(a) * SR / sr)), endpoint=False)
    return np.interp(x, np.arange(len(a)), a).astype(np.float32)


def _frames_db(a: np.ndarray) -> np.ndarray:
    n = int(FRAME_S * SR)
    k = len(a) // n
    if k == 0:
        return np.array([-120.0])
    f = a[: k * n].reshape(k, n)
    rms = np.sqrt((f ** 2).mean(axis=1)) + 1e-12
    return 20 * np.log10(rms)


def trim(a: np.ndarray) -> np.ndarray:
    db = _frames_db(a)
    on = np.where(db > SIL_DB)[0]
    if len(on) == 0:
        raise VoiceError("Đoạn giọng toàn khoảng lặng.")
    n = int(FRAME_S * SR)
    s, e = on[0] * n, (on[-1] + 1) * n
    pad = int(PAD_S * SR)
    return a[max(0, s - pad): min(len(a), e + pad)]


def loudnorm(a: np.ndarray) -> np.ndarray:
    r = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), "-f", "f32le", "-"],
                       input=a.astype(np.float32).tobytes(), capture_output=True, check=True)
    out = np.frombuffer(r.stdout, dtype=np.float32).copy()
    return out[: len(a)] if len(out) >= len(a) else np.pad(out, (0, len(a) - len(out)))


def measure(a: np.ndarray, text: str) -> dict:
    db = _frames_db(a)
    on = db > SIL_DB
    lead = int(np.argmax(on)) * FRAME_S if on.any() else len(a) / SR
    trail = int(np.argmax(on[::-1])) * FRAME_S if on.any() else len(a) / SR
    gap, cur = 0.0, 0
    if on.any():
        inner = on[np.argmax(on): len(on) - np.argmax(on[::-1])]
        for v in inner:
            cur = cur + 1 if not v else 0
            gap = max(gap, cur * FRAME_S)
    dur = len(a) / SR
    syl = syllables(text)
    peak = 20 * np.log10(np.abs(a).max() + 1e-12)
    return {"duration_s": round(dur, 3), "syllables": syl, "sps": round(syl / dur, 2) if dur else 0.0,
            "peak_dbfs": round(float(peak), 2), "lead_s": round(lead, 3), "trail_s": round(trail, 3),
            "max_gap_s": round(gap, 3)}


def _write_wav(path: Path, a: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())


def _read_wav(path: Path) -> np.ndarray:
    with wave.open(str(path), "rb") as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _score(m: dict, target_sps: float) -> float:
    """Thấp hơn là tốt hơn: phạt khoảng lặng giữa câu, lệch tốc độ, đỉnh sát 0 dB."""
    return m["max_gap_s"] * 4 + abs(m["sps"] - target_sps) + max(0.0, m["peak_dbfs"] + 1) * 2


# ---------- dựng ----------

def synth_all(project: Path, engine, takes: int = 1, only: set[str] | None = None, check_gate: bool = True) -> dict:
    project = Path(project)
    if check_gate:
        g = review.gate(project, "animatic")
        if not g.ok:
            raise VoiceError(f"Cổng 'animatic' chưa mở: {g.message}")
    script = load_yaml(project, "01_script/script.yaml")
    brief = load_yaml(project, "00_brief/brief.yaml")
    vname = voice_name(brief["brand"]["voice"])
    pron = (script.get("meta") or {}).get("pronunciation") or script.get("pronunciation") or {}
    mpath = project / DIR / "voice_manifest.yaml"
    old = {}
    if only and mpath.is_file():
        old = {m["id"]: m for m in load_yaml(project, f"{DIR}/voice_manifest.yaml")["segments"]}
    target_sps = float(((brief.get("voice_profile") or {}).get("syllables_per_second")) or 3.2)

    entries = []
    for _, seg in script_segments(script):
        if seg.get("kind") != "voice":
            continue
        if only and seg["id"] not in only and seg["id"] in old:
            entries.append(old[seg["id"]])
            continue
        spoken = prepare_text(seg["text"], pron)
        best = None
        for _ in range(max(1, takes)):
            if hasattr(engine, "current_id"):
                engine.current_id = seg["id"]
            raw, sr = engine.synth(spoken, vname)
            a = loudnorm(trim(_resample(np.asarray(raw, dtype=np.float32), sr)))
            m = measure(a, seg["text"])
            if best is None or _score(m, target_sps) < _score(best[1], target_sps):
                best = (a, m)
        a, m = best
        f = project / DIR / "segments" / f"{seg['id']}.wav"
        _write_wav(f, a)
        entries.append({"id": seg["id"], "file": f"segments/{seg['id']}.wav", "text": seg["text"], "spoken_text": spoken,
                        **m, "takes": max(1, takes), "sha256": _sha(f)})

    # nối toàn bộ theo thứ tự kịch bản, chèn im lặng
    by = {e["id"]: e for e in entries}
    parts = []
    for _, seg in script_segments(script):
        if seg.get("kind") == "voice":
            parts.append(_read_wav(project / DIR / by[seg["id"]]["file"]))
        else:
            parts.append(np.zeros(int(round(float(seg.get("est_duration_s") or 0) * SR)), dtype=np.float32))
    full = np.concatenate(parts) if parts else np.zeros(0, dtype=np.float32)
    _write_wav(project / DIR / "voice_full.wav", full)
    sps = [e["sps"] for e in entries]
    man = {"engine": engine.name, "voice": vname, "sample_rate": SR, "total_s": round(len(full) / SR, 3),
           "measured_sps_median": round(statistics.median(sps), 2) if sps else None,
           "pronunciation_applied": pron, "segments": entries}
    dump_yaml(mpath, man)
    return man


def calibrate(project: Path, apply: bool = False, channels_dir: Path | None = None) -> dict:
    project = Path(project)
    man = load_yaml(project, f"{DIR}/voice_manifest.yaml")
    sps = round(statistics.median(e["sps"] for e in man["segments"]), 2)
    res = {"measured_sps": sps, "segments": len(man["segments"]), "applied_to": None}
    if apply:
        ref = load_yaml(project, "00_brief/brief.yaml").get("channel_ref")
        if not ref:
            raise VoiceError("Brief không có channel_ref — không biết ghi hiệu chỉnh vào kênh nào.")
        cp = Path(channels_dir or CHANNELS_DIR) / ref / "channel.yaml"
        ch = load_yaml(cp.parent, "channel.yaml")
        ch.setdefault("voice_profile", {}).update({"syllables_per_second": sps, "calibrated": True,
                                                   "calibrated_from": f"{project.name} ({man['engine']}, {man['voice']})"})
        dump_yaml(cp, ch)
        res["applied_to"] = str(cp)
    return res


def to_animatic(project: Path) -> int:
    project = Path(project)
    man = load_yaml(project, f"{DIR}/voice_manifest.yaml")
    dst = project / "03_animatic" / "scratch_voice"
    dst.mkdir(parents=True, exist_ok=True)
    for e in man["segments"]:
        shutil.copy(project / DIR / e["file"], dst / f"{e['id']}.wav")
    return len(man["segments"])


def recording_sheet(project: Path) -> Path:
    """Phiếu thu âm: mỗi dòng một đoạn — tên file cần lưu, câu cần đọc (đã áp phát âm), thời lượng gợi ý."""
    project = Path(project)
    script = load_yaml(project, "01_script/script.yaml")
    pron = (script.get("meta") or {}).get("pronunciation") or script.get("pronunciation") or {}
    out = [f"# Phiếu thu âm — {script['meta']['title']}", "",
           "Thu trong phòng yên tĩnh, điện thoại cách miệng khoảng 20–30 cm, giữ cùng một khoảng cách và giọng cho mọi câu.",
           "Mỗi câu lưu **một file riêng**, đặt tên đúng cột *Tên file* (đuôi .m4a / .wav / .mp3 đều được), "
           "rồi chép vào `04_voice/recordings/`. Đọc tự nhiên, để trống khoảng 0,5 giây trước và sau câu.", "",
           "| Tên file | Câu cần đọc | Gợi ý thời lượng |", "|---|---|---|"]
    for _, seg in script_segments(script):
        if seg.get("kind") == "voice":
            out.append(f"| `{seg['id']}` | {prepare_text(seg['text'], pron)} | ~{float(seg['est_duration_s']):.1f}s |")
    out += ["", "Sau đó chạy: `python -m vp voice synth projects/<dự án> --engine recording`", ""]
    f = project / DIR / "recording_sheet.md"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text("\n".join(out), encoding="utf-8")
    return f
