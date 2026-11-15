"""OTM MSNR PRO (msnr-pro-ep1..ep7; Thai: msnr-pro-epN-th, same file with LANG = "th").
Scenes live in work/pro.py (one function per episode). Writes ../index.html, work/cues.json and work/timing.json.
Episodes 1-6 end on the next-episode card; episode 7 is the last of the series and ends on the outro."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *
import pro

LANG = "th"
EP = 0
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = f"msnr-pro-ep{EP}" + ("-th" if LANG == "th" else "")
TOTAL = init(ROOT, LANG, COMP, f"mix_pro{EP}" + ("_th" if LANG == "th" else ""))
getattr(pro, f"ep{EP}")()
write()
