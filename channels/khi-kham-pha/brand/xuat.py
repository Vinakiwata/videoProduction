"""Tách bộ nhận diện 'Khỉ Khám Phá' (goc/bo_nhan_dien.png, ảnh tổng 1536x1024 do chủ dự án cung cấp)
thành file upload riêng (xuat/) và PNG linh vật cho video (mascot/).
Chạy: python3 channels/khi-kham-pha/brand/xuat.py"""
from pathlib import Path
from collections import deque
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

HERE = Path(__file__).resolve().parent
SRC = Image.open(HERE / 'goc' / 'bo_nhan_dien.png').convert('RGB')
OUT = HERE / 'xuat'; OUT.mkdir(parents=True, exist_ok=True)
MASCOT = HERE / 'mascot'; MASCOT.mkdir(parents=True, exist_ok=True)
L = Image.LANCZOS


def up(im, size):
    return im.resize(size, L).filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))


def cut_bg(box, keep_largest=False, keep_point=None):
    """Nền trắng nối với mép vùng cắt -> trong suốt. Giữ nguyên trắng bên trong (mắt, chữ)."""
    im = SRC.crop(box)
    a = np.asarray(im).astype(int)
    h, w, _ = a.shape
    white = (a.min(axis=2) > 228) & ((a.max(axis=2) - a.min(axis=2)) < 28)
    bg = np.zeros((h, w), bool)
    q = deque([(y, x) for x in range(w) for y in (0, h - 1)] + [(y, x) for y in range(h) for x in (0, w - 1)])
    while q:
        y, x = q.popleft()
        if 0 <= y < h and 0 <= x < w and white[y, x] and not bg[y, x]:
            bg[y, x] = True
            q.extend(((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)))
    fg = ~bg
    if keep_largest or keep_point:
        lab = np.zeros((h, w), int); n = 0; sizes = {}
        for sy in range(h):
            for sx in range(w):
                if fg[sy, sx] and not lab[sy, sx]:
                    n += 1; lab[sy, sx] = n; dq = deque([(sy, sx)]); c = 0
                    while dq:
                        y, x = dq.popleft(); c += 1
                        for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                            if 0 <= yy < h and 0 <= xx < w and fg[yy, xx] and not lab[yy, xx]:
                                lab[yy, xx] = n; dq.append((yy, xx))
                    sizes[n] = c
        k = lab[keep_point[1], keep_point[0]] if keep_point else max(sizes, key=sizes.get)
        fg = lab == k
    alpha = Image.fromarray((fg * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))
    im = im.convert('RGBA'); im.putalpha(alpha)
    return im.crop(im.getbbox())


def square_pad(im, size, margin=0.06):
    s = int(size * (1 - 2 * margin))
    r = min(s / im.width, s / im.height)
    im2 = up(im, (max(1, round(im.width * r)), max(1, round(im.height * r))))
    c = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    c.alpha_composite(im2, ((size - im2.width) // 2, (size - im2.height) // 2))
    return c


def tile(box, inset=12):
    """Ô avatar bo góc -> lấy phần vuông bên trong (bỏ góc trắng)."""
    x0, y0, x1, y1 = box
    x0 += inset; y0 += inset; x1 -= inset; y1 -= inset
    s = min(x1 - x0, y1 - y0)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    return SRC.crop((cx - s // 2, cy - s // 2, cx - s // 2 + s, cy - s // 2 + s))


files = []
def save(im, name, **kw):
    p = OUT / name; im.save(p, **kw); files.append(p)

# 1) Avatar YouTube 800x800 + TikTok + Khám Phá
yt = tile((503, 88, 760, 343), inset=0); save(up(yt, (800, 800)), 'avatar_youtube_800.png')
tt = tile((775, 88, 1027, 343), inset=0); save(up(tt, (800, 800)), 'avatar_tiktok_800.png'); save(tt.resize((200, 200), L), 'avatar_tiktok_200.png')
kp = SRC.crop((1041, 94, 1263, 316)); save(up(kp, (800, 800)), 'avatar_kham_pha_800.png')

# 2) Logo tròn nền trong suốt
logo = cut_bg((22, 22, 494, 500), keep_point=(236, 240))
save(square_pad(logo, 1024, 0.02), 'logo_khi_kham_pha_1024.png')
save(square_pad(logo, 150, 0.0), 'watermark_youtube_150.png')
square_pad(logo, 1024, 0.02).save(MASCOT / 'logo.png')

# 3) Ảnh bìa YouTube 2560x1440 — cả bìa nằm gọn vùng an toàn 1546x423 ở giữa
ban = SRC.crop((38, 670, 1498, 970))
W, H, SW, SH = 2560, 1440, 1546, 423
sharp = up(ban, (SW, round(ban.height * SW / ban.width)))
_a = np.asarray(ban).astype(float)
_top, _bot = _a[:25, 200:-200].reshape(-1, 3).mean(0), _a[-25:, 200:-200].reshape(-1, 3).mean(0)
_t = np.linspace(0, 1, H)[:, None, None] ** 1.6
bg = Image.fromarray((_top * (1 - _t) + _bot * _t).repeat(W, axis=1).astype(np.uint8))   # trời (trên) → đất (dưới), sạch
mask = Image.new('L', sharp.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, sharp.width - 1, sharp.height - 1), radius=18, fill=255)
bg.paste(sharp, ((W - SW) // 2, (H - sharp.height) // 2), mask)
save(bg, 'anh_bia_youtube_2560x1440.jpg', quality=92)
ban_full = SRC.crop((38, 670, 1498, 970)); save(ban_full, 'anh_bia_goc_1460x300.png')

# 4) Sticker biểu cảm nền trong suốt: tách theo vùng liền khối, gán vào từng nhân vật theo toạ độ
from scipy import ndimage
SB = (392, 418, 1515, 632)
ar = np.asarray(SRC.crop(SB)).astype(int)
h, w, _ = ar.shape
white = (ar.min(axis=2) > 228) & ((ar.max(axis=2) - ar.min(axis=2)) < 28)
lab_bg, _ = ndimage.label(white)
border = set(np.unique(np.concatenate([lab_bg[0], lab_bg[-1], lab_bg[:, 0], lab_bg[:, -1]]))) - {0}
fg = ~np.isin(lab_bg, list(border))
EDGES = [3, 160, 364, 536, 720, 844, 984, 1123]
for e in EDGES[1:-1]:
    fg[:, e] = False                                      # cắt dọc tại ranh giới để tách các viền dính nhau
lab, n = ndimage.label(fg)
objs = ndimage.find_objects(lab)
names = ['tham_hoi', 'vui_mung', 'thich_lam', 'doc_sach', 'ngac_nhien', 'ngau', 'yeu_trai_dat']
groups = {k: np.zeros((h, w), bool) for k in range(7)}
for idx, sl in enumerate(objs, start=1):
    ys, xs = sl
    area = (lab[sl] == idx).sum()
    if area < 25: continue
    if ys.start == 0 and xs.start + 392 < 500: continue          # mép logo lấn vào dải
    if ys.start == 0 and ys.stop - ys.start < 10: continue        # vệt mảnh của nhãn phía trên
    cx = (xs.start + xs.stop) / 2
    k = max(0, min(6, next(i for i in range(7) if cx < EDGES[i + 1])))
    if ys.stop < 70 and 660 < cx < 780: k = 4                    # cụm dấu '!!' thuộc sticker ngạc nhiên
    groups[k] |= lab == idx
for k, m in groups.items():
    al = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))
    im = SRC.crop(SB).convert('RGBA'); im.putalpha(al); im = im.crop(im.getbbox())
    sq = square_pad(im, 512, 0.04)
    save(sq, f'sticker_{k + 1}_{names[k]}_512.png')
    sq.save(MASCOT / f'{names[k]}.png')                        # bản dùng trong video (linh vật)

# 5) Thẻ khẩu hiệu
save(up(SRC.crop((1284, 32, 1514, 344)), (690, 936)), 'the_khau_hieu.png')
print('\n'.join(f'{p.name}  {Image.open(p).size}' for p in files))
