"""OTM "Don't Stop Now": a glowing-figure motivation video for traders in the OTM style, inspired by a motivational
talk clip ("you're one win away... don't stop now"). Its twist: you're not one lucky trade away, you're one habit away,
one rule you finally keep. The hardest part is behind you (you started, one step at a time); the hard stretch (losing
weeks, doubt, silence) is a test, and tests are temporary. Traders who make it find a way: one more chart, one more
lesson, one more day of discipline, however long it takes. Keep stacking the steps and the future you're building
meets you halfway. English version (Quentin); otm-dontstop-th is the Thai version from the same scene file.
Original script, voice only, no music.
Scenes key off word indices of work/words.json (anchor table ANC, helper K). Writes ../index.html, work/cues.json and
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

LANG = "en"
# ---- shared scenes for "Don't Stop Now" (English: otm-dontstop, Thai: otm-dontstop-th); LANG is set just above this line
def ix(i):
    return W(i)

TH_ = LANG == "th"
ANC = dict(
    close=(0, 0), notlucky=(7, 1), habit=(12, 2), rule=(15, 3), whatever=(20, 5), dontstop=(24, 7), hardest=(27, 8),
    started=(34, 10), kept=(36, 11), step=(39, 12), hard=(44, 13), losing=(49, 15), doubt=(51, 16), silence=(52, 17),
    test=(53, 18), temporary=(58, 19), traders=(62, 21), findway=(70, 23), chart=(74, 24), lesson=(77, 25), day=(80, 26),
    howlong=(85, 27), stacking=(92, 29), future=(96, 30), halfway=(104, 31), dontstop2=(105, 32), order=(108, 33),
    dont=(111, 36), follow=(117, 37))

def K(key):
    a = ANC[key][1 if TH_ else 0]
    return ix(a[0]) + a[1] if isinstance(a, tuple) else ix(a)

TXT = dict(
    t1=("YOU MIGHT BE", "คุณอาจ"), t2=("CLOSER THAN YOU THINK", "ใกล้กว่าที่คิด"),
    luck_s=("NOT ONE", "ไม่ใช่ห่างแค่"), luck_b=("LUCKY TRADE AWAY", "เทรดดวงดีไม้เดียว"), lucky=("LUCKY TRADE", "เทรดดวงดี"),
    habit_s=("ONE HABIT AWAY", "แต่ห่างแค่นิสัยเดียว"), habit_b=("ONE RULE YOU FINALLY KEEP", "กฎข้อเดียวที่ทำได้จริง"),
    c1=("1 HABIT", "1 นิสัย"), c2=("1 RULE", "1 กฎ"),
    stop_s=("SO WHATEVER YOU DO", "ไม่ว่าจะเกิดอะไรขึ้น"), stop_b=("DON'T STOP NOW", "อย่าหยุดตอนนี้"),
    hard_s=("THE HARDEST PART IS", "ส่วนที่ยากที่สุด"), hard_b=("ALREADY BEHIND YOU", "คุณผ่านมาแล้ว"),
    step_s=("YOU STARTED. YOU KEPT GOING", "คุณเริ่มต้น แล้วก็เดินต่อ"), step_b=("ONE STEP AT A TIME", "ทีละก้าว"),
    started=("STARTED", "เริ่มต้น"),
    rough_s=("YES,", "ใช่"), rough_b=("THIS STRETCH IS HARD", "ช่วงนี้มันยาก"),
    w1=("LOSING WEEKS", "ขาดทุนหลายสัปดาห์"), w2=("DOUBT", "ความสงสัย"), w3=("SILENCE", "ความเงียบ"),
    test_s=("BUT THAT'S JUST", "แต่นั่นเป็นแค่"), test_b=("A TEST", "บททดสอบ"),
    temp_s=("AND TESTS ARE", "และบททดสอบ"), temp_b=("TEMPORARY", "เป็นเรื่องชั่วคราว"),
    easy_s=("TRADERS WHO MAKE IT", "เทรดเดอร์ที่ไปถึงฝั่ง"), easy_b=("DON'T WAIT FOR EASY", "ไม่รอให้ทุกอย่างง่าย"),
    way_b=("THEY FIND A WAY", "พวกเขาหาทางจนเจอ"),
    p1=("+1 CHART", "+1 กราฟ"), p2=("+1 LESSON", "+1 บทเรียน"), p3=("+1 DAY OF DISCIPLINE", "+1 วันที่มีวินัย"),
    long_s=("IT DOESN'T MATTER", "จะใช้เวลานานแค่ไหน"), long_b=("HOW LONG IT TAKES", "ก็ไม่สำคัญ"),
    dayw=("DAY", "วันที่"),
    stack_s=("KEEP STACKING", "ก้าวต่อไป"), stack_b=("THE STEPS", "ทีละขั้น"),
    fut_s=("THE FUTURE YOU'RE BUILDING", "แล้วอนาคตที่คุณสร้าง"), fut_b=("WILL MEET YOU HALFWAY", "จะเดินมาเจอคุณครึ่งทาง"),
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

def pill(s, x, y, text, fill, tcol, size, op=0):
    i = s.pill(x, y, text, fill, tcol, size, op)
    if TH_: thai(s)
    return i

def toplab(s, small, big, t0, t1, bcol=WHITE, scol=LBL, bsize=52, y=560):
    ids = []
    if small:
        a = tx(s, 540, y - 72, small, 28, scol, 0, 700, sp=0.12); ids.append(a)
    b = tx(s, 540, y, big, bsize, bcol, 0, 800, sp=0.04); ids.append(b)
    for i in ids:
        s.fade(i, t0, 0.3, y=10)
        tl(f'tl.to("#{i}", {{opacity: 0, duration: 0.15}}, {t1 - 0.17:.3f});')
    return ids

def hide(i, t, d=0.3, to=0):
    tl(f'tl.to("#{i}", {{opacity: {to}, duration: {d}}}, {t:.3f});')

SX0, SW, SH, SN = 150, 110, 58, 7          # the staircase: 7 blocks rising to the right
def step_xy(i):
    return SX0 + i * SW + SW / 2, GY - (i + 1) * SH

def stairs(s, op=1, t=None, stag=0.12, top_glow=True):
    ids = []
    for i in range(SN):
        x, y = SX0 + i * SW, GY - (i + 1) * SH
        last = top_glow and i == SN - 1
        st = s.raw(f'<rect id="@ID@" x="{x}" y="{y}" width="{SW}" height="{(i + 1) * SH}" fill="{"#3a2f14" if last else "#12161c"}" '
                   f'stroke="{GOLD if last else "#ffffff70"}" stroke-width="2.5" style="opacity:{op}"/>', "stp")
        if t is not None: s.pop(st, t + i * stag, 0.3, 0.3, "50% 100%")
        ids.append(st)
    return ids

def flag(s, x, base=GY, op=0, col=GOLD, k=1.0):
    return s.raw(f'<g id="@ID@" style="opacity:{op};filter:drop-shadow(0 0 14px rgba(232,194,106,0.8))">'
                 f'<rect x="{x - 3}" y="{base - 200 * k:.0f}" width="6" height="{200 * k:.0f}" fill="{col}"/>'
                 f'<path d="M {x + 3} {base - 200 * k:.0f} L {x + 95 * k:.0f} {base - 174 * k:.0f} L {x + 3} {base - 146 * k:.0f} Z" fill="{col}"/></g>', "fg")

# 1  "You might be closer than you think."
s = S(0, K("notlucky") - 0.1, first=True)
tx(s, 540, 486, X("t1"), 44, LBL, 1, 700, sp=0.08)
tx(s, 540, 572, X("t2"), 60, GOLD, 1, 800, sp=0.04)
stairs(s, 1)
fx, fy = step_xy(SN - 1)
fl1 = flag(s, fx, fy, 1, k=0.9)
px, py = step_xy(4)
f1 = s.fig(px, 0.7, WHITE, 1, gy=py)
gl = s.raw(f'<circle id="@ID@" cx="{fx}" cy="{fy - 80}" r="120" fill="{GOLD}" fill-opacity="0.12" style="filter:blur(20px)"/>', "gw")
tl(f'tl.fromTo("#{gl}", {{opacity: 0.5}}, {{opacity: 1, duration: 1.2, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false}}, 0.2);')
cue(0.3, "swell_1", -24)

# 2  "Not one lucky trade away. One habit away. One rule you finally keep."
s = S(K("notlucky") - 0.1, K("whatever") - 0.1, ground=False, restore=False)
toplab(s, X("luck_s"), X("luck_b"), K("notlucky"), K("habit") - 0.1, RED, LBL, 56)
pips = "".join(f'<circle cx="{540 + dx}" cy="{850 + dy}" r="12" fill="#0b0b0b"/>' for dx, dy in [(-42, -42), (42, -42), (0, 0), (-42, 42), (42, 42)])
dice = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(450, 760, 180, 180, 30)}" fill="#f4f4f2"/>{pips}</g>', "di")
s.pop(dice, K("notlucky"), 0.4, 0.5, "50% 50%"); cue(K("notlucky"), "pop_1", -20)
tl(f'tl.fromTo("#{dice}", {{rotation: -14}}, {{rotation: 14, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut", svgOrigin: "540 850", immediateRender: false}}, {K("notlucky") + 0.3:.3f});')
dl = tx(s, 540, 1000, X("lucky"), 30, LBL, 0, 800, sp=0.12); s.fade(dl, K("notlucky") + 0.2, 0.3)
dx_ = s.path("M 430 750 L 650 950 M 650 750 L 430 950", RED, 9); s.draw(dx_, K("habit") - 0.45, 0.35); cue(K("habit") - 0.45, "tock_1", -18)
for i_ in (dice, dl, dx_):
    hide(i_, K("habit") + 0.1, 0.4, 0.15)
toplab(s, X("habit_s"), X("habit_b"), K("habit"), K("whatever") - 0.1, GOLD, LBL, 46)
for j, (key, x, t) in enumerate([("c1", 300, K("habit") + 0.1), ("c2", 780, K("rule"))]):
    cd = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(x - 190, 1040, 380, 180, 24)}" fill="#14110a" stroke="{GOLD}" stroke-width="3"/>'
               f'<text x="{x}" y="{1150 if not TH_ else 1152}" text-anchor="middle" {FNT} font-size="{50 if TH_ else 46}" fill="{GOLD}">{X(key)}</text></g>', "cd")
    s.pop(cd, t, 0.4, 0.6, "50% 50%"); cue(t, "bell_" + ["C5", "E5"][j], -20)

# 3  "So whatever you do... don't stop now."
s = S(K("whatever") - 0.1, K("hardest") - 0.1, ground=False, hide=False)
w3s = tx(s, 540, 760, X("stop_s"), 32, LBL, 0, 700, sp=0.14); s.fade(w3s, K("whatever"), 0.35, y=10)
w3b = tx(s, 540, 870, X("stop_b"), 76, WHITE, 0, 800, sp=0.04)
tl(f'tl.fromTo("#{w3b}", {{opacity: 0, scale: 1.3, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.45, ease: "expo.out", immediateRender: false}}, {K("dontstop") - 0.1:.3f});')
pz = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="490" y="980" width="34" height="120" rx="8" fill="#6b7079"/><rect x="556" y="980" width="34" height="120" rx="8" fill="#6b7079"/></g>', "pz")
s.pop(pz, K("whatever") + 0.3, 0.35, 0.5, "50% 50%")
px3 = s.path("M 460 970 L 620 1110 M 620 970 L 460 1110", RED, 8); s.draw(px3, K("dontstop") + 0.1, 0.3)
hide(pz, K("dontstop") + 0.5, 0.3); hide(px3, K("dontstop") + 0.5, 0.3)
pl3 = s.raw(f'<path id="@ID@" d="M 500 975 L 600 1040 L 500 1105 Z" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 14px rgba(232,194,106,0.9))"/>', "py")
s.pop(pl3, K("dontstop") + 0.6, 0.4, 0.4, "50% 50%")
cue(K("dontstop") - 0.1, "whoosh-short_2", -22); cue(K("dontstop") + 0.1, "tock_1", -18); cue(K("dontstop") + 0.6, "bell_G5", -20)

# 4  "The hardest part is already behind you. You started. You kept going, one step at a time."
s = S(K("hardest") - 0.1, K("hard") - 0.1)
st4 = stairs(s, 0, K("hardest") - 0.05, 0.08)
x0, y0 = step_xy(0)
f4 = s.fig(x0, 0.7, WHITE, gy=y0); s.pop(f4, K("hardest") + 0.4, 0.4)
toplab(s, X("hard_s"), X("hard_b"), K("hardest"), K("started") - 0.1, WHITE, LBL, 56)
toplab(s, X("step_s"), X("step_b"), K("started"), K("hard") - 0.1, GOLD, LBL, 58)
sl4 = tx(s, x0, GY + 50, X("started"), 28, GOLD, 0, 800, sp=0.12); s.fade(sl4, K("started"), 0.3)
lit0 = s.raw(f'<rect id="@ID@" x="{SX0}" y="{GY - SH}" width="{SW}" height="{SH}" fill="{GOLD}" fill-opacity="0.5" style="opacity:0"/>', "lt")
s.fade(lit0, K("started"), 0.3); cue(K("started"), "pop_1", -20)
T0, n_up = K("kept"), 4
dt_ = max(0.45, (K("hard") - 0.6 - T0) / n_up)
for k in range(1, n_up + 1):
    t = T0 + (k - 1) * dt_
    tl(f'tl.to("#{f4}", {{x: {k * SW}, y: {-k * SH}, duration: 0.32, ease: "power2.out"}}, {t:.3f});')
    lt = s.raw(f'<rect id="@ID@" x="{SX0 + k * SW}" y="{GY - (k + 1) * SH}" width="{SW}" height="{SH}" fill="{GOLD}" fill-opacity="0.5" style="opacity:0"/>', "lt")
    s.fade(lt, t + 0.25, 0.3)
    cue(t + 0.25, "tick_" + str((k - 1) % 3 + 1), -20)

# 5  "Yes, this stretch is hard. Losing weeks. Doubt. Silence. But that's just a test. And tests are temporary."
s = S(K("hard") - 0.1, K("traders") - 0.1)
f5 = s.fig(540, 1.0, WHITE); s.pop(f5, K("hard") - 0.05, 0.4)
toplab(s, X("rough_s"), X("rough_b"), K("hard"), K("test") - 0.1, WHITE, LBL, 58)
cid = s.uid("cl"); rid = s.uid("rn")
rain = "".join(f'<line x1="{x}" y1="{y}" x2="{x - 12}" y2="{y + 34}" stroke="#9aa0a8" stroke-width="3" stroke-linecap="round"/>'
               for x in range(400, 700, 34) for y in (900, 960) if (x // 34 + y // 60) % 2 == 0)
s.raw(f'<g id="{cid}" style="opacity:0"><g fill="#3a3f47"><circle cx="470" cy="820" r="60"/><circle cx="545" cy="790" r="78"/><circle cx="625" cy="825" r="58"/>'
      f'<rect x="420" y="820" width="250" height="62" rx="31"/></g><g id="{rid}">{rain}</g></g>', "x")
s.fade(cid, K("hard") + 0.2, 0.5)
tl(f'tl.fromTo("#{rid}", {{y: -10}}, {{y: 26, duration: 0.35, repeat: {int((K("temporary") + 0.8 - K("hard")) / 0.35)}, ease: "none", immediateRender: false}}, {K("hard") + 0.2:.3f});')
cue(K("hard") + 0.2, "swell_2", -26)
for j, (key, x, y, t) in enumerate([("w1", 250, 1000, K("losing")), ("w2", 840, 960, K("doubt")), ("w3", 830, 1110, K("silence"))]):
    wl = tx(s, x, y, X(key), 30, "#c26a74", 0, 800, sp=0.08); s.fade(wl, t - 0.05, 0.3)
    hide(wl, K("test"), 0.4)
    cue(t - 0.05, "tick-crisp_" + str(j + 1), -22)
toplab(s, X("test_s"), X("test_b"), K("test"), K("temporary") - 0.1, GOLD, LBL, 64)
hg = s.raw(f'<g id="@ID@" style="opacity:0"><path d="M 210 980 H 330 L 270 1050 Z M 210 1120 H 330 L 270 1050 Z" fill="none" stroke="{GOLD}" stroke-width="5" stroke-linejoin="round"/>'
           f'<path d="M 245 1105 H 295 L 270 1078 Z" fill="{GOLD}"/></g>', "hg")
s.pop(hg, K("test") + 0.2, 0.4, 0.5, "50% 50%")
tl(f'tl.to("#{hg}", {{rotation: 180, svgOrigin: "270 1050", duration: 0.6, ease: "power2.inOut"}}, {K("temporary") + 0.2:.3f});')
toplab(s, X("temp_s"), X("temp_b"), K("temporary"), K("traders") - 0.1, GOLD, LBL, 64)
tl(f'tl.to("#{cid}", {{x: 520, opacity: 0, duration: 1.2, ease: "power2.in"}}, {K("temporary") + 0.4:.3f});')
sun = s.raw(f'<circle id="@ID@" cx="540" cy="860" r="90" fill="{GOLD}" fill-opacity="0.18" style="opacity:0;filter:blur(16px)"/>', "sn")
s.fade(sun, K("temporary") + 0.9, 0.8)
cue(K("temporary") + 0.4, "whoosh-long_1", -24)

# 6  "Traders who make it don't wait for easy. They find a way. One more chart. One more lesson. One more day of discipline."
s = S(K("traders") - 0.1, K("howlong") - 0.1)
f6 = s.fig(220, 1.0, WHITE); s.pop(f6, K("traders"), 0.4)
wall = s.raw(f'<rect id="@ID@" x="520" y="990" width="44" height="250" rx="8" fill="#3a3f47" stroke="#9aa0a8" stroke-width="3" style="opacity:0"/>', "wa")
s.pop(wall, K("traders") + 0.2, 0.35, 0.2, "50% 100%"); cue(K("traders") + 0.2, "land_1", -18)
toplab(s, X("easy_s"), X("easy_b"), K("traders"), K("findway") - 0.1, WHITE, LBL, 52)
toplab(s, "", X("way_b"), K("findway"), K("howlong") - 0.1, GOLD, LBL, 60)
arc = s.path("M 270 1080 Q 542 760 830 1150", GOLD, 5, extra='stroke-dasharray="14 10"', drawn=True, style="opacity:0")
s.fade(arc, K("findway"), 0.4)
tl(f'tl.to("#{f6}", {{x: 620, duration: 1.1, ease: "power1.inOut"}}, {K("findway") + 0.3:.3f});')
tl(f'tl.to("#{f6}", {{y: -300, duration: 0.55, ease: "sine.out", yoyo: true, repeat: 1}}, {K("findway") + 0.3:.3f});')
cue(K("findway") + 0.3, "whoosh-short_1", -22)
for j, (key, t) in enumerate([("p1", K("chart")), ("p2", K("lesson")), ("p3", K("day"))]):
    p = pill(s, 540, 1330 + j * 72, X(key), GOLD, "#111", 28); s.pop(p, t - 0.05, 0.35, 0.6, "50% 50%")
    cue(t - 0.05, "pop_" + str(j + 1), -20)

# 7  "It doesn't matter how long it takes."
s = S(K("howlong") - 0.1, K("stacking") - 0.1, ground=False)
toplab(s, X("long_s"), X("long_b"), K("howlong"), K("stacking") - 0.1, WHITE, LBL, 60)
cal = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(400, 820, 280, 280, 26)}" fill="#0f1319" stroke="#f4f4f2" stroke-width="4"/>'
            f'<path d="M 400 900 V 846 Q 400 820 426 820 H 654 Q 680 820 680 846 V 900 Z" fill="{GOLD}"/>'
            f'<rect x="460" y="796" width="16" height="50" rx="8" fill="#f4f4f2"/><rect x="604" y="796" width="16" height="50" rx="8" fill="#f4f4f2"/></g>', "ca")
s.pop(cal, K("howlong"), 0.4, 0.6, "50% 50%")
dw = tx(s, 540, 878, X("dayw"), 28, "#111", 0, 800, sp=0.18); s.fade(dw, K("howlong") + 0.1, 0.3)
span = K("stacking") - 0.3 - (K("howlong") + 0.2)
for j, n in enumerate([1, 90, 365]):
    t = K("howlong") + 0.2 + j * span / 3
    nl = tx(s, 540, 1045, str(n), 96, WHITE, 0, 800, sp=0.02)
    s.fade(nl, t, 0.12)
    if j < 2: hide(nl, t + span / 3 - 0.05, 0.08)
    cue(t, "click_" + str(j % 2 + 1), -22)

# 8  "Keep stacking the steps, and the future you're building will meet you halfway."
s = S(K("stacking") - 0.1, K("dontstop2") - 0.1)
st8 = stairs(s, 0, K("stacking"), 0.22)
cue(K("stacking"), "tick_1", -22); cue(K("stacking") + 0.66, "tick_2", -22); cue(K("stacking") + 1.32, "tick_3", -22)
toplab(s, X("stack_s"), X("stack_b"), K("stacking"), K("future") - 0.1, WHITE, LBL, 62)
x0, y0 = step_xy(0)
w8 = s.fig(x0, 0.7, WHITE, gy=y0); s.pop(w8, K("stacking") + 0.2, 0.4)
x6, y6 = step_xy(SN - 1)
g8 = s.fig(x6, 0.7, GOLD, gy=y6); s.pop(g8, K("future"), 0.45)
gs = s.spot(x6, 0, "232,194,106", 30, 90, gy=y6, y0=640); s.fade(gs, K("future"), 0.5)
toplab(s, X("fut_s"), X("fut_b"), K("future"), K("dontstop2") - 0.1, GOLD, LBL, 50)
for k in range(1, 4):
    t = K("stacking") + 1.4 + (k - 1) * 0.6
    tl(f'tl.to("#{w8}", {{x: {k * SW}, y: {-k * SH}, duration: 0.32, ease: "power2.out"}}, {t:.3f});')
for k in range(1, 3):
    t = K("future") + 0.9 + (k - 1) * 0.6
    tl(f'tl.to("#{g8}", {{x: {-k * SW}, y: {k * SH}, duration: 0.32, ease: "power2.out"}}, {t:.3f});')
mx, my = (step_xy(3)[0] + step_xy(4)[0]) / 2, step_xy(4)[1] - 120
mt = s.raw(f'<circle id="@ID@" cx="{mx}" cy="{my}" r="26" fill="none" stroke="{GOLD}" stroke-width="4" style="opacity:0"/>', "mt")
tl(f'tl.fromTo("#{mt}", {{opacity: 1, scale: 0.5, transformOrigin: "50% 50%"}}, {{opacity: 0, scale: 4, duration: 0.9, ease: "power2.out", immediateRender: false}}, {K("halfway") + 0.1:.3f});')
cue(K("halfway") + 0.1, "bell_A4", -18)

# 9  "Don't stop now."
s = S(K("dontstop2") - 0.1, K("order") + 0.35)
s.spot(540, 1, "232,194,106")
g9 = s.fig(540, 1.0, GOLD); s.pop(g9, K("dontstop2") - 0.1, 0.4)
a9 = tx(s, 540, 640, X("stop_b"), 72, GOLD, 0, 800, sp=0.04)
tl(f'tl.fromTo("#{a9}", {{opacity: 0, scale: 1.3, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.45, ease: "expo.out", immediateRender: false}}, {K("dontstop2") - 0.05:.3f});')
cue(K("dontstop2"), "bell_G5", -16)

# 10  outro (handles, no end card; brand lines stay in English)
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
    <div id="root" data-composition-id="otm-dontstop" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
{TIMELINE}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-dontstop-audio" class="clip" src="assets/audio/mix_dontstop.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-dontstop"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
