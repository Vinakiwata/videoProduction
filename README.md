# videoProduction — Dây chuyền sản xuất video bằng code

Dây chuyền gồm 12 công đoạn, đi từ brief tới video đăng YouTube. Mỗi công đoạn do một tool riêng đảm nhận.
Giữa hai công đoạn luôn có một **cổng kiểm duyệt theo checklist**: chưa ĐẠT thì công đoạn sau không chạy.

| # | Công đoạn | Thư mục | Trạng thái tool |
|---|---|---|---|
| 0 | Brief & bộ nhận diện | `00_brief` | checklist ✅ · tool ⏳ |
| 1 | Kịch bản | `01_script` | checklist ✅ (cổng này = Tool 2 kiểm duyệt kịch bản) · tool ⏳ |
| 2 | Thiết kế nội dung & storyboard | `02_design` | checklist ✅ · tool ⏳ |
| 3 | Animatic | `03_animatic` | checklist ✅ · tool ⏳ |
| 4 | Giọng đọc (VieNeu-TTS) | `04_voice` | checklist ✅ · tool ⏳ |
| 5 | Timeline tổng | `05_timeline` | checklist ✅ · tool ⏳ |
| 6 | Hoạt ảnh 2D | `06_animation` | checklist ✅ · tool ⏳ |
| 7 | Web trình chiếu 1920×1080 | `07_presentation` | checklist ✅ · tool ⏳ |
| 8 | Render khung hình | `08_render` | checklist ✅ · tool ⏳ |
| 9 | Mix âm thanh & ghép | `09_mix` | checklist ✅ · tool ⏳ |
| 10 | QC tổng | `10_final` | checklist ✅ · tool ⏳ |
| 11 | Đóng gói xuất bản | `11_package` | checklist ✅ · tool ⏳ |

## Xem lại kết quả duyệt
- Nhật ký mọi lần duyệt của một dự án: `projects/<dự án>/reviews/LOG.md`
- Báo cáo chi tiết từng lần: `projects/<dự án>/reviews/<công đoạn>/<thời gian>/report.md`
- Dự án mẫu đã chạy thử: [`projects/vi-du-bau-troi-xanh/reviews/LOG.md`](projects/vi-du-bau-troi-xanh/reviews/LOG.md)

## Lệnh
```bash
python -m vp new projects/<dự án> --title "Tên video"
python -m vp status projects/<dự án>
python -m vp review start    projects/<dự án> <công đoạn>
python -m vp review finalize projects/<dự án> <công đoạn>
python -m vp review override projects/<dự án> <công đoạn> --by "Tên" --reason "Lý do"   # chỉ người dùng
python -m vp gate projects/<dự án> <công đoạn>
python3 -m pytest -q
```

## Luật cổng (tóm tắt)
- Mỗi mục có mức **Chặn / Nghiêm trọng / Nhẹ**, chấm bằng **máy đo** (`auto`) hoặc **phán đoán có bằng chứng** (`ai`).
- Có mục Chặn hoặc Nghiêm trọng trượt thì **KHÔNG ĐẠT**. Mục Nhẹ trượt chỉ ghi "nên cải thiện".
- Mọi kết luận phải có bằng chứng. Trượt thì phải có hướng sửa.
- Sửa file sau khi duyệt thì cổng **HẾT HIỆU LỰC**, phải duyệt lại.

Chi tiết: [`docs/superpowers/specs/2026-11-27-kien-truc-va-kiem-duyet-design.md`](docs/superpowers/specs/2026-11-27-kien-truc-va-kiem-duyet-design.md)
