"""Kiểm tra tự động cho render (08_render): đủ khung, khung giống trang trình chiếu, dựng từ đúng bản 07."""
import json
import subprocess
import tempfile
from pathlib import Path

import numpy as np

from vp.checks import CheckResult, register
from vp.checks.files import load_yaml

VIDEO = "08_render/video_silent.mp4"


def _count_frames(path: Path) -> int:
    r = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                        "stream=nb_read_frames", "-of", "csv=p=0", str(path)], capture_output=True, text=True, check=True)
    return int(r.stdout.strip())


def _decode_frame(path: Path, n: int, w: int, h: int) -> np.ndarray:
    """Khung thứ n của video → RGB (đổi YUV→RGB theo BT.709 như khi mã hoá)."""
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf",
                        f"select=eq(n\\,{n}),scale={w}:{h}:in_color_matrix=bt709:in_range=tv:flags=accurate_rnd+full_chroma_int,format=rgb24",
                        "-frames:v", "1", "-f", "rawvideo", "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.uint8).reshape(h, w, 3)


def psnr(a: np.ndarray, b: np.ndarray) -> float:
    mse = np.mean((a.astype(np.float64) - b.astype(np.float64)) ** 2)
    return float("inf") if mse == 0 else 10 * np.log10(255 ** 2 / mse)


def psnr_luma(a: np.ndarray, b: np.ndarray) -> float:
    """PSNR trên độ sáng (Y theo hệ số BT.709). yuv420p bắt buộc của nền tảng chỉ giữ màu ở 1/4 độ phân giải,
    nên PSNR màu bị chặn trên ~36 dB kể cả khi mã hoá không mất dữ liệu; độ sáng mới phản ánh đúng khung, độ nét, vỡ khối."""
    k = np.array([0.2126, 0.7152, 0.0722])
    ya, yb = a.astype(np.float64) @ k, b.astype(np.float64) @ k
    mse = np.mean((ya - yb) ** 2)
    return float("inf") if mse == 0 else 10 * np.log10(255 ** 2 / mse)


def sample_frames(rows: list[dict], k: int) -> list[int]:
    """Khung mốc giữa khung hình + giữa lượt chuyển cảnh (chuyển động mạnh nhất → nhạy với lệch khung), rải đều tối đa k khung."""
    rows = [r for r in rows if r["role"] in ("mid", "transition")]
    if len(rows) > k:
        rows = [rows[round(i * (len(rows) - 1) / (k - 1))] for i in range(k)] if k > 1 else rows[:1]
    return [r["frame"] for r in rows]


@register("render_frame_count")
def frame_count(project: Path, params: dict) -> CheckResult:
    v = project / params.get("path", VIDEO)
    if not v.is_file():
        return CheckResult("fail", f"Chưa có {params.get('path', VIDEO)}. Chạy: python -m vp render build <dự án>")
    want = int(load_yaml(project, "05_timeline/timeline.yaml")["total_frames"])
    got = _count_frames(v)
    if got != want:
        return CheckResult("fail", f"Video có {got} khung, timeline có {want} khung (lệch {got - want:+d}).")
    return CheckResult("pass", f"Video có đúng {got} khung = timeline ({want}).")


@register("render_matches_presentation")
def matches_presentation(project: Path, params: dict) -> CheckResult:
    from vp import presentation_tools as pt
    v = project / params.get("path", VIDEO)
    mp = project / pt.DIR / "check" / "check_manifest.json"
    if not v.is_file():
        return CheckResult("fail", "Chưa có video render.")
    if not mp.is_file():
        return CheckResult("fail", "Chưa có tờ kiểm 07. Chạy: python -m vp presentation check <dự án>")
    comp = json.loads((project / pt.DIR / "presentation.json").read_text(encoding="utf-8"))
    w, h = comp["canvas"]["width"], comp["canvas"]["height"]
    frames = sample_frames(json.loads(mp.read_text(encoding="utf-8"))["frames"], int(params.get("max_frames", 12)))
    lo = float(params.get("min_psnr", 40))
    from PIL import Image
    with tempfile.TemporaryDirectory() as tmp:
        cap = pt._run_capture(project / pt.DIR / "index.html", frames, Path(tmp) / "ref", measure=False, canvas=comp["canvas"])
        res = []
        for r in cap["frames"]:
            ref = np.asarray(Image.open(r["file"]).convert("RGB"))
            dec = _decode_frame(v, r["frame"], w, h)
            res.append((r["frame"], r["shot"], psnr_luma(dec, ref), psnr(dec, ref)))
    bad = [f"khung {f} ({s}): độ sáng {p:.1f} dB < {lo:g} dB" for f, s, p, _ in res if p < lo]
    if bad:
        return CheckResult("fail", "Khung trong video khác trang trình chiếu (PSNR độ sáng):\n" + "\n".join(f"- {b}" for b in bad))
    worst = min(res, key=lambda x: x[2])
    return CheckResult("pass", f"{len(res)} khung mốc giống trang 07: PSNR độ sáng thấp nhất {worst[2]:.1f} dB (khung {worst[0]}, {worst[1]}), "
                               f"trung bình {sum(r[2] for r in res) / len(res):.1f} dB ≥ {lo:g} dB; PSNR màu {min(r[3] for r in res):.1f}–"
                               f"{max(r[3] for r in res):.1f} dB (giới hạn của yuv420p).")


@register("render_in_sync")
def in_sync(project: Path, params: dict) -> CheckResult:
    from vp import presentation_tools as pt
    from vp import render_tools as rt
    mp = project / rt.DIR / "manifest.json"
    if not mp.is_file():
        return CheckResult("fail", "Chưa có manifest render. Chạy: python -m vp render build <dự án>")
    if json.loads(mp.read_text(encoding="utf-8")).get("build_hash") != pt.build_hash(project):
        return CheckResult("fail", "Video dựng từ bản trình chiếu cũ — 07 đã dựng lại. Chạy lại: python -m vp render build <dự án>")
    return CheckResult("pass", "Video dựng từ đúng bản trình chiếu hiện tại (build_hash khớp).")
