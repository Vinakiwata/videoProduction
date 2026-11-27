---
name: vp-timeline
description: Dùng khi cần dựng, sửa hoặc duyệt timeline tổng (05_timeline) cho video trong repo này — khoá mốc thời gian theo khung hình từ giọng thật + storyboard, chèn nhịp thở, tạo phụ đề .srt.
---

# Timeline tổng (05_timeline)

1. `python -m vp gate projects/<dự án> voice` phải báo MỞ.
2. `python -m vp timeline build projects/<dự án>` (tham số nhịp thở: `--breath 0.30`, `--breath-question 0.45`) tạo:
   - `05_timeline/timeline.yaml`, tính bằng khung hình nguyên, gồm các rãnh `segments / voice / shots / cues / sfx / music`;
   - `subtitles.srt`;
   - `manifest.json`.
3. **Không sửa tay** `timeline.yaml`. Muốn đổi thời gian thì sửa nguồn rồi build lại:
   - giọng (04),
   - storyboard (02, đổi `span` hoặc `at`),
   - hoặc tham số nhịp thở.
4. Kiểm nhanh: đọc bảng `cues` cạnh lời đọc. Phần tử minh hoạ từ khoá phải vào ngay trước hoặc đúng lúc từ khoá được nói.
5. Duyệt bằng skill `vp-kiem-duyet`, công đoạn `timeline`. Từ đây trở đi, web trình chiếu, render và mix chỉ đọc `timeline.yaml`.
