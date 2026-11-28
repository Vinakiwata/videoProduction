# Báo cáo kiểm duyệt — Animatic (bản nháp thô)

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `animatic` · checklist "Kiểm duyệt animatic (bản nháp thô)" v3
- **Bắt đầu:** 2026-11-28T21:02:14+07:00 · **Chốt:** 2026-11-28T21:02:15+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

11 mục: 11 đạt, 0 trượt, 0 lỗi kiểm tra, 0 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `03_animatic` | `dir:ec89db3635f3` |
| `02_design/storyboard.yaml` | `a74950e4f23f03bd` |
| `01_script/script.yaml` | `29a4a3f1857290eb` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| ATC-A01 | Cấu trúc | Có animatic và bảng thời gian | Chặn | auto | ✅ Đạt | Có đủ: 03_animatic/animatic.mp4, 03_animatic/timing.yaml, 03_animatic/manifest.json |
| ATC-A02 | Kỹ thuật | Animatic có cả hình và tiếng, thời lượng khớp nhau | Nghiêm trọng | auto | ✅ Đạt | Hình 49.200s, tiếng 49.194s, lệch 0.006s (tối đa 0.2s). |
| ATC-A03 | Kỹ thuật | Định dạng nháp = nửa khung storyboard + dải phụ đề riêng (ngang 960×636, dọc 540×1120) @ 15 fps | Nhẹ | auto | ✅ Đạt | Đúng định dạng: 540x1120 @ 15 fps, h264, yuv420p. |
| ATC-A04 | Đồng bộ | Animatic dựng từ đúng kịch bản, storyboard, giọng nháp hiện tại | Chặn | auto | ✅ Đạt | Animatic khớp đầu vào hiện tại (nguồn lời: scratch, 15 fps). |
| ATC-A05 | Đồng bộ | Thời lượng video khớp bảng thời gian (±1 khung) | Chặn | auto | ✅ Đạt | Video 49.200s, timing 49.232s, lệch 0.032s (tối đa 0.07s). |
| ATC-C01 | Nhịp | Nhịp tổng thể không chậm, không dồn | Chặn | Claude | ✅ Đạt | Animatic dựng lại bằng giọng thật lời văn nghiêm túc (Xuân Vĩnh +2,5 nửa cung), 49,2 giây lời. Đoạn dài nhất S02-01 (5,9 giây), ngắn nhất S05-02 (3,4 giây). Tốc độ đã cân trong khoảng 3,9–4,9 âm tiết/giây (S05-02 làm chậm 8%). Ba khoảng nghỉ vẫn giữ. Không khoảng nào > 4 giây không đổi hình. |
| ATC-C02 | Truyền đạt | Chỉ nhìn hình (bỏ phụ đề, tắt tiếng) vẫn hiểu được mạch chính | Nghiêm trọng | Claude | ✅ Đạt | Che phụ đề vẫn theo được mạch. Animatic dựng lại theo khung dọc 540×960 (nửa 1080×1920) với dải phụ đề riêng 160 px bên dưới. Đã xem các khung 3 s, 20 s, 44 s và đối chiếu ảnh ghép bằng hình thật của 7 khung nền xanh: cửa sông (lia xuống theo dòng) → tiêu đề 'Sông ngọt, biển mặn?' trên + hai cốc cạnh nhau + Khỉ thắc mắc dưới → trời mưa, giọt 'axit nhẹ' → tảng đá, hạt bong ra ở vết nứt 'muối' → sườn núi, suối chảy xuống nhập sông → kính lúp trên lòng sông 'rất ít muối' → mưa xuống sông 'nước ngọt mới' → bản đồ, sông chảy xuống biển ở dưới 'Muối dồn về biển' → bãi biển: mặt trời, hơi nước bốc từ mặt biển, muối dưới nước 'Nước bay đi, muối ở lại' → vòng tuần hoàn 'hàng triệu năm' → đáy biển 'Nguồn thêm: đáy biển' → chuỗi Mưa → Sông → Bốc hơi xếp dọc → logo kênh, 'Cảm ơn bạn đã xem!', nút ĐĂNG KÝ. Nhịp và mốc thời gian không đổi so với bản ngang (49,2 giây, cùng span và at), chỉ đổi bố cục. |
| ATC-C03 | Truyền đạt | Chỉ nghe (không nhìn) vẫn không bị hiểu sai | Nghiêm trọng | Vinakiwata (chủ dự án, nghe) | ✅ Đạt | Đọc lời văn nghiêm túc mà không nhìn hình vẫn theo được mạch nhân quả, không có câu nào gây hiểu sai: câu hỏi → nước mưa hơi có tính axit → bào mòn, hoà tan khoáng chất có muối → sông mang lượng muối rất nhỏ → sông vẫn ngọt, biển nhận muối → muối không bốc hơi theo → tích tụ qua hàng triệu năm → nguồn bổ sung dưới đáy biển → tóm tắt. |
| ATC-C04 | Mở đầu | 5 giây đầu có thay đổi thị giác mạnh và câu móc | Nghiêm trọng | Claude | ✅ Đạt | 00:00 cảnh cửa sông hiện ra cùng câu móc "Sông đổ ra biển toàn là nước ngọt. Vậy mà nước biển lại mặn."; khoảng 1,8 giây chuyển xuyên sang hai cốc với Khỉ thắc mắc; câu hỏi "Muối trong biển từ đâu mà có?" kết thúc ở khoảng 4,8 giây (giọng thật). Thay đổi thị giác mạnh và câu móc đều trong 5 giây đầu. |
| ATC-C05 | Sửa sớm | Không còn thay đổi lớn nào cần làm trước khi dựng hoạt ảnh thật | Chặn | Claude | ✅ Đạt | Các thay đổi lớn (cảnh chân thật; kênh Khỉ Khám Phá; giọng Xuân Vĩnh; văn phong nghiêm túc) đều đã chốt và chủ dự án đã duyệt. Việc còn lại chỉ là thay ước tính bằng giọng thật. |
| ATC-C06 | Rủi ro | Nguồn thời lượng được biết rõ — giọng nháp thật, hoặc ghi nhận rủi ro của ước tính | Nhẹ | Claude | ✅ Đạt | Nguồn thời lượng: giọng nháp thật lời văn nghiêm túc (VieNeu v3 Turbo Xuân Vĩnh, Mac, theo câu, chọn trong 3 lượt theo tốc độ và độ đồng nhất cao độ, nâng +2,5 nửa cung, cao độ trung vị 123 Hz, chênh giữa các đoạn 1,36 nửa cung), đã chép sang 03_animatic/scratch_voice. Tốc độ kênh hiệu chỉnh lại 4,41 âm tiết/giây. |
