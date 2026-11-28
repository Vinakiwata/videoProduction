"""Tool animatic — video nháp: khung storyboard theo đúng mốc thời gian + phụ đề lời + tiếng động nháp."""
import hashlib
import json
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from vp import review
from vp.checks.files import load_yaml
from vp.checks.script import segments as script_segments
from vp.design_preview import _font, _rgb, _text_in_box, preview_size, render_frame
from vp.project import dump_yaml
from vp.sfx_synth import synth

DIR = "03_animatic"
SR = 48000
CAPTION_H = 96
# khung hình = nửa canvas (preview_size), dải phụ đề CAPTION_H nằm RIÊNG bên dưới, không che hình


class AnimaticError(RuntimeError):
    pass


def _wav_seconds(p: Path) -> float:
    with wave.open(str(p), "rb") as w:
        return w.getnframes() / w.getframerate()


def _read_wav(p: Path, sr: int) -> np.ndarray:
    with wave.open(str(p), "rb") as w:
        if w.getsampwidth() != 2:
            raise AnimaticError(f"{p.name}: chỉ hỗ trợ WAV 16-bit")
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        ch, rate = w.getnchannels(), w.getframerate()
    if ch > 1:
        data = data.reshape(-1, ch).mean(axis=1)
    if rate != sr:  # nội suy tuyến tính đơn giản — đủ cho giọng nháp
        x = np.linspace(0, len(data), int(len(data) * sr / rate), endpoint=False)
        data = np.interp(x, np.arange(len(data)), data).astype(np.float32)
    return data


# ---------- thời gian ----------

def compute_timing(project: Path) -> dict:
    project = Path(project)
    script = load_yaml(project, "01_script/script.yaml")
    sb = load_yaml(project, "02_design/storyboard.yaml")
    sv = project / DIR / "scratch_voice"
    segs, t = [], 0.0
    for _, s in script_segments(script):
        wav = sv / f"{s['id']}.wav"
        if s.get("kind") == "voice" and wav.is_file():
            d, src = round(_wav_seconds(wav), 3), "scratch"
        else:
            d, src = float(s.get("est_duration_s") or 0), "estimate" if s.get("kind") == "voice" else "silent"
        segs.append({"id": s["id"], "kind": s.get("kind"), "start_s": round(t, 3), "dur_s": d, "source": src,
                     "text": s.get("text")})
        t += d
    by = {s["id"]: s for s in segs}
    shots = []
    for sh in sb.get("shots") or []:
        sg = by[sh["segment"]]
        a, b = sh["span"]
        shots.append({"id": sh["id"], "segment": sh["segment"], "start_s": round(sg["start_s"] + sg["dur_s"] * a, 3),
                      "dur_s": round(sg["dur_s"] * (b - a), 3)})
    shots.sort(key=lambda s: s["start_s"])
    timing = {"total_s": round(t, 3), "segments": segs, "shots": shots}
    (project / DIR).mkdir(parents=True, exist_ok=True)
    dump_yaml(project / DIR / "timing.yaml", timing)
    return timing


# ---------- âm thanh ----------

def _event_frac(el: dict, event: str) -> float:
    if event == "exit":
        return (el.get("exit") or {}).get("at", 1.0)
    return (el.get(event) or {}).get("at", 0.0) if event == "enter" else 0.0


def build_audio(project: Path, timing: dict, sr: int = SR) -> np.ndarray:
    project = Path(project)
    n = round(timing["total_s"] * sr)
    out = np.zeros(n, dtype=np.float32)

    def place(sig, t):
        i = int(round(t * sr))
        if i >= n:
            return
        m = min(len(sig), n - i)
        out[i:i + m] += sig[:m]

    sv = project / DIR / "scratch_voice"
    for s in timing["segments"]:
        if s["source"] == "scratch":
            place(_read_wav(sv / f"{s['id']}.wav", sr), s["start_s"])
    sb = load_yaml(project, "02_design/storyboard.yaml")
    tshot = {s["id"]: s for s in timing["shots"]}
    for sh in sb.get("shots") or []:
        els = {e["id"]: e for e in sh.get("elements") or []}
        for fx in sh.get("sfx") or []:
            ts = tshot[sh["id"]]
            place(synth(fx["name"], sr), ts["start_s"] + ts["dur_s"] * _event_frac(els.get(fx["target"], {}), fx["event"]))
    peak = np.abs(out).max()
    if peak > 0.95:
        out *= 0.95 / peak
    return out


def _write_wav(path: Path, data: np.ndarray, sr: int) -> None:
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(data, -1, 1) * 32767).astype(np.int16).tobytes())


# ---------- hình ----------

def element_alpha(el: dict, t: float, dur: float) -> float:
    """Độ hiện (0–1) của phần tử ở giây t trong khung dài dur."""
    a = 1.0
    en = el.get("enter")
    if en:
        t0 = en["at"] * dur
        d = max(en.get("dur_s", 0.3), 1e-3)
        a = 0.0 if t < t0 else min(1.0, (t - t0) / d)
    ex = el.get("exit")
    if ex:
        t1 = ex["at"] * dur
        d = max(ex.get("dur_s", 0.3), 1e-3)
        if t >= t1:
            a = min(a, max(0.0, 1 - (t - t1) / d))
    return a


_LAYERS: dict = {}


def _layers(shot, assets, canvas):
    """Nền trống + mỗi phần tử một lớp (ảnh, mặt nạ) — tính một lần cho mỗi khung."""
    key = id(shot)
    if key not in _LAYERS:
        empty = render_frame(dict(shot, elements=[]), assets, canvas)
        layers = []
        for e in shot.get("elements") or []:
            img = render_frame(dict(shot, elements=[e]), assets, canvas)
            layers.append((img, _mask(img, empty)))
        _LAYERS.clear()
        _LAYERS[key] = (empty, layers)
    return _LAYERS[key]


def _frame(shot, assets, canvas, t, dur, seg, timecode):
    empty, layers = _layers(shot, assets, canvas)
    pic = empty.copy()
    for e, (img, mask) in zip(shot.get("elements") or [], layers):
        al = element_alpha(e, t, dur)
        if al <= 0:
            continue
        pic.paste(img, (0, 0), mask if al >= 1 else mask.point(lambda v: int(v * al)))
    W, H = pic.size
    OUT_H = H + CAPTION_H
    base = Image.new("RGB", (W, OUT_H), (12, 12, 14))
    base.paste(pic, (0, 0))
    d = ImageDraw.Draw(base, "RGBA")
    spoken = seg.get("text") or "(im lặng)"
    _text_in_box(d, [16, H + 10, W - 16, OUT_H], spoken, _font(26, True), (255, 255, 255), CAPTION_H - 14)
    tag = f"{shot['id']}  {timecode}"
    f = _font(16, True)
    tw = d.textlength(tag, font=f)
    d.rectangle([W - tw - 16, 0, W, 24], fill=(0, 0, 0, 180))
    d.text((W - tw - 8, 3), tag, font=f, fill=(255, 210, 63))
    return base


def _mask(layer, bg):
    """Vùng điểm ảnh khác nền (phần tử vừa vẽ)."""
    a = np.asarray(layer.convert("RGB"), dtype=np.int16)
    b = np.asarray(bg.convert("RGB"), dtype=np.int16)
    m = (np.abs(a - b).sum(axis=2) > 6).astype(np.uint8) * 255
    return Image.fromarray(m, "L")


# ---------- dựng ----------

def input_hash(project: Path, fps: int) -> str:
    project = Path(project)
    h = hashlib.sha256()
    for rel in ("01_script/script.yaml", "02_design/storyboard.yaml"):
        h.update(json.dumps(load_yaml(project, rel), sort_keys=True, ensure_ascii=False, default=str).encode())
    sv = project / DIR / "scratch_voice"
    if sv.is_dir():
        for f in sorted(sv.glob("*.wav")):
            h.update(f.name.encode()); h.update(hashlib.sha256(f.read_bytes()).hexdigest().encode())
    W, H = preview_size(load_yaml(project, "02_design/storyboard.yaml")["meta"]["canvas"])
    h.update(f"fps={fps};w={W};h={H + CAPTION_H};layout=caption_below".encode())
    return h.hexdigest()


def build(project: Path, fps: int = 15, check_gate: bool = False) -> Path:
    project = Path(project)
    if check_gate:
        g = review.gate(project, "design")
        if not g.ok:
            raise AnimaticError(f"Cổng 'design' chưa mở: {g.message}")
    timing = compute_timing(project)
    sb = load_yaml(project, "02_design/storyboard.yaml")
    assets = {a["id"]: a for a in sb.get("assets") or []}
    canvas = sb["meta"]["canvas"]
    W, H = preview_size(canvas)
    OUT_H = H + CAPTION_H
    shots = {s["id"]: s for s in sb.get("shots") or []}
    segs = {s["id"]: s for s in timing["segments"]}
    out = project / DIR / "animatic.mp4"
    nframes = round(timing["total_s"] * fps)
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "a.wav"
        _write_wav(wav, build_audio(project, timing), SR)
        cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{OUT_H}", "-r", str(fps),
               "-i", "-", "-i", str(wav), "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "128k", "-shortest", str(out)]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        cache = {}
        k = 0
        for i in range(nframes):
            t = i / fps
            while k + 1 < len(timing["shots"]) and timing["shots"][k + 1]["start_s"] <= t + 1e-9:
                k += 1
            ts = timing["shots"][k]
            sh = shots[ts["id"]]
            lt = t - ts["start_s"]
            alphas = tuple(round(element_alpha(e, lt, ts["dur_s"]), 2) for e in sh.get("elements") or [])
            m, s = divmod(t, 60)
            key = (ts["id"], alphas, int(t))
            if key not in cache:
                cache.clear()
                img = _frame(sh, assets, canvas, lt, ts["dur_s"], segs[sh["segment"]], f"{int(m):02d}:{int(s):02d}")
                cache[key] = img.tobytes()
            proc.stdin.write(cache[key])
        proc.stdin.close()
        if proc.wait() != 0:
            raise AnimaticError("ffmpeg dựng animatic thất bại")
    voice_src = sorted({s["source"] for s in timing["segments"] if s["kind"] == "voice"})
    (project / DIR / "manifest.json").write_text(json.dumps({
        "hash": input_hash(project, fps), "fps": fps, "size": [W, OUT_H], "total_s": timing["total_s"],
        "voice_source": "scratch" if voice_src == ["scratch"] else ("mixed" if "scratch" in voice_src else "estimate"),
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    return out
