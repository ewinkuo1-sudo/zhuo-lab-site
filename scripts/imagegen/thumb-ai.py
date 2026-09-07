"""
thumb-ai.png  (1200x800) -- research-card image for "AI-assisted label-free pathology".

Left two-thirds : a procedurally synthesised label-free multiphoton mosaic
                  (SHG collagen in emerald, faint amber TPEF cells) with a
                  whole-slide style 8x6 tile grid; each tile carries a
                  translucent classifier tint (cool mint -> warm coral).
Right third     : a minimal model motif (stack of feature-map squares, three
                  nodes, two outcome bars) in thin mint strokes.

Fully deterministic (fixed seed).  Run:  python3 scripts/imagegen/thumb-ai.py
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter, map_coordinates

OUT_DIR = "/Users/ewinkuo/git-repos/zhuo-lab-site/static/media/gen"
os.makedirs(OUT_DIR, exist_ok=True)
rng = np.random.default_rng(20260907)

# ---------------------------------------------------------------- palette
INK = (4, 32, 28)
GREEN = (15, 157, 120)
MINT = (110, 231, 183)
MINT_SOFT = (236, 253, 245)
WARM = (246, 112, 118)      # orange / rose blend for the "other" class
CREAM = (228, 222, 190)     # neutral mid-point for uncertain tiles

# ---------------------------------------------------------------- layout
W, H = 1200, 800
TILE, NX, NY = 96, 8, 6
PX0, PY0 = 44, 112
PW, PH = TILE * NX, TILE * NY          # 768 x 576 tissue panel
T = 2                                  # tissue synthesis supersample
tw, th = PW * T, PH * T
S = 2                                  # vector-layer supersample


def smooth_noise(shape, sigma):
    n = gaussian_filter(rng.standard_normal(shape), sigma)
    n -= n.mean()
    n /= n.std() + 1e-9
    return n


def ramp(t, stops):
    """Piecewise-linear colour ramp; stops = [(pos, (r,g,b)), ...]."""
    t = np.clip(t, 0.0, 1.0)
    out = np.zeros(t.shape + (3,), dtype=np.float64)
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]
        p1, c1 = stops[i + 1]
        m = (t >= p0) & (t <= p1)
        f = (t[m] - p0) / (p1 - p0)
        for c in range(3):
            out[..., c][m] = c0[c] * (1 - f) + c1[c] * f
    return out


def rgba(col, a):
    return (col[0], col[1], col[2], int(round(255 * a)))


# ================================================================ tissue fields
yy, xx = np.mgrid[0:th, 0:tw].astype(np.float64)
u, v = xx / tw, yy / th

# tumour (right) vs stroma (left) with a wavy, noisy boundary
bnd = 0.60 + 0.045 * np.sin(v * 2.0 * math.pi * 1.1 + 0.6) + 0.035 * smooth_noise((th, tw), 70)
ptum = 1.0 / (1.0 + np.exp(-(u - bnd) / 0.045))

# tumour nests: patchy islands of cells inside the tumour region
patch = np.clip((smooth_noise((th, tw), 40) + 0.45) / 0.3, 0, 1)
nest = ptum * patch

# collagen density: dense aligned stroma on the left, sparse septa on the right
gaps = np.clip(0.35 + 0.65 * (0.5 + 0.5 * smooth_noise((th, tw), 80)), 0, 1) ** 1.2
fdens = (1.0 - 0.92 * nest) * gaps * (0.6 + 0.4 * np.clip(0.5 + 0.5 * smooth_noise((th, tw), 35), 0, 1))
fdens *= 1.0 - 0.55 * ptum

# fibre orientation field (radians)
theta = -0.45 + 0.5 * smooth_noise((th, tw), 150) + 0.3 * smooth_noise((th, tw), 80) + 0.3 * smooth_noise((th, tw), 40)
theta += ptum * 1.0 * smooth_noise((th, tw), 25)

# ================================================================ collagen fibres
N_FIB = 760
cand = rng.uniform([0, 0], [tw, th], size=(60000, 2))
acc = rng.uniform(0, 1, 60000) < map_coordinates(fdens, [cand[:, 1], cand[:, 0]], order=1, mode="nearest")
seeds = cand[acc][:N_FIB]
N = seeds.shape[0]
pt_seed = map_coordinates(ptum, [seeds[:, 1], seeds[:, 0]], order=1, mode="nearest")

STEP = 1.0
L_stroma = np.where(rng.uniform(0, 1, N) < 0.35, rng.uniform(50, 160, N), rng.uniform(140, 460, N))
L_tum = rng.uniform(35, 130, N)
# second fibre family crossing the dominant one
fam_off = np.where(rng.uniform(0, 1, N) < 0.30, rng.normal(1.05, 0.15, N), rng.normal(0, 0.08, N))
L = np.where(rng.uniform(0, 1, N) < pt_seed, L_tum, L_stroma)
half = (L / 2 / STEP).astype(int)
NS = int(half.max()) + 1


def trace_dir(P0, sign, nsteps, nlim):
    P = P0.copy()
    th0 = map_coordinates(theta, [P[:, 1], P[:, 0]], order=1, mode="nearest") + fam_off
    d = np.stack([np.cos(th0), np.sin(th0)], 1) * sign
    traj = np.full((nsteps, P.shape[0], 2), np.nan)
    alive = np.ones(P.shape[0], bool)
    for k in range(nsteps):
        thk = map_coordinates(theta, [P[:, 1], P[:, 0]], order=1, mode="nearest") + fam_off
        dk = np.stack([np.cos(thk), np.sin(thk)], 1)
        flip = (dk * d).sum(1) < 0
        dk[flip] *= -1
        d = dk
        P = P + d * STEP
        alive &= (P[:, 0] > -30) & (P[:, 0] < tw + 30) & (P[:, 1] > -30) & (P[:, 1] < th + 30)
        alive &= k < nlim
        traj[k, alive] = P[alive]
    return traj


fwd = trace_dir(seeds, 1.0, NS, half)
bwd = trace_dir(seeds, -1.0, NS, half)
full = np.concatenate([bwd[::-1], seeds[None, :, :], fwd], axis=0)   # (M, N, 2)
M = full.shape[0]
s = (np.arange(M) - NS)[:, None] * STEP                               # arc length (M,1)

valid = ~np.isnan(full[..., 0])
fx = np.where(valid, full[..., 0], 0.0)
fy = np.where(valid, full[..., 1], 0.0)
th_pt = map_coordinates(theta, [fy.ravel(), fx.ravel()], order=1, mode="nearest").reshape(M, N) + fam_off[None, :]
nx_, ny_ = -np.sin(th_pt), np.cos(th_pt)

# per-fibre parameters
wave_a = rng.uniform(0.8, 5.5, N)[None, :]
wave_l = rng.uniform(45, 110, N)[None, :]
wave_p = rng.uniform(0, 2 * math.pi, N)[None, :]
mod_l = rng.uniform(40, 170, N)[None, :]
mod_p = rng.uniform(0, 2 * math.pi, N)[None, :]
bright = np.exp(rng.normal(0, 0.55, N))[None, :]
wclass = rng.choice(3, N, p=[0.50, 0.32, 0.18])
n_sib = rng.choice([1, 1, 2, 2, 3, 4], N)
sib_gap = rng.uniform(2.8, 6.0, N)

POL = -0.45   # excitation polarisation: fibres parallel to it are brightest (P-SHG look)
ends = np.abs(s) * 0 + (L[None, :] / 2 - np.abs(s))
taper = np.clip(ends / 45.0, 0, 1)
pshg = 0.35 + 0.65 * np.cos(th_pt - POL) ** 2
along = 1.0 + 0.45 * np.sin(2 * math.pi * s / mod_l + mod_p)
inten = bright * taper * pshg * along * (1.0 + 0.35 * wclass[None, :])
wave = wave_a * np.sin(2 * math.pi * s / wave_l + wave_p)
sib_ph = rng.uniform(0, 2 * math.pi, N)[None, :]

bufs = [np.zeros((th, tw)) for _ in range(3)]


def splat(buf, x, y, w):
    ok = (x >= 0) & (x < tw - 1) & (y >= 0) & (y < th - 1)
    x, y, w = x[ok], y[ok], w[ok]
    x0 = np.floor(x).astype(int)
    y0 = np.floor(y).astype(int)
    fxr, fyr = x - x0, y - y0
    idx = y0 * tw + x0
    acc_ = np.zeros(th * tw)
    acc_ += np.bincount(idx, w * (1 - fxr) * (1 - fyr), minlength=th * tw)
    acc_ += np.bincount(idx + 1, w * fxr * (1 - fyr), minlength=th * tw)
    acc_ += np.bincount(idx + tw, w * (1 - fxr) * fyr, minlength=th * tw)
    acc_ += np.bincount(idx + tw + 1, w * fxr * fyr, minlength=th * tw)
    buf += acc_.reshape(th, tw)


for j in range(4):
    sel = n_sib > j
    if not sel.any():
        continue
    off = ((j - (n_sib - 1) / 2.0) * sib_gap)[None, :]
    # each sibling drifts slowly and crimps with its own phase, so bundles do not look combed
    off_s = off * (1.0 + 0.3 * np.sin(2 * math.pi * s / 320.0 + sib_ph + j))
    wave_j = wave_a * (1.0 + 0.15 * j) * np.sin(2 * math.pi * s / wave_l + wave_p + 0.7 * j)
    px = fx + nx_ * (wave_j + off_s)
    py = fy + ny_ * (wave_j + off_s)
    wgt = inten * (1.0 - 0.18 * j)
    for c in range(3):
        m = valid & sel[None, :] & (wclass == c)[None, :]
        splat(bufs[c], px[m], py[m], wgt[m])

shg = gaussian_filter(bufs[0], 0.85) * 1.0 + gaussian_filter(bufs[1], 1.35) * 1.15 + gaussian_filter(bufs[2], 2.4) * 1.5

# local defocus: part of the field is slightly out of the focal plane
defocus = np.clip(0.3 + 0.5 * smooth_noise((th, tw), 110), 0, 0.5)
shg = shg * (1 - defocus) + gaussian_filter(shg, 2.2) * defocus
shg *= 1.0 + 0.18 * smooth_noise((th, tw), 1.0)       # fibril granularity
shg = shg + 0.08 * gaussian_filter(shg, 7.0)         # faint out-of-focus halo
shg = np.clip(shg, 0, None)
shg /= np.percentile(shg, 99.6) + 1e-9

# ================================================================ TPEF cells
tpef = np.zeros((th, tw))


def add_cell(cx, cy, sig, amp, elong=1.0, ang=0.0, nuc=0.65, lobes=(0.0, 0.0)):
    R = int(3.2 * sig * max(1.0, elong)) + 1
    x0, x1 = max(int(cx) - R, 0), min(int(cx) + R + 1, tw)
    y0, y1 = max(int(cy) - R, 0), min(int(cy) + R + 1, th)
    if x1 <= x0 or y1 <= y0:
        return
    ys, xs = np.mgrid[y0:y1, x0:x1].astype(np.float64)
    dx, dy = xs - cx, ys - cy
    ca, sa = math.cos(ang), math.sin(ang)
    px_ = (dx * ca + dy * sa) / elong
    py_ = -dx * sa + dy * ca
    phi = np.arctan2(py_, px_)
    rr = np.sqrt(px_ * px_ + py_ * py_) * (1 + 0.12 * np.cos(2 * phi + lobes[0]) + 0.08 * np.cos(3 * phi + lobes[1]))
    body = np.exp(-rr ** 2 / (2 * sig ** 2))
    core = np.exp(-rr ** 2 / (2 * (0.5 * sig) ** 2))
    tpef[y0:y1, x0:x1] += amp * body * (1 - nuc * core)


# close-packed tumour cells on a jittered hex lattice, accepted by nest density
sp = 40.0
gy = np.arange(0, th + sp, sp * 0.87)
cells = []
for r_i, gyv in enumerate(gy):
    gx = np.arange(0, tw + sp, sp) + (sp / 2 if r_i % 2 else 0)
    for gxv in gx:
        cx = gxv + rng.normal(0, 5.0)
        cy = gyv + rng.normal(0, 5.0)
        if not (0 <= cx < tw and 0 <= cy < th):
            continue
        nv = nest[int(cy), int(cx)]
        if rng.uniform() < nv * 0.95:
            cells.append((cx, cy))
for cx, cy in cells:
    add_cell(cx, cy, sig=rng.normal(11.5, 1.6), amp=np.exp(rng.normal(0, 0.35)),
             elong=rng.uniform(1.0, 1.35), ang=rng.uniform(0, math.pi),
             nuc=rng.uniform(0.75, 0.92), lobes=(rng.uniform(0, 6.3), rng.uniform(0, 6.3)))

# sparse elongated stromal cells (fibroblast-like), aligned with local fibres
cand = rng.uniform([0, 0], [tw, th], size=(6000, 2))
pv = map_coordinates(ptum, [cand[:, 1], cand[:, 0]], order=1, mode="nearest")
sc = cand[rng.uniform(0, 1, 6000) < (1 - pv) * 0.05][:150]
for cx, cy in sc:
    ang = theta[int(cy), int(cx)] + rng.normal(0, 0.25)
    add_cell(cx, cy, sig=rng.normal(7.0, 1.0), amp=np.exp(rng.normal(-0.6, 0.3)),
             elong=rng.uniform(2.2, 3.8), ang=ang, nuc=0.35, lobes=(0, 0))

# faint continuum inside the nests (cytoplasmic autofluorescence)
tpef += 0.05 * nest * (0.75 + 0.25 * np.clip(smooth_noise((th, tw), 10) * 0.5 + 0.5, 0, 1))
tpef = gaussian_filter(tpef, 0.9)
tpef /= np.percentile(tpef, 99.5) + 1e-9

# ================================================================ down-sample to 1x
def down(a):
    return a.reshape(PH, T, PW, T).mean(axis=(1, 3))


shg1, tpef1, ptum1 = down(shg), down(tpef), down(ptum)

# mosaic artefacts: per-tile gain drift and a mild per-tile vignette
gain = 1.0 + 0.045 * rng.standard_normal((NY, NX))
gain_map = np.kron(gain, np.ones((TILE, TILE)))
ty, tx = np.mgrid[0:TILE, 0:TILE].astype(np.float64)
rr = ((tx - TILE / 2 + 0.5) ** 2 + (ty - TILE / 2 + 0.5) ** 2) / (2 * (TILE / 2) ** 2)
vig = np.tile(1.0 - 0.09 * rr, (NY, NX))
row = 1.0 + 0.012 * rng.standard_normal((PH, 1))

shg1 = shg1 * gain_map * vig * row
tpef1 = tpef1 * gain_map * vig * row

t_shg = 1.0 - np.exp(-1.35 * shg1)
t_tpef = (1.0 - np.exp(-1.6 * tpef1)) * 0.50

# detector noise: photon-like (scales with sqrt of signal) plus a floor
t_shg = t_shg + rng.normal(0, 1, t_shg.shape) * (0.012 + 0.045 * np.sqrt(np.clip(t_shg, 0, 1)))
t_tpef = t_tpef + rng.normal(0, 1, t_tpef.shape) * (0.010 + 0.035 * np.sqrt(np.clip(t_tpef, 0, 1)))
t_shg = np.clip(t_shg, 0, 1)
t_tpef = np.clip(t_tpef, 0, 1)

shg_rgb = ramp(t_shg, [(0.0, (0, 0, 0)), (0.30, (6, 84, 62)), (0.65, (40, 190, 138)), (1.0, (196, 247, 224))])
tpef_rgb = ramp(t_tpef, [(0.0, (0, 0, 0)), (0.5, (140, 88, 22)), (1.0, (245, 196, 112))])

haze = np.clip(0.5 + 0.5 * smooth_noise((PH, PW), 60), 0, 1)
base = np.array([2.0, 18.0, 16.0])[None, None, :] + 9.0 * haze[..., None]
panel = base + shg_rgb + tpef_rgb
panel += rng.uniform(-0.5, 0.5, panel.shape)          # dither against banding
panel = np.clip(panel, 0, 255).astype(np.uint8)

# ================================================================ canvas
img = Image.new("RGB", (W, H), INK)
img.paste(Image.fromarray(panel), (PX0, PY0))
img = img.convert("RGBA")

# ---- classifier tile tints (1x, axis aligned)
tint = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(tint)
p_tiles = np.zeros((NY, NX))
for r in range(NY):
    for c in range(NX):
        p = ptum1[r * TILE:(r + 1) * TILE, c * TILE:(c + 1) * TILE].mean()
        p = float(np.clip(p + rng.normal(0, 0.05), 0, 1))
        p_tiles[r, c] = p
        conf = abs(2 * p - 1)
        if p < 0.5:
            f = p / 0.5
            col = tuple(int(MINT[i] * (1 - f) + CREAM[i] * f) for i in range(3))
        else:
            f = (p - 0.5) / 0.5
            col = tuple(int(CREAM[i] * (1 - f) + WARM[i] * f) for i in range(3))
        a = 0.10 + 0.25 * conf ** 0.85
        x0, y0 = PX0 + c * TILE, PY0 + r * TILE
        d.rectangle([x0, y0, x0 + TILE - 1, y0 + TILE - 1], fill=rgba(col, a))
img = Image.alpha_composite(img, tint)

# ---- tile grid + panel border (crisp 1px)
grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(grid)
for c in range(1, NX):
    x = PX0 + c * TILE
    d.line([(x, PY0), (x, PY0 + PH - 1)], fill=rgba(MINT_SOFT, 0.22), width=1)
for r in range(1, NY):
    y = PY0 + r * TILE
    d.line([(PX0, y), (PX0 + PW - 1, y)], fill=rgba(MINT_SOFT, 0.22), width=1)
d.rectangle([PX0 - 1, PY0 - 1, PX0 + PW, PY0 + PH], outline=rgba(MINT, 0.45), width=1)
img = Image.alpha_composite(img, grid)

# ---- vector layer (motif + highlighted tile), drawn at S x and down-sampled
vec = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
d = ImageDraw.Draw(vec)


def P(x, y):
    return (x * S, y * S)


def line(pts, col, a, w=1.5):
    d.line([P(*p) for p in pts], fill=rgba(col, a), width=max(1, int(round(w * S))))


def circle(cx, cy, r, fill=None, outline=None, w=1.5):
    box = [P(cx - r, cy - r), P(cx + r, cy + r)]
    d.ellipse(box, fill=fill, outline=outline, width=max(1, int(round(w * S))))


def rect(x0, y0, x1, y1, fill=None, outline=None, w=1.5, radius=0):
    box = [P(x0, y0), P(x1, y1)]
    if radius:
        d.rounded_rectangle(box, radius=radius * S, fill=fill, outline=outline, width=max(1, int(round(w * S))))
    else:
        d.rectangle(box, fill=fill, outline=outline, width=max(1, int(round(w * S))))


# highlighted tile (the tile currently being classified) -- rightmost column, 2nd row
hc, hr = NX - 1, 1
hx0, hy0 = PX0 + hc * TILE, PY0 + hr * TILE
rect(hx0 + 0.5, hy0 + 0.5, hx0 + TILE - 0.5, hy0 + TILE - 0.5, outline=rgba(MINT, 0.95), w=1.6)
hcy = hy0 + TILE / 2

# feature-map stack
SQ = 124
fx0, fy0 = 930, 190
for k_, (dx, dy, a_out) in enumerate([(32, -32, 0.35), (16, -16, 0.55), (0, 0, 0.9)]):
    x0, y0 = fx0 + dx, fy0 + dy
    rect(x0, y0, x0 + SQ, y0 + SQ, fill=rgba(INK, 1.0), outline=rgba(MINT, a_out), w=1.4)
# faint inner grid + a few activated cells on the front map
cells_n = 5
cs = SQ / cells_n
act = np.clip(0.5 + 0.5 * smooth_noise((cells_n, cells_n), 0.8), 0, 1)
for r in range(cells_n):
    for c in range(cells_n):
        x0, y0 = fx0 + c * cs, fy0 + r * cs
        a = 0.02 + 0.30 * float(act[r, c]) ** 2.2
        rect(x0 + 1.5, y0 + 1.5, x0 + cs - 1.5, y0 + cs - 1.5, fill=rgba(MINT, a))
for i in range(1, cells_n):
    line([(fx0 + i * cs, fy0), (fx0 + i * cs, fy0 + SQ)], MINT, 0.16, 1.0)
    line([(fx0, fy0 + i * cs), (fx0 + SQ, fy0 + i * cs)], MINT, 0.16, 1.0)

# connector from highlighted tile to the stack (dashed)
cx0, cx1 = hx0 + TILE + 5, fx0 - 5
seg, gap, x = 7.0, 5.0, cx0
while x < cx1:
    line([(x, hcy), (min(x + seg, cx1), hcy)], MINT, 0.55, 1.2)
    x += seg + gap
circle(cx0, hcy, 2.6, fill=rgba(MINT, 0.9))
circle(cx1, hcy, 2.6, fill=rgba(MINT, 0.9))

# three hidden nodes
nodes = [(948, 400), (1008, 400), (1068, 400)]
stack_bottom = (fx0 + SQ / 2, fy0 + SQ)
for nx, ny in nodes:
    line([stack_bottom, (nx, ny - 7)], MINT, 0.40, 1.2)
# outputs
outs = [(924, 520, MINT, 210), (924, 588, WARM, 88)]
for nx, ny in nodes:
    for ox, oy, col, _ in outs:
        line([(nx, ny + 7), (ox, oy - 6)], MINT, 0.22, 1.1)
for nx, ny in nodes:
    circle(nx, ny, 7, fill=rgba(INK, 1.0), outline=rgba(MINT, 0.85), w=1.5)

# outcome bars
BAR_X0, BAR_X1, BH = 944, 1168, 14
for ox, oy, col, length in outs:
    rect(BAR_X0, oy - BH / 2, BAR_X1, oy + BH / 2, fill=rgba(MINT_SOFT, 0.07), radius=BH / 2)
    rect(BAR_X0, oy - BH / 2, BAR_X0 + length, oy + BH / 2, fill=rgba(col, 0.92), radius=BH / 2)
    circle(ox, oy, 6, fill=rgba(col, 0.95))

vec = vec.resize((W, H), Image.LANCZOS)
img = Image.alpha_composite(img, vec).convert("RGB")

png_path = os.path.join(OUT_DIR, "thumb-ai.png")
webp_path = os.path.join(OUT_DIR, "thumb-ai.webp")
img.save(png_path, optimize=True)
img.save(webp_path, quality=82, method=6)
print("wrote", png_path, webp_path)
print("tile probabilities:\n", np.round(p_tiles, 2))
