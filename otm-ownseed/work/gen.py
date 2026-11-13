"""OTM "Own the Seed": a glowing-figure video in the OTM style (same scene system as otm-missed) on why the rich keep
getting richer, inspired by a short about patented seeds. A farmer can buy seeds, grow a crop and sell the harvest, but
can be sued for replanting patented seed: the farmer owns the crop, the company owns the recipe, so every season the
farmer pays again. Most people sell the crop (their hours, paid once, then start over); the rich own the seed (shares,
businesses, patents that pay every season). A crop gets eaten, a seed makes more crops. It's not how hard you work, it's
what you own: every month turn part of your harvest into seed. Own the recipe, not just the crop.
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

GLOW = "filter:drop-shadow(0 0 12px rgba(232,194,106,0.75))"

def coin(s, x, y, r=22, op=0):
    return s.raw(f'<g id="@ID@" style="opacity:{op};{GLOW}"><circle cx="{x}" cy="{y}" r="{r}" fill="{GOLD}" stroke="#fff3c4" stroke-width="2"/>'
                 f'<text x="{x}" y="{y + r * 0.4:.0f}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="{r * 1.15:.0f}" fill="#3a2c0a" data-layout-ignore>$</text></g>', "cn")

def seed_svg(x, y, k=1.0, col=GOLD):
    return (f'<g transform="translate({x},{y}) rotate(-25) scale({k})"><ellipse cx="0" cy="0" rx="14" ry="21" fill="{col}"/>'
            f'<path d="M -4 -12 Q -9 0 -4 12" fill="none" stroke="#fff6d8" stroke-width="3" stroke-linecap="round" opacity="0.8"/></g>')

def seed(s, x, y, k=1.0, op=0, col=GOLD):
    return s.raw(f'<g id="@ID@" style="opacity:{op};{GLOW}">{seed_svg(x, y, k, col)}</g>', "sd")

def plant_svg(x, gy, k=1.0, col=WHITE, fruit=False):
    h = 110 * k
    f = (f'<ellipse cx="{x + 22 * k:.0f}" cy="{gy - h * 0.55:.0f}" rx="{11 * k:.0f}" ry="{24 * k:.0f}" fill="{GOLD}" transform="rotate(-18 {x + 22 * k:.0f} {gy - h * 0.55:.0f})"/>'
         if fruit else "")
    return (f'<path d="M {x} {gy} C {x} {gy - h * 0.4:.0f} {x + 6 * k:.0f} {gy - h * 0.7:.0f} {x} {gy - h:.0f}" fill="none" stroke="{col}" stroke-width="{5 * k:.1f}" stroke-linecap="round"/>'
            f'<path d="M {x} {gy - h * 0.45:.0f} Q {x - 46 * k:.0f} {gy - h * 0.62:.0f} {x - 52 * k:.0f} {gy - h * 0.9:.0f} Q {x - 14 * k:.0f} {gy - h * 0.82:.0f} {x} {gy - h * 0.45:.0f} Z" fill="{col}"/>'
            f'<path d="M {x} {gy - h * 0.7:.0f} Q {x + 44 * k:.0f} {gy - h * 0.86:.0f} {x + 48 * k:.0f} {gy - h * 1.12:.0f} Q {x + 12 * k:.0f} {gy - h * 1.02:.0f} {x} {gy - h * 0.7:.0f} Z" fill="{col}"/>{f}')

def plant(s, x, gy, k=1.0, col=WHITE, fruit=False, op=0):
    return s.raw(f'<g id="@ID@" style="opacity:{op};filter:drop-shadow(0 0 10px rgba(255,255,255,0.4))">{plant_svg(x, gy, k, col, fruit)}</g>', "pt")

def crop_svg(x, y, k=1.0):
    return (f'<g transform="translate({x},{y}) rotate(-22) scale({k})"><rect x="-52" y="-18" width="104" height="36" rx="18" fill="#f4f4f2"/>'
            f'<path d="M 52 -2 l 14 -10" stroke="{GOLD}" stroke-width="5" stroke-linecap="round"/>'
            f'<circle cx="-22" cy="-4" r="2.6" fill="#b9bec6"/><circle cx="0" cy="5" r="2.6" fill="#b9bec6"/><circle cx="22" cy="-3" r="2.6" fill="#b9bec6"/></g>')

def doc_svg(x, y, title="PATENT", w=170, h=210):
    lines = "".join(f'<line x1="{x - w / 2 + 22}" y1="{y + 40 + j * 18}" x2="{x + w / 2 - 22 - (j % 2) * 26}" y2="{y + 40 + j * 18}" stroke="#b9ad93" stroke-width="3"/>' for j in range(3))
    return (f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="8" fill="#f3ead8"/>'
            f'<text x="{x}" y="{y - h / 2 + 40}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" letter-spacing="0.08em" fill="#8a2430">{title}</text>'
            f'{seed_svg(x, y - 8, 1.1)}{lines}')

def building_svg(x, base, w=220, h=190, col=WHITE):
    cols = "".join(f'<rect x="{x - w / 2 + 26 + j * (w - 52) / 3 - 9:.0f}" y="{base - h + 62}" width="18" height="{h - 84}" fill="{col}"/>' for j in range(4))
    return (f'<path d="M {x - w / 2 - 6} {base - h + 56} L {x} {base - h} L {x + w / 2 + 6} {base - h + 56} Z" fill="{col}"/>{cols}'
            f'<rect x="{x - w / 2}" y="{base - 22}" width="{w}" height="22" fill="{col}"/>')

# 1  "This is why the rich keep getting richer."
s = S(0, ix(8) - 0.1, first=True)
s.label(540, 490, "WHY THE RICH", 56, WHITE, 1, 800, 0.06)
s.label(540, 570, "KEEP GETTING RICHER", 56, GOLD, 1, 800, 0.05)
s.fig(380, 1.0, WHITE, 1)
s.spot(700, 1, "232,194,106")
s.fig(700, 1.0, GOLD, 1)
for k in range(7):
    c = coin(s, 840, GY - 16 - k * 26, 26)
    tl(f'tl.fromTo("#{c}", {{opacity: 0, y: -60}}, {{opacity: 1, y: 0, duration: 0.3, ease: "power2.in", immediateRender: false}}, {ix(4) + k * 0.16:.3f});')
cue(ix(4), "tick-crisp_1", -22); cue(ix(4) + 0.5, "tick-crisp_2", -22); cue(ix(4) + 0.96, "tick-crisp_3", -20)

# 2  "In America, a farmer can buy seeds, grow a crop, and sell the whole harvest. But if he saves the seeds and plants them again,
#     he can be sued."
s = S(ix(8) - 0.1, ix(37) + 0.1)
fm = s.fig(180, 1.0, WHITE); s.pop(fm, ix(8), 0.4)
toplab(s, "IN AMERICA, A FARMER CAN", "BUY SEEDS", ix(8), ix(15) - 0.15, WHITE, LBL, 58)
bag = s.raw(f'<g id="@ID@" style="opacity:0"><path d="M 268 1240 L 272 1124 Q 278 1100 300 1098 L 344 1098 Q 366 1100 370 1124 L 374 1240 Z" fill="#f3ead8"/>'
            f'<path d="M 292 1098 L 286 1082 L 356 1082 L 350 1098" fill="none" stroke="#f3ead8" stroke-width="5" stroke-linejoin="round"/>'
            f'<text x="321" y="1186" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" fill="#5b4a2a">SEED</text></g>', "bg")
s.pop(bag, ix(13) - 0.1, 0.35, 0.5); cue(ix(13) - 0.1, "pop_1", -20)
P2 = [500, 640, 780, 920]
pl = [plant(s, x, GY, 1.3, WHITE, fruit=True) for x in P2]
for k, p in enumerate(pl):
    s.pop(p, ix(15) - 0.1 + k * 0.12, 0.5, 0.05, "50% 100%")
cue(ix(15) - 0.1, "swell_1", -22)
toplab(s, "GROW A CROP, AND SELL", "THE WHOLE HARVEST", ix(15) - 0.15, ix(23) - 0.1, GOLD, LBL, 54)
sold = s.pill(710, 1000, "SOLD", GOLD, "#111", 32); s.pop(sold, ix(21) - 0.1, 0.4, 0.6, "50% 50%"); cue(ix(21) - 0.1, "bell_C5", -20)
for i_ in pl:
    hide(i_, ix(23) + 0.1, 0.4, 0.15)
hide(sold, ix(23) + 0.1, 0.4)
toplab(s, "BUT IF HE SAVES THE SEEDS", "AND PLANTS THEM AGAIN", ix(23), ix(33) - 0.2, WHITE, LBL, 50)
sds = []
for k, x in enumerate(P2):
    sd = seed(s, 240, 1150, 0.8)
    s.pop(sd, ix(26) + k * 0.08, 0.3, 0.3, "50% 50%")
    tl(f'tl.to("#{sd}", {{x: {x - 240}, y: 70, duration: 0.6, ease: "power2.in"}}, {ix(30) - 0.1 + k * 0.1:.3f});')
    hide(sd, ix(31) + k * 0.1, 0.2)
    sp = plant(s, x, GY, 0.55, GOLD)
    s.pop(sp, ix(31) + 0.05 + k * 0.1, 0.4, 0.05, "50% 100%")
cue(ix(26), "tick_1", -22); cue(ix(30), "whoosh-short_1", -24); cue(ix(31) + 0.1, "pop_2", -22)
toplab(s, "", "HE CAN BE SUED", ix(33) - 0.2, ix(37) + 0.1, RED, LBL, 62)
gv = s.uid("gv")
s.raw(f'<g transform="translate(900,900)"><g id="{gv}" style="opacity:0;filter:drop-shadow(0 0 12px rgba(255,77,94,0.6))">'
      f'<rect x="-150" y="-8" width="150" height="16" rx="8" fill="#f4f4f2"/><rect x="-196" y="-42" width="56" height="84" rx="10" fill="#f4f4f2"/>'
      f'<rect x="-205" y="-30" width="74" height="10" fill="{RED}"/><rect x="-205" y="20" width="74" height="10" fill="{RED}"/></g></g>', "x")
pad = s.raw(f'<rect id="@ID@" x="672" y="946" width="120" height="20" rx="6" fill="#f4f4f2" style="opacity:0"/>', "pd")
s.fade(pad, ix(33), 0.3); s.fade(gv, ix(33), 0.3)
tl(f'tl.fromTo("#{gv}", {{rotation: -40, svgOrigin: "0 0"}}, {{rotation: 0, svgOrigin: "0 0", duration: 0.22, ease: "power3.in", immediateRender: false}}, {ix(36) - 0.22:.3f});')
fl = s.raw(f'<circle id="@ID@" cx="732" cy="950" r="30" fill="none" stroke="{RED}" stroke-width="5" style="opacity:0"/>', "fl")
tl(f'tl.fromTo("#{fl}", {{opacity: 1, scale: 0.4, transformOrigin: "50% 50%"}}, {{opacity: 0, scale: 2.4, duration: 0.5, ease: "power2.out", immediateRender: false}}, {ix(36):.3f});')
cue(ix(36), "tock_1", -12)

# 3  "Because the company that made the seed owns the patent. The farmer owns the crop. The company owns the recipe.
#     So every season, the farmer comes back and pays again."
o3, c3 = ix(37) - 0.1, ix(67) - 0.1
s = S(o3, c3, ground=False, restore=False)
toplab(s, "BECAUSE THE COMPANY THAT MADE THE SEED", "OWNS THE PATENT", ix(37), ix(47) - 0.1, GOLD, LBL, 56)
bd = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 12px rgba(255,255,255,0.4))">{building_svg(780, 950)}</g>', "bd")
s.pop(bd, ix(39) - 0.1, 0.45, 0.6); cue(ix(39) - 0.1, "land-light_1", -20)
cl3 = s.label(780, 995, "COMPANY", 28, LBL, 0, 800, 0.18); s.fade(cl3, ix(39), 0.3)
pd = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 16px rgba(232,194,106,0.5))">{doc_svg(780, 1160)}</g>', "pd")
s.pop(pd, ix(46) - 0.1, 0.45, 0.5, "50% 50%"); cue(ix(46) - 0.1, "pop_3", -20)
fm3 = s.fig(300, 1.0, WHITE, gy=950); s.pop(fm3, ix(47) - 0.1, 0.4)
fl3 = s.label(300, 995, "FARMER", 28, LBL, 0, 800, 0.18); s.fade(fl3, ix(47), 0.3)
bk = s.raw(f'<g id="@ID@" style="opacity:0">'
           f'<path d="M 205 1150 L 395 1150 L 375 1250 L 225 1250 Z" fill="none" stroke="#f4f4f2" stroke-width="5" stroke-linejoin="round"/>'
           f'{crop_svg(255, 1128, 0.75)}{crop_svg(310, 1118, 0.75)}{crop_svg(355, 1132, 0.7)}</g>', "bk")
s.pop(bk, ix(50) - 0.1, 0.4, 0.5); cue(ix(50) - 0.1, "pop_1", -22)
ol3 = s.label(300, 1320, "OWNS THE CROP", 30, WHITE, 0, 800, 0.08); s.fade(ol3, ix(50), 0.3)
or3 = s.label(780, 1320, "OWNS THE RECIPE", 30, GOLD, 0, 800, 0.08); s.fade(or3, ix(55), 0.3)
toplab(s, "", "THE FARMER OWNS THE CROP", ix(47), ix(52) - 0.1, WHITE, LBL, 46)
toplab(s, "", "THE COMPANY OWNS THE RECIPE", ix(52), ix(57) - 0.1, GOLD, LBL, 46)
tl(f'tl.fromTo("#{pd}", {{scale: 1}}, {{scale: 1.08, transformOrigin: "50% 50%", duration: 0.35, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false}}, {ix(56) - 0.1:.3f});')
cue(ix(56) - 0.1, "bell_G5", -22)
toplab(s, "SO EVERY SEASON", "THE FARMER PAYS AGAIN", ix(57), c3, RED, LBL, 50)
for k in range(3):
    t = ix(58) + k * 0.95
    cn = coin(s, 370, 830, 22)
    tl(f'tl.set("#{cn}", {{opacity: 1}}, {t:.3f});')
    tl(f'tl.to("#{cn}", {{x: 330, duration: 0.8, ease: "power1.inOut"}}, {t:.3f});')
    tl(f'tl.to("#{cn}", {{y: -90, duration: 0.4, ease: "sine.out", yoyo: true, repeat: 1}}, {t:.3f});')
    hide(cn, t + 0.75, 0.12)
    sl = s.label(540, 1030, f"SEASON {k + 1}", 30, RED, 0, 800, 0.15)
    s.fade(sl, t, 0.2)
    if k < 2: hide(sl, t + 0.85, 0.12)
    cue(t + 0.78, "tick_" + str(k + 1), -18)

# 4  "That's the whole game."
s = S(ix(67) - 0.1, ix(71) - 0.1, ground=False, hide=False)
g4 = s.label(540, 930, "THAT'S THE WHOLE GAME", 56, WHITE, 0, 800, 0.04)
tl(f'tl.fromTo("#{g4}", {{opacity: 0, scale: 1.25, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.45, ease: "expo.out", immediateRender: false}}, {ix(67) - 0.05:.3f});')
cue(ix(67) - 0.05, "whoosh-short_2", -22)

# 5  "Most people sell the crop. Their hours, their effort. They get paid once, then start over."
s = S(ix(71) - 0.1, ix(87) + 0.15)
w5 = s.fig(540, 1.0, WHITE); s.pop(w5, ix(71) - 0.05, 0.4)
toplab(s, "MOST PEOPLE", "SELL THE CROP", ix(71), ix(80) - 0.1, WHITE, LBL, 58)
ck = s.raw(f'<g id="@ID@" style="opacity:0"><circle cx="270" cy="880" r="62" fill="none" stroke="#f4f4f2" stroke-width="6"/>'
           f'<path d="M 270 880 L 270 840 M 270 880 L 300 896" stroke="#f4f4f2" stroke-width="6" stroke-linecap="round"/></g>', "ck")
s.pop(ck, ix(77) - 0.1, 0.4, 0.5, "50% 50%")
cl5 = s.label(270, 990, "HOURS", 30, LBL, 0, 800, 0.15); s.fade(cl5, ix(77), 0.3)
bo = s.raw(f'<path id="@ID@" d="M 822 812 L 776 886 L 806 886 L 790 948 L 842 866 L 810 866 Z" fill="#f4f4f2" style="opacity:0"/>', "bo")
s.pop(bo, ix(79) - 0.1, 0.4, 0.5, "50% 50%")
el5 = s.label(810, 990, "EFFORT", 30, LBL, 0, 800, 0.15); s.fade(el5, ix(79), 0.3)
cue(ix(77) - 0.1, "pop_1", -22); cue(ix(79) - 0.1, "pop_2", -22)
toplab(s, "THEY GET", "PAID ONCE", ix(80), ix(84) - 0.1, GOLD, LBL, 58)
s.raw(f'<rect x="290" y="1310" width="500" height="34" rx="17" fill="none" stroke="#ffffff40" stroke-width="2.5"/>', "bf")
bar = s.raw(f'<rect id="@ID@" x="290" y="1310" width="0" height="34" rx="17" fill="{GOLD}"/>', "br")
tl(f'tl.fromTo("#{bar}", {{attr: {{width: 0}}}}, {{attr: {{width: 500}}, duration: 0.7, ease: "power2.out", immediateRender: false}}, {ix(81) - 0.1:.3f});')
pl5 = s.label(540, 1400, "+ ONE PAYCHECK", 30, GOLD, 0, 800, 0.1); s.fade(pl5, ix(82), 0.3)
cue(ix(81) - 0.1, "swell_1", -22)
toplab(s, "THEN", "START OVER", ix(84), ix(87) + 0.15, RED, LBL, 60)
tl(f'tl.to("#{bar}", {{attr: {{width: 0}}, duration: 0.6, ease: "power2.in"}}, {ix(85) - 0.1:.3f});')
hide(pl5, ix(85) - 0.1, 0.3)
z5 = s.label(540, 1400, "BACK TO ZERO", 30, RED, 0, 800, 0.1); s.fade(z5, ix(85) + 0.1, 0.3)
cue(ix(85) - 0.1, "whoosh-short_3", -22)

# 6  "The rich own the seed. Shares, businesses, patents. Things that pay them again and again every season."
s = S(ix(87) - 0.1, ix(104) - 0.1)
sp6 = s.spot(540, 0, "232,194,106"); s.fade(sp6, ix(87), 0.5)
r6 = s.fig(540, 1.0, GOLD); s.pop(r6, ix(87), 0.45)
toplab(s, "THE RICH", "OWN THE SEED", ix(87), ix(95) - 0.1, GOLD, LBL, 60)
bs = seed(s, 540, 1000, 2.0); s.pop(bs, ix(91) - 0.1, 0.45, 0.2, "50% 50%"); cue(ix(91) - 0.1, "bell_E5", -18)
hide(bs, ix(92) - 0.1, 0.3)
TILES = [("SHARES", 220, 92), ("BUSINESSES", 540, 93), ("PATENTS", 860, 94)]
ICON = {
    "SHARES": f'<path d="M -50 22 L -18 -6 L 6 8 L 48 -30" fill="none" stroke="{GOLD}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
              f'<path d="M 30 -32 L 50 -32 L 50 -12" fill="none" stroke="{GOLD}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>',
    "BUSINESSES": f'<path d="M -52 -10 L -44 -36 L 44 -36 L 52 -10 Z" fill="{GOLD}"/><rect x="-44" y="-10" width="88" height="44" fill="none" stroke="{GOLD}" stroke-width="6"/>'
                  f'<rect x="-12" y="6" width="24" height="28" fill="{GOLD}"/>',
    "PATENTS": f'<rect x="-34" y="-40" width="68" height="80" rx="6" fill="none" stroke="{GOLD}" stroke-width="6"/>{seed_svg(0, -2, 0.9)}',
}
tiles = []
for name, x, w_ in TILES:
    t_ = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(x - 140, 700, 280, 200, 20)}" fill="#0f1319" stroke="{GOLD}" stroke-opacity="0.55" stroke-width="2.5"/>'
               f'<g transform="translate({x},776)">{ICON[name]}</g>'
               f'<text x="{x}" y="872" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" letter-spacing="0.06em" fill="#fff">{name}</text></g>', "tl")
    s.pop(t_, ix(w_) - 0.1, 0.4, 0.6, "50% 50%"); cue(ix(w_) - 0.1, "pop_" + str(len(tiles) + 1), -20); tiles.append(t_)
toplab(s, "THINGS THAT PAY THEM", "AGAIN AND AGAIN", ix(95), ix(104) - 0.1, GOLD, LBL, 56)
for wv, t in enumerate([ix(97), ix(99) + 0.1, ix(102)]):
    for j, (_, x, _w) in enumerate(TILES):
        cn = coin(s, x, 930, 22)
        tl(f'tl.fromTo("#{cn}", {{opacity: 0, y: -20}}, {{opacity: 1, y: 0, duration: 0.2, immediateRender: false}}, {t + j * 0.07:.3f});')
        tl(f'tl.to("#{cn}", {{x: {(540 - x) * 0.55 + (j - 1) * 30:.0f}, y: 150, duration: 0.55, ease: "power2.in"}}, {t + j * 0.07 + 0.2:.3f});')
        hide(cn, t + j * 0.07 + 0.7, 0.15)
    cue(t + 0.7, "tick-crisp_" + str(wv + 1), -18)

# 7  "A crop gets eaten. A seed makes more crops."
s = S(ix(104) - 0.1, ix(113) - 0.1, ground=False)
toplab(s, "", "A CROP GETS EATEN", ix(104), ix(108) - 0.1, WHITE, LBL, 56)
bites = s.uid("bi")
cr = s.raw(f'<g id="@ID@" style="opacity:0">{crop_svg(270, 1000, 2.4)}<g id="{bites}" style="opacity:0"><circle cx="398" cy="948" r="46" fill="#06070a"/><circle cx="368" cy="990" r="38" fill="#06070a"/></g></g>', "cr")
s.pop(cr, ix(104), 0.4, 0.5, "50% 50%")
s.fade(bites, ix(106), 0.12); cue(ix(106), "click_1", -18)
tl(f'tl.to("#{cr}", {{opacity: 0, scale: 0.6, transformOrigin: "50% 50%", duration: 0.5, ease: "power2.in"}}, {ix(107) + 0.1:.3f});')
z7 = s.label(270, 1180, "GONE", 34, RED, 0, 800, 0.15); s.fade(z7, ix(107) + 0.3, 0.3)
toplab(s, "", "A SEED MAKES MORE CROPS", ix(108), ix(113) - 0.1, GOLD, LBL, 50)
s0 = seed(s, 780, 1180, 1.3); s.pop(s0, ix(108), 0.35, 0.3, "50% 50%")
l1 = s.label(780, 1250, "1 SEED", 28, LBL, 0, 800, 0.12); s.fade(l1, ix(108) + 0.1, 0.3)
br = s.path("M 780 1160 L 780 1060 M 780 1110 L 670 1060 M 780 1110 L 890 1060", "#f4f4f2", 4); s.draw(br, ix(110) - 0.1, 0.4)
for j, x in enumerate([670, 780, 890]):
    p = plant(s, x, 1060, 0.8, WHITE, fruit=True); s.pop(p, ix(110) + 0.15 + j * 0.08, 0.4, 0.05, "50% 100%")
    for q, dx in enumerate([-30, 0, 30]):
        sd = seed(s, x + dx, 930 - (q % 2) * 18, 0.55); s.pop(sd, ix(111) + 0.1 + j * 0.1 + q * 0.05, 0.3, 0.2, "50% 50%")
l9 = s.label(780, 880, "MORE SEEDS", 28, GOLD, 0, 800, 0.12); s.fade(l9, ix(112) - 0.1, 0.3)
cue(ix(110), "swell_2", -20); cue(ix(111) + 0.1, "pop_3", -22)

# 8  "So the real question isn't how hard you work. It's what you own."
s = S(ix(113) - 0.1, ix(126) - 0.1)
toplab(s, "THE REAL QUESTION ISN'T", "HOW HARD YOU WORK", ix(113), ix(122) - 0.1, WHITE, LBL, 54)
w8 = s.fig(540, 1.0, WHITE); s.pop(w8, ix(113) - 0.05, 0.4)
tl(f'tl.fromTo("#{w8}", {{y: 0}}, {{y: -16, duration: 0.18, yoyo: true, repeat: 15, ease: "sine.inOut", immediateRender: false}}, {ix(116):.3f});')
st8 = s.path("M 200 545 H 880", RED, 6); s.draw(st8, ix(121) - 0.2, 0.35); cue(ix(121) - 0.2, "tock_1", -18)
hide(w8, ix(122) - 0.05, 0.3)
hide(st8, ix(122) - 0.2, 0.15)
sp8 = s.spot(540, 0, "232,194,106"); s.fade(sp8, ix(122), 0.5)
g8 = s.fig(540, 1.0, GOLD); s.pop(g8, ix(122), 0.45)
toplab(s, "IT'S", "WHAT YOU OWN", ix(122), ix(126) - 0.1, GOLD, LBL, 62)
for j, (x, y) in enumerate([(380, 960), (700, 940), (560, 860)]):
    sd = seed(s, x, y, 1.0); s.pop(sd, ix(124) + j * 0.12, 0.35, 0.2, "50% 50%")
cue(ix(122), "bell_C5", -18)

# 9  "Every month, take part of your harvest and turn it into seed."
s = S(ix(126) - 0.1, ix(138) - 0.1, ground=False)
toplab(s, "EVERY MONTH, TAKE", "PART OF YOUR HARVEST", ix(126), ix(133) - 0.1, WHITE, LBL, 52)
hv = s.label(540, 720, "THIS MONTH'S HARVEST", 28, LBL, 0, 800, 0.15); s.fade(hv, ix(126), 0.3)
items = []
for k in range(10):
    x = 180 + k * 80
    it = s.raw(f'<g id="@ID@" style="opacity:0">{crop_svg(x, 800, 0.55)}</g>', "it")
    s.pop(it, ix(126) + 0.05 + k * 0.05, 0.3, 0.5, "50% 50%"); items.append((x, it))
cue(ix(126), "pop_1", -22)
jar = s.raw(f'<g id="@ID@" style="opacity:0"><path d="M 450 1010 L 450 1210 Q 450 1240 480 1240 L 600 1240 Q 630 1240 630 1210 L 630 1010" fill="none" stroke="{GOLD}" stroke-width="5" stroke-linejoin="round"/>'
            f'<rect x="436" y="994" width="208" height="18" rx="6" fill="{GOLD}"/>'
            f'<text x="540" y="1300" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" letter-spacing="0.2em" fill="{GOLD}">SEED</text></g>', "jr")
s.pop(jar, ix(128) - 0.1, 0.4, 0.6, "50% 50%")
for j, (x, it) in enumerate(items[-2:]):
    tl(f'tl.to("#{it}", {{x: {520 + j * 40 - x}, y: 350, scale: 0.7, transformOrigin: "50% 50%", duration: 0.7, ease: "power2.inOut"}}, {ix(129) + j * 0.15:.3f});')
    hide(it, ix(134) - 0.1, 0.3)
    sd = seed(s, 520 + j * 40, 1170 - j * 10, 1.0); s.pop(sd, ix(134) - 0.05 + j * 0.1, 0.35, 0.2, "50% 50%")
cue(ix(129), "whoosh-short_1", -22)
toplab(s, "AND TURN IT", "INTO SEED", ix(133), ix(138) - 0.1, GOLD, LBL, 62)
sprout = plant(s, 540, 1000, 0.9, GOLD); s.pop(sprout, ix(136), 0.5, 0.05, "50% 100%")
cue(ix(134) - 0.05, "bell_E5", -20); cue(ix(136), "swell_1", -22)

# 10  "Own the recipe. Not just the crop."
s = S(ix(138) - 0.1, ix(145) + 0.35)
s.spot(540, 1, "232,194,106")
g10 = s.fig(540, 1.0, GOLD); s.pop(g10, ix(138) - 0.1, 0.4)
t10 = s.label(540, 620, "OWN THE RECIPE", 64, GOLD, 0, 800, 0.06)
tl(f'tl.fromTo("#{t10}", {{opacity: 0, scale: 1.3, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.45, ease: "expo.out", immediateRender: false}}, {ix(138) - 0.05:.3f});')
n10 = s.label(540, 715, "NOT JUST THE CROP", 40, "#9aa0a8", 0, 800, 0.08); s.fade(n10, ix(141) - 0.1, 0.35, y=10)
s10 = seed(s, 540, 960, 1.6); s.pop(s10, ix(139), 0.45, 0.2, "50% 50%")
cue(ix(138), "bell_G5", -16)

# 11  outro (handles, no end card)
s = S(ix(145) + 0.3, TOTAL)
es = s.spot(540, 0, "232,194,106", 40, 230); s.fade(es, ix(145) + 0.35, 0.6)
em = s.raw('<image id="@ID@" href="assets/otm_emblem.png" x="390" y="900" width="300" height="291" style="opacity:0;filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>', "i")
s.pop(em, ix(145) + 0.35, 0.7, 0.6, "50% 50%"); cue(ix(145) + 0.35, "bell_A4", -16)
o1l = s.label(540, 1300, "ORDER THE MARKET", 32, GOLD, 0, 800, 0.3); s.fade(o1l, ix(145) + 0.55, 0.5)
o2 = s.label(540, 1360, "DON'T LET THE MARKET ORDER YOU", 28, WHITE, 0, 700, 0.12); s.fade(o2, ix(148), 0.4)
o3 = s.pill(540, 1470, "FOLLOW FOR MORE", GOLD, "#111", 30); s.pop(o3, ix(154), 0.4, 0.6, "50% 50%"); cue(ix(154), "click-confirm_1", -16)
hx = 290
soc = s.raw(f'<g id="@ID@" style="opacity:0">'
            f'<rect x="{hx}" y="1548" width="36" height="36" rx="10" fill="none" stroke="#fff" stroke-width="3"/>'
            f'<circle cx="{hx + 18}" cy="1566" r="8.5" fill="none" stroke="#fff" stroke-width="3"/><circle cx="{hx + 28}" cy="1556" r="2.4" fill="#fff"/>'
            f'<text x="{hx + 48}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@fxzuez_28</text>'
            f'<path d="M {hx + 322} 1546 V 1574 A 9 9 0 1 1 {hx + 313} 1565 M {hx + 322} 1546 Q {hx + 326} 1557 {hx + 338} 1558" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>'
            f'<text x="{hx + 348}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@zuez_28</text></g>', "so")
disc = s.label(540, 1650, "EDUCATIONAL ONLY · NOT FINANCIAL ADVICE", 28, GREY, 0, 600, 0.12)
s.fade(soc, ix(148) + 0.6, 0.5, y=12)
s.fade(disc, ix(148) + 0.9, 0.5)
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
    <div id="root" data-composition-id="otm-ownseed" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
{TIMELINE}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-ownseed-audio" class="clip" src="assets/audio/mix_ownseed.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-ownseed"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
