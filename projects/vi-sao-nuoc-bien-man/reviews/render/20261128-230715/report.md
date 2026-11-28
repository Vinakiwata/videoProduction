# Báo cáo kiểm duyệt — Render khung hình

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `render` · checklist "Kiểm duyệt render khung hình" v3
- **Bắt đầu:** 2026-11-28T23:07:15+07:00 · **Chốt:** 2026-11-28T23:07:52+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

9 mục: 9 đạt, 0 trượt, 0 lỗi kiểm tra, 0 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `08_render` | `dir:cdc4f19467ff` |
| `07_presentation/presentation.json` | `d80df0c5e17de51d` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| RND-A01 | Cấu trúc | Có video render | Chặn | auto | ✅ Đạt | Có đủ: 08_render/video_silent.mp4 |
| RND-A02 | Kỹ thuật | Đúng khung của brief, 30 fps, H.264, yuv420p | Chặn | auto | ✅ Đạt | Đúng định dạng: 1080x1920 @ 30 fps, h264, yuv420p. |
| RND-A03 | Kỹ thuật | Không có khung đen ngoài ý muốn (> 0,2 giây) | Chặn | auto | ✅ Đạt | Không có đoạn đen > 0.2s (0 đoạn đen ngắn). |
| RND-A04 | Kỹ thuật | Không đứng hình quá 4 giây | Nghiêm trọng | auto | ✅ Đạt | Không có đoạn đứng hình > 4s. |
| RND-A05 | Đồng bộ | Số khung hình = tổng khung của timeline (không rớt, không thừa khung) | Chặn | auto | ✅ Đạt | Video có đúng 1626 khung = timeline (1626). |
| RND-A06 | Chất lượng hình | Khung mốc trong video giống trang trình chiếu 07 (PSNR độ sáng ≥ 40 dB) | Nghiêm trọng | auto | ✅ Đạt | 12 khung mốc giống trang 07: PSNR độ sáng thấp nhất 47.0 dB (khung 1577, S05-02-a), trung bình 50.2 dB ≥ 40 dB; PSNR màu 35.7–46.7 dB (giới hạn của yuv420p). |
| RND-A07 | Cấu trúc | Video dựng từ đúng bản trình chiếu hiện tại | Chặn | auto | ✅ Đạt | Video dựng từ đúng bản trình chiếu hiện tại (build_hash khớp). |
| RND-C02 | Chất lượng hình | Lấy mẫu khung tại mỗi đầu cảnh — giống ảnh chụp từ web trình chiếu | Nghiêm trọng | Claude | ✅ Đạt | Trích khung giữa 19 khung hình từ chính video_silent.mp4 (giải mã BT.709 chính xác), so với tờ khung mốc 07: bố cục, chữ, linh vật, màu nhận diện khớp. Khung 0 là ảnh bìa 1 giây (bãi biển thật + câu hỏi 'Vì sao nước biển lại mặn?' + Khỉ thắc mắc), xuất riêng thumbnail.png 1080×1920 từ khung 0. Màn kết: logo + 'Cảm ơn bạn đã xem!' + nút ĐĂNG KÝ, lời đọc kêu gọi mới. RND-A06: 12 khung mốc, PSNR độ sáng thấp nhất 47,0 dB (khung 1577, S05-02-a), trung bình 50,2 dB ≥ 40 dB; PSNR màu 35,7–46,7 dB (giới hạn của yuv420p). Chữ hai dòng ngắt đúng storyboard. Chủ dự án xem bản v2 có tiếng trên điện thoại ngày 28/11/2026: 'Nét, màu đúng'. Mép màu bão hoà nhoè nhẹ ở mức điểm ảnh — giới hạn vốn có của yuv420p mà nền tảng bắt buộc. |
| RND-C03 | Chất lượng hình | Bitrate đủ cao, không vỡ khối (blocking) ở cảnh chuyển động nhiều | Nghiêm trọng | Claude | ✅ Đạt | H.264 CRF 18, preset veryfast, 1080×1920, 30 fps, 1626 khung = 54,2 giây, bitrate trung bình ≈ 1,29 Mbit/giây (8,7 MB). Đã xem vùng cắt cỡ thật 540×540 ở cảnh mưa (khung 302, mưa rơi + giọt, cảnh khó nén nhất): mép giọt, vệt mưa sắc nét, không vỡ khối, không bóng ma. Cảnh phẳng nên CRF 18 dư bitrate; nguồn sạch giúp bản nền tảng nén lại ít hỏng hơn. Chủ dự án xem trên điện thoại: nét, không vỡ khối. |
