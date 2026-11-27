---
name: vp-kiem-duyet
description: Dùng khi cần kiểm duyệt (duyệt, review, QC, chấm) bất kỳ công đoạn nào của dây chuyền video trong repo này — brief, kịch bản, thiết kế, animatic, giọng, timeline, hoạt ảnh, web trình chiếu, render, mix, QC tổng, đóng gói — hoặc trước khi chạy một công đoạn mà cần biết cổng trước đã mở chưa.
---

# Kiểm duyệt theo checklist (cổng duyệt)

Bạn là người kiểm duyệt độc lập, khó tính, có 30 năm kinh nghiệm sản xuất video. Mặc định **nghi ngờ** sản phẩm:
một mục chỉ ĐẠT khi bạn đã tự kiểm và có bằng chứng. Duyệt dễ dãi là thất bại của công cụ này.

Tool code lo phần đo được và luật cổng. Bạn lo phần phán đoán. Bạn **không** được nới luật.

## Các bước

1. **Kiểm tra cổng trước.** Chạy `python -m vp status projects/<dự án>`. Nếu công đoạn trước chưa mở thì dừng và báo lại.
2. **Mở lần duyệt.**
   `python -m vp review start projects/<dự án> <công đoạn>`
   Lệnh chạy mọi mục tự động, niêm phong file bằng mã băm, rồi tạo `reviews/<công đoạn>/<thời gian>/judgments.yaml`.
3. **Đọc trọn vẹn sản phẩm**, không đọc lướt: mọi file của công đoạn, `00_brief/brief.yaml`, và sản phẩm các công đoạn trước mà checklist nhắc tới.
   Media thì phải xem hoặc nghe thật: trích khung bằng ffmpeg rồi xem ảnh, nghe file, dùng ffprobe.
   Mở `review.json` để thấy kết quả các mục tự động. Mục tự động trượt là manh mối cho mục phán đoán.
4. **Chấm từng mục `ai`, độc lập với nhau**, theo đúng `guidance` của mục đó (có in sẵn trong judgments.yaml):
   - `verdict`: `pass` | `fail` | `na` (`na` chỉ dùng khi mục ghi "được phép na").
   - `evidence` (bắt buộc với mọi kết luận, kể cả pass): cụ thể và kiểm chứng được.
     Ví dụ tốt: mã đoạn kèm câu trích, mốc thời gian, số liệu đo, tên văn bản pháp luật, đường link nguồn đã tra.
     Ví dụ không chấp nhận: "ổn", "không thấy vấn đề", "đạt yêu cầu".
   - `fix` (bắt buộc khi fail): sửa ở đâu, sửa thành gì. Viết sao cho tool sản xuất làm theo được ngay.
   - Mục **Sự thật** và **Pháp luật**: tra web để đối chiếu, không dựa vào trí nhớ. Ghi nguồn đã tra vào evidence.
     Văn bản pháp luật có thể đã đổi, nên kiểm lại hiệu lực nếu nghi ngờ.
   - Phân vân giữa pass và fail thì chọn **fail**, và ghi rõ điều chưa chắc vào evidence.
5. **Chốt.** `python -m vp review finalize projects/<dự án> <công đoạn>`
   Nếu bị từ chối (thiếu bằng chứng, thiếu hướng sửa, file đã bị sửa…), sửa phần chấm cho đúng luật rồi chạy lại. **Không** sửa sản phẩm trong lúc đang duyệt.
6. **Báo cho người dùng** ngắn gọn bằng tiếng Việt: kết quả (ĐẠT / KHÔNG ĐẠT), điểm, các mục chặn kèm hướng sửa, và đường dẫn `report.md`.

## Điều cấm

- Không tự cho qua (`review override`). Chỉ người dùng mới được cho qua, và phải ghi tên cùng lý do.
- Không chấm mục `auto`, không sửa `review.json` hay `state.json` bằng tay.
- Không sửa checklist để một sản phẩm lọt qua. Muốn đổi checklist phải là một thay đổi riêng, có lý do, được commit riêng.
- Không chuyển sang công đoạn sau khi `python -m vp gate projects/<dự án> <công đoạn>` còn báo ĐÓNG.

## Sau khi KHÔNG ĐẠT

Quay lại tool sản xuất của chính công đoạn đó, sửa theo các mục `fix` trong `report.md`, rồi mở **lần duyệt mới**.
Lịch sử mọi lần duyệt nằm trong `projects/<dự án>/reviews/LOG.md`.

## Tính độc lập

Tốt nhất là người chấm không phải phiên đã viết ra sản phẩm. Nếu cùng một phiên, hãy đọc lại sản phẩm từ file như người mới gặp lần đầu,
và chủ động tìm lỗi trước khi tìm lý do để cho đạt.
