"""OTM "Selfish With Your Time" (Thai version): the Thai-language edition of otm-selfish, built from the same scene file
with LANG = "th". Thai narration (ElevenLabs "Patinya", calm Thai narrator), Thai on-screen text in Kanit (OFL,
assets/fonts); the outro keeps the brand lines in English. Selfish with your time, never all in on one trade, all in on
the process. Original script, voice only, no music. Scenes key off token indices of work/words.json (the script's tokens
aligned to the voice; anchor table ANC). Writes ../index.html, work/cues.json and work/timing.json."""
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
# ---- shared scenes for "Selfish With Your Time" (English: otm-selfish, Thai: otm-selfish-th); LANG is set just above
def ix(i):
    return W(i)

TH_ = LANG == "th"
ANC = dict(
    selfish=(0, 0), notpeople=(7, 1), time=(10, 2), mask=(13, 3), skill=(20, 4), savings=(23, 5), discipline=(26, 6),
    trading=(29, 7), process=(39, 9), truth=(45, 10), notwhere=(49, 11), study=(56, 12), journal=(60, 13), rules=(65, 14),
    harddays=(73, 15), three2=(75, 16), five=(85, 18), seven=(86, 19), twelve=(87, 20), imagine=(91, 21),
    focused=(96, 23), humble=(98, 24), grounded=(100, 25), stacking=(102, 26), noone=(109, 27), order=(116, 28),
    dont=(119, 31), follow=(125, 32))

def K(key):
    a = ANC[key][1 if TH_ else 0]
    return ix(a[0]) + a[1] if isinstance(a, tuple) else ix(a)

TXT = dict(
    t1=("BE SELFISH", "เห็นแก่ตัว"), t2=("FOR THE NEXT 3 YEARS", "สักสามปี"), yr=("YEAR", "ปี"),
    np_s=("NOT WITH PEOPLE", "ไม่ใช่กับคนรอบข้าง"), np_b=("WITH YOUR TIME", "แต่กับเวลาของคุณ"),
    people=("PEOPLE", "คนรอบข้าง"), yourtime=("YOUR TIME", "เวลาของคุณ"),
    mask_s=("PUT YOUR OWN", "ใส่หน้ากากออกซิเจน"), mask_b=("OXYGEN MASK ON FIRST", "ให้ตัวเองก่อน"),
    skill=("SKILL", "ทักษะ"), savings=("SAVINGS", "เงินเก็บ"), discipline=("DISCIPLINE", "วินัย"),
    allin_s=("IN TRADING, NEVER GO", "ในการเทรด"), allin_b=("ALL IN ON ONE POSITION", "อย่าทุ่มหมดตัวในไม้เดียว"),
    proc_s=("GO ALL IN ON", "ให้ทุ่มสุดตัวกับ"), proc_b=("THE PROCESS", "กระบวนการ"),
    allin=("ALL IN", "ทุ่มหมดตัว"), onetrade=("1 TRADE", "ไม้เดียว"),
    p1=("PLAN", "วางแผน"), p2=("EXECUTE", "ลงมือ"), p3=("JOURNAL", "จดบันทึก"), p4=("REVIEW", "ทบทวน"),
    truth_b=("TELL YOURSELF THE TRUTH", "บอกความจริงกับตัวเอง"),
    nw=("“I'M NOT WHERE I WANT TO BE.”", "“ฉันยังไม่ได้อยู่ในจุดที่อยากอยู่”"),
    c1=("I CAN STUDY MORE", "ศึกษาให้มากกว่านี้"), c2=("I CAN JOURNAL EVERY TRADE", "จดบันทึกทุกเทรด"),
    c3=("I CAN FOLLOW MY RULES", "ทำตามกฎ แม้ในวันที่ยาก"),
    d3_s=("DO THAT FOR", "ทำแบบนี้"), d3_b=("3 YEARS", "สักสามปี"),
    y_s=("AND WHAT YOU CAN DO IN", "แล้วสิ่งที่คุณทำได้ใน"), y_b=("5, 7, 12 YEARS", "อีก 5, 7, 12 ปี"),
    im_b=("IS HARD TO IMAGINE", "อาจเกินกว่าที่นึกภาพไว้"), yl=("Y", " ปี"),
    s1=("STAY FOCUSED", "จดจ่อไว้"), s2=("STAY HUMBLE", "ถ่อมตัวไว้"), s3=("STAY GROUNDED", "ติดดินไว้"),
    st_s=("KEEP STACKING", "สะสมต่อไป"), st_b=("ONE DAY AT A TIME", "ทีละวัน"),
    no_s=("NO MATTER WHAT", "ไม่ว่าคนรอบข้าง"), no_b=("ANYONE AROUND YOU SAYS", "จะพูดอะไร"),
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

# 1  "Be selfish for the next three years."
s = S(0, K("notpeople") - 0.1, first=True)
tx(s, 540, 486, X("t1"), 68, WHITE, 1, 800, sp=0.04)
tx(s, 540, 566, X("t2"), 46, GOLD, 1, 800, sp=0.06)
f1 = s.fig(540, 1.0, WHITE, 1)
T1 = max(1.6, K("notpeople") - 0.5)
for r in range(3):
    tx(s, 222, 718 + r * 62, f"{X('yr')} {r + 1}" if not TH_ else f"ปี {r + 1}", 28, LBL, 1, 800, "end", sp=0.06)
    for c in range(12):
        k = r * 12 + c
        x, y = 240 + c * 52, 682 + r * 62
        s.raw(f'<rect x="{x}" y="{y}" width="44" height="44" rx="8" fill="none" stroke="#ffffff38" stroke-width="2"/>', "o")
        b = s.raw(f'<rect id="@ID@" x="{x}" y="{y}" width="44" height="44" rx="8" fill="{GOLD}" style="opacity:0"/>', "mb")
        s.fade(b, 0.2 + k * (T1 - 0.2) / 36, 0.12)
cue(0.2, "swell_1", -24)

# 2  "Not with people. With your time."
s = S(K("notpeople") - 0.1, K("mask") - 0.1)
toplab(s, X("np_s"), X("np_b"), K("notpeople"), K("mask") - 0.1, GOLD, LBL, 60)
for j, x in enumerate([200, 290, 380]):
    p = s.fig(x, 0.55, "#c9ced6"); s.pop(p, K("notpeople") + j * 0.08, 0.35)
hrt = s.raw(f'<path id="@ID@" d="M 290 1052 C 250 1020 250 980 278 976 C 288 975 290 984 290 990 C 290 984 292 975 302 976 C 330 980 330 1020 290 1052 Z" '
            f'fill="{RED}" style="opacity:0;filter:drop-shadow(0 0 10px rgba(255,77,94,0.7))"/>', "ht")
s.pop(hrt, K("notpeople") + 0.4, 0.4, 0.3, "50% 50%")
pl = tx(s, 290, 1300, X("people"), 28, LBL, 0, 800, sp=0.12); s.fade(pl, K("notpeople") + 0.2, 0.3)
clk = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 16px rgba(232,194,106,0.8))"><circle cx="770" cy="1040" r="96" fill="none" stroke="{GOLD}" stroke-width="8"/>'
            f'<path d="M 770 1040 L 770 980 M 770 1040 L 812 1064" stroke="{GOLD}" stroke-width="8" stroke-linecap="round"/>'
            f'<rect x="742" y="1150" width="56" height="44" rx="8" fill="{GOLD}"/><path d="M 752 1150 V 1136 A 18 18 0 0 1 788 1136 V 1150" fill="none" stroke="{GOLD}" stroke-width="6"/></g>', "ck")
s.pop(clk, K("time") - 0.1, 0.45, 0.5, "50% 50%"); cue(K("time") - 0.1, "bell_C5", -20)
tlb = tx(s, 770, 1300, X("yourtime"), 30, GOLD, 0, 800, sp=0.12); s.fade(tlb, K("time"), 0.3)

# 3  "Put your own oxygen mask on first. Build your skill. Build your savings. Build your discipline."
s = S(K("mask") - 0.1, K("trading") - 0.1)
f3 = s.fig(300, 1.0, WHITE); s.pop(f3, K("mask") - 0.05, 0.4)
toplab(s, X("mask_s"), X("mask_b"), K("mask"), K("trading") - 0.1, GOLD, LBL, 56)
tube = s.path("M 300 620 C 300 760 360 880 330 1020", "#9aa0a8", 4); s.draw(tube, K("mask") + 0.1, 0.5)
msk = s.raw(f'<path id="@ID@" d="M 300 1060 Q 300 1040 318 1040 L 350 1040 Q 368 1040 368 1060 L 362 1088 Q 334 1102 306 1088 Z" fill="{GOLD}" '
            f'style="opacity:0;filter:drop-shadow(0 0 10px rgba(232,194,106,0.9))"/>', "mk")
tl(f'tl.fromTo("#{msk}", {{opacity: 0, y: -360}}, {{opacity: 1, y: 0, duration: 0.6, ease: "bounce.out", immediateRender: false}}, {K("mask") + 0.3:.3f});')
cue(K("mask") + 0.6, "pop_1", -18)
for j, (key, x, h) in enumerate([("skill", 520, 150), ("savings", 700, 230), ("discipline", 900, 310)]):
    t = K(key) - 0.1
    b = s.raw(f'<rect id="@ID@" x="{x - 55}" y="{GY}" width="110" height="0" rx="10" fill="{GOLD}" fill-opacity="{0.55 + j * 0.2:.2f}" stroke="{GOLD}" stroke-width="3"/>', "bb")
    tl(f'tl.fromTo("#{b}", {{attr: {{y: {GY}, height: 0}}}}, {{attr: {{y: {GY - h}, height: {h}}}, duration: 0.5, ease: "back.out(1.4)", immediateRender: false}}, {t:.3f});')
    lb = tx(s, x, 1295, X(key), 28, WHITE, 0, 800, sp=0.06); s.fade(lb, t + 0.1, 0.3)
    cue(t, "pop_" + str(j + 2), -20)

# 4  "And in trading, never go all in on one position. Go all in on the process."
s = S(K("trading") - 0.1, K("truth") - 0.1, ground=False, restore=False)
toplab(s, X("allin_s"), X("allin_b"), K("trading"), K("process") - 0.1, RED, LBL, 50)
chips = "".join(f'<ellipse cx="540" cy="{960 - k * 22}" rx="78" ry="20" fill="{GOLD}" stroke="#6b5216" stroke-width="3"/>' for k in range(7))
ch = s.raw(f'<g id="@ID@" style="opacity:0">{chips}</g>', "ch")
tl(f'tl.fromTo("#{ch}", {{opacity: 0, x: -380}}, {{opacity: 1, x: 0, duration: 0.6, ease: "power3.out", immediateRender: false}}, {K("trading") + 0.3:.3f});')
bx = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(440, 990, 200, 120, 16)}" fill="#0f1319" stroke="#f4f4f2" stroke-width="3"/>'
           f'<text x="540" y="1062" text-anchor="middle" {FNT} font-size="{32 if TH_ else 30}" fill="#fff">{X("onetrade")}</text></g>', "bx")
s.fade(bx, K("trading") + 0.1, 0.3)
ai = pill(s, 540, 760, X("allin"), RED, "#fff", 30); s.pop(ai, K("trading") + 0.8, 0.35, 0.6, "50% 50%")
xx = s.path("M 400 760 L 680 1130 M 680 760 L 400 1130", RED, 10); s.draw(xx, K("process") - 0.5, 0.35)
cue(K("trading") + 0.3, "whoosh-short_1", -22); cue(K("process") - 0.5, "tock_1", -16)
for i_ in (ch, bx, ai, xx):
    hide(i_, K("process") - 0.1, 0.35)
toplab(s, X("proc_s"), X("proc_b"), K("process"), K("truth") - 0.1, GOLD, LBL, 66)
ring = s.raw(f'<circle id="@ID@" cx="540" cy="980" r="190" fill="none" stroke="{GOLD}" stroke-opacity="0.35" stroke-width="4" style="opacity:0"/>', "rg")
s.fade(ring, K("process"), 0.4)
arcd = s.path("M 540 790 A 190 190 0 0 1 730 980", GOLD, 7, style="opacity:0;filter:drop-shadow(0 0 10px rgba(232,194,106,0.9))", drawn=True)
s.fade(arcd, K("process") + 0.2, 0.3)
tl(f'tl.fromTo("#{arcd}", {{rotation: 0}}, {{rotation: 540, svgOrigin: "540 980", duration: {max(1.0, K("truth") - 0.4 - K("process") - 0.2):.3f}, ease: "none", immediateRender: false}}, {K("process") + 0.2:.3f});')
for j, (key, x, y) in enumerate([("p1", 540, 760), ("p2", 800, 990), ("p3", 540, 1222), ("p4", 280, 990)]):
    nd = pill(s, x, y, X(key), "#14110a", GOLD, 30); s.pop(nd, K("process") + 0.25 + j * 0.15, 0.35, 0.5, "50% 50%")
cue(K("process") + 0.25, "bell_E5", -20)

# 5  "Tell yourself the truth. I'm not where I want to be. I can study more. I can journal every trade. I can follow my rules..."
s = S(K("truth") - 0.1, K("three2") - 0.1, ground=False, hide=False, restore=False)
toplab(s, "", X("truth_b"), K("truth"), K("three2") - 0.1, WHITE, LBL, 54)
nw = tx(s, 540, 740, X("nw"), 34 if not TH_ else 36, GOLD, 0, 800, sp=0.02); s.fade(nw, K("notwhere") - 0.05, 0.4, y=10)
cue(K("notwhere"), "bell_C5", -22)
for j, (key, t) in enumerate([("c1", K("study")), ("c2", K("journal")), ("c3", K("rules"))]):
    y = 880 + j * 110
    s.raw(f'<rect x="170" y="{y - 34}" width="48" height="48" rx="10" fill="none" stroke="#f4f4f2" stroke-width="3"/>', "cb")
    lt = tx(s, 250, y, X(key), 34, WHITE, 0, 800, "start", sp=0.04); s.fade(lt, t - 0.1, 0.3)
    ck = s.path(f"M 180 {y - 12} L 194 {y + 4} L 212 {y - 26}", GOLD, 7); s.draw(ck, t + 0.4, 0.25)
    cue(t + 0.4, "tick_" + str(j + 1), -18)
if not TH_:
    hd = tx(s, 250, 1250, "EVEN ON THE HARD DAYS", 30, LBL, 0, 700, "start", sp=0.1); s.fade(hd, K("rules") + 0.5, 0.3)

# 6  "Do that for three years... and what you can do five, seven, twelve years from now... is hard to imagine."
s = S(K("three2") - 0.1, K("focused") - 0.1, ground=False, hide=False)
toplab(s, X("d3_s"), X("d3_b"), K("three2"), K("five") - 0.1, WHITE, LBL, 64)
toplab(s, X("y_s"), X("y_b"), K("five") - 0.1, K("imagine") - 0.1, GOLD, LBL, 60)
toplab(s, "", X("im_b"), K("imagine") - 0.1, K("focused") - 0.1, GOLD, LBL, 56)
s.raw(f'<path d="M 150 1250 H 950 M 150 1250 V 700" fill="none" stroke="#ffffff50" stroke-width="3"/>', "ax")
def cy(yr):
    return 1250 - 520 * ((1.3 ** yr - 1) / (1.3 ** 12 - 1))
def cx(yr):
    return 150 + yr * 66
seg1 = "M " + " L ".join(f"{cx(t / 4):.0f} {cy(t / 4):.0f}" for t in range(0, 13))
seg2 = "M " + " L ".join(f"{cx(t / 4):.0f} {cy(t / 4):.0f}" for t in range(12, 49))
p1 = s.path(seg1, "#e9ecf1", 5); s.draw(p1, K("three2") + 0.2, 0.9)
p2 = s.path(seg2, GOLD, 6, style="filter:drop-shadow(0 0 10px rgba(232,194,106,0.9))"); s.draw(p2, K("five") - 0.1, K("twelve") + 0.45 - K("five"), "power1.in")
for yr, key in [(3, "three2"), (5, "five"), (7, "seven"), (12, "twelve")]:
    t = K(key) + (0.6 if key == "three2" else (0.35 if key == "twelve" else 0))
    d = s.raw(f'<circle id="@ID@" cx="{cx(yr):.0f}" cy="{cy(yr):.0f}" r="12" fill="{GOLD if yr > 3 else WHITE}" style="opacity:0"/>', "dd")
    s.pop(d, t, 0.3, 0.3, "50% 50%")
    lb = tx(s, cx(yr), 1300, f"{yr}{X('yl')}", 30, GOLD if yr > 3 else WHITE, 0, 800, sp=0.04); s.fade(lb, t, 0.3)
    cue(t, "tick-crisp_" + str(min(3, max(1, yr // 4))), -20)

# 7  "So stay focused. Stay humble. Stay grounded."
s = S(K("focused") - 0.1, K("stacking") + 0.2)
s.spot(540, 1, "232,194,106")
f7 = s.fig(540, 1.0, GOLD); s.pop(f7, K("focused") - 0.1, 0.4)
for j, key in enumerate(["s1", "s2", "s3"]):
    t = K(["focused", "humble", "grounded"][j]) - (0.1 if j < 2 else 0.25)
    l = tx(s, 540, 640 + j * 90, X(key), 50, [WHITE, LBL, GOLD][j], 0, 800, sp=0.05); s.fade(l, t, 0.35, y=10)
    cue(t, "bell_" + ["C5", "E5", "G5"][j], -22)
gg = s.raw(f'<line id="@ID@" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="{GOLD}" stroke-width="4" style="opacity:0;filter:drop-shadow(0 0 8px rgba(232,194,106,0.9))"/>', "gg")
s.fade(gg, K("grounded"), 0.5)

# 8  "Keep stacking, one day at a time, no matter what anyone around you says."
s = S(K("stacking") + 0.15, K("order") + 0.35)
f8 = s.fig(540, 1.0, GOLD); s.pop(f8, K("stacking") + 0.15, 0.4)
toplab(s, X("st_s"), X("st_b"), K("stacking") + 0.15, K("noone") + 0.15, GOLD, LBL, 60)
NB = 6
span = max(2.4, K("noone") + 1.2 - K("stacking"))
for k in range(NB):
    t = K("stacking") + 0.3 + k * span / NB
    bl = s.raw(f'<rect id="@ID@" x="470" y="{GY - (k + 1) * 46}" width="140" height="42" rx="8" fill="#14110a" stroke="{GOLD}" stroke-width="3" style="opacity:0"/>', "sb")
    s.fade(bl, t, 0.15)
    tl(f'tl.to("#{f8}", {{y: {-(k + 1) * 46}, duration: 0.25, ease: "power2.out"}}, {t:.3f});')
    cue(t, "land-light_1", -24)
toplab(s, X("no_s"), X("no_b"), K("noone") + 0.15, K("order") + 0.35, WHITE, LBL, 52)
for j, x in enumerate([170, 910]):
    o = s.fig(x, 0.6, "#6b7079"); s.pop(o, K("noone") - 0.1, 0.35)
    bb = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(x - 60, 1000, 120, 60, 26)}" fill="#3a3f47"/>'
               f'<circle cx="{x - 24}" cy="1030" r="7" fill="#9aa0a8"/><circle cx="{x}" cy="1030" r="7" fill="#9aa0a8"/><circle cx="{x + 24}" cy="1030" r="7" fill="#9aa0a8"/></g>', "bu")
    s.pop(bb, K("noone") + 0.1 + j * 0.15, 0.3, 0.5, "50% 50%")
    hide(bb, K("noone") + 1.4, 0.5, 0.2); hide(o, K("noone") + 1.4, 0.5, 0.35)
cue(K("noone"), "pop_2", -24)

# 9  outro (handles, no end card; brand lines stay in English)
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
    <div id="root" data-composition-id="otm-selfish-th" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
{TIMELINE}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-selfish-th-audio" class="clip" src="assets/audio/mix_selfish_th.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-selfish-th"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
