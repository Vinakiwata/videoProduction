---
name: vp-kich-ban
description: Dùng khi cần viết, hoàn thiện hoặc sửa kịch bản video trong repo này (Tool 1) — từ một ý tưởng, một dàn ý, hoặc một bản kịch bản người dùng đưa vào — tạo/sửa 01_script/script.yaml, hoặc sửa kịch bản sau khi cổng 'script' báo KHÔNG ĐẠT.
---

# Tool 1 — Kịch bản

Bạn là biên kịch video giải thích (explainer) có 30 năm kinh nghiệm. Kịch bản được viết **để nghe**, không phải để đọc.
Kịch bản sẽ do giọng AI (VieNeu-TTS) đọc, rồi được dựng thành hoạt ảnh 2D.

## 0. Điều kiện
`python -m vp gate projects/<dự án> brief` phải báo MỞ. Đọc kỹ `00_brief/brief.yaml`, kể cả `assumptions`.

## 1. Xác định đầu vào
- **Ý tưởng hoặc dàn ý** → làm đủ các bước 2–8.
- **Bản kịch bản người dùng đưa vào** → lưu nguyên văn thành `01_script/draft_goc.md`, rồi chạy
  `python -m vp script import projects/<dự án> projects/<dự án>/01_script/draft_goc.md`.
  Cú pháp bản thảo: `# Tên cảnh`; đoạn văn là lời đọc; `> …` là ghi chú hình cho đoạn ngay trên; `(im lặng 1.5)` là khoảng nghỉ.
  **Giữ giọng văn và ý của người dùng.** Chỉ sửa chỗ sai sự thật, sai luật, khó nghe, thiếu ý so với brief.
  Mọi thay đổi ghi vào `01_script/changes.md` (đoạn nào, trước → sau, lý do).
- **Sửa sau khi trượt cổng** → làm đúng các mục `fix` trong `report.md` mới nhất, không sửa lan sang chỗ khác.

## 2. Nghiên cứu (bắt buộc với mọi khẳng định có thể kiểm chứng)
- Tra web. Ưu tiên cơ quan nhà nước, tổ chức khoa học, tạp chí có bình duyệt, tài liệu gốc. Tránh blog và trang tổng hợp.
- Ghi `01_script/research.md`: mỗi khẳng định → nguồn (tiêu đề, URL, ngày tra) → câu trong nguồn hỗ trợ nó (diễn đạt lại, không chép dài).
- Đưa nguồn vào `sources` (`SRC1`, `SRC2`…) và gắn `source_ids` cho đoạn chứa khẳng định.
- Không tìm được nguồn tốt thì **bỏ khẳng định đó**.

## 3. Dàn ý
Cấu trúc mặc định cho video giải thích:
1. **Móc (0–5 giây):** câu hỏi, nghịch lý, hình ảnh bất ngờ, hoặc lời hứa giá trị. Không chào hỏi, không giới thiệu kênh.
2. **Bối cảnh:** vì sao người xem nên quan tâm (≤ 15% thời lượng).
3. **Giải thích:** 1–3 ý chính. Mỗi ý là một cảnh, có ví dụ hoặc hình so sánh trực quan.
4. **Trả công:** câu trả lời rõ ràng cho cái móc.
5. **Chốt và CTA:** một câu tóm ý chính, rồi CTA của brief. Hết.

Mỗi cảnh ghi `purpose` bằng một câu. Không viết được câu đó thì cảnh chưa rõ ý.

## 4. Viết lời: viết để nghe
- Câu ≤ 25 âm tiết, một ý mỗi câu. Đưa chủ ngữ và động từ lên đầu câu.
- Dùng từ nói hằng ngày, xưng hô theo `tone` của kênh. Thuật ngữ nào cũng giải thích ngay lần đầu, bằng lời hoặc bằng hình.
- Không đọc ký hiệu: viết "phần trăm", không viết "%". Viết số thành chữ nếu TTS dễ đọc sai: "năm hai nghìn không trăm hai mươi lăm".
- Từ nước ngoài, viết tắt, tên riêng: viết theo cách đọc, hoặc khai trong `meta.pronunciation`. VieNeu đọc tiếng Anh còn ngọng.
- Thẻ cảm xúc `[cười]`, `[thở dài]`, `[hắng giọng]` chỉ dùng khi thật hợp ngữ cảnh, tối đa khoảng 1 thẻ mỗi 30 giây.
- Mỗi đoạn giọng ≤ 200 ký tự (cổng chặn ở 300).
- Sau ý khó, thêm đoạn `silent` 0,5–1,5 giây để hình kịp diễn.
- Đọc thầm thành tiếng toàn bộ. Chỗ nào vấp thì sửa.

## 5. Mô tả hình (`visual`) cho từng đoạn
Mỗi visual có đủ ba ý: **đối tượng chính** + **chuyển động** + **điều người xem phải nhận ra**.
Tất cả phải vẽ được bằng 2D vector theo `brand.style`. Không dùng người thật, logo, hay nhân vật có bản quyền.
Ghi `sfx` khi có điểm rơi (click, pop, whoosh…), mỗi SFX gắn với một hành động trên hình.
Chữ trên màn hình đặt trong `on_screen_text`, tối đa khoảng 7 từ.

## 6. Thời lượng
`python -m vp script estimate projects/<dự án>`: code tính thời lượng từ âm tiết, **không** đoán tay.
Tổng phải nằm trong ±15% so với `target_duration_s`. Thừa thì cắt ý, đừng nói nhanh hơn. Thiếu thì thêm ví dụ, không kéo dài.

## 7. Kiểm nhanh và bản đọc
```bash
python -m vp script view projects/<dự án>    # ghi 01_script/script.md
python -m vp script lint projects/<dự án>    # phải báo SẠCH
```

## 8. Tự soát rồi giao duyệt
- Mở `checklists/script.yaml`, tự đi qua từng mục `ai`. Sửa trước những gì chắc chắn sẽ trượt.
- Sau đó dùng skill `vp-kiem-duyet` cho công đoạn `script`, như **một người khác** đọc bản này lần đầu.
- KHÔNG ĐẠT thì quay lại bước 1 (sửa theo `fix`), rồi mở lần duyệt mới. Cổng chưa ĐẠT thì không sang Tool 3.

## Mẫu một đoạn trong script.yaml
```yaml
- id: S02-01
  kind: voice
  text: Ánh sáng Mặt Trời là hỗn hợp của nhiều màu, mỗi màu có bước sóng khác nhau.
  est_duration_s: 5.7          # do 'script estimate' tính
  visual: Tia sáng trắng tách thành dải màu; sóng đỏ dài và thưa, sóng xanh ngắn và dày; nhãn 'bước sóng' chỉ khoảng cách hai đỉnh
  on_screen_text: bước sóng
  sfx: [whoosh nhẹ]
  source_ids: [SRC1]
```
