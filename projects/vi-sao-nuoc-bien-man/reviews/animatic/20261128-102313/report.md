# Báo cáo kiểm duyệt — Animatic (bản nháp thô)

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `animatic` · checklist "Kiểm duyệt animatic (bản nháp thô)" v2
- **Bắt đầu:** 2026-11-28T10:23:13+07:00 · **Chốt:** 2026-11-28T10:23:13+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 97/100

11 mục: 9 đạt, 1 trượt, 0 lỗi kiểm tra, 1 không áp dụng.

## Nên cải thiện (không chặn cổng)

- **ATC-C06 Nguồn thời lượng được biết rõ — giọng nháp thật, hoặc ghi nhận rủi ro của ước tính:** timeline nguồn: 10/10 đoạn giọng là estimate (4,43 âm tiết/giây, đã hiệu chỉnh từ giọng Hải Đăng thật). Có giọng theo câu với khoảng ngắt 0,35/0,45 giây, nên thời lượng thật sẽ dài hơn ước tính ở các đoạn nhiều câu (S01-01, S03-02, S04-01). → Sau khi chạy voice synth: "python -m vp voice to-animatic", dựng lại animatic và duyệt lại cổng này với giọng thật; chủ dự án nghe để chấm ATC-C03.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `03_animatic` | `dir:d1213563c7fa` |
| `02_design/storyboard.yaml` | `82024fb70d2f43cf` |
| `01_script/script.yaml` | `f1e243f1430c98b5` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| ATC-A01 | Cấu trúc | Có animatic và bảng thời gian | Chặn | auto | ✅ Đạt | Có đủ: 03_animatic/animatic.mp4, 03_animatic/timing.yaml, 03_animatic/manifest.json |
| ATC-A02 | Kỹ thuật | Animatic có cả hình và tiếng, thời lượng khớp nhau | Nghiêm trọng | auto | ✅ Đạt | Hình 48.667s, tiếng 48.661s, lệch 0.006s (tối đa 0.2s). |
| ATC-A03 | Kỹ thuật | Định dạng nháp 960×636 @ 15 fps (hình 960×540 + dải phụ đề riêng) | Nhẹ | auto | ✅ Đạt | Đúng định dạng: 960x636 @ 15 fps, h264, yuv420p. |
| ATC-A04 | Đồng bộ | Animatic dựng từ đúng kịch bản, storyboard, giọng nháp hiện tại | Chặn | auto | ✅ Đạt | Animatic khớp đầu vào hiện tại (nguồn lời: estimate, 15 fps). |
| ATC-A05 | Đồng bộ | Thời lượng video khớp bảng thời gian (±1 khung) | Chặn | auto | ✅ Đạt | Video 48.667s, timing 48.700s, lệch 0.033s (tối đa 0.07s). |
| ATC-C01 | Nhịp | Nhịp tổng thể không chậm, không dồn | Chặn | Claude | ✅ Đạt | Trích 49 khung (1/giây), đối chiếu timing.yaml (48,7 giây, ước tính theo tốc độ đã hiệu chỉnh 4,43 âm tiết/giây). Không có khoảng > 4 giây không đổi hình. Khoảng dài nhất là S04-04-a, từ 00:35,6 (chữ "Nguồn thêm") tới 00:39,0 (khoáng chất bay lên), ≈ 3,4 giây, có camera zoom_in và núi lửa nhấp nháy. Không có cụm dồn dập: S05-01 hiện 3 biểu tượng cách nhau khoảng 1,2–1,6 giây. |
| ATC-C02 | Truyền đạt | Chỉ nhìn hình (bỏ phụ đề, tắt tiếng) vẫn hiểu được mạch chính | Nghiêm trọng | Claude | ✅ Đạt | Che dải phụ đề vẫn đọc được mạch: sông ra biển → 2 cốc + "Sông ngọt → Biển mặn?" → giọt mưa "axit nhẹ" → đá, hạt bong ra "muối" → suối thành sông, kính lúp "rất ít muối" → mưa xuống sông "nước ngọt mới" → bản đồ "Muối dồn về biển" → mặt trời, hơi nước "Nước bay đi, muối ở lại" → vòng tuần hoàn "hàng triệu năm" → đáy biển "Nguồn thêm" → Mưa → Sông → Bốc hơi → nút đăng ký "Mỗi tuần một hiện tượng". Đây là wireframe; hình thật ở Tool 06 phải giữ đúng chuỗi và nhãn này. |
| ATC-C03 | Truyền đạt | Chỉ nghe (không nhìn) vẫn không bị hiểu sai | Nghiêm trọng | Claude | ➖ Không áp dụng | Bản animatic này dựng bằng thời lượng ước tính (manifest.voice_source = estimate). Giọng theo câu mới vừa tạo và chưa được nghe duyệt. Mục này sẽ kiểm ở lần dựng lại animatic có giọng, khi chủ dự án nghe theo phiếu nghe. |
| ATC-C04 | Mở đầu | 5 giây đầu có thay đổi thị giác mạnh và câu móc | Nghiêm trọng | Claude | ✅ Đạt | 00:00 dòng sông vẽ ra; 00:01 biển; 00:02 zoom xuyên sang khung hai cốc; 00:03 dấu hỏi vàng + "Sông ngọt → Biển mặn?". Nghịch lý được nói và hiện ngay từ giây 0. |
| ATC-C05 | Sửa sớm | Không còn thay đổi lớn nào cần làm trước khi dựng hoạt ảnh thật | Chặn | Claude | ✅ Đạt | Cấu trúc nhân quả mưa → đá → sông → biển → bốc hơi → tích luỹ → nguồn phụ → tóm → CTA giữ nguyên. Tổng 48,7 giây so với mục tiêu mới 50 giây (−2,6%). Không cần đổi cấu trúc trước khi dựng hoạt ảnh. |
| ATC-C06 | Rủi ro | Nguồn thời lượng được biết rõ — giọng nháp thật, hoặc ghi nhận rủi ro của ước tính | Nhẹ | Claude | ❌ Trượt | timeline nguồn: 10/10 đoạn giọng là estimate (4,43 âm tiết/giây, đã hiệu chỉnh từ giọng Hải Đăng thật). Có giọng theo câu với khoảng ngắt 0,35/0,45 giây, nên thời lượng thật sẽ dài hơn ước tính ở các đoạn nhiều câu (S01-01, S03-02, S04-01). |
