"""OTM trade recap, 6 Nov 2026: slide-style recap built on the trader's own screenshot (assets/trade.jpg, the MT5 deals
list and their 15-minute XAUUSD chart with their SHIFT / FVG / SBR / PDH / IDM / BoS markings), in the layout of the "Recap order XAUUSD"
reference reel: white slides, a red italic "Recap order XAUUSD" title, one subtitle line per beat, markings on the
real chart. The deals (assets/deals.jpg, both closed 2026.11.06 15:31:50):
  sell 6 lots 4133.00 -> 4036.63  +57,822.00   (under the high)
  sell 6 lots 4115.00 -> 4036.63  +47,022.00   (at their SBR)
  together +104,844.00. Their chart markings: SHIFT, FVG, SBR, PDH, IDM, BoS and a later sell zone.
  The stops are not given, so the video shows no RR.
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

# screenshot geometry (1320 x 2346), calibrated on their two entry lines (4133.00 at y 720.5, 4115.00 at y 955.5)
IMW, IMH = 1320, 2346
def sy(p): return 720.5 + (4133.00 - p) * 13.056
B1 = (156, 661, 272, 720)               # sell 1 position box (top part)
B2 = (402, 898, 520, 955)               # sell 2 box at their SBR
SHIFT_L, FVG_L, PDH_L, IDM_L, BOS_L = (23, 1023, 106, 1043), (158, 1416, 229, 1456), (1015, 1030, 1068, 1048), (793, 1420, 839, 1456), (917, 1965, 964, 1992)
ZONE = (909, 1271, 1103, 1396)          # their later sell zone
X_LOW, Y_LOW, X_TOP2, Y_TOP2 = 780, 1989, 939, 1402
CROP = (0, 600, IMW, 1530)
PANEL = (57, 372, 966)

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

def boxhl(s, b, col, op=0, w=7, pad=8):
    x0, y0, x1, y1 = b
    return s.raw(f'<rect id="@ID@" x="{x0 - pad}" y="{y0 - pad}" width="{x1 - x0 + 2 * pad}" height="{y1 - y0 + 2 * pad}" rx="10" fill="none" '
                 f'stroke="{col}" stroke-width="{w}" style="opacity:{op};filter:drop-shadow(0 0 8px {col})"/>', "bh")

def shot_open(s, crop=CROP, panel=PANEL, shadow=True, img="assets/trade.jpg", size=(IMW, IMH)):
    cx, cy, cw, ch_ = crop; x, y, w = panel
    h = w * ch_ / cw
    if shadow:
        s.raw(f'<rect id="@ID@" x="{x - 6}" y="{y - 6}" width="{w + 12}" height="{h + 12:.0f}" rx="18" fill="#ffffff" '
              f'stroke="#d9dce1" stroke-width="2" style="filter:drop-shadow(0 8px 24px rgba(0,0,0,0.18))"/>', "sh")
    s.items.append(f'<svg x="{x}" y="{y}" width="{w}" height="{h:.1f}" viewBox="{cx} {cy:.1f} {cw} {ch_:.1f}" preserveAspectRatio="none">'
                   f'<image href="{img}" x="0" y="0" width="{size[0]}" height="{size[1]}"/>')
    return y + h

def chart(s, extra=None):
    bot = shot_open(s)
    if extra: extra()
    shot_close(s)
    s.label(540, bot + 30, "* real trade, my own screenshot and markings", 20, "#8a8f98", 1, 600, 0.02)
    return bot

def base_lines(s, which=(1, 2)):
    if 1 in which: hl(s, S1, 150, 1100, RED2, 4, "14 9", 0.55)
    if 2 in which: hl(s, S2, 395, 1100, RED2, 4, "14 9", 0.55)

# 1  hook: the real chart and the result
o1, c1 = 0, K("why") - 0.1
s = S(o1, c1, first=True)
slide_bg(s)
def x1():
    tag(s, 330, 1700, "+$104,844", GRN2, "#fff", 72, 1)
    tag(s, 330, 1805, "2 SELLS  ·  6 NOV  ·  15M", INK, "#fff", 38, 1)
chart(s, x1)
subtitle(s, [(0.05, [("Gold, 6 Nov: ", INK), ("two sells", RED2)]), (K("result") - 0.1, [("Together: ", INK), ("+$104,844", GRN2)])], c1)
cue(0.3, "whoosh-short_1", -22)

# 2  the top and the first sell
o2, c2 = K("why") - 0.1, K("shift") - 0.1
s = S(o2, c2)
slide_bg(s)
def x2():
    b = boxhl(s, B1, RED2); s.pop(b, K("top") + 0.4, 0.4, 0.6)
    l = hl(s, S1, 150, 1100, RED2, 5, "14 9"); s.fade(l, K("sell1") + 0.2, 0.3)
    t2 = tag(s, 640, sy(S1) - 46, f"SELL #1  {px(S1)}", RED2, "#fff", 42); s.pop(t2, K("sell1") + 0.3, 0.35, 0.5)
chart(s, x2)
cue(K("top") + 0.4, "bell_G4", -22); cue(K("sell1") + 0.3, "bell_E5", -20)
subtitle(s, [(o2 + 0.1, [("The plan", INK)]), (K("top") - 0.1, [("Price stalls ", INK), ("under the high", RED2)]),
             (K("sell1") - 0.1, [("Sell #1 at ", INK), (px(S1), RED2)])], c2)

# 3  shift, FVG, the SBR and the second sell
o3, c3 = K("shift") - 0.1, K("idm") - 0.1
s = S(o3, c3)
slide_bg(s)
def x3():
    base_lines(s, (1,))
    a = boxhl(s, SHIFT_L, ORG); s.pop(a, K("shift") + 0.3, 0.35, 0.6)
    f = boxhl(s, FVG_L, ORG); s.pop(f, K("fvg") + 0.3, 0.35, 0.6)
    b = boxhl(s, B2, RED2); s.pop(b, K("sbr") + 1.2, 0.4, 0.6)
    l = hl(s, S2, 395, 1100, RED2, 5, "14 9"); s.fade(l, K("sell2") + 0.3, 0.3)
    t2 = tag(s, 760, sy(S2) - 46, f"SELL #2  {px(S2)}", RED2, "#fff", 42); s.pop(t2, K("sell2") + 0.4, 0.35, 0.5)
chart(s, x3)
cue(K("shift") + 0.3, "tick-crisp_1", -22); cue(K("sbr") + 1.2, "swell_1", -22); cue(K("sell2") + 0.4, "bell_E5", -20)
subtitle(s, [(o3 + 0.1, [("Structure ", INK), ("shifts", ORG), (" down", INK)]), (K("fvg") - 0.1, [("It leaves a ", INK), ("fair value gap", ORG)]),
             (K("sbr") - 0.1, [("Back up into the ", INK), ("SBR", RED2), (": old support", INK)]),
             (K("sell2") - 0.1, [("Sell #2 at ", INK), (px(S2), RED2)])], c3)

# 4  IDM, the low, the failed bounce, the close
o4, c4 = K("idm") - 0.1, K("pnl") - 0.1
s = S(o4, c4)
slide_bg(s)
def x4():
    base_lines(s)
    i = boxhl(s, IDM_L, ORG); s.pop(i, K("idm") + 0.3, 0.35, 0.6)
    r = ring(s, X_LOW, Y_LOW, 36, GRN2); s.pop(r, K("low") + 0.3, 0.35, 0.3)
    z = boxhl(s, ZONE, RED2, pad=4); s.pop(z, K("bounce") + 0.4, 0.4, 0.6)
    xm = xmark(s, X_TOP2 + 80, Y_TOP2 - 20, 26, RED2, 8); s.draw(xm, K("fail") + 0.1, 0.3)
    a = arrow(s, X_TOP2 + 60, Y_TOP2 + 60, 1080, sy(CLOSE) - 40, RED2, 9, 36); show_arrow(s, a, K("fail") + 0.5, 0.7)
    l = hl(s, CLOSE, 560, 1110, GRN2, 6, "14 9"); s.fade(l, K("close") + 0.2, 0.3)
    t = tag(s, 520, sy(CLOSE) + 70, f"CLOSE BOTH  {px(CLOSE)}", GRN2, "#fff", 40); s.pop(t, K("close") + 0.3, 0.35, 0.5)
    p1 = tag(s, 760, 760, f"+{S1 - CLOSE:.2f}", GRN2, "#fff", 46); s.pop(p1, K("pts") + 0.2, 0.35, 0.5)
    p2 = tag(s, 760, 860, f"+{S2 - CLOSE:.2f}", GRN2, "#fff", 46); s.pop(p2, KW("pts", 4), 0.35, 0.5)
chart(s, x4)
cue(K("idm") + 0.3, "tick-crisp_2", -22); cue(K("fail") + 0.5, "whoosh-short_2", -22); cue(K("close") + 0.3, "bell_G5", -20)
subtitle(s, [(o4 + 0.1, [("Price breaks the ", INK), ("IDM", ORG)]), (K("low") - 0.1, [("Runs to the ", INK), ("low", GRN2)]),
             (K("bounce") - 0.1, [("Bounces into the next ", INK), ("sell zone", RED2)]), (K("fail") - 0.1, [("Fails, and rolls over", INK)]),
             (K("close") - 0.1, [("Closed both at ", INK), (px(CLOSE), GRN2)]),
             (K("pts") - 0.1, [("+96.37", GRN2), (" and ", INK), ("+78.37", GRN2), (" per ounce", INK)])], c4)

# 5  the deals
o5, c5 = K("pnl") - 0.1, K("recap") - 0.1
s = S(o5, c5)
slide_bg(s)
bot = shot_open(s, crop=(0, 0, 1320, 327), panel=(40, 560, 1000), img="assets/deals.jpg", size=(1320, 327))
r1 = boxhl(s, (40, 18, 1290, 150), GRN2); s.pop(r1, KW("pnl", 3) + 0.4, 0.35, 0.6)
r2 = boxhl(s, (40, 178, 1290, 310), GRN2); s.pop(r2, KW("pnl", 7), 0.35, 0.6)
shot_close(s)
pn = s.raw(f'<text id="@ID@" x="540" y="{bot + 230:.0f}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="130" '
           f'fill="{GRN2}" style="opacity:0">+$104,844</text>', "pn")
s.pop(pn, KW("pnl", 3), 0.5, 0.5); cue(KW("pnl", 3), "bell_A4", -16)
s.label(540, bot + 320, "2 SELLS  ·  6 LOTS EACH  ·  CLOSED 15:31", 34, INK, 1, 800, 0.04)
s.label(540, bot + 390, "* my MT5 deals, 6 Nov 2026", 22, "#8a8f98", 1, 600, 0.02)
subtitle(s, [(o5 + 0.1, [("6 lots each: ", INK), ("+57,822", GRN2), (" and ", INK), ("+47,022", GRN2)])], c5)

# 6  summary
o6, c6 = K("recap") - 0.1, K("order") - 0.05
s = S(o6, c6)
slide_bg(s)
s.label(540, 470, "Summary of this trade", 44, RED2, 1, 800, 0.02)
rows = [("1", [("Shift", ORG), (" + FVG: the trend turns down", INK)], KW("recap", 0)),
        ("2", [("SBR", RED2), (": sell the rally into old support", INK)], KW("recap", 1)),
        ("3", [("IDM", ORG), (" breaks: sellers in control", INK)], KW("recap", 2)),
        ("4", [("Target the ", INK), ("low", GRN2), (": +$104,844", GRN2)], KW("recap", 3))]
for k, (n, parts, t) in enumerate(rows):
    yy = 600 + 150 * k
    card = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="80" y="{yy - 52}" width="920" height="104" rx="22" fill="#f4f5f7" stroke="#e3e5e8" stroke-width="2"/>'
                 f'<circle cx="140" cy="{yy}" r="30" fill="{RED2}"/><text x="140" y="{yy + 12}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="32" fill="#fff">{n}</text>'
                 f'<text x="190" y="{yy + 12}" font-family="Montserrat" font-weight="700" font-size="31">'
                 + "".join(f'<tspan fill="{c}">{tx}</tspan>' for tx, c in parts) + "</text></g>", "rw")
    s.fade(card, t, 0.35, y=14); cue(t, "bell_C5", -26)
lv = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="160" y="1210" width="760" height="90" rx="45" fill="{GRN2}"/>'
           f'<text x="540" y="1268" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" fill="#fff">Then let price do the work</text></g>', "lv")
s.pop(lv, K("let"), 0.4, 0.7); cue(K("let"), "swell_2", -24)
subtitle(s, [(o6 + 0.1, [("Recap: ", INK), ("shift, SBR, IDM, the low", RED2)])], c6)

outro(K("order") - 0.05)
write()
