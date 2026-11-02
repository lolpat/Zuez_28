"""OTM "Your Knowledge": a glowing-figure explainer (same system as otm-circle / otm-anyway). White soft-glow figures on a dashed ground line, spotlights, small
caps labels and simple diagrams, one scene per sentence of the narration (Quentin). Gold marks the payoff, red the
gamble. Writes ../index.html, work/cues.json (soft kit sounds) and work/timing.json."""
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

    def path(self, d, col=WHITE, w=4, fill="none", drawn=False, extra=""):
        dash = "" if drawn else 'pathLength="1" style="stroke-dasharray:1 1.2;stroke-dashoffset:1.1"'
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
def bulb(s, x, y, col=GOLD, op=0):
    return s.raw(f'<g id="@ID@" style="opacity:{op};filter:drop-shadow(0 0 16px {col})"><circle cx="{x}" cy="{y}" r="36" fill="none" stroke="{col}" stroke-width="4"/>'
                 f'<path d="M {x - 14} {y + 34} V {y + 52} H {x + 14} V {y + 34} M {x - 10} {y + 60} H {x + 10} M {x - 10} {y + 4} Q {x} {y - 14} {x + 10} {y + 4}" '
                 f'fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round"/></g>', "b")

# 1  what you know about trading is worth more than you think
s = S(0, W(11) - 0.05, first=True)
s.label(540, 560, "YOUR KNOWLEDGE", 30, LBL, 1)
s.spot(540)
s.fig(540, 1.05)
b1 = bulb(s, 540, 860, GOLD, 1)
tl(f'tl.fromTo("#{b1}", {{scale: 1}}, {{scale: 1.12, transformOrigin: "50% 50%", duration: 0.5, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}}, {W(4):.3f});')
tg = s.pill(720, 820, "WORTH: ?", GOLD, "#111", 30); s.pop(tg, W(6), 0.4, 0.5, "50% 50%"); cue(W(6), "pop_2", -18)
s.label(540, 1300, "YOU", 28, GREY, 1)

# 2  the more you learn, the less special it feels
s = S(W(11) - 0.05, W(24) - 0.05)
s.label(540, 560, "THE STRANGE THING", 30, LBL, 1)
s.path("M 170 690 V 1170 H 950", "#ffffff60", 2, drawn=True)
s.label(560, 1215, "TIME", 28, GREY, 1, 700, 0.2)
up = s.path("M 180 1140 C 400 1100 620 920 930 740", WHITE, 5); s.draw(up, W(15), 1.2)
ul = s.label(930, 712, "WHAT YOU KNOW", 28, WHITE, 0, 800, 0.08, "end"); s.fade(ul, W(16), 0.4)
dn = s.path("M 180 760 C 420 800 640 980 930 1140", GOLD, 5); s.draw(dn, W(19), 1.2)
dl = s.label(200, 725, "HOW SPECIAL IT FEELS", 28, GOLD, 0, 800, 0.08, "start"); s.fade(dl, W(19) + 0.2, 0.4)
xd = s.raw(f'<circle id="@ID@" cx="555" cy="944" r="12" fill="#fff" style="opacity:0;filter:drop-shadow(0 0 10px #fff)"/>', "c")
s.pop(xd, W(22), 0.3, 0.3, "50% 50%"); cue(W(22), "tick_2", -20)

# 3  reading a candle, placing a stop, sizing a trade
s = S(W(24) - 0.05, W(33) - 0.05)
s.label(540, 560, "WHAT YOU ALREADY KNOW", 30, LBL, 1)
y3 = s.fig(540, 0.8, "#d9dde3", 0.9); s.pop(y3, W(24), 0.4)
cards = [(230, W(24), "CANDLES"), (540, W(27), "STOPS"), (850, W(30), "SIZING")]
for k, (x, t, lab) in enumerate(cards):
    c = s.path(rrect(x - 115, 700, 230, 210, 18), WHITE, 3); s.draw(c, t, 0.45)
    if k == 0:
        ic = s.raw(f'<g id="@ID@" style="opacity:0"><line x1="{x}" y1="730" x2="{x}" y2="880" stroke="{GOLD}" stroke-width="4"/><rect x="{x - 24}" y="760" width="48" height="90" fill="{GOLD}"/></g>')
    elif k == 1:
        ic = s.raw(f'<g id="@ID@" style="opacity:0"><path d="M {x - 80} 760 L {x - 40} 790 L {x} 770 L {x + 40} 810 L {x + 80} 780" fill="none" stroke="#fff" stroke-width="4"/>'
                   f'<line x1="{x - 85}" y1="860" x2="{x + 85}" y2="860" stroke="{RED}" stroke-width="4" stroke-dasharray="10 8"/>'
                   f'<text x="{x + 85}" y="895" text-anchor="end" font-family="Montserrat" font-weight="800" font-size="28" fill="{RED}">SL</text></g>')
    else:
        ic = s.raw(f'<g id="@ID@" style="opacity:0"><text x="{x}" y="835" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="72" fill="{GOLD}">1%</text>'
                   f'<rect x="{x - 70}" y="860" width="140" height="10" rx="5" fill="#ffffff40"/><rect x="{x - 70}" y="860" width="30" height="10" rx="5" fill="{GOLD}"/></g>')
    s.pop(ic, t + 0.2, 0.4, 0.5, "50% 50%")
    lb = s.label(x, 960, lab, 28, WHITE, 0, 800, 0.12); s.fade(lb, t + 0.3, 0.35)
    cue(t + 0.2, "pop_" + str(k + 1), -20)

# 4  months to understand; now so obvious you forget anyone struggles with it
s = S(W(33) - 0.05, W(51) - 0.05)
y4 = s.fig(250, 0.9); s.pop(y4, W(33), 0.4)
pts, x = [(330, 880)], 330
r4 = random.Random(4)
while x < 760:
    x += r4.uniform(18, 40); pts.append((x + r4.uniform(-60, 60), 880 + r4.uniform(-110, 110)))
tang = s.path("M " + " L ".join(f"{a:.0f} {b:.0f}" for a, b in pts), "#ffffffc0", 3); s.draw(tang, W(33), W(38) - W(33) + 0.3, "power1.in")
m1 = s.label(540, 1060, "MONTH 1 · CONFUSING", 28, GREY, 0, 700, 0.12); s.fade(m1, W(34), 0.4)
tl(f'tl.to(["#{tang}", "#{m1}"], {{opacity: 0, duration: 0.35}}, {W(39) - 0.2:.3f});')
st = s.path("M 330 880 H 760 M 730 860 L 760 880 L 730 900", GOLD, 6); s.draw(st, W(39), 0.6)
m6 = s.label(540, 830, "MONTH 6", 30, GOLD, 0, 800, 0.15); s.fade(m6, W(40), 0.4)
ob = s.label(540, 960, "OBVIOUS", 34, WHITE, 0, 800, 0.2); s.fade(ob, W(43), 0.4, y=10); cue(W(43), "bell_E5", -20)
nb = s.fig(870, 0.8, "#9aa0a8", 0.8, False); s.pop(nb, W(45), 0.4)
nq = s.pill(870, 1000, "???", "#2a2f38", WHITE, 30); s.pop(nq, W(47), 0.35, 0.5, "50% 50%"); cue(W(47), "tick_1", -20)
s.label(870, 1300, "NEW TRADER", 28, GREY, 0); s.fade(s.items[-1].split('"')[1], W(46), 0.35)

# 5  valued by the person who doesn't have it
s = S(W(51) - 0.05, W(68) - 0.05)
s.label(540, 560, "WHO VALUES IT", 30, LBL, 1)
y5 = s.fig(250, 1.0); s.pop(y5, W(51), 0.4)
n5 = s.fig(730, 1.0, "#cfd3da", 0.9); s.pop(n5, W(61), 0.4)
s.label(250, 1300, "YOU", 28, GREY, 1)
nl = s.label(730, 1300, "NEW TRADER", 28, GREY, 0); s.fade(nl, W(61), 0.35)
for k, (bx, t, frac, lab) in enumerate([(370, W(54), 0.2, "TO YOU · 2/10"), (850, W(62), 0.9, "TO THEM · 9/10")]):
    tr = s.path(rrect(bx - 32, 900, 64, 340, 10), "#ffffff80", 3); s.draw(tr, t - 0.3, 0.4)
    h = 336 * frac
    fl = s.raw(f'<rect id="@ID@" x="{bx - 30}" y="{1238 - h:.0f}" width="60" height="{h:.0f}" rx="8" fill="{GOLD if k else "#8a8f98"}" style="opacity:0"/>', "r")
    tl(f'tl.fromTo("#{fl}", {{opacity: 1, scaleY: 0, transformOrigin: "50% 100%"}}, {{opacity: 1, scaleY: 1, duration: 0.8, ease: "power2.out", immediateRender: false}}, {t:.3f});')
    lb = s.label(bx, 870, lab, 28, GOLD if k else WHITE, 0, 800, 0.08); s.fade(lb, t + 0.3, 0.35)
    cue(t, "swell_1" if k else "tick_3", -22)

# 6  the mistake you fixed; a new trader blowing account after account
s = S(W(68) - 0.05, W(88) - 0.05)
s.label(540, 560, "THE SAME MISTAKE", 30, LBL, 1)
y6 = s.fig(200, 0.95); s.pop(y6, W(68), 0.4)
fx = s.pill(200, 960, "MOVING STOPS", "#2a2f38", WHITE, 28); s.pop(fx, W(69), 0.35, 0.5, "50% 50%")
fs = s.path("M 70 960 H 330", GOLD, 5); s.draw(fs, W(72), 0.3)
fc = s.raw(f'<g id="@ID@" style="opacity:0"><circle cx="330" cy="905" r="22" fill="{GOLD}"/><path d="M 320 905 L 328 913 L 341 897" fill="none" stroke="#111" stroke-width="5" stroke-linecap="round"/></g>', "ck")
s.pop(fc, W(72) + 0.2, 0.35, 0.3, "50% 50%"); cue(W(72), "bell_C5", -20)
n6 = s.fig(780, 0.95, "#cfd3da", 0.9); s.pop(n6, W(77), 0.4)
mp = s.pill(780, 960, "MOVING STOPS", WHITE, "#111", 28); s.pop(mp, W(75), 0.35, 0.5, "50% 50%")
for k in range(3):
    x = 610 + k * 170
    cd = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="{x - 70}" y="700" width="140" height="110" rx="12" fill="none" stroke="#fff" stroke-width="3"/>'
               f'<text x="{x}" y="745" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="28" fill="#c9ced6">ACC {k + 1}</text>'
               f'<text x="{x}" y="790" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" fill="#fff">$1,000</text></g>', "cd")
    s.fade(cd, W(79) + k * 0.12, 0.3)
    bl = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="{x - 70}" y="700" width="140" height="110" rx="12" fill="{RED}"/>'
               f'<text x="{x}" y="768" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" fill="#fff">BLOWN</text></g>', "bl")
    tb = W(84) + k * 0.4
    tl(f'tl.fromTo("#{bl}", {{opacity: 0, scale: 1.3, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.25, ease: "power3.out", immediateRender: false}}, {tb:.3f});')
    cue(tb, "land-light_1", -16)

# 7  simple to you; to them it saves a year and a lot of money
s = S(W(88) - 0.05, W(106) - 0.05)
s.label(540, 560, "TO YOU · TO THEM", 30, LBL, 1)
s7 = s.fig(140, 0.75, "#cfd3da", 0.9); s.pop(s7, W(88), 0.4)
for y in (820, 1090):
    s.raw(f'<g id="@ID@"><circle cx="920" cy="{y}" r="20" fill="none" stroke="{GOLD}" stroke-width="3"/><circle cx="920" cy="{y}" r="7" fill="{GOLD}"/></g>')
sl = s.path("M 200 1090 H 895", GOLD, 6); s.draw(sl, W(90), 0.7)
sll = s.label(540, 1150, "WITH YOUR ANSWER · 6 WEEKS", 28, GOLD, 0, 800, 0.08); s.fade(sll, W(92), 0.4)
d, x = "M 200 820", 200
for k in range(6):
    d += f" C {x + 40} 700, {x + 110} 700, {x + 90} 820 S {x + 60} 940, {x + 115} 820"; x += 115
d += " L 895 820"
lp = s.path(d, "#ffffffb0", 3); s.draw(lp, W(94), W(100) - W(94) + 0.4, "power1.inOut")
lpl = s.label(540, 650, "ALONE · 1 YEAR", 28, WHITE, 0, 800, 0.08); s.fade(lpl, W(95), 0.4)
sv = s.pill(540, 970, "1 YEAR SAVED", GOLD, "#111", 30); s.pop(sv, W(99), 0.4, 0.5, "50% 50%"); cue(W(99), "bell_G5", -18)
mn = s.pill(540, 970, "+ NO BLOWN ACCOUNTS", WHITE, "#111", 28)
tl(f'tl.to("#{sv}", {{opacity: 0, duration: 0.25}}, {W(101) - 0.3:.3f});')
s.pop(mn, W(101), 0.35, 0.5, "50% 50%"); cue(W(101), "pop_3", -20)

# 8  traders pay for mentorship even when the information is free online
s = S(W(106) - 0.05, W(119) - 0.05)
s.label(540, 560, "WHY TRADERS PAY", 30, LBL, 1)
pc = s.path(rrect(580, 700, 340, 300, 22), WHITE, 3); s.draw(pc, W(106), 0.5)
p1 = s.label(750, 800, "$99", 64, GOLD, 0, 800, 0.02); s.fade(p1, W(109), 0.35, y=10); cue(W(109), "click_1", -20)
p2 = s.label(750, 860, "MENTORSHIP", 28, WHITE, 0, 800, 0.12); s.fade(p2, W(111) - 0.2, 0.35)
p3 = s.label(750, 940, "DONE WITH YOU", 28, GREY, 0, 700, 0.1); s.fade(p3, W(111), 0.35)
fc8 = s.path(rrect(160, 700, 340, 300, 22), "#ffffff90", 3); s.draw(fc8, W(112), 0.5)
f1 = s.label(330, 790, "FREE", 40, WHITE, 0, 800, 0.15); s.fade(f1, W(117), 0.35)
f2 = s.label(330, 860, "1,240,000 RESULTS", 28, LBL, 0, 700, 0.04); s.fade(f2, W(115), 0.35)
f3 = s.label(330, 940, "DO IT ALONE", 28, GREY, 0, 700, 0.1); s.fade(f3, W(116), 0.35)
s8 = s.fig(540, 0.75, "#cfd3da", 0.9); s.pop(s8, W(106), 0.4)
cur = s.raw('<path id="@ID@" d="M 300 1030 l 0 52 l 14 -14 l 10 24 l 10 -5 l -10 -23 l 20 0 z" fill="#fff" style="opacity:0"/>', "p")
s.fade(cur, W(117), 0.25)
tl(f'tl.to("#{cur}", {{x: 420, y: -60, duration: 0.6, ease: "power2.inOut"}}, {W(117) + 0.2:.3f});')
gl = s.path(rrect(580, 700, 340, 300, 22), GOLD, 6); s.draw(gl, W(118) + 0.1, 0.35); cue(W(118) + 0.1, "click-confirm_1", -16)

# 9  not buying information, buying the shortcut: someone who has been where they are
s = S(W(119) - 0.05, W(137) - 0.05)
bk = s.raw(f'<g id="@ID@" style="opacity:0"><path d="M 540 760 C 490 730 420 730 380 745 V 905 C 420 890 490 890 540 920 C 590 890 660 890 700 905 V 745 C 660 730 590 730 540 760 Z M 540 760 V 920" '
           f'fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/></g>', "bk")
s.pop(bk, W(119), 0.4, 0.6, "50% 50%")
il = s.label(540, 980, "INFORMATION", 28, WHITE, 0, 800, 0.15); s.fade(il, W(121), 0.35)
ix = s.path("M 360 960 L 720 720", GOLD, 6); s.draw(ix, W(122), 0.3); cue(W(122), "whoosh-short_1", -20)
tl(f'tl.to(["#{bk}", "#{il}", "#{ix}"], {{opacity: 0.25, duration: 0.4}}, {W(124) - 0.2:.3f});')
nt = s.fig(170, 0.8, "#cfd3da", 0.9); s.pop(nt, W(124), 0.4)
d9, x = "M 230 1180", 230
for k in range(5):
    d9 += f" Q {x + 60} {1060 if k % 2 else 1300}, {x + 120} 1180"; x += 120
wd = s.path(d9, "#ffffff50", 3); s.draw(wd, W(124), 0.8)
sc9 = s.path("M 230 1150 H 800 M 772 1130 L 800 1150 L 772 1170", GOLD, 6); s.draw(sc9, W(127), 0.6)
scl = s.label(515, 1110, "SHORTCUT", 30, GOLD, 0, 800, 0.2); s.fade(scl, W(128), 0.35); cue(W(128), "bell_A4", -20)
gd = s.fig(890, 0.95); s.pop(gd, W(129), 0.4)
gs = s.spot(890, 0, "232,194,106", 30, 110); s.fade(gs, W(129), 0.5)
bt = s.label(890, 1300, "BEEN THERE", 28, GOLD, 0, 800); s.fade(bt, W(132), 0.35)

# 10  not everything you know is worth selling
s = S(W(137) - 0.05, W(144) - 0.05)
pn = s.path(rrect(170, 660, 740, 420, 24), WHITE, 3); s.draw(pn, W(137), 0.5)
s.label(220, 720, "DEMAND", 28, LBL, 1, 800, 0.2, "start")
rows = [("RISK PLAN", 0.9), ("PRICE ACTION", 0.8), ("MAGIC INDICATOR", 0.12), ("LUCKY TRADES", 0.02)]
for k, (lab, v) in enumerate(rows):
    y = 790 + k * 75
    lb = s.label(220, y + 10, lab, 28, WHITE if v > 0.5 else GREY, 0, 700, 0.06, "start"); s.fade(lb, W(138) + k * 0.25, 0.3)
    s.raw(f'<rect id="@ID@" x="590" y="{y - 10}" width="280" height="16" rx="8" fill="#ffffff20"/>')
    br = s.raw(f'<rect id="@ID@" x="590" y="{y - 10}" width="{max(6, 280 * v):.0f}" height="16" rx="8" fill="{GOLD if v > 0.5 else "#8a8f98"}" style="opacity:0"/>', "r")
    tl(f'tl.fromTo("#{br}", {{opacity: 1, scaleX: 0, transformOrigin: "0% 50%"}}, {{opacity: 1, scaleX: 1, duration: 0.6, ease: "power2.out", immediateRender: false}}, {W(138) + k * 0.25 + 0.1:.3f});')
    cue(W(138) + k * 0.25 + 0.1, "tick-crisp_" + str(k % 3 + 1), -22)
y10 = s.fig(540, 0.75); s.pop(y10, W(137), 0.4)

# 11  the lesson you stopped thinking was special is what someone else is looking for
s = S(W(144) - 0.05, W(161) - 0.05)
s.label(540, 560, "SOMEONE IS LOOKING FOR IT", 30, LBL, 1)
y11 = s.fig(190, 1.0); s.pop(y11, W(144), 0.4)
b11 = bulb(s, 190, 900, GOLD, 0); s.pop(b11, W(146), 0.45, 0.5, "50% 50%"); cue(W(146), "swell_2", -20)
for k, x in enumerate([470, 620, 770, 920]):
    f = s.fig(x, 0.72, "#9aa0a8", 0.8, False); s.pop(f, W(152) + k * 0.08, 0.4)
    q = s.pill(x, 1000, "?", "#2a2f38", WHITE, 30); s.pop(q, W(153) + k * 0.1, 0.3, 0.5, "50% 50%")
    ln = s.path(f"M 226 900 Q {(226 + x) / 2:.0f} 800, {x} 960", "#e8c26a90", 2); s.draw(ln, W(156) + k * 0.22, 0.4)
    lit = s.fig(x, 0.72, WHITE, 0); s.fade(lit, W(156) + k * 0.22 + 0.35, 0.3)
    gq = s.pill(x, 1000, "✓", GOLD, "#111", 30)
    tl(f'tl.set("#{q}", {{opacity: 0}}, {W(156) + k * 0.22 + 0.35:.3f});')
    s.pop(gq, W(156) + k * 0.22 + 0.35, 0.3, 0.5, "50% 50%")
    cue(W(156) + k * 0.22 + 0.35, "pop_" + str(k + 1), -20)

# 12  order the market (outro with handles; no end card)
s = S(W(161) - 0.05, TOTAL)
es = s.spot(540, 0, "232,194,106", 40, 230); s.fade(es, W(161), 0.6)
em = s.raw('<image id="@ID@" href="assets/otm_emblem.png" x="390" y="900" width="300" height="291" style="opacity:0;filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>', "i")
s.pop(em, W(161), 0.7, 0.6, "50% 50%"); cue(W(161), "bell_A4", -16)
o1 = s.label(540, 1300, "ORDER THE MARKET", 32, GOLD, 0, 800, 0.3); s.fade(o1, W(161) + 0.3, 0.5)
o2 = s.label(540, 1360, "DON'T LET THE MARKET ORDER YOU", 28, WHITE, 0, 700, 0.12); s.fade(o2, W(164), 0.4)
o3 = s.pill(540, 1470, "FOLLOW FOR MORE", GOLD, "#111", 30); s.pop(o3, W(170), 0.4, 0.6, "50% 50%"); cue(W(170), "click-confirm_1", -16)
hx = 290
soc = s.raw(f'<g id="@ID@" style="opacity:0">'
            f'<rect x="{hx}" y="1548" width="36" height="36" rx="10" fill="none" stroke="#fff" stroke-width="3"/>'
            f'<circle cx="{hx + 18}" cy="1566" r="8.5" fill="none" stroke="#fff" stroke-width="3"/><circle cx="{hx + 28}" cy="1556" r="2.4" fill="#fff"/>'
            f'<text x="{hx + 48}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@fxzuez_28</text>'
            f'<path d="M {hx + 322} 1546 V 1574 A 9 9 0 1 1 {hx + 313} 1565 M {hx + 322} 1546 Q {hx + 326} 1557 {hx + 338} 1558" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>'
            f'<text x="{hx + 348}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@zuez_28</text></g>', "so")
disc = s.label(540, 1650, "EDUCATIONAL ONLY · NOT FINANCIAL ADVICE", 28, GREY, 0, 600, 0.12)
s.fade(soc, W(166), 0.5, y=12)
s.fade(disc, W(166) + 0.3, 0.5)

# ------------------------------------------------------------------ end card, dust, ground, emblem
tl(f'tl.to("#mark", {{opacity: 0, duration: 0.3}}, {W(161) - 0.2:.3f});')
dust = ""
for k in range(40):
    x, y, r, op = rnd.uniform(0, 1080), rnd.uniform(0, 1920), rnd.uniform(1.2, 3.2), rnd.uniform(0.05, 0.22)
    dust += f'<circle id="d{k}" cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#fff" opacity="{op:.2f}"/>'
    tl(f'tl.fromTo("#d{k}", {{x: 0, y: 0}}, {{x: {rnd.uniform(-70, 70):.0f}, y: {-rnd.uniform(150, 480):.0f}, duration: {TOTAL}, ease: "none"}}, 0);')

CREDIT = 'music: “Song for Tony” by geoffpeters · CC BY 3.0'
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
    <div id="root" data-composition-id="otm-know" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-know-audio" class="clip" src="assets/audio/mix_know.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-know"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
