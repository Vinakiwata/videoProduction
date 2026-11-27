"""Tạo khung thư mục cho một dự án video."""
from pathlib import Path

import yaml

from vp import stages


def create_project(project: Path, title: str) -> Path:
    project = Path(project)
    for st in stages.STAGES:
        (project / st.folder).mkdir(parents=True, exist_ok=True)
    meta = project / "project.yaml"
    if not meta.is_file():
        meta.write_text(yaml.safe_dump({"slug": project.name, "title": title, "language": "vi"},
                                       allow_unicode=True, sort_keys=False), encoding="utf-8")
    return project


def dump_yaml(path: Path, data) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8")
    return path
