"""OTM "The Trade You Missed": a glowing-figure story in the OTM style (same scene system as otm-chance / otm-livermore),
inspired by a "the delay that saved me" skit. POV: the perfect setup, the platform freezes at the entry, price runs
without you, the urge to chase at any price (you don't), then breaking news spikes the market through where your stop
would have been: the trade you missed would have been a big loss. A missed trade costs nothing; a forced trade can
cost everything. Not every setup is yours. Original script, voice only (Quentin), no music.
Scenes key off word indices of work/words.json (helper ix). Writes ../index.html, work/cues.json and work/timing.json."""
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

def header(s, text, col=LBL):
    return s.label(540, 560, text, 30, col, 1, 700, 0.2)

def monitor(s, x0, y0, w, h, op=1):
    """a trading screen on a stand; returns its id"""
    return s.raw(f'<g id="@ID@" style="opacity:{op}"><rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="14" fill="#0b1220" stroke="#fff" stroke-width="4" '
                 f'style="filter:drop-shadow(0 0 18px rgba(120,180,255,0.35))"/>'
                 f'<rect x="{x0 + w / 2 - 14}" y="{y0 + h}" width="28" height="50" fill="#fff" opacity="0.8"/>'
                 f'<rect x="{x0 + w / 2 - 90}" y="{y0 + h + 50}" width="180" height="10" rx="5" fill="#fff" opacity="0.8"/></g>', "mon")

def check(s, x, y, col=GOLD, sz=1.0, w=6):
    return s.path(f"M {x - 16 * sz} {y} L {x - 4 * sz} {y + 13 * sz} L {x + 18 * sz} {y - 15 * sz}", col, w)

# 1  "POV: The trade gets away from you."
s = S(0, ix(7) - 0.1, first=True)
s.label(540, 560, "POV:", 40, GOLD, 1, 800, 0.2)
s.label(540, 630, "THE TRADE GETS AWAY FROM YOU", 40, WHITE, 1, 800, 0.03)
monitor(s, 430, 740, 440, 270)
s.path("M 460 950 L 520 920 L 570 935 L 630 880 L 680 895 L 740 840 L 800 810", "#ffffff60", 4, drawn=True)
ga = s.raw(f'<g id="@ID@"><path d="M 800 810 L 860 780" stroke="{GOLD}" stroke-width="6" stroke-linecap="round"/>'
           f'<polygon points="872,774 842,772 856,796" fill="{GOLD}"/></g>', "ga")
tl(f'tl.to("#{ga}", {{x: 260, y: -260, opacity: 0, duration: 0.9, ease: "power2.in"}}, {ix(4) - 0.1:.3f});')
cue(ix(4) - 0.1, "whoosh-short_1", -18)
y1 = s.fig(270, 0.95, WHITE)

# 2  "The setup is perfect. You've waited all week for it."
s = S(ix(7) - 0.1, ix(17) - 0.1, ground=False, restore=False)
header(s, "THE SETUP")
s.path("M 90 1150 H 990", "#ffffff40", 2, drawn=True)
r2 = random.Random(2)
pts = [(110 + k * 22, 1000 + r2.uniform(-25, 25) if 8 <= k <= 26 else 1060 - k * 4 if k < 8 else 1000 - (k - 26) * 2) for k in range(36)]
ch2 = s.path("M " + " L ".join(f"{x:.0f} {y:.0f}" for x, y in pts), WHITE, 4); s.draw(ch2, ix(7), 1.2)
zone = s.raw(f'<rect id="@ID@" x="276" y="960" width="420" height="80" rx="8" fill="{GOLD}" fill-opacity="0.12" stroke="{GOLD}" stroke-width="3" stroke-dasharray="10 8" style="opacity:0"/>', "zn")
s.fade(zone, ix(8) - 0.1, 0.4); cue(ix(8) - 0.1, "pop_1", -20)
pf = s.label(486, 930, "PERFECT", 32, GOLD, 0, 800, 0.2); s.fade(pf, ix(10) - 0.1, 0.35, y=10)
for k, d in enumerate(["M", "T", "W", "T", "F"]):
    x = 300 + k * 120
    s.raw(f'<g id="@ID@"><circle cx="{x}" cy="760" r="34" fill="none" stroke="#ffffff50" stroke-width="2"/>'
          f'<text x="{x}" y="771" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" fill="{LBL}">{d}</text></g>', "dd")
    dg = s.raw(f'<circle id="@ID@" cx="{x}" cy="760" r="34" fill="{GOLD}" fill-opacity="0.2" stroke="{GOLD}" stroke-width="3" style="opacity:0"/>', "dg")
    s.fade(dg, ix(12) + k * 0.2, 0.25); cue(ix(12) + k * 0.2, "tick_" + str(k % 3 + 1), -24)
wk = s.label(540, 850, "WAITED ALL WEEK", 30, WHITE, 0, 800, 0.15); s.fade(wk, ix(13), 0.35)

# 3  "You reach for the entry... and the platform freezes."
s = S(ix(17) - 0.1, ix(26) - 0.1, ground=False, hide=False, restore=False)
mon3 = monitor(s, 160, 640, 760, 480)
s.path("M 200 1000 L 290 960 L 360 980 L 450 900 L 520 920 L 600 860", "#ffffffa0", 4, drawn=True)
buy = s.raw(f'<g id="@ID@"><rect x="660" y="980" width="200" height="90" rx="14" fill="{GOLD}"/>'
            f'<text x="760" y="1040" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="40" fill="#111">BUY</text></g>', "by")
cur = s.raw(f'<path id="@ID@" d="M 0 0 L 0 46 L 12 34 L 22 56 L 30 52 L 20 31 L 36 31 Z" fill="#fff" stroke="#000" stroke-width="2" transform="translate(380 1180)"/>', "cu")
tl(f'tl.fromTo("#{cur}", {{x: 0, y: 0}}, {{x: 360, y: -150, duration: 0.9, ease: "power2.inOut", immediateRender: false}}, {ix(18) - 0.1:.3f});')
tl(f'tl.fromTo("#{buy}", {{scale: 1, transformOrigin: "50% 50%"}}, {{scale: 0.92, duration: 0.08, yoyo: true, repeat: 1, immediateRender: false}}, {ix(21):.3f});')
cue(ix(21), "click_1", -14)
frz = s.raw(f'<rect id="@ID@" x="164" y="644" width="752" height="472" rx="12" fill="#000" style="opacity:0"/>', "fz")
tl(f'tl.fromTo("#{frz}", {{opacity: 0}}, {{opacity: 0.62, duration: 0.15, immediateRender: false}}, {ix(24) - 0.05:.3f});')
ring = s.raw(f'<circle id="@ID@" cx="540" cy="840" r="46" fill="none" stroke="#ffffff30" stroke-width="7" style="opacity:0"/>', "rg"); s.fade(ring, ix(24), 0.2)
spin = s.raw(f'<circle id="@ID@" cx="540" cy="840" r="46" fill="none" stroke="#fff" stroke-width="7" stroke-dasharray="70 220" stroke-linecap="round" style="opacity:0"/>', "sp")
s.fade(spin, ix(24), 0.2)
tl(f'tl.fromTo("#{spin}", {{rotation: 0, transformOrigin: "50% 50%"}}, {{rotation: 720, duration: 1.4, ease: "none", immediateRender: false}}, {ix(24):.3f});')
nr = s.label(540, 960, "NOT RESPONDING", 34, RED, 0, 800, 0.14); s.fade(nr, ix(25) - 0.1, 0.3)
tl(f'tl.fromTo("#{mon3}", {{x: -6}}, {{x: 6, duration: 0.05, repeat: 5, yoyo: true, ease: "none", immediateRender: false}}, {ix(25):.3f});')
cue(ix(25) - 0.1, "tock_1", -16)

# 4  "The price moves without you."
s = S(ix(26) - 0.1, ix(31) - 0.1, ground=False, hide=False)
header(s, "WITHOUT YOU")
s.path("M 90 1150 H 990", "#ffffff40", 2, drawn=True)
en = s.path("M 120 1020 H 980", "#ffffff70", 3, drawn=True, extra='stroke-dasharray="12 10"')
s.label(130, 1062, "YOUR ENTRY", 28, LBL, 1, 700, 0.12, "start")
run = s.path("M 140 1020 L 260 990 L 320 1005 L 440 920 L 500 940 L 640 820 L 700 840 L 860 700 L 960 650", GOLD, 6, style="filter:drop-shadow(0 0 10px rgba(232,194,106,0.7))")
s.draw(run, ix(27) - 0.1, 1.3); cue(ix(27) - 0.1, "swell_1", -20)
y4 = s.fig(200, 0.7, "#9aa0a8", 0.8, False, 1240)

# 5  "You're frustrated. You were right, and you're not in it."
s = S(ix(31) - 0.1, ix(41) - 0.1)
y5 = s.fig(540, 1.0, WHITE); s.pop(y5, ix(31) - 0.05, 0.35)
fr = s.path("M 470 980 L 450 950 L 480 945 L 460 915 M 610 980 L 630 950 L 600 945 L 620 915 M 540 920 L 525 885 L 555 880 L 540 845", RED, 5)
s.draw(fr, ix(32) - 0.1, 0.4); cue(ix(32) - 0.1, "tock_1", -18)
tl(f'tl.fromTo("#{y5}", {{x: -5}}, {{x: 5, duration: 0.05, repeat: 7, yoyo: true, ease: "none", immediateRender: false}}, {ix(32):.3f});')
r1 = s.label(560, 680, "YOU WERE RIGHT", 40, GOLD, 0, 800, 0.08); s.fade(r1, ix(33) - 0.1, 0.35, y=10)
ck5 = check(s, 190, 668, GOLD, 1.0); s.draw(ck5, ix(35) - 0.1, 0.3)
r2l = s.label(560, 760, "YOU'RE NOT IN", 40, RED, 0, 800, 0.08); s.fade(r2l, ix(37) - 0.1, 0.35, y=10)
xm5 = s.path("M 192 742 L 222 772 M 222 742 L 192 772", RED, 6); s.draw(xm5, ix(38) - 0.1, 0.3)

# 6  "So you tell yourself, just chase it. Get in now, at any price. But you don't."
s = S(ix(41) - 0.1, ix(57) - 0.1)
y6 = s.fig(300, 1.0, WHITE); s.pop(y6, ix(41), 0.35)
bub = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(150, 700, 330, 120, 26)}" fill="#11151b" stroke="{RED}" stroke-width="3"/>'
            f'<text x="315" y="773" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" fill="{RED}">JUST CHASE IT</text>'
            f'<circle cx="280" cy="852" r="10" fill="{RED}"/><circle cx="294" cy="884" r="6" fill="{RED}"/></g>', "bb")
s.pop(bub, ix(45) - 0.1, 0.4, 0.5, "50% 50%"); cue(ix(45) - 0.1, "pop_2", -18)
cb = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 22px rgba(255,77,94,0.7))"><rect x="600" y="900" width="380" height="140" rx="22" fill="{RED}"/>'
           f'<text x="790" y="960" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="40" fill="#fff">BUY NOW</text>'
           f'<text x="790" y="1010" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="28" fill="#fff">ANY PRICE</text></g>', "cb")
s.pop(cb, ix(48) - 0.1, 0.4, 0.5, "50% 50%"); cue(ix(48) - 0.1, "click_2", -18)
tl(f'tl.fromTo("#{cb}", {{scale: 1, transformOrigin: "50% 50%"}}, {{scale: 1.06, duration: 0.3, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}}, {ix(50) + 0.12:.3f});')
tl(f'tl.to("#{cb}", {{opacity: 0.18, duration: 0.4}}, {ix(55) - 0.1:.3f});')
tl(f'tl.to("#{bub}", {{opacity: 0, duration: 0.3}}, {ix(55) - 0.1:.3f});')
s.walk(y6, ix(54), -120, 0.7)
yd = s.label(540, 640, "BUT YOU DON'T", 44, GOLD, 0, 800, 0.1); s.fade(yd, ix(55) - 0.05, 0.4, y=10)
cue(ix(55), "bell_C5", -18)

# 7  "Ten minutes later, the news hits. The market spikes the other way, straight through where your stop would have been."
s = S(ix(57) - 0.1, ix(77) - 0.1, ground=False, restore=False)
tm = s.label(540, 560, "+10 MIN", 40, LBL, 0, 800, 0.2); s.fade(tm, ix(57), 0.35); cue(ix(57), "tick-crisp_1", -18)
nb = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="140" y="610" width="800" height="76" rx="8" fill="{RED}"/>'
           f'<text x="540" y="660" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="36" letter-spacing="0.14em" fill="#fff">BREAKING NEWS</text></g>', "nb")
tl(f'tl.fromTo("#{nb}", {{opacity: 0, scaleX: 0.2, transformOrigin: "50% 50%"}}, {{opacity: 1, scaleX: 1, duration: 0.35, ease: "back.out(1.6)", immediateRender: false}}, {ix(61) - 0.1:.3f});')
cue(ix(61) - 0.1, "land-light_1", -16)
s.path("M 90 1230 H 990", "#ffffff40", 2, drawn=True)
s.path("M 140 1020 L 260 990 L 320 1005 L 440 920 L 500 940 L 640 820 L 700 840", "#e8c26a90", 5, drawn=True)
stp = s.path("M 120 1060 H 980", "#ffffff90", 3, extra='stroke-dasharray="12 10"'); s.draw(stp, ix(70) - 0.4, 0.5)
sl = s.label(130, 1102, "WHERE YOUR STOP WOULD BE", 28, LBL, 0, 700, 0.08, "start"); s.fade(sl, ix(71) - 0.1, 0.3)
dn = s.path("M 700 840 L 760 760 L 800 900 L 840 1010 L 880 1150 L 930 1200", RED, 7, style="filter:drop-shadow(0 0 12px rgba(255,77,94,0.8))")
s.draw(dn, ix(65) - 0.1, 0.9); cue(ix(65) - 0.1, "whoosh-long_1", -16)
hit = s.path("M 830 1035 L 870 1075 M 870 1035 L 830 1075", RED, 7); s.draw(hit, ix(73) - 0.1, 0.3); cue(ix(73) - 0.1, "tock_1", -16)

# 8  "The trade you missed would have been a loss. A big one."
s = S(ix(77) - 0.1, ix(89) - 0.1, ground=False, hide=False)
gt = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(200, 660, 680, 420, 24)}" fill="none" stroke="#ffffff60" stroke-width="3" stroke-dasharray="14 10"/>'
           f'<text x="540" y="740" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="32" letter-spacing="0.12em" fill="{LBL}">THE TRADE YOU MISSED</text></g>', "gt")
s.fade(gt, ix(77), 0.4)
ls = s.label(540, 900, "LOSS", 120, RED, 0, 800, 0.06)
tl(f'tl.fromTo("#{ls}", {{opacity: 0, scale: 1.4, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.45, ease: "expo.out", immediateRender: false}}, {ix(85) - 0.15:.3f});')
cue(ix(85) - 0.15, "land_1", -16)
bg8 = s.label(540, 1000, "A BIG ONE", 40, RED, 0, 800, 0.2); s.fade(bg8, ix(87) - 0.1, 0.35, y=10)
av = s.label(540, 1200, "AVOIDED", 44, GOLD, 0, 800, 0.24); s.fade(av, ix(88) + 0.2, 0.4, y=10)

# 9  "Sometimes, the market takes a trade away from you, and it's the best thing that happens all day."
s = S(ix(89) - 0.1, ix(107) - 0.1)
s.spot(540, 1, "232,194,106")
y9 = s.fig(540, 1.0, GOLD); s.pop(y9, ix(89), 0.4)
sh = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 20px rgba(232,194,106,0.8))"><path d="M 540 640 L 650 680 V 770 C 650 840 600 880 540 905 C 480 880 430 840 430 770 V 680 Z" fill="#14120a" stroke="{GOLD}" stroke-width="6"/>'
           f'<path d="M 495 770 L 530 805 L 590 740" fill="none" stroke="{GOLD}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></g>', "sh")
s.pop(sh, ix(101) - 0.15, 0.5, 0.4, "50% 50%"); cue(ix(101) - 0.15, "bell_E5", -16)
bt = s.label(540, 1320, "THE BEST THING ALL DAY", 36, GOLD, 0, 800, 0.1); s.fade(bt, ix(101), 0.4, y=10)
ta = s.label(540, 1320, "THE MARKET TOOK A TRADE AWAY", 32, WHITE, 0, 800, 0.06); s.fade(ta, ix(92) - 0.1, 0.4, y=10)
tl(f'tl.to("#{ta}", {{opacity: 0, duration: 0.25}}, {ix(101) - 0.3:.3f});')

# 10  "A missed trade costs you nothing. A forced trade can cost you everything."
s = S(ix(107) - 0.1, ix(120) - 0.1, ground=False)
for k, (title, val, col, w_title, w_val) in enumerate([("MISSED TRADE", "$0", GOLD, 108, 112), ("FORCED TRADE", "EVERYTHING", RED, 114, 119)]):
    x = 290 + k * 500
    c = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(x - 220, 700, 440, 420, 26)}" fill="#0f1319" stroke="{col}" stroke-width="3"/>'
              f'<text x="{x}" y="780" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" letter-spacing="0.1em" fill="#fff">{title}</text>'
              f'<text x="{x}" y="850" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="28" letter-spacing="0.2em" fill="{LBL}">COSTS YOU</text></g>', "cd")
    s.pop(c, ix(w_title) - 0.2, 0.4, 0.6, "50% 50%")
    v = s.label(x, 1000, val, 96 if k == 0 else 54, col, 0, 800, 0.04)
    tl(f'tl.fromTo("#{v}", {{opacity: 0, scale: 1.4, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.45, ease: "expo.out", immediateRender: false}}, {ix(w_val) - 0.15:.3f});')
    cue(ix(w_val) - 0.15, "bell_G5" if k == 0 else "land_1", -16)

# 11  "Not every setup is yours. Let it go."
s = S(ix(120) - 0.1, ix(128) - 0.05)
tiles = []
r11 = random.Random(11)
for k in range(5):
    x = 140 + k * 200
    pts = " L ".join(f"{x - 70 + j * 28:.0f} {780 - r11.uniform(-30, 30):.0f}" for j in range(6))
    t = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(x - 85, 700, 170, 160, 16)}" fill="#0f1319" stroke="#ffffff70" stroke-width="2"/>'
              f'<path d="M {pts}" fill="none" stroke="{GOLD if k == 2 else "#ffffffb0"}" stroke-width="4"/></g>', "tt")
    s.pop(t, ix(120) + k * 0.1, 0.35, 0.5, "50% 50%"); tiles.append(t)
for k, t in enumerate(tiles):
    if k != 2:
        tl(f'tl.to("#{t}", {{y: -160, opacity: 0, duration: 1.0, ease: "power2.in"}}, {ix(125) + abs(k - 2) * 0.12:.3f});')
cue(ix(125), "whoosh-long_1", -20)
ny = s.label(540, 620, "NOT EVERY SETUP IS YOURS", 38, WHITE, 0, 800, 0.06); s.fade(ny, ix(120), 0.4, y=10)
lg = s.label(540, 960, "LET IT GO", 48, GOLD, 0, 800, 0.2); s.fade(lg, ix(125), 0.4, y=10)
y11 = s.fig(540, 0.95, WHITE); s.pop(y11, ix(120) + 0.2, 0.4)

# 12  outro (handles, no end card)
s = S(ix(128) - 0.05, TOTAL)
es = s.spot(540, 0, "232,194,106", 40, 230); s.fade(es, ix(128), 0.6)
em = s.raw('<image id="@ID@" href="assets/otm_emblem.png" x="390" y="900" width="300" height="291" style="opacity:0;filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>', "i")
s.pop(em, ix(128), 0.7, 0.6, "50% 50%"); cue(ix(128), "bell_A4", -16)
o1 = s.label(540, 1300, "ORDER THE MARKET", 32, GOLD, 0, 800, 0.3); s.fade(o1, ix(128) + 0.3, 0.5)
o2 = s.label(540, 1360, "DON'T LET THE MARKET ORDER YOU", 28, WHITE, 0, 700, 0.12); s.fade(o2, ix(131), 0.4)
o3 = s.pill(540, 1470, "FOLLOW FOR MORE", GOLD, "#111", 30); s.pop(o3, ix(137), 0.4, 0.6, "50% 50%"); cue(ix(137), "click-confirm_1", -16)
hx = 290
soc = s.raw(f'<g id="@ID@" style="opacity:0">'
            f'<rect x="{hx}" y="1548" width="36" height="36" rx="10" fill="none" stroke="#fff" stroke-width="3"/>'
            f'<circle cx="{hx + 18}" cy="1566" r="8.5" fill="none" stroke="#fff" stroke-width="3"/><circle cx="{hx + 28}" cy="1556" r="2.4" fill="#fff"/>'
            f'<text x="{hx + 48}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@fxzuez_28</text>'
            f'<path d="M {hx + 322} 1546 V 1574 A 9 9 0 1 1 {hx + 313} 1565 M {hx + 322} 1546 Q {hx + 326} 1557 {hx + 338} 1558" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>'
            f'<text x="{hx + 348}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@zuez_28</text></g>', "so")
disc = s.label(540, 1650, "EDUCATIONAL ONLY · NOT FINANCIAL ADVICE", 28, GREY, 0, 600, 0.12)
s.fade(soc, ix(131) + 0.6, 0.5, y=12)
s.fade(disc, ix(131) + 0.9, 0.5)
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
    <div id="root" data-composition-id="otm-missed" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
{TIMELINE}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-missed-audio" class="clip" src="assets/audio/mix_missed.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-missed"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
