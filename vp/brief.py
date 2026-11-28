"""Tool 0 — tạo 00_brief/brief.yaml từ hồ sơ kênh + tham số. Giả định nào cũng được ghi lại."""
from pathlib import Path

from vp.channel import ChannelError, load_channel
from vp.project import create_project, dump_yaml


class BriefError(RuntimeError):
    pass


def new_brief(project: Path, *, channel: str, title: str, goal: str | None = None, audience: str | None = None,
              duration: float | None = None, ads: bool | None = None, force: bool = False,
              channels_dir: Path | None = None) -> Path:
    project = Path(project)
    path = project / "00_brief" / "brief.yaml"
    if path.exists() and not force:
        raise BriefError(f"{path} đã có. Sửa trực tiếp, hoặc dùng --force để tạo lại.")
    try:
        ch = load_channel(channel, channels_dir)
    except ChannelError as e:
        raise BriefError(str(e)) from e

    assumptions: list[str] = []
    if audience is None:
        audience = ch["audience"]
        assumptions.append(f"audience lấy theo hồ sơ kênh: \"{audience}\"")
    if duration is None:
        duration = ch["default_duration_s"]
        assumptions.append(f"target_duration_s lấy mặc định của kênh: {duration:g} giây")
    if ads is None:
        ads = False
        assumptions.append("Giả định video không có quảng cáo/tài trợ (is_advertising: false)")

    brief = {
        "title": title,
        "goal": goal or "TODO: sau khi xem, người xem hiểu/làm được điều gì cụ thể?",
        "audience": audience,
        "channel": ch["channel"],
        "format": dict(ch["format"]),
        **({"platforms": list(ch["platforms"])} if ch.get("platforms") else {}),
        "target_duration_s": duration,
        "tone": ch["tone"],
        "cta": ch["cta"],
        "brand": dict(ch["brand"]),
        "is_advertising": bool(ads),
        "channel_ref": channel,
        "assumptions": assumptions,
        "constraints": [
            "Chỉ dùng hình, nhạc, font tự tạo hoặc có giấy phép rõ ràng",
            "Giọng đọc AI phải được gắn nhãn khi xuất bản (Luật Trí tuệ nhân tạo 134/2025/QH15)",
        ],
    }
    create_project(project, title)
    return dump_yaml(path, brief)
