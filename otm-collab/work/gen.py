"""OTM x Accurate System: a short collaboration teaser in the OTM glowing style (same scene system as otm-chance /
otm-break). The OTM emblem lights up and slides aside, a gold x brings in the ACCURATE SYSTEM wordmark (text only: no
partner logo supplied), "new collaboration / two names, one mission", three locked tiles and a progress bar ("something
is being built ... almost ready"), "BIG THINGS ARE COMING", then the OTM outro with the handles. Voice: Quentin, no
music. Writes ../index.html, work/cues.json (soft kit sounds) and work/timing.json."""
import json, math, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAD = 0.3
GOLD, RED, WHITE, GREY, LBL = "#e8c26a", "#ff4d5e", "#ffffff", "#7d838c", "#c9ced6"
GY = 1240                                   # ground line
words = json.load(open(f"{ROOT}/work/words.json"))
def W(i): return round(words[i]["start"] + LEAD, 3)
def WE(i): return round(words[i]["end"] + LEAD, 3)
END_T = round(words[-1]["end"] + LEAD + 0.6, 2)
TOTAL = round(END_T + 2.0, 2)          # no end card: the outro holds (handles readable), then fades out
rnd = random.Random(7)

T, CUES = [], []
def tl(s): T.append(s)
def cue(t, snd, gain): CUES.append(dict(t=round(t, 3), snd=snd, gain=gain))


class S:
    """Builds one scene's SVG and its tweens."""
    n = 0
    scenes = []

    def __init__(self, o, c, ground=True, first=False, restore=True, hide=True):
        S.n += 1
        self.id, self.o, self.c, self.items = f"sc{S.n}", o, c, []
        S.scenes.append(self)
        if first:
            tl(f'tl.set("#{self.id}", {{opacity: 1, visibility: "visible"}}, 0);')
        else:
            tl(f'tl.set("#{self.id}", {{visibility: "visible"}}, {o:.3f});')
            tl(f'tl.fromTo("#{self.id}", {{opacity: 0}}, {{opacity: 1, duration: 0.3, ease: "power2.out", immediateRender: false}}, {o:.3f});')
        tl(f'tl.fromTo("#{self.id}", {{scale: 1}}, {{scale: 1.035, transformOrigin: "50% 60%", duration: {c - o:.3f}, ease: "none", immediateRender: false}}, {o:.3f});')
        tl(f'tl.to("#{self.id}", {{opacity: 0, duration: 0.25, ease: "power2.in"}}, {c - 0.25:.3f});')
        tl(f'tl.set("#{self.id}", {{opacity: 0, visibility: "hidden"}}, {c:.3f});')
        if not ground and hide:
            tl(f'tl.to("#ground", {{opacity: 0, duration: 0.3}}, {o - 0.15:.3f});')
        if not ground and restore:
            tl(f'tl.to("#ground", {{opacity: 1, duration: 0.3}}, {c - 0.15:.3f});')

    def uid(self, p):
        S.n += 1
        return f"{p}{S.n}"

    def add(self, s, p="e"):
        i = self.uid(p)
        self.items.append(s.replace("@ID@", i))
        return i

    # ---- primitives ----
    def fig(self, x, s=1.0, col=WHITE, op=1.0, glow=True, gy=GY, dashed=False):
        f = (f'fill="none" stroke="{col}" stroke-width="5" stroke-dasharray="14 10"' if dashed else f'fill="{col}"')
        g = "filter:drop-shadow(0 0 16px rgba(255,255,255,0.55));" if glow and not dashed else ""
        return self.add(f'<g transform="translate({x},{gy}) scale({s})"><g id="@ID@" style="opacity:{op};{g}">'
                        f'<circle cx="0" cy="-158" r="31" {f}/><path d="M -48 0 L -48 -66 Q -48 -116 0 -116 Q 48 -116 48 -66 L 48 0 Z" {f}/></g></g>', "f")

    def spot(self, x, op=1.0, col="255,255,255", top=36, bot=150, gy=GY):
        gid = self.uid("gr")
        return self.add(f'<g id="@ID@" style="opacity:{op}"><defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
                        f'<stop offset="0" stop-color="rgb({col})" stop-opacity="0.26"/><stop offset="1" stop-color="rgb({col})" stop-opacity="0.04"/></linearGradient></defs>'
                        f'<path d="M {x - top} 380 L {x + top} 380 L {x + bot} {gy} L {x - bot} {gy} Z" fill="url(#{gid})"/>'
                        f'<ellipse cx="{x}" cy="{gy}" rx="{bot + 10}" ry="26" fill="none" stroke="rgb({col})" stroke-opacity="0.55" stroke-width="2" stroke-dasharray="8 8"/></g>', "sp")

    def label(self, x, y, text, size=28, col=LBL, op=0, weight=700, sp=0.18, anchor="middle"):
        return self.add(f'<text id="@ID@" x="{x}" y="{y}" text-anchor="{anchor}" font-family="Montserrat" font-weight="{weight}" font-size="{size}" '
                        f'letter-spacing="{sp}em" fill="{col}" style="opacity:{op}">{text}</text>', "t")

    def pill(self, x, y, text, fill=WHITE, tcol="#0b0b0b", size=28, op=0):
        w = len(text) * size * 0.74 + 52; h = size + 28
        return self.add(f'<g id="@ID@" style="opacity:{op}"><rect x="{x - w / 2:.0f}" y="{y - h / 2:.0f}" width="{w:.0f}" height="{h}" rx="{h / 2}" fill="{fill}" '
                        f'style="filter:drop-shadow(0 0 12px rgba(255,255,255,0.35))"/><text x="{x}" y="{y + size * 0.36:.0f}" text-anchor="middle" '
                        f'font-family="Montserrat" font-weight="800" font-size="{size}" letter-spacing="0.06em" fill="{tcol}">{text}</text></g>', "pl")

    def path(self, d, col=WHITE, w=4, fill="none", drawn=False, extra="", style=""):
        st = ("" if drawn else "stroke-dasharray:1 1.2;stroke-dashoffset:1.1;") + style
        dash = ('' if drawn else 'pathLength="1" ') + (f'style="{st}"' if st else "")
        return self.add(f'<path id="@ID@" d="{d}" fill="{fill}" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {dash} {extra}/>', "p")

    def raw(self, s, p="r"):
        return self.add(s, p)

    # ---- motion ----
    def draw(self, i, t, d=0.6, ease="power2.inOut"):
        tl(f'tl.fromTo("#{i}", {{strokeDashoffset: 1.1}}, {{strokeDashoffset: 0, duration: {d:.3f}, ease: "{ease}", immediateRender: false}}, {t:.3f});')

    def fade(self, i, t, d=0.35, to=1, frm=0, y=0):
        a = f", y: {y}" if y else ""; b = ", y: 0" if y else ""
        tl(f'tl.fromTo("#{i}", {{opacity: {frm}{a}}}, {{opacity: {to}{b}, duration: {d:.3f}, ease: "power2.out", immediateRender: false}}, {t:.3f});')

    def pop(self, i, t, d=0.4, frm=0.4, origin="50% 100%"):
        if t > self.o + 0.05:                                   # hidden until its pop, even if drawn visible
            tl(f'tl.set("#{i}", {{opacity: 0}}, {self.o:.3f});')
        tl(f'tl.fromTo("#{i}", {{opacity: 0, scale: {frm}, transformOrigin: "{origin}"}}, {{opacity: 1, scale: 1, duration: {d:.3f}, ease: "back.out(1.8)", immediateRender: false}}, {t:.3f});')

    def walk(self, i, t, dx, d):
        tl(f'tl.to("#{i}", {{x: "+={dx}", duration: {d:.3f}, ease: "power1.inOut"}}, {t:.3f});')
        steps = max(1, int(d / 0.18))
        tl(f'tl.to("#{i}", {{y: -7, duration: {d / (2 * steps):.3f}, yoyo: true, repeat: {2 * steps - 1}, ease: "sine.inOut"}}, {t:.3f});')


def rrect(x, y, w, h, r):
    return (f"M {x + r} {y} H {x + w - r} Q {x + w} {y} {x + w} {y + r} V {y + h - r} Q {x + w} {y + h} {x + w - r} {y + h} "
            f"H {x + r} Q {x} {y + h} {x} {y + h - r} V {y + r} Q {x} {y} {x + r} {y} Z")

def mini_curve(x, y, w=110, h=50, up=True):
    pts = [(0, 0.85), (0.2, 0.6), (0.35, 0.72), (0.55, 0.4), (0.7, 0.5), (1.0, 0.05)] if up else [(0, 0.1), (0.3, 0.3), (0.45, 0.2), (0.7, 0.7), (1, 0.95)]
    return "M " + " L ".join(f"{x + px * w:.0f} {y + py * h:.0f}" for px, py in pts)

# ================================================================================================= scenes
import re as _re
def _n(x): return _re.sub(r"[^a-z0-9']", "", x.lower())
def F(word, k=1):
    c = 0
    for i, w in enumerate(words):
        if _n(w["text"]) == word:
            c += 1
            if c == k: return i
    raise KeyError((word, k))
def A(word, k=1): return W(F(word, k))

# ================================================================================================= scenes
EMB_W, EMB_H = 300, 291

def lock(x, y, col="#fff", sc=1.0):
    return (f'<path d="M {x - 18 * sc} {y - 4 * sc} V {y - 22 * sc} A {18 * sc} {18 * sc} 0 0 1 {x + 18 * sc} {y - 22 * sc} V {y - 4 * sc}" fill="none" stroke="{col}" stroke-width="{5 * sc}"/>'
            f'<rect x="{x - 28 * sc}" y="{y - 6 * sc}" width="{56 * sc}" height="{44 * sc}" rx="{8 * sc}" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y + 14 * sc}" r="{5 * sc}" fill="#000"/>')

# 1  "Order the Market ... and Accurate System. A new collaboration. Two names. One mission."
s = S(0, A("something") - 0.1, ground=False, first=True, restore=False, hide=False)
s.items.append(f'<defs><radialGradient id="eglow"><stop offset="0" stop-color="{GOLD}" stop-opacity="0.38"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
grp = s.raw(f'<g id="@ID@"><circle cx="540" cy="800" r="270" fill="url(#eglow)"/>'
            f'<image href="assets/otm_emblem.png" x="{540 - EMB_W / 2}" y="{800 - EMB_H / 2:.1f}" width="{EMB_W}" height="{EMB_H}" style="filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>'
            f'<text x="540" y="1012" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" letter-spacing="0.22em" fill="{GOLD}">ORDER THE MARKET</text></g>', "eg")
tl(f'tl.fromTo("#{grp}", {{opacity: 0.6, scale: 0.92, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.9, ease: "power2.out"}}, 0);')
tl(f'tl.to("#{grp}", {{x: -245, scale: 0.78, transformOrigin: "50% 50%", duration: 0.7, ease: "power3.inOut"}}, {A("and") - 0.15:.3f});')
cue(0.05, "swell_1", -18)
xm = s.label(540, 830, "×", 96, GOLD, 0, 800, 0); s.pop(xm, A("and") + 0.15, 0.4, 0.3, "50% 50%"); cue(A("and") + 0.15, "bell_C5", -18)
cid = s.uid("cp"); rid = s.uid("cr")
s.items.append(f'<defs><clipPath id="{cid}"><rect id="{rid}" x="572" y="680" width="0" height="240"/></clipPath></defs>')
wm = s.raw(f'<g id="@ID@" clip-path="url(#{cid})" style="filter:drop-shadow(0 0 14px rgba(255,255,255,0.35))">'
           f'<text x="795" y="792" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="66" letter-spacing="0.04em" fill="#fff">ACCURATE</text>'
           f'<text x="795" y="870" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="66" letter-spacing="0.16em" fill="#fff">SYSTEM</text>'
           f'<rect x="700" y="896" width="190" height="5" rx="2.5" fill="{GOLD}"/></g>', "wm")
tl(f'tl.fromTo("#{rid}", {{attr: {{width: 0}}}}, {{attr: {{width: 440}}, duration: 0.8, ease: "power2.out", immediateRender: false}}, {A("accurate") - 0.15:.3f});')
cue(A("accurate") - 0.15, "whoosh-short_1", -20)
pc = s.pill(540, 1150, "NEW COLLABORATION", GOLD, "#111", 30); s.pop(pc, A("collaboration") - 0.2, 0.45, 0.5, "50% 50%"); cue(A("collaboration") - 0.1, "click-confirm_1", -18)
burst = s.raw(f'<circle id="@ID@" cx="540" cy="800" r="60" fill="none" stroke="{GOLD}" stroke-width="4" style="opacity:0"/>', "c")
tl(f'tl.fromTo("#{burst}", {{opacity: 0.9, scale: 0.6, transformOrigin: "50% 50%"}}, {{opacity: 0, scale: 4.5, duration: 1.0, ease: "power2.out", immediateRender: false}}, {A("one") - 0.05:.3f});')
cue(A("one") - 0.05, "swell_2", -18)
t2 = s.label(556, 1262, "TWO NAMES ·", 32, WHITE, 0, 800, 0.14, "end"); s.fade(t2, A("two") - 0.05, 0.35, y=10)
t3 = s.label(570, 1262, "ONE MISSION", 32, GOLD, 0, 800, 0.14, "start"); s.fade(t3, A("one") - 0.05, 0.35, y=10)

# 2  "Something is being built ... and it's almost ready."
s = S(A("something") - 0.1, A("big") - 0.1, ground=False, restore=False, hide=False)
s.label(540, 600, "OTM  ×  ACCURATE SYSTEM", 30, LBL, 1, 700, 0.2)
for k, (x, w_) in enumerate([(270, "something"), (540, "being"), (810, "built")]):
    tile = s.raw(f'<g id="@ID@" style="opacity:0"><path d="{rrect(x - 105, 720, 210, 230, 20)}" fill="#0d1117" stroke="#ffffff90" stroke-width="3"/>{lock(x, 835, "#ffffffd0", 1.1)}</g>', "tl")
    s.pop(tile, A(w_) - 0.1, 0.4, 0.6, "50% 50%"); cue(A(w_) - 0.1, "tick-crisp_" + str(k + 1), -18)
    gl = s.raw(f'<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 14px {GOLD})"><path d="{rrect(x - 105, 720, 210, 230, 20)}" fill="none" stroke="{GOLD}" stroke-width="4"/>{lock(x, 835, GOLD, 1.1)}</g>', "tg")
    s.fade(gl, A("ready") - 0.1 + k * 0.12, 0.35)
cue(A("ready") - 0.1, "bell_E5", -18)
s.raw('<rect id="@ID@" x="170" y="1050" width="740" height="16" rx="8" fill="#ffffff22"/>', "bt")
bar = s.raw(f'<rect id="@ID@" x="170" y="1050" width="0" height="16" rx="8" fill="{GOLD}" style="filter:drop-shadow(0 0 10px {GOLD})"/>', "bf")
tl(f'tl.fromTo("#{bar}", {{attr: {{width: 0}}}}, {{attr: {{width: 660}}, duration: {A("ready") + 0.3 - A("something"):.3f}, ease: "power1.inOut", immediateRender: false}}, {A("something"):.3f});')
ip = s.label(540, 1130, "IN PROGRESS", 30, GREY, 1, 700, 0.24)
tl(f'tl.to("#{ip}", {{opacity: 0, duration: 0.2}}, {A("almost") - 0.2:.3f});')
ar = s.label(540, 1130, "ALMOST READY", 32, GOLD, 0, 800, 0.24); s.fade(ar, A("almost"), 0.35, y=10)

# 3  "Big things are coming."
s = S(A("big") - 0.1, A("follow") - 0.05, ground=False, restore=False, hide=False)
fl = s.raw('<rect id="@ID@" x="0" y="0" width="1080" height="1920" fill="#fff" style="opacity:0"/>', "fl")
tl(f'tl.fromTo("#{fl}", {{opacity: 0.32}}, {{opacity: 0, duration: 0.45, ease: "power2.out", immediateRender: false}}, {A("big") - 0.05:.3f});')
b1 = s.label(540, 880, "BIG THINGS", 118, WHITE, 0, 800, 0.02)
tl(f'tl.fromTo("#{b1}", {{opacity: 0, scale: 1.35, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.45, ease: "expo.out", immediateRender: false}}, {A("big") - 0.05:.3f});')
b2 = s.label(540, 1010, "ARE COMING", 96, GOLD, 0, 800, 0.04)
tl(f'tl.fromTo("#{b2}", {{opacity: 0, scale: 1.35, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.45, ease: "expo.out", immediateRender: false}}, {A("are") - 0.05:.3f});')
cue(A("big") - 0.05, "land_1", -16); cue(A("are") - 0.05, "land-light_1", -18)
sm = s.label(540, 1110, "OTM  ×  ACCURATE SYSTEM", 30, LBL, 0, 700, 0.2); s.fade(sm, A("coming"), 0.35)

# 4  outro: "Follow, so you don't miss it."   (no end card: holds, then fades out)
o4 = A("follow") - 0.05
s = S(o4, TOTAL)
tl(f'tl.to("#ground", {{opacity: 1, duration: 0.4}}, {o4:.3f});')
es = s.spot(540, 0, "232,194,106", 40, 230); s.fade(es, o4, 0.5)
em = s.raw(f'<image id="@ID@" href="assets/otm_emblem.png" x="390" y="900" width="{EMB_W}" height="{EMB_H}" style="opacity:0;filter:drop-shadow(0 0 26px rgba(232,194,106,0.6))"/>', "i")
s.pop(em, o4, 0.6, 0.6, "50% 50%"); cue(o4, "bell_A4", -16)
o1 = s.label(540, 1300, "ORDER THE MARKET", 32, GOLD, 0, 800, 0.3); s.fade(o1, o4 + 0.2, 0.45)
o2 = s.label(540, 1360, "×  ACCURATE SYSTEM  ·  COMING SOON", 28, WHITE, 0, 700, 0.12); s.fade(o2, o4 + 0.4, 0.45)
o3 = s.pill(540, 1470, "FOLLOW FOR MORE", GOLD, "#111", 30); s.pop(o3, A("follow") + 0.1, 0.4, 0.6, "50% 50%"); cue(A("follow") + 0.1, "click-confirm_1", -16)
hx = 290
soc = s.raw(f'<g id="@ID@" style="opacity:0">'
            f'<rect x="{hx}" y="1548" width="36" height="36" rx="10" fill="none" stroke="#fff" stroke-width="3"/>'
            f'<circle cx="{hx + 18}" cy="1566" r="8.5" fill="none" stroke="#fff" stroke-width="3"/><circle cx="{hx + 28}" cy="1556" r="2.4" fill="#fff"/>'
            f'<text x="{hx + 48}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@fxzuez_28</text>'
            f'<path d="M {hx + 322} 1546 V 1574 A 9 9 0 1 1 {hx + 313} 1565 M {hx + 322} 1546 Q {hx + 326} 1557 {hx + 338} 1558" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>'
            f'<text x="{hx + 348}" y="1577" font-family="Montserrat" font-weight="700" font-size="30" fill="#fff">@zuez_28</text></g>', "so")
disc = s.label(540, 1650, "EDUCATIONAL ONLY · NOT FINANCIAL ADVICE", 28, GREY, 0, 600, 0.12)
s.fade(soc, A("miss") - 0.2, 0.5, y=12)
s.fade(disc, A("miss") + 0.2, 0.5)


# ------------------------------------------------------------------ end card, dust, ground, emblem
dust = ""
for k in range(40):
    x, y, r, op = rnd.uniform(0, 1080), rnd.uniform(0, 1920), rnd.uniform(1.2, 3.2), rnd.uniform(0.05, 0.22)
    dust += f'<circle id="d{k}" cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#fff" opacity="{op:.2f}"/>'
    tl(f'tl.fromTo("#d{k}", {{x: 0, y: 0}}, {{x: {rnd.uniform(-70, 70):.0f}, y: {-rnd.uniform(150, 480):.0f}, duration: {TOTAL}, ease: "none"}}, 0);')

scenes_svg = "\n".join(f'<g id="{x.id}" style="opacity:0;visibility:hidden" data-layout-allow-overlap>' + "".join(x.items) + "</g>" for x in S.scenes)
CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #000; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #000; font-family: Montserrat, sans-serif; color: #fff; }
#stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
#vig { position: absolute; inset: 0; pointer-events: none; background: radial-gradient(ellipse at 50% 48%, rgba(40,44,52,0.35) 0%, transparent 55%, rgba(0,0,0,0.6) 100%); }
#mark { position: absolute; left: 495px; top: 1560px; width: 90px; opacity: 0.85; filter: drop-shadow(0 0 10px rgba(255,255,255,0.2)); }
"""
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="otm-collab" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="vig"></div>
      <svg id="stage" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overlap>
        <g id="dust">{dust}</g>
        <line id="ground" x1="0" y1="{GY}" x2="1080" y2="{GY}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="12 12" style="opacity:0"/>
{scenes_svg}
      </svg>
      <audio id="otm-collab-audio" class="clip" src="assets/audio/mix_collab.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-collab"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)
json.dump(dict(total=TOTAL, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("total", TOTAL, "end", END_T, "scenes", len(S.scenes), "tl lines", len(T), "cues", len(CUES))
