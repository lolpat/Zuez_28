"""OTM "why price moves" animation (third reference): one idea per scene in glowing line icons, phrase captions,
the OTM outro. Sound: the earshot kit (work/kit.json) placed on the cue frames by work/mix_kit.py.

Outputs: index.html and work/cues.json.
"""
import json, os, random
from common import *
from scenes import SCENES, KEY

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
        if n: C.append(dict(t=t_in, snd="whoosh.short", gain=-8))
    cm, ct = captions(end_t)
    C += [dict(t=0, snd="bed", file="bed"), dict(t=LEAD, snd="vo", file="vo_main", gain=0),
          dict(t=end_t, snd="whoosh.long", gain=-1), dict(t=end_t + 0.25, snd="hit", gain=-1),
          dict(t=vo_o, snd="vo", file="vo_outro", gain=0), dict(t=vo_o + OUTRO[1], snd="pop", gain=-3),
          dict(t=vo_o + OUTRO[2], snd="land", gain=0)]
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
    <div id="root" data-composition-id="otm-pricemoves" data-start="0" data-duration="{total}" data-width="{W}" data-height="{H}" data-motion-blur="on">
      <div id="vig"></div>
      <div id="stage"><svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="gl"><stop offset="0" stop-color="#fff" stop-opacity="0.5"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs><g id="dustg">{dust}</g>
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
        window.__timelines["otm-pricemoves"] = tl;
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
