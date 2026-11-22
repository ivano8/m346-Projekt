"""Sound design + mix.

SFX / music: if an ElevenLabs file exists (audio/sfx/el_<name>.mp3, audio/music/el_music.mp3) it is used,
otherwise a procedurally synthesised placeholder is generated (and saved to audio/sfx/<name>.wav).
Output: build/mix.wav (48 kHz stereo, loudness-normalised later by ffmpeg).
"""
import json, os, random, subprocess
import numpy as np
import soundfile as sf
from scipy import signal

SR = 48000
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
rng = np.random.default_rng(7)


def T(d):
    return np.arange(int(d * SR)) / SR


def lp(x, f, o=2):
    return signal.sosfilt(signal.butter(o, f, "low", fs=SR, output="sos"), x)


def hp(x, f, o=2):
    return signal.sosfilt(signal.butter(o, f, "high", fs=SR, output="sos"), x)


def bp(x, f1, f2, o=2):
    return signal.sosfilt(signal.butter(o, [f1, f2], "band", fs=SR, output="sos"), x)


def norm(x, p=0.9):
    m = np.abs(x).max()
    return x / m * p if m > 0 else x


def decode(path):
    raw = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"])
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


# ------------------------------------------------------------------ synth placeholders
def s_hit():
    t = T(2.2)
    f = 32 + 70 * np.exp(-t * 9)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.4)
    click = lp(rng.standard_normal(len(t)), 2500) * np.exp(-t * 40) * 0.8
    metal = sum(np.sin(2 * np.pi * fr * t + rng.uniform(0, 6)) * a for fr, a in ((174, .3), (481, .18), (937, .1), (1310, .06))) * np.exp(-t * 2.8)
    x = np.tanh(1.8 * boom) + click + 0.35 * metal
    return norm(x)


def s_glitch():
    out = []
    d = 0
    while d < 0.42:
        seg = rng.uniform(0.015, 0.06)
        t = T(seg)
        k = rng.integers(0, 4)
        if k == 0:
            s = np.sign(np.sin(2 * np.pi * rng.uniform(150, 2200) * t))
        elif k == 1:
            s = np.round(rng.standard_normal(len(t)) * 2) / 2
        elif k == 2:
            s = np.sin(2 * np.pi * (rng.uniform(800, 4000) - 3000 * t / seg) * t)
        else:
            s = np.zeros(len(t))
        out.append(s * rng.uniform(0.3, 1))
        d += seg
    x = np.concatenate(out)
    x = np.repeat(x[::3], 3)[: len(x)]  # sample-rate crush
    return norm(hp(x, 120), 0.7)


def s_tick(pitch=1.0):
    t = T(0.09)
    x = rng.standard_normal(len(t)) * np.exp(-t * 400)
    x = hp(x, 1500) + 0.6 * np.sin(2 * np.pi * 3100 * pitch * t) * np.exp(-t * 120) + 0.4 * np.sin(2 * np.pi * 1200 * pitch * t) * np.exp(-t * 90)
    return norm(x, 0.8)


def s_heartbeat():
    t = T(0.9)
    x = np.zeros(len(t))
    for st, a in ((0.0, 1.0), (0.26, 0.7)):
        i = int(st * SR)
        tt = t[: len(t) - i]
        f = 38 + 30 * np.exp(-tt * 30)
        x[i:] += a * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 14) * (1 - np.exp(-tt * 400))
    return norm(lp(np.tanh(2 * x), 300))


def s_thud():
    t = T(1.2)
    f = 40 + 60 * np.exp(-t * 15)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5)
    x += lp(rng.standard_normal(len(t)), 600) * np.exp(-t * 18) * 1.5
    rattle = bp(rng.standard_normal(len(t)), 1500, 5000) * np.exp(-((t - 0.08) ** 2) / 0.002) * 0.25
    return norm(np.tanh(2 * x) + rattle)


def s_whoosh():
    t = T(0.7)
    n = rng.standard_normal(len(t))
    env = np.sin(np.pi * np.clip(t / 0.7, 0, 1)) ** 2
    out = np.zeros(len(t))
    for i in range(0, len(t), 2400):
        c = 300 + 3000 * (i / len(t))
        seg = slice(i, i + 2400)
        out[seg] = bp(n[seg], c * 0.6, c * 1.4)
    return norm(lp(out, 6000) * env, 0.7)


def s_riser(d=1.1):
    t = T(d)
    n = rng.standard_normal(len(t))
    x = hp(n, 800) * (t / d) ** 2
    x += np.sin(2 * np.pi * np.cumsum(200 + 900 * (t / d) ** 2) / SR) * (t / d) ** 3 * 0.5
    return norm(x, 0.7)


def s_chalk():
    t = T(1.6)
    x = np.zeros(len(t))
    for st in np.arange(0.05, 1.5, 0.22):
        i = int((st + rng.uniform(0, .05)) * SR)
        L = int(rng.uniform(0.06, 0.16) * SR)
        seg = bp(rng.standard_normal(L), 1800, 6000) * np.hanning(L)
        x[i:i + L] += seg[: len(x) - i]
    return norm(x, 0.5)


def s_drone(d):
    t = T(d)
    x = sum(a * signal.sawtooth(2 * np.pi * f * t + rng.uniform(0, 6)) for f, a in ((55, .5), (55.35, .5), (82.6, .3), (110.4, .15), (77.8, .12)))
    x = lp(x, 260, 3) * (0.75 + 0.25 * np.sin(2 * np.pi * 0.11 * t))
    wind = bp(rng.standard_normal(len(t)), 200, 700) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * t + 1)) * 0.25
    return norm(x + wind, 0.8)


def s_bus(d):
    t = T(d)
    rumble = lp(np.cumsum(rng.standard_normal(len(t))) * 0.02, 180)
    rumble -= lp(rumble, 20)
    hum = np.sin(2 * np.pi * (46 + 2 * np.sin(2 * np.pi * 0.3 * t)) * t) * 0.4
    traffic = bp(rng.standard_normal(len(t)), 300, 2000) * (0.3 + 0.2 * np.sin(2 * np.pi * 0.13 * t)) * 0.3
    return norm(rumble / (np.abs(rumble).max() + 1e-9) + hum + traffic, 0.8)


def s_music(d):
    """Quiet dark ambient bed: D minor pads + sparse music-box notes."""
    t = T(d)
    chords = [(50, 53, 57, 62), (46, 50, 53, 58), (43, 46, 50, 55), (45, 49, 52, 57)]  # Dm Bb Gm A
    out = np.zeros(len(t))
    cl = 4.0
    for ci in range(int(d / cl) + 1):
        notes = chords[ci % 4]
        st = int(ci * cl * SR)
        L = min(int((cl + 1.5) * SR), len(t) - st)
        if L <= 0:
            break
        tt = np.arange(L) / SR
        env = np.minimum(tt / 1.4, 1) * np.minimum(1, np.maximum(0, (cl + 1.5 - tt) / 1.5))
        seg = np.zeros(L)
        for n in notes:
            f = 440 * 2 ** ((n - 69) / 12)
            seg += signal.sawtooth(2 * np.pi * f * tt) + signal.sawtooth(2 * np.pi * f * 1.004 * tt)
        out[st:st + L] += lp(seg, 700, 2) * env * 0.12
    scale = [74, 77, 81, 82, 86, 89, 93]
    tn = 1.0
    while tn < d - 2:
        n = rng.choice(scale)
        f = 440 * 2 ** ((n - 69) / 12)
        st = int(tn * SR)
        L = min(int(2.0 * SR), len(t) - st)
        tt = np.arange(L) / SR
        out[st:st + L] += (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * f * 3 * tt)) * np.exp(-tt * 2.2) * 0.12
        tn += rng.choice([1.0, 1.5, 2.0, 3.0])
    return norm(out, 0.8)


SYNTH = dict(hit=s_hit, glitch=s_glitch, tick=s_tick, heartbeat=s_heartbeat, thud=s_thud, whoosh=s_whoosh,
             riser=s_riser, chalk=s_chalk)


def get(name, synth_fn=None, dur=None):
    el = f"audio/sfx/el_{name}.mp3"
    if os.path.exists(el):
        x = decode(el).mean(1)
        if dur:
            reps = int(np.ceil(dur * SR / len(x)))
            x = np.tile(x, reps)[: int(dur * SR)]
        return norm(x, 0.9), "elevenlabs"
    fn = synth_fn or SYNTH[name]
    x = fn(dur) if dur else fn()
    sf.write(f"audio/sfx/{name}.wav", x.astype(np.float32), SR)
    return x, "placeholder"


# ------------------------------------------------------------------ mix
def main():
    TL = json.load(open("timeline.json"))
    ev = TL["events"]
    SCn = {s["id"]: s for s in TL["scenes"]}
    total = TL["total"]
    N = int(total * SR) + SR
    mix = np.zeros((N, 2))
    vo_bus = np.zeros(N)
    sources = {}

    def place(x, t, g=1.0, pan=0.0):
        i = int(t * SR)
        if i >= N:
            return
        x = x[: N - i]
        mix[i:i + len(x), 0] += x * g * (1 - max(pan, 0))
        mix[i:i + len(x), 1] += x * g * (1 + min(pan, 0))

    lib = {}
    for k in SYNTH:
        lib[k], sources[k] = get(k)
    lib["tick_lo"] = s_tick(0.6)
    # ---------------- VO
    ir_t = T(0.9)
    ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 7)
    ir = lp(ir, 3500)
    ir /= np.abs(ir).sum() ** 0.5 * 6
    vo_src = "placeholder"
    for ln in TL["lines"]:
        if ln["src"].endswith(".mp3"):
            x = decode(ln["src"]).mean(1)
            vo_src = "elevenlabs"
        else:
            x, sr = sf.read(ln["src"])
            x = signal.resample_poly(x, SR // 1000, sr // 1000)
        x = hp(x, 70)
        x = norm(x, 0.85)
        wet = signal.fftconvolve(x, ir)[: len(x) + int(0.5 * SR)]
        y = np.zeros(len(wet))
        y[: len(x)] += x
        y += wet * 0.18
        i = int(ln["start"] * SR)
        y = y[: N - i]
        vo_bus[i:i + len(y)] += y
    sources["voice"] = vo_src
    # ---------------- beds
    drone, sources["drone"] = get("drone", s_drone, total + 1)
    dg = np.full(len(drone), 0.10)
    for sid, g in (("S04_bus", 0.08), ("S05_collapse", 0.2), ("S06_reaction", 0.2), ("S07_mirror", 0.22), ("S08_class", 0.14), ("S09_compare", 0.22), ("S10_choice", 0.25)):
        a, b = int(SCn[sid]["start"] * SR), int(SCn[sid]["end"] * SR)
        dg[a:b] = g
    dg = signal.savgol_filter(dg, 48001, 1) if len(dg) > 48001 else dg
    place(drone[:N] * dg[:N], 0)
    music, sources["music"] = (decode("audio/music/el_music.mp3").mean(1), "elevenlabs") if os.path.exists("audio/music/el_music.mp3") else (s_music(total + 1), "placeholder")
    if sources["music"] == "placeholder":
        sf.write("audio/music/music.wav", music.astype(np.float32), SR)
    music = np.pad(music, (0, max(0, N - len(music))))[:N]
    mg = np.full(N, 0.16)
    a = int(ev["collapse"] * SR)
    mg[a:a + int(2.2 * SR)] = 0.0  # silence after the collapse
    mg[int(ev["endcard"] * SR):] = 0.10
    mg = signal.savgol_filter(mg, 24001, 1)
    # sidechain ducking under VO
    env = lp(np.abs(vo_bus), 6)
    env = np.clip(env / (env.max() + 1e-9) * 4, 0, 1)
    music_g = mg * (1 - 0.55 * env)
    place(music * music_g, 0, 1.0)
    bus, sources["bus"] = get("bus", s_bus, SCn["S05_collapse"]["end"] - SCn["S04_bus"]["start"])
    bs = SCn["S04_bus"]["start"]
    bg = np.ones(len(bus)) * 0.22
    ci = int((ev["collapse"] - bs) * SR)
    bg[ci:] = 0.07
    fade = np.minimum(1, np.arange(len(bus)) / (0.3 * SR)) * np.minimum(1, (len(bus) - np.arange(len(bus))) / (0.3 * SR))
    place(lp(bus, 1200) * bg * fade, bs)
    # ---------------- events
    H = lib["hit"]
    place(lib["glitch"], 0.0, 0.5)
    place(H, ev["eyes_open"], 0.9)
    place(lib["glitch"], ev["eyes_open"], 0.45)
    place(lib["whoosh"], SCn["S02_street"]["start"] - 0.25, 0.5)
    place(H, ev["street_timers"], 0.6)
    for i in range(7):
        place(lib["tick"], ev["street_timers"] + 0.11 * i, 0.35, pan=(i - 3) / 4)
    # kitchen clock ticks
    k0, k1 = SCn["S03_kitchen"]["start"], SCn["S03_kitchen"]["end"]
    t = np.ceil(k0)
    while t < k1:
        place(lib["tick"] if int(t) % 2 else lib["tick_lo"], t, 0.16, 0.3)
        t += 1
    place(H, ev["mom_timer"], 0.6)
    place(lib["glitch"], ev["mom_timer"], 0.2)
    place(H, ev["dog_timer"], 0.55)
    place(lib["glitch"], ev["dog_timer"], 0.2)
    # bus countdown
    place(lib["whoosh"], SCn["S04_bus"]["start"] - 0.25, 0.4)
    place(H, ev["stranger_timer"], 0.7)
    place(lib["glitch"], ev["stranger_timer"], 0.25)
    t = ev["stranger_timer"] + 1
    while t < ev["fast_from"]:
        place(lib["tick"], t, 0.35)
        t += 1
    # accelerating ticks
    last, n = ev["fast_from"], 0
    for i in range(1, 400):
        tt = ev["fast_from"] + (ev["three"] - ev["fast_from"]) * (i / 400) ** (1 / 1.6)
        if tt - last > 0.07:
            place(lib["tick"] if n % 2 else lib["tick_lo"], tt, 0.3)
            last, n = tt, n + 1
    hb = ev["fast_from"] + 0.3
    period = 1.0
    while hb < ev["collapse"] - 0.2:
        place(lib["heartbeat"], hb, 0.7)
        hb += period
        period = max(0.45, period * 0.93)
    for e in ("three", "two", "one"):
        place(lib["tick"], ev[e], 0.8)
        place(H, ev[e], 0.35)
    place(lib["riser"], ev["collapse"] - 1.05, 0.45)
    place(lib["thud"], ev["collapse"], 1.0)
    place(H, ev["collapse"], 1.0)
    place(lib["glitch"], ev["collapse"], 0.5)
    place(lib["heartbeat"], ev["reaction"], 0.8)
    place(lib["heartbeat"], ev["reaction"] + 0.75, 0.6)
    place(lib["whoosh"], ev["reaction"] - 0.2, 0.4)
    # mirror
    place(lib["whoosh"], SCn["S07_mirror"]["start"] - 0.2, 0.35)
    place(lib["tick"], ev["room_timers"], 0.35, -0.4)
    place(lib["tick"], ev["room_timers"] + 0.15, 0.35, -0.2)
    place(lib["riser"], ev["my_timer"] - 1.1, 0.35)
    place(H, ev["my_timer"], 1.0)
    place(lib["glitch"], ev["my_timer"], 0.55)
    hb = ev["my_timer"] + 1.0
    while hb < SCn["S07_mirror"]["end"] - 0.3:
        place(lib["heartbeat"], hb, 0.5)
        hb += 1.05
    place(lib["glitch"], ev["tilt"] + 0.75, 0.3)
    place(lib["glitch"], ev["smile"], 0.4)
    place(H, ev["smile"], 0.35)
    # class
    place(lib["chalk"], SCn["S08_class"]["start"] + 0.1, 0.35)
    place(lib["chalk"], SCn["S08_class"]["start"] + 1.6, 0.3)
    place(lib["whoosh"], ev["turn"] - 0.15, 0.45)
    place(lib["riser"], ev["teacher_timer"] - 1.0, 0.3)
    place(H, ev["teacher_timer"], 1.0)
    place(lib["glitch"], ev["teacher_timer"], 0.55)
    # compare: synced ticks both sides
    t = np.ceil(SCn["S09_compare"]["start"])
    while t < SCn["S09_compare"]["end"]:
        place(lib["tick"], t, 0.4, -0.6)
        place(lib["tick"], t, 0.4, 0.6)
        t += 1
    place(lib["heartbeat"], SCn["S09_compare"]["start"] + 0.5, 0.5)
    place(lib["heartbeat"], SCn["S09_compare"]["start"] + 2.5, 0.5)
    # choice
    place(lib["whoosh"], SCn["S10_choice"]["start"] - 0.2, 0.4)
    place(lib["whoosh"], ev["card_a"] - 0.1, 0.4, -0.5)
    place(H, ev["card_a"], 0.55)
    place(lib["whoosh"], ev["card_b"] - 0.1, 0.4, 0.5)
    place(H, ev["card_b"], 0.55)
    place(H, ev["cta"], 0.6)
    place(lib["riser"], ev["endcard"] - 1.1, 0.35)
    place(H, ev["endcard"], 1.0)
    place(lib["glitch"], ev["endcard"], 0.45)
    place(lib["tick"], total - 0.6, 0.6)
    # ---------------- sum
    mix[:, 0] += vo_bus
    mix[:, 1] += vo_bus
    mix = mix[: int(total * SR)]
    fo = int(0.5 * SR)
    mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
    mix = np.tanh(mix / max(1.0, np.abs(mix).max()) * 1.2) * 0.9
    os.makedirs("build", exist_ok=True)
    sf.write("build/mix.wav", mix.astype(np.float32), SR)
    json.dump(sources, open("build/audio_sources.json", "w"), indent=1)
    print(sources)


if __name__ == "__main__":
    main()
