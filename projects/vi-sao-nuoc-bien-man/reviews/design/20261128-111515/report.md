# Báo cáo kiểm duyệt — Thiết kế nội dung & storyboard

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `design` · checklist "Kiểm duyệt thiết kế nội dung & storyboard" v3
- **Bắt đầu:** 2026-11-28T11:15:15+07:00 · **Chốt:** 2026-11-28T11:15:55+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

19 mục: 19 đạt, 0 trượt, 0 lỗi kiểm tra, 0 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `02_design` | `dir:b1dd01af676e` |
| `01_script/script.yaml` | `c15dd0b128e4e0af` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| DSN-A01 | Cấu trúc | Storyboard đúng định dạng chuẩn (schema) | Chặn | auto | ✅ Đạt | 02_design/storyboard.yaml khớp schema 'storyboard'. |
| DSN-A02 | Cấu trúc | Không còn chỗ trống (TODO) | Chặn | auto | ✅ Đạt | 02_design/storyboard.yaml: không còn chỗ trống hay đánh dấu tạm. |
| DSN-A03 | Độ phủ | Mọi đoạn kịch bản được phủ kín bởi khung hình, không hở, không chồng | Chặn | auto | ✅ Đạt | 13 đoạn kịch bản đều được phủ kín bởi 18 khung hình. |
| DSN-A04 | Cấu trúc | Tham chiếu asset / điểm nhìn / tiếng động hợp lệ | Chặn | auto | ✅ Đạt | 18 khung, 27 asset, mọi tham chiếu hợp lệ. |
| DSN-A05 | Khả năng đọc | Tương phản chữ/nền ≥ 4,5:1 (chữ trên cảnh tính với màu sáng nhất của cảnh, qua tấm nền text_plate) | Chặn | auto | ✅ Đạt | 15 phần tử chữ, tương phản thấp nhất 5.23:1 (≥ 4.5:1) (chữ trên cảnh tính qua tấm nền, với màu sáng nhất của cảnh). |
| DSN-A06 | Nhận diện | Mọi màu thuộc bảng màu của brief (màu cảnh chỉ cho asset kind=scene) | Nghiêm trọng | auto | ✅ Đạt | Mọi màu thuộc bảng màu nhận diện (4 màu, cảnh dùng thêm 20 màu tự nhiên). |
| DSN-A07 | Khả năng đọc | Chữ đủ lớn, ≤ 7 từ/dòng, hiển thị đủ lâu để đọc | Nghiêm trọng | auto | ✅ Đạt | 15 phần tử chữ: đủ cỡ, ≤ 7 từ/dòng, đủ thời gian đọc. |
| DSN-A08 | Bố cục | Chữ trong vùng an toàn 5%, hình không tràn quá 10% | Nghiêm trọng | auto | ✅ Đạt | Chữ trong vùng an toàn 5%, hình không tràn quá 10%. |
| DSN-A09 | Âm thanh | Tiếng động không dày quá 5 cái mỗi 10 giây | Nhẹ | auto | ✅ Đạt | 6 tiếng động, dày nhất 2 trong 10 giây (tối đa 5). |
| DSN-A10 | Cấu trúc | Ảnh phác thảo khớp storyboard hiện tại | Nhẹ | auto | ✅ Đạt | 18 ảnh phác thảo khớp storyboard hiện tại. |
| DSN-C02 | Truyền đạt | Mỗi khung có một điểm nhìn chính rõ ràng | Nghiêm trọng | Claude | ✅ Đạt | Đã ghép thử 18 khung đúng toạ độ storyboard (cảnh SVG thật + phần tử + chữ có tấm nền) và xem từng khung. Cảnh chiếm cả khung, phần tử focal nổi trên cảnh: S03-01-b kính lúp vàng đặt đúng lòng sông (tâm ≈ 48%, 72%); S04-01-a hơi nước trắng trên trời xanh, chân đặt đúng mặt biển (50%); S02-02-b hạt muối ngay vết nứt trên đỉnh đá (đã hạ hộp từ y 38 xuống 46 sau khi thấy hạt lơ lửng phía trên đá); S04-01/02 đã đưa cảnh A-BIEN xuống lớp dưới cùng (trước đó che mất mặt trời). Mỗi khung còn một điểm nhìn chính, cảnh nền không tranh chú ý vì chi tiết nhỏ và sắc độ dịu. |
| DSN-C03 | Truyền đạt | Hình minh hoạ đúng nghĩa lời đọc, không gây hiểu sai | Chặn | Claude | ✅ Đạt | Hình khớp nghĩa và đúng lúc ở mọi khung. S04-04-a đã thêm e3 A-KHOANG-CHAT với enter slide_up at 0.7, khớp chữ "thả khoáng chất vào nước" (âm tiết 15–20 trên 20 ≈ 0.7). Mô tả A-DAY-BIEN đã bỏ phần khoáng chất để không vẽ trùng. Đã kiểm lại các khung khoa học: hơi nước không mang muối (S04-01-a), cốc biển dừng ở mức hiện nay (S04-03-b, đúng NOAA). Đã kiểm lại mốc chữ sau khi giọng nhanh hơn: các nhãn đưa lên sớm 0,06–0,08 (vd. "axit nhẹ" 0.56, "muối" 0.6) — vẫn ngay trước/đúng lúc từ khoá được nói, không đến sau lời. Lần này đã kiểm thêm cảnh mới: cửa sông S01-01-a cho thấy đúng sông đổ ra biển; A-NEN-MUA là trời mưa cho chặng mưa – đá; bản đồ S03-02-b có lớp A-SANG-BIEN khớp đúng vùng biển; bãi biển S04-01-a có muối nằm DƯỚI mặt nước (hộp y 62–72, biển 50–80%), không nằm trên cát. |
| DSN-C04 | Nhịp | Điểm rơi và tiếng động đặt đúng khoảnh khắc có nghĩa | Nghiêm trọng | Claude | ✅ Đạt | 6 tiếng động, mỗi cái gắn với một hành động có nghĩa: pop ← dấu hỏi bật (S01-01-b); lách tách ← hạt bong khỏi đá (S02-02-b); róc rách ← muối trôi (S02-03); pop nhẹ ← mây hình thành (S04-01-a, rơi đúng chữ "thành mây", củng cố từ đó chứ không che, vì là tiếng nhẹ dưới giọng); whoosh ← mây trôi đi trong đoạn im lặng S04-02; click ← nút đăng ký. Dày nhất 1–2 cái mỗi 10 giây. |
| DSN-C05 | Nhận diện | Phong cách hình đúng brand.style | Nghiêm trọng | Claude | ✅ Đạt | brand.style mới (28/11/2026): phẳng, nét tròn, bóng đổ nhẹ; cảnh (kind scene) vẽ như phong cảnh thật bằng màu tự nhiên; icon, chữ, nút chỉ 4 màu nhận diện. Storyboard có 10 asset scene (A-SONG, A-CUA-SONG, A-BIEN, A-SUOI, A-NEN-MUA, A-DA, A-DAY-BIEN, A-BAN-DO-SONG) và mọi màu nằm trong scene_palette. Icon (cốc, giọt, mây, mũi tên, nút, chuông, A-SONG-ICON) giữ 4 màu nhận diện; khung giải thích (S01-01-b, S01-02-a, S04-03-b, S05) vẫn nền xanh đậm hoặc tối. Chữ trên cảnh có text_plate #1B1B1F 0,75 (DSN-A05 đo với màu sáng nhất của cảnh: đạt). |
| DSN-C06 | Khả năng đọc | Chữ trên màn hình bổ trợ lời, không chép nguyên lời | Nghiêm trọng | Claude | ✅ Đạt | Mọi chữ trên màn hình là từ khoá hoặc nhãn, không chép câu lời. S01-01-b và S01-02-a đã đổi thành "Sông ngọt → Biển mặn?" (nghịch lý dạng ký hiệu, khác câu nói "Muối từ đâu ra?"). Các chữ khác: "axit nhẹ", "muối", "rất ít muối", "nước ngọt mới", "Muối dồn về biển" (rút gọn để đọc kịp ở nhịp giọng thật), "Nước bay đi, muối ở lại", "hàng triệu năm", "Nguồn thêm: đáy biển", "Mưa/Sông/Bốc hơi", "Mỗi tuần một hiện tượng". |
| DSN-C07 | Khả thi | Mọi asset và chuyển động làm được bằng SVG/CSS/Canvas/Lottie | Nghiêm trọng | Claude | ✅ Đạt | Mọi asset vẽ được bằng SVG, đã chứng minh bằng 27 file SVG có thật ở 06_animation (cảnh cũng là vector phẳng, sinh từ code). Hiệu ứng nằm trong tập anim của schema; draw cho A-SUOI chỉ áp vào lớp streams (đã ghi chú), morph giọt, typewriter, zoom xuyên mặt biển đều có ghi chú cách làm. Tấm nền chữ là hình chữ nhật bo góc, Tool 07 vẽ bằng CSS. Không cần 3D hay ảnh chụp. |
| DSN-C08 | Bản quyền | Không phỏng theo nhân vật, logo, tác phẩm có bản quyền | Chặn | Claude | ✅ Đạt | A-NUT-DANG-KY tự thiết kế, không dùng logo YouTube. Các cảnh (núi, cây thông, sông, bãi biển, cây dừa, đá, núi lửa) là phong cảnh chung chung vẽ từ hình học, không phỏng theo tranh, phim hay nhân vật nào; không có người, không có logo. |
| DSN-C09 | Nhịp | Nhịp thị giác — có thay đổi có nghĩa mỗi khoảng 2–4 giây, không khung tĩnh > 5 giây | Nghiêm trọng | Claude | ✅ Đạt | Sau khi rút thời lượng theo giọng thật (tổng ~48,7 giây), khung dài nhất là S04-04-a (~4,6 giây) và S04-01-a (~4,4 giây), đều có phần tử mới hoặc camera chạy bên trong; không khung nào > 5 giây. Đoạn dài vẫn được tách khung. |
| DSN-C10 | Liên tục | Liên tục giữa các khung — cùng đối tượng dùng cùng asset, cùng vị trí logic, hướng chuyển động nhất quán | Nghiêm trọng | Claude | ✅ Đạt | Cùng đối tượng dùng cùng asset: A-SONG ở S03-01-b và S03-02-a; A-DA + A-NEN-MUA ở S02-02-a/b, S02-03-a, S04-03-a; A-BIEN ở S04-01-a và S04-02-a (cùng hộp, nối match_cut); A-MAY và A-COC-BIEN lặp lại. Hướng: cửa sông S01-01-a sông chảy trái → phải ra biển; S02-03 muối trôi phải; suối S03-01-a nhập sông chảy sang phải; ở A-SONG sông chảy từ núi ra phía trước (trung tính, không ngược hướng); S04-02 mây trôi trái về đất liền, rồi S04-03-a mây vào từ phải đổ mưa lên đá. Bố cục trời trên, đất/biển dưới giữ nhất quán ở mọi cảnh. |
