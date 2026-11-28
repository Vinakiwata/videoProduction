# Chuyển kênh Khỉ Khám Phá sang khung dọc 9:16 (Shorts/TikTok)

Ngày 28/11/2026. Chủ dự án chọn:
- **Chỉ làm dọc 9:16**, theo cách **A: thiết kế lại cho khung dọc**.
- **Hồ sơ riêng cho từng nền tảng**: YouTube Shorts, TikTok, Instagram/Facebook Reels.
- **Số đo theo giao diện đăng thường**, không lấy chuẩn quảng cáo.

## Ý định và lý do
Kênh đăng lên YouTube Shorts và TikTok. Bản hiện tại là khung ngang 1920×1080: lên Shorts bị đệm hai dải đen trên và dưới, nên hình và chữ chỉ còn khoảng 1/3 màn hình điện thoại. Từ nay mọi video của kênh làm khung **1080×1920, 30 fps, dài tối đa 60 giây**. Video mẫu `vi-sao-nuoc-bien-man` (53,4 giây) được làm lại theo khung này.

**Mục tiêu**
- Hình kín màn hình dọc, chữ to, đọc rõ trên điện thoại.
- Chữ, linh vật và nút đăng ký không bị giao diện Shorts/TikTok/Reels che.
- Máy đọc kích thước khung và vùng an toàn từ brief, không còn số cứng 1920×1080.

**Không làm**
- Không giữ song song bản ngang 16:9.
- Không cắt hay đệm tự động từ bản ngang.

**Coi là thất bại dù chạy được**
- Chữ hoặc Khỉ nằm dưới cột nút bên phải hay dải chú thích bên dưới.
- Cảnh ngang bị kéo méo cho vừa khung dọc.
- Nới cổng duyệt để bản cũ lọt qua.

## Các cách đã cân nhắc
- **A. Thiết kế lại cho khung dọc** *(đã chọn)*: viết lại bố cục storyboard, vẽ lại cảnh trên khung dọc, giữ kịch bản, giọng và nhịp. Tốn công nhất nhưng đúng chất lượng, và chỉ phải trả một lần cho cả kênh.
- B. Cảnh ngang ở nửa trên, chữ ở nửa dưới: cảnh chỉ còn 1080×608, nửa dưới lại vướng vùng giao diện che. Loại.
- C. Phóng cảnh ngang phủ khung dọc rồi lia camera: mỗi lúc chỉ thấy khoảng 30% bề ngang, nên cảnh bản đồ và cửa sông mất ý nghĩa. Loại.

## Ràng buộc
**Vùng an toàn theo từng nền tảng** (lề không đều, tính trên khung 1080×1920, số đo của giao diện đăng thường):

| Nền tảng | Trên | Dưới | Trái | Phải | Thứ bị che | Nguồn (đối chiếu 28/11/2026) |
|---|---|---|---|---|---|---|
| `youtube_shorts` | 154 | 461 | 65 | 173 | Thanh tìm kiếm; kênh, nút Đăng ký, tiêu đề, thanh tiến trình; cột Thích/Bình luận/Chia sẻ/Remix | aicarousels.com YouTube Shorts Safe Zone Checker |
| `tiktok` | 108 | 320 | 60 | 120 | Tab For You; chú thích, nhạc; cột nút | Ignite Social Media, TikTok safe zone |
| `reels` | 220 | 420 | 35 | 84 | Tài khoản, Follow; chú thích; cột nút | Ignite Social Media (rộng 1010, cao 1280); cột nút phải 84 theo PostPlanify |

- Brief chọn `platforms`, mặc định theo kênh là cả ba. Bộ kiểm lấy **lề chặt nhất từng cạnh** của các nền tảng đã chọn, vì cùng một file video sẽ đăng lên tất cả.
- Với cả ba nền tảng, lề tổng hợp là **trên 220 (Reels) · dưới 461 (Shorts) · trái 65 · phải 173 (Shorts)**. Vùng an toàn còn lại **842×1239 px**, bắt đầu từ (65, 220).
- Số đo quảng cáo (vd. Shorts 288/672/48/192) **không dùng**: vùng nội dung chỉ còn khoảng 840×960, chữ và hình phải thu nhỏ.
- **Bắt buộc trong vùng an toàn:** chữ, linh vật (`kind: mascot`), nút và icon kêu gọi (`kind: ui`).
- **Được tràn ra ngoài:** cảnh nền (`kind: scene`) phủ kín 1080×1920; hình khác được tràn khung tối đa 10% như luật cũ.
- **Lưu ý thiết kế:** vật chính của cảnh (sông, mặt biển, núi lửa) nên nằm trong vùng an toàn. Dải dưới 420 px chỉ đặt phần phụ (cát, đồi, đáy biển).

**Giữ nguyên:**
- Kịch bản 01, giọng 04 (file âm thanh không đổi), mã khung hình và `span` của từng khung.
- Như vậy timeline 05 ra đúng mốc khung cũ; chỉ phải duyệt lại vì storyboard đổi.

**Chuẩn mực có sẵn:**
- Font Be Vietnam Pro, bảng màu, `text_plate`, luật linh vật DSN-A11 (2–3 phản ứng và có mặt ở kết), cỡ chữ tối thiểu 48 px.

## Phần đã quyết
1. **Hồ sơ nền tảng, kênh và brief**
   - Thư mục mới `platforms/<id>.yaml` (`youtube_shorts`, `tiktok`, `reels`), có schema `platform.schema.json`. Mỗi hồ sơ gồm:
     - `name`, `canvas {width: 1080, height: 1920, fps: 30}`, `max_duration_s` (Shorts 180, TikTok 600, Reels 180; kênh vẫn giữ 60 giây);
     - `safe_margins_px {top, bottom, left, right}`, `ui_zones` (các ô bị che, dùng để vẽ lớp phủ);
     - `source` (tên và URL), `checked` (ngày đối chiếu).
   - Giao diện ứng dụng thay đổi theo thời gian, nên hồ sơ ghi ngày. Bộ kiểm cảnh báo khi số đo cũ hơn 180 ngày.
   - Kênh: `format: {width: 1080, height: 1920, fps: 30}`, `channel: youtube_shorts`, `platforms: [youtube_shorts, tiktok, reels]`.
   - Brief: thêm `platforms` (mặc định lấy của kênh). Khung lấy từ hồ sơ nền tảng; các nền tảng trong một brief phải cùng khung, không thì báo lỗi.
   - `vp/platforms.py` cung cấp `safe_margins(brief)`, trả lề chặt nhất từng cạnh. Brief không có `platforms` thì mặc định 5% mỗi cạnh, để dự án cũ vẫn chạy.
2. **Máy đọc khung từ brief** (`brief.format`), bỏ số cứng ở:
   - `design_preview` và `animatic`: khung xem trước bằng nửa canvas (540×960); dải phụ đề animatic vẫn nằm riêng bên dưới.
   - Tool 07: `presentation_tools`, `capture.mjs`, thumbnail tờ kiểm; `player.js` dùng lề bốn cạnh khi đo vùng an toàn.
   - Bộ kiểm: `checks/presentation.py`, `checks/design.py`, `checks/animation.py`.
3. **Checklist** (chủ dự án duyệt cùng tài liệu này):
   - `design` v5, DSN-A08:
     - Tiêu đề mới: "Chữ, linh vật, nút trong vùng an toàn của các nền tảng đã chọn; hình không tràn quá 10%".
     - Lề lấy từ `vp.platforms.safe_margins(brief)`; lỗi ghi rõ nền tảng nào che.
     - Thêm mascot và ui vào nhóm bắt buộc trong vùng an toàn.
   - `presentation` v2:
     - PRS-A04: "đúng kích thước khung của brief".
     - PRS-A06: "vùng an toàn của các nền tảng đã chọn", lề đọc từ brief qua `presentation.json`.
   - `brief`: thêm BRF-A tự động "Nền tảng có hồ sơ, cùng khung, thời lượng ≤ giới hạn của từng nền tảng và của kênh; số đo không cũ quá 180 ngày".
   - `render`, `mix`, `final`: tham số kích thước đọc từ brief, không ghi cứng 1920×1080. Các công đoạn này chưa có tool, nên chỉ đổi tham số và tiêu đề.
4. **Storyboard dọc**: viết lại `box` cho 18 khung theo nguyên tắc:
   - Xếp theo trục dọc: hai cốc trên–dưới; chuỗi Mưa → Sông → Bốc hơi chạy từ trên xuống, mũi tên chỉ xuống.
   - Vòng tuần hoàn nằm giữa vùng an toàn; Khỉ ở phần dưới vùng an toàn.
   - Chữ một đến hai dòng, rộng tối đa 900 px.
   - Hướng nhân quả vẫn trái → phải ở cảnh ngang nhỏ, còn dòng chảy chính đi từ trên xuống.
   - Ghi chú camera theo khung dọc: pan_up/pan_down thay pan_left/pan_right khi hợp.
5. **Vẽ lại cảnh** trên khung **540×960** (bằng 1080×1920 chia 2):
   - Các cảnh: A-SONG, A-CUA-SONG, A-BIEN, A-SUOI, A-NEN-MUA, A-DAY-BIEN, A-BAN-DO-SONG và A-SANG-BIEN (khớp vùng biển của bản đồ).
   - Bố cục chung: trời và núi ở trên, sông uốn từ trên xuống, biển hay đáy biển ở phần dưới.
   - A-DA vẫn là hình theo ô (không phủ khung); vẽ lại tỉ lệ cho hợp ô mới.
   - Icon, ui và linh vật giữ nguyên; chỉ chỉnh `viewBox` nếu tỉ lệ ô mới lệch nhiều.
   - Chuyển động lớp (`motion`) làm lại theo hình mới: đường tâm sông, mưa phủ rộng hơn khung (dx, dy), toạ độ tâm quay.
6. **Thứ tự duyệt lại:** brief 00 → script 01 → design 02 → animatic 03 → voice 04 → timeline 05 → animation 06 → presentation 07.
   - 01 và 04 không đổi nội dung, chỉ duyệt lại nếu cổng báo hết hiệu lực vì brief đổi.
   - Phần nghe của 04 kế thừa điểm chủ dự án đã chấm, vì file âm thanh trùng hash.
   - Mục chấm tay **PRS-C03 do chủ dự án xem lại bản dọc**.
7. **Xem như trên điện thoại:** chế độ xem của Tool 07 có nút chọn nền tảng (Shorts / TikTok / Reels / tắt). Mỗi nền tảng vẽ lớp phủ `ui_zones` của nó, tô mờ chỗ bị che, để người duyệt thấy khi đăng lên thì cái gì bị che. Tờ khung mốc có thêm một bản chồng lớp phủ của nền tảng che nhiều nhất.

## Để lại cho người xây (quyết định của tôi, chủ dự án có thể sửa)
- Lấy số đo giao diện đăng thường từ nguồn đo trên giao diện thật, ghi nguồn và ngày trong từng hồ sơ. Chủ dự án có thể sửa số trong `platforms/*.yaml` khi tự đo trên máy mình.
- Facebook Reels dùng chung hồ sơ `reels` với Instagram Reels.
- Bản ngang cũ không giữ lại trong repo: lịch sử git đã lưu, PR #8 là mốc.
- Cỡ chữ tối thiểu giữ 48 px, tiêu đề 72 px, vì khung dọc rộng 1080 nên chữ trông to hơn tương đối.
- Khung xem trước và animatic ở 540×960 cho nhẹ.
- Việc này làm trên nhánh mới `feat/khung-doc` tách từ `feat/tool-trinh-chieu`.
