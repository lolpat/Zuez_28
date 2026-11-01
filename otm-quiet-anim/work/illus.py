"""Line-art pictures for OTM Trade In Silence. One small animated drawing per phrase, in the zone between the words
(centred near y=700) and the emblem (y=1500). White strokes with a soft glow, gold for the payoff, red only for loss.
build(G, tl, cue) returns SVG markup; G[i] = dict(o=open, c=close, w=[absolute word starts]) for phrase group i."""
import math, random

W, GOLD, RED, GREEN, WHITE = 1080, "#e8c26a", "#ff4d5e", "#31d07f", "#ffffff"
CX, CY = 540, 1150


class B:
    def __init__(self, tl, cue):
        self.tl, self.cue, self.svg, self.n = tl, cue, [], 0

    def id(self, p="e"):
        self.n += 1
        return f"{p}{self.n}"

    # --- markup helpers -------------------------------------------------------------------------------------------
    def path(self, d, col=WHITE, w=4, fill="none", extra="", drawn=False):
        i = self.id("p")
        dash = "" if drawn else 'pathLength="1" style="stroke-dasharray:1 1.2;stroke-dashoffset:1.1"'
        self.cur.append(f'<path id="{i}" d="{d}" fill="{fill}" stroke="{col}" stroke-width="{w}" stroke-linecap="round" '
                        f'stroke-linejoin="round" {dash} {extra}/>')
        return i

    def raw(self, s, pre="r"):
        i = self.id(pre)
        self.cur.append(s.replace("@ID@", i))
        return i

    def text(self, x, y, s, size=40, col=WHITE, weight=700, anchor="middle", op=0, family="Montserrat", extra=""):
        return self.raw(f'<text id="@ID@" x="{x}" y="{y}" text-anchor="{anchor}" font-family="{family}" font-weight="{weight}" '
                        f'font-size="{size}" fill="{col}" style="opacity:{op}" {extra}>{s}</text>', "t")

    def circ_d(self, cx, cy, r):
        return f"M {cx - r} {cy} a {r} {r} 0 1 0 {2 * r} 0 a {r} {r} 0 1 0 {-2 * r} 0"

    def rrect_d(self, x, y, w, h, r):
        return (f"M {x + r} {y} H {x + w - r} Q {x + w} {y} {x + w} {y + r} V {y + h - r} Q {x + w} {y + h} {x + w - r} {y + h} "
                f"H {x + r} Q {x} {y + h} {x} {y + h - r} V {y + r} Q {x} {y} {x + r} {y} Z")

    # --- animation helpers ----------------------------------------------------------------------------------------
    def draw(self, i, t, d=0.8, ease="power2.inOut"):
        self.tl(f'tl.fromTo("#{i}", {{strokeDashoffset: 1.1}}, {{strokeDashoffset: 0, duration: {d:.3f}, ease: "{ease}", immediateRender: false}}, {t:.3f});')

    def fade(self, i, t, d=0.35, to=1, frm=0, y=0):
        ys = f", y: {y}" if y else ""
        ye = ", y: 0" if y else ""
        self.tl(f'tl.fromTo("#{i}", {{opacity: {frm}{ys}}}, {{opacity: {to}{ye}, duration: {d:.3f}, ease: "power2.out", immediateRender: false}}, {t:.3f});')

    def pop(self, i, t, d=0.35, frm=0.0):
        self.tl(f'tl.fromTo("#{i}", {{opacity: 0, scale: {frm}, transformOrigin: "50% 50%"}}, '
                f'{{opacity: 1, scale: 1, duration: {d:.3f}, ease: "back.out(2)", immediateRender: false}}, {t:.3f});')

    def scene(self, o, c):
        g = self.id("s")
        self.cur = []
        self.scenes.append((g, o, c, self.cur))
        self.tl(f'tl.set("#{g}", {{opacity: 1, visibility: "visible"}}, {o:.3f});')
        self.tl(f'tl.to("#{g}", {{opacity: 0, duration: 0.22, ease: "power2.in"}}, {c - 0.22:.3f});')
        self.tl(f'tl.set("#{g}", {{opacity: 0, visibility: "hidden"}}, {c:.3f});')
        return g


def build(G, tl, cue, total):
    b = B(tl, cue)
    b.scenes = []
    rnd = random.Random(28)
    w = lambda gi, k: G[gi]["w"][k]

    # 0-1  a chart dips (humble, in private), then climbs in gold (pays, in public)
    b.scene(G[0]["o"], G[1]["c"])
    b.path("M 200 1360 H 880", "#ffffff40", 2, drawn=True)
    p1 = b.path("M 220 1120 L 290 1080 L 350 1130 L 410 1070 L 470 1160 L 520 1300")
    b.draw(p1, w(0, 0), w(0, 4) - w(0, 0) + 0.2)
    rc = b.raw(f'<g id="@ID@" style="opacity:0"><line x1="520" y1="1215" x2="520" y2="1335" stroke="{RED}" stroke-width="4"/>'
               f'<rect x="504" y="1236" width="32" height="74" fill="{RED}"/></g>')
    b.pop(rc, w(0, 5)); cue(w(0, 5), "land-light_1", -16)
    p2 = b.path("M 520 1300 L 600 1250 L 650 1270 L 730 1150 L 780 1170 L 860 1000", GOLD, 6)
    b.draw(p2, w(1, 0), w(1, 5) - w(1, 0) + 0.3)
    ar = b.path("M 820 1010 L 862 998 L 858 1042", GOLD, 6)
    b.draw(ar, w(1, 5) + 0.2, 0.3)
    glow = b.raw(f'<circle id="@ID@" cx="860" cy="1000" r="16" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 14px {GOLD})"/>', "c")
    b.pop(glow, w(1, 5) + 0.4); cue(w(1, 5) + 0.4, "bell_E5", -20)

    # 2  an eye opens and looks around
    b.scene(G[2]["o"], G[2]["c"])
    up = b.path("M 360 1150 Q 540 1000 720 1150"); lo = b.path("M 360 1150 Q 540 1300 720 1150")
    b.draw(up, w(2, 0), 0.5); b.draw(lo, w(2, 0), 0.5)
    iris = b.path(b.circ_d(540, 1150, 62), WHITE, 4)
    b.draw(iris, w(2, 1), 0.45)
    pupil = b.raw(f'<circle id="@ID@" cx="540" cy="1150" r="26" fill="{GOLD}" style="opacity:0"/>', "c")
    b.pop(pupil, w(2, 1) + 0.2)
    tl(f'tl.to("#{pupil}", {{x: -26, duration: 0.35, ease: "power2.inOut"}}, {w(2, 1) + 0.6:.3f});')
    tl(f'tl.to("#{pupil}", {{x: 22, duration: 0.45, ease: "power2.inOut"}}, {w(2, 1) + 1.0:.3f});')

    # 3  a phone with a green P&L gets screenshotted, likes float up
    b.scene(G[3]["o"], G[3]["c"])
    ph = b.path(b.rrect_d(430, 940, 220, 420, 34), WHITE, 4)
    b.draw(ph, G[3]["o"], 0.55)
    pl = b.text(540, 1110, "+$2,480", 46, GREEN, 800)
    b.fade(pl, w(3, 2), 0.3, y=10)
    mc = b.path("M 465 1250 L 500 1230 L 530 1240 L 565 1195 L 590 1205 L 615 1160", GREEN, 4)
    b.draw(mc, w(3, 2), 0.5)
    fl = b.raw('<rect id="@ID@" x="434" y="944" width="212" height="412" rx="30" fill="#fff" style="opacity:0"/>', "r")
    tl(f'tl.fromTo("#{fl}", {{opacity: 0.85}}, {{opacity: 0, duration: 0.35, ease: "power2.out", immediateRender: false}}, {w(3, 3) + 0.15:.3f});')
    cue(w(3, 3) + 0.15, "snap_1", -12)
    for k, (x, dy) in enumerate([(700, 0), (735, 0.18), (690, 0.36)]):
        h = b.text(x, 1180, "♥", 44, "#ff5d7d", 700)
        tl(f'tl.fromTo("#{h}", {{opacity: 0, y: 0}}, {{opacity: 1, y: -60, duration: 0.5, ease: "power2.out", immediateRender: false}}, {w(3, 3) + 0.4 + dy:.3f});')
        tl(f'tl.to("#{h}", {{opacity: 0, y: -130, duration: 0.5, ease: "power1.in"}}, {w(3, 3) + 0.9 + dy:.3f});')
        cue(w(3, 3) + 0.4 + dy, "pop_" + str(k + 1), -20)

    # 4  a clock whose hands spin through the hours
    b.scene(G[4]["o"], G[4]["c"])
    cl = b.path(b.circ_d(540, 1150, 150), WHITE, 4)
    b.draw(cl, G[4]["o"], 0.6)
    ticks = ""
    for k in range(12):
        a = k / 12 * math.tau
        ticks += f'<line x1="{540 + math.sin(a) * 128:.1f}" y1="{1150 - math.cos(a) * 128:.1f}" x2="{540 + math.sin(a) * 140:.1f}" y2="{1150 - math.cos(a) * 140:.1f}" stroke="#ffffff99" stroke-width="3"/>'
    tk = b.raw(f'<g id="@ID@" style="opacity:0">{ticks}</g>')
    b.fade(tk, G[4]["o"] + 0.3, 0.4)
    mh = b.raw(f'<line id="@ID@" x1="540" y1="1150" x2="540" y2="1040" stroke="{WHITE}" stroke-width="5" stroke-linecap="round" style="opacity:0"/>', "l")
    hh = b.raw(f'<line id="@ID@" x1="540" y1="1150" x2="540" y2="1080" stroke="{GOLD}" stroke-width="7" stroke-linecap="round" style="opacity:0"/>', "l")
    for i in (mh, hh): b.fade(i, G[4]["o"] + 0.4, 0.3)
    dur = G[4]["c"] - w(4, 3)
    tl(f'tl.fromTo("#{mh}", {{rotation: 0}}, {{rotation: 1080, svgOrigin: "540 1150", duration: {dur:.3f}, ease: "power1.inOut", immediateRender: false}}, {w(4, 3):.3f});')
    tl(f'tl.fromTo("#{hh}", {{rotation: 0}}, {{rotation: 90, svgOrigin: "540 1150", duration: {dur:.3f}, ease: "power1.inOut", immediateRender: false}}, {w(4, 3):.3f});')
    for k in range(4): cue(w(4, 3) + k * 0.28, "tick_" + str(k % 3 + 1), -22)

    # 5  a backtest fills with candles; a journal fills with lines
    b.scene(G[5]["o"], G[5]["c"])
    ch = b.path("M 220 1330 H 500", "#ffffff60", 2, drawn=True)
    v = 1200
    for k in range(9):
        o = v; v = max(1040, min(1300, v + rnd.choice([-1, 1]) * rnd.uniform(25, 70)))
        top, bot = min(o, v), max(o, v); x = 240 + k * 30
        col = GOLD if v < o else "#ffffffb0"
        c = b.raw(f'<g id="@ID@" style="opacity:0"><line x1="{x}" y1="{top - 18}" x2="{x}" y2="{bot + 18}" stroke="{col}" stroke-width="3"/>'
                  f'<rect x="{x - 9}" y="{top}" width="18" height="{max(6, bot - top):.0f}" fill="{col}"/></g>')
        b.pop(c, w(5, 1) - 0.1 + k * 0.07, 0.25, 0.4)
    nb = b.path(b.rrect_d(590, 1010, 250, 320, 16), WHITE, 4)
    b.draw(nb, w(5, 2) - 0.2, 0.5)
    for k in range(5):
        ln = b.path(f"M 620 {1070 + k * 50} H {800 - (k % 2) * 50}", "#ffffffc0", 3)
        b.draw(ln, w(5, 3) + k * 0.12, 0.3)
    cue(w(5, 3), "key_3", -22); cue(w(5, 3) + 0.25, "key_5", -22)

    # 6  three trade setups, all crossed out
    b.scene(G[6]["o"], G[6]["c"])
    for k, lab in enumerate(["BUY", "SELL", "BUY"]):
        x = 225 + k * 220
        cd = b.path(b.rrect_d(x, 1080, 190, 150, 18), WHITE, 3)
        b.draw(cd, G[6]["o"] + k * 0.12, 0.45)
        tx = b.text(x + 95, 1140, lab, 34, WHITE, 800)
        b.fade(tx, G[6]["o"] + 0.25 + k * 0.12, 0.3)
        mini = b.path(f"M {x + 30} 1205 L {x + 70} {1185 if lab == 'BUY' else 1195} L {x + 110} 1198 L {x + 160} {1170 if lab == 'BUY' else 1210}", "#ffffff90", 3)
        b.draw(mini, G[6]["o"] + 0.35 + k * 0.12, 0.35)
        x1 = b.path(f"M {x + 25} 1100 L {x + 165} 1210 M {x + 165} 1100 L {x + 25} 1210", GOLD, 6)
        b.draw(x1, w(6, 3) + k * 0.16, 0.25)
        cue(w(6, 3) + k * 0.16, "click_" + str(k % 2 + 1), -18)

    # 8  a loud waveform falls silent
    b.scene(G[8]["o"], G[8]["c"])
    bars = ""
    ids = []
    for k in range(34):
        x = 250 + k * 17.5; h = 40 + 220 * abs(math.sin(k * 0.55)) * rnd.uniform(0.5, 1)
        i = b.id("bar"); ids.append(i)
        bars += f'<rect id="{i}" x="{x:.1f}" y="{CY - h / 2:.1f}" width="9" height="{h:.1f}" rx="4" fill="#ffffffd0"/>'
    b.raw(f'<g id="@ID@">{bars}</g>')
    sel = ", ".join("#" + i for i in ids)
    tl(f'tl.fromTo([{", ".join(repr("#" + i) for i in ids)}], {{scaleY: 0, transformOrigin: "50% 50%"}}, {{scaleY: 1, duration: 0.35, ease: "power2.out", stagger: 0.012, immediateRender: false}}, {G[8]["o"]:.3f});')
    tl(f'tl.to([{", ".join(repr("#" + i) for i in ids)}], {{scaleY: 0.03, duration: 0.6, ease: "power3.inOut", stagger: {{each: 0.012, from: "edges"}}}}, {w(8, 3) - 0.1:.3f});')
    qd = b.raw(f'<circle id="@ID@" cx="540" cy="{CY}" r="10" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 10px {GOLD})"/>', "c")
    b.pop(qd, w(8, 3) + 0.6)

    # 9  no posting, no bragging
    b.scene(G[9]["o"], G[9]["c"])
    pb = b.path(b.rrect_d(250, 1100, 250, 100, 50), WHITE, 4)
    b.draw(pb, G[9]["o"], 0.45)
    pt = b.text(375, 1166, "POST", 40, WHITE, 800)
    b.fade(pt, G[9]["o"] + 0.2, 0.3)
    s1 = b.path("M 235 1215 L 515 1085", GOLD, 6); b.draw(s1, w(9, 2), 0.3)
    mg = b.path("M 620 1130 L 700 1130 L 790 1080 L 790 1230 L 700 1180 L 620 1180 Z M 650 1180 L 665 1235 L 700 1235 L 690 1180", WHITE, 4)
    b.draw(mg, w(9, 3) - 0.15, 0.5)
    s2 = b.path("M 600 1240 L 820 1070", GOLD, 6); b.draw(s2, w(9, 5), 0.3)
    cue(w(9, 2), "whoosh-short_1", -22); cue(w(9, 5), "whoosh-short_2", -22)

    # 10  a crosshair waits, then locks onto the level
    b.scene(G[10]["o"], G[10]["c"])
    pr = b.path("M 200 1190 C 260 1120 310 1250 370 1180 S 470 1110 540 1160 S 650 1240 720 1150 S 820 1130 880 1170", "#ffffffb0", 3)
    b.draw(pr, G[10]["o"], G[10]["c"] - G[10]["o"] - 0.3, "none")
    lv = b.path("M 200 1160 H 880", GOLD, 3, extra='stroke-dasharray="12 12"', drawn=True)
    tl(f'tl.fromTo("#{lv}", {{opacity: 0}}, {{opacity: 0.8, duration: 0.4, immediateRender: false}}, {G[10]["o"] + 0.2:.3f});')
    xh = b.raw(f'<g id="@ID@" style="opacity:0"><circle cx="540" cy="1160" r="60" fill="none" stroke="#fff" stroke-width="3"/>'
               f'<line x1="540" y1="1080" x2="540" y2="1120" stroke="#fff" stroke-width="3"/><line x1="540" y1="1200" x2="540" y2="1240" stroke="#fff" stroke-width="3"/>'
               f'<line x1="460" y1="1160" x2="500" y2="1160" stroke="#fff" stroke-width="3"/><line x1="580" y1="1160" x2="620" y2="1160" stroke="#fff" stroke-width="3"/></g>')
    tl(f'tl.fromTo("#{xh}", {{opacity: 0, scale: 2.4, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: {w(10, 4) - G[10]["o"]:.3f}, ease: "power2.inOut", immediateRender: false}}, {G[10]["o"]:.3f});')
    xg = b.raw(f'<circle id="@ID@" cx="540" cy="1160" r="60" fill="none" stroke="{GOLD}" stroke-width="5" style="opacity:0;filter:drop-shadow(0 0 10px {GOLD})"/>', "c")
    b.pop(xg, w(10, 4), 0.3, 1.4); cue(w(10, 4), "click-confirm_1", -16)

    # 11  everything else drifts away; one gold candle stays
    b.scene(G[11]["o"], G[11]["c"])
    gc = b.raw(f'<g id="@ID@" style="opacity:0"><line x1="540" y1="1080" x2="540" y2="1230" stroke="{GOLD}" stroke-width="4"/>'
               f'<rect x="522" y="1110" width="36" height="90" fill="{GOLD}"/></g>')
    b.fade(gc, G[11]["o"], 0.3)
    for k in range(16):
        a = k / 16 * math.tau + rnd.uniform(-0.15, 0.15); r = rnd.uniform(140, 230)
        x, y = 540 + math.cos(a) * r, 1155 + math.sin(a) * r * 0.75; h = rnd.uniform(30, 70)
        c = b.raw(f'<g id="@ID@" style="opacity:0"><line x1="{x:.0f}" y1="{y - h / 2 - 12:.0f}" x2="{x:.0f}" y2="{y + h / 2 + 12:.0f}" stroke="#fff" stroke-width="2"/>'
                  f'<rect x="{x - 8:.0f}" y="{y - h / 2:.0f}" width="16" height="{h:.0f}" fill="#ffffffb0"/></g>')
        b.fade(c, G[11]["o"] + k * 0.02, 0.25)
        tl(f'tl.to("#{c}", {{x: {math.cos(a) * 260:.0f}, y: {math.sin(a) * 200:.0f}, opacity: 0, duration: 1.1, ease: "power2.in"}}, {w(11, 1) + rnd.uniform(0, 0.35):.3f});')
    cue(w(11, 1) + 0.2, "whoosh-long_1", -20)

    # 12  a clean line tangles into a scribble
    b.scene(G[12]["o"], G[12]["c"])
    pts = [(200, 1160)]
    x = 200
    while x < 880:
        x += rnd.uniform(25, 55)
        pts.append((x + rnd.uniform(-60, 60), 1160 + rnd.uniform(-150, 150) * min(1, (x - 200) / 300)))
    d = "M " + " L ".join(f"{px:.0f} {py:.0f}" for px, py in pts)
    sc = b.path(d, "#ffffffc0", 3)
    b.draw(sc, G[12]["o"], G[12]["c"] - G[12]["o"] - 0.2, "power1.in")

    # 13-14  a cursor chases a running price and never catches it; then it stops
    b.scene(G[13]["o"], G[14]["c"])
    tr = b.path("M 230 1220 L 330 1150 L 420 1200 L 520 1110 L 610 1170 L 700 1080 L 800 1140 L 900 1050", "#ffffff50", 3, extra='stroke-dasharray="10 10"', drawn=True)
    tl(f'tl.fromTo("#{tr}", {{opacity: 0}}, {{opacity: 1, duration: 0.4, immediateRender: false}}, {G[13]["o"]:.3f});')
    dot = b.raw(f'<circle id="@ID@" cx="230" cy="1220" r="16" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 10px {GOLD})"/>', "c")
    cur = b.raw('<path id="@ID@" d="M 180 1240 l 0 52 l 14 -14 l 10 24 l 10 -5 l -10 -23 l 20 0 z" fill="#fff" style="opacity:0"/>', "p")
    b.fade(dot, G[13]["o"], 0.2); b.fade(cur, G[13]["o"], 0.2)
    run = w(14, 1) - G[13]["o"]
    tl(f'tl.fromTo("#{dot}", {{x: 0, y: 0}}, {{keyframes: [{{x: 100, y: -70}}, {{x: 190, y: -20}}, {{x: 290, y: -110}}, {{x: 380, y: -50}}], duration: {run:.3f}, ease: "none", immediateRender: false}}, {G[13]["o"]:.3f});')
    tl(f'tl.fromTo("#{cur}", {{x: 0, y: 0}}, {{keyframes: [{{x: 60, y: -40}}, {{x: 150, y: -10}}, {{x: 230, y: -80}}, {{x: 300, y: -30}}], duration: {run:.3f}, ease: "none", immediateRender: false}}, {G[13]["o"] + 0.1:.3f});')
    tl(f'tl.to("#{dot}", {{keyframes: [{{x: 470, y: -140}}, {{x: 570, y: -80}}, {{x: 680, y: -170}}], opacity: 0, duration: 1.1, ease: "power1.in"}}, {w(14, 1):.3f});')
    tl(f'tl.to("#{cur}", {{scale: 0.85, transformOrigin: "0% 0%", duration: 0.12, yoyo: true, repeat: 1}}, {w(14, 1) + 0.1:.3f});')
    stopc = b.raw(f'<circle id="@ID@" cx="490" cy="1238" r="48" fill="none" stroke="{GOLD}" stroke-width="4" style="opacity:0"/>', "c")
    b.pop(stopc, w(14, 1) + 0.15, 0.3, 0.3)
    cue(G[13]["o"] + 0.1, "whoosh-short_3", -22); cue(w(14, 1) + 0.12, "tock_1", -16)

    # 15  the balance counts down to zero and dissolves; the chart under it falls
    b.scene(G[15]["o"], G[15]["c"])
    vals = ["$10,000", "$8,240", "$6,115", "$3,870", "$1,920", "$640", "$0"]
    t0, t1 = w(15, 2) - 0.25, w(15, 4) + 0.15
    ids15 = []
    for k, s in enumerate(vals):
        col = WHITE if k < 3 else ("#ff9aa3" if k < 6 else RED)
        i = b.text(540, 1110, s, 84, col, 800)
        ids15.append(i)
        ts = G[15]["o"] + 0.1 if k == 0 else t0 + (t1 - t0) * k / (len(vals) - 1)
        te = t0 + (t1 - t0) * (k + 1) / (len(vals) - 1) if k < len(vals) - 1 else None
        tl(f'tl.set("#{i}", {{opacity: 1}}, {ts:.3f});')
        if te: tl(f'tl.set("#{i}", {{opacity: 0}}, {te:.3f});')
    tl(f'tl.to("#{ids15[-1]}", {{opacity: 0, scale: 1.25, filter: "blur(14px)", transformOrigin: "50% 50%", duration: 0.7, ease: "power2.in"}}, {t1 + 0.3:.3f});')
    fc = b.path("M 230 1180 L 320 1210 L 380 1190 L 460 1260 L 540 1240 L 640 1320 L 720 1310 L 860 1380", RED, 4)
    b.draw(fc, t0, t1 - t0 + 0.2, "power1.in")
    for k in range(6): cue(t0 + (t1 - t0) * (k + 1) / 6, "tick-crisp_" + str(k % 3 + 1), -22)

    # 16  forcing a trade for a feeling: an erratic heartbeat line
    b.scene(G[16]["o"], G[16]["c"])
    d = "M 200 1160"
    x = 200
    for k in range(9):
        x += 30; d += f" L {x} 1160"
        hgt = rnd.uniform(90, 210)
        d += f" L {x + 12} {1160 - hgt:.0f} L {x + 26} {1160 + hgt * 0.6:.0f} L {x + 38} 1160"; x += 38
    d += " L 880 1160"
    ecg = b.path(d, "#ff6b78", 4, extra='pathLength="1" style="stroke-dasharray:1 1.2;stroke-dashoffset:1.1;filter:drop-shadow(0 0 8px #ff4d5e)"', drawn=True)
    b.draw(ecg, G[16]["o"], G[16]["c"] - G[16]["o"] - 0.15, "none")

    # 17  the market already told you: a clear downtrend with its trendline
    b.scene(G[17]["o"], G[17]["c"])
    dn = b.path("M 220 1050 L 300 1110 L 360 1080 L 450 1170 L 510 1140 L 600 1240 L 660 1210 L 760 1320 L 860 1300", WHITE, 4)
    b.draw(dn, G[17]["o"], w(17, 4) - G[17]["o"])
    tlp = b.path("M 230 1020 L 860 1260", GOLD, 4, extra='pathLength="1" style="stroke-dasharray:1 1.2;stroke-dashoffset:1.1;filter:drop-shadow(0 0 6px #e8c26a)"', drawn=True)
    b.draw(tlp, w(17, 4), 0.5)
    arr = b.path("M 800 1330 L 870 1370 L 840 1300", GOLD, 5)
    b.draw(arr, w(17, 6) - 0.05, 0.3); cue(w(17, 6), "bell_A4", -22)

    # 18  no applause: the stage lights switch off one by one
    b.scene(G[18]["o"], G[18]["c"])
    lights = []
    for k in range(5):
        x = 300 + k * 120
        lt = b.raw(f'<g id="@ID@" style="opacity:0"><circle cx="{x}" cy="1120" r="34" fill="#fff8e0" style="filter:drop-shadow(0 0 18px #ffe9a8)"/>'
                   f'<path d="M {x - 70} 1350 L {x - 24} 1150 L {x + 24} 1150 L {x + 70} 1350 Z" fill="#fff6d0" opacity="0.08"/></g>')
        lights.append(lt)
        b.fade(lt, G[18]["o"] + k * 0.08, 0.3)
    for k, lt in enumerate(lights):
        tl(f'tl.to("#{lt}", {{opacity: 0.12, duration: 0.12}}, {w(18, 6) - 0.1 + k * 0.14:.3f});')
        cue(w(18, 6) - 0.1 + k * 0.14, "click_" + str(k % 2 + 1), -22)

    # 19  growth: a sprout pushes up
    b.scene(G[19]["o"], G[19]["c"])
    gr = b.path("M 380 1360 H 700", "#ffffff60", 3, drawn=True)
    st = b.path("M 540 1360 C 530 1290 555 1220 540 1110", WHITE, 5)
    b.draw(st, G[19]["o"] + 0.2, w(19, 4) - G[19]["o"])
    lf1 = b.path("M 541 1230 C 490 1200 470 1160 480 1140 C 520 1150 545 1190 541 1230", GOLD, 4, fill="none")
    lf2 = b.path("M 543 1180 C 600 1150 620 1110 610 1090 C 570 1100 545 1140 543 1180", GOLD, 4, fill="none")
    b.draw(lf1, w(19, 5), 0.45); b.draw(lf2, w(19, 6), 0.45)
    bud = b.raw(f'<circle id="@ID@" cx="540" cy="1106" r="10" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 10px {GOLD})"/>', "c")
    b.pop(bud, w(19, 6) + 0.3); cue(w(19, 6) + 0.3, "bell_G5", -24)

    # 20-21  a week of empty days, then a gold tick on every one
    b.scene(G[20]["o"], G[21]["c"])
    for k, dname in enumerate(["MON", "TUE", "WED", "THU", "FRI"]):
        x = 205 + k * 138
        bx = b.path(b.rrect_d(x, 1100, 118, 130, 14), WHITE, 3)
        b.draw(bx, w(20, 2) + k * 0.08, 0.35)
        lb = b.text(x + 59, 1080, dname, 28, "#ffffffb0", 700)
        b.fade(lb, w(20, 2) + k * 0.08, 0.3)
        da = b.path(f"M {x + 39} 1165 H {x + 79}", "#ffffff90", 4)
        b.draw(da, w(20, 4) + k * 0.1, 0.2)
        ck = b.path(f"M {x + 30} 1168 L {x + 52} 1192 L {x + 92} 1138", GOLD, 7)
        b.draw(ck, w(21, 2) + k * 0.12, 0.25)
        cue(w(21, 2) + k * 0.12, "pop_" + str(k % 4 + 1), -20)

    # 22-23  the emblem rises in gold light
    b.scene(G[22]["o"], G[23]["c"])
    rays = ""
    for k in range(16):
        a = k / 16 * math.tau
        rays += f'<line x1="{540 + math.cos(a) * 190:.0f}" y1="{1150 + math.sin(a) * 190:.0f}" x2="{540 + math.cos(a) * 300:.0f}" y2="{1150 + math.sin(a) * 300:.0f}" stroke="{GOLD}" stroke-width="3" stroke-linecap="round" opacity="0.55"/>'
    ry = b.raw(f'<g id="@ID@" style="opacity:0">{rays}</g>')
    b.fade(ry, w(22, 0) + 0.2, 0.6)
    tl(f'tl.fromTo("#{ry}", {{rotation: 0}}, {{rotation: 40, svgOrigin: "540 1150", duration: {G[23]["c"] - G[22]["o"]:.3f}, ease: "none", immediateRender: false}}, {G[22]["o"]:.3f});')
    em = b.raw(f'<image id="@ID@" href="assets/otm_emblem.png" x="390" y="1004" width="300" height="291" style="opacity:0;filter:drop-shadow(0 0 24px rgba(232,194,106,0.6))"/>', "i")
    b.pop(em, w(22, 0), 0.7, 0.6); cue(w(22, 0), "swell_1", -16)
    rg = b.raw(f'<circle id="@ID@" cx="540" cy="1150" r="180" fill="none" stroke="{GOLD}" stroke-width="4" style="opacity:0"/>', "c")
    tl(f'tl.fromTo("#{rg}", {{opacity: 0.9, scale: 0.9, transformOrigin: "50% 50%"}}, {{opacity: 0, scale: 1.5, duration: 0.8, ease: "power2.out", immediateRender: false}}, {w(23, 4):.3f});')
    cue(w(23, 4), "land_1", -18)

    # 24  a follow button gets pressed
    b.scene(G[24]["o"], G[24]["c"] + 0.25)
    fb = b.path(b.rrect_d(340, 1110, 400, 110, 55), WHITE, 4)
    b.draw(fb, G[24]["o"], 0.4)
    ff = b.raw(f'<rect id="@ID@" x="340" y="1110" width="400" height="110" rx="55" fill="{GOLD}" style="opacity:0"/>', "r")
    t1_ = b.text(540, 1180, "+ FOLLOW", 44, WHITE, 800)
    t2_ = b.text(540, 1180, "FOLLOWING ✓", 40, "#111", 800)
    b.fade(t1_, G[24]["o"] + 0.2, 0.25)
    tp = w(24, 1)
    tl(f'tl.set("#{ff}", {{opacity: 1}}, {tp:.3f});'); tl(f'tl.set("#{t1_}", {{opacity: 0}}, {tp:.3f});'); tl(f'tl.set("#{t2_}", {{opacity: 1}}, {tp:.3f});')
    rip = b.raw(f'<circle id="@ID@" cx="600" cy="1170" r="30" fill="none" stroke="#fff" stroke-width="4" style="opacity:0"/>', "c")
    tl(f'tl.fromTo("#{rip}", {{opacity: 1, scale: 0.5, transformOrigin: "50% 50%"}}, {{opacity: 0, scale: 3, duration: 0.5, ease: "power2.out", immediateRender: false}}, {tp:.3f});')
    cue(tp, "click-confirm_1", -14)

    # ambient dust drifting up through the whole film
    dust = ""
    for k in range(42):
        x, y = rnd.uniform(0, 1080), rnd.uniform(0, 1920); r = rnd.uniform(1.2, 3.4); op = rnd.uniform(0.06, 0.26)
        i = b.id("d")
        dust += f'<circle id="{i}" cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#fff" opacity="{op:.2f}"/>'
        tl(f'tl.fromTo("#{i}", {{x: 0, y: 0}}, {{x: {rnd.uniform(-80, 80):.0f}, y: {-rnd.uniform(160, 520):.0f}, duration: {total:.2f}, ease: "none"}}, 0);')

    out = [f'<svg id="dust" viewBox="0 0 1080 1920" width="1080" height="1920">{dust}</svg>',
           '<svg id="ill" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>']
    for g, o, c, items in b.scenes:
        out.append(f'<g id="{g}" style="opacity:0;visibility:hidden" data-layout-allow-overlap>' + "".join(items) + "</g>")
    out.append("</svg>")
    return "\n".join(out)
