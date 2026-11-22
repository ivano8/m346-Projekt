"""Builds timeline.json from script.json + the narration audio actually on disk.

VO source priority per line: audio/vo/<ID>.mp3 (ElevenLabs, with <ID>.align.json
character timings) -> audio/vo/<ID>.wav (placeholder TTS, word timings estimated).
"""
import json, os, re, subprocess

FPS = 30


def dur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", path]).decode().strip())


def words_est(text, d):
    words = text.split()
    w = []
    for x in words:
        k = len(re.sub(r"[^A-Za-z0-9]", "", x)) + 1.5
        if x.endswith((",", ".", "?", "!")):
            k += 2.5
        if x.endswith("..."):
            k += 4
        w.append(k)
    tot = sum(w)
    t, out = 0.0, []
    for x, k in zip(words, w):
        out.append([x, round(t * d / tot, 3)])
        t += k
    return out


def words_align(text, align):
    chars, starts = align["characters"], align["character_start_times_seconds"]
    out, i = [], 0
    s = "".join(chars)
    for wd in text.split():
        j = s.find(wd[0], i)
        out.append([wd, round(starts[j] if j >= 0 else 0, 3)])
        i = (j if j >= 0 else i) + len(wd)
    return out


def build():
    sc = json.load(open("script.json"))
    lines, t = [], 0.25
    for ln in sc["narration"]:
        mp3, wav = f"audio/vo/{ln['id']}.mp3", f"audio/vo/{ln['id']}.wav"
        src = mp3 if os.path.exists(mp3) else wav
        d = dur(src)
        al = f"audio/vo/{ln['id']}.align.json"
        words = words_align(ln["text"], json.load(open(al))) if (src == mp3 and os.path.exists(al)) else words_est(ln["text"], d)
        lines.append(dict(id=ln["id"], text=ln["text"], src=src, start=round(t, 3), dur=round(d, 3),
                          words=[[w, round(t + o, 3)] for w, o in words]))
        t += (max(d, ln["slot"]) if "slot" in ln else d) + ln.get("pause_after", 0.0)
    L = {l["id"]: l for l in lines}

    def ws(lid, i):
        return L[lid]["words"][i][1]

    def end(lid):
        return L[lid]["start"] + L[lid]["dur"]

    collapse = L["L07c"]["start"] + 1.0
    # make sure L08 starts after the collapse beat
    cuts = {
        "S01_wake": 0.0,
        "S02_street": ws("L01", 3) - 0.08,
        "S03_kitchen": L["L02"]["start"] - 0.2,
        "S04_bus": L["L05"]["start"] - 0.25,
        "S05_collapse": collapse,
        "S06_reaction": ws("L09", 3) - 0.1,
        "S07_mirror": L["L10"]["start"] - 0.3,
        "S08_class": L["L14"]["start"] - 0.25,
        "S09_compare": L["L16"]["start"] - 0.2,
        "S10_choice": L["L18"]["start"] - 0.3,
    }
    total = end("L20") + 2.2
    names = list(cuts)
    scenes = [dict(id=n, start=round(cuts[n], 3), end=round(cuts[names[i + 1]] if i + 1 < len(names) else total, 3))
              for i, n in enumerate(names)]
    ev = dict(
        eyes_open=0.18,
        street_timers=ws("L01", 6) - 0.25,
        mom_timer=ws("L02", 2),
        dog_timer=ws("L03", 2),
        stranger_timer=ws("L05", 6),
        fast_from=L["L06"]["start"],
        three=L["L07a"]["start"], two=L["L07b"]["start"], one=L["L07c"]["start"],
        collapse=collapse,
        reaction=cuts["S06_reaction"],
        room_timers=L["L11"]["start"] + 0.2,
        my_timer=L["L12"]["start"],
        tilt=L["L13"]["start"] + 0.2,
        smile=ws("L13", 5),
        turn=end("L14") - 0.25,
        teacher_timer=L["L15"]["start"],
        card_a=L["L18"]["start"],
        card_b=L["L19"]["start"],
        cta=L["L20"]["start"],
        endcard=end("L20") + 0.35,
        total=round(total, 3),
    )
    ev = {k: round(v, 3) for k, v in ev.items()}
    out = dict(fps=FPS, total=round(total, 3), lines=lines, scenes=scenes, events=ev)
    json.dump(out, open("timeline.json", "w"), indent=1)
    # write final timings back into script.json
    for s in sc["scenes"]:
        m = next(x for x in scenes if x["id"] == s["id"])
        s["final"] = [m["start"], m["end"]]
    for ln in sc["narration"]:
        ln["final_start"] = L[ln["id"]]["start"]
    sc["final_duration_s"] = round(total, 2)
    json.dump(sc, open("script.json", "w"), indent=2)
    return out


if __name__ == "__main__":
    o = build()
    print("total", o["total"])
    for s in o["scenes"]:
        print(s["id"], s["start"], s["end"])
    print(o["events"])
