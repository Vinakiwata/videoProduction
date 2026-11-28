---
name: vp-render
description: Dùng khi cần render, render lại hoặc duyệt video khung hình (08_render) cho video trong repo này — chụp trang trình chiếu 07 đã duyệt từng khung thành video_silent.mp4 và bản xem nhanh có giọng.
---

# Render khung hình (08_render)

Trang trình chiếu 07 là bộ dựng duy nhất. Tool 08 chỉ chụp lại đúng trang đó, không vẽ thêm gì.
Thiết kế: `docs/superpowers/specs/2026-11-28-tool-render-design.md`.

1. `python -m vp gate projects/<dự án> presentation` phải báo MỞ.
2. `python -m vp render build projects/<dự án>` (dự án mẫu 1602 khung dọc mất khoảng 3 phút trên máy 2 lõi). Kết quả:
   - `08_render/video_silent.mp4`: H.264 CRF 18, yuv420p, màu BT.709 (đổi màu chế độ chính xác `accurate_rnd+full_chroma_int`), fps và khung theo `presentation.json`;
   - `08_render/preview_voice.mp4`: video + `07_presentation/audio/voice.wav`, chỉ để xem nhanh; bản đăng do Tool 09 mix;
   - `08_render/manifest.json`: `build_hash` của 07, số khung, thời gian dựng.
   Trang có lỗi JS giữa chừng thì dừng và xoá file dở.
3. `python -m vp render lint projects/<dự án>` phải báo SẠCH:
   - RND-A05: số khung = timeline;
   - RND-A06: PSNR độ sáng ≥ 40 dB so với trang 07. Không dùng PSNR màu: yuv420p giữ màu ở 1/4 độ phân giải, nên mã hoá không mất dữ liệu cũng chỉ đạt ~36 dB màu ở chỗ nhiều chi tiết;
   - RND-A07: video dựng từ đúng bản 07 hiện tại. Dựng lại 07 thì phải render lại.
4. Tự xem:
   - trích khung giữa mỗi khung hình từ MP4 (giải mã `in_color_matrix=bt709`);
   - vùng cắt cỡ thật ở cảnh nhiều hạt chuyển động (mưa, chấm muối) để soi vỡ khối;
   - chữ hai dòng ngắt đúng storyboard.
5. Gửi `preview_voice.mp4` cho chủ dự án xem trên điện thoại. Chép sang máy họ qua file đã gửi (`fileUuid`), rồi so mã băm **luồng** (`ffmpeg -map 0:v -c copy -f streamhash`), không so cả file, vì đường truyền có thể đóng gói lại MP4. Chỉ ghi vào `~/Documents/DEV_WORK_SUB/VieNeu-TTS/`.
6. Duyệt bằng `vp-kiem-duyet`, công đoạn `render`.
