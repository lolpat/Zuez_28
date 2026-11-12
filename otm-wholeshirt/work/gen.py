"""OTM "The Whole Shirt": a glowing-figure motivation video in the OTM style, the companion to otm-blackdot. One bad
day, one mistake, one person who let you down, and that's all you can think about: the black dot on a white shirt that
everyone points at while nobody mentions the white. A hundred good days and you replay the one that went wrong; a room
full of compliments and you remember the one that stung. That's where your attention landed, not the whole truth. Step
back and look at the white: the people who stayed, the progress you made, the times you got back up. The dot is real,
but it's small. Don't let one dot define the whole shirt.
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

def hide(i, t, d=0.3, to=0):
    tl(f'tl.to("#{i}", {{opacity: {to}, duration: {d}}}, {t:.3f});')

SHIRT = ("M -90 -240 Q 0 -165 90 -240 L 250 -195 L 330 -60 L 240 -15 L 200 -80 L 200 240 Q 0 252 -200 240 "
         "L -200 -80 L -240 -15 L -330 -60 L -250 -195 Z")
DX, DY = 120, -120                                         # the dot sits high on the right of the chest

def shirt(s, x, y, sc=1.0, r=16, inner="", wrap=False):
    """A glowing white T-shirt with one black dot. Returns (wrapper id or None, group id, dot id, dot centre on screen)."""
    g, d, w = s.uid("sh"), s.uid("dt"), s.uid("wr")
    wo, wc = (f'<g id="{w}">', '</g>') if wrap else ("", "")
    s.raw(f'<g transform="translate({x},{y}) scale({sc})">{wo}<g id="{g}" style="opacity:0;filter:drop-shadow(0 0 22px rgba(255,255,255,0.45))">'
          f'<path d="{SHIRT}" fill="#f4f4f2" stroke="#ffffff" stroke-width="3" stroke-linejoin="round"/>'
          f'<circle id="{d}" cx="{DX}" cy="{DY}" r="{r}" fill="#0b0b0b"/>{inner}</g>{wc}</g>', "x")
    return (w if wrap else None), g, d, (x + DX * sc, y + DY * sc)

def outline(s, x, y, sc=1.0, col=GOLD):
    return s.raw(f'<g transform="translate({x},{y}) scale({sc})"><path id="@ID@" d="{SHIRT}" fill="none" stroke="{col}" stroke-width="7" '
                 f'stroke-linejoin="round" pathLength="1" style="stroke-dasharray:1 1.2;stroke-dashoffset:1.1;filter:drop-shadow(0 0 12px rgba(232,194,106,0.9))"/></g>', "ol")

def ring(s, x, y, r, col, t, w=5):
    g = s.path(f"M {x + r:.0f} {y:.0f} A {r} {r} 0 1 1 {x + r - 0.1:.1f} {y - 2:.0f}", col, w); s.draw(g, t, 0.45)
    return g

# 1  "One bad day. One mistake. One person who let you down. And somehow, that's all you can think about."
s = S(0, ix(19) - 0.1, first=True)
f1 = s.fig(540, 1.0, WHITE, 1)
L1 = []
for k, (txt, t) in enumerate([("ONE BAD DAY", None), ("ONE MISTAKE", ix(3)), ("ONE PERSON WHO LET YOU DOWN", ix(5))]):
    l = s.label(540, 470 + k * 66, txt, 40 if k < 2 else 36, WHITE, 1 if t is None else 0, 800, 0.06)
    if t is not None: s.fade(l, t - 0.05, 0.3, y=10); cue(t - 0.05, "tock_1", -22)
    L1.append(l)
for l in L1:
    hide(l, ix(11), 0.4, 0.3)
c1 = s.raw('<circle id="@ID@" cx="568" cy="1004" r="9" fill="#f4f4f2" style="opacity:0"/>', "b")
c2 = s.raw('<circle id="@ID@" cx="596" cy="958" r="14" fill="#f4f4f2" style="opacity:0"/>', "b")
cl = s.raw('<circle id="@ID@" cx="560" cy="800" r="125" fill="#f4f4f2" style="opacity:0;filter:drop-shadow(0 0 18px rgba(255,255,255,0.5))"/>', "c")
s.pop(c1, ix(11), 0.25, 0.3, "50% 50%"); s.pop(c2, ix(11) + 0.1, 0.25, 0.3, "50% 50%"); s.pop(cl, ix(11) + 0.2, 0.45, 0.5, "50% 50%")
cue(ix(11), "pop_2", -20)
bd = s.raw('<circle id="@ID@" cx="560" cy="800" r="104" fill="#0b0b0b" style="opacity:0"/>', "bd")
tl(f'tl.fromTo("#{bd}", {{opacity: 0, scale: 0.12, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 0.15, duration: 0.2, immediateRender: false}}, {ix(13) - 0.1:.3f});')
tl(f'tl.to("#{bd}", {{scale: 1, duration: {ix(18) + 0.3 - ix(13):.3f}, ease: "power1.in"}}, {ix(13) + 0.1:.3f});')
cue(ix(13), "swell_1", -20)
tl(f'tl.to("#{f1}", {{opacity: 0.55, duration: 0.6}}, {ix(14):.3f});')
th = s.label(540, 1330, "THAT'S ALL YOU CAN THINK ABOUT", 34, WHITE, 0, 800, 0.08); s.fade(th, ix(13) - 0.05, 0.35, y=10)

# 2  "Picture a white shirt with one small black dot. Ask anyone what they see, and they point at the dot. Nobody mentions the white."
s = S(ix(19) - 0.1, ix(43) - 0.1)
_, sh, dt, (dx_, dy_) = shirt(s, 540, 860, 0.85)
s.pop(sh, ix(21) - 0.1, 0.5, 0.6, "50% 50%"); cue(ix(21) - 0.1, "swell_2", -22)
s.pop(dt, ix(26), 0.35, 0.1, "50% 50%"); cue(ix(26), "tick-crisp_1", -16)
toplab(s, "PICTURE", "A WHITE SHIRT", ix(19), ix(25) - 0.1, WHITE, LBL, 58)
toplab(s, "WITH ONE SMALL", "BLACK DOT", ix(25) - 0.1, ix(28) - 0.25, WHITE, LBL, 58)
toplab(s, "", "WHAT DO YOU SEE?", ix(28) - 0.25, ix(33) - 0.4, WHITE, LBL, 56)
toplab(s, "", "EVERYONE POINTS AT THE DOT", ix(33) - 0.4, ix(39) + 0.1, WHITE, LBL, 44)
toplab(s, "NOBODY MENTIONS", "THE WHITE", ix(39) + 0.1, ix(43) - 0.1, GOLD, LBL, 60)
aims = []
for j, x in enumerate([120, 310, 770, 960]):
    sc = 0.55
    f = s.fig(x, sc, WHITE); s.pop(f, ix(28) + j * 0.08, 0.35);
    side = 1 if dx_ > x else -1
    sx, sy = x + side * 22, GY - 92 * sc
    L = math.hypot(dx_ - sx, dy_ - sy); ux, uy = (dx_ - sx) / L, (dy_ - sy) / L
    ex, ey = sx + ux * 58, sy + uy * 58
    arm = s.path(f"M {sx:.0f} {sy:.0f} L {ex:.0f} {ey:.0f}", WHITE, 9, style="filter:drop-shadow(0 0 8px rgba(255,255,255,0.6))")
    s.draw(arm, ix(35) - 0.1 + j * 0.06, 0.25, "power2.out")
    aim = s.path(f"M {ex + ux * 14:.0f} {ey + uy * 14:.0f} L {dx_ - ux * 30:.0f} {dy_ - uy * 30:.0f}", "#8a9099", 3, drawn=True,
                 extra='stroke-dasharray="9 9"', style="opacity:0")
    s.fade(aim, ix(35) + 0.1 + j * 0.06, 0.4, to=0.8); aims.append(aim)
cue(ix(28), "pop_3", -22); cue(ix(35) - 0.1, "whoosh-short_1", -24)
for a in aims:
    hide(a, ix(39), 0.4, 0.12)
ol = outline(s, 540, 860, 0.85); s.draw(ol, ix(39) + 0.1, 1.2); cue(ix(39) + 0.1, "swell_1", -20)

# 3  "Your mind does the same thing with your life. A hundred good days, and you replay the one that went wrong.
#     A room full of compliments, and you remember the one comment that stung."
s = S(ix(43) - 0.1, ix(77) - 0.1, ground=False, restore=False)
toplab(s, "YOUR MIND DOES", "THE SAME THING", ix(43), ix(52) - 0.1, WHITE, LBL, 58)
BAD = (6, 3)
rows = []
for r in range(10):
    cs = "".join(f'<rect x="{265 + c * 56}" y="{680 + r * 56}" width="46" height="46" rx="9" fill="{GOLD}" fill-opacity="{0.78 + 0.18 * ((r * 3 + c) % 3) / 2:.2f}"/>'
                 for c in range(10) if (r, c) != BAD)
    rid = s.raw(f'<g id="@ID@" style="opacity:0">{cs}</g>', "row"); rows.append(rid)
    s.fade(rid, ix(51) - 0.1 + r * 0.07, 0.25)
bx, by = 265 + BAD[1] * 56, 680 + BAD[0] * 56
bc = s.raw(f'<rect id="@ID@" x="{bx}" y="{by}" width="46" height="46" rx="9" fill="#0b0b0b" stroke="{RED}" stroke-width="3" style="opacity:0"/>', "bc")
s.fade(bc, ix(51) - 0.1 + BAD[0] * 0.07, 0.25)
cue(ix(51) - 0.1, "swell_2", -22)
toplab(s, "A HUNDRED", "GOOD DAYS", ix(52), ix(57) - 0.1, GOLD, LBL, 60)
toplab(s, "YOU REPLAY", "THE ONE THAT WENT WRONG", ix(57), ix(64) - 0.1, RED, LBL, 46)
for rid in rows:
    hide(rid, ix(58), 0.5, 0.22)
cx_, cy_ = bx + 23, by + 23
rp = s.path(f"M {cx_ + 42} {cy_} A 42 42 0 1 1 {cx_ + 30} {cy_ - 30} M {cx_ + 30} {cy_ - 30} L {cx_ + 33} {cy_ - 52} M {cx_ + 30} {cy_ - 30} L {cx_ + 52} {cy_ - 27}",
            RED, 5, style="filter:drop-shadow(0 0 8px rgba(255,77,94,0.9))")
s.draw(rp, ix(58) - 0.1, 0.4)
tl(f'tl.fromTo("#{rp}", {{rotation: 0}}, {{rotation: 720, svgOrigin: "{cx_} {cy_}", duration: {ix(64) - 0.5 - ix(58):.3f}, ease: "none", immediateRender: false}}, {ix(58) + 0.3:.3f});')
cue(ix(58) - 0.1, "whoosh-short_2", -22)
for i_ in rows + [bc, rp]:
    hide(i_, ix(64) - 0.35)
# compliments
B = [("GREAT JOB!", 270, 712), ("PROUD OF YOU", 760, 700), ("YOU'RE AMAZING", 520, 830), ("THANK YOU!", 250, 950), ("WELL DONE", 820, 920),
     ("LOVE THIS", 290, 1178), ("YOU GOT THIS", 790, 1172), ("SO HELPFUL", 540, 1290)]
bub = []
for k, (txt, x, y) in enumerate(B):
    w = len(txt) * 28 * 0.72 + 50
    b = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(x - w / 2, y - 32, w, 64, 32)}" fill="#f4f4f2"/>'
              f'<path d="M {x - w / 2 + 34} {y + 26} L {x - w / 2 + 22} {y + 50} L {x - w / 2 + 58} {y + 28} Z" fill="#f4f4f2"/>'
              f'<text x="{x}" y="{y + 10}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" fill="#15171b">{txt}</text></g>', "bu")
    s.pop(b, ix(64) + 0.1 + k * 0.1, 0.3, 0.5, "50% 50%"); bub.append(b)
cue(ix(64) + 0.1, "pop_1", -22); cue(ix(64) + 0.4, "pop_2", -24); cue(ix(64) + 0.7, "pop_3", -24)
txt, x, y = "NOT GOOD ENOUGH", 540, 1060
w = len(txt) * 28 * 0.72 + 50
rb = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(x - w / 2, y - 32, w, 64, 32)}" fill="#1a0f12" stroke="{RED}" stroke-width="3"/>'
           f'<text x="{x}" y="{y + 10}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" fill="{RED}">{txt}</text></g>', "rb")
s.pop(rb, ix(66), 0.3, 0.5, "50% 50%")
for b in bub:
    hide(b, ix(71), 0.5, 0.18)
tl(f'tl.to("#{rb}", {{scale: 1.3, transformOrigin: "50% 50%", duration: 0.5, ease: "back.out(1.6)"}}, {ix(73) - 0.1:.3f});')
cue(ix(73) - 0.1, "tock_1", -16)
toplab(s, "A ROOM FULL OF", "COMPLIMENTS", ix(64), ix(70) - 0.1, GOLD, LBL, 58)
toplab(s, "YOU REMEMBER", "THE ONE THAT STUNG", ix(70), ix(77) - 0.1, RED, LBL, 50)

# 4  "That's not the whole truth. It's just where your attention landed."
s = S(ix(77) - 0.1, ix(88) - 0.1, ground=False, hide=False, restore=False)
_, sh4, dt4, (dx4, dy4) = shirt(s, 540, 900, 0.9)
s.pop(sh4, ix(77) - 0.05, 0.5, 0.7, "50% 50%")
toplab(s, "THAT'S NOT", "THE WHOLE TRUTH", ix(77), ix(82) - 0.1, WHITE, LBL, 58)
toplab(s, "IT'S JUST WHERE", "YOUR ATTENTION LANDED", ix(82), ix(88) - 0.1, GOLD, LBL, 46)
hide(sh4, ix(82) + 0.1, 0.6, 0.2)
sp4 = s.spot(dx4, 0, "255,255,255", 22, 60, gy=dy4, y0=380); s.fade(sp4, ix(84) - 0.1, 0.5)
d4 = s.raw(f'<g id="@ID@" style="opacity:0"><circle cx="{dx4}" cy="{dy4}" r="34" fill="#f4f4f2" style="filter:drop-shadow(0 0 16px rgba(255,255,255,0.8))"/>'
           f'<circle cx="{dx4}" cy="{dy4}" r="{16 * 0.9:.1f}" fill="#0b0b0b"/></g>', "d4")
s.pop(d4, ix(84), 0.35, 0.4, "50% 50%"); cue(ix(84), "bell_E5", -20)

# 5  "So when one dot starts to take over... step back. Look at the white. The people who stayed. The progress you made.
#     The times you got back up. The dot is real, but it's small. Don't let one dot define the whole shirt."
s = S(ix(88) - 0.1, ix(131) + 0.35, ground=False, hide=False)
lines5 = [s.uid("t") for _ in range(3)]
inner = "".join(f'<text id="{lid}" x="0" y="{50 + k * 70}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" '
                f'letter-spacing="0.02em" fill="#1d1f23" style="opacity:0">{txt}</text>'
                for k, (lid, txt) in enumerate(zip(lines5, ["PEOPLE WHO STAYED", "PROGRESS YOU MADE", "GOT BACK UP"])))
wr5, sh5, dt5, (dx5, dy5) = shirt(s, 540, 900, 1.0, inner=inner, wrap=True)
tl(f'tl.set("#{wr5}", {{scale: 1.1, transformOrigin: "50% 50%"}}, {ix(88) - 0.1:.3f});')
s.pop(sh5, ix(88) - 0.05, 0.5, 0.7, "50% 50%")
toplab(s, "WHEN ONE DOT", "STARTS TO TAKE OVER", ix(88), ix(96) - 0.1, RED, LBL, 50)
tl(f'tl.to("#{dt5}", {{scale: 6.5, transformOrigin: "50% 50%", duration: {ix(95) - ix(91):.3f}, ease: "power2.inOut"}}, {ix(91) - 0.1:.3f});')
cue(ix(91), "swell_2", -18)
tl(f'tl.to("#{dt5}", {{scale: 1, duration: 0.6, ease: "power2.inOut"}}, {ix(96) - 0.05:.3f});')
tl(f'tl.to("#{wr5}", {{scale: 1, duration: 0.6, ease: "power2.inOut"}}, {ix(96) - 0.05:.3f});')
cue(ix(96) - 0.05, "whoosh-long_1", -22)
toplab(s, "", "STEP BACK", ix(96), ix(98) - 0.1, WHITE, LBL, 60)
toplab(s, "", "LOOK AT THE WHITE", ix(98), ix(116) - 0.1, GOLD, LBL, 58)
ol5 = outline(s, 540, 900, 1.0); s.draw(ol5, ix(98) + 0.1, 1.1); cue(ix(98) + 0.1, "swell_1", -20)
for lid, w_ in zip(lines5, (102, 106, 110)):
    s.fade(lid, ix(w_) - 0.05, 0.4, y=10); cue(ix(w_) - 0.05, "bell_" + {102: "C5", 106: "E5", 110: "G5"}[w_], -22)
rg5 = ring(s, dx5, dy5, 40, RED, ix(117) - 0.1); cue(ix(117) - 0.1, "tick-crisp_2", -18)
tl(f'tl.to("#{rg5}", {{scale: 0.62, svgOrigin: "{dx5} {dy5}", duration: 0.5, ease: "power2.inOut"}}, {ix(121):.3f});')
hide(rg5, ix(123) - 0.2)
toplab(s, "THE DOT IS", "REAL", ix(116), ix(120) - 0.1, WHITE, LBL, 64)
toplab(s, "BUT IT'S", "SMALL", ix(120), ix(123) - 0.1, GOLD, LBL, 64)
toplab(s, "DON'T LET ONE DOT DEFINE", "THE WHOLE SHIRT", ix(123), ix(131) + 0.35, GOLD, LBL, 58)
cue(ix(129), "bell_G5", -20)

# 6  outro (handles, no end card)
s = S(ix(131) + 0.3, TOTAL)
es = s.spot(540, 0, "232,194,106", 40, 230); s.fade(es, ix(131) + 0.35, 0.6)
em = s.raw('<image id="@ID@" href="assets/otm_emblem.png" x="390" y="900" width="300" height="291" style="opacity:0;filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>', "i")
s.pop(em, ix(131) + 0.35, 0.7, 0.6, "50% 50%"); cue(ix(131) + 0.35, "bell_A4", -16)
o1l = s.label(540, 1300, "ORDER THE MARKET", 32, GOLD, 0, 800, 0.3); s.fade(o1l, ix(131) + 0.55, 0.5)
o2 = s.label(540, 1360, "DON'T LET THE MARKET ORDER YOU", 28, WHITE, 0, 700, 0.12); s.fade(o2, ix(134), 0.4)
o3 = s.pill(540, 1470, "FOLLOW FOR MORE", GOLD, "#111", 30); s.pop(o3, ix(140), 0.4, 0.6, "50% 50%"); cue(ix(140), "click-confirm_1", -16)
hx = 290
soc = s.raw(f'<g id="@ID@" style="opacity:0">'
            f'<rect x="{hx}" y="1548" width="36" height="36" rx="10" fill="none" stroke="#fff" stroke-width="3"/>'
            f'<circle cx="{hx + 18}" cy="1566" r="8.5" fill="none" stroke="#fff" stroke-width="3"/><circle cx="{hx + 28}" cy="1556" r="2.4" fill="#fff"/>'
            f'<text x="{hx + 48}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@fxzuez_28</text>'
            f'<path d="M {hx + 322} 1546 V 1574 A 9 9 0 1 1 {hx + 313} 1565 M {hx + 322} 1546 Q {hx + 326} 1557 {hx + 338} 1558" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>'
            f'<text x="{hx + 348}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@zuez_28</text></g>', "so")
disc = s.label(540, 1650, "EDUCATIONAL ONLY · NOT FINANCIAL ADVICE", 28, GREY, 0, 600, 0.12)
s.fade(soc, ix(134) + 0.6, 0.5, y=12)
s.fade(disc, ix(134) + 0.9, 0.5)
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
    <div id="root" data-composition-id="otm-wholeshirt" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
{TIMELINE}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-wholeshirt-audio" class="clip" src="assets/audio/mix_wholeshirt.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-wholeshirt"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
