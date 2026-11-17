#!/usr/bin/env bash
# Buduje film: klatki (Chromium/Playwright) + muzyka (numpy) -> mozg_w_hipnozie.mp4
set -euo pipefail
cd "$(dirname "$0")"
BUILD=${BUILD:-build}
mkdir -p "$BUILD"
node render.js "$BUILD"
python3 muzyka.py "$BUILD/muzyka.wav"
ffmpeg -y -loglevel error -f concat -safe 0 -i "$BUILD/list.txt" -i "$BUILD/muzyka.wav" \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart mozg_w_hipnozie.mp4
echo "Gotowe: hipnoza/mozg_w_hipnozie.mp4"
