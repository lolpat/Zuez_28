"""OTM "Believe First": a glowing-figure explainer (same system as otm-circle / otm-anyway / otm-know / otm-noise). Voice only, no music. White soft-glow figures on a dashed ground line, spotlights, small
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

def badge(s, x, y):
    return s.raw(f'<circle id="@ID@" cx="{x}" cy="{y}" r="9" fill="{RED}" style="filter:drop-shadow(0 0 6px {RED})"/>', "c")

def screens(s, x0, y0, cols, rows, w=110, h=72, gap=16, lit=True):
    ids = []
    for r in range(rows):
        for c in range(cols):
            x, y = x0 + c * (w + gap), y0 + r * (h + gap)
            ids.append(s.raw(f'<g id="@ID@"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#0b1220" stroke="#fff" stroke-width="2.5" '
                             f'style="filter:drop-shadow(0 0 10px rgba(120,180,255,0.5))"/>'
                             f'<path d="M {x + 12} {y + h - 18} L {x + 35} {y + h - 34} L {x + 55} {y + h - 26} L {x + 80} {y + 22} L {x + w - 10} {y + 16}" fill="none" stroke="{GOLD}" stroke-width="2.5"/></g>', "sc"))
    return ids

def tree(s, x, gy=GY, sc=1.0):
    return s.raw(f'<g id="@ID@" style="opacity:0"><line x1="{x}" y1="{gy}" x2="{x}" y2="{gy - 120 * sc}" stroke="#fff" stroke-width="{6 * sc}"/>'
                 f'<circle cx="{x}" cy="{gy - 175 * sc}" r="{75 * sc}" fill="none" stroke="#fff" stroke-width="4" style="filter:drop-shadow(0 0 10px rgba(255,255,255,0.4))"/></g>', "tr")

def house(s, x, gy=GY):
    return s.raw(f'<g id="@ID@" style="opacity:0"><path d="M {x - 60} {gy} V {gy - 90} L {x} {gy - 150} L {x + 60} {gy - 90} V {gy} Z M {x - 16} {gy} V {gy - 45} H {x + 16} V {gy}" '
                 f'fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/><rect x="{x + 22}" y="{gy - 82}" width="22" height="22" fill="{GOLD}" opacity="0.8"/></g>', "hs")

OTHER = "#8a8f98"

def mirror(s, cx, gy=GY, w=230, h=430, op=1):
    x0, y0 = cx - w / 2, gy - h
    sheen = "".join(f'<line x1="{x0 + 20 + k * 40}" y1="{y0 + 20}" x2="{x0 + 70 + k * 40}" y2="{y0 + 110}" stroke="#ffffff22" stroke-width="6"/>' for k in range(3))
    return s.raw(f'<g id="@ID@" style="opacity:{op}"><rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="6" fill="#ffffff08" stroke="#fff" stroke-width="4" '
                 f'style="filter:drop-shadow(0 0 14px rgba(255,255,255,0.35))"/>{sheen}</g>', "mr")

def vs(s, x, y, op=0):
    return s.raw(f'<g id="@ID@" style="opacity:{op}"><circle cx="{x}" cy="{y}" r="42" fill="#0b0f15" stroke="#fff" stroke-width="3"/>'
                 f'<text x="{x}" y="{y + 11}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" fill="#fff">VS</text></g>', "vs")

def ring(s, x0=130, x1=950, gy=GY, op=1):
    ropes = "".join(f'<line x1="{x0}" y1="{gy - 90 - k * 70}" x2="{x1}" y2="{gy - 90 - k * 70}" stroke="#ffffffa0" stroke-width="3"/>' for k in range(3))
    posts = f'<rect x="{x0 - 10}" y="{gy - 260}" width="20" height="260" fill="#fff"/><rect x="{x1 - 10}" y="{gy - 260}" width="20" height="260" fill="#fff"/>'
    return s.raw(f'<g id="@ID@" style="opacity:{op}">{ropes}{posts}<rect x="{x0 - 30}" y="{gy}" width="{x1 - x0 + 60}" height="16" fill="#ffffff30"/></g>', "rg")

def xmark(s, x, y, r=60, col=RED):
    return s.path(f"M {x - r} {y - r} L {x + r} {y + r} M {x + r} {y - r} L {x - r} {y + r}", col, 7)

# 1  every profitable trader was once alone, believing it would work
s = S(0, A("when") - 0.05, first=True)
s.label(540, 560, "ALONE AT FIRST", 30, LBL, 1)
mt = s.path("M 420 1240 L 520 1120 L 580 1160 L 660 1010 L 720 1060 L 820 820 L 880 900 L 1000 1240", "#ffffffa0", 4, drawn=True)
s.raw(f'<g id="@ID@"><line x1="820" y1="820" x2="820" y2="700" stroke="{GOLD}" stroke-width="4"/><path d="M 820 702 L 880 722 L 820 742 Z" fill="{GOLD}"/></g>')
s.label(820, 670, "PROFITABLE", 28, GOLD, 1, 800, 0.12)
s.spot(200, 0.6)
s.fig(200, 1.0)
s.label(200, 1300, "YOU, AT THE START", 28, GREY, 1, 700, 0.08)
orb = s.raw(f'<circle id="@ID@" cx="262" cy="1120" r="16" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 18px {GOLD})"/>', "c")
s.pop(orb, A("believing"), 0.4, 0.2, "50% 50%"); cue(A("believing"), "swell_1", -20)

# 2-3  people judge your chances by what you've made; nothing yet, nothing to believe in
s = S(A("when") - 0.05, A("spend") - 0.4)
s.label(540, 560, "HOW PEOPLE JUDGE YOU", 30, LBL, 1)
bd = s.path(rrect(220, 650, 640, 230, 20), WHITE, 3); s.draw(bd, A("when"), 0.5)
s.label(260, 705, "WHAT YOU'VE MADE", 28, LBL, 0, 800, 0.15, "start"); s.fade(s.items[-1].split('"')[1], A("when") + 0.3, 0.3)
z = s.label(540, 830, "$0", 90, WHITE, 0, 800, 0.02); s.pop(z, A("made", 1), 0.4, 0.5, "50% 50%"); cue(A("made", 1), "land-light_1", -18)
mg = s.raw('<g id="@ID@" style="opacity:0"><circle cx="760" cy="770" r="40" fill="none" stroke="#fff" stroke-width="5"/><line x1="790" y1="800" x2="830" y2="840" stroke="#fff" stroke-width="8" stroke-linecap="round"/></g>', "mg")
s.pop(mg, A("judge"), 0.35, 0.5, "50% 50%")
y2 = s.fig(200, 1.0); s.pop(y2, A("when"), 0.4)
for k, x in enumerate([560, 690, 820, 950]):
    f = s.fig(x, 0.75, "#cfd3da", 0.85); s.pop(f, A("people") + k * 0.08, 0.35)
rb = s.label(540, 960, "REASONS TO BELIEVE: 0", 30, GREY, 0, 800, 0.1); s.fade(rb, A("believe", 1) - 0.6, 0.4); cue(A("believe", 1), "tick_2", -20)

# 4  months of backtesting, journaling, a demo, without a single dollar; everyone else moving ahead
s = S(A("spend") - 0.4, A("sooner") - 0.05)
s.label(540, 560, "MONTHS IN", 30, LBL, 1)
s.raw('<g id="@ID@"><rect x="140" y="1100" width="360" height="14" fill="#fff" opacity="0.85"/>'
      '<line x1="160" y1="1114" x2="160" y2="1240" stroke="#fff" stroke-width="5" opacity="0.7"/><line x1="480" y1="1114" x2="480" y2="1240" stroke="#fff" stroke-width="5" opacity="0.7"/>'
      '<rect x="300" y="980" width="160" height="110" rx="8" fill="#0b1220" stroke="#fff" stroke-width="3" style="filter:drop-shadow(0 0 18px rgba(120,180,255,0.6))"/>'
      '<line x1="380" y1="1090" x2="380" y2="1100" stroke="#fff" stroke-width="4"/></g>')
y4 = s.fig(240, 0.85, gy=1180)
tl(f'tl.to("#{y4}", {{y: -4, duration: 0.22, yoyo: true, repeat: 15, ease: "sine.inOut"}}, {A("spend"):.3f});')
for k, (txt, w_) in enumerate([("BACKTEST", "back"), ("JOURNAL", "journaling"), ("DEMO", "demo")]):
    p = s.pill(170 + k * 150, 880 - (k % 2) * 70, txt, "#2a2f38", WHITE, 28); s.pop(p, A(w_) - 0.05, 0.3, 0.5, "50% 50%"); cue(A(w_), "pop_" + str(k + 1), -20)
for k in range(4):
    c = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="800" y="620" width="190" height="100" rx="12" fill="#11151b" stroke="#fff" stroke-width="3"/>'
              f'<text x="895" y="684" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" fill="#fff">MONTH {[1, 2, 4, 6][k]}</text></g>', "mo")
    ta = A("months") + k * 0.45
    tl(f'tl.fromTo("#{c}", {{opacity: 0, y: -25}}, {{opacity: 1, y: 0, duration: 0.2, immediateRender: false}}, {ta:.3f});')
    if k < 3: tl(f'tl.set("#{c}", {{opacity: 0}}, {ta + 0.45:.3f});')
ea = s.pill(320, 1310, "EARNED: $0", "#2a2f38", WHITE, 28); s.pop(ea, A("dollar") - 0.1, 0.3, 0.5, "50% 50%"); cue(A("dollar"), "land-light_1", -18)
st = s.path("M 600 1240 H 690 V 1170 H 780 V 1100 H 870 V 1030 H 980", "#ffffff80", 3); s.draw(st, A("everyone") - 0.2, 0.5)
for k, (x, y) in enumerate([(640, 1240), (730, 1170), (820, 1100)]):
    f = s.fig(x, 0.5, "#cfd3da", 0.85, gy=y); s.pop(f, A("everyone") + k * 0.1, 0.35)
    s.walk(f, A("ahead") - 0.3, 90, 0.8)
s.label(800, 1310, "MOVING AHEAD", 28, GREY, 0, 700, 0.1); s.fade(s.items[-1].split('"')[1], A("ahead") - 0.2, 0.35)

# 5  someone asks why you're still wasting your time
s = S(A("sooner") - 0.05, A("hard") - 0.5)
y5 = s.fig(540, 1.0); s.pop(y5, A("sooner"), 0.4)
for k, (x, txt, px, py) in enumerate([(140, "STILL ON THIS?", 200, 960), (290, "GET A REAL JOB", 330, 860), (790, "WASTING TIME?", 770, 960), (940, "IT'S GAMBLING", 870, 860)]):
    f = s.fig(x, 0.75, "#9aa0a8", 0.8, False); s.pop(f, A("sooner") + k * 0.1, 0.35)
    p = s.pill(px, py, txt, "#2a2f38", WHITE, 28); s.pop(p, A("asks") + k * 0.3, 0.3, 0.5, "50% 50%"); cue(A("asks") + k * 0.3, "tick_" + str(k % 3 + 1), -20)

# 6  you can't prove them wrong yet: no payouts, no track record, just a plan and a belief
s = S(A("hard") - 0.5, A("this") - 0.05)
s.label(540, 560, "NO PROOF YET", 30, LBL, 1)
y6 = s.fig(330, 1.0); s.pop(y6, A("hard") - 0.45, 0.4)
pr = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="230" y="760" width="200" height="140" rx="10" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="10 8"/>'
           f'<line x1="330" y1="900" x2="330" y2="1050" stroke="#fff" stroke-width="3"/>'
           f'<text x="330" y="845" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" letter-spacing="0.12em" fill="#9aa0a8">PROOF?</text></g>', "pf")
s.pop(pr, A("prove"), 0.35, 0.5, "50% 50%")
for k, (txt, w_) in enumerate([("PAYOUTS", "payouts"), ("TRACK RECORD", "track")]):
    y = 760 + k * 100
    p = s.pill(770, y, txt, "#2a2f38", WHITE, 28); s.pop(p, A(w_) - 0.1, 0.3, 0.5, "50% 50%")
    hw = len(txt) * 28 * 0.37 + 30
    sl = s.path(f"M {770 - hw} {y} H {770 + hw}", RED, 5); s.draw(sl, A(w_) + 0.3, 0.25); cue(A(w_) + 0.3, "click_" + str(k + 1), -20)
pl = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="700" y="950" width="140" height="170" rx="8" fill="#11151b" stroke="{GOLD}" stroke-width="3"/>'
           + "".join(f'<line x1="720" y1="{990 + j * 30}" x2="{820 - (j % 2) * 30}" y2="{990 + j * 30}" stroke="{GOLD}" stroke-width="3"/>' for j in range(4)) +
           f'<text x="770" y="1160" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" fill="{GOLD}">PLAN</text></g>', "pn")
s.pop(pl, A("plan"), 0.35, 0.5, "50% 50%"); cue(A("plan"), "pop_2", -18)
orb6 = s.raw(f'<circle id="@ID@" cx="392" cy="1110" r="18" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 22px {GOLD})"/>', "c")
s.pop(orb6, A("belief"), 0.4, 0.2, "50% 50%"); cue(A("belief"), "bell_E5", -18)

# 7  believing in your process matters more than anyone's approval
s = S(A("this") - 0.05, A("because", 1) - 0.35)
s.label(540, 560, "WHAT MATTERS MORE", 30, LBL, 1)
b1 = s.raw(f'<rect id="@ID@" x="270" y="700" width="120" height="540" rx="12" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 18px rgba(232,194,106,0.5))"/>', "r")
tl(f'tl.fromTo("#{b1}", {{opacity: 1, scaleY: 0, transformOrigin: "50% 100%"}}, {{opacity: 1, scaleY: 1, duration: 0.9, ease: "power2.out", immediateRender: false}}, {A("believing", 2) if sum(1 for w in words if _n(w["text"]) == "believing") > 1 else A("process") - 0.6:.3f});')
b2 = s.raw(f'<rect id="@ID@" x="690" y="1110" width="120" height="130" rx="12" fill="#8a8f98" style="opacity:0"/>', "r")
tl(f'tl.fromTo("#{b2}", {{opacity: 1, scaleY: 0, transformOrigin: "50% 100%"}}, {{opacity: 1, scaleY: 1, duration: 0.6, ease: "power2.out", immediateRender: false}}, {A("approval") - 0.1:.3f});')
gt = s.label(540, 1050, ">", 110, WHITE, 0, 800, 0); s.pop(gt, A("more") if "more" in [_n(w["text"]) for w in words] else A("approval"), 0.35, 0.5, "50% 50%")
l1 = s.label(330, 1300, "YOUR PROCESS", 28, GOLD, 0, 800, 0.1); s.fade(l1, A("process"), 0.35); cue(A("process"), "swell_2", -20)
l2 = s.label(750, 1300, "APPROVAL", 28, GREY, 0, 800, 0.1); s.fade(l2, A("approval"), 0.35)

# 8  not every strategy works; nobody can promise an edge before you do the work
s = S(A("because", 1) - 0.35, A("still", 2) - 0.35)
s.label(540, 560, "NO GUARANTEES", 30, LBL, 1)
stp = s.path("M 120 1240 H 240 V 1180 H 360 V 1120 H 480 V 1060 H 600 V 1000 H 650", WHITE, 3); s.draw(stp, A("because", 1), 0.6)
s.label(330, 1300, "THE WORK", 28, GREY, 0, 700, 0.15); s.fade(s.items[-1].split('"')[1], A("work", 3) - 0.2, 0.35)
bx = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="680" y="900" width="260" height="340" rx="12" fill="#0b0f15" stroke="#fff" stroke-width="4"/>'
           f'<text x="810" y="1100" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="110" fill="{GOLD}">?</text>'
           f'<text x="810" y="960" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" letter-spacing="0.2em" fill="#fff">EDGE</text></g>', "bx")
s.pop(bx, A("strategy") - 0.1, 0.4, 0.6, "50% 100%")
gu = s.pill(810, 820, "GUARANTEED", WHITE, "#111", 28); s.pop(gu, A("promise") - 0.1, 0.3, 0.5, "50% 50%")
gx = s.path("M 670 820 H 950", RED, 6); s.draw(gx, A("promise") + 0.35, 0.25); cue(A("promise") + 0.35, "land-light_1", -18)
y8 = s.fig(180, 0.8)
tl(f'tl.to("#{y8}", {{keyframes: [{{x: 120, y: -60}}, {{x: 240, y: -120}}, {{x: 360, y: -180}}, {{x: 440, y: -240}}], duration: 1.6, ease: "none"}}, {A("work", 3) - 0.3:.3f});')
cue(A("find"), "bell_G5", -20)

# 9  spot your mistakes, adjust your rules, learn from what isn't working
s = S(A("still", 2) - 0.35, A("but", 2) - 0.05)
s.label(540, 560, "THE LOOP", 30, LBL, 1)
CX9, CY9, R9 = 540, 950, 190
ring9 = s.path(f"M {CX9 - R9} {CY9} a {R9} {R9} 0 1 0 {2 * R9} 0 a {R9} {R9} 0 1 0 {-2 * R9} 0", "#ffffff60", 3, extra='stroke-dasharray="10 10"', drawn=True)
nodes = [("SPOT", -90, "spot"), ("ADJUST", 30, "adjust"), ("LEARN", 150, "learn")]
for k, (lab, ang, w_) in enumerate(nodes):
    a = math.radians(ang); x, y = CX9 + math.cos(a) * R9, CY9 + math.sin(a) * R9
    p = s.pill(x, y, lab, GOLD if k == 2 else WHITE, "#111", 30); s.pop(p, A(w_) - 0.05, 0.35, 0.5, "50% 50%"); cue(A(w_), "pop_" + str(k + 1), -20)
jr = s.raw('<g id="@ID@" style="opacity:0"><rect x="490" y="890" width="100" height="125" rx="8" fill="none" stroke="#fff" stroke-width="3"/>'
           + "".join(f'<line x1="505" y1="{920 + j * 24}" x2="{575 - (j % 2) * 20}" y2="{920 + j * 24}" stroke="#ffffff90" stroke-width="3"/>' for j in range(4)) + '</g>', "jr")
s.fade(jr, A("still", 2), 0.4)
dot9 = s.raw(f'<circle id="@ID@" cx="{CX9}" cy="{CY9 - R9}" r="10" fill="{GOLD}" style="filter:drop-shadow(0 0 10px {GOLD})"/>', "c")
tl(f'tl.fromTo("#{dot9}", {{rotation: 0}}, {{rotation: 720, svgOrigin: "{CX9} {CY9}", duration: {A("but", 2) - A("still", 2):.3f}, ease: "none", immediateRender: false}}, {A("still", 2) - 0.3:.3f});')

# 10  needing everyone to believe first means waiting for permission forever
s = S(A("but", 2) - 0.05, A("sometimes") - 0.05)
s.label(540, 560, "WAITING", 30, LBL, 1)
dr = s.raw(f'<g id="@ID@"><rect x="700" y="940" width="170" height="300" rx="6" fill="#05070a" stroke="#fff" stroke-width="4"/><circle cx="845" cy="1095" r="7" fill="#fff"/>'
           f'<text x="785" y="910" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" letter-spacing="0.2em" fill="#fff">START</text></g>', "dr")
y10 = s.fig(500, 1.0); s.pop(y10, A("but", 2), 0.4)
for k, n in enumerate([3, 4]):
    c = s.pill(540, 760, f"PEOPLE WHO BELIEVE: {n} / 100", "#2a2f38", WHITE, 28)
    ta = A("need") if k == 0 else A("waiting") - 0.1
    tl(f'tl.fromTo("#{c}", {{opacity: 0, scale: 0.7, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)", immediateRender: false}}, {ta:.3f});')
    if k == 0: tl(f'tl.set("#{c}", {{opacity: 0}}, {A("waiting") - 0.1:.3f});')
    cue(ta, "tick_" + str(k + 1), -20)
wp = s.pill(500, 860, "WAITING FOR PERMISSION", WHITE, "#111", 28); s.pop(wp, A("permission") - 0.4, 0.35, 0.5, "50% 50%"); cue(A("permission"), "land-light_1", -18)

# 11  believe first, long before the chart gives you a reason to
s = S(A("sometimes") - 0.05, A("order") - 0.05)
bf = s.label(540, 700, "BELIEVE FIRST", 52, GOLD, 0, 800, 0.15); s.fade(bf, A("first") - 0.2, 0.5, y=14); cue(A("first"), "swell_2", -16)
gs = s.spot(300, 0, "232,194,106", 40, 180); s.fade(gs, A("sometimes"), 0.6)
y11 = s.fig(300, 1.05); s.pop(y11, A("sometimes"), 0.4)
fut = s.path("M 360 1150 L 470 1120 L 540 1135 L 640 1040 L 710 1060 L 830 920 L 960 860", "#e8c26a70", 4, extra='stroke-dasharray="12 12"', drawn=True)
tl(f'tl.fromTo("#{fut}", {{opacity: 0}}, {{opacity: 1, duration: 0.6, immediateRender: false}}, {A("long") if "long" in [_n(w["text"]) for w in words] else A("first") + 0.4:.3f});')
sol = s.path("M 360 1150 L 470 1120 L 540 1135 L 640 1040 L 710 1060 L 830 920 L 960 860", GOLD, 6); s.draw(sol, A("chart"), 1.0)
rs = s.label(780, 1300, "THE REASON COMES LATER", 28, GREY, 0, 700, 0.08); s.fade(rs, A("chart"), 0.4)

# 12  order the market (outro with handles; no end card)
s = S(A("order") - 0.05, TOTAL)
es = s.spot(540, 0, "232,194,106", 40, 230); s.fade(es, A("order"), 0.6)
em = s.raw('<image id="@ID@" href="assets/otm_emblem.png" x="390" y="900" width="300" height="291" style="opacity:0;filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>', "i")
s.pop(em, A("order"), 0.7, 0.6, "50% 50%"); cue(A("order"), "bell_A4", -16)
o1 = s.label(540, 1300, "ORDER THE MARKET", 32, GOLD, 0, 800, 0.3); s.fade(o1, A("order") + 0.3, 0.5)
o2 = s.label(540, 1360, "DON'T LET THE MARKET ORDER YOU", 28, WHITE, 0, 700, 0.12); s.fade(o2, A("don't"), 0.4)
o3 = s.pill(540, 1470, "FOLLOW FOR MORE", GOLD, "#111", 30); s.pop(o3, A("follow"), 0.4, 0.6, "50% 50%"); cue(A("follow"), "click-confirm_1", -16)
hx = 290
soc = s.raw(f'<g id="@ID@" style="opacity:0">'
            f'<rect x="{hx}" y="1548" width="36" height="36" rx="10" fill="none" stroke="#fff" stroke-width="3"/>'
            f'<circle cx="{hx + 18}" cy="1566" r="8.5" fill="none" stroke="#fff" stroke-width="3"/><circle cx="{hx + 28}" cy="1556" r="2.4" fill="#fff"/>'
            f'<text x="{hx + 48}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@fxzuez_28</text>'
            f'<path d="M {hx + 322} 1546 V 1574 A 9 9 0 1 1 {hx + 313} 1565 M {hx + 322} 1546 Q {hx + 326} 1557 {hx + 338} 1558" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>'
            f'<text x="{hx + 348}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@zuez_28</text></g>', "so")
disc = s.label(540, 1650, "EDUCATIONAL ONLY · NOT FINANCIAL ADVICE", 28, GREY, 0, 600, 0.12)
s.fade(soc, A("don't") + 0.6, 0.5, y=12)
s.fade(disc, A("don't") + 0.9, 0.5)

# ------------------------------------------------------------------ end card, dust, ground, emblem
tl(f'tl.to("#mark", {{opacity: 0, duration: 0.3}}, {A("order") - 0.2:.3f});')
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
    <div id="root" data-composition-id="otm-believe" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-believe-audio" class="clip" src="assets/audio/mix_believe.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-believe"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
