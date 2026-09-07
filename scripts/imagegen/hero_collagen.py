#!/usr/bin/env python3
"""
hero_collagen.py -- procedural second-harmonic-generation (SHG) micrograph of
collagen for the Zhuo Lab hero background.

Outputs (2400 x 1500 px, PNG + WebP):
  static/media/gen/hero-collagen.png         emerald intensity image
  static/media/gen/hero-collagen-orient.png  P-SHG style orientation map
                                             (hue = fibre angle, brightness = SHG)

Method
  * Collagen bundles are parametric curves in a bundle-local frame (u along,
    v across): slow meander + periodic crimp whose amplitude and phase drift
    along the bundle.  Each bundle is many fibrils at lateral offsets with
    their own drift, crimp-phase offset and amplitude; fibrils are grouped in
    sub-bundles across the width and appear as segments (they enter and leave
    the focal plane).
  * Fibrils are rasterised as additive Gaussian-profile strokes into a float32
    intensity buffer at 2x resolution, together with an orientation buffer that
    accumulates intensity-weighted (cos 2phi, sin 2phi) so crossings average
    like real axial data.
  * SHG intensity along a fibril = focal-plane window x fine texture x
    polarisation factor (cos^2 of the angle between the local fibre axis and
    the excitation polarisation) x out-of-plane tilt loss on crimp flanks, so
    crimp shows up as the periodic banding seen in tendon / dermis SHG.
  * Per-bundle Gaussian blur models defocus; a low-pass noise field plus a
    wide blur of the fibre image gives out-of-plane haze; Poisson shot noise,
    dark counts and faint scan-line gain ripple are added at final resolution.
  * Tone mapped with a gamma curve, mapped through the emerald LUT, and faded
    into the page ink (#04201c) on the left and the top/bottom edges so hero
    text can sit on the left.

Deterministic (fixed seed).  Run:  python3 scripts/imagegen/hero_collagen.py
Set HERO_PREVIEW_DIR=<dir> to also write 100 % QA crops.
"""
import math
import os
import time

import numpy as np
from scipy import ndimage
from PIL import Image

# --------------------------------------------------------------------------
# configuration
# --------------------------------------------------------------------------
W, H = 2400, 1500          # final size
SS = 2                     # supersampling factor
WS, HS = W * SS, H * SS
SEED = 20260907

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT_DIR = os.path.join(ROOT, "static", "media", "gen")
PREVIEW_DIR = os.environ.get("HERO_PREVIEW_DIR", "")   # optional crops for QA

INK = np.array([0x04, 0x20, 0x1c], dtype=np.float32) / 255.0
EMERALD_STOPS = [
    (0.00, "#03181a"),
    (0.30, "#0f5f52"),
    (0.60, "#10b981"),
    (0.84, "#6ee7b7"),
    (1.00, "#d1fae5"),
]
# cyclic map for the orientation image: a hue circle with moderate saturation
# and roughly even lightness (t = 0 and t = 1 are the same colour)
CYCLIC_STOPS = [
    (0.000, "#e6a94a"),
    (0.125, "#e5765a"),
    (0.250, "#d65a9c"),
    (0.375, "#9e6fe0"),
    (0.500, "#5b8ef0"),
    (0.625, "#2ab4c8"),
    (0.750, "#3fc27c"),
    (0.875, "#9fc04c"),
    (1.000, "#e6a94a"),
]

POL_ANGLE_DEG = -16.0      # excitation polarisation (image coords, y down)
POL_FLOOR = 0.20           # I = floor + (1-floor) cos^2(alpha)
TILT_LOSS = 0.62           # intensity loss at crimp flanks (out-of-plane tilt)
CRIMP_SCALE = 1.25         # global multiplier on crimp amplitude
FIBRIL_DENSITY = 1.15      # global multiplier on fibrils per bundle

# Bundle definitions (final-pixel units).  angle: direction of the bundle in
# image coordinates (y down), so negative = running lower-left to upper-right.
# ends: (u_start, u_end) relative to (x, y) for bundles that leave the focal
# plane inside the frame; None = spans the whole canvas.
BUNDLES = [
    # ---- main family: lower-left -> upper-right ----
    dict(x=1620, y=840, angle=-34, width=130, spacing=3.2, meander=90,
         crimp_lam=62, crimp_amp=3.2, blur=0.0, gain=1.00, ends=None),
    dict(x=1920, y=560, angle=-30, width=80, spacing=3.0, meander=70,
         crimp_lam=55, crimp_amp=2.8, blur=0.0, gain=0.92, ends=(-950, 750)),
    dict(x=1360, y=1210, angle=-38, width=100, spacing=3.3, meander=110,
         crimp_lam=70, crimp_amp=3.6, blur=1.3, gain=0.72, ends=None),
    dict(x=2110, y=340, angle=-37, width=64, spacing=3.1, meander=60,
         crimp_lam=48, crimp_amp=2.4, blur=3.5, gain=0.45, ends=None),
    dict(x=1150, y=650, angle=-31, width=170, spacing=3.5, meander=120,
         crimp_lam=75, crimp_amp=4.0, blur=9.0, gain=0.38, ends=None),
    dict(x=2250, y=1060, angle=-27, width=48, spacing=2.8, meander=50,
         crimp_lam=52, crimp_amp=2.2, blur=0.0, gain=0.80, ends=(-650, 520)),
    dict(x=1800, y=1330, angle=-33, width=72, spacing=3.1, meander=80,
         crimp_lam=58, crimp_amp=2.8, blur=2.2, gain=0.55, ends=None),
    # ---- crossing bundles ----
    dict(x=1750, y=950, angle=22, width=90, spacing=3.1, meander=90,
         crimp_lam=58, crimp_amp=2.8, blur=0.0, gain=0.85, ends=(-820, 900)),
    dict(x=1420, y=450, angle=-78, width=58, spacing=3.1, meander=70,
         crimp_lam=50, crimp_amp=2.2, blur=2.6, gain=0.55, ends=None),
    dict(x=2060, y=1250, angle=62, width=44, spacing=2.9, meander=55,
         crimp_lam=45, crimp_amp=2.0, blur=0.6, gain=0.70, ends=(-520, 600)),
    dict(x=1480, y=560, angle=-36, width=66, spacing=2.8, meander=70,
         crimp_lam=60, crimp_amp=2.6, blur=0.8, gain=0.72, ends=(-700, 800)),
    dict(x=2150, y=180, angle=-25, width=40, spacing=2.8, meander=60,
         crimp_lam=54, crimp_amp=2.2, blur=1.5, gain=0.50, ends=None),
    # ---- thin wisps ----
    dict(x=1500, y=300, angle=-20, width=16, spacing=2.8, meander=110,
         crimp_lam=50, crimp_amp=1.8, blur=0.0, gain=0.55, ends=(-700, 600)),
    dict(x=1700, y=1150, angle=-60, width=12, spacing=2.8, meander=90,
         crimp_lam=52, crimp_amp=1.8, blur=0.3, gain=0.45, ends=(-420, 520)),
    dict(x=2300, y=700, angle=-50, width=20, spacing=2.8, meander=80,
         crimp_lam=56, crimp_amp=2.0, blur=1.0, gain=0.50, ends=(-500, 700)),
    dict(x=1250, y=1000, angle=8, width=14, spacing=2.8, meander=120,
         crimp_lam=60, crimp_amp=1.8, blur=0.4, gain=0.45, ends=(-600, 500)),
]


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def hex_to_rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32) / 255.0


def build_lut(stops, n=2048):
    pos = np.array([p for p, _ in stops], dtype=np.float32)
    cols = np.stack([hex_to_rgb(c) for _, c in stops])
    t = np.linspace(0, 1, n, dtype=np.float32)
    lut = np.stack([np.interp(t, pos, cols[:, k]) for k in range(3)], axis=1)
    return lut.astype(np.float32)


def apply_lut(lut, t):
    idx = np.clip((t * (len(lut) - 1) + 0.5).astype(np.int32), 0, len(lut) - 1)
    return lut[idx]


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


class Series:
    """Sum of a few sinusoids with random wavelengths/phases: a cheap, smooth,
    deterministic 1-D random function with an analytic derivative."""

    def __init__(self, rng, n, lam_range, amp):
        self.l = rng.uniform(lam_range[0], lam_range[1], n).astype(np.float32)
        self.p = rng.uniform(0, 2 * np.pi, n).astype(np.float32)
        a = rng.uniform(0.4, 1.0, n)
        self.a = (amp * a / a.sum()).astype(np.float32)

    def __call__(self, u):
        out = np.zeros_like(u, dtype=np.float32)
        for l, p, a in zip(self.l, self.p, self.a):
            out += a * np.sin(2 * np.pi * u / l + p)
        return out

    def d(self, u):
        out = np.zeros_like(u, dtype=np.float32)
        for l, p, a in zip(self.l, self.p, self.a):
            out += a * (2 * np.pi / l) * np.cos(2 * np.pi * u / l + p)
        return out


def window(rng, grid, lam_range, floor, sharp=1.5, n=4):
    """Smooth 0..1 gating function along u (focal-plane in/out), on a grid."""
    s = Series(rng, n, lam_range, 1.0)
    g = s(grid)
    g = g / (np.abs(g).max() + 1e-6) * 1.6
    w = 0.5 + 0.5 * np.tanh(sharp * g)
    return floor + (1.0 - floor) * w


def downsample(a, f):
    h, w = a.shape[0] // f, a.shape[1] // f
    return a[:h * f, :w * f].reshape(h, f, w, f).mean(axis=(1, 3))


# --------------------------------------------------------------------------
# rasteriser
# --------------------------------------------------------------------------
def raster_bundle(b, rng, Xr, Yc, acc_I, acc_cx, acc_cy):
    th = math.radians(b["angle"])
    c, s = math.cos(th), math.sin(th)
    x0, y0 = b["x"], b["y"]
    # local frame over the whole canvas (float32, final px units)
    u = (Xr - x0) * c + (Yc - y0) * s
    v = -(Xr - x0) * s + (Yc - y0) * c

    umin, umax = float(u.min()), float(u.max())
    grid = np.arange(umin - 2, umax + 3, 1.0, dtype=np.float32)

    # centreline: slow meander
    meander = Series(rng, 3, (600, 1600), b["meander"])
    m_g, dm_g = meander(grid), meander.d(grid)
    vc = np.interp(u, grid, m_g).astype(np.float32)

    half = b["width"] / 2.0
    # width can breathe a bit along the bundle
    wmod_g = 1.0 + Series(rng, 2, (400, 1000), 0.20)(grid)
    wmod = np.interp(u, grid, wmod_g).astype(np.float32)

    strip = np.abs(v - vc) < (half * 1.3 + 10)
    if not strip.any():
        return
    rows = np.nonzero(strip.any(axis=1))[0]
    cols = np.nonzero(strip.any(axis=0))[0]
    r0, r1 = rows[0], rows[-1] + 1
    c0, c1 = cols[0], cols[-1] + 1
    sub = strip[r0:r1, c0:c1]
    uu = u[r0:r1, c0:c1][sub]
    vv = v[r0:r1, c0:c1][sub] - vc[r0:r1, c0:c1][sub]
    ww = wmod[r0:r1, c0:c1][sub]
    dvc = np.interp(uu, grid, dm_g).astype(np.float32)
    del u, v, vc, strip, wmod

    # crimp: phase drifts slowly (local wavelength varies) and the amplitude
    # has an envelope (crimped stretches alternate with straighter ones)
    lam, A = b["crimp_lam"], b["crimp_amp"] * CRIMP_SCALE
    ph0 = rng.uniform(0, 2 * np.pi)
    phmod = Series(rng, 3, (300, 900), 1.2)
    t = (2 * np.pi * uu / lam + ph0 + np.interp(uu, grid, phmod(grid))).astype(np.float32)
    dt_du = (2 * np.pi / lam + np.interp(uu, grid, phmod.d(grid))).astype(np.float32)
    cenv_g = window(rng, grid, (250, 700), 0.30, 1.3, n=3)
    cenv = np.interp(uu, grid, cenv_g).astype(np.float32)

    # bundle-level focal window and soft ends
    bwin_g = window(rng, grid, (400, 1200), 0.20, 1.6)
    if b["ends"] is not None:
        ua, ub = b["ends"]
        e = 0.5 * (1 + np.tanh((grid - ua) / 70.0)) * 0.5 * (1 - np.tanh((grid - ub) / 70.0))
        bwin_g = bwin_g * e
    bwin = np.interp(uu, grid, bwin_g).astype(np.float32)

    # fibrils across the width: sub-bundle clustering + soft lateral envelope
    spacing = b["spacing"] / FIBRIL_DENSITY
    n_fib = max(3, int(round(b["width"] / spacing)))
    offs = (np.arange(n_fib) - (n_fib - 1) / 2.0) * spacing
    offs = offs + rng.normal(0, 0.4 * spacing, n_fib)
    lat_lam = rng.uniform(18, 40)
    lat_ph = rng.uniform(0, 2 * np.pi)
    lat = 0.35 + 0.65 * (0.5 + 0.5 * np.sin(2 * np.pi * offs / lat_lam + lat_ph))
    edge = np.exp(-(offs / (0.78 * half + 1e-3)) ** 6)
    base = np.exp(rng.normal(0.0, 0.35, n_fib)) * lat * edge
    base = base.astype(np.float32)
    sig = rng.uniform(0.95, 1.5, n_fib).astype(np.float32)
    dph = rng.normal(0, 0.30, n_fib).astype(np.float32)
    dA = rng.normal(0, 0.15, n_fib).astype(np.float32)

    pol = math.radians(POL_ANGLE_DEG)
    I = np.zeros(uu.shape, dtype=np.float32)
    CX = np.zeros(uu.shape, dtype=np.float32)
    CY = np.zeros(uu.shape, dtype=np.float32)
    for i in range(n_fib):
        # lateral drift: most fibrils stay in the bundle, a few stray off it
        if rng.uniform() < 0.14:
            drift = Series(rng, 2, (500, 1300), rng.uniform(8.0, 22.0))
        else:
            drift = Series(rng, 3, (160, 600), rng.uniform(2.0, 6.0))
        # high-frequency wobble so fibrils are not perfectly parallel
        wob = Series(rng, 3, (25, 90), rng.uniform(0.4, 1.1))
        dr = np.interp(uu, grid, drift(grid) + wob(grid)).astype(np.float32)
        ddr = np.interp(uu, grid, drift.d(grid) + wob.d(grid)).astype(np.float32)
        # fibril segments: it drops in and out of the focal plane
        fwin_g = window(rng, grid, (90, 380), 0.05, 2.4)
        tex_g = 1.0 + 0.65 * Series(rng, 4, (8, 45), 1.0)(grid)
        amp_g = np.clip(fwin_g * tex_g, 0.0, None)
        amp = np.interp(uu, grid, amp_g).astype(np.float32)

        ti = t + dph[i]
        ai = A * (1.0 + dA[i]) * cenv
        vi = offs[i] * ww + dr + ai * np.sin(ti)
        slope_c = ai * dt_du * np.cos(ti)                 # crimp part of slope
        dvi = dvc + ddr + slope_c
        phi = th + np.arctan(dvi)                          # local fibre angle
        alpha = phi - pol
        pfac = POL_FLOOR + (1 - POL_FLOOR) * np.cos(alpha) ** 2
        # on crimp flanks fibrils tilt out of the focal plane -> darker bands
        rel = slope_c / (A * (1.0 + dA[i]) * (2 * np.pi / lam) + 1e-6)
        tilt = 1.0 - TILT_LOSS * np.clip(rel * rel, 0, 1)
        a_here = base[i] * bwin * amp * pfac * tilt
        g = np.exp(-0.5 * ((vv - vi) / sig[i]) ** 2)
        contrib = a_here * g
        I += contrib
        CX += contrib * np.cos(2 * phi)
        CY += contrib * np.sin(2 * phi)

    # place into bbox buffers, blur for defocus, add to accumulators
    for src, acc in ((I, acc_I), (CX, acc_cx), (CY, acc_cy)):
        buf = np.zeros(sub.shape, dtype=np.float32)
        buf[sub] = src
        sigma = 0.6 * SS + b["blur"] * SS    # small PSF blur even in focus
        buf = ndimage.gaussian_filter(buf, sigma, truncate=3.0)
        acc[r0:r1, c0:c1] += buf * b["gain"]


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    os.makedirs(OUT_DIR, exist_ok=True)

    Xr = ((np.arange(WS, dtype=np.float32) + 0.5) / SS)[None, :]
    Yc = ((np.arange(HS, dtype=np.float32) + 0.5) / SS)[:, None]
    acc_I = np.zeros((HS, WS), dtype=np.float32)
    acc_cx = np.zeros((HS, WS), dtype=np.float32)
    acc_cy = np.zeros((HS, WS), dtype=np.float32)

    for k, b in enumerate(BUNDLES):
        raster_bundle(b, rng, Xr, Yc, acc_I, acc_cx, acc_cy)
        print(f"bundle {k + 1}/{len(BUNDLES)} done  {time.time() - t0:5.1f}s", flush=True)

    # ---- down to final resolution ----
    I = downsample(acc_I, SS)
    CX = downsample(acc_cx, SS)
    CY = downsample(acc_cy, SS)
    del acc_I, acc_cx, acc_cy

    p = float(np.percentile(I, 99.85))
    I /= p
    CX /= p
    CY /= p

    # ---- haze: out-of-plane fibres + scattered light ----
    noise_lp = ndimage.gaussian_filter(rng.standard_normal((H, W)).astype(np.float32), 90)
    noise_lp = (noise_lp - noise_lp.min()) / (noise_lp.max() - noise_lp.min() + 1e-6)
    haze = 0.035 + 0.075 * noise_lp
    glow = ndimage.gaussian_filter(I, 24) * 0.25
    Itot = I + haze + glow

    # faint scan-line gain ripple (PMT / galvo)
    row = ndimage.gaussian_filter1d(rng.standard_normal(H).astype(np.float32), 1.2)
    Itot = Itot * (1.0 + 0.018 * row)[:, None]

    # ---- shot noise ----
    NPH = 40.0
    dark = 0.4
    counts = rng.poisson(np.clip(Itot, 0, None) * NPH + dark).astype(np.float32)
    In = counts / NPH + rng.normal(0, 0.012, (H, W)).astype(np.float32)
    In = np.clip(In, 0.0, 1.0)

    # ---- tone map ----
    T = In ** 0.72

    # ---- fade mask for hero text ----
    xs = (np.arange(W, dtype=np.float32) + 0.5) / W
    ys = (np.arange(H, dtype=np.float32) + 0.5) / H
    mx = smoothstep(0.30, 0.60, xs)[None, :]
    my = (smoothstep(0.0, 0.13, ys) * smoothstep(1.0, 0.86, ys))[:, None]
    M = (mx * my).astype(np.float32)
    TM = T * M

    # ---- emerald image ----
    lut = build_lut(EMERALD_STOPS)
    rgb = apply_lut(lut, TM)
    rgb = rgb + (INK - lut[0])[None, None, :] * (1.0 - M)[..., None]
    img = Image.fromarray(np.clip(rgb * 255 + 0.5, 0, 255).astype(np.uint8))
    img.save(os.path.join(OUT_DIR, "hero-collagen.png"), optimize=True)
    img.save(os.path.join(OUT_DIR, "hero-collagen.webp"), quality=82, method=6)
    print("wrote hero-collagen  ", f"{time.time() - t0:5.1f}s", flush=True)

    # ---- orientation map (P-SHG style) ----
    ang = 0.5 * np.arctan2(CY, CX)                       # (-pi/2, pi/2]
    hue = ((ang / np.pi) + 0.5) % 1.0
    coh = np.clip(np.sqrt(CX ** 2 + CY ** 2) / (I + 0.02), 0, 1)
    clut = build_lut(CYCLIC_STOPS)
    base = apply_lut(clut, hue)
    grey = np.array([0.55, 0.58, 0.57], dtype=np.float32)
    sat = (0.15 + 0.85 * coh)[..., None]
    col = grey[None, None, :] * (1.0 - sat) + base * sat
    V = np.clip(1.15 * TM ** 0.9 * (0.5 + 0.5 * coh), 0, 1)[..., None]   # haze stays dim
    dark0 = hex_to_rgb("#03181a")
    body = col * V + dark0[None, None, :] * (1.0 - V)
    rgb2 = body * M[..., None] + INK[None, None, :] * (1.0 - M)[..., None]
    img2 = Image.fromarray(np.clip(rgb2 * 255 + 0.5, 0, 255).astype(np.uint8))
    img2.save(os.path.join(OUT_DIR, "hero-collagen-orient.png"), optimize=True)
    img2.save(os.path.join(OUT_DIR, "hero-collagen-orient.webp"), quality=82, method=6)
    print("wrote hero-collagen-orient", f"{time.time() - t0:5.1f}s", flush=True)

    # ---- optional QA crops at 100 % ----
    if PREVIEW_DIR:
        os.makedirs(PREVIEW_DIR, exist_ok=True)
        img.crop((1450, 600, 2250, 1100)).save(os.path.join(PREVIEW_DIR, "crop-a.png"))
        img.crop((900, 900, 1700, 1400)).save(os.path.join(PREVIEW_DIR, "crop-b.png"))
        img2.crop((1450, 600, 2250, 1100)).save(os.path.join(PREVIEW_DIR, "crop-orient.png"))
        print("wrote QA crops", flush=True)


if __name__ == "__main__":
    main()
