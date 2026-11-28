# Báo cáo kiểm duyệt — Hoạt ảnh 2D

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `animation` · checklist "Kiểm duyệt hoạt ảnh 2D" v4
- **Bắt đầu:** 2026-11-28T15:34:23+07:00 · **Chốt:** 2026-11-28T15:34:24+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

13 mục: 13 đạt, 0 trượt, 0 lỗi kiểm tra, 0 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `06_animation` | `dir:8f73d2717688` |
| `02_design/storyboard.yaml` | `da9fc6eb6ce28138` |
| `05_timeline/timeline.yaml` | `7ab8ae0a2500598a` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| ANI-A01 | Cấu trúc | Đủ hình cho mọi asset của storyboard, mỗi hình có nguồn và giấy phép | Chặn | auto | ✅ Đạt | 31 hình đủ file, có nguồn và giấy phép, khớp thư viện storyboard. |
| ANI-A02 | Kỹ thuật | SVG hợp lệ — có viewBox, không ảnh/script/nguồn ngoài, chữ đúng font | Chặn | auto | ✅ Đạt | 26 file SVG hợp lệ, có viewBox, không ảnh/script/nguồn ngoài, chữ đúng font. |
| ANI-A03 | Nhận diện | Icon/chữ/nút chỉ dùng màu nhận diện (≤ 4 màu); cảnh chỉ dùng bảng màu cảnh đã duyệt (≤ 16 màu) | Nghiêm trọng | auto | ✅ Đạt | Icon/chữ/nút chỉ dùng màu nhận diện, nhiều nhất 4 màu/hình (≤ 4); 8 cảnh dùng màu tự nhiên đã duyệt, nhiều nhất 15 màu/cảnh (≤ 16). |
| ANI-A04 | Kỹ thuật | Có đủ các lớp tách để làm chuyển động | Chặn | auto | ✅ Đạt | 44 lớp khai báo đều có trong file SVG. |
| ANI-A05 | An toàn thị giác | Không nhấp nháy nhanh — chu kỳ sáng/tối ≥ 0,4 giây (WCAG 2.3.1) | Chặn | auto | ✅ Đạt | 8 vòng lặp sáng/tối đều có chu kỳ ≥ 0.4s (≤ 2.5 lần/giây). |
| ANI-A06 | Cấu trúc | Tờ xem trước khớp các file SVG hiện tại | Nhẹ | auto | ✅ Đạt | Tờ xem trước khớp các file SVG hiện tại. |
| ANI-A07 | Thương hiệu | Linh vật PNG nền trong suốt, trùng bản gốc của kênh, không phóng to quá cỡ file | Nghiêm trọng | auto | ✅ Đạt | 5 hình linh vật: PNG nền trong suốt, trùng bản gốc của kênh, không phóng to quá cỡ file. |
| ANI-C01 | Độ phủ | Mọi hoạt ảnh trong storyboard đã có, đúng mã cảnh | Chặn | Claude | ✅ Đạt | Đối chiếu storyboard với 06_animation/assets.yaml: đủ 31/31 id, gồm 26 SVG (10 scene) và 5 linh vật PNG (A-KHI-THAC-MAC, A-KHI-NGAC-NHIEN, A-KHI-TRAI-DAT, A-KHI-VUI-MUNG, A-KHI-LOGO). A-HOI đã bỏ khỏi cả storyboard lẫn danh mục, vì Khỉ thắc mắc thay chỗ (animation sync đã khớp). Mọi phần tử của 18 khung đều có hình. Mọi loop đều có lớp tương ứng, riêng linh vật chuyển động nguyên khối (pop, bob, wiggle) nên không cần lớp. |
| ANI-C02 | Chất lượng hình | Không lỗi hình — không vỡ nét, chi tiết thừa, vật thể xuyên nhau, hình méo | Chặn | Claude | ✅ Đạt | Đã xem assets_preview.png, kể cả 5 ô linh vật trên hai nền nâu và xanh: viền sticker trắng gọn, không sót nền trắng, không lẫn mảnh của sticker bên cạnh (lúc tách đã sửa: ngạc nhiên dính ngầu, vệt xanh của nhãn, mép sách). Đã xem 4 khung trong video chuyển động: 3,8 / 30,6 / 36,5 / 50 giây. Khỉ không che nội dung chính (đứng giữa hai cốc, góc bãi cát, góc dưới vòng tuần hoàn, bên trái nút đăng ký). Nền khung giải thích đổi sang xanh đậm #0B3D91 theo lựa chọn của chủ dự án; đã ghép thử lại 6 khung: cốc biển xanh #0078E0 vẫn tách khỏi nền xanh đậm, chữ trên tấm nền xanh đậm, nút vàng chữ nâu, vòng tuần hoàn vàng; không vỡ nét, không méo. Các lỗi đã sửa ở lượt trước vẫn giữ (sông nối ra biển, bờ sông không gãy, mặt trời không bị che). |
| ANI-C03 | Chất lượng chuyển động | Chuyển động tự nhiên (easing, có đà, có quán tính), không tuyến tính cứng | Nghiêm trọng | Claude | ✅ Đạt | Storyboard có 18 lượt vào/ra không ghi ease (vd. S02-01-a e3 scale_out, S04-04-a e1 fade, S05-01-a e2 draw). Đã bổ sung motion_defaults trong 06_animation/assets.yaml: fade vào ease_out/ra ease_in, draw ease_in_out, pop back_out (có đà), scale_out back_in (anticipation), drop ease_in + squash 0,85/1,15 trong 4 khung khi chạm (follow-through); loop bob/wiggle/pulse/shimmer dùng sine_in_out; chỉ flow/rotate là tuyến tính liền mạch và typewriter theo bước — đều là bản chất của chuyển động đó. Không còn lượt nào chạy tuyến tính cứng. Việc dựng thật sẽ được Tool 07 kiểm lại ở cổng presentation. |
| ANI-C04 | Truyền đạt | Hoạt ảnh dễ hiểu, không gây hiểu sai hay rối mắt | Chặn | Claude | ✅ Đạt | Mỗi cảnh xếp nhịp bằng 'at' để chỉ một chuyển động chính tại một thời điểm, vd. S02-01-a: mây fade 0 → giọt drop 0,05 → phân tử slide_right 0,35 → morph 0,62; S01-01-a: cốc sông 0 → cốc biển 0,15 → dấu hỏi 0,6. Hướng nhân quả trái→phải (sông/suối chảy sang phải, phân tử bay phải vào giọt, mũi tên chỉ phải); ngoại lệ mây trôi trái ở S04-02-a có ghi chú lý do (về đất liền). Vòng tuần hoàn quay theo chiều kim đồng hồ đúng thứ tự mưa→đá→sông→biển→mây. Chấm khoáng chất bay từ đúng nguồn, không gây hiểu sai. Cảnh nền chân thật không làm rối: chi tiết nhỏ, sắc độ dịu, chừa trống vùng chuyển động chính (trời trống cho mây, mưa và hơi nước; mặt biển trống cho hàng muối). Chữ trên cảnh có tấm nền tối nên luôn đọc rõ. |
| ANI-C05 | Nhận diện | Đúng phong cách nét trong bộ nhận diện (màu đã đo tự động) | Nghiêm trọng | Claude | ✅ Đạt | Theo brand.style của Khỉ Khám Phá:<br>- Khung giải thích nền xanh đậm #0B3D91 (chủ dự án chọn sau khi so sánh). Cảnh phẳng, màu tự nhiên trong scene_colors. Màu kênh cũ trong cảnh đã thay: dải biển xa dùng #0A2A66, nước đáy biển #1F7FC4/#145A9E, bóng đổ nâu #5E270E 22%, dung nham sáng #FFC907.<br>- 16 icon/ui đổi sang bảng 6 màu kênh, mỗi hình ≤ 4 màu (ANI-A03 đo: đạt).<br>- Linh vật giữ nguyên PNG gốc, đúng chủ ý thương hiệu; ANI-A07 đo: trùng bản gốc của kênh.<br>Khỉ (vẽ chi tiết) và cảnh (phẳng) khác nét nhưng tách bạch nhờ viền trắng kiểu sticker. Đây là cách nhiều kênh giáo dục dùng linh vật, không gây rối. |
| ANI-C06 | Kỹ thuật | Vector hoặc độ phân giải đủ cho 1080p, nền trong suốt khi cần chồng lớp | Nghiêm trọng | Claude | ✅ Đạt | 26 SVG vector thuần (ANI-A02). 5 PNG linh vật RGBA nền trong suốt, 512 px (logo 1024 px). Ô lớn nhất trên hình là A-KHI-VUI-MUNG 44% × 1080 = 475 px ≤ 512 px, nên không phóng to quá cỡ file (ANI-A07 đạt). Giới hạn đã ghi ở hồ sơ kênh: chi tiết gốc của mỗi biểu cảm chỉ khoảng 150–200 px. Hiện đủ dùng ở cỡ đang đặt; nên thay bằng ảnh gốc độ phân giải cao khi có. |
