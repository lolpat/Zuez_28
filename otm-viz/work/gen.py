"""OTM Visualizer: the OTM emblem in a dark disk, ringed by a glowing shape that pulses to "Trap Monopoly" (Robbero,
CC BY 3.0), in a foggy night of candlestick towers with falling ash. The canvas is drawn from the hf-seek time with
baked audio envelopes (work/env.json); GSAP drives the DOM (timer, tagline, end card). Writes ../index.html."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = json.load(open(f"{ROOT}/work/env.json"))
TOTAL, DROP, SWITCH, END, BAR = E["total"], E["drop"], E["switch"], E["end"], E["bar"]
OUTRO = [0.0, 1.32, 3.34, 4.09]
CREDIT = "music: “Trap Monopoly” by Robbero · CC BY 3.0"

T = []
def tl(s): T.append(s)

# timer (one div per second) and tagline
timer = ""
for s in range(int(TOTAL) + 1):
    timer += f'<div class="tm" id="tm{s}">{s // 60}:{s % 60:02d}</div>'
    tl(f'tl.set("#tm{s}", {{opacity: 1}}, {s:.3f});')
    tl(f'tl.set("#tm{s}", {{opacity: 0}}, {min(TOTAL, s + 1):.3f});')
tl(f'tl.fromTo("#tag", {{opacity: 0, y: 12}}, {{opacity: 1, y: 0, duration: 1.2, ease: "power2.out"}}, 0.6);')
tl(f'tl.to(["#timer", "#tag"], {{opacity: 0, duration: 0.25}}, {END:.3f});')
# end card over the still-moving scene
tl(f'tl.fromTo("#end", {{opacity: 0}}, {{opacity: 1, duration: 0.3, ease: "power2.out"}}, {END + 0.05:.3f});')
tl(f'tl.fromTo("#end-logo", {{opacity: 0, scale: 2.2, filter: "blur(14px)"}}, {{opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.45, ease: "expo.out"}}, {END + 0.05:.3f});')
tl(f'tl.fromTo("#end-tag", {{opacity: 0, y: 30}}, {{opacity: 1, y: 0, duration: 0.3, ease: "expo.out"}}, {END + 0.3 + OUTRO[1]:.3f});')
tl(f'tl.fromTo("#end-cta", {{opacity: 0, scale: 1.4}}, {{opacity: 1, scale: 1, duration: 0.25, ease: "power4.out"}}, {END + 0.3 + OUTRO[2]:.3f});')
tl(f'tl.fromTo("#end-note", {{opacity: 0}}, {{opacity: 1, duration: 0.4}}, {END + 0.7:.3f});')
tl(f'tl.fromTo("#end-credit", {{opacity: 0}}, {{opacity: 1, duration: 0.4}}, {END + 0.9:.3f});')
tl(f'tl.fromTo("#end-foot-img", {{y: 255}}, {{y: 0, duration: 0.4, ease: "back.out(1.4)"}}, {END + 0.4:.3f});')

DATA = json.dumps(dict(fps=E["fps"], drop=DROP, switch=SWITCH, end=END, bar=BAR, total=TOTAL,
                       bass=E["bass"], mid=E["mid"], high=E["high"], kicks=E["kicks"], beats=E["beats"]), separators=(",", ":"))

JS = r"""
(function () {
  const D = __DATA__;
  const W = 1080, H = 1920, FPS = D.fps, CX = 540, CY = 880;
  const cv = document.getElementById("cv"), ctx = cv.getContext("2d");
  const logo = new Image(); logo.src = "assets/otm_emblem.png";
  const ready = new Promise((r) => { if (logo.complete && logo.naturalWidth) r(); else { logo.onload = () => r(); logo.onerror = () => r(); } });
  function rng(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  const hash = (n) => rng(n * 7919 + 13)();
  const R = rng(11);
  const fr = (t) => Math.max(0, Math.min(D.bass.length - 1, Math.round(t * FPS)));
  const ev = (a, t) => a[fr(t)] / 100;
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const ease = (u) => u * u * (3 - 2 * u);
  const KT = D.kicks.map((k) => k / FPS);
  function pulse(t) {
    let p = 0;
    for (const k of KT) if (k <= t && t - k < 0.6) p = Math.max(p, Math.exp(-(t - k) / 0.13));
    for (let i = 0; i < D.beats.length; i++) { const b = D.beats[i]; if (b <= t && t - b < 0.6) p = Math.max(p, (i % 2 ? 0.45 : 0.75) * Math.exp(-(t - b) / 0.12)); }
    return t < D.drop ? p * 0.35 : p;
  }
  const dist = (t) => (t < D.drop ? t : D.drop + (t - D.drop) * 1.8);

  // ---- seeded scene ----
  const P = []; for (let i = 0; i < 190; i++) { const z = R(); P.push({ x: R() * 1500 - 200, y: R() * 2100, z, v: 200 + 600 * z, a: 1.83 + R() * 0.14 }); }
  const BK = []; for (let i = 0; i < 46; i++) { BK.push({ t0: i * D.total / 46 + R() * 0.5, life: 0.8 + R() * 0.8, x: R() * 1200 - 60, y: R() * 1500 - 300,
    vx: (R() - 0.65) * 900, vy: 500 + R() * 900, r: 60 + R() * 170, a: 0.36 + R() * 0.26, keep: i % 3 === 0 }); }
  const FOG = []; for (let i = 0; i < 8; i++) FOG.push({ x: R() * 1080, y: 300 + R() * 1500, r: 450 + R() * 450, ph: R() * 6.28 });
  function row(n, x0, span, wmin, wmax, tmin, tmax) { const a = []; let x = x0; for (let i = 0; i < n; i++) { const w = wmin + R() * (wmax - wmin); a.push({ x, w, top: tmin + R() * (tmax - tmin), wick: 60 + R() * 160 }); x += span / n; } return a; }
  const FAR = row(24, -300, 1750, 34, 58, 980, 1480), NEAR = row(13, -260, 1700, 70, 120, 1180, 1660);
  const PATS = [
    [[-0.78, 0.36, 1], [0.78, 0.36, 1]],
    [[-Math.PI / 2, 0.55, 1], [Math.PI / 2, 0.55, 1]],
    [[-0.62, 0.26, 0.8], [0, 0.26, 1], [0.62, 0.26, 0.8]],
    [[Math.PI - 0.7, 0.4, 1], [Math.PI + 0.7, 0.4, 1]],
    [[0, 0.48, 1], [Math.PI, 0.48, 1]],
  ];
  function lob(pat, th, rot) { let s = 0; for (const [a, w, amp] of pat) { let d = th - (a + rot); d = Math.atan2(Math.sin(d), Math.cos(d)); s += amp * Math.exp(-(d * d) / (w * w)); } return Math.min(1.2, s); }
  function shape(th, t) {
    const rot = 0.2 * Math.sin(t * 0.9);
    if (t < D.drop) return 0.5 * lob(PATS[0], th, rot);
    const bar = Math.floor((t - D.drop) / (2 * D.bar)), k = bar % PATS.length, pk = (bar + PATS.length - 1) % PATS.length;
    const u = bar === 0 ? 1 : ease(clamp(((t - D.drop) - bar * 2 * D.bar) / 0.18, 0, 1));
    return lob(PATS[pk], th, rot) * (1 - u) + lob(PATS[k], th, rot) * u;
  }
  function blob(t, sc, extra) {
    const b = ev(D.bass, t), m = ev(D.mid, t), h = ev(D.high, t), p = pulse(t);
    const drive = t < D.drop ? 0.18 + 0.3 * b + 0.3 * p : 0.45 + 0.25 * clamp((b - 0.55) / 0.4, 0, 1) + 0.5 * p;
    const pts = [];
    for (let i = 0; i <= 180; i++) {
      const th = i / 180 * Math.PI * 2;
      const r = (232 + extra + 14 * p + drive * (16 + 135 * shape(th, t)) + m * 7 * Math.sin(9 * th + 4 * t) + h * 4 * Math.sin(23 * th - 7 * t)) * sc;
      pts.push([CX + Math.sin(th) * r, CY - Math.cos(th) * r]);
    }
    return pts;
  }
  function path(pts) { ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) ctx.lineTo(pts[i][0], pts[i][1]); ctx.closePath(); }
  function glitchWin(t) {
    const w = [[D.drop, 0.42, 1], [D.switch, 0.3, 0.8], [D.switch + 2 * D.bar, 0.3, 0.8], [D.end - 0.12, 0.12, 0.6]];
    let g = 0; for (const [a, d, s] of w) if (t >= a && t < a + d) g = Math.max(g, s * (1 - (t - a) / d)); return g;
  }

  function background(t, b) {
    const g = ctx.createLinearGradient(0, 0, 0, H);
    g.addColorStop(0, "#01050c"); g.addColorStop(0.45, "#05203b"); g.addColorStop(1, "#010409");
    ctx.fillStyle = g; ctx.fillRect(-200, -200, W + 400, H + 400);
    // god rays from above the disk
    ctx.save(); ctx.globalCompositeOperation = "lighter";
    for (let i = 0; i < 6; i++) {
      const a = Math.PI / 2 + (i - 2.5) * 0.17 + 0.08 * Math.sin(t * 0.21 + i), w = 0.035 + 0.02 * ((i * 37) % 5) / 5, L = 2300;
      const rg = ctx.createLinearGradient(CX, -150, CX + Math.cos(a) * L, -150 + Math.sin(a) * L);
      rg.addColorStop(0, `rgba(90,180,255,${0.05 + 0.05 * b})`); rg.addColorStop(1, "rgba(90,180,255,0)");
      ctx.fillStyle = rg; ctx.beginPath(); ctx.moveTo(CX, -150);
      ctx.lineTo(CX + Math.cos(a - w) * L, -150 + Math.sin(a - w) * L); ctx.lineTo(CX + Math.cos(a + w) * L, -150 + Math.sin(a + w) * L); ctx.fill();
    }
    ctx.restore();
    // fog
    for (const f of FOG) {
      const x = f.x + Math.sin(t * 0.13 + f.ph) * 140, y = f.y + Math.cos(t * 0.09 + f.ph) * 80;
      const rg = ctx.createRadialGradient(x, y, 0, x, y, f.r);
      rg.addColorStop(0, `rgba(35,120,200,${0.13 * (0.8 + 0.4 * b)})`); rg.addColorStop(1, "rgba(35,120,200,0)");
      ctx.fillStyle = rg; ctx.fillRect(x - f.r, y - f.r, f.r * 2, f.r * 2);
    }
    // candlestick towers: far row in the fog, near row as dark silhouettes with a cold rim light
    const offF = -t * 4, offN = -t * 9;
    ctx.fillStyle = "rgba(14,50,90,0.55)"; ctx.strokeStyle = "rgba(14,50,90,0.55)"; ctx.lineWidth = 6;
    for (const c of FAR) { const x = c.x + offF; ctx.fillRect(x, c.top, c.w, H - c.top + 50); ctx.beginPath(); ctx.moveTo(x + c.w / 2, c.top); ctx.lineTo(x + c.w / 2, c.top - c.wick); ctx.stroke(); }
    for (const c of NEAR) {
      const x = c.x + offN;
      ctx.fillStyle = "rgba(1,5,12,0.94)"; ctx.fillRect(x, c.top, c.w, H - c.top + 50);
      ctx.strokeStyle = "rgba(1,5,12,0.94)"; ctx.lineWidth = 10; ctx.beginPath(); ctx.moveTo(x + c.w / 2, c.top); ctx.lineTo(x + c.w / 2, c.top - c.wick); ctx.stroke();
      ctx.strokeStyle = `rgba(90,185,255,${0.22 + 0.2 * b})`; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(x, c.top + 1); ctx.lineTo(x + c.w, c.top + 1); ctx.stroke();
    }
  }
  function ash(t, front) {
    const d = dist(t), fast = t >= D.drop && t < D.end + 0.4 ? 1.7 : 1;
    ctx.lineCap = "round";
    for (let i = 0; i < P.length; i++) {
      const p = P[i]; if ((p.z > 0.72) !== front) continue;
      const dx = Math.cos(p.a), dy = Math.sin(p.a), s = d * p.v;
      const x = ((p.x + dx * s) % 1500 + 1500) % 1500 - 200, y = ((p.y + dy * s) % 2100 + 2100) % 2100 - 100;
      const L = (8 + 46 * p.z) * fast;
      ctx.strokeStyle = `rgba(150,220,255,${0.16 + 0.6 * p.z})`; ctx.lineWidth = 1 + 3.4 * p.z;
      ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x - dx * L, y - dy * L); ctx.stroke();
    }
  }
  function bokeh(t) {
    ctx.save(); ctx.globalCompositeOperation = "lighter";
    for (const k of BK) {
      if (!k.keep && t < D.drop) continue;
      const u = (t - k.t0) / k.life; if (u < 0 || u > 1) continue;
      const x = k.x + k.vx * u * k.life, y = k.y + k.vy * u * k.life, a = k.a * Math.sin(Math.PI * u);
      const rg = ctx.createRadialGradient(x, y, 0, x, y, k.r);
      rg.addColorStop(0, `rgba(80,200,255,${a})`); rg.addColorStop(0.55, `rgba(60,170,255,${a * 0.55})`); rg.addColorStop(1, "rgba(60,170,255,0)");
      ctx.fillStyle = rg; ctx.beginPath(); ctx.ellipse(x, y, k.r * 1.25, k.r * 0.8, 0.6, 0, Math.PI * 2); ctx.fill();
    }
    ctx.restore();
  }
  function disk(t, p, h, alpha, sc) {
    ctx.save(); ctx.globalAlpha = alpha;
    const r = 215 * sc;
    const g = ctx.createRadialGradient(CX, CY - 40, 20, CX, CY, r);
    g.addColorStop(0, "#0a1f36"); g.addColorStop(1, "#02070f");
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(CX, CY, r, 0, Math.PI * 2); ctx.fill();
    ctx.shadowColor = "rgba(232,194,106,0.8)"; ctx.shadowBlur = 14; ctx.strokeStyle = "#e8c26a"; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.arc(CX, CY, r, 0, Math.PI * 2); ctx.stroke(); ctx.shadowBlur = 0;
    // dial ticks that light with the hi-hats
    for (let i = 0; i < 72; i++) {
      const a = i / 72 * Math.PI * 2 + t * 0.15, lit = 0.12 + 0.6 * h * (0.5 + 0.5 * Math.sin(i * 1.7 + t * 6));
      ctx.strokeStyle = `rgba(110,210,255,${lit})`; ctx.lineWidth = i % 6 ? 2 : 3;
      const r1 = r - 18, r2 = r - (i % 6 ? 9 : 4);
      ctx.beginPath(); ctx.moveTo(CX + Math.sin(a) * r1, CY - Math.cos(a) * r1); ctx.lineTo(CX + Math.sin(a) * r2, CY - Math.cos(a) * r2); ctx.stroke();
    }
    ctx.restore();
  }
  function emblem(t, p, alpha, sc) {
    const s = sc * (1 + 0.05 * p), w = 280 * s, h = 272 * s, x = CX - w / 2, y = CY - h / 2 - 4;
    const g = glitchWin(t), f = fr(t);
    ctx.save(); ctx.globalAlpha = alpha;
    const inSwitch = t >= D.switch && t < D.switch + 2 * D.bar;
    if (inSwitch) {
      // the emblem turns into a live chart for two bars
      const hs = [80, 130, 105, 175], cols = ["#2962ff", "#e8c26a", "#2962ff", "#e8c26a"];
      for (let i = 0; i < 4; i++) {
        const k = 0.75 + 0.5 * pulse(t - i * 0.06), bh = hs[i] * k * sc, cx = CX - 105 * sc + i * 70 * sc, base = CY + 95 * sc;
        ctx.strokeStyle = cols[i]; ctx.lineWidth = 4 * sc; ctx.beginPath(); ctx.moveTo(cx, base - bh - 34 * sc); ctx.lineTo(cx, base + 18 * sc); ctx.stroke();
        ctx.fillStyle = cols[i]; ctx.shadowColor = cols[i]; ctx.shadowBlur = 18; ctx.fillRect(cx - 20 * sc, base - bh, 40 * sc, bh); ctx.shadowBlur = 0;
      }
    } else if (logo.naturalWidth) {
      if (g > 0) {
        const n = 10, sh = logo.naturalHeight / n;
        for (let j = 0; j < n; j++) {
          const dx = (hash(f * 31 + j) - 0.5) * 90 * g;
          ctx.drawImage(logo, 0, j * sh, logo.naturalWidth, sh, x + dx, y + j * sh * s, w, sh * s + 1);
        }
        ctx.globalCompositeOperation = "lighter"; ctx.globalAlpha = alpha * 0.45 * g;
        ctx.drawImage(logo, x - 14 * g, y, w, h); ctx.drawImage(logo, x + 14 * g, y, w, h);
      } else {
        ctx.drawImage(logo, x, y, w, h);
      }
    }
    ctx.restore();
  }
  function ring(t, alpha, sc) {
    if (alpha <= 0) return;
    ctx.save(); ctx.lineJoin = "round";
    const trail = blob(t - 0.07, sc, 0);
    path(trail); ctx.strokeStyle = `rgba(30,110,255,${0.55 * alpha})`; ctx.lineWidth = 5; ctx.stroke();
    const pts = blob(t, sc, 0);
    path(pts); ctx.shadowColor = "rgba(40,200,255,0.95)"; ctx.shadowBlur = 30; ctx.strokeStyle = `rgba(60,210,255,${alpha})`; ctx.lineWidth = 10; ctx.stroke();
    ctx.shadowBlur = 0; ctx.strokeStyle = `rgba(235,250,255,${alpha})`; ctx.lineWidth = 3; ctx.stroke();
    const outer = blob(t - 0.03, sc, 18);
    path(outer); ctx.strokeStyle = `rgba(80,200,255,${0.4 * alpha})`; ctx.lineWidth = 2; ctx.stroke();
    ctx.restore();
  }
  function renderAt(t) {
    t = clamp(t, 0, D.total);
    const b = ev(D.bass, t), h = ev(D.high, t), p = pulse(t), f = fr(t);
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, W, H);
    // camera: slow push through the build, a breath after the drop, hits on kicks, shake on the big moments
    let cs = t < D.drop ? 1.07 - 0.07 * ease(t / D.drop) : 1 + 0.02 * Math.sin((t - D.drop) * 0.6) + 0.018 * p;
    let amp = 0;
    for (const [a, d, s] of [[D.drop, 0.5, 26], [D.switch, 0.3, 12], [D.end, 0.45, 20]]) if (t >= a && t < a + d) amp = Math.max(amp, s * (1 - (t - a) / d));
    const sx = (hash(f * 3 + 1) - 0.5) * 2 * amp, sy = (hash(f * 3 + 2) - 0.5) * 2 * amp;
    ctx.translate(CX + sx, CY + sy); ctx.scale(cs, cs); ctx.translate(-CX, -CY);
    background(t, b);
    ash(t, false);
    // the disk and its ring leave with a burst at the end card
    const e = t >= D.end ? clamp((t - D.end) / 0.35, 0, 1) : 0, burst = 1 + 1.6 * e * e, al = 1 - e;
    ring(t, al, burst);
    disk(t, p, h, al, 1 + 0.25 * e);
    emblem(t, p, al, 1 + 0.25 * e);
    bokeh(t);
    ash(t, true);
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    // vignette and flashes
    const vg = ctx.createRadialGradient(CX, CY, 420, CX, CY, 1250);
    vg.addColorStop(0, "rgba(0,0,0,0)"); vg.addColorStop(1, "rgba(0,0,0,0.78)");
    ctx.fillStyle = vg; ctx.fillRect(0, 0, W, H);
    let fl = 0;
    for (const [a, s, d] of [[D.drop, 0.85, 0.09], [D.switch, 0.45, 0.07], [D.switch + 2 * D.bar, 0.45, 0.07], [D.end, 0.9, 0.1]]) if (t >= a) fl = Math.max(fl, s * Math.exp(-(t - a) / d));
    if (fl > 0.01) { ctx.fillStyle = `rgba(220,240,255,${fl})`; ctx.fillRect(0, 0, W, H); }
  }
  window.addEventListener("hf-seek", (e) => {
    const t = e.detail.time;
    if (e.detail.waitUntil) e.detail.waitUntil(ready.then(() => renderAt(t))); else renderAt(t);
  });
  renderAt(0); ready.then(() => renderAt(0));
})();
""".replace("__DATA__", DATA)

CSS = """
@font-face { font-family: "Orbitron"; src: url("assets/fonts/Orbitron-Bold.ttf") format("truetype"); font-weight: 700; font-style: normal; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #01050c; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #01050c; font-family: Montserrat, sans-serif; color: #fff; }
#cv { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
#timer { position: absolute; left: 0; top: 1400px; width: 1080px; height: 90px; }
.tm { position: absolute; left: 0; top: 0; width: 1080px; text-align: center; font-family: Orbitron, Montserrat, sans-serif; font-weight: 700;
  font-size: 66px; letter-spacing: 0.06em; color: #7fdcff; opacity: 0; text-shadow: 0 0 18px rgba(40,200,255,0.9), 0 0 4px rgba(200,240,255,0.8); }
#tag { position: absolute; left: 0; top: 1510px; width: 1080px; text-align: center; font-size: 30px; font-weight: 700; letter-spacing: 0.42em;
  color: #e8c26a; opacity: 0; text-shadow: 0 0 12px rgba(232,194,106,0.5); }
#end { position: absolute; inset: 0; background: rgba(0,3,8,0.8); opacity: 0; z-index: 50; }
#end-logo { position: absolute; left: 110px; top: 470px; width: 860px; }
#end-tag { position: absolute; left: 0; width: 1080px; top: 920px; text-align: center; font-size: 44px; font-weight: 800; letter-spacing: 0.04em; }
#end-tag span { color: #e8c26a; }
#end-cta { position: absolute; left: 0; width: 1080px; top: 1040px; text-align: center; font-family: "Archivo Black"; font-size: 92px; }
#end-cta span { color: #2962ff; }
#end-note { position: absolute; left: 0; width: 1080px; top: 1180px; text-align: center; font-size: 28px; font-weight: 700; letter-spacing: 0.12em; color: #9aa3ad; }
#end-credit { position: absolute; left: 0; width: 1080px; top: 1230px; text-align: center; font-size: 28px; font-weight: 500; color: #9aa3ad; }
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
    <div id="root" data-composition-id="otm-viz" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <canvas id="cv" width="1080" height="1920" data-layout-allow-occlusion></canvas>
      <div id="timer">{timer}</div>
      <div id="tag">ORDER THE MARKET</div>
      <div id="end"><img id="end-logo" src="assets/otm_logo.png" alt="Order the Market" />
        <div id="end-tag">DON'T LET THE MARKET <span>ORDER YOU</span></div>
        <div id="end-cta">FOLLOW FOR <span>MORE</span></div>
        <div id="end-note">EDUCATIONAL ONLY · NOT FINANCIAL ADVICE</div>
        <div id="end-credit">{CREDIT}</div>
        <div id="end-foot"><img id="end-foot-img" src="assets/footer.jpg" alt="" /></div></div>
      <audio id="otm-viz-audio" class="clip" src="assets/audio/mix_viz.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>{JS}</script>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join("        " + t for t in T)}
        window.__timelines["otm-viz"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(html)
print("total", TOTAL, "drop", DROP, "switch", SWITCH, "end", END, "tl lines", len(T), "html KB", len(html) // 1024)
