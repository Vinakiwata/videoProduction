# Báo cáo kiểm duyệt — Brief & bộ nhận diện

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `brief` · checklist "Kiểm duyệt brief" v4
- **Bắt đầu:** 2026-11-28T17:39:26+07:00 · **Chốt:** 2026-11-28T17:39:26+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

12 mục: 12 đạt, 0 trượt, 0 lỗi kiểm tra, 0 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `00_brief/brief.yaml` | `265ae6ddce217881` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| BRF-A01 | Cấu trúc | Brief đúng định dạng chuẩn | Chặn | auto | ✅ Đạt | 00_brief/brief.yaml khớp schema 'brief'. |
| BRF-A02 | Cấu trúc | Không còn trường bỏ trống (TODO) | Chặn | auto | ✅ Đạt | 00_brief/brief.yaml: không còn chỗ trống hay đánh dấu tạm. |
| BRF-A03 | Bộ nhận diện | Giọng đọc trong brand.voice là giọng có thật của VieNeu-TTS v3 Turbo | Chặn | auto | ✅ Đạt | Giọng 'Xuân Vĩnh' có trong danh sách giọng dựng sẵn (vieneu_v3_turbo_voices.txt). |
| BRF-A04 | Nền tảng | Nền tảng có hồ sơ, cùng khung, brief.format trùng khung đó, thời lượng ≤ giới hạn của từng nền tảng | Chặn | auto | ✅ Đạt | YouTube Shorts, TikTok, Instagram/Facebook Reels: cùng khung 1080×1920@30, 50 giây trong giới hạn; lề an toàn trên 220 · dưới 461 · trái 65 · phải 173 px. |
| BRF-A05 | Nền tảng | Số đo vùng an toàn của các nền tảng đối chiếu trong vòng 180 ngày (cảnh báo) | Nhẹ | auto | ✅ Đạt | Số đo vùng an toàn còn mới: YouTube Shorts 2026-11-28, TikTok 2026-11-28, Instagram/Facebook Reels 2026-11-28 |
| BRF-C01 | Mục tiêu | Mục tiêu đo được — sau khi xem, người xem biết/làm được gì | Chặn | Claude | ✅ Đạt | goal: "Sau khoảng 50 giây, người xem giải thích lại được vì sao biển mặn còn sông thì không (mưa hoà tan khoáng chất trong đá, sông mang muối ra biển, nước bốc hơi còn muối ở lại)…" — kết quả cụ thể, đo được ở kịch bản và QC tổng. |
| BRF-C02 | Khán giả | Khán giả cụ thể (độ tuổi/trình độ/bối cảnh xem) | Nghiêm trọng | Claude | ✅ Đạt | audience "Học sinh trung học và người lớn tò mò, xem trên điện thoại và máy tính": có trình độ, động cơ và thiết bị xem. Đủ để chọn từ vựng phổ thông và chữ lớn. |
| BRF-C03 | Định dạng | Định dạng khớp kênh (YouTube 16:9 → 1920×1080; Shorts → 1080×1920, ≤ 60 giây) | Chặn | Claude | ✅ Đạt | channel youtube, 1920x1080 @30 fps (16:9), target_duration_s 50 — khớp video YouTube thường. |
| BRF-C04 | Bộ nhận diện | Bộ nhận diện đủ để giữ đồng bộ (màu, font có hỗ trợ tiếng Việt, giọng) | Nghiêm trọng | Claude | ✅ Đạt | channel youtube_shorts, khung dọc 1080×1920 @30 fps (9:16), platforms youtube_shorts + tiktok + reels (chủ dự án chọn 28/11/2026), target_duration_s 50 — trong giới hạn kênh 60 giây và giới hạn từng nền tảng (Shorts 180, TikTok 600, Reels 180); BRF-A04 đo tự động: cùng khung, lề an toàn trên 220 · dưới 461 · trái 65 · phải 173 px. Khớp hồ sơ kênh Khỉ Khám Phá đã chuyển sang dọc. |
| BRF-C05 | Pháp lý | Đã khai báo có quảng cáo/tài trợ hay không | Nghiêm trọng | Claude | ✅ Đạt | is_advertising: false, được tạo với --no-ads. goal và cta không nhắc sản phẩm hay thương hiệu nào. |
| BRF-C06 | Khả thi | Thời lượng phù hợp khối lượng nội dung | Nhẹ | Claude | ✅ Đạt | 50 giây ở tốc độ giọng Hải Đăng đo thật 4,43 âm tiết/giây ≈ 200 âm tiết cho 3 mắt xích + móc + CTA (kịch bản hiện có 199 âm tiết lời) — vừa khối lượng, không phải cắt ý. |
| BRF-C07 | Minh bạch | Mọi giả định tự đưa ra đều được ghi rõ và hợp lý | Nghiêm trọng | Claude | ✅ Đạt | assumptions có 10 mục (thêm 28/11: bớt dí dỏm, lời văn nghiêm túc vừa phải, chủ dự án đã duyệt bản nháp; tone đổi thành thân thiện, rõ ràng, nghiêm túc vừa phải, không tiếng lóng) (thêm 28/11: giọng Xuân Vĩnh +2,5 nửa cung, kịch bản dí dỏm do chủ dự án duyệt; tone và cta đổi theo kênh) (thêm: 28/11 chọn nền xanh đậm #0B3D91 thay nâu gỗ), đều khớp hồ sơ kênh:<br>- audience và thời lượng lấy theo kênh.<br>- Chủ đề chạy thử do Claude chọn.<br>- Dùng kênh khi-kham-pha thay cho kênh mẫu.<br>- 27/11: giữ tốc độ đọc gốc, nên mục tiêu 50 giây.<br>- 28/11: cảnh chân thật, màu tự nhiên.<br>- 28/11: đổi hẳn sang Khỉ Khám Phá; Khỉ phản ứng ở điểm nhấn và có mặt ở cảnh kết; không logo góc, không intro.<br>cta đổi theo kênh mới: 'cùng Khỉ khám phá'. Lời đọc giữ nguyên 'cùng mình khám phá', vẫn đúng ý vì người dẫn là Khỉ. constraints thêm việc gắn nhãn AI cho hình linh vật. Không còn lệch nào chưa ghi. |
