"""OTM trade recap, 23 Nov 2026: two XAUUSD trades on the 30M, built from the trader's own screenshots, in the same
white-slide layout as otm-recap-1106 / 1116.
  assets/m30.png      30M chart: CRT range (CRH 3,587, CRL ~3,520), sweep to the low 3,502.99, long position tool
                      (entry 3,503.93, SL 3,500.05, TP 3,587), sell position tool (entry 3,690, SL 3,697.137, TP 3,630)
  assets/account.jpg  MT5 history: buy 15 @3504.00 -> 3587.00 +124,500.00 (closed 2026.11.23 01:31:00) and the account
                      summary taken before the sell closed (not shown).
  assets/account2.jpg updated account summary after both trades: deposit 100.00, credit 20.00, withdrawal
                      -150,000.00, profit 285,850.36 (rows Deposit..Profit shown; the Balance row is cropped out because
                      its 285,950.36 does not net the withdrawal).
  assets/sell.jpg     sell 8 @3690.00 -> 3630.00 +48,000.00 (closed 2026.11.23 21:37:41)
The trader asked for the account summary to be shown. English (Quentin)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *

LANG = "en"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = "otm-recap-1123"
TOTAL = init(ROOT, LANG, COMP, "mix_recap1123")
def KW(key, n): return W(G["marks"][key] + n)

INK, RED2, GRN2, ORG, BLU = "#111111", "#e0322b", "#1f9d55", "#f08a24", "#2962ff"
def px(p): return f"{p:,.2f}"

# 30M chart (1320 x 2868): CRH 3,587 at y 1700, 7.186 px per dollar (axis 3,600 at y 1601, 3,740 at y 595)
def ym(p): return 1700 + (3587.0 - p) * 7.186

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


BE, BSL_, BTP = 3503.93, 3500.05, 3587.00          # buy position tool: entry, SL, TP (= CRH)
SE, SSL_, STP = 3690.00, 3697.137, 3630.00          # sell position tool
CRL = 3520.3
M30 = ("assets/m30.png", (1320, 2868), (0, 850, 1320, 1530))
RX0, RX1 = 318, 549                                  # their CRH / CRL / zone lines
TX = 860                                             # tags in the empty space right of the price action

# 1  hook
o1, c1 = 0, K("crt") - 0.1
s = S(o1, c1, first=True)
slide_bg(s)
def x1():
    tag(s, TX, 1180, "+$172,500", GRN2, "#fff", 72, 1)
    tag(s, TX, 1290, "2 TRADES · 23 NOV", INK, "#fff", 36, 1)
chart(s, *M30, x1)
subtitle(s, [(0.05, [("Gold, 23 Nov: ", INK), ("two trades", RED2)]), (K("result") - 0.1, [("Together: ", INK), ("+$172,500", GRN2)])], c1)
cue(0.3, "whoosh-short_1", -22)

# 2  the CRT buy
o2, c2 = K("crt") - 0.1, K("buypnl") - 0.1
s = S(o2, c2)
slide_bg(s)
def x2():
    t0 = tag(s, TX, 1520, "CRT · 30M", INK, "#fff", 40); s.pop(t0, K("crt") + 0.3, 0.35, 0.5); out(t0, K("tp") - 0.2)
    r = boxhl(s, (RX0, ym(BTP), RX1, ym(CRL)), ORG, pad=6); s.pop(r, K("range") + 0.3, 0.4, 0.6); out(r, K("sweep"), 0.3, 0.35)
    th = tag(s, TX, ym(BTP), "CRH 3,587", ORG, "#fff", 36); s.pop(th, KW("range", 5), 0.35, 0.5); out(th, K("sweep"))
    tl_ = tag(s, TX, ym(CRL), "CRL ~3,520", ORG, "#fff", 36); s.pop(tl_, KW("range", 9), 0.35, 0.5); out(tl_, K("sweep"))
    rg = ring(s, 408, 2290, 34, RED2); s.pop(rg, K("sweep") + 0.4, 0.35, 0.3)
    sw = tag(s, TX, 2175, "SWEPT BELOW CRL", RED2, "#fff", 34); s.pop(sw, K("sweep") + 0.5, 0.35, 0.5)
    le = hline(s, ym(BE), RX0, 760, BLU, 6, glow=True); s.fade(le, K("entry") + 0.3, 0.3)
    te = tag(s, TX, 2262, "BUY 15 @ 3,504", BLU, "#fff", 36); s.pop(te, KW("entry", 3), 0.35, 0.5)
    ls = hline(s, ym(BSL_), RX0, 760, RED2, 5, "12 8"); s.fade(ls, K("sl") + 0.2, 0.3)
    ts = tag(s, 780, 2348, "SL 3,500.05", RED2, "#fff", 32); s.pop(ts, KW("sl", 4), 0.35, 0.5)
    lt = hline(s, ym(BTP), RX0, 760, GRN2, 7, glow=True); s.fade(lt, K("tp") + 0.2, 0.3)
    tt = tag(s, TX, ym(BTP), "TP = CRH 3,587", GRN2, "#fff", 38); s.pop(tt, K("tp") + 0.5, 0.35, 0.5)
    ar = arrow(s, 425, 2240, 468, 1745, GRN2, 10, 36); show_arrow(s, ar, K("hit") + 0.2, 0.8)
    ck = check(s, 470, 1640, 28, GRN2, 9); s.draw(ck, K("hit") + 1.1, 0.35)
chart(s, *M30, x2)
cue(K("range") + 0.3, "bell_G4", -22); cue(K("entry") + 0.3, "bell_E5", -22); cue(K("hit") + 0.2, "whoosh-short_2", -22); cue(K("hit") + 1.1, "bell_G5", -20)
subtitle(s, [(o2 + 0.1, [("Trade 1: a ", INK), ("CRT", ORG), (" on the 30M", INK)]),
             (K("range") - 0.1, [("The range: ", INK), ("CRH 3,587", ORG), (" / ", INK), ("CRL ~3,520", ORG)]),
             (K("sweep") - 0.1, [("Price ", INK), ("sweeps below the CRL", RED2)]),
             (K("entry") - 0.1, [("Buy 15 lots at ", INK), ("3,504", BLU)]),
             (K("sl") - 0.1, [("Stop at ", INK), ("3,500", RED2), (": under $4 of risk", INK)]),
             (K("tp") - 0.1, [("Target: the ", INK), ("range high", GRN2)]),
             (K("hit") - 0.1, [("Price runs back up and ", INK), ("hits it", GRN2)])], c2)

def result_slide(o, c, img, size, crop, box, t_box, big, t_big, line2, t2, note):
    s = S(o, c)
    slide_bg(s)
    bot = shot_open(s, img, size, crop, panel=(40, 560, 1000))
    b = boxhl(s, box, GRN2, pad=4); s.pop(b, t_box, 0.35, 0.6)
    shot_close(s)
    s.label(540, bot + 40, note, 22, "#8a8f98", 1, 600, 0.02)
    pn = s.raw(f'<text id="@ID@" x="540" y="{bot + 230:.0f}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="130" '
               f'fill="{GRN2}" style="opacity:0">{big}</text>', "pn")
    s.pop(pn, t_big, 0.5, 0.5); cue(t_big, "bell_A4", -16)
    l2 = tag(s, 540, bot + 330, line2, INK, "#fff", 36); s.pop(l2, t2, 0.35, 0.5)
    return s

# 3  the buy result
o3, c3 = K("buypnl") - 0.1, K("next") - 0.1
s = result_slide(o3, c3, "assets/account.jpg", (1320, 874), (0, 0, 1320, 175), (14, 30, 1306, 165), K("buypnl") + 0.2,
                 "+$124,500", KW("buypnl", 6), "+83.00 × 15 LOTS · CLOSED AT CRH", K("buypnl") + 0.4, "* my MT5 history, 23 Nov 2026, closed 01:31")
subtitle(s, [(o3 + 0.1, [("$83 on 15 lots: ", INK), ("+$124,500", GRN2)])], c3)

# 4  the sell
o4, c4 = K("next") - 0.1, K("sellpnl") - 0.1
s = S(o4, c4)
slide_bg(s)
def x4():
    up = arrow(s, 495, 1640, 585, 1010, BLU, 9, 32); show_arrow(s, up, K("next") + 0.3, 0.8)
    z = boxhl(s, (RX0, ym(SSL_), RX1, ym(SE)), RED2, pad=8); s.pop(z, K("zone") + 0.5, 0.4, 0.6)
    tz = tag(s, TX, 1010, "SELL ZONE 3,690", RED2, "#fff", 38); s.pop(tz, KW("zone", 5), 0.35, 0.5)
    ts = tag(s, TX, 1090, "SELL 8 · SL 3,697", INK, "#fff", 34); s.pop(ts, K("sell") + 0.3, 0.35, 0.5)
    lt = hline(s, ym(STP), RX0, 760, GRN2, 7, glow=True); s.fade(lt, K("tp2") + 0.2, 0.3)
    tt = tag(s, TX, 1450, "TP 3,630", GRN2, "#fff", 38); s.pop(tt, K("tp2") + 0.5, 0.35, 0.5)
    dn = arrow(s, 600, 1000, 655, 1370, GRN2, 10, 34); show_arrow(s, dn, K("hit2") + 0.2, 0.7)
chart(s, *M30, x4)
cue(K("zone") + 0.5, "bell_E5", -22); cue(K("hit2") + 0.2, "whoosh-short_1", -22)
subtitle(s, [(o4 + 0.1, [("Then price ", INK), ("keeps running", BLU)]),
             (K("zone") - 0.1, [("Into my ", INK), ("sell zone", RED2), (" at 3,690", INK)]),
             (K("sell") - 0.1, [("Sell 8 lots, ", INK), ("SL 3,697", RED2)]),
             (K("tp2") - 0.1, [("Target: ", INK), ("3,630", GRN2)]),
             (K("hit2") - 0.1, [("Price falls ", INK), ("$60", GRN2)])], c4)

# 5  the sell result
o5, c5 = K("sellpnl") - 0.1, K("acct") - 0.1
s = result_slide(o5, c5, "assets/sell.jpg", (1320, 180), (0, 30, 1320, 150), (14, 48, 1306, 150), K("sellpnl") + 0.2,
                 "+$48,000", K("sellpnl") + 0.3, "+60.00 × 8 LOTS · CLOSED AT TP", K("sellpnl") + 0.6, "* my MT5 history, 23 Nov 2026, closed 21:37")
subtitle(s, [(o5 + 0.1, [("Sell: ", INK), ("+$48,000", GRN2)])], c5)

# 6  the account (shown at the trader's request)
o6, c6 = K("acct") - 0.1, K("recap") - 0.1
s = S(o6, c6)
slide_bg(s)
bot = shot_open(s, "assets/account2.jpg", (1320, 504), (0, 12, 1320, 262), panel=(40, 520, 1000))
for b, t, col in [((14, 25, 1306, 78), K("dep") + 0.3, BLU), ((14, 214, 1306, 259), K("profit") + 0.3, GRN2), ((14, 152, 1306, 196), K("wd") + 0.2, ORG)]:
    h = boxhl(s, b, col, pad=4); s.pop(h, t, 0.35, 0.6)
shot_close(s)
s.label(540, bot + 40, "* my MT5 account history", 22, "#8a8f98", 1, 600, 0.02)
d = tag(s, 540, bot + 120, "FROM A $100 DEPOSIT", BLU, "#fff", 40); s.pop(d, K("dep") + 0.4, 0.35, 0.5)
pf = s.raw(f'<text id="@ID@" x="540" y="{bot + 290:.0f}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="112" '
           f'fill="{GRN2}" style="opacity:0">+$285,850.36</text>', "pf")
s.pop(pf, KW("profit", 2), 0.5, 0.5); cue(KW("profit", 2), "bell_A4", -16)
pl = s.label(540, bot + 350, "TOTAL PROFIT", 30, INK, 0, 800, 0.08); s.fade(pl, KW("profit", 2) + 0.2, 0.3)
w = tag(s, 540, bot + 450, "$150,000 ALREADY WITHDRAWN", ORG, "#fff", 38); s.pop(w, K("wd") + 0.3, 0.35, 0.5); cue(K("wd") + 0.3, "swell_1", -24)
s.label(540, bot + 540, "Past results don't guarantee future ones.", 24, "#8a8f98", 1, 600, 0.02)
subtitle(s, [(o6 + 0.1, [("The ", INK), ("bigger picture", RED2)]),
             (K("dep") - 0.1, [("Started with a ", INK), ("$100", BLU), (" deposit", INK)]),
             (K("profit") - 0.1, [("Total profit: ", INK), ("+$285,850", GRN2)]),
             (K("wd") - 0.1, [("$150,000", ORG), (" already withdrawn", INK)])], c6)

# 7  summary
o7, c7 = K("recap") - 0.1, K("order") - 0.05
s = S(o7, c7)
slide_bg(s)
s.label(540, 470, "Summary of this trade", 44, RED2, 1, 800, 0.02)
rows = [("1", [("Wait for the ", INK), ("sweep", RED2), (" below the CRL", INK)], KW("recap", 0)),
        ("2", [("Buy", BLU), (" the range low, tight stop", INK)], KW("recap", 4)),
        ("3", [("Target the ", INK), ("range high", GRN2), (" (CRH)", INK)], KW("recap", 8))]
for k, (n, parts, t) in enumerate(rows):
    yy = 610 + 150 * k
    card = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="80" y="{yy - 52}" width="920" height="104" rx="22" fill="#f4f5f7" stroke="#e3e5e8" stroke-width="2"/>'
                 f'<circle cx="140" cy="{yy}" r="30" fill="{RED2}"/><text x="140" y="{yy + 12}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="32" fill="#fff">{n}</text>'
                 f'<text x="190" y="{yy + 12}" font-family="Montserrat" font-weight="700" font-size="31">'
                 + "".join(f'<tspan fill="{c}">{tx}</tspan>' for tx, c in parts) + "</text></g>", "rw")
    s.fade(card, t, 0.35, y=14); cue(t, "bell_C5", -26)
lv = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="160" y="1110" width="760" height="90" rx="45" fill="{GRN2}"/>'
           f'<text x="540" y="1168" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" fill="#fff">Then let price do the work</text></g>', "lv")
s.pop(lv, K("let"), 0.4, 0.7); cue(K("let"), "swell_2", -24)
subtitle(s, [(o7 + 0.1, [("Recap: ", INK), ("sweep, range low, range high", RED2)])], c7)

outro(K("order") - 0.05)
write()
