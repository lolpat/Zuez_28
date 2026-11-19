"""OTM "The Skill of Doing Nothing": a glowing-figure trading video in the OTM style, inspired by an interview clip
about profitable traders being able to do nothing. The rarest skill in trading is doing nothing: a good trader can watch
the chart for two hours, see nothing worth taking and close the screen. Most traders can't; at the chart they feel they
should be in a trade, so they force entries, take B-grade setups and trade out of boredom. That's activity, not
progress. The market doesn't pay you for being busy; it pays you for being picky. Some days the best trade is the one
you don't take. English version (Quentin); otm-nothing-th is the Thai version from the same scene file. Original
script, voice only, no music. Scenes key off word indices of work/words.json (anchor table EN_ANC, helper K). Writes
../index.html, work/cues.json and work/timing.json."""
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

LANG = "en"
# ---- shared scenes for "The Skill of Doing Nothing" (English: otm-nothing, Thai: otm-nothing-th); LANG is set just above this line
def ix(i):
    return W(i)

TH_ = LANG == "th"
# EN: word indices of work/words.json; TH: token indices of work/script.txt (aligned into work/words.json)
EN_ANC = dict(nothing=5, watch=7, seenothing=17, close=21, most=25, atchart=28, force=41, bgrade=45, bored=51, activity=56,
              notprog=58, market=61, picky=(69, 0.2), somedays=75, oneyou=82, order=88, dont=91, follow=97)
TH_ANC = dict(nothing=1, watch=2, seenothing=4, close=5, most=6, atchart=7, force=9, bgrade=10, bored=11, activity=12,
              notprog=13, market=14, picky=15, somedays=16, oneyou=(18, -0.55), order=19, dont=22, follow=23)

def K(key):
    a = (TH_ANC if TH_ else EN_ANC)[key]
    return ix(a[0]) + a[1] if isinstance(a, tuple) else ix(a)

TXT = dict(
    r_s=("THE RAREST SKILL IN TRADING", "ทักษะที่หายากที่สุดในการเทรด"), r_b=("DOING NOTHING", "การไม่ทำอะไรเลย"),
    today=("TRADES TODAY", "เทรดวันนี้"),
    w_s=("A GOOD TRADER CAN WATCH", "เทรดเดอร์ที่ดี นั่งดูกราฟได้"), w_b=("FOR 2 HOURS", "สองชั่วโมง"),
    s_s=("SEE NOTHING WORTH TAKING", "ไม่เจออะไรที่น่าเข้า"), s_b=("AND CLOSE THE SCREEN", "แล้วก็ปิดจอไป"),
    m_b=("MOST TRADERS CAN'T.", "ส่วนใหญ่ทำไม่ได้"),
    a_s=("IF THEY'RE AT THE CHART", "ถ้านั่งหน้ากราฟ"), a_b=("THEY FEEL THEY MUST TRADE", "ก็รู้สึกว่าต้องมีออเดอร์"),
    urge=("URGE", "อยากเข้า"),
    f1=("FORCED ENTRY", "ฝืนเข้าเทรด"), f2=("B-GRADE SETUP", "เซ็ตอัพแค่พอใช้"), f3=("BORED TRADE", "เทรดเพราะเบื่อ"),
    ac_s=("THAT'S ACTIVITY.", "นั่นคือความยุ่ง"), ac_b=("NOT PROGRESS.", "ไม่ใช่ความก้าวหน้า"),
    act=("ACTIVITY", "ความยุ่ง"), prog=("PROGRESS", "ความก้าวหน้า"),
    mk_s=("THE MARKET DOESN'T PAY YOU FOR", "ตลาดไม่ได้จ่ายเงินให้"), mk_b=("BEING BUSY", "คนที่ยุ่ง"),
    pk_s=("IT PAYS YOU FOR", "แต่จ่ายให้"), pk_b=("BEING PICKY", "คนที่เลือก"),
    sd_s=("SOME DAYS, THE BEST TRADE", "บางวัน เทรดที่ดีที่สุด"), sd_b=("IS THE ONE YOU DON'T TAKE", "คือเทรดที่คุณไม่ได้เข้า"),
    skip=("SKIPPED", "ไม่เข้า"),
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

def monitor(s, op=1):
    return s.raw(f'<g id="@ID@" style="opacity:{op}"><path d="{rrect(520, 760, 440, 300, 18)}" fill="#0f1319" stroke="#ffffffb0" stroke-width="3"/>'
                 f'<line x1="740" y1="1060" x2="740" y2="1236" stroke="#ffffff80" stroke-width="6"/>'
                 f'<line x1="680" y1="1236" x2="800" y2="1236" stroke="#ffffff80" stroke-width="6" stroke-linecap="round"/></g>', "mn")

CHOP = [(545, 920), (585, 895), (620, 930), (655, 900), (690, 925), (725, 890), (760, 922), (795, 897), (830, 928), (865, 902), (900, 924), (935, 905)]
CHOP_D = "M " + " L ".join(f"{x} {y}" for x, y in CHOP)

# 1  "The rarest skill in trading? Doing nothing."
s = S(0, K("watch") - 0.1, first=True)
a1 = tx(s, 540, 488, X("r_s"), 28, LBL, 1, 700, sp=0.12)
b1 = tx(s, 540, 560, X("r_b"), 66, GOLD, 0, 800, sp=0.04); s.fade(b1, K("nothing"), 0.3, y=10)
for i in (a1, b1):
    tl(f'tl.to("#{i}", {{opacity: 0, duration: 0.15}}, {K("watch") - 0.27:.3f});')
sp1 = s.spot(540, 1, "232,194,106", 30, 150)
f1 = s.fig(540, 1.0, GOLD, 1)
cc = s.raw(f'<path id="@ID@" d="{rrect(390, 740, 300, 180, 22)}" fill="#14110a" stroke="{GOLD}" stroke-width="3" '
           f'style="opacity:0;filter:drop-shadow(0 0 14px rgba(232,194,106,0.5))"/>', "cc")
cl = tx(s, 540, 790, X("today"), 28, LBL, 0, 700, sp=0.1)
c0 = num(s, 540, 892, "0", 84, GOLD)
s.pop(cc, K("nothing") + 0.2, 0.4, 0.6, "50% 50%"); s.fade(cl, K("nothing") + 0.3, 0.3)
s.pop(c0, K("nothing") + 0.45, 0.4, 0.3, "50% 50%"); cue(K("nothing") + 0.45, "bell_C5", -18)

# 2  "A good trader can watch the chart for two hours... see nothing worth taking... and close the screen."
s = S(K("watch") - 0.1, K("most") - 0.1)
toplab(s, X("w_s"), X("w_b"), K("watch"), K("seenothing") - 0.1, WHITE, LBL, 62)
toplab(s, X("s_s"), X("s_b"), K("seenothing"), K("most") - 0.1, GOLD, LBL, 52)
mn = monitor(s)
ch = s.path(CHOP_D, "#c9ced6", 4); s.draw(ch, K("watch") + 0.1, max(1.0, K("seenothing") + 0.4 - K("watch")), "none")
clk = s.raw(f'<g id="@ID@"><circle cx="250" cy="830" r="62" fill="#0f1319" stroke="#c9ced6" stroke-width="4"/>'
            f'<circle cx="250" cy="830" r="5" fill="#c9ced6"/></g>', "ck")
hh = s.raw(f'<line id="@ID@" x1="250" y1="830" x2="250" y2="796" stroke="{GOLD}" stroke-width="6" stroke-linecap="round"/>', "hh")
mh = s.raw(f'<line id="@ID@" x1="250" y1="830" x2="250" y2="782" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>', "mh")
t_c0, t_c1 = K("watch") + 0.1, K("seenothing") + 0.2
tl(f'tl.fromTo("#{hh}", {{rotation: 0}}, {{rotation: 60, svgOrigin: "250 830", duration: {t_c1 - t_c0:.3f}, ease: "power1.inOut", immediateRender: false}}, {t_c0:.3f});')
tl(f'tl.fromTo("#{mh}", {{rotation: 0}}, {{rotation: 720, svgOrigin: "250 830", duration: {t_c1 - t_c0:.3f}, ease: "power1.inOut", immediateRender: false}}, {t_c0:.3f});')
cue(t_c0, "tick_1", -24)
f2 = s.fig(250, 1.0, GOLD, 1)
for k, x in enumerate((620, 740, 860)):
    m = s.path(f"M {x - 14} 830 L {x + 14} 858 M {x + 14} 830 L {x - 14} 858", "#7d838c", 5)
    s.draw(m, K("seenothing") + 0.25 + k * 0.3, 0.15); cue(K("seenothing") + 0.25 + k * 0.3, "tick_" + str(k + 1), -24)
off = s.raw(f'<path id="@ID@" d="{rrect(523, 763, 434, 294, 16)}" fill="#000000" style="opacity:0"/>', "of")
s.fade(off, K("close") + 0.1, 0.35, 0.92); cue(K("close") + 0.1, "click_2", -18)
s.walk(f2, K("close") + 0.5, -150, 1.1)

# 3  "Most traders can't. If they're at the chart, they feel they should be in a trade."
s = S(K("most") - 0.1, K("force") - 0.1)
toplab(s, "", X("m_b"), K("most"), K("atchart") - 0.1, RED, LBL, 62)
toplab(s, X("a_s"), X("a_b"), K("atchart"), K("force") - 0.1, WHITE, LBL, 46)
monitor(s)
ch3 = s.path(CHOP_D, "#c9ced6", 4, drawn=True)
f3 = s.fig(330, 1.0, WHITE, 1)
tl(f'tl.to("#{f3}", {{x: 6, duration: 0.09, yoyo: true, repeat: {int((K("force") - K("most")) / 0.18) * 2 - 1}, ease: "sine.inOut"}}, {K("most") + 0.2:.3f});')
bt = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(810, 990, 120, 50, 25)}" fill="{RED}" style="filter:drop-shadow(0 0 12px rgba(255,77,94,0.9))"/>'
           f'<text x="870" y="1025" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" fill="#fff">BUY</text></g>', "bt")
s.pop(bt, K("atchart"), 0.35, 0.5, "50% 50%")
tl(f'tl.fromTo("#{bt}", {{scale: 1}}, {{scale: 1.12, transformOrigin: "50% 50%", duration: 0.3, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false}}, {K("atchart") + 0.4:.3f});')
cue(K("atchart"), "pop_1", -20)
ul = tx(s, 165, 890, X("urge"), 28, RED, 0, 800, sp=0.1); s.fade(ul, K("most") + 0.2, 0.3)
s.raw(f'<rect id="@ID@" x="148" y="910" width="34" height="320" rx="17" fill="#1d2229"/>', "ut")
uf = s.raw(f'<rect id="@ID@" x="148" y="1230" width="34" height="0" rx="17" fill="{RED}" style="filter:drop-shadow(0 0 8px rgba(255,77,94,0.8))"/>', "uf")
tl(f'tl.fromTo("#{uf}", {{attr: {{y: 1230, height: 0}}}}, {{attr: {{y: 920, height: 310}}, duration: {K("force") - 0.3 - K("most"):.3f}, ease: "power1.in", immediateRender: false}}, {K("most") + 0.2:.3f});')
cue(K("most") + 0.2, "swell_2", -24)

# 4  "So they force entries. They take the B-grade setup. They trade because they're bored."
s = S(K("force") - 0.1, K("activity") - 0.1, ground=False, restore=False)
tdl = tx(s, 540, 488, X("today"), 28, LBL, 0, 700, sp=0.12); s.fade(tdl, K("force"), 0.3)
cnt = []
for k in range(3):
    c = num(s, 540, 572, str(k + 1), 72, RED); cnt.append(c)
for k, (key, k_) in enumerate((("f1", "force"), ("f2", "bgrade"), ("f3", "bored"))):
    t = K(k_)
    tl(f'tl.fromTo("#{cnt[k]}", {{opacity: 0, scale: 1.4, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.8)", immediateRender: false}}, {t:.3f});')
    if k < 2:
        tl(f'tl.set("#{cnt[k]}", {{opacity: 0}}, {K(("bgrade", "bored")[k]):.3f});')
    y = 720 + k * 170
    cd = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(150, y - 62, 780, 124, 22)}" fill="#1a0f12" stroke="{RED}" stroke-width="3"/>'
               f'<path d="M 790 {y - 30} L 820 {y - 10} L 845 {y - 20} L 880 {y + 28}" fill="none" stroke="{RED}" stroke-width="5" '
               f'stroke-linecap="round" stroke-linejoin="round"/><path d="M 862 {y + 24} L 882 {y + 30} L 884 {y + 10}" fill="none" '
               f'stroke="{RED}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></g>', "fc")
    ft = tx(s, 195, y + 13, X(key), 38, WHITE, 0, 800, "start", sp=0.04)
    s.pop(cd, t, 0.35, 0.7, "50% 50%"); s.fade(ft, t + 0.05, 0.3); cue(t, "tock_1", -18)

# 5  "That's activity. It isn't progress."
s = S(K("activity") - 0.1, K("market") - 0.1, ground=False, hide=False, restore=False)
toplab(s, X("ac_s"), X("ac_b"), K("activity"), K("market") - 0.1, WHITE, LBL, 62, tb=K("notprog"))
for j, (lab, col, t, full, pct) in enumerate((("act", RED, K("activity") + 0.2, 780, "100%"), ("prog", GOLD, K("notprog") + 0.2, 26, "0%"))):
    y = 780 + j * 200
    l = tx(s, 150, y, X(lab), 34, LBL, 0, 800, "start", sp=0.1); s.fade(l, t - 0.2, 0.3)
    s.raw(f'<rect x="150" y="{y + 26}" width="780" height="56" rx="28" fill="#1d2229"/>', "bt")
    fb = s.raw(f'<rect id="@ID@" x="150" y="{y + 26}" width="0" height="56" rx="28" fill="{col}" style="filter:drop-shadow(0 0 10px {col})"/>', "fb")
    tl(f'tl.fromTo("#{fb}", {{attr: {{width: 0}}}}, {{attr: {{width: {full}}}, duration: {0.9 if j == 0 else 0.5}, ease: "power2.out", immediateRender: false}}, {t:.3f});')
    pv = num(s, 930, y, pct, 36, col if j == 0 else GREY, 0, "end"); s.fade(pv, t + 0.5, 0.3)
    cue(t, "swell_1" if j == 0 else "tock_1", -22 if j == 0 else -18)

# 6  "The market doesn't pay you for being busy. It pays you for being picky."
s = S(K("market") - 0.1, K("somedays") - 0.1, ground=False, hide=False)
toplab(s, X("mk_s"), X("mk_b"), K("market"), K("picky") - 0.1, RED, LBL, 62)
toplab(s, X("pk_s"), X("pk_b"), K("picky"), K("somedays") - 0.1, GOLD, LBL, 62)
PICK = (7, 16)
for k in range(20):
    x, y = 125 + (k % 5) * 170, 680 + (k // 5) * 125
    sq = f"M {x + 18} {y + 70} L {x + 50} {y + 40} L {x + 74} {y + 58} L {x + 100} {y + 30} L {x + 132} {y + 46}"
    tb_ = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(x, y, 150, 100, 14)}" fill="#0f1319" stroke="#ffffff40" stroke-width="2"/>'
                f'<path d="{sq}" fill="none" stroke="#7d838c" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></g>', "gt")
    s.fade(tb_, K("market") + 0.1 + (k % 5) * 0.04 + (k // 5) * 0.06, 0.25)
    rd = s.raw(f'<path id="@ID@" d="{rrect(x, y, 150, 100, 14)}" fill="{RED}" fill-opacity="0.12" stroke="{RED}" stroke-width="3" style="opacity:0"/>', "rd")
    t = K("market") + 0.5 + k * 0.03
    tl(f'tl.fromTo("#{rd}", {{opacity: 0}}, {{opacity: 1, duration: 0.12, immediateRender: false}}, {t:.3f});')
    hide(rd, K("picky") - 0.3, 0.25)
    if k in PICK:
        gd = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 14px rgba(232,194,106,0.9))"><path d="{rrect(x, y, 150, 100, 14)}" fill="#14110a" stroke="{GOLD}" stroke-width="4"/>'
                   f'<path d="{sq}" fill="none" stroke="{GOLD}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
                   f'<path d="M {x + 112} {y + 80} L {x + 122} {y + 90} L {x + 140} {y + 70}" fill="none" stroke="{GOLD}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></g>', "gd")
        s.pop(gd, K("picky") + 0.15 + PICK.index(k) * 0.25, 0.35, 0.7, "50% 50%")
        cue(K("picky") + 0.15 + PICK.index(k) * 0.25, "bell_G5" if PICK.index(k) else "bell_E5", -20)
    else:
        hide(tb_, K("picky"), 0.4, 0.25)
cue(K("market") + 0.5, "tick-crisp_1", -22); cue(K("market") + 0.8, "tick-crisp_2", -22)

# 7  "Some days, the best trade you make... is the one you don't take."
s = S(K("somedays") - 0.1, K("order") + 0.35)
toplab(s, X("sd_s"), X("sd_b"), K("somedays"), K("order") + 0.35, GOLD, LBL, 44, tb=K("oneyou"))
f7 = s.fig(250, 1.0, GOLD); s.pop(f7, K("somedays"), 0.4)
pn = s.raw(f'<path id="@ID@" d="{rrect(420, 720, 540, 440, 20)}" fill="#0f1319" stroke="#ffffff50" stroke-width="2" style="opacity:0"/>', "pn")
s.fade(pn, K("somedays") + 0.05, 0.35)
p1 = s.path("M 450 1060 L 520 1000 L 575 1030 L 640 950 L 690 985 L 740 930", "#c9ced6", 5); s.draw(p1, K("somedays") + 0.2, 0.9)
gl = s.raw(f'<line id="@ID@" x1="740" y1="930" x2="940" y2="930" stroke="#c9ced6" stroke-width="3" stroke-dasharray="10 9" style="opacity:0"/>', "gl")
s.fade(gl, K("somedays") + 1.0, 0.3)
p2 = s.path("M 740 930 L 790 985 L 830 965 L 880 1060 L 930 1120", RED, 5, style="filter:drop-shadow(0 0 8px rgba(255,77,94,0.8))")
s.draw(p2, K("oneyou") + 0.1, 0.6); cue(K("oneyou") + 0.1, "whoosh-short_2", -22)
bd = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 14px rgba(232,194,106,0.8))"><path d="{rrect(560, 770, 260, 70, 35)}" fill="#14110a" stroke="{GOLD}" stroke-width="3"/>'
           f'<path d="M 590 806 L 603 819 L 626 793" fill="none" stroke="{GOLD}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></g>', "bd")
bdt = tx(s, 720, 817, X("skip"), 30, GOLD, 0, 800, sp=0.08)
s.pop(bd, K("oneyou") + 0.7, 0.4, 0.6, "50% 50%"); s.fade(bdt, K("oneyou") + 0.8, 0.3); cue(K("oneyou") + 0.7, "bell_E5", -18)

# 8  outro (handles, no end card; brand lines stay in English)
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
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="otm-nothing" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
{TIMELINE}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-nothing-audio" class="clip" src="assets/audio/mix_nothing.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-nothing"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
