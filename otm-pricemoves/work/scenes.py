"""Scenes of the "why price moves" film. Each returns (svg, timeline, cues); cue `snd` names are roles of the
earshot kit (work/kit.json), placed by work/mix_kit.py."""
import math
from common import *

def s_chase():
    T, C = [], []
    gy = CY + 120
    ground = f'<line x1="60" y1="{gy}" x2="1020" y2="{gy}" stroke="#fff" stroke-width="2" stroke-dasharray="14 12" opacity="0.5"/>'
    speed = "".join(f'<line class="ch-sp" x1="{x}" y1="{y}" x2="{x + w}" y2="{y}" stroke="#fff" stroke-width="2" opacity="0.35"/>'
                    for x, y, w in ((120, gy - 160, 160), (200, gy - 90, 220), (90, gy - 30, 120), (640, gy - 200, 180), (720, gy - 60, 160)))
    fig = f'<g id="ch-fig">{person(0, 0, 1.4)}</g>'
    coin = (f'<g id="ch-coin"><circle cx="0" cy="0" r="62" fill="#fff"/>'
            f'<text x="0" y="22" text-anchor="middle" font-family="Archivo Black" font-size="64" fill="#000">$</text></g>')
    glow = f'<circle id="ch-glow" cx="0" cy="0" r="200" fill="url(#gl)" opacity="0.9"/>'
    svg = ground + speed + f'<g id="ch-cg">{glow}{coin}</g>' + fig
    T.append(f'tl.set("#ch-fig", {{x: 260, y: {gy}}}, 0);')
    T.append(f'tl.set("#ch-cg", {{x: 640, y: {gy - 120}}}, 0);')
    T.append(f'tl.to("#ch-fig", {{x: 520, duration: {at("from") - 0.2:.2f}, ease: "none"}}, 0.2);')
    T.append(f'tl.to("#ch-cg", {{x: 880, duration: {at("from") - 0.2:.2f}, ease: "none"}}, 0.2);')
    T.append(f'tl.fromTo("#ch-fig", {{y: {gy}}}, {{y: {gy - 14}, duration: 0.16, yoyo: true, repeat: 15, ease: "sine.inOut", immediateRender: false}}, 0.2);')
    T.append(f'tl.fromTo("#ch-coin", {{scaleX: 1}}, {{scaleX: 0.08, duration: 0.18, yoyo: true, repeat: 9, ease: "sine.inOut", svgOrigin: "0 0"}}, {at("profit"):.2f});')
    T.append(f'tl.fromTo(".ch-sp", {{x: 80}}, {{x: -120, duration: 0.6, repeat: 6, ease: "none"}}, 0.2);')
    C += [dict(t=0.2, snd="whoosh.long", gain=-4), dict(t=at("profit"), snd="tick.crisp", gain=-2),
          dict(t=at("harder"), snd="tick.crisp", gain=-2)]
    return svg, T, C

def s_goal():
    T, C = [], []
    figs = "".join(f'<g class="gl-f" opacity="0">{person(CX - 360 + i * 80, CY + 300, 0.8)}</g>' for i in range(10))
    rays = "".join(f'<line class="gl-r" x1="{CX - 360 + i * 80}" y1="{CY + 220}" x2="{CX}" y2="{CY - 70}" stroke="#fff" stroke-width="1.5" opacity="0"/>' for i in range(10))
    cnt = (f'{label(CX, CY - 200, "HOW MUCH I WANT", 28, eid="gl-l")}'
           f'<text id="gl-n" x="{CX}" y="{CY - 100}" text-anchor="middle" font-family="Archivo Black" font-size="92" fill="#fff" opacity="0">$0</text>')
    svg = rays + figs + cnt
    T.append(f'tl.fromTo(".gl-f", {{opacity: 0, y: 20}}, {{opacity: 1, y: 0, duration: 0.3, stagger: 0.05, ease: "back.out(2)"}}, {at("most"):.2f});')
    T.append(f'tl.to(".gl-r", {{opacity: 0.5, duration: 0.3, stagger: 0.04}}, {at("thinking"):.2f});')
    fade(T, "#gl-l", at("thinking")); fade(T, "#gl-n", at("thinking"))
    t0, d = at("how"), at("make") - at("how") + 0.3
    for k in range(25):                                    # a counter made of set steps: seeking any frame shows a formatted value
        f = (k / 24) ** 2.2
        T.append(f'tl.set("#gl-n", {{textContent: "${round(f * 1000000):,}"}}, {t0 + d * k / 24:.2f});')
    C += [dict(t=at("most"), snd="pop", gain=-3), dict(t=at("thinking"), snd="land.light", gain=-2),
          dict(t=at("make") + 0.3, snd="hit", gain=-5)]
    return svg, T, C

def s_iceberg():
    T, C = [], []
    wl = CY - 40
    tip = f'<path id="ib-tip" d="M {CX - 150} {wl} L {CX - 30} {wl - 190} L {CX + 40} {wl - 130} L {CX + 160} {wl}" {S} fill="#000"/>'
    under = (f'<path id="ib-und" d="M {CX - 150} {wl} L {CX - 320} {wl + 160} L {CX - 250} {wl + 420} L {CX + 40} {wl + 540} L {CX + 300} {wl + 400} '
             f'L {CX + 330} {wl + 150} L {CX + 160} {wl}" fill="#fff" fill-opacity="0.05" stroke="#fff" stroke-width="3" stroke-dasharray="6 10" opacity="0"/>')
    water = f'<path d="M 60 {wl} Q 300 {wl - 12} 540 {wl} T 1020 {wl}" {S} stroke-width="3"/>'
    svg = (under + tip + water + label(CX + 5, wl - 40, "PROFIT", 30, "#fff", "ib-p", sp="0.2em")
           + label(CX, wl + 290, "ORDER FLOW", 40, GOLD, "ib-v", sp="0.25em"))
    fade(T, "#ib-p", at("instead") - 0.1)
    T.append(f'tl.fromTo("#ib-und", {{opacity: 0, y: -40}}, {{opacity: 1, y: 0, duration: 0.9, ease: "power2.out"}}, {at("understanding"):.2f});')
    pop(T, "#ib-v", at("moves"), 0.5, 0.7)
    C += [dict(t=at("instead"), snd="whoosh.short", gain=-3), dict(t=at("understanding"), snd="land", gain=-2),
          dict(t=at("moves"), snd="bell", gain=-6)]
    return svg, T, C

def s_scale():
    T, C = [], []
    py, bx = CY - 120, 300
    stand = f'<line x1="{CX}" y1="{py}" x2="{CX}" y2="{CY + 330}" {S}/><path d="M {CX - 90} {CY + 330} L {CX + 90} {CY + 330}" {S}/>'
    def pan(x, eid, lab, n):
        crowd = "".join(person(x - 50 + (i % 3) * 50, py + 190 - (i // 3) * 46, 0.55) for i in range(n))
        return (f'<g id="{eid}"><line x1="{x}" y1="{py}" x2="{x - 90}" y2="{py + 200}" {S} stroke-width="3"/>'
                f'<line x1="{x}" y1="{py}" x2="{x + 90}" y2="{py + 200}" {S} stroke-width="3"/>'
                f'<path d="M {x - 110} {py + 200} Q {x} {py + 290} {x + 110} {py + 200} Z" {S}/>{crowd}{label(x, py + 350, lab, 28, op=1)}</g>')
    beam = f'<g id="sc-beam"><line x1="{CX - bx}" y1="{py}" x2="{CX + bx}" y2="{py}" {S}/>' + pan(CX - bx, "sc-l", "BUYERS", 3) + pan(CX + bx, "sc-r", "SELLERS", 6) + '</g>'
    q = label(CX, CY - 400, "?", 90, "#fff", "sc-q", sp="0")
    forced = label(CX, CY - 400, "FORCED TO ACT", 34, GOLD, "sc-f", sp="0.22em")
    svg = f'<g id="sc-all" opacity="0">{stand}{beam}</g>' + q + forced
    pop(T, "#sc-q", at("doesn't"), 0.4, 0.4)
    T.append(f'tl.to("#sc-q", {{opacity: 0, duration: 0.2}}, {at("moves", 2) - 0.2:.2f});')
    pop(T, "#sc-all", at("moves", 2), 0.5, 0.8)
    for sel, ang, ox in (("#sc-beam", -12, CX), ("#sc-l", 12, CX - bx), ("#sc-r", 12, CX + bx)):
        T.append(f'tl.fromTo("{sel}", {{rotation: 0, svgOrigin: "{ox} {py}"}}, {{rotation: {ang}, svgOrigin: "{ox} {py}", duration: 0.5, yoyo: true, repeat: 1, ease: "sine.inOut"}}, {at("disagree"):.2f});')
        T.append(f'tl.to("{sel}", {{rotation: {-ang * 1.4}, svgOrigin: "{ox} {py}", duration: 0.8, ease: "elastic.out(1, 0.45)"}}, {at("forced"):.2f});')
    pop(T, "#sc-f", at("forced"), 0.45, 1.3)
    C += [dict(t=at("doesn't"), snd="tock", gain=-4), dict(t=at("disagree"), snd="tick", gain=-2),
          dict(t=at("forced"), snd="land", gain=0), dict(t=at("act"), snd="snap", gain=-3)]
    return svg, T, C

def s_lens():
    T, C = [], []
    pts = [(CX - 300, CY + 160), (CX - 200, CY + 60), (CX - 120, CY + 120), (CX - 20, CY - 40), (CX + 60, CY + 20), (CX + 160, CY - 140), (CX + 300, CY - 60)]
    line, L = polyline("ln-c", pts, "#fff", 4)
    lens = "".join(f'<circle cx="{CX + dx}" cy="{CY}" r="120" {S} stroke-width="6"/>' for dx in (-135, 135))
    glasses = (f'<g id="ln-g" opacity="0">{lens}<path d="M {CX - 15} {CY - 10} Q {CX} {CY - 30} {CX + 15} {CY - 10}" {S} stroke-width="6"/>'
               f'<line x1="{CX - 255}" y1="{CY - 20}" x2="{CX - 330}" y2="{CY - 60}" {S} stroke-width="6"/>'
               f'<line x1="{CX + 255}" y1="{CY - 20}" x2="{CX + 330}" y2="{CY - 60}" {S} stroke-width="6"/></g>')
    svg = line + glasses
    draw(T, "#ln-c", L, at("understanding", 2), 1.0)
    T.append(f'tl.fromTo("#ln-g", {{opacity: 0, y: 260, scale: 0.7, transformOrigin: "50% 50%"}}, {{opacity: 1, y: 0, scale: 1, duration: 0.7, ease: "power3.out"}}, {at("changes"):.2f});')
    T.append(f'tl.to("#ln-c", {{stroke: "{GOLD}", duration: 0.4}}, {at("chart"):.2f});')
    C += [dict(t=at("understanding", 2), snd="whoosh.short", gain=-3), dict(t=at("changes"), snd="land.light", gain=-1),
          dict(t=at("chart"), snd="bell", gain=-6)]
    return svg, T, C

def s_orders():
    T, C = [], []
    base = CY + 260
    cs = [(-300, 0, -60), (-230, -60, -20), (-160, -20, -110), (-90, -110, -70), (-20, -70, -170), (50, -170, -130)]
    candles = "".join(f'<rect class="od-c" x="{CX + x - 22}" y="{base + min(o, c)}" width="44" height="{abs(c - o)}" fill="#fff" opacity="0"/>'
                      f'<line class="od-c" x1="{CX + x}" y1="{base + min(o, c) - 18}" x2="{CX + x}" y2="{base + max(o, c) + 18}" {S} stroke-width="3" opacity="0"/>' for x, o, c in cs)
    hi = base - 170
    lvl = f'<line id="od-lv" x1="{CX - 330}" y1="{hi - 30}" x2="{CX + 330}" y2="{hi - 30}" stroke="{GOLD}" stroke-width="3" stroke-dasharray="10 10" opacity="0"/>'
    stops = "".join(f'<g class="od-s" opacity="0">{person(CX - 260 + i * 70, hi - 40, 0.5)}</g>' for i in range(8))
    spike = f'<rect id="od-sp" x="{CX + 128 - 22}" y="{hi - 300}" width="44" height="{base - 130 - (hi - 300)}" fill="{GOLD}" opacity="0"/>'
    svg = candles + lvl + stops + spike + label(CX - 200, hi - 120, "ORDERS WAITING", 30, GOLD, "od-l", sp="0.25em")
    T.append(f'tl.to(".od-c", {{opacity: 1, duration: 0.2, stagger: 0.08}}, {at("every") - 0.1:.2f});')
    T.append(f'tl.to("#od-lv", {{opacity: 1, duration: 0.4}}, {at("orders"):.2f});')
    T.append(f'tl.fromTo(".od-s", {{opacity: 0, y: -20}}, {{opacity: 1, y: 0, duration: 0.25, stagger: 0.05, ease: "back.out(2)"}}, {at("waiting"):.2f});')
    fade(T, "#od-l", at("waiting"))
    T.append(f'tl.fromTo("#od-sp", {{opacity: 0, scaleY: 0, transformOrigin: "50% 100%"}}, {{opacity: 1, scaleY: 1, duration: 0.5, ease: "expo.out"}}, {at("somewhere"):.2f});')
    C += [dict(t=at("every"), snd="whoosh.short", gain=-4), dict(t=at("orders"), snd="tick", gain=-2)]
    C += [dict(t=at("waiting") + i * 0.05, snd="key", gain=-6) for i in range(0, 8, 2)]
    C += [dict(t=at("somewhere"), snd="hit", gain=-4)]
    return svg, T, C

def s_network():
    T, C = [], []
    hub = (f'<g id="nw-h" opacity="0"><circle cx="{CX}" cy="{CY}" r="95" {S}/>'
           f'{label(CX, CY + 10, "LIQUIDITY", 28, "#fff", sp="0.18em", op=1)}</g>')
    sats = [("nw0", CX - 260, CY - 300, "STOPS ABOVE", "HIGHS", "stop"), ("nw1", CX + 260, CY - 300, "LIMIT", "ORDERS", "limit"),
            ("nw2", CX, CY + 340, "TRAPPED", "TRADERS", "trapped")]
    out = ""
    for eid, x, y, a, b, w in sats:
        L = round(math.dist((CX, CY), (x, y)) - 160)
        ly = y - 140 if y < CY else y + 115
        ang = math.atan2(y - CY, x - CX)
        x0, y0 = CX + 95 * math.cos(ang), CY + 95 * math.sin(ang)
        x1, y1 = x - 70 * math.cos(ang), y - 70 * math.sin(ang)
        out += (f'<line id="{eid}-ln" x1="{x0:.0f}" y1="{y0:.0f}" x2="{x1:.0f}" y2="{y1:.0f}" {S} stroke-width="3" stroke-dasharray="{L}" stroke-dashoffset="{L}"/>'
                f'<g id="{eid}" opacity="0"><circle cx="{x}" cy="{y}" r="70" {S}/>'
                f'<circle cx="{x}" cy="{y}" r="16" fill="{GOLD}"/>{label(x, ly, a, 28, op=1)}{label(x, ly + 35, b, 28, op=1)}</g>')
        draw(T, f"#{eid}-ln", L, at(w) - 0.15, 0.35)
        pop(T, f"#{eid}", at(w), 0.45, 0.4)
        C.append(dict(t=at(w), snd="pop", gain=-2))
    svg = hub + out
    pop(T, "#nw-h", at("sometimes") - 0.1, 0.5, 0.6)
    C.insert(0, dict(t=at("sometimes"), snd="land", gain=-2))
    return svg, T, C

def s_simple():
    T, C = [], []
    lx, rx = CX - 230, CX + 230
    spag = "".join(f'<path d="M {lx - 140} {CY - 60 + k*30} C {lx - 60} {CY - 160 + k*60}, {lx + 20} {CY + 80 - k*40}, {lx + 140} {CY - 80 + k*35}" '
                   f'stroke="#fff" stroke-width="2.5" fill="none" opacity="{0.4 + k*0.12:.2f}"/>' for k in range(5))
    gears = "".join(f'<circle cx="{lx + dx}" cy="{CY - 200 + dy}" r="{r}" {S} stroke-width="3" stroke-dasharray="6 6"/>' for dx, dy, r in ((-40, 0, 40), (30, 30, 28)))
    left = f'<g id="sm-l" opacity="0">{spag}{gears}{label(lx, CY + 150, "COMPLICATED", 28, op=1)}</g>'
    right = (f'<g id="sm-r" opacity="0"><line x1="{rx - 140}" y1="{CY}" x2="{rx + 140}" y2="{CY}" stroke="{GOLD}" stroke-width="5"/>'
             f'<circle id="sm-dot" cx="{rx}" cy="{CY}" r="12" fill="{GOLD}"/>{label(rx, CY + 150, "ONE LEVEL", 28, op=1)}</g>')
    div = f'<line x1="{CX}" y1="{CY - 260}" x2="{CX}" y2="{CY + 200}" stroke="#fff" stroke-width="2" stroke-dasharray="6 10" opacity="0.4"/>'
    def meter(x, eid, lab, v):
        return (f'{label(x - 140, CY + 230, lab, 28, anchor="start", sp="0.12em", op=1)}'
                f'<rect x="{x - 140}" y="{CY + 250}" width="280" height="10" rx="5" fill="#fff" opacity="0.15"/>'
                f'<rect id="{eid}" x="{x - 140}" y="{CY + 250}" width="{280 * v:.0f}" height="10" rx="5" fill="#fff"/>')
    meters = f'<g id="sm-m" opacity="0">{meter(lx, "sm-m1", "EDGE", 0.2)}{meter(rx, "sm-m2", "EDGE", 0.92)}</g>'
    ring = f'<circle id="sm-ring" cx="{rx}" cy="{CY}" r="125" stroke="{GOLD}" stroke-width="3" fill="none" opacity="0"/>'
    fig = f'<g id="sm-fig" opacity="0">{person(rx + 175, CY + 20, 0.9)}</g>'
    svg = div + left + right + meters + ring + fig
    pop(T, "#sm-l", at("complicated"), 0.5, 0.7)
    pop(T, "#sm-r", at("ones", 2), 0.5, 0.7)
    fade(T, "#sm-m", at("understand") - 0.6)
    T.append(f'tl.fromTo(["#sm-m1", "#sm-m2"], {{scaleX: 0, transformOrigin: "0% 50%"}}, {{scaleX: 1, duration: 0.8, ease: "power2.out"}}, {at("understand") - 0.5:.2f});')
    T.append(f'tl.fromTo("#sm-ring", {{opacity: 0, scale: 0.5, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.6, ease: "expo.out"}}, {at("forced", 2):.2f});')
    pop(T, "#sm-fig", at("trade"), 0.4, 0.4)
    C += [dict(t=at("complicated"), snd="tock", gain=-3), dict(t=at("ones", 2), snd="land.light", gain=-1),
          dict(t=at("forced", 2), snd="bell", gain=-5), dict(t=at("trade"), snd="pop", gain=-2)]
    return svg, T, C

def s_behavior():
    import random
    T, C = [], []
    rnd = random.Random(3)
    nodes = [(rnd.uniform(CX - 380, CX + 380), rnd.uniform(CY - 300, CY + 300)) for _ in range(26)]
    figs = "".join(f'<g class="bh-f" opacity="0">{person(x, y, 0.55)}</g>' for x, y in nodes)
    links = ""
    for i, (x, y) in enumerate(nodes):
        j = min((k for k in range(len(nodes)) if k != i), key=lambda k: math.dist(nodes[k], (x, y)))
        links += f'<line class="bh-l" x1="{x:.0f}" y1="{y - 20:.0f}" x2="{nodes[j][0]:.0f}" y2="{nodes[j][1] - 20:.0f}" stroke="#fff" stroke-width="1.5" opacity="0"/>'
    br = "".join(f'<path d="M {x} {y + dy} L {x} {y} L {x + dx} {y}" {S} stroke-width="3"/>'
                 for x, y, dx, dy in ((CX - 420, CY - 360, 50, 50), (CX + 420, CY - 360, -50, 50), (CX - 420, CY + 360, 50, -50), (CX + 420, CY + 360, -50, -50)))
    edge = (f'<g id="bh-e" opacity="0"><rect x="{CX - 110}" y="{CY - 470}" width="220" height="62" rx="31" fill="#fff"/>'
            f'<text x="{CX}" y="{CY - 428}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" letter-spacing="0.2em" fill="#000">EDGE</text></g>')
    svg = links + figs + f'<g id="bh-br" opacity="0">{br}</g>' + label(CX - 400, CY - 380, "TRADER BEHAVIOR", 28, eid="bh-t", anchor="start", sp="0.2em") + edge
    T.append(f'tl.fromTo(".bh-f", {{opacity: 0, scale: 0, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.3, stagger: 0.03, ease: "back.out(2)"}}, {at("this", 2):.2f});')
    T.append(f'tl.to("#bh-br", {{opacity: 1, duration: 0.4}}, {at("trader", 1) - 0.2:.2f});')
    fade(T, "#bh-t", at("behavior"))
    T.append(f'tl.to(".bh-l", {{opacity: 0.45, duration: 0.2, stagger: 0.03}}, {at("behavior"):.2f});')
    pop(T, "#bh-e", at("edge"), 0.45, 0.5)
    C += [dict(t=at("this", 2), snd="whoosh.long", gain=-5), dict(t=at("behavior"), snd="tick", gain=-3), dict(t=at("edge"), snd="hit", gain=-3)]
    return svg, T, C

def s_venn():
    T, C = [], []
    r = 190
    cs = [("vn0", CX, CY - 120, "GET IN", "in"), ("vn1", CX - 130, CY + 100, "PANIC", "panic"), ("vn2", CX + 130, CY + 100, "FORCED OUT", "out")]
    out = ""
    for eid, x, y, lab, w in cs:
        ly = y - 60 if eid == "vn0" else y + 90
        lx = x if eid == "vn0" else (x - 60 if eid == "vn1" else x + 60)
        out += f'<g id="{eid}" opacity="0"><circle cx="{x}" cy="{y}" r="{r}" fill="#fff" fill-opacity="0.06" {S.replace("fill=\"none\" ", "")}/>{label(lx, ly, lab, 28, op=1)}</g>'
        pop(T, f"#{eid}", at(w) - 0.1, 0.5, 0.6)
        C.append(dict(t=at(w) - 0.1, snd="pop", gain=-3))
    core = f'<circle id="vn-c" cx="{CX}" cy="{CY + 30}" r="40" fill="{GOLD}" opacity="0"/>'
    tag = (f'<g id="vn-t" opacity="0"><rect x="{CX + 120}" y="{CY - 420}" width="320" height="62" rx="31" fill="{GOLD}"/>'
           f'<text x="{CX + 280}" y="{CY - 378}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" letter-spacing="0.16em" fill="#000">OPPORTUNITY</text>'
           f'<line x1="{CX + 200}" y1="{CY - 358}" x2="{CX + 30}" y2="{CY + 0}" stroke="{GOLD}" stroke-width="3"/></g>')
    svg = out + core + tag
    T.append(f'tl.fromTo("#vn-c", {{opacity: 0, scale: 0, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.5, ease: "back.out(3)"}}, {at("easier"):.2f});')
    pop(T, "#vn-t", at("opportunity"), 0.45, 0.6)
    C += [dict(t=at("easier"), snd="bell", gain=-5), dict(t=at("opportunity"), snd="hit", gain=-3)]
    return svg, T, C

def s_ne():
    T, C = [], []
    svg = (f'<text id="ne-a" x="{CX}" y="{CY - 40}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="76" letter-spacing="0.18em" fill="#fff" opacity="0">PROFITABLE</text>'
           f'<text id="ne-b" x="{CX}" y="{CY + 70}" text-anchor="middle" font-family="Archivo Black" font-size="90" fill="#fff" opacity="0">≠</text>'
           + label(CX, CY + 160, "WANTING MORE MONEY", 34, "#cfd3da", "ne-c", sp="0.22em"))
    T.append(f'tl.fromTo("#ne-a", {{opacity: 0, filter: "blur(10px)"}}, {{opacity: 1, filter: "blur(0px)", duration: 0.6}}, {at("profitable"):.2f});')
    pop(T, "#ne-b", at("isn't"), 0.4, 0.4)
    fade(T, "#ne-c", at("wanting"))
    C += [dict(t=at("profitable"), snd="whoosh.short", gain=-4), dict(t=at("isn't"), snd="snap", gain=-3)]
    return svg, T, C

def s_flow():
    import random
    T, C = [], []
    rnd = random.Random(9)
    dots = ""
    for i in range(70):
        y = rnd.uniform(CY - 330, CY + 330); x = rnd.uniform(-200, 600)
        dots += f'<circle class="fl-d" cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(2, 5):.1f}" fill="#fff" opacity="{rnd.uniform(0.25, 0.8):.2f}"/>'
    lines = "".join(f'<path d="M -100 {CY - 260 + k*52} C 300 {CY - 260 + k*52}, 520 {CY + 40 - (k - 5)*10}, 760 {CY + 40}" stroke="#fff" stroke-width="1" fill="none" opacity="0.18"/>' for k in range(11))
    box = (f'<g id="fl-you" opacity="0"><rect x="{CX + 200}" y="{CY - 10}" width="110" height="110" rx="14" fill="#fff"/>'
           f'<rect x="{CX + 145}" y="{CY + 110}" width="110" height="110" rx="14" {S} stroke-width="3"/>'
           f'<rect x="{CX + 255}" y="{CY + 110}" width="110" height="110" rx="14" {S} stroke-width="3"/>'
           f'{label(CX + 255, CY + 290, "YOU", 34, GOLD, sp="0.3em", op=1)}</g>')
    svg = lines + dots + box + label(CX, CY - 420, "WHY PRICE MOVES", 28, eid="fl-t", sp="0.3em")
    fade(T, "#fl-t", at("understanding", 4))
    T.append(f'tl.fromTo(".fl-d", {{x: 0}}, {{x: 620, duration: 5, ease: "power1.in", stagger: {{each: 0.04, repeat: 2}}}}, {at("it's", 3):.2f});')
    pop(T, "#fl-you", at("positioned"), 0.5, 0.6)
    C += [dict(t=at("it's", 3), snd="whoosh.long", gain=-4), dict(t=at("positioned"), snd="land", gain=0), dict(t=at("does"), snd="bell", gain=-4)]
    return svg, T, C

SCENES = [(s_chase, 0.0), (s_goal, at("most") - 0.25), (s_iceberg, at("instead") - 0.3), (s_scale, at("because", 1) - 0.2),
          (s_lens, at("and", 3) - 0.1), (s_orders, at("every") - 0.3), (s_network, at("sometimes", 1) - 0.3),
          (s_simple, at("and", 4) - 0.1), (s_behavior, at("this", 2) - 0.2), (s_venn, at("better") - 0.3),
          (s_ne, at("because", 4) - 0.2), (s_flow, at("it's", 3) - 0.2)]
KEY = {"profit", "price", "moves", "forced", "orders", "stop", "losses", "limit", "trapped", "edge", "opportunity",
       "profitable", "positioned", "panic", "behavior", "liquidity"}
