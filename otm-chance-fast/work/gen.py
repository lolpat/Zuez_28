"""OTM "Second Chance" (fast, original-clip pace): hard cuts every 2-3 words and a giant word layer, in the glowing-figure world (same system as otm-circle / otm-anyway / otm-know / otm-noise). Voice only, no music. White soft-glow figures on a dashed ground line, spotlights, small
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

import re
# ================================================================================= fast cut: picture per 2-3 words + giant word layer
class Cut(S):
    """A hard cut: on at o with a punch-in, off at c. No fades."""
    def __init__(self, o, c, punch=True):
        S.n += 1
        self.id, self.o, self.c, self.items = f"sc{S.n}", o, c, []
        S.scenes.append(self)
        tl(f'tl.set("#{self.id}", {{opacity: 1, visibility: "visible"}}, {o:.3f});')
        if punch:
            tl(f'tl.fromTo("#{self.id}", {{scale: 1.14}}, {{scale: 1, transformOrigin: "50% 62%", duration: 0.35, ease: "expo.out", immediateRender: false}}, {o:.3f});')
        tl(f'tl.set("#{self.id}", {{opacity: 0, visibility: "hidden"}}, {c:.3f});')

def ticket(s, x, y, sc=1.0):
    w, h = 150 * sc, 70 * sc
    return s.raw(f'<g id="@ID@"><rect x="{x - w / 2:.0f}" y="{y - h / 2:.0f}" width="{w:.0f}" height="{h:.0f}" rx="10" fill="{GOLD}" style="filter:drop-shadow(0 0 12px rgba(232,194,106,0.6))"/>'
                 f'<circle cx="{x - w / 2:.0f}" cy="{y}" r="{10 * sc:.0f}" fill="#000"/><circle cx="{x + w / 2:.0f}" cy="{y}" r="{10 * sc:.0f}" fill="#000"/>'
                 f'<text x="{x}" y="{y + 10 * sc:.0f}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="{max(28, 28 * sc):.0f}" fill="#111">2ND</text></g>', "tk")

def dcircle(s, x, y, kind, col=GOLD, r=75):
    base = f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{col}" stroke-width="3" stroke-dasharray="10 8"/>'
    if kind == "bird":
        ic = f'<path d="M {x - 45} {y + 8} Q {x - 22} {y - 18} {x} {y + 6} Q {x + 22} {y - 18} {x + 45} {y + 8} M {x - 27} {y + 36} Q {x - 13} {y + 22} {x} {y + 36} Q {x + 13} {y + 22} {x + 27} {y + 36}" fill="none" stroke="#fff" stroke-width="4"/>'
    elif kind == "bars":
        ic = "".join(f'<rect x="{x - 44 + i * 24}" y="{y + 36 - (18 + i * 16)}" width="16" height="{18 + i * 16}" fill="#fff"/>' for i in range(4))
    else:
        ic = (f'<circle cx="{x}" cy="{y - 34}" r="14" fill="none" stroke="{GOLD}" stroke-width="4" stroke-dasharray="6 5"/>'
              f'<path d="M {x - 24} {y + 40} V {y + 4} Q {x - 24} {y - 16} {x} {y - 16} Q {x + 24} {y - 16} {x + 24} {y + 4} V {y + 40}" fill="none" stroke="{GOLD}" stroke-width="4" stroke-dasharray="6 5"/>')
    return s.raw(f'<g id="@ID@">{base}{ic}</g>', "dc")

def desk(s, x0=360):
    s.raw(f'<g id="@ID@"><rect x="{x0}" y="1100" width="360" height="14" fill="#fff" opacity="0.85"/>'
          f'<line x1="{x0 + 20}" y1="1114" x2="{x0 + 20}" y2="1240" stroke="#fff" stroke-width="5" opacity="0.7"/><line x1="{x0 + 340}" y1="1114" x2="{x0 + 340}" y2="1240" stroke="#fff" stroke-width="5" opacity="0.7"/>'
          f'<rect x="{x0 + 150}" y="980" width="170" height="110" rx="8" fill="#0b1220" stroke="#fff" stroke-width="3" style="filter:drop-shadow(0 0 18px rgba(120,180,255,0.6))"/>'
          f'<line x1="{x0 + 235}" y1="1090" x2="{x0 + 235}" y2="1100" stroke="#fff" stroke-width="4"/>'
          f'<path d="M {x0 + 165} 1070 L {x0 + 195} 1055 L {x0 + 220} 1062 L {x0 + 250} 1030 L {x0 + 275} 1040 L {x0 + 305} 1000" fill="none" stroke="{GOLD}" stroke-width="4"/></g>')

def T_tickets(s):
    for k, x in enumerate([150, 300, 780, 930]):
        s.fig(x, 0.8, "#cfd3da", 0.85); ticket(s, x, 1000, 0.8)
    s.fig(540, 1.0)
def T_spot_you(s):
    s.spot(540, 1, "232,194,106"); s.fig(540, 1.05); ticket(s, 540, 960, 1.1)
def T_desk(s):
    desk(s); s.fig(450, 0.85, gy=1180)
def T_promise(s):
    s.fig(540, 1.0)
    s.raw(f'<g id="@ID@"><rect x="380" y="880" width="320" height="110" rx="18" fill="#11151b" stroke="{GOLD}" stroke-width="3"/>'
          f'<text x="540" y="948" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" letter-spacing="0.2em" fill="{GOLD}">PROMISE</text></g>')
def T_bird(s):
    dcircle(s, 540, 960, "bird"); s.fig(330, 0.9)
def T_bars(s):
    dcircle(s, 540, 960, "bars"); s.fig(750, 0.9)
def T_future(s):
    s.fig(380, 0.95); s.fig(700, 1.45, GOLD, 1, dashed=True)
def T_dreams(s):
    for x, k in [(230, "bird"), (540, "bars"), (850, "future")]: dcircle(s, x, 940, k, r=70)
    s.fig(540, 0.8)
def T_fall(s):
    for x, k in [(250, "bird"), (540, "bars"), (830, "future")]: dcircle(s, x, 1180, k, "#ffffff50", r=55)
    s.fig(540, 0.9, "#9aa0a8", 0.8, False)
def T_sad(s):
    s.spot(540, 0.5); s.fig(540, 1.0, "#9aa0a8", 0.85, False)
def T_blown(s):
    s.raw(f'<g id="@ID@"><rect x="420" y="880" width="240" height="160" rx="16" fill="{RED}"/><text x="540" y="985" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="56" fill="#fff">$0</text></g>')
    s.fig(800, 0.85, "#9aa0a8", 0.8, False)
def T_down(s):
    s.path("M 200 900 L 320 960 L 400 930 L 520 1060 L 600 1030 L 740 1170 L 880 1150", RED, 6, drawn=True)
    s.fig(900, 0.7, "#9aa0a8", 0.8, False)
def T_pin(s):
    s.path("M 200 1230 C 400 1150 600 1220 840 980", "#ffffff70", 3, drawn=True, extra='stroke-dasharray="12 12"')
    s.raw('<g id="@ID@"><path d="M 840 1000 C 790 940 790 890 840 880 C 890 890 890 940 840 1000 Z" fill="none" stroke="#fff" stroke-width="4"/><circle cx="840" cy="925" r="14" fill="#fff"/></g>')
    s.fig(200, 0.9)
def T_candles(s):
    r = random.Random(3)
    g = ""
    for i in range(45):
        x = 150 + (i % 15) * 54; y = 930 + (i // 15) * 85; h = r.uniform(18, 50); col = GOLD if r.random() < 0.35 else "#ffffffb0"
        g += f'<line x1="{x}" y1="{y - h / 2 - 8:.0f}" x2="{x}" y2="{y + h / 2 + 8:.0f}" stroke="{col}" stroke-width="2"/><rect x="{x - 7}" y="{y - h / 2:.0f}" width="14" height="{h:.0f}" fill="{col}"/>'
    s.raw(f'<g id="@ID@">{g}</g>')
def T_clock(s):
    x, y = 540, 1030
    s.raw(f'<g id="@ID@"><circle cx="{x}" cy="{y}" r="130" fill="none" stroke="#fff" stroke-width="3"/>'
          f'<path d="M {x} {y - 130} A 130 130 0 0 1 {x + 113} {y + 65}" fill="none" stroke="{GOLD}" stroke-width="10"/>'
          f'<path d="M {x + 113} {y + 65} A 130 130 0 0 1 {x - 113} {y + 65}" fill="none" stroke="#8fb6ff" stroke-width="10"/>'
          f'<path d="M {x - 113} {y + 65} A 130 130 0 0 1 {x} {y - 130}" fill="none" stroke="#ffffffb0" stroke-width="10"/>'
          f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y - 90}" stroke="#fff" stroke-width="6"/><line x1="{x}" y1="{y}" x2="{x + 60}" y2="{y}" stroke="#fff" stroke-width="6"/></g>')
def T_stars(s):
    for (x, y, r) in [(220, 930, 14), (380, 1010, 10), (560, 900, 18), (720, 990, 12), (880, 920, 16), (640, 1080, 9), (300, 1100, 9)]:
        s.raw(f'<circle id="@ID@" cx="{x}" cy="{y}" r="{r}" fill="{GOLD}" style="filter:drop-shadow(0 0 14px {GOLD})"/>', "c")
    s.fig(540, 0.8)
def T_timeline(s):
    s.path("M 80 1000 H 1000", "#ffffff40", 3, drawn=True)
    for x in (140, 230, 320): s.raw(f'<circle id="@ID@" cx="{x}" cy="1000" r="12" fill="#8a8f98"/>', "c")
    for x in range(560, 1000, 60): s.raw(f'<circle id="@ID@" cx="{x}" cy="1000" r="13" fill="{GOLD}" style="filter:drop-shadow(0 0 10px {GOLD})"/>', "c")
    s.fig(440, 0.9)
def T_ahead(s):
    s.spot(760, 1, "232,194,106"); s.fig(300, 0.9); s.fig(760, 1.2, GOLD, 1, dashed=True)
def T_plan(s):
    s.raw(f'<g id="@ID@"><rect x="430" y="880" width="220" height="280" rx="10" fill="#11151b" stroke="{GOLD}" stroke-width="4"/>'
          + "".join(f'<line x1="460" y1="{930 + j * 40}" x2="{620 - (j % 2) * 40}" y2="{930 + j * 40}" stroke="{GOLD}" stroke-width="4"/>' for j in range(5)) + '</g>')
def T_journal(s):
    s.raw('<g id="@ID@"><path d="M 540 930 C 470 900 390 900 330 915 V 1110 C 390 1095 470 1095 540 1125 C 610 1095 690 1095 750 1110 V 915 C 690 900 610 900 540 930 Z M 540 930 V 1125" '
          'fill="none" stroke="#fff" stroke-width="5" stroke-linejoin="round"/></g>')
def T_backtest(s):
    r = random.Random(9)
    g = ""
    for i in range(9):
        x = 250 + i * 70; h = r.uniform(40, 110); y = 1130 - i * 25
        g += f'<line x1="{x}" y1="{y - h / 2 - 15:.0f}" x2="{x}" y2="{y + h / 2 + 15:.0f}" stroke="{GOLD}" stroke-width="3"/><rect x="{x - 15}" y="{y - h / 2:.0f}" width="30" height="{h:.0f}" fill="{GOLD}"/>'
    s.raw(f'<g id="@ID@">{g}</g>')
def T_future_gold(s):
    s.spot(540, 1, "232,194,106"); s.fig(540, 1.25, GOLD, 1)
def T_startline(s):
    s.raw('<g id="@ID@"><line x1="300" y1="1240" x2="300" y2="1050" stroke="#fff" stroke-width="4"/><text x="300" y="1030" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" letter-spacing="0.2em" fill="#fff">START</text></g>')
    s.fig(420, 1.0); s.raw(f'<rect id="@ID@" x="450" y="1110" width="50" height="70" rx="12" fill="{GOLD}"/>', "bp")
def T_lessons(s):
    for x in (300, 540, 780): s.pill(x, 980, "LESSON", GOLD, "#111", 30, op=1)
    s.fig(540, 0.85); s.raw(f'<rect id="@ID@" x="570" y="1150" width="40" height="60" rx="10" fill="{GOLD}"/>', "bp")
def T_ticket_big(s):
    ticket(s, 540, 1030, 2.2)
def T_equity(s):
    s.path("M 140 1000 L 240 940 L 310 1090 L 370 1160 L 440 1110 L 530 1070 L 620 990", WHITE, 5, drawn=True)
    s.path("M 620 990 L 710 940 L 790 960 L 880 850 L 960 790", GOLD, 7, drawn=True)
    s.raw(f'<circle id="@ID@" cx="960" cy="790" r="16" fill="{GOLD}" style="filter:drop-shadow(0 0 12px {GOLD})"/>', "c")

SECTIONS = [  # (start anchor, pictures cycled over that section's cuts)
    (None, [T_tickets, T_spot_you]),
    (("remember", 1), [T_desk, T_promise]),
    (("freedom", 1), [T_bird, T_bars, T_future]),
    (("remember", 2), [T_dreams]),
    (("so", 1), [T_fall, T_sad]),
    (("because", 1), [T_blown, T_down, T_pin]),
    (("look", 1), [T_candles, T_clock, T_stars]),
    (("how", 2), [T_timeline, T_ahead]),
    (("maybe", 1), [T_plan]),
    (("open", 1), [T_journal, T_backtest, T_future_gold]),
    (("don't", 1), [T_startline]),
    (("start", 2), [T_lessons]),
    (("give", 3), [T_ticket_big, T_equity]),
]
KW = [("blew", T_blown), ("account", T_blown), ("strategy", T_down), ("planned", T_down), ("work", T_down), ("thought", T_pin), ("now", T_pin),
      ("where", T_pin), ("thousands", T_candles), ("setups", T_candles), ("traded", T_candles), ("sessions", T_clock), ("studied", T_clock),
      ("opportunities", T_stars), ("imagined", T_stars), ("freedom", T_bird), ("dreamed", T_bird), ("growing", T_bars), ("account", T_bars),
      ("swore", T_future), ("trader", T_future), ("become", T_future), ("journal", T_journal), ("open", T_journal), ("back", T_backtest),
      ("test", T_backtest), ("setup", T_backtest), ("abandoned", T_backtest), ("believed", T_future_gold), ("could", T_future_gold),
      ("trader", T_future_gold), ("equity", T_equity), ("curve", T_equity), ("finished", T_equity), ("chance", T_ticket_big),
      ("yourself", T_ticket_big), ("promise", T_promise), ("made", T_promise), ("chart", T_desk), ("first", T_desk), ("opened", T_desk),
      ("best", T_timeline), ("behind", T_timeline), ("trades", T_timeline), ("seen", T_ahead), ("offer", T_ahead), ("still", T_ahead),
      ("losses", T_lessons), ("taught", T_lessons), ("everything", T_lessons), ("even", T_spot_you), ("you", T_spot_you)]
OUT = F("order")
sec_start = [0] + [F(w, k) for (w, k), _ in [(a, b) for a, b in SECTIONS[1:]]]
# cut points: a new picture every 2-3 words, at pauses, and at every section start
cuts, run = [0], 0
for i in range(1, OUT):
    run += 1
    gap = words[i]["start"] - words[i - 1]["end"]
    if i in sec_start or run >= 2 or (gap > 0.18 and run >= 1):
        cuts.append(i); run = 0
cuts.append(OUT)
sec_of = lambda i: max(k for k, st in enumerate(sec_start) if st <= i)
counter = {}
for j in range(len(cuts) - 1):
    a, b = cuts[j], cuts[j + 1]
    sk = sec_of(a)
    pics = SECTIONS[sk][1]
    n_ = counter.get(sk, 0); counter[sk] = n_ + 1
    seg = [_n(w["text"]) for w in words[a:b]]
    pick = None
    for kw, fn in KW:
        if fn in pics and kw in seg: pick = fn; break
    o = 0.0 if j == 0 else W(a) - 0.05
    c_ = W(b) - 0.05
    cut = Cut(o, c_, punch=j > 0)
    (pick or pics[n_ % len(pics)])(cut)
    if a in sec_start and j > 0:
        cue(o, "whoosh-short_" + str(sk % 3 + 1), -24)
        tl(f'tl.fromTo("#flash", {{opacity: 0.35}}, {{opacity: 0, duration: 0.14, ease: "power2.out", immediateRender: false}}, {o:.3f});')
print("cuts", len(cuts) - 1, "avg %.2fs" % ((W(OUT) - W(0)) / (len(cuts) - 1)))

# giant word layer: one word at a time, popping in on the word
GOLDW = {"SECOND", "CHANCE", "PROMISE", "FREEDOM", "ACCOUNT", "TRADER", "BADLY", "WHY", "STRATEGY", "MARKET", "THOUSANDS",
         "OPPORTUNITIES", "BEST", "PLAN", "ANOTHER", "JOURNAL", "BACK", "TEST", "BACKTEST", "BECOME", "BELIEVED", "LOSSES", "TAUGHT",
         "EQUITY", "FINISHED", "AGAIN", "DREAMED", "FIRST", "SETUPS", "OFFER", "YOURSELF"}
REDW = {"BLEW", "GIVE"}
layer = Cut(0, W(OUT) - 0.05, punch=False)
layer.items.append('<rect id="flash" x="0" y="0" width="1080" height="1920" fill="#fff" style="opacity:0"/>')
for i in range(OUT):
    txt = re.sub(r"[^A-Za-z0-9'$%-]", "", words[i]["text"]).upper().strip("-")
    if not txt: continue
    fs = int(min(150, 940 / (0.72 * max(4, len(txt)))))
    col = GOLD if txt in GOLDW else (RED if txt in REDW else WHITE)
    wid = layer.raw(f'<text id="@ID@" class="bw" x="540" y="790" text-anchor="middle" font-size="{fs}" fill="{col}" style="opacity:0">{txt}</text>', "w")
    t0 = W(i) - 0.04 if i else 0.25
    t1 = W(i + 1) - 0.04 if i + 1 < OUT else W(OUT) - 0.1
    if words[i + 1]["start"] - words[i]["end"] > 0.45 if i + 1 < len(words) else False:
        t1 = min(t1, words[i]["end"] + LEAD + 0.35)
    tl(f'tl.fromTo("#{wid}", {{opacity: 1, scale: 1.32, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.12, ease: "power2.out", immediateRender: false}}, {t0:.3f});')
    tl(f'tl.set("#{wid}", {{opacity: 0}}, {max(t1, t0 + 0.13):.3f});')

# outro (handles; no end card)
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
s.fade(soc, A("don't", 2) + 0.5, 0.4, y=12)
s.fade(disc, A("don't", 2) + 0.8, 0.4)

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
.bw { font-family: "Archivo Black", Montserrat, sans-serif; font-weight: 400; paint-order: stroke; stroke: #000; stroke-width: 12px; stroke-linejoin: round; letter-spacing: 0.01em; }
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
    <div id="root" data-composition-id="otm-chance-fast" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-chance-fast-audio" class="clip" src="assets/audio/mix_fast.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-chance-fast"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
