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


def split_sentences(text: str) -> list[str]:
    """Tách câu theo . ? ! … (giữ dấu). Mỗi câu được đọc riêng để chèn khoảng ngắt có kiểm soát."""
    parts = [p.strip() for p in re.split(r"(?<=[.!?…])\s+", text.strip()) if p.strip()]
    return parts or [text.strip()]


def pause_after(sentence: str, pause_sentence: float, pause_question: float) -> float:
    return pause_question if sentence.rstrip().endswith(("?", "!")) else pause_sentence


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
    """Giọng có sẵn dạng file: 04_voice/recordings/<mã đoạn>.<đuôi> (người thu), hoặc nhiều lượt
    <mã đoạn>_t1.wav, <mã đoạn>_t2.wav … (vd. VieNeu chạy trên máy Mac của người dùng). Mỗi lần gọi trả lượt kế tiếp."""
    name = "recording"

    def __init__(self, project: Path, name: str = "recording"):
        self.dir = Path(project) / DIR / "recordings"
        self.name = name
        self.current_id = None
        self._served: dict = {}
        self.current_part = None

    def files(self, seg_id: str, part: int | None = None) -> list[Path]:
        if not self.dir.is_dir():
            return []
        if part is not None:
            return sorted(self.dir.glob(f"{seg_id}_s{part}_t*.*")) or sorted(self.dir.glob(f"{seg_id}_s{part}.*"))
        return sorted({*self.dir.glob(f"{seg_id}.*"), *self.dir.glob(f"{seg_id}_t*.*")})

    def has_parts(self, seg_id: str) -> bool:
        """Có file theo từng câu (<mã>_s1_t1.wav …) không; nếu không, đọc nguyên đoạn như cũ."""
        return bool(self.files(seg_id, 1))

    def synth(self, text: str, voice_name_: str):
        part = getattr(self, "current_part", None)
        files = self.files(self.current_id, part) if part is not None else self.files(self.current_id)
        if not files:
            what = f"{self.current_id}_s{part}_t1.wav" if part is not None else f"{self.current_id}.m4a hoặc {self.current_id}_t1.wav"
            raise VoiceError(f"Thiếu file giọng cho {self.current_id} trong {self.dir} (vd. {what}).")
        key = (self.current_id, part)
        k = self._served.get(key, 0)
        self._served[key] = k + 1
        return _decode(files[k % len(files)]), SR


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


def loudnorm(a: np.ndarray, tempo: float = 1.0, pitch_semitones: float = 0.0) -> np.ndarray:
    """Chuẩn -16 LUFS; tempo < 1 làm chậm giọng (giữ nguyên cao độ, ffmpeg atempo);
    pitch_semitones > 0 nâng tông mà giữ nguyên độ dài (ffmpeg rubberband, dịch cả formant cho giọng trẻ hơn)."""
    af = (f"atempo={tempo:.4f}," if abs(tempo - 1) > 1e-6 else "")
    if abs(pitch_semitones) > 1e-6:
        af += f"rubberband=pitch={2 ** (pitch_semitones / 12):.6f}:formant=shifted:pitchq=quality,"
    af += "loudnorm=I=-16:TP=-1.5:LRA=11"
    r = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                        "-af", af, "-ar", str(SR), "-f", "f32le", "-"],
                       input=a.astype(np.float32).tobytes(), capture_output=True, check=True)
    out = np.frombuffer(r.stdout, dtype=np.float32).copy()
    n = int(round(len(a) / tempo))
    return out[:n] if len(out) >= n else np.pad(out, (0, n - len(out)))


def f0_median(a: np.ndarray) -> float | None:
    """Cao độ trung vị (Hz) của phần có tiếng — tự tương quan trên khung 40 ms, đã hạ mẫu 16 kHz cho nhanh."""
    sr = 16000
    x = a[:: SR // sr].astype(np.float64)
    fr, hop = int(0.04 * sr), int(0.02 * sr)
    if len(x) < fr:
        return None
    thr = max(1e-4, 0.1 * float(np.sqrt(np.mean(x ** 2)) or 0))
    lo, hi = int(sr / 400), int(sr / 70)
    out = []
    for i in range(0, len(x) - fr, hop):
        s_ = x[i:i + fr]
        if np.sqrt(np.mean(s_ ** 2)) < thr:
            continue
        s_ = s_ - s_.mean()
        c = np.correlate(s_, s_, "full")[fr - 1:]
        k = lo + int(np.argmax(c[lo:hi]))
        if c[0] > 0 and c[k] > 0.4 * c[0]:
            out.append(sr / k)
    return float(np.median(out)) if out else None


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

def target_speed(project: Path, channels_dir: Path | None = None) -> float:
    """Tốc độ mục tiêu để chọn lượt: voice_profile của brief, nếu không có thì của kênh (channel_ref), cuối cùng 3,2."""
    brief = load_yaml(Path(project), "00_brief/brief.yaml")
    v = (brief.get("voice_profile") or {}).get("syllables_per_second")
    if not v and brief.get("channel_ref"):
        cp = Path(channels_dir or CHANNELS_DIR) / brief["channel_ref"] / "channel.yaml"
        if cp.is_file():
            v = (load_yaml(cp.parent, "channel.yaml").get("voice_profile") or {}).get("syllables_per_second")
    return float(v or 3.2)


def synth_all(project: Path, engine, takes: int = 1, only: set[str] | None = None, check_gate: bool = True,
              tempo: float = 1.0, pause_sentence: float = 0.45, pause_question: float = 0.55,
              per_sentence: bool = True, pitch_semitones: float | None = None,
              even_speed: float = 0.0, max_tempo_adjust: float = 0.10) -> dict:
    project = Path(project)
    if check_gate:
        g = review.gate(project, "animatic")
        if not g.ok:
            raise VoiceError(f"Cổng 'animatic' chưa mở: {g.message}")
    script = load_yaml(project, "01_script/script.yaml")
    brief = load_yaml(project, "00_brief/brief.yaml")
    vname = voice_name(brief["brand"]["voice"])
    if pitch_semitones is None:
        pitch_semitones = float(brief["brand"].get("voice_pitch_semitones") or 0.0)
    pron = (script.get("meta") or {}).get("pronunciation") or script.get("pronunciation") or {}
    mpath = project / DIR / "voice_manifest.yaml"
    old = {}
    if only and mpath.is_file():
        old = {m["id"]: m for m in load_yaml(project, f"{DIR}/voice_manifest.yaml")["segments"]}
    target_sps = target_speed(project)

    # lượt 1: thu mọi lượt của mọi câu
    plan = []
    for _, seg in script_segments(script):
        if seg.get("kind") != "voice":
            continue
        if only and seg["id"] not in only and seg["id"] in old:
            plan.append((seg, None, None, None))
            continue
        spoken = prepare_text(seg["text"], pron)
        use_parts = per_sentence and (not hasattr(engine, "has_parts") or engine.has_parts(seg["id"]))
        sentences = split_sentences(spoken) if use_parts else [spoken]
        cands = []
        for k, sent in enumerate(sentences, 1):
            opts = []
            for _ in range(max(1, takes)):
                if hasattr(engine, "current_id"):
                    engine.current_id = seg["id"]
                    engine.current_part = k if use_parts else None
                raw, sr = engine.synth(sent, vname)
                part = trim(_resample(np.asarray(raw, dtype=np.float32), sr))
                opts.append((part, measure(part, sent), f0_median(part)))
            cands.append(opts)
        plan.append((seg, spoken, sentences, cands))
    # cao độ chung của cả bài = trung vị cao độ mọi lượt -> chọn lượt gần nhất để giọng đồng nhất giữa các đoạn
    allf = [f for p in plan if p[3] for opts in p[3] for _, _, f in opts if f]
    ref_f0 = float(np.median(allf)) if allf else None
    kept = [old[seg["id"]] for seg, _s, _ss, cands in plan if cands is None]      # các đoạn giữ nguyên khi --only
    if kept:
        # --only: giữ mốc của cả bài — cao độ các đoạn giữ nguyên (quy về trước khi nâng tông), không chỉ các lượt mới
        kf = [k["f0_hz"] / 2 ** (float(k.get("pitch_semitones") or 0) / 12) for k in kept if k.get("f0_hz")]
        if kf:
            ref_f0 = float(np.median(kf))

    def pick(opts):
        def sc(o):
            pen = abs(12 * np.log2(o[2] / ref_f0)) if (ref_f0 and o[2]) else 0.0
            return _score(o[1], target_sps) + pen
        return min(opts, key=sc)

    built = {}
    for seg, spoken, sentences, cands in plan:
        if cands is None:
            continue
        pieces = []
        for k, (sent, opts) in enumerate(zip(sentences, cands), 1):
            pieces.append(pick(opts)[0])
            if k < len(sentences):     # khoảng ngắt sau câu (đã có 2 x PAD_S đệm hai bên)
                gap = max(0.0, pause_after(sent, pause_sentence, pause_question) - 2 * PAD_S)
                pieces.append(np.zeros(int(round(gap * SR)), dtype=np.float32))
        raw_a = np.concatenate(pieces)
        built[seg["id"]] = (raw_a, measure(raw_a, seg["text"])["sps"])
    # cân tốc độ: đoạn lệch quá ±even_speed so với trung vị được làm nhanh/chậm về mép dải, tối đa ±max_tempo_adjust (giữ cao độ)
    # trung vị tốc độ tính trên cả bài: đoạn giữ nguyên (--only) quy về tốc độ trước khi cân (sps / tempo đã áp)
    all_sps = [v[1] for v in built.values()] + [k["sps"] / float(k.get("tempo") or 1.0) for k in kept if k.get("sps")]
    med_sps = float(np.median(all_sps)) if all_sps else 0.0
    seg_tempo = {}
    for sid, (_, sp) in built.items():
        t_ = 1.0
        if even_speed and med_sps and sp:
            want = min(max(sp, med_sps * (1 - even_speed)), med_sps * (1 + even_speed))
            t_ = min(max(want / sp, 1 - max_tempo_adjust), 1 + max_tempo_adjust)
            t_ = 1.0 if abs(t_ - 1) < 1e-3 else round(t_, 4)
        seg_tempo[sid] = t_

    entries = []
    for seg, spoken, sentences, cands in plan:
        if cands is None:
            entries.append(old[seg["id"]])
            continue
        a = loudnorm(built[seg["id"]][0], tempo * seg_tempo[seg["id"]], pitch_semitones)
        m = measure(a, seg["text"])
        f = project / DIR / "segments" / f"{seg['id']}.wav"
        _write_wav(f, a)
        fz = f0_median(a)
        entries.append({"id": seg["id"], "file": f"segments/{seg['id']}.wav", "text": seg["text"], "spoken_text": spoken,
                        **m, "takes": max(1, takes), "tempo": round(tempo * seg_tempo[seg["id"]], 4), "pitch_semitones": pitch_semitones,
                        "f0_hz": round(fz, 1) if fz else None, "sentences": len(sentences), "sha256": _sha(f)})

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
    fs = [e["f0_hz"] for e in entries if e.get("f0_hz")]
    man = {"engine": engine.name, "voice": vname, "tempo": tempo, "pitch_semitones": pitch_semitones,
           "f0_median_hz": round(float(np.median(fs)), 1) if fs else None,
           "pitch_spread_semitones": round(float(12 * np.log2(max(fs) / min(fs))), 2) if len(fs) > 1 else 0.0,
           "pauses": {"sentence_s": pause_sentence, "question_s": pause_question, "per_sentence": per_sentence}, "sample_rate": SR, "total_s": round(len(full) / SR, 3),
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
