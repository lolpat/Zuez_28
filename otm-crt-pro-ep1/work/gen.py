"""OTM CRT PRO (otm-crt-pro-ep0..ep5; Thai: otm-crt-pro-epN-th, same file with LANG = "th").
Scenes live in work/crtpro.py (one function per episode). Writes ../index.html, work/cues.json and work/timing.json.
Episodes 0-4 end on the next-episode card; episode 5 is the last and ends on the outro."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *
import crtpro

LANG = "en"
EP = 1
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = f"otm-crt-pro-ep{EP}" + ("-th" if LANG == "th" else "")
TOTAL = init(ROOT, LANG, COMP, f"mix_crtpro{EP}" + ("_th" if LANG == "th" else ""))
getattr(crtpro, f"ep{EP}")()
write()
