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

  // rooms recorded per day from the weekly summaries: [date, pips won, pips lost, stop losses, signals]
  function computeDays(room, deduct) {
    const ds = room.days.slice().sort((a, b) => a[0].localeCompare(b[0]));
    const won = ds.reduce((s, d) => s + d[1], 0), lost = ds.reduce((s, d) => s + d[2], 0), net = won - lost;
    const sls = ds.reduce((s, d) => s + d[3], 0);
    const green = ds.filter((d) => d[1] - d[2] > 0).length;
    const withSig = ds.filter((d) => d[4] != null), signals = withSig.reduce((s, d) => s + d[4], 0);
    // weeks, keyed by their Monday
    const monday = (iso) => { const d = new Date(iso + "T12:00:00Z"); d.setUTCDate(d.getUTCDate() - ((d.getUTCDay() + 6) % 7)); return d.toISOString().slice(0, 10); };
    const weeks = new Map();
    for (const d of ds) { const k = monday(d[0]), g = weeks.get(k) || { k, net: 0, sl: 0 }; g.net += d[1] - d[2]; g.sl += d[3]; weeks.set(k, g); }
    const wl = [...weeks.values()].sort((a, b) => a.k.localeCompare(b.k));
    let run = 0, noSl = 0; for (const w of wl) { run = w.sl ? 0 : run + 1; noSl = Math.max(noSl, run); }
    let dRun = 0, dBest = 0; for (const d of ds) { dRun = d[1] - d[2] > 0 ? dRun + 1 : 0; dBest = Math.max(dBest, dRun); }
    const bestWeek = wl.reduce((a, b) => (!a || b.net > a.net ? b : a), null);
    const bestDay = ds.reduce((a, d) => (!a || d[1] - d[2] > a[1] ? [d[0], d[1] - d[2]] : a), null);
    const byMonth = new Map();
    for (const d of ds) {
      const m = d[0].slice(0, 7), g = byMonth.get(m) || { m, days: 0, won: 0, lost: 0, sl: 0, weeks: new Set() };
      g.days++; g.won += d[1]; g.lost += d[2]; g.sl += d[3]; g.weeks.add(monday(d[0])); byMonth.set(m, g);
    }
    const pv = (room.pipValue && Object.values(room.pipValue)[0]) || 10;
    return {
      days: ds.length, weeks: wl.length, won, lost, net, sls, green, pf: lost ? won / lost : Infinity,
      signals, sigDays: withSig.length, noSl, dBest, bestWeek, bestDay, avgWeek: wl.length ? net / wl.length : 0,
      months: [...byMonth.values()].map((g) => ({ ...g, pips: g.won - g.lost, weeks: g.weeks.size })).sort((a, b) => b.m.localeCompare(a.m)),
      lots: [0.01, 0.1, 0.5, 1].map((lot) => [lot, net * pv * lot * (1 - deduct)]),
      from: ds.length ? ds[0][0] : null, to: ds.length ? ds[ds.length - 1][0] : null
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
    const hasData = (r) => (r.trades && r.trades.length) || (r.days && r.days.length);
    const rooms = D.rooms.map((r, k) => hasData(r) ? { ...r, real: true } : { ...r, real: false, trades: live ? [] : sample(r, k) });
    let cur = 0;
    const months = (m) => new Date(m + "-15T12:00:00").toLocaleDateString(root.OTMI18n.lang === "th" ? "th-TH" : "en-GB", { month: "long", year: "numeric" });
    const draw = () => {
      const r = rooms[cur], isSample = !r.real && !live;
      if (r.days && r.days.length) return drawDays(r);
      const s = compute(r, D.deduct ?? 0.15);
      const bars = s.months.slice().reverse();
      el.innerHTML = `
        ${tabs()}
        ${isSample ? `<div class="sig-sample"><b>${t("sig.sample.t")}</b> ${t("sig.sample.d")}</div>` : ""}
        <div class="sig-head card">
          <span class="sig-head__b">${badge(r)}</span>
          <div><h3>${esc(r.name)}</h3><small>${t("sig.source", { s: esc(r.source || "") })}${s.from ? ` · ${t("sig.range", { a: s.from, b: s.to })}` : ""}</small></div>
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
      wire();
    };
    const wire = () => el.querySelectorAll("[data-room]").forEach((b) => b.addEventListener("click", () => { cur = +b.dataset.room; draw(); }));
    const tabs = () => `<div class="sig-tabs" role="tablist" aria-label="${esc(t("sig.rooms"))}">${rooms.map((x, i) => `
          <button type="button" role="tab" class="sig-tab ${i === cur ? "is-on" : ""}" aria-selected="${i === cur}" data-room="${i}">
            <span class="sig-tab__b">${badge(x)}</span><span>${esc(x.name)}</span></button>`).join("")}</div>`;
    // a room recorded from its weekly summaries
    const drawDays = (r) => {
      const s = computeDays(r, D.deduct ?? 0.15), bars = s.months.slice().reverse(), pf = s.pf === Infinity ? "∞" : num(s.pf, 1);
      el.innerHTML = `
        ${tabs()}
        <div class="sig-head card">
          <span class="sig-head__b">${badge(r)}</span>
          <div><h3>${esc(r.name)}</h3><small>${t("sig.source", { s: esc(r.source || "") })} · ${t("sig.range", { a: s.from, b: s.to })} · ${t("sig.fromWeekly", { n: s.weeks })}</small></div>
        </div>
        <div class="sig-kpis">
          <div><b class="gold">${sgn(s.net)}</b><span>${t("sig.d.net")}</span></div>
          <div><b>${s.days}</b><span>${t("sig.d.days")}</span></div>
          <div><b class="gold">${num((s.green / s.days) * 100, 0)}%</b><span>${t("sig.d.green")}</span></div>
          <div><b>${s.sls}</b><span>${t("sig.d.sl")}</span></div>
          <div><b class="gold">${pf}</b><span>${t("sig.k.pf")}</span></div>
        </div>
        <div class="sig-row3">
          <section class="card sig-card"><h4>🔥 ${t("sig.pips")}</h4><b class="sig-big up">${sgn(s.net)}</b>
            <ul class="sig-lots"><li><span>${t("sig.d.won")}</span><b class="up">${sgn(s.won)}</b></li><li><span>${t("sig.d.lost")}</span><b class="down">${sgn(-s.lost)}</b></li>
            <li><span>${t("sig.d.avgWeek")}</span><b>${sgn(s.avgWeek)}</b></li></ul>
            ${s.bestDay ? `<small>↗ ${t("sig.bestDay", { p: sgn(s.bestDay[1]), d: s.bestDay[0] })}</small>` : ""}</section>
          <section class="card sig-card"><h4>⚡ ${t("sig.streaks")}</h4>
            <div class="sig-2x2"><div><small>${t("sig.d.dayStreak")}</small><b class="gold">${s.dBest}</b></div><div><small>${t("sig.d.noSl")}</small><b class="gold">${s.noSl}</b></div>
            <div><small>${t("sig.d.weeks")}</small><b>${s.weeks}</b></div><div><small>${t("sig.d.bestWeek")}</small><b>${s.bestWeek ? sgn(s.bestWeek.net) : "–"}</b></div></div></section>
          <section class="card sig-card"><h4>◎ ${t("sig.benefit")}</h4><small>${t("sig.benefit.d", { p: num((D.deduct ?? 0.15) * 100) })}</small>
            <ul class="sig-lots">${s.lots.map(([lot, v]) => `<li><span>${lot} lot</span><b class="${v >= 0 ? "up" : "down"}">${usd(v)}</b></li>`).join("")}</ul></section>
        </div>
        <div class="sig-row2">
          <section class="card sig-card"><h4>📊 ${t("sig.monthly")}</h4>
            <div class="table-wrap"><table class="table sig-mtab"><thead><tr><th>${t("sig.col.month")}</th><th class="r">${t("sig.d.colDays")}</th><th class="r">SL</th><th class="r">${t("sig.d.colWon")}</th><th class="r">${t("sig.d.colLost")}</th><th class="r">${t("sig.d.colNet")}</th></tr></thead>
            <tbody>${s.months.map((g) => `<tr><td>${months(g.m)}</td><td class="r">${g.days}</td><td class="r">${g.sl}</td><td class="r up">${sgn(g.won)}</td><td class="r down">${g.lost ? sgn(-g.lost) : "0"}</td><td class="r gold"><b>${sgn(g.pips)}</b></td></tr>`).join("")}</tbody></table></div></section>
          <section class="card sig-card"><h4>📈 ${t("sig.byMonth")}</h4>
            ${root.OTMCharts ? root.OTMCharts.bars(bars.map((g) => ({ label: months(g.m).replace(/\s*\d{4}$/, "").slice(0, 3), value: g.pips, sub: "" })), { fmt: (x) => sgn(x) + " pips", short: (x) => (Math.abs(x) >= 1000 ? sgn(x / 1000, 0) + "k" : sgn(x)), label: t("sig.byMonth"), w: 460, h: 230 }) : ""}</section>
        </div>
        <p class="sig-note">${t("sig.d.note")}</p>`;
      wire();
    };
    draw();
    document.addEventListener("otm:lang", draw);
  }

  root.OTMSignals = { render, compute };
})(window);
