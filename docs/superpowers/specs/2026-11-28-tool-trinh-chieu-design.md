# Tool 07 — Web trình chiếu 1920×1080 (07_presentation)

**Ngày:** 28/11/2026. Chủ dự án chọn **cách A: trang web là bộ dựng duy nhất**.

## Vì sao
Hình (Tool 06), giọng (Tool 04) và mốc thời gian theo khung (Tool 05) đã có. Bước này ghép tất cả thành một trang có chuyển động thật, để:
- chủ dự án xem được bằng trình duyệt, có tiếng, tua được;
- Tool 08 chụp lại **đúng trang đó** từng khung thành video.

Xem thử và video cuối giống nhau vì cùng một bộ dựng.

## Phương án đã cân nhắc
- **A. Trang web là bộ dựng duy nhất (đã chọn).** Tool 08 dùng Chrome chạy ngầm (có sẵn), điều khiển qua giao thức DevTools bằng Node (có sẵn `WebSocket`). Đã đo: 0,09 giây mỗi khung, 1920×1080, tiếng Việt chuẩn.
- **B. Python ghép SVG làm bộ dựng chính.** Dựng nhanh, nhưng thành hai bộ dựng dễ lệch nhau; rsvg không tự xuống dòng chữ.
- **C. GSAP hoặc Remotion.** Không cài được vì không có mạng; Remotion còn có điều kiện giấy phép.

## Mục tiêu
1. **Tất định:** trạng thái mỗi khung là hàm thuần của số khung. `vp.seek(f)` trả về Promise; gọi lại cùng `f` cho ảnh giống hệt, kể cả khi tua lộn xộn. Không dùng đồng hồ thật khi dựng.
2. Đủ mọi thứ storyboard và timeline đã chốt: lượt vào/ra, vòng lặp, chuyển động lớp trong SVG, camera, chuyển cảnh, chữ có tấm nền, linh vật PNG.
3. Chữ dùng **đúng font của kênh** (Be Vietnam Pro), nhúng file font kèm giấy phép OFL. Không có font thì **chặn cổng**, không âm thầm dùng font thay thế.
4. Trang tự chứa: mở `index.html` là xem được, không cần mạng.

## Không làm
- Không mix âm thanh: xem thử chỉ phát giọng; SFX và nhạc để Tool 09.
- Không xuất video: việc của Tool 08.

## Thiết kế
**Đầu ra** (`07_presentation/`):
- `presentation.json`: cảnh đã biên dịch.
  - canvas, fps, `total_frames`.
  - shots: khung bắt đầu và kết thúc, nền, camera, chuyển cảnh vào kèm số khung chồng.
  - Mỗi phần tử: box, thứ tự lớp, asset hoặc chữ, enter/exit/loop **đã quy ra khung và ease**. Easing lấy từ timeline cue; nếu thiếu thì lấy `motion_defaults` của `assets.yaml`.
  - `text_plate`, chuyển động lớp.
  - `input_hash` của timeline, storyboard và assets.
- `index.html`, `player.js`, `player.css`.
- `assets/`: bản chép SVG/PNG từ 06, trùng hash.
- `fonts/`: Be Vietnam Pro và `OFL.txt`.
- `audio/voice_full.wav`.

**Bộ dựng JS** (không dùng thư viện ngoài):
- **Hai lớp cảnh** để làm chuyển cảnh: khung trước và khung hiện tại. Các kiểu chuyển cảnh:
  - `cut`, `match_cut`: chuyển thẳng.
  - `crossfade`: chồng 8 khung.
  - `push_up`, `push_left`: đẩy 10 khung.
  - `zoom_through`: phóng to khung cũ, khung mới hiện dần, 10 khung.
- **Camera** biến đổi cả lớp cảnh, dùng ease_in_out theo tiến độ khung hình: `zoom_in`, `zoom_out`, `pan_*`.
- **Chữ** là lớp phủ ngoài camera nên không bị phóng hay cắt. Chữ đặt trong div, tự xuống dòng trong box, tấm nền bo góc (đệm 0,4 em) theo `text_plate`.
- **Lượt vào/ra:** fade, pop, scale_in/out, slide_*, drop (kèm bẹp rồi bật lại 4 khung), grow, wipe, draw (lộ dần nét SVG bằng dash), typewriter (lộ từng ký tự), morph (mờ chồng sang asset mới).
- **Vòng lặp mức phần tử:** bob, pulse, rotate, wiggle, shimmer, blink_slow, flow (giọt rơi lặp).
- **Chuyển động lớp trong SVG** khai trong `assets.yaml` → `motion: [{layer, recipe, ...}]`, dùng thư viện công thức:
  - `bob`: dập dềnh.
  - `rotate`: quay quanh tâm.
  - `twinkle`: lấp lánh bằng độ mờ.
  - `dashflow`: nét đứt trôi dọc đường. Dùng cho dòng sông, suối, chấm muối chạy trên bản đồ, mũi tên hơi nước.
  - `rise`: bay lên có lặp liền mạch.
  - `fall`: mưa rơi có lặp liền mạch.
  - `pulse_opacity`.
  Công thức nào chạy cũng phải chỉ phụ thuộc số khung.
- **Chế độ** `?render=1`: không có thanh điều khiển, nền đúng canvas, `window.vp` dùng cho Tool 08. Chế độ xem: nút phát/dừng kèm tiếng, thanh tua, số khung, mã khung hình, bật/tắt vùng an toàn.

**Tool Python** (`vp/presentation_tools.py`, CLI `vp presentation build|check|preview|lint`):
- `build`: cần cổng animation ĐẠT; biên dịch JSON, chép file, ghi trang.
- `check`: Chrome chạy ngầm seek các khung mốc (đầu, giữa, cuối mỗi khung hình và mọi khung chuyển cảnh), chụp ảnh vào `07_presentation/check/`, ghi `check_manifest.json` gồm lỗi JS, hash ảnh, đo DOM chữ tràn.
- `preview`: tờ ảnh các khung mốc (`contact.png`) để người duyệt xem.

**Checklist `presentation` v1:**
- **Tự động:**
  - PRS-A01: presentation.json khớp đầu vào (`input_hash`).
  - PRS-A02: mọi asset có trong `assets/` và trùng hash với 06.
  - PRS-A03: font nhận diện có file và giấy phép. Mức **chặn**.
  - PRS-A04: dựng thử không lỗi JS, đúng 1920×1080, không khung trống hay đen toàn bộ.
  - PRS-A05: tất định — seek ngược, xuôi, lặp lại đều cho ảnh trùng hash.
  - PRS-A06: chữ không tràn box và nằm trong vùng an toàn, đo trong DOM.
  - PRS-A07: mọi vòng lặp hoặc chuyển động lớp có công thức tương ứng.
  - PRS-A08: tờ kiểm khớp bản dựng hiện tại.
- **Phán đoán:**
  - C01: bố cục khớp storyboard.
  - C02: chuyển cảnh mượt, đúng loại.
  - C03: chuyển động tự nhiên, khớp lời. Người duyệt xem video xem trước có tiếng.
  - C04: chữ đúng font, đọc rõ, không lỗi dấu tiếng Việt.
  - C05: linh vật và thương hiệu đúng luật.

## Việc cần chủ dự án
- Tải font **Be Vietnam Pro** (Google Fonts, giấy phép SIL OFL) về thư mục `~/Documents/DEV_WORK_SUB/VieNeu-TTS/fonts/`. Máy dựng không có mạng để tải.

## Để lại cho người xây
- Số khung chuyển cảnh (8/10) là mặc định, có thể chỉnh trong `presentation.json`.
- Thay các lớp gợn sóng tĩnh bằng `dashflow` trong `ve_hinh.py`/`canh.py`, khi đó phải duyệt lại cổng 06.
