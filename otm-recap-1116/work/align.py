"""Aligns work/script.txt (with [key] marks) to work/voice.mp3.
Writes work/words.json (one entry per script token, with start/end seconds) and work/marks.json (key -> token index).
The voice is transcribed with faster-whisper (small.en for English, small for Thai) with word timings; each transcript
character gets a time (spread over its word), and the script's characters are matched to the transcript's with difflib,
so each script token takes the time of its matched characters. Usage: python3 work/align.py en|th"""
import difflib, json, os, re, subprocess, sys, tempfile
import soundfile as sf
from faster_whisper import WhisperModel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lang = sys.argv[1]

text = open(f"{ROOT}/work/script.txt").read()
tokens, marks = [], {}
for part in text.split():
    m = re.fullmatch(r"\[([a-z0-9]+)\]", part)
    if m: marks[m.group(1)] = len(tokens)
    else: tokens.append(part)

def norm(s): return [ch for ch in s.lower() if ch.isalnum()]

with tempfile.TemporaryDirectory() as d:
    wav = f"{d}/v.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{ROOT}/work/voice.mp3", "-ac", "1", "-ar", "16000", wav], check=True)
    aud, _ = sf.read(wav, dtype="float32")
model = WhisperModel("small.en" if lang == "en" else "small", device="cpu", compute_type="int8")

# script characters with their token index
sc, si = [], []
for i, tok in enumerate(tokens):
    for c in norm(tok):
        sc.append(c); si.append(i)

# whisper sometimes drops a stretch of speech; try three decoding setups and keep the one that matches the script best
CONFIGS = [dict(), dict(condition_on_previous_text=False),
           dict(condition_on_previous_text=False, vad_filter=True, vad_parameters=dict(min_silence_duration_ms=300))]
best = None
for cfg in CONFIGS:
    segs, _ = model.transcribe(aud, word_timestamps=True, language=lang, **cfg)
    words_ = [(w.word, w.start, w.end) for s in segs for w in s.words]
    tc_, tt_ = [], []                                  # transcript characters with times
    for word, a, b in words_:
        ch = norm(word)
        for k, c in enumerate(ch):
            tc_.append(c); tt_.append(a + (b - a) * (k + 0.5) / max(1, len(ch)))
    sm_ = difflib.SequenceMatcher(None, sc, tc_, autojunk=False)
    r = sum(n for _, _, n in sm_.get_matching_blocks()) / max(1, len(sc))
    # a usable setup also places every mark at its own time, in order (a dropped stretch piles marks on one time)
    first = {}
    for a, b, n in sm_.get_matching_blocks():
        for k in range(n): first.setdefault(si[a + k], tt_[b + k])
    mt = [first.get(i) for i in marks.values()]
    ok = all(x is not None for x in mt) and all(y - x > 0.25 for x, y in zip(mt, mt[1:]))
    print(f"  setup {CONFIGS.index(cfg)}: matched {r:.0%}, marks {'ok' if ok else 'broken'}")
    key = (ok, r)
    if best is None or key > best[0]:
        best = (key, words_, tt_, sm_)
_, tw, tt, sm = best
ctime = [None] * len(sc)
for a, b, n in sm.get_matching_blocks():
    for k in range(n): ctime[a + k] = tt[b + k]
# fill unmatched characters by linear interpolation
known = [k for k, v in enumerate(ctime) if v is not None]
for k in range(len(ctime)):
    if ctime[k] is None:
        lo = max([j for j in known if j < k], default=None); hi = min([j for j in known if j > k], default=None)
        if lo is None: ctime[k] = ctime[hi]
        elif hi is None: ctime[k] = ctime[lo]
        else: ctime[k] = ctime[lo] + (ctime[hi] - ctime[lo]) * (k - lo) / (hi - lo)

words = []
for i, tok in enumerate(tokens):
    ts = [ctime[k] for k in range(len(sc)) if si[k] == i]
    if not ts: ts = [words[-1]["end"]] if words else [0.0]
    words.append(dict(text=tok, start=round(max(0, min(ts) - 0.06), 2), end=round(max(ts) + 0.06, 2)))
for a, b in zip(words, words[1:]):                  # keep starts in order
    if b["start"] < a["start"]: b["start"] = a["start"]
json.dump(words, open(f"{ROOT}/work/words.json", "w"), ensure_ascii=False)
json.dump(marks, open(f"{ROOT}/work/marks.json", "w"))
ratio = sum(n for _, _, n in sm.get_matching_blocks()) / max(1, len(sc))
print(f"{len(tokens)} tokens, {len(marks)} marks, matched {ratio:.0%} of script characters; whisper heard:")
print(" ".join(w for w, _, _ in tw)[:600])
for k, i in marks.items():
    print(f"  [{k}] {words[i]['start']:6.2f}  {tokens[i]}")
