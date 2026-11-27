import pytest
import yaml

from conftest import write_yaml
from vp.brief import BriefError, new_brief
from vp.checks import run_check

CHANNEL = {
    "name": "Kênh thử", "channel": "youtube",
    "format": {"width": 1920, "height": 1080, "fps": 30},
    "default_duration_s": 60, "tone": "Thân thiện, rõ ràng", "cta": "Đăng ký kênh nhé",
    "audience": "Người lớn tò mò về khoa học",
    "brand": {"colors": ["#112233"], "fonts": ["Be Vietnam Pro"], "voice": "VieNeu-TTS: Hải Đăng"},
    "voice_profile": {"syllables_per_second": 3.0},
}


@pytest.fixture
def channels(tmp_path):
    d = tmp_path / "channels"
    write_yaml(d / "kenh-thu" / "channel.yaml", CHANNEL)
    return d


def read(p):
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def test_new_brief_merges_channel(tmp_path, channels):
    proj = tmp_path / "projects" / "v1"
    path = new_brief(proj, channel="kenh-thu", title="Vì sao lá rụng", goal="Người xem giải thích lại được vì sao cây rụng lá mùa đông",
                     duration=45, ads=False, channels_dir=channels)
    b = read(path)
    assert b["title"] == "Vì sao lá rụng"
    assert b["target_duration_s"] == 45            # tham số ưu tiên hơn kênh
    assert b["brand"]["colors"] == ["#112233"]      # lấy từ kênh
    assert b["channel_ref"] == "kenh-thu"
    assert b["is_advertising"] is False
    assert any("audience" in a for a in b["assumptions"])  # khán giả lấy mặc định -> ghi giả định
    assert (proj / "01_script").is_dir() and (proj / "project.yaml").is_file()
    r = run_check("yaml_schema", proj, {"path": "00_brief/brief.yaml", "schema": "brief"})
    assert r.status == "pass", r.evidence


def test_missing_goal_is_todo_and_blocked(tmp_path, channels):
    proj = tmp_path / "projects" / "v2"
    new_brief(proj, channel="kenh-thu", title="Chủ đề", channels_dir=channels)
    b = read(proj / "00_brief" / "brief.yaml")
    assert b["goal"].startswith("TODO")
    assert any("quảng cáo" in a for a in b["assumptions"])
    r = run_check("no_placeholders", proj, {"path": "00_brief/brief.yaml"})
    assert r.status == "fail" and "goal" in r.evidence


def test_no_overwrite(tmp_path, channels):
    proj = tmp_path / "projects" / "v3"
    new_brief(proj, channel="kenh-thu", title="A", channels_dir=channels)
    with pytest.raises(BriefError, match="đã có"):
        new_brief(proj, channel="kenh-thu", title="B", channels_dir=channels)


def test_unknown_channel(tmp_path, channels):
    with pytest.raises(BriefError, match="kenh-khong-co"):
        new_brief(tmp_path / "p", channel="kenh-khong-co", title="A", channels_dir=channels)


def test_repo_sample_channel_valid():
    from vp.channel import load_channel
    ch = load_channel("kenh-khoa-hoc-mau")
    assert ch["voice_profile"]["syllables_per_second"] > 0


def test_brand_voice_valid(project):
    from conftest import write_yaml
    import yaml as _y
    p = {"path": "00_brief/brief.yaml"}
    assert run_check("brand_voice_valid", project, p).status == "pass"
    b = _y.safe_load((project / "00_brief" / "brief.yaml").read_text(encoding="utf-8"))
    b["brand"]["voice"] = "VieNeu-TTS v3 Turbo: Ngọc Lan"     # tên không tồn tại trong v3 Turbo
    write_yaml(project / "00_brief" / "brief.yaml", b)
    r = run_check("brand_voice_valid", project, p)
    assert r.status == "fail" and "Ngọc Lan" in r.evidence
