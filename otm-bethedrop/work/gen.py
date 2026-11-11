"""OTM "Be the Drop": a motivational glowing-figure video in the OTM style, the companion to otm-dropstone (same
water-and-stone idea, told as general motivation in original words). Not the strongest, the one still there; hammer
starts fade by Friday; small daily things (a page, a workout, an honest hour); day 1, day 30, day 200 the stone cracks
open and shows the person you're becoming; water carves stone with repetition, not force; stop waiting for one big
breakthrough; be the drop and show up again tomorrow. Voice only (Quentin), no music.
Scenes key off word indices of work/words.json (helper ix)."""
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

    def spot(self, x, op=1.0, col="255,255,255", top=36, bot=150, gy=GY, y0=380):
        gid = self.uid("gr")
        return self.add(f'<g id="@ID@" style="opacity:{op}"><defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
                        f'<stop offset="0" stop-color="rgb({col})" stop-opacity="0.26"/><stop offset="1" stop-color="rgb({col})" stop-opacity="0.04"/></linearGradient></defs>'
                        f'<path d="M {x - top} {y0} L {x + top} {y0} L {x + bot} {gy} L {x - bot} {gy} Z" fill="url(#{gid})"/>'
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

def ix(i):
    return W(i)

# ---------------------------------------------------------------- shared drawing: the cave, the stone, the drops
CEIL_Y, TIP_Y, STONE_TOP = 560, 610, 772
LEFT_HALF = "M 250 1240 C 220 1060 270 800 520 772 L 545 830 L 520 900 L 560 980 L 525 1060 L 555 1150 L 530 1240 Z"
RIGHT_HALF = "M 530 1240 L 555 1150 L 525 1060 L 560 980 L 520 900 L 545 830 L 520 772 C 760 760 860 980 830 1240 Z"
CRACK_A = "M 520 772 L 545 830 L 520 900"
CRACK_B = "M 520 900 L 560 980 L 525 1060 L 555 1150 L 530 1240"

def ceiling(s):
    pts = " ".join(f"L {x} {CEIL_Y + (8 if (x // 60) % 2 else -6)}" for x in range(80, 1020, 60))
    return s.raw(f'<path id="@ID@" d="M 40 {CEIL_Y} {pts} L 500 {CEIL_Y} L 540 {TIP_Y} L 580 {CEIL_Y} L 1040 {CEIL_Y}" fill="none" stroke="#c9ced6" stroke-width="4" stroke-linejoin="round"/>', "cl")

def stone(s, behind=""):
    """the stone: one glowing outline until it splits, over two fill-only halves that can move apart.
    returns (left_half, right_half, crackA, crackB, outline, left_edge, right_edge)"""
    if behind:
        s.raw(behind, "bh")
    lh = s.raw(f'<g id="@ID@"><path d="{LEFT_HALF}" fill="#06080b"/></g>', "lh")
    rh = s.raw(f'<g id="@ID@"><path d="{RIGHT_HALF}" fill="#06080b"/></g>', "rh")
    ol = s.raw(f'<path id="@ID@" d="M 250 1240 C 220 1060 270 800 520 772 C 760 760 860 980 830 1240" fill="none" stroke="#e9ecf1" stroke-width="5" '
               f'style="filter:drop-shadow(0 0 14px rgba(255,255,255,0.25))"/>', "ol")
    le = s.raw(f'<path id="@ID@" d="{LEFT_HALF}" fill="none" stroke="#e9ecf1" stroke-width="5" stroke-linejoin="round" style="opacity:0"/>', "le")
    re_ = s.raw(f'<path id="@ID@" d="{RIGHT_HALF}" fill="none" stroke="#e9ecf1" stroke-width="5" stroke-linejoin="round" style="opacity:0"/>', "re")
    ca = s.path(CRACK_A, "#e9ecf1", 4)
    cb = s.path(CRACK_B, "#e9ecf1", 4)
    return lh, rh, ca, cb, ol, le, re_

def drops(s, t0, t1, every=0.7, col=GOLD, x=540, y0=TIP_Y + 8, y1=STONE_TOP - 8):
    """drops falling from the tip onto the stone from t0 to t1; returns the times they land"""
    lands = []
    t = t0
    while t < t1:
        d = s.raw(f'<path id="@ID@" d="M {x} {y0 - 14} C {x + 9} {y0} {x + 9} {y0 + 10} {x} {y0 + 12} C {x - 9} {y0 + 10} {x - 9} {y0} {x} {y0 - 14} Z" fill="{col}" style="opacity:0;filter:drop-shadow(0 0 8px {col})"/>', "dp")
        tl(f'tl.fromTo("#{d}", {{opacity: 1, y: 0}}, {{opacity: 1, y: {y1 - y0}, duration: 0.42, ease: "power2.in", immediateRender: false}}, {t:.3f});')
        tl(f'tl.set("#{d}", {{opacity: 0}}, {t + 0.42:.3f});')
        sp = s.raw(f'<path id="@ID@" d="M {x - 22} {y1 + 4} Q {x - 14} {y1 - 14} {x - 6} {y1} M {x + 22} {y1 + 4} Q {x + 14} {y1 - 14} {x + 6} {y1}" fill="none" stroke="{col}" stroke-width="3" style="opacity:0"/>', "sp")
        tl(f'tl.fromTo("#{sp}", {{opacity: 1, scale: 0.6, transformOrigin: "50% 100%"}}, {{opacity: 0, scale: 1.3, duration: 0.35, ease: "power2.out", immediateRender: false}}, {t + 0.42:.3f});')
        lands.append(t + 0.42)
        t += every
    return lands

def toplab(s, small, big, t0, t1, bcol=WHITE, scol=LBL, bsize=58):
    ids = []
    if small:
        a = s.label(540, 380, small, 28, scol, 0, 700, 0.18); ids.append(a)
    b = s.label(540, 455, big, bsize, bcol, 0, 800, 0.04); ids.append(b)
    for i in ids:
        s.fade(i, t0, 0.3, y=10)
        tl(f'tl.to("#{i}", {{opacity: 0, duration: 0.15}}, {t1 - 0.17:.3f});')
    return ids

def hammer(s, x, y, flip=False):
    """a hammer held toward the stone; returns its id (swing it with rotation)"""
    sx = -1 if flip else 1
    return s.raw(f'<g id="@ID@"><line x1="{x}" y1="{y}" x2="{x + sx * 90}" y2="{y - 40}" stroke="#c9ced6" stroke-width="7" stroke-linecap="round"/>'
                 f'<rect x="{x + sx * 90 - 18}" y="{y - 70}" width="36" height="56" rx="6" fill="#c9ced6" transform="rotate({-24 * sx} {x + sx * 90} {y - 40})"/></g>', "hm")


def tile(s, x, y, w, h, inner, stroke="#ffffff60", op=0, fill="#0f1319"):
    return s.raw(f'<g id="@ID@" style="opacity:{op}"><path d="{rrect(x - w / 2, y - h / 2, w, h, 16)}" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>{inner}</g>', "tl")

# 1  "You don't need to be the strongest person in the room, you need to be the one who's still there."
s = S(0, ix(20) - 0.1, first=True)
for i_ in (s.label(540, 380, "YOU DON'T NEED TO BE", 28, LBL, 1, 700, 0.18), s.label(540, 455, "THE STRONGEST", 64, WHITE, 1, 800, 0.04)):
    tl(f'tl.to("#{i_}", {{opacity: 0, duration: 0.15}}, {ix(11) - 0.27:.3f});')
toplab(s, "YOU NEED TO BE", "THE ONE STILL THERE", ix(11), ix(20) - 0.1, GOLD, LBL, 56)
room = []
for k, (x, sc) in enumerate([(150, 0.75), (300, 0.75), (540, 1.25), (780, 0.75), (930, 0.75)]):
    f = s.fig(x, sc, "#9aa0a8" if k != 3 else WHITE, 1, k == 3)
    room.append(f)
sg = s.label(540, 980, "STRONGEST", 28, LBL, 0, 800, 0.2); s.fade(sg, ix(6) - 0.1, 0.3)
for k, f in enumerate(room):
    if k != 3:
        tl(f'tl.to("#{f}", {{opacity: 0, x: {-60 if k < 3 else 60}, duration: 0.6, ease: "power2.in"}}, {ix(16) + k * 0.12:.3f});')
tl(f'tl.to("#{sg}", {{opacity: 0, duration: 0.3}}, {ix(16):.3f});')
gs = s.fig(780, 0.75, GOLD, 0); s.fade(gs, ix(18) - 0.1, 0.5)
sp1 = s.spot(780, 0, "232,194,106", 30, 110); s.fade(sp1, ix(18) - 0.1, 0.5)
cue(ix(18) - 0.1, "swell_1", -18)

# 2  "Most people attack their goals like a hammer, a huge start, a burst of energy, then nothing. Big plans on Monday, gone by Friday."
s = S(ix(20) - 0.1, ix(44) - 0.1, ground=False, restore=False)
toplab(s, "MOST PEOPLE ATTACK THEIR GOALS", "LIKE A HAMMER", ix(20), ix(28) - 0.1, WHITE, LBL)
toplab(s, "", "A HUGE START", ix(28), ix(31) - 0.1, GOLD)
toplab(s, "", "A BURST OF ENERGY", ix(31), ix(35) - 0.1, GOLD)
toplab(s, "", "THEN NOTHING", ix(35), ix(37) - 0.1, "#9aa0a8")
toplab(s, "BIG PLANS ON MONDAY", "GONE BY FRIDAY", ix(37), ix(44) - 0.1, RED, LBL)
s.path("M 120 1060 H 960", "#ffffff40", 3, drawn=True)
hm = s.raw(f'<g id="@ID@" style="opacity:0"><line x1="420" y1="760" x2="540" y2="640" stroke="#c9ced6" stroke-width="12" stroke-linecap="round"/>'
           f'<rect x="500" y="580" width="90" height="120" rx="12" fill="#c9ced6" transform="rotate(45 545 640)"/></g>', "hm")
s.pop(hm, ix(25) - 0.1, 0.35, 0.5, "50% 50%")
tl(f'tl.fromTo("#{hm}", {{rotation: 0, svgOrigin: "420 760"}}, {{rotation: 40, svgOrigin: "420 760", duration: 0.18, yoyo: true, repeat: 3, ease: "power2.in", immediateRender: false}}, {ix(27):.3f});')
tl(f'tl.to("#{hm}", {{opacity: 0, duration: 0.3}}, {ix(29) - 0.2:.3f});')
cue(ix(27), "tock_1", -18)
en = s.path("M 160 1060 L 300 1050 L 360 760 L 420 700 L 480 860 L 560 1000 L 700 1052 L 920 1056", GOLD, 6, style="filter:drop-shadow(0 0 10px rgba(232,194,106,0.7))")
s.draw(en, ix(29) - 0.1, 2.6)
cue(ix(29), "swell_2", -20)
for k, d in enumerate(["MON", "TUE", "WED", "THU", "FRI"]):
    x = 200 + k * 170
    dl = s.label(x, 1130, d, 30, GOLD if k == 0 else LBL, 0, 800, 0.1); s.fade(dl, ix(38) + k * 0.12, 0.25)
x5 = s.path("M 856 1094 L 904 1142 M 904 1094 L 856 1142", RED, 6); s.draw(x5, ix(42) - 0.1, 0.3); cue(ix(42) - 0.1, "tock_1", -18)

# 3  "But the things that really change your life are small. One page a day, one workout, one honest hour of work."
s = S(ix(44) - 0.1, ix(65) - 0.1, ground=False, hide=False)
toplab(s, "THE THINGS THAT CHANGE YOUR LIFE", "ARE SMALL", ix(44), ix(65) - 0.1, GOLD, LBL)
items = [(220, ix(55) - 0.1, f'<rect x="170" y="720" width="100" height="130" rx="6" fill="#f3ead8"/>' + "".join(f'<line x1="186" y1="{748 + j * 22}" x2="254" y2="{748 + j * 22}" stroke="#b9ad93" stroke-width="3"/>' for j in range(4)), "ONE PAGE A DAY"),
         (540, ix(59) - 0.1, f'<rect x="460" y="770" width="160" height="16" rx="6" fill="{GOLD}"/><rect x="450" y="745" width="26" height="66" rx="6" fill="{GOLD}"/><rect x="604" y="745" width="26" height="66" rx="6" fill="{GOLD}"/>', "ONE WORKOUT"),
         (860, ix(61) - 0.1, f'<circle cx="860" cy="785" r="62" fill="none" stroke="{GOLD}" stroke-width="5"/><path d="M 860 745 V 785 L 890 805" fill="none" stroke="{GOLD}" stroke-width="5" stroke-linecap="round"/>', "ONE HONEST HOUR")]
for k, (x, t, ic, lab) in enumerate(items):
    tt = tile(s, x, 820, 270, 300, ic + f'<text x="{x}" y="930" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" fill="#fff">{lab}</text>', GOLD, 0)
    s.pop(tt, t, 0.4, 0.5, "50% 50%"); cue(t, "pop_" + str(k + 1), -18)
sm = s.label(540, 1150, "SMALL. DAILY. REAL.", 40, WHITE, 0, 800, 0.1); s.fade(sm, ix(63), 0.4, y=10)

# 4  "It doesn't look like much. Day one, nothing happens. Day 30, nothing you can see. But somewhere around day 200, something cracks open."
o4, c4 = ix(65) - 0.1, ix(88) - 0.1
s = S(o4, c4)
ceiling(s)
behind = (f'<g><circle cx="540" cy="1000" r="230" fill="url(#gglow)"/>'
          f'<g transform="translate(540,1240) scale(1.25)"><g style="filter:drop-shadow(0 0 18px rgba(232,194,106,0.9))"><circle cx="0" cy="-158" r="31" fill="{GOLD}"/>'
          f'<path d="M -48 0 L -48 -66 Q -48 -116 0 -116 Q 48 -116 48 -66 L 48 0 Z" fill="{GOLD}"/></g></g></g>')
s.items.append(f'<defs><radialGradient id="gglow"><stop offset="0" stop-color="{GOLD}" stop-opacity="0.45"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
lh, rh, ca, cb, ol, le, re_ = stone(s, behind)
toplab(s, "", "IT DOESN'T LOOK LIKE MUCH", o4 + 0.1, ix(70) - 0.1, WHITE, LBL, 48)
toplab(s, "NOTHING HAPPENS", "DAY 1", ix(70), ix(74) - 0.1, GOLD, "#9aa0a8", 72)
toplab(s, "NOTHING YOU CAN SEE", "DAY 30", ix(74), ix(80) - 0.1, GOLD, "#9aa0a8", 72)
toplab(s, "SOMETHING CRACKS OPEN", "DAY 200", ix(80), c4, GOLD, GOLD, 72)
lands = drops(s, o4 + 0.2, ix(86), 0.7)
for k, t in enumerate(lands):
    if k % 3 == 0:
        cue(t, "tick_" + str(k % 3 + 1), -28)
y4 = s.fig(140, 0.8, WHITE); s.pop(y4, o4 + 0.1, 0.4)
s.draw(ca, ix(76), 0.8); cue(ix(76), "tick-crisp_2", -18)
s.draw(cb, ix(85) - 0.4, 0.5)
tl(f'tl.set("#{ol}", {{opacity: 0}}, {ix(86):.3f});')
for half, edge, dx, rot, org in ((lh, le, -170, -7, "250 1240"), (rh, re_, 170, 7, "830 1240")):
    tl(f'tl.set("#{edge}", {{opacity: 1}}, {ix(86):.3f});')
    for el in (half, edge):
        tl(f'tl.to("#{el}", {{x: {dx}, rotation: {rot}, svgOrigin: "{org}", duration: 1.0, ease: "power3.inOut"}}, {ix(86):.3f});')
for c_ in (ca, cb):
    tl(f'tl.to("#{c_}", {{opacity: 0, duration: 0.2}}, {ix(86):.3f});')
cue(ix(86), "land_1", -14); cue(ix(86) + 0.3, "swell_2", -16)

# 5  "That's how water carves stone. Not with force, with repetition."
s = S(ix(88) - 0.1, ix(98) - 0.1)
s.path("M 160 1240 C 200 1020 340 900 540 890 C 740 900 880 1020 920 1240", "#e9ecf1", 5, drawn=True, style="filter:drop-shadow(0 0 14px rgba(255,255,255,0.25))")
s.path("M 120 600 L 500 600 L 540 660 L 580 600 L 960 600", "#c9ced6", 4, drawn=True)
hole = s.raw(f'<ellipse id="@ID@" cx="540" cy="900" rx="34" ry="12" fill="#000" stroke="{GOLD}" stroke-width="3" style="opacity:0"/>', "ho")
s.fade(hole, ix(91), 0.8)
drops(s, ix(88), ix(98) - 0.5, 0.55, GOLD, 540, 668, 880)
toplab(s, "THAT'S HOW", "WATER CARVES STONE", ix(88), ix(93) - 0.1, WHITE, LBL)
toplab(s, "", "NOT WITH FORCE", ix(93), ix(96) - 0.1, "#9aa0a8")
toplab(s, "", "WITH REPETITION", ix(96), ix(98) - 0.1, GOLD)
cue(ix(96), "bell_C5", -18)

# 6  "So stop waiting for one big breakthrough."
s = S(ix(98) - 0.1, ix(105) - 0.1)
toplab(s, "STOP WAITING FOR", "ONE BIG BREAKTHROUGH", ix(98), ix(105) - 0.1, WHITE, LBL, 52)
bolt = s.raw(f'<g id="@ID@" style="opacity:0"><path d="M 600 640 L 470 860 L 545 860 L 500 1040 L 650 800 L 570 800 L 620 640 Z" fill="#3a3f48" stroke="#9aa0a8" stroke-width="4" stroke-linejoin="round"/></g>', "bo")
s.pop(bolt, ix(102), 0.4, 0.5, "50% 50%")
xb = s.path("M 440 700 L 680 980 M 680 700 L 440 980", RED, 8); s.draw(xb, ix(104) - 0.15, 0.35); cue(ix(104) - 0.15, "tock_1", -16)
w6 = s.fig(300, 0.8, "#9aa0a8", 1, False); s.pop(w6, ix(98), 0.4)

# 7  "Be the drop and show up again tomorrow."
s = S(ix(105) - 0.1, ix(113) - 0.05)
bd = s.raw(f'<path id="@ID@" d="M 540 640 C 630 760 650 860 540 900 C 430 860 450 760 540 640 Z" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 30px rgba(232,194,106,0.9))"/>', "bd")
tl(f'tl.fromTo("#{bd}", {{opacity: 0, scale: 0.4, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.6, ease: "back.out(1.6)", immediateRender: false}}, {ix(105) - 0.05:.3f});')
tl(f'tl.fromTo("#{bd}", {{scale: 1, transformOrigin: "50% 50%"}}, {{scale: 1.06, duration: 0.5, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}}, {ix(108):.3f});')
cue(ix(105) - 0.05, "bell_E5", -16)
bl = s.label(540, 1000, "BE THE DROP", 72, GOLD, 0, 800, 0.08); s.fade(bl, ix(106) - 0.1, 0.4, y=10)
for k, d in enumerate(["TODAY", "TOMORROW"]):
    x = 380 + k * 320
    t_ = tile(s, x, 1140, 260, 90, f'<text x="{x}" y="1151" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" fill="{GOLD if k else "#fff"}">{d}</text>', GOLD if k else "#ffffff60", 0)
    s.pop(t_, ix(109) + k * 0.6, 0.4, 0.5, "50% 50%")
cue(ix(111), "pop_2", -18)
su = s.label(540, 1330, "SHOW UP AGAIN", 40, WHITE, 0, 800, 0.15); s.fade(su, ix(109), 0.4, y=10)

# 8  outro (handles, no end card)
s = S(ix(113) - 0.05, TOTAL)
es = s.spot(540, 0, "232,194,106", 40, 230); s.fade(es, ix(113), 0.6)
em = s.raw('<image id="@ID@" href="assets/otm_emblem.png" x="390" y="900" width="300" height="291" style="opacity:0;filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>', "i")
s.pop(em, ix(113), 0.7, 0.6, "50% 50%"); cue(ix(113), "bell_A4", -16)
o1l = s.label(540, 1300, "ORDER THE MARKET", 32, GOLD, 0, 800, 0.3); s.fade(o1l, ix(113) + 0.3, 0.5)
o2 = s.label(540, 1360, "DON'T LET THE MARKET ORDER YOU", 28, WHITE, 0, 700, 0.12); s.fade(o2, ix(116), 0.4)
o3 = s.pill(540, 1470, "FOLLOW FOR MORE", GOLD, "#111", 30); s.pop(o3, ix(122), 0.4, 0.6, "50% 50%"); cue(ix(122), "click-confirm_1", -16)
hx = 290
soc = s.raw(f'<g id="@ID@" style="opacity:0">'
            f'<rect x="{hx}" y="1548" width="36" height="36" rx="10" fill="none" stroke="#fff" stroke-width="3"/>'
            f'<circle cx="{hx + 18}" cy="1566" r="8.5" fill="none" stroke="#fff" stroke-width="3"/><circle cx="{hx + 28}" cy="1556" r="2.4" fill="#fff"/>'
            f'<text x="{hx + 48}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@fxzuez_28</text>'
            f'<path d="M {hx + 322} 1546 V 1574 A 9 9 0 1 1 {hx + 313} 1565 M {hx + 322} 1546 Q {hx + 326} 1557 {hx + 338} 1558" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>'
            f'<text x="{hx + 348}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@zuez_28</text></g>', "so")
disc = s.label(540, 1650, "EDUCATIONAL ONLY · NOT FINANCIAL ADVICE", 28, GREY, 0, 600, 0.12)
s.fade(soc, ix(116) + 0.6, 0.5, y=12)
s.fade(disc, ix(116) + 0.9, 0.5)
TIMELINE = ""


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
    <div id="root" data-composition-id="otm-bethedrop" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
{TIMELINE}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-bethedrop-audio" class="clip" src="assets/audio/mix_bethedrop.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-bethedrop"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
