"""After the episode renders: Reels-safe copies, the combined full video and a cover image per episode.

The full video plays every episode up to its end card and keeps only the last episode's end card.
"""
import json, os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = f"{ROOT}/renders"
EPS = [f"ep{i}" for i in range(9)]
REELS = ("color=black:s=1080x1920:r=30[bg];[0:v]scale=918:1632:flags=lanczos,fps=30[s];"
         "[bg][s]overlay=x=40:y=140:shortest=1,format=yuv420p")
ENC = ["-c:v", "libx264", "-profile:v", "high", "-level", "4.1", "-crf", "17", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart"]

def run(*a):
    subprocess.run(a, check=True, capture_output=True)

def end_t(ep):
    vo = json.load(open(f"{ROOT}/work/vo/{ep}.json"))
    return round(0.35 + vo["dur"] + 0.7, 2)

os.makedirs(f"{R}/reels", exist_ok=True)
os.makedirs(f"{R}/covers", exist_ok=True)
for ep in EPS:
    src = f"{R}/MSNR_{ep}.mp4"
    run("ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", REELS, *ENC, f"{R}/reels/MSNR_{ep}_Reels.mp4")
    run("ffmpeg", "-v", "error", "-y", "-ss", f"{end_t(ep) - 0.6:.2f}", "-i", src, "-frames:v", "1", "-q:v", "2",
        f"{R}/covers/MSNR_{ep}_cover.jpg")
    print(ep, "done")

# full video: each episode cut at its end card, the last one whole
ins, parts = [], []
for k, ep in enumerate(EPS):
    ins += ["-i", f"{R}/MSNR_{ep}.mp4"]
    cut = "" if ep == EPS[-1] else f"trim=0:{end_t(ep)},"
    acut = "" if ep == EPS[-1] else f"atrim=0:{end_t(ep)},"
    parts.append(f"[{k}:v]{cut}setpts=PTS-STARTPTS,fps=30,format=yuv420p[v{k}];"
                 f"[{k}:a]{acut}asetpts=PTS-STARTPTS,aresample=48000,afade=t=out:st={max(0, end_t(ep) - 0.08) if ep != EPS[-1] else 999}:d=0.08[a{k}];")
fc = "".join(parts) + "".join(f"[v{k}][a{k}]" for k in range(len(EPS))) + f"concat=n={len(EPS)}:v=1:a=1[v][a]"
run("ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", *ENC, f"{R}/MSNR_Full_Series.mp4")
run("ffmpeg", "-v", "error", "-y", "-i", f"{R}/MSNR_Full_Series.mp4", "-filter_complex", REELS, "-map", "0:a", *ENC,
    f"{R}/reels/MSNR_Full_Series_Reels.mp4")
print("full done")
