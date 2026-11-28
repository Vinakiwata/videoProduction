"""Tool 08 — render khung hình từ trang trình chiếu (07) ra MP4."""
import json
import shutil
import subprocess

import pytest

from vp import presentation_tools as pt
from vp import render_tools as rt
from test_presentation import pproj  # noqa: F401  — dự án Tool 07 mẫu (2 khung hình, 120 khung)

NEED = pytest.mark.skipif(not all(shutil.which(x) for x in ("google-chrome", "node", "ffmpeg", "ffprobe")),
                          reason="cần Chrome + Node + ffmpeg")


def _probe(path, *extra):
    r = subprocess.run(["ffprobe", "-v", "error", *extra, "-show_streams", "-of", "json", str(path)],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)["streams"]


@pytest.fixture
def built(pproj):
    pt.build(pproj)
    return pproj


@NEED
def test_render_builds_exact_frames_bt709(built):
    out = rt.build(built, check_gate=False)
    assert out == built / "08_render" / "video_silent.mp4" and out.is_file()
    v = _probe(out, "-count_frames", "-select_streams", "v:0")[0]
    assert int(v["nb_read_frames"]) == 120 and (v["width"], v["height"]) == (1920, 1080)
    assert v["codec_name"] == "h264" and v["pix_fmt"] == "yuv420p" and v.get("color_space") == "bt709"
    man = json.loads((built / "08_render" / "manifest.json").read_text(encoding="utf-8"))
    assert man["frames"] == 120 and man["build_hash"] == pt.build_hash(built) and man["crf"] == 18
    kinds = {s["codec_type"] for s in _probe(built / "08_render" / "preview_voice.mp4")}
    assert kinds == {"video", "audio"}


def test_render_requires_presentation_gate(built, monkeypatch):
    monkeypatch.setattr(rt.review, "gate", lambda p, s: rt.review.GateStatus(False, "chưa duyệt"))
    with pytest.raises(rt.RenderError) as e:
        rt.build(built)
    assert "presentation" in str(e.value)


@NEED
def test_render_aborts_on_page_error(built):
    d = built / "07_presentation" / "data.js"
    d.write_text(d.read_text(encoding="utf-8") + "\nwindow.addEventListener('load', () => { throw new Error('hỏng'); });\n",
                 encoding="utf-8")
    with pytest.raises(rt.RenderError) as e:
        rt.build(built, check_gate=False)
    assert "hỏng" in str(e.value)
    assert not (built / "08_render" / "video_silent.mp4").exists()
    assert not list((built / "08_render").glob("*.tmp.mp4"))


def test_cli_render_error_clean(built, monkeypatch):
    from vp.__main__ import main
    real = shutil.which
    monkeypatch.setattr(rt.shutil, "which", lambda n: None if n == "google-chrome" else real(n))
    monkeypatch.setattr(rt.review, "gate", lambda p, s: rt.review.GateStatus(True, "ĐẠT"))
    with pytest.raises(SystemExit) as e:
        main(["render", "build", str(built)])
    assert str(e.value.code).startswith("LỖI") and "Chrome" in str(e.value.code)


# ---------------- checklist render v3 ----------------
@pytest.fixture
def rendered(built):
    rt.build(built, check_gate=False)
    return built


def _rc(name, project, **params):
    from vp.checks import run_check
    return run_check(name, project, params)


@NEED
def test_rnd_a05_frame_count_mismatch(rendered):
    v = rendered / "08_render" / "video_silent.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(v), "-frames:v", "99", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    str(v.with_name("x.mp4"))], check=True)
    v.with_name("x.mp4").replace(v)
    r = _rc("render_frame_count", rendered)
    assert r.status == "fail" and "99" in r.evidence and "120" in r.evidence


@NEED
def test_rnd_a06_passes_on_real_render(rendered):
    pt.check(rendered)
    assert _rc("render_frame_count", rendered).status == "pass"
    r = _rc("render_matches_presentation", rendered, min_psnr=40, max_frames=4)
    assert r.status == "pass" and "dB" in r.evidence, r.evidence


@NEED
def test_rnd_a06_detects_wrong_frame(rendered):
    pt.check(rendered)
    v = rendered / "08_render" / "video_silent.mp4"
    # lệch 60 khung (sang hẳn khung hình kia — dữ liệu mẫu gần như đứng yên trong mỗi khung hình)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(v), "-vf", "trim=start_frame=60,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop=60",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(v.with_name("x.mp4"))], check=True)
    v.with_name("x.mp4").replace(v)
    r = _rc("render_matches_presentation", rendered, min_psnr=40, max_frames=4)
    assert r.status == "fail" and "dB" in r.evidence


@NEED
def test_rnd_a07_stale_build(rendered):
    assert _rc("render_in_sync", rendered).status == "pass"
    css = rendered / "07_presentation" / "player.css"
    css.write_text(css.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    assert _rc("render_in_sync", rendered).status == "fail"


def test_psnr_luma_ignores_chroma_only_difference():
    """yuv420p làm nhoè màu ở mép (mất chroma) nhưng giữ độ sáng: PSNR độ sáng phải cao, PSNR màu thì không."""
    import numpy as np
    from vp.checks.render import psnr, psnr_luma
    a = np.zeros((40, 40, 3), np.uint8); a[:, :20] = (255, 201, 7)        # vàng | xanh đậm
    a[:, 20:] = (11, 61, 145)
    y = lambda c: 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    b = a.copy()
    # đổi màu cột 19–20 sang màu khác nhưng giữ đúng độ sáng (mô phỏng nhoè chroma)
    for x in (19, 20):
        c = a[0, x].astype(float); g = (y(c) - 0.2126 * c[2] - 0.0722 * c[0]) / 0.7152
        b[:, x] = np.clip([c[2], g, c[0]], 0, 255).astype(np.uint8)
    assert psnr_luma(a, b) > psnr(a, b) + 10
    assert psnr_luma(a, a) == float("inf")


# ---------------- sửa sau review toàn nhánh ----------------
def _chromes():
    r = subprocess.run(["pgrep", "-f", "vp-chrome-"], capture_output=True, text=True)
    return set(r.stdout.split())


def _fake_page(tmp_path, body):
    p = tmp_path / "page.html"
    p.write_text(f"<!doctype html><html><body><script>{body}</script></body></html>", encoding="utf-8")
    return p.resolve().as_uri()


JSDIR = rt.JS.parent


@NEED
def test_cdp_failure_after_launch_closes_chrome(tmp_path):
    """vp.ready bị reject (lỗi sau khi đã mở Chrome) → không để Chrome mồ côi."""
    before = _chromes()
    url = _fake_page(tmp_path, "window.vp = {ready: Promise.reject(new Error('ready hỏng')), errors: []};")
    spec = tmp_path / "s.json"
    spec.write_text(json.dumps({"url": url, "out_dir": str(tmp_path / "o"), "frames": [0], "width": 320, "height": 240}))
    r = subprocess.run(["node", str(JSDIR / "capture.mjs"), str(spec)], capture_output=True, text=True, timeout=60)
    assert r.returncode != 0 and "ready hỏng" in r.stderr
    import time; time.sleep(1)
    assert _chromes() <= before


@NEED
def test_render_mjs_epipe_closes_chrome(built, tmp_path):
    """Đầu đọc (ffmpeg) chết sớm → Node thoát, không treo, không để Chrome mồ côi."""
    before = _chromes()
    spec = tmp_path / "s.json"
    spec.write_text(json.dumps({"url": (built / "07_presentation/index.html").resolve().as_uri() + "?render=1",
                                "width": 1920, "height": 1080, "total": 120}))
    p = subprocess.Popen(["node", str(rt.JS), str(spec)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.stdout.read(200_000); p.stdout.close()
    assert p.wait(timeout=60) != 0
    import time; time.sleep(1)
    assert _chromes() <= before


@NEED
def test_render_reports_ffmpeg_error_not_node_epipe(built, monkeypatch):
    monkeypatch.setattr(rt, "CRF", "abc")                       # ffmpeg từ chối tham số
    with pytest.raises(rt.RenderError) as e:
        rt.build(built, check_gate=False)
    assert "ffmpeg" in str(e.value) and "EPIPE" not in str(e.value)
    assert not list((built / "08_render").glob("*.tmp.mp4"))


@NEED
def test_render_times_out_when_seek_hangs(built, tmp_path):
    """vp.seek không bao giờ xong → hết giờ, báo lỗi rõ, dọn tiến trình và file tạm."""
    before = _chromes()
    d = built / "07_presentation" / "data.js"
    d.write_text(d.read_text(encoding="utf-8") + "\nwindow.addEventListener('load', () => { vp.seek = () => new Promise(() => {}); });\n",
                 encoding="utf-8")
    with pytest.raises(rt.RenderError) as e:
        rt.build(built, check_gate=False, step_timeout_s=3)
    assert "quá thời gian" in str(e.value)
    assert not list((built / "08_render").glob("*.tmp.mp4"))
    import time; time.sleep(1)
    assert _chromes() <= before


def test_rnd_a06_samples_mid_and_transition_frames():
    """Khung mẫu gồm cả giữa khung hình lẫn giữa lượt chuyển cảnh (chuyển động mạnh nhất), rải đều tối đa k khung."""
    from vp.checks.render import sample_frames
    rows = [{"frame": f, "role": r} for f, r in ((0, "start"), (29, "mid"), (59, "end"), (64, "transition"), (89, "mid"), (119, "end"))]
    assert sample_frames(rows, 12) == [29, 64, 89]
    many = [{"frame": i, "role": "mid" if i % 2 else "transition"} for i in range(40)]
    got = sample_frames(many, 12)
    assert len(got) == 12 and got[0] == 0 and got[-1] == 39
