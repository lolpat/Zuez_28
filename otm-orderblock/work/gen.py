"""OTM "The Order Block": a chart explainer in the glowing OTM style (same scene system as otm-break / otm-chance).
An example chart (synthetic, work/chart.py) is built candle by candle as the narration (Quentin) walks through it: a
strong push up, the last down candle before it (the order block), price coming back to the zone, the buy limit at the
middle of the candle's body, the stop under its low, the failure case, and the gap the strongest blocks leave behind.
Candle colours: up #2962ff, down white. Voice only, no music. Writes ../index.html, work/cues.json and work/timing.json."""
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


# ================================================================================================= the chart
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chart import Chart, UP, OB, OB_O, OB_C, OB_H, OB_L, OB_MID, STOP, FILL, GAP_LO, GAP_HI, X1

C = Chart()
LBLUE = "#7d9bff"                               # a lighter tint of the up colour, for the gap box text
CAP_Y = 1352                                    # caption line under the chart
ORD, DONT, FOL = 106, 109, 115                  # outro words: "Order", "Don't", "Follow"
def ix(i): return W(i)

def poly(pts):
    return "M " + " L ".join("%s %s" % C.xy(i, p) for i, p in pts)

def arrowhead(a, b, col, size=22):
    (x0, y0), (x1, y1) = C.xy(*a), C.xy(*b)
    ang = math.atan2(y1 - y0, x1 - x0)
    pts = [(x1, y1), (x1 - size * math.cos(ang - 0.45), y1 - size * math.sin(ang - 0.45)), (x1 - size * math.cos(ang + 0.45), y1 - size * math.sin(ang + 0.45))]
    return " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)

def candles_clip(s, i1=None, op=1.0):
    """all candles in one group behind a clip rect; returns the clip rect id (tween its width to reveal)"""
    cid, rid = s.uid("cp"), s.uid("cr")
    s.items.append(f'<defs><clipPath id="{cid}"><rect id="{rid}" x="0" y="0" width="0" height="1920"/></clipPath></defs>')
    s.raw(f'<g id="@ID@" clip-path="url(#{cid})" style="opacity:{op}">' + "".join(C.candles(0, i1)) + "</g>", "cg")
    return rid

def edge(i): return round(C.x(i) + C.sp * 0.6, 1)

def reveal(rid, keys, t_open):
    """keys: [(t, idx), ...] in time order; the clip edge sits just past candle idx at time t"""
    tl(f'tl.set("#{rid}", {{attr: {{width: {edge(keys[0][1])}}}}}, {t_open:.3f});')
    for (t0, i0), (t1, i1) in zip(keys, keys[1:]):
        if i1 != i0:
            tl(f'tl.fromTo("#{rid}", {{attr: {{width: {edge(i0)}}}}}, {{attr: {{width: {edge(i1)}}}, duration: {max(0.05, t1 - t0):.3f}, ease: "none", immediateRender: false}}, {t0:.3f});')

def captions(s, items, end):
    """items: [(t, text, col)]; each holds until the next one"""
    for k, (t, text, col) in enumerate(items):
        t_end = items[k + 1][0] if k + 1 < len(items) else end
        i = s.label(540, CAP_Y, text, 32, col, 0, 800, 0.06)
        s.fade(i, t, 0.3, y=10)
        tl(f'tl.to("#{i}", {{opacity: 0, duration: 0.15}}, {t_end - 0.18:.3f});')

def out(i, t, d=0.3, to=0):
    tl(f'tl.to("#{i}", {{opacity: {to}, duration: {d}}}, {t:.3f});')

def zone(s, op=0, wid=True):
    """the order block zone: from the block candle's left edge to the right edge, high to low"""
    x0 = C.x(OB) - C.bw / 2 - 4
    y0, y1 = C.y(OB_H), C.y(OB_L)
    return s.raw(f'<rect id="@ID@" x="{x0:.1f}" y="{y0:.1f}" width="{(X1 + 30 - x0) if wid else 0:.1f}" height="{y1 - y0:.1f}" '
                 f'fill="{GOLD}" fill-opacity="0.13" stroke="{GOLD}" stroke-opacity="0.85" stroke-width="2.5" style="opacity:{op}"/>', "z"), X1 + 30 - x0

def ob_ring(s, op=0):
    x, pad = C.x(OB), 10
    y0, y1 = C.y(OB_H) - pad, C.y(OB_L) + pad
    return s.raw(f'<rect id="@ID@" x="{x - C.bw / 2 - pad:.1f}" y="{y0:.1f}" width="{C.bw + 2 * pad:.1f}" height="{y1 - y0:.1f}" rx="8" fill="none" '
                 f'stroke="{GOLD}" stroke-width="4" style="opacity:{op};filter:drop-shadow(0 0 10px {GOLD})"/>', "rg")

# 1  big money leaves footprints; this is one of them: the order block   (frame 0 is the thumbnail)
s = S(0, ix(12) - 0.15, ground=False, first=True, restore=False, hide=False)
s.label(540, 360, "THE ORDER", 64, WHITE, 1, 800, 0.06)
s.label(540, 440, "BLOCK", 64, GOLD, 1, 800, 0.12)
s.raw('<g id="@ID@" style="opacity:0.8">' + "".join(C.candles()) + "</g>", "cg")
z1, _ = zone(s, 1)
r1 = ob_ring(s, 1)
tl(f'tl.fromTo("#{r1}", {{opacity: 1}}, {{opacity: 0.35, duration: 0.6, yoyo: true, repeat: 5, ease: "sine.inOut"}}, 0.3);')
p1 = s.pill(C.x(OB) + 10, C.y(OB_L) + 70, "ORDER BLOCK", GOLD, "#111", 28, 1)
captions(s, [(0.05, "BIG MONEY LEAVES FOOTPRINTS", WHITE), (ix(4) - 0.1, "THIS IS ONE OF THEM", GOLD)], ix(12) - 0.15)
cue(ix(9), "bell_C5", -20)

# 2  the example chart, built as the voice walks through it
open2, close2 = ix(12) - 0.15, ix(ORD) - 0.05
s = S(open2, close2, ground=False, restore=False, hide=False)
s.label(540, 500, "ORDER BLOCK  ·  EXAMPLE CHART", 28, GREY, 1, 700, 0.22)
# zone, limit and stop sit behind the candles
zb, zw = zone(s, 1, wid=False)
lim = s.path(f"M {C.x(OB) - C.bw / 2 - 4:.1f} {C.y(OB_MID):.1f} H {X1 + 30}", GOLD, 3, drawn=True, style="stroke-dasharray:14 10;opacity:0")
stp = s.path(f"M {C.x(OB) - C.bw / 2 - 4:.1f} {C.y(STOP):.1f} H {X1 + 30}", RED, 3, drawn=True, style="stroke-dasharray:14 10;opacity:0")
rid = candles_clip(s)
gx0 = C.x(OB) + C.bw / 2 + 2                   # the gap box sits over the candles (it lies inside candle 20's body)
gap = s.raw(f'<rect id="@ID@" x="{gx0:.1f}" y="{C.y(GAP_HI):.1f}" width="{C.x(22.5) - gx0:.1f}" height="{C.y(GAP_LO) - C.y(GAP_HI):.1f}" '
            f'fill="{LBLUE}" fill-opacity="0.35" stroke="#ffffff" stroke-width="2.5" stroke-dasharray="7 5" style="opacity:0"/>', "gp")
keys = [(open2, OB), (ix(14), OB), (ix(16) + 0.35, 23),            # the push
        (ix(38), 23), (ix(43) + 0.3, 35), (ix(45), 35), (ix(46) + 0.1, FILL),   # the drift and the pullback into the zone
        (ix(46) + 0.2, FILL), (ix(47) + 0.2, 37),                   # the bounce: buyers defend it
        (ix(91), 37), (ix(95), 47)]                                 # the rally
reveal(rid, keys, open2)
cue(ix(14), "whoosh-short_1", -22)
# the push
pa = s.path(poly([(19.2, 47), (22.4, 72)]), GOLD, 5); s.draw(pa, ix(15), 0.5)
pah = s.raw(f'<polygon id="@ID@" points="{arrowhead((19.2, 47), (22.4, 72), GOLD)}" fill="{GOLD}" style="opacity:0"/>', "ah"); s.pop(pah, ix(15) + 0.45, 0.2, 0.5, "50% 50%")
pl = s.label(C.x(21), C.y(79), "STRONG PUSH", 28, GOLD, 0, 800, 0.1); s.fade(pl, ix(15), 0.35); cue(ix(15), "swell_1", -22)
for i in (pa, pah): out(i, ix(17) - 0.1, 0.3, 0.25)
out(pl, ix(17) - 0.1)
# look right before it: the last down candle
hl = s.raw(f'<rect id="@ID@" x="{C.x(OB) - C.sp / 2:.1f}" y="{C.y(100):.1f}" width="{C.sp:.1f}" height="{C.y(0) - C.y(100):.1f}" fill="#ffffff" fill-opacity="0.07" style="opacity:0"/>', "hl")
s.fade(hl, ix(18), 0.4); out(hl, ix(26), 0.4)
la = s.path(f"M {C.x(OB) + 120:.1f} {C.y(18):.1f} Q {C.x(OB) + 60:.1f} {C.y(14):.1f} {C.x(OB) + 14:.1f} {C.y(OB_L) + 22:.1f}", WHITE, 4); s.draw(la, ix(19), 0.45)
lah = s.raw(f'<polygon id="@ID@" points="{C.x(OB) + 6:.1f},{C.y(OB_L) + 12:.1f} {C.x(OB) + 30:.1f},{C.y(OB_L) + 26:.1f} {C.x(OB) + 14:.1f},{C.y(OB_L) + 42:.1f}" fill="#fff" style="opacity:0"/>', "ah")
s.pop(lah, ix(19) + 0.4, 0.2, 0.5, "50% 50%"); cue(ix(19), "tick-crisp_1", -20)
r2 = ob_ring(s); s.pop(r2, ix(23), 0.35, 0.6, "50% 50%"); cue(ix(23), "pop_1", -18)
ld = s.pill(C.x(OB) + 150, C.y(14), "LAST DOWN CANDLE", WHITE, "#111", 26); s.pop(ld, ix(24), 0.35, 0.5, "50% 50%")
for i in (la, lah, ld): out(i, ix(26) - 0.05)
# that's the order block: the zone opens to the right
tl(f'tl.fromTo("#{zb}", {{attr: {{width: 0}}}}, {{attr: {{width: {zw:.1f}}}, duration: 0.7, ease: "power2.out", immediateRender: false}}, {ix(27):.3f});')
cue(ix(27), "whoosh-short_2", -22)
zl = s.label(X1 + 20, C.y(OB_L) - 14, "ORDER BLOCK", 26, GOLD, 0, 800, 0.12, "end"); s.fade(zl, ix(28), 0.35)
out(r2, ix(30) - 0.1, 0.4)
# big buyers placed their orders there
chips = []
for k, i in enumerate((23.8, 30, 36.2)):
    ch = s.pill(C.x(i), C.y(32.5), "BUY", UP, WHITE, 22)
    s.pop(ch, ix(32) + 0.18 * k, 0.3, 0.5, "50% 50%"); cue(ix(32) + 0.18 * k, f"tick_{k + 1}", -22); chips.append(ch)
for ch in chips: out(ch, ix(37) - 0.1)
# price comes back to the zone; buyers defend it
tl(f'tl.to("#{zb}", {{attr: {{"fill-opacity": 0.28}}, duration: 0.35, yoyo: true, repeat: 1}}, {ix(42):.3f});')
cue(ix(42), "tock_1", -20)
da = s.path(poly([(37, 26.5), (38.6, 44)]), GOLD, 5); s.draw(da, ix(46), 0.4)
dah = s.raw(f'<polygon id="@ID@" points="{arrowhead((37, 26.5), (38.6, 44), GOLD)}" fill="{GOLD}" style="opacity:0"/>', "ah"); s.pop(dah, ix(46) + 0.35, 0.2, 0.5, "50% 50%")
dl = s.label(C.x(38) + 26, C.y(47), "DEFENDED", 26, GOLD, 0, 800, 0.12, "start"); s.fade(dl, ix(46) + 0.2, 0.35); cue(ix(46) + 0.2, "land-light_1", -18)
for i in (da, dah, dl): out(i, ix(48) - 0.1)
# don't chase the move
cx_, cy_ = C.xy(23, 72)
xm = xmark(s, cx_, cy_ - 10, 22); s.draw(xm, ix(49), 0.3); cue(ix(49), "click_2", -18)
ce = s.pill(cx_ - 120, cy_ - 30, "CHASING", RED, WHITE, 24); s.pop(ce, ix(50), 0.35, 0.5, "50% 50%")
for i in (xm, ce): out(i, ix(58) - 0.1)
# let price come to you
lp = s.path(poly([(24, 72), (31, 60), (FILL, 38)]), WHITE, 3, style="stroke-dasharray:1 1.2;stroke-dashoffset:1.1")
s.draw(lp, ix(54), 0.9)
lph = s.raw(f'<polygon id="@ID@" points="{arrowhead((31, 60), (FILL, 38), WHITE, 20)}" fill="#fff" style="opacity:0"/>', "ah"); s.pop(lph, ix(55) + 0.4, 0.2, 0.5, "50% 50%")
cue(ix(54), "whoosh-short_3", -24)
for i in (lp, lph): out(i, ix(58) - 0.1)
# the buy limit at the middle of the body
s.fade(lim, ix(61), 0.4); cue(ix(61), "pop_2", -20)
mx, my = C.xy(OB, OB_MID)
md = s.raw(f'<g id="@ID@" style="opacity:0"><line x1="{mx - 26}" y1="{my}" x2="{mx + 26}" y2="{my}" stroke="{GOLD}" stroke-width="5"/>'
           f'<circle cx="{mx}" cy="{my}" r="7" fill="{GOLD}"/></g>', "md")
s.pop(md, ix(64), 0.3, 0.4, "50% 50%"); cue(ix(64), "bell_E5", -22)
mt = s.label(mx - 40, my + 10, "50%", 26, GOLD, 0, 800, 0.04, "end"); s.fade(mt, ix(64), 0.3)
ll = s.label(X1 + 20, C.y(OB_MID) - 14, "BUY LIMIT", 26, GOLD, 0, 800, 0.12, "end"); s.fade(ll, ix(61) + 0.1, 0.35)
out(zl, ix(61), 0.3)
fx, fy = C.xy(FILL, OB_MID)
fr = s.raw(f'<circle id="@ID@" cx="{fx}" cy="{fy}" r="20" fill="none" stroke="{GOLD}" stroke-width="4" style="opacity:0;filter:drop-shadow(0 0 10px {GOLD})"/>', "c")
s.pop(fr, ix(67), 0.35, 0.3, "50% 50%"); cue(ix(67), "click-confirm_1", -18)
fl = s.pill(fx + 6, fy - 210, "FILLED", GOLD, "#111", 24); s.pop(fl, ix(67) + 0.1, 0.35, 0.5, "50% 50%")
for i in (fl,): out(i, ix(69) + 0.4)
# the stop under the low
s.fade(stp, ix(70), 0.4); cue(ix(70), "tock_1", -18)
sl = s.label(X1 + 20, C.y(STOP) + 34, "STOP", 26, RED, 0, 800, 0.12, "end"); s.fade(sl, ix(70) + 0.1, 0.35)
sx = s.raw(f'<g id="@ID@" style="opacity:0"><line x1="{C.x(OB) - 26}" y1="{C.y(OB_L)}" x2="{C.x(OB) + 26}" y2="{C.y(OB_L)}" stroke="{RED}" stroke-width="4"/></g>', "sx")
s.pop(sx, ix(72), 0.3, 0.4, "50% 50%")
slw = s.label(C.x(OB) - 40, C.y(OB_L) + 10, "LOW", 24, RED, 0, 800, 0.08, "end"); s.fade(slw, ix(72), 0.3)
for i in (md, mt, sx, slw): out(i, ix(84))
# the failure: a close below it, the idea is wrong (a ghost candle)
gx = C.x(40)
gh = s.raw(f'<g id="@ID@" style="opacity:0"><line x1="{gx}" y1="{C.y(38)}" x2="{gx}" y2="{C.y(22)}" stroke="{RED}" stroke-width="2" stroke-dasharray="5 4"/>'
           f'<rect x="{gx - C.bw / 2:.1f}" y="{C.y(36.5):.1f}" width="{C.bw:.1f}" height="{C.y(23.5) - C.y(36.5):.1f}" fill="{RED}" fill-opacity="0.25" stroke="{RED}" stroke-width="2.5" stroke-dasharray="6 4"/></g>', "gh")
s.pop(gh, ix(77), 0.35, 0.4, "50% 100%"); cue(ix(77), "whoosh-short_1", -22)
xw = xmark(s, gx, C.y(16), 16); s.draw(xw, ix(83) - 0.1, 0.3); cue(ix(83), "click_1", -18)
wr = s.pill(gx + 90, C.y(9), "IDEA WRONG", RED, WHITE, 24); s.pop(wr, ix(81), 0.35, 0.5, "50% 50%")
for i in (gh, xw, wr): out(i, ix(91) - 0.1)
# the rally, then the gap the strongest blocks leave
for i in (lim, ll, stp, sl, fr): out(i, ix(91), 0.4, 0.3)
cue(ix(91), "swell_2", -20)
s.fade(gap, ix(96), 0.4); cue(ix(97), "bell_G5", -20)
gl = s.pill(C.x(22.5) + 56, C.y((GAP_LO + GAP_HI) / 2), "GAP", UP, WHITE, 24); s.pop(gl, ix(97), 0.35, 0.5, "50% 50%")
tl(f'tl.to("#{gap}", {{attr: {{"fill-opacity": 0.6}}, duration: 0.4, yoyo: true, repeat: 3}}, {ix(101):.3f});')
ur = s.pill(C.x(21), C.y(80), "REAL URGENCY", UP, WHITE, 24); s.pop(ur, ix(104), 0.35, 0.5, "50% 50%"); cue(ix(104), "pop_3", -20)
captions(s, [(open2 + 0.1, "FIND A STRONG PUSH UP", WHITE), (ix(17) - 0.1, "LOOK RIGHT BEFORE IT", WHITE),
             (ix(22) - 0.1, "THE LAST DOWN CANDLE", WHITE), (ix(26) - 0.1, "THAT'S THE ORDER BLOCK", GOLD),
             (ix(30) - 0.1, "BIG BUYERS PLACED ORDERS HERE", WHITE), (ix(37) - 0.1, "PRICE COMES BACK TO THE ZONE", WHITE),
             (ix(44) - 0.1, "BUYERS OFTEN DEFEND IT", GOLD), (ix(48) - 0.1, "DON'T CHASE THE MOVE", RED),
             (ix(53) - 0.1, "LET PRICE COME TO YOU", WHITE), (ix(58) - 0.1, "BUY LIMIT: MIDDLE OF THE BODY", GOLD),
             (ix(69) - 0.1, "STOP: UNDER ITS LOW", RED), (ix(75) - 0.1, "CLOSE BELOW IT = IDEA WRONG", RED),
             (ix(84) - 0.1, "SMALL LOSS. MOVE ON.", WHITE), (ix(91) - 0.1, "THE STRONGEST BLOCKS LEAVE A GAP", GOLD),
             (ix(101) - 0.1, "THE GAP SHOWS REAL URGENCY", GOLD)], close2)

# 3  order the market (outro with handles; no end card)
s = S(ix(ORD) - 0.05, TOTAL)
es = s.spot(540, 0, "232,194,106", 40, 230); s.fade(es, ix(ORD), 0.6)
em = s.raw('<image id="@ID@" href="assets/otm_emblem.png" x="390" y="900" width="300" height="291" style="opacity:0;filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>', "i")
s.pop(em, ix(ORD), 0.7, 0.6, "50% 50%"); cue(ix(ORD), "bell_A4", -16)
o1 = s.label(540, 1300, "ORDER THE MARKET", 32, GOLD, 0, 800, 0.3); s.fade(o1, ix(ORD) + 0.3, 0.5)
o2 = s.label(540, 1360, "DON'T LET THE MARKET ORDER YOU", 28, WHITE, 0, 700, 0.12); s.fade(o2, ix(DONT), 0.4)
o3 = s.pill(540, 1470, "FOLLOW FOR MORE", GOLD, "#111", 30); s.pop(o3, ix(FOL), 0.4, 0.6, "50% 50%"); cue(ix(FOL), "click-confirm_1", -16)
hx = 290
soc = s.raw(f'<g id="@ID@" style="opacity:0">'
            f'<rect x="{hx}" y="1548" width="36" height="36" rx="10" fill="none" stroke="#fff" stroke-width="3"/>'
            f'<circle cx="{hx + 18}" cy="1566" r="8.5" fill="none" stroke="#fff" stroke-width="3"/><circle cx="{hx + 28}" cy="1556" r="2.4" fill="#fff"/>'
            f'<text x="{hx + 48}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@fxzuez_28</text>'
            f'<path d="M {hx + 322} 1546 V 1574 A 9 9 0 1 1 {hx + 313} 1565 M {hx + 322} 1546 Q {hx + 326} 1557 {hx + 338} 1558" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>'
            f'<text x="{hx + 348}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@zuez_28</text></g>', "so")
disc = s.label(540, 1650, "EDUCATIONAL ONLY · NOT FINANCIAL ADVICE", 28, GREY, 0, 600, 0.12)
s.fade(soc, ix(DONT) + 0.6, 0.5, y=12)
s.fade(disc, ix(DONT) + 0.9, 0.5)
# ------------------------------------------------------------------ end card, dust, ground, emblem
tl(f'tl.to("#mark", {{opacity: 0, duration: 0.3}}, {ix(ORD) - 0.2:.3f});')
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
    <div id="root" data-composition-id="otm-orderblock" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12" style="opacity:0"/>
{scenes_svg}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-orderblock-audio" class="clip" src="assets/audio/mix_orderblock.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-orderblock"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
