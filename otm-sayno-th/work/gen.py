"""OTM "Say No" (Thai version): the Thai-language edition of otm-sayno, built from the same scene file with LANG = "th".
Thai narration (ElevenLabs "Patinya", calm Thai narrator), Thai on-screen text in Kanit (OFL, assets/fonts); numbers
stay in Montserrat; the outro keeps the brand lines in English. Three temptations, three no's: risk 1%, keep the same
setup, wait for the best trade. Original script, voice only, no music. Scenes key off token indices of work/words.json
(the script's tokens aligned to the voice; anchor table TH_ANC). Writes ../index.html, work/cues.json and
work/timing.json."""
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
# ---- shared scenes for "Say No" (English: otm-sayno, Thai: otm-sayno-th); LANG is set just above this line
def ix(i):
    return W(i)

TH_ = LANG == "th"
# EN: word indices of work/words.json; TH: token indices of work/script.txt (aligned into work/words.json)
EN_ANC = dict(refuse=8, tempt=15, one=23, q1=24, no1=31, alt1=32, alt1b=35, two=40, q2=41, no2=51, alt2=52, alt2b=56,
              three=60, q3=61, no3=67, alt3=68, alt3b=74, noa=78, nob=79, noc=81, job=82, order=85, dont=88, follow=94)
TH_ANC = dict(refuse=1, tempt=2, one=3, q1=4, no1=(6, 0.45), alt1=7, alt1b=8, two=9, q2=10, no2=(12, 0.45), alt2=13, alt2b=15,
              three=16, q3=17, no3=(19, 0.45), alt3=20, alt3b=21, noa=22, nob=23, noc=24, job=(25, -0.35), order=26, dont=29, follow=30)

def K(key):
    a = (TH_ANC if TH_ else EN_ANC)[key]
    return ix(a[0]) + a[1] if isinstance(a, tuple) else ix(a)

TXT = dict(
    h_s=("MOST OF TRADING ISN'T ABOUT", "การเทรดส่วนใหญ่ไม่ได้อยู่ที่"), h_b=("WHAT YOU DO", "สิ่งที่คุณทำ"),
    r_s=("IT'S ABOUT WHAT YOU", "แต่อยู่ที่สิ่งที่คุณ"), r_b=("REFUSE TO DO", "ปฏิเสธ"),
    tm_s=("THE MARKET WILL TEMPT YOU", "ตลาดจะยั่วคุณ"), tm_b=("3 WAYS", "3 แบบ"),
    tn=("TEMPTATION", "แบบที่"),
    t1b=("RISK MORE", "เสี่ยงเยอะขึ้น"), q1=("“WIN IT BACK FASTER”", "“จะได้ทุนคืนเร็วๆ”"), i1=("RISK 20%", "เสี่ยง 20%"),
    t2b=("TRY A NEW STRATEGY", "ลองระบบใหม่ดู"), q2=("“3 LOSSES IN A ROW...”", "“แพ้สามไม้ติด...”"),
    t3b=("JUST TAKE SOMETHING", "เข้าสักไม้เถอะ"), q3=("“BORED? JUST TAKE ONE”", "“เบื่อแล้ว เข้าสักไม้”"),
    no=("NO", "ไม่"), sn=("SAY NO.", "บอกว่าไม่"),
    a1=("RISK 1%", "เสี่ยงแค่ 1%"), a1s=("STAY IN THE GAME", "แล้วอยู่ในเกมต่อ"),
    a2=("SAME SETUP. SAME RULES.", "เซ็ตอัพเดิม กฎเดิม"), a2s=("LONG ENOUGH TO WORK", "นานพอให้มันทำงาน"),
    a3=("WAIT FOR THE A+ TRADE", "รอเทรดที่ดีที่สุด"), a3s=("ON YOUR BEST DAY", "ในวันที่ดีที่สุดของคุณ"),
    job=("THAT'S THE JOB", "นั่นแหละคืองาน"),
    sub=("DON'T LET THE MARKET ORDER YOU", "อย่าให้ตลาดเป็นฝ่ายสั่งคุณ"))

def X(key):
    return TXT[key][1 if TH_ else 0]

FONTS = "" if not TH_ else "".join(
    f"@font-face {{ font-family: 'Kanit'; font-style: normal; font-weight: {w}; font-display: block; "
    f"src: url('assets/fonts/kanit-{sub}-{w}-normal.woff2') format('woff2'); unicode-range: {rng}; }}\n"
    for w in (600, 700)
    for sub, rng in (("thai", "U+02D7, U+0303, U+0331, U+0E01-0E5B, U+200C-200D, U+25CC"),
                     ("latin", "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, "
                               "U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD")))
FNT = 'font-family="Kanit" font-weight="700"' if TH_ else 'font-family="Montserrat" font-weight="800" letter-spacing="0.04em"'

def thai(s):
    s.items[-1] = (s.items[-1].replace('font-family="Montserrat"', 'font-family="Kanit"').replace('font-weight="800"', 'font-weight="700"'))
    s.items[-1] = _re.sub(r'letter-spacing="[^"]*"', 'letter-spacing="0"', s.items[-1])

def tx(s, x, y, text, size=30, col=LBL, op=0, weight=800, anchor="middle", sp=0.06):
    if TH_:
        i = s.label(x, y, text, round(size * 1.08), col, op, 700 if weight >= 700 else 600, 0, anchor); thai(s)
    else:
        i = s.label(x, y, text, size, col, op, weight, sp, anchor)
    return i

def num(s, x, y, text, size, col, op=0, anchor="middle"):
    """Numbers always in Montserrat (digits read the same in both languages)."""
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

def stamp(s, cx, cy, w, h, size, rot):
    """the gold NO stamp (Kanit for Thai)"""
    return s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 18px rgba(232,194,106,0.85))"><g transform="rotate({rot} {cx} {cy})">'
                 f'<path d="{rrect(cx - w // 2, cy - h // 2, w, h, 22)}" fill="rgba(20,17,10,0.85)" stroke="{GOLD}" stroke-width="9"/>'
                 f'<text x="{cx}" y="{cy + size * 0.36:.0f}" text-anchor="middle" {FNT} font-size="{size}" fill="{GOLD}">{X("no")}</text></g></g>', "ns")

# 1  "Most of trading isn't about what you do. It's about what you refuse to do."
s = S(0, K("tempt") - 0.1, first=True)
toplab(s, X("h_s"), X("h_b"), 0, K("refuse") - 0.1, WHITE, LBL, 64, op=1)
toplab(s, X("r_s"), X("r_b"), K("refuse"), K("tempt") - 0.1, GOLD, LBL, 64)
s.spot(540, 1, "232,194,106", 30, 150)
s.fig(540, 1.0, GOLD, 1)
ring = s.path("M 540 950 A 175 175 0 1 1 539 950", GOLD, 5, style="filter:drop-shadow(0 0 12px rgba(232,194,106,0.9))")
s.draw(ring, K("refuse") + 0.4, 0.9); cue(K("refuse") + 0.4, "swell_1", -22)

# 2  "The market will tempt you in three ways."
s = S(K("tempt") - 0.1, K("one") - 0.1)
toplab(s, X("tm_s"), X("tm_b"), K("tempt"), K("one") - 0.1, RED, LBL, 66)
s.spot(540, 1, "232,194,106", 30, 150)
s.fig(540, 1.0, GOLD, 1)
for k, (cx, cy) in enumerate(((240, 830), (840, 760), (830, 1030))):
    c = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 16px rgba(255,77,94,0.8))"><path d="{rrect(cx - 80, cy - 55, 160, 110, 20)}" '
              f'fill="#1a0f12" stroke="{RED}" stroke-width="3"/><text x="{cx}" y="{cy + 22}" text-anchor="middle" font-family="Montserrat" '
              f'font-weight="800" font-size="60" fill="{RED}">{k + 1}</text></g>', "tc")
    t = K("tempt") + 0.5 + k * 0.3
    s.pop(c, t, 0.4, 0.5, "50% 50%"); cue(t, "pop_" + str(k + 1), -20)
    tl(f'tl.to("#{c}", {{y: -12, duration: 0.9, yoyo: true, repeat: 3, ease: "sine.inOut"}}, {t + 0.4:.3f});')

# 3-5  the three temptations, each answered with a NO
def temptation(n, ks, ke, ground_kw):
    s = S(K(ks) - 0.1, K(ke) - 0.1, ground=False, **ground_kw)
    q, no, alt, altb = f"q{n}", f"no{n}", f"alt{n}", f"alt{n}b"
    toplab(s, f'{X("tn")} {n}/3', X(f"t{n}b"), K(ks), K(no) - 0.1, RED, LBL, 56)
    toplab(s, X("sn"), X(f"a{n}"), K(no), K(ke) - 0.1, GOLD, GOLD, 50 if n > 1 else 64, tb=K(alt))
    cd = s.raw(f'<path id="@ID@" d="{rrect(150, 660, 780, 300, 26)}" fill="#1a0f12" stroke="{RED}" stroke-width="3" '
               f'style="opacity:0;filter:drop-shadow(0 0 16px rgba(255,77,94,0.55))"/>', "cd")
    s.pop(cd, K(ks) + 0.15, 0.4, 0.7, "50% 50%")
    qt = tx(s, 540, 750, X(q), 40, WHITE, 0, 800, sp=0.03); s.fade(qt, K(q), 0.3)
    icons = []
    if n == 1:
        ic = tx(s, 600, 900, X("i1"), 64, RED, 0, 800, sp=0.03); icons.append(ic)
        ar = s.path("M 300 920 L 340 860 L 370 885 L 420 800 M 396 802 L 422 798 L 424 826", RED, 6); icons.append(ar)
    elif n == 2:
        for j, x in enumerate((420, 540, 660)):
            xx = s.path(f"M {x - 30} 840 L {x + 30} 900 M {x + 30} 840 L {x - 30} 900", RED, 9); icons.append(xx)
    else:
        bt = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(450, 830, 180, 80, 40)}" fill="{RED}" style="filter:drop-shadow(0 0 14px rgba(255,77,94,0.9))"/>'
                   f'<text x="540" y="884" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="40" fill="#fff">BUY</text></g>', "by")
        icons.append(bt)
    for j, i in enumerate(icons):
        t = K(q) + 0.3 + j * 0.25
        if i.startswith("p"):
            s.draw(i, t, 0.3)
        else:
            s.pop(i, t, 0.35, 0.6, "50% 50%")
    if n == 3:
        tl(f'tl.fromTo("#{icons[0]}", {{scale: 1}}, {{scale: 1.1, transformOrigin: "50% 50%", duration: 0.28, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}}, {K(q) + 0.7:.3f});')
    cue(K(q) + 0.3, "tick_" + str(n), -22)
    st = stamp(s, 540, 810, 400, 190, 150 if not TH_ else 140, -9)
    t_hit = K(no)
    tl(f'tl.fromTo("#{st}", {{opacity: 0, scale: 2.4, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.22, ease: "power4.in", immediateRender: false}}, {t_hit - 0.22:.3f});')
    cue(t_hit, "land_1", -14)
    for i in [cd, qt] + icons:
        tl(f'tl.to("#{i}", {{opacity: 0.25, duration: 0.3}}, {t_hit + 0.1:.3f});')
    tl(f'tl.fromTo("#{cd}", {{x: 0}}, {{x: 8, duration: 0.05, yoyo: true, repeat: 5, immediateRender: false}}, {t_hit:.3f});')
    ta = K(alt) + 0.2
    if n == 1:
        ch = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 14px rgba(232,194,106,0.9))"><circle cx="330" cy="1120" r="62" fill="#14110a" stroke="{GOLD}" stroke-width="5"/>'
                   f'<text x="330" y="1136" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="40" fill="{GOLD}">1%</text></g>', "ch")
        s.pop(ch, ta, 0.4, 0.5, "50% 50%")
        lb = tx(s, 420, 1134, X("a1s"), 40, GOLD, 0, 800, "start", sp=0.04)
    elif n == 2:
        for j, x in enumerate((210, 450, 690)):
            sq = f"M {x + 16} 1122 L {x + 52} 1090 L {x + 78} 1110 L {x + 108} 1082 L {x + 160} 1100"
            tile = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 10px rgba(232,194,106,0.7))"><path d="{rrect(x, 1060, 180, 100, 16)}" fill="#14110a" stroke="{GOLD}" stroke-width="3"/>'
                         f'<path d="{sq}" fill="none" stroke="{GOLD}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></g>', "st")
            s.pop(tile, ta + j * 0.25, 0.35, 0.6, "50% 50%")
        lb = tx(s, 540, 1230, X("a2s"), 36, GOLD, 0, 800, sp=0.06)
    else:
        ck = s.raw(f'<g id="@ID@" style="opacity:0"><circle cx="300" cy="1110" r="56" fill="#0f1319" stroke="#c9ced6" stroke-width="4"/>'
                   f'<line x1="300" y1="1110" x2="300" y2="1074" stroke="{GOLD}" stroke-width="5" stroke-linecap="round"/>'
                   f'<line x1="300" y1="1110" x2="330" y2="1122" stroke="#fff" stroke-width="4" stroke-linecap="round"/></g>', "ck")
        s.pop(ck, ta, 0.35, 0.6, "50% 50%")
        ap = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 16px rgba(232,194,106,0.9))"><path d="{rrect(420, 1050, 360, 120, 20)}" fill="#14110a" stroke="{GOLD}" stroke-width="4"/>'
                   f'<text x="600" y="1132" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="64" fill="{GOLD}">A+</text></g>', "ap")
        s.pop(ap, ta + 0.4, 0.4, 0.6, "50% 50%")
        lb = tx(s, 540, 1240, X("a3s"), 30, GOLD, 0, 800, sp=0.05)
    s.fade(lb, K(alt) + 0.6, 0.35)
    cue(ta, "bell_" + ("C5", "E5", "G5")[n - 1], -18)

temptation(1, "one", "two", dict(restore=False))
temptation(2, "two", "three", dict(hide=False, restore=False))
temptation(3, "three", "noa", dict(hide=False))

# 6  "No. No. And no. That's the job."
s = S(K("noa") - 0.1, K("order") + 0.35)
toplab(s, "", X("job"), K("job"), K("order") + 0.35, GOLD, LBL, 66)
sp6 = s.spot(540, 0, "232,194,106", 30, 150); s.fade(sp6, K("job"), 0.5)
f6 = s.fig(540, 1.0, GOLD); s.pop(f6, K("noa"), 0.4)
for k, (key, cx, rot) in enumerate((("noa", 250, -8), ("nob", 540, 4), ("noc", 830, -5))):
    b = stamp(s, cx, 780, 230, 120, 86 if not TH_ else 80, rot)
    tl(f'tl.fromTo("#{b}", {{opacity: 0, scale: 2.0, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.2, ease: "power4.in", immediateRender: false}}, {K(key) - 0.2:.3f});')
    cue(K(key), "tock_1", -16)
cue(K("job"), "bell_A4", -18)

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
    <div id="root" data-composition-id="otm-sayno-th" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
{TIMELINE}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-sayno-th-audio" class="clip" src="assets/audio/mix_sayno_th.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-sayno-th"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
