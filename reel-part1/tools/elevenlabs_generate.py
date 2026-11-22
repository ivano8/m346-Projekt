"""Generate real ElevenLabs assets (voice with timestamps, SFX, music).
Requires ELEVENLABS_API_KEY. Files written here replace the placeholders automatically on the next ./build.sh:
  audio/vo/<ID>.mp3 + <ID>.align.json, audio/sfx/el_<name>.mp3, audio/music/el_music.mp3
"""
import base64, json, os, sys, urllib.request

KEY = os.environ.get("ELEVENLABS_API_KEY")
if not KEY:
    sys.exit("ELEVENLABS_API_KEY not set - keeping placeholder audio.")
VOICE = os.environ.get("ELEVENLABS_VOICE_ID", "pNInz6obpgDQGcFmaJgB")  # premade 'Adam'; any calm low narrator works
API = "https://api.elevenlabs.io/v1"
sc = json.load(open("script.json"))
cfg = sc["elevenlabs"]


def post(path, body, accept="application/json"):
    req = urllib.request.Request(API + path, data=json.dumps(body).encode(), method="POST",
                                 headers={"xi-api-key": KEY, "Content-Type": "application/json", "Accept": accept})
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read()


prev = None
for ln in sc["narration"]:
    body = {"text": ln["text"], "model_id": cfg["voice"]["model_id"],
            "voice_settings": {k: cfg["voice"][k] for k in ("stability", "similarity_boost", "style")}}
    if prev:
        body["previous_text"] = prev
    r = json.loads(post(f"/text-to-speech/{VOICE}/with-timestamps", body))
    open(f"audio/vo/{ln['id']}.mp3", "wb").write(base64.b64decode(r["audio_base64"]))
    json.dump(r["alignment"], open(f"audio/vo/{ln['id']}.align.json", "w"))
    prev = ln["text"]
    print("vo", ln["id"])

durations = {"drone": 22, "bus": 12}
for name, prompt in cfg["sfx_prompts"].items():
    body = {"text": prompt, "prompt_influence": 0.6}
    if name in durations:
        body["duration_seconds"] = durations[name]
    open(f"audio/sfx/el_{name}.mp3", "wb").write(post("/sound-generation", body, "audio/mpeg"))
    print("sfx", name)

total_ms = int((sc.get("final_duration_s", 56) + 2) * 1000)
try:
    data = post("/music", {"prompt": cfg["music_prompt"], "music_length_ms": total_ms}, "audio/mpeg")
except Exception as e:  # music API not on every plan -> fall back to a long ambient sound generation
    print("music endpoint failed:", e)
    data = post("/sound-generation", {"text": cfg["music_prompt"], "duration_seconds": 22}, "audio/mpeg")
open("audio/music/el_music.mp3", "wb").write(data)
print("music done")
