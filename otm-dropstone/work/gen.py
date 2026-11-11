"""OTM "Drop by Drop": a glowing-figure trading parable in the OTM style (same scene system as otm-chance / otm-missed),
after the old water-and-stone idea, in original words. Traders hammer at the wall between them and consistent trading
(bigger lots, higher leverage, win it all back), blow up and walk away; one trader repeats one small edge the same way
every day (same risk, same rules, same journal); day 1, day 100 a crack, day 300 the stone splits and shows consistency;
water breaks stone by showing up drop after drop; consistency beats force. Voice only (Quentin), no music.
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

# 1  the long cave scene: the wall, the hammers, the blow-ups, the one trader, the drops, day 1 / 100 / 300, the split
o1, c1 = 0.0, ix(102) - 0.1
s = S(o1, c1, first=True)
ceiling(s)
behind = (f'<g><path d="{rrect(330, 860, 420, 300, 18)}" fill="#14120a" stroke="{GOLD}" stroke-width="3"/>'
          f'<path d="M 360 1110 L 430 1080 L 480 1095 L 550 1020 L 600 1035 L 690 950 L 720 930" fill="none" stroke="{GOLD}" stroke-width="7" stroke-linecap="round" style="filter:drop-shadow(0 0 12px rgba(232,194,106,0.9))"/>'
          f'<text x="540" y="905" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" letter-spacing="0.14em" fill="{GOLD}">CONSISTENCY</text></g>')
lh, rh, ca, cb, ol, le, re_ = stone(s, behind)
toplab(s, "PICTURE A WALL BETWEEN YOU AND", "CONSISTENT TRADING", 0.0, ix(8) - 0.1, GOLD, LBL, 52)
toplab(s, "MOST TRADERS TRY TO", "SMASH THROUGH IT", ix(8), ix(15) - 0.1)
toplab(s, "", "BIGGER LOTS", ix(15), ix(17) - 0.1, RED)
toplab(s, "", "HIGHER LEVERAGE", ix(17), ix(19) - 0.1, RED)
toplab(s, "ONE MORE TRADE TO", "WIN IT ALL BACK", ix(19), ix(27) - 0.1, RED)
toplab(s, "FOR A FEW WEEKS", "THEY SWING HARDER", ix(27), ix(38) - 0.1)
toplab(s, "", "THEN THEY BLOW UP", ix(38), ix(43) - 0.1, RED)
toplab(s, "", "AND WALK AWAY", ix(43), ix(45) - 0.1, "#9aa0a8")
crowd = []
for k, (x, flip) in enumerate([(110, False), (200, False), (880, True), (970, True)]):
    f = s.fig(x, 0.72, "#9aa0a8", 1, False); s.pop(f, ix(9) + k * 0.12, 0.35)
    h = hammer(s, x + (-30 if flip else 30), 1110, flip)
    s.pop(h, ix(12) + k * 0.1, 0.3, 0.5, "50% 50%")
    sw = -1 if flip else 1
    tl(f'tl.fromTo("#{h}", {{rotation: 0, svgOrigin: "{x + (-30 if flip else 30)} 1110"}}, {{rotation: {-28 * sw}, svgOrigin: "{x + (-30 if flip else 30)} 1110", duration: 0.22, yoyo: true, repeat: 15, ease: "power2.in", immediateRender: false}}, {ix(13) + k * 0.07:.3f});')
    tl(f'tl.fromTo("#{h}", {{rotation: 0, svgOrigin: "{x + (-30 if flip else 30)} 1110"}}, {{rotation: {-34 * sw}, svgOrigin: "{x + (-30 if flip else 30)} 1110", duration: 0.14, yoyo: true, repeat: 15, ease: "power2.in", immediateRender: false}}, {ix(31) + k * 0.05:.3f});')
    crowd.append((f, h, x, flip))
for k in range(5):
    cue(ix(13) + k * 0.45, "tock_1", -26)
for k in range(6):
    cue(ix(31) + k * 0.3, "tock_1", -24)
fl1 = s.raw(f'<rect id="@ID@" x="0" y="0" width="1080" height="1920" fill="{RED}" style="opacity:0"/>', "fl")
tl(f'tl.fromTo("#{fl1}", {{opacity: 0.22}}, {{opacity: 0, duration: 0.6, immediateRender: false}}, {ix(40) - 0.05:.3f});')
cue(ix(40) - 0.05, "land_1", -16)
for f, h, x, flip in crowd:
    tl(f'tl.to("#{h}", {{y: 120, rotation: {90 if flip else -90}, svgOrigin: "{x} 1110", opacity: 0, duration: 0.5, ease: "power2.in"}}, {ix(40):.3f});')
    tl(f'tl.to("#{f}", {{x: {420 if flip else -420}, opacity: 0, duration: 1.2, ease: "power1.in"}}, {ix(43) - 0.1:.3f});')
cue(ix(43), "whoosh-long_1", -22)
# the one trader, the drop
toplab(s, "ONE TRADER DOES", "SOMETHING DIFFERENT", ix(45), ix(50) - 0.1, GOLD)
one = s.fig(150, 0.8, WHITE); s.pop(one, ix(45), 0.45)
toplab(s, "HE FINDS", "ONE SMALL EDGE", ix(50), ix(55) - 0.1, GOLD)
toplab(s, "", "ONE SETUP", ix(55), ix(59) - 0.1, GOLD)
d0 = s.raw(f'<path id="@ID@" d="M 540 604 C 549 618 549 628 540 630 C 531 628 531 618 540 604 Z" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 10px {GOLD})"/>', "d0")
s.pop(d0, ix(53) - 0.1, 0.4, 0.3, "50% 0%"); cue(ix(53) - 0.1, "bell_E5", -18)
tl(f'tl.set("#{d0}", {{opacity: 0}}, {ix(59) - 0.05:.3f});')
toplab(s, "THE SAME WAY", "EVERY DAY", ix(59), ix(68) - 0.1, GOLD)
toplab(s, "", "SAME RISK", ix(68), ix(70) - 0.1)
toplab(s, "", "SAME RULES", ix(70), ix(72) - 0.1)
toplab(s, "", "SAME JOURNAL", ix(72), ix(74) - 0.1)
lands = drops(s, ix(59), ix(88), 0.75)
for k, t in enumerate(lands):
    if k % 3 == 0:
        cue(t, "tick_" + str(k % 3 + 1), -28)
toplab(s, "NOTHING CHANGES", "DAY 1", ix(74), ix(78) - 0.1, GOLD, "#9aa0a8", 72)
toplab(s, "A CRACK APPEARS", "DAY 100", ix(78), ix(83) - 0.1, GOLD, WHITE, 72)
s.draw(ca, ix(80) - 0.1, 0.6); cue(ix(80) - 0.1, "tick-crisp_2", -18)
toplab(s, "THE WALL GIVES WAY", "DAY 300", ix(83), ix(89) - 0.1, GOLD, GOLD, 72)
s.draw(cb, ix(84), 0.7)
tl(f'tl.set("#{ol}", {{opacity: 0}}, {ix(86):.3f});')
for half, edge, dx, rot, org in ((lh, le, -170, -7, "250 1240"), (rh, re_, 170, 7, "830 1240")):
    tl(f'tl.set("#{edge}", {{opacity: 1}}, {ix(86):.3f});')
    for el in (half, edge):
        tl(f'tl.to("#{el}", {{x: {dx}, rotation: {rot}, svgOrigin: "{org}", duration: 1.0, ease: "power3.inOut"}}, {ix(86):.3f});')
for c_ in (ca, cb):
    tl(f'tl.to("#{c_}", {{opacity: 0, duration: 0.2}}, {ix(86):.3f});')
cue(ix(86), "land_1", -14); cue(ix(87), "swell_2", -16)
tl(f'tl.to("#{one}", {{x: 230, duration: 1.2, ease: "power1.inOut"}}, {ix(87):.3f});')
toplab(s, "THE TRADERS WHO SWUNG HARDEST", "LEFT THE GAME", ix(89), c1, "#9aa0a8", LBL)
for x, flip in [(90, False), (990, True)]:
    hh = s.raw(f'<g id="@ID@" style="opacity:0"><line x1="{x - 50}" y1="1232" x2="{x + 40}" y2="1232" stroke="#5a606b" stroke-width="7" stroke-linecap="round"/>'
               f'<rect x="{x + (30 if not flip else -66)}" y="1206" width="36" height="30" rx="5" fill="#5a606b"/></g>', "dh")
    s.fade(hh, ix(92), 0.5)

# 2  "Water doesn't break stone with force. It breaks it by showing up, drop after drop."
s = S(ix(102) - 0.1, ix(117) - 0.1)
s.path("M 160 1240 C 200 1020 340 900 540 890 C 740 900 880 1020 920 1240", "#e9ecf1", 5, drawn=True, style="filter:drop-shadow(0 0 14px rgba(255,255,255,0.25))")
s.path(f"M 120 600 L 500 600 L 540 660 L 580 600 L 960 600", "#c9ced6", 4, drawn=True)
hl = s.path("M 540 890 L 548 930 L 532 970", "#e9ecf1", 4); s.draw(hl, ix(109), 1.4)
drops(s, ix(102) + 0.2, ix(117) - 0.6, 0.6, GOLD, 540, 668, 880)
toplab(s, "WATER DOESN'T BREAK STONE", "WITH FORCE", ix(102), ix(108) - 0.1, WHITE, LBL)
toplab(s, "IT BREAKS IT BY", "SHOWING UP", ix(108), ix(114) - 0.1, GOLD, LBL)
toplab(s, "", "DROP AFTER DROP", ix(114), ix(117) - 0.1, GOLD)
cue(ix(112), "swell_1", -20)

# 3  "In trading, consistency beats force every time."
s = S(ix(117) - 0.1, ix(124) - 0.05, ground=False)
s.label(540, 600, "IN TRADING", 30, LBL, 1, 700, 0.2)
fc = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(610, 700, 360, 380, 20)}" fill="#0f1319" stroke="#ffffff40" stroke-width="2.5"/>'
           f'<line x1="750" y1="930" x2="830" y2="830" stroke="#9aa0a8" stroke-width="10" stroke-linecap="round"/>'
           f'<rect x="800" y="780" width="60" height="80" rx="8" fill="#9aa0a8" transform="rotate(38 830 820)"/>'
           f'<text x="790" y="1030" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="36" fill="#9aa0a8">FORCE</text></g>', "fc")
cc = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 14px rgba(232,194,106,0.5))"><path d="{rrect(110, 700, 360, 380, 20)}" fill="#14120a" stroke="{GOLD}" stroke-width="3"/>'
           f'<path d="M 290 780 C 330 840 340 880 290 900 C 240 880 250 840 290 780 Z" fill="{GOLD}"/>'
           f'<text x="290" y="1030" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="32" fill="{GOLD}">CONSISTENCY</text></g>', "cc")
s.pop(cc, ix(119) - 0.1, 0.45, 0.5, "50% 50%"); s.pop(fc, ix(121) - 0.1, 0.4, 0.5, "50% 50%")
bt = s.label(540, 905, "BEATS", 30, WHITE, 0, 800, 0.15); s.fade(bt, ix(120) - 0.1, 0.3)
et = s.label(540, 1200, "EVERY TIME", 52, GOLD, 0, 800, 0.2); s.fade(et, ix(122) - 0.1, 0.4, y=10)
cue(ix(119) - 0.1, "bell_C5", -18); cue(ix(122) - 0.1, "bell_G5", -18)

# 4  outro (handles, no end card)
s = S(ix(124) - 0.05, TOTAL)
es = s.spot(540, 0, "232,194,106", 40, 230); s.fade(es, ix(124), 0.6)
em = s.raw('<image id="@ID@" href="assets/otm_emblem.png" x="390" y="900" width="300" height="291" style="opacity:0;filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>', "i")
s.pop(em, ix(124), 0.7, 0.6, "50% 50%"); cue(ix(124), "bell_A4", -16)
o1l = s.label(540, 1300, "ORDER THE MARKET", 32, GOLD, 0, 800, 0.3); s.fade(o1l, ix(124) + 0.3, 0.5)
o2 = s.label(540, 1360, "DON'T LET THE MARKET ORDER YOU", 28, WHITE, 0, 700, 0.12); s.fade(o2, ix(127), 0.4)
o3 = s.pill(540, 1470, "FOLLOW FOR MORE", GOLD, "#111", 30); s.pop(o3, ix(133), 0.4, 0.6, "50% 50%"); cue(ix(133), "click-confirm_1", -16)
hx = 290
soc = s.raw(f'<g id="@ID@" style="opacity:0">'
            f'<rect x="{hx}" y="1548" width="36" height="36" rx="10" fill="none" stroke="#fff" stroke-width="3"/>'
            f'<circle cx="{hx + 18}" cy="1566" r="8.5" fill="none" stroke="#fff" stroke-width="3"/><circle cx="{hx + 28}" cy="1556" r="2.4" fill="#fff"/>'
            f'<text x="{hx + 48}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@fxzuez_28</text>'
            f'<path d="M {hx + 322} 1546 V 1574 A 9 9 0 1 1 {hx + 313} 1565 M {hx + 322} 1546 Q {hx + 326} 1557 {hx + 338} 1558" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>'
            f'<text x="{hx + 348}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@zuez_28</text></g>', "so")
disc = s.label(540, 1650, "EDUCATIONAL ONLY · NOT FINANCIAL ADVICE", 28, GREY, 0, 600, 0.12)
s.fade(soc, ix(127) + 0.6, 0.5, y=12)
s.fade(disc, ix(127) + 0.9, 0.5)
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
    <div id="root" data-composition-id="otm-dropstone" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
{TIMELINE}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-dropstone-audio" class="clip" src="assets/audio/mix_dropstone.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-dropstone"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
