"""OTM Mindset ep1, "A loss is a teacher": one original script (EN Quentin / TH Patinya), two looks.
  style "otm":     the dark glowing OTM look: SL-hit chart, stuck loop vs staircase, stop loss -> tuition receipt,
                   trade journal, the same setup again, losses -> edge; phrase captions with the spoken word in gold.
  style "classic": full-screen classical paintings (generated for this video, assets/c1..c7.jpg) with a slow push-in,
                   one big word at a time, keywords in gold.
Both end on the Order the Market outro (handles + educational-only line). Candles: up #2962ff, down white, connected.
Thai visuals keep trading terms in English (stop loss, setup, edge, SL HIT)."""
from otm import *

def kw(key, en, th): return W(G["marks"][key] + (th if TH() else en))

# ---------------------------------------------------------------- captions
def _toks():
    w = G["words"]; end = G["marks"]["order"]
    return [(i, w[i]["text"]) for i in range(end)]

def _font(text):
    thai = any(0x0E00 <= ord(c) <= 0x0E7F for c in text)
    return ("Kanit", 700) if thai else ("Montserrat", 800)

def phrase_captions(y=1420, size=46):
    """phrase lines (up to 3 words EN, 1-2 chunks TH); the word being spoken turns gold"""
    o, c = 0, K("order") - 0.05
    s = S(o, c, first=True)
    T[:] = [ln for ln in T if f'"#{s.id}", {{scale: 1}}' not in ln]          # captions do not drift with the scene zoom
    starts = set(G["marks"].values())
    groups, cur = [], []
    for i, t in _toks():
        if cur and (i in starts or len(cur) >= (2 if TH() else 3) or (TH() and tw(" ".join(x[1] for x in cur) + t, size) > 900)):
            groups.append(cur); cur = []
        cur.append((i, t))
        if not TH() and t[-1] in ".?!,:":
            groups.append(cur); cur = []
    if cur: groups.append(cur)
    for g, grp in enumerate(groups):
        t0 = W(grp[0][0]) - 0.05
        t1 = (W(groups[g + 1][0][0]) - 0.05) if g + 1 < len(groups) else c - 0.1
        words = [(i, t.upper() if not TH() else t) for i, t in grp]
        fam, fw = _font("".join(t for _, t in words))
        fs = round(size * 1.08) if fam == "Kanit" else size
        while tw(" ".join(t for _, t in words), fs, 0.02) > 960: fs -= 2
        ids, spans = [], []
        for k, (i, t) in enumerate(words):
            wid = s.uid("cw"); ids.append((wid, i))
            spans.append(f'<tspan id="{wid}" fill="#ffffff">{t}</tspan>')
        gid = s.raw(f'<text id="@ID@" x="540" y="{y}" text-anchor="middle" font-family="{fam}" font-weight="{fw}" font-size="{fs}" letter-spacing="0.02em" '
                    f'style="opacity:0;paint-order:stroke;stroke:#000;stroke-width:6px" xml:space="preserve">' + " ".join(spans) + "</text>", "cg")
        d = min(0.15, max(0.04, (t1 - t0) * 0.5))
        tl(f'tl.fromTo("#{gid}", {{opacity: 0}}, {{opacity: 1, duration: {d:.3f}, ease: "power2.out", immediateRender: false}}, {t0:.3f});')
        tl(f'tl.set("#{gid}", {{opacity: 0}}, {max(t1, t0 + d + 0.01):.3f});')
        for k, (wid, i) in enumerate(ids):
            tl(f'tl.set("#{wid}", {{attr: {{fill: "{GOLD}"}}}}, {W(i):.3f});')
            if k + 1 < len(ids):
                tl(f'tl.set("#{wid}", {{attr: {{fill: "#ffffff"}}}}, {W(ids[k + 1][1]):.3f});')

KEY_EN = ("TEACHING", "STUCK", "BETTER", "PUNISHMENT", "TUITION", "LESSON", "LEARN", "MISTAKE", "READY", "DATA", "EDGE")
KEY_TH = ("สอน", "ติดอยู่", "เก่งขึ้น", "ลงโทษ", "ค่าเรียน", "บทเรียน", "คุ้ม", "พลาด", "พร้อม", "ข้อมูล", "edge")

def word_captions(y=1290):
    """one big word (EN) or phrase chunk (TH) at a time, centred, keywords gold (the classic look)"""
    o, c = 0, K("order") - 0.05
    s = S(o, c, first=True)
    T[:] = [ln for ln in T if f'"#{s.id}", {{scale: 1}}' not in ln]
    toks = _toks()
    for k, (i, t) in enumerate(toks):
        txt = t.strip(".,?!:").upper() if not TH() else t.strip(".")
        fam, fw = _font(txt)
        fs = 92 if fam == "Montserrat" else 78
        while tw(txt, fs, 0.02) > 960: fs -= 4
        key = any(kk.lower() in txt.lower() for kk in (KEY_TH if TH() else KEY_EN))
        col = GOLD if key else "#ffffff"
        t0 = W(i); t1 = W(toks[k + 1][0]) if k + 1 < len(toks) else c - 0.1
        wid = s.raw(f'<text id="@ID@" x="540" y="{y}" text-anchor="middle" font-family="{fam}" font-weight="{fw}" font-size="{fs}" letter-spacing="0.02em" '
                    f'fill="{col}" style="opacity:0;paint-order:stroke;stroke:#000;stroke-width:10px;filter:drop-shadow(0 4px 14px rgba(0,0,0,0.8))">{txt}</text>', "ww")
        d = min(0.12, max(0.03, (t1 - t0) * 0.5))
        tl(f'tl.fromTo("#{wid}", {{opacity: 0, scale: 0.86, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: {d:.3f}, ease: "power2.out", immediateRender: false}}, {t0:.3f});')
        tl(f'tl.set("#{wid}", {{opacity: 0}}, {max(t1, t0 + d + 0.01):.3f});')

# ---------------------------------------------------------------- the OTM look
def lbl(s, x, y, en, th, size=30, col=LBL, op=0, weight=800, sp=0.12):
    return s.label(x, y, L(en, th), size, col, op, weight, sp)

def pill(s, x, y, en, th, fill, tcol="#0b0b0b", size=30, op=0):
    return s.pill(x, y, L(en, th), fill, tcol, size, op)

def otm_scenes():
    # 1  the losing trade, "why?" -> "what is it teaching me?"
    o, c = 0, K("shift") - 0.1
    s = S(o, c, first=True)
    s.spot(540, 0.55, "255,77,94", 40, 260, 1120)
    ent = s.path("M 160 820 L 920 820", UP, 4, drawn=True, style="opacity:0;stroke-dasharray:14 10"); s.fade(ent, 0.2, 0.3)
    bt = s.add(f'<text id="@ID@" x="930" y="810" text-anchor="end" font-family="Montserrat" font-weight="800" font-size="24" fill="{UP}" style="opacity:0">BUY</text>', "t"); s.fade(bt, 0.2, 0.3)
    sl = s.path("M 160 960 L 920 960", RED, 4, drawn=True, style="opacity:0;stroke-dasharray:14 10"); s.fade(sl, 0.3, 0.3)
    s.add(f'<text id="@ID@" x="930" y="1000" text-anchor="end" font-family="Montserrat" font-weight="800" font-size="24" fill="{RED}" style="opacity:1">SL</text>', "t")
    cs = [(840, 800, 785, 855), (800, 770, 755, 815), (770, 795, 760, 805), (795, 760, 745, 805), (760, 820, 752, 830),
          (820, 880, 812, 890), (880, 860, 850, 900), (860, 930, 852, 940), (930, 1010, 920, 1030)]
    t_end_draw = kw("hook", 4, 1) if len(G["words"]) > 5 else 1.8
    for k, (yo, yc, yh, yl) in enumerate(cs):
        cd = big_candle(s, 220 + 80 * k, 44, yh, yo, yc, yl, 0)
        s.fade(cd, 0.15 + k * (t_end_draw - 0.3) / len(cs), 0.18)
    hit = pill(s, 540, 1080, "SL HIT", "SL HIT", RED, "#fff", 30); s.pop(hit, t_end_draw, 0.4, 0.5); cue(t_end_draw, "whoosh-short_1", -24)
    why = lbl(s, 540, 600, "WHY ME?", "ทำไม?", 76, RED, 0, 800, 0.06); s.pop(why, kw("hook", 2, 1) - 0.2, 0.4, 0.6)
    xm = xmark(s, 540, 575, 70, RED, 9); s.draw(xm, K("ask") + 0.1, 0.35)
    out(why, K("ask") + 0.4, 0.3, 0.25)
    tea = lbl(s, 540, 1210, "WHAT IS IT TEACHING ME?", "มันสอนอะไรเรา?", 44, GOLD, 0, 800, 0.06); s.pop(tea, K("ask") + 0.6, 0.45, 0.6)
    cue(K("ask") + 0.6, "bell_A4", -20)

    # 2  stuck vs better
    o, c = K("shift") - 0.1, K("sl") - 0.1
    s = S(o, c)
    lp = s.path("M 410 860 A 110 110 0 1 1 380 790", GREY, 7); s.draw(lp, K("shift") + 0.2, 0.8)
    lh = s.raw(f'<polygon id="@ID@" points="372,770 404,780 380,806" fill="{GREY}" style="opacity:0"/>', "ah"); s.fade(lh, K("shift") + 0.95, 0.2)
    lq = lbl(s, 300, 1060, "STUCK", "ติดอยู่ที่เดิม", 34, GREY, 0); s.fade(lq, K("shift") + 0.5, 0.3)
    q1 = lbl(s, 300, 660, "WHY?", "ทำไม?", 30, GREY, 0, 800, 0.1); s.fade(q1, K("shift") + 0.3, 0.3)
    st = s.path("M 640 1000 L 700 1000 L 700 940 L 760 940 L 760 880 L 820 880 L 820 820 L 880 820 L 880 760 L 940 760", GOLD, 7,
                style="filter:drop-shadow(0 0 12px rgba(232,194,106,0.6))"); s.draw(st, K("better") + 0.1, 0.9)
    ar = arrow(s, 900, 740, 975, 665, GOLD, 7, 26); show_arrow(s, ar, K("better") + 0.9, 0.3)
    bq = lbl(s, 800, 1060, "BETTER", "เก่งขึ้น", 34, GOLD, 0); s.pop(bq, K("better") + 0.6, 0.4, 0.6)
    q2 = lbl(s, 790, 660, "WHAT?", "สอนอะไร?", 30, GOLD, 0, 800, 0.1); s.fade(q2, K("better") + 0.2, 0.3)
    out(lp, K("better") + 0.3, 0.4, 0.3); out(lq, K("better") + 0.3, 0.4, 0.4)
    cue(K("better") + 0.1, "swell_1", -24)

    # 3  stop loss -> tuition -> paid -> learn it
    o, c = K("sl") - 0.1, K("journal") - 0.1
    s = S(o, c)
    p1 = pill(s, 540, 640, "STOP LOSS", "STOP LOSS", RED, "#fff", 40); s.pop(p1, K("sl") + 0.2, 0.4, 0.5)
    n1 = lbl(s, 540, 735, "IS NOT A PUNISHMENT", "ไม่ใช่การลงโทษ", 28, GREY, 0); s.fade(n1, kw("sl", 3, 2), 0.3)
    a1 = arrow(s, 540, 770, 540, 850, GOLD, 6, 22); show_arrow(s, a1, K("tuition") + 0.05, 0.3)
    p2 = pill(s, 540, 905, "IT'S TUITION", "มันคือค่าเรียน", GOLD, "#0b0b0b", 40); s.pop(p2, K("tuition") + 0.25, 0.4, 0.5); cue(K("tuition") + 0.25, "bell_C5", -22)
    rc = s.raw('<g id="@ID@" style="opacity:0"><rect x="380" y="990" width="320" height="230" rx="14" fill="none" stroke="#fff" stroke-width="3" '
               'style="filter:drop-shadow(0 0 10px rgba(255,255,255,0.25))"/>'
               + "".join(f'<line x1="410" y1="{1035 + 34 * k}" x2="{650 - 40 * (k % 2)}" y2="{1035 + 34 * k}" stroke="#7d838c" stroke-width="5" stroke-linecap="round"/>' for k in range(5))
               + "</g>", "rc")
    s.fade(rc, K("paid") + 0.1, 0.35, y=12)
    sp = s.raw(f'<g id="@ID@" style="opacity:0"><g transform="rotate(-14 540 1105)"><rect x="420" y="1068" width="240" height="74" rx="10" fill="none" stroke="{GOLD}" stroke-width="6"/>'
               f'<text x="540" y="1122" text-anchor="middle" font-family="{_font(L("PAID", "จ่ายแล้ว"))[0]}" font-weight="800" font-size="46" letter-spacing="0.12em" fill="{GOLD}">{L("PAID", "จ่ายแล้ว")}</text></g></g>', "sp")
    s.pop(sp, kw("paid", 2, 0) + 0.2, 0.35, 1.6); cue(kw("paid", 2, 0) + 0.2, "bell_G4", -20)
    ck = check(s, 790, 1105, 34, GOLD, 9); s.draw(ck, K("learn") + 0.15, 0.35)
    lt = lbl(s, 790, 1190, "LEARN IT", "เรียนให้คุ้ม", 26, GOLD, 0); s.fade(lt, K("learn") + 0.4, 0.3)

    # 4  the journal: write it down, find the mistake
    o, c = K("journal") - 0.1, K("next") - 0.1
    s = S(o, c)
    s.raw('<rect id="@ID@" x="300" y="600" width="480" height="600" rx="22" fill="rgba(255,255,255,0.03)" stroke="#fff" stroke-width="3" '
          'style="filter:drop-shadow(0 0 14px rgba(255,255,255,0.2))"/>', "nb")
    lbl(s, 540, 660, "TRADE JOURNAL", "TRADE JOURNAL", 26, LBL, 1, 800, 0.2)
    rows = [("ENTRY", "ENTRY", LBL), ("STOP LOSS", "STOP LOSS", LBL), ("RESULT  -1R", "RESULT  -1R", RED), ("MISTAKE: ENTERED EARLY", "จุดพลาด: เข้าเร็วไป", GOLD)]
    t_w = K("journal") + 0.15
    for k, (en, th, col) in enumerate(rows):
        yy = 760 + 105 * k
        ln = s.path(f"M 340 {yy + 22} L 740 {yy + 22}", "#3a3f47", 3); s.draw(ln, t_w + 0.25 * k, 0.3)
        tx = s.label(350, yy, L(en, th), 26, col, 0, 800, 0.06, "start"); s.fade(tx, t_w + 0.25 * k + 0.15, 0.25)
    t_find = kw("journal", 3, 1)
    rg = s.raw(f'<rect id="@ID@" x="330" y="1043" width="420" height="58" rx="29" fill="none" stroke="{GOLD}" stroke-width="5" '
               f'style="opacity:0;filter:drop-shadow(0 0 10px {GOLD})"/>', "rg")
    s.pop(rg, t_find + 0.1, 0.4, 0.6); cue(t_find + 0.1, "bell_E5", -22)

    # 5  the same setup again: ready
    o, c = K("next") - 0.1, K("data") - 0.1
    s = S(o, c)
    zb = rbox(s, 170, 900, 910, 980, GOLD, 0.12, 0.8, 2.5); s.fade(zb, K("next") + 0.2, 0.4)
    zl = lbl(s, 300, 1015, "SAME SETUP", "setup แบบเดิม", 24, GOLD, 0, 800, 0.12); s.fade(zl, K("next") + 0.4, 0.3)
    cs = [(760, 800, 750, 810), (800, 850, 790, 860), (850, 905, 840, 935), (905, 860, 850, 965), (860, 800, 790, 870),
          (800, 740, 730, 810), (740, 690, 680, 750), (690, 640, 625, 700)]
    t0, t1 = K("next") + 0.3, K("ready") + 0.2
    for k, (yo, yc, yh, yl) in enumerate(cs):
        cd = big_candle(s, 230 + 85 * k, 46, yh, yo, yc, yl, 0)
        s.fade(cd, t0 + k * (t1 - t0) / len(cs), 0.18)
    rp = pill(s, 540, 1130, "READY", "พร้อม", GOLD, "#0b0b0b", 44); s.pop(rp, K("ready") + 0.3, 0.4, 0.5); cue(K("ready") + 0.3, "swell_2", -24)

    # 6  losses become data, mistakes become your edge
    o, c = K("data") - 0.1, K("order") - 0.05
    s = S(o, c)
    xs = [220, 380, 540, 700, 860]
    chips = stop_chips(s, xs, 700, RED, "-1R", 24)
    for k, i in enumerate(chips): s.pop(i, K("data") + 0.1 + 0.1 * k, 0.3, 0.5)
    dl = lbl(s, 540, 790, "LOSS = DATA", "ขาดทุน = ข้อมูล", 32, LBL, 0, 800, 0.12); s.fade(dl, kw("data", 3, 1), 0.3)
    for k, x in enumerate(xs):
        p = s.path(f"M {x} 730 Q {(x + 540) / 2} 900 540 1010", GOLD, 3); s.draw(p, K("edge") + 0.1 + 0.05 * k, 0.5)
    s.spot(540, 0, "232,194,106", 40, 230, 1150)
    eg = pill(s, 540, 1070, "YOUR EDGE", "edge ของเรา", GOLD, "#0b0b0b", 50); s.pop(eg, K("edge") + 0.6, 0.45, 0.5); cue(K("edge") + 0.6, "bell_A4", -18)

# ---------------------------------------------------------------- the classic look
def classic_scenes():
    keys = ["hook", "shift", "sl", "paid", "journal", "next", "data", "order"]
    origins = ["50% 40%", "50% 70%", "60% 40%", "50% 35%", "40% 55%", "55% 60%", "50% 35%"]
    for k in range(7):
        o = 0 if k == 0 else K(keys[k]) - 0.15
        c = K(keys[k + 1]) + (0.2 if k < 6 else -0.05)
        s = S(o, c, first=(k == 0))
        im = s.raw(f'<image id="@ID@" href="assets/c{k + 1}.jpg" x="0" y="0" width="1080" height="1920" preserveAspectRatio="xMidYMid slice"/>', "im")
        tl(f'tl.fromTo("#{im}", {{scale: 1.0, transformOrigin: "{origins[k]}"}}, {{scale: 1.12, duration: {c - o:.3f}, ease: "none", immediateRender: false}}, {o:.3f});')
        gid = s.uid("gd")
        s.raw(f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/>'
              f'<stop offset="1" stop-color="#000" stop-opacity="0.78"/></linearGradient></defs>'
              f'<rect id="@ID@" x="0" y="950" width="1080" height="970" fill="url(#{gid})"/>', "gr")
        if k > 0: cue(o + 0.05, "whoosh-short_%d" % (1 + k % 2), -28)

def build(style):
    if style == "otm":
        otm_scenes(); phrase_captions()
    else:
        classic_scenes(); word_captions()
    outro(K("order") - 0.05)
    write()
