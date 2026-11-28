# Báo cáo kiểm duyệt — Animatic (bản nháp thô)

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `animatic` · checklist "Kiểm duyệt animatic (bản nháp thô)" v2
- **Bắt đầu:** 2026-11-28T16:15:32+07:00 · **Chốt:** 2026-11-28T16:15:33+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

11 mục: 11 đạt, 0 trượt, 0 lỗi kiểm tra, 0 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `03_animatic` | `dir:bf1e1051a52d` |
| `02_design/storyboard.yaml` | `1ee13c8780212fbf` |
| `01_script/script.yaml` | `8b3752fcb9c89921` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| ATC-A01 | Cấu trúc | Có animatic và bảng thời gian | Chặn | auto | ✅ Đạt | Có đủ: 03_animatic/animatic.mp4, 03_animatic/timing.yaml, 03_animatic/manifest.json |
| ATC-A02 | Kỹ thuật | Animatic có cả hình và tiếng, thời lượng khớp nhau | Nghiêm trọng | auto | ✅ Đạt | Hình 52.867s, tiếng 52.900s, lệch 0.033s (tối đa 0.2s). |
| ATC-A03 | Kỹ thuật | Định dạng nháp 960×636 @ 15 fps (hình 960×540 + dải phụ đề riêng) | Nhẹ | auto | ✅ Đạt | Đúng định dạng: 960x636 @ 15 fps, h264, yuv420p. |
| ATC-A04 | Đồng bộ | Animatic dựng từ đúng kịch bản, storyboard, giọng nháp hiện tại | Chặn | auto | ✅ Đạt | Animatic khớp đầu vào hiện tại (nguồn lời: estimate, 15 fps). |
| ATC-A05 | Đồng bộ | Thời lượng video khớp bảng thời gian (±1 khung) | Chặn | auto | ✅ Đạt | Video 52.867s, timing 52.900s, lệch 0.033s (tối đa 0.07s). |
| ATC-C01 | Nhịp | Nhịp tổng thể không chậm, không dồn | Chặn | Claude | ✅ Đạt | Animatic dựng tạm theo thời lượng ước tính của lời văn nghiêm túc (52,9 giây, 4,15 âm tiết/giây đã hiệu chỉnh), trong lúc chờ dựng giọng thật. Ba khoảng nghỉ vẫn giữ. Không khoảng nào > 4 giây không đổi hình, không dồn hai ý mới liền nhau. |
| ATC-C02 | Truyền đạt | Chỉ nhìn hình (bỏ phụ đề, tắt tiếng) vẫn hiểu được mạch chính | Nghiêm trọng | Claude | ✅ Đạt | Che phụ đề vẫn theo được mạch. Lần này đối chiếu với 18 khung ghép bằng hình SVG thật: cửa sông → hai cốc + 'Sông ngọt → Biển mặn?' → trời mưa, giọt 'axit nhẹ' → tảng đá thật, hạt bong ra ở vết nứt 'muối' → sườn núi, suối nhập sông → kính lúp trên lòng sông 'rất ít muối' → mưa xuống thung lũng sông 'nước ngọt mới' → bản đồ, biển sáng lên 'Muối dồn về biển' → bãi biển: mặt trời, hơi nước bốc từ mặt biển, muối ở dưới nước 'Nước bay đi, muối ở lại' → vòng tuần hoàn 'hàng triệu năm' → đáy biển núi lửa 'Nguồn thêm' → Mưa → Sông → Bốc hơi → nút đăng ký. Cảnh thật giúp nhận ra sông, biển, đá ngay mà không cần chữ. Khỉ làm mạch rõ hơn khi tắt tiếng: thắc mắc ở câu hỏi mở đầu, ngạc nhiên lúc lộ đáp án, ôm Trái Đất ở 'hàng triệu năm', vui mừng ở lời mời đăng ký. |
| ATC-C03 | Truyền đạt | Chỉ nghe (không nhìn) vẫn không bị hiểu sai | Nghiêm trọng | Vinakiwata (chủ dự án, nghe) | ✅ Đạt | Đọc lời văn nghiêm túc mà không nhìn hình vẫn theo được mạch nhân quả, không có câu nào gây hiểu sai: câu hỏi → nước mưa hơi có tính axit → bào mòn, hoà tan khoáng chất có muối → sông mang lượng muối rất nhỏ → sông vẫn ngọt, biển nhận muối → muối không bốc hơi theo → tích tụ qua hàng triệu năm → nguồn bổ sung dưới đáy biển → tóm tắt. |
| ATC-C04 | Mở đầu | 5 giây đầu có thay đổi thị giác mạnh và câu móc | Nghiêm trọng | Claude | ✅ Đạt | 00:00 cảnh cửa sông hiện ra cùng câu móc "Sông đổ ra biển toàn là nước ngọt. Vậy mà nước biển lại mặn."; khoảng 1,8 giây chuyển xuyên sang hai cốc với Khỉ thắc mắc; câu hỏi "Muối trong biển từ đâu mà có?" kết thúc ở khoảng 5,1 giây. Thay đổi thị giác mạnh và câu móc đều trong 5 giây đầu. |
| ATC-C05 | Sửa sớm | Không còn thay đổi lớn nào cần làm trước khi dựng hoạt ảnh thật | Chặn | Claude | ✅ Đạt | Các thay đổi lớn (cảnh chân thật; kênh Khỉ Khám Phá; giọng Xuân Vĩnh; văn phong nghiêm túc) đều đã chốt và chủ dự án đã duyệt. Việc còn lại chỉ là thay ước tính bằng giọng thật. |
| ATC-C06 | Rủi ro | Nguồn thời lượng được biết rõ — giọng nháp thật, hoặc ghi nhận rủi ro của ước tính | Nhẹ | Claude | ✅ Đạt | Nguồn thời lượng: ước tính (4,15 âm tiết/giây, đã hiệu chỉnh từ giọng Xuân Vĩnh thật hôm nay, nên sai số nhỏ). Giọng thật (45 lượt) đã có, sẽ dựng ngay sau cổng này, rồi chạy voice to-animatic, dựng lại animatic và duyệt lại. |
