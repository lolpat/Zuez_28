"""Voice only (work/base.wav from mix.sh, no music), plus soft kit sounds on the drawings (work/cues.json).
Each sound is peak-normalised to -6 dBFS, then placed at its cue gain. Writes assets/audio/mix_blackdot.wav."""
import json, os, numpy as np, soundfile as sf
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
base, sr = sf.read("work/base.wav", always_2d=True)
out = base.copy()
for c in json.load(open("work/cues.json")):
    x, s2 = sf.read(f"assets/kit/{c['snd']}.wav", always_2d=True)
    assert s2 == sr, (c, s2)
    if x.shape[1] == 1: x = np.repeat(x, 2, axis=1)
    x = x / (np.abs(x).max() + 1e-9) * 10 ** (-6 / 20) * 10 ** (c["gain"] / 20)
    a = int(c["t"] * sr); n = min(len(x), len(out) - a)
    if n > 0: out[a:a + n] += x[:n]
pk = np.abs(out).max()
if pk > 10 ** (-1.5 / 20): out *= 10 ** (-1.5 / 20) / pk
sf.write("assets/audio/mix_blackdot.wav", out, sr, subtype="PCM_16")
print("wrote assets/audio/mix_blackdot.wav", round(len(out) / sr, 3), "s, peak %.1f dBFS" % (20 * np.log10(np.abs(out).max())))
