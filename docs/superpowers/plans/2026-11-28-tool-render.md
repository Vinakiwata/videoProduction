# Tool 08 — Render khung hình: kế hoạch thực hiện

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `python -m vp render build` chụp trang 07 từng khung rồi đẩy vào ffmpeg, ra `08_render/video_silent.mp4` (H.264, BT.709) kèm bản xem nhanh có giọng. Checklist `render` v3 kiểm số khung, độ giống trang 07 và bản dựng khớp.

**Architecture:** Node `vp/js/render.mjs` (CDP, tái dùng cách mở Chrome của `capture.mjs`) ghi PNG liên tiếp ra stdout. Python `vp/render_tools.py` nối stdout đó vào stdin của ffmpeg (image2pipe). Các check mới nằm ở `vp/checks/render.py`.

**Tech Stack:** Python 3.13, Node 22, Chrome headless, ffmpeg/ffprobe, Pillow, numpy, pytest.

**Spec:** `docs/superpowers/specs/2026-11-28-tool-render-design.md`

## Global Constraints
- Cần cổng `presentation` MỞ trước khi dựng.
- Mã hoá: `libx264 -crf 18 -preset veryfast -pix_fmt yuv420p`, `scale=out_color_matrix=bt709:out_range=tv`, `-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv`, `-movflags +faststart`, fps = `presentation.json.canvas.fps`.
- Kích thước = `presentation.json.canvas` (dự án mẫu 1080×1920).
- Đầu ra: `08_render/video_silent.mp4`, `08_render/preview_voice.mp4` (video + `07_presentation/audio/voice.wav`, AAC 192k), `08_render/manifest.json`.
- PSNR ngưỡng 40 dB.
- Checklist `render` v3, artifacts `[08_render, 07_presentation/presentation.json]`.

## Review Focus
1. Trang báo lỗi JS giữa chừng (`vp.errors` khác rỗng) → dừng, xoá file dở, báo lỗi rõ; không để lại MP4 cụt. *(Task 1: `test_render_aborts_on_page_error`)*
2. Bản 07 đã dựng lại sau khi render → RND-A07 trượt. *(Task 2: `test_rnd_a07_stale_build`)*
3. Video thiếu hoặc thừa khung so với timeline → RND-A05 trượt, nêu cả hai số. *(Task 2: `test_rnd_a05_frame_count_mismatch`)*
4. Màu bị đổi theo BT.601 hoặc sai khung → RND-A06 trượt (PSNR thấp). *(Task 2: `test_rnd_a06_detects_wrong_frame`)*
5. Chrome/Node/ffmpeg không có → lỗi `RenderError` dễ hiểu, CLI không in traceback. *(Task 1: `test_cli_render_error_clean`)*

---

### Task 1: Bộ dựng `render build`

**Files:**
- Create: `vp/js/render.mjs`, `vp/render_tools.py`, `tests/test_render.py`
- Modify: `vp/__main__.py` (lệnh `render build|lint`, bắt `RenderError`)

**Interfaces:**
- Produces:
  - `render_tools.DIR = "08_render"`
  - `class RenderError(RuntimeError)`
  - `build(project: Path, check_gate: bool = True) -> Path` → trả đường dẫn `video_silent.mp4`, ghi `manifest.json` gồm `{build_hash, frames, fps, size, crf, seconds}`.
  - `lint(project) -> list[(item, CheckResult)]`.
- `render.mjs` nhận `<spec.json>` `{url, width, height, total}`. In PNG lần lượt ra stdout; có `vp.errors` thì in lỗi ra stderr và thoát mã 3.

- [ ] **Step 1: Test** (dùng fixture `pproj` của `tests/test_presentation.py` sau `pt.build`; skip nếu thiếu Chrome/Node/ffmpeg):
  - `test_render_builds_exact_frames_bt709`: `build(pproj, check_gate=False)` → ffprobe: 120 khung, 1920×1080, h264, yuv420p, `color_space == "bt709"`; `manifest["frames"] == 120`; có `preview_voice.mp4` có luồng tiếng.
  - `test_render_requires_presentation_gate`: gate giả ĐÓNG → `RenderError` chứa "presentation".
  - `test_render_aborts_on_page_error`: chèn `window.addEventListener('load',()=>{throw new Error('hỏng')})` vào `07_presentation/data.js` → `RenderError` chứa "hỏng", không còn `video_silent.mp4`.
  - `test_cli_render_error_clean`: monkeypatch `shutil.which` trả None cho "google-chrome" → `main(["render","build",…])` → `SystemExit` bắt đầu bằng "LỖI".
- [ ] **Step 2:** `python3 -m pytest -q tests/test_render.py` → FAIL.
- [ ] **Step 3:** Viết `render.mjs` (chụp `Page.captureScreenshot` PNG, `clip` đúng khung, `vp.seek(f)` tuần tự) và `render_tools.build`:
  - `Popen(node)` nối `stdout` vào `Popen(ffmpeg).stdin`, theo đúng tham số ở Global Constraints;
  - ghi ra `video_silent.tmp.mp4` rồi đổi tên khi cả hai tiến trình thoát 0; lỗi thì xoá file tạm;
  - sau đó ghép bản xem nhanh với `voice.wav`.
- [ ] **Step 4:** `python3 -m pytest -q` → PASS.
- [ ] **Step 5:** Commit `feat(render): Tool 08 dựng video từ trang trình chiếu`.

### Task 2: Check RND-A05/A06/A07, checklist `render` v3

**Files:**
- Create: `vp/checks/render.py`
- Modify: `vp/checks/__init__.py` (import), `checklists/render.yaml` (v3), `tests/test_render.py`

**Interfaces:**
- Consumes: `render_tools.build`, `presentation_tools.build_hash`, `presentation_tools._run_capture`, `07_presentation/check/check_manifest.json` (danh sách khung mốc).
- Produces các check:
  - `render_frame_count(project, params)`: ffprobe `-count_frames` so với `timeline.total_frames`.
  - `render_matches_presentation(project, params)`: lấy các khung vai `mid` của tờ kiểm 07 (tối đa `params.max_frames`, mặc định 12), giải mã khung đó từ MP4 bằng ffmpeg `select=eq(n\,F)` ra RGB, chụp lại khung đó từ trang 07, tính PSNR; dưới `params.min_psnr` (40) thì trượt, nêu khung và số dB.
  - `render_in_sync(project, params)`: `manifest.build_hash == presentation_tools.build_hash(project)`.

- [ ] **Step 1: Test:**
  - `test_rnd_a05_frame_count_mismatch`: MP4 99 khung với timeline 120 → fail, evidence chứa "99" và "120".
  - `test_rnd_a06_passes_on_real_render`: sau `build` → pass, evidence có "dB".
  - `test_rnd_a06_detects_wrong_frame`: thay MP4 bằng video khung lệch 15 khung (`-vf "setpts=PTS+0.5/TB"` hoặc ghép lệch) → fail.
  - `test_rnd_a07_stale_build`: sửa 1 byte `07_presentation/player.css` sau render → fail.
- [ ] **Step 2:** Chạy → FAIL.
- [ ] **Step 3:** Cài đặt check. `checklists/render.yaml` v3:
  - giữ A01–A04;
  - RND-A05 (chặn) `render_frame_count`;
  - RND-A06 (nghiêm trọng) `render_matches_presentation {min_psnr: 40, max_frames: 12}`;
  - RND-A07 (chặn) `render_in_sync`;
  - bỏ RND-C01; giữ C02, C03;
  - artifacts `[08_render, 07_presentation/presentation.json]`.
- [ ] **Step 4:** `python3 -m pytest -q` → PASS.
- [ ] **Step 5:** Commit `feat(render): checklist v3 — số khung, PSNR so trang 07, khớp bản dựng`.

### Task 3: Dựng video mẫu, duyệt cổng 08, tài liệu, PR

**Files:**
- Create: `.claude/skills/vp-render/SKILL.md`
- Modify: `README.md` (dòng công đoạn 8, lệnh), `CLAUDE.md` (skill `vp-render`)

- [ ] **Step 1:** `python -m vp render build projects/vi-sao-nuoc-bien-man` → lint SẠCH. Ghi thời gian dựng.
- [ ] **Step 2:** Tự xem khung trích ở đầu mỗi khung hình (màu, độ nét), xem chậm cảnh mưa và bản đồ (vỡ khối). Chép `preview_voice.mp4` sang `~/Documents/DEV_WORK_SUB/VieNeu-TTS/videoproduction/vi-sao-nuoc-bien-man/`, đối chiếu mã băm trên máy chủ dự án.
- [ ] **Step 3:** Duyệt `render` bằng `vp-kiem-duyet`; chủ dự án xem bản xem nhanh trên điện thoại.
- [ ] **Step 4:** Viết skill, cập nhật README/CLAUDE.md; commit; push `feat/tool-render`; mở PR base `feat/khung-doc` qua `gh api`.
