import json

import pytest
import yaml

from conftest import write_yaml
from vp import review
from vp.review import ReviewError

GOOD = "Đã đọc toàn bộ kịch bản, đoạn S02-02 có nguồn SRC1 (NASA)."


def judge(rdir, **items):
    write_yaml(rdir / "judgments.yaml", items)


def full_pass(rdir):
    judge(rdir,
          **{"T-C01": {"verdict": "pass", "evidence": GOOD},
             "T-C02": {"verdict": "pass", "evidence": "S01-01 đặt câu hỏi ngay giây đầu tiên."},
             "T-C03": {"verdict": "pass", "evidence": "Không có từ lặp quá 2 lần trong một câu."}})


def pass_brief(project, checklist_dir):
    rdir = review.start(project, "brief", checklist_dir=checklist_dir)
    return review.finalize(project, "brief", checklist_dir=checklist_dir)


def test_start_requires_previous_gate(project, checklist_dir):
    with pytest.raises(ReviewError, match="brief"):
        review.start(project, "script", checklist_dir=checklist_dir)


def test_start_runs_auto_and_lists_ai(project, checklist_dir):
    pass_brief(project, checklist_dir)
    rdir = review.start(project, "script", checklist_dir=checklist_dir)
    data = json.loads((rdir / "review.json").read_text(encoding="utf-8"))
    assert data["status"] == "pending"
    items = {i["id"]: i for i in data["items"]}
    assert items["T-A01"]["result"] == "pass"
    assert items["T-C01"]["result"] is None
    tpl = yaml.safe_load((rdir / "judgments.yaml").read_text(encoding="utf-8"))
    assert set(tpl) == {"T-C01", "T-C02", "T-C03"}


def test_full_pass_gives_dat(project, checklist_dir):
    pass_brief(project, checklist_dir)
    rdir = review.start(project, "script", checklist_dir=checklist_dir)
    full_pass(rdir)
    res = review.finalize(project, "script", checklist_dir=checklist_dir)
    assert res["decision"] == "DAT"
    assert res["score"] == 100
    assert "ĐẠT" in (rdir / "report.md").read_text(encoding="utf-8")
    log = (project / "reviews" / "LOG.md").read_text(encoding="utf-8")
    assert "script" in log and "ĐẠT" in log
    link = log.strip().splitlines()[-1].split("](")[1].rstrip(")| ")
    assert (project / "reviews" / link).is_file(), link
    assert review.gate(project, "script").ok


def test_missing_judgment_rejected(project, checklist_dir):
    pass_brief(project, checklist_dir)
    rdir = review.start(project, "script", checklist_dir=checklist_dir)
    judge(rdir, **{"T-C01": {"verdict": "pass", "evidence": GOOD}})
    with pytest.raises(ReviewError, match="T-C02"):
        review.finalize(project, "script", checklist_dir=checklist_dir)


def test_pass_without_evidence_rejected(project, checklist_dir):
    pass_brief(project, checklist_dir)
    rdir = review.start(project, "script", checklist_dir=checklist_dir)
    full_pass(rdir)
    j = yaml.safe_load((rdir / "judgments.yaml").read_text(encoding="utf-8"))
    j["T-C01"]["evidence"] = "ok"
    judge(rdir, **j)
    with pytest.raises(ReviewError, match="bằng chứng"):
        review.finalize(project, "script", checklist_dir=checklist_dir)


def test_fail_requires_fix(project, checklist_dir):
    pass_brief(project, checklist_dir)
    rdir = review.start(project, "script", checklist_dir=checklist_dir)
    full_pass(rdir)
    j = yaml.safe_load((rdir / "judgments.yaml").read_text(encoding="utf-8"))
    j["T-C02"] = {"verdict": "fail", "evidence": "Mở đầu chậm, 6 giây chưa vào ý chính."}
    judge(rdir, **j)
    with pytest.raises(ReviewError, match="hướng sửa"):
        review.finalize(project, "script", checklist_dir=checklist_dir)


def test_major_fail_blocks_gate(project, checklist_dir):
    pass_brief(project, checklist_dir)
    rdir = review.start(project, "script", checklist_dir=checklist_dir)
    full_pass(rdir)
    j = yaml.safe_load((rdir / "judgments.yaml").read_text(encoding="utf-8"))
    j["T-C02"] = {"verdict": "fail", "evidence": "Mở đầu chậm, 6 giây chưa vào ý chính.",
                  "fix": "Đưa câu hỏi lên giây đầu, cắt phần chào."}
    judge(rdir, **j)
    res = review.finalize(project, "script", checklist_dir=checklist_dir)
    assert res["decision"] == "KHONG_DAT"
    assert res["score"] == round(100 * (5 + 5 + 1) / (5 + 5 + 3 + 1))
    assert not review.gate(project, "script").ok
    report = (rdir / "report.md").read_text(encoding="utf-8")
    assert "KHÔNG ĐẠT" in report and "Đưa câu hỏi lên giây đầu" in report


def test_minor_fail_still_dat(project, checklist_dir):
    pass_brief(project, checklist_dir)
    rdir = review.start(project, "script", checklist_dir=checklist_dir)
    full_pass(rdir)
    j = yaml.safe_load((rdir / "judgments.yaml").read_text(encoding="utf-8"))
    j["T-C03"] = {"verdict": "fail", "evidence": "Từ 'xanh' lặp 3 lần ở S02-03.", "fix": "Thay một chữ bằng 'lam'."}
    judge(rdir, **j)
    assert review.finalize(project, "script", checklist_dir=checklist_dir)["decision"] == "DAT"


def test_na_only_when_allowed(project, checklist_dir):
    pass_brief(project, checklist_dir)
    rdir = review.start(project, "script", checklist_dir=checklist_dir)
    full_pass(rdir)
    j = yaml.safe_load((rdir / "judgments.yaml").read_text(encoding="utf-8"))
    j["T-C01"] = {"verdict": "na", "evidence": "Kịch bản không có khẳng định nào cả."}
    judge(rdir, **j)
    with pytest.raises(ReviewError, match="không áp dụng"):
        review.finalize(project, "script", checklist_dir=checklist_dir)
    j["T-C01"] = {"verdict": "pass", "evidence": GOOD}
    j["T-C03"] = {"verdict": "na", "evidence": "Video không lời, không có câu chữ để xét."}
    judge(rdir, **j)
    assert review.finalize(project, "script", checklist_dir=checklist_dir)["decision"] == "DAT"


def test_cannot_override_auto(project, checklist_dir):
    pass_brief(project, checklist_dir)
    rdir = review.start(project, "script", checklist_dir=checklist_dir)
    full_pass(rdir)
    j = yaml.safe_load((rdir / "judgments.yaml").read_text(encoding="utf-8"))
    j["T-A01"] = {"verdict": "pass", "evidence": "Tôi thấy ổn, cho qua mục tự động."}
    judge(rdir, **j)
    with pytest.raises(ReviewError, match="T-A01"):
        review.finalize(project, "script", checklist_dir=checklist_dir)


def test_artifact_changed_during_review(project, checklist_dir):
    pass_brief(project, checklist_dir)
    rdir = review.start(project, "script", checklist_dir=checklist_dir)
    full_pass(rdir)
    with open(project / "01_script" / "script.yaml", "a", encoding="utf-8") as f:
        f.write("\n# sửa\n")
    with pytest.raises(ReviewError, match="thay đổi"):
        review.finalize(project, "script", checklist_dir=checklist_dir)


def test_gate_expires_when_artifact_edited(project, checklist_dir):
    pass_brief(project, checklist_dir)
    rdir = review.start(project, "script", checklist_dir=checklist_dir)
    full_pass(rdir)
    review.finalize(project, "script", checklist_dir=checklist_dir)
    with open(project / "01_script" / "script.yaml", "a", encoding="utf-8") as f:
        f.write("\n# sửa sau duyệt\n")
    g = review.gate(project, "script")
    assert not g.ok and "HẾT HIỆU LỰC" in g.message


def test_auto_error_blocks(project, checklist_dir):
    (project / "00_brief" / "brief.yaml").unlink()
    rdir = review.start(project, "brief", checklist_dir=checklist_dir)
    res = review.finalize(project, "brief", checklist_dir=checklist_dir)
    assert res["decision"] == "KHONG_DAT"


def test_override(project, checklist_dir):
    pass_brief(project, checklist_dir)
    rdir = review.start(project, "script", checklist_dir=checklist_dir)
    full_pass(rdir)
    j = yaml.safe_load((rdir / "judgments.yaml").read_text(encoding="utf-8"))
    j["T-C02"] = {"verdict": "fail", "evidence": "Mở đầu chậm, 6 giây chưa vào ý chính.",
                  "fix": "Đưa câu hỏi lên giây đầu."}
    judge(rdir, **j)
    review.finalize(project, "script", checklist_dir=checklist_dir)
    with pytest.raises(ReviewError):
        review.override(project, "script", by="", reason="x")
    review.override(project, "script", by="Vinakiwata", reason="Chấp nhận mở đầu chậm cho bản thử nghiệm")
    g = review.gate(project, "script")
    assert g.ok and "CHO QUA" in g.message
    assert "CHO QUA" in (project / "reviews" / "LOG.md").read_text(encoding="utf-8")


def test_finalize_without_pending(project, checklist_dir):
    with pytest.raises(ReviewError, match="chưa có"):
        review.finalize(project, "brief", checklist_dir=checklist_dir)
