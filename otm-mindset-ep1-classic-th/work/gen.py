"""OTM Mindset ep1 "A loss is a teacher" (th, classic look). See work/mind.py. Writes ../index.html, work/cues.json, work/timing.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *
from mind import build
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
init(ROOT, "th", "otm-mindset-ep1-classic-th", "mix_mind1cth")
build("classic")
