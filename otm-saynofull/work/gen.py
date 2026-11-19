"""OTM "Say No (full)": the full-length version of "Say No", one video that brings the last three OTM videos together
(The Last $1,000, Stop Strategy Hopping, The Skill of Doing Nothing). Most of trading is what you refuse to do; the
market tempts you three ways and each chapter says no and shows why. 1) Risk more, win it back faster: down to your
last $1,000, survive first, risk 1% a trade (five losses cost $50, still standing); slow growth never killed a small
account, big ambition does. 2) Three losses, try a new strategy: the loss/new-strategy cycle, nothing gets enough
trades, every strategy has losing streaks, keep it boring (same setup, same risk, same rules). 3) Bored, just take
something: watch two hours and close the screen; forced entries feel like progress but are just activity; the market
pays for being picky, not busy. No, no and no: that's the job. English version (Quentin); otm-saynofull-th is the
Thai version from the same scene file. Original script, voice only, no music. Scenes key off word indices of
work/words.json (anchor table EN_ANC, helper K). Writes ../index.html, work/cues.json and work/timing.json."""
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
# ---- shared scenes for "Say No (full)" (English: otm-saynofull, Thai: otm-saynofull-th); LANG is set just above this line
# One video built from the last three: three temptations, each a chapter (The Last $1,000 / Stop Strategy Hopping /
# The Skill of Doing Nothing), each answered with a NO.
def ix(i):
    return W(i)

TH_ = LANG == "th"
# EN: word indices of work/words.json; TH: token indices of work/script.txt (aligned into work/words.json)
EN_ANC = dict(refuse=8, tempt=15, howto=23,
              one=(31, -0.85), q1=31, no1=38, imagine=39, last=45, urge=47, job=53, survive=61,
              risk1=64, less=70, five=72, cost=77, standing=80, slow=83, ambition=90,
              two=93, q2=94, no2=104, loss1=105, new1=107, loss2=109, new2=111, loss3=113, new3=115, nothing=117, show=123,
              streak=(128, 0.4), evengood=(133, -0.35), boring=(137, 0.3), same1=141, same2=143, same3=145, long=147,
              three=153, q3=154, no3=160, watch=161, seenothing=171, close=175,
              forced=179, bgrade=182, feel=185, activity=(188, -0.2), market=(191, 0.3), picky=(199, 0.2),
              noa=205, nob=206, noc=208, thejob=209, order=212, dont=215, follow=221)
TH_ANC = dict(refuse=1, tempt=2, howto=3,
              one=5, q1=6, no1=(8, 0.45), imagine=(9, 0.3), last=10, urge=11, job=12, survive=13,
              risk1=14, less=15, five=16, cost=17, standing=(18, -0.3), slow=(19, 0.35), ambition=20,
              two=21, q2=22, no2=(24, 0.45), loss1=(25, 0.3), new1=26, loss2=27, new2=28, loss3=29, new3=30, nothing=(31, 0.6), show=33,
              streak=(34, 0.4), evengood=(35, -0.3), boring=(36, 0.3), same1=37, same2=38, same3=39, long=40,
              three=41, q3=42, no3=(44, 0.45), watch=(45, 0.5), seenothing=47, close=48,
              forced=49, bgrade=50, feel=51, activity=(52, -0.3), market=(53, 0.35), picky=54,
              noa=55, nob=56, noc=57, thejob=(58, -0.35), order=59, dont=62, follow=63)

def K(key):
    a = (TH_ANC if TH_ else EN_ANC)[key]
    return ix(a[0]) + a[1] if isinstance(a, tuple) else ix(a)

TXT = dict(
    h_s=("MOST OF TRADING ISN'T ABOUT", "การเทรดส่วนใหญ่ไม่ได้อยู่ที่"), h_b=("WHAT YOU DO", "สิ่งที่คุณทำ"),
    r_s=("IT'S ABOUT WHAT YOU", "แต่อยู่ที่สิ่งที่คุณ"), r_b=("REFUSE TO DO", "ปฏิเสธ"),
    tm_s=("THE MARKET WILL TEMPT YOU", "ตลาดจะยั่วคุณ"), tm_b=("3 WAYS", "3 แบบ"),
    hw_s=("HERE'S HOW TO", "และนี่คือวิธี"), hw_b=("SAY NO TO EACH ONE", "บอกว่าไม่กับทุกแบบ"),
    tn=("TEMPTATION", "แบบที่"),
    t1b=("RISK MORE", "เสี่ยงเยอะขึ้น"), q1=("“WIN IT BACK FASTER”", "“จะได้ทุนคืนเร็วๆ”"), i1=("RISK 20%", "เสี่ยง 20%"),
    t2b=("TRY A NEW STRATEGY", "ลองระบบใหม่ดู"), q2=("“3 LOSSES IN A ROW...”", "“แพ้สามไม้ติด...”"),
    t3b=("JUST TAKE SOMETHING", "เข้าสักไม้เถอะ"), q3=("“BORED? JUST TAKE ONE”", "“เบื่อแล้ว เข้าสักไม้”"),
    no=("NO", "ไม่"), sn=("SAY NO.", "บอกว่าไม่"),
    im_s=("IMAGINE YOU'RE DOWN TO", "ลองนึกว่าคุณเหลือเงินก้อนสุดท้าย"), im_b=("YOUR LAST $1,000", "แค่ $1,000"),
    ur_s=("THE URGE", "ใจอยาก"), ur_b=("DOUBLE IT", "ทำให้เป็นสองเท่า"),
    j_s=("JOB #1 OF A SMALL ACCOUNT", "หน้าที่แรกของพอร์ตเล็ก"), j_b=("SURVIVE", "อยู่รอด"),
    p_s=("RISK PER TRADE", "ความเสี่ยงต่อไม้"), p_b=("1% OR LESS", "1% หรือน้อยกว่า"),
    risk10=("$10 AT RISK", "เสี่ยงแค่ $10"), bal=("BALANCE", "ยอดเงิน"),
    f_s=("5 LOSSES IN A ROW", "แพ้ห้าไม้ติด"), f_b=("STILL STANDING", "คุณยังยืนอยู่"),
    s_s=("SLOW GROWTH NEVER KILLED", "การโตช้าไม่เคยฆ่า"), s_b=("A SMALL ACCOUNT", "พอร์ตเล็ก"),
    a_b=("BIG AMBITION DOES.", "ความอยากรวยเร็วต่างหาก"), fast=("GET RICH FAST", "รวยเร็ว"),
    l1=("1 LOSS", "แพ้ 1 ไม้"), l2=("2 LOSSES", "แพ้ 2 ไม้"), l3=("3 LOSSES", "แพ้ 3 ไม้"),
    n1=("NEW STRATEGY", "เปลี่ยนกลยุทธ์"), n2=("NEW INDICATOR", "เปลี่ยนอินดิเคเตอร์"), n3=("NEW MENTOR", "เปลี่ยนเมนเทอร์"),
    ng_s=("NOTHING EVER GETS", "ไม่มีระบบไหน"), ng_b=("ENOUGH TRADES", "ได้เทรดนานพอ"),
    sh_b=("TO SHOW WHAT IT CAN DO", "ที่จะพิสูจน์ตัวเอง"), trades=("TRADES", "ไม้"),
    st_s=("EVERY STRATEGY HAS", "ทุกกลยุทธ์มี"), st_b=("LOSING STREAKS", "ช่วงแพ้ติดกัน"), eg_b=("EVEN A GOOD ONE", "แม้แต่กลยุทธ์ที่ดี"),
    kb_s=("SO KEEP IT", "ทำให้มัน"), kb_b=("BORING", "น่าเบื่อไว้"),
    sm1=("SAME SETUP", "เซ็ตอัพเดิม"), sm2=("SAME RISK", "ความเสี่ยงเดิม"), sm3=("SAME RULES", "กฎเดิม"),
    lg_b=("LONG ENOUGH TO LET IT WORK", "นานพอให้มันทำงาน"),
    w_s=("A GOOD TRADER CAN WATCH", "เทรดเดอร์ที่ดี นั่งดูกราฟได้"), w_b=("FOR 2 HOURS", "สองชั่วโมง"),
    s2_s=("SEE NOTHING WORTH TAKING", "ไม่เจออะไรที่น่าเข้า"), s2_b=("AND CLOSE THE SCREEN", "แล้วก็ปิดจอไป"),
    fs=("FORCED ENTRIES · B-GRADE SETUPS", "ฝืนเข้าเทรด · เซ็ตอัพแค่พอใช้"),
    fp_b=("FEEL LIKE PROGRESS", "ให้ความรู้สึกเหมือนก้าวหน้า"), ja_b=("THEY'RE JUST ACTIVITY", "แต่มันแค่ความยุ่ง"),
    f1=("FORCED ENTRY", "ฝืนเข้าเทรด"), f2=("B-GRADE SETUP", "เซ็ตอัพแค่พอใช้"),
    act=("ACTIVITY", "ความยุ่ง"), prog=("PROGRESS", "ความก้าวหน้า"),
    mk_s=("THE MARKET DOESN'T PAY YOU FOR", "ตลาดไม่ได้จ่ายเงินให้"), mk_b=("BEING BUSY", "คนที่ยุ่ง"),
    pk_s=("IT PAYS YOU FOR", "แต่จ่ายให้"), pk_b=("BEING PICKY", "คนที่เลือก"),
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

def stamp(s, cx, cy, w, h, size, rot):
    """the gold NO stamp (Kanit for Thai)"""
    return s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 18px rgba(232,194,106,0.85))"><g transform="rotate({rot} {cx} {cy})">'
                 f'<path d="{rrect(cx - w // 2, cy - h // 2, w, h, 22)}" fill="rgba(20,17,10,0.85)" stroke="{GOLD}" stroke-width="9"/>'
                 f'<text x="{cx}" y="{cy + size * 0.36:.0f}" text-anchor="middle" {FNT} font-size="{size}" fill="{GOLD}">{X("no")}</text></g></g>', "ns")

def card(s, cx, op=1, y=1090, w=220, h=130):
    """the $1,000 account card, standing on the ground"""
    return s.raw(f'<g id="@ID@" style="opacity:{op};filter:drop-shadow(0 0 16px rgba(232,194,106,0.45))">'
                 f'<path d="{rrect(cx - w // 2, y, w, h, 18)}" fill="#14110a" stroke="{GOLD}" stroke-width="3"/>'
                 f'<text x="{cx}" y="{y + h // 2 + 16}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="46" '
                 f'letter-spacing="0.02em" fill="{GOLD}">$1,000</text></g>', "cd")

def monitor(s, op=1):
    return s.raw(f'<g id="@ID@" style="opacity:{op}"><path d="{rrect(520, 760, 440, 300, 18)}" fill="#0f1319" stroke="#ffffffb0" stroke-width="3"/>'
                 f'<line x1="740" y1="1060" x2="740" y2="1236" stroke="#ffffff80" stroke-width="6"/>'
                 f'<line x1="680" y1="1236" x2="800" y2="1236" stroke="#ffffff80" stroke-width="6" stroke-linecap="round"/></g>', "mn")

CHOP = [(545, 920), (585, 895), (620, 930), (655, 900), (690, 925), (725, 890), (760, 922), (795, 897), (830, 928), (865, 902), (900, 924), (935, 905)]
CHOP_D = "M " + " L ".join(f"{x} {y}" for x, y in CHOP)

def temptation(n, ks, ke, gkw):
    """a red temptation card, then the gold NO stamp lands on it"""
    s = S(K(ks) - 0.1, K(ke) - 0.1, ground=False, **gkw)
    q, no = f"q{n}", f"no{n}"
    toplab(s, f'{X("tn")} {n}/3', X(f"t{n}b"), K(ks), K(no) - 0.35, RED, LBL, 56)
    toplab(s, "", X("sn"), K(no) - 0.35, K(ke) - 0.1, GOLD, LBL, 66)
    cd = s.raw(f'<path id="@ID@" d="{rrect(150, 660, 780, 300, 26)}" fill="#1a0f12" stroke="{RED}" stroke-width="3" '
               f'style="opacity:0;filter:drop-shadow(0 0 16px rgba(255,77,94,0.55))"/>', "cd")
    s.pop(cd, K(ks) + 0.15, 0.4, 0.7, "50% 50%")
    qt = tx(s, 540, 750, X(q), 40, WHITE, 0, 800, sp=0.03); s.fade(qt, K(q), 0.3)
    icons = []
    if n == 1:
        icons.append(tx(s, 600, 900, X("i1"), 64, RED, 0, 800, sp=0.03))
        icons.append(s.path("M 300 920 L 340 860 L 370 885 L 420 800 M 396 802 L 422 798 L 424 826", RED, 6))
    elif n == 2:
        for x in (420, 540, 660):
            icons.append(s.path(f"M {x - 30} 840 L {x + 30} 900 M {x + 30} 840 L {x - 30} 900", RED, 9))
    else:
        icons.append(s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(450, 830, 180, 80, 40)}" fill="{RED}" style="filter:drop-shadow(0 0 14px rgba(255,77,94,0.9))"/>'
                           f'<text x="540" y="884" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="40" fill="#fff">BUY</text></g>', "by"))
    for j, i in enumerate(icons):
        t = K(q) + 0.3 + j * 0.25
        s.draw(i, t, 0.3) if i.startswith("p") else s.pop(i, t, 0.35, 0.6, "50% 50%")
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

# 1  "Most of trading isn't about what you do. It's about what you refuse to do."
s = S(0, K("tempt") - 0.1, first=True)
toplab(s, X("h_s"), X("h_b"), 0, K("refuse") - 0.1, WHITE, LBL, 64, op=1)
toplab(s, X("r_s"), X("r_b"), K("refuse"), K("tempt") - 0.1, GOLD, LBL, 64)
s.spot(540, 1, "232,194,106", 30, 150)
s.fig(540, 1.0, GOLD, 1)
ring = s.path("M 540 950 A 175 175 0 1 1 539 950", GOLD, 5, style="filter:drop-shadow(0 0 12px rgba(232,194,106,0.9))")
s.draw(ring, K("refuse") + 0.4, 0.9); cue(K("refuse") + 0.4, "swell_1", -22)

# 2  "The market will tempt you in three ways. Here's how to say no to each one."
s = S(K("tempt") - 0.1, K("one") - 0.1)
toplab(s, X("tm_s"), X("tm_b"), K("tempt"), K("howto") - 0.1, RED, LBL, 66)
toplab(s, X("hw_s"), X("hw_b"), K("howto"), K("one") - 0.1, GOLD, LBL, 54)
s.spot(540, 1, "232,194,106", 30, 150)
s.fig(540, 1.0, GOLD, 1)
for k, (cx, cy) in enumerate(((240, 830), (840, 760), (830, 1030))):
    c = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 16px rgba(255,77,94,0.8))"><path d="{rrect(cx - 80, cy - 55, 160, 110, 20)}" '
              f'fill="#1a0f12" stroke="{RED}" stroke-width="3"/><text x="{cx}" y="{cy + 22}" text-anchor="middle" font-family="Montserrat" '
              f'font-weight="800" font-size="60" fill="{RED}">{k + 1}</text></g>', "tc")
    t = K("tempt") + 0.5 + k * 0.3
    s.pop(c, t, 0.4, 0.5, "50% 50%"); cue(t, "pop_" + str(k + 1), -20)
    tl(f'tl.to("#{c}", {{y: -12, duration: 0.9, yoyo: true, repeat: 3, ease: "sine.inOut"}}, {t + 0.4:.3f});')

# 3  chapter 1: "One. Risk more, win it back faster. Say no."
temptation(1, "one", "imagine", dict())

# 4  "Imagine you're down to your last thousand dollars. The urge is to double it. But the first job of a small account... is to survive."
s = S(K("imagine") - 0.1, K("risk1") - 0.1)
toplab(s, X("im_s"), X("im_b"), K("imagine"), K("urge") - 0.1, GOLD, LBL, 60)
toplab(s, X("ur_s"), X("ur_b"), K("urge"), K("job") - 0.1, RED, LBL, 64)
toplab(s, X("j_s"), X("j_b"), K("job"), K("risk1") - 0.1, GOLD, LBL, 64, tb=K("survive"))
s.fig(330, 1.0, WHITE, 1)
sp4 = s.spot(700, 0, "232,194,106", 30, 150); s.fade(sp4, K("last") - 0.1, 0.5)
c4 = card(s, 700, 0); s.pop(c4, K("last"), 0.45, 0.5); cue(K("last"), "pop_1", -18)
ar = s.path("M 790 1080 Q 840 960 880 830 M 852 858 L 880 830 L 896 866", GOLD, 6); s.draw(ar, K("urge") + 0.15, 0.5)
x2 = num(s, 880, 800, "×2", 64, GOLD); s.pop(x2, K("urge") + 0.5, 0.4, 0.4, "50% 50%")
cue(K("urge") + 0.15, "whoosh-short_2", -22)
st = s.path("M 826 792 L 936 744", RED, 8); s.draw(st, K("job") - 0.5, 0.25); cue(K("job") - 0.5, "tock_1", -18)
hide(ar, K("job") - 0.2, 0.3, 0.25); hide(x2, K("job") - 0.2, 0.3, 0.25); hide(st, K("job") - 0.2, 0.3, 0.4)
sh = s.path("M 700 1000 L 852 1042 V 1146 Q 852 1226 700 1262 Q 548 1226 548 1146 V 1042 Z", GOLD, 6,
            style="filter:drop-shadow(0 0 14px rgba(232,194,106,0.8))")
s.draw(sh, K("job") + 0.1, 0.8); cue(K("job") + 0.1, "swell_1", -22); cue(K("survive"), "bell_C5", -18)

# 5  "So risk one percent a trade, or less. Five losses in a row cost you fifty dollars. You're still standing."
s = S(K("risk1") - 0.1, K("slow") - 0.1, ground=False)
toplab(s, X("p_s"), X("p_b"), K("risk1"), K("five") - 0.1, GOLD, LBL, 64)
toplab(s, X("f_s"), X("f_b"), K("five"), K("slow") - 0.1, GOLD, LBL, 60, tb=K("standing"))
dots = "".join(f'<circle cx="{414 + (k % 10) * 28}" cy="{680 + (k // 10) * 28}" r="10" fill="{GOLD}" fill-opacity="0.32"/>' for k in range(1, 100))
dg = s.raw(f'<g id="@ID@" style="opacity:0">{dots}</g>', "dg"); s.fade(dg, K("risk1") + 0.1, 0.4)
rd = s.raw(f'<circle id="@ID@" cx="414" cy="680" r="14" fill="{RED}" style="opacity:0;filter:drop-shadow(0 0 8px rgba(255,77,94,0.9))"/>', "rd")
s.pop(rd, K("risk1") + 0.45, 0.35, 0.2, "50% 50%"); cue(K("risk1") + 0.45, "pop_2", -18)
tl(f'tl.to("#{rd}", {{scale: 0.6, transformOrigin: "50% 50%", duration: 0.35, ease: "power2.inOut"}}, {K("less"):.3f});')
r10 = tx(s, 540, 1000, X("risk10"), 34, RED, 0, 800, sp=0.08); s.fade(r10, K("risk1") + 0.6, 0.3)
t_x0, t_x1 = K("five") + 0.3, K("standing") - 0.2
for k in range(5):
    x = 180 + k * 150
    bx = s.raw(f'<path id="@ID@" d="{rrect(x, 1060, 120, 100, 16)}" fill="#0f1319" stroke="#ffffff55" stroke-width="2" style="opacity:0"/>', "bx")
    s.fade(bx, K("risk1") + 0.8 + k * 0.06, 0.3)
    t = t_x0 + k * (t_x1 - t_x0) / 4
    xx = s.path(f"M {x + 38} 1088 L {x + 82} 1132 M {x + 82} 1088 L {x + 38} 1132", RED, 7); s.draw(xx, t, 0.18)
    cue(t, "tick_" + str(k % 3 + 1), -22)
tr = s.raw(f'<rect id="@ID@" x="180" y="1200" width="720" height="44" rx="22" fill="#1d2229" style="opacity:0"/>', "tr")
bar = s.raw(f'<rect id="@ID@" x="180" y="1200" width="720" height="44" rx="22" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 10px rgba(232,194,106,0.6))"/>', "br")
s.fade(tr, K("risk1") + 0.8, 0.3); s.fade(bar, K("risk1") + 0.8, 0.3)
bl = tx(s, 180, 1310, X("bal"), 30, LBL, 0, 700, "start", sp=0.1); s.fade(bl, K("risk1") + 0.8, 0.3)
vals = [num(s, 900, 1314, f"${1000 - 10 * k:,}", 48, GOLD, 0, "end") for k in range(6)]
s.fade(vals[0], K("risk1") + 0.8, 0.3)
for k in range(1, 6):
    t = t_x0 + (k - 1) * (t_x1 - t_x0) / 4 + 0.1
    tl(f'tl.set("#{vals[k - 1]}", {{opacity: 0}}, {t:.3f}); tl.set("#{vals[k]}", {{opacity: 1}}, {t:.3f});')
    tl(f'tl.to("#{bar}", {{attr: {{width: {720 - 7.2 * k:.1f}}}, duration: 0.2, ease: "power2.out"}}, {t:.3f});')
m50 = num(s, 180, 1390, "−$50", 44, RED, 0, "start"); s.fade(m50, K("cost") + 0.3, 0.3)
cue(K("standing"), "bell_E5", -20)

# 6  "Slow growth never killed a small account. Big ambition does."
s = S(K("slow") - 0.1, K("two") - 0.1)
toplab(s, X("s_s"), X("s_b"), K("slow"), K("ambition") - 0.1, GOLD, LBL, 60)
toplab(s, "", X("a_b"), K("ambition"), K("two") - 0.1, RED, LBL, 54)
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

# 7  chapter 2: "Two. Three losses in a row, try a new strategy. Say no."
temptation(2, "two", "loss1", dict(restore=False))

# 8  "One loss, new strategy. Two losses, new indicator. Three losses, new mentor."
s = S(K("loss1") - 0.1, K("nothing") - 0.1, ground=False, hide=False, restore=False)
for j, (lk, nk, lab, newl) in enumerate((("loss1", "new1", "l1", "n1"), ("loss2", "new2", "l2", "n2"), ("loss3", "new3", "l3", "n3"))):
    y = 690 + j * 180
    lb = s.raw(f'<path id="@ID@" d="{rrect(130, y - 62, 330, 124, 22)}" fill="#1a0f12" stroke="{RED}" stroke-width="3" style="opacity:0"/>', "lb")
    lt = tx(s, 295, y + 14, X(lab), 38, RED, 0, 800, sp=0.04)
    s.pop(lb, K(lk), 0.35, 0.6, "50% 50%"); s.fade(lt, K(lk) + 0.05, 0.3); cue(K(lk), "tock_1", -20)
    a8 = s.path(f"M 478 {y} H 588 M 566 {y - 18} L 590 {y} L 566 {y + 18}", LBL, 5); s.draw(a8, K(nk) - 0.25, 0.3)
    nb = s.raw(f'<path id="@ID@" d="{rrect(610, y - 62, 340, 124, 22)}" fill="#0f1319" stroke="#ffffffa0" stroke-width="3" style="opacity:0"/>', "nb")
    ntx = tx(s, 780, y + 12, X(newl), 31, WHITE, 0, 800, sp=0.03)
    s.pop(nb, K(nk), 0.35, 0.6, "50% 50%"); s.fade(ntx, K(nk) + 0.05, 0.3); cue(K(nk), "pop_" + str(j + 1), -20)
loop = s.path("M 120 1050 C 40 990 40 750 112 694 M 92 720 L 114 692 L 128 726", RED, 5, style="opacity:0.85")
s.draw(loop, K("new3") + 0.6, 0.5); cue(K("new3") + 0.6, "whoosh-short_3", -24)

# 9  "Nothing ever gets enough trades to show what it can do."
s = S(K("nothing") - 0.1, K("streak") - 0.1, ground=False, hide=False, restore=False)
toplab(s, X("ng_s"), X("ng_b"), K("nothing"), K("streak") - 0.1, RED, LBL, 60)
tg = s.raw(f'<line id="@ID@" x1="880" y1="670" x2="880" y2="1000" stroke="{GOLD}" stroke-width="4" stroke-dasharray="12 10" '
           f'style="opacity:0;filter:drop-shadow(0 0 8px rgba(232,194,106,0.8))"/>', "tg")
s.fade(tg, K("nothing") + 0.1, 0.4)
tn = num(s, 880, 1060, "100", 44, GOLD); s.fade(tn, K("nothing") + 0.1, 0.4)
tt = tx(s, 880, 1104, X("trades"), 28, GOLD, 0, 700, sp=0.1); s.fade(tt, K("nothing") + 0.1, 0.4)
LENS = [90, 150, 60, 120, 80]
t_r0, t_r1 = K("nothing") + 0.2, K("show") - 0.1
for k, ln in enumerate(LENS):
    y = 700 + k * 66
    t = t_r0 + k * (t_r1 - t_r0) / 5
    rl = num(s, 150, y + 12, "ABCDE"[k], 34, LBL); s.fade(rl, t, 0.25)
    s.raw(f'<line x1="200" y1="{y}" x2="860" y2="{y}" stroke="#ffffff20" stroke-width="2" stroke-dasharray="4 10"/>', "gl")
    br = s.raw(f'<rect id="@ID@" x="200" y="{y - 12}" width="0" height="24" rx="12" fill="{GOLD}" fill-opacity="0.85"/>', "rb")
    tl(f'tl.fromTo("#{br}", {{attr: {{width: 0}}}}, {{attr: {{width: {ln}}}, duration: 0.3, ease: "power2.out", immediateRender: false}}, {t:.3f});')
    cx = 200 + ln + 22
    xx = s.path(f"M {cx - 13} {y - 13} L {cx + 13} {y + 13} M {cx + 13} {y - 13} L {cx - 13} {y + 13}", RED, 6); s.draw(xx, t + 0.3, 0.15)
    cue(t + 0.3, "tick_" + str(k % 3 + 1), -22)
gap = s.raw(f'<rect id="@ID@" x="380" y="680" width="480" height="300" rx="16" fill="{RED}" fill-opacity="0.07" stroke="{RED}" '
            f'stroke-opacity="0.5" stroke-width="2" stroke-dasharray="10 8" style="opacity:0"/>', "gp")
s.fade(gap, K("show"), 0.4)
sw = tx(s, 540, 1200, X("sh_b"), 40, WHITE, 0, 800, sp=0.04); s.fade(sw, K("show") - 0.5, 0.3)
cue(K("show"), "swell_2", -24)

# 10  "Every strategy has losing streaks. Even a good one."
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
zones, k = [], 0
while k < len(STEPS):
    if STEPS[k] < 0:
        j = k
        while j < len(STEPS) and STEPS[j] < 0: j += 1
        if j - k >= 3: zones.append((k, j))
        k = j
    else:
        k += 1
for a_, b_ in zones:
    x0, x1 = pts[a_][0], pts[b_][0]
    ys = [p[1] for p in pts[a_:b_ + 1]]
    z = s.raw(f'<rect id="@ID@" x="{x0}" y="{min(ys) - 20:.0f}" width="{x1 - x0}" height="{max(ys) - min(ys) + 40:.0f}" rx="8" fill="{RED}" '
              f'fill-opacity="0.16" stroke="{RED}" stroke-opacity="0.7" stroke-width="2" style="opacity:0"/>', "zn")
    tz = t_c0 + (x1 - 150) / (pts[-1][0] - 150) * (t_c1 - t_c0)
    s.fade(z, tz, 0.3); cue(tz, "tock_1", -24)
trd = s.path(f"M {pts[0][0]} {pts[0][1]} L {pts[-1][0]} {pts[-1][1]}", "#ffffff70", 3, drawn=True, style="stroke-dasharray:10 10;opacity:0")
s.fade(trd, K("evengood") + 0.3, 0.4); cue(K("evengood"), "bell_E5", -20)

# 11  "So keep it boring. Same setup. Same risk. Same rules. Long enough to let it work."
s = S(K("boring") - 0.1, K("three") - 0.1, ground=False, hide=False, restore=False)
toplab(s, X("kb_s"), X("kb_b"), K("boring"), K("long") - 0.1, WHITE, LBL, 66)
toplab(s, "", X("lg_b"), K("long"), K("three") - 0.1, GOLD, LBL, 46)
for j, (key, k_) in enumerate((("sm1", "same1"), ("sm2", "same2"), ("sm3", "same3"))):
    p = tpill(s, 540, 700 + j * 120, X(key), GOLD, "#111", 42)
    s.pop(p, K(k_), 0.35, 0.6, "50% 50%"); cue(K(k_), "pop_" + str(j + 1), -18)
    hide(p, K("three") - 0.5, 0.2)
t_a, t_b = K("same1") + 0.3, K("three") - 0.9
for k in range(12):
    x = 156 + k * 64
    tb_ = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(x, 1080, 52, 52, 10)}" fill="#14110a" stroke="{GOLD}" stroke-width="2"/>'
                f'<path d="M {x + 14} 1107 L {x + 23} 1117 L {x + 39} 1095" fill="none" stroke="{GOLD}" stroke-width="4" '
                f'stroke-linecap="round" stroke-linejoin="round"/></g>', "tb")
    t = t_a + k * (t_b - t_a) / 11
    s.pop(tb_, t, 0.25, 0.6, "50% 50%"); hide(tb_, K("three") - 0.5, 0.2)
    if k % 3 == 0: cue(t, "tick-crisp_" + str(k // 3 % 3 + 1), -24)

# 12  chapter 3: "Three. You're bored, just take something. Say no."
temptation(3, "three", "watch", dict(hide=False))

# 13  "A good trader can watch the chart for two hours... see nothing worth taking... and close the screen."
s = S(K("watch") - 0.1, K("forced") - 0.1)
toplab(s, X("w_s"), X("w_b"), K("watch"), K("seenothing") - 0.1, WHITE, LBL, 62)
toplab(s, X("s2_s"), X("s2_b"), K("seenothing"), K("forced") - 0.1, GOLD, LBL, 52)
monitor(s)
ch = s.path(CHOP_D, "#c9ced6", 4); s.draw(ch, K("watch") + 0.1, max(1.0, K("seenothing") + 0.4 - K("watch")), "none")
s.raw(f'<g id="@ID@"><circle cx="250" cy="830" r="62" fill="#0f1319" stroke="#c9ced6" stroke-width="4"/><circle cx="250" cy="830" r="5" fill="#c9ced6"/></g>', "ck")
hh = s.raw(f'<line id="@ID@" x1="250" y1="830" x2="250" y2="796" stroke="{GOLD}" stroke-width="6" stroke-linecap="round"/>', "hh")
mh = s.raw(f'<line id="@ID@" x1="250" y1="830" x2="250" y2="782" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>', "mh")
t_c0, t_c1 = K("watch") + 0.1, K("seenothing") + 0.2
tl(f'tl.fromTo("#{hh}", {{rotation: 0}}, {{rotation: 60, svgOrigin: "250 830", duration: {t_c1 - t_c0:.3f}, ease: "power1.inOut", immediateRender: false}}, {t_c0:.3f});')
tl(f'tl.fromTo("#{mh}", {{rotation: 0}}, {{rotation: 720, svgOrigin: "250 830", duration: {t_c1 - t_c0:.3f}, ease: "power1.inOut", immediateRender: false}}, {t_c0:.3f});')
cue(t_c0, "tick_1", -24)
f13 = s.fig(250, 1.0, GOLD, 1)
for k, x in enumerate((620, 740, 860)):
    m = s.path(f"M {x - 14} 830 L {x + 14} 858 M {x + 14} 830 L {x - 14} 858", "#7d838c", 5)
    s.draw(m, K("seenothing") + 0.25 + k * 0.3, 0.15); cue(K("seenothing") + 0.25 + k * 0.3, "tick_" + str(k + 1), -24)
off = s.raw(f'<path id="@ID@" d="{rrect(523, 763, 434, 294, 16)}" fill="#000000" style="opacity:0"/>', "of")
s.fade(off, K("close") + 0.1, 0.35, 0.92); cue(K("close") + 0.1, "click_2", -18)
s.walk(f13, K("close") + 0.5, -150, 1.1)

# 14  "Forced entries and B-grade setups feel like progress. They're just activity."
s = S(K("forced") - 0.1, K("market") - 0.1, ground=False, restore=False)
toplab(s, X("fs"), X("fp_b"), K("forced"), K("activity") - 0.1, WHITE, LBL, 52, tb=K("feel"))
toplab(s, "", X("ja_b"), K("activity"), K("market") - 0.1, RED, LBL, 58)
for k, (key, k_) in enumerate((("f1", "forced"), ("f2", "bgrade"))):
    y = 700 + k * 150
    cd = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(150, y - 58, 780, 116, 22)}" fill="#1a0f12" stroke="{RED}" stroke-width="3"/>'
               f'<path d="M 790 {y - 28} L 820 {y - 8} L 845 {y - 18} L 880 {y + 26}" fill="none" stroke="{RED}" stroke-width="5" '
               f'stroke-linecap="round" stroke-linejoin="round"/></g>', "fc")
    ft = tx(s, 195, y + 13, X(key), 38, WHITE, 0, 800, "start", sp=0.04)
    s.pop(cd, K(k_), 0.35, 0.7, "50% 50%"); s.fade(ft, K(k_) + 0.05, 0.3); cue(K(k_), "tock_1", -18)
for j, (lab, col, t, full, pct) in enumerate((("act", RED, K("feel") + 0.2, 780, "100%"), ("prog", GOLD, K("activity") + 0.2, 26, "0%"))):
    y = 1000 + j * 170
    l = tx(s, 150, y, X(lab), 34, LBL, 0, 800, "start", sp=0.1); s.fade(l, t - 0.2, 0.3)
    s.raw(f'<rect x="150" y="{y + 26}" width="780" height="50" rx="25" fill="#1d2229"/>', "bt")
    fb = s.raw(f'<rect id="@ID@" x="150" y="{y + 26}" width="0" height="50" rx="25" fill="{col}" style="filter:drop-shadow(0 0 10px {col})"/>', "fb")
    tl(f'tl.fromTo("#{fb}", {{attr: {{width: 0}}}}, {{attr: {{width: {full}}}, duration: {0.9 if j == 0 else 0.5}, ease: "power2.out", immediateRender: false}}, {t:.3f});')
    pv = num(s, 930, y, pct, 36, col if j == 0 else GREY, 0, "end"); s.fade(pv, t + 0.5, 0.3)
    cue(t, "swell_1" if j == 0 else "tock_1", -22 if j == 0 else -18)

# 15  "The market doesn't pay you for being busy. It pays you for being picky."
s = S(K("market") - 0.1, K("noa") - 0.1, ground=False, hide=False)
toplab(s, X("mk_s"), X("mk_b"), K("market"), K("picky") - 0.1, RED, LBL, 62)
toplab(s, X("pk_s"), X("pk_b"), K("picky"), K("noa") - 0.1, GOLD, LBL, 62)
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

# 16  "No. No. And no. That's the job."
s = S(K("noa") - 0.1, K("order") + 0.35)
toplab(s, "", X("job"), K("thejob"), K("order") + 0.35, GOLD, LBL, 66)
sp16 = s.spot(540, 0, "232,194,106", 30, 150); s.fade(sp16, K("thejob"), 0.5)
f16 = s.fig(540, 1.0, GOLD); s.pop(f16, K("noa"), 0.4)
for k, (key, cx, rot) in enumerate((("noa", 250, -8), ("nob", 540, 4), ("noc", 830, -5))):
    b = stamp(s, cx, 780, 230, 120, 86 if not TH_ else 80, rot)
    tl(f'tl.fromTo("#{b}", {{opacity: 0, scale: 2.0, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.2, ease: "power4.in", immediateRender: false}}, {K(key) - 0.2:.3f});')
    cue(K(key), "tock_1", -16)
cue(K("thejob"), "bell_A4", -18)

# 17  outro (handles, no end card; brand lines stay in English)
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
    <div id="root" data-composition-id="otm-saynofull" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12"/>
{scenes_svg}
{TIMELINE}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-saynofull-audio" class="clip" src="assets/audio/mix_saynofull.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-saynofull"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
