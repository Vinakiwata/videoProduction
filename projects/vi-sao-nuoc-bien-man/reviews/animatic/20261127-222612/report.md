# Báo cáo kiểm duyệt — Animatic (bản nháp thô)

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `animatic` · checklist "Kiểm duyệt animatic (bản nháp thô)" v2
- **Bắt đầu:** 2026-11-27T22:26:12+07:00 · **Chốt:** 2026-11-27T22:26:12+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 97/100

11 mục: 9 đạt, 1 trượt, 0 lỗi kiểm tra, 1 không áp dụng.

## Nên cải thiện (không chặn cổng)

- **ATC-C06 Nguồn thời lượng được biết rõ — giọng nháp thật, hoặc ghi nhận rủi ro của ước tính:** timing.yaml: cả 10 đoạn giọng có source = estimate (3,2 âm tiết/giây), 0 đoạn giọng nháp. Nhịp đang duyệt dựa hoàn toàn trên ước tính. Nếu VieNeu đọc chậm hoặc nhanh hơn 10–15%, khoảng trống và độ dồn giữa các khung sẽ thay đổi. → Khi có VieNeu-TTS (bật quyền mạng): tạo giọng nháp vào 03_animatic/scratch_voice/<mã đoạn>.wav, chạy lại "python -m vp animatic build" để duyệt nhịp với giọng thật. Bắt buộc kiểm lại nhịp ở cổng voice và timeline; cập nhật voice_profile.syllables_per_second của kênh theo số đo thật.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `03_animatic` | `dir:a2d2e7f9b809` |
| `02_design/storyboard.yaml` | `ac028c7e7eb00790` |
| `01_script/script.yaml` | `acd0288e8539eda3` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| ATC-A01 | Cấu trúc | Có animatic và bảng thời gian | Chặn | auto | ✅ Đạt | Có đủ: 03_animatic/animatic.mp4, 03_animatic/timing.yaml, 03_animatic/manifest.json |
| ATC-A02 | Kỹ thuật | Animatic có cả hình và tiếng, thời lượng khớp nhau | Nghiêm trọng | auto | ✅ Đạt | Hình 65.867s, tiếng 65.900s, lệch 0.033s (tối đa 0.2s). |
| ATC-A03 | Kỹ thuật | Định dạng nháp 960×636 @ 15 fps (hình 960×540 + dải phụ đề riêng) | Nhẹ | auto | ✅ Đạt | Đúng định dạng: 960x636 @ 15 fps, h264, yuv420p. |
| ATC-A04 | Đồng bộ | Animatic dựng từ đúng kịch bản, storyboard, giọng nháp hiện tại | Chặn | auto | ✅ Đạt | Animatic khớp đầu vào hiện tại (nguồn lời: estimate, 15 fps). |
| ATC-A05 | Đồng bộ | Thời lượng video khớp bảng thời gian (±1 khung) | Chặn | auto | ✅ Đạt | Video 65.867s, timing 65.900s, lệch 0.033s (tối đa 0.07s). |
| ATC-C01 | Nhịp | Nhịp tổng thể không chậm, không dồn | Chặn | Claude | ✅ Đạt | Trích 66 khung (1 khung/giây) và xem tuần tự, đối chiếu timing.yaml. Không chỗ nào quá 4 giây không có thay đổi thị giác. Khoảng lặng dài nhất: S04-04-a từ 00:48,5 (chữ vào) tới 00:52,3 (khoáng chất bay lên) ≈ 3,8 giây, có camera zoom_in và nhịp sáng núi lửa; S03-02-b 00:29,9 → 00:33,4 ≈ 3,5 giây, có dòng chấm chảy và biển nhấp nháy. Không có cụm ≥ 3 phần tử mới cách nhau < 0,5 giây; S05-01 hiện 3 biểu tượng cách nhau khoảng 1,6–1,9 giây. |
| ATC-C02 | Truyền đạt | Chỉ nhìn hình (bỏ phụ đề, tắt tiếng) vẫn hiểu được mạch chính | Nghiêm trọng | Claude | ✅ Đạt | Che dải phụ đề và xem chuỗi khung: sông đổ ra biển → hai cốc (ngọt/mặn) + "Sông ngọt → Biển mặn?" → giọt mưa hút khí, đổi viền "axit nhẹ" → mưa trên đá, hạt bong ra "muối" → suối thành sông, kính lúp "rất ít muối" → mưa xuống sông "nước ngọt mới" → bản đồ mọi sông đổ về biển → mặt trời, hơi nước bay lên, "Nước bay đi, muối ở lại" → vòng tuần hoàn "hàng triệu năm" → đáy biển "Nguồn thêm" → Mưa → Sông → Bốc hơi → nút đăng ký. Mạch nhân quả đọc được chỉ bằng hình và nhãn. Lưu ý: đây là wireframe; hình thật ở Tool 06 phải giữ đúng các nhãn và chuỗi này. |
| ATC-C03 | Truyền đạt | Chỉ nghe (không nhìn) vẫn không bị hiểu sai | Nghiêm trọng | Claude | ➖ Không áp dụng | manifest.voice_source = estimate: chưa có giọng nháp (môi trường chưa cài được VieNeu-TTS, chưa có file trong scratch_voice/). Không thể nghe thử. Mục này phải kiểm lại ở cổng voice và mix. |
| ATC-C04 | Mở đầu | 5 giây đầu có thay đổi thị giác mạnh và câu móc | Nghiêm trọng | Claude | ✅ Đạt | Khung 0–5 giây: 00:00 dòng sông vẽ ra; 00:01 biển hiện bên phải; 00:02,2 zoom xuyên sang khung hai cốc (cắt cảnh mạnh); 00:02,7 cốc biển bật lên; 00:03,8 chữ "Sông ngọt → Biển mặn?"; 00:04,3 dấu hỏi vàng bật kèm pop. Câu móc là nghịch lý, nói ngay từ giây 0. |
| ATC-C05 | Sửa sớm | Không còn thay đổi lớn nào cần làm trước khi dựng hoạt ảnh thật | Chặn | Claude | ✅ Đạt | Thứ tự cảnh theo đúng chuỗi nhân quả mưa → đá → sông → biển → bốc hơi → tích luỹ, cộng nguồn phụ và tóm lại. Tổng 65,9 giây so với mục tiêu 60 giây (+9,8%, trong ngưỡng). Không thấy cần đổi cấu trúc. Rủi ro còn lại chỉ ở thời lượng thật của giọng (xem ATC-C06), không ở cấu trúc. |
| ATC-C06 | Rủi ro | Nguồn thời lượng được biết rõ — giọng nháp thật, hoặc ghi nhận rủi ro của ước tính | Nhẹ | Claude | ❌ Trượt | timing.yaml: cả 10 đoạn giọng có source = estimate (3,2 âm tiết/giây), 0 đoạn giọng nháp. Nhịp đang duyệt dựa hoàn toàn trên ước tính. Nếu VieNeu đọc chậm hoặc nhanh hơn 10–15%, khoảng trống và độ dồn giữa các khung sẽ thay đổi. |
