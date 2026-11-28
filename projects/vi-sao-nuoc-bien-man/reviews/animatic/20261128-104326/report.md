# Báo cáo kiểm duyệt — Animatic (bản nháp thô)

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `animatic` · checklist "Kiểm duyệt animatic (bản nháp thô)" v2
- **Bắt đầu:** 2026-11-28T10:43:26+07:00 · **Chốt:** 2026-11-28T10:43:27+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

11 mục: 11 đạt, 0 trượt, 0 lỗi kiểm tra, 0 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `03_animatic` | `dir:e4ef8ccbfd29` |
| `02_design/storyboard.yaml` | `82024fb70d2f43cf` |
| `01_script/script.yaml` | `c15dd0b128e4e0af` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| ATC-A01 | Cấu trúc | Có animatic và bảng thời gian | Chặn | auto | ✅ Đạt | Có đủ: 03_animatic/animatic.mp4, 03_animatic/timing.yaml, 03_animatic/manifest.json |
| ATC-A02 | Kỹ thuật | Animatic có cả hình và tiếng, thời lượng khớp nhau | Nghiêm trọng | auto | ✅ Đạt | Hình 47.867s, tiếng 47.850s, lệch 0.017s (tối đa 0.2s). |
| ATC-A03 | Kỹ thuật | Định dạng nháp 960×636 @ 15 fps (hình 960×540 + dải phụ đề riêng) | Nhẹ | auto | ✅ Đạt | Đúng định dạng: 960x636 @ 15 fps, h264, yuv420p. |
| ATC-A04 | Đồng bộ | Animatic dựng từ đúng kịch bản, storyboard, giọng nháp hiện tại | Chặn | auto | ✅ Đạt | Animatic khớp đầu vào hiện tại (nguồn lời: scratch, 15 fps). |
| ATC-A05 | Đồng bộ | Thời lượng video khớp bảng thời gian (±1 khung) | Chặn | auto | ✅ Đạt | Video 47.867s, timing 47.900s, lệch 0.033s (tối đa 0.07s). |
| ATC-C01 | Nhịp | Nhịp tổng thể không chậm, không dồn | Chặn | Claude | ✅ Đạt | Animatic dựng bằng giọng thật (47,9 giây). Nhịp hình theo đúng storyboard đã duyệt; các mốc hình co giãn theo tỉ lệ đoạn nên tương quan giữ nguyên so với bản trích 49 khung trước (không khoảng nào > 4 giây không đổi hình, dài nhất S04-04-a ≈ 3,3 giây có camera và núi lửa nhấp nháy). Ngắt giữa các đoạn (0,6–0,9 giây) sẽ do timeline thêm; hình được giữ lại qua các khoảng ngắt. |
| ATC-C02 | Truyền đạt | Chỉ nhìn hình (bỏ phụ đề, tắt tiếng) vẫn hiểu được mạch chính | Nghiêm trọng | Claude | ✅ Đạt | Che dải phụ đề vẫn đọc được mạch: sông ra biển → 2 cốc + "Sông ngọt → Biển mặn?" → giọt mưa "axit nhẹ" → đá, hạt bong ra "muối" → suối thành sông, kính lúp "rất ít muối" → mưa xuống sông "nước ngọt mới" → bản đồ "Muối dồn về biển" → mặt trời, hơi nước "Nước bay đi, muối ở lại" → vòng tuần hoàn "hàng triệu năm" → đáy biển "Nguồn thêm" → Mưa → Sông → Bốc hơi → nút đăng ký "Mỗi tuần một hiện tượng". Đây là wireframe; hình thật ở Tool 06 phải giữ đúng chuỗi và nhãn này. |
| ATC-C03 | Truyền đạt | Chỉ nghe (không nhìn) vẫn không bị hiểu sai | Nghiêm trọng | Vinakiwata (chủ dự án, nghe) | ✅ Đạt | Chủ dự án nghe bản giọng 3 (giong_ban_3_toan_bai.mp3, 28/11/2026 10:43) và trả lời "ổn" cho phiếu nghe, gồm mục "chỉ nghe, không nhìn có chỗ nào dễ hiểu sai". Hai lỗi phát hiện ở các bản trước (cacbonic đọc sai, ngắt câu chưa tự nhiên) đã sửa trước bản này. |
| ATC-C04 | Mở đầu | 5 giây đầu có thay đổi thị giác mạnh và câu móc | Nghiêm trọng | Claude | ✅ Đạt | 00:00 dòng sông vẽ ra; 00:01 biển; 00:02 zoom xuyên sang khung hai cốc; 00:03 dấu hỏi vàng + "Sông ngọt → Biển mặn?". Nghịch lý được nói và hiện ngay từ giây 0. |
| ATC-C05 | Sửa sớm | Không còn thay đổi lớn nào cần làm trước khi dựng hoạt ảnh thật | Chặn | Claude | ✅ Đạt | Cấu trúc nhân quả giữ nguyên. Tổng dự kiến sau timeline ≈ 52 giây so với mục tiêu 50 (+4%). Chủ dự án đã nghe và chấp nhận giọng, nhịp. Không cần đổi cấu trúc. |
| ATC-C06 | Rủi ro | Nguồn thời lượng được biết rõ — giọng nháp thật, hoặc ghi nhận rủi ro của ước tính | Nhẹ | Claude | ✅ Đạt | timing.yaml: cả 10 đoạn giọng có source = scratch (giọng VieNeu Hải Đăng thật, theo câu, ngắt 0,45/0,55 giây). manifest.voice_source = scratch. Tổng 47,9 giây (chưa gồm ngắt giữa các đoạn, do timeline thêm vào). |
