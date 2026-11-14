"""Shared constants and drawing helpers for the "why price moves" film (from the otm-losses film) in the style of the reference: one idea per scene, drawn as glowing white
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
    C.append(dict(t=t + 0.2, snd="tock", gain=-3))
def plen(pts):
    import math
    return round(sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)) + 2)
def polyline(eid, pts, color="#fff", w=4, extra=""):
    L = plen(pts)
    return (f'<polyline id="{eid}" points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="none" stroke="{color}" stroke-width="{w}" '
            f'stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="{L}" stroke-dashoffset="{L}" {extra}/>'), L

