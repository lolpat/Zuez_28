"""OTM "You vs You": a glowing-figure explainer (same system as otm-circle / otm-anyway / otm-know / otm-noise). Voice only, no music. White soft-glow figures on a dashed ground line, spotlights, small
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

# 1  trading is you versus you
s = S(0, A("not") - 0.05, first=True)
s.label(540, 560, "YOU VS YOU", 30, LBL, 1)
s.fig(300, 1.1)
mirror(s, 760)
s.fig(760, 1.0, "#cfd3da", 0.75)
v1 = vs(s, 530, 1050, 1)
s.label(300, 1300, "YOU", 28, GREY, 1)
s.label(760, 1300, "ALSO YOU", 28, GREY, 1)
tl(f'tl.fromTo("#{v1}", {{scale: 1}}, {{scale: 1.15, transformOrigin: "50% 50%", duration: 0.4, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false}}, {A("versus"):.3f});')
cue(A("versus"), "land_1", -18)

# 2  not the market, not the broker, not the guy with the bigger account
s = S(A("not") - 0.05, A("none") - 0.05)
s.label(540, 560, "NOT THEM", 30, LBL, 1)
y2 = s.fig(540, 0.8); s.pop(y2, A("not"), 0.4)
items = [(230, "THE MARKET", A("not", 1)), (540, "THE BROKER", A("not", 2)), (850, "BIGGER ACCOUNT", A("not", 3))]
for k, (x, lab, t) in enumerate(items):
    if k == 0:
        ic = s.raw(f'<g id="@ID@" style="opacity:0"><line x1="{x - 40}" y1="740" x2="{x - 40}" y2="900" stroke="#fff" stroke-width="3"/><rect x="{x - 56}" y="770" width="32" height="90" fill="#fff"/>'
                   f'<line x1="{x + 30}" y1="760" x2="{x + 30}" y2="890" stroke="{RED}" stroke-width="3"/><rect x="{x + 14}" y="790" width="32" height="70" fill="{RED}"/></g>')
    elif k == 1:
        ic = s.raw(f'<g id="@ID@" style="opacity:0"><path d="M {x - 80} 790 L {x} 740 L {x + 80} 790 Z M {x - 80} 900 H {x + 80} M {x - 55} 800 V 890 M {x - 18} 800 V 890 M {x + 18} 800 V 890 M {x + 55} 800 V 890" '
                   f'fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/></g>')
    else:
        ic = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="{x - 20}" y="740" width="40" height="160" rx="6" fill="{GOLD}"/>'
                   f'<text x="{x}" y="835" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" fill="#111">$</text></g>')
    s.pop(ic, t, 0.35, 0.5, "50% 50%")
    lb = s.label(x, 950, lab, 28, WHITE, 0, 800, 0.1); s.fade(lb, t + 0.1, 0.3)
    xm = xmark(s, x, 820, 70); s.draw(xm, t + 0.4, 0.25); cue(t + 0.4, "click_" + str(k % 2 + 1), -18)

# 3  none of them are clicking your buttons
s = S(A("none") - 0.05, A("only") - 0.35)
s.label(540, 560, "YOUR BUTTONS", 30, LBL, 1)
pn = s.path(rrect(250, 720, 580, 220, 24), WHITE, 3); s.draw(pn, A("none"), 0.5)
bb = s.pill(420, 830, "BUY", GOLD, "#111", 40); s.pop(bb, A("none") + 0.2, 0.35, 0.6, "50% 50%")
sb = s.pill(660, 830, "SELL", WHITE, "#111", 40); s.pop(sb, A("none") + 0.3, 0.35, 0.6, "50% 50%")
y3 = s.fig(540, 1.0); s.pop(y3, A("none"), 0.4)
cur = s.raw('<path id="@ID@" d="M 520 1060 l 0 52 l 14 -14 l 10 24 l 10 -5 l -10 -23 l 20 0 z" fill="#fff" style="opacity:0"/>', "p")
s.fade(cur, A("clicking") - 0.2, 0.2)
tl(f'tl.to("#{cur}", {{x: -90, y: -200, duration: 0.5, ease: "power2.inOut"}}, {A("clicking"):.3f});')
tl(f'tl.to("#{bb}", {{scale: 0.92, transformOrigin: "50% 50%", duration: 0.1, yoyo: true, repeat: 1}}, {A("buttons"):.3f});')
cue(A("buttons"), "click-confirm_1", -16)
ol = s.label(540, 1300, "ONLY YOU CLICK", 28, GOLD, 0, 800, 0.15); s.fade(ol, A("clicking") - 0.2, 0.35)

# 4  the version of you that moves the stop, chases the candle, says next week, year three
s = S(A("only") - 0.35, A("that's", 1) - 0.05)
y4 = s.fig(140, 0.9); s.pop(y4, A("only") - 0.3, 0.4)
fl = s.raw(f'<g id="@ID@" style="opacity:0"><line x1="900" y1="{GY}" x2="900" y2="{GY - 200}" stroke="{GOLD}" stroke-width="5"/><path d="M 900 {GY - 198} L 970 {GY - 175} L 900 {GY - 152} Z" fill="{GOLD}"/></g>', "fl")
s.pop(fl, A("consistency") - 0.2, 0.4, 0.4); cue(A("consistency"), "bell_E5", -20)
s.label(890, 1300, "CONSISTENCY", 28, GOLD, 0, 800, 0.1); s.fade(s.items[-1].split('"')[1], A("consistency"), 0.35)
ot = s.fig(560, 1.0, OTHER, 0.9, False); s.pop(ot, A("version") - 0.1, 0.4); cue(A("version"), "land-light_1", -18)
s.label(560, 1300, "THE OTHER YOU", 28, GREY, 0, 700, 0.12); s.fade(s.items[-1].split('"')[1], A("version"), 0.35)
for k, (txt, w_) in enumerate([("MOVES THE STOP", "moves"), ("CHASES THE CANDLE", "chases"), ("“NEXT WEEK”", "plan")]):
    p = s.pill(560, 960 - k * 85, txt, "#2a2f38", WHITE, 28); s.pop(p, A(w_) - 0.05, 0.3, 0.5, "50% 50%"); cue(A(w_), "tick_" + str(k + 1), -20)
for k in range(3):
    c = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="800" y="610" width="180" height="110" rx="12" fill="#11151b" stroke="#fff" stroke-width="3"/>'
              f'<text x="890" y="680" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="32" fill="{RED if k == 2 else "#fff"}">YEAR {k + 1}</text></g>', "yr")
    ta = A("third") - 0.9 + k * 0.46
    tl(f'tl.fromTo("#{c}", {{opacity: 0, y: -30}}, {{opacity: 1, y: 0, duration: 0.2, ease: "power2.out", immediateRender: false}}, {ta:.3f});')
    if k < 2: tl(f'tl.set("#{c}", {{opacity: 0}}, {ta + 0.46:.3f});')
    cue(ta, "tock_1", -22)

# 5  that's the fight, every session
s = S(A("that's", 1) - 0.05, A("trader", 1) - 0.35)
s.label(540, 560, "EVERY SESSION", 30, LBL, 1)
ring(s)
y5 = s.fig(380, 1.0); s.pop(y5, A("that's", 1), 0.4)
o5 = s.fig(700, 1.0, OTHER, 0.9, False); s.pop(o5, A("that's", 1) + 0.1, 0.4)
bell = s.raw(f'<g id="@ID@" style="opacity:0"><path d="M 510 860 Q 510 800 540 795 Q 570 800 570 860 Z M 500 860 H 580" fill="none" stroke="{GOLD}" stroke-width="4"/><circle cx="540" cy="872" r="7" fill="{GOLD}"/></g>', "bl")
s.pop(bell, A("fight", 1) - 0.1, 0.3, 0.5, "50% 50%"); cue(A("fight", 1), "bell_A4", -14)
tl(f'tl.to("#{bell}", {{rotation: 12, transformOrigin: "50% 0%", duration: 0.08, yoyo: true, repeat: 5}}, {A("fight", 1) + 0.25:.3f});')
for k, (txt, t) in enumerate([("LONDON", A("fight", 1) + 0.3), ("NEW YORK", A("session"))]):
    p = s.pill(540, 700, txt, "#2a2f38", WHITE, 28)
    tl(f'tl.fromTo("#{p}", {{opacity: 0, scale: 0.6, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)", immediateRender: false}}, {t:.3f});')
    if k == 0: tl(f'tl.set("#{p}", {{opacity: 0}}, {A("session") - 0.02:.3f});')

# 6  the trader who wrote the rules against the trader who wants to break them
s = S(A("trader", 1) - 0.35, A("here's") - 0.4)
s.label(540, 560, "RULES VS IMPULSE", 30, LBL, 1)
y6 = s.fig(250, 1.0); s.pop(y6, A("trader", 1) - 0.3, 0.4)
rp = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="185" y="790" width="130" height="160" rx="8" fill="#11151b" stroke="{GOLD}" stroke-width="3"/>'
           + "".join(f'<line x1="205" y1="{830 + k * 28}" x2="{295 - (k % 2) * 25}" y2="{830 + k * 28}" stroke="{GOLD}" stroke-width="3"/>' for k in range(4)) + '</g>', "rp")
s.pop(rp, A("rules"), 0.35, 0.5, "50% 50%"); cue(A("rules"), "pop_1", -20)
s.label(250, 1300, "WROTE THE RULES", 28, GOLD, 0, 800, 0.08); s.fade(s.items[-1].split('"')[1], A("rules"), 0.35)
v6 = vs(s, 540, 1060); s.pop(v6, A("against") - 0.1, 0.35, 0.5, "50% 50%")
o6 = s.fig(830, 1.0, OTHER, 0.9, False); s.pop(o6, A("trader", 2), 0.4)
bp = s.pill(830, 870, "BREAK THEM", RED, WHITE, 28); s.pop(bp, A("break"), 0.35, 0.5, "50% 50%"); cue(A("break"), "land-light_1", -16)
s.label(830, 1300, "WANTS TO BREAK THEM", 28, GREY, 0, 700, 0.06); s.fade(s.items[-1].split('"')[1], A("trader", 2), 0.35)

# 7  nobody tells you: he isn't reckless for fun, he's impatient
s = S(A("here's") - 0.4, A("wants", 2) - 0.3)
s.label(540, 560, "WHAT NOBODY TELLS YOU", 30, LBL, 1)
sp7 = s.spot(540, 0); s.fade(sp7, A("here's"), 0.5)
o7 = s.fig(540, 1.05, OTHER, 0.95, False); s.pop(o7, A("here's"), 0.4)
rk = s.pill(540, 860, "RECKLESS?", "#2a2f38", WHITE, 30); s.pop(rk, A("reckless") - 0.1, 0.3, 0.5, "50% 50%")
rx = s.path("M 420 860 H 660", GOLD, 5); s.draw(rx, A("fun"), 0.25)
tl(f'tl.to("#{rk}", {{opacity: 0.3, duration: 0.3}}, {A("fun") + 0.2:.3f});')
ip = s.pill(540, 760, "IMPATIENT", GOLD, "#111", 34); s.pop(ip, A("impatient") - 0.05, 0.35, 0.5, "50% 50%"); cue(A("impatient"), "bell_C5", -18)
hg = s.raw(f'<g id="@ID@" style="opacity:0"><path d="M 760 980 H 840 M 760 1120 H 840 M 770 980 Q 770 1040 800 1050 Q 830 1040 830 980 M 770 1120 Q 770 1060 800 1050 Q 830 1060 830 1120" '
           f'fill="none" stroke="#fff" stroke-width="4"/><path d="M 785 1115 Q 800 1085 815 1115 Z" fill="{GOLD}"/></g>', "hg")
s.pop(hg, A("impatient") + 0.2, 0.35, 0.5, "50% 50%")
tl(f'tl.to("#{hg}", {{rotation: 180, transformOrigin: "50% 50%", duration: 0.6, ease: "power2.inOut"}}, {A("impatient") + 0.7:.3f});')

# 8  he wants action, and makes "just this once" sound reasonable
s = S(A("wants", 2) - 0.3, A("most") - 0.05)
s.label(540, 560, "“JUST THIS ONCE”", 30, LBL, 1)
o8 = s.fig(540, 1.05, OTHER, 0.95, False); s.pop(o8, A("wants", 2) - 0.25, 0.4)
bolt = s.raw(f'<path id="@ID@" d="M 260 760 L 220 860 H 262 L 238 960 L 320 840 H 276 L 300 760 Z" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 12px {GOLD})"/>', "bt")
s.pop(bolt, A("action") - 0.1, 0.3, 0.4, "50% 50%"); cue(A("action"), "whoosh-short_2", -20)
s.label(270, 1010, "ACTION", 28, GOLD, 0, 800, 0.15); s.fade(s.items[-1].split('"')[1], A("action"), 0.3)
jt = s.pill(640, 880, "JUST THIS ONCE", WHITE, "#111", 32); s.pop(jt, A("just") - 0.05, 0.35, 0.5, "50% 50%"); cue(A("just"), "pop_3", -18)
tl(f'tl.to("#{jt}", {{scale: 1.12, transformOrigin: "50% 50%", duration: 0.6, yoyo: true, repeat: 1, ease: "sine.inOut"}}, {A("just") + 0.5:.3f});')
sr = s.label(540, 1300, "SOUNDS REASONABLE", 28, WHITE, 0, 800, 0.12); s.fade(sr, A("reasonable") - 0.2, 0.35)

# 9  most traders lose to him without ever noticing there was a fight
s = S(A("most") - 0.05, A("blame") - 0.4)
s.label(540, 560, "WITHOUT NOTICING", 30, LBL, 1)
for k, x in enumerate([160, 350, 540, 730, 920]):
    sh = s.fig(x + 26, 0.8, OTHER, 0.45, False)
    f = s.fig(x, 0.8, "#e6e9ee", 1); s.pop(f, A("most") + k * 0.08, 0.35); s.pop(sh, A("most") + k * 0.08 + 0.1, 0.35)
    tk = A("lose") + 0.15 + k * 0.28
    tl(f'tl.to("#{f}", {{opacity: 0.25, duration: 0.25}}, {tk:.3f});')
    ko = s.label(x, 1300, "K.O.", 28, RED, 0, 800, 0.1); s.fade(ko, tk, 0.2)
    cue(tk, "land-light_1", -24)

# 10  they blame the news, the spread, the stop hunt, and never look at who clicked
s = S(A("blame") - 0.4, A("don't", 1) - 0.35)
s.label(540, 560, "WHO CLICKED?", 30, LBL, 1)
y10 = s.fig(170, 0.95); s.pop(y10, A("blame") - 0.35, 0.4)
arm = s.path("M 205 1110 L 290 1040", "#fff", 8); s.draw(arm, A("blame"), 0.25)
icons = [(400, 740, "NEWS", A("news")), (640, 680, "SPREAD", A("spread")), (880, 740, "STOP HUNT", A("hunt"))]
for k, (x, y, lab, t) in enumerate(icons):
    if k == 0:
        ic = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="{x - 60}" y="{y - 50}" width="120" height="90" rx="6" fill="none" stroke="#fff" stroke-width="3"/>'
                   f'<line x1="{x - 45}" y1="{y - 30}" x2="{x + 45}" y2="{y - 30}" stroke="#fff" stroke-width="6"/>'
                   + "".join(f'<line x1="{x - 45}" y1="{y - 8 + j * 16}" x2="{x + 45 - (j % 2) * 20}" y2="{y - 8 + j * 16}" stroke="#ffffff90" stroke-width="3"/>' for j in range(3)) + '</g>')
    elif k == 1:
        ic = s.raw(f'<g id="@ID@" style="opacity:0"><line x1="{x - 60}" y1="{y - 25}" x2="{x + 60}" y2="{y - 25}" stroke="#8fb6ff" stroke-width="4"/>'
                   f'<line x1="{x - 60}" y1="{y + 25}" x2="{x + 60}" y2="{y + 25}" stroke="{RED}" stroke-width="4"/>'
                   f'<path d="M {x} {y - 20} V {y + 20} M {x - 8} {y - 12} L {x} {y - 20} L {x + 8} {y - 12} M {x - 8} {y + 12} L {x} {y + 20} L {x + 8} {y + 12}" fill="none" stroke="#fff" stroke-width="3"/></g>')
    else:
        ic = s.raw(f'<g id="@ID@" style="opacity:0"><line x1="{x - 70}" y1="{y + 10}" x2="{x + 70}" y2="{y + 10}" stroke="{RED}" stroke-width="3" stroke-dasharray="8 6"/>'
                   f'<line x1="{x}" y1="{y - 50}" x2="{x}" y2="{y + 40}" stroke="#fff" stroke-width="3"/><rect x="{x - 14}" y="{y - 40}" width="28" height="30" fill="#fff"/></g>')
    s.pop(ic, t - 0.1, 0.3, 0.5, "50% 50%")
    lb = s.label(x, y + 90, lab, 28, WHITE, 0, 800, 0.1); s.fade(lb, t, 0.3)
    cue(t, "tick_" + str(k + 1), -20)
mr10 = mirror(s, 640, GY, 190, 300, 0); s.fade(mr10, A("look") - 0.1, 0.4)
rf = s.fig(640, 0.8, "#cfd3da", 0); s.fade(rf, A("look") + 0.1, 0.4)
cue(A("clicked"), "bell_G4", -18)

# 11  you don't need to beat the market; beat him, once today, again tomorrow
s = S(A("don't", 1) - 0.35, A("that's", 2) - 0.05)
s.label(540, 560, "BEAT HIM", 30, LBL, 1)
ring(s)
y11 = s.fig(400, 1.0); s.pop(y11, A("don't", 1) - 0.3, 0.4)
o11 = s.fig(700, 1.0, OTHER, 0.9, False); s.pop(o11, A("don't", 1) - 0.2, 0.4)
tl(f'tl.to("#{y11}", {{x: 120, duration: 0.18, ease: "power3.in", yoyo: true, repeat: 1}}, {A("beat", 2) - 0.1:.3f});')
tl(f'tl.to("#{o11}", {{rotation: 80, transformOrigin: "100% 100%", opacity: 0.4, duration: 0.45, ease: "power2.in"}}, {A("beat", 2) + 0.1:.3f});')
cue(A("beat", 2) + 0.1, "land_1", -14)
for k, (txt, t, x) in enumerate([("TODAY ✓", A("today"), 360), ("TOMORROW ✓", A("tomorrow"), 720)]):
    p = s.pill(x, 740, txt, GOLD, "#111", 30); s.pop(p, t - 0.05, 0.35, 0.5, "50% 50%"); cue(t, "pop_" + str(k + 1), -18)

# 12  that's the whole game: a streak, day after day
s = S(A("that's", 2) - 0.05, A("nobody", 2) - 0.05)
s.label(540, 560, "THE WHOLE GAME", 30, LBL, 1)
cells = []
for r in range(6):
    for c in range(10):
        x, y = 215 + c * 66, 680 + r * 66
        s.raw(f'<rect id="@ID@" x="{x}" y="{y}" width="52" height="52" rx="8" fill="none" stroke="#ffffff50" stroke-width="2"/>')
        cells.append(s.raw(f'<rect id="@ID@" x="{x}" y="{y}" width="52" height="52" rx="8" fill="{GOLD}" style="opacity:0"/>', "cl"))
t0, t1 = A("that's", 2), A("nobody", 2) - 0.4
for i, c in enumerate(cells):
    tl(f'tl.set("#{c}", {{opacity: 1}}, {t0 + (t1 - t0) * i / len(cells):.3f});')
lb12 = s.label(540, 1150, "ONE DAY AT A TIME", 34, GOLD, 0, 800, 0.12); s.fade(lb12, t0 + 0.1, 0.35)
cue(t0, "swell_1", -22)

# 13  nobody is coming to follow your plan for you
s = S(A("nobody", 2) - 0.05, A("order") - 0.05)
ring(s, op=0.6)
sp13 = s.spot(540, 1)
y13 = s.fig(140, 1.0); s.walk(y13, A("nobody", 2), 400, 1.4)
nb = s.label(540, 800, "IT'S ON YOU", 40, GOLD, 0, 800, 0.2); s.fade(nb, A("coming"), 0.5, y=12); cue(A("coming"), "bell_E5", -18)

# 14  order the market (outro with handles; no end card)
s = S(A("order") - 0.05, TOTAL)
es = s.spot(540, 0, "232,194,106", 40, 230); s.fade(es, A("order"), 0.6)
em = s.raw('<image id="@ID@" href="assets/otm_emblem.png" x="390" y="900" width="300" height="291" style="opacity:0;filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>', "i")
s.pop(em, A("order"), 0.7, 0.6, "50% 50%"); cue(A("order"), "bell_A4", -16)
o1 = s.label(540, 1300, "ORDER THE MARKET", 32, GOLD, 0, 800, 0.3); s.fade(o1, A("order") + 0.3, 0.5)
o2 = s.label(540, 1360, "DON'T LET THE MARKET ORDER YOU", 28, WHITE, 0, 700, 0.12); s.fade(o2, A("don't", 2), 0.4)
o3 = s.pill(540, 1470, "FOLLOW FOR MORE", GOLD, "#111", 30); s.pop(o3, A("follow", 3), 0.4, 0.6, "50% 50%"); cue(A("follow", 3), "click-confirm_1", -16)
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
    <div id="root" data-composition-id="otm-vs" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-vs-audio" class="clip" src="assets/audio/mix_vs.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-vs"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
