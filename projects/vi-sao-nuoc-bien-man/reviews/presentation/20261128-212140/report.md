# Báo cáo kiểm duyệt — Web trình chiếu

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `presentation` · checklist "Kiểm duyệt web trình chiếu" v2
- **Bắt đầu:** 2026-11-28T21:21:40+07:00 · **Chốt:** 2026-11-28T21:21:40+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

13 mục: 13 đạt, 0 trượt, 0 lỗi kiểm tra, 0 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `07_presentation` | `dir:7a01886adb60` |
| `00_brief/brief.yaml` | `265ae6ddce217881` |
| `05_timeline/timeline.yaml` | `cf891af263c4dad1` |
| `02_design/storyboard.yaml` | `a74950e4f23f03bd` |
| `06_animation/assets.yaml` | `7951cffbc74932fb` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| PRS-A01 | Cấu trúc | presentation.json khớp đầu vào (timeline, storyboard, hình, giọng) | Chặn | auto | ✅ Đạt | presentation.json khớp đầu vào: 18 khung hình, 1602 khung. |
| PRS-A02 | Cấu trúc | Mọi hình có trong assets/ và trùng hash với 06_animation | Chặn | auto | ✅ Đạt | 29 hình có trong assets/ và trùng hash với 06_animation. |
| PRS-A03 | Nhận diện | Font nhận diện có file, có giấy phép và trình duyệt nạp được | Chặn | auto | ✅ Đạt | Font Be Vietnam Pro: 4 file kèm giấy phép, trình duyệt đã nạp. |
| PRS-A04 | Kỹ thuật | Dựng thử không lỗi JS/console, đúng khung của brief, không khung đen hay trống | Chặn | auto | ✅ Đạt | Dựng thử 76 khung mốc 1080×1920: không lỗi JS hay console, không khung đen/trống. |
| PRS-A05 | Kỹ thuật | Tất định — tua xuôi, tua ngược cho ảnh trùng hash điểm ảnh | Chặn | auto | ✅ Đạt | Tất định: 76 khung chụp xuôi rồi ngược trùng hash điểm ảnh. |
| PRS-A06 | Hiển thị | Chữ không tràn box và nằm trong vùng an toàn của các nền tảng đã chọn (đo trong DOM) | Nghiêm trọng | auto | ✅ Đạt | Chữ nằm gọn trong box và trong vùng an toàn của YouTube Shorts, TikTok, Instagram/Facebook Reels (trên 220 · dưới 461 · trái 65 · phải 173 px) ở 76 khung mốc. |
| PRS-A07 | Chuyển động | Mọi vòng lặp và chuyển động lớp có công thức; cảnh có loop phải chạy bằng lớp | Nghiêm trọng | auto | ✅ Đạt | Mọi vòng lặp phần tử và 16 chuyển động lớp đều có công thức; cảnh có loop đều chạy bằng lớp. |
| PRS-A08 | Cấu trúc | Tờ kiểm và tờ ảnh khung mốc khớp bản dựng hiện tại | Chặn | auto | ✅ Đạt | Tờ kiểm và tờ ảnh khung mốc khớp bản dựng hiện tại. |
| PRS-C01 | Bố cục | Bố cục từng khung hình khớp storyboard (vị trí, thứ tự lớp, nền) | Chặn | Claude | ✅ Đạt | Khung dọc 1080×1920 (Shorts/TikTok/Reels). Đối chiếu check/contact.png (76 khung mốc) với 02_design/frames và ảnh ghép bằng hình thật cả 18 khung: vị trí, thứ tự lớp, nền khớp storyboard dọc. Ví dụ: S01-01-b/S01-02-a tiêu đề 'Sông ngọt, biển mặn?' trên, hai cốc cạnh nhau, Khỉ thắc mắc dưới (bố cục chủ dự án chọn); S02-02-b hạt muối ở miệng vết nứt, nhãn 'muối' phải trên; S03-01-b kính lúp trên lòng sông; S03-02-b sông chảy xuống biển, biển sáng trong vùng an toàn; S04-01-a hơi nước bốc từ mặt biển, hàng muối dưới nước, Khỉ ngạc nhiên phải dưới, chữ trái dưới; S04-03-b chữ trên, vòng tuần hoàn giữa, Khỉ và cốc biển hai góc dưới; S04-04-a khoáng chất bay ra từ miệng núi lửa và khe nứt; S05-01-a chuỗi dọc mũi tên chỉ xuống; S05-02-a logo, 'Cảm ơn bạn đã xem!', nút ĐĂNG KÝ (phương án A chủ dự án chọn). check/contact_ui.png chồng giao diện YouTube Shorts (nền tảng che nhiều nhất): không chữ, Khỉ, nút nào nằm dưới vùng che; đã xem thêm khung 1000 ở cỡ thật với lớp phủ TikTok. |
| PRS-C02 | Chuyển cảnh | Chuyển cảnh mượt, đúng loại đã khai | Nghiêm trọng | Claude | ✅ Đạt | 18 khung hình: crossfade 6, match_cut 5, zoom_through 3, cut 2, push_up 1, push_left 1 — đúng loại timeline khai. Đã xem các khung vai 'transition' và 'settled' trong contact.png: zoom_through khung cũ phóng và mờ, khung mới hiện lên; crossfade 8 khung chồng mờ không giật; push_up (đá đẩy lên, cùng nền mưa) và push_left (bãi biển sang nền mưa) liền mạch; match_cut giữ nguyên vị trí vật (hai cốc S01-01-b → S01-02-a, đá S02-02-a → b, bãi biển S04-01-a → S04-02-a). Không khung 'settled' nào kẹt giữa hai cảnh. Chủ dự án xem cả bản có tiếng, không báo lỗi chuyển cảnh. |
| PRS-C03 | Chuyển động | Chuyển động tự nhiên, khớp lời đọc | Chặn | Claude | ✅ Đạt | Chủ dự án (Vinakiwata) chấm ngày 28/11/2026 trên bản dọc 9:16 (Documents/DEV_WORK_SUB/VieNeu-TTS/videoproduction/vi-sao-nuoc-bien-man/trinh_chieu_doc/index.html), phát hết 53,4 giây có tiếng, có lớp phủ Shorts/TikTok/Reels. Lượt đầu chủ dự án báo 'có chỗ chưa ổn' ở đoạn 'Sông ngọt, biển mặn' → đã đổi bố cục (tiêu đề trên, hai cốc cạnh nhau, Khỉ dưới) theo ảnh trước/sau chủ dự án duyệt; sau đó yêu cầu làm lại màn kết, bỏ bớt icon, lồng lời cảm ơn → phương án A (logo, 'Cảm ơn bạn đã xem!', nút ĐĂNG KÝ; bỏ chuông, Khỉ thứ hai, 'Cùng Khỉ nhé!'), lời cảm ơn chỉ bằng chữ. Xem lại bản cập nhật: 'Đã thấy, ổn'. |
| PRS-C04 | Hiển thị | Chữ đúng font nhận diện, đọc rõ, không lỗi dấu tiếng Việt | Chặn | Claude | ✅ Đạt | Trình duyệt nạp đúng 'Be Vietnam Pro 700' và 'Be Vietnam Pro 800' (check_manifest.fonts), font nhúng base64 (OFL). Mọi ký tự chữ trên màn hình đều có trong font (đã đo; bỏ ký tự → không có trong font). Đã xem ở cỡ thật khung 1000 (S04-02-a, 'Nước bay đi, muối ở lại' hai dòng) và các khung có chữ: dấu chồng đúng, không ô vuông, không font dự phòng. Chữ vàng/trắng trên tấm nền xanh đậm 90%, đọc rõ trên mưa, bãi biển, đáy biển. PRS-A06 đo trong DOM: không chữ nào tràn hộp hay ra ngoài vùng an toàn của Shorts/TikTok/Reels (lề 220/461/65/173 px). |
| PRS-C05 | Nhận diện | Linh vật và thương hiệu đúng luật kênh | Nghiêm trọng | Claude | ✅ Đạt | Linh vật phản ứng 3 lần (DSN-A11): thắc mắc (S01-01-b → S01-02-a tính 1), ngạc nhiên (S04-01-a → S04-02-a), ôm Trái Đất (S04-03-b); màn kết có logo Khỉ Khám Phá (linh vật trong logo). PNG giữ tỉ lệ, không phóng quá cỡ file (lớn nhất 367 px/512, logo 540/1024). Khỉ không che nội dung chính và luôn nằm trong vùng an toàn, không dưới cột nút hay dải chú thích của nền tảng. Màu khung, chữ, nút đúng brand (#0B3D91, #0078E0, #FFC907, chữ nút nâu #5E270E). Không logo góc, không intro. |
