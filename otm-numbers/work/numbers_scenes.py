# ---- shared scenes for "Know Your Numbers" (English: otm-numbers, Thai: otm-numbers-th); LANG is set just above this line
def ix(i):
    return W(i)

TH_ = LANG == "th"
# EN word indices are filled from work/words.json (EN_ANC below); TH token indices come from work/script.txt
EN_ANC = {}
TH_ANC = dict(hunting=0, process=2, ask=4, hundred=5, cant=6, guesses=8, three=10, winrate=11, avgwin=12, avgloss=13, say=14,
              twoR=15, oneR=16, math=17, minus=18, plus20=19, loseoften=21, stillmoney=22, stop=23, start=25, over100=28,
              genius=29, prove=31, order=33, dont=36, follow=37)

def K(key):
    a = (TH_ANC if TH_ else EN_ANC)[key]
    return ix(a[0]) + a[1] if isinstance(a, tuple) else ix(a)

TXT = dict(
    h_s=("MOST TRADERS HUNT FOR", "เทรดเดอร์ส่วนใหญ่ตามหา"), h_b=("A WINNING TRADE", "ไม้ที่ชนะ"),
    p_s=("THE ONES WHO LAST BUILD", "คนที่อยู่รอดสร้าง"), p_b=("A WINNING PROCESS", "ระบบที่ชนะ"),
    a_s=("ASK ABOUT THEIR", "ลองถามถึง"), a_b=("LAST 100 TRADES", "ร้อยไม้ล่าสุด"),
    c_s=("THEY CAN'T TELL YOU IF", "เขาตอบไม่ได้ว่า"), c_b=("THE STRATEGY MAKES MONEY", "กลยุทธ์ทำเงินหรือเปล่า"),
    jt=("LAST 100 TRADES", "ร้อยไม้ล่าสุด"),
    g_s=("NO GUESSES.", "ห้ามเดา"), g_b=("KNOW 3 NUMBERS", "รู้ตัวเลข 3 ตัว"),
    wr=("WIN RATE", "อัตราชนะ"), aw=("AVG WIN", "กำไรเฉลี่ย"), al=("AVG LOSS", "ขาดทุนเฉลี่ย"),
    ex_s=("SAY YOU", "สมมติว่าคุณ"), ex_b=("WIN 40% OF THE TIME", "ชนะ 40%"),
    m_s=("THE MATH", "คำนวณ"), m_b=("OVER 100 TRADES", "ใน 100 ไม้"),
    lo_s=("YOU LOSE MORE OFTEN", "คุณแพ้บ่อยกว่า"), lo_b=("AND STILL MAKE MONEY", "แต่ยังทำเงินได้"),
    wins=("40 WINS", "ชนะ 40"), losses=("60 LOSSES", "แพ้ 60"),
    st_b=("STOP ASKING", "เลิกถามว่า"), sa_b=("START ASKING", "เริ่มถามว่า"),
    q1=("WILL MY NEXT TRADE WIN?", "ไม้ต่อไปจะชนะไหม?"), q2a=("DOES MY STRATEGY MAKE MONEY", "กลยุทธ์ของฉันทำเงินได้ไหม"),
    q2b=("OVER 100 TRADES?", "ใน 100 ไม้?"),
    ge_s=("ONE WINNING TRADE FEELS LIKE", "ชนะไม้เดียว รู้สึกเหมือน"), ge_b=("GENIUS", "อัจฉริยะ"),
    pr_s=("ONLY YOUR NUMBERS", "มีแค่ตัวเลข"), pr_b=("PROVE YOUR EDGE", "ที่พิสูจน์ความได้เปรียบ"),
    edge=("EDGE", "ความได้เปรียบ"), pertrade=("PER TRADE", "ต่อไม้"),
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
    """Numbers and maths always in Montserrat (digits read the same in both languages)."""
    return s.label(x, y, text, size, col, op, 800, 0.02, anchor)

def toplab(s, small, big, t0, t1, bcol=WHITE, scol=LBL, bsize=52, y=560, op=0):
    ids = []
    if small:
        a = tx(s, 540, y - 72, small, 28, scol, op, 700, sp=0.12); ids.append(a)
    b = tx(s, 540, y, big, bsize, bcol, op, 800, sp=0.04); ids.append(b)
    for i in ids:
        if not op: s.fade(i, t0, 0.3, y=10)
        tl(f'tl.to("#{i}", {{opacity: 0, duration: 0.15}}, {t1 - 0.17:.3f});')
    return ids

def hide(i, t, d=0.3, to=0):
    tl(f'tl.to("#{i}", {{opacity: {to}, duration: {d}}}, {t:.3f});')

# 1  "Most traders are hunting for a winning trade. The ones who last are building a winning process."
s = S(0, K("ask") - 0.1, first=True)
toplab(s, X("h_s"), X("h_b"), 0, K("process") - 0.1, WHITE, LBL, 58, op=1)
toplab(s, X("p_s"), X("p_b"), K("process"), K("ask") - 0.1, GOLD, LBL, 58)
f1 = s.fig(360, 1.0, WHITE, 1)
cnd = s.raw(f'<g id="@ID@"><line x1="250" y1="820" x2="250" y2="980" stroke="#e9ecf1" stroke-width="4"/><rect x="230" y="850" width="40" height="90" rx="4" fill="{GOLD}"/></g>', "cd")
mg = s.raw(f'<g id="@ID@"><circle cx="250" cy="895" r="62" fill="none" stroke="#f4f4f2" stroke-width="7"/>'
           f'<line x1="296" y1="940" x2="350" y2="1000" stroke="#f4f4f2" stroke-width="12" stroke-linecap="round"/></g>', "mg")
tl(f'tl.fromTo("#{mg}", {{x: -10, y: 0}}, {{x: 14, y: 8, duration: 0.6, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}}, 0.2);')
f1g = s.fig(780, 1.0, GOLD); s.pop(f1g, K("process"), 0.45)
gear = "".join(f'<rect x="{776 - 8}" y="{850 - 92}" width="16" height="30" rx="4" fill="{GOLD}" transform="rotate({a} 776 850)"/>' for a in range(0, 360, 45))
gr = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 12px rgba(232,194,106,0.8))">{gear}<circle cx="776" cy="850" r="68" fill="none" stroke="{GOLD}" stroke-width="12"/>'
           f'<circle cx="776" cy="850" r="22" fill="{GOLD}"/></g>', "gr")
s.pop(gr, K("process") + 0.3, 0.45, 0.4, "50% 50%")
tl(f'tl.fromTo("#{gr}", {{rotation: 0}}, {{rotation: 180, svgOrigin: "776 850", duration: 3, ease: "none", immediateRender: false}}, {K("process") + 0.3:.3f});')
cue(K("process"), "bell_C5", -20)

# 2  "Ask a struggling trader about their last hundred trades... and they can't tell you if their strategy even makes money."
s = S(K("ask") - 0.1, K("guesses") - 0.1)
f2 = s.fig(230, 1.0, WHITE); s.pop(f2, K("ask"), 0.4)
qm = s.label(230, 1010, "?", 90, RED, 0, 800, 0); s.pop(qm, K("cant"), 0.4, 0.3, "50% 50%")
toplab(s, X("a_s"), X("a_b"), K("ask"), K("cant") - 0.1, WHITE, LBL, 58)
toplab(s, X("c_s"), X("c_b"), K("cant"), K("guesses") - 0.1, RED, LBL, 48)
jr = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(420, 700, 520, 520, 24)}" fill="#0f1319" stroke="#f4f4f2" stroke-opacity="0.7" stroke-width="3"/>'
           + "".join(f'<line x1="460" y1="{820 + k * 60}" x2="{900 - (k % 3) * 60}" y2="{820 + k * 60}" stroke="#3a3f47" stroke-width="10" stroke-linecap="round"/>' for k in range(6))
           + '</g>', "jr")
s.pop(jr, K("hundred") - 0.1, 0.45, 0.6, "50% 50%")
jt = tx(s, 680, 770, X("jt"), 30, GOLD, 0, 800, sp=0.1); s.fade(jt, K("hundred"), 0.3)
bq = s.label(680, 1110, "???", 110, "#6b7079", 0, 800, 0.1); s.fade(bq, K("cant") + 0.2, 0.4)
cue(K("hundred") - 0.1, "pop_1", -20); cue(K("cant"), "tock_1", -18)

# 3  "You can't run a business on guesses. So know three numbers. Your win rate. Your average win. Your average loss.
#     Say you win forty percent of the time. Your average win is two R. Your average loss is one R."
s = S(K("guesses") - 0.1, K("math") - 0.1, ground=False, restore=False)
toplab(s, X("g_s"), X("g_b"), K("guesses"), K("say") - 0.1, GOLD, LBL, 60)
toplab(s, X("ex_s"), X("ex_b"), K("say"), K("math") - 0.1, WHITE, LBL, 52)
bd = s.raw(f'<path id="@ID@" d="{rrect(150, 650, 780, 360, 24)}" fill="#0f1319" stroke="{GOLD}" stroke-opacity="0.6" stroke-width="3" style="opacity:0"/>', "bd")
s.pop(bd, K("three") - 0.1, 0.4, 0.7, "50% 50%")
VALS = [("wr", "winrate", "40%", "say", 1.0), ("aw", "avgwin", "2R", "twoR", 0.7), ("al", "avgloss", "1R", "oneR", 0.7)]
for j, (key, k_in, val, k_val, dt) in enumerate(VALS):
    y = 750 + j * 105
    l = tx(s, 200, y, X(key), 36, WHITE, 0, 800, "start", sp=0.06); s.fade(l, K(k_in) - 0.1, 0.3)
    dsh = s.raw(f'<line id="@ID@" x1="640" y1="{y - 12}" x2="880" y2="{y - 12}" stroke="#6b7079" stroke-width="4" stroke-dasharray="10 10" style="opacity:0"/>', "dl")
    s.fade(dsh, K(k_in) - 0.1, 0.3)
    v = num(s, 880, y + 6, val, 64, [GOLD, GOLD, RED][j], 0, "end")
    hide(dsh, K(k_val) + dt - 0.1, 0.15)
    tl(f'tl.fromTo("#{v}", {{opacity: 0, scale: 1.4, transformOrigin: "100% 50%"}}, {{opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.8)", immediateRender: false}}, {K(k_val) + dt:.3f});')
    cue(K(k_in) - 0.1, "tick_" + str(j + 1), -22); cue(K(k_val) + dt, "pop_" + str(j + 1), -18)
rr = random.Random(11)
order = [1] * 40 + [0] * 60; rr.shuffle(order)
dots = "".join(f'<circle cx="{285 + (k % 20) * 27}" cy="{1080 + (k // 20) * 30}" r="10" fill="{GOLD if w else RED}" fill-opacity="{0.95 if w else 0.7}"/>'
               for k, w in enumerate(order))
dg = s.raw(f'<g id="@ID@" style="opacity:0">{dots}</g>', "dg")
s.fade(dg, K("say") + 1.2, 0.5)
lw = tx(s, 300, 1260, X("wins"), 30, GOLD, 0, 800, "start", sp=0.08); s.fade(lw, K("say") + 1.4, 0.3)
ll = tx(s, 780, 1260, X("losses"), 30, RED, 0, 800, "end", sp=0.08); s.fade(ll, K("say") + 1.4, 0.3)

# 4  "Forty times two... minus sixty times one. That's plus twenty R over a hundred trades. You lose more often... and still make money."
s = S(K("math") - 0.1, K("stop") - 0.1, ground=False, hide=False, restore=False)
toplab(s, X("m_s"), X("m_b"), K("math"), K("loseoften") - 0.1, WHITE, LBL, 52)
toplab(s, X("lo_s"), X("lo_b"), K("loseoften"), K("stop") - 0.1, GOLD, LBL, 52)
m1 = num(s, 540, 740, "40 × 2R = +80R", 64, GOLD); s.fade(m1, K("math") - 0.05, 0.35, y=10)
m2 = num(s, 540, 840, "60 × 1R = −60R", 64, RED); s.fade(m2, K("minus") - 0.05, 0.35, y=10)
rl = s.path("M 260 880 H 820", "#ffffff80", 4); s.draw(rl, K("plus20") - 0.3, 0.3)
m3 = num(s, 540, 990, "= +20R", 104, GOLD)
tl(f'tl.fromTo("#{m3}", {{opacity: 0, scale: 1.4, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)", immediateRender: false}}, {K("plus20") - 0.05:.3f});')
cue(K("math") - 0.05, "tick_1", -20); cue(K("minus") - 0.05, "tick_2", -20); cue(K("plus20") - 0.05, "bell_G5", -16)
eq, pts = 0, []
for k, w in enumerate(order):
    eq += 2 if w else -1
    pts.append((160 + k * 7.6, 1270 - eq * 6.5))
cv = s.path("M 160 1270 L " + " L ".join(f"{x:.0f} {y:.0f}" for x, y in pts), GOLD, 4, style="filter:drop-shadow(0 0 8px rgba(232,194,106,0.8))")
zl = s.raw(f'<line id="@ID@" x1="160" y1="1270" x2="930" y2="1270" stroke="#ffffff40" stroke-width="2" stroke-dasharray="8 8" style="opacity:0"/>', "zl")
s.fade(zl, K("loseoften") - 0.3, 0.3)
s.draw(cv, K("loseoften") - 0.1, max(1.6, K("stop") - 0.6 - K("loseoften")), "none")
cue(K("loseoften") - 0.1, "swell_1", -22)

# 5  "So stop asking, will my next trade win? Start asking, does my strategy make money over a hundred trades?"
s = S(K("stop") - 0.1, K("genius") - 0.1, ground=False, hide=False)
toplab(s, "", X("st_b"), K("stop"), K("start") - 0.1, RED, LBL, 58)
toplab(s, "", X("sa_b"), K("start"), K("genius") - 0.1, GOLD, LBL, 58)
c1 = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(150, 680, 780, 150, 26)}" fill="#1a0f12" stroke="{RED}" stroke-width="3"/></g>', "c1")
s.pop(c1, K("stop") + 0.1, 0.4, 0.7, "50% 50%")
q1 = tx(s, 540, 772, X("q1"), 40, WHITE, 0, 800, sp=0.03); s.fade(q1, K("stop") + 0.2, 0.3)
k1 = s.path("M 190 755 H 890", RED, 6); s.draw(k1, K("start") - 0.4, 0.35); cue(K("start") - 0.4, "tock_1", -18)
c2 = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 18px rgba(232,194,106,0.45))"><path d="{rrect(150, 900, 780, 220, 26)}" fill="#14110a" stroke="{GOLD}" stroke-width="4"/></g>', "c2")
s.pop(c2, K("start") + 0.1, 0.45, 0.7, "50% 50%")
q2 = tx(s, 540, 1000, X("q2a"), 40, GOLD, 0, 800, sp=0.03); s.fade(q2, K("start") + 0.2, 0.3)
q3 = tx(s, 540, 1070, X("q2b"), 40, GOLD, 0, 800, sp=0.03); s.fade(q3, K("over100") - 0.2, 0.3)
cue(K("start") + 0.1, "bell_E5", -20)

# 6  "One winning trade can make you feel like a genius. Only your numbers can prove your edge."
s = S(K("genius") - 0.1, K("order") + 0.35)
toplab(s, X("ge_s"), X("ge_b"), K("genius"), K("prove") - 0.1, WHITE, LBL, 60)
toplab(s, X("pr_s"), X("pr_b"), K("prove"), K("order") + 0.35, GOLD, LBL, 54)
f6 = s.fig(260, 1.0, WHITE); s.pop(f6, K("genius"), 0.4)
crown = s.raw(f'<path id="@ID@" d="M 222 1050 L 230 1010 L 248 1032 L 260 1000 L 272 1032 L 290 1010 L 298 1050 Z" fill="{GOLD}" '
              f'style="opacity:0;filter:drop-shadow(0 0 10px rgba(232,194,106,0.9))"/>', "cr")
s.pop(crown, K("genius") + 0.6, 0.4, 0.3, "50% 50%"); cue(K("genius") + 0.6, "bell_A4", -20)
tl(f'tl.to("#{crown}", {{y: 60, rotation: 40, opacity: 0, transformOrigin: "50% 50%", duration: 0.6, ease: "power2.in"}}, {K("prove") - 0.1:.3f});')
cue(K("prove") - 0.1, "whoosh-short_2", -22)
cd6 = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 18px rgba(232,194,106,0.4))"><path d="{rrect(410, 720, 480, 470, 24)}" fill="#14110a" stroke="{GOLD}" stroke-width="3"/></g>', "c6")
s.pop(cd6, K("prove"), 0.45, 0.6, "50% 50%")
for j, (key, val, col) in enumerate([("wr", "40%", GOLD), ("aw", "2R", GOLD), ("al", "1R", RED)]):
    y = 800 + j * 80
    l = tx(s, 440, y, X(key), 28, LBL, 0, 800, "start", sp=0.06); s.fade(l, K("prove") + 0.2 + j * 0.12, 0.3)
    v = num(s, 860, y + 2, val, 40, col, 0, "end"); s.fade(v, K("prove") + 0.2 + j * 0.12, 0.3)
ln6 = s.raw(f'<line id="@ID@" x1="440" y1="1020" x2="860" y2="1020" stroke="{GOLD}" stroke-opacity="0.5" stroke-width="2" style="opacity:0"/>', "ln")
s.fade(ln6, K("prove") + 0.5, 0.3)
el = tx(s, 440, 1090, X("edge"), 32, GOLD, 0, 800, "start", sp=0.08); s.fade(el, K("prove") + 0.7, 0.3)
ev = num(s, 860, 1094, "+0.2R", 52, GOLD, 0, "end")
tl(f'tl.fromTo("#{ev}", {{opacity: 0, scale: 1.4, transformOrigin: "100% 50%"}}, {{opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.8)", immediateRender: false}}, {K("prove") + 0.8:.3f});')
pt = tx(s, 860, 1150, X("pertrade"), 26, LBL, 0, 700, "end", sp=0.1); s.fade(pt, K("prove") + 0.9, 0.3)
cue(K("prove") + 0.8, "bell_G5", -18)

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
