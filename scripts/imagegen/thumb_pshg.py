"""thumb-pshg: synthetic polarization-resolved SHG (P-SHG) fibre-orientation
map of collagen for the Zhuo Lab research card.

Pipeline (deterministic, fixed seeds):
  1. A synthetic orientation field with three domains: a dominant crimped
     bundle (22 deg) crossed by a sparser second bundle (118 deg) on the left,
     and a cartilage-like arcade on the right (legs curving over into a
     tangential surface zone).
  2. Fibres are traced as streamlines with Jobard-Lefer style spacing, given
     a partly coherent crimp wave, along-fibre intensity variation,
     out-of-plane fading and end tapers.
  3. Each fibre is splatted at 2x resolution as a Gaussian line into an
     intensity accumulator and a doubled-angle vector accumulator, so that
     crossings lose anisotropy (as they do in real P-SHG fits).
  4. Hue = orientation (cyclic, isoluminant OKLCh wheel), lightness = SHG
     intensity, chroma = anisotropy.  Shot/read noise and speckle added.
  5. Overlays: orientation colour-wheel legend (bottom right) and a small
     polar P-SHG response inset (bottom left).  No text.
Outputs static/media/gen/thumb-pshg.png and .webp (1200x800).
"""
import os
import math
import numpy as np
from scipy.ndimage import gaussian_filter
from PIL import Image, ImageDraw

W, H = 1200, 800
S = 2
WS, HS = W * S, H * S
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "static", "media", "gen")
rng = np.random.default_rng(20260907)

H0 = math.radians(160.0)   # hue of a horizontal fibre (teal)
CMAX = 0.092               # peak chroma of the orientation wheel


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def field_noise(sig, seed):
    r = np.random.default_rng(seed)
    n = gaussian_filter(r.standard_normal((H, W)), sig)
    return n / (n.std() + 1e-9)


# ---------------------------------------------------------------- fields
A_ANG = math.radians(22.0)
B_ANG = math.radians(118.0)
XC, YC = 930.0, 470.0           # arcade centre

PERT = field_noise(45, 11) * math.radians(6.0) + field_noise(14, 12) * math.radians(2.5)
_yy, _xx = np.mgrid[0:H, 0:W].astype(float)
_rad = np.hypot(_xx - XC, _yy - YC)
DENS = 0.15 + 0.85 * smoothstep(-1.0, 1.4, field_noise(110, 13))
DENS *= 0.25 + 0.75 * smoothstep(70.0, 190.0, _rad)
XB = 640.0 + 70.0 * field_noise(70, 14)
_yn = _yy + 70.0 * field_noise(80, 15)
PAB = np.clip(1.0 - 0.6 * smoothstep(280.0, 620.0, _yn), 0.45, 0.97)
XBL = 640.0 + 90.0 * field_noise(60, 16)   # centre of the A/C blend


def field_dir(x, y, ftype):
    """Unit direction of the orientation field at (x, y) for a fibre type."""
    xi = int(x)
    yi = int(y)
    if xi < 0:
        xi = 0
    elif xi >= W:
        xi = W - 1
    if yi < 0:
        yi = 0
    elif yi >= H:
        yi = H - 1
    rx = x - XC
    ry = y - YC
    if abs(rx) + abs(ry) < 1e-9:
        thC = 0.0
    else:
        thC = math.atan2(rx, -ry)
    if ry > 0:
        tv = ry / 170.0
        tv = 1.0 if tv > 1 else tv
        wv = tv * tv * (3 - 2 * tv)
        thV = math.pi / 2 + 0.08 * rx / 300.0
        c2 = (1 - wv) * math.cos(2 * thC) + wv * math.cos(2 * thV)
        s2 = (1 - wv) * math.sin(2 * thC) + wv * math.sin(2 * thV)
        thC = 0.5 * math.atan2(s2, c2)
    tw = (x - XBL[yi, xi] + 150.0) / 300.0
    tw = 0.0 if tw < 0 else (1.0 if tw > 1 else tw)
    wC = tw * tw * (3 - 2 * tw)
    thL = B_ANG if ftype == 1 else A_ANG
    c2 = (1 - wC) * math.cos(2 * thL) + wC * math.cos(2 * thC)
    s2 = (1 - wC) * math.sin(2 * thL) + wC * math.sin(2 * thC)
    th = 0.5 * math.atan2(s2, c2) + PERT[yi, xi]
    return math.cos(th), math.sin(th)


def trace(x0, y0, ftype, sign, maxlen, block, r):
    pts = []
    x, y = x0, y0
    dx, dy = field_dir(x, y, ftype)
    dx *= sign
    dy *= sign
    h = 0.5
    L = 0.0
    while L < maxlen:
        mx = x + 0.5 * h * dx
        my = y + 0.5 * h * dy
        ex, ey = field_dir(mx, my, ftype)
        if ex * dx + ey * dy < 0:
            ex = -ex
            ey = -ey
        x += h * ex
        y += h * ey
        dx, dy = ex, ey
        L += h
        if x < -25 or x > W + 25 or y < -25 or y > H + 25:
            break
        xi = int(x)
        yi = int(y)
        if 0 <= xi < W and 0 <= yi < H:
            if block[yi, xi]:
                break
            if r.random() < 0.010 * (1.0 - DENS[yi, xi]):
                break
        pts.append((x, y))
    return pts


def disk_offsets(rad):
    n = int(math.ceil(rad))
    o = np.arange(-n, n + 1)
    ox, oy = np.meshgrid(o, o)
    m = ox * ox + oy * oy <= rad * rad
    return ox[m], oy[m]


def stamp(mask, pts, rad):
    ox, oy = disk_offsets(rad)
    P = np.asarray(pts)[::2]
    ix = (np.round(P[:, 0]).astype(int)[:, None] + ox[None, :]).ravel()
    iy = (np.round(P[:, 1]).astype(int)[:, None] + oy[None, :]).ravel()
    ok = (ix >= 0) & (ix < W) & (iy >= 0) & (iy < H)
    mask[iy[ok], ix[ok]] = True


def type_main(x, y, r):
    xi, yi = int(x), int(y)
    if x > XB[yi, xi]:
        return 2
    return 0 if r.random() < PAB[yi, xi] else 1


def make_fibres(n_cand, dsep, maxcount, r, len_range):
    seedblk = [np.zeros((H, W), bool) for _ in range(3)]
    trcblk = [np.zeros((H, W), bool) for _ in range(3)]
    fibres = []
    cand = r.uniform(0, 1, (n_cand, 2)) * np.array([W, H])
    for x0, y0 in cand:
        xi, yi = int(x0), int(y0)
        if r.random() > DENS[yi, xi]:
            continue
        t = type_main(x0, y0, r)
        if seedblk[t][yi, xi]:
            continue
        ml = r.uniform(len_range[0], len_range[1])
        fwd = trace(x0, y0, t, 1.0, ml, trcblk[t], r)
        bwd = trace(x0, y0, t, -1.0, ml, trcblk[t], r)
        pts = bwd[::-1] + [(x0, y0)] + fwd
        if len(pts) < 70:
            continue
        d = dsep[t] * r.uniform(0.8, 1.2)
        stamp(seedblk[t], pts, d)
        stamp(trcblk[t], pts, 0.55 * d)
        fibres.append((t, pts))
        if len(fibres) >= maxcount:
            break
    return fibres


# ---------------------------------------------------------------- render
def smooth1d(n, sig, r):
    v = gaussian_filter(r.standard_normal(n), sig, mode="nearest")
    return v / (v.std() + 1e-9)


def splat(accI, accR, accM, P1, angs, wts, sigma):
    P = P1 * S
    R = int(math.ceil(3.0 * sigma))
    off = np.arange(-R, R + 1)
    ox, oy = np.meshgrid(off, off)
    ox = ox.ravel()
    oy = oy.ravel()
    cx = np.round(P[:, 0]).astype(int)
    cy = np.round(P[:, 1]).astype(int)
    ix = cx[:, None] + ox[None, :]
    iy = cy[:, None] + oy[None, :]
    d2 = (ix - P[:, 0:1]) ** 2 + (iy - P[:, 1:2]) ** 2
    k = np.exp(-d2 / (2 * sigma * sigma)) / (sigma * math.sqrt(2 * math.pi))
    wv = wts[:, None] * k
    wr = wv * np.cos(2 * angs)[:, None]
    wm = wv * np.sin(2 * angs)[:, None]
    ix = ix.ravel()
    iy = iy.ravel()
    ok = (ix >= 0) & (ix < WS) & (iy >= 0) & (iy < HS)
    if not ok.any():
        return
    ix = ix[ok]
    iy = iy[ok]
    x0, x1 = ix.min(), ix.max() + 1
    y0, y1 = iy.min(), iy.max() + 1
    lw, lh = x1 - x0, y1 - y0
    li = (iy - y0) * lw + (ix - x0)
    for acc, wgt in ((accI, wv), (accR, wr), (accM, wm)):
        acc[y0:y1, x0:x1] += np.bincount(li, weights=wgt.ravel()[ok], minlength=lw * lh).reshape(lh, lw)


def render_fibre(accI, accR, accM, t, pts, r, amp_scale, sig_med, bright):
    P = np.asarray(pts, float)
    n = len(P)
    T = np.gradient(P, axis=0)
    T /= np.linalg.norm(T, axis=1)[:, None] + 1e-9
    N = np.stack([-T[:, 1], T[:, 0]], 1)
    s = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))])
    if t == 0:
        lam, amp, ph0 = 95.0, 1.7, 0.0
        proj = P[:, 0] * math.cos(A_ANG) + P[:, 1] * math.sin(A_ANG)
    elif t == 1:
        lam, amp, ph0 = 80.0, 1.4, 1.1
        proj = P[:, 0] * math.cos(B_ANG) + P[:, 1] * math.sin(B_ANG)
    else:
        lam, amp, ph0 = 110.0, 1.0, r.uniform(0, 2 * math.pi)
        proj = s
    phase = 2 * math.pi * proj / lam + ph0 + r.uniform(-0.9, 0.9)
    amp *= amp_scale * math.exp(r.normal(0, 0.3))
    wander = 2.5 * smooth1d(n, 110, r)
    disp = amp * np.sin(phase) + wander
    Pd = P + N * disp[:, None]
    Td = np.gradient(Pd, axis=0)
    Td = gaussian_filter(Td, (7, 0), mode="nearest")
    ang = np.arctan2(Td[:, 1], Td[:, 0])
    base = bright * 0.6 * math.exp(r.normal(0, 0.5))
    base = min(base, 2.6)
    sig = sig_med * math.exp(r.normal(0, 0.35))
    base *= (sig / sig_med) ** 0.6
    w = np.full(n, base)
    w *= np.exp(0.30 * smooth1d(n, 50, r))
    w *= 0.30 + 0.70 * smoothstep(-0.9, 0.5, smooth1d(n, 130, r))
    m = 0.25 if t < 2 else 0.12
    w *= 1 - m * np.sin(0.5 * phase) ** 2
    L = s[-1]
    w *= np.clip(s / 28.0, 0, 1) * np.clip((L - s) / 28.0, 0, 1)
    splat(accI, accR, accM, Pd, ang, w, sig)


# ---------------------------------------------------------------- colour
def oklch_to_lin(Lc, Cc, hc):
    a = Cc * np.cos(hc)
    b = Cc * np.sin(hc)
    l_ = Lc + 0.3963377774 * a + 0.2158037573 * b
    m_ = Lc - 0.1055613458 * a - 0.0638541728 * b
    s_ = Lc - 0.0894841775 * a - 1.2914855480 * b
    l = l_ ** 3
    m = m_ ** 3
    s = s_ ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bb = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return r, g, bb


def to_rgb_linear(Lc, Cc, hc):
    C = np.array(Cc, float, copy=True)
    for _ in range(12):
        r, g, b = oklch_to_lin(Lc, C, hc)
        bad = (r < -0.002) | (g < -0.002) | (b < -0.002) | (r > 1.002) | (g > 1.002) | (b > 1.002)
        if not bad.any():
            break
        C = np.where(bad, C * 0.82, C)
    r, g, b = oklch_to_lin(Lc, C, hc)
    return np.clip(np.stack([r, g, b], -1), 0, 1)


def enc(x):
    x = np.clip(x, 0, 1)
    return np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(x, 1 / 2.4) - 0.055)


def box_down(a, Q):
    h, w = a.shape[0] // Q, a.shape[1] // Q
    if a.ndim == 3:
        return a[:h * Q, :w * Q].reshape(h, Q, w, Q, a.shape[2]).mean(axis=(1, 3))
    return a[:h * Q, :w * Q].reshape(h, Q, w, Q).mean(axis=(1, 3))


# ---------------------------------------------------------------- overlays
def ring_layer(r_out, r_in, Q=4, pad=10):
    m = r_out + pad
    n = int(2 * m * Q)
    yy, xx = np.mgrid[0:n, 0:n]
    px = (xx + 0.5) / Q - m
    py = (yy + 0.5) / Q - m
    rr = np.hypot(px, py)
    ph = np.arctan2(py, px)
    a_ring = smoothstep(r_in - 0.5, r_in + 0.5, rr) * (1 - smoothstep(r_out - 0.5, r_out + 0.5, rr))
    a_back = (1 - smoothstep(r_out + 6.0, r_out + 7.5, rr)) * 0.72
    hue = H0 + 2 * ph
    rgb_ring = enc(to_rgb_linear(np.full(rr.shape, 0.80), np.full(rr.shape, CMAX), hue))
    back = np.array([4, 32, 28]) / 255.0
    rgb = back[None, None, :] * (a_back * (1 - a_ring))[..., None] + rgb_ring * a_ring[..., None]
    alpha = a_back * (1 - a_ring) + a_ring
    tick = np.array([213, 232, 225]) / 255.0
    for kk in range(4):
        ak = kk * math.pi / 2
        u = px * math.cos(ak) + py * math.sin(ak)
        v = -px * math.sin(ak) + py * math.cos(ak)
        am = (1 - smoothstep(0.5, 1.1, np.abs(v))) * smoothstep(r_out + 1.5, r_out + 2.5, u) * (1 - smoothstep(r_out + 5.0, r_out + 6.0, u))
        am *= 0.85
        rgb = rgb * (1 - am[..., None]) + tick * am[..., None]
        alpha = alpha * (1 - am) + am
    return box_down(rgb, Q), box_down(alpha, Q)


def inset_layer(rad, th0, r, Q=4, pad=6):
    m = rad + pad
    n = int(2 * m * Q)
    layer = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    c = n / 2
    Rq = rad * Q
    d.ellipse([c - Rq, c - Rq, c + Rq, c + Rq], fill=(4, 32, 28, 212), outline=(110, 231, 183, 120), width=Q)
    for f in (1 / 3, 2 / 3, 1.0):
        rr = Rq * 0.84 * f
        d.ellipse([c - rr, c - rr, c + rr, c + rr], outline=(110, 231, 183, 42), width=max(1, Q // 2))
    for ak in (th0, th0 + math.pi / 2):
        rr = Rq * 0.84
        d.line([(c - rr * math.cos(ak), c - rr * math.sin(ak)), (c + rr * math.cos(ak), c + rr * math.sin(ak))],
               fill=(110, 231, 183, 42), width=max(1, Q // 2))
    ph = np.linspace(0, 2 * np.pi, 361)
    psi = ph - th0
    I = (1.7 * np.cos(psi) ** 2 + np.sin(psi) ** 2) ** 2 + 0.6 * np.sin(2 * psi) ** 2
    rc = Rq * 0.84 * I / I.max()
    xs = c + rc * np.cos(ph)
    ys = c + rc * np.sin(ph)
    d.line(list(zip(xs, ys)), fill=(110, 231, 183, 240), width=int(1.4 * Q), joint="curve")
    for kk in range(24):
        a = kk * math.pi / 12
        pk = a - th0
        Ik = (1.7 * math.cos(pk) ** 2 + math.sin(pk) ** 2) ** 2 + 0.6 * math.sin(2 * pk) ** 2
        rk = Rq * 0.84 * Ik / I.max() * (1 + r.normal(0, 0.04))
        x = c + rk * math.cos(a)
        y = c + rk * math.sin(a)
        dr = 1.3 * Q
        d.ellipse([x - dr, y - dr, x + dr, y + dr], fill=(236, 253, 245, 210))
    arr = np.asarray(layer).astype(float) / 255.0
    alpha = arr[..., 3]
    rgb = arr[..., :3] * alpha[..., None]
    return box_down(rgb, Q), box_down(alpha, Q)


def composite(base, rgb, alpha, cx, cy):
    h, w = alpha.shape
    x0 = int(round(cx - w / 2))
    y0 = int(round(cy - h / 2))
    sl = base[y0:y0 + h, x0:x0 + w]
    sl[:] = sl * (1 - alpha[..., None]) + rgb


# ---------------------------------------------------------------- main
def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    r_main = np.random.default_rng(101)
    r_oof = np.random.default_rng(202)
    main_f = make_fibres(9000, (11.0, 13.0, 10.0), 420, r_main, (100.0, 700.0))
    oof_f = make_fibres(3000, (18.0, 18.0, 18.0), 120, r_oof, (80.0, 400.0))
    print("fibres:", len(main_f), "oof:", len(oof_f))

    accI = np.zeros((HS, WS))
    accR = np.zeros((HS, WS))
    accM = np.zeros((HS, WS))
    for t, pts in main_f:
        render_fibre(accI, accR, accM, t, pts, r_main, 1.0, 2.0, 1.0 if t != 1 else 0.8)
    oI = np.zeros((HS, WS))
    oR = np.zeros((HS, WS))
    oM = np.zeros((HS, WS))
    for t, pts in oof_f:
        render_fibre(oI, oR, oM, t, pts, r_oof, 1.0, 7.0, 0.14)

    gI = gaussian_filter(accI, 9)
    gR = gaussian_filter(accR, 9)
    gM = gaussian_filter(accM, 9)
    I = box_down(accI + 0.14 * gI + oI, S)
    R = box_down(accR + 0.14 * gR + oR, S)
    M = box_down(accM + 0.14 * gM + oM, S)

    yy, xx = np.mgrid[0:H, 0:W]
    rr = np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2))
    I *= 0.80 + 0.20 * (1 - 0.5 * rr ** 2)

    I = I + 0.025 + rng.normal(0, 0.016, I.shape) + np.sqrt(np.maximum(I, 0)) * rng.normal(0, 0.05, I.shape)
    I = np.maximum(I, 0.002)
    zs = np.sqrt(I) * 0.05 + 0.018
    R = R + zs * rng.normal(0, 1, I.shape)
    M = M + zs * rng.normal(0, 1, I.shape)
    aniso = np.clip(np.hypot(R, M) / I, 0, 1)
    hue = H0 + np.arctan2(M, R)
    t = 1 - np.exp(-I / 0.70)
    Lc = 0.92 * t ** 0.62
    Cc = CMAX * aniso * np.clip(t / 0.2, 0, 1) * (1 - 0.3 * t ** 4)
    rgb = to_rgb_linear(Lc, Cc, hue)
    rgb = rgb + rng.normal(0, 0.0025, rgb.shape) + np.sqrt(rgb) * rng.normal(0, 0.02, rgb.shape)
    srgb = enc(rgb)
    srgb = np.clip(srgb + rng.normal(0, 0.006, srgb.shape), 0, 1)

    lr, la = ring_layer(40, 27)
    composite(srgb, lr, la, W - 72, H - 72)
    ir, ia = inset_layer(58, B_ANG, np.random.default_rng(303))
    composite(srgb, ir, ia, 90, H - 90)

    u8 = (np.clip(srgb, 0, 1) * 255 + 0.5).astype(np.uint8)
    img = Image.fromarray(u8)
    img.save(os.path.join(OUT_DIR, "thumb-pshg.png"), optimize=True)
    img.save(os.path.join(OUT_DIR, "thumb-pshg.webp"), "WEBP", quality=82, method=6)
    print("saved")


if __name__ == "__main__":
    main()
