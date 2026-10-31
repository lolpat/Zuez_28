"""A driving 120 BPM bed for the terminal film: four-on-the-floor kick, off-beat hats, a pulsing A-minor bass and a
pad, all synthesized (no music generator is available in this connector). Writes assets/audio/music.wav."""
import os, sys, numpy as np, soundfile as sf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR, T, BPM = 48000, float(sys.argv[1]), 120
beat = 60 / BPM; n = int(SR * T); out = np.zeros(n)
rng = np.random.default_rng(3)
def put(x, t, g=1.0):
    s = int(t * SR); e = min(n, s + len(x)); out[s:e] += x[: e - s] * g
tk = np.arange(int(0.35 * SR)) / SR
kick = np.sin(2 * np.pi * (45 + 90 * np.exp(-tk * 30)) * tk) * np.exp(-tk * 9)
th = np.arange(int(0.06 * SR)) / SR
hat = rng.standard_normal(len(th)) * np.exp(-th * 70); hat = np.diff(np.concatenate([[0], hat]))
bass_notes = [55.0, 55.0, 65.41, 49.0]                  # A1 A1 C2 G1, one per bar
k = 0; t = 0.0
while t < T:
    bar = int(t / (4 * beat))
    if t > 0.1: put(kick, t, 0.9)
    put(hat, t + beat / 2, 0.25)
    f = bass_notes[bar % 4]; tb = np.arange(int(beat * 0.9 * SR)) / SR
    b = np.tanh(2.2 * np.sin(2 * np.pi * f * tb)) * np.exp(-tb * 3.5) * 0.35
    put(b, t + beat / 2)
    t += beat
pad_t = np.arange(n) / SR
pad = sum(np.sin(2 * np.pi * fr * pad_t + ph) for fr, ph in ((220, 0), (261.6, 1), (329.6, 2), (392, 3))) * 0.04
pad *= 0.6 + 0.4 * np.sin(2 * np.pi * pad_t / 8)
mix = out + pad
# side-chain pump on the kick
pump = np.ones(n)
for i in range(int(T / beat)):
    s = int(i * beat * SR); L = int(0.25 * SR); e = min(n, s + L)
    pump[s:e] = np.minimum(pump[s:e], 0.55 + 0.45 * np.linspace(0, 1, e - s))
mix *= pump
fade = np.minimum(1, pad_t / 1.0) * np.minimum(1, (T - pad_t) / 2.5)
mix *= fade; mix /= np.abs(mix).max() / 0.7
st = np.stack([mix, np.concatenate([np.zeros(240), mix[:-240]])], 1)
sf.write(f"{ROOT}/assets/audio/music.wav", st.astype(np.float32), SR, subtype="PCM_16"); print("music", T)
