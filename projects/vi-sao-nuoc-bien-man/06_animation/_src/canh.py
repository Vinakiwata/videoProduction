"""Cảnh minh hoạ chân thật, màu tự nhiên (asset kind=scene) — quyết định của chủ dự án 28/11/2026.
Vẫn phẳng, nét tròn; chiều sâu tạo bằng lớp xa → gần (núi xa nhạt, đồi gần đậm), cây/đá có mặt sáng–tối.
Mọi cảnh vẽ trên khung 960×540 (= 1920×1080 chia 2) để toạ độ khớp storyboard theo %.
"""
import math
import random

# màu nhận diện
Y, W, D = "#FFC907", "#FFFFFF", "#5E270E"   # màu kênh dùng trong cảnh: vàng (dung nham sáng), trắng, nâu (bóng đổ)
# bảng màu cảnh (brand.scene_colors)
SKY, RAIN_SKY = "#4A98D6", "#6F879E"
MTN_FAR, MTN = "#8AA6CF", "#5B7DB1"
HILL_L, HILL = "#7CC36A", "#5AA84C"
TREE, TREE_D, TRUNK, SOIL = "#3E9B4F", "#2F7A3A", "#8A5A2B", "#6B4A2E"
RIVER, SEA, SEA_MID, SEA_DEEP = "#3FA7E0", "#1F7FC4", "#145A9E", "#0A2A66"
SAND, SAND_WET = "#F2D49B", "#E3BC78"
ROCK_L, ROCK, ROCK_D, LAVA = "#B4B4BC", "#8C8C94", "#5E5E66", "#FF7A2F"
SHADOW = f'fill="{D}" fill-opacity="0.22"'


def svg(vb, *parts, extra=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{extra}>\n' + "\n".join(parts) + "\n</svg>\n"


def g(id_, *parts):
    return f'<g id="{id_}">' + "".join(parts) + "</g>"


# ---------- chi tiết dùng chung ----------
def pine(x, y, s=1.0, light=TREE, dark=TREE_D):
    """Cây thông phẳng: tán hai sắc (nửa phải tối), thân nâu; (x, y) là gốc."""
    h, w = 64 * s, 24 * s
    tan = (f"M{x:.1f} {y - h:.1f} C{x + 0.9 * w:.1f} {y - 0.62 * h:.1f} {x + 1.15 * w:.1f} {y - 0.22 * h:.1f} {x + 0.85 * w:.1f} {y - 0.1 * h:.1f} "
           f"L{x - 0.85 * w:.1f} {y - 0.1 * h:.1f} C{x - 1.15 * w:.1f} {y - 0.22 * h:.1f} {x - 0.9 * w:.1f} {y - 0.62 * h:.1f} {x:.1f} {y - h:.1f}Z")
    half = (f"M{x:.1f} {y - h:.1f} C{x + 0.9 * w:.1f} {y - 0.62 * h:.1f} {x + 1.15 * w:.1f} {y - 0.22 * h:.1f} {x + 0.85 * w:.1f} {y - 0.1 * h:.1f} "
            f"L{x:.1f} {y - 0.1 * h:.1f}Z")
    return (f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{w:.1f}" ry="{4 * s:.1f}" {SHADOW}/>'
            f'<rect x="{x - 3 * s:.1f}" y="{y - 0.16 * h:.1f}" width="{6 * s:.1f}" height="{0.16 * h:.1f}" rx="{2 * s:.1f}" fill="{TRUNK}"/>'
            f'<path d="{tan}" fill="{light}"/><path d="{half}" fill="{dark}"/>')


def bush(x, y, s=1.0, c=TREE, d=TREE_D):
    return (f'<circle cx="{x - 10 * s:.1f}" cy="{y - 8 * s:.1f}" r="{11 * s:.1f}" fill="{c}"/>'
            f'<circle cx="{x + 8 * s:.1f}" cy="{y - 10 * s:.1f}" r="{13 * s:.1f}" fill="{d}"/>'
            f'<circle cx="{x:.1f}" cy="{y - 14 * s:.1f}" r="{12 * s:.1f}" fill="{c}"/>')


def snow_caps(peaks):
    out = []
    for x, y, w in peaks:
        out.append(f'<path d="M{x} {y} L{x - w} {y + 1.15 * w} L{x - 0.45 * w} {y + 0.9 * w} L{x} {y + 1.3 * w} '
                   f'L{x + 0.45 * w} {y + 0.9 * w} L{x + w} {y + 1.15 * w}Z" fill="{W}"/>')
    return "".join(out)


def _spline(pts, n=24):
    """Catmull-Rom qua các điểm (x, y, rộng) → danh sách điểm dày đặc."""
    P = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in range(3)))
    out.append(pts[-1])
    return out


def river_path(pts):
    """Dải sông có bề rộng thay đổi theo đường tâm (x, y, rộng).
    Dựng bằng hợp của các hình thang nối tiếp + hình tròn ở mỗi điểm (cùng chiều vẽ, luật nonzero),
    nên khúc cua gắt không bao giờ làm mép sông tự cắt nhau."""
    c = _spline(pts, n=40)
    segs, dots = [], []
    for i, (x, y, w) in enumerate(c):
        a, b = c[max(i - 1, 0)], c[min(i + 1, len(c) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        r = w / 2
        dots.append(f"M{x - r:.1f} {y:.1f}a{r:.1f} {r:.1f} 0 1 0 {2 * r:.1f} 0a{r:.1f} {r:.1f} 0 1 0 {-2 * r:.1f} 0Z")
        if i:
            px, py, pnx, pny, pr = prev
            quad = [(px + pnx * pr, py + pny * pr), (x + nx * r, y + ny * r), (x - nx * r, y - ny * r), (px - pnx * pr, py - pny * pr)]
            # giữ cùng một chiều vẽ cho mọi hình thang
            area = sum(quad[k][0] * quad[(k + 1) % 4][1] - quad[(k + 1) % 4][0] * quad[k][1] for k in range(4))
            if area < 0:
                quad.reverse()
            segs.append("M" + " L".join(f"{qx:.1f} {qy:.1f}" for qx, qy in quad) + "Z")
        prev = (x, y, nx, ny, r)
    return "".join(segs) + "".join(dots), c


def ripples(center, every=5, color=W, op=0.85, width=4):
    out = []
    for i in range(every, len(center) - 2, every):
        x, y, w = center[i]
        L = max(6.0, w * 0.32)
        out.append(f'<path d="M{x - L:.1f} {y:.1f} q{L / 2:.1f} {-L * 0.22:.1f} {L:.1f} 0 t{L:.1f} 0" stroke="{color}" '
                   f'stroke-opacity="{op}" stroke-width="{width}" fill="none" stroke-linecap="round"/>')
    return "".join(out)


def small_cloud(x, y, s=1.0):
    return (f'<g fill="{W}" fill-opacity="0.9"><circle cx="{x - 22 * s}" cy="{y}" r="{16 * s}"/><circle cx="{x}" cy="{y - 9 * s}" r="{22 * s}"/>'
            f'<circle cx="{x + 24 * s}" cy="{y + 1 * s}" r="{15 * s}"/><rect x="{x - 38 * s}" y="{y}" width="{78 * s}" height="{16 * s}" rx="{8 * s}"/></g>')


S = {}

# ---------- A-SONG: núi, đồi cây, sông uốn lượn ----------
_song_pts = [(482, 296, 5), (504, 312, 12), (472, 330, 24), (442, 352, 40), (452, 386, 70), (496, 424, 100), (516, 468, 136), (500, 516, 176), (474, 560, 216)]
_song_d, _song_c = river_path(_song_pts)
random.seed(3)
_far_trees = [(x, 318 + random.uniform(-6, 6), 0.42 + random.uniform(-0.06, 0.06)) for x in range(20, 960, 34) if not 400 < x < 560]
_near_trees = [(70, 470, 1.25), (150, 488, 1.05), (220, 462, 0.9), (300, 500, 1.35), (720, 478, 1.2), (800, 452, 0.95), (860, 498, 1.45), (930, 466, 1.0)]
S["A-SONG"] = svg("0 0 960 540",
    g("sky", f'<rect width="960" height="540" fill="{SKY}"/>', small_cloud(150, 80, 1.1), small_cloud(760, 60, 0.9)),
    g("mountains",
      f'<path d="M0 250 L110 150 L210 222 L330 108 L450 226 L560 128 L690 236 L800 150 L960 222 V540 H0Z" fill="{MTN_FAR}"/>',
      snow_caps([(110, 150, 18), (330, 108, 24), (560, 128, 22), (800, 150, 18)]),
      f'<path d="M0 292 L150 202 L270 276 L400 192 L520 282 L650 200 L800 286 L960 232 V540 H0Z" fill="{MTN}"/>'),
    g("hills",
      f'<path d="M0 330 C160 292 320 314 470 300 C640 286 800 312 960 292 V540 H0Z" fill="{HILL_L}"/>',
      f'<path d="M0 420 C200 392 380 432 960 402 V540 H0Z" fill="{HILL}"/>'),
    g("river", f'<path d="{_song_d}" fill="{RIVER}"/>'),
    g("ripples", ripples(_song_c, every=34, width=3)),
    g("trees", *[pine(x, y, s) for x, y, s in _far_trees], *[pine(x, y, s) for x, y, s in _near_trees],
      bush(380, 520, 1.2), bush(640, 525, 1.4)))

# ---------- A-CUA-SONG: sông từ núi đổ ra bãi biển ----------
_cs_pts = [(300, 286, 5), (334, 302, 12), (284, 326, 24), (330, 360, 40), (450, 384, 58), (560, 398, 72), (632, 404, 84), (690, 408, 56), (740, 412, 6)]
_cs_d, _cs_c = river_path(_cs_pts)
_coast = "M600 250 C610 300 640 350 628 400 C618 450 680 500 700 540"
S["A-CUA-SONG"] = svg("0 0 960 540",
    g("sky", f'<rect width="960" height="540" fill="{SKY}"/>', small_cloud(820, 90, 1.0), small_cloud(420, 70, 0.8)),
    g("mountains",
      f'<path d="M0 240 L100 150 L200 214 L300 120 L410 222 L500 170 L620 250 V540 H0Z" fill="{MTN_FAR}"/>',
      snow_caps([(100, 150, 16), (300, 120, 22)]),
      f'<path d="M0 282 L130 210 L240 270 L360 205 L470 268 L620 252 V540 H0Z" fill="{MTN}"/>'),
    g("sea", f'<path d="M560 250 H960 V540 H700 C680 500 618 450 628 400 C640 350 610 300 600 250Z" fill="{SEA}"/>',
      f'<path d="M560 250 H960 V272 H596Z" fill="{SEA_MID}"/>'),
    g("hills",
      f'<path d="M0 320 C150 284 330 306 470 296 C540 291 590 280 604 262 C612 300 640 350 628 400 C620 450 680 500 700 540 H0Z" fill="{HILL_L}"/>',
      f'<path d="M0 430 C180 398 360 444 560 420 C600 452 650 500 670 540 H0Z" fill="{HILL}"/>'),
    g("beach", f'<path d="{_coast}" stroke="{SAND}" stroke-width="26" fill="none" stroke-linecap="round"/>',
      f'<path d="{_coast}" stroke="{SAND_WET}" stroke-width="8" fill="none" stroke-linecap="round" transform="translate(12 0)"/>'),
    g("river", f'<path d="{_cs_d}" fill="{RIVER}"/>', ripples(_cs_c[:-60], every=30, width=3)),
    g("waves", *[f'<path d="M{x} {y} q12 -6 24 0 t24 0" stroke="{W}" stroke-width="4" fill="none" stroke-linecap="round" stroke-opacity="0.85"/>'
                 for x, y in ((700, 300), (820, 330), (760, 380), (880, 420), (740, 460), (860, 500))],
      f'<path d="M640 392 q10 -8 20 0 t20 0 M646 416 q10 -8 20 0 t20 0" stroke="{W}" stroke-width="5" fill="none" stroke-linecap="round"/>'),
    g("trees", *[pine(x, y, s) for x, y, s in ((40, 330, 0.5), (90, 322, 0.45), (180, 318, 0.5), (420, 312, 0.45), (480, 306, 0.42),
                                               (60, 470, 1.2), (150, 448, 0.9), (240, 486, 1.25), (420, 478, 1.0))]))

# ---------- A-BIEN: bãi biển ----------
_shore = "M0 428 C160 412 340 444 560 424 C720 410 840 436 960 420"
S["A-BIEN"] = svg("0 0 960 540",
    g("sky", f'<rect width="960" height="272" fill="{SKY}"/>'),
    g("sea", f'<rect y="270" width="960" height="180" fill="{SEA}"/>', f'<rect y="270" width="960" height="22" fill="{SEA_DEEP}"/>',
      f'<rect y="292" width="960" height="44" fill="{SEA_MID}"/>'),
    g("waves", *[f'<path d="M{x} {y} q{w / 2} {-w * 0.22} {w} 0 t{w} 0" stroke="{W}" stroke-opacity="{o}" stroke-width="{sw}" fill="none" stroke-linecap="round"/>'
                 for x, y, w, o, sw in ((80, 300, 14, 0.6, 3), (300, 306, 14, 0.6, 3), (560, 298, 14, 0.6, 3), (820, 304, 14, 0.6, 3),
                                        (40, 352, 22, 0.8, 4), (360, 366, 22, 0.8, 4), (640, 350, 22, 0.8, 4), (860, 372, 22, 0.8, 4),
                                        (180, 398, 30, 0.9, 5), (520, 404, 30, 0.9, 5), (760, 396, 30, 0.9, 5))]),
    g("sand", f'<path d="{_shore} V540 H0Z" fill="{SAND_WET}"/>',
      f'<path d="M0 446 C180 430 360 462 560 442 C720 428 840 454 960 438 V540 H0Z" fill="{SAND}"/>',
      f'<path d="{_shore}" stroke="{W}" stroke-width="7" fill="none" stroke-linecap="round"/>',
      f'<path d="M700 492 C708 476 742 474 752 492Z" fill="{ROCK}"/><path d="M728 492 C734 480 748 480 752 492Z" fill="{ROCK_D}"/>',
      f'<path d="M790 500 C794 490 812 490 816 500Z" fill="{ROCK_D}"/>',
      f'<ellipse cx="610" cy="505" rx="9" ry="4" fill="{W}" fill-opacity="0.8"/>'),
    g("palm", f'<ellipse cx="96" cy="500" rx="56" ry="9" {SHADOW}/>',
      f'<path d="M92 498 C100 420 130 350 176 286" stroke="{TRUNK}" stroke-width="18" fill="none" stroke-linecap="round"/>',
      *[f'<path d="M{100 + i * 6} {470 - i * 46} l14 -6" stroke="{SOIL}" stroke-width="4" stroke-linecap="round"/>' for i in range(4)],
      f'<path d="M176 286 C130 252 84 260 58 300 C100 280 140 282 176 286Z" fill="{TREE}"/>',
      f'<path d="M176 286 C160 238 186 208 226 198 C206 232 194 258 176 286Z" fill="{TREE_D}"/>',
      f'<path d="M176 286 C224 258 272 266 300 306 C254 288 214 286 176 286Z" fill="{TREE}"/>',
      f'<path d="M176 286 C138 246 100 232 70 246 C110 256 148 268 176 286Z" fill="{TREE_D}"/>',
      f'<path d="M176 286 C222 242 260 232 290 246 C250 258 210 270 176 286Z" fill="{TREE_D}"/>',
      f'<circle cx="170" cy="294" r="8" fill="{SOIL}"/><circle cx="184" cy="296" r="7" fill="{SOIL}"/>'))

# ---------- A-SUOI: sườn núi, ba dòng suối nhập thành sông ----------
_streams = [[(170, 196, 4), (200, 250, 6), (180, 310, 8), (250, 370, 11), (330, 410, 16), (420, 430, 22)],
            [(262, 176, 4), (280, 230, 6), (320, 290, 9), (350, 350, 13), (420, 430, 20)],
            [(360, 226, 4), (410, 270, 6), (400, 330, 9), (440, 390, 13), (420, 430, 20)]]
_river_pts = [(420, 430, 26), (520, 446, 40), (640, 438, 56), (780, 456, 74), (960, 450, 92)]
_rv_d, _rv_c = river_path(_river_pts)
random.seed(5)
_suoi_trees = []
for _ in range(60):
    x, y = random.uniform(30, 940), random.uniform(250, 530)
    near = any(math.hypot(x - px, y - py) < 26 + w for st in _streams for px, py, w in _spline(st, 6))
    near |= any(math.hypot(x - px, y - py) < 30 + w / 2 for px, py, w in _spline(_river_pts, 6))
    hill_top = 300 - 0.12 * (x - 480) if x > 380 else 260
    if not near and y > hill_top:
        _suoi_trees.append((x, y, 0.45 + (y - 250) / 280 * 0.7))
_suoi_trees.sort(key=lambda t: t[1])
S["A-SUOI"] = svg("0 0 960 540",
    g("sky", f'<rect width="960" height="540" fill="{SKY}"/>', small_cloud(760, 80, 1.0)),
    g("mountains",
      f'<path d="M0 300 L0 210 L230 56 L330 150 L420 120 L560 250 L700 210 L960 300 V540 H0Z" fill="{MTN_FAR}"/>',
      snow_caps([(230, 56, 30), (420, 120, 20)]),
      f'<path d="M0 330 L0 260 L150 170 L250 250 L340 200 L470 300 L960 330 V540 H0Z" fill="{MTN}"/>'),
    g("hills", f'<path d="M0 360 C120 300 260 280 400 300 C560 320 760 300 960 330 V540 H0Z" fill="{HILL_L}"/>',
      f'<path d="M0 470 C220 440 420 480 960 452 V540 H0Z" fill="{HILL}"/>'),
    g("streams", *[f'<path d="{river_path(st)[0]}" fill="{RIVER}"/>' for st in _streams]),
    g("river", f'<path d="{_rv_d}" fill="{RIVER}"/>', ripples(_rv_c, every=26, width=3)),
    g("trees", *[pine(x, y, s) for x, y, s in _suoi_trees],
      f'<path d="M120 520 C128 500 160 498 170 520Z" fill="{ROCK}"/><path d="M146 520 C150 506 166 506 170 520Z" fill="{ROCK_D}"/>'))

# ---------- A-NEN-MUA: đồi dưới trời mưa ----------
random.seed(9)
_rain = "".join(f'<path d="M{x:.0f} {y:.0f} l-8 26" stroke="{W}" stroke-opacity="0.35" stroke-width="2.5" stroke-linecap="round"/>'
                for x, y in ((random.uniform(0, 980), random.uniform(0, 400)) for _ in range(90)))
S["A-NEN-MUA"] = svg("0 0 960 540",
    g("sky", f'<rect width="960" height="540" fill="{RAIN_SKY}"/>'),
    g("hills", f'<path d="M0 410 C140 380 260 396 420 384 C600 370 780 392 960 376 V540 H0Z" fill="{MTN}"/>',
      f'<path d="M0 450 C200 420 400 456 620 436 C760 424 860 446 960 432 V540 H0Z" fill="{HILL}"/>',
      f'<path d="M0 500 C240 482 520 512 960 490 V540 H0Z" fill="{TREE}"/>'),
    g("trees", *[pine(x, y, s, light=TREE, dark=TREE_D) for x, y, s in ((60, 444, 0.6), (120, 440, 0.5), (760, 432, 0.55), (840, 436, 0.65), (900, 430, 0.5))],
      bush(300, 500, 1.0, TREE_D, SOIL), bush(640, 506, 1.1, TREE_D, SOIL)),
    g("rain", _rain))

# ---------- A-DA: tảng đá granit thật ----------
_rk = [(150, 262), (176, 176), (252, 112), (360, 80), (470, 92), (560, 140), (612, 214), (604, 270)]
S["A-DA"] = svg("0 0 760 320",
    f'<ellipse cx="380" cy="282" rx="290" ry="22" {SHADOW}/>',
    g("rock",
      f'<path d="M150 272 L176 176 L252 112 L360 80 L470 92 L560 140 L612 214 L604 274 Z" fill="{ROCK}"/>',
      f'<path d="M176 176 L252 112 L360 80 L470 92 L400 130 L300 140 L220 186Z" fill="{ROCK_L}"/>',
      f'<path d="M470 92 L560 140 L612 214 L604 274 L520 274 L540 200 L500 140Z" fill="{ROCK_D}"/>',
      f'<path d="M150 272 L176 176 L220 186 L210 274Z" fill="{ROCK_L}" fill-opacity="0.6"/>',
      f'<path d="M260 118 C300 100 350 92 380 96 C360 112 320 118 290 128 C276 132 262 128 260 118Z" fill="{HILL_L}"/>',
      f'<path d="M440 104 C470 100 500 112 512 128 C490 124 466 120 448 116Z" fill="{HILL}"/>',
      f'<path d="M180 196 C188 186 200 184 210 190 C202 200 190 204 180 196Z" fill="{HILL}"/>'),
    g("cracks", f'<path d="M386 70 L380 104 L398 140 L384 190 L396 240 M398 140 L436 168 M300 150 L280 200 L292 250 M520 170 L548 214"'
                f' stroke="{D}" stroke-opacity="0.65" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'),
    g("grass", *[f'<path d="M{x} 280 l-6 -22 M{x} 280 l2 -26 M{x} 280 l9 -20" stroke="{c}" stroke-width="5" stroke-linecap="round" fill="none"/>'
                 for x, c in ((130, TREE), (160, HILL), (330, TREE), (470, HILL), (620, TREE), (648, HILL))]))

# ---------- A-DAY-BIEN: mặt cắt đáy biển thật ----------
S["A-DAY-BIEN"] = svg("0 0 960 540",
    g("water", f'<rect width="960" height="540" fill="{SEA_DEEP}"/>', f'<rect width="960" height="300" fill="{SEA_MID}"/>',
      f'<rect width="960" height="120" fill="{SEA}"/>',
      *[f'<path d="M{x} 0 L{x + 60} 0 L{x + 160} 420 L{x + 120} 420Z" fill="{W}" fill-opacity="0.06"/>' for x in (120, 380, 640)],
      f'<path d="M0 30 q60 -16 120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0" stroke="{W}" stroke-opacity="0.45" stroke-width="5" fill="none"/>'),
    g("floor", f'<path d="M0 425 C160 405 260 445 420 428 C560 412 700 440 960 420 L960 540 L0 540Z" fill="{SOIL}"/>',
      f'<path d="M0 470 C200 452 420 486 960 462 V540 H0Z" fill="{SAND_WET}" fill-opacity="0.35"/>',
      f'<path d="M60 470 C70 446 120 442 134 470Z M820 480 C832 456 880 456 892 480Z" fill="{ROCK_D}"/>',
      f'<path d="M96 470 C100 456 124 456 134 470Z M856 480 C862 466 882 466 892 480Z" fill="{ROCK}"/>'),
    g("volcano", f'<path d="M240 440 C300 420 350 340 378 300 L422 300 C450 340 500 420 560 440Z" fill="{ROCK_D}"/>',
      f'<path d="M400 300 L422 300 C450 340 500 420 560 440 L470 440 C450 400 420 340 400 300Z" fill="{D}" fill-opacity="0.35"/>',
      f'<path d="M392 322 C380 360 360 380 350 420 M410 322 C420 356 440 372 446 410" stroke="{LAVA}" stroke-width="6" fill="none" stroke-linecap="round"/>',
      f'<path d="M378 300 L422 300 L436 322 L364 322Z" fill="{LAVA}"/>', f'<path d="M388 300 L412 300 L418 312 L382 312Z" fill="{Y}"/>'),
    g("vent", f'<path d="M650 436 L660 384 L680 384 L690 436Z" fill="{ROCK_D}"/>', f'<path d="M670 384 L680 384 L690 436 L676 436Z" fill="{ROCK}"/>',
      f'<path d="M660 384 L680 384" stroke="{LAVA}" stroke-width="6" stroke-linecap="round"/>'),
    g("glow", f'<ellipse cx="400" cy="298" rx="46" ry="16" fill="{LAVA}" fill-opacity="0.45"/>', f'<ellipse cx="400" cy="300" rx="26" ry="8" fill="{Y}" fill-opacity="0.7"/>',
      *[f'<path d="M{x} 372 q-12 -26 0 -52 t0 -52" stroke="{Y}" stroke-width="7" fill="none" stroke-linecap="round" stroke-opacity="0.8"/>' for x in (662, 678)]))

# ---------- A-BAN-DO-SONG + A-SANG-BIEN: bản đồ màu tự nhiên ----------
_sea_d = "M590 0 C640 120 600 260 650 360 C690 440 640 500 660 540 L960 540 L960 0Z"
_coast_d = "M590 0 C640 120 600 260 650 360 C690 440 640 500 660 540"
_COAST_SEGS = [((590, 0), (640, 120), (600, 260), (650, 360)), ((650, 360), (690, 440), (640, 500), (660, 540))]


def coast_x(y):
    """Toạ độ x của đường bờ biển (cùng đường cong với _coast_d) tại độ cao y — tìm bằng chia đôi."""
    for p0, p1, p2, p3 in _COAST_SEGS:
        if p0[1] <= y <= p3[1]:
            lo, hi = 0.0, 1.0
            for _ in range(40):
                t = (lo + hi) / 2
                u = 1 - t
                yy = u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]
                lo, hi = (t, hi) if yy < y else (lo, t)
            u = 1 - t
            return u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0]
    raise ValueError(y)


# Mỗi sông chảy qua bãi cát và đổ hẳn vào biển: điểm cuối nằm trong nước, cách mép bờ 22 px.
_river_src = [((40, 60), (200, 120), (380, 150), 190), ((60, 420), (220, 400), (420, 330), 330), ((20, 240), (200, 250), (400, 258), 262),
              ((200, 20), (260, 110), (430, 120), 112), ((240, 520), (330, 470), (480, 420), 420)]
_rivers = tuple(f"M{a[0]} {a[1]} C{b[0]} {b[1]} {c[0]} {c[1]} {coast_x(y) + 18:.1f} {y}" for a, b, c, y in _river_src)


def _bez_pt(src, t):
    a, b, c, y = src
    d = (coast_x(y) + 18, y)
    u = 1 - t
    return tuple(u ** 3 * a[i] + 3 * u * u * t * b[i] + 3 * u * t * t * c[i] + t ** 3 * d[i] for i in range(2))


# chấm muối nằm đúng trên đường sông (tham số t dọc mỗi sông)
_dots = tuple(_bez_pt(src, t) for src, ts in zip(_river_src, ((0.25, 0.55, 0.8), (0.3, 0.6, 0.85), (0.2, 0.5, 0.78), (0.35, 0.7), (0.4, 0.75)))
              for t in ts)
random.seed(13)
_forest = "".join(f'<circle cx="{random.uniform(20, 560):.0f}" cy="{random.uniform(20, 520):.0f}" r="{random.uniform(14, 30):.0f}" '
                  f'fill="{random.choice((HILL, TREE))}" fill-opacity="0.9"/>' for _ in range(34))
_mtns = "".join(f'<path d="M{x - 26} {y + 18} L{x} {y - 22} L{x + 26} {y + 18}Z" fill="{TRUNK}"/><path d="M{x} {y - 22} L{x + 26} {y + 18} L{x + 6} {y + 18}Z" fill="{SOIL}"/>'
                for x, y in ((60, 160), (100, 190), (70, 300), (110, 330), (40, 470), (90, 500), (150, 40)))
S["A-BAN-DO-SONG"] = svg("0 0 960 540",
    g("land", f'<rect width="960" height="540" fill="{HILL_L}"/>', _forest, _mtns),
    g("sea", f'<path d="{_sea_d}" fill="{SEA}"/>', f'<path d="M760 0 C800 140 770 300 820 420 C850 480 830 520 840 540 L960 540 L960 0Z" fill="{SEA_MID}"/>',
      f'<path d="{_coast_d}" stroke="{SAND}" stroke-width="14" fill="none"/>'),
    g("rivers", *[f'<path d="{d}" stroke="{RIVER}" stroke-width="11" fill="none" stroke-linecap="round"/>' for d in _rivers]),
    g("dots", *[f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{W}"/>' for x, y in _dots]))
S["A-SANG-BIEN"] = svg("0 0 960 540", g("glow", f'<path d="{_sea_d}" fill="{W}" fill-opacity="0.28"/>'))
