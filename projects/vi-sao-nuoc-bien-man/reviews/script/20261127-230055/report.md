# Báo cáo kiểm duyệt — Kịch bản

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `script` · checklist "Kiểm duyệt kịch bản" v3
- **Bắt đầu:** 2026-11-27T23:00:55+07:00 · **Chốt:** 2026-11-27T23:00:56+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

31 mục: 28 đạt, 0 trượt, 0 lỗi kiểm tra, 3 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `01_script/script.yaml` | `a4b83bc98b2b13a6` |
| `00_brief/brief.yaml` | `e9f680f5cf7a49eb` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| SCR-A01 | Cấu trúc | Kịch bản đúng định dạng chuẩn (schema) | Chặn | auto | ✅ Đạt | 01_script/script.yaml khớp schema 'script'. |
| SCR-A02 | Cấu trúc | Mã cảnh/đoạn không trùng | Chặn | auto | ✅ Đạt | 18 mã cảnh/đoạn, không trùng. |
| SCR-A03 | Cấu trúc | Mọi trích dẫn trỏ tới nguồn có thật trong danh sách | Chặn | auto | ✅ Đạt | 5 nguồn, 7 đoạn có trích nguồn, mọi tham chiếu hợp lệ. |
| SCR-A04 | Cấu trúc | Không còn chỗ trống / đánh dấu tạm (TODO, ???, [..]) | Chặn | auto | ✅ Đạt | 01_script/script.yaml: không còn chỗ trống hay đánh dấu tạm. |
| SCR-A05 | Cấu trúc | Mỗi đoạn giọng ≤ 300 ký tự | Nghiêm trọng | auto | ✅ Đạt | Mọi đoạn giọng ≤ 300 ký tự. |
| SCR-A06 | Cấu trúc | Tốc độ đọc trong dải chấp nhận (2,5–5,0 âm tiết/giây) | Nghiêm trọng | auto | ✅ Đạt | 10 đoạn giọng, tốc độ 4.32–4.42 âm tiết/giây. |
| SCR-A07 | Cấu trúc | Tổng thời lượng ước tính khớp mục tiêu (±15%) | Nghiêm trọng | auto | ✅ Đạt | Tổng ước tính 48.7s so với mục tiêu 50s (lệch 3%, cho phép 15%). |
| SCR-A08 | Cấu trúc | Bản đọc script.md khớp script.yaml | Nhẹ | auto | ✅ Đạt | 01_script/script.md khớp 01_script/script.yaml. |
| SCR-F01 | Sự thật & nguồn | Mọi khẳng định sự thật đều đúng | Chặn | Claude | ✅ Đạt | Kiểm 8 khẳng định, đối chiếu research.md và kết quả tra web 2026-11-27. S02-01 mưa hoà tan CO₂ thành axit yếu (USGS, Britannica). S02-02 mưa bào mòn đá, hoà tan muối khoáng (USGS). S03-01 sông có muối nhưng rất ít (USGS, NOAA). S03-02 mưa bổ sung nước ngọt cho sông, biển gom muối mọi sông (NOAA riversnotsalty). S04-01 nước bốc hơi, muối ở lại (Britannica). S04-03 hàng triệu năm, độ mặn "như hôm nay" (NMSF; dùng thì quá khứ, khớp NOAA: nay biển không mặn thêm). S04-04 núi lửa và khe nhiệt dịch đáy biển (NOAA whysalty, USGS). Không có khẳng định sai. |
| SCR-F02 | Sự thật & nguồn | Khẳng định quan trọng có nguồn ghi trong kịch bản | Nghiêm trọng | Claude | ✅ Đạt | Mọi đoạn có khẳng định khoa học (S02-01, S02-02, S03-01, S03-02, S04-01, S04-03, S04-04) đều có source_ids, mỗi nguồn hỗ trợ đúng nội dung như ghi ở research.md (K1–K7). S01-01 (sông ngọt, biển mặn) là kiến thức phổ thông. S05-01 chỉ tóm lại các ý đã có nguồn. |
| SCR-F03 | Sự thật & nguồn | Không đơn giản hoá tới mức sai bản chất | Nghiêm trọng | Claude | ✅ Đạt | Dùng "muối" thay cho "các ion hoà tan", và bỏ chi tiết sinh vật biển dùng bớt một số ion (research.md có ghi lý do lược). Đây là đơn giản hoá được phép. Đã tránh lỗi phổ biến "biển đang mặn thêm" bằng S04-03 "tích dần đến độ mặn như hôm nay". |
| SCR-L01 | Pháp luật | Không có nội dung bị cấm trên không gian mạng | Chặn | Claude | ✅ Đạt | Đối chiếu nhóm nội dung cấm theo Luật An ninh mạng 116/2025/QH15: chỉ có nội dung địa chất, hải dương học phổ thông. Không có yếu tố chính trị, tôn giáo, bạo lực, xúc phạm. |
| SCR-L02 | Pháp luật | Không thông tin sai sự thật, giả mạo về cá nhân/tổ chức/sự kiện có thật | Chặn | Claude | ✅ Đạt | Lời đọc không nhắc cá nhân, tổ chức hay sự kiện có thật nào. Các cơ quan (USGS, NOAA, Britannica, NMSF) chỉ có trong danh sách nguồn. |
| SCR-L03 | Pháp luật | Nếu có quảng cáo/tài trợ — tuân thủ Luật Quảng cáo | Chặn | Claude | ➖ Không áp dụng | brief.is_advertising = false. Kịch bản không giới thiệu sản phẩm, dịch vụ hay thương hiệu nào. CTA chỉ mời đăng ký kênh của chính mình. |
| SCR-L04 | Pháp luật | Không xâm phạm đời tư, hình ảnh, dữ liệu cá nhân | Chặn | Claude | ✅ Đạt | Không có tên, hình ảnh hay dữ liệu người thật. Visual chỉ gồm sông, biển, đá, mây, núi lửa, nút bấm. |
| SCR-L05 | Pháp luật | Nội dung chuyên môn nhạy cảm (y tế, pháp lý, tài chính) có giới hạn trách nhiệm | Nghiêm trọng | Claude | ➖ Không áp dụng | Nội dung khoa học tự nhiên, không có lời khuyên y tế, pháp lý hay tài chính. |
| SCR-P01 | Nền tảng | Không vi phạm Nguyên tắc cộng đồng YouTube | Chặn | Claude | ✅ Đạt | Không có nội dung nguy hiểm. Không khuyến khích uống nước biển (S01-01 chỉ nói "mặn chát"). Phù hợp mọi lứa tuổi. |
| SCR-P02 | Nền tảng | Không dùng tác phẩm có bản quyền của người khác | Chặn | Claude | ✅ Đạt | Không trích tác phẩm nào. S05-02 dùng "nút đăng ký tự thiết kế" theo màu brand, không dùng logo YouTube. Mọi hình là mô tả chung. |
| SCR-P03 | Nền tảng | Tiêu đề/nội dung không câu view sai sự thật | Nghiêm trọng | Claude | ✅ Đạt | Câu hỏi mở đầu "Muối từ đâu ra?" được trả lời trọn ở S02–S04 và tóm lại ở S05-01. Tiêu đề "Vì sao nước biển lại mặn?" đúng nội dung. |
| SCR-Q01 | Chất lượng | Khớp brief (mục tiêu, khán giả, giọng điệu, CTA) | Chặn | Claude | ✅ Đạt | Khớp brief: goal 3 mắt xích có ở S02, S03, S04-01 và tóm ở S05-01; "sông thì không" ở S03-02; khán giả trung học (từ phổ thông); tone xưng mình–gọi bạn (S05-02); CTA ở S05-02. Thời lượng ước theo tốc độ giọng thật 4,43 âm tiết/giây: 48,7 giây so với mục tiêu 50 giây (−2,6%). |
| SCR-Q02 | Chất lượng | Mở đầu giữ chân người xem trong 5 giây đầu | Nghiêm trọng | Claude | ✅ Đạt | S01-01 mở bằng nghịch lý từ giây 0; câu hỏi "Muối từ đâu ra?" kết thúc ở ~4,1 giây (giọng thật). Không chào hỏi. |
| SCR-Q03 | Chất lượng | Mạch logic rõ — mỗi cảnh một ý, chuyển ý có cầu nối | Nghiêm trọng | Claude | ✅ Đạt | Mỗi cảnh một ý: S01 nghịch lý; S02 mưa lấy muối từ đá; S03 sông chở muối, vì sao sông vẫn ngọt; S04 bốc hơi giữ muối, tích qua thời gian, nguồn phụ dưới đáy biển; S05 tóm và CTA. Cầu nối: "Nước mưa chua nhẹ ấy", "Nước mưa gom về", "Mây lại mưa xuống đất", "Thêm một nguồn nữa". |
| SCR-Q04 | Chất lượng | Đúng trình độ khán giả, thuật ngữ được giải thích | Nghiêm trọng | Claude | ✅ Đạt | "Khí cacbonic" là kiến thức lớp 8, có hình phân tử khí bay vào giọt mưa. "Hơi chua" có nhãn "axit nhẹ". "Khe nứt nóng dưới đáy biển" được vẽ ở mặt cắt S04-04. Không dùng thuật ngữ "ion", "nhiệt dịch", "độ muối". |
| SCR-Q05 | Chất lượng | Kết thúc có chốt ý và CTA tự nhiên | Nhẹ | Claude | ✅ Đạt | S05-01 tóm cả 3 mắt xích trong một câu, có biểu tượng hiện theo từng vế. S05-02 là CTA 5,4 giây rồi hết. |
| SCR-Q06 | Chất lượng | Nhịp độ có điểm nghỉ (đoạn im lặng/điểm rơi) hợp lý | Nhẹ | Claude | ✅ Đạt | Có 3 khoảng nghỉ: S01-02 sau câu móc, S02-03 sau đoạn đá (ý khó đầu tiên), S04-02 sau đoạn bốc hơi. Không có 3 đoạn dày thông tin mới liền nhau. Chuỗi S04-03 → S04-04 → S05-01 có S05-01 là câu tóm, không thêm thông tin mới. |
| SCR-V01 | Ngôn ngữ | Chính tả, dấu tiếng Việt, ngữ pháp đúng | Chặn | Claude | ✅ Đạt | Đọc 10 đoạn giọng: không lỗi chính tả, dấu đúng ("hoà tan", "bào mòn", "khoáng chất li ti", "mặn chát", "bổ sung"), câu đủ thành phần. S04-04 dùng dấu phẩy sau "Thêm một nguồn nữa", vẫn chấp nhận được trong văn nói. |
| SCR-V02 | Ngôn ngữ | Văn nói tự nhiên — viết để nghe, không phải để đọc | Nghiêm trọng | Claude | ✅ Đạt | Câu dài nhất là S02-02 và S04-03 (23 âm tiết), đều có dấu phẩy ngắt nhịp. Không có ký hiệu trong lời đọc (mũi tên chỉ nằm trong visual và on_screen_text). Đọc thành tiếng trôi chảy. Với giọng Hải Đăng đo thật 4,4 âm tiết/giây (chủ dự án chọn giữ tốc độ gốc), câu dài nhất ~5,2 giây. |
| SCR-V03 | Ngôn ngữ | Số, viết tắt, từ nước ngoài có cách đọc rõ cho TTS | Nghiêm trọng | Claude | ✅ Đạt | Từ vay mượn duy nhất "cacbonic" đã khai trong meta.pronunciation ("các-bon-níc"). Không có số, đơn vị hay viết tắt trong lời đọc. "Hàng triệu" là chữ. Mã màu chỉ nằm trong visual. |
| SCR-V04 | Ngôn ngữ | Thẻ cảm xúc dùng đúng chỗ, không lạm dụng | Nhẹ | Claude | ➖ Không áp dụng | Không dùng thẻ cảm xúc nào trong 10 đoạn giọng. |
| SCR-D01 | Khả năng sản xuất | Mô tả hình ảnh đủ cụ thể để thiết kế 2D | Nghiêm trọng | Claude | ✅ Đạt | Mỗi visual có đối tượng, chuyển động và điều cần nhận ra. Ví dụ S02-02: hạt trắng bong khỏi đá, đánh dấu hình lập phương muối "để người xem thấy muối đến từ đá". S03-02: nhiều sông dồn chấm trắng về một biển. S04-01: mũi tên lên chỉ có nước, muối ở lại. S04-03: bộ đếm năm, biển đậm màu dần rồi dừng. |
| SCR-D02 | Khả năng sản xuất | Hình ảnh khả thi bằng hoạt ảnh 2D vector, không cần quay thật | Nghiêm trọng | Claude | ✅ Đạt | Sông, biển, đá, giọt mưa, phân tử, mây, mặt trời, núi lửa mặt cắt, bản đồ phẳng, nút bấm đều là hình 2D vector phẳng theo brand.style. Không cần quay thật, không có người. |
