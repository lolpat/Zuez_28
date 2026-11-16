"""Fallback aligner for takes whisper can't transcribe (some Thai reads): spreads the script's space-separated phrases
over the voice's speech time in proportion to their length, then snaps each phrase start to the nearest pause end
(silencedetect). Writes work/words.json and work/marks.json in the same format as work/align.py."""
import json, re, subprocess, sys

root = sys.argv[1] if len(sys.argv) > 1 else "."
txt = open(f"{root}/work/script.txt").read()
toks, marks, pend = [], {}, []
for part in re.findall(r"\[[a-z0-9]+\]|[^\s\[\]]+", txt):
    if part.startswith("["):
        pend.append(part[1:-1])
    else:
        for k in pend: marks[k] = len(toks)
        pend = []; toks.append(part)
o = subprocess.run(["ffmpeg", "-nostats", "-i", f"{root}/work/voice.mp3", "-af", "silencedetect=n=-38dB:d=0.09", "-f", "null", "-"],
                   capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", o)]
en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", o)]
dur = float(re.search(r"Duration: (\d+):(\d+):([\d.]+)", o).group(3)) + 60 * int(re.search(r"Duration: (\d+):(\d+)", o).group(2))
# speech segments between silences
segs, t = [], 0.0
if st and st[0] < 0.05: t = en[0]; st, en = st[1:], en[1:]
for a, b in zip(st, en + [dur]):
    if a > t: segs.append((t, a))
    t = b
if t < dur - 0.05: segs.append((t, dur))
speech = sum(b - a for a, b in segs)
def at(x):                                     # speech-time -> real time
    for a, b in segs:
        if x <= b - a: return a + x
        x -= b - a
    return segs[-1][1]
w = [len(re.sub(r"[ัิ-ฺ็-๎]", "", t_)) + 2 for t_ in toks]   # rough spoken length per phrase
tot = sum(w); starts = []; acc = 0
for x in w:
    starts.append(at(speech * acc / tot)); acc += x
seg_starts = [a for a, b in segs]
# monotonic DP: every phrase starts at a speech-segment start (two phrases may share one, at a cost); the cost is the
# distance from the proportional estimate, so long pauses at line breaks pull the line-start phrases onto them
n, m, INF = len(starts), len(seg_starts), 1e9
D = [[INF] * m for _ in range(n)]; P = [[-1] * m for _ in range(n)]
for j in range(m): D[0][j] = abs(starts[0] - seg_starts[j]) + 0.3 * j
for i in range(1, n):
    best, bj = INF, -1
    for j in range(m):
        # strictly later segment: best over k < j
        if j > 0 and D[i - 1][j - 1] < best: best, bj = D[i - 1][j - 1], j - 1
        c_new = best if bj >= 0 else INF
        c_share = D[i - 1][j] + 1.2
        if c_new <= c_share: D[i][j], P[i][j] = c_new + abs(starts[i] - seg_starts[j]), bj
        else: D[i][j], P[i][j] = c_share + abs(starts[i] - seg_starts[j]), j
j = min(range(m), key=lambda j: D[n - 1][j]); assign = [0] * n
for i in range(n - 1, -1, -1):
    assign[i] = j; j = P[i][j] if i else j
snapped = []
for i in range(n):
    s_ = seg_starts[assign[i]]
    if i and assign[i] == assign[i - 1]:              # shared segment: put it part-way in
        a_, b_ = segs[assign[i]]; s_ = round(min(b_ - 0.2, max(snapped[-1] + 0.3, starts[i])), 3)
    snapped.append(round(s_, 3))
words = [{"text": t_, "start": s, "end": round((snapped[i + 1] if i + 1 < len(snapped) else segs[-1][1]) - 0.05, 3)} for i, (t_, s) in enumerate(zip(toks, snapped))]
json.dump(words, open(f"{root}/work/words.json", "w"), ensure_ascii=False, indent=0)
json.dump(marks, open(f"{root}/work/marks.json", "w"), indent=0)
print(f"{len(toks)} phrases, {len(segs)} speech segments, {len(marks)} marks")
for k, i in marks.items(): print(f"  [{k}] {words[i]['start']:6.2f}  {words[i]['text']}")
