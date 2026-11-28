# Báo cáo kiểm duyệt — Kịch bản

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `script` · checklist "Kiểm duyệt kịch bản" v4
- **Bắt đầu:** 2026-11-28T16:11:55+07:00 · **Chốt:** 2026-11-28T16:11:56+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

32 mục: 29 đạt, 0 trượt, 0 lỗi kiểm tra, 3 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `01_script/script.yaml` | `8b3752fcb9c89921` |
| `00_brief/brief.yaml` | `5d59457f09d659ed` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| SCR-A01 | Cấu trúc | Kịch bản đúng định dạng chuẩn (schema) | Chặn | auto | ✅ Đạt | 01_script/script.yaml khớp schema 'script'. |
| SCR-A02 | Cấu trúc | Mã cảnh/đoạn không trùng | Chặn | auto | ✅ Đạt | 18 mã cảnh/đoạn, không trùng. |
| SCR-A03 | Cấu trúc | Mọi trích dẫn trỏ tới nguồn có thật trong danh sách | Chặn | auto | ✅ Đạt | 5 nguồn, 7 đoạn có trích nguồn, mọi tham chiếu hợp lệ. |
| SCR-A04 | Cấu trúc | Không còn chỗ trống / đánh dấu tạm (TODO, ???, [..]) | Chặn | auto | ✅ Đạt | 01_script/script.yaml: không còn chỗ trống hay đánh dấu tạm. |
| SCR-A05 | Cấu trúc | Mỗi đoạn giọng ≤ 300 ký tự | Nghiêm trọng | auto | ✅ Đạt | Mọi đoạn giọng ≤ 300 ký tự. |
| SCR-A06 | Cấu trúc | Tốc độ đọc trong dải chấp nhận (2,5–5,0 âm tiết/giây) | Nghiêm trọng | auto | ✅ Đạt | 10 đoạn giọng, tốc độ 4.07–4.15 âm tiết/giây. |
| SCR-A07 | Cấu trúc | Tổng thời lượng ước tính khớp mục tiêu (±15%) | Nghiêm trọng | auto | ✅ Đạt | Tổng ước tính 52.9s so với mục tiêu 50s (lệch 6%, cho phép 15%). |
| SCR-A09 | Ngôn ngữ | Cách đọc (meta.pronunciation) viết rời từng âm tiết, không gạch nối/ký hiệu | Nghiêm trọng | auto | ✅ Đạt | 1 mục phát âm đúng định dạng (âm tiết viết rời). |
| SCR-A08 | Cấu trúc | Bản đọc script.md khớp script.yaml | Nhẹ | auto | ✅ Đạt | 01_script/script.md khớp 01_script/script.yaml. |
| SCR-F01 | Sự thật & nguồn | Mọi khẳng định sự thật đều đúng | Chặn | Claude | ✅ Đạt | Đã kiểm lại từng khẳng định theo lời văn nghiêm túc, đối chiếu research.md và các nguồn tra ngày 27/11:<br>- S02-01 "mưa hoà tan khí cacbonic nên hơi có tính axit": tạo axit cacbonic yếu (USGS, Britannica).<br>- S02-02 "bào mòn dần và hoà tan các khoáng chất li ti, trong đó có muối": phong hoá hoá học (USGS).<br>- S03-01 "lượng muối rất nhỏ, nhỏ đến mức ta không nếm ra": USGS, NOAA.<br>- S03-02 "sông luôn được mưa bổ sung nước ngọt mới… biển nhận muối từ tất cả các dòng sông": NOAA.<br>- S04-01 "muối không bốc hơi theo, mà ở lại trong biển": Britannica.<br>- S04-03 "vòng tuần hoàn ấy lặp lại suốt hàng triệu năm, khiến muối trong biển tích tụ dần": NMSF, NOAA.<br>- S04-04 "núi lửa và các khe nứt nóng dưới đáy biển cũng bổ sung thêm khoáng chất": NOAA, USGS.<br>- S05-01 tóm đúng 3 mắt xích.<br>Không có số liệu cụ thể. |
| SCR-F02 | Sự thật & nguồn | Khẳng định quan trọng có nguồn ghi trong kịch bản | Nghiêm trọng | Claude | ✅ Đạt | Mọi đoạn có khẳng định khoa học (S02-01, S02-02, S03-01, S03-02, S04-01, S04-03, S04-04) đều có source_ids, mỗi nguồn hỗ trợ đúng nội dung như ghi ở research.md (K1–K7). S01-01 (sông ngọt, biển mặn) là kiến thức phổ thông. S05-01 chỉ tóm lại các ý đã có nguồn. |
| SCR-F03 | Sự thật & nguồn | Không đơn giản hoá tới mức sai bản chất | Nghiêm trọng | Claude | ✅ Đạt | Dùng "muối" thay cho "các ion hoà tan", và bỏ chi tiết sinh vật biển dùng bớt một số ion (research.md có ghi lý do lược). Đây là đơn giản hoá được phép, không sai bản chất. Lời văn nghiêm túc bỏ hết nhân hoá, nói thẳng cơ chế: hoà tan, bào mòn, bốc hơi, tích tụ. |
| SCR-L01 | Pháp luật | Không có nội dung bị cấm trên không gian mạng | Chặn | Claude | ✅ Đạt | Đối chiếu nhóm nội dung cấm theo Luật An ninh mạng 116/2025/QH15: chỉ có nội dung địa chất, hải dương học phổ thông. Không có yếu tố chính trị, tôn giáo, bạo lực, xúc phạm. |
| SCR-L02 | Pháp luật | Không thông tin sai sự thật, giả mạo về cá nhân/tổ chức/sự kiện có thật | Chặn | Claude | ✅ Đạt | Lời đọc không nhắc cá nhân, tổ chức hay sự kiện có thật nào. Các cơ quan (USGS, NOAA, Britannica, NMSF) chỉ có trong danh sách nguồn. |
| SCR-L03 | Pháp luật | Nếu có quảng cáo/tài trợ — tuân thủ Luật Quảng cáo | Chặn | Claude | ➖ Không áp dụng | brief.is_advertising = false. Kịch bản không giới thiệu sản phẩm, dịch vụ hay thương hiệu nào. CTA chỉ mời đăng ký kênh của chính mình. |
| SCR-L04 | Pháp luật | Không xâm phạm đời tư, hình ảnh, dữ liệu cá nhân | Chặn | Claude | ✅ Đạt | Không có tên, hình ảnh hay dữ liệu người thật. Visual chỉ gồm sông, biển, đá, mây, núi lửa, nút bấm. |
| SCR-L05 | Pháp luật | Nội dung chuyên môn nhạy cảm (y tế, pháp lý, tài chính) có giới hạn trách nhiệm | Nghiêm trọng | Claude | ➖ Không áp dụng | Nội dung khoa học tự nhiên, không có lời khuyên y tế, pháp lý hay tài chính. |
| SCR-P01 | Nền tảng | Không vi phạm Nguyên tắc cộng đồng YouTube | Chặn | Claude | ✅ Đạt | Không có nội dung nguy hiểm. Không khuyến khích nếm hay uống nước sông, nước biển. Văn phong lịch sự, không tiếng lóng, không chế giễu ai. Phù hợp mọi lứa tuổi. |
| SCR-P02 | Nền tảng | Không dùng tác phẩm có bản quyền của người khác | Chặn | Claude | ✅ Đạt | Không trích tác phẩm nào. S05-02 dùng "nút đăng ký tự thiết kế" theo màu brand, không dùng logo YouTube. Mọi hình là mô tả chung. Linh vật Khỉ và logo thuộc bộ nhận diện do chủ dự án cung cấp và dùng cho kênh của chính chủ dự án, không phỏng theo nhân vật có bản quyền đã biết. Hình tạo bằng AI nên được gắn nhãn theo constraints của brief. |
| SCR-P03 | Nền tảng | Tiêu đề/nội dung không câu view sai sự thật | Nghiêm trọng | Claude | ✅ Đạt | Câu hỏi mở đầu "Muối trong biển từ đâu mà có?" được trả lời trọn ở S02–S04, mở bằng "Câu trả lời bắt đầu từ nước mưa", và tóm lại ở S05-01. Tiêu đề "Vì sao nước biển lại mặn?" đúng nội dung. Chữ trên màn hình "Muối từ đâu ra?" khớp ý câu hỏi. |
| SCR-Q01 | Chất lượng | Khớp brief (mục tiêu, khán giả, giọng điệu, CTA) | Chặn | Claude | ✅ Đạt | Khớp brief:<br>- goal 3 mắt xích có ở S02, S03, S04-01, tóm lại ở S05-01; ý "sông thì không" ở S03-02.<br>- Khán giả trung học: từ phổ thông, có "tính axit", "khoáng chất", "tích tụ".<br>- tone mới "thân thiện, rõ ràng, nghiêm túc vừa phải; gọi bạn; không tiếng lóng; Khỉ ở lời mời cuối": không còn "nè", "ta" (khẩu ngữ), "xíu xiu"; S05-02 "cùng Khỉ khám phá".<br>- cta khớp S05-02.<br>- Ước tính 52,9 giây (4,15 âm tiết/giây, đã hiệu chỉnh) so với mục tiêu 50, +6%, trong ngưỡng ±15% (SCR-A07 đạt). |
| SCR-Q02 | Chất lượng | Mở đầu giữ chân người xem trong 5 giây đầu | Nghiêm trọng | Claude | ✅ Đạt | S01-01 mở ngay bằng nghịch lý từ giây 0 ("Sông đổ ra biển toàn là nước ngọt. Vậy mà nước biển lại mặn."). Câu hỏi "Muối trong biển từ đâu mà có?" kết thúc ở khoảng 5,1 giây theo ước tính. Không chào hỏi. |
| SCR-Q03 | Chất lượng | Mạch logic rõ — mỗi cảnh một ý, chuyển ý có cầu nối | Nghiêm trọng | Claude | ✅ Đạt | Mỗi cảnh một ý: S01 nghịch lý; S02 mưa lấy muối từ đá; S03 sông chở muối, vì sao sông vẫn ngọt; S04 bốc hơi giữ muối, tích qua thời gian, nguồn phụ dưới đáy biển; S05 tóm và CTA. Cầu nối: "Nước mưa chua nhẹ ấy", "Nước mưa gom về", "Mây lại mưa xuống đất", "Thêm một nguồn nữa". |
| SCR-Q04 | Chất lượng | Đúng trình độ khán giả, thuật ngữ được giải thích | Nghiêm trọng | Claude | ✅ Đạt | "Khí cacbonic" là kiến thức lớp 8, có hình phân tử khí bay vào giọt mưa. "Hơi chua" có nhãn "axit nhẹ". "Khe nứt nóng dưới đáy biển" được vẽ ở mặt cắt S04-04. Không dùng thuật ngữ "ion", "nhiệt dịch", "độ muối". |
| SCR-Q05 | Chất lượng | Kết thúc có chốt ý và CTA tự nhiên | Nhẹ | Claude | ✅ Đạt | S05-01 tóm cả 3 mắt xích trong một câu, có biểu tượng hiện theo từng vế. S05-02 là CTA khoảng 4,1 giây rồi hết. |
| SCR-Q06 | Chất lượng | Nhịp độ có điểm nghỉ (đoạn im lặng/điểm rơi) hợp lý | Nhẹ | Claude | ✅ Đạt | Có 3 khoảng nghỉ: S01-02 sau câu móc, S02-03 sau đoạn đá (ý khó đầu tiên), S04-02 sau đoạn bốc hơi. Không có 3 đoạn dày thông tin mới liền nhau. Chuỗi S04-03 → S04-04 → S05-01 có S05-01 là câu tóm, không thêm thông tin mới. |
| SCR-V01 | Ngôn ngữ | Chính tả, dấu tiếng Việt, ngữ pháp đúng | Chặn | Claude | ✅ Đạt | Đã đọc 10 đoạn lời mới: không lỗi chính tả, dấu đúng ("tính axit", "bào mòn", "khoáng chất li ti", "tích tụ", "bổ sung"). Câu đủ thành phần. Từ "ta" ở S03-01 dùng như đại từ chung ("ta không nếm ra"), không phải khẩu ngữ. |
| SCR-V02 | Ngôn ngữ | Văn nói tự nhiên — viết để nghe, không phải để đọc | Nghiêm trọng | Claude | ✅ Đạt | Câu dài nhất là S04-03 (22 âm tiết), có dấu phẩy ngắt nhịp. S03-01, S04-04, S05-01 khoảng 20–21 âm tiết, đều có dấu phẩy. Không có ký hiệu trong lời đọc. Đọc to thử: rõ ràng, không líu lưỡi. |
| SCR-V03 | Ngôn ngữ | Số, viết tắt, từ nước ngoài có cách đọc rõ cho TTS | Nghiêm trọng | Claude | ✅ Đạt | Từ vay mượn duy nhất "cacbonic" khai pronunciation "các bô ních" (âm tiết rời, đúng chính tả vần -ich). Lịch sử: "các-bon-níc" bị đọc "cacbon-i-c"; "các bô níc" bị đánh vần "các bô i xê" — cả hai do chủ dự án nghe phát hiện 27–28/11; đã thêm kiểm tra tự động (SCR-A09: không gạch nối + chính tả vần sau i/ê phải ch/nh). Không có số, đơn vị, viết tắt trong lời. |
| SCR-V04 | Ngôn ngữ | Thẻ cảm xúc dùng đúng chỗ, không lạm dụng | Nhẹ | Claude | ➖ Không áp dụng | Không dùng thẻ cảm xúc nào trong 10 đoạn giọng. |
| SCR-D01 | Khả năng sản xuất | Mô tả hình ảnh đủ cụ thể để thiết kế 2D | Nghiêm trọng | Claude | ✅ Đạt | Mỗi visual có đối tượng, chuyển động và điều cần nhận ra. Ví dụ S02-02: hạt trắng bong khỏi đá, đánh dấu hình lập phương muối "để người xem thấy muối đến từ đá". S03-02: nhiều sông dồn chấm trắng về một biển. S04-01: mũi tên lên chỉ có nước, muối ở lại. S04-03: bộ đếm năm, biển đậm màu dần rồi dừng. |
| SCR-D02 | Khả năng sản xuất | Hình ảnh khả thi bằng hoạt ảnh 2D vector, không cần quay thật | Nghiêm trọng | Claude | ✅ Đạt | Lời đọc viết lại theo văn phong nghiêm túc (chủ dự án duyệt bản nháp 28/11); phải tạo lại giọng Xuân Vĩnh +2,5 nửa cung. Mọi visual giữ nguyên, vẫn khớp ý từng câu. Hình vẫn làm được bằng SVG vector và PNG linh vật. |
