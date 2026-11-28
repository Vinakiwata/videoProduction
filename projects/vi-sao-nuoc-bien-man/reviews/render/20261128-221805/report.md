# Báo cáo kiểm duyệt — Render khung hình

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `render` · checklist "Kiểm duyệt render khung hình" v3
- **Bắt đầu:** 2026-11-28T22:18:05+07:00 · **Chốt:** 2026-11-28T22:18:55+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

9 mục: 9 đạt, 0 trượt, 0 lỗi kiểm tra, 0 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `08_render` | `dir:feb734fa1f9d` |
| `07_presentation/presentation.json` | `5d56f32f34fcef3e` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| RND-A01 | Cấu trúc | Có video render | Chặn | auto | ✅ Đạt | Có đủ: 08_render/video_silent.mp4 |
| RND-A02 | Kỹ thuật | Đúng khung của brief, 30 fps, H.264, yuv420p | Chặn | auto | ✅ Đạt | Đúng định dạng: 1080x1920 @ 30 fps, h264, yuv420p. |
| RND-A03 | Kỹ thuật | Không có khung đen ngoài ý muốn (> 0,2 giây) | Chặn | auto | ✅ Đạt | Không có đoạn đen > 0.2s (0 đoạn đen ngắn). |
| RND-A04 | Kỹ thuật | Không đứng hình quá 4 giây | Nghiêm trọng | auto | ✅ Đạt | Không có đoạn đứng hình > 4s. |
| RND-A05 | Đồng bộ | Số khung hình = tổng khung của timeline (không rớt, không thừa khung) | Chặn | auto | ✅ Đạt | Video có đúng 1602 khung = timeline (1602). |
| RND-A06 | Chất lượng hình | Khung mốc trong video giống trang trình chiếu 07 (PSNR độ sáng ≥ 40 dB) | Nghiêm trọng | auto | ✅ Đạt | 12 khung mốc giống trang 07: PSNR độ sáng thấp nhất 47.3 dB (khung 1128, S04-03-b), trung bình 49.8 dB ≥ 40 dB; PSNR màu 35.7–44.5 dB (giới hạn của yuv420p). |
| RND-A07 | Cấu trúc | Video dựng từ đúng bản trình chiếu hiện tại | Chặn | auto | ✅ Đạt | Video dựng từ đúng bản trình chiếu hiện tại (build_hash khớp). |
| RND-C02 | Chất lượng hình | Lấy mẫu khung tại mỗi đầu cảnh — giống ảnh chụp từ web trình chiếu | Nghiêm trọng | Claude | ✅ Đạt | Trích khung giữa 18 khung hình từ chính video_silent.mp4 (giải mã BT.709 chính xác) và ghép thành tờ, so với tờ khung mốc 07: bố cục, chữ, linh vật, màu nhận diện khớp (nền xanh đậm #0B3D91, màn kết #0078E0, chữ vàng #FFC907). Vùng phẳng sau khi mã hoá lệch ≤ 1 mức so với ảnh chụp trang (đã đo: (11,61,145) → (11,60,145)) nhờ đổi màu BT.709 chế độ chính xác; trước khi sửa lệch 1–2 mức. RND-A06: PSNR độ sáng 47,3–49,8 dB trên 12 khung mốc. Chữ hai dòng ngắt đúng storyboard sau khi sửa bộ dựng 07 (pre-line). Không banding thấy được ở nền tia sáng đáy biển. Chủ dự án xem bản có tiếng trên điện thoại ngày 28/11/2026: 'Nét, màu đúng'. Mép màu bão hoà (logo, chữ vàng trên xanh) nhoè nhẹ ở mức điểm ảnh — giới hạn vốn có của yuv420p mà nền tảng bắt buộc. |
| RND-C03 | Chất lượng hình | Bitrate đủ cao, không vỡ khối (blocking) ở cảnh chuyển động nhiều | Nghiêm trọng | Claude | ✅ Đạt | H.264 CRF 18, preset veryfast, 1080×1920, 30 fps, bitrate trung bình ≈ 1,3 Mbit/giây cho 53,4 giây (8,6 MB). Đã xem vùng cắt cỡ thật 540×540 ở cảnh mưa (khung 272, mưa rơi + giọt + phân tử, cảnh khó nén nhất vì hạt nhỏ chuyển động khắp khung) và bản đồ (khung 815, chấm muối chạy trên sông): mép giọt mưa, vệt mưa, sông, chấm trắng sắc nét, không vỡ khối, không bóng ma. Cảnh phẳng nên CRF 18 dư bitrate; Shorts/TikTok sẽ nén lại nhưng nguồn sạch giúp bản sau nén ít hỏng hơn. Chủ dự án xem trên điện thoại: không thấy nhoè hay vỡ khối. |
