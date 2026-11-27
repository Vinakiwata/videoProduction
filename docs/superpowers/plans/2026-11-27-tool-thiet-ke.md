# Tool 3 (Storyboard) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Storyboard YAML có schema, các kiểm tra tự động, bản đọc và ảnh phác thảo, nối vào cổng `design`.

**Architecture:** `vp/schemas/storyboard.schema.json`; `vp/checks/design.py` (kiểm tra, đăng ký vào REGISTRY); `vp/design_tools.py` (init, view, lint); `vp/design_preview.py` (Pillow vẽ wireframe, manifest hash). CLI `python -m vp design init|lint|view|preview`.

**Tech Stack:** Python 3.11+, PyYAML, jsonschema, Pillow 12 (có sẵn), font DejaVu Sans.

**Spec:** `docs/superpowers/specs/2026-11-27-tool-thiet-ke-design.md`

## Global Constraints
- Thời điểm hiệu ứng là tỉ lệ 0–1 trong khung hình; độ dài hiệu ứng tính bằng giây.
- Cỡ chữ ≥ 48 px (title ≥ 72 px); ≤ 7 từ mỗi dòng; hiển thị ≥ 0,3 giây/từ + 1 giây; tương phản ≥ 4,5:1; vùng an toàn chữ 5%, hình được tràn tối đa 10%; ≤ 5 tiếng động mỗi 10 giây.
- Ảnh phác thảo 960×540; tờ tổng hợp 4 cột.

## Review Focus
- Đoạn có nhiều khung với span lệch số thực (0.333…) gây báo hở hoặc chồng giả.
- Màu viết thường và viết hoa (`#ffd23f` so với `#FFD23F`).
- Chữ nhiều dòng; chữ rất dài tràn ô khi vẽ ảnh phác thảo.
- Khung không có phần tử chữ (bỏ qua kiểm tra tương phản).
- Đoạn im lặng (est_duration từ kịch bản) dùng khi tính thời gian đọc chữ.

## Tasks
- [ ] **T1 — Schema + fixture + `storyboard_coverage`, `storyboard_refs`.** Test: `tests/test_design_checks.py`.
- [ ] **T2 — `storyboard_palette`, `storyboard_text`, `storyboard_contrast`, `storyboard_safe_area`, `storyboard_sfx_density`.**
- [ ] **T3 — `design init` / `view` / `lint`.** Test: `tests/test_design_tools.py`.
- [ ] **T4 — `design preview` + `storyboard_preview_in_sync`.**
- [ ] **T5 — Checklist design v2 + skill `vp-thiet-ke` + README/CLAUDE.md.**
- [ ] **T6 — Storyboard thật cho `vi-sao-nuoc-bien-man`, qua cổng `design`, push, PR.**
