"""Kiểm tra tự động cho storyboard (02_design/storyboard.yaml)."""
from collections import defaultdict
from pathlib import Path

from vp.checks import CheckResult, register
from vp.checks.files import load_yaml
from vp.checks.script import segments as script_segments

EPS = 1e-3


def _fmt(bad, head):
    return CheckResult("fail", head + "\n" + "\n".join(f"- {b}" for b in bad[:30])
                       + (f"\n… và {len(bad) - 30} mục khác" if len(bad) > 30 else ""))


def _mmss(t):
    m, s = divmod(t, 60)
    return f"{int(m):02d}:{s:04.1f}"


class Ctx:
    """Nạp storyboard + kịch bản, tính thời lượng và mốc tuyệt đối của từng khung."""

    def __init__(self, project: Path, params: dict):
        self.sb = load_yaml(project, params["path"])
        self.script = load_yaml(project, params.get("script", "01_script/script.yaml"))
        self.seg = {}
        self.seg_start = {}
        t = 0.0
        for _, s in script_segments(self.script):
            self.seg[s["id"]] = s
            self.seg_start[s["id"]] = t
            t += float(s.get("est_duration_s") or 0)
        self.total = t

    def shot_dur(self, shot):
        seg = self.seg.get(shot["segment"])
        if not seg:
            return 0.0
        a, b = shot["span"]
        return float(seg.get("est_duration_s") or 0) * (b - a)

    def shot_start(self, shot):
        seg = self.seg.get(shot["segment"])
        if not seg:
            return 0.0
        return self.seg_start[shot["segment"]] + float(seg.get("est_duration_s") or 0) * shot["span"][0]

    def texts(self):
        for sh in self.sb.get("shots") or []:
            for e in sh.get("elements") or []:
                if "text" in e:
                    yield sh, e


@register("storyboard_coverage")
def coverage(project: Path, params: dict) -> CheckResult:
    c = Ctx(project, params)
    by = defaultdict(list)
    bad = []
    for sh in c.sb.get("shots") or []:
        if sh["segment"] not in c.seg:
            bad.append(f"{sh['id']}: trỏ tới đoạn {sh['segment']} không có trong kịch bản")
            continue
        a, b = sh["span"]
        if not a < b:
            bad.append(f"{sh['id']}: span {sh['span']} không hợp lệ (đầu phải nhỏ hơn cuối)")
        by[sh["segment"]].append(sh)
    for sid in c.seg:
        shots = sorted(by.get(sid, []), key=lambda s: s["span"][0])
        if not shots:
            bad.append(f"{sid}: chưa có khung hình nào")
            continue
        if shots[0]["span"][0] > EPS:
            bad.append(f"{sid}: hở từ 0 tới {shots[0]['span'][0]} (khung đầu {shots[0]['id']})")
        if shots[-1]["span"][1] < 1 - EPS:
            bad.append(f"{sid}: hở từ {shots[-1]['span'][1]} tới 1 (khung cuối {shots[-1]['id']})")
        for p, n in zip(shots, shots[1:]):
            d = n["span"][0] - p["span"][1]
            if d > EPS:
                bad.append(f"{sid}: hở giữa {p['id']} và {n['id']} ({p['span'][1]} → {n['span'][0]})")
            elif d < -EPS:
                bad.append(f"{sid}: chồng giữa {p['id']} và {n['id']} ({p['span'][1]} > {n['span'][0]})")
    if bad:
        return _fmt(bad, "Độ phủ storyboard so với kịch bản bị lỗi:")
    n = len(c.sb.get("shots") or [])
    return CheckResult("pass", f"{len(c.seg)} đoạn kịch bản đều được phủ kín bởi {n} khung hình.")


@register("storyboard_refs")
def refs(project: Path, params: dict) -> CheckResult:
    sb = load_yaml(project, params["path"])
    bad = []
    assets = [a["id"] for a in sb.get("assets") or []]
    dup_a = {a for a in assets if assets.count(a) > 1}
    bad += [f"asset {a}: trùng mã" for a in sorted(dup_a)]
    aset, used = set(assets), set()
    seen = set()
    for sh in sb.get("shots") or []:
        if sh["id"] in seen:
            bad.append(f"{sh['id']}: trùng mã khung")
        seen.add(sh["id"])
        if not sh["id"].startswith(sh["segment"] + "-"):
            bad.append(f"{sh['id']}: mã khung không khớp đoạn {sh['segment']}")
        eids = [e["id"] for e in sh.get("elements") or []]
        bad += [f"{sh['id']}: trùng mã phần tử {e}" for e in sorted({x for x in eids if eids.count(x) > 1})]
        for e in sh.get("elements") or []:
            if "asset" in e:
                used.add(e["asset"])
                if e["asset"] not in aset:
                    bad.append(f"{sh['id']}/{e['id']}: asset {e['asset']} không có trong thư viện")
        if sh.get("focal") not in eids:
            bad.append(f"{sh['id']}: focal {sh.get('focal')} không phải phần tử của khung")
        for fx in sh.get("sfx") or []:
            if fx["target"] not in eids:
                bad.append(f"{sh['id']}: sfx '{fx['name']}' gắn với {fx['target']} không có trong khung")
    if bad:
        return _fmt(bad, "Tham chiếu trong storyboard bị hỏng:")
    unused = sorted(aset - used)
    note = f" Asset chưa dùng: {', '.join(unused)}." if unused else ""
    return CheckResult("pass", f"{len(seen)} khung, {len(aset)} asset, mọi tham chiếu hợp lệ.{note}")


@register("storyboard_palette")
def palette(project: Path, params: dict) -> CheckResult:
    """Chữ, nền, icon, nút: chỉ màu nhận diện. Asset kind=scene: thêm bảng màu tự nhiên (brand.scene_colors)."""
    sb = load_yaml(project, params["path"])
    brief = load_yaml(project, params.get("brief", "00_brief/brief.yaml"))
    brand = {c.upper() for c in brief["brand"]["colors"]}
    scene_brand = {c.upper() for c in brief["brand"].get("scene_colors") or []}
    pal = {c.upper() for c in sb.get("palette") or []}
    spal = {c.upper() for c in sb.get("scene_palette") or []}
    bad = [f"palette có {c} không thuộc brand.colors của brief" for c in sorted(pal - brand)]
    bad += [f"scene_palette có {c} không thuộc brand.scene_colors của brief" for c in sorted(spal - scene_brand)]
    for a in sb.get("assets") or []:
        if a.get("kind") == "mascot":
            continue                      # linh vật là ảnh của bộ nhận diện, màu đã chốt ở brand.mascot
        ok = pal | spal if a.get("kind") == "scene" else pal
        where = "bảng màu cảnh" if a.get("kind") == "scene" else "màu nhận diện (chỉ asset kind=scene mới được dùng màu cảnh)"
        bad += [f"asset {a['id']}: màu {c} ngoài {where}" for c in a.get("colors") or [] if c.upper() not in ok]
    tp = sb.get("text_plate")
    if tp and tp["color"].upper() not in pal:
        bad.append(f"text_plate: màu {tp['color']}")
    for sh in sb.get("shots") or []:
        if sh["background"].upper() not in pal:
            bad.append(f"{sh['id']}: nền {sh['background']}")
        for e in sh.get("elements") or []:
            if e.get("color") and e["color"].upper() not in pal:
                bad.append(f"{sh['id']}/{e['id']}: màu chữ {e['color']}")
    if bad:
        return _fmt(bad, f"Màu ngoài bảng màu nhận diện {sorted(pal)} / bảng màu cảnh {sorted(spal)}:")
    extra = f", cảnh dùng thêm {len(spal)} màu tự nhiên" if spal else ""
    return CheckResult("pass", f"Mọi màu thuộc bảng màu nhận diện ({len(pal)} màu{extra}).")


def _overflow(e, canvas) -> str | None:
    """Đo chữ bằng font thật (DejaVu Sans, hơi rộng hơn font tiêu đề thông dụng) ở kích thước khung thật."""
    from PIL import ImageFont
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
                                  if e["style"] == "title" else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                                  e["font_px"])
    except OSError:
        return None
    bw = canvas["width"] * e["box"]["w"] / 100
    bh = canvas["height"] * e["box"]["h"] / 100
    lines = 0
    for para in e["text"].split("\n"):
        cur = ""
        n = 1
        for w in para.split():
            if font.getlength(w) > bw:
                return f"từ \"{w}\" rộng {font.getlength(w):.0f}px > hộp {bw:.0f}px"
            t = f"{cur} {w}".strip()
            if cur and font.getlength(t) > bw:
                n += 1
                cur = w
            else:
                cur = t
        lines += n
    need = lines * e["font_px"] * 1.15
    if need > bh + 1:
        return f"cần {lines} dòng ≈ {need:.0f}px nhưng hộp cao {bh:.0f}px"
    return None


@register("storyboard_text")
def text(project: Path, params: dict) -> CheckResult:
    """Chữ giống hệt nhau, không có exit, nối tiếp qua các khung liền nhau được tính là một lần hiển thị."""
    c = Ctx(project, params)
    min_px, min_title = int(params.get("min_px", 48)), int(params.get("min_title_px", 72))
    max_w = int(params.get("max_words_per_line", 7))
    spw, base = float(params.get("s_per_word", 0.3)), float(params.get("base_s", 1.0))
    order = sorted(c.sb.get("shots") or [], key=c.shot_start)

    def text_el(sh, txt):
        return next((e for e in sh.get("elements") or [] if e.get("text") == txt), None)

    bad, n = [], 0
    for i, sh in enumerate(order):
        for e in sh.get("elements") or []:
            if "text" not in e:
                continue
            n += 1
            where = f"{sh['id']}/{e['id']}"
            need_px = min_title if e["style"] == "title" else min_px
            if e["font_px"] < need_px:
                bad.append(f"{where}: cỡ chữ {e['font_px']}px < {need_px}px ({e['style']})")
            lines = e["text"].split("\n")
            for ln in lines:
                w = len(ln.split())
                if w > max_w:
                    bad.append(f"{where}: dòng \"{ln[:40]}\" có {w} từ > {max_w}")
            over = _overflow(e, c.sb["meta"]["canvas"])
            if over:
                bad.append(f"{where}: chữ tràn hộp — {over}")
            prev = text_el(order[i - 1], e["text"]) if i > 0 else None
            if prev and not prev.get("exit") and not (e.get("enter") or {}).get("at", 0):
                continue  # phần nối tiếp của chữ đã xét ở khung trước
            words = sum(len(ln.split()) for ln in lines)
            a = (e.get("enter") or {}).get("at", 0)
            cur, j = e, i
            vis = c.shot_dur(sh) * max(0.0, (cur.get("exit") or {}).get("at", 1) - a)
            while not cur.get("exit") and j + 1 < len(order):
                nxt = text_el(order[j + 1], e["text"])
                if not nxt or (nxt.get("enter") or {}).get("at", 0):
                    break
                cur, j = nxt, j + 1
                vis += c.shot_dur(order[j]) * (cur.get("exit") or {}).get("at", 1)
            need = spw * words + base
            if vis + EPS < need:
                bad.append(f"{where}: {words} từ hiện {vis:.1f}s, cần ≥ {need:.1f}s")
    if bad:
        return _fmt(bad, "Chữ trên màn hình khó đọc:")
    return CheckResult("pass", f"{n} phần tử chữ: đủ cỡ, ≤ {max_w} từ/dòng, đủ thời gian đọc.")


def _lum(hexc: str) -> float:
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (int(hexc[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast_ratio(a: str, b: str) -> float:
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def _blend(top: str, under: str, opacity: float) -> str:
    t = [int(top[i:i + 2], 16) for i in (1, 3, 5)]
    u = [int(under[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(opacity * a + (1 - opacity) * b):02X}" for a, b in zip(t, u))


@register("storyboard_contrast")
def contrast(project: Path, params: dict) -> CheckResult:
    """Chữ trên nền khung; nếu khung có cảnh minh hoạ (kind=scene) thì tính với MỌI màu của cảnh
    (trường hợp xấu nhất), qua tấm nền text_plate nếu có."""
    sb = load_yaml(project, params["path"])
    mn = float(params.get("min_ratio", 4.5))
    kinds = {a["id"]: a for a in sb.get("assets") or []}
    tp = sb.get("text_plate")
    bad, worst, n = [], None, 0
    for sh in sb.get("shots") or []:
        scene = sorted({c.upper() for e in sh.get("elements") or [] if e.get("asset")
                        for c in (kinds.get(e["asset"], {}).get("colors") or [])
                        if kinds.get(e["asset"], {}).get("kind") == "scene"})
        for e in sh.get("elements") or []:
            if "text" not in e:
                continue
            n += 1
            if scene:
                cands = [(c, _blend(tp["color"], c, tp["opacity"]) if tp else c) for c in scene]
            elif tp and tp.get("always"):
                cands = [(sh["background"], _blend(tp["color"], sh["background"], tp["opacity"]))]
            else:
                cands = [(sh["background"], sh["background"])]
            r, (src, bg) = min((contrast_ratio(e["color"], bg), (src, bg)) for src, bg in cands)
            worst = r if worst is None else min(worst, r)
            if r < mn:
                via = f" qua tấm nền {tp['color']} {tp['opacity']:g} = {bg}" if tp and (scene or tp.get("always")) else ""
                kind = "cảnh" if scene else "nền"
                bad.append(f"{sh['id']}/{e['id']}: {e['color']} trên {kind} {src}{via} = {r:.2f}:1")
    if bad:
        return _fmt(bad, f"Tương phản chữ/nền dưới {mn}:1:")
    if not n:
        return CheckResult("pass", "Không có phần tử chữ.")
    plate = " (chữ trên cảnh tính qua tấm nền, với màu sáng nhất của cảnh)" if tp else ""
    return CheckResult("pass", f"{n} phần tử chữ, tương phản thấp nhất {worst:.2f}:1 (≥ {mn}:1){plate}.")


@register("storyboard_safe_area")
def safe_area(project: Path, params: dict) -> CheckResult:
    sb = load_yaml(project, params["path"])
    m, bleed = float(params.get("text_margin_pct", 5)), float(params.get("max_bleed_pct", 10))
    bad = []
    for sh in sb.get("shots") or []:
        for e in sh.get("elements") or []:
            bx = e["box"]
            x0, y0, x1, y1 = bx["x"], bx["y"], bx["x"] + bx["w"], bx["y"] + bx["h"]
            where = f"{sh['id']}/{e['id']}"
            if "text" in e:
                if x0 < m - EPS or y0 < m - EPS or x1 > 100 - m + EPS or y1 > 100 - m + EPS:
                    bad.append(f"{where}: chữ ra ngoài vùng an toàn {m:g}% (hộp {x0:g},{y0:g} → {x1:g},{y1:g})")
            elif x0 < -bleed or y0 < -bleed or x1 > 100 + bleed or y1 > 100 + bleed:
                bad.append(f"{where}: hình tràn khung quá {bleed:g}% (hộp {x0:g},{y0:g} → {x1:g},{y1:g})")
    if bad:
        return _fmt(bad, "Phần tử ngoài vùng an toàn:")
    return CheckResult("pass", f"Chữ trong vùng an toàn {m:g}%, hình không tràn quá {bleed:g}%.")


@register("storyboard_sfx_density")
def sfx_density(project: Path, params: dict) -> CheckResult:
    c = Ctx(project, params)
    mx, win = int(params.get("max_per_10s", 5)), float(params.get("window_s", 10))
    times = []
    for sh in c.sb.get("shots") or []:
        els = {e["id"]: e for e in sh.get("elements") or []}
        for fx in sh.get("sfx") or []:
            e = els.get(fx["target"], {})
            frac = (e.get(fx["event"]) or {}).get("at", 0 if fx["event"] != "exit" else 1)
            times.append((c.shot_start(sh) + c.shot_dur(sh) * frac, f"{sh['id']}:{fx['name']}"))
    times.sort()
    peak, at = 0, 0.0
    for i, (t, _) in enumerate(times):
        k = sum(1 for u, _ in times[i:] if u < t + win)
        if k > peak:
            peak, at = k, t
    if peak > mx:
        return CheckResult("fail", f"{peak} tiếng động trong {win:g} giây từ {_mmss(at)} (tối đa {mx}). Bớt hoặc dàn ra.")
    return CheckResult("pass", f"{len(times)} tiếng động, dày nhất {peak} trong {win:g} giây (tối đa {mx}).")


@register("storyboard_preview_in_sync")
def preview_in_sync(project: Path, params: dict) -> CheckResult:
    import json
    from vp.design_preview import content_hash
    mpath = project / params["manifest"]
    if not mpath.is_file():
        return CheckResult("fail", "Chưa có ảnh phác thảo. Chạy: python -m vp design preview <dự án>")
    man = json.loads(mpath.read_text(encoding="utf-8"))
    now = content_hash(project, params["path"], params.get("script", "01_script/script.yaml"))
    if man.get("hash") != now:
        return CheckResult("fail", "Ảnh phác thảo đã cũ so với storyboard/kịch bản. Chạy lại: python -m vp design preview <dự án>")
    return CheckResult("pass", f"{len(man.get('frames', []))} ảnh phác thảo khớp storyboard hiện tại.")


@register("storyboard_mascot")
def mascot(project: Path, params: dict) -> CheckResult:
    """Linh vật: phản ứng ở điểm nhấn (min–max lần, không tính cảnh kết), cảnh kết luôn có linh vật,
    biểu cảm phải có trong brand.mascot của brief."""
    sb = load_yaml(project, params["path"])
    brief = load_yaml(project, params.get("brief", "00_brief/brief.yaml"))
    m = brief["brand"].get("mascot")
    if not m:
        return CheckResult("pass", "Kênh không có linh vật — bỏ qua.")
    known = {e["id"] for e in m["expressions"]}
    masc = {a["id"]: a for a in sb.get("assets") or [] if a.get("kind") == "mascot"}
    bad = [f"asset {i}: biểu cảm '{a.get('expression')}' không có trong brand.mascot ({sorted(known)})"
           for i, a in masc.items() if a.get("expression") not in known]
    shots = sb.get("shots") or []
    uses, prev = [], set()
    for sh in shots[:-1]:
        cur = {e["asset"] for e in sh.get("elements") or [] if e.get("asset") in masc}
        uses += [(sh["id"], a) for a in sorted(cur - prev)]   # cùng linh vật kéo dài qua khung nối tiếp = 1 lần phản ứng
        prev = cur
    lo, hi = int(params.get("min_reactions", 2)), int(params.get("max_reactions", 3))
    if not lo <= len(uses) <= hi:
        bad.append(f"{m['name']} phản ứng {len(uses)} lần ngoài cảnh kết (cần {lo}–{hi} lần, ở các điểm nhấn)")
    if shots and not any(e.get("asset") in masc for e in shots[-1].get("elements") or []):
        bad.append(f"cảnh kết {shots[-1]['id']} chưa có {m['name']}")
    if bad:
        return _fmt(bad, "Linh vật chưa đúng luật:")
    where = ", ".join(f"{s}:{masc[a].get('expression')}" for s, a in uses)
    return CheckResult("pass", f"{m['name']} phản ứng {len(uses)} lần ({where}) và có mặt ở cảnh kết {shots[-1]['id']}.")
