"""OTM MSNR key-level series v2, episode 0: the overview (msnr-ep0; Thai msnr-ep0-th, same file with LANG = "th").
MSNR = exact levels from candle opens and closes, not zones; where price reacts, reverses, rejects or continues; the six
key levels; every entry / order block / liquidity target must line up with one; and the higher-timeframe bias first.
Writes ../index.html, work/cues.json and work/timing.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *
from msnr import series_tag_m, title_block, next_card, KW

LANG = "th"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = "msnr-ep0" + ("-th" if LANG == "th" else "")
TOTAL = init(ROOT, LANG, COMP, "mix_msnr0" + ("_th" if LANG == "th" else ""))
LEVELS = [("CLASSIC V", "CLASSIC V"), ("CLASSIC A", "CLASSIC A"), ("SBR", "SBR"), ("RBS", "RBS"), ("OCL", "OCL"), ("QM", "QM")]

# 1  title (frame 0 is the thumbnail: the title and the six levels)
o1, c1 = 0, K("exact") - 0.1
s = S(o1, c1, first=True)
s.label(540, 300, L("MSNR KEY LEVELS", "MSNR KEY LEVELS"), 30, GOLD, 1, 700, 0.2)
s.label(540, 520, "MSNR", 150, WHITE, 1, 800, 0.06)
s.label(540, 610, L("MALAYSIAN SUPPORT & RESISTANCE", "MALAYSIAN SUPPORT & RESISTANCE"), 32, GOLD, 1, 700, 0.1)
for k, (en, th) in enumerate(LEVELS):
    x = 300 if k % 2 == 0 else 780; yy = 780 + 110 * (k // 2)
    s.pill(x, yy, f"{k + 1}  " + L(en, th), WHITE if k % 2 == 0 else GOLD, "#111", 30, 1)
captions(s, [(0.1, L("SIX KEY LEVELS", "6 KEY LEVELS"), WHITE)], c1)
cue(0.3, "whoosh-short_1", -22)

# 2  exact levels, not zones; react, reverse, reject, continue
o2, c2 = K("exact") - 0.1, K("six") - 0.1
s = S(o2, c2)
s.label(540, 300, L("MSNR KEY LEVELS", "MSNR KEY LEVELS"), 26, GOLD, 1, 700, 0.2)
zb = rbox(s, 160, 640, 920, 860, GREY, 0.22, 0.8, 2); s.fade(zb, K("exact") + 0.1, 0.4)
zl = s.label(540, 760, L("WIDE ZONE", "WIDE ZONE"), 40, GREY, 0, 800, 0.1); s.fade(zl, K("exact") + 0.2)
xz = xmark(s, 540, 750, 70, RED, 9); s.draw(xz, KW("exact", L(2, 1)) - 0.2, 0.35)
for i in (zb, zl, xz): out(i, KW("exact", L(4, 2)), 0.4, 0.15)
b1 = big_candle(s, 470, 70, 600, 840, 750, 880, 0, DOWN); b2 = big_candle(s, 560, 70, 690, 750, 650, 790, 0, UP)
s.pop(b1, KW("exact", L(4, 2)), 0.4, 0.4); s.pop(b2, KW("exact", L(4, 2)) + 0.2, 0.4, 0.4)
lv = s.raw(f'<line id="@ID@" x1="420" y1="750" x2="420" y2="750" stroke="{GOLD}" stroke-width="6"/>', "lv")
tl(f'tl.to("#{lv}", {{attr: {{x2: 980}}, duration: 0.7, ease: "power2.out"}}, {KW("exact", L(6, 3)):.3f});')
ll = s.label(980, 734, L("EXACT LEVEL", "EXACT LEVEL"), 30, GOLD, 0, 800, 0.08, "end"); s.fade(ll, KW("exact", L(6, 3)) + 0.4)
cl = s.label(410, 760, L("CLOSE", "CLOSE"), 24, WHITE, 0, 800, 0.08, "end"); s.fade(cl, KW("exact", L(8, 4)))
op_ = s.label(610, 760, L("OPEN", "OPEN"), 24, LBLUE, 0, 800, 0.08, "start"); s.fade(op_, KW("exact", L(7, 3)) + 0.2)
cue(KW("exact", L(6, 3)), "whoosh-short_2", -22)
for k, ((en, th), tok) in enumerate(zip([("REACT", "REACTION"), ("REVERSE", "REVERSAL"), ("REJECT", "REJECTION"), ("CONTINUE", "CONTINUATION")], L([7, 8, 9, 11], [0, 1, 2, 3]))):
    x = 300 if k % 2 == 0 else 780; yy = 1000 + 110 * (k // 2)
    p = s.pill(x, yy, L(en, th), [GOLD, WHITE, RED, LBLUE][k], "#111" if k != 2 else WHITE, 32); s.pop(p, KW("react", tok), 0.35, 0.5)
    cue(KW("react", tok), "tick-crisp_" + str(k % 3 + 1), -20)
captions(s, [(K("exact") - 0.1, L("EXACT LEVELS, NOT ZONES", "EXACT LEVEL ไม่ใช่ ZONE"), GOLD),
             (K("react") - 0.1, L("WHERE PRICE MAKES A DECISION", "จุดที่ราคาตัดสินใจ"), WHITE)], c2)

# 3  the six key levels
o3, c3 = K("six") - 0.1, K("align") - 0.1
s = S(o3, c3)
s.label(540, 300, L("MSNR KEY LEVELS", "MSNR KEY LEVELS"), 26, GOLD, 1, 700, 0.2)
s.label(540, 520, L("6 KEY LEVELS", "6 KEY LEVELS"), 72, WHITE, 1, 800, 0.04)
for k, (en, th) in enumerate(LEVELS):
    x = 300 if k % 2 == 0 else 780; yy = 700 + 140 * (k // 2)
    p = s.pill(x, yy, f"{k + 1}  " + L(en, th), WHITE if k % 2 == 0 else GOLD, "#111", 34); s.pop(p, K(f"l{k + 1}"), 0.35, 0.5)
    cue(K(f"l{k + 1}"), "bell_" + ["G4", "C5", "E5", "G4", "C5", "E5"][k], -24)
captions(s, [(o3 + 0.1, L("CLASSIC V · A · SBR · RBS · OCL · QM", "V · A · SBR · RBS · OCL · QM"), WHITE)], c3)

# 4  everything lines up with a key level
o4, c4 = K("align") - 0.1, K("htf") - 0.1
s = S(o4, c4)
s.label(540, 300, L("MSNR KEY LEVELS", "MSNR KEY LEVELS"), 26, GOLD, 1, 700, 0.2)
items = [("ENTRY", "ENTRY"), ("ORDER BLOCK", "ORDER BLOCK"), ("LIQUIDITY", "LIQUIDITY")]
for k, (en, th) in enumerate(items):
    x = [220, 540, 860][k]
    p = s.pill(x, 640, L(en, th), WHITE, "#111", 28); s.pop(p, o4 + 0.3 + 0.35 * k, 0.35, 0.5)
    a = arrow(s, x, 690, 540 + (x - 540) * 0.3, 900, GOLD, 5, 20); show_arrow(s, a, o4 + 1.4 + 0.15 * k, 0.5)
kl = s.raw(f'<line id="@ID@" x1="160" y1="940" x2="920" y2="940" stroke="{GOLD}" stroke-width="7" style="opacity:0;filter:drop-shadow(0 0 12px {GOLD})"/>', "kl")
s.fade(kl, o4 + 1.9, 0.4)
kt = s.label(540, 1010, L("MUST LINE UP WITH A KEY LEVEL", "ต้องตรงกับ KEY LEVEL"), 38, GOLD, 0, 800, 0.04); s.fade(kt, o4 + 2.1)
cue(o4 + 1.9, "swell_1", -22)
captions(s, [(o4 + 0.1, L("NO KEY LEVEL, NO TRADE", "ไม่ตรง KEY LEVEL ก็ไม่เทรด"), WHITE)], c4)

# 5  higher-timeframe bias first
o5, c5 = K("htf") - 0.1, K("next") - 0.1
s = S(o5, c5)
s.label(540, 300, L("MSNR KEY LEVELS", "MSNR KEY LEVELS"), 26, GOLD, 1, 700, 0.2)
r1 = s.label(540, 520, L("RULE #1", "กฎข้อแรก"), 40, GREY, 0, 800, 0.2); s.fade(r1, o5 + 0.2)
hb = big_candle(s, 300, 110, 640, 690, 1000, 1060, 0, DOWN); s.pop(hb, o5 + 0.6, 0.45, 0.4)
hl_ = s.label(300, 1120, "HTF", 34, WHITE, 0, 800, 0.1); s.fade(hl_, o5 + 0.8)
a = arrow(s, 400, 850, 560, 850, GOLD, 6, 24); show_arrow(s, a, o5 + 1.2, 0.4)
mini = Chart(path_candles([(0, 70), (3, 80), (6, 55), (9, 62), (13, 25)], seed=4, noise=3, wick=3), 15, 600, 940, 680, 1060, 0, 100, 0.6)
mg = s.raw(f'<g id="@ID@" style="opacity:0">' + mini.candles() + "</g>", "mc"); s.fade(mg, o5 + 1.5, 0.5)
ml = s.label(770, 1120, "LTF", 34, WHITE, 0, 800, 0.1); s.fade(ml, o5 + 1.6)
bt = s.label(540, 1240, L("CONFIRM THE BIAS ON THE HTF FIRST", "ยืนยัน BIAS บน HTF ก่อนเสมอ"), 34, GOLD, 0, 800, 0.04); s.fade(bt, KW("htf", L(13, 2)), 0.4, y=10)
cue(o5 + 0.6, "bell_A4", -20)
captions(s, [(o5 + 0.1, L("NO SETUP WITHOUT HTF BIAS", "ไม่มี SETUP ถ้าไม่มี HTF BIAS"), WHITE)], c5, 1352)

next_card(s, K("next") - 0.1, G["TOTAL"], 1, "CLASSIC V", "CLASSIC V")
write()
