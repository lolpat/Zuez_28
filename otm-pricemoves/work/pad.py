"""Soft ambient bed: a slow, airy minor-9 pad with a faint shimmer. Writes assets/audio/bed.wav."""
import os, sys, numpy as np, soundfile as sf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR, T = 48000, float(sys.argv[1]) if len(sys.argv) > 1 else 64
t = np.arange(int(SR * T)) / SR
rng = np.random.default_rng(7)
def voice(f, amp, det=0.4):
    ph = rng.uniform(0, 2 * np.pi, 3)
    x = sum(np.sin(2 * np.pi * (f + d) * t + p) for d, p in zip((-det, 0, det), ph)) / 3
    lfo = 0.75 + 0.25 * np.sin(2 * np.pi * rng.uniform(0.03, 0.08) * t + rng.uniform(0, 6))
    return x * amp * lfo
# two chords that trade places slowly: Am9 -> Fmaj7(9)
c1 = [110.0, 164.81, 220.0, 261.63, 329.63, 493.88]
c2 = [87.31, 130.81, 174.61, 220.0, 261.63, 392.0]
mix = np.zeros_like(t)
xf = 0.5 + 0.5 * np.sin(2 * np.pi * t / 16.0)      # 16 s cycle between the chords
for f1, f2, a in zip(c1, c2, (0.5, 0.35, 0.3, 0.22, 0.18, 0.1)):
    mix += voice(f1, a) * xf + voice(f2, a) * (1 - xf)
shimmer = voice(987.77, 0.03, 1.5) * (0.5 + 0.5 * np.sin(2 * np.pi * t / 7))
mix += shimmer
# gentle low-pass by moving average, stereo by small delay
k = 24; mix = np.convolve(mix, np.ones(k) / k, mode="same")
d = int(0.012 * SR); L = mix; R = np.concatenate([np.zeros(d), mix[:-d]])
st = np.stack([L, R], 1)
fade = np.minimum(1, t / 3)[:, None] * np.minimum(1, (T - t) / 3)[:, None]
st = st * fade; st /= np.abs(st).max() / 0.5
sf.write(f"{ROOT}/assets/audio/bed.wav", st.astype(np.float32), SR, subtype="PCM_16")
print("bed", T)
