"""Mixes work/cues.json into assets/audio/sfx.wav using the sounds in assets/sfx (map: work/sfxmap.json)."""
import json, os, sys
import numpy as np, soundfile as sf, pyloudnorm as pyln
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
CUES = sys.argv[2] if len(sys.argv) > 2 else f"{ROOT}/work/cues.json"
OUT = sys.argv[3] if len(sys.argv) > 3 else f"{ROOT}/assets/audio/mix.wav"
cues = json.load(open(CUES)); m = json.load(open(f"{ROOT}/work/sfxmap.json"))
total = cues["total"]; out = np.zeros((int(total * SR) + SR, 2)); vo = np.zeros_like(out)
use = {k: 0 for k in m}; cache = {}
def load(name):
    if name not in cache:
        x, sr = sf.read(f"{ROOT}/assets/sfx/{name}.wav", always_2d=True)
        if sr != SR:
            import soxr; x = soxr.resample(x, sr, SR)
        if x.shape[1] == 1: x = np.repeat(x, 2, axis=1)
        x = x / (np.abs(x).max() + 1e-9) * 10 ** (-1 / 20)
        env = np.abs(x).max(axis=1)
        onset = int(np.argmax(env > env.max() * 0.08)); peak = int(np.argmax(env))
        cache[name] = (x, onset, peak)
    return cache[name]
log = []
for c in cues["cues"]:
    if c["snd"] == "vo":                 # the voice: placed as is, on its own bus
        x, sr = sf.read(f"{ROOT}/assets/audio/{c['file']}.wav", always_2d=True)
        if x.shape[1] == 1: x = np.repeat(x, 2, axis=1)
        st = int(round(c["t"] * SR)); seg = x[: len(vo) - st]; vo[st:st + len(seg)] += seg
        log.append(f'{c["t"]:6.2f} vo      {c["file"]}'); continue
    opts = m[c["snd"]]; pick = opts[use[c["snd"]] % len(opts)]; use[c["snd"]] += 1
    x, onset, peak = load(pick.replace("/", "_").replace(":", "_"))
    align = c.get("align", "onset")
    ref = {"onset": onset, "peak": peak, "end": len(x)}[align]
    start = int(round(c["t"] * SR)) - ref + (int(SR / 30) if align == "peak" else 0)   # sound one frame after picture
    if start < 0: x = x[-start:]; start = 0
    seg = x[: len(out) - start] * 10 ** (c["gain"] / 20)
    out[start:start + len(seg)] += seg
    log.append(f'{c["t"]:6.2f} {c["snd"]:7s} {pick}')
out = out[: int(total * SR)]; vo = vo[: int(total * SR)]
meter = pyln.Meter(SR)
target = float(sys.argv[1]) if len(sys.argv) > 1 else -16.0
lufs = meter.integrated_loudness(out)
if np.abs(vo).max() > 0:
    # effects sit under the voice: the voice bus at the target, the effects 9 dB under it, ducked 5 dB while he speaks
    vl = meter.integrated_loudness(vo); vo *= 10 ** ((target - vl) / 20)
    out *= 10 ** ((target - 9 - lufs) / 20)
    env = np.convolve(np.abs(vo).max(axis=1), np.ones(int(0.25 * SR)) / int(0.25 * SR), mode="same")
    duck = np.where(env > 10 ** (-40 / 20), 10 ** (-5 / 20), 1.0)
    duck = np.convolve(duck, np.ones(int(0.08 * SR)) / int(0.08 * SR), mode="same")
    out = out * duck[:, None] + vo
    l2 = meter.integrated_loudness(out); out *= 10 ** ((target - l2) / 20)
else:
    out *= 10 ** ((target - lufs) / 20)
pk = np.abs(out).max(); ceil = 10 ** (-1.5 / 20)
if pk > ceil:                      # soft limiter on the loudest moments only
    out = np.tanh(out / ceil * 1.0) * ceil if pk > ceil * 1.6 else out * (ceil / pk)
# 30 ms fade at the very end
n = int(0.03 * SR); out[-n:] *= np.linspace(1, 0, n)[:, None]
os.makedirs(f"{ROOT}/assets/audio", exist_ok=True)
sf.write(OUT, out.astype(np.float32), SR, subtype="PCM_16")
print(f"wrote mix.wav {total}s, {len(cues['cues'])} cues; loudness {meter.integrated_loudness(out):.1f} LUFS (was {lufs:.1f} before gain), peak {20*np.log10(np.abs(out).max()):.1f} dBFS")
open(f"{ROOT}/work/mix_log.txt", "w").write("\n".join(log))
