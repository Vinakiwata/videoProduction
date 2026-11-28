---
name: vp-trinh-chieu
description: Dùng khi cần dựng, sửa hoặc duyệt web trình chiếu (07_presentation) cho video trong repo này — biến timeline + storyboard + hình đã duyệt thành một trang tất định theo khung của brief (1080×1920 cho Shorts/TikTok/Reels), chụp kiểm bằng Chrome chạy ngầm, dựng tờ khung mốc.
---

# Web trình chiếu (07_presentation)

Trang web là **bộ dựng duy nhất**: Tool 08 chụp chính trang này thành khung hình. Cái gì sai ở đây sẽ sai trong video.
Thiết kế: `docs/superpowers/specs/2026-11-28-tool-trinh-chieu-design.md`.

1. `python -m vp gate projects/<dự án> animation` phải báo MỞ.
2. **Font nhận diện** nằm ở `channels/<kênh>/brand/fonts/` (file .ttf theo độ đậm + `OFL.txt`). Thiếu font thì PRS-A03 chặn. Máy dựng không có mạng: nhờ chủ dự án tải và đặt vào `~/Documents/DEV_WORK_SUB/VieNeu-TTS/fonts/`, rồi chép sang (chỉ dùng đúng thư mục này trên máy họ).
3. **Chuyển động lớp** khai trong `06_animation/assets.yaml` → `motion: [{layer, recipe, ...}]`. Công thức:
   - `bob` (amp, ax, period_s), `rotate` (center, period_s), `twinkle`/`pulse_opacity` (lo, hi, period_s), `dashflow` (speed: nét đứt trôi).
   - `rise`/`fall` (dx, dy, period_s): nhân đôi lớp, trôi lặp liền mạch. Nội dung lớp phải phủ rộng hơn khung một chu kỳ, kẻo lộ chỗ nối.
   - `along`: hạt chạy dọc đường. Nguồn đường: `path` (đường ẩn `data-flow` trong lớp, sinh bằng `flow_path()` ở `canh.py`), `paths_from` (lớp khác, ví dụ `rivers`) hoặc `paths` (chuỗi d). Tham số: `spacing` px hoặc `count`, `period_s` (thời gian đi một khoảng cách), `stagger`, `shape` ripple|dot, `fade`.
   - **Cảnh (`kind: scene`) có loop trong storyboard bắt buộc có `motion`.** Không trôi hay đập cả khối cảnh; PRS-A07 chặn.
   - Thêm hay sửa motion là đổi `assets.yaml`, nên phải duyệt lại cổng 06 trước.
4. `python -m vp presentation build projects/<dự án>`: biên dịch `presentation.json`, chép hình, trộn giọng thành `audio/voice.wav`, nhúng font base64 và SVG vào `data.js` (mở `file://` vẫn chạy).
5. `python -m vp presentation check projects/<dự án>`: Chrome chạy ngầm chụp các khung mốc (đầu, giữa, cuối mỗi khung hình, giữa mỗi lượt chuyển cảnh) hai lượt xuôi rồi ngược, ghi `check/check_manifest.json`.
6. `python -m vp presentation preview projects/<dự án>`: tạo `check/contact.png`. **Tự mở xem**, đối chiếu với `02_design/frames/`.
7. `python -m vp presentation lint projects/<dự án>` phải báo SẠCH.
8. Duyệt bằng skill `vp-kiem-duyet`, công đoạn `presentation`. **PRS-C03 (chuyển động khớp lời) do chủ dự án chấm**: chép thư mục `07_presentation` sang máy họ (thư mục VieNeu-TTS) để họ mở `index.html`, bấm Phát và xem có tiếng.

## Luật của bộ dựng (`vp/web/player.js`)
- Mỗi khung là hàm thuần của số khung: không `Date`, `Math.random`, đồng hồ thật hay CSS animation.
- Mỗi lần `seek` tháo rồi gắn lại cây khung hình. Không dùng `will-change`, vì Chrome sẽ giữ phần đã vẽ ở tỉ lệ cũ và ảnh phụ thuộc lịch sử tua; PRS-A05 sẽ bắt.
- Phần tử phải nằm trong DOM thì mới đo được `getBBox`/`getTotalLength`.
- Chữ là lớp phủ ngoài camera, có tấm nền `text_plate`. `vp.measure()` đo chữ tràn và vùng an toàn, bỏ qua khung đang chuyển cảnh.
- Khung đầu một khung hình được phép trống trước lượt vào đầu tiên. Giữa hay cuối khung hình mà trống thì PRS-A04 chặn.

## Khung dọc và lớp phủ nền tảng (từ 28/11/2026)
- Khung và vùng an toàn lấy từ brief: `presentation.json` có `safe_margins` (px từng cạnh, `by` = nền tảng quyết định cạnh) và `platforms` (tên + `ui_zones`).
- `vp.measure()` báo "chữ ra ngoài vùng an toàn ở cạnh … (<nền tảng> che)".
- Chế độ xem: ô **giao diện** chọn Shorts / TikTok / Reels để tô mờ vùng giao diện che; ô **vùng an toàn** vẽ khung lề. Bản dựng (`?render=1`) không có lớp phủ.
- `preview` tạo thêm `check/contact_ui.png`: tờ khung mốc chồng giao diện của nền tảng che nhiều nhất — xem để chắc không chữ, Khỉ, nút nào bị che.
- Chủ dự án xem bản có tiếng bằng cách chép thư mục `07_presentation` (trừ `check/`, `fonts/`, `presentation.json`) sang máy họ.
