# Báo cáo kiểm duyệt — Brief & bộ nhận diện

- **Dự án:** vi-du-bau-troi-xanh
- **Công đoạn:** `brief` · checklist "Kiểm duyệt brief" v1
- **Bắt đầu:** 2026-11-27T21:31:22+07:00 · **Chốt:** 2026-11-27T21:31:36+07:00

## Kết luận: ❌ KHÔNG ĐẠT — điểm chất lượng 80/100

7 mục: 6 đạt, 1 trượt, 0 lỗi kiểm tra, 0 không áp dụng.

## ❗ Phải sửa trước khi đi tiếp

### BRF-C01 · [Chặn] Mục tiêu đo được — sau khi xem, người xem biết/làm được gì
- **Hiện trạng:** goal = "Giải thích một hiện tượng khoa học trong 30 giây, người xem hiểu và muốn xem tiếp kênh". Chưa nói người xem hiểu ĐIỀU GÌ, nên không dùng làm thước đo cho kịch bản được ("một hiện tượng khoa học" là chung chung, chỉ có tiêu đề nêu hiện tượng).
- **Cách sửa:** Viết lại goal thành kết quả cụ thể, ví dụ: "Sau 30 giây, người xem giải thích lại được bằng một câu: ánh sáng xanh có bước sóng ngắn nên bị không khí tán xạ mạnh hơn, lan khắp bầu trời; và muốn xem tiếp kênh."

## File đã niêm phong

| File | Mã băm |
|---|---|
| `00_brief/brief.yaml` | `e20c7e92aec6dac8` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| BRF-A01 | Cấu trúc | Brief đúng định dạng chuẩn | Chặn | auto | ✅ Đạt | 00_brief/brief.yaml khớp schema 'brief'. |
| BRF-C01 | Mục tiêu | Mục tiêu đo được — sau khi xem, người xem biết/làm được gì | Chặn | Claude | ❌ Trượt | goal = "Giải thích một hiện tượng khoa học trong 30 giây, người xem hiểu và muốn xem tiếp kênh". Chưa nói người xem hiểu ĐIỀU GÌ, nên không dùng làm thước đo cho kịch bản được ("một hiện tượng khoa học" là chung chung, chỉ có tiêu đề nêu hiện tượng). |
| BRF-C02 | Khán giả | Khán giả cụ thể (độ tuổi/trình độ/bối cảnh xem) | Nghiêm trọng | Claude | ✅ Đạt | audience = "Học sinh trung học và người lớn tò mò, xem trên điện thoại và máy tính": có trình độ (trung học), động cơ (tò mò) và bối cảnh xem (điện thoại/máy tính), đủ để chọn từ vựng phổ thông và chữ lớn. |
| BRF-C03 | Định dạng | Định dạng khớp kênh (YouTube 16:9 → 1920×1080; Shorts → 1080×1920, ≤ 60 giây) | Chặn | Claude | ✅ Đạt | channel = youtube, format = 1920x1080 @ 30 fps (16:9), target_duration_s = 30. Không mâu thuẫn; 30 giây là video ngắn trên kênh YouTube thường, hợp lệ. |
| BRF-C04 | Bộ nhận diện | Bộ nhận diện đủ để giữ đồng bộ (màu, font có hỗ trợ tiếng Việt, giọng) | Nghiêm trọng | Claude | ✅ Đạt | colors: 3 mã hex hợp lệ (#0B3D91, #FFD23F, #FFFFFF, tương phản xanh đậm/trắng cao). Font Be Vietnam Pro được thiết kế cho tiếng Việt, giấy phép SIL OFL cho dùng thương mại. Giọng "Ngọc Lan" là giọng mặc định có sẵn của VieNeu-TTS v3 Turbo (examples/main_v3turbo.py). |
| BRF-C05 | Pháp lý | Đã khai báo có quảng cáo/tài trợ hay không | Nghiêm trọng | Claude | ✅ Đạt | is_advertising: false. Kiểm tra goal, cta, constraints: không nhắc sản phẩm hay thương hiệu nào; CTA chỉ là đăng ký kênh. |
| BRF-C06 | Khả thi | Thời lượng phù hợp khối lượng nội dung | Nhẹ | Claude | ✅ Đạt | 30 giây cho đúng một ý chính (tán xạ Rayleigh), tương đương khoảng 75–100 âm tiết lời đọc. Vừa sức, không tham. |
