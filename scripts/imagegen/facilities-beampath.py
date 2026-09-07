"""facilities-beampath: optical-layout schematic of the Zhuo Lab multiphoton
scanning microscope (SVG + PNG + WebP). Fully deterministic (no randomness).
Run:  python3 scripts/imagegen/facilities-beampath.py
Outputs go to static/media/gen/facilities-beampath.{svg,png,webp}; check
renders (cairosvg + raw-SVG Chromium screenshot) go to the scratchpad."""
import math
import os
import subprocess
from PIL import Image, ImageFont

ROOT = '/Users/ewinkuo/git-repos/zhuo-lab-site'
OUT = os.path.join(ROOT, 'static', 'media', 'gen')
SCR = os.path.join('/private/tmp/claude-501/-Users-ewinkuo',
                   '4872956d-47a4-419b-a303-3950b431e40b', 'scratchpad')
CHROME = os.path.expanduser(
    '~/Library/Caches/ms-playwright/chromium_headless_shell-1223/'
    'chrome-headless-shell-mac-arm64/chrome-headless-shell')
HELV = '/System/Library/Fonts/Helvetica.ttc'
os.makedirs(OUT, exist_ok=True)
os.makedirs(SCR, exist_ok=True)

W, H = 1600, 900
FOREST, GREEN, MINT, MINTSOFT = '#064e3b', '#0f9d78', '#6ee7b7', '#ecfdf5'
SURFACE, BORDER, TEXT, MUTED = '#f3faf7', '#d5e8e1', '#1f2937', '#5b6b66'
AMBER = '#f59e0b'
FONT = "Inter, 'Helvetica Neue', Helvetica, Arial, sans-serif"

L_box, L_ctrl, L_beam, L_comp, L_text = [], [], [], [], []
labels, boxes, segs = [], [], []


def n(v):
    s = '%.1f' % v
    return s[:-2] if s.endswith('.0') else s


def pts_d(pts):
    return 'M ' + ' L '.join(n(x) + ' ' + n(y) for x, y in pts)


# ---------------------------------------------------------------- primitives
def label(x, y, s, size=22, anchor='middle', weight=500, fill=FOREST,
          inside=False, layer=None):
    (layer if layer is not None else L_text).append(
        f'<text x="{n(x)}" y="{n(y)}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}">{s}</text>')
    labels.append((x, y, s, size, anchor, inside))


def rect(layer, x0, y0, x1, y1, fill='white', stroke=FOREST, sw=2.5, r=10,
         op=1.0):
    layer.append(
        f'<rect x="{n(x0)}" y="{n(y0)}" width="{n(x1 - x0)}" height="{n(y1 - y0)}" '
        f'rx="{r}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" '
        f'stroke-width="{sw}"/>')
    boxes.append((x0, y0, x1, y1))


def line(layer, a, b, stroke, sw, op=1.0):
    layer.append(
        f'<line x1="{n(a[0])}" y1="{n(a[1])}" x2="{n(b[0])}" y2="{n(b[1])}" '
        f'stroke="{stroke}" stroke-width="{n(sw)}" stroke-opacity="{op}" '
        f'stroke-linecap="round"/>')


def beam(pts, color, sw=3, halo=True, op=1.0):
    d = pts_d(pts)
    if halo:
        L_beam.append(
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="9" '
            f'stroke-opacity="0.16" stroke-linecap="round" stroke-linejoin="round"/>')
    L_beam.append(
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{n(sw)}" '
        f'stroke-opacity="{op}" stroke-linecap="round" stroke-linejoin="round"/>')
    segs.extend(zip(pts, pts[1:]))


def wedge(pts, color, op):
    pstr = ' '.join(n(x) + ',' + n(y) for x, y in pts)
    L_beam.append(f'<polygon points="{pstr}" fill="{color}" fill-opacity="{op}"/>')


def dashed(pts):
    L_ctrl.append(
        f'<path d="{pts_d(pts)}" fill="none" stroke="{MUTED}" stroke-width="2" '
        f'stroke-dasharray="7 5" stroke-linecap="round" stroke-linejoin="round"/>')
    segs.extend(zip(pts, pts[1:]))


def dot(x, y):
    L_ctrl.append(f'<circle cx="{n(x)}" cy="{n(y)}" r="3.5" fill="{MUTED}"/>')


def arrow(x, y, ang, color, L=14, w=6, layer=None):
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    px, py = -uy, ux
    p = [(x + ux * L / 2, y + uy * L / 2),
         (x - ux * L / 2 + px * w, y - uy * L / 2 + py * w),
         (x - ux * L / 2 - px * w, y - uy * L / 2 - py * w)]
    pstr = ' '.join(n(q[0]) + ',' + n(q[1]) for q in p)
    (layer if layer is not None else L_comp).append(
        f'<polygon points="{pstr}" fill="{color}"/>')


def lens_v(cx, cy, h, w):
    d = (f'M {n(cx)} {n(cy - h / 2)} Q {n(cx - w)} {n(cy)} {n(cx)} {n(cy + h / 2)} '
         f'Q {n(cx + w)} {n(cy)} {n(cx)} {n(cy - h / 2)} Z')
    L_comp.append(f'<path d="{d}" fill="{MINT}" fill-opacity="0.5" stroke="{FOREST}" '
                  f'stroke-width="2.5" stroke-linejoin="round"/>')
    boxes.append((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))


def lens_h(cx, cy, w, h):
    d = (f'M {n(cx - w / 2)} {n(cy)} Q {n(cx)} {n(cy - h)} {n(cx + w / 2)} {n(cy)} '
         f'Q {n(cx)} {n(cy + h)} {n(cx - w / 2)} {n(cy)} Z')
    L_comp.append(f'<path d="{d}" fill="{MINT}" fill-opacity="0.5" stroke="{FOREST}" '
                  f'stroke-width="2.5" stroke-linejoin="round"/>')
    boxes.append((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))


def plate(x, y, w, h, fill, op=0.6):
    rect(L_comp, x, y, x + w, y + h, fill=fill, op=op, sw=2, r=2)


def mirror(cx, cy, ang, nrm, L=34):
    a = math.radians(ang)
    dx, dy = math.cos(a) * L / 2, math.sin(a) * L / 2
    bx, by = -nrm[0] * 6, -nrm[1] * 6
    line(L_comp, (cx - dx + bx, cy - dy + by), (cx + dx + bx, cy + dy + by), MUTED, 3, 0.7)
    line(L_comp, (cx - dx, cy - dy), (cx + dx, cy + dy), FOREST, 6)
    boxes.append((cx - L / 2, cy - L / 2, cx + L / 2, cy + L / 2))


def rot_arc(cx, cy, r, a0, a1, color=MUTED):
    p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
    L_comp.append(f'<path d="M {n(p0[0])} {n(p0[1])} A {r} {r} 0 0 1 {n(p1[0])} {n(p1[1])}" '
                  f'fill="none" stroke="{color}" stroke-width="1.5"/>')
    arrow(p0[0], p0[1], a0 - 90, color, L=8, w=3.5)
    arrow(p1[0], p1[1], a1 + 90, color, L=8, w=3.5)


def dichroic(cx, cy, ang, L=76, t=9):
    L_comp.append(
        f'<rect x="{n(cx - L / 2)}" y="{n(cy - t / 2)}" width="{L}" height="{t}" rx="2" '
        f'fill="{MINT}" fill-opacity="0.8" stroke="{FOREST}" stroke-width="2" '
        f'transform="rotate({ang} {n(cx)} {n(cy)})"/>')
    boxes.append((cx - 27, cy - 27, cx + 27, cy + 27))


def pmt(x0, y0, x1, y1, side, name):
    rect(L_comp, x0, y0, x1, y1, r=8)
    win = 14
    if side == 'left':
        rect(L_comp, x0 + 3, y0 + 3, x0 + 3 + win, y1 - 3, fill=MINT, stroke='none', r=4)
        cx, cy = x0 + 3 + win + (x1 - x0 - 6 - win) / 2, (y0 + y1) / 2
    elif side == 'top':
        rect(L_comp, x0 + 3, y0 + 3, x1 - 3, y0 + 3 + win, fill=MINT, stroke='none', r=4)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + win / 2
    else:
        rect(L_comp, x0 + 3, y1 - 3 - win, x1 - 3, y1 - 3, fill=MINT, stroke='none', r=4)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 - win / 2
    label(cx, cy - 6, 'PMT', size=15, weight=500, fill=MUTED, inside=True)
    label(cx, cy + 17, name, size=22, weight=600, inside=True)


def objective(cx, top):
    rect(L_comp, cx - 36, top, cx + 36, top + 14, r=3)
    d = (f'M {n(cx - 30)} {n(top + 14)} L {n(cx + 30)} {n(top + 14)} '
         f'L {n(cx + 13)} {n(top + 94)} L {n(cx - 13)} {n(top + 94)} Z')
    L_comp.append(f'<path d="{d}" fill="white" stroke="{FOREST}" stroke-width="2.5" '
                  f'stroke-linejoin="round"/>')
    line(L_comp, (cx - 23, top + 40), (cx + 23, top + 40), BORDER, 2)
    L_comp.append(f'<ellipse cx="{n(cx)}" cy="{n(top + 94)}" rx="11" ry="3.5" '
                  f'fill="{MINT}" stroke="{FOREST}" stroke-width="1.5"/>')
    boxes.append((cx - 36, top, cx + 36, top + 97))


# ------------------------------------------------------------------- layout
YA, Y0, XD = 390, 450, 1040          # post-scanner axis, laser axis, vertical axis
LASER = (50, Y0 - 50, 300, Y0 + 50)
HWP_X, QWP_X = 365, 435
SC = (520, 330, 680, 510)            # scanner housing
M1, M2 = (565, Y0), (625, YA)
SL_X, TL_X = 770, 905
D1, D2 = (XD, YA), (XD, 280)
OBJ_TOP = 450
FOCUS = 580
COND_Y, FILT_F_Y = 640, 695
PMT_F = (955, 755, 1125, 815)
FILT_E_X = 1150
PMT_E = (1200, 250, 1370, 310)
FILT_T_Y = 210
PMT_T = (955, 116, 1125, 176)
PC = (1340, 560, 1580, 640)
BUS_X, BUS_TOP, BUS_BOT = 1460, 85, 855
SPUR_X = 600

# housings (bottom layer)
rect(L_box, *LASER)
rect(L_box, *SC, r=12)
rect(L_box, *PC)

# control / data lines
dashed([(XD, PMT_T[1]), (XD, BUS_TOP), (BUS_X, BUS_TOP), (BUS_X, PC[1])])
dashed([(PMT_E[2], 280), (BUS_X, 280)])
dashed([(XD, PMT_F[3]), (XD, BUS_BOT), (BUS_X, BUS_BOT), (BUS_X, PC[3])])
dashed([(SPUR_X, SC[3]), (SPUR_X, BUS_BOT), (XD, BUS_BOT)])
dot(BUS_X, 280)
dot(XD, BUS_BOT)

# excitation (green)
beam([(LASER[2], Y0), M1, M2, (XD, YA), (XD - 4, YA + 4), (XD - 4, OBJ_TOP)], GREEN)
wedge([(XD - 11, OBJ_TOP + 94), (XD + 11, OBJ_TOP + 94), (XD, FOCUS)], GREEN, 0.28)
line(L_beam, (XD - 11, OBJ_TOP + 94), (XD, FOCUS), GREEN, 2)
line(L_beam, (XD + 11, OBJ_TOP + 94), (XD, FOCUS), GREEN, 2)
beam([(XD - 6, FOCUS), (XD - 6, FILT_F_Y - 6)], GREEN, sw=2, halo=False, op=0.6)

# emitted signal (amber)
wedge([(XD, FOCUS), (XD - 20, COND_Y - 8), (XD + 20, COND_Y - 8)], AMBER, 0.22)
beam([(XD, FOCUS), (XD, PMT_F[1])], AMBER)
beam([(XD + 4, FOCUS - 16), (XD + 4, 284), (XD, 280), (XD, PMT_T[3])], AMBER)
beam([(XD, 280), (PMT_E[0], 280)], AMBER)

# direction arrows
arrow(312, Y0, 0, GREEN)
arrow(722, YA, 0, GREEN)
arrow(965, YA, 0, GREEN)
arrow(XD, 670, 90, AMBER)
arrow(1106, 280, 0, AMBER)
arrow(XD, 240, -90, AMBER)

# components
plate(HWP_X - 5, Y0 - 38, 10, 76, MINT)
plate(QWP_X - 5, Y0 - 38, 10, 76, MINT)
line(L_comp, (HWP_X - 14, Y0 + 52), (QWP_X + 14, Y0 + 52), MUTED, 1.5)
line(L_comp, (HWP_X - 14, Y0 + 46), (HWP_X - 14, Y0 + 52), MUTED, 1.5)
line(L_comp, (QWP_X + 14, Y0 + 46), (QWP_X + 14, Y0 + 52), MUTED, 1.5)

N1 = (-0.383, -0.924)
N2 = (0.383, 0.924)
mirror(M1[0], M1[1], -22.5, N1)
mirror(M2[0], M2[1], -22.5, N2)
rot_arc(M1[0], M1[1], 26, 67.5 - 36, 67.5 + 36)
rot_arc(M2[0], M2[1], 26, 247.5 - 36, 247.5 + 36)

lens_v(SL_X, YA, 100, 26)
lens_v(TL_X, YA, 112, 28)
dichroic(D1[0], D1[1], 45)
dichroic(D2[0], D2[1], -45)
objective(XD, OBJ_TOP)

# sample on stage
rect(L_comp, XD - 80, FOCUS - 6, XD + 80, FOCUS + 6, fill=MINTSOFT, sw=1.5, r=2, op=0.85)
L_comp.append(f'<ellipse cx="{n(XD)}" cy="{n(FOCUS)}" rx="26" ry="4" fill="{GREEN}" '
              f'fill-opacity="0.5"/>')
rect(L_comp, XD - 100, FOCUS + 8, XD - 40, FOCUS + 28, fill=BORDER, sw=1.5, r=3)
rect(L_comp, XD + 40, FOCUS + 8, XD + 100, FOCUS + 28, fill=BORDER, sw=1.5, r=3)

lens_h(XD, COND_Y, 90, 22)
plate(XD - 30, FILT_F_Y - 5, 60, 10, AMBER, 0.4)
plate(FILT_E_X - 5, 250, 10, 60, AMBER, 0.4)
plate(XD - 30, FILT_T_Y - 5, 60, 10, AMBER, 0.4)

pmt(*PMT_F, 'top', 'SHG forward')
pmt(*PMT_E, 'left', 'SHG epi')
pmt(*PMT_T, 'bottom', 'TPEF')

# labels
label(175, Y0 - 6, 'Femtosecond laser', size=22, weight=600, inside=True)
label(175, Y0 + 24, '1030 nm', size=20, weight=500, fill=MUTED, inside=True)
label(HWP_X, Y0 - 52, '&#955;/2')
label(QWP_X, Y0 - 52, '&#955;/4')
label(400, Y0 + 78, 'Polarisation control')
label(400, Y0 + 104, 'for P-SHG', size=20, weight=400, fill=MUTED)
label(600, SC[1] - 16, 'Resonant / galvo scanner', size=24)
label(SL_X, YA + 82, 'Scan lens')
label(TL_X, YA + 82, 'Tube lens')
label(XD + 42, YA + 8, 'Dichroic', anchor='start')
label(XD + 50, OBJ_TOP + 62, 'Objective', anchor='start')
label(XD + 115, FOCUS + 22, 'Sample / stage', anchor='start')
label(XD + 62, COND_Y + 8, 'Condenser', anchor='start')
label(XD + 46, FILT_F_Y + 8, 'Bandpass filter', anchor='start')
label(XD - 42, 288, 'Dichroic', anchor='end')
label(XD - 42, FILT_T_Y + 8, 'Bandpass filter', anchor='end')
label(FILT_E_X, 342, 'Bandpass filter')
label(1460, 608, 'Computer / DAQ', size=24, weight=600, inside=True)

# legend (top-left)
beam([(60, 93), (108, 93)], GREEN)
label(122, 100, 'Excitation beam, 1030 nm', anchor='start')
beam([(60, 128), (108, 128)], AMBER)
label(122, 135, 'Emitted signal (SHG / TPEF)', anchor='start')
dashed([(60, 163), (108, 163)])
label(122, 170, 'Control / data', anchor='start')

# ------------------------------------------------------ overlap verification
def tbox(x, y, s, size, anchor):
    fnt = ImageFont.truetype(HELV, size, index=0)
    txt = s.replace('&#955;', 'l')
    w = fnt.getlength(txt) * 1.06
    x0 = x - w / 2 if anchor == 'middle' else (x - w if anchor == 'end' else x)
    return (x0, y - 0.74 * size, x0 + w, y + 0.2 * size)


def overlap(a, b, m=4):
    return not (a[2] + m < b[0] or b[2] + m < a[0] or a[3] + m < b[1] or b[3] + m < a[1])


def seg_hits(r, a, b, m=5):
    x0, y0, x1, y1 = r[0] - m, r[1] - m, r[2] + m, r[3] + m
    k = int(math.hypot(b[0] - a[0], b[1] - a[1]) / 2) + 1
    for i in range(k + 1):
        t = i / k
        x = a[0] + (b[0] - a[0]) * t
        y = a[1] + (b[1] - a[1]) * t
        if x0 <= x <= x1 and y0 <= y <= y1:
            return True
    return False


problems = []
tb = [(tbox(x, y, s, size, anc), s, inside) for (x, y, s, size, anc, inside) in labels]
for i in range(len(tb)):
    for j in range(i + 1, len(tb)):
        if overlap(tb[i][0], tb[j][0]):
            problems.append('text/text: %r vs %r' % (tb[i][1], tb[j][1]))
    if not tb[i][2]:
        for bx in boxes:
            if overlap(tb[i][0], bx, 3):
                problems.append('text/component: %r vs box %s' % (tb[i][1], [round(v) for v in bx]))
    for a, b in segs:
        if seg_hits(tb[i][0], a, b):
            problems.append('text/beam: %r vs seg %s-%s' % (tb[i][1], a, b))
print('overlap problems:', len(problems))
for p in problems:
    print('  ', p)

# ---------------------------------------------------------------- assemble
svg = '\n'.join([
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
    f'role="img" aria-label="Optical layout of the multiphoton scanning microscope" '
    f'font-family="{FONT}">',
    f'<rect width="{W}" height="{H}" fill="{SURFACE}"/>',
    *L_box, *L_ctrl, *L_beam, *L_comp, *L_text,
    '</svg>'])

svg_path = os.path.join(OUT, 'facilities-beampath.svg')
with open(svg_path, 'w', encoding='utf-8') as fh:
    fh.write(svg)
print('wrote', svg_path, len(svg), 'bytes')

# check render 1: cairosvg
import cairosvg
cairosvg.svg2png(url=svg_path, write_to=os.path.join(SCR, 'beampath-cairo.png'),
                 output_width=W, output_height=H)

# check render 2 / final: headless Chromium
html_path = os.path.join(SCR, 'beampath.html')
with open(html_path, 'w', encoding='utf-8') as fh:
    fh.write('<!doctype html><html><head><meta charset="utf-8">'
             '<link rel="preconnect" href="https://fonts.googleapis.com">'
             '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">'
             f'<style>html,body{{margin:0;background:{SURFACE}}}svg{{display:block;width:{W}px;height:{H}px}}</style>'
             f'</head><body>{svg}</body></html>')


def shot(url, out, scale):
    if os.path.exists(out):
        os.remove(out)
    cmd = [CHROME, '--headless', '--no-sandbox', '--hide-scrollbars',
           f'--window-size={W},{H}', f'--force-device-scale-factor={scale}',
           '--virtual-time-budget=8000', f'--screenshot={out}', url]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if not os.path.exists(out):
        print('chromium failed:', r.stderr[-600:])
        return None
    return Image.open(out)


raw = shot('file://' + svg_path, os.path.join(SCR, 'beampath-chrome-svg.png'), 1)
big = shot('file://' + html_path, os.path.join(SCR, 'beampath-chrome-2x.png'), 2)
print('raw svg shot:', raw.size if raw else None, ' html 2x shot:', big.size if big else None)
if big is not None:
    img = big.convert('RGB')
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    png_path = os.path.join(OUT, 'facilities-beampath.png')
    img.save(png_path, optimize=True)
    img.save(os.path.join(OUT, 'facilities-beampath.webp'), quality=82, method=6)
    print('wrote', png_path, img.size)
