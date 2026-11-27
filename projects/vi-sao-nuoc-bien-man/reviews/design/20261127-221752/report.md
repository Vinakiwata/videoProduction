# Báo cáo kiểm duyệt — Thiết kế nội dung & storyboard

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `design` · checklist "Kiểm duyệt thiết kế nội dung & storyboard" v2
- **Bắt đầu:** 2026-11-27T22:17:52+07:00 · **Chốt:** 2026-11-27T22:17:53+07:00

## Kết luận: ❌ KHÔNG ĐẠT — điểm chất lượng 84/100

19 mục: 16 đạt, 3 trượt, 0 lỗi kiểm tra, 0 không áp dụng.

## ❗ Phải sửa trước khi đi tiếp

### DSN-C02 · [Nghiêm trọng] Mỗi khung có một điểm nhìn chính rõ ràng
- **Hiện trạng:** Xem 18 ảnh phác thảo: 17 khung có điểm nhìn rõ. Riêng S03-02-a (ý "mưa bổ sung nước ngọt nên sông vẫn ngọt") đặt focal là e2 (đám mây), trong khi nội dung cần nhìn là mưa rơi xuống sông (e3); dải sông e1 rộng toàn khung, mây 50%, cả hai cùng tranh chú ý, còn giọt mưa (thứ nối hai bên) lại không được nhấn.
- **Cách sửa:** S03-02-a: đổi focal sang e3 (A-GIOT-MUA). Thu mây e2 còn khoảng 36% chiều rộng, đẩy lên y=4. Cho mưa e3 rơi thành cột rõ xuống đúng giữa dòng sông.

### DSN-C03 · [Chặn] Hình minh hoạ đúng nghĩa lời đọc, không gây hiểu sai
- **Hiện trạng:** Hình khớp nghĩa lời ở hầu hết các khung (vd. S04-01-a: mũi tên hơi nước chỉ mang chấm trắng, muối sáng lên khi nói "muối thì không bay theo"; S04-03-b: cốc biển dừng ở mức hiện nay, đúng NOAA). Nhưng S04-04-a: hình quan trọng nhất của câu ("thả khoáng chất vào nước", khoảng 0.7) chỉ nằm trong notes và trong mô tả asset A-DAY-BIEN, không phải phần tử có enter.at. Tool hoạt ảnh và web trình chiếu sẽ không biết đặt khoảng nào, nên hình có thể không xuất hiện đúng lúc lời nói tới nó.
- **Cách sửa:** Thêm asset A-KHOANG-CHAT (chấm khoáng chất trắng bay lên). Trong S04-04-a thêm phần tử e3 với enter slide_up at 0.7, loop flow, đặt trên miệng núi lửa và khe nứt. Bỏ phần "chấm khoáng chất trắng bay lên" khỏi mô tả A-DAY-BIEN để không vẽ trùng.

### DSN-C06 · [Nghiêm trọng] Chữ trên màn hình bổ trợ lời, không chép nguyên lời
- **Hiện trạng:** Phần lớn chữ là từ khoá ("axit nhẹ", "muối", "rất ít muối", "Nước bay đi, muối ở lại", "Mưa/Sông/Bốc hơi"). Nhưng S01-01-b và S01-02-a có tiêu đề "Muối từ đâu ra?", trùng nguyên văn câu đang nói ở cuối S01-01, nên người xem đọc và nghe cùng một câu.
- **Cách sửa:** Đổi chữ ở S01-01-b và S01-02-a thành từ khoá thể hiện nghịch lý, ví dụ "Sông ngọt → Biển mặn?" (title, 96px, vàng). Giữ nguyên thời điểm và hộp; kiểm lại chữ có tràn hộp không.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `02_design` | `dir:91c5817d4914` |
| `01_script/script.yaml` | `acd0288e8539eda3` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| DSN-A01 | Cấu trúc | Storyboard đúng định dạng chuẩn (schema) | Chặn | auto | ✅ Đạt | 02_design/storyboard.yaml khớp schema 'storyboard'. |
| DSN-A02 | Cấu trúc | Không còn chỗ trống (TODO) | Chặn | auto | ✅ Đạt | 02_design/storyboard.yaml: không còn chỗ trống hay đánh dấu tạm. |
| DSN-A03 | Độ phủ | Mọi đoạn kịch bản được phủ kín bởi khung hình, không hở, không chồng | Chặn | auto | ✅ Đạt | 13 đoạn kịch bản đều được phủ kín bởi 18 khung hình. |
| DSN-A04 | Cấu trúc | Tham chiếu asset / điểm nhìn / tiếng động hợp lệ | Chặn | auto | ✅ Đạt | 18 khung, 22 asset, mọi tham chiếu hợp lệ. |
| DSN-A05 | Khả năng đọc | Tương phản chữ/nền ≥ 4,5:1 | Chặn | auto | ✅ Đạt | 15 phần tử chữ, tương phản thấp nhất 6.96:1 (≥ 4.5:1). |
| DSN-A06 | Nhận diện | Mọi màu thuộc bảng màu nhận diện của brief | Nghiêm trọng | auto | ✅ Đạt | Mọi màu thuộc bảng màu nhận diện (4 màu). |
| DSN-A07 | Khả năng đọc | Chữ đủ lớn, ≤ 7 từ/dòng, hiển thị đủ lâu để đọc | Nghiêm trọng | auto | ✅ Đạt | 15 phần tử chữ: đủ cỡ, ≤ 7 từ/dòng, đủ thời gian đọc. |
| DSN-A08 | Bố cục | Chữ trong vùng an toàn 5%, hình không tràn quá 10% | Nghiêm trọng | auto | ✅ Đạt | Chữ trong vùng an toàn 5%, hình không tràn quá 10%. |
| DSN-A09 | Âm thanh | Tiếng động không dày quá 5 cái mỗi 10 giây | Nhẹ | auto | ✅ Đạt | 6 tiếng động, dày nhất 2 trong 10 giây (tối đa 5). |
| DSN-A10 | Cấu trúc | Ảnh phác thảo khớp storyboard hiện tại | Nhẹ | auto | ✅ Đạt | 18 ảnh phác thảo khớp storyboard hiện tại. |
| DSN-C02 | Truyền đạt | Mỗi khung có một điểm nhìn chính rõ ràng | Nghiêm trọng | Claude | ❌ Trượt | Xem 18 ảnh phác thảo: 17 khung có điểm nhìn rõ. Riêng S03-02-a (ý "mưa bổ sung nước ngọt nên sông vẫn ngọt") đặt focal là e2 (đám mây), trong khi nội dung cần nhìn là mưa rơi xuống sông (e3); dải sông e1 rộng toàn khung, mây 50%, cả hai cùng tranh chú ý, còn giọt mưa (thứ nối hai bên) lại không được nhấn. |
| DSN-C03 | Truyền đạt | Hình minh hoạ đúng nghĩa lời đọc, không gây hiểu sai | Chặn | Claude | ❌ Trượt | Hình khớp nghĩa lời ở hầu hết các khung (vd. S04-01-a: mũi tên hơi nước chỉ mang chấm trắng, muối sáng lên khi nói "muối thì không bay theo"; S04-03-b: cốc biển dừng ở mức hiện nay, đúng NOAA). Nhưng S04-04-a: hình quan trọng nhất của câu ("thả khoáng chất vào nước", khoảng 0.7) chỉ nằm trong notes và trong mô tả asset A-DAY-BIEN, không phải phần tử có enter.at. Tool hoạt ảnh và web trình chiếu sẽ không biết đặt khoảng nào, nên hình có thể không xuất hiện đúng lúc lời nói tới nó. |
| DSN-C04 | Nhịp | Điểm rơi và tiếng động đặt đúng khoảnh khắc có nghĩa | Nghiêm trọng | Claude | ✅ Đạt | 6 tiếng động, mỗi cái gắn với một hành động có nghĩa: pop ← dấu hỏi bật (S01-01-b); lách tách ← hạt bong khỏi đá (S02-02-b); róc rách ← muối trôi (S02-03); pop nhẹ ← mây hình thành (S04-01-a, rơi đúng chữ "thành mây", củng cố từ đó chứ không che, vì là tiếng nhẹ dưới giọng); whoosh ← mây trôi đi trong đoạn im lặng S04-02; click ← nút đăng ký. Dày nhất 1–2 cái mỗi 10 giây. |
| DSN-C05 | Nhận diện | Phong cách hình đúng brand.style | Nghiêm trọng | Claude | ✅ Đạt | brand.style là "flat, nét tròn, bóng đổ nhẹ, ≤ 4 màu mỗi khung". 22 asset đều mô tả hình phẳng bo tròn, mỗi asset 1–4 màu thuộc palette. Có quy ước màu xuyên suốt ghi ở đầu file (biển/trời xanh đậm, đất tối, nước/muối trắng, nhấn vàng). Mỗi khung dùng tối đa 4 màu (vd. S04-04-a: xanh, tối, vàng, trắng). |
| DSN-C06 | Khả năng đọc | Chữ trên màn hình bổ trợ lời, không chép nguyên lời | Nghiêm trọng | Claude | ❌ Trượt | Phần lớn chữ là từ khoá ("axit nhẹ", "muối", "rất ít muối", "Nước bay đi, muối ở lại", "Mưa/Sông/Bốc hơi"). Nhưng S01-01-b và S01-02-a có tiêu đề "Muối từ đâu ra?", trùng nguyên văn câu đang nói ở cuối S01-01, nên người xem đọc và nghe cùng một câu. |
| DSN-C07 | Khả thi | Mọi asset và chuyển động làm được bằng SVG/CSS/Canvas/Lottie | Nghiêm trọng | Claude | ✅ Đạt | Mọi asset là hình phẳng vẽ được bằng SVG: cốc, giọt, mây, đá, sông, bản đồ, mặt cắt đáy biển, nút. Các hiệu ứng nằm trong tập anim của schema. Hiệu ứng phức tạp có ghi chú cách làm: morph giọt trắng → giọt viền vàng (S02-01-a), typewriter "hàng triệu năm" (S04-03-b), zoom xuyên mặt biển (S01-01-b). Không cần 3D hay ảnh chụp. |
| DSN-C08 | Bản quyền | Không phỏng theo nhân vật, logo, tác phẩm có bản quyền | Chặn | Claude | ✅ Đạt | A-NUT-DANG-KY ghi rõ "tự thiết kế — không dùng logo YouTube". Không nhân vật, không logo, không phỏng theo tác phẩm nào. Mọi asset là hình học cơ bản. |
| DSN-C09 | Nhịp | Nhịp thị giác — có thay đổi có nghĩa mỗi khoảng 2–4 giây, không khung tĩnh > 5 giây | Nghiêm trọng | Claude | ✅ Đạt | Khung dài nhất S04-04-a (6,3s) có chữ vào ở 0.1, camera zoom_in suốt khung, nhịp sáng của núi lửa. S04-03-b (5,9s) có vòng tuần hoàn xoay, chữ gõ ở 0.15, cốc biển vào ở 0.6, camera lùi. Các khung khác ≤ 5s hoặc có phần tử mới trong 2–4 giây. Đoạn dài được tách khung (S01-01, S02-02, S03-01, S03-02, S04-03). |
| DSN-C10 | Liên tục | Liên tục giữa các khung — cùng đối tượng dùng cùng asset, cùng vị trí logic, hướng chuyển động nhất quán | Nghiêm trọng | Claude | ✅ Đạt | Quy ước hướng trái → phải giữ suốt: S01-01-a sông trái, biển phải; S02-03 muối trôi sang phải; S04-02 mây trôi sang trái về đất liền rồi S04-03-a mây vào từ phải đổ mưa lên đá. Cùng đối tượng dùng cùng asset (A-SONG, A-MAY, A-DA, A-COC-BIEN lặp lại ở S04-03-b). Khung giống nhau S01-01-b → S01-02-a có ghi chú "nối tiếp liền mạch" với match_cut, có lý do. |
