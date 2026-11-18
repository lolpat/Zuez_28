"""OTM "The Last $1,000" (Thai version): the Thai-language edition of otm-thousand, built from the same scene file with
LANG = "th". Thai narration (ElevenLabs "Patinya", calm Thai narrator), Thai on-screen text in Kanit (OFL,
assets/fonts); money and numbers stay in Montserrat; the outro keeps the brand lines in English. Protect the last
$1,000: survive first, risk 1% or less, one setup, no shortcuts. Original script, voice only, no music.
Scenes key off token indices of work/words.json (the script's tokens aligned to the voice; anchor table TH_ANC).
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

LANG = "th"
# ---- shared scenes for "The Last $1,000" (English: otm-thousand, Thai: otm-thousand-th); LANG is set just above this line
def ix(i):
    return W(i)

TH_ = LANG == "th"
# EN: word indices of work/words.json; TH: token indices of work/script.txt (aligned into work/words.json)
EN_ANC = dict(last=6, how=8, double=13, job=19, survive=26, risk=29, week=35, knock=38, pct=42, less=46, setup=48, again=52,
              know=58, noshort=65, nohero=67, protect=71, repeat=72, grow=74, slow=76, ambition=83, order=86, dont=89, follow=95)
TH_ANC = dict(last=1, how=(2, -0.2), double=(3, 0.5), job=4, survive=5, risk=6, week=7, knock=8, pct=9, less=10, setup=11, again=12,
              know=13, noshort=14, nohero=15, protect=16, repeat=17, grow=18, slow=19, ambition=20, order=21, dont=24, follow=25)

def K(key):
    a = (TH_ANC if TH_ else EN_ANC)[key]
    return ix(a[0]) + a[1] if isinstance(a, tuple) else ix(a)

TXT = dict(
    h1s=("IMAGINE YOU'RE DOWN TO", "ลองนึกว่าคุณเหลือเงิน"), h1b=("YOUR LAST $1,000", "ก้อนสุดท้าย $1,000"),
    h2b=("HOW WOULD YOU TRADE IT?", "คุณจะเทรดยังไง?"),
    d_s=("NOT BY TRYING TO", "ไม่ใช่พยายาม"), d_b=("DOUBLE IT", "ทำให้เป็นสองเท่า"),
    j_s=("JOB #1 OF A SMALL ACCOUNT", "หน้าที่แรกของพอร์ตเล็ก"), j_b=("SURVIVE", "อยู่รอด"),
    r_s=("RISK SO LITTLE THAT ONE BAD WEEK", "เสี่ยงให้น้อยพอ ที่สัปดาห์แย่ๆ"), r_b=("CAN'T KNOCK YOU OUT", "ล้มคุณไม่ได้"),
    p_s=("RISK PER TRADE", "ความเสี่ยงต่อไม้"), p_b=("1% OR LESS", "1% หรือน้อยกว่า"),
    bal=("BALANCE", "ยอดเงิน"), stand=("STILL STANDING", "ยังยืนอยู่"), risk10=("$10 AT RISK", "เสี่ยงแค่ $10"),
    o_s=("TRADE", "เทรดแค่"), o_b=("ONE SETUP", "เซ็ตอัพเดียว"),
    k_s=("UNTIL YOU KNOW IT", "จนรู้จักมัน"), k_b=("BETTER THAN ANYONE", "ดีกว่าใคร"),
    skill=("SKILL", "ความชำนาญ"),
    ns=("NO SHORTCUTS.", "ไม่มีทางลัด"), nh=("NO HERO TRADES.", "ไม่มีไม้ฮีโร่"),
    c_short=("SHORTCUT", "ทางลัด"), c_all=("ALL IN", "ทุ่มหมดตัว"),
    pr=("PROTECT", "ปกป้อง"), rp=("REPEAT", "ทำซ้ำ"), gw=("GROW SLOWLY", "โตช้าๆ"),
    s_s=("SLOW GROWTH NEVER KILLED", "การโตช้าไม่เคยฆ่า"), s_b=("A SMALL ACCOUNT", "พอร์ตเล็ก"),
    a_b=("BIG AMBITION DOES.", "ความอยากรวยเร็วต่างหาก"),
    fast=("GET RICH FAST", "รวยเร็ว"),
    sub=("DON'T LET THE MARKET ORDER YOU", "อย่าให้ตลาดเป็นฝ่ายสั่งคุณ"))
DAYS = (["MON", "TUE", "WED", "THU", "FRI"], ["จ.", "อ.", "พ.", "พฤ.", "ศ."])

def X(key):
    return TXT[key][1 if TH_ else 0]

FONTS = "" if not TH_ else "".join(
    f"@font-face {{ font-family: 'Kanit'; font-style: normal; font-weight: {w}; font-display: block; "
    f"src: url('assets/fonts/kanit-{sub}-{w}-normal.woff2') format('woff2'); unicode-range: {rng}; }}\n"
    for w in (600, 700)
    for sub, rng in (("thai", "U+02D7, U+0303, U+0331, U+0E01-0E5B, U+200C-200D, U+25CC"),
                     ("latin", "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, "
                               "U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD")))

def thai(s):
    s.items[-1] = (s.items[-1].replace('font-family="Montserrat"', 'font-family="Kanit"').replace('font-weight="800"', 'font-weight="700"'))
    s.items[-1] = _re.sub(r'letter-spacing="[^"]*"', 'letter-spacing="0"', s.items[-1])

def tx(s, x, y, text, size=30, col=LBL, op=0, weight=800, anchor="middle", sp=0.06):
    if TH_:
        i = s.label(x, y, text, round(size * 1.08), col, op, 700 if weight >= 700 else 600, 0, anchor); thai(s)
    else:
        i = s.label(x, y, text, size, col, op, weight, sp, anchor)
    return i

def tpill(s, x, y, text, fill=GOLD, tcol="#111", size=36):
    i = s.pill(x, y, text, fill, tcol, size)
    if TH_: thai(s)
    return i

def num(s, x, y, text, size, col, op=0, anchor="middle"):
    """Numbers and money always in Montserrat (digits read the same in both languages)."""
    return s.label(x, y, text, size, col, op, 800, 0.02, anchor)

def toplab(s, small, big, t0, t1, bcol=WHITE, scol=LBL, bsize=52, y=560, op=0, tb=None):
    """small line + big line; tb lets the big line arrive later than the small one."""
    ids = []
    if small:
        a = tx(s, 540, y - 72, small, 28, scol, op, 700, sp=0.12); ids.append((a, t0))
    b = tx(s, 540, y, big, bsize, bcol, op, 800, sp=0.04); ids.append((b, tb if tb is not None else t0))
    for i, t in ids:
        if not op: s.fade(i, t, 0.3, y=10)
        tl(f'tl.to("#{i}", {{opacity: 0, duration: 0.15}}, {t1 - 0.17:.3f});')
    return [i for i, _ in ids]

def hide(i, t, d=0.3, to=0):
    tl(f'tl.to("#{i}", {{opacity: {to}, duration: {d}}}, {t:.3f});')

def card(s, cx, op=1, y=1090, w=220, h=130):
    """the $1,000 account card, standing on the ground"""
    return s.raw(f'<g id="@ID@" style="opacity:{op};filter:drop-shadow(0 0 16px rgba(232,194,106,0.45))">'
                 f'<path d="{rrect(cx - w // 2, y, w, h, 18)}" fill="#14110a" stroke="{GOLD}" stroke-width="3"/>'
                 f'<text x="{cx}" y="{y + h // 2 + 16}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="46" '
                 f'letter-spacing="0.02em" fill="{GOLD}">$1,000</text></g>', "cd")

# 1  "Imagine you're down to your last thousand dollars. How would you trade it?"
s = S(0, K("double") - 0.1, first=True)
toplab(s, X("h1s"), X("h1b"), 0, K("how") - 0.1, GOLD, LBL, 60, op=1)
toplab(s, "", X("h2b"), K("how"), K("double") - 0.1, WHITE, LBL, 50)
f1 = s.fig(330, 1.0, WHITE, 1)
sp1 = s.spot(700, 0, "232,194,106", 30, 150); s.fade(sp1, K("last") - 0.1, 0.5)
c1 = card(s, 700, 0); s.pop(c1, K("last"), 0.45, 0.5); cue(K("last"), "pop_1", -18)
q1 = s.label(330, 1020, "?", 84, WHITE, 0, 800, 0); s.pop(q1, K("how"), 0.4, 0.3, "50% 50%"); cue(K("how"), "tick_1", -20)

# 2  "Not by trying to double it. The first job of a small account... is to survive."
s = S(K("double") - 0.1, K("risk") - 0.1)
toplab(s, X("d_s"), X("d_b"), K("double"), K("job") - 0.1, RED, LBL, 60)
toplab(s, X("j_s"), X("j_b"), K("job"), K("risk") - 0.1, GOLD, LBL, 64, tb=K("survive"))
s.fig(330, 1.0, WHITE, 1)
card(s, 700, 1)
ar = s.path("M 790 1080 Q 840 960 880 830 M 852 858 L 880 830 L 896 866", GOLD, 6); s.draw(ar, K("double") + 0.15, 0.5)
x2 = num(s, 880, 800, "×2", 64, GOLD); s.pop(x2, K("double") + 0.5, 0.4, 0.4, "50% 50%")
cue(K("double") + 0.15, "whoosh-short_2", -22)
st = s.path("M 826 792 L 936 744", RED, 8); s.draw(st, K("job") - 0.5, 0.25); cue(K("job") - 0.5, "tock_1", -18)
hide(ar, K("job") - 0.2, 0.3, 0.25); hide(x2, K("job") - 0.2, 0.3, 0.25); hide(st, K("job") - 0.2, 0.3, 0.4)
sh = s.path("M 700 1000 L 852 1042 V 1146 Q 852 1226 700 1262 Q 548 1226 548 1146 V 1042 Z", GOLD, 6,
            style="filter:drop-shadow(0 0 14px rgba(232,194,106,0.8))")
s.draw(sh, K("job") + 0.1, 0.8); cue(K("job") + 0.1, "swell_1", -22); cue(K("survive"), "bell_C5", -18)

# 3  "So you risk so little... that one bad week can't knock you out. One percent a trade, or less."
s = S(K("risk") - 0.1, K("setup") - 0.1, ground=False, restore=False)
toplab(s, X("r_s"), X("r_b"), K("risk"), K("pct") - 0.1, WHITE, LBL, 52)
toplab(s, X("p_s"), X("p_b"), K("pct"), K("setup") - 0.1, GOLD, LBL, 64)
days = DAYS[1 if TH_ else 0]
t_x0, t_x1 = K("week"), K("pct") - 0.2
for k in range(5):
    x = 180 + k * 150
    bx = s.raw(f'<path id="@ID@" d="{rrect(x, 650, 120, 110, 16)}" fill="#0f1319" stroke="#ffffff55" stroke-width="2" style="opacity:0"/>', "bx")
    s.fade(bx, K("risk") + 0.15 + k * 0.08, 0.3)
    dl = tx(s, x + 60, 690, days[k], 28, LBL, 0, 700, sp=0.06); s.fade(dl, K("risk") + 0.15 + k * 0.08, 0.3)
    t = t_x0 + k * (t_x1 - t_x0) / 4
    xx = s.path(f"M {x + 40} 712 L {x + 80} 748 M {x + 80} 712 L {x + 40} 748", RED, 7); s.draw(xx, t, 0.18)
    cue(t, "tick_" + str(k % 3 + 1), -22)
tr = s.raw(f'<rect id="@ID@" x="180" y="820" width="720" height="44" rx="22" fill="#1d2229" style="opacity:0"/>', "tr")
bar = s.raw(f'<rect id="@ID@" x="180" y="820" width="720" height="44" rx="22" fill="{GOLD}" '
            f'style="opacity:0;filter:drop-shadow(0 0 10px rgba(232,194,106,0.6))"/>', "br")
s.fade(tr, K("risk") + 0.3, 0.3); s.fade(bar, K("risk") + 0.3, 0.3)
bl = tx(s, 180, 930, X("bal"), 30, LBL, 0, 700, "start", sp=0.1); s.fade(bl, K("risk") + 0.3, 0.3)
vals = []
for k in range(6):
    v = num(s, 900, 934, f"${1000 - 10 * k:,}", 48, GOLD, 0, "end"); vals.append(v)
s.fade(vals[0], K("risk") + 0.3, 0.3)
for k in range(1, 6):
    t = t_x0 + (k - 1) * (t_x1 - t_x0) / 4 + 0.1
    tl(f'tl.set("#{vals[k - 1]}", {{opacity: 0}}, {t:.3f}); tl.set("#{vals[k]}", {{opacity: 1}}, {t:.3f});')
    tl(f'tl.to("#{bar}", {{attr: {{width: {720 - 7.2 * k:.1f}}}, duration: 0.2, ease: "power2.out"}}, {t:.3f});')
m5 = num(s, 180, 1000, "−5%", 40, RED, 0, "start"); s.fade(m5, t_x1 + 0.3, 0.3)
sd = tx(s, 900, 1000, X("stand"), 34, GOLD, 0, 800, "end", sp=0.08); s.fade(sd, t_x1 + 0.45, 0.3)
cue(t_x1 + 0.45, "bell_E5", -20)
dots = "".join(f'<circle cx="{414 + (k % 10) * 28}" cy="{1090 + (k // 10) * 28}" r="10" fill="{GOLD}" fill-opacity="0.32"/>'
               for k in range(1, 100))
dg = s.raw(f'<g id="@ID@" style="opacity:0">{dots}</g>', "dg"); s.fade(dg, K("pct") + 0.1, 0.4)
rd = s.raw(f'<circle id="@ID@" cx="414" cy="1090" r="14" fill="{RED}" style="opacity:0;filter:drop-shadow(0 0 8px rgba(255,77,94,0.9))"/>', "rd")
s.pop(rd, K("pct") + 0.45, 0.35, 0.2, "50% 50%"); cue(K("pct") + 0.45, "pop_2", -18)
tl(f'tl.to("#{rd}", {{scale: 0.6, transformOrigin: "50% 50%", duration: 0.35, ease: "power2.inOut"}}, {K("less"):.3f});')
r10 = tx(s, 540, 1410, X("risk10"), 34, RED, 0, 800, sp=0.08); s.fade(r10, K("pct") + 0.6, 0.3)

# 4  "You trade one setup. The same one, again and again... until you know it better than anyone."
s = S(K("setup") - 0.1, K("noshort") - 0.1, ground=False, hide=False, restore=False)
toplab(s, X("o_s"), X("o_b"), K("setup"), K("know") - 0.1, GOLD, LBL, 64)
toplab(s, X("k_s"), X("k_b"), K("know"), K("noshort") - 0.1, WHITE, LBL, 52)
def tile(x, y, op=0):
    pat = (f"M {x + 14} {y + 22} L {x + 54} {y + 74} L {x + 76} {y + 58} L {x + 98} {y + 82} L {x + 128} {y + 44} L {x + 156} {y + 18}")
    return s.raw(f'<g id="@ID@" style="opacity:{op}"><path d="{rrect(x, y, 170, 110, 16)}" fill="#0f1319" stroke="#ffffff40" stroke-width="2"/>'
                 f'<line x1="{x + 14}" y1="{y + 84}" x2="{x + 156}" y2="{y + 84}" stroke="#7d838c" stroke-width="2" stroke-dasharray="6 6"/>'
                 f'<path d="{pat}" fill="none" stroke="{GOLD}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
                 f'<circle cx="{x + 98}" cy="{y + 82}" r="6" fill="{GOLD}"/></g>', "tl")
t_a, t_b = K("again"), K("know") + 0.3
for k in range(12):
    x, y = 170 + (k % 4) * 190, 650 + (k // 4) * 130
    ti = tile(x, y)
    t = K("setup") + 0.15 if k == 0 else t_a + (k - 1) * (t_b - t_a) / 10
    s.pop(ti, t, 0.3, 0.6, "50% 50%")
    if k in (0, 3, 6, 9, 11): cue(t, "tick-crisp_" + str(k % 3 + 1), -22)
sk = tx(s, 170, 1110, X("skill"), 30, LBL, 0, 700, "start", sp=0.1); s.fade(sk, t_a, 0.3)
s.raw(f'<rect id="@ID@" x="170" y="1140" width="740" height="36" rx="18" fill="#1d2229"/>', "st")
sb = s.raw(f'<rect id="@ID@" x="170" y="1140" width="0" height="36" rx="18" fill="{GOLD}" style="filter:drop-shadow(0 0 10px rgba(232,194,106,0.7))"/>', "sb")
tl(f'tl.fromTo("#{sb}", {{attr: {{width: 0}}}}, {{attr: {{width: 740}}, duration: {t_b + 0.3 - t_a:.3f}, ease: "power1.inOut", immediateRender: false}}, {t_a:.3f});')
cue(t_b + 0.3, "bell_E5", -18)

# 5  "No shortcuts. No hero trades. Just protect, repeat, and grow slowly."
s = S(K("noshort") - 0.1, K("slow") - 0.1, ground=False, hide=False)
toplab(s, X("ns"), X("nh"), K("noshort"), K("protect") - 0.1, RED, LBL, 52, tb=K("nohero"))
cA = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(150, 660, 360, 260, 22)}" fill="#0f1319" stroke="#ffffff55" stroke-width="2"/>'
           f'<path d="M 330 700 C 360 725 365 770 355 812 L 305 812 C 295 770 300 725 330 700 Z" fill="none" stroke="#f4f4f2" stroke-width="5"/>'
           f'<circle cx="330" cy="752" r="10" fill="none" stroke="#f4f4f2" stroke-width="4"/>'
           f'<path d="M 306 790 L 286 828 L 310 816 M 354 790 L 374 828 L 350 816" fill="none" stroke="#f4f4f2" stroke-width="5" stroke-linejoin="round"/>'
           f'<path d="M 316 820 Q 330 862 344 820" fill="none" stroke="{GOLD}" stroke-width="5"/></g>', "ca")
cAl = tx(s, 330, 892, X("c_short"), 30, WHITE, 0, 800, sp=0.08)
chips = "".join(f'<ellipse cx="750" cy="{826 - k * 22}" rx="58" ry="17" fill="#1a0f12" stroke="{GOLD}" stroke-width="4"/>' for k in range(5))
cB = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(570, 660, 360, 260, 22)}" fill="#0f1319" stroke="#ffffff55" stroke-width="2"/>{chips}</g>', "cb")
cBl = tx(s, 750, 892, X("c_all"), 30, WHITE, 0, 800, sp=0.08)
s.pop(cA, K("noshort"), 0.4, 0.6, "50% 50%"); s.fade(cAl, K("noshort") + 0.1, 0.3)
s.pop(cB, K("nohero"), 0.4, 0.6, "50% 50%"); s.fade(cBl, K("nohero") + 0.1, 0.3)
xa = s.path("M 190 690 L 470 890 M 470 690 L 190 890", RED, 8); s.draw(xa, K("noshort") + 0.45, 0.25)
xb = s.path("M 610 690 L 890 890 M 890 690 L 610 890", RED, 8); s.draw(xb, K("nohero") + 0.45, 0.25)
cue(K("noshort") + 0.45, "tock_1", -18); cue(K("nohero") + 0.45, "tock_1", -18)
for i in (cA, cAl, cB, cBl, xa, xb):
    hide(i, K("protect") - 0.35, 0.25)
for j, (key, k_) in enumerate((("pr", "protect"), ("rp", "repeat"), ("gw", "grow"))):
    p = tpill(s, 540, 640 + j * 130, X(key), GOLD if j < 2 else WHITE, "#111", 44)
    s.pop(p, K(k_), 0.35, 0.6, "50% 50%"); cue(K(k_), "pop_" + str(j + 1), -18)
stairs = "M 190 1300 " + " ".join(f"H {190 + (k + 1) * 85} V {1300 - (k + 1) * 26}" for k in range(8))
sc = s.path(stairs, GOLD, 5, style="filter:drop-shadow(0 0 10px rgba(232,194,106,0.8))")
s.draw(sc, K("protect") + 0.2, max(1.2, K("slow") - 0.6 - K("protect")), "power1.inOut")

# 6  "Slow growth never killed a small account. Big ambition does."
s = S(K("slow") - 0.1, K("order") + 0.35)
toplab(s, X("s_s"), X("s_b"), K("slow"), K("ambition") - 0.1, GOLD, LBL, 60)
toplab(s, "", X("a_b"), K("ambition"), K("order") + 0.35, RED, LBL, 54)
f6 = s.fig(250, 1.0, WHITE); s.pop(f6, K("slow"), 0.4)
c6 = card(s, 600, 1, 1110, 220, 120)
tl(f'tl.fromTo("#{c6}", {{scale: 1}}, {{scale: 1.07, transformOrigin: "50% 100%", duration: {K("ambition") - K("slow"):.3f}, ease: "none", immediateRender: false}}, {K("slow"):.3f});')
crack = [(600, 1110), (588, 1140), (608, 1165), (590, 1195), (600, 1230)]
cpts = " ".join(f"L {x} {y}" for x, y in crack[1:])
rpts = " ".join(f"L {x} {y}" for x, y in reversed(crack[:-1]))
hl = s.raw(f'<path id="@ID@" d="M 508 1110 H 600 {cpts} H 508 Q 490 1230 490 1212 V 1128 Q 490 1110 508 1110 Z" fill="#1a0f12" stroke="{RED}" stroke-width="3" style="opacity:0"/>', "hl")
hr = s.raw(f'<path id="@ID@" d="M 600 1110 H 692 Q 710 1110 710 1128 V 1212 Q 710 1230 692 1230 H 600 {rpts} Z" fill="#1a0f12" stroke="{RED}" stroke-width="3" style="opacity:0"/>', "hr")
blk = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(440, 976, 320, 124, 16)}" fill="#2a0d12" stroke="{RED}" stroke-width="4" '
            f'style="filter:drop-shadow(0 0 16px rgba(255,77,94,0.7))"/></g>', "bk")
bkt = tx(s, 600, 1050, X("fast"), 32, RED, 0, 800, sp=0.06)
t_hit = K("ambition") + 0.45
for i in (blk, bkt):
    tl(f'tl.set("#{i}", {{y: -1500, opacity: 1}}, {s.o:.3f});')
    tl(f'tl.to("#{i}", {{y: 0, duration: 0.45, ease: "power3.in"}}, {K("ambition"):.3f});')
    tl(f'tl.to("#{i}", {{y: 70, duration: 0.3, ease: "power2.out"}}, {t_hit:.3f});')
cue(K("ambition"), "whoosh-short_1", -20); cue(t_hit, "land_1", -14)
tl(f'tl.set("#{c6}", {{opacity: 0}}, {t_hit:.3f}); tl.set("#{hl}", {{opacity: 1}}, {t_hit:.3f}); tl.set("#{hr}", {{opacity: 1}}, {t_hit:.3f});')
tl(f'tl.to("#{hl}", {{rotation: -24, x: -60, y: 24, opacity: 0, transformOrigin: "0% 100%", duration: 0.9, ease: "power2.out"}}, {t_hit:.3f});')
tl(f'tl.to("#{hr}", {{rotation: 24, x: 60, y: 24, opacity: 0, transformOrigin: "100% 100%", duration: 0.9, ease: "power2.out"}}, {t_hit:.3f});')

# 7  outro (handles, no end card; brand lines stay in English)
s = S(K("order") + 0.3, TOTAL)
es = s.spot(540, 0, "232,194,106", 40, 230); s.fade(es, K("order") + 0.35, 0.6)
em = s.raw('<image id="@ID@" href="assets/otm_emblem.png" x="390" y="900" width="300" height="291" style="opacity:0;filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>', "i")
s.pop(em, K("order") + 0.35, 0.7, 0.6, "50% 50%"); cue(K("order") + 0.35, "bell_A4", -16)
o1l = s.label(540, 1300, "ORDER THE MARKET", 32, GOLD, 0, 800, 0.3); s.fade(o1l, K("order") + 0.55, 0.5)
o2 = tx(s, 540, 1362, X("sub"), 28, WHITE, 0, 700 if not TH_ else 600, sp=0.12); s.fade(o2, K("dont"), 0.4)
o3 = s.pill(540, 1470, "FOLLOW FOR MORE", GOLD, "#111", 30); s.pop(o3, K("follow"), 0.4, 0.6, "50% 50%"); cue(K("follow"), "click-confirm_1", -16)
hx = 290
soc = s.raw(f'<g id="@ID@" style="opacity:0">'
            f'<rect x="{hx}" y="1548" width="36" height="36" rx="10" fill="none" stroke="#fff" stroke-width="3"/>'
            f'<circle cx="{hx + 18}" cy="1566" r="8.5" fill="none" stroke="#fff" stroke-width="3"/><circle cx="{hx + 28}" cy="1556" r="2.4" fill="#fff"/>'
            f'<text x="{hx + 48}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@fxzuez_28</text>'
            f'<path d="M {hx + 322} 1546 V 1574 A 9 9 0 1 1 {hx + 313} 1565 M {hx + 322} 1546 Q {hx + 326} 1557 {hx + 338} 1558" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>'
            f'<text x="{hx + 348}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@zuez_28</text></g>', "so")
disc = s.label(540, 1650, "EDUCATIONAL ONLY · NOT FINANCIAL ADVICE", 28, GREY, 0, 600, 0.12)
s.fade(soc, K("dont") + 0.6, 0.5, y=12)
s.fade(disc, K("dont") + 0.9, 0.5)
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
    <div id="root" data-composition-id="otm-thousand-th" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
{TIMELINE}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-thousand-th-audio" class="clip" src="assets/audio/mix_thousand_th.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-thousand-th"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
