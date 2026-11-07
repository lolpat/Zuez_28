"""OTM "The Trendline Break": a chart explainer in the glowing OTM style (same scene system as otm-chance / otm-believe).
An example chart (synthetic, work/chart.py) is built candle by candle as the narration (Quentin) walks through it:
impulse, complex W-X-Y-X-Z correction, the trend line across the falling highs, the break, the pullback, target 1, the
next leg and the failure case; then a 4-hour zoom (A-B-C, A-B-C with a triangle = W-X-Y), the question, and the outro.
Voice only, no music. Writes ../index.html, work/cues.json (soft kit sounds) and work/timing.json."""
import json, math, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAD = 0.3
GOLD, RED, WHITE, GREY, LBL = "#e8c26a", "#ff4d5e", "#ffffff", "#7d838c", "#c9ced6"
GY = 1240                                   # ground line
words = json.load(open(f"{ROOT}/work/words.json"))
def W(i): return round(words[i]["start"] + LEAD, 3)
def WE(i): return round(words[i]["end"] + LEAD, 3)
END_T = round(words[-1]["end"] + LEAD + 0.6, 2)
TOTAL = round(END_T + 1.0, 2)          # no end card: the outro holds, then fades out
rnd = random.Random(7)

T, CUES = [], []
def tl(s): T.append(s)
def cue(t, snd, gain): CUES.append(dict(t=round(t, 3), snd=snd, gain=gain))


class S:
    """Builds one scene's SVG and its tweens."""
    n = 0
    scenes = []

    def __init__(self, o, c, ground=True, first=False, restore=True, hide=True):
        S.n += 1
        self.id, self.o, self.c, self.items = f"sc{S.n}", o, c, []
        S.scenes.append(self)
        if first:
            tl(f'tl.set("#{self.id}", {{opacity: 1, visibility: "visible"}}, 0);')
        else:
            tl(f'tl.set("#{self.id}", {{visibility: "visible"}}, {o:.3f});')
            tl(f'tl.fromTo("#{self.id}", {{opacity: 0}}, {{opacity: 1, duration: 0.3, ease: "power2.out", immediateRender: false}}, {o:.3f});')
        tl(f'tl.fromTo("#{self.id}", {{scale: 1}}, {{scale: 1.035, transformOrigin: "50% 60%", duration: {c - o:.3f}, ease: "none", immediateRender: false}}, {o:.3f});')
        tl(f'tl.to("#{self.id}", {{opacity: 0, duration: 0.25, ease: "power2.in"}}, {c - 0.25:.3f});')
        tl(f'tl.set("#{self.id}", {{opacity: 0, visibility: "hidden"}}, {c:.3f});')
        if not ground and hide:
            tl(f'tl.to("#ground", {{opacity: 0, duration: 0.3}}, {o - 0.15:.3f});')
        if not ground and restore:
            tl(f'tl.to("#ground", {{opacity: 1, duration: 0.3}}, {c - 0.15:.3f});')

    def uid(self, p):
        S.n += 1
        return f"{p}{S.n}"

    def add(self, s, p="e"):
        i = self.uid(p)
        self.items.append(s.replace("@ID@", i))
        return i

    # ---- primitives ----
    def fig(self, x, s=1.0, col=WHITE, op=1.0, glow=True, gy=GY, dashed=False):
        f = (f'fill="none" stroke="{col}" stroke-width="5" stroke-dasharray="14 10"' if dashed else f'fill="{col}"')
        g = "filter:drop-shadow(0 0 16px rgba(255,255,255,0.55));" if glow and not dashed else ""
        return self.add(f'<g transform="translate({x},{gy}) scale({s})"><g id="@ID@" style="opacity:{op};{g}">'
                        f'<circle cx="0" cy="-158" r="31" {f}/><path d="M -48 0 L -48 -66 Q -48 -116 0 -116 Q 48 -116 48 -66 L 48 0 Z" {f}/></g></g>', "f")

    def spot(self, x, op=1.0, col="255,255,255", top=36, bot=150, gy=GY):
        gid = self.uid("gr")
        return self.add(f'<g id="@ID@" style="opacity:{op}"><defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
                        f'<stop offset="0" stop-color="rgb({col})" stop-opacity="0.26"/><stop offset="1" stop-color="rgb({col})" stop-opacity="0.04"/></linearGradient></defs>'
                        f'<path d="M {x - top} 380 L {x + top} 380 L {x + bot} {gy} L {x - bot} {gy} Z" fill="url(#{gid})"/>'
                        f'<ellipse cx="{x}" cy="{gy}" rx="{bot + 10}" ry="26" fill="none" stroke="rgb({col})" stroke-opacity="0.55" stroke-width="2" stroke-dasharray="8 8"/></g>', "sp")

    def label(self, x, y, text, size=28, col=LBL, op=0, weight=700, sp=0.18, anchor="middle"):
        return self.add(f'<text id="@ID@" x="{x}" y="{y}" text-anchor="{anchor}" font-family="Montserrat" font-weight="{weight}" font-size="{size}" '
                        f'letter-spacing="{sp}em" fill="{col}" style="opacity:{op}">{text}</text>', "t")

    def pill(self, x, y, text, fill=WHITE, tcol="#0b0b0b", size=28, op=0):
        w = len(text) * size * 0.74 + 52; h = size + 28
        return self.add(f'<g id="@ID@" style="opacity:{op}"><rect x="{x - w / 2:.0f}" y="{y - h / 2:.0f}" width="{w:.0f}" height="{h}" rx="{h / 2}" fill="{fill}" '
                        f'style="filter:drop-shadow(0 0 12px rgba(255,255,255,0.35))"/><text x="{x}" y="{y + size * 0.36:.0f}" text-anchor="middle" '
                        f'font-family="Montserrat" font-weight="800" font-size="{size}" letter-spacing="0.06em" fill="{tcol}">{text}</text></g>', "pl")

    def path(self, d, col=WHITE, w=4, fill="none", drawn=False, extra="", style=""):
        st = ("" if drawn else "stroke-dasharray:1 1.2;stroke-dashoffset:1.1;") + style
        dash = ('' if drawn else 'pathLength="1" ') + (f'style="{st}"' if st else "")
        return self.add(f'<path id="@ID@" d="{d}" fill="{fill}" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {dash} {extra}/>', "p")

    def raw(self, s, p="r"):
        return self.add(s, p)

    # ---- motion ----
    def draw(self, i, t, d=0.6, ease="power2.inOut"):
        tl(f'tl.fromTo("#{i}", {{strokeDashoffset: 1.1}}, {{strokeDashoffset: 0, duration: {d:.3f}, ease: "{ease}", immediateRender: false}}, {t:.3f});')

    def fade(self, i, t, d=0.35, to=1, frm=0, y=0):
        a = f", y: {y}" if y else ""; b = ", y: 0" if y else ""
        tl(f'tl.fromTo("#{i}", {{opacity: {frm}{a}}}, {{opacity: {to}{b}, duration: {d:.3f}, ease: "power2.out", immediateRender: false}}, {t:.3f});')

    def pop(self, i, t, d=0.4, frm=0.4, origin="50% 100%"):
        if t > self.o + 0.05:                                   # hidden until its pop, even if drawn visible
            tl(f'tl.set("#{i}", {{opacity: 0}}, {self.o:.3f});')
        tl(f'tl.fromTo("#{i}", {{opacity: 0, scale: {frm}, transformOrigin: "{origin}"}}, {{opacity: 1, scale: 1, duration: {d:.3f}, ease: "back.out(1.8)", immediateRender: false}}, {t:.3f});')

    def walk(self, i, t, dx, d):
        tl(f'tl.to("#{i}", {{x: "+={dx}", duration: {d:.3f}, ease: "power1.inOut"}}, {t:.3f});')
        steps = max(1, int(d / 0.18))
        tl(f'tl.to("#{i}", {{y: -7, duration: {d / (2 * steps):.3f}, yoyo: true, repeat: {2 * steps - 1}, ease: "sine.inOut"}}, {t:.3f});')


def rrect(x, y, w, h, r):
    return (f"M {x + r} {y} H {x + w - r} Q {x + w} {y} {x + w} {y + r} V {y + h - r} Q {x + w} {y + h} {x + w - r} {y + h} "
            f"H {x + r} Q {x} {y + h} {x} {y + h - r} V {y + r} Q {x} {y} {x + r} {y} Z")

def mini_curve(x, y, w=110, h=50, up=True):
    pts = [(0, 0.85), (0.2, 0.6), (0.35, 0.72), (0.55, 0.4), (0.7, 0.5), (1.0, 0.05)] if up else [(0, 0.1), (0.3, 0.3), (0.45, 0.2), (0.7, 0.7), (1, 0.95)]
    return "M " + " L ".join(f"{x + px * w:.0f} {y + py * h:.0f}" for px, py in pts)

# ================================================================================================= scenes
import re as _re
def _n(x): return _re.sub(r"[^a-z0-9']", "", x.lower())
def F(word, k=1):
    c = 0
    for i, w in enumerate(words):
        if _n(w["text"]) == word:
            c += 1
            if c == k: return i
    raise KeyError((word, k))
def A(word, k=1): return W(F(word, k))

def xmark(s, x, y, r=60, col=RED):
    return s.path(f"M {x - r} {y - r} L {x + r} {y + r} M {x + r} {y - r} L {x - r} {y + r}", col, 7)


# ================================================================================================= scenes (spliced into gen.py)
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chart import Chart, line_at, DAILY, DAILY_N, DAILY_LABELS, TL, CH_TOP, CH_BOT_AT, PULL, TGT_I, NEXT, FAIL, H4, H4_LABELS, H4_TL, TRI

BLUE = "#7b93ff"
CAP_Y = 1352                                   # caption line under the chart

def ix(i): return W(i)                         # start of word i on the video clock

D = Chart(DAILY, DAILY_N, 3); D.cap_below(*TL, 73, 96)
H = Chart(H4, 86, 5, noise=1.3); H.cap_below(*H4_TL, 17, 74)

def seg(c, a, b, i0, i1):
    x0, y0 = c.xy(i0, line_at(a, b, i0)); x1, y1 = c.xy(i1, line_at(a, b, i1))
    return f"M {x0} {y0} L {x1} {y1}"

def poly(c, pts):
    return "M " + " L ".join("%s %s" % c.xy(i, p) for i, p in pts)

def arrowhead(c, a, b, col, size=22):
    (x0, y0), (x1, y1) = c.xy(*a), c.xy(*b)
    ang = math.atan2(y1 - y0, x1 - x0)
    pts = [(x1, y1), (x1 - size * math.cos(ang - 0.45), y1 - size * math.sin(ang - 0.45)), (x1 - size * math.cos(ang + 0.45), y1 - size * math.sin(ang + 0.45))]
    return " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)

def candles_clip(s, c, i1=None, op=1.0):
    """all candles in one group behind a clip rect; returns the clip rect id (tween its width to reveal)"""
    cid = s.uid("cp")
    rid = s.uid("cr")
    s.items.append(f'<defs><clipPath id="{cid}"><rect id="{rid}" x="0" y="0" width="0" height="1920"/></clipPath></defs>')
    s.raw(f'<g id="@ID@" clip-path="url(#{cid})" style="opacity:{op}">' + "".join(c.candles(0, i1)) + "</g>", "cg")
    return rid

def reveal(rid, c, keys, t_open):
    """keys: [(t, idx), ...] in time order; the clip edge sits just past candle idx at time t"""
    sp = (c.x1 - c.x0) / c.nx
    def w(i): return round(c.x(i) + sp * 0.6, 1)
    tl(f'tl.set("#{rid}", {{attr: {{width: {w(keys[0][1])}}}}}, {t_open:.3f});')
    for (t0, i0), (t1, i1) in zip(keys, keys[1:]):
        tl(f'tl.fromTo("#{rid}", {{attr: {{width: {w(i0)}}}}}, {{attr: {{width: {w(i1)}}}, duration: {max(0.05, t1 - t0):.3f}, ease: "none", immediateRender: false}}, {t0:.3f});')

def t_at(keys, idx):
    """time the reveal edge passes candle idx"""
    for (t0, i0), (t1, i1) in zip(keys, keys[1:]):
        if i0 <= idx <= i1:
            return t0 + (t1 - t0) * (idx - i0) / max(1e-6, i1 - i0)
    return keys[-1][0]

def wave_label(s, c, i, p, text, kind, col, size=30):
    x, y = c.xy(i, p)
    y = y - 22 if kind == "hi" else y + 46
    return s.label(x, y, text, size, col, 0, 800, 0.02)

def captions(s, items, end):
    """items: [(t, text, col)]; each holds until the next one"""
    for k, (t, text, col) in enumerate(items):
        t_end = items[k + 1][0] if k + 1 < len(items) else end
        i = s.label(540, CAP_Y, text, 32, col, 0, 800, 0.06)
        s.fade(i, t, 0.3, y=10)
        tl(f'tl.to("#{i}", {{opacity: 0, duration: 0.15}}, {t_end - 0.18:.3f});')

def header(s, text):
    s.label(540, 500, text, 28, GREY, 1, 700, 0.22)

# 1  a trend line just broke; here's how to read it   (frame 0 is the thumbnail: the whole chart, the line, the break)
s = S(0, ix(10) - 0.15, ground=False, first=True, restore=False, hide=False)
s.label(540, 360, "THE TRENDLINE", 64, WHITE, 1, 800, 0.06)
s.label(540, 440, "BREAK", 64, GOLD, 1, 800, 0.12)
s.raw(f'<g id="@ID@" style="opacity:0.75">' + "".join(D.candles(0, 98)) + "</g>", "cg")
s.path(seg(D, *TL, 71, 104), WHITE, 5, drawn=True, style='filter:drop-shadow(0 0 8px rgba(255,255,255,0.6))')
bx, by = D.xy(96.3, line_at(*TL, 96.3))
ring = s.raw(f'<circle id="@ID@" cx="{bx}" cy="{by}" r="34" fill="none" stroke="{GOLD}" stroke-width="5" style="filter:drop-shadow(0 0 12px {GOLD})"/>', "c")
tl(f'tl.fromTo("#{ring}", {{scale: 1, transformOrigin: "50% 50%"}}, {{scale: 1.25, duration: 0.6, yoyo: true, repeat: 3, ease: "sine.inOut"}}, 0.2);')
bk = s.pill(bx - 10, by - 92, "BROKEN", GOLD, "#111", 28, 1)
hw = s.label(540, CAP_Y, "HOW TO READ IT", 32, WHITE, 0, 800, 0.1); s.fade(hw, ix(6), 0.35, y=10); cue(ix(4), "tick-crisp_1", -18)

# 2  the daily chart, built as the voice walks through it
open2, close2 = ix(10) - 0.15, ix(131) - 0.1
s = S(open2, close2, ground=False, restore=False, hide=False)
header(s, "DAILY  ·  EXAMPLE CHART")
rid = candles_clip(s, D, 98)
keys = [(ix(10), 0), (ix(17) + 0.1, 40), (ix(19), 40), (ix(27), 48), (ix(28), 55), (ix(29), 66), (ix(31), 73), (ix(33), 90), (ix(59), 90), (ix(61) + 0.3, 97)]
reveal(rid, D, keys, open2)
for k, (i, p, text, kind) in enumerate(DAILY_LABELS):
    lab = wave_label(s, D, i, p, text, kind, WHITE if k < 5 else BLUE)
    t = t_at(keys, i) if k < 5 else W([27, 28, 29, 31, 33][k - 5])
    s.pop(lab, t - 0.05, 0.3, 0.4, "50% 50%")
    cue(t, "tick_" + str(k % 3 + 1) if k < 5 else "tock_1", -24 if k < 5 else -21)
imp = s.path(poly(D, [(1, 40), (19, 74)]), GOLD, 5); s.draw(imp, ix(18) - 0.1, 0.5)
imh = s.raw(f'<polygon id="@ID@" points="{arrowhead(D, (1, 40), (19, 74), GOLD)}" fill="{GOLD}" style="opacity:0"/>', "ah"); s.pop(imh, ix(18) + 0.35, 0.2, 0.5, "50% 50%")
iml = s.label(210, D.y(80), "IMPULSE", 30, GOLD, 0, 800, 0.12); s.fade(iml, ix(18), 0.35); cue(ix(18), "swell_1", -22)
# the trend line across the falling highs, its two touches, the sellers' side
tlw = s.path(seg(D, *TL, 71, 106), WHITE, 5, style='filter:drop-shadow(0 0 8px rgba(255,255,255,0.55))'); s.draw(tlw, ix(39), 1.0)
cue(ix(39), "whoosh-short_1", -22)
for k, (i, p) in enumerate(TL):
    x, y = D.xy(i, p)
    dot = s.raw(f'<circle id="@ID@" cx="{x}" cy="{y}" r="10" fill="none" stroke="#fff" stroke-width="3" style="opacity:0"/>', "c"); s.pop(dot, ix(44) + k * 0.25, 0.3, 0.3, "50% 50%")
shade = [(i, line_at(*TL, i)) for i in (73, 96)] + [(i, line_at(*TL, i) - 16) for i in (96, 73)]
s.items.append(f'<defs><linearGradient id="shg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{RED}" stop-opacity="0.32"/>'
               f'<stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient></defs>')
sh = s.raw(f'<path id="@ID@" d="{poly(D, shade)} Z" fill="url(#shg)" style="opacity:0"/>', "sh")
s.fade(sh, ix(46), 0.5); tl(f'tl.to("#{sh}", {{opacity: 0, duration: 0.4}}, {ix(59) - 0.2:.3f});')
tlg = s.path(seg(D, *TL, 71, 106), GOLD, 5, drawn=True, style='opacity:0;filter:drop-shadow(0 0 12px rgba(232,194,106,0.8))')
s.fade(tlg, ix(56) - 0.2, 0.4); cue(ix(56) - 0.2, "bell_C5", -22)
# the break
ring2 = s.raw(f'<circle id="@ID@" cx="{bx}" cy="{by}" r="30" fill="none" stroke="{GOLD}" stroke-width="5" style="opacity:0;filter:drop-shadow(0 0 12px {GOLD})"/>', "c")
s.pop(ring2, ix(61) + 0.2, 0.4, 0.3, "50% 50%"); cue(ix(61) + 0.2, "land-light_1", -18)
tl(f'tl.to("#{ring2}", {{opacity: 0, duration: 0.3}}, {ix(84) - 0.3:.3f});')
ne = s.pill(bx - 30, by - 110, "NOT THE ENTRY", RED, WHITE, 28)
s.pop(ne, ix(76) - 0.1, 0.35, 0.5, "50% 50%"); tl(f'tl.to("#{ne}", {{opacity: 0, duration: 0.3}}, {ix(79) - 0.1:.3f});'); cue(ix(76), "click_2", -20)
# the ideal path: pullback holds above the line, new impulse to the channel top, then the next leg
B0 = (97, 44); TG = (TGT_I, line_at(*CH_TOP, TGT_I))
p1 = s.path(poly(D, [B0, PULL]), GOLD, 5); s.draw(p1, ix(84), 0.5)
hd = s.raw(f'<circle id="@ID@" cx="{D.x(PULL[0])}" cy="{D.y(PULL[1])}" r="11" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 10px {GOLD})"/>', "c"); s.pop(hd, ix(86), 0.3, 0.3, "50% 50%")
hl = s.label(D.x(PULL[0]) + 22, D.y(PULL[1]) + 10, "HOLDS", 28, GOLD, 0, 800, 0.1, "start"); s.fade(hl, ix(86), 0.3); cue(ix(86), "pop_1", -20)
p2 = s.path(poly(D, [PULL, TG]), GOLD, 5); s.draw(p2, ix(92), 0.6); cue(ix(92), "whoosh-short_2", -22)
ct = s.path(seg(D, *CH_TOP, 46, 124), BLUE, 3); s.draw(ct, ix(96), 0.8)
cbot = ((CH_BOT_AT[0], CH_BOT_AT[1]), (CH_BOT_AT[0] + 10, CH_BOT_AT[1] + line_at(*CH_TOP, 10) - line_at(*CH_TOP, 0)))
cb = s.path(seg(D, *cbot, 46, 124), BLUE, 3); s.draw(cb, ix(96) + 0.2, 0.8)
tr = s.raw(f'<circle id="@ID@" cx="{D.x(TG[0])}" cy="{D.y(TG[1])}" r="22" fill="none" stroke="{GOLD}" stroke-width="5" style="opacity:0;filter:drop-shadow(0 0 10px {GOLD})"/>', "c")
s.pop(tr, ix(100), 0.35, 0.3, "50% 50%"); cue(ix(100), "bell_E5", -20)
tt = s.label(D.x(TG[0]) + 32, D.y(TG[1]) + 11, "T1", 30, GOLD, 0, 800, 0.06, "start"); s.fade(tt, ix(100), 0.3)
p3 = s.path(poly(D, [TG, NEXT]), GOLD, 5); s.draw(p3, ix(106), 0.6)
p3h = s.raw(f'<polygon id="@ID@" points="{arrowhead(D, TG, NEXT, GOLD)}" fill="{GOLD}" style="opacity:0"/>', "ah"); s.pop(p3h, ix(106) + 0.55, 0.2, 0.5, "50% 50%")
nl = s.label(D.x(NEXT[0]) - 30, D.y(NEXT[1]) - 6, "NEXT LEG UP", 28, GOLD, 0, 800, 0.1, "end"); s.fade(nl, ix(111), 0.35); cue(ix(106), "swell_2", -20)
# the failure: back below the line, the idea is wrong
pf = s.path(poly(D, [PULL, FAIL]), RED, 5); s.draw(pf, ix(118), 0.6); cue(ix(118), "whoosh-short_3", -22)
xf = xmark(s, D.x(FAIL[0]), D.y(FAIL[1]) + 6, 18); s.draw(xf, ix(126) - 0.1, 0.3); cue(ix(126), "tock_1", -18)
for i in (p1, p2, p3, p3h, hd, hl):
    tl(f'tl.to("#{i}", {{opacity: 0.35, duration: 0.4}}, {ix(118) - 0.1:.3f});')
captions(s, [(open2 + 0.1, "THE BIG TREND IS UP", WHITE), (ix(21) - 0.2, "THEN A COMPLEX CORRECTION", WHITE),
             (ix(39) - 0.1, "ONE LINE ACROSS THE FALLING HIGHS", WHITE), (ix(46), "BELOW IT, SELLERS ARE IN CONTROL", RED),
             (ix(52), "THE LINE TO WATCH", GOLD), (ix(58), "A CLEAN CLOSE ABOVE IT", WHITE), (ix(65), "THE CORRECTION MAY BE ENDING", WHITE),
             (ix(72), "THE BREAK IS NOT THE ENTRY", RED), (ix(80) - 0.1, "A PULLBACK THAT HOLDS", GOLD), (ix(90), "THEN A NEW IMPULSE", GOLD),
             (ix(95), "TARGET 1: THE CHANNEL TOP", GOLD), (ix(104), "BREAKS WITH STRENGTH: NEXT LEG", GOLD),
             (ix(115), "BACK BELOW THE LINE: WRONG", RED), (ix(127) - 0.1, "SMALL LOSS. NEXT TRADE.", WHITE)], close2)

# 3  zoom into the 4-hour chart: A B C, then A B C with a triangle inside; two corrections joined as W X Y
open3, close3 = ix(131) - 0.1, ix(160) - 0.1
s = S(open3, close3, ground=False, restore=True, hide=False)
header(s, "4-HOUR  ·  EXAMPLE CHART")
zid = s.uid("zm")
s.items.append(f'<g id="{zid}">')
rid3 = candles_clip(s, H)
k3 = [(open3 + 0.2, 1), (ix(136), 10), (ix(139), 16), (ix(143), 28), (ix(144) + 0.2, 35), (ix(146), 42), (ix(147), 59), (ix(148) + 0.25, 68),
      (ix(153), 68), (ix(155), 77)]
reveal(rid3, H, k3, open3)
for k, (i, p, text, kind) in enumerate(H4_LABELS):
    lab = wave_label(s, H, i, p, text, kind, GOLD if text != "X" else BLUE)
    if k == 5: tl(f'tl.set("#{lab}", {{y: -18}}, {open3:.3f});')        # the triangle's B sits just under the trend line: lift it
    t = [ix(136), ix(139), ix(143), ix(158) + 0.05, ix(146), ix(147), ix(148)][k]
    s.pop(lab, t - 0.05, 0.3, 0.4, "50% 50%"); cue(t, ["tick_1", "tick_2", "tick_3", "tock_1", "tick_1", "tick_2", "tick_3"][k], -21)
tri_hi = [p for p in TRI if p[1] > 42.5]; tri_lo = [p for p in TRI if p[1] < 42.5]
for pts in (tri_hi, tri_lo):
    a, b = pts[0], pts[-1]
    tp = s.path(seg(H, a, b, a[0] - 1, b[0] + 3), WHITE, 3); s.draw(tp, ix(151) - 0.1, 0.5)
cue(ix(151), "pop_3", -20)
tlh = s.path(seg(H, *H4_TL, 12, 82), WHITE, 4, style='filter:drop-shadow(0 0 8px rgba(255,255,255,0.55))'); s.draw(tlh, ix(153) - 0.1, 0.9)
ar = s.path(poly(H, [(75, 34), (81, 52)]), GOLD, 5); s.draw(ar, ix(155) + 0.1, 0.4)
arh = s.raw(f'<polygon id="@ID@" points="{arrowhead(H, (75, 34), (81, 52), GOLD)}" fill="{GOLD}" style="opacity:0"/>', "ah"); s.pop(arh, ix(155) + 0.45, 0.2, 0.5, "50% 50%")
# brackets: W over the first A-B-C, Y over the second
for k, (i0, i1, text, t) in enumerate([(0, 28, "W", ix(157)), (35, 68, "Y", ix(159))]):
    yb = H.y(96 if k == 0 else 70)
    br = s.path(f"M {H.x(i0)} {yb + 16} V {yb} H {H.x(i1)} V {yb + 16}", GOLD, 3); s.draw(br, t - 0.2, 0.35)
    bl = s.label((H.x(i0) + H.x(i1)) / 2, yb - 16, text, 36, GOLD, 0, 800, 0.02); s.pop(bl, t - 0.05, 0.3, 0.4, "50% 50%")
    cue(t, "bell_" + ["G4", "C5"][k], -20)
s.items.append("</g>")
tl(f'tl.fromTo("#{zid}", {{scale: 1.5, opacity: 0.2, transformOrigin: "90% 70%"}}, {{scale: 1, opacity: 1, duration: 0.8, ease: "power3.out", immediateRender: false}}, {open3:.3f});')
cue(open3, "whoosh-long_1", -20)
captions(s, [(ix(134) - 0.2, "DOWN A · UP B · DOWN C", WHITE), (ix(144), "ANOTHER A-B-C, TRIANGLE INSIDE", WHITE),
             (ix(153), "TWO CORRECTIONS = W-X-Y", GOLD)], close3)

# 4  buy the break, or wait for the pullback? tell me in the comments
s = S(ix(160) - 0.1, A("order") - 0.05)
y4 = s.fig(540, 1.0); s.pop(y4, ix(160), 0.4)
q = s.label(540, 1000, "?", 64, GOLD, 0, 800, 0); s.pop(q, ix(161), 0.35, 0.4, "50% 50%")
for k, (x, text, fill, tc, wi) in enumerate([(270, "BUY THE BREAK", GOLD, "#111", 163), (810, "WAIT FOR PULLBACK", WHITE, "#111", 167)]):
    ln = s.path(f"M 540 1060 L {x} 860", "#ffffff60", 3); s.draw(ln, ix(wi) - 0.3, 0.4)
    pl = s.pill(x, 820, text, fill, tc, 28); s.pop(pl, ix(wi) - 0.1, 0.35, 0.5, "50% 50%"); cue(ix(wi), "pop_" + str(k + 1), -18)
    if k == 0:
        mi = s.path(f"M {x - 80} 700 L {x - 40} 680 L {x - 10} 690 L {x + 20} 650 L {x + 70} 600", GOLD, 4)
        lb = s.path(f"M {x - 90} 640 L {x + 60} 700", "#ffffffa0", 3)
    else:
        mi = s.path(f"M {x - 80} 690 L {x - 30} 620 L {x + 10} 660 L {x + 70} 590", WHITE, 4)
        lb = s.path(f"M {x - 90} 650 L {x + 60} 700", "#ffffffa0", 3)
    s.draw(lb, ix(wi) - 0.1, 0.3); s.draw(mi, ix(wi) + 0.1, 0.5)
bub = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(420, 420, 240, 120, 26)}" fill="#11151b" stroke="#fff" stroke-width="3"/>'
            f'<path d="M 500 538 L 480 580 L 540 538" fill="#11151b" stroke="#fff" stroke-width="3" stroke-linejoin="round"/>'
            + "".join(f'<circle cx="{500 + j * 40}" cy="480" r="9" fill="{GOLD}"/>' for j in range(3)) + "</g>", "bb")
s.pop(bub, ix(171), 0.4, 0.5, "50% 50%"); cue(ix(171), "click-confirm_1", -18)
cm = s.label(540, 1330, "TELL ME IN THE COMMENTS", 32, WHITE, 0, 800, 0.08); s.fade(cm, ix(171), 0.35, y=10)


# 13  order the market (outro with handles; no end card)
s = S(A("order") - 0.05, TOTAL)
es = s.spot(540, 0, "232,194,106", 40, 230); s.fade(es, A("order"), 0.6)
em = s.raw('<image id="@ID@" href="assets/otm_emblem.png" x="390" y="900" width="300" height="291" style="opacity:0;filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>', "i")
s.pop(em, A("order"), 0.7, 0.6, "50% 50%"); cue(A("order"), "bell_A4", -16)
o1 = s.label(540, 1300, "ORDER THE MARKET", 32, GOLD, 0, 800, 0.3); s.fade(o1, A("order") + 0.3, 0.5)
o2 = s.label(540, 1360, "DON'T LET THE MARKET ORDER YOU", 28, WHITE, 0, 700, 0.12); s.fade(o2, A("don't", 1), 0.4)
o3 = s.pill(540, 1470, "FOLLOW FOR MORE", GOLD, "#111", 30); s.pop(o3, A("follow"), 0.4, 0.6, "50% 50%"); cue(A("follow"), "click-confirm_1", -16)
hx = 290
soc = s.raw(f'<g id="@ID@" style="opacity:0">'
            f'<rect x="{hx}" y="1548" width="36" height="36" rx="10" fill="none" stroke="#fff" stroke-width="3"/>'
            f'<circle cx="{hx + 18}" cy="1566" r="8.5" fill="none" stroke="#fff" stroke-width="3"/><circle cx="{hx + 28}" cy="1556" r="2.4" fill="#fff"/>'
            f'<text x="{hx + 48}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@fxzuez_28</text>'
            f'<path d="M {hx + 322} 1546 V 1574 A 9 9 0 1 1 {hx + 313} 1565 M {hx + 322} 1546 Q {hx + 326} 1557 {hx + 338} 1558" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>'
            f'<text x="{hx + 348}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@zuez_28</text></g>', "so")
disc = s.label(540, 1650, "EDUCATIONAL ONLY · NOT FINANCIAL ADVICE", 28, GREY, 0, 600, 0.12)
s.fade(soc, A("don't", 1) + 0.6, 0.5, y=12)
s.fade(disc, A("don't", 1) + 0.9, 0.5)

# ------------------------------------------------------------------ end card, dust, ground, emblem
tl(f'tl.to("#mark", {{opacity: 0, duration: 0.3}}, {A("order") - 0.2:.3f});')
dust = ""
for k in range(40):
    x, y, r, op = rnd.uniform(0, 1080), rnd.uniform(0, 1920), rnd.uniform(1.2, 3.2), rnd.uniform(0.05, 0.22)
    dust += f'<circle id="d{k}" cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#fff" opacity="{op:.2f}"/>'
    tl(f'tl.fromTo("#d{k}", {{x: 0, y: 0}}, {{x: {rnd.uniform(-70, 70):.0f}, y: {-rnd.uniform(150, 480):.0f}, duration: {TOTAL}, ease: "none"}}, 0);')

scenes_svg = "\n".join(f'<g id="{x.id}" style="opacity:0;visibility:hidden" data-layout-allow-overlap>' + "".join(x.items) + "</g>" for x in S.scenes)
CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #000; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #000; font-family: Montserrat, sans-serif; color: #fff; }
#stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
#vig { position: absolute; inset: 0; pointer-events: none; background: radial-gradient(ellipse at 50% 48%, rgba(40,44,52,0.35) 0%, transparent 55%, rgba(0,0,0,0.6) 100%); }
#mark { position: absolute; left: 495px; top: 1560px; width: 90px; opacity: 0.85; filter: drop-shadow(0 0 10px rgba(255,255,255,0.2)); }
"""
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="otm-break" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12" style="opacity:0"/>
{scenes_svg}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-break-audio" class="clip" src="assets/audio/mix_break.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-break"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
