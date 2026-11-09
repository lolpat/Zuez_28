"""OTM "The $100 Million Lesson" (Jesse Livermore), detailed version: a glowing-figure story in the OTM style (same scene
system as otm-chance / otm-break). Livermore is the figure in the fedora; a timeline across the top lights each year as
the story reaches it (1891 to 1940). 23 scenes: the hook, the name, school -> farm -> Boston with $5, Paine Webber at
$5 a week and the notebook of patterns, the bucket shop (no real stock, just a bet up or down), the first $5 railroad
bet, $5 vs ~$200 a week, banned (the Boy Plunger), 1907 borrowed money and the bet against it, the panic (+$1,000,000),
the 1908 cotton tip, BANKRUPT 1915, the Bethlehem Steel comeback and the creditors repaid, the 1920s borrowing boom,
1929 ($100,000,000), the rules slipping, 1934 (debt vs what was left), his rules written down in 1940, rule 3 broken,
"he failed his rules", "every day", and the outro with the handles. Original script, voice only (Quentin), no music.
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


def ix(i):
    """start of word i of work/words.json on the video clock (the detailed take: indices are stable for this voice)"""
    return W(i)

def header(s, text, col=LBL):
    return s.label(540, 590, text, 30, col, 1, 700, 0.2)

def coin(s, x, y, text="$5", r=46, op=0):
    return s.raw(f'<g id="@ID@" style="opacity:{op};filter:drop-shadow(0 0 14px rgba(232,194,106,0.6))"><circle cx="{x}" cy="{y}" r="{r}" fill="#1a160b" stroke="{GOLD}" stroke-width="5"/>'
                 f'<text x="{x}" y="{y + r * 0.36:.0f}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="{int(r * 0.95)}" fill="{GOLD}">{text}</text></g>', "cn")

def shop(s, x0, gy=GY, op=1):
    """a small storefront with an awning and a BUCKET SHOP sign"""
    w = 330
    aw = "".join(f'<rect x="{x0 + k * 33}" y="{gy - 300}" width="33" height="40" fill="{RED if k % 2 else "#e9ecf1"}" opacity="0.85"/>' for k in range(10))
    return s.raw(f'<g id="@ID@" style="opacity:{op}"><rect x="{x0}" y="{gy - 260}" width="{w}" height="260" fill="#0f1319" stroke="#fff" stroke-width="4"/>{aw}'
                 f'<rect x="{x0 + 40}" y="{gy - 370}" width="{w - 80}" height="60" rx="8" fill="#11151b" stroke="{GOLD}" stroke-width="3"/>'
                 f'<text x="{x0 + w / 2}" y="{gy - 329}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" letter-spacing="0.08em" fill="{GOLD}">BUCKET SHOP</text>'
                 f'<rect x="{x0 + 120}" y="{gy - 170}" width="90" height="170" fill="#1c222c" stroke="#fff" stroke-width="3"/>'
                 f'<rect x="{x0 + 20}" y="{gy - 200}" width="80" height="80" fill="#1c222c" stroke="#ffffff90" stroke-width="2"/>'
                 f'<rect x="{x0 + 230}" y="{gy - 200}" width="80" height="80" fill="#1c222c" stroke="#ffffff90" stroke-width="2"/></g>', "shop")

def arrow(x, y, up=True, h=120, w=70):
    if up:
        return f"M {x} {y + h / 2} V {y - h / 2 + 30} M {x - w / 2} {y - h / 2 + 40} L {x} {y - h / 2} L {x + w / 2} {y - h / 2 + 40}"
    return f"M {x} {y - h / 2} V {y + h / 2 - 30} M {x - w / 2} {y + h / 2 - 40} L {x} {y + h / 2} L {x + w / 2} {y + h / 2 - 40}"

def loan_tag(s, x, y, op=0):
    return s.raw(f'<g id="@ID@" style="opacity:{op}"><rect x="{x - 26}" y="{y - 20}" width="52" height="40" rx="8" fill="{RED}"/>'
                 f'<text x="{x}" y="{y + 11}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" fill="#fff">$</text></g>', "lt")

def bar(s, x, top, w, col, gy=1100, op=0, glow=True):
    g = f";filter:drop-shadow(0 0 14px {col}80)" if glow else ""
    return s.raw(f'<rect id="@ID@" x="{x - w / 2}" y="{top}" width="{w}" height="{gy - top}" fill="{col}" style="opacity:{op}{g}"/>', "bar")

def grow(i, t, d=0.9):
    tl(f'tl.fromTo("#{i}", {{opacity: 0, scaleY: 0, transformOrigin: "50% 100%"}}, {{opacity: 1, scaleY: 1, duration: {d}, ease: "power3.out", immediateRender: false}}, {t:.3f});')

# ---------------------------------------------------------------- the timeline across the top (1891 to 1940)
YEARS = [(1891, 31), (1892, 90), (1893, 125), (1900, 153), (1907, 179), (1908, 220), (1915, 242), (1929, 290), (1934, 330), (1940, 345)]
T_YEAR = [ix(i) - 0.1 for _, i in YEARS]
TL_ON, TL_OFF = ix(31) - 0.15, ix(380) - 0.1
tlx = [90 + i * 100 for i in range(len(YEARS))]
tlsvg = f'<line x1="60" y1="430" x2="1020" y2="430" stroke="#ffffff40" stroke-width="2"/>'
for i, (yr, _) in enumerate(YEARS):
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

# 1  "He made a hundred million dollars in the market... and ended up buried in debt."
s = S(0, ix(15) - 0.1, first=True)
sp1 = s.spot(540, 1, "232,194,106")
lv1 = hatfig(s, 540, 1.05, GOLD)
s.label(540, 600, "HE MADE", 34, LBL, 1, 700, 0.3)
m1 = money(s, 540, 720, "$100,000,000", 104, GOLD, 1)
tl(f'tl.fromTo("#{m1}", {{scale: 0.96, transformOrigin: "50% 50%"}}, {{scale: 1.03, duration: {ix(10) - 0.2:.3f}, ease: "none"}}, 0);')
m1r = money(s, 540, 720, "$100,000,000", 104, RED, 0)
cr = s.path("M 170 690 L 910 700", RED, 8); s.draw(cr, ix(12) - 0.1, 0.35)
tl(f'tl.to("#{m1}", {{opacity: 0, duration: 0.3}}, {ix(12) - 0.1:.3f});'); s.fade(m1r, ix(12) - 0.1, 0.3)
tl(f'tl.to("#{sp1}", {{opacity: 0.25, duration: 0.6}}, {ix(12) - 0.1:.3f});')
tl(f'tl.to("#{lv1}", {{opacity: 0.55, duration: 0.6}}, {ix(12) - 0.1:.3f});')
db = s.label(540, 860, "BURIED IN DEBT", 44, RED, 0, 800, 0.12); s.fade(db, ix(14) - 0.1, 0.4, y=12); cue(ix(14) - 0.1, "tock_1", -16)

# 2  "His name was Jesse Livermore. And his story might be the most expensive lesson in trading."
s = S(ix(15) - 0.1, ix(31) - 0.15)
s.spot(540, 1, "232,194,106")
lv2 = hatfig(s, 540, 1.05, WHITE); s.pop(lv2, ix(15), 0.45)
n1 = s.label(540, 720, "JESSE", 92, WHITE, 0, 800, 0.08); s.fade(n1, ix(18) - 0.1, 0.4, y=14)
n2 = s.label(540, 820, "LIVERMORE", 92, GOLD, 0, 800, 0.08); s.fade(n2, ix(19) - 0.1, 0.4, y=14)
n3 = s.label(540, 890, "1877 – 1940", 30, LBL, 0, 700, 0.3); s.fade(n3, ix(19) + 0.3, 0.4)
n4 = s.label(540, 1340, "THE MOST EXPENSIVE LESSON IN TRADING", 30, GOLD, 0, 800, 0.08); s.fade(n4, ix(26) - 0.1, 0.4, y=10)
cue(ix(18) - 0.1, "swell_1", -18); cue(ix(27), "bell_E5", -20)

# 3  "1891. He's 14. His father pulls him out of school to work on the farm. So he leaves for Boston, with $5 in his pocket."
s = S(ix(31) - 0.15, ix(56) - 0.1)
header(s, "1891  ·  AGE 14")
sch = s.raw(f'<g id="@ID@"><path d="M 60 1240 V 1110 L 150 1050 L 240 1110 V 1240 Z" fill="#0f1319" stroke="#fff" stroke-width="4" stroke-linejoin="round"/>'
            f'<rect x="125" y="1170" width="50" height="70" fill="none" stroke="#fff" stroke-width="3"/><circle cx="150" cy="1095" r="12" fill="none" stroke="{GOLD}" stroke-width="3"/></g>', "sc")
s.label(150, 1290, "SCHOOL", 28, GREY, 1, 700, 0.15)
xs = xmark(s, 150, 1150, 46, RED, 6); s.draw(xs, ix(38) - 0.1, 0.35); cue(ix(38), "tock_1", -18)
s.raw(f'<g id="@ID@" style="opacity:0.7"><path d="M 400 1240 V 1150 L 460 1100 L 520 1150 V 1240 Z M 440 1240 V 1190 H 480 V 1240" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/></g>', "bn")
s.label(460, 1290, "FARM", 28, GREY, 1, 700, 0.15)
fa = s.fig(600, 1.0, "#8a8f98", 1, False); s.pop(fa, ix(35) - 0.1, 0.4)
tl(f'tl.to("#{fa}", {{opacity: 0.25, duration: 0.5}}, {ix(48) - 0.2:.3f});')
s.raw(f'<g id="@ID@"><line x1="900" y1="1240" x2="900" y2="1020" stroke="#c9a46a" stroke-width="6"/>'
      f'<path d="M 830 1030 H 990 L 1020 1060 L 990 1090 H 830 Z" fill="#11151b" stroke="{GOLD}" stroke-width="3"/>'
      f'<text x="915" y="1071" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" letter-spacing="0.1em" fill="{GOLD}">BOSTON</text></g>', "sg")
kid = hatfig(s, 260, 0.72, WHITE); s.pop(kid, ix(31), 0.4)
s.walk(kid, ix(36), 210, 1.1)
s.walk(kid, ix(48) - 0.1, 300, 1.5)
c3 = coin(s, 770, 960); s.pop(c3, ix(52) - 0.1, 0.4, 0.4, "50% 50%"); cue(ix(52) - 0.1, "bell_C5", -18)

# 4  "He gets a job at a brokerage, Paine Webber, writing stock prices on a giant chalkboard. $5 a week. Day after day ... patterns. ... a notebook."
s = S(ix(56) - 0.1, ix(90) - 0.1)
header(s, "PAINE WEBBER  ·  BOSTON")
bx0, by0, bw, bh = 430, 680, 560, 400
s.raw(f'<g id="@ID@"><rect x="{bx0}" y="{by0}" width="{bw}" height="{bh}" rx="8" fill="#10201a" stroke="#c9a46a" stroke-width="10"/>'
      f'<line x1="{bx0 + 40}" y1="{by0 + bh + 6}" x2="{bx0 + 40}" y2="1240" stroke="#c9a46a" stroke-width="6"/><line x1="{bx0 + bw - 40}" y1="{by0 + bh + 6}" x2="{bx0 + bw - 40}" y2="1240" stroke="#c9a46a" stroke-width="6"/></g>', "cb")
r3 = random.Random(3)
cols, rows = 5, 5
vals = [[round(100 + r3.uniform(-9, 9), 1) for _ in range(cols)] for _ in range(rows)]
zig = [4, 2, 3, 1, 0]
pat = []
for c in range(cols):
    for r in range(rows):
        x, y = bx0 + 62 + c * 108, by0 + 66 + r * 70
        i = s.raw(f'<text id="@ID@" x="{x}" y="{y}" text-anchor="middle" font-family="Montserrat" font-weight="600" font-size="28" fill="#e8efe9" style="opacity:0">{vals[r][c]}</text>', "ch")
        tl(f'tl.fromTo("#{i}", {{opacity: 0}}, {{opacity: 0.85, duration: 0.12, immediateRender: false}}, {ix(63) + (c * rows + r) * 0.07:.3f});')
        if zig[c] == r:
            g = s.raw(f'<text id="@ID@" x="{x}" y="{y}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 8px {GOLD})">{vals[r][c]}</text>', "cg")
            s.fade(g, ix(82) - 0.6 + c * 0.1, 0.25)
            pat.append((x, y - 10))
cue(ix(63), "key_3", -22); cue(ix(77), "key_5", -24)
pl = s.path("M " + " L ".join(f"{x} {y}" for x, y in pat), GOLD, 4, style="filter:drop-shadow(0 0 8px rgba(232,194,106,0.8))"); s.draw(pl, ix(82) - 0.2, 0.7)
cue(ix(82) - 0.2, "swell_1", -20)
lv4 = hatfig(s, 250, 0.8, WHITE); s.pop(lv4, ix(56), 0.4)
wk = s.pill(250, 880, "$5 / WEEK", GOLD, "#111", 30); s.pop(wk, ix(70) - 0.1, 0.4, 0.5, "50% 50%"); cue(ix(70) - 0.1, "pop_1", -18)
tl(f'tl.to("#{wk}", {{opacity: 0, duration: 0.3}}, {ix(83) - 0.3:.3f});')
nb = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="150" y="790" width="200" height="150" rx="10" fill="#f3ead8" stroke="{GOLD}" stroke-width="3"/>'
           + "".join(f'<line x1="170" y1="{820 + k * 24}" x2="330" y2="{820 + k * 24}" stroke="#b9ad93" stroke-width="2"/>' for k in range(5)) +
           f'<path d="M 170 915 L 210 870 L 245 890 L 290 835 L 330 845" fill="none" stroke="{RED}" stroke-width="4"/></g>', "nb")
s.pop(nb, ix(89) - 0.15, 0.4, 0.5, "50% 50%"); cue(ix(89) - 0.15, "click_1", -18)
s.label(250, 990, "NOTEBOOK", 28, LBL, 0, 700, 0.15); s.fade(s.items[-1].split('"')[1], ix(89), 0.3)

# 5  "At 15, he walks into a bucket shop. It doesn't buy real stock. You just bet on whether the price will go up or down."
s = S(ix(90) - 0.1, ix(115) - 0.1)
header(s, "1892  ·  AGE 15")
sh5 = shop(s, 120, GY, 0); s.fade(sh5, ix(95) - 0.2, 0.4); cue(ix(96), "pop_2", -20)
lv5 = hatfig(s, 900, 0.78, WHITE); s.pop(lv5, ix(90), 0.4); s.walk(lv5, ix(92), -330, 1.3)
cert = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="620" y="680" width="340" height="200" rx="8" fill="#f3ead8" stroke="{GOLD}" stroke-width="4"/>'
             f'<rect x="636" y="696" width="308" height="168" rx="4" fill="none" stroke="#b9925a" stroke-width="2"/>'
             f'<text x="790" y="768" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" letter-spacing="0.2em" fill="#6b5130">STOCK</text>'
             f'<text x="790" y="812" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="28" fill="#8c7350">CERTIFICATE</text></g>', "ce")
s.pop(cert, ix(98) - 0.1, 0.4, 0.5, "50% 50%")
xc = xmark(s, 790, 780, 70, RED, 8); s.draw(xc, ix(101) - 0.1, 0.35); cue(ix(101) - 0.1, "tock_1", -18)
nr = s.label(790, 930, "NO REAL STOCK", 30, RED, 0, 800, 0.12); s.fade(nr, ix(101), 0.35)
for k, (up, w_) in enumerate([(True, 112), (False, 114)]):
    tl(f'tl.to("#{cert}", {{opacity: 0, duration: 0.3}}, {ix(105) - 0.3:.3f});') if k == 0 else None
    x = 700 + k * 200
    ar = s.path(arrow(x, 790, up, 170, 90), GOLD if up else RED, 10, style=f"filter:drop-shadow(0 0 10px {GOLD if up else RED})")
    s.draw(ar, ix(w_) - 0.15, 0.35)
    lb = s.label(x, 930, "UP" if up else "DOWN", 32, GOLD if up else RED, 0, 800, 0.15); s.fade(lb, ix(w_) - 0.1, 0.3)
    cue(ix(w_) - 0.1, "tick-crisp_" + str(k + 1), -18)
for i in (xc, nr):
    tl(f'tl.to("#{i}", {{opacity: 0, duration: 0.3}}, {ix(105) - 0.3:.3f});')
bt = s.label(800, 1010, "JUST A BET", 34, WHITE, 0, 800, 0.15); s.fade(bt, ix(105), 0.35, y=10)

# 6  "His first bet, $5 on a railroad stock. He wins."
s = S(ix(115) - 0.1, ix(125) - 0.1)
header(s, "HIS FIRST BET")
lv6 = hatfig(s, 220, 0.8, WHITE); s.pop(lv6, ix(115), 0.4)
train = s.raw(f'<g id="@ID@"><rect x="420" y="1100" width="300" height="100" rx="10" fill="#0f1319" stroke="#fff" stroke-width="4"/>'
              f'<rect x="620" y="1030" width="110" height="170" rx="8" fill="#0f1319" stroke="#fff" stroke-width="4"/>'
              f'<rect x="640" y="1050" width="70" height="50" fill="#1c222c" stroke="{GOLD}" stroke-width="2"/>'
              f'<rect x="460" y="1060" width="40" height="40" fill="#0f1319" stroke="#fff" stroke-width="4"/>'
              + "".join(f'<circle cx="{cx}" cy="1210" r="28" fill="#000" stroke="#fff" stroke-width="4"/>' for cx in (470, 560, 670)) +
              f'<path d="M 420 1180 L 380 1236 H 420" fill="none" stroke="#fff" stroke-width="4"/></g>', "tr")
tl(f'tl.fromTo("#{train}", {{x: 520, opacity: 0}}, {{x: 0, opacity: 1, duration: 1.0, ease: "power2.out", immediateRender: false}}, {ix(121) - 0.6:.3f});')
tl(f'tl.set("#{train}", {{opacity: 0}}, {ix(115) - 0.1:.3f});')
cue(ix(121) - 0.6, "whoosh-long_1", -20)
s.label(580, 980, "RAILROAD STOCK", 30, LBL, 0, 700, 0.15); s.fade(s.items[-1].split('"')[1], ix(121), 0.35)
c6 = coin(s, 540, 780, "$5", 60); s.pop(c6, ix(118) - 0.1, 0.4, 0.4, "50% 50%"); cue(ix(118) - 0.1, "pop_3", -18)
win = s.label(820, 800, "WIN", 96, GOLD, 0, 800, 0.08)
tl(f'tl.fromTo("#{win}", {{opacity: 0, scale: 1.4, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.4, ease: "expo.out", immediateRender: false}}, {ix(124) - 0.1:.3f});')
cue(ix(124) - 0.1, "bell_G5", -16)

# 7  "By 16, he's making around $200 a week. He quits his job."
s = S(ix(125) - 0.1, ix(137) - 0.1)
header(s, "1893  ·  AGE 16")
lv7 = hatfig(s, 180, 0.8, WHITE); s.pop(lv7, ix(125), 0.4)
s.raw('<line id="@ID@" x1="330" y1="1100" x2="980" y2="1100" stroke="#ffffff60" stroke-width="3"/>', "ax")
jb = bar(s, 480, 1090, 170, "#7d838c", 1100, 0, False); grow(jb, ix(125) + 0.3, 0.5)
tb = bar(s, 790, 700, 170, GOLD, 1100, 0); grow(tb, ix(128) - 0.1, 1.0); cue(ix(128) - 0.1, "swell_2", -20)
s.label(480, 1150, "JOB", 30, LBL, 1, 800, 0.15); s.label(480, 1060, "$5/WK", 30, LBL, 1, 800, 0.05)
s.label(790, 1150, "TRADING", 30, GOLD, 1, 800, 0.15)
t7 = s.label(790, 670, "~$200/WK", 36, GOLD, 0, 800, 0.05); s.fade(t7, ix(130) - 0.1, 0.35, y=10)
xq = xmark(s, 480, 1060, 60, RED, 7); s.draw(xq, ix(134) - 0.1, 0.35); cue(ix(134) - 0.1, "tock_1", -18)
qt = s.label(480, 980, "QUITS", 34, RED, 0, 800, 0.15); s.fade(qt, ix(134), 0.3)

# 8  "He wins so often that the bucket shops ban him. They call him the Boy Plunger."
s = S(ix(137) - 0.1, ix(153) - 0.15)
header(s, "1893")
sh8 = shop(s, 120, GY, 1)
lv8 = hatfig(s, 580, 0.78, GOLD); s.pop(lv8, ix(137), 0.4)
cs = [coin(s, 505 + k * 50, 1000 - (k % 2) * 30, "$", 26) for k in range(4)]
for k, c in enumerate(cs):
    s.pop(c, ix(138) + k * 0.12, 0.3, 0.4, "50% 50%")
stamp(s, 285, 1040, "BANNED", RED, 52, ix(145) - 0.35)
s.walk(lv8, ix(146), 330, 1.2)
bp1 = s.label(800, 760, "THE BOY", 64, WHITE, 0, 800, 0.08); s.fade(bp1, ix(150) - 0.1, 0.4, y=12)
bp2 = s.label(800, 840, "PLUNGER", 64, GOLD, 0, 800, 0.08); s.fade(bp2, ix(151) - 0.1, 0.4, y=12)
cue(ix(151) - 0.1, "swell_1", -18)

# 8b  "1900, he moves to New York to trade with real brokers. Real orders fill slower than bucket-shop bets, and he loses everything. So he adapts."
s = S(ix(153) - 0.15, ix(179) - 0.15)
header(s, "1900  ·  NEW YORK")
sky = ""
for x, w, h in [(600, 90, 260), (700, 110, 360), (820, 80, 220), (910, 120, 300)]:
    sky += f'<rect x="{x}" y="{1240 - h}" width="{w}" height="{h}" fill="#0f1319" stroke="#ffffffb0" stroke-width="3"/>'
    sky += "".join(f'<rect x="{x + 12 + c * 22}" y="{1240 - h + 20 + r * 34}" width="10" height="16" fill="{GOLD}" opacity="0.45"/>' for c in range(max(1, (w - 20) // 22)) for r in range(max(1, (h - 40) // 34)))
s.raw(f'<g id="@ID@">{sky}</g>', "sky")
s.label(815, 1290, "NEW YORK", 28, GREY, 1, 700, 0.2)
lv8b = hatfig(s, 120, 0.8, WHITE); s.pop(lv8b, ix(153), 0.4); s.walk(lv8b, ix(155), 260, 1.4)
for k, (lab, col, d, tag) in enumerate([("BUCKET SHOP", GOLD, 0.25, "INSTANT"), ("REAL MARKET", "#9aa0a8", 1.7, "DELAY")]):
    y = 720 + k * 110
    s.label(100, y + 10, lab, 28, LBL, 0 if False else 1, 800, 0.08, "start")
    s.raw(f'<rect id="@ID@" x="380" y="{y - 12}" width="420" height="22" rx="11" fill="#ffffff1c"/>', "tk")
    fb = s.raw(f'<rect id="@ID@" x="380" y="{y - 12}" width="0" height="22" rx="11" fill="{col}"/>', "fb")
    t0 = ix(164) - 0.1 + k * 0.05
    tl(f'tl.fromTo("#{fb}", {{attr: {{width: 0}}}}, {{attr: {{width: 420}}, duration: {d}, ease: "{"power2.out" if k == 0 else "power1.in"}", immediateRender: false}}, {t0:.3f});')
    tg = s.label(822, y + 10, tag, 28, col, 0, 800, 0.08, "start"); s.fade(tg, t0 + d, 0.3)
    cue(t0 + d, "tick-crisp_1" if k == 0 else "tock_1", -20)
fl8b = s.raw(f'<rect id="@ID@" x="0" y="0" width="1080" height="1920" fill="{RED}" style="opacity:0"/>', "fl")
tl(f'tl.fromTo("#{fl8b}", {{opacity: 0.18}}, {{opacity: 0, duration: 0.6, immediateRender: false}}, {ix(174) - 0.05:.3f});')
le8b = s.label(540, 1350, "LOST EVERYTHING", 40, RED, 0, 800, 0.1); s.fade(le8b, ix(174) - 0.05, 0.35, y=10)
tl(f'tl.to("#{lv8b}", {{opacity: 0.45, duration: 0.5}}, {ix(174):.3f});')
cue(ix(174) - 0.05, "land-light_1", -16)
lv8g = hatfig(s, 380, 0.8, GOLD, 0); s.fade(lv8g, ix(176), 0.6)
tl(f'tl.to("#{lv8b}", {{opacity: 0, duration: 0.4}}, {ix(176):.3f});')
ad = s.label(540, 1420, "SO HE ADAPTS", 36, GOLD, 0, 800, 0.15); s.fade(ad, ix(176), 0.4, y=10)
tl(f'tl.to("#{le8b}", {{opacity: 0.35, duration: 0.4}}, {ix(176):.3f});')
cue(ix(176), "swell_1", -20)

# 9  "1907, he sees too many people borrowing money to buy stocks. So he bets against the market."
s = S(ix(179) - 0.15, ix(196) - 0.1)
header(s, "1907")
crowd = []
for k in range(6):
    x = 110 + k * 105
    f = s.fig(x, 0.6, "#8a8f98", 1, False); s.pop(f, ix(183) - 0.1 + k * 0.08, 0.3); crowd.append(f)
    tg = loan_tag(s, x, 1020); s.pop(tg, ix(185) - 0.1 + k * 0.1, 0.3, 0.4, "50% 50%")
bm = s.label(375, 920, "BORROWED MONEY", 32, RED, 0, 800, 0.12); s.fade(bm, ix(185), 0.35, y=10)
cue(ix(185), "pop_2", -20)
lv9 = hatfig(s, 900, 1.0, GOLD); s.pop(lv9, ix(190) - 0.1, 0.45)
dar = s.path(arrow(900, 820, False, 190, 100), GOLD, 12, style=f"filter:drop-shadow(0 0 10px {GOLD})"); s.draw(dar, ix(192) - 0.1, 0.4)
ba = s.label(800, 680, "BETS AGAINST IT", 32, GOLD, 0, 800, 0.1); s.fade(ba, ix(192), 0.35, y=10)
cue(ix(192) - 0.1, "whoosh-short_1", -18)

# 10  "The panic hits. In a single day, he makes a million dollars."
s = S(ix(196) - 0.1, ix(220) - 0.15)
header(s, "1907  ·  THE PANIC", RED)
cl = crash_line(s, 120, 680, 520, 420); s.draw(cl, ix(197) - 0.2, 0.8); cue(ix(197) - 0.2, "whoosh-long_1", -18)
lv10 = hatfig(s, 820, 1.0, GOLD); s.pop(lv10, ix(196), 0.45)
sp10 = s.spot(820, 0, "232,194,106", y0=640); s.fade(sp10, ix(206) - 0.2, 0.5)
mm = money(s, 540, 1345, "+$1,000,000", 84, GOLD, 0)
tl(f'tl.fromTo("#{mm}", {{opacity: 0, scale: 1.3, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.45, ease: "expo.out", immediateRender: false}}, {ix(206) - 0.15:.3f});')
od = s.label(540, 1420, "IN ONE DAY", 32, WHITE, 0, 800, 0.2); s.fade(od, ix(201) - 0.1, 0.35)
cue(ix(206) - 0.15, "bell_G5", -16)
tl(f'tl.to("#{cl}", {{opacity: 0.18, duration: 0.4}}, {ix(208) - 0.3:.3f});')
tgm = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(100, 690, 500, 210, 14)}" fill="#f3ead8" stroke="{GOLD}" stroke-width="3"/>'
            f'<text x="130" y="735" font-family="Montserrat" font-weight="800" font-size="28" letter-spacing="0.2em" fill="#8c7350">TELEGRAM</text>'
            f'<text x="130" y="795" font-family="Montserrat" font-weight="800" font-size="30" fill="#3b2a14">FROM: J.P. MORGAN</text>'
            f'<text x="130" y="860" font-family="Montserrat" font-weight="800" font-size="34" fill="#a3262f">PLEASE STOP SELLING</text></g>', "tg")
tl(f'tl.fromTo("#{tgm}", {{opacity: 0, y: 30, rotation: -4, transformOrigin: "50% 50%"}}, {{opacity: 1, y: 0, rotation: -2, duration: 0.5, ease: "back.out(1.6)", immediateRender: false}}, {ix(208) - 0.1:.3f});')
cue(ix(208) - 0.1, "click_2", -18)
hd = s.label(250, 982, "HE DOES", 36, GOLD, 0, 800, 0.15, "start"); s.fade(hd, ix(218) - 0.05, 0.35, y=10)
hck = s.path("M 196 966 L 212 984 L 238 950", GOLD, 6); s.draw(hck, ix(218) - 0.05, 0.3)
cue(ix(218) - 0.05, "pop_1", -18)

# 11  "1908, he ignores his own judgment and follows another trader's advice on cotton. The price falls, and almost everything is gone."
s = S(ix(220) - 0.15, ix(241) - 0.1)
header(s, "1908  ·  COTTON")
lv11 = hatfig(s, 330, 1.0, WHITE); s.pop(lv11, ix(220), 0.4)
mine = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(220, 730, 220, 110, 20)}" fill="#11151b" stroke="{GOLD}" stroke-width="3"/>'
             f'<text x="330" y="798" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" letter-spacing="0.12em" fill="{GOLD}">MY PLAN</text>'
             f'<circle cx="300" cy="870" r="9" fill="{GOLD}"/><circle cx="318" cy="900" r="6" fill="{GOLD}"/></g>', "mp")
s.pop(mine, ix(220) + 0.2, 0.4, 0.5, "50% 50%")
tl(f'tl.to("#{mine}", {{opacity: 0.12, duration: 0.6}}, {ix(222):.3f});')
xm11 = xmark(s, 330, 785, 40, RED, 6); s.draw(xm11, ix(222) + 0.1, 0.35); cue(ix(222) + 0.1, "tock_1", -18)
ot = hatfig(s, 780, 0.95, "#8a8f98", 1, GY, False); s.pop(ot, ix(227) - 0.2, 0.4)
tip = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(640, 730, 280, 110, 20)}" fill="#11151b" stroke="#fff" stroke-width="3"/>'
            f'<path d="M 760 838 L 780 880 L 800 838" fill="#11151b" stroke="#fff" stroke-width="3" stroke-linejoin="round"/>'
            f'<text x="780" y="798" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" letter-spacing="0.08em" fill="#fff">COTTON TIP</text></g>', "tp")
s.pop(tip, ix(230) - 0.15, 0.4, 0.5, "50% 50%"); cue(ix(230) - 0.15, "pop_2", -18)
fall = s.path("M 520 700 L 580 720 L 610 700 L 660 790 L 700 770 L 760 880 L 800 860 L 860 960", RED, 5); s.draw(fall, ix(234) - 0.1, 0.7)
tl(f'tl.to("#{tip}", {{opacity: 0, duration: 0.3}}, {ix(234) - 0.2:.3f});')
fl11 = s.raw(f'<rect id="@ID@" x="0" y="0" width="1080" height="1920" fill="{RED}" style="opacity:0"/>', "fl")
tl(f'tl.fromTo("#{fl11}", {{opacity: 0.18}}, {{opacity: 0, duration: 0.6, immediateRender: false}}, {ix(237) - 0.05:.3f});')
le = s.label(540, 1330, "ALMOST EVERYTHING GONE", 40, RED, 0, 800, 0.1); s.fade(le, ix(237) - 0.05, 0.35, y=10)
tl(f'tl.to("#{lv11}", {{opacity: 0.5, duration: 0.6}}, {ix(237):.3f});')
cue(ix(237) - 0.05, "land-light_1", -16)

# 12  "By 1915, he's bankrupt,"
s = S(ix(241) - 0.1, ix(245) - 0.1)
header(s, "1915")
lv12 = hatfig(s, 540, 1.0, "#8a8f98", 0.85, GY, False); s.pop(lv12, ix(241), 0.4)
stamp(s, 540, 800, "BANKRUPT", RED, 76, ix(244) - 0.35)

# 13  "but he doesn't quit. He waits for the right setup, buys Bethlehem Steel, and climbs back."
s = S(ix(245) - 0.1, ix(261) - 0.1)
header(s, "THE COMEBACK")
dq = s.label(540, 680, "HE DOESN'T QUIT", 40, WHITE, 0, 800, 0.1); s.fade(dq, ix(246), 0.4, y=10)
hg = s.raw(f'<g id="@ID@" style="opacity:0"><path d="M 800 700 H 900 M 800 840 H 900 M 812 700 C 812 760 888 760 888 770 C 888 780 812 780 812 840 M 888 700 C 888 760 812 760 812 770 C 812 780 888 780 888 840" '
           f'fill="none" stroke="{GOLD}" stroke-width="5" stroke-linecap="round"/></g>', "hg")
s.pop(hg, ix(250) - 0.1, 0.4, 0.5, "50% 50%"); cue(ix(250) - 0.1, "tick_2", -18)
ws = s.label(800, 900, "WAITS FOR THE SETUP", 28, GOLD, 0, 800, 0.08); s.fade(ws, ix(252), 0.35)
for i in (hg, ws):
    tl(f'tl.to("#{i}", {{opacity: 0, duration: 0.3}}, {ix(255) - 0.35:.3f});')
beam = s.raw(f'<g id="@ID@" style="opacity:0"><path d="M 760 700 H 940 V 730 H 870 V 820 H 940 V 850 H 760 V 820 H 830 V 730 H 760 Z" fill="#c5ccd6" stroke="#fff" stroke-width="3"/></g>', "ib")
s.pop(beam, ix(255) - 0.1, 0.4, 0.5, "50% 50%"); cue(ix(255) - 0.1, "land-light_1", -18)
bs = s.label(850, 900, "BETHLEHEM STEEL", 30, WHITE, 0, 800, 0.08); s.fade(bs, ix(256) - 0.1, 0.35)
steps = s.path("M 100 1240 H 240 V 1170 H 360 V 1100 H 480 V 1030 H 600", "#ffffff90", 4); s.draw(steps, ix(259) - 0.6, 0.6)
lv13 = hatfig(s, 170, 0.7, WHITE); s.pop(lv13, ix(245), 0.4)
tl(f'tl.to("#{lv13}", {{x: 370, y: -210, duration: 1.4, ease: "power1.inOut"}}, {ix(259) - 0.3:.3f});')
up13 = s.path("M 640 1180 L 700 1120 L 740 1140 L 820 1040 L 860 1060 L 960 940", GOLD, 5); s.draw(up13, ix(259) - 0.2, 0.8)
cue(ix(259) - 0.2, "swell_2", -20)

# 14  "He repays every creditor, even though the law says he doesn't have to."
s = S(ix(261) - 0.1, ix(274) - 0.1)
header(s, "THE COMEBACK")
lv14 = hatfig(s, 220, 1.0, GOLD); s.pop(lv14, ix(261), 0.4)
for k in range(3):
    x = 560 + k * 170
    f = s.fig(x, 0.75, "#8a8f98", 1, False); s.pop(f, ix(261) + k * 0.1, 0.3)
    c = coin(s, x, 960, "$", 34); s.pop(c, ix(262) + 0.2 + k * 0.25, 0.35, 0.4, "50% 50%")
    cue(ix(262) + 0.2 + k * 0.25, "pop_" + str(k + 1), -20)
rp = s.pill(560 + 170, 820, "EVERY CREDITOR REPAID", GOLD, "#111", 28); s.pop(rp, ix(263), 0.4, 0.5, "50% 50%")
nl = s.label(540, 1330, "EVEN THOUGH THE LAW DIDN'T REQUIRE IT", 28, LBL, 0, 700, 0.08); s.fade(nl, ix(268) - 0.1, 0.4, y=10)

# 15  "The 1920s, the whole country is buying stocks, many with borrowed money. He's seen this before."
s = S(ix(274) - 0.1, ix(290) - 0.15)
header(s, "THE 1920s")
rise = s.path("M 90 1000 L 200 960 L 260 975 L 380 900 L 450 915 L 560 820 L 640 835 L 760 720", GOLD, 5); s.draw(rise, ix(280) - 0.2, 1.2)
for k in range(8):
    x = 90 + k * 95
    f = s.fig(x, 0.5, "#8a8f98", 1, False); s.pop(f, ix(277) + k * 0.06, 0.3)
    if k % 2 == 0:
        tg = loan_tag(s, x, 1060); s.pop(tg, ix(284) - 0.1 + k * 0.06, 0.3, 0.4, "50% 50%")
cue(ix(280), "swell_1", -22); cue(ix(284), "pop_2", -20)
bm15 = s.label(420, 1320, "MANY WITH BORROWED MONEY", 30, RED, 0, 800, 0.08); s.fade(bm15, ix(284), 0.35, y=10)
lv15 = hatfig(s, 930, 0.95, GOLD); s.pop(lv15, ix(286) - 0.2, 0.45)
sb = s.label(1040, 900, "SEEN IT BEFORE", 28, GOLD, 0, 800, 0.08, "end"); s.fade(sb, ix(287), 0.35)

# 16  "1929, the market collapses and Jesse Livermore makes a hundred million dollars."
s = S(ix(290) - 0.15, ix(312) - 0.1)
header(s, "1929  ·  THE CRASH", RED)
cl16 = crash_line(s, 120, 680, 560, 440); s.draw(cl16, ix(293) - 0.2, 0.8); cue(ix(293) - 0.2, "whoosh-long_1", -18)
lv16 = hatfig(s, 860, 1.0, GOLD); s.pop(lv16, ix(290), 0.45)
sp16 = s.spot(860, 0, "232,194,106", y0=640); s.fade(sp16, ix(299) - 0.2, 0.5)
m16 = money(s, 540, 1360, "$100,000,000", 96, GOLD, 0)
gb = s.label(540, 1440, "THE GREAT BEAR OF WALL STREET", 30, WHITE, 0, 800, 0.08); s.fade(gb, ix(307) - 0.1, 0.4, y=10)
cue(ix(307) - 0.1, "bell_C5", -20)
tl(f'tl.fromTo("#{m16}", {{opacity: 0, scale: 1.3, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.45, ease: "expo.out", immediateRender: false}}, {ix(299) - 0.15:.3f});')
cue(ix(299) - 0.15, "bell_A4", -16)

# 17  "Then the rules start slipping. He buys back in too early, an expensive divorce. Bigger bets, less patience."
s = S(ix(312) - 0.1, ix(330) - 0.15)
header(s, "AFTER 1929")
bk = s.raw(f'<g id="@ID@"><path d="M 540 700 C 500 680 440 680 400 690 V 840 C 440 830 500 830 540 850 C 580 830 640 830 680 840 V 690 C 640 680 580 680 540 700 Z M 540 700 V 850" '
           f'fill="#11151b" stroke="{GOLD}" stroke-width="4" stroke-linejoin="round"/>'
           + "".join(f'<line x1="{420 if j < 4 else 560}" y1="{725 + (j % 4) * 26}" x2="{520 if j < 4 else 660}" y2="{725 + (j % 4) * 26}" stroke="{GOLD}" stroke-width="3"/>' for j in range(8)) +
           f'<text x="540" y="900" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" letter-spacing="0.2em" fill="{GOLD}">HIS RULES</text></g>', "bk")
tl(f'tl.to("#{bk}", {{opacity: 0.12, duration: 1.6, ease: "power1.in"}}, {ix(315):.3f});')
cue(ix(315), "swell_2", -22)
for k, (txt, w_) in enumerate([("BOUGHT BACK IN TOO EARLY", 318), ("AN EXPENSIVE DIVORCE", 324), ("BIGGER BETS · LESS PATIENCE", 326)]):
    y = 990 + k * 110
    r = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(140, y - 44, 800, 88, 16)}" fill="#160d10" stroke="{RED}" stroke-width="2"/>'
              f'<text x="540" y="{y + 11}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" letter-spacing="0.04em" fill="#fff">{txt}</text></g>', "sl")
    tl(f'tl.fromTo("#{r}", {{opacity: 0, x: -40}}, {{opacity: 1, x: 0, duration: 0.4, ease: "power3.out", immediateRender: false}}, {ix(w_) - 0.2:.3f});')
    cue(ix(w_) - 0.2, "tick-crisp_" + str(k + 1), -18)

# 18  "1934, bankrupt again, over two million dollars in debt and less than 200,000 left."
s = S(ix(330) - 0.15, ix(344) - 0.1)
header(s, "1934")
stamp(s, 540, 690, "BANKRUPT AGAIN", RED, 64, ix(331) - 0.35)
s.raw('<line id="@ID@" x1="200" y1="1180" x2="880" y2="1180" stroke="#ffffff60" stroke-width="3"/>', "ax")
dbar = bar(s, 380, 900, 200, RED, 1180, 0); grow(dbar, ix(333) - 0.1, 0.9)
lbar = bar(s, 700, 1162, 200, "#7d838c", 1180, 0, False); grow(lbar, ix(339) - 0.1, 0.5)
s.label(380, 1230, "DEBT", 30, RED, 1, 800, 0.15); s.label(700, 1230, "LEFT", 30, LBL, 1, 800, 0.15)
dl = s.label(380, 872, "$2,000,000+", 40, RED, 0, 800, 0.03); s.fade(dl, ix(334), 0.35, y=10)
ll = s.label(700, 1132, "< $200,000", 40, LBL, 0, 800, 0.03); s.fade(ll, ix(341) - 0.1, 0.35, y=10)
cue(ix(333) - 0.1, "land_1", -18)

# 19  "In 1940, he wrote his rules down, cut losses fast, never add to a loser. Let the market prove you right. Trust your own plan."
RULES = [("CUT LOSSES FAST · MAX 10%", 358), ("NEVER ADD TO A LOSER", 365), ("LET THE MARKET PROVE YOU RIGHT", 370), ("TRUST YOUR OWN PLAN", 376)]
def rule_rows(s, y0=720, gap=130, op=0):
    rows = []
    for k, (txt, _) in enumerate(RULES):
        y = y0 + k * gap
        size = 34 if len(txt) < 24 else 28
        r = s.raw(f'<g id="@ID@" style="opacity:{op}"><path d="{rrect(90, y - 48, 900, 96, 18)}" fill="#0f1319" stroke="#ffffff30" stroke-width="2"/>'
                  f'<circle cx="150" cy="{y}" r="26" fill="none" stroke="{GOLD}" stroke-width="3"/>'
                  f'<text x="150" y="{y + 11}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" fill="{GOLD}">{k + 1}</text>'
                  f'<text x="200" y="{y + size * 0.36:.0f}" font-family="Montserrat" font-weight="800" font-size="{size}" letter-spacing="0.03em" fill="#fff">{txt}</text></g>', "rr")
        rows.append(r)
    return rows
s = S(ix(344) - 0.1, ix(380) - 0.1)
h19 = s.label(540, 600, "HIS RULES · 1940", 40, GOLD, 0, 800, 0.2); s.fade(h19, ix(344), 0.4, y=10)
tl(f'tl.to("#{h19}", {{opacity: 0, duration: 0.25}}, {ix(352) - 0.3:.3f});')
bt19 = s.label(540, 600, "“HOW TO TRADE IN STOCKS” · 1940", 34, GOLD, 0, 800, 0.06); s.fade(bt19, ix(352) - 0.05, 0.4, y=10)
cue(ix(352) - 0.05, "swell_1", -20)
rr = rule_rows(s)
for k, r in enumerate(rr):
    t = ix(RULES[k][1]) - 0.15
    tl(f'tl.fromTo("#{r}", {{opacity: 0, x: -40}}, {{opacity: 1, x: 0, duration: 0.4, ease: "power3.out", immediateRender: false}}, {t:.3f});')
    cue(t, "pop_" + str(k + 1), -18)
cue(ix(347), "key_3", -22)

# 20  "After 1929, he broke rule number three and everything else followed."
s = S(ix(380) - 0.1, ix(391) - 0.1)
rr2 = rule_rows(s, 760, 120, 1)
a20 = s.label(540, 595, "AFTER 1929", 40, WHITE, 0, 800, 0.2); s.fade(a20, ix(380), 0.4, y=10)
r3 = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(90, 760 + 2 * 120 - 48, 900, 96, 18)}" fill="none" stroke="{RED}" stroke-width="4" style="filter:drop-shadow(0 0 10px {RED})"/>'
           f'<line x1="200" y1="{760 + 2 * 120}" x2="760" y2="{760 + 2 * 120}" stroke="{RED}" stroke-width="5"/></g>', "r3")
s.fade(r3, ix(384) - 0.1, 0.3); cue(ix(384) - 0.1, "tock_1", -16)
tl(f'tl.fromTo("#{rr2[2]}", {{x: -8}}, {{x: 8, duration: 0.06, repeat: 5, yoyo: true, ease: "none", immediateRender: false}}, {ix(384):.3f});')
br3 = s.label(540, 665, "RULE 3 BROKEN", 34, RED, 0, 800, 0.12); s.fade(br3, ix(384), 0.35)
for k, i in enumerate([1, 3, 0]):
    tl(f'tl.to("#{rr2[i]}", {{opacity: 0.2, duration: 0.35}}, {ix(388) + k * 0.25:.3f});')
    cue(ix(388) + k * 0.25, "tick_" + str(k + 1), -22)

# 21  "His rules never failed him. He failed his rules."
s = S(ix(391) - 0.1, ix(400) - 0.25)
rr3 = rule_rows(s, 820, 110, 0.22)
l1 = s.label(540, 620, "HIS RULES NEVER FAILED HIM.", 40, WHITE, 0, 800, 0.04); s.fade(l1, ix(391), 0.4, y=10)
l2 = s.label(540, 710, "HE FAILED HIS RULES.", 48, RED, 0, 800, 0.06); s.fade(l2, ix(396) - 0.1, 0.4, y=10)
cue(ix(396) - 0.1, "tock_1", -16)

# 22  "The best rules in the world mean nothing if you don't follow them every day."
s = S(ix(400) - 0.25, ix(415) - 0.05)
lv22 = hatfig(s, 540, 0.95, GOLD); s.pop(lv22, ix(400) - 0.2, 0.45)
s.spot(540, 1, "232,194,106", y0=640)
for k, d in enumerate(["MON", "TUE", "WED", "THU", "FRI"]):
    x = 180 + k * 180
    s.raw(f'<g id="@ID@"><path d="{rrect(x - 70, 680, 140, 150, 16)}" fill="#0f1319" stroke="#ffffff50" stroke-width="2"/>'
          f'<text x="{x}" y="720" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="28" fill="{LBL}">{d}</text></g>', "dy")
    ck = s.path(f"M {x - 30} 775 L {x - 8} 798 L {x + 32} 748", GOLD, 7, style="filter:drop-shadow(0 0 8px rgba(232,194,106,0.8))")
    s.draw(ck, ix(411) + k * 0.18, 0.3)
    cue(ix(411) + k * 0.18, "tick-crisp_" + str(k % 3 + 1), -20)
ed = s.label(540, 910, "EVERY DAY", 44, GOLD, 0, 800, 0.24); s.fade(ed, ix(413) - 0.1, 0.4, y=10)
br = s.label(540, 600, "THE BEST RULES MEAN NOTHING…", 32, WHITE, 0, 800, 0.08); s.fade(br, ix(400), 0.4)

# 23  outro (handles, no end card)
s = S(ix(415) - 0.05, TOTAL)
es = s.spot(540, 0, "232,194,106", 40, 230); s.fade(es, ix(415), 0.6)
em = s.raw('<image id="@ID@" href="assets/otm_emblem.png" x="390" y="900" width="300" height="291" style="opacity:0;filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>', "i")
s.pop(em, ix(415), 0.7, 0.6, "50% 50%"); cue(ix(415), "bell_A4", -16)
o1 = s.label(540, 1300, "ORDER THE MARKET", 32, GOLD, 0, 800, 0.3); s.fade(o1, ix(415) + 0.3, 0.5)
o2 = s.label(540, 1360, "DON'T LET THE MARKET ORDER YOU", 28, WHITE, 0, 700, 0.12); s.fade(o2, ix(418), 0.4)
o3 = s.pill(540, 1470, "FOLLOW FOR MORE", GOLD, "#111", 30); s.pop(o3, ix(424), 0.4, 0.6, "50% 50%"); cue(ix(424), "click-confirm_1", -16)
hx = 290
soc = s.raw(f'<g id="@ID@" style="opacity:0">'
            f'<rect x="{hx}" y="1548" width="36" height="36" rx="10" fill="none" stroke="#fff" stroke-width="3"/>'
            f'<circle cx="{hx + 18}" cy="1566" r="8.5" fill="none" stroke="#fff" stroke-width="3"/><circle cx="{hx + 28}" cy="1556" r="2.4" fill="#fff"/>'
            f'<text x="{hx + 48}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@fxzuez_28</text>'
            f'<path d="M {hx + 322} 1546 V 1574 A 9 9 0 1 1 {hx + 313} 1565 M {hx + 322} 1546 Q {hx + 326} 1557 {hx + 338} 1558" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>'
            f'<text x="{hx + 348}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@zuez_28</text></g>', "so")
disc = s.label(540, 1650, "EDUCATIONAL ONLY · NOT FINANCIAL ADVICE", 28, GREY, 0, 600, 0.12)
s.fade(soc, ix(418) + 0.6, 0.5, y=12)
s.fade(disc, ix(418) + 0.9, 0.5)


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
