"""Mixes work/cues.json with the earshot kit: each cue's role picks the next take of that role (assets/kit,
kit.lock.json), earshot's kit.place puts the take's sync point (onset / whoosh peak) on the cue frame, and the take
plays at the role's level_db plus the cue's gain. Voice, bed and the effects bus are then balanced like the earlier
films: voice at the target, effects 9 dB under, ducked 5 dB while he speaks, the bed 15 dB under.
usage: python mix_kit.py TARGET_LUFS work/cues.json assets/audio/mix.wav
"""
import json, os, sys
import numpy as np, soundfile as sf, pyloudnorm as pyln
from earshot.forge import kit
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
target, CUES, OUT = float(sys.argv[1]), sys.argv[2], sys.argv[3]
cues = json.load(open(CUES)); lock = json.load(open(f"{ROOT}/assets/kit/kit.lock.json"))
total = cues["total"]; n = int(total * SR) + SR
fx, vo, bed = np.zeros((n, 2)), np.zeros((n, 2)), np.zeros((n, 2))
def load(path):
    x, sr = sf.read(path, always_2d=True)
    if sr != SR:
        import soxr; x = soxr.resample(x, sr, SR)
    return np.repeat(x, 2, axis=1) if x.shape[1] == 1 else x
def add(bus, x, t):
    st = int(round(t * SR))
    if st < 0: x = x[-st:]; st = 0
    seg = x[: len(bus) - st]; bus[st:st + len(seg)] += seg
used, log = {}, []
for c in cues["cues"]:
    if c["snd"] in ("vo", "bed"):
        add(vo if c["snd"] == "vo" else bed, load(f"{ROOT}/assets/audio/{c['file']}.wav"), c["t"]); continue
    role = lock["roles"][c["snd"]]
    k = used.get(c["snd"], 0); used[c["snd"]] = k + 1
    take = role["takes"][k % len(role["takes"])]
    start = kit.place(take, role, c["t"])
    g = role.get("level_db", 0) + c.get("gain", 0)
    add(fx, load(f"{ROOT}/assets/kit/{take['file']}") * 10 ** (g / 20), start)
    log.append(f'{c["t"]:6.2f} {c["snd"]:13s} {take["file"]:22s} start {start:6.2f} gain {g:+.1f} dB')
L = int(total * SR); fx, vo, bed = fx[:L], vo[:L], bed[:L]
m = pyln.Meter(SR)
vo *= 10 ** ((target - m.integrated_loudness(vo)) / 20)
fx *= 10 ** ((target - 9 - m.integrated_loudness(fx)) / 20)
bed *= 10 ** ((target - 15 - m.integrated_loudness(bed)) / 20)
env = np.convolve(np.abs(vo).max(axis=1), np.ones(int(0.25 * SR)) / int(0.25 * SR), mode="same")
duck = np.where(env > 10 ** (-40 / 20), 10 ** (-5 / 20), 1.0)
duck = np.convolve(duck, np.ones(int(0.08 * SR)) / int(0.08 * SR), mode="same")[:, None]
out = fx * duck + bed * (duck * 0.6 + 0.4) + vo
out *= 10 ** ((target - m.integrated_loudness(out)) / 20)
ceil = 10 ** (-1.5 / 20); pk = np.abs(out).max()
if pk > ceil: out = np.tanh(out / ceil) * ceil if pk > ceil * 1.6 else out * ceil / pk
out[-int(0.03 * SR):] *= np.linspace(1, 0, int(0.03 * SR))[:, None]
sf.write(OUT, out.astype(np.float32), SR, subtype="PCM_16")
open(f"{ROOT}/work/mix_log.txt", "w").write("\n".join(log))
print(f"wrote {OUT} {total}s, {len(log)} kit cues; {m.integrated_loudness(out):.1f} LUFS, peak {20*np.log10(np.abs(out).max()):.1f} dBFS")
