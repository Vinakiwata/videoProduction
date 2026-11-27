"""Danh sách 12 công đoạn của dây chuyền, theo đúng thứ tự chạy."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Stage:
    code: str
    folder: str
    name: str


STAGES: list[Stage] = [
    Stage("brief", "00_brief", "Brief & bộ nhận diện"),
    Stage("script", "01_script", "Kịch bản"),
    Stage("design", "02_design", "Thiết kế nội dung & storyboard"),
    Stage("animatic", "03_animatic", "Animatic (bản nháp thô)"),
    Stage("voice", "04_voice", "Giọng đọc"),
    Stage("timeline", "05_timeline", "Timeline tổng"),
    Stage("animation", "06_animation", "Hoạt ảnh 2D"),
    Stage("presentation", "07_presentation", "Web trình chiếu"),
    Stage("render", "08_render", "Render khung hình"),
    Stage("mix", "09_mix", "Mix âm thanh & ghép video"),
    Stage("final", "10_final", "QC tổng"),
    Stage("package", "11_package", "Đóng gói xuất bản"),
]

BY_CODE = {s.code: s for s in STAGES}


def get(code: str) -> Stage:
    if code not in BY_CODE:
        raise KeyError(f"Không có công đoạn '{code}'. Hợp lệ: {', '.join(BY_CODE)}")
    return BY_CODE[code]


def previous(code: str) -> Stage | None:
    i = STAGES.index(get(code))
    return STAGES[i - 1] if i > 0 else None
