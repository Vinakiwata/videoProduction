---
name: vp-brief
description: Dùng khi bắt đầu một video mới trong repo này (Tool 0) — người dùng đưa ý tưởng, chủ đề hay yêu cầu làm video, cần tạo hoặc sửa 00_brief/brief.yaml, hoặc cần tạo/sửa hồ sơ kênh channels/<kênh>/channel.yaml.
---

# Tool 0 — Brief

Brief là **thước đo** cho mọi công đoạn sau. Kịch bản, thiết kế và QC tổng đều được chấm theo brief.
Brief mơ hồ thì không công đoạn nào chấm đúng được.

## Các bước

1. **Chọn kênh.** Xem `channels/`. Chưa có kênh phù hợp thì tạo `channels/<kênh>/channel.yaml` theo `vp/schemas/channel.schema.json`,
   và **báo người dùng** rằng đó là bộ nhận diện tạm, cần họ xác nhận.
2. **Rút thông tin từ yêu cầu**: chủ đề, mục tiêu, khán giả, độ dài, có quảng cáo hay không.
   Tìm trong cuộc trò chuyện trước, không hỏi lại điều người dùng đã nói.
3. **Viết mục tiêu (goal) dạng kết quả ở người xem.** Mẫu: *"Sau N giây, người xem [giải thích lại được / làm được / quyết định được] … và [hành động CTA]."*
   Không viết "làm video hay về …".
4. **Tạo file:**
   `python -m vp brief new projects/<slug> --channel <kênh> --title "…" --goal "…" [--audience "…"] [--duration N] [--ads|--no-ads]`
   `slug` viết thường, không dấu, nối bằng gạch ngang. Ví dụ: `vi-sao-la-chuyen-vang`.
5. **Người dùng có mặt:** hỏi **từng câu một**, chỉ hỏi điều làm thay đổi video, theo thứ tự:
   mục tiêu → khán giả (nếu khác kênh) → có quảng cáo/tài trợ không → độ dài.
   **Người dùng vắng mặt:** tự quyết theo cách hợp lý nhất, rồi ghi **mỗi** quyết định vào `assumptions`, ví dụ:
   `"Giả định khán giả là học sinh THPT vì chủ đề nằm trong chương trình Vật lý 11"`.
6. **Soát nhanh:** không còn `TODO`; độ dài hợp với khối lượng ý (khoảng 20–40 giây cho mỗi ý chính); định dạng khớp kênh.
7. **Qua cổng:** dùng skill `vp-kiem-duyet` cho công đoạn `brief`. Cổng chưa ĐẠT thì không viết kịch bản.

## Lưu ý
- Có nhắc tới sản phẩm, thương hiệu hay nhà tài trợ thì phải dùng `--ads` (Luật Quảng cáo sửa đổi 75/2025/QH15).
- Sửa brief sau khi đã qua cổng thì cổng **hết hiệu lực**, và mọi công đoạn sau cũng phải duyệt lại.
