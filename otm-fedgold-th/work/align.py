"""Align the script's tokens (work/script.txt, split on spaces) to work/voice.mp3 with faster-whisper (small, Thai,
word timestamps) and a character-level difflib match. Writes work/words.json ([{text, start, end}] per token)."""
import difflib, json, os, subprocess, numpy as np
from faster_whisper import WhisperModel
os.chdir(os.path.dirname(os.path.abspath(__file__)))
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", "voice.mp3", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
audio = np.frombuffer(pcm, np.float32)
segs, _ = WhisperModel("small", compute_type="int8").transcribe(audio, language="th", word_timestamps=True)
hc, ht = [], []                                        # heard chars and their times
for s in segs:
    for w in s.words:
        t = w.word.strip().lower()
        for k, ch in enumerate(t):
            hc.append(ch); ht.append(w.start + (w.end - w.start) * (k + 0.5) / max(1, len(t)))
heard = "".join(hc); print("heard:", heard)
toks = open("script.txt").read().split()
sc, owner = [], []
for i, t in enumerate(toks):
    for ch in t.lower(): sc.append(ch); owner.append(i)
script = "".join(sc)
sm = difflib.SequenceMatcher(None, script, heard, autojunk=False)
tmap = {}
for a, b, n in sm.get_matching_blocks():
    for k in range(n): tmap[a + k] = ht[b + k]
print("matched %.0f%% of script chars" % (100 * len(tmap) / len(script)))
out = []
for i, t in enumerate(toks):
    idx = [k for k, o in enumerate(owner) if o == i and k in tmap]
    out.append(dict(text=t, start=round(tmap[idx[0]], 2) if idx else None, end=round(tmap[idx[-1]], 2) if idx else None))
for i, w in enumerate(out):                            # fill gaps from neighbours
    if w["start"] is None:
        p = next((out[j]["end"] for j in range(i - 1, -1, -1) if out[j]["end"] is not None), 0)
        w["start"] = w["end"] = p
for i in range(len(out) - 1):                          # monotone
    out[i + 1]["start"] = max(out[i + 1]["start"], out[i]["start"])
json.dump(out, open("words.json", "w"), ensure_ascii=False, indent=0)
for i, w in enumerate(out): print(i, w["start"], w["end"], w["text"])
