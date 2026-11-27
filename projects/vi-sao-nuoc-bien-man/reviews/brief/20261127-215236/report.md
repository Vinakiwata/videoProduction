# Báo cáo kiểm duyệt — Brief & bộ nhận diện

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `brief` · checklist "Kiểm duyệt brief" v2
- **Bắt đầu:** 2026-11-27T21:52:36+07:00 · **Chốt:** 2026-11-27T21:52:49+07:00

## Kết luận: ❌ KHÔNG ĐẠT — điểm chất lượng 91/100

9 mục: 8 đạt, 1 trượt, 0 lỗi kiểm tra, 0 không áp dụng.

## ❗ Phải sửa trước khi đi tiếp

### BRF-C07 · [Nghiêm trọng] Mọi giả định tự đưa ra đều được ghi rõ và hợp lý
- **Hiện trạng:** assumptions ghi 2 giả định (audience, thời lượng lấy theo kênh), cả hai hợp lý. Nhưng thiếu giả định lớn nhất: chủ đề "Vì sao nước biển lại mặn?" do Claude tự chọn để chạy thử dây chuyền, chủ dự án chưa yêu cầu. Ngoài ra kênh kenh-khoa-hoc-mau là hồ sơ kênh mẫu chưa được chủ dự án xác nhận.
- **Cách sửa:** Thêm vào assumptions: (1) "Chủ đề do Claude chọn để chạy thử Tool 0–1; chủ dự án chưa yêu cầu video này"; (2) "Dùng hồ sơ kênh mẫu kenh-khoa-hoc-mau, bộ nhận diện chưa được chủ dự án xác nhận".

## File đã niêm phong

| File | Mã băm |
|---|---|
| `00_brief/brief.yaml` | `1dbb2895b267006a` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| BRF-A01 | Cấu trúc | Brief đúng định dạng chuẩn | Chặn | auto | ✅ Đạt | 00_brief/brief.yaml khớp schema 'brief'. |
| BRF-A02 | Cấu trúc | Không còn trường bỏ trống (TODO) | Chặn | auto | ✅ Đạt | 00_brief/brief.yaml: không còn chỗ trống hay đánh dấu tạm. |
| BRF-C01 | Mục tiêu | Mục tiêu đo được — sau khi xem, người xem biết/làm được gì | Chặn | Claude | ✅ Đạt | goal nêu kết quả cụ thể: người xem "giải thích lại được vì sao biển mặn còn sông thì không", kèm 3 mắt xích phải truyền đạt (mưa hoà tan khoáng chất trong đá → sông mang muối ra biển → nước bốc hơi, muối ở lại) và CTA. Dùng làm thước đo cho kịch bản và QC tổng được. |
| BRF-C02 | Khán giả | Khán giả cụ thể (độ tuổi/trình độ/bối cảnh xem) | Nghiêm trọng | Claude | ✅ Đạt | audience "Học sinh trung học và người lớn tò mò, xem trên điện thoại và máy tính": có trình độ, động cơ và thiết bị xem. Đủ để chọn từ vựng phổ thông và chữ lớn. |
| BRF-C03 | Định dạng | Định dạng khớp kênh (YouTube 16:9 → 1920×1080; Shorts → 1080×1920, ≤ 60 giây) | Chặn | Claude | ✅ Đạt | channel youtube, format 1920x1080 @ 30 fps (16:9), target_duration_s 60. Khớp video YouTube thường, không mâu thuẫn. |
| BRF-C04 | Bộ nhận diện | Bộ nhận diện đủ để giữ đồng bộ (màu, font có hỗ trợ tiếng Việt, giọng) | Nghiêm trọng | Claude | ✅ Đạt | Bộ nhận diện lấy từ hồ sơ kênh kenh-khoa-hoc-mau: 4 màu hex hợp lệ; font Be Vietnam Pro (thiết kế cho tiếng Việt, giấy phép SIL OFL); giọng "VieNeu-TTS v3 Turbo: Ngọc Lan" là giọng có sẵn. Có thêm phong cách hình (flat, tối đa 4 màu mỗi khung). |
| BRF-C05 | Pháp lý | Đã khai báo có quảng cáo/tài trợ hay không | Nghiêm trọng | Claude | ✅ Đạt | is_advertising: false, được tạo với --no-ads. goal và cta không nhắc sản phẩm hay thương hiệu nào. |
| BRF-C06 | Khả thi | Thời lượng phù hợp khối lượng nội dung | Nhẹ | Claude | ✅ Đạt | 60 giây cho 3 mắt xích giải thích + móc + CTA, khoảng 180–200 âm tiết ở 3,2 âm tiết/giây. Mỗi ý chính có khoảng 15–20 giây, vừa sức. |
| BRF-C07 | Minh bạch | Mọi giả định tự đưa ra đều được ghi rõ và hợp lý | Nghiêm trọng | Claude | ❌ Trượt | assumptions ghi 2 giả định (audience, thời lượng lấy theo kênh), cả hai hợp lý. Nhưng thiếu giả định lớn nhất: chủ đề "Vì sao nước biển lại mặn?" do Claude tự chọn để chạy thử dây chuyền, chủ dự án chưa yêu cầu. Ngoài ra kênh kenh-khoa-hoc-mau là hồ sơ kênh mẫu chưa được chủ dự án xác nhận. |
