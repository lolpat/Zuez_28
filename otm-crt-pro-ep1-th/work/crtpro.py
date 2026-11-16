"""Scenes for CRT PRO (otm-crt-pro-ep0..ep5; Thai: otm-crt-pro-epN-th, same file with LANG = "th").
A 5-part follow-up to the OTM CRT series (plus a "what you'll learn" intro): the valid sweep, the MSS + FVG + CE
entry, the stop and the targets, the timeframe pairs, and the checklist. Original drawings and synthetic XAUUSD charts
(candles up #2962ff, down white, connected). Thai visuals keep the trading term names in English."""
from otm import *
from msnr import title_block
from story import FW, rows, panel, mini, pos_box, next_card
from pro import hl

TOT = 5
NEXT = {0: "THE VALID SWEEP", 1: "THE ENTRY", 2: "STOP & TARGETS", 3: "TIMEFRAME PAIRS", 4: "THE CHECKLIST"}


def tagc(s, n):
    return s.label(540, 300, f"XAUUSD  ·  CRT PRO  ·  {n}/{TOT}", 26, GOLD, 1, 700, 0.2)


# one long setup used by the examples: a 4H range 40..80, a 5M sweep of the low that closes back inside, a shift up,
# a fair value gap 45..47.5 (CE 46.25), a partial at the range 50% (60), some chop, then the run to the CRT high.
HI, LO, MID = 80, 40, 60
def long_setup():
    return [(62, 63, 57, 58), (58, 60, 53, 54), (54, 55, 48, 49), (49, 50.5, 44, 45), (45, 47, 41, 42),
            (42, 43, 38.5, 41.5), (41.5, 44, 41, 43.5), (43.5, 45, 42.5, 43), (43, 49, 42.8, 48.5), (48.5, 52, 47.5, 51),
            (51, 51.5, 46, 47.5), (47.5, 55, 47, 54.5), (54.5, 60.5, 54, 59.5), (59.5, 61, 57, 58), (58, 60.5, 56.5, 59.8),
            (59.8, 61, 57.5, 58.5), (58.5, 60, 57, 59.5), (59.5, 68, 59, 67), (67, 75, 66.5, 74), (74, 80.4, 73.5, 79.5)]
SW, MSS, FVG0, FVG1, CE, FILL = 5, 8, 7, 9, 46.25, 10


def range_chart(s, C, t, nxs=None, x0=250, x1=1000, top=600, bot=1220, pmin=30, pmax=88, hi=HI, lo=LO, tf="4H", op=0):
    """the HTF candle on the left, the range box and its two levels; returns the LTF chart"""
    ch = Chart(C, nxs or len(C) + 2, x0, x1, top, bot, pmin, pmax, 0.62)
    box = rbox(s, 95, ch.y(hi), 1000, ch.y(lo), GOLD, 0.07, 0.0, 0, op)
    l1 = hl(s, 95, 1000, ch.y(hi), GOLD, 3, "14 10", op); l2 = hl(s, 95, 1000, ch.y(lo), GOLD, 3, "14 10", op)
    t1 = s.label(1000, ch.y(hi) - 14, "CRT HIGH", 24, GOLD, op, 800, 0.08, "end")
    t2 = s.label(1000, ch.y(lo) + 34, "CRT LOW", 24, GOLD, op, 800, 0.08, "end")
    hc = big_candle(s, 165, 70, ch.y(hi), ch.y(hi - 5), ch.y(lo + 6), ch.y(lo), op, DOWN)
    ht = s.label(165, ch.y(hi) - 22, tf, 24, GREY, op, 800, 0.1)
    if not op:
        for k, i in enumerate((hc, ht, box, l1, l2, t1, t2)):
            s.fade(i, t + 0.08 * k, 0.35)
    return ch


# ======================================================================================================== 0  intro
def ep0():
    o1, c1 = 0, K("l1") - 0.1
    s = S(o1, c1, first=True)
    s.label(540, 300, L("XAUUSD  ·  CRT PRO  ·  START HERE", "XAUUSD  ·  CRT PRO  ·  เริ่มที่นี่"), 26, GOLD, 1, 700, 0.2)
    title_block(s, "CRT PRO", L("WHAT YOU'LL LEARN IN 5 PARTS", "ดูจบ 5 ตอน คุณจะได้อะไร"))
    for k in range(5):
        p = s.pill(540 + (k - 2) * 140, 820, str(k + 1), GOLD if k == 4 else WHITE, "#111", 40); s.pop(p, 0.5 + 0.2 * k, 0.35, 0.5)
    captions(s, [(0.1, L("CANDLE RANGE THEORY, WITH RULES", "CANDLE RANGE THEORY แบบมีกฎ"), WHITE)], c1)

    o2, c2 = K("l1") - 0.1, K("go") - 0.1
    s = S(o2, c2)
    s.label(540, 300, L("XAUUSD  ·  CRT PRO  ·  START HERE", "XAUUSD  ·  CRT PRO  ·  เริ่มที่นี่"), 26, GOLD, 1, 700, 0.2)
    s.label(540, 450, L("BY THE END, YOU CAN", "ดูจบแล้ว คุณจะ"), 44, WHITE, 1, 800, 0.04)
    items = [("SPOT A VALID SWEEP", "แยก SWEEP จริง / หลอก", WHITE), ("ENTER ON MSS + FVG", "เข้าที่ MSS + FVG", WHITE),
             ("PLACE THE SL  ·  PARTIAL AT 50%", "วาง SL  ·  แบ่งกำไรที่ 50%", WHITE), ("PICK THE RIGHT TIMEFRAME PAIR", "เลือกคู่ TIMEFRAME ให้ถูก", WHITE),
             ("RUN ONE CHECKLIST EVERY TRADE", "ไล่ CHECKLIST ก่อนเทรดทุกครั้ง", GOLD)]
    rows(s, items, [K(f"l{k}") for k in range(1, 6)], y0=600, dy=140, size=32)
    for k in range(5):
        ck = check(s, 975, 600 + 140 * k, 18, GREEN, 5); s.draw(ck, K(f"l{k + 1}") + 0.5, 0.3)

    o3, c3 = K("go") - 0.1, G["TOTAL"]
    s = S(o3, c3)
    a = s.label(540, 700, L("SAVE THE SERIES", "เซฟซีรีส์นี้ไว้"), 64, WHITE, 0, 800, 0.04); s.pop(a, o3 + 0.2, 0.4, 0.6)
    tn = FW("go", "start", "เริ่ม", 1.2)
    nx_ = s.label(540, 840, L(f"NEXT  ·  1/{TOT}", f"ตอนต่อไป  ·  1/{TOT}"), 30, GREY, 0, 700, 0.2); s.fade(nx_, tn, 0.4)
    b = s.label(540, 960, NEXT[0], 76, GOLD, 0, 800, 0.04); s.pop(b, tn + 0.3, 0.4, 0.6)
    cue(o3 + 0.2, "swell_2", -22); cue(tn + 0.3, "whoosh-long_1", -22)


# ======================================================================================================== 1  the valid sweep
def ep1():
    o1, c1 = 0, K("range") - 0.1
    s = S(o1, c1, first=True)
    tagc(s, 1)
    title_block(s, "THE VALID SWEEP", L("NOT EVERY WICK IS ONE", "ไม่ใช่ทุก WICK ที่เป็น SWEEP"))
    ln = hl(s, 200, 880, 900, GOLD, 4, "14 10"); s.fade(ln, 0.4, 0.4)
    c_ = big_candle(s, 540, 90, 760, 800, 860, 1060, 0, UP); s.pop(c_, 0.8, 0.4, 0.6)
    q = s.label(640, 1030, "?", 70, RED, 0, 800, 0); s.fade(q, 1.4, 0.3)
    captions(s, [(0.1, L("IT ALL STARTS WITH THE SWEEP", "ทุกอย่างเริ่มที่ SWEEP"), WHITE)], c1)

    o2, c2 = K("range") - 0.1, K("valid") - 0.1
    s = S(o2, c2)
    tagc(s, 1)
    C = long_setup()[:6]
    ch = range_chart(s, C, o2 + 0.3, nxs=22)
    cg = s.raw('<g id="@ID@" style="opacity:0">' + ch.candles() + "</g>", "cg"); s.fade(cg, o2 + 1.0, 0.4)
    b1 = s.label(560, ch.y(HI) - 70, "BSL", 34, LBLUE, 0, 800, 0.1); s.fade(b1, K("liq") + 0.2)
    b2 = s.label(560, ch.y(LO) + 100, "SSL", 34, RED, 0, 800, 0.1); s.fade(b2, K("liq") + 0.5)
    for k, x in enumerate((380, 470, 650, 740)):
        a = s.pill(x, ch.y(HI) - 30, "SL", "#2a2a2a", LBLUE, 18, 0, False); s.fade(a, K("liq") + 0.3 + 0.08 * k, 0.25)
        b = s.pill(x, ch.y(LO) + 60, "SL", "#2a2a2a", RED, 18, 0, False); s.fade(b, K("liq") + 0.6 + 0.08 * k, 0.25)
    captions(s, [(o2 + 0.1, L("ONE HTF CANDLE = THE RANGE", "แท่ง HTF หนึ่งแท่ง = กรอบ"), GOLD), (K("liq") - 0.1, L("STOPS SIT ON BOTH SIDES", "STOP LOSS รออยู่ทั้งสองฝั่ง"), WHITE)], c2)

    o3, c3 = K("valid") - 0.1, K("ex") - 0.1
    s = S(o3, c3)
    tagc(s, 1)
    for k, (x0, key, ok) in enumerate(((60, "valid", True), (560, "out", False))):
        t = K(key)
        pn = panel(s, x0, 520, 460, 620); s.fade(pn, t, 0.3)
        lv = hl(s, x0 + 20, x0 + 440, 900, GOLD, 4, "12 8"); s.fade(lv, t + 0.1, 0.3)
        lt = s.label(x0 + 30, 934, "CRT LOW", 22, GOLD, 0, 800, 0.08, "start"); s.fade(lt, t + 0.15)
        a = big_candle(s, x0 + 150, 64, 700, 720, 880, 900, 0, DOWN, False); s.fade(a, t + 0.2, 0.3)
        if ok:
            b = big_candle(s, x0 + 290, 64, 760, 870, 800, 1060, 0, UP, False)
            lab, col = L("CLOSES BACK INSIDE", "ปิดกลับเข้ากรอบ"), GREEN
        else:
            b = big_candle(s, x0 + 290, 64, 860, 870, 990, 1060, 0, DOWN, False)
            lab, col = L("CLOSES OUTSIDE", "ปิดนอกกรอบ"), RED
        s.fade(b, t + 0.6, 0.3)
        mk = (check if ok else xmark)(s, x0 + 410, 600, 24, col, 7); s.draw(mk, t + 1.0, 0.35)
        lb = s.label(x0 + 230, 1110, lab, 28, col, 0, 800, 0.04); s.fade(lb, t + 1.0)
        sb = s.label(x0 + 200, 612, "SWEEP" if ok else L("NOT A SWEEP", "ไม่ใช่ SWEEP"), 34, col, 0, 800, 0.06); s.fade(sb, t + 1.1)
        cue(t + 1.0, "bell_C5" if ok else "whoosh-short_1", -22)
    nn = s.pill(540, 1260, L("NEITHER SIDE TAKEN  =  NO TRADE", "ไม่มีฝั่งไหนโดนกวาด  =  ไม่มีเทรด"), RED, WHITE, 28); s.pop(nn, K("none") + 0.1, 0.4, 0.5)
    captions(s, [(K("valid") - 0.1, L("RUN THE LEVEL, CLOSE BACK INSIDE", "วิ่งเลยระดับ แล้วปิดกลับเข้ากรอบ"), GREEN),
                 (K("out") - 0.1, L("CLOSE OUTSIDE = ACCEPTANCE", "ปิดนอกกรอบ = ราคายอมรับระดับใหม่"), RED)], K("none") - 0.1, 1352)

    o4, c4 = K("ex") - 0.1, K("next") - 0.1
    s = S(o4, c4)
    tagc(s, 1)
    hp = s.pill(540, 470, "XAUUSD  ·  4H RANGE  ·  15M", WHITE, "#0b0b0b", 26); s.pop(hp, o4 + 0.2, 0.4, 0.5)
    t1, t2 = o4 + 0.3, K("ex2")
    for k, (x0, t, ok) in enumerate(((40, t1, False), (550, t2, True))):
        pn = panel(s, x0, 560, 490, 640); s.fade(pn, t, 0.3)
        if ok:
            D = [(62, 63, 56, 57), (57, 58, 50, 51), (51, 52, 45, 46), (46, 47, 41.5, 42.5), (42.5, 43, 35, 41.8), (41.8, 47, 41, 46.5), (46.5, 53, 46, 52.5), (52.5, 58, 51, 57)]
        else:
            D = [(62, 63, 56, 57), (57, 58, 50, 51), (51, 52, 45, 46), (46, 47, 41.5, 42.5), (42.5, 43, 35, 36), (36, 37, 31, 32), (32, 33, 27, 28), (28, 29.5, 25, 26)]
        ch, g = mini(s, D, x0 + 10, 600, 470, 520, 20, 70, 1); s.fade(g, t + 0.1, 0.4)
        lv = hl(s, x0 + 20, x0 + 470, ch.y(40), GOLD, 3, "10 7"); s.fade(lv, t + 0.2, 0.3)
        lt = s.label(x0 + 470, ch.y(40) - 10, "CRT LOW", 20, GOLD, 0, 800, 0.08, "end"); s.fade(lt, t + 0.25)
        r = ring(s, ch.x(4), ch.y(41.8 if ok else 36), 16, GREEN if ok else RED); s.pop(r, t + 0.8, 0.35, 0.3)
        lb = s.label(x0 + 245, 1170, L("CLOSED BACK INSIDE  ·  TRADE", "ปิดกลับเข้ากรอบ  ·  เทรดได้") if ok else L("CLOSED OUTSIDE  ·  SKIP", "ปิดนอกกรอบ  ·  ข้าม"),
                     22, GREEN if ok else RED, 0, 800, 0.04); s.fade(lb, t + 1.0)
        cue(t + 0.8, "bell_E5" if ok else "whoosh-short_2", -22)
    captions(s, [(o4 + 0.1, L("CLOSED BELOW, KEPT FALLING", "ปิดใต้โลว์ แล้วร่วงต่อ"), RED), (t2 - 0.1, L("WICK BELOW, CLOSE INSIDE: TRADE", "WICK ทะลุ ปิดในกรอบ: เทรดได้"), GREEN)], c4)
    next_card(K("next") - 0.1, G["TOTAL"], 2, NEXT[1], NEXT[1], TOT)


# ======================================================================================================== 2  the entry
def ep2():
    o1, c1 = 0, K("mss") - 0.1
    s = S(o1, c1, first=True)
    tagc(s, 2)
    title_block(s, "THE ENTRY", L("SWEEP = WHERE  ·  SHIFT = WHEN", "SWEEP = ที่ไหน  ·  SHIFT = เมื่อไหร่"))
    a = s.pill(370, 820, "SWEEP", RED, WHITE, 40); s.pop(a, 0.5, 0.4, 0.5)
    b = s.pill(710, 820, "SHIFT", LBLUE, "#111", 40); s.pop(b, FW("hook", "shift", "เปลี่ยน", 1.6), 0.4, 0.5)
    captions(s, [(0.1, L("WHERE, THEN WHEN", "ที่ไหน แล้วค่อยเมื่อไหร่"), WHITE)], c1)

    o2, c2 = K("mss") - 0.1, K("ex") - 0.1
    s = S(o2, c2)
    tagc(s, 2)
    C = long_setup()[2:12]
    ch = Chart(C, len(C) + 1, 110, 980, 560, 1200, 34, 58, 0.6)
    s.raw('<g id="@ID@">' + ch.candles() + "</g>", "cg")
    lo = hl(s, 110, 980, ch.y(LO), GOLD, 3, "12 8", 1)
    s.label(980, ch.y(LO) + 32, "CRT LOW", 22, GOLD, 1, 800, 0.08, "end")
    sw = ring(s, ch.x(SW - 2), ch.y(38.5), 16, RED, 1)
    s.label(ch.x(SW - 2), ch.y(38.5) + 44, "SWEEP", 22, RED, 1, 800, 0.08)
    lh = hl(s, ch.x(1) - 20, ch.x(7), ch.y(47), WHITE, 3, "8 6"); s.fade(lh, o2 + 0.4, 0.3)
    lht = s.label(ch.x(1) - 20, ch.y(47) - 12, L("LAST LOWER HIGH", "LOWER HIGH ล่าสุด"), 20, WHITE, 0, 800, 0.06, "start"); s.fade(lht, o2 + 0.5)
    mr = rbox(s, ch.x(MSS - 2) - 22, ch.y(49.3), ch.x(MSS - 2) + 22, ch.y(42.6), LBLUE, 0.0, 1, 4); s.fade(mr, FW("mss", "body", "เนื้อ", 2.4), 0.3)
    mt = s.pill(ch.x(MSS - 2), ch.y(49.3) - 30, "MSS", LBLUE, "#111", 22); s.pop(mt, FW("mss", "body", "เนื้อ", 2.4) + 0.1, 0.35, 0.5)
    fb = rbox(s, ch.x(FVG0 - 2) - 16, ch.y(47.5), ch.x(FVG1 - 2) + 60, ch.y(45), GOLD, 0.28, 0.9, 2); s.fade(fb, K("fvg") + 0.2, 0.4)
    ft = s.label(ch.x(FVG1 - 2) + 70, ch.y(47.5) + 4, "FVG", 26, GOLD, 0, 800, 0.08, "start"); s.fade(ft, K("fvg") + 0.3)
    ce = hl(s, ch.x(FVG0 - 2) - 16, ch.x(FVG1 - 2) + 60, ch.y(CE), WHITE, 3, "6 5"); s.fade(ce, K("ce") + 0.2, 0.3)
    cet = s.label(ch.x(FVG1 - 2) + 70, ch.y(CE) + 30, "CE 50%", 24, WHITE, 0, 800, 0.08, "start"); s.fade(cet, K("ce") + 0.3)
    en = s.pill(ch.x(FILL - 2), ch.y(44.4) + 6, "ENTRY", GOLD, "#111", 20); s.pop(en, K("ce") + 0.8, 0.35, 0.5)
    cue(K("fvg") + 0.2, "bell_C5", -22); cue(K("ce") + 0.8, "bell_E5", -22)
    captions(s, [(o2 + 0.1, L("BODY CLOSES ABOVE THE LOWER HIGH", "เนื้อเทียนปิดเหนือ LOWER HIGH"), LBLUE), (K("fvg") - 0.1, L("THE MOVE LEAVES A GAP", "การวิ่งทิ้ง FVG ไว้"), GOLD),
                 (K("ce") - 0.1, L("ENTRY = 50% OF THE GAP", "ENTRY = 50% ของ FVG"), WHITE)], c2)

    o3, c3 = K("ex") - 0.1, K("next") - 0.1
    s = S(o3, c3)
    tagc(s, 2)
    hp = s.pill(540, 470, "XAUUSD  ·  4H RANGE  ·  5M ENTRY", WHITE, "#0b0b0b", 26); s.pop(hp, o3 + 0.2, 0.4, 0.5)
    C = long_setup()[:13]
    ch = range_chart(s, C, o3 + 0.3, nxs=22)
    rid = candles_clip(s, ch)
    t2 = K("ex2")
    reveal(rid, ch, [(o3, -1), (o3 + 0.8, 3), (K("ex") + 1.6, SW), (t2 - 0.1, SW), (t2 + 1.2, FILL), (t2 + 2.6, 12)], o3)
    r = ring(s, ch.x(SW), ch.y(38.5), 14, RED); s.pop(r, K("ex") + 1.6, 0.35, 0.3)
    fb = rbox(s, ch.x(FVG0) - 8, ch.y(47.5), ch.x(FVG1) + 40, ch.y(45), GOLD, 0.3, 0.9, 2); s.fade(fb, t2 + 0.8, 0.3)
    lp = s.pill(ch.x(FVG1) + 110, ch.y(CE), "LIMIT @ CE", GOLD, "#111", 20); s.pop(lp, t2 + 1.0, 0.35, 0.5)
    cue(K("ex") + 1.6, "bell_C5", -24); cue(t2 + 1.0, "bell_E5", -22)
    captions(s, [(o3 + 0.1, L("4H RANGE  ·  5M SWEEP OF THE LOW", "กรอบ 4H  ·  SWEEP โลว์บน 5M"), WHITE), (t2 - 0.1, L("MSS UP  ·  LIMIT AT THE CE", "MSS ขึ้น  ·  LIMIT ที่ CE"), GOLD)], c3)
    next_card(K("next") - 0.1, G["TOTAL"], 3, NEXT[2], NEXT[2], TOT)


# ======================================================================================================== 3  stop & targets
def ep3():
    o1, c1 = 0, K("sl") - 0.1
    s = S(o1, c1, first=True)
    tagc(s, 3)
    title_block(s, "STOP & TARGETS", L("WHERE OUT  ·  WHERE PAID", "ออกตรงไหน  ·  กำไรตรงไหน"))
    for k, (txt, col) in enumerate((("SL", RED), ("50%", GOLD), ("TP", LBLUE))):
        p = s.pill(330 + 210 * k, 820, txt, col, "#111" if col != RED else WHITE, 40); s.pop(p, 0.6 + 0.3 * k, 0.35, 0.5)
    captions(s, [(0.1, L("THE STOP, THE PARTIAL, THE TARGET", "SL  ·  แบ่งกำไร  ·  เป้าหมาย"), WHITE)], c1)

    o2, c2 = K("sl") - 0.1, K("next") - 0.1
    s = S(o2, c2)
    tagc(s, 3)
    hp = s.pill(540, 470, "XAUUSD  ·  4H RANGE  ·  5M", WHITE, "#0b0b0b", 26); s.pop(hp, o2 + 0.2, 0.4, 0.5)
    C = long_setup()
    ch = range_chart(s, C, o2 + 0.2, nxs=22, op=1)
    rid = candles_clip(s, ch)
    te, tc = K("ex"), K("ex2")
    reveal(rid, ch, [(o2, FILL), (te - 0.1, FILL), (te + 1.0, 12), (tc - 0.1, 12), (tc + 1.6, 16), (tc + 3.0, 19)], o2)
    en = hl(s, ch.x(FILL) - 10, 1000, ch.y(CE), WHITE, 3); s.fade(en, o2 + 0.4, 0.3)
    ent = s.label(ch.x(FILL) - 18, ch.y(CE) + 8, "ENTRY", 20, WHITE, 0, 800, 0.06, "end"); s.fade(ent, o2 + 0.5)
    sl = hl(s, ch.x(SW) - 10, 1000, ch.y(38), RED, 4, "10 6"); s.fade(sl, K("sl") + 0.4, 0.3)
    slt = s.label(ch.x(SW) - 18, ch.y(38) + 8, "SL", 22, RED, 0, 800, 0.06, "end"); s.fade(slt, K("sl") + 0.5)
    r = ring(s, ch.x(SW), ch.y(38.5), 14, RED); s.pop(r, K("sl") + 0.3, 0.35, 0.3)
    md = hl(s, 95, 1000, ch.y(MID), GOLD, 3, "6 6"); s.fade(md, K("half") + 0.3, 0.3)
    mdt = s.label(95, ch.y(MID) - 10, L("RANGE 50%  ·  PARTIAL", "RANGE 50%  ·  แบ่งกำไร"), 22, GOLD, 0, 800, 0.06, "start"); s.fade(mdt, K("half") + 0.4)
    tp = s.pill(ch.x(16), ch.y(HI) - 34, L("TP  ·  CRT HIGH", "TP  ·  CRT HIGH"), LBLUE, "#111", 22); s.pop(tp, K("tp") + 0.4, 0.35, 0.5)
    pb = s.pill(ch.x(12), ch.y(MID) + 44, L("PARTIAL BANKED", "แบ่งกำไรแล้ว"), GOLD, "#111", 20); s.pop(pb, te + 1.0, 0.35, 0.5)
    chp = rbox(s, ch.x(12) - 10, ch.y(61.5), ch.x(16) + 10, ch.y(56), GREY, 0.12, 0.6, 2, 0, "6 5"); s.fade(chp, tc + 0.6, 0.3)
    cht = s.label(ch.x(14), ch.y(56) + 30, "CHOP", 20, GREY, 0, 800, 0.1); s.fade(cht, tc + 0.7)
    win = s.pill(ch.x(19) - 60, ch.y(HI) + 40, "4R", GREEN, "#111", 24); s.pop(win, tc + 3.0, 0.35, 0.5)
    cue(K("sl") + 0.3, "swell_1", -24); cue(te + 1.0, "bell_C5", -22); cue(tc + 3.0, "bell_A4", -20)
    captions(s, [(K("sl") - 0.1, L("SL BEYOND THE SWEEP WICK", "SL เลย WICK ที่กวาด"), RED), (K("half") - 0.1, L("BANK A PARTIAL AT 50%", "แบ่งกำไรที่ 50%"), GOLD),
                 (K("tp") - 0.1, L("FULL TARGET: THE OTHER SIDE", "เป้าเต็ม: อีกฝั่งของกรอบ"), LBLUE), (te - 0.1, L("PARTIAL AT 50%, THEN CHOP", "แบ่งกำไรที่ 50% แล้วแกว่ง"), GOLD),
                 (tc + 2.6, L("CRT HIGH HIT  ·  ABOUT 4X THE RISK", "ถึง CRT HIGH  ·  ประมาณ 4 เท่าของความเสี่ยง"), GREEN)], c2)
    next_card(K("next") - 0.1, G["TOTAL"], 4, NEXT[3], NEXT[3], TOT)


# ======================================================================================================== 4  timeframe pairs
def ep4():
    o1, c1 = 0, K("p1") - 0.1
    s = S(o1, c1, first=True)
    tagc(s, 4)
    title_block(s, "TIMEFRAME PAIRS", L("RIGHT RANGE  ·  RIGHT ENTRY CHART", "กรอบถูก  ·  กราฟเข้าออเดอร์ถูก"))
    captions(s, [(0.1, L("WRONG TIMEFRAME STILL LOSES", "TIMEFRAME ผิด ก็ยังขาดทุน"), RED)], c1)
    xm = xmark(s, 540, 860, 80, RED, 12); s.draw(xm, 0.8, 0.4)

    o2, c2 = K("p1") - 0.1, K("low") - 0.1
    s = S(o2, c2)
    tagc(s, 4)
    s.label(540, 470, L("THE PAIRS", "คู่ TIMEFRAME"), 50, WHITE, 1, 800, 0.06)
    for k, (rng, ent, key) in enumerate((("4H RANGE", "5M  /  15M ENTRY", "p1"), ("DAILY RANGE", "1H ENTRY", "p2"))):
        y = 700 + 230 * k; t = K(key)
        a = s.pill(300, y, rng, GOLD, "#111", 40); s.pop(a, t, 0.35, 0.5)
        ar = arrow(s, 470, y, 590, y, GREY, 5, 18); show_arrow(s, ar, t + 0.3, 0.3)
        b = s.pill(790, y, ent, LBLUE, "#111", 36); s.pop(b, t + 0.5, 0.35, 0.5)
        cue(t + 0.5, "bell_C5", -22)

    o3, c3 = K("low") - 0.1, K("ex") - 0.1
    s = S(o3, c3)
    tagc(s, 4)
    hp = s.pill(540, 470, L("4H RANGE ON THE 1M  ·  TOO LOW", "กรอบ 4H บน 1M  ·  เล็กเกินไป"), RED, WHITE, 26); s.pop(hp, o3 + 0.2, 0.4, 0.5)
    D = path_candles([(0, 62), (3, 57), (5, 61), (8, 55.5), (10, 60), (13, 54.8), (15, 59), (18, 55.2), (20, 58), (22, 56)], seed=91, noise=0.5, wick=0.5)
    ch = Chart(D, len(D) + 1, 120, 980, 600, 1200, 36, 84, 0.6)
    box = rbox(s, 100, ch.y(HI), 1000, ch.y(LO), GOLD, 0.06, 0.0, 0, 1)
    hl(s, 100, 1000, ch.y(HI), GOLD, 3, "14 10", 1); hl(s, 100, 1000, ch.y(LO), GOLD, 3, "14 10", 1)
    s.label(1000, ch.y(HI) - 12, "CRT HIGH", 22, GOLD, 1, 800, 0.08, "end"); s.label(1000, ch.y(LO) + 32, "CRT LOW", 22, GOLD, 1, 800, 0.08, "end")
    rid = candles_clip(s, ch)
    reveal(rid, ch, [(o3, -1), (o3 + 0.3, 4), (K("mid") - 0.1, 14), (K("loss") + 1.2, 22)], o3)
    for k, i in enumerate((3, 8, 13, 18)):
        t = o3 + 0.5 + (K("mid") - o3 - 0.6) * k / 3
        q = s.label(ch.x(i), ch.y(D[i][2]) + 36, "SWEEP?", 20, RED, 0, 800, 0.06); s.fade(q, t)
        x_ = xmark(s, ch.x(i), ch.y(D[i][2]) + 66, 10, RED, 4); s.draw(x_, K("loss") + 0.2 * k, 0.25)
    mb = rbox(s, ch.x(2), ch.y(63), ch.x(20), ch.y(53.5), RED, 0.08, 0.8, 2, 0, "8 6"); s.fade(mb, K("mid") + 0.2, 0.4)
    mt = s.label(540, ch.y(66), L("MID-RANGE NOISE", "สัญญาณรบกวนกลางกรอบ"), 30, RED, 0, 800, 0.06); s.fade(mt, K("mid") + 0.3)
    lz = s.pill(540, 1270, L("SL HIT  ·  SL HIT  ·  SL HIT", "SL HIT  ·  SL HIT  ·  SL HIT"), RED, WHITE, 26); s.pop(lz, K("loss") + 0.8, 0.4, 0.5)
    cue(K("loss") + 0.8, "whoosh-short_1", -22)

    o4, c4 = K("ex") - 0.1, K("next") - 0.1
    s = S(o4, c4)
    tagc(s, 4)
    hp = s.pill(540, 470, L("SAME SESSION ON THE 5M", "เซสชันเดียวกันบน 5M"), LBLUE, "#111", 26); s.pop(hp, o4 + 0.2, 0.4, 0.5)
    C = long_setup()[:12]
    ch = range_chart(s, C, o4 + 0.3, nxs=20, tf="4H")
    rid = candles_clip(s, ch)
    reveal(rid, ch, [(o4, -1), (o4 + 0.8, 3), (o4 + 2.2, SW + 1), (c4 - 0.6, 11)], o4)
    r = ring(s, ch.x(SW), ch.y(38.5), 16, GREEN); s.pop(r, o4 + 2.2, 0.35, 0.3)
    sp = s.pill(ch.x(SW), ch.y(38.5) + 50, L("ONE REAL SWEEP", "SWEEP จริงครั้งเดียว"), GREEN, "#111", 22); s.pop(sp, o4 + 2.3, 0.35, 0.5)
    cue(o4 + 2.2, "bell_C5", -22)
    next_card(K("next") - 0.1, G["TOTAL"], 5, NEXT[4], NEXT[4], TOT)


# ======================================================================================================== 5  checklist + outro
def ep5():
    o1, c1 = 0, K("c1") - 0.1
    s = S(o1, c1, first=True)
    tagc(s, 5)
    title_block(s, "THE CRT CHECKLIST", L("BEFORE EVERY TRADE", "ก่อนเทรดทุกครั้ง"))
    captions(s, [(0.1, L("RUN IT EVERY TIME", "ไล่ทุกครั้ง"), WHITE)], c1)

    o2, c2 = K("c1") - 0.1, K("miss") - 0.1
    s = S(o2, c2)
    tagc(s, 5)
    s.label(540, 470, L("THE CHECKLIST", "เช็กลิสต์"), 50, WHITE, 1, 800, 0.06)
    items = [("MARK THE HTF RANGE", "มาร์คกรอบบน HTF", WHITE), ("SWEEP CLOSES BACK INSIDE", "SWEEP ที่ปิดกลับเข้ากรอบ", WHITE),
             ("MSS + FVG", "MSS + FVG", LBLUE), ("ENTRY AT CE  ·  SL BEYOND THE WICK", "ENTRY ที่ CE  ·  SL เลย WICK", WHITE),
             ("PARTIAL AT 50%  ·  TP OTHER SIDE", "แบ่งกำไรที่ 50%  ·  TP อีกฝั่ง", GOLD)]
    rows(s, items, [K(f"c{k}") for k in range(1, 6)], y0=600, dy=140, size=30)
    for k in range(5):
        ck = check(s, 975, 600 + 140 * k, 18, GREEN, 5); s.draw(ck, K(f"c{k + 1}") + 0.6, 0.3)

    o3, c3 = K("miss") - 0.1, K("order") - 0.05
    s = S(o3, c3)
    tagc(s, 5)
    a = s.label(540, 780, L("MISS ONE STEP", "ขาดข้อไหนไป"), 64, WHITE, 0, 800, 0.04); s.pop(a, o3 + 0.2, 0.4, 0.6)
    b = s.label(540, 900, L("NO TRADE", "ไม่มีเทรด"), 90, RED, 0, 800, 0.06); s.pop(b, FW("miss", "no", "ไม่มี", 1.0), 0.4, 0.6)
    cue(FW("miss", "no", "ไม่มี", 1.0), "bell_A4", -20)
    outro(K("order") - 0.05)
