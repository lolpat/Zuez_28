"""Shared scene engine for the OTM CRT series (otm-crt-ep1..5, English, and otm-crt-ep1-th..5-th, Thai).
Same glowing OTM scene system as otm-break / otm-orderblock, plus: a candle chart that can hold any candles, Thai text in
Kanit, and timing marks. The script (work/script.txt) carries [key] marks; work/align.py turns the voice into
work/words.json (one entry per script token) and work/marks.json (key -> token index), and K(key) is the time the voice
reaches that mark. Candle colours: up #2962ff, down white."""
import json, math, os, random, re

GOLD, RED, WHITE, GREY, LBL = "#e8c26a", "#ff4d5e", "#ffffff", "#7d838c", "#c9ced6"
UP, DOWN, LBLUE, GREEN = "#2962ff", "#ffffff", "#7d9bff", "#3ddc97"
LEAD = 0.3
GY = 1240
CAP_Y = 1352

T, CUES = [], []
G = dict()                                       # ROOT, LANG, COMP, MIX, words, marks, END_T, TOTAL
rnd = random.Random(7)


def init(root, lang, comp, mix):
    G.update(ROOT=root, LANG=lang, COMP=comp, MIX=mix)
    G["words"] = json.load(open(f"{root}/work/words.json"))
    G["marks"] = json.load(open(f"{root}/work/marks.json"))
    G["END_T"] = round(G["words"][-1]["end"] + LEAD + 0.6, 2)
    G["TOTAL"] = round(G["END_T"] + 1.0, 2)          # no end card: the outro holds, then fades out
    return G["TOTAL"]

def TH(): return G["LANG"] == "th"
def L(en, th): return th if TH() else en
def W(i): return round(G["words"][i]["start"] + LEAD, 3)
def WE(i): return round(G["words"][i]["end"] + LEAD, 3)
def K(key, off=0.0): return round(W(G["marks"][key]) + off, 3)
def KE(key, n=0):
    """end of the n-th token after the mark"""
    return WE(G["marks"][key] + n)
def tl(s): T.append(s)
def cue(t, snd, gain): CUES.append(dict(t=round(t, 3), snd=snd, gain=gain))


_COMB = set(range(0x0E31, 0x0E32)) | set(range(0x0E34, 0x0E3B)) | set(range(0x0E47, 0x0E4F))
def tw(text, size, sp=0.06):
    """rough rendered width of a text run"""
    w = 0.0
    for ch in text:
        o = ord(ch)
        if o in _COMB: continue
        if 0x0E00 <= o <= 0x0E7F: w += 0.60
        elif ch.isupper() or ch.isdigit(): w += 0.72 + sp
        elif ch == " ": w += 0.32 + sp
        else: w += 0.55 + sp
    return w * size


class S:
    """Builds one scene's SVG and its tweens."""
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
        tl(f'tl.fromTo("#{self.id}", {{scale: 1}}, {{scale: 1.03, transformOrigin: "50% 55%", duration: {c - o:.3f}, ease: "none", immediateRender: false}}, {o:.3f});')
        tl(f'tl.to("#{self.id}", {{opacity: 0, duration: 0.25, ease: "power2.in"}}, {c - 0.25:.3f});')
        tl(f'tl.set("#{self.id}", {{opacity: 0, visibility: "hidden"}}, {c:.3f});')

    def uid(self, p):
        S.n += 1
        return f"{p}{S.n}"

    def add(self, s, p="e"):
        i = self.uid(p)
        self.items.append(s.replace("@ID@", i))
        return i

    def raw(self, s, p="r"):
        return self.add(s, p)

    # ---- text (Kanit for Thai, Montserrat for English) ----
    def label(self, x, y, text, size=28, col=LBL, op=0, weight=800, sp=0.06, anchor="middle"):
        if TH() and any(0x0E00 <= ord(ch) <= 0x0E7F for ch in text):
            fam, size, weight, sp = "Kanit", round(size * 1.1), (700 if weight >= 700 else 600), 0
        else:
            fam = "Montserrat"
        return self.add(f'<text id="@ID@" x="{x}" y="{y}" text-anchor="{anchor}" font-family="{fam}" font-weight="{weight}" font-size="{size}" '
                        f'letter-spacing="{sp}em" fill="{col}" style="opacity:{op}">{text}</text>', "t")

    def pill(self, x, y, text, fill=WHITE, tcol="#0b0b0b", size=28, op=0, glow=True):
        thai = TH() and any(0x0E00 <= ord(ch) <= 0x0E7F for ch in text)
        fam, fs, fw, sp = ("Kanit", round(size * 1.1), 700, 0) if thai else ("Montserrat", size, 800, 0.06)
        w = tw(text, fs, sp) + 52; h = size + 28
        g = 'style="filter:drop-shadow(0 0 12px rgba(255,255,255,0.3))"' if glow else ""
        return self.add(f'<g id="@ID@" style="opacity:{op}"><rect x="{x - w / 2:.0f}" y="{y - h / 2:.0f}" width="{w:.0f}" height="{h}" rx="{h / 2}" fill="{fill}" {g}/>'
                        f'<text x="{x}" y="{y + size * 0.36:.0f}" text-anchor="middle" font-family="{fam}" font-weight="{fw}" font-size="{fs}" '
                        f'letter-spacing="{sp}em" fill="{tcol}">{text}</text></g>', "pl")

    def path(self, d, col=WHITE, w=4, fill="none", drawn=False, style=""):
        st = ("" if drawn else "stroke-dasharray:1 1.2;stroke-dashoffset:1.1;") + style
        dash = ('' if drawn else 'pathLength="1" ') + (f'style="{st}"' if st else "")
        return self.add(f'<path id="@ID@" d="{d}" fill="{fill}" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {dash}/>', "p")

    def spot(self, x, op=1.0, col="255,255,255", top=36, bot=150, gy=GY):
        gid = self.uid("gr")
        return self.add(f'<g id="@ID@" style="opacity:{op}"><defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
                        f'<stop offset="0" stop-color="rgb({col})" stop-opacity="0.26"/><stop offset="1" stop-color="rgb({col})" stop-opacity="0.04"/></linearGradient></defs>'
                        f'<path d="M {x - top} 380 L {x + top} 380 L {x + bot} {gy} L {x - bot} {gy} Z" fill="url(#{gid})"/>'
                        f'<ellipse cx="{x}" cy="{gy}" rx="{bot + 10}" ry="26" fill="none" stroke="rgb({col})" stroke-opacity="0.55" stroke-width="2" stroke-dasharray="8 8"/></g>', "sp")

    # ---- motion ----
    def draw(self, i, t, d=0.6, ease="power2.inOut"):
        tl(f'tl.fromTo("#{i}", {{strokeDashoffset: 1.1}}, {{strokeDashoffset: 0, duration: {d:.3f}, ease: "{ease}", immediateRender: false}}, {t:.3f});')

    def fade(self, i, t, d=0.35, to=1, frm=0, y=0):
        a = f", y: {y}" if y else ""; b = ", y: 0" if y else ""
        tl(f'tl.fromTo("#{i}", {{opacity: {frm}{a}}}, {{opacity: {to}{b}, duration: {d:.3f}, ease: "power2.out", immediateRender: false}}, {t:.3f});')

    def pop(self, i, t, d=0.4, frm=0.4, origin="50% 50%"):
        if t > self.o + 0.05:
            tl(f'tl.set("#{i}", {{opacity: 0}}, {self.o:.3f});')
        tl(f'tl.fromTo("#{i}", {{opacity: 0, scale: {frm}, transformOrigin: "{origin}"}}, {{opacity: 1, scale: 1, duration: {d:.3f}, ease: "back.out(1.8)", immediateRender: false}}, {t:.3f});')


def out(i, t, d=0.3, to=0):
    tl(f'tl.to("#{i}", {{opacity: {to}, duration: {d}}}, {t:.3f});')

def pulse(i, t, n=3, lo=0.35, d=0.4):
    tl(f'tl.to("#{i}", {{opacity: {lo}, duration: {d}, yoyo: true, repeat: {2 * n - 1}, ease: "sine.inOut"}}, {t:.3f});')

def xmark(s, x, y, r=20, col=RED, w=6):
    return s.path(f"M {x - r} {y - r} L {x + r} {y + r} M {x + r} {y - r} L {x - r} {y + r}", col, w)

def check(s, x, y, r=20, col=GREEN, w=6):
    return s.path(f"M {x - r} {y} L {x - r * 0.3} {y + r * 0.7} L {x + r} {y - r * 0.7}", col, w)

def arrow(s, x0, y0, x1, y1, col=GOLD, w=5, head=20):
    p = s.path(f"M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f}", col, w)
    ang = math.atan2(y1 - y0, x1 - x0)
    pts = [(x1, y1), (x1 - head * math.cos(ang - 0.45), y1 - head * math.sin(ang - 0.45)), (x1 - head * math.cos(ang + 0.45), y1 - head * math.sin(ang + 0.45))]
    h = s.raw(f'<polygon id="@ID@" points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="{col}" style="opacity:0"/>', "ah")
    return p, h

def show_arrow(s, ph, t, d=0.45):
    p, h = ph
    s.draw(p, t, d); s.pop(h, t + d - 0.05, 0.2, 0.5)

def captions(s, items, end, y=CAP_Y, size=32):
    """items: [(t, text, col)]; each holds until the next one"""
    for k, (t, text, col) in enumerate(items):
        t_end = items[k + 1][0] if k + 1 < len(items) else end
        i = s.label(540, y, text, size, col, 0, 800, 0.06)
        s.fade(i, t, 0.3, y=10)
        tl(f'tl.to("#{i}", {{opacity: 0, duration: 0.15}}, {t_end - 0.18:.3f});')

def header(s, text, y=500):
    return s.label(540, y, text, 28, GREY, 1, 700, 0.2)

SYMBOL = "XAUUSD"                                 # the whole series is made for gold

def series_tag(s, ep):
    """small series marker at the top of every chart scene"""
    return s.label(540, 300, L(f"{SYMBOL}  ·  CRT SERIES  ·  PART {ep}/5", f"{SYMBOL}  ·  ซีรีส์ CRT  ·  ตอนที่ {ep}/5"), 26, GOLD, 1, 700, 0.2)

def sym_pill(s, y=235):
    """the symbol badge on the opening (thumbnail) scene"""
    return s.pill(540, y, L(f"{SYMBOL}  ·  GOLD", f"{SYMBOL}  ·  ทองคำ"), GOLD, "#111", 28, 1)

def gp(p, base=4100.0, k=0.6):
    """example XAUUSD price for chart price p (illustrative, not real data)"""
    return f"{base + p * k:,.2f}"


# ================================================================================================= candles
class Chart:
    """candles [(o, h, l, c)]; price pmin..pmax maps to y bot..top, index 0..nx maps to x x0..x1"""
    def __init__(self, candles, nx=None, x0=80, x1=1000, top=600, bot=1240, pmin=0, pmax=100, bwf=0.7):
        self.c = candles
        self.nx = nx or len(candles)
        self.x0, self.x1, self.top, self.bot, self.pmin, self.pmax, self.bwf = x0, x1, top, bot, pmin, pmax, bwf

    def x(self, i): return self.x0 + (self.x1 - self.x0) * (i + 0.5) / self.nx
    def y(self, p): return self.bot - (self.bot - self.top) * (p - self.pmin) / (self.pmax - self.pmin)
    def xy(self, i, p): return (round(self.x(i), 1), round(self.y(p), 1))
    @property
    def sp(self): return (self.x1 - self.x0) / self.nx
    @property
    def bw(self): return max(3.0, self.sp * self.bwf)

    def candle(self, i, extra="", up=UP, down=DOWN, sw=2):
        o, h, lo, c = self.c[i]
        col = up if c >= o else down
        x = self.x(i)
        yt, yb = self.y(max(o, c)), self.y(min(o, c))
        return (f'<g {extra}><line x1="{x:.1f}" y1="{self.y(h):.1f}" x2="{x:.1f}" y2="{self.y(lo):.1f}" stroke="{col}" stroke-width="{sw}"/>'
                f'<rect x="{x - self.bw / 2:.1f}" y="{yt:.1f}" width="{self.bw:.1f}" height="{max(2, yb - yt):.1f}" fill="{col}"/></g>')

    def candles(self, i0=0, i1=None):
        i1 = len(self.c) if i1 is None else i1
        return "".join(self.candle(i) for i in range(i0, i1))

    def edge(self, i): return round(self.x(i) + self.sp * 0.55, 1)


def path_candles(pivots, seed=3, noise=1.2, wick=0.9, start=None):
    """candles through hand-placed pivots (index, price): closes follow the line between pivots with a little noise; a
    pivot high/low is hit exactly by that candle's wick and no neighbour goes past it."""
    r = random.Random(seed)
    path = []
    for (i0, p0), (i1, p1) in zip(pivots, pivots[1:]):
        path += [p0 + (p1 - p0) * (i - i0) / (i1 - i0) for i in range(i0, i1)]
    path.append(pivots[-1][1])
    piv = dict(pivots)
    kind = {}
    for k, (i, p) in enumerate(pivots):
        pr = pivots[k - 1][1] if k else None
        nx = pivots[k + 1][1] if k + 1 < len(pivots) else None
        if (pr is None or p > pr) and (nx is None or p > nx): kind[i] = "hi"
        elif (pr is None or p < pr) and (nx is None or p < nx): kind[i] = "lo"
    out, prev = [], (start if start is not None else path[0])
    for i, p in enumerate(path):
        c = p + (r.uniform(-noise, noise) if i not in piv else 0)
        o = prev
        if kind.get(i) == "hi": o = p - r.uniform(0.4, 1.2) * wick; c = p - r.uniform(0.2, 0.6) * wick
        if kind.get(i) == "lo": o = p + r.uniform(0.4, 1.2) * wick; c = p + r.uniform(0.2, 0.6) * wick
        h = max(o, c) + r.uniform(0.2, 1.0) * wick
        lo = min(o, c) - r.uniform(0.2, 1.0) * wick
        if kind.get(i) == "hi": h = p
        if kind.get(i) == "lo": lo = p
        for j in (i - 1, i + 1):
            if kind.get(j) == "hi": h = min(h, piv[j] - 0.15); o = min(o, h); c = min(c, h)
            if kind.get(j) == "lo": lo = max(lo, piv[j] + 0.15); o = max(o, lo); c = max(c, lo)
        out.append((o, h, lo, c))
        prev = c
    return out


def candles_clip(s, ch, i1=None, op=1.0):
    """all candles in one group behind a clip rect; returns the clip rect id (tween its width to reveal)"""
    cid, rid = s.uid("cp"), s.uid("cr")
    s.items.append(f'<defs><clipPath id="{cid}"><rect id="{rid}" x="0" y="0" width="0" height="1920"/></clipPath></defs>')
    s.raw(f'<g id="@ID@" clip-path="url(#{cid})" style="opacity:{op}">' + ch.candles(0, i1) + "</g>", "cg")
    return rid

def reveal(rid, ch, keys, t_open):
    """keys: [(t, idx), ...]; the clip edge sits just past candle idx at time t (idx -1 = nothing shown)"""
    def w(i): return ch.x0 if i < 0 else ch.edge(i)
    tl(f'tl.set("#{rid}", {{attr: {{width: {w(keys[0][1])}}}}}, {t_open:.3f});')
    for (t0, i0), (t1, i1) in zip(keys, keys[1:]):
        if i1 != i0:
            tl(f'tl.fromTo("#{rid}", {{attr: {{width: {w(i0)}}}}}, {{attr: {{width: {w(i1)}}}, duration: {max(0.05, t1 - t0):.3f}, ease: "none", immediateRender: false}}, {t0:.3f});')

def hline(s, ch, p, i0, i1, col, w=3, dash="14 10", op=0):
    x0, x1 = (ch.x(i0) if isinstance(i0, (int, float)) and i0 > -50 else i0), ch.x(i1)
    return s.raw(f'<line id="@ID@" x1="{x0:.1f}" y1="{ch.y(p):.1f}" x2="{x1:.1f}" y2="{ch.y(p):.1f}" stroke="{col}" stroke-width="{w}" '
                 f'stroke-dasharray="{dash}" style="opacity:{op}"/>', "hl")

def rbox(s, x0, y0, x1, y1, col, fop=0.14, sop=0.85, sw=2.5, op=0, dash=""):
    d = f'stroke-dasharray="{dash}"' if dash else ""
    return s.raw(f'<rect id="@ID@" x="{min(x0, x1):.1f}" y="{min(y0, y1):.1f}" width="{abs(x1 - x0):.1f}" height="{abs(y1 - y0):.1f}" fill="{col}" '
                 f'fill-opacity="{fop}" stroke="{col}" stroke-opacity="{sop}" stroke-width="{sw}" {d} style="opacity:{op}"/>', "bx")

def ring(s, x, y, r=22, col=GOLD, op=0):
    return s.raw(f'<circle id="@ID@" cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" stroke="{col}" stroke-width="4" style="opacity:{op};filter:drop-shadow(0 0 10px {col})"/>', "c")

def big_candle(s, x, w, yh, yo, yc, yl, op=1, col=None, glow=True):
    """one big candle in screen coordinates (y of high, open, close, low)"""
    col = col or (UP if yc < yo else DOWN)
    g = f"filter:drop-shadow(0 0 18px {'rgba(41,98,255,0.55)' if col == UP else 'rgba(255,255,255,0.35)'});" if glow else ""
    return s.raw(f'<g id="@ID@" style="opacity:{op};{g}"><line x1="{x}" y1="{yh}" x2="{x}" y2="{yl}" stroke="{col}" stroke-width="5"/>'
                 f'<rect x="{x - w / 2}" y="{min(yo, yc)}" width="{w}" height="{abs(yc - yo)}" fill="{col}"/></g>', "bc")

def stop_chips(s, xs, y, col=RED, text="SL", size=18):
    """a row of small stop-loss chips; returns their ids"""
    ids = []
    for x in xs:
        w = tw(text, size) + 22; h = size + 14
        ids.append(s.raw(f'<g id="@ID@" style="opacity:0"><rect x="{x - w / 2:.0f}" y="{y - h / 2:.0f}" width="{w:.0f}" height="{h}" rx="6" fill="{col}"/>'
                         f'<text x="{x}" y="{y + size * 0.36:.0f}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="{size}" fill="#fff">{text}</text></g>', "sc"))
    return ids


# ================================================================================================= outro + page
def outro(o):
    """order the market (outro with handles; no end card)"""
    s = S(o, G["TOTAL"])
    ko, kd, kf = K("order"), K("dont"), K("follow")
    es = s.spot(540, 0, "232,194,106", 40, 230); s.fade(es, ko, 0.6)
    em = s.raw('<image id="@ID@" href="assets/otm_emblem.png" x="390" y="900" width="300" height="291" style="opacity:0;filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>', "i")
    s.pop(em, ko, 0.7, 0.6); cue(ko, "bell_A4", -16)
    o1 = s.label(540, 1300, "ORDER THE MARKET", 32, GOLD, 0, 800, 0.3); s.fade(o1, ko + 0.3, 0.5)
    o2 = s.label(540, 1362, L("DON'T LET THE MARKET ORDER YOU", "อย่าให้ตลาดเป็นฝ่ายสั่งคุณ"), 28, WHITE, 0, 700, 0.12); s.fade(o2, kd, 0.4)
    o3 = s.pill(540, 1470, "FOLLOW FOR MORE", GOLD, "#111", 30); s.pop(o3, kf, 0.4, 0.6); cue(kf, "click-confirm_1", -16)
    hx = 290
    soc = s.raw(f'<g id="@ID@" style="opacity:0">'
                f'<rect x="{hx}" y="1548" width="36" height="36" rx="10" fill="none" stroke="#fff" stroke-width="3"/>'
                f'<circle cx="{hx + 18}" cy="1566" r="8.5" fill="none" stroke="#fff" stroke-width="3"/><circle cx="{hx + 28}" cy="1556" r="2.4" fill="#fff"/>'
                f'<text x="{hx + 48}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@fxzuez_28</text>'
                f'<path d="M {hx + 322} 1546 V 1574 A 9 9 0 1 1 {hx + 313} 1565 M {hx + 322} 1546 Q {hx + 326} 1557 {hx + 338} 1558" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>'
                f'<text x="{hx + 348}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@zuez_28</text></g>', "so")
    disc = s.label(540, 1650, "EDUCATIONAL ONLY · NOT FINANCIAL ADVICE", 28, GREY, 0, 600, 0.12)
    s.fade(soc, kd + 0.6, 0.5, y=12)
    s.fade(disc, kd + 0.9, 0.5)
    tl(f'tl.to("#mark", {{opacity: 0, duration: 0.3}}, {ko - 0.2:.3f});')


_FONTS = "".join(
    f"@font-face {{ font-family: 'Kanit'; font-style: normal; font-weight: {w}; font-display: block; "
    f"src: url('assets/fonts/kanit-{sub}-{w}-normal.woff2') format('woff2'); unicode-range: {rng}; }}\n"
    for w in (600, 700)
    for sub, rng in (("thai", "U+02D7, U+0303, U+0331, U+0E01-0E5B, U+200C-200D, U+25CC"),
                     ("latin", "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, "
                               "U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD")))


def write():
    ROOT, TOTAL, COMP = G["ROOT"], G["TOTAL"], G["COMP"]
    dust = ""
    for k in range(40):
        x, y, r, op = rnd.uniform(0, 1080), rnd.uniform(0, 1920), rnd.uniform(1.2, 3.2), rnd.uniform(0.05, 0.22)
        dust += f'<circle id="d{k}" cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#fff" opacity="{op:.2f}"/>'
        tl(f'tl.fromTo("#d{k}", {{x: 0, y: 0}}, {{x: {rnd.uniform(-70, 70):.0f}, y: {-rnd.uniform(150, 480):.0f}, duration: {TOTAL}, ease: "none"}}, 0);')
    scenes_svg = "\n".join(f'<g id="{x.id}" style="opacity:0;visibility:hidden" data-layout-allow-overlap>' + "".join(x.items) + "</g>" for x in S.scenes)
    css = (_FONTS if TH() else "") + """
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #000; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #000; font-family: Montserrat, sans-serif; color: #fff; }
#stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
#vig { position: absolute; inset: 0; pointer-events: none; background: radial-gradient(ellipse at 50% 48%, rgba(40,44,52,0.35) 0%, transparent 55%, rgba(0,0,0,0.6) 100%); }
#mark { position: absolute; left: 495px; top: 1560px; width: 90px; opacity: 0.85; filter: drop-shadow(0 0 10px rgba(255,255,255,0.2)); }
"""
    html = f"""<!doctype html>
<html lang="{G['LANG']}" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{css}</style>
  </head>
  <body>
    <div id="root" data-composition-id="{COMP}" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
{scenes_svg}
      </svg>
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <audio id="{COMP}-audio" class="clip" src="assets/audio/{G['MIX']}.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["{COMP}"] = tl;
      }})();
    </script>
  </body>
</html>
"""
    open(f"{ROOT}/index.html", "w").write(html)
    json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
    json.dump(dict(total=TOTAL, lead=LEAD, end_t=G["END_T"]), open(f"{ROOT}/work/timing.json", "w"))
    print(COMP, "total", TOTAL, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
