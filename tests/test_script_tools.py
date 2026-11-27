import pytest
import yaml

from conftest import write_yaml
from vp import script_tools as st
from vp.checks import run_check

DRAFT = """Bạn có biết vì sao lá cây chuyển vàng vào mùa thu không?
> Một chiếc lá xanh chuyển dần sang vàng

# Diệp lục
Lá xanh nhờ diệp lục. Khi ngày ngắn lại, cây ngừng tạo diệp lục.

(im lặng 1.5)

# Kết
Đăng ký kênh nhé!
"""


@pytest.fixture
def proj(project):
    (project / "01_script" / "script.yaml").unlink()
    return project


def load(project):
    return yaml.safe_load((project / "01_script" / "script.yaml").read_text(encoding="utf-8"))


def test_import_structure(proj, tmp_path):
    src = tmp_path / "draft.md"
    src.write_text(DRAFT, encoding="utf-8")
    st.import_draft(proj, src)
    s = load(proj)
    assert s["meta"]["target_duration_s"] == 30          # lấy từ brief
    assert [sc["title"] for sc in s["scenes"]] == ["Mở đầu", "Diệp lục", "Kết"]
    first = s["scenes"][0]["segments"][0]
    assert first["id"] == "S01-01" and first["kind"] == "voice"
    assert first["visual"] == "Một chiếc lá xanh chuyển dần sang vàng"
    seg2 = s["scenes"][1]["segments"]
    assert seg2[0]["text"].startswith("Lá xanh nhờ diệp lục.")
    assert seg2[0]["visual"].startswith("TODO")
    assert seg2[1] == {"id": "S02-02", "kind": "silent", "est_duration_s": 1.5, "visual": "TODO: mô tả hình"}
    assert all(seg["est_duration_s"] > 0 for sc in s["scenes"] for seg in sc["segments"])
    assert s["scenes"][0]["purpose"].startswith("TODO")


def test_import_splits_long_sentences(proj, tmp_path):
    long = ", ".join(["đây là một vế câu khá dài để thử tách"] * 12) + "."
    src = tmp_path / "d.md"
    src.write_text(long, encoding="utf-8")
    st.import_draft(proj, src)
    segs = load(proj)["scenes"][0]["segments"]
    assert len(segs) > 1
    assert all(len(x["text"]) <= 200 for x in segs)
    assert " ".join(x["text"] for x in segs).replace(" ,", ",") .split() == long.split()


def test_import_refuses_overwrite(project, tmp_path):
    src = tmp_path / "d.md"
    src.write_text("Xin chào các bạn.", encoding="utf-8")
    with pytest.raises(st.ScriptToolError, match="đã có"):
        st.import_draft(project, src)
    st.import_draft(project, src, force=True)


def test_estimate_formula(project):
    n = st.estimate(project, sps=3.0)
    s = load(project)
    seg = s["scenes"][0]["segments"][0]                  # 15 âm tiết
    assert seg["est_duration_s"] == 5.0
    assert s["scenes"][0]["segments"][1]["est_duration_s"] == 1   # silent giữ nguyên
    assert n == 5
    assert st.estimate_seconds("một hai ba", 3.2) == 1.0          # 0.9375 -> 1.0
    assert st.estimate_seconds("ừ", 3.2) == 0.5                   # tối thiểu 0,5 giây


def test_estimate_uses_channel_voice_profile(project, tmp_path):
    ch = tmp_path / "channels"
    write_yaml(ch / "k" / "channel.yaml", {"voice_profile": {"syllables_per_second": 5.0}})
    b = yaml.safe_load((project / "00_brief" / "brief.yaml").read_text(encoding="utf-8"))
    b["channel_ref"] = "k"
    write_yaml(project / "00_brief" / "brief.yaml", b)
    assert st.resolve_sps(project, None, channels_dir=ch) == 5.0
    assert st.resolve_sps(project, 2.0, channels_dir=ch) == 2.0


def test_view_and_sync(project):
    st.view(project)
    md = (project / "01_script" / "script.md").read_text(encoding="utf-8")
    assert "| 00:00.0 | S01-01 |" in md
    assert "| 00:04.0 | S01-02 |" in md        # luỹ kế: đoạn 1 dài 4 giây
    assert "Tổng thời lượng: 29.0 giây" in md
    assert "NASA" in md
    p = {"path": "01_script/script.yaml", "view": "01_script/script.md"}
    assert run_check("script_view_in_sync", project, p).status == "pass"
    with open(project / "01_script" / "script.yaml", "a", encoding="utf-8") as f:
        f.write("\n")
    assert run_check("script_view_in_sync", project, p).status == "pass"   # chỉ đổi định dạng, nội dung giữ nguyên
    s = load(project); s["scenes"][0]["segments"][0]["text"] = "Câu mới hoàn toàn khác nhé bạn ơi."
    write_yaml(project / "01_script" / "script.yaml", s)
    r = run_check("script_view_in_sync", project, p)
    assert r.status == "fail" and "view" in r.evidence


def test_lint(project):
    st.view(project)
    results = st.lint(project)
    assert results and all(r.status == "pass" for _, r in results)
    s = load(project); s["scenes"][0]["segments"][0]["text"] = "TODO viết sau"
    write_yaml(project / "01_script" / "script.yaml", s)
    bad = [it["id"] for it, r in st.lint(project) if r.status != "pass"]
    assert "SCR-A04" in bad
    assert not (project / "reviews").exists()   # lint không mở lần duyệt
