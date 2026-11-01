"""Scenes of "Start before you're ready" (fourth reference: future self, regret, the START gate), in glowing line
icons. Each returns (svg, timeline, cues); cue `snd` names are earshot kit roles (work/kit.json)."""
import math
from common import *

def s_regret():
    T, C = [], []
    gy = CY + 330
    line = f'<line x1="60" y1="{gy}" x2="1020" y2="{gy}" stroke="#fff" stroke-width="2" stroke-dasharray="10 12" opacity="0.5"/>'
    yrs = "".join(f'<g class="rg-y" opacity="0"><line x1="{120 + i * 168}" y1="{gy - 10}" x2="{120 + i * 168}" y2="{gy + 10}" {S} stroke-width="3"/>'
                  f'{label(120 + i * 168, gy + 52, str(2026 + i), 28, op=1)}</g>' for i in range(6))
    fig = f'<g id="rg-f" opacity="0">{person(0, 0, 1.0)}</g>'
    you = label(0, 0, "FUTURE YOU", 28, GOLD, "rg-l", sp="0.2em")
    py, bx = CY - 230, 260
    def pan(x, eid, lab):
        return (f'<g id="{eid}"><line x1="{x}" y1="{py}" x2="{x - 80}" y2="{py + 180}" {S} stroke-width="3"/><line x1="{x}" y1="{py}" x2="{x + 80}" y2="{py + 180}" {S} stroke-width="3"/>'
                f'<path d="M {x - 100} {py + 180} Q {x} {py + 260} {x + 100} {py + 180} Z" {S}/>{label(x, py + 310, lab, 28, op=1)}</g>')
    tickets = "".join(f'<rect class="rg-t" x="{CX + bx - 60 + (i % 3) * 40}" y="{py + 140 - (i // 3) * 30}" width="34" height="24" rx="4" {S} stroke-width="2.5" opacity="0"/>' for i in range(9))
    loss = f'<rect id="rg-ls" x="{CX - bx - 22}" y="{py + 146}" width="44" height="30" rx="5" fill="#fff" opacity="0"/>'
    scale = (f'<g id="rg-s" opacity="0"><line x1="{CX}" y1="{py}" x2="{CX}" y2="{CY + 150}" {S}/><path d="M {CX - 80} {CY + 150} L {CX + 80} {CY + 150}" {S}/>'
             f'<g id="rg-b"><line x1="{CX - bx}" y1="{py}" x2="{CX + bx}" y2="{py}" {S}/>{pan(CX - bx, "rg-pl", "LOSSES")}{pan(CX + bx, "rg-pr", "REGRET")}{loss}{tickets}</g></g>')
    svg = line + yrs + scale + fig + you
    T.append(f'tl.to(".rg-y", {{opacity: 1, duration: 0.2, stagger: 0.06}}, 0.1);')
    T.append(f'tl.set("#rg-f", {{x: 120, y: {gy}}}, 0);')
    T.append(f'tl.to("#rg-f", {{opacity: 1, duration: 0.3}}, 0.1);')
    T.append(f'tl.to("#rg-f", {{x: 960, duration: {at("took") + 0.6:.2f}, ease: "none"}}, 0.1);')
    T.append(f'tl.set("#rg-l", {{x: 0, y: 0}}, 0);')
    T.append(f'tl.fromTo("#rg-l", {{opacity: 0, x: 120, y: {gy - 120}}}, {{opacity: 1, x: 260, duration: 0.5}}, {at("future"):.2f});')
    T.append(f'tl.to("#rg-l", {{x: 900, duration: {at("took") - at("future"):.2f}, ease: "none"}}, {at("future") + 0.5:.2f});')
    pop(T, "#rg-s", at("regret") - 0.1, 0.5, 0.8)
    T.append(f'tl.to(".rg-t", {{opacity: 1, duration: 0.1, stagger: 0.06}}, {at("scared"):.2f});')
    T.append(f'tl.to("#rg-ls", {{opacity: 1, duration: 0.2}}, {at("losses"):.2f});')
    for sel, ox, ang in (("#rg-b", CX, 9), ("#rg-pl", CX - bx, -9), ("#rg-pr", CX + bx, -9)):
        T.append(f'tl.to("{sel}", {{rotation: {ang}, svgOrigin: "{ox} {py}", duration: 0.9, ease: "elastic.out(1, 0.45)"}}, {at("took"):.2f});')
    C += [dict(t=at("future"), snd="whoosh.short", gain=-5), dict(t=at("regret"), snd="land", gain=-2), dict(t=at("scared"), snd="tick", gain=-4),
          dict(t=at("losses"), snd="tock", gain=-3), dict(t=at("took"), snd="land", gain=0)]
    return svg, T, C

def s_crossroad():
    T, C = [], []
    post = (f'<g id="cr-p" opacity="0"><line x1="{CX}" y1="{CY - 360}" x2="{CX}" y2="{CY + 200}" {S}/>'
            f'<path d="M {CX - 230} {CY - 330} L {CX - 20} {CY - 330} L {CX - 20} {CY - 260} L {CX - 230} {CY - 260} L {CX - 270} {CY - 295} Z" {S} fill="#000"/>'
            f'{label(CX - 125, CY - 284, "WRONG?", 28, op=1)}'
            f'<path d="M {CX + 20} {CY - 230} L {CX + 230} {CY - 230} L {CX + 270} {CY - 195} L {CX + 230} {CY - 160} L {CX + 20} {CY - 160} Z" {S} fill="#000"/>'
            f'{label(CX + 125, CY - 184, "RIGHT?", 28, GOLD, op=1)}</g>')
    door = (f'<g id="cr-d" opacity="0"><rect x="{CX + 250}" y="{CY - 60}" width="150" height="260" {S}/>'
            f'<rect id="cr-dl" x="{CX + 250}" y="{CY - 60}" width="150" height="260" fill="{GOLD}" opacity="0.85"/>'
            f'{label(CX + 325, CY - 85, "RIGHT", 28, GOLD, op=1)}</g>')
    crowd = "".join(f'<g class="cr-c" opacity="0">{person(CX - 300 + (i % 4) * 70, CY + 200 - (i // 4) * 60, 0.75)}</g>' for i in range(8))
    svg = post + door + crowd
    T.append(f'tl.fromTo(".cr-c", {{opacity: 0, y: 20}}, {{opacity: 1, y: 0, duration: 0.25, stagger: 0.05, ease: "back.out(2)"}}, {at("most"):.2f});')
    pop(T, "#cr-p", at("afraid", 1) - 0.2, 0.45, 0.7)
    T.append(f'tl.to(".cr-c", {{x: 5, duration: 0.05, yoyo: true, repeat: 9, ease: "none"}}, {at("wrong", 1):.2f});')
    pop(T, "#cr-d", at("chance") - 0.4, 0.4, 0.6)
    T.append(f'tl.to("#cr-dl", {{scaleX: 0, transformOrigin: "100% 50%", duration: 0.9, ease: "power2.in"}}, {at("right", 1):.2f});')
    C += [dict(t=at("most"), snd="pop", gain=-4), dict(t=at("afraid", 1), snd="tock", gain=-3), dict(t=at("chance"), snd="bell", gain=-6),
          dict(t=at("right", 1) + 0.9, snd="land", gain=-1)]
    return svg, T, C

def s_waiting():
    T, C = [], []
    desk = (f'<g id="wt-d" opacity="0"><path d="M {CX - 280} {CY + 130} L {CX + 280} {CY + 130} M {CX - 240} {CY + 130} L {CX - 240} {CY + 300} M {CX + 240} {CY + 130} L {CX + 240} {CY + 300}" {S}/>'
            f'<rect x="{CX - 40}" y="{CY - 90}" width="250" height="160" rx="10" {S}/>'
            f'<polyline points="{CX - 20},{CY + 30} {CX + 30},{CY - 10} {CX + 70},{CY + 10} {CX + 120},{CY - 40} {CX + 180},{CY - 20}" {S} stroke-width="3"/>'
            f'<line x1="{CX + 85}" y1="{CY + 70}" x2="{CX + 85}" y2="{CY + 130}" {S}/></g>')
    fig = f'<g id="wt-f" opacity="0">{person(CX - 150, CY + 125, 1.1)}</g>'
    clock = (f'<g id="wt-c" opacity="0"><circle cx="{CX - 200}" cy="{CY - 320}" r="60" {S}/>'
             f'<line id="wt-h" x1="{CX - 200}" y1="{CY - 320}" x2="{CX - 200}" y2="{CY - 360}" {S} stroke-width="5"/>'
             f'<text id="wt-m" x="{CX - 110}" y="{CY - 305}" font-family="Archivo Black" font-size="54" fill="#fff">1</text>'
             f'{label(CX - 110, CY - 350, "MONTHS", 28, anchor="start", op=1)}</g>')
    bar = (f'<g id="wt-b" opacity="0">{label(CX + 40, CY - 210, "READY", 28, anchor="start", op=1)}'
           f'<rect x="{CX + 40}" y="{CY - 190}" width="260" height="14" rx="7" fill="#fff" opacity="0.15"/>'
           f'<rect id="wt-bf" x="{CX + 40}" y="{CY - 190}" width="260" height="14" rx="7" fill="{GOLD}"/>'
           f'<text id="wt-p" x="{CX + 300}" y="{CY - 212}" text-anchor="end" font-family="Montserrat" font-weight="800" font-size="28" fill="{GOLD}">0%</text></g>')
    svg = desk + fig + clock + bar
    pop(T, "#wt-d", at("watch") - 0.2, 0.45, 0.8); pop(T, "#wt-f", at("watch"), 0.4, 0.6); fade(T, "#wt-c", at("months") - 0.3)
    T.append(f'tl.fromTo("#wt-h", {{rotation: 0, svgOrigin: "{CX - 200} {CY - 320}"}}, {{rotation: 1080, svgOrigin: "{CX - 200} {CY - 320}", duration: 2.6, ease: "none"}}, {at("months"):.2f});')
    for k in range(9):
        T.append(f'tl.set("#wt-m", {{textContent: "{k + 1}"}}, {at("months") + k * 0.28:.2f});')
    fade(T, "#wt-b", at("waiting", 1))
    T.append(f'tl.fromTo("#wt-bf", {{scaleX: 0}}, {{scaleX: 0.09, transformOrigin: "0% 50%", duration: 1.6, ease: "power3.out"}}, {at("waiting", 1):.2f});')
    for k, v in enumerate((2, 4, 6, 7, 8, 9)):
        T.append(f'tl.set("#wt-p", {{textContent: "{v}%"}}, {at("waiting", 1) + k * 0.25:.2f});')
    T.append(f'tl.to("#wt-p", {{opacity: 0.3, duration: 0.15, yoyo: true, repeat: 3}}, {at("ready"):.2f});')
    C += [dict(t=at("watch"), snd="land.light", gain=-2)] + [dict(t=at("months") + k * 0.28, snd="tick", gain=-8) for k in range(0, 9, 2)]
    C += [dict(t=at("ready"), snd="tock", gain=-4)]
    return svg, T, C

def s_pile():
    T, C = [], []
    base = CY + 200
    desk = f'<path d="M {CX - 320} {base} L {CX + 320} {base}" {S}/>'
    def item(eid, y, inner, lab):
        return f'<g id="{eid}" opacity="0"><rect x="{CX - 330}" y="{y}" width="300" height="90" rx="12" {S} fill="#000"/>{inner}{label(CX - 150, y + 56, lab, 28, op=1)}</g>'
    book = f'<path d="M {CX - 310} {base - 70} l 30 -12 l 30 12 l 0 46 l -30 -12 l -30 12 Z" {S} stroke-width="3"/>'
    sq = f'<path d="M {CX - 315} {base - 150} q 12 -24 24 0 t 24 0 t 24 0" {S} stroke-width="3"/>'
    flask = f'<path d="M {CX - 300} {base - 300 + 30} l 0 18 l -14 30 l 40 0 l -14 -30 l 0 -18" {S} stroke-width="3"/>'
    stack = item("pl0", base - 95, book, "COURSE") + item("pl1", base - 190, sq, "INDICATOR") + item("pl2", base - 285, flask, "STRATEGY")
    btn = (f'<g id="pl-b" opacity="0"><rect x="{CX + 80}" y="{base - 160}" width="220" height="100" rx="22" fill="{BLUE}"/>'
           f'<text x="{CX + 190}" y="{base - 96}" text-anchor="middle" font-family="Archivo Black" font-size="44" fill="#fff">BUY</text></g>')
    cur = (f'<g id="pl-c" opacity="0"><path d="M 0 0 L 0 46 L 12 34 L 22 54 L 30 50 L 20 30 L 38 30 Z" fill="#fff" stroke="#000" stroke-width="2"/></g>')
    unc = label(CX + 190, base - 200, "UNCERTAIN", 28, GOLD, "pl-u", sp="0.2em")
    svg = desk + stack + btn + cur + unc
    for k, w in enumerate(("course", "indicator", "strategy")):
        T.append(f'tl.fromTo("#pl{k}", {{opacity: 0, y: -160}}, {{opacity: 1, y: 0, duration: 0.45, ease: "bounce.out"}}, {at(w) - 0.25:.2f});')
        C.append(dict(t=at(w) + 0.05, snd="land", gain=-3))
    pop(T, "#pl-b", at("pressing") - 0.3, 0.4, 0.6)
    T.append(f'tl.set("#pl-c", {{x: {CX + 420}, y: {base + 60}}}, {at("pressing") - 0.1:.2f});')
    T.append(f'tl.to("#pl-c", {{opacity: 1, x: {CX + 230}, y: {base - 110}, duration: 0.7, ease: "power2.out"}}, {at("pressing"):.2f});')
    T.append(f'tl.to("#pl-c", {{x: {CX + 400}, y: {base + 40}, duration: 0.5, ease: "power2.in"}}, {at("uncertain"):.2f});')
    pop(T, "#pl-u", at("uncertain"), 0.4, 0.6)
    C += [dict(t=at("pressing"), snd="whoosh.short", gain=-8), dict(t=at("uncertain"), snd="tock", gain=-3)]
    return svg, T, C

def s_sidelines():
    T, C = [], []
    bench = (f'<g id="sl-b" opacity="0"><path d="M {CX - 220} {CY + 120} L {CX + 220} {CY + 120} M {CX - 200} {CY + 120} L {CX - 200} {CY + 220} M {CX + 200} {CY + 120} L {CX + 200} {CY + 220} M {CX - 220} {CY + 40} L {CX + 220} {CY + 40}" {S}/>'
             f'{label(CX, CY + 290, "SIDELINES", 30, op=1)}</g>')
    fig = f'<g id="sl-f" opacity="0">{person(CX, CY + 115, 1.1)}</g>'
    g = (f'<g id="sl-g" opacity="0"><path d="M {CX - 120} {CY - 220} A 120 120 0 0 1 {CX + 120} {CY - 220}" {S}/>'
         f'<line id="sl-n" x1="{CX}" y1="{CY - 220}" x2="{CX - 95}" y2="{CY - 230}" stroke="{GOLD}" stroke-width="5" stroke-linecap="round"/>'
         f'{label(CX, CY - 150, "RISK 0%*", 34, "#fff", sp="0.1em", op=1)}</g>')
    star = label(CX, CY - 400, "* TIME", 40, GOLD, "sl-s", sp="0.3em")
    svg = bench + fig + g + star
    pop(T, "#sl-b", at("sitting") - 0.2, 0.45, 0.8); pop(T, "#sl-f", at("sidelines"), 0.4, 0.6); pop(T, "#sl-g", at("risking") - 0.3, 0.45, 0.6)
    pop(T, "#sl-s", at("anything") + 0.3, 0.5, 1.4)
    C += [dict(t=at("sitting"), snd="land.light", gain=-2), dict(t=at("risking"), snd="tick", gain=-3), dict(t=at("anything") + 0.3, snd="bell", gain=-5)]
    return svg, T, C

def s_hourglass():
    T, C = [], []
    w, h = 170, 280
    glass = (f'<g id="hg-g" opacity="0"><path d="M {CX - w} {CY - h} L {CX + w} {CY - h} L {CX + 14} {CY} L {CX + w} {CY + h} L {CX - w} {CY + h} L {CX - 14} {CY} Z" {S}/>'
             f'<line x1="{CX - w - 30}" y1="{CY - h}" x2="{CX + w + 30}" y2="{CY - h}" {S} stroke-width="6"/><line x1="{CX - w - 30}" y1="{CY + h}" x2="{CX + w + 30}" y2="{CY + h}" {S} stroke-width="6"/></g>')
    clips = (f'<defs><clipPath id="hg-ct"><rect id="hg-rt" x="{CX - w}" y="{CY - h + 50}" width="{2 * w}" height="{h - 58}"/></clipPath>'
             f'<clipPath id="hg-cb"><rect id="hg-rb" x="{CX - w}" y="{CY + h - 4}" width="{2 * w}" height="0"/></clipPath></defs>')
    top = clips + f'<path id="hg-t" d="M {CX - w + 40} {CY - h + 50} L {CX + w - 40} {CY - h + 50} L {CX + 10} {CY - 8} L {CX - 10} {CY - 8} Z" fill="#fff" clip-path="url(#hg-ct)"/>'
    bot = f'<path id="hg-b" d="M {CX - w + 10} {CY + h - 4} L {CX + w - 10} {CY + h - 4} L {CX} {CY + 60} Z" fill="#fff" clip-path="url(#hg-cb)"/>'
    stream = f'<line id="hg-s" x1="{CX}" y1="{CY}" x2="{CX}" y2="{CY + h - 10}" stroke="#fff" stroke-width="4" opacity="0"/>'
    svg = glass + top + bot + stream + label(CX, CY - h - 60, "EXPERIENCE", 30, GOLD, "hg-l", sp="0.3em") + label(CX, CY + h + 90, "GONE", 44, "#fff", "hg-x", sp="0.3em")
    pop(T, "#hg-g", at("every") - 0.2, 0.45, 0.8)
    T.append(f'tl.set(["#hg-t", "#hg-b"], {{opacity: 1}}, {at("every") - 0.2:.2f});')
    T.append(f'tl.to("#hg-rt", {{attr: {{y: {CY - 8}, height: 0}}, duration: 3.0, ease: "none"}}, {at("month"):.2f});')
    T.append(f'tl.to("#hg-rb", {{attr: {{y: {CY + 60}, height: {h - 64}}}, duration: 3.0, ease: "none"}}, {at("month"):.2f});')
    T.append(f'tl.to("#hg-s", {{opacity: 1, duration: 0.2}}, {at("month"):.2f});')
    T.append(f'tl.to("#hg-s", {{opacity: 0, duration: 0.2}}, {at("month") + 3.0:.2f});')
    fade(T, "#hg-l", at("experience")); pop(T, "#hg-x", at("back"), 0.4, 1.4)
    C += [dict(t=at("every"), snd="whoosh.short", gain=-5), dict(t=at("experience"), snd="tick", gain=-4), dict(t=at("back"), snd="land", gain=0)]
    return svg, T, C

def s_grid():
    T, C = [], []
    dots = ""
    for i in range(60):
        x = CX - 360 + (i % 10) * 80; y = CY - 300 + (i // 10) * 80
        dots += f'<circle class="gd-d" cx="{x}" cy="{y}" r="22" fill="none" stroke="#fff" stroke-width="3" opacity="0.25"/>'
    svg = (dots + label(CX, CY - 380, "5 YEARS · 60 MONTHS", 30, eid="gd-t", sp="0.25em")
           + label(CX - 360, CY + 260, "PREPARING", 28, anchor="start", eid="gd-p", sp="0.2em")
           + f'<g id="gd-c" opacity="0">{label(CX + 360, CY + 260, "TRADES TAKEN", 28, anchor="end", sp="0.2em", op=1)}'
             f'<text id="gd-n" x="{CX + 360}" y="{CY + 360}" text-anchor="end" font-family="Archivo Black" font-size="90" fill="{GOLD}">0</text></g>')
    fade(T, "#gd-t", at("imagine"))
    T.append(f'tl.to(".gd-d", {{fill: "#ffffff", opacity: 0.9, duration: 0.05, stagger: 0.07}}, {at("realizing"):.2f});')
    fade(T, "#gd-p", at("preparing")); fade(T, "#gd-c", at("trades", 2))
    T.append(f'tl.fromTo("#gd-n", {{scale: 1}}, {{scale: 1.4, transformOrigin: "50% 50%", duration: 0.2, yoyo: true, repeat: 1}}, {at("courage"):.2f});')
    C += [dict(t=at("imagine"), snd="whoosh.short", gain=-6)] + [dict(t=at("realizing") + k * 0.7, snd="tick", gain=-10) for k in range(6)]
    C += [dict(t=at("courage"), snd="tock", gain=-2)]
    return svg, T, C

def s_launch():
    T, C = [], []
    items = ["PLAN", "LEVELS", "RISK", "EXECUTE"]
    lst = (f'<g id="la-l" opacity="0"><rect x="{CX - 380}" y="{CY - 260}" width="380" height="440" rx="20" {S}/>'
           + "".join(f'<rect x="{CX - 340}" y="{CY - 200 + k * 95}" width="44" height="44" rx="8" {S} stroke-width="3"/>{label(CX - 270, CY - 166 + k * 95, it, 30, anchor="start", sp="0.15em", op=1)}' for k, it in enumerate(items))
           + "".join(f'<path class="la-c" d="M {CX - 332} {CY - 178 + k * 95} l 10 12 l 22 -26" stroke="{GOLD}" stroke-width="5" fill="none" opacity="0"/>' for k in range(3)) + '</g>')
    rocket = (f'<g id="la-r" opacity="0"><path d="M {CX + 220} {CY - 260} Q {CX + 280} {CY - 160} {CX + 270} {CY + 80} L {CX + 170} {CY + 80} Q {CX + 160} {CY - 160} {CX + 220} {CY - 260} Z" {S}/>'
              f'<circle cx="{CX + 220}" cy="{CY - 110}" r="22" {S} stroke-width="3"/>'
              f'<path d="M {CX + 170} {CY + 20} L {CX + 130} {CY + 120} L {CX + 175} {CY + 90} M {CX + 270} {CY + 20} L {CX + 310} {CY + 120} L {CX + 265} {CY + 90}" {S} stroke-width="3"/>'
              f'<line x1="{CX + 90}" y1="{CY + 180}" x2="{CX + 350}" y2="{CY + 180}" {S}/></g>')
    q = (f'<text id="la-q" x="{CX + 220}" y="{CY - 300}" text-anchor="middle" font-family="Playfair Display" font-style="italic" font-size="120" fill="{GOLD}" opacity="0">?</text>')
    svg = lst + rocket + q
    pop(T, "#la-l", at("not", 2) - 0.1, 0.45, 0.7); pop(T, "#la-r", at("plan"), 0.45, 0.7)
    T.append(f'tl.to(".la-c", {{opacity: 1, duration: 0.12, stagger: 0.18}}, {at("plan") + 0.2:.2f});')
    T.append(f'tl.to("#la-r", {{x: 4, duration: 0.05, yoyo: true, repeat: 11, ease: "none"}}, {at("afraid", 2):.2f});')
    pop(T, "#la-q", at("find"), 0.45, 0.4)
    C += [dict(t=at("plan") + 0.2 + k * 0.18, snd="tick.crisp", gain=-3) for k in range(3)]
    C += [dict(t=at("afraid", 2), snd="tock", gain=-4), dict(t=at("find"), snd="pop", gain=-2)]
    return svg, T, C

def s_steps():
    T, C = [], []
    st = [("DEMO", 0), ("0.01 LOT", 1), ("1% RISK", 2)]
    steps = "".join(f'<g class="sp-s" opacity="0"><rect x="{CX - 330 + k * 220}" y="{CY + 200 - k * 120}" width="220" height="{120 + k * 120}" {S} fill="#000"/>'
                    f'{label(CX - 220 + k * 220, CY + 260 - k * 120, n, 28, GOLD if k == 2 else "#cfd3da", sp="0.12em", op=1)}</g>' for n, k in st)
    shield = (f'<g id="sp-sh" opacity="0"><path d="M {CX} {CY - 400} L {CX + 80} {CY - 370} L {CX + 80} {CY - 300} Q {CX + 80} {CY - 230} {CX} {CY - 195} Q {CX - 80} {CY - 230} {CX - 80} {CY - 300} L {CX - 80} {CY - 370} Z" {S}/>'
              f'{label(CX, CY - 150, "RESPECT", 30, op=1)}</g>')
    fig = f'<g id="sp-f" opacity="0">{person(0, 0, 0.9)}</g>'
    svg = shield + steps + fig
    pop(T, "#sp-sh", at("respect") - 0.4, 0.45, 0.6)
    T.append(f'tl.fromTo(".sp-s", {{opacity: 0, y: 40}}, {{opacity: 1, y: 0, duration: 0.3, stagger: 0.15, ease: "back.out(2)"}}, {at("start", 1) - 0.2:.2f});')
    pos = [(CX - 220, CY + 200), (CX, CY + 80), (CX + 220, CY - 40)]
    T.append(f'tl.set("#sp-f", {{x: {pos[0][0]}, y: {pos[0][1]}}}, {at("start", 1):.2f});')
    T.append(f'tl.to("#sp-f", {{opacity: 1, duration: 0.2}}, {at("start", 1):.2f});')
    for k, w in ((1, "small"), (2, "little")):
        t = at(w); x0, y0 = pos[k - 1]; x1, y1 = pos[k]
        T.append(f'tl.to("#sp-f", {{x: {x1}, duration: 0.45, ease: "none"}}, {t:.2f});')
        T.append(f'tl.to("#sp-f", {{y: {min(y0, y1) - 70}, duration: 0.22, ease: "power2.out"}}, {t:.2f});')
        T.append(f'tl.to("#sp-f", {{y: {y1}, duration: 0.23, ease: "power2.in"}}, {t + 0.22:.2f});')
        C.append(dict(t=t + 0.45, snd="land.light", gain=-1))
    C += [dict(t=at("respect"), snd="bell", gain=-6), dict(t=at("start", 1), snd="pop", gain=-3)]
    return svg, T, C

def s_tree():
    T, C = [], []
    ox, oy = CX - 380, CY + 40
    lines = ""
    lv = [(ox, oy)]
    k = 0
    for d in range(1, 6):
        new = []
        for (x, y) in lv:
            for s in (-1, 1):
                nx, ny = x + 150, y + s * (240 / (2 ** (d - 1)))
                lines += f'<line class="tr-l{d}" x1="{x}" y1="{y}" x2="{nx}" y2="{ny:.0f}" stroke="#fff" stroke-width="{3 - d * 0.35:.2f}" opacity="0"/>'
                new.append((nx, ny)); k += 1
        lv = new
    fig = f'<g id="tr-f" opacity="0">{person(ox - 50, oy + 40, 0.8)}</g>'
    cnt = (f'<g id="tr-c" opacity="0">{label(CX + 380, CY - 360, "WHAT IFS", 28, anchor="end", sp="0.2em", op=1)}'
           f'<text id="tr-n" x="{CX + 380}" y="{CY - 270}" text-anchor="end" font-family="Archivo Black" font-size="80" fill="#fff">2</text></g>')
    tag = (f'<g id="tr-e" opacity="0"><rect x="{CX - 110}" y="{CY - 10}" width="240" height="70" rx="35" fill="#fff"/>'
           f'<text x="{CX + 10}" y="{CY + 37}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="32" letter-spacing="5" fill="#000">EXCUSE</text></g>')
    svg = lines + fig + cnt + tag
    pop(T, "#tr-f", at("point") - 0.3, 0.4, 0.6); fade(T, "#tr-c", at("point"))
    vals = [2, 4, 8, 16, 32, 64, 256, 1024, 4096]
    for d in range(1, 6):
        T.append(f'tl.to(".tr-l{d}", {{opacity: 0.8, duration: 0.15, stagger: 0.01}}, {at("point") + d * 0.3:.2f});')
        C.append(dict(t=at("point") + d * 0.3, snd="tick", gain=-9))
    for i, v in enumerate(vals):
        T.append(f'tl.set("#tr-n", {{textContent: "{v:,}"}}, {at("point") + i * 0.22:.2f});')
    pop(T, "#tr-e", at("excuse"), 0.45, 1.5)
    C += [dict(t=at("excuse"), snd="snap", gain=-2)]
    return svg, T, C

def s_cost():
    T, C = [], []
    base = CY + 240
    hs = [70, 130, 200, 280, 370, 470]
    bars = "".join(f'<g class="ct-b" opacity="0"><rect x="{CX - 380 + i * 130}" y="{base - h}" width="90" height="{h}" rx="6" fill="{GOLD if i == 0 else "none"}" stroke="{GOLD if i == 0 else "#fff"}" stroke-width="3"/>'
                   f'{label(CX - 335 + i * 130, base + 46, "TODAY" if i == 0 else str(2026 + i), 28, GOLD if i == 0 else "#cfd3da", sp="0.08em", op=1)}</g>' for i, h in enumerate(hs))
    svg = (f'<line x1="{CX - 400}" y1="{base}" x2="{CX + 400}" y2="{base}" {S} stroke-width="3" opacity="0.6"/>' + bars
           + label(CX, CY - 380, "COST OF A LESSON", 30, eid="ct-t", sp="0.25em")
           + f'<g id="ct-a" opacity="0"><path d="M {CX - 335} {base - 170} L {CX - 335} {base - 100} M {CX - 355} {base - 120} L {CX - 335} {base - 100} L {CX - 315} {base - 120}" stroke="{GOLD}" stroke-width="5" fill="none"/>'
             f'{label(CX - 335, base - 190, "CHEAPEST", 28, GOLD, sp="0.15em", op=1)}</g>')
    fade(T, "#ct-t", at("today") - 0.4)
    T.append(f'tl.fromTo(".ct-b", {{opacity: 0, scaleY: 0, transformOrigin: "50% 100%"}}, {{opacity: 1, scaleY: 1, duration: 0.35, stagger: 0.12, ease: "power3.out"}}, {at("today"):.2f});')
    pop(T, "#ct-a", at("cheapest"), 0.45, 0.6)
    C += [dict(t=at("today") + k * 0.12, snd="pop", gain=-7) for k in range(6)] + [dict(t=at("cheapest"), snd="bell", gain=-4)]
    return svg, T, C

def s_start():
    T, C = [], []
    gy = CY + 260
    rays = "".join(f'<line class="st-r" x1="{CX}" y1="{CY - 60}" x2="{CX + 520 * math.cos(math.radians(a)):.0f}" y2="{CY - 60 + 520 * math.sin(math.radians(a)):.0f}" stroke="{GOLD}" stroke-width="2" opacity="0"/>' for a in range(200, 345, 12))
    gate = (f'<g id="st-g" opacity="0"><rect x="{CX - 120}" y="{CY - 260}" width="240" height="{gy - (CY - 260)}" {S}/>'
            f'<rect id="st-l" x="{CX - 120}" y="{CY - 260}" width="240" height="{gy - (CY - 260)}" fill="{GOLD}" opacity="0"/>'
            f'<rect x="{CX - 150}" y="{CY - 330}" width="300" height="70" rx="10" fill="#000" stroke="#fff" stroke-width="4"/>'
            f'<text x="{CX}" y="{CY - 282}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="36" letter-spacing="10" fill="#fff">START</text></g>')
    ground = f'<line x1="60" y1="{gy}" x2="1020" y2="{gy}" stroke="#fff" stroke-width="2" opacity="0.5"/>'
    fig = f'<g id="st-f" opacity="0">{person(0, 0, 1.0)}</g>'
    svg = rays + ground + gate + fig
    pop(T, "#st-g", at("trader", 1) - 0.2, 0.5, 0.7)
    T.append(f'tl.set("#st-f", {{x: {CX - 380}, y: {gy}}}, {at("trader", 1):.2f});')
    T.append(f'tl.to("#st-f", {{opacity: 1, duration: 0.3}}, {at("trader", 1):.2f});')
    T.append(f'tl.to("#st-f", {{x: {CX}, duration: {at("started") - at("trader", 1):.2f}, ease: "power1.inOut"}}, {at("trader", 1) + 0.2:.2f});')
    T.append(f'tl.to("#st-l", {{opacity: 0.9, duration: 0.5}}, {at("started"):.2f});')
    T.append(f'tl.to(".st-r", {{opacity: 0.7, duration: 0.3, stagger: 0.03}}, {at("started"):.2f});')
    T.append(f'tl.to("#st-f", {{opacity: 0, scale: 0.7, transformOrigin: "50% 100%", duration: 0.5}}, {at("started") + 0.2:.2f});')
    C += [dict(t=at("trader", 1), snd="whoosh.long", gain=-6), dict(t=at("started"), snd="hit", gain=-2), dict(t=at("started") + 0.05, snd="bell", gain=-4)]
    return svg, T, C

SCENES = [(s_regret, 0.0), (s_crossroad, at("most") - 0.3), (s_waiting, at("they", 2) - 0.3), (s_pile, at("they", 4) - 0.25),
          (s_sidelines, at("and", 1) - 0.2), (s_hourglass, at("but", 1) - 0.2), (s_grid, at("imagine") - 0.25), (s_launch, at("not", 2) - 0.25),
          (s_steps, at("of", 2) - 0.2), (s_tree, at("but", 3) - 0.2), (s_cost, at("because", 4) - 0.2), (s_start, at("and", 3) - 0.2)]
KEY = {"regret", "scared", "losses", "wrong", "right", "ready", "buy", "uncertain", "sidelines", "risking", "experience", "courage",
       "plan", "respect", "start", "small", "risk", "little", "excuse", "today", "cheapest", "started", "afraid"}
