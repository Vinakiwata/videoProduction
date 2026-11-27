# Báo cáo kiểm duyệt — Kịch bản

- **Dự án:** vi-du-bau-troi-xanh
- **Công đoạn:** `script` · checklist "Kiểm duyệt kịch bản" v1
- **Bắt đầu:** 2026-11-27T21:33:46+07:00 · **Chốt:** 2026-11-27T21:33:46+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

30 mục: 27 đạt, 0 trượt, 0 lỗi kiểm tra, 3 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `01_script/script.yaml` | `3c762e4038117dc2` |
| `00_brief/brief.yaml` | `181f27a16079b863` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| SCR-A01 | Cấu trúc | Kịch bản đúng định dạng chuẩn (schema) | Chặn | auto | ✅ Đạt | 01_script/script.yaml khớp schema 'script'. |
| SCR-A02 | Cấu trúc | Mã cảnh/đoạn không trùng | Chặn | auto | ✅ Đạt | 10 mã cảnh/đoạn, không trùng. |
| SCR-A03 | Cấu trúc | Mọi trích dẫn trỏ tới nguồn có thật trong danh sách | Chặn | auto | ✅ Đạt | 1 nguồn, 2 đoạn có trích nguồn, mọi tham chiếu hợp lệ. |
| SCR-A04 | Cấu trúc | Không còn chỗ trống / đánh dấu tạm (TODO, ???, [..]) | Chặn | auto | ✅ Đạt | Không còn chỗ trống hay đánh dấu tạm. |
| SCR-A05 | Cấu trúc | Mỗi đoạn giọng ≤ 300 ký tự | Nghiêm trọng | auto | ✅ Đạt | Mọi đoạn giọng ≤ 300 ký tự. |
| SCR-A06 | Cấu trúc | Tốc độ đọc tự nhiên (2,5–4,0 âm tiết/giây) | Nghiêm trọng | auto | ✅ Đạt | 5 đoạn giọng, tốc độ 2.83–3.75 âm tiết/giây. |
| SCR-A07 | Cấu trúc | Tổng thời lượng ước tính khớp mục tiêu (±15%) | Nghiêm trọng | auto | ✅ Đạt | Tổng ước tính 29s so với mục tiêu 30s (lệch 3%, cho phép 15%). |
| SCR-F01 | Sự thật & nguồn | Mọi khẳng định sự thật đều đúng | Chặn | Claude | ✅ Đạt | Có 3 khẳng định: S02-01 ánh sáng Mặt Trời gồm nhiều màu, mỗi màu một bước sóng; S02-02 ánh sáng xanh bước sóng ngắn bị phân tử khí làm bật ra mọi hướng; S03-01 vì vậy cả bầu trời trông xanh. Đối chiếu NASA Space Place (spaceplace.nasa.gov/blue-sky, tra 2026-11-27): khớp cả 3. Tán xạ Rayleigh đúng là phát tán theo mọi hướng. |
| SCR-F02 | Sự thật & nguồn | Khẳng định quan trọng có nguồn ghi trong kịch bản | Nghiêm trọng | Claude | ✅ Đạt | S02-02 và S03-01 (hai khẳng định cốt lõi) có source_ids [SRC1], và nguồn hỗ trợ đúng nội dung. S02-01 là kiến thức phổ thông, cũng được SRC1 xác nhận. |
| SCR-F03 | Sự thật & nguồn | Không đơn giản hoá tới mức sai bản chất | Nghiêm trọng | Claude | ✅ Đạt | Bỏ qua chi tiết ánh sáng tím (tán xạ mạnh hơn nhưng mắt kém nhạy và Mặt Trời phát ít hơn). "Bật tung ra mọi hướng" là cách nói hình ảnh đúng bản chất tán xạ. Không câu nào sai. |
| SCR-L01 | Pháp luật | Không có nội dung bị cấm trên không gian mạng | Chặn | Claude | ✅ Đạt | Đối chiếu nhóm nội dung cấm theo Luật An ninh mạng 116/2025/QH15: chỉ có nội dung vật lý phổ thông, không chính trị, tôn giáo, bạo lực, đồi truỵ, xúc phạm. |
| SCR-L02 | Pháp luật | Không thông tin sai sự thật, giả mạo về cá nhân/tổ chức/sự kiện có thật | Chặn | Claude | ✅ Đạt | Lời đọc không nhắc cá nhân, tổ chức hay sự kiện có thật nào. NASA chỉ xuất hiện trong danh sách nguồn. |
| SCR-L03 | Pháp luật | Nếu có quảng cáo/tài trợ — tuân thủ Luật Quảng cáo | Chặn | Claude | ➖ Không áp dụng | brief.is_advertising = false. CTA chỉ là đăng ký kênh của chính mình, không quảng bá sản phẩm hay thương hiệu nào. |
| SCR-L04 | Pháp luật | Không xâm phạm đời tư, hình ảnh, dữ liệu cá nhân | Chặn | Claude | ✅ Đạt | Không có tên, hình ảnh hay dữ liệu người thật. Bản này đã bỏ nhân vật, các visual chỉ còn thiên nhiên, tia sáng, phân tử, nút đăng ký. |
| SCR-L05 | Pháp luật | Nội dung chuyên môn nhạy cảm (y tế, pháp lý, tài chính) có giới hạn trách nhiệm | Nghiêm trọng | Claude | ➖ Không áp dụng | Nội dung khoa học vật lý thuần tuý, không có lời khuyên y tế, pháp lý hay tài chính. |
| SCR-P01 | Nền tảng | Không vi phạm Nguyên tắc cộng đồng YouTube | Chặn | Claude | ✅ Đạt | Không có nội dung nguy hiểm, quấy rối, thù ghét hay thông tin sai về y tế. Phù hợp mọi lứa tuổi. |
| SCR-P02 | Nền tảng | Không dùng tác phẩm có bản quyền của người khác | Chặn | Claude | ✅ Đạt | Không trích tác phẩm của người khác. Nút đăng ký mô tả là nút tự thiết kế theo màu brand, không dùng logo YouTube. |
| SCR-P03 | Nền tảng | Tiêu đề/nội dung không câu view sai sự thật | Nghiêm trọng | Claude | ✅ Đạt | Câu hỏi S01-01 được trả lời trọn ở S02-02 và S03-01. Không phóng đại. |
| SCR-Q01 | Chất lượng | Khớp brief (mục tiêu, khán giả, giọng điệu, CTA) | Chặn | Claude | ✅ Đạt | Khớp brief: mục tiêu "giải thích lại được bằng một câu" được đáp ứng bởi S02-02 + S03-01; khán giả trung học (không thuật ngữ khó); giọng thân thiện ("nhé!"); CTA đăng ký có ở S03-02; tổng 29 giây so với mục tiêu 30 giây. |
| SCR-Q02 | Chất lượng | Mở đầu giữ chân người xem trong 5 giây đầu | Nghiêm trọng | Claude | ✅ Đạt | S01-01 mở bằng câu hỏi gợi tò mò ngay giây 0, dấu chấm hỏi bật ra. Không chào hỏi. |
| SCR-Q03 | Chất lượng | Mạch logic rõ — mỗi cảnh một ý, chuyển ý có cầu nối | Nghiêm trọng | Claude | ✅ Đạt | S01 đặt câu hỏi → S02 ánh sáng nhiều màu, xanh bị bật ra mọi hướng → S03 vì thế trời xanh + CTA. Mỗi cảnh một ý, có cầu nối "Khi đi qua khí quyển". |
| SCR-Q04 | Chất lượng | Đúng trình độ khán giả, thuật ngữ được giải thích | Nghiêm trọng | Claude | ✅ Đạt | "Bước sóng" được giải thích bằng hình ở S02-01 (sóng đỏ dài và thưa so với sóng xanh ngắn và dày, nhãn chỉ khoảng cách hai đỉnh sóng). Từ chuyên môn "tán xạ" đã thay bằng "bật tung ra mọi hướng". Không còn thuật ngữ chưa giải thích. |
| SCR-Q05 | Chất lượng | Kết thúc có chốt ý và CTA tự nhiên | Nhẹ | Claude | ✅ Đạt | S03-01 chốt ý chính trong một câu, S03-02 là CTA 5 giây rồi hết, không kéo dài. |
| SCR-Q06 | Chất lượng | Nhịp độ có điểm nghỉ (đoạn im lặng/điểm rơi) hợp lý | Nhẹ | Claude | ✅ Đạt | Sau hai đoạn dày thông tin S02-01 (6s) và S02-02 (7s) có đoạn nghỉ S02-03 (1s, whoosh) để hoạt ảnh tán xạ diễn ra. Sau câu hỏi mở đầu cũng có nghỉ S01-02 (1s). |
| SCR-V01 | Ngôn ngữ | Chính tả, dấu tiếng Việt, ngữ pháp đúng | Chặn | Claude | ✅ Đạt | Đọc lại 5 đoạn giọng: không lỗi chính tả, dấu đúng ("khí quyển", "phân tử", "bước sóng"). S03-01 đã sửa thành "Thế nên ánh sáng xanh phủ kín bầu trời, và nhìn đâu ta cũng thấy màu xanh.", không còn thừa quan hệ từ. |
| SCR-V02 | Ngôn ngữ | Văn nói tự nhiên — viết để nghe, không phải để đọc | Nghiêm trọng | Claude | ✅ Đạt | Câu dài nhất S02-02 có 21 âm tiết, có dấu phẩy ngắt nhịp. Không ký hiệu. Đọc thành tiếng trôi chảy. |
| SCR-V03 | Ngôn ngữ | Số, viết tắt, từ nước ngoài có cách đọc rõ cho TTS | Nghiêm trọng | Claude | ✅ Đạt | Không có số, đơn vị, viết tắt hay từ nước ngoài trong lời đọc. Mã màu (#FFD23F) chỉ nằm ở visual, không đọc. |
| SCR-V04 | Ngôn ngữ | Thẻ cảm xúc dùng đúng chỗ, không lạm dụng | Nhẹ | Claude | ➖ Không áp dụng | Không dùng thẻ cảm xúc nào trong 5 đoạn giọng. |
| SCR-D01 | Khả năng sản xuất | Mô tả hình ảnh đủ cụ thể để thiết kế 2D | Nghiêm trọng | Claude | ✅ Đạt | Mọi visual nêu đối tượng, chuyển động và điều cần nhận ra. Ví dụ S02-02: tia xanh dội nhiều lần, đặt cạnh tia đỏ đi thẳng "để người xem thấy xanh bị dội nhiều hơn". S03-01: toàn cảnh Trái Đất với khí quyển sáng xanh. S03-02 ghi rõ mã màu. |
| SCR-D02 | Khả năng sản xuất | Hình ảnh khả thi bằng hoạt ảnh 2D vector, không cần quay thật | Nghiêm trọng | Claude | ✅ Đạt | Sóng, tia sáng, phân tử, Trái Đất, nút bấm đều là hình 2D vector đơn giản. Không cần quay thật. |
