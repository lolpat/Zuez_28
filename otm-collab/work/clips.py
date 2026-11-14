"""Accurate's platform screens for the tour scene. work/src/*.mp4 are silent crops of their own app screens, cut from the
Accurate reel the user supplied (times and crop boxes in work/src/segs.txt: name, start, end, x, y, w, h; scaled 1.5x;
their captions and music left out). This re-times each one to its slot in the voice (work/clip_slots.json, written by
gen.py): a clip shorter than its slot plays slower (never below 0.55x) and then holds its last frame; a longer one is
trimmed. Writes assets/clips/<name>.mp4 and work/clip_sizes.json.  Usage: python3 work/clips.py [--sizes-only]"""
import json, subprocess, sys

def probe(p):
    o = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height:format=duration", "-of", "json", p], capture_output=True, text=True).stdout
    d = json.loads(o)
    return d["streams"][0]["width"], d["streams"][0]["height"], float(d["format"]["duration"])

names = [l.split()[0] for l in open("work/src/segs.txt") if l.strip()]
sizes = {n: list(probe(f"work/src/{n}.mp4")[:2]) for n in names}
json.dump(sizes, open("work/clip_sizes.json", "w"), indent=1)
if "--sizes-only" in sys.argv:
    sys.exit(0)
slots = json.load(open("work/clip_slots.json"))
for n in names:
    w, h, L = probe(f"work/src/{n}.mp4")
    d = slots[n]
    if L >= d:
        vf = "fps=30"
        note = "trim"
    else:
        sp = max(0.55, L / d)
        pad = max(0.0, d - L / sp)
        vf = f"setpts=PTS/{sp:.4f},fps=30,tpad=stop_mode=clone:stop_duration={pad + 0.1:.3f}"
        note = f"x{sp:.2f} + hold {pad:.2f}s"
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", f"work/src/{n}.mp4", "-an", "-vf", vf, "-t", f"{d:.3f}",
                    "-c:v", "libx264", "-crf", "18", "-g", "10", "-pix_fmt", "yuv420p", "-movflags", "+faststart", f"assets/clips/{n}.mp4"], check=True)
    print(f"{n:7s} slot {d:5.2f}s  src {L:4.2f}s  {note}  -> {probe(f'assets/clips/{n}.mp4')[2]:.2f}s")
