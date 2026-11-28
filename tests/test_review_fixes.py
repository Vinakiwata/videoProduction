"""Sửa sau review toàn nhánh khung dọc: mỗi test tái hiện một phát hiện Important."""
import shutil

import pytest
import yaml

from conftest import write_yaml
from vp import platforms as pf
from vp import review
from vp.checks import run_check
from test_presentation import pproj  # noqa: F401  — fixture dự án Tool 07 mẫu

V = {"width": 1080, "height": 1920, "fps": 30}
ALL3 = ["youtube_shorts", "tiktok", "reels"]


def _brief(project, **kv):
    b = yaml.safe_load((project / "00_brief" / "brief.yaml").read_text(encoding="utf-8"))
    b.update(kv)
    for k, v in kv.items():
        if v is None:
            b.pop(k)
    write_yaml(project / "00_brief" / "brief.yaml", b)


# Important 1: khung storyboard phải trùng khung của brief
def test_dsn_a08_flags_storyboard_canvas_mismatch(project):
    _brief(project, format=dict(V), platforms=ALL3)
    write_yaml(project / "02_design" / "storyboard.yaml", {"meta": {"title": "T", "canvas": {"width": 1920, "height": 1080, "fps": 30}},
                                                           "assets": [], "shots": []})
    r = run_check("storyboard_safe_area", project, {"path": "02_design/storyboard.yaml", "brief": "00_brief/brief.yaml"})
    assert r.status == "fail" and "1920×1080" in r.evidence and "1080×1920" in r.evidence


@pytest.fixture
def mism(pproj):
    b = yaml.safe_load((pproj / "00_brief" / "brief.yaml").read_text(encoding="utf-8"))
    b["format"], b["platforms"] = dict(V), ALL3
    write_yaml(pproj / "00_brief" / "brief.yaml", b)        # storyboard của pproj vẫn 1920×1080
    return pproj


def test_compile_raises_when_storyboard_canvas_differs_from_brief(mism):
    from vp import presentation_tools as pt
    with pytest.raises(pt.PresentationError) as e:
        pt.compile_presentation(mism)
    assert "1920×1080" in str(e.value) and "1080×1920" in str(e.value)


# Important 2: sửa số đo trong platforms/*.yaml phải làm bản dựng 07 cũ và cổng hết hiệu lực
def test_presentation_input_hash_covers_platform_profiles(pproj, tmp_path, monkeypatch):
    from vp import presentation_tools as pt
    d = tmp_path / "plats"
    shutil.copytree(pf.PLATFORMS_DIR, d)
    monkeypatch.setattr(pf, "PLATFORMS_DIR", d)
    b = yaml.safe_load((pproj / "00_brief" / "brief.yaml").read_text(encoding="utf-8"))
    b["format"], b["platforms"] = dict(V), ALL3
    write_yaml(pproj / "00_brief" / "brief.yaml", b)
    h1 = pt.input_hash(pproj)
    prof = yaml.safe_load((d / "youtube_shorts.yaml").read_text(encoding="utf-8"))
    prof["safe_margins_px"]["right"] = 200
    write_yaml(d / "youtube_shorts.yaml", prof)
    assert pt.input_hash(pproj) != h1


def test_hash_artifacts_repo_path(project, tmp_path, monkeypatch):
    d = tmp_path / "repo" / "platforms"
    d.mkdir(parents=True)
    (d / "a.yaml").write_text("x: 1", encoding="utf-8")
    monkeypatch.setattr(review, "REPO_ROOT", tmp_path / "repo")
    h1 = review.hash_artifacts(project, ["@platforms"])["@platforms"]
    (d / "a.yaml").write_text("x: 2", encoding="utf-8")
    h2 = review.hash_artifacts(project, ["@platforms"])["@platforms"]
    assert h1 and h2 and h1 != h2


def test_design_and_presentation_checklists_seal_platform_profiles():
    from vp.checklist import load_checklist
    for st in ("design", "presentation"):
        assert "@platforms" in load_checklist(st)["artifacts"], st


# Important 3: brief không chọn nền tảng (kênh/dự án cũ) không bị chặn vĩnh viễn
def test_brief_without_platforms_passes_with_legacy_note(project):
    _brief(project, platforms=None)
    r = run_check("brief_platforms", project, {"path": "00_brief/brief.yaml"})
    assert r.status == "pass" and "5%" in r.evidence


# Important 4: tên nền tảng sai không làm CLI văng traceback
def test_cli_reports_platform_error_cleanly(project, capsys):
    from vp.__main__ import main
    _brief(project, platforms=["tik_tok"])
    write_yaml(project / "02_design" / "storyboard.yaml", {"meta": {"title": "T", "canvas": dict(V)}, "assets": [], "shots": []})
    with pytest.raises(SystemExit) as e:
        main(["design", "preview", str(project)])
    assert "tik_tok" in str(e.value.code) and str(e.value.code).startswith("LỖI")
