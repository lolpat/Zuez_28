"""Bake the music into per-frame envelopes (30 fps) for the canvas: bass, mid, high (0-100) and kick frames.
# Needs work/music/51732.wav: ffmpeg -i work/music/51732.mp3 -ac 1 -ar 22050 work/music/51732.wav
Video t=0 is music time OFFSET (a beat in the build); the drop lands at music 14.155 s."""
import json, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
FPS = 30
beats = json.load(open("work/music/51732.beats.json"))["beatTimes"]
OFFSET = 7.995
i_drop = min(range(len(beats)), key=lambda i: abs(beats[i] - 14.155))
DROP = round(beats[i_drop] - OFFSET, 3)
SWITCH = round(beats[i_drop + 32] - OFFSET, 3)          # 8 bars after the drop
END_T = round(beats[i_drop + 48] - OFFSET, 3)           # 12 bars after the drop
BAR = round((beats[i_drop + 48] - beats[i_drop]) / 12, 4)
TOTAL = round(END_T + 0.3 + 4.09 + 1.3, 2)
x, sr = sf.read("work/music/51732.wav")
seg = x[int(OFFSET * sr): int((OFFSET + TOTAL + 0.5) * sr)]
def band(lo, hi):
    if lo and hi: sos = butter(4, [lo, hi], "band", fs=sr, output="sos")
    elif hi: sos = butter(4, hi, "low", fs=sr, output="sos")
    else: sos = butter(4, lo, "high", fs=sr, output="sos")
    return sosfilt(sos, seg)
def env(sig, lo_db, hi_db, rel):
    n = int(TOTAL * FPS); hop = sr / FPS; out = []; prev = 0.0
    for f in range(n):
        a = int(f * hop); w = sig[a: a + int(hop * 1.5)]
        db = 20 * np.log10(np.sqrt(np.mean(w ** 2)) + 1e-9)
        v = min(1.0, max(0.0, (db - lo_db) / (hi_db - lo_db)))
        prev = v if v > prev else prev + (v - prev) * (1 - np.exp(-1 / (FPS * rel)))
        out.append(prev)
    return out, n
bass, n = env(band(None, 150), -36, -4, 0.10)
mid, _ = env(band(300, 2000), -44, -10, 0.12)
high, _ = env(band(5000, None), -54, -18, 0.08)
# kicks: frames where the raw bass jumps by more than 5 dB over ~70 ms
lo = band(40, 110); hop = sr / FPS
raw = [20 * np.log10(np.sqrt(np.mean(lo[int(f * hop): int(f * hop + hop)] ** 2)) + 1e-9) for f in range(n)]
kicks = [f for f in range(2, n) if raw[f] - min(raw[f - 2], raw[f - 1]) > 3.5 and raw[f] > -30]
kicks = [k for i, k in enumerate(kicks) if i == 0 or k - kicks[i - 1] > 3]
q = lambda a: [int(round(v * 100)) for v in a]
json.dump(dict(fps=FPS, offset=OFFSET, drop=DROP, switch=SWITCH, end=END_T, bar=BAR, total=TOTAL,
               beats=[round(b - OFFSET, 3) for b in beats if OFFSET - 0.01 <= b <= OFFSET + TOTAL], bass=q(bass), mid=q(mid), high=q(high), kicks=kicks), open("work/env.json", "w"))
print(f"drop {DROP} switch {SWITCH} end {END_T} bar {BAR} total {TOTAL} frames {n} kicks {len(kicks)}")
print("kicks (s):", [round(k / FPS, 2) for k in kicks[:24]])
print("bass pct before:", np.percentile(bass[:int(DROP*FPS)],[10,50,90]).round(2), "after:", np.percentile(bass[int(DROP*FPS):int(END_T*FPS)],[10,50,90]).round(2))
print("mid pct after:", np.percentile(mid[int(DROP*FPS):int(END_T*FPS)],[10,50,90]).round(2), "high:", np.percentile(high[int(DROP*FPS):int(END_T*FPS)],[10,50,90]).round(2))
print("bass mean before/after drop: %.2f / %.2f" % (np.mean(bass[:int(DROP*FPS)]), np.mean(bass[int(DROP*FPS):int(END_T*FPS)])))
