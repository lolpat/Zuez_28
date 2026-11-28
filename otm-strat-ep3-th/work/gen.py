"""OTM STRATEGIES series, episode 3: Liquidity Sweep (th): the answer to ep 2's quiz, BSL / SSL and equal highs / lows,
valid liquidity, run vs sweep, sweep -> CHoCH -> FVG / OB -> pullback, a gold example, the save-this recap, the
think-along quiz and the follow-for-more outro. Scenes in work/strat.py (ep3). Writes ../index.html, cues, timing."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *
import strat
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
init(ROOT, "th", "otm-strat-ep3-th", "mix_st3th")
strat.ep3()
write()
