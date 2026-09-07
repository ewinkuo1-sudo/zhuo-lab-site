#!/usr/bin/env python3
"""Zhuo Lab logo mark generator.

Builds three exploratory concepts (scripts/imagegen/logo-concepts/concept-*.svg),
renders contact sheets with headless Chromium, and writes the final deliverables
(logo-mark.svg, logo-mark-256.png/.webp, logo-mark-512-dark.png/.webp,
wordmark.svg) into static/media/gen/.  Everything is deterministic: the
geometry is computed analytically, no randomness is used.

Concept: second-harmonic generation, two photons at omega become one at
2*omega.  The mark is a green field-of-view disc holding a single wave whose
frequency doubles as it passes the centre (the focus / the sample).

Usage:  python3 scripts/imagegen/logo-mark.py [concepts|refine|final|all]
"""
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image

ROOT = '/Users/ewinkuo/git-repos/zhuo-lab-site'
CONCEPTS = f'{ROOT}/scripts/imagegen/logo-concepts'
OUT = f'{ROOT}/static/media/gen'
SCRATCH = ('/private/tmp/claude-501/-Users-ewinkuo/'
           '4872956d-47a4-419b-a303-3950b431e40b/scratchpad/logo')
CHROME = os.path.expanduser(
    '~/Library/Caches/ms-playwright/chromium_headless_shell-1223/'
    'chrome-headless-shell-mac-arm64/chrome-headless-shell')
INTER_BOLD = f'{SCRATCH}/Inter-Bold.ttf'   # Inter 700 static TTF (Google Fonts)

INK = '#04201c'
GREEN = '#0f9d78'
MINT = '#6ee7b7'
MINT_SOFT = '#ecfdf5'
WHITE = '#ffffff'

for d in (CONCEPTS, OUT, SCRATCH):
    os.makedirs(d, exist_ok=True)


# ----------------------------------------------------------------------------
# geometry helpers
# ----------------------------------------------------------------------------
def smoothstep(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def chirp_points(x0, x1, k_of_x, a_of_x, yc_of_x, phase0=0.0, step=math.pi / 4):
    """Sample y = yc(x) - A(x) sin(phi(x)) with phi' = k(x), at uniform phase steps.

    Sampling in phase keeps the point density proportional to the local
    frequency, which is what a Catmull-Rom spline needs to stay faithful.
    """
    xs = np.linspace(x0, x1, 4001)
    ks = k_of_x(xs)
    phi = phase0 + np.concatenate(
        [[0.0], np.cumsum((ks[1:] + ks[:-1]) / 2.0 * np.diff(xs))])
    targets = np.arange(phi[0], phi[-1] - 1e-9, step)
    targets = np.append(targets, phi[-1])
    xq = np.interp(targets, phi, xs)
    y = yc_of_x(xq) - a_of_x(xq) * np.sin(targets)
    return np.stack([xq, y], axis=1)


def cr_path(pts):
    """Catmull-Rom spline through pts, emitted as cubic Beziers."""
    P = np.asarray(pts, dtype=float)
    n = len(P)
    d = [f'M{P[0, 0]:.2f} {P[0, 1]:.2f}']
    for i in range(n - 1):
        p0 = P[i - 1] if i > 0 else P[i]
        p1, p2 = P[i], P[i + 1]
        p3 = P[i + 2] if i + 2 < n else P[i + 1]
        c1 = p1 + (p2 - p0) / 6.0
        c2 = p2 - (p3 - p1) / 6.0
        d.append(f'C{c1[0]:.2f} {c1[1]:.2f} {c2[0]:.2f} {c2[1]:.2f} '
                 f'{p2[0]:.2f} {p2[1]:.2f}')
    return ' '.join(d)


def svg_wrap(body, label='Zhuo Lab mark', vb='0 0 64 64'):
    w, h = vb.split()[2:]
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="' + vb + '" '
            f'width="{w}" height="{h}" role="img" aria-label="{label}">\n{body}\n</svg>\n')


def stroke_path(d, color, width, extra=''):
    return (f'  <path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round"{extra}/>')


# ----------------------------------------------------------------------------
# concept A: disc + single wave whose frequency doubles at the centre
# ----------------------------------------------------------------------------
def tangent_path(P, T):
    """Cubic Bezier path through points P with unit tangents T (1/3-chord handles)."""
    d = [f'M{P[0, 0]:.2f} {P[0, 1]:.2f}']
    for i in range(len(P) - 1):
        chord = np.linalg.norm(P[i + 1] - P[i])
        c1 = P[i] + T[i] * chord / 3.0
        c2 = P[i + 1] - T[i + 1] * chord / 3.0
        d.append(f'C{c1[0]:.2f} {c1[1]:.2f} {c2[0]:.2f} {c2[1]:.2f} '
                 f'{P[i + 1, 0]:.2f} {P[i + 1, 1]:.2f}')
    return ' '.join(d)


def mark_body(periods=(0.5, 1.0), amp=8.5, amp_r=0.8, width=5.2, trans=math.pi / 4,
              phase0=0.0, x0=9.0, x1=55.0, wave_color=WHITE, disc=True,
              disc_color=GREEN, prefix='', step=math.pi / 8, **_ignored):
    """Body of the mark (disc + wave whose frequency doubles at the centre).

    The wave is defined in the phase domain: x(phi) = x0 + int dphi / k(phi),
    y(phi) = 32 - A(phi) sin(phi).  k and A ramp from the omega values to the
    2*omega values inside a window of half-width `trans` (radians) centred on
    the zero crossing between the two regimes, where the flank is nearly
    straight, so every crest and trough stays a symmetric pure sine.

    periods: (periods in the left half, periods in the right half)
    amp_r:   amplitude multiplier on the 2*omega side
    """
    half = (x1 - x0) / 2.0
    k1 = 2 * math.pi * periods[0] / half
    k2 = 2 * math.pi * periods[1] / half
    phi_end = 2 * math.pi * (periods[0] + periods[1])
    phi_mid = 2 * math.pi * periods[0]        # phase at the regime boundary
    phi = phase0 + np.linspace(0.0, phi_end, 4001)
    ramp = smoothstep((phi - (phase0 + phi_mid - trans)) / (2 * trans))
    k = k1 + (k2 - k1) * ramp
    A = amp * (1.0 + (amp_r - 1.0) * ramp)
    x = np.concatenate([[0.0], np.cumsum((1 / k[1:] + 1 / k[:-1]) / 2 * np.diff(phi))])
    x = x0 + x * (x1 - x0) / x[-1]           # fit the span exactly
    y = 32.0 - A * np.sin(phi)
    dx = np.gradient(x, phi)
    dy = np.gradient(y, phi)
    # sample every `step` radians, plus the end point
    n = int(round(phi_end / step))
    idx = np.unique(np.clip(np.round(np.linspace(0, 4000, n + 1)).astype(int), 0, 4000))
    P = np.stack([x[idx], y[idx]], axis=1)
    T = np.stack([dx[idx], dy[idx]], axis=1)
    T /= np.linalg.norm(T, axis=1, keepdims=True)
    body = []
    if disc:
        body.append(f'{prefix}  <circle cx="32" cy="32" r="30" fill="{disc_color}"/>')
    body.append(prefix + stroke_path(tangent_path(P, T), wave_color, width))
    return '\n'.join(body)


def concept_a(**kw):
    return svg_wrap(mark_body(**kw))


# ----------------------------------------------------------------------------
# concept B: disc + three crimped collagen fibres running diagonally
# ----------------------------------------------------------------------------
def concept_b(fibre_color=WHITE, width=3.4, offsets=(-9.0, 0.0, 9.0), crimp=2.3,
              crimp_lam=14.0, r_in=26.0):
    u = np.array([math.cos(math.radians(-45)), math.sin(math.radians(-45))])
    nrm = np.array([-u[1], u[0]])
    c = np.array([32.0, 32.0])
    body = [f'  <circle cx="32" cy="32" r="30" fill="{GREEN}"/>']
    for d in offsets:
        smax = math.sqrt(r_in ** 2 - d ** 2) - 1.2
        s = np.linspace(-smax, smax, 41)
        disp = crimp * np.sin(2 * math.pi * s / crimp_lam)
        pts = c + nrm * d + np.outer(s, u) + np.outer(disp, nrm)
        body.append(stroke_path(cr_path(pts), fibre_color, width))
    return svg_wrap('\n'.join(body))


# ----------------------------------------------------------------------------
# concept C: disc + two omega waves converging into one 2*omega wave
# ----------------------------------------------------------------------------
def concept_c(wave_color=WHITE, width=3.8, sep=7.5, a1=3.0, a2=6.6, lam1=20.0,
              lam2=10.0, x0=8.0, x1=56.0):
    k1, k2 = 2 * math.pi / lam1, 2 * math.pi / lam2

    def k(x):
        return k1 + (k2 - k1) * smoothstep((x - 28.0) / 8.0)

    def amp(x):
        return a1 + (a2 - a1) * smoothstep((x - 26.0) / 10.0)

    def yc_top(x):
        return 32.0 - sep * (1.0 - smoothstep((x - 20.0) / 13.0))

    def yc_bot(x):
        return 32.0 + sep * (1.0 - smoothstep((x - 20.0) / 13.0))

    top = chirp_points(x0, x1, k, amp, yc_top)
    bot = chirp_points(x0, 33.0, k, amp, yc_bot)
    body = [f'  <circle cx="32" cy="32" r="30" fill="{GREEN}"/>',
            stroke_path(cr_path(top), wave_color, width),
            stroke_path(cr_path(bot), wave_color, width)]
    return svg_wrap('\n'.join(body))


# ----------------------------------------------------------------------------
# wordmark: mark + "Zhuo Lab" set in Inter Bold, converted to outlines
# ----------------------------------------------------------------------------
def _kern_lookup(font):
    """Return kern(a, b) -> x-advance adjustment in font units (GPOS pair kerning)."""
    tables = []
    if 'GPOS' in font:
        gpos = font['GPOS'].table
        idx = set()
        for fr in gpos.FeatureList.FeatureRecord:
            if fr.FeatureTag == 'kern':
                idx.update(fr.Feature.LookupListIndex)
        for i in sorted(idx):
            lk = gpos.LookupList.Lookup[i]
            for st in lk.SubTable:
                if getattr(st, 'ExtSubTable', None) is not None:
                    st = st.ExtSubTable
                if type(st).__name__ == 'PairPos':
                    tables.append(st)

    def kern(a, b):
        for st in tables:
            if a not in st.Coverage.glyphs:
                continue
            if st.Format == 1:
                ps = st.PairSet[st.Coverage.glyphs.index(a)]
                for pvr in ps.PairValueRecord:
                    if pvr.SecondGlyph == b:
                        return getattr(pvr.Value1, 'XAdvance', 0) if pvr.Value1 else 0
            elif st.Format == 2:
                c1 = st.ClassDef1.classDefs.get(a, 0)
                c2 = st.ClassDef2.classDefs.get(b, 0)
                rec = st.Class1Record[c1].Class2Record[c2]
                adv = getattr(rec.Value1, 'XAdvance', 0) if rec.Value1 else 0
                if adv:
                    return adv
        return 0
    return kern


def text_outlines(text, font_path, size, x, baseline, tracking=0.0):
    """Return (svg path d, advance width) for text set at font-size `size`."""
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen

    font = TTFont(font_path)
    if 'fvar' in font:
        from fontTools.varLib.instancer import instantiateVariableFont
        font = instantiateVariableFont(font, {'wght': 700})
    upem = font['head'].unitsPerEm
    s = size / upem
    cmap = font.getBestCmap()
    gs = font.getGlyphSet()
    kern = _kern_lookup(font)
    names = [cmap[ord(ch)] for ch in text]
    d = []
    pen_x = x
    for i, gname in enumerate(names):
        if i > 0:
            pen_x += kern(names[i - 1], gname) * s + tracking
        pen = SVGPathPen(gs)
        gs[gname].draw(TransformPen(pen, (s, 0, 0, -s, pen_x, baseline)))
        cmds = pen.getCommands()
        if cmds:
            d.append(cmds)
        pen_x += gs[gname].width * s
    cap = font['OS/2'].sCapHeight * s if hasattr(font['OS/2'], 'sCapHeight') else 0.73 * size
    return ' '.join(d), pen_x - x, cap


def wordmark_svg(mark_kw, font_size=32.0, gap=12.0, text_color=WHITE):
    # cap-height box centred on the disc centre (y = 32)
    _, _, cap = text_outlines('Zhuo Lab', INTER_BOLD, font_size, 0, 0)
    baseline = 32.0 + cap / 2.0
    tx = 64.0 + gap
    d, adv, _ = text_outlines('Zhuo Lab', INTER_BOLD, font_size, tx, baseline)
    width = math.ceil(tx + adv + 2)
    body = mark_body(**mark_kw) + f'\n  <path d="{d}" fill="{text_color}"/>'
    return svg_wrap(body, 'Zhuo Lab', vb=f'0 0 {width} 64'), width


# ----------------------------------------------------------------------------
# rendering
# ----------------------------------------------------------------------------
def chrome_shot(html_path, png_path, w, h, transparent=False):
    args = [CHROME, '--headless', '--no-sandbox', '--hide-scrollbars',
            '--force-device-scale-factor=1', f'--window-size={w},{h}',
            '--virtual-time-budget=5000', f'--screenshot={png_path}',
            f'file://{html_path}']
    if transparent:
        args.insert(1, '--default-background-color=00000000')
    subprocess.run(args, check=True, capture_output=True)


def render_svg(svg_path, png_path, w, h, bg=None):
    """Rasterise an SVG file at exactly w x h px (transparent when bg is None)."""
    html = (f'<!doctype html><meta charset="utf-8"><body style="margin:0;'
            f'background:{bg or "transparent"}"><img src="file://{svg_path}" '
            f'width="{w}" height="{h}" style="display:block"></body>')
    html_path = f'{SCRATCH}/render.html'
    with open(html_path, 'w') as f:
        f.write(html)
    chrome_shot(html_path, png_path, w, h, transparent=bg is None)
    im = Image.open(png_path)
    im = im.convert('RGBA' if bg is None else 'RGB')
    im.save(png_path)
    return im


SIZES = (28, 64, 256)
PAD = 20


def contact_sheet(rows, sheet_png, zoom_png):
    """rows: list of (label, svg_path). Renders dark + white panels side by side."""
    panel_w = sum(SIZES) + PAD * (len(SIZES) + 1)
    row_h = max(SIZES) + PAD
    header = 36
    W = 16 * 3 + panel_w * 2
    H = header + row_h * len(rows) + 16
    cells = []
    coords = {}
    for r, (label, svg) in enumerate(rows):
        y0 = header + r * row_h
        cells.append(f'<div class="lab" style="left:16px;top:{y0 + 2}px">{label}</div>')
        for p, bg in enumerate((INK, WHITE)):
            px0 = 16 + p * (panel_w + 16)
            x = px0 + PAD
            for s in SIZES:
                yy = y0 + (row_h - s) // 2 + 6
                cells.append(f'<img src="file://{svg}" width="{s}" height="{s}" '
                             f'style="left:{x}px;top:{yy}px">')
                coords[(r, bg, s)] = (x, yy)
                x += s + PAD
    panels = ''.join(
        f'<div class="panel" style="left:{16 + p * (panel_w + 16)}px;top:{header - 8}px;'
        f'width:{panel_w}px;height:{row_h * len(rows) + 8}px;background:{bg}"></div>'
        for p, bg in enumerate((INK, WHITE)))
    html = f'''<!doctype html><meta charset="utf-8"><style>
body{{margin:0;background:#8a8f8d;width:{W}px;height:{H}px;position:relative;font:12px Helvetica,Arial}}
.panel{{position:absolute}} img{{position:absolute;display:block}}
.lab{{position:absolute;color:#fff;font-weight:700;z-index:2;text-shadow:0 0 3px #000}}
h1{{position:absolute;left:16px;top:6px;margin:0;font-size:13px;color:#fff}}
</style><body><h1>28 / 64 / 256 px on ink and on white</h1>{panels}{''.join(cells)}</body>'''
    html_path = f'{SCRATCH}/sheet.html'
    with open(html_path, 'w') as f:
        f.write(html)
    chrome_shot(html_path, sheet_png, W, H)

    # zoom sheet: real 28 px and 64 px pixels blown up with nearest neighbour
    im = Image.open(sheet_png).convert('RGB')
    z28, z64 = 8, 4
    cell_w = 28 * z28 + 12 + 64 * z64 + 24
    zoom = Image.new('RGB', (16 + cell_w * 2 + 16, 16 + (64 * z64 + 40) * len(rows)),
                     (138, 143, 141))
    for r, (label, svg) in enumerate(rows):
        yy = 16 + r * (64 * z64 + 40)
        for p, bg in enumerate((INK, WHITE)):
            x = 16 + p * cell_w
            for s, z in ((28, z28), (64, z64)):
                cx, cy = coords[(r, bg, s)]
                crop = im.crop((cx - 4, cy - 4, cx + s + 4, cy + s + 4))
                crop = crop.resize((crop.width * z, crop.height * z), Image.NEAREST)
                zoom.paste(crop, (x, yy))
                x += crop.width + 12
    zoom.save(zoom_png)


def write_rows(variants, folder):
    rows = []
    for label, name, svg in variants:
        path = f'{folder}/{name}'
        with open(path, 'w') as f:
            f.write(svg)
        rows.append((label, path))
    return rows


def build_concepts():
    variants = [
        ('A  disc + doubling wave (white)', 'concept-a.svg', concept_a()),
        ('B  disc + crimped collagen fibres', 'concept-b.svg', concept_b()),
        ('C  disc + two waves merging into one', 'concept-c.svg', concept_c()),
        ('A2 doubling wave in mint-soft', 'concept-a-mint.svg', concept_a(wave_color=MINT_SOFT)),
    ]
    rows = write_rows(variants, CONCEPTS)
    contact_sheet(rows, f'{CONCEPTS}/contact-sheet.png', f'{CONCEPTS}/contact-sheet-zoom.png')


# refinement variants of concept A (round 2)
REFINE = [
    ('R1 1+2 periods, gentler chirp, w4.4', dict(periods=(1, 2), amp=8.2, width=4.4, trans=12, x0=9, x1=55)),
    ('R2 0.5+1 periods, w5', dict(periods=(0.5, 1), amp=9.0, width=5.0, trans=10, x0=9, x1=55)),
    ('R3 0.5+1, start -45deg, right amp 0.85', dict(periods=(0.5, 1), amp=9.0, amp_r=0.85, width=5.0, trans=10, phase0=-math.pi / 4, x0=9, x1=55)),
    ('R4 0.75+1.5 periods, w4.6', dict(periods=(0.75, 1.5), amp=8.5, width=4.6, trans=10, x0=9, x1=55)),
    ('R5 1+2, start at crest, right amp 0.8', dict(periods=(1, 2), amp=8.0, amp_r=0.8, width=4.4, trans=12, phase0=math.pi / 2, x0=9, x1=55)),
]


# round 3: R2 family (half period -> one period), tuning the 2*omega side
REFINE3 = [
    ('S1 R2 reference: amp 9, w5, trans 10', dict(periods=(0.5, 1), amp=9.0, width=5.0, trans=10, x0=9, x1=55)),
    ('S2 amp 8.5, right amp 0.8, w5.2', dict(periods=(0.5, 1), amp=8.5, amp_r=0.8, width=5.2, trans=10, x0=9, x1=55)),
    ('S3 as S2 but crisp transition (trans 5)', dict(periods=(0.5, 1), amp=9.0, amp_r=0.8, width=5.2, trans=5, x0=9, x1=55)),
    ('S4 as S2 but very gradual chirp (trans 18)', dict(periods=(0.5, 1), amp=9.0, amp_r=0.8, width=5.2, trans=18, x0=9, x1=55)),
    ('S5 wider span 7..57, amp 9.5, right 0.8', dict(periods=(0.5, 1), amp=9.5, amp_r=0.8, width=5.2, trans=10, x0=7, x1=57)),
]


# round 4: S2 family, ends on extrema (horizontal tangents) vs zero crossings
REFINE4 = [
    ('T1 start at crest: crest, trough, crest, trough', dict(periods=(0.5, 1), amp=8.0, amp_r=0.8, width=5.2, trans=10, phase0=math.pi / 2, x0=10, x1=54)),
    ('T2 start at trough (vertical mirror of T1)', dict(periods=(0.5, 1), amp=8.0, amp_r=0.8, width=5.2, trans=10, phase0=-math.pi / 2, x0=10, x1=54)),
    ('T3 S2 reference (zero-crossing ends)', dict(periods=(0.5, 1), amp=8.5, amp_r=0.8, width=5.2, trans=10, x0=9, x1=55)),
    ('T4 T1 with right amp 0.7, trans 12, w5.4', dict(periods=(0.5, 1), amp=8.5, amp_r=0.7, width=5.4, trans=12, phase0=math.pi / 2, x0=10, x1=54)),
    ('T5 T1 with amp 9, right amp 0.85, w5', dict(periods=(0.5, 1), amp=9.0, amp_r=0.85, width=5.0, trans=10, phase0=math.pi / 2, x0=10, x1=54)),
]


def build_refine(variants=REFINE, tag='refine'):
    folder = f'{CONCEPTS}/{tag}'
    os.makedirs(folder, exist_ok=True)
    rows = write_rows([(lab, f'{tag}-{i + 1}.svg', concept_a(**kw))
                       for i, (lab, kw) in enumerate(variants)], folder)
    contact_sheet(rows, f'{folder}/{tag}-sheet.png', f'{folder}/{tag}-zoom.png')


# final parameters (chosen after reviewing the refinement sheets)
FINAL = dict(periods=(0.5, 1), amp=8.5, amp_r=0.8, width=5.2, trans=math.pi / 4, x0=9, x1=55)


def build_final():
    svg_path = f'{OUT}/logo-mark.svg'
    with open(svg_path, 'w') as f:
        f.write(concept_a(**FINAL))
    im = render_svg(svg_path, f'{OUT}/logo-mark-256.png', 256, 256, bg=None)
    im.save(f'{OUT}/logo-mark-256.webp', 'WEBP', quality=82)
    im = render_svg(svg_path, f'{OUT}/logo-mark-512-dark.png', 512, 512, bg=INK)
    im.save(f'{OUT}/logo-mark-512-dark.webp', 'WEBP', quality=82)

    svg, width = wordmark_svg(FINAL)
    wm_path = f'{OUT}/wordmark.svg'
    with open(wm_path, 'w') as f:
        f.write(svg)
    # proof: wordmark in a 40 px navbar on ink, and the mark at 28 px on both grounds
    scale = 40.0 / 64.0
    ww = round(width * scale)
    html = f'''<!doctype html><meta charset="utf-8"><style>
body{{margin:0;background:#8a8f8d;width:760px;height:300px}}
.nav{{height:64px;background:{INK};display:flex;align-items:center;padding:0 24px;gap:40px;
     border-bottom:1px solid rgba(110,231,183,.18);font:500 16px Inter,Helvetica,Arial;color:#fff}}
.nav span{{margin-left:auto}} .white{{background:#fff;color:#1f2937}}
.big{{background:{INK};padding:16px 24px}}
</style><body>
<div class="nav"><img src="file://{wm_path}" height="40" width="{ww}"><span>Research&nbsp;&nbsp;&nbsp;People&nbsp;&nbsp;&nbsp;Publications</span></div>
<div class="nav white"><img src="file://{svg_path}" height="28" width="28"><b>Zhuo Lab</b><span>Research&nbsp;&nbsp;&nbsp;People</span></div>
<div class="big"><img src="file://{wm_path}" height="120" width="{round(width * 120 / 64)}"></div>
</body>'''
    html_path = f'{SCRATCH}/proof.html'
    with open(html_path, 'w') as f:
        f.write(html)
    chrome_shot(html_path, f'{CONCEPTS}/final-proof.png', 760, 300)


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'concepts'
    if what in ('concepts', 'all'):
        build_concepts()
    if what in ('refine', 'all'):
        build_refine()
    if what in ('refine3', 'all'):
        build_refine(REFINE3, 'refine3')
    if what in ('refine4', 'all'):
        build_refine(REFINE4, 'refine4')
    if what in ('final', 'all'):
        build_final()
    print('done')
