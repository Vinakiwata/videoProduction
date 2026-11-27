# Báo cáo kiểm duyệt — Brief & bộ nhận diện

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `brief` · checklist "Kiểm duyệt brief" v3
- **Bắt đầu:** 2026-11-27T22:47:23+07:00 · **Chốt:** 2026-11-27T22:47:23+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

10 mục: 10 đạt, 0 trượt, 0 lỗi kiểm tra, 0 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `00_brief/brief.yaml` | `8e5456b287f34960` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| BRF-A01 | Cấu trúc | Brief đúng định dạng chuẩn | Chặn | auto | ✅ Đạt | 00_brief/brief.yaml khớp schema 'brief'. |
| BRF-A02 | Cấu trúc | Không còn trường bỏ trống (TODO) | Chặn | auto | ✅ Đạt | 00_brief/brief.yaml: không còn chỗ trống hay đánh dấu tạm. |
| BRF-A03 | Bộ nhận diện | Giọng đọc trong brand.voice là giọng có thật của VieNeu-TTS v3 Turbo | Chặn | auto | ✅ Đạt | Giọng 'Hải Đăng' có trong danh sách giọng dựng sẵn (vieneu_v3_turbo_voices.txt). |
| BRF-C01 | Mục tiêu | Mục tiêu đo được — sau khi xem, người xem biết/làm được gì | Chặn | Claude | ✅ Đạt | goal nêu kết quả cụ thể: người xem "giải thích lại được vì sao biển mặn còn sông thì không", kèm 3 mắt xích phải truyền đạt (mưa hoà tan khoáng chất trong đá → sông mang muối ra biển → nước bốc hơi, muối ở lại) và CTA. Dùng làm thước đo cho kịch bản và QC tổng được. |
| BRF-C02 | Khán giả | Khán giả cụ thể (độ tuổi/trình độ/bối cảnh xem) | Nghiêm trọng | Claude | ✅ Đạt | audience "Học sinh trung học và người lớn tò mò, xem trên điện thoại và máy tính": có trình độ, động cơ và thiết bị xem. Đủ để chọn từ vựng phổ thông và chữ lớn. |
| BRF-C03 | Định dạng | Định dạng khớp kênh (YouTube 16:9 → 1920×1080; Shorts → 1080×1920, ≤ 60 giây) | Chặn | Claude | ✅ Đạt | channel youtube, format 1920x1080 @ 30 fps (16:9), target_duration_s 60. Khớp video YouTube thường, không mâu thuẫn. |
| BRF-C04 | Bộ nhận diện | Bộ nhận diện đủ để giữ đồng bộ (màu, font có hỗ trợ tiếng Việt, giọng) | Nghiêm trọng | Claude | ✅ Đạt | Bộ nhận diện: 4 màu hex hợp lệ; font Be Vietnam Pro (thiết kế cho tiếng Việt, SIL OFL); giọng đổi thành "VieNeu-TTS v3 Turbo: Hải Đăng". Đã đối chiếu src/vieneu/assets/voices_v3_turbo.json: Hải Đăng là default_voice (Nam · Bắc · tự nhiên). Giọng cũ "Ngọc Lan" KHÔNG tồn tại trong v3 Turbo; lần duyệt trước ghi sai do dựa vào README cũ, nay đã có kiểm tra tự động BRF-A03 chặn lỗi này. Hải Đăng cũng là giọng chủ dự án đã dùng ở MeProduct. |
| BRF-C05 | Pháp lý | Đã khai báo có quảng cáo/tài trợ hay không | Nghiêm trọng | Claude | ✅ Đạt | is_advertising: false, được tạo với --no-ads. goal và cta không nhắc sản phẩm hay thương hiệu nào. |
| BRF-C06 | Khả thi | Thời lượng phù hợp khối lượng nội dung | Nhẹ | Claude | ✅ Đạt | 60 giây cho 3 mắt xích giải thích + móc + CTA, khoảng 180–200 âm tiết ở 3,2 âm tiết/giây. Mỗi ý chính có khoảng 15–20 giây, vừa sức. |
| BRF-C07 | Minh bạch | Mọi giả định tự đưa ra đều được ghi rõ và hợp lý | Nghiêm trọng | Claude | ✅ Đạt | assumptions giờ có 4 giả định: audience và thời lượng theo kênh; chủ đề do Claude chọn để chạy thử; dùng hồ sơ kênh mẫu chưa được xác nhận. Đối chiếu từng trường với hồ sơ kênh: tone, cta, brand, format trùng kênh; goal và title được truyền rõ khi tạo. Không còn lệch nào chưa ghi. Thêm: đổi giọng sang Hải Đăng theo yêu cầu dùng VieNeu "giống như MeProduct" và vì Ngọc Lan không tồn tại. |
