"""Tool 08 — Render khung hình: chụp trang trình chiếu (07) từng khung, đẩy thẳng PNG vào ffmpeg → video chưa có tiếng.
Thiết kế: docs/superpowers/specs/2026-11-28-tool-render-design.md"""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from vp import presentation_tools, review

DIR = "08_render"
JS = Path(__file__).resolve().parent / "js" / "render.mjs"
CRF = 18
PRESET = "veryfast"
COLOR = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]


class RenderError(RuntimeError):
    pass


def _need(tools: dict[str, str]) -> None:
    miss = [label for name, label in tools.items() if not shutil.which(name)]
    if miss:
        raise RenderError("Thiếu công cụ để render: " + ", ".join(miss))


def build(project: Path, check_gate: bool = True) -> Path:
    """Dựng 08_render/video_silent.mp4 (+ preview_voice.mp4, manifest.json) từ 07_presentation."""
    project = Path(project)
    if check_gate:
        g = review.gate(project, "presentation")
        if not g.ok:
            raise RenderError(f"Cổng 'presentation' chưa mở: {g.message}")
    _need({"google-chrome": "Chrome (google-chrome)", "node": "Node", "ffmpeg": "ffmpeg"})
    pres = project / presentation_tools.DIR
    comp = json.loads((pres / "presentation.json").read_text(encoding="utf-8"))
    cv, total = comp["canvas"], int(comp["total_frames"])
    out_dir = project / DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp_mp4 = out_dir / "video_silent.tmp.mp4"
    final = out_dir / "video_silent.mp4"
    t0 = time.time()
    with tempfile.TemporaryDirectory() as tmp:
        spec = Path(tmp) / "spec.json"
        spec.write_text(json.dumps({"url": (pres / "index.html").resolve().as_uri() + "?render=1", "width": cv["width"],
                                    "height": cv["height"], "total": total, "chrome": shutil.which("google-chrome")}), encoding="utf-8")
        log = Path(tmp) / "node.log"
        with open(log, "w", encoding="utf-8") as errf:
            node = subprocess.Popen(["node", str(JS), str(spec)], stdout=subprocess.PIPE, stderr=errf)
            ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "image2pipe", "-framerate", str(cv["fps"]), "-c:v", "png", "-i", "-",
                                   "-vf", "scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int+full_chroma_inp,format=yuv420p",
                                   "-c:v", "libx264", "-crf", str(CRF), "-preset", PRESET, "-pix_fmt", "yuv420p", *COLOR,
                                   "-r", str(cv["fps"]), "-movflags", "+faststart", str(tmp_mp4)],
                                  stdin=node.stdout, stderr=subprocess.PIPE)
            node.stdout.close()
            _, fferr = ff.communicate()
            ncode = node.wait()
        nlog = log.read_text(encoding="utf-8")
    if ncode != 0 or ff.returncode != 0:
        tmp_mp4.unlink(missing_ok=True)
        why = nlog.strip().splitlines()[-5:] if ncode else [fferr.decode(errors="replace")[-800:]]
        raise RenderError("Render thất bại:\n" + "\n".join(why))
    tmp_mp4.replace(final)
    voice = pres / "audio" / "voice.wav"
    if voice.is_file():
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(final), "-i", str(voice), "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                        str(out_dir / "preview_voice.mp4")], check=True)
    (out_dir / "manifest.json").write_text(json.dumps({
        "build_hash": presentation_tools.build_hash(project), "frames": total, "fps": cv["fps"],
        "size": [cv["width"], cv["height"]], "crf": CRF, "preset": PRESET, "seconds": round(time.time() - t0, 1),
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    return final


def lint(project: Path, checklist_dir: Path | None = None):
    from vp.checklist import load_checklist
    from vp.checks import run_check
    cl = load_checklist("render", checklist_dir)
    return [(it, run_check(it["check"], Path(project), it.get("params"))) for it in cl["items"] if it["method"] == "auto"]
