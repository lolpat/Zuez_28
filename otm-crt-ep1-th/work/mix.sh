#!/bin/bash
# voice only (-16 LUFS, starts at LEAD), no background music; mix_sfx.py then adds the soft kit sounds.
# Chain: light de-esser, gentle compressor, one static gain, look-ahead limiter.
# No dynamic loudnorm (it rode the voice level up and down with sudden jumps). Instead: a gentle compressor, then ONE
# static gain measured on the whole take (to -16 LUFS), then a look-ahead limiter at -1 dBFS that only touches the
# rare peaks (well under 0.1% of samples), so nothing pumps or crackles.
set -e
cd "$(dirname "$0")/.."
read TOTAL LEAD END VE < <(python3 -c "import json;d=json.load(open('work/timing.json'));print(d['total'],d['lead'],d['end_t'],d.get('voice_end',d['total']))")
N=$(python3 -c "print(int(round($TOTAL*48000)))")
D=$(python3 -c "print(int($LEAD*1000))")
FO=$(python3 -c "print(round($VE-0.12,3))")                         # parts 1-4 stop the voice in the pause before the outro line
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
ffmpeg -v error -y -i work/voice.mp3 -af "aresample=48000,deesser=i=0.35:m=0.5:f=0.5,acompressor=threshold=-20dB:ratio=2:attack=10:release=250:knee=6" \
  -ar 48000 -c:a pcm_f32le "$T/c.wav"
I=$(ffmpeg -nostats -i "$T/c.wav" -af ebur128 -f null - 2>&1 | grep -A1 "Integrated loudness" | awk '/I:/{print $2}')
G=$(python3 -c "print(round(-16-($I),2))")
ffmpeg -v error -y -i "$T/c.wav" -filter_complex "\
[0:a]volume=${G}dB,alimiter=limit=0.891:attack=5:release=100:asc=1:level=false,adelay=${D}|${D},\
asetpts=N/SR/TB,atrim=end=${VE},afade=t=out:st=${FO}:d=0.12,apad=whole_len=${N},atrim=end_sample=${N},aformat=channel_layouts=stereo[o]" \
  -map "[o]" -ar 48000 -c:a pcm_s16le work/base.wav
echo "wrote work/base.wav (voice only; static gain ${G} dB)"
