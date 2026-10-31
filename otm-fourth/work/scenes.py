"""Scenes of "The fourth trader": three traders the market orders around, and the one who orders it.
Each scene returns (svg, timeline, cues). Cue `snd` names are earshot kit roles (work/kit.json) or "file" for a
bank sound rendered with `earshot sfx render` (assets/audio/<file>.wav)."""
import math
from common import *

CY2 = 1000                       # stage centre for this film (title cards sit above it)

def candles(cls, x0, base, seq, w=40, gap=58, color="#fff"):
    """seq: (open, close) offsets above `base` (positive = up); returns svg and the candle centres"""
    out, xs = "", []
    for i, (o, c) in enumerate(seq):
        x = x0 + i * gap; xs.append(x)
        top, bot = base - max(o, c), base - min(o, c)
        col = BLUE if c >= o else color
        out += (f'<g class="{cls}" opacity="0"><line x1="{x}" y1="{top - 16}" x2="{x}" y2="{bot + 16}" stroke="{col}" stroke-width="3"/>'
                f'<rect x="{x - w / 2}" y="{top}" width="{w}" height="{max(4, bot - top)}" fill="{col}"/></g>')
    return out, xs

def puppet_strings(cls, xs, y_top, y_bot):
    return "".join(f'<line class="{cls}" x1="{x}" y1="{y_top}" x2="{x}" y2="{y_bot}" stroke="#fff" stroke-width="2" '
                   f'stroke-dasharray="{y_bot - y_top}" stroke-dashoffset="{y_bot - y_top}"/>' for x in xs)

def s_sides():
    T, C = [], []
    lx, rx = CX - 230, CX + 230
    buy = (f'<g id="sd-b" opacity="0"><path d="M {lx} {CY2 + 120} L {lx} {CY2 - 140} M {lx - 50} {CY2 - 90} L {lx} {CY2 - 140} L {lx + 50} {CY2 - 90}" '
           f'stroke="{BLUE}" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>{label(lx, CY2 + 200, "BUYERS", 28, op=1)}</g>')
    sell = (f'<g id="sd-s" opacity="0"><path d="M {rx} {CY2 - 140} L {rx} {CY2 + 120} M {rx - 50} {CY2 + 70} L {rx} {CY2 + 120} L {rx + 50} {CY2 + 70}" '
            f'stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>{label(rx, CY2 + 200, "SELLERS", 28, op=1)}</g>')
    div = f'<line id="sd-d" x1="{CX}" y1="{CY2 - 220}" x2="{CX}" y2="{CY2 + 240}" stroke="#fff" stroke-width="2" stroke-dasharray="8 10" opacity="0"/>'
    bar = f'<g id="sd-bar" opacity="0"><rect x="{CX - 260}" y="{CY2 - 330}" width="520" height="16" rx="8" fill="#fff"/>{label(CX, CY2 - 350, "THE MARKET", 28, op=1)}</g>'
    pupp = f'<g id="sd-p" opacity="0">{person(CX, CY2 + 120, 1.3)}</g>'
    strings = puppet_strings("sd-str", [CX - 26, CX, CX + 26], CY2 - 314, CY2 + 20)
    svg = div + buy + sell + bar + strings + pupp
    pop(T, "#sd-b", at("trade") - 0.1, 0.5, 0.6); pop(T, "#sd-s", at("two"), 0.5, 0.6); fade(T, "#sd-d", at("sides"))
    T.append(f'tl.to(["#sd-b", "#sd-s", "#sd-d"], {{opacity: 0.18, duration: 0.4}}, {at("looking"):.2f});')
    fade(T, "#sd-bar", at("market"))
    pop(T, "#sd-p", at("side", 1) if False else at("ordered", 1) - 0.4, 0.4, 0.6)
    T.append(f'tl.to(".sd-str", {{strokeDashoffset: 0, duration: 0.4, stagger: 0.08}}, {at("ordered", 1):.2f});')
    T.append(f'tl.to("#sd-p", {{x: 26, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut"}}, {at("around"):.2f});')
    C += [dict(t=at("trade") - 0.1, snd="pop", gain=-3), dict(t=at("two"), snd="pop", gain=-3), dict(t=at("market"), snd="land.light", gain=-2),
          dict(t=at("ordered", 1), snd="tick.crisp", gain=-2), dict(t=at("around"), snd="tock", gain=-3)]
    return svg, T, C

def s_chaser():
    T, C = [], []
    base = CY2 + 260
    seq = [(0, 30), (30, 70), (70, 130), (130, 200), (200, 290), (290, 400), (400, 360), (360, 230), (230, 90), (90, 20)]
    cs, xs = candles("ch-c", CX - 270, base, seq)
    fig = f'<g id="ch-f" opacity="0">{person(0, 0, 0.9)}</g>'
    entry = (f'<g id="ch-e" opacity="0"><circle cx="{xs[5]}" cy="{base - 410}" r="16" fill="{GOLD}"/>'
             f'{label(xs[5] - 30, base - 450, "LATE ENTRY", 28, GOLD, anchor="end", sp="0.15em", op=1)}</g>')
    exitl = label(xs[8] + 40, base - 330, "SOMEONE'S EXIT", 28, "#fff", "ch-x", anchor="start", sp="0.15em")
    svg = cs + entry + fig + exitl
    T.append(f'tl.to(".ch-c", {{opacity: 1, duration: 0.15, stagger: {{each: 0.16}}, filter: "none"}}, {at("price"):.2f});')
    T.append(f'tl.set("#ch-f", {{x: {xs[0]}, y: {base + 60}}}, {at("price"):.2f});')
    T.append(f'tl.to("#ch-f", {{opacity: 1, duration: 0.2}}, {at("price"):.2f});')
    T.append(f'tl.to("#ch-f", {{x: {xs[5]}, y: {base - 420}, duration: {at("top") - at("price"):.2f}, ease: "power1.in"}}, {at("price"):.2f});')
    pop(T, "#ch-e", at("top"), 0.4, 0.4)
    T.append(f'tl.to("#ch-f", {{y: {base - 40}, x: {xs[8]}, duration: 0.9, ease: "power3.in"}}, {at("become"):.2f});')
    pop(T, "#ch-x", at("exit"), 0.4, 1.3)
    C += [dict(t=at("price"), snd="whoosh.short", gain=-4), dict(t=at("top"), snd="click", gain=-1),
          dict(t=at("become"), snd="file", file="fall", gain=-14), dict(t=at("exit"), snd="file", file="glitch", gain=-8)]
    return svg, T, C

def s_hoper():
    T, C = [], []
    base = CY2 + 120
    seq = [(0, 40), (40, 20), (20, -40), (-40, -90), (-90, -140), (-140, -200), (-200, -270)]
    cs, xs = candles("hp-c", CX - 200, base, seq)
    entry = f'<g id="hp-e" opacity="0"><circle cx="{xs[0]}" cy="{base - 40}" r="14" fill="{GOLD}"/>{label(xs[0] - 30, base - 60, "ENTRY", 28, GOLD, anchor="end", sp="0.15em", op=1)}</g>'
    stop = (f'<g id="hp-s" opacity="0"><line x1="{CX - 300}" y1="{base + 60}" x2="{CX + 320}" y2="{base + 60}" stroke="#fff" stroke-width="3" stroke-dasharray="12 10"/>'
            f'{label(CX + 320, base + 40, "STOP", 28, anchor="end", sp="0.2em", op=1)}</g>')
    acc = (f'<g id="hp-a" opacity="0">{label(CX - 300, CY2 - 300, "ACCOUNT", 28, anchor="start", sp="0.2em", op=1)}'
           f'<rect x="{CX - 300}" y="{CY2 - 280}" width="600" height="16" rx="8" fill="#fff" opacity="0.15"/>'
           f'<rect id="hp-bar" x="{CX - 300}" y="{CY2 - 280}" width="600" height="16" rx="8" fill="#fff"/></g>')
    svg = acc + cs + entry + stop
    pop(T, "#hp-e", at("trade", 2) - 0.1, 0.4, 0.5); fade(T, "#hp-s", at("trade", 2)); fade(T, "#hp-a", at("trade", 2))
    T.append(f'tl.to(".hp-c", {{opacity: 1, duration: 0.15, stagger: 0.12}}, {at("goes"):.2f});')
    T.append(f'tl.to("#hp-s", {{y: 100, duration: 0.5, ease: "power2.inOut"}}, {at("move"):.2f});')
    T.append(f'tl.to("#hp-s", {{y: 190, duration: 0.5, ease: "power2.inOut"}}, {at("wait"):.2f});')
    T.append(f'tl.to("#hp-bar", {{scaleX: 0.25, transformOrigin: "0% 50%", duration: 1.2, ease: "power2.in"}}, {at("rarely"):.2f});')
    C += [dict(t=at("trade", 2), snd="click", gain=-2), dict(t=at("goes"), snd="whoosh.short", gain=-6), dict(t=at("move"), snd="tock", gain=-2),
          dict(t=at("wait"), snd="tock", gain=-2), dict(t=at("rarely"), snd="file", file="glitch", gain=-8), dict(t=at("does"), snd="drop", gain=-4)]
    return svg, T, C

def s_doubter():
    T, C = [], []
    lvl = CY2 + 160
    seq = [(300, 250), (250, 180), (180, 120), (120, 60), (60, 10)]
    cs, xs = candles("db-c", CX - 280, lvl, seq)
    up = [(10, 120), (120, 260), (260, 420), (420, 560)]
    us, uxs = candles("db-u", xs[-1] + 58, lvl, up)
    line = f'<line id="db-l" x1="{CX - 330}" y1="{lvl}" x2="{CX + 330}" y2="{lvl}" stroke="{GOLD}" stroke-width="4" opacity="0"/>'
    fig = f'<g id="db-f" opacity="0">{person(CX + 260, lvl + 220, 1.0)}</g>'
    q = label(CX + 260, lvl + 70, "?", 80, "#fff", "db-q", sp="0")
    miss = label(CX - 120, CY2 - 340, "MISSED", 40, "#fff", "db-m", sp="0.3em")
    svg = line + cs + us + fig + q + miss
    T.append(f'tl.to("#db-l", {{opacity: 1, duration: 0.4}}, {at("setup"):.2f});')
    T.append(f'tl.to(".db-c", {{opacity: 1, duration: 0.15, stagger: 0.14}}, {at("arrives"):.2f});')
    pop(T, "#db-f", at("hesitate") - 0.2, 0.4, 0.6); pop(T, "#db-q", at("hesitate"), 0.4, 0.4)
    T.append(f'tl.to("#db-q", {{rotation: 14, transformOrigin: "50% 80%", duration: 0.12, yoyo: true, repeat: 5}}, {at("hesitate") + 0.3:.2f});')
    T.append(f'tl.to(".db-u", {{opacity: 1, duration: 0.12, stagger: 0.1}}, {at("leave"):.2f});')
    pop(T, "#db-m", at("them", 1) if False else at("without"), 0.4, 1.3)
    C += [dict(t=at("setup"), snd="bell", gain=-6), dict(t=at("hesitate"), snd="tick", gain=-2), dict(t=at("leave"), snd="whoosh.short", gain=-3),
          dict(t=at("without"), snd="file", file="glitch", gain=-8)]
    return svg, T, C

def s_three():
    T, C = [], []
    xs = [CX - 300, CX, CX + 300]; fy = CY2 + 200
    figs = "".join(f'<g id="tr{i}" opacity="0">{person(x, fy, 1.1, "#000")}<path d="M {x - 24} {fy} L {x - 24} {fy - 22} A 24 24 0 0 1 {x + 24} {fy - 22} L {x + 24} {fy}" {S} stroke-width="3"/>'
                   f'<circle cx="{x}" cy="{fy - 66}" r="16" {S} stroke-width="3"/>{label(x, fy + 60, n, 28, op=1)}</g>'
                   for i, (x, n) in enumerate(zip(xs, ("CHASER", "HOPER", "DOUBTER"))))
    xm = "".join(xmark(f"tx{i}", x, fy - 50, 50) for i, x in enumerate(xs))
    bar = f'<g id="tb" opacity="0"><rect x="{CX - 400}" y="{CY2 - 300}" width="800" height="16" rx="8" fill="#fff"/>{label(CX, CY2 - 320, "THE MARKET", 28, op=1)}</g>'
    strs = puppet_strings("ts", [x + d for x in xs for d in (-22, 22)], CY2 - 284, fy - 90)
    svg = bar + strs + figs + xm
    for i, w in enumerate((("three", 1), ("three", 1), ("three", 1))):
        pop(T, f"#tr{i}", at("traders", 1) - 0.3 + i * 0.15, 0.4, 0.6)
    C.append(dict(t=at("traders", 1) - 0.3, snd="pop", gain=-3))
    for i in range(3):
        strike(T, C, f"tx{i}", at("mistakes") - 0.2 + i * 0.12)
    T.append(f'tl.to("[id^=tx] .xl", {{opacity: 0.3, duration: 0.4}}, {at("one"):.2f});')
    fade(T, "#tb", at("one"))
    T.append(f'tl.to(".ts", {{strokeDashoffset: 0, duration: 0.5, stagger: 0.05}}, {at("market", 3) - 0.1:.2f});')
    T.append(f'tl.to(["#tr0", "#tr1", "#tr2"], {{y: -12, duration: 0.3, yoyo: true, repeat: 3, stagger: 0.1, ease: "sine.inOut"}}, {at("decide"):.2f});')
    C += [dict(t=at("one"), snd="land.light", gain=-2), dict(t=at("market", 3), snd="tick.crisp", gain=-2), dict(t=at("decide"), snd="tock", gain=-3)]
    return svg, T, C

def s_fourth():
    T, C = [], []
    fy = CY2 + 220
    glow = f'<circle id="ft-gl" cx="{CX}" cy="{fy - 70}" r="380" fill="url(#gg)" opacity="0"/>'
    fig = f'<g id="ft-f" opacity="0">{person(CX, fy, 1.8, GOLD)}</g>'
    bar = f'<rect id="ft-b" x="{CX - 260}" y="{CY2 - 300}" width="520" height="16" rx="8" fill="#fff" opacity="0"/>'
    cut = "".join(f'<line class="ft-s" x1="{CX + d}" y1="{CY2 - 284}" x2="{CX + d}" y2="{fy - 150}" stroke="#fff" stroke-width="2" opacity="0"/>' for d in (-40, 0, 40))
    svg = glow + bar + cut + fig
    T.append(f'tl.to(["#ft-b", ".ft-s"], {{opacity: 1, duration: 0.3}}, {at("fourth"):.2f});')
    pop(T, "#ft-f", at("fourth"), 0.5, 0.6)
    T.append(f'tl.to(".ft-s", {{y: 260, rotation: 25, opacity: 0, duration: 0.7, stagger: 0.06, ease: "power2.in", transformOrigin: "50% 100%"}}, {at("different", 2):.2f});')
    T.append(f'tl.to("#ft-b", {{opacity: 0, duration: 0.5}}, {at("different", 2) + 0.3:.2f});')
    T.append(f'tl.to("#ft-gl", {{opacity: 1, duration: 0.8}}, {at("different", 2):.2f});')
    C += [dict(t=at("fourth"), snd="land", gain=-1), dict(t=at("different", 2), snd="snap", gain=0), dict(t=at("different", 2) + 0.15, snd="hit", gain=-3)]
    return svg, T, C

def s_plan():
    T, C = [], []
    lvl = CY2 + 120
    line = f'<line id="pl-l" x1="{CX - 330}" y1="{lvl}" x2="{CX + 330}" y2="{lvl}" stroke="{GOLD}" stroke-width="5" stroke-dasharray="660" stroke-dashoffset="660"/>'
    lab = label(CX + 330, lvl - 22, "LEVEL", 28, GOLD, "pl-ll", anchor="end", sp="0.2em")
    seq = [(420, 380), (380, 330), (330, 260), (260, 200), (200, 140), (140, 60), (60, 10)]
    cs, xs = candles("pl-c", CX - 330, lvl, seq, gap=52)
    stop = (f'<g id="pl-s" opacity="0"><line x1="{CX - 330}" y1="{lvl + 90}" x2="{CX + 330}" y2="{lvl + 90}" stroke="#fff" stroke-width="3" stroke-dasharray="12 10"/>'
            f'{label(CX + 330, lvl + 140, "WRONG HERE  -1R", 28, anchor="end", sp="0.12em", op=1)}</g>')
    tgt = (f'<g id="pl-t" opacity="0"><line x1="{CX - 330}" y1="{lvl - 470}" x2="{CX + 330}" y2="{lvl - 470}" stroke="{BLUE}" stroke-width="3" stroke-dasharray="12 10"/>'
           f'{label(CX + 330, lvl - 490, "TARGET  +3R", 28, BLUE, anchor="end", sp="0.12em", op=1)}</g>')
    entry = (f'<g id="pl-e" opacity="0"><path d="M {xs[-1] + 70} {lvl + 60} L {xs[-1] + 70} {lvl - 40} M {xs[-1] + 46} {lvl - 16} L {xs[-1] + 70} {lvl - 40} L {xs[-1] + 94} {lvl - 16}" '
             f'stroke="{GOLD}" stroke-width="6" fill="none" stroke-linecap="round"/></g>')
    up = [(10, 140), (140, 300), (300, 470)]
    us, _ = candles("pl-u", xs[-1] + 52, lvl, up, gap=52)
    stamp = (f'<g id="pl-x" opacity="0"><rect x="{CX - 190}" y="{CY2 - 330}" width="380" height="96" rx="12" fill="none" stroke="{GOLD}" stroke-width="5"/>'
             f'<text x="{CX}" y="{CY2 - 264}" text-anchor="middle" font-family="Archivo Black" font-size="56" letter-spacing="0.08em" fill="{GOLD}">EXECUTE</text></g>')
    svg = line + lab + stop + tgt + cs + us + entry + stamp
    draw(T, "#pl-l", 660, at("mark"), 0.7); fade(T, "#pl-ll", at("level", 2))
    T.append(f'tl.to(".pl-c", {{opacity: 0.35, duration: 0.15, stagger: 0.1}}, {at("before", 1):.2f});')
    fade(T, "#pl-s", at("wrong", 2)); pop(T, "#pl-e", at("enter"), 0.4, 0.5); fade(T, "#pl-t", at("enter") + 0.3)
    T.append(f'tl.to(".pl-c", {{opacity: 1, duration: 0.2, stagger: 0.06}}, {at("arrives", 2):.2f});')
    T.append(f'tl.to(".pl-u", {{opacity: 1, duration: 0.15, stagger: 0.18}}, {at("execute"):.2f});')
    T.append(f'tl.fromTo("#pl-x", {{opacity: 0, scale: 1.8, rotation: -8, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, rotation: -4, duration: 0.25, ease: "power4.in"}}, {at("execute"):.2f});')
    C += [dict(t=at("mark"), snd="whoosh.short", gain=-5), dict(t=at("level", 2), snd="tick", gain=-2), dict(t=at("wrong", 2), snd="tock", gain=-2),
          dict(t=at("enter"), snd="click.confirm", gain=-2), dict(t=at("arrives", 2), snd="tick.crisp", gain=-2),
          dict(t=at("execute") + 0.25, snd="land", gain=2), dict(t=at("execute") + 0.3, snd="bell", gain=-4)]
    return svg, T, C

def s_order():
    T, C = [], []
    a = (f'<text id="or-a" x="{CX}" y="{CY2 - 60}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="54" letter-spacing="0.12em" fill="#fff" opacity="0">ORDERED BY THE MARKET</text>'
         f'<line id="or-st" x1="{CX - 380}" y1="{CY2 - 78}" x2="{CX + 380}" y2="{CY2 - 78}" stroke="#fff" stroke-width="5" stroke-dasharray="760" stroke-dashoffset="760"/>')
    b = f'<text id="or-b" x="{CX}" y="{CY2 + 110}" text-anchor="middle" font-family="Archivo Black" font-size="120" fill="{GOLD}" opacity="0">ORDERING IT</text>'
    svg = a + b
    T.append(f'tl.fromTo("#or-a", {{opacity: 0, filter: "blur(10px)"}}, {{opacity: 1, filter: "blur(0px)", duration: 0.5}}, {at("being", 2):.2f});')
    draw(T, "#or-st", 760, at("and", 99) if False else at("ordering") - 0.5, 0.35)
    T.append(f'tl.to("#or-a", {{opacity: 0.35, duration: 0.3}}, {at("ordering") - 0.3:.2f});')
    T.append(f'tl.fromTo("#or-b", {{opacity: 0, scale: 1.5, filter: "blur(16px)", transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.45, ease: "expo.out"}}, {at("ordering"):.2f});')
    C += [dict(t=at("being", 2), snd="whoosh.short", gain=-5), dict(t=at("ordering") - 0.5, snd="tock", gain=-2), dict(t=at("ordering"), snd="hit", gain=-1)]
    return svg, T, C

SCENES = [(s_sides, 0.0), (s_chaser, at("first") - 0.2), (s_hoper, at("then", 1) - 0.2), (s_doubter, at("then", 2) - 0.2),
          (s_three, at("three", 1) - 0.25), (s_fourth, at("fourth") - 0.3), (s_plan, at("mark") - 0.3), (s_order, at("that's", 2) - 0.2)]
# kinetic title cards over the stage: (id, number, name, start word, end word, glitch?)
TITLES = [("t1", "01", "THE CHASER", ("first", 1), ("then", 1), True), ("t2", "02", "THE HOPER", ("then", 1), ("then", 2), True),
          ("t3", "03", "THE DOUBTER", ("then", 2), ("three", 1), True), ("t4", "04", "THE ONE WHO ORDERS", ("fourth", 1), ("that's", 2), False)]
KEY = {"chaser", "hoper", "doubter", "exit", "stop", "level", "fourth", "different", "execute", "ordering", "market", "wrong", "mistakes"}
