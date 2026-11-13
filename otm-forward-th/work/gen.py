"""OTM "Always Forward" (Thai version): the Thai-language edition of otm-forward, built from the same scene file with
LANG = "th". Thai narration (ElevenLabs "Patinya", calm Thai narrator), Thai on-screen text in Kanit (OFL, assets/fonts);
the outro keeps the brand lines in English. Plan for losses (stop loss), never plan to quit. Original script, voice only,
no music. Scenes key off token indices of work/words.json (the script's tokens aligned to the voice; anchor table ANC).
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
# ---- shared scenes for "Always Forward" (English: otm-forward, Thai: otm-forward-th); LANG is set just above this line
def ix(i):
    return W(i)

TH_ = LANG == "th"
# anchor -> word index (English, work/words.json from faster-whisper) or token index (Thai, work/script.txt aligned)
ANC = dict(
    title=(0, 0), back=(2, 1), goal=(4, 2), door=(9, 3), maybe=(15, 4), quit1=(17, 5), thought=(23, 6), plan_fail=(26, 7),
    trading=(31, 8), plan_loss=(36, 9), stop=(39, 10), stoploss=(42, (10, 1.2)), but_plan=(46, 11), not_quit=(52, 12),
    every=(56, 13), month=(63, 14), streak=(69, 15), blown=(72, 16), walk=(75, 17), diff=(81, 18), didnt=(84, 19),
    persist=(85, 20), mood=(88, 21), decision=(91, 22), outside=(92, 23), keep=(100, 24), inside=(108, 25),
    cut=(109, 26), dream=(112, 27), fwd2=(115, 28), back2=(117, 29), order=(119, 30), dont=(122, 33), follow=(128, 34))

def K(key):
    a = ANC[key][1 if TH_ else 0]
    return ix(a[0]) + a[1] if isinstance(a, tuple) else ix(a)

TXT = dict(
    t1=("ALWAYS FORWARD", "ไปข้างหน้าเสมอ"), t2=("NEVER BACKWARD", "ไม่ถอยหลัง"),
    goal_s=("ONCE YOU'VE CHOSEN", "เมื่อเลือก"), goal_b=("YOUR GOAL", "เป้าหมายแล้ว"),
    door_s=("STOP LEAVING", "เลิกเปิด"), door_b=("THE BACK DOOR OPEN", "ประตูหลังทิ้งไว้"),
    goal=("GOAL", "เป้าหมาย"), backdoor=("BACK DOOR", "ประตูหลัง"),
    q1=("“MAYBE I'LL QUIT", "“ถ้าเดือนนี้แย่..."), q2=("IF THIS MONTH GOES BADLY…”", "ก็คงเลิก”"),
    fail_s=("THAT THOUGHT IS ALREADY", "ความคิดนี้ คือ"), fail_b=("A PLAN TO FAIL", "แผนที่จะล้มเหลว"),
    trade_s=("IN TRADING", "ในการเทรด"), trade_b=("YOU DO PLAN FOR LOSSES", "ต้องวางแผนรับการขาดทุน"),
    entry=("ENTRY", "จุดเข้า"), stoploss=("STOP LOSS", "สต็อปลอส"),
    but_s=("BUT PLANNING FOR A LOSS", "แต่การวางแผนรับการขาดทุน"), but_b=("IS NOT PLANNING TO QUIT", "ไม่ใช่การวางแผนที่จะเลิก"),
    card1=("PLAN FOR A LOSS", "วางแผนรับขาดทุน"), card2=("PLAN TO QUIT", "วางแผนจะเลิก"),
    every_s=("EVERY TRADER WHO MADE IT HAD", "เทรดเดอร์ทุกคนที่ไปถึงฝั่ง"), every_b=("A MONTH THAT ALMOST BROKE THEM", "เคยมีเดือนที่แทบพัง"),
    w1=("LOSING STREAK", "ขาดทุนติดกัน"), w2=("BLOWN ACCOUNT", "พอร์ตแตก"), w3=("WANTED TO QUIT", "อยากเดินหนี"),
    diff_s=("THE DIFFERENCE?", "ความต่างคืออะไร?"), diff_b=("THEY DIDN'T QUIT", "พวกเขาไม่เลิก"),
    pers_s=("PERSISTENCE", "ความอดทน"), pers_b=("ISN'T A MOOD", "ไม่ใช่อารมณ์"), dec_b=("IT'S A DECISION", "แต่คือการตัดสินใจ"),
    mood=("MOOD", "อารมณ์"), decision=("DECISION", "การตัดสินใจ"),
    out_s=("THE MARKET TESTS YOU", "ตลาดจะทดสอบคุณ"), out_b=("FROM THE OUTSIDE", "จากข้างนอก"),
    in_s=("WHETHER YOU KEEP GOING", "จะไปต่อหรือไม่"), in_b=("IS DECIDED INSIDE", "ตัดสินจากข้างใน"),
    cut=("CUT THE LOSS", "ตัดขาดทุน"), dream=("KEEP THE DREAM", "แต่อย่าตัดความฝัน"),
    loss=("LOSS", "ขาดทุน"), dreaml=("DREAM", "ความฝัน"),
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
    """A label in the video's language: Montserrat caps (English) or Kanit (Thai, a touch larger, no letter-spacing)."""
    if TH_:
        i = s.label(x, y, text, round(size * 1.08), col, op, 700 if weight >= 700 else 600, 0, anchor); thai(s)
    else:
        i = s.label(x, y, text, size, col, op, weight, sp, anchor)
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

def flag(s, x, base=GY, op=0, col=GOLD):
    return s.raw(f'<g id="@ID@" style="opacity:{op};filter:drop-shadow(0 0 14px rgba(232,194,106,0.8))">'
                 f'<rect x="{x - 3}" y="{base - 230}" width="6" height="230" fill="{col}"/>'
                 f'<path d="M {x + 3} {base - 230} L {x + 110} {base - 200} L {x + 3} {base - 168} Z" fill="{col}"/></g>', "fg")

def star_d(cx, cy, r):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5; rr = r if k % 2 == 0 else r * 0.45
        pts.append(f"{cx + rr * math.cos(a):.1f} {cy + rr * math.sin(a):.1f}")
    return "M " + " L ".join(pts) + " Z"

# 1  "Always forward. Never backward."
s = S(0, K("goal") - 0.1, first=True)
tx(s, 540, 486, X("t1"), 64, WHITE, 1, 800, sp=0.04)
nb = tx(s, 540, 572, X("t2"), 64, GOLD, 1, 800, sp=0.04)
f1 = s.fig(300, 1.0, WHITE, 1)
s.walk(f1, 0.15, 360, K("goal") - 0.4)
ar = s.path(f"M 180 1300 H 900 M 900 1300 L 872 1286 M 900 1300 L 872 1314", GOLD, 5, style="filter:drop-shadow(0 0 8px rgba(232,194,106,0.8))")
s.draw(ar, 0.2, 1.0)
bk = s.path(f"M 520 1380 H 200 M 200 1380 L 228 1366 M 200 1380 L 228 1394", "#6b7079", 4); s.draw(bk, K("back") - 0.1, 0.5)
xb = s.path("M 340 1362 L 376 1398 M 376 1362 L 340 1398", RED, 6); s.draw(xb, K("back") + 0.4, 0.3)
cue(0.2, "whoosh-short_1", -24); cue(K("back") + 0.4, "tock_1", -20)

# 2  "Once you've chosen your goal, stop leaving the back door open."
s = S(K("goal") - 0.1, K("maybe") - 0.1)
f2 = s.fig(540, 1.0, WHITE); s.pop(f2, K("goal"), 0.4)
fg = flag(s, 860); s.pop(fg, K("goal") + 0.5, 0.45, 0.4); cue(K("goal") + 0.5, "bell_C5", -20)
gl = tx(s, 905, 1300, X("goal"), 30, GOLD, 0, 800, sp=0.15); s.fade(gl, K("goal") + 0.6, 0.3)
toplab(s, X("goal_s"), X("goal_b"), K("goal"), K("door") - 0.1, GOLD, LBL, 60)
s.raw(f'<rect x="110" y="1030" width="130" height="210" fill="none" stroke="#f4f4f2" stroke-opacity="0.8" stroke-width="5"/>', "df")
lite = s.raw(f'<rect id="@ID@" x="113" y="1033" width="124" height="204" fill="#ffffff" fill-opacity="0.16"/>', "dl")
dopen = s.raw(f'<path id="@ID@" d="M 110 1030 L 52 1052 L 52 1222 L 110 1240 Z" fill="#f4f4f2" fill-opacity="0.85"/>', "do")
dshut = s.raw(f'<rect id="@ID@" x="113" y="1033" width="124" height="204" fill="#2a2e35" stroke="#f4f4f2" stroke-width="3" style="opacity:0"/>', "ds")
bl = tx(s, 175, 1300, X("backdoor"), 28, LBL, 1, 800, sp=0.08)
toplab(s, X("door_s"), X("door_b"), K("door"), K("maybe") - 0.1, WHITE, LBL, 52)
T_SHUT = K("door") + 1.1
hide(dopen, T_SHUT, 0.15); hide(lite, T_SHUT, 0.2)
s.fade(dshut, T_SHUT, 0.12)
lk = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="160" y="1128" width="30" height="24" rx="4" fill="{GOLD}"/>'
           f'<path d="M 165 1128 V 1118 A 10 10 0 0 1 185 1118 V 1128" fill="none" stroke="{GOLD}" stroke-width="4"/></g>', "lk")
s.pop(lk, T_SHUT + 0.15, 0.3, 0.3, "50% 50%")
cue(T_SHUT, "land_1", -14)

# 3  "'Maybe I'll quit if this month goes badly.' That thought is already a plan to fail."
s = S(K("maybe") - 0.1, K("trading") - 0.1)
f3 = s.fig(540, 1.0, WHITE); s.pop(f3, K("maybe") - 0.05, 0.4)
c1 = s.raw('<circle id="@ID@" cx="572" cy="1004" r="9" fill="#f4f4f2" style="opacity:0"/>', "b")
c2 = s.raw('<circle id="@ID@" cx="602" cy="960" r="14" fill="#f4f4f2" style="opacity:0"/>', "b")
cl = s.raw(f'<path id="@ID@" d="{rrect(170, 700, 740, 220, 60)}" fill="#0f1319" stroke="#f4f4f2" stroke-width="4" style="opacity:0"/>', "c")
s.pop(c1, K("maybe"), 0.25, 0.3, "50% 50%"); s.pop(c2, K("maybe") + 0.1, 0.25, 0.3, "50% 50%"); s.pop(cl, K("maybe") + 0.2, 0.4, 0.6, "50% 50%")
q1 = tx(s, 540, 795, X("q1"), 40, WHITE, 0, 800, sp=0.04); s.fade(q1, K("maybe") + 0.3, 0.3)
q2 = tx(s, 540, 862, X("q2"), 40, WHITE, 0, 800, sp=0.04); s.fade(q2, K("quit1") - 0.05, 0.3)
cue(K("maybe"), "pop_2", -20)
toplab(s, X("fail_s"), X("fail_b"), K("thought"), K("trading") - 0.1, RED, LBL, 60)
tl(f'tl.to("#{cl}", {{stroke: "{RED}", duration: 0.3}}, {K("plan_fail"):.3f});')
for q in (q1, q2):
    tl(f'tl.to("#{q}", {{fill: "{RED}", duration: 0.3}}, {K("plan_fail"):.3f});')
tl(f'tl.to("#{f3}", {{opacity: 0.45, duration: 0.5}}, {K("plan_fail"):.3f});')
cue(K("plan_fail"), "tock_1", -16)

# 4  "Now, in trading, you do plan for losses. That's what a stop loss is for. But planning for a loss is not planning to quit."
s = S(K("trading") - 0.1, K("every") - 0.1, ground=False)
toplab(s, X("trade_s"), X("trade_b"), K("trading"), K("but_plan") - 0.1, GOLD, LBL, 50)
pr = s.path("M 180 1000 L 250 975 L 300 985 L 360 940 L 420 955 L 500 900 L 560 915 L 640 860 L 700 875 L 780 810 L 840 830 L 900 770",
            "#e9ecf1", 5); s.draw(pr, K("trading") + 0.2, 1.4)
en = s.raw(f'<circle id="@ID@" cx="300" cy="985" r="12" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 8px rgba(232,194,106,0.9))"/>', "en")
s.pop(en, K("plan_loss"), 0.3, 0.3, "50% 50%")
el = tx(s, 300, 945, X("entry"), 28, GOLD, 0, 800, sp=0.12); s.fade(el, K("plan_loss"), 0.3)
sl = s.raw(f'<line id="@ID@" x1="180" y1="1060" x2="920" y2="1060" stroke="{RED}" stroke-width="4" stroke-dasharray="14 10" style="opacity:0"/>', "sl")
s.fade(sl, K("stop"), 0.4)
spl = s.pill(780, 1120, X("stoploss"), RED, "#fff", 28)
if TH_: thai(s)
s.pop(spl, K("stoploss"), 0.4, 0.6, "50% 50%")
ck = s.path("M 920 1105 L 935 1122 L 965 1090", GOLD, 7); s.draw(ck, K("stoploss") + 0.4, 0.3)
cue(K("stop"), "tick_1", -20); cue(K("stoploss"), "pop_1", -18)
for i_ in (pr, en, el, sl, spl, ck):
    hide(i_, K("but_plan") - 0.2, 0.4, 0.15)
toplab(s, X("but_s"), X("but_b"), K("but_plan"), K("every") - 0.1, WHITE, LBL, 48)
for j, (key, x, col) in enumerate([("card1", 300, GOLD), ("card2", 780, RED)]):
    cd = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(x - 210, 1170, 420, 170, 22)}" fill="#0f1319" stroke="{col}" stroke-width="3"/>'
               f'<text x="{x}" y="1310" text-anchor="middle" {FNT} font-size="{32 if TH_ else 30}" fill="#fff">{X(key)}</text></g>', "cd")
    s.pop(cd, K("but_plan") + 0.2 + j * 0.25, 0.4, 0.6, "50% 50%")
mk1 = s.path("M 270 1232 L 292 1256 L 332 1210", GOLD, 8); s.draw(mk1, K("but_plan") + 0.7, 0.3)
mk2 = s.path("M 758 1212 L 802 1256 M 802 1212 L 758 1256", RED, 8); s.draw(mk2, K("not_quit") + 0.2, 0.3)
cue(K("but_plan") + 0.7, "bell_E5", -20); cue(K("not_quit") + 0.2, "tock_1", -16)

# 5  "Every trader who made it had a month that almost broke them. A losing streak. A blown account. A day they wanted to walk away.
#     The difference? They didn't."
s = S(K("every") - 0.1, K("persist") + 0.15)
f5 = s.fig(140, 1.0, WHITE); s.pop(f5, K("every"), 0.4)
s.walk(f5, K("every") + 0.4, 110, 1.4)
toplab(s, X("every_s"), X("every_b"), K("every"), K("diff") - 0.1, WHITE, LBL, 38 if not TH_ else 52)
walls, wlabs = [], []
for j, (key, x, ly) in enumerate([("w1", 380, 1000), ("w2", 600, 935), ("w3", 820, 1000)]):
    w = s.raw(f'<rect id="@ID@" x="{x - 16}" y="1040" width="32" height="200" rx="6" fill="{RED}" fill-opacity="0.35" stroke="{RED}" stroke-width="3" '
              f'style="opacity:0;filter:drop-shadow(0 0 10px rgba(255,77,94,0.6))"/>', "wl")
    t = K(["streak", "blown", "walk"][j])
    s.pop(w, t - 0.1, 0.35, 0.2, "50% 100%"); cue(t - 0.1, "land-light_1", -18)
    wl = tx(s, x, ly, X(key), 28, RED, 0, 800, sp=0.06); s.fade(wl, t - 0.05, 0.3)
    walls.append(w); wlabs.append(wl)
toplab(s, X("diff_s"), X("diff_b"), K("diff"), K("persist") + 0.15, GOLD, LBL, 58)
T_GO = K("diff") + 0.4
for j, (w, wl) in enumerate(zip(walls, wlabs)):
    tb = T_GO + [0.12, 0.62, 1.12][j]
    tl(f'tl.to("#{w}", {{opacity: 0, scaleY: 0.2, transformOrigin: "50% 100%", duration: 0.3, ease: "power2.in"}}, {tb:.3f});')
    hide(wl, tb, 0.3)
    cue(tb, "click_" + str(j % 2 + 1), -18)
s.walk(f5, T_GO, 640, 1.6)
fg5 = flag(s, 980); s.pop(fg5, T_GO + 1.3, 0.4, 0.4); cue(T_GO + 1.3, "bell_C5", -20)

# 6  "Persistence isn't a mood. It's a decision."
s = S(K("persist") + 0.1, K("outside") + 0.25, ground=False)
toplab(s, X("pers_s"), X("pers_b"), K("persist") + 0.1, K("mood") + 0.4, WHITE, LBL, 60)
wave = "M 120 960 " + " ".join(f"Q {150 + k * 60} {960 + (70 if k % 2 == 0 else -70)} {180 + k * 60} 960" for k in range(6))
wv = s.path(wave, "#9aa0a8", 5); s.draw(wv, K("mood") - 0.2, 0.8)
ml = tx(s, 300, 1100, X("mood"), 32, "#9aa0a8", 0, 800, sp=0.15); s.fade(ml, K("mood"), 0.3)
cue(K("mood") - 0.2, "whoosh-short_2", -24)
toplab(s, "", X("dec_b"), K("mood") + 0.4, K("outside") + 0.25, GOLD, LBL, 60)
hide(wv, K("decision"), 0.4, 0.25); hide(ml, K("decision"), 0.4, 0.4)
da = s.path("M 600 960 H 940 M 940 960 L 910 942 M 940 960 L 910 978", GOLD, 7, style="filter:drop-shadow(0 0 10px rgba(232,194,106,0.9))")
s.draw(da, K("decision"), 0.5)
dl = tx(s, 770, 1100, X("decision"), 32, GOLD, 0, 800, sp=0.15); s.fade(dl, K("decision") + 0.2, 0.3)
cue(K("decision"), "bell_G5", -18)

# 7  "The market will test you from the outside. Whether you keep going is decided on the inside."
s = S(K("outside") + 0.2, K("cut") - 0.3)
f7 = s.fig(540, 1.0, WHITE); s.pop(f7, K("outside") + 0.25, 0.4)
toplab(s, X("out_s"), X("out_b"), K("outside") + 0.25, K("keep") - 0.1, RED, LBL, 60)
for j, (ang, dist) in enumerate([(190, 330), (-10, 330), (150, 320), (30, 320), (120, 300), (60, 300)]):
    a = math.radians(ang); cx, cy = 540, 1150
    sx, sy = cx + math.cos(a) * dist, cy - math.sin(a) * dist
    ex, ey = cx + math.cos(a) * 120, cy - math.sin(a) * 120
    ux, uy = (ex - sx), (ey - sy); L = math.hypot(ux, uy); ux, uy = ux / L, uy / L
    hx1, hy1 = ex - ux * 18 - uy * 10, ey - uy * 18 + ux * 10
    hx2, hy2 = ex - ux * 18 + uy * 10, ey - uy * 18 - ux * 10
    arw = s.path(f"M {sx:.0f} {sy:.0f} L {ex:.0f} {ey:.0f} M {hx1:.0f} {hy1:.0f} L {ex:.0f} {ey:.0f} L {hx2:.0f} {hy2:.0f}", RED, 5)
    t = K("outside") + 0.3 + j * 0.28
    s.draw(arw, t, 0.3, "power2.in"); hide(arw, t + 0.9, 0.3)
    cue(t + 0.28, "tick_" + str(j % 3 + 1), -22)
toplab(s, X("in_s"), X("in_b"), K("keep"), K("cut") - 0.3, GOLD, LBL, 56)
core = s.raw(f'<circle id="@ID@" cx="540" cy="{GY - 62}" r="18" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 16px rgba(232,194,106,1))"/>', "co")
s.pop(core, K("inside") - 0.1, 0.4, 0.2, "50% 50%")
rg = s.raw(f'<circle id="@ID@" cx="540" cy="{GY - 62}" r="30" fill="none" stroke="{GOLD}" stroke-width="4" style="opacity:0"/>', "rg")
tl(f'tl.fromTo("#{rg}", {{opacity: 1, scale: 0.6, transformOrigin: "50% 50%"}}, {{opacity: 0, scale: 5, duration: 1.0, ease: "power2.out", immediateRender: false}}, {K("inside"):.3f});')
cue(K("inside") - 0.1, "swell_2", -18)

# 8  "Cut the loss. Keep the dream."
s = S(K("cut") - 0.35, K("fwd2") + 0.2, ground=False)
toplab(s, "", X("cut"), K("cut") - 0.3, K("dream") - 0.05, RED, LBL, 66)
ls1 = s.path("M 150 820 L 290 940", RED, 7); s.draw(ls1, K("cut") - 0.05, 0.35)
ls2 = s.path("M 290 940 L 440 1080", RED, 7); s.draw(ls2, K("cut") + 0.25, 0.35)
cutm = s.path("M 250 990 L 340 900", WHITE, 5); s.draw(cutm, K("cut") + 0.7, 0.18); cue(K("cut") + 0.7, "click_2", -14)
tl(f'tl.to("#{ls2}", {{y: 160, opacity: 0, duration: 0.6, ease: "power2.in"}}, {K("cut") + 0.85:.3f});')
hide(cutm, K("cut") + 1.0, 0.3)
lsl = tx(s, 230, 1150, X("loss"), 30, RED, 0, 800, sp=0.15); s.fade(lsl, K("cut"), 0.3)
toplab(s, "", X("dream"), K("dream") - 0.05, K("fwd2") + 0.2, GOLD, LBL, 60)
st = s.raw(f'<path id="@ID@" d="{star_d(770, 950, 110)}" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 22px rgba(232,194,106,0.9))"/>', "st")
s.pop(st, K("dream"), 0.5, 0.3, "50% 50%"); cue(K("dream"), "bell_A4", -18)
drl = tx(s, 770, 1150, X("dreaml"), 30, GOLD, 0, 800, sp=0.15); s.fade(drl, K("dream") + 0.2, 0.3)

# 9  "Always forward. Never backward."
s = S(K("fwd2") + 0.15, K("order") + 0.35)
s.spot(540, 1, "232,194,106")
f9 = s.fig(380, 1.0, GOLD); s.pop(f9, K("fwd2") + 0.15, 0.4)
s.walk(f9, K("fwd2") + 0.2, 160, 1.3)
fg9 = flag(s, 760); s.pop(fg9, K("fwd2") + 0.2, 0.4, 0.4)
a9 = tx(s, 540, 620, X("t1"), 66, GOLD, 0, 800, sp=0.04)
tl(f'tl.fromTo("#{a9}", {{opacity: 0, scale: 1.3, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.45, ease: "expo.out", immediateRender: false}}, {K("fwd2") + 0.2:.3f});')
n9 = tx(s, 540, 712, X("t2"), 46, "#9aa0a8", 0, 800, sp=0.06); s.fade(n9, K("back2") - 0.1, 0.35, y=10)
cue(K("fwd2"), "bell_G5", -16)

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
<html lang="th" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="otm-forward-th" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
{TIMELINE}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-forward-th-audio" class="clip" src="assets/audio/mix_forward_th.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-forward-th"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
