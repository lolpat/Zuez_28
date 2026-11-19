#!/bin/bash
# Joins three finished OTM videos into one Instagram Reel: otm-thousand -> otm-hopping -> otm-nothing.
# The first two are cut where their "Order the market..." outro line begins (so the outro appears once, at the end),
# each with a 0.4 s dip to black; the last one plays in full, outro and all. Output is the Reels layout
# (918 x 1632 picture on a 1080 x 1920 black canvas), like the single videos.
# usage: bash combine.sh en|th ROOT OUT.mp4   (ROOT holds <project>/renders/<project>.mp4 from `npx hyperframes render`)
set -e
L=${1:?en or th}; ROOT=${2:?root}; OUT=${3:?out.mp4}
if [ "$L" = th ]; then SUF=-th; C1=34.46; C2=34.83; else SUF=; C1=32.55; C2=33.84; fi
# C1/C2: onset of "Order" in the first two voices (seconds), measured on work/base.wav
A=$ROOT/otm-thousand$SUF/renders/otm-thousand$SUF.mp4
B=$ROOT/otm-hopping$SUF/renders/otm-hopping$SUF.mp4
C=$ROOT/otm-nothing$SUF/renders/otm-nothing$SUF.mp4
T=0.25   # picture kept after the cut (the fade to black finishes here)
seg() {  # $1 input label, $2 cut, $3 fade-in?
  local e; e=$(python3 -c "print(round($2 + $T, 3))")
  local fin=""; [ "$3" = 1 ] && fin="fade=t=in:st=0:d=0.3,"
  printf '[%s:v]trim=0:%s,setpts=PTS-STARTPTS,%sfade=t=out:st=%s:d=0.4[v%s];' "$1" "$e" "$fin" "$(python3 -c "print(round($2 - 0.15, 3))")" "$1"
  printf '[%s:a]atrim=0:%s,asetpts=PTS-STARTPTS,afade=t=out:st=%s:d=0.06,apad=whole_dur=%s[a%s];' "$1" "$2" "$(python3 -c "print(round($2 - 0.06, 3))")" "$e" "$1"
}
FC="$(seg 0 $C1 0)$(seg 1 $C2 1)[2:v]fade=t=in:st=0:d=0.3[v2];[2:a]anull[a2];"
FC="$FC[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[cv][ca];"
FC="${FC}color=black:s=1080x1920:r=30[bg];[cv]scale=918:1632:flags=lanczos,fps=30[s];[bg][s]overlay=x=40:y=140:shortest=1,format=yuv420p[ov]"
ffmpeg -v error -y -i "$A" -i "$B" -i "$C" -filter_complex "$FC" -map "[ov]" -map "[ca]" \
  -c:v libx264 -crf 17 -preset slow -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$OUT"
echo "wrote $OUT"
