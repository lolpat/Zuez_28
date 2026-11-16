"""OTM trade recap, 16 Nov 2026 (plan from 12 Nov): slide-style recap built on the trader's own screenshots, in the same
layout as otm-recap-1106 (white slides, red italic "Recap order XAUUSD" title, one subtitle line per beat).
  assets/plan2h.jpg   2H plan, 12/11/2026: BSL 3,955.50, SSL 3,866.37, BUY ZONE 3,847.65 / 3,843.64 (OC) / 3,840.52, SL 3,830.72
  assets/h4.png       4H, 16/11/2026: SSL swept, price in the zone, 50% wick 3,841.99, SL 3,830.32
  assets/m5.jpg       5M, 16/11/2026: the tap of the 50% wick (3,842.33) and the run back up to the SSL
  assets/positions.jpg MT5 positions (still open, price 3865.92):
      buy 3   @3851.99  +4,179.00
      buy 4.8 @3846.61  +9,268.80
      buy 4.8 @3842.50  +11,241.60   (main)       together +24,689.40 floating
They missed their CRT fib entry (asleep) and used three buy limits around the 50% wick instead.
English (Quentin). Writes ../index.html, work/cues.json and work/timing.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *

LANG = "en"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = "otm-recap-1116"
TOTAL = init(ROOT, LANG, COMP, "mix_recap1116")
def KW(key, n): return W(G["marks"][key] + n)

INK, RED2, GRN2, ORG, BLU = "#111111", "#e0322b", "#1f9d55", "#f08a24", "#2962ff"
E1, E2, E3 = 3851.99, 3846.61, 3842.50
def px(p): return f"{p:,.2f}"

# price -> y on each screenshot (original pixels), calibrated on two drawn level lines each
def y2(p): return 697 + (3955.50 - p) * 8.487       # 2H: BSL 3,955.50 at y 697, SL 3,830.72 at y 1756
def y4(p): return 745 + (3955.50 - p) * 11.495      # 4H: BSL at y 745, SL 3,830.32 at y 2184
def y5(p): return 946 + (3866.37 - p) * 18.76       # 5M: SSL 3,866.37 at y 946, 50% wick 3,842.33 at y 1397

def slide_bg(s):
    s.raw('<rect id="@ID@" x="0" y="0" width="1080" height="1920" fill="#ffffff"/>', "bg")
    s.raw('<text id="@ID@" x="540" y="232" text-anchor="middle" font-family="Montserrat" font-weight="800" font-style="italic" '
          f'font-size="58" fill="{RED2}">Recap order XAUUSD</text>', "tt")

def subtitle(s, items, end, y=318):
    """items: [(t, [(text, colour), ...])]; one line per beat, swapped with a fade"""
    for k, (t, parts) in enumerate(items):
        t1 = items[k + 1][0] if k + 1 < len(items) else end
        spans = "".join(f'<tspan fill="{c}">{tx}</tspan>' for tx, c in parts)
        i = s.raw(f'<text id="@ID@" x="540" y="{y}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" '
                  f'style="opacity:0">{spans}</text>', "st")
        s.fade(i, t, 0.3, y=8)
        tl(f'tl.to("#{i}", {{opacity: 0, duration: 0.15}}, {t1 - 0.17:.3f});')

def tag(s, x, y, text, fill, tcol="#fff", size=30, op=0):
    w = tw(text, size, 0.04) + 40; h = size + 22
    return s.raw(f'<g id="@ID@" style="opacity:{op}"><rect x="{x - w / 2:.0f}" y="{y - h / 2:.0f}" width="{w:.0f}" height="{h}" rx="{h / 2}" fill="{fill}"/>'
                 f'<text x="{x}" y="{y + size * 0.36:.0f}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="{size}" '
                 f'letter-spacing="0.04em" fill="{tcol}">{text}</text></g>', "tg")

def hline(s, y, x0, x1, col, w=5, dash="", op=0, glow=False):
    d = f'stroke-dasharray="{dash}"' if dash else ""
    g = f";filter:drop-shadow(0 0 8px {col})" if glow else ""
    return s.raw(f'<line id="@ID@" x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{col}" stroke-width="{w}" {d} style="opacity:{op}{g}"/>', "hl")

def boxhl(s, b, col, op=0, w=7, pad=8):
    x0, y0, x1, y1 = b
    return s.raw(f'<rect id="@ID@" x="{x0 - pad}" y="{y0 - pad:.1f}" width="{x1 - x0 + 2 * pad}" height="{y1 - y0 + 2 * pad:.1f}" rx="10" fill="none" '
                 f'stroke="{col}" stroke-width="{w}" style="opacity:{op};filter:drop-shadow(0 0 8px {col})"/>', "bh")

def shot_open(s, img, size, crop, panel=(57, 372, 966), shadow=True):
    cx, cy, cw, ch_ = crop; x, y, w = panel
    h = w * ch_ / cw
    if shadow:
        s.raw(f'<rect id="@ID@" x="{x - 6}" y="{y - 6}" width="{w + 12}" height="{h + 12:.0f}" rx="18" fill="#ffffff" '
              f'stroke="#d9dce1" stroke-width="2" style="filter:drop-shadow(0 8px 24px rgba(0,0,0,0.18))"/>', "sh")
    s.items.append(f'<svg x="{x}" y="{y}" width="{w}" height="{h:.1f}" viewBox="{cx} {cy:.1f} {cw} {ch_:.1f}" preserveAspectRatio="none">'
                   f'<image href="{img}" x="0" y="0" width="{size[0]}" height="{size[1]}"/>')
    return y + h

def shot_close(s): s.items.append("</svg>")

def chart(s, img, size, crop, extra=None, note="* real trade, my own screenshot and markings", panel=(57, 372, 966)):
    bot = shot_open(s, img, size, crop, panel)
    if extra: extra()
    shot_close(s)
    s.label(540, bot + 30, note, 20, "#8a8f98", 1, 600, 0.02)
    return bot

P2 = ("assets/plan2h.jpg", (1101, 2133), (0, 560, 1101, 1270))
P4 = ("assets/h4.png", (1320, 2868), (0, 700, 1320, 1550))
P5 = ("assets/m5.jpg", (1109, 2119), (0, 380, 1109, 1300))

# 1  hook: the 4H chart and the floating result
o1, c1 = 0, K("plan") - 0.1
s = S(o1, c1, first=True)
slide_bg(s)
def x1():
    tag(s, 360, 860, "+$24,689", GRN2, "#fff", 76, 1)
    t = tag(s, 360, 975, "FLOATING · STILL OPEN", INK, "#fff", 34); s.pop(t, KE("result", 4) + 0.1, 0.35, 0.5)
    tag(s, 360, 1060, "3 BUY LIMITS · 16 NOV · 4H", BLU, "#fff", 34, 1)
chart(s, *P4, x1)
subtitle(s, [(0.05, [("Gold, 16 Nov: ", INK), ("three buy limits", BLU)]), (K("result") - 0.1, [("Together: ", INK), ("+$24,689", GRN2), (" and running", INK)])], c1)
cue(0.3, "whoosh-short_1", -22)

# 2  the plan on the 2H (12 Nov)
o2, c2 = K("plan") - 0.1, K("wait") - 0.1
s = S(o2, c2)
slide_bg(s)
def x2():
    d = tag(s, 820, 1020, "PLAN · 12 NOV · 2H", INK, "#fff", 40); s.pop(d, K("plan") + 0.3, 0.35, 0.5)
    a = hline(s, y2(3866.37), 200, 650, ORG, 7, glow=True); s.fade(a, K("ssl") + 0.2, 0.3)
    z = boxhl(s, (200, y2(3847.65), 650, y2(3840.52)), ORG, pad=10); s.pop(z, K("zone") + 0.3, 0.4, 0.6)
    zt = tag(s, 820, 1300, "BUY ZONE 3,840 – 3,848", ORG, "#fff", 36); s.pop(zt, KW("zone", 7), 0.35, 0.5)
    l = hline(s, y2(3830.72), 200, 650, RED2, 7, glow=True); s.fade(l, K("sl") + 0.2, 0.3)
    st = tag(s, 150, 1700, "SL 3,830.72", RED2, "#fff", 36); s.pop(st, KW("sl", 4), 0.35, 0.5)
    b = hline(s, y2(3955.50), 200, 650, GRN2, 7, glow=True); s.fade(b, K("target") + 0.2, 0.3)
    ar = arrow(s, 560, y2(3847.65) - 30, 560, y2(3955.50) + 40, GRN2, 9, 34); show_arrow(s, ar, K("target") + 0.4, 0.8)
    bt = tag(s, 820, 800, "TARGET 3,955.50", GRN2, "#fff", 40); s.pop(bt, KW("target", 3), 0.35, 0.5)
chart(s, *P2, x2)
cue(K("zone") + 0.3, "bell_G4", -22); cue(K("target") + 0.4, "swell_1", -24)
subtitle(s, [(o2 + 0.1, [("The plan: ", INK), ("12 Nov", RED2), (", 2H chart", INK)]),
             (K("ssl") - 0.1, [("Price stops at ", INK), ("sell-side liquidity", ORG)]),
             (K("zone") - 0.1, [("Buy zone at the ", INK), ("OC", ORG), (": 3,840 – 3,848", INK)]),
             (K("sl") - 0.1, [("Stop loss under it: ", INK), ("3,830.72", RED2)]),
             (K("target") - 0.1, [("Target: ", INK), ("buy-side liquidity", GRN2)])], c2)

# 3  four days later, the 4H: sweep, into the zone, the 50% wick
o3, c3 = K("wait") - 0.1, K("miss") - 0.1
s = S(o3, c3)
slide_bg(s)
def x3():
    w = tag(s, 360, 900, "4 DAYS LATER · 16 NOV", INK, "#fff", 42); s.pop(w, K("wait") + 0.2, 0.4, 0.5)
    a = hline(s, y4(3866.37), 0, 820, ORG, 8, glow=True); s.fade(a, K("sweep") + 0.6, 0.3)
    at = tag(s, 200, 1880, "SSL SWEPT", ORG, "#fff", 40); s.pop(at, KW("sweep", 9), 0.35, 0.5)
    z = boxhl(s, (0, 1989, 480, 2071), ORG, pad=10); s.pop(z, K("tap") + 0.3, 0.4, 0.6)
    r = ring(s, 685, 2049, 40, BLU); s.pop(r, K("wick") + 0.3, 0.35, 0.3)
    wt = tag(s, 905, 1885, "50% WICK 3,841.99", BLU, "#fff", 38); s.pop(wt, KW("wick", 4), 0.35, 0.5)
chart(s, *P4, x3)
cue(K("wait") + 0.2, "whoosh-short_2", -22); cue(K("tap") + 0.3, "bell_E5", -22); cue(K("wick") + 0.3, "bell_G5", -22)
subtitle(s, [(o3 + 0.1, [("Then I ", INK), ("waited", RED2), (" four days", INK)]),
             (K("sweep") - 0.1, [("16 Nov, 4H: price sweeps the ", INK), ("SSL", ORG)]),
             (K("tap") - 0.1, [("…and drops right into ", INK), ("my zone", ORG)]),
             (K("wick") - 0.1, [("The ", INK), ("50% wick", BLU), (": 3,841.99", INK)])], c3)

# 4  missed the CRT fib entry, so three buy limits (a clean price ladder)
o4, c4 = K("miss") - 0.1, K("m5") - 0.1
s = S(o4, c4)
slide_bg(s)
mi = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="190" y="420" width="700" height="84" rx="42" fill="#f4f5f7" stroke="#d9dce1" stroke-width="2"/>'
           f'<text x="560" y="474" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="32" fill="#8a8f98">CRT fib entry: missed (asleep)</text></g>', "mi")
s.fade(mi, K("miss") + 0.2, 0.35, y=10)
xm = xmark(s, 240, 462, 18, RED2, 7); s.draw(xm, K("miss") + 0.7, 0.3)
def ly(p): return 700 + (3856.0 - p) * 30.0
X0, X1 = 110, 970
lad = []
lad.append(s.raw(f'<rect id="@ID@" x="{X0}" y="{ly(3847.65):.1f}" width="{X1 - X0}" height="{ly(3840.52) - ly(3847.65):.1f}" fill="{ORG}" fill-opacity="0.13" '
                 f'stroke="{ORG}" stroke-opacity="0.8" stroke-width="2.5" style="opacity:0"/>', "zb"))
lad.append(s.label(X0 + 10, ly(3847.65) - 16, "BUY ZONE (OC)", 26, ORG, 0, 800, 0.04, "start"))
lad.append(hline(s, ly(3841.99), X0, X1, INK, 3, "6 8"))
lad.append(s.label(X0 + 10, ly(3841.99) + 40, "50% WICK 3,841.99", 26, INK, 0, 800, 0.04, "start"))
lad.append(hline(s, ly(3830.72), X0, X1, RED2, 5))
lad.append(s.label(X0 + 10, ly(3830.72) - 16, "SL 3,830.72", 28, RED2, 0, 800, 0.04, "start"))
for i in lad: s.fade(i, K("limits") + 0.2, 0.4)
for k, (p, lots, key, main) in enumerate([(E1, "3", "l1", False), (E2, "4.8", "l2", False), (E3, "4.8", "l3", True)]):
    t = K(key) + (0.6 if main else 0.1)
    ln = hline(s, ly(p), X0, X1, BLU, 7 if main else 5, "", 0, glow=main); s.fade(ln, t, 0.3)
    txt = f"MAIN · BUY {lots} @ {px(p)}" if main else f"BUY {lots} @ {px(p)}"
    tg = tag(s, 700, ly(p) - 40, txt, BLU, "#fff", 34 if main else 30); s.pop(tg, t + 0.1, 0.35, 0.5)
    cue(t, "bell_C5", -24)
subtitle(s, [(o4 + 0.1, [("I missed my ", INK), ("CRT fib", ORG), (" entry", INK)]),
             (K("limits") - 0.1, [("So: ", INK), ("three buy limits", BLU)]),
             (K("l3") - 0.1, [("Main one on the ", INK), ("50% wick", BLU)])], c4)

# 5  the 5M: tap of the wick and the run back up
o5, c5 = K("m5") - 0.1, K("pos") - 0.1
s = S(o5, c5)
slide_bg(s)
def x5():
    for p, a in [(E1, 0.75), (E2, 0.75), (E3, 0.95)]:
        hline(s, y5(p), 0, 1109, BLU, 4, "12 8", a)
    for p, lab in [(E1, "3,851.99"), (E2, "3,846.61"), (E3, "3,842.50")]:
        tag(s, 990, y5(p) - 30, lab, BLU, "#fff", 28, 1)
    tf = tag(s, 860, 600, "16 NOV · 5M", INK, "#fff", 40, 1)
    r = ring(s, 411, 1400, 40, BLU); s.pop(r, K("m5") + 0.6, 0.35, 0.3)
    tt = tag(s, 360, 1540, "TAGGED THE 50% WICK", BLU, "#fff", 36); s.pop(tt, KW("m5", 5), 0.35, 0.5)
    ar = arrow(s, 470, 1330, 520, 990, GRN2, 10, 36); show_arrow(s, ar, K("run") + 0.2, 0.7)
    rt = tag(s, 830, 830, "BACK TO THE SSL", GRN2, "#fff", 38); s.pop(rt, K("run") + 0.8, 0.35, 0.5)
chart(s, *P5, x5)
cue(K("m5") + 0.6, "bell_G4", -22); cue(K("run") + 0.2, "whoosh-short_1", -22)
subtitle(s, [(o5 + 0.1, [("5M: price ", INK), ("tags the wick", BLU)]),
             (K("run") - 0.1, [("…and runs ", INK), ("straight back up", GRN2)])], c5)

# 6  the open positions
o6, c6 = K("pos") - 0.1, K("recap") - 0.1
s = S(o6, c6)
slide_bg(s)
bot = shot_open(s, "assets/positions.jpg", (1320, 583), (0, 0, 1320, 583), panel=(40, 470, 1000))
for k, key in enumerate([KW("pnl", 0), KW("pnl", 3), KW("pnl", 7)]):
    b = boxhl(s, (30, 92 + 170 * k, 1290, 228 + 170 * k), GRN2, pad=4); s.pop(b, key, 0.35, 0.6)
shot_close(s)
s.label(540, bot + 40, "* my MT5 positions, 16 Nov 2026 (still open)", 22, "#8a8f98", 1, 600, 0.02)
pn = s.raw(f'<text id="@ID@" x="540" y="{bot + 200:.0f}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="124" '
           f'fill="{GRN2}" style="opacity:0">+$24,689.40</text>', "pn")
s.pop(pn, K("total") + 0.3, 0.5, 0.5); cue(K("total") + 0.3, "bell_A4", -16)
fl = tag(s, 540, bot + 295, "FLOATING · PRICE 3,865.92", INK, "#fff", 36); s.pop(fl, KW("total", 8), 0.35, 0.5)
tg = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="150" y="{bot + 370:.0f}" width="780" height="96" rx="48" fill="#ffffff" stroke="{GRN2}" stroke-width="4"/>'
           f'<text x="540" y="{bot + 431:.0f}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" fill="{GRN2}">TARGET STILL ABOVE: 3,955.50</text></g>', "tg")
s.pop(tg, K("still") + 0.2, 0.4, 0.6); cue(K("still") + 0.2, "swell_2", -24)
s.label(540, bot + 545, "3 + 4.8 + 4.8 lots", 30, INK, 1, 800, 0.04)
subtitle(s, [(o6 + 0.1, [("All three ", INK), ("filled", BLU)]),
             (K("pnl") - 0.1, [("+4,179", GRN2), (" · ", INK), ("+9,268", GRN2), (" · ", INK), ("+11,241", GRN2)]),
             (K("total") - 0.1, [("Together: ", INK), ("+$24,689", GRN2), (", floating", INK)]),
             (K("still") - 0.1, [("The target is ", INK), ("still above", GRN2)])], c6)

# 7  summary
o7, c7 = K("recap") - 0.1, K("order") - 0.05
s = S(o7, c7)
slide_bg(s)
s.label(540, 470, "Summary of this trade", 44, RED2, 1, 800, 0.02)
rows = [("1", [("Plan early", RED2), (": 2H buy zone at the OC", INK)], KW("recap", 0)),
        ("2", [("Mark the zone", ORG), (" + the 50% wick", INK)], KW("recap", 2)),
        ("3", [("Set ", INK), ("3 buy limits", BLU), (", SL under the zone", INK)], KW("recap", 5))]
for k, (n, parts, t) in enumerate(rows):
    yy = 610 + 150 * k
    card = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="80" y="{yy - 52}" width="920" height="104" rx="22" fill="#f4f5f7" stroke="#e3e5e8" stroke-width="2"/>'
                 f'<circle cx="140" cy="{yy}" r="30" fill="{RED2}"/><text x="140" y="{yy + 12}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="32" fill="#fff">{n}</text>'
                 f'<text x="190" y="{yy + 12}" font-family="Montserrat" font-weight="700" font-size="31">'
                 + "".join(f'<tspan fill="{c}">{tx}</tspan>' for tx, c in parts) + "</text></g>", "rw")
    s.fade(card, t, 0.35, y=14); cue(t, "bell_C5", -26)
lv = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="160" y="1110" width="760" height="90" rx="45" fill="{GRN2}"/>'
           f'<text x="540" y="1168" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" fill="#fff">Then let price come to you</text></g>', "lv")
s.pop(lv, K("let"), 0.4, 0.7); cue(K("let"), "swell_2", -24)
subtitle(s, [(o7 + 0.1, [("Recap: ", INK), ("plan, zone, limits", RED2)])], c7)

outro(K("order") - 0.05)
write()
