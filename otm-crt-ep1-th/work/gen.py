"""OTM CRT series, part 1/5: "What is CRT". English (otm-crt-ep1) and Thai (otm-crt-ep1-th) are built from this same
file; only LANG differs. One higher-timeframe candle sets a range (the CRT high and low, buy stops above, sell stops
below); the next candles sweep one side, close back inside and deliver to the other side, fuelled by the trapped
breakdown sellers' stops. Range, sweep, delivery. Synthetic example chart; candles up #2962ff, down white.
Writes ../index.html, work/cues.json and work/timing.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *

LANG = "th"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = "otm-crt-ep1" + ("-th" if LANG == "th" else "")
TOTAL = init(ROOT, LANG, COMP, "mix_crt1" + ("_th" if LANG == "th" else ""))
def KW(key, n): return W(G["marks"][key] + n)        # start of the n-th token after a mark

# ---- the example: a 4H range, then 5-minute candles that sweep the low, close back inside and run to the high
HI, LO = 75, 30
ch = Chart(path_candles([(0, 44), (3, 50), (7, 38), (9, 42), (12, 24), (15, 40), (18, 35), (24, 56), (27, 50), (36, 74),
                         (38, 76.5), (40, 72)], seed=5, noise=1.6, wick=1.5),
           nx=42, x0=250, x1=1000, top=560, bot=1260, pmin=15, pmax=85)
ch.c[10] = (41, 41.6, 35.5, 36); ch.c[11] = (36, 36.6, 31, 31.4)
ch.c[12] = (31.4, 33.6, 24, 33.2)                    # the sweep: wick under the low, close back inside
ch.c[13] = (33.2, 37.8, 32.6, 37.4)
SW = 12
N = len(ch.c)
HX, HW = 165, 84                                      # the higher-timeframe candle
BX0, BX1 = 115, 1010                                  # the range box
def y(p): return ch.y(p)

def range_box(s, op=0):
    return rbox(s, BX0, y(HI), BX1, y(LO), GOLD, 0.07, 0.0, 0, op)

def htf(s, op=1):
    return big_candle(s, HX, HW, y(HI), y(HI - 3), y(LO + 3), y(LO), op)

# 1  thumbnail / hook: the whole picture
s = S(0, K("hl") - 0.15, first=True)
s.label(540, 330, L("CANDLE RANGE THEORY", "CANDLE RANGE THEORY"), 46, WHITE, 1, 800, 0.06)
s.label(540, 430, "CRT", 96, GOLD, 1, 800, 0.12)
range_box(s, 1)
hline(s, ch, HI, BX0, N + 0.5, GOLD, 3, "14 10", 1); hline(s, ch, LO, BX0, N + 0.5, GOLD, 3, "14 10", 1)
htf(s)
s.raw('<g id="@ID@">' + ch.candles() + "</g>", "cg")
s.pill(ch.x(SW), y(24) + 52, L("SWEEP", "กวาด"), RED, WHITE, 24, 1)
show = arrow(s, ch.x(SW) + 30, y(24), ch.x(38) - 20, y(HI) + 12, GOLD, 5); s.draw(show[0], 0.4, 0.8); s.pop(show[1], 1.15, 0.2)
captions(s, [(0.1, L("ONE CANDLE CAN MAP THE NEXT MOVE", "แท่งเดียว บอกทางไปต่อของราคา"), WHITE)], K("hl") - 0.15)
cue(0.4, "whoosh-short_1", -22)

# 2  the build
o2, c2 = K("hl") - 0.15, K("recap") - 0.1
s = S(o2, c2)
series_tag(s, 1)
# step pills
steps = []
for k, (x, en, th, key) in enumerate([(220, "1 RANGE", "1 กรอบ", "p1"), (540, "2 SWEEP", "2 กวาด", "p2"), (860, "3 DELIVERY", "3 ส่งราคา", "p3")]):
    p = s.pill(x, 470, L(en, th), GOLD, "#111", 26); s.pop(p, K(key), 0.4, 0.5); cue(K(key), "pop_" + str(k + 1), -18)
    steps.append(p)
for k in range(2): out(steps[k], [K("p2"), K("p3")][k], 0.3, 0.4)
# the higher-timeframe candle, its high and low
bc = htf(s, 0); s.pop(bc, K("hl"), 0.5, 0.3, "50% 50%"); cue(K("hl"), "swell_1", -22)
tf = s.label(HX, y(HI) - 22, L("4H", "4H"), 26, GREY, 0, 800, 0.1); s.fade(tf, K("hl") + 0.2)
lh = s.label(HX + 60, y(HI) + 9, L("HIGH", "ไฮ"), 26, WHITE, 0, 800, 0.1, "start"); s.fade(lh, KW("hl", L(4, 1)))
ll = s.label(HX + 60, y(LO) + 9, L("LOW", "โลว์"), 26, WHITE, 0, 800, 0.1, "start"); s.fade(ll, KW("hl", L(7, 2)))
for i in (lh, ll): out(i, K("box") + 0.3)
# the range box
lhi = s.raw(f'<line id="@ID@" x1="{BX0}" y1="{y(HI)}" x2="{BX0}" y2="{y(HI)}" stroke="{GOLD}" stroke-width="3" stroke-dasharray="14 10"/>', "ln")
llo = s.raw(f'<line id="@ID@" x1="{BX0}" y1="{y(LO)}" x2="{BX0}" y2="{y(LO)}" stroke="{GOLD}" stroke-width="3" stroke-dasharray="14 10"/>', "ln")
for i in (lhi, llo):
    tl(f'tl.to("#{i}", {{attr: {{x2: {BX1}}}, duration: 0.8, ease: "power2.out"}}, {K("box"):.3f});')
bx = range_box(s); s.fade(bx, K("box") + 0.3, 0.6); cue(K("box"), "whoosh-short_2", -22)
chh = s.label(BX1 - 6, y(HI) - 14, L("CRT HIGH", "ไฮของกรอบ"), 26, GOLD, 0, 800, 0.12, "end"); s.fade(chh, K("box") + 0.6)
chl = s.label(BX1 - 6, y(LO) + 36, L("CRT LOW", "โลว์ของกรอบ"), 26, GOLD, 0, 800, 0.12, "end"); s.fade(chl, K("box") + 0.8)
# stops above and below
up_chips = stop_chips(s, [480, 590, 700, 810], y(HI) - 34, RED, L("STOP", "STOP"), 18)
dn_chips = stop_chips(s, [330, 440, 550, 660], y(LO) + 30, RED, L("STOP", "STOP"), 18)
for k, i in enumerate(up_chips): s.pop(i, K("liq") + 0.12 * k, 0.3, 0.4);
for k, i in enumerate(dn_chips): s.pop(i, K("liq2") + 0.12 * k, 0.3, 0.4)
cue(K("liq"), "tick_1", -20); cue(K("liq2"), "tick_2", -20)
bsl = s.label(645, y(HI) - 78, L("BUY STOPS", "สต็อปฝั่งขาย"), 26, WHITE, 0, 800, 0.12); s.fade(bsl, K("liq"))
ssl = s.label(495, y(LO) + 92, L("SELL STOPS", "สต็อปฝั่งซื้อ"), 26, WHITE, 0, 800, 0.12); s.fade(ssl, K("liq2"))
out(chh, K("liq") - 0.1); out(chl, K("liq2") - 0.1)
for i in (bsl, ssl): out(i, K("p2") + 0.4)
# the 5-minute candles: sweep, close back inside, delivery
rid = candles_clip(s, ch)
keys = [(o2, -1), (K("p2") + 0.3, -1), (K("take") + 0.1, SW - 1), (K("take") + 0.5, SW),
        (K("p3") + 0.6, SW), (K("p3") + 1.4, 15), (K("run"), 15), (K("why") - 0.2, 26),
        (K("fuel") + 0.5, 26), (K("target") - 0.2, 33), (K("target") + 0.9, N - 1)]
reveal(rid, ch, keys, o2)
ltf = s.label(ch.x(1), y(HI) - 24, L("5M", "5M"), 24, GREY, 0, 800, 0.1); s.fade(ltf, K("p2") + 0.3)
for k, i in enumerate(dn_chips):                     # the sweep takes the stops under the low
    tl(f'tl.to("#{i}", {{opacity: 0, y: 30, duration: 0.35, ease: "power2.in"}}, {K("take") + 0.45 + 0.08 * k:.3f});')
cue(K("take") + 0.45, "whoosh-short_1", -20)
swp = s.pill(ch.x(SW), y(24) + 52, L("SWEEP", "กวาด"), RED, WHITE, 24); s.pop(swp, K("take") + 0.5, 0.35, 0.5)
rg = ring(s, ch.x(SW), y(33.2), 20, GOLD); s.pop(rg, K("p3") + 0.5, 0.35, 0.3); cue(K("p3") + 0.5, "click-confirm_1", -18)
cbi = s.label(ch.x(SW) + 34, y(40), L("CLOSED BACK INSIDE", "ปิดกลับเข้ากรอบ"), 24, GOLD, 0, 800, 0.08, "start"); s.fade(cbi, K("p3") + 0.6)
out(cbi, K("run") - 0.1); out(rg, K("run") - 0.1)
dl = arrow(s, ch.x(SW) + 26, y(28), ch.x(36), y(HI) - 4, GOLD, 4, 18); show_arrow(s, dl, K("run"), 0.7); cue(K("run"), "swell_2", -20)
for i in dl: out(i, K("why") - 0.1, 0.3, 0.25)
# why: trapped breakdown sellers; their stops are buy orders; up to the untouched highs
TX = [ch.x(SW) - 95, ch.x(SW), ch.x(SW) + 95]
trap = stop_chips(s, TX, y(19.5), "#5b6270", L("SELL", "SELL"), 18)
for k, i in enumerate(trap): s.pop(i, K("why") + 1.0 + 0.15 * k, 0.3, 0.4)
cue(K("why") + 1.0, "tock_1", -18)
for k, i in enumerate(trap):
    tl(f'tl.to("#{i} rect", {{attr: {{fill: "{UP}"}}, duration: 0.3}}, {K("fuel") + 0.3 + 0.1 * k:.3f});')
fa = [arrow(s, x, y(22.3), x, y(28.5), UP, 4, 14) for x in TX]
out(swp, K("why") + 0.6)
for k, a in enumerate(fa): show_arrow(s, a, K("fuel") + 0.8 + 0.12 * k, 0.4)
cue(K("fuel") + 0.8, "pop_3", -20)
for k, i in enumerate(up_chips):                     # the highs get taken at the end
    tl(f'tl.to("#{i}", {{opacity: 0, y: -30, duration: 0.35, ease: "power2.in"}}, {K("target") + 0.7 + 0.08 * k:.3f});')
uh = rbox(s, 440, y(HI) - 58, 850, y(HI) - 10, GOLD, 0.12, 1, 3)
s.fade(uh, K("target"), 0.3); out(uh, K("target") + 1.0, 0.4)
cue(K("target") + 0.7, "bell_E5", -20)
captions(s, [(o2 + 0.1, L("EVERY CANDLE HAS A HIGH AND A LOW", "ทุกแท่งมีไฮ และโลว์"), WHITE),
             (K("box") - 0.1, L("CRT TREATS THAT RANGE LIKE A BOX", "ซีอาร์ที มองกรอบนี้เป็นกล่อง"), GOLD),
             (K("p1") - 0.1, L("A HIGHER-TIMEFRAME CANDLE SETS IT", "แท่งไทม์เฟรมใหญ่ กำหนดกรอบ"), WHITE),
             (K("liq") - 0.1, L("STOPS SIT ABOVE AND BELOW", "สต็อปรออยู่ทั้งบน และล่าง"), WHITE),
             (K("p2") - 0.1, L("THE NEXT CANDLES RUN ONE SIDE", "แท่งถัดไปวิ่งทะลุไปด้านหนึ่ง"), RED),
             (K("take") - 0.1, L("AND TAKE THOSE STOPS", "แล้วเก็บสต็อปไป"), RED),
             (K("p3") - 0.1, L("CLOSE BACK INSIDE THE BOX", "ปิดกลับเข้ามาในกล่อง"), GOLD),
             (K("run") - 0.1, L("THEN TRAVEL TO THE OTHER SIDE", "แล้ววิ่งไปอีกฝั่ง"), GOLD),
             (K("why") - 0.1, L("BREAKDOWN SELLERS ARE TRAPPED", "คนขายตามการหลุดกรอบ ติดอยู่ใต้กรอบ"), RED),
             (K("fuel") - 0.1, L("THEIR STOPS PUSH PRICE UP", "สต็อปของพวกเขา ดันราคาขึ้น"), LBLUE),
             (K("target") - 0.1, L("TOWARD THE UNTOUCHED HIGHS", "ไปหาไฮที่ยังไม่มีใครแตะ"), GOLD)], c2)

# 3  recap: range, sweep, delivery
o3, c3 = K("recap") - 0.1, K("next") - 0.1
s = S(o3, c3)
series_tag(s, 1)
for k, (en, th, col) in enumerate([("RANGE", "กรอบ", WHITE), ("SWEEP", "กวาด", RED), ("DELIVERY", "ส่งราคา", GOLD)]):
    t = KW("recap", k)
    yy = 760 + 170 * k
    n = s.label(300, yy, str(k + 1), 92, col, 0, 800, 0)
    w_ = s.label(380, yy - 4, L(en, th), 70, col, 0, 800, 0.06, "start")
    s.pop(n, t, 0.35, 0.4); s.fade(w_, t + 0.05, 0.35); cue(t, ["tick-crisp_1", "tick-crisp_2", "tick-crisp_3"][k], -16)

# 4  next part
o4, c4 = K("next") - 0.1, K("order") - 0.05
s = S(o4, c4)
nx_ = s.label(540, 760, L("NEXT  ·  PART 2/5", "ตอนต่อไป  ·  ตอนที่ 2/5"), 30, GREY, 0, 700, 0.2); s.fade(nx_, o4 + 0.1)
a_ = s.label(540, 900, L("REAL SWEEP", "กวาดของจริง"), 68, GREEN, 0, 800, 0.04); s.pop(a_, KW("next", L(5, 1)), 0.4, 0.6)
v_ = s.label(540, 990, "VS", 40, GREY, 0, 800, 0.1); s.fade(v_, KW("next", L(7, 2)) - 0.3)
b_ = s.label(540, 1090, L("FAKE SWEEP", "กวาดของปลอม"), 68, RED, 0, 800, 0.04); s.pop(b_, KW("next", L(9, 2)), 0.4, 0.6)
cue(o4 + 0.2, "whoosh-long_1", -22)

outro(K("order") - 0.05)
write()
