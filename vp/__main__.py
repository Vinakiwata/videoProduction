"""Dòng lệnh: python -m vp <lệnh> ...

  new <thư-mục-dự-án> --title "..."          tạo khung dự án
  review start <dự án> <công đoạn>             chạy mục tự động, tạo phiếu chấm
  review finalize <dự án> <công đoạn>          kiểm phần chấm, ra quyết định, ghi báo cáo
  review override <dự án> <công đoạn> --by TÊN --reason "..."
  gate <dự án> <công đoạn>                     mã thoát 0 nếu cổng đang mở
  status <dự án>                               trạng thái cổng của mọi công đoạn
"""
import argparse
import json
import sys
from pathlib import Path

import yaml

from vp import review, stages
from vp.checklist import ChecklistError


def cmd_new(a):
    p = Path(a.project)
    if p.exists() and any(p.iterdir()):
        sys.exit(f"Thư mục {p} đã có dữ liệu.")
    for st in stages.STAGES:
        (p / st.folder).mkdir(parents=True, exist_ok=True)
    (p / "project.yaml").write_text(
        yaml.safe_dump({"slug": p.name, "title": a.title, "language": "vi"}, allow_unicode=True, sort_keys=False),
        encoding="utf-8")
    print(f"Đã tạo dự án {p}")


def cmd_review(a):
    p = Path(a.project)
    if a.action == "start":
        rdir = review.start(p, a.stage)
        data = json.loads((rdir / "review.json").read_text(encoding="utf-8"))
        print(f"Đã mở lần duyệt: {rdir}")
        for it in data["items"]:
            mark = it["result"] or "CHỜ CHẤM"
            print(f"  [{mark:>8}] {it['id']} {it['title']}")
        print(f"Chấm các mục 'CHỜ CHẤM' trong {rdir / 'judgments.yaml'} rồi chạy 'review finalize'.")
    elif a.action == "finalize":
        res = review.finalize(p, a.stage, reviewer=a.reviewer)
        print(f"{review.DECISION_LABEL[res['decision']]} — điểm {res['score']}/100")
        if res["blocking"]:
            print("Mục chặn cổng: " + ", ".join(res["blocking"]))
        print(f"Báo cáo: {res['report']}")
    elif a.action == "override":
        review.override(p, a.stage, by=a.by, reason=a.reason)
        print("Đã ghi nhận CHO QUA.")


def cmd_gate(a):
    g = review.gate(Path(a.project), a.stage)
    print(("MỞ: " if g.ok else "ĐÓNG: ") + g.message)
    sys.exit(0 if g.ok else 1)


def cmd_status(a):
    p = Path(a.project)
    for st in stages.STAGES:
        g = review.gate(p, st.code)
        print(f"{'✅' if g.ok else '⛔'} {st.folder:<16} {st.name:<32} {g.message}")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="vp", description="Dây chuyền sản xuất video — cổng kiểm duyệt")
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new"); n.add_argument("project"); n.add_argument("--title", required=True)
    n.set_defaults(fn=cmd_new)
    r = sub.add_parser("review")
    r.add_argument("action", choices=["start", "finalize", "override"])
    r.add_argument("project"); r.add_argument("stage", choices=list(stages.BY_CODE))
    r.add_argument("--reviewer", default="Claude"); r.add_argument("--by"); r.add_argument("--reason")
    r.set_defaults(fn=cmd_review)
    g = sub.add_parser("gate"); g.add_argument("project"); g.add_argument("stage", choices=list(stages.BY_CODE))
    g.set_defaults(fn=cmd_gate)
    s = sub.add_parser("status"); s.add_argument("project"); s.set_defaults(fn=cmd_status)
    a = ap.parse_args(argv)
    try:
        a.fn(a)
    except (review.ReviewError, ChecklistError) as e:
        sys.exit(f"LỖI: {e}")


if __name__ == "__main__":
    main()
