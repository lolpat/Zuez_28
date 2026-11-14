"""OTM "trader mindset" animation in the style of the reference: glowing line art, a staircase of steps up to a
floating goal island, and kinetic text timed to the narration's words.

Inputs: work/words.json (word timings of assets/audio/vo_main.wav), assets/audio/vo_outro.wav.
Outputs: index.html and work/cues.json (sound cues for work/mix.py).
"""
import json, math, os, random, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1080, 1920
LEAD = 0.3                                   # narration starts here
GOLD, BLUE = "#e8c26a", "#2962ff"
WORDS = json.load(open(f"{ROOT}/work/words.json"))["words"]
WORDS = [w for w in WORDS if w["type"] == "word"]
def wt(i): return LEAD + WORDS[i]["start"]
def we(i): return LEAD + WORDS[i]["end"]

# ---------------------------------------------------------------------------------------------------------------------
# Kinetic text. Lines split by " / ", one token per spoken word. Prefix: * italic serif, # heavy caps, ~ outline caps,
# ^ small tracked, ! gold bold. "+X" adds a decorative token that is not spoken (shown with the previous word).
BLOCKS = [
    "This is why / some traders *become / #PROFITABLE",
    "before they make / *any #MONEY. / +$0",
    "*Imagine / two traders",
    "who both want / to be *consistent.",
    "The first trader / sees someone with a / #WINNING #ACCOUNT",
    "and thinks they / must have been *lucky",
    "or found a / ~secret / #INDICATOR.",
    "They see profit / as something / that happens to / *other *people.",
    "The second trader / looks at the same account",
    "and starts asking / *different *questions.",
    "What #RULES / did they follow?",
    "What #LOSSES / did they *survive?",
    "And what would I / need to do / to get *there?",
    "This difference / might seem ^small,",
    "but it changes / #EVERYTHING / about how they trade.",
    "When you can see / the *steps,",
    "the *plan, / the *risk, / the *patience,",
    "the goal stops looking / ~IMPOSSIBLE",
    "and starts looking / like a #PROCESS.",
    "That's why some traders / become profitable / *in *their *head",
    "*long *before / their #ACCOUNT,",
    "because they've already / changed the way they *think",
    "*and the way they / !ACT.",
]
def norm(s): return re.sub(r"[^a-z0-9']", "", s.lower().replace("’", "'"))

def parse_blocks():
    out, k = [], 0
    for b in BLOCKS:
        lines = []
        for ln in b.split(" / "):
            toks = []
            for tok in ln.split(" "):
                if tok.startswith("+"):
                    toks.append(dict(text=tok[1:], style="#", i=k - 1, extra=True)); continue
                style = tok[0] if tok[0] in "*#~^!" else ""
                text = tok[1:] if style else tok
                assert norm(text) == norm(WORDS[k]["text"]), (text, WORDS[k]["text"], k)
                toks.append(dict(text=text, style=style, i=k)); k += 1
            lines.append(toks)
        out.append(lines)
    assert k == len(WORDS), (k, len(WORDS))
    return out

STYLE_CSS = {
    "": "font-family:Montserrat;font-weight:700;font-size:52px;color:#fff;",
    "*": "font-family:'Playfair Display';font-style:italic;font-weight:400;font-size:82px;color:#fff;",
    "#": "font-family:'Archivo Black';font-size:118px;color:#fff;text-transform:uppercase;letter-spacing:-0.01em;"
         "text-shadow:0 0 28px rgba(255,255,255,0.45);",
    "~": "font-family:'Archivo Black';font-size:112px;color:transparent;-webkit-text-stroke:2.5px #fff;text-transform:uppercase;",
    "^": "font-family:Montserrat;font-weight:600;font-size:40px;color:#cfd3da;letter-spacing:0.45em;",
    "!": f"font-family:'Archivo Black';font-size:150px;color:{GOLD};text-shadow:0 0 40px rgba(232,194,106,0.65);",
}

def text_layer(blocks, outro_t):
    M, T = [], []
    for b, lines in enumerate(blocks):
        first = [t for ln in lines for t in ln if not t.get("extra")][0]["i"]
        last = [t for ln in lines for t in ln if not t.get("extra")][-1]["i"]
        if b + 1 < len(blocks):
            nxt = [t for ln in blocks[b + 1] for t in ln if not t.get("extra")][0]["i"]
            out_t = min(wt(nxt) - 0.3, we(last) + 1.1)
        else:
            out_t = outro_t - 0.5
        bid = f"tb{b}"
        rows = []
        for li, ln in enumerate(lines):
            # long heavy lines shrink to fit
            spans = []
            for j, t in enumerate(ln):
                sid = f"{bid}w{li}_{j}"
                css = STYLE_CSS[t["style"]]
                if t["style"] in "#~":
                    chars = sum(len(x["text"]) for x in ln if x["style"] in "#~") + 1
                    css = css.replace("font-size:118px", f"font-size:{min(118, int(1380 / chars))}px").replace(
                        "font-size:112px", f"font-size:{min(112, int(1350 / chars))}px")
                spans.append(f'<span id="{sid}" class="w" style="{css}">{t["text"]}</span>')
                at = wt(t["i"]) - 0.06 + (0.25 if t.get("extra") else 0)
                if t["style"] in "#~!":
                    T.append(f'tl.fromTo("#{sid}", {{opacity: 0, scale: 1.35, filter: "blur(18px)"}}, '
                             f'{{opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.42, ease: "expo.out"}}, {at:.2f});')
                elif t["style"] == "^":
                    T.append(f'tl.fromTo("#{sid}", {{opacity: 0, scaleX: 0.55, filter: "blur(8px)"}}, '
                             f'{{opacity: 1, scaleX: 1, filter: "blur(0px)", duration: 0.6, ease: "power3.out"}}, {at:.2f});')
                else:
                    T.append(f'tl.fromTo("#{sid}", {{opacity: 0, y: 22, filter: "blur(10px)"}}, '
                             f'{{opacity: 1, y: 0, filter: "blur(0px)", duration: 0.34, ease: "power3.out"}}, {at:.2f});')
            rows.append(f'<div class="ln">{" ".join(spans)}</div>')
        M.append(f'<div id="{bid}" class="tb">{"".join(rows)}</div>')
        T.append(f'tl.to("#{bid}", {{opacity: 0, y: -26, filter: "blur(14px)", duration: 0.22, ease: "power2.in"}}, {out_t:.2f});')
    return M, T

# ---------------------------------------------------------------------------------------------------------------------
# World (scene) geometry
GY = 1700
FA, FB = (420, GY), (580, GY)
PLAT = [(640, 1520, "rules"), (700, 1385, "losses"), (750, 1250, "the plan"), (790, 1110, "risk"), (815, 975, "patience")]
ISL = (850, 820)

def figure(fid, x, y, filled, s=1.0, op=1.0):
    body = f"M {-26*s:.1f} 0 L {-26*s:.1f} {-26*s:.1f} A {26*s:.1f} {26*s:.1f} 0 0 1 {26*s:.1f} {-26*s:.1f} L {26*s:.1f} 0"
    fill = "#fff" if filled else "#000"
    return (f'<g id="{fid}" transform="translate({x},{y})" opacity="{op}">'
            f'<path d="{body} Z" fill="{fill}" stroke="#fff" stroke-width="3"/>'
            f'<circle cx="0" cy="{-70*s:.1f}" r="{17*s:.1f}" fill="{fill}" stroke="#fff" stroke-width="3"/></g>')

def bowl(cx, cy, w, extra=""):
    h = w * 0.45
    d = (f"M {cx - w:.1f} {cy:.1f} L {cx + w:.1f} {cy:.1f} Q {cx + w * 0.45:.1f} {cy + h * 0.25:.1f} {cx + w * 0.12:.1f} {cy + h * 0.85:.1f} "
         f"Q {cx:.1f} {cy + h * 1.15:.1f} {cx - w * 0.12:.1f} {cy + h * 0.85:.1f} Q {cx - w * 0.45:.1f} {cy + h * 0.25:.1f} {cx - w:.1f} {cy:.1f} Z")
    return f'<path d="{d}" fill="#000" stroke="#fff" stroke-width="3" {extra}/>'

def flag(x, y, fid, color="#fff", s=1.0):
    return (f'<g id="{fid}"><line x1="{x}" y1="{y}" x2="{x}" y2="{y - 110*s}" stroke="#fff" stroke-width="3"/>'
            f'<path d="M {x} {y - 110*s} L {x + 52*s} {y - 94*s} L {x} {y - 78*s} Z" fill="{color}"/></g>')

def island(gid, cx, cy, w=130, hero=True, fl=True, s=1.0, flag_id=None, flag_color="#fff"):
    parts = [bowl(cx, cy, w)]
    if hero: parts.append(figure(f"{gid}-hero", cx - w * 0.3, cy, False, s))
    if fl: parts.append(flag(cx + w * 0.62, cy, flag_id or f"{gid}-flag", flag_color, s))
    return f'<g id="{gid}">{"".join(parts)}</g>'

def path_pts():
    pts = [(FB[0], FB[1] - 10)] + [(x, y) for x, y, _ in PLAT] + [(ISL[0] + 10, ISL[1])]
    return " ".join(f"{x},{y}" for x, y in pts)

def world():
    rnd = random.Random(11)
    dust = "".join(f'<circle class="dust" cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(200, 1900):.0f}" r="{rnd.uniform(1, 2.6):.1f}" '
                   f'fill="#fff" opacity="{rnd.uniform(0.08, 0.3):.2f}"/>' for _ in range(46))
    plats = "".join(f'<g id="p{i}" opacity="0">{bowl(x, y, 46)}'
                    f'<circle cx="{x}" cy="{y + 12}" r="5" fill="#fff"/>'
                    f'<text x="{x + 62}" y="{y + 14}" font-family="Playfair Display" font-style="italic" font-size="34" fill="#d9dce2">{lab}</text></g>'
                    for i, (x, y, lab) in enumerate(PLAT))
    others = "".join(f'<g class="oth" opacity="0">{island(f"oi{i}", x, y, 70, True, True, 0.55)}</g>'
                     for i, (x, y) in enumerate([(170, 640), (420, 470), (660, 380), (960, 560)]))
    hook_plats = "".join(bowl(x, y, 46) for x, y, _ in PLAT)
    card = (f'<g transform="translate(-260,200)"><g id="card" opacity="0"><rect x="{ISL[0] - 95}" y="{ISL[1] - 330}" width="190" height="112" rx="16" fill="#000" stroke="#fff" stroke-width="3"/>'
            f'<polyline points="{ISL[0] - 70},{ISL[1] - 240} {ISL[0] - 35},{ISL[1] - 262} {ISL[0] - 5},{ISL[1] - 252} {ISL[0] + 30},{ISL[1] - 290} {ISL[0] + 70},{ISL[1] - 305}" '
            f'fill="none" stroke="{GOLD}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<text id="card-t" x="{ISL[0] + 74}" y="{ISL[1] - 236}" text-anchor="end" font-family="Archivo Black" font-size="26" fill="{GOLD}">+$</text></g></g>')
    clover = "".join(f'<circle cx="{620 + dx}" cy="{1215 + dy}" r="13" fill="none" stroke="#fff" stroke-width="3"/>'
                     for dx, dy in ((-11, -11), (11, -11), (-11, 11), (11, 11)))
    ind = (f'<g id="ind" opacity="0"><rect x="452" y="1352" width="120" height="72" rx="10" fill="#000" stroke="#fff" stroke-width="3"/>'
           f'<path d="M 464 1400 Q 482 1366 500 1392 T 536 1390 T 560 1374" fill="none" stroke="#fff" stroke-width="3"/>'
           f'<text x="590" y="1372" font-family="Playfair Display" font-style="italic" font-size="54" fill="#fff">?</text></g>')
    qs = "".join(f'<text id="q{i}" x="{FB[0] + dx}" y="{FB[1] - 120 + dy}" opacity="0" font-family="Playfair Display" font-style="italic" '
                 f'font-size="{fs}" fill="#fff" text-anchor="middle">?</text>' for i, (dx, dy, fs) in enumerate([(-40, -20, 46), (30, -60, 60)]))
    return f"""
<defs>
  <radialGradient id="glow"><stop offset="0" stop-color="#fff" stop-opacity="0.55"/><stop offset="0.35" stop-color="#fff" stop-opacity="0.18"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
  <radialGradient id="gglow"><stop offset="0" stop-color="{GOLD}" stop-opacity="0.6"/><stop offset="0.4" stop-color="{GOLD}" stop-opacity="0.18"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
  <clipPath id="pathclip"><rect id="pathclip-r" x="0" y="{GY + 20}" width="{W}" height="0"/></clipPath>
  <clipPath id="glowclip"><rect id="glowclip-r" x="0" y="{GY + 20}" width="{W}" height="0"/></clipPath>
  <clipPath id="aclip"><rect id="aclip-r" x="0" y="{GY + 20}" width="{W}" height="0"/></clipPath>
</defs>
<g id="dustg">{dust}</g>
<circle id="bloom-isl" cx="{ISL[0]}" cy="{ISL[1] - 60}" r="430" fill="url(#glow)" opacity="0"/>
<circle id="bloom-b" cx="{FB[0]}" cy="{FB[1] - 50}" r="260" fill="url(#glow)" opacity="0"/>
<circle id="bloom-gold" cx="{ISL[0]}" cy="{ISL[1] - 80}" r="520" fill="url(#gglow)" opacity="0"/>
<line id="ground" x1="-600" y1="{GY}" x2="{W + 600}" y2="{GY}" stroke="#fff" stroke-width="2" opacity="0.45"/>
<g id="hook">{hook_plats}<polyline points="{path_pts()}" fill="none" stroke="#fff" stroke-width="3"/>
  {island("hk", ISL[0], ISL[1], 130, False, True, 1.0, "hk-flag", GOLD)}{figure("hk-fig", ISL[0] - 30, ISL[1], True)}</g>
<g id="others">{others}</g>
<line id="aline" x1="{FA[0]}" y1="{FA[1] - 100}" x2="{ISL[0] - 60}" y2="{ISL[1] + 40}" stroke="#fff" stroke-width="3" stroke-dasharray="10 16" clip-path="url(#aclip)"/>
<g id="clover" opacity="0">{clover}<line x1="620" y1="1228" x2="628" y2="1262" stroke="#fff" stroke-width="3"/></g>
{ind}
<polyline id="bpath" points="{path_pts()}" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="2 14" stroke-linecap="round" clip-path="url(#pathclip)"/>
<polyline id="bglow" points="{path_pts()}" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" clip-path="url(#glowclip)" opacity="0.95"/>
{plats}
<g id="isl" opacity="0">{island("mi", ISL[0], ISL[1], 130, True, True, 1.0, "mi-flag")}</g>
{card}
<g id="headring" opacity="0"><circle cx="0" cy="0" r="34" fill="none" stroke="{GOLD}" stroke-width="3"/></g>
{figure("figA", FA[0], FA[1], False, 1.0, 0)}
{figure("figB", FB[0], FB[1], True, 1.0, 0)}
{qs}
"""

# camera: focus world point (fx, fy) at screen (540, 1180) with scale s
CAM = [  # (t, fx, fy, s, dur)
    (0.0, 840, 1060, 1.22, 0), (5.35, 500, 1590, 2.0, 1.5), (LEAD + 9.2, 640, 1330, 0.92, 1.7),
    (LEAD + 16.0, 560, 1060, 0.7, 2.0), (LEAD + 19.7, 600, 1520, 1.55, 1.4), (LEAD + 24.5, 700, 1390, 1.0, 1.6),
    (LEAD + 31.7, 640, 1220, 0.76, 1.8), (LEAD + 36.7, FB[0] + 30, FB[1] - 250, 1.15, 1.0),
]
HOPS = [(LEAD + 37.8, 0), (LEAD + 38.7, 1), (LEAD + 39.65, 2), (LEAD + 40.5, 3), (LEAD + 41.75, 4)]
for t, k in HOPS:
    CAM.append((t + 0.05, PLAT[k][0], PLAT[k][1] - 250, 1.15, 0.7))
CAM += [(LEAD + 42.9, 690, 1250, 0.88, 1.5), (LEAD + 46.3, ISL[0] + 10, ISL[1] - 40, 1.85, 1.7),
        (LEAD + 49.4, ISL[0], ISL[1] + 80, 1.3, 1.6), (LEAD + 53.9, ISL[0], ISL[1] + 20, 1.6, 1.7)]

def cam_tl():
    T = []
    for t, fx, fy, s, d in CAM:
        x, y = 540 - fx * s, 1180 - fy * s
        if d == 0:
            T.append(f'tl.set("#world", {{x: {x:.1f}, y: {y:.1f}, scale: {s}}}, {t:.2f});')
        else:
            T.append(f'tl.to("#world", {{x: {x:.1f}, y: {y:.1f}, scale: {s}, duration: {d}, ease: "power3.inOut"}}, {t:.2f});')
    return T

def hop(T, C, t, x0, y0, x1, y1, d=0.45):
    peak = min(y0, y1) - 70
    T.append(f'tl.to("#figB", {{x: {x1}, duration: {d}, ease: "none"}}, {t:.2f});')
    T.append(f'tl.to("#figB", {{y: {peak}, duration: {d / 2:.3f}, ease: "power2.out"}}, {t:.2f});')
    T.append(f'tl.to("#figB", {{y: {y1}, duration: {d / 2:.3f}, ease: "power2.in"}}, {t + d / 2:.3f});')
    C.append(dict(t=t + d, snd="tick", gain=-17))

def scene_tl():
    T, C = [], []
    T += cam_tl()
    T.append('tl.fromTo(".dust", {y: 0}, {y: -120, duration: 60, ease: "none"}, 0);')
    # hook: the finished climb, then it dissolves
    T.append(f'tl.fromTo("#bloom-isl", {{opacity: 0, scale: 0.6, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 1.2, ease: "power2.out"}}, 0.05);')
    T.append(f'tl.fromTo("#hk-flag", {{scaleY: 0, transformOrigin: "50% 100%"}}, {{scaleY: 1, duration: 0.6, ease: "back.out(2)"}}, {wt(6):.2f});')
    T.append(f'tl.to("#hook", {{opacity: 0, filter: "blur(10px)", duration: 0.8, ease: "power2.in"}}, 4.95);')
    T.append(f'tl.to("#bloom-isl", {{opacity: 0, duration: 0.8}}, 4.95);')
    # two traders
    T.append(f'tl.fromTo("#figA", {{opacity: 0, y: {GY + 30}}}, {{opacity: 1, y: {GY}, duration: 0.5, ease: "back.out(2)"}}, {wt(13):.2f});')
    T.append(f'tl.fromTo("#figB", {{opacity: 0, y: {GY + 30}}}, {{opacity: 1, y: {GY}, duration: 0.5, ease: "back.out(2)"}}, {wt(13) + 0.18:.2f});')
    C += [dict(t=wt(13), snd="pop", gain=-15), dict(t=wt(13) + 0.18, snd="pop", gain=-15)]
    # first trader looks up at the winning account
    T.append(f'tl.fromTo("#isl", {{opacity: 0, y: 40}}, {{opacity: 1, y: 0, duration: 0.8, ease: "power3.out"}}, {wt(25):.2f});')
    T.append(f'tl.fromTo("#bloom-isl", {{opacity: 0}}, {{opacity: 0.55, duration: 1.0, immediateRender: false}}, {wt(25):.2f});')
    T.append(f'tl.fromTo("#card", {{opacity: 0, y: 30}}, {{opacity: 1, y: 0, duration: 0.5, ease: "back.out(1.6)"}}, {wt(28):.2f});')
    C += [dict(t=wt(25), snd="swish", gain=-17), dict(t=wt(28), snd="ping", gain=-15)]
    T.append(f'tl.to("#aclip-r", {{attr: {{y: {ISL[1]}, height: {GY + 20 - ISL[1]}}}, duration: 1.3, ease: "power2.inOut"}}, {wt(21):.2f});')
    T.append(f'tl.fromTo("#clover", {{opacity: 0, scale: 0.4, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2.5)"}}, {wt(36):.2f});')
    T.append(f'tl.fromTo("#ind", {{opacity: 0, scale: 0.6, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2.5)"}}, {wt(41):.2f});')
    C += [dict(t=wt(36), snd="ping", gain=-16), dict(t=wt(41), snd="ping", gain=-16)]
    # other people's islands
    T.append(f'tl.fromTo(".oth", {{opacity: 0, y: -30}}, {{opacity: 0.55, y: 0, duration: 0.9, stagger: 0.25, ease: "power2.out"}}, {wt(48):.2f});')
    T.append(f'tl.to(".oth", {{opacity: 0, duration: 0.6, stagger: 0.1}}, {wt(52) - 0.2:.2f});')
    C.append(dict(t=wt(48), snd="swish", gain=-18))
    # second trader asks questions
    T.append(f'tl.to(["#figA", "#clover", "#ind", "#aline"], {{opacity: 0.35, duration: 0.6}}, {wt(52):.2f});')
    T.append(f'tl.fromTo("#bloom-b", {{opacity: 0, scale: 0.5, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.9, ease: "power2.out"}}, {wt(53):.2f});')
    for i, k in enumerate((62, 64)):
        T.append(f'tl.fromTo("#q{i}", {{opacity: 0, y: 20}}, {{opacity: 1, y: 0, duration: 0.4, ease: "back.out(2)"}}, {wt(k):.2f});')
        C.append(dict(t=wt(k), snd="ping", gain=-18))
    T.append(f'tl.to(["#q0", "#q1"], {{opacity: 0, duration: 0.4}}, {wt(65) + 0.3:.2f});')
    # platforms appear with the questions and the steps
    for k, wi in ((0, 66), (1, 71), (2, 105), (3, 107), (4, 109)):
        T.append(f'tl.fromTo("#p{k}", {{opacity: 0, scale: 0.4, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2.2)"}}, {wt(wi):.2f});')
        C.append(dict(t=wt(wi), snd="pop", gain=-14))
    T.append(f'tl.to("#pathclip-r", {{attr: {{y: {ISL[1] - 20}, height: {GY + 40 - ISL[1]}}}, duration: 2.0, ease: "power2.inOut"}}, {wt(75):.2f});')
    C.append(dict(t=wt(75), snd="draw", gain=-17))
    # "changes EVERYTHING"
    T.append(f'tl.fromTo("#bloom-b", {{scale: 1}}, {{scale: 1.6, duration: 0.25, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false}}, {wt(93):.2f});')
    C += [dict(t=wt(93) - 1.0, snd="riser", gain=-16), dict(t=wt(93), snd="impact", gain=-12)]
    # the climb
    T.append(f'tl.to("#bloom-b", {{opacity: 0, duration: 0.6}}, {wt(98):.2f});')
    pos = [(FB[0], FB[1])] + [(x, y) for x, y, _ in PLAT]
    for n, (t, k) in enumerate(HOPS):
        hop(T, C, t, *pos[n], *pos[n + 1])
    # impossible -> process
    T.append(f'tl.to("#aline", {{opacity: 0.9, duration: 0.08, repeat: 5, yoyo: true, ease: "none"}}, {wt(114):.2f});')
    T.append(f'tl.to("#aline", {{opacity: 0, duration: 0.5}}, {wt(114) + 0.6:.2f});')
    C.append(dict(t=wt(114), snd="glitch", gain=-18))
    T.append(f'tl.to("#glowclip-r", {{attr: {{y: {ISL[1] - 20}, height: {GY + 40 - ISL[1]}}}, duration: 0.9, ease: "power2.inOut"}}, {wt(120) - 0.4:.2f});')
    T.append(f'tl.fromTo("#p0, #p1, #p2, #p3, #p4", {{filter: "drop-shadow(0 0 0px #fff)"}}, {{filter: "drop-shadow(0 0 14px #fff)", duration: 0.3, stagger: 0.12}}, {wt(120) - 0.3:.2f});')
    C += [dict(t=wt(120), snd="stamp", gain=-12), dict(t=wt(120) - 0.4, snd="whip", gain=-16)]
    # onto the island, profitable in their head
    hop(T, C, wt(121) + 0.1, PLAT[4][0], PLAT[4][1], ISL[0] + 30, ISL[1], 0.55)
    T.append(f'tl.to("#bloom-isl", {{opacity: 1, scale: 1.15, duration: 1.2, ease: "power2.out"}}, {wt(121) + 0.6:.2f});')
    T.append(f'tl.set("#headring", {{x: {ISL[0] + 30}, y: {ISL[1] - 70}}}, {wt(128):.2f});')
    T.append(f'tl.fromTo("#headring", {{opacity: 0, scale: 0.4, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1.4, duration: 0.6, ease: "expo.out"}}, {wt(129):.2f});')
    C.append(dict(t=wt(129), snd="ping", gain=-14))
    # long before their account: the card reads $0
    T.append(f'tl.to("#card-t", {{opacity: 0, duration: 0.2}}, {wt(130):.2f});')
    T.append(f'tl.set("#card-t", {{textContent: "$0"}}, {wt(130) + 0.2:.2f});')
    T.append(f'tl.to("#card-t", {{opacity: 1, duration: 0.3}}, {wt(133):.2f});')
    T.append(f'tl.to("#card", {{opacity: 0.45, duration: 0.6}}, {wt(133) + 0.4:.2f});')
    C.append(dict(t=wt(133), snd="tick", gain=-15))
    # think ... ACT: the flag turns gold
    T.append(f'tl.fromTo("#headring", {{scale: 1.4}}, {{scale: 2.2, opacity: 0, duration: 0.8, ease: "power2.out", immediateRender: false}}, {wt(141):.2f});')
    T.append(f'tl.to("#mi-flag path", {{fill: "{GOLD}", duration: 0.3}}, {wt(146):.2f});')
    T.append(f'tl.fromTo("#mi-flag", {{scaleY: 1, transformOrigin: "50% 100%"}}, {{scaleY: 1.25, duration: 0.3, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false}}, {wt(146):.2f});')
    T.append(f'tl.fromTo("#bloom-gold", {{opacity: 0, scale: 0.4, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.9, ease: "expo.out"}}, {wt(146):.2f});')
    C += [dict(t=wt(146), snd="impact", gain=-11), dict(t=wt(146) + 0.05, snd="sting", gain=-13)]
    return T, C

# ---------------------------------------------------------------------------------------------------------------------
OUTRO = [0.0, 1.32, 3.34, 4.09]            # phrase starts in vo_outro.wav (see the MSNR series)

def build():
    blocks = parse_blocks()
    vo_end = we(len(WORDS) - 1)
    end_t = round(vo_end + 0.8, 2)
    vo_o = round(end_t + 0.3, 2)
    total = round(vo_o + OUTRO[3] + 1.3, 2)
    tm, tt = text_layer(blocks, end_t)
    st, sc = scene_tl()
    C = [dict(t=0, snd="bed", file="bed"), dict(t=LEAD, snd="vo", file="vo_main", gain=0),
         dict(t=0.05, snd="swish", gain=-16),
         dict(t=end_t, snd="whoosh", gain=-11, align="peak"), dict(t=end_t + 0.25, snd="impact", gain=-9),
         dict(t=vo_o, snd="vo", file="vo_outro", gain=0), dict(t=vo_o + OUTRO[1], snd="pop", gain=-14),
         dict(t=vo_o + OUTRO[2], snd="stamp", gain=-12)] + sc
    for t, *_ in CAM[1:]:
        C.append(dict(t=t, snd="swish", gain=-21))
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
      #vig {{ position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 55%, rgba(30,30,34,0.55) 0%, rgba(0,0,0,0) 60%); }}
      #world {{ position: absolute; left: 0; top: 0; width: {W}px; height: {H}px; transform-origin: 0 0; }}
      #world svg {{ width: {W}px; height: {H}px; overflow: visible; filter: drop-shadow(0 0 5px rgba(255,255,255,0.45)); }}
      #text {{ position: absolute; left: 0; top: 0; width: {W}px; height: {H}px; }}
      #text::before {{ content: ""; position: absolute; left: 0; right: 0; top: 0; height: 760px;
        background: linear-gradient(#000 0%, rgba(0,0,0,0.85) 55%, rgba(0,0,0,0) 100%); }}
      .tb {{ position: absolute; left: 60px; width: 960px; top: 250px; text-align: center; }}
      .ln {{ line-height: 1.12; white-space: nowrap; }}
      .w {{ display: inline-block; opacity: 0; margin: 0 0.12em; }}
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
    <div id="root" data-composition-id="otm-mindset" data-start="0" data-duration="{total}" data-width="{W}" data-height="{H}" data-motion-blur="on">
      <div id="vig"></div>
      <div id="world"><svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{world()}</svg></div>
      <div id="text" data-layout-allow-overlap>
{chr(10).join("        " + m for m in tm)}
      </div>
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
{chr(10).join("        " + t for t in st)}
{chr(10).join("        " + t for t in tt)}
        tl.to("#world", {{ opacity: 0, filter: "blur(10px)", duration: 0.4, ease: "power2.in" }}, {end_t - 0.4:.2f});
        tl.fromTo("#flash", {{ opacity: 0.8 }}, {{ opacity: 0, duration: 0.35, ease: "power2.out", immediateRender: false }}, {end_t:.2f});
        tl.fromTo("#end", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.05, immediateRender: false }}, {end_t:.2f});
        tl.fromTo("#end-logo", {{ opacity: 0, scale: 2.2, filter: "blur(14px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.5, ease: "expo.out" }}, {end_t + 0.1:.2f});
        tl.fromTo("#end-tag", {{ opacity: 0, y: 30, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.4, ease: "expo.out" }}, {vo_o + OUTRO[1]:.2f});
        tl.fromTo("#end-cta", {{ opacity: 0, clipPath: "inset(0% 100% 0% 0%)" }}, {{ opacity: 1, clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power3.out" }}, {vo_o + OUTRO[2]:.2f});
        tl.fromTo("#end-note", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {end_t + 1.0:.2f});
        tl.fromTo("#end-foot-img", {{ y: 255 }}, {{ y: 0, duration: 0.5, ease: "back.out(1.2)" }}, {end_t + 0.9:.2f});
        window.__timelines["otm-mindset"] = tl;
      }})();
    </script>
  </body>
</html>
"""
    open(f"{ROOT}/index.html", "w").write(html)
    json.dump(dict(total=total, cues=sorted(C, key=lambda c: c["t"])), open(f"{ROOT}/work/cues.json", "w"), indent=1)
    print("total", total, "end card", end_t)

if __name__ == "__main__":
    build()
