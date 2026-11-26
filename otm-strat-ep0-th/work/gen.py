"""OTM STRATEGIES series, episode 0 (th). Scenes in work/strat.py. Writes ../index.html, work/cues.json, work/timing.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *
import strat
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
init(ROOT, "th", "otm-strat-ep0-th", "mix_st0th")
strat.ep0()
write()
