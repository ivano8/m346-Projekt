# The Timer — Part 1 (Instagram Reel)

**Final video:** `reel_part1.mp4`. 1080x1920, 30 fps, 55.97 s, H.264 + AAC, about -14.7 LUFS.
**Cover frame:** `cover.jpg`

| Path | What |
|---|---|
| `script.json` | Script, narration lines, scene list with planned and final timings, ElevenLabs prompts |
| `timeline.json` | Final line, word, scene and event timings (generated from the real VO lengths) |
| `assets/svg/` | Every scene layer as hand-drawn-style SVG (parallax layers, plus pose variants) |
| `assets/layers/` | Rasterised layers, 3 "line-boil" variants each |
| `assets/fonts/` | Anton (captions) and Share Tech Mono (timers), both OFL |
| `audio/vo/`, `audio/sfx/`, `audio/music/` | Narration, sound effects and music stems |
| `tools/` | `art.py` (SVG drawing), `build_layers.py`, `timeline.py`, `render.py` (animation), `audio.py` (sound design + mix), `elevenlabs_generate.py`, `vo_placeholder.py` |
| `build.sh` | Rebuilds the whole pipeline in one command |

## Audio status
ELEVENLABS_API_KEY was **not set**, and api.elevenlabs.io was blocked by the sandbox network, so this render uses placeholders:
- Voice: local Kokoro TTS (voice `am_michael`, speed 0.9, light reverb). Word timings are estimated.
- SFX (hit, glitch, tick, heartbeat, thud, whoosh, riser, chalk, drone, bus) and music: synthesised in code.

To switch to ElevenLabs: `export ELEVENLABS_API_KEY=...` (optionally `ELEVENLABS_VOICE_ID=...`), then run `./build.sh`.
This generates the voice with character timestamps (so the captions sync exactly), the SFX and the music, then re-times and re-renders everything.
