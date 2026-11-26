"""OTM STRATEGIES series, episode 1 (en). Scenes in work/strat.py. Writes ../index.html, work/cues.json, work/timing.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *
import strat
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
init(ROOT, "en", "otm-strat-ep1", "mix_st1")
strat.ep1()
write()
