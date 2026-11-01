"""Music from the build (linear gain to about -14 LUFS so the drop keeps its size), a kit hit on the end card, the OTM
voice outro at END+0.3 with the music ducked under it, fade out. Writes assets/audio/mix_viz.wav at the exact length."""
import json, subprocess, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
E = json.load(open("work/env.json")); TOT, END, OFF = E["total"], E["end"], E["offset"]
def measure(args):
    r = subprocess.run(["ffmpeg", "-hide_banner", *args, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    return json.loads(r[r.rindex("{"): r.rindex("}") + 1])
m = measure(["-ss", str(OFF), "-t", str(TOT), "-i", "work/music/51732.mp3"])
gain_m = -14 - float(m["input_i"])
v = measure(["-i", "assets/audio/vo_outro.wav"]); gain_v = -13 - float(v["input_i"])
N = int(round(TOT * 48000)); dv = int((END + 0.3) * 1000); dh = int(END * 1000)
duck = f"volume='1-0.55*min(1\\,max(0\\,(t-{END + 0.15})/0.3))':eval=frame"
fc = (f"[0:a]aresample=48000,asetpts=N/SR/TB,volume={gain_m:.2f}dB,{duck},afade=t=in:d=0.12,afade=t=out:st={TOT - 1.6:.2f}:d=1.6[m];"
      f"[1:a]aresample=48000,volume={gain_v:.2f}dB,adelay={dv}|{dv}[v];"
      f"[2:a]aresample=48000,volume=-3dB,adelay={dh}|{dh}[h];"
      f"[m][v][h]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.84:level=false,asetpts=N/SR/TB,apad=whole_len={N},atrim=end_sample={N},aformat=channel_layouts=stereo[o]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(OFF), "-t", str(TOT + 0.2), "-i", "work/music/51732.mp3", "-i", "assets/audio/vo_outro.wav",
                "-i", "assets/audio/hit.wav", "-filter_complex", fc, "-map", "[o]", "-ar", "48000", "-c:a", "pcm_s16le", "assets/audio/mix_viz.wav"], check=True)
print(f"wrote assets/audio/mix_viz.wav ({TOT}s), music gain {gain_m:+.1f} dB, voice gain {gain_v:+.1f} dB")
