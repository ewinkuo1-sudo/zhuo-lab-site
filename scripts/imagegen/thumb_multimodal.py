#!/usr/bin/env python3
"""
thumb-multimodal.png  (1200x800, + .webp)

Synthetic three-channel nonlinear-microscopy composite of an unstained tissue
section, rendered as it would come off a multiphoton scanner:

  * SHG   (green)  - wavy, crimped collagen bundles of the stroma, traced as
                     streamlines through a smooth orientation field that turns
                     parallel to the epithelial boundary
  * TPEF  (amber)  - autofluorescent epithelium: packed roundish cells with dark
                     nuclei and granular cytoplasm, plus a few stromal fibroblasts
  * CARS  (orange) - sparse lipid droplets, some clustered

Followed by an acquisition model: PSF blur, out-of-focus haze, vignetting,
illumination unevenness, scan-line gain jitter, Poisson shot noise, read noise
and 8-bit quantisation per channel.  Channels are colour-mapped and summed on
black.  Fully deterministic (fixed seed).
"""
import os
import numpy as np
from scipy import ndimage as ndi
from scipy.spatial import cKDTree
from PIL import Image

W, H = 1200, 800
SEED = 20260907
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "static", "media", "gen")
PREVIEW_DIR = "/private/tmp/claude-501/-Users-ewinkuo/4872956d-47a4-419b-a303-3950b431e40b/scratchpad"
rng = np.random.default_rng(SEED)

yy, xx = np.mgrid[0:H, 0:W]
yy = yy.astype(np.float32)
xx = xx.astype(np.float32)


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
def smooth_noise(shape, sigma):
    n = rng.standard_normal(shape).astype(np.float32)
    n = ndi.gaussian_filter(n, sigma)
    n /= n.std() + 1e-9
    return n


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def splat(acc, px, py, sig, amp, step, R=7):
    """Accumulate Gaussian cross-section line samples into acc.
    Normalised so that a line of samples spaced `step` px apart has peak ~amp."""
    Hh, Ww = acc.shape
    ix = np.floor(px).astype(np.int64)
    iy = np.floor(py).astype(np.int64)
    fx = px - ix
    fy = py - iy
    norm = amp * step / (np.sqrt(2 * np.pi) * sig)
    inv = 1.0 / (2.0 * sig * sig)
    flat = np.zeros(Hh * Ww, dtype=np.float64)
    for dy in range(-R, R + 2):
        ddy = dy - fy
        Y = iy + dy
        for dx in range(-R, R + 2):
            ddx = dx - fx
            X = ix + dx
            w = norm * np.exp(-(ddx * ddx + ddy * ddy) * inv)
            ok = (X >= 0) & (X < Ww) & (Y >= 0) & (Y < Hh) & (w > 1e-4)
            if not ok.any():
                continue
            flat += np.bincount(Y[ok] * Ww + X[ok], w[ok], minlength=Hh * Ww)
    acc += flat.reshape(Hh, Ww).astype(np.float32)


def ellipse_field(cx, cy, a, b, ang, x, y):
    """Normalised radial coordinate of an ellipse (1 at the rim)."""
    c, s = np.cos(ang), np.sin(ang)
    u = (x - cx) * c + (y - cy) * s
    v = -(x - cx) * s + (y - cy) * c
    return np.sqrt((u / a) ** 2 + (v / b) ** 2)


def add_soft_ellipse(acc, cx, cy, a, b, ang, amp, edge=0.12, nucleus=None):
    r = int(max(a, b) * 1.4) + 3
    x0, x1 = max(0, int(cx) - r), min(W, int(cx) + r + 1)
    y0, y1 = max(0, int(cy) - r), min(H, int(cy) + r + 1)
    if x1 <= x0 or y1 <= y0:
        return
    xs = xx[y0:y1, x0:x1]
    ys = yy[y0:y1, x0:x1]
    d = ellipse_field(cx, cy, a, b, ang, xs, ys)
    body = smoothstep(1.0 + edge, 1.0 - edge, d)
    if nucleus is not None:
        na, nb, nang, ndark = nucleus
        dn = ellipse_field(cx, cy, na, nb, nang, xs, ys)
        body = body * (1.0 - ndark * smoothstep(1.2, 0.8, dn))
    acc[y0:y1, x0:x1] += amp * body


# ----------------------------------------------------------------------------
# 1. tissue geometry: epithelium occupies the right ~third, wavy boundary
# ----------------------------------------------------------------------------
ys_line = np.arange(-120, H + 120, dtype=np.float32)
bn = ndi.gaussian_filter(rng.standard_normal(ys_line.size), 28)
bn /= bn.std()
xb_line = (800 + 70 * np.sin(2 * np.pi * ys_line / 560 + 0.9)
           + 32 * np.sin(2 * np.pi * ys_line / 205 + 2.1) + 28 * bn)
xb_line += 75 * np.exp(-((ys_line - 300) / 62) ** 2)   # stromal papilla
xb_line -= 65 * np.exp(-((ys_line - 630) / 58) ** 2)   # rete ridge
xb_line = ndi.gaussian_filter(xb_line, 6)
xb = np.interp(np.arange(H, dtype=np.float32), ys_line, xb_line).astype(np.float32)
dxb = np.gradient(xb)

epi = xx > xb[:, None]
dist_out = ndi.distance_transform_edt(~epi).astype(np.float32)   # stroma -> boundary
dist_in = ndi.distance_transform_edt(epi).astype(np.float32)     # epithelium -> boundary
epi_frac = epi.mean()

# boundary tangent angle (axial), broadcast per row
theta_t = np.arctan2(1.0, dxb).astype(np.float32)[:, None] * np.ones((1, W), np.float32)

# ----------------------------------------------------------------------------
# 2. collagen orientation field  (axial angles, blended via doubled angles)
# ----------------------------------------------------------------------------
theta0 = -0.45 + 0.55 * smooth_noise((H, W), 70) + 0.38 * smooth_noise((H, W), 18)
wgt = np.exp(-dist_out / 110.0)


def blend_axial(theta_a, theta_b, w):
    c2 = (1 - w) * np.cos(2 * theta_a) + w * np.cos(2 * theta_b)
    s2 = (1 - w) * np.sin(2 * theta_a) + w * np.sin(2 * theta_b)
    return 0.5 * np.arctan2(s2, c2)


theta_field = blend_axial(theta0, theta_t, wgt)
# a second, crossing fibre family (basket-weave), weaker near the boundary
theta_cross = blend_axial(theta0 + 0.95 + 0.3 * smooth_noise((H, W), 40), theta_t, wgt * 0.7)
FIELDS = [(np.cos(2 * theta_field).astype(np.float32), np.sin(2 * theta_field).astype(np.float32)),
          (np.cos(2 * theta_cross).astype(np.float32), np.sin(2 * theta_cross).astype(np.float32))]
cos2, sin2 = FIELDS[0]
epi_f = epi.astype(np.float32)
POL = 0.35   # laser polarisation angle for SHG intensity modulation
# collagen-rich vs collagen-poor regions of the stroma
density = 0.4 + 0.6 * smoothstep(-1.2, 0.8, smooth_noise((H, W), 95) + 0.5 * smooth_noise((H, W), 35))
density = np.maximum(density, np.exp(-dist_out / 70.0))


def sample(field, x, y):
    return ndi.map_coordinates(field, [[y], [x]], order=1, mode='nearest')[0]


def trace(p0, length, step=1.5, fam=0):
    """Trace an axial-field streamline in both directions from p0."""
    c2f, s2f = FIELDS[fam]
    halves = []
    for sgn in (1.0, -1.0):
        pts = []
        p = np.array(p0, dtype=np.float64)
        prev = None
        n_steps = int(length / 2 / step)
        for _ in range(n_steps):
            if not (-30 <= p[0] < W + 30 and -30 <= p[1] < H + 30):
                break
            if sample(epi_f, p[0], p[1]) > 0.5:
                break
            th = 0.5 * np.arctan2(sample(s2f, p[0], p[1]), sample(c2f, p[0], p[1]))
            d = np.array([np.cos(th), np.sin(th)])
            if prev is None:
                d = d * sgn
            elif np.dot(d, prev) < 0:
                d = -d
            prev = d
            pts.append(p.copy())
            p = p + step * d
        halves.append(pts)
    back = halves[1][::-1]
    pts = back + halves[0][1:] if halves[0] else back
    return np.array(pts) if len(pts) > 6 else None


# ----------------------------------------------------------------------------
# 3. SHG channel: collagen bundles
# ----------------------------------------------------------------------------
shg = np.zeros((H, W), np.float32)
shg_oof = np.zeros((H, W), np.float32)   # out-of-focus fibres

STEP = 1.5
n_bundles = 0
attempts = 0
# collect all fibre samples then splat in a few sigma buckets
samples = {'x': [], 'y': [], 'sig': [], 'amp': []}
oof_samples = {'x': [], 'y': [], 'sig': [], 'amp': []}

while n_bundles < 420 and attempts < 8000:
    attempts += 1
    x0 = rng.uniform(-20, W + 20)
    y0 = rng.uniform(-20, H + 20)
    xi, yi = int(np.clip(x0, 0, W - 1)), int(np.clip(y0, 0, H - 1))
    if epi[yi, xi]:
        continue
    if rng.random() > density[yi, xi]:
        continue
    # denser, more parallel collagen right under the epithelium
    near = np.exp(-dist_out[yi, xi] / 90.0)
    fam = 1 if (rng.random() < 0.18 * (1 - 0.6 * near)) else 0
    length = rng.uniform(130, 460) * (1.0 + 0.4 * near)
    path = trace((x0, y0), length, STEP, fam=fam)
    if path is None:
        continue
    n_bundles += 1
    seg = np.diff(path, axis=0)
    seg = np.vstack([seg, seg[-1:]])
    dnorm = seg / (np.linalg.norm(seg, axis=1, keepdims=True) + 1e-9)
    nrm = np.stack([-dnorm[:, 1], dnorm[:, 0]], axis=1)
    s = np.arange(len(path)) * STEP
    th_local = np.arctan2(dnorm[:, 1], dnorm[:, 0])
    # SHG polarisation dependence + intensity fluctuation along the bundle
    pol = 0.30 + 0.70 * np.cos(th_local - POL) ** 2
    fluct = ndi.gaussian_filter1d(rng.standard_normal(len(path)), 14)
    fluct = np.clip(1.0 + 0.5 * fluct / (fluct.std() + 1e-9), 0.15, 2.2)
    taper = smoothstep(0, 20, s) * smoothstep(s[-1], s[-1] - 20, s)
    base_amp = (0.28 + 0.72 * rng.random() ** 1.5) * (0.85 + 0.25 * near) * (0.75 if fam else 1.0)
    k = rng.integers(1, 6)                     # fibres per bundle
    spread = 2.2 * (k - 1) + rng.uniform(0, 3)
    crimped = rng.random() < 0.7
    lam = rng.uniform(16, 44)                  # crimp wavelength
    A = (rng.uniform(1.5, 6.0) if crimped else rng.uniform(0, 0.8)) * (0.7 + 0.3 * near)
    phase0 = rng.uniform(0, 2 * np.pi)
    is_oof = rng.random() < 0.2
    for j in range(k):
        off = (j - (k - 1) / 2) * (spread / max(k - 1, 1)) if k > 1 else 0.0
        crimp = A * np.sin(2 * np.pi * s / lam + phase0 + 0.12 * j)
        pts = path + nrm * (off + crimp)[:, None]
        width = rng.uniform(1.4, 4.4)          # FWHM px
        sig = width / 2.355
        amp = base_amp * rng.uniform(0.7, 1.2) * pol * fluct * taper
        tgt = oof_samples if is_oof else samples
        tgt['x'].append(pts[:, 0]); tgt['y'].append(pts[:, 1])
        tgt['sig'].append(np.full(len(pts), sig)); tgt['amp'].append(amp)

# fine, faint fibrils filling the stroma
for _ in range(260):
    x0 = rng.uniform(0, W); y0 = rng.uniform(0, H)
    if epi[int(y0), int(x0)] or rng.random() > 0.2 + 0.8 * density[int(y0), int(x0)]:
        continue
    path = trace((x0, y0), rng.uniform(50, 180), STEP, fam=int(rng.random() < 0.4))
    if path is None:
        continue
    s = np.arange(len(path)) * STEP
    taper = smoothstep(0, 12, s) * smoothstep(s[-1], s[-1] - 12, s)
    amp = rng.uniform(0.12, 0.32) * taper
    samples['x'].append(path[:, 0]); samples['y'].append(path[:, 1])
    samples['sig'].append(np.full(len(path), 0.75)); samples['amp'].append(amp)


def splat_bucketed(acc, S, step, blur=None):
    x = np.concatenate(S['x']); y = np.concatenate(S['y'])
    sg = np.concatenate(S['sig']); am = np.concatenate(S['amp'])
    edges = np.quantile(sg, [0, 0.25, 0.5, 0.75, 1.0])
    for i in range(4):
        m = (sg >= edges[i]) & (sg <= edges[i + 1] if i == 3 else sg < edges[i + 1])
        if not m.any():
            continue
        sig = float(np.median(sg[m]))
        R = int(np.ceil(3.2 * sig)) + 1
        splat(acc, x[m], y[m], sig, am[m], step, R=max(R, 3))


splat_bucketed(shg, samples, STEP)
splat_bucketed(shg_oof, oof_samples, STEP)
shg_oof = ndi.gaussian_filter(shg_oof, 4.0) * 0.4
shg = shg + shg_oof
# collagen is absent in epithelium, but its fibres press right up to the boundary
shg *= (1.0 - 0.97 * smoothstep(-1.0, 4.0, dist_in))
shg_pk = np.quantile(shg[~epi], 0.995)
shg = shg / shg_pk
shg = np.where(shg > 1, 1 + 0.35 * np.log1p(np.maximum(shg - 1, 0)), shg)   # soft shoulder

# ----------------------------------------------------------------------------
# 4. TPEF channel: epithelial cells + stromal cells
# ----------------------------------------------------------------------------
tpef = np.zeros((H, W), np.float32)

# --- cell centres by variable-radius dart throwing inside the epithelium
epi_dil = ndi.binary_dilation(epi, iterations=6)
cand_n = 26000
cx_c = rng.uniform(xb.min() - 10, W + 10, cand_n)
cy_c = rng.uniform(-10, H + 10, cand_n)
ci = np.clip(cx_c, 0, W - 1).astype(int); cj = np.clip(cy_c, 0, H - 1).astype(int)
inside = epi_dil[cj, ci]
cx_c, cy_c = cx_c[inside], cy_c[inside]
d_in_c = dist_in[np.clip(cy_c, 0, H - 1).astype(int), np.clip(cx_c, 0, W - 1).astype(int)]
r_c = 12.5 + 8.5 * smoothstep(10, 230, d_in_c) + rng.normal(0, 2.0, cx_c.size)
r_c = np.clip(r_c, 10.5, 23.0)
# basal cells first (sort by distance) so the basal layer packs tightly
order = np.argsort(d_in_c + rng.uniform(0, 60, d_in_c.size))
accx, accy, accr = [], [], []
for idx in order:
    x, y, r = cx_c[idx], cy_c[idx], r_c[idx]
    if accx:
        ax = np.array(accx); ay = np.array(accy); ar = np.array(accr)
        dd = np.hypot(ax - x, ay - y)
        if np.any(dd < (ar + r) * rng.uniform(0.80, 0.92)):
            continue
    accx.append(x); accy.append(y); accr.append(r)
cells = np.stack([np.array(accx), np.array(accy)], axis=1)
crad = np.array(accr)
n_cells = len(crad)
c_dist = dist_in[np.clip(cells[:, 1], 0, H - 1).astype(int), np.clip(cells[:, 0], 0, W - 1).astype(int)]
c_tang = np.arctan2(1.0, dxb[np.clip(cells[:, 1], 0, H - 1).astype(int)])   # boundary tangent
# per-cell brightness: random x slow spatial field x layer gradient
patch = smooth_noise((H, W), 45)
c_bright = rng.uniform(0.5, 1.0, n_cells) * np.clip(1 + 0.22 * patch[np.clip(cells[:, 1], 0, H - 1).astype(int), np.clip(cells[:, 0], 0, W - 1).astype(int)], 0.5, 1.5)
c_bright *= 1.15 - 0.35 * smoothstep(30, 300, c_dist)      # basal bright, superficial dimmer
# cell shape: roundish, superficial layers flattened parallel to the surface
c_aspect = 1.0 + rng.uniform(0.0, 0.35, n_cells) + 0.6 * smoothstep(180, 330, c_dist)
c_ang = np.where(c_dist > 150, c_tang + rng.normal(0, 0.25, n_cells), rng.uniform(0, np.pi, n_cells))
# nuclei: variable size, offset, contrast (some barely visible)
nuc_off = rng.normal(0, 0.16, (n_cells, 2)) * crad[:, None]
nuc_a = 0.42 * crad * rng.uniform(0.95, 1.25, n_cells)
nuc_b = 0.42 * crad * rng.uniform(0.7, 1.0, n_cells)
nuc_ang = rng.uniform(0, np.pi, n_cells)
nuc_dark = rng.uniform(0.45, 0.9, n_cells)
# basal nuclei are larger relative to the cell (high N:C ratio), elongated radially
basal = c_dist < 40
nuc_a[basal] *= 1.3; nuc_b[basal] *= 1.05
nuc_ang[basal] = c_tang[basal] + np.pi / 2
nuc_dark[basal] = np.clip(nuc_dark[basal] + 0.15, 0, 0.92)

tree = cKDTree(cells)
pm = np.argwhere(epi_dil)
py_, px_ = pm[:, 0], pm[:, 1]
dists, idxs = tree.query(np.stack([px_, py_], axis=1).astype(np.float64), k=2)
d1, d2 = dists[:, 0], dists[:, 1]
i1 = idxs[:, 0]
r1 = crad[i1]
# roundish/elliptical cell body that nearly fills its Voronoi tile
ca0, sa0 = np.cos(c_ang[i1]), np.sin(c_ang[i1])
u0 = (px_ - cells[i1, 0]) * ca0 + (py_ - cells[i1, 1]) * sa0
v0 = -(px_ - cells[i1, 0]) * sa0 + (py_ - cells[i1, 1]) * ca0
d_ell = np.sqrt((u0 / (r1 * c_aspect[i1])) ** 2 + (v0 / (r1 / np.sqrt(c_aspect[i1]))) ** 2)
body = smoothstep(1.14, 0.96, d_ell)
gap = 0.42 + 0.58 * smoothstep(0.4, 2.8, d2 - d1)          # thin dark membrane line
# nucleus
ncx = cells[i1, 0] + nuc_off[i1, 0]; ncy = cells[i1, 1] + nuc_off[i1, 1]
ca, sa = np.cos(nuc_ang[i1]), np.sin(nuc_ang[i1])
u = (px_ - ncx) * ca + (py_ - ncy) * sa
v = -(px_ - ncx) * sa + (py_ - ncy) * ca
dn = np.sqrt((u / nuc_a[i1]) ** 2 + (v / nuc_b[i1]) ** 2)
nuc = 1.0 - nuc_dark[i1] * smoothstep(1.12, 0.84, dn)
ring = 1.0 + 0.12 * np.exp(-((dn - 1.25) / 0.25) ** 2) * (rng.random(n_cells)[i1] < 0.5)
val = c_bright[i1] * body * gap * nuc * ring
cell_img = np.zeros((H, W), np.float32)
cell_img[py_, px_] = val
# cytoplasm granularity (mitochondrial NAD(P)H) and slow patchiness
gran = 1.0 + 0.22 * smooth_noise((H, W), 1.2) + 0.14 * smooth_noise((H, W), 3.5)
cell_img *= np.clip(gran, 0.3, 1.9)
cell_img *= 0.85 + 0.15 * smoothstep(-8, 3, dist_in)
tpef += 0.65 * cell_img

# --- stroma: faint diffuse autofluorescence, fibroblasts, a few round cells
tpef += 0.05 * shg + 0.025 * smoothstep(0, 1, (~epi).astype(np.float32)) * np.clip(1 + 0.5 * smooth_noise((H, W), 30), 0, 2)
for _ in range(16):
    x0 = rng.uniform(20, W - 20); y0 = rng.uniform(20, H - 20)
    if dist_out[int(y0), int(x0)] < 25:
        continue
    th = 0.5 * np.arctan2(sin2[int(y0), int(x0)], cos2[int(y0), int(x0)])
    a = rng.uniform(13, 22); b = rng.uniform(3.5, 6.0)
    add_soft_ellipse(tpef, x0, y0, a, b, th, rng.uniform(0.35, 0.6), edge=0.18,
                     nucleus=(a * 0.55, b * 0.8, th, 0.7))
for _ in range(9):
    x0 = rng.uniform(20, W - 20); y0 = rng.uniform(20, H - 20)
    if dist_out[int(y0), int(x0)] < 25:
        continue
    r = rng.uniform(4.5, 6.5)
    add_soft_ellipse(tpef, x0, y0, r, r * rng.uniform(0.85, 1.0), rng.uniform(0, np.pi),
                     rng.uniform(0.5, 0.8), edge=0.2, nucleus=(r * 0.6, r * 0.55, 0.0, 0.5))
tpef = np.clip(tpef, 0, None)
tpef = np.where(tpef > 1, 1 + 0.3 * np.log1p(np.maximum(tpef - 1, 0)), tpef)

# ----------------------------------------------------------------------------
# 5. CARS channel: sparse lipid droplets
# ----------------------------------------------------------------------------
cars = np.zeros((H, W), np.float32)
drops = []
# scattered singles in the stroma
n_single = 0
while n_single < 26:
    x0 = rng.uniform(15, W - 15); y0 = rng.uniform(15, H - 15)
    if epi[int(y0), int(x0)] or dist_out[int(y0), int(x0)] < 12:
        continue
    drops.append((x0, y0, 3.0 + 5.0 * rng.uniform(0, 1) ** 0.6))
    n_single += 1
# clusters
for _ in range(4):
    while True:
        x0 = rng.uniform(60, W - 60); y0 = rng.uniform(60, H - 60)
        if not epi[int(y0), int(x0)] and dist_out[int(y0), int(x0)] > 30:
            break
    for _ in range(rng.integers(4, 8)):
        drops.append((x0 + rng.normal(0, 16), y0 + rng.normal(0, 16), rng.uniform(3.0, 7.0)))
# a few inside epithelial cytoplasm
for _ in range(7):
    i = rng.integers(0, n_cells)
    ang = rng.uniform(0, 2 * np.pi); rr = crad[i] * rng.uniform(0.55, 0.8)
    drops.append((cells[i, 0] + rr * np.cos(ang), cells[i, 1] + rr * np.sin(ang), rng.uniform(2.6, 4.5)))
for (x0, y0, r) in drops:
    amp = rng.uniform(0.7, 1.0)
    add_soft_ellipse(cars, x0, y0, r, r * rng.uniform(0.9, 1.0), rng.uniform(0, np.pi), amp, edge=0.18)
    # slightly brighter centre (spherical droplet)
    add_soft_ellipse(cars, x0, y0, r * 0.55, r * 0.5, 0.0, 0.18 * amp, edge=0.5)
# weak non-resonant background follows the tissue
cars += 0.035 * tpef + 0.02 * shg
cars = np.clip(cars, 0, 1.2)

# ----------------------------------------------------------------------------
# 6. acquisition model
# ----------------------------------------------------------------------------
rn = np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)) / np.sqrt(2)
vign = 1.0 - 0.42 * rn ** 2.2
illum = np.clip(1.0 + 0.07 * smooth_noise((H, W), 160), 0.8, 1.2)
rowgain = (1.0 + rng.normal(0, 0.012, (H, 1))).astype(np.float32)
field = (vign * illum * rowgain).astype(np.float32)


def acquire(ch, photons, bg, haze=(0.08, 0.05)):
    ch = ndi.gaussian_filter(ch, 1.15)                                # PSF
    ch = ch + haze[0] * ndi.gaussian_filter(ch, 16) + haze[1] * ndi.gaussian_filter(ch, 55)
    ch = ch * field
    lam = np.clip(ch + bg, 0, None) * photons
    counts = rng.poisson(lam).astype(np.float32)
    v = counts / photons + rng.normal(0, 0.011, ch.shape).astype(np.float32)
    v = v - bg * 0.7
    v = np.clip(v, 0, 1)
    v = np.round(v * 255) / 255                                        # 8-bit
    return v.astype(np.float32)


shg_a = acquire(shg, 36, 0.015)
tpef_a = acquire(tpef, 70, 0.012, haze=(0.07, 0.07))
cars_a = acquire(cars, 55, 0.010, haze=(0.06, 0.03))


# ----------------------------------------------------------------------------
# 7. colour mapping and composite
# ----------------------------------------------------------------------------
def colorize(v, base, hi, knee=0.62, gamma=0.92):
    v = np.clip(v, 0, 1) ** gamma
    v = v[..., None]
    base = np.array(base, np.float32) / 255
    hi = np.array(hi, np.float32) / 255
    t1 = np.clip(v / knee, 0, 1)
    t2 = np.clip((v - knee) / (1 - knee), 0, 1)
    return base * t1 + (hi - base) * t2


rgb = (colorize(shg_a, (16, 185, 129), (167, 243, 208), gamma=1.12)
       + colorize(tpef_a, (245, 158, 11), (253, 230, 138), knee=0.68)
       + colorize(cars_a, (249, 115, 22), (254, 200, 150), knee=0.6))
rgb = np.clip(rgb, 0, 1)
img8 = (rgb * 255 + 0.5).astype(np.uint8)
im = Image.fromarray(img8)

os.makedirs(OUT_DIR, exist_ok=True)
im.save(os.path.join(OUT_DIR, 'thumb-multimodal.png'), optimize=True)
im.save(os.path.join(OUT_DIR, 'thumb-multimodal.webp'), quality=82, method=6)

# small preview at card display size, for checking legibility (not shipped)
prev = im.resize((300, 200), Image.LANCZOS)
prev.save(os.path.join(PREVIEW_DIR, 'preview-thumb-multimodal-300.png'))
print('cells:', n_cells, 'bundles:', n_bundles, 'droplets:', len(drops),
      'epithelium fraction: %.2f' % epi_frac)
