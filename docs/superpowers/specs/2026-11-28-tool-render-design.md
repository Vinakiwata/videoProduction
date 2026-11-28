# Tool 08 — Render khung hình (08_render)

Ngày 28/11/2026. Chủ dự án duyệt thiết kế ngắn này.

## Ý định
Biến trang trình chiếu đã duyệt (07) thành video chưa có tiếng, đúng từng khung, để Tool 09 ghép tiếng. Trang 07 là bộ dựng duy nhất (quyết định của Tool 07): cái gì đã duyệt ở 07 phải ra đúng như vậy trong video.

## Các cách đã cân nhắc
- **Chụp tuần tự bằng bộ chụp của Tool 07, đẩy PNG thẳng vào ffmpeg** *(đã chọn)*: tất định, không tốn đĩa.
- Quay màn hình: không tất định, rớt khung. Loại.
- Ghi 1602 PNG ra đĩa rồi mới mã hoá: tốn khoảng 2 GB mà không lợi gì. Loại.

## Thiết kế
- **Lệnh:** `python -m vp render build <dự án>`. Yêu cầu cổng `presentation` mở.
- **Chụp:** `vp/js/render.mjs` mở `07_presentation/index.html?render=1` ở đúng khung `presentation.json.canvas`, tua `vp.seek(f)` lần lượt f = 0…total_frames−1. Mỗi khung chụp PNG rồi ghi ra stdout theo kiểu image2pipe. Có lỗi JS (`vp.errors`) thì dừng và báo.
- **Mã hoá:** ffmpeg `-f image2pipe -framerate <fps> -i -`, `libx264 -crf 18 -preset veryfast -pix_fmt yuv420p`.
  - Đổi màu theo BT.709 (`scale=out_color_matrix=bt709:out_range=tv`) và gắn nhãn `-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv`.
  - Thêm `-movflags +faststart`.
  - Ra file `08_render/video_silent.mp4`.
- **Bản xem nhanh:** `08_render/preview_voice.mp4` = video + `07_presentation/audio/voice.wav` (AAC). Chỉ để xem trên điện thoại; bản mix thật là việc của Tool 09.
- **Manifest** `08_render/manifest.json`: `build_hash` của 07, số khung, fps, kích thước, CRF, thời gian dựng.
- **Checklist `render` v3** (chủ dự án duyệt cùng thiết kế):
  - RND-A05 (thay RND-C01): số khung đếm bằng ffprobe = `timeline.total_frames`.
  - RND-A06 (mới): giải mã khung mốc của tờ kiểm 07 từ MP4, so với ảnh chụp lại cùng khung từ trang 07, PSNR ≥ 40 dB.
  - RND-A07 (mới): video dựng từ đúng bản 07 hiện tại (`build_hash` khớp).
  - Giữ C02 (màu, độ nét bằng mắt) và C03 (vỡ khối).
- **Artifacts cổng:** `08_render`, `07_presentation/presentation.json`.

## Để lại cho người xây
- Mã nguồn chụp dùng chung với `capture.mjs` khi hợp lý.
- Ngưỡng PSNR 40 dB đủ cho H.264 CRF 18. Thấp hơn nghĩa là sai khung hoặc sai màu.
