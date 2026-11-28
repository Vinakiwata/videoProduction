"""Tool 7 — Web trình chiếu 1920×1080: biên dịch timeline + storyboard + hình thành một trang tất định.
Xem docs/superpowers/specs/2026-11-28-tool-trinh-chieu-design.md."""
from __future__ import annotations

import base64
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

from vp import review
from vp.checks.files import load_yaml

DIR = "07_presentation"
WEB = Path(__file__).resolve().parent / "web"
TRANSITION_FRAMES = {"cut": 0, "match_cut": 0, "crossfade": 8, "push_up": 10, "push_left": 10, "push_right": 10,
                     "push_down": 10, "zoom_through": 10}
ELEMENT_LOOPS = {"bob", "pulse", "rotate", "wiggle", "shimmer", "blink_slow", "flow"}
FONT_EXT = (".ttf", ".otf", ".woff", ".woff2")


class PresentationError(RuntimeError):
    pass


def _sha_file(h, f: Path):
    h.update(f.name.encode())
    h.update(f.read_bytes() if f.is_file() else b"-")


def input_hash(project: Path) -> str:
    project = Path(project)
    h = hashlib.sha256()
    for rel in ("05_timeline/timeline.yaml", "02_design/storyboard.yaml", "06_animation/assets.yaml", "00_brief/brief.yaml"):
        _sha_file(h, project / rel)
    man = load_yaml(project, "06_animation/assets.yaml")
    for a in man.get("assets") or []:
        _sha_file(h, project / "06_animation" / a["file"])
    for v in load_yaml(project, "05_timeline/timeline.yaml").get("voice") or []:
        _sha_file(h, project / v["file"])
    return h.hexdigest()


def _default_ease(defaults: dict, event: str, anim: str) -> str | None:
    key = "slide" if anim.startswith("slide") else anim
    return (defaults.get(event) or {}).get(key)


def compile_presentation(project: Path) -> dict:
    """Quy mọi thứ ra khung: khung hình, phần tử, lượt vào/ra/lặp (đã chốt easing), camera, chuyển cảnh."""
    project = Path(project)
    tl = load_yaml(project, "05_timeline/timeline.yaml")
    sb = load_yaml(project, "02_design/storyboard.yaml")
    man = load_yaml(project, "06_animation/assets.yaml")
    defaults = man.get("motion_defaults") or {}
    amap = {a["id"]: a for a in man.get("assets") or []}
    sbs = {s["id"]: s for s in sb.get("shots") or []}
    cues: dict = {}
    for c in tl.get("cues") or []:
        cues.setdefault((c["shot"], c["element"]), []).append(c)
    shots = []
    for ts in tl["shots"]:
        s = sbs[ts["id"]]
        tr = ts.get("transition_in") or "cut"
        els = []
        for z, e in enumerate(s.get("elements") or []):
            el = {"id": e["id"], "z": z, "box": {k: float(v) for k, v in e["box"].items()}}
            if "asset" in e:
                a = amap.get(e["asset"]) or {}
                el.update(asset=e["asset"], file=a.get("file"), kind=a.get("kind"), layer_motion=bool(a.get("motion")))
            else:
                el.update(text=str(e["text"]), style=e.get("style", "label"), font_px=int(e.get("font_px", 48)), color=e.get("color"))
            for c in cues.get((ts["id"], e["id"]), []):
                if c["event"] == "loop":
                    el["loop"] = {"anim": c["anim"], "start": int(c["frame"]), "period": int(c.get("period_frames") or 45)}
                    continue
                sb_m = e.get(c["event"]) or {}
                ease = sb_m.get("ease") or _default_ease(defaults, c["event"], c["anim"]) or c.get("ease") or "ease_out"
                el[c["event"]] = {"anim": c["anim"], "start": int(c["frame"]), "dur": int(c.get("dur_frames") or 9), "ease": ease}
            els.append(el)
        shots.append({"id": ts["id"], "segment": ts.get("segment"), "start": int(ts["start_frame"]), "end": int(ts["end_frame"]),
                      "background": s.get("background", "#000000"), "camera": ts.get("camera") or {"move": "static"},
                      "transition": {"type": tr, "frames": TRANSITION_FRAMES.get(tr, 0) if shots else 0}, "elements": els})
    assets = {i: {"file": a["file"], "kind": a.get("kind"), "motion": a.get("motion") or []} for i, a in amap.items()}
    fonts = sb.get("fonts") or {}
    return {"version": 1, "canvas": {k: int(v) for k, v in sb["meta"]["canvas"].items()} | {"fps": int(tl["fps"])},
            "total_frames": int(tl["total_frames"]), "fonts": fonts, "text_plate": sb.get("text_plate"),
            "safe_area": 0.05, "shots": shots, "assets": assets, "input_hash": input_hash(project)}


def font_files(project: Path) -> tuple[list[Path], Path | None]:
    """File font của kênh: channels/<kênh>/brand/fonts/ (kèm OFL.txt)."""
    brief = load_yaml(Path(project), "00_brief/brief.yaml")
    ref = brief.get("channel_ref")
    d = Path(project).parents[1] / "channels" / str(ref) / "brand" / "fonts"
    if not d.is_dir():
        return [], None
    files = sorted(f for f in d.rglob("*") if f.suffix.lower() in FONT_EXT)
    lic = next((f for f in d.rglob("*") if f.name.upper().startswith("OFL")), None)
    return files, lic


def _font_css(files: list[Path], families: list[str]) -> str:
    """@font-face nhúng base64 (mở file:// vẫn chạy). Độ đậm suy từ tên file."""
    weights = {"thin": 100, "extralight": 200, "light": 300, "regular": 400, "medium": 500, "semibold": 600,
               "extrabold": 800, "bold": 700, "black": 900}
    css = []
    for f in files:
        stem = f.stem.lower().replace("-", "").replace("_", "")
        if "italic" in stem:
            continue
        w = 400
        for k in sorted(weights, key=len, reverse=True):
            if stem.endswith(k):
                w = weights[k]
                break
        fmt = {".ttf": "truetype", ".otf": "opentype", ".woff": "woff", ".woff2": "woff2"}[f.suffix.lower()]
        data = base64.b64encode(f.read_bytes()).decode()
        for fam in families:
            css.append(f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:normal;"
                       f"src:url(data:font/{f.suffix[1:].lower()};base64,{data}) format('{fmt}');}}")
    return "\n".join(css)


def _voice_track(project: Path, tl: dict, out: Path) -> None:
    """Giọng đặt đúng khung của timeline (để xem thử có tiếng khớp hình)."""
    fps = float(tl["fps"])
    vs = tl.get("voice") or []
    out.parent.mkdir(parents=True, exist_ok=True)
    if not vs:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t",
                        str(tl["total_s"]), str(out)], check=True)
        return
    args, flt = [], []
    for i, v in enumerate(vs):
        args += ["-i", str(project / v["file"])]
        flt.append(f"[{i}:a]adelay={int(round(v['start_frame'] / fps * 1000))}:all=1[a{i}]")
    flt.append("".join(f"[a{i}]" for i in range(len(vs))) +
               f"amix=inputs={len(vs)}:normalize=0,apad=whole_dur={tl['total_frames'] / fps:.3f}[m]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args, "-filter_complex", ";".join(flt), "-map", "[m]",
                    "-ar", "48000", "-ac", "1", str(out)], check=True)


def build(project: Path) -> Path:
    project = Path(project)
    g = review.gate(project, "animation")
    if not g.ok:
        raise PresentationError(f"Cổng 'animation' chưa mở: {g.message}")
    comp = compile_presentation(project)
    d = project / DIR
    if (d / "assets").exists():
        shutil.rmtree(d / "assets")
    (d / "assets").mkdir(parents=True, exist_ok=True)
    svgs = {}
    for i, a in comp["assets"].items():
        src = project / "06_animation" / a["file"]
        shutil.copyfile(src, d / a["file"])
        if src.suffix.lower() == ".svg":
            svgs[i] = src.read_text(encoding="utf-8")
    tl = load_yaml(project, "05_timeline/timeline.yaml")
    _voice_track(project, tl, d / "audio" / "voice.wav")
    files, lic = font_files(project)
    fams = sorted({v for v in (comp.get("fonts") or {}).values() if v})
    if (d / "fonts").exists():
        shutil.rmtree(d / "fonts")
    if files:
        (d / "fonts").mkdir(parents=True)
        for f in files:
            shutil.copyfile(f, d / "fonts" / f.name)
        if lic:
            shutil.copyfile(lic, d / "fonts" / lic.name)
    comp["font_files"] = [f.name for f in files]
    (d / "presentation.json").write_text(json.dumps(comp, ensure_ascii=False, indent=1), encoding="utf-8")
    (d / "data.js").write_text("window.VP_DATA = " + json.dumps(comp, ensure_ascii=False) + ";\nwindow.VP_SVG = " +
                               json.dumps(svgs, ensure_ascii=False) + ";\n", encoding="utf-8")
    (d / "fonts.css").write_text(_font_css(files, fams), encoding="utf-8")
    for f in ("player.js", "player.css", "index.html"):
        shutil.copyfile(WEB / f, d / f)
    return d / "index.html"


# ---------------- kiểm tự động bằng Chrome chạy ngầm ----------------
CAPTURE = Path(__file__).resolve().parent / "js" / "capture.mjs"
RECIPES = {"bob", "rotate", "twinkle", "pulse_opacity", "dashflow", "rise", "fall", "along"}
CHECK_DIR = "check"


def build_hash(project: Path) -> str:
    """Băm bản dựng (mọi file trong 07_presentation trừ thư mục check/)."""
    d = Path(project) / DIR
    h = hashlib.sha256()
    for f in sorted(x for x in d.rglob("*") if x.is_file() and CHECK_DIR not in x.relative_to(d).parts[:1]):
        h.update(str(f.relative_to(d)).encode())
        h.update(hashlib.sha256(f.read_bytes()).digest())
    return h.hexdigest()


def key_frames(comp: dict) -> list[dict]:
    """Khung mốc: đầu, giữa, cuối mỗi khung hình và giữa mỗi lượt chuyển cảnh."""
    out = {}
    for s in comp["shots"]:
        a, b = s["start"], s["end"] - 1
        out.setdefault(a, "start")
        tr = (s.get("transition") or {}).get("frames") or 0
        if tr:
            out[a + tr // 2] = "transition"
            out.setdefault(min(b, a + tr), "settled")
        out[(a + b) // 2] = "mid"
        out.setdefault(b, "end")
    return [{"frame": f, "role": r} for f, r in sorted(out.items())]


def _run_capture(index: Path, frames: list[int], out_dir: Path, measure: bool) -> dict:
    spec = {"url": index.resolve().as_uri() + "?render=1", "out_dir": str(out_dir), "frames": frames,
            "width": 1920, "height": 1080, "measure": measure, "chrome": shutil.which("google-chrome") or "google-chrome"}
    sp = out_dir.parent / (out_dir.name + ".spec.json")
    sp.write_text(json.dumps(spec), encoding="utf-8")
    r = subprocess.run(["node", str(CAPTURE), str(sp)], capture_output=True, text=True, timeout=1800)
    sp.unlink()
    if r.returncode != 0:
        raise PresentationError("Chụp khung lỗi:\n" + (r.stderr or r.stdout)[-3000:])
    return json.loads(r.stdout)


def _pixels(png: Path):
    from PIL import Image, ImageStat
    im = Image.open(png).convert("RGB")
    st = ImageStat.Stat(im)
    return im, hashlib.sha256(im.tobytes()).hexdigest(), max(st.stddev), max(st.extrema[i][1] for i in range(3))


def check(project: Path) -> Path:
    """Chụp các khung mốc hai lượt (xuôi rồi ngược) để đo lỗi JS, chữ tràn, khung trống và tính tất định."""
    import tempfile
    project = Path(project)
    d = project / DIR
    if not (d / "index.html").is_file():
        raise PresentationError("Chưa có bản dựng. Chạy: python -m vp presentation build <dự án>")
    comp = json.loads((d / "presentation.json").read_text(encoding="utf-8"))
    keys = key_frames(comp)
    frames = [k["frame"] for k in keys]
    cdir = d / CHECK_DIR
    if cdir.exists():
        shutil.rmtree(cdir)
    cdir.mkdir()
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        fwd = _run_capture(d / "index.html", frames, tmp / "xuoi", measure=True)
        rev = _run_capture(d / "index.html", frames[::-1], tmp / "nguoc", measure=False)
        rev_hash = {}
        for r in rev["frames"]:
            rev_hash[r["frame"]] = _pixels(Path(r["file"]))[1]
        rows, mism = [], []
        for k, r in zip(keys, fwd["frames"]):
            im, hx, sd, mx = _pixels(Path(r["file"]))
            name = f"f{r['frame']:05d}.jpg"
            im.resize((960, 540)).save(cdir / name, quality=85)
            if rev_hash.get(r["frame"]) != hx:
                mism.append(r["frame"])
            rows.append({"frame": r["frame"], "role": k["role"], "shot": r["shot"], "file": f"{CHECK_DIR}/{name}",
                         "size": list(im.size), "sha256": hx, "stddev": round(sd, 2), "max": mx, "issues": r["issues"]})
    man = {"build_hash": build_hash(project), "input_hash": comp.get("input_hash"), "frames": rows,
           "errors": fwd["errors"] + [e for e in rev["errors"] if e not in fwd["errors"]],
           "console": fwd["console"] + rev["console"], "fonts": fwd.get("fonts", []),
           "determinism": {"checked": len(frames), "order": "xuôi rồi ngược", "mismatch": mism}}
    (cdir / "check_manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    return cdir / "check_manifest.json"


def preview(project: Path) -> Path:
    """Tờ ảnh các khung mốc (contact.png) cho người duyệt, kèm số khung và mã khung hình."""
    from PIL import Image, ImageDraw, ImageFont
    project = Path(project)
    d = project / DIR
    mp = d / CHECK_DIR / "check_manifest.json"
    if not mp.is_file():
        raise PresentationError("Chưa có tờ kiểm. Chạy: python -m vp presentation check <dự án>")
    man = json.loads(mp.read_text(encoding="utf-8"))
    rows = man["frames"]
    cols, W, H, cap = 5, 384, 216, 26
    sheet = Image.new("RGB", (cols * W, ((len(rows) + cols - 1) // cols) * (H + cap)), "#1d1f24")
    dr = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 15)
    except OSError:
        font = ImageFont.load_default()
    fps = 30
    try:
        fps = json.loads((d / "presentation.json").read_text(encoding="utf-8"))["canvas"]["fps"]
    except (KeyError, OSError):
        pass
    for i, r in enumerate(rows):
        x, y = (i % cols) * W, (i // cols) * (H + cap)
        sheet.paste(Image.open(d / r["file"]).resize((W, H)), (x, y))
        dr.text((x + 6, y + H + 4), f"{r['frame']} · {r['frame'] / fps:.2f}s · {r['shot']} · {r['role']}", fill="#e8e8ea", font=font)
    out = d / CHECK_DIR / "contact.png"
    sheet.save(out)
    man["contact_build_hash"] = man["build_hash"]
    mp.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


def lint(project: Path, checklist_dir: Path | None = None):
    from vp.checklist import load_checklist
    from vp.checks import run_check
    cl = load_checklist("presentation", checklist_dir)
    return [(it, run_check(it["check"], Path(project), it.get("params")))
            for it in cl["items"] if it["method"] == "auto"]
