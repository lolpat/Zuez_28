"""OTM MSNR key-level series v2, one episode per key level (msnr-ep1..ep6; Thai: msnr-epN-th, same file with LANG = "th").
The scenes live in work/msnr.py, the per-episode content in work/specs.py. Writes ../index.html, work/cues.json and
work/timing.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *
from msnr import episode
from specs import SPECS

LANG = "en"
EP = 4
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = f"msnr-ep{EP}" + ("-th" if LANG == "th" else "")
TOTAL = init(ROOT, LANG, COMP, f"mix_msnr{EP}" + ("_th" if LANG == "th" else ""))
episode(SPECS[EP])
write()
