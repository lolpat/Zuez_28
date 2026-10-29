"""MSNR series: one vertical explainer per level, drawn as original animated SVG.

Inputs : work/script.json (the narration, one entry per beat), work/vo/epN.json (beat start times + duration,
         written by work/vo.py), assets/audio/vo_epN.wav.
Outputs: epN.html (a standalone composition per episode) and work/cues_epN.json (sound cues for work/mix.py).
"""
import json, math, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1080, 1920
BULL, BEAR = "#2962FF", "#FFFFFF"
DY, CY = 520, 1030           # tops of the diagram panel (1080x500) and the chart panel (1080x380)
SCRIPT = json.load(open(f"{ROOT}/work/script.json"))

def mirror_y(pts, h=520):
    return [(x, h - y) for x, y in pts]

# ---------------------------------------------------------------------------------------------------------------------
# Episode specs. Coordinates are in the diagram panel (1080 x 500, y down). b = beat index (0-3), at = seconds into it.
EP = {}
EP["ep0"] = dict(title="MSNR", sub="Malaysian Support & Resistance", accent="#e8536b", accent2="#ff9aa9", n="",
    els=[dict(k="zone", x0=330, y0=150, x1=750, y1=350, color="#8a8f98", label="ZONE", b=1, at=0.2),
         dict(k="candle", x=500, o=430, c=250, h=210, l=460, b=1, at=0.5),
         dict(k="candle", x=580, o=250, c=440, h=230, l=475, b=1, at=0.75),
         dict(k="fade", target="zone", b=1, at=2.4),
         dict(k="level", x0=330, x1=900, y=250, label="LEVEL", color="#ff6b81", b=1, at=2.5),
         dict(k="marker", x=540, y=250, color="#ff6b81", b=1, at=2.8)],
    grid=["CLASSIC A", "CLASSIC V", "QML", "RBS", "SBR", "OCL", "TRENDLINE", "CE W 50%"])

A_PATH = [(110, 470), (250, 90), (360, 360), (410, 250), (450, 320), (500, 200), (535, 270), (590, 90), (690, 470)]
EP["ep1"] = dict(title="CLASSIC A", sub="A-Level", accent="#f29bb0", accent2="#ffd1dc", n="1/8",
    els=[dict(k="path", pts=A_PATH, color="#ffffff", b=1, at=0.1, dur=2.2, arrow=True),
         dict(k="marker", x=250, y=90, color="#f29bb0", b=1, at=0.75),
         dict(k="level", x0=250, x1=740, y=90, label="A-Level", lx=740, la="end", color="#f29bb0", b=1, at=1.6),
         dict(k="marker", x=590, y=90, color="#f29bb0", b=1, at=2.0),
         dict(k="candle", x=830, o=330, c=120, h=95, l=365, b=2, at=0.2),
         dict(k="candle", x=905, o=120, c=440, h=100, l=470, b=2, at=0.55),
         dict(k="level", x0=770, x1=1050, y=120, label="", color="#f29bb0", b=2, at=1.0),
         dict(k="zone", x0=800, y0=110, x1=935, y1=130, color="#f29bb0", label="", b=2, at=1.2),
         dict(k="text", x=868, y=40, s="close / open · not the wick", color="#bfc4cc", size=30, b=2, at=1.6)],
    chart=dict(wp=[0.15, 0.92, 0.45, 0.66, 0.5, 0.92, 0.2], n=34, b=3, at=0.0,
               levels=[(0.92, "A-Level", "#f29bb0")], marks=[(5, "sell")]))

V_PATH = mirror_y(A_PATH)
EP["ep2"] = dict(title="CLASSIC V", sub="V-Level", accent="#b3b7ff", accent2="#dfe1ff", n="2/8",
    els=[dict(k="path", pts=V_PATH, color="#ffffff", b=1, at=0.1, dur=2.2, arrow=True),
         dict(k="marker", x=250, y=430, color="#b3b7ff", b=1, at=0.75),
         dict(k="level", x0=250, x1=740, y=430, label="V-Level", lx=740, la="end", color="#b3b7ff", b=1, at=1.6),
         dict(k="marker", x=590, y=430, color="#b3b7ff", b=1, at=2.0),
         dict(k="candle", x=830, o=190, c=400, h=155, l=425, b=2, at=0.2),
         dict(k="candle", x=905, o=400, c=80, h=50, l=420, b=2, at=0.55),
         dict(k="level", x0=770, x1=1050, y=400, label="", color="#b3b7ff", b=2, at=1.0),
         dict(k="zone", x0=800, y0=390, x1=935, y1=410, color="#b3b7ff", label="", b=2, at=1.2),
         dict(k="text", x=868, y=20, s="close / open · not the wick", color="#bfc4cc", size=30, b=2, at=1.6)],
    chart=dict(wp=[0.85, 0.08, 0.55, 0.34, 0.5, 0.08, 0.8], n=34, b=3, at=0.0,
               levels=[(0.08, "V-Level", "#b3b7ff")], marks=[(5, "buy")]))

SELL = [(600, 330), (680, 150), (740, 280), (820, 40), (880, 380), (950, 150), (1010, 470)]
BUY = [(x - 540, 500 - y) for x, y in SELL]
EP["ep3"] = dict(title="QM / QML", sub="Quasimodo · Quasimodo Level", accent="#a6e3a1", accent2="#d7f5d3", n="3/8",
    els=[dict(k="divider", x=540, b=0, at=0.8),
         dict(k="text", x=1000, y=40, s="SELL", color="#5ec8e0", size=40, b=1, at=0.0, anchor="end"),
         dict(k="path", pts=SELL, color="#ffffff", b=1, at=0.2, dur=2.6, arrow=True),
         dict(k="level", x0=740, x1=880, y=280, label="MSS", color="#f5d76e", b=1, at=2.4, dashed=True),
         dict(k="marker", x=862, y=280, color="#f5d76e", b=1, at=2.6),
         dict(k="zone", x0=800, y0=40, x1=930, y1=150, color="#5ec8e0", label="QM", b=2, at=0.4),
         dict(k="level", x0=680, x1=1040, y=150, label="QML", color="#5ec8e0", b=2, at=0.2),
         dict(k="marker", x=950, y=150, color="#5ec8e0", b=2, at=1.4),
         dict(k="text", x=80, y=40, s="BUY", color="#ff6b81", size=40, b=3, at=0.0, anchor="start"),
         dict(k="path", pts=BUY, color="#ffffff", b=3, at=0.2, dur=2.4, arrow=True),
         dict(k="level", x0=200, x1=340, y=220, label="MSS", color="#f5d76e", b=3, at=1.4, dashed=True),
         dict(k="zone", x0=260, y0=350, x1=390, y1=460, color="#ff6b81", label="QM", b=3, at=1.9),
         dict(k="level", x0=140, x1=500, y=350, label="QML", color="#ff6b81", b=3, at=1.8),
         dict(k="marker", x=410, y=350, color="#ff6b81", b=3, at=2.4)],
    chart=dict(wp=[0.35, 0.72, 0.52, 0.95, 0.3, 0.72, 0.12], n=36, b=2, at=1.0,
               levels=[(0.72, "QML", "#5ec8e0"), (0.52, "MSS", "#f5d76e")], marks=[(5, "sell")]))

RBS = [(80, 470), (330, 250), (450, 420), (640, 90), (780, 250), (1000, 30)]
EP["ep4"] = dict(title="RBS", sub="Resistance Becomes Support", accent="#5ee0c0", accent2="#b7f7a8", n="4/8",
    els=[dict(k="path", pts=RBS, color="#ffffff", b=1, at=0.1, dur=2.6, arrow=True),
         dict(k="marker", x=330, y=250, color="#ff6b9a", b=1, at=0.6),
         dict(k="text", x=200, y=230, s="resistance", color="#bfc4cc", size=28, b=1, at=0.8),
         dict(k="level", x0=330, x1=1040, y=250, label="RBS", color="#ff6b9a", b=1, at=1.2),
         dict(k="marker", x=780, y=250, color="#5ee0c0", b=2, at=0.2),
         dict(k="text", x=780, y=300, s="now support", color="#5ee0c0", size=30, b=2, at=0.5),
         dict(k="arrow", x=780, y=330, dir="up", color=BULL, b=2, at=1.0)],
    chart=dict(wp=[0.08, 0.4, 0.22, 0.6, 0.4, 0.8, 0.6, 1.0], n=36, b=3, at=0.0,
               levels=[(0.4, "RBS", "#ff6b9a"), (0.6, "RBS", "#ff6b9a")], marks=[(4, "buy"), (6, "buy")]))

SBR = mirror_y(RBS)
EP["ep5"] = dict(title="SBR", sub="Support Becomes Resistance", accent="#f5c451", accent2="#ffe7a3", n="5/8",
    els=[dict(k="path", pts=SBR, color="#ffffff", b=1, at=0.1, dur=2.6, arrow=True),
         dict(k="marker", x=330, y=270, color="#5ec8e0", b=1, at=0.6),
         dict(k="text", x=330, y=320, s="support", color="#bfc4cc", size=28, b=1, at=0.8),
         dict(k="level", x0=330, x1=1040, y=270, label="SBR", color="#5ec8e0", b=1, at=1.2),
         dict(k="marker", x=780, y=270, color="#f5c451", b=2, at=0.2),
         dict(k="text", x=780, y=230, s="now resistance", color="#f5c451", size=30, b=2, at=0.5),
         dict(k="arrow", x=780, y=190, dir="down", color="#ff4d5e", b=2, at=1.0)],
    chart=dict(wp=[0.92, 0.6, 0.78, 0.4, 0.6, 0.2, 0.4, 0.0], n=36, b=3, at=0.0,
               levels=[(0.6, "SBR", "#5ec8e0"), (0.4, "SBR", "#5ec8e0")], marks=[(4, "sell"), (6, "sell")]))

EP["ep6"] = dict(title="OCL", sub="Open Close Level", accent="#a8e063", accent2="#c471ed", n="6/8",
    els=[dict(k="candle", x=230, o=420, c=250, h=225, l=455, b=1, at=0.2),
         dict(k="candle", x=310, o=250, c=70, h=40, l=290, b=1, at=0.6),
         dict(k="level", x0=180, x1=480, y=250, label="OCL", lx=480, la="end", color="#c9a0ff", b=1, at=1.3),
         dict(k="marker", x=270, y=250, color="#c9a0ff", b=1, at=1.6),
         dict(k="divider", x=540, b=2, at=0.0),
         dict(k="candle", x=720, o=70, c=250, h=40, l=275, b=2, at=0.1),
         dict(k="candle", x=800, o=250, c=440, h=225, l=470, b=2, at=0.45),
         dict(k="level", x0=670, x1=980, y=250, label="OCL", lx=980, la="end", color="#c9a0ff", b=2, at=1.0),
         dict(k="marker", x=760, y=250, color="#c9a0ff", b=2, at=1.3)],
    chart=dict(wp=[0.3, 0.12, 0.5, 0.88, 0.62, 0.5, 1.0], n=34, b=3, at=0.0,
               levels=[(0.5, "OCL", "#ff6b9a")], marks=[(5, "buy")]))

TL_FALL = [(60, 120), (120, 300), (190, 160), (250, 340), (320, 200), (380, 470)]
TL_RISE = [(600, 470), (650, 300), (700, 420), (770, 240), (830, 380), (890, 160), (940, 346), (1010, 40)]
EP["ep7"] = dict(title="TRENDLINE", sub="Touch · React · Break", accent="#8e7cff", accent2="#ff6b9a", n="7/8",
    els=[dict(k="path", pts=TL_FALL, color="#ffffff", b=1, at=0.1, dur=2.0, arrow=True),
         dict(k="line", x0=60, y0=120, x1=470, y1=246, color="#ff6b9a", b=1, at=1.0),
         dict(k="divider", x=540, b=1, at=0.6),
         dict(k="path", pts=TL_RISE, color="#ffffff", b=1, at=1.4, dur=2.2, arrow=True),
         dict(k="line", x0=640, y0=438, x1=1040, y1=315, color="#ff6b9a", b=1, at=2.4),
         dict(k="marker", x=60, y=120, color="#ff6b9a", b=2, at=0.0),
         dict(k="marker", x=190, y=160, color="#ff6b9a", b=2, at=0.25),
         dict(k="marker", x=320, y=200, color="#ff6b9a", b=2, at=0.6, big=True),
         dict(k="marker", x=700, y=420, color="#ff6b9a", b=2, at=1.6),
         dict(k="marker", x=830, y=380, color="#ff6b9a", b=2, at=1.85),
         dict(k="marker", x=940, y=346, color="#ff6b9a", b=2, at=2.2, big=True)],
    chart=dict(wp=[0.1, 0.35, 0.2, 0.55, 0.32, 0.72, 0.44, 0.85, 0.12], n=40, b=3, at=0.0,
               levels=[], trend=[2, 4, 6], marks=[(8, "sell")]))

EP["ep8"] = dict(title="CE W 50%", sub="Consequent Encroachment of Wick", accent="#d6336c", accent2="#ff8fb5", n="8/8",
    els=[dict(k="candle", x=170, o=180, c=330, h=160, l=350, b=1, at=0.1),
         dict(k="candle", x=240, o=250, c=340, h=235, l=470, b=1, at=0.5),
         dict(k="level", x0=140, x1=500, y=350, label="Sweep", lx=500, la="end", color="#ffffff", b=1, at=1.1),
         dict(k="marker", x=240, y=470, color="#d6336c", b=1, at=1.5),
         dict(k="candle", x=310, o=330, c=110, h=90, l=345, b=2, at=0.0),
         dict(k="level", x0=210, x1=500, y=405, label="Wick 50%", lx=500, la="end", color="#d6336c", b=2, at=0.5),
         dict(k="marker", x=240, y=405, color="#d6336c", b=2, at=0.8),
         dict(k="divider", x=540, b=3, at=0.0),
         dict(k="text", x=810, y=36, s="HTF · 1H / 4H", color="#d6336c", size=34, b=3, at=0.2),
         dict(k="candle", x=710, o=340, c=190, h=360, l=170, b=3, at=0.4),
         dict(k="candle", x=780, o=270, c=180, h=285, l=50, b=3, at=0.7),
         dict(k="candle", x=850, o=190, c=410, h=175, l=430, b=3, at=1.0),
         dict(k="level", x0=680, x1=1040, y=170, label="Sweep", lx=1040, la="end", color="#ffffff", b=3, at=1.3),
         dict(k="level", x0=750, x1=1040, y=115, label="Wick 50%", lx=1040, la="end", color="#d6336c", b=3, at=1.6)],
    chart=dict(wp=[0.85, 0.55, 0.62, 0.35, 0.42, 0.18, 0.7, 1.0], n=36, b=2, at=1.0,
               levels=[], wick=5, marks=[(5, "buy")]))

# ---------------------------------------------------------------------------------------------------------------------
def build_ohlc(wp, n, seed):
    rnd = random.Random(seed)
    seg = (n - 1) / (len(wp) - 1)
    closes = []
    for i in range(n):
        f = i / seg; k = min(int(f), len(wp) - 2); u = f - k
        v = wp[k] + (wp[k + 1] - wp[k]) * (u * u * (3 - 2 * u))
        closes.append(v + (rnd.uniform(-0.025, 0.025) if 0 < i < n - 1 else 0))
    for k, v in enumerate(wp):        # land the waypoints exactly
        closes[min(n - 1, round(k * seg))] = v
    out, prev = [], closes[0] - 0.02
    for c in closes:
        o = prev
        hi = max(o, c) + rnd.uniform(0.005, 0.03); lo = min(o, c) - rnd.uniform(0.005, 0.03)
        out.append([o, hi, lo, c]); prev = c
    return out, seg

def chart_svg(ep, spec, beat_t):
    ohlc, seg = build_ohlc(spec["wp"], spec["n"], hash(ep) % 997)
    if spec.get("wick") is not None:
        i = round(spec["wick"] * seg)
        o, hi, lo, c = ohlc[i]
        ohlc[i] = [o, hi, min(lo, c) - 0.16, max(c, o) + 0.02]
        ohlc[i][3] = max(ohlc[i][3], ohlc[i][0] + 0.03)
    vals = [v for r in ohlc for v in r[1:3]]
    vmin, vmax = min(vals) - 0.04, max(vals) + 0.04
    X0, X1, Y0, Y1 = 90, 900, 70, 310
    def X(i): return X0 + (X1 - X0) * (i + 0.5) / spec["n"]
    def Y(v): return Y1 - (Y1 - Y0) * (v - vmin) / (vmax - vmin)
    cw = (X1 - X0) / spec["n"] * 0.62
    t0 = beat_t + spec["at"]
    parts, tl = [], []
    for i, (o, hi, lo, c) in enumerate(ohlc):
        col = BULL if c >= o else BEAR
        top, bot = Y(max(o, c)), Y(min(o, c))
        parts.append(f'<g class="{ep}-cc" style="transform-box:fill-box;transform-origin:50% 100%">'
                     f'<line x1="{X(i):.1f}" y1="{Y(hi):.1f}" x2="{X(i):.1f}" y2="{Y(lo):.1f}" stroke="{col}" stroke-width="2.5"/>'
                     f'<rect x="{X(i) - cw / 2:.1f}" y="{top:.1f}" width="{cw:.1f}" height="{max(2, bot - top):.1f}" fill="{col}"/></g>')
    build = min(2.2, 0.05 * spec["n"])
    tl.append(f'tl.fromTo(".{ep}-cc", {{opacity: 0, scaleY: 0.2}}, {{opacity: 1, scaleY: 1, duration: 0.22, ease: "power2.out", stagger: {build / spec["n"]:.3f}}}, {t0:.2f});')
    cues = [dict(t=t0, snd="swish", gain=-16)]
    tend = t0 + build
    for j, (v, label, col) in enumerate(spec.get("levels", [])):
        lid = f"{ep}-cl{j}"
        parts.append(f'<line id="{lid}" x1="{X0}" y1="{Y(v):.1f}" x2="{X1 + 40}" y2="{Y(v):.1f}" stroke="{col}" stroke-width="3" stroke-dasharray="{X1 + 40 - X0}" stroke-dashoffset="{X1 + 40 - X0}"/>')
        parts.append(f'<text id="{lid}t" x="{X1 + 44}" y="{Y(v) + 9:.1f}" fill="{col}" font-size="28" font-family="Montserrat" font-weight="700" opacity="0">{label}</text>')
        tl.append(f'tl.fromTo("#{lid}", {{strokeDashoffset: {X1 + 40 - X0}}}, {{strokeDashoffset: 0, duration: 0.5, ease: "power2.inOut"}}, {tend + 0.1 + j * 0.25:.2f});')
        tl.append(f'tl.fromTo("#{lid}t", {{opacity: 0, x: -14}}, {{opacity: 1, x: 0, duration: 0.3, ease: "expo.out"}}, {tend + 0.45 + j * 0.25:.2f});')
        cues.append(dict(t=tend + 0.1 + j * 0.25, snd="tick", gain=-18))
    if spec.get("trend"):
        idx = [round(k * seg) for k in spec["trend"]]
        ys = [Y(ohlc[i][2]) for i in idx]; xs = [X(i) for i in idx]
        m = (ys[1] - ys[0]) / (xs[1] - xs[0])
        xa, xb = X0, X1 + 20
        LT = math.hypot(xb - xa, m * (xb - xa)) + 2
        parts.append(f'<line id="{ep}-ctl" x1="{xa}" y1="{ys[0] + m * (xa - xs[0]):.1f}" x2="{xb}" y2="{ys[0] + m * (xb - xs[0]):.1f}" stroke="#ff6b9a" stroke-width="3" stroke-dasharray="{LT:.1f}" stroke-dashoffset="{LT:.1f}"/>')
        tl.append(f'tl.fromTo("#{ep}-ctl", {{strokeDashoffset: {LT:.1f}}}, {{strokeDashoffset: 0, duration: 0.6, ease: "power2.inOut"}}, {tend + 0.1:.2f});')
        for q, (x, y) in enumerate(zip(xs, ys)):
            parts.append(f'<circle id="{ep}-ctm{q}" cx="{x:.1f}" cy="{ys[0] + m * (x - xs[0]):.1f}" r="13" fill="#ff6b9a" opacity="0"/>')
            tl.append(f'tl.fromTo("#{ep}-ctm{q}", {{opacity: 0, scale: 2.4, transformOrigin: "50% 50%"}}, {{opacity: 0.85, scale: 1, duration: 0.3, ease: "back.out(2)"}}, {tend + 0.5 + q * 0.2:.2f});')
            cues.append(dict(t=tend + 0.5 + q * 0.2, snd="ping", gain=-20))
    for j, (k, side) in enumerate(spec.get("marks", [])):
        i = round(k * seg)
        x = X(i)
        if side == "sell":
            y = Y(ohlc[i][1]) - 26; col = "#ff4d5e"; pts = f"{x - 22},{y - 40} {x + 22},{y - 40} {x},{y}"
        else:
            y = Y(ohlc[i][2]) + 26; col = BULL; pts = f"{x - 22},{y + 40} {x + 22},{y + 40} {x},{y}"
        lab = "SELL" if side == "sell" else "BUY"
        ly = y - 10 if side == "sell" else y + 34
        parts.append(f'<g id="{ep}-cm{j}" opacity="0"><polygon points="{pts}" fill="{col}"/>'
                     f'<text x="{x + 30:.1f}" y="{ly:.1f}" text-anchor="start" fill="{col}" font-size="30" font-family="Montserrat" font-weight="800">{lab}</text></g>')
        tl.append(f'tl.fromTo("#{ep}-cm{j}", {{opacity: 0, y: {-30 if side == "sell" else 30}}}, {{opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)"}}, {tend + 0.8 + j * 0.3:.2f});')
        cues.append(dict(t=tend + 0.8 + j * 0.3, snd="stamp", gain=-12))
    return "\n".join(parts), tl, cues

def el_markup(ep, i, e, bt, accent):
    """markup, timeline lines, cues for one diagram element"""
    t = bt[e["b"]] + e["at"]
    eid = f"{ep}-e{i}"
    M, T, C = [], [], []
    k = e["k"]
    if k == "path":
        pts = " ".join(f"{x},{y}" for x, y in e["pts"])
        L = sum(math.hypot(x2 - x1, y2 - y1) for (x1, y1), (x2, y2) in zip(e["pts"], e["pts"][1:])) + 2
        M.append(f'<polyline id="{eid}" points="{pts}" fill="none" stroke="{e["color"]}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round" stroke-dasharray="{L:.1f}" stroke-dashoffset="{L:.1f}" opacity="0"/>')
        T.append(f'tl.fromTo("#{eid}", {{opacity: 0, strokeDashoffset: {L:.1f}}}, {{opacity: 1, strokeDashoffset: 0, duration: {e["dur"]}, ease: "power1.inOut"}}, {t:.2f});')
        C.append(dict(t=t, snd="swish", gain=-15))
        if e.get("arrow"):
            (x1, y1), (x2, y2) = e["pts"][-2], e["pts"][-1]
            a = math.degrees(math.atan2(y2 - y1, x2 - x1))
            M.append(f'<polygon id="{eid}a" points="0,-14 26,0 0,14" fill="{e["color"]}" opacity="0" transform="translate({x2},{y2}) rotate({a:.1f})"/>')
            T.append(f'tl.fromTo("#{eid}a", {{opacity: 0}}, {{opacity: 1, duration: 0.12}}, {t + e["dur"] - 0.05:.2f});')
    elif k == "level":
        L = abs(e["x1"] - e["x0"]) + 2
        M.append(f'<line id="{eid}" x1="{e["x0"]}" y1="{e["y"]}" x2="{e["x1"]}" y2="{e["y"]}" stroke="{e["color"]}" stroke-width="{3 if e.get("dashed") else 4}" stroke-dasharray="{L}" stroke-dashoffset="{L}"/>')
        T.append(f'tl.fromTo("#{eid}", {{strokeDashoffset: {L}}}, {{strokeDashoffset: 0, duration: 0.55, ease: "power2.inOut"}}, {t:.2f});')
        T.append(f'tl.fromTo("#{eid}", {{opacity: 1}}, {{opacity: 0.35, duration: 0.08, repeat: 3, yoyo: true, ease: "none", immediateRender: false}}, {t + 0.6:.2f});')
        if e["label"]:
            M.append(f'<text id="{eid}t" x="{e.get("lx", e["x0"] + 10)}" y="{e["y"] - 14}" text-anchor="{e.get("la", "start")}" fill="{e["color"]}" font-size="34" font-family="Montserrat" font-weight="800" opacity="0">{e["label"]}</text>')
            T.append(f'tl.fromTo("#{eid}t", {{opacity: 0, y: 12}}, {{opacity: 1, y: 0, duration: 0.3, ease: "expo.out"}}, {t + 0.4:.2f});')
        C.append(dict(t=t, snd="tick", gain=-16))
    elif k == "line":
        L = math.hypot(e["x1"] - e["x0"], e["y1"] - e["y0"]) + 2
        M.append(f'<line id="{eid}" x1="{e["x0"]}" y1="{e["y0"]}" x2="{e["x1"]}" y2="{e["y1"]}" stroke="{e["color"]}" stroke-width="4" stroke-dasharray="{L:.1f}" stroke-dashoffset="{L:.1f}"/>')
        T.append(f'tl.fromTo("#{eid}", {{strokeDashoffset: {L:.1f}}}, {{strokeDashoffset: 0, duration: 0.7, ease: "power2.inOut"}}, {t:.2f});')
        C.append(dict(t=t, snd="tick", gain=-16))
    elif k == "zone":
        M.append(f'<g id="{eid}" opacity="0" style="transform-box:fill-box;transform-origin:50% 50%"><rect x="{e["x0"]}" y="{e["y0"]}" width="{e["x1"] - e["x0"]}" height="{e["y1"] - e["y0"]}" fill="{e["color"]}" fill-opacity="0.32" stroke="{e["color"]}" stroke-width="2"/>'
                 + (f'<text x="{(e["x0"] + e["x1"]) / 2}" y="{(e["y0"] + e["y1"]) / 2 + 12}" text-anchor="middle" fill="#ffffff" font-size="36" font-family="Montserrat" font-weight="800">{e["label"]}</text>' if e["label"] else "")
                 + "</g>")
        T.append(f'tl.fromTo("#{eid}", {{opacity: 0, scaleX: 0.3}}, {{opacity: 1, scaleX: 1, duration: 0.4, ease: "expo.out"}}, {t:.2f});')
        C.append(dict(t=t, snd="pop", gain=-15))
    elif k == "fade":
        tgt = next(j for j, x in enumerate(EP[ep]["els"]) if x["k"] == e["target"])
        T.append(f'tl.to("#{ep}-e{tgt}", {{opacity: 0.12, duration: 0.4, ease: "power2.out"}}, {t:.2f});')
    elif k == "candle":
        col = BULL if e["c"] < e["o"] else BEAR
        top, bot = min(e["o"], e["c"]), max(e["o"], e["c"])
        M.append(f'<g id="{eid}" opacity="0" style="transform-box:fill-box;transform-origin:50% 100%">'
                 f'<line x1="{e["x"]}" y1="{e["h"]}" x2="{e["x"]}" y2="{e["l"]}" stroke="{col}" stroke-width="4"/>'
                 f'<rect x="{e["x"] - 30}" y="{top}" width="60" height="{bot - top}" fill="{col}"/></g>')
        T.append(f'tl.fromTo("#{eid}", {{opacity: 0, scaleY: 0.1}}, {{opacity: 1, scaleY: 1, duration: 0.42, ease: "expo.out"}}, {t:.2f});')
        C.append(dict(t=t, snd="pop", gain=-14))
    elif k == "marker":
        r = 22 if e.get("big") else 15
        M.append(f'<circle id="{eid}" cx="{e["x"]}" cy="{e["y"]}" r="{r}" fill="{e["color"]}" opacity="0"/>')
        M.append(f'<circle id="{eid}r" cx="{e["x"]}" cy="{e["y"]}" r="{r}" fill="none" stroke="{e["color"]}" stroke-width="4" opacity="0"/>')
        T.append(f'tl.fromTo("#{eid}", {{opacity: 0, scale: 2.5, transformOrigin: "50% 50%"}}, {{opacity: 0.9, scale: 1, duration: 0.3, ease: "back.out(2.2)"}}, {t:.2f});')
        T.append(f'tl.fromTo("#{eid}r", {{opacity: 1, scale: 1, transformOrigin: "50% 50%"}}, {{opacity: 0, scale: 3.4, duration: 0.6, ease: "power2.out", immediateRender: false}}, {t + 0.1:.2f});')
        C.append(dict(t=t, snd="ping", gain=-17))
    elif k == "text":
        anchor = e.get("anchor", "middle")
        M.append(f'<text id="{eid}" x="{e["x"]}" y="{e["y"]}" text-anchor="{anchor}" fill="{e["color"]}" font-size="{e["size"]}" font-family="Montserrat" font-weight="800" opacity="0">{e["s"]}</text>')
        T.append(f'tl.fromTo("#{eid}", {{opacity: 0, y: 14}}, {{opacity: 1, y: 0, duration: 0.3, ease: "expo.out"}}, {t:.2f});')
    elif k == "divider":
        M.append(f'<line id="{eid}" x1="{e["x"]}" y1="10" x2="{e["x"]}" y2="490" stroke="#8a8f98" stroke-width="3" stroke-dasharray="10 12" opacity="0"/>')
        T.append(f'tl.fromTo("#{eid}", {{opacity: 0}}, {{opacity: 0.8, duration: 0.4}}, {t:.2f});')
    elif k == "arrow":
        x, y = e["x"], e["y"]
        pts = f"{x - 30},{y + 50} {x + 30},{y + 50} {x},{y}" if e["dir"] == "up" else f"{x - 30},{y - 50} {x + 30},{y - 50} {x},{y}"
        M.append(f'<polygon id="{eid}" points="{pts}" fill="{e["color"]}" opacity="0"/>')
        T.append(f'tl.fromTo("#{eid}", {{opacity: 0, y: {40 if e["dir"] == "up" else -40}}}, {{opacity: 1, y: 0, duration: 0.4, ease: "back.out(2)"}}, {t:.2f});')
        C.append(dict(t=t, snd="stamp", gain=-12))
    return M, T, C

OUTRO = [0.0, 1.32, 3.34, 4.09]

def captions(ep, beats, bt, bend):
    """caption chunks of up to 5 words, timed by characters inside each beat's speech window"""
    M, T = [], []
    n = 0
    for b, text in enumerate(beats):
        words = text.split()
        chunks, cur = [], []
        for w in words:
            cur.append(w)
            if len(cur) >= 8 or w[-1] in ".:?" and len(cur) >= 3:
                chunks.append(" ".join(cur)); cur = []
        if cur:
            if chunks and len(cur) <= 3: chunks[-1] += " " + " ".join(cur)
            else: chunks.append(" ".join(cur))
        t0, t1 = bt[b], bend[b]
        total = sum(len(c) for c in chunks)
        acc = 0
        for c in chunks:
            s = t0 + (t1 - t0) * acc / total; acc += len(c); e = t0 + (t1 - t0) * acc / total
            cid = f"{ep}-cap{n}"; n += 1
            M.append(f'<div id="{cid}" class="cap" data-layout-allow-overlap>{c}</div>')
            T.append(f'tl.fromTo("#{cid}", {{opacity: 0, scale: 0.92}}, {{opacity: 1, scale: 1, duration: 0.12, ease: "power2.out"}}, {s:.2f});')
            T.append(f'tl.to("#{cid}", {{opacity: 0, duration: 0.08, ease: "none"}}, {max(s + 0.2, e - 0.04):.2f});')
    return M, T

def build(ep):
    spec = EP[ep]
    vo = json.load(open(f"{ROOT}/work/vo/{ep}.json"))
    lead = 0.35
    bt = [lead + s for s in vo["starts"]]
    bend = [lead + e for e in vo["ends"]]
    vo_end = lead + vo["dur"]
    end_t = round(vo_end + 0.7, 2)          # end card start
    vo_o = round(end_t + 0.3, 2)            # outro line: "Order the Market. Don't let the market order you. Follow for more."
    total = round(vo_o + OUTRO[3] + 1.3, 2)
    accent, accent2 = spec["accent"], spec["accent2"]
    M, T, C = [], [], []
    for i, e in enumerate(spec.get("els", [])):
        m, t, c = el_markup(ep, i, e, bt, accent); M += m; T += t; C += c
    chart_m, chart_t = "", []
    if spec.get("chart"):
        chart_m, chart_t, cc = chart_svg(ep, spec["chart"], bt[spec["chart"]["b"]]); C += cc
    grid_m, grid_t = "", []
    if spec.get("grid"):
        cols = ["#f29bb0", "#b3b7ff", "#a6e3a1", "#5ee0c0", "#f5c451", "#c9a0ff", "#8e7cff", "#d6336c"]
        items = []
        t0 = bt[2]; span = max(1.5, bend[2] - bt[2] - 0.6)
        for j, name in enumerate(spec["grid"]):
            x = 90 + (j % 2) * 460; y = 30 + (j // 2) * 88
            gid = f"{ep}-g{j}"
            items.append(f'<g id="{gid}" opacity="0" style="transform-box:fill-box;transform-origin:50% 50%"><rect x="{x}" y="{y}" width="430" height="72" rx="36" fill="none" stroke="{cols[j]}" stroke-width="3"/>'
                         f'<text x="{x + 215}" y="{y + 48}" text-anchor="middle" fill="{cols[j]}" font-size="36" font-family="Montserrat" font-weight="800">{name}</text></g>')
            tt = t0 + span * j / 8
            grid_t.append(f'tl.fromTo("#{gid}", {{opacity: 0, scale: 0.4}}, {{opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)"}}, {tt:.2f});')
            C.append(dict(t=tt, snd="pop", gain=-15))
            grid_t.append(f'tl.fromTo("#{gid}", {{scale: 1}}, {{scale: 1.12, duration: 0.12, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false}}, {bt[3] + 0.15 * j:.2f});')
        grid_m = "\n".join(items)
    capM, capT = captions(ep, SCRIPT[ep], bt, bend)
    C.append(dict(t=0.12, snd="hit", gain=-7))
    C.append(dict(t=end_t, snd="whoosh", gain=-10, align="peak"))
    C.append(dict(t=end_t + 0.25, snd="impact", gain=-8))
    C.append(dict(t=end_t + 0.6, snd="sting", gain=-12))
    C.append(dict(t=lead, snd="vo", file=f"vo_{ep}", gain=0))
    C.append(dict(t=vo_o, snd="vo", file="vo_outro", gain=0))
    C.append(dict(t=vo_o + OUTRO[1], snd="pop", gain=-14))
    C.append(dict(t=vo_o + OUTRO[2], snd="stamp", gain=-12))
    title_size = 168 if len(spec["title"]) <= 5 else (128 if len(spec["title"]) <= 9 else 112)
    series = f"MSNR SERIES · {spec['n']}" if spec["n"] else "MSNR SERIES · OVERVIEW"
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: {W}px; height: {H}px; overflow: hidden; background: #000;
        font-family: "Montserrat", sans-serif; }}
      #{ep}-grid {{ position: absolute; inset: 0; opacity: 0.55;
        background-image: linear-gradient(rgba(255,255,255,0.045) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.045) 1px, transparent 1px);
        background-size: 60px 60px; }}
      #{ep}-cam {{ position: absolute; inset: 0; transform-origin: 540px 900px; }}
      #{ep}-shake {{ position: absolute; inset: 0; }}
      #{ep}-logo {{ position: absolute; left: 395px; top: 60px; width: 290px; }}
      #{ep}-series {{ position: absolute; left: 0; width: {W}px; top: 210px; text-align: center; font-size: 30px; font-weight: 700;
        letter-spacing: 0.32em; color: #8a8f98; }}
      #{ep}-title, #{ep}-shine {{ position: absolute; left: 0; width: {W}px; top: 252px; text-align: center;
        font-family: "Playfair Display", serif; font-weight: 700; font-size: {title_size}px; line-height: 1; color: #fff; letter-spacing: 0.02em; }}
      #{ep}-shine {{ color: transparent; background: linear-gradient(100deg, transparent 35%, rgba(255,255,255,0.0) 40%, {accent2} 50%, rgba(255,255,255,0) 60%, transparent 65%);
        background-size: 300% 100%; -webkit-background-clip: text; background-clip: text; }}
      #{ep}-sub {{ position: absolute; left: 0; width: {W}px; top: 440px; text-align: center; font-family: "Playfair Display", serif;
        font-weight: 700; font-size: 50px; background: linear-gradient(90deg, {accent}, {accent2}); -webkit-background-clip: text; background-clip: text; color: transparent; }}
      #{ep}-diag {{ position: absolute; left: 0; top: {DY}px; width: {W}px; height: 500px; overflow: visible; }}
      #{ep}-chart {{ position: absolute; left: 0; top: {CY}px; width: {W}px; height: 380px; overflow: visible; }}
      .cap {{ position: absolute; left: 60px; width: 960px; top: 1428px; text-align: center; font-size: 50px; font-weight: 800; color: #fff;
        line-height: 1.15; opacity: 0; text-shadow: 0 3px 0 #000, 0 0 14px rgba(0,0,0,0.9); }}
      #{ep}-flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 50; }}
      #{ep}-end {{ position: absolute; inset: 0; background: #000; opacity: 0; z-index: 40; }}
      #{ep}-end-logo {{ position: absolute; left: 110px; top: 470px; width: 860px; }}
      #{ep}-end-cta {{ position: absolute; left: 0; width: {W}px; top: 1040px; text-align: center; font-family: "Archivo Black", sans-serif;
        font-size: 92px; color: #fff; }}
      #{ep}-end-cta span {{ color: {BULL}; }}
      #{ep}-end-note {{ position: absolute; left: 0; width: {W}px; top: 1180px; text-align: center; font-size: 28px; font-weight: 700;
        letter-spacing: 0.12em; color: #8a8f98; }}
      #{ep}-end-tag {{ position: absolute; left: 0; width: {W}px; top: 920px; text-align: center; font-size: 44px; font-weight: 800;
        letter-spacing: 0.04em; color: #fff; }}
      #{ep}-end-tag span {{ color: #e8c26a; }}
      #{ep}-end-foot {{ position: absolute; left: 0; top: 1665px; width: {W}px; height: 255px; overflow: hidden; }}
      #{ep}-end-foot img {{ width: {W}px; height: 255px; display: block; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="{ep}" data-start="0" data-duration="{total}" data-width="{W}" data-height="{H}" data-motion-blur="on">
      <div id="{ep}-grid"></div>
      <div id="{ep}-cam"><div id="{ep}-shake">
        <img id="{ep}-logo" src="assets/otm_logo.png" alt="Order the Market" />
        <div id="{ep}-series">{series}</div>
        <div id="{ep}-title" data-layout-allow-occlusion>{spec["title"]}</div>
        <div id="{ep}-shine" data-layout-allow-overlap data-layout-allow-occlusion>{spec["title"]}</div>
        <div id="{ep}-sub">{spec["sub"]}</div>
        <svg id="{ep}-diag" viewBox="0 0 {W} 500">
{chr(10).join("          " + m for m in M)}
        </svg>
        <svg id="{ep}-chart" viewBox="0 0 {W} 380">
{chart_m}
{grid_m}
        </svg>
{chr(10).join("        " + m for m in capM)}
      </div></div>
      <div id="{ep}-end">
        <img id="{ep}-end-logo" src="assets/otm_logo.png" alt="Order the Market" />
        <div id="{ep}-end-tag">DON'T LET THE MARKET <span>ORDER YOU</span></div>
        <div id="{ep}-end-cta">FOLLOW FOR <span>MORE</span></div>
        <div id="{ep}-end-note">EDUCATIONAL ONLY · NOT FINANCIAL ADVICE</div>
        <div id="{ep}-end-foot"><img id="{ep}-end-foot-img" src="assets/footer.jpg" alt="" /></div>
      </div>
      <div id="{ep}-flash"></div>
      <audio id="{ep}-audio" class="clip" src="assets/audio/mix_{ep}.wav" data-start="0" data-duration="{total}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
        const SX = [0.9, -0.75, 0.6, -0.8, 0.5, -0.45, 0.3, -0.2], SY = [-0.5, 0.8, -0.6, 0.45, -0.7, 0.3, -0.25, 0.12];
        function shake(t, amp) {{
          SX.forEach((v, i) => tl.to("#{ep}-shake", {{ x: amp * v * (1 - i / 8), y: amp * SY[i] * (1 - i / 8), duration: 0.035, ease: "none" }}, t + i * 0.035));
          tl.to("#{ep}-shake", {{ x: 0, y: 0, duration: 0.05 }}, t + 0.28);
        }}
                tl.fromTo("#{ep}-cam", {{ scale: 1.12 }}, {{ scale: 1, duration: 0.6, ease: "expo.out" }}, 0);
        tl.fromTo("#{ep}-logo", {{ opacity: 0.6, y: -20 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }}, 0);
        tl.fromTo("#{ep}-series", {{ opacity: 0, scaleX: 1.4, filter: "blur(6px)" }}, {{ opacity: 1, scaleX: 1, filter: "blur(0px)", duration: 0.6, ease: "expo.out" }}, 0.2);
        tl.fromTo("#{ep}-title", {{ opacity: 1, scale: 1.45, filter: "blur(3px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.36, ease: "expo.out" }}, 0);
        tl.fromTo("#{ep}-flash", {{ opacity: 0.55 }}, {{ opacity: 0, duration: 0.2, ease: "power2.out", immediateRender: false }}, 0.12);
        shake(0.2, 20);
        tl.fromTo("#{ep}-shine", {{ backgroundPosition: "100% 0%" }}, {{ backgroundPosition: "0% 0%", duration: 0.9, ease: "power2.inOut" }}, 0.55);
        tl.fromTo("#{ep}-sub", {{ opacity: 0, clipPath: "inset(0% 100% 0% 0%)" }}, {{ opacity: 1, clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "power3.out" }}, 0.45);
{chr(10).join("        " + t for t in T)}
{chr(10).join("        " + t for t in chart_t)}
{chr(10).join("        " + t for t in grid_t)}
{chr(10).join("        " + t for t in capT)}
        tl.to("#{ep}-cam", {{ scale: 1.6, filter: "blur(12px)", duration: 0.4, ease: "power3.in" }}, {end_t - 0.4:.2f});
        tl.fromTo("#{ep}-flash", {{ opacity: 0.9 }}, {{ opacity: 0, duration: 0.3, ease: "power2.out", immediateRender: false }}, {end_t:.2f});
        tl.fromTo("#{ep}-end", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.05, immediateRender: false }}, {end_t:.2f});
        tl.to("#{ep}-cam", {{ opacity: 0, duration: 0.05, ease: "none" }}, {end_t + 0.05:.2f});
        tl.fromTo("#{ep}-end-logo", {{ opacity: 0, scale: 2.2, filter: "blur(14px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.5, ease: "expo.out" }}, {end_t + 0.1:.2f});
        tl.fromTo("#{ep}-end-cta", {{ opacity: 0, clipPath: "inset(0% 100% 0% 0%)" }}, {{ opacity: 1, clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power3.out" }}, {vo_o + OUTRO[2]:.2f});
        tl.fromTo("#{ep}-end-tag", {{ opacity: 0, y: 30, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.4, ease: "expo.out" }}, {vo_o + OUTRO[1]:.2f});
        tl.fromTo("#{ep}-end-note", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {end_t + 1.0:.2f});
        tl.fromTo("#{ep}-end-foot-img", {{ y: 255 }}, {{ y: 0, duration: 0.5, ease: "back.out(1.2)" }}, {end_t + 0.9:.2f});
        window.__timelines["{ep}"] = tl;
      }})();
    </script>
  </body>
</html>
"""
    d = f"{ROOT}/eps/{ep}"; os.makedirs(d, exist_ok=True)
    open(f"{d}/index.html", "w").write(html)
    if not os.path.exists(f"{d}/assets"): os.symlink("../../assets", f"{d}/assets")
    for f in ("hyperframes.json", "package.json"):
        if os.path.exists(f"{ROOT}/{f}") and not os.path.exists(f"{d}/{f}"): os.symlink(f"../../{f}", f"{d}/{f}")
    json.dump(dict(total=total, cues=sorted(C, key=lambda c: c["t"])), open(f"{ROOT}/work/cues_{ep}.json", "w"), indent=1)
    return total

if __name__ == "__main__":
    import sys
    eps = sys.argv[1:] or [e for e in EP if os.path.exists(f"{ROOT}/work/vo/{e}.json")]
    for e in eps:
        print(e, build(e), "s")
