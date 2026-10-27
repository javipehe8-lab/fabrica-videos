#!/usr/bin/env bash
# Genera un episodio completo. Uso: bash hacer_episodio.sh N
# Necesita stick/guionN.py y stick/escenasN.py (+ efectos de sonido en sonido.py si hay escenas nuevas).
set -e
N="$1"; ROOT="$(cd "$(dirname "$0")" && pwd)"; cd "$ROOT/stick"
export EP="$N"
python3.13 voz.py "voz$N"
python3.13 render.py "voz$N" "out$N" --preview   # hoja de previsualización: out$N/preview.png (REVISAR antes de seguir)
python3.13 render.py "voz$N" "out$N"
python3.13 sonido.py "voz$N" "out$N"
mkdir -p "$ROOT/videos"
ffmpeg -y -v error -i "out$N/video_mudo.mp4" -i "out$N/audio.wav" -map 0:v -map 1:a \
  -c:v libx264 -preset veryfast -crf 23 -maxrate 6M -bufsize 12M -pix_fmt yuv420p \
  -af "loudnorm=I=-14:TP=-1.2:LRA=9" -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart \
  "$ROOT/videos/El_Sonriente_Parte$N.mp4"
ls -la "$ROOT/videos/El_Sonriente_Parte$N.mp4"
