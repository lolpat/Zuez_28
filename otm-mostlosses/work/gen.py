"""OTM "The Trader With the Most Losses": a glowing-figure explainer in the OTM style (same scene system as otm-chance /
otm-missed), inspired by a "the student who fails the most" explainer, rewritten for trading in original words. In school
a mistake cost points; in the market losses aren't graded and only what works gets paid, over time. Test, lose small,
write it down; three strategies; the journal; when a loss gets expensive (big, or nothing learned); small written losses
become data; data is the difference between guessing and an edge; 100 lessons vs 0; a small loss is the fee for finding
out what works. Voice only (Quentin), no music. Scenes key off word indices of work/words.json (helper ix)."""
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

def header(s, text, col=LBL, op=1):
    return s.label(540, 590, text, 30, col, op, 700, 0.2)

def check(s, x, y, col=GOLD, sz=1.0, w=6):
    return s.path(f"M {x - 16 * sz} {y} L {x - 4 * sz} {y + 13 * sz} L {x + 18 * sz} {y - 15 * sz}", col, w)

def xm(s, x, y, r=18, col=RED, w=6):
    return s.path(f"M {x - r} {y - r} L {x + r} {y + r} M {x + r} {y - r} L {x - r} {y + r}", col, w)

def tile(s, x, y, w, h, inner, stroke="#ffffff60", op=0, fill="#0f1319"):
    return s.raw(f'<g id="@ID@" style="opacity:{op}"><path d="{rrect(x - w / 2, y - h / 2, w, h, 14)}" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>{inner}</g>', "tl")

def mini(x, y, pts, col, w=4):
    return f'<path d="M ' + " L ".join(f"{x + px:.0f} {y + py:.0f}" for px, py in pts) + f'" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'

# 1  "The trader with the most losing trades... is often the one who ends up consistent."
s = S(0, ix(15) - 0.1, first=True)
s.label(540, 590, "THE TRADER WITH THE", 30, LBL, 1, 700, 0.2)
s.label(540, 650, "MOST LOSING TRADES", 46, RED, 1, 800, 0.06)
for k in range(12):
    x, y = 300 + (k % 6) * 96, 760 + (k // 6) * 96
    t = tile(s, x, y, 72, 72, f'<path d="M {x - 14} {y - 14} L {x + 14} {y + 14} M {x + 14} {y - 14} L {x - 14} {y + 14}" stroke="{RED}" stroke-width="5" stroke-linecap="round"/>', "#ff4d5e80", 1 if k < 6 else 0)
    if k >= 6:
        s.pop(t, ix(5) + (k - 6) * 0.08, 0.3, 0.5, "50% 50%")
cue(ix(5), "tick_1", -22)
eq = s.path("M 160 1080 L 260 1060 L 330 1090 L 430 1020 L 500 1040 L 610 960 L 680 985 L 800 900 L 920 860", GOLD, 6, style="filter:drop-shadow(0 0 10px rgba(232,194,106,0.8))")
s.draw(eq, ix(12) - 0.3, 1.0)
ec = s.label(540, 1330, "ENDS UP CONSISTENT", 40, GOLD, 0, 800, 0.1); s.fade(ec, ix(13) - 0.1, 0.4, y=10)
cue(ix(12) - 0.3, "swell_1", -18)
s.spot(540, 0.5, "232,194,106", y0=1100)
y1 = s.fig(540, 0.55, GOLD)

# 2  "Most people think a losing trade means you're falling behind."
s = S(ix(15) - 0.1, ix(25) - 0.1)
header(s, "MOST PEOPLE THINK")
s.path("M 80 1180 H 1000", "#ffffff30", 3, drawn=True, extra='stroke-dasharray="14 12"')
others = []
for k, x in enumerate([560, 700, 840]):
    f = s.fig(x, 0.75, "#9aa0a8", 0.9, False); others.append(f)
    tl(f'tl.to("#{f}", {{x: 120, duration: 2.6, ease: "none"}}, {ix(15):.3f});')
yo = s.fig(420, 0.8, WHITE); s.pop(yo, ix(15), 0.35)
tl(f'tl.to("#{yo}", {{x: -260, duration: 1.0, ease: "power2.out"}}, {ix(21):.3f});')
lt = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="380" y="900" width="80" height="60" rx="10" fill="{RED}"/>'
           f'<text x="420" y="942" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" fill="#fff">L</text></g>', "lt")
s.pop(lt, ix(18) - 0.1, 0.35, 0.5, "50% 50%")
tl(f'tl.to("#{lt}", {{x: -260, duration: 1.0, ease: "power2.out"}}, {ix(21):.3f});')
fb = s.label(540, 720, "FALLING BEHIND?", 48, WHITE, 0, 800, 0.06); s.fade(fb, ix(23) - 0.1, 0.4, y=10)
cue(ix(18) - 0.1, "tock_1", -18); cue(ix(21), "whoosh-short_2", -22)

# 3  "In school, it did. Every mistake cost you points."
s = S(ix(25) - 0.1, ix(34) - 0.1)
header(s, "IN SCHOOL")
paper = s.raw(f'<g id="@ID@"><path d="{rrect(280, 680, 380, 480, 12)}" fill="#f3ead8" stroke="#c9bfa8" stroke-width="3"/>'
              + "".join(f'<line x1="320" y1="{790 + k * 56}" x2="{600 - (k % 2) * 60}" y2="{790 + k * 56}" stroke="#b9ad93" stroke-width="4"/>' for k in range(6)) + '</g>', "pp")
ga = s.raw(f'<g id="@ID@"><circle cx="790" cy="800" r="90" fill="none" stroke="{GOLD}" stroke-width="5"/>'
           f'<text x="790" y="838" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="110" fill="{GOLD}">A</text></g>', "ga")
gc = s.raw(f'<g id="@ID@" style="opacity:0"><circle cx="790" cy="800" r="90" fill="none" stroke="{RED}" stroke-width="5"/>'
           f'<text x="790" y="838" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="110" fill="{RED}">C</text></g>', "gc")
for k in range(3):
    m = xm(s, 610, 790 + k * 112, 18, RED, 6); s.draw(m, ix(29) + k * 0.25, 0.25)
    cue(ix(29) + k * 0.25, "tick-crisp_" + str(k + 1), -20)
tl(f'tl.to("#{ga}", {{opacity: 0, duration: 0.3}}, {ix(31) - 0.1:.3f});'); s.fade(gc, ix(31) - 0.1, 0.3)
pts = s.label(790, 960, "−10 POINTS", 36, RED, 0, 800, 0.06); s.fade(pts, ix(32) - 0.1, 0.35, y=10)
cue(ix(31), "tock_1", -16)

# 4  "But in the market, the rules flip. Nobody grades your losses. The market only pays for what works, over time."
s = S(ix(34) - 0.1, ix(54) - 0.1)
fl = s.label(540, 600, "THE RULES FLIP", 48, GOLD, 0, 800, 0.08); s.fade(fl, ix(38) - 0.1, 0.4, y=10)
front = s.raw(f'<g id="@ID@"><path d="{rrect(220, 700, 640, 420, 24)}" fill="#f3ead8" stroke="#c9bfa8" stroke-width="3"/>'
              f'<text x="540" y="930" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="60" letter-spacing="0.1em" fill="#6b5130">SCHOOL</text></g>', "fr")
back = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(220, 700, 640, 420, 24)}" fill="#0f1319" stroke="{GOLD}" stroke-width="4"/>'
             f'<text x="540" y="780" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="40" letter-spacing="0.14em" fill="{GOLD}">THE MARKET</text></g>', "bk")
tl(f'tl.fromTo("#{front}", {{scaleX: 1, transformOrigin: "50% 50%"}}, {{scaleX: 0, duration: 0.25, ease: "power2.in", immediateRender: false}}, {ix(39) - 0.1:.3f});')
tl(f'tl.fromTo("#{back}", {{opacity: 1, scaleX: 0, transformOrigin: "50% 50%"}}, {{opacity: 1, scaleX: 1, duration: 0.25, ease: "power2.out", immediateRender: false}}, {ix(39) + 0.15:.3f});')
cue(ix(39) - 0.1, "whoosh-short_1", -18)
r1 = s.raw(f'<g id="@ID@" style="opacity:0"><text x="270" y="880" font-family="Montserrat" font-weight="800" font-size="34" fill="{LBL}">LOSSES</text>'
           f'<text x="810" y="880" text-anchor="end" font-family="Montserrat" font-weight="800" font-size="34" fill="#9aa0a8">NOT GRADED</text></g>', "r1")
s.fade(r1, ix(41) - 0.1, 0.35)
r2 = s.raw(f'<g id="@ID@" style="opacity:0"><text x="270" y="970" font-family="Montserrat" font-weight="800" font-size="34" fill="{LBL}">WHAT WORKS</text>'
           f'<text x="810" y="970" text-anchor="end" font-family="Montserrat" font-weight="800" font-size="34" fill="{GOLD}">GETS PAID</text></g>', "r2")
s.fade(r2, ix(48) - 0.1, 0.35); cue(ix(48) - 0.1, "bell_C5", -20)
ot = s.path("M 280 1080 L 380 1060 L 440 1075 L 540 1030 L 600 1045 L 700 1000 L 800 990", GOLD, 5); s.draw(ot, ix(52) - 0.2, 0.9)
s.label(540, 1180, "OVER TIME", 30, GOLD, 0, 800, 0.2); s.fade(s.items[-1].split('"')[1], ix(52), 0.4)

# 5  "And the fastest way to find what works is to test, lose small, and write it down."
s = S(ix(54) - 0.1, ix(71) - 0.1)
header(s, "THE FASTEST WAY")
steps5 = [(540, 760, "TEST", ix(64), "flask"), (790, 1040, "LOSE SMALL", ix(65), "bar"), (290, 1040, "WRITE IT DOWN", ix(68), "pen")]
for k, (x, y, lab, t, icon) in enumerate(steps5):
    if icon == "flask":
        ic = f'<path d="M {x - 22} {y - 50} H {x + 22} M {x - 14} {y - 50} V {y - 10} L {x - 44} {y + 40} H {x + 44} L {x + 14} {y - 10} V {y - 50}" fill="none" stroke="{GOLD}" stroke-width="5" stroke-linejoin="round"/><circle cx="{x}" cy="{y + 22}" r="8" fill="{GOLD}"/>'
    elif icon == "bar":
        ic = f'<rect x="{x - 40}" y="{y + 10}" width="80" height="26" rx="4" fill="{RED}"/><line x1="{x - 60}" y1="{y + 36}" x2="{x + 60}" y2="{y + 36}" stroke="#fff" stroke-width="3"/>'
    else:
        ic = f'<rect x="{x - 40}" y="{y - 46}" width="80" height="96" rx="6" fill="#f3ead8"/>' + "".join(f'<line x1="{x - 28}" y1="{y - 26 + j * 20}" x2="{x + 28}" y2="{y - 26 + j * 20}" stroke="#b9ad93" stroke-width="3"/>' for j in range(4))
    t_ = tile(s, x, y, 300, 200, ic + f'<text x="{x}" y="{y + 85}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" fill="#fff">{lab}</text>', "#ffffff60", 0)
    s.pop(t_, t - 0.1, 0.4, 0.5, "50% 50%"); cue(t - 0.1, "pop_" + str(k + 1), -18)
for k, d in enumerate(["M 690 800 Q 770 840 790 930", "M 630 1050 H 450", "M 290 930 Q 300 840 390 790"]):
    a = s.path(d, "#ffffff70", 3); s.draw(a, [ix(65), ix(68), ix(69) + 0.3][k], 0.4)
fw = s.label(540, 1330, "WHAT WORKS", 40, GOLD, 0, 800, 0.15); s.fade(fw, ix(60), 0.4, y=10)

# 6  "Picture a new trader. His first strategy gets stopped out. The second one bleeds slowly. The third one works, and he doesn't know why yet."
s = S(ix(71) - 0.1, ix(96) - 0.1)
header(s, "A NEW TRADER")
y6 = s.fig(540, 0.8, WHITE); s.pop(y6, ix(71), 0.4)
strat = [(220, "STRATEGY 1", [(0, 30), (30, 10), (60, 20), (90, -10), (110, 60)], RED, ix(79), "STOPPED OUT"),
         (540, "STRATEGY 2", [(0, -10), (30, 0), (60, 10), (90, 22), (110, 34)], RED, ix(84), "SLOW BLEED"),
         (860, "STRATEGY 3", [(0, 30), (30, 20), (60, 10), (90, -10), (110, -30)], GOLD, ix(89), "WORKS")]
for k, (x, name, pts, col, t, res) in enumerate(strat):
    tt = tile(s, x, 790, 260, 190, f'<text x="{x}" y="728" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" fill="{LBL}">{name}</text>'
              + mini(x - 55, 800, pts, col, 5)
              + f'<text x="{x}" y="868" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" fill="{col}">{res}</text>', col + "90", 0)
    s.pop(tt, [ix(76), ix(82), ix(87)][k] - 0.1, 0.4, 0.5, "50% 50%")
    cue(t - 0.1, "tock_1" if col == RED else "bell_E5", -18)
q = s.label(860, 650, "?", 64, GOLD, 0, 800, 0); s.pop(q, ix(93) - 0.1, 0.35, 0.4, "50% 50%")
wy = s.label(700, 1000, "HE DOESN'T KNOW WHY YET", 28, LBL, 0, 700, 0.06); s.fade(wy, ix(92), 0.35)

# 7  "But every loss is in his journal, and every loss tells him something about price."
s = S(ix(96) - 0.1, ix(111) - 0.1)
header(s, "HIS JOURNAL")
s.raw(f'<g id="@ID@"><path d="{rrect(130, 680, 470, 560, 16)}" fill="#f3ead8" stroke="{GOLD}" stroke-width="3"/>'
      f'<line x1="180" y1="680" x2="180" y2="1240" stroke="#d9a9a0" stroke-width="3"/></g>', "jr")
entries = ["#1  STOPPED OUT", "#2  SLOW BLEED", "#3  ENTERED EARLY", "#4  NEWS SPIKE", "#5  WRONG LEVEL"]
for k, e in enumerate(entries):
    y = 760 + k * 92
    en = s.raw(f'<g id="@ID@" style="opacity:0"><text x="205" y="{y}" font-family="Montserrat" font-weight="800" font-size="28" fill="#a3262f">{e}</text>'
               f'<line x1="205" y1="{y + 22}" x2="560" y2="{y + 22}" stroke="#b9ad93" stroke-width="2"/></g>', "en")
    s.fade(en, ix(98) + k * 0.3, 0.3); cue(ix(98) + k * 0.3, "key_" + ("3" if k % 2 else "5"), -24)
lessons = ["TIMING", "LEVELS", "VOLATILITY"]
for k, l in enumerate(lessons):
    y = 800 + k * 150
    ar = s.path(f"M 620 {y - 10} H 700", GOLD, 4); s.draw(ar, ix(106) + k * 0.25, 0.25)
    p = s.pill(840, y - 10, l, GOLD, "#111", 28); s.pop(p, ix(107) + k * 0.25, 0.35, 0.5, "50% 50%")
    cue(ix(107) + k * 0.25, "pop_" + str(k + 1), -20)
ab = s.label(840, 700, "ABOUT PRICE", 30, GOLD, 0, 800, 0.15); s.fade(ab, ix(109) - 0.1, 0.35)

# 8  "A loss only gets expensive when it's big, or when you learn nothing from it."
s = S(ix(111) - 0.1, ix(126) - 0.1)
header(s, "WHEN A LOSS GETS EXPENSIVE", RED)
bl = tile(s, 300, 900, 380, 360, f'<rect x="200" y="760" width="200" height="220" fill="{RED}" style="filter:drop-shadow(0 0 14px rgba(255,77,94,0.6))"/>'
          f'<text x="300" y="1040" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" fill="#fff">IT’S BIG</text>', "#ff4d5e90", 0)
s.pop(bl, ix(118) - 0.15, 0.4, 0.5, "50% 50%"); cue(ix(118) - 0.15, "land_1", -16)
nl = tile(s, 780, 900, 380, 360, f'<rect x="700" y="760" width="160" height="200" rx="6" fill="#f3ead8"/>'
          f'<path d="M 740 820 L 820 900 M 820 820 L 740 900" stroke="{RED}" stroke-width="7" stroke-linecap="round"/>'
          f'<text x="780" y="1040" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" fill="#fff">NOTHING LEARNED</text>', "#ff4d5e90", 0)
s.pop(nl, ix(122) - 0.15, 0.4, 0.5, "50% 50%"); cue(ix(122) - 0.15, "tock_1", -16)
s.label(540, 908, "OR", 34, LBL, 0, 800, 0.2); s.fade(s.items[-1].split('"')[1], ix(119), 0.3)

# 9  "Keep it small, keep it written, and every losing trade turns into data."
s = S(ix(126) - 0.1, ix(139) - 0.1)
header(s, "KEEP IT")
bars = []
for k in range(6):
    x = 230 + k * 124
    rb = s.raw(f'<rect id="@ID@" x="{x - 40}" y="820" width="80" height="240" fill="{RED}" style="opacity:0.9"/>', "rb")
    tl(f'tl.to("#{rb}", {{attr: {{y: 1000, height: 60}}, duration: 0.5, ease: "power2.inOut"}}, {ix(128) - 0.1 + k * 0.06:.3f});')
    pen = s.path(f"M {x - 40} 1090 H {x + 40}", "#f3ead8", 4); s.draw(pen, ix(130) + k * 0.1, 0.2)
    gb = s.raw(f'<rect id="@ID@" x="{x - 40}" y="{1060 - (60 + k * 40 + (k % 2) * 30)}" width="80" height="{60 + k * 40 + (k % 2) * 30}" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 10px rgba(232,194,106,0.6))"/>', "gb")
    tl(f'tl.to("#{rb}", {{opacity: 0, duration: 0.3}}, {ix(136) + k * 0.08:.3f});')
    tl(f'tl.fromTo("#{gb}", {{opacity: 0, scaleY: 0, transformOrigin: "50% 100%"}}, {{opacity: 1, scaleY: 1, duration: 0.45, ease: "back.out(1.6)", immediateRender: false}}, {ix(136) + k * 0.08:.3f});')
s.raw('<line id="@ID@" x1="150" y1="1060" x2="930" y2="1060" stroke="#ffffff70" stroke-width="3"/>', "ax")
k1 = s.label(330, 680, "SMALL", 40, WHITE, 0, 800, 0.15); s.fade(k1, ix(127), 0.35, y=10)
k2 = s.label(750, 680, "WRITTEN", 40, WHITE, 0, 800, 0.15); s.fade(k2, ix(130), 0.35, y=10)
dt = s.label(540, 1180, "= DATA", 56, GOLD, 0, 800, 0.15); s.fade(dt, ix(138) - 0.1, 0.4, y=10)
cue(ix(128), "swell_2", -22); cue(ix(136), "bell_G5", -18)

# 10  "Data is the difference between guessing and having an edge."
s = S(ix(139) - 0.1, ix(149) - 0.1)
gq = tile(s, 290, 880, 380, 380, f'<circle cx="290" cy="850" r="90" fill="none" stroke="#9aa0a8" stroke-width="5" stroke-dasharray="14 10"/>'
          f'<text x="290" y="885" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="100" fill="#9aa0a8">?</text>'
          f'<text x="290" y="1030" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" fill="#9aa0a8">GUESSING</text>', "#ffffff40", 0)
s.pop(gq, ix(144) - 0.15, 0.4, 0.5, "50% 50%")
ed = tile(s, 790, 880, 380, 380, mini(690, 900, [(0, 40), (40, 20), (70, 30), (110, -10), (140, 0), (200, -60)], GOLD, 6)
          + f'<text x="790" y="1030" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" fill="{GOLD}">AN EDGE</text>', GOLD, 0)
s.pop(ed, ix(147) - 0.15, 0.4, 0.5, "50% 50%"); cue(ix(147) - 0.15, "bell_E5", -18)
s.label(540, 620, "DATA IS THE DIFFERENCE", 40, WHITE, 0, 800, 0.06); s.fade(s.items[-1].split('"')[1], ix(139), 0.4, y=10)
vs10 = s.label(540, 908, "VS", 34, LBL, 0, 800, 0.2); s.fade(vs10, ix(145), 0.3)

# 11  "A hundred journaled losses are a hundred lessons. The trader who hides from every loss has none."
s = S(ix(149) - 0.1, ix(166) - 0.1)
for k in range(100):
    x, y = 140 + (k % 10) * 40, 720 + (k // 10) * 40
    d = s.raw(f'<circle id="@ID@" cx="{x}" cy="{y}" r="12" fill="{GOLD}" style="opacity:0"/>', "d")
    tl(f'tl.fromTo("#{d}", {{opacity: 0}}, {{opacity: 0.9, duration: 0.1, immediateRender: false}}, {ix(150) + k * 0.018:.3f});')
cue(ix(150), "tick-crisp_2", -20)
hl = s.label(320, 1320, "100 LESSONS", 40, GOLD, 0, 800, 0.08); s.fade(hl, ix(155) - 0.1, 0.4, y=10)
wall = s.raw('<rect id="@ID@" x="720" y="860" width="40" height="380" fill="#3a3f48"/>', "wl")
hid = s.fig(840, 0.8, "#8a8f98", 0.85, False); s.pop(hid, ix(157) - 0.1, 0.4)
zl = s.label(830, 1320, "0 LESSONS", 40, "#9aa0a8", 0, 800, 0.08); s.fade(zl, ix(164) - 0.1, 0.4, y=10)
hd = s.label(830, 800, "HIDES FROM LOSSES", 28, LBL, 0, 700, 0.08); s.fade(hd, ix(160) - 0.1, 0.35)
cue(ix(164) - 0.1, "tock_1", -18)

# 12  "In school, a mistake cost you points. In trading, a small loss is the fee for finding out what works."
s = S(ix(166) - 0.1, ix(186) - 0.05)
c1 = tile(s, 540, 760, 860, 170, f'<text x="160" y="745" font-family="Montserrat" font-weight="800" font-size="30" letter-spacing="0.14em" fill="{LBL}">SCHOOL</text>'
          f'<text x="160" y="800" font-family="Montserrat" font-weight="800" font-size="36" fill="{RED}">MISTAKE = −POINTS</text>', "#ff4d5e80", 0)
s.pop(c1, ix(166), 0.4, 0.6, "50% 50%"); cue(ix(166), "tick_1", -20)
c2 = tile(s, 540, 1000, 860, 210, f'<text x="160" y="965" font-family="Montserrat" font-weight="800" font-size="30" letter-spacing="0.14em" fill="{GOLD}">TRADING</text>'
          f'<text x="160" y="1022" font-family="Montserrat" font-weight="800" font-size="36" fill="#fff">SMALL LOSS = THE FEE</text>'
          f'<text x="160" y="1068" font-family="Montserrat" font-weight="700" font-size="28" fill="{GOLD}">FOR FINDING OUT WHAT WORKS</text>', GOLD, 0)
s.pop(c2, ix(173), 0.4, 0.6, "50% 50%"); cue(ix(180), "bell_C5", -18)

# 13  outro (handles, no end card)
s = S(ix(186) - 0.05, TOTAL)
es = s.spot(540, 0, "232,194,106", 40, 230); s.fade(es, ix(186), 0.6)
em = s.raw('<image id="@ID@" href="assets/otm_emblem.png" x="390" y="900" width="300" height="291" style="opacity:0;filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>', "i")
s.pop(em, ix(186), 0.7, 0.6, "50% 50%"); cue(ix(186), "bell_A4", -16)
o1 = s.label(540, 1300, "ORDER THE MARKET", 32, GOLD, 0, 800, 0.3); s.fade(o1, ix(186) + 0.3, 0.5)
o2 = s.label(540, 1360, "DON'T LET THE MARKET ORDER YOU", 28, WHITE, 0, 700, 0.12); s.fade(o2, ix(189), 0.4)
o3 = s.pill(540, 1470, "FOLLOW FOR MORE", GOLD, "#111", 30); s.pop(o3, ix(195), 0.4, 0.6, "50% 50%"); cue(ix(195), "click-confirm_1", -16)
hx = 290
soc = s.raw(f'<g id="@ID@" style="opacity:0">'
            f'<rect x="{hx}" y="1548" width="36" height="36" rx="10" fill="none" stroke="#fff" stroke-width="3"/>'
            f'<circle cx="{hx + 18}" cy="1566" r="8.5" fill="none" stroke="#fff" stroke-width="3"/><circle cx="{hx + 28}" cy="1556" r="2.4" fill="#fff"/>'
            f'<text x="{hx + 48}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@fxzuez_28</text>'
            f'<path d="M {hx + 322} 1546 V 1574 A 9 9 0 1 1 {hx + 313} 1565 M {hx + 322} 1546 Q {hx + 326} 1557 {hx + 338} 1558" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>'
            f'<text x="{hx + 348}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@zuez_28</text></g>', "so")
disc = s.label(540, 1650, "EDUCATIONAL ONLY · NOT FINANCIAL ADVICE", 28, GREY, 0, 600, 0.12)
s.fade(soc, ix(189) + 0.6, 0.5, y=12)
s.fade(disc, ix(189) + 0.9, 0.5)
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
    <div id="root" data-composition-id="otm-mostlosses" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
{TIMELINE}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-mostlosses-audio" class="clip" src="assets/audio/mix_mostlosses.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-mostlosses"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
