"""Cảnh minh hoạ chân thật, màu tự nhiên (asset kind=scene) — quyết định của chủ dự án 28/11/2026.
Vẫn phẳng, nét tròn; chiều sâu tạo bằng lớp xa → gần (núi xa nhạt, đồi gần đậm), cây/đá có mặt sáng–tối.
Khung dọc 9:16 (28/11/2026): mọi cảnh vẽ trên khung 540×960 (= 1080×1920 chia 2) để toạ độ khớp storyboard theo %.
Vùng an toàn trên khung này: x 32–454, y 110–730 (lề Shorts/TikTok/Reels chia 2) — vật chính của cảnh nằm trong đó;
dải dưới 230 px chỉ là phần phụ (đồi, cát, đáy biển). Dòng chảy chính đi từ trên xuống.
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


def flow_path(center, n=11):
    """Đường tâm ẩn cho công thức chuyển động `along` của Tool 07: gợn sóng trôi xuôi dòng theo đường này.
    data-flow = nửa chiều dài gợn ở n điểm cách đều theo độ dài cung (gợn to dần khi sông rộng ra)."""
    pts = [(x, y) for x, y, _ in center]
    acc = [0.0]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        acc.append(acc[-1] + math.hypot(x1 - x0, y1 - y0))
    sizes, j = [], 0
    for k in range(n):
        target = acc[-1] * k / (n - 1)
        while j < len(acc) - 2 and acc[j + 1] < target:
            j += 1
        sizes.append(max(6.0, center[j][2] * 0.32))
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    return f'<path data-flow="{" ".join(f"{v:.1f}" for v in sizes)}" d="{d}" fill="none" stroke="none"/>'


def small_cloud(x, y, s=1.0):
    return (f'<g fill="{W}" fill-opacity="0.9"><circle cx="{x - 22 * s}" cy="{y}" r="{16 * s}"/><circle cx="{x}" cy="{y - 9 * s}" r="{22 * s}"/>'
            f'<circle cx="{x + 24 * s}" cy="{y + 1 * s}" r="{15 * s}"/><rect x="{x - 38 * s}" y="{y}" width="{78 * s}" height="{16 * s}" rx="{8 * s}"/></g>')


S = {}
VB = "0 0 540 960"

# ---------- A-SONG: núi trên, đồi cây, sông uốn từ chân núi xuống ----------
# Kính lúp S03-01-b: tâm mắt kính ≈ (243, 435) → sông đi qua đó; giọt mưa S03-02-a rơi xuống (243, 446).
_song_pts = [(262, 330, 5), (282, 362, 12), (252, 400, 22), (238, 440, 32), (262, 496, 48), (304, 560, 68), (290, 640, 94),
             (244, 724, 126), (232, 822, 166), (262, 960, 220)]
_song_d, _song_c = river_path(_song_pts)
random.seed(3)
_far_trees = [(x, 352 + random.uniform(-6, 6), 0.42 + random.uniform(-0.06, 0.06)) for x in range(14, 540, 30) if not 220 < x < 310]
_near_trees = [(52, 600, 1.1), (110, 680, 1.25), (40, 790, 1.45), (130, 880, 1.6), (440, 610, 1.1), (500, 700, 1.3),
               (420, 800, 1.5), (490, 900, 1.7), (160, 540, 0.9), (400, 520, 0.85)]
S["A-SONG"] = svg(VB,
    g("sky", f'<rect width="540" height="960" fill="{SKY}"/>', small_cloud(110, 150, 1.1), small_cloud(420, 118, 0.9)),
    g("mountains",
      f'<path d="M0 300 L70 214 L140 270 L230 170 L320 268 L400 200 L540 290 V960 H0Z" fill="{MTN_FAR}"/>',
      snow_caps([(70, 214, 16), (230, 170, 22), (400, 200, 18)]),
      f'<path d="M0 340 L100 262 L190 320 L300 250 L390 322 L540 276 V960 H0Z" fill="{MTN}"/>'),
    g("hills",
      f'<path d="M0 362 C110 336 200 352 270 344 C360 334 450 352 540 338 V960 H0Z" fill="{HILL_L}"/>',
      f'<path d="M0 640 C140 610 300 660 540 620 V960 H0Z" fill="{HILL}"/>'),
    g("river", f'<path d="{_song_d}" fill="{RIVER}"/>'),
    g("ripples", flow_path(_song_c), ripples(_song_c, every=34, width=3)),
    g("trees", *[pine(x, y, s) for x, y, s in _far_trees], *[pine(x, y, s) for x, y, s in sorted(_near_trees, key=lambda t: t[1])],
      bush(150, 940, 1.4), bush(420, 950, 1.5)))

# ---------- A-CUA-SONG: núi trên, sông chảy xuống đổ ra biển ở 1/3 dưới ----------
_cs_coast = "M0 668 C90 650 180 630 260 640 C340 650 430 628 540 616"
_cs_pts = [(240, 300, 5), (262, 330, 12), (226, 372, 22), (250, 430, 34), (300, 492, 46), (282, 560, 58), (262, 612, 70), (270, 648, 48), (272, 690, 6)]
_cs_d, _cs_c = river_path(_cs_pts)
S["A-CUA-SONG"] = svg(VB,
    g("sky", f'<rect width="540" height="960" fill="{SKY}"/>', small_cloud(420, 140, 1.0), small_cloud(120, 110, 0.8)),
    g("mountains",
      f'<path d="M0 270 L80 190 L170 250 L270 150 L370 246 L450 196 L540 262 V960 H0Z" fill="{MTN_FAR}"/>',
      snow_caps([(80, 190, 14), (270, 150, 22), (450, 196, 14)]),
      f'<path d="M0 316 L110 244 L210 300 L320 236 L430 300 L540 262 V960 H0Z" fill="{MTN}"/>'),
    g("sea", f'<path d="{_cs_coast} V960 H0Z" fill="{SEA}"/>', f'<path d="M0 840 C160 826 360 850 540 830 V960 H0Z" fill="{SEA_MID}"/>'),
    g("hills",
      f'<path d="M0 338 C100 310 220 326 300 318 C400 308 470 324 540 312 V616 C430 628 340 650 260 640 C180 630 90 650 0 668Z" fill="{HILL_L}"/>',
      f'<path d="M0 520 C120 494 220 530 300 516 C380 502 460 524 540 506 V616 C430 628 340 650 260 640 C180 630 90 650 0 668Z" fill="{HILL}"/>'),
    g("beach", f'<path d="{_cs_coast}" stroke="{SAND}" stroke-width="26" fill="none" stroke-linecap="round"/>',
      f'<path d="{_cs_coast}" stroke="{SAND_WET}" stroke-width="8" fill="none" stroke-linecap="round" transform="translate(0 12)"/>'),
    g("river", f'<path d="{_cs_d}" fill="{RIVER}"/>'),
    g("ripples", flow_path(_cs_c[:-60]), ripples(_cs_c[:-60], every=30, width=3)),
    g("waves", *[f'<path d="M{x} {y} q12 -6 24 0 t24 0" stroke="{W}" stroke-width="4" fill="none" stroke-linecap="round" stroke-opacity="0.85"/>'
                 for x, y in ((60, 720), (360, 700), (180, 780), (440, 770), (90, 870), (300, 900))],
      f'<path d="M248 690 q10 -8 20 0 t20 0 M262 712 q10 -8 20 0 t20 0" stroke="{W}" stroke-width="5" fill="none" stroke-linecap="round"/>'),
    g("trees", *[pine(x, y, s) for x, y, s in ((30, 352, 0.5), (90, 344, 0.45), (380, 336, 0.45), (440, 340, 0.42), (500, 332, 0.45),
                                               (60, 460, 0.9), (140, 560, 1.1), (60, 610, 1.15), (400, 450, 0.9), (460, 560, 1.15), (390, 600, 1.05))]))

# ---------- A-BIEN: bãi biển — chân trời 45 % (432), biển 432–691, cát dưới ----------
_shore = "M0 700 C120 684 240 712 360 694 C430 684 490 700 540 690"
S["A-BIEN"] = svg(VB,
    g("sky", f'<rect width="540" height="434" fill="{SKY}"/>'),
    g("sea", f'<rect y="432" width="540" height="280" fill="{SEA}"/>', f'<rect y="432" width="540" height="24" fill="{SEA_DEEP}"/>',
      f'<rect y="456" width="540" height="60" fill="{SEA_MID}"/>'),
    g("waves", *[f'<path d="M{x} {y} q{w / 2} {-w * 0.22} {w} 0 t{w} 0" stroke="{W}" stroke-opacity="{o}" stroke-width="{sw}" fill="none" stroke-linecap="round"/>'
                 for x, y, w, o, sw in ((40, 466, 12, 0.6, 3), (230, 472, 12, 0.6, 3), (420, 464, 12, 0.6, 3),
                                        (20, 560, 20, 0.8, 4), (300, 576, 20, 0.8, 4), (470, 552, 20, 0.8, 4),
                                        (120, 640, 26, 0.9, 5), (380, 650, 26, 0.9, 5))]),
    g("sand", f'<path d="{_shore} V960 H0Z" fill="{SAND_WET}"/>',
      f'<path d="M0 720 C120 704 240 734 360 716 C430 706 490 722 540 712 V960 H0Z" fill="{SAND}"/>',
      f'<path d="{_shore}" stroke="{W}" stroke-width="7" fill="none" stroke-linecap="round"/>',
      f'<path d="M330 820 C338 802 372 800 382 820Z" fill="{ROCK}"/><path d="M358 820 C364 806 378 806 382 820Z" fill="{ROCK_D}"/>',
      f'<path d="M420 860 C424 850 442 850 446 860Z" fill="{ROCK_D}"/>',
      f'<ellipse cx="250" cy="880" rx="9" ry="4" fill="{W}" fill-opacity="0.8"/>'),
    g("palm", f'<ellipse cx="48" cy="930" rx="50" ry="8" {SHADOW}/>',
      f'<path d="M44 928 C40 800 52 640 92 486" stroke="{TRUNK}" stroke-width="18" fill="none" stroke-linecap="round"/>',
      *[f'<path d="M{44 + i * 6} {880 - i * 90} l14 -6" stroke="{SOIL}" stroke-width="4" stroke-linecap="round"/>' for i in range(4)],
      f'<path d="M92 486 C50 450 6 458 -20 500 C20 480 60 482 92 486Z" fill="{TREE}"/>',
      f'<path d="M92 486 C78 436 104 404 142 394 C124 430 110 456 92 486Z" fill="{TREE_D}"/>',
      f'<path d="M92 486 C140 458 186 466 212 506 C168 488 130 486 92 486Z" fill="{TREE}"/>',
      f'<path d="M92 486 C56 446 20 432 -6 446 C30 456 66 468 92 486Z" fill="{TREE_D}"/>',
      f'<path d="M92 486 C136 442 172 432 200 446 C162 458 124 470 92 486Z" fill="{TREE_D}"/>',
      f'<circle cx="86" cy="494" r="8" fill="{SOIL}"/><circle cx="100" cy="496" r="7" fill="{SOIL}"/>'))

# ---------- A-SUOI: núi trên, ba suối chảy xuống nhập thành sông ở dưới ----------
_streams = [[(120, 250, 4), (150, 300, 6), (126, 360, 8), (170, 420, 11), (220, 480, 15), (262, 540, 22)],
            [(250, 220, 4), (236, 276, 6), (270, 340, 9), (254, 410, 13), (262, 540, 20)],
            [(390, 260, 4), (420, 316, 6), (380, 380, 9), (330, 450, 13), (262, 540, 20)]]
_river_pts = [(262, 540, 26), (250, 620, 40), (290, 700, 56), (262, 800, 76), (236, 880, 94), (250, 960, 112)]
_rv_d, _rv_c = river_path(_river_pts)
random.seed(5)
_suoi_trees = []
for _ in range(70):
    x, y = random.uniform(16, 524), random.uniform(330, 950)
    near = any(math.hypot(x - px, y - py) < 24 + w for st in _streams for px, py, w in _spline(st, 6))
    near |= any(math.hypot(x - px, y - py) < 28 + w / 2 for px, py, w in _spline(_river_pts, 6))
    if not near:
        _suoi_trees.append((x, y, 0.45 + (y - 330) / 620 * 0.9))
_suoi_trees.sort(key=lambda t: t[1])
S["A-SUOI"] = svg(VB,
    g("sky", f'<rect width="540" height="960" fill="{SKY}"/>', small_cloud(420, 130, 1.0)),
    g("mountains",
      f'<path d="M0 330 L0 230 L130 120 L210 190 L270 150 L380 250 L460 200 L540 260 V960 H0Z" fill="{MTN_FAR}"/>',
      snow_caps([(130, 120, 24), (270, 150, 18), (460, 200, 14)]),
      f'<path d="M0 360 L0 290 L100 230 L190 290 L280 250 L400 330 L540 310 V960 H0Z" fill="{MTN}"/>'),
    g("hills", f'<path d="M0 380 C100 340 200 330 290 346 C380 360 460 340 540 356 V960 H0Z" fill="{HILL_L}"/>',
      f'<path d="M0 760 C160 730 330 776 540 744 V960 H0Z" fill="{HILL}"/>'),
    g("streams", *[f'<path d="{river_path(st)[0]}" fill="{RIVER}"/>' for st in _streams]),
    g("river", f'<path d="{_rv_d}" fill="{RIVER}"/>'),
    g("ripples", flow_path(_rv_c), ripples(_rv_c, every=26, width=3)),
    g("trees", *[pine(x, y, s) for x, y, s in _suoi_trees],
      f'<path d="M80 930 C88 910 120 908 130 930Z" fill="{ROCK}"/><path d="M106 930 C110 916 126 916 130 930Z" fill="{ROCK_D}"/>'))

# ---------- A-NEN-MUA: đồi dưới trời mưa (trời trống 0–600 cho mây, giọt mưa, tảng đá) ----------
random.seed(9)
_rain = "".join(f'<path d="M{x:.0f} {y:.0f} l-8 26" stroke="{W}" stroke-opacity="0.35" stroke-width="2.5" stroke-linecap="round"/>'
                for x, y in ((random.uniform(-300, 840), random.uniform(-30, 930)) for _ in range(250)))
# Mưa phủ rộng hơn khung (x −300…840, cả chiều cao) để Tool 07 cho rơi lặp liền mạch: công thức `fall` dời (−295, 960)/chu kỳ.
S["A-NEN-MUA"] = svg(VB,
    g("sky", f'<rect width="540" height="960" fill="{RAIN_SKY}"/>'),
    g("hills", f'<path d="M0 596 C90 576 170 590 270 582 C380 572 460 588 540 576 V960 H0Z" fill="{MTN}"/>',
      f'<path d="M0 628 C120 610 250 636 380 624 C450 618 500 630 540 622 V960 H0Z" fill="{HILL}"/>',
      f'<path d="M0 840 C150 822 330 852 540 830 V960 H0Z" fill="{TREE}"/>'),
    g("trees", *[pine(x, y, s, light=TREE, dark=TREE_D) for x, y, s in ((24, 640, 0.6), (70, 636, 0.5), (480, 632, 0.6), (522, 634, 0.55))],
      bush(170, 860, 1.0, TREE_D, SOIL), bush(400, 866, 1.1, TREE_D, SOIL)),
    g("rain", _rain))

# ---------- A-DA: tảng đá granit thật (hình theo ô, tỉ lệ 2,375 khớp ô dọc 80 %×19 %) ----------
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

# ---------- A-DAY-BIEN: mặt cắt đáy biển thật, khung dọc ----------
# Khoáng chất (A-KHOANG-CHAT, ô x 10–80 %, y 40–59,7 % → 54–432 × 384–573 trên khung này) bay lên từ
# miệng núi lửa (200, 572) và đầu khe nứt (372, 572): cả hai nằm ngay đáy ô khoáng chất.
VOLC, VENT = (200, 572), (372, 572)
S["A-DAY-BIEN"] = svg(VB,
    g("water", f'<rect width="540" height="960" fill="{SEA_DEEP}"/>', f'<rect width="540" height="560" fill="{SEA_MID}"/>',
      f'<rect width="540" height="230" fill="{SEA}"/>',
      *[f'<path d="M{x} 0 L{x + 50} 0 L{x + 140} 760 L{x + 104} 760Z" fill="{W}" fill-opacity="0.06"/>' for x in (40, 220, 380)],
      f'<path d="M0 40 q45 -14 90 0 t90 0 t90 0 t90 0 t90 0 t90 0" stroke="{W}" stroke-opacity="0.45" stroke-width="5" fill="none"/>'),
    g("floor", f'<path d="M0 770 C100 750 170 790 270 772 C360 756 440 784 540 764 L540 960 L0 960Z" fill="{SOIL}"/>',
      f'<path d="M0 840 C120 822 260 856 540 832 V960 H0Z" fill="{SAND_WET}" fill-opacity="0.35"/>',
      f'<path d="M20 830 C30 806 80 802 94 830Z M440 846 C452 822 500 822 512 846Z" fill="{ROCK_D}"/>',
      f'<path d="M56 830 C60 816 84 816 94 830Z M476 846 C482 832 502 832 512 846Z" fill="{ROCK}"/>'),
    g("volcano", f'<path d="M60 790 C120 760 160 650 178 572 L222 572 C240 650 280 760 340 790Z" fill="{ROCK_D}"/>',
      f'<path d="M200 572 L222 572 C240 650 280 760 340 790 L250 790 C236 720 214 640 200 572Z" fill="{D}" fill-opacity="0.35"/>',
      f'<path d="M192 594 C182 650 164 690 154 750 M210 594 C220 646 236 680 242 740" stroke="{LAVA}" stroke-width="6" fill="none" stroke-linecap="round"/>',
      f'<path d="M178 572 L222 572 L236 594 L164 594Z" fill="{LAVA}"/>', f'<path d="M188 572 L212 572 L218 584 L182 584Z" fill="{Y}"/>'),
    g("vent", f'<path d="M352 790 L362 572 L382 572 L392 790Z" fill="{ROCK_D}"/>', f'<path d="M372 572 L382 572 L392 790 L378 790Z" fill="{ROCK}"/>',
      f'<path d="M362 572 L382 572" stroke="{LAVA}" stroke-width="6" stroke-linecap="round"/>'),
    g("glow", f'<ellipse cx="200" cy="570" rx="46" ry="16" fill="{LAVA}" fill-opacity="0.45"/>', f'<ellipse cx="200" cy="572" rx="26" ry="8" fill="{Y}" fill-opacity="0.7"/>',
      *[f'<path d="M{x} 560 q-12 -26 0 -52 t0 -52" stroke="{Y}" stroke-width="7" fill="none" stroke-linecap="round" stroke-opacity="0.8"/>' for x in (364, 380)]))

# ---------- A-BAN-DO-SONG + A-SANG-BIEN: bản đồ nhìn từ trên cao, biển ở 1/3 dưới ----------
_sea_d = "M0 560 C120 610 260 570 360 620 C440 660 500 610 540 630 L540 960 L0 960Z"
_coast_d = "M0 560 C120 610 260 570 360 620 C440 660 500 610 540 630"
_COAST_SEGS = [((0, 560), (120, 610), (260, 570), (360, 620)), ((360, 620), (440, 660), (500, 610), (540, 630))]


def coast_y(x):
    """Toạ độ y của đường bờ biển (cùng đường cong với _coast_d) tại hoành độ x — tìm bằng chia đôi."""
    for p0, p1, p2, p3 in _COAST_SEGS:
        if p0[0] <= x <= p3[0]:
            lo, hi = 0.0, 1.0
            for _ in range(40):
                t = (lo + hi) / 2
                u = 1 - t
                xx = u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0]
                lo, hi = (t, hi) if xx < x else (lo, t)
            u = 1 - t
            return u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]
    raise ValueError(x)


# Mỗi sông chảy xuống qua bãi cát và đổ hẳn vào biển: điểm cuối nằm trong nước, dưới mép bờ 18 px.
_river_src = [((40, 120), (110, 280), (60, 420), 90), ((180, 60), (240, 240), (160, 400), 200), ((300, 110), (270, 300), (330, 450), 300),
              ((440, 80), (420, 260), (450, 420), 420), ((530, 260), (510, 380), (490, 480), 495)]
_rivers = tuple(f"M{a[0]} {a[1]} C{b[0]} {b[1]} {c[0]} {c[1]} {x} {coast_y(x) + 18:.1f}" for a, b, c, x in _river_src)


def _bez_pt(src, t):
    a, b, c, x = src
    d = (x, coast_y(x) + 18)
    u = 1 - t
    return tuple(u ** 3 * a[i] + 3 * u * u * t * b[i] + 3 * u * t * t * c[i] + t ** 3 * d[i] for i in range(2))


# chấm muối nằm đúng trên đường sông (tham số t dọc mỗi sông)
_dots = tuple(_bez_pt(src, t) for src, ts in zip(_river_src, ((0.25, 0.55, 0.8), (0.3, 0.6, 0.85), (0.2, 0.5, 0.78), (0.35, 0.7), (0.4, 0.75)))
              for t in ts)
random.seed(13)
_forest = "".join(f'<circle cx="{random.uniform(16, 524):.0f}" cy="{random.uniform(20, 540):.0f}" r="{random.uniform(12, 26):.0f}" '
                  f'fill="{random.choice((HILL, TREE))}" fill-opacity="0.9"/>' for _ in range(40))
_mtns = "".join(f'<path d="M{x - 24} {y + 16} L{x} {y - 20} L{x + 24} {y + 16}Z" fill="{TRUNK}"/><path d="M{x} {y - 20} L{x + 24} {y + 16} L{x + 6} {y + 16}Z" fill="{SOIL}"/>'
                for x, y in ((90, 50), (130, 80), (260, 40), (380, 60), (420, 90), (500, 40), (40, 200)))
S["A-BAN-DO-SONG"] = svg(VB,
    g("land", f'<rect width="540" height="960" fill="{HILL_L}"/>', _forest, _mtns),
    g("sea", f'<path d="{_sea_d}" fill="{SEA}"/>', f'<path d="M0 760 C140 790 300 750 420 790 C470 806 510 780 540 790 L540 960 L0 960Z" fill="{SEA_MID}"/>',
      f'<path d="{_coast_d}" stroke="{SAND}" stroke-width="14" fill="none"/>'),
    g("rivers", *[f'<path d="{d}" stroke="{RIVER}" stroke-width="11" fill="none" stroke-linecap="round"/>' for d in _rivers]),
    g("dots", *[f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{W}"/>' for x, y in _dots]))
S["A-SANG-BIEN"] = svg(VB, g("glow", f'<path d="{_sea_d}" fill="{W}" fill-opacity="0.28"/>'))
