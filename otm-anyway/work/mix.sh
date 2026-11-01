#!/bin/bash
# voice (-16 LUFS, starts at LEAD) + "Piece of Quiet" bed (about -31 LUFS, swells under the end card, fades out)
set -e
cd "$(dirname "$0")/.."
read TOTAL LEAD END < <(python3 -c "import json;d=json.load(open('work/timing.json'));print(d['total'],d['lead'],d['end_t'])")
N=$(python3 -c "print(int(round($TOTAL*48000)))")
D=$(python3 -c "print(int($LEAD*1000))")
ffmpeg -v error -y -i work/take2.mp3 -i work/music/31391.mp3 -filter_complex "\
[0:a]aresample=48000,loudnorm=I=-16:TP=-2:LRA=11,aresample=48000,adelay=${D}|${D},apad,atrim=0:${TOTAL}[v];\
[1:a]aresample=48000,atrim=0:${TOTAL},asetpts=N/SR/TB,loudnorm=I=-30:TP=-8:LRA=15,aresample=48000,\
volume='1+0.9*min(1\,max(0\,(t-${END})/0.8))':eval=frame,afade=t=in:d=1.5,afade=t=out:st=$(python3 -c "print($TOTAL-1.8)"):d=1.8[m];\
[v][m]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.84:level=false,asetpts=N/SR/TB,apad=whole_len=${N},atrim=end_sample=${N},aformat=channel_layouts=stereo[o]" \
  -map "[o]" -ar 48000 -c:a pcm_s16le work/base.wav
echo "wrote work/base.wav"
