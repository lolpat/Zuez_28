"""OTM "5 Rules to Order the Market": a neon trading-terminal design. Navy-black, electric blue #2962ff and gold,
a moving 3D grid floor, glass HUD panels, a price ticker, scanlines, particles, chromatic number slams (after the
registry's headline-slam), RGB wipe transitions (after chromatic-aberration-wipe), typing fields and a clicking
cursor (after agent-cursor), rolling counters (after number-wheel), HUD brackets (after telemetry-hud) and a
three-frame stage shake on every landing.

Inputs: work/words.json (word timings of assets/audio/vo_main.wav). Outputs: index.html, work/cues.json.
Cue `snd` names are roles of the earshot "launch" kit (work/kit.json) or "file" for a rendered bank sound.
"""
import json, math, os, random, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1080, 1920
LEAD = 0.3
BLUE, GOLD, NAVY, CYAN = "#2962ff", "#e8c26a", "#05070f", "#5ad1ff"
MONO = "'JetBrains Mono', 'DejaVu Sans Mono', monospace"
WORDS = [w for w in json.load(open(f"{ROOT}/work/words.json"))["words"] if w["type"] == "word"]
def norm(s): return re.sub(r"[^a-z0-9']", "", s.lower())
def at(word, k=1):
    n = 0
    for w in WORDS:
        if norm(w["text"]) == word:
            n += 1
            if n == k: return round(LEAD + w["start"], 2)
    raise KeyError(word, k)

T, C, M = [], [], []          # timeline lines, sound cues, markup
rnd = random.Random(7)
def tl(s): T.append(s)
def cue(t, snd, gain=0, **kw): C.append(dict(t=round(t, 3), snd=snd, gain=gain, **kw))

# ---------------------------------------------------------------------------------------------------------------------
# effect helpers
def shake(sel, t, amp=14, frames=3):
    """the headline-slam landing: a deterministic three-frame stage shake"""
    f = 1 / 30
    for i in range(frames):
        tl(f'tl.set("{sel}", {{x: {amp if i % 2 == 0 else -amp * 0.7:.1f}, y: {-amp * 0.5 if i % 2 == 0 else amp * 0.35:.1f}}}, {t + i * f:.3f});')
    tl(f'tl.set("{sel}", {{x: 0, y: 0}}, {t + frames * f:.3f});')

def slam(sel, t, frm=1.7, d=0.42):
    tl(f'tl.fromTo("{sel}", {{opacity: 0, scale: {frm}, filter: "blur(18px)"}}, {{opacity: 1, scale: 1, filter: "blur(0px)", duration: {d}, ease: "expo.out"}}, {t:.2f});')
    shake("#cam", t + d * 0.55)

def rgb(selbase, t, steps=6, amp=16):
    """chromatic split on the stacked red/cyan copies of a word"""
    for s in range(steps + 1):
        dx = 0 if s == steps else rnd.choice([-1, 1]) * rnd.uniform(amp * 0.3, amp)
        tl(f'tl.set("{selbase} .r", {{x: {dx:.1f}, y: {0 if s == steps else rnd.uniform(-3, 3):.1f}}}, {t + s * 0.04:.2f});')
        tl(f'tl.set("{selbase} .c", {{x: {-dx:.1f}}}, {t + s * 0.04:.2f});')

def typed(eid, text, t, cps=22, sound=True, cls="ty"):
    """a field that types itself with a caret (set steps, so any frame shows the right characters)"""
    M_ = f'<span id="{eid}" class="{cls}"></span><span id="{eid}-k" class="caret"></span>'
    for i in range(len(text) + 1):
        tl(f'tl.set("#{eid}", {{textContent: {json.dumps(text[:i])}}}, {t + i / cps:.3f});')
        if sound and i and text[i - 1] != " " and i % 2 == 1: cue(t + i / cps, "key", -6)
    tl(f'tl.fromTo("#{eid}-k", {{opacity: 1}}, {{opacity: 0, duration: 0.25, repeat: 7, yoyo: true, ease: "steps(1)"}}, {t:.2f});')
    tl(f'tl.set("#{eid}-k", {{opacity: 0}}, {t + len(text) / cps + 2.0:.2f});')
    return M_

def roll(eid, a, b, t, d, fmt="${:,.0f}", steps=24):
    """a rolling counter in set steps (after number-wheel)"""
    for k in range(steps + 1):
        f = 1 - (1 - k / steps) ** 3
        tl(f'tl.set("#{eid}", {{textContent: {json.dumps(fmt.format(a + (b - a) * f))}}}, {t + d * k / steps:.3f});')

def wipe(t):
    """RGB-split wipe between rules (after chromatic-aberration-wipe): three bars sweep across, the stage blurs"""
    tl(f'tl.fromTo(".wp", {{xPercent: -110}}, {{xPercent: 110, duration: 0.55, ease: "power3.inOut", stagger: 0.04, immediateRender: false}}, {t - 0.3:.2f});')
    tl(f'tl.fromTo("#flash", {{opacity: 0.55}}, {{opacity: 0, duration: 0.25, immediateRender: false}}, {t:.2f});')
    cue(t - 0.3, "whoosh.long", -3)

def cam_push(t0, t1, s0=1.0, s1=1.07):
    tl(f'tl.fromTo("#cam", {{scale: {s0}}}, {{scale: {s1}, duration: {max(0.5, t1 - t0):.2f}, ease: "none", immediateRender: false}}, {t0:.2f});')

def rule_card(n, name, t_in, t_out):
    """big chromatic number + title, top of the frame"""
    rid = f"rc{n}"
    M.append(f'<div id="{rid}" class="rc"><div class="lab">RULE</div>'
             f'<div class="num" data-layout-allow-overlap><span class="r">0{n}</span><span class="c">0{n}</span><b>0{n}</b></div>'
             f'<div class="nm">{name}</div></div>')
    tl(f'tl.set("#{rid}", {{opacity: 1}}, {t_in - 0.01:.2f});')
    slam(f"#{rid} .num", t_in, 2.2, 0.38)
    rgb(f"#{rid} .num", t_in + 0.05)
    tl(f'tl.fromTo("#{rid} .lab", {{opacity: 0, y: 10}}, {{opacity: 1, y: 0, duration: 0.3}}, {t_in:.2f});')
    tl(f'tl.fromTo("#{rid} .nm", {{opacity: 0, clipPath: "inset(0% 100% 0% 0%)"}}, {{opacity: 1, clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power3.out"}}, {t_in + 0.45:.2f});')
    tl(f'tl.to("#{rid}", {{opacity: 0, y: -40, filter: "blur(12px)", duration: 0.25}}, {t_out - 0.3:.2f});')
    cue(t_in - 1.0, "riser", -6)
    cue(t_in + 0.2, "hit", 0)
    cue(t_in + 0.45, "whoosh.short", -6)

def panel(pid, inner, top=560, h=760, t_in=0, t_out=0):
    M.append(f'<div id="{pid}" class="pn" style="top:{top}px;height:{h}px"><div class="br tl"></div><div class="br tr"></div>'
             f'<div class="br bl"></div><div class="br brr"></div>{inner}</div>')
    tl(f'tl.fromTo("#{pid}", {{opacity: 0, rotationX: 28, y: 80, scale: 0.92, transformPerspective: 1200}}, '
       f'{{opacity: 1, rotationX: 0, y: 0, scale: 1, duration: 0.6, ease: "power3.out"}}, {t_in:.2f});')
    tl(f'tl.fromTo("#{pid} .br", {{scale: 1.6, opacity: 0}}, {{scale: 1, opacity: 1, duration: 0.35, stagger: 0.05, ease: "back.out(2)"}}, {t_in + 0.2:.2f});')
    tl(f'tl.to("#{pid}", {{opacity: 0, scale: 1.08, filter: "blur(14px)", duration: 0.3, ease: "power2.in"}}, {t_out - 0.32:.2f});')
    cue(t_in, "land", -3)

def svg_candles(seq, x0, base, sc, w=26, gap=40, cls="cd"):
    out = ""
    for i, (o, c) in enumerate(seq):
        x = x0 + i * gap; top, bot = base - max(o, c) * sc, base - min(o, c) * sc
        col = BLUE if c >= o else "#e9edf5"
        out += (f'<g class="{cls}" opacity="0"><line x1="{x}" y1="{top - 10}" x2="{x}" y2="{bot + 10}" stroke="{col}" stroke-width="3"/>'
                f'<rect x="{x - w / 2}" y="{top:.1f}" width="{w}" height="{max(3, bot - top):.1f}" fill="{col}"/></g>')
    return out

# ---------------------------------------------------------------------------------------------------------------------
R = [at("rule", k) for k in range(1, 6)]
END_VO = LEAD + WORDS[-1]["end"]
END_T = round(END_VO + 0.7, 2)
VO_O = round(END_T + 0.3, 2)
OUTRO = [0.0, 1.32, 3.34, 4.09]
TOTAL = round(VO_O + OUTRO[3] + 1.3, 2)

# ---- intro: a giant chromatic 5 ---------------------------------------------------------------------------------------
M.append('<div id="intro"><div class="five" data-layout-allow-overlap><span class="r">5</span><span class="c">5</span><b>5</b></div>'
         f'<div class="ititle"><div class="l1">RULES TO</div><div class="l2">ORDER THE MARKET</div></div></div>')
tl('tl.set("#intro", {opacity: 1}, 0);')
slam("#intro .five", 0.12, 3.0, 0.5)
rgb("#intro .five", 0.15, 8, 26)
tl(f'tl.fromTo("#intro .l1", {{opacity: 0, y: 40}}, {{opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)"}}, {at("rules", 1):.2f});')
tl(f'tl.fromTo("#intro .l2", {{opacity: 0, scale: 1.4, filter: "blur(12px)"}}, {{opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.4, ease: "expo.out"}}, {at("order", 1):.2f});')
shake("#cam", at("market", 1), 10)
tl(f'tl.fromTo("#intro .l2", {{backgroundPosition: "-300% 0"}}, {{backgroundPosition: "300% 0", duration: 0.9, ease: "power2.inOut"}}, {at("market", 1):.2f});')
tl(f'tl.to("#intro", {{opacity: 0, scale: 1.3, filter: "blur(16px)", duration: 0.35, ease: "power2.in"}}, {R[0] - 0.35:.2f});')
cue(0.12, "hit", 2); cue(0.15, "swell", -4, align_note="reverse swell lands on the slam")
cue(at("rules", 1), "pop", -3); cue(at("order", 1), "snap", -2); cue(at("market", 1), "drop", -2)

# ---- rule 1: risk 1% --------------------------------------------------------------------------------------------------
rule_card(1, "RISK 1%", R[0], R[1])
wipe(R[0])
t1 = at("risk")
calc = (f'<div class="row"><span class="k">ACCOUNT</span><span class="v" id="r1-acc">$0</span></div>'
        f'<div class="row"><span class="k">RISK</span><span class="v gold" id="r1-pct">0.0%</span></div>'
        f'<div class="row big"><span class="k">MAX LOSS</span><span class="v blue" id="r1-max">$0</span></div>'
        f'<div class="gauge"><svg viewBox="0 0 400 220"><path d="M 30 200 A 170 170 0 0 1 370 200" stroke="#ffffff22" stroke-width="22" fill="none" stroke-linecap="round"/>'
        f'<path id="r1-arc" d="M 30 200 A 170 170 0 0 1 370 200" stroke="{GOLD}" stroke-width="22" fill="none" stroke-linecap="round" stroke-dasharray="535" stroke-dashoffset="535"/>'
        f'<line id="r1-cap" x1="56" y1="150" x2="22" y2="128" stroke="#ff4d5e" stroke-width="6" opacity="0"/></svg>'
        f'<div class="glab" id="r1-lock">MAX 1% · LOCKED</div></div>'
        f'<div class="cal" id="r1-cal">' + "".join(f'<i class="d{" bad" if i == 7 else ""}"></i>' for i in range(20)) + '</div>')
panel("p1", calc, 560, 820, t1 - 0.1, R[1])
roll("r1-acc", 0, 10000, t1, 0.8)
roll("r1-pct", 0, 1.0, at("one", 2), 0.5, "{:.1f}%", 10)
roll("r1-max", 0, 100, at("percent"), 0.6, "${:,.0f}", 12)
tl(f'tl.to("#r1-arc", {{strokeDashoffset: 529, duration: 0.6, ease: "power2.out"}}, {at("percent"):.2f});')
tl(f'tl.fromTo("#r1-lock", {{opacity: 0, scale: 1.6}}, {{opacity: 1, scale: 1, duration: 0.3, ease: "back.out(3)"}}, {at("never", 1):.2f});')
shake("#cam", at("more") + 0.05, 8)
tl(f'tl.fromTo("#r1-cal .d", {{opacity: 0, scale: 0}}, {{opacity: 1, scale: 1, duration: 0.2, stagger: 0.03, ease: "back.out(3)"}}, {at("bad"):.2f});')
tl(f'tl.fromTo("#r1-cal .bad", {{backgroundColor: "#ffffff22"}}, {{backgroundColor: "#ff4d5e", duration: 0.1, repeat: 3, yoyo: true}}, {at("trade", 1):.2f});')
tl(f'tl.to("#r1-cal .d:not(.bad)", {{backgroundColor: "{BLUE}", duration: 0.2, stagger: 0.02}}, {at("month"):.2f});')
cue(t1, "tick.crisp", -2); cue(at("percent"), "bell", -4); cue(at("never", 1), "snap", -1); cue(at("bad"), "pop", -6); cue(at("month"), "click.confirm", -3)
cam_push(R[0], R[1])

# ---- rule 2: levels before the session ---------------------------------------------------------------------------------
rule_card(2, "LEVELS FIRST", R[1], R[2])
wipe(R[1])
t2 = at("mark")
lv = [(330, "PDH", GOLD), (470, "KEY LEVEL", CYAN), (600, "PDL", GOLD)]
lines = "".join(f'<line class="r2-l" x1="40" y1="{y}" x2="900" y2="{y}" stroke="{c}" stroke-width="4" stroke-dasharray="860" stroke-dashoffset="860"/>'
                f'<text class="r2-t" x="900" y="{y - 12}" text-anchor="end" fill="{c}" font-family="Montserrat" font-weight="800" font-size="28" letter-spacing="4" opacity="0">{n}</text>' for y, n, c in lv)
seq = [(0, 40), (40, 90), (90, 140), (140, 185), (185, 150), (150, 110), (110, 70), (70, 120), (120, 190), (190, 260), (260, 215)]
cds = svg_candles(seq, 80, 620, 1.55, cls="r2-c")
clock = (f'<div class="clock"><div class="ck-l">LONDON OPEN</div><div class="ck-t" id="r2-clk">00:03:00</div></div>')
panel("p2", clock + f'<svg class="chart" viewBox="0 0 940 680">{lines}{cds}</svg>', 560, 820, t2 - 0.15, R[2])
for k, s in enumerate(("00:03:00", "00:02:00", "00:01:00", "00:00:30", "00:00:10", "00:00:00")):
    tl(f'tl.set("#r2-clk", {{textContent: "{s}"}}, {t2 + k * 0.32:.2f});')
tl(f'tl.to("#r2-clk", {{color: "{BLUE}", textShadow: "0 0 30px {BLUE}", duration: 0.2}}, {at("opens"):.2f});')
tl(f'tl.to(".r2-l", {{strokeDashoffset: 0, duration: 0.45, stagger: 0.18, ease: "power2.inOut"}}, {at("levels"):.2f});')
tl(f'tl.to(".r2-t", {{opacity: 1, duration: 0.2, stagger: 0.18}}, {at("levels") + 0.3:.2f});')
tl(f'tl.to(".r2-c", {{opacity: 1, duration: 0.12, stagger: 0.12}}, {at("not"):.2f});')
cue(at("levels"), "whoosh.short", -4); cue(at("levels") + 0.2, "tick", -3); cue(at("levels") + 0.38, "tick", -3); cue(at("levels") + 0.56, "tick", -3)
cue(at("opens"), "click.confirm", -2); cue(at("not"), "tock", -4)
cam_push(R[1], R[2], 1.0, 1.06)

# ---- rule 3: confirmation ----------------------------------------------------------------------------------------------
rule_card(3, "WAIT FOR CONFIRMATION", R[2], R[3])
wipe(R[2])
t3 = at("wait")
seq3 = [(330, 290), (290, 240), (240, 200), (200, 160), (160, 120), (120, 100), (100, 92)]
c3 = svg_candles(seq3, 90, 640, 1.5, w=34, gap=58, cls="r3-c")
eng = (f'<g id="r3-e" opacity="0"><line x1="{90 + 7 * 58}" y1="{640 - 380 * 1.5 - 12}" x2="{90 + 7 * 58}" y2="{640 - 70 * 1.5 + 12}" stroke="{BLUE}" stroke-width="4"/>'
       f'<rect x="{90 + 7 * 58 - 24}" y="{640 - 380 * 1.5}" width="48" height="{310 * 1.5}" fill="{BLUE}"/></g>')
lvl3 = f'<line id="r3-l" x1="40" y1="{640 - 95 * 1.5}" x2="900" y2="{640 - 95 * 1.5}" stroke="{GOLD}" stroke-width="4" opacity="0"/>'
q = f'<text id="r3-q" x="760" y="420" text-anchor="middle" fill="#fff" font-family="Playfair Display" font-style="italic" font-size="200" opacity="0">?</text>'
ring = f'<circle id="r3-r" cx="{90 + 6 * 58}" cy="{640 - 95 * 1.5}" r="40" stroke="{GOLD}" stroke-width="4" fill="none" opacity="0"/>'
stamp = (f'<div id="r3-s" class="stamp">CONFIRMED <span>✓</span></div>')
panel("p3", f'<svg class="chart" viewBox="0 0 940 680">{lvl3}{c3}{ring}{eng}{q}</svg>' + stamp, 560, 820, t3 - 0.15, R[3])
tl(f'tl.to("#r3-l", {{opacity: 1, duration: 0.3}}, {t3:.2f});')
tl(f'tl.to(".r3-c", {{opacity: 1, duration: 0.12, stagger: 0.14}}, {at("confirmation"):.2f});')
tl(f'tl.fromTo("#r3-r", {{opacity: 1, scale: 0.4, transformOrigin: "50% 50%"}}, {{opacity: 0, scale: 2.4, duration: 0.8, repeat: 2, ease: "power2.out"}}, {at("level", 1):.2f});')
tl(f'tl.fromTo("#r3-q", {{opacity: 0, scale: 2, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)"}}, {at("question"):.2f});')
tl(f'tl.to("#r3-q", {{rotation: 12, duration: 0.15, yoyo: true, repeat: 3, transformOrigin: "50% 80%"}}, {at("question") + 0.4:.2f});')
tl(f'tl.to("#r3-q", {{opacity: 0, scale: 0.5, duration: 0.2}}, {at("candle") - 0.1:.2f});')
tl(f'tl.fromTo("#r3-e", {{opacity: 1, scaleY: 0, transformOrigin: "50% 100%"}}, {{scaleY: 1, duration: 0.6, ease: "expo.out"}}, {at("candle"):.2f});')
tl(f'tl.fromTo("#r3-s", {{opacity: 0, scale: 2.4, rotation: -14}}, {{opacity: 1, scale: 1, rotation: -6, duration: 0.22, ease: "power4.in"}}, {at("answer"):.2f});')
shake("#cam", at("answer") + 0.22, 16)
cue(at("confirmation"), "tock", -4); cue(at("level", 1), "tick", -2); cue(at("question"), "pop", -2); cue(at("candle"), "riser", -10)
cue(at("answer") + 0.22, "drop", 0); cue(at("answer") + 0.25, "bell", -3)
cam_push(R[2], R[3], 1.0, 1.08)

# ---- rule 4: exit before entry -----------------------------------------------------------------------------------------
rule_card(4, "EXIT BEFORE ENTRY", R[3], R[4])
wipe(R[3])
t4 = at("know")
ticket = (f'<div class="tk"><div class="tk-h"><span>XAUUSD</span><span class="blue">MARKET ORDER</span></div>'
          f'<div class="fld" id="r4-f1"><span class="k">STOP LOSS</span><span class="val red">{typed("r4-sl", "2,371.50", at("stop"))}</span></div>'
          f'<div class="fld" id="r4-f2"><span class="k">TAKE PROFIT</span><span class="val blue">{typed("r4-tp", "2,410.00", at("target"))}</span></div>'
          f'<div class="fld"><span class="k">R : R</span><span class="val gold" id="r4-rr">—</span></div>'
          f'<div class="btns"><div class="b sell">SELL</div><div class="b buy" id="r4-buy">BUY</div></div>'
          f'<div id="r4-ok" class="toast">✓ ORDER FILLED · 1:3</div></div>'
          f'<div id="r4-cur" class="cur"><svg viewBox="0 0 40 40"><path d="M4 2 L4 32 L12 24 L18 38 L24 35 L18 22 L30 22 Z" fill="#fff" stroke="#000" stroke-width="2"/></svg>'
          f'<div class="cl">YOU</div></div><div id="r4-rip" class="rip"></div>')
panel("p4", ticket, 560, 820, t4 - 0.15, R[4])
tl(f'tl.fromTo("#r4-f1", {{borderColor: "#ffffff22"}}, {{borderColor: "#ff4d5e", duration: 0.2}}, {at("stop"):.2f});')
tl(f'tl.fromTo("#r4-f2", {{borderColor: "#ffffff22"}}, {{borderColor: "{BLUE}", duration: 0.2}}, {at("target"):.2f});')
tl(f'tl.set("#r4-rr", {{textContent: "1 : 3"}}, {at("second"):.2f});')
tl(f'tl.fromTo("#r4-rr", {{scale: 1.6}}, {{scale: 1, duration: 0.3, ease: "back.out(3)"}}, {at("second"):.2f});')
tl(f'tl.fromTo("#r4-cur", {{opacity: 0, x: 900, y: 900}}, {{opacity: 1, x: 690, y: 560, duration: 0.7, ease: "power3.out"}}, {at("then", 1) - 0.4:.2f});')
tl(f'tl.to("#r4-cur", {{scale: 0.85, duration: 0.08, yoyo: true, repeat: 1}}, {at("click"):.2f});')
tl(f'tl.fromTo("#r4-rip", {{opacity: 0.9, scale: 0.2}}, {{opacity: 0, scale: 2.6, duration: 0.5, ease: "power2.out"}}, {at("click"):.2f});')
tl(f'tl.to("#r4-buy", {{backgroundColor: "#ffffff", color: "{BLUE}", duration: 0.08, yoyo: true, repeat: 1}}, {at("click"):.2f});')
tl(f'tl.fromTo("#r4-ok", {{opacity: 0, y: 30}}, {{opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)"}}, {at("click") + 0.2:.2f});')
cue(at("stop"), "tock", -4); cue(at("target"), "tock", -4); cue(at("second"), "pop", -3); cue(at("then", 1) - 0.4, "whoosh.short", -9)
cue(at("click"), "click", 2); cue(at("click") + 0.2, "click.confirm", -2)
cam_push(R[3], R[4], 1.0, 1.06)

# ---- rule 5: journal ---------------------------------------------------------------------------------------------------
rule_card(5, "JOURNAL EVERY TRADE", R[4], at("five", 3))
wipe(R[4])
t5 = at("journal")
rows = [("MON", "XAUUSD", "+3.0R", True), ("TUE", "EURUSD", "-1.0R", False), ("WED", "GBPUSD", "+2.1R", True), ("THU", "XAUUSD", "-1.0R", False), ("FRI", "NAS100", "+3.4R", True)]
tbl = "".join(f'<div class="jr" id="r5-r{i}"><span>{d}</span><span>{p}</span><span class="{"blue" if ok else "red"}">{r}</span>'
              f'<span class="tag" id="r5-t{i}">{"✓ RULES" if ok else "LESSON"}</span></div>' for i, (d, p, r, ok) in enumerate(rows))
eq = f'<svg class="eq" viewBox="0 0 900 220"><polyline id="r5-eq" points="0,200 180,120 360,150 540,90 720,120 900,20" fill="none" stroke="{GOLD}" stroke-width="6" stroke-linejoin="round" stroke-dasharray="1100" stroke-dashoffset="1100"/></svg>'
stats = f'<div class="st"><span class="k">WIN RATE</span><span class="v" id="r5-wr">0%</span><span class="k">NET</span><span class="v blue" id="r5-net">+0.0R</span></div>'
panel("p5", f'<div class="jh"><span>DAY</span><span>PAIR</span><span>RESULT</span><span>NOTE</span></div>{tbl}{stats}{eq}', 560, 820, t5 - 0.15, at("five", 3))
for i in range(5):
    tl(f'tl.fromTo("#r5-r{i}", {{opacity: 0, x: -60}}, {{opacity: 1, x: 0, duration: 0.25, ease: "power3.out"}}, {at("every", 1) + i * 0.22:.2f});')
    cue(at("every", 1) + i * 0.22, "key", -3)
tl(f'tl.fromTo("[id^=r5-t]", {{opacity: 0, scale: 1.5}}, {{opacity: 1, scale: 1, duration: 0.25, stagger: 0.12, ease: "back.out(3)"}}, {at("past"):.2f});')
roll("r5-wr", 0, 60, at("best"), 0.7, "{:.0f}%", 14)
roll("r5-net", 0, 6.5, at("best"), 0.7, "+{:.1f}R", 14)
tl(f'tl.to("#r5-eq", {{strokeDashoffset: 0, duration: 1.2, ease: "power2.inOut"}}, {at("teacher"):.2f});')
cue(at("past"), "pop", -4); cue(at("best"), "tick.crisp", -2); cue(at("teacher"), "whoosh.short", -6); cue(at("have"), "bell", -4)
cam_push(R[4], at("five", 3), 1.0, 1.06)

# ---- finale ------------------------------------------------------------------------------------------------------------
tf = at("five", 3)
chips = ["RISK 1%", "LEVELS FIRST", "CONFIRMATION", "EXIT FIRST", "JOURNAL"]
M.append('<div id="fin">' + "".join(f'<div class="chip" id="ch{i}"><b>0{i + 1}</b>{c}</div>' for i, c in enumerate(chips)) +
         '<div id="emo"><div class="em">FEAR</div><div class="em">GREED</div><div class="em">FOMO</div></div>'
         '<div class="otm" data-layout-allow-overlap><span class="r">ORDER THE MARKET</span><span class="c">ORDER THE MARKET</span><b>ORDER THE MARKET</b></div>'
         '<div id="streak"></div></div>')
wipe(tf)
tl(f'tl.set("#fin", {{opacity: 1}}, {tf - 0.05:.2f});')
for i in range(5):
    tl(f'tl.fromTo("#ch{i}", {{opacity: 0, x: {(-1) ** i * 700}, rotation: {(-1) ** i * 12}}}, {{opacity: 1, x: 0, rotation: 0, duration: 0.4, ease: "back.out(1.6)"}}, {tf + i * 0.12:.2f});')
    cue(tf + i * 0.12, "pop", -3)
tl(f'tl.fromTo("#emo .em", {{opacity: 0, scale: 0.5}}, {{opacity: 1, scale: 1, duration: 0.25, stagger: 0.08, ease: "back.out(2)"}}, {at("no") - 0.1:.2f});')
tl(f'tl.to("#emo .em", {{textDecoration: "line-through", color: "#ff4d5e", duration: 0.01, stagger: 0.1}}, {at("emotions"):.2f});')
tl(f'tl.to("#emo .em", {{opacity: 0, y: 40, duration: 0.3, stagger: 0.05}}, {at("emotions") + 0.6:.2f});')
tl(f'tl.to(".chip", {{opacity: 0.25, scale: 0.9, duration: 0.3}}, {at("that's") - 0.2:.2f});')
slam("#fin .otm", at("order", 2) - 0.1, 2.4, 0.45)
rgb("#fin .otm", at("order", 2), 8, 22)
tl(f'tl.set("#streak", {{opacity: 1}}, {at("market", 2):.2f});')
tl(f'tl.fromTo("#streak", {{xPercent: -100}}, {{xPercent: 100, duration: 0.7, ease: "power2.inOut", immediateRender: false}}, {at("market", 2):.2f});')
tl(f'tl.set("#streak", {{opacity: 0}}, {at("market", 2) + 0.72:.2f});')
cue(at("emotions"), "snap", -1); cue(at("order", 2) - 1.4, "riser", -4); cue(at("order", 2), "hit", 3); cue(at("order", 2) + 0.02, "drop", 0)
cue(at("market", 2), "whoosh.short", -4)

# ---- persistent layers: grid floor, ticker, particles, HUD -------------------------------------------------------------
tl('tl.set(".wp", {xPercent: -110}, 0);')
tl(f'tl.fromTo("#gridin", {{y: 0}}, {{y: 120, duration: 1.2, ease: "none", repeat: {int(TOTAL / 1.2)}}}, 0);')
tl(f'tl.fromTo("#tick", {{x: 0}}, {{x: -3600, duration: {TOTAL}, ease: "none"}}, 0);')
for i in range(40):
    x, s, d = rnd.uniform(0, W), rnd.uniform(2, 5), rnd.uniform(4, 9)
    M.append(f'<i class="pt" id="pt{i}" style="left:{x:.0f}px;width:{s:.1f}px;height:{s:.1f}px;background:{rnd.choice([BLUE, CYAN, GOLD, "#fff"])}"></i>')
    tl(f'tl.fromTo("#pt{i}", {{y: {rnd.uniform(1900, 2100):.0f}, opacity: 0}}, {{y: {rnd.uniform(-200, 600):.0f}, opacity: {rnd.uniform(0.3, 0.8):.2f}, duration: {d:.1f}, repeat: {int(TOTAL / d) + 1}, ease: "none"}}, {rnd.uniform(0, 4):.2f});')
tl(f'tl.fromTo("#glowA", {{x: -120, y: -60}}, {{x: 120, y: 80, duration: 9, yoyo: true, repeat: 5, ease: "sine.inOut"}}, 0);')
tl(f'tl.fromTo("#glowB", {{x: 100, y: 60}}, {{x: -120, y: -80, duration: 11, yoyo: true, repeat: 4, ease: "sine.inOut"}}, 0);')
tl(f'tl.fromTo("#scan", {{y: -200}}, {{y: 2100, duration: 3.2, repeat: {int(TOTAL / 3.2)}, ease: "none"}}, 0);')
t = 0.0
while t < END_T:
    tl(f'tl.set("#tc", {{textContent: "REC ● {int(t // 60):02d}:{int(t % 60):02d}:{int((t % 1) * 30):02d}"}}, {t:.2f});'); t += 1 / 3

# ---- captions -----------------------------------------------------------------------------------------------------------
KEY = {"risk", "one", "percent", "levels", "confirmation", "candle", "answer", "exit", "entry", "stop", "loss", "target", "click",
       "journal", "teacher", "emotions", "order", "market", "question", "never"}
phr, cur = [], []
for i, w in enumerate(WORDS):
    cur.append(i)
    if w["text"][-1] in ".,:?" or len(cur) >= 5: phr.append(cur); cur = []
if cur: phr.append(cur)
for p, idx in enumerate(phr):
    t0 = LEAD + WORDS[idx[0]]["start"] - 0.05
    t1 = (LEAD + WORDS[phr[p + 1][0]]["start"] - 0.1) if p + 1 < len(phr) else END_T - 0.3
    html = " ".join(f'<span class="{"hl" if norm(WORDS[i]["text"]) in KEY else ""}">{WORDS[i]["text"]}</span>' for i in idx)
    M.append(f'<div class="cap" id="cp{p}">{html}</div>')
    tl(f'tl.fromTo("#cp{p}", {{opacity: 0, y: 20, scale: 0.9}}, {{opacity: 1, y: 0, scale: 1, duration: 0.18, ease: "back.out(2)"}}, {t0:.2f});')
    tl(f'tl.to("#cp{p}", {{opacity: 0, duration: 0.1}}, {max(t0 + 0.4, t1):.2f});')

# ---- end card -----------------------------------------------------------------------------------------------------------
tl(f'tl.to("#cam", {{opacity: 0, scale: 1.4, filter: "blur(14px)", duration: 0.4, ease: "power3.in"}}, {END_T - 0.4:.2f});')
tl(f'tl.fromTo("#flash", {{opacity: 0.9}}, {{opacity: 0, duration: 0.35, immediateRender: false}}, {END_T:.2f});')
tl(f'tl.fromTo("#end", {{opacity: 0}}, {{opacity: 1, duration: 0.05, immediateRender: false}}, {END_T:.2f});')
tl(f'tl.fromTo("#end-logo", {{opacity: 0, scale: 2.2, filter: "blur(14px)"}}, {{opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.5, ease: "expo.out"}}, {END_T + 0.1:.2f});')
tl(f'tl.fromTo("#end-tag", {{opacity: 0, y: 30}}, {{opacity: 1, y: 0, duration: 0.4, ease: "expo.out"}}, {VO_O + OUTRO[1]:.2f});')
tl(f'tl.fromTo("#end-cta", {{opacity: 0, clipPath: "inset(0% 100% 0% 0%)"}}, {{opacity: 1, clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power3.out"}}, {VO_O + OUTRO[2]:.2f});')
tl(f'tl.fromTo("#end-note", {{opacity: 0}}, {{opacity: 1, duration: 0.4}}, {END_T + 1.0:.2f});')
tl(f'tl.fromTo("#end-foot-img", {{y: 255}}, {{y: 0, duration: 0.5, ease: "back.out(1.2)"}}, {END_T + 0.9:.2f});')
cue(END_T - 0.4, "whoosh.long", 0); cue(END_T + 0.1, "hit", 0)
C += [dict(t=0, snd="bed", file="music"), dict(t=LEAD, snd="vo", file="vo_main", gain=0), dict(t=VO_O, snd="vo", file="vo_outro", gain=0),
      dict(t=VO_O + OUTRO[1], snd="pop", gain=-3), dict(t=VO_O + OUTRO[2], snd="land", gain=0)]

TICK = "   ".join(["XAUUSD 2,384.20 ▲ +0.42%", "EURUSD 1.0842 ▼ -0.11%", "GBPUSD 1.2731 ▲ +0.08%", "NAS100 18,412 ▲ +0.65%",
                   "USDJPY 151.32 ▼ -0.20%", "BTCUSD 67,940 ▲ +1.12%", "OIL 81.44 ▼ -0.35%"] * 4)

CSS = f"""
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: {NAVY}; }}
#root {{ position: relative; width: {W}px; height: {H}px; overflow: hidden; background: {NAVY}; font-family: Montserrat, sans-serif; color: #fff; }}
#glowA, #glowB {{ position: absolute; width: 1100px; height: 1100px; border-radius: 50%; filter: blur(60px); }}
#glowA {{ left: -400px; top: -300px; background: radial-gradient(circle, {BLUE}55, transparent 65%); }}
#glowB {{ right: -420px; bottom: 100px; background: radial-gradient(circle, {GOLD}33, transparent 65%); }}
#grid {{ position: absolute; left: -540px; right: -540px; bottom: 0; height: 640px; perspective: 520px; perspective-origin: 50% 0%; overflow: hidden;
  -webkit-mask-image: linear-gradient(transparent, #000 45%); mask-image: linear-gradient(transparent, #000 45%); }}
#gridin {{ position: absolute; left: 0; right: 0; top: 0; height: 2400px; transform-origin: 50% 0%; transform: rotateX(62deg);
  background-image: linear-gradient({BLUE}aa 2px, transparent 2px), linear-gradient(90deg, {BLUE}aa 2px, transparent 2px); background-size: 120px 120px; }}
#cam {{ position: absolute; inset: 0; transform-origin: 50% 48%; }}
#ticker {{ position: absolute; left: 0; right: 0; top: 64px; height: 56px; overflow: hidden; border-top: 1px solid {BLUE}66; border-bottom: 1px solid {BLUE}66;
  background: linear-gradient(90deg, {NAVY}, #0b1330, {NAVY}); }}
#tick {{ position: absolute; left: 0; top: 12px; white-space: nowrap; font-family: {MONO}; font-size: 26px; color: {CYAN}; letter-spacing: 2px; }}
#hud .b {{ position: absolute; width: 70px; height: 70px; border-color: {CYAN}aa; border-style: solid; }}
#hud .b1 {{ left: 26px; top: 140px; border-width: 3px 0 0 3px; }} #hud .b2 {{ right: 26px; top: 140px; border-width: 3px 3px 0 0; }}
#hud .b3 {{ left: 26px; bottom: 30px; border-width: 0 0 3px 3px; }} #hud .b4 {{ right: 26px; bottom: 30px; border-width: 0 3px 3px 0; }}
#tc {{ position: absolute; right: 44px; top: 150px; font-family: {MONO}; font-size: 28px; color: #ff4d5e; }}
#brand {{ position: absolute; left: 44px; top: 150px; font-family: {MONO}; font-size: 28px; color: {CYAN}aa; letter-spacing: 3px; }}
#scanl {{ position: absolute; inset: 0; background: repeating-linear-gradient(0deg, #ffffff08 0 2px, transparent 2px 5px); pointer-events: none; z-index: 30; }}
#scan {{ position: absolute; left: 0; right: 0; height: 180px; background: linear-gradient(transparent, {CYAN}14, transparent); z-index: 31; }}
.pt {{ position: absolute; top: 0; border-radius: 50%; box-shadow: 0 0 10px currentColor; opacity: 0; }}
.r, .c {{ position: absolute; left: 0; top: 0; mix-blend-mode: screen; }} .r {{ color: #ff2d55; }} .c {{ color: #22e5ff; }}
#intro {{ position: absolute; inset: 0; opacity: 0; }}
#intro .five {{ position: absolute; left: 0; right: 0; top: 330px; height: 760px; text-align: center; }}
#intro .five b, #intro .five span {{ font-family: 'Archivo Black'; font-size: 760px; line-height: 1; width: 100%; text-align: center; font-weight: 400; }}
#intro .five b {{ position: relative; color: #fff; text-shadow: 0 0 60px {BLUE}, 0 0 140px {BLUE}; }}
#intro .ititle {{ position: absolute; left: 0; right: 0; top: 1060px; text-align: center; }}
#intro .l1 {{ font-family: {MONO}; font-size: 44px; letter-spacing: 18px; color: {CYAN}; }}
#intro .l2 {{ font-family: 'Archivo Black'; font-size: 82px; margin-top: 10px;
  background: linear-gradient(100deg, #fff 40%, {GOLD} 50%, #fff 60%); background-size: 300% 100%; -webkit-background-clip: text; background-clip: text; color: transparent; }}
.rc {{ position: absolute; left: 0; right: 0; top: 190px; text-align: center; opacity: 0; }}
.rc .lab {{ font-family: {MONO}; font-size: 30px; letter-spacing: 14px; color: {CYAN}; }}
.rc .num {{ position: relative; display: inline-block; height: 220px; }}
.rc .num b, .rc .num span {{ font-family: 'Archivo Black'; font-size: 220px; line-height: 1; font-weight: 400; }}
.rc .num b {{ position: relative; color: #fff; text-shadow: 0 0 40px {BLUE}; }}
.rc .nm {{ font-family: 'Archivo Black'; font-size: 58px; color: {GOLD}; letter-spacing: 1px; margin-top: 6px; text-shadow: 0 0 24px {GOLD}66; }}
.pn {{ position: absolute; left: 60px; width: 960px; border-radius: 28px; padding: 44px 44px; opacity: 0;
  background: linear-gradient(160deg, #ffffff12, #ffffff05 40%, #2962ff10); border: 1px solid #ffffff22;
  box-shadow: 0 30px 80px #000a, inset 0 1px 0 #ffffff22, 0 0 60px {BLUE}22; backdrop-filter: blur(8px); }}
.pn .br {{ position: absolute; width: 40px; height: 40px; border-color: {GOLD}; border-style: solid; }}
.pn .tl {{ left: -6px; top: -6px; border-width: 4px 0 0 4px; border-radius: 10px 0 0 0; }} .pn .tr {{ right: -6px; top: -6px; border-width: 4px 4px 0 0; border-radius: 0 10px 0 0; }}
.pn .bl {{ left: -6px; bottom: -6px; border-width: 0 0 4px 4px; border-radius: 0 0 0 10px; }} .pn .brr {{ right: -6px; bottom: -6px; border-width: 0 4px 4px 0; border-radius: 0 0 10px 0; }}
.row {{ display: flex; justify-content: space-between; align-items: baseline; padding: 16px 6px; border-bottom: 1px solid #ffffff18; }}
.row .k, .fld .k, .st .k {{ font-family: {MONO}; font-size: 30px; letter-spacing: 4px; color: #aab4c8; }}
.row .v {{ font-family: 'Archivo Black'; font-size: 64px; }} .row.big .v {{ font-size: 92px; text-shadow: 0 0 30px {BLUE}; }}
.gold {{ color: {GOLD}; }} .blue {{ color: {BLUE}; }} .red {{ color: #ff4d5e; }}
.gauge {{ position: relative; width: 400px; margin: 18px auto 0; }} .gauge svg {{ width: 400px; height: 220px; }}
.glab {{ text-align: center; font-family: {MONO}; font-size: 28px; color: {GOLD}; letter-spacing: 3px; margin-top: -40px; opacity: 0; }}
.cal {{ display: grid; grid-template-columns: repeat(10, 1fr); gap: 10px; margin-top: 26px; }}
.cal .d {{ height: 40px; border-radius: 8px; background: #ffffff22; opacity: 0; }}
.clock {{ text-align: center; margin-bottom: 10px; }} .ck-l {{ font-family: {MONO}; font-size: 30px; letter-spacing: 8px; color: #aab4c8; }}
.ck-t {{ font-family: {MONO}; font-size: 96px; font-weight: 700; color: #fff; }}
.chart {{ width: 872px; height: 560px; }}
.stamp {{ position: absolute; right: 70px; top: 60px; padding: 14px 26px; border: 6px solid {GOLD}; border-radius: 14px; font-family: 'Archivo Black';
  font-size: 54px; color: {GOLD}; opacity: 0; text-shadow: 0 0 20px {GOLD}88; box-shadow: 0 0 30px {GOLD}55; }}
.tk-h {{ display: flex; justify-content: space-between; font-family: {MONO}; font-size: 34px; letter-spacing: 3px; padding-bottom: 20px; border-bottom: 1px solid #ffffff22; }}
.fld {{ display: flex; justify-content: space-between; align-items: center; margin-top: 26px; padding: 22px 26px; border-radius: 16px; border: 2px solid #ffffff22; background: #00000040; }}
.fld .val {{ font-family: {MONO}; font-size: 52px; font-weight: 700; min-height: 60px; }}
.caret {{ display: inline-block; width: 4px; height: 52px; background: #fff; margin-left: 6px; vertical-align: middle; opacity: 0; }}
.btns {{ display: flex; gap: 24px; margin-top: 40px; }} .b {{ flex: 1; text-align: center; padding: 30px; border-radius: 18px; font-family: 'Archivo Black'; font-size: 52px; }}
.b.sell {{ border: 2px solid #ffffff55; color: #ffffffaa; }} .b.buy {{ background: {BLUE}; box-shadow: 0 0 40px {BLUE}aa; }}
.toast {{ margin-top: 30px; text-align: center; padding: 22px; border-radius: 16px; background: {GOLD}; color: #000; font-family: 'Archivo Black'; font-size: 40px; opacity: 0; }}
.cur {{ position: absolute; left: 0; top: 0; width: 80px; opacity: 0; z-index: 20; }} .cur svg {{ width: 64px; height: 64px; }}
.cur .cl {{ display: inline-block; margin-left: 40px; padding: 4px 12px; border-radius: 8px; background: {GOLD}; color: #000; font-family: {MONO}; font-weight: 700; font-size: 28px; }}
.rip {{ position: absolute; left: 630px; top: 500px; width: 120px; height: 120px; border-radius: 50%; border: 6px solid #fff; opacity: 0; z-index: 19; }}
.jh, .jr {{ display: grid; grid-template-columns: 1fr 1.6fr 1.4fr 1.6fr; align-items: center; font-family: {MONO}; }}
.jh {{ font-size: 28px; color: #aab4c8; letter-spacing: 3px; padding-bottom: 14px; border-bottom: 1px solid #ffffff22; }}
.jr {{ font-size: 36px; padding: 16px 0; border-bottom: 1px solid #ffffff12; opacity: 0; }}
.jr .tag {{ font-size: 28px; padding: 6px 12px; border-radius: 8px; background: #ffffff14; color: {GOLD}; text-align: center; opacity: 0; }}
.st {{ display: flex; justify-content: space-between; align-items: baseline; margin-top: 22px; }} .st .v {{ font-family: 'Archivo Black'; font-size: 56px; }}
.eq {{ width: 872px; height: 200px; margin-top: 16px; }}
#fin {{ position: absolute; inset: 0; opacity: 0; }}
.chip {{ position: relative; margin: 0 auto 22px; width: 760px; padding: 22px 30px; border-radius: 18px; border: 2px solid {BLUE}; background: #0b1330cc;
  font-family: 'Archivo Black'; font-size: 46px; box-shadow: 0 0 30px {BLUE}55; opacity: 0; }}
.chip b {{ font-family: {MONO}; color: {GOLD}; margin-right: 26px; }}
#fin > .chip:first-child {{ margin-top: 330px; }}
#emo {{ position: absolute; left: 0; right: 0; top: 1010px; display: flex; justify-content: center; gap: 30px; }}
.em {{ font-family: 'Archivo Black'; font-size: 64px; color: #fff; opacity: 0; }}
.otm {{ position: absolute; left: 0; right: 0; top: 1150px; height: 140px; text-align: center; white-space: nowrap; }}
.otm b, .otm span {{ font-family: 'Archivo Black'; font-size: 82px; line-height: 1.3; width: 100%; text-align: center; font-weight: 400; }}
.otm b {{ position: relative; color: {GOLD}; text-shadow: 0 0 40px {GOLD}aa; }}
#streak {{ position: absolute; left: 0; top: 1150px; width: 100%; height: 130px; opacity: 0;
  background: linear-gradient(100deg, #ffffff00 44%, #ffffffaa 50%, #ffffff00 56%); mix-blend-mode: screen; }}
.wp {{ position: absolute; top: 0; bottom: 0; left: 0; width: 140%; z-index: 40; }}
.wp1 {{ background: linear-gradient(90deg, transparent, #ff2d5566 45%, transparent 55%); }}
.wp2 {{ background: linear-gradient(90deg, transparent, {BLUE}cc 48%, #ffffff 50%, {BLUE}cc 52%, transparent); }}
.wp3 {{ background: linear-gradient(90deg, transparent, #22e5ff66 45%, transparent 55%); }}
.cap {{ position: absolute; left: 80px; width: 920px; top: 1440px; text-align: center; font-size: 48px; font-weight: 800; opacity: 0; z-index: 35;
  padding: 18px 26px; border-radius: 22px; background: #05070fcc; border: 1px solid #ffffff1f; }}
.cap .hl {{ color: {GOLD}; }}
#flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 60; }}
#end {{ position: absolute; inset: 0; background: #000; opacity: 0; z-index: 50; }}
#end-logo {{ position: absolute; left: 110px; top: 470px; width: 860px; }}
#end-tag {{ position: absolute; left: 0; width: {W}px; top: 920px; text-align: center; font-size: 44px; font-weight: 800; letter-spacing: 0.04em; }}
#end-tag span {{ color: {GOLD}; }}
#end-cta {{ position: absolute; left: 0; width: {W}px; top: 1040px; text-align: center; font-family: "Archivo Black"; font-size: 92px; }}
#end-cta span {{ color: {BLUE}; }}
#end-note {{ position: absolute; left: 0; width: {W}px; top: 1180px; text-align: center; font-size: 28px; font-weight: 700; letter-spacing: 0.12em; color: #8a8f98; }}
#end-foot {{ position: absolute; left: 0; top: 1665px; width: {W}px; height: 255px; overflow: hidden; }}
#end-foot img {{ width: {W}px; height: 255px; display: block; }}
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
    <div id="root" data-composition-id="otm-rules" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}" data-motion-blur="on">
      <div id="glowA"></div><div id="glowB"></div>
      <div id="grid"><div id="gridin"></div></div>
      {"".join(m for m in M if m.startswith('<i class="pt"'))}
      <div id="cam" data-layout-allow-overlap>
{chr(10).join("        " + m for m in M if not m.startswith('<i class="pt"') and not m.startswith('<div class="cap"'))}
      </div>
      <div id="ticker"><div id="tick">{TICK}</div></div>
      <div id="hud"><i class="b b1"></i><i class="b b2"></i><i class="b b3"></i><i class="b b4"></i></div>
      <div id="brand">OTM://TERMINAL</div><div id="tc">REC ● 00:00:00</div>
{chr(10).join("      " + m for m in M if m.startswith('<div class="cap"'))}
      <div id="scanl"></div><div id="scan"></div>
      <div class="wp wp1"></div><div class="wp wp2"></div><div class="wp wp3"></div>
      <div id="end">
        <img id="end-logo" src="assets/otm_logo.png" alt="Order the Market" />
        <div id="end-tag">DON'T LET THE MARKET <span>ORDER YOU</span></div>
        <div id="end-cta">FOLLOW FOR <span>MORE</span></div>
        <div id="end-note">EDUCATIONAL ONLY · NOT FINANCIAL ADVICE</div>
        <div id="end-foot"><img id="end-foot-img" src="assets/footer.jpg" alt="" /></div>
      </div>
      <div id="flash"></div>
      <audio id="otm-audio" class="clip" src="assets/audio/mix.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-rules"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
if os.path.exists(f"{ROOT}/work/realsfx_added.json"): C += json.load(open(f"{ROOT}/work/realsfx_added.json"))   # moments Real SFX found uncued
json.dump(dict(total=TOTAL, cues=sorted(C, key=lambda c: c["t"])), open(f"{ROOT}/work/cues.json", "w"), indent=1)
print("total", TOTAL, "rules at", R, "lines", len(T), "cues", len(C))
