# Báo cáo kiểm duyệt — Hoạt ảnh 2D

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `animation` · checklist "Kiểm duyệt hoạt ảnh 2D" v4
- **Bắt đầu:** 2026-11-28T17:55:51+07:00 · **Chốt:** 2026-11-28T17:55:52+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

13 mục: 13 đạt, 0 trượt, 0 lỗi kiểm tra, 0 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `06_animation` | `dir:63f21aedf3a0` |
| `02_design/storyboard.yaml` | `bcb3f118086440ae` |
| `05_timeline/timeline.yaml` | `6fb8cd41c90f67f8` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| ANI-A01 | Cấu trúc | Đủ hình cho mọi asset của storyboard, mỗi hình có nguồn và giấy phép | Chặn | auto | ✅ Đạt | 31 hình đủ file, có nguồn và giấy phép, khớp thư viện storyboard. |
| ANI-A02 | Kỹ thuật | SVG hợp lệ — có viewBox, không ảnh/script/nguồn ngoài, chữ đúng font | Chặn | auto | ✅ Đạt | 26 file SVG hợp lệ, có viewBox, không ảnh/script/nguồn ngoài, chữ đúng font. |
| ANI-A03 | Nhận diện | Icon/chữ/nút chỉ dùng màu nhận diện (≤ 4 màu); cảnh chỉ dùng bảng màu cảnh đã duyệt (≤ 16 màu) | Nghiêm trọng | auto | ✅ Đạt | Icon/chữ/nút chỉ dùng màu nhận diện, nhiều nhất 4 màu/hình (≤ 4); 8 cảnh dùng màu tự nhiên đã duyệt, nhiều nhất 15 màu/cảnh (≤ 16). |
| ANI-A04 | Kỹ thuật | Có đủ các lớp tách để làm chuyển động | Chặn | auto | ✅ Đạt | 46 lớp khai báo đều có trong file SVG. |
| ANI-A05 | An toàn thị giác | Không nhấp nháy nhanh — chu kỳ sáng/tối ≥ 0,4 giây (WCAG 2.3.1) | Chặn | auto | ✅ Đạt | 8 vòng lặp sáng/tối đều có chu kỳ ≥ 0.4s (≤ 2.5 lần/giây). |
| ANI-A06 | Cấu trúc | Tờ xem trước khớp các file SVG hiện tại | Nhẹ | auto | ✅ Đạt | Tờ xem trước khớp các file SVG hiện tại. |
| ANI-A07 | Thương hiệu | Linh vật PNG nền trong suốt, trùng bản gốc của kênh, không phóng to quá cỡ file | Nghiêm trọng | auto | ✅ Đạt | 5 hình linh vật: PNG nền trong suốt, trùng bản gốc của kênh, không phóng to quá cỡ file. |
| ANI-C01 | Độ phủ | Mọi hoạt ảnh trong storyboard đã có, đúng mã cảnh | Chặn | Claude | ✅ Đạt | Đối chiếu storyboard với 06_animation/assets.yaml: đủ 31/31 id, gồm 26 SVG (10 scene) và 5 linh vật PNG (A-KHI-THAC-MAC, A-KHI-NGAC-NHIEN, A-KHI-TRAI-DAT, A-KHI-VUI-MUNG, A-KHI-LOGO). A-HOI đã bỏ khỏi cả storyboard lẫn danh mục, vì Khỉ thắc mắc thay chỗ (animation sync đã khớp). Mọi phần tử của 18 khung đều có hình. Mọi loop đều có lớp tương ứng, riêng linh vật chuyển động nguyên khối (pop, bob, wiggle) nên không cần lớp. Lượt 28/11 (chuẩn bị Tool 07): 14 asset khai chuyển động lớp (motion) trong assets.yaml: gợn sóng trôi dọc đường tâm ẩn (along) cho A-SONG/A-CUA-SONG/A-SUOI, gợn tách ra lớp ripples riêng ở A-CUA-SONG và A-SUOI (đã thêm vào layers); chấm muối chạy dọc 5 dòng sông bản đồ; hơi nước bay lên và mũi tên nét đứt trôi; mưa rơi lặp (fall); sóng dập dềnh; tia mặt trời và vòng tuần hoàn quay quanh tâm; ánh sáng đáy biển, vùng biển sáng, lấp lánh muối đổi độ mờ; khoáng chất dập dềnh. Các cảnh có loop trong storyboard đều đã có motion, nên Tool 07 không phải trôi cả khối cảnh. |
| ANI-C02 | Chất lượng hình | Không lỗi hình — không vỡ nét, chi tiết thừa, vật thể xuyên nhau, hình méo | Chặn | Claude | ✅ Đạt | Khung dọc 9:16 (28/11/2026): vẽ lại 8 cảnh trên viewBox 540×960 (A-SONG, A-CUA-SONG, A-BIEN, A-SUOI, A-NEN-MUA, A-DAY-BIEN, A-BAN-DO-SONG, A-SANG-BIEN); A-DA giữ nguyên vì tỉ lệ 2,375 khớp ô dọc (80 %×19 % = 864×365 px); A-MUI-TEN vẽ lại thành mũi tên chỉ xuống (100×200) cho chuỗi tóm tắt dọc; A-KHOANG-CHAT đặt lại điểm phát theo đáy biển dọc. Đã xem assets_preview.png trên hai nền và ghép thử cả 18 khung bằng hình thật theo toạ độ storyboard dọc, kèm khung vùng an toàn đỏ. Đã sửa 3 lỗi phát hiện khi ghép: (1) tảng đá đứng trên dải đồi xa xanh lam như trôi trên nước → nâng đồi xanh lá lên 628 để đá đứng trên cỏ; (2) hạt muối lơ lửng trên vết nứt → hạ hộp xuống y 44 %; (3) vùng biển bản đồ nằm phần lớn dưới dải giao diện 461 px → kéo bờ lên 80 px, rồi tách hai sông bên phải đang cắt chéo nhau. Sau sửa: sông cửa sông và 5 sông bản đồ đều đổ hẳn vào biển, không mép gãy; kính lúp đúng trên lòng sông; giọt mưa rơi xuống đúng dòng sông; hơi nước bốc từ mặt biển (chân trời 45 %); hàng muối nằm dưới mặt nước; khoáng chất bay ra từ đúng miệng núi lửa và khe nứt. Linh vật giữ nguyên PNG gốc, viền sticker gọn, không che nội dung chính. |
| ANI-C03 | Chất lượng chuyển động | Chuyển động tự nhiên (easing, có đà, có quán tính), không tuyến tính cứng | Nghiêm trọng | Claude | ✅ Đạt | Storyboard có 18 lượt vào/ra không ghi ease (vd. S02-01-a e3 scale_out, S04-04-a e1 fade, S05-01-a e2 draw). Đã bổ sung motion_defaults trong 06_animation/assets.yaml: fade vào ease_out/ra ease_in, draw ease_in_out, pop back_out (có đà), scale_out back_in (anticipation), drop ease_in + squash 0,85/1,15 trong 4 khung khi chạm (follow-through); loop bob/wiggle/pulse/shimmer dùng sine_in_out; chỉ flow/rotate là tuyến tính liền mạch và typewriter theo bước — đều là bản chất của chuyển động đó. Không còn lượt nào chạy tuyến tính cứng. Việc dựng thật sẽ được Tool 07 kiểm lại ở cổng presentation. |
| ANI-C04 | Truyền đạt | Hoạt ảnh dễ hiểu, không gây hiểu sai hay rối mắt | Chặn | Claude | ✅ Đạt | Dòng chảy chính đi từ trên xuống theo khung dọc: sông từ núi xuống biển (A-CUA-SONG, A-SONG, A-SUOI, bản đồ), giọt mưa rơi từ mây xuống, chuỗi tóm tắt Mưa → Sông → Bốc hơi với mũi tên chỉ xuống. Vật chính của mỗi cảnh nằm trong vùng an toàn (x 32–454, y 110–730 trên khung 540×960): lòng sông nơi đặt kính lúp và giọt mưa, mặt biển nơi hơi nước bốc lên, miệng núi lửa, vùng biển sáng của bản đồ; dải dưới 230 px chỉ là đồi, cát, đáy biển. Một chuyển động chính mỗi lúc, cảnh nền chi tiết nhỏ, sắc độ dịu; trời trống cho mây, mưa, hơi nước. Chữ luôn có tấm nền xanh đậm. |
| ANI-C05 | Nhận diện | Đúng phong cách nét trong bộ nhận diện (màu đã đo tự động) | Nghiêm trọng | Claude | ✅ Đạt | Theo brand.style của Khỉ Khám Phá:<br>- Khung giải thích nền xanh đậm #0B3D91 (chủ dự án chọn sau khi so sánh). Cảnh phẳng, màu tự nhiên trong scene_colors. Màu kênh cũ trong cảnh đã thay: dải biển xa dùng #0A2A66, nước đáy biển #1F7FC4/#145A9E, bóng đổ nâu #5E270E 22%, dung nham sáng #FFC907.<br>- 16 icon/ui đổi sang bảng 6 màu kênh, mỗi hình ≤ 4 màu (ANI-A03 đo: đạt).<br>- Linh vật giữ nguyên PNG gốc, đúng chủ ý thương hiệu; ANI-A07 đo: trùng bản gốc của kênh.<br>Khỉ (vẽ chi tiết) và cảnh (phẳng) khác nét nhưng tách bạch nhờ viền trắng kiểu sticker. Đây là cách nhiều kênh giáo dục dùng linh vật, không gây rối. |
| ANI-C06 | Kỹ thuật | Vector hoặc độ phân giải đủ cho 1080p, nền trong suốt khi cần chồng lớp | Nghiêm trọng | Claude | ✅ Đạt | 26 SVG vector thuần (ANI-A02), cảnh vẽ trên 540×960 rồi phóng lên 1080×1920 không vỡ. 5 PNG linh vật RGBA nền trong suốt, 512 px (logo 1024 px). Ô linh vật lớn nhất trên khung dọc là A-KHI-THAC-MAC / A-KHI-VUI-MUNG rộng 34 % × 1080 = 367 px ≤ 512 px; logo 40 % = 432 px ≤ 1024 px, nên không phóng to quá cỡ file (ANI-A07 đạt). |
