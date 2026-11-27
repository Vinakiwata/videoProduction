---
name: vp-animatic
description: Dùng khi cần dựng hoặc duyệt animatic (video nháp duyệt nhịp) cho video trong repo này — sau khi storyboard qua cổng 'design', hoặc khi có giọng nháp mới cần dựng lại animatic.
---

# Animatic — video nháp duyệt nhịp

Mục đích: duyệt **nhịp, thứ tự, sự khớp lời–hình** khi việc sửa còn rẻ. Chưa cần đẹp.

1. `python -m vp gate projects/<dự án> design` phải báo MỞ.
2. **Giọng nháp (nên có):** đặt `03_animatic/scratch_voice/<mã đoạn>.wav`, mỗi đoạn giọng một file WAV 16-bit.
   Nguồn có thể là VieNeu-TTS hoặc người tự thu. Đoạn nào có file thì thời lượng lấy theo file, đoạn nào không có thì lấy theo ước tính của kịch bản.
3. `python -m vp animatic build projects/<dự án>` tạo:
   - `03_animatic/animatic.mp4`: hình 960×540 cộng dải phụ đề 96 px **bên dưới**, 15 fps;
   - `timing.yaml`: mốc từng đoạn và từng khung, kèm nguồn thời lượng;
   - `manifest.json`.
4. **Xem thật.** Trích khung mỗi giây rồi xem tuần tự:
   ```bash
   ffmpeg -i projects/<dự án>/03_animatic/animatic.mp4 -vf "fps=1,scale=320:-2" /tmp/a/f%03d.png
   ffmpeg -pattern_type glob -i '/tmp/a/f*.png' -vf tile=6x6:padding=4 /tmp/a/sheet%d.png
   ```
   Tìm: khoảng chết > 4 giây, cụm dồn dập, hình đến trước hoặc sau lời, chữ bị che.
5. Lỗi ở nhịp hay hình thì sửa **storyboard** (Tool 3, cổng design phải duyệt lại). Lỗi ở lời hay độ dài thì sửa **kịch bản** (Tool 1, các cổng sau đều phải duyệt lại).
6. Duyệt bằng skill `vp-kiem-duyet`, công đoạn `animatic`.
