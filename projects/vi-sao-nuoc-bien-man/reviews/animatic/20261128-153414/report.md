# Báo cáo kiểm duyệt — Animatic (bản nháp thô)

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `animatic` · checklist "Kiểm duyệt animatic (bản nháp thô)" v2
- **Bắt đầu:** 2026-11-28T15:34:14+07:00 · **Chốt:** 2026-11-28T15:34:14+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

11 mục: 11 đạt, 0 trượt, 0 lỗi kiểm tra, 0 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `03_animatic` | `dir:6c1f6c554445` |
| `02_design/storyboard.yaml` | `da9fc6eb6ce28138` |
| `01_script/script.yaml` | `fcd113c10281807c` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| ATC-A01 | Cấu trúc | Có animatic và bảng thời gian | Chặn | auto | ✅ Đạt | Có đủ: 03_animatic/animatic.mp4, 03_animatic/timing.yaml, 03_animatic/manifest.json |
| ATC-A02 | Kỹ thuật | Animatic có cả hình và tiếng, thời lượng khớp nhau | Nghiêm trọng | auto | ✅ Đạt | Hình 47.867s, tiếng 47.850s, lệch 0.017s (tối đa 0.2s). |
| ATC-A03 | Kỹ thuật | Định dạng nháp 960×636 @ 15 fps (hình 960×540 + dải phụ đề riêng) | Nhẹ | auto | ✅ Đạt | Đúng định dạng: 960x636 @ 15 fps, h264, yuv420p. |
| ATC-A04 | Đồng bộ | Animatic dựng từ đúng kịch bản, storyboard, giọng nháp hiện tại | Chặn | auto | ✅ Đạt | Animatic khớp đầu vào hiện tại (nguồn lời: scratch, 15 fps). |
| ATC-A05 | Đồng bộ | Thời lượng video khớp bảng thời gian (±1 khung) | Chặn | auto | ✅ Đạt | Video 47.867s, timing 47.900s, lệch 0.033s (tối đa 0.07s). |
| ATC-C01 | Nhịp | Nhịp tổng thể không chậm, không dồn | Chặn | Claude | ✅ Đạt | Animatic dựng lại bằng giọng thật, dài 47,9 giây. timing.yaml không đổi vì lời và giọng giữ nguyên; chỉ hình đổi: bộ nhận diện Khỉ Khám Phá và Khỉ xuất hiện. Khỉ vào bằng pop ở các mốc S01-01-b (0,6), S04-01-a (0,58), S04-03-b (0,35), mỗi lần chỉ một phần tử mới, không dồn thêm thông tin. Không khoảng nào > 4 giây không đổi hình. |
| ATC-C02 | Truyền đạt | Chỉ nhìn hình (bỏ phụ đề, tắt tiếng) vẫn hiểu được mạch chính | Nghiêm trọng | Claude | ✅ Đạt | Che phụ đề vẫn theo được mạch. Lần này đối chiếu với 18 khung ghép bằng hình SVG thật: cửa sông → hai cốc + 'Sông ngọt → Biển mặn?' → trời mưa, giọt 'axit nhẹ' → tảng đá thật, hạt bong ra ở vết nứt 'muối' → sườn núi, suối nhập sông → kính lúp trên lòng sông 'rất ít muối' → mưa xuống thung lũng sông 'nước ngọt mới' → bản đồ, biển sáng lên 'Muối dồn về biển' → bãi biển: mặt trời, hơi nước bốc từ mặt biển, muối ở dưới nước 'Nước bay đi, muối ở lại' → vòng tuần hoàn 'hàng triệu năm' → đáy biển núi lửa 'Nguồn thêm' → Mưa → Sông → Bốc hơi → nút đăng ký. Cảnh thật giúp nhận ra sông, biển, đá ngay mà không cần chữ. Khỉ làm mạch rõ hơn khi tắt tiếng: thắc mắc ở câu hỏi mở đầu, ngạc nhiên lúc lộ đáp án, ôm Trái Đất ở 'hàng triệu năm', vui mừng ở lời mời đăng ký. |
| ATC-C03 | Truyền đạt | Chỉ nghe (không nhìn) vẫn không bị hiểu sai | Nghiêm trọng | Vinakiwata (chủ dự án, nghe) | ✅ Đạt | Chủ dự án nghe bản giọng 3 (giong_ban_3_toan_bai.mp3, 28/11/2026 10:43) và trả lời "ổn" cho phiếu nghe, gồm mục "chỉ nghe, không nhìn có chỗ nào dễ hiểu sai". Hai lỗi phát hiện ở các bản trước (cacbonic đọc sai, ngắt câu chưa tự nhiên) đã sửa trước bản này. |
| ATC-C04 | Mở đầu | 5 giây đầu có thay đổi thị giác mạnh và câu móc | Nghiêm trọng | Claude | ✅ Đạt | 00:00 cảnh cửa sông hiện ra, sông chảy ra biển (đổi màu mạnh: trời xanh, đồi xanh lá, biển); 00:02 zoom xuyên sang khung hai cốc trên nền xanh đậm; 00:03 dấu hỏi vàng + 'Sông ngọt → Biển mặn?'. Nghịch lý được nói và hiện ngay từ giây 0. |
| ATC-C05 | Sửa sớm | Không còn thay đổi lớn nào cần làm trước khi dựng hoạt ảnh thật | Chặn | Claude | ✅ Đạt | Hai thay đổi lớn (cảnh chân thật; đổi kênh sang Khỉ Khám Phá có linh vật) đều đã làm xong ở storyboard trước khi dựng hoạt ảnh thật. Lời, giọng và thời lượng giữ nguyên (≈ 52 giây sau timeline, chủ dự án đã chấp nhận). Không còn thay đổi lớn nào chờ làm. |
| ATC-C06 | Rủi ro | Nguồn thời lượng được biết rõ — giọng nháp thật, hoặc ghi nhận rủi ro của ước tính | Nhẹ | Claude | ✅ Đạt | timing.yaml: cả 10 đoạn giọng có source = scratch (giọng VieNeu Hải Đăng thật, theo câu, ngắt 0,45/0,55 giây). manifest.voice_source = scratch. Tổng 47,9 giây (chưa gồm ngắt giữa các đoạn, do timeline thêm vào). |
