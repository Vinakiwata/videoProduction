"""Bản đọc script.md: bảng mốc thời gian / lời / hình để người xem nhanh trên GitHub."""


def _ts(t: float) -> str:
    m, s = divmod(t, 60)
    return f"{int(m):02d}:{s:04.1f}"


def _cell(v) -> str:
    if isinstance(v, list):
        v = ", ".join(map(str, v))
    return str(v or "").replace("|", "\\|").replace("\n", " ")


def render_view(script: dict) -> str:
    meta = script.get("meta", {})
    out = [
        f"# {meta.get('title', '')}",
        "",
        "> Bản đọc tự động sinh từ `script.yaml` bằng `python -m vp script view`. Đừng sửa file này bằng tay.",
        "",
        f"- **Khán giả:** {meta.get('audience', '')}",
        f"- **Mục tiêu:** {meta.get('goal', '')}",
        f"- **Thời lượng mục tiêu:** {meta.get('target_duration_s', '')} giây",
        "",
    ]
    t = 0.0
    for sc in script.get("scenes") or []:
        out += [f"## {sc.get('id')} · {sc.get('title', '')}", "", f"*Mục đích:* {sc.get('purpose', '')}", "",
                "| Bắt đầu | Mã | Loại | Lời đọc | Hình | SFX | Dài (s) |", "|---|---|---|---|---|---|---|"]
        for seg in sc.get("segments") or []:
            d = float(seg.get("est_duration_s") or 0)
            kind = "🎙️ giọng" if seg.get("kind") == "voice" else "🔇 im lặng"
            text = _cell(seg.get("text"))
            if seg.get("source_ids"):
                text += f" <sub>[{_cell(seg['source_ids'])}]</sub>"
            out.append(f"| {_ts(t)} | {seg.get('id')} | {kind} | {text} | {_cell(seg.get('visual'))} "
                       f"| {_cell(seg.get('sfx'))} | {d:g} |")
            t += d
        out.append("")
    out += [f"**Tổng thời lượng: {t:.1f} giây**", ""]
    if script.get("pronunciation"):
        out += ["## Phát âm", "", "| Viết | Đọc là |", "|---|---|"]
        out += [f"| {_cell(k)} | {_cell(v)} |" for k, v in script["pronunciation"].items()]
        out.append("")
    if script.get("sources"):
        out += ["## Nguồn", ""]
        for s in script["sources"]:
            url = f" — {s['url']}" if s.get("url") else ""
            out.append(f"- **{s.get('id')}** {s.get('title', '')}{url}")
        out.append("")
    return "\n".join(out)
