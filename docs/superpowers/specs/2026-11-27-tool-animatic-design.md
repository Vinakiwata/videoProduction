# Thiết kế: Tool Animatic (03_animatic)

- Ngày: 2026-11-27
- Trạng thái: **Đã duyệt theo uỷ quyền** (chủ dự án yêu cầu "làm bước tiếp theo"; Claude tự quyết, ghi ở mục 6)

## 1. Mục đích
Một video nháp ghép các khung storyboard theo đúng mốc thời gian, để **duyệt nhịp độ, thứ tự và sự khớp giữa lời và hình** trước khi tốn công vẽ hoạt ảnh thật.
Đây là chốt chặn cuối mà việc đổi cấu trúc vẫn còn rẻ.

## 2. Mục tiêu / Không làm / Thất bại nếu
**Mục tiêu**
- Lấy thời lượng mỗi đoạn từ **giọng nháp** nếu có (`03_animatic/scratch_voice/<mã đoạn>.wav`, do người thu hoặc TTS tạo). Không có thì dùng `est_duration_s` của kịch bản.
  File `timing.yaml` ghi rõ nguồn của từng đoạn (`scratch` hoặc `estimate`).
- Hình: ảnh phác thảo của storyboard, với từng phần tử **hiện ra và biến mất đúng `enter.at` / `exit.at`** (mờ dần theo `dur_s`). Camera và hiệu ứng chi tiết chưa làm.
- Lời: phụ đề lớn ở **dải riêng bên dưới khung hình**, không che hình (lời của đoạn đang chạy), kèm mã khung và mốc thời gian ở góc. Ai duyệt cũng theo dõi được, kể cả khi chưa có giọng.
- Tiếng: giọng nháp (nếu có) cộng tiếng động mô phỏng tổng hợp bằng code, đặt đúng thời điểm sự kiện của phần tử gắn với nó.
- Tất định: cùng đầu vào thì ra cùng video. `manifest.json` lưu mã băm đầu vào, để cổng biết khi nào animatic đã cũ.

**Không làm:** chưa có hoạt ảnh thật, chưa có camera, chưa có chuyển cảnh mềm, chưa có nhạc nền.

**Thất bại nếu:** mốc thời gian trong animatic khác mốc mà timeline sau này dùng; người duyệt không biết đang xem giọng thật hay ước tính.

## 3. Các cách đã cân nhắc
| Cách | Kết luận |
|---|---|
| A. Chờ có VieNeu-TTS rồi mới làm animatic | Loại: chặn cả dây chuyền vì một điều kiện ngoài, trong khi nhịp hình đã duyệt được |
| **B. Animatic phụ đề + tiếng động mô phỏng, tự nhận giọng nháp khi có** | **Chọn**: đúng thực hành studio khi chưa thu giọng |
| C. Quay màn hình web trình chiếu | Loại: web trình chiếu là Tool 07, chưa có |

## 4. Thành phần
- `vp/animatic.py`:
  - `compute_timing()` tính mốc đoạn và khung, ghi `timing.yaml`.
  - `build_audio()` dựng WAV 48 kHz mono, đúng tổng thời lượng.
  - `render()` vẽ khung (hình 960×540 + dải phụ đề 96 px = 960×636, mặc định 15 fps), đẩy luồng sang ffmpeg, rồi ghép tiếng.
- `vp/sfx_synth.py`: tiếng động mô phỏng tổng hợp bằng numpy. Tên SFX được ánh xạ theo từ khoá: pop, click, whoosh, nước/róc rách, lách tách; tên khác thì dùng "blip". Đây chỉ là tiếng nháp; Tool mix sẽ dùng thư viện SFX có giấy phép.
- Lệnh: `python -m vp animatic build <dự án> [--fps 15]`. Lệnh này yêu cầu cổng `design` đang MỞ.
- Kiểm tra tự động mới:
  - `animatic_in_sync`: mã băm storyboard, kịch bản, giọng nháp và tham số khớp `manifest.json`.
  - `animatic_duration`: thời lượng video khớp `timing.yaml` (±1 khung).

## 5. Checklist `animatic` v2
- Máy đo:
  - Có file (`animatic.mp4`, `timing.yaml`).
  - Định dạng 960×636 @ 15 fps.
  - Hình và tiếng khớp nhau.
  - `animatic_in_sync` (chặn).
  - `animatic_duration` (chặn).
- ATC-C03 (chỉ nghe) cho phép `na` **khi chưa có giọng nháp**, và phải ghi rõ lý do.
- Thêm ATC-C06 (nhẹ): nguồn thời lượng. Nếu toàn bộ là ước tính, ghi rủi ro lệch nhịp và yêu cầu kiểm lại ở cổng `voice` và `timeline`.

## 6. Quyết định của Claude (cần xem lại)
1. Animatic 960×636 @ 15 fps (dải phụ đề nằm ngoài khung hình; phát hiện khi chạy thật: phụ đề đè lên sẽ che chữ ở 18% dưới khung): đủ để duyệt nhịp, render nhanh. Bản cuối vẫn là 1920×1080 @ 30 fps.
2. Phần tử chỉ mờ vào và mờ ra; các hiệu ứng pop, slide, draw… đều mô phỏng bằng mờ dần.
3. Chưa có giọng thật, nên animatic lần này dùng phụ đề, và nhịp dựa trên ước tính 3,2 âm tiết/giây.
