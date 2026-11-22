"""Hand-drawn style SVG art for 'The Timer' Part 1.

Every scene is split into parallax layers. Each layer is drawn in world
coordinates (frame = 0..1080 x 0..1920, bleed = -216..1296 x -384..2304) and
rendered in several 'boil' variants (different jitter seeds) so the outlines
shimmer like hand-drawn animation.
"""
import math
import random

OUT = "#0c0a10"
VB = (-216, -384, 1512, 2688)

PAL = dict(
    bg0="#0d111d", bg1="#151b2c", bg2="#1d2540", bg3="#283252", bg4="#36415f",
    pur="#251f38", pur2="#352c4f", pur3="#4a3e66",
    teal="#18323a", teal2="#22474f", teal3="#2f5d66",
    skin="#c7a28b", skin_sh="#9e7a68", skin_pale="#cdb3a3",
    hair="#141219", cold="#8ea4c2", cold2="#5d7393", warm="#6a5a48", warm2="#8a7556",
    white="#d9dbe3", eye="#e6e4ea",
)

_clip = [0]


def cid():
    _clip[0] += 1
    return f"c{_clip[0]}"


class Pen:
    def __init__(self, seed, j=1.0):
        self.r = random.Random(seed)
        self.j = j

    def u(self, a):
        return self.r.uniform(-a, a) * self.j

    # --- paths -------------------------------------------------------
    @staticmethod
    def cr(pts, closed=True):
        n = len(pts)
        d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
        rng = range(n) if closed else range(n - 1)
        for i in rng:
            p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
            p1 = pts[i]
            p2 = pts[(i + 1) % n]
            p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
            c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
            c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
            d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
        return d + (" Z" if closed else "")

    def blob_pts(self, cx, cy, rx, ry, n=16, j=0.025, rot=0.0):
        pts = []
        for i in range(n):
            a = 2 * math.pi * i / n + rot
            k = 1 + self.u(j)
            pts.append((cx + math.cos(a) * rx * k, cy + math.sin(a) * ry * k))
        return pts

    def blob(self, cx, cy, rx, ry, n=16, j=0.025, rot=0.0):
        return self.cr(self.blob_pts(cx, cy, rx, ry, n, j, rot))

    def smooth(self, pts, closed=True, j=2.0):
        return self.cr([(x + self.u(j), y + self.u(j)) for x, y in pts], closed)

    def poly(self, pts, closed=True, j=2.0, seg=110):
        out = []
        n = len(pts)
        m = n if closed else n - 1
        for i in range(m):
            a = pts[i]
            b = pts[(i + 1) % n]
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            k = max(1, int(L / seg))
            for s in range(k):
                t = s / k
                jj = j if s else j * 0.6
                out.append((a[0] + (b[0] - a[0]) * t + self.u(jj), a[1] + (b[1] - a[1]) * t + self.u(jj)))
        if not closed:
            out.append((pts[-1][0] + self.u(j * 0.6), pts[-1][1] + self.u(j * 0.6)))
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in out)
        return d + (" Z" if closed else "")

    def rect(self, x, y, w, h, j=2.0):
        return self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], True, j)


def P(d, fill="none", sw=7, stroke=OUT, op=None, extra=""):
    o = f' opacity="{op}"' if op is not None else ""
    st = f' stroke="{stroke}" stroke-width="{sw:.2f}" stroke-linejoin="round" stroke-linecap="round"' if sw else ""
    return f'<path d="{d}" fill="{fill}"{st}{o}{extra}/>'


def G(inner, tx=0, ty=0, s=1.0, rot=0.0, extra=""):
    return f'<g transform="translate({tx:.1f},{ty:.1f}) rotate({rot:.2f}) scale({s:.3f})"{extra}>{inner}</g>'


def svg_doc(body, defs=""):
    x, y, w, h = VB
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" width="{w}" height="{h}">'
            f"<defs>{defs}</defs>{body}</svg>")


# ---------------------------------------------------------------- characters
CHARS = {
    "you": dict(skin=PAL["skin_pale"], hair=PAL["hair"], style="messy", shirt="#2a4652", shirt_sh="#1d333c", bags=True, hood=True),
    "mom": dict(skin=PAL["skin"], hair="#4f3528", style="bob", shirt="#62506a", shirt_sh="#4a3c52", bags=False),
    "stranger": dict(skin="#b39684", hair="#2a2a30", style="beanie", shirt="#4d535c", shirt_sh="#393e46", bags=True, stubble=True, phones=True),
    "teacher": dict(skin=PAL["skin"], hair="#47271f", style="bun", shirt="#2d4b40", shirt_sh="#21372f", glasses=True, collar=True),
    "kid1": dict(skin="#b89a87", hair="#2d2219", style="short", shirt="#3b3550", shirt_sh="#2b263b"),
    "kid2": dict(skin="#a88672", hair="#18161c", style="bob", shirt="#40404a", shirt_sh="#2f2f37"),
    "kid3": dict(skin="#c9ab98", hair="#5a3f2b", style="short", shirt="#2f4048", shirt_sh="#222f35"),
    "man1": dict(skin="#b08e7a", hair="#222", style="short", shirt="#3a3f4f", shirt_sh="#2b2f3b"),
    "wom1": dict(skin="#c2a08c", hair="#3a2622", style="bob", shirt="#4b3a4a", shirt_sh="#372a36"),
}


def person(pen, who, expr="open", view="front", sw=7.0, arms="down", rim=0.0, mouth=None, look=(0, 0)):
    """Local coords: head centre (0,0); head ~95x110; torso to y~520."""
    c = CHARS[who]
    o = []
    skin = c["skin"]
    # ---- torso
    torso = [(-62, 100), (62, 100), (150, 150), (182, 300), (190, 540), (-190, 540), (-182, 300), (-150, 150)]
    tid = cid()
    td = pen.smooth(torso, True, 3)
    o.append(f'<clipPath id="{tid}"><path d="{td}"/></clipPath>')
    o.append(P(td, c["shirt"], sw))
    o.append(f'<g clip-path="url(#{tid})">' + P(pen.blob(150, 330, 90, 260), c["shirt_sh"], 0) + "</g>")
    if c.get("hood") and view == "front":
        o.append(P(pen.smooth([(-95, 105), (-60, 150), (0, 175), (60, 150), (95, 105), (40, 125), (-40, 125)], True, 2), c["shirt_sh"], sw))
        o.append(P(pen.smooth([(-25, 170), (-28, 260)], False, 1.5), "none", sw * 0.6))
        o.append(P(pen.smooth([(25, 170), (28, 260)], False, 1.5), "none", sw * 0.6))
    if c.get("collar") and view == "front":
        o.append(P(pen.poly([(-48, 100), (0, 175), (48, 100)], True, 2), "#c9c6c0", sw))
        o.append(P(pen.poly([(-62, 100), (-10, 230), (-70, 220)], True, 2), c["shirt_sh"], sw * 0.8))
        o.append(P(pen.poly([(62, 100), (10, 230), (70, 220)], True, 2), c["shirt_sh"], sw * 0.8))
    # ---- arms
    if arms == "down":
        for sx in (-1, 1):
            o.append(P(pen.smooth([(sx * 150, 160), (sx * 205, 260), (sx * 215, 470), (sx * 170, 475), (sx * 160, 280)], True, 2), c["shirt"], sw))
            o.append(P(pen.blob(sx * 195, 495, 30, 34), skin, sw))
    elif arms == "mug":
        o.append(P(pen.smooth([(-150, 160), (-205, 260), (-215, 470), (-170, 475), (-160, 280)], True, 2), c["shirt"], sw))
        o.append(P(pen.blob(-195, 495, 30, 34), skin, sw))
        o.append(P(pen.smooth([(150, 160), (200, 250), (190, 340), (60, 350), (60, 310), (150, 290), (150, 240)], True, 2), c["shirt"], sw))
        o.append(P(pen.rect(-5, 250, 80, 95, 2), "#7f8794", sw))
        o.append(P(pen.smooth([(75, 270), (105, 285), (100, 320), (75, 325)], False, 1), "none", sw))
        o.append(P(pen.blob(55, 330, 32, 28), skin, sw))
        for k in range(2):
            o.append(P(pen.smooth([(20 + k * 30, 235), (10 + k * 30, 205), (25 + k * 30, 180), (15 + k * 30, 150)], False, 2), "none", sw * 0.5, PAL["cold2"], 0.6))
    elif arms == "phone":
        for sx in (-1, 1):
            o.append(P(pen.smooth([(sx * 150, 160), (sx * 200, 260), (sx * 150, 360), (sx * 30, 380), (sx * 30, 340), (sx * 130, 300), (sx * 150, 240)], True, 2), c["shirt"], sw))
        o.append(P(pen.rect(-45, 300, 90, 130, 2), "#1b1f29", sw))
        o.append(P(pen.rect(-33, 312, 66, 104, 1), "#7fa6d6", 0, op=0.85))
        o.append(P(pen.blob(-40, 365, 28, 26), skin, sw))
        o.append(P(pen.blob(40, 365, 28, 26), skin, sw))
    elif arms == "pole":  # right hand up gripping a pole
        o.append(P(pen.smooth([(-150, 160), (-205, 260), (-215, 470), (-170, 475), (-160, 280)], True, 2), c["shirt"], sw))
        o.append(P(pen.blob(-195, 495, 30, 34), skin, sw))
        o.append(P(pen.smooth([(140, 150), (215, 40), (235, -150), (190, -150), (170, 20), (110, 120)], True, 2), c["shirt"], sw))
        o.append(P(pen.blob(212, -180, 34, 38), skin, sw))
    elif arms == "chalk":  # back view, right arm raised to board
        o.append(P(pen.smooth([(-150, 160), (-205, 260), (-215, 470), (-170, 475), (-160, 280)], True, 2), c["shirt"], sw))
        o.append(P(pen.blob(-195, 495, 30, 34), skin, sw))
        o.append(P(pen.smooth([(140, 150), (230, 60), (280, -90), (240, -105), (190, 30), (110, 120)], True, 2), c["shirt"], sw))
        o.append(P(pen.blob(262, -120, 30, 32), skin, sw))
    # ---- neck + head
    o.append(P(pen.rect(-34, 60, 68, 70, 1.5), PAL["skin_sh"] if view == "front" else skin, sw))
    hd = pen.blob(0, 0, 95, 112, 18, 0.018)
    style = c["style"]
    if view == "front":
        # back hair
        if style == "bob":
            o.append(P(pen.smooth([(-118, -40), (-128, 60), (-112, 105), (-60, 92), (60, 92), (112, 105), (128, 60), (118, -40), (60, -130), (-60, -130)], True, 3), c["hair"], sw))
        if style == "bun":
            o.append(P(pen.blob(0, -128, 52, 46), c["hair"], sw))
            o.append(P(pen.smooth([(-108, -20), (-110, 50), (-90, 70), (90, 70), (110, 50), (108, -20), (60, -118), (-60, -118)], True, 3), c["hair"], sw))
        for sx in (-1, 1):
            o.append(P(pen.blob(sx * 95, 12, 18, 26), skin, sw))
        hid = cid()
        o.append(f'<clipPath id="{hid}"><path d="{hd}"/></clipPath>')
        o.append(P(hd, skin, sw))
        o.append(f'<g clip-path="url(#{hid})">' + P(pen.blob(105, 30, 60, 140), PAL["skin_sh"], 0, op=0.55) + "</g>")
        if c.get("stubble"):
            for i in range(26):
                a = math.pi * (0.15 + 0.7 * pen.r.random())
                rr = 70 + pen.r.random() * 25
                o.append(f'<circle cx="{math.cos(a)*rr*0.95:.1f}" cy="{math.sin(a)*rr*0.85+20:.1f}" r="2.2" fill="#3a2f2c" opacity="0.7"/>')
        o.append(face(pen, expr, sw, c, mouth, look))
        # front hair
        o.append(hair_front(pen, style, c["hair"], sw))
        if c.get("phones"):
            o.append(P(pen.smooth([(-112, 0), (-105, -95), (0, -150), (105, -95), (112, 0)], False, 2), "none", sw * 1.6, OUT))
            for sx in (-1, 1):
                o.append(P(pen.blob(sx * 108, 10, 24, 36), "#20232b", sw))
        if rim > 0:
            o.append(f'<g clip-path="url(#{hid})">' + P(pen.blob(0, -150, 140, 80), "#ff4d1f", 0, op=rim) + "</g>")
    else:  # back view
        if style == "bun":
            o.append(P(pen.blob(0, -118, 54, 48), c["hair"], sw))
        for sx in (-1, 1):
            o.append(P(pen.blob(sx * 95, 12, 18, 26), skin, sw))
        o.append(P(hd, c["hair"], sw))
        if style == "messy":
            o.append(P(hair_spikes(pen, back=True), c["hair"], sw))
        if style == "bob":
            o.append(P(pen.smooth([(-118, -40), (-128, 60), (-112, 105), (0, 100), (112, 105), (128, 60), (118, -40), (60, -130), (-60, -130)], True, 3), c["hair"], sw))
        if c.get("hood"):
            o.append(P(pen.smooth([(-120, 90), (-70, 150), (0, 165), (70, 150), (120, 90), (60, 120), (-60, 120)], True, 2), c["shirt_sh"], sw))
        o.append(P(pen.smooth([(-40, -60), (-20, 20), (-30, 70)], False, 2), "none", sw * 0.5, "#2a2630"))
        o.append(P(pen.smooth([(30, -80), (40, 0), (25, 60)], False, 2), "none", sw * 0.5, "#2a2630"))
        if rim > 0:
            hid = cid()
            o.append(f'<clipPath id="{hid}"><path d="{hd}"/></clipPath>')
            o.append(f'<g clip-path="url(#{hid})">' + P(pen.blob(0, -150, 140, 80), "#ff4d1f", 0, op=rim) + "</g>")
    return "".join(o)


def hair_spikes(pen, back=False):
    pts = []
    n = 13
    for i in range(n + 1):
        a = math.pi * (1.02 + 0.96 * i / n)
        r = 128 if i % 2 == 0 else 104
        pts.append((math.cos(a) * r * 1.02, math.sin(a) * r * 1.05 - 8))
    if back:
        pts += [(100, 40), (60, 70), (0, 80), (-60, 70), (-100, 40)]
    else:
        pts += [(100, -10), (78, -48), (52, -22), (30, -60), (2, -26), (-28, -62), (-50, -24), (-78, -50), (-100, -8)]
    return pen.cr([(x + pen.u(2), y + pen.u(2)) for x, y in pts])


def hair_front(pen, style, col, sw):
    if style == "messy":
        return P(hair_spikes(pen), col, sw)
    if style == "bob":
        return P(pen.smooth([(-112, 0), (-108, -70), (-50, -122), (40, -125), (105, -75), (112, 10), (90, -40), (40, -62), (-20, -55), (-70, -30)], True, 2.5), col, sw)
    if style == "bun":
        return P(pen.smooth([(-104, -5), (-95, -80), (-40, -116), (0, -112), (40, -116), (95, -80), (104, -5), (80, -48), (6, -70), (0, -100), (-6, -70), (-80, -48)], True, 2), col, sw)
    if style == "beanie":
        a = P(pen.smooth([(-110, -40), (-100, -110), (-40, -152), (40, -152), (100, -110), (110, -40)], True, 2), "#2b2f39", sw)
        b = P(pen.rect(-116, -62, 232, 42, 2), "#363b47", sw)
        return a + b
    if style == "short":
        return P(pen.smooth([(-100, -5), (-98, -80), (-40, -122), (40, -124), (100, -80), (100, -5), (75, -55), (20, -70), (-40, -62), (-80, -40)], True, 2), col, sw)
    return ""


def face(pen, expr, sw, c, mouth=None, look=(0, 0)):
    o = []
    lx, ly = look
    ex, ey = 38, -2
    if expr in ("open", "wide", "smile", "worried", "flat"):
        rw, rh = (25, 25) if expr == "wide" else (22, 15 if expr == "flat" else 17)
        pr = 5 if expr == "wide" else 8
        for sx in (-1, 1):
            o.append(P(pen.blob(sx * ex, ey, rw, rh, 12, 0.03), PAL["eye"], sw * 0.8))
            o.append(f'<circle cx="{sx*ex+lx+pen.u(0.6):.1f}" cy="{ey+ly+pen.u(0.6):.1f}" r="{pr}" fill="{OUT}"/>')
            if expr == "flat":
                o.append(P(pen.smooth([(sx * ex - 26, ey - 6), (sx * ex, ey - 14), (sx * ex + 26, ey - 6), (sx * ex + 26, ey - 18), (sx * ex - 26, ey - 18)], True, 1), c["skin"], sw * 0.7))
        # brows
        if expr in ("wide", "worried"):
            for sx in (-1, 1):
                o.append(P(pen.smooth([(sx * 62, ey - 38), (sx * 38, ey - 42), (sx * 16, ey - 54)], False, 1.5), "none", sw * 1.1))
        elif expr == "smile":
            for sx in (-1, 1):
                o.append(P(pen.smooth([(sx * 62, ey - 32), (sx * 38, ey - 38), (sx * 16, ey - 30)], False, 1.5), "none", sw * 1.1))
        else:
            for sx in (-1, 1):
                o.append(P(pen.smooth([(sx * 62, ey - 34), (sx * 38, ey - 40), (sx * 16, ey - 36)], False, 1.5), "none", sw * 1.1))
    elif expr == "closed":
        for sx in (-1, 1):
            o.append(P(pen.smooth([(sx * 58, ey + 2), (sx * 38, ey + 10), (sx * 18, ey + 2)], False, 1), "none", sw))
            o.append(P(pen.smooth([(sx * 62, ey - 30), (sx * 38, ey - 34), (sx * 16, ey - 30)], False, 1.5), "none", sw * 1.0))
    if c.get("bags"):
        for sx in (-1, 1):
            o.append(P(pen.smooth([(sx * 56, ey + 24), (sx * 38, ey + 31), (sx * 20, ey + 24)], False, 1), "none", sw * 0.45, "#6e5a63"))
    if c.get("glasses"):
        for sx in (-1, 1):
            o.append(P(pen.blob(sx * ex, ey, 31, 27, 14, 0.015), "none", sw * 0.8))
        o.append(P(pen.smooth([(-8, ey - 2), (0, ey - 7), (8, ey - 2)], False, 1), "none", sw * 0.8))
        o.append(P(pen.poly([(-60, ey - 18), (-38, ey - 28), (-30, ey - 8)], True, 1), "#ffffff", 0, op=0.18))
    # nose
    o.append(P(pen.smooth([(4, 18), (12, 42), (-2, 46)], False, 1), "none", sw * 0.7))
    m = mouth or {"wide": "o", "smile": "smile", "closed": "flat", "worried": "frown"}.get(expr, "flat")
    if m == "o":
        o.append(P(pen.blob(0, 74, 13, 17), "#2a1a1e", sw * 0.8))
    elif m == "smile":
        o.append(P(pen.smooth([(-30, 68), (-6, 78), (24, 72), (38, 60)], False, 1), "none", sw * 0.8))
    elif m == "frown":
        o.append(P(pen.smooth([(-24, 78), (0, 70), (24, 78)], False, 1), "none", sw * 0.8))
    elif m == "open_slack":
        o.append(P(pen.blob(0, 74, 18, 9), "#2a1a1e", sw * 0.8))
    else:
        o.append(P(pen.smooth([(-22, 74), (0, 72), (22, 75)], False, 1), "none", sw * 0.8))
    return "".join(o)


def dog(pen, sw=7.0, expr="open"):
    """Sitting dog, local origin = head centre."""
    o = []
    fur, fur_sh, dark = "#77695d", "#5c5047", "#3c332e"
    o.append(P(pen.smooth([(120, 300), (200, 260), (230, 200), (215, 185), (180, 240), (120, 260)], True, 2), fur, sw))  # tail
    o.append(P(pen.smooth([(-110, 90), (-150, 250), (-160, 380), (-90, 410), (90, 410), (160, 380), (150, 250), (110, 90)], True, 3), fur, sw))
    o.append(P(pen.blob(0, 260, 70, 120), "#8d7f72", 0, op=0.8))
    for sx in (-1, 1):
        o.append(P(pen.smooth([(sx * 40, 260), (sx * 60, 400), (sx * 100, 410), (sx * 85, 260)], True, 2), fur, sw))
        o.append(P(pen.blob(sx * 80, 405, 38, 18), fur_sh, sw))
    o.append(P(pen.smooth([(-100, 95), (0, 120), (100, 95), (100, 130), (0, 155), (-100, 130)], True, 1.5), "#23262e", sw))
    o.append(P(pen.blob(0, 150, 14, 14), "#9aa0a8", sw * 0.7))
    o.append(P(pen.blob(0, 0, 105, 95, 16, 0.02), fur, sw))
    for sx in (-1, 1):
        o.append(P(pen.smooth([(sx * 70, -70), (sx * 135, -50), (sx * 150, 60), (sx * 120, 95), (sx * 95, 40)], True, 2), dark, sw))
    o.append(P(pen.blob(0, 50, 62, 45), "#9a8b7d", sw))
    o.append(P(pen.blob(0, 25, 22, 15), OUT, sw * 0.6))
    o.append(P(pen.smooth([(0, 40), (0, 62), (-18, 72)], False, 1), "none", sw * 0.7))
    o.append(P(pen.smooth([(0, 62), (18, 72)], False, 1), "none", sw * 0.7))
    for sx in (-1, 1):
        o.append(P(pen.blob(sx * 40, -20, 15, 17), PAL["eye"], sw * 0.7))
        o.append(f'<circle cx="{sx*40+1:.1f}" cy="-18" r="8" fill="{OUT}"/>')
    return "".join(o)


def walker(pen, who, sw=7.0, seed_shift=0):
    """Tiny background pedestrian (front view, simplified)."""
    return person(pen, who, "flat", "front", sw)


# ---------------------------------------------------------------- environments
def S(s):
    """Outline width for a character drawn at scale s (keeps lines bold but not huge)."""
    return 6.5 * (s ** 0.42) / s


def bg_grad(id_, top, bot):
    return f'<linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bot}"/></linearGradient>'


def radial(id_, col, op=0.8):
    return (f'<radialGradient id="{id_}"><stop offset="0" stop-color="{col}" stop-opacity="{op}"/>'
            f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>')


FULL = (-216, -384, 1512, 2688)


def fill_rect(col, op=None):
    x, y, w, h = FULL
    o = f' opacity="{op}"' if op is not None else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}"{o}/>'


# ======================================================================== SCENES
# Each scene function returns {layer_name: (svg_string, depth)} for a given seed.

def sc_wake(seed):
    p = Pen(seed)
    L = {}
    # background: dark bedroom wall with blind stripes of cold light
    b = [fill_rect(PAL["bg1"])]
    for i in range(7):
        y = -200 + i * 170
        b.append(P(p.poly([(-300, y + 300), (1400, y - 200), (1400, y - 130), (-300, y + 370)], True, 4), PAL["cold2"], 0, op=0.18))
    L["bg"] = (svg_doc("".join(b)), 0.3)
    # pillow + blanket + face (lying, head tilted)
    s = 3.6
    body = []
    body.append(P(p.smooth([(-260, 380), (1340, 420), (1360, 1650), (-280, 1700)], True, 8), "#2c3550", 7))
    L["bed"] = (svg_doc("".join(body)), 0.6)
    bl = [P(p.smooth([(-260, 1450), (300, 1380), (900, 1470), (1360, 1420), (1360, 2400), (-280, 2400)], True, 8), "#3a2f50", 7)]
    for i in range(4):
        bl.append(P(p.smooth([(-200 + i * 380, 1500), (-100 + i * 380, 1800), (-150 + i * 380, 2200)], False, 6), "none", 5, op=0.6))
    for ex in ("closed", "wide"):
        f = person(p, "you", ex, "front", S(s), arms="none", rim=0, look=(0, -4) if ex == "wide" else (0, 0))
        L[f"face_{ex}"] = (svg_doc(G(f, 560, 920, s, rot=-14)), 1.0)
    L["blanket"] = (svg_doc("".join(bl)), 1.1)
    return L


def sc_street(seed):
    p = Pen(seed)
    L = {}
    defs = bg_grad("sky", "#0a0d18", "#2a2a48")
    b = [f'<rect x="-216" y="-384" width="1512" height="2688" fill="url(#sky)"/>']
    # far buildings
    x = -260
    rr = random.Random(7)
    while x < 1350:
        w = rr.randint(160, 260)
        h = rr.randint(400, 900)
        b.append(P(p.rect(x, 760 - h, w, h + 400, 3), rr.choice([PAL["bg2"], PAL["bg3"], PAL["pur2"]]), 6))
        for wy in range(760 - h + 50, 960, 110):
            for wx in range(x + 30, x + w - 50, 70):
                lit = rr.random() < 0.22
                b.append(P(p.rect(wx, wy, 38, 60, 1.5), PAL["warm2"] if lit else "#1a2034", 4, op=0.9 if lit else 1))
        x += w + rr.randint(-10, 20)
    L["far"] = (svg_doc("".join(b), defs), 0.25)
    # street and sidewalk + people
    m = [P(p.poly([(-300, 900), (1400, 900), (1400, 2400), (-300, 2400)], True, 4), "#1c2133", 7),
         P(p.poly([(-300, 900), (1400, 900), (1400, 1010), (-300, 1010)], True, 3), "#2b3248", 6)]
    for i in range(6):
        m.append(P(p.rect(-150 + i * 280, 1380, 140, 22, 2), "#3a4058", 0))
    for lx in (60, 1000):
        m.append(P(p.rect(lx - 12, 400, 24, 600, 2), "#252a3b", 6))
        m.append(P(p.poly([(lx - 70, 400), (lx + 70, 400), (lx + 40, 360), (lx - 40, 360)], True, 2), "#252a3b", 6))
        m.append(f'<ellipse cx="{lx}" cy="640" rx="200" ry="420" fill="url(#lamp)"/>')
    defs2 = radial("lamp", "#8ea4c2", 0.16)
    peds = [("man1", 170, 830, 0.36), ("wom1", 400, 860, 0.4), ("kid1", 640, 820, 0.32),
            ("kid3", 880, 850, 0.38), ("stranger", 280, 1110, 0.5), ("wom1", 760, 1140, 0.52),
            ("man1", 520, 1300, 0.6)]
    for who, px, py, s in peds:
        m.append(G(person(p, who, "flat", "front", S(s) * 1.25), px, py, s))
    L["street"] = (svg_doc("".join(m), defs2), 0.55)
    # window frame foreground
    f = []
    f.append(P(f"M-216,-384 H1296 V2304 H-216 Z M40,120 H1040 V1660 H40 Z", "#141018", 0, extra=' fill-rule="evenodd"'))
    f.append(P(p.rect(40, 120, 1000, 1540, 3), "none", 14))
    f.append(P(p.rect(530, 120, 20, 1540, 2), "#211b26", 8))
    f.append(P(p.rect(-40, 1650, 1160, 90, 3), "#2a2230", 9))
    f.append(P(p.smooth([(-216, -384), (110, -300), (170, 400), (120, 1200), (50, 1750), (-216, 1850)], True, 6), "#2e2540", 9))
    for i in range(4):
        f.append(P(p.smooth([(0 + i * 40, -200), (60 + i * 35, 600), (20 + i * 30, 1500)], False, 4), "none", 5, op=0.7))
    # plant on sill
    f.append(P(p.poly([(880, 1655), (1020, 1655), (1000, 1540), (900, 1540)], True, 2), "#3b3445", 8))
    for a in (-0.9, -0.4, 0.1, 0.6, 1.0):
        f.append(P(p.blob(950 + math.sin(a) * 80, 1490 - math.cos(a) * 60, 26, 60, 10, 0.04, a), "#22382f", 7))
    L["frame"] = (svg_doc("".join(f)), 1.0)
    return L


def sc_kitchen(seed):
    p = Pen(seed)
    L = {}
    b = [fill_rect(PAL["teal"])]
    for i in range(-2, 14):  # tiles
        b.append(P(p.poly([(-216, 900 + i * 0), (1296, 900)], False, 2), "none", 0))
    for yy in range(1000, 1300, 90):
        b.append(P(p.poly([(-216, yy), (1296, yy)], False, 2), "none", 3, "#123036"))
    for xx in range(-200, 1300, 90):
        b.append(P(p.poly([(xx, 960), (xx, 1300)], False, 2), "none", 3, "#123036"))
    b.append(P(p.rect(-216, 960, 1512, 340, 2), "#1f4148", 0, op=0.5))
    # window (grey dawn)
    b.append(P(p.rect(620, 150, 420, 520, 3), "#5d7393", 9))
    b.append(P(p.rect(640, 170, 380, 480, 2), "#7d93b0", 0))
    b.append(P(p.poly([(830, 150), (830, 670)], False, 2), "none", 10))
    b.append(P(p.poly([(620, 410), (1040, 410)], False, 2), "none", 10))
    # cabinets
    for i in range(3):
        b.append(P(p.rect(-160 + i * 230, 100, 220, 400, 3), "#26343d", 8))
        b.append(P(p.rect(-80 + i * 230, 280, 60, 14, 1), "#5a6470", 5))
    # wall clock
    b.append(P(p.blob(500, 290, 85, 85), "#d1cfc8", 8))
    b.append(P(p.poly([(500, 290), (500, 225)], False, 1), "none", 8))
    b.append(P(p.poly([(500, 290), (545, 315)], False, 1), "none", 7))
    # counter
    b.append(P(p.rect(-216, 1300, 1512, 80, 3), "#3a3340", 8))
    b.append(P(p.rect(-216, 1380, 1512, 1000, 3), "#2a2532", 8))
    for i in range(5):
        b.append(P(p.rect(-180 + i * 300, 1430, 260, 500, 3), "#302a3a", 6))
    b.append(P(p.rect(-216, 1950, 1512, 400, 3), "#1a1620", 6))
    L["bg"] = (svg_doc("".join(b)), 0.35)
    L["mom"] = (svg_doc(G(person(p, "mom", "open", "front", S(1.55), arms="mug", look=(6, 0), mouth="smile"), 330, 820, 1.55)), 0.75)
    L["dog"] = (svg_doc(G(dog(p, S(1.2)), 820, 1400, 1.2)), 0.8)
    # foreground table edge with bowl + chair
    f = [P(p.poly([(-260, 1800), (1340, 1760), (1340, 2400), (-260, 2400)], True, 5), "#3d3241", 9),
         P(p.poly([(-260, 1800), (1340, 1760), (1340, 1830), (-260, 1870)], True, 3), "#4b3f51", 7),
         P(p.smooth([(220, 1740), (480, 1740), (450, 1810), (250, 1810)], True, 3), "#8b93a0", 8),
         P(p.blob(350, 1742, 130, 24), "#5b4a3a", 6)]
    L["fg"] = (svg_doc("".join(f)), 1.25)
    return L


def _bus_outside(p):
    defs = bg_grad("nsky", "#0b0e1a", "#1c1f36")
    o = [f'<rect x="-216" y="-384" width="5000" height="2688" fill="url(#nsky)"/>']
    rr = random.Random(11)
    x = -300
    while x < 4800:
        w = rr.randint(140, 260)
        h = rr.randint(300, 700)
        o.append(P(p.rect(x, 1000 - h, w, h + 300, 3), rr.choice([PAL["bg2"], PAL["pur"], PAL["bg3"]]), 6))
        for wy in range(1000 - h + 40, 1000, 90):
            for wx in range(x + 25, x + w - 40, 60):
                if rr.random() < 0.3:
                    o.append(P(p.rect(wx, wy, 30, 46, 1), PAL["warm2"], 3, op=0.8))
        if rr.random() < 0.5:
            o.append(f'<ellipse cx="{x+w/2}" cy="560" rx="120" ry="200" fill="url(#sl)"/>')
        x += w + rr.randint(10, 60)
    defs += radial("sl", "#c9d4e6", 0.22)
    x0, y0, _, h0 = VB
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} 5000 {h0}" width="5000" height="{h0}"><defs>{defs}</defs>{"".join(o)}</svg>')


def _bus_interior(p, seats_empty=False):
    o = []
    hole = "M380,470 H1296 V1000 H380 Z M-216,470 H330 V1000 H-216 Z"
    o.append(P(f"M-216,-384 H1296 V2304 H-216 Z {hole}", "#232a3c", 0, extra=' fill-rule="evenodd"'))
    o.append(P(p.rect(-216, -384, 1512, 700, 3), "#1a1f2e", 7))  # ceiling
    o.append(P(p.poly([(-216, 300), (1296, 300)], False, 2), "none", 14, "#5a6274"))  # rail
    for hx in range(-150, 1300, 170):
        o.append(P(p.poly([(hx, 300), (hx, 380)], False, 1), "none", 5))
        o.append(P(p.blob(hx, 405, 24, 28), "none", 9, "#5a6274"))
    o.append(P(p.rect(-216, 455, 1512, 30, 2), "#2d3548", 7))
    o.append(P(p.rect(-216, 990, 1512, 40, 2), "#2d3548", 7))
    o.append(P(p.rect(330, 455, 50, 575, 2), "#2d3548", 7))
    # seats back row
    for sx in (-120, 160, 440, 720, 1000):
        o.append(P(p.smooth([(sx - 120, 760), (sx + 120, 760), (sx + 130, 1270), (sx - 130, 1270)], True, 3), "#3b2f4d", 8))
        o.append(P(p.poly([(sx - 100, 820), (sx + 100, 820)], False, 2), "none", 4, "#2b223a"))
    o.append(P(p.rect(-216, 1200, 1512, 130, 3), "#33284a", 8))  # seat bench
    o.append(P(p.rect(-216, 1330, 1512, 1000, 3), "#1b1f2b", 8))  # floor
    for i in range(8):
        o.append(P(p.poly([(-216, 1420 + i * 120), (1296, 1420 + i * 120)], False, 3), "none", 3, "#242a39"))
    return "".join(o)


def sc_bus(seed, collapsed=False):
    p = Pen(seed)
    L = {}
    L["outside"] = (_bus_outside(p), 0.2)
    L["interior"] = (svg_doc(_bus_interior(p)), 0.6)
    chars = []
    chars.append(G(person(p, "wom1", "flat", "front", S(1.25), arms="phone", look=(0, 8)), 150, 960, 1.25))
    chars.append(G(person(p, "man1", "flat", "front", S(1.3), arms="phone", look=(0, 8)), 930, 950, 1.3))
    if not collapsed:
        chars.append(G(person(p, "stranger", "flat", "front", S(1.45), arms="down", look=(0, 6)), 545, 900, 1.45))
    L["chars"] = (svg_doc("".join(chars)), 0.75)
    if collapsed:
        L["body"] = (svg_doc(G(person(p, "stranger", "closed", "front", S(1.35), arms="down", mouth="open_slack"), 420, 1560, 1.35, rot=-78)), 0.85)
    f = [P(p.rect(1110, -384, 60, 2700, 2), "#4b5366", 9), P(p.rect(1125, -384, 12, 2700, 1), "#7d869a", 0, op=0.6)]
    L["fg"] = (svg_doc("".join(f)), 1.3)
    return L


def sc_reaction(seed):
    p = Pen(seed)
    L = {}
    L["interior"] = (svg_doc(_bus_interior(p)), 0.4)
    L["you"] = (svg_doc(G(person(p, "you", "wide", "front", S(2.9), arms="pole", look=(-8, 4)), 560, 900, 2.9)), 1.0)
    L["pole"] = (svg_doc(P(p.rect(820, -384, 70, 2700, 2), "#4b5366", 9)), 1.0)
    return L


def sc_mirror(seed):
    p = Pen(seed)
    L = {}
    mx, my, mw, mh = 120, 220, 840, 1180
    # reflected room
    r = [P(p.rect(mx - 20, my - 20, mw + 40, mh + 40, 2), PAL["teal2"], 0)]
    for yy in range(my, my + mh, 100):
        r.append(P(p.poly([(mx, yy), (mx + mw, yy)], False, 2), "none", 3, "#1a3b42"))
    for xx in range(mx, mx + mw, 100):
        r.append(P(p.poly([(xx, my), (xx, my + mh)], False, 2), "none", 3, "#1a3b42"))
    # open door to dark hallway (left in reflection)
    r.append(P(p.rect(180, 330, 300, 900, 3), "#0b0d15", 8))
    r.append(P(p.rect(160, 310, 340, 30, 2), "#2a3a42", 6))
    r.append(G(person(p, "mom", "open", "front", S(0.62), arms="down", look=(10, 0)), 330, 640, 0.62))
    r.append(G(dog(p, S(0.42)), 420, 1000, 0.42))
    r.append(P(p.blob(540, 330, 260, 60), "#e6e0c8", 0, op=0.12))
    L["room"] = (svg_doc("".join(r)), 0.55)
    for ex, mo in (("worried", "frown"), ("smile", "smile")):
        L[f"refl_{ex}"] = (svg_doc(G(person(p, "you", "worried" if ex == "worried" else "flat", "front", S(1.9), arms="down", mouth=mo, rim=0, look=(0, -2)), 620, 860, 1.9)), 0.6)
    # wall with hole + frame + sheen
    w = [P(f"M-216,-384 H1296 V2304 H-216 Z M{mx},{my} H{mx+mw} V{my+mh} H{mx} Z", "#16303a", 0, extra=' fill-rule="evenodd"')]
    for yy in range(-300, 2300, 110):
        if my < yy < my + mh:
            w.append(P(p.poly([(-216, yy), (mx, yy)], False, 2), "none", 3, "#0f252c"))
            w.append(P(p.poly([(mx + mw, yy), (1296, yy)], False, 2), "none", 3, "#0f252c"))
        else:
            w.append(P(p.poly([(-216, yy), (1296, yy)], False, 2), "none", 3, "#0f252c"))
    w.append(P(p.rect(mx, my, mw, mh, 3), "none", 22, "#2c2a33"))
    w.append(P(p.rect(mx, my, mw, mh, 3), "none", 7))
    for k in range(3):
        w.append(P(p.poly([(mx + 100 + k * 90, my + mh), (mx + 380 + k * 90, my), (mx + 420 + k * 90, my), (mx + 140 + k * 90, my + mh)], True, 2), "#ffffff", 0, op=0.05))
    w.append(f'<rect x="-216" y="-384" width="1512" height="500" fill="url(#bulb)"/>')
    L["wall"] = (svg_doc("".join(w), radial("bulb", "#e6e0c8", 0.18)), 0.6)
    # sink + you from behind
    f = [P(p.smooth([(-100, 1520), (1180, 1520), (1120, 1720), (-40, 1720)], True, 4), "#b9bec8", 9),
         P(p.blob(540, 1560, 300, 40), "#7d8492", 7),
         P(p.rect(-216, 1720, 1512, 700, 3), "#232633", 9)]
    L["sink"] = (svg_doc("".join(f)), 0.9)
    L["back"] = (svg_doc(G(person(p, "you", "open", "back", S(2.5), arms="down"), 470, 1640, 2.5)), 1.15)
    return L


def sc_class(seed):
    p = Pen(seed)
    L = {}
    b = [fill_rect(PAL["pur"])]
    b.append(P(p.rect(-120, 180, 1320, 820, 3), "#2b3a33", 10))
    b.append(P(p.rect(-120, 180, 1320, 820, 3), "none", 22, "#4a3a2e"))
    for txt_y in (300, 380, 460):
        b.append(P(p.smooth([(-60, txt_y), (100, txt_y - 10), (260, txt_y + 6), (420, txt_y - 4)], False, 4), "none", 5, "#a9b2a8", 0.6))
    b.append(P(p.smooth([(700, 560), (900, 540), (1080, 560)], False, 4), "none", 5, "#a9b2a8", 0.6))
    b.append(P(p.blob(980, 90, 70, 70), "#d1cfc8", 8))
    b.append(P(p.rect(-216, 1000, 1512, 1400, 3), "#1e1a2b", 8))
    L["bg"] = (svg_doc("".join(b)), 0.4)
    L["teach_back"] = (svg_doc(G(person(p, "teacher", "open", "back", S(1.35), arms="chalk"), 560, 760, 1.35)), 0.65)
    L["teach_front"] = (svg_doc(G(person(p, "teacher", "flat", "front", S(1.35), arms="down", look=(0, 3), rim=0), 560, 760, 1.35)), 0.65)
    d = [P(p.rect(-216, 1260, 1512, 80, 3), "#3c2f2a", 8)]
    for who, x, y, s in (("kid1", 120, 1450, 1.4), ("kid2", 540, 1480, 1.5), ("kid3", 960, 1450, 1.4)):
        d.append(G(person(p, who, "open", "back", S(s)), x, y, s))
    d.append(P(p.rect(-216, 1900, 1512, 600, 3), "#2d2430", 9))
    L["students"] = (svg_doc("".join(d)), 1.0)
    return L


def sc_compare(seed):
    p = Pen(seed)
    L = {}
    top = [P(p.rect(-216, -384, 1512, 1346, 2), "#243229", 0)]
    for txt_y in (100, 180, 260):
        top.append(P(p.smooth([(-100, txt_y), (100, txt_y - 10), (300, txt_y + 6)], False, 4), "none", 5, "#a9b2a8", 0.4))
    top.append(G(person(p, "teacher", "flat", "front", S(2.4), arms="down", look=(0, 2), rim=0), 560, 610, 2.4))
    L["top"] = (svg_doc("".join(top)), 0.0)
    bot = [P(p.rect(-216, 958, 1512, 1346, 2), PAL["teal2"], 0)]
    for yy in range(958, 2304, 100):
        bot.append(P(p.poly([(-216, yy), (1296, yy)], False, 2), "none", 3, "#1a3b42"))
    bot.append(G(person(p, "you", "worried", "front", S(2.4), arms="down", rim=0), 520, 1560, 2.4))
    L["bot"] = (svg_doc(f'<clipPath id="cb"><rect x="-216" y="958" width="1512" height="1346"/></clipPath><g clip-path="url(#cb)">{"".join(bot)}</g>'), 0.0)
    L["divider"] = (svg_doc(P(p.poly([(-216, 958), (1296, 958)], False, 3), "none", 18)), 0.0)
    return L


def sc_hall(seed):
    p = Pen(seed)
    L = {}
    vx, vy = 540, 820
    b = [fill_rect("#121626")]
    b.append(P(p.poly([(-216, 2304), (vx - 80, vy + 90), (vx + 80, vy + 90), (1296, 2304)], True, 3), "#1d2132", 7))
    b.append(P(p.poly([(-216, -384), (vx - 80, vy - 150), (vx + 80, vy - 150), (1296, -384)], True, 3), "#0f1220", 7))
    b.append(P(p.rect(vx - 80, vy - 150, 160, 240, 2), "#2c3550", 7))
    b.append(P(p.rect(vx - 30, vy - 110, 60, 200, 2), "#5d7393", 5))
    for side in (-1, 1):
        for k in range(9):
            t0 = k / 9
            t1 = (k + 0.85) / 9

            def pt(t, yy):
                ex = -216 if side < 0 else 1296
                x = ex + (vx + side * 80 - ex) * (t ** 0.6)
                yb = 2304 + (vy + 90 - 2304) * (t ** 0.6)
                yt = -384 + (vy - 150 + 384) * (t ** 0.6)
                return (x, yt + (yb - yt) * yy)
            a, bb, c, d = pt(t0, 0.2), pt(t1, 0.2), pt(t1, 0.78), pt(t0, 0.78)
            b.append(P(p.poly([a, bb, c, d], True, 2), "#2a3350" if k % 2 else "#253048", 5))
            ma = pt((t0 + t1) / 2, 0.3)
            b.append(P(p.poly([ma, pt((t0 + t1) / 2, 0.7)], False, 2), "none", 3, "#3b4666"))
    for k in range(5):
        t = (k + 0.5) / 5
        y = -384 + (vy - 150 + 384) * (t ** 0.6) + 40
        w = 400 * (1 - t ** 0.6) + 30
        b.append(P(p.rect(vx - w / 2, y, w, 18 * (1 - t) + 6, 2), "#c8d0de", 3, op=0.55))
    b.append(f'<ellipse cx="{vx}" cy="{vy+400}" rx="260" ry="700" fill="url(#hl)"/>')
    L["bg"] = (svg_doc("".join(b), radial("hl", "#8ea4c2", 0.12)), 0.35)
    L["teacher"] = (svg_doc(G(person(p, "teacher", "open", "back", S(0.62)), 0, 0, 0.62)), 0.7)  # positioned by animation
    L["you"] = (svg_doc(G(person(p, "you", "open", "back", S(2.7)), 260, 1830, 2.7)), 1.2)
    return L


SCENES = {
    "S01_wake": sc_wake, "S02_street": sc_street, "S03_kitchen": sc_kitchen,
    "S04_bus": sc_bus, "S05_collapse": lambda s: sc_bus(s, True), "S06_reaction": sc_reaction,
    "S07_mirror": sc_mirror, "S08_class": sc_class, "S09_compare": sc_compare, "S10_choice": sc_hall,
}
