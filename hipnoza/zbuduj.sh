#!/usr/bin/env bash
# Buduje oba filmy: lektor (Piper) -> timeline -> klatki (Chromium) -> muzyka + miks -> MP4
# Wymaga: pip install piper-tts numpy; modele głosu Piper (pl_PL-mc_speech-medium) w katalogu $GLOSY
set -euo pipefail
cd "$(dirname "$0")"
BUILD=${BUILD:-build}; GLOSY=${GLOSY:-glosy}
mkdir -p "$BUILD"
python3 lektor.py "$GLOSY" "$BUILD/lektor.wav" timeline.js
ffmpeg -y -loglevel error -i "$BUILD/lektor.wav" -af "highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,aresample=44100:resampler=soxr" "$BUILD/lektor44.wav"
python3 muzyka.py timeline.js "$BUILD/lektor44.wav" "$BUILD/miks.wav"
ffmpeg -y -loglevel error -i "$BUILD/miks.wav" -af loudnorm=I=-14:TP=-1.5:LRA=11 -ar 44100 "$BUILD/miks_norm.wav"
for l in v h; do
  node render.js "$BUILD" $l
  n=$([ $l = v ] && echo pion_9x16 || echo poziom_16x9)
  ffmpeg -y -loglevel error -f concat -safe 0 -i "$BUILD/${l}_list.txt" -i "$BUILD/miks_norm.wav" \
    -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "mozg_w_hipnozie_$n.mp4"
done
echo "Gotowe."
