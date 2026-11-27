# Báo cáo kiểm duyệt — Kịch bản

- **Dự án:** vi-du-bau-troi-xanh
- **Công đoạn:** `script` · checklist "Kiểm duyệt kịch bản" v1
- **Bắt đầu:** 2026-11-27T21:31:52+07:00 · **Chốt:** 2026-11-27T21:32:35+07:00

## Kết luận: ❌ KHÔNG ĐẠT — điểm chất lượng 87/100

30 mục: 22 đạt, 5 trượt, 0 lỗi kiểm tra, 3 không áp dụng.

## ❗ Phải sửa trước khi đi tiếp

### SCR-Q01 · [Chặn] Khớp brief (mục tiêu, khán giả, giọng điệu, CTA)
- **Hiện trạng:** Mục tiêu, khán giả, giọng điệu khớp brief. Nhưng brief.cta = "Đăng ký kênh để xem thêm hiện tượng khoa học", còn kịch bản KHÔNG có lời kêu gọi đăng ký: đoạn cuối S03-01 chỉ là câu cảm xúc. Thiếu CTA đã yêu cầu.
- **Cách sửa:** Thêm một đoạn giọng sau S03-01, ví dụ S03-02: "Đăng ký kênh để cùng khám phá thêm những hiện tượng khoa học quanh ta nhé!" (khoảng 4 giây), visual nút đăng ký bật lên theo màu brand #FFD23F. Cập nhật lại tổng thời lượng.

### SCR-Q04 · [Nghiêm trọng] Đúng trình độ khán giả, thuật ngữ được giải thích
- **Hiện trạng:** Thuật ngữ "bước sóng" xuất hiện ở S02-01 và là mấu chốt của lời giải thích (S02-02 "bước sóng ngắn"), nhưng không được giải thích bằng lời hay bằng hình (visual S02-01 chỉ là "tia sáng trắng tách thành dải cầu vồng"). Người lớn tò mò hoặc học sinh lớp dưới có thể không hiểu "ngắn" nghĩa là gì. "Tán xạ" cũng chưa được hình dung hoá rõ.
- **Cách sửa:** S02-01: đổi visual thành dải màu tách ra kèm các đường sóng có độ dài khác nhau (đỏ: sóng dài, thưa; xanh: sóng ngắn, dày), nhãn chữ "bước sóng". S02-02: visual chỉ rõ tia xanh dội lệch nhiều lần còn tia đỏ đi gần thẳng. Có thể thêm cụm "tức là bị bật tung ra mọi hướng" sau "tán xạ".

### SCR-D01 · [Nghiêm trọng] Mô tả hình ảnh đủ cụ thể để thiết kế 2D
- **Hiện trạng:** Phần lớn visual đủ cụ thể. Nhưng S03-01 "Nhân vật ngước nhìn trời, mỉm cười" đưa vào một nhân vật chưa từng xuất hiện và chưa mô tả (ai, phong cách). S02-02 "Tia xanh dội lung tung giữa các phân tử" chưa nói người xem cần nhận ra gì (so sánh với tia đỏ).
- **Cách sửa:** S03-01: mô tả nhân vật (ví dụ "bạn nhỏ hoạt hình phong cách phẳng, áo màu brand #FFD23F, đứng trên đồi cỏ") hoặc thay bằng hình đã có từ trước. S02-02: thêm "đặt cạnh tia đỏ đi gần như thẳng để người xem thấy xanh bị dội nhiều hơn".

## Nên cải thiện (không chặn cổng)

- **SCR-Q05 Kết thúc có chốt ý và CTA tự nhiên:** S03-01 kết bằng hình ảnh thơ ("ánh sáng đang nhảy múa quanh bạn") nhưng không nhắc lại ý chính trong một câu, và không có CTA (xem SCR-Q01). → Trước câu thơ, thêm một câu chốt ngắn: "Tóm lại: ánh sáng xanh bị không khí tán xạ mạnh nhất, nên phủ kín bầu trời." Sau đó là CTA ở S03-02.
- **SCR-Q06 Nhịp độ có điểm nghỉ (đoạn im lặng/điểm rơi) hợp lý:** Ba đoạn giọng dày thông tin S02-01 (6s), S02-02 (7s), S02-03 (6s) liền nhau, tổng 19 giây không có khoảng nghỉ. Chính guidance của mục này nêu đúng trường hợp đó. → Chèn một đoạn silent khoảng 1 giây sau S02-02 (đoạn khó nhất) để hoạt ảnh tia xanh dội ra mọi hướng diễn xong, kèm SFX nhẹ.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `01_script/script.yaml` | `c2a21c843fe060ba` |
| `00_brief/brief.yaml` | `181f27a16079b863` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| SCR-A01 | Cấu trúc | Kịch bản đúng định dạng chuẩn (schema) | Chặn | auto | ✅ Đạt | 01_script/script.yaml khớp schema 'script'. |
| SCR-A02 | Cấu trúc | Mã cảnh/đoạn không trùng | Chặn | auto | ✅ Đạt | 9 mã cảnh/đoạn, không trùng. |
| SCR-A03 | Cấu trúc | Mọi trích dẫn trỏ tới nguồn có thật trong danh sách | Chặn | auto | ✅ Đạt | 1 nguồn, 2 đoạn có trích nguồn, mọi tham chiếu hợp lệ. |
| SCR-A04 | Cấu trúc | Không còn chỗ trống / đánh dấu tạm (TODO, ???, [..]) | Chặn | auto | ✅ Đạt | Không còn chỗ trống hay đánh dấu tạm. |
| SCR-A05 | Cấu trúc | Mỗi đoạn giọng ≤ 300 ký tự | Nghiêm trọng | auto | ✅ Đạt | Mọi đoạn giọng ≤ 300 ký tự. |
| SCR-A06 | Cấu trúc | Tốc độ đọc tự nhiên (2,5–4,0 âm tiết/giây) | Nghiêm trọng | auto | ✅ Đạt | 5 đoạn giọng, tốc độ 2.50–3.75 âm tiết/giây. |
| SCR-A07 | Cấu trúc | Tổng thời lượng ước tính khớp mục tiêu (±15%) | Nghiêm trọng | auto | ✅ Đạt | Tổng ước tính 29s so với mục tiêu 30s (lệch 3%, cho phép 15%). |
| SCR-F01 | Sự thật & nguồn | Mọi khẳng định sự thật đều đúng | Chặn | Claude | ✅ Đạt | Có 3 khẳng định kiểm chứng được: (1) S02-01 ánh sáng Mặt Trời gồm nhiều màu, mỗi màu một bước sóng; (2) S02-02 ánh sáng xanh bước sóng ngắn bị phân tử khí tán xạ mạnh hơn; (3) S02-03 vì vậy trời trông xanh. Đã đối chiếu NASA Space Place (spaceplace.nasa.gov/blue-sky, tra 2026-11-27): trang nêu đúng cả 3 ý. "Mạnh hơn nhiều" khớp tán xạ Rayleigh tỉ lệ 1/λ⁴ (xanh 450 nm mạnh gấp khoảng 6 lần đỏ 700 nm). |
| SCR-F02 | Sự thật & nguồn | Khẳng định quan trọng có nguồn ghi trong kịch bản | Nghiêm trọng | Claude | ✅ Đạt | Hai khẳng định cốt lõi S02-02 và S02-03 có source_ids [SRC1], và nguồn thực sự nói điều đó. S02-01 (ánh sáng trắng gồm nhiều màu) là kiến thức phổ thông, không bắt buộc nguồn; cùng nguồn SRC1 cũng xác nhận. |
| SCR-F03 | Sự thật & nguồn | Không đơn giản hoá tới mức sai bản chất | Nghiêm trọng | Claude | ✅ Đạt | Kịch bản bỏ qua chi tiết ánh sáng tím còn bị tán xạ mạnh hơn xanh (mắt người nhạy với xanh hơn, Mặt Trời phát ít tím hơn). Đây là đơn giản hoá được phép: không có câu nào khẳng định sai, không tạo hiểu lầm cho khán giả trung học. |
| SCR-L01 | Pháp luật | Không có nội dung bị cấm trên không gian mạng | Chặn | Claude | ✅ Đạt | Đối chiếu nhóm nội dung cấm theo Luật An ninh mạng 116/2025/QH15: kịch bản chỉ có nội dung khoa học phổ thông, không có yếu tố chính trị, tôn giáo, bạo lực, đồi truỵ, xúc phạm hay vu khống. |
| SCR-L02 | Pháp luật | Không thông tin sai sự thật, giả mạo về cá nhân/tổ chức/sự kiện có thật | Chặn | Claude | ✅ Đạt | Không nhắc tới cá nhân hay tổ chức có thật nào trong lời đọc (NASA chỉ có trong danh sách nguồn). Không có sự kiện thời sự. Mọi thông tin khoa học đã kiểm ở SCR-F01. |
| SCR-L03 | Pháp luật | Nếu có quảng cáo/tài trợ — tuân thủ Luật Quảng cáo | Chặn | Claude | ➖ Không áp dụng | brief.is_advertising = false. Kịch bản không nhắc sản phẩm, dịch vụ hay thương hiệu nào nên không thuộc phạm vi Luật Quảng cáo. |
| SCR-L04 | Pháp luật | Không xâm phạm đời tư, hình ảnh, dữ liệu cá nhân | Chặn | Claude | ✅ Đạt | Không có tên, hình ảnh hay dữ liệu của người thật. S03-01 có một "nhân vật" nhưng là nhân vật hoạt hình chưa định danh, không phải người thật. |
| SCR-L05 | Pháp luật | Nội dung chuyên môn nhạy cảm (y tế, pháp lý, tài chính) có giới hạn trách nhiệm | Nghiêm trọng | Claude | ➖ Không áp dụng | Video thuần khoa học vật lý phổ thông. Không có lời khuyên y tế, pháp lý hay tài chính. |
| SCR-P01 | Nền tảng | Không vi phạm Nguyên tắc cộng đồng YouTube | Chặn | Claude | ✅ Đạt | Không có nội dung nguy hiểm, quấy rối, thù ghét hay thông tin y tế. Nội dung phù hợp mọi lứa tuổi, kể cả khi bị coi là dành cho trẻ em. |
| SCR-P02 | Nền tảng | Không dùng tác phẩm có bản quyền của người khác | Chặn | Claude | ✅ Đạt | Không trích lời bài hát, thơ hay văn bản dài. Các visual (bầu trời, dấu chấm hỏi, dải cầu vồng, phân tử, nhân vật) đều là mô tả chung, không yêu cầu nhân vật hay logo có bản quyền. |
| SCR-P03 | Nền tảng | Tiêu đề/nội dung không câu view sai sự thật | Nghiêm trọng | Claude | ✅ Đạt | Câu hỏi mở đầu S01-01 ("vì sao bầu trời lại có màu xanh") được trả lời đầy đủ ở S02-02 và S02-03. Không phóng đại. |
| SCR-Q01 | Chất lượng | Khớp brief (mục tiêu, khán giả, giọng điệu, CTA) | Chặn | Claude | ❌ Trượt | Mục tiêu, khán giả, giọng điệu khớp brief. Nhưng brief.cta = "Đăng ký kênh để xem thêm hiện tượng khoa học", còn kịch bản KHÔNG có lời kêu gọi đăng ký: đoạn cuối S03-01 chỉ là câu cảm xúc. Thiếu CTA đã yêu cầu. |
| SCR-Q02 | Chất lượng | Mở đầu giữ chân người xem trong 5 giây đầu | Nghiêm trọng | Claude | ✅ Đạt | S01-01 bắt đầu ngay giây 0 bằng câu hỏi gợi tò mò, visual dấu chấm hỏi bật ra. Không chào hỏi, không giới thiệu kênh trước. |
| SCR-Q03 | Chất lượng | Mạch logic rõ — mỗi cảnh một ý, chuyển ý có cầu nối | Nghiêm trọng | Claude | ✅ Đạt | Tóm được mỗi cảnh một câu: S01 đặt câu hỏi; S02 ánh sáng gồm nhiều màu → xanh tán xạ mạnh → trời xanh; S03 chốt. Cầu nối rõ: "Khi đi qua khí quyển", "nên". Không trùng ý, không nhảy cóc. |
| SCR-Q04 | Chất lượng | Đúng trình độ khán giả, thuật ngữ được giải thích | Nghiêm trọng | Claude | ❌ Trượt | Thuật ngữ "bước sóng" xuất hiện ở S02-01 và là mấu chốt của lời giải thích (S02-02 "bước sóng ngắn"), nhưng không được giải thích bằng lời hay bằng hình (visual S02-01 chỉ là "tia sáng trắng tách thành dải cầu vồng"). Người lớn tò mò hoặc học sinh lớp dưới có thể không hiểu "ngắn" nghĩa là gì. "Tán xạ" cũng chưa được hình dung hoá rõ. |
| SCR-Q05 | Chất lượng | Kết thúc có chốt ý và CTA tự nhiên | Nhẹ | Claude | ❌ Trượt | S03-01 kết bằng hình ảnh thơ ("ánh sáng đang nhảy múa quanh bạn") nhưng không nhắc lại ý chính trong một câu, và không có CTA (xem SCR-Q01). |
| SCR-Q06 | Chất lượng | Nhịp độ có điểm nghỉ (đoạn im lặng/điểm rơi) hợp lý | Nhẹ | Claude | ❌ Trượt | Ba đoạn giọng dày thông tin S02-01 (6s), S02-02 (7s), S02-03 (6s) liền nhau, tổng 19 giây không có khoảng nghỉ. Chính guidance của mục này nêu đúng trường hợp đó. |
| SCR-V01 | Ngôn ngữ | Chính tả, dấu tiếng Việt, ngữ pháp đúng | Chặn | Claude | ✅ Đạt | Đã đọc 5 đoạn giọng S01-01, S02-01, S02-02, S02-03, S03-01: không lỗi chính tả, dấu đúng (vd. "tán xạ", "khí quyển", "phân tử"), câu đủ thành phần. |
| SCR-V02 | Ngôn ngữ | Văn nói tự nhiên — viết để nghe, không phải để đọc | Nghiêm trọng | Claude | ✅ Đạt | Câu dài nhất S02-02 có 23 âm tiết (≤ 25), có dấu phẩy ngắt nhịp. Không có ký hiệu trong lời đọc. Đọc thành tiếng trôi chảy. |
| SCR-V03 | Ngôn ngữ | Số, viết tắt, từ nước ngoài có cách đọc rõ cho TTS | Nghiêm trọng | Claude | ✅ Đạt | Lời đọc không có số, đơn vị, viết tắt hay từ nước ngoài. "NASA" chỉ nằm trong danh sách nguồn, không được đọc. "Mặt Trời" là từ tiếng Việt. |
| SCR-V04 | Ngôn ngữ | Thẻ cảm xúc dùng đúng chỗ, không lạm dụng | Nhẹ | Claude | ➖ Không áp dụng | Kịch bản không dùng thẻ cảm xúc [cười] / [thở dài] / [hắng giọng] nào. |
| SCR-D01 | Khả năng sản xuất | Mô tả hình ảnh đủ cụ thể để thiết kế 2D | Nghiêm trọng | Claude | ❌ Trượt | Phần lớn visual đủ cụ thể. Nhưng S03-01 "Nhân vật ngước nhìn trời, mỉm cười" đưa vào một nhân vật chưa từng xuất hiện và chưa mô tả (ai, phong cách). S02-02 "Tia xanh dội lung tung giữa các phân tử" chưa nói người xem cần nhận ra gì (so sánh với tia đỏ). |
| SCR-D02 | Khả năng sản xuất | Hình ảnh khả thi bằng hoạt ảnh 2D vector, không cần quay thật | Nghiêm trọng | Claude | ✅ Đạt | Mọi cảnh (bầu trời, dấu chấm hỏi, dải màu, phân tử, tia sáng, nhân vật hoạt hình) đều vẽ được bằng 2D vector. Không yêu cầu quay thật hay ảnh chụp. |
