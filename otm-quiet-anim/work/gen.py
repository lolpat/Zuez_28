"""OTM Quiet: a minimal black-screen narration. Words fade in as the voice says them; the key words sit on a bigger
second line; a small OTM emblem stays at the bottom. Writes ../index.html.
Group syntax: "small words / second small line | BIG LINE". Word timings come from words_take1.json (faster-whisper)."""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT_CY = 700                   # words sit higher so the line drawings fit underneath
LEAD = 0.3                      # voice starts 0.3 s in, so frame 0 already shows the first line (thumbnail)
GOLD = "#e8c26a"

GROUPS = [
    "the market will humble you | in private",
    "before it ever pays you | in public.",
    "watch | closely.",
    "everyone sees the | green screenshot.",
    "nobody sees the | hours behind it.",
    "the backtests. / the journals.",
    "the trades you | didn't take.",
    "| why?",
    "because discipline is | quiet.",
    "it doesn't post. / it doesn't brag.",
    "it waits for the | setup",
    "and lets everything else go.",
    "most traders lose themselves",
    "chasing the | next trade.",
    "do not | chase the market.",
    "that is where | accounts disappear.",
    "if you have to force a trade / just to feel something,",
    "the market has already told you | everything.",
    "progress does not always come with | applause.",
    "sometimes, the clearest proof / that you've grown",
    "is a week of | doing nothing,",
    "and still | being right.",
    "| ORDER / THE MARKET.",
    "don't let the market | order you.",
    "follow for more.",
]
GOLD_GROUPS = {21, 22}

def norm(s): return re.sub(r"[^a-z0-9']", "", s.lower())

words = json.load(open(f"{ROOT}/work/words_take1.json"))
toks = []
for g in GROUPS:
    for part in re.split(r"(\||/)", g):
        if part in ("|", "/"): continue
        toks += part.split()
assert len(toks) == len(words), (len(toks), len(words))
for a, w in zip(toks, words):
    assert norm(a) == norm(w["text"]), (a, w["text"])

T, M = [], []
def tl(s): T.append(s)

wi = 0
plan = []
for gi, g in enumerate(GROUPS):
    small, big = (g.split("|") + [""])[:2] if "|" in g else (g, "")
    lines = [l.strip() for l in small.split("/") if l.strip()]
    gw = []
    for li, line in enumerate(lines):
        gw.append([("s", li, w) for w in line.split()])
    for bi, bl in enumerate(l.strip() for l in big.split("/") if l.strip()):
        gw.append([("b", bi, w) for w in bl.split()])
    flat = [x for line in gw for x in line]
    times = words[wi:wi + len(flat)]; wi += len(flat)
    plan.append((gi, gw, times))

def big_size(text):
    est = 0.74 if text.isupper() else 0.56                    # rough average glyph width of Montserrat 700, in em
    return int(max(64, min(112, 900 / (est * max(6, len(text))))))

total = round(words[-1]["end"] + LEAD + 4.2, 2)
END_T = round(words[-1]["end"] + LEAD + 0.55, 2)

G = []
for gi, gw, times in plan:
    n_small = sum(1 for line in gw if line[0][0] == "s")
    has_big = any(line[0][0] == "b" for line in gw)
    first = times[0]["start"] + LEAD
    last = times[-1]["end"] + LEAD
    open_t = 0.0 if gi == 0 else round(first - 0.12, 3)
    if gi + 1 < len(plan):
        nxt = plan[gi + 1][2][0]["start"] + LEAD - 0.12
        close_t = min(nxt, last + 1.4)
    else:
        close_t = END_T
    close_t = round(close_t, 3)
    G.append(dict(o=open_t, c=close_t, w=[round(x["start"] + LEAD, 3) for x in times]))
    # vertical layout: block centred on y = 900
    bigs = [" ".join(w for _, _, w in line) for line in gw if line[0][0] == "b"]
    fs_big = min(big_size(t) for t in bigs) if bigs else 0
    hs, hb = 62, fs_big * 1.15 * len(bigs)
    block = n_small * hs + hb + (14 if has_big and n_small else 0)
    y = TEXT_CY - block / 2
    html = ""
    k = 0
    for line in gw:
        kind = line[0][0]
        text = " ".join(w for _, _, w in line)
        if kind == "s":
            style = f"top:{y:.0f}px;font-size:44px;font-weight:600"
            y += hs
        else:
            y += 14 if (n_small and line[0][1] == 0) else 0
            fs = fs_big
            col = f";color:{GOLD}" if gi in GOLD_GROUPS else ""
            ls = ";letter-spacing:0.04em" if text.isupper() else ""
            style = f"top:{y:.0f}px;font-size:{fs}px;font-weight:700{col}{ls}"
            y += fs * 1.15
        spans = ""
        for _, _, w in line:
            spans += f'<span class="w" id="g{gi}w{k}">{w}</span> '; k += 1
        html += f'<div class="ln" style="{style}">{spans.strip()}</div>'
    M.append(f'<div class="grp" id="g{gi}" data-layout-allow-overlap>{html}</div>')
    tl(f'tl.set("#g{gi}", {{opacity: 1, visibility: "visible"}}, {open_t:.3f});')
    tl(f'tl.fromTo("#g{gi}", {{scale: 0.985}}, {{scale: 1.015, duration: {max(0.5, close_t - open_t):.3f}, ease: "none"}}, {open_t:.3f});')
    for j, w in enumerate(times):
        t0 = max(0.0, w["start"] + LEAD - 0.06)
        frm, blur = (0.3, 0) if gi == 0 else (0, 6)
        tl(f'tl.fromTo("#g{gi}w{j}", {{opacity: {frm}, y: {0 if gi == 0 else 8}, filter: "blur({blur}px)"}}, '
           f'{{opacity: 1, y: 0, filter: "blur(0px)", duration: 0.3, ease: "power2.out", immediateRender: {"true" if gi == 0 else "false"}}}, {t0:.3f});')
    tl(f'tl.to("#g{gi}", {{opacity: 0, duration: 0.18, ease: "power2.in"}}, {close_t - 0.18:.3f});')
    tl(f'tl.set("#g{gi}", {{opacity: 0, visibility: "hidden"}}, {close_t:.3f});')

# line drawings under the words, dust behind everything, sound cues for the mix
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import illus
CUES = []
M.insert(0, illus.build(G, tl, lambda t, snd, gain: CUES.append(dict(t=round(t, 3), snd=snd, gain=gain)), total))
tl(f'tl.to("#mark", {{opacity: 0, duration: 0.3}}, {G[22]["o"]:.3f});')
tl(f'tl.to("#mark", {{opacity: 0.92, duration: 0.4}}, {G[24]["o"]:.3f});')
json.dump(G, open(f"{ROOT}/work/groups.json", "w"))
json.dump(sorted(CUES, key=lambda c: c["t"]), open(f"{ROOT}/work/cues.json", "w"), indent=0)

# emblem stays at the bottom, then the end card takes over
tl(f'tl.to("#mark", {{opacity: 0, duration: 0.4}}, {END_T - 0.2:.3f});')
tl(f'tl.set("#end", {{opacity: 1, visibility: "visible"}}, {END_T:.3f});')
tl(f'tl.fromTo("#end-logo", {{opacity: 0, y: 20, filter: "blur(10px)"}}, {{opacity: 1, y: 0, filter: "blur(0px)", duration: 0.9, ease: "power2.out"}}, {END_T:.3f});')
tl(f'tl.fromTo("#end-note", {{opacity: 0}}, {{opacity: 1, duration: 0.6}}, {END_T + 0.5:.3f});')
tl(f'tl.fromTo("#end-credit", {{opacity: 0}}, {{opacity: 1, duration: 0.6}}, {END_T + 0.7:.3f});')
tl(f'tl.fromTo("#end-foot-img", {{y: 255}}, {{y: 0, duration: 0.6, ease: "power3.out"}}, {END_T + 0.3:.3f});')
tl(f'tl.fromTo("#end-logo", {{scale: 1}}, {{scale: 1.04, duration: {total - END_T:.3f}, ease: "none", immediateRender: false}}, {END_T:.3f});')

CREDIT = 'music: “Piece of Quiet” by geoffpeters · CC BY 3.0'
CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #000; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #000; font-family: Montserrat, sans-serif; color: #fff; }
.grp { position: absolute; inset: 0; opacity: 0; visibility: hidden; transform-origin: 50% 36%; }
#dust, #ill { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }
#ill { filter: drop-shadow(0 0 6px rgba(255,255,255,0.28)); }
.ln { position: absolute; left: 0; width: 1080px; text-align: center; line-height: 1.15; white-space: nowrap;
  text-shadow: 0 0 18px rgba(255,255,255,0.35), 0 0 4px rgba(255,255,255,0.25); }
.w { display: inline-block; opacity: 0; }
#mark { position: absolute; left: 485px; top: 1500px; width: 110px; opacity: 0.92; filter: drop-shadow(0 0 10px rgba(255,255,255,0.25)); }
#end { position: absolute; inset: 0; background: #000; opacity: 0; visibility: hidden; z-index: 20; }
#end-logo { position: absolute; left: 190px; top: 640px; width: 700px; }
#end-note { position: absolute; left: 0; width: 1080px; top: 1060px; text-align: center; font-size: 28px; font-weight: 600; letter-spacing: 0.12em; color: #8a8f98; }
#end-credit { position: absolute; left: 0; width: 1080px; top: 1112px; text-align: center; font-size: 28px; font-weight: 500; color: #8a8f98; }
#end-foot { position: absolute; left: 0; top: 1665px; width: 1080px; height: 255px; overflow: hidden; }
#end-foot img { width: 1080px; height: 255px; display: block; }
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
    <div id="root" data-composition-id="otm-quiet-anim" data-start="0" data-duration="{total}" data-width="1080" data-height="1920">
{chr(10).join("      " + m for m in M)}
      <img id="mark" src="assets/otm_emblem.png" alt="OTM" />
      <div id="end"><img id="end-logo" src="assets/otm_logo.png" alt="Order the Market" />
        <div id="end-note">EDUCATIONAL ONLY · NOT FINANCIAL ADVICE</div>
        <div id="end-credit">{CREDIT}</div>
        <div id="end-foot"><img id="end-foot-img" src="assets/footer.jpg" alt="" /></div></div>
      <audio id="otm-quiet-anim-audio" class="clip" src="assets/audio/mix_quiet_anim.wav" data-start="0" data-duration="{total}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-quiet-anim"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
json.dump(dict(total=total, lead=LEAD, end_t=END_T), open(f"{ROOT}/work/timing.json", "w"))
print("cues", len(CUES), "total", total, "end", END_T, "groups", len(plan), "lines", len(T))
