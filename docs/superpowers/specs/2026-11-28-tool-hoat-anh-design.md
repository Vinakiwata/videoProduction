# Thiết kế: Tool 6 — Hoạt ảnh 2D (06_animation)

- Ngày: 2026-11-28
- Trạng thái: **Đã duyệt**. Chủ dự án chọn cách A, hình SVG viết bằng code ("làm đi").

## 1. Mục đích
Tạo **hình thật** cho mọi asset trong storyboard dưới dạng SVG vector, theo đúng bộ nhận diện. Các chi tiết cần chuyển động riêng được **tách lớp** (`<g id="…">`), để web trình chiếu (Tool 07) tạo chuyển động theo `cues` của timeline.
Tool 6 làm **hình và lớp**. Chuyển động lúc chạy do Tool 07 điều khiển theo timeline, vì timeline đã khoá thời gian theo khung.

## 2. Mục tiêu / Không làm / Thất bại nếu
**Mục tiêu**
- Mỗi asset có một file `06_animation/assets/<MÃ>.svg`, khai trong `06_animation/assets.yaml` gồm:
  - file, viewBox, nguồn, giấy phép;
  - danh sách lớp bắt buộc (`layers`);
  - ghi chú cho người dựng chuyển động.
- Máy kiểm từng file:
  - XML hợp lệ, có viewBox;
  - không `<image>`, không `<script>`, không tham chiếu ra ngoài;
  - chữ (nếu có) dùng font của brief;
  - màu thuộc palette, cho phép độ trong suốt (`opacity`);
  - ≤ 4 màu mỗi hình;
  - có đủ các lớp đã khai.
- Kiểm **an toàn nhấp nháy** trên timeline: mọi vòng lặp `pulse`, `blink_slow`, `shimmer` có chu kỳ ≥ 0,4 giây, tức ≤ 2,5 lần mỗi giây (WCAG 2.3.1 cho phép tối đa 3 lần mỗi giây).
- Tờ xem trước `06_animation/assets_preview.png`: mỗi hình một ô, kèm mã và mô tả. Hình được dựng bằng `rsvg-convert` trên nền tối và nền xanh, để thấy rõ hình trên cả hai nền đang dùng.

**Không làm:** Lottie, hình raster, chuyển động trong file SVG (SMIL/CSS). Chuyển động thuộc Tool 07.

**Thất bại nếu:** hình lệch màu nhận diện; hình rối, sai khoa học; thiếu lớp khiến Tool 07 không tạo được chuyển động như storyboard mô tả.

## 3. Các cách đã cân nhắc
| Cách | Kết luận |
|---|---|
| **A. SVG viết bằng code, tách lớp** | **Chọn**: chủ dự án duyệt |
| B. Kho hình Canva | Loại: khó tách lớp, khó đồng nhất màu, phải kiểm bản quyền từng hình |
| C. Kết hợp A + B | Loại ở giai đoạn này |

## 4. Lệnh
| Lệnh | Việc |
|---|---|
| `python -m vp animation init <dự án>` | Cổng `timeline` phải MỞ. Tạo `assets.yaml` từ thư viện asset của storyboard (`file` = `assets/<MÃ>.svg`, `layers: []`, nguồn và giấy phép mặc định là thiết kế gốc). Không ghi đè |
| `python -m vp animation preview <dự án>` | Dựng tờ xem trước |
| `python -m vp animation lint <dự án>` | Chạy các mục tự động của checklist `animation` |

## 5. Kiểm tra tự động mới
| Tên | Kiểm gì |
|---|---|
| `animation_assets_complete` | Mọi asset của storyboard đều có trong `assets.yaml` và có file. Không thừa asset lạ. Mỗi mục có `source` và `license` |
| `svg_valid` | XML hợp lệ, có `viewBox`; không `<image>`, `<script>`, `<foreignObject>`, không href ra ngoài; `<text>` chỉ dùng font trong `brief.brand.fonts` |
| `svg_palette` | Mọi màu `fill`/`stroke`/`stop-color` thuộc palette (không phân biệt hoa thường; `none`, `transparent`, `currentColor` được phép); ≤ `max_colors` màu mỗi hình |
| `svg_layers` | Mọi lớp khai trong `layers` có `<g id>` tương ứng trong file |
| `animation_flash_safety` | Mọi cue `loop` thuộc `pulse`, `blink_slow`, `shimmer` trong timeline có `period_frames` ≥ 0,4 × fps |
| `animation_preview_in_sync` | Tờ xem trước khớp mã băm các file SVG hiện tại |

## 6. Quyết định của Claude (cần xem lại)
1. Bóng đổ nhẹ làm bằng màu tối `#1B1B1F` với độ trong suốt khoảng 0,25, không thêm màu mới.
2. Nút đăng ký có chữ "ĐĂNG KÝ" dạng `<text>` dùng font Be Vietnam Pro. Tool 07 sẽ nhúng font này. Ảnh xem trước tạm dùng font dự phòng.
3. Chu kỳ nhấp nháy tối thiểu 0,4 giây, chặt hơn ngưỡng WCAG để có biên an toàn.
