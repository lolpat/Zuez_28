"""OTM "The Black Dot": a glowing-figure trading video in the OTM style (same scene system as otm-missed), inspired by
the white-shirt-and-one-black-dot story. A month of 20 trades (14 wins, 6 losses, account up), yet the trader only talks
about the one trade that hit the stop at the worst moment: the black dot on a white shirt. A loss hurts about twice as
much as a win feels good, so one red trade feels like the whole story, and traders break their rules (move the stop,
double the size, win it back). Judge your trading by the whole shirt: win rate, average win vs. average loss,
discipline over a hundred trades. One loss is a data point, not a verdict.
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

def hide(i, t, d=0.3):
    tl(f'tl.to("#{i}", {{opacity: 0, duration: {d}}}, {t:.3f});')

SHIRT = ("M -90 -240 Q 0 -165 90 -240 L 250 -195 L 330 -60 L 240 -15 L 200 -80 L 200 240 Q 0 252 -200 240 "
         "L -200 -80 L -240 -15 L -330 -60 L -250 -195 Z")

def shirt(s, x, y, sc=1.0, dx=30, dy=20, r=16):
    """A glowing white T-shirt with one black dot. Returns (group id, dot id, dot centre on screen)."""
    g, d = s.uid("sh"), s.uid("dt")
    s.raw(f'<g transform="translate({x},{y}) scale({sc})"><g id="{g}" style="opacity:0;filter:drop-shadow(0 0 22px rgba(255,255,255,0.45))">'
          f'<path d="{SHIRT}" fill="#f4f4f2" stroke="#ffffff" stroke-width="3" stroke-linejoin="round"/>'
          f'<circle id="{d}" cx="{dx}" cy="{dy}" r="{r}" fill="#0b0b0b"/></g></g>', "x")
    return g, d, (x + dx * sc, y + dy * sc)

def outline(s, x, y, sc=1.0, col=GOLD):
    return s.raw(f'<g transform="translate({x},{y}) scale({sc})"><path id="@ID@" d="{SHIRT}" fill="none" stroke="{col}" stroke-width="7" '
                 f'stroke-linejoin="round" pathLength="1" style="stroke-dasharray:1 1.2;stroke-dashoffset:1.1;filter:drop-shadow(0 0 12px rgba(232,194,106,0.9))"/></g>', "ol")

def xmark(s, x, y, t, r=16):
    m = s.path(f"M {x - r} {y - r} L {x + r} {y + r} M {x + r} {y - r} L {x - r} {y + r}", RED, 6); s.draw(m, t, 0.3)
    return m

LOSS = {3, 7, 10, 14, 16, 19}
def trade_grid(s, x0, y0, size, gap, t_win, t_loss, glyph=True, stag=(0.05, 0.07), out_t=None):
    """5 x 4 month of trades: 14 gold wins, 6 red losses. Dashed slots visible from the start, or faded in at out_t. Returns {k: id}."""
    out, wj, lj, slots, at = {}, 0, 0, "", len(s.items)
    for k in range(20):
        c, r = k % 5, k // 5
        x, y = x0 + c * (size + gap), y0 + r * (size + gap)
        slots += f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{size * 0.13:.0f}" fill="none" stroke="#ffffff38" stroke-width="2.5" stroke-dasharray="8 7"/>'
        lo = k in LOSS; col = RED if lo else GOLD
        cx, cy, a = x + size / 2, y + size / 2, size * 0.2
        gl = (f'<path d="M {cx - a} {cy + (-a / 2 if lo else a / 2)} L {cx} {cy + (a / 2 if lo else -a / 2)} L {cx + a} {cy + (-a / 2 if lo else a / 2)}" '
              f'fill="none" stroke="#0b0b0b" stroke-width="{size * 0.07:.1f}" stroke-linecap="round" stroke-linejoin="round"/>') if glyph else ""
        i_ = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 10px {col}88)"><rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{size * 0.13:.0f}" fill="{col}"/>{gl}</g>', "q")
        if lo: s.pop(i_, t_loss + lj * stag[1], 0.3, 0.5, "50% 50%"); lj += 1
        else: s.pop(i_, t_win + wj * stag[0], 0.3, 0.5, "50% 50%"); wj += 1
        out[k] = i_
    sg = s.raw(f'<g id="@ID@" style="opacity:{0 if out_t is not None else 1}">{slots}</g>', "o")
    s.items.insert(at, s.items.pop())               # slots sit under the squares
    if out_t is not None: s.fade(sg, out_t, 0.3)
    return out

# 1  "Twenty trades this month. Fourteen winners. Six losers. The account is up."
s = S(0, ix(12) + 0.2, first=True)
s.label(540, 560, "20 TRADES THIS MONTH", 52, WHITE, 1, 800, 0.04)
trade_grid(s, 221, 660, 110, 22, ix(4) - 0.1, ix(6) - 0.1)
cue(ix(4) - 0.1, "pop_1", -20); cue(ix(6) - 0.1, "tock_1", -20)
l1 = s.label(540, 1320, "14 WINNERS", 34, GOLD, 0, 800, 0.15); s.fade(l1, ix(4) - 0.1, 0.3)
l2 = s.label(540, 1380, "6 LOSERS", 34, RED, 0, 800, 0.15); s.fade(l2, ix(6) - 0.1, 0.3)
l3 = s.label(540, 1450, "THE ACCOUNT IS UP", 34, WHITE, 0, 800, 0.1); s.fade(l3, ix(8) - 0.2, 0.35, y=10)
cue(ix(9), "bell_C5", -20)

# 2  "But ask the trader how the month went... and all they talk about is one trade. The one that hit the stop at the worst possible moment."
s = S(ix(12) - 0.1, ix(39) - 0.1)
tr = s.fig(260, 1.0, WHITE); s.pop(tr, ix(12), 0.4)
toplab(s, "", "HOW WAS THE MONTH?", ix(12), ix(20) - 0.1, WHITE, LBL, 52)
toplab(s, "ALL THEY TALK ABOUT IS", "ONE TRADE", ix(20), ix(39) - 0.1, RED, LBL, 60)
b1 = s.raw('<circle id="@ID@" cx="330" cy="1005" r="10" fill="#fff" style="opacity:0"/>', "b")
b2 = s.raw('<circle id="@ID@" cx="375" cy="960" r="16" fill="#fff" style="opacity:0"/>', "b")
cl = s.raw(f'<path id="@ID@" d="{rrect(420, 640, 590, 300, 40)}" fill="#0f1319" stroke="#ffffffaa" stroke-width="3" style="opacity:0"/>', "c")
s.pop(b1, ix(21), 0.25, 0.3, "50% 50%"); s.pop(b2, ix(21) + 0.1, 0.25, 0.3, "50% 50%"); s.pop(cl, ix(21) + 0.2, 0.4, 0.6, "50% 50%")
cue(ix(21), "pop_2", -20)
sl = s.raw(f'<g id="@ID@" style="opacity:0"><line x1="450" y1="868" x2="980" y2="868" stroke="{RED}" stroke-width="3" stroke-dasharray="12 9"/>'
           f'<text x="980" y="848" text-anchor="end" font-family="Montserrat" font-weight="800" font-size="28" letter-spacing="0.1em" fill="{RED}">STOP</text></g>', "sl")
s.fade(sl, ix(26), 0.3)
pre = s.path("M 450 800 L 510 780 L 555 792 L 605 760 L 655 772 L 700 740", "#e9ecf1", 4); s.draw(pre, ix(26), 0.6)
dr = s.path("M 700 740 L 728 800 L 758 905", RED, 5, style="filter:drop-shadow(0 0 8px rgba(255,77,94,0.9))"); s.draw(dr, ix(31) - 0.05, 0.35, "power2.in")
fl = s.raw(f'<circle id="@ID@" cx="745" cy="860" r="18" fill="none" stroke="{RED}" stroke-width="4" style="opacity:0"/>', "fl")
s.pop(fl, ix(32) + 0.05, 0.3, 0.2, "50% 50%"); cue(ix(32), "tock_1", -16)
so = s.label(590, 918, "STOPPED OUT", 28, RED, 0, 800, 0.1); s.fade(so, ix(33), 0.3)
rv = s.path("M 758 905 L 800 845 L 845 862 L 895 770 L 955 680", GOLD, 5, style="filter:drop-shadow(0 0 8px rgba(232,194,106,0.9))"); s.draw(rv, ix(36) - 0.1, 0.9)
cue(ix(36) - 0.1, "whoosh-short_1", -22)

# 3  "That's a black dot on a white shirt. Everyone stares at the dot. Nobody mentions the white."
s = S(ix(39) - 0.1, ix(56) - 0.1)
sh, dt, (dx_, dy_) = shirt(s, 540, 840, 0.85)
s.pop(sh, ix(39) - 0.05, 0.5, 0.6, "50% 50%"); cue(ix(39), "swell_1", -22)
s.pop(dt, ix(41), 0.35, 0.1, "50% 50%"); cue(ix(41), "tick-crisp_1", -16)
toplab(s, "THAT'S A", "BLACK DOT ON A WHITE SHIRT", ix(39), ix(47) - 0.1, WHITE, LBL, 44)
toplab(s, "", "EVERYONE STARES AT THE DOT", ix(47), ix(52) - 0.1, WHITE, LBL, 44)
toplab(s, "NOBODY MENTIONS", "THE WHITE", ix(52), ix(56) - 0.1, GOLD, LBL, 60)
lines = []
for j, x in enumerate([120, 310, 770, 960]):
    f = s.fig(x, 0.55, WHITE); s.pop(f, ix(47) - 0.1 + j * 0.08, 0.35)
    hx, hy = x, GY - 158 * 0.55
    L = math.hypot(dx_ - hx, dy_ - hy); ex, ey = dx_ - (dx_ - hx) / L * 34, dy_ - (dy_ - hy) / L * 34
    ln = s.path(f"M {hx + (dx_ - hx) / L * 30:.0f} {hy + (dy_ - hy) / L * 30:.0f} L {ex:.0f} {ey:.0f}", "#8a9099", 3)
    s.draw(ln, ix(48) + j * 0.08, 0.5); lines.append(ln)
cue(ix(47) - 0.1, "pop_3", -22)
for ln in lines:
    tl(f'tl.to("#{ln}", {{opacity: 0.15, duration: 0.4}}, {ix(52):.3f});')
ol = outline(s, 540, 840, 0.85); s.draw(ol, ix(52) + 0.1, 1.2); cue(ix(52) + 0.1, "swell_2", -20)

# 4  "Our brains are built this way. A loss can hurt about twice as much as a win feels good. So one red trade starts to feel like the whole story."
s = S(ix(56) - 0.1, ix(86) - 0.1, ground=False, restore=False)
toplab(s, "", "OUR BRAINS ARE BUILT THIS WAY", ix(56), ix(63) - 0.1, WHITE, LBL, 44)
toplab(s, "A LOSS CAN HURT", "ABOUT 2× AS MUCH", ix(63) - 0.1, ix(76) - 0.1, RED, LBL, 56)
bl = s.path("M 160 1150 H 920", "#ffffff60", 3); s.draw(bl, ix(56), 0.6)
rb = s.raw(f'<rect id="@ID@" x="250" y="1150" width="220" height="0" rx="10" fill="{RED}" style="filter:drop-shadow(0 0 14px rgba(255,77,94,0.6))"/>', "rb")
tl(f'tl.fromTo("#{rb}", {{attr: {{y: 1150, height: 0}}}}, {{attr: {{y: 730, height: 420}}, duration: 0.9, ease: "power2.out", immediateRender: false}}, {ix(63) - 0.1:.3f});')
gb = s.raw(f'<rect id="@ID@" x="610" y="1150" width="220" height="0" rx="10" fill="{GOLD}" style="filter:drop-shadow(0 0 14px rgba(232,194,106,0.6))"/>', "gb")
tl(f'tl.fromTo("#{gb}", {{attr: {{y: 1150, height: 0}}}}, {{attr: {{y: 940, height: 210}}, duration: 0.6, ease: "power2.out", immediateRender: false}}, {ix(72) - 0.1:.3f});')
x2 = s.label(360, 700, "2×", 48, RED, 0, 800, 0.04); s.fade(x2, ix(67) - 0.1, 0.3, y=10)
lp = s.label(360, 1205, "PAIN OF A LOSS", 28, RED, 0, 800, 0.08); s.fade(lp, ix(63), 0.3)
lw = s.label(720, 1205, "JOY OF A WIN", 28, GOLD, 0, 800, 0.08); s.fade(lw, ix(63) + 0.2, 0.3)
cue(ix(63) - 0.1, "whoosh-short_2", -22); cue(ix(67) - 0.1, "tock_1", -18); cue(ix(72) - 0.1, "pop_1", -22)
for i_ in (bl, rb, gb, x2, lp, lw):
    hide(i_, ix(76) - 0.35)
toplab(s, "ONE RED TRADE", "FEELS LIKE THE WHOLE STORY", ix(76) - 0.1, ix(86) - 0.1, RED, LBL, 44)
g4 = trade_grid(s, 279, 760, 90, 18, ix(76) - 0.05, ix(76) + 0.1, stag=(0.02, 0.02), out_t=ix(76) - 0.1)
for k, i_ in g4.items():
    if k != 7: tl(f'tl.to("#{i_}", {{opacity: 0.12, duration: 0.4}}, {ix(78):.3f});')
tl(f'tl.to("#{g4[7]}", {{scale: 6, transformOrigin: "50% 50%", duration: 1.0, ease: "power2.inOut"}}, {ix(79):.3f});')
cue(ix(79), "swell_1", -18)

# 5  "And that's when traders break their own rules. They move the stop. They double the size. They try to win it back."
s = S(ix(86) - 0.1, ix(108) - 0.1, ground=False, hide=False, restore=False)
toplab(s, "THAT'S WHEN TRADERS", "BREAK THEIR OWN RULES", ix(86), ix(108) - 0.1, RED, LBL, 48)
cd = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(170, 660, 740, 600, 28)}" fill="#0f1319" stroke="#ffffff50" stroke-width="2.5"/>'
           f'<text x="540" y="735" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" letter-spacing="0.25em" fill="{LBL}">MY RULES</text>'
           f'<line x1="220" y1="770" x2="860" y2="770" stroke="#ffffff30" stroke-width="2"/></g>', "cd")
s.pop(cd, ix(86), 0.45, 0.7, "50% 50%")
ck = s.path("M 330 690 L 380 735 L 420 705 L 470 752 L 515 712 L 565 760 L 610 718 L 655 755 L 700 722 L 750 748", RED, 4,
            style="filter:drop-shadow(0 0 6px rgba(255,77,94,0.9))")
s.draw(ck, ix(90) - 0.05, 0.35, "power2.out"); cue(ix(90) - 0.05, "tock_1", -16)
# row 1: move the stop
r1 = s.raw(f'<g id="@ID@" style="opacity:0"><path d="M 220 830 L 255 815 L 290 822 L 330 800 L 360 808" fill="none" stroke="#e9ecf1" stroke-width="4" stroke-linecap="round"/></g>', "r1")
st = s.raw(f'<line id="@ID@" x1="215" y1="855" x2="365" y2="855" stroke="{RED}" stroke-width="4" stroke-dasharray="10 7" style="opacity:0"/>', "st")
t1 = s.label(400, 852, "MOVE THE STOP", 32, WHITE, 0, 800, 0.06, "start")
for i_ in (r1, st, t1): s.fade(i_, ix(95) - 0.1, 0.3)
tl(f'tl.to("#{st}", {{y: 40, duration: 0.5, ease: "power2.inOut"}}, {ix(95) + 0.3:.3f});')
xmark(s, 872, 842, ix(97)); cue(ix(97), "tick_1", -18)
# row 2: double the size
sz = s.raw(f'<rect id="@ID@" x="225" y="965" width="55" height="55" rx="6" fill="{GOLD}" style="opacity:0"/>', "sz")
t2 = s.label(400, 1002, "DOUBLE THE SIZE", 32, WHITE, 0, 800, 0.06, "start")
for i_ in (sz, t2): s.fade(i_, ix(99) - 0.1, 0.3)
tl(f'tl.to("#{sz}", {{scaleX: 2.2, transformOrigin: "0% 50%", duration: 0.45, ease: "back.out(1.6)"}}, {ix(99) + 0.25:.3f});')
xmark(s, 872, 992, ix(101)); cue(ix(101), "tick_2", -18)
# row 3: try to win it back
rv5 = s.path("M 318 1112 A 40 40 0 1 1 268 1112 M 318 1112 L 322 1088 M 318 1112 L 296 1106", GOLD, 5); s.draw(rv5, ix(103) - 0.1, 0.5)
t3 = s.label(400, 1152, "TRY TO WIN IT BACK", 32, WHITE, 0, 800, 0.06, "start"); s.fade(t3, ix(103) - 0.1, 0.3)
xmark(s, 872, 1142, ix(106)); cue(ix(106), "tick_3", -18)

# 6  "Don't judge your trading by one dot. Judge it by the whole shirt. Your win rate. Your average win against your average loss.
#     Your discipline over a hundred trades. One loss is a data point, not a verdict."
s = S(ix(108) - 0.1, ix(146) + 0.35, ground=False, hide=False)
sh6, dt6, (dx6, dy6) = shirt(s, 540, 860, 0.8)
s.pop(sh6, ix(108) - 0.05, 0.5, 0.7, "50% 50%")
rg = s.path(f"M {dx6 + 44:.0f} {dy6:.0f} A 44 44 0 1 1 {dx6 + 43.9:.0f} {dy6 - 2:.0f}", RED, 5); s.draw(rg, ix(113) - 0.05, 0.45)
cue(ix(113) - 0.05, "tick-crisp_2", -18)
toplab(s, "DON'T JUDGE YOUR TRADING", "BY ONE DOT", ix(108), ix(115) - 0.1, RED, LBL, 58)
hide(rg, ix(115) - 0.1)
ol6 = outline(s, 540, 860, 0.8); s.draw(ol6, ix(115), 0.8); cue(ix(115), "swell_2", -18)
toplab(s, "JUDGE IT BY", "THE WHOLE SHIRT", ix(115), ix(137) - 0.1, GOLD, LBL, 58)
for i_ in (sh6, ol6):
    hide(i_, ix(121) - 0.15)
# stats
a1 = s.label(150, 735, "WIN RATE", 30, LBL, 0, 800, 0.12, "start"); s.fade(a1, ix(121) + 0.15, 0.3)
a2 = s.label(930, 737, "14 / 20 · 70%", 40, GOLD, 0, 800, 0.04, "end"); s.fade(a2, ix(122) + 0.1, 0.3); cue(ix(122) + 0.1, "pop_1", -22)
b1_ = s.label(150, 847, "AVG WIN", 28, LBL, 0, 800, 0.12, "start"); s.fade(b1_, ix(125) - 0.1, 0.3)
bw = s.raw(f'<rect id="@ID@" x="400" y="818" width="0" height="34" rx="8" fill="{GOLD}"/>', "bw")
tl(f'tl.fromTo("#{bw}", {{attr: {{width: 0}}}}, {{attr: {{width: 430}}, duration: 0.6, ease: "power2.out", immediateRender: false}}, {ix(125) - 0.05:.3f});')
b2_ = s.label(150, 927, "AVG LOSS", 28, LBL, 0, 800, 0.12, "start"); s.fade(b2_, ix(129) - 0.1, 0.3)
bl6 = s.raw(f'<rect id="@ID@" x="400" y="898" width="0" height="34" rx="8" fill="{RED}"/>', "bl")
tl(f'tl.fromTo("#{bl6}", {{attr: {{width: 0}}}}, {{attr: {{width: 200}}, duration: 0.5, ease: "power2.out", immediateRender: false}}, {ix(129) - 0.05:.3f});')
cue(ix(125) - 0.05, "whoosh-short_3", -24); cue(ix(129) - 0.05, "tick_1", -22)
for i_ in (a1, a2, b1_, bw, b2_, bl6):
    hide(i_, ix(137) - 0.35)
# 100 trades: the whole record (gold wins, dim red losses); one red dot is the loss in question
rr = random.Random(5)
HI = (4, 9)
grid_id = s.uid("gd")
rows, body = [], ""
for r in range(10):
    rid = s.uid("gr"); rows.append(rid); cs = ""
    for c in range(10):
        lo = (r, c) == HI or rr.random() < 0.33
        cs += (f'<circle cx="{405 + c * 30}" cy="{1060 + r * 28}" r="9" fill="{RED if lo else GOLD}" fill-opacity="{1 if (r, c) == HI else (0.55 if lo else 0.9)}"/>')
    body += f'<g id="{rid}" style="opacity:0">{cs}</g>'
hx, hy = 405 + HI[1] * 30, 1060 + HI[0] * 28
ring = s.uid("rg"); dl = s.uid("dl")
body += (f'<circle id="{ring}" cx="{hx}" cy="{hy}" r="20" fill="none" stroke="#fff" stroke-width="3.5" style="opacity:0"/>'
         f'<text id="{dl}" x="{hx + 40}" y="{hy + 9}" font-family="Montserrat" font-weight="800" font-size="28" letter-spacing="0.06em" fill="#fff" style="opacity:0">= 1 DATA POINT</text>')
dlab = s.uid("t")
s.raw(f'<g id="{grid_id}"><text id="{dlab}" x="150" y="1015" font-family="Montserrat" font-weight="800" font-size="28" letter-spacing="0.12em" fill="{LBL}" style="opacity:0">DISCIPLINE · 100 TRADES</text>{body}</g>', "x")
s.fade(dlab, ix(131) - 0.1, 0.3)
for r, rid in enumerate(rows):
    s.fade(rid, ix(132) + r * 0.12, 0.25)
cue(ix(132), "swell_1", -22)
tl(f'tl.to("#{grid_id}", {{y: -250, duration: 0.7, ease: "power2.inOut"}}, {ix(137) - 0.35:.3f});')
s.pop(ring, ix(138), 0.35, 0.3, "50% 50%"); cue(ix(138), "tick-crisp_3", -16)
s.fade(dl, ix(141) - 0.1, 0.35)
toplab(s, "", "ONE LOSS = ONE DATA POINT", ix(137), ix(143) - 0.1, WHITE, LBL, 46)
toplab(s, "NOT A", "VERDICT", ix(143), ix(146) + 0.35, RED, LBL, 64)

# 7  outro (handles, no end card)
s = S(ix(146) + 0.3, TOTAL)
es = s.spot(540, 0, "232,194,106", 40, 230); s.fade(es, ix(146) + 0.35, 0.6)
em = s.raw('<image id="@ID@" href="assets/otm_emblem.png" x="390" y="900" width="300" height="291" style="opacity:0;filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>', "i")
s.pop(em, ix(146) + 0.35, 0.7, 0.6, "50% 50%"); cue(ix(146) + 0.35, "bell_A4", -16)
o1l = s.label(540, 1300, "ORDER THE MARKET", 32, GOLD, 0, 800, 0.3); s.fade(o1l, ix(146) + 0.55, 0.5)
o2 = s.label(540, 1360, "DON'T LET THE MARKET ORDER YOU", 28, WHITE, 0, 700, 0.12); s.fade(o2, ix(149), 0.4)
o3 = s.pill(540, 1470, "FOLLOW FOR MORE", GOLD, "#111", 30); s.pop(o3, ix(155), 0.4, 0.6, "50% 50%"); cue(ix(155), "click-confirm_1", -16)
hx = 290
soc = s.raw(f'<g id="@ID@" style="opacity:0">'
            f'<rect x="{hx}" y="1548" width="36" height="36" rx="10" fill="none" stroke="#fff" stroke-width="3"/>'
            f'<circle cx="{hx + 18}" cy="1566" r="8.5" fill="none" stroke="#fff" stroke-width="3"/><circle cx="{hx + 28}" cy="1556" r="2.4" fill="#fff"/>'
            f'<text x="{hx + 48}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@fxzuez_28</text>'
            f'<path d="M {hx + 322} 1546 V 1574 A 9 9 0 1 1 {hx + 313} 1565 M {hx + 322} 1546 Q {hx + 326} 1557 {hx + 338} 1558" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>'
            f'<text x="{hx + 348}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@zuez_28</text></g>', "so")
disc = s.label(540, 1650, "EDUCATIONAL ONLY · NOT FINANCIAL ADVICE", 28, GREY, 0, 600, 0.12)
s.fade(soc, ix(149) + 0.6, 0.5, y=12)
s.fade(disc, ix(149) + 0.9, 0.5)
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
    <div id="root" data-composition-id="otm-blackdot" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
{TIMELINE}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-blackdot-audio" class="clip" src="assets/audio/mix_blackdot.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-blackdot"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
