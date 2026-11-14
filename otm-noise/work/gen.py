"""OTM "The Noise": a glowing-figure explainer (same system as otm-circle / otm-anyway / otm-know). Voice only, no music. White soft-glow figures on a dashed ground line, spotlights, small
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

# 1  some of the best traders are quietly stepping away from the noise
s = S(0, A("not") - 0.05, first=True)
s.label(540, 560, "THE NOISE", 30, LBL, 1)
s.raw('<rect id="@ID@" x="140" y="700" width="800" height="470" rx="18" fill="none" stroke="#ffffff70" stroke-width="2" stroke-dasharray="10 10"/>')
crowd = []
r1 = random.Random(1)
for row, gy in enumerate([870, 1010, 1150]):
    for col in range(6):
        x = 230 + col * 124
        f = s.fig(x, 0.42, "#e6e9ee", 1, True, gy=gy)
        bd = badge(s, x + 24, gy - 82)
        d_, t_ = r1.uniform(0.18, 0.35), r1.uniform(0.2, 1.2)
        if len(crowd) not in (11, 12):                          # the two who step away stop blinking first
            tl(f'tl.to("#{bd}", {{opacity: 0.25, duration: {d_:.2f}, yoyo: true, repeat: 7, ease: "none"}}, {t_:.2f});')
        crowd.append((f, bd, x, gy))
for (f, bd, x, gy), dx in [(crowd[11], 180), (crowd[12], -170)]:
    s.walk(f, A("stepping") - 0.1, dx, 1.4)
    tl(f'tl.to("#{bd}", {{opacity: 0, duration: 0.3}}, {A("stepping") + 0.3:.3f});')
cue(A("stepping"), "whoosh-short_1", -22)

# 2  not because they quit; they started questioning the way we're told to trade
s = S(A("not") - 0.05, A("six") - 0.05)
s.label(540, 560, "HOW WE'RE TOLD TO TRADE", 30, LBL, 1)
q2 = s.fig(200, 1.0); s.pop(q2, A("not"), 0.4)
qm = s.pill(200, 930, "?", GOLD, "#111", 34); s.pop(qm, A("questioning"), 0.35, 0.4, "50% 50%"); cue(A("questioning"), "pop_2", -18)
steps = ["LEARN", "TRADE ALL DAY", "POST EVERY WIN", "REPEAT"]
for k, txt in enumerate(steps):
    y = 740 + k * 120
    p = s.pill(660, y, txt, "#2a2f38", WHITE, 30); s.pop(p, A("quit") + k * 0.3, 0.35, 0.5, "50% 50%")
    if k: ar = s.path(f"M 660 {y - 88} V {y - 34} M 648 {y - 46} L 660 {y - 34} L 672 {y - 46}", "#ffffff80", 3); s.draw(ar, A("quit") + k * 0.3 - 0.1, 0.25)
    cue(A("quit") + k * 0.3, "tick_" + str(k % 3 + 1), -22)
lk = s.path("M 660 1150 Q 900 1150 900 940 Q 900 740 790 740", "#ffffff50", 3); s.draw(lk, A("told"), 0.7)

# 3  six screens, every session, every signal group, every new indicator
s = S(A("six") - 0.05, A("stare") - 0.65, ground=False)
cells = [(300, 820, "6 SCREENS", A("six")), (780, 820, "EVERY SESSION", A("every", 1)), (300, 1120, "SIGNAL GROUPS", A("every", 2)), (780, 1120, "NEW INDICATORS", A("every", 3))]
for k, (x, y, lab, t) in enumerate(cells):
    if k == 0:
        ids = screens(s, x - 125, y - 85, 3, 2, 72, 48, 14)
        for j, i in enumerate(ids): s.pop(i, t + j * 0.05, 0.25, 0.4, "50% 50%")
    elif k == 1:
        ic = s.raw(f'<g id="@ID@" style="opacity:0"><circle cx="{x}" cy="{y - 20}" r="68" fill="none" stroke="#fff" stroke-width="3"/>'
                   f'<path d="M {x} {y - 88} A 68 68 0 0 1 {x + 59} {y + 14}" fill="none" stroke="{GOLD}" stroke-width="7"/>'
                   f'<path d="M {x + 59} {y + 14} A 68 68 0 0 1 {x - 59} {y + 14}" fill="none" stroke="#8fb6ff" stroke-width="7"/>'
                   f'<path d="M {x - 59} {y + 14} A 68 68 0 0 1 {x} {y - 88}" fill="none" stroke="#ffffffb0" stroke-width="7"/>'
                   f'<line x1="{x}" y1="{y - 20}" x2="{x}" y2="{y - 70}" stroke="#fff" stroke-width="4"/><line x1="{x}" y1="{y - 20}" x2="{x + 30}" y2="{y - 20}" stroke="#fff" stroke-width="4"/></g>')
        s.pop(ic, t, 0.35, 0.5, "50% 50%")
    elif k == 2:
        ic = s.raw(f'<g id="@ID@" style="opacity:0"><path d="M {x - 85} {y - 95} H {x + 85} Q {x + 100} {y - 95} {x + 100} {y - 80} V {y + 5} Q {x + 100} {y + 20} {x + 85} {y + 20} '
                   f'H {x - 40} L {x - 70} {y + 45} V {y + 20} H {x - 85} Q {x - 100} {y + 20} {x - 100} {y + 5} V {y - 80} Q {x - 100} {y - 95} {x - 85} {y - 95} Z" fill="none" stroke="#fff" stroke-width="3"/>'
                   f'<line x1="{x - 70}" y1="{y - 55}" x2="{x + 60}" y2="{y - 55}" stroke="#ffffff90" stroke-width="3"/><line x1="{x - 70}" y1="{y - 22}" x2="{x + 20}" y2="{y - 22}" stroke="#ffffff90" stroke-width="3"/>'
                   f'<rect x="{x + 50}" y="{y - 120}" width="92" height="50" rx="25" fill="{RED}"/><text x="{x + 96}" y="{y - 85}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" fill="#fff">99+</text></g>')
        s.pop(ic, t, 0.35, 0.5, "50% 50%")
    else:
        lines = "".join(f'<path d="M {x - 100} {y - 30 + j * 6} C {x - 50} {y - 90 + j * 25}, {x} {y + 10 - j * 15}, {x + 100} {y - 70 + j * 18}" fill="none" stroke="{c}" stroke-width="3"/>'
                        for j, c in enumerate(["#fff", GOLD, "#8fb6ff", "#ff9aa3", "#9aff9a"]))
        ic = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="{x - 110}" y="{y - 110}" width="220" height="140" rx="10" fill="none" stroke="#fff" stroke-width="3"/>{lines}</g>')
        s.pop(ic, t, 0.35, 0.5, "50% 50%")
    lb = s.label(x, y + 75, lab, 28, WHITE, 0, 800, 0.1); s.fade(lb, t + 0.15, 0.3)
    cue(t, "pop_" + str(k + 1), -20)

# 4  stare at charts all day, take every move, barely time to enjoy what you make
t4 = A("stare")
s = S(t4 - 0.65, A("somehow") - 0.05)
s.label(540, 560, "ALL DAY", 30, LBL, 1)
scr = screens(s, 250, 760, 3, 2, 120, 80, 18)
s.raw('<g id="@ID@"><rect x="230" y="1100" width="460" height="14" fill="#fff" opacity="0.85"/>'
      '<line x1="250" y1="1114" x2="250" y2="1240" stroke="#fff" stroke-width="5" opacity="0.7"/><line x1="670" y1="1114" x2="670" y2="1240" stroke="#fff" stroke-width="5" opacity="0.7"/></g>')
k4 = s.fig(460, 0.85, gy=1180)
tl(f'tl.to("#{k4}", {{x: -10, duration: 0.12, yoyo: true, repeat: 9, ease: "sine.inOut"}}, {A("every", 4):.3f});')
cue(A("every", 4), "tick-crisp_1", -22)
pie = s.raw(f'<g id="@ID@" style="opacity:0"><circle cx="860" cy="860" r="90" fill="none" stroke="#ffffff40" stroke-width="40"/></g>', "pi")
s.fade(pie, A("barely") - 0.3, 0.3)
pa = s.raw(f'<circle id="@ID@" cx="860" cy="860" r="90" fill="none" stroke="#fff" stroke-width="40" pathLength="1" transform="rotate(-90 860 860)" '
           f'style="stroke-dasharray:1 1.2;stroke-dashoffset:1.1"/>', "pa")
tl(f'tl.fromTo("#{pa}", {{strokeDashoffset: 1.1}}, {{strokeDashoffset: 0.1, duration: 0.8, ease: "power2.inOut", immediateRender: false}}, {A("barely"):.3f});')
pl1 = s.label(860, 1010, "CHARTS 90%", 28, WHITE, 0, 800, 0.08); s.fade(pl1, A("barely") + 0.4, 0.3)
pl2 = s.label(860, 1050, "LIFE 10%", 28, GOLD, 0, 800, 0.08); s.fade(pl2, A("enjoy"), 0.3); cue(A("enjoy"), "land-light_1", -18)

# 5  and somehow everyone calls that normal
s = S(A("somehow") - 0.05, A("you're") - 0.05)
for row, gy in enumerate([900, 1070, 1240]):
    for col in range(3):
        x = 230 + col * 310
        d = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="{x - 70}" y="{gy - 40}" width="140" height="10" fill="#fff" opacity="0.7"/>'
                  f'<rect x="{x + 5}" y="{gy - 100}" width="70" height="50" rx="5" fill="#0b1220" stroke="#fff" stroke-width="2" style="filter:drop-shadow(0 0 8px rgba(120,180,255,0.5))"/></g>', "dk")
        s.fade(d, A("somehow") + (row * 3 + col) * 0.05, 0.3)
        f = s.fig(x - 30, 0.42, "#d9dde3", 0.9, gy=gy - 30); s.pop(f, A("somehow") + (row * 3 + col) * 0.05, 0.3)
nm = s.pill(540, 690, "NORMAL", GOLD, "#111", 34); s.pop(nm, A("normal"), 0.4, 0.5, "50% 50%"); cue(A("normal"), "bell_C5", -20)

# 6  post every win, chase the leaderboard, copy a lifestyle that doesn't make you happy
s = S(A("you're") - 0.05, A("question") - 0.05)
pn = s.path(rrect(180, 650, 720, 330, 20), WHITE, 3); s.draw(pn, A("supposed"), 0.5)
s.label(220, 705, "LEADERBOARD", 28, LBL, 0, 800, 0.2, "start"); s.fade(s.items[-1].split('"')[1], A("supposed") + 0.2, 0.3)
for k, (nm6, pct, col) in enumerate([("#1  @LAMBO_FX", "+480%", GOLD), ("#2  @SIGNAL_KING", "+390%", WHITE), ("#3  YOU", "+12%", GREY)]):
    y = 780 + k * 70
    a = s.label(220, y, nm6, 28, col, 0, 800, 0.04, "start"); b = s.label(860, y, pct, 28, col, 0, 800, 0.04, "end")
    s.fade(a, A("leaderboard") + k * 0.15, 0.3); s.fade(b, A("leaderboard") + k * 0.15, 0.3)
cue(A("leaderboard"), "tick_2", -22)
y6 = s.fig(540, 1.0); s.pop(y6, A("supposed"), 0.4)
po = s.pill(300, 1080, "POST WIN", "#2a2f38", WHITE, 28); s.pop(po, A("post"), 0.3, 0.5, "50% 50%"); cue(A("post"), "pop_1", -20)
st = s.raw(f'<path id="@ID@" d="M 780 1000 L 795 1040 L 838 1042 L 804 1068 L 816 1110 L 780 1085 L 744 1110 L 756 1068 L 722 1042 L 765 1040 Z" fill="{GOLD}" '
           f'style="opacity:0;filter:drop-shadow(0 0 14px {GOLD})"/>', "st")
s.pop(st, A("lifestyle"), 0.35, 0.4, "50% 50%"); cue(A("lifestyle"), "bell_G5", -22)
tl(f'tl.to("#{st}", {{opacity: 0.2, duration: 0.5}}, {A("happy") - 0.2:.3f});')
tl(f'tl.to("#{y6}", {{opacity: 0.45, duration: 0.5}}, {A("happy") - 0.2:.3f});')
hp = s.label(540, 1300, "DOESN'T MAKE YOU HAPPY", 28, WHITE, 0, 800, 0.1); s.fade(hp, A("lifestyle") + 0.4, 0.35)

# 7  question any of it and people say that's just how trading works
s = S(A("question") - 0.05, A("so") - 0.05)
s.raw(f'<g id="@ID@"><rect x="110" y="880" width="140" height="110" rx="8" fill="none" stroke="#fff" stroke-width="3"/>'
      f'<line x1="180" y1="990" x2="180" y2="1060" stroke="#fff" stroke-width="3"/>'
      f'<text x="180" y="958" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="60" fill="{GOLD}">?</text></g>')
q7 = s.fig(180, 0.9); s.pop(q7, A("question"), 0.4)
for k, x in enumerate([500, 610, 720, 830, 940]):
    f = s.fig(x, 0.7, "#cfd3da", 0.85); s.pop(f, A("people") + k * 0.06, 0.35)
big = s.pill(720, 880, "THAT'S HOW IT WORKS", WHITE, "#111", 28); s.pop(big, A("people") + 0.2, 0.35, 0.5, "50% 50%"); cue(A("people") + 0.2, "land-light_1", -18)
for k, (txt, x) in enumerate([("JUST GRIND", 560), ("MORE TRADES", 850)]):
    p = s.pill(x, 990, txt, "#2a2f38", WHITE, 28); s.pop(p, A("people") + 0.4 + k * 0.25, 0.3, 0.5, "50% 50%")

# 8  so some traders slowly stop playing along
s = S(A("so") - 0.05, A("close") - 0.05)
s.label(540, 560, "THE GAME", 30, LBL, 1)
bd8 = s.path(rrect(200, 680, 620, 470, 20), WHITE, 3); s.draw(bd8, A("so"), 0.6)
sq = ""
for i in range(7):
    sq += f'<rect x="{214 + i * 85}" y="694" width="70" height="60" rx="6" fill="none" stroke="#ffffff70" stroke-width="2"/>'
    sq += f'<rect x="{214 + i * 85}" y="1076" width="70" height="60" rx="6" fill="none" stroke="#ffffff70" stroke-width="2"/>'
sqg = s.raw(f'<g id="@ID@" style="opacity:0">{sq}<text x="510" y="930" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="40" letter-spacing="0.2em" fill="#fff">THE GAME</text></g>')
s.fade(sqg, A("so") + 0.3, 0.4)
pcs = [s.fig(x, 0.4, "#e6e9ee", 1, gy=1060) for x in (330, 430, 590, 690)]
for i, f in enumerate(pcs): s.pop(f, A("traders", 2) + i * 0.08, 0.3)
s.walk(pcs[3], A("slowly"), 260, 1.3)
tl(f'tl.to("#{pcs[3]}", {{y: 180, duration: 0.5, ease: "power2.in"}}, {A("slowly") + 1.36:.3f});')
cue(A("playing"), "whoosh-short_2", -20)

# 9  close the extra charts, leave the signal groups, a few clean setups a week, log off
s = S(A("close") - 0.05, A("maybe") - 0.05)
s.label(540, 560, "STEP AWAY", 30, LBL, 1)
scr9 = screens(s, 285, 650, 3, 2, 150, 90, 20)
for j in range(5):
    r, c = divmod(j + 1, 3)
    o = s.raw(f'<rect id="@ID@" x="{285 + c * 170}" y="{650 + r * 110}" width="150" height="90" rx="6" fill="#03050a" stroke="#ffffff40" stroke-width="2" style="opacity:0"/>', "of")
    tl(f'tl.set("#{o}", {{opacity: 1}}, {A("close") + 0.15 + j * 0.15:.3f});')
    cue(A("close") + 0.15 + j * 0.15, "click_" + str(j % 2 + 1), -22)
lg = s.pill(540, 920, "YOU LEFT THE GROUP", "#2a2f38", WHITE, 28); s.pop(lg, A("leave"), 0.35, 0.5, "50% 50%"); cue(A("leave"), "tick_1", -20)
for k, d in enumerate(["MON", "TUE", "WED", "THU", "FRI"]):
    x = 260 + k * 140
    s.raw(f'<g id="@ID@"><rect x="{x - 50}" y="1000" width="100" height="90" rx="10" fill="none" stroke="#ffffff90" stroke-width="2"/></g>')
    lb = s.label(x, 990, d, 28, GREY, 1, 700, 0.1)
    if k in (1, 3):
        ck = s.path(f"M {x - 22} 1045 L {x - 4} 1065 L {x + 26} 1025", GOLD, 7); s.draw(ck, A("take", 2) + 0.3 + (k == 3) * 0.3, 0.25)
        cue(A("take", 2) + 0.3 + (k == 3) * 0.3, "pop_" + str(k), -20)
fg9 = s.fig(140, 0.8)
lo = s.pill(540, 1180, "LOGGED OFF", GOLD, "#111", 30); s.pop(lo, A("log"), 0.35, 0.5, "50% 50%"); cue(A("log"), "click-confirm_1", -16)
tl(f'tl.set("#{scr9[0]}", {{opacity: 0.15}}, {A("log"):.3f});')

# 10  maybe that's what the noise doesn't understand
s = S(A("maybe") - 0.05, A("less") - 0.45)
s.label(540, 560, "THE NOISE DOESN'T GET IT", 30, LBL, 1)
for k, x in enumerate([130, 250, 370]):
    f = s.fig(x, 0.75, "#9aa0a8", 0.8, False); s.pop(f, A("maybe") + k * 0.08, 0.35)
    b = badge(s, x + 40, 1080); s.pop(b, A("noise", 2) + k * 0.1, 0.25, 0.3, "50% 50%")
    q = s.pill(x, 990, "?", "#2a2f38", WHITE, 28); s.pop(q, A("understand") - 0.2 + k * 0.1, 0.3, 0.5, "50% 50%")
cue(A("noise", 2), "pop_4", -22)
tr10 = tree(s, 900); s.fade(tr10, A("maybe"), 0.5)
hs10 = house(s, 700); s.fade(hs10, A("maybe") + 0.2, 0.5)
me10 = s.fig(810, 0.85); s.pop(me10, A("maybe") + 0.3, 0.4)

# 11  trading less doesn't mean you're losing
s = S(A("less") - 0.45, A("sometimes") - 0.05)
s.label(540, 560, "TRADING LESS", 30, LBL, 1)
for x0, lab, col in [(150, "MORE TRADES", WHITE), (580, "FEWER TRADES", GOLD)]:
    s.path(f"M {x0} 700 V 1080 H {x0 + 350}", "#ffffff50", 2, drawn=True)
    lb = s.label(x0 + 175, 1130, lab, 28, col, 0, 800, 0.1); s.fade(lb, A("less"), 0.35)
jag = "M 160 900 " + " ".join(f"L {170 + i * 20} {900 + (40 if i % 2 else -40) + (i % 5) * 6}" for i in range(17))
jp = s.path(jag, "#ffffffc0", 3); s.draw(jp, A("less"), 0.9, "none")
sm = s.path("M 590 1040 C 690 1020 760 980 830 900 S 900 760 930 730", GOLD, 6); s.draw(sm, A("mean"), 0.9)
gk = s.raw(f'<g id="@ID@" style="opacity:0"><circle cx="930" cy="700" r="26" fill="{GOLD}"/><path d="M 918 700 L 927 710 L 943 690" fill="none" stroke="#111" stroke-width="5" stroke-linecap="round"/></g>', "ck")
s.pop(gk, A("losing"), 0.35, 0.3, "50% 50%"); cue(A("losing"), "bell_E5", -18)

# 12  the best trade is the one that gives you your life back
s = S(A("sometimes") - 0.05, A("order") - 0.05)
sun = s.raw(f'<g id="@ID@"><circle cx="540" cy="1240" r="150" fill="{GOLD}" opacity="0.9" style="filter:drop-shadow(0 0 40px {GOLD})"/></g>', "sun")
s.items.append('<rect x="0" y="1242" width="1080" height="700" fill="#000"/>')
tl(f'tl.fromTo("#{sun}", {{y: 160}}, {{y: 0, duration: 2.6, ease: "power2.out", immediateRender: false}}, {A("sometimes"):.3f});')
tr12 = tree(s, 850); s.fade(tr12, A("sometimes") + 0.3, 0.5)
me12 = s.fig(330, 1.0); s.pop(me12, A("sometimes") + 0.2, 0.4)
lap = s.raw('<path id="@ID@" d="M 420 1240 L 430 1222 L 500 1222 L 510 1240 Z" fill="none" stroke="#fff" stroke-width="3" style="opacity:0"/>', "lp")
s.fade(lap, A("sometimes") + 0.4, 0.4)
lb12 = s.label(540, 780, "YOUR LIFE BACK", 40, GOLD, 0, 800, 0.2); s.fade(lb12, A("life"), 0.5, y=12); cue(A("life"), "swell_2", -18)

# 13  order the market (outro with handles; no end card)
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
s.fade(soc, A("market", 2) + 0.2, 0.5, y=12)
s.fade(disc, A("market", 2) + 0.5, 0.5)

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
    <div id="root" data-composition-id="otm-noise" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-noise-audio" class="clip" src="assets/audio/mix_noise.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-noise"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
