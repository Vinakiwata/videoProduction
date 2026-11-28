# Báo cáo kiểm duyệt — Hoạt ảnh 2D

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `animation` · checklist "Kiểm duyệt hoạt ảnh 2D" v3
- **Bắt đầu:** 2026-11-28T11:16:56+07:00 · **Chốt:** 2026-11-28T11:17:17+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

12 mục: 12 đạt, 0 trượt, 0 lỗi kiểm tra, 0 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `06_animation` | `dir:4810a5de4c44` |
| `02_design/storyboard.yaml` | `239630144b5d47ca` |
| `05_timeline/timeline.yaml` | `eaae4508575608f8` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| ANI-A01 | Cấu trúc | Đủ hình cho mọi asset của storyboard, mỗi hình có nguồn và giấy phép | Chặn | auto | ✅ Đạt | 27 hình đủ file, có nguồn và giấy phép, khớp thư viện storyboard. |
| ANI-A02 | Kỹ thuật | SVG hợp lệ — có viewBox, không ảnh/script/nguồn ngoài, chữ đúng font | Chặn | auto | ✅ Đạt | 27 file SVG hợp lệ, có viewBox, không ảnh/script/nguồn ngoài, chữ đúng font. |
| ANI-A03 | Nhận diện | Icon/chữ/nút chỉ dùng màu nhận diện (≤ 4 màu); cảnh chỉ dùng bảng màu cảnh đã duyệt (≤ 16 màu) | Nghiêm trọng | auto | ✅ Đạt | Icon/chữ/nút chỉ dùng màu nhận diện, nhiều nhất 4 màu/hình (≤ 4); 8 cảnh dùng màu tự nhiên đã duyệt, nhiều nhất 15 màu/cảnh (≤ 16). |
| ANI-A04 | Kỹ thuật | Có đủ các lớp tách để làm chuyển động | Chặn | auto | ✅ Đạt | 44 lớp khai báo đều có trong file SVG. |
| ANI-A05 | An toàn thị giác | Không nhấp nháy nhanh — chu kỳ sáng/tối ≥ 0,4 giây (WCAG 2.3.1) | Chặn | auto | ✅ Đạt | 8 vòng lặp sáng/tối đều có chu kỳ ≥ 0.4s (≤ 2.5 lần/giây). |
| ANI-A06 | Cấu trúc | Tờ xem trước khớp các file SVG hiện tại | Nhẹ | auto | ✅ Đạt | Tờ xem trước khớp các file SVG hiện tại. |
| ANI-C01 | Độ phủ | Mọi hoạt ảnh trong storyboard đã có, đúng mã cảnh | Chặn | Claude | ✅ Đạt | Đối chiếu storyboard (27 asset, gồm 4 asset mới A-CUA-SONG, A-SONG-ICON, A-NEN-MUA, A-SANG-BIEN) với 06_animation/assets.yaml: đủ 27/27 id, mỗi id có file assets/<ID>.svg, đúng kind (10 scene). Mọi phần tử của 18 khung trỏ tới asset đều có hình; mọi loop (flow, pulse, bob, shimmer, rotate, wiggle) có lớp <g id> tương ứng, vd. A-CUA-SONG có river (flow) và waves (bob), A-SUOI có streams (draw), A-SANG-BIEN có glow (pulse). Không thiếu hình nào. |
| ANI-C02 | Chất lượng hình | Không lỗi hình — không vỡ nét, chi tiết thừa, vật thể xuyên nhau, hình méo | Chặn | Claude | ✅ Đạt | Đã xem assets_preview.png (27 hình, hai nền), từng cảnh ở 960×540, và 18 khung ghép đúng toạ độ storyboard. Lỗi tìm thấy ở lượt vẽ cảnh và đã sửa: mép sông A-SONG tự cắt nhau ở khúc cua gắt (nay dựng sông bằng hợp các đoạn nối tiếp, không thể tự cắt); cửa sông A-CUA-SONG bị cắt vuông khi chạm biển (nay loe ra thành luồng nước); một cây thông mọc giữa lòng sông A-CUA-SONG (đã dời); gợn sóng dày rối mắt (giãn ra); quầng sáng miệng núi lửa ra màu ô-liu (đổi sang cam dung nham); mặt trời bị cảnh che ở S04-01/02 (đổi thứ tự lớp); hạt muối lơ lửng trên đá ở S02-02-b (hạ xuống vết nứt). Bản hiện tại không vỡ nét, không chi tiết thừa, không vật thể xuyên nhau, không méo; A-KHOANG-CHAT vẫn khớp miệng núi lửa và khe nứt. |
| ANI-C03 | Chất lượng chuyển động | Chuyển động tự nhiên (easing, có đà, có quán tính), không tuyến tính cứng | Nghiêm trọng | Claude | ✅ Đạt | Storyboard có 18 lượt vào/ra không ghi ease (vd. S02-01-a e3 scale_out, S04-04-a e1 fade, S05-01-a e2 draw). Đã bổ sung motion_defaults trong 06_animation/assets.yaml: fade vào ease_out/ra ease_in, draw ease_in_out, pop back_out (có đà), scale_out back_in (anticipation), drop ease_in + squash 0,85/1,15 trong 4 khung khi chạm (follow-through); loop bob/wiggle/pulse/shimmer dùng sine_in_out; chỉ flow/rotate là tuyến tính liền mạch và typewriter theo bước — đều là bản chất của chuyển động đó. Không còn lượt nào chạy tuyến tính cứng. Việc dựng thật sẽ được Tool 07 kiểm lại ở cổng presentation. |
| ANI-C04 | Truyền đạt | Hoạt ảnh dễ hiểu, không gây hiểu sai hay rối mắt | Chặn | Claude | ✅ Đạt | Mỗi cảnh xếp nhịp bằng 'at' để chỉ một chuyển động chính tại một thời điểm, vd. S02-01-a: mây fade 0 → giọt drop 0,05 → phân tử slide_right 0,35 → morph 0,62; S01-01-a: cốc sông 0 → cốc biển 0,15 → dấu hỏi 0,6. Hướng nhân quả trái→phải (sông/suối chảy sang phải, phân tử bay phải vào giọt, mũi tên chỉ phải); ngoại lệ mây trôi trái ở S04-02-a có ghi chú lý do (về đất liền). Vòng tuần hoàn quay theo chiều kim đồng hồ đúng thứ tự mưa→đá→sông→biển→mây. Chấm khoáng chất bay từ đúng nguồn, không gây hiểu sai. Cảnh nền chân thật không làm rối: chi tiết nhỏ, sắc độ dịu, chừa trống vùng chuyển động chính (trời trống cho mây, mưa và hơi nước; mặt biển trống cho hàng muối). Chữ trên cảnh có tấm nền tối nên luôn đọc rõ. |
| ANI-C05 | Nhận diện | Đúng phong cách nét trong bộ nhận diện (màu đã đo tự động) | Nghiêm trọng | Claude | ✅ Đạt | Theo brand.style mới: 10 cảnh (canh.py) vẽ phẳng, có chiều sâu bằng lớp xa → gần, cây thông dùng chung hàm pine() hai sắc, sông dùng chung river_path(), bóng đổ #1B1B1F 22%, màu chỉ lấy trong scene_colors (ANI-A03 đo: đạt, ≤ 16 màu/cảnh). 17 icon/ui (ve_hinh.py) giữ phẳng, nét tròn, bóng đổ nhẹ, chỉ 4 màu nhận diện, mỗi hình ≤ 4 màu. Mức chi tiết đồng đều trong từng nhóm; icon nổi rõ trên cảnh (mây, giọt, hơi nước trắng trên trời #4A98D6 hoặc #6F879E, tương phản ≥ 3,1:1). |
| ANI-C06 | Kỹ thuật | Vector hoặc độ phân giải đủ cho 1080p, nền trong suốt khi cần chồng lớp | Nghiêm trọng | Claude | ✅ Đạt | Cả 27 file là SVG vector thuần (ANI-A02: không ảnh raster, không GIF), co giãn tuỳ ý cho 1080p. Cảnh (kind scene) có nền riêng vì là lớp dưới cùng phủ cả khung (box 0,0,100,100) hoặc là vật đứng riêng có nền trong suốt (A-DA). 17 icon và lớp phủ (A-SANG-BIEN, A-KHOANG-CHAT, A-HOI-NUOC, A-MUOI-O-LAI…) đều nền trong suốt để chồng lên cảnh, đã kiểm bằng 18 khung ghép. |
