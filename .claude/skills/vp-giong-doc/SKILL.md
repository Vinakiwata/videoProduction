---
name: vp-giong-doc
description: Dùng khi cần tạo, nhập, sửa hoặc duyệt giọng đọc cho video trong repo này (công đoạn 04_voice) — bằng VieNeu-TTS hoặc file người tự thu — kể cả hiệu chỉnh tốc độ đọc của kênh và đưa giọng về animatic.
---

# Giọng đọc (04_voice)

1. `python -m vp gate projects/<dự án> animatic` phải báo MỞ.
2. **Chọn nguồn giọng:**
   - **VieNeu-TTS** (mặc định). Cần mạng ở lần đầu để chạy `pip install vieneu` và tải mô hình.
     `python -m vp voice synth projects/<dự án>`. Mặc định đọc 2 lượt mỗi đoạn và chọn lượt tốt hơn. Giọng lấy từ `brand.voice`.
   - **Người tự thu.** `python -m vp voice sheet projects/<dự án>` tạo `04_voice/recording_sheet.md`.
     Gửi phiếu này cho người đọc. Nhận lại file `<mã đoạn>.m4a/.wav/.mp3` vào `04_voice/recordings/`, rồi chạy
     `python -m vp voice synth projects/<dự án> --engine recording`.
3. Tool tự áp phát âm, cắt lặng, chuẩn −16 LUFS, đo thời lượng và chất lượng, rồi ghi `voice_manifest.yaml` và `voice_full.wav`.
   Đoạn nào lỗi thì tạo lại riêng đoạn đó: `--only S02-01,S04-03`.
4. **Nghe thật từng đoạn** trước khi giao duyệt: đọc sót hay sai chữ, phát âm tên riêng, tạp âm, ngữ điệu.
   Lỗi phát âm thì thêm vào `meta.pronunciation` của kịch bản. Việc này làm thay đổi kịch bản, nên cổng `script` phải duyệt lại.
5. `python -m vp voice calibrate projects/<dự án> --apply` ghi tốc độ đọc thật vào hồ sơ kênh.
6. **Duyệt lại nhịp với giọng thật:**
   - `python -m vp voice to-animatic projects/<dự án>`
   - `python -m vp animatic build projects/<dự án>`
   - duyệt lại cổng `animatic`
   - sau đó duyệt cổng `voice` bằng skill `vp-kiem-duyet`.
