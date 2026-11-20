"""OTM "Fed Minutes: gold below 3,800" (Thai news reel, Instagram Reels only). Thai narration (Higgsfield text2speech_v2,
ElevenLabs engine, preset voice "John", sped up 1.1x), Thai on-screen text in Kanit (OFL, assets/fonts); numbers in
Montserrat. News photos from Wikimedia Commons (public domain / CC0, see CREDITS.md) in rounded frames with a slow push-in;
the rest is drawn (rate steps, indicator tiles, an illustrative candle chart, two scenarios). Scenes key off token indices
of work/words.json (the script's tokens aligned to the voice by work/align.py). Writes ../index.html, work/cues.json and
work/timing.json. No end card: the outro holds, then fades out."""
import json, os, random, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAD = 0.3
GOLD, RED, GREEN, WHITE, GREY, LBL = "#e8c26a", "#ff4d5e", "#3ddc97", "#ffffff", "#7d838c", "#c9ced6"
words = json.load(open(f"{ROOT}/work/words.json"))
def K(i, d=0.0): return round(words[i]["start"] + LEAD + d, 3)
END_T = round(words[-1]["end"] + LEAD + 0.6, 2)
TOTAL = round(END_T + 1.0, 2)
rnd = random.Random(11)
T, CUES = [], []
def tl(s): T.append(s)
def cue(t, snd, gain): CUES.append(dict(t=round(t, 3), snd=snd, gain=gain))


def rrect(x, y, w, h, r):
    return (f"M {x + r} {y} H {x + w - r} Q {x + w} {y} {x + w} {y + r} V {y + h - r} Q {x + w} {y + h} {x + w - r} {y + h} "
            f"H {x + r} Q {x} {y + h} {x} {y + h - r} V {y + r} Q {x} {y} {x + r} {y} Z")


class S:
    """One scene: an SVG group plus its tweens."""
    n = 0
    scenes = []

    def __init__(self, o, c, first=False):
        S.n += 1
        self.id, self.o, self.c, self.items = f"sc{S.n}", o, c, []
        S.scenes.append(self)
        if first:
            tl(f'tl.set("#{self.id}", {{opacity: 1, visibility: "visible"}}, 0);')
        else:
            tl(f'tl.set("#{self.id}", {{visibility: "visible"}}, {o:.3f});')
            tl(f'tl.fromTo("#{self.id}", {{opacity: 0}}, {{opacity: 1, duration: 0.3, ease: "power2.out", immediateRender: false}}, {o:.3f});')
        if c < TOTAL:
            tl(f'tl.to("#{self.id}", {{opacity: 0, duration: 0.25, ease: "power2.in"}}, {c - 0.25:.3f});')
            tl(f'tl.set("#{self.id}", {{opacity: 0, visibility: "hidden"}}, {c:.3f});')

    def uid(self, p):
        S.n += 1
        return f"{p}{S.n}"

    def add(self, s, p="e"):
        i = self.uid(p)
        self.items.append(s.replace("@ID@", i))
        return i

    def label(self, x, y, text, size, col, op, weight, sp, anchor, fam="Montserrat"):
        return self.add(f'<text id="@ID@" x="{x}" y="{y}" text-anchor="{anchor}" font-family="{fam}" font-weight="{weight}" font-size="{size}" '
                        f'letter-spacing="{sp}em" fill="{col}" style="opacity:{op}">{text}</text>', "t")

    def path(self, d, col=WHITE, w=4, fill="none", drawn=False, style=""):
        st = ("" if drawn else "stroke-dasharray:1 1.2;stroke-dashoffset:1.1;") + style
        dash = ('' if drawn else 'pathLength="1" ') + (f'style="{st}"' if st else "")
        return self.add(f'<path id="@ID@" d="{d}" fill="{fill}" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {dash}/>', "p")

    def raw(self, s, p="r"):
        return self.add(s, p)

    def draw(self, i, t, d=0.6, ease="power2.inOut"):
        tl(f'tl.fromTo("#{i}", {{strokeDashoffset: 1.1}}, {{strokeDashoffset: 0, duration: {d:.3f}, ease: "{ease}", immediateRender: false}}, {t:.3f});')

    def fade(self, i, t, d=0.35, y=0):
        a = f", y: {y}" if y else ""; b = ", y: 0" if y else ""
        tl(f'tl.fromTo("#{i}", {{opacity: 0{a}}}, {{opacity: 1{b}, duration: {d:.3f}, ease: "power2.out", immediateRender: false}}, {t:.3f});')

    def pop(self, i, t, d=0.4, frm=0.5, origin="50% 50%"):
        tl(f'tl.set("#{i}", {{opacity: 0}}, {self.o:.3f});')
        tl(f'tl.fromTo("#{i}", {{opacity: 0, scale: {frm}, transformOrigin: "{origin}"}}, {{opacity: 1, scale: 1, duration: {d:.3f}, ease: "back.out(1.8)", immediateRender: false}}, {t:.3f});')

    # ---- text ----
    def tx(self, x, y, text, size=40, col=WHITE, op=0, weight=700, anchor="middle"):
        """Thai (and mixed) text in Kanit."""
        return self.label(x, y, text, size, col, op, 700 if weight >= 700 else 600, 0, anchor, "Kanit")

    def num(self, x, y, text, size, col, op=0, anchor="middle"):
        return self.label(x, y, text, size, col, op, 800, 0.02, anchor)

    # ---- a news photo in a rounded frame, slow push-in, credit line ----
    def photo(self, href, x, y, w, h, credit, t0, t1, tag=None, focus="50% 50%"):
        cid = self.uid("cp"); gid = self.uid("pg")
        img = self.uid("im")
        self.items.append(
            f'<defs><clipPath id="{cid}"><path d="{rrect(x, y, w, h, 28)}"/></clipPath>'
            f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0.55" stop-color="#000" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="#000" stop-opacity="0.75"/></linearGradient></defs>'
            f'<g clip-path="url(#{cid})"><image id="{img}" href="{href}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{gid})"/></g>'
            f'<path d="{rrect(x, y, w, h, 28)}" fill="none" stroke="#ffffff30" stroke-width="2"/>'
            f'<text x="{x + 24}" y="{y + h - 22}" font-family="Kanit" font-weight="600" font-size="22" fill="#ffffffb0">{credit}</text>')
        tl(f'tl.fromTo("#{img}", {{scale: 1.0}}, {{scale: 1.12, transformOrigin: "{focus}", duration: {t1 - t0:.3f}, ease: "none", immediateRender: false}}, {t0:.3f});')
        if tag:
            w2 = 40 + len(tag) * 22
            tg = self.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(x + 24, y + 24, w2, 58, 12)}" fill="{RED}"/>'
                          f'<circle cx="{x + 50}" cy="{y + 53}" r="8" fill="#fff"/>'
                          f'<text x="{x + 68}" y="{y + 66}" font-family="Kanit" font-weight="700" font-size="34" fill="#fff">{tag}</text></g>', "tg")
            self.pop(tg, t0 + 0.15, 0.35, 0.6, "0% 0%"); cue(t0 + 0.15, "pop_1", -18)
            tl(f'tl.to("#{tg} circle", {{opacity: 0.2, duration: 0.45, yoyo: true, repeat: {int((t1 - t0) / 0.9)}, ease: "sine.inOut"}}, {t0 + 0.5:.3f});')
        return img

    def card(self, x, y, w, h, col, fill="#10151c", glow=False):
        g = f";filter:drop-shadow(0 0 16px {col}66)" if glow else ""
        return self.raw(f'<g id="@ID@" style="opacity:0{g}"><path d="{rrect(x, y, w, h, 18)}" fill="{fill}"/>'
                        f'<rect x="{x}" y="{y + 10}" width="7" height="{h - 20}" rx="3" fill="{col}"/></g>', "cd")


def hide(i, t, d=0.25):
    tl(f'tl.to("#{i}", {{opacity: 0, duration: {d}}}, {t:.3f});')

def arrow(x, y, up, col, s=1.0):
    """Filled arrow centred at x,y."""
    d = (f"M {x} {y - 26 * s} L {x + 22 * s} {y} L {x + 9 * s} {y} L {x + 9 * s} {y + 24 * s} L {x - 9 * s} {y + 24 * s} L {x - 9 * s} {y} L {x - 22 * s} {y} Z" if up else
         f"M {x} {y + 26 * s} L {x + 22 * s} {y} L {x + 9 * s} {y} L {x + 9 * s} {y - 24 * s} L {x - 9 * s} {y - 24 * s} L {x - 9 * s} {y} L {x - 22 * s} {y} Z")
    return f'<path d="{d}" fill="{col}"/>'


# ================================================================================================= scenes
PX, PW = 60, 960

# 1  "เฟดส่งสัญญาณแรง ทองคำหลุด 3,800 ดอลลาร์ ครั้งแรกในรอบ 14 เดือน"
c1 = K(3, -0.1)
s = S(0, c1, first=True)
s.photo("assets/photos/eccles.jpg", PX, 290, PW, 640, "ภาพ: Federal Reserve · สาธารณสมบัติ", 0, c1, tag="ข่าวด่วน", focus="50% 40%")
t0 = s.tx(540, 1060, "เฟดส่งสัญญาณแรง", 70, WHITE); s.fade(t0, 0.1, 0.4, y=12)
t1 = s.tx(520, 1200, "ทองคำหลุด", 58, LBL, anchor="end"); s.fade(t1, K(1), 0.3, y=10)
pr = s.num(545, 1210, "$3,800", 92, RED, anchor="start")
s.pop(pr, K(1, 0.35), 0.45, 0.6, "0% 50%"); cue(K(1, 0.35), "land_1", -14)
ar = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 12px rgba(255,77,94,0.8))">{arrow(950, 1180, False, RED, 1.3)}</g>', "ar")
s.pop(ar, K(1, 0.5), 0.35, 0.4)
tl(f'tl.to("#{ar}", {{y: 14, duration: 0.5, yoyo: true, repeat: 5, ease: "sine.inOut"}}, {K(1, 0.9):.3f});')
pl = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(260, 1270, 560, 76, 38)}" fill="#14110a" stroke="{GOLD}" stroke-width="3"/></g>', "pl")
s.pop(pl, K(2), 0.4, 0.6); cue(K(2), "bell_E5", -20)
plt = s.tx(540, 1322, "ครั้งแรกในรอบ 14 เดือน", 40, GOLD); s.fade(plt, K(2, 0.05), 0.3)

# 2  "เมื่อคืนเฟดเปิดบันทึกการประชุม FOMC รอบเดือนตุลาคม / คงดอกเบี้ยไว้ แต่เกือบทุกคน... มองว่าน่าจะต้องขึ้นดอกเบี้ยต่อ"
o2, c2 = c1, K(9, -0.1)
s = S(o2, c2)
s.photo("assets/photos/fomc2016.jpg", PX, 290, PW, 560, "ภาพ: ห้องประชุม FOMC · Federal Reserve · สาธารณสมบัติ", o2, c2, focus="45% 55%")
k1 = s.label(540, 935, "FOMC MINUTES", 30, GOLD, 0, 800, 0.24, "middle"); s.fade(k1, K(3), 0.3)
k2 = s.tx(540, 1010, "บันทึกการประชุม รอบ ต.ค.", 56, WHITE); s.fade(k2, K(4), 0.35, y=10); cue(K(4), "click_1", -20)
cd = s.card(140, 1060, 800, 96, GOLD)
s.pop(cd, K(6), 0.35, 0.8, "0% 50%")
r1 = s.tx(180, 1124, "คงดอกเบี้ยไว้ที่", 38, LBL, anchor="start"); s.fade(r1, K(6, 0.05), 0.3)
r2 = s.num(900, 1126, "3.75–4.00%", 44, GOLD, anchor="end"); s.fade(r2, K(6, 0.2), 0.3); cue(K(6, 0.2), "tick-crisp_1", -22)
# 19 FOMC participants; "almost all" light up gold
dots = []
for j in range(19):
    row, col = divmod(j, 10)
    x = 192 + col * 77 + (38 if row else 0); y = 1235 + row * 82
    d = s.raw(f'<g id="@ID@" style="opacity:0"><circle cx="{x}" cy="{y - 14}" r="13" fill="#3a3f47"/>'
              f'<path d="M {x - 22} {y + 26} Q {x - 22} {y + 2} {x} {y + 2} Q {x + 22} {y + 2} {x + 22} {y + 26} Z" fill="#3a3f47"/></g>', "dt")
    s.fade(d, K(7, j * 0.03), 0.2); dots.append((d, x, y))
for j, (d, x, y) in enumerate(dots):
    if j in (6, 15):
        continue
    t = K(7, 0.6 + j * 0.06)
    tl(f'tl.to("#{d} circle, #{d} path", {{fill: "{GOLD}", duration: 0.2}}, {t:.3f});')
cue(K(7, 0.6), "swell_1", -24)
up = s.raw(f'<g id="@ID@" style="opacity:0">{arrow(250, 1418, True, GOLD, 0.9)}</g>', "up")
lab = s.tx(290, 1432, "เกือบทุกคน: น่าจะต้องขึ้นดอกเบี้ยต่อ", 40, GOLD, anchor="start")
s.pop(up, K(8), 0.35, 0.4); s.fade(lab, K(8, 0.05), 0.3); cue(K(8), "bell_G5", -20)

# 3  "และมีบางคนถึงขั้นบอกว่า ถ้าเงินเฟ้อยังไม่ยอมลง อาจต้องขึ้นแรงกว่าปกติ"
o3, c3 = c2, K(12, -0.1)
s = S(o3, c3)
h3 = s.tx(540, 420, "บางคนถึงขั้นบอกว่า...", 62, WHITE); s.fade(h3, K(9), 0.35, y=10)
ca = s.card(120, 500, 840, 100, LBL); s.pop(ca, K(10), 0.35, 0.8, "0% 50%")
cat = s.tx(160, 566, "ถ้าเงินเฟ้อยังไม่ยอมลง...", 42, WHITE, anchor="start"); s.fade(cat, K(10, 0.05), 0.3)
cb = s.card(120, 620, 840, 100, RED, glow=True); s.pop(cb, K(11), 0.35, 0.8, "0% 50%"); cue(K(11), "land_1", -16)
cbt = s.tx(160, 686, "อาจต้องขึ้นแรงกว่า 0.25%", 46, RED, anchor="start"); s.fade(cbt, K(11, 0.05), 0.3)
# rate steps: now -> +0.25 -> bigger step
base = 1360
s.raw(f'<line x1="140" y1="{base}" x2="940" y2="{base}" stroke="#ffffff30" stroke-width="2" stroke-dasharray="6 10"/>')
st0 = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="160" y="{base - 200}" width="220" height="200" rx="10" fill="#2a2f37"/></g>', "s0")
st0t = s.num(270, base - 220, "3.75–4.00%", 30, LBL); st0l = s.tx(270, base + 50, "ตอนนี้", 32, LBL)
for i in (st0, st0t, st0l): s.fade(i, K(9, 0.3), 0.3)
st1 = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="420" y="{base - 270}" width="220" height="270" rx="10" fill="#4a4230"/></g>', "s1")
st1t = s.num(530, base - 290, "+0.25%", 32, GOLD); st1l = s.tx(530, base + 50, "ขึ้นปกติ", 32, LBL)
s.pop(st1, K(10, 0.3), 0.4, 0.5, "50% 100%"); s.fade(st1t, K(10, 0.5), 0.3); s.fade(st1l, K(10, 0.5), 0.3); cue(K(10, 0.3), "pop_2", -20)
st2 = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 18px rgba(255,77,94,0.6))"><rect x="680" y="{base - 420}" width="220" height="420" rx="10" fill="#3a1218" stroke="{RED}" stroke-width="3"/></g>', "s2")
st2t = s.num(790, base - 440, "> 0.25%", 34, RED); st2l = s.tx(790, base + 50, "ขึ้นแรง", 32, RED)
s.pop(st2, K(11, 0.4), 0.45, 0.4, "50% 100%"); s.fade(st2t, K(11, 0.6), 0.3); s.fade(st2l, K(11, 0.6), 0.3)
cue(K(11, 0.4), "whoosh-short_1", -20)

# 4  "ผลคือ ดอลลาร์แข็งค่า บอนด์ยีลด์ยังสูง และทองโดนกดลงไปแถว 3,700"
o4, c4 = c3, K(16, -0.1)
s = S(o4, c4)
h4 = s.tx(540, 400, "ผลคือ...", 62, WHITE); s.fade(h4, K(12), 0.3, y=10)
tiles = [("$", "ดอลลาร์", True, GOLD, 13), ("%", "บอนด์ยีลด์", True, GOLD, 14), ("Au", "ทองคำ", False, RED, 15)]
for j, (sym, name, upd, col, k) in enumerate(tiles):
    x = 100 + j * 300
    tb = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(x, 460, 280, 200, 20)}" fill="#10151c" stroke="{col}" stroke-width="3"/>'
               f'<circle cx="{x + 105}" cy="540" r="44" fill="none" stroke="{col}" stroke-width="4"/>'
               f'<text x="{x + 105}" y="556" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="{42 if len(sym) == 1 else 34}" fill="{col}">{sym}</text>'
               f'{arrow(x + 195, 540, upd, GREEN if upd else RED, 1.1)}'
               f'<text x="{x + 140}" y="632" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="34" fill="{WHITE}">{name}</text></g>', "tb")
    s.pop(tb, K(k), 0.4, 0.6); cue(K(k), "pop_" + str(j + 1), -18)
# illustrative candle chart breaking 3,800
CY0, CY1, PHI, PLO = 760, 1290, 3960, 3660
def py(p): return CY0 + (PHI - p) / (PHI - PLO) * (CY1 - CY0)
s.raw(f'<path d="{rrect(80, 720, 920, 620, 20)}" fill="#0c1016" stroke="#ffffff1a" stroke-width="2"/>')
cl = s.label(110, 768, "XAU/USD", 26, LBL, 1, 800, 0.1, "start")
for p in (3900, 3700):
    s.raw(f'<line x1="110" y1="{py(p):.0f}" x2="860" y2="{py(p):.0f}" stroke="#ffffff10" stroke-width="2"/>')
    s.num(970, py(p) + 9, f"{p:,}", 24, GREY, 1, "end")
l38 = s.raw(f'<line id="@ID@" x1="110" y1="{py(3800):.0f}" x2="860" y2="{py(3800):.0f}" stroke="{GOLD}" stroke-width="3" stroke-dasharray="12 8" style="opacity:0.9"/>', "l38")
s.num(970, py(3800) + 10, "3,800", 28, GOLD, 1, "end")
prices = [3930, 3912, 3921, 3898, 3880, 3889, 3862, 3845, 3851, 3826, 3808, 3815, 3786, 3768, 3774, 3748, 3729, 3738, 3712, 3704]
ts, te = K(12, 0.3), K(15, 2.2)
prev = 3940
for j, p in enumerate(prices):
    x = 130 + j * 36
    o, c_ = prev, p
    hi, lo = max(o, c_) + rnd.uniform(4, 14), min(o, c_) - rnd.uniform(4, 14)
    col = GREEN if c_ > o else RED
    top, bot = py(max(o, c_)), py(min(o, c_))
    cdl = s.raw(f'<g id="@ID@" style="opacity:0"><line x1="{x + 11}" y1="{py(hi):.0f}" x2="{x + 11}" y2="{py(lo):.0f}" stroke="{col}" stroke-width="3"/>'
                f'<rect x="{x}" y="{top:.0f}" width="22" height="{max(4, bot - top):.0f}" rx="3" fill="{col}"/></g>', "cd")
    t = ts + (te - ts) * j / (len(prices) - 1)
    s.fade(cdl, t, 0.15)
    if prev >= 3800 > p:
        brk = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(x - 70, py(3800) - 92, 190, 54, 12)}" fill="{RED}"/>'
                    f'<text x="{x + 25}" y="{py(3800) - 55:.0f}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="32" fill="#fff">หลุด 3,800</text></g>', "bk")
        s.pop(brk, t + 0.1, 0.35, 0.6); cue(t + 0.1, "tock_1", -16)
    prev = p
low = s.raw(f'<g id="@ID@" style="opacity:0"><line x1="110" y1="{py(3700):.0f}" x2="860" y2="{py(3700):.0f}" stroke="{RED}" stroke-width="3" stroke-dasharray="6 8"/>'
            f'<path d="{rrect(560, py(3700) + 14, 300, 54, 12)}" fill="#3a1218" stroke="{RED}" stroke-width="2"/>'
            f'<text x="710" y="{py(3700) + 52:.0f}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="32" fill="{RED}">ต่ำสุดแถว 3,700</text></g>', "lw")
s.fade(low, te + 0.1, 0.35); cue(te + 0.1, "bell_C5", -22)
nt = s.tx(540, 1385, "ภาพประกอบทิศทาง · ไม่ใช่กราฟราคาจริง", 26, GREY, 1, 600)

# 5  "คำถามคือ ทองลงมาขนาดนี้ น่ารับหรือยัง?"
o5, c5 = c4, K(19, -0.1)
s = S(o5, c5)
s.photo("assets/photos/goldbars.jpg", PX, 290, PW, 700, "ภาพ: Stevebidmead · CC0", o5, c5, focus="50% 60%")
q0 = s.tx(540, 1100, "คำถามคือ...", 44, LBL); s.fade(q0, K(16), 0.3)
q1 = s.tx(540, 1200, "ทองลงมาขนาดนี้", 70, WHITE); s.fade(q1, K(17), 0.35, y=12)
q2 = s.tx(540, 1310, "น่ารับหรือยัง?", 84, GOLD); s.pop(q2, K(18), 0.45, 0.6); cue(K(18), "bell_E5", -18)

# 6  "ประเด็นไม่ใช่ว่าทองถูกแค่ไหน แต่คือตลาดจะยังเพิ่มเดิมพันเรื่องขึ้นดอกเบี้ยอีกไหม"
o6, c6 = c5, K(21, -0.1)
s = S(o6, c6)
h6 = s.tx(540, 440, "ประเด็นจริงคือ...", 62, WHITE); s.fade(h6, K(19), 0.3, y=10)
g1 = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(140, 520, 800, 130, 22)}" fill="#151a22" stroke="#ffffff30" stroke-width="2"/></g>', "g1")
g1t = s.tx(540, 605, "ทองถูกแค่ไหน?", 54, LBL)
s.pop(g1, K(19, 0.3), 0.35, 0.8); s.fade(g1t, K(19, 0.35), 0.3)
k6 = s.path("M 250 588 H 830", RED, 7); s.draw(k6, K(20, -0.3), 0.35); cue(K(20, -0.3), "tock_1", -18)
tl(f'tl.to("#{g1}, #{g1t}", {{opacity: 0.35, duration: 0.3}}, {K(20):.3f});')
g2 = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 18px rgba(232,194,106,0.45))"><path d="{rrect(140, 700, 800, 230, 24)}" fill="#14110a" stroke="{GOLD}" stroke-width="4"/></g>', "g2")
s.pop(g2, K(20), 0.45, 0.7); cue(K(20), "bell_G5", -20)
g2a = s.tx(540, 795, "ตลาดจะเพิ่มเดิมพัน", 54, GOLD); s.fade(g2a, K(20, 0.1), 0.3)
g2b = s.tx(540, 875, "ขึ้นดอกเบี้ยอีกไหม?", 54, GOLD); s.fade(g2b, K(20, 0.5), 0.3)
# a "bets on hikes" meter
mt = s.tx(140, 1050, "แรงเดิมพันขึ้นดอกเบี้ย", 34, LBL, anchor="start"); s.fade(mt, K(20, 0.8), 0.3)
s.raw(f'<path d="{rrect(140, 1080, 800, 44, 22)}" fill="#1a1f27"/>')
mb = s.raw(f'<rect id="@ID@" x="140" y="1080" width="800" height="44" rx="22" fill="{GOLD}" style="opacity:0.9"/>', "mb")
tl(f'tl.fromTo("#{mb}", {{scaleX: 0.05, transformOrigin: "0% 50%"}}, {{scaleX: 0.78, duration: 1.4, ease: "power2.out", immediateRender: true}}, {K(20, 0.9):.3f});')
tl(f'tl.to("#{mb}", {{scaleX: 0.9, duration: 0.5, yoyo: true, repeat: 1, ease: "sine.inOut"}}, {K(20, 2.4):.3f});')
mq = s.num(900, 1200, "?", 70, GOLD); s.pop(mq, K(20, 2.0), 0.4, 0.3)
for j, (sym, upd) in enumerate((("$", True), ("%", True))):
    x = 360 + j * 360
    ic = s.raw(f'<g id="@ID@" style="opacity:0"><circle cx="{x}" cy="1260" r="46" fill="none" stroke="{GOLD}" stroke-width="4"/>'
               f'<text x="{x}" y="1276" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="42" fill="{GOLD}">{sym}</text>'
               f'{arrow(x + 80, 1258, upd, GREEN, 1.0)}</g>', "ic")
    s.pop(ic, K(20, 1.2 + j * 0.25), 0.35, 0.5)

# 7  two scenarios
o7, c7 = c6, K(26, -0.1)
s = S(o7, c7)
h7 = s.tx(540, 400, "2 ทางที่ต้องจับตา", 60, WHITE); s.fade(h7, K(21), 0.3, y=10)
A = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(80, 450, 920, 440, 24)}" fill="#160d10" stroke="{RED}" stroke-width="3"/></g>', "A")
s.pop(A, K(21), 0.4, 0.85); cue(K(21), "pop_3", -20)
a1 = s.tx(120, 525, "ถ้า $ กับยีลด์ ยังแข็ง", 44, WHITE, anchor="start"); s.fade(a1, K(21, 0.1), 0.3)
pa = s.path("M 130 600 L 200 640 L 250 620 L 330 700 L 390 680 L 470 760 L 530 740 L 600 820", RED, 6,
            style="filter:drop-shadow(0 0 10px rgba(255,77,94,0.8))")
s.draw(pa, K(21, 0.5), 1.4, "power1.inOut")
s.raw(f'<g>{arrow(640, 840, False, RED, 0.9)}</g>')
a2 = s.tx(960, 760, "ทองยังมี", 40, LBL, anchor="end"); a3 = s.tx(960, 830, "แรงกดดัน", 54, RED, anchor="end")
s.fade(a2, K(22), 0.3); s.pop(a3, K(22, 0.15), 0.4, 0.6, "100% 50%"); cue(K(22, 0.15), "land-light_1", -16)
B = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(80, 930, 920, 500, 24)}" fill="#0d1612" stroke="{GREEN}" stroke-width="3"/></g>', "B")
s.pop(B, K(23), 0.4, 0.85); cue(K(23), "pop_4", -20)
b1 = s.tx(120, 1005, "ถ้าสองตัวนี้ เริ่มพัก", 44, WHITE, anchor="start"); s.fade(b1, K(23, 0.1), 0.3)
pb1 = s.path("M 130 1080 L 200 1130 L 260 1110 L 330 1200 L 390 1180 L 440 1250", "#c9ced6", 6)
s.draw(pb1, K(23, 0.4), 0.9)
pb2 = s.path("M 440 1250 L 490 1215 L 540 1245 L 590 1222 L 640 1243", GOLD, 6); s.draw(pb2, K(24), 0.9)
lowl = s.raw(f'<line id="@ID@" x1="420" y1="1262" x2="680" y2="1262" stroke="{GOLD}" stroke-width="3" stroke-dasharray="8 8" style="opacity:0"/>', "ll")
s.fade(lowl, K(24, 0.3), 0.3)
b2 = s.tx(560, 1310, "ไม่ทำโลว์ใหม่", 32, GOLD); s.fade(b2, K(24, 0.4), 0.3); cue(K(24, 0.4), "tick-crisp_2", -22)
pb3 = s.path("M 640 1243 L 700 1180 L 750 1200 L 820 1100", GREEN, 7, style="filter:drop-shadow(0 0 10px rgba(61,220,151,0.8))")
s.draw(pb3, K(25), 0.6, "power2.out"); cue(K(25), "whoosh-short_2", -20)
b3 = s.tx(960, 1380, "ค่อยมองหาจังหวะเด้ง", 46, GREEN, anchor="end"); s.pop(b3, K(25, 0.3), 0.4, 0.6, "100% 50%")
cue(K(25, 0.3), "bell_C5", -20)

# 8  "อย่ารีบรับมีด ให้ตลาดยืนยันก่อน"
o8, c8 = c7, K(28, -0.1)
s = S(o8, c8)
s.photo("assets/photos/ingots.jpg", PX, 290, PW, 600, "ภาพ: Szaaman · สาธารณสมบัติ", o8, c8, focus="50% 50%")
d1 = s.tx(540, 1070, "อย่ารีบรับมีด", 92, RED); s.pop(d1, K(26), 0.45, 0.6); cue(K(26), "land_1", -14)
ck = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 14px rgba(232,194,106,0.5))"><path d="{rrect(170, 1150, 740, 110, 55)}" fill="#14110a" stroke="{GOLD}" stroke-width="3"/>'
           f'<path d="M 215 1205 L 237 1227 L 277 1183" fill="none" stroke="{GOLD}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></g>', "ck")
s.pop(ck, K(27), 0.4, 0.7); cue(K(27), "click-confirm_1", -18)
ckt = s.tx(575, 1222, "ให้ตลาดยืนยันก่อน", 52, GOLD); s.fade(ckt, K(27, 0.1), 0.3)

# 9  outro (handles, no end card; brand lines in English, the line under them in Thai)
K_ORD, K_DONT, K_FOL = K(28), K(31), K(32)
s = S(K_ORD - 0.1, TOTAL)
gid = s.uid("gr")
es = s.raw(f'<g id="@ID@" style="opacity:0"><defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
           f'<stop offset="0" stop-color="rgb(232,194,106)" stop-opacity="0.26"/><stop offset="1" stop-color="rgb(232,194,106)" stop-opacity="0.04"/></linearGradient></defs>'
           f'<path d="M 500 380 L 580 380 L 770 1240 L 310 1240 Z" fill="url(#{gid})"/></g>', "sp")
s.fade(es, K_ORD, 0.6)
em = s.raw('<image id="@ID@" href="assets/otm_emblem.png" x="390" y="900" width="300" height="291" style="opacity:0;filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>', "i")
s.pop(em, K_ORD, 0.7, 0.6); cue(K_ORD, "bell_A4", -16)
o1 = s.label(540, 1300, "ORDER THE MARKET", 32, GOLD, 0, 800, 0.3, "middle"); s.fade(o1, K_ORD + 0.2, 0.5)
o2 = s.tx(540, 1362, "อย่าให้ตลาดเป็นฝ่ายสั่งคุณ", 32, WHITE, weight=600); s.fade(o2, K_DONT, 0.4)
pw = len("FOLLOW FOR MORE") * 30 * 0.74 + 52
o3 = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="{540 - pw / 2:.0f}" y="1441" width="{pw:.0f}" height="58" rx="29" fill="{GOLD}" '
           f'style="filter:drop-shadow(0 0 12px rgba(255,255,255,0.35))"/><text x="540" y="1481" text-anchor="middle" font-family="Montserrat" '
           f'font-weight="800" font-size="30" letter-spacing="0.06em" fill="#111">FOLLOW FOR MORE</text></g>', "pl")
s.pop(o3, K_FOL, 0.4, 0.6); cue(K_FOL, "click-confirm_1", -16)
hx = 290
soc = s.raw(f'<g id="@ID@" style="opacity:0">'
            f'<rect x="{hx}" y="1548" width="36" height="36" rx="10" fill="none" stroke="#fff" stroke-width="3"/>'
            f'<circle cx="{hx + 18}" cy="1566" r="8.5" fill="none" stroke="#fff" stroke-width="3"/><circle cx="{hx + 28}" cy="1556" r="2.4" fill="#fff"/>'
            f'<text x="{hx + 48}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@fxzuez_28</text>'
            f'<path d="M {hx + 322} 1546 V 1574 A 9 9 0 1 1 {hx + 313} 1565 M {hx + 322} 1546 Q {hx + 326} 1557 {hx + 338} 1558" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>'
            f'<text x="{hx + 348}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@zuez_28</text></g>', "so")
disc = s.label(540, 1650, "EDUCATIONAL ONLY · NOT FINANCIAL ADVICE", 28, GREY, 0, 600, 0.12, "middle")
s.fade(soc, K_DONT + 0.6, 0.5, y=12)
s.fade(disc, K_DONT + 0.9, 0.5)

# ------------------------------------------------------------------ header, dust, fade-out
tl(f'tl.to("#hdr, #mark", {{opacity: 0, duration: 0.3}}, {K_ORD - 0.3:.3f});')
tl(f'tl.to("#root", {{opacity: 0, duration: 0.9, ease: "power1.in"}}, {TOTAL - 0.9:.3f});')
dust = ""
for k in range(36):
    x, y, r, op = rnd.uniform(0, 1080), rnd.uniform(0, 1920), rnd.uniform(1.2, 3.2), rnd.uniform(0.05, 0.2)
    dust += f'<circle id="d{k}" cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#fff" opacity="{op:.2f}"/>'
    tl(f'tl.fromTo("#d{k}", {{x: 0, y: 0}}, {{x: {rnd.uniform(-70, 70):.0f}, y: {-rnd.uniform(150, 480):.0f}, duration: {TOTAL}, ease: "none"}}, 0);')
hdr = (f'<g id="hdr"><rect x="60" y="180" width="6" height="56" rx="3" fill="{GOLD}"/>'
       f'<text x="84" y="206" font-family="Montserrat" font-weight="800" font-size="26" letter-spacing="0.2em" fill="{GOLD}">ORDER THE MARKET</text>'
       f'<text x="84" y="238" font-family="Kanit" font-weight="600" font-size="26" fill="{LBL}">ข่าวทอง · FOMC Minutes</text>'
       f'<text x="1020" y="238" text-anchor="end" font-family="Kanit" font-weight="600" font-size="26" fill="{GREY}">18 พ.ย. 2026 (เวลาสหรัฐฯ)</text></g>')

FONTS = "".join(
    f"@font-face {{ font-family: 'Kanit'; font-style: normal; font-weight: {w}; font-display: block; "
    f"src: url('assets/fonts/kanit-{sub}-{w}-normal.woff2') format('woff2'); unicode-range: {rng}; }}\n"
    for w in (600, 700)
    for sub, rng in (("thai", "U+02D7, U+0303, U+0331, U+0E01-0E5B, U+200C-200D, U+25CC"),
                     ("latin", "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, "
                               "U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD")))
scenes_svg = "\n".join(f'<g id="{x.id}" style="opacity:0;visibility:hidden" data-layout-allow-overlap>' + "".join(x.items) + "</g>" for x in S.scenes)
CSS = FONTS + """
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #000; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #000; font-family: Montserrat, sans-serif; color: #fff; }
#stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
#vig { position: absolute; inset: 0; pointer-events: none; background: radial-gradient(ellipse at 50% 48%, rgba(40,44,52,0.35) 0%, transparent 55%, rgba(0,0,0,0.6) 100%); }
#mark { position: absolute; left: 505px; top: 1580px; width: 70px; opacity: 0.8; filter: drop-shadow(0 0 10px rgba(255,255,255,0.2)); }
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
    <div id="root" data-composition-id="otm-fedgold-th" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        {hdr}
{scenes_svg}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="otm-fedgold-th-audio" class="clip" src="assets/audio/mix_fedgold_th.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-fedgold-th"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
