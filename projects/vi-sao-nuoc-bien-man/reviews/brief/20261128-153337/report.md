# Báo cáo kiểm duyệt — Brief & bộ nhận diện

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `brief` · checklist "Kiểm duyệt brief" v3
- **Bắt đầu:** 2026-11-28T15:33:37+07:00 · **Chốt:** 2026-11-28T15:33:37+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

10 mục: 10 đạt, 0 trượt, 0 lỗi kiểm tra, 0 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `00_brief/brief.yaml` | `88b8a58841c75400` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| BRF-A01 | Cấu trúc | Brief đúng định dạng chuẩn | Chặn | auto | ✅ Đạt | 00_brief/brief.yaml khớp schema 'brief'. |
| BRF-A02 | Cấu trúc | Không còn trường bỏ trống (TODO) | Chặn | auto | ✅ Đạt | 00_brief/brief.yaml: không còn chỗ trống hay đánh dấu tạm. |
| BRF-A03 | Bộ nhận diện | Giọng đọc trong brand.voice là giọng có thật của VieNeu-TTS v3 Turbo | Chặn | auto | ✅ Đạt | Giọng 'Hải Đăng' có trong danh sách giọng dựng sẵn (vieneu_v3_turbo_voices.txt). |
| BRF-C01 | Mục tiêu | Mục tiêu đo được — sau khi xem, người xem biết/làm được gì | Chặn | Claude | ✅ Đạt | goal: "Sau khoảng 50 giây, người xem giải thích lại được vì sao biển mặn còn sông thì không (mưa hoà tan khoáng chất trong đá, sông mang muối ra biển, nước bốc hơi còn muối ở lại)…" — kết quả cụ thể, đo được ở kịch bản và QC tổng. |
| BRF-C02 | Khán giả | Khán giả cụ thể (độ tuổi/trình độ/bối cảnh xem) | Nghiêm trọng | Claude | ✅ Đạt | audience "Học sinh trung học và người lớn tò mò, xem trên điện thoại và máy tính": có trình độ, động cơ và thiết bị xem. Đủ để chọn từ vựng phổ thông và chữ lớn. |
| BRF-C03 | Định dạng | Định dạng khớp kênh (YouTube 16:9 → 1920×1080; Shorts → 1080×1920, ≤ 60 giây) | Chặn | Claude | ✅ Đạt | channel youtube, 1920x1080 @30 fps (16:9), target_duration_s 50 — khớp video YouTube thường. |
| BRF-C04 | Bộ nhận diện | Bộ nhận diện đủ để giữ đồng bộ (màu, font có hỗ trợ tiếng Việt, giọng) | Nghiêm trọng | Claude | ✅ Đạt | Bộ nhận diện Khỉ Khám Phá (channels/khi-kham-pha, chủ dự án cung cấp 28/11/2026):<br>- 6 màu cho chữ, icon, nút: xanh dương #0078E0, vàng #FFC907, trắng, nâu gỗ #5E270E, cam #FD8305, xanh lá #669F2D. Năm màu lấy mẫu trực tiếp từ ảnh bộ nhận diện.<br>- Thêm xanh đậm #0B3D91 làm nền khung giải thích; chủ dự án chọn sau khi xem so sánh với nền nâu gỗ (28/11/2026). Đã đo: trắng trên xanh dương #0078E0 chỉ 4,41:1, nên mọi chữ đặt trên tấm nền xanh đậm; vàng #FFC907 trên #0B3D91 đạt 6,51:1, trắng 10,04:1 (đã đo bằng contrast_ratio).<br>- 20 màu cảnh tự nhiên giữ nguyên.<br>- Khẩu hiệu: 'Khám phá thế giới · Học hỏi mỗi ngày · Cùng Khỉ nhé!'.<br>- Logo tròn và 7 biểu cảm Khỉ dạng PNG nền trong suốt, mỗi biểu cảm ghi rõ khi nào dùng (brand.mascot).<br>- Font Be Vietnam Pro (SIL OFL, thiết kế cho tiếng Việt); giọng VieNeu-TTS v3 Turbo: Hải Đăng (BRF-A03 đạt).<br>- brand trong brief trùng khớp channel.yaml. Đã ghi giới hạn: ảnh linh vật gốc chỉ 150–200 px. |
| BRF-C05 | Pháp lý | Đã khai báo có quảng cáo/tài trợ hay không | Nghiêm trọng | Claude | ✅ Đạt | is_advertising: false, được tạo với --no-ads. goal và cta không nhắc sản phẩm hay thương hiệu nào. |
| BRF-C06 | Khả thi | Thời lượng phù hợp khối lượng nội dung | Nhẹ | Claude | ✅ Đạt | 50 giây ở tốc độ giọng Hải Đăng đo thật 4,43 âm tiết/giây ≈ 200 âm tiết cho 3 mắt xích + móc + CTA (kịch bản hiện có 199 âm tiết lời) — vừa khối lượng, không phải cắt ý. |
| BRF-C07 | Minh bạch | Mọi giả định tự đưa ra đều được ghi rõ và hợp lý | Nghiêm trọng | Claude | ✅ Đạt | assumptions có 8 mục (thêm: 28/11 chọn nền xanh đậm #0B3D91 thay nâu gỗ), đều khớp hồ sơ kênh:<br>- audience và thời lượng lấy theo kênh.<br>- Chủ đề chạy thử do Claude chọn.<br>- Dùng kênh khi-kham-pha thay cho kênh mẫu.<br>- 27/11: giữ tốc độ đọc gốc, nên mục tiêu 50 giây.<br>- 28/11: cảnh chân thật, màu tự nhiên.<br>- 28/11: đổi hẳn sang Khỉ Khám Phá; Khỉ phản ứng ở điểm nhấn và có mặt ở cảnh kết; không logo góc, không intro.<br>cta đổi theo kênh mới: 'cùng Khỉ khám phá'. Lời đọc giữ nguyên 'cùng mình khám phá', vẫn đúng ý vì người dẫn là Khỉ. constraints thêm việc gắn nhãn AI cho hình linh vật. Không còn lệch nào chưa ghi. |
