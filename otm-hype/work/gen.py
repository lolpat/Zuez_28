"""OTM hype edits cut to the beat of "Mist" (EsDeeKid, Rico Ace; ~98.7 BPM). The song is NOT in these files: it is
added in the TikTok / Instagram app (their licensed library), starting at the drop, so every cut here sits on the
beat grid of the drop (t = 0 is the first beat after the drop).

Design: black-and-white, film grain, letterbox bars, huge Archivo Black words with gold accents, blue candles, and on
every beat a hard cut, zoom punch, flash, shake or RGB split.

  lonely/  "lonely at the top" (text only, the trend format)
  haters/  "you'll never find a hater doing better than you" (Quentin voice, work/words_haters.json)
Outputs: <video>/index.html and work/cues_<video>.json (sound cues for work/mix_kit.py, earshot launch kit roles).
"""
import json, os, random, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1080, 1920
BEAT = 60 / 98.7
GOLD, BLUE, RED = "#e8c26a", "#2962ff", "#ff2d55"
OUTRO = [0.0, 1.32, 3.34, 4.09]

def b(n): return round(n * BEAT, 3)

class Film:
    def __init__(self, cid):
        self.cid, self.T, self.C, self.M = cid, [], [], []
        self.rnd = random.Random(hash(cid) % 1000)
    def tl(self, s): self.T.append(s)
    def cue(self, t, snd, gain=0, **kw): self.C.append(dict(t=round(t, 3), snd=snd, gain=gain, **kw))
    # -- beat effects -------------------------------------------------------------------------------------------------
    def punch(self, t, s=1.14):
        self.tl(f'tl.fromTo("#cam", {{scale: {s}}}, {{scale: 1, duration: {BEAT * 0.9:.3f}, ease: "expo.out", immediateRender: false}}, {t:.3f});')
    def flash(self, t, a=0.55):
        self.tl(f'tl.fromTo("#flash", {{opacity: {a}}}, {{opacity: 0, duration: 0.18, ease: "power2.out", immediateRender: false}}, {t:.3f});')
    def streak(self, t):
        self.tl(f'tl.fromTo("#streak", {{xPercent: -120, opacity: 1}}, {{xPercent: 120, opacity: 1, duration: 0.35, ease: "power2.inOut", immediateRender: false}}, {t:.3f});')
        self.tl(f'tl.set("#streak", {{opacity: 0}}, {t + 0.36:.3f});')
    def shake(self, t, amp=16):
        for i in range(4):
            self.tl(f'tl.set("#cam", {{x: {0 if i == 3 else self.rnd.choice([-1, 1]) * amp:.0f}, y: {0 if i == 3 else self.rnd.choice([-1, 1]) * amp * 0.6:.0f}}}, {t + i / 30:.3f});')
    def rgb(self, sel, t, amp=18, steps=5):
        for s in range(steps + 1):
            dx = 0 if s == steps else self.rnd.choice([-1, 1]) * self.rnd.uniform(amp * 0.4, amp)
            self.tl(f'tl.set("{sel} .r", {{x: {dx:.1f}}}, {t + s * 0.035:.3f});')
            self.tl(f'tl.set("{sel} .c", {{x: {-dx:.1f}}}, {t + s * 0.035:.3f});')
    def invert(self, t, d=0.07):
        self.tl(f'tl.set("#root-in", {{filter: "invert(1)"}}, {t:.3f});')
        self.tl(f'tl.set("#root-in", {{filter: "none"}}, {t + d:.3f});')
    # -- words ----------------------------------------------------------------------------------------------------------
    def word(self, wid, html, t_in, t_out, size=150, top=760, color="#fff", glitch=True, enter="slam"):
        g = (f'<span class="r">{html}</span><span class="c">{html}</span>' if glitch else "")
        self.M.append(f'<div id="{wid}" class="wd" style="top:{top}px;font-size:{size}px;color:{color}" data-layout-allow-overlap>{g}<b>{html}</b></div>')
        if t_in < 0.01:                                       # the first card is visible on frame 0 (the thumbnail)
            self.tl(f'tl.fromTo("#{wid}", {{opacity: 1, scale: 1.35}}, {{opacity: 1, scale: 1, duration: 0.25, ease: "power4.out"}}, 0);')
        elif enter == "slam":
            self.tl(f'tl.fromTo("#{wid}", {{opacity: 0, scale: 1.8, filter: "blur(14px)"}}, {{opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.16, ease: "power4.out"}}, {t_in:.3f});')
        elif enter == "up":
            self.tl(f'tl.fromTo("#{wid}", {{opacity: 0, y: 120}}, {{opacity: 1, y: 0, duration: 0.2, ease: "power4.out"}}, {t_in:.3f});')
        else:
            self.tl(f'tl.fromTo("#{wid}", {{opacity: 0}}, {{opacity: 1, duration: 0.06}}, {t_in:.3f});')
        self.tl(f'tl.set("#{wid}", {{opacity: 0}}, {t_out:.3f});')
        if glitch: self.rgb(f"#{wid}", t_in)

    def candles(self, cid, seq, x0, base, sc, w=34, gap=50, cls=None):
        cls = cls or cid
        out = ""
        for i, (o, c) in enumerate(seq):
            x = x0 + i * gap; top, bot = base - max(o, c) * sc, base - min(o, c) * sc
            col = BLUE if c >= o else "#f2f2f2"
            out += (f'<g class="{cls}" opacity="0"><line x1="{x}" y1="{top - 14}" x2="{x}" y2="{bot + 14}" stroke="{col}" stroke-width="4"/>'
                    f'<rect x="{x - w / 2}" y="{top:.0f}" width="{w}" height="{max(4, bot - top):.0f}" fill="{col}"/></g>')
        return out

    def svg(self, sid, inner, t_in, t_out):
        self.M.append(f'<svg id="{sid}" class="sv" viewBox="0 0 {W} {H}" opacity="0">{inner}</svg>')
        self.tl(f'tl.set("#{sid}", {{opacity: 1}}, {t_in:.3f});')
        self.tl(f'tl.set("#{sid}", {{opacity: 0}}, {t_out:.3f});')

    def endcard(self, t, voice):
        self.M.append('<div id="end"><img id="end-logo" src="assets/otm_logo.png" alt="Order the Market" />'
                      '<div id="end-tag">DON\'T LET THE MARKET <span>ORDER YOU</span></div>'
                      '<div id="end-cta">FOLLOW FOR <span>MORE</span></div>'
                      '<div id="end-note">EDUCATIONAL ONLY · NOT FINANCIAL ADVICE</div>'
                      '<div id="end-foot"><img id="end-foot-img" src="assets/footer.jpg" alt="" /></div></div>')
        self.tl(f'tl.set("#end", {{opacity: 1}}, {t:.3f});')
        self.flash(t, 0.9); self.shake(t, 20)
        self.tl(f'tl.fromTo("#end-logo", {{opacity: 0, scale: 2.4, filter: "blur(14px)"}}, {{opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.35, ease: "expo.out"}}, {t:.3f});')
        tag_t, cta_t = (t + 0.3 + OUTRO[1], t + 0.3 + OUTRO[2]) if voice else (t + b(1), t + b(2))
        self.tl(f'tl.fromTo("#end-tag", {{opacity: 0, y: 30}}, {{opacity: 1, y: 0, duration: 0.25, ease: "expo.out"}}, {tag_t:.3f});')
        self.tl(f'tl.fromTo("#end-cta", {{opacity: 0, scale: 1.5}}, {{opacity: 1, scale: 1, duration: 0.2, ease: "power4.out"}}, {cta_t:.3f});')
        self.tl(f'tl.fromTo("#end-note", {{opacity: 0}}, {{opacity: 1, duration: 0.3}}, {t + 0.6:.3f});')
        self.tl(f'tl.fromTo("#end-foot-img", {{y: 255}}, {{y: 0, duration: 0.35, ease: "back.out(1.4)"}}, {t + 0.4:.3f});')
        self.cue(t, "hit", 2); self.cue(t + 0.02, "drop", 0)
        if voice:
            self.cue(t + 0.3, "vo", 0, file="vo_outro"); self.cue(cta_t, "snap", -2)

    def write(self, total, folder):
        rnd = random.Random(3)
        t = 0.0
        while t < total:                                          # grain steps (seek-safe)
            self.tl(f'tl.set("#grain", {{x: {rnd.randint(-60, 60)}, y: {rnd.randint(-80, 80)}}}, {t:.2f});'); t += 1 / 15
        # background: a faint ghost chart scrolling under everything, plus a light streak on each shake
        gc, x, v = "", 40, 900
        for i in range(44):
            o = v; v = max(300, min(1500, v + rnd.choice([-1, 1]) * rnd.uniform(30, 120))); c = v
            top, bot = min(o, c), max(o, c)
            gc += f'<line x1="{x}" y1="{top - 30}" x2="{x}" y2="{bot + 30}" stroke="#fff" stroke-width="4"/><rect x="{x - 18}" y="{top}" width="36" height="{max(6, bot - top)}" fill="#fff"/>'
            x += 52
        self.M.insert(0, f'<svg id="ghost" viewBox="0 0 2400 1920" style="position:absolute;left:0;top:0;width:2400px;height:1920px;opacity:0.07">{gc}</svg>'
                         '<div id="streak"></div>')
        self.tl(f'tl.fromTo("#ghost", {{x: 0}}, {{x: -1300, duration: {total}, ease: "none"}}, 0);')
        css = CSS.replace("@W@", str(W))
        html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{css}</style>
  </head>
  <body>
    <div id="root" data-composition-id="{self.cid}" data-start="0" data-duration="{total}" data-width="{W}" data-height="{H}" data-motion-blur="on">
      <div id="root-in">
        <div id="cam" data-layout-allow-overlap>
{chr(10).join("          " + m for m in self.M if not m.startswith('<div id="end"'))}
        </div>
        <div class="bar top"></div><div class="bar bot"></div>
        <div id="grain"></div>
      </div>
{chr(10).join("      " + m for m in self.M if m.startswith('<div id="end"'))}
      <div id="flash"></div>
      <audio id="{self.cid}-audio" class="clip" src="assets/audio/mix_{self.cid}.wav" data-start="0" data-duration="{total}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in self.T)}
        window.__timelines["{self.cid}"] = tl;
      }})();
    </script>
  </body>
</html>
"""
        d = f"{ROOT}/{folder}"; os.makedirs(d, exist_ok=True)
        open(f"{d}/index.html", "w").write(html)
        for f in ("hyperframes.json", "package.json"):
            if not os.path.exists(f"{d}/{f}"): os.symlink(f"../{f}", f"{d}/{f}")
        if not os.path.exists(f"{d}/assets"): os.symlink("../assets", f"{d}/assets")
        json.dump(dict(total=total, cues=sorted(self.C, key=lambda c: c["t"])), open(f"{ROOT}/work/cues_{self.cid}.json", "w"), indent=1)
        print(self.cid, "total", total, "lines", len(self.T), "cues", len(self.C))

CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #000; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #000; font-family: Montserrat, sans-serif; color: #fff; }
#root-in, #cam { position: absolute; inset: 0; }
#cam { transform-origin: 50% 50%; }
.wd { position: absolute; left: 0; width: 1080px; text-align: center; font-family: 'Archivo Black'; line-height: 1.02; letter-spacing: -0.01em;
  opacity: 0; text-transform: uppercase; }
.wd b { position: relative; font-weight: 400; text-shadow: 0 0 40px rgba(0,0,0,0.9); }
.wd .r, .wd .c { position: absolute; left: 0; top: 0; width: 100%; mix-blend-mode: screen; }
.wd .r { color: #ff2d55; } .wd .c { color: #22e5ff; }
.gold { color: #e8c26a; } .blue { color: #2962ff; }
.sv { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
.sub { position: absolute; left: 0; width: 1080px; text-align: center; font-family: Montserrat; font-weight: 800; font-size: 44px; letter-spacing: 0.12em; opacity: 0; }
.bar { position: absolute; left: 0; right: 0; height: 120px; background: #000; z-index: 5; }
.bar.top { top: 0; } .bar.bot { bottom: 0; }
#grain { position: absolute; inset: -10%; pointer-events: none; z-index: 6; opacity: 0.16; mix-blend-mode: screen;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"); }
#root-in::after { content: ""; position: absolute; inset: 0; z-index: 7; pointer-events: none; background: radial-gradient(ellipse at 50% 50%, transparent 45%, rgba(0,0,0,0.75) 100%); }
#streak { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0; z-index: 4;
  background: linear-gradient(105deg, transparent 40%, rgba(255,255,255,0.22) 50%, transparent 60%); }
#flash { position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 60; }
#end { position: absolute; inset: 0; background: #000; opacity: 0; z-index: 50; }
#end-logo { position: absolute; left: 110px; top: 470px; width: 860px; }
#end-tag { position: absolute; left: 0; width: 1080px; top: 920px; text-align: center; font-size: 44px; font-weight: 800; letter-spacing: 0.04em; }
#end-tag span { color: #e8c26a; }
#end-cta { position: absolute; left: 0; width: 1080px; top: 1040px; text-align: center; font-family: "Archivo Black"; font-size: 92px; }
#end-cta span { color: #2962ff; }
#end-note { position: absolute; left: 0; width: 1080px; top: 1180px; text-align: center; font-size: 28px; font-weight: 700; letter-spacing: 0.12em; color: #8a8f98; }
#end-foot { position: absolute; left: 0; top: 1665px; width: 1080px; height: 255px; overflow: hidden; }
#end-foot img { width: 1080px; height: 255px; display: block; }
"""

# =====================================================================================================================
def lonely():
    f = Film("lonely")
    # beat effects on every beat of the first 20 beats
    f.word("l1", "I DON'T<br>CARE", 0, b(2), 170, 700)
    f.word("l2", "IF IT'S<br><span class='gold'>LONELY</span>", b(2), b(4), 170, 700)
    # at the top: a rally to a peak with a figure on it
    up = [(0, 40), (40, 90), (90, 160), (160, 240), (240, 330), (330, 440), (440, 560)]
    peak = (f'<g id="lt-p" opacity="0"><circle cx="830" cy="{1300 - 600}" r="26" fill="{GOLD}"/>'
            f'<path d="M 806 {1300 - 560} L 806 {1300 - 590} A 24 24 0 0 1 854 {1300 - 590} L 854 {1300 - 560} Z" fill="{GOLD}"/></g>'
            f'<text id="lt-n" x="540" y="1520" text-anchor="middle" font-family="Archivo Black" font-size="96" fill="{GOLD}" opacity="0">+$84,210</text>')
    f.svg("s-top", f.candles("lt", up, 220, 1300, 1.0, w=46, gap=100) + peak, b(4), b(8))
    f.tl(f'tl.to(".lt", {{opacity: 1, duration: 0.05, stagger: {BEAT / 3:.3f}}}, {b(4):.3f});')
    f.tl(f'tl.fromTo("#lt-p", {{opacity: 0, y: -60}}, {{opacity: 1, y: 0, duration: 0.2, ease: "back.out(2)"}}, {b(6):.3f});')
    f.tl(f'tl.fromTo("#lt-n", {{opacity: 0, scale: 1.6}}, {{opacity: 1, scale: 1, duration: 0.18, ease: "power4.out"}}, {b(6):.3f});')
    f.word("l3", "AT THE<br><span class='gold'>TOP</span>", b(4), b(8), 150, 300)
    f.word("l4", "IT WAS<br>LONELY", b(8), b(10), 170, 700)
    # at the bottom too: a one-beat montage
    f.word("l5", "AT THE<br>BOTTOM TOO", b(10), b(16), 118, 260)
    mont = [("3:00 AM", "LONDON OPEN", "#fff"), ("BACKTEST", "#247", "#fff"), ("-14%", "DRAWDOWN", RED),
            ("ACCOUNT", "BLOWN", RED), ("NOBODY", "CLAPPING", "#fff"), ("STILL", "HERE", GOLD)]
    for i, (a, c, col) in enumerate(mont):
        t0 = b(10 + i)
        f.M.append(f'<div id="m{i}" class="sub" style="top:900px;font-family:\'Archivo Black\';font-size:120px;letter-spacing:0;color:{col}">{a}'
                   f'<div style="font-family:Montserrat;font-weight:800;font-size:46px;letter-spacing:0.3em;color:#cfd3da;margin-top:14px">{c}</div></div>')
        f.tl(f'tl.fromTo("#m{i}", {{opacity: 0, scale: 1.3}}, {{opacity: 1, scale: 1, duration: 0.12, ease: "power4.out"}}, {t0:.3f});')
        f.tl(f'tl.set("#m{i}", {{opacity: 0}}, {t0 + BEAT - 0.02:.3f});')
    down = [(560, 480), (480, 400), (400, 300), (300, 200), (200, 110), (110, 30)]
    f.svg("s-bot", f.candles("lb", down, 270, 1560, 0.55, w=46, gap=110), b(10), b(16))
    f.tl(f'tl.to(".lb", {{opacity: 0.55, duration: 0.05, stagger: {BEAT:.3f}}}, {b(10):.3f});')
    f.word("l6", "SIT ON<br><span class='gold'>THAT.</span>", b(16), b(20), 190, 640)
    f.M.append('<div id="skull" class="sub" style="top:1150px;font-size:150px;letter-spacing:0;font-family:\'Noto Color Emoji\'">💀</div>')
    f.tl(f'tl.fromTo("#skull", {{opacity: 0, scale: 0.3, rotation: -30}}, {{opacity: 1, scale: 1, rotation: 0, duration: 0.25, ease: "back.out(3)"}}, {b(18):.3f});')
    f.tl(f'tl.set("#skull", {{opacity: 0}}, {b(20):.3f});')
    for k in range(20):                                     # a hit on every beat, harder on the downbeats
        t = b(k)
        f.punch(t, 1.18 if k % 2 == 0 else 1.08)
        if k % 2 == 0: f.flash(t, 0.45); f.cue(t, "hit", -2 if k % 4 == 0 else -6)
        else: f.cue(t, "tick.crisp", -6)
        if k in (4, 10, 16): f.shake(t, 22); f.invert(t); f.streak(t)
    f.cue(b(18), "pop", -1)
    f.endcard(b(20), voice=False)
    f.write(round(b(24), 2), "lonely")

def haters():
    f = Film("haters")
    LEAD = 0.3
    Wd = json.load(open(f"{ROOT}/work/words_haters.json"))["words"]
    def norm(s): return re.sub(r"[^a-z0-9']", "", s.lower())
    def at(word, k=1):
        n = 0
        for w in Wd:
            if norm(w["text"]) == word:
                n += 1
                if n == k: return round(LEAD + w["start"], 3)
        raise KeyError(word)
    vo_end = LEAD + Wd[-1]["end"]
    # phrase cards: (text html, start word, size, top)
    cards = [("YOU'LL NEVER<br>FIND A <span class='gold'>HATER</span>", ("you", 1), 140, 640),
             ("DOING BETTER<br>THAN YOU", ("doing", 1), 140, 640),
             ("THINK<br>ABOUT IT.", ("think", 1), 170, 680),
             ("PROFITABLE?", ("profitable", 1), 130, 360),
             ("\"IT'S LUCK\"", ("calling", 1), 140, 360),
             ("DISCIPLINED?", ("disciplined", 1), 130, 360),
             ("THEY <span style='color:#ff2d55'>BLEW</span><br>THEIR ACCOUNT", ("already", 1), 130, 360),
             ("YOU DIDN'T<br><span class='gold'>QUIT.</span>", ("you", 3), 136, 640),
             ("THEY DID.", ("they", 1), 150, 690),
             ("THEY<br><span style='color:#ff2d55'>HATE</span>", ("hate", 1), 190, 620),
             ("BECAUSE YOU<br>REMIND THEM", ("because", 1), 112, 650),
             ("OF THE TRADER<br>THEY COULD<br><span class='gold'>HAVE BEEN.</span>", ("of", 1), 102, 580)]
    starts = [at(*c[1]) - 0.04 for c in cards]
    starts[0] = 0.0                                          # the first card is the thumbnail
    for i, (txt, _, size, top) in enumerate(cards):
        t_out = starts[i + 1] if i + 1 < len(cards) else vo_end + 0.6
        f.word(f"h{i}", txt, starts[i], t_out, size, top)
        f.cue(starts[i], "whoosh.short", -9)
    # comment bubbles for "calling it luck"
    coms = ["just lucky 🍀", "it's a scam", "get a real job", "fake P&L", "gambling lol"]
    for i, c in enumerate(coms):
        x = 90 + (i % 2) * 380; y = 820 + i * 150
        f.M.append(f'<div id="cm{i}" class="sub" style="left:{x}px;width:auto;top:{y}px;font-size:42px;letter-spacing:0;padding:20px 30px;border-radius:30px;'
                   f'background:#1a1d24;border:2px solid #ffffff33;font-family:Montserrat,\'Noto Color Emoji\'">💬 {c}</div>')
        f.tl(f'tl.fromTo("#cm{i}", {{opacity: 0, y: 40, scale: 0.8}}, {{opacity: 1, y: 0, scale: 1, duration: 0.18, ease: "back.out(2)"}}, {at("calling") + i * BEAT / 2:.3f});')
        f.tl(f'tl.to("#cm{i}", {{opacity: 0, x: -60, duration: 0.15}}, {at("if", 2) - 0.1:.3f});')
        f.cue(at("calling") + i * BEAT / 2, "pop", -6)
    # the equity curve that keeps rising under "profitable"
    eq = f'<polyline id="eqc" points="120,1500 300,1380 420,1420 600,1220 760,1260 960,980" fill="none" stroke="{GOLD}" stroke-width="10" stroke-linejoin="round" stroke-dasharray="1200" stroke-dashoffset="1200"/>'
    f.svg("s-eq", eq, at("profitable") - 0.05, at("calling") - 0.05)
    f.tl(f'tl.to("#eqc", {{strokeDashoffset: 0, duration: 0.8, ease: "power2.out"}}, {at("profitable"):.3f});')
    # blown account: a candle crash through a stop line
    crash = f.candles("bl", [(300, 340), (340, 300), (300, 200), (200, 60), (60, -120)], 300, 1300, 1.0, w=50, gap=120)
    crash += '<line x1="120" y1="1200" x2="960" y2="1200" stroke="#fff" stroke-width="4" stroke-dasharray="16 12"/>'
    crash += f'<text x="960" y="1180" text-anchor="end" font-family="Montserrat" font-weight="800" font-size="34" letter-spacing="4" fill="#fff">STOP LOSS</text>'
    f.svg("s-bl", crash, at("disciplined") - 0.05, at("you", 3) - 0.05)
    f.tl(f'tl.to(".bl", {{opacity: 1, duration: 0.05, stagger: {BEAT / 2:.3f}}}, {at("laughing"):.3f});')
    # quitters fade out, you stay
    figs = "".join(f'<g class="qf" opacity="0"><circle cx="{220 + i * 160}" cy="1240" r="30" fill="#fff"/>'
                   f'<path d="M {192 + i * 160} 1350 L {192 + i * 160} 1310 A 28 28 0 0 1 {248 + i * 160} 1310 L {248 + i * 160} 1350 Z" fill="#fff"/></g>' for i in range(5))
    figs += (f'<g id="you" opacity="0"><circle cx="540" cy="1240" r="34" fill="{GOLD}"/>'
             f'<path d="M 508 1360 L 508 1316 A 32 32 0 0 1 572 1316 L 572 1360 Z" fill="{GOLD}"/></g>')
    f.svg("s-q", figs, at("you", 3) - 0.05, at("hate") - 0.05)
    f.tl(f'tl.to(".qf", {{opacity: 1, duration: 0.1}}, {at("you", 3):.3f});')
    f.tl(f'tl.to(".qf", {{opacity: 0, y: 60, duration: 0.25, stagger: 0.08}}, {at("they", 1):.3f});')
    f.tl(f'tl.to("#you", {{opacity: 1, duration: 0.15}}, {at("they", 1) + 0.2:.3f});')
    # the ghost of the trader they could have been
    ghost = (f'<g id="gh"><circle cx="540" cy="1150" r="70" fill="none" stroke="{GOLD}" stroke-width="5" stroke-dasharray="10 10"/>'
             f'<path d="M 470 1400 L 470 1300 A 70 70 0 0 1 610 1300 L 610 1400" fill="none" stroke="{GOLD}" stroke-width="5" stroke-dasharray="10 10"/></g>')
    f.svg("s-gh", ghost, at("of") - 0.05, vo_end + 0.6)
    f.tl(f'tl.fromTo("#gh", {{opacity: 0, scale: 0.8, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.6}}, {at("of"):.3f});')
    # the beat grid under the voice: punches on every downbeat, flashes on the bars
    nb = int((vo_end + 0.6) / BEAT)
    for k in range(nb):
        t = b(k)
        f.punch(t, 1.1 if k % 2 == 0 else 1.04)
        if k % 4 == 0: f.flash(t, 0.3)
    for w in (("blew", 1), ("hate", 1), ("been", 1)):
        f.shake(at(*w), 22); f.invert(at(*w)); f.streak(at(*w)); f.cue(at(*w), "hit", -1)
    f.cue(at("luck"), "snap", -3); f.cue(at("quit"), "tock", -2)
    f.cue(LEAD, "vo", 0, file="vo_haters")
    end_t = round(vo_end + 0.7, 2)
    f.endcard(end_t, voice=True)
    f.write(round(end_t + 0.3 + OUTRO[3] + 1.2, 2), "haters")

if __name__ == "__main__":
    lonely(); haters()
