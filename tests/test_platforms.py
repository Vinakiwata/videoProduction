import json
from datetime import date, timedelta

import pytest
import yaml
from jsonschema import Draft202012Validator

from conftest import write_yaml
from vp import platforms as pf
from vp.checks import run_check

ALL3 = ["youtube_shorts", "tiktok", "reels"]


def vbrief(**over):
    b = {"format": {"width": 1080, "height": 1920, "fps": 30}, "platforms": list(ALL3), "target_duration_s": 50}
    b.update(over)
    return b


def test_profiles_valid_schema():
    schema = json.loads((pf.SCHEMA).read_text(encoding="utf-8"))
    for pid in ALL3:
        prof = yaml.safe_load((pf.PLATFORMS_DIR / f"{pid}.yaml").read_text(encoding="utf-8"))
        assert not list(Draft202012Validator(schema).iter_errors(prof)), pid
        assert prof["id"] == pid and len(prof["ui_zones"]) == 3


def test_safe_margins_union_all_three():
    m = pf.safe_margins(vbrief())
    assert (m["top"], m["bottom"], m["left"], m["right"]) == (220, 461, 65, 173)
    assert m["by"]["top"] == "reels" and m["by"]["right"] == "youtube_shorts" and m["by"]["bottom"] == "youtube_shorts"


def test_safe_margins_tiktok_only():
    m = pf.safe_margins(vbrief(platforms=["tiktok"]))
    assert (m["top"], m["bottom"], m["left"], m["right"]) == (108, 320, 60, 120)


def test_legacy_brief_5pct():
    m = pf.safe_margins({"format": {"width": 1920, "height": 1080, "fps": 30}})
    assert (m["top"], m["bottom"], m["left"], m["right"]) == (54, 54, 96, 96) and m["by"] == {}
    assert pf.canvas({"format": {"width": 1920, "height": 1080, "fps": 30}}) == {"width": 1920, "height": 1080, "fps": 30}


def test_canvas_vertical():
    assert pf.canvas(vbrief()) == {"width": 1080, "height": 1920, "fps": 30}


def _fake_dir(tmp_path, **profiles):
    d = tmp_path / "platforms"
    d.mkdir()
    for pid in ALL3:
        (d / f"{pid}.yaml").write_text((pf.PLATFORMS_DIR / f"{pid}.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    for pid, changes in profiles.items():
        p = yaml.safe_load((d / f"{pid}.yaml").read_text(encoding="utf-8")) if (d / f"{pid}.yaml").exists() else \
            yaml.safe_load((pf.PLATFORMS_DIR / "tiktok.yaml").read_text(encoding="utf-8"))
        p.update(changes, id=pid)
        write_yaml(d / f"{pid}.yaml", p)
    return d


def test_mixed_canvas_rejected(tmp_path):
    d = _fake_dir(tmp_path, youtube_long={"canvas": {"width": 1920, "height": 1080, "fps": 30}})
    with pytest.raises(pf.PlatformError) as e:
        pf.canvas(vbrief(platforms=["youtube_long", "tiktok"]), d)
    assert "1920×1080" in str(e.value) and "1080×1920" in str(e.value)


def _proj(project, brief):
    write_yaml(project / "00_brief" / "brief.yaml", brief)
    return project


def test_unknown_platform_fails(project):
    r = run_check("brief_platforms", _proj(project, vbrief(platforms=["tik_tok"])), {"path": "00_brief/brief.yaml"})
    assert r.status == "fail" and "tik_tok" in r.evidence and "youtube_shorts" in r.evidence


def test_brief_platforms_pass(project):
    r = run_check("brief_platforms", _proj(project, vbrief()), {"path": "00_brief/brief.yaml"})
    assert r.status == "pass", r.evidence


def test_brief_format_mismatch_fails(project):
    b = vbrief(format={"width": 1920, "height": 1080, "fps": 30})
    assert run_check("brief_platforms", _proj(project, b), {"path": "00_brief/brief.yaml"}).status == "fail"


def test_duration_over_platform_limit_fails(project, tmp_path):
    d = _fake_dir(tmp_path, tiktok={"max_duration_s": 30})
    r = run_check("brief_platforms", _proj(project, vbrief()), {"path": "00_brief/brief.yaml", "platforms_dir": str(d)})
    assert r.status == "fail" and "TikTok" in r.evidence


def test_stale_profile_fails(project, tmp_path):
    old = (date.today() - timedelta(days=200)).isoformat()
    d = _fake_dir(tmp_path, reels={"checked": old})
    params = {"path": "00_brief/brief.yaml", "max_age_days": 180, "platforms_dir": str(d)}
    r = run_check("platform_profiles_fresh", _proj(project, vbrief()), params)
    assert r.status == "fail" and "Reels" in r.evidence
    assert run_check("platform_profiles_fresh", project, {**params, "platforms_dir": None}).status == "pass"
