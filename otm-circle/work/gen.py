"""OTM "Your Circle": a glowing-figure explainer. White soft-glow figures on a dashed ground line, spotlights, small
caps labels and simple diagrams, one scene per sentence of the narration (Quentin). Gold marks the payoff, red the
gamble. Writes ../index.html, work/cues.json (soft kit sounds) and work/timing.json."""
import json, math, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAD = 0.3
GOLD, RED, WHITE, GREY, LBL = "#e8c26a", "#ff4d5e", "#ffffff", "#7d838c", "#c9ced6"
GY = 1240                                   # ground line
words = json.load(open(f"{ROOT}/work/words_take1.json"))
def W(i): return round(words[i]["start"] + LEAD, 3)
def WE(i): return round(words[i]["end"] + LEAD, 3)
END_T = round(words[-1]["end"] + LEAD + 0.6, 2)
TOTAL = round(END_T + 3.8, 2)
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
# 1  three disciplined traders ... you become the fourth
s = S(0, W(10) - 0.05, first=True)
s.label(540, 560, "DISCIPLINED TRADERS", 30, LBL, 1)
xs = [210, 420, 630]
for k, x in enumerate(xs):
    s.spot(x)
    s.fig(x)
    c = s.path(mini_curve(x - 55, 900), GOLD, 4)
    s.draw(c, W(3) + k * 0.15, 0.7)
    s.label(x, 1300, ["RISK 1%", "RULES", "JOURNAL"][k], 28, GREY, 0)
    s.fade(s.items and s.items[-1].split('"')[1], W(4) + k * 0.12, 0.4)
dim = s.fig(1010, op=0.35, col=GREY, glow=False)
s.walk(dim, W(5) - 0.2, -140, 1.0)
sp4 = s.spot(870, 0, col="232,194,106")
s.fade(sp4, W(9) - 0.05, 0.35)
you = s.fig(1010, op=0)
tl(f'tl.set("#{you}", {{x: -140}}, 0);')
s.fade(you, W(9), 0.4)
yl = s.label(870, 900, "YOU", 30, GOLD, 0, 800)
s.fade(yl, W(9) + 0.1, 0.4, y=12)
cue(W(9), "bell_E5", -18)

# 2-3  the people around you decide what's normal; when they call it gambling, you gamble
s = S(W(10) - 0.05, W(28) - 0.05)
t1 = s.label(540, 560, "THE PEOPLE AROUND YOU", 30, LBL, 0); s.fade(t1, W(10), 0.4)
row = [180, 360, 540, 720, 900]
figs = []
for k, x in enumerate(row):
    if k == 2:
        figs.append(s.fig(x, col=WHITE))
    else:
        figs.append(s.fig(x, col="#d9dde3", op=0.9))
    s.pop(figs[-1], W(10) + 0.05 + abs(k - 2) * 0.12, 0.45)
    cue(W(10) + 0.05 + abs(k - 2) * 0.12, "pop_" + str(k % 4 + 1), -24)
ring = s.path("M 90 1240 A 450 58 0 1 0 990 1240 A 450 58 0 1 0 90 1240", "#ffffff90", 2, extra='')
s.draw(ring, W(12), 0.9)
cl = s.label(540, 1330, "YOUR CIRCLE", 28, GREY, 0); s.fade(cl, W(12) + 0.4, 0.4)
nm = s.label(540, 650, "DECIDES WHAT FEELS NORMAL", 28, WHITE, 0, 800); s.fade(nm, W(14), 0.4, y=10)
tl(f'tl.to("#{nm}", {{opacity: 0, duration: 0.25}}, {W(18) - 0.3:.3f});')
tl(f'tl.to("#{t1}", {{opacity: 0, duration: 0.25}}, {W(18) - 0.3:.3f});')
t2 = s.label(540, 560, "WHAT THEY SAY", 30, LBL, 0); s.fade(t2, W(18), 0.4)
for k, (txt, x, y) in enumerate([("IT'S GAMBLING", 230, 900), ("JUST SEND IT", 410, 790), ("NO STOP NEEDED", 680, 900), ("ALL IN", 880, 790)]):
    p = s.pill(x, y, txt); s.pop(p, W(21) + k * 0.22, 0.35, 0.6, "50% 50%"); cue(W(21) + k * 0.22, "tick_" + str(k % 3 + 1), -20)
redyou = s.fig(540, col=RED, op=0)
s.fade(redyou, W(25), 0.5)
rp = s.pill(540, 700, "YOU: ALL IN", RED, WHITE); s.pop(rp, W(25), 0.4, 0.6, "50% 50%"); cue(W(25), "land-light_1", -16)

# 4  the group chat chases every pump; you chase it too
s = S(W(28) - 0.05, W(39) - 0.05)
s.label(540, 560, "THE GROUP CHAT", 30, LBL, 1)
ph = s.path(rrect(120, 640, 360, 560, 40), WHITE, 4); s.draw(ph, W(28), 0.6)
for k, txt in enumerate(["BUY NOW!!", "IT'S PUMPING", "DON'T MISS IT", "LAST CHANCE"]):
    y = 720 + k * 110; x = 300 + (35 if k % 2 else -35)
    b = s.pill(x, y, txt, "#1e2a3a", WHITE, 28)
    s.pop(b, W(31) + k * 0.25, 0.35, 0.6, "50% 50%"); cue(W(31) + k * 0.25, "pop_" + str(k + 1), -20)
runner = s.fig(600, 0.85)
arrow = s.path("M 680 1120 L 760 1060 L 820 1080 L 900 960 L 960 900", GOLD, 6)
s.draw(arrow, W(33), 1.0)
s.walk(runner, W(35) - 0.1, 240, 1.0)
crash = s.path("M 960 900 L 1000 1000 L 1030 1180", RED, 6)
s.draw(crash, W(37), 0.45); cue(W(37), "whoosh-short_1", -18)
cz = s.label(840, 1300, "BOUGHT THE TOP", 28, RED, 0); s.fade(cz, W(37), 0.3)

# 5  spend time with traders who are already consistent
s = S(W(39) - 0.05, W(51) - 0.05)
s.label(540, 560, "ALREADY CONSISTENT", 30, LBL, 1)
for k, x in enumerate([370, 570, 770]):
    f = s.fig(x, 0.9, gy=1170); s.pop(f, W(40) + k * 0.15, 0.4)
    lap = s.path(f"M {x - 50} 1105 L {x - 38} 1070 L {x + 38} 1070 L {x + 50} 1105 Z", "#ffffffb0", 3, fill="#0b0f15"); s.draw(lap, W(41) + k * 0.15, 0.4)
    ck = s.add(f'<g id="@ID@" style="opacity:0"><circle cx="{x}" cy="770" r="30" fill="none" stroke="{GOLD}" stroke-width="3"/>'
               f'<path d="M {x - 13} 770 L {x - 3} 781 L {x + 15} 759" fill="none" stroke="{GOLD}" stroke-width="5" stroke-linecap="round"/></g>', "ck")
    s.pop(ck, W(47) + k * 0.18, 0.35, 0.3, "50% 50%"); cue(W(47) + k * 0.18, "bell_" + ["G4", "C5", "E5"][k], -24)
desk = s.path(rrect(250, 1110, 640, 130, 10), WHITE, 3, fill="#05070a"); s.draw(desk, W(39), 0.7)
me = s.fig(-80, 0.95)
s.walk(me, W(40), 230, 1.3)
glowr = s.raw(f'<ellipse id="@ID@" cx="150" cy="{GY}" rx="90" ry="20" fill="none" stroke="{GOLD}" stroke-width="3" style="opacity:0"/>', "c")
tl(f'tl.fromTo("#{glowr}", {{opacity: 1, scale: 0.6, transformOrigin: "50% 50%"}}, {{opacity: 0, scale: 2.2, duration: 0.9, ease: "power2.out", immediateRender: false}}, {W(50):.3f});')
cue(W(50), "swell_1", -22)

# 6  a stop you never move, a week with no trades, a red day with no revenge
s = S(W(51) - 0.05, W(68) - 0.05)
s.label(540, 560, "WHAT BECOMES NORMAL", 30, LBL, 1)
starts = [(W(51), WE(56)), (W(57), WE(61)), (W(62), WE(67))]
for k, (x, lab) in enumerate([(230, "STOP STAYS"), (540, "0 TRADES"), (850, "NO REVENGE")]):
    ta, tb = starts[k]
    c = s.path(f"M {x - 95} 830 a 95 95 0 1 0 190 0 a 95 95 0 1 0 -190 0", WHITE, 3); s.draw(c, ta, 0.5)
    if k == 0:
        ic = s.path(f"M {x - 55} 860 L {x - 25} 820 L {x + 5} 840 L {x + 50} 790 M {x - 60} 880 H {x + 60}", WHITE, 4); s.draw(ic, ta + 0.2, 0.5)
        lk = s.path(f"M {x + 30} 880 v -12 a 12 12 0 0 1 24 0 v 12 h 6 v 22 h -36 v -22 z", GOLD, 3); s.draw(lk, ta + 0.6, 0.4)
    elif k == 1:
        g = "".join(f'<rect x="{x - 60 + i * 25}" y="{800 + j * 25}" width="18" height="18" rx="3" fill="none" stroke="#fff" stroke-width="2"/>' for i in range(5) for j in range(2))
        gi = s.raw(f'<g id="@ID@" style="opacity:0">{g}</g>'); s.fade(gi, ta + 0.2, 0.4)
    else:
        rc = s.raw(f'<g id="@ID@" style="opacity:0"><line x1="{x}" y1="780" x2="{x}" y2="890" stroke="{RED}" stroke-width="4"/><rect x="{x - 16}" y="795" width="32" height="70" fill="{RED}"/></g>')
        s.fade(rc, ta + 0.2, 0.35)
        no = s.path(f"M {x - 45} 830 a 45 45 0 1 0 90 0 a 45 45 0 1 0 -90 0 M {x - 32} 862 L {x + 32} 798", WHITE, 4); s.draw(no, ta + 0.7, 0.4)
    lb = s.label(x, 975, lab, 28, WHITE, 0, 800); s.fade(lb, ta + 0.3, 0.35)
    ck = s.add(f'<g id="@ID@" style="opacity:0"><circle cx="{x + 70}" cy="760" r="24" fill="{GOLD}"/>'
               f'<path d="M {x + 59} 760 L {x + 67} 769 L {x + 82} 751" fill="none" stroke="#111" stroke-width="5" stroke-linecap="round"/></g>', "ck")
    s.pop(ck, tb - 0.1, 0.35, 0.3, "50% 50%"); cue(tb - 0.1, "pop_" + str(k + 1), -18)
youd = s.fig(540, 1.0, GREY, 0.45, False)
youb = s.fig(540, 1.0, WHITE, 0)
for k, (ta, tb) in enumerate(starts):
    tl(f'tl.to("#{youb}", {{opacity: {(k + 1) / 3:.2f}, duration: 0.5}}, {tb - 0.1:.3f});')

# 7  impossible starts to feel normal
s = S(W(68) - 0.05, W(76) - 0.05)
wall = s.raw(f'<g id="@ID@"><rect x="600" y="560" width="140" height="680" fill="#11151b" stroke="#fff" stroke-width="3"/>'
             f'<text class="wl" x="670" y="900" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" letter-spacing="0.2em" fill="#fff" '
             f'transform="rotate(-90 670 900)">IMPOSSIBLE</text></g>', "w")
tl(f'tl.fromTo("#{wall}", {{scaleY: 0, transformOrigin: "50% 100%"}}, {{scaleY: 1, duration: 0.5, ease: "power3.out", immediateRender: false}}, {W(68):.3f});')
cue(W(68), "land_1", -18)
tl(f'tl.to("#{wall} .wl", {{opacity: 0, duration: 0.3}}, {W(72):.3f});')
tl(f'tl.to("#{wall}", {{scaleY: 0.1, transformOrigin: "50% 100%", duration: 0.8, ease: "power2.inOut"}}, {W(72):.3f});')
stepl = s.label(670, 1300, "NORMAL", 30, GOLD, 0, 800); s.fade(stepl, W(74), 0.4)
w7 = s.fig(380); s.pop(w7, W(68) + 0.1, 0.4)
s.walk(w7, W(73) - 0.1, 470, 1.0)
cue(W(72), "whoosh-long_1", -22)

# 8  not because their results rub off on you
s = S(W(76) - 0.05, W(84) - 0.05)
th = s.fig(330, 1.0); s.pop(th, W(76), 0.4)
tg = s.label(330, 860, "+$84,210", 40, GOLD, 0, 800, 0.02); s.fade(tg, W(76) + 0.2, 0.4, y=10)
yo = s.fig(750, 1.0, "#d9dde3", 0.9); s.pop(yo, W(76) + 0.15, 0.4)
s.label(330, 1300, "THEIR RESULTS", 28, GREY, 1)
s.label(750, 1300, "YOU", 28, GREY, 1)
ar = s.path("M 420 1000 C 500 930 580 930 660 1000", "#ffffffa0", 3, extra=''); s.draw(ar, W(78), 0.6)
rp8 = s.pill(420, 960, "RESULTS", GOLD, "#111", 28)
tl(f'tl.fromTo("#{rp8}", {{opacity: 0, x: 0}}, {{opacity: 1, x: 150, duration: 0.6, ease: "power2.out", immediateRender: false}}, {W(79):.3f});')
tl(f'tl.to("#{rp8}", {{x: 60, y: 60, rotation: -20, opacity: 0, duration: 0.6, ease: "power2.in"}}, {max(W(81), W(79) + 0.62):.3f});')
xx = s.path("M 510 920 L 570 980 M 570 920 L 510 980", RED, 6); s.draw(xx, W(81) + 0.2, 0.3); cue(W(81) + 0.2, "click_1", -18)

# 9  you see how they think: wait, size, take the loss, move on
s = S(W(84) - 0.05, W(105) - 0.05)
s.label(540, 560, "HOW THEY THINK", 30, LBL, 1)
tf = s.fig(190, 0.95); s.pop(tf, W(84), 0.4)
dl = s.path("M 250 1000 L 420 760", "#ffffff70", 2, extra=''); s.draw(dl, W(88), 0.4)
boxes = [("SETUP?", 700, W(89)), ("WAIT", 820, W(91)), ("SIZE 1%", 940, W(94)), ("TAKE THE LOSS", 1060, W(97)), ("MOVE ON", 1180, W(103))]
prev = None
for k, (txt, y, t) in enumerate(boxes):
    col = GOLD if k == 4 else WHITE
    bw = len(txt) * 20 + 70
    b = s.path(rrect(620 - bw / 2, y - 38, bw, 76, 38 if k else 10), col, 3); s.draw(b, t, 0.45)
    lb = s.label(620, y + 10, txt, 28, col, 0, 800, 0.1); s.fade(lb, t + 0.15, 0.3)
    if prev is not None:
        ln = s.path(f"M 620 {prev + 40} L 620 {y - 40}", "#ffffff90", 3); s.draw(ln, t - 0.2, 0.25)
    prev = y
    cue(t, "tick-crisp_" + str(k % 3 + 1), -20)

# 10  you start spotting setups you used to ignore
s = S(W(105) - 0.05, W(113) - 0.05)
s.label(600, 560, "WHAT YOU NOTICE", 30, LBL, 1)
rf = s.fig(170, 0.9); s.pop(rf, W(105), 0.4)
RX, RY, RR = 640, 930, 230
rad = s.path(f"M {RX - RR} {RY} a {RR} {RR} 0 1 0 {2 * RR} 0 a {RR} {RR} 0 1 0 {-2 * RR} 0", WHITE, 3); s.draw(rad, W(105), 0.6)
s.raw(f'<g id="@ID@" opacity="0.35"><circle cx="{RX}" cy="{RY}" r="{RR * 0.55}" fill="none" stroke="#fff" stroke-width="2"/>'
      f'<line x1="{RX - RR}" y1="{RY}" x2="{RX + RR}" y2="{RY}" stroke="#fff" stroke-width="2"/><line x1="{RX}" y1="{RY - RR}" x2="{RX}" y2="{RY + RR}" stroke="#fff" stroke-width="2"/></g>')
sw = s.raw(f'<line id="@ID@" x1="{RX}" y1="{RY}" x2="{RX}" y2="{RY - RR}" stroke="#fff" stroke-width="4" stroke-linecap="round" style="filter:drop-shadow(0 0 8px #fff)"/>', "l")
dur10 = W(113) - W(105)
tl(f'tl.fromTo("#{sw}", {{rotation: 0}}, {{rotation: 540, svgOrigin: "{RX} {RY}", duration: {dur10:.3f}, ease: "none", immediateRender: false}}, {W(105):.3f});')
link = s.path(f"M 230 1080 L {RX - RR + 20} {RY + 60}", "#ffffff60", 2, extra=''); s.draw(link, W(106), 0.4)
dots = [("A+ SETUP", 40, 0.7), ("KEY LEVEL", 130, 0.5), ("LIQUIDITY", 220, 0.75), ("BREAK OF STRUCTURE", 300, 0.45)]
cnt = []
for k, (txt, ang, rr) in enumerate(dots):
    a = math.radians(ang); x = RX + math.sin(a) * RR * rr; y = RY - math.cos(a) * RR * rr
    tk = W(105) + dur10 * (ang / 540) + 0.05
    d = s.raw(f'<circle id="@ID@" cx="{x:.0f}" cy="{y:.0f}" r="11" fill="#fff" style="opacity:0;filter:drop-shadow(0 0 10px #fff)"/>', "c")
    s.pop(d, tk, 0.3, 0.2, "50% 50%")
    lab = s.label(x, y - 24, txt, 28, WHITE, 0, 700, 0.08); s.fade(lab, tk + 0.05, 0.3)
    cue(tk, "click_" + str(k % 2 + 1), -20)
    cnt.append(tk)
s.label(980, 760, "SPOTTED", 28, GREY, 1, 700, 0.12)
for k in range(5):
    n = s.label(980, 830, str(k), 56, GOLD, 1 if k == 0 else 0, 800, 0)
    if k > 0: tl(f'tl.set("#{n}", {{opacity: 1}}, {cnt[k - 1]:.3f});')
    if k < 4: tl(f'tl.set("#{n}", {{opacity: 0}}, {cnt[k] if k < 4 else 0:.3f});')

# 11  and questioning habits you never noticed
s = S(W(113) - 0.05, W(119) - 0.05)
s.label(540, 560, "OLD HABITS", 30, LBL, 1)
hf = s.fig(190, 0.95); s.pop(hf, W(113), 0.4)
for k, txt in enumerate(["MOVING STOPS", "OVERTRADING", "REVENGE TRADES", "NO JOURNAL"]):
    y = 760 + k * 120
    p = s.pill(640, y, txt + "  ?", "#1e2a3a", WHITE, 30); s.pop(p, W(114) + k * 0.18, 0.35, 0.6, "50% 50%")
    st = s.path(f"M {640 - len(txt) * 13 - 50} {y} H {640 + len(txt) * 13 + 50}", GOLD, 5); s.draw(st, W(117) + k * 0.15, 0.25)
    tl(f'tl.to("#{p}", {{opacity: 0.4, duration: 0.3}}, {W(117) + k * 0.15 + 0.2:.3f});')
    cue(W(117) + k * 0.15, "whoosh-short_" + str(k % 3 + 1), -24)

# 12  on the internet, discipline looks like another world
s = S(W(119) - 0.05, W(127) - 0.05, ground=False, restore=False)
ph = s.path(rrect(330, 520, 420, 820, 48), WHITE, 4); s.draw(ph, W(119), 0.6)
s.label(540, 600, "ONLINE", 28, GREY, 1)
isl = s.raw(f'<g id="@ID@" style="opacity:0"><path d="M 400 1010 L 680 1010 L 540 1180 Z" fill="none" stroke="#fff" stroke-width="3"/>'
            f'<path d="M 430 1050 H 650 M 455 1085 H 625" stroke="#ffffff60" stroke-width="2" stroke-dasharray="8 8"/></g>')
s.fade(isl, W(121), 0.5)
inf = s.fig(490, 0.6, gy=1010); s.pop(inf, W(121) + 0.2, 0.4)
mc = s.path(mini_curve(550, 900, 100, 90), GOLD, 4); s.draw(mc, W(122), 0.6)
big = s.label(540, 760, "$84,210", 56, WHITE, 0, 800, 0.02); s.fade(big, W(122), 0.4, y=12)
lk = s.label(540, 1270, "♥ 133K LIKES", 28, LBL, 0, 700, 0.06); s.fade(lk, W(124), 0.4)
aw = s.label(540, 1440, "ANOTHER WORLD", 30, GOLD, 0, 800); s.fade(aw, W(125), 0.4)
cue(W(124), "pop_2", -20)

# 13  in your room, every day: the distance disappears
s = S(W(127) - 0.05, W(138) - 0.05, ground=False, hide=False)
s.label(540, 560, "YOUR ROOM", 30, LBL, 1)
il = s.raw(f'<g id="@ID@"><path d="M 60 1000 L 360 1000 L 210 1170 Z" fill="none" stroke="#fff" stroke-width="3"/>'
           f'<path d="M 90 1040 H 330 M 120 1075 H 300" stroke="#ffffff60" stroke-width="2" stroke-dasharray="8 8"/></g>', "il")
ir = s.raw(f'<g id="@ID@"><path d="M 720 1000 L 1020 1000 L 870 1170 Z" fill="none" stroke="#fff" stroke-width="3"/>'
           f'<path d="M 750 1040 H 990 M 780 1075 H 960" stroke="#ffffff60" stroke-width="2" stroke-dasharray="8 8"/></g>', "il")
fl = s.fig(210, 0.7, gy=1000); fr = s.fig(870, 0.7, gy=1000)
crv = s.path(mini_curve(900, 820, 90, 60), GOLD, 4); s.draw(crv, W(127) + 0.2, 0.5)
for i in (il, fl): tl(f'tl.fromTo("#{i}", {{x: -60}}, {{x: 0, duration: 0.3, ease: "power2.out", immediateRender: false}}, {W(127) - 0.05:.3f});')
move = W(132) - W(129)
for i in (il, fl): tl(f'tl.to("#{i}", {{x: 160, duration: {move:.3f}, ease: "power2.inOut"}}, {W(129):.3f});')
for i in (ir, fr, crv): tl(f'tl.to("#{i}", {{x: -160, duration: {move:.3f}, ease: "power2.inOut"}}, {W(129):.3f});')
kms = ["9,800 KM", "6,400 KM", "3,100 KM", "900 KM", "0 KM"]
for k, km in enumerate(kms):
    n = s.label(540, 1320, km, 44, GOLD if k == 4 else WHITE, 1 if k == 0 else 0, 800, 0.04)
    ta = W(129) + move * k / 4
    if k > 0: tl(f'tl.set("#{n}", {{opacity: 1}}, {ta:.3f});')
    if k < 4: tl(f'tl.set("#{n}", {{opacity: 0}}, {W(129) + move * (k + 1) / 4:.3f});')
    if k > 0: cue(ta, "tick_" + str(k % 3 + 1), -22)
s.label(540, 1375, "DISTANCE", 28, GREY, 1)
jn = s.raw(f'<ellipse id="@ID@" cx="540" cy="1000" rx="200" ry="24" fill="none" stroke="{GOLD}" stroke-width="3" style="opacity:0"/>', "c")
tl(f'tl.fromTo("#{jn}", {{opacity: 1, scale: 0.8, transformOrigin: "50% 50%"}}, {{opacity: 0, scale: 1.8, duration: 0.8, ease: "power2.out", immediateRender: false}}, {W(132):.3f});')
cue(W(132), "bell_C5", -18)

# 14-15  the trader you are today ... the trader you can become
s = S(W(138) - 0.05, W(157) - 0.05)
for k, (x, lab) in enumerate([(130, "HABITS"), (300, "CIRCLE"), (780, "RULES"), (950, "ROUTINE")]):
    f = s.fig(x, 0.75, "#cfd3da", 0.8); s.pop(f, W(138) + k * 0.1, 0.4)
    s.label(x, 1300, lab, 28, GREY, 0); s.fade(s.items[-1].split('"')[1], W(139) + k * 0.1, 0.35)
ghost = s.fig(540, 2.0, GOLD, 0, dashed=True)
tday = s.fig(540, 1.35)
s.pop(tday, W(138), 0.5)
td = s.label(540, 900, "TODAY", 34, WHITE, 0, 800, 0.25); s.fade(td, W(146) - 0.2, 0.4)
wy = s.label(540, 1300, "WHO YOU ARE", 28, WHITE, 0, 800); s.fade(wy, W(144), 0.35)
tl(f'tl.to("#{td}", {{opacity: 0, duration: 0.3}}, {W(148):.3f});')
tl(f'tl.fromTo("#{ghost}", {{opacity: 0, scale: 0.68, transformOrigin: "50% 100%"}}, {{opacity: 1, scale: 1, duration: 1.4, ease: "power2.out", immediateRender: false}}, {W(149):.3f});')
gs = s.spot(540, 0, "232,194,106", 50, 260); s.fade(gs, W(149), 0.8)
bc = s.label(540, 560, "WHO YOU CAN BECOME", 32, GOLD, 0, 800, 0.2); s.fade(bc, W(153), 0.5, y=12)
tl(f'tl.to("#{wy}", {{opacity: 0, duration: 0.3}}, {W(149):.3f});')
cue(W(149), "swell_2", -16)

# 16  order the market
s = S(W(157) - 0.05, END_T + 0.2)
es = s.spot(540, 0, "232,194,106", 40, 230); s.fade(es, W(157), 0.6)
em = s.raw('<image id="@ID@" href="assets/otm_emblem.png" x="390" y="900" width="300" height="291" style="opacity:0;filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>', "i")
s.pop(em, W(157), 0.7, 0.6, "50% 50%"); cue(W(157), "bell_A4", -16)
o1 = s.label(540, 1300, "ORDER THE MARKET", 32, GOLD, 0, 800, 0.3); s.fade(o1, W(157) + 0.3, 0.5)
o2 = s.label(540, 1360, "DON'T LET THE MARKET ORDER YOU", 28, WHITE, 0, 700, 0.12); s.fade(o2, W(160), 0.4)
o3 = s.pill(540, 1470, "FOLLOW FOR MORE", GOLD, "#111", 30); s.pop(o3, W(166), 0.4, 0.6, "50% 50%"); cue(W(166), "click-confirm_1", -16)
# socials under the follow button
hx = 290
soc = s.raw(f'<g id="@ID@" style="opacity:0">'
            f'<rect x="{hx}" y="1548" width="36" height="36" rx="10" fill="none" stroke="#fff" stroke-width="3"/>'
            f'<circle cx="{hx + 18}" cy="1566" r="8.5" fill="none" stroke="#fff" stroke-width="3"/><circle cx="{hx + 28}" cy="1556" r="2.4" fill="#fff"/>'
            f'<text x="{hx + 48}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@fxzuez_28</text>'
            f'<path d="M {hx + 322} 1546 V 1574 A 9 9 0 1 1 {hx + 313} 1565 M {hx + 322} 1546 Q {hx + 326} 1557 {hx + 338} 1558" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>'
            f'<text x="{hx + 348}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@zuez_28</text></g>', "so")
s.fade(soc, W(162), 0.5, y=12)

# ------------------------------------------------------------------ end card, dust, ground, emblem
tl(f'tl.to("#mark", {{opacity: 0, duration: 0.3}}, {W(157) - 0.2:.3f});')
tl(f'tl.set("#end", {{opacity: 1, visibility: "visible"}}, {END_T:.3f});')
tl(f'tl.fromTo("#end-logo", {{opacity: 0, y: 20, filter: "blur(10px)"}}, {{opacity: 1, y: 0, filter: "blur(0px)", duration: 0.9, ease: "power2.out"}}, {END_T:.3f});')
tl(f'tl.fromTo("#end-note", {{opacity: 0}}, {{opacity: 1, duration: 0.6}}, {END_T + 0.5:.3f});')
tl(f'tl.fromTo("#end-credit", {{opacity: 0}}, {{opacity: 1, duration: 0.6}}, {END_T + 0.7:.3f});')
tl(f'tl.fromTo("#end-foot-img", {{y: 255}}, {{y: 0, duration: 0.6, ease: "power3.out"}}, {END_T + 0.3:.3f});')
dust = ""
for k in range(40):
    x, y, r, op = rnd.uniform(0, 1080), rnd.uniform(0, 1920), rnd.uniform(1.2, 3.2), rnd.uniform(0.05, 0.22)
    dust += f'<circle id="d{k}" cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#fff" opacity="{op:.2f}"/>'
    tl(f'tl.fromTo("#d{k}", {{x: 0, y: 0}}, {{x: {rnd.uniform(-70, 70):.0f}, y: {-rnd.uniform(150, 480):.0f}, duration: {TOTAL}, ease: "none"}}, 0);')

CREDIT = 'music: “Gmin Piano Improv (Friday)” by The3amAssociation · CC BY 3.0'
scenes_svg = "\n".join(f'<g id="{x.id}" style="opacity:0;visibility:hidden" data-layout-allow-overlap>' + "".join(x.items) + "</g>" for x in S.scenes)
CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #000; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #000; font-family: Montserrat, sans-serif; color: #fff; }
#stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
#vig { position: absolute; inset: 0; pointer-events: none; background: radial-gradient(ellipse at 50% 48%, rgba(40,44,52,0.35) 0%, transparent 55%, rgba(0,0,0,0.6) 100%); }
#mark { position: absolute; left: 495px; top: 1560px; width: 90px; opacity: 0.85; filter: drop-shadow(0 0 10px rgba(255,255,255,0.2)); }
#end { position: absolute; inset: 0; background: #000; opacity: 0; visibility: hidden; z-index: 20; }
#end-logo { position: absolute; left: 190px; top: 640px; width: 700px; }
#end-note { position: absolute; left: 0; width: 1080px; top: 1060px; text-align: center; font-size: 28px; font-weight: 600; letter-spacing: 0.12em; color: #8a8f98; }
#end-credit { position: absolute; left: 0; width: 1080px; top: 1112px; text-align: center; font-size: 28px; font-weight: 500; color: #8a8f98; }
#end-foot { position: absolute; left: 0; top: 1665px; width: 1080px; height: 255px; overflow: hidden; }
#end-foot img { width: 1080px; height: 255px; display: block; }
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
    <div id="root" data-composition-id="otm-circle" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <div id="end"><img id="end-logo" src="assets/otm_logo.png" alt="Order the Market" />
        <div id="end-note">EDUCATIONAL ONLY · NOT FINANCIAL ADVICE</div>
        <div id="end-credit">{CREDIT}</div>
        <div id="end-foot"><img id="end-foot-img" src="assets/footer.jpg" alt="" /></div></div>
      <audio id="otm-circle-audio" class="clip" src="assets/audio/mix_circle.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-circle"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
