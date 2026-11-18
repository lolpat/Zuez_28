"""OTM "Stop Strategy Hopping": a glowing-figure trading video in the OTM style, inspired by an interview clip about
traders who change strategy every time they lose. The habit that keeps traders stuck: one loss, new strategy; two
losses, new indicator; three losses, new mentor. Nothing works because nothing gets enough trades to show what it can
do. Every strategy has losing streaks, even a good one. Profitable trading looks boring: same setup, same risk, same
rules, trade after trade. The edge isn't in a new strategy; it's in sticking with one long enough to let it work.
English version (Quentin); otm-hopping-th is the Thai version from the same scene file. Original script, voice only,
no music. Scenes key off word indices of work/words.json (anchor table EN_ANC, helper K). Writes ../index.html,
work/cues.json and work/timing.json."""
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
# ---- shared scenes for "Stop Strategy Hopping" (English: otm-hopping, Thai: otm-hopping-th); LANG is set just above this line
def ix(i):
    return W(i)

TH_ = LANG == "th"
# EN: word indices of work/words.json; TH: token indices of work/script.txt (aligned into work/words.json)
EN_ANC = dict(change=7, loss1=13, new1=15, loss2=17, new2=19, loss3=21, new3=23, nothing=25, because=29, prove=35, streak=41,
              evengood=(46, -0.35), boring=(50, 0.25), same1=54, same2=56, same3=58, tradeafter=60, edge=63, sticking=70, order=81, dont=84, follow=90)
TH_ANC = dict(change=1, loss1=2, new1=3, loss2=4, new2=5, loss3=6, new3=7, nothing=(8, 0.4), because=9, prove=11, streak=12,
              evengood=(13, -0.3), boring=(14, 0.3), same1=15, same2=16, same3=17, tradeafter=18, edge=19, sticking=20, order=22, dont=25, follow=26)

def K(key):
    a = (TH_ANC if TH_ else EN_ANC)[key]
    return ix(a[0]) + a[1] if isinstance(a, tuple) else ix(a)

TXT = dict(
    h_s=("A HABIT THAT KEEPS TRADERS", "นิสัยที่ทำให้เทรดเดอร์"), h_b=("STUCK", "ย่ำอยู่กับที่"),
    c_s=("CHANGING STRATEGY", "เปลี่ยนกลยุทธ์"), c_b=("EVERY TIME THEY LOSE", "ทุกครั้งที่ขาดทุน"),
    strat=("STRATEGY", "กลยุทธ์"),
    l1=("1 LOSS", "แพ้ 1 ไม้"), l2=("2 LOSSES", "แพ้ 2 ไม้"), l3=("3 LOSSES", "แพ้ 3 ไม้"),
    n1=("NEW STRATEGY", "เปลี่ยนกลยุทธ์"), n2=("NEW INDICATOR", "เปลี่ยนอินดิเคเตอร์"), n3=("NEW MENTOR", "เปลี่ยนเมนเทอร์"),
    nw_s=("AND NOTHING EVER", "แล้วก็ไม่มีอะไร"), nw_b=("WORKS", "ได้ผลเลย"),
    bc_s=("NO STRATEGY GETS ENOUGH TRADES", "ไม่มีระบบไหนได้เทรดนานพอ"), bc_b=("TO SHOW WHAT IT CAN DO", "ที่จะพิสูจน์ตัวเอง"),
    trades=("TRADES", "ไม้"),
    st_s=("EVERY STRATEGY HAS", "ทุกกลยุทธ์มี"), st_b=("LOSING STREAKS", "ช่วงแพ้ติดกัน"),
    eg_b=("EVEN A GOOD ONE", "แม้แต่กลยุทธ์ที่ดี"),
    bo_s=("PROFITABLE TRADING", "การเทรดที่ทำกำไร"), bo_b=("LOOKS BORING", "ดูน่าเบื่อ"),
    sm1=("SAME SETUP", "เซ็ตอัพเดิม"), sm2=("SAME RISK", "ความเสี่ยงเดิม"), sm3=("SAME RULES", "กฎเดิม"),
    ed_s=("THE EDGE ISN'T IN", "ความได้เปรียบไม่ได้อยู่ใน"), ed_b=("A NEW STRATEGY", "กลยุทธ์ใหม่"),
    sk_s=("IT'S IN STICKING WITH ONE", "แต่อยู่ที่การอยู่กับกลยุทธ์เดียว"), sk_b=("LONG ENOUGH TO LET IT WORK", "นานพอให้มันทำงาน"),
    new=("NEW", "ใหม่"),
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

def tpill(s, x, y, text, fill=GOLD, tcol="#111", size=36):
    i = s.pill(x, y, text, fill, tcol, size)
    if TH_: thai(s)
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

# 1  "Here's a habit that keeps traders stuck. Changing strategy every time they lose."
s = S(0, K("loss1") - 0.1, first=True)
toplab(s, X("h_s"), X("h_b"), 0, K("change") - 0.1, WHITE, LBL, 66, op=1)
toplab(s, X("c_s"), X("c_b"), K("change"), K("loss1") - 0.1, RED, LBL, 52)
tm = s.raw(f'<g id="@ID@"><path d="{rrect(380, 1238, 320, 26, 13)}" fill="#1d2229" stroke="#ffffff60" stroke-width="2"/>'
           f'<line x1="690" y1="1238" x2="738" y2="1050" stroke="#ffffff80" stroke-width="6" stroke-linecap="round"/>'
           f'<line x1="712" y1="1056" x2="770" y2="1056" stroke="#ffffff80" stroke-width="6" stroke-linecap="round"/></g>', "tm")
belt = s.raw(f'<line id="@ID@" x1="394" y1="1251" x2="686" y2="1251" stroke="{GOLD}" stroke-width="4" stroke-dasharray="14 14"/>', "bl")
tl(f'tl.fromTo("#{belt}", {{strokeDashoffset: 0}}, {{strokeDashoffset: 280, duration: {K("loss1") - 0.1:.3f}, ease: "none", immediateRender: false}}, 0);')
f1 = s.fig(540, 1.0, WHITE, 1, gy=1236)
steps = max(1, int((K("loss1") - 0.2) / 0.36))
tl(f'tl.to("#{f1}", {{y: -8, duration: 0.18, yoyo: true, repeat: {2 * steps - 1}, ease: "sine.inOut"}}, 0.05);')
cb = s.raw(f'<path id="@ID@" d="{rrect(430, 760, 220, 150, 18)}" fill="#0f1319" stroke="#ffffff70" stroke-width="3" style="opacity:0"/>', "cb")
cl = tx(s, 540, 800, X("strat"), 28, LBL, 0, 700, sp=0.1)
s.pop(cb, K("change"), 0.35, 0.6, "50% 50%"); s.fade(cl, K("change"), 0.3)
lets = []
for k, ch in enumerate("ABCD"):
    lt = num(s, 540, 884, ch, 64, [WHITE, GOLD, RED, WHITE][k]); lets.append(lt)
dt_ = (K("loss1") - 0.5 - K("change")) / 4
for k, lt in enumerate(lets):
    t = K("change") + 0.15 + k * dt_
    tl(f'tl.fromTo("#{lt}", {{opacity: 0, scaleX: 0, transformOrigin: "50% 50%"}}, {{opacity: 1, scaleX: 1, duration: 0.18, immediateRender: false}}, {t:.3f});')
    if k < 3:
        tl(f'tl.to("#{lt}", {{opacity: 0, scaleX: 0, transformOrigin: "50% 50%", duration: 0.15}}, {t + dt_ - 0.16:.3f});')
    cue(t, "click_" + str(k % 2 + 1), -24)

# 2  "One loss... new strategy. Two losses... new indicator. Three losses... new mentor."
s = S(K("loss1") - 0.1, K("nothing") - 0.1, ground=False, restore=False)
for j, (lk, nk, lab, newl) in enumerate((("loss1", "new1", "l1", "n1"), ("loss2", "new2", "l2", "n2"), ("loss3", "new3", "l3", "n3"))):
    y = 690 + j * 180
    lb = s.raw(f'<path id="@ID@" d="{rrect(130, y - 62, 330, 124, 22)}" fill="#1a0f12" stroke="{RED}" stroke-width="3" style="opacity:0"/>', "lb")
    lt = tx(s, 295, y + 14, X(lab), 38, RED, 0, 800, sp=0.04)
    s.pop(lb, K(lk), 0.35, 0.6, "50% 50%"); s.fade(lt, K(lk) + 0.05, 0.3); cue(K(lk), "tock_1", -20)
    ar = s.path(f"M 478 {y} H 588 M 566 {y - 18} L 590 {y} L 566 {y + 18}", LBL, 5); s.draw(ar, K(nk) - 0.25, 0.3)
    nb = s.raw(f'<path id="@ID@" d="{rrect(610, y - 62, 340, 124, 22)}" fill="#0f1319" stroke="#ffffffa0" stroke-width="3" style="opacity:0"/>', "nb")
    ntx = tx(s, 780, y + 12, X(newl), 31, WHITE, 0, 800, sp=0.03)
    s.pop(nb, K(nk), 0.35, 0.6, "50% 50%"); s.fade(ntx, K(nk) + 0.05, 0.3); cue(K(nk), "pop_" + str(j + 1), -20)
loop = s.path("M 120 1050 C 40 990 40 750 112 694 M 92 720 L 114 692 L 128 726", RED, 5, style="opacity:0.85")
s.draw(loop, K("new3") + 0.7, 0.6); cue(K("new3") + 0.7, "whoosh-short_3", -24)

# 3  "And nothing ever works. Because nothing ever gets enough trades to show what it can do."
s = S(K("nothing") - 0.1, K("streak") - 0.1, ground=False, hide=False, restore=False)
toplab(s, X("nw_s"), X("nw_b"), K("nothing"), K("because") - 0.1, RED, LBL, 64)
toplab(s, X("bc_s"), X("bc_b"), K("because"), K("streak") - 0.1, WHITE, LBL, 46)
tg = s.raw(f'<line id="@ID@" x1="880" y1="670" x2="880" y2="1000" stroke="{GOLD}" stroke-width="4" stroke-dasharray="12 10" '
           f'style="opacity:0;filter:drop-shadow(0 0 8px rgba(232,194,106,0.8))"/>', "tg")
s.fade(tg, K("nothing") + 0.1, 0.4)
tn = num(s, 880, 1060, "100", 44, GOLD); s.fade(tn, K("nothing") + 0.1, 0.4)
tt = tx(s, 880, 1104, X("trades"), 28, GOLD, 0, 700, sp=0.1); s.fade(tt, K("nothing") + 0.1, 0.4)
LENS = [90, 150, 60, 120, 80]
t_r0, t_r1 = K("nothing") + 0.2, K("prove") - 0.2
for k, ln in enumerate(LENS):
    y = 700 + k * 66
    t = t_r0 + k * (t_r1 - t_r0) / 5
    rl = num(s, 150, y + 12, "ABCDE"[k], 34, LBL); s.fade(rl, t, 0.25)
    s.raw(f'<line x1="200" y1="{y}" x2="860" y2="{y}" stroke="#ffffff20" stroke-width="2" stroke-dasharray="4 10"/>', "gl")
    br = s.raw(f'<rect id="@ID@" x="200" y="{y - 12}" width="0" height="24" rx="12" fill="{GOLD}" fill-opacity="0.85"/>', "rb")
    tl(f'tl.fromTo("#{br}", {{attr: {{width: 0}}}}, {{attr: {{width: {ln}}}, duration: 0.35, ease: "power2.out", immediateRender: false}}, {t:.3f});')
    cx = 200 + ln + 22
    xx = s.path(f"M {cx - 13} {y - 13} L {cx + 13} {y + 13} M {cx + 13} {y - 13} L {cx - 13} {y + 13}", RED, 6); s.draw(xx, t + 0.4, 0.15)
    cue(t + 0.4, "tick_" + str(k % 3 + 1), -22)
gap = s.raw(f'<rect id="@ID@" x="380" y="680" width="480" height="300" rx="16" fill="{RED}" fill-opacity="0.07" stroke="{RED}" '
            f'stroke-opacity="0.5" stroke-width="2" stroke-dasharray="10 8" style="opacity:0"/>', "gp")
s.fade(gap, K("prove"), 0.4)
tl(f'tl.fromTo("#{tg}", {{scaleY: 1}}, {{scaleY: 1.06, transformOrigin: "50% 50%", duration: 0.35, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}}, {K("prove"):.3f});')
cue(K("prove"), "swell_2", -24)

# 4  "Every strategy has losing streaks. Even a good one."
s = S(K("streak") - 0.1, K("boring") - 0.1, ground=False, hide=False, restore=False)
toplab(s, X("st_s"), X("st_b"), K("streak"), K("evengood") - 0.1, RED, LBL, 62)
toplab(s, "", X("eg_b"), K("evengood"), K("boring") - 0.1, GOLD, LBL, 62)
STEPS = [2, 3, -1, 2, 3, -2, -3, -2, -2, 3, 4, 2, -1, 3, 2, 3, -2, -3, -2, -1, 4, 3, 2, 3, -1, 3, 2, 4, -2, -3, -2, 3, 4, 3, 2]
pts, eq = [(150, 1260)], 0
for k, d in enumerate(STEPS):
    eq += d; pts.append((150 + (k + 1) * 22, 1260 - eq * 9))
cv = s.path("M " + " L ".join(f"{x:.0f} {y:.0f}" for x, y in pts), GOLD, 5, style="filter:drop-shadow(0 0 8px rgba(232,194,106,0.8))")
t_c0, t_c1 = K("streak") + 0.1, K("evengood") + 0.2
s.draw(cv, t_c0, t_c1 - t_c0, "none")
zones, k = [], 0                                  # drawdown runs of 3+ losing steps
while k < len(STEPS):
    if STEPS[k] < 0:
        j = k
        while j < len(STEPS) and STEPS[j] < 0: j += 1
        if j - k >= 3: zones.append((k, j))
        k = j
    else:
        k += 1
for a, b in zones:
    x0, x1 = pts[a][0], pts[b][0]
    ys = [p[1] for p in pts[a:b + 1]]
    z = s.raw(f'<rect id="@ID@" x="{x0}" y="{min(ys) - 20:.0f}" width="{x1 - x0}" height="{max(ys) - min(ys) + 40:.0f}" rx="8" fill="{RED}" '
              f'fill-opacity="0.16" stroke="{RED}" stroke-opacity="0.7" stroke-width="2" style="opacity:0"/>', "zn")
    tz = t_c0 + (x1 - 150) / (pts[-1][0] - 150) * (t_c1 - t_c0)
    s.fade(z, tz, 0.3); cue(tz, "tock_1", -24)
tr = s.path(f"M {pts[0][0]} {pts[0][1]} L {pts[-1][0]} {pts[-1][1]}", "#ffffff70", 3, drawn=True, style="stroke-dasharray:10 10;opacity:0")
s.fade(tr, K("evengood") + 0.3, 0.4)
cue(K("evengood"), "bell_E5", -20)

# 5  "Profitable trading looks boring. Same setup. Same risk. Same rules. Trade after trade."
s = S(K("boring") - 0.1, K("edge") - 0.1, ground=False, hide=False)
toplab(s, X("bo_s"), X("bo_b"), K("boring"), K("edge") - 0.1, WHITE, LBL, 64)
for j, (key, k_) in enumerate((("sm1", "same1"), ("sm2", "same2"), ("sm3", "same3"))):
    p = tpill(s, 540, 690 + j * 120, X(key), GOLD, "#111", 42)
    s.pop(p, K(k_), 0.35, 0.6, "50% 50%"); cue(K(k_), "pop_" + str(j + 1), -18)
    hide(p, K("edge") - 0.5, 0.2)
t_a, t_b = K("same1") + 0.3, K("edge") - 0.8
for k in range(12):
    x = 156 + k * 64
    tb_ = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(x, 1080, 52, 52, 10)}" fill="#14110a" stroke="{GOLD}" stroke-width="2"/>'
                f'<path d="M {x + 14} 1107 L {x + 23} 1117 L {x + 39} 1095" fill="none" stroke="{GOLD}" stroke-width="4" '
                f'stroke-linecap="round" stroke-linejoin="round"/></g>', "tb")
    t = t_a + k * (t_b - t_a) / 11
    s.pop(tb_, t, 0.25, 0.6, "50% 50%"); hide(tb_, K("edge") - 0.5, 0.2)
    if k % 3 == 0: cue(t, "tick-crisp_" + str(k // 3 % 3 + 1), -24)

# 6  "The edge isn't in a new strategy. It's in sticking with one long enough to let it work."
s = S(K("edge") - 0.1, K("order") + 0.35)
toplab(s, X("ed_s"), X("ed_b"), K("edge"), K("sticking") - 0.1, RED, LBL, 60)
toplab(s, X("sk_s"), X("sk_b"), K("sticking"), K("order") + 0.35, GOLD, LBL, 44)
for k, (gx, gy) in enumerate(((150, 690), (700, 670), (190, 930), (730, 900))):
    g = s.raw(f'<path id="@ID@" d="{rrect(gx, gy, 200, 90, 16)}" fill="none" stroke="#7d838c" stroke-width="3" stroke-dasharray="10 8" style="opacity:0"/>', "gh")
    gt = tx(s, gx + 100, gy + 57, X("new"), 32, GREY, 0, 800, sp=0.1)
    for i in (g, gt):
        s.pop(i, K("edge") + 0.1 + k * 0.15, 0.3, 0.6, "50% 50%")
        tl(f'tl.to("#{i}", {{opacity: 0, y: -24, duration: 0.4, ease: "power2.in"}}, {K("sticking") - 0.45:.3f});')
cue(K("edge") + 0.1, "pop_4", -22)
f6 = s.fig(250, 1.0, GOLD); s.pop(f6, K("sticking"), 0.45); cue(K("sticking"), "bell_C5", -18)
rr = random.Random(5)
cpts, y = [], 1190
for k in range(26):
    y += rr.uniform(-26, 8) if k % 5 != 4 else rr.uniform(4, 16)
    cpts.append((360 + k * 22, y))
lc = s.path("M " + " L ".join(f"{x:.0f} {y:.0f}" for x, y in cpts), GOLD, 5, style="filter:drop-shadow(0 0 10px rgba(232,194,106,0.8))")
s.draw(lc, K("sticking") + 0.3, max(1.2, K("order") - 0.2 - K("sticking")), "power1.inOut")

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
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="otm-hopping" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
{TIMELINE}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-hopping-audio" class="clip" src="assets/audio/mix_hopping.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-hopping"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
