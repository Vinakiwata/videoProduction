# Báo cáo kiểm duyệt — Hoạt ảnh 2D

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `animation` · checklist "Kiểm duyệt hoạt ảnh 2D" v2
- **Bắt đầu:** 2026-11-28T10:54:21+07:00 · **Chốt:** 2026-11-28T10:54:45+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

12 mục: 12 đạt, 0 trượt, 0 lỗi kiểm tra, 0 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `06_animation` | `dir:70bc9fbe681a` |
| `02_design/storyboard.yaml` | `82024fb70d2f43cf` |
| `05_timeline/timeline.yaml` | `75be9ec1f41add3c` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| ANI-A01 | Cấu trúc | Đủ hình cho mọi asset của storyboard, mỗi hình có nguồn và giấy phép | Chặn | auto | ✅ Đạt | 23 hình đủ file, có nguồn và giấy phép, khớp thư viện storyboard. |
| ANI-A02 | Kỹ thuật | SVG hợp lệ — có viewBox, không ảnh/script/nguồn ngoài, chữ đúng font | Chặn | auto | ✅ Đạt | 23 file SVG hợp lệ, có viewBox, không ảnh/script/nguồn ngoài, chữ đúng font. |
| ANI-A03 | Nhận diện | Chỉ dùng màu nhận diện, ≤ 4 màu mỗi hình | Nghiêm trọng | auto | ✅ Đạt | Mọi hình chỉ dùng màu nhận diện; nhiều nhất 4 màu/hình (≤ 4). |
| ANI-A04 | Kỹ thuật | Có đủ các lớp tách để làm chuyển động | Chặn | auto | ✅ Đạt | 0 lớp khai báo đều có trong file SVG. |
| ANI-A05 | An toàn thị giác | Không nhấp nháy nhanh — chu kỳ sáng/tối ≥ 0,4 giây (WCAG 2.3.1) | Chặn | auto | ✅ Đạt | 8 vòng lặp sáng/tối đều có chu kỳ ≥ 0.4s (≤ 2.5 lần/giây). |
| ANI-A06 | Cấu trúc | Tờ xem trước khớp các file SVG hiện tại | Nhẹ | auto | ✅ Đạt | Tờ xem trước khớp các file SVG hiện tại. |
| ANI-C01 | Độ phủ | Mọi hoạt ảnh trong storyboard đã có, đúng mã cảnh | Chặn | Claude | ✅ Đạt | Đối chiếu 02_design/storyboard.yaml (23 asset ở mục assets) với 06_animation/assets.yaml: đủ 23/23 id, mỗi id có file assets/<ID>.svg. Mọi phần tử của 14 cảnh S01-01-a…S05-02-a trỏ tới asset đều có hình; các chuyển động loop (flow 10, pulse 5, bob 4, shimmer 3, rotate 3, wiggle 2) đều có lớp <g id> tương ứng (ANI-A04 đạt). Không thiếu hình nào. |
| ANI-C02 | Chất lượng hình | Không lỗi hình — không vỡ nét, chi tiết thừa, vật thể xuyên nhau, hình méo | Chặn | Claude | ✅ Đạt | Đã xem assets_preview.png ở cả nền #1B1B1F và #0B3D91, mở riêng A-MAY, A-VONG-TUAN-HOAN và ảnh chồng A-DAY-BIEN + A-KHOANG-CHAT ở 960×540. Lượt đầu phát hiện và đã sửa: COC-SONG/COC-BIEN thiếu nhãn 'sông'/'biển'; A-MAY chỉ 2 khối và có mép vuông thừa (nay 3 khối, đáy phẳng); icon biển trong vòng tuần hoàn trông như vương miện (nay là dải sóng có đáy); núi lửa A-DAY-BIEN quá nhỏ; 7 hình lệch tỉ lệ với ô storyboard (A-SONG, A-MAY, A-DA, A-HAT-MUOI, A-MUOI-O-LAI, A-PHANTU-KHI, A-SUOI) đã chỉnh viewBox; A-KHOANG-CHAT nay khớp đúng miệng núi lửa (225,276) và khe nứt (764,432) trong hộp 864×432. Bản hiện tại: không vỡ nét, không chi tiết thừa, không vật thể xuyên nhau, không méo. |
| ANI-C03 | Chất lượng chuyển động | Chuyển động tự nhiên (easing, có đà, có quán tính), không tuyến tính cứng | Nghiêm trọng | Claude | ✅ Đạt | Storyboard có 18 lượt vào/ra không ghi ease (vd. S02-01-a e3 scale_out, S04-04-a e1 fade, S05-01-a e2 draw). Đã bổ sung motion_defaults trong 06_animation/assets.yaml: fade vào ease_out/ra ease_in, draw ease_in_out, pop back_out (có đà), scale_out back_in (anticipation), drop ease_in + squash 0,85/1,15 trong 4 khung khi chạm (follow-through); loop bob/wiggle/pulse/shimmer dùng sine_in_out; chỉ flow/rotate là tuyến tính liền mạch và typewriter theo bước — đều là bản chất của chuyển động đó. Không còn lượt nào chạy tuyến tính cứng. Việc dựng thật sẽ được Tool 07 kiểm lại ở cổng presentation. |
| ANI-C04 | Truyền đạt | Hoạt ảnh dễ hiểu, không gây hiểu sai hay rối mắt | Chặn | Claude | ✅ Đạt | Mỗi cảnh xếp nhịp bằng 'at' để chỉ một chuyển động chính tại một thời điểm, vd. S02-01-a: mây fade 0 → giọt drop 0,05 → phân tử slide_right 0,35 → morph 0,62; S01-01-a: cốc sông 0 → cốc biển 0,15 → dấu hỏi 0,6. Hướng nhân quả trái→phải (sông/suối chảy sang phải, phân tử bay phải vào giọt, mũi tên chỉ phải); ngoại lệ mây trôi trái ở S04-02-a có ghi chú lý do (về đất liền). Vòng tuần hoàn quay theo chiều kim đồng hồ đúng thứ tự mưa→đá→sông→biển→mây. Chấm khoáng chất bay từ đúng nguồn, không gây hiểu sai. |
| ANI-C05 | Nhận diện | Đúng phong cách nét trong bộ nhận diện (màu đã đo tự động) | Nghiêm trọng | Claude | ✅ Đạt | Cả 23 hình cùng một bộ quy tắc từ _src/ve_hinh.py: phẳng, đầu nét tròn (stroke-linecap/linejoin round), bóng đổ nhẹ #1B1B1F 25% dưới các vật thể đứng riêng (cốc, giọt, mây, đá, chuông, nút, dấu hỏi), hạt muối lập phương dùng chung một hàm cube(), giọt nước dùng chung drop_path(). Hai hình nền toàn khung (A-BAN-DO-SONG, A-DAY-BIEN) không có bóng — đúng vì là mặt cắt/bản đồ. Mức chi tiết đồng đều, không hình nào lệch phong cách; màu đã đo tự động ở ANI-A03. |
| ANI-C06 | Kỹ thuật | Vector hoặc độ phân giải đủ cho 1080p, nền trong suốt khi cần chồng lớp | Nghiêm trọng | Claude | ✅ Đạt | Toàn bộ 23 file là SVG vector thuần (ANI-A02: không có ảnh raster, không GIF), co giãn tuỳ ý cho 1080p. Nền trong suốt ở 20 hình dùng để chồng lớp; chỉ A-BAN-DO-SONG và A-DAY-BIEN có nền riêng vì chiếm cả khung (box 100×100 trong storyboard), A-BIEN tự tô vì là dải biển. A-BIEN và A-SONG đặt preserveAspectRatio=none để phủ đúng ô rộng 4,4–6,4:1. |
