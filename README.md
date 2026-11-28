# videoProduction — Dây chuyền sản xuất video bằng code

Dây chuyền gồm 12 công đoạn, đi từ brief tới video đăng YouTube. Mỗi công đoạn do một tool riêng đảm nhận.
Giữa hai công đoạn luôn có một **cổng kiểm duyệt theo checklist**: chưa ĐẠT thì công đoạn sau không chạy.

| # | Công đoạn | Thư mục | Trạng thái tool |
|---|---|---|---|
| 0 | Brief & bộ nhận diện | `00_brief` | checklist ✅ · tool ✅ (`vp brief new`, skill `vp-brief`) |
| 1 | Kịch bản | `01_script` | checklist ✅ (cổng này = Tool 2 kiểm duyệt kịch bản) · tool ✅ (`vp script …`, skill `vp-kich-ban`) |
| 2 | Thiết kế nội dung & storyboard | `02_design` | checklist ✅ · tool ✅ (`vp design …`, skill `vp-thiet-ke`) |
| 3 | Animatic | `03_animatic` | checklist ✅ · tool ✅ (`vp animatic build`, skill `vp-animatic`) |
| 4 | Giọng đọc (VieNeu-TTS) | `04_voice` | checklist ✅ · tool ✅ (`vp voice …`, skill `vp-giong-doc`; chạy thật cần mạng hoặc file thu âm) |
| 5 | Timeline tổng | `05_timeline` | checklist ✅ · tool ✅ (`vp timeline build`, skill `vp-timeline`) |
| 6 | Hoạt ảnh 2D | `06_animation` | checklist ✅ · tool ✅ (`vp animation init/preview/lint`, skill `vp-hoat-anh`) |
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
# Tool 0 — brief (dùng hồ sơ kênh trong channels/)
python -m vp brief new projects/<dự án> --channel kenh-khoa-hoc-mau --title "…" --goal "…"
# Tool 1 — kịch bản
python -m vp script import   projects/<dự án> <bản-thảo.md>   # khi đã có bản thảo
python -m vp script estimate projects/<dự án>
python -m vp script view     projects/<dự án>
python -m vp script lint     projects/<dự án>
# Tool 3 — storyboard
python -m vp design init|preview|view|lint projects/<dự án>
# Giọng đọc
python -m vp voice synth projects/<dự án> [--engine recording]
python -m vp voice sheet|calibrate|to-animatic projects/<dự án>
# Timeline
python -m vp timeline build projects/<dự án>
# Animatic
python -m vp animatic build projects/<dự án>
# Hoạt ảnh 2D (SVG vẽ bằng code: 06_animation/_src/ve_hinh.py)
python -m vp animation init|sync|preview|lint projects/<dự án>
# Bộ nhận diện kênh Khỉ Khám Phá: tách lại file upload và linh vật
python3 channels/khi-kham-pha/brand/xuat.py
# Cổng duyệt
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
