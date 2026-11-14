"""OTM "Headlines vs. the Trend": a glowing-figure explainer in the OTM style (same scene system as otm-missed),
inspired by an infographic that put four founders' widely reported personal scandals on their companies' stock charts.
Four documented cases in neutral wording (no photos, no logos, no unverified rumours, no exact figures; the charts
are illustrative), then the lesson: years later every stock was far higher, not because of the scandal (timing
doesn't prove cause) but because the businesses kept growing. The headline lasted a week, the trend lasted years:
ask whether news changes the business or just the conversation. Trade the trend, not the gossip.
Original script, voice only (Quentin), no music.
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

def toplab(s, small, big, t0, t1, bcol=WHITE, scol=LBL, bsize=52, y=560):
    ids = []
    if small:
        a = s.label(540, y - 70, small, 28, scol, 0, 700, 0.12); ids.append(a)
    b = s.label(540, y, big, bsize, bcol, 0, 800, 0.04); ids.append(b)
    for i in ids:
        s.fade(i, t0, 0.3, y=10)
        tl(f'tl.to("#{i}", {{opacity: 0, duration: 0.15}}, {t1 - 0.17:.3f});')
    return ids

def paper(x, y, w=150, h=110):
    lines = "".join(f'<line x1="{x - w / 2 + 14}" y1="{y - h / 2 + 46 + k * 16}" x2="{x + w / 2 - 14 - (k % 2) * 30}" y2="{y - h / 2 + 46 + k * 16}" stroke="#b9ad93" stroke-width="3"/>' for k in range(4))
    return (f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="6" fill="#f3ead8"/>'
            f'<rect x="{x - w / 2 + 12}" y="{y - h / 2 + 12}" width="{w - 24}" height="18" fill="{RED}"/>{lines}')

# 1  "Four founders, four personal scandals, four front pages."
s = S(0, ix(8) - 0.1, first=True)
s.label(540, 560, "HEADLINES", 64, WHITE, 1, 800, 0.06)
s.label(540, 640, "VS. THE TREND", 48, GOLD, 1, 800, 0.08)
figs = []
for k in range(4):
    x = 210 + k * 220
    f = s.fig(x, 0.85, WHITE); figs.append(f)
    tg = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="{x - 70}" y="960" width="140" height="44" rx="10" fill="{RED}"/>'
               f'<text x="{x}" y="991" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" fill="#fff">SCANDAL</text></g>', "sc")
    s.pop(tg, ix(4) - 0.1 + k * 0.12, 0.3, 0.5, "50% 50%")
    pp = s.raw(f'<g id="@ID@" style="opacity:0">{paper(x, 800)}</g>', "pp")
    tl(f'tl.fromTo("#{pp}", {{opacity: 0, y: -60, rotation: -8, transformOrigin: "50% 50%"}}, {{opacity: 1, y: 0, rotation: {(-1) ** k * 4}, duration: 0.4, ease: "back.out(1.5)", immediateRender: false}}, {ix(6) - 0.1 + k * 0.12:.3f});')
cue(ix(4) - 0.1, "tock_1", -18); cue(ix(6) - 0.1, "whoosh-short_1", -20)
for k, (lab, t) in enumerate([("4 FOUNDERS", ix(0)), ("4 SCANDALS", ix(2)), ("4 FRONT PAGES", ix(5))]):
    l = s.label(540, 1330 + k * 60, lab, 32, [WHITE, RED, LBL][k], 0, 800, 0.15); s.fade(l, t, 0.3)

# 2  the four cases on a 2x2 grid of illustrative charts; "you'd expect the stocks to suffer"; "years later, every one of them was far higher"
o2, c2 = ix(8) - 0.1, ix(68) - 0.1
s = S(o2, c2, ground=False, restore=False)
CASES = [("AMAZON", "2019", 300, 820, ix(8), "THE FOUNDER'S PRIVATE LIFE", "MAKES WORLD NEWS"),
         ("MICROSOFT", "2021", 780, 820, ix(23), "REPORTS REVEAL", "A PAST AFFAIR"),
         ("SK HYNIX", "2015", 300, 1180, ix(33), "THE CHAIRMAN", "PUBLICLY ADMITS AN AFFAIR"),
         ("GOOGLE", "2013", 780, 1180, ix(42), "A CO-FOUNDER'S AFFAIR", "GOES PUBLIC")]
nxt = [ix(23), ix(33), ix(42), ix(53)]
r2 = random.Random(21)
for k, (name, yr, cx, cy, t, l1, l2) in enumerate(CASES):
    card = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(cx - 220, cy - 160, 440, 320, 18)}" fill="#0f1319" stroke="#ffffff50" stroke-width="2.5"/>'
                 f'<text x="{cx - 196}" y="{cy - 112}" font-family="Montserrat" font-weight="800" font-size="32" fill="#fff">{name}</text>'
                 f'<text x="{cx + 196}" y="{cy - 112}" text-anchor="end" font-family="Montserrat" font-weight="800" font-size="30" fill="{GOLD}">{yr}</text>'
                 f'<line x1="{cx - 196}" y1="{cy + 130}" x2="{cx + 196}" y2="{cy + 130}" stroke="#ffffff30" stroke-width="2"/></g>', "cd")
    s.pop(card, t - 0.15, 0.4, 0.6, "50% 50%"); cue(t - 0.15, "pop_" + str(k % 4 + 1), -20)
    # before the headline: a modest, noisy line up to the dot
    x0, x1d, yb = cx - 190, cx - 20, cy + 100
    pts = [(x0 + j * (x1d - x0) / 8, yb - j * 7 - r2.uniform(-8, 8)) for j in range(9)]
    pre = s.path("M " + " L ".join(f"{x:.0f} {y:.0f}" for x, y in pts), "#e9ecf1", 4); s.draw(pre, t + 0.1, 0.8)
    dx, dy = pts[-1]
    dot = s.raw(f'<circle id="@ID@" cx="{dx:.0f}" cy="{dy:.0f}" r="11" fill="{RED}" style="opacity:0;filter:drop-shadow(0 0 8px {RED})"/>', "dt")
    s.pop(dot, t + 0.9, 0.3, 0.3, "50% 50%"); cue(t + 0.9, "tick-crisp_" + str(k % 3 + 1), -20)
    exp = s.path(f"M {dx:.0f} {dy:.0f} L {dx + 90:.0f} {dy + 40:.0f} L {dx + 200:.0f} {dy + 70:.0f}", RED, 3, drawn=True, extra='stroke-dasharray="10 8"', style="opacity:0")
    s.fade(exp, ix(54) + k * 0.1, 0.4)
    tl(f'tl.to("#{exp}", {{opacity: 0.25, duration: 0.4}}, {ix(61):.3f});')
    post = [(dx, dy)]
    for j in range(1, 9):
        post.append((dx + j * 25, dy - j * j * 1.6 - j * 3 - r2.uniform(-6, 6)))
    up = s.path("M " + " L ".join(f"{x:.0f} {y:.0f}" for x, y in post), GOLD, 5, style="filter:drop-shadow(0 0 8px rgba(232,194,106,0.8))")
    s.draw(up, ix(61) + k * 0.15, 1.0)
    toplab(s, l1, l2, t, nxt[k], WHITE, LBL, 40)
cue(ix(54), "whoosh-short_2", -22); cue(ix(61), "swell_2", -18)
s.label(540, 1380, "ILLUSTRATIVE CHARTS · NOT ACTUAL PRICES", 28, GREY, 1, 600, 0.04)
toplab(s, "", "YOU'D EXPECT THE STOCKS TO SUFFER", ix(53), ix(59), RED, LBL, 40)
toplab(s, "YEARS LATER", "EVERY ONE WAS FAR HIGHER", ix(59), c2, GOLD, LBL, 44)

# 3  "Not because of the scandal. Timing doesn't prove cause. They rose because the businesses kept growing. Products, customers, earnings."
s = S(ix(68) - 0.1, ix(87) - 0.1, ground=False, hide=False, restore=False)
toplab(s, "NOT BECAUSE OF THE SCANDAL", "TIMING ≠ CAUSE", ix(68), ix(77) - 0.1, WHITE, LBL, 56)
hd = s.raw(f'<g id="@ID@" style="opacity:0"><circle cx="300" cy="840" r="70" fill="none" stroke="{RED}" stroke-width="5"/>'
           f'<text x="300" y="851" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" fill="{RED}">NEWS</text></g>', "hd")
tr = s.raw(f'<g id="@ID@" style="opacity:0"><circle cx="780" cy="840" r="70" fill="none" stroke="{GOLD}" stroke-width="5"/>'
           f'<path d="M 740 870 L 770 840 L 790 852 L 822 812" fill="none" stroke="{GOLD}" stroke-width="6" stroke-linecap="round"/></g>', "tr")
s.pop(hd, ix(70), 0.35, 0.5, "50% 50%"); s.pop(tr, ix(71), 0.35, 0.5, "50% 50%")
lk = s.path("M 380 840 H 700", "#ffffff80", 4, drawn=True, extra='stroke-dasharray="14 10"', style="opacity:0"); s.fade(lk, ix(72), 0.4)
bx = s.path("M 510 800 L 570 880 M 570 800 L 510 880", RED, 7); s.draw(bx, ix(75) - 0.1, 0.3); cue(ix(75) - 0.1, "tock_1", -16)
for i_ in (hd, tr, lk, bx):
    tl(f'tl.to("#{i_}", {{opacity: 0, duration: 0.3}}, {ix(77) - 0.3:.3f});')
toplab(s, "THEY ROSE BECAUSE", "THE BUSINESS KEPT GROWING", ix(77), ix(87) - 0.1, GOLD, LBL, 44)
bl = s.path("M 110 1150 H 970", "#ffffff60", 3); s.draw(bl, ix(78), 0.6)
for k, (lab, w_) in enumerate([("PRODUCTS", 84), ("CUSTOMERS", 85), ("EARNINGS", 86)]):
    x, h = 250 + k * 290, 140 + k * 110
    gh = s.raw(f'<rect id="@ID@" x="{x - 110}" y="{1150 - h}" width="220" height="{h}" rx="10" fill="none" stroke="#ffffff40" stroke-width="2.5" stroke-dasharray="10 8" style="opacity:0"/>', "gh")
    s.fade(gh, ix(79) + k * 0.15, 0.4)
    b = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="{x - 110}" y="{1150 - h}" width="220" height="{h}" rx="10" fill="{GOLD}" fill-opacity="{0.35 + k * 0.25}" stroke="{GOLD}" stroke-width="3"/>'
              f'<text x="{x}" y="1200" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" fill="#fff">{lab}</text></g>', "bk")
    tl(f'tl.fromTo("#{b}", {{opacity: 0, y: 40}}, {{opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.6)", immediateRender: false}}, {ix(w_) - 0.1:.3f});')
    cue(ix(w_) - 0.1, "pop_" + str(k + 1), -18)
ar = s.path("M 170 960 L 900 700 M 900 700 L 856 694 M 900 700 L 876 737", GOLD, 6, style="filter:drop-shadow(0 0 10px rgba(232,194,106,0.8))"); s.draw(ar, ix(84) - 0.1, ix(86) + 0.25 - ix(84), "power1.inOut")

# 4  "The headline lasted a week. The trend lasted years."
s = S(ix(87) - 0.1, ix(96) - 0.1, ground=False, hide=False)
s.label(130, 820, "THE HEADLINE", 34, RED, 1, 800, 0.08, "start")
hb = s.raw(f'<rect id="@ID@" x="130" y="850" width="0" height="60" rx="10" fill="{RED}"/>', "hb")
tl(f'tl.fromTo("#{hb}", {{attr: {{width: 0}}}}, {{attr: {{width: 110}}, duration: 0.4, ease: "power2.out", immediateRender: false}}, {ix(89):.3f});')
hw = s.label(260, 892, "1 WEEK", 30, WHITE, 0, 800, 0.08, "start"); s.fade(hw, ix(91) - 0.1, 0.3)
s.label(130, 1040, "THE TREND", 34, GOLD, 1, 800, 0.08, "start")
tb = s.raw(f'<rect id="@ID@" x="130" y="1070" width="0" height="60" rx="10" fill="{GOLD}" style="filter:drop-shadow(0 0 12px rgba(232,194,106,0.6))"/>', "tb")
tl(f'tl.fromTo("#{tb}", {{attr: {{width: 0}}}}, {{attr: {{width: 820}}, duration: 1.4, ease: "power2.out", immediateRender: false}}, {ix(93):.3f});')
ty = s.label(940, 1180, "YEARS", 40, GOLD, 0, 800, 0.15, "end"); s.fade(ty, ix(95) - 0.1, 0.35)
cue(ix(89), "tick_1", -18); cue(ix(93), "swell_1", -18)

# 5  "So next time the news is screaming, ask one question. Does this change the business or just the conversation?"
s = S(ix(96) - 0.1, ix(115) - 0.1)
y5 = s.fig(540, 1.0, WHITE); s.pop(y5, ix(96), 0.4)
for k, (x, y) in enumerate([(300, 820), (780, 820), (240, 1020), (840, 1020)]):
    n = s.raw(f'<g id="@ID@" style="opacity:0">{paper(x, y, 160, 110)}</g>', "np")
    s.pop(n, ix(99) + k * 0.1, 0.3, 0.5, "50% 50%")
    tl(f'tl.fromTo("#{n}", {{x: -4}}, {{x: 4, duration: 0.06, repeat: 9, yoyo: true, ease: "none", immediateRender: false}}, {ix(102) + k * 0.05:.3f});')
    tl(f'tl.to("#{n}", {{opacity: 0.12, duration: 0.4}}, {ix(103) - 0.2:.3f});')
cue(ix(102), "tock_1", -18)
toplab(s, "NEXT TIME THE NEWS IS", "SCREAMING", ix(96), ix(103) - 0.1, RED, LBL, 56)
toplab(s, "", "ASK ONE QUESTION", ix(103), ix(106) - 0.1, GOLD, LBL, 52)
q1 = s.label(540, 520, "DOES THIS CHANGE", 34, WHITE, 0, 800, 0.08); s.fade(q1, ix(106), 0.35, y=10)
q2 = s.label(540, 600, "THE BUSINESS?", 56, GOLD, 0, 800, 0.06); s.fade(q2, ix(109) - 0.1, 0.35, y=10)
q3 = s.label(540, 680, "OR JUST THE CONVERSATION?", 36, "#9aa0a8", 0, 800, 0.06); s.fade(q3, ix(111) - 0.1, 0.35, y=10)
cue(ix(109) - 0.1, "bell_C5", -18)

# 6  "Trade the trend, not the gossip."
s = S(ix(115) - 0.1, ix(121) + 0.35)
s.spot(540, 1, "232,194,106")
y6 = s.fig(540, 1.0, GOLD); s.pop(y6, ix(115) - 0.1, 0.4)
t6 = s.label(540, 640, "TRADE THE TREND", 60, GOLD, 0, 800, 0.06)
tl(f'tl.fromTo("#{t6}", {{opacity: 0, scale: 1.3, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.45, ease: "expo.out", immediateRender: false}}, {ix(115) - 0.05:.3f});')
g6 = s.label(540, 740, "NOT THE GOSSIP", 44, "#9aa0a8", 0, 800, 0.06); s.fade(g6, ix(118) - 0.1, 0.35, y=10)
st6 = s.path("M 330 728 H 750", RED, 6); s.draw(st6, ix(120) - 0.15, 0.3)
cue(ix(115), "bell_G5", -16); cue(ix(120) - 0.15, "tock_1", -18)

# 7  outro (handles, no end card)
s = S(ix(121) + 0.3, TOTAL)
es = s.spot(540, 0, "232,194,106", 40, 230); s.fade(es, ix(121) + 0.35, 0.6)
em = s.raw('<image id="@ID@" href="assets/otm_emblem.png" x="390" y="900" width="300" height="291" style="opacity:0;filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>', "i")
s.pop(em, ix(121) + 0.35, 0.7, 0.6, "50% 50%"); cue(ix(121) + 0.35, "bell_A4", -16)
o1l = s.label(540, 1300, "ORDER THE MARKET", 32, GOLD, 0, 800, 0.3); s.fade(o1l, ix(121) + 0.55, 0.5)
o2 = s.label(540, 1360, "DON'T LET THE MARKET ORDER YOU", 28, WHITE, 0, 700, 0.12); s.fade(o2, ix(124), 0.4)
o3 = s.pill(540, 1470, "FOLLOW FOR MORE", GOLD, "#111", 30); s.pop(o3, ix(130), 0.4, 0.6, "50% 50%"); cue(ix(130), "click-confirm_1", -16)
hx = 290
soc = s.raw(f'<g id="@ID@" style="opacity:0">'
            f'<rect x="{hx}" y="1548" width="36" height="36" rx="10" fill="none" stroke="#fff" stroke-width="3"/>'
            f'<circle cx="{hx + 18}" cy="1566" r="8.5" fill="none" stroke="#fff" stroke-width="3"/><circle cx="{hx + 28}" cy="1556" r="2.4" fill="#fff"/>'
            f'<text x="{hx + 48}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@fxzuez_28</text>'
            f'<path d="M {hx + 322} 1546 V 1574 A 9 9 0 1 1 {hx + 313} 1565 M {hx + 322} 1546 Q {hx + 326} 1557 {hx + 338} 1558" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>'
            f'<text x="{hx + 348}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@zuez_28</text></g>', "so")
disc = s.label(540, 1650, "EDUCATIONAL ONLY · NOT FINANCIAL ADVICE", 28, GREY, 0, 600, 0.12)
s.fade(soc, ix(124) + 0.6, 0.5, y=12)
s.fade(disc, ix(124) + 0.9, 0.5)
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
    <div id="root" data-composition-id="otm-headlines" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
{TIMELINE}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-headlines-audio" class="clip" src="assets/audio/mix_headlines.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-headlines"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
