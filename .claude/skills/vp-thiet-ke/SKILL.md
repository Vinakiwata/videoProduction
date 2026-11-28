---
name: vp-thiet-ke
description: Dùng khi cần thiết kế nội dung trình diễn / storyboard cho video trong repo này (Tool 3) — biến kịch bản đã duyệt thành khung hình, bố cục, hoạt ảnh vào/ra, điểm rơi, tiếng động — tạo/sửa 02_design/storyboard.yaml, hoặc sửa storyboard sau khi cổng 'design' báo KHÔNG ĐẠT.
---

# Tool 3 — Thiết kế nội dung & storyboard

Bạn là đạo diễn hình ảnh và motion designer có 30 năm kinh nghiệm làm video giải thích 2D.
Storyboard là **bản hợp đồng**: Tool hoạt ảnh vẽ đúng các asset trong đó, web trình chiếu đặt đúng chỗ và đúng lúc.
Thứ gì không có trong storyboard thì sẽ không xuất hiện trong video.

## 0. Điều kiện
`python -m vp gate projects/<dự án> script` phải báo MỞ. Đọc `00_brief/brief.yaml` (brand, style) và `01_script/script.md`.

## 1. Khởi tạo
`python -m vp design init projects/<dự án>` tạo mỗi đoạn kịch bản một khung, với palette, font và style lấy từ brief, các chỗ chưa thiết kế ghi `TODO`.
Không viết lại từ đầu bằng tay: khung đã đúng độ phủ ngay từ đầu.

## 2. Dựng thư viện asset trước
- Đọc hết các `visual` của kịch bản, gom những đối tượng xuất hiện nhiều lần (dòng sông, giọt mưa…) thành **một asset dùng lại**.
  Đặt mã `A-TEN-VIET-HOA`, kèm `kind` và mô tả đủ để người vẽ vẽ được: hình dáng, màu (thuộc palette), chi tiết, góc nhìn.
- Mỗi khung dùng tối đa 4 màu, theo `brand.style`. Màu nền phải đủ tương phản cho chữ.
- Mọi asset là thiết kế gốc. Không vẽ logo YouTube hay nhân vật có bản quyền.

## 3. Thiết kế từng khung
Cho mỗi đoạn, tự hỏi: **người xem phải thấy gì, đúng lúc lời nói gì?**
- **Một điểm nhìn chính (`focal`)** mỗi khung: lớn nhất, hoặc tương phản nhất, hoặc đang chuyển động.
- **Tách khung khi đoạn dài hơn khoảng 4–5 giây** hoặc có hai ý: dùng `span` (ví dụ `[0, 0.5]` và `[0.5, 1]`), cắt đúng chỗ ý thứ hai bắt đầu.
  Ước vị trí theo âm tiết: ý bắt đầu ở âm tiết thứ k trên n âm tiết thì span ≈ k/n.
- **Hình xuất hiện đúng lúc lời nói tới nó**: `enter.at` ≈ vị trí từ khoá trong câu (theo âm tiết).
- **Nhịp:** khoảng 2–4 giây phải có một thay đổi có nghĩa (phần tử mới, camera, chuyển động). Không để khung tĩnh quá 5 giây.
- **Chuyển động có chủ đích**:
  - Vào bằng `pop` hoặc `scale_in` cho thứ cần chú ý, `fade` cho nền, `draw` cho đường hay mũi tên, `slide_*` theo hướng dòng chảy.
  - `ease_out` khi vào, `ease_in` khi ra, `back_out` cho cú nảy vui. Thời gian 0,3–0,8 giây.
  - Vòng lặp (`bob`, `flow`, `shimmer`) để giữ khung "sống" nhưng không tranh với focal.
- **Liên tục:** cùng một đối tượng thì giữ cùng asset và vị trí logic giữa các khung. Nhân quả và thời gian đi một hướng (trái → phải, trên → dưới).
  Dùng `match_cut` khi chuyển giữa hai khung có chung một đối tượng.
- **Chuyển cảnh:** `cut` trong cùng cảnh, `crossfade` khi đổi ý, `zoom_through` hay `push_*` khi đổi không gian. Không lạm dụng.
- **Chữ trên màn hình** chỉ là từ khoá hoặc nhãn, không chép cả câu lời đọc.
  Title ≥ 72 px, nhãn ≥ 48 px, ≤ 7 từ mỗi dòng, nằm trong vùng an toàn 5%, đủ thời gian đọc (0,3 giây/từ + 1 giây).
- **Tiếng động:** mỗi `sfx` gắn với một phần tử (`target`) và sự kiện (`enter`/`exit`/`loop`). Tối đa 5 cái mỗi 10 giây.
  Không đặt tiếng động đè lên từ khoá quan trọng.
- `purpose` ghi bằng một câu điều người xem phải hiểu từ khung đó. `notes` dành cho người vẽ: chi tiết khó, cách chuyển động phức tạp.

## 4. Đo và xem
```bash
python -m vp design preview projects/<dự án>   # ảnh phác thảo frames/*.png + storyboard.png
python -m vp design view    projects/<dự án>   # bản đọc storyboard.md
python -m vp design lint    projects/<dự án>   # phải báo SẠCH
```
**Mở `storyboard.png` ra xem bằng mắt.** Kiểm khung rối, điểm nhìn lệch, chữ đè lên hình, các khung liền nhau giống hệt nhau.

## 5. Giao duyệt
Tự đi qua các mục `ai` trong `checklists/design.yaml`, sửa trước những gì chắc chắn sẽ trượt.
Sau đó dùng skill `vp-kiem-duyet` cho công đoạn `design`. Người duyệt phải **xem ảnh phác thảo**, không chỉ đọc YAML.

## Cảnh chân thật (luật từ 28/11/2026)
- **Cảnh minh hoạ** (sông, biển, núi, đá, đáy biển, bản đồ…) dùng `kind: scene`:
  - Mô tả như phong cảnh thật: sông có núi, cây và dòng sông uốn lượn; biển là bãi biển.
  - Chỉ dùng màu trong `scene_palette`.
  - Đặt phủ cả khung `box {x: 0, y: 0, w: 100, h: 100}` và luôn là **phần tử đầu tiên** của khung, tức lớp dưới cùng.
- **Icon, chữ, nút** chỉ dùng `palette` (4 màu nhận diện).
- Mọi chữ nằm trên cảnh có `text_plate` (đặt một lần ở đầu file). DSN-A05 đo tương phản với màu sáng nhất của cảnh.
- **Vị trí phần tử theo vị trí thật trong cảnh**, ví dụ:
  - hơi nước bốc lên từ mặt biển;
  - muối nằm dưới mặt nước;
  - khoáng chất bay ra từ miệng núi lửa.

## Linh vật của kênh (luật từ 28/11/2026)
- Nếu `brand.mascot` có trong brief, thêm asset `kind: mascot`, `expression: <id>`. Chọn biểu cảm theo cột `use`.
- Khỉ **phản ứng 2–3 lần** ở điểm nhấn thật: nêu câu hỏi, lộ đáp án, quy mô, mẹo. Cùng một Khỉ kéo dài qua khung nối tiếp chỉ tính 1 lần.
- **Cảnh kết bắt buộc có Khỉ** (thêm logo nếu có). DSN-A11 kiểm cả hai luật.
- Đặt Khỉ ở góc hoặc cạnh, không che nội dung chính. Cỡ ≤ 44% chiều cao, vì PNG chỉ 512 px.
- Mọi chữ có tấm nền khi `text_plate.always: true`.
