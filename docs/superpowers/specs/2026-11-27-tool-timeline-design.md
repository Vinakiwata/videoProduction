# Thiết kế: Tool Timeline tổng (05_timeline)

- Ngày: 2026-11-27
- Trạng thái: **Đã duyệt theo uỷ quyền** (chủ dự án: "quay lại tiếp tục với setup tool"). Claude tự quyết, ghi ở mục 5.

## 1. Mục đích
Một file **khoá** toàn bộ thời gian của video, tính bằng **khung hình nguyên** ở fps của brief. Web trình chiếu, render và mix chỉ đọc file này, không tự tính lại.
Mọi thời điểm đều suy ra từ ba nguồn:
- **thời lượng giọng đo thật** (`04_voice/voice_manifest.yaml`);
- **tỉ lệ trong storyboard** (span, `enter.at`, `exit.at`);
- **thời lượng im lặng của kịch bản**.

## 2. Mục tiêu / Không làm / Thất bại nếu
**Mục tiêu**
- **Nhịp thở:** chèn khoảng nghỉ giữa hai đoạn giọng liền nhau. Mặc định 0,35 giây (khớp khoảng ngắt giữa các câu trong đoạn); 0,45 giây sau câu hỏi hoặc câu cảm thán; không chèn khi đoạn kế là im lặng (đã có nghỉ sẵn).
  Khoảng thở được tính vào **khung cuối** của đoạn trước, nên hình đứng lại trong lúc thở, không đứt.
- **Làm tròn theo khung:** mọi mốc làm tròn về khung gần nhất. Thời lượng một đoạn tính bằng hiệu hai mốc đã làm tròn, nên không có sai số cộng dồn.
- **Rãnh (track):**
  - `voice`: đoạn, file, khung bắt đầu và kết thúc;
  - `shots`: phủ kín 0 → tổng, không hở, không chồng;
  - `cues`: từng sự kiện vào, ra, lặp của phần tử, đổi ra khung tuyệt đối;
  - `sfx`;
  - `music`: để trống, Tool mix sẽ điền.
- **Phụ đề `subtitles.srt`:** mỗi đoạn giọng tách thành dòng ≤ 42 ký tự, ngắt ở dấu câu hoặc trước từ nối, mỗi cụm tối đa 2 dòng. Thời gian chia theo số âm tiết trong đoạn, mỗi cụm hiện ≥ 1 giây, không chồng nhau.
- **`manifest.json`** lưu mã băm đầu vào. Kịch bản, storyboard, giọng hoặc tham số đổi thì cổng chặn.

**Không làm:** chưa có nhạc nền (Tool mix chọn nhạc có giấy phép), chưa căn phụ đề theo từng từ (cần ASR).

**Thất bại nếu:** có hai nơi tự tính thời gian; một sự kiện rơi ra ngoài khung hình của nó; phụ đề chữ khác lời đọc.

## 3. Kiểm tra tự động mới
| Tên | Kiểm gì |
|---|---|
| `timeline_consistency` | Thời lượng giọng = manifest (±1 khung); giọng không chồng; shots phủ kín và nối liền; mọi cue nằm trong khung của nó; tổng khung = tổng thời lượng × fps; thứ tự đoạn = kịch bản |
| `subtitles_valid` | SRT đọc được; ≤ 2 dòng, ≤ 42 ký tự mỗi dòng; hiện ≥ 1 giây; không chồng; **chữ ghép lại đúng bằng lời kịch bản** |
| `timeline_in_sync` | Mã băm đầu vào khớp `manifest.json` |

Checklist `timeline` v2: ba mục trên ở mức **chặn**. Bỏ TML-C01, C02, C04, C06 vì đã đo tự động. Giữ phán đoán cho:
- C03: điểm neo cue có nghĩa;
- C05: nhạc;
- C07 (mới): nhịp thở tự nhiên, không hụt, không lê thê.

## 4. Lệnh
`python -m vp timeline build <dự án> [--breath 0.30] [--breath-question 0.45]`. Lệnh chỉ chạy khi cổng `voice` đang MỞ.

## 5. Quyết định của Claude (cần xem lại)
1. Nhịp thở mặc định 0,35 giây, sau câu hỏi hoặc cảm thán 0,45 giây.
2. Phụ đề ≤ 42 ký tự mỗi dòng, ≤ 2 dòng, ≥ 1 giây (theo thói quen phụ đề phát sóng và gợi ý của YouTube).
3. Khoảng thở thuộc về khung cuối của đoạn trước.
