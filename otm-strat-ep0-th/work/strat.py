"""Scenes for the OTM STRATEGIES series (otm-strat-epN, Thai otm-strat-epN-th, same file with LANG = "th").
Ep 0 maps every strategy the series covers (and the three jobs a strategy can do: WHERE / WHEN / ENTRY); ep 1..14
teach one each. Built on the CRT engine (work/otm.py). Original drawings and synthetic XAUUSD charts (candles up
#2962ff, down white, connected); example prices are illustrations, not a real trade. Thai visuals keep the trading
terms in English. Only the last episode ends on the Order the Market outro; the others end on the next-episode card."""
from otm import *
from msnr import title_block
from story import FW, panel, mini, pos_box, rows
from pro import hl

TOT = 14
CFG = dict(end0=True, start1=0.0, outro1=False)     # merged ep 0 + 1: end0=False, start1=<ep 1 start>, outro1=True
BLUEJ, GOLDJ, GREENJ = "#4f7bff", GOLD, GREEN          # job colours: WHERE / WHEN / ENTRY


def tag(s, n):
    txt = L("XAUUSD  ·  STRATEGIES  ·  START HERE", "XAUUSD  ·  STRATEGIES  ·  เริ่มที่นี่") if n == 0 else f"XAUUSD  ·  STRATEGIES  ·  EP {n}/{TOT}"
    return s.label(540, 300, txt, 26, GOLD, 1, 700, 0.2)


def next_ep(o, c, n, en, th, extra=None):
    s = S(o, c)
    a = s.label(540, 740, L(f"NEXT  ·  EP {n}/{TOT}", f"ตอนต่อไป  ·  EP {n}/{TOT}"), 30, GREY, 0, 700, 0.2); s.fade(a, o + 0.1)
    b = s.label(540, 880, L(en, th), 70, GOLD, 0, 800, 0.04); s.pop(b, o + 0.45, 0.4, 0.6)
    cue(o + 0.2, "whoosh-long_1", -22)
    return s


# ------------------------------------------------------------------------------------------- strategy icons (r ~ 50)
def icon(kind, x, y, col=WHITE):
    P = lambda d, w=4, c=col: f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
    def C(cx, top, bot, up=True, w=12):                 # a tiny candle body
        return f'<rect x="{cx - w / 2}" y="{top}" width="{w}" height="{bot - top}" fill="{UP if up else DOWN}"/>'
    X, Y = x, y
    if kind == "bos":
        return P(f"M {X-45} {Y+28} L {X-22} {Y-2} L {X-5} {Y+14} L {X+18} {Y-22} L {X+45} {Y-40}") + P(f"M {X-26} {Y-2} L {X+30} {Y-2}", 3, GOLD)
    if kind == "choch":
        return P(f"M {X-45} {Y-30} L {X-25} {Y+5} L {X-8} {Y-12} L {X+8} {Y+30} L {X+42} {Y-30}") + P(f"M {X-12} {Y-12} L {X+30} {Y-12}", 3, GOLD)
    if kind == "sweep":
        return P(f"M {X-45} {Y+12} L {X+45} {Y+12}", 3, GOLD) + C(X - 18, Y - 20, Y + 4, False) + f'<line x1="{X-18}" y1="{Y+4}" x2="{X-18}" y2="{Y+34}" stroke="#fff" stroke-width="3"/>' + C(X + 8, Y - 26, Y + 6, True) + C(X + 30, Y - 40, Y - 20, True)
    if kind == "sr":
        return P(f"M {X-45} {Y-26} L {X+45} {Y-26}", 3, GOLD) + P(f"M {X-45} {Y+26} L {X+45} {Y+26}", 3, GOLD) + P(f"M {X-40} {Y+24} L {X-22} {Y-24} L {X-4} {Y+24} L {X+14} {Y-24} L {X+34} {Y+24}")
    if kind == "sd":
        return f'<rect x="{X-45}" y="{Y+10}" width="90" height="22" fill="{GREEN}" fill-opacity="0.35"/><rect x="{X-45}" y="{Y-40}" width="90" height="20" fill="{RED}" fill-opacity="0.35"/>' + P(f"M {X-30} {Y-18} L {X-10} {Y+12} L {X+12} {Y-16} L {X+32} {Y+10}")
    if kind == "ob":
        return f'<rect x="{X-34}" y="{Y-2}" width="26" height="34" fill="none" stroke="{GOLD}" stroke-width="3"/>' + C(X - 21, Y + 2, Y + 28, False) + C(X + 2, Y - 18, Y + 20, True) + C(X + 22, Y - 40, Y - 12, True)
    if kind == "breaker":
        return f'<rect x="{X-40}" y="{Y-6}" width="80" height="20" fill="{GOLD}" fill-opacity="0.25" stroke="{GOLD}" stroke-width="2"/>' + P(f"M {X-40} {Y-36} L {X-14} {Y+32} L {X+10} {Y-2} L {X+40} {Y-38}")
    if kind == "fvg":
        return f'<rect x="{X-30}" y="{Y-12}" width="60" height="20" fill="{GREEN}" fill-opacity="0.3"/>' + C(X - 22, Y + 8, Y + 34, True) + C(X, Y - 30, Y + 22, True) + C(X + 22, Y - 42, Y - 12, True)
    if kind == "ifvg":
        return f'<rect x="{X-30}" y="{Y-12}" width="60" height="20" fill="{RED}" fill-opacity="0.35"/>' + C(X - 22, Y - 38, Y - 12, False) + C(X, Y - 24, Y + 30, False) + P(f"M {X+12} {Y+30} L {X+40} {Y-10}", 4, GOLD)
    if kind == "ote":
        return "".join(P(f"M {X-45} {Y+o} L {X+45} {Y+o}", 2, c) for o, c in ((-34, GREY), (6, GOLD), (18, GOLD), (36, GREY))) + P(f"M {X-40} {Y+36} L {X+20} {Y-34} L {X+38} {Y+12}")
    if kind == "breakout":
        return P(f"M {X-45} {Y-30} L {X+10} {Y-8}", 3, GOLD) + P(f"M {X-45} {Y+30} L {X+10} {Y+8}", 3, GOLD) + P(f"M {X-40} {Y+20} L {X-25} {Y-20} L {X-10} {Y+10} L {X+4} {Y-6} L {X+40} {Y-40}")
    if kind == "silver":
        return f'<circle cx="{X}" cy="{Y}" r="34" fill="none" stroke="#fff" stroke-width="4"/>' + P(f"M {X} {Y} L {X} {Y-22} M {X} {Y} L {X+16} {Y+8}", 4, GOLD)
    if kind == "po3":
        return P(f"M {X-45} {Y+4} L {X-30} {Y} L {X-18} {Y+6} L {X-6} {Y+2} L {X+4} {Y+34} L {X+20} {Y-10} L {X+44} {Y-40}") + f'<text x="{X+30}" y="{Y+34}" font-family="Montserrat" font-weight="800" font-size="18" fill="{GOLD}">AMD</text>'
    if kind == "crt":
        return f'<rect x="{X-38}" y="{Y-34}" width="22" height="62" fill="#fff"/>' + P(f"M {X-40} {Y-36} L {X+45} {Y-36} M {X-40} {Y+30} L {X+45} {Y+30}", 2, GOLD) + C(X + 6, Y + 10, Y + 26, True) + C(X + 28, Y - 30, Y + 12, True)
    if kind == "all":
        return f'<path d="M {X} {Y-38} L {X+11} {Y-12} L {X+40} {Y-12} L {X+17} {Y+6} L {X+26} {Y+34} L {X} {Y+18} L {X-26} {Y+34} L {X-17} {Y+6} L {X-40} {Y-12} L {X-11} {Y-12} Z" fill="{GOLD}"/>'
    return ""


# name (EN, TH), icon, job, keyword in [grid] (EN, TH)
GRID = [(("BOS", "BOS"), "bos", "when", ("structure", "structure")), (("CHoCH", "CHoCH"), "choch", "when", ("character", "character")),
        (("SWEEP", "SWEEP"), "sweep", "when", ("sweep", "sweep")), (("S & R", "S & R"), "sr", "where", ("support", "support")),
        (("SUPPLY / DEMAND", "SUPPLY / DEMAND"), "sd", "where", ("supply", "supply")),
        (("ORDER BLOCK", "ORDER BLOCK"), "ob", "where", ("order", "order")), (("BREAKER", "BREAKER"), "breaker", "where", ("breaker", "breaker")),
        (("FVG", "FVG"), "fvg", "entry", ("fair", "fair")), (("IFVG", "IFVG"), "ifvg", "entry", ("inverse", "inverse")),
        (("OTE", "OTE"), "ote", "entry", ("optimal", "optimal")), (("BREAKOUT", "BREAKOUT"), "breakout", "when", ("breakout", "breakout")),
        (("SILVER BULLET", "SILVER BULLET"), "silver", "when", ("silver", "silver")), (("POWER OF 3", "POWER OF 3"), "po3", None, ("power", "power")),
        (("CRT  ·  FULL SERIES", "CRT  ·  มีซีรีส์แล้ว"), "crt", None, None), (("ALL TOGETHER", "รวมทุกอย่าง"), "all", None, None)]


# ======================================================================================================== 0  the map
def ep0():
    o1, c1 = 0, K("series") - 0.1
    s = S(o1, c1, first=True)
    tag(s, 0)
    for k, (en, w, y) in enumerate((("FAIR VALUE GAP", "fair", 620), ("ORDER BLOCK", "order", 780), ("LIQUIDITY SWEEP", "sweep", 940))):
        p = s.pill(540, y, en, WHITE, "#0b0b0b", 40); s.pop(p, FW("hook", w, w) - 0.05, 0.35, 0.5)
        cue(FW("hook", w, w), "bell_C5", -26)
    rn = random.Random(5)
    names = ["BOS", "OTE", "IFVG", "S&D", "CRT", "BREAKER", "SILVER BULLET", "PO3", "CHoCH", "S&R"]
    for k, nm in enumerate(names):
        x, y = (rn.uniform(110, 250) if k % 2 else rn.uniform(830, 970)), rn.uniform(520, 1240)
        q = s.pill(x, y, nm, "#1b1e23", GREY, 22, 0, False)
        s.pop(q, K("lost") + 0.15 + 0.12 * k, 0.3, 0.4)
        tl(f'tl.to("#{q}", {{x: {rn.uniform(-120, 120):.0f}, y: {rn.uniform(-90, 90):.0f}, duration: 1.6, ease: "sine.inOut", yoyo: true, repeat: 1}}, {K("lost") + 0.3 + 0.12 * k:.3f});')
    captions(s, [(0.1, L("SO MANY STRATEGIES", "กลยุทธ์มีเยอะมาก"), WHITE), (K("lost") - 0.1, L("JUMPING AROUND = MASTER NONE", "กระโดดไปมา = ไม่เก่งสักอัน"), RED)], c1)

    o2, c2 = K("series") - 0.1, K("next") - 0.1
    s = S(o2, c2)
    tag(s, 0)
    tt = s.label(540, 450, L("ONE BY ONE  ·  ON GOLD", "ทีละอัน  ·  บนทองคำ"), 48, WHITE, 0, 800, 0.04); s.pop(tt, o2 + 0.2, 0.4, 0.6)
    out(tt, K("jobs") - 0.2, 0.25)
    xs, ys = [120 + 210 * k for k in range(5)], [640, 900, 1160]
    rings = {"where": [], "when": [], "entry": []}
    for k, ((en, th), ic, job, kw) in enumerate(GRID):
        x, y = xs[k % 5], ys[k // 5]
        t = FW("grid", kw[0], kw[1]) if kw else (K("grid") + 9.0 if k == 13 else K("last") + 0.2)
        if k == 13: t = FW("grid", "power", "power") + 0.9
        base = "#2a2e35" if ic != "all" else GOLD
        g = s.raw(f'<g id="@ID@" style="opacity:0"><circle cx="{x}" cy="{y}" r="82" fill="#0e1014" stroke="{base}" stroke-width="3"/>{icon(ic, x, y)}'
                  f'<text x="{x}" y="{y + 118}" text-anchor="middle" font-family="{"Kanit" if TH() and any(0x0E00 <= ord(ch) <= 0x0E7F for ch in th) else "Montserrat"}" '
                  f'font-weight="800" font-size="19" letter-spacing="0.04em" fill="{GOLD if ic in ("all", "crt") else LBL}">{L(en, th)}</text></g>', "gc")
        s.pop(g, t, 0.35, 0.5)
        if job:
            col = {"where": BLUEJ, "when": GOLDJ, "entry": GREENJ}[job]
            r = s.raw(f'<circle id="@ID@" cx="{x}" cy="{y}" r="86" fill="none" stroke="{col}" stroke-width="6" style="opacity:0;filter:drop-shadow(0 0 12px {col})"/>', "jr")
            rings[job].append(r)
    if True:
        sp = s.spot(xs[4], 0, "232,194,106", 30, 120, ys[2] + 90); s.fade(sp, K("last") + 0.2, 0.5)
    cue(K("last") + 0.2, "swell_2", -22)
    for k, (job, en, th, col) in enumerate((("where", "WHERE", "ที่ไหน", BLUEJ), ("when", "WHEN", "เมื่อไหร่", GOLDJ), ("entry", "ENTRY", "จุดเข้า", GREENJ))):
        t = K(job)
        p = s.pill(250 + 290 * k, 450, L(en, th), col, "#0b0b0b" if col != BLUEJ else "#fff", 34); s.pop(p, t, 0.35, 0.5)
        for r in rings[job]: s.fade(r, t + 0.1, 0.35)
        cue(t, "bell_G4", -22)
    captions(s, [(o2 + 0.1, L("THE SERIES  ·  ONE EPISODE EACH", "ซีรีส์นี้  ·  ตอนละหนึ่งกลยุทธ์"), WHITE),
                 (K("jobs") - 0.1, L("EVERY STRATEGY HAS ONE JOB", "ทุกกลยุทธ์ มีหน้าที่หนึ่งอย่าง"), GOLD),
                 (K("stack") - 0.1, L("ONE OF EACH = A CLEAN TRADE", "อย่างละหนึ่ง = เทรดที่คลีน"), GREEN),
                 (K("last") - 0.1, L("LAST EPISODE: ALL TOGETHER", "ตอนสุดท้าย: รวมทุกอย่าง"), GOLD)], c2, 1352 + 40)

    if not CFG["end0"]:
        return
    s = next_ep(K("next") - 0.1, G["TOTAL"], 1, "BREAK OF STRUCTURE", "BREAK OF STRUCTURE")
    sv = s.label(540, 1060, L("SAVE THE SERIES  ·  FOLLOW", "เซฟซีรีส์ไว้  ·  กดติดตาม"), 34, WHITE, 0, 800, 0.1); s.fade(sv, K("go") + 0.1, 0.4)
    cue(K("go") + 0.1, "swell_1", -24)


# ======================================================================================================== 1  BOS
def zig(s, pts, t, d, col=WHITE, w=6):
    p = s.path("M " + " L ".join(f"{x} {y}" for x, y in pts), col, w, style="filter:drop-shadow(0 0 8px rgba(255,255,255,0.3))")
    s.draw(p, t, d, "power1.inOut")
    return p


def ep1():
    # 1  title
    o, c = CFG["start1"], K("struct") - 0.1
    s = S(o, c, first=(o == 0))
    tag(s, 1)
    s.label(540, 450, "BREAK OF STRUCTURE", 64, WHITE, 1, 800, 0.03)
    s.label(540, 530, L("EP 1  ·  LEARN THIS ONE FIRST", "EP 1  ·  ต้องรู้อันนี้ก่อน"), 34, GOLD, 1, 700, 0.14)
    zig(s, [(160, 1150), (330, 900), (430, 1010), (620, 760), (720, 870), (930, 620)], o + 0.4, 1.6)
    l1 = hl(s, 330, 760, 900, GOLD, 4, "14 10"); s.fade(l1, o + 1.0, 0.3)
    l2 = hl(s, 620, 960, 760, GOLD, 4, "14 10"); s.fade(l2, o + 1.5, 0.3)
    for x, y, t in ((560, 885, 1.2), (850, 745, 1.7)):
        b = s.label(x, y, "BOS", 26, GOLD, 0, 800, 0.1); s.fade(b, o + t, 0.3)
    captions(s, [(o + 0.1, L("MOST STRATEGIES USE IT", "เกือบทุกกลยุทธ์ใช้มัน"), WHITE)], c)

    # 2  structure: uptrend / downtrend
    o, c = K("struct") - 0.1, K("bos") - 0.1
    s = S(o, c)
    tag(s, 1)
    for k, (key, pts, labs, col, head) in enumerate((
            ("up", [(90, 1130), (180, 960), (240, 1040), (330, 860), (390, 950), (490, 720)],
             [(180, 960, "HH", -24), (240, 1040, "HL", 44), (330, 860, "HH", -24), (390, 950, "HL", 44), (490, 720, "HH", -24)], UP, L("UPTREND", "ขาขึ้น")),
            ("down", [(590, 720), (680, 890), (740, 810), (830, 990), (890, 910), (990, 1130)],
             [(680, 890, "LL", 44), (740, 810, "LH", -24), (830, 990, "LL", 44), (890, 910, "LH", -24), (990, 1130, "LL", 44)], RED, L("DOWNTREND", "ขาลง")))):
        t = K(key)
        pn = panel(s, 50 + 500 * k, 600, 480, 640); s.fade(pn, t, 0.3)
        h = s.label(290 + 500 * k, 670, head, 32, col, 0, 800, 0.12); s.fade(h, t + 0.1)
        zig(s, pts, t + 0.2, 1.4)
        for j, (x, y, txt, dy) in enumerate(labs):
            lb = s.label(x, y + dy, txt, 24, col if txt in ("HH", "LL") else LBL, 0, 800, 0.06); s.fade(lb, t + 0.4 + 0.22 * j, 0.25)
    captions(s, [(o + 0.1, L("READ THE STRUCTURE FIRST", "ดูโครงสร้างก่อน"), WHITE),
                 (K("up") - 0.1, L("UP: HIGHER HIGHS, HIGHER LOWS", "ขาขึ้น: HIGHER HIGH, HIGHER LOW"), LBLUE),
                 (K("down") - 0.1, L("DOWN: LOWER HIGHS, LOWER LOWS", "ขาลง: LOWER HIGH, LOWER LOW"), RED)], c)

    # 3  what a BOS is
    o, c = K("bos") - 0.1, K("close") - 0.1
    s = S(o, c)
    tag(s, 1)
    C = path_candles([(0, 40), (4, 56), (7, 48), (11, 66), (14, 58), (17, 75)], seed=4, noise=0.9, wick=1.4)
    ch = Chart(C, 20, 90, 990, 600, 1180, 34, 80, 0.62)
    rid = candles_clip(s, ch)
    reveal(rid, ch, [(o + 0.2, 10), (K("cont") + 0.2, 10), (K("cont") + 1.4, 17)], o)
    lv = hline(s, ch, 66, 11, 19, GOLD, 4); s.fade(lv, K("bos") + 0.6, 0.3)
    hh = s.label(ch.x(10.4), ch.y(66) - 14, L("LAST HIGH", "HIGH ล่าสุด"), 22, GOLD, 0, 800, 0.08, "end"); s.fade(hh, K("bos") + 0.7)
    up = None
    i_b = next(i for i in range(12, len(C)) if C[i][3] > 66)
    rg = ring(s, ch.x(i_b), ch.y(C[i_b][3]), 22, GREEN); s.pop(rg, K("cont") + 0.2 + 1.2 * (i_b - 10) / 7, 0.35, 0.3)
    bt = s.pill(ch.x(13), ch.y(66) - 46, "BOS", GOLD, "#0b0b0b", 26); s.pop(bt, K("cont") + 0.3 + 1.2 * (i_b - 10) / 7, 0.35, 0.5)
    cue(K("cont") + 0.3 + 1.2 * (i_b - 10) / 7, "bell_E5", -22)
    nr = s.label(540, 1250, L("NOT A REVERSAL", "ไม่ใช่สัญญาณกลับตัว"), 30, GREY, 0, 800, 0.1); s.fade(nr, K("notrev") + 0.1)
    xr = s.path("M 380 1240 L 700 1240", RED, 5); s.draw(xr, K("notrev") + 0.7, 0.3)
    tc = s.pill(540, 520, L("TREND STILL ALIVE", "เทรนด์ยังไปต่อ"), GREEN, "#0b0b0b", 32); s.pop(tc, FW("notrev", "alive", "ไปต่อ") - 0.2, 0.4, 0.5)
    captions(s, [(o + 0.1, L("BREAK THE LAST SWING, SAME DIRECTION", "ทะลุ SWING ล่าสุด ไปทางเดิม"), WHITE),
                 (K("cont") - 0.1, L("UPTREND: CLOSE ABOVE THE LAST HIGH", "ขาขึ้น: ปิดเหนือ HIGH ล่าสุด"), GOLD)], c, 1352 + 20)

    # 4  rule one: a body close, not a wick
    o, c = K("close") - 0.1, K("swing") - 0.1
    s = S(o, c)
    tag(s, 1)
    hd = s.label(540, 450, L("RULE 1  ·  A CANDLE CLOSE", "กฎข้อ 1  ·  ต้องปิดแท่ง"), 40, WHITE, 0, 800, 0.06); s.pop(hd, o + 0.2, 0.4, 0.6)
    for k, (x0, key, ok) in enumerate(((60, "close", True), (560, "wick", False))):
        t = K(key) + (0.3 if ok else 0.1)
        pn = panel(s, x0, 560, 460, 600); s.fade(pn, t, 0.3)
        lv = hl(s, x0 + 20, x0 + 440, 800, GOLD, 4, "12 8"); s.fade(lv, t + 0.1, 0.3)
        lt = s.label(x0 + 30, 786, "HIGH", 22, GOLD, 0, 800, 0.08, "start"); s.fade(lt, t + 0.15)
        a = big_candle(s, x0 + 150, 64, 820, 1000, 860, 1040, 0, UP, False); s.fade(a, t + 0.2, 0.3)
        b = (big_candle(s, x0 + 300, 64, 700, 860, 740, 880, 0, UP, False) if ok else big_candle(s, x0 + 300, 64, 690, 860, 830, 880, 0, UP, False))
        s.fade(b, t + 0.6, 0.3)
        mk = (check if ok else xmark)(s, x0 + 400, 640, 24, GREEN if ok else RED, 7); s.draw(mk, t + 1.0, 0.35)
        lb = s.label(x0 + 230, 1110, L("BODY CLOSES ABOVE  ·  BOS", "เนื้อเทียนปิดเหนือ  ·  BOS") if ok else L("WICK ONLY  ·  STOP HUNT", "แค่ไส้ทะลุ  ·  ล่า STOP LOSS"),
                     24, GREEN if ok else RED, 0, 800, 0.04); s.fade(lb, t + 1.0)
        cue(t + 1.0, "bell_C5" if ok else "whoosh-short_1", -22)
    captions(s, [(o + 0.1, L("IT HAS TO CLOSE", "ต้องปิดแท่ง"), WHITE), (K("wick") - 0.1, L("A WICK THAT SNAPS BACK DOESN'T COUNT", "ไส้ทะลุแล้วเด้งกลับ ไม่นับ"), RED)], c)

    # 5  rule two: the right high
    o, c = K("swing") - 0.1, K("tf") - 0.1
    s = S(o, c)
    tag(s, 1)
    hd = s.label(540, 450, L("RULE 2  ·  THE RIGHT HIGH", "กฎข้อ 2  ·  HIGH ที่ถูกตัว"), 40, WHITE, 0, 800, 0.06); s.pop(hd, o + 0.2, 0.4, 0.6)
    pts = [(90, 1150), (150, 1060), (175, 1085), (215, 1010), (245, 1045), (285, 990), (320, 1040), (400, 870), (600, 1060), (720, 900), (800, 760), (900, 640)]
    zig(s, pts, o + 0.3, 1.6)
    for k, (x, y) in enumerate(((150, 1060), (285, 990))):
        m = s.label(x, y - 26, L("MINOR", "ยอดเล็ก"), 20, GREY, 0, 800, 0.08); s.fade(m, K("small") + 0.1 + 0.3 * k)
        xm = xmark(s, x, y - 60, 12, RED, 5); s.draw(xm, K("small") + 0.4 + 0.3 * k, 0.25)
    lo_ = ring(s, 320, 1040, 22, LBLUE); s.pop(lo_, FW("small", "low", "low") + 0.1, 0.35, 0.3)
    ll = s.label(360, 1100, L("THE LOW THAT PUSHED", "LOW ที่ดันราคาจริง"), 22, LBLUE, 0, 800, 0.06); s.fade(ll, FW("small", "low", "low") + 0.2)
    hi_ = ring(s, 400, 870, 22, GOLD); s.pop(hi_, FW("small", "high", "high") + 0.1, 0.35, 0.3)
    lh = hl(s, 400, 960, 870, GOLD, 4, "14 10"); s.fade(lh, FW("small", "high", "high") + 0.2, 0.3)
    th_ = s.label(400, 840, L("THIS HIGH", "HIGH ตัวนี้"), 24, GOLD, 0, 800, 0.08); s.fade(th_, FW("small", "high", "high") + 0.2)
    bb = s.pill(760, 830, "BOS", GOLD, "#0b0b0b", 24); s.pop(bb, FW("small", "higher", "จริงๆ") + 0.3, 0.35, 0.5)
    captions(s, [(o + 0.1, L("NOT EVERY LITTLE BUMP", "ไม่ใช่ทุกยอดเล็กๆ"), WHITE), (K("small") + 1.2, L("USE THE MAJOR SWING", "ใช้ SWING หลัก"), GOLD)], c)

    # 6  rule three: the timeframe
    o, c = K("tf") - 0.1, K("use") - 0.1
    s = S(o, c)
    tag(s, 1)
    hd = s.label(540, 450, L("RULE 3  ·  THE TIMEFRAME", "กฎข้อ 3  ·  TIMEFRAME"), 40, WHITE, 0, 800, 0.06); s.pop(hd, o + 0.2, 0.4, 0.6)
    for k, (txt, ok, w) in enumerate((("1M", False, "one"), ("3M", False, "three"), ("5M", True, "five"), ("15M+", True, "fifteen"))):
        t = FW("tf", w, {"one": "หนึ่ง", "three": "สาม", "five": "ห้า", "fifteen": "สิบห้า"}[w])
        x = 180 + 240 * k
        p = s.pill(x, 640, txt, "#1b1e23" if not ok else GREEN, GREY if not ok else "#0b0b0b", 40, 0, False); s.pop(p, t, 0.35, 0.5)
        mk = (check if ok else xmark)(s, x, 760, 26, GREEN if ok else RED, 7); s.draw(mk, t + 0.3, 0.3)
    D1 = [(50 + 3 * ((i * 7) % 5) - 6 + i * 0.4, 0, 0, 0) for i in range(26)]
    nz = [(o_, o_ + 2.5, o_ - 2.5, o_ + (2 if i % 2 else -2)) for i, (o_, _, _, _) in enumerate(D1)]
    ch1, g1 = mini(s, nz, 60, 860, 460, 340, 35, 70); s.fade(g1, FW("tf", "fake", "หลอก"), 0.4)
    f1 = s.label(290, 1240, L("FAKE BREAKS EVERYWHERE", "ทะลุหลอกเต็มไปหมด"), 22, RED, 0, 800, 0.06); s.fade(f1, FW("tf", "fake", "หลอก") + 0.2)
    C2 = path_candles([(0, 40), (3, 52), (5, 47), (8, 60), (10, 55), (13, 68)], seed=2, noise=0.7, wick=1.2)
    ch2, g2 = mini(s, C2, 560, 860, 460, 340, 36, 72); s.fade(g2, FW("tf", "five", "ห้า") + 0.4, 0.4)
    f2 = s.label(790, 1240, L("CLEAN STRUCTURE", "โครงสร้างชัด"), 22, GREEN, 0, 800, 0.06); s.fade(f2, FW("tf", "five", "ห้า") + 0.6)
    captions(s, [(o + 0.1, L("LOW TIMEFRAMES LIE", "TIMEFRAME เล็ก หลอกเยอะ"), RED), (FW("tf", "five", "ห้า") - 0.1, L("USE 5M AND 15M, OR HIGHER", "ใช้ 5M กับ 15M หรือสูงกว่า"), GREEN)], c, 1352 + 20)

    # 7  how to use it: sweep -> BOS -> pullback entry
    o, c = K("use") - 0.1, K("ex") - 0.1
    s = S(o, c)
    tag(s, 1)
    C = path_candles([(0, 62), (4, 50), (7, 56), (10, 44), (11, 39), (14, 54), (16, 60), (19, 52), (23, 70)], seed=6, noise=0.8, wick=1.3)
    ch = Chart(C, 25, 90, 990, 560, 1200, 34, 76, 0.62)
    rid = candles_clip(s, ch)
    reveal(rid, ch, [(o + 0.2, 9), (K("sweep") + 0.1, 9), (K("sweep") + 1.0, 11), (FW("sweep", "break", "break"), 11), (FW("sweep", "break", "break") + 1.2, 16), (K("pull"), 16), (K("pull") + 1.6, 23)], o)
    sl = hline(s, ch, 44, 3, 13, RED, 3); s.fade(sl, o + 0.4, 0.3)
    sw = ring(s, ch.x(11), ch.y(39), 22, RED); s.pop(sw, K("sweep") + 1.0, 0.35, 0.3)
    p1 = s.pill(ch.x(11), ch.y(39) + 60, L("1  SWEEP", "1  SWEEP"), RED, "#fff", 22); s.pop(p1, K("sweep") + 1.1, 0.35, 0.5)
    bl = hline(s, ch, 56, 7, 17, GOLD, 4); s.fade(bl, FW("sweep", "break", "break") - 0.2, 0.3)
    p2 = s.pill(ch.x(12), ch.y(56) - 40, L("2  BOS", "2  BOS"), GOLD, "#0b0b0b", 22); s.pop(p2, FW("sweep", "break", "break") + 1.0, 0.35, 0.5)
    ch_x = s.pill(ch.x(16), ch.y(62) - 40, L("DON'T CHASE", "อย่าไล่"), "#1b1e23", RED, 20, 0, False); s.pop(ch_x, K("pull") + 0.1, 0.35, 0.5)
    zb = rbox(s, ch.x(17) - 30, ch.y(54), ch.x(22), ch.y(51), GREEN, 0.2, 0.8, 2.5); s.fade(zb, K("pull") + 1.0, 0.4)
    p3 = s.pill(ch.x(19), ch.y(51) + 46, L("3  PULLBACK ENTRY", "3  เข้าตอน PULLBACK"), GREEN, "#0b0b0b", 22); s.pop(p3, K("pull") + 1.2, 0.35, 0.5)
    lt = s.label(ch.x(19), ch.y(51) + 100, L("ZONES: LATER EPISODES", "โซน: ตอนถัดๆไป"), 20, GREY, 0, 700, 0.1); s.fade(lt, K("later") + 0.1)
    cue(K("sweep") + 1.0, "bell_G4", -22); cue(FW("sweep", "break", "break") + 1.0, "bell_E5", -22); cue(K("pull") + 1.2, "bell_C5", -22)
    captions(s, [(o + 0.1, L("HOW TO USE IT", "ใช้ยังไง"), WHITE), (K("sweep") - 0.1, L("SWEEP, THEN WAIT FOR THE BOS", "SWEEP แล้วรอ BOS"), GOLD),
                 (K("pull") - 0.1, L("ENTER ON THE PULLBACK", "เข้าตอน PULLBACK"), GREEN)], c, 1352 + 40)

    # 8  example on gold
    o, c = K("ex") - 0.1, K("next") - 0.1
    s = S(o, c)
    tag(s, 1)
    hp = s.pill(540, 450, "XAUUSD  ·  15M  ·  EXAMPLE", WHITE, "#0b0b0b", 26); s.pop(hp, o + 0.2, 0.4, 0.5)
    C = path_candles([(0, 3842), (4, 3866), (7, 3852), (11, 3880), (14, 3864), (17, 3889), (20, 3866), (24, 3900)], seed=9, noise=1.6, wick=2.2)
    ch = Chart(C, 27, 90, 900, 560, 1200, 3836, 3906, 0.62)
    rid = candles_clip(s, ch)
    t_b = FW("ex", "closed", "ปิด")
    reveal(rid, ch, [(o + 0.2, 14), (t_b - 0.2, 14), (t_b + 0.8, 17), (K("ex2"), 17), (K("ex2") + 1.2, 20), (K("ex2") + 2.4, 20), (K("ex2") + 3.6, 24)], o)
    lv = hline(s, ch, 3880, 11, 26, GOLD, 4); s.fade(lv, o + 0.6, 0.3)
    lt = s.label(990, ch.y(3880) + 8, "3,880", 24, GOLD, 0, 800, 0.04, "end"); s.fade(lt, o + 0.7)
    bt = s.pill(ch.x(13), ch.y(3880) - 44, "BOS", GOLD, "#0b0b0b", 24); s.pop(bt, t_b + 0.7, 0.35, 0.5); cue(t_b + 0.7, "bell_E5", -22)
    hl_ = ring(s, ch.x(20), ch.y(3866), 20, LBLUE); s.pop(hl_, K("ex2") + 1.2, 0.35, 0.3)
    hlt = s.label(ch.x(20), ch.y(3866) + 60, "HL", 24, LBLUE, 0, 800, 0.08); s.fade(hlt, K("ex2") + 1.3)
    tp, slb = pos_box(s, ch.x(20), 990, ch.y(3866), ch.y(3900), ch.y(3858), FW("ex2", "bought", "ซื้อ") + 0.1)
    e = s.label(990, ch.y(3866) - 8, L("BUY 3,866", "BUY 3,866"), 22, WHITE, 0, 800, 0.04, "end"); s.fade(e, FW("ex2", "bought", "ซื้อ") + 0.2)
    sl_ = s.label(990, ch.y(3858) + 28, "SL 3,858", 22, RED, 0, 800, 0.04, "end"); s.fade(sl_, FW("ex2", "stop", "stop") + 0.1)
    cue(FW("ex2", "bought", "ซื้อ") + 0.1, "bell_C5", -22)
    nt = s.label(540, 1260, L("* ILLUSTRATION, NOT A REAL TRADE", "* ภาพตัวอย่าง ไม่ใช่เทรดจริง"), 20, GREY, 1, 600, 0.06)
    captions(s, [(o + 0.1, L("LAST HIGH: 3,880", "HIGH ล่าสุด: 3,880"), GOLD), (t_b - 0.1, L("CLOSED ABOVE: BOS", "ปิดเหนือ: BOS"), GOLD),
                 (K("ex2") - 0.1, L("BUY THE PULLBACK, SL UNDER THE LOW", "ซื้อตอนย่อ SL ใต้ LOW"), GREEN)], c, 1352 + 40)

    if CFG["outro1"]:
        next_ep(K("next") - 0.1, K("order") - 0.05, 2, "CHANGE OF CHARACTER", "CHANGE OF CHARACTER")
        outro(K("order") - 0.05)
    else:
        next_ep(K("next") - 0.1, G["TOTAL"], 2, "CHANGE OF CHARACTER", "CHANGE OF CHARACTER")


# ======================================================================================================== ep 1 ending: remember + think along
def end1():
    """a short ending clip for ep 0 + 1: a 'save this' recap of the 3 BOS rules, a think-along quiz (downtrend, a close
    above the last lower high: BOS or CHoCH? the answer, CHoCH, opens ep 2), then the follow-for-more outro"""
    o, c = 0, K("quiz") - 0.1
    s = S(o, c, first=True)
    tag(s, 1)
    s.label(540, 450, L("SAVE THIS", "เซฟไว้"), 64, WHITE, 1, 800, 0.06)
    s.label(540, 530, L("BREAK OF STRUCTURE  ·  3 RULES", "BREAK OF STRUCTURE  ·  3 กฎ"), 30, GOLD, 1, 700, 0.14)
    rows(s, [("CLOSE, NOT WICK", "ต้องปิดแท่ง ไม่ใช่แค่ไส้", WHITE), ("THE MAJOR SWING, NOT EVERY BUMP", "ใช้ SWING หลัก ไม่ใช่ยอดเล็ก", WHITE),
             ("5M / 15M OR HIGHER", "5M / 15M ขึ้นไป", GOLD)], [K("r1"), K("r2"), K("r3")], y0=690, dy=150, size=32)
    sc = s.label(540, 1200, L("SCREENSHOT IT", "แคปเก็บไว้"), 26, GREY, 0, 700, 0.2); s.fade(sc, K("r3") + 0.8, 0.4)

    o, c = K("quiz") - 0.1, K("order") - 0.05
    s = S(o, c)
    tag(s, 1)
    hd = s.label(540, 450, L("THINK ALONG", "คิดตาม"), 64, GOLD, 0, 800, 0.06); s.pop(hd, o + 0.15, 0.4, 0.6)
    C = path_candles([(0, 76), (3, 64), (5, 70), (9, 55), (11, 62), (14, 46), (16, 52)], seed=11, noise=0.8, wick=1.3)
    C += [(52, 53, 50.5, 51), (51, 64, 50.5, 63.5)]
    ch = Chart(C, 22, 70, 960, 600, 1120, 40, 80, 0.62)
    rid = candles_clip(s, ch)
    reveal(rid, ch, [(o + 0.2, 8), (K("q") + 0.2, 8), (K("q") + 1.8, 17), (K("q") + 2.6, 17), (K("q") + 3.1, 18)], o)
    for k, (i, p, t) in enumerate(((3, 64, "LL"), (5, 70, "LH"), (9, 55, "LL"), (11, 62, "LH"), (14, 46, "LL"))):
        lb = s.label(ch.x(i), ch.y(p) + (34 if t == "LL" else -16), t, 20, RED if t == "LL" else LBL, 0, 800, 0.06); s.fade(lb, K("q") + 0.3 + 0.12 * k)
    lv = hline(s, ch, 62, 11, 20, GOLD, 4); s.fade(lv, K("q") + 1.6, 0.3)
    lt = s.label(ch.x(12.2), ch.y(62) - 14, L("LAST LH", "LOWER HIGH ล่าสุด"), 22, GOLD, 0, 800, 0.06, "start"); s.fade(lt, K("q") + 1.7)
    rg = ring(s, ch.x(18), ch.y(63.5), 22, WHITE); s.pop(rg, K("q") + 3.2, 0.35, 0.3); cue(K("q") + 3.2, "bell_E5", -22)
    q = s.label(ch.x(18), ch.y(63.5) - 50, "?", 90, GOLD, 0, 800, 0); s.pop(q, K("ask") + 0.1, 0.4, 0.5)
    for k, (txt, x, key) in enumerate((("BOS", 330, FW("ask", "break", "break")), ("CHoCH", 750, FW("ask", "change", "change")))):
        p = s.pill(x, 1230, txt, "#1b1e23", WHITE, 40, 0, False); s.pop(p, key, 0.35, 0.5); cue(key, "bell_C5", -24)
    o_ = s.label(540, 1236, L("OR", "หรือ"), 30, GREY, 0, 800, 0.1); s.fade(o_, FW("ask", "change", "change") - 0.2)
    cm = s.label(540, 1320, L("COMMENT YOUR ANSWER  ·  ANSWER IN EP 2", "ตอบในคอมเมนต์  ·  เฉลยตอนหน้า"), 26, GOLD, 0, 800, 0.08); s.fade(cm, K("ans") + 0.1, 0.4)
    cue(K("ans") + 0.1, "swell_1", -24)
    outro(K("order") - 0.05)


# ======================================================================================================== 2  CHoCH
def quiz_chart_down(s, t0, t_close):
    """the ep 1 quiz chart: a downtrend (LH / LL), then a candle closes above the last lower high"""
    C = path_candles([(0, 76), (3, 64), (5, 70), (9, 55), (11, 62), (14, 46), (16, 52)], seed=11, noise=0.8, wick=1.3)
    C += [(52, 53, 50.5, 51), (51, 64, 50.5, 63.5)]
    ch = Chart(C, 22, 70, 960, 600, 1120, 40, 80, 0.62)
    rid = candles_clip(s, ch)
    reveal(rid, ch, [(t0, 17), (t_close - 0.4, 17), (t_close + 0.2, 18)], t0 - 0.2)
    for k, (i, p, t) in enumerate(((3, 64, "LL"), (5, 70, "LH"), (9, 55, "LL"), (11, 62, "LH"), (14, 46, "LL"))):
        s.label(ch.x(i), ch.y(p) + (34 if t == "LL" else -16), t, 20, RED if t == "LL" else LBL, 1, 800, 0.06)
    lv = hline(s, ch, 62, 11, 20, GOLD, 4, op=1)
    s.label(ch.x(12.2), ch.y(62) - 14, L("LAST LH", "LOWER HIGH ล่าสุด"), 22, GOLD, 1, 800, 0.06, "start")
    return ch


def short_box(s, x0, x1, y_entry, y_tp, y_sl, t):
    tp = rbox(s, x0, y_entry, x1, y_tp, UP, 0.28, 0.0, 0); sl = rbox(s, x0, y_sl, x1, y_entry, GREY, 0.35, 0.0, 0)
    s.fade(tp, t, 0.4); s.fade(sl, t, 0.4)
    return tp, sl


def ep2():
    # 1  the answer to ep 1's quiz
    o, c = 0, K("what") - 0.1
    s = S(o, c, first=True)
    tag(s, 2)
    hd = s.label(540, 450, L("LAST EPISODE'S QUESTION", "คำถามตอนที่แล้ว"), 44, WHITE, 1, 800, 0.04)
    ch = quiz_chart_down(s, 0.3, FW("hook", "closes", "ปิด") + 0.2)
    rg = ring(s, ch.x(18), ch.y(63.5), 22, WHITE); s.pop(rg, FW("hook", "closes", "ปิด") + 0.5, 0.35, 0.3)
    b1 = s.pill(330, 1230, "BOS", "#1b1e23", WHITE, 40, 0, False); s.pop(b1, FW("hook", "break", "break"), 0.35, 0.5)
    b2 = s.pill(750, 1230, "CHoCH", "#1b1e23", WHITE, 40, 0, False); s.pop(b2, FW("hook", "change", "change"), 0.35, 0.5)
    out(b1, K("answer") + 0.3, 0.3, 0.25)
    b3 = s.pill(750, 1230, "CHoCH", GREEN, "#0b0b0b", 40); s.pop(b3, K("answer") + 0.4, 0.4, 0.5)
    ck = check(s, 905, 1230, 22, GREEN, 7); s.draw(ck, K("answer") + 0.7, 0.3); cue(K("answer") + 0.4, "bell_A4", -18)
    captions(s, [(0.1, L("BOS OR CHoCH?", "BOS หรือ CHoCH?"), WHITE), (K("answer") - 0.1, L("ANSWER: CHANGE OF CHARACTER", "คำตอบ: CHANGE OF CHARACTER"), GREEN)], c, 1352 + 40)

    # 2  what it is: down and up
    o, c = K("what") - 0.1, K("seq") - 0.1
    s = S(o, c)
    tag(s, 2)
    s.label(540, 450, "CHANGE OF CHARACTER", 60, WHITE, 1, 800, 0.03)
    s.label(540, 525, L("THE FIRST BREAK AGAINST THE TREND", "ครั้งแรกที่ทะลุสวนเทรนด์"), 28, GOLD, 1, 700, 0.12)
    for k, (key, pts, lv, labs, col, head, txt) in enumerate((
            ("down", [(90, 700), (170, 880), (230, 800), (320, 990), (380, 910), (450, 1110), (490, 820)], (380, 910, 500),
             [(230, 800, "LH", -18), (380, 910, "LH", -18), (320, 990, "LL", 38), (450, 1110, "LL", 38)], RED, L("DOWNTREND", "ขาลง"), L("CLOSE ABOVE LAST LH", "ปิดเหนือ LH ล่าสุด")),
            ("up", [(590, 1110), (670, 930), (730, 1010), (820, 820), (880, 900), (950, 700), (990, 990)], (880, 900, 1000),
             [(730, 1010, "HL", 38), (880, 900, "HL", 38), (820, 820, "HH", -18), (950, 700, "HH", -18)], UP, L("UPTREND", "ขาขึ้น"), L("CLOSE BELOW LAST HL", "ปิดใต้ HL ล่าสุด")))):
        t = K(key)
        pn = panel(s, 50 + 500 * k, 600, 480, 640); s.fade(pn, t, 0.3)
        h = s.label(290 + 500 * k, 660, head, 30, col, 0, 800, 0.12); s.fade(h, t + 0.1)
        zig(s, pts, t + 0.2, 1.4)
        for j, (x, y, tx, dy) in enumerate(labs):
            lb = s.label(x, y + dy, tx, 22, LBL, 0, 800, 0.06); s.fade(lb, t + 0.3 + 0.15 * j, 0.25)
        x0, y0, x1 = lv
        ln = hl(s, x0, x1, y0, GOLD, 4, "12 8"); s.fade(ln, t + 1.2, 0.3)
        cp = s.pill(290 + 500 * k, 1180, "CHoCH", GOLD, "#0b0b0b", 26); s.pop(cp, t + 1.7, 0.35, 0.5)
        tt = s.label(290 + 500 * k, 1132, txt, 20, GOLD, 0, 800, 0.04); s.fade(tt, t + 1.8)
        cue(t + 1.7, "bell_E5", -22)
    captions(s, [(K("down") - 0.1, L("DOWN: FIRST CLOSE ABOVE THE LAST LH", "ขาลง: ปิดเหนือ LH ล่าสุด ครั้งแรก"), GOLD),
                 (K("up") - 0.1, L("UP: FIRST CLOSE BELOW THE LAST HL", "ขาขึ้น: ปิดใต้ HL ล่าสุด ครั้งแรก"), GOLD)], c, 1352 + 40)

    # 3  the usual order: BOS, BOS, CHoCH; a warning
    o, c = K("seq") - 0.1, K("close") - 0.1
    s = S(o, c)
    tag(s, 2)
    hd = s.label(540, 450, L("THE USUAL ORDER", "ลำดับที่เจอบ่อย"), 44, WHITE, 0, 800, 0.04); s.pop(hd, o + 0.2, 0.4, 0.6)
    pts = [(80, 1150), (180, 980), (240, 1050), (360, 840), (420, 930), (560, 700), (640, 820), (720, 760), (840, 1060), (920, 980)]
    zig(s, pts, o + 0.4, 2.2)
    for x0, x1, y, lab, t in ((180, 420, 980, "BOS", FW("seq", "break", "break") + 0.3), (360, 620, 840, "BOS", FW("seq", "break", "break") + 1.5),
                              (640, 900, 820, "CHoCH", FW("seq", "change", "change") + 0.2)):
        col = GOLD if lab == "CHoCH" else LBL
        ln = hl(s, x0, x1, y, col, 4, "12 8"); s.fade(ln, t, 0.3)
        lb = s.pill((x0 + x1) / 2 + (40 if lab == "CHoCH" else 0), y + (50 if lab == "CHoCH" else -36), lab, col, "#0b0b0b", 24); s.pop(lb, t + 0.1, 0.35, 0.5)
        cue(t + 0.1, "bell_C5" if lab == "BOS" else "bell_E5", -24)
    wn = s.pill(540, 1260, L("A WARNING, NOT A GUARANTEE", "สัญญาณเตือน ยังไม่ใช่การยืนยัน"), "#2a1d0e", GOLD, 30, 0, False); s.pop(wn, K("warn") + 0.2, 0.4, 0.5)
    captions(s, [(o + 0.1, "BOS  ·  BOS  ·  CHoCH", GOLD), (K("warn") - 0.1, L("THE TREND MAY BE TURNING", "เทรนด์อาจกำลังเปลี่ยน"), WHITE)], c, 1352 + 40)

    # 4  rule 1: close, not wick
    o, c = K("close") - 0.1, K("swing") - 0.1
    s = S(o, c)
    tag(s, 2)
    hd = s.label(540, 450, L("RULE 1  ·  A CANDLE CLOSE", "กฎข้อ 1  ·  ต้องปิดแท่ง"), 42, WHITE, 0, 800, 0.04); s.pop(hd, o + 0.2, 0.4, 0.6)
    for k, (x0, key, ok) in enumerate(((60, "close", True), (560, "wick", False))):
        t = K(key) + (0.3 if ok else 0.1)
        pn = panel(s, x0, 560, 460, 600); s.fade(pn, t, 0.3)
        lv = hl(s, x0 + 20, x0 + 440, 900, GOLD, 4, "12 8"); s.fade(lv, t + 0.1, 0.3)
        lt = s.label(x0 + 30, 935, L("LAST HL", "HL ล่าสุด"), 22, GOLD, 0, 800, 0.08, "start"); s.fade(lt, t + 0.15)
        a = big_candle(s, x0 + 150, 64, 660, 680, 860, 880, 0, DOWN, False); s.fade(a, t + 0.2, 0.3)
        b = (big_candle(s, x0 + 300, 64, 840, 860, 1010, 1040, 0, DOWN, False) if ok else big_candle(s, x0 + 300, 64, 840, 860, 880, 1040, 0, DOWN, False))
        s.fade(b, t + 0.6, 0.3)
        mk = (check if ok else xmark)(s, x0 + 400, 640, 24, GREEN if ok else RED, 7); s.draw(mk, t + 1.0, 0.35)
        lb = s.label(x0 + 230, 1110, L("BODY CLOSES BELOW  ·  CHoCH", "เนื้อเทียนปิดใต้  ·  CHoCH") if ok else L("WICK ONLY  ·  LIQUIDITY GRAB", "แค่ไส้  ·  ล่า LIQUIDITY"),
                     24, GREEN if ok else RED, 0, 800, 0.04); s.fade(lb, t + 1.0)
        cue(t + 1.0, "bell_C5" if ok else "whoosh-short_1", -22)
    captions(s, [(o + 0.1, L("SAME RULE: IT HAS TO CLOSE", "กฎเดิม: ต้องปิดแท่ง"), WHITE), (K("wick") - 0.1, L("A WICK THROUGH IT = LIQUIDITY GRAB", "ไส้ทะลุ = ล่า LIQUIDITY"), RED)], c)

    # 4b  rule 2: break a real swing (after the inducement is swept)
    o, c = K("swing") - 0.1, K("confirm") - 0.1
    s = S(o, c)
    tag(s, 2)
    hd = s.label(540, 450, L("RULE 2  ·  A REAL SWING", "กฎข้อ 2  ·  SWING จริง"), 42, WHITE, 0, 800, 0.04); s.pop(hd, o + 0.2, 0.4, 0.6)
    pts = [(90, 640), (250, 1010), (380, 800), (450, 890), (500, 850), (610, 990), (700, 900), (800, 700)]
    zig(s, pts, K("idm") - 0.2, 3.0)
    sh = ring(s, 380, 800, 20, GOLD); s.pop(sh, K("idm") + 0.1, 0.35, 0.3)
    sht = s.label(380, 770, "SWING HIGH?", 22, GOLD, 0, 800, 0.06); s.fade(sht, K("idm") + 0.2)
    il = hl(s, 450, 700, 890, LBLUE, 4, "10 7"); s.fade(il, FW("idm", "inducement", "inducement") + 0.1, 0.3)
    it = s.label(700, 925, "IDM", 24, LBLUE, 0, 800, 0.1, "end"); s.fade(it, FW("idm", "inducement", "inducement") + 0.2)
    t_sw = K("idm") - 0.2 + 3.0 * 0.62
    sw = ring(s, 610, 990, 20, LBLUE); s.pop(sw, t_sw, 0.35, 0.3)
    swt = s.label(610, 1050, L("IDM SWEPT", "กวาด IDM แล้ว"), 22, LBLUE, 0, 800, 0.06); s.fade(swt, t_sw + 0.1)
    out(sht, t_sw + 0.2, 0.2)
    rl = hl(s, 380, 880, 800, GOLD, 5, "14 9"); s.fade(rl, t_sw + 0.3, 0.3)
    rt = s.label(380, 770, L("REAL SWING HIGH", "SWING HIGH จริง"), 22, GOLD, 0, 800, 0.06); s.fade(rt, t_sw + 0.35)
    cp = s.pill(840, 660, "CHoCH", GOLD, "#0b0b0b", 26); s.pop(cp, K("idm") + 2.9, 0.35, 0.5); cue(K("idm") + 2.9, "bell_E5", -22)
    tr = s.path("M 500 850 L 560 760", RED, 5, style="stroke-dasharray:10 8;opacity:0"); s.fade(tr, K("trap") + 0.1, 0.3)
    tx = xmark(s, 575, 740, 14, RED, 5); s.draw(tx, K("trap") + 0.4, 0.25)
    tp_ = s.pill(540, 1180, L("BREAK BEFORE THE SWEEP = OFTEN A TRAP", "ทะลุก่อนกวาด IDM = มักเป็นกับดัก"), "#2a0e12", RED, 24, 0, False); s.pop(tp_, K("trap") + 0.5, 0.35, 0.5)
    cue(K("trap") + 0.4, "whoosh-short_1", -24)
    captions(s, [(o + 0.1, L("BREAK A REAL SWING", "ทะลุ SWING จริง"), WHITE), (K("idm") - 0.1, L("IT COUNTS AFTER THE IDM IS SWEPT", "นับได้หลังกวาด IDM"), LBLUE),
                 (K("trap") - 0.1, L("BEFORE THAT: OFTEN A TRAP", "ก่อนนั้น: มักเป็นกับดัก"), RED)], c, 1352 + 40)

    # 4c  rule 3: confirmation, a BOS in the new direction
    o, c = K("confirm") - 0.1, K("mistake") - 0.1
    s = S(o, c)
    tag(s, 2)
    hd = s.label(540, 450, L("RULE 3  ·  WAIT FOR CONFIRMATION", "กฎข้อ 3  ·  รอการยืนยัน"), 40, WHITE, 0, 800, 0.04); s.pop(hd, o + 0.2, 0.4, 0.6)
    pts = [(90, 640), (220, 900), (300, 820), (430, 1080), (540, 780), (630, 920), (800, 620)]
    zig(s, pts, o + 0.3, 2.6)
    l1 = hl(s, 300, 600, 820, GOLD, 4, "12 8"); s.fade(l1, o + 1.2, 0.3)
    p1 = s.pill(560, 870, "CHoCH", GOLD, "#0b0b0b", 24); s.pop(p1, o + 1.4, 0.35, 0.5)
    t_b = FW("bos2", "break", "break")
    l2 = hl(s, 540, 860, 780, GREEN, 4, "12 8"); s.fade(l2, t_b, 0.3)
    p2 = s.pill(860, 740, "BOS", GREEN, "#0b0b0b", 26); s.pop(p2, t_b + 0.2, 0.35, 0.5)
    cf = s.pill(540, 1180, L("CHoCH + BOS = CONFIRMED", "CHoCH + BOS = ยืนยันแล้ว"), GREEN, "#0b0b0b", 30); s.pop(cf, t_b + 0.8, 0.4, 0.5)
    cue(o + 1.4, "bell_C5", -24); cue(t_b + 0.2, "bell_E5", -22); cue(t_b + 0.8, "swell_1", -24)
    captions(s, [(o + 0.1, L("WAIT FOR CONFIRMATION", "รอการยืนยัน"), WHITE), (K("bos2") - 0.1, L("A BOS IN THE NEW DIRECTION", "BOS ในทิศทางใหม่"), GREEN)], c, 1352 + 40)

    # 5  the mistake: entering on the CHoCH candle; wait for the pullback
    o, c = K("mistake") - 0.1, K("ex") - 0.1
    s = S(o, c)
    tag(s, 2)
    C = path_candles([(0, 42), (4, 56), (6, 50), (10, 66), (12, 60), (15, 72), (18, 52), (21, 62), (25, 44)], seed=5, noise=0.8, wick=1.3)
    ch = Chart(C, 27, 70, 960, 560, 1200, 38, 78, 0.62)
    rid = candles_clip(s, ch)
    reveal(rid, ch, [(o + 0.2, 17), (K("wait"), 17), (K("wait") + 1.6, 21), (FW("wait", "then", "ค่อยเข้า"), 21), (FW("wait", "then", "ค่อยเข้า") + 1.6, 25)], o)
    lv = hline(s, ch, 60, 12, 26, GOLD, 4); s.fade(lv, o + 0.4, 0.3)
    s.label(ch.x(12), ch.y(60) + 34, L("LAST HL", "HL ล่าสุด"), 20, GOLD, 1, 800, 0.06)
    cp = s.pill(ch.x(17), ch.y(60) + 80, "CHoCH", GOLD, "#0b0b0b", 22); s.pop(cp, o + 0.6, 0.35, 0.5)
    ds = s.pill(ch.x(17), ch.y(48), L("DON'T SELL HERE", "อย่ารีบขายตรงนี้"), "#2a0e12", RED, 22, 0, False); s.pop(ds, K("mistake") + 1.0, 0.35, 0.5)
    xm = xmark(s, ch.x(17) - 120, ch.y(48), 14, RED, 5); s.draw(xm, K("mistake") + 1.3, 0.25)
    lh = ring(s, ch.x(21), ch.y(62), 20, LBLUE); s.pop(lh, K("wait") + 1.6, 0.35, 0.3)
    lht = s.label(ch.x(21), ch.y(62) - 30, "LH", 22, LBLUE, 0, 800, 0.08); s.fade(lht, K("wait") + 1.7)
    zb = rbox(s, ch.x(19.5), ch.y(63.5), ch.x(23), ch.y(59.5), GREEN, 0.18, 0.85, 2.5); s.fade(zb, FW("wait", "zone", "โซน") + 0.1, 0.35)
    zt = s.label(ch.x(21.2), ch.y(63.5) - 50, "OB  ·  FVG  ·  62–79%", 22, GREEN, 0, 800, 0.04); s.fade(zt, FW("wait", "order", "order") , 0.3)
    se = s.pill(ch.x(21.2), ch.y(52), L("SELL IN THE ZONE", "ขายในโซน"), GREEN, "#0b0b0b", 22); s.pop(se, FW("wait", "then", "ค่อยเข้า") , 0.35, 0.5)
    cue(K("mistake") + 1.0, "whoosh-short_2", -24); cue(FW("wait", "zone", "โซน") + 0.1, "bell_E5", -22)
    captions(s, [(o + 0.1, L("DON'T ENTER ON THE CHoCH CANDLE", "อย่าเข้าตรงแท่ง CHoCH"), RED), (K("wait") - 0.1, L("WAIT FOR THE PULLBACK INTO A ZONE", "รอย่อกลับเข้าโซน"), GREEN)], c, 1352 + 40)

    # 6  example on gold (short)
    o, c = K("ex") - 0.1, K("save") - 0.1
    s = S(o, c)
    tag(s, 2)
    hp = s.pill(540, 450, "XAUUSD  ·  15M  ·  EXAMPLE", WHITE, "#0b0b0b", 26); s.pop(hp, o + 0.2, 0.4, 0.5)
    C = path_candles([(0, 3818), (4, 3842), (7, 3832), (11, 3860), (13, 3840), (16, 3868), (19, 3834), (22, 3855), (26, 3824)], seed=8, noise=1.6, wick=2.2)
    ch = Chart(C, 29, 70, 880, 560, 1200, 3812, 3874, 0.62)
    rid = candles_clip(s, ch)
    t_b = FW("ex", "closed", "ปิด")
    reveal(rid, ch, [(o + 0.2, 16), (t_b - 0.3, 16), (t_b + 0.9, 19), (K("ex2"), 19), (K("ex2") + 1.4, 22), (K("ex2") + 3.0, 22), (K("ex2") + 4.6, 26)], o)
    lv = hline(s, ch, 3840, 13, 28, GOLD, 4); s.fade(lv, o + 0.6, 0.3)
    lt = s.label(990, ch.y(3840) - 10, "3,840", 24, GOLD, 0, 800, 0.04, "end"); s.fade(lt, o + 0.7)
    cp = s.pill(ch.x(15), ch.y(3840) + 44, "CHoCH", GOLD, "#0b0b0b", 24); s.pop(cp, t_b + 0.9, 0.35, 0.5); cue(t_b + 0.9, "bell_E5", -22)
    t_s = FW("ex2", "sold", "ขาย") + 0.1
    tp, slb = short_box(s, ch.x(22), 990, ch.y(3855), ch.y(3825), ch.y(3865), t_s)
    e = s.label(990, ch.y(3855) - 8, "SELL 3,855", 22, WHITE, 0, 800, 0.04, "end"); s.fade(e, t_s + 0.1)
    sl_ = s.label(990, ch.y(3865) - 8, "SL 3,865", 22, RED, 0, 800, 0.04, "end"); s.fade(sl_, FW("ex2", "stop", "stop") + 0.1)
    tp_ = s.label(990, ch.y(3825) + 28, "TP 3,825", 22, LBLUE, 0, 800, 0.04, "end"); s.fade(tp_, FW("ex2", "target", "เป้า") + 0.1)
    rr = s.pill(ch.x(18), ch.y(3819), "1 : 3", GREEN, "#0b0b0b", 26); s.pop(rr, FW("ex2", "one", "หนึ่งต่อ"), 0.35, 0.5)
    cue(t_s, "bell_C5", -22)
    s.label(540, 1260, L("* ILLUSTRATION, NOT A REAL TRADE", "* ภาพตัวอย่าง ไม่ใช่เทรดจริง"), 20, GREY, 1, 600, 0.06)
    captions(s, [(o + 0.1, L("LAST HL: 3,840", "HL ล่าสุด: 3,840"), GOLD), (t_b - 0.1, L("CLOSED BELOW: CHoCH", "ปิดใต้: CHoCH"), GOLD),
                 (K("ex2") - 0.1, L("REJECTED AT 3,855: SELL", "โดนปฏิเสธที่ 3,855: ขาย"), GREEN)], c, 1352 + 40)

    # 7  save this
    o, c = K("save") - 0.1, K("quiz") - 0.1
    s = S(o, c)
    tag(s, 2)
    s.label(540, 450, L("SAVE THIS", "เซฟไว้"), 64, WHITE, 1, 800, 0.06)
    s.label(540, 530, "CHANGE OF CHARACTER  ·  3 RULES" if not TH() else "CHANGE OF CHARACTER  ·  3 กฎ", 28, GOLD, 1, 700, 0.12)
    rows(s, [("FIRST BREAK AGAINST THE TREND, A CLOSE", "ทะลุสวนเทรนด์ครั้งแรก ต้องปิดแท่ง", WHITE), ("A REAL SWING, AFTER THE IDM SWEEP", "SWING จริง หลังกวาด IDM", WHITE),
             ("WAIT FOR THE BOS, THEN THE PULLBACK", "รอ BOS ยืนยัน แล้วเข้าตอน PULLBACK", GOLD)], [K("s1"), K("s2"), K("s3")], y0=690, dy=150, size=28)
    sc = s.label(540, 1200, L("SCREENSHOT IT", "แคปเก็บไว้"), 26, GREY, 0, 700, 0.2); s.fade(sc, K("s3") + 1.0, 0.4)

    # 8  think along: breakdown or liquidity sweep? (answer: sweep, ep 3)
    o, c = K("quiz") - 0.1, K("order") - 0.05
    s = S(o, c)
    tag(s, 2)
    hd = s.label(540, 450, L("THINK ALONG", "คิดตาม"), 64, GOLD, 0, 800, 0.06); s.pop(hd, o + 0.15, 0.4, 0.6)
    C = path_candles([(0, 66), (3, 52), (6, 62), (9, 50.5), (12, 60), (14, 54)], seed=12, noise=0.8, wick=1.2)
    C += [(54, 55, 52.5, 53), (53, 54, 46, 53.8), (53.8, 58, 53, 57.5)]
    ch = Chart(C, 20, 70, 960, 600, 1120, 40, 72, 0.62)
    rid = candles_clip(s, ch)
    t_w = FW("q", "wicks", "ไส้")
    reveal(rid, ch, [(o + 0.2, 14), (t_w - 0.2, 14), (t_w + 0.8, 16), (FW("q", "closes", "ปิด"), 16), (FW("q", "closes", "ปิด") + 0.6, 17)], o)
    lv = hline(s, ch, 50.5, 9, 19, LBLUE, 4); s.fade(lv, K("q") + 0.2, 0.3)
    lt = s.label(ch.x(9), ch.y(50.5) + 34, L("OLD LOW", "LOW เก่า"), 22, LBLUE, 0, 800, 0.06, "start"); s.fade(lt, K("q") + 0.3)
    rg = ring(s, ch.x(16), ch.y(46), 22, WHITE); s.pop(rg, t_w + 0.8, 0.35, 0.3); cue(t_w + 0.8, "bell_E5", -22)
    q = s.label(ch.x(16), ch.y(46) + 110, "?", 90, GOLD, 0, 800, 0); s.pop(q, K("ask") + 0.1, 0.4, 0.5)
    for txt, x, key in ((L("BREAKDOWN", "BREAKDOWN"), 320, FW("ask", "breakdown", "breakdown")), ("SWEEP", 760, FW("ask", "sweep", "sweep"))):
        p = s.pill(x, 1230, txt, "#1b1e23", WHITE, 38, 0, False); s.pop(p, key, 0.35, 0.5); cue(key, "bell_C5", -24)
    o_ = s.label(540, 1236, L("OR", "หรือ"), 30, GREY, 0, 800, 0.1); s.fade(o_, FW("ask", "sweep", "sweep") - 0.2)
    cm = s.label(540, 1320, L("COMMENT YOUR ANSWER  ·  ANSWER IN EP 3", "ตอบในคอมเมนต์  ·  เฉลยตอนหน้า"), 26, GOLD, 0, 800, 0.08); s.fade(cm, K("ans") + 0.1, 0.4)
    cue(K("ans") + 0.1, "swell_1", -24)
    outro(K("order") - 0.05)
