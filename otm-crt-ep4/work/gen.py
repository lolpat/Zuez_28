"""OTM CRT series, part 4/5: "Timeframe pairs". English (otm-crt-ep4) and Thai (otm-crt-ep4-th) are built from this
same file; only LANG differs. The range and the entry live on different charts: a 4-hour range pairs with a 5- or
15-minute entry, a daily range with a 1-hour entry. Too close and the sweep is noise, too far and you wait days. The
classic mistake: on the 1-minute every small dip inside the range looks like a sweep, and buying them gets stopped;
only the sweep of the range's own low matters. Synthetic example chart; candles up #2962ff, down white.
Writes ../index.html, work/cues.json and work/timing.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *

LANG = "en"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = "otm-crt-ep4" + ("-th" if LANG == "th" else "")
TOTAL = init(ROOT, LANG, COMP, "mix_crt4" + ("_th" if LANG == "th" else ""))
def KW(key, n): return W(G["marks"][key] + n)

def mini_big(s, x, yc, op=1):
    """small icon: one big candle (a higher-timeframe range)"""
    return big_candle(s, x, 46, yc - 70, yc - 52, yc + 50, yc + 70, op, DOWN, glow=False)

def mini_small(s, x, yc, op=1, n=7, seed=3):
    """small icon: a run of little candles (a lower-timeframe chart)"""
    c = path_candles([(0, 40), (2, 60), (4, 45), (6, 70)], seed=seed, noise=4, wick=4)
    ch = Chart(c, n, x - 70, x + 70, yc - 70, yc + 70, 20, 80, 0.6)
    return s.raw(f'<g id="@ID@" style="opacity:{op}">' + ch.candles() + "</g>", "ms")

def pair_row(s, yc, left, right, op=1):
    ids = []
    ids.append(s.raw(f'<rect id="@ID@" x="90" y="{yc - 120}" width="900" height="240" rx="28" fill="#ffffff" fill-opacity="0.04" stroke="#ffffff" stroke-opacity="0.18" stroke-width="2" style="opacity:{op}"/>', "rw"))
    ids.append(mini_big(s, 200, yc - 10, op))
    ids.append(s.label(270, yc + 12, left, 38, WHITE, op, 800, 0.04, "start"))
    ids.append(s.path(f"M 470 {yc} L 540 {yc} M 520 {yc - 16} L 540 {yc} L 520 {yc + 16}", GOLD, 5, drawn=True, style=f"opacity:{op}"))
    ids.append(mini_small(s, 640, yc - 10, op))
    ids.append(s.label(730, yc + 12, right, 36, GOLD, op, 800, 0.02, "start"))
    return ids

# 1  the pairs (frame 0 is the thumbnail)
o1, c1 = 0, K("close") - 0.1
s = S(o1, c1, first=True)
s.label(540, 330, L("THE RANGE AND THE ENTRY", "กรอบราคา กับจุดเข้า"), 44, WHITE, 1, 800, 0.04)
s.label(540, 420, L("LIVE ON DIFFERENT CHARTS", "อยู่คนละกราฟ"), 52, GOLD, 1, 800, 0.04)
r1 = pair_row(s, 760, "4H", L("5M / 15M", "5M / 15M"))
r2 = pair_row(s, 1080, L("DAILY", "รายวัน"), "1H")
s.label(270, 760 + 60, L("RANGE", "กรอบ"), 24, GREY, 1, 700, 0.16, "start"); s.label(730, 760 + 60, L("ENTRY", "จุดเข้า"), 24, GREY, 1, 700, 0.16, "start")
s.label(270, 1080 + 60, L("RANGE", "กรอบ"), 24, GREY, 1, 700, 0.16, "start"); s.label(730, 1080 + 60, L("ENTRY", "จุดเข้า"), 24, GREY, 1, 700, 0.16, "start")
for row, key in ((r1, "p1"), (r2, "p2")):
    tl(f'tl.to("#{row[0]}", {{attr: {{"stroke-opacity": 1, stroke: "{GOLD}", "fill-opacity": 0.08}}, duration: 0.3}}, {K(key):.3f});')
    tl(f'tl.to("#{row[0]}", {{attr: {{"stroke-opacity": 0.18, stroke: "#ffffff", "fill-opacity": 0.04}}, duration: 0.3}}, {K(key) + 3.6 if key == "p1" else c1 - 0.6:.3f});')
    cue(K(key), "pop_1" if key == "p1" else "pop_2", -18)
captions(s, [(K("p1") - 0.1, L("4H RANGE  ·  5M OR 15M ENTRY", "กรอบ 4H  ·  เข้าที่ 5M หรือ 15M"), WHITE),
             (K("p2") - 0.1, L("DAILY RANGE  ·  1H ENTRY", "กรอบรายวัน  ·  เข้าที่ 1H"), GOLD)], c1)

# 2  too close, too far, the sweet spot
o2, c2 = K("close") - 0.1, K("mist") - 0.1
s = S(o2, c2)
series_tag(s, 4)
s.path("M 120 900 H 960", "#ffffff60", 4, drawn=True)
zc = rbox(s, 120, 850, 380, 950, RED, 0.18, 0.9, 2, 0); s.fade(zc, K("close") + 0.2, 0.4)
zf = rbox(s, 700, 850, 960, 950, RED, 0.18, 0.9, 2, 0); s.fade(zf, K("far") + 0.2, 0.4)
zs = rbox(s, 400, 850, 680, 950, GOLD, 0.2, 1, 3, 0); s.fade(zs, K("far") + 1.8, 0.4)
tc = s.label(250, 820, L("TOO CLOSE", "ใกล้เกินไป"), 30, RED, 0, 800, 0.06); s.fade(tc, K("close") + 0.2)
tf = s.label(830, 820, L("TOO FAR", "ห่างเกินไป"), 30, RED, 0, 800, 0.06); s.fade(tf, K("far") + 0.2)
ts = s.label(540, 820, L("SWEET SPOT", "พอดี"), 30, GOLD, 0, 800, 0.06); s.fade(ts, K("far") + 1.8)
nz = s.raw('<g id="@ID@" style="opacity:0">' + "".join(
    f'<line x1="{140 + 20 * k}" y1="{900 - 34 - (k * 37) % 40}" x2="{140 + 20 * k}" y2="{900 + 10 + (k * 23) % 30}" stroke="{WHITE if k % 2 else UP}" stroke-width="7"/>' for k in range(12)) + "</g>", "nz")
s.fade(nz, K("close") + 0.5, 0.3); tl(f'tl.to("#{nz}", {{x: 4, duration: 0.08, yoyo: true, repeat: 15, ease: "none"}}, {K("close") + 0.6:.3f});')
nl = s.label(250, 1010, L("NOISE", "สัญญาณรบกวน"), 30, WHITE, 0, 800, 0.08); s.fade(nl, KW("close", L(8, 1)))
cue(K("close") + 0.5, "tick_1", -20)
clk = s.raw(f'<g id="@ID@" style="opacity:0"><circle cx="830" cy="900" r="36" fill="none" stroke="#fff" stroke-width="5"/>'
            f'<line id="hand" x1="830" y1="900" x2="830" y2="874" stroke="{GOLD}" stroke-width="5" stroke-linecap="round"/></g>', "ck")
s.fade(clk, K("far") + 0.4, 0.3)
tl(f'tl.fromTo("#hand", {{rotation: 0, svgOrigin: "830 900"}}, {{rotation: 720, svgOrigin: "830 900", duration: 2.4, ease: "none", immediateRender: false}}, {K("far") + 0.5:.3f});')
dl = s.label(830, 1010, L("DAYS OF WAITING", "รอหลายวัน"), 30, WHITE, 0, 800, 0.08); s.fade(dl, KW("far", L(7, 1)))
cue(K("far") + 0.4, "tock_1", -20); cue(K("far") + 1.8, "bell_E5", -20)
captions(s, [(K("close") - 0.1, L("TOO CLOSE: THE SWEEP IS NOISE", "ใกล้เกินไป: การกวาดเป็นแค่สัญญาณรบกวน"), RED),
             (K("far") - 0.1, L("TOO FAR: DAYS FOR ONE SETUP", "ห่างเกินไป: รอหลายวันกว่าจะเจอ"), RED)], c2)

# 3  the classic mistake: the 1-minute chart inside the range
HI, LO = 84, 24
C = path_candles([(0, 62), (3, 70), (7, 55), (9, 63), (12, 51), (15, 60), (18, 48), (21, 57), (24, 52), (27, 62),
                  (30, 56), (33, 60), (39, 28), (41, 19), (43, 34), (46, 30), (48, 44)], seed=31, noise=1.2, wick=1.2)
SWI = 41
C[SWI] = (25.5, 26, 19, 25.2)                     # the real sweep: under the CRT low, closed back inside
C[SWI + 1] = (25.2, 30, 24.6, 29.5)
ch = Chart(C, 50, 90, 1000, 560, 1260, 12, 92, 0.66)
N = len(C)
def y(p): return ch.y(p)
DIPS = [7, 12, 18]
o3, c3 = K("mist") - 0.1, K("next") - 0.1
s = S(o3, c3)
series_tag(s, 4)
mp = s.pill(540, 470, L("THE CLASSIC MISTAKE", "ความผิดพลาดที่เจอบ่อย"), RED, WHITE, 26); s.pop(mp, K("mist") + 0.1, 0.4, 0.5); cue(K("mist") + 0.1, "whoosh-short_1", -22)
for p, lab, ly in ((HI, L("CRT HIGH", "ไฮของกรอบ"), -14), (LO, L("CRT LOW", "โลว์ของกรอบ"), 36)):
    s.raw(f'<line id="@ID@" x1="90" y1="{y(p)}" x2="1000" y2="{y(p)}" stroke="{GOLD}" stroke-width="3" stroke-dasharray="14 10"/>', "lv")
    s.label(1000, y(p) + ly, lab, 24, GOLD, 1, 800, 0.1, "end")
m1 = s.label(100, y(HI) + 40, "1M", 26, GREY, 0, 800, 0.1, "start"); s.fade(m1, K("m1") + 0.3)
rid = candles_clip(s, ch)
keys = [(o3, -1), (K("m1") + 0.2, -1), (K("m2") - 0.2, 6), (K("m2") + 1.4, 8), (K("m3") + 0.4, 8), (K("m3") + 1.6, 13),
        (K("m3b") - 0.1, 13), (K("m3b") + 1.0, 19), (K("m5") - 0.4, 19), (K("m5") + 1.6, SWI + 1), (K("next") - 0.5, N - 1)]
reveal(rid, ch, keys, o3)
tags = []
for k, i in enumerate(DIPS):
    tg = ring(s, ch.x(i), y(C[i][2]), 13, GOLD); tags.append(tg)
s.pop(tags[0], K("m2") + 1.2, 0.3, 0.3); cue(K("m2") + 1.2, "tick_2", -20)
# buy one, stopped; then another
for k, (bi, hit, key) in enumerate([(7, 12, "m3"), (12, 18, "m3b")]):
    bp = C[bi][3]
    b = s.pill(ch.x(bi), y(C[bi][2]) + 40, L("BUY", "ซื้อ"), UP, WHITE, 16); s.pop(b, K(key) + 0.1, 0.3, 0.5)
    sl = s.raw(f'<line id="@ID@" x1="{ch.x(bi) - 10:.1f}" y1="{y(C[bi][2] - 1):.1f}" x2="{ch.x(hit) + 10:.1f}" y2="{y(C[bi][2] - 1):.1f}" stroke="{RED}" stroke-width="3" stroke-dasharray="8 6" style="opacity:0"/>', "sl")
    s.fade(sl, K(key) + 0.3, 0.3)
    xm = xmark(s, ch.x(hit) + 28, y(C[bi][2] - 1), 12, RED, 5); s.draw(xm, (K("m3") + 1.6 if k == 0 else K("m3b") + 1.0), 0.25)
    cue((K("m3") + 1.6 if k == 0 else K("m3b") + 1.0), "click_2", -18)
    if k == 1: s.pop(tags[1], K("m3") + 1.6, 0.3, 0.3); s.pop(tags[2], K("m3b") + 1.0, 0.3, 0.3)
# none of those lows were the CRT low; almost no stops under them
crl = rbox(s, 90, y(LO) - 10, 1000, y(LO) + 10, GOLD, 0.25, 1, 2, 0); s.fade(crl, K("m4") + 0.3, 0.4); pulse(crl, K("m4") + 0.8, 2)
cue(K("m4") + 0.3, "bell_C5", -20)
few = []
many = stop_chips(s, [300, 380, 460, 540, 620], y(LO) + 34, RED, "STOP", 16)
for k, i in enumerate(few): s.pop(i, K("m4b") + 0.1 * k, 0.3, 0.4)
for k, i in enumerate(many): s.pop(i, K("m4b") + 0.8 + 0.08 * k, 0.3, 0.4)
fw = s.label(ch.x(13), y(40), L("ALMOST NO STOPS UNDER THESE", "แทบไม่มีสต็อปใต้โลว์เหล่านี้"), 24, WHITE, 0, 800, 0.06); s.fade(fw, K("m4b") + 0.3)
cue(K("m4b") + 0.8, "tick_3", -20)
for i in tags + few + [fw]: out(i, K("m5") - 0.1)
# the sweep of the range's own low
for k, i in enumerate(many):
    tl(f'tl.to("#{i}", {{opacity: 0, y: 30, duration: 0.35, ease: "power2.in"}}, {K("m5") + 1.5 + 0.06 * k:.3f});')
tm = s.pill(ch.x(SWI) - 40, y(19) + 52, L("THIS ONE MATTERS", "อันนี้แหละที่สำคัญ"), GREEN, "#0b0b0b", 22); s.pop(tm, K("m5") + 1.6, 0.4, 0.5)
cue(K("m5") + 1.6, "click-confirm_1", -16)
captions(s, [(K("m1") - 0.1, L("A TRADER DROPS TO THE 1-MINUTE", "ลงไปดูถึงกราฟ 1 นาที"), WHITE),
             (K("m2") - 0.1, L("EVERY SMALL DIP LOOKS LIKE A SWEEP", "ทุกการย่อ ดูเหมือนการกวาด"), GOLD),
             (K("m3") - 0.1, L("BUY ONE: STOPPED", "ซื้อไม้หนึ่ง: โดนสต็อป"), RED), (K("m3b") - 0.1, L("THEN ANOTHER", "แล้วก็อีกไม้"), RED),
             (K("m4") - 0.1, L("NONE OF THEM WAS THE CRT LOW", "ไม่มีอันไหนเป็นโลว์ของกรอบ"), GOLD),
             (K("m4b") - 0.1, L("TINY SWINGS, ALMOST NO STOPS", "สวิงเล็กๆ แทบไม่มีสต็อป"), WHITE),
             (K("m5") - 0.1, L("ONLY THE RANGE'S OWN LOW MATTERS", "สำคัญแค่โลว์ของกรอบเท่านั้น"), GREEN)], c3)

# 4  next part
o4, c4 = K("next") - 0.1, K("order") - 0.05
s = S(o4, c4)
nx_ = s.label(540, 760, L("NEXT  ·  PART 5/5", "ตอนต่อไป  ·  ตอนที่ 5/5"), 30, GREY, 0, 700, 0.2); s.fade(nx_, o4 + 0.1)
a_ = s.label(540, 900, L("THE CRT", "เช็กลิสต์"), 76, WHITE, 0, 800, 0.04); s.pop(a_, o4 + 0.6, 0.4, 0.6)
b_ = s.label(540, 1000, L("CHECKLIST", "CRT"), 76, GOLD, 0, 800, 0.04); s.pop(b_, o4 + 0.9, 0.4, 0.6)
cue(o4 + 0.2, "whoosh-long_1", -22)

outro(K("order") - 0.05)
write()
