"""OTM "The $100 Million Lesson" (Jesse Livermore): a glowing-figure story in the OTM style (same scene system as
otm-chance / otm-break). Livermore is the figure in the fedora; a timeline across the top lights each year as the story
reaches it (1891 to 1934). Scenes: the hook ($100,000,000 -> buried in debt), the name, the Boston chalkboard and its
patterns, the $5 first trade, job vs trading, 1907 (+$1,000,000 in one day), the 1908 cotton tip, BANKRUPT 1915, the
comeback and 1929, the rulebook he stopped following, BANKRUPT AGAIN 1934, his four rules, "he failed his rules",
"every day", and the outro with the handles. Original script, voice only (Quentin), no music.
Writes ../index.html, work/cues.json (soft kit sounds) and work/timing.json."""
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

def xmark(s, x, y, r=60, col=RED, w=7):
    return s.path(f"M {x - r} {y - r} L {x + r} {y + r} M {x + r} {y - r} L {x - r} {y + r}", col, w)

def hatfig(s, x, sc=1.0, col=WHITE, op=1.0, gy=GY, glow=True):
    """the glowing figure with a fedora: Jesse Livermore"""
    g = "filter:drop-shadow(0 0 16px rgba(255,255,255,0.55));" if glow else ""
    return s.add(f'<g transform="translate({x},{gy}) scale({sc})"><g id="@ID@" style="opacity:{op};{g}">'
                 f'<circle cx="0" cy="-158" r="31" fill="{col}"/><path d="M -48 0 L -48 -66 Q -48 -116 0 -116 Q 48 -116 48 -66 L 48 0 Z" fill="{col}"/>'
                 f'<path d="M -52 -179 Q 0 -192 52 -179 L 52 -172 Q 0 -183 -52 -172 Z" fill="{col}"/>'
                 f'<path d="M -29 -180 L -25 -214 Q 0 -223 25 -214 L 29 -180 Z" fill="{col}"/>'
                 f'<rect x="-28" y="-191" width="56" height="6" fill="#000" opacity="0.55"/></g></g>', "f")

def stamp(s, x, y, text, col=RED, size=64, t=0):
    w = len(text) * size * 0.74 + 60; h = size + 40
    i = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="{x - w / 2:.0f}" y="{y - h / 2:.0f}" width="{w:.0f}" height="{h:.0f}" rx="10" fill="none" stroke="{col}" stroke-width="7"/>'
              f'<text x="{x}" y="{y + size * 0.36:.0f}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="{size}" letter-spacing="0.06em" fill="{col}">{text}</text></g>', "st")
    tl(f'tl.fromTo("#{i}", {{opacity: 0, scale: 1.8, rotation: -14, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, rotation: -8, duration: 0.35, ease: "power4.in", immediateRender: false}}, {t:.3f});')
    cue(t + 0.33, "land_1", -16)
    return i

def money(s, x, y, text, size=96, col=GOLD, op=0):
    return s.label(x, y, text, size, col, op, 800, 0.02)

def crash_line(s, x0, y0, w, h, col=RED):
    pts = [(0, 0.05), (0.12, 0.12), (0.2, 0.08), (0.33, 0.3), (0.42, 0.25), (0.55, 0.55), (0.64, 0.5), (0.78, 0.82), (0.88, 0.78), (1.0, 0.98)]
    return s.path("M " + " L ".join(f"{x0 + px * w:.0f} {y0 + py * h:.0f}" for px, py in pts), col, 6)

# ---------------------------------------------------------------- the timeline across the top (scenes 3 to 11)
YEARS = [(1891, "at", 1), (1892, "at", 2), (1893, "by", 1), (1907, "1907", 1), (1908, None, None), (1915, "1915", 1), (1929, "1929", 1), (1934, "1934", 1)]
T_YEAR = [A(w_, k) - 0.1 if w_ else W(F("year")) - 0.25 for _, w_, k in YEARS]
TL_ON, TL_OFF = A("at", 1) - 0.1, W(F("simple") - 4) - 0.1           # "and his rules were simple" closes the story part
tlx = [120 + i * 120 for i in range(len(YEARS))]
tlsvg = f'<line x1="100" y1="430" x2="980" y2="430" stroke="#ffffff40" stroke-width="2"/>'
for i, (yr, _, _) in enumerate(YEARS):
    tlsvg += (f'<circle cx="{tlx[i]}" cy="430" r="7" fill="#5a606b"/><circle id="tld{i}" cx="{tlx[i]}" cy="430" r="8" fill="{GOLD}" style="opacity:0"/>'
              f'<text x="{tlx[i]}" y="484" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="28" fill="#5a606b">{yr}</text>'
              f'<text id="tll{i}" x="{tlx[i]}" y="484" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" fill="{GOLD}" style="opacity:0">{yr}</text>')
tlsvg += f'<circle id="tlring" cx="{tlx[0]}" cy="430" r="17" fill="none" stroke="{GOLD}" stroke-width="3" style="filter:drop-shadow(0 0 8px {GOLD})"/>'
TIMELINE = f'<g id="tline" style="opacity:0;visibility:hidden">{tlsvg}</g>'
tl(f'tl.set("#tline", {{visibility: "visible"}}, {TL_ON:.3f});')
tl(f'tl.fromTo("#tline", {{opacity: 0}}, {{opacity: 1, duration: 0.4, immediateRender: false}}, {TL_ON:.3f});')
tl(f'tl.to("#tline", {{opacity: 0, duration: 0.3}}, {TL_OFF - 0.3:.3f});')
tl(f'tl.set("#tline", {{visibility: "hidden"}}, {TL_OFF:.3f});')
for i, t in enumerate(T_YEAR):
    tl(f'tl.fromTo("#tld{i}", {{opacity: 0}}, {{opacity: 1, duration: 0.3, immediateRender: false}}, {t:.3f});')
    tl(f'tl.fromTo("#tll{i}", {{opacity: 0}}, {{opacity: 1, duration: 0.3, immediateRender: false}}, {t:.3f});')
    if i:
        tl(f'tl.to("#tll{i - 1}", {{opacity: 0.45, duration: 0.3}}, {t:.3f});')
        tl(f'tl.fromTo("#tlring", {{x: {tlx[i - 1] - tlx[0]}}}, {{x: {tlx[i] - tlx[0]}, duration: 0.45, ease: "power2.inOut", immediateRender: false}}, {t:.3f});')
    cue(t, "tick_" + str(i % 3 + 1), -24)

def header(s, text, col=LBL):
    return s.label(540, 590, text, 30, col, 1, 700, 0.2)

# 1  "He made a hundred million dollars in the market... and ended up buried in debt."
s = S(0, A("his") - 0.1, first=True)
sp1 = s.spot(540, 1, "232,194,106")
lv1 = hatfig(s, 540, 1.05, GOLD)
s.label(540, 600, "HE MADE", 34, LBL, 1, 700, 0.3)
m1 = money(s, 540, 720, "$100,000,000", 104, GOLD, 1)
tl(f'tl.fromTo("#{m1}", {{scale: 0.96, transformOrigin: "50% 50%"}}, {{scale: 1.03, duration: {A("ended") - 0.2:.3f}, ease: "none"}}, 0);')
m1r = money(s, 540, 720, "$100,000,000", 104, RED, 0)
cr = s.path("M 170 690 L 910 700", RED, 8); s.draw(cr, A("buried") - 0.1, 0.35)
tl(f'tl.to("#{m1}", {{opacity: 0, duration: 0.3}}, {A("buried") - 0.1:.3f});'); s.fade(m1r, A("buried") - 0.1, 0.3)
tl(f'tl.to("#{sp1}", {{opacity: 0.25, duration: 0.6}}, {A("buried") - 0.1:.3f});')
tl(f'tl.to("#{lv1}", {{opacity: 0.55, duration: 0.6}}, {A("buried") - 0.1:.3f});')
db = s.label(540, 860, "BURIED IN DEBT", 44, RED, 0, 800, 0.12); s.fade(db, A("debt") - 0.1, 0.4, y=12); cue(A("debt") - 0.1, "tock_1", -16)

# 2  "His name was Jesse Livermore."
s = S(A("his") - 0.1, A("at", 1) - 0.1)
s.spot(540, 1, "232,194,106")
lv2 = hatfig(s, 540, 1.05, WHITE); s.pop(lv2, A("his"), 0.45)
n1 = s.label(540, 760, "JESSE", 92, WHITE, 0, 800, 0.08); s.fade(n1, A("jesse") - 0.1, 0.4, y=14)
n2 = s.label(540, 860, "LIVERMORE", 92, GOLD, 0, 800, 0.08); s.fade(n2, A("livermore") - 0.1, 0.4, y=14)
n3 = s.label(540, 930, "1877 – 1940", 30, LBL, 0, 700, 0.3); s.fade(n3, A("livermore") + 0.3, 0.4)
cue(A("jesse") - 0.1, "swell_1", -18)

# 3  "At 14, he left the farm for Boston, writing stock prices on a chalkboard. Day after day, he noticed the prices moved in patterns."
s = S(A("at", 1) - 0.1, A("at", 2) - 0.1)
header(s, "AGE 14  ·  BOSTON")
barn = s.raw(f'<g id="@ID@" style="opacity:0.55"><path d="M 60 1240 V 1150 L 120 1100 L 180 1150 V 1240 Z M 100 1240 V 1190 H 140 V 1240" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/></g>', "bn")
s.label(120, 1290, "FARM", 28, GREY, 1, 700, 0.15)
bx0, by0, bw, bh = 430, 700, 560, 380
s.raw(f'<g id="@ID@"><rect x="{bx0}" y="{by0}" width="{bw}" height="{bh}" rx="8" fill="#10201a" stroke="#c9a46a" stroke-width="10"/>'
      f'<line x1="{bx0 + 40}" y1="{by0 + bh + 6}" x2="{bx0 + 40}" y2="1240" stroke="#c9a46a" stroke-width="6"/><line x1="{bx0 + bw - 40}" y1="{by0 + bh + 6}" x2="{bx0 + bw - 40}" y2="1240" stroke="#c9a46a" stroke-width="6"/></g>', "cb")
r3 = random.Random(3)
cells, pat = [], []
cols, rows = 5, 5
vals = [[round(100 + r3.uniform(-9, 9), 1) for _ in range(cols)] for _ in range(rows)]
zig = [4, 2, 3, 1, 0]                                  # the row lit in each column: a rising zigzag
for c in range(cols):
    for r in range(rows):
        x, y = bx0 + 62 + c * 108, by0 + 62 + r * 68
        lit = zig[c] == r
        i = s.raw(f'<text id="@ID@" x="{x}" y="{y}" text-anchor="middle" font-family="Montserrat" font-weight="600" font-size="28" fill="#e8efe9" style="opacity:0">{vals[r][c]}</text>', "ch")
        tl(f'tl.fromTo("#{i}", {{opacity: 0}}, {{opacity: 0.85, duration: 0.12, immediateRender: false}}, {A("writing") + (c * rows + r) * 0.05:.3f});')
        if lit:
            g = s.raw(f'<text id="@ID@" x="{x}" y="{y}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 8px {GOLD})">{vals[r][c]}</text>', "cg")
            s.fade(g, A("patterns") - 0.6 + c * 0.1, 0.25)
            pat.append((x, y - 10))
cue(A("writing"), "key_3", -22)
pl = s.path("M " + " L ".join(f"{x} {y}" for x, y in pat), GOLD, 4, style="filter:drop-shadow(0 0 8px rgba(232,194,106,0.8))"); s.draw(pl, A("patterns") - 0.2, 0.7)
cue(A("patterns") - 0.2, "swell_1", -20)
lv3 = hatfig(s, 200, 0.75, WHITE); s.walk(lv3, A("left"), 160, 1.4)
pt = s.label(710, 1150, "PATTERNS", 32, GOLD, 0, 800, 0.2); s.fade(pt, A("patterns"), 0.35, y=10)

# 4  "At 15, he made his first trade, $5."
s = S(A("at", 2) - 0.1, A("by", 1) - 0.1)
header(s, "AGE 15  ·  FIRST TRADE")
lv4 = hatfig(s, 330, 0.95, WHITE); s.pop(lv4, A("at", 2), 0.4)
bill = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 18px rgba(232,194,106,0.6))"><rect x="520" y="820" width="340" height="170" rx="14" fill="#14120a" stroke="{GOLD}" stroke-width="5"/>'
             f'<circle cx="690" cy="905" r="52" fill="none" stroke="{GOLD}" stroke-width="3"/>'
             f'<text x="690" y="932" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="76" fill="{GOLD}">$5</text></g>', "bl")
s.pop(bill, A("5") - 0.1, 0.45, 0.4, "50% 50%"); cue(A("5") - 0.1, "bell_E5", -18)
ft = s.label(690, 1060, "HIS FIRST TRADE", 30, WHITE, 0, 800, 0.16); s.fade(ft, A("first") - 0.1, 0.35)

# 5  "By 16, trading paid him more than his job ever did."
s = S(A("by", 1) - 0.1, W(F("1907") - 1) - 0.1)
header(s, "AGE 16")
lv5 = hatfig(s, 240, 0.9, WHITE); s.pop(lv5, A("by", 1), 0.4)
s.raw('<line id="@ID@" x1="420" y1="1100" x2="960" y2="1100" stroke="#ffffff60" stroke-width="3"/>', "ax")
jb = s.raw(f'<rect id="@ID@" x="480" y="1040" width="150" height="60" fill="#7d838c" style="opacity:0"/>', "jb")
s.pop(jb, A("job") - 0.1, 0.4, 0.2, "50% 100%")
tb = s.raw(f'<rect id="@ID@" x="730" y="700" width="150" height="400" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 16px rgba(232,194,106,0.55))"/>', "tb")
tl(f'tl.fromTo("#{tb}", {{opacity: 0, scaleY: 0, transformOrigin: "50% 100%"}}, {{opacity: 1, scaleY: 1, duration: 0.9, ease: "power3.out", immediateRender: false}}, {A("trading") - 0.1:.3f});')
s.label(555, 1150, "JOB", 30, LBL, 1, 800, 0.15)
s.label(805, 1150, "TRADING", 30, GOLD, 1, 800, 0.15)
cue(A("trading") - 0.1, "swell_2", -20)

# 6  "In 1907, the market crashed, and he made a million dollars in a single day."
s = S(W(F("1907") - 1) - 0.1, W(F("year")) - 0.35)
header(s, "1907  ·  THE PANIC", RED)
cl = crash_line(s, 120, 680, 520, 420); s.draw(cl, A("crashed") - 0.2, 0.8); cue(A("crashed") - 0.2, "whoosh-long_1", -18)
lv6 = hatfig(s, 820, 1.0, GOLD); s.pop(lv6, A("1907"), 0.45)
sp6 = s.spot(820, 0, "232,194,106", y0=640); s.fade(sp6, A("million", 2) - 0.2, 0.5)
mm = money(s, 540, 1345, "+$1,000,000", 84, GOLD, 0)
tl(f'tl.fromTo("#{mm}", {{opacity: 0, scale: 1.3, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.45, ease: "expo.out", immediateRender: false}}, {A("million", 2) - 0.15:.3f});')
od = s.label(540, 1420, "IN ONE DAY", 32, WHITE, 0, 800, 0.2); s.fade(od, A("single") - 0.1, 0.35)
cue(A("million", 2) - 0.15, "bell_G5", -16)

# 7  "A year later, he ignored his own judgment, took someone else's advice on cotton, and lost almost everything."
s = S(W(F("year")) - 0.35, W(F("1915") - 1) - 0.1)
header(s, "1908  ·  COTTON")
lv7 = hatfig(s, 330, 1.0, WHITE); s.pop(lv7, W(F("year")) - 0.3, 0.4)
mine = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(220, 730, 220, 110, 20)}" fill="#11151b" stroke="{GOLD}" stroke-width="3"/>'
             f'<text x="330" y="798" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" letter-spacing="0.12em" fill="{GOLD}">MY PLAN</text>'
             f'<circle cx="300" cy="870" r="9" fill="{GOLD}"/><circle cx="318" cy="900" r="6" fill="{GOLD}"/></g>', "mp")
s.pop(mine, W(F("year")) - 0.1, 0.4, 0.5, "50% 50%")
tl(f'tl.to("#{mine}", {{opacity: 0.12, duration: 0.6}}, {A("ignored"):.3f});')
xm7 = xmark(s, 330, 785, 40, RED, 6); s.draw(xm7, A("ignored") + 0.1, 0.35); cue(A("ignored") + 0.1, "tock_1", -18)
ot = hatfig(s, 780, 0.95, "#8a8f98", 1, GY, False); s.pop(ot, A("took") - 0.3, 0.4)
tip = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(640, 730, 280, 110, 20)}" fill="#11151b" stroke="#fff" stroke-width="3"/>'
            f'<path d="M 760 838 L 780 880 L 800 838" fill="#11151b" stroke="#fff" stroke-width="3" stroke-linejoin="round"/>'
            f'<text x="780" y="798" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" letter-spacing="0.08em" fill="#fff">COTTON TIP</text></g>', "tp")
s.pop(tip, A("advice") - 0.15, 0.4, 0.5, "50% 50%"); cue(A("advice") - 0.15, "pop_2", -18)
fl7 = s.raw(f'<rect id="@ID@" x="0" y="0" width="1080" height="1920" fill="{RED}" style="opacity:0"/>', "fl")
tl(f'tl.fromTo("#{fl7}", {{opacity: 0.18}}, {{opacity: 0, duration: 0.6, immediateRender: false}}, {A("lost") - 0.05:.3f});')
le = s.label(540, 1330, "LOST ALMOST EVERYTHING", 40, RED, 0, 800, 0.1); s.fade(le, A("lost") - 0.05, 0.35, y=10)
tl(f'tl.to("#{lv7}", {{opacity: 0.5, duration: 0.6}}, {A("lost"):.3f});')
cue(A("lost") - 0.05, "land-light_1", -16)

# 8  "By 1915, he was bankrupt."
s = S(W(F("1915") - 1) - 0.1, A("came") - 0.35)
header(s, "1915")
lv8 = hatfig(s, 540, 1.0, "#8a8f98", 0.85, GY, False); s.pop(lv8, A("1915") - 0.3, 0.4)
stamp(s, 540, 800, "BANKRUPT", RED, 76, A("bankrupt", 1) - 0.35)

# 9  "He came back, he repaid every creditor, and in 1929, as the market collapsed, he made a hundred million dollars."
s = S(A("came") - 0.35, W(F("slowly") - 1) - 0.1)
header(s, "THE COMEBACK")
steps = s.path("M 120 1240 H 300 V 1160 H 440 V 1080 H 580 V 1000 H 720", "#ffffff80", 4); s.draw(steps, A("came") - 0.3, 0.8)
lv9 = hatfig(s, 210, 0.7, WHITE)
tl(f'tl.to("#{lv9}", {{x: 440, y: -240, duration: 1.6, ease: "power1.inOut"}}, {A("came") - 0.1:.3f});')
rp = s.pill(560, 860, "EVERY CREDITOR REPAID", GOLD, "#111", 28); s.pop(rp, A("repaid") - 0.1, 0.4, 0.5, "50% 50%"); cue(A("repaid") - 0.1, "click-confirm_1", -18)
tl(f'tl.to("#{rp}", {{opacity: 0, duration: 0.3}}, {A("1929") - 0.3:.3f});')
tl(f'tl.to("#{steps}", {{opacity: 0.15, duration: 0.4}}, {A("1929") - 0.3:.3f});')
cl9 = crash_line(s, 120, 700, 560, 440); s.draw(cl9, A("collapsed") - 0.2, 0.8); cue(A("collapsed") - 0.2, "whoosh-long_1", -18)
m9 = money(s, 540, 1360, "$100,000,000", 96, GOLD, 0)
tl(f'tl.fromTo("#{m9}", {{opacity: 0, scale: 1.3, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.45, ease: "expo.out", immediateRender: false}}, {A("hundred", 2) - 0.15:.3f});')
cue(A("hundred", 2) - 0.15, "bell_A4", -16)
tl(f'tl.to("#{lv9}", {{opacity: 0, duration: 0.3}}, {A("1929") - 0.3:.3f});')
lv9b = hatfig(s, 860, 1.0, GOLD); s.pop(lv9b, A("1929"), 0.45)
sp9 = s.spot(860, 0, "232,194,106", y0=640); s.fade(sp9, A("hundred", 2) - 0.2, 0.5)

# 10  "Then, slowly, he stopped following his own rules."
s = S(W(F("slowly") - 1) - 0.1, A("by", 3) - 0.1)
header(s, "AFTER 1929")
bk = s.raw(f'<g id="@ID@"><path d="M 760 820 C 720 800 660 800 620 810 V 960 C 660 950 720 950 760 970 C 800 950 860 950 900 960 V 810 C 860 800 800 800 760 820 Z M 760 820 V 970" '
           f'fill="#11151b" stroke="{GOLD}" stroke-width="4" stroke-linejoin="round"/>'
           + "".join(f'<line x1="{640 if j < 4 else 780}" y1="{845 + (j % 4) * 26}" x2="{740 if j < 4 else 880}" y2="{845 + (j % 4) * 26}" stroke="{GOLD}" stroke-width="3"/>' for j in range(8)) +
           f'<text x="760" y="1030" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" letter-spacing="0.2em" fill="{GOLD}">HIS RULES</text></g>', "bk")
tl(f'tl.to("#{bk}", {{opacity: 0.15, duration: 2.2, ease: "power1.in"}}, {A("slowly"):.3f});')
lv10 = hatfig(s, 560, 1.0, WHITE); s.walk(lv10, A("stopped") - 0.2, -330, 1.4)
tl(f'tl.to("#{lv10}", {{opacity: 0.6, duration: 1.2}}, {A("stopped"):.3f});')
cue(A("stopped") - 0.2, "swell_2", -22)

# 11  "By 1934, he was bankrupt again, millions in debt,"
s = S(A("by", 3) - 0.1, TL_OFF)
header(s, "1934")
lv11 = hatfig(s, 540, 1.0, "#8a8f98", 0.8, GY, False); s.pop(lv11, A("1934") - 0.3, 0.4)
stamp(s, 540, 760, "BANKRUPT AGAIN", RED, 64, A("bankrupt", 2) - 0.35)
md = s.label(540, 900, "MILLIONS IN DEBT", 40, RED, 0, 800, 0.12); s.fade(md, A("millions") - 0.1, 0.35, y=10)

# 12  "and his rules were simple. Cut losses fast. Never add to a loser. Wait for the market to prove you right. Trust your own plan."
RULES = [("CUT LOSSES FAST", "cut", 1), ("NEVER ADD TO A LOSER", "never", 1), ("LET THE MARKET PROVE YOU RIGHT", "wait", 1), ("TRUST YOUR OWN PLAN", "trust", 1)]
def rule_rows(s, y0=720, gap=130, op=0):
    rows = []
    for k, (txt, w_, kk) in enumerate(RULES):
        y = y0 + k * gap
        size = 34 if len(txt) < 24 else 28
        r = s.raw(f'<g id="@ID@" style="opacity:{op}"><path d="{rrect(90, y - 48, 900, 96, 18)}" fill="#0f1319" stroke="#ffffff30" stroke-width="2"/>'
                  f'<circle cx="150" cy="{y}" r="26" fill="none" stroke="{GOLD}" stroke-width="3"/>'
                  f'<text x="150" y="{y + 11}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" fill="{GOLD}">{k + 1}</text>'
                  f'<text x="200" y="{y + size * 0.36:.0f}" font-family="Montserrat" font-weight="800" font-size="{size}" letter-spacing="0.03em" fill="#fff">{txt}</text></g>', "rr")
        rows.append(r)
    return rows
s = S(TL_OFF, W(F("never", 2) - 2) - 0.1)
s.label(540, 590, "HIS RULES", 40, GOLD, 1, 800, 0.24)
rr = rule_rows(s)
for k, r in enumerate(rr):
    t = A(RULES[k][1], RULES[k][2]) - 0.15
    tl(f'tl.fromTo("#{r}", {{opacity: 0, x: -40}}, {{opacity: 1, x: 0, duration: 0.4, ease: "power3.out", immediateRender: false}}, {t:.3f});')
    cue(t, "pop_" + str(k + 1), -18)

# 13  "His rules never failed him. He failed his rules."
s = S(W(F("never", 2) - 2) - 0.1, A("best") - 0.25)
rr2 = rule_rows(s, 760, 110, 1)
l1 = s.label(540, 600, "HIS RULES NEVER FAILED HIM.", 40, WHITE, 0, 800, 0.04); s.fade(l1, A("never", 2) - 0.6, 0.4, y=10)
l2 = s.label(540, 680, "HE FAILED HIS RULES.", 44, RED, 0, 800, 0.06); s.fade(l2, A("failed", 2) - 0.15, 0.4, y=10)
for k, r in enumerate(rr2):
    tl(f'tl.to("#{r}", {{opacity: 0.22, duration: 0.35}}, {A("failed", 2) + 0.1 + k * 0.12:.3f});')
cue(A("failed", 2) - 0.15, "tock_1", -16)

# 14  "The best rules in the world mean nothing if you don't follow them every day."
s = S(A("best") - 0.25, A("order") - 0.05)
lv14 = hatfig(s, 540, 0.95, GOLD); s.pop(lv14, A("best") - 0.2, 0.45)
s.spot(540, 1, "232,194,106")
days = ["MON", "TUE", "WED", "THU", "FRI"]
for k, d in enumerate(days):
    x = 180 + k * 180
    s.raw(f'<g id="@ID@"><path d="{rrect(x - 70, 640, 140, 150, 16)}" fill="#0f1319" stroke="#ffffff50" stroke-width="2"/>'
          f'<text x="{x}" y="680" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="28" fill="{LBL}">{d}</text></g>', "dy")
    ck = s.path(f"M {x - 30} 735 L {x - 8} 758 L {x + 32} 708", GOLD, 7, style="filter:drop-shadow(0 0 8px rgba(232,194,106,0.8))")
    s.draw(ck, A("follow", 1) + k * 0.18, 0.3)
    cue(A("follow", 1) + k * 0.18, "tick-crisp_" + str(k % 3 + 1), -20)
ed = s.label(540, 870, "EVERY DAY", 44, GOLD, 0, 800, 0.24); s.fade(ed, A("every", 2) - 0.1, 0.4, y=10)
br = s.label(540, 590, "THE BEST RULES MEAN NOTHING…", 32, WHITE, 0, 800, 0.08); s.fade(br, A("best") - 0.1, 0.4)

# 15  outro (handles, no end card)
s = S(A("order") - 0.05, TOTAL)
es = s.spot(540, 0, "232,194,106", 40, 230); s.fade(es, A("order"), 0.6)
em = s.raw('<image id="@ID@" href="assets/otm_emblem.png" x="390" y="900" width="300" height="291" style="opacity:0;filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>', "i")
s.pop(em, A("order"), 0.7, 0.6, "50% 50%"); cue(A("order"), "bell_A4", -16)
o1 = s.label(540, 1300, "ORDER THE MARKET", 32, GOLD, 0, 800, 0.3); s.fade(o1, A("order") + 0.3, 0.5)
o2 = s.label(540, 1360, "DON'T LET THE MARKET ORDER YOU", 28, WHITE, 0, 700, 0.12); s.fade(o2, A("don't", 2), 0.4)
o3 = s.pill(540, 1470, "FOLLOW FOR MORE", GOLD, "#111", 30); s.pop(o3, A("follow", 2), 0.4, 0.6, "50% 50%"); cue(A("follow", 2), "click-confirm_1", -16)
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
    <div id="root" data-composition-id="otm-livermore" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
{TIMELINE}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-livermore-audio" class="clip" src="assets/audio/mix_livermore.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-livermore"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
