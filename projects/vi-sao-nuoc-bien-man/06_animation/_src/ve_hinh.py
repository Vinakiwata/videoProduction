#!/usr/bin/env python3
"""Vẽ toàn bộ hình SVG cho 'Vì sao nước biển lại mặn?' — phong cách phẳng, nét tròn, bóng đổ nhẹ.
Icon/chữ/nút: chỉ 4 màu nhận diện, sắc độ bằng độ trong suốt. Cảnh (kind=scene): màu tự nhiên, ở canh.py. Mỗi chi tiết cần chuyển động nằm trong <g id="...">.
Chạy: python3 projects/vi-sao-nuoc-bien-man/06_animation/_src/ve_hinh.py
"""
import math
import random
from pathlib import Path

N, Y, W, D = "#0078E0", "#FFC907", "#FFFFFF", "#5E270E"   # bảng màu Khỉ Khám Phá: xanh dương, vàng, trắng, nâu gỗ
OUT = Path(__file__).resolve().parents[1] / "assets"
SHADOW = f'fill="{D}" fill-opacity="0.25"'


def svg(vb, *parts, extra=""):
    body = "\n".join(parts)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{extra}>\n{body}\n</svg>\n')


def g(id_, *parts):
    return f'<g id="{id_}">' + "".join(parts) + "</g>"


def drop_path(cx, cy, r):
    """Giọt nước: đỉnh nhọn phía trên, đáy tròn bán kính r tâm (cx, cy)."""
    return (f"M{cx} {cy - 2.3 * r} C{cx + 0.35 * r} {cy - 1.5 * r} {cx + r} {cy - 0.75 * r} {cx + r} {cy} "
            f"A{r} {r} 0 1 1 {cx - r} {cy} C{cx - r} {cy - 0.75 * r} {cx - 0.35 * r} {cy - 1.5 * r} {cx} {cy - 2.3 * r}Z")


def cube(x, y, s, fill=W, op=1.0):
    """Hạt muối lập phương nhìn nghiêng: mặt trước + mặt trên + mặt bên (sắc độ bằng độ trong suốt)."""
    t = s * 0.35
    return (f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{s * 0.12:.1f}" fill="{fill}" fill-opacity="{op}"/>'
            f'<path d="M{x} {y} L{x + t} {y - t} L{x + s + t} {y - t} L{x + s} {y}Z" fill="{fill}" fill-opacity="{op * 0.75:.2f}"/>'
            f'<path d="M{x + s} {y} L{x + s + t} {y - t} L{x + s + t} {y + s - t} L{x + s} {y + s}Z" fill="{fill}" fill-opacity="{op * 0.55:.2f}"/>')


def cloud(cx, cy, s, op=1.0):
    """Mây phẳng: 3 khối tròn (nhỏ - lớn - vừa) chồng nhau, đáy phẳng tại cy."""
    cid = f"cb{int(cx)}_{int(cy)}"

    def c(dx, dy, r):
        return f'<circle cx="{cx + dx * s:.1f}" cy="{cy + dy * s:.1f}" r="{r * s:.1f}" fill="{W}" fill-opacity="{op}"/>'
    return (f'<ellipse cx="{cx}" cy="{cy + 7 * s:.1f}" rx="{70 * s:.1f}" ry="{8 * s:.1f}" {SHADOW}/>'
            f'<clipPath id="{cid}"><rect x="{cx - 80 * s:.1f}" y="{cy - 80 * s:.1f}" width="{160 * s:.1f}" height="{80 * s:.1f}"/></clipPath>'
            f'<g clip-path="url(#{cid})">' + c(-46, -18, 30) + c(0, -34, 44) + c(48, -20, 32) +
            f'<rect x="{cx - 70 * s:.1f}" y="{cy - 24 * s:.1f}" width="{140 * s:.1f}" height="{24 * s:.1f}" rx="{2 * s:.1f}" fill="{W}" fill-opacity="{op}"/></g>')


A = {}

# ---------- nước, sông, biển ----------
A["A-SONG-ICON"] = svg("0 0 300 220",
    f'<ellipse cx="150" cy="204" rx="120" ry="9" {SHADOW}/>',
    g("water", f'<path d="M20 60 C90 30 120 110 170 100 S250 60 285 90 L285 140 C240 112 210 160 160 156 S80 92 20 118Z" fill="{W}"/>'),
    g("ripples", *[f'<path d="M{x} {y} q14 -6 28 0" stroke="{N}" stroke-width="6" stroke-linecap="round" fill="none"/>'
                   for x, y in ((50, 92), (140, 126), (225, 108))]))

glass_shape = "M60 40 L240 40 L215 340 Q213 360 193 360 L107 360 Q87 360 85 340Z"
A["A-COC-SONG"] = svg("0 0 360 440", '<g transform="translate(30 0)">',
    f'<ellipse cx="150" cy="370" rx="85" ry="12" {SHADOW}/>',
    g("water", f'<path d="M72 130 L228 130 L215 340 Q213 360 193 360 L107 360 Q87 360 85 340Z" fill="{W}" fill-opacity="0.22"/>'),
    g("drop", f'<path d="{drop_path(150, 255, 32)}" fill="{W}"/>',
      f'<circle cx="139" cy="248" r="7" fill="{N}" fill-opacity="0.35"/>'),
    g("glass", f'<path d="{glass_shape}" fill="none" stroke="{W}" stroke-width="12" stroke-linejoin="round"/>',
      f'<path d="M95 70 L108 300" stroke="{W}" stroke-opacity="0.6" stroke-width="8" stroke-linecap="round"/>'), '</g>',
    g("label", f'<text x="180" y="425" font-family="Be Vietnam Pro, DejaVu Sans, sans-serif" font-size="40" font-weight="700" text-anchor="middle" fill="{W}">sông</text>'))

A["A-COC-BIEN"] = svg("0 0 360 440", '<g transform="translate(30 0)">',
    f'<ellipse cx="150" cy="370" rx="85" ry="12" {SHADOW}/>',
    g("water", f'<path d="M72 130 L228 130 L215 340 Q213 360 193 360 L107 360 Q87 360 85 340Z" fill="{N}"/>',
      f'<path d="M72 130 q39 -14 78 0 t78 0" stroke="{W}" stroke-width="6" fill="none"/>'),
    g("salt", cube(108, 250, 34), cube(160, 285, 30), cube(150, 205, 26)),
    g("glass", f'<path d="{glass_shape}" fill="none" stroke="{W}" stroke-width="12" stroke-linejoin="round"/>',
      f'<path d="M95 70 L108 300" stroke="{W}" stroke-opacity="0.6" stroke-width="8" stroke-linecap="round"/>'), '</g>',
    g("label", f'<text x="180" y="425" font-family="Be Vietnam Pro, DejaVu Sans, sans-serif" font-size="40" font-weight="700" text-anchor="middle" fill="{W}">biển</text>'))

# A-HOI đã bỏ (28/11/2026): Khỉ thắc mắc (linh vật) thay dấu hỏi.

A["A-MAY"] = svg("0 0 480 190", g("cloud", cloud(240, 168, 2.0)))

A["A-GIOT-MUA"] = svg("0 0 120 200", g("drop",
    f'<ellipse cx="60" cy="190" rx="26" ry="6" {SHADOW}/>',
    f'<path d="{drop_path(60, 135, 42)}" fill="{W}"/>',
    f'<path d="M42 118 q-6 18 4 34" stroke="{N}" stroke-opacity="0.35" stroke-width="7" fill="none" stroke-linecap="round"/>'))

A["A-GIOT-MUA-CHUA"] = svg("0 0 120 200",
    f'<ellipse cx="60" cy="190" rx="26" ry="6" {SHADOW}/>',
    g("drop", f'<path d="{drop_path(60, 135, 42)}" fill="{W}"/>'),
    g("acid_rim", f'<path d="{drop_path(60, 135, 42)}" fill="none" stroke="{Y}" stroke-width="9" stroke-linejoin="round"/>'),
    g("bubbles", f'<circle cx="50" cy="140" r="9" fill="{Y}"/>', f'<circle cx="72" cy="118" r="6" fill="{Y}"/>',
      f'<circle cx="68" cy="156" r="5" fill="{Y}"/>'))

def molecule(cx, cy, s, ang):
    dx, dy = math.cos(ang) * 26 * s, math.sin(ang) * 26 * s
    return (f'<line x1="{cx - dx:.1f}" y1="{cy - dy:.1f}" x2="{cx + dx:.1f}" y2="{cy + dy:.1f}" stroke="{W}" stroke-width="{6 * s:.1f}" stroke-linecap="round"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{13 * s:.1f}" fill="{W}"/>'
            f'<circle cx="{cx - dx:.1f}" cy="{cy - dy:.1f}" r="{9 * s:.1f}" fill="{W}" fill-opacity="0.8"/>'
            f'<circle cx="{cx + dx:.1f}" cy="{cy + dy:.1f}" r="{9 * s:.1f}" fill="{W}" fill-opacity="0.8"/>')

A["A-PHANTU-KHI"] = svg("0 0 450 300", g("molecules",
    *[molecule(x, y, s, a) for x, y, s, a in ((70, 80, 1.0, 0.3), (220, 60, 0.85, 1.9), (170, 170, 1.1, 0.9),
                                              (60, 230, 0.8, 2.6), (330, 200, 1.0, 0.1), (390, 80, 0.9, 1.2))]))

random.seed(7)
grains = "".join(cube(20 + random.randint(0, 380), 40 + random.randint(0, 120), random.choice((14, 18, 24)),
                      op=random.choice((0.75, 0.9, 1.0))) for _ in range(18))
A["A-HAT-MUOI"] = svg("0 0 440 200", g("grains", grains),
    g("sparkles", *[f'<path d="M{x} {y - 10} L{x + 3} {y - 3} L{x + 10} {y} L{x + 3} {y + 3} L{x} {y + 10} L{x - 3} {y + 3} '
                    f'L{x - 10} {y} L{x - 3} {y - 3}Z" fill="{Y}"/>' for x, y in ((60, 30), (330, 40), (200, 185))]))

A["A-KINH-LUP"] = svg("0 0 300 520",
    g("handle", f'<path d="M150 300 L150 500" stroke="{D}" stroke-opacity="0.25" stroke-width="44" stroke-linecap="round" transform="translate(8 8)"/>',
      f'<path d="M150 300 L150 500" stroke="{Y}" stroke-width="40" stroke-linecap="round"/>'),
    g("lens", f'<circle cx="150" cy="150" r="128" fill="{W}" fill-opacity="0.12"/>',
      f'<path d="M30 175 q60 -24 120 0 t120 0" stroke="{W}" stroke-opacity="0.6" stroke-width="8" fill="none"/>',
      f'<circle cx="150" cy="150" r="128" fill="none" stroke="{Y}" stroke-width="22"/>'),
    g("salt", cube(85, 120, 26), cube(180, 190, 22), cube(140, 85, 18)))

rays = "".join(f'<line x1="{150 + math.cos(a) * 92:.1f}" y1="{150 + math.sin(a) * 92:.1f}" x2="{150 + math.cos(a) * 130:.1f}" '
               f'y2="{150 + math.sin(a) * 130:.1f}" stroke="{Y}" stroke-width="18" stroke-linecap="round"/>'
               for a in (i * math.pi / 4 for i in range(8)))
A["A-MAT-TROI"] = svg("0 0 300 300", g("rays", rays), g("core", f'<circle cx="150" cy="150" r="72" fill="{Y}"/>',
    f'<circle cx="128" cy="128" r="22" fill="{W}" fill-opacity="0.35"/>'))

A["A-HOI-NUOC"] = svg("0 0 300 500",
    g("arrows", *[f'<path d="M{x} 440 L{x} 90" stroke="{W}" stroke-width="7" stroke-dasharray="4 22" stroke-linecap="round" fill="none"/>'
                  f'<path d="M{x - 26} 112 L{x} 70 L{x + 26} 112" stroke="{W}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                  for x in (70, 150, 230)]),
    g("vapor", *[f'<circle cx="{x}" cy="{y}" r="9" fill="{W}" fill-opacity="0.85"/>' for x, y in (
        (95, 380), (125, 300), (180, 350), (205, 250), (110, 200), (175, 160), (245, 320), (55, 270))]))

A["A-MUOI-O-LAI"] = svg("0 0 940 160",
    g("salt", *[cube(30 + i * 52, 70 + (i % 3) * 14, 30 if i % 2 else 24, op=0.9 if i % 3 else 1.0) for i in range(17)]),
    g("sparkles", *[f'<path d="M{x} {y - 12} L{x + 4} {y - 4} L{x + 12} {y} L{x + 4} {y + 4} L{x} {y + 12} L{x - 4} {y + 4} '
                    f'L{x - 12} {y} L{x - 4} {y - 4}Z" fill="{Y}"/>' for x, y in ((120, 40), (380, 30), (620, 50), (850, 36))]))

def ring_icon(kind, x, y):
    if kind == "rain":
        return f'<path d="{drop_path(x, y + 10, 18)}" fill="{W}"/>'
    if kind == "rock":
        return f'<path d="M{x - 34} {y + 20} C{x - 40} {y - 4} {x - 10} {y - 26} {x + 14} {y - 22} C{x + 40} {y - 16} {x + 40} {y + 16} {x + 26} {y + 24}Z" fill="{W}"/>'
    if kind == "river":
        return f'<path d="M{x - 40} {y - 6} C{x - 14} {y - 22} {x + 10} {y + 8} {x + 40} {y - 6} L{x + 40} {y + 12} C{x + 10} {y + 26} {x - 14} {y - 4} {x - 40} {y + 12}Z" fill="{W}"/>'
    if kind == "sea":
        return (f'<path d="M{x - 42} {y - 2} q10.5 -12 21 0 t21 0 t21 0 t21 0 V{y + 26} Q{x + 42} {y + 32} {x + 36} {y + 32} '
                f'H{x - 36} Q{x - 42} {y + 32} {x - 42} {y + 26}Z" fill="{W}"/>'
                f'<path d="M{x - 30} {y + 14} q7.5 -7 15 0 t15 0 t15 0 t15 0" stroke="{N}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    return cloud(x, y + 8, 0.55)

pts = {"rain": (200, 70), "rock": (330, 170), "river": (300, 320), "sea": (100, 320), "cloud": (70, 170)}
arcs = "".join(f'<path d="{d}" stroke="{Y}" stroke-width="12" fill="none" stroke-linecap="round"/>'
               f'<path d="{h}" fill="{Y}"/>' for d, h in (
    ("M240 85 A160 160 0 0 1 320 130", "M330 112 L322 146 L298 124Z"),
    ("M335 215 A160 160 0 0 1 320 280", "M338 276 L310 300 L300 266Z"),
    ("M250 330 A160 160 0 0 1 150 332", "M160 316 L130 334 L158 352Z"),
    ("M75 285 A160 160 0 0 1 65 215", "M48 228 L66 196 L84 226Z"),
    ("M105 125 A160 160 0 0 1 160 80", "M146 66 L182 72 L158 98Z")))
A["A-VONG-TUAN-HOAN"] = svg("0 0 400 400", g("ring", arcs), g("icons", *[ring_icon(k, *v) for k, v in pts.items()]))

# Khung A-KHOANG-CHAT trong storyboard: x 30–75 %, y 30–70 % của khung 1920×1080 → hộp 864×432.
# Miệng núi lửa (400,300 trên 960×540) → (225, 276); khe nứt (670,384) → (764, 432) trong hộp này.
def _khoang():
    random.seed(11)
    out = []
    for sx, sy, n, drift in ((225, 276, 9, 25), (764, 430, 10, -25)):
        for i in range(n):
            t = (i + 1) / n
            x = sx + random.uniform(-1, 1) * 60 * t + drift * t
            y = sy - t * (sy - 20)
            out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{9 - 4 * t:.1f}" fill="{W}" fill-opacity="{1 - 0.45 * t:.2f}"/>')
    return out


A["A-KHOANG-CHAT"] = svg("0 0 864 432", g("dots", *_khoang()))

A["A-MUI-TEN"] = svg("0 0 200 100", g("arrow",
    f'<path d="M20 50 L150 50" stroke="{Y}" stroke-width="22" stroke-linecap="round"/>',
    f'<path d="M120 15 L180 50 L120 85Z" fill="{Y}" stroke="{Y}" stroke-width="10" stroke-linejoin="round"/>'))

A["A-NUT-DANG-KY"] = svg("0 0 520 180",
    f'<rect x="18" y="26" width="490" height="140" rx="70" {SHADOW}/>',
    g("button", f'<rect x="10" y="14" width="490" height="140" rx="70" fill="{Y}"/>'),
    g("label", f'<text x="255" y="104" font-family="Be Vietnam Pro, DejaVu Sans, sans-serif" font-size="64" font-weight="800" '
               f'text-anchor="middle" fill="{D}">ĐĂNG KÝ</text>'))

A["A-CHUONG"] = svg("0 0 200 240",
    g("bell", f'<path d="M100 30 C55 30 45 75 45 115 C45 150 30 165 22 178 L178 178 C170 165 155 150 155 115 C155 75 145 30 100 30Z" fill="{W}"/>',
      f'<circle cx="100" cy="22" r="12" fill="{W}"/>', f'<path d="M78 192 a22 22 0 0 0 44 0Z" fill="{W}"/>'),
    g("ringlines", f'<path d="M20 70 q-14 40 0 80 M180 70 q14 40 0 80" stroke="{W}" stroke-width="9" fill="none" stroke-linecap="round"/>'))

# Cảnh chân thật, màu tự nhiên (kind=scene) — xem canh.py
import sys as _sys
_sys.dont_write_bytecode = True   # không sinh __pycache__ trong 06_animation (sẽ làm cổng duyệt hết hiệu lực)
_sys.path.insert(0, str(Path(__file__).resolve().parent))
from canh import S as _CANH  # noqa: E402
A.update(_CANH)

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for k, v in A.items():
        (OUT / f"{k}.svg").write_text(v, encoding="utf-8")
    print(f"Đã vẽ {len(A)} hình vào {OUT}")
