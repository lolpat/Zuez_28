"""OTM CRT series, part 2/5: "Real sweep vs fake". English (otm-crt-ep2) and Thai (otm-crt-ep2-th) are built from this
same file; only LANG differs. The sweep is not the signal, the close is: price drops under the CRT low, then either
(A) closes back inside (a real sweep) or (B) closes below (price accepting lower prices; buying it gets stopped out).
If neither side is taken there is no trade. No close back inside, no CRT. Synthetic example charts; candles up
#2962ff, down white. Writes ../index.html, work/cues.json and work/timing.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *

LANG = "en"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = "otm-crt-ep2" + ("-th" if LANG == "th" else "")
TOTAL = init(ROOT, LANG, COMP, "mix_crt2" + ("_th" if LANG == "th" else ""))
def KW(key, n): return W(G["marks"][key] + n)

HI, LO = 72, 32
NX = 24
pre = path_candles([(0, 54), (3, 64), (6, 46), (9, 53), (11, 35)], seed=4, noise=1.6, wick=1.6)
pre[11] = (37.5, 38, 33.6, 34)
A = pre + [(34, 37, 25, 36.5)] + path_candles([(0, 36.5), (3, 47), (5, 42), (9, 62)], seed=8, noise=1.4, wick=1.5, start=36.5)[1:]
B = pre + [(34, 34.5, 25, 26.2)] + path_candles([(0, 26.2), (2, 29.5), (5, 18), (6, 21), (9, 11)], seed=9, noise=1.2, wick=1.3, start=26.2)[1:]
SW = 11 + 1
cA = Chart(A, NX, 250, 1000, 560, 1260, 10, 80)
cB = Chart(B, NX, 250, 1000, 560, 1260, 10, 80)
cP = Chart(pre, NX, 250, 1000, 560, 1260, 10, 80)
INS = path_candles([(0, 50), (4, 64), (8, 42), (12, 62), (16, 40), (20, 58), (23, 50)], seed=12, noise=1.6, wick=1.6)
cI = Chart(INS, NX, 250, 1000, 560, 1260, 10, 80)
HX, HW, BX0, BX1 = 165, 84, 115, 1010
def y(p): return cA.y(p)

def frame(s, op=1, labels=True):
    """the 4H range: the higher-timeframe candle, the box, the CRT high and low lines"""
    rbox(s, BX0, y(HI), BX1, y(LO), GOLD, 0.07, 0.0, 0, op)
    big_candle(s, HX, HW, y(HI), y(HI - 3), y(LO + 3), y(LO), op)
    hline(s, cA, HI, BX0, NX, GOLD, 3, "14 10", op); hline(s, cA, LO, BX0, NX, GOLD, 3, "14 10", op)
    s.label(HX, y(HI) - 22, "4H", 26, GREY, op, 800, 0.1)
    if labels:
        s.label(BX1 - 6, y(HI) - 14, L("CRT HIGH", "ไฮของกรอบ"), 26, GOLD, op, 800, 0.12, "end")
        s.label(BX1 - 6, y(LO) - 14, L("CRT LOW", "โลว์ของกรอบ"), 26, GOLD, op, 800, 0.12, "end")

def mini(s, x, ok, op=1):
    """thumbnail icon: one candle against a line, closing back above it (ok) or below it"""
    ly = 880
    g = s.raw(f'<line id="@ID@" x1="{x - 120}" y1="{ly}" x2="{x + 120}" y2="{ly}" stroke="{GOLD}" stroke-width="4" stroke-dasharray="14 10" style="opacity:{op}"/>', "ln")
    if ok:
        big_candle(s, x, 110, 600, 840, 720, 1080, op, UP)
    else:
        big_candle(s, x, 110, 600, 640, 1010, 1080, op, DOWN)
    (check if ok else xmark)(s, x, 1150, 30, GREEN if ok else RED, 8)
    s.label(x, 1240, L("CLOSE BACK INSIDE", "ปิดกลับเข้ากรอบ") if ok else L("CLOSE BELOW", "ปิดใต้โลว์"), 28, GREEN if ok else RED, op, 800, 0.06)
    return g

# 1  hook: the sweep is not the signal, the close is
s = S(0, K("setup") - 0.15, first=True)
s.label(540, 330, L("THE SWEEP IS NOT THE SIGNAL.", "ไส้เทียนไม่ใช่สัญญาณ"), 44, WHITE, 1, 800, 0.04)
s.label(540, 420, L("THE CLOSE IS.", "ราคาปิดคือสัญญาณ"), 64, GOLD, 1, 800, 0.06)
mini(s, 300, True); mini(s, 780, False)
captions(s, [(0.1, L("REAL SWEEP  VS  FAKE SWEEP", "กวาดจริง  กับ  กวาดปลอม"), WHITE)], K("setup") - 0.15)
cue(0.3, "whoosh-short_1", -22)

# 2  the 4H range, the dip under the low, then A (real) and B (fake)
o2, c2 = K("setup") - 0.15, K("c") - 0.1
s = S(o2, c2)
series_tag(s, 2)
frame(s)
rp = candles_clip(s, cP)
reveal(rp, cP, [(o2, -1), (o2 + 0.4, -1), (K("dip") - 0.2, 10), (K("dip") + 0.6, 11)], o2)
# a probe wick under the low (shared by A and B) before either close
probe = s.raw(f'<line id="@ID@" x1="{cA.x(SW)}" y1="{y(34)}" x2="{cA.x(SW)}" y2="{y(25)}" stroke="{WHITE}" stroke-width="2.5" style="opacity:0"/>', "pw")
s.fade(probe, K("dip") + 0.9, 0.4); cue(K("dip") + 0.9, "whoosh-short_2", -22)
q = s.label(cA.x(SW) + 30, y(22), "?", 56, GOLD, 0, 800, 0, "start"); s.pop(q, KW("dip", L(5, 2)), 0.35, 0.4)
two = s.label(540, 560, L("2 OUTCOMES", "เป็นไปได้ 2 แบบ"), 30, GREY, 0, 800, 0.16); s.fade(two, KW("dip", L(5, 2)))
out(q, K("a")); out(two, K("a")); out(probe, K("a"))
# A: closes back inside -> real sweep
ga = s.uid("ga"); s.items.append(f'<g id="{ga}">')
ra = candles_clip(s, Chart(A[SW:], NX, cA.x0 + cA.sp * SW, cA.x1 + cA.sp * SW, 560, 1260, 10, 80))
s.items.append("</g>")
def edgeA(i): return round(cA.sp * (i + 1.05), 1)
tl(f'tl.set("#{ra}", {{attr: {{width: 0}}}}, {o2:.3f});')
tl(f'tl.set("#{ra}", {{attr: {{x: {cA.x0 + cA.sp * SW:.1f}}}}}, {o2:.3f});')
tl(f'tl.to("#{ra}", {{attr: {{width: {edgeA(0)}}}, duration: 0.3}}, {K("a") + 0.2:.3f});')
tl(f'tl.to("#{ra}", {{attr: {{width: {edgeA(len(A) - SW - 1)}}}, duration: 2.6, ease: "none"}}, {K("areal") + 0.5:.3f});')
pa = s.pill(160 + 30, 560, L("A", "A"), GREEN, "#0b0b0b", 30); s.pop(pa, K("a"), 0.35, 0.5)
ca = check(s, cA.x(SW) + 50, y(36), 22, GREEN, 7); s.draw(ca, KW("a", L(3, 1)), 0.35); cue(KW("a", L(3, 1)), "click-confirm_1", -18)
rs = s.pill(cA.x(SW), y(25) + 56, L("REAL SWEEP", "กวาดของจริง"), GREEN, "#0b0b0b", 24); s.pop(rs, K("areal"), 0.35, 0.5)
dn = stop_chips(s, [cA.x(5), cA.x(8), cA.x(11) + 40], y(LO) + 34, RED, "STOP", 18)
for k, i in enumerate(dn):
    s.pop(i, o2 + 0.6 + 0.1 * k, 0.3, 0.4)
    tl(f'tl.to("#{i}", {{opacity: 0, y: 30, duration: 0.35, ease: "power2.in"}}, {K("areal") + 1.0 + 0.1 * k:.3f});')
cue(K("areal") + 1.0, "tick_1", -20)
for i in (ga, pa, ca, rs): out(i, K("b") - 0.15, 0.25)
# B: closes below -> not a sweep, price accepts lower prices, buying it gets stopped
gb = s.uid("gb"); s.items.append(f'<g id="{gb}">')
rb_ = candles_clip(s, Chart(B[SW:], NX, cB.x0 + cB.sp * SW, cB.x1 + cB.sp * SW, 560, 1260, 10, 80))
s.items.append("</g>")
tl(f'tl.set("#{rb_}", {{attr: {{x: {cB.x0 + cB.sp * SW:.1f}}}}}, {o2:.3f});')
tl(f'tl.to("#{rb_}", {{attr: {{width: {edgeA(0)}}}, duration: 0.3}}, {K("b") + 0.2:.3f});')
tl(f'tl.to("#{rb_}", {{attr: {{width: {edgeA(len(B) - SW - 1)}}}, duration: 2.8, ease: "none"}}, {K("bfake") + 1.0:.3f});')
pb = s.pill(190, 560, "B", RED, WHITE, 30); s.pop(pb, K("b"), 0.35, 0.5)
xb = xmark(s, cB.x(SW) + 48, y(30), 18, RED, 7); s.draw(xb, KW("b", L(4, 1)), 0.3); cue(KW("b", L(4, 1)), "tock_1", -18)
ns = s.pill(cB.x(SW) - 20, y(LO) - 56, L("NOT A SWEEP", "ไม่ใช่การกวาด"), RED, WHITE, 24); s.pop(ns, K("bfake"), 0.35, 0.5)
acc = s.label(cB.x(SW) + 120, y(10), L("ACCEPTING LOWER PRICES", "ยอมรับราคาที่ต่ำลง"), 24, RED, 0, 800, 0.06); s.fade(acc, K("bfake") + 1.2)
by = s.pill(cB.x(SW) - 70, y(26.2), L("BUY", "ซื้อ"), UP, WHITE, 20); s.pop(by, K("bstop"), 0.3, 0.5)
sl = hline(s, cB, 21.5, SW - 3, SW + 6, RED, 3, "10 8"); s.fade(sl, K("bstop") + 0.3)
slb = s.label(cB.x(SW - 3) - 8, y(21.5) + 9, "SL", 22, RED, 0, 800, 0.06, "end"); s.fade(slb, K("bstop") + 0.3)
so = s.pill(cB.x(SW + 5), y(21.5) - 48, L("STOPPED OUT", "โดนสต็อป"), RED, WHITE, 22); s.pop(so, KW("bstop", L(7, 1)) + 0.3, 0.35, 0.5)
cue(KW("bstop", L(7, 1)) + 0.3, "land-light_1", -18)
captions(s, [(o2 + 0.1, L("A 4-HOUR RANGE", "กรอบสี่ชั่วโมง"), WHITE), (K("dip") - 0.1, L("PRICE DROPS UNDER THE LOW", "ราคาหลุดลงไปใต้โลว์"), WHITE),
             (K("a") - 0.1, L("A: CLOSES BACK INSIDE", "แบบเอ: ปิดกลับเข้ากรอบ"), GREEN), (K("areal") - 0.1, L("STOPS TAKEN, BACK IN THE BOX", "เก็บสต็อปแล้ว กลับเข้ากล่อง"), GREEN),
             (K("b") - 0.1, L("B: CLOSES BELOW THE LOW", "แบบบี: ปิดใต้โลว์"), RED), (K("bfake") - 0.1, L("THAT'S NOT A SWEEP", "นี่ไม่ใช่การกวาด"), RED),
             (K("bstop") - 0.1, L("BUYING IT GETS YOU STOPPED", "ซื้อตรงนี้ โดนสต็อปแทน"), RED)], c2)

# 3  neither side taken: no sweep, no trade
o3, c3 = K("c") - 0.1, K("rule") - 0.1
s = S(o3, c3)
series_tag(s, 2)
frame(s)
ri = candles_clip(s, cI)
reveal(ri, cI, [(o3, -1), (o3 + 0.3, -1), (K("cno") - 0.2, len(INS) - 1)], o3)
for k, (yy, en, th) in enumerate([(y(HI) - 50, "HIGH UNTOUCHED", "ไฮยังไม่ถูกแตะ"), (y(LO) + 60, "LOW UNTOUCHED", "โลว์ยังไม่ถูกแตะ")]):
    u = s.label(560, yy, L(en, th), 26, GREY, 0, 800, 0.12); s.fade(u, K("c") + 0.8 + 0.4 * k)
nt = s.pill(540, 560, L("NO SWEEP = NO TRADE", "ไม่มีกวาด = ไม่มีเทรด"), WHITE, "#0b0b0b", 28); s.pop(nt, K("cno"), 0.4, 0.5); cue(K("cno"), "pop_2", -18)
captions(s, [(o3 + 0.1, L("NEITHER SIDE TAKEN?", "ไม่แตะทั้งสองฝั่ง?"), WHITE), (K("cno") + 1.2, L("WAIT FOR THE NEXT CANDLE", "รอแท่งถัดไป"), GOLD)], c3)

# 4  the rule
o4, c4 = K("rule") - 0.1, K("next") - 0.1
s = S(o4, c4)
series_tag(s, 2)
r0 = s.label(540, 700, L("THE RULE", "กฎข้อเดียว"), 34, GREY, 0, 800, 0.2); s.fade(r0, o4 + 0.1)
r1 = s.label(540, 880, L("NO CLOSE BACK INSIDE", "ไม่ปิดกลับเข้ากรอบ"), 62, WHITE, 0, 800, 0.03); s.pop(r1, K("rule2"), 0.4, 0.6)
r2 = s.label(540, 1000, L("NO CRT", "ก็ไม่ใช่ CRT"), 96, RED, 0, 800, 0.06); s.pop(r2, KW("rule2", L(4, 1)), 0.4, 0.5)
cue(K("rule2"), "bell_C5", -18); cue(KW("rule2", L(4, 1)), "land_1", -18)

# 5  next part
o5, c5 = K("next") - 0.1, K("order") - 0.05
s = S(o5, c5)
nx_ = s.label(540, 760, L("NEXT  ·  PART 3/5", "ตอนต่อไป  ·  ตอนที่ 3/5"), 30, GREY, 0, 700, 0.2); s.fade(nx_, o5 + 0.1)
for k, (en, th, col) in enumerate([("ENTRY", "จุดเข้า", UP), ("STOP", "สต็อป", RED), ("TARGET", "เป้าหมาย", GOLD)]):
    t = o5 + 0.6 + 0.45 * k
    w_ = s.label(540, 900 + 110 * k, L(en, th), 70, col if col != UP else LBLUE, 0, 800, 0.06); s.pop(w_, t, 0.35, 0.6)
    cue(t, f"tick_{k + 1}", -20)
cue(o5 + 0.2, "whoosh-long_1", -22)

outro(K("order") - 0.05)
write()
