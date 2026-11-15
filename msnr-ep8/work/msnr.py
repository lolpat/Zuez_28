"""Shared scenes for the OTM MSNR key-level series v2 (msnr-ep0..ep6, English, and msnr-ep0-th..ep6-th, Thai).
Built on the CRT engine (work/otm.py). Episodes 1-6 share one layout, driven by a spec in each work/gen.py:
  1. title + the level's shape as a line diagram (key level marked)
  2. how to draw it: a close-up of the candles, the exact close / open that makes the level
  3. an XAUUSD example chart, built step by step (liquidity, key level, reaction, target)
  4. the four-step flow
  5. the next-episode card (episode 6 instead: the bearish mirror, the save card and the outro)
Candles up #2962ff, down white. Example charts are synthetic illustrations, not real prices."""
from otm import *

DX0, DX1, DY0, DY1 = 110, 970, 640, 1180            # diagram panel
def nx(u): return DX0 + (DX1 - DX0) * u
def ny(v): return DY1 - (DY1 - DY0) * v
SERIES_N = 6


def series_tag_m(s, n):
    return s.label(540, 300, L(f"MSNR KEY LEVELS  ·  {n}/6", f"MSNR KEY LEVELS  ·  {n}/6"), 26, GOLD, 1, 700, 0.2)


def KW(key, n): return W(G["marks"][key] + n)


def FWm(key, en, th, off=0.0, span=40):
    """time of the first word at/after mark `key` containing `en` / `th`; falls back to K(key)+off"""
    sub = (th if TH() else en).lower(); ws = G["words"]; i0 = G["marks"][key]
    for i in range(i0, min(len(ws), i0 + span)):
        acc = ""
        for j in range(i, min(len(ws), i + 6)):
            acc += ws[j]["text"].strip().lower()
            if sub in acc: return W(i)
    return K(key, off)


def title_block(s, title, sub, op=1, t=None):
    a = s.label(540, 450, title, 84, WHITE, op, 800, 0.04)
    b = s.label(540, 530, sub, 34, GOLD, op, 700, 0.14)
    if t is not None:
        s.pop(a, t, 0.45, 0.6); s.fade(b, t + 0.3, 0.4)
    return a, b


def diagram(s, pts, t0, dur, level=None, ghost=True, col=WHITE):
    """a line-chart sketch of the level's shape; level = (v, u0, u1, label, t)"""
    d = "M " + " L ".join(f"{nx(u):.1f} {ny(v):.1f}" for u, v in pts)
    if ghost:
        s.raw(f'<path id="@ID@" d="{d}" fill="none" stroke="#ffffff" stroke-opacity="0.12" stroke-width="5" stroke-linejoin="round"/>', "gh")
    p = s.path(d, col, 6, style="filter:drop-shadow(0 0 10px rgba(255,255,255,0.35))")
    s.draw(p, t0, dur, "power1.inOut")
    out_ = [p]
    if level:
        v, u0, u1, text, t = level
        ln = s.raw(f'<line id="@ID@" x1="{nx(u0):.1f}" y1="{ny(v):.1f}" x2="{nx(u0):.1f}" y2="{ny(v):.1f}" stroke="{GOLD}" stroke-width="5" stroke-dasharray="16 10"/>', "lv")
        tl(f'tl.to("#{ln}", {{attr: {{x2: {nx(u1):.1f}}}, duration: 0.7, ease: "power2.out"}}, {t:.3f});')
        lb = s.label(nx(u1), ny(v) + (-16 if v < 0.5 else 44), text, 30, GOLD, 0, 800, 0.08, "end"); s.fade(lb, t + 0.4)
        cue(t, "whoosh-short_2", -24)
        out_ += [ln, lb]
    return out_


def chart_panel(s, candles, nxs, top=680, bot=1180, pmin=0, pmax=100, x0=150, x1=950):
    return Chart(candles, nxs, x0, x1, top, bot, pmin, pmax, 0.62)


def flow_card(s, steps, times, y0=720, dy=150):
    """the four-step flow: words popping one under another, joined by chevrons"""
    for k, ((en, th, col), t) in enumerate(zip(steps, times)):
        yy = y0 + dy * k
        w_ = s.label(540, yy, L(en, th), 66, col, 0, 800, 0.05); s.pop(w_, t, 0.35, 0.6)
        cue(t, ["tick-crisp_1", "tick-crisp_2", "tick-crisp_3", "tick-crisp_1"][k % 4], -18)
        if k:
            yc = yy - dy + 46
            a = s.path(f"M 518 {yc} L 540 {yc + 18} L 562 {yc}", GREY, 4, drawn=True, style="opacity:0"); s.fade(a, t - 0.1, 0.2)


def next_card(s, o, c, n_next, en, th):
    s2 = S(o, c)
    nx_ = s2.label(540, 760, L(f"NEXT  ·  {n_next}/6", f"ตอนต่อไป  ·  {n_next}/6"), 30, GREY, 0, 700, 0.2); s2.fade(nx_, o + 0.1)
    a = s2.label(540, 900, L(en, th), 80, GOLD, 0, 800, 0.04); s2.pop(a, o + 0.5, 0.4, 0.6)
    cue(o + 0.2, "whoosh-long_1", -22)
    return s2


def episode(spec):
    """episodes 1-6"""
    n, last = spec["n"], spec.get("last", False)
    # 1  title + shape
    o1, c1 = 0, K("draw") - 0.1
    s = S(o1, c1, first=True)
    series_tag_m(s, n)
    title_block(s, L(*spec["title"]), L(*spec["sub"]))
    diagram(s, spec["shape"], K("shape"), max(1.5, K("why") - K("shape") - 0.4), spec.get("shape_level") and
            (spec["shape_level"][0], spec["shape_level"][1], spec["shape_level"][2], L(*spec["shape_level"][3]), K("why")))
    for (u, v, key, en, th, col, dy) in spec.get("shape_marks", []):
        r = ring(s, nx(u), ny(v), 20, col); s.pop(r, K(key) + spec.get("mark_off", {}).get(en, 0.8), 0.35, 0.3)
        lb = s.label(nx(u), ny(v) + dy, L(en, th), 26, col, 0, 800, 0.08); s.fade(lb, K(key) + spec.get("mark_off", {}).get(en, 0.8) + 0.1)
    captions(s, [(K(k) - 0.1, L(en, th), col) for k, en, th, col in spec["cap1"]], c1)

    # 2  how to draw
    o2, c2 = K("draw") - 0.1, K("ex") - 0.1
    s = S(o2, c2)
    series_tag_m(s, n)
    hd = s.pill(540, 470, L("HOW TO DRAW", "วิธีวาด"), WHITE, "#0b0b0b", 30); s.pop(hd, o2 + 0.2, 0.4, 0.5)
    dr = spec["draw"]
    if dr["kind"] == "line":
        # Classic V / A: mark the turn on the LINE chart (closes), then switch back to candles for the stop
        ch = chart_panel(s, dr["candles"], len(dr["candles"]) + 1, top=700, bot=1170, x0=170, x1=880)
        up = dr["side"] == "below"
        t_line, t_mark = K("draw") + 0.2, FWm("draw", dr["word"][0], dr["word"][1], 1.6)
        t_cnd, t_sl = K("draw2") - 0.05, FWm("draw2", dr["slword"][0], dr["slword"][1], 1.6)
        # chart-mode switch: LINE CHART -> CANDLES
        for k, (en, th) in enumerate((("LINE CHART", "LINE CHART"), ("CANDLES", "CANDLES"))):
            x = 400 + 280 * k
            s.pill(x, 590, L(en, th), "#2a2a2a", GREY, 24, 1, False)
            on = s.pill(x, 590, L(en, th), GOLD, "#111", 24, 0)
            s.fade(on, t_line if k == 0 else t_cnd, 0.25)
            if k == 0: out(on, t_cnd, 0.25)
        cg = s.raw('<g id="@ID@" style="opacity:0">' + ch.candles() + "</g>", "cg"); s.fade(cg, t_cnd, 0.45)
        d = "M " + " L ".join(f"{ch.x(i):.1f} {ch.y(c[3]):.1f}" for i, c in enumerate(ch.c))
        ln_ = s.path(d, WHITE, 6, style="filter:drop-shadow(0 0 10px rgba(255,255,255,0.35))"); s.draw(ln_, t_line, 1.1, "power1.inOut")
        out(ln_, t_cnd + 0.1, 0.4, 0.22)
        i = dr["lvl"]; p = ch.c[i][3]
        r = ring(s, ch.x(i), ch.y(p), 18, GOLD); s.pop(r, t_mark, 0.35, 0.3); cue(t_mark, "bell_E5", -24)
        lv = s.raw(f'<line id="@ID@" x1="{ch.x(i):.1f}" y1="{ch.y(p):.1f}" x2="{ch.x(i):.1f}" y2="{ch.y(p):.1f}" stroke="{GOLD}" stroke-width="5"/>', "lv")
        tl(f'tl.to("#{lv}", {{attr: {{x2: 990}}, duration: 0.8, ease: "power2.out"}}, {t_mark + 0.2:.3f});')
        lb = s.label(990, ch.y(p) + (44 if up else -16), L(*dr["label"]), 32, GOLD, 0, 800, 0.08, "end"); s.fade(lb, t_mark + 0.6)
        # the stop: past the wick of the turning candle
        w = ch.c[i][2] if up else ch.c[i][1]
        sl = w - 2.5 if up else w + 2.5
        rw = ring(s, ch.x(i), ch.y(w), 16, RED); s.pop(rw, t_sl, 0.35, 0.3)
        sll = s.raw(f'<line id="@ID@" x1="{ch.x(i) - 40:.1f}" y1="{ch.y(sl):.1f}" x2="990" y2="{ch.y(sl):.1f}" stroke="{RED}" stroke-width="4" stroke-dasharray="12 8" style="opacity:0"/>', "sl")
        s.fade(sll, t_sl + 0.15, 0.35)
        slt = s.pill(930, ch.y(sl) + (34 if up else -34), "SL", RED, WHITE, 24); s.pop(slt, t_sl + 0.3, 0.35, 0.5)
        cue(t_sl, "swell_1", -24)
    elif dr["kind"] == "candles":
        ch = chart_panel(s, dr["candles"], len(dr["candles"]) + dr.get("pad", 1), x0=dr.get("x0", 200), x1=dr.get("x1", 900))
        s.raw('<g id="@ID@">' + ch.candles() + "</g>", "cg")
        for (i, p, key, en, th, side) in dr["marks"]:
            x = ch.x(i) + (-ch.sp * 0.42 if side == "l" else ch.sp * 0.42)
            r = ring(s, x, ch.y(p), 16, GOLD); s.pop(r, K(key) + 0.3, 0.35, 0.3)
            lb = s.label(x + (-28 if side == "l" else 28), ch.y(p) + 10, L(en, th), 28, GOLD, 0, 800, 0.08, "end" if side == "l" else "start")
            s.fade(lb, K(key) + 0.4); cue(K(key) + 0.3, "bell_E5", -24)
        for (i, p, key) in dr.get("touches", []):
            r = ring(s, ch.x(i), ch.y(p), 18, WHITE); s.pop(r, K(key) + 0.3, 0.35, 0.3)
        for (i, key) in dr.get("highlight", []):
            o_, h_, l_, c_ = ch.c[i]
            bx = rbox(s, ch.x(i) - ch.bw / 2 - 12, ch.y(h_) - 12, ch.x(i) + ch.bw / 2 + 12, ch.y(l_) + 12, GOLD, 0.0, 1, 4); s.fade(bx, K(key) + 0.3, 0.3)
        p, i0, en, th, key = dr["level"]
        ln = s.raw(f'<line id="@ID@" x1="{ch.x(i0) - ch.bw:.1f}" y1="{ch.y(p):.1f}" x2="{ch.x(i0) - ch.bw:.1f}" y2="{ch.y(p):.1f}" stroke="{GOLD}" stroke-width="5"/>', "lv")
        tl(f'tl.to("#{ln}", {{attr: {{x2: 990}}, duration: 0.8, ease: "power2.out"}}, {K(key) + 0.6:.3f});')
        lb = s.label(990, ch.y(p) + dr.get("label_dy", -16), L(en, th), 32, GOLD, 0, 800, 0.08, "end"); s.fade(lb, K(key) + 1.0)
        cue(K(key) + 0.6, "whoosh-short_1", -24)
    else:   # a line sketch (QM)
        diagram(s, dr["pts"], o2 + 0.3, 2.0, (dr["level"][0], dr["level"][1], dr["level"][2], L(*dr["level"][3]), K(dr["level"][4])))
        for (u, v, key, en, th, col, dy) in dr.get("marks", []):
            r = ring(s, nx(u), ny(v), 20, col); s.pop(r, K(key) + 0.3, 0.35, 0.3)
            lb = s.label(nx(u), ny(v) + dy, L(en, th), 28, col, 0, 800, 0.08); s.fade(lb, K(key) + 0.4)
    captions(s, [(K(k) - 0.1, L(en, th), col) for k, en, th, col in spec["cap2"]], c2)

    # 3  XAUUSD example
    o3, c3 = K("ex") - 0.1, (K("mirror") if last else K("rule")) - 0.1
    s = S(o3, c3)
    series_tag_m(s, n)
    hp = s.pill(540, 470, L("XAUUSD  ·  EXAMPLE", "XAUUSD  ·  ตัวอย่าง"), WHITE, "#0b0b0b", 28); s.pop(hp, o3 + 0.2, 0.4, 0.5)
    ex = spec["example"]
    C = path_candles(ex["pivots"], seed=ex.get("seed", 5), noise=ex.get("noise", 1.6), wick=ex.get("wick", 1.6))
    for i, v in ex.get("override", {}).items(): C[i] = v
    ch = Chart(C, len(C) + 3, 90, 1000, 620, 1230, 0, 100, 0.64)
    N = len(C)
    if ex.get("sl"):
        sp, si0, skey = ex["sl"]
        sll = hline(s, ch, sp, si0, N + 2, RED, 3, "10 7", 0); s.fade(sll, K(skey) + 0.9, 0.4)
        slt = s.label(ch.x(N + 2), ch.y(sp) + (30 if ex.get("level_below") else -12), "SL", 24, RED, 0, 800, 0.08, "end"); s.fade(slt, K(skey) + 1.0)
    # level, liquidity lines and the accumulation box behind the candles
    lp, li0, len_, lth = ex["level"]
    lv = hline(s, ch, lp, li0, N + 2, GOLD, 4, "14 9", 0)
    s.fade(lv, o3 + 0.4, 0.5)
    lvt = s.label(ch.x(N + 2), ch.y(lp) + (36 if ex.get("level_below") else -14), L(len_, lth), 28, GOLD, 0, 800, 0.08, "end"); s.fade(lvt, o3 + 0.6)
    for (p, i0, i1, en, th, col, key, below) in ex.get("lines", []):
        ln = hline(s, ch, p, i0, i1, col, 3, "8 7", 0); s.fade(ln, K(key) + 0.2, 0.4)
        lt = s.label(ch.x(i1), ch.y(p) + (34 if below else -12), L(en, th), 24, col, 0, 800, 0.08, "end"); s.fade(lt, K(key) + 0.3)
    if ex.get("box"):
        i0, i1, p0, p1, en, th, key = ex["box"]
        bx = rbox(s, ch.x(i0), ch.y(p1), ch.x(i1), ch.y(p0), LBLUE, 0.16, 0.8, 2); s.fade(bx, K(key) + 0.3, 0.4)
        bt = s.label((ch.x(i0) + ch.x(i1)) / 2, ch.y(p1) - 12, L(en, th), 24, LBLUE, 0, 800, 0.08); s.fade(bt, K(key) + 0.4)
    rid = candles_clip(s, ch)
    keys = [(o3, -1), (o3 + 0.3, ex["start"])]
    for key, idx in ex["reveal"]:
        keys += [(K(key) - 0.05, keys[-1][1]), (K(key) + ex.get("rdur", 1.0), idx)]
    keys.append((c3 - 0.6, N - 1))
    reveal(rid, ch, keys, o3)
    for (key, ri, rp, pi, pp, en, th, col) in ex["steps"]:
        t = K(key) + ex.get("rdur", 1.0) * 0.8
        if ri is not None:
            r = ring(s, ch.x(ri), ch.y(rp), 20, col); s.pop(r, t, 0.35, 0.3)
        if en:
            pl = s.pill(ch.x(pi), ch.y(pp), L(en, th), col, "#0b0b0b" if col != RED else WHITE, 22); s.pop(pl, t + 0.1, 0.35, 0.5)
        cue(t, "bell_C5" if col == GOLD else "swell_1", -24)
    captions(s, [(K(k) - 0.1, L(en, th), col) for k, en, th, col in spec["cap3"]], c3)

    # 4  the four-step flow (episode 6: the bearish mirror comes first, as in the script)
    if last:
        o5, c5 = K("mirror") - 0.1, K("rule") - 0.1
        s = S(o5, c5)
        series_tag_m(s, n)
        title_block(s, L("BEARISH QM", "BEARISH QM"), L("THE MIRROR IMAGE", "ภาพกลับด้าน"))
        diagram(s, [(u, 1 - v) for u, v in spec["draw"]["pts"]], o5 + 0.3, 1.6,
                (1 - spec["draw"]["level"][0], spec["draw"]["level"][1], spec["draw"]["level"][2], "QM", o5 + 1.4))
    o4 = K("rule") - 0.1
    c4 = (K("save") if last else K("next")) - 0.1
    s = S(o4, c4)
    series_tag_m(s, n)
    flow_card(s, spec["flow"], [KW("rule", k) for k in L(*spec["flow_tok"])])

    if not last:
        nn, en, th = spec["next"]
        next_card(s, K("next") - 0.1, G["TOTAL"], nn, en, th)
        return
    # episode 6: the save card (the series continues with the storyline part)
    o6, c6 = K("save") - 0.1, G["TOTAL"]
    s = S(o6, c6)
    series_tag_m(s, n)
    lv = [("CLASSIC V", "CLASSIC V"), ("CLASSIC A", "CLASSIC A"), ("SBR", "SBR"), ("RBS", "RBS"), ("OCL", "OCL"), ("QM", "QM")]
    for k, (en, th) in enumerate(lv):
        x = 300 if k % 2 == 0 else 780; yy = 640 + 120 * (k // 2)
        p = s.pill(x, yy, L(en, th), GOLD if k % 2 else WHITE, "#111", 30); s.pop(p, o6 + 0.3 + 0.12 * k, 0.35, 0.5)
    sv = s.label(540, 1060, L("SAVE THIS SERIES", "เซฟซีรีส์นี้ไว้"), 56, WHITE, 0, 800, 0.05); s.pop(sv, KW("save", L(3, 1)), 0.4, 0.6)
    hb = s.pill(540, 1180, L("HTF BIAS FIRST", "ยืนยัน BIAS บน HTF ก่อน"), GOLD, "#111", 32); s.pop(hb, KW("save", L(7, 2)), 0.4, 0.6)
    cue(o6 + 0.3, "swell_2", -22); cue(KW("save", L(3, 1)), "bell_A4", -20)
    nn, en, th = spec["next"]
    nl = s.label(540, 1290, L(f"NEXT  ·  {en}", f"ตอนต่อไป  ·  {th}"), 30, GREY, 0, 700, 0.16); s.fade(nl, G["VOICE_END"] - 0.4 if G.get("VOICE_END") else KW("save", L(9, 2)) + 1.0)
