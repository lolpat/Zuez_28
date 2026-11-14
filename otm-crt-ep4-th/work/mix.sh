#!/bin/bash
# voice only (-16 LUFS, starts at LEAD), no background music; mix_sfx.py then adds the soft kit sounds
set -e
cd "$(dirname "$0")/.."
read TOTAL LEAD END < <(python3 -c "import json;d=json.load(open('work/timing.json'));print(d['total'],d['lead'],d['end_t'])")
N=$(python3 -c "print(int(round($TOTAL*48000)))")
D=$(python3 -c "print(int($LEAD*1000))")
ffmpeg -v error -y -i work/voice.mp3 -filter_complex "\
[0:a]aresample=48000,loudnorm=I=-16:TP=-2:LRA=11,aresample=48000,adelay=${D}|${D},\
alimiter=limit=0.84:level=false,asetpts=N/SR/TB,apad=whole_len=${N},atrim=end_sample=${N},aformat=channel_layouts=stereo[o]" \
  -map "[o]" -ar 48000 -c:a pcm_s16le work/base.wav
echo "wrote work/base.wav (voice only)"
