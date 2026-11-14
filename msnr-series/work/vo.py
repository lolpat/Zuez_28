"""Downloads each episode's first voice take, trims it, speeds it to 1.1x and finds the start and end of each beat.

Beats are the script.json entries. Their boundaries are the pauses closest to where the characters say they should be.
Writes assets/audio/vo_epN.wav and work/vo/epN.json ({starts, ends, dur} in seconds).
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPO = 1.1
script = json.load(open(f"{ROOT}/work/script.json"))
media = json.load(open(f"{ROOT}/work/vo/media.json"))

def run(*a):
    return subprocess.run(a, capture_output=True, text=True, check=True)

def duration(f):
    return float(run("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f).stdout)

for ep, beats in script.items():
    full = " ".join(beats)
    take = next(m for m in media if m["prompt"].strip() == full.strip())
    raw = f"{ROOT}/work/vo/{ep}_raw.mp3"
    if not os.path.exists(raw):
        run("curl", "-sS", "-o", raw, take["url"])
    out = f"{ROOT}/assets/audio/vo_{ep}.wav"
    run("ffmpeg", "-v", "error", "-y", "-i", raw, "-af",
        "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,"
        f"silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.1,areverse,atempo={TEMPO}",
        "-ar", "48000", "-ac", "2", out)
    dur = duration(out)
    # pauses inside the line
    err = subprocess.run(["ffmpeg", "-i", out, "-af", "silencedetect=n=-38dB:d=0.18", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    gaps = [(s, e) for s, e in zip(st, en) if e < dur - 0.05]
    # expected boundaries from character counts
    lens = [len(b) for b in beats]
    cum = [sum(lens[:i + 1]) / sum(lens) * dur for i in range(len(beats) - 1)]
    chosen, used = [], set()
    for target in cum:
        # sentence ends pause longer than commas: score by distance, discounted by pause length
        cands = [(abs((s + e) / 2 - target) / max(0.15, e - s) ** 0.7, i) for i, (s, e) in enumerate(gaps)
                 if i not in used and (not chosen or (s + e) / 2 > chosen[-1][1])]
        if cands:
            _, i = min(cands); used.add(i); chosen.append(gaps[i])
        else:
            chosen.append((target, target))
    starts = [0.0] + [e for s, e in chosen]
    ends = [s for s, e in chosen] + [dur]
    json.dump(dict(starts=[round(x, 3) for x in starts], ends=[round(x, 3) for x in ends], dur=round(dur, 3)),
              open(f"{ROOT}/work/vo/{ep}.json", "w"))
    print(ep, f"{dur:.2f}s", "beats at", [round(x, 2) for x in starts], "expected", [round(x, 2) for x in cum])
