# Thiết kế: Kiến trúc chung & Tool kiểm duyệt (Cổng duyệt)

- Ngày: 2026-11-27
- Trạng thái: **Đã duyệt theo uỷ quyền.** Chủ dự án uỷ quyền cho Claude tự quyết và ghi lại, sẽ xem lại sau.
- Phạm vi: (1) kiến trúc chung mà mọi tool dùng; (2) tool kiểm duyệt dùng chung, chạy ở **mọi** điểm duyệt.

## 1. Mục đích và lý do

Chủ dự án muốn có một dây chuyền sản xuất video YouTube bằng code. Dây chuyền gồm các tool riêng lẻ, mỗi tool làm một việc, nối lại thành một quy trình. Ưu tiên **chất lượng từ đầu, không cần nhanh**.

Chủ dự án hiện **chưa tham gia duyệt**. Vì vậy cần một tool kiểm duyệt **chặt chẽ, dựa trên checklist**, thay chủ dự án đứng ở các cổng duyệt. Kết quả mọi lần duyệt phải lưu lại để chủ dự án **vào xem lại khi cần**.

## 2. Mục tiêu / Không làm / Thất bại nếu

**Mục tiêu**
- Mỗi công đoạn có một checklist rõ ràng. Mỗi mục có mức độ (chặn / nghiêm trọng / nhẹ) và cách chấm (máy tự đo / AI phán đoán).
- Mục máy đo được thì **code đo**, không để AI "ước chừng".
- Mục AI phán đoán **bắt buộc có bằng chứng**: trích dẫn, vị trí hoặc số liệu. Mục trượt bắt buộc có hướng sửa.
- Có mục chặn hoặc nghiêm trọng trượt thì **công đoạn sau không được chạy**.
- Báo cáo đọc được bằng tiếng Việt. Có sổ nhật ký duyệt cho mỗi dự án.
- Sửa sản phẩm sau khi đã duyệt thì kết quả duyệt **tự mất hiệu lực**, kiểm tra bằng mã băm (hash) file.

**Không làm (giai đoạn này)**
- Chưa xây các tool sản xuất (kịch bản, giọng, hoạt ảnh…). Chỉ định nghĩa chỗ chúng cắm vào.
- Chưa gọi API AI từ code. Phần phán đoán do Claude thực hiện trong phiên làm việc, theo skill `vp-kiem-duyet`.

**Thất bại nếu** (dù chạy được)
- Duyệt "cho qua": có thể chấm ĐẠT mà không có bằng chứng.
- Kết quả duyệt cũ vẫn còn hiệu lực sau khi file đã bị sửa.
- Báo cáo dài mà không chỉ ra được cần sửa gì, ở đâu.

## 3. Quy trình 12 công đoạn

Bảng dưới đối chiếu với đánh số ý tưởng ban đầu của chủ dự án.

| Mã công đoạn | Thư mục | Việc | Ý tưởng gốc |
|---|---|---|---|
| `brief` | `00_brief` | Brief: mục tiêu, khán giả, kênh, độ dài, bộ nhận diện | *(mới)* |
| `script` | `01_script` | Kịch bản chi tiết | Tool 1 |
| — | — | **Cổng duyệt `script` chính là Tool 2 (kiểm duyệt kịch bản)** | Tool 2 |
| `design` | `02_design` | Thiết kế trình bày, storyboard, điểm rơi, âm thanh | Tool 3 |
| `animatic` | `03_animatic` | Bản nháp thô (khung tĩnh + giọng nháp) để duyệt nhịp | *(mới)* |
| `voice` | `04_voice` | Sản xuất giọng (VieNeu-TTS) + đo thời lượng | Tool 8 → **đưa lên trước** |
| `timeline` | `05_timeline` | Timeline tổng: giọng / im lặng / SFX / nhạc / phụ đề, khoá lại | Tool 5 |
| `animation` | `06_animation` | Hoạt ảnh 2D (SVG/CSS/Canvas/Lottie) + QA | Tool 4 |
| `presentation` | `07_presentation` | Web trình chiếu 1920×1080 chạy theo timeline | Tool 6 |
| `render` | `08_render` | Render từng khung hình có kiểm soát (Playwright) | Tool 7 |
| `mix` | `09_mix` | Mix âm thanh, ghép hình + tiếng, phụ đề | Tool 9 |
| `final` | `10_final` | QC tổng, bảng điểm | Tool 10 |
| `package` | `11_package` | Thumbnail, tiêu đề, mô tả, chapters, nhãn AI | *(mới)* |

Quy tắc cổng: công đoạn thứ *n* chỉ được chạy khi cổng của công đoạn *n−1* đang **ĐẠT** (hoặc **CHO QUA CÓ GHI NHẬN**), và các file đã duyệt chưa bị sửa.

## 4. Cấu trúc một dự án video

```
projects/<slug>/
  project.yaml            # tên, ngày tạo, ngôn ngữ, mục tiêu thời lượng
  00_brief/brief.yaml
  01_script/script.yaml
  02_design/ … 11_package/
  reviews/
    LOG.md                # sổ nhật ký mọi lần duyệt
    state.json            # trạng thái cổng hiện tại của từng công đoạn
    <stage>/<YYYYMMDD-HHMMSS>/
      review.json         # dữ liệu duyệt (máy đọc)
      judgments.yaml      # phần chấm của AI/người cho mục phán đoán
      report.md           # báo cáo đọc được
```

Định dạng chính thức của mỗi công đoạn là YAML có schema (JSON Schema trong `vp/schemas/`). Giai đoạn này mới định nghĩa schema cho `brief` và `script`. Các công đoạn sau sẽ có schema riêng khi xây tool đó.

## 5. Các cách đã cân nhắc

| Cách | Ưu | Nhược | Kết luận |
|---|---|---|---|
| A. AI đọc và cho nhận xét tự do | Nhanh, linh hoạt | Không lặp lại được, dễ "cho qua", không đo được | Loại |
| B. Chỉ dùng kiểm tra tự động bằng code | Khách quan, lặp lại được | Không đánh giá được nội dung, pháp luật, độ đúng | Không đủ |
| **C. Checklist lai: code đo + AI chấm từng mục có bằng chứng + luật cổng cứng** | Khách quan ở phần đo được, có trách nhiệm ở phần phán đoán, lặp lại được, truy vết được | Phải viết và duy trì checklist | **Chọn** |

## 6. Thiết kế tool kiểm duyệt

### 6.1 Checklist (`checklists/<stage>.yaml`)
```yaml
stage: script
version: 1
title: Kiểm duyệt kịch bản
artifacts: [01_script/script.yaml]   # các file bị "niêm phong" bằng hash
items:
  - id: SCR-A01
    group: Cấu trúc
    title: Kịch bản đúng định dạng chuẩn
    severity: chan          # chan | nghiem_trong | nhe
    method: auto            # auto | ai
    check: yaml_schema      # tên hàm kiểm tra tự động
    params: {path: 01_script/script.yaml, schema: script}
  - id: SCR-L01
    group: Pháp luật
    title: Không có nội dung bị cấm theo pháp luật Việt Nam
    severity: chan
    method: ai
    guidance: |              # tiêu chí ĐẠT / TRƯỢT cụ thể cho người chấm
      ...
    allow_na: false          # mục chặn mặc định không được "không áp dụng"
```

### 6.2 Quy trình một lần duyệt
1. `python -m vp review start <dự án> <công đoạn>`: kiểm tra tiền điều kiện, băm các file sản phẩm, chạy mọi mục `auto`, tạo `review.json` (trạng thái `pending`) và file `judgments.yaml` mẫu, liệt kê các mục `ai` cần chấm.
2. Claude, theo skill `vp-kiem-duyet`, chấm **từng** mục `ai`. Mỗi mục gồm kết luận, bằng chứng, và hướng sửa nếu trượt.
3. `python -m vp review finalize <dự án> <công đoạn>`: kiểm tra phần chấm thật nghiêm, ra quyết định cổng, ghi `report.md`, cập nhật `state.json` và `LOG.md`.
4. `python -m vp gate <dự án> <công đoạn>`: mã thoát 0 khi cổng ĐẠT và file chưa bị sửa. Các tool sản xuất gọi lệnh này trước khi chạy.

### 6.3 Luật chấm (không có ngoại lệ)
- Mỗi mục `ai` phải có `verdict` ∈ {`pass`, `fail`, `na`}.
- `evidence` bắt buộc, tối thiểu 20 ký tự, với **mọi** kết luận, kể cả `pass`.
- `fail` bắt buộc có `fix`, tối thiểu 10 ký tự.
- `na` chỉ được dùng khi mục có `allow_na: true`, và `evidence` phải nêu lý do.
- Không được ghi đè kết quả của mục `auto`.
- Mục `auto` không chạy được (lỗi công cụ, thiếu file) tính là `error`, và `error` tính như trượt.
- Nếu file sản phẩm bị sửa giữa `start` và `finalize`, từ chối chốt và yêu cầu duyệt lại.

### 6.4 Quyết định cổng
- **KHÔNG ĐẠT**: có ít nhất một mục `chan` hoặc `nghiem_trong` bị `fail`/`error`.
- **ĐẠT**: không có mục chặn hay nghiêm trọng nào trượt. Mục `nhe` trượt được liệt kê thành "cần cải thiện".
- **Điểm chất lượng** (để theo dõi, không quyết định cổng) = tổng trọng số các mục đạt / tổng trọng số các mục áp dụng × 100. Trọng số: chặn 5, nghiêm trọng 3, nhẹ 1.
- **CHO QUA CÓ GHI NHẬN**: chỉ người được ghi tên mới có quyền dùng, qua `python -m vp review override … --by <tên> --reason <lý do>`. Lần cho qua được ghi đậm trong nhật ký.

### 6.5 Hiệu lực
`state.json` lưu hash các file đã duyệt. `gate` băm lại các file hiện tại. Nếu khác, cổng trả về **HẾT HIỆU LỰC** và phải duyệt lại.

### 6.6 Kiểm tra tự động có sẵn (giai đoạn này)
- File: `file_exists`, `yaml_schema`.
- Kịch bản: `script_unique_ids`, `script_source_refs`, `script_no_placeholders`, `script_segment_length`, `script_reading_speed`, `script_total_duration`.
- Media (dùng cho các công đoạn sau, dựa trên ffprobe/ffmpeg): `video_format`, `audio_loudness`, `black_frames`, `freeze_frames`, `av_duration_match`.

Mỗi checklist chỉ được dùng tên kiểm tra đã đăng ký. Bộ test kiểm tra điều này cho mọi checklist.

## 7. Căn cứ pháp lý và nền tảng (cho checklist)

Tra cứu ngày 2026-11-27. Khi duyệt, người chấm phải tra lại nếu nghi ngờ văn bản đã thay đổi.
- Luật An ninh mạng số 116/2025/QH15, hiệu lực 01/7/2026, thay Luật An ninh mạng 2018 và Luật An toàn thông tin mạng 2015.
- Luật Trí tuệ nhân tạo số 134/2025/QH15, hiệu lực 01/3/2026: nội dung âm thanh, hình ảnh, video do AI tạo hoặc chỉnh sửa khi đưa ra công chúng phải được đánh dấu hoặc gắn nhãn. **Hệ quả cho dự án:** video dùng giọng AI (VieNeu-TTS) phải có nhãn AI. Đưa vào checklist `package` và `final`.
- Luật sửa đổi Luật Quảng cáo số 75/2025/QH15, hiệu lực 01/01/2026, kèm Nghị định 342/2025/NĐ-CP: nội dung quảng cáo phải trung thực, chính xác, không gây hiểu nhầm. Có quy định mới về người chuyển tải sản phẩm quảng cáo và việc thông báo đang quảng cáo.
- Nghị định 174/2026/NĐ-CP, hiệu lực 01/7/2026: xử phạt hành chính về thông tin sai sự thật trên mạng, thay phần lớn Nghị định 15/2020.
- YouTube: bắt buộc khai báo nội dung "altered or synthetic" trông như thật. Từ 2026, YouTube còn tự phát hiện và gắn nhãn.

## 8. Quyết định của Claude (chủ dự án cần xem lại)
1. Cổng duyệt `script` thay cho Tool 2 riêng, để tránh hai hệ thống duyệt song song.
2. Mục `nghiem_trong` trượt cũng chặn cổng, không chỉ mục `chan`. Lý do: chủ dự án yêu cầu "chặt chẽ".
3. Tốc độ đọc tiếng Việt chấp nhận được: 2,5–4,0 âm tiết/giây. Đây là giá trị tạm, sẽ hiệu chỉnh khi có giọng VieNeu thật.
4. Độ dài tối đa một đoạn giọng: 300 ký tự, để TTS đọc ổn định và dễ căn thời gian.
5. Viết bằng Python 3 + PyYAML + jsonschema + ffmpeg (đã có sẵn), không cần cài thêm.

## 9. Để lại cho người xây
- Ngưỡng cụ thể của từng kiểm tra media nằm trong `params` của checklist, chỉnh được mà không cần sửa code.
- Giao diện xem báo cáo (web/dashboard) để sau. Giai đoạn này đọc `LOG.md` và `report.md` trên GitHub.
