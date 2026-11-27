import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).parent / "fixtures"


def write_yaml(path: Path, data) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return path


@pytest.fixture
def good_script():
    return yaml.safe_load((FIXTURES / "script_good.yaml").read_text(encoding="utf-8"))


@pytest.fixture
def project(tmp_path, good_script):
    """Dự án tạm có brief + kịch bản hợp lệ."""
    p = tmp_path / "projects" / "demo"
    write_yaml(p / "project.yaml", {"slug": "demo", "title": "Demo", "language": "vi"})
    (p / "00_brief").mkdir(parents=True)
    shutil.copy(FIXTURES / "brief_good.yaml", p / "00_brief" / "brief.yaml")
    write_yaml(p / "01_script" / "script.yaml", good_script)
    return p


@pytest.fixture
def checklist_dir(tmp_path):
    """Thư mục checklist nhỏ dùng riêng cho test luồng duyệt."""
    d = tmp_path / "checklists"
    write_yaml(d / "brief.yaml", {
        "stage": "brief", "version": 1, "title": "Test brief",
        "artifacts": ["00_brief/brief.yaml"],
        "items": [
            {"id": "B-A01", "group": "Cấu trúc", "title": "Brief tồn tại", "severity": "chan",
             "method": "auto", "check": "file_exists", "params": {"paths": ["00_brief/brief.yaml"]}},
        ],
    })
    write_yaml(d / "script.yaml", {
        "stage": "script", "version": 1, "title": "Test kịch bản",
        "artifacts": ["01_script/script.yaml"],
        "items": [
            {"id": "T-A01", "group": "Cấu trúc", "title": "Đúng schema", "severity": "chan",
             "method": "auto", "check": "yaml_schema",
             "params": {"path": "01_script/script.yaml", "schema": "script"}},
            {"id": "T-C01", "group": "Nội dung", "title": "Đúng sự thật", "severity": "chan",
             "method": "ai", "guidance": "Mọi khẳng định có nguồn."},
            {"id": "T-C02", "group": "Nội dung", "title": "Mở đầu hấp dẫn", "severity": "nghiem_trong",
             "method": "ai", "guidance": "Hook trong 5 giây đầu."},
            {"id": "T-C03", "group": "Văn phong", "title": "Câu chữ mượt", "severity": "nhe",
             "method": "ai", "guidance": "Không lặp từ.", "allow_na": True},
        ],
    })
    return d


def make_video(path: Path, *, seconds=2, size="1920x1080", fps=30, color="blue",
               black_first=0.0, audio=True, tone_db=-14):
    """Sinh video thử bằng ffmpeg lavfi."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if black_first:
        vf = (f"color=c=black:s={size}:r={fps}:d={black_first}[a];"
              f"testsrc2=s={size}:r={fps}:d={seconds - black_first}[b];[a][b]concat=n=2:v=1:a=0[v]")
    else:
        vf = f"testsrc2=s={size}:r={fps}:d={seconds}[v]"
    cmd = ["ffmpeg", "-y", "-v", "error"]
    if audio:
        cmd += ["-f", "lavfi", "-i", f"sine=f=440:d={seconds}:sample_rate=48000"]
    cmd += ["-filter_complex", vf, "-map", "[v]"]
    if audio:
        cmd += ["-map", "0:a", "-filter:a", f"volume={tone_db + 3}dB", "-c:a", "aac"]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-t", str(seconds), str(path)]
    subprocess.run(cmd, check=True)
    return path
