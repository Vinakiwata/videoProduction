"""Engine kiểm duyệt: start -> (chấm mục AI) -> finalize -> gate.

Luật chấm và quyết định cổng: xem docs/superpowers/specs/2026-11-27-kien-truc-va-kiem-duyet-design.md
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml

from vp import stages
from vp.checklist import load_checklist
from vp.checks import run_check

TZ = ZoneInfo("Asia/Ho_Chi_Minh")
WEIGHTS = {"chan": 5, "nghiem_trong": 3, "nhe": 1}
SEV_LABEL = {"chan": "Chặn", "nghiem_trong": "Nghiêm trọng", "nhe": "Nhẹ"}
RESULT_LABEL = {"pass": "✅ Đạt", "fail": "❌ Trượt", "error": "⚠️ Lỗi kiểm tra", "na": "➖ Không áp dụng"}
DECISION_LABEL = {"DAT": "✅ ĐẠT", "KHONG_DAT": "❌ KHÔNG ĐẠT"}
MIN_EVIDENCE, MIN_FIX = 20, 10


class ReviewError(RuntimeError):
    pass


@dataclass
class GateStatus:
    ok: bool
    message: str


# ---------- tiện ích ----------

def _now() -> datetime:
    return datetime.now(TZ)


def _reviews(project: Path) -> Path:
    return project / "reviews"


def _load_state(project: Path) -> dict:
    p = _reviews(project) / "state.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"stages": {}}


def _save_state(project: Path, state: dict) -> None:
    p = _reviews(project) / "state.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def hash_artifacts(project: Path, rels: list[str]) -> dict[str, str | None]:
    """Băm file; với thư mục thì băm toàn bộ file bên trong (theo đường dẫn tương đối)."""
    out = {}
    for rel in rels:
        p = project / rel
        if p.is_file():
            out[rel] = _sha(p)
        elif p.is_dir():
            h = hashlib.sha256()
            for f in sorted(x for x in p.rglob("*") if x.is_file()):
                h.update(str(f.relative_to(p)).encode())
                h.update(_sha(f).encode())
            out[rel] = "dir:" + h.hexdigest()
        else:
            out[rel] = None
    return out


def _read_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(p: Path, data: dict) -> None:
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------- start ----------

def start(project: Path, stage: str, checklist_dir: Path | None = None) -> Path:
    project = Path(project)
    st = stages.get(stage)
    prev = stages.previous(stage)
    if prev:
        g = gate(project, prev.code)
        if not g.ok:
            raise ReviewError(f"Chưa được duyệt '{stage}': công đoạn trước '{prev.code}' chưa qua cổng — {g.message}")
    cl = load_checklist(stage, checklist_dir)
    now = _now()
    rdir = _reviews(project) / stage / now.strftime("%Y%m%d-%H%M%S")
    n = 1
    while rdir.exists():
        n += 1
        rdir = rdir.with_name(now.strftime("%Y%m%d-%H%M%S") + f"-{n}")
    rdir.mkdir(parents=True)

    items = []
    for it in cl["items"]:
        rec = {k: it.get(k) for k in ("id", "group", "title", "severity", "method", "guidance", "allow_na")}
        rec.update(result=None, evidence=None, fix=None, reviewer=None)
        if it["method"] == "auto":
            r = run_check(it["check"], project, it.get("params"))
            rec.update(result=r.status, evidence=r.evidence, reviewer="auto", check=it["check"])
        items.append(rec)

    data = {
        "project": project.name, "stage": stage, "stage_name": st.name,
        "checklist_title": cl["title"], "checklist_version": cl["version"],
        "started_at": now.isoformat(timespec="seconds"), "finalized_at": None,
        "status": "pending", "artifacts": hash_artifacts(project, cl["artifacts"]),
        "items": items, "decision": None, "score": None,
    }
    _write_json(rdir / "review.json", data)
    _write_judgment_template(rdir / "judgments.yaml", items)

    state = _load_state(project)
    entry = state["stages"].setdefault(stage, {})
    old = entry.get("pending")
    if old and (project / old / "review.json").is_file():
        od = _read_json(project / old / "review.json")
        od["status"] = "abandoned"
        _write_json(project / old / "review.json", od)
    entry["pending"] = str(rdir.relative_to(project))
    _save_state(project, state)
    return rdir


def _write_judgment_template(path: Path, items: list[dict]) -> None:
    lines = [
        "# Phần chấm cho các mục phán đoán (method: ai).",
        "# verdict: pass | fail | na   — evidence bắt buộc (≥20 ký tự, trích dẫn/vị trí/số liệu)",
        "# fail bắt buộc có fix. na chỉ dùng khi mục cho phép (allow_na) và phải nêu lý do.",
        "# Không được chấm các mục auto.",
        "",
    ]
    for it in items:
        if it["method"] != "ai":
            continue
        lines.append(f"# [{SEV_LABEL[it['severity']]}] {it['title']}"
                     + ("  (được phép na)" if it.get("allow_na") else ""))
        for g in str(it.get("guidance") or "").strip().splitlines():
            lines.append(f"#   {g}")
        lines += [f"{it['id']}:", '  verdict: ""', '  evidence: ""', '  fix: ""', ""]
    path.write_text("\n".join(lines), encoding="utf-8")


# ---------- finalize ----------

def finalize(project: Path, stage: str, checklist_dir: Path | None = None, reviewer: str = "Claude") -> dict:
    project = Path(project)
    state = _load_state(project)
    pending = state["stages"].get(stage, {}).get("pending")
    if not pending:
        raise ReviewError(f"Công đoạn '{stage}' chưa có lần duyệt nào đang chờ. Chạy 'review start' trước.")
    rdir = project / pending
    data = _read_json(rdir / "review.json")
    jpath = rdir / "judgments.yaml"
    judgments = (yaml.safe_load(jpath.read_text(encoding="utf-8")) if jpath.is_file() else None) or {}

    errs = []
    now_hash = hash_artifacts(project, list(data["artifacts"]))
    changed = [k for k in data["artifacts"] if data["artifacts"][k] != now_hash[k]]
    if changed:
        errs.append("File sản phẩm đã thay đổi sau khi bắt đầu duyệt: " + ", ".join(changed)
                    + ". Phải chạy lại 'review start'.")

    by_id = {it["id"]: it for it in data["items"]}
    for jid in judgments:
        if jid not in by_id:
            errs.append(f"{jid}: không có trong checklist.")
        elif by_id[jid]["method"] == "auto":
            errs.append(f"{jid}: là mục tự động, không được chấm tay.")

    for it in data["items"]:
        if it["method"] != "ai":
            continue
        j = judgments.get(it["id"]) or {}
        verdict = str(j.get("verdict") or "").strip()
        evidence = str(j.get("evidence") or "").strip()
        fix = str(j.get("fix") or "").strip()
        if verdict not in ("pass", "fail", "na"):
            errs.append(f"{it['id']}: chưa chấm (verdict phải là pass/fail/na).")
            continue
        if len(evidence) < MIN_EVIDENCE:
            errs.append(f"{it['id']}: thiếu bằng chứng (evidence ≥ {MIN_EVIDENCE} ký tự).")
        if verdict == "fail" and len(fix) < MIN_FIX:
            errs.append(f"{it['id']}: trượt nhưng thiếu hướng sửa (fix ≥ {MIN_FIX} ký tự).")
        if verdict == "na" and not it.get("allow_na"):
            errs.append(f"{it['id']}: mục này không cho phép 'không áp dụng' (na).")
        it.update(result=verdict, evidence=evidence, fix=fix or None,
                  reviewer=str(j.get("reviewer") or reviewer))

    if errs:
        raise ReviewError("Chưa chốt được lần duyệt:\n- " + "\n- ".join(errs))

    blocking = [it for it in data["items"]
                if it["severity"] in ("chan", "nghiem_trong") and it["result"] in ("fail", "error")]
    applicable = [it for it in data["items"] if it["result"] != "na"]
    total = sum(WEIGHTS[it["severity"]] for it in applicable)
    passed = sum(WEIGHTS[it["severity"]] for it in applicable if it["result"] == "pass")
    data.update(
        status="finalized", finalized_at=_now().isoformat(timespec="seconds"),
        decision="KHONG_DAT" if blocking else "DAT",
        score=round(100 * passed / total) if total else 100,
    )
    _write_json(rdir / "review.json", data)
    (rdir / "report.md").write_text(render_report(data), encoding="utf-8")

    entry = state["stages"].setdefault(stage, {})
    entry["pending"] = None
    entry["latest"] = {"review": pending, "decision": data["decision"], "score": data["score"],
                       "artifacts": data["artifacts"], "finalized_at": data["finalized_at"], "override": None}
    _save_state(project, state)
    fails = [it["id"] for it in data["items"] if it["result"] in ("fail", "error")]
    _append_log(project, data["finalized_at"], stage, DECISION_LABEL[data["decision"]], data["score"],
                ", ".join(fails) or "—", f"{pending}/report.md")
    return {"decision": data["decision"], "score": data["score"], "report": rdir / "report.md",
            "blocking": [it["id"] for it in blocking]}


# ---------- báo cáo & nhật ký ----------

def _cell(s) -> str:
    return str(s or "").replace("|", "\\|").replace("\n", "<br>")


def render_report(d: dict) -> str:
    items = d["items"]
    blocking = [i for i in items if i["severity"] in ("chan", "nghiem_trong") and i["result"] in ("fail", "error")]
    minor = [i for i in items if i["severity"] == "nhe" and i["result"] in ("fail", "error")]
    counts = {k: sum(1 for i in items if i["result"] == k) for k in ("pass", "fail", "error", "na")}
    out = [
        f"# Báo cáo kiểm duyệt — {d['stage_name']}",
        "",
        f"- **Dự án:** {d['project']}",
        f"- **Công đoạn:** `{d['stage']}` · checklist \"{d['checklist_title']}\" v{d['checklist_version']}",
        f"- **Bắt đầu:** {d['started_at']} · **Chốt:** {d['finalized_at']}",
        "",
        f"## Kết luận: {DECISION_LABEL[d['decision']]} — điểm chất lượng {d['score']}/100",
        "",
        f"{len(items)} mục: {counts['pass']} đạt, {counts['fail']} trượt, "
        f"{counts['error']} lỗi kiểm tra, {counts['na']} không áp dụng.",
        "",
    ]
    if blocking:
        out += ["## ❗ Phải sửa trước khi đi tiếp", ""]
        for i in blocking:
            out += [f"### {i['id']} · [{SEV_LABEL[i['severity']]}] {i['title']}",
                    f"- **Hiện trạng:** {i['evidence']}",
                    f"- **Cách sửa:** {i['fix'] or 'Xem hiện trạng, sửa sản phẩm rồi duyệt lại.'}", ""]
    if minor:
        out += ["## Nên cải thiện (không chặn cổng)", ""]
        for i in minor:
            out += [f"- **{i['id']} {i['title']}:** {i['evidence']} → {i['fix'] or ''}"]
        out.append("")
    out += ["## File đã niêm phong", "", "| File | Mã băm |", "|---|---|"]
    for k, v in d["artifacts"].items():
        out.append(f"| `{k}` | `{(v or 'KHÔNG TỒN TẠI')[:16]}` |")
    out += ["", "## Toàn bộ checklist", "",
            "| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |", "|---|---|---|---|---|---|---|"]
    for i in items:
        out.append(f"| {i['id']} | {_cell(i['group'])} | {_cell(i['title'])} | {SEV_LABEL[i['severity']]} "
                   f"| {_cell(i['reviewer'])} | {RESULT_LABEL[i['result']]} | {_cell(i['evidence'])} |")
    out.append("")
    return "\n".join(out)


def _append_log(project: Path, when: str, stage: str, result: str, score, fails: str, link: str) -> None:
    """link: đường dẫn tính từ thư mục dự án; ghi vào LOG.md (nằm trong reviews/) dạng tương đối."""
    link = str(Path(link).relative_to("reviews"))
    p = _reviews(project) / "LOG.md"
    if not p.is_file():
        p.write_text(f"# Nhật ký kiểm duyệt — {project.name}\n\n"
                     "| Thời gian | Công đoạn | Kết quả | Điểm | Mục trượt | Báo cáo |\n"
                     "|---|---|---|---|---|---|\n", encoding="utf-8")
    with open(p, "a", encoding="utf-8") as f:
        f.write(f"| {when} | {stage} | {result} | {score} | {_cell(fails)} | [{link}]({link}) |\n")


# ---------- override & gate ----------

def override(project: Path, stage: str, by: str, reason: str) -> None:
    project = Path(project)
    if not (by or "").strip():
        raise ReviewError("Phải ghi tên người cho qua (--by).")
    if len((reason or "").strip()) < 10:
        raise ReviewError("Phải ghi lý do cho qua (≥ 10 ký tự).")
    state = _load_state(project)
    latest = state["stages"].get(stage, {}).get("latest")
    if not latest:
        raise ReviewError(f"Công đoạn '{stage}' chưa có lần duyệt nào đã chốt.")
    if latest["decision"] == "DAT":
        raise ReviewError(f"Công đoạn '{stage}' đã ĐẠT, không cần cho qua.")
    when = _now().isoformat(timespec="seconds")
    latest["override"] = {"by": by.strip(), "reason": reason.strip(), "at": when}
    _save_state(project, state)
    rep = project / latest["review"] / "report.md"
    with open(rep, "a", encoding="utf-8") as f:
        f.write(f"\n## ⚠️ CHO QUA CÓ GHI NHẬN\n\n- **Người cho qua:** {by}\n- **Lúc:** {when}\n- **Lý do:** {reason}\n")
    _append_log(project, when, stage, f"⚠️ **CHO QUA** bởi {_cell(by)}: {_cell(reason)}", latest["score"],
                "—", f"{latest['review']}/report.md")


def gate(project: Path, stage: str) -> GateStatus:
    project = Path(project)
    stages.get(stage)
    latest = _load_state(project)["stages"].get(stage, {}).get("latest")
    if not latest:
        return GateStatus(False, f"'{stage}' chưa được duyệt.")
    now = hash_artifacts(project, list(latest["artifacts"]))
    changed = [k for k, v in latest["artifacts"].items() if now[k] != v]
    if changed:
        return GateStatus(False, f"HẾT HIỆU LỰC — đã sửa sau lần duyệt {latest['finalized_at']}: "
                                 + ", ".join(changed) + ". Phải duyệt lại.")
    if latest["decision"] == "DAT":
        return GateStatus(True, f"ĐẠT ({latest['score']}/100) lúc {latest['finalized_at']}.")
    ov = latest.get("override")
    if ov:
        return GateStatus(True, f"CHO QUA CÓ GHI NHẬN bởi {ov['by']} lúc {ov['at']}: {ov['reason']}")
    return GateStatus(False, f"KHÔNG ĐẠT ({latest['score']}/100). Xem {latest['review']}/report.md")
