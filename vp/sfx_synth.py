"""Tiếng động NHÁP tổng hợp bằng numpy — chỉ dùng cho animatic. Bản thật dùng thư viện SFX có giấy phép."""
import numpy as np


def _env(n, attack=0.005, sr=48000):
    a = max(1, int(attack * sr))
    e = np.exp(-np.linspace(0, 6, n))
    e[:a] *= np.linspace(0, 1, a)
    return e


def _noise(n, seed):
    return np.random.default_rng(seed).uniform(-1, 1, n)


def synth(name: str, sr: int = 48000) -> np.ndarray:
    k = name.lower()
    if "pop" in k:
        n = int(0.12 * sr); t = np.arange(n) / sr
        f = np.linspace(900, 300, n)
        sig = np.sin(2 * np.pi * np.cumsum(f) / sr) * _env(n, sr=sr)
        amp = 0.35 if "nhẹ" in k else 0.6
    elif "click" in k:
        n = int(0.04 * sr)
        sig = _noise(n, 1) * _env(n, 0.001, sr) ; amp = 0.5
    elif "whoosh" in k:
        n = int(0.7 * sr)
        x = _noise(n, 2)
        k_len = 40
        x = np.convolve(x, np.ones(k_len) / k_len, mode="same")      # lọc thấp thô
        win = np.sin(np.linspace(0, np.pi, n)) ** 2
        sig = x * win / (np.abs(x).max() + 1e-9); amp = 0.35 if "nhẹ" in k else 0.5
    elif any(w in k for w in ("nước", "róc rách", "chảy")):
        n = int(1.0 * sr); t = np.arange(n) / sr
        sig = np.zeros(n)
        rng = np.random.default_rng(3)
        for s in rng.uniform(0, 0.9, 14):
            i = int(s * sr); m = int(0.06 * sr); tt = np.arange(m) / sr
            f = rng.uniform(500, 1400)
            sig[i:i + m] += np.sin(2 * np.pi * f * tt * (1 + 3 * tt)) * _env(m, sr=sr)
        sig /= np.abs(sig).max() + 1e-9; amp = 0.3
    elif "lách tách" in k or "tách" in k:
        n = int(0.6 * sr); sig = np.zeros(n)
        rng = np.random.default_rng(4)
        for s in rng.uniform(0, 0.55, 9):
            i = int(s * sr); m = int(0.012 * sr)
            sig[i:i + m] += _noise(m, int(s * 1e6)) * _env(m, 0.0005, sr)
        sig /= np.abs(sig).max() + 1e-9; amp = 0.35
    else:  # blip mặc định
        n = int(0.15 * sr); t = np.arange(n) / sr
        sig = np.sin(2 * np.pi * 660 * t) * _env(n, sr=sr); amp = 0.4
    return (amp * sig).astype(np.float32)
