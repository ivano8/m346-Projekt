"""Frame renderer: parallax camera, boil, timers, glitch/shake/flash, word-by-word captions.
Pipes raw RGB frames to ffmpeg -> build/video_silent.mp4
"""
import json, math, os, random, subprocess, sys
from functools import lru_cache
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
F = np.array([540.0, 960.0])
OFF = np.array([216.0, 384.0])
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
TL = json.load(open("timeline.json"))
EV = TL["events"]
FPS = TL["fps"]
SC = {s["id"]: s for s in TL["scenes"]}
CAP_FONT = "assets/fonts/Anton-Regular.ttf"
TIM_FONT = "assets/fonts/ShareTechMono-Regular.ttf"
ACC = (255, 84, 36)


# ------------------------------------------------------------------ helpers
def ease(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def kf(t, keys):
    """keys: [(t, value_tuple)] -> eased interpolation."""
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t0 <= t <= t1:
            k = ease((t - t0) / max(t1 - t0, 1e-6))
            return tuple(a + (b - a) * k for a, b in zip(v0, v1))
    return keys[-1][1]


def pulse(t, t0, dur):
    if t < t0 or t > t0 + dur:
        return 0.0
    return 1.0 - (t - t0) / dur


def rot_m(deg, cx, cy, s=1.0):
    a = math.radians(deg)
    c, si = math.cos(a) * s, math.sin(a) * s
    return np.array([[c, -si, cx - c * cx + si * cy], [si, c, cy - si * cx - c * cy], [0, 0, 1.0]])


def tr(dx, dy):
    return np.array([[1, 0, dx], [0, 1, dy], [0, 0, 1.0]])


@lru_cache(maxsize=64)
def layer_img(scene, name, v):
    p = f"assets/layers/{scene}__{name}__v{v}.png"
    if not os.path.exists(p):
        p = f"assets/layers/{scene}__{name}__v0.png"
    return Image.open(p).convert("RGBA")


# ------------------------------------------------------------------ timers
def fmt_years(y, base_s, t):
    # base_s seconds-of-day offset, ticks down
    rem = base_s - int(t)
    hh, mm, ss = rem // 3600 % 24, rem // 60 % 60, rem % 60
    return f"{y}Y 0{(y*7)%9+1}M {(y*13)%27+1:02d}D {hh:02d}:{mm:02d}:{ss:02d}"


def days_sub(t):
    rem = 6 * 86400 + 4 * 3600 + 17 * 60 + 32 - int(t)
    d, hh, mm, ss = rem // 86400, rem // 3600 % 24, rem // 60 % 60, rem % 60
    return f"{d}D {hh:02d}:{mm:02d}:{ss:02d}"


@lru_cache(maxsize=512)
def timer_sprite(main, sub, size_q, mirror=False, dim=False):
    size = size_q / 100
    fm = ImageFont.truetype(TIM_FONT, max(int(78 * size), 8))
    fs = ImageFont.truetype(TIM_FONT, max(int(30 * size), 6))
    pad = int(40 * size) + 6
    bm = fm.getbbox(main)
    bs = fs.getbbox(sub) if sub else (0, 0, 0, 0)
    w = max(bm[2], bs[2]) + pad * 2
    h = bm[3] + (bs[3] + int(10 * size) if sub else 0) + pad * 2
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    col = (255, 96, 50, 255) if not dim else (150, 60, 40, 255)
    d.text(((w - bm[2]) / 2, pad - bm[1] * 0.3), main, font=fm, fill=col)
    if sub:
        d.text(((w - bs[2]) / 2, pad + bm[3] + int(8 * size)), sub, font=fs, fill=(255, 140, 100, 230))
    yb = pad + bm[3] + (bs[3] + int(10 * size) if sub else 0) + int(4 * size)
    d.line([(pad, yb), (w - pad, yb)], fill=(255, 84, 36, 160), width=max(1, int(3 * size)))
    glow = img.filter(ImageFilter.GaussianBlur(max(2, 14 * size)))
    g = np.asarray(glow).astype(np.float32)
    g[..., 3] *= 1.6
    out = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8))
    core = img.copy()
    cd = np.asarray(core).astype(np.float32)
    cd[..., :3] = cd[..., :3] * 0.65 + np.array([255, 205, 180]) * 0.35  # hot core
    out.alpha_composite(Image.fromarray(cd.astype(np.uint8)))
    out.alpha_composite(glow, (0, 0)) if False else None
    if mirror:
        out = out.transpose(Image.FLIP_LEFT_RIGHT)
    return out


@lru_cache(maxsize=8)
def glow_sprite(q):
    r = q
    y, x = np.mgrid[-r:r, -r:r]
    a = np.clip(1 - np.sqrt(x * x + (y * 1.4) ** 2) / r, 0, 1) ** 2
    arr = np.zeros((2 * r, 2 * r, 4), np.uint8)
    arr[..., 0], arr[..., 1], arr[..., 2] = 255, 70, 25
    arr[..., 3] = (a * 70).astype(np.uint8)
    return Image.fromarray(arr)


def draw_timer(frame, pos, size, main, sub, t, t_on, mirror=False, alpha=1.0, flicker=0.0, seed=0):
    if t < t_on or alpha <= 0.01:
        return
    age = t - t_on
    pop = 0.55 + 0.45 * ease(age / 0.16) + 0.08 * math.sin(min(age, 0.4) * 25) * max(0, 1 - age / 0.4)
    rnd = random.Random(int(t * 30) * 31 + seed)
    a = alpha
    if age < 0.35:
        a *= 1.0 if rnd.random() > 0.35 else 0.25
    if flicker > 0 and rnd.random() < flicker:
        a *= rnd.uniform(0.0, 0.5)
    s = size * pop
    sq = max(10, int(round(s * 100 / 2)) * 2)
    spr = timer_sprite(main, sub, sq, mirror)
    gl = glow_sprite(max(20, int(220 * size)))
    x, y = pos
    if a < 1:
        spr = spr.copy()
        spr.putalpha(spr.getchannel("A").point(lambda v: int(v * a)))
    frame.alpha_composite(gl, (int(x - gl.width / 2), int(y - gl.height / 2 + 40 * size)))
    frame.alpha_composite(spr, (int(x - spr.width / 2), int(y - spr.height / 2)))


# ------------------------------------------------------------------ captions
CAP_CACHE = {}


def cap_word(word, size, color):
    key = (word, size, color)
    if key not in CAP_CACHE:
        f = ImageFont.truetype(CAP_FONT, size)
        bb = f.getbbox(word, stroke_width=int(size * 0.1))
        img = Image.new("RGBA", (bb[2] - bb[0] + 20, bb[3] - bb[1] + 30), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.text((10 - bb[0] + 6, 10 - bb[1] + 9), word, font=f, fill=(0, 0, 0, 150), stroke_width=int(size * 0.1), stroke_fill=(0, 0, 0, 150))
        img = img.filter(ImageFilter.GaussianBlur(3))
        d = ImageDraw.Draw(img)
        d.text((10 - bb[0], 10 - bb[1]), word, font=f, fill=color, stroke_width=int(size * 0.1), stroke_fill=(10, 8, 14))
        CAP_CACHE[key] = img
    return CAP_CACHE[key]


ACCENT_WORDS = {"TIMER", "SIXTY-ONE", "YEARS.", "THREE", "THREE.", "TWO.", "ONE.", "FOUR", "MINUTES.", "SIX", "DAYS.", "SHORTEST", "A", "B", "SECOND."}


def build_chunks():
    chunks = []
    for ln in TL["lines"]:
        ws = ln["words"]
        end = ln["start"] + ln["dur"]
        cur = []
        for i, (w, t) in enumerate(ws):
            cur.append((w.upper(), t))
            brk = w.endswith((".", ",", "?", "...")) or len(cur) >= 3 or sum(len(x[0]) for x in cur) > 13
            if brk or i == len(ws) - 1:
                nxt = ws[i + 1][1] if i + 1 < len(ws) else end + 0.25
                chunks.append(dict(words=cur, start=cur[0][1], end=nxt))
                cur = []
    return chunks


CHUNKS = build_chunks()


def caption_y(t):
    if SC["S09_compare"]["start"] <= t < SC["S09_compare"]["end"]:
        return 958
    return 1450


def draw_captions(frame, t):
    for ch in CHUNKS:
        if ch["start"] <= t < ch["end"]:
            size = 112
            vis = [(w, wt) for w, wt in ch["words"] if wt <= t]
            imgs = []
            for j, (w, wt) in enumerate(vis):
                col = (255, 96, 50) if w.strip(".,?!") in {x.strip(".,?!") for x in ACCENT_WORDS} or w in ACCENT_WORDS else (245, 243, 240)
                img = cap_word(w, size, col)
                age = t - wt
                sc = 1.0 + 0.28 * max(0, 1 - age / 0.13)
                if sc != 1.0:
                    img = img.resize((int(img.width * sc), int(img.height * sc)), Image.BILINEAR)
                imgs.append(img)
            total = sum(i.width for i in imgs) - 18 * (len(imgs) - 1)
            scale = min(1.0, 980 / max(total, 1))
            x = W / 2 - total * scale / 2
            cy = caption_y(t)
            for img in imgs:
                if scale < 1:
                    img = img.resize((int(img.width * scale), int(img.height * scale)), Image.BILINEAR)
                frame.alpha_composite(img, (int(x), int(cy - img.height / 2)))
                x += img.width - 18 * scale
            break


# ------------------------------------------------------------------ scene definitions
def tsec(t, sc):
    return t - SC[sc]["start"]


def scene_spec(sid, t):
    """Returns (layers, camera(zoom,cx,cy), timers, fx dict). Layers: [(name, depth, extra_matrix_layer_to_world, alpha)]."""
    s0, s1 = SC[sid]["start"], SC[sid]["end"]
    lt = t - s0
    layers, timers = [], []
    fx = dict(shake=0.0, glitch=0.0, flash=0.0, flash_col=(255, 255, 255), strobe=0.0, dark=0.0, red=0.0)
    I = np.eye(3)
    if sid == "S01_wake":
        cam = kf(lt, [(0, (1.12, 560, 880)), (1.2, (1.22, 560, 860))])
        face = "face_wide" if t >= EV["eyes_open"] else "face_closed"
        layers = [("bg", .3, I), ("bed", .6, I), (face, 1.0, I), ("blanket", 1.1, I)]
        fx["shake"] = 22 * pulse(t, EV["eyes_open"], 0.35)
        fx["glitch"] = 0.9 * pulse(t, EV["eyes_open"], 0.25) + (0.7 if t < 0.06 else 0)
        fx["flash"] = 0.5 * pulse(t, EV["eyes_open"], 0.15)
        fx["red"] = 0.18
    elif sid == "S02_street":
        cam = kf(lt, [(0, (1.18, 540, 820)), (s1 - s0, (1.05, 540, 960))])
        layers = [("far", .25, I), ("street", .55, I), ("frame", 1.0, I)]
        peds = [(170, 830, 0.36, "72 YRS"), (400, 860, 0.4, "40 YRS"), (640, 820, 0.32, "18 YRS"), (880, 850, 0.38, "55 YRS"),
                (280, 1110, 0.5, "63 YRS"), (760, 1140, 0.52, "9 YRS"), (520, 1300, 0.6, "81 YRS")]
        for i, (x, y, s, txt) in enumerate(peds):
            timers.append(dict(depth=.55, pos=(x, y - 150 * s - 30 * s), size=0.55 + s * 0.6, main=txt, sub=None, on=EV["street_timers"] + 0.11 * i))
        fx["glitch"] = 0.5 * pulse(t, s0, 0.15)
        fx["shake"] = 8 * pulse(t, EV["street_timers"], 0.3)
    elif sid == "S03_kitchen":
        dur = s1 - s0
        a, b = EV["mom_timer"] - s0, EV["dog_timer"] - s0
        cam = kf(lt, [(0, (1.0, 540, 1000)), (a - 0.2, (1.12, 420, 820)), (b - 0.5, (1.15, 420, 800)), (b + 0.1, (1.2, 760, 1130)),
                      (b + 1.2, (1.2, 770, 1140)), (dur, (1.02, 560, 1000))])
        layers = [("bg", .35, I), ("mom", .75, I), ("dog", .8, I), ("fg", 1.25, I)]
        timers.append(dict(depth=.75, pos=(330, 500), size=1.1, main="61 YRS", sub="yrs", on=EV["mom_timer"], kind="mom"))
        timers.append(dict(depth=.8, pos=(820, 1185), size=0.95, main="3 YRS", sub="dog", on=EV["dog_timer"], kind="dog"))
        fx["shake"] = 7 * pulse(t, EV["mom_timer"], 0.25) + 7 * pulse(t, EV["dog_timer"], 0.25)
        fx["glitch"] = 0.35 * pulse(t, EV["mom_timer"], 0.12) + 0.35 * pulse(t, EV["dog_timer"], 0.12)
    elif sid in ("S04_bus", "S05_collapse"):
        speed = 380 if sid == "S04_bus" else 120
        scroll = -((t - SC["S04_bus"]["start"]) * speed) % 3400
        layers = [("outside", .2, tr(-scroll, 0)), ("interior", .6, I), ("chars", .75, I)]
        if sid == "S05_collapse":
            layers.append(("body", .85, I))
        layers.append(("fg", 1.3, I))
        others = [dict(depth=.75, pos=(150, 700), size=0.7, main="44 YRS", sub=None, on=s0 - 1),
                  dict(depth=.75, pos=(930, 680), size=0.7, main="29 YRS", sub=None, on=s0 - 1)]
        timers += others
        fx["strobe"] = 1.0
        if sid == "S04_bus":
            dur = s1 - s0
            cam = kf(lt, [(0, (1.0, 540, 960)), (EV["fast_from"] - s0, (1.12, 545, 820)), (EV["three"] - s0, (1.25, 545, 760)), (dur, (1.5, 545, 700))])
            # countdown value
            if t < EV["fast_from"]:
                rem = 240 - max(0, int(t - EV["stranger_timer"]))
            elif t < EV["three"]:
                k = (t - EV["fast_from"]) / (EV["three"] - EV["fast_from"])
                k = k ** 1.6
                rem = int(round(239 - (239 - 4) * k))
            else:
                rem = 3 - int(t - EV["three"])
            rem = max(rem, 0)
            timers.append(dict(depth=.75, pos=(545, 600), size=1.25, main=f"00:{rem//60:02d}:{rem%60:02d}", sub=None, on=EV["stranger_timer"]))
            for e in ("three", "two", "one"):
                fx["shake"] += 10 * pulse(t, EV[e], 0.25)
                fx["glitch"] += 0.25 * pulse(t, EV[e], 0.1)
            fx["shake"] += 6 * pulse(t, EV["stranger_timer"], 0.25)
            fx["red"] = 0.25 * ease((t - EV["three"]) / 3.0) if t > EV["three"] else 0
        else:
            cam = kf(lt, [(0, (1.18, 470, 1150)), (s1 - s0, (1.08, 500, 1080))])
            timers.append(dict(depth=.85, pos=(380, 1290), size=1.1, main="00:00:00", sub=None, on=s0 - 1,
                               alpha=max(0.0, 1 - lt / 2.2), flicker=0.5))
            fx["shake"] = 26 * pulse(t, s0, 0.45)
            fx["glitch"] = 0.8 * pulse(t, s0, 0.3)
            fx["flash"] = 0.6 * pulse(t, s0, 0.12)
            fx["flash_col"] = (255, 70, 30)
    elif sid == "S06_reaction":
        cam = kf(lt, [(0, (1.0, 540, 930)), (0.18, (1.14, 540, 880)), (s1 - s0, (1.2, 540, 870))])
        layers = [("interior", .4, I), ("you", 1.0, I), ("pole", 1.0, I)]
        fx["shake"] = 14 * pulse(t, s0, 0.3)
        fx["dark"] = 0.15
    elif sid == "S07_mirror":
        dur = s1 - s0
        cam = kf(lt, [(0, (1.0, 540, 1000)), (EV["my_timer"] - s0 - 0.3, (1.12, 540, 880)), (EV["my_timer"] - s0 + 0.1, (1.3, 600, 760)),
                      (EV["tilt"] - s0, (1.33, 600, 760)), (dur, (1.42, 600, 800))])
        ang_back = -7 * ease((t - EV["tilt"]) / 0.45)
        ang_refl = -7 * ease((t - EV["tilt"] - 0.75) / 0.45)
        Mb = rot_m(ang_back, 470, 1700)
        Mr = rot_m(ang_refl, 620, 1080)
        refl = "refl_smile" if t >= EV["smile"] else "refl_worried"
        layers = [("room", .55, I), (refl, .6, Mr), ("wall", .6, I), ("sink", .9, I), ("back", 1.15, Mb)]
        # mirrored (correct for a mirror) timers for mom + dog, but YOUR timer reads normally -> wrong
        timers.append(dict(depth=.55, pos=(330, 505), size=0.55, main="61 YRS", sub=None, on=EV["room_timers"], mirror=True))
        timers.append(dict(depth=.55, pos=(420, 885), size=0.45, main="3 YRS", sub=None, on=EV["room_timers"] + 0.15, mirror=True))
        timers.append(dict(depth=.6, pos=(640, 470), size=1.2, main="6 DAYS", sub="days", on=EV["my_timer"], M=Mr))
        fx["shake"] = 22 * pulse(t, EV["my_timer"], 0.5)
        fx["glitch"] = 0.9 * pulse(t, EV["my_timer"], 0.35) + 0.5 * pulse(t, EV["smile"], 0.2) + 0.35 * pulse(t, EV["tilt"] + 0.75, 0.15)
        fx["flash"] = 0.4 * pulse(t, EV["my_timer"], 0.12)
        fx["flash_col"] = (255, 70, 30)
        fx["dark"] = 0.1 + 0.15 * ease((t - EV["tilt"]) / 2)
        fx["red"] = 0.15 if t > EV["my_timer"] else 0
    elif sid == "S08_class":
        dur = s1 - s0
        cam = kf(lt, [(0, (1.0, 540, 1000)), (EV["turn"] - s0, (1.1, 560, 900)), (EV["teacher_timer"] - s0 + 0.05, (1.32, 560, 700)), (dur, (1.4, 560, 690))])
        teach = "teach_front" if t >= EV["turn"] else "teach_back"
        layers = [("bg", .4, I), (teach, .65, I), ("students", 1.0, I)]
        for x, y, txt in ((120, 1190, "58 YRS"), (540, 1210, "66 YRS"), (960, 1190, "71 YRS")):
            timers.append(dict(depth=1.0, pos=(x, y), size=0.6, main=txt, sub=None, on=s0 - 1))
        timers.append(dict(depth=.65, pos=(560, 470), size=1.1, main="6 DAYS", sub="days", on=EV["teacher_timer"]))
        fx["shake"] = 22 * pulse(t, EV["teacher_timer"], 0.45) + 5 * pulse(t, EV["turn"], 0.2)
        fx["glitch"] = 0.85 * pulse(t, EV["teacher_timer"], 0.3)
        fx["flash"] = 0.4 * pulse(t, EV["teacher_timer"], 0.1)
        fx["flash_col"] = (255, 70, 30)
    elif sid == "S09_compare":
        cam = (1.0, 540, 960)
        layers = [("top", 0, tr(-14 * lt, 0) @ rot_m(0, 0, 0, 1.0)), ("bot", 0, tr(14 * lt, 0)), ("divider", 0, I)]
        timers.append(dict(depth=0, pos=(560 - 14 * lt, 150), size=1.0, main="6 DAYS", sub="days", on=s0 - 1))
        timers.append(dict(depth=0, pos=(520 + 14 * lt, 1100), size=1.0, main="6 DAYS", sub="days", on=s0 - 1))
        fx["glitch"] = 0.5 * pulse(t, s0, 0.2)
    elif sid == "S10_choice":
        dur = s1 - s0
        cam = kf(lt, [(0, (1.0, 540, 1000)), (dur, (1.18, 540, 900))])
        k = lt / dur
        sc_ = 1.0 - 0.45 * k
        bob = 8 * abs(math.sin(lt * 5.5))
        px, py = 540, 1010 - 140 * k - bob * sc_
        Mt = tr(px, py) @ rot_m(1.5 * math.sin(lt * 5.5), 0, 0, sc_)
        layers = [("bg", .35, I), ("teacher", .7, Mt), ("you", 1.2, I)]
        timers.append(dict(depth=.7, pos=(0, -175), size=0.85, main="6 DAYS", sub="days", on=s0 - 1, M=Mt, scale_with_M=True))
        fx["shake"] = 6 * pulse(t, EV["card_a"], 0.2) + 6 * pulse(t, EV["card_b"], 0.2) + 10 * pulse(t, EV["cta"], 0.25)
        fx["glitch"] = 0.3 * pulse(t, EV["card_a"], 0.12) + 0.3 * pulse(t, EV["card_b"], 0.12) + 0.5 * pulse(t, EV["endcard"], 0.25)
        fx["dark"] = 0.1
    return layers, cam, timers, fx


# ------------------------------------------------------------------ frame
_rng_noise = np.random.default_rng(3)
GRAIN = [(_rng_noise.standard_normal((H // 2, W // 2)) * 7).astype(np.float32) for _ in range(6)]
yy, xx = np.mgrid[0:H, 0:W]
VIG = (1 - 0.55 * np.clip(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.6)) ** 2, 0, 1)).astype(np.float32)[..., None]
del yy, xx


def cam_matrix(cam, depth, shake_xy, shake_rot):
    z, cx, cy = cam
    zd = 1 + (z - 1) * depth
    c = F + (np.array([cx, cy]) - F) * depth
    # world -> frame
    M = np.array([[zd, 0, F[0] - c[0] * zd], [0, zd, F[1] - c[1] * zd], [0, 0, 1.0]])
    M = tr(shake_xy[0] * depth, shake_xy[1] * depth) @ rot_m(shake_rot * depth, F[0], F[1]) @ M
    return M


def apply(M, p):
    v = M @ np.array([p[0], p[1], 1.0])
    return v[0], v[1]


def chip(frame, text, x, y, w, h, alpha, border=ACC, letter=None, font_size=74):
    if alpha <= 0:
        return
    box = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(box)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=26, fill=(14, 12, 20, 225), outline=border + (255,), width=6)
    f = ImageFont.truetype(CAP_FONT, font_size)
    tx = 36
    if letter:
        d.rounded_rectangle([22, 18, 22 + h - 36, h - 18], radius=18, fill=border + (255,))
        lb = f.getbbox(letter)
        d.text((22 + (h - 36 - lb[2]) / 2, (h - lb[3] - lb[1]) / 2 - 2), letter, font=f, fill=(14, 12, 20))
        tx = 22 + h - 36 + 30
    tb = f.getbbox(text)
    d.text((tx, (h - tb[3] - tb[1]) / 2 - 2), text, font=f, fill=(245, 243, 240))
    if alpha < 1:
        box.putalpha(box.getchannel("A").point(lambda v: int(v * alpha)))
    frame.alpha_composite(box, (int(x), int(y)))


def overlays(frame, t):
    # Part tag
    if t < SC["S10_choice"]["start"]:
        a = min(1.0, t / 0.4)
        chip(frame, "PART 1", 60, 190, 230, 84, a * 0.9, font_size=48)
    if t >= EV["card_a"]:
        for key, letter, txt, y in (("card_a", "A", "TELL HER", 250), ("card_b", "B", "FOLLOW HER", 430)):
            if t >= EV[key]:
                age = t - EV[key]
                x = 110 + (1 - ease(age / 0.22)) * (-700 if letter == "A" else 700)
                chip(frame, txt, x, y, 860, 150, min(1, age / 0.15), letter=letter, font_size=84)
    if t >= EV["cta"]:
        age = t - EV["cta"]
        if age > 0:
            f = ImageFont.truetype(CAP_FONT, 64)
            msg = "COMMENT A OR B"
            img = cap_word(msg, 96, (255, 96, 50))
            sc = 1 + 0.2 * max(0, 1 - age / 0.15)
            img = img.resize((int(img.width * sc), int(img.height * sc)))
            frame.alpha_composite(img, (int(W / 2 - img.width / 2), 640))
    if t >= EV["endcard"]:
        age = t - EV["endcard"]
        a = min(1, age / 0.3)
        dark = Image.new("RGBA", (W, H), (8, 6, 12, int(200 * a)))
        frame.alpha_composite(dark)
        for txt, size, col, y in (("MAJORITY DECIDES", 92, (245, 243, 240), 760), ("PART 2", 230, (255, 96, 50), 900), ("A  OR  B ?", 120, (245, 243, 240), 1170)):
            img = cap_word(txt, size, col)
            img = img.copy()
            img.putalpha(img.getchannel("A").point(lambda v: int(v * a)))
            frame.alpha_composite(img, (int(W / 2 - img.width / 2), y))


def render_frame(fi):
    t = fi / FPS
    sid = next(s["id"] for s in TL["scenes"] if s["start"] <= t < s["end"]) if t < TL["total"] else TL["scenes"][-1]["id"]
    layers, cam, timers, fx = scene_spec(sid, t)
    rnd = random.Random(fi * 7919)
    sh = fx["shake"]
    shake_xy = (rnd.uniform(-sh, sh), rnd.uniform(-sh, sh))
    shake_rot = rnd.uniform(-sh, sh) * 0.04
    # gentle handheld drift
    shake_xy = (shake_xy[0] + 3 * math.sin(t * 0.9), shake_xy[1] + 3 * math.cos(t * 0.7))
    v = (fi // 4) % 3  # boil at 7.5 fps
    frame = Image.new("RGBA", (W, H), (10, 10, 16, 255))
    Ms = {}
    for name, depth, A in layers:
        C = cam_matrix(cam, depth, shake_xy, shake_rot)
        M = C @ A  # layer -> frame
        Ms[name] = M
        inv = np.linalg.inv(M)
        P = tr(OFF[0], OFF[1]) @ inv  # frame -> layer pixel
        img = layer_img(sid, name, v)
        out = img.transform((W, H), Image.AFFINE, tuple(P[:2].flatten()), resample=Image.BILINEAR)
        frame.alpha_composite(out)
    for i, tm in enumerate(timers):
        A = tm.get("M", np.eye(3))
        C = cam_matrix(cam, tm["depth"], shake_xy, shake_rot)
        M = C @ A
        x, y = apply(M, tm["pos"])
        zs = math.sqrt(abs(np.linalg.det(M[:2, :2])))
        sub = tm["sub"]
        if sub == "yrs":
            sub = fmt_years(61, 7 * 3600 + 33 * 60 + 21, t)
        elif sub == "dog":
            sub = fmt_years(3, 14 * 3600 + 5 * 60 + 48, t)
        elif sub == "days":
            sub = days_sub(t)
        draw_timer(frame, (x, y), tm["size"] * zs, tm["main"], sub, t, tm["on"], tm.get("mirror", False), tm.get("alpha", 1.0), tm.get("flicker", 0.0), seed=i)
    arr = np.asarray(frame.convert("RGB")).astype(np.float32)
    # bus streetlight strobe
    if fx["strobe"]:
        ph = (t * 1.6) % 1.0
        arr *= 1.0 + 0.16 * math.exp(-((ph - 0.5) ** 2) / 0.01) - 0.05
    if fx["dark"]:
        arr *= 1 - fx["dark"]
    if fx["red"]:
        arr[..., 0] = arr[..., 0] * (1 + fx["red"] * 0.6)
        arr[..., 1:] *= 1 - fx["red"] * 0.25
    if fx["flash"] > 0:
        arr = arr * (1 - fx["flash"]) + np.array(fx["flash_col"], np.float32) * fx["flash"]
    g = min(fx["glitch"], 1.2)
    if g > 0.02:
        gr = random.Random(fi * 131)
        sft = int(28 * g) + 2
        arr[..., 0] = np.roll(arr[..., 0], sft, axis=1)
        arr[..., 2] = np.roll(arr[..., 2], -sft, axis=1)
        for _ in range(int(3 + 10 * g)):
            y0 = gr.randint(0, H - 40)
            hh = gr.randint(8, int(30 + 120 * g))
            arr[y0:y0 + hh] = np.roll(arr[y0:y0 + hh], gr.randint(-int(140 * g), int(140 * g)) , axis=1)
        for _ in range(int(2 * g + 1)):
            y0, x0 = gr.randint(0, H - 60), gr.randint(0, W - 200)
            arr[y0:y0 + gr.randint(6, 40), x0:x0 + gr.randint(60, 400)] = np.array([255, 80, 35]) if gr.random() < 0.5 else 235
        arr[::4] *= 1 - 0.25 * min(g, 1)
    # grade: lift blacks to navy, slight contrast
    arr = arr * 0.94 + np.array([6, 6, 12], np.float32)
    arr *= VIG
    gn = GRAIN[fi % len(GRAIN)]
    arr += np.repeat(np.repeat(gn, 2, 0), 2, 1)[..., None]
    frame = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    overlays(frame, t)
    draw_captions(frame, t)
    return np.asarray(frame.convert("RGB")).tobytes()


def render_range(args):
    a, b, path = args
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for fi in range(a, b):
        p.stdin.write(render_frame(fi))
    p.stdin.close()
    p.wait()
    return path


if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    n = int(round(TL["total"] * FPS))
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for t in [float(x) for x in sys.argv[2:]]:
            Image.frombytes("RGB", (W, H), render_frame(int(t * FPS))).save(f"build/still_{t:05.2f}.png")
        sys.exit()
    # split by scene boundaries into chunks so each worker keeps few layers in memory
    cuts = sorted(set([0, n] + [int(round(s["start"] * FPS)) for s in TL["scenes"]]))
    ranges = []
    for a, b in zip(cuts, cuts[1:]):
        step = 90
        for k in range(a, b, step):
            ranges.append((k, min(k + step, b), f"build/part_{k:05d}.mp4"))
    with Pool(4) as pool:
        parts = pool.map(render_range, ranges, chunksize=1)
    with open("build/parts.txt", "w") as f:
        for p in parts:
            f.write(f"file '{os.path.basename(p)}'\n")
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "build/parts.txt", "-c", "copy", "build/video_silent.mp4"])
    for p in parts:
        os.remove(p)
    print("done", n, "frames")
