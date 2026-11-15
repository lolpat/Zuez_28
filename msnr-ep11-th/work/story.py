"""Scenes for the MSNR series v2, part 2 (episodes 7-11): storyline, fresh & unfresh, rejection & breakout, the four
timeframes, and the false-breakout mistake + summary. English and Thai from the same code (LANG in work/gen.py).
Drawings and example charts are original illustrations (synthetic), candles up #2962ff, down white."""
from otm import *
from msnr import nx, ny, diagram, title_block, flow_card, KW



def FW(key, en, th, off=0.0, span=60):
    """time of the first word at/after mark `key` containing `en` (English) or `th` (Thai); falls back to K(key)+off"""
    sub = (th if TH() else en).lower()
    i0 = G["marks"][key]
    ws = G["words"]
    for i in range(i0, min(len(ws), i0 + span)):
        acc = ""
        for j in range(i, min(len(ws), i + 6)):     # Thai words can be split: match across a short joined window
            acc += ws[j]["word"].strip().lower()
            if sub in acc:
                return W(j if sub in ws[j]["word"].lower() else i)
    print("FW fallback", key, sub)
    return K(key, off)


def tag(s, n):
    return s.label(540, 300, L(f"MSNR STORYLINE  ·  {n}/5", f"MSNR สตอรี่ไลน์  ·  {n}/5"), 26, GOLD, 1, 700, 0.2)


def next_card(o, c, n, en, th):
    s = S(o, c)
    a = s.label(540, 760, L(f"NEXT  ·  {n}/5", f"ตอนต่อไป  ·  {n}/5"), 30, GREY, 0, 700, 0.2); s.fade(a, o + 0.1)
    b = s.label(540, 900, L(en, th), 72, GOLD, 0, 800, 0.04); s.pop(b, o + 0.5, 0.4, 0.6)
    cue(o + 0.2, "whoosh-long_1", -22)


def rows(s, items, times, y0=640, dy=130, mark="num", col_mark=RED, size=34):
    """numbered / crossed rows: items [(en, th, col)]"""
    for k, ((en, th, col), t) in enumerate(zip(items, times)):
        yy = y0 + dy * k
        g = f'<g id="@ID@" style="opacity:0"><rect x="70" y="{yy - 50}" width="940" height="100" rx="22" fill="#ffffff" fill-opacity="0.05" stroke="#ffffff" stroke-opacity="0.15" stroke-width="2"/>'
        if mark == "num":
            g += f'<circle cx="130" cy="{yy}" r="30" fill="{GOLD}"/><text x="130" y="{yy + 12}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="32" fill="#111">{k + 1}</text>'
        else:
            g += f'<path d="M 112 {yy - 18} L 148 {yy + 18} M 148 {yy - 18} L 112 {yy + 18}" stroke="{col_mark}" stroke-width="7" stroke-linecap="round"/>'
        fam = "Kanit" if TH() else "Montserrat"
        g += f'<text x="185" y="{yy + 12}" font-family="{fam}" font-weight="{700 if TH() else 800}" font-size="{size + (3 if TH() else 0)}" letter-spacing="{0 if TH() else 0.02}em" fill="{col}">{L(en, th)}</text></g>'
        i = s.raw(g, "rw"); s.fade(i, t, 0.35, y=14)
        cue(t, ["tick-crisp_1", "tick-crisp_2", "tick-crisp_3"][k % 3], -20)


def panel(s, x0, y0, w, h, op=0):
    return s.raw(f'<rect id="@ID@" x="{x0}" y="{y0}" width="{w}" height="{h}" rx="20" fill="#ffffff" fill-opacity="0.04" stroke="#ffffff" stroke-opacity="0.22" stroke-width="2" style="opacity:{op}"/>', "pn")


def mini(s, candles, x0, y0, w, h, pmin=0, pmax=100, pad=1, op=0):
    ch = Chart(candles, len(candles) + pad, x0 + 20, x0 + w - 20, y0 + 30, y0 + h - 30, pmin, pmax, 0.62)
    g = s.raw(f'<g id="@ID@" style="opacity:{op}">' + ch.candles() + "</g>", "mc")
    return ch, g


def seg_path(s, pts, col=WHITE, w=6, dash=None):
    d = "M " + " L ".join(f"{nx(u):.1f} {ny(v):.1f}" for u, v in pts)
    st = "filter:drop-shadow(0 0 8px rgba(255,255,255,0.3));" + (f"stroke-dasharray:{dash};" if dash else "")
    return s.path(d, col, w, drawn=bool(dash), style=st + ("opacity:0;" if dash else ""))


# ======================================================================================================== episode 7
def ep7():
    o1, c1 = 0, K("seq") - 0.1
    s = S(o1, c1, first=True)
    tag(s, 1)
    title_block(s, L("STORYLINE", "สตอรี่ไลน์"), L("READ THE STORY FIRST", "อ่านเรื่องราวก่อน"))
    pts = [(0.0, 0.25), (0.14, 0.55), (0.24, 0.42), (0.44, 0.78), (0.56, 0.6)]
    diagram(s, pts, K("hook") + 0.3, 1.6)
    proj = seg_path(s, [(0.56, 0.6), (0.82, 0.9)], GOLD, 5, "14 10"); s.fade(proj, K("q3"), 0.4)
    for (u, v, en, th, key, dy) in [(0.0, 0.25, "WHERE FROM?", "มาจากไหน?", "q1", 60), (0.56, 0.6, "WHERE NOW?", "ตอนนี้อยู่ไหน?", "q2", 70),
                                    (0.82, 0.9, "WHERE NEXT?", "ไปไหนต่อ?", "q3", -50)]:
        r = ring(s, nx(u), ny(v), 16, GOLD); s.pop(r, K(key), 0.35, 0.3)
        p = s.pill(min(max(nx(u), 180), 900), ny(v) + dy, L(en, th), GOLD, "#111", 26); s.pop(p, K(key) + 0.1, 0.35, 0.5)
        cue(K(key), "bell_C5", -24)
    captions(s, [(0.1, L("BEFORE ANY ENTRY: THE STORYLINE", "ก่อนเข้าออเดอร์: สตอรี่ไลน์"), WHITE)], c1)

    o2, c2 = K("seq") - 0.1, K("rules") - 0.1
    s = S(o2, c2)
    tag(s, 1)
    s.label(540, 470, L("A SEQUENCE OF EVENTS", "ลำดับของเหตุการณ์"), 46, WHITE, 1, 800, 0.04)
    segs = [([(0.0, 0.15), (0.28, 0.72)], WHITE, "s1", "PUSH", "แรงดัน", (0.1, 0.52)),
            ([(0.28, 0.72), (0.34, 0.64), (0.4, 0.72), (0.46, 0.65)], WHITE, "s2", "PAUSE", "พักตัว", (0.37, 0.86)),
            ([(0.46, 0.65), (0.6, 0.42)], WHITE, "s3", "REACTION", "ตอบสนอง", (0.6, 0.3)),
            ([(0.6, 0.42), (0.9, 0.92)], LBLUE, "s4", "CONTINUATION", "ไปต่อ", (0.82, 0.98)),
            ([(0.6, 0.42), (0.9, 0.05)], RED, "s4", "REVERSAL", "กลับตัว", (0.82, -0.04))]
    for k, (pts, col, key, en, th, (lu, lv)) in enumerate(segs):
        p = seg_path(s, pts, col, 6); s.draw(p, K(key) + (0.3 if k == 4 else 0), 0.5)
        lb = s.label(nx(lu), ny(lv), L(en, th), 30, col if col != WHITE else GOLD, 0, 800, 0.08); s.fade(lb, K(key) + 0.3 + (0.3 if k == 4 else 0))
        cue(K(key), "tick-crisp_" + str(k % 3 + 1), -22)
    captions(s, [(o2 + 0.1, L("PUSH · PAUSE · REACTION · NEXT", "ดัน · พัก · ตอบสนอง · ต่อไป"), WHITE)], c2)

    o3, c3 = K("rules") - 0.1, K("ex") - 0.1
    s = S(o3, c3)
    tag(s, 1)
    s.label(540, 480, L("THE STORYLINE STARTS", "สตอรี่ไลน์เริ่มต้นเมื่อ"), 46, WHITE, 1, 800, 0.04)
    rows(s, [("TAP A FRESH LEVEL", "แตะระดับที่ยังสด", WHITE), ("REJECT: WICK + CLOSED CANDLE", "ปฏิเสธ: ไส้ + แท่งปิดแล้ว", WHITE),
             ("ONE TF LOWER: BREAKOUT", "TF เล็กลงหนึ่งขั้น: เบรก", GOLD)], [K("r1"), K("r2"), K("r3")], y0=660, dy=150, size=32)

    o4, c4 = K("ex") - 0.1, K("quote") - 0.1
    s = S(o4, c4)
    tag(s, 1)
    hp = s.pill(540, 470, L("DAILY CHART  ·  XAUUSD", "กราฟรายวัน  ·  XAUUSD"), WHITE, "#0b0b0b", 26); s.pop(hp, o4 + 0.2, 0.4, 0.5)
    C = path_candles([(0, 22), (3, 40), (5, 34), (8, 55), (10, 48), (13, 70), (15, 84), (18, 58), (21, 34), (22, 30)], seed=7, noise=1.6, wick=1.6)
    C[22] = (32, 33, 21.6, 31.5)
    ch = Chart(C, 33, 90, 1000, 640, 1230, 10, 95, 0.64)
    lv = hline(s, ch, 22, 0, 32, GOLD, 4, "14 9"); s.fade(lv, o4 + 0.4, 0.4)
    lt = s.label(ch.x(32), ch.y(22) + 36, L("DAILY KEY · FRESH", "ระดับรายวัน · สด"), 24, GOLD, 0, 800, 0.08, "end"); s.fade(lt, o4 + 0.6)
    rid = candles_clip(s, ch)
    reveal(rid, ch, [(o4, -1), (o4 + 0.3, 12), (K("ex") + 1.8, 22)], o4)
    r = ring(s, ch.x(22), ch.y(21.6), 20, RED); s.pop(r, FW("ex", "rejected", "ปฏิเสธ", 1.4), 0.35, 0.3)
    rj = s.pill(ch.x(22) - 40, ch.y(12), L("DAILY REJECT", "รายวันปฏิเสธ"), RED, WHITE, 22); s.pop(rj, FW("ex", "rejected", "ปฏิเสธ", 1.4) + 0.1, 0.35, 0.5)
    # the 4H inset: waiting for the breakout
    p = panel(s, 720, 640, 270, 330); s.fade(p, K("ex2"), 0.4)
    it = s.label(855, 680, "4H", 26, GREY, 0, 800, 0.1); s.fade(it, K("ex2"))
    zz = s.path("M 750 900 L 790 840 L 820 870 L 860 800 L 890 830", WHITE, 4); s.draw(zz, K("ex2") + 0.2, 0.6)
    bl = s.raw('<line id="@ID@" x1="780" y1="800" x2="975" y2="800" stroke="#7d9bff" stroke-width="3" style="opacity:0"/>', "bl"); s.fade(bl, K("ex2") + 0.6, 0.3)
    aa = s.path("M 890 830 L 950 720", LBLUE, 4, style="stroke-dasharray:10 8;"); s.draw(aa, K("ex2") + 0.9, 0.5)
    bt = s.label(855, 940, L("BREAKOUT?", "เบรก?"), 26, LBLUE, 0, 800, 0.08); s.fade(bt, K("ex2") + 1.0)
    cue(K("ex2"), "whoosh-short_2", -22)
    captions(s, [(o4 + 0.1, L("THE DAILY REJECTS A FRESH LEVEL", "รายวันปฏิเสธระดับที่ยังสด"), RED), (K("ex2") - 0.1, L("WAIT FOR THE 4H BREAKOUT", "รอการเบรกบน 4H"), LBLUE)], c4)

    o5, c5 = K("quote") - 0.1, K("next") - 0.1
    s = S(o5, c5)
    tag(s, 1)
    q1 = s.label(540, 820, L("“WHERE ONE STORYLINE ENDS,", "“ที่ไหนที่สตอรี่ไลน์หนึ่งจบ"), 44, WHITE, 0, 800, 0.02); s.fade(q1, o5 + 0.2, 0.5, y=10)
    q2 = s.label(540, 900, L("THE OPPOSITE ONE BEGINS.”", "ฝั่งตรงข้ามจะเริ่มต้น”"), 44, GOLD, 0, 800, 0.02); s.fade(q2, FW("quote", "opposite", "ฝั่ง", 1.4), 0.5, y=10)
    cue(o5 + 0.2, "swell_2", -22)
    next_card(K("next") - 0.1, G["TOTAL"], 2, "FRESH & UNFRESH", "สด และ ไม่สด")


# ======================================================================================================== episode 8
def ep8():
    o1, c1 = 0, K("fresh") - 0.1
    s = S(o1, c1, first=True)
    tag(s, 2)
    title_block(s, L("FRESH & UNFRESH", "สด และ ไม่สด"), L("EVERY LEVEL HAS A STATUS", "ทุกระดับมีสถานะ"))
    for k, (en, th, col) in enumerate([("FRESH", "สด", GREEN), ("UNFRESH", "ไม่สด", RED), ("FINISHED", "จบแล้ว", GREY)]):
        s.pill(250 + 290 * k, 800, L(en, th), col, "#111" if col != RED else WHITE, 34, 1)
    captions(s, [(0.1, L("FRESH OR UNFRESH?", "สด หรือ ไม่สด?"), WHITE)], c1)

    o2, c2 = K("fresh") - 0.1, K("first") - 0.1
    s = S(o2, c2)
    tag(s, 2)
    P = [(60, 450, 460, 400), (560, 450, 460, 400), (60, 900, 460, 400), (560, 900, 460, 400)]
    base = [(40, 78, 38, 76), (76, 80, 50, 52), (52, 54, 40, 42)]
    sets = [base + [(42, 44, 30, 32), (32, 36, 25, 28), (28, 30, 20, 22)],
            base + [(42, 60, 40, 58), (58, 77.5, 56, 60), (60, 62, 40, 42)],
            base + [(42, 60, 40, 58), (58, 90, 56, 88), (88, 94, 80, 90)],
            base + [(42, 77.6, 40, 60), (60, 62, 45, 50), (50, 77.4, 48, 62), (62, 64, 28, 32)]]
    info = [("fresh", "FRESH", "สด", GREEN, "FULL STRENGTH", "แรงเต็มที่", []),
            ("wick", "UNFRESH", "ไม่สด", RED, "WICK TOUCH: USED ONCE", "ไส้แตะ: ใช้ไปหนึ่งครั้ง", [(4, 77.5)]),
            ("body", "FRESH AGAIN", "กลับมาสด", GREEN, "BODY BREAK: STARTS OVER", "เนื้อเทียนเบรก: เริ่มใหม่", []),
            ("twice", "FINISHED", "จบแล้ว", GREY, "USED TWICE", "ใช้ไปสองครั้ง", [(3, 77.6), (5, 77.4)])]
    for k, ((x0, y0, w, h), cs, (key, en, th, col, sen, sth, dots)) in enumerate(zip(P, sets, info)):
        t = K(key)
        pn = panel(s, x0, y0, w, h); s.fade(pn, t, 0.3)
        ch, g = mini(s, cs, x0 + 10, y0 + 60, w - 120, h - 140, 10, 100, 1); s.fade(g, t + 0.1, 0.3)
        ln = s.raw(f'<line id="@ID@" x1="{ch.x(0) - 10:.1f}" y1="{ch.y(76):.1f}" x2="{x0 + w - 20}" y2="{ch.y(76):.1f}" stroke="{GOLD}" stroke-width="3" style="opacity:0"/>', "ln")
        s.fade(ln, t + 0.2, 0.3)
        for (i, p) in dots:
            d = s.raw(f'<circle id="@ID@" cx="{ch.x(i):.1f}" cy="{ch.y(p):.1f}" r="11" fill="{RED}" style="opacity:0"/>', "d"); s.pop(d, t + 0.5, 0.3, 0.3)
        pl = s.pill(x0 + w / 2, y0 + 40, L(en, th), col, "#111" if col != RED else WHITE, 24); s.pop(pl, t + 0.3, 0.35, 0.5)
        sl = s.label(x0 + w / 2, y0 + h - 22, L(sen, sth), 21, LBL, 0, 700, 0.04); s.fade(sl, t + 0.5)
        if key == "twice":
            out(ln, t + 1.6, 0.5, 0.25)
        cue(t + 0.3, ["bell_G4", "tock_1", "bell_E5", "tock_1"][k], -22)
    captions(s, [(K("fresh") - 0.1, L("FRESH UNTIL PRICE TOUCHES IT", "สด จนกว่าราคาจะมาแตะ"), GREEN),
                 (K("wick") - 0.1, L("A WICK TOUCH: UNFRESH", "ไส้แตะ: ไม่สด"), RED),
                 (K("body") - 0.1, L("A BODY BREAK: FRESH AGAIN", "เนื้อเทียนเบรก: สดอีกครั้ง"), GREEN),
                 (K("twice") - 0.1, L("USED TWICE: FINISHED", "ใช้สองครั้ง: จบ"), GREY)], c2, 1395, 30)

    o3, c3 = K("first") - 0.1, K("next") - 0.1
    s = S(o3, c3)
    tag(s, 2)
    a = s.label(540, 760, L("CHECK THE STATUS", "เช็กสถานะ"), 66, WHITE, 0, 800, 0.04); s.pop(a, o3 + 0.2, 0.4, 0.6)
    b = s.label(540, 850, L("BEFORE YOU PLAN THE TRADE", "ก่อนวางแผนเทรด"), 38, GOLD, 0, 800, 0.06); s.fade(b, o3 + 0.6, 0.4, y=10)
    cue(o3 + 0.2, "bell_A4", -20)
    next_card(K("next") - 0.1, G["TOTAL"], 3, "REJECTION & BREAKOUT", "ปฏิเสธ และ เบรก")


# ======================================================================================================== episode 9
def ep9():
    o1, c1 = 0, K("rej") - 0.1
    s = S(o1, c1, first=True)
    tag(s, 3)
    title_block(s, L("REJECT OR BREAK", "ปฏิเสธ หรือ เบรก"), L("BOTH NEED CONFIRMATION", "ทั้งคู่ต้องมีการยืนยัน"))
    lv = s.raw(f'<line id="@ID@" x1="{nx(0.05):.1f}" y1="{ny(0.55):.1f}" x2="{nx(1):.1f}" y2="{ny(0.55):.1f}" stroke="{GOLD}" stroke-width="5" stroke-dasharray="16 10"/>', "lv")
    a = seg_path(s, [(0.05, 0.12), (0.45, 0.55), (0.7, 0.1)], WHITE, 6); s.draw(a, 0.4, 1.2)
    b = seg_path(s, [(0.45, 0.55), (0.62, 0.62), (0.95, 0.95)], LBLUE, 6); s.draw(b, FW("hook", "break", "เบรก", 1.6), 0.8)
    la = s.label(nx(0.72), ny(0.06), L("REJECT", "ปฏิเสธ"), 30, WHITE, 0, 800, 0.08); s.fade(la, 1.2)
    lb_ = s.label(nx(0.9), ny(0.98), L("BREAK", "เบรก"), 30, LBLUE, 0, 800, 0.08); s.fade(lb_, FW("hook", "break", "เบรก", 1.6) + 0.6)
    captions(s, [(0.1, L("AT A LEVEL: TWO OUTCOMES", "ที่ระดับราคา: เป็นไปได้สองแบบ"), WHITE)], c1)

    o2, c2 = K("rej") - 0.1, K("brk") - 0.1
    s = S(o2, c2)
    tag(s, 3)
    s.label(540, 470, L("REJECTION = “NOT HERE”", "ปฏิเสธ = “ไม่ใช่ตรงนี้”"), 46, WHITE, 1, 800, 0.03)
    P = [(60, 560, 460, 360), (560, 560, 460, 360), (60, 950, 460, 360), (560, 950, 460, 360)]
    sets = [[(30, 34, 26, 32), (32, 36, 28, 30), (30, 92, 28, 36)],
            [(40, 44, 30, 32), (32, 62, 30, 60), (60, 64, 18, 22)],
            [(40, 64, 38, 62), (62, 63, 44, 46), (46, 47, 28, 30), (30, 31, 12, 14)],
            None]
    lab = [("g1", "LONG WICK", "ไส้เทียนยาว"), ("g2", "ENGULFING", "แท่งกลืนกิน"), ("g3", "DISPLACEMENT", "แรงผลักแรง"), ("g4", "LTF SHIFT", "TF เล็กเปลี่ยนโครงสร้าง")]
    for k, ((x0, y0, w, h), cs, (key, en, th)) in enumerate(zip(P, sets, lab)):
        t = K(key)
        pn = panel(s, x0, y0, w, h); s.fade(pn, t, 0.3)
        if cs:
            ch, g = mini(s, cs, x0 + 100, y0 + 30, w - 200, h - 90, 0, 100, 0); s.fade(g, t + 0.1, 0.3)
        else:
            zz = s.path(f"M {x0 + 40} {y0 + 90} L {x0 + 120} {y0 + 210} L {x0 + 180} {y0 + 160} L {x0 + 250} {y0 + 270} L {x0 + 320} {y0 + 150} L {x0 + 400} {y0 + 60}", WHITE, 4)
            s.draw(zz, t + 0.1, 0.6)
            ms = s.raw(f'<line id="@ID@" x1="{x0 + 170}" y1="{y0 + 160}" x2="{x0 + 360}" y2="{y0 + 160}" stroke="{LBLUE}" stroke-width="3" style="opacity:0"/>', "ms"); s.fade(ms, t + 0.6, 0.3)
            mt = s.label(x0 + 380, y0 + 150, "MSS", 22, LBLUE, 0, 800, 0.08, "start"); s.fade(mt, t + 0.7)
        lb = s.label(x0 + w / 2, y0 + h - 18, L(en, th), 28, GOLD, 0, 800, 0.06); s.fade(lb, t + 0.2)
        cue(t, ["tick-crisp_1", "tick-crisp_2", "tick-crisp_3", "tick-crisp_1"][k], -20)
    captions(s, [(K("rej") - 0.1, L("THE MARKET SAYS: NOT HERE", "ตลาดบอกว่า: ไม่ใช่ตรงนี้"), WHITE)], c2, 1395, 30)

    o3, c3 = K("brk") - 0.1, K("next") - 0.1
    s = S(o3, c3)
    tag(s, 3)
    s.label(540, 470, L("A REAL BREAKOUT", "การเบรกจริง"), 52, WHITE, 1, 800, 0.03)
    C = path_candles([(0, 30), (3, 59.5), (6, 40), (9, 59.7), (12, 47), (15, 59.6), (17, 52), (19, 59), (20, 54), (21, 58.5), (22, 56)], seed=3, noise=1.4, wick=1.2)
    C += [(56, 82, 55, 80), (80, 86, 77, 84)]
    ch = Chart(C, len(C) + 2, 100, 980, 560, 1000, 20, 92, 0.64)
    lv = hline(s, ch, 60, 0, len(C) + 1, GOLD, 4, "14 9", 1)
    rid = candles_clip(s, ch)
    reveal(rid, ch, [(o3, -1), (o3 + 0.3, 16), (K("b1") - 0.3, 22), (K("b1") + 0.3, len(C) - 1)], o3)
    for k, i in enumerate((3, 9, 15)):
        r = ring(s, ch.x(i), ch.y(60), 16, WHITE); s.pop(r, K("b2") + 0.15 * k, 0.3, 0.3)
    sq = rbox(s, ch.x(16) - 10, ch.y(61), ch.x(22) + 10, ch.y(50), LBLUE, 0.15, 0.9, 2); s.fade(sq, K("b3"), 0.4)
    bc = rbox(s, ch.x(23) - 22, ch.y(84), ch.x(23) + 22, ch.y(54), GREEN, 0.0, 1, 4); s.fade(bc, K("b1") + 0.3, 0.3)
    rows(s, [("CLOSES BEYOND THE LEVEL", "ปิดเลยระดับ", WHITE), ("HIT MANY TIMES BEFORE", "เคยถูกแตะหลายครั้ง", WHITE),
             ("SQUEEZED TIGHT FIRST", "บีบตัวแคบก่อนเบรก", WHITE)], [K("b1"), K("b2"), K("b3")], y0=1080, dy=110, size=30)
    captions(s, [(o3 + 0.1, L("DECISIVE: THROUGH THE LEVEL", "ผ่านระดับอย่างเด็ดขาด"), LBLUE)], K("b1") - 0.2, 1420, 28)
    next_card(K("next") - 0.1, G["TOTAL"], 4, "4 TIMEFRAMES", "4 ไทม์เฟรม")


# ======================================================================================================== episode 10
def ep10():
    o1, c1 = 0, K("x1") - 0.1
    s = S(o1, c1, first=True)
    tag(s, 4)
    title_block(s, L("4 TIMEFRAMES", "4 ไทม์เฟรม"), "X1  ·  X2  ·  X3  ·  X4")
    for k in range(4):
        p = s.pill(195 + 230 * k, 780, f"X{k + 1}", [GOLD, WHITE, WHITE, GREY][k], "#111", 40, 1)
    captions(s, [(0.1, L("ONE STORYLINE, FOUR TIMEFRAMES", "หนึ่งสตอรี่ไลน์ สี่ไทม์เฟรม"), WHITE)], c1)

    o2, c2 = K("x1") - 0.1, K("ex") - 0.1
    s = S(o2, c2)
    tag(s, 4)
    R = [("X1", "MN · W · D", ("FRESH LEVEL + REJECTION", "ระดับสด + การปฏิเสธ"), GOLD),
         ("X2", "W · D · 4H", ("BREAKOUT + ENTRY LEVEL", "เบรก + ระดับจุดเข้า"), WHITE),
         ("X3", "D · 4H · 1H", ("REFINE + SETUP", "ปรับระดับ + เซ็ตอัพ"), WHITE),
         ("X4", "4H · 1H · 15M · 5M", ("CONFIRMATION (OPTIONAL)", "ยืนยัน (ไม่บังคับ)"), GREY)]
    for k, (x, tf, job, col) in enumerate(R):
        t = K(f"x{k + 1}"); yy = 560 + 190 * k
        bx = s.raw(f'<rect id="@ID@" x="60" y="{yy - 70}" width="960" height="160" rx="24" fill="#ffffff" fill-opacity="0.05" stroke="{col}" stroke-opacity="0.5" stroke-width="2" style="opacity:0"/>', "bx")
        s.fade(bx, t, 0.3)
        p = s.pill(150, yy + 10, x, col, "#111", 40); s.pop(p, t + 0.05, 0.35, 0.5)
        a = s.label(250, yy - 10, tf, 30, GREY, 0, 700, 0.06, "start"); s.fade(a, t + 0.15)
        b = s.label(250, yy + 46, L(*job), 34, col if col != GREY else LBL, 0, 800, 0.03, "start"); s.fade(b, t + 0.25)
        cue(t, ["bell_G4", "bell_C5", "bell_E5", "tick-crisp_1"][k], -22)
    captions(s, [(K("x4") + 0.8, L("X4 NEVER DECIDES THE DIRECTION", "X4 ไม่เคยกำหนดทิศทาง"), GOLD)], c2, 1395, 30)

    o3, c3 = K("ex") - 0.1, K("limit") - 0.1
    s = S(o3, c3)
    tag(s, 4)
    hp = s.pill(540, 470, L("XAUUSD  ·  EXAMPLE", "XAUUSD  ·  ตัวอย่าง"), WHITE, "#0b0b0b", 26); s.pop(hp, o3 + 0.2, 0.4, 0.5)
    cols = [(40, "X1 · WEEKLY", "X1 · รายสัปดาห์", ("weekly", "สัปดาห์", 0.8)), (380, "X2 · DAILY", "X2 · รายวัน", ("daily", "รายวัน", 2.0)),
            (720, "X3 · 4H", "X3 · 4H", ("four", "สี่", 3.2))]
    for k, (x0, en, th, tok) in enumerate(cols):
        t = FW("ex", *tok)
        pn = panel(s, x0, 560, 320, 640); s.fade(pn, t, 0.3)
        lb = s.label(x0 + 160, 610, L(en, th), 26, GOLD, 0, 800, 0.06); s.fade(lb, t + 0.1)
        if k == 0:
            c1_ = big_candle(s, x0 + 110, 60, 800, 1060, 820, 1110, 0, UP)
            c2_ = big_candle(s, x0 + 210, 60, 740, 820, 1040, 1090, 0, DOWN)
            for i in (c1_, c2_): s.fade(i, t + 0.2, 0.3)
            ln = s.raw(f'<line id="@ID@" x1="{x0 + 60}" y1="740" x2="{x0 + 300}" y2="740" stroke="{GOLD}" stroke-width="3" style="opacity:0"/>', "ln"); s.fade(ln, t + 0.4, 0.3)
            d = s.raw(f'<circle id="@ID@" cx="{x0 + 210}" cy="740" r="12" fill="{RED}" style="opacity:0"/>', "d"); s.pop(d, t + 0.6, 0.3, 0.3)
            tx = s.label(x0 + 160, 1170, L("REJECT", "ปฏิเสธ"), 28, RED, 0, 800, 0.08); s.fade(tx, t + 0.6)
        elif k == 1:
            ch, g = mini(s, path_candles([(0, 70), (3, 80), (6, 60), (8, 66), (11, 30), (13, 36), (15, 22)], seed=2, noise=2, wick=2), x0 + 10, 660, 300, 460, 10, 95, 1)
            s.fade(g, t + 0.2, 0.4)
            ln = s.raw(f'<line id="@ID@" x1="{x0 + 30}" y1="{ch.y(60):.1f}" x2="{x0 + 300}" y2="{ch.y(60):.1f}" stroke="{GOLD}" stroke-width="3" style="opacity:0"/>', "ln"); s.fade(ln, t + 0.4, 0.3)
            tx = s.label(x0 + 160, 1170, L("BREAKOUT", "เบรก"), 28, LBLUE, 0, 800, 0.08); s.fade(tx, t + 0.6)
        else:
            ch, g = mini(s, path_candles([(0, 30), (3, 62), (5, 50), (7, 66), (10, 40), (12, 46), (16, 18)], seed=4, noise=2, wick=2), x0 + 10, 660, 300, 460, 10, 95, 1)
            s.fade(g, t + 0.2, 0.4)
            ln = s.raw(f'<line id="@ID@" x1="{x0 + 30}" y1="{ch.y(64):.1f}" x2="{x0 + 300}" y2="{ch.y(64):.1f}" stroke="{GOLD}" stroke-width="3" style="opacity:0"/>', "ln"); s.fade(ln, t + 0.4, 0.3)
            en_ = s.pill(x0 + 160, ch.y(64) - 34, L("ENTRY", "จุดเข้า"), RED, WHITE, 20); s.pop(en_, t + 0.6, 0.35, 0.5)
            lq = s.raw(f'<line id="@ID@" x1="{x0 + 30}" y1="{ch.y(16):.1f}" x2="{x0 + 300}" y2="{ch.y(16):.1f}" stroke="{RED}" stroke-width="3" stroke-dasharray="8 6" style="opacity:0"/>', "lq")
            s.fade(lq, K("ex2"), 0.3)
            tx = s.label(x0 + 160, 1170, L("TO LIQUIDITY", "ไปหาลิควิดิตี้"), 26, RED, 0, 800, 0.06); s.fade(tx, K("ex2") + 0.2)
        cue(t, ["bell_G4", "bell_C5", "bell_E5"][k], -22)
        if k < 2:
            ar = s.path(f"M {x0 + 330} 880 L {x0 + 370} 880 M {x0 + 356} 868 L {x0 + 370} 880 L {x0 + 356} 892", GOLD, 4, drawn=True, style="opacity:0")
            s.fade(ar, t + 0.8, 0.3)
    captions(s, [(o3 + 0.1, L("WEEKLY · DAILY · 4H", "รายสัปดาห์ · รายวัน · 4H"), WHITE), (K("ex2") - 0.1, L("THEN THE RUN TO LIQUIDITY", "แล้ววิ่งไปหาลิควิดิตี้"), RED)], c3)

    o4, c4 = K("limit") - 0.1, K("next") - 0.1
    s = S(o4, c4)
    tag(s, 4)
    for k in range(3):
        p = s.pill(240 + 300 * k, 760, f"X{k + 1}", GOLD if k == 0 else WHITE, "#111", 44); s.pop(p, o4 + 0.3 + 0.3 * k, 0.35, 0.5)
        if k < 2:
            pl = s.label(390 + 300 * k, 778, "+", 52, GREY, 0, 800, 0); s.fade(pl, o4 + 0.4 + 0.3 * k)
    eq = s.label(540, 940, L("= LIMIT ORDER AT X3", "= ตั้งลิมิตที่ X3"), 54, GOLD, 0, 800, 0.03); s.pop(eq, FW("limit", "limit", "ลิมิต", 2.0), 0.4, 0.6)
    cue(FW("limit", "limit", "ลิมิต", 2.0), "bell_A4", -20)
    next_card(K("next") - 0.1, G["TOTAL"], 5, "THE MISTAKE", "ความผิดพลาด")


# ======================================================================================================== episode 11
def ep11():
    o1, c1 = 0, K("trap") - 0.1
    s = S(o1, c1, first=True)
    tag(s, 5)
    title_block(s, L("THE MISTAKE", "ความผิดพลาด"), L("FALSE BREAKOUTS", "การเบรกหลอก"))
    captions(s, [(0.1, L("A REJECTION, THEN A FAKE BREAK", "ปฏิเสธ แล้วตามด้วยเบรกหลอก"), RED)], c1)
    xm = xmark(s, 540, 860, 90, RED, 12); s.draw(xm, 0.6, 0.4)

    o2, c2 = K("trap") - 0.1, K("sum") - 0.1
    s = S(o2, c2)
    tag(s, 5)
    KL, BL = 0.85, 0.55
    kl = s.raw(f'<line id="@ID@" x1="{nx(0.05):.1f}" y1="{ny(KL):.1f}" x2="{nx(0.98):.1f}" y2="{ny(KL):.1f}" stroke="{GOLD}" stroke-width="4" style="opacity:0"/>', "kl")
    s.fade(kl, o2 + 0.2, 0.4)
    klt = s.label(nx(0.98), ny(KL) - 16, L("X1 KEY LEVEL", "ระดับ X1"), 24, GOLD, 0, 800, 0.08, "end"); s.fade(klt, o2 + 0.3)
    pre = seg_path(s, [(0.02, 0.35), (0.12, 0.62), (0.16, 0.56)], WHITE, 5); s.draw(pre, o2 + 0.3, 0.6)
    bc = big_candle(s, nx(0.22), 46, ny(0.9), ny(0.7), ny(0.6), ny(BL), 0, DOWN); s.pop(bc, o2 + 0.8, 0.4, 0.4)
    path = [(0.27, 0.6), (0.35, 0.72), (0.44, 0.46), (0.52, 0.7), (0.6, 0.62)]
    p = seg_path(s, path, WHITE, 5); s.draw(p, K("trap") + 0.6, 1.8, "power1.inOut")
    fk = ring(s, nx(0.44), ny(0.46), 18, RED); s.pop(fk, K("fake"), 0.35, 0.3)
    fkt = s.pill(nx(0.44), ny(0.33), L("FAKE BREAKOUT", "เบรกหลอก"), RED, WHITE, 22); s.pop(fkt, K("fake") + 0.2, 0.35, 0.5)
    cue(K("fake"), "whoosh-short_1", -22)
    ft = ring(s, nx(0.22), ny(0.9), 18, GOLD); s.pop(ft, K("first"), 0.35, 0.3)
    ftt = s.pill(nx(0.22), ny(1.0), L("FIRST TAP", "แตะแรก"), GOLD, "#111", 22); s.pop(ftt, K("first") + 0.15, 0.35, 0.5)
    cue(K("first"), "bell_C5", -22)
    rb = s.raw(f'<line id="@ID@" x1="{nx(0.22):.1f}" y1="{ny(BL):.1f}" x2="{nx(0.98):.1f}" y2="{ny(BL):.1f}" stroke="{LBLUE}" stroke-width="4" stroke-dasharray="12 8" style="opacity:0"/>', "rb")
    s.fade(rb, K("first") + 0.6, 0.4)
    rbt = s.label(nx(0.98), ny(BL) + 40, L("REAL BREAKOUT LEVEL", "จุดที่ต้องเบรกจริง"), 22, LBLUE, 0, 800, 0.06, "end"); s.fade(rbt, K("first") + 0.8)
    up = arrow(s, nx(0.62), ny(0.64), nx(0.8), ny(0.8), GOLD, 4, 16); show_arrow(s, up, K("wait") + 0.4, 0.4)
    dn = arrow(s, nx(0.62), ny(0.6), nx(0.8), ny(0.2), LBLUE, 4, 16); show_arrow(s, dn, K("wait") + 0.6, 0.4)
    q = s.label(nx(0.88), ny(0.5) + 12, "?", 64, WHITE, 0, 800, 0); s.fade(q, K("wait") + 0.9)
    captions(s, [(K("trap") - 0.1, L("A WICK THROUGH IS NOT A BREAKOUT", "ไส้ทะลุ ไม่ใช่การเบรก"), RED), (K("fake") - 0.1, L("THE FIRST BREAK TRAPS TRADERS", "เบรกแรก ไว้ดักเทรดเดอร์"), RED),
                 (K("first") - 0.1, L("WHICH CANDLE TAPPED FIRST?", "แท่งไหนแตะก่อน?"), GOLD), (K("wait") - 0.1, L("WAIT, LET THE MARKET DECIDE", "รอ แล้วให้ตลาดตัดสินใจ"), LBLUE)], c2)

    o3, c3 = K("sum") - 0.1, K("rule") - 0.1
    s = S(o3, c3)
    tag(s, 5)
    s.label(540, 470, L("AVOID", "หลีกเลี่ยง"), 56, RED, 1, 800, 0.1)
    rows(s, [("TRADING UNFRESH LEVELS", "เทรดระดับที่ไม่สด", WHITE), ("ENTERING BEFORE THE REJECTION", "เข้าก่อนการปฏิเสธ", WHITE),
             ("CALLING EVERY WICK A BREAKOUT", "เรียกทุกไส้ว่าเบรก", WHITE), ("IGNORING THE HIGHER TIMEFRAME", "มองข้ามไทม์เฟรมใหญ่", WHITE),
             ("DRAWING TOO MANY LEVELS", "วาดเส้นเยอะเกินไป", WHITE)], [K(f"m{k}") for k in range(1, 6)], y0=600, dy=125, mark="x", size=30)

    o4, c4 = K("rule") - 0.1, K("order") - 0.05
    s = S(o4, c4)
    tag(s, 5)
    a = s.label(540, 760, L("FIND THE STORYLINE FIRST", "หาสตอรี่ไลน์ก่อน"), 50, WHITE, 0, 800, 0.03); s.pop(a, o4 + 0.2, 0.4, 0.6)
    b = s.label(540, 840, L("THEN THE SETUP", "แล้วค่อยหาเซ็ตอัพ"), 40, LBL, 0, 800, 0.06); s.fade(b, FW("rule", "then", "แล้ว", 1.2), 0.4, y=10)
    c_ = s.label(540, 980, L("NO STORYLINE, NO TRADE", "ไม่มีสตอรี่ไลน์ ไม่มีเทรด"), 54, GOLD, 0, 800, 0.03); s.pop(c_, FW("rule", "no", "ไม่มี", 2.4), 0.4, 0.6)
    cue(FW("rule", "no", "ไม่มี", 2.4), "bell_A4", -18)
    outro(K("order") - 0.05)
