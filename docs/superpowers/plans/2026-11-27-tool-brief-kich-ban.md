# Tool 0 (Brief) & Tool 1 (Kịch bản) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Lệnh hỗ trợ và skill để tạo brief từ hồ sơ kênh, cùng kịch bản hoàn chỉnh từ ý tưởng hoặc bản thảo, đủ chất lượng để qua cổng duyệt.

**Architecture:** Code Python nhỏ, chia theo trách nhiệm: `vp/channel.py`, `vp/brief.py`, `vp/script_tools.py`. Lệnh mới gắn vào `vp/__main__.py`. Phần sáng tạo và nghiên cứu nằm trong skill `.claude/skills/vp-brief`, `.claude/skills/vp-kich-ban`.

**Tech Stack:** Python 3.11+, PyYAML, jsonschema, pytest (đã có sẵn).

**Spec:** `docs/superpowers/specs/2026-11-27-tool-brief-kich-ban-design.md`

## Global Constraints
- Tốc độ đọc mặc định 3,2 âm tiết/giây; thời lượng = âm tiết/sps làm tròn lên 0,1 giây, tối thiểu 0,5 giây.
- Khi nhập bản thảo, tách câu ở ngưỡng 200 ký tự.
- Chuỗi tạm có dạng `TODO: …`. Thẻ cảm xúc `[cười]`, `[thở dài]`, `[hắng giọng]` không tính là chỗ trống.
- Thông báo cho người dùng viết bằng tiếng Việt.

## Review Focus
- Bản thảo có dòng trống thừa, tiêu đề cảnh rỗng, hoặc cảnh không có đoạn nào.
- Câu không có dấu kết câu nhưng vẫn quá dài (phải tách theo dấu phẩy, rồi theo từ).
- YAML có ngày tháng bị hiểu thành kiểu date.
- `estimate` chạy lên kịch bản có đoạn silent.
- `script.md` lệch sau khi sửa yaml mà quên chạy `view`.

## Tasks
- [ ] **T1 — Hồ sơ kênh + `brief new`** (`vp/channel.py`, `vp/brief.py`, `channel.schema.json`, sửa `brief.schema.json`). Test: `tests/test_brief_tool.py`.
- [ ] **T2 — `no_placeholders` tổng quát** (thay `script_no_placeholders`). Cập nhật checklist brief/script. Test: `tests/test_checks_script.py`.
- [ ] **T3 — `script import` / `estimate`** (`vp/script_tools.py`). Test: `tests/test_script_tools.py`.
- [ ] **T4 — `script view` / `lint` + kiểm tra `script_view_in_sync` + SCR-A08**. Test: `tests/test_script_tools.py`.
- [ ] **T5 — Skill `vp-brief`, `vp-kich-ban`.** Cập nhật README và CLAUDE.md.
- [ ] **T6 — Chạy thật:** dự án mới từ ý tưởng → brief → cổng → kịch bản → cổng. Commit, push, PR.
