"""OTM MSNR series v2, storyline part (msnr-ep7..ep11; Thai: msnr-epN-th, same file with LANG = "th").
Scenes live in work/story.py (one function per episode). Writes ../index.html, work/cues.json and work/timing.json.
Episodes 7-10 end on the next-episode card; episode 11 is the last of the series and ends on the outro."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *
import story

LANG = "th"
EP = 9
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = f"msnr-ep{EP}" + ("-th" if LANG == "th" else "")
TOTAL = init(ROOT, LANG, COMP, f"mix_msnr{EP}" + ("_th" if LANG == "th" else ""))
getattr(story, f"ep{EP}")()
write()
