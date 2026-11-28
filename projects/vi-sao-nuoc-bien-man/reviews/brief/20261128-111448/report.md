# Báo cáo kiểm duyệt — Brief & bộ nhận diện

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `brief` · checklist "Kiểm duyệt brief" v3
- **Bắt đầu:** 2026-11-28T11:14:48+07:00 · **Chốt:** 2026-11-28T11:15:01+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

10 mục: 10 đạt, 0 trượt, 0 lỗi kiểm tra, 0 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `00_brief/brief.yaml` | `fdff86d4b94ad0f0` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| BRF-A01 | Cấu trúc | Brief đúng định dạng chuẩn | Chặn | auto | ✅ Đạt | 00_brief/brief.yaml khớp schema 'brief'. |
| BRF-A02 | Cấu trúc | Không còn trường bỏ trống (TODO) | Chặn | auto | ✅ Đạt | 00_brief/brief.yaml: không còn chỗ trống hay đánh dấu tạm. |
| BRF-A03 | Bộ nhận diện | Giọng đọc trong brand.voice là giọng có thật của VieNeu-TTS v3 Turbo | Chặn | auto | ✅ Đạt | Giọng 'Hải Đăng' có trong danh sách giọng dựng sẵn (vieneu_v3_turbo_voices.txt). |
| BRF-C01 | Mục tiêu | Mục tiêu đo được — sau khi xem, người xem biết/làm được gì | Chặn | Claude | ✅ Đạt | goal: "Sau khoảng 50 giây, người xem giải thích lại được vì sao biển mặn còn sông thì không (mưa hoà tan khoáng chất trong đá, sông mang muối ra biển, nước bốc hơi còn muối ở lại)…" — kết quả cụ thể, đo được ở kịch bản và QC tổng. |
| BRF-C02 | Khán giả | Khán giả cụ thể (độ tuổi/trình độ/bối cảnh xem) | Nghiêm trọng | Claude | ✅ Đạt | audience "Học sinh trung học và người lớn tò mò, xem trên điện thoại và máy tính": có trình độ, động cơ và thiết bị xem. Đủ để chọn từ vựng phổ thông và chữ lớn. |
| BRF-C03 | Định dạng | Định dạng khớp kênh (YouTube 16:9 → 1920×1080; Shorts → 1080×1920, ≤ 60 giây) | Chặn | Claude | ✅ Đạt | channel youtube, 1920x1080 @30 fps (16:9), target_duration_s 50 — khớp video YouTube thường. |
| BRF-C04 | Bộ nhận diện | Bộ nhận diện đủ để giữ đồng bộ (màu, font có hỗ trợ tiếng Việt, giọng) | Nghiêm trọng | Claude | ✅ Đạt | Bộ nhận diện: 4 màu nhận diện hex hợp lệ cho chữ, icon và nút; thêm brand.scene_colors gồm 20 màu tự nhiên cho cảnh minh hoạ (trời #4A98D6, trời mưa #6F879E, núi, đồi, cây, đất, sông, biển 3 mức, cát 2 mức, đá 3 mức, dung nham) theo quyết định của chủ dự án ngày 28/11/2026. Đã đo: hình trắng trên trời #4A98D6 đạt 3,11:1, trên trời mưa 3,73:1 (≥ 3:1 cho đồ hoạ). style mô tả rõ luật mới. Font Be Vietnam Pro (thiết kế cho tiếng Việt, SIL OFL); giọng VieNeu-TTS v3 Turbo: Hải Đăng (BRF-A03 đã kiểm có thật). Đồng bộ với channels/kenh-khoa-hoc-mau/channel.yaml. |
| BRF-C05 | Pháp lý | Đã khai báo có quảng cáo/tài trợ hay không | Nghiêm trọng | Claude | ✅ Đạt | is_advertising: false, được tạo với --no-ads. goal và cta không nhắc sản phẩm hay thương hiệu nào. |
| BRF-C06 | Khả thi | Thời lượng phù hợp khối lượng nội dung | Nhẹ | Claude | ✅ Đạt | 50 giây ở tốc độ giọng Hải Đăng đo thật 4,43 âm tiết/giây ≈ 200 âm tiết cho 3 mắt xích + móc + CTA (kịch bản hiện có 199 âm tiết lời) — vừa khối lượng, không phải cắt ý. |
| BRF-C07 | Minh bạch | Mọi giả định tự đưa ra đều được ghi rõ và hợp lý | Nghiêm trọng | Claude | ✅ Đạt | assumptions có 6 mục, đã đối chiếu với hồ sơ kênh: audience và thời lượng lấy theo kênh; chủ đề do Claude chọn để chạy thử; dùng hồ sơ kênh mẫu chưa xác nhận; quyết định 27/11 giữ tốc độ gốc nên mục tiêu hạ 60 → 50 giây; và mục mới, quyết định 28/11 cảnh minh hoạ phải chân thật, dùng màu tự nhiên (sông có núi, cây, dòng sông uốn lượn; biển là bãi biển), icon, chữ, nút giữ 4 màu. brand trong brief trùng khớp channel.yaml, kể cả scene_colors. Không còn lệch nào chưa ghi. |
