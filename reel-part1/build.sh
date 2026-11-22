#!/usr/bin/env bash
# Full pipeline: (ElevenLabs if key) -> timeline -> SVG layers -> frames -> mix -> final MP4
set -euo pipefail
cd "$(dirname "$0")"
if [ -n "${ELEVENLABS_API_KEY:-}" ]; then python3 tools/elevenlabs_generate.py; fi
[ -f audio/vo/L01.wav ] || [ -f audio/vo/L01.mp3 ] || python3 tools/vo_placeholder.py
python3 tools/timeline.py
python3 tools/build_layers.py
python3 tools/render.py
python3 tools/audio.py
ffmpeg -y -loglevel error -i build/video_silent.mp4 -i build/mix.wav -map 0:v -map 1:a \
  -c:v libx264 -preset slow -crf 22 -maxrate 12M -bufsize 24M -pix_fmt yuv420p -profile:v high -r 30 \
  -af "volume=7dB,alimiter=limit=0.84:level=false" -c:a aac -b:a 256k -ar 48000 -shortest -movflags +faststart reel_part1.mp4
echo "-> $(pwd)/reel_part1.mp4"
