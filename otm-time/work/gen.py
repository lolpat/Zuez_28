"""OTM "Not much time" (en): general-motivation Reel in the OTM glowing style. See work/timeviz.py.
Writes ../index.html, work/cues.json, work/timing.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *
from timeviz import build
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
init(ROOT, "en", "otm-time", "mix_time")
build()
