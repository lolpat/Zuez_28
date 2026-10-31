"""OTM "which losses to take" animation in the style of the reference: one idea per scene, drawn as glowing white
line icons with small tracked labels, cut to the narration's words, with a phrase caption under the stage.

Inputs: work/words.json (word timings of assets/audio/vo_main.wav), assets/audio/vo_outro.wav.
Outputs: index.html and work/cues.json (sound cues for work/mix.py).
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1080, 1920
LEAD = 0.3
GOLD, BLUE = "#e8c26a", "#2962ff"
CX, CY = 540, 900                                      # stage centre
WORDS = [w for w in json.load(open(f"{ROOT}/work/words.json"))["words"] if w["type"] == "word"]
def norm(s): return re.sub(r"[^a-z0-9']", "", s.lower())
def at(word, k=1):
    """start of the k-th time `word` is spoken (seconds on the video clock)"""
    n = 0
    for w in WORDS:
        if norm(w["text"]) == word:
            n += 1
            if n == k: return round(LEAD + w["start"], 2)
    raise KeyError(word, k)

# ---------------------------------------------------------------------------------------------------------------------
# drawing helpers (all strokes white, glow comes from the svg filter)
S = 'stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"'
def label(x, y, text, size=28, color="#cfd3da", eid="", anchor="middle", sp="0.32em", op=0):
    i = f'id="{eid}" ' if eid else ""
    return (f'<text {i}x="{x}" y="{y}" text-anchor="{anchor}" font-family="Montserrat" font-weight="700" font-size="{size}" '
            f'letter-spacing="{sp}" fill="{color}" opacity="{op}">{text}</text>')
def person(x, y, s=1.0, fill="#fff"):
    return (f'<path d="M {x - 22*s} {y} L {x - 22*s} {y - 20*s} A {22*s} {22*s} 0 0 1 {x + 22*s} {y - 20*s} L {x + 22*s} {y} Z" fill="{fill}"/>'
            f'<circle cx="{x}" cy="{y - 60*s}" r="{15*s}" fill="{fill}"/>')
def xmark(eid, x, y, r):
    L = round(r * 2 * 1.4142 + 2)
    return (f'<g id="{eid}"><line class="xl" x1="{x - r}" y1="{y - r}" x2="{x + r}" y2="{y + r}" {S} stroke-width="5" stroke-dasharray="{L}" stroke-dashoffset="{L}"/>'
            f'<line class="xl" x1="{x + r}" y1="{y - r}" x2="{x - r}" y2="{y + r}" {S} stroke-width="5" stroke-dasharray="{L}" stroke-dashoffset="{L}"/></g>')
def draw(T, sel, L, t, d=0.6):
    T.append(f'tl.fromTo("{sel}", {{strokeDashoffset: {L}}}, {{strokeDashoffset: 0, duration: {d}, ease: "power2.inOut"}}, {t:.2f});')
def pop(T, sel, t, d=0.45, fr=0.5):
    T.append(f'tl.fromTo("{sel}", {{opacity: 0, scale: {fr}, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: {d}, ease: "back.out(2)"}}, {t:.2f});')
def fade(T, sel, t, d=0.4, op=1):
    T.append(f'tl.fromTo("{sel}", {{opacity: 0, y: 14}}, {{opacity: {op}, y: 0, duration: {d}, ease: "power2.out"}}, {t:.2f});')
def strike(T, C, eid, t):
    T.append(f'tl.to("#{eid} .xl", {{strokeDashoffset: 0, duration: 0.22, stagger: 0.12, ease: "power2.in"}}, {t:.2f});')
    C.append(dict(t=t + 0.2, snd="stamp", gain=-13))
def plen(pts):
    import math
    return round(sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)) + 2)
def polyline(eid, pts, color="#fff", w=4, extra=""):
    L = plen(pts)
    return (f'<polyline id="{eid}" points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="none" stroke="{color}" stroke-width="{w}" '
            f'stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="{L}" stroke-dashoffset="{L}" {extra}/>'), L

# ---------------------------------------------------------------------------------------------------------------------
# scenes: each returns (svg, timeline, cues); the scene group itself is faded in and out by build()
def s_hook():
    T, C = [], []
    card = (f'<g id="h-card" opacity="0"><rect x="{CX - 230}" y="{CY - 150}" width="460" height="280" rx="26" {S}/>'
            f'{label(CX - 190, CY - 90, "ACCOUNT", 28, "#9aa0aa", anchor="start", op=1)}'
            f'<text id="h-bal" x="{CX - 190}" y="{CY}" font-family="Archivo Black" font-size="76" fill="#fff">$10,000</text>'
            f'<rect x="{CX - 190}" y="{CY + 40}" width="160" height="14" rx="7" fill="#fff" opacity="0.25"/></g>')
    chains = ""
    for k, (a, b) in enumerate((((CX - 300, CY - 200), (CX + 300, CY + 180)), ((CX + 300, CY - 200), (CX - 300, CY + 180)))):
        links = ""
        n = 17
        for i in range(n):
            x = a[0] + (b[0] - a[0]) * (i + 0.5) / n; y = a[1] + (b[1] - a[1]) * (i + 0.5) / n
            ang = 32 if k == 0 else -32
            hh = 8 if i % 2 else 24
            links += (f'<rect class="link{k}" x="{x - 24:.0f}" y="{y - hh / 2:.0f}" width="48" height="{hh}" rx="{hh / 2:.0f}" {S} stroke-width="5" opacity="0" '
                      f'transform="rotate({ang} {x:.0f} {y:.0f})"/>')
        chains += links
    lx = CX + 150; ly = CY + 140
    lock = (f'<g id="h-lock" opacity="0"><rect x="{lx - 48}" y="{ly - 30}" width="96" height="78" rx="12" fill="#000" {S.replace("fill=\"none\" ", "")}/>'
            f'<path d="M {lx - 28} {ly - 30} L {lx - 28} {ly - 56} A 28 28 0 0 1 {lx + 28} {ly - 56} L {lx + 28} {ly - 30}" {S}/>'
            f'<circle cx="{lx}" cy="{ly + 8}" r="8" fill="#fff"/></g>')
    flat, L = polyline("h-flat", [(CX - 300, CY + 330), (CX - 120, CY + 330), (CX + 60, CY + 334), (CX + 300, CY + 330)])
    svg = card + chains + lock + flat + label(CX, CY + 400, "+0.00%", 34, "#fff", "h-pct", sp="0.2em")
    pop(T, "#h-card", 0.15, 0.6, 0.85)
    T.append(f'tl.to(".link0", {{opacity: 1, duration: 0.08, stagger: 0.035}}, {at("lose"):.2f});')
    T.append(f'tl.to(".link1", {{opacity: 1, duration: 0.08, stagger: 0.035}}, {at("lose") + 0.2:.2f});')
    pop(T, "#h-lock", at("money"), 0.45, 0.3)
    draw(T, "#h-flat", L, at("making"), 0.7)
    fade(T, "#h-pct", at("any"))
    C += [dict(t=0.15, snd="pop", gain=-14), dict(t=at("lose"), snd="draw", gain=-13), dict(t=at("money"), snd="stamp", gain=-11),
          dict(t=at("making"), snd="swish", gain=-17)]
    return svg, T, C

def s_crowd():
    T, C = [], []
    figs = ""
    for r in range(5):
        for c in range(7):
            x = CX - 330 + c * 110 + (55 if r % 2 else 0) - 27; y = CY + 30 + r * 120
            if x > CX + 340: continue
            figs += f'<g class="cr" opacity="0">{person(x, y, 0.85)}</g>'
    bub = (f'<g id="c-bub" opacity="0"><rect x="{CX - 300}" y="{CY - 330}" width="600" height="190" rx="95" {S}/>'
           f'<path d="M {CX - 40} {CY - 141} L {CX - 70} {CY - 90} L {CX + 10} {CY - 141}" {S} fill="#000"/>'
           f'<circle cx="{CX - 200}" cy="{CY - 235}" r="44" {S}/>'
           f'<path d="M {CX - 200} {CY - 262} L {CX - 192} {CY - 243} L {CX - 172} {CY - 241} L {CX - 187} {CY - 228} L {CX - 182} {CY - 208} '
           f'L {CX - 200} {CY - 219} L {CX - 218} {CY - 208} L {CX - 213} {CY - 228} L {CX - 228} {CY - 241} L {CX - 208} {CY - 243} Z" fill="#fff"/>'
           f'{label(CX + 50, CY - 248, "THE BEST TRADE", 30, "#fff", anchor="middle", sp="0.18em", op=1)}'
           f'{label(CX + 50, CY - 200, "NEVER LOSES", 30, GOLD, "c-nl", anchor="middle", sp="0.18em")}</g>')
    svg = figs + bub
    T.append(f'tl.fromTo(".cr", {{opacity: 0, y: 20}}, {{opacity: 1, y: 0, duration: 0.3, stagger: {{each: 0.025, from: "center"}}, ease: "back.out(2)"}}, {at("most"):.2f});')
    pop(T, "#c-bub", at("best"), 0.5, 0.6)
    fade(T, "#c-nl", at("never"))
    C += [dict(t=at("most"), snd="swish", gain=-15), dict(t=at("best"), snd="pop", gain=-13), dict(t=at("never"), snd="ping", gain=-14)]
    return svg, T, C

def s_diff():
    T, C = [], []
    lx, rx = CX - 260, CX + 260
    shield = (f'<g id="d-sh" opacity="0"><path d="M {lx} {CY - 120} L {lx + 95} {CY - 85} L {lx + 95} {CY + 5} Q {lx + 95} {CY + 95} {lx} {CY + 140} '
              f'Q {lx - 95} {CY + 95} {lx - 95} {CY + 5} L {lx - 95} {CY - 85} Z" {S}/>'
              f'<line x1="{lx - 30}" y1="{CY}" x2="{lx + 30}" y2="{CY}" {S} stroke-width="6"/>'
              f'{label(lx, CY + 230, "AVOIDING", 28, op=1)}{label(lx, CY + 272, "LOSSES", 28, op=1)}</g>')
    ne = (f'<g id="d-ne" opacity="0"><circle cx="{CX}" cy="{CY}" r="62" {S}/>'
          f'<line x1="{CX - 28}" y1="{CY - 12}" x2="{CX + 28}" y2="{CY - 12}" {S}/><line x1="{CX - 28}" y1="{CY + 12}" x2="{CX + 28}" y2="{CY + 12}" {S}/>'
          f'<line x1="{CX + 18}" y1="{CY - 32}" x2="{CX - 18}" y2="{CY + 32}" {S}/></g>')
    import math
    ticks = "".join(f'<line x1="{rx + 110*math.cos(math.radians(a)):.0f}" y1="{CY + 40 - 110*math.sin(math.radians(a)):.0f}" '
                    f'x2="{rx + 92*math.cos(math.radians(a)):.0f}" y2="{CY + 40 - 92*math.sin(math.radians(a)):.0f}" {S} stroke-width="3"/>'
                    for a in range(0, 181, 20))
    gauge = (f'<g id="d-ga" opacity="0"><path d="M {rx - 130} {CY + 40} A 130 130 0 0 1 {rx + 130} {CY + 40}" {S}/>{ticks}'
             f'<g id="d-needle"><line x1="{rx}" y1="{CY + 40}" x2="{rx}" y2="{CY - 60}" stroke="{GOLD}" stroke-width="6" stroke-linecap="round"/></g>'
             f'<circle cx="{rx}" cy="{CY + 40}" r="10" fill="#fff"/>'
             f'{label(rx, CY + 110, "1%", 36, GOLD, sp="0.1em", op=1)}'
             f'{label(rx, CY + 230, "MANAGING", 28, op=1)}{label(rx, CY + 272, "RISK", 28, op=1)}</g>')
    svg = shield + ne + gauge
    pop(T, "#d-ne", at("difference"), 0.45, 0.3)
    pop(T, "#d-sh", at("avoiding"), 0.5, 0.6)
    pop(T, "#d-ga", at("managing"), 0.5, 0.6)
    T.append(f'tl.fromTo("#d-needle", {{rotation: 80, svgOrigin: "{rx} {CY + 40}"}}, {{rotation: -62, svgOrigin: "{rx} {CY + 40}", duration: 0.9, ease: "elastic.out(1, 0.5)"}}, {at("risk"):.2f});')
    C += [dict(t=at("difference"), snd="ping", gain=-14), dict(t=at("avoiding"), snd="pop", gain=-13),
          dict(t=at("managing"), snd="pop", gain=-13), dict(t=at("risk"), snd="tick", gain=-12)]
    return svg, T, C

def s_trader():
    T, C = [], []
    b = 230
    corners = "".join(f'<path d="M {x} {y + dy} L {x} {y} L {x + dx} {y}" {S} stroke-width="3"/>'
                      for x, y, dx, dy in ((CX - b, CY - b, 50, 50), (CX + b, CY - b, -50, 50), (CX - b, CY + b, 50, -50), (CX + b, CY + b, -50, -50)))
    tag = (f'<g id="t-tag" opacity="0"><rect x="{CX + 60}" y="{CY - 170}" width="150" height="74" rx="14" {S}/>'
           f'<text x="{CX + 135}" y="{CY - 120}" text-anchor="middle" font-family="Archivo Black" font-size="34" fill="#fff">-$</text>'
           f'<circle cx="{CX + 210}" cy="{CY - 170}" r="34" fill="#000" {S.replace("fill=\"none\" ", "")}/>'
           f'<line x1="{CX + 186}" y1="{CY - 146}" x2="{CX + 234}" y2="{CY - 194}" {S}/></g>')
    svg = f'<g id="t-fr" opacity="0">{corners}</g><g id="t-p" opacity="0">{person(CX - 40, CY + 120, 1.6)}</g>{tag}' + label(CX, CY + b + 70, "THE TRADER", 28, eid="t-l")
    fade(T, "#t-fr", at("imagine"), 0.5)
    pop(T, "#t-p", at("imagine") + 0.15, 0.5, 0.6)
    fade(T, "#t-l", at("trader"))
    pop(T, "#t-tag", at("refuses"), 0.45, 0.4)
    C += [dict(t=at("imagine"), snd="swish", gain=-15), dict(t=at("refuses"), snd="stamp", gain=-12)]
    return svg, T, C

def s_habits():
    T, C = [], []
    xs = [CX - 330, CX, CX + 330]; y0 = CY - 40
    box = lambda i: f'<rect x="{xs[i] - 120}" y="{y0 - 120}" width="240" height="240" rx="28" {S}/>'
    # 1 moves the stop loss
    i0 = (f'<g id="hb0" opacity="0">{box(0)}<line x1="{xs[0] - 30}" y1="{y0 - 80}" x2="{xs[0] - 30}" y2="{y0 + 40}" {S} stroke-width="3"/>'
          f'<rect x="{xs[0] - 50}" y="{y0 - 55}" width="40" height="70" fill="#fff"/>'
          f'<line id="hb0-sl" x1="{xs[0] - 90}" y1="{y0 + 30}" x2="{xs[0] + 90}" y2="{y0 + 30}" stroke="#fff" stroke-width="4" stroke-dasharray="12 10"/>'
          f'<path d="M {xs[0] + 50} {y0 - 10} L {xs[0] + 50} {y0 + 80} M {xs[0] + 32} {y0 + 62} L {xs[0] + 50} {y0 + 80} L {xs[0] + 68} {y0 + 62}" {S}/>'
          f'{label(xs[0], y0 + 175, "MOVES", 28, op=1)}{label(xs[0], y0 + 212, "THE STOP", 28, op=1)}</g>')
    # 2 cuts winners early
    i1 = (f'<g id="hb1" opacity="0">{box(1)}<path d="M {xs[1] - 90} {y0 + 70} L {xs[1] - 40} {y0 + 20} L {xs[1] - 10} {y0 + 40}" {S}/>'
          f'<path d="M {xs[1] + 30} {y0 - 10} L {xs[1] + 90} {y0 - 70}" {S} stroke-dasharray="8 10" opacity="0.5"/>'
          f'<circle cx="{xs[1] + 12}" cy="{y0 + 14}" r="14" {S} stroke-width="3"/><circle cx="{xs[1] - 4}" cy="{y0 + 52}" r="14" {S} stroke-width="3"/>'
          f'<line x1="{xs[1] + 22}" y1="{y0 + 26}" x2="{xs[1] + 60}" y2="{y0 + 60}" {S} stroke-width="3"/>'
          f'<line x1="{xs[1] + 8}" y1="{y0 + 40}" x2="{xs[1] + 60}" y2="{y0 + 10}" {S} stroke-width="3"/>'
          f'{label(xs[1], y0 + 175, "CUTS", 28, op=1)}{label(xs[1], y0 + 212, "WINNERS", 28, op=1)}</g>')
    # 3 skips valid setups
    i2 = (f'<g id="hb2" opacity="0">{box(2)}<rect x="{xs[2] - 60}" y="{y0 - 80}" width="120" height="150" rx="10" {S} stroke-width="3"/>'
          + "".join(f'<path d="M {xs[2] - 40} {y0 - 40 + k*40} l 10 10 l 18 -20" {S} stroke-width="3"/><line x1="{xs[2] + 0}" y1="{y0 - 35 + k*40}" x2="{xs[2] + 40}" y2="{y0 - 35 + k*40}" {S} stroke-width="3"/>' for k in range(3))
          + f'{label(xs[2], y0 + 175, "SKIPS", 28, op=1)}{label(xs[2], y0 + 212, "SETUPS", 28, op=1)}</g>')
    xm = "".join(xmark(f"hx{i}", xs[i], y0, 95) for i in range(3))
    q = (f'<text id="hb-q" x="{CX}" y="{CY + 420}" text-anchor="middle" font-family="Playfair Display" font-style="italic" font-size="120" '
         f'fill="#fff" opacity="0">?</text>')
    svg = i0 + i1 + i2 + xm + q
    for k, word in enumerate(("stop", "cut", "skip")):
        t = at(word)
        pop(T, f"#hb{k}", t - 0.25, 0.45, 0.6)
        C.append(dict(t=t - 0.25, snd="pop", gain=-13))
        if k == 0:
            T.append(f'tl.fromTo("#hb0-sl", {{y: 0}}, {{y: 40, duration: 0.4, yoyo: true, repeat: 1, ease: "power2.inOut"}}, {t + 0.2:.2f});')
        strike(T, C, f"hx{k}", t + 0.55)
    pop(T, "#hb-q", at("scared"), 0.5, 0.4)
    C.append(dict(t=at("scared"), snd="ping", gain=-14))
    return svg, T, C

def s_dome():
    T, C = [], []
    coins = "".join(f'<rect x="{CX - 90}" y="{CY + 150 - k*30}" width="180" height="26" rx="13" {S} stroke-width="3"/>' for k in range(6))
    dome = (f'<g id="m-dome" opacity="0"><path d="M {CX - 180} {CY + 200} L {CX - 180} {CY - 20} A 180 180 0 0 1 {CX + 180} {CY - 20} L {CX + 180} {CY + 200}" {S}/>'
            f'<line x1="{CX - 230}" y1="{CY + 200}" x2="{CX + 230}" y2="{CY + 200}" {S}/>'
            f'<circle cx="{CX}" cy="{CY - 210}" r="12" {S} stroke-width="3"/></g>')
    sh = (f'<g id="m-sh" opacity="0"><path d="M {CX - 330} {CY - 40} L {CX - 280} {CY - 22} L {CX - 280} {CY + 20} Q {CX - 280} {CY + 66} {CX - 330} {CY + 88} '
          f'Q {CX - 380} {CY + 66} {CX - 380} {CY + 20} L {CX - 380} {CY - 22} Z" {S} stroke-width="3"/>'
          f'<path d="M {CX - 350} {CY + 22} l 14 14 l 28 -30" {S} stroke-width="3"/>{label(CX - 330, CY + 150, "PROTECTED", 28, op=1)}</g>')
    ghost = "".join(f'<rect class="m-g" x="{CX - 90}" y="{CY - 40 - k*30}" width="180" height="26" rx="13" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="6 8" opacity="0"/>' for k in range(12))
    lim = (f'<g id="m-lim" opacity="0">{label(CX + 330, CY - 50, "LIMITED", 28, GOLD, op=1)}'
           + "".join(f'<path d="M {CX + 300 + k*30} {CY - 120} l 0 40 m -10 -12 l 10 12 l 10 -12" {S} stroke-width="3" stroke="{GOLD}"/>' for k in range(3))
           + f'{label(CX, CY - 440, "POTENTIAL", 28, op=1)}</g>')
    svg = ghost + f'<g id="m-coins" opacity="0">{coins}</g>' + dome + sh + lim
    pop(T, "#m-coins", at("protecting") - 0.1, 0.45, 0.7)
    pop(T, "#m-dome", at("account", 1), 0.5, 0.8)
    pop(T, "#m-sh", at("have"), 0.45, 0.5)
    T.append(f'tl.to(".m-g", {{opacity: 0.6, duration: 0.12, stagger: 0.06}}, {at("limiting"):.2f});')
    fade(T, "#m-lim", at("become"))
    C += [dict(t=at("protecting"), snd="pop", gain=-13), dict(t=at("account", 1), snd="swish", gain=-15),
          dict(t=at("limiting"), snd="riser", gain=-17), dict(t=at("become"), snd="tick", gain=-12)]
    return svg, T, C

def s_receipt():
    T, C = [], []
    x0, x1, y0, y1 = CX - 170, CX + 170, CY - 280, CY + 260
    zig = " ".join(f"L {x1 - k*34} {y1 + (14 if k % 2 else 0)}" for k in range(11))
    paper = (f'<g id="r-pp" opacity="0"><path d="M {x0} {y0} L {x1} {y0} L {x1} {y1} {zig} L {x0} {y0} Z" {S}/>'
             f'<rect x="{x0 - 30}" y="{y0 - 22}" width="{x1 - x0 + 60}" height="34" rx="10" fill="#000" {S.replace("fill=\"none\" ", "")}/>'
             + "".join(f'<line x1="{x0 + 40}" y1="{CY - 120 + k*56}" x2="{x0 + 170}" y2="{CY - 120 + k*56}" {S} stroke-width="3" opacity="0.6"/>'
                       f'<line x1="{x1 - 90}" y1="{CY - 120 + k*56}" x2="{x1 - 40}" y2="{CY - 120 + k*56}" {S} stroke-width="3" opacity="0.6"/>' for k in range(4))
             + f'<text x="{x0 + 40}" y="{CY + 170}" font-family="Montserrat" font-weight="800" font-size="34" fill="#fff">LOSS</text>'
               f'<text x="{x1 - 40}" y="{CY + 170}" text-anchor="end" font-family="Archivo Black" font-size="34" fill="#fff">-1%</text></g>')
    head = (f'<text id="r-h1" x="{CX}" y="{y0 + 70}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="40" letter-spacing="0.2em" fill="#fff" opacity="0">LOSS</text>'
            f'<line id="r-st" x1="{CX - 90}" y1="{y0 + 56}" x2="{CX + 90}" y2="{y0 + 56}" stroke="#fff" stroke-width="5" stroke-dasharray="182" stroke-dashoffset="182"/>'
            f'<text id="r-h2" x="{CX}" y="{CY + 380}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="38" letter-spacing="0.18em" fill="{GOLD}" opacity="0">COST OF BUSINESS</text>')
    svg = paper + head
    T.append(f'tl.fromTo("#r-pp", {{opacity: 0, y: -160}}, {{opacity: 1, y: 0, duration: 0.9, ease: "power2.out"}}, {at("because", 2):.2f});')
    fade(T, "#r-h1", at("losses", 2))
    draw(T, "#r-st", 182, at("losses", 3), 0.35)
    pop(T, "#r-h2", at("cost"), 0.5, 0.7)
    C += [dict(t=at("because", 2), snd="swish", gain=-15), dict(t=at("losses", 3), snd="draw", gain=-14), dict(t=at("cost"), snd="stamp", gain=-11)]
    return svg, T, C

def s_nostop():
    T, C = [], []
    cs = [(CX - 280, -150, -110), (CX - 200, -110, -40), (CX - 120, -60, 40), (CX - 40, 20, 150), (CX + 40, 120, 330)]
    candles = "".join(f'<g class="ns-c" opacity="0"><line x1="{x}" y1="{CY + o - 20}" x2="{x}" y2="{CY + c + 20}" {S} stroke-width="3"/>'
                      f'<rect x="{x - 24}" y="{CY + o}" width="48" height="{c - o}" fill="#fff"/></g>' for x, o, c in cs)
    acc = (f'<g id="ns-acc" opacity="0"><rect x="{CX + 120}" y="{CY - 260}" width="260" height="150" rx="20" {S}/>'
           f'{label(CX + 145, CY - 215, "ACCOUNT", 28, "#9aa0aa", anchor="start", op=1)}'
           f'<text id="ns-bal" x="{CX + 145}" y="{CY - 140}" font-family="Archivo Black" font-size="54" fill="#fff">$10,000</text></g>')
    gone = (f'<text id="ns-gone" x="{CX + 250}" y="{CY - 40}" text-anchor="middle" font-family="Archivo Black" font-size="64" '
            f'letter-spacing="0.12em" fill="#fff" opacity="0">GONE</text>')
    nos = label(CX - 160, CY - 260, "NO STOP LOSS", 28, eid="ns-l")
    svg = candles + acc + gone + nos
    T.append(f'tl.fromTo(".ns-c", {{opacity: 0, scaleY: 0.2, transformOrigin: "50% 0%"}}, {{opacity: 1, scaleY: 1, duration: 0.3, stagger: 0.18, ease: "power2.out"}}, {at("trade", 2) - 0.1:.2f});')
    fade(T, "#ns-l", at("no"))
    pop(T, "#ns-acc", at("stop", 2), 0.45, 0.7)
    T.append(f'tl.to("#ns-bal", {{textContent: 0, duration: 1.0, ease: "power2.in", snap: {{textContent: 1}}, '
             f'onUpdate: function () {{ const e = document.querySelector("#ns-bal"); e.textContent = "$" + Number(e.textContent.replace(/[^0-9]/g, "")).toLocaleString("en-US"); }} }}, {at("empty") - 0.3:.2f});')
    pop(T, "#ns-gone", at("account", 2), 0.4, 1.4)
    C += [dict(t=at("trade", 2), snd="swish", gain=-15), dict(t=at("empty"), snd="riser", gain=-16), dict(t=at("account", 2), snd="impact", gain=-10)]
    return svg, T, C

def s_r():
    T, C = [], []
    base = CY + 120
    bl = f'<line x1="{CX - 320}" y1="{base}" x2="{CX + 320}" y2="{base}" {S} stroke-width="3" opacity="0.7"/>'
    neg = (f'<g id="rr-n" opacity="0"><rect x="{CX - 220}" y="{base}" width="120" height="90" fill="#fff" opacity="0.85"/>'
           f'{label(CX - 160, base + 150, "-1R", 34, "#fff", sp="0.1em", op=1)}{label(CX - 160, base + 192, "PLANNED", 28, op=1)}</g>')
    chk = f'<path id="rr-c" d="M {CX - 190} {base - 60} l 18 18 l 36 -40" {S} stroke-width="6" opacity="0"/>'
    pos = (f'<rect id="rr-p" x="{CX + 100}" y="{base - 360}" width="120" height="360" fill="{GOLD}" opacity="0"/>'
           f'{label(CX + 160, base - 390, "+3R", 46, GOLD, "rr-pl", sp="0.1em")}{label(CX + 160, base + 60, "WINNER", 28, eid="rr-w")}')
    sp = "".join(f'<circle class="rr-s" cx="{CX + 160 + dx}" cy="{base - 360 + dy}" r="5" fill="{GOLD}" opacity="0"/>'
                 for dx, dy in ((-90, -30), (90, -60), (-70, -110), (70, -140), (0, -190)))
    svg = bl + neg + chk + pos + sp + label(CX, CY - 380, "THE PRICE OF THE NEXT WIN", 28, eid="rr-t")
    fade(T, "#rr-t", at("planned") - 0.2)
    T.append(f'tl.fromTo("#rr-n", {{opacity: 0, scaleY: 0, transformOrigin: "50% 0%"}}, {{opacity: 1, scaleY: 1, duration: 0.5, ease: "power3.out"}}, {at("percent"):.2f});')
    pop(T, "#rr-c", at("valid", 2), 0.4, 0.4)
    T.append(f'tl.fromTo("#rr-p", {{opacity: 0, scaleY: 0, transformOrigin: "50% 100%"}}, {{opacity: 1, scaleY: 1, duration: 0.7, ease: "expo.out"}}, {at("3r"):.2f});')
    fade(T, "#rr-pl", at("3r") + 0.3); fade(T, "#rr-w", at("winner"))
    T.append(f'tl.fromTo(".rr-s", {{opacity: 0, scale: 0, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.3, stagger: 0.06, ease: "back.out(3)"}}, {at("3r") + 0.4:.2f});')
    C += [dict(t=at("percent"), snd="tick", gain=-12), dict(t=at("valid", 2), snd="ping", gain=-14),
          dict(t=at("3r") - 0.8, snd="riser", gain=-16), dict(t=at("3r"), snd="impact", gain=-11), dict(t=at("winner"), snd="sting", gain=-15)]
    return svg, T, C

def s_slot():
    T, C = [], []
    x0, y0 = CX - 200, CY - 250
    body = (f'<g id="sl-b" opacity="0"><rect x="{x0}" y="{y0}" width="400" height="500" rx="30" {S}/>'
            f'{label(CX, y0 + 62, "PROFIT", 30, "#fff", sp="0.3em", op=1)}'
            f'<rect x="{x0 + 40}" y="{y0 + 110}" width="320" height="140" rx="14" {S} stroke-width="3"/>'
            + "".join(f'<line x1="{x0 + 40 + k*107}" y1="{y0 + 110}" x2="{x0 + 40 + k*107}" y2="{y0 + 250}" {S} stroke-width="3"/>' for k in (1, 2))
            + f'<rect x="{x0 + 70}" y="{y0 + 300}" width="260" height="60" rx="12" {S} stroke-width="3"/>'
            f'<line x1="{x0 + 440}" y1="{y0 + 120}" x2="{x0 + 440}" y2="{y0 + 260}" {S}/><circle id="sl-k" cx="{x0 + 440}" cy="{y0 + 105}" r="18" fill="#fff"/></g>')
    reels = "".join(f'<text id="sl-r{k}" x="{x0 + 93 + k*107}" y="{y0 + 205}" text-anchor="middle" font-family="Archivo Black" font-size="64" fill="#fff" opacity="0">7</text>' for k in range(3))
    bad, L = polyline("sl-bad", [(CX - 260, CY + 330), (CX - 140, CY + 300), (CX - 40, CY + 350), (CX + 80, CY + 390), (CX + 260, CY + 450)], "#fff", 5)
    svg = body + reels + bad + label(CX + 260, CY + 510, "BAD TRADE", 28, eid="sl-bl", anchor="end")
    pop(T, "#sl-b", at("course") - 0.1, 0.5, 0.7)
    T.append(f'tl.to("[id^=sl-r]", {{opacity: 1, duration: 0.1}}, {at("course"):.2f});')
    T.append(f'tl.fromTo("#sl-k", {{y: 0}}, {{y: 120, duration: 0.25, yoyo: true, repeat: 1, ease: "power2.in"}}, {at("automatically"):.2f});')
    for k in range(3):
        T.append(f'tl.fromTo("#sl-r{k}", {{y: -30, opacity: 0.2}}, {{y: 0, opacity: 1, duration: 0.12, repeat: {6 + k*3}, ease: "none"}}, {at("automatically") + 0.1:.2f});')
    T.append(f'tl.set("#sl-r2", {{textContent: "✕"}}, {at("profitable"):.2f});')
    draw(T, "#sl-bad", L, at("bad", 1), 0.9)
    fade(T, "#sl-bl", at("bad", 2))
    C += [dict(t=at("course"), snd="pop", gain=-14), dict(t=at("automatically"), snd="glitch", gain=-18),
          dict(t=at("profitable"), snd="stamp", gain=-11), dict(t=at("bad", 1), snd="draw", gain=-15)]
    return svg, T, C

def s_scale():
    T, C = [], []
    py, bx = CY - 160, 300
    stand = (f'<g id="sc-st" opacity="0"><line x1="{CX}" y1="{py}" x2="{CX}" y2="{CY + 330}" {S}/>'
             f'<path d="M {CX - 90} {CY + 330} L {CX + 90} {CY + 330}" {S}/><circle cx="{CX}" cy="{py - 14}" r="12" {S} stroke-width="3"/></g>')
    def pan(x, eid, content, lab):
        return (f'<g id="{eid}"><line x1="{x}" y1="{py}" x2="{x - 90}" y2="{py + 200}" {S} stroke-width="3"/>'
                f'<line x1="{x}" y1="{py}" x2="{x + 90}" y2="{py + 200}" {S} stroke-width="3"/>'
                f'<path d="M {x - 110} {py + 200} Q {x} {py + 290} {x + 110} {py + 200} Z" {S}/>{content}'
                f'{label(x, py + 350, lab, 28, op=1)}</g>')
    dice = (f'<g id="sc-d" opacity="0"><rect x="{CX - bx - 45}" y="{py + 105}" width="90" height="90" rx="16" {S} stroke-width="3"/>'
            + "".join(f'<circle cx="{CX - bx + dx}" cy="{py + 150 + dy}" r="7" fill="#fff"/>' for dx, dy in ((-22, -22), (22, 22), (0, 0))) + '</g>')
    plan = (f'<g id="sc-p" opacity="0"><rect x="{CX + bx - 42}" y="{py + 85}" width="84" height="110" rx="10" {S} stroke-width="3"/>'
            + "".join(f'<path d="M {CX + bx - 26} {py + 116 + k*28} l 8 8 l 14 -14" stroke="{GOLD}" stroke-width="3" fill="none"/>' for k in range(3)) + '</g>')
    beam = (f'<g id="sc-beam" opacity="0"><line x1="{CX - bx}" y1="{py}" x2="{CX + bx}" y2="{py}" {S}/>'
            + pan(CX - bx, "sc-l", dice, "GAMBLE") + pan(CX + bx, "sc-r", plan, "PLAN") + '</g>')
    svg = stand + beam + label(CX, CY - 420, "THE DIFFERENCE", 28, eid="sc-t")
    fade(T, "#sc-t", at("important"))
    pop(T, "#sc-st", at("important"), 0.45, 0.8)
    pop(T, "#sc-beam", at("understanding"), 0.5, 0.8)
    pop(T, "#sc-d", at("gamble"), 0.4, 0.3)
    pop(T, "#sc-p", at("plan"), 0.4, 0.3)
    T.append(f'tl.to("#sc-beam", {{rotation: 10, svgOrigin: "{CX} {py}", duration: 0.9, ease: "elastic.out(1, 0.45)"}}, {at("plan") + 0.1:.2f});')
    T.append(f'tl.to("#sc-l", {{rotation: -10, svgOrigin: "{CX - bx} {py}", duration: 0.9, ease: "elastic.out(1, 0.45)"}}, {at("plan") + 0.1:.2f});')
    T.append(f'tl.to("#sc-r", {{rotation: -10, svgOrigin: "{CX + bx} {py}", duration: 0.9, ease: "elastic.out(1, 0.45)"}}, {at("plan") + 0.1:.2f});')
    C += [dict(t=at("important"), snd="swish", gain=-15), dict(t=at("gamble"), snd="pop", gain=-13),
          dict(t=at("plan"), snd="stamp", gain=-11)]
    return svg, T, C

def s_curve():
    T, C = [], []
    pts = [(CX - 330, CY + 300), (CX - 250, CY + 230), (CX - 210, CY + 260), (CX - 120, CY + 150), (CX - 80, CY + 185),
           (CX + 10, CY + 60), (CX + 50, CY + 95), (CX + 140, CY - 40), (CX + 180, CY - 5), (CX + 330, CY - 220)]
    cur, L = polyline("cv-l", pts, "#fff", 6)
    gold, _ = polyline("cv-g", pts, GOLD, 6)
    dips = [pts[2], pts[4], pts[6], pts[8]]
    dots = "".join(f'<circle class="cv-d" cx="{x}" cy="{y}" r="11" fill="#000" stroke="#fff" stroke-width="4" opacity="0"/>' for x, y in dips)
    tags = "".join(f'<text class="cv-t" x="{x}" y="{y + 50}" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="28" fill="#cfd3da" opacity="0">-1R</text>' for x, y in dips)
    axis = (f'<path d="M {CX - 360} {CY - 300} L {CX - 360} {CY + 340} L {CX + 360} {CY + 340}" {S} stroke-width="3" opacity="0.6"/>')
    svg = axis + cur + gold + dots + tags + label(CX, CY + 450, "KNOW WHICH LOSSES TO TAKE.", 28, "#fff", "cv-k", sp="0.22em")
    draw(T, "#cv-l", L, at("consistent"), 2.0)
    T.append(f'tl.fromTo(".cv-d", {{opacity: 0, scale: 0, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.3, stagger: 0.12, ease: "back.out(3)"}}, {at("never", 2):.2f});')
    T.append(f'tl.to(".cv-t", {{opacity: 1, duration: 0.3, stagger: 0.12}}, {at("lose", 2):.2f});')
    draw(T, "#cv-g", L, at("know"), 1.0)
    fade(T, "#cv-k", at("take"))
    C += [dict(t=at("consistent"), snd="draw", gain=-15), dict(t=at("never", 2), snd="tick", gain=-13),
          dict(t=at("know"), snd="riser", gain=-17), dict(t=at("take"), snd="sting", gain=-13)]
    return svg, T, C

SCENES = [  # (builder, start)
    (s_hook, 0.0), (s_crowd, at("most") - 0.25), (s_diff, at("but", 1) - 0.1), (s_trader, at("imagine") - 0.2),
    (s_habits, at("they", 1) - 0.1), (s_dome, at("protecting") - 0.3), (s_receipt, at("because", 2) - 0.1),
    (s_nostop, at("trade", 2) - 0.3), (s_r, at("but", 3) - 0.1), (s_slot, at("course") - 0.35),
    (s_scale, at("important") - 0.3), (s_curve, at("because", 3) - 0.1),
]

# ---------------------------------------------------------------------------------------------------------------------
# phrase captions under the stage
KEY = {"lose", "losses", "loss", "risk", "plan", "gamble", "profitable", "consistent", "3r", "winner", "one", "percent",
       "business", "empty", "never", "losing", "planned", "valid"}
def captions(end_t):
    M, T, phrases, cur = [], [], [], []
    for i, w in enumerate(WORDS):
        cur.append(i)
        brk = w["text"][-1] in ".,?!" or len(cur) >= 7
        if brk:
            phrases.append(cur); cur = []
    if cur: phrases.append(cur)
    for p, idx in enumerate(phrases):
        t0 = LEAD + WORDS[idx[0]]["start"] - 0.05
        t1 = (LEAD + WORDS[phrases[p + 1][0]]["start"] - 0.12) if p + 1 < len(phrases) else end_t - 0.4
        words = []
        for i in idx:
            txt = WORDS[i]["text"]
            col = GOLD if norm(txt) in KEY else "#fff"
            words.append(f'<span style="color:{col}">{txt}</span>')
        cid = f"cap{p}"
        M.append(f'<div id="{cid}" class="cap">{" ".join(words)}</div>')
        T.append(f'tl.fromTo("#{cid}", {{opacity: 0, y: 16}}, {{opacity: 1, y: 0, duration: 0.18, ease: "power2.out"}}, {t0:.2f});')
        T.append(f'tl.to("#{cid}", {{opacity: 0, duration: 0.12, ease: "none"}}, {max(t0 + 0.4, t1):.2f});')
    return M, T

OUTRO = [0.0, 1.32, 3.34, 4.09]

def build():
    vo_end = LEAD + WORDS[-1]["end"]
    end_t = round(vo_end + 0.8, 2)
    vo_o = round(end_t + 0.3, 2)
    total = round(vo_o + OUTRO[3] + 1.3, 2)
    groups, T, C = [], [], []
    for n, (fn, t_in) in enumerate(SCENES):
        svg, t, c = fn()
        t_out = SCENES[n + 1][1] if n + 1 < len(SCENES) else end_t - 0.4
        groups.append(f'<g id="sc{n}" opacity="0">{svg}</g>')
        T.append(f'tl.fromTo("#sc{n}", {{opacity: 0, scale: 0.94, filter: "blur(10px)", transformOrigin: "{CX}px {CY}px"}}, '
                 f'{{opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.45, ease: "power3.out"}}, {t_in:.2f});')
        T.append(f'tl.to("#sc{n}", {{scale: 1.035, duration: {max(0.5, t_out - t_in - 0.3):.2f}, ease: "none"}}, {t_in + 0.45:.2f});')
        T.append(f'tl.to("#sc{n}", {{opacity: 0, filter: "blur(10px)", duration: 0.3, ease: "power2.in"}}, {t_out - 0.3:.2f});')
        T += t; C += c
        if n: C.append(dict(t=t_in, snd="whip", gain=-20))
    cm, ct = captions(end_t)
    C += [dict(t=0, snd="bed", file="bed"), dict(t=LEAD, snd="vo", file="vo_main", gain=0),
          dict(t=end_t, snd="whoosh", gain=-11, align="peak"), dict(t=end_t + 0.25, snd="impact", gain=-9),
          dict(t=vo_o, snd="vo", file="vo_outro", gain=0), dict(t=vo_o + OUTRO[1], snd="pop", gain=-14),
          dict(t=vo_o + OUTRO[2], snd="stamp", gain=-12)]
    import random
    rnd = random.Random(5)
    dust = "".join(f'<circle class="dust" cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.uniform(1, 2.4):.1f}" '
                   f'fill="#fff" opacity="{rnd.uniform(0.06, 0.25):.2f}"/>' for _ in range(40))
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: {W}px; height: {H}px; overflow: hidden; background: #000; font-family: Montserrat, sans-serif; }}
      #vig {{ position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 46%, rgba(44,44,50,0.6) 0%, rgba(0,0,0,0) 58%); }}
      #stage {{ position: absolute; inset: 0; }}
      #stage svg {{ width: {W}px; height: {H}px; overflow: visible; filter: drop-shadow(0 0 6px rgba(255,255,255,0.5)); }}
      .cap {{ position: absolute; left: 70px; width: 940px; top: 1500px; text-align: center; font-size: 50px; font-weight: 800; color: #fff;
        line-height: 1.18; opacity: 0; text-shadow: 0 0 18px rgba(0,0,0,0.9); }}
      #end {{ position: absolute; inset: 0; background: #000; opacity: 0; z-index: 40; }}
      #end-logo {{ position: absolute; left: 110px; top: 470px; width: 860px; }}
      #end-tag {{ position: absolute; left: 0; width: {W}px; top: 920px; text-align: center; font-size: 44px; font-weight: 800; letter-spacing: 0.04em; color: #fff; }}
      #end-tag span {{ color: {GOLD}; }}
      #end-cta {{ position: absolute; left: 0; width: {W}px; top: 1040px; text-align: center; font-family: "Archivo Black", sans-serif; font-size: 92px; color: #fff; }}
      #end-cta span {{ color: {BLUE}; }}
      #end-note {{ position: absolute; left: 0; width: {W}px; top: 1180px; text-align: center; font-size: 28px; font-weight: 700; letter-spacing: 0.12em; color: #8a8f98; }}
      #end-foot {{ position: absolute; left: 0; top: 1665px; width: {W}px; height: 255px; overflow: hidden; }}
      #end-foot img {{ width: {W}px; height: 255px; display: block; }}
      #flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 50; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="otm-losses" data-start="0" data-duration="{total}" data-width="{W}" data-height="{H}" data-motion-blur="on">
      <div id="vig"></div>
      <div id="stage"><svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><g id="dustg">{dust}</g>
{chr(10).join(groups)}
      </svg></div>
{chr(10).join("      " + m for m in cm)}
      <div id="end">
        <img id="end-logo" src="assets/otm_logo.png" alt="Order the Market" />
        <div id="end-tag">DON'T LET THE MARKET <span>ORDER YOU</span></div>
        <div id="end-cta">FOLLOW FOR <span>MORE</span></div>
        <div id="end-note">EDUCATIONAL ONLY · NOT FINANCIAL ADVICE</div>
        <div id="end-foot"><img id="end-foot-img" src="assets/footer.jpg" alt="" /></div>
      </div>
      <div id="flash"></div>
      <audio id="otm-audio" class="clip" src="assets/audio/mix.wav" data-start="0" data-duration="{total}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
        tl.fromTo(".dust", {{ y: 0 }}, {{ y: -140, duration: {end_t}, ease: "none" }}, 0);
{chr(10).join("        " + t for t in T)}
{chr(10).join("        " + t for t in ct)}
        tl.to("#stage", {{ opacity: 0, duration: 0.3 }}, {end_t - 0.3:.2f});
        tl.fromTo("#flash", {{ opacity: 0.8 }}, {{ opacity: 0, duration: 0.35, ease: "power2.out", immediateRender: false }}, {end_t:.2f});
        tl.fromTo("#end", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.05, immediateRender: false }}, {end_t:.2f});
        tl.fromTo("#end-logo", {{ opacity: 0, scale: 2.2, filter: "blur(14px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.5, ease: "expo.out" }}, {end_t + 0.1:.2f});
        tl.fromTo("#end-tag", {{ opacity: 0, y: 30, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.4, ease: "expo.out" }}, {vo_o + OUTRO[1]:.2f});
        tl.fromTo("#end-cta", {{ opacity: 0, clipPath: "inset(0% 100% 0% 0%)" }}, {{ opacity: 1, clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power3.out" }}, {vo_o + OUTRO[2]:.2f});
        tl.fromTo("#end-note", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {end_t + 1.0:.2f});
        tl.fromTo("#end-foot-img", {{ y: 255 }}, {{ y: 0, duration: 0.5, ease: "back.out(1.2)" }}, {end_t + 0.9:.2f});
        window.__timelines["otm-losses"] = tl;
      }})();
    </script>
  </body>
</html>
"""
    open(f"{ROOT}/index.html", "w").write(html)
    json.dump(dict(total=total, cues=sorted(C, key=lambda c: c["t"])), open(f"{ROOT}/work/cues.json", "w"), indent=1)
    print("total", total, "end card", end_t, "scenes", [round(t, 2) for _, t in SCENES])

if __name__ == "__main__":
    build()
