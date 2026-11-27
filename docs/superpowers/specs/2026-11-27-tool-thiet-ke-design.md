# Thiết kế: Tool 3 (Thiết kế nội dung & storyboard)

- Ngày: 2026-11-27
- Trạng thái: **Đã duyệt theo uỷ quyền** (chủ dự án yêu cầu "tiếp tục với tool 3", Claude tự quyết và ghi lại ở mục 8)
- Dựa trên: thiết kế kiến trúc chung và thiết kế Tool 0/1

## 1. Mục đích
Biến kịch bản đã duyệt thành **bản thiết kế trình diễn**: từng khung hình có bố cục, điểm nhìn chính, các đối tượng 2D, cách chúng vào, ra và chuyển động, chữ trên màn hình, tiếng động, cách chuyển cảnh.
Đây là "hợp đồng" để Tool hoạt ảnh (06) vẽ đúng thứ cần vẽ, và Tool web trình chiếu (07) đặt đúng chỗ, đúng lúc.

## 2. Mục tiêu / Không làm / Thất bại nếu
**Mục tiêu**
- Mọi đoạn kịch bản có khung hình phủ kín từ đầu tới cuối, không hở, không chồng.
- **Thời điểm trong storyboard là tỉ lệ (0–1) của đoạn**, không phải giây tuyệt đối. Nhờ vậy khi giọng thật dài hoặc ngắn hơn ước tính, thiết kế vẫn đúng, Tool timeline chỉ cần nhân với thời lượng thật.
- Đo bằng máy mọi thứ đo được: độ phủ, tham chiếu, màu nhận diện, tương phản, cỡ chữ, thời gian đọc chữ, vùng an toàn, mật độ tiếng động.
- **Ảnh phác thảo (wireframe)** cho từng khung và một tờ tổng hợp `storyboard.png`, để người duyệt và chủ dự án *nhìn thấy* thay vì chỉ đọc chữ.
- Thư viện tài nguyên (`assets`) dùng lại qua nhiều khung, để hình ảnh nhất quán và giảm việc cho Tool hoạt ảnh.

**Không làm:** chưa vẽ hình thật (đó là Tool 06). Ảnh phác thảo chỉ là khối màu kèm nhãn.

**Thất bại nếu:** người dựng phải đoán ý; khung rối nhiều điểm nhìn; chữ không kịp đọc; màu lạc khỏi nhận diện; storyboard lệch kịch bản mà không ai biết.

## 3. Các cách đã cân nhắc
| Cách | Kết luận |
|---|---|
| A. Storyboard là văn bản mô tả tự do (markdown) | Loại: không đo được, Tool 06/07 không đọc được |
| **B. Storyboard YAML có schema + kiểm tra tự động + ảnh phác thảo sinh từ dữ liệu** | **Chọn** |
| C. Vẽ storyboard bằng công cụ thiết kế ngoài (Figma, Canva) | Loại ở giai đoạn này: không nối tự động vào dây chuyền. Có thể dùng sau để vẽ asset |

## 4. Dữ liệu: `02_design/storyboard.yaml`
```yaml
meta: {title: …, canvas: {width: 1920, height: 1080, fps: 30}}
palette: ['#0B3D91', '#FFD23F', '#FFFFFF', '#1B1B1F']   # = brief.brand.colors
fonts: {title: Be Vietnam Pro, body: Be Vietnam Pro}
style: Minh hoạ phẳng…                                  # = brief.brand.style
assets:                                                  # thư viện dùng chung
  - id: A-SONG
    kind: illustration          # illustration | icon | diagram | background | ui
    description: Dòng sông uốn lượn, nước xanh nhạt, viền tròn
    colors: ['#FFFFFF', '#0B3D91']
shots:
  - id: S01-01-a                # <mã đoạn>-<a,b,c…>
    segment: S01-01
    span: [0, 1]                # phần của đoạn mà khung này chiếm (0–1)
    purpose: Đặt hai cốc cạnh nhau để thấy nghịch lý
    background: '#0B3D91'
    focal: e2                   # đúng 1 phần tử là điểm nhìn chính
    camera: {move: static}      # static | zoom_in | zoom_out | pan_left | pan_right | pan_up | pan_down
    transition_in: cut          # cut | crossfade | wipe_left | wipe_right | push_left | push_up | match_cut | zoom_through
    elements:
      - id: e1
        asset: A-SONG
        box: {x: 0, y: 55, w: 100, h: 45}      # % khung 1920×1080
        enter: {anim: fade, at: 0, dur_s: 0.4, ease: ease_out}
      - id: e3
        text: Muối từ đâu ra?
        style: title            # title | label | caption | number
        font_px: 96
        color: '#FFD23F'
        box: {x: 20, y: 8, w: 60, h: 14}
        enter: {anim: pop, at: 0.75, dur_s: 0.3, ease: back_out}
        exit: {anim: fade, at: 1.0, dur_s: 0.2}
        loop: {anim: bob}       # bob | pulse | rotate | shimmer | flow | wiggle
    sfx:
      - {name: pop, target: e3, event: enter}   # không dùng khoá 'on': YAML hiểu 'on' là true
    notes: …
```
- `enter.at` và `exit.at`: tỉ lệ 0–1 **trong khung hình**. `dur_s`: giây, vì cảm giác chuyển động không co giãn theo thời lượng.
- Danh sách `anim` và `ease` là tập đóng, nằm trong schema, để Tool 06/07 cài đặt được hết.
- Phần tử chữ (`text`) bắt buộc có `style`, `font_px`, `color`. Phần tử hình bắt buộc có `asset`.

## 5. Lệnh `python -m vp design …`
| Lệnh | Việc |
|---|---|
| `init <dự án>` | Gate `script` phải MỞ. Tạo khung storyboard: palette, fonts và style lấy từ brief; mỗi đoạn kịch bản một khung `-a`; `on_screen_text` và `sfx` của kịch bản thành phần tử hoặc tiếng động nháp; các chỗ chưa thiết kế ghi `TODO`. Không ghi đè, trừ khi `--force`. |
| `lint <dự án>` | Chạy mọi mục tự động của checklist `design`, không ghi nhật ký. |
| `view <dự án>` | Ghi `02_design/storyboard.md`: theo từng đoạn gồm lời đọc, khung, điểm nhìn, phần tử, hiệu ứng, tiếng động. |
| `preview <dự án>` | Vẽ `02_design/frames/<shot>.png` (960×540) và `02_design/storyboard.png` (tờ tổng hợp, mỗi ô có mã khung và lời đọc), kèm `frames/manifest.json` ghi mã băm storyboard. |

## 6. Kiểm tra tự động mới (`vp/checks/design.py`)
| Tên | Kiểm gì | Ngưỡng mặc định |
|---|---|---|
| `storyboard_coverage` | Mọi đoạn kịch bản có khung; `span` của từng đoạn phủ kín [0,1], không hở, không chồng; không có khung trỏ tới đoạn không tồn tại | sai số 0,001 |
| `storyboard_refs` | `asset`, `focal`, `sfx.target` trỏ tới thứ có thật; mã khung và mã phần tử không trùng; `focal` thuộc khung đó | — |
| `storyboard_palette` | Mọi mã màu (background, color, assets.colors) thuộc palette; palette = brief.brand.colors | — |
| `storyboard_text` | Chữ: `font_px` ≥ 48 với label/caption/number và ≥ 72 với title; ≤ 7 từ mỗi dòng (dòng tách bằng `\n`); thời gian hiển thị ≥ 0,3 giây/từ + 1 giây (tính theo est_duration của đoạn × span × tỉ lệ hiện) | các số ở cột trước |
| `storyboard_contrast` | Tỉ lệ tương phản chữ/nền ≥ 4,5:1 (WCAG). Nền là `background` của khung | 4,5 |
| `storyboard_safe_area` | Hộp chữ nằm trong vùng an toàn chữ (cách mép 5%); hộp hình không vượt khung quá 10% (cho phép tràn có chủ đích) | 5% / 10% |
| `storyboard_sfx_density` | Không quá N tiếng động trong mỗi cửa sổ 10 giây | N = 5 |
| `storyboard_preview_in_sync` | `frames/manifest.json` ghi đúng mã băm storyboard hiện tại | — |

## 7. Checklist `design` v2
- Thay DSN-A01 (chỉ kiểm file tồn tại) bằng các mục tự động ở bảng trên: coverage, refs, contrast ở mức **chặn**; palette, text, safe_area ở mức **nghiêm trọng**; sfx_density, preview_in_sync ở mức **nhẹ**.
- Bỏ DSN-C01 (độ phủ) vì đã đo tự động. DSN-C05 (nhận diện) giữ phần **phong cách** cho mục phán đoán, còn màu đã đo tự động.
- Thêm **DSN-C09** (nghiêm trọng): nhịp thị giác, nghĩa là cứ khoảng 2–4 giây có thay đổi thị giác có nghĩa, không có khung tĩnh quá 5 giây.
- Thêm **DSN-C10** (nghiêm trọng): tính liên tục, nghĩa là đối tượng xuyên suốt dùng cùng asset, cùng vị trí logic giữa các khung, hướng chuyển động nhất quán.
- `artifacts`: `02_design` và `01_script/script.yaml`. Kịch bản đổi thì thiết kế hết hiệu lực.

## 8. Quyết định của Claude (cần xem lại)
1. Ảnh phác thảo dùng font DejaVu Sans, vì môi trường làm việc chưa có Be Vietnam Pro. Đây chỉ là bản phác, Tool 07 sẽ nhúng font thật.
2. Cỡ chữ tối thiểu 48 px (title 72 px) ở khung 1080p, để còn đọc được trên điện thoại.
3. Thời gian đọc chữ 0,3 giây/từ + 1 giây. Tối đa 5 tiếng động mỗi 10 giây.
4. Thời điểm hiệu ứng tính theo tỉ lệ đoạn (0–1), còn độ dài hiệu ứng tính bằng giây.
