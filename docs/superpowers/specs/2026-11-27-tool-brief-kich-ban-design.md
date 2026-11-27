# Thiết kế: Tool 0 (Brief) và Tool 1 (Kịch bản)

- Ngày: 2026-11-27
- Trạng thái: **Đã duyệt theo uỷ quyền.** Chủ dự án chưa tham gia duyệt, Claude tự quyết và ghi lại ở mục 7.
- Dựa trên: `2026-11-27-kien-truc-va-kiem-duyet-design.md`

## 1. Mục đích
- **Tool 0** biến một yêu cầu, dù chỉ một câu, thành `00_brief/brief.yaml` đủ chặt để làm thước đo cho mọi công đoạn sau.
- **Tool 1** nhận **ý tưởng** hoặc **bản kịch bản có sẵn** của chủ dự án, rồi tạo ra `01_script/script.yaml` hoàn chỉnh: đúng sự thật, có nguồn, viết để nghe, đọc được bằng TTS, mô tả hình đủ để thiết kế 2D. Kịch bản phải qua được cổng `script` (30 mục).

## 2. Mục tiêu / Không làm / Thất bại nếu
**Mục tiêu**
- Bộ nhận diện **dùng chung cho cả kênh**, để mọi video cùng một phong cách mà không phải khai lại.
- Mọi giả định Claude tự đưa ra khi chủ dự án vắng mặt đều được **ghi vào brief** (`assumptions`), để chủ dự án xem lại và người duyệt nhìn thấy.
- Thời lượng ước tính **tính bằng code** từ số âm tiết, không đoán tay.
- Tự kiểm nhanh mà không mở lần duyệt chính thức, nên sửa vòng nhỏ được nhiều lần mà nhật ký không bị nhiễu.
- Có bản đọc `script.md` dạng bảng (lời, hình, mốc thời gian) để chủ dự án xem trên GitHub.
- Kịch bản do chủ dự án đưa vào được **giữ giọng văn và ý**. Mọi thay đổi được ghi vào `01_script/changes.md`.

**Không làm:** chưa gọi API AI từ code; chưa tạo giọng (đó là Tool giọng đọc).

**Thất bại nếu:** kịch bản đọc thì hay nhưng nói ra thì vấp; có khẳng định sai lọt qua; brief có giả định ngầm mà không ai thấy.

## 3. Các cách đã cân nhắc
| Cách | Kết luận |
|---|---|
| A. Chỉ có skill: Claude viết YAML bằng tay theo hướng dẫn | Loại: thời lượng đoán tay, không có vòng kiểm nhanh, nhập bản thảo dễ sai |
| **B. Skill (phần sáng tạo, nghiên cứu) + lệnh code hỗ trợ (đo, nhập, kiểm, xuất bản đọc)** | **Chọn** |
| C. Code gọi API AI để viết kịch bản | Loại ở giai đoạn này (đã chốt trước đó) |

## 4. Thành phần

### 4.1 Hồ sơ kênh: `channels/<kênh>/channel.yaml`
Gồm `name`, `channel`, `format`, `tone`, `cta`, `brand {colors, fonts, voice}`, `audience`, `voice_profile {syllables_per_second}`.
Schema nằm ở `vp/schemas/channel.schema.json`.

### 4.2 Tool 0: `python -m vp brief new <dự án> --channel <kênh> --title "…" [--goal …] [--audience …] [--duration 60] [--ads]`
- Tạo khung dự án nếu chưa có, rồi ghi `00_brief/brief.yaml`, gộp hồ sơ kênh với tham số dòng lệnh. Tham số dòng lệnh được ưu tiên.
- Trường chưa có giá trị được ghi `"TODO: …"`, để cổng `brief` chặn cho tới khi Claude hoặc chủ dự án điền xong.
  Muốn vậy, mục kiểm `script_no_placeholders` được tổng quát hoá thành `no_placeholders` (quét mọi chuỗi trong một file YAML).
- Brief có thêm `channel_ref` và `assumptions: [..]`.

### 4.3 Tool 1: các lệnh `python -m vp script …`
| Lệnh | Việc |
|---|---|
| `import <dự án> <file.md/.txt>` | Đọc bản thảo. Dòng `# …` là tiêu đề cảnh, đoạn văn là lời đọc, tách câu khi vượt 200 ký tự. Dòng `> …` là ghi chú hình cho đoạn ngay trước. Đoạn thiếu hình được ghi `TODO: mô tả hình`. Lệnh này **không ghi đè** kịch bản đã có, trừ khi dùng `--force`. |
| `estimate <dự án> [--sps N]` | Tính `est_duration_s` cho mọi đoạn giọng: âm tiết / sps, làm tròn lên 0,1 giây, tối thiểu 0,5 giây. Không cộng thêm thời gian nghỉ: muốn nghỉ thì viết thành đoạn im lặng `(im lặng 1.5)`, nếu không đoạn ngắn sẽ bị tính đọc quá chậm. sps lấy theo thứ tự: tham số dòng lệnh, `voice_profile` của kênh, rồi mặc định 3,2. Đoạn im lặng giữ nguyên. |
| `lint <dự án>` | Chạy mọi mục **tự động** của checklist `script` và in kết quả. Không mở lần duyệt, không ghi nhật ký. Mã thoát 1 nếu có mục trượt. |
| `view <dự án>` | Ghi `01_script/script.md`: bảng gồm mốc bắt đầu, mã đoạn, loại, lời, hình, SFX, thời lượng, kèm tổng thời lượng và danh sách nguồn. |

Checklist `script` có thêm **SCR-A08** (nhẹ, tự động): `script.md` phải khớp `script.yaml`. Kiểm tra mới `script_view_in_sync` tạo lại bản đọc trong bộ nhớ rồi so với file.

### 4.4 Skill
- `vp-brief`: cách rút brief từ yêu cầu; danh sách câu hỏi khi chủ dự án có mặt; cách ghi giả định khi họ vắng mặt.
- `vp-kich-ban`: quy trình gồm cổng brief → phân loại đầu vào → nghiên cứu (`research.md`, mỗi khẳng định quan trọng có ≥ 1 nguồn uy tín) → dàn ý → viết để nghe → phát âm → mô tả hình → `estimate` → `lint` → `view` → tự soát theo checklist → chuyển sang `vp-kiem-duyet`.

## 5. Dữ liệu mới / thay đổi
- `brief.schema.json`: thêm `channel_ref` (chuỗi) và `assumptions` (mảng chuỗi).
- `script.schema.json`: không đổi.
- `checklists/brief.yaml`: thêm **BRF-A02** (chặn, tự động) dùng `no_placeholders` trên brief, và **BRF-C07** (nghiêm trọng, ai) yêu cầu mọi giả định phải hợp lý và được nêu rõ.
- `checklists/script.yaml`: SCR-A04 chuyển sang dùng `no_placeholders`, thêm SCR-A08.

## 6. Kiểm thử
Có unit test cho: gộp hồ sơ kênh, ghi TODO, `no_placeholders` (bỏ qua thẻ cảm xúc), nhập bản thảo (tiêu đề cảnh, ghi chú hình, tách câu dài, không ghi đè), ước lượng (công thức, làm tròn), `view` (mốc thời gian luỹ kế), `lint` (mã thoát), và `script_view_in_sync`.

## 7. Quyết định của Claude (cần xem lại)
1. Tốc độ đọc mặc định 3,2 âm tiết/giây, không cộng thời gian nghỉ vào đoạn giọng. Sẽ hiệu chỉnh khi có giọng VieNeu thật.
2. Khi nhập bản thảo, câu dài hơn 200 ký tự thì tách (giới hạn cứng của cổng là 300), để TTS ổn định hơn.
3. Kênh mẫu `kenh-khoa-hoc-mau` chỉ để chạy thử. Chủ dự án cần cung cấp bộ nhận diện thật.
4. Chỉnh checklist (BRF-A02, BRF-C07, SCR-A08, SCR-A04) là thay đổi có chủ đích, kèm lý do ở mục 5, không nhằm cho sản phẩm nào lọt cổng.
