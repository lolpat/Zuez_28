"""OTM STRATEGIES series, episode 2: Change of Character (th): the answer to ep 1's quiz, the 3 rules (close, a real swing
after the IDM sweep, a BOS to confirm), entering on the pullback, a gold example, the save-this recap, the think-along
quiz and the follow-for-more outro. Scenes in work/strat.py (ep2). Writes ../index.html, work/cues.json, work/timing.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *
import strat
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
init(ROOT, "th", "otm-strat-ep2-th", "mix_st2th")
strat.ep2()
write()
