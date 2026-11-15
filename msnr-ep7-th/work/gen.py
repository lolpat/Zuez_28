"""OTM MSNR series v2, storyline and entry parts (msnr-ep7..ep15; Thai: msnr-epN-th, same file with LANG = "th").
Scenes live in work/story.py (one function per episode). Writes ../index.html, work/cues.json and work/timing.json.
Episodes 7-14 end on the next-episode card; episode 15 is the last of the series and ends on the outro."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *
import story

LANG = "th"
EP = 7
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = f"msnr-ep{EP}" + ("-th" if LANG == "th" else "")
# part 11 stops before its spoken outro line: the series continues with the entry part (12-15), which ends on the outro
TOTAL = init(ROOT, LANG, COMP, f"mix_msnr{EP}" + ("_th" if LANG == "th" else ""), end_key="order" if EP == 11 else None)
getattr(story, f"ep{EP}")()
write()
