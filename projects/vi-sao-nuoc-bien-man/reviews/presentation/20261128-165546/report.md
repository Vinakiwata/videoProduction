# Báo cáo kiểm duyệt — Web trình chiếu

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `presentation` · checklist "Kiểm duyệt web trình chiếu" v1
- **Bắt đầu:** 2026-11-28T16:55:46+07:00 · **Chốt:** 2026-11-28T16:56:24+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

13 mục: 13 đạt, 0 trượt, 0 lỗi kiểm tra, 0 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `07_presentation` | `dir:555ebbd446a5` |
| `05_timeline/timeline.yaml` | `11997789b3395a6e` |
| `02_design/storyboard.yaml` | `369ae12028c325bd` |
| `06_animation/assets.yaml` | `f31a4e60ffb41357` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| PRS-A01 | Cấu trúc | presentation.json khớp đầu vào (timeline, storyboard, hình, giọng) | Chặn | auto | ✅ Đạt | presentation.json khớp đầu vào: 18 khung hình, 1602 khung. |
| PRS-A02 | Cấu trúc | Mọi hình có trong assets/ và trùng hash với 06_animation | Chặn | auto | ✅ Đạt | 31 hình có trong assets/ và trùng hash với 06_animation. |
| PRS-A03 | Nhận diện | Font nhận diện có file, có giấy phép và trình duyệt nạp được | Chặn | auto | ✅ Đạt | Font Be Vietnam Pro: 4 file kèm giấy phép, trình duyệt đã nạp. |
| PRS-A04 | Kỹ thuật | Dựng thử không lỗi JS/console, đúng 1920×1080, không khung đen hay trống | Chặn | auto | ✅ Đạt | Dựng thử 76 khung mốc 1920×1080: không lỗi JS hay console, không khung đen/trống. |
| PRS-A05 | Kỹ thuật | Tất định — tua xuôi, tua ngược cho ảnh trùng hash điểm ảnh | Chặn | auto | ✅ Đạt | Tất định: 76 khung chụp xuôi rồi ngược trùng hash điểm ảnh. |
| PRS-A06 | Hiển thị | Chữ không tràn box và nằm trong vùng an toàn 5% (đo trong DOM) | Nghiêm trọng | auto | ✅ Đạt | Chữ nằm gọn trong box và trong vùng an toàn 5% ở 76 khung mốc. |
| PRS-A07 | Chuyển động | Mọi vòng lặp và chuyển động lớp có công thức; cảnh có loop phải chạy bằng lớp | Nghiêm trọng | auto | ✅ Đạt | Mọi vòng lặp phần tử và 16 chuyển động lớp đều có công thức; cảnh có loop đều chạy bằng lớp. |
| PRS-A08 | Cấu trúc | Tờ kiểm và tờ ảnh khung mốc khớp bản dựng hiện tại | Chặn | auto | ✅ Đạt | Tờ kiểm và tờ ảnh khung mốc khớp bản dựng hiện tại. |
| PRS-C01 | Bố cục | Bố cục từng khung hình khớp storyboard (vị trí, thứ tự lớp, nền) | Chặn | Claude | ✅ Đạt | Đặt cạnh nhau 18/18 khung: 02_design/frames/<mã>.png và khung cuối của từng khung hình trong check/ (ảnh so sánh dựng từ check_manifest). Vị trí, thứ tự lớp và nền đều khớp. Ví dụ: S01-01-b hai cốc hai bên, Khỉ thắc mắc ở giữa, chữ 'Sông ngọt → Biển mặn?' dưới; S02-01-a giọt đã morph thành giọt axit vàng, phân tử đã scale_out, nhãn 'axit nhẹ' bên phải; S02-02-b nhãn 'muối' góc phải trên, hạt muối nằm trên vết nứt; S03-02-b lớp A-SANG-BIEN phủ đúng vùng biển bản đồ; S04-01-a mặt trời trái, hơi nước bay lên, hàng muối trên mặt biển, Khỉ ngạc nhiên góc phải; S04-03-b vòng tuần hoàn giữa, cốc biển phải, 'hàng triệu năm' trái, Khỉ ôm trái đất dưới trái; S04-04-a nhãn trái trên, khoáng chất bay từ miệng núi lửa và khe nứt; S05-01-a chuỗi Mưa → Sông → Bốc hơi; S05-02-a logo trên, Khỉ vui mừng trái, nút ĐĂNG KÝ và chuông, 'Cùng Khỉ nhé!'. Camera chạy đúng hướng: zoom_in S02-02-b đá to dần, zoom_out S03-02-b bản đồ thu về. Nền xanh đậm #0B3D91 ở khung giải thích, kết #0078E0. Không thiếu phần tử nào. |
| PRS-C02 | Chuyển cảnh | Chuyển cảnh mượt, đúng loại đã khai | Nghiêm trọng | Claude | ✅ Đạt | Xem 17 khung vai 'transition' và 'settled' trong contact.png. Mỗi lượt đúng loại đã khai trong timeline. zoom_through (khung 62, 773, 1200): khung cũ phóng to và mờ dần, khung mới hiện lên. crossfade 8 khung (179, 867, 1066, 1351, 1503): hai khung chồng mờ, không giật. push_up (375): cảnh đá đẩy lên từ dưới, cùng nền mưa nên liền mạch. push_left (1034): bãi biển đẩy sang trái, nền mưa vào từ phải. match_cut (145, 415, 498, 528, 580, 999) chuyển thẳng, giữ nguyên vị trí vật nên không nhảy hình: hai cốc S01-01-b → S01-02-a, đá S02-02-a → b. Không còn khung nào kẹt giữa hai cảnh sau lượt chuyển (khung 'settled' đều sạch). Chủ dự án xem cả bản có tiếng, không báo lỗi chuyển cảnh. |
| PRS-C03 | Chuyển động | Chuyển động tự nhiên, khớp lời đọc | Chặn | Claude | ✅ Đạt | Chủ dự án (Vinakiwata) chấm ngày 28/11/2026, sau khi mở 07_presentation trên máy mình (Documents/DEV_WORK_SUB/VieNeu-TTS/videoproduction/vi-sao-nuoc-bien-man/trinh_chieu/index.html), phát hết 53,4 giây có tiếng. Kết luận: 'Tự nhiên, khớp lời'. Các chuyển động đã xem: sông chảy (gợn trôi xuôi dòng), mưa rơi, muối chạy ra biển trên bản đồ, nắng quay, Khỉ phản ứng. |
| PRS-C04 | Hiển thị | Chữ đúng font nhận diện, đọc rõ, không lỗi dấu tiếng Việt | Chặn | Claude | ✅ Đạt | Trình duyệt nạp đúng 'Be Vietnam Pro 700' và 'Be Vietnam Pro 800' (check_manifest.fonts), font nhúng base64 từ channels/khi-kham-pha/brand/fonts (OFL). Đã xem ở cỡ thật 1920×1080 các khung 144, 998, 1270: dấu chồng hiển thị đúng ('ở lại', 'Nguồn thêm: đáy biển', 'Biển mặn?'), không ô vuông, không rơi về font dự phòng. Chữ vàng #FFC907 hoặc trắng trên tấm nền xanh đậm 90%, đọc rõ cả trên cảnh mưa và bãi biển; mục DSN đã đo tương phản ≥ 5:1. PRS-A06 đo trong DOM: không chữ nào tràn box hay ra ngoài vùng an toàn. |
| PRS-C05 | Nhận diện | Linh vật và thương hiệu đúng luật kênh | Nghiêm trọng | Claude | ✅ Đạt | Linh vật phản ứng 3 lần, khớp storyboard và DSN-A11: thắc mắc (S01-01-b, S01-02-a liền nhau tính 1), ngạc nhiên (S04-01-a, S04-02-a), ôm trái đất (S04-03-b). Kết video có logo Khỉ Khám Phá và Khỉ vui mừng cạnh nút ĐĂNG KÝ. PNG giữ nguyên tỉ lệ (object-fit contain, không méo), viền sticker trắng gọn trên cả nền xanh và cảnh. Khỉ không che nội dung chính: giữa hai cốc, góc bãi cát, góc dưới vòng tuần hoàn, trái nút đăng ký. Màu khung, chữ, nút đúng brand (#0B3D91, #0078E0, #FFC907, chữ nút nâu #5E270E). Không có logo góc hay intro, đúng lựa chọn của chủ dự án. |
