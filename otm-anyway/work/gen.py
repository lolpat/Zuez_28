"""OTM "Start Anyway": a glowing-figure explainer (same system as otm-circle). White soft-glow figures on a dashed ground line, spotlights, small
caps labels and simple diagrams, one scene per sentence of the narration (Quentin). Gold marks the payoff, red the
gamble. Writes ../index.html, work/cues.json (soft kit sounds) and work/timing.json."""
import json, math, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAD = 0.3
GOLD, RED, WHITE, GREY, LBL = "#e8c26a", "#ff4d5e", "#ffffff", "#7d838c", "#c9ced6"
GY = 1240                                   # ground line
words = json.load(open(f"{ROOT}/work/words_take2.json"))
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
# 1  right now, somewhere, a kid in his room with a chart open, dreaming of a life nobody believes in
s = S(0, W(25) - 0.05, first=True)
s.label(540, 560, "RIGHT NOW · SOMEWHERE", 30, LBL, 1)
room = s.path(rrect(250, 700, 580, 540, 8), "#ffffffb0", 3, drawn=True)
win = s.raw('<g id="@ID@"><rect x="300" y="760" width="170" height="150" fill="none" stroke="#ffffff90" stroke-width="3"/>'
            '<line x1="385" y1="760" x2="385" y2="910" stroke="#ffffff60" stroke-width="2"/><line x1="300" y1="835" x2="470" y2="835" stroke="#ffffff60" stroke-width="2"/>'
            '<circle cx="335" cy="790" r="3" fill="#fff"/><circle cx="430" cy="805" r="2.5" fill="#fff"/><circle cx="360" cy="880" r="2" fill="#fff"/></g>')
desk = s.raw('<g id="@ID@"><rect x="520" y="1100" width="260" height="14" fill="#fff" opacity="0.85"/>'
             '<line x1="540" y1="1114" x2="540" y2="1240" stroke="#fff" stroke-width="5" opacity="0.7"/><line x1="760" y1="1114" x2="760" y2="1240" stroke="#fff" stroke-width="5" opacity="0.7"/></g>')
mon = s.raw(f'<g id="@ID@"><rect x="600" y="960" width="170" height="120" rx="8" fill="#0b1220" stroke="#fff" stroke-width="3" style="filter:drop-shadow(0 0 22px rgba(120,180,255,0.6))"/>'
            f'<line x1="685" y1="1080" x2="685" y2="1100" stroke="#fff" stroke-width="4"/></g>')
mch = s.path("M 615 1060 L 645 1040 L 670 1048 L 700 1010 L 725 1020 L 755 985", GOLD, 4)
s.draw(mch, W(12), 0.7)
kid = s.fig(470, 0.8, gy=1240)
tl(f'tl.to("#{kid}", {{y: -4, duration: 0.25, yoyo: true, repeat: 9, ease: "sine.inOut"}}, 0.4);')
bub = s.raw(f'<g id="@ID@" style="opacity:0"><circle cx="520" cy="900" r="10" fill="none" stroke="{GOLD}" stroke-width="3"/><circle cx="500" cy="860" r="16" fill="none" stroke="{GOLD}" stroke-width="3"/>'
            f'<ellipse cx="560" cy="770" rx="110" ry="62" fill="none" stroke="{GOLD}" stroke-width="3" stroke-dasharray="10 8"/>'
            f'<path d="M 520 800 L 520 760 L 560 735 L 600 760 L 600 800 Z M 548 800 V 775 H 572 V 800" fill="none" stroke="{GOLD}" stroke-width="4" stroke-linejoin="round"/></g>')
s.pop(bub, W(14), 0.5, 0.5, "50% 100%"); cue(W(14), "swell_1", -22)
for k, (x, px, txt) in enumerate([(130, 185, "NOT REALISTIC"), (950, 895, "GET A REAL JOB")]):
    f = s.fig(x, 0.7, "#9aa0a8", 0.7, False); s.pop(f, W(18) + k * 0.2, 0.4)
    p = s.pill(px, 1020 - k * 70, txt, "#2a2f38", WHITE, 28); s.pop(p, W(19) + k * 0.25, 0.35, 0.6, "50% 50%")
    cue(W(19) + k * 0.25, "tick_" + str(k + 1), -20)

# 2  maybe trade for a living, buy his parents a house, or just freedom
s = S(W(25) - 0.05, W(47) - 0.05)
s.label(540, 560, "HIS DREAMS", 30, LBL, 1)
k2 = s.fig(540, 0.95); s.pop(k2, W(25), 0.4)
dreams = [(230, W(25), ["TRADE FOR", "A LIVING"]), (540, W(33), ["PARENTS'", "HOUSE"]), (850, W(42), ["FREEDOM"])]
for k, (x, t, lab) in enumerate(dreams):
    c = s.raw(f'<circle id="@ID@" cx="{x}" cy="820" r="85" fill="none" stroke="{GOLD}" stroke-width="3" stroke-dasharray="10 8" style="opacity:0"/>', "c")
    s.pop(c, t + 0.1, 0.45, 0.5, "50% 50%")
    if k == 0:
        ic = s.path(f"M {x - 45} 850 L {x - 15} 820 L {x + 5} 835 L {x + 45} 785 M {x - 50} 865 H {x + 50}", WHITE, 4)
    elif k == 1:
        ic = s.path(f"M {x - 45} 860 V 815 L {x} 780 L {x + 45} 815 V 860 Z M {x - 12} 860 V 830 H {x + 12} V 860", WHITE, 4)
    else:
        ic = s.path(f"M {x - 50} 830 Q {x - 25} 800 {x} 828 Q {x + 25} 800 {x + 50} 830 M {x - 30} 860 Q {x - 15} 845 {x} 860 Q {x + 15} 845 {x + 30} 860", WHITE, 4)
    s.draw(ic, t + 0.3, 0.6)
    for li, line in enumerate(lab):
        lb = s.label(x, 950 + li * 36, line, 28, WHITE, 0, 800, 0.08); s.fade(lb, t + 0.4, 0.35)
    ln = s.path(f"M 540 1040 L {x} 1000", "#ffffff50", 2); s.draw(ln, t + 0.05, 0.35)
    cue(t + 0.1, "bell_" + ["G4", "C5", "E5"][k], -22)

# 3  nobody knows his name; nobody sees the backtests, the journals, the hours
s = S(W(47) - 0.05, W(59) - 0.05)
s.label(540, 560, "NOBODY SEES", 30, LBL, 1)
sp3 = s.spot(540, 0.55)
k3 = s.fig(540, 1.0, "#d9dde3", 0.9); s.pop(k3, W(47), 0.4)
nm = s.pill(540, 920, "NAME: ???", "#2a2f38", "#9aa0a8", 28); s.pop(nm, W(48), 0.35, 0.6, "50% 50%")
items = [(220, W(54), "BACKTEST #312"), (540, W(56), "JOURNAL P.94"), (860, W(58), "1,240 HOURS")]
tl(f'tl.to("#{nm}", {{opacity: 0, duration: 0.3}}, {W(51) - 0.2:.3f});')
for k, (x, t, lab) in enumerate(items):
    cd = s.path(rrect(x - 120, 690, 240, 170, 16), "#ffffff70", 3, extra=''); s.draw(cd, t - 0.15, 0.45)
    if k == 0:
        ic = s.path(f"M {x - 80} 820 L {x - 40} 790 L {x - 10} 805 L {x + 30} 755 L {x + 80} 740", "#ffffffa0", 3)
    elif k == 1:
        ic = s.path(f"M {x - 70} 735 H {x + 70} M {x - 70} 770 H {x + 50} M {x - 70} 805 H {x + 70} M {x - 70} 840 H {x + 20}", "#ffffffa0", 3)
    else:
        ic = s.path(f"M {x - 50} 775 a 50 50 0 1 0 100 0 a 50 50 0 1 0 -100 0 M {x} 775 V 745 M {x} 775 L {x + 25} 790", "#ffffffa0", 3)
    s.draw(ic, t, 0.5)
    lb = s.label(x, 900, lab, 28, LBL, 0, 700, 0.08); s.fade(lb, t + 0.15, 0.35)
    cue(t, "key_" + str(3 + 2 * k if k < 2 else 3), -22)

# 4  but he's working on it anyway
s = S(W(59) - 0.05, W(72) - 0.05)
s.label(540, 560, "HE STARTS ANYWAY", 30, LBL, 1)
s.raw('<g id="@ID@"><rect x="400" y="1100" width="300" height="14" fill="#fff" opacity="0.85"/>'
      '<line x1="420" y1="1114" x2="420" y2="1240" stroke="#fff" stroke-width="5" opacity="0.7"/><line x1="680" y1="1114" x2="680" y2="1240" stroke="#fff" stroke-width="5" opacity="0.7"/>'
      '<rect x="470" y="960" width="170" height="120" rx="8" fill="#0b1220" stroke="#fff" stroke-width="3" style="filter:drop-shadow(0 0 22px rgba(120,180,255,0.6))"/>'
      '<line x1="555" y1="1080" x2="555" y2="1100" stroke="#fff" stroke-width="4"/></g>')
k4 = s.fig(420, 0.85)
tl(f'tl.to("#{k4}", {{y: -4, duration: 0.2, yoyo: true, repeat: {int((W(72) - W(59)) / 0.2) - 1}, ease: "sine.inOut"}}, {W(59):.3f});')
c4 = s.path("M 485 1060 L 515 1045 L 540 1052 L 570 1020 L 595 1030 L 625 990", GOLD, 4); s.draw(c4, W(60), 1.2)
s.path("M 240 1330 H 840", "#ffffff40", 14, drawn=True)
bar = s.raw(f'<line id="@ID@" x1="240" y1="1330" x2="840" y2="1330" stroke="{GOLD}" stroke-width="14" stroke-linecap="round" style="opacity:1"/>', "l")
tl(f'tl.fromTo("#{bar}", {{scaleX: 0.02, transformOrigin: "0% 50%"}}, {{scaleX: 0.42, duration: {W(72) - W(59) - 0.3:.3f}, ease: "power1.inOut", immediateRender: false}}, {W(59):.3f});')
s.label(240, 1390, "PROGRESS", 28, GREY, 1, 700, 0.15, "start")
any4 = s.label(540, 700, "ANYWAY.", 64, GOLD, 0, 800, 0.08); s.fade(any4, W(64), 0.4, y=14); cue(W(64), "land_1", -18)

# 5  you don't need everybody to believe in you; no applause, no permission, nobody saying you're good enough
s = S(W(72) - 0.05, W(93) - 0.05)
s.label(540, 560, "YOU DON'T NEED", 30, LBL, 1)
crowd = []
for k, x in enumerate([150, 310, 770, 930]):
    f = s.fig(x, 0.8, "#cfd3da", 0.85); s.pop(f, W(72) + k * 0.08, 0.4); crowd.append(f)
    tl(f'tl.to("#{f}", {{opacity: 0.2, duration: 0.5}}, {W(80) + k * 0.06:.3f});')
y5 = s.fig(540, 1.05); s.pop(y5, W(72), 0.4)
ys = s.spot(540, 0, "232,194,106"); s.fade(ys, W(80), 0.5)
st = s.pill(540, 960, "START", GOLD, "#111", 32); s.pop(st, W(82), 0.4, 0.6, "50% 50%"); cue(W(82), "click-confirm_1", -16)
for k, (txt, t, y) in enumerate([("APPLAUSE", W(84), 700), ("PERMISSION", W(86), 790), ("“YOU'RE GOOD ENOUGH”", W(87), 880)]):
    xpos = 540
    p = s.pill(xpos, y - 60, txt, "#2a2f38", WHITE, 28); s.pop(p, t - 0.1, 0.3, 0.6, "50% 50%")
    hw = len(txt) * 28 * 0.37 + 30
    sl = s.path(f"M {xpos - hw} {y - 60} H {xpos + hw}", GOLD, 5); s.draw(sl, t + 0.45, 0.25)
    tl(f'tl.to("#{p}", {{opacity: 0.35, duration: 0.3}}, {t + 0.6:.3f});')
    cue(t + 0.45, "whoosh-short_" + str(k + 1), -22)

# 6  believe in a plan before anyone else can see it
s = S(W(93) - 0.05, W(107) - 0.05)
s.label(540, 560, "THE PLAN", 30, LBL, 1)
y6 = s.fig(200, 0.95); s.pop(y6, W(93), 0.4)
steps = "M 280 1240 H 380 V 1140 H 480 V 1040 H 580 V 940 H 680 V 840 H 780"
pl = s.path(steps, GOLD, 4, extra=''); s.draw(pl, W(95), W(101) - W(95))
fl = s.raw(f'<g id="@ID@" style="opacity:0"><line x1="780" y1="840" x2="780" y2="720" stroke="{GOLD}" stroke-width="4"/>'
           f'<path d="M 780 722 L 850 745 L 780 768 Z" fill="{GOLD}"/></g>')
s.pop(fl, W(101), 0.4, 0.4); cue(W(101), "bell_A4", -20)
fog = s.raw('<rect id="@ID@" x="380" y="700" width="520" height="560" fill="url(#fogg)" style="opacity:0"/>', "r")
s.items.insert(0, '<defs><linearGradient id="fogg" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="0.35" stop-color="#05070a" stop-opacity="0.92"/><stop offset="1" stop-color="#05070a" stop-opacity="0.96"/></linearGradient></defs>')
s.fade(fog, W(102), 0.6)
for k, x in enumerate([880, 990]):
    f = s.fig(x, 0.75, "#9aa0a8", 0.75, False); s.pop(f, W(102) + k * 0.12, 0.4)
    q = s.pill(x, 960 - k * 60, "?", "#2a2f38", WHITE, 32); s.pop(q, W(104) + k * 0.15, 0.3, 0.5, "50% 50%")
    cue(W(104) + k * 0.15, "pop_" + str(k + 1), -22)
sl6 = s.label(540, 1330, "ONLY YOU CAN SEE IT", 28, GOLD, 0, 800); s.fade(sl6, W(101) + 0.2, 0.4)

# 7  start learning, start backtesting, take the small loss, try again
s = S(W(107) - 0.05, W(118) - 0.05)
s.label(540, 560, "START", 30, LBL, 1)
stairs = [(200, 1240, "LEARN", W(108)), (420, 1140, "BACKTEST", W(110)), (640, 1040, "SMALL LOSS", W(112)), (860, 940, "TRY AGAIN", W(116))]
d = "M 90 1240 H 310 V 1140 H 530 V 1040 H 750 V 940 H 990"
sp = s.path(d, WHITE, 3); s.draw(sp, W(107), 0.7)
y7 = s.fig(120, 0.8)
px, py = 120, 1240
for k, (x, y, lab, t) in enumerate(stairs):
    lb = s.label(x, y + 50, lab, 28, RED if k == 2 else WHITE, 0, 800, 0.1); s.fade(lb, t, 0.3)
    tl(f'tl.to("#{y7}", {{x: {x - 120}, y: {y - 1240}, duration: 0.45, ease: "power2.inOut"}}, {t:.3f});')
    cue(t + 0.4, "land-light_1" if k == 2 else "tock_1", -18)
rt = s.pill(640, 900, "-1R", RED, WHITE, 28); s.pop(rt, W(114), 0.3, 0.6, "50% 50%")
tl(f'tl.to("#{rt}", {{opacity: 0, duration: 0.3}}, {W(116):.3f});')
ok7 = s.pill(860, 800, "+3R", GOLD, "#111", 28); s.pop(ok7, W(117) + 0.3, 0.35, 0.6, "50% 50%"); cue(W(117) + 0.3, "bell_E5", -20)

# 8  somewhere, someone is chasing the same goal, and they're not waiting for the perfect moment
s = S(W(118) - 0.05, W(137) - 0.05)
s.label(540, 560, "SAME GOAL", 30, LBL, 1)
s.path("M 60 1020 H 1020", "#ffffff50", 2, drawn=True, extra='stroke-dasharray="12 12"')
for y in (1020, 1240):
    s.raw(f'<g id="@ID@"><line x1="960" y1="{y}" x2="960" y2="{y - 170}" stroke="{GOLD}" stroke-width="4"/><path d="M 960 {y - 168} L 1020 {y - 148} L 960 {y - 128} Z" fill="{GOLD}"/></g>')
oth = s.fig(140, 0.8, "#cfd3da", 0.9, gy=1020); s.pop(oth, W(120), 0.4)
ol = s.label(140, 830, "SOMEONE", 28, GREY, 0); s.fade(ol, W(120) + 0.2, 0.3)
me8 = s.fig(140, 0.8); s.pop(me8, W(124), 0.4)
ml = s.label(140, 1295, "YOU", 28, WHITE, 0, 800); s.fade(ml, W(124) + 0.2, 0.3)
s.walk(oth, W(122), 520, W(137) - W(122) - 0.3)
tl(f'tl.to("#{ol}", {{x: "+=520", duration: {W(137) - W(122) - 0.3:.3f}, ease: "power1.inOut"}}, {W(122):.3f});')
wt = s.pill(420, 1060, "WAITING FOR THE PERFECT MOMENT", "#2a2f38", WHITE, 28)
s.pop(wt, W(130), 0.35, 0.6, "50% 50%"); cue(W(130), "tick_2", -20)
wx = s.path("M 90 1060 H 750", GOLD, 5); s.draw(wx, W(135), 0.3)

# 9  so what are you waiting for?
s = S(W(137) - 0.05, W(143) - 0.05)
sp9 = s.spot(540, 1)
y9 = s.fig(540, 1.1); s.pop(y9, W(137), 0.4)
qm = s.label(540, 860, "?", 160, GOLD, 0, 800, 0); s.pop(qm, W(141) - 0.1, 0.4, 0.4, "50% 50%"); cue(W(141), "pop_3", -16)
wl = s.label(540, 1330, "WHAT ARE YOU WAITING FOR", 28, WHITE, 0, 800, 0.14); s.fade(wl, W(138), 0.4)

# 10  your equity curve isn't going to draw itself
s = S(W(143) - 0.05, W(151) - 0.05)
s.label(540, 560, "YOUR EQUITY CURVE", 30, LBL, 1)
s.path("M 120 660 V 1180 H 960", "#ffffff60", 2, drawn=True)
eq = s.path("M 130 1150 L 220 1120 L 290 1135 L 370 1060 L 440 1080 L 530 980 L 600 1000 L 690 880 L 760 900 L 860 760 L 950 700", GOLD, 6,
            extra='')
dur = W(151) - W(144) - 0.3
s.draw(eq, W(144), dur, "power1.inOut")
y10 = s.fig(130, 0.7)
s.walk(y10, W(144), 800, dur)
tip = s.raw(f'<circle id="@ID@" cx="950" cy="700" r="14" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 12px {GOLD})"/>', "c")
s.pop(tip, W(144) + dur, 0.35, 0.3, "50% 50%"); cue(W(144) + dur, "bell_G5", -18)
dl = s.label(540, 1330, "YOU DRAW IT", 30, GOLD, 0, 800); s.fade(dl, W(149), 0.4)

# 11  order the market
s = S(W(151) - 0.05, TOTAL)
es = s.spot(540, 0, "232,194,106", 40, 230); s.fade(es, W(151), 0.6)
em = s.raw('<image id="@ID@" href="assets/otm_emblem.png" x="390" y="900" width="300" height="291" style="opacity:0;filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>', "i")
s.pop(em, W(151), 0.7, 0.6, "50% 50%"); cue(W(151), "bell_A4", -16)
o1 = s.label(540, 1300, "ORDER THE MARKET", 32, GOLD, 0, 800, 0.3); s.fade(o1, W(151) + 0.3, 0.5)
o2 = s.label(540, 1360, "DON'T LET THE MARKET ORDER YOU", 28, WHITE, 0, 700, 0.12); s.fade(o2, W(154), 0.4)
o3 = s.pill(540, 1470, "FOLLOW FOR MORE", GOLD, "#111", 30); s.pop(o3, W(160), 0.4, 0.6, "50% 50%"); cue(W(160), "click-confirm_1", -16)
# socials under the follow button
hx = 290
soc = s.raw(f'<g id="@ID@" style="opacity:0">'
            f'<rect x="{hx}" y="1548" width="36" height="36" rx="10" fill="none" stroke="#fff" stroke-width="3"/>'
            f'<circle cx="{hx + 18}" cy="1566" r="8.5" fill="none" stroke="#fff" stroke-width="3"/><circle cx="{hx + 28}" cy="1556" r="2.4" fill="#fff"/>'
            f'<text x="{hx + 48}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@fxzuez_28</text>'
            f'<path d="M {hx + 322} 1546 V 1574 A 9 9 0 1 1 {hx + 313} 1565 M {hx + 322} 1546 Q {hx + 326} 1557 {hx + 338} 1558" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>'
            f'<text x="{hx + 348}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@zuez_28</text></g>', "so")
disc = s.label(540, 1650, "EDUCATIONAL ONLY · NOT FINANCIAL ADVICE", 28, GREY, 0, 600, 0.12)
soc_t = W(156)
s.fade(soc, soc_t, 0.5, y=12)
s.fade(disc, soc_t + 0.3, 0.5)

# ------------------------------------------------------------------ end card, dust, ground, emblem
tl(f'tl.to("#mark", {{opacity: 0, duration: 0.3}}, {W(151) - 0.2:.3f});')
dust = ""
for k in range(40):
    x, y, r, op = rnd.uniform(0, 1080), rnd.uniform(0, 1920), rnd.uniform(1.2, 3.2), rnd.uniform(0.05, 0.22)
    dust += f'<circle id="d{k}" cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#fff" opacity="{op:.2f}"/>'
    tl(f'tl.fromTo("#d{k}", {{x: 0, y: 0}}, {{x: {rnd.uniform(-70, 70):.0f}, y: {-rnd.uniform(150, 480):.0f}, duration: {TOTAL}, ease: "none"}}, 0);')

CREDIT = 'music: “Piece of Quiet” by geoffpeters · CC BY 3.0'
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
    <div id="root" data-composition-id="otm-anyway" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-anyway-audio" class="clip" src="assets/audio/mix_anyway.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-anyway"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
