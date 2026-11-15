"""Scenes for MSNR PRO (msnr-pro-ep1..ep7; Thai: msnr-pro-epN-th, same file with LANG = "th").
A 7-part follow-up to the MSNR series: strong A & V, the 50% wick, the fresh flip, the refinement ladder, the storyline
road map, the 2-timeframes-lower entry model and trendline confirmation. Original drawings and synthetic XAUUSD charts
(candles up #2962ff, down white). Thai visuals keep the trading term names in English."""
from otm import *
from msnr import nx, ny, title_block
from story import FW, rows, panel, mini, seg_path, lvl, pos_box, next_card

TOT = 7
NEXT = {1: ("THE 50% WICK", "THE 50% WICK"), 2: ("THE FRESH FLIP", "THE FRESH FLIP"), 3: ("REFINEMENT LADDER", "REFINEMENT LADDER"),
        4: ("STORYLINE ROAD MAP", "STORYLINE ROAD MAP"), 5: ("THE ENTRY MODEL", "THE ENTRY MODEL"), 6: ("TRENDLINES", "TRENDLINES")}


def tagp(s, n):
    return s.label(540, 300, f"MSNR PRO  ·  {n}/{TOT}", 26, GOLD, 1, 700, 0.2)


def pos_short(s, x0, x1, y_entry, y_tp, y_sl, t):
    """a short position: blue target box below, grey stop box above"""
    tp = rbox(s, x0, y_entry, x1, y_tp, UP, 0.28, 0.0, 0); sl = rbox(s, x0, y_sl, x1, y_entry, GREY, 0.35, 0.0, 0)
    s.fade(tp, t, 0.4); s.fade(sl, t, 0.4)
    return tp, sl


def hl(s, x0, x1, y, col, w=3, dash="", op=0):
    return s.raw(f'<line id="@ID@" x1="{x0:.1f}" y1="{y:.1f}" x2="{x1:.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="{w}" '
                 + (f'stroke-dasharray="{dash}" ' if dash else "") + f'style="opacity:{op}"/>', "hl")


def pair(s, cx, kind, t, w=56, gap=46, label=None, lcol=GREY, scale=1.0, y0=0):
    """two candles of a Classic A: bullish first candle, then the second candle (weak / strong / sweep)"""
    k = scale
    def Y(v): return y0 + v * k
    a = big_candle(s, cx - gap, w, Y(740), Y(1000), Y(780), Y(1030), 0, UP, False)
    hi2, cl2, lo2 = {"weak": (770, 830, 850), "strong": (770, 1030, 1060), "sweep": (690, 1030, 1060)}[kind]
    b = big_candle(s, cx + gap, w, Y(hi2), Y(780), Y(cl2), Y(lo2), 0, DOWN, False)
    s.fade(a, t, 0.3); s.fade(b, t + 0.25, 0.3)
    out_ = [a, b]
    if label:
        lb = s.label(cx, Y(1130), label, 28, lcol, 0, 800, 0.08); s.fade(lb, t + 0.4); out_.append(lb)
    return out_


# ======================================================================================================== 1  strong A & V
def ep1():
    o1, c1 = 0, K("body") - 0.1
    s = S(o1, c1, first=True)
    tagp(s, 1)
    title_block(s, "STRONG A & V", L("NOT EVERY LEVEL IS EQUAL", "ไม่ใช่ทุกระดับที่เท่ากัน"))
    pair(s, 330, "weak", 0.7, label="WEAK", lcol=GREY, scale=0.75, y0=170)
    pair(s, 750, "strong", FW("hook", "strong", "แข็งแรง", 2.4), label="STRONG", lcol=GOLD, scale=0.75, y0=170)
    captions(s, [(0.1, L("STRONG OR WEAK?", "แข็งแรง หรือ อ่อน?"), WHITE)], c1)

    o2, c2 = K("body") - 0.1, K("strong") - 0.1
    s = S(o2, c2)
    tagp(s, 1)
    hd = s.pill(540, 470, L("THE BODY-CLOSE RULE", "กฎ BODY CLOSE"), WHITE, "#0b0b0b", 28); s.pop(hd, o2 + 0.2, 0.4, 0.5)
    a = big_candle(s, 440, 110, 640, 1080, 820, 1120, 0, UP); s.fade(a, o2 + 0.3, 0.3)
    b = big_candle(s, 640, 110, 600, 820, 1100, 1150, 0, DOWN); s.fade(b, o2 + 0.5, 0.3)
    xw = xmark(s, 640, 625, 24, RED, 6); s.draw(xw, o2 + 1.0, 0.35)
    wt = s.label(720, 632, L("WICKS DON'T MATTER", "WICK ไม่สำคัญ"), 26, RED, 0, 800, 0.06, "start"); s.fade(wt, o2 + 1.1)
    t_lv = FW("body", "close", "ราคาปิด", 2.6)
    ln = hl(s, 200, 990, 820, GOLD, 5); s.fade(ln, t_lv, 0.4)
    r = ring(s, 440, 820, 20, GOLD); s.pop(r, t_lv, 0.35, 0.3)
    lt = s.label(540, 1190, L("LEVEL = BODY CLOSE OF CANDLE 1", "LEVEL = CLOSE ของแท่งแรก"), 30, GOLD, 0, 800, 0.06); s.fade(lt, t_lv + 0.2)
    cue(t_lv, "bell_C5", -22)
    gp = s.pill(540, 1268, L("GAP ON CANDLE 2?  THE LEVEL STAYS", "แท่งที่ 2 เปิดแก๊ป?  ระดับไม่เปลี่ยน"), LBLUE, "#111", 26); s.pop(gp, K("gap") + 0.3, 0.4, 0.5)
    captions(s, [(o2 + 0.1, L("BODY CLOSE ONLY", "ใช้ราคาปิดของเนื้อเทียน"), GOLD), (K("gap") - 0.1, L("THE LEVEL NEVER MOVES", "ระดับไม่ขยับ"), LBLUE)], c2, 1352)

    o3, c3 = K("strong") - 0.1, K("ex") - 0.1
    s = S(o3, c3)
    tagp(s, 1)
    pair(s, 200, "weak", o3 + 0.2, label="WEAK", lcol=GREY, scale=1.0, y0=-60)
    pair(s, 540, "strong", o3 + 0.9, label="STRONG", lcol=WHITE, scale=1.0, y0=-60)
    pair(s, 880, "sweep", K("sweep"), label="STRONGEST", lcol=GOLD, scale=1.0, y0=-60)
    eb = rbox(s, 540 + 46 - 36, -60 + 770, 540 + 46 + 36, -60 + 1040, GOLD, 0.0, 1, 3, 0, "8 6"); s.fade(eb, o3 + 1.6, 0.3)
    rs = ring(s, 880 + 46, -60 + 690, 18, RED); s.pop(rs, K("sweep") + 0.8, 0.35, 0.3)
    st = s.label(880 + 46, -60 + 690 - 28, "SWEEP", 24, RED, 0, 800, 0.08); s.fade(st, K("sweep") + 0.9)
    cue(K("sweep") + 0.8, "bell_E5", -22)
    vv = s.pill(540, 1250, L("CLASSIC V  =  THE MIRROR", "CLASSIC V  =  กลับด้าน"), WHITE, "#111", 28); s.pop(vv, K("v") + 0.2, 0.4, 0.5)
    captions(s, [(o3 + 0.1, L("CLOSES BELOW THE FIRST OPEN", "ปิดต่ำกว่า OPEN ของแท่งแรก"), WHITE), (K("sweep") - 0.1, L("SWEEP THE HIGH, THEN CLOSE DOWN", "SWEEP ไฮ แล้วปิดลง"), GOLD),
                 (K("v") - 0.1, L("V: CLOSES ABOVE THE FIRST OPEN", "V: ปิดเหนือ OPEN ของแท่งแรก"), WHITE)], c3, 1352)

    o4, c4 = K("ex") - 0.1, K("next") - 0.1
    s = S(o4, c4)
    tagp(s, 1)
    hp = s.pill(540, 470, "XAUUSD  ·  4H", WHITE, "#0b0b0b", 26); s.pop(hp, o4 + 0.2, 0.4, 0.5)
    C = path_candles([(0, 30), (3, 50), (5, 68), (6, 71), (10, 45), (14, 68.3), (18, 40), (21, 59), (22, 60.5), (24, 57), (28, 82)], seed=21, noise=1.2, wick=1.2)
    C[5] = (60, 69, 59, 68); C[6] = (68, 71, 51, 52)
    C[21] = (54, 59.5, 53, 59); C[22] = (59, 60.5, 57.6, 58.2)
    ch = Chart(C, 31, 80, 1000, 600, 1230, 20, 90, 0.64)
    rid = candles_clip(s, ch)
    t2 = K("ex2")
    reveal(rid, ch, [(o4, -1), (o4 + 0.2, 7), (K("ex") + 0.6, 7), (K("ex") + 2.2, 16), (t2 - 0.1, 16), (t2 + 0.6, 22), (t2 + 2.4, 28)], o4)
    l1 = hl(s, ch.x(5), ch.x(17), ch.y(68), GOLD, 4); s.fade(l1, o4 + 0.6, 0.35)
    t1_ = s.label(ch.x(0) - 30, ch.y(68) - 14, L("STRONG A · HELD", "STRONG A · ยืนได้"), 22, GOLD, 0, 800, 0.06, "start"); s.fade(t1_, o4 + 0.8)
    rr = ring(s, ch.x(14), ch.y(68.3), 18, GOLD); s.pop(rr, K("ex") + 2.0, 0.35, 0.3)
    l2 = hl(s, ch.x(21), ch.x(30), ch.y(59), GREY, 3, "10 8"); s.fade(l2, t2 + 0.6, 0.35)
    t2_ = s.label(ch.x(30), ch.y(59) + 62, L("WEAK A · BROKEN", "WEAK A · โดนเบรก"), 22, GREY, 0, 800, 0.06, "end"); s.fade(t2_, t2 + 0.8)
    xb = xmark(s, ch.x(25), ch.y(59), 14, RED, 5); s.draw(xb, t2 + 1.6, 0.3)
    cue(K("ex") + 2.0, "bell_C5", -22)
    captions(s, [(o4 + 0.1, L("THE STRONG A HOLDS", "STRONG A ยืนได้"), GOLD), (t2 - 0.1, L("THE WEAK A BREAKS", "WEAK A โดนเบรก"), RED)], c4)
    next_card(K("next") - 0.1, G["TOTAL"], 2, *NEXT[1], TOT)


# ======================================================================================================== 2  the 50% wick
def ep2():
    o1, c1 = 0, K("problem") - 0.1
    s = S(o1, c1, first=True)
    tagp(s, 2)
    title_block(s, "THE 50% WICK", L("TIGHTER STOP  ·  BETTER R:R", "SL แคบลง  ·  R:R ดีขึ้น"))
    c_ = big_candle(s, 540, 100, 640, 900, 1080, 1120, 0, DOWN); s.pop(c_, 0.6, 0.4, 0.6)
    captions(s, [(0.1, L("A LONG WICK, A WIDE STOP", "WICK ยาว SL ก็กว้าง"), WHITE)], c1)

    o2, c2 = K("problem") - 0.1, K("ex") - 0.1
    s = S(o2, c2)
    tagp(s, 2)
    a = big_candle(s, 430, 100, 880, 1120, 900, 1150, 0, UP); s.fade(a, o2 + 0.2, 0.3)
    b = big_candle(s, 590, 100, 600, 900, 1090, 1120, 0, DOWN); s.fade(b, o2 + 0.4, 0.3)
    lv = hl(s, 300, 990, 900, GOLD, 5); s.fade(lv, o2 + 0.6, 0.3)
    lt = s.label(990, 940, L("A LEVEL · ENTRY", "A LEVEL · ENTRY"), 26, GOLD, 0, 800, 0.06, "end"); s.fade(lt, o2 + 0.7)
    sf = hl(s, 300, 990, 580, RED, 4, "12 8"); s.fade(sf, o2 + 0.9, 0.3)
    sft = s.label(990, 566, L("SL · FULL WICK", "SL · WICK เต็ม"), 26, RED, 0, 800, 0.06, "end"); s.fade(sft, o2 + 1.0)
    br = s.path("M 680 600 L 700 600 L 700 900 L 680 900", WHITE, 3); s.draw(br, K("rule") + 0.2, 0.5)
    mid = hl(s, 540, 990, 750, GOLD, 4, "10 6"); s.fade(mid, K("rule") + 0.8, 0.3)
    mt = s.label(990, 736, "50%", 30, GOLD, 0, 800, 0.06, "end"); s.fade(mt, K("rule") + 0.9)
    cue(K("rule") + 0.8, "bell_C5", -22)
    out(sf, K("use") + 0.4, 0.4, 0.2); out(sft, K("use") + 0.4, 0.4, 0.2)
    s5 = hl(s, 300, 990, 728, RED, 4); s.fade(s5, K("use") + 0.6, 0.3)
    s5t = s.label(110, 714, L("SL · JUST BEYOND 50%", "SL · เลย 50% นิดเดียว"), 26, RED, 0, 800, 0.06, "start"); s.fade(s5t, K("use") + 0.7)
    cue(K("use") + 0.6, "bell_E5", -22)
    captions(s, [(o2 + 0.1, L("STOP BEYOND THE TIP: TOO WIDE", "SL เลยปลายไส้: กว้างเกินไป"), RED), (K("rule") - 0.1, L("MARK THE 50% OF THE WICK", "มาร์ค 50% ของ WICK"), GOLD),
                 (K("use") - 0.1, L("SAME ENTRY, STOP BEYOND THE 50%", "ENTRY เดิม SL เลย 50%"), WHITE)], c2)

    o3, c3 = K("ex") - 0.1, K("next") - 0.1
    s = S(o3, c3)
    tagp(s, 2)
    hp = s.pill(540, 470, "XAUUSD  ·  1H", WHITE, "#0b0b0b", 26); s.pop(hp, o3 + 0.2, 0.4, 0.5)
    C = path_candles([(0, 30), (5, 62), (6, 80), (10, 45), (15, 70.6), (21, 26), (23, 30)], seed=23, noise=1.2, wick=1.2)
    C[5] = (55, 63, 54, 62); C[6] = (62, 80, 55, 56)
    ch = Chart(C, 26, 80, 1000, 600, 1230, 15, 90, 0.64)
    rid = candles_clip(s, ch)
    reveal(rid, ch, [(o3, -1), (o3 + 0.2, 7), (FW("ex", "came", "กลับ", 2.0) - 0.1, 7), (FW("ex", "came", "กลับ", 2.0) + 1.4, 15), (K("rr") - 0.2, 15), (K("rr") + 1.6, 21)], o3)
    lvl(s, ch, 62, 5, 25, GOLD, L("A LEVEL", "A LEVEL"), o3 + 0.6, 4, "", False, 22)
    lvl(s, ch, 71, 6, 25, GOLD, "50%", o3 + 1.2, 3, "10 6", True, 22)
    r = ring(s, ch.x(15), ch.y(70.6), 18, GOLD); s.pop(r, FW("ex", "came", "กลับ", 2.0) + 1.4, 0.35, 0.3)
    pos_short(s, ch.x(15), ch.x(23), ch.y(62), ch.y(26), ch.y(72), K("rr"))
    p1 = s.pill(300, 1300, L("FULL WICK  1 : 1.9", "WICK เต็ม  1 : 1.9"), "#2a2a2a", GREY, 26, 0, False); s.pop(p1, K("rr") + 0.4, 0.35, 0.5)
    p2 = s.pill(780, 1300, L("50% WICK  1 : 3.6", "50% WICK  1 : 3.6"), GOLD, "#111", 26); s.pop(p2, FW("rr", "almost", "เกือบ", 3.0), 0.35, 0.5)
    cue(FW("rr", "almost", "เกือบ", 3.0), "bell_A4", -20)
    captions(s, [(o3 + 0.1, L("THE RETEST TAPS THE 50%", "RETEST แตะ 50%"), GOLD)], K("rr") + 0.2)
    next_card(K("next") - 0.1, G["TOTAL"], 3, *NEXT[2], TOT)


# ======================================================================================================== 3  the fresh flip
def ep3():
    o1, c1 = 0, K("clean") - 0.1
    s = S(o1, c1, first=True)
    tagp(s, 3)
    title_block(s, "THE FRESH FLIP", L("BROKEN IS NOT DEAD", "เบรกแล้ว ไม่ได้แปลว่าจบ"))
    ln = hl(s, nx(0.05), nx(1), ny(0.5), GOLD, 5, "16 10"); s.fade(ln, 0.5, 0.4)
    captions(s, [(0.1, L("A BROKEN LEVEL CAN STILL WORK", "ระดับที่โดนเบรก ยังใช้ได้"), WHITE)], c1)

    o2, c2 = K("clean") - 0.1, K("touch") - 0.1
    s = S(o2, c2)
    tagp(s, 3)
    s.label(540, 470, L("CLEAN BREAK", "เบรกแบบไม่แตะ"), 46, WHITE, 1, 800, 0.04)
    ln = hl(s, nx(0.05), nx(1), ny(0.5), GOLD, 5, "16 10", 1)
    lb = s.label(nx(1), ny(0.5) - 16, "KEY LEVEL", 24, GOLD, 1, 800, 0.08, "end")
    p1 = seg_path(s, [(0, 0.88), (0.12, 0.5), (0.25, 0.78), (0.4, 0.66), (0.55, 0.22)], WHITE, 6); s.draw(p1, o2 + 0.3, 1.4)
    r = ring(s, nx(0.455), ny(0.5), 18, LBLUE); s.pop(r, o2 + 1.5, 0.35, 0.3)
    nt = s.pill(nx(0.62), ny(0.62), L("NO TOUCH", "ไม่แตะ"), LBLUE, "#111", 22); s.pop(nt, o2 + 1.6, 0.35, 0.5)
    p2 = seg_path(s, [(0.55, 0.22), (0.68, 0.48), (0.85, 0.08)], RED, 6); s.draw(p2, K("flip") + 0.2, 1.0)
    r2 = ring(s, nx(0.68), ny(0.49), 18, GOLD); s.pop(r2, K("flip") + 0.8, 0.35, 0.3)
    fr = s.pill(nx(0.8), ny(0.36), L("STILL FRESH", "ยัง FRESH"), GOLD, "#111", 24); s.pop(fr, K("flip") + 1.0, 0.35, 0.5)
    sb = s.label(540, 1240, L("SUPPORT BECOMES RESISTANCE", "SUPPORT กลายเป็น RESISTANCE"), 30, WHITE, 0, 800, 0.06); s.fade(sb, FW("flip", "support", "แนวรับ", 2.4), 0.4)
    cue(K("flip") + 0.8, "bell_C5", -22)
    captions(s, [(o2 + 0.1, L("THE ORDERS WERE NEVER USED", "ออเดอร์ยังไม่ถูกใช้"), WHITE), (K("flip") - 0.1, L("FRESH, AND THE ROLE FLIPS", "ยัง FRESH และสลับบทบาท"), GOLD)], c2, 1352)

    o3, c3 = K("touch") - 0.1, K("ex") - 0.1
    s = S(o3, c3)
    tagp(s, 3)
    s.label(540, 470, L("TOUCHED ONCE", "เคยถูกแตะ"), 46, WHITE, 1, 800, 0.04)
    ln = hl(s, nx(0.05), nx(1), ny(0.5), GOLD, 5, "16 10", 1)
    p1 = seg_path(s, [(0, 0.88), (0.12, 0.5), (0.25, 0.78), (0.38, 0.51), (0.5, 0.7)], WHITE, 6); s.draw(p1, o3 + 0.3, 1.3)
    r = ring(s, nx(0.38), ny(0.51), 18, RED); s.pop(r, o3 + 1.3, 0.35, 0.3)
    us = s.pill(nx(0.38), ny(0.36), L("USED", "ใช้แล้ว"), RED, WHITE, 24); s.pop(us, o3 + 1.4, 0.35, 0.5)
    p2 = seg_path(s, [(0.5, 0.7), (0.66, 0.24), (0.84, 0.1)], WHITE, 6); s.draw(p2, K("fail") + 0.2, 0.9)
    xm = xmark(s, nx(0.57), ny(0.5), 18, RED, 6); s.draw(xm, K("fail") + 0.8, 0.3)
    bk = s.pill(nx(0.78), ny(0.3), L("2ND VISIT: BREAKS", "รอบสอง: เบรก"), RED, WHITE, 24); s.pop(bk, K("fail") + 0.9, 0.35, 0.5)
    cue(K("fail") + 0.8, "whoosh-short_1", -22)
    captions(s, [(o3 + 0.1, L("A TAP AND A REACTION: USED", "แตะแล้วเด้ง: ใช้แล้ว"), RED), (K("fail") - 0.1, L("NEXT TIME IT USUALLY BREAKS", "รอบหน้ามักเบรก"), RED)], c3)

    o4, c4 = K("ex") - 0.1, K("next") - 0.1
    s = S(o4, c4)
    tagp(s, 3)
    hp = s.pill(540, 470, "XAUUSD  ·  1D", WHITE, "#0b0b0b", 26); s.pop(hp, o4 + 0.2, 0.4, 0.5)
    t1, t2 = o4 + 0.3, K("ex2")
    pn = panel(s, 40, 560, 490, 640); s.fade(pn, t1, 0.3)
    A = path_candles([(0, 70), (3, 50), (6, 64), (9, 58), (12, 26), (15, 49.8), (19, 20)], seed=31, noise=1.0, wick=1.0)
    ch, g = mini(s, A, 50, 610, 470, 520, 10, 85, 1); s.fade(g, t1 + 0.1, 0.4)
    l1 = hl(s, ch.x(3) - 6, 520, ch.y(50), GOLD, 3); s.fade(l1, t1 + 0.3, 0.3)
    r1 = ring(s, ch.x(15), ch.y(49.8), 14, GOLD); s.pop(r1, t1 + 1.2, 0.35, 0.3)
    a1 = s.label(285, 1170, L("FRESH FLIP · REJECTED", "FRESH FLIP · REJECT"), 24, GOLD, 0, 800, 0.06); s.fade(a1, t1 + 1.3)
    pn2 = panel(s, 550, 560, 490, 640); s.fade(pn2, t2, 0.3)
    B = path_candles([(0, 72), (3, 50), (6, 68), (9, 50.6), (12, 64), (16, 22)], seed=33, noise=1.0, wick=1.0)
    ch2, g2 = mini(s, B, 560, 610, 470, 520, 10, 85, 1); s.fade(g2, t2 + 0.1, 0.4)
    l2 = hl(s, ch2.x(3) - 6, 1030, ch2.y(50), GREY, 3, "8 6"); s.fade(l2, t2 + 0.3, 0.3)
    r2 = ring(s, ch2.x(9), ch2.y(50.6), 14, RED); s.pop(r2, t2 + 0.8, 0.35, 0.3)
    x2 = xmark(s, ch2.x(13.3), ch2.y(50), 12, RED, 5); s.draw(x2, t2 + 1.4, 0.3)
    a2 = s.label(795, 1170, L("TAPPED · THEN BROKEN", "แตะแล้ว · แล้วเบรก"), 24, RED, 0, 800, 0.06); s.fade(a2, t2 + 1.5)
    cue(t1 + 1.2, "bell_C5", -22); cue(t2 + 1.4, "whoosh-short_2", -24)
    captions(s, [(o4 + 0.1, L("FRESH FLIP: A SHARP REJECTION", "FRESH FLIP: REJECT แรง"), GOLD), (t2 - 0.1, L("USED LEVEL: BROKEN NEXT VISIT", "ระดับที่ใช้แล้ว: รอบหน้าเบรก"), RED)], c4)
    next_card(K("next") - 0.1, G["TOTAL"], 4, *NEXT[3], TOT)


# ======================================================================================================== 4  refinement ladder
def ep4():
    o1, c1 = 0, K("s1") - 0.1
    s = S(o1, c1, first=True)
    tagp(s, 4)
    title_block(s, "REFINEMENT", L("MANY LEVELS  ·  ONE ENTRY", "หลายระดับ  ·  ENTRY เดียว"))
    for k, tf in enumerate(("5M", "15M", "30M")):
        p = s.pill(540, 1060 - 140 * k, tf, [WHITE, WHITE, GOLD][k], "#111", 38); s.pop(p, 0.6 + 0.35 * k, 0.35, 0.5)
    captions(s, [(0.1, L("TOO MANY LINES?", "เส้นเยอะเกินไป?"), WHITE)], c1)

    o2, c2 = K("s1") - 0.1, K("ex") - 0.1
    s = S(o2, c2)
    tagp(s, 4)
    s.label(540, 470, L("THE LADDER", "บันไดรีไฟน์"), 50, WHITE, 1, 800, 0.06)
    rows(s, [("SET THE HTF BIAS", "ตั้ง BIAS บน HTF", WHITE), ("MARK EVERY FRESH LEVEL ON THE LTF", "มาร์คทุก FRESH LEVEL บน LTF", WHITE),
             ("STEP UP  ·  DELETE NON-LEVELS", "ขยับ TF ขึ้น  ·  ลบเส้นที่ไม่ใช่", WHITE), ("ONE LEVEL LEFT  =  ENTRY", "เหลือเส้นเดียว  =  ENTRY", GOLD)],
         [K("s1"), K("s2"), K("s3"), K("s4")], y0=620, dy=140, size=30)
    sl = s.label(540, 1220, L("SL JUST BEYOND THE WICK", "SL เลย WICK ไปนิดเดียว"), 32, RED, 0, 800, 0.06); s.fade(sl, K("sl") + 0.2, 0.4, y=10)
    captions(s, [(K("del") - 0.1, L("NOT A KEY LEVEL UP THERE? DELETE", "ไม่ใช่ KEY LEVEL บน TF ใหญ่? ลบ"), RED)], K("s4") - 0.1)

    o3, c3 = K("ex") - 0.1, K("next") - 0.1
    s = S(o3, c3)
    tagp(s, 4)
    hp = s.pill(400, 470, L("XAUUSD  ·  SELL BIAS", "XAUUSD  ·  SELL BIAS"), WHITE, "#0b0b0b", 26); s.pop(hp, o3 + 0.2, 0.4, 0.5)
    C = path_candles([(0, 40), (4, 48), (6, 44), (9, 58), (11, 55), (14, 78), (17, 60), (19, 70.3), (24, 36)], seed=41, noise=1.0, wick=1.0)
    ch = Chart(C, 27, 80, 1000, 600, 1230, 25, 90, 0.64)
    rid = candles_clip(s, ch)
    t15, t30 = FW("ex", "fifteen", "สิบห้า", 2.2), FW("ex", "thirty", "สามสิบ", 3.6)
    reveal(rid, ch, [(o3, -1), (o3 + 0.2, 17), (t30 + 0.8, 17), (t30 + 2.4, 24)], o3)
    tfs = []
    for k, tf in enumerate(("5M", "15M", "30M")):
        p = s.pill(800, 470, tf, GOLD if k == 2 else LBLUE, "#111", 30); tfs.append(p)
    s.pop(tfs[0], o3 + 0.4, 0.3, 0.5); out(tfs[0], t15, 0.15); s.pop(tfs[1], t15, 0.3, 0.5); out(tfs[1], t30, 0.15); s.pop(tfs[2], t30, 0.3, 0.5)
    L6 = [74, 70, 66, 62, 58, 54]
    kill15, kill30 = (74, 62, 54), (66, 58)
    for k, p in enumerate(L6):
        ln = hl(s, ch.x(8), ch.x(26), ch.y(p), WHITE, 3); s.fade(ln, o3 + 0.6 + 0.15 * k, 0.25)
        if p in kill15 or p in kill30:
            t = t15 + 0.4 if p in kill15 else t30 + 0.4
            out(ln, t, 0.35, 0.1)
            xm = xmark(s, ch.x(26) + 18, ch.y(p), 9, RED, 4); s.draw(xm, t, 0.25)
    keep = hl(s, ch.x(8), ch.x(26), ch.y(70), GOLD, 5); s.fade(keep, t30 + 0.6, 0.3)
    en = s.pill(ch.x(23), ch.y(70) - 32, "ENTRY", GOLD, "#111", 22); s.pop(en, t30 + 0.8, 0.35, 0.5)
    slp = hl(s, ch.x(14), ch.x(26), ch.y(79.5), RED, 3, "10 6"); s.fade(slp, t30 + 1.0, 0.3)
    slt = s.label(ch.x(26), ch.y(79.5) - 12, "SL", 22, RED, 0, 800, 0.08, "end"); s.fade(slt, t30 + 1.1)
    cue(t15 + 0.4, "whoosh-short_1", -24); cue(t30 + 0.6, "bell_A4", -20)
    captions(s, [(o3 + 0.1, L("5M: SIX LINES", "5M: หกเส้น"), WHITE), (t15 - 0.1, L("15M: THREE LEFT", "15M: เหลือสามเส้น"), LBLUE),
                 (t30 - 0.1, L("30M: ONE LEVEL = ENTRY", "30M: เส้นเดียว = ENTRY"), GOLD)], c3)
    next_card(K("next") - 0.1, G["TOTAL"], 5, *NEXT[4], TOT)


# ======================================================================================================== 5  storyline road map
def ep5():
    o1, c1 = 0, K("conf") - 0.1
    s = S(o1, c1, first=True)
    tagp(s, 5)
    title_block(s, "ROAD MAP", L("KEY LEVEL TO KEY LEVEL", "จาก KEY LEVEL สู่ KEY LEVEL"))
    b1 = rbox(s, nx(0.02), ny(0.2), nx(0.98), ny(0.1), GOLD, 0.16, 0.8, 2); s.fade(b1, 0.4, 0.4)
    b2 = rbox(s, nx(0.02), ny(0.92), nx(0.98), ny(0.82), GOLD, 0.16, 0.8, 2); s.fade(b2, 0.6, 0.4)
    t1 = s.label(nx(0.98) - 10, ny(0.1) + 34, "KEY LEVEL", 24, GOLD, 0, 800, 0.08, "end"); s.fade(t1, 0.5)
    t2 = s.label(nx(0.98) - 10, ny(0.92) - 14, "NEXT KEY LEVEL", 24, GOLD, 0, 800, 0.08, "end"); s.fade(t2, 0.7)
    p = seg_path(s, [(0.08, 0.15), (0.3, 0.45), (0.38, 0.36), (0.6, 0.66), (0.68, 0.58), (0.9, 0.87)], WHITE, 6); s.draw(p, 0.9, 1.6)
    captions(s, [(0.1, L("FROM ONE LEVEL TO THE NEXT", "จากระดับหนึ่ง สู่อีกระดับ"), WHITE)], c1)

    o2, c2 = K("conf") - 0.1, K("bias") - 0.1
    s = S(o2, c2)
    tagp(s, 5)
    s.label(540, 480, L("CONFIRMED BY A LOWER-TF MSS", "ยืนยันด้วย MSS บน TF ที่เล็กกว่า"), 40, WHITE, 1, 800, 0.03)
    rows(s, [("MONTHLY KL  ·  MSS ON W OR D", "MONTHLY KL  ·  MSS บน W หรือ D", GOLD), ("WEEKLY KL  ·  MSS ON D OR 4H", "WEEKLY KL  ·  MSS บน D หรือ 4H", WHITE),
             ("DAILY KL  ·  MSS ON 4H OR 1H", "DAILY KL  ·  MSS บน 4H หรือ 1H", WHITE)], [K("m"), K("w"), K("d")], y0=680, dy=160, size=32)
    captions(s, [(o2 + 0.1, L("ONE OR TWO TIMEFRAMES LOWER", "ต่ำกว่า 1 หรือ 2 TIMEFRAME"), LBLUE)], c2)

    o3, c3 = K("bias") - 0.1, K("ex") - 0.1
    s = S(o3, c3)
    tagp(s, 5)
    s.label(540, 470, L("TRADE WITH THE STORY", "เทรดตามเรื่องราว"), 46, WHITE, 1, 800, 0.04)
    b1 = rbox(s, nx(0.02), ny(0.16), nx(0.98), ny(0.06), GOLD, 0.16, 0.8, 2, 1)
    b2 = rbox(s, nx(0.02), ny(0.96), nx(0.98), ny(0.86), GOLD, 0.16, 0.8, 2, 1)
    rbl = hl(s, nx(0.02), nx(0.98), ny(0.55), GREY, 4, "12 8"); s.fade(rbl, K("road"), 0.3)
    rbt = s.pill(nx(0.18), ny(0.55), "ROAD BLOCK", "#3a3a3a", WHITE, 22, 0, False); s.pop(rbt, K("road") + 0.1, 0.35, 0.5)
    p = seg_path(s, [(0.06, 0.11), (0.28, 0.4), (0.35, 0.32), (0.5, 0.55), (0.58, 0.42), (0.88, 0.9)], WHITE, 6); s.draw(p, o3 + 0.3, 2.2)
    up = arrow(s, nx(0.7), ny(0.5), nx(0.82), ny(0.75), GREEN, 5, 18); show_arrow(s, up, o3 + 1.6, 0.4)
    dn = arrow(s, nx(0.5), ny(0.58), nx(0.6), ny(0.36), RED, 5, 18); show_arrow(s, dn, K("road") + 1.0, 0.4)
    xm = xmark(s, nx(0.56), ny(0.42), 16, RED, 5); s.draw(xm, K("road") + 1.5, 0.3)
    rk = s.label(nx(0.62), ny(0.3), L("COUNTER-TREND = HIGHER RISK", "สวนเทรนด์ = เสี่ยงกว่า"), 24, RED, 0, 800, 0.06, "start"); s.fade(rk, K("road") + 1.6)
    cue(K("road"), "whoosh-short_2", -24)
    captions(s, [(o3 + 0.1, L("ONLY THAT DIRECTION, TO THE NEXT LEVEL", "ทิศเดียว จนถึงระดับถัดไป"), GREEN), (K("road") - 0.1, L("ROAD BLOCKS CAUSE PULLBACKS", "ROAD BLOCK ทำให้ราคาย่อ"), GREY)], c3)

    o4, c4 = K("ex") - 0.1, K("next") - 0.1
    s = S(o4, c4)
    tagp(s, 5)
    hp = s.pill(540, 470, "XAUUSD  ·  MONTHLY + DAILY", WHITE, "#0b0b0b", 26); s.pop(hp, o4 + 0.2, 0.4, 0.5)
    C = path_candles([(0, 42), (3, 22), (5, 31), (7, 24.5), (9, 38), (12, 33), (17, 62), (19, 56), (24, 86)], seed=51, noise=1.1, wick=1.1)
    ch = Chart(C, 27, 80, 1000, 600, 1230, 12, 94, 0.64)
    rid = candles_clip(s, ch)
    th, tsh, tr = FW("ex", "held", "ยืน", 1.4), FW("ex", "shifted", "เปลี่ยน", 2.6), FW("ex", "ran", "วิ่ง", 3.6)
    reveal(rid, ch, [(o4, -1), (o4 + 0.2, 4), (th + 0.6, 7), (tsh - 0.1, 7), (tsh + 0.8, 10), (tr - 0.1, 10), (tr + 2.0, 24)], o4)
    lvl(s, ch, 22, 0, 26, GOLD, L("MONTHLY KL · HELD", "MONTHLY KL · ยืนได้"), th, 4, "", False, 22)
    ms = hl(s, ch.x(5), ch.x(11), ch.y(31.5), LBLUE, 3); s.fade(ms, tsh + 0.5, 0.3)
    mt = s.label(ch.x(11) + 8, ch.y(31.5) + 8, "DAILY MSS", 22, LBLUE, 0, 800, 0.06, "start"); s.fade(mt, tsh + 0.6)
    lvl(s, ch, 86, 0, 26, GOLD, L("NEXT MONTHLY KL", "MONTHLY KL ถัดไป"), tr, 4, "", True, 22)
    rt = ring(s, ch.x(24), ch.y(86), 20, GOLD); s.pop(rt, tr + 2.0, 0.35, 0.3)
    cue(tsh + 0.5, "bell_C5", -22); cue(tr + 2.0, "bell_A4", -20)
    captions(s, [(o4 + 0.1, L("MONTHLY LEVEL + DAILY MSS", "MONTHLY LEVEL + DAILY MSS"), GOLD), (tr - 0.1, L("ON TO THE NEXT MONTHLY LEVEL", "ไปต่อถึง MONTHLY LEVEL ถัดไป"), GOLD)], c4)
    next_card(K("next") - 0.1, G["TOTAL"], 6, *NEXT[5], TOT)


# ======================================================================================================== 6  the entry model
def ep6():
    o1, c1 = 0, K("s1") - 0.1
    s = S(o1, c1, first=True)
    tagp(s, 6)
    title_block(s, "THE ENTRY MODEL", L("2 TIMEFRAMES LOWER", "ลงไป 2 TIMEFRAME"))
    for k, (a, b) in enumerate((("D", "1H"), ("4H", "30M"))):
        y = 760 + 150 * k
        p1 = s.pill(330, y, a, GOLD, "#111", 40); s.pop(p1, 0.6 + 0.4 * k, 0.35, 0.5)
        sk = s.label(540, y + 12, "·  ·  ·", 40, GREY, 0, 800, 0.1); s.fade(sk, 0.8 + 0.4 * k)
        p2 = s.pill(750, y, b, LBLUE, "#111", 40); s.pop(p2, 1.0 + 0.4 * k, 0.35, 0.5)
    captions(s, [(0.1, L("THE FULL MODEL, STEP BY STEP", "โมเดลเต็ม ทีละขั้น"), WHITE)], c1)

    o2, c2 = K("s1") - 0.1, K("re") - 0.1
    s = S(o2, c2)
    tagp(s, 6)
    rows(s, [("TAP A HTF KEY LEVEL", "แตะ KEY LEVEL บน HTF", WHITE), ("DROP 2 TF  ·  D TO 1H  ·  4H TO 30M", "ลง 2 TF  ·  D ไป 1H  ·  4H ไป 30M", WHITE),
             ("MSS WITH A BODY CLOSE", "MSS ที่ปิดด้วยเนื้อเทียน", LBLUE), ("MARK THE LEG  ·  REFINE TO ONE", "มาร์คทั้งขา  ·  REFINE เหลือเส้นเดียว", WHITE),
             ("LIMIT  ·  SL BEYOND WICK  ·  TARGET KL", "LIMIT  ·  SL เลย WICK  ·  TARGET KL", GOLD)],
         [K("s1"), K("s2"), K("s3"), K("s4"), K("s5")], y0=500, dy=150, size=28)
    xw = s.label(540, 1290, L("A WICK THROUGH IS NOT AN MSS", "WICK ทะลุ ไม่ใช่ MSS"), 28, RED, 0, 800, 0.06); s.fade(xw, K("s3") + 1.4, 0.4)

    o3, c3 = K("re") - 0.1, K("next") - 0.1
    s = S(o3, c3)
    tagp(s, 6)
    hp = s.pill(540, 470, L("XAUUSD  ·  ENTRY + RE-ENTRY", "XAUUSD  ·  ENTRY + RE-ENTRY"), WHITE, "#0b0b0b", 26); s.pop(hp, o3 + 0.2, 0.4, 0.5)
    C = path_candles([(0, 44), (3, 22), (5, 34), (7, 27), (10, 40), (12, 35.4), (15, 56), (17, 51), (19, 63), (21, 55.4), (26, 84)], seed=61, noise=1.0, wick=1.0)
    ch = Chart(C, 29, 80, 1000, 600, 1230, 15, 92, 0.64)
    rid = candles_clip(s, ch)
    d = max(0.4, (c3 - 1.0 - o3) / 6)
    reveal(rid, ch, [(o3, -1), (o3 + 0.2, 12), (o3 + 0.2 + d, 12), (o3 + 0.2 + 2 * d, 15), (o3 + 0.2 + 3 * d, 21), (o3 + 0.2 + 5 * d, 26)], o3)
    lvl(s, ch, 22, 0, 28, GOLD, "HTF KL", o3 + 0.3, 4, "", False, 22)
    m1 = hl(s, ch.x(5), ch.x(10), ch.y(34.5), LBLUE, 3); s.fade(m1, o3 + 0.5, 0.3)
    m1t = s.label(ch.x(5), ch.y(34.5) - 10, "MSS", 20, LBLUE, 0, 800, 0.06, "start"); s.fade(m1t, o3 + 0.6)
    pos_box(s, ch.x(12) - 6, ch.x(19), ch.y(36), ch.y(63), ch.y(31), o3 + 0.2 + d)
    e1 = s.pill(ch.x(12), ch.y(36) + 30, "ENTRY 1", GOLD, "#111", 20); s.pop(e1, o3 + 0.3 + d, 0.35, 0.5)
    m2 = hl(s, ch.x(15), ch.x(19), ch.y(56.5), LBLUE, 3); s.fade(m2, o3 + 0.2 + 2.6 * d, 0.3)
    m2t = s.label(ch.x(15), ch.y(56.5) - 10, "MSS 2", 20, LBLUE, 0, 800, 0.06, "start"); s.fade(m2t, o3 + 0.3 + 2.6 * d)
    pos_box(s, ch.x(21) - 6, ch.x(27), ch.y(56), ch.y(84), ch.y(52), o3 + 0.2 + 3 * d)
    e2 = s.pill(ch.x(21), ch.y(56) + 30, "RE-ENTRY", GOLD, "#111", 20); s.pop(e2, o3 + 0.3 + 3 * d, 0.35, 0.5)
    cue(o3 + 0.3 + d, "bell_C5", -22); cue(o3 + 0.3 + 3 * d, "bell_E5", -22)
    captions(s, [(o3 + 0.1, L("SHIFT AGAIN? ADD A RE-ENTRY", "MSS อีกครั้ง? เข้าเพิ่ม"), GOLD)], c3)
    next_card(K("next") - 0.1, G["TOTAL"], 7, *NEXT[6], TOT)


# ======================================================================================================== 7  trendline confirmation + outro
def ep7():
    o1, c1 = 0, K("t1") - 0.1
    s = S(o1, c1, first=True)
    tagp(s, 7)
    title_block(s, "TRENDLINES", L("A CONFIRMATION, NEVER THE ENTRY", "เป็นการยืนยัน ไม่ใช่จุดเข้า"))
    kb = rbox(s, 200, 900, 880, 990, GOLD, 0.16, 0.8, 2); s.fade(kb, 0.6, 0.4)
    kt = s.label(540, 958, "KEY LEVEL", 30, GOLD, 0, 800, 0.1); s.fade(kt, 0.7)
    tln = s.path("M 180 1150 L 900 780", LBLUE, 5); s.draw(tln, 1.0, 0.8)
    captions(s, [(0.1, L("CONFIRMATION AT A KEY LEVEL", "การยืนยัน ที่ KEY LEVEL"), WHITE)], c1)

    o2, c2 = K("t1") - 0.1, K("flip") - 0.1
    s = S(o2, c2)
    tagp(s, 7)
    hp = s.pill(540, 470, "XAUUSD  ·  1H", WHITE, "#0b0b0b", 26); s.pop(hp, o2 + 0.2, 0.4, 0.5)
    C = path_candles([(0, 44), (2, 48), (4, 30), (8, 58), (11, 44), (15, 68), (18, 58), (22, 82)], seed=71, noise=0.9, wick=0.9)
    C[4] = (38, 39, 30, 33); C[5] = (33, 42, 32, 41); C[11] = (50, 51, 44, 46); C[12] = (46, 56, 45, 54)
    ch = Chart(C, 25, 80, 1000, 600, 1230, 20, 90, 0.64)
    kb = rbox(s, ch.x(16), ch.y(61), ch.x(21), ch.y(55), GOLD, 0.16, 0.8, 2); s.fade(kb, o2 + 0.4, 0.4)
    kt = s.label(ch.x(21), ch.y(55) + 28, "KL", 22, GOLD, 0, 800, 0.08, "end"); s.fade(kt, o2 + 0.5)
    rid = candles_clip(s, ch)
    t2, td, t3 = K("t2"), K("draw"), K("t3")
    reveal(rid, ch, [(o2, -1), (o2 + 0.2, 6), (t2 - 0.1, 6), (t2 + 0.6, 12), (td - 0.1, 12), (td + 0.8, 15), (t3 - 0.1, 15), (t3 + 0.7, 18), (t3 + 2.0, 22)], o2)
    for (i, t, key) in ((4.5, K("t1") + 0.3, "t1"), (11.5, t2 + 0.6, "t2")):
        lo = min(C[int(i - 0.5)][2], C[int(i + 0.5)][2])
        r = rbox(s, ch.x(i - 0.5) - 14, ch.y(max(C[int(i - 0.5)][1], C[int(i + 0.5)][1]) + 1.5), ch.x(i + 0.5) + 14, ch.y(lo - 1.5), WHITE, 0.0, 1, 3, 0, "6 5")
        s.fade(r, t, 0.3)
        lb = s.pill(ch.x(i), ch.y(lo) + 40, "ENGULFING", WHITE, "#111", 20); s.pop(lb, t + 0.1, 0.35, 0.5)
        cue(t, "bell_G4", -24)
    bos = hl(s, ch.x(8), ch.x(14), ch.y(58), LBLUE, 3); s.fade(bos, FW("t2", "break", "เบรก", 2.2) + 0.2, 0.3)
    bt = s.label(ch.x(14) + 8, ch.y(58) + 8, "BOS", 22, LBLUE, 0, 800, 0.08, "start"); s.fade(bt, FW("t2", "break", "เบรก", 2.2) + 0.3)
    def tly(i): return 30 + 2 * (i - 4)
    tl_ = s.path(f"M {ch.x(4):.1f} {ch.y(tly(4)):.1f} L {ch.x(22):.1f} {ch.y(tly(22)):.1f}", LBLUE, 4); s.draw(tl_, td + 0.2, 0.8)
    rr = ring(s, ch.x(18), ch.y(58), 18, GOLD); s.pop(rr, t3 + 0.7, 0.35, 0.3)
    en = s.pill(ch.x(18) + 70, ch.y(58) + 40, L("3RD TOUCH = ENTRY", "แตะครั้งที่ 3 = ENTRY"), GOLD, "#111", 22); s.pop(en, t3 + 0.8, 0.35, 0.5)
    cue(t3 + 0.7, "bell_A4", -20)
    captions(s, [(o2 + 0.1, L("SWING 1: ENGULFING", "SWING 1: ENGULFING"), WHITE), (t2 - 0.1, L("SWING 2: ENGULFING + BOS", "SWING 2: ENGULFING + BOS"), LBLUE),
                 (td - 0.1, L("CONNECT THE TWO SWINGS", "ลากเส้นเชื่อมสองสวิง"), LBLUE), (t3 - 0.1, L("THIRD TOUCH AT THE KEY LEVEL", "แตะครั้งที่ 3 ที่ KEY LEVEL"), GOLD)], c2)

    o3, c3 = K("flip") - 0.1, K("body") - 0.1
    s = S(o3, c3)
    tagp(s, 7)
    s.label(540, 470, L("BROKEN? DON'T DELETE IT", "โดนเบรก? อย่าลบ"), 46, WHITE, 1, 800, 0.03)
    tl_ = s.path(f"M {nx(0.0):.1f} {ny(0.1):.1f} L {nx(1.0):.1f} {ny(0.85):.1f}", LBLUE, 4, drawn=True)
    p = seg_path(s, [(0.02, 0.4), (0.14, 0.2), (0.24, 0.5), (0.32, 0.34), (0.44, 0.62), (0.55, 0.2), (0.7, 0.62), (0.84, 0.25)], WHITE, 6); s.draw(p, o3 + 0.3, 2.2)
    xb = xmark(s, nx(0.48), ny(0.46), 16, RED, 5); s.draw(xb, o3 + 1.3, 0.3)
    rt = ring(s, nx(0.7), ny(0.62), 18, RED); s.pop(rt, o3 + 2.0, 0.35, 0.3)
    rp = s.pill(nx(0.78), ny(0.75), L("RETEST = SELL", "RETEST = SELL"), RED, WHITE, 24); s.pop(rp, o3 + 2.1, 0.35, 0.5)
    cue(o3 + 2.0, "bell_E5", -22)
    captions(s, [(o3 + 0.1, L("THE RETEST FROM THE OTHER SIDE", "RETEST จากอีกฝั่ง"), RED)], c3)

    o4, c4 = K("body") - 0.1, K("sum") - 0.1
    s = S(o4, c4)
    tagp(s, 7)
    s.label(540, 470, L("FLAT SWINGS: BODY TO BODY", "สวิงแนวราบ: BODY ถึง BODY"), 42, WHITE, 1, 800, 0.03)
    xs = (260, 440, 640, 820)
    bodies = [(820, 980, 1110), (800, 965, 1140), (830, 975, 1090), (790, 960, 1150)]
    for k, (x, (top, bot, wick)) in enumerate(zip(xs, bodies)):
        c_ = big_candle(s, x, 70, top - 40, top, bot, wick, 0, UP if k % 2 else DOWN, False); s.fade(c_, o4 + 0.2 + 0.15 * k, 0.3)
    wl = s.path(f"M 200 1150 L 900 1150", GREY, 3, style="stroke-dasharray:10 8;"); s.fade(wl, o4 + 1.0, 0.3)
    wx = xmark(s, 940, 1150, 14, RED, 5); s.draw(wx, o4 + 1.3, 0.3)
    wt = s.label(200, 1200, L("WICK TO WICK", "WICK ถึง WICK"), 24, GREY, 0, 800, 0.06, "start"); s.fade(wt, o4 + 1.2)
    bl = s.path("M 200 968 L 900 968", GOLD, 5); s.draw(bl, FW("body", "body", "เนื้อเทียน", 1.0) + 0.3, 0.6)
    bt = s.label(900, 948, "BODY TO BODY", 26, GOLD, 0, 800, 0.06, "end"); s.fade(bt, FW("body", "body", "เนื้อเทียน", 1.0) + 0.6)
    captions(s, [(o4 + 0.1, L("LINE THROUGH THE BODIES", "ลากผ่านเนื้อเทียน"), GOLD)], c4)

    o5, c5 = K("sum") - 0.1, K("order") - 0.05
    s = S(o5, c5)
    tagp(s, 7)
    s.label(540, 470, "MSNR PRO", 56, GOLD, 1, 800, 0.1)
    items = [("STRONG LEVELS", "STRONG LEVELS"), ("TIGHT STOPS", "SL ที่แคบ"), ("FRESH FLIPS", "FRESH FLIPS"), ("ONE REFINED LEVEL", "REFINE เหลือเส้นเดียว"),
             ("A CLEAR STORY", "STORYLINE ที่ชัด"), ("A CONFIRMED ENTRY", "ENTRY ที่ยืนยันแล้ว")]
    step = max(0.35, (c5 - o5 - 1.0) / 7)
    for k, it in enumerate(items):
        p = s.pill(540, 620 + 110 * k, L(*it), GOLD if k == 5 else WHITE, "#111", 30); s.pop(p, o5 + 0.3 + step * k, 0.35, 0.5)
    cue(o5 + 0.3 + step * 5, "bell_A4", -20)
    outro(K("order") - 0.05)
