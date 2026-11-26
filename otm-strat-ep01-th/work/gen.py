"""OTM STRATEGIES: episode 0 + episode 1 in one video (th), ending on the Order the Market outro (follow for more).
Voice = ep 0 take (up to its next card) + ep 1 take + the outro line from the otm-mindset-ep1 take (same voice);
work/marks.json holds both parts' marks prefixed a: / b:. Scenes in work/strat.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *
import strat
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
init(ROOT, "th", "otm-strat-ep01-th", "mix_st01th")
ALL = dict(G["marks"])
def part(p): return {k[2:]: v for k, v in ALL.items() if k.startswith(p + ":")}
G["marks"] = part("a")
strat.CFG.update(end0=False, outro1=True)
strat.ep0()
G["marks"] = part("b")
strat.CFG["start1"] = round(K("hook") - 0.15, 3)
strat.ep1()
write()
