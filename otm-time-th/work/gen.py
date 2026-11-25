"""OTM "Not much time" (th): general-motivation Reel in the OTM glowing style. See work/timeviz.py.
Writes ../index.html, work/cues.json, work/timing.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *
from timeviz import build
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
init(ROOT, "th", "otm-time-th", "mix_timeth")
build()
