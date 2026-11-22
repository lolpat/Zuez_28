// Per-signal chart: gold candles with the trade drawn as a position (entry, stop loss, take-profits reached, exit),
// like TradingView's long / short position tool. Uses TradingView Lightweight Charts, loaded only when needed.
(function (root) {
  const LIB = "https://cdn.jsdelivr.net/npm/lightweight-charts@4.1.3/dist/lightweight-charts.standalone.production.js";
  let lib = null;
  const loadLib = () => lib || (lib = new Promise((ok, no) => {
    if (root.LightweightCharts) return ok(root.LightweightCharts);
    const s = document.createElement("script"); s.src = LIB; s.async = true;
    s.onload = () => ok(root.LightweightCharts); s.onerror = () => { lib = null; no(new Error("chart-lib")); };
    document.head.appendChild(s);
  }));

  const PPU = { XAUUSD: 10 };                                       // pips per price unit (gold: $1 = 10 pips)
  // where the trade closed, from its result in pips
  function exitPrice(p) {
    const ppu = PPU[p.symbol] || 10, e = +p.entry;
    if (!Number.isFinite(e) || p.pips == null) return null;
    return +(p.side === "sell" ? e - p.pips / ppu : e + p.pips / ppu).toFixed(2);
  }

  // draws into `box` (an empty element); returns a function that removes the chart
  async function draw(box, p, candles, opts = {}) {
    const LW = await loadLib();
    box.innerHTML = `<div class="pc__chart"></div><canvas class="pc__boxes" aria-hidden="true"></canvas>`;
    const el = box.querySelector(".pc__chart"), cv = box.querySelector(".pc__boxes"), ctx = cv.getContext("2d");
    const css = getComputedStyle(document.documentElement), col = (n, f) => (css.getPropertyValue(n) || "").trim() || f;
    const gold = col("--accent", "#dcb84a"), hi = col("--accent-hi", "#f0d68c"), pink = col("--accent-2", "#e52150"), loss = col("--loss", "#ff6b5e"), profit = col("--profit", "#5ad17f");
    const tz = -new Date().getTimezoneOffset() * 60;               // the viewer's own clock
    const chart = LW.createChart(el, {
      autoSize: true,
      layout: { background: { type: "solid", color: "transparent" }, textColor: col("--muted", "#a39a96"), fontFamily: "IBM Plex Sans Thai, system-ui, sans-serif" },
      grid: { vertLines: { color: "rgba(255,255,255,.04)" }, horzLines: { color: "rgba(255,255,255,.04)" } },
      rightPriceScale: { borderColor: "rgba(255,255,255,.08)", scaleMargins: { top: .1, bottom: .1 } },
      timeScale: { borderColor: "rgba(255,255,255,.08)", timeVisible: true, secondsVisible: false, rightOffset: 4 },
      crosshair: { mode: 0 },
      watermark: { visible: true, text: "ORDER THE MARKET", fontSize: 28, color: "rgba(220,184,74,.06)" },
    });
    const series = chart.addCandlestickSeries({ upColor: gold, borderUpColor: gold, wickUpColor: gold, downColor: pink, borderDownColor: pink, wickDownColor: pink });
    series.setData(candles.map((x) => ({ time: x.t + tz, open: x.o, high: x.h, low: x.l, close: x.c })));

    const entry = +p.entry, sl = p.sl == null ? null : +p.sl, ex = exitPrice(p), zoneHi = p.entry2 == null ? null : +p.entry2;
    const sideSign = p.side === "sell" ? -1 : 1;
    const reached = (p.tps || []).map(Number).filter((v) => ex != null && (v - entry) * sideSign > 0 && (ex - v) * sideSign >= 0);
    // keep entry, SL and exit in view
    const keep = [entry, sl, ex, zoneHi].filter((v) => v != null && Number.isFinite(v));
    series.applyOptions({ autoscaleInfoProvider: (orig) => { const r = orig(); if (!r || !keep.length) return r; return { priceRange: { minValue: Math.min(r.priceRange.minValue, ...keep), maxValue: Math.max(r.priceRange.maxValue, ...keep) } }; } });
    const line = (price, title, color, style = 0) => price != null && series.createPriceLine({ price, title, color, lineStyle: style, lineWidth: 1, axisLabelVisible: true });
    line(sl, "SL", loss); line(entry, "ENTRY", "#cfc7c2", 2);
    if (ex != null && ex !== entry) line(ex, opts.exitLabel || "EXIT", p.pips >= 0 ? profit : loss);
    chart.timeScale().fitContent();

    const t1 = Math.floor(Date.parse(p.opened_at) / 1000) + tz, t2 = Math.floor(Date.parse(p.closed_at) / 1000) + tz;
    // a time between candles has no x of its own: use the nearest candle
    const xAt = (t) => {
      const ts = chart.timeScale(), direct = ts.timeToCoordinate(t);
      if (direct != null) return direct;
      const d = series.data(); if (!d.length) return null;
      let best = d[0]; for (const c of d) if (Math.abs(c.time - t) < Math.abs(best.time - t)) best = c;
      return ts.timeToCoordinate(best.time);
    };
    const paint = () => {
      const r = el.getBoundingClientRect(), dpr = root.devicePixelRatio || 1;
      cv.width = Math.round(r.width * dpr); cv.height = Math.round(r.height * dpr); cv.style.width = r.width + "px"; cv.style.height = r.height + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, r.width, r.height);
      const x1 = xAt(t1), x2 = xAt(Math.max(t2, t1 + 60)), y = (v) => series.priceToCoordinate(v);
      if (x1 == null || x2 == null || y(entry) == null) return;
      const w = Math.max(x2 - x1, 6);
      const rect = (a, b, fill, stroke) => { const ya = y(a), yb = y(b); if (ya == null || yb == null) return; const top = Math.min(ya, yb), h = Math.abs(yb - ya);
        ctx.fillStyle = fill; ctx.fillRect(x1, top, w, h); ctx.strokeStyle = stroke; ctx.lineWidth = 1; ctx.strokeRect(x1 + .5, top + .5, w, h); };
      if (sl != null) rect(entry, sl, "rgba(255,107,94,.15)", "rgba(255,107,94,.55)");
      if (ex != null && ex !== entry) rect(entry, ex, p.pips >= 0 ? "rgba(90, 209, 127,.12)" : "rgba(255,107,94,.28)", p.pips >= 0 ? "rgba(90, 209, 127,.5)" : "rgba(255,107,94,.8)");
      if (zoneHi != null && y(zoneHi) != null) { ctx.fillStyle = "rgba(243,238,233,.08)"; const a = y(zoneHi), b = y(entry); ctx.fillRect(x1, Math.min(a, b), w, Math.abs(b - a)); }
      ctx.setLineDash([4, 4]); ctx.strokeStyle = "rgba(240,214,140,.6)"; ctx.font = "600 11px Kanit, sans-serif";
      (p.tps || []).map(Number).forEach((v, i) => { if (!reached.includes(v)) return; const yy = y(v); if (yy == null) return;
        ctx.beginPath(); ctx.moveTo(x1, yy + .5); ctx.lineTo(x1 + w, yy + .5); ctx.stroke(); ctx.fillStyle = hi; ctx.fillText("TP" + (i + 1), x1 + 6, yy - 3); });
      ctx.setLineDash([]);
      // entry marker
      const ey = y(entry); ctx.fillStyle = p.side === "sell" ? pink : profit; ctx.beginPath();
      if (p.side === "sell") { ctx.moveTo(x1 - 7, ey - 15); ctx.lineTo(x1 + 7, ey - 15); ctx.lineTo(x1, ey - 4); } else { ctx.moveTo(x1 - 7, ey + 15); ctx.lineTo(x1 + 7, ey + 15); ctx.lineTo(x1, ey + 4); }
      ctx.closePath(); ctx.fill();
      // labels
      const tag = (txt, yy, bg, fg) => { if (yy == null || !txt) return; ctx.font = "600 12px Kanit, sans-serif"; const tw = ctx.measureText(txt).width + 14;
        const x = Math.min(x1 + 6, r.width - tw - 70); ctx.fillStyle = bg; ctx.beginPath(); (ctx.roundRect ? ctx.roundRect(x, yy - 11, tw, 22, 6) : ctx.rect(x, yy - 11, tw, 22)); ctx.fill(); ctx.fillStyle = fg; ctx.fillText(txt, x + 7, yy + 4); };
      const away = (v) => { const a = y(v), b = y(entry); return a == null ? null : a + (a >= b ? 16 : -16); };   // just outside the box
      if (sl != null) tag(opts.slTag, away(sl), "rgba(255,107,94,.92)", "#1a0b0a");
      if (ex != null && ex !== entry) tag(opts.exitTag, away(ex), p.pips >= 0 ? "rgba(90, 209, 127,.92)" : "rgba(255,107,94,.92)", p.pips >= 0 ? "#0b1405" : "#1a0b0a");
    };
    const redraw = () => requestAnimationFrame(paint);
    chart.timeScale().subscribeVisibleLogicalRangeChange(redraw);
    const ro = new ResizeObserver(redraw); ro.observe(el);
    setTimeout(redraw, 60);
    return () => { ro.disconnect(); chart.remove(); };
  }

  root.OTMPosChart = { draw, exitPrice, loadLib };
})(window);
