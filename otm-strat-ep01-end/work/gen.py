"""OTM STRATEGIES: the ending clip for ep 0 + 1 (en): 'save this' recap, a think-along quiz (BOS or CHoCH?), and the
follow-for-more outro. Scenes in work/strat.py (end1). Writes ../index.html, work/cues.json, work/timing.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *
import strat
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
init(ROOT, "en", "otm-strat-ep01-end", "mix_st01end")
strat.end1()
write()
