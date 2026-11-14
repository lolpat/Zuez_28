"""OTM trade recap, 12 Nov 2026: a real XAUUSD sell (from work/trade_screenshot.jpg): 3.8 lots, entry 3953.83, stop
3958.28, closed 3938.83 at 14:33 (+15.00 = +$5,700, about 3.4R). The idea (from the trader): old support became
resistance (SBR), a small dip on the way back up was the inducement (IDM), the sell came where price stalled at the SBR
line, the stop went above it, and price took out the IDM low and kept falling.
The entry, stop and close are the real prices; the candles between them are a simplified illustration (the video says
so). Candles up #2962ff, down white. English (Quentin). Writes ../index.html, work/cues.json and work/timing.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *

LANG = "en"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = "otm-recap-1112"
TOTAL = init(ROOT, LANG, COMP, "mix_recap1112")
def KW(key, n): return W(G["marks"][key] + n)

ENTRY, SL, CLOSE = 3953.83, 3958.28, 3938.83          # the real trade
SBR = 3956.5                                           # old support -> resistance
IDM_I, IDM_P = 18, 3948.6                              # the inducement dip
STALL, EI, CI = 21, 22, 40                             # stall high, entry candle, close candle
def px(p): return f"{p:,.2f}"

C = path_candles([(0, 3959), (2, SBR), (4, 3960.5), (6, SBR + 0.1), (8, 3958.5), (11, 3944.5), (14, 3949), (16, 3951.5),
                  (IDM_I, IDM_P), (STALL, 3956.3), (23, 3954.2), (26, 3947), (28, 3949.4), (30, 3945.4), (32, 3948.8),
                  (36, 3936.8), (38, 3940.2), (CI, CLOSE)], seed=12, noise=0.5, wick=0.6)
C[EI] = (C[EI - 1][3], 3954.6, 3952.2, 3952.6)        # the entry candle: sold at 3953.83 inside it
o, h, lo, c = C[CI]; C[CI] = (o, max(h, o, CLOSE), min(lo, o, CLOSE), CLOSE)
ch = Chart(C, 44, 90, 1000, 600, 1240, 3932, 3962)
N = len(C)
assert all(c_[1] < SL for c_ in C[EI:]), "no candle after the entry reaches the stop"
assert C[EI][2] <= ENTRY <= C[EI][1]
def y(p): return ch.y(p)
XR = ch.x(43.6)

def level(s, p, col, text, i0, op=0, dash="12 8", w=3, ly=-12, size=22, anchor_x=None, anchor="end"):
    ln = s.raw(f'<line id="@ID@" x1="{ch.x(i0) - 8:.1f}" y1="{y(p):.1f}" x2="{XR:.1f}" y2="{y(p):.1f}" stroke="{col}" stroke-width="{w}" '
               f'stroke-dasharray="{dash}" style="opacity:{op}"/>', "lv")
    lb = s.label(anchor_x or XR, y(p) + ly, text, size, col, op, 800, 0.06, anchor) if text else None
    return ln, lb

def full_picture(s, op=1):
    rbox(s, ch.x(EI), y(SL), XR, y(ENTRY), RED, 0.16, 0, 0, op)
    rbox(s, ch.x(EI), y(ENTRY), ch.x(CI), y(CLOSE), GREEN, 0.14, 0, 0, op)
    level(s, SBR, GOLD, "SBR", 0, op, ly=-10)
    level(s, SL, RED, f"SL {px(SL)}", EI, op)
    level(s, ENTRY, WHITE, f"SELL {px(ENTRY)}", EI, op, ly=34, anchor_x=XR)
    level(s, CLOSE, GREEN, f"CLOSE {px(CLOSE)}", EI, op, ly=34, anchor_x=ch.x(33))
    s.raw('<g id="@ID@">' + ch.candles() + "</g>", "cg")

# 1  hook / thumbnail: the whole trade
o1, c1 = 0, K("why") - 0.1
s = S(o1, c1, first=True)
sym_pill(s)
s.label(540, 330, "MY TRADE RECAP", 40, WHITE, 1, 800, 0.08)
s.label(540, 440, "+$5,700", 96, GOLD, 1, 800, 0.04)
full_picture(s)
s.label(540, 1290, "REAL ENTRY, STOP AND CLOSE  ·  CANDLES SIMPLIFIED", 20, GREY, 1, 700, 0.1)
captions(s, [(0.1, "XAUUSD SELL  ·  5-MINUTE", WHITE), (K("sold") - 0.1, f"SOLD AT {px(ENTRY)}", WHITE),
             (K("result") - 0.1, "CLOSED 15.00 LOWER", GREEN)], c1)
cue(0.3, "whoosh-short_1", -22)

# 2  the walk-through
o2, c2 = K("why") - 0.1, K("pnl") - 0.1
s = S(o2, c2)
s.label(540, 300, "MY TRADE RECAP", 26, GOLD, 1, 700, 0.2)
hp = s.pill(540, 470, "XAUUSD  ·  5M  ·  12 NOV 2026", WHITE, "#0b0b0b", 26); s.pop(hp, o2 + 0.2, 0.4, 0.5)
risk = rbox(s, ch.x(EI), y(SL), XR, y(ENTRY), RED, 0.16, 0, 0)
prof = rbox(s, ch.x(EI), y(ENTRY), ch.x(CI), y(CLOSE), GREEN, 0.14, 0, 0)
supL = s.raw(f'<line id="@ID@" x1="{ch.x(0) - 8:.1f}" y1="{y(SBR):.1f}" x2="{ch.x(8):.1f}" y2="{y(SBR):.1f}" stroke="#fff" stroke-width="3" stroke-dasharray="12 8" style="opacity:0"/>', "sp")
rid = candles_clip(s, ch)
keys = [(o2, -1), (K("sup") - 0.3, -1), (K("sup") + 0.8, 7), (K("brk"), 7), (K("brk") + 1.0, 11), (K("idm") - 0.2, 11),
        (K("idm") + 1.6, IDM_I + 1), (K("stall") - 0.2, IDM_I + 1), (K("stall") + 1.2, STALL), (K("entry") - 0.1, STALL),
        (K("entry") + 0.3, EI), (K("drop") - 0.1, EI), (K("take") + 0.6, 27), (K("fall") + 0.2, 27), (K("close") + 0.2, CI)]
reveal(rid, ch, keys, o2)
# old support, the break, support becomes resistance
s.fade(supL, K("sup") + 0.2, 0.4)
for i in (2, 6):
    r = ring(s, ch.x(i), y(SBR), 14, WHITE); s.pop(r, K("sup") + 0.4 + (0.3 if i == 6 else 0), 0.3, 0.3); out(r, K("sbr"))
sl_ = s.label(ch.x(0), y(SBR) + 34, "SUPPORT", 22, WHITE, 0, 800, 0.08, "start"); s.fade(sl_, K("sup") + 0.3); out(sl_, K("sbr"))
cue(K("sup") + 0.4, "bell_G4", -24)
bk = s.pill(ch.x(10) + 30, y(3949) , "BREAK", WHITE, "#0b0b0b", 20); s.pop(bk, K("brk") + 0.7, 0.35, 0.5); out(bk, K("sbr") + 0.6)
sbrL = s.raw(f'<line id="@ID@" x1="{ch.x(0) - 8:.1f}" y1="{y(SBR):.1f}" x2="{ch.x(0) - 8:.1f}" y2="{y(SBR):.1f}" stroke="{GOLD}" stroke-width="4" stroke-dasharray="12 8"/>', "sb")
tl(f'tl.to("#{sbrL}", {{attr: {{x2: {XR:.1f}}}, duration: 0.9, ease: "power2.out"}}, {K("sbr"):.3f});')
out(supL, K("sbr") + 0.1)
sbt = s.label(XR, y(SBR) - 12, "SBR: SUPPORT BECOMES RESISTANCE", 22, GOLD, 0, 800, 0.06, "end"); s.fade(sbt, K("sbr") + 0.5)
cue(K("sbr"), "whoosh-short_2", -22)
# the inducement and the stops under it
ir = ring(s, ch.x(IDM_I), y(IDM_P), 16, LBLUE); s.pop(ir, K("idm") + 1.6, 0.35, 0.3)
it = s.pill(ch.x(IDM_I), y(IDM_P) + 44, "IDM", LBLUE, "#0b0b0b", 20); s.pop(it, K("idm2"), 0.35, 0.5)
chips = stop_chips(s, [ch.x(IDM_I) - 72, ch.x(IDM_I), ch.x(IDM_I) + 72], y(IDM_P) + 86, RED, "STOP", 16)
for k, i in enumerate(chips): s.pop(i, KW("idm2", 6) + 0.1 * k, 0.3, 0.4)
cue(K("idm2"), "swell_1", -24)
# the stall at the SBR and the sell
st = ring(s, ch.x(STALL), y(3956.3), 18, GOLD); s.pop(st, K("stall") + 1.2, 0.35, 0.3); out(st, K("sl"))
enL, enT = level(s, ENTRY, WHITE, None, EI)
s.fade(enL, K("entry") + 0.3, 0.3)
sp_ = s.pill(ch.x(EI) + 140, y(ENTRY) + 2, f"SELL {px(ENTRY)}", RED, WHITE, 20); s.pop(sp_, K("entry") + 0.3, 0.35, 0.5)
cue(K("entry") + 0.3, "bell_E5", -20)
# the stop above the line
slL, slT = level(s, SL, RED, f"SL {px(SL)}", EI)
s.fade(slL, K("sl") + 0.2, 0.4); s.fade(slT, K("sl") + 0.3); s.fade(risk, K("sl") + 0.4, 0.4)
rk = s.label(XR - 10, y((SL + ENTRY) / 2) + 8, "RISK 4.45", 20, RED, 0, 800, 0.06, "end"); s.fade(rk, K("risk"))
out(sbt, K("sl"))
# the drop: the IDM low goes, then the run to the close
for k, i in enumerate(chips):
    tl(f'tl.to("#{i}", {{opacity: 0, y: 30, duration: 0.35, ease: "power2.in"}}, {K("take") + 0.4 + 0.08 * k:.3f});')
cue(K("take") + 0.4, "whoosh-short_3", -22)
for i in (ir, it): out(i, K("fall") + 0.4)
clL, clT = level(s, CLOSE, GREEN, f"CLOSE {px(CLOSE)}", EI, ly=34, anchor_x=ch.x(33))
s.fade(clL, K("close") + 0.2, 0.3); s.fade(clT, K("close") + 0.3); s.fade(prof, K("close") + 0.3, 0.5)
cue(K("close") + 0.3, "bell_G5", -20)
rr = s.pill(ch.x(26), y(3941.5), "+15.00  ·  ABOUT 3.4R", GREEN, "#0b0b0b", 22); s.pop(rr, K("rr"), 0.4, 0.5)
s.label(540, 1290, "REAL ENTRY, STOP AND CLOSE  ·  CANDLES SIMPLIFIED", 20, GREY, 1, 700, 0.1)
captions(s, [(o2 + 0.1, "HERE'S WHY", WHITE), (K("sup") - 0.1, "THIS LEVEL WAS SUPPORT", WHITE),
             (K("brk") - 0.1, "PRICE BROKE BELOW IT", WHITE), (K("sbr") - 0.1, "OLD SUPPORT = NEW RESISTANCE", GOLD),
             (K("idm") - 0.1, "ONE SMALL DIP ON THE WAY UP", LBLUE), (K("idm2") - 0.1, "THE INDUCEMENT: STOPS UNDER IT", LBLUE),
             (K("stall") - 0.1, "PRICE STALLS AT THE SBR", GOLD), (K("entry") - 0.1, f"SELL {px(ENTRY)}", RED),
             (K("sl") - 0.1, f"STOP ABOVE THE LINE: {px(SL)}", RED), (K("drop") - 0.1, "PRICE ROLLS OVER", WHITE),
             (K("take") - 0.1, "THE IDM LOW GOES", WHITE), (K("fall") - 0.1, "AND KEEPS FALLING", WHITE),
             (K("close") - 0.1, f"CLOSED {px(CLOSE)}", GREEN), (K("rr") - 0.1, "15.00 PER OUNCE  ·  ABOUT 3.4x RISK", GREEN)], c2)

# 3  the result
o3, c3 = K("pnl") - 0.1, K("recap") - 0.1
s = S(o3, c3)
s.label(540, 300, "MY TRADE RECAP", 26, GOLD, 1, 700, 0.2)
s.label(540, 560, "XAUUSD  ·  SELL  ·  3.8 LOTS", 32, LBL, 1, 800, 0.1)
pn = s.label(540, 760, "+$5,700", 150, GOLD, 0, 800, 0.02); s.pop(pn, KW("pnl", 4), 0.5, 0.5); cue(KW("pnl", 4), "bell_A4", -16)
for k, (a, b, col) in enumerate([("ENTRY", px(ENTRY), WHITE), ("STOP", px(SL), RED), ("CLOSE", px(CLOSE), GREEN), ("RESULT", "+15.00  ·  ABOUT 3.4R", GOLD)]):
    yy = 920 + 80 * k
    l_ = s.label(250, yy, a, 30, GREY, 0, 800, 0.12, "start")
    v_ = s.label(830, yy, b, 34 if k < 3 else 30, col, 0, 800, 0.04 if k < 3 else 0.02, "end")
    for i in (l_, v_): s.fade(i, o3 + 0.3 + 0.15 * k, 0.35, y=8)
s.label(540, 1300, "12 NOV 2026  ·  CLOSED 14:33  ·  5-MINUTE CHART", 22, GREY, 1, 700, 0.1)

# 4  level, inducement, entry, stop; then let price do the work
o4, c4 = K("recap") - 0.1, K("order") - 0.05
s = S(o4, c4)
s.label(540, 300, "MY TRADE RECAP", 26, GOLD, 1, 700, 0.2)
for k, (w_, col) in enumerate([("LEVEL", GOLD), ("INDUCEMENT", LBLUE), ("ENTRY", WHITE), ("STOP", RED)]):
    t = KW("recap", k)
    lb = s.label(540, 640 + 140 * k, w_, 70, col, 0, 800, 0.06); s.pop(lb, t, 0.35, 0.6)
    cue(t, "bell_C5" if k == 0 else "bell_E5" if k == 2 else "swell_2", -26)
captions(s, [(K("let") - 0.1, "THEN LET PRICE DO THE WORK", WHITE)], c4, 1290, 34)

outro(K("order") - 0.05)
write()
