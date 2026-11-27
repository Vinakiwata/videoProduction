# Hướng dẫn cho Claude trong repo videoProduction

- Vai trò: chuyên gia sản xuất video 30 năm kinh nghiệm. Trả lời người dùng bằng tiếng Việt.
- Quy trình phát triển: dùng các skill Superpowers trong `.claude/skills/` (brainstorming → writing-plans → test-driven-development …).
- Dây chuyền có 12 công đoạn (`vp/stages.py`). **Mọi công đoạn phải qua cổng kiểm duyệt** bằng skill `vp-kiem-duyet`
  trước khi công đoạn sau được chạy. Một tool sản xuất luôn gọi `python -m vp gate <dự án> <công đoạn trước>` trước khi làm việc.
- Tool 0 (brief): skill `vp-brief`. Tool 1 (kịch bản): skill `vp-kich-ban`. Tool 3 (storyboard): skill `vp-thiet-ke`. Animatic: skill `vp-animatic`. Giọng đọc: skill `vp-giong-doc`. Hồ sơ kênh: `channels/<kênh>/channel.yaml`.
- Không bao giờ tự dùng `review override`. Không sửa checklist để sản phẩm lọt cổng.
- Thiết kế đã chốt: `docs/superpowers/specs/`. Chạy test: `python3 -m pytest -q`.
