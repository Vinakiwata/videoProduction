# Thiết kế: Tool Giọng đọc (04_voice)

- Ngày: 2026-11-27
- Trạng thái: **Đã duyệt theo uỷ quyền** (chủ dự án: "bước tiếp theo giúp tôi"). Claude tự quyết, ghi ở mục 6.

## 1. Mục đích
Tạo giọng đọc cho mọi đoạn `voice` của kịch bản đã khoá. **Đo thời lượng thật** của từng đoạn, vì timeline và hình sau này đều chạy theo số đo này.
Kèm theo là các phép đo máy để bắt lỗi thường gặp của TTS: vỡ tiếng, câu bị cắt, khoảng lặng lạ giữa câu, đọc quá nhanh hay quá chậm bất thường.

## 2. Mục tiêu / Không làm / Thất bại nếu
**Mục tiêu**
- Hai nguồn giọng, dùng chung một đường xử lý:
  - `vieneu`: VieNeu-TTS v3 Turbo, giọng lấy từ `brand.voice` (vd. "VieNeu-TTS v3 Turbo: Ngọc Lan").
  - `recording`: file người thu trong `04_voice/recordings/<mã đoạn>.<wav|m4a|mp3|…>`. Thu bằng điện thoại cũng được.
- **Phát âm:** áp `meta.pronunciation` của kịch bản trước khi đưa vào TTS. Mọi thay thế đều được ghi lại.
- **Xử lý mỗi đoạn:**
  - đổi về 48 kHz mono;
  - cắt lặng đầu và cuối, chừa đệm 0,08 giây;
  - chuẩn âm lượng −16 LUFS, đỉnh −1,5 dBTP (ffmpeg loudnorm).
- **Nhiều lượt đọc (takes):** TTS có ngẫu nhiên. Với `--takes N`, mỗi đoạn được đọc N lần, rồi chọn lượt có điểm tốt nhất: ít khoảng lặng giữa câu bất thường, tốc độ gần tốc độ trung vị.
- **Kết quả:**
  - `04_voice/segments/<mã>.wav`;
  - `voice_full.wav`: các đoạn nối theo thứ tự, đoạn im lặng chèn đúng thời lượng của kịch bản;
  - `voice_manifest.yaml`: thời lượng, số đo chất lượng, mã băm, văn bản đã đọc.
- **Hiệu chỉnh:** `vp voice calibrate --apply` ghi tốc độ đọc đo thật vào `voice_profile` của kênh, để các video sau ước lượng đúng hơn.
- **Đưa về animatic:** `vp voice to-animatic` chép giọng sang `03_animatic/scratch_voice/`. Cổng animatic sẽ hết hiệu lực, nên phải dựng lại và duyệt lại nhịp với giọng thật. Đây là chủ đích.

**Không làm:** nhận dạng giọng nói (ASR) để so chữ tự động, vì môi trường chưa có mô hình. Mục "đọc đúng từng chữ" vẫn do người hoặc AI nghe và chấm.

**Thất bại nếu:** thời lượng ghi trong manifest khác file thật; manifest cũ vẫn qua cổng sau khi kịch bản đổi; lỗi TTS lọt qua mà không có số đo nào cảnh báo.

## 3. Các cách đã cân nhắc
| Cách | Kết luận |
|---|---|
| A. Gọi API VieNeu v4 (trả phí, giọng tốt hơn) | Để sau. Thiết kế engine dạng cắm được nên thêm vào dễ |
| **B. VieNeu v3 Turbo chạy cục bộ + nguồn thu âm, chung một đường xử lý và đo** | **Chọn**: miễn phí, Apache 2.0, chạy được bằng CPU |
| C. Chỉ dùng thu âm người | Loại làm mặc định: tốn công, khó đồng nhất. Vẫn giữ làm nguồn thứ hai |

## 4. Kiểm tra tự động mới
| Tên | Kiểm gì |
|---|---|
| `voice_manifest` | Mọi đoạn `voice` có giọng. Văn bản đã đọc bằng văn bản kịch bản sau khi áp phát âm (kịch bản đổi thì cổng chặn). File tồn tại, mã băm khớp, thời lượng khớp file (±0,01 giây) |
| `voice_segment_quality` | Mỗi đoạn: đỉnh ≤ −1 dBFS; lặng đầu và cuối ≤ 0,35 giây; lặng giữa câu ≤ 1,0 giây; tốc độ 2,0–5,0 âm tiết/giây (ngoài khoảng này thường là câu bị cắt hoặc TTS đọc lỗi) |
| `audio_loudness` (đã có) | `voice_full.wav` ở −16 ±1,5 LUFS, đỉnh ≤ −1 dBTP |

Checklist `voice` v2: thêm hai mục trên ở mức **chặn**. Bỏ VOI-C06 (đo thời lượng) vì đã tự động.

## 5. Lệnh
```
python -m vp voice synth <dự án> [--engine vieneu|recording] [--takes 2] [--only S01-01,S02-01]
python -m vp voice calibrate <dự án> [--apply]
python -m vp voice to-animatic <dự án>
```

## 6. Quyết định của Claude (cần xem lại)
1. Âm lượng giọng −16 LUFS (bản mix cuối sẽ lên −14 LUFS). Đệm 0,08 giây ở hai đầu mỗi đoạn.
2. Mặc định 2 lượt đọc mỗi đoạn với VieNeu, chọn lượt tốt hơn theo số đo.
3. Giữ watermark mặc định của VieNeu (nếu gói `resemble-perth` có cài). Việc này hỗ trợ nghĩa vụ đánh dấu nội dung AI ở định dạng máy đọc (Luật Trí tuệ nhân tạo 134/2025/QH15).
4. Môi trường hiện **chưa có mạng**, nên phần chạy thật với VieNeu chưa làm được. Code đã được kiểm thử bằng engine giả lập và bằng file thu âm giả lập.
