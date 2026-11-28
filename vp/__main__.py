"""Dòng lệnh: python -m vp <lệnh> ...

  new <thư-mục-dự-án> --title "..."          tạo khung dự án
  review start <dự án> <công đoạn>             chạy mục tự động, tạo phiếu chấm
  review finalize <dự án> <công đoạn>          kiểm phần chấm, ra quyết định, ghi báo cáo
  review override <dự án> <công đoạn> --by TÊN --reason "..."
  gate <dự án> <công đoạn>                     mã thoát 0 nếu cổng đang mở
  status <dự án>                               trạng thái cổng của mọi công đoạn
  brief new <dự án> --channel KÊNH --title "..." [--goal ..] [--audience ..] [--duration N] [--ads/--no-ads]
  script import <dự án> <bản-thảo.md> [--force]   nhập bản thảo thành script.yaml
  script estimate <dự án> [--sps N]            tính lại thời lượng theo âm tiết
  script view <dự án>                          ghi bản đọc 01_script/script.md
  script lint <dự án>                          kiểm nhanh các mục tự động (không ghi nhật ký)
  design init|view|preview|lint <dự án>        Tool 3: storyboard, bản đọc, ảnh phác thảo, kiểm nhanh
  voice synth <dự án> [--engine vieneu|recording] [--takes N] [--only S01-01,..]   tạo/nhập giọng, đo, manifest
  voice calibrate <dự án> [--apply] · voice to-animatic <dự án>
  animation init|sync|preview|lint <dự án>     Tool 6: danh mục hình (SVG + linh vật PNG), tờ xem trước, kiểm nhanh
  presentation build|check|preview|lint <dự án>  Tool 7: trang trình chiếu tất định, chụp kiểm bằng Chrome, tờ khung mốc
  render build|lint <dự án>                   Tool 8: chụp trang trình chiếu từng khung → video_silent.mp4 (+ bản xem nhanh có giọng)
  timeline build <dự án> [--breath 0.6 --breath-scene 0.9]        khoá thời gian theo khung + phụ đề
  animatic build <dự án> [--fps 15]            animatic: khung theo mốc thời gian + phụ đề + tiếng động nháp
"""
import argparse
import json
import sys
from pathlib import Path

import yaml

from vp import brief as brief_tool
from vp import platforms
from vp import animatic, animation_tools, design_tools, presentation_tools, render_tools, review, script_tools, stages, timeline, voice
from vp.project import create_project
from vp.checklist import ChecklistError


def cmd_new(a):
    p = Path(a.project)
    if p.exists() and any(p.iterdir()):
        sys.exit(f"Thư mục {p} đã có dữ liệu.")
    create_project(p, a.title)
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


def cmd_brief(a):
    path = brief_tool.new_brief(Path(a.project), channel=a.channel, title=a.title, goal=a.goal,
                                audience=a.audience, duration=a.duration, ads=a.ads, force=a.force)
    print(f"Đã tạo {path}")
    b = yaml.safe_load(path.read_text(encoding="utf-8"))
    for x in b.get("assumptions") or []:
        print(f"  • giả định: {x}")
    todo = [k for k, v in b.items() if isinstance(v, str) and v.startswith("TODO")]
    if todo:
        print("Còn phải điền: " + ", ".join(todo))


def cmd_script(a):
    p = Path(a.project)
    if a.action == "import":
        if not a.src:
            sys.exit("Thiếu đường dẫn bản thảo: python -m vp script import <dự án> <file>")
        print(f"Đã nhập bản thảo -> {script_tools.import_draft(p, Path(a.src), force=a.force, sps=a.sps)}")
    elif a.action == "estimate":
        n = script_tools.estimate(p, sps=a.sps)
        print(f"Đã ước lượng lại {n} đoạn giọng ở {script_tools.resolve_sps(p, a.sps)} âm tiết/giây.")
    elif a.action == "view":
        print(f"Đã ghi {script_tools.view(p)}")
    elif a.action == "lint":
        results = script_tools.lint(p)
        bad = 0
        for it, r in results:
            bad += r.status != "pass"
            print(f"[{r.status:>5}] {it['id']} {it['title']}")
            if r.status != "pass":
                print("        " + r.evidence.replace("\n", "\n        "))
        print("Kiểm nhanh: " + ("SẠCH" if not bad else f"{bad} mục cần sửa"))
        sys.exit(1 if bad else 0)


def _print_lint(results):
    bad = 0
    for it, r in results:
        bad += r.status != "pass"
        print(f"[{r.status:>5}] {it['id']} {it['title']}")
        if r.status != "pass":
            print("        " + r.evidence.replace("\n", "\n        "))
    print("Kiểm nhanh: " + ("SẠCH" if not bad else f"{bad} mục cần sửa"))
    sys.exit(1 if bad else 0)


def cmd_design(a):
    p = Path(a.project)
    if a.action == "init":
        print(f"Đã tạo khung storyboard -> {design_tools.init(p, force=a.force)}")
    elif a.action == "view":
        print(f"Đã ghi {design_tools.view(p)}")
    elif a.action == "preview":
        print(f"Đã vẽ ảnh phác thảo -> {design_tools.preview(p)}")
    elif a.action == "lint":
        _print_lint(design_tools.lint(p))


def cmd_animatic(a):
    out = animatic.build(Path(a.project), fps=a.fps, check_gate=True)
    import json as _j
    man = _j.loads((Path(a.project) / "03_animatic" / "manifest.json").read_text(encoding="utf-8"))
    print(f"Đã dựng {out} — {man['total_s']:.1f}s, nguồn lời: {man['voice_source']}")


def cmd_voice(a):
    p = Path(a.project)
    if a.action == "synth":
        if a.engine == "vieneu":
            eng = voice.VieneuEngine()
        else:
            eng = voice.RecordingEngine(p, name=a.source_name or "recording")
        only = set(a.only.split(",")) if a.only else None
        man = voice.synth_all(p, eng, takes=a.takes or (2 if a.engine == "vieneu" else 1), only=only, tempo=a.tempo,
                               pause_sentence=a.pause_sentence, pause_question=a.pause_question, even_speed=a.even_speed)
        for e in man["segments"]:
            print(f"  {e['id']}: {e['duration_s']:.2f}s, {e['sps']} âm tiết/giây, lặng giữa câu {e['max_gap_s']}s")
        print(f"Tổng {man['total_s']:.1f}s; tốc độ trung vị {man['measured_sps_median']} âm tiết/giây ({man['engine']}, {man['voice']})")
    elif a.action == "calibrate":
        r = voice.calibrate(p, apply=a.apply)
        print(f"Tốc độ đọc đo được: {r['measured_sps']} âm tiết/giây" + (f" → đã ghi vào {r['applied_to']}" if r["applied_to"] else " (thêm --apply để ghi vào hồ sơ kênh)"))
    elif a.action == "sheet":
        print(f"Đã ghi phiếu thu âm {voice.recording_sheet(p)}")
    elif a.action == "to-animatic":
        print(f"Đã chép {voice.to_animatic(p)} đoạn giọng sang 03_animatic/scratch_voice — dựng lại animatic và duyệt lại nhịp.")


def cmd_timeline(a):
    out = timeline.build(Path(a.project), breath=a.breath, breath_scene=a.breath_scene, question_extra=a.question_extra)
    import yaml as _y
    t = _y.safe_load(out.read_text(encoding="utf-8"))
    print(f"Đã khoá timeline {out}: {t['total_frames']} khung = {t['total_s']}s @ {t['fps']:g} fps, "
          f"{len(t['shots'])} khung hình, {len(t['cues'])} cue, {len(t['sfx'])} SFX; phụ đề 05_timeline/subtitles.srt")


def cmd_render(a):
    p = Path(a.project)
    if a.action == "build":
        out = render_tools.build(p)
        print(f"Đã render {out} — {json.loads((p / render_tools.DIR / 'manifest.json').read_text(encoding='utf-8'))['seconds']} giây")
    else:
        _print_lint(render_tools.lint(p))


def cmd_presentation(a):
    p = Path(a.project)
    if a.action == "build":
        print(f"Đã dựng trang trình chiếu {presentation_tools.build(p)}")
    elif a.action == "check":
        print(f"Đã chụp kiểm {presentation_tools.check(p)}")
    elif a.action == "preview":
        print(f"Đã dựng tờ khung mốc {presentation_tools.preview(p)}")
    else:
        _print_lint(presentation_tools.lint(p))


def cmd_animation(a):
    p = Path(a.project)
    if a.action == "init":
        print(f"Đã tạo danh mục hình {animation_tools.init(p, force=a.force)}")
    elif a.action == "sync":
        print(f"Đã khớp danh mục hình với storyboard {animation_tools.sync(p)}")
    elif a.action == "preview":
        print(f"Đã dựng tờ xem trước {animation_tools.preview(p)}")
    elif a.action == "lint":
        _print_lint(animation_tools.lint(p))


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
    b = sub.add_parser("brief"); b.add_argument("action", choices=["new"]); b.add_argument("project")
    b.add_argument("--channel", required=True); b.add_argument("--title", required=True)
    b.add_argument("--goal"); b.add_argument("--audience"); b.add_argument("--duration", type=float)
    b.add_argument("--ads", action=argparse.BooleanOptionalAction, default=None); b.add_argument("--force", action="store_true")
    b.set_defaults(fn=cmd_brief)
    sc = sub.add_parser("script"); sc.add_argument("action", choices=["import", "estimate", "view", "lint"])
    sc.add_argument("project"); sc.add_argument("src", nargs="?"); sc.add_argument("--sps", type=float)
    sc.add_argument("--force", action="store_true"); sc.set_defaults(fn=cmd_script)
    dz = sub.add_parser("design"); dz.add_argument("action", choices=["init", "view", "preview", "lint"])
    dz.add_argument("project"); dz.add_argument("--force", action="store_true"); dz.set_defaults(fn=cmd_design)
    am = sub.add_parser("animatic"); am.add_argument("action", choices=["build"]); am.add_argument("project")
    am.add_argument("--fps", type=int, default=15); am.set_defaults(fn=cmd_animatic)
    vo = sub.add_parser("voice"); vo.add_argument("action", choices=["synth", "calibrate", "to-animatic", "sheet"])
    vo.add_argument("project"); vo.add_argument("--engine", choices=["vieneu", "recording"], default="vieneu")
    vo.add_argument("--takes", type=int); vo.add_argument("--only"); vo.add_argument("--apply", action="store_true")
    vo.add_argument("--tempo", type=float, default=1.0, help="<1 làm chậm giọng, giữ cao độ (vd. 0.9)")
    vo.add_argument("--pause-sentence", type=float, default=0.45, help="khoảng ngắt sau câu kết thúc bằng dấu chấm (giây)")
    vo.add_argument("--pause-question", type=float, default=0.55, help="khoảng ngắt sau câu hỏi/cảm thán (giây)")
    vo.add_argument("--even-speed", type=float, default=0.12,
                    help="cân tốc độ: đoạn lệch quá ±tỉ lệ này so với trung vị được chỉnh nhẹ (tối đa ±10%%, giữ cao độ); 0 = tắt")
    vo.add_argument("--source-name", help="Tên nguồn ghi vào manifest khi dùng file có sẵn (vd. vieneu-mac)")
    vo.set_defaults(fn=cmd_voice)
    tlp = sub.add_parser("timeline"); tlp.add_argument("action", choices=["build"]); tlp.add_argument("project")
    tlp.add_argument("--breath", type=float, default=0.60, help="ngắt giữa hai đoạn cùng cảnh (giây)")
    tlp.add_argument("--breath-scene", type=float, default=0.90, help="ngắt khi sang cảnh mới (giây)")
    tlp.add_argument("--question-extra", type=float, default=0.10, help="cộng thêm sau câu hỏi/cảm thán (giây)")
    tlp.set_defaults(fn=cmd_timeline)
    an = sub.add_parser("animation"); an.add_argument("action", choices=["init", "sync", "preview", "lint"])
    an.add_argument("project"); an.add_argument("--force", action="store_true"); an.set_defaults(fn=cmd_animation)
    pr = sub.add_parser("presentation"); pr.add_argument("action", choices=["build", "check", "preview", "lint"])
    pr.add_argument("project"); pr.set_defaults(fn=cmd_presentation)
    rn = sub.add_parser("render"); rn.add_argument("action", choices=["build", "lint"])
    rn.add_argument("project"); rn.set_defaults(fn=cmd_render)
    s = sub.add_parser("status"); s.add_argument("project"); s.set_defaults(fn=cmd_status)
    a = ap.parse_args(argv)
    try:
        a.fn(a)
    except (review.ReviewError, ChecklistError, brief_tool.BriefError, script_tools.ScriptToolError,
            design_tools.DesignToolError, animatic.AnimaticError, voice.VoiceError, timeline.TimelineError,
            animation_tools.AnimationToolError, presentation_tools.PresentationError, platforms.PlatformError,
            render_tools.RenderError) as e:
        sys.exit(f"LỖI: {e}")


if __name__ == "__main__":
    main()
