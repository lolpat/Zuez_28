"""OTM "Own the Seed" (Thai version): the Thai-language edition of otm-ownseed, a glowing-figure video in the OTM style on
why the rich keep getting richer. A farmer can be sued for replanting patented seed: the farmer owns the crop, the
company owns the recipe, so every season the farmer pays again. Most people sell the crop (their hours, paid once); the
rich own the seed (shares, businesses, patents that pay every season). Turn part of every harvest into seed.
Thai narration (ElevenLabs "Patinya", calm Thai narrator), Thai on-screen text in Kanit (OFL, assets/fonts); the outro
keeps the brand lines in English. Original script, voice only, no music.
Scenes key off token indices of work/words.json (the script's tokens, aligned to the voice; helper ix).
Writes ../index.html, work/cues.json and work/timing.json."""
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

FONTS = "".join(
    f"@font-face {{ font-family: 'Kanit'; font-style: normal; font-weight: {w}; font-display: block; "
    f"src: url('assets/fonts/kanit-{sub}-{w}-normal.woff2') format('woff2'); unicode-range: {rng}; }}\n"
    for w in (600, 700, 800)
    for sub, rng in (("thai", "U+02D7, U+0303, U+0331, U+0E01-0E5B, U+200C-200D, U+25CC"),
                     ("latin", "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, "
                               "U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD")))

def thai(s):
    """Switch the item just added to Kanit with no letter-spacing (spacing pulls Thai marks off their letters)."""
    s.items[-1] = (s.items[-1].replace('font-family="Montserrat"', 'font-family="Kanit"')
                   .replace('font-weight="800"', 'font-weight="700"'))
    s.items[-1] = _re.sub(r'letter-spacing="[^"]*"', 'letter-spacing="0"', s.items[-1])

def thl(s, x, y, text, size=30, col=LBL, op=0, weight=700, anchor="middle"):
    i = s.label(x, y, text, size, col, op, weight, 0, anchor); thai(s)
    return i

def toplab(s, small, big, t0, t1, bcol=WHITE, scol=LBL, bsize=52, y=560):
    ids = []
    if small:
        a = thl(s, 540, y - 72, small, 32, scol, 0, 600); ids.append(a)
    b = thl(s, 540, y, big, bsize, bcol, 0, 700); ids.append(b)
    for i in ids:
        s.fade(i, t0, 0.3, y=10)
        tl(f'tl.to("#{i}", {{opacity: 0, duration: 0.15}}, {t1 - 0.17:.3f});')
    return ids

def hide(i, t, d=0.3, to=0):
    tl(f'tl.to("#{i}", {{opacity: {to}, duration: {d}}}, {t:.3f});')

GLOW = "filter:drop-shadow(0 0 12px rgba(232,194,106,0.75))"
TH = 'font-family="Kanit" font-weight="700"'

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

def doc_svg(x, y, title="สิทธิบัตร", w=170, h=210):
    lines = "".join(f'<line x1="{x - w / 2 + 22}" y1="{y + 40 + j * 18}" x2="{x + w / 2 - 22 - (j % 2) * 26}" y2="{y + 40 + j * 18}" stroke="#b9ad93" stroke-width="3"/>' for j in range(3))
    return (f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="8" fill="#f3ead8"/>'
            f'<text x="{x}" y="{y - h / 2 + 42}" text-anchor="middle" {TH} font-size="30" fill="#8a2430">{title}</text>'
            f'{seed_svg(x, y - 8, 1.1)}{lines}')

def building_svg(x, base, w=220, h=190, col=WHITE):
    cols = "".join(f'<rect x="{x - w / 2 + 26 + j * (w - 52) / 3 - 9:.0f}" y="{base - h + 62}" width="18" height="{h - 84}" fill="{col}"/>' for j in range(4))
    return (f'<path d="M {x - w / 2 - 6} {base - h + 56} L {x} {base - h} L {x + w / 2 + 6} {base - h + 56} Z" fill="{col}"/>{cols}'
            f'<rect x="{x - w / 2}" y="{base - 22}" width="{w}" height="22" fill="{col}"/>')

# 1  "นี่คือเหตุผล ที่คนรวย... ยิ่งรวยขึ้นเรื่อยๆ"
s = S(0, ix(3) - 0.1, first=True)
thl(s, 540, 486, "ทำไมคนรวย", 64, WHITE, 1, 700)
thl(s, 540, 572, "ถึงรวยขึ้นเรื่อยๆ", 64, GOLD, 1, 700)
s.fig(380, 1.0, WHITE, 1)
s.spot(700, 1, "232,194,106")
s.fig(700, 1.0, GOLD, 1)
for k in range(7):
    c = coin(s, 840, GY - 16 - k * 26, 26)
    tl(f'tl.fromTo("#{c}", {{opacity: 0, y: -60}}, {{opacity: 1, y: 0, duration: 0.3, ease: "power2.in", immediateRender: false}}, {ix(1) + k * 0.2:.3f});')
cue(ix(1), "tick-crisp_1", -22); cue(ix(1) + 0.6, "tick-crisp_2", -22); cue(ix(1) + 1.2, "tick-crisp_3", -20)

# 2  "ที่อเมริกา เกษตรกรซื้อเมล็ดพันธุ์มาปลูก แล้วขายผลผลิตได้ทั้งหมด / แต่ถ้าเขาเก็บเมล็ดไว้... แล้วเอามาปลูกซ้ำ เขาอาจโดนฟ้องได้"
s = S(ix(3) - 0.1, ix(9) + 0.1)
fm = s.fig(180, 1.0, WHITE); s.pop(fm, ix(3), 0.4)
toplab(s, "ที่อเมริกา เกษตรกร", "ซื้อเมล็ดพันธุ์มาปลูก", ix(3), ix(5) - 0.15, WHITE, LBL, 58)
bag = s.raw(f'<g id="@ID@" style="opacity:0"><path d="M 268 1240 L 272 1124 Q 278 1100 300 1098 L 344 1098 Q 366 1100 370 1124 L 374 1240 Z" fill="#f3ead8"/>'
            f'<path d="M 292 1098 L 286 1082 L 356 1082 L 350 1098" fill="none" stroke="#f3ead8" stroke-width="5" stroke-linejoin="round"/>'
            f'<text x="321" y="1186" text-anchor="middle" {TH} font-size="30" fill="#5b4a2a">เมล็ด</text></g>', "bg")
s.pop(bag, ix(4) + 0.5, 0.35, 0.5); cue(ix(4) + 0.5, "pop_1", -20)
P2 = [500, 640, 780, 920]
pl = [plant(s, x, GY, 1.3, WHITE, fruit=True) for x in P2]
for k, p in enumerate(pl):
    s.pop(p, ix(5) - 0.9 + k * 0.12, 0.5, 0.05, "50% 100%")
cue(ix(5) - 0.9, "swell_1", -22)
toplab(s, "แล้วขายผลผลิต", "ได้ทั้งหมด", ix(5) - 0.15, ix(6) - 0.1, GOLD, LBL, 60)
sold = s.pill(710, 1000, "ขายหมด", GOLD, "#111", 32); thai(s); s.pop(sold, ix(5) + 0.7, 0.4, 0.6, "50% 50%"); cue(ix(5) + 0.7, "bell_C5", -20)
for i_ in pl:
    hide(i_, ix(6) + 0.1, 0.4, 0.15)
hide(sold, ix(6) + 0.1, 0.4)
toplab(s, "แต่ถ้าเขาเก็บเมล็ดไว้", "แล้วเอามาปลูกซ้ำ", ix(6), ix(8) - 0.2, WHITE, LBL, 58)
for k, x in enumerate(P2):
    sd = seed(s, 240, 1150, 0.8)
    s.pop(sd, ix(6) + 0.6 + k * 0.08, 0.3, 0.3, "50% 50%")
    tl(f'tl.to("#{sd}", {{x: {x - 240}, y: 70, duration: 0.6, ease: "power2.in"}}, {ix(7) + k * 0.1:.3f});')
    hide(sd, ix(7) + 0.6 + k * 0.1, 0.2)
    sp = plant(s, x, GY, 0.55, GOLD)
    s.pop(sp, ix(7) + 0.65 + k * 0.1, 0.4, 0.05, "50% 100%")
cue(ix(6) + 0.6, "tick_1", -22); cue(ix(7), "whoosh-short_1", -24); cue(ix(7) + 0.7, "pop_2", -22)
toplab(s, "", "เขาอาจโดนฟ้องได้", ix(8) - 0.2, ix(9) + 0.1, RED, LBL, 64)
gv = s.uid("gv")
s.raw(f'<g transform="translate(900,900)"><g id="{gv}" style="opacity:0;filter:drop-shadow(0 0 12px rgba(255,77,94,0.6))">'
      f'<rect x="-150" y="-8" width="150" height="16" rx="8" fill="#f4f4f2"/><rect x="-196" y="-42" width="56" height="84" rx="10" fill="#f4f4f2"/>'
      f'<rect x="-205" y="-30" width="74" height="10" fill="{RED}"/><rect x="-205" y="20" width="74" height="10" fill="{RED}"/></g></g>', "x")
pad = s.raw(f'<rect id="@ID@" x="672" y="946" width="120" height="20" rx="6" fill="#f4f4f2" style="opacity:0"/>', "pd")
s.fade(pad, ix(8) - 0.2, 0.3); s.fade(gv, ix(8) - 0.2, 0.3)
T_SUE = ix(8) + 0.8
tl(f'tl.fromTo("#{gv}", {{rotation: -40, svgOrigin: "0 0"}}, {{rotation: 0, svgOrigin: "0 0", duration: 0.22, ease: "power3.in", immediateRender: false}}, {T_SUE - 0.22:.3f});')
fl = s.raw(f'<circle id="@ID@" cx="732" cy="950" r="30" fill="none" stroke="{RED}" stroke-width="5" style="opacity:0"/>', "fl")
tl(f'tl.fromTo("#{fl}", {{opacity: 1, scale: 0.4, transformOrigin: "50% 50%"}}, {{opacity: 0, scale: 2.4, duration: 0.5, ease: "power2.out", immediateRender: false}}, {T_SUE:.3f});')
cue(T_SUE, "tock_1", -12)

# 3  "เพราะบริษัทที่สร้างเมล็ดพันธุ์นั้น ถือสิทธิบัตรไว้ / เกษตรกรเป็นเจ้าของผลผลิต แต่บริษัทเป็นเจ้าของสูตร / ทุกฤดูกาล เกษตรกรจึงต้องกลับมา... จ่ายใหม่"
o3, c3 = ix(9) - 0.1, ix(16) - 0.1
s = S(o3, c3, ground=False, restore=False)
toplab(s, "เพราะบริษัทที่สร้างเมล็ดพันธุ์นั้น", "ถือสิทธิบัตรไว้", ix(9), ix(11) - 0.1, GOLD, LBL, 60)
bd = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 12px rgba(255,255,255,0.4))">{building_svg(780, 950)}</g>', "bd")
s.pop(bd, ix(9) + 0.3, 0.45, 0.6); cue(ix(9) + 0.3, "land-light_1", -20)
cl3 = thl(s, 780, 1000, "บริษัท", 30, LBL, 0, 600); s.fade(cl3, ix(9) + 0.4, 0.3)
pd = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 16px rgba(232,194,106,0.5))">{doc_svg(780, 1160)}</g>', "pd")
s.pop(pd, ix(10) + 0.2, 0.45, 0.5, "50% 50%"); cue(ix(10) + 0.2, "pop_3", -20)
fm3 = s.fig(300, 1.0, WHITE, gy=950); s.pop(fm3, ix(11) - 0.1, 0.4)
fl3 = thl(s, 300, 1000, "เกษตรกร", 30, LBL, 0, 600); s.fade(fl3, ix(11), 0.3)
bk = s.raw(f'<g id="@ID@" style="opacity:0">'
           f'<path d="M 205 1150 L 395 1150 L 375 1250 L 225 1250 Z" fill="none" stroke="#f4f4f2" stroke-width="5" stroke-linejoin="round"/>'
           f'{crop_svg(255, 1128, 0.75)}{crop_svg(310, 1118, 0.75)}{crop_svg(355, 1132, 0.7)}</g>', "bk")
s.pop(bk, ix(11) + 0.8, 0.4, 0.5); cue(ix(11) + 0.8, "pop_1", -22)
ol3 = thl(s, 300, 1325, "เจ้าของผลผลิต", 34, WHITE, 0, 700); s.fade(ol3, ix(11) + 0.9, 0.3)
or3 = thl(s, 780, 1325, "เจ้าของสูตร", 34, GOLD, 0, 700); s.fade(or3, ix(12) + 1.0, 0.3)
toplab(s, "", "เกษตรกรเป็นเจ้าของผลผลิต", ix(11), ix(12) - 0.1, WHITE, LBL, 52)
toplab(s, "", "แต่บริษัทเป็นเจ้าของสูตร", ix(12), ix(13) - 0.1, GOLD, LBL, 52)
tl(f'tl.fromTo("#{pd}", {{scale: 1}}, {{scale: 1.08, transformOrigin: "50% 50%", duration: 0.35, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false}}, {ix(12) + 0.9:.3f});')
cue(ix(12) + 0.9, "bell_G5", -22)
toplab(s, "ทุกฤดูกาล", "เกษตรกรต้องกลับมาจ่ายใหม่", ix(13), c3, RED, LBL, 52)
sn = thl(s, 585, 1035, "ฤดูกาลที่", 34, RED, 0, 700, "end"); s.fade(sn, ix(13) + 0.5, 0.2)
for k in range(3):
    t = ix(13) + 0.5 + k * 1.0
    cn = coin(s, 370, 830, 22)
    tl(f'tl.set("#{cn}", {{opacity: 1}}, {t:.3f});')
    tl(f'tl.to("#{cn}", {{x: 330, duration: 0.8, ease: "power1.inOut"}}, {t:.3f});')
    tl(f'tl.to("#{cn}", {{y: -90, duration: 0.4, ease: "sine.out", yoyo: true, repeat: 1}}, {t:.3f});')
    hide(cn, t + 0.75, 0.12)
    sl = thl(s, 600, 1035, f"{k + 1}", 38, RED, 0, 700, "start")
    s.fade(sl, t, 0.2)
    if k < 2: hide(sl, t + 0.9, 0.12)
    cue(t + 0.78, "tick_" + str(k + 1), -18)

# 4  "นี่แหละ คือเกมทั้งหมด"
s = S(ix(16) - 0.1, ix(18) - 0.1, ground=False, hide=False)
g4a = thl(s, 540, 880, "นี่แหละ", 44, LBL, 0, 600)
s.fade(g4a, ix(16) - 0.05, 0.35, y=10)
g4 = thl(s, 540, 975, "คือเกมทั้งหมด", 72, WHITE, 0, 700)
tl(f'tl.fromTo("#{g4}", {{opacity: 0, scale: 1.25, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.45, ease: "expo.out", immediateRender: false}}, {ix(17) - 0.1:.3f});')
cue(ix(17) - 0.1, "whoosh-short_2", -22)

# 5  "คนส่วนใหญ่ขายผลผลิต ขายเวลา ขายแรงงาน ได้เงินครั้งเดียว... แล้วก็ต้องเริ่มใหม่"
s = S(ix(18) - 0.1, ix(23) + 0.3)
w5 = s.fig(540, 1.0, WHITE); s.pop(w5, ix(18) - 0.05, 0.4)
toplab(s, "คนส่วนใหญ่", "ขายผลผลิต", ix(18), ix(21) - 0.1, WHITE, LBL, 64)
ck = s.raw(f'<g id="@ID@" style="opacity:0"><circle cx="270" cy="880" r="62" fill="none" stroke="#f4f4f2" stroke-width="6"/>'
           f'<path d="M 270 880 L 270 840 M 270 880 L 300 896" stroke="#f4f4f2" stroke-width="6" stroke-linecap="round"/></g>', "ck")
s.pop(ck, ix(19) - 0.1, 0.4, 0.5, "50% 50%")
cl5 = thl(s, 270, 1000, "ขายเวลา", 34, LBL, 0, 700); s.fade(cl5, ix(19), 0.3)
bo = s.raw(f'<path id="@ID@" d="M 822 812 L 776 886 L 806 886 L 790 948 L 842 866 L 810 866 Z" fill="#f4f4f2" style="opacity:0"/>', "bo")
s.pop(bo, ix(20) - 0.1, 0.4, 0.5, "50% 50%")
el5 = thl(s, 810, 1000, "ขายแรงงาน", 34, LBL, 0, 700); s.fade(el5, ix(20), 0.3)
cue(ix(19) - 0.1, "pop_1", -22); cue(ix(20) - 0.1, "pop_2", -22)
toplab(s, "ได้เงิน", "ครั้งเดียว", ix(21), ix(22) - 0.1, GOLD, LBL, 64)
s.raw(f'<rect x="290" y="1310" width="500" height="34" rx="17" fill="none" stroke="#ffffff40" stroke-width="2.5"/>', "bf")
bar = s.raw(f'<rect id="@ID@" x="290" y="1310" width="0" height="34" rx="17" fill="{GOLD}"/>', "br")
tl(f'tl.fromTo("#{bar}", {{attr: {{width: 0}}}}, {{attr: {{width: 500}}, duration: 0.7, ease: "power2.out", immediateRender: false}}, {ix(21) + 0.1:.3f});')
pl5 = thl(s, 540, 1405, "+ ได้เงินหนึ่งครั้ง", 34, GOLD, 0, 700); s.fade(pl5, ix(21) + 0.2, 0.3)
cue(ix(21) + 0.1, "swell_1", -22)
toplab(s, "แล้วก็ต้อง", "เริ่มใหม่", ix(22), ix(23) + 0.3, RED, LBL, 66)
tl(f'tl.to("#{bar}", {{attr: {{width: 0}}, duration: 0.6, ease: "power2.in"}}, {ix(22) + 0.4:.3f});')
hide(pl5, ix(22) + 0.4, 0.25)
z5 = thl(s, 540, 1405, "กลับไปที่ศูนย์", 34, RED, 0, 700); s.fade(z5, ix(22) + 0.6, 0.3)
cue(ix(22) + 0.4, "whoosh-short_3", -22)

# 6  "แต่คนรวยถือเมล็ด หุ้น ธุรกิจ สิทธิบัตร สิ่งที่จ่ายเงินให้เขา ซ้ำแล้วซ้ำอีก ทุกฤดูกาล"
s = S(ix(23) + 0.25, ix(30) - 0.1)
sp6 = s.spot(540, 0, "232,194,106"); s.fade(sp6, ix(23) + 0.3, 0.5)
r6 = s.fig(540, 1.0, GOLD); s.pop(r6, ix(23) + 0.3, 0.45)
toplab(s, "แต่คนรวย", "ถือเมล็ด", ix(23) + 0.3, ix(27) - 0.1, GOLD, LBL, 68)
bs = seed(s, 540, 1000, 2.0); s.pop(bs, ix(23) + 1.0, 0.45, 0.2, "50% 50%"); cue(ix(23) + 1.0, "bell_E5", -18)
hide(bs, ix(24) - 0.1, 0.3)
TILES = [("หุ้น", 220, 24), ("ธุรกิจ", 540, 25), ("สิทธิบัตร", 860, 26)]
ICON = [
    f'<path d="M -50 22 L -18 -6 L 6 8 L 48 -30" fill="none" stroke="{GOLD}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
    f'<path d="M 30 -32 L 50 -32 L 50 -12" fill="none" stroke="{GOLD}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>',
    f'<path d="M -52 -10 L -44 -36 L 44 -36 L 52 -10 Z" fill="{GOLD}"/><rect x="-44" y="-10" width="88" height="44" fill="none" stroke="{GOLD}" stroke-width="6"/>'
    f'<rect x="-12" y="6" width="24" height="28" fill="{GOLD}"/>',
    f'<rect x="-34" y="-40" width="68" height="80" rx="6" fill="none" stroke="{GOLD}" stroke-width="6"/>{seed_svg(0, -2, 0.9)}',
]
tiles = []
for (name, x, w_), icon in zip(TILES, ICON):
    t_ = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(x - 140, 700, 280, 200, 20)}" fill="#0f1319" stroke="{GOLD}" stroke-opacity="0.55" stroke-width="2.5"/>'
               f'<g transform="translate({x},772)">{icon}</g>'
               f'<text x="{x}" y="876" text-anchor="middle" {TH} font-size="34" fill="#fff">{name}</text></g>', "tl")
    s.pop(t_, ix(w_) - 0.1, 0.4, 0.6, "50% 50%"); cue(ix(w_) - 0.1, "pop_" + str(len(tiles) + 1), -20); tiles.append(t_)
toplab(s, "สิ่งที่จ่ายเงินให้เขา", "ซ้ำแล้วซ้ำอีก", ix(27), ix(30) - 0.1, GOLD, LBL, 64)
for wv, t in enumerate([ix(27) + 0.4, ix(28) + 0.1, ix(29) + 0.2]):
    for j, (_, x, _w) in enumerate(TILES):
        cn = coin(s, x, 930, 22)
        tl(f'tl.fromTo("#{cn}", {{opacity: 0, y: -20}}, {{opacity: 1, y: 0, duration: 0.2, immediateRender: false}}, {t + j * 0.07:.3f});')
        tl(f'tl.to("#{cn}", {{x: {(540 - x) * 0.55 + (j - 1) * 30:.0f}, y: 150, duration: 0.55, ease: "power2.in"}}, {t + j * 0.07 + 0.2:.3f});')
        hide(cn, t + j * 0.07 + 0.7, 0.15)
    cue(t + 0.7, "tick-crisp_" + str(wv + 1), -18)

# 7  "ผลผลิตกินแล้วก็หมด แต่เมล็ดหนึ่งเมล็ด งอกเป็นผลผลิตได้อีกมากมาย"
s = S(ix(30) - 0.1, ix(33) + 0.15, ground=False)
toplab(s, "", "ผลผลิต กินแล้วก็หมด", ix(30) - 0.1, ix(31), WHITE, LBL, 60)
bites = s.uid("bi")
cr = s.raw(f'<g id="@ID@" style="opacity:0">{crop_svg(270, 1000, 2.4)}<g id="{bites}" style="opacity:0"><circle cx="398" cy="948" r="46" fill="#06070a"/><circle cx="368" cy="990" r="38" fill="#06070a"/></g></g>', "cr")
s.pop(cr, ix(30), 0.4, 0.5, "50% 50%")
s.fade(bites, ix(30) + 0.55, 0.12); cue(ix(30) + 0.55, "click_1", -18)
tl(f'tl.to("#{cr}", {{opacity: 0, scale: 0.6, transformOrigin: "50% 50%", duration: 0.5, ease: "power2.in"}}, {ix(30) + 1.0:.3f});')
z7 = thl(s, 270, 1185, "หมด", 40, RED, 0, 700); s.fade(z7, ix(30) + 1.3, 0.3)
toplab(s, "แต่เมล็ดหนึ่งเมล็ด", "งอกเป็นผลผลิตได้อีกมากมาย", ix(31), ix(33) + 0.15, GOLD, LBL, 52)
s0 = seed(s, 780, 1180, 1.3); s.pop(s0, ix(31), 0.35, 0.3, "50% 50%")
l1 = thl(s, 780, 1258, "1 เมล็ด", 32, LBL, 0, 700); s.fade(l1, ix(31) + 0.1, 0.3)
br = s.path("M 780 1160 L 780 1060 M 780 1110 L 670 1060 M 780 1110 L 890 1060", "#f4f4f2", 4); s.draw(br, ix(32), 0.4)
for j, x in enumerate([670, 780, 890]):
    p = plant(s, x, 1060, 0.8, WHITE, fruit=True); s.pop(p, ix(32) + 0.25 + j * 0.08, 0.4, 0.05, "50% 100%")
    for q, dx in enumerate([-30, 0, 30]):
        sd = seed(s, x + dx, 930 - (q % 2) * 18, 0.55); s.pop(sd, ix(32) + 0.9 + j * 0.1 + q * 0.05, 0.3, 0.2, "50% 50%")
l9 = thl(s, 780, 880, "เมล็ดอีกมากมาย", 32, GOLD, 0, 700); s.fade(l9, ix(32) + 1.0, 0.3)
cue(ix(32), "swell_2", -20); cue(ix(32) + 0.9, "pop_3", -22)

# 8  "คำถามจริงๆ จึงไม่ใช่ว่าคุณทำงานหนักแค่ไหน แต่คือ... คุณเป็นเจ้าของอะไร"
s = S(ix(33) + 0.1, ix(37) - 0.1)
tw = toplab(s, "คำถามจริงๆ ไม่ใช่ว่า", "คุณทำงานหนักแค่ไหน", ix(33) + 0.15, ix(35) - 0.1, WHITE, LBL, 58)
w8 = s.fig(540, 1.0, WHITE); s.pop(w8, ix(33) + 0.15, 0.4)
tl(f'tl.fromTo("#{w8}", {{y: 0}}, {{y: -16, duration: 0.18, yoyo: true, repeat: 11, ease: "sine.inOut", immediateRender: false}}, {ix(34):.3f});')
st8 = s.path("M 200 542 H 880", RED, 6); s.draw(st8, ix(35) - 0.45, 0.35); cue(ix(35) - 0.45, "tock_1", -18)
hide(st8, ix(35) - 0.2, 0.15)
hide(w8, ix(36) - 0.15, 0.3)
sp8 = s.spot(540, 0, "232,194,106"); s.fade(sp8, ix(36) - 0.1, 0.5)
g8 = s.fig(540, 1.0, GOLD); s.pop(g8, ix(36) - 0.1, 0.45)
toplab(s, "แต่คือ", "คุณเป็นเจ้าของอะไร", ix(35), ix(37) - 0.1, GOLD, LBL, 64)
for j, (x, y) in enumerate([(380, 960), (700, 940), (560, 860)]):
    sd = seed(s, x, y, 1.0); s.pop(sd, ix(36) + 0.4 + j * 0.12, 0.35, 0.2, "50% 50%")
cue(ix(36) - 0.1, "bell_C5", -18)

# 9  "ทุกเดือน แบ่งผลผลิตของคุณส่วนหนึ่ง... แล้วเปลี่ยนมันให้เป็นเมล็ด"
s = S(ix(37) - 0.1, ix(40) - 0.1, ground=False)
toplab(s, "ทุกเดือน แบ่ง", "ผลผลิตของคุณส่วนหนึ่ง", ix(37), ix(39) - 0.1, WHITE, LBL, 56)
hv = thl(s, 540, 722, "ผลผลิตเดือนนี้", 32, LBL, 0, 600); s.fade(hv, ix(37), 0.3)
items = []
for k in range(10):
    x = 180 + k * 80
    it = s.raw(f'<g id="@ID@" style="opacity:0">{crop_svg(x, 800, 0.55)}</g>', "it")
    s.pop(it, ix(37) + 0.05 + k * 0.05, 0.3, 0.5, "50% 50%"); items.append((x, it))
cue(ix(37), "pop_1", -22)
jar = s.raw(f'<g id="@ID@" style="opacity:0"><path d="M 450 1010 L 450 1210 Q 450 1240 480 1240 L 600 1240 Q 630 1240 630 1210 L 630 1010" fill="none" stroke="{GOLD}" stroke-width="5" stroke-linejoin="round"/>'
            f'<rect x="436" y="994" width="208" height="18" rx="6" fill="{GOLD}"/>'
            f'<text x="540" y="1305" text-anchor="middle" {TH} font-size="36" fill="{GOLD}">เมล็ด</text></g>', "jr")
s.pop(jar, ix(38), 0.4, 0.6, "50% 50%")
for j, (x, it) in enumerate(items[-2:]):
    tl(f'tl.to("#{it}", {{x: {520 + j * 40 - x}, y: 350, scale: 0.7, transformOrigin: "50% 50%", duration: 0.7, ease: "power2.inOut"}}, {ix(38) + 0.6 + j * 0.15:.3f});')
    hide(it, ix(39) + 0.2, 0.3)
    sd = seed(s, 520 + j * 40, 1170 - j * 10, 1.0); s.pop(sd, ix(39) + 0.25 + j * 0.1, 0.35, 0.2, "50% 50%")
cue(ix(38) + 0.6, "whoosh-short_1", -22)
toplab(s, "แล้วเปลี่ยนมัน", "ให้เป็นเมล็ด", ix(39), ix(40) - 0.1, GOLD, LBL, 68)
sprout = plant(s, 540, 1000, 0.9, GOLD); s.pop(sprout, ix(39) + 0.55, 0.5, 0.05, "50% 100%")
cue(ix(39) + 0.25, "bell_E5", -20); cue(ix(39) + 0.55, "swell_1", -22)

# 10  "จงเป็นเจ้าของสูตร ไม่ใช่แค่ผลผลิต"
s = S(ix(40) - 0.1, ix(42) + 0.35)
s.spot(540, 1, "232,194,106")
g10 = s.fig(540, 1.0, GOLD); s.pop(g10, ix(40) - 0.1, 0.4)
t10 = thl(s, 540, 620, "จงเป็นเจ้าของสูตร", 72, GOLD, 0, 700)
tl(f'tl.fromTo("#{t10}", {{opacity: 0, scale: 1.3, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.45, ease: "expo.out", immediateRender: false}}, {ix(40) - 0.05:.3f});')
n10 = thl(s, 540, 715, "ไม่ใช่แค่ผลผลิต", 46, "#9aa0a8", 0, 700); s.fade(n10, ix(41) - 0.1, 0.35, y=10)
s10 = seed(s, 540, 960, 1.6); s.pop(s10, ix(40) + 0.5, 0.45, 0.2, "50% 50%")
cue(ix(40), "bell_G5", -16)

# 11  outro (handles, no end card; the brand lines stay in English)
s = S(ix(42) + 0.3, TOTAL)
es = s.spot(540, 0, "232,194,106", 40, 230); s.fade(es, ix(42) + 0.35, 0.6)
em = s.raw('<image id="@ID@" href="assets/otm_emblem.png" x="390" y="900" width="300" height="291" style="opacity:0;filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>', "i")
s.pop(em, ix(42) + 0.35, 0.7, 0.6, "50% 50%"); cue(ix(42) + 0.35, "bell_A4", -16)
o1l = s.label(540, 1300, "ORDER THE MARKET", 32, GOLD, 0, 800, 0.3); s.fade(o1l, ix(42) + 0.55, 0.5)
o2 = thl(s, 540, 1365, "อย่าให้ตลาดเป็นฝ่ายสั่งคุณ", 34, WHITE, 0, 600); s.fade(o2, ix(45), 0.4)
o3 = s.pill(540, 1470, "FOLLOW FOR MORE", GOLD, "#111", 30); s.pop(o3, ix(46), 0.4, 0.6, "50% 50%"); cue(ix(46), "click-confirm_1", -16)
hx = 290
soc = s.raw(f'<g id="@ID@" style="opacity:0">'
            f'<rect x="{hx}" y="1548" width="36" height="36" rx="10" fill="none" stroke="#fff" stroke-width="3"/>'
            f'<circle cx="{hx + 18}" cy="1566" r="8.5" fill="none" stroke="#fff" stroke-width="3"/><circle cx="{hx + 28}" cy="1556" r="2.4" fill="#fff"/>'
            f'<text x="{hx + 48}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@fxzuez_28</text>'
            f'<path d="M {hx + 322} 1546 V 1574 A 9 9 0 1 1 {hx + 313} 1565 M {hx + 322} 1546 Q {hx + 326} 1557 {hx + 338} 1558" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>'
            f'<text x="{hx + 348}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@zuez_28</text></g>', "so")
disc = s.label(540, 1650, "EDUCATIONAL ONLY · NOT FINANCIAL ADVICE", 28, GREY, 0, 600, 0.12)
s.fade(soc, ix(45) + 0.6, 0.5, y=12)
s.fade(disc, ix(45) + 0.9, 0.5)
TIMELINE = ""


# ------------------------------------------------------------------ end card, dust, ground, emblem
tl(f'tl.to("#mark", {{opacity: 0, duration: 0.3}}, {A("order") - 0.2:.3f});')
dust = ""
for k in range(40):
    x, y, r, op = rnd.uniform(0, 1080), rnd.uniform(0, 1920), rnd.uniform(1.2, 3.2), rnd.uniform(0.05, 0.22)
    dust += f'<circle id="d{k}" cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#fff" opacity="{op:.2f}"/>'
    tl(f'tl.fromTo("#d{k}", {{x: 0, y: 0}}, {{x: {rnd.uniform(-70, 70):.0f}, y: {-rnd.uniform(150, 480):.0f}, duration: {TOTAL}, ease: "none"}}, 0);')

scenes_svg = "\n".join(f'<g id="{x.id}" style="opacity:0;visibility:hidden" data-layout-allow-overlap>' + "".join(x.items) + "</g>" for x in S.scenes)
CSS = FONTS + """
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #000; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #000; font-family: Montserrat, sans-serif; color: #fff; }
#stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
#vig { position: absolute; inset: 0; pointer-events: none; background: radial-gradient(ellipse at 50% 48%, rgba(40,44,52,0.35) 0%, transparent 55%, rgba(0,0,0,0.6) 100%); }
#mark { position: absolute; left: 495px; top: 1560px; width: 90px; opacity: 0.85; filter: drop-shadow(0 0 10px rgba(255,255,255,0.2)); }
"""
html = f"""<!doctype html>
<html lang="th" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="otm-ownseed-th" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
{TIMELINE}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-ownseed-th-audio" class="clip" src="assets/audio/mix_ownseed_th.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-ownseed-th"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
