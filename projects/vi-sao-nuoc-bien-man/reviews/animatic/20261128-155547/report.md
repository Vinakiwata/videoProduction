# Báo cáo kiểm duyệt — Animatic (bản nháp thô)

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `animatic` · checklist "Kiểm duyệt animatic (bản nháp thô)" v2
- **Bắt đầu:** 2026-11-28T15:55:47+07:00 · **Chốt:** 2026-11-28T15:56:04+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

11 mục: 11 đạt, 0 trượt, 0 lỗi kiểm tra, 0 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `03_animatic` | `dir:723972fe0577` |
| `02_design/storyboard.yaml` | `1ee13c8780212fbf` |
| `01_script/script.yaml` | `9cf5b54d02782ba3` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| ATC-A01 | Cấu trúc | Có animatic và bảng thời gian | Chặn | auto | ✅ Đạt | Có đủ: 03_animatic/animatic.mp4, 03_animatic/timing.yaml, 03_animatic/manifest.json |
| ATC-A02 | Kỹ thuật | Animatic có cả hình và tiếng, thời lượng khớp nhau | Nghiêm trọng | auto | ✅ Đạt | Hình 49.400s, tiếng 49.400s, lệch 0.000s (tối đa 0.2s). |
| ATC-A03 | Kỹ thuật | Định dạng nháp 960×636 @ 15 fps (hình 960×540 + dải phụ đề riêng) | Nhẹ | auto | ✅ Đạt | Đúng định dạng: 960x636 @ 15 fps, h264, yuv420p. |
| ATC-A04 | Đồng bộ | Animatic dựng từ đúng kịch bản, storyboard, giọng nháp hiện tại | Chặn | auto | ✅ Đạt | Animatic khớp đầu vào hiện tại (nguồn lời: estimate, 15 fps). |
| ATC-A05 | Đồng bộ | Thời lượng video khớp bảng thời gian (±1 khung) | Chặn | auto | ✅ Đạt | Video 49.400s, timing 49.400s, lệch 0.000s (tối đa 0.07s). |
| ATC-C01 | Nhịp | Nhịp tổng thể không chậm, không dồn | Chặn | Claude | ✅ Đạt | Animatic dựng theo thời lượng ước tính của lời mới (49,4 giây, 4,43 âm tiết/giây), vì giọng Xuân Vĩnh đang được tạo trên Mac. Đoạn dài nhất 5,0 giây (S01-01, S02-01), ngắn nhất 4,1 giây (S05-02). Ba khoảng nghỉ S01-02, S02-03, S04-02 vẫn giữ. Không khoảng nào > 4 giây không đổi hình, không dồn hai ý mới liền nhau. |
| ATC-C02 | Truyền đạt | Chỉ nhìn hình (bỏ phụ đề, tắt tiếng) vẫn hiểu được mạch chính | Nghiêm trọng | Claude | ✅ Đạt | Che phụ đề vẫn theo được mạch. Lần này đối chiếu với 18 khung ghép bằng hình SVG thật: cửa sông → hai cốc + 'Sông ngọt → Biển mặn?' → trời mưa, giọt 'axit nhẹ' → tảng đá thật, hạt bong ra ở vết nứt 'muối' → sườn núi, suối nhập sông → kính lúp trên lòng sông 'rất ít muối' → mưa xuống thung lũng sông 'nước ngọt mới' → bản đồ, biển sáng lên 'Muối dồn về biển' → bãi biển: mặt trời, hơi nước bốc từ mặt biển, muối ở dưới nước 'Nước bay đi, muối ở lại' → vòng tuần hoàn 'hàng triệu năm' → đáy biển núi lửa 'Nguồn thêm' → Mưa → Sông → Bốc hơi → nút đăng ký. Cảnh thật giúp nhận ra sông, biển, đá ngay mà không cần chữ. Khỉ làm mạch rõ hơn khi tắt tiếng: thắc mắc ở câu hỏi mở đầu, ngạc nhiên lúc lộ đáp án, ôm Trái Đất ở 'hàng triệu năm', vui mừng ở lời mời đăng ký. |
| ATC-C03 | Truyền đạt | Chỉ nghe (không nhìn) vẫn không bị hiểu sai | Nghiêm trọng | Vinakiwata (chủ dự án, nghe) | ✅ Đạt | Đọc lời mới mà không nhìn hình vẫn theo được mạch nhân quả: câu hỏi "Muối ở đâu ra vậy ta?" → "thủ phạm đầu tiên là nước mưa… hơi chua" → "gặm… hoà tan khoáng chất… có muối" → "rủ nhau về suối, về sông… xíu xiu" → "sông vẫn ngọt, biển gom muối" → "muối không biết bay, ở lại" → "hàng triệu năm" → "thêm nguồn đáy biển" → tóm tắt. Các câu nhân hoá không gây hiểu sai, vì ngay sau đó đều có ý khoa học rõ: "hơi chua", "hoà tan khoáng chất", "ở lại dưới biển". |
| ATC-C04 | Mở đầu | 5 giây đầu có thay đổi thị giác mạnh và câu móc | Nghiêm trọng | Claude | ✅ Đạt | 00:00 cảnh cửa sông hiện ra cùng câu móc "Ê bạn ơi, sông đổ ra biển toàn nước ngọt. Vậy mà biển lại mặn chát!"; khoảng 1,8 giây chuyển xuyên sang hai cốc với Khỉ thắc mắc; câu hỏi "Muối ở đâu ra vậy ta?" kết thúc ở khoảng 5 giây. Thay đổi thị giác mạnh và câu móc đều nằm trong 5 giây đầu. |
| ATC-C05 | Sửa sớm | Không còn thay đổi lớn nào cần làm trước khi dựng hoạt ảnh thật | Chặn | Claude | ✅ Đạt | Ba thay đổi lớn (cảnh chân thật; kênh Khỉ Khám Phá có linh vật; giọng Xuân Vĩnh + lời dí dỏm) đều đã chốt và chủ dự án đã duyệt. Cấu trúc nhân quả và hình giữ nguyên. Việc còn lại chỉ là thay thời lượng ước tính bằng giọng thật, không phải thay đổi lớn. |
| ATC-C06 | Rủi ro | Nguồn thời lượng được biết rõ — giọng nháp thật, hoặc ghi nhận rủi ro của ước tính | Nhẹ | Claude | ✅ Đạt | Nguồn thời lượng: ước tính (4,43 âm tiết/giây theo voice_profile của kênh). Rủi ro đã biết: giọng Xuân Vĩnh nâng +2,5 nửa cung chưa hiệu chỉnh tốc độ. Buổi nghe thử 4 câu cho thấy tốc độ xấp xỉ Hải Đăng: tổng 10,9 giây cho 45 âm tiết, tính cả lặng hai đầu, tức ≥ 4,1 âm tiết/giây. Rubberband nâng tông không đổi độ dài. Khi có giọng thật sẽ chạy voice to-animatic, dựng lại animatic và duyệt lại; timeline cũng sẽ khoá theo giọng thật. |
