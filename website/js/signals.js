// Signal results: one tab per signal room, every figure computed from the room's trade log
// in js/signals-data.js. No numbers are typed in by hand.
(function (root) {
  const cfg = root.OTM_CONFIG || {};
  const live = !!(cfg.SUPABASE_URL && cfg.SUPABASE_ANON_KEY);
  const t = (k, v) => root.OTMI18n.t(k, v);
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const num = (v, d = 0) => Number(v).toLocaleString("en-US", { minimumFractionDigits: d, maximumFractionDigits: d });
  const sgn = (v, d = 0) => (v > 0 ? "+" : v < 0 ? "−" : "") + num(Math.abs(v), d);
  const usd = (v) => (v >= 0 ? "+$" : "−$") + num(Math.abs(v));

  // ---------------------------------------------------------------- sample data (demo preview only)
  function sample(room, k) {
    let s = 7919 + k * 101;
    const rnd = () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
    const shape = [
      { n: 70, win: 0.7, tp: [180, 520], sl: [90, 220] },
      { n: 160, win: 0.74, tp: [25, 90], sl: [30, 70] },
      { n: 60, win: 0.45, tp: [300, 900], sl: [80, 160] },
      { n: 80, win: 0.62, tp: [120, 600], sl: [80, 300] }
    ][k];
    const syms = Object.keys(room.pipValue || { XAUUSD: 10 });
    const out = [], now = new Date();
    for (let i = 0; i < shape.n; i++) {
      const d = new Date(now.getTime() - (1 + rnd() * 58) * 864e5);
      const w = rnd() < shape.win, r = w ? shape.tp : shape.sl;
      const pips = Math.round(r[0] + rnd() * (r[1] - r[0])) * (w ? 1 : -1);
      out.push([d.toISOString().slice(0, 10), syms[Math.floor(rnd() * syms.length)], rnd() < 0.55 ? "buy" : "sell", pips]);
    }
    return out;
  }

  // ---------------------------------------------------------------- the numbers
  function compute(room, deduct) {
    const tr = room.trades.slice().sort((a, b) => a[0].localeCompare(b[0]));
    const wins = tr.filter((x) => x[3] > 0), losses = tr.filter((x) => x[3] < 0);
    const gw = wins.reduce((s, x) => s + x[3], 0), gl = -losses.reduce((s, x) => s + x[3], 0);
    const total = gw - gl;
    // streaks and average run lengths
    let best = 0, worst = 0, run = 0, sign = 0; const winRuns = [], lossRuns = [];
    const close = () => { if (sign > 0) winRuns.push(run); else if (sign < 0) lossRuns.push(run); };
    for (const x of tr) {
      const sg = x[3] > 0 ? 1 : x[3] < 0 ? -1 : 0;
      if (!sg) continue;
      if (sg === sign) run++; else { close(); sign = sg; run = 1; }
      if (sg > 0) best = Math.max(best, run); else worst = Math.max(worst, run);
    }
    close();
    const avg = (a) => (a.length ? a.reduce((s, v) => s + v, 0) / a.length : 0);
    // best day
    const byDay = new Map(); tr.forEach((x) => byDay.set(x[0], (byDay.get(x[0]) || 0) + x[3]));
    let bestDay = null; for (const [d, v] of byDay) if (!bestDay || v > bestDay[1]) bestDay = [d, v];
    // months
    const byMonth = new Map();
    for (const x of tr) {
      const m = x[0].slice(0, 7), g = byMonth.get(m) || { m, n: 0, w: 0, l: 0, pips: 0 };
      g.n++; g.pips += x[3]; if (x[3] > 0) g.w++; else if (x[3] < 0) g.l++;
      byMonth.set(m, g);
    }
    // money if you had followed every signal at a fixed lot, after the spread/commission deduction
    const pv = room.pipValue || {};
    const dollars1 = tr.reduce((s, x) => s + x[3] * (pv[x[1]] ?? 10), 0) * (1 - deduct);
    return {
      n: tr.length, w: wins.length, l: losses.length, wr: tr.length ? (wins.length / tr.length) * 100 : 0,
      pf: gl ? gw / gl : (gw ? Infinity : 0), total, best, worst, avgW: avg(winRuns), avgL: avg(lossRuns),
      bestDay, months: [...byMonth.values()].sort((a, b) => b.m.localeCompare(a.m)),
      lots: [0.01, 0.1, 0.5, 1].map((lot) => [lot, dollars1 * lot]),
      from: tr.length ? tr[0][0] : null, to: tr.length ? tr[tr.length - 1][0] : null
    };
  }

  // ---------------------------------------------------------------- room badges (drawn, no images)
  function badge(room) {
    if (room.hype) return `<span class="sig-hype">HYPE</span>`;
    const pal = { 1: ["#6e4f12", "#c89f3a", "#f6e4a6"], 2: ["#5c6069", "#b4b8c1", "#eef0f4"], 3: ["#5a2e14", "#b06a3b", "#f0b38a"] }[room.medal] || ["#555", "#999", "#ddd"];
    const id = "sgm" + room.id;
    return `<svg class="sig-medal" viewBox="0 0 40 46" width="34" height="40" aria-hidden="true">
      <defs><radialGradient id="${id}" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="${pal[2]}"/><stop offset=".6" stop-color="${pal[1]}"/><stop offset="1" stop-color="${pal[0]}"/></radialGradient></defs>
      <path d="M12 0h7l-3 14h-7zM28 0h-7l3 14h7z" fill="#e52150" opacity=".85"/>
      <circle cx="20" cy="28" r="15" fill="url(#${id})" stroke="${pal[0]}"/>
      <circle cx="20" cy="28" r="10.5" fill="none" stroke="${pal[2]}" stroke-opacity=".6"/>
      <text x="20" y="33" text-anchor="middle" fill="#2a1a08" style="font:700 14px var(--font-head)">${room.medal}</text>
    </svg>${room.flash ? `<span class="sig-flash" aria-hidden="true">⚡</span>` : ""}`;
  }

  // ---------------------------------------------------------------- page
  function render(el, opts = {}) {
    if (!el) return;
    const D = root.OTM_SIGNALS || { rooms: [] };
    const anyReal = D.rooms.some((r) => r.trades && r.trades.length);
    const isSample = !anyReal && !live;
    if (!anyReal && live) { el.innerHTML = `<p class="sig-soon">${t("sig.soon")}</p>`; return; }
    const rooms = D.rooms.map((r, k) => ({ ...r, trades: anyReal ? r.trades || [] : sample(r, k) }));
    let cur = 0;
    const months = (m) => new Date(m + "-15T12:00:00").toLocaleDateString(root.OTMI18n.lang === "th" ? "th-TH" : "en-GB", { month: "long", year: "numeric" });
    const draw = () => {
      const r = rooms[cur], s = compute(r, D.deduct ?? 0.15);
      const bars = s.months.slice().reverse();
      el.innerHTML = `
        ${isSample ? `<div class="sig-sample"><b>${t("sig.sample.t")}</b> ${t("sig.sample.d")}</div>` : ""}
        <div class="sig-tabs" role="tablist" aria-label="${esc(t("sig.rooms"))}">${rooms.map((x, i) => `
          <button type="button" role="tab" class="sig-tab ${i === cur ? "is-on" : ""}" aria-selected="${i === cur}" data-room="${i}">
            <span class="sig-tab__b">${badge(x)}</span><span>${esc(x.name)}</span></button>`).join("")}</div>
        <div class="sig-head card">
          <span class="sig-head__b">${badge(r)}</span>
          <div><h3>${esc(r.name)}</h3><small>${t("sig.source", { s: esc(r.source || "") })}${s.from ? ` · ${t("sig.range", { a: s.from, b: s.to })}` : ""}${D.updated && !isSample ? ` · ${t("sig.updated", { d: D.updated })}` : ""}</small></div>
          ${isSample ? `<span class="sig-pill">${t("sig.sample.pill")}</span>` : ""}
        </div>
        ${s.n ? `
        <div class="sig-kpis">
          <div><b>${s.n}</b><span>${t("sig.k.trades")}</span></div>
          <div><b class="gold">${num(s.wr, 0)}%</b><span>${t("sig.k.wr")}</span></div>
          <div><b class="gold">${s.w}</b><span>${t("sig.k.tp")}</span></div>
          <div><b>${s.l}</b><span>${t("sig.k.sl")}</span></div>
          <div><b class="gold">${s.pf === Infinity ? "∞" : num(s.pf, 2)}</b><span>${t("sig.k.pf")}</span></div>
        </div>
        <div class="sig-row3">
          <section class="card sig-card"><h4>🔥 ${t("sig.pips")}</h4><b class="sig-big ${s.total >= 0 ? "up" : "down"}">${sgn(s.total)}</b>
            ${s.bestDay ? `<small>↗ ${t("sig.bestDay", { p: sgn(s.bestDay[1]), d: s.bestDay[0] })}</small>` : ""}</section>
          <section class="card sig-card"><h4>⚡ ${t("sig.streaks")}</h4>
            <div class="sig-2x2"><div><small>${t("sig.winStreak")}</small><b class="gold">${s.best}</b></div><div><small>${t("sig.lossStreak")}</small><b>${s.worst}</b></div>
            <div><small>${t("sig.avgWin")}</small><b>${num(s.avgW, 1)}</b></div><div><small>${t("sig.avgLoss")}</small><b>${num(s.avgL, 1)}</b></div></div></section>
          <section class="card sig-card"><h4>◎ ${t("sig.benefit")}</h4><small>${t("sig.benefit.d", { p: num((D.deduct ?? 0.15) * 100) })}</small>
            <ul class="sig-lots">${s.lots.map(([lot, v]) => `<li><span>${lot} lot</span><b class="${v >= 0 ? "up" : "down"}">${usd(v)}</b></li>`).join("")}</ul></section>
        </div>
        <div class="sig-row2">
          <section class="card sig-card"><h4>📊 ${t("sig.monthly")}</h4>
            <div class="table-wrap"><table class="table sig-mtab"><thead><tr><th>${t("sig.col.month")}</th><th class="r">${t("sig.col.trades")}</th><th class="r">Win%</th><th class="r">TP</th><th class="r">SL</th><th class="r">Pips</th></tr></thead>
            <tbody>${s.months.map((g) => `<tr><td>${months(g.m)}</td><td class="r">${g.n}</td><td class="r gold">${num((g.w / g.n) * 100, 0)}%</td><td class="r">${g.w}</td><td class="r">${g.l}</td><td class="r ${g.pips >= 0 ? "up" : "down"}">${sgn(g.pips)}</td></tr>`).join("")}</tbody></table></div></section>
          <section class="card sig-card"><h4>📈 ${t("sig.byMonth")}</h4>
            ${root.OTMCharts ? root.OTMCharts.bars(bars.map((g) => ({ label: months(g.m).replace(/\s*\d{4}$/, ""), value: g.pips, sub: String(g.m.slice(0, 4)) })), { fmt: (x) => sgn(x) + " pips", short: (x) => (Math.abs(x) >= 1000 ? sgn(x / 1000, 1) + "k" : sgn(x)), label: t("sig.byMonth"), w: 420, h: 230 }) : ""}</section>
        </div>` : `<p class="sig-soon">${t("sig.soon")}</p>`}
        <p class="sig-note">${t("sig.note")}</p>`;
      el.querySelectorAll("[data-room]").forEach((b) => b.addEventListener("click", () => { cur = +b.dataset.room; draw(); }));
    };
    draw();
    document.addEventListener("otm:lang", draw);
  }

  root.OTMSignals = { render, compute };
})(window);
