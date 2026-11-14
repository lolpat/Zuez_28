"""OTM "Second Chance" (normal pace): a glowing-figure explainer (same system as otm-circle / otm-anyway / otm-know / otm-noise). Voice only, no music. White soft-glow figures on a dashed ground line, spotlights, small
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

def ticket(s, x, y, op=0, sc=1.0):
    w, h = 150 * sc, 70 * sc
    return s.raw(f'<g id="@ID@" style="opacity:{op}"><rect x="{x - w / 2:.0f}" y="{y - h / 2:.0f}" width="{w:.0f}" height="{h:.0f}" rx="10" fill="{GOLD}" '
                 f'style="filter:drop-shadow(0 0 12px rgba(232,194,106,0.6))"/><circle cx="{x - w / 2:.0f}" cy="{y}" r="{10 * sc:.0f}" fill="#000"/><circle cx="{x + w / 2:.0f}" cy="{y}" r="{10 * sc:.0f}" fill="#000"/>'
                 f'<text x="{x}" y="{y + 10 * sc:.0f}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="{max(28, 28 * sc):.0f}" fill="#111">2ND</text></g>', "tk")

def circle_icon(s, x, y, kind, col=GOLD):
    base = f'<circle cx="{x}" cy="{y}" r="85" fill="none" stroke="{col}" stroke-width="3" stroke-dasharray="10 8"/>'
    if kind == "bird":
        ic = f'<path d="M {x - 50} {y + 10} Q {x - 25} {y - 20} {x} {y + 8} Q {x + 25} {y - 20} {x + 50} {y + 10} M {x - 30} {y + 40} Q {x - 15} {y + 25} {x} {y + 40} Q {x + 15} {y + 25} {x + 30} {y + 40}" fill="none" stroke="#fff" stroke-width="4"/>'
    elif kind == "bars":
        ic = "".join(f'<rect x="{x - 48 + i * 26}" y="{y + 40 - (20 + i * 18)}" width="18" height="{20 + i * 18}" fill="#fff"/>' for i in range(4))
    else:
        ic = (f'<circle cx="{x}" cy="{y - 38}" r="16" fill="none" stroke="{GOLD}" stroke-width="4" stroke-dasharray="6 5"/>'
              f'<path d="M {x - 26} {y + 45} V {y + 5} Q {x - 26} {y - 18} {x} {y - 18} Q {x + 26} {y - 18} {x + 26} {y + 5} V {y + 45}" fill="none" stroke="{GOLD}" stroke-width="4" stroke-dasharray="6 5"/>')
    return s.raw(f'<g id="@ID@" style="opacity:0">{base}{ic}</g>', "ci")

# 1  everyone deserves a second chance, even you
s = S(0, A("remember", 1) - 0.05, first=True)
s.label(540, 560, "SECOND CHANCE", 30, LBL, 1)
for k, x in enumerate([150, 300, 780, 930]):
    s.fig(x, 0.8, "#cfd3da", 0.85)
    t = ticket(s, x, 980, 1 if k < 2 else 0, 0.8)
    if k >= 2: s.pop(t, A("chance", 1) - 0.2 + (k - 2) * 0.12, 0.3, 0.5, "50% 50%")
sp1 = s.spot(540, 0, "232,194,106"); s.fade(sp1, A("even", 1) - 0.1, 0.4)
y1 = s.fig(540, 1.05)
yt = ticket(s, 540, 950, 0, 1.1); s.pop(yt, A("even", 1) + 0.1, 0.4, 0.4, "50% 50%"); cue(A("even", 1) + 0.1, "bell_E5", -18)
s.label(540, 1300, "EVEN YOU", 28, GOLD, 0, 800, 0.15); s.fade(s.items[-1].split('"')[1], A("even", 1) + 0.1, 0.35)

# 2  the promise you made when you opened your first chart
s = S(A("remember", 1) - 0.05, A("freedom") - 0.4)
s.label(540, 560, "DAY ONE", 30, LBL, 1)
s.raw('<g id="@ID@"><rect x="380" y="1100" width="360" height="14" fill="#fff" opacity="0.85"/>'
      '<line x1="400" y1="1114" x2="400" y2="1240" stroke="#fff" stroke-width="5" opacity="0.7"/><line x1="720" y1="1114" x2="720" y2="1240" stroke="#fff" stroke-width="5" opacity="0.7"/>'
      '<rect x="530" y="980" width="170" height="110" rx="8" fill="#0b1220" stroke="#fff" stroke-width="3" style="filter:drop-shadow(0 0 18px rgba(120,180,255,0.6))"/>'
      '<line x1="615" y1="1090" x2="615" y2="1100" stroke="#fff" stroke-width="4"/></g>')
fc = s.path("M 545 1070 L 575 1055 L 600 1062 L 630 1030 L 655 1040 L 685 1000", GOLD, 4); s.draw(fc, A("first") - 0.2, 0.8)
y2 = s.fig(470, 0.85, gy=1180); s.pop(y2, A("remember", 1), 0.4)
pr = s.raw(f'<g id="@ID@" style="opacity:0"><path d="M 400 740 H 680 Q 700 740 700 760 V 860 Q 700 880 680 880 H 400 Q 380 880 380 860 V 760 Q 380 740 400 740 Z" fill="#11151b" stroke="{GOLD}" stroke-width="3"/>'
           f'<text x="540" y="822" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" letter-spacing="0.2em" fill="{GOLD}">PROMISE</text></g>', "pm")
s.pop(pr, A("promise") - 0.05, 0.4, 0.5, "50% 50%"); cue(A("promise"), "swell_1", -20)

# 3-4  freedom, the account you imagined growing, the trader you swore you'd become; how badly you wanted it
s = S(A("freedom") - 0.4, A("why") - 0.6)
s.label(540, 560, "WHAT YOU WANTED", 30, LBL, 1)
y3 = s.fig(540, 1.0); s.pop(y3, A("freedom") - 0.35, 0.4)
dreams = [(230, "bird", ["FREEDOM"], "freedom"), (540, "bars", ["A GROWING", "ACCOUNT"], "growing"), (850, "future", ["THE TRADER", "YOU SWORE"], "swore")]
ds = []
for k, (x, kind, lab, w_) in enumerate(dreams):
    c = circle_icon(s, x, 790, kind); s.pop(c, A(w_) - 0.3, 0.45, 0.5, "50% 50%"); ds.append(c)
    for li, line in enumerate(lab):
        lb = s.label(x, 915 + li * 36, line, 28, WHITE, 0, 800, 0.06); s.fade(lb, A(w_) - 0.2, 0.35); ds.append(lb)
    ln = s.path(f"M 540 1040 L {x} 960", "#e8c26a60", 2); s.draw(ln, A(w_) - 0.3, 0.35); ds.append(ln)
    cue(A(w_) - 0.3, "bell_" + ["G4", "C5", "E5"][k], -22)
gl = s.raw(f'<ellipse id="@ID@" cx="540" cy="800" rx="460" ry="150" fill="url(#gl3)" style="opacity:0"/>', "e")
s.items.insert(0, f'<defs><radialGradient id="gl3"><stop offset="0" stop-color="{GOLD}" stop-opacity="0.25"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
s.fade(gl, A("badly") - 0.3, 0.6); cue(A("badly"), "swell_2", -20)

# 5  so why did you give up on it
s = S(A("why") - 0.6, A("because", 1) - 0.05)
y5 = s.fig(540, 1.0, "#9aa0a8", 0.8, False); s.pop(y5, A("why") - 0.55, 0.4)
fallen = []
for k, (x, kind) in enumerate([(230, "bird"), (540, "bars"), (850, "future")]):
    c = circle_icon(s, x, 790, kind, "#ffffff70")
    tl(f'tl.set("#{c}", {{opacity: 0.9}}, {A("why") - 0.6:.3f});')
    tl(f'tl.to("#{c}", {{y: 380, opacity: 0, duration: 0.9, ease: "power2.in"}}, {A("give", 1) + k * 0.12:.3f});')
cue(A("give", 1), "whoosh-long_1", -22)
wq = s.label(540, 700, "WHY DID YOU STOP?", 40, WHITE, 0, 800, 0.12); s.fade(wq, A("why") - 0.3, 0.4, y=12)

# 6  because you blew one account, a strategy failed, you're not where you thought you'd be
s = S(A("because", 1) - 0.05, A("look") - 0.05)
s.label(540, 560, "THE REASONS", 30, LBL, 1)
y6 = s.fig(540, 0.9, "#9aa0a8", 0.8, False); s.pop(y6, A("because", 1), 0.4)
reasons = [(230, "BLOWN ACCOUNT", A("blew")), (540, "STRATEGY FAILED", A("strategy")), (850, "NOT THERE YET", A("now") - 0.6)]
for k, (x, lab, t) in enumerate(reasons):
    if k == 0:
        ic = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="{x - 75}" y="740" width="150" height="110" rx="12" fill="{RED}"/><text x="{x}" y="808" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" fill="#fff">$0</text></g>')
    elif k == 1:
        ic = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="{x - 80}" y="740" width="160" height="110" rx="12" fill="none" stroke="#fff" stroke-width="3"/>'
                   f'<path d="M {x - 60} 765 L {x - 25} 790 L {x} 780 L {x + 30} 820 L {x + 60} 835" fill="none" stroke="{RED}" stroke-width="4"/></g>')
    else:
        ic = s.raw(f'<g id="@ID@" style="opacity:0"><path d="M {x} 860 C {x - 50} 800 {x - 50} 750 {x} 740 C {x + 50} 750 {x + 50} 800 {x} 860 Z" fill="none" stroke="#fff" stroke-width="4"/>'
                   f'<circle cx="{x}" cy="785" r="14" fill="#fff"/></g>')
    s.pop(ic, t - 0.1, 0.35, 0.5, "50% 50%")
    lb = s.label(x, 900, lab, 28, WHITE, 0, 800, 0.06); s.fade(lb, t, 0.3)
    cue(t, "land-light_1" if k == 0 else "tick_" + str(k), -18)

# 7  look at the market: thousands of setups, sessions, opportunities you haven't imagined
s = S(A("look") - 0.05, A("how", 2) - 0.05)
s.label(540, 560, "LOOK AT THE MARKET", 30, LBL, 1)
r7 = random.Random(7)
cands = []
for i in range(60):
    x = 150 + (i % 15) * 54; y = 700 + (i // 15) * 70; h = r7.uniform(14, 44); col = GOLD if r7.random() < 0.35 else "#ffffffb0"
    cands.append(s.raw(f'<g id="@ID@" style="opacity:0"><line x1="{x}" y1="{y - h / 2 - 8:.0f}" x2="{x}" y2="{y + h / 2 + 8:.0f}" stroke="{col}" stroke-width="2"/>'
                       f'<rect x="{x - 7}" y="{y - h / 2:.0f}" width="14" height="{h:.0f}" fill="{col}"/></g>', "cd"))
for i, c in enumerate(cands): tl(f'tl.fromTo("#{c}", {{opacity: 0}}, {{opacity: 1, duration: 0.15, immediateRender: false}}, {A("thousands") + i * 0.02:.3f});')
cue(A("thousands"), "pop_2", -20)
sl = s.label(540, 1010, "SETUPS YOU'VE NEVER TRADED", 28, WHITE, 0, 800, 0.08); s.fade(sl, A("setups"), 0.3)
ss = s.label(540, 1060, "SESSIONS YOU'VE NEVER STUDIED", 28, LBL, 0, 700, 0.08); s.fade(ss, A("sessions"), 0.3)
so = s.label(540, 1110, "OPPORTUNITIES YOU CAN'T SEE YET", 28, GOLD, 0, 800, 0.08); s.fade(so, A("opportunities"), 0.3); cue(A("opportunities"), "bell_G5", -20)
y7 = s.fig(940, 0.7); s.pop(y7, A("look"), 0.4)

# 8  best trades behind you? you haven't seen what the market still has to offer
s = S(A("how", 2) - 0.05, A("maybe") - 0.05)
s.label(540, 560, "BEHIND YOU? OR AHEAD?", 30, LBL, 1)
s.path("M 80 960 H 1000", "#ffffff40", 3, drawn=True)
for x in (140, 230, 320):
    s.raw(f'<circle id="@ID@" cx="{x}" cy="960" r="12" fill="#8a8f98"/>')
s.label(230, 1010, "BEHIND", 28, GREY, 0, 700, 0.15); s.fade(s.items[-1].split('"')[1], A("behind") - 0.1, 0.3)
y8 = s.fig(440, 0.9); s.pop(y8, A("how", 2), 0.4)
for k, x in enumerate(range(560, 1000, 60)):
    d = s.raw(f'<circle id="@ID@" cx="{x}" cy="960" r="13" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 10px {GOLD})"/>', "c")
    s.pop(d, A("offer") - 0.9 + k * 0.1, 0.25, 0.3, "50% 50%")
ah = s.label(780, 1010, "STILL AHEAD", 28, GOLD, 0, 800, 0.15); s.fade(ah, A("offer") - 0.4, 0.35); cue(A("offer") - 0.4, "swell_1", -20)

# 9  maybe it's time to give that plan another chance
s = S(A("maybe") - 0.05, A("open") - 0.05)
pl = s.raw(f'<g id="@ID@" data-layout-ignore><rect x="430" y="760" width="220" height="280" rx="10" fill="#11151b" stroke="{GOLD}" stroke-width="4"/>'
           + "".join(f'<line x1="460" y1="{810 + j * 40}" x2="{620 - (j % 2) * 40}" y2="{810 + j * 40}" stroke="{GOLD}" stroke-width="4"/>' for j in range(5)) +
           f'<text x="540" y="1090" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" letter-spacing="0.2em" fill="{GOLD}">PLAN</text></g>', "pl")
tl(f'tl.fromTo("#{pl}", {{scale: 0.35, rotation: -25, opacity: 0.5, transformOrigin: "50% 50%"}}, {{scale: 1, rotation: 0, opacity: 1, duration: 0.9, ease: "back.out(1.4)", immediateRender: false}}, {A("plan") - 0.2:.3f});')
tl(f'tl.set("#{pl}", {{scale: 0.35, rotation: -25, opacity: 0.5, transformOrigin: "50% 50%"}}, {A("maybe") - 0.05:.3f});')
cue(A("plan") - 0.2, "whoosh-short_2", -20)
ac = s.label(540, 650, "ANOTHER CHANCE", 40, GOLD, 0, 800, 0.15); s.fade(ac, A("another"), 0.4, y=12); cue(A("another"), "bell_C5", -20)

# 10  open the journal, backtest the abandoned setup, become the trader you believed you could be
s = S(A("open") - 0.05, A("don't", 1) - 0.35)
s.label(540, 560, "START AGAIN", 30, LBL, 1)
bk = s.raw('<g id="@ID@" style="opacity:0"><path d="M 230 760 C 200 745 160 745 130 752 V 850 C 160 843 200 843 230 858 C 260 843 300 843 330 850 V 752 C 300 745 260 745 230 760 Z M 230 760 V 858" '
           'fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/></g>', "bk")
s.pop(bk, A("open"), 0.35, 0.5, "50% 50%"); cue(A("open"), "pop_1", -20)
s.label(230, 910, "JOURNAL", 28, WHITE, 0, 800, 0.15); s.fade(s.items[-1].split('"')[1], A("journal"), 0.3)
r10 = random.Random(10)
for i in range(7):
    x = 450 + i * 28; h = r10.uniform(20, 60); y = 820 - i * 8
    c = s.raw(f'<g id="@ID@" style="opacity:0"><line x1="{x}" y1="{y - h / 2 - 10:.0f}" x2="{x}" y2="{y + h / 2 + 10:.0f}" stroke="{GOLD}" stroke-width="2"/><rect x="{x - 8}" y="{y - h / 2:.0f}" width="16" height="{h:.0f}" fill="{GOLD}"/></g>', "cd")
    s.pop(c, A("backtest") - 0.1 + i * 0.07 if "backtest" in [_n(w["text"]) for w in words] else A("setup") - 0.3 + i * 0.07, 0.2, 0.4, "50% 50%")
s.label(540, 910, "BACKTEST", 28, WHITE, 0, 800, 0.15); s.fade(s.items[-1].split('"')[1], A("setup"), 0.3)
fut = circle_icon(s, 850, 800, "future"); s.pop(fut, A("become", 2) - 0.1, 0.4, 0.5, "50% 50%")
y10 = s.fig(540, 1.0); s.pop(y10, A("open"), 0.4)
s.walk(y10, A("become", 2), 310, 1.2)
gold10 = s.fig(850, 1.0, GOLD, 0); s.fade(gold10, A("believed"), 0.5); cue(A("believed"), "swell_2", -18)

# 11  you don't have to start over as the trader you were; start again with what your losses taught you
s = S(A("don't", 1) - 0.35, A("give", 3) - 0.05)
s.label(540, 560, "NOT FROM ZERO", 30, LBL, 1)
s.raw('<g id="@ID@"><line x1="200" y1="1240" x2="200" y2="1050" stroke="#fff" stroke-width="4"/><text x="200" y="1030" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" letter-spacing="0.2em" fill="#fff">START</text></g>')
y11 = s.fig(300, 1.0); s.pop(y11, A("don't", 1) - 0.3, 0.4)
bp = s.raw(f'<rect id="@ID@" x="330" y="1110" width="50" height="70" rx="12" fill="{GOLD}" style="opacity:0"/>', "bp")
s.pop(bp, A("start", 2), 0.35, 0.5, "50% 50%")
for k, x in enumerate([580, 770, 960]):
    lc = s.pill(x, 900, "LOSS", RED, WHITE, 28); s.pop(lc, A("start", 2) - 0.3 + k * 0.15, 0.3, 0.5, "50% 50%")
    ls = s.pill(x, 900, "LESSON", GOLD, "#111", 28)
    tb = A("losses") + 0.1 + k * 0.2
    tl(f'tl.set("#{lc}", {{opacity: 0}}, {tb:.3f});')
    tl(f'tl.fromTo("#{ls}", {{opacity: 0, scale: 0.6, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)", immediateRender: false}}, {tb:.3f});')
    tl(f'tl.to("#{ls}", {{x: {355 - x}, y: 245, scale: 0.3, opacity: 0, duration: 0.6, ease: "power2.in"}}, {max(A("taught") + 0.1 + k * 0.15, tb + 0.32):.3f});')
    cue(tb, "pop_" + str(k + 1), -20)

# 12  give yourself a second chance; your equity curve isn't finished yet
s = S(A("give", 3) - 0.05, A("order") - 0.05)
s.path("M 120 700 V 1180 H 960", "#ffffff50", 2, drawn=True)
eq = s.path("M 130 1000 L 230 940 L 300 1080 L 360 1150 L 430 1100 L 520 1060 L 610 980", WHITE, 5, drawn=True)
nx = s.path("M 610 980 L 700 930 L 780 950 L 870 840 L 950 780", GOLD, 6); s.draw(nx, A("equity"), 1.0)
tip = s.raw(f'<circle id="@ID@" cx="950" cy="780" r="14" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 12px {GOLD})"/>', "c")
s.pop(tip, A("finished") - 0.1, 0.35, 0.3, "50% 50%"); cue(A("finished"), "bell_E5", -18)
t12 = ticket(s, 300, 780, 0, 1.2); s.pop(t12, A("chance", 3) - 0.2, 0.4, 0.4, "50% 50%")
nf = s.label(780, 680, "NOT FINISHED", 40, GOLD, 0, 800, 0.15); s.fade(nf, A("finished") - 0.3, 0.4, y=12)

# 13  order the market (outro with handles; no end card)
s = S(A("order") - 0.05, TOTAL)
es = s.spot(540, 0, "232,194,106", 40, 230); s.fade(es, A("order"), 0.6)
em = s.raw('<image id="@ID@" href="assets/otm_emblem.png" x="390" y="900" width="300" height="291" style="opacity:0;filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>', "i")
s.pop(em, A("order"), 0.7, 0.6, "50% 50%"); cue(A("order"), "bell_A4", -16)
o1 = s.label(540, 1300, "ORDER THE MARKET", 32, GOLD, 0, 800, 0.3); s.fade(o1, A("order") + 0.3, 0.5)
o2 = s.label(540, 1360, "DON'T LET THE MARKET ORDER YOU", 28, WHITE, 0, 700, 0.12); s.fade(o2, A("don't", 2), 0.4)
o3 = s.pill(540, 1470, "FOLLOW FOR MORE", GOLD, "#111", 30); s.pop(o3, A("follow"), 0.4, 0.6, "50% 50%"); cue(A("follow"), "click-confirm_1", -16)
hx = 290
soc = s.raw(f'<g id="@ID@" style="opacity:0">'
            f'<rect x="{hx}" y="1548" width="36" height="36" rx="10" fill="none" stroke="#fff" stroke-width="3"/>'
            f'<circle cx="{hx + 18}" cy="1566" r="8.5" fill="none" stroke="#fff" stroke-width="3"/><circle cx="{hx + 28}" cy="1556" r="2.4" fill="#fff"/>'
            f'<text x="{hx + 48}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@fxzuez_28</text>'
            f'<path d="M {hx + 322} 1546 V 1574 A 9 9 0 1 1 {hx + 313} 1565 M {hx + 322} 1546 Q {hx + 326} 1557 {hx + 338} 1558" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>'
            f'<text x="{hx + 348}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@zuez_28</text></g>', "so")
disc = s.label(540, 1650, "EDUCATIONAL ONLY · NOT FINANCIAL ADVICE", 28, GREY, 0, 600, 0.12)
s.fade(soc, A("don't", 2) + 0.6, 0.5, y=12)
s.fade(disc, A("don't", 2) + 0.9, 0.5)

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
    <div id="root" data-composition-id="otm-chance" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-chance-audio" class="clip" src="assets/audio/mix_chance.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-chance"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
