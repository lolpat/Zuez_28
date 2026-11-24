"""OTM Mindset ep1 "A loss is a teacher" (en, otm look). See work/mind.py. Writes ../index.html, work/cues.json, work/timing.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *
from mind import build
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
init(ROOT, "en", "otm-mindset-ep1", "mix_mind1")
build("otm")
