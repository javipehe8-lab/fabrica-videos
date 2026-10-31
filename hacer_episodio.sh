#!/usr/bin/env bash
# Genera un episodio completo. Uso: bash hacer_episodio.sh N [en]
# Español: stick/guionN.py -> videos/El_Sonriente_ParteN.mp4
# 3AM:     bash hacer_episodio.sh 3am1 -> videos/3am/Si_Oyes_Esto_1.mp4
# Inglés:  stick/guionN_en.py (mismas escenas, texto traducido) -> videos/en/The_Grinner_PartN.mp4
set -e
N="$1"; L="${2:-es}"; ROOT="$(cd "$(dirname "$0")" && pwd)"; cd "$ROOT/stick"
export EP="$N"
if [ "$L" = "en" ]; then
  export IDIOMA=en; SUF="_en"; OUTDIR="$ROOT/videos/en"; OUT="$OUTDIR/The_Grinner_Part$N.mp4"
else
  unset IDIOMA; SUF=""; OUTDIR="$ROOT/videos"; OUT="$OUTDIR/El_Sonriente_Parte$N.mp4"
fi
# Serie "Si oyes esto a las 3AM": N = 3amK (guion3amK.py / escenas3amK.py) -> videos/3am/Si_Oyes_Esto_K.mp4
case "$N" in 3am*) K="${N#3am}"
  if [ "$L" = "en" ]; then OUTDIR="$ROOT/videos/3am/en"; OUT="$OUTDIR/If_You_Hear_This_$K.mp4"
  else OUTDIR="$ROOT/videos/3am"; OUT="$OUTDIR/Si_Oyes_Esto_$K.mp4"; fi;; esac
python3.13 voz.py "voz$N$SUF"
python3.13 render.py "voz$N$SUF" "out$N$SUF" --preview   # out$N$SUF/preview.png: REVISAR antes de publicar
python3.13 render.py "voz$N$SUF" "out$N$SUF"
python3.13 sonido.py "voz$N$SUF" "out$N$SUF"
mkdir -p "$OUTDIR"
ffmpeg -y -v error -i "out$N$SUF/video_mudo.mp4" -i "out$N$SUF/audio.wav" -map 0:v -map 1:a \
  -c:v libx264 -preset veryfast -crf 23 -maxrate 6M -bufsize 12M -pix_fmt yuv420p \
  -af "loudnorm=I=-14:TP=-1.2:LRA=9" -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart "$OUT"
ls -la "$OUT"
