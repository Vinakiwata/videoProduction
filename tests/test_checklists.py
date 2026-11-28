from vp.checklist import CHECKLIST_DIR, load_checklist
from vp.stages import STAGES


def test_every_stage_has_valid_checklist():
    for st in STAGES:
        cl = load_checklist(st.code, CHECKLIST_DIR)
        assert cl["stage"] == st.code
        assert len(cl["items"]) >= 5, st.code


def test_ids_unique_across_all_checklists():
    seen = set()
    for st in STAGES:
        for it in load_checklist(st.code, CHECKLIST_DIR)["items"]:
            assert it["id"] not in seen, it["id"]
            seen.add(it["id"])


def test_every_stage_has_blocker():
    for st in STAGES:
        sev = {i["severity"] for i in load_checklist(st.code, CHECKLIST_DIR)["items"]}
        assert "chan" in sev, st.code


def test_all_real_checklists_load():
    """Mọi checklist thật trong repo phải nạp được: đủ khoá, không trùng id, kiểm tra tự động đã đăng ký."""
    from vp.checklist import load_checklist
    from vp.stages import STAGES
    from conftest import ROOT
    loaded = [st.code for st in STAGES if (ROOT / "checklists" / f"{st.code}.yaml").is_file()]
    assert len(loaded) >= 7
    for code in loaded:
        load_checklist(code)
