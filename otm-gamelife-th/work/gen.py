"""OTM "Study the Game (life + trading)" (Thai version): the Thai-language edition of otm-gamelife, built from the same
scene file with LANG = "th". Thai narration (ElevenLabs "Patinya", calm Thai narrator), Thai on-screen text in Kanit
(OFL, assets/fonts); numbers stay in Montserrat; the outro keeps the brand lines in English. Motivation (school vs the
real world, understand how the game works) and the same game in trading. Original script, voice only, no music. Scenes
key off token indices of work/words.json (the script's tokens aligned to the voice; anchor table TH_ANC). Writes
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

LANG = "th"
# ---- shared scenes for "Study the Game (life + trading)" (English: otm-gamelife, Thai: otm-gamelife-th); LANG is set above
# Motivation first (school, the real world, how the game works), then the same game in trading.
def ix(i):
    return W(i)

TH_ = LANG == "th"
EN_ANC = dict(gota=8, ends=11, nobody=14, outhere=21, understand=34, who=43, want=45, where=49, trading=53,
              book=58, ind=63, pat=64, perf=65, last=68, game=73, quiet=75, wakes=80, stops=(85, 0.3), because=(90, 0.3), news=97, hits=(104, 0.15),
              hit=(104, 0.35), hardw=113, effort=(116, 0.15), noise=120, stopask=123, startask=131, inmarket=138, inlife=141,
              order=145, dont=148, follow=154)
TH_ANC = dict(gota=2, ends=3, nobody=4, outhere=5, understand=8, who=9, want=10, where=11, trading=(13, 0.35),
              book=(14, 0.3), ind=15, pat=16, perf=17, last=18, game=19, quiet=20, wakes=21, stops=(22, 0.25), because=(23, 0.45), news=24, hits=25,
              hit=(25, 0.4), hardw=(26, 0.5), effort=(27, 0.35), noise=28, stopask=29, startask=30, inmarket=31, inlife=32,
              order=33, dont=36, follow=37)

def K(key):
    a = (TH_ANC if TH_ else EN_ANC)[key]
    return ix(a[0]) + a[1] if isinstance(a, tuple) else ix(a)

TXT = dict(
    b_s=("MOST TRADERS STUDY", "เทรดเดอร์ส่วนใหญ่เรียนจาก"), b_b=("THE BOOK", "ตำรา"),
    bk1=("INDICATORS", "อินดิเคเตอร์"), bk2=("PATTERNS", "แพทเทิร์น"), bk3=("THE PERFECT ENTRY", "จุดเข้าที่สมบูรณ์แบบ"),
    g_s=("THE ONES WHO LAST STUDY", "แต่คนที่อยู่รอด ศึกษา"), g_b=("THE GAME", "เกม"),
    q_s=("THEY KNOW WHEN THE MARKET IS", "เขารู้ว่าตลาด"), q_b=("QUIET", "เงียบตอนไหน"), wk_b=("AND WHEN IT WAKES UP", "และตื่นตอนไหน"),
    quiet=("QUIET HOURS", "ช่วงเงียบ"), open=("THE OPEN", "ตลาดเปิด"),
    sl_s=("THEY KNOW WHERE", "เขารู้ว่า"), sl_b=("THE STOP LOSSES SIT", "สต็อปลอสกองอยู่ตรงไหน"),
    pl_s=("BECAUSE THAT'S WHERE", "เพราะนั่นคือที่ที่"), pl_b=("PRICE LIKES TO GO", "ราคาชอบวิ่งไปหา"),
    liq=("LIQUIDITY", "สภาพคล่อง"),
    nw_s=("THEY KNOW WHICH NEWS CAN MOVE PRICE", "เขารู้ว่าข่าวไหนขยับราคาได้"), nw_b=("IN SECONDS", "ในไม่กี่วินาที"),
    ht_s=("AND THEY'RE NOT IN A TRADE", "และเขาไม่มีออเดอร์ค้าง"), ht_b=("WHEN IT HITS", "ตอนข่าวออก"),
    news=("HIGH-IMPACT NEWS", "ข่าวแรง"), flat=("NO POSITION", "ไม่มีออเดอร์"),
    wh_s=("EVERYONE ELSE", "คนอื่น"), wh_b=("WORKS HARD", "ทำงานหนัก"),
    scr=("SCREEN TIME", "เวลาหน้าจอ"), crs=("NEW COURSE", "คอร์สใหม่"),
    sy_s=("THE MARKET DOESN'T HAND YOU", "ตลาดไม่ได้แจก"), sy_b=("A SYLLABUS", "ตำราเรียนให้ใคร"),
    gr_b=("NOBODY GRADES YOUR EFFORT", "ไม่มีใครให้คะแนนความพยายาม"),
    syl=("SYLLABUS", "ตำราเรียน"), eff=("EFFORT", "ความพยายาม"),
    sa_b=("STOP ASKING", "เลิกถามว่า"), st_b=("START ASKING", "เริ่มถามว่า"),
    qa=("HOW HARD SHOULD I WORK?", "ต้องทำงานหนักแค่ไหน?"), qb1=("HOW DOES THE GAME", "เกมนี้ทำงาน"), qb2=("ACTUALLY WORK?", "ยังไงจริงๆ?"),
    sub=("DON'T LET THE MARKET ORDER YOU", "อย่าให้ตลาดเป็นฝ่ายสั่งคุณ"),
    s1_s=("IN SCHOOL, THE KID WHO MEMORIZED THE BOOK", "ตอนเรียน เด็กที่ท่องตำราได้"), s1_b=("GOT THE A", "ได้เกรดเอ"),
    e_s=("BUT SCHOOL ENDS", "แต่พอเรียนจบ"), e_b=("NO ONE HANDS YOU A SYLLABUS", "ไม่มีใครแจกตำราเรียนให้อีกแล้ว"),
    o_s=("OUT HERE, THE WINNERS AREN'T", "ในชีวิตจริง คนที่ชนะ ไม่ใช่"), o_b=("THE HARDEST WORKERS", "คนที่ทำงานหนักที่สุด"),
    u_s=("THEY'RE THE ONES WHO UNDERSTAND", "แต่เป็นคนที่เข้าใจว่า"), u_b=("HOW THE GAME WORKS", "เกมนี้ทำงานยังไง"),
    qq1=("WHO DECIDES?", "ใครเป็นคนตัดสิน?"), qq2=("WHAT DO THEY WANT?", "เขาต้องการอะไร?"), qq3=("WHERE'S THE REAL OPPORTUNITY?", "โอกาสจริงๆ อยู่ตรงไหน?"),
    tr_s=("TRADING IS", "การเทรดก็คือ"), tr_b=("THE SAME GAME", "เกมเดียวกัน"),
    hw_b=("HARD WORK MATTERS", "การทำงานหนักสำคัญ"), ef_s=("BUT EFFORT WITHOUT UNDERSTANDING", "แต่ความพยายามที่ไม่มีความเข้าใจ"),
    ef_b=("IS JUST NOISE", "ก็แค่เสียงรบกวน"), noise=("NOISE", "เสียงรบกวน"),
    im=("IN THE MARKET", "ในตลาด"), il=("IN YOUR LIFE", "ในชีวิตคุณ"))

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
# L1  "In school, the kid who memorized the book got the A."
s = S(0, K("ends") - 0.1, first=True)
a1 = tx(s, 540, 488, X("s1_s"), 28, LBL, 1, 700, sp=0.12)
b1 = tx(s, 540, 560, X("s1_b"), 66, GOLD, 0, 800, sp=0.04); s.fade(b1, K("gota"), 0.3, y=10)
for i in (a1, b1):
    tl(f'tl.to("#{i}", {{opacity: 0, duration: 0.15}}, {K("ends") - 0.27:.3f});')
for r, (gy, sc) in enumerate(((1020, 0.55), (1236, 0.62))):
    for c, x in enumerate((290, 540, 790)):
        s.fig(x, sc, WHITE if (r, c) != (1, 1) else WHITE, 0.55 if (r, c) != (1, 1) else 1, glow=(r, c) == (1, 1), gy=gy - 30)
        w = 190 if r else 170
        s.raw(f'<rect x="{x - w // 2}" y="{gy - 60}" width="{w}" height="22" rx="6" fill="#2a3038" stroke="#5c6168" stroke-width="2"/>'
              f'<line x1="{x - w // 2 + 16}" y1="{gy - 38}" x2="{x - w // 2 + 16}" y2="{gy}" stroke="#5c6168" stroke-width="4"/>'
              f'<line x1="{x + w // 2 - 16}" y1="{gy - 38}" x2="{x + w // 2 - 16}" y2="{gy}" stroke="#5c6168" stroke-width="4"/>', "dk")
bkk = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(500, 1150, 80, 26, 4)}" fill="#151a22" stroke="#c9ced6" stroke-width="2"/></g>', "bk")
s.pop(bkk, 0.6, 0.35, 0.5, "50% 100%")
ap = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 16px rgba(232,194,106,0.9))"><path d="{rrect(600, 900, 130, 160, 10)}" fill="#e9e4d8"/>'
           f'<text x="665" y="1000" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="60" fill="#a3122a">A+</text></g>', "ap")
s.pop(ap, K("gota") + 0.1, 0.4, 0.4, "50% 50%"); cue(K("gota") + 0.1, "bell_C5", -18)

# L2  "But school ends... and nobody hands you a syllabus anymore."
s = S(K("ends") - 0.1, K("outhere") - 0.1)
toplab(s, X("e_s"), X("e_b"), K("ends"), K("outhere") - 0.1, WHITE, LBL, 50, tb=K("nobody"))
f2 = s.fig(300, 1.0, WHITE, 1)
for j, (x, dx, rot) in enumerate(((260, -60, -30), (540, 20, 25), (800, 70, -20))):
    cap = s.raw(f'<g id="@ID@" style="opacity:0"><path d="M {x - 60} {1000} L {x} {975} L {x + 60} {1000} L {x} {1025} Z" fill="#1d2229" stroke="#c9ced6" stroke-width="3"/>'
                f'<line x1="{x + 40}" y1="{1007}" x2="{x + 46}" y2="{1050}" stroke="{GOLD}" stroke-width="3"/></g>', "cp")
    t = K("ends") + 0.15 + j * 0.12
    tl(f'tl.fromTo("#{cap}", {{opacity: 0, y: 0, x: 0, rotation: 0}}, {{opacity: 1, y: -260, x: {dx}, rotation: {rot}, transformOrigin: "50% 50%", duration: 0.9, ease: "power2.out", immediateRender: false}}, {t:.3f});')
    tl(f'tl.to("#{cap}", {{opacity: 0, duration: 0.4}}, {t + 0.9:.3f});')
cue(K("ends") + 0.15, "whoosh-short_3", -22)
pp = s.raw(f'<g id="@ID@" style="opacity:0"><g transform="rotate(4 690 990)"><path d="{rrect(530, 780, 320, 420, 14)}" fill="#e9e4d8" stroke="#c9ced6" stroke-width="2"/>'
           + "".join(f'<line x1="570" y1="{870 + k * 50}" x2="{800 - (k % 3) * 40}" y2="{870 + k * 50}" stroke="#c4bdae" stroke-width="6" stroke-dasharray="2 18" stroke-linecap="round"/>' for k in range(6))
           + '</g></g>', "pp")
s.pop(pp, K("nobody") + 0.1, 0.4, 0.6, "50% 50%")
ppt = tx(s, 690, 845, X("syl"), 30, "#3a3f47", 0, 800, sp=0.08); s.fade(ppt, K("nobody") + 0.2, 0.3)
qm = s.label(690, 1060, "?", 130, "#9a927f", 0, 800, 0); s.pop(qm, K("nobody") + 0.7, 0.4, 0.3, "50% 50%"); cue(K("nobody") + 0.7, "tock_1", -20)

# L3  "Out here, the people who win aren't the ones who work the hardest. They're the ones who understand how the game works."
s = S(K("outhere") - 0.1, K("who") - 0.1)
toplab(s, X("o_s"), X("o_b"), K("outhere"), K("understand") - 0.1, WHITE, LBL, 56)
toplab(s, X("u_s"), X("u_b"), K("understand"), K("who") - 0.1, GOLD, LBL, 60)
s.raw(f'<g id="@ID@"><path d="{rrect(150, 1238, 260, 24, 12)}" fill="#1d2229" stroke="#ffffff60" stroke-width="2"/>'
      f'<line x1="400" y1="1238" x2="440" y2="1080" stroke="#ffffff80" stroke-width="6" stroke-linecap="round"/>'
      f'<line x1="420" y1="1086" x2="470" y2="1086" stroke="#ffffff80" stroke-width="6" stroke-linecap="round"/></g>', "tm")
belt = s.raw(f'<line id="@ID@" x1="162" y1="1250" x2="398" y2="1250" stroke="{GOLD}" stroke-width="4" stroke-dasharray="14 14"/>', "bl")
dur3 = K("who") - K("outhere")
tl(f'tl.fromTo("#{belt}", {{strokeDashoffset: 0}}, {{strokeDashoffset: 300, duration: {dur3:.3f}, ease: "none", immediateRender: false}}, {K("outhere") - 0.1:.3f});')
fw = s.fig(280, 1.0, WHITE, 1, gy=1236)
tl(f'tl.to("#{fw}", {{y: -8, duration: 0.16, yoyo: true, repeat: {int(dur3 / 0.32) * 2 - 1}, ease: "sine.inOut"}}, {K("outhere"):.3f});')
fg = s.fig(800, 1.0, GOLD); s.pop(fg, K("understand"), 0.4)
mp = s.raw(f'<path id="@ID@" d="{rrect(620, 720, 360, 300, 20)}" fill="#0f1319" stroke="{GOLD}" stroke-width="3" style="opacity:0;filter:drop-shadow(0 0 14px rgba(232,194,106,0.45))"/>', "mp")
s.pop(mp, K("understand") + 0.2, 0.4, 0.6, "50% 50%")
route = s.path("M 660 980 C 720 980 700 900 770 900 S 840 840 860 800 L 930 760", GOLD, 5, style="filter:drop-shadow(0 0 8px rgba(232,194,106,0.9))")
s.draw(route, K("understand") + 0.5, 1.0)
star = s.raw(f'<path id="@ID@" d="M 930 735 L 938 752 L 956 754 L 942 766 L 947 784 L 930 774 L 913 784 L 918 766 L 904 754 L 922 752 Z" fill="{GOLD}" style="opacity:0"/>', "st")
s.pop(star, K("understand") + 1.5, 0.35, 0.4, "50% 50%"); cue(K("understand") + 1.5, "bell_E5", -18)

# L4  "Who decides? What do they want? Where's the real opportunity?"
s = S(K("who") - 0.1, K("trading") - 0.1, ground=False)
for j, (key, k_) in enumerate((("qq1", "who"), ("qq2", "want"), ("qq3", "where"))):
    y = 700 + j * 170
    cq = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 14px rgba(232,194,106,0.4))"><path d="{rrect(130, y - 60, 820, 120, 24)}" fill="#14110a" stroke="{GOLD}" stroke-width="3"/>'
               f'<circle cx="195" cy="{y}" r="30" fill="none" stroke="{GOLD}" stroke-width="4"/></g>', "cq")
    qn = s.label(195, y + 16, "?", 44, GOLD, 0, 800, 0)
    qt = tx(s, 248, y + 12, X(key), 33, WHITE, 0, 800, "start", sp=0.02)
    s.pop(cq, K(k_), 0.35, 0.7, "50% 50%"); s.fade(qn, K(k_) + 0.05, 0.3); s.fade(qt, K(k_) + 0.1, 0.3)
    cue(K(k_), "pop_" + str(j + 1), -20)

# L5  "Trading is the same game."
s = S(K("trading") - 0.1, K("book") - 0.1)
toplab(s, X("tr_s"), X("tr_b"), K("trading"), K("book") - 0.1, GOLD, LBL, 70)
s.spot(300, 1, "232,194,106", 30, 150)
s.fig(300, 1.0, GOLD, 1)
bd5 = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 18px rgba(232,194,106,0.45))"><path d="{rrect(500, 820, 420, 400, 22)}" fill="#0f1319" stroke="{GOLD}" stroke-width="3"/>'
            + "".join(f'<line x1="{500 + k * 70}" y1="820" x2="{500 + k * 70}" y2="1220" stroke="#ffffff14" stroke-width="2"/>' for k in range(1, 6))
            + "".join(f'<line x1="500" y1="{820 + k * 80}" x2="920" y2="{820 + k * 80}" stroke="#ffffff14" stroke-width="2"/>' for k in range(1, 5)) + '</g>', "bd")
s.pop(bd5, K("trading") + 0.1, 0.45, 0.7, "50% 50%")
ch5 = s.path("M 530 1150 L 580 1110 L 620 1130 L 670 1060 L 710 1080 L 760 990 L 800 1020 L 850 930 L 890 880", GOLD, 5, style="filter:drop-shadow(0 0 8px rgba(232,194,106,0.9))")
s.draw(ch5, K("trading") + 0.4, 0.9); cue(K("trading"), "bell_G5", -18)

# 1  "Most traders study the book. Indicators. Patterns. The perfect entry."
s = S(K("book") - 0.1, K("last") - 0.1)
toplab(s, X("b_s"), X("b_b"), K("book"), K("last") - 0.1, WHITE, LBL, 66)
s.fig(300, 1.0, WHITE, 1)
for k, (key, k_, rot) in enumerate((("bk1", "ind", -2), ("bk2", "pat", 3), ("bk3", "perf", -1))):
    y = 1170 - k * 72
    bk = s.raw(f'<g id="@ID@" style="opacity:0"><g transform="rotate({rot} 700 {y + 35})"><path d="{rrect(520, y, 360, 68, 10)}" fill="#151a22" '
               f'stroke="#c9ced6" stroke-width="3"/><rect x="532" y="{y + 8}" width="10" height="52" fill="#c9ced6" opacity="0.6"/></g></g>', "bk")
    bt = tx(s, 710, y + 45, X(key), 28, WHITE, 0, 800, sp=0.05)
    s.pop(bk, K(k_), 0.35, 0.6, "50% 100%"); s.fade(bt, K(k_) + 0.05, 0.3); cue(K(k_), "land-light_1", -18)

# 2  "The ones who last study the game."
s = S(K("last") - 0.1, K("quiet") - 0.1)
toplab(s, X("g_s"), X("g_b"), K("last"), K("quiet") - 0.1, GOLD, LBL, 70, tb=K("game"))
s.spot(300, 1, "232,194,106", 30, 150)
f2 = s.fig(300, 1.0, GOLD, 1)
bd = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 18px rgba(232,194,106,0.45))"><path d="{rrect(500, 820, 420, 400, 22)}" fill="#0f1319" stroke="{GOLD}" stroke-width="3"/>'
           + "".join(f'<line x1="{500 + k * 70}" y1="820" x2="{500 + k * 70}" y2="1220" stroke="#ffffff14" stroke-width="2"/>' for k in range(1, 6))
           + "".join(f'<line x1="500" y1="{820 + k * 80}" x2="920" y2="{820 + k * 80}" stroke="#ffffff14" stroke-width="2"/>' for k in range(1, 5)) + '</g>', "bd")
s.pop(bd, K("last") + 0.3, 0.45, 0.7, "50% 50%")
ic1 = s.raw(f'<g id="@ID@" style="opacity:0"><circle cx="610" cy="930" r="44" fill="none" stroke="{GOLD}" stroke-width="5"/>'
            f'<line x1="610" y1="930" x2="610" y2="900" stroke="{GOLD}" stroke-width="5" stroke-linecap="round"/><line x1="610" y1="930" x2="632" y2="940" stroke="{GOLD}" stroke-width="5" stroke-linecap="round"/></g>', "ia")
ic2 = s.raw(f'<g id="@ID@" style="opacity:0">' + "".join(f'<path d="{rrect(730 + j * 18, 890 + j * 24, 140, 44, 22)}" fill="#1a0f12" stroke="{RED}" stroke-width="3"/>' for j in range(2))
            + f'<text x="818" y="946" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" fill="{RED}">STOP</text></g>', "ib")
ic3 = s.raw(f'<path id="@ID@" d="M 712 1040 L 672 1120 L 706 1120 L 690 1190 L 752 1094 L 716 1094 L 740 1040 Z" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 12px rgba(232,194,106,0.9))"/>', "ic")
for j, i in enumerate((ic1, ic2, ic3)):
    s.pop(i, K("last") + 0.8 + j * 0.25, 0.35, 0.5, "50% 50%"); cue(K("last") + 0.8 + j * 0.25, "pop_" + str(j + 1), -20)
mg = s.raw(f'<g id="@ID@" style="opacity:0"><circle cx="430" cy="960" r="54" fill="none" stroke="#f4f4f2" stroke-width="7"/>'
           f'<line x1="392" y1="998" x2="350" y2="1040" stroke="#f4f4f2" stroke-width="12" stroke-linecap="round"/></g>', "mg")
s.pop(mg, K("game"), 0.4, 0.5, "50% 50%")
tl(f'tl.to("#{mg}", {{x: 30, y: -14, duration: 0.7, yoyo: true, repeat: 1, ease: "sine.inOut"}}, {K("game") + 0.5:.3f});')

# 3  "They know when the market is quiet... and when it wakes up."
s = S(K("quiet") - 0.1, K("stops") - 0.1, ground=False, restore=False)
toplab(s, X("q_s"), X("q_b"), K("quiet"), K("wakes") - 0.1, LBL, LBL, 64)
qs3 = tx(s, 540, 488, X("q_s"), 28, LBL, 0, 700, sp=0.12); tl(f'tl.set("#{qs3}", {{opacity: 1}}, {K("wakes") - 0.17:.3f});')
hide(qs3, K("stops") - 0.27, 0.15)
toplab(s, "", X("wk_b"), K("wakes"), K("stops") - 0.1, GOLD, LBL, 56)
s.raw(f'<line x1="140" y1="1000" x2="940" y2="1000" stroke="#ffffff22" stroke-width="2" stroke-dasharray="6 10"/>', "bl")
flat = "M 140 1000 " + " ".join(f"L {150 + k * 20} {1000 + (6 if k % 2 else -6)}" for k in range(1, 21))
pf = s.path(flat, "#9aa0a8", 4); s.draw(pf, K("quiet") + 0.1, max(1.0, K("wakes") - 0.3 - K("quiet")), "none")
ql = tx(s, 345, 1080, X("quiet"), 30, LBL, 0, 700, sp=0.1); s.fade(ql, K("quiet") + 0.4, 0.3)
ol = s.raw(f'<line id="@ID@" x1="560" y1="760" x2="560" y2="1300" stroke="{GOLD}" stroke-width="3" stroke-dasharray="10 8" style="opacity:0"/>', "ol")
s.fade(ol, K("wakes") - 0.1, 0.3)
olb = tx(s, 580, 790, X("open"), 32, GOLD, 0, 800, "start", sp=0.08); s.fade(olb, K("wakes") - 0.05, 0.3)
rr = random.Random(9)
vpts, y = [], 1000
for k in range(1, 20):
    y += rr.choice((-1, 1)) * rr.uniform(30, 70) - 8
    y = min(1180, max(820, y))
    vpts.append((560 + k * 20, y))
pv = s.path("M 560 1000 " + " ".join(f"L {x} {y:.0f}" for x, y in vpts), GOLD, 5, style="filter:drop-shadow(0 0 10px rgba(232,194,106,0.9))")
s.draw(pv, K("wakes") + 0.1, 0.9, "none"); cue(K("wakes"), "bell_C5", -18)
for k in range(20):
    h = 14 + (k * 7) % 12 if k < 10 else 60 + (k * 37) % 90
    vb = s.raw(f'<rect id="@ID@" x="{146 + k * 40}" y="{1320 - h}" width="26" height="{h}" rx="4" fill="{GOLD if k >= 10 else "#5c6168"}" style="opacity:0"/>', "vb")
    s.fade(vb, (K("quiet") + 0.2 + k * 0.08) if k < 10 else (K("wakes") + 0.15 + (k - 10) * 0.08), 0.2)

# 4  "They know where the stop losses are sitting... because that's where price likes to go."
s = S(K("stops") - 0.1, K("news") - 0.1, ground=False, hide=False, restore=False)
toplab(s, X("sl_s"), X("sl_b"), K("stops"), K("because") - 0.1, WHITE, LBL, 56)
toplab(s, X("pl_s"), X("pl_b"), K("because"), K("news") - 0.1, GOLD, LBL, 60)
rng = "M 140 900 L 200 960 L 260 1000 L 320 930 L 380 880 L 440 950 L 500 1000 L 560 940 L 620 900"
p1 = s.path(rng, "#c9ced6", 5); s.draw(p1, K("stops") + 0.1, 1.0)
ll = s.raw(f'<line id="@ID@" x1="200" y1="1002" x2="760" y2="1002" stroke="#ffffff80" stroke-width="3" stroke-dasharray="10 8" style="opacity:0"/>', "ll")
s.fade(ll, K("stops") + 0.8, 0.3)
tags = []
for j, (tx_, ty) in enumerate(((250, 1052), (380, 1052), (510, 1052), (640, 1052), (315, 1108), (445, 1108), (575, 1108))):
    tg = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(tx_ - 58, ty - 21, 116, 42, 21)}" fill="#1a0f12" stroke="{RED}" stroke-width="3"/>'
               f'<text x="{tx_}" y="{ty + 10}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" fill="{RED}">STOP</text></g>', "sg")
    s.pop(tg, K("stops") + 0.9 + j * 0.1, 0.3, 0.5, "50% 50%"); tags.append(tg)
cue(K("stops") + 0.9, "tick-crisp_1", -22)
t_w = K("because") + 0.4
p2 = s.path("M 620 900 L 680 960 L 720 1140 L 760 1030 L 820 900 L 880 800 L 940 760", GOLD, 6, style="filter:drop-shadow(0 0 10px rgba(232,194,106,0.9))")
s.draw(p2, t_w, 1.0); cue(t_w + 0.35, "whoosh-short_2", -20)
for j, tg in enumerate(tags):
    tl(f'tl.to("#{tg}", {{opacity: 0, scale: 0.4, transformOrigin: "50% 50%", duration: 0.25}}, {t_w + 0.35 + j * 0.05:.3f});')
lq = tx(s, 450, 1200, X("liq"), 34, GOLD, 0, 800, sp=0.1); s.fade(lq, t_w + 0.6, 0.3); cue(t_w + 0.6, "bell_E5", -20)

# 5  "They know which news can move price in seconds... and they're not in a trade when it hits."
s = S(K("news") - 0.1, K("hardw") - 0.1, ground=False, hide=False)
toplab(s, X("nw_s"), X("nw_b"), K("news"), K("hits") - 0.1, WHITE, LBL, 60)
toplab(s, X("ht_s"), X("ht_b"), K("hits"), K("hardw") - 0.1, GOLD, LBL, 60)
nc = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 14px rgba(255,77,94,0.6))"><path d="{rrect(150, 650, 780, 110, 20)}" fill="#1a0f12" stroke="{RED}" stroke-width="3"/>'
           f'<circle cx="200" cy="705" r="14" fill="{RED}"/></g>', "nc")
s.pop(nc, K("news") + 0.2, 0.4, 0.6, "50% 50%")
nl = tx(s, 236, 718, X("news"), 34, WHITE, 0, 800, "start", sp=0.06); s.fade(nl, K("news") + 0.3, 0.3)
t_hit = K("hit")
cds = []
for j in range(3):
    c = num(s, 900, 724, f"0:0{3 - j}", 40, RED, 0, "end"); cds.append(c)
c0 = num(s, 900, 724, "0:00", 40, RED, 0, "end")
for j, c in enumerate(cds + [c0]):
    t = t_hit - 3 * 0.55 + j * 0.55
    tl(f'tl.set("#{c}", {{opacity: 1}}, {t:.3f});')
    if j < 3:
        tl(f'tl.set("#{c}", {{opacity: 0}}, {t + 0.55:.3f});')
        cue(t, "tick_" + str(j + 1), -24)
s.raw(f'<line x1="140" y1="1050" x2="940" y2="1050" stroke="#ffffff22" stroke-width="2" stroke-dasharray="6 10"/>', "bl")
calm = "M 140 1050 " + " ".join(f"L {150 + k * 20} {1050 + (5 if k % 2 else -5)}" for k in range(1, 18))
pc = s.path(calm, "#9aa0a8", 4); s.draw(pc, K("news") + 0.4, max(1.0, t_hit - 0.2 - K("news") - 0.4), "none")
spike = "M 490 1050 L 520 820 L 545 1260 L 575 880 L 600 1220 L 630 960 L 660 1150 L 700 1000 L 760 1080 L 820 1020"
ps = s.path(spike, RED, 6, style="filter:drop-shadow(0 0 12px rgba(255,77,94,0.9))"); s.draw(ps, t_hit, 0.5, "power1.out")
cue(t_hit, "land_1", -14)
f5 = s.fig(880, 0.62, GOLD, 1, gy=1290)
np_ = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 12px rgba(232,194,106,0.8))"><path d="{rrect(640, 1320, 340, 66, 33)}" fill="#14110a" stroke="{GOLD}" stroke-width="3"/>'
            f'<path d="M 668 1353 L 680 1365 L 702 1341" fill="none" stroke="{GOLD}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></g>', "np")
npl = tx(s, 830, 1364, X("flat"), 28, GOLD, 0, 800, sp=0.06)
s.pop(np_, t_hit + 0.5, 0.35, 0.6, "50% 50%"); s.fade(npl, t_hit + 0.55, 0.3); cue(t_hit + 0.5, "bell_G5", -20)

# N  "Hard work matters. But effort without understanding... is just noise."
s = S(K("hardw") - 0.1, K("stopask") - 0.1)
toplab(s, "", X("hw_b"), K("hardw"), K("effort") - 0.1, WHITE, LBL, 62)
toplab(s, X("ef_s"), X("ef_b"), K("effort"), K("stopask") - 0.1, RED, LBL, 60, tb=K("noise"))
f6 = s.fig(250, 1.0, WHITE, 1)
tl(f'tl.to("#{f6}", {{y: -6, duration: 0.12, yoyo: true, repeat: {int((K("stopask") - K("hardw")) / 0.24) * 2 - 1}, ease: "sine.inOut"}}, {K("hardw") + 0.1:.3f});')
sc = s.raw(f'<path id="@ID@" d="{rrect(150, 700, 300, 150, 20)}" fill="#0f1319" stroke="#ffffff60" stroke-width="2" style="opacity:0"/>', "sc")
s.fade(sc, K("hardw") + 0.2, 0.3)
scl = tx(s, 300, 745, X("scr"), 28, LBL, 0, 700, sp=0.1); s.fade(scl, K("hardw") + 0.2, 0.3)
for j, h in enumerate(("2H", "6H", "9H", "12H")):
    v = num(s, 300, 822, h, 56, RED if j == 3 else WHITE)
    t = K("hardw") + 0.4 + j * 0.6
    tl(f'tl.set("#{v}", {{opacity: 1}}, {t:.3f});')
    if j < 3: tl(f'tl.set("#{v}", {{opacity: 0}}, {t + 0.6:.3f});')
    cue(t, "tick-crisp_" + str(j % 3 + 1), -24)
for j in range(3):
    y = 1170 - j * 64
    cc = s.raw(f'<g id="@ID@" style="opacity:0"><g transform="rotate({(-4, 3, -2)[j]} 740 {y + 28})"><path d="{rrect(560, y, 360, 56, 12)}" fill="#151a22" stroke="#c9ced6" stroke-width="2"/></g></g>', "cc")
    t = K("hardw") + 0.5 + j * 0.25
    s.pop(cc, t, 0.3, 0.6, "50% 100%"); cue(t, "land-light_1", -24)
    ct = tx(s, 740, y + 38, f'{X("crs")} #{j + 1}', 28, WHITE, 0, 800, sp=0.05); s.fade(ct, t + 0.05, 0.2)
rz = random.Random(4)
nz = "M 150 940 " + " ".join(f"L {150 + k * 20} {940 + rz.uniform(-40, 40):.0f}" for k in range(1, 40))
pn = s.path(nz, RED, 3, style="opacity:0.9")
s.draw(pn, K("noise") - 0.2, 0.6, "none"); cue(K("noise"), "swell_2", -22)
nlb = tx(s, 930, 1010, X("noise"), 32, RED, 0, 800, "end", sp=0.1); s.fade(nlb, K("noise") + 0.3, 0.3)

# F  "So stop asking how hard you should work. Start asking how the game actually works. In the market... and in your life."
s = S(K("stopask") - 0.1, K("order") + 0.35, ground=False)
toplab(s, "", X("sa_b"), K("stopask"), K("startask") - 0.1, RED, LBL, 62)
toplab(s, "", X("st_b"), K("startask"), K("order") + 0.35, GOLD, LBL, 62)
c1 = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(150, 680, 780, 150, 26)}" fill="#1a0f12" stroke="{RED}" stroke-width="3"/></g>', "c1")
s.pop(c1, K("stopask") + 0.1, 0.4, 0.7, "50% 50%")
q1 = tx(s, 540, 772, X("qa"), 40, WHITE, 0, 800, sp=0.03); s.fade(q1, K("stopask") + 0.2, 0.3)
k1 = s.path("M 190 757 H 890", RED, 6); s.draw(k1, K("startask") - 0.4, 0.35); cue(K("startask") - 0.4, "tock_1", -18)
c2 = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 18px rgba(232,194,106,0.45))"><path d="{rrect(150, 900, 780, 220, 26)}" fill="#14110a" stroke="{GOLD}" stroke-width="4"/></g>', "c2")
s.pop(c2, K("startask") + 0.1, 0.45, 0.7, "50% 50%")
q2 = tx(s, 540, 1000, X("qb1"), 40, GOLD, 0, 800, sp=0.03); s.fade(q2, K("startask") + 0.2, 0.3)
q3 = tx(s, 540, 1070, X("qb2"), 40, GOLD, 0, 800, sp=0.03); s.fade(q3, K("startask") + 0.6, 0.3)
pm = s.pill(330, 1230, X("im"), GOLD, "#111", 34)
if TH_: thai(s)
s.pop(pm, K("inmarket"), 0.35, 0.6, "50% 50%"); cue(K("inmarket"), "pop_1", -18)
pl_ = s.pill(750, 1230, X("il"), WHITE, "#111", 34)
if TH_: thai(s)
s.pop(pl_, K("inlife"), 0.35, 0.6, "50% 50%"); cue(K("inlife"), "bell_C5", -18)
cue(K("startask") + 0.1, "bell_E5", -20)

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
    <div id="root" data-composition-id="otm-gamelife-th" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
{TIMELINE}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-gamelife-th-audio" class="clip" src="assets/audio/mix_gamelife_th.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-gamelife-th"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
