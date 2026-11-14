"""OTM CRT series, part 3/5: "Entry, stop, target". English (otm-crt-ep3) and Thai (otm-crt-ep3-th) are built from
this same file; only LANG differs. On the 5-minute chart under a 4-hour range: the sweep of the CRT low and the close
back inside, the shift above the last lower high, the fair value gap it leaves, the entry at the middle of the gap,
the stop under the sweep wick, the target at the CRT high and a partial at the range 50%. Synthetic example chart;
candles up #2962ff, down white. Writes ../index.html, work/cues.json and work/timing.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *

LANG = "th"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = "otm-crt-ep3" + ("-th" if LANG == "th" else "")
TOTAL = init(ROOT, LANG, COMP, "mix_crt3" + ("_th" if LANG == "th" else ""))
def KW(key, n): return W(G["marks"][key] + n)

HI, LO = 78, 30
MID50 = (HI + LO) / 2                                   # 54: the range 50%
LH = 50                                                 # the last lower high (candle 9)
GAP_LO, GAP_HI = 40, 46                                 # candle 14's high .. candle 16's low
ENTRY = (GAP_LO + GAP_HI) / 2                           # 43
SL = 22.5
SW, BRK, FILL = 12, 15, 19
pre = path_candles([(0, 54), (3, 60), (6, 44), (9, LH)], seed=21, noise=1.4, wick=1.4)
mid_ = [(48, 49.4, 45, 46), (46, 46.5, 36, 37), (37, 38, 24, 31.8), (31.8, 36, 31, 35.5), (35.5, GAP_LO, 35, 39.5),
        (39.5, 53, 39, 52), (52, 56, GAP_HI, 55), (55, 56.5, 51, 52), (52, 52.5, 46.5, 47), (47, 48.5, 42.6, 48),
        (48, 52, 47.5, 51.5)]
post = path_candles([(0, 51.5), (2, 56), (4, 52.5), (6, 55.5), (8, 53), (15, 79)], seed=22, noise=1.2, wick=1.4, start=51.5)[1:]
C = pre + mid_ + post
NX = 36
ch = Chart(C, NX, 90, 1000, 560, 1260, 15, 85)
N = len(C)
def y(p): return ch.y(p)
XR = ch.x(NX - 0.5)                                     # right end of the level lines

def lvl(s, p, col, label, op=0, dash="14 10", w=3, i0=0, ly=-14, size=24):
    ln = s.raw(f'<line id="@ID@" x1="{ch.x(i0) - 10:.1f}" y1="{y(p):.1f}" x2="{XR:.1f}" y2="{y(p):.1f}" stroke="{col}" stroke-width="{w}" stroke-dasharray="{dash}" style="opacity:{op}"/>', "lv")
    lb = s.label(XR, y(p) + ly, label, size, col, op, 800, 0.1, "end") if label else None
    return ln, lb

# 1  hook / thumbnail: the finished trade
s = S(0, K("ltf") - 0.15, first=True)
sym_pill(s)
s.label(540, 330, L("THE SWEEP IS REAL.", "เจอการกวาดของจริงแล้ว"), 44, WHITE, 1, 800, 0.04)
s.label(540, 420, L("WHERE DO YOU GET IN?", "จะเข้าตรงไหน?"), 58, GOLD, 1, 800, 0.04)
rbox(s, ch.x(FILL), y(ENTRY), XR, y(HI), GREEN, 0.12, 0, 0, 1)
rbox(s, ch.x(FILL), y(SL), XR, y(ENTRY), RED, 0.12, 0, 0, 1)
for p, col, lab in ((HI, GOLD, L("TARGET · CRT HIGH", "เป้า · ไฮของกรอบ") + "  " + gp(HI)), (LO, GOLD, L("CRT LOW", "โลว์ของกรอบ") + "  " + gp(LO)), (ENTRY, LBLUE, L("ENTRY", "จุดเข้า")), (SL, RED, L("STOP", "สต็อป"))):
    lvl(s, p, col, lab, 1)
rbox(s, ch.x(14), y(GAP_HI), ch.x(22), y(GAP_LO), LBLUE, 0.3, 0.9, 2, 1)
s.raw('<g id="@ID@">' + ch.candles() + "</g>", "cg")
s.pill(ch.x(SW), y(24) + 48, L("SWEEP", "กวาด"), RED, WHITE, 22, 1)
captions(s, [(0.1, L("ENTRY · STOP · TARGET", "จุดเข้า · สต็อป · เป้าหมาย"), WHITE)], K("ltf") - 0.15)
cue(0.3, "whoosh-short_1", -22)

# 2  the walk-through on the 5-minute chart
o2, c2 = K("ltf") - 0.15, K("recap") - 0.1
s = S(o2, c2)
series_tag(s, 3)
tf = s.pill(540, 470, L("XAUUSD  ·  4H RANGE  ·  5M ENTRY", "XAUUSD  ·  กรอบ 4H  ·  เข้าที่ 5M"), WHITE, "#0b0b0b", 26); s.pop(tf, K("ltf") + 0.2, 0.4, 0.5); cue(K("ltf") + 0.2, "whoosh-long_1", -22)
hiL, hiT = lvl(s, HI, GOLD, L("CRT HIGH", "ไฮของกรอบ") + "  " + gp(HI)); loL, loT = lvl(s, LO, GOLD, L("CRT LOW", "โลว์ของกรอบ") + "  " + gp(LO), ly=36)
for i in (hiL, hiT, loL, loT): s.fade(i, K("ltf") + 0.4, 0.5)
pr = rbox(s, ch.x(FILL), y(ENTRY), XR, y(HI), GREEN, 0.12, 0, 0)
rk = rbox(s, ch.x(FILL), y(SL), XR, y(ENTRY), RED, 0.12, 0, 0)
gap = rbox(s, ch.x(14), y(GAP_HI), XR, y(GAP_LO), LBLUE, 0.28, 0.9, 2)
rid = candles_clip(s, ch)
keys = [(o2, -1), (K("ltf") + 0.6, -1), (K("sweep") - 0.2, SW - 1), (KW("sweep", L(3, 1)), SW),
        (K("shift") + 1.2, SW), (K("shift") + 2.6, 16), (K("mid") + 0.6, 16), (K("mid") + 1.8, FILL),
        (K("half") - 0.4, FILL), (K("half") + 1.0, 25), (K("hit") - 1.2, 25), (K("hit") + 0.1, N - 1)]
reveal(rid, ch, keys, o2)
# the sweep and the close back inside
sw = s.pill(ch.x(SW), y(24) + 48, L("SWEEP", "กวาด"), RED, WHITE, 22); s.pop(sw, KW("sweep", L(3, 1)) + 0.1, 0.35, 0.5)
cue(KW("sweep", L(3, 1)), "whoosh-short_2", -20)
cr = ring(s, ch.x(SW), y(31.8), 18, GREEN); s.pop(cr, K("close") + 0.2, 0.35, 0.3); cue(K("close") + 0.2, "click-confirm_1", -18)
ck = s.label(ch.x(SW) + 30, y(29) + 8, L("CLOSED BACK INSIDE", "ปิดกลับเข้ากรอบ"), 22, GREEN, 0, 800, 0.06, "start"); s.fade(ck, K("close") + 0.3)
for i in (cr, ck): out(i, K("shift") - 0.1)
# the shift: the break of the last lower high
lhL = s.raw(f'<line id="@ID@" x1="{ch.x(9):.1f}" y1="{y(LH):.1f}" x2="{ch.x(17):.1f}" y2="{y(LH):.1f}" stroke="#fff" stroke-width="3" stroke-dasharray="8 7" style="opacity:0"/>', "lh")
s.fade(lhL, K("shift") + 0.4, 0.4)
lht = s.label(ch.x(9), y(LH) - 30, L("LAST LOWER HIGH", "โลเวอร์ไฮล่าสุด"), 22, WHITE, 0, 800, 0.06, "middle"); s.fade(lht, K("shift") + 0.5)
bk = s.pill(ch.x(BRK) + 20, y(60) - 6, L("SHIFT", "เปลี่ยนโครงสร้าง"), WHITE, "#0b0b0b", 22); s.pop(bk, K("shift") + 2.2, 0.35, 0.5); cue(K("shift") + 2.2, "pop_1", -18)
for i in (lht, bk): out(i, K("fvg") + 1.6)
out(lhL, K("stop"), 0.3, 0.3)
# the fair value gap and the entry at its middle
s.fade(gap, K("fvg") + 0.3, 0.5); cue(K("fvg") + 0.3, "swell_1", -22)
gl = s.label(XR, y(GAP_HI) - 12, L("FAIR VALUE GAP", "แฟร์แวลูแก็ป"), 22, LBLUE, 0, 800, 0.08, "end"); s.fade(gl, K("fvg") + 0.5)
enL, enT = lvl(s, ENTRY, GOLD, None, 0, "10 7", 3, 14)
s.fade(enL, K("mid") + 0.1, 0.4)
et = s.pill(XR - 110, y(ENTRY) + 2, L("ENTRY · 50%", "จุดเข้า · 50%"), GOLD, "#111", 20); s.pop(et, K("mid") + 0.2, 0.35, 0.5); cue(K("mid") + 0.2, "bell_E5", -20)
fr = ring(s, ch.x(FILL), y(ENTRY), 18, GOLD); s.pop(fr, K("mid") + 1.7, 0.35, 0.3); cue(K("mid") + 1.7, "click_1", -18)
out(gl, K("stop") - 0.1)
# the stop under the sweep wick
slL, slT = lvl(s, SL, RED, L("STOP", "สต็อป"), 0, "10 7", 3, SW - 1, 36)
s.fade(slL, K("stop") + 0.2, 0.4); s.fade(slT, K("stop") + 0.3); cue(K("stop") + 0.2, "tock_1", -18)
s.fade(rk, K("stop") + 0.4, 0.5)
fx = xmark(s, ch.x(SW + 3), y(18.5), 14, RED, 5); s.draw(fx, K("fail") + 0.6, 0.3)
ft = s.label(ch.x(SW + 3) + 26, y(18.5) + 8, L("FAILED", "ล้มเหลว"), 22, RED, 0, 800, 0.06, "start"); s.fade(ft, K("fail") + 0.7)
for i in (fx, ft): out(i, K("target") - 0.1)
# the target at the CRT high; the partial at the range 50%
tg = s.pill(XR - 120, y(HI) - 76, L("TARGET", "เป้าหมาย"), GOLD, "#111", 22); s.pop(tg, K("target") + 0.6, 0.35, 0.5); cue(K("target") + 0.6, "bell_G5", -20)
s.fade(pr, K("target") + 0.7, 0.5)
hfL, hfT = lvl(s, MID50, GREY, L("RANGE 50%", "50% ของกรอบ"), 0, "6 8", 2)
s.fade(hfL, K("half") + 0.1, 0.4); s.fade(hfT, K("half") + 0.2)
pp = s.pill(ch.x(25) + 10, y(MID50) - 40, L("PARTIAL", "ปิดบางส่วน"), WHITE, "#0b0b0b", 20); s.pop(pp, K("part") + 0.3, 0.35, 0.5); cue(K("part") + 0.3, "pop_2", -18)
th = s.pill(ch.x(N - 1) - 120, y(HI) + 44, L("TARGET HIT", "ถึงเป้า"), GREEN, "#0b0b0b", 24); s.pop(th, K("hit") + 0.15, 0.4, 0.5); cue(K("hit") + 0.15, "click-confirm_1", -16)
out(tg, K("hit"))
captions(s, [(o2 + 0.1, L("DROP FROM THE 4H RANGE TO THE 5M", "ลงจากกรอบ 4H ไปกราฟ 5M"), WHITE),
             (K("sweep") - 0.1, L("THE WICK UNDER THE CRT LOW", "ไส้เทียนหลุดใต้โลว์ของกรอบ"), RED),
             (K("close") - 0.1, L("AND THE CLOSE BACK INSIDE", "แล้วปิดกลับเข้ามา"), GREEN),
             (K("shift") - 0.1, L("WAIT FOR THE SHIFT", "รอการเปลี่ยนโครงสร้าง"), WHITE),
             (K("fvg") - 0.1, L("THE PUSH LEAVES A FAIR VALUE GAP", "แรงดันทิ้งแฟร์แวลูแก็ปไว้"), LBLUE),
             (K("mid") - 0.1, L("ENTRY: THE MIDDLE OF THE GAP", "จุดเข้า: กึ่งกลางแก็ป"), GOLD),
             (K("stop") - 0.1, L("STOP: BELOW THE SWEEP WICK", "สต็อป: ใต้ไส้ที่กวาดโลว์"), RED),
             (K("fail") - 0.1, L("BACK UNDER IT = SWEEP FAILED", "กลับลงไปใต้ไส้ = กวาดล้มเหลว"), RED),
             (K("target") - 0.1, L("TARGET: THE CRT HIGH", "เป้าหมาย: ไฮของกรอบ"), GOLD),
             (K("half") - 0.1, L("PARTIAL AT THE RANGE 50%", "ปิดบางส่วนที่ 50% ของกรอบ"), WHITE),
             (K("hit") - 0.1, L("TARGET HIT", "ถึงเป้า"), GREEN)], c2)

# 3  recap: sweep, shift, gap, entry
o3, c3 = K("recap") - 0.1, K("next") - 0.1
s = S(o3, c3)
series_tag(s, 3)
for k, (en, th, col) in enumerate([("SWEEP", "กวาด", RED), ("SHIFT", "เปลี่ยนโครงสร้าง", WHITE), ("GAP", "แก็ป", LBLUE), ("ENTRY", "จุดเข้า", GOLD)]):
    t = KW("recap", k)
    w_ = s.label(540, 720 + 150 * k, L(en, th), 72, col, 0, 800, 0.06); s.pop(w_, t, 0.35, 0.6)
    cue(t, ["tick-crisp_1", "tick-crisp_2", "tick-crisp_3", "tick-crisp_1"][k], -16)
    if k:
        yy = 720 + 150 * k - 96
        a_ = s.path(f"M 522 {yy} L 540 {yy + 16} L 558 {yy}", GREY, 4, drawn=True, style="opacity:0"); s.fade(a_, t - 0.1, 0.2)

# 4  next part
o4, c4 = K("next") - 0.1, K("order") - 0.05
s = S(o4, c4)
nx_ = s.label(540, 760, L("NEXT  ·  PART 4/5", "ตอนต่อไป  ·  ตอนที่ 4/5"), 30, GREY, 0, 700, 0.2); s.fade(nx_, o4 + 0.1)
a_ = s.label(540, 900, L("TIMEFRAME", "จับคู่"), 76, GOLD, 0, 800, 0.04); s.pop(a_, o4 + 0.6, 0.4, 0.6)
b_ = s.label(540, 1000, L("PAIRS", "ไทม์เฟรม"), 76, WHITE, 0, 800, 0.04); s.pop(b_, o4 + 0.9, 0.4, 0.6)
cue(o4 + 0.2, "whoosh-long_1", -22)

outro(K("order") - 0.05)
write()
