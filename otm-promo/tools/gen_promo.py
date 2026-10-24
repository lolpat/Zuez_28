"""Generate the Order The Market x Limitless promo scenes (run: python3 tools/gen_promo.py .). Shot rects are in the 921x2000 display coords of the
original screenshots; each image entry says which crop of that screenshot the file holds."""
import json, os, sys

ROOT = sys.argv[1]
F = 1320 / 921
BG = "#08090a"
BLUE = "#4d8dff"
CX, CY, BOX_W, BOX_H = 1300, 540, 1040, 860  # where the camera puts the focus rect

IMAGES = {
    # name: (file, natural w, natural h, crop x, crop y in display coords)
    "dashboard": ("assets/screens/dashboard.png", 1320, 2393, 0, 130),
    "automation": ("assets/screens/automation-key.png", 831, 511, 300, 330),
    "alerts": ("assets/screens/alerts.png", 1320, 2393, 0, 130),
    "scanners": ("assets/screens/scanners.png", 1320, 2393, 0, 130),
    "ai": ("assets/screens/ai.png", 1320, 2393, 0, 130),
    "academy": ("assets/screens/academy-top.png", 867, 1154, 285, 280),
    "live": ("assets/screens/live.png", 1320, 2393, 0, 130),
    "journal": ("assets/screens/journal-stats.png", 867, 1491, 285, 410),
    "coach": ("assets/screens/coach.png", 1320, 2393, 0, 130),
    "risk": ("assets/screens/risk.png", 1320, 2393, 0, 130),
    "leaderboard": ("assets/screens/leaderboard.png", 1320, 2393, 0, 130),
    "xp": ("assets/screens/xp-trips.png", 867, 638, 285, 835),
}

# (kind, id, start, duration, payload)
SCENES = [
    ("otm", "otm", 0, 3.5, None),
    ("hook", "hook", 3.5, 4, None),
    ("screen", "dash", 7.5, 4, dict(img="dashboard", kicker="DASHBOARD",
        line="See when Asia, London and New York open.",
        shots=[(0, (285, 280, 600, 520)), (1.5, (430, 425, 420, 50))])),
    ("word", "w-signals", 11.5, 1.5, dict(text="SIGNALS", mode="slam")),
    ("screen", "alerts", 13, 4, dict(img="alerts", kicker="TRADE ALERTS",
        line="Four signal rooms. Pick the one that fits.",
        shots=[(0, (285, 280, 600, 330)), (1.0, (285, 615, 600, 420)), (2.5, (285, 1055, 600, 420))])),
    ("word", "w-auto", 17, 1.5, dict(text="AUTOMATE", mode="stretch")),
    ("screen", "auto", 18.5, 4, dict(img="automation", kicker="TRADING AUTOMATION",
        line="Connect once. Trades copy automatically.",
        shots=[(0, (300, 330, 580, 135)), (1.5, (300, 507, 580, 180))])),
    ("word", "w-plan", 22.5, 1.5, dict(text="PLAN", mode="slide")),
    ("screen", "ai", 24, 4, dict(img="ai", kicker="LIMITLESS AI",
        line="Get entry, stop loss and two targets.",
        shots=[(0, (300, 300, 570, 380)), (1.5, (335, 735, 500, 260)), (2.9, (505, 735, 330, 260))])),
    ("screen", "scan", 28, 3.5, dict(img="scanners", kicker="SCANNERS",
        line="New scanners on the way.",
        shots=[(0, (285, 540, 600, 560)), (1.5, (490, 690, 400, 400))])),
    ("word", "w-learn", 31.5, 1.5, dict(text="LEARN", mode="split")),
    ("screen", "academy", 33, 4, dict(img="academy", kicker="ACADEMY",
        line="Courses from beginner to advanced.",
        shots=[(0, (285, 280, 600, 190)), (1.5, (285, 560, 600, 520))])),
    ("screen", "live", 37, 4, dict(img="live", kicker="LIVE SESSIONS",
        line="Trade live with coaches every week.",
        shots=[(0, (300, 300, 570, 170)), (1.5, (300, 480, 570, 480))])),
    ("word", "w-track", 41, 1.5, dict(text="TRACK", mode="slam")),
    ("screen", "journal", 42.5, 4, dict(img="journal", kicker="TRADING JOURNAL",
        line="Every trade logged in your journal.",
        shots=[(0, (285, 480, 600, 290)), (1.5, (285, 795, 600, 650))])),
    ("screen", "coach", 46.5, 3.5, dict(img="coach", kicker="AI COACH",
        line="Nova, your AI coach, reviews your trading.",
        shots=[(0, (330, 470, 520, 290)), (1.5, (315, 785, 540, 190))])),
    ("screen", "risk", 50, 4, dict(img="risk", kicker="RISK CALCULATORS",
        line="The right lot size for your balance.",
        shots=[(0, (310, 140, 550, 390)), (1.5, (345, 680, 480, 460))])),
    ("word", "w-level", 54, 1.5, dict(text="LEVEL UP", mode="stretch")),
    ("screen", "board", 55.5, 2.5, dict(img="leaderboard", kicker="LEADERBOARD",
        line="Climb the monthly leaderboard.",
        shots=[(0, (285, 175, 600, 320)), (1.2, (285, 520, 600, 400))])),
    ("screen", "xp", 58, 2.5, dict(img="xp", kicker="XP STORE",
        line="Turn XP into real rewards.",
        shots=[(0, (285, 835, 605, 445)), (1.2, (285, 835, 605, 230))])),
    ("end", "end", 60.5, 5, None),
]

# The narration is the clock. Each scene starts LEAD seconds before its first word, measured in
# assets/vo/narration.wav with ElevenLabs Scribe word timestamps; the file plays from VO_AT.
VO_AT = 0.3
LEAD = 0.15
VO_END = 54.751  # last word ends
CUES = {
    "hook": 2.972, "dash": 6.246, "w-signals": 10.403, "alerts": 11.691, "w-auto": 15.488,
    "auto": 16.544, "w-plan": 20.224, "ai": 21.339, "scan": 25.727, "w-learn": 28.13,
    "academy": 29.28, "live": 31.961, "w-track": 34.458, "journal": 35.561, "coach": 38.173,
    "risk": 41.366, "w-level": 45.023, "board": 45.8, "xp": 47.542, "end": 50.723,
}
HOOK_WORDS = {"guessing": 3.355, "start": 4.052, "plan": 5.399}  # narration seconds
END_HOLD = 2.5  # the end card holds this long after the last word

_starts = {cid: 0 if cid == "otm" else round(CUES[cid] + VO_AT - LEAD, 3) for _, cid, *_ in SCENES}
TOTAL = round(VO_END + VO_AT + END_HOLD, 2)
_order = [cid for _, cid, *_ in SCENES]
SCENES = [(k, cid, _starts[cid],
           round((_starts[_order[i + 1]] if i + 1 < len(_order) else TOTAL) - _starts[cid], 3), p)
          for i, (k, cid, _, _, p) in enumerate(SCENES)]
HOOK_AT = {w: round(t + VO_AT - _starts["hook"], 3) for w, t in HOOK_WORDS.items()}
HOOK_AT["plan"] = min(HOOK_AT["plan"], round(HOOK_AT["start"] + 0.4, 3))  # long enough to read


def cam(img, rect, mult=1.0):
    _, w, h, ox, oy = IMAGES[img]
    x, y, rw, rh = [(v - o) * F for v, o in zip(rect, (ox, oy, 0, 0))]
    rw, rh = rect[2] * F, rect[3] * F
    s = min(BOX_W / rw, BOX_H / rh) * mult
    fx, fy = x + rw / 2, y + rh / 2
    return dict(x=round(CX - s * fx, 1), y=round(CY - s * fy, 1), scale=round(s, 4))


def wrap(cid, css, html, js):
    return f"""<template>
  <style>
    #root {{
      position: absolute;
      inset: 0;
      overflow: hidden;
      background: {BG};
    }}
{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080">
{html}
  </div>
  <script>
    (() => {{
      const tl = gsap.timeline({{ paused: true }});
{js}
      window.__timelines["{cid}"] = tl;
    }})();
  </script>
</template>
"""


def screen(cid, dur, p):
    file, w, h, *_ = IMAGES[p["img"]]
    words = "".join(f'<span class="{cid}-word">{wd}</span> ' for wd in p["line"].split()).strip()
    css = f"""    #{cid}-cam {{
      position: absolute;
      left: 0;
      top: 0;
      width: {w}px;
      height: {h}px;
    }}
    #{cid}-cam img {{
      display: block;
      width: 100%;
      height: 100%;
    }}
    #{cid}-scrim {{
      position: absolute;
      inset: 0;
      background: linear-gradient(90deg, rgba(8, 9, 10, 0.98) 0%, rgba(8, 9, 10, 0.96) 38%, rgba(8, 9, 10, 0) 54%);
    }}
    #{cid}-copy {{
      position: absolute;
      left: 120px;
      top: 0;
      bottom: 0;
      width: 620px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 26px;
    }}
    #{cid}-kicker {{
      font-family: "Inter", sans-serif;
      font-size: 28px;
      font-weight: 700;
      letter-spacing: 0.16em;
      color: {BLUE};
    }}
    #{cid}-line {{
      font-family: "Inter", sans-serif;
      font-size: 72px;
      font-weight: 700;
      line-height: 1.06;
      letter-spacing: -0.025em;
      color: #ffffff;
    }}
    .{cid}-word {{
      display: inline-block;
    }}"""
    html = f"""    <div id="{cid}-cam" data-layout-allow-overflow data-layout-ignore>
      <img id="{cid}-img" src="{file}" alt="" />
    </div>
    <div id="{cid}-scrim" data-layout-ignore></div>
    <div id="{cid}-copy">
      <div id="{cid}-kicker">{p["kicker"]}</div>
      <div id="{cid}-line">{words}</div>
    </div>"""
    shots = p["shots"]
    squeeze = min(1, (dur - 0.9) / (shots[-1][0] + 0.5))
    shots = [(round(t * squeeze, 3), r) for t, r in shots]
    first = cam(p["img"], shots[0][1])
    js = [f"      const shots = {json.dumps([dict(t=t, **cam(p['img'], r)) for t, r in shots])};",
          f'      const sel = "#{cid}-cam";',
          "      // Arrive slightly large and settle on the first framing.",
          f"      tl.fromTo(sel, {{ x: {cam(p['img'], shots[0][1], 1.12)['x']}, y: {cam(p['img'], shots[0][1], 1.12)['y']}, scale: {cam(p['img'], shots[0][1], 1.12)['scale']}, transformOrigin: \"0 0\", filter: \"blur(8px)\" }},",
          f"        {{ x: {first['x']}, y: {first['y']}, scale: {first['scale']}, filter: \"blur(0px)\", duration: 0.5, ease: \"expo.out\" }}, 0);",
          "      // Fast moves to each next framing, with a blur peak mid-move.",
          "      shots.slice(1).forEach((s) => {",
          "        tl.to(sel, { x: s.x, y: s.y, scale: s.scale, duration: 0.45, ease: \"power3.inOut\" }, s.t);",
          "        tl.to(sel, { filter: \"blur(6px)\", duration: 0.2, ease: \"power2.in\" }, s.t);",
          "        tl.to(sel, { filter: \"blur(0px)\", duration: 0.25, ease: \"power2.out\" }, s.t + 0.2);",
          "      });",
          "      // Copy: kicker, then the line word by word.",
          f'      tl.fromTo("#{cid}-kicker", {{ opacity: 0, x: -24 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "power4.out" }}, 0.15);',
          f'      tl.fromTo(".{cid}-word", {{ opacity: 0, filter: "blur(6px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.15, ease: "power2.out", stagger: 0.067 }}, 0.3);']
    last = shots[-1][1]
    out = cam(p["img"], last, 1.3)
    js += ["      // Zoom through on the way out; the cut lands on the beat.",
           f'      tl.to(sel, {{ x: {out["x"]}, y: {out["y"]}, scale: {out["scale"]}, filter: "blur(10px)", duration: 0.28, ease: "power3.in" }}, {dur - 0.3});',
           f'      tl.to("#{cid}-copy", {{ opacity: 0, filter: "blur(8px)", duration: 0.15, ease: "power2.in" }}, {dur - 0.2});']
    return wrap(cid, css, html, "\n".join(js))


def word(cid, dur, p):
    text = p["text"]
    size = min(300, int(1500 / (0.8 * len(text))))
    if p["mode"] == "split":
        letters = "".join(f'<span class="{cid}-ch">{c if c != " " else "&nbsp;"}</span>' for c in text)
    else:
        letters = text
    css = f"""    #{cid}-stage {{
      position: absolute;
      inset: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 28px;
    }}
    #{cid}-text {{
      font-family: "Archivo Black", sans-serif;
      font-size: {size}px;
      line-height: 1;
      letter-spacing: -0.01em;
      color: #ffffff;
      white-space: nowrap;
    }}
    .{cid}-ch {{
      display: inline-block;
    }}
    #{cid}-bar {{
      width: 360px;
      height: 14px;
      border-radius: 7px;
      background: {BLUE};
    }}"""
    html = f"""    <div id="{cid}-stage">
      <div id="{cid}-text">{letters}</div>
      <div id="{cid}-bar"></div>
    </div>"""
    t = f'"#{cid}-text"'
    mode = p["mode"]
    if mode == "slam":
        enter = f'tl.fromTo({t}, {{ scale: 1.6, opacity: 0, filter: "blur(12px)" }}, {{ scale: 1, opacity: 1, filter: "blur(0px)", duration: 0.3, ease: "power4.out" }}, 0);'
    elif mode == "stretch":
        enter = f'tl.fromTo({t}, {{ scaleY: 0.08, opacity: 0 }}, {{ scaleY: 1, opacity: 1, duration: 0.32, ease: "power4.out" }}, 0);'
    elif mode == "slide":
        enter = f'tl.fromTo({t}, {{ x: 520, opacity: 0, filter: "blur(14px)" }}, {{ x: 0, opacity: 1, filter: "blur(0px)", duration: 0.3, ease: "expo.out" }}, 0);'
    else:  # split
        enter = (f'tl.fromTo(".{cid}-ch", {{ y: (i) => (i % 2 ? 160 : -160), opacity: 0 }}, '
                 f'{{ y: 0, opacity: 1, duration: 0.32, ease: "power4.out", stagger: 0.035 }}, 0);')
    js = f"""      {enter}
      tl.fromTo("#{cid}-bar", {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.3, ease: "power3.out" }}, 0.25);
      tl.to("#{cid}-stage", {{ opacity: 0, scale: 0.92, filter: "blur(10px)", duration: 0.15, ease: "power3.in" }}, {dur - 0.17});"""
    return wrap(cid, css, html, js)


def hook(cid, dur):
    css = f"""    .hook-screen {{
      position: absolute;
      inset: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      font-family: "Archivo Black", sans-serif;
      color: #ffffff;
      line-height: 0.95;
      text-align: center;
    }}
    .hook-big {{
      font-size: 250px;
    }}
    .hook-mid {{
      font-size: 190px;
    }}
    .hook-accent {{
      color: {BLUE};
    }}"""
    html = """    <div id="hook-a" class="hook-screen">
      <div id="hook-stop" class="hook-big">STOP</div>
      <div id="hook-guess" class="hook-big hook-accent">GUESSING.</div>
    </div>
    <div id="hook-b" class="hook-screen">
      <div id="hook-trade" class="hook-mid">TRADE GOLD</div>
      <div id="hook-plan" class="hook-mid">WITH A <span class="hook-accent">PLAN.</span></div>
    </div>"""
    g, b, pl = HOOK_AT["guessing"], HOOK_AT["start"], HOOK_AT["plan"]
    js = f"""      // Screen 1, then screen 2, each word landing as the voice says it.
      tl.fromTo("#hook-stop", {{ scale: 1.12, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "power4.out" }}, 0);
      tl.fromTo("#hook-guess", {{ x: -700, opacity: 0, filter: "blur(16px)" }}, {{ x: 0, opacity: 1, filter: "blur(0px)", duration: 0.3, ease: "expo.out" }}, {g});
      tl.to("#hook-a", {{ opacity: 0, scale: 0.9, filter: "blur(10px)", duration: 0.15, ease: "power3.in" }}, {round(b - 0.17, 3)});
      tl.fromTo("#hook-b", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01 }}, {b});
      tl.fromTo("#hook-trade", {{ scaleY: 0.08, opacity: 0 }}, {{ scaleY: 1, opacity: 1, duration: 0.3, ease: "power4.out" }}, {b});
      tl.fromTo("#hook-plan", {{ scale: 1.5, opacity: 0, filter: "blur(12px)" }}, {{ scale: 1, opacity: 1, filter: "blur(0px)", duration: 0.3, ease: "power4.out" }}, {pl});
      tl.to("#hook-b", {{ opacity: 0, scale: 0.92, filter: "blur(10px)", duration: 0.15, ease: "power3.in" }}, {round(dur - 0.17, 3)});"""
    return wrap(cid, css, html, js)


def otm(cid, dur):
    css = """    #otm-stage {
      position: absolute;
      inset: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }
    #otm-logo {
      width: 1000px;
      height: auto;
    }
    #otm-presents {
      margin-top: 40px;
      font-family: "Inter", sans-serif;
      font-size: 34px;
      font-weight: 700;
      letter-spacing: 0.5em;
      color: #e5cf86;
    }"""
    html = """    <div id="otm-stage">
      <img id="otm-logo" src="assets/screens/otm-logo.png" alt="Order The Market" />
      <div id="otm-presents">PRESENTS</div>
    </div>"""
    js = """      tl.fromTo("#otm-logo", { opacity: 0.5, scale: 0.92, filter: "blur(6px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.6, ease: "expo.out" }, 0);
      tl.fromTo("#otm-presents", { opacity: 0, y: 24, filter: "blur(6px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.5, ease: "power3.out" }, 0.9);
      tl.to("#otm-stage", { opacity: 0, scale: 0.94, filter: "blur(10px)", duration: 0.2, ease: "power3.in" }, EXIT_AT);""".replace("EXIT_AT", str(round(dur - 0.22, 3)))
    return wrap(cid, css, html, js)


def end(cid, dur):
    css = f"""    #root {{
      background: #0a111d;
    }}
    #end-stage {{
      position: absolute;
      inset: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }}
    #end-logo {{
      width: 780px;
      height: auto;
    }}
    #end-line {{
      margin-top: 48px;
      font-family: "Inter", sans-serif;
      font-size: 52px;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: #ffffff;
    }}
    #end-cta {{
      margin-top: 52px;
      padding: 30px 68px;
      border-radius: 999px;
      background: #2f6bff;
      font-family: "Inter", sans-serif;
      font-size: 42px;
      font-weight: 700;
      color: #ffffff;
      box-shadow: 0 0 60px rgba(47, 107, 255, 0.45);
    }}
    #end-by {{
      margin-top: 52px;
      display: flex;
      align-items: center;
      gap: 20px;
      font-family: "Inter", sans-serif;
      font-weight: 700;
      color: #e5cf86;
    }}
    #end-by-label {{
      font-size: 28px;
      letter-spacing: 0.3em;
      color: #9aa3b2;
    }}
    #end-otm {{
      width: 96px;
      height: 96px;
    }}
    #end-by-name {{
      font-size: 36px;
      letter-spacing: 0.22em;
    }}
    #end-risk {{
      margin-top: 36px;
      font-family: "Inter", sans-serif;
      font-size: 28px;
      color: #9aa3b2;
    }}"""
    html = """    <div id="end-stage">
      <img id="end-logo" src="assets/screens/logo.png" alt="Limitless" />
      <div id="end-line">Your all-in-one gold trading hub.</div>
      <div id="end-cta">Start your free trial</div>
      <div id="end-by">
        <span id="end-by-label">PRESENTED BY</span>
        <img id="end-otm" src="assets/screens/otm-mark.png" alt="" />
        <span id="end-by-name">ORDER THE MARKET</span>
      </div>
      <div id="end-risk">Order The Market is an independent Limitless affiliate. Trading involves substantial risk of loss.</div>
    </div>"""
    js = """      tl.fromTo("#end-logo", { clipPath: "inset(0% 100% 0% 0%)", opacity: 1 }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power3.out" }, 0);
      tl.fromTo("#end-line", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power2.out" }, 0.35);
      tl.fromTo("#end-cta", { opacity: 0, scale: 0.9, y: 24 }, { opacity: 1, scale: 1, y: 0, duration: 0.45, ease: "expo.out" }, 0.55);
      tl.fromTo("#end-by", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }, 1.0);
      tl.fromTo("#end-risk", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out" }, 1.1);"""
    return wrap(cid, css, html, js)

# Sound (PROMPT 13 + voiceover). Each clip starts so its peak lands one frame after its picture.
FRAME = 1 / 30
SFX_FILES = {  # name: (file, duration, seconds from file start to peak, volume under the voice)
    "tick": ("assets/sfx/tick.wav", 0.09, 0.001, 1.6),
    "snap": ("assets/sfx/snap.wav", 0.16, 0.005, 1.8),
    "switch": ("assets/sfx/switch.wav", 0.14, 0.047, 1.4),
    "chime": ("assets/sfx/chime.wav", 0.95, 0.163, 2.0),
}
SFX = []  # (name, film second the picture happens)
for kind, cid, start, dur, p in SCENES:
    if kind == "screen":
        SFX.append(("tick", start + 0.15))  # the kicker lands
        SFX += [("switch", start + t) for t, _ in p["shots"][1:]]  # each camera move
    elif kind == "word":
        SFX.append(("snap", start))  # the big word slams in
    elif kind == "hook":
        SFX += [("snap", start + HOOK_AT["guessing"]), ("snap", start + HOOK_AT["start"]), ("snap", start + HOOK_AT["plan"])]
    elif kind == "end":
        SFX.append(("chime", start))  # the last card
        SFX.append(("tick", start + 1.0))  # presented by Order The Market
    elif kind == "otm":
        SFX.append(("chime", start))  # the presenter's logo

# Voiceover: ElevenLabs "Everett - Confident American Ads", one continuous take (assets/vo/narration.wav).
VO = [("narration", 54.75, VO_AT)]

hosts = []
for kind, cid, start, dur, p in SCENES:
    body = {"screen": lambda: screen(cid, dur, p), "word": lambda: word(cid, dur, p),
            "hook": lambda: hook(cid, dur), "end": lambda: end(cid, dur), "otm": lambda: otm(cid, dur)}[kind]()
    with open(os.path.join(ROOT, "compositions", f"{cid}.html"), "w") as fh:
        fh.write(body)
    hosts.append(f"""      <div
        id="{cid}"
        class="clip"
        data-composition-id="{cid}"
        data-composition-src="compositions/{cid}.html"
        data-start="{start}"
        data-duration="{dur}"
        data-track-index="0"
        data-track-kind="graphics"
        data-width="1920"
        data-height="1080"
      ></div>""")

for i, (name, at) in enumerate(SFX, 1):
    file, length, peak, vol = SFX_FILES[name]
    begin = round(at + FRAME - peak, 3)
    hosts.append(f"""      <audio
        id="sfx-{i:02d}-{name}"
        class="clip"
        src="{file}"
        data-start="{begin}"
        data-duration="{length}"
        data-track-index="1"
        data-volume="{vol}"
      ></audio>""")

for name, length, at in VO:
    hosts.append(f"""      <audio
        id="{name}"
        class="clip"
        src="assets/vo/{name}.wav"
        data-start="{at}"
        data-duration="{length}"
        data-track-index="2"
        data-volume="1"
      ></audio>""")

index = f"""<!doctype html>
<html lang="en" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <!-- GSAP 3.14.2, vendored so renders don't depend on a CDN -->
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      @font-face {{
        font-family: "Inter";
        src: url("assets/fonts/Inter-400.woff2") format("woff2");
        font-weight: 400;
      }}
      @font-face {{
        font-family: "Inter";
        src: url("assets/fonts/Inter-700.woff2") format("woff2");
        font-weight: 700;
      }}
      @font-face {{
        font-family: "Archivo Black";
        src: url("assets/fonts/ArchivoBlack-400.woff2") format("woff2");
        font-weight: 400;
      }}
      * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }}
      html,
      body {{
        margin: 0;
        width: 1920px;
        height: 1080px;
        overflow: hidden;
        background: {BG};
      }}
      #root {{
        width: 100%;
        height: 100%;
      }}
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-duration="{TOTAL}"
      data-width="1920"
      data-height="1080"
    >
{chr(10).join(hosts)}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
with open(os.path.join(ROOT, "index.html"), "w") as fh:
    fh.write(index)
print("scenes:", len(SCENES))
