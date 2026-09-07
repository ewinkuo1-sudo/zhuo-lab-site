#!/usr/bin/python3
"""Generate thumb-endoscope.svg (1200x800) and render it to PNG + WebP.

Technical illustration of a miniaturised fibre-based nonlinear endomicroscopy
probe imaging tissue. Deterministic (fixed seed). Rendered with headless
Chromium so that SVG filters (glows) are honoured, then converted with Pillow.
"""
import math
import pathlib
import random
import subprocess
import sys
import tempfile

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "static" / "media" / "gen"
OUT.mkdir(parents=True, exist_ok=True)
NAME = "thumb-endoscope"

W, H = 1200, 800
BG = "#04201c"
INK2 = "#062e28"
FOREST = "#064e3b"
GREEN = "#0f9d78"
MINT = "#6ee7b7"
MINT_SOFT = "#ecfdf5"
PALE = "#d1fae5"

# probe geometry (local frame: x along the probe axis, tip lens face at x=0)
TIP = (600.0, 460.0)
ANG = 38.0
FOCUS_X = 150.0
R_OUT = 60.0      # housing outer radius
R_IN = 52.0       # housing inner radius (wall thickness 8)
GRIN_L = 92.0     # GRIN rod lens length
GRIN_R = 34.0     # GRIN rod lens radius
FIB_TIP = -128.0  # fibre end face
PZ_X0, PZ_X1, PZ_R = -322.0, -208.0, 21.0  # piezo tube scanner
X_LEFT = -780.0   # far left (off canvas)
# tissue block (front = cross-section face), oblique extrusion vector
BX0, BX1, BY0, BY1 = 0.0, 760.0, -330.0, 490.0
EX, EY = -26.0, -36.0

rng = random.Random(20260907)


def f(v):
    return f"{v:.1f}"


def wavy_path(cx, cy, ang, length, amp, lam, ph, bend, bph):
    ux, uy = math.cos(ang), math.sin(ang)
    nx, ny = -uy, ux
    step = 5.0
    n = int(length / step)
    pts = []
    for i in range(n + 1):
        t = -length / 2 + i * step
        off = amp * math.sin(2 * math.pi * t / lam + ph) + bend * math.sin(math.pi * t / length + bph)
        pts.append((cx + t * ux + off * nx, cy + t * uy + off * ny))
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def collagen_paths():
    paths = []
    bundles = []
    for _ in range(20):
        bundles.append((rng.uniform(60, 640), rng.uniform(-320, 460), False))
    # bundles crossing the focal volume
    bundles.append((FOCUS_X + rng.uniform(-12, 12), rng.uniform(-30, 30), True))
    bundles.append((FOCUS_X + rng.uniform(-40, 40), rng.uniform(-20, 20), True))
    bundles.append((FOCUS_X + 30, rng.uniform(-60, 60), False))
    for (cx, cy, at_focus) in bundles:
        if at_focus or rng.random() < 0.75:
            ang = math.radians(90 + rng.uniform(-28, 28))
        else:
            ang = math.radians(rng.uniform(20, 160))
        length = rng.uniform(260, 520)
        amp = rng.uniform(4.0, 9.0)
        lam = rng.uniform(70, 130)
        bend = rng.uniform(6, 26)
        bph = rng.uniform(0, 2 * math.pi)
        ph = rng.uniform(0, 2 * math.pi)
        nf = rng.choice([3, 3, 4, 5])
        gap = rng.uniform(6.0, 9.0)
        nx, ny = -math.sin(ang), math.cos(ang)
        for k in range(nf):
            o = (k - (nf - 1) / 2) * gap
            paths.append(wavy_path(cx + o * nx, cy + o * ny, ang, length * rng.uniform(0.8, 1.0),
                                   amp * rng.uniform(0.8, 1.2), lam, ph + rng.uniform(-0.5, 0.5),
                                   bend, bph))
    return paths


def build_svg():
    p = []
    a = p.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
      f'aria-label="Fibre-based nonlinear endomicroscopy probe imaging collagen in tissue">')
    # ---------- defs ----------
    a("<defs>")
    a(f'<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">'
      f'<path d="M40 0H0V40" fill="none" stroke="#34d399" stroke-opacity="0.07" stroke-width="1"/></pattern>')
    a(f'<radialGradient id="vig" cx="{f(TIP[0])}" cy="{f(TIP[1])}" r="620" gradientUnits="userSpaceOnUse">'
      f'<stop offset="0" stop-color="{GREEN}" stop-opacity="0.10"/>'
      f'<stop offset="0.55" stop-color="{GREEN}" stop-opacity="0.03"/>'
      f'<stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></radialGradient>')
    # tissue block
    a('<linearGradient id="tissue" x1="0" y1="0" x2="640" y2="0" gradientUnits="userSpaceOnUse">'
      '<stop offset="0" stop-color="#0e4f40" stop-opacity="0.62"/>'
      '<stop offset="0.45" stop-color="#0a3d32" stop-opacity="0.55"/>'
      '<stop offset="1" stop-color="#06302a" stop-opacity="0.5"/></linearGradient>')
    a(f'<clipPath id="tclip"><rect x="{f(BX0)}" y="{f(BY0)}" width="{f(BX1 - BX0)}" height="{f(BY1 - BY0)}"/></clipPath>')
    a(f'<clipPath id="tclip2"><rect x="{f(BX0 + 30)}" y="{f(BY0)}" width="{f(BX1 - BX0 - 30)}" height="{f(BY1 - BY0)}"/></clipPath>')
    a(f'<clipPath id="lensclip"><rect x="{f(-GRIN_L)}" y="{f(-GRIN_R)}" width="{f(GRIN_L)}" height="{f(2 * GRIN_R)}"/></clipPath>')
    a(f'<radialGradient id="fmask" cx="{f(FOCUS_X)}" cy="0" r="95" gradientUnits="userSpaceOnUse">'
      '<stop offset="0" stop-color="#fff" stop-opacity="1"/>'
      '<stop offset="0.35" stop-color="#fff" stop-opacity="0.8"/>'
      '<stop offset="0.7" stop-color="#fff" stop-opacity="0.25"/>'
      '<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>')
    a('<mask id="focusmask" maskUnits="userSpaceOnUse" x="-100" y="-400" width="900" height="800">'
      '<rect x="-100" y="-400" width="900" height="800" fill="#000"/>'
      f'<circle cx="{f(FOCUS_X)}" cy="0" r="95" fill="url(#fmask)"/></mask>')
    # housing shading (across the cylinder)
    a('<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1">'
      '<stop offset="0" stop-color="#126352"/>'
      '<stop offset="0.3" stop-color="#0c4e3f"/>'
      '<stop offset="1" stop-color="#03201a"/></linearGradient>')
    a('<linearGradient id="lumen" x1="0" y1="0" x2="0" y2="1">'
      '<stop offset="0" stop-color="#0b4538"/>'
      '<stop offset="0.5" stop-color="#07332c"/>'
      '<stop offset="1" stop-color="#04231d"/></linearGradient>')
    a('<linearGradient id="grin" x1="0" y1="0" x2="0" y2="1">'
      '<stop offset="0" stop-color="#0a3d33" stop-opacity="0.9"/>'
      '<stop offset="0.5" stop-color="#2cc39c" stop-opacity="0.8"/>'
      '<stop offset="1" stop-color="#0a3d33" stop-opacity="0.9"/></linearGradient>')
    a('<linearGradient id="piezo" x1="0" y1="0" x2="0" y2="1">'
      '<stop offset="0" stop-color="#155e4c"/>'
      '<stop offset="0.5" stop-color="#0c4538"/>'
      '<stop offset="1" stop-color="#083227"/></linearGradient>')
    # beams
    a(f'<linearGradient id="exc" x1="{f(FIB_TIP)}" y1="0" x2="{f(FOCUS_X)}" y2="0" gradientUnits="userSpaceOnUse">'
      f'<stop offset="0" stop-color="{PALE}" stop-opacity="0.16"/>'
      f'<stop offset="0.45" stop-color="{PALE}" stop-opacity="0.2"/>'
      f'<stop offset="1" stop-color="{MINT_SOFT}" stop-opacity="0.55"/></linearGradient>')
    a(f'<linearGradient id="exc2" x1="{f(FOCUS_X)}" y1="0" x2="{f(FOCUS_X + 130)}" y2="0" gradientUnits="userSpaceOnUse">'
      f'<stop offset="0" stop-color="{MINT_SOFT}" stop-opacity="0.4"/>'
      f'<stop offset="1" stop-color="{MINT_SOFT}" stop-opacity="0"/></linearGradient>')
    a(f'<linearGradient id="ret" x1="{f(FOCUS_X)}" y1="0" x2="0" y2="0" gradientUnits="userSpaceOnUse">'
      '<stop offset="0" stop-color="#34d399" stop-opacity="0.42"/>'
      '<stop offset="1" stop-color="#34d399" stop-opacity="0.1"/></linearGradient>')
    a(f'<linearGradient id="retfib" x1="{f(FIB_TIP)}" y1="0" x2="{f(X_LEFT)}" y2="0" gradientUnits="userSpaceOnUse">'
      '<stop offset="0" stop-color="#34d399" stop-opacity="0.16"/>'
      '<stop offset="1" stop-color="#34d399" stop-opacity="0.03"/></linearGradient>')
    a('<radialGradient id="pulse" cx="0.5" cy="0.5" r="0.5">'
      '<stop offset="0" stop-color="#ffffff" stop-opacity="1"/>'
      '<stop offset="0.45" stop-color="#d1fae5" stop-opacity="0.9"/>'
      '<stop offset="1" stop-color="#6ee7b7" stop-opacity="0"/></radialGradient>')
    a('<radialGradient id="spot" cx="0.5" cy="0.5" r="0.5">'
      '<stop offset="0" stop-color="#ffffff" stop-opacity="1"/>'
      '<stop offset="0.5" stop-color="#d1fae5" stop-opacity="0.9"/>'
      '<stop offset="1" stop-color="#34d399" stop-opacity="0"/></radialGradient>')
    a('<filter id="glow" x="-40%" y="-40%" width="180%" height="180%">'
      '<feGaussianBlur stdDeviation="3" result="b"/>'
      '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    a('<filter id="blur6" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6"/></filter>')
    a('<filter id="blur12" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="12"/></filter>')
    a('<filter id="blur26" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="26"/></filter>')
    a('<g id="fibres">')
    for d in collagen_paths():
        a(f'<path d="{d}"/>')
    a('</g>')
    a("</defs>")

    # ---------- background ----------
    a(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    a(f'<rect width="{W}" height="{H}" fill="url(#grid)"/>')
    a(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')

    # ---------- rotated probe frame ----------
    a(f'<g transform="translate({f(TIP[0])} {f(TIP[1])}) rotate({f(ANG)})">')

    # axis line (engineering centre line)
    a(f'<line x1="{f(X_LEFT - 200)}" y1="0" x2="{f(FOCUS_X + 330)}" y2="0" stroke="{MINT}" stroke-opacity="0.22" '
      'stroke-width="1" stroke-dasharray="22 8 4 8"/>')

    # ----- tissue block -----
    # oblique faces: tissue surface (left) and top
    surf = (f'{f(BX0)},{f(BY0)} {f(BX0)},{f(BY1)} {f(BX0 + EX)},{f(BY1 + EY)} {f(BX0 + EX)},{f(BY0 + EY)}')
    topf = (f'{f(BX0)},{f(BY0)} {f(BX1)},{f(BY0)} {f(BX1 + EX)},{f(BY0 + EY)} {f(BX0 + EX)},{f(BY0 + EY)}')
    a(f'<polygon points="{surf}" fill="#1c7d64" fill-opacity="0.42"/>')
    a(f'<polygon points="{topf}" fill="#15654f" fill-opacity="0.36"/>')
    a(f'<rect x="{f(BX0)}" y="{f(BY0)}" width="{f(BX1 - BX0)}" height="{f(BY1 - BY0)}" fill="url(#tissue)"/>')
    a('<g clip-path="url(#tclip)">')
    a(f'<rect x="{f(BX0)}" y="{f(BY0)}" width="30" height="{f(BY1 - BY0)}" fill="#14634f" fill-opacity="0.3"/>')
    a('</g>')
    a(f'<g clip-path="url(#tclip2)" fill="none" stroke-linecap="round" stroke-linejoin="round">')
    a(f'<g stroke="{GREEN}" stroke-opacity="0.3" stroke-width="2.2"><use href="#fibres" xlink:href="#fibres"/></g>')
    # bright fibres near the focus (SHG)
    a('<g mask="url(#focusmask)">')
    a('<g stroke="#34d399" stroke-opacity="0.5" stroke-width="9" filter="url(#blur6)"><use href="#fibres" xlink:href="#fibres"/></g>')
    a('<g stroke="#a7f3d0" stroke-opacity="0.95" stroke-width="2.6" filter="url(#glow)"><use href="#fibres" xlink:href="#fibres"/></g>')
    a("</g>")
    a("</g>")
    a(f'<g fill="none" stroke="{MINT}" stroke-opacity="0.34" stroke-width="1.6" stroke-linejoin="round">'
      f'<rect x="{f(BX0)}" y="{f(BY0)}" width="{f(BX1 - BX0)}" height="{f(BY1 - BY0)}"/>'
      f'<polygon points="{surf}"/><polygon points="{topf}"/></g>')

    # ----- returning SHG signal cone (focus -> lens face) -----

    # ----- excitation beam (fibre tip -> GRIN -> focus) -----
    ya = 13.0   # half height at GRIN entrance
    yb = GRIN_R - 10.0  # half height at GRIN exit
    top = (f'M{f(FIB_TIP)} 0 L{f(-GRIN_L)} {f(-ya)} C{f(-GRIN_L + 30)} {f(-ya - 14)} {f(-40)} {f(-yb - 8)} 0 {f(-yb)} '
           f'L{f(FOCUS_X)} 0')
    bot = (f'L0 {f(yb)} C{f(-40)} {f(yb + 8)} {f(-GRIN_L + 30)} {f(ya + 14)} {f(-GRIN_L)} {f(ya)} Z')
    a(f'<path d="{top} {bot}" fill="url(#exc)"/>')
    a(f'<polygon points="{f(FOCUS_X)},0 {f(FOCUS_X + 130)},-24 {f(FOCUS_X + 130)},24" fill="url(#exc2)"/>')
    # marginal rays (thin) and central ray
    a(f'<path d="{top}" fill="none" stroke="{MINT_SOFT}" stroke-opacity="0.55" stroke-width="1"/>')
    a(f'<path d="M{f(FIB_TIP)} 0 L{f(-GRIN_L)} {f(ya)} C{f(-GRIN_L + 30)} {f(ya + 14)} {f(-40)} {f(yb + 8)} 0 {f(yb)} '
      f'L{f(FOCUS_X)} 0" fill="none" stroke="{MINT_SOFT}" stroke-opacity="0.55" stroke-width="1"/>')
    a(f'<line x1="{f(FIB_TIP)}" y1="0" x2="{f(FOCUS_X + 60)}" y2="0" stroke="{MINT_SOFT}" stroke-opacity="0.35" stroke-width="1"/>')

    # ----- returning SHG signal cone (focus -> lens face) -----
    a(f'<polygon points="{f(FOCUS_X)},0 0,{f(-GRIN_R + 1)} 0,{f(GRIN_R - 1)}" fill="url(#ret)"/>')
    a(f'<g fill="none" stroke="#34d399" stroke-opacity="0.5" stroke-width="1" stroke-dasharray="5 5">'
      f'<line x1="{f(FOCUS_X)}" y1="0" x2="0" y2="{f(-GRIN_R + 1)}"/>'
      f'<line x1="{f(FOCUS_X)}" y1="0" x2="0" y2="{f(GRIN_R - 1)}"/></g>')

    # ----- scan field (imaging plane) through the focus -----
    a(f'<g stroke="{MINT}" stroke-opacity="0.4" stroke-width="1">'
      f'<line x1="{f(FOCUS_X)}" y1="-78" x2="{f(FOCUS_X)}" y2="78" stroke-dasharray="3 5"/>'
      f'<line x1="{f(FOCUS_X - 6)}" y1="-78" x2="{f(FOCUS_X + 6)}" y2="-78"/>'
      f'<line x1="{f(FOCUS_X - 6)}" y1="78" x2="{f(FOCUS_X + 6)}" y2="78"/></g>')

    # ----- focal spot -----
    a(f'<ellipse cx="{f(FOCUS_X)}" cy="0" rx="70" ry="42" fill="#10b981" fill-opacity="0.35" filter="url(#blur26)"/>')
    a(f'<ellipse cx="{f(FOCUS_X)}" cy="0" rx="34" ry="14" fill="#34d399" fill-opacity="0.6" filter="url(#blur12)"/>')
    a(f'<ellipse cx="{f(FOCUS_X)}" cy="0" rx="16" ry="5.5" fill="url(#spot)" filter="url(#glow)"/>')

    # ----- probe housing (cutaway) -----
    a(f'<rect x="{f(X_LEFT)}" y="{f(-R_OUT)}" width="{f(-X_LEFT)}" height="{f(2 * R_OUT)}" rx="4" fill="url(#wall)"/>')
    a(f'<rect x="{f(X_LEFT)}" y="{f(-R_IN)}" width="{f(-X_LEFT - GRIN_L - 10)}" height="{f(2 * R_IN)}" fill="url(#lumen)"/>')
    # lens holder / ferrule at the tip
    a(f'<rect x="{f(-GRIN_L - 10)}" y="{f(-R_IN)}" width="{f(GRIN_L + 10)}" height="{f(2 * R_IN)}" fill="#0e5544"/>')
    a(f'<line x1="{f(-GRIN_L - 10)}" y1="{f(-R_IN)}" x2="{f(-GRIN_L - 10)}" y2="{f(R_IN)}" stroke="{MINT}" stroke-opacity="0.45" stroke-width="1"/>')
    # inner wall lines
    a(f'<g stroke="{MINT}" stroke-opacity="0.4" stroke-width="1">'
      f'<line x1="{f(X_LEFT)}" y1="{f(-R_IN)}" x2="{f(-GRIN_L - 10)}" y2="{f(-R_IN)}"/>'
      f'<line x1="{f(X_LEFT)}" y1="{f(R_IN)}" x2="{f(-GRIN_L - 10)}" y2="{f(R_IN)}"/></g>')

    # ----- piezo leads (wiring) -----
    a(f'<g fill="none" stroke="{MINT}" stroke-opacity="0.4" stroke-width="1">'
      f'<path d="M{f(PZ_X0)} -14 L{f(PZ_X0 - 30)} -40 L{f(X_LEFT)} -40"/>'
      f'<path d="M{f(PZ_X0)} 14 L{f(PZ_X0 - 30)} 40 L{f(X_LEFT)} 40"/></g>')

    # ----- double-clad fibre -----
    a(f'<rect x="{f(X_LEFT)}" y="-15" width="{f(PZ_X0 - 30 - X_LEFT)}" height="30" fill="#0a4437" fill-opacity="0.9"/>')
    a(f'<rect x="{f(X_LEFT)}" y="-15" width="{f(PZ_X0 - 30 - X_LEFT)}" height="30" fill="none" stroke="{MINT}" stroke-opacity="0.5" stroke-width="1"/>')
    a(f'<rect x="{f(X_LEFT)}" y="-10" width="{f(FIB_TIP - X_LEFT)}" height="20" fill="#137058" fill-opacity="0.9"/>')
    a(f'<rect x="{f(X_LEFT)}" y="-10" width="{f(FIB_TIP - X_LEFT)}" height="20" fill="url(#retfib)"/>')
    a(f'<g fill="none" stroke="{MINT}" stroke-width="1.3">'
      f'<rect x="{f(X_LEFT)}" y="-10" width="{f(FIB_TIP - X_LEFT)}" height="20" stroke-opacity="0.75"/>'
      f'<line x1="{f(X_LEFT)}" y1="-5.5" x2="{f(FIB_TIP)}" y2="-5.5" stroke-opacity="0.35"/>'
      f'<line x1="{f(X_LEFT)}" y1="5.5" x2="{f(FIB_TIP)}" y2="5.5" stroke-opacity="0.35"/></g>')
    # core with excitation light
    a(f'<line x1="{f(X_LEFT)}" y1="0" x2="{f(FIB_TIP)}" y2="0" stroke="{MINT}" stroke-opacity="0.5" stroke-width="5" filter="url(#blur6)"/>')
    a(f'<line x1="{f(X_LEFT)}" y1="0" x2="{f(FIB_TIP)}" y2="0" stroke="{PALE}" stroke-opacity="0.7" stroke-width="1.8"/>')
    # cantilever scan ghosts
    a(f'<g fill="none" stroke="{MINT}" stroke-opacity="0.4" stroke-width="1" stroke-dasharray="4 4">'
      f'<path d="M{f(PZ_X1)} -10 Q{f(PZ_X1 + 60)} -10 {f(FIB_TIP)} -24"/>'
      f'<path d="M{f(PZ_X1)} 10 Q{f(PZ_X1 + 60)} 10 {f(FIB_TIP)} 24"/></g>')
    # scan arrow at the fibre tip
    ax = FIB_TIP + 8
    a(f'<g stroke="{MINT}" stroke-opacity="0.6" stroke-width="1" fill="{MINT}" fill-opacity="0.6">'
      f'<line x1="{f(ax)}" y1="-30" x2="{f(ax)}" y2="30"/>'
      f'<polygon points="{f(ax - 3.5)},-27 {f(ax + 3.5)},-27 {f(ax)},-35"/>'
      f'<polygon points="{f(ax - 3.5)},27 {f(ax + 3.5)},27 {f(ax)},35"/></g>')

    # ----- piezo tube scanner -----
    a(f'<rect x="{f(PZ_X0)}" y="{f(-PZ_R)}" width="{f(PZ_X1 - PZ_X0)}" height="{f(2 * PZ_R)}" rx="4" fill="url(#piezo)"/>')
    a(f'<rect x="{f(PZ_X0)}" y="{f(-PZ_R)}" width="{f(PZ_X1 - PZ_X0)}" height="{f(2 * PZ_R)}" rx="4" fill="none" stroke="{MINT}" stroke-opacity="0.85" stroke-width="1.5"/>')
    a(f'<g stroke="{MINT}" stroke-opacity="0.35" stroke-width="1">'
      f'<line x1="{f(PZ_X0 + 8)}" y1="-9" x2="{f(PZ_X1 - 8)}" y2="-9"/>'
      f'<line x1="{f(PZ_X0 + 8)}" y1="9" x2="{f(PZ_X1 - 8)}" y2="9"/></g>')

    # ----- GRIN lens -----
    a(f'<rect x="{f(-GRIN_L)}" y="{f(-GRIN_R)}" width="{f(GRIN_L)}" height="{f(2 * GRIN_R)}" rx="3" fill="url(#grin)"/>')
    a(f'<rect x="{f(-GRIN_L)}" y="{f(-GRIN_R)}" width="{f(GRIN_L)}" height="{f(2 * GRIN_R)}" rx="3" fill="none" stroke="{MINT}" stroke-opacity="0.9" stroke-width="1.6"/>')

    # ----- beam inside the lens region (drawn above the lens) -----
    a(f'<path d="{top} {bot}" fill="url(#exc)" clip-path="url(#lensclip)"/>')

    # ----- femtosecond pulses in the core -----
    for x in (-650.0, -505.0, -360.0, -168.0):
        a(f'<ellipse cx="{f(x)}" cy="0" rx="20" ry="8" fill="{MINT}" fill-opacity="0.7" filter="url(#blur6)"/>')
        a(f'<ellipse cx="{f(x)}" cy="0" rx="11" ry="3.4" fill="url(#pulse)"/>')
    # returning SHG marks in the inner cladding (travelling back)
    for x, y in ((-440.0, -7.0), (-590.0, 7.0), (-720.0, -7.0)):
        a(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="7" ry="2.4" fill="#34d399" fill-opacity="0.75" filter="url(#glow)"/>')

    # ----- housing highlight (cylinder) -----
    a(f'<line x1="{f(X_LEFT)}" y1="{f(-R_OUT + 4)}" x2="{f(-4)}" y2="{f(-R_OUT + 4)}" stroke="#a7f3d0" stroke-opacity="0.22" stroke-width="2"/>')
    # ----- housing outline -----
    a(f'<rect x="{f(X_LEFT)}" y="{f(-R_OUT)}" width="{f(-X_LEFT)}" height="{f(2 * R_OUT)}" rx="4" fill="none" stroke="{MINT}" stroke-opacity="0.9" stroke-width="2"/>')

    a("</g>")  # end rotated frame
    a("</svg>")
    return "\n".join(p)


def render(svg_text):
    svg_path = OUT / f"{NAME}.svg"
    png_path = OUT / f"{NAME}.png"
    webp_path = OUT / f"{NAME}.webp"
    svg_path.write_text(svg_text)

    tmp = pathlib.Path(tempfile.mkdtemp(prefix="thumb-endoscope-"))
    html = tmp / "page.html"
    html.write_text(
        "<!doctype html><html><head><meta charset='utf-8'><style>"
        f"html,body{{margin:0;padding:0;background:{BG};overflow:hidden}}svg{{display:block}}"
        "</style></head><body>" + svg_text + "</body></html>")
    chrome = (pathlib.Path.home() / "Library/Caches/ms-playwright/chromium_headless_shell-1223/"
              "chrome-headless-shell-mac-arm64/chrome-headless-shell")
    cmd = [str(chrome), "--headless", "--no-sandbox", "--hide-scrollbars", "--disable-gpu",
           "--force-device-scale-factor=1", f"--window-size={W},{H}", "--virtual-time-budget=5000",
           f"--screenshot={png_path}", f"file://{html}"]
    subprocess.run(cmd, check=True, capture_output=True, timeout=120)

    im = Image.open(png_path).convert("RGB")
    if im.size != (W, H):
        im = im.crop((0, 0, W, H))
        im.save(png_path, optimize=True)
    im.save(webp_path, "WEBP", quality=82, method=6)

    # small preview for legibility checks (not shipped)
    preview_dir = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else tmp
    preview_dir.mkdir(parents=True, exist_ok=True)
    im.resize((300, 200), Image.LANCZOS).save(preview_dir / f"{NAME}-300.png")
    print(svg_path)
    print(png_path)
    print(webp_path)
    print(preview_dir / f"{NAME}-300.png")


if __name__ == "__main__":
    render(build_svg())
