"""OTM trade recap, 6 Nov 2026: slide-style recap built on the trader's own screenshot (assets/trade.jpg, the MT5 deals
list over his 15-minute XAUUSD chart with his OB / SBR / CHoCH markings), in the layout of the "Recap order XAUUSD"
reference reel: white slides, a red italic "Recap order XAUUSD" title, one subtitle line per beat, markings on the
real chart. The deals (from the screenshot, closed 2026.11.06 15:31:50 unless noted):
  sell 6 lots 4133.00 -> 4036.63  +57,822.00   (at the order block)
  sell 6 lots 4115.00 -> 4036.63  +47,022.00   (at the SBR)
  buy  6 lots 4065.00 -> 4061.00   -2,400.00   (03:30:12, stopped out)
  Profit 102,444.00. The stops of the two sells are not in the screenshot, so the video shows no RR.
English (Quentin). Writes ../index.html, work/cues.json and work/timing.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *

LANG = "en"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = "otm-recap-1106"
TOTAL = init(ROOT, LANG, COMP, "mix_recap1106")
def KW(key, n): return W(G["marks"][key] + n)

S1, S2, CLOSE = 4133.00, 4115.00, 4036.63
INK, RED2, GRN2, ORG = "#111111", "#e0322b", "#1f9d55", "#f08a24"
def px(p): return f"{p:,.2f}"

# screenshot geometry (1320 x 2346), calibrated on the live-price line (4033.57 at y 1970.5) and the axis spacing
IMW, IMH = 1320, 2346
def sy(p): return 1970.5 + (4033.57 - p) * 11.264
OB_BOX = (18, 792, 111, 842)            # x0, y0, x1, y1 of his upper order block
SBR_BOX = (217, 995, 311, 1054)         # his upper SBR box
OB2_BOX = (657, 1305, 892, 1408)        # his lower OB / SBR area
X_RALLY, X_CLOSE, X_LOW = 651, 815, 792
CROP = (0, 740, IMW, 1380)              # the chart part
PANEL = (40, 390, 1000)
DEALS = (387, 320, 700, 290)            # the deals list
PROFIT = (387, 625, 700, 205)           # deposit / profit / swap / balance
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

def shot_open(s, crop=CROP, panel=PANEL, shadow=True):
    """open a nested svg that shows a crop of the screenshot; overlays added before shot_close use image pixels"""
    cx, cy, cw, ch_ = crop; x, y, w = panel
    h = w * ch_ / cw
    if shadow:
        s.raw(f'<rect id="@ID@" x="{x - 6}" y="{y - 6}" width="{w + 12}" height="{h + 12:.0f}" rx="18" fill="#ffffff" '
              f'stroke="#d9dce1" stroke-width="2" style="filter:drop-shadow(0 8px 24px rgba(0,0,0,0.18))"/>', "sh")
    s.items.append(f'<svg x="{x}" y="{y}" width="{w}" height="{h:.1f}" viewBox="{cx} {cy:.1f} {cw} {ch_:.1f}" preserveAspectRatio="none">'
                   f'<image href="assets/trade.jpg" x="0" y="0" width="{IMW}" height="{IMH}"/>')
    return y + h

def shot_close(s): s.items.append("</svg>")

def tag(s, x, y, text, fill, tcol="#fff", size=30, op=0):
    w = tw(text, size, 0.04) + 40; h = size + 22
    return s.raw(f'<g id="@ID@" style="opacity:{op}"><rect x="{x - w / 2:.0f}" y="{y - h / 2:.0f}" width="{w:.0f}" height="{h}" rx="{h / 2}" fill="{fill}"/>'
                 f'<text x="{x}" y="{y + size * 0.36:.0f}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="{size}" '
                 f'letter-spacing="0.04em" fill="{tcol}">{text}</text></g>', "tg")

def hl(s, p, x0, x1, col, w=5, dash="", op=0):
    d = f'stroke-dasharray="{dash}"' if dash else ""
    return s.raw(f'<line id="@ID@" x1="{x0}" y1="{sy(p):.1f}" x2="{x1}" y2="{sy(p):.1f}" stroke="{col}" stroke-width="{w}" {d} style="opacity:{op}"/>', "hl")

def note(s, text, y):
    return s.label(540, y, text, 22, "#8a8f98", 1, 600, 0.02)

def boxhl(s, b, col, op=0, w=7):
    x0, y0, x1, y1 = b
    return s.raw(f'<rect id="@ID@" x="{x0 - 8}" y="{y0 - 8}" width="{x1 - x0 + 16}" height="{y1 - y0 + 16}" rx="10" fill="none" '
                 f'stroke="{col}" stroke-width="{w}" style="opacity:{op};filter:drop-shadow(0 0 8px {col})"/>', "bh")

def chart(s, extra=None):
    bot = shot_open(s)
    if extra: extra()
    shot_close(s)
    note(s, "* real trade, my own screenshot (my OB / SBR / CHoCH markings)", bot + 40)
    return bot

# 1  hook: the real chart and the day's result
o1, c1 = 0, K("why") - 0.1
s = S(o1, c1, first=True)
slide_bg(s)
def x1():
    tag(s, 1000, 980, "+$102,444", GRN2, "#fff", 64, 1)
    tag(s, 1000, 1080, "2 SELLS  ·  15M", INK, "#fff", 36, 1)
chart(s, x1)
subtitle(s, [(0.05, [("Gold, 6 Nov: ", INK), ("two sells", RED2)]), (K("result") - 0.1, [("Day closed at ", INK), ("+$102,444", GRN2)])], c1)
cue(0.3, "whoosh-short_1", -22)

# 2  the order block and the first sell
o2, c2 = K("why") - 0.1, K("sbr") - 0.1
s = S(o2, c2)
slide_bg(s)
def x2():
    b = boxhl(s, OB_BOX, ORG); s.pop(b, K("ob") + 0.4, 0.4, 0.6)
    t = tag(s, 200, 776, "ORDER BLOCK", ORG, "#fff", 34); s.pop(t, K("ob") + 0.6, 0.35, 0.5)
    l = hl(s, S1, 18, 640, RED2, 5, "14 9"); s.fade(l, K("sell1") + 0.2, 0.3)
    t2 = tag(s, 450, sy(S1) + 46, f"SELL {px(S1)}", RED2, "#fff", 38); s.pop(t2, K("sell1") + 0.3, 0.35, 0.5)
chart(s, x2)
cue(K("ob") + 0.4, "bell_G4", -22); cue(K("sell1") + 0.3, "bell_E5", -20)
subtitle(s, [(o2 + 0.1, [("The plan", INK)]), (K("ob") - 0.1, [("Top: an ", INK), ("order block", ORG)]),
             (K("sell1") - 0.1, [("Sell #1 at ", INK), (px(S1), RED2)])], c2)

# 3  the SBR and the second sell
o3, c3 = K("sbr") - 0.1, K("choch") - 0.1
s = S(o3, c3)
slide_bg(s)
def x3():
    hl(s, S1, 18, 640, RED2, 4, "14 9", 0.6)
    b = boxhl(s, SBR_BOX, RED2); s.pop(b, K("sbr") + 0.4, 0.4, 0.6)
    t = tag(s, 264, 935, "SBR", RED2, "#fff", 38); s.pop(t, K("sbr") + 0.6, 0.35, 0.5)
    l = hl(s, S2, 217, 760, RED2, 5, "14 9"); s.fade(l, K("sell2") + 0.8, 0.3)
    t2 = tag(s, 560, sy(S2) - 40, f"SELL {px(S2)}", RED2, "#fff", 38); s.pop(t2, K("sell2") + 0.9, 0.35, 0.5)
chart(s, x3)
cue(K("sbr") + 0.4, "swell_1", -22); cue(K("sell2") + 0.9, "bell_E5", -20)
subtitle(s, [(o3 + 0.1, [("SBR", RED2), (": old support became resistance", INK)]),
             (K("sell2") - 0.1, [("Back into it: sell #2 at ", INK), (px(S2), RED2)])], c3)

# 4  structure breaks, the failed bounce at the next SBR, the fall, the close
o4, c4 = K("choch") - 0.1, K("loss") - 0.1
s = S(o4, c4)
slide_bg(s)
def x4():
    hl(s, S1, 18, 640, RED2, 4, "14 9", 0.6); hl(s, S2, 217, 760, RED2, 4, "14 9", 0.6)
    b = boxhl(s, OB2_BOX, ORG); s.pop(b, K("lh") + 0.6, 0.4, 0.6)
    r = ring(s, X_RALLY, 1440, 34, ORG); s.pop(r, K("lh") + 1.2, 0.35, 0.3)
    xm = xmark(s, X_RALLY + 70, 1440, 22, RED2, 7); s.draw(xm, K("lh") + 1.6, 0.3)
    a = arrow(s, X_RALLY + 30, 1500, X_CLOSE - 10, sy(CLOSE) - 30, RED2, 9, 36); show_arrow(s, a, K("fall"), 0.8)
    l = hl(s, CLOSE, 300, 900, GRN2, 6, "14 9"); s.fade(l, K("close") + 0.2, 0.3)
    t = tag(s, 470, sy(CLOSE) + 60, f"CLOSE BOTH {px(CLOSE)}", GRN2, "#fff", 36); s.pop(t, K("close") + 0.3, 0.35, 0.5)
    p1 = tag(s, 760, 880, f"+{S1 - CLOSE:.2f}", GRN2, "#fff", 40); s.pop(p1, K("pts") + 0.2, 0.35, 0.5)
    p2 = tag(s, 760, 980, f"+{S2 - CLOSE:.2f}", GRN2, "#fff", 40); s.pop(p2, KW("pts", 4), 0.35, 0.5)
chart(s, x4)
cue(K("lh") + 1.6, "whoosh-short_2", -22); cue(K("close") + 0.3, "bell_G5", -20)
subtitle(s, [(o4 + 0.1, [("Then the ", INK), ("structure breaks", RED2)]), (K("lh") - 0.1, [("Bounce into the next ", INK), ("SBR", RED2), (": fails", INK)]),
             (K("fall") - 0.1, [("And keeps falling", INK)]), (K("close") - 0.1, [("Closed both at ", INK), (px(CLOSE), GRN2)]),
             (K("pts") - 0.1, [("+96.37", GRN2), (" and ", INK), ("+78.37", GRN2), (" per ounce", INK)])], c4)

# 5  the deals list: the loss, and the net for the day
o5, c5 = K("loss") - 0.1, K("recap") - 0.1
s = S(o5, c5)
slide_bg(s)
bot = shot_open(s, crop=DEALS, panel=(40, 430, 1000))
r1 = boxhl(s, (392, 335, 1080, 400), GRN2); s.pop(r1, o5 + 0.3, 0.35, 0.6)
r3 = boxhl(s, (392, 528, 1080, 593), GRN2); s.pop(r3, o5 + 0.45, 0.35, 0.6)
r2 = boxhl(s, (392, 432, 1080, 497), RED2); s.pop(r2, K("loss") + 0.6, 0.35, 0.6)
shot_close(s)
bot2 = shot_open(s, crop=PROFIT, panel=(40, bot + 40, 1000))
r4 = boxhl(s, (392, 678, 1080, 706), GRN2); s.pop(r4, K("net"), 0.35, 0.6)
shot_close(s)
pn = s.raw(f'<text id="@ID@" x="540" y="{bot2 + 160:.0f}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="120" '
           f'fill="{GRN2}" style="opacity:0">+$102,444</text>', "pn")
s.pop(pn, KW("net", 4), 0.5, 0.5); cue(KW("net", 4), "bell_A4", -16)
note(s, "* from my MT5 deals, 6 Nov 2026 (swap +371.04 not included)", bot2 + 230)
cue(K("loss") + 0.6, "swell_2", -24)
subtitle(s, [(o5 + 0.1, [("One buy stopped out: ", INK), ("-2,400", RED2)]), (K("net") - 0.1, [("Net for the day: ", INK), ("+$102,444", GRN2)])], c5)

# 6  summary
o6, c6 = K("recap") - 0.1, K("order") - 0.05
s = S(o6, c6)
slide_bg(s)
s.label(540, 470, "Summary of this trade", 44, RED2, 1, 800, 0.02)
rows = [("1", [("Order block", ORG), (" at the top: sell #1", INK)], KW("recap", 0)),
        ("2", [("SBR", RED2), (": sell #2 on the way back up", INK)], KW("recap", 2)),
        ("3", [("Wait for the ", INK), ("structure", RED2), (" to break", INK)], KW("recap", 3)),
        ("4", [("Let price do the work: ", INK), ("+$102,444", GRN2)], K("let"))]
for k, (n, parts, t) in enumerate(rows):
    yy = 600 + 150 * k
    card = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="80" y="{yy - 52}" width="920" height="104" rx="22" fill="#f4f5f7" stroke="#e3e5e8" stroke-width="2"/>'
                 f'<circle cx="140" cy="{yy}" r="30" fill="{RED2}"/><text x="140" y="{yy + 12}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="32" fill="#fff">{n}</text>'
                 f'<text x="190" y="{yy + 12}" font-family="Montserrat" font-weight="700" font-size="31">'
                 + "".join(f'<tspan fill="{c}">{tx}</tspan>' for tx, c in parts) + "</text></g>", "rw")
    s.fade(card, t, 0.35, y=14); cue(t, "swell_2" if k == 3 else "bell_C5", -26)
lv = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="160" y="1210" width="760" height="90" rx="45" fill="{GRN2}"/>'
           f'<text x="540" y="1268" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" fill="#fff">OB · SBR · Structure · Patience</text></g>', "lv")
s.pop(lv, K("let") + 0.6, 0.4, 0.7)
subtitle(s, [(o6 + 0.1, [("Recap: ", INK), ("OB, SBR, wait for structure", RED2)])], c6)

outro(K("order") - 0.05)
write()
