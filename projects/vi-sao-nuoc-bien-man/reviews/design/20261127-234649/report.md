# Báo cáo kiểm duyệt — Thiết kế nội dung & storyboard

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `design` · checklist "Kiểm duyệt thiết kế nội dung & storyboard" v2
- **Bắt đầu:** 2026-11-27T23:46:49+07:00 · **Chốt:** 2026-11-27T23:46:50+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

19 mục: 19 đạt, 0 trượt, 0 lỗi kiểm tra, 0 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `02_design` | `dir:169b5fc46f47` |
| `01_script/script.yaml` | `f1e243f1430c98b5` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| DSN-A01 | Cấu trúc | Storyboard đúng định dạng chuẩn (schema) | Chặn | auto | ✅ Đạt | 02_design/storyboard.yaml khớp schema 'storyboard'. |
| DSN-A02 | Cấu trúc | Không còn chỗ trống (TODO) | Chặn | auto | ✅ Đạt | 02_design/storyboard.yaml: không còn chỗ trống hay đánh dấu tạm. |
| DSN-A03 | Độ phủ | Mọi đoạn kịch bản được phủ kín bởi khung hình, không hở, không chồng | Chặn | auto | ✅ Đạt | 13 đoạn kịch bản đều được phủ kín bởi 18 khung hình. |
| DSN-A04 | Cấu trúc | Tham chiếu asset / điểm nhìn / tiếng động hợp lệ | Chặn | auto | ✅ Đạt | 18 khung, 23 asset, mọi tham chiếu hợp lệ. |
| DSN-A05 | Khả năng đọc | Tương phản chữ/nền ≥ 4,5:1 | Chặn | auto | ✅ Đạt | 15 phần tử chữ, tương phản thấp nhất 6.96:1 (≥ 4.5:1). |
| DSN-A06 | Nhận diện | Mọi màu thuộc bảng màu nhận diện của brief | Nghiêm trọng | auto | ✅ Đạt | Mọi màu thuộc bảng màu nhận diện (4 màu). |
| DSN-A07 | Khả năng đọc | Chữ đủ lớn, ≤ 7 từ/dòng, hiển thị đủ lâu để đọc | Nghiêm trọng | auto | ✅ Đạt | 15 phần tử chữ: đủ cỡ, ≤ 7 từ/dòng, đủ thời gian đọc. |
| DSN-A08 | Bố cục | Chữ trong vùng an toàn 5%, hình không tràn quá 10% | Nghiêm trọng | auto | ✅ Đạt | Chữ trong vùng an toàn 5%, hình không tràn quá 10%. |
| DSN-A09 | Âm thanh | Tiếng động không dày quá 5 cái mỗi 10 giây | Nhẹ | auto | ✅ Đạt | 6 tiếng động, dày nhất 2 trong 10 giây (tối đa 5). |
| DSN-A10 | Cấu trúc | Ảnh phác thảo khớp storyboard hiện tại | Nhẹ | auto | ✅ Đạt | 18 ảnh phác thảo khớp storyboard hiện tại. |
| DSN-C02 | Truyền đạt | Mỗi khung có một điểm nhìn chính rõ ràng | Nghiêm trọng | Claude | ✅ Đạt | Xem lại 18 ảnh: mỗi khung có một focal được viền vàng. S03-02-a đã sửa: focal là e3 (cột mưa 24%×34% rơi đúng giữa sông), mây thu còn 36% chiều rộng ở trên cùng, sông hạ xuống y=55. Mắt đi từ mây theo cột mưa xuống sông, không còn hai khối tranh nhau. |
| DSN-C03 | Truyền đạt | Hình minh hoạ đúng nghĩa lời đọc, không gây hiểu sai | Chặn | Claude | ✅ Đạt | Hình khớp nghĩa và đúng lúc ở mọi khung. S04-04-a đã thêm e3 A-KHOANG-CHAT với enter slide_up at 0.7, khớp chữ "thả khoáng chất vào nước" (âm tiết 15–20 trên 20 ≈ 0.7). Mô tả A-DAY-BIEN đã bỏ phần khoáng chất để không vẽ trùng. Đã kiểm lại các khung khoa học: hơi nước không mang muối (S04-01-a), cốc biển dừng ở mức hiện nay (S04-03-b, đúng NOAA). Đã kiểm lại mốc chữ sau khi giọng nhanh hơn: các nhãn đưa lên sớm 0,06–0,08 (vd. "axit nhẹ" 0.56, "muối" 0.6) — vẫn ngay trước/đúng lúc từ khoá được nói, không đến sau lời. |
| DSN-C04 | Nhịp | Điểm rơi và tiếng động đặt đúng khoảnh khắc có nghĩa | Nghiêm trọng | Claude | ✅ Đạt | 6 tiếng động, mỗi cái gắn với một hành động có nghĩa: pop ← dấu hỏi bật (S01-01-b); lách tách ← hạt bong khỏi đá (S02-02-b); róc rách ← muối trôi (S02-03); pop nhẹ ← mây hình thành (S04-01-a, rơi đúng chữ "thành mây", củng cố từ đó chứ không che, vì là tiếng nhẹ dưới giọng); whoosh ← mây trôi đi trong đoạn im lặng S04-02; click ← nút đăng ký. Dày nhất 1–2 cái mỗi 10 giây. |
| DSN-C05 | Nhận diện | Phong cách hình đúng brand.style | Nghiêm trọng | Claude | ✅ Đạt | brand.style là "flat, nét tròn, bóng đổ nhẹ, ≤ 4 màu mỗi khung". 22 asset đều mô tả hình phẳng bo tròn, mỗi asset 1–4 màu thuộc palette. Có quy ước màu xuyên suốt ghi ở đầu file (biển/trời xanh đậm, đất tối, nước/muối trắng, nhấn vàng). Mỗi khung dùng tối đa 4 màu (vd. S04-04-a: xanh, tối, vàng, trắng). |
| DSN-C06 | Khả năng đọc | Chữ trên màn hình bổ trợ lời, không chép nguyên lời | Nghiêm trọng | Claude | ✅ Đạt | Mọi chữ trên màn hình là từ khoá hoặc nhãn, không chép câu lời. S01-01-b và S01-02-a đã đổi thành "Sông ngọt → Biển mặn?" (nghịch lý dạng ký hiệu, khác câu nói "Muối từ đâu ra?"). Các chữ khác: "axit nhẹ", "muối", "rất ít muối", "nước ngọt mới", "Muối dồn về biển" (rút gọn để đọc kịp ở nhịp giọng thật), "Nước bay đi, muối ở lại", "hàng triệu năm", "Nguồn thêm: đáy biển", "Mưa/Sông/Bốc hơi", "Mỗi tuần một hiện tượng". |
| DSN-C07 | Khả thi | Mọi asset và chuyển động làm được bằng SVG/CSS/Canvas/Lottie | Nghiêm trọng | Claude | ✅ Đạt | Mọi asset là hình phẳng vẽ được bằng SVG: cốc, giọt, mây, đá, sông, bản đồ, mặt cắt đáy biển, nút. Các hiệu ứng nằm trong tập anim của schema. Hiệu ứng phức tạp có ghi chú cách làm: morph giọt trắng → giọt viền vàng (S02-01-a), typewriter "hàng triệu năm" (S04-03-b), zoom xuyên mặt biển (S01-01-b). Không cần 3D hay ảnh chụp. |
| DSN-C08 | Bản quyền | Không phỏng theo nhân vật, logo, tác phẩm có bản quyền | Chặn | Claude | ✅ Đạt | A-NUT-DANG-KY ghi rõ "tự thiết kế — không dùng logo YouTube". Không nhân vật, không logo, không phỏng theo tác phẩm nào. Mọi asset là hình học cơ bản. |
| DSN-C09 | Nhịp | Nhịp thị giác — có thay đổi có nghĩa mỗi khoảng 2–4 giây, không khung tĩnh > 5 giây | Nghiêm trọng | Claude | ✅ Đạt | Sau khi rút thời lượng theo giọng thật (tổng ~48,7 giây), khung dài nhất là S04-04-a (~4,6 giây) và S04-01-a (~4,4 giây), đều có phần tử mới hoặc camera chạy bên trong; không khung nào > 5 giây. Đoạn dài vẫn được tách khung. |
| DSN-C10 | Liên tục | Liên tục giữa các khung — cùng đối tượng dùng cùng asset, cùng vị trí logic, hướng chuyển động nhất quán | Nghiêm trọng | Claude | ✅ Đạt | Quy ước hướng trái → phải giữ suốt: S01-01-a sông trái, biển phải; S02-03 muối trôi sang phải; S04-02 mây trôi sang trái về đất liền rồi S04-03-a mây vào từ phải đổ mưa lên đá. Cùng đối tượng dùng cùng asset (A-SONG, A-MAY, A-DA, A-COC-BIEN lặp lại ở S04-03-b). Khung giống nhau S01-01-b → S01-02-a có ghi chú "nối tiếp liền mạch" với match_cut, có lý do. |
