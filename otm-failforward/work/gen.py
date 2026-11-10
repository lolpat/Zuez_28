"""OTM "Fail Forward": a motivational glowing-figure video in the OTM style (same scene system as otm-chance / otm-missed),
the companion to otm-mostlosses (same reference idea, told as general motivation in original words). Nobody counts the
falls, only the day you stood up and stayed up; school taught you to hide mistakes; every no, closed door and dead end
was training; failure is never final unless you stop; 10 failures = 10 lessons; try again, fail smaller, learn faster,
keep showing up; the person you're becoming is built from every time you didn't quit. Voice only (Quentin), no music.
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

def header(s, text, col=LBL, op=1, y=590, size=30):
    return s.label(540, y, text, size, col, op, 700 if col == LBL else 800, 0.2 if size <= 32 else 0.06)

def xm(s, x, y, r=18, col=RED, w=6):
    return s.path(f"M {x - r} {y - r} L {x + r} {y + r} M {x + r} {y - r} L {x - r} {y + r}", col, w)

def tile(s, x, y, w, h, inner, stroke="#ffffff60", op=0, fill="#0f1319"):
    return s.raw(f'<g id="@ID@" style="opacity:{op}"><path d="{rrect(x - w / 2, y - h / 2, w, h, 16)}" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>{inner}</g>', "tl")

def fall(fid, t, d=0.35, hold=0.25):
    """the figure tips over and gets back up"""
    tl(f'tl.to("#{fid}", {{rotation: -82, transformOrigin: "50% 100%", duration: {d}, ease: "power2.in"}}, {t:.3f});')
    tl(f'tl.to("#{fid}", {{rotation: 0, transformOrigin: "50% 100%", duration: {d}, ease: "power2.out"}}, {t + d + hold:.3f});')

# 1  "Nobody counts how many times you fell. They only remember the day you stood up and stayed up."
s = S(0, ix(18) - 0.1, first=True)
s.label(540, 600, "NOBODY COUNTS", 48, WHITE, 1, 800, 0.06)
s.label(540, 660, "HOW MANY TIMES YOU FELL", 32, LBL, 1, 700, 0.12)
f1 = s.fig(540, 1.0, "#9aa0a8", 1, False)
for k, t in enumerate([0.25, 1.35, 2.45]):
    fall(f1, t)
    m = s.raw(f'<line id="@ID@" x1="{430 + k * 26}" y1="760" x2="{430 + k * 26}" y2="830" stroke="#9aa0a8" stroke-width="6" stroke-linecap="round" style="opacity:0"/>', "tm")
    s.fade(m, t + 0.35, 0.2); cue(t + 0.3, "land-light_1", -24)
for k in range(3, 6):
    m = s.raw(f'<line id="@ID@" x1="{430 + k * 26}" y1="760" x2="{430 + k * 26}" y2="830" stroke="#9aa0a8" stroke-width="6" stroke-linecap="round" style="opacity:0"/>', "tm")
    s.fade(m, 3.3 + (k - 3) * 0.2, 0.2)
s.raw(f'<line id="@ID@" x1="420" y1="815" x2="580" y2="775" stroke="#9aa0a8" stroke-width="6" stroke-linecap="round" style="opacity:0"/>', "tm")
s.fade(s.items[-1].split('"')[1], 4.0, 0.2)
sp1 = s.spot(540, 0, "232,194,106"); s.fade(sp1, ix(12) - 0.1, 0.5)
g1 = s.fig(540, 1.0, GOLD, 0); s.fade(g1, ix(13) - 0.1, 0.5)
tl(f'tl.to("#{f1}", {{opacity: 0, duration: 0.4}}, {ix(13) - 0.1:.3f});')
cue(ix(13) - 0.1, "swell_1", -18)
su = s.label(540, 1330, "AND STAYED UP", 44, GOLD, 0, 800, 0.14); s.fade(su, ix(16) - 0.1, 0.4, y=10)

# 2  "School taught you that mistakes are something to hide. A red mark, a lower grade."
s = S(ix(18) - 0.1, ix(33) - 0.1, ground=False, restore=False)
header(s, "SCHOOL")
s.raw(f'<g id="@ID@"><path d="{rrect(250, 680, 400, 500, 12)}" fill="#f3ead8" stroke="#c9bfa8" stroke-width="3"/>'
      + "".join(f'<line x1="290" y1="{780 + k * 58}" x2="{610 - (k % 2) * 70}" y2="{780 + k * 58}" stroke="#b9ad93" stroke-width="4"/>' for k in range(6)) + '</g>', "pp")
rm = s.raw(f'<ellipse id="@ID@" cx="460" cy="896" rx="160" ry="40" fill="none" stroke="{RED}" stroke-width="6" style="opacity:0"/>', "rm")
s.draw(rm, ix(28) - 0.1, 0.4) if False else s.fade(rm, ix(28) - 0.1, 0.3)
cue(ix(28) - 0.1, "tock_1", -18)
gd = s.raw(f'<g id="@ID@" style="opacity:0"><circle cx="800" cy="820" r="92" fill="none" stroke="{RED}" stroke-width="5"/>'
           f'<text x="800" y="860" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="116" fill="{RED}">D</text></g>', "gd")
s.pop(gd, ix(31) - 0.1, 0.4, 0.5, "50% 50%"); cue(ix(31) - 0.1, "land-light_1", -18)
hd = s.label(540, 1300, "SOMETHING TO HIDE", 40, "#9aa0a8", 0, 800, 0.1); s.fade(hd, ix(25) - 0.1, 0.4, y=10)

# 3  "But life works the other way. Every no you heard, every door that didn't open, every attempt that went nowhere. None of it was wasted."
s = S(ix(33) - 0.1, ix(58) - 0.1, ground=False, hide=False)
lw = header(s, "BUT LIFE WORKS THE OTHER WAY", GOLD, 0, 600, 40); s.fade(lw, ix(33), 0.4, y=10)
icons = [
    (220, ix(40), f'<path d="{rrect(150, 760, 140, 100, 22)}" fill="none" stroke="#fff" stroke-width="5"/><path d="M 190 858 L 175 895 L 220 858" fill="none" stroke="#fff" stroke-width="5" stroke-linejoin="round"/>'
                  f'<text x="220" y="826" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="44" fill="#fff">NO</text>', "EVERY NO"),
    (540, ix(44), f'<rect x="480" y="740" width="120" height="180" rx="6" fill="none" stroke="#fff" stroke-width="5"/><circle cx="580" cy="835" r="7" fill="#fff"/>'
                  f'<path d="M 470 750 L 610 910" stroke="{RED}" stroke-width="6" stroke-linecap="round"/>', "CLOSED DOORS"),
    (860, ix(49), f'<path d="M 780 900 H 900 V 800" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-dasharray="1 0"/>'
                  f'<rect x="880" y="760" width="60" height="16" fill="#fff"/><path d="M 900 800 L 890 788" stroke="#fff" stroke-width="6"/>', "DEAD ENDS"),
]
for k, (x, t, ic, lab) in enumerate(icons):
    tt = tile(s, x, 830, 260, 260, ic.replace('#fff', '#c9ced6') + f'<text x="{x}" y="1000" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" fill="{LBL}">{lab}</text>', "#ffffff50", 0)
    s.pop(tt, t - 0.1, 0.4, 0.5, "50% 50%"); cue(t - 0.1, "tick-crisp_" + str(k + 1), -20)
    gt = tile(s, x, 830, 260, 260, ic.replace('#fff', GOLD) + f'<text x="{x}" y="1000" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" fill="{GOLD}">{lab}</text>', GOLD, 0)
    s.fade(gt, ix(53) + k * 0.15, 0.4)
nw = s.label(540, 1260, "NONE OF IT WAS WASTED", 44, GOLD, 0, 800, 0.06); s.fade(nw, ix(53), 0.4, y=10)
cue(ix(53), "bell_E5", -18)

# 4  "It was training. Each failure showed you one more way that doesn't work, and pushed you one step closer to the way that does."
s = S(ix(58) - 0.1, ix(82) - 0.1)
tr = header(s, "IT WAS TRAINING", GOLD, 0, 600, 44); s.fade(tr, ix(58), 0.4, y=10)
steps = "M 80 1240 H 260 V 1150 H 420 V 1060 H 580 V 970 H 740 V 880 H 900"
s.path(steps, "#ffffffa0", 4, drawn=True)
for k, (x, y) in enumerate([(340, 1150), (500, 1060), (660, 970)]):
    m = xm(s, x, y - 40, 14, RED, 5); s.draw(m, ix(63) + k * 0.4, 0.25); cue(ix(63) + k * 0.4, "tick_" + str(k + 1), -22)
door = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 22px rgba(232,194,106,0.8))"><rect x="830" y="700" width="110" height="180" rx="6" fill="{GOLD}" fill-opacity="0.25" stroke="{GOLD}" stroke-width="5"/>'
             f'<circle cx="920" cy="795" r="7" fill="{GOLD}"/></g>', "dr")
s.fade(door, ix(78) - 0.2, 0.5); cue(ix(78) - 0.2, "swell_2", -18)
wd = s.label(885, 670, "THE WAY THAT DOES", 28, GOLD, 0, 800, 0.08); s.fade(wd, ix(79), 0.35)
cl = s.fig(170, 0.7, WHITE)
for k, (dx, dy, t) in enumerate([(160, -90, ix(64)), (160, -90, ix(72)), (160, -90, ix(75)), (160, -90, ix(77))]):
    tl(f'tl.to("#{cl}", {{x: "+={dx}", y: "+={dy}", duration: 0.5, ease: "power2.inOut"}}, {t:.3f});')

# 5  "Failure is never final, unless you stop."
s = S(ix(82) - 0.1, ix(89) - 0.1)
fa = s.label(540, 740, "FAILURE IS", 52, WHITE, 0, 800, 0.06); s.fade(fa, ix(82) - 0.05, 0.4, y=10)
nf = s.label(540, 840, "NEVER FINAL", 80, GOLD, 0, 800, 0.04)
tl(f'tl.fromTo("#{nf}", {{opacity: 0, scale: 1.3, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.45, ease: "expo.out", immediateRender: false}}, {ix(84) - 0.1:.3f});')
cue(ix(84) - 0.1, "bell_C5", -18)
f5 = s.fig(380, 0.9, WHITE)
stp = s.raw(f'<g id="@ID@" style="opacity:0"><path d="M 650 960 L 710 960 L 750 1000 L 750 1060 L 710 1100 L 650 1100 L 610 1060 L 610 1000 Z" fill="{RED}"/>'
            f'<text x="680" y="1042" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" fill="#fff">STOP</text>'
            f'<rect x="676" y="1100" width="8" height="140" fill="#c9ced6"/></g>', "st")
s.pop(stp, ix(87) - 0.1, 0.35, 0.4, "50% 100%"); cue(ix(87) - 0.1, "tock_1", -16)
tl(f'tl.to("#{f5}", {{opacity: 0.4, duration: 0.4}}, {ix(87):.3f});')
us = s.label(540, 1330, "UNLESS YOU STOP", 40, RED, 0, 800, 0.12); s.fade(us, ix(86), 0.35, y=10)

# 6  "Ten failures means ten lessons. Zero failures means you never really tried."
s = S(ix(89) - 0.1, ix(101) - 0.1, ground=False)
c1 = tile(s, 290, 900, 400, 470, f'<text x="290" y="720" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" fill="#fff">10 FAILURES</text>', "#ffffff60", 0)
s.pop(c1, ix(89), 0.4, 0.6, "50% 50%")
for k in range(10):
    x, y = 170 + (k % 5) * 60, 820 + (k // 5) * 80
    xx = xm(s, x, y, 14, RED, 5); s.draw(xx, ix(90) + k * 0.05, 0.15)
    bulb = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 8px {GOLD})"><circle cx="{x}" cy="{y - 4}" r="16" fill="{GOLD}"/><rect x="{x - 8}" y="{y + 12}" width="16" height="10" rx="3" fill="{GOLD}"/></g>', "bu")
    tl(f'tl.to("#{xx}", {{opacity: 0, duration: 0.2}}, {ix(92) + k * 0.06:.3f});')
    s.fade(bulb, ix(92) + k * 0.06, 0.25)
l10 = s.label(290, 1060, "= 10 LESSONS", 36, GOLD, 0, 800, 0.06); s.fade(l10, ix(93) - 0.1, 0.35, y=10)
cue(ix(92), "bell_G5", -18)
c2 = tile(s, 790, 900, 400, 470, f'<text x="790" y="720" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" fill="#9aa0a8">0 FAILURES</text>'
          f'<circle cx="790" cy="870" r="70" fill="none" stroke="#5a606b" stroke-width="5" stroke-dasharray="12 10"/>', "#ffffff30", 0)
s.pop(c2, ix(94) - 0.1, 0.4, 0.6, "50% 50%")
nt = s.label(790, 1060, "= NEVER TRIED", 36, "#9aa0a8", 0, 800, 0.06); s.fade(nt, ix(98) - 0.1, 0.35, y=10)
cue(ix(98) - 0.1, "tock_1", -18)

# 7  "So try again, fail smaller, learn faster, and keep showing up."
s = S(ix(101) - 0.1, ix(112) - 0.1)
rows = [("TRY AGAIN", ix(102)), ("FAIL SMALLER", ix(104)), ("LEARN FASTER", ix(106)), ("KEEP SHOWING UP", ix(109))]
for k, (txt, t) in enumerate(rows):
    y = 640 + k * 100
    r = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(220, y - 38, 640, 76, 38)}" fill="{GOLD if k == 3 else "#0f1319"}" stroke="{GOLD}" stroke-width="3"/>'
              f'<text x="540" y="{y + 12}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" letter-spacing="0.06em" fill="{"#111" if k == 3 else "#fff"}">{txt}</text></g>', "rw")
    tl(f'tl.fromTo("#{r}", {{opacity: 0, x: -50}}, {{opacity: 1, x: 0, duration: 0.4, ease: "power3.out", immediateRender: false}}, {t - 0.1:.3f});')
    cue(t - 0.1, "pop_" + str(k + 1), -18)
f7 = s.fig(140, 0.8, WHITE); s.walk(f7, ix(101), 800, ix(111) - ix(101) + 0.4)

# 8  "Because the person you're becoming is built from every time you didn't quit."
s = S(ix(112) - 0.1, ix(125) - 0.05)
pb = header(s, "THE PERSON YOU'RE BECOMING", WHITE, 0, 600, 40); s.fade(pb, ix(113) - 0.1, 0.4, y=10)
sp8 = s.spot(540, 1, "232,194,106", 40, 220, y0=640)
s.fig(540, 2.0, GOLD, 1, False, GY, True)
cid = s.uid("cp"); rid = s.uid("cr")
s.items.append(f'<defs><clipPath id="{cid}"><rect id="{rid}" x="0" y="1240" width="1080" height="0"/></clipPath></defs>')
s.raw(f'<g id="@ID@" clip-path="url(#{cid})"><g transform="translate(540,{GY}) scale(2)"><g style="filter:drop-shadow(0 0 18px rgba(232,194,106,0.7))">'
      f'<circle cx="0" cy="-158" r="31" fill="{GOLD}"/><path d="M -48 0 L -48 -66 Q -48 -116 0 -116 Q 48 -116 48 -66 L 48 0 Z" fill="{GOLD}"/></g></g></g>', "gf")
tl(f'tl.fromTo("#{rid}", {{attr: {{y: 1240, height: 0}}}}, {{attr: {{y: 840, height: 400}}, duration: {ix(124) - ix(117) + 0.4:.3f}, ease: "power1.inOut", immediateRender: false}}, {ix(117) - 0.1:.3f});')
for k in range(8):
    y = 1225 - k * 50
    b = s.raw(f'<rect id="@ID@" x="{560 + (k % 2) * 20 - 330}" y="{y - 12}" width="40" height="24" rx="4" fill="{GOLD}" style="opacity:0"/>', "bk")
    t = ix(117) + k * (ix(124) - ix(117)) / 8
    tl(f'tl.fromTo("#{b}", {{opacity: 1, x: 0}}, {{opacity: 0, x: 300, duration: 0.35, ease: "power2.in", immediateRender: false}}, {t:.3f});')
    cue(t, "tick_" + str(k % 3 + 1), -26)
bf = s.label(540, 1330, "BUILT FROM EVERY TIME", 40, GOLD, 0, 800, 0.08); s.fade(bf, ix(118) - 0.1, 0.4, y=10)
dq = s.label(540, 1400, "YOU DIDN'T QUIT", 48, WHITE, 0, 800, 0.08); s.fade(dq, ix(122) - 0.1, 0.4, y=10)
cue(ix(122) - 0.1, "swell_2", -16)

# 9  outro (handles, no end card)
s = S(ix(125) - 0.05, TOTAL)
es = s.spot(540, 0, "232,194,106", 40, 230); s.fade(es, ix(125), 0.6)
em = s.raw('<image id="@ID@" href="assets/otm_emblem.png" x="390" y="900" width="300" height="291" style="opacity:0;filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>', "i")
s.pop(em, ix(125), 0.7, 0.6, "50% 50%"); cue(ix(125), "bell_A4", -16)
o1 = s.label(540, 1300, "ORDER THE MARKET", 32, GOLD, 0, 800, 0.3); s.fade(o1, ix(125) + 0.3, 0.5)
o2 = s.label(540, 1360, "DON'T LET THE MARKET ORDER YOU", 28, WHITE, 0, 700, 0.12); s.fade(o2, ix(128), 0.4)
o3 = s.pill(540, 1470, "FOLLOW FOR MORE", GOLD, "#111", 30); s.pop(o3, ix(134), 0.4, 0.6, "50% 50%"); cue(ix(134), "click-confirm_1", -16)
hx = 290
soc = s.raw(f'<g id="@ID@" style="opacity:0">'
            f'<rect x="{hx}" y="1548" width="36" height="36" rx="10" fill="none" stroke="#fff" stroke-width="3"/>'
            f'<circle cx="{hx + 18}" cy="1566" r="8.5" fill="none" stroke="#fff" stroke-width="3"/><circle cx="{hx + 28}" cy="1556" r="2.4" fill="#fff"/>'
            f'<text x="{hx + 48}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@fxzuez_28</text>'
            f'<path d="M {hx + 322} 1546 V 1574 A 9 9 0 1 1 {hx + 313} 1565 M {hx + 322} 1546 Q {hx + 326} 1557 {hx + 338} 1558" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>'
            f'<text x="{hx + 348}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@zuez_28</text></g>', "so")
disc = s.label(540, 1650, "EDUCATIONAL ONLY · NOT FINANCIAL ADVICE", 28, GREY, 0, 600, 0.12)
s.fade(soc, ix(128) + 0.6, 0.5, y=12)
s.fade(disc, ix(128) + 0.9, 0.5)
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
    <div id="root" data-composition-id="otm-failforward" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
{TIMELINE}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-failforward-audio" class="clip" src="assets/audio/mix_failforward.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-failforward"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
