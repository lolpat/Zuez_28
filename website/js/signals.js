// Signal results: a rail of rooms on the left, the chosen room on the right (orbit ring of
// monthly pips, a ledger, the cumulative line, a gold tile per week and a lot calculator).
// Every figure is computed from js/signals-data.js. No numbers are typed in by hand.
(function (root) {
  const cfg = root.OTM_CONFIG || {};
  const live = !!(cfg.SUPABASE_URL && cfg.SUPABASE_ANON_KEY);
  const t = (k, v) => root.OTMI18n.t(k, v);
  const th = () => root.OTMI18n.lang === "th";
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const num = (v, d = 0) => Number(v).toLocaleString("en-US", { minimumFractionDigits: d, maximumFractionDigits: d });
  const sgn = (v, d = 0) => (v > 0 ? "+" : v < 0 ? "−" : "") + num(Math.abs(v), d);
  const usd = (v) => (v >= 0 ? "+$" : "−$") + num(Math.abs(v));
  const kfmt = (v) => (Math.abs(v) >= 1000 ? sgn(v / 1000, 1) + "k" : sgn(v));
  const loc = () => (th() ? "th-TH-u-ca-gregory" : "en-GB");
  const dShort = (iso, year) => new Date(iso + "T12:00:00").toLocaleDateString(loc(), { day: "numeric", month: "short", ...(year ? { year: "numeric" } : {}) });
  const mShort = (m) => new Date(m + "-15T12:00:00").toLocaleDateString(loc(), { month: "short" });
  const monday = (iso) => { const d = new Date(iso + "T12:00:00Z"); d.setUTCDate(d.getUTCDate() - ((d.getUTCDay() + 6) % 7)); return d.toISOString().slice(0, 10); };

  // ---------------------------------------------------------------- sample trades (demo preview only)
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

  // ---------------------------------------------------------------- one model for both kinds of room
  // A room either has a trade log ([date, symbol, side, pips]) or days from weekly summaries
  // ([date, pips won, pips lost, stop losses, signals|null]). Both become days here.
  function toDays(room) {
    const pv = room.pipValue || {}, first = Object.values(pv)[0] ?? 10;
    if (room.days && room.days.length) {
      return { perTrade: false, days: room.days.map(([d, won, lost, sl, n]) => ({ d, won, lost, sl, n, w: null, usd: (won - lost) * first })) };
    }
    const by = new Map();
    for (const [d, sym, , p] of room.trades || []) {
      const g = by.get(d) || { d, won: 0, lost: 0, sl: 0, n: 0, w: 0, usd: 0 };
      g.n++; g.usd += p * (pv[sym] ?? first);
      if (p > 0) { g.won += p; g.w++; } else if (p < 0) { g.lost -= p; g.sl++; }
      by.set(d, g);
    }
    return { perTrade: true, days: [...by.values()] };
  }

  function stats(room, deduct = 0.15) {
    const { perTrade, days } = toDays(room);
    const ds = days.sort((a, b) => a.d.localeCompare(b.d));
    const sum = (f, a = ds) => a.reduce((s, x) => s + f(x), 0);
    const won = sum((x) => x.won), lost = sum((x) => x.lost), net = won - lost;
    const weeks = new Map();
    for (const x of ds) { const k = monday(x.d), g = weeks.get(k) || { k, net: 0, sl: 0 }; g.net += x.won - x.lost; g.sl += x.sl; weeks.set(k, g); }
    const wl = [...weeks.values()].sort((a, b) => a.k.localeCompare(b.k));
    let run = 0, noSl = 0; for (const w of wl) { run = w.sl ? 0 : run + 1; noSl = Math.max(noSl, run); }
    const months = new Map(); for (const x of ds) { const m = x.d.slice(0, 7); months.set(m, (months.get(m) || 0) + x.won - x.lost); }
    const signals = perTrade ? sum((x) => x.n) : null, wins = perTrade ? sum((x) => x.w) : null;
    let c = 0;
    return {
      days: ds.length, weeks: wl, won, lost, net, sls: sum((x) => x.sl), green: ds.filter((x) => x.won - x.lost > 0).length,
      pf: lost ? won / lost : Infinity, wr: signals ? (wins / signals) * 100 : null, signals,
      noSl, bestWeek: wl.reduce((a, b) => (!a || b.net > a.net ? b : a), null), avgWeek: wl.length ? net / wl.length : 0,
      months: [...months.entries()].sort((a, b) => a[0].localeCompare(b[0])),
      cum: ds.map((x) => ({ x: x.d, y: (c += x.won - x.lost) })),
      usd1: sum((x) => x.usd) * (1 - deduct), deduct,
      from: ds.length ? ds[0].d : null, to: ds.length ? ds[ds.length - 1].d : null
    };
  }

  // ---------------------------------------------------------------- pieces
  function badge(room) {
    if (room.hype) return `<span class="ss-hype">HYPE</span>`;
    const pal = { 1: ["#6e4f12", "#c89f3a", "#f6e4a6"], 2: ["#5c6069", "#b4b8c1", "#eef0f4"], 3: ["#5a2e14", "#b06a3b", "#f0b38a"] }[room.medal] || ["#555", "#999", "#ddd"];
    const id = "ssm" + room.id;
    return `<svg viewBox="0 0 40 46" width="30" height="35" aria-hidden="true">
      <defs><radialGradient id="${id}" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="${pal[2]}"/><stop offset=".6" stop-color="${pal[1]}"/><stop offset="1" stop-color="${pal[0]}"/></radialGradient></defs>
      <path d="M12 0h7l-3 14h-7zM28 0h-7l3 14h7z" fill="#e52150" opacity=".85"/>
      <circle cx="20" cy="28" r="15" fill="url(#${id})" stroke="${pal[0]}"/>
      <circle cx="20" cy="28" r="10.5" fill="none" stroke="${pal[2]}" stroke-opacity=".6"/>
      <text x="20" y="33" text-anchor="middle" fill="#2a1a08" style="font:700 14px var(--font-head)">${room.medal}</text></svg>`;
  }

  // the orbit: one gold arc per month around the net total, thicker for bigger months
  function orbit(s) {
    const R = 100, C = 140, pos = s.months.map(([m, v]) => [m, Math.max(0, v)]).filter(([, v]) => v > 0);
    const tot = pos.reduce((a, [, v]) => a + v, 0), top = Math.max(1, ...pos.map(([, v]) => v));
    const gap = pos.length > 1 ? 3 : 0;
    const pt = (a, r) => [C + r * Math.cos((a * Math.PI) / 180), C + r * Math.sin((a * Math.PI) / 180)];
    let a0 = -90;
    const arcs = pos.map(([m, v], i) => {
      const sweep = Math.min(359.9, (v / tot) * 360 - gap), a1 = a0 + sweep;
      const [x0, y0] = pt(a0, R), [x1, y1] = pt(a1, R), [lx, ly] = pt(a0 + sweep / 2, R + 25);
      const out = `<path d="M${x0.toFixed(1)} ${y0.toFixed(1)} A${R} ${R} 0 ${sweep > 180 ? 1 : 0} 1 ${x1.toFixed(1)} ${y1.toFixed(1)}" stroke="url(#ssog)" stroke-width="${(12 + (10 * v) / top).toFixed(1)}" fill="none" opacity="${0.55 + 0.45 * (i % 2)}"><title>${esc(mShort(m))} ${sgn(v)} pips</title></path>
        ${sweep > 14 ? `<text x="${lx.toFixed(1)}" y="${(ly + 4).toFixed(1)}" text-anchor="middle" class="ss-olbl">${esc(mShort(m))}</text>` : ""}`;
      a0 = a1 + gap; return out;
    }).join("");
    return `<svg viewBox="-10 -10 300 300" role="img" aria-label="${esc(t("sig.d.net"))} ${sgn(s.net)}">
      <defs><linearGradient id="ssog" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f6e4a6"/><stop offset=".5" stop-color="#dcb84a"/><stop offset="1" stop-color="#a8832c"/></linearGradient></defs>
      <circle cx="${C}" cy="${C}" r="${R}" fill="none" stroke="rgba(255,255,255,.05)" stroke-width="24"/>${arcs}
      <circle class="ss-ospin" cx="${C}" cy="${C}" r="76" fill="none" stroke="rgba(229,33,80,.3)" stroke-width="3" stroke-dasharray="2 5"/>
      <text x="${C}" y="126" text-anchor="middle" class="ss-ok">${esc(t("ss.ring.net"))}</text>
      <text x="${C}" y="158" text-anchor="middle" class="ss-onet">${sgn(s.net)}</text>
      <text x="${C}" y="180" text-anchor="middle" class="ss-osub">${esc(t("ss.ring.sub", { w: s.weeks.length, d: s.days }))}</text></svg>`;
  }

  // a row per month, a polished gold tile per week; red dots count that week's stop losses
  function heat(s) {
    const max = Math.max(1, ...s.weeks.map((w) => w.net));
    const by = new Map(); for (const w of s.weeks) { const m = w.k.slice(0, 7); if (!by.has(m)) by.set(m, []); by.get(m).push(w); }
    return [...by.entries()].map(([m, ws]) => `<div class="ss-hrow"><small>${esc(mShort(m))}</small>${[0, 1, 2, 3, 4].map((i) => {
      const w = ws[i]; if (!w) return `<div class="ss-w ss-none" aria-hidden="true"></div>`;
      const a = w.net > 0 ? (0.25 + (0.75 * w.net) / max).toFixed(2) : "0.25";
      const dl = (-((i * 0.9 + Number(w.k.slice(8)) * 0.17) % 6)).toFixed(2);
      const tip = t("ss.week.tip", { d: dShort(w.k), p: sgn(w.net), s: w.sl });
      const dots = w.sl ? `<i>${"<span></span>".repeat(Math.min(w.sl, 6))}</i>` : "";
      return `<div class="ss-w${w.net < 0 ? " neg" : ""}" style="--a:${a};--dl:${dl}s" title="${esc(tip)}" aria-label="${esc(tip)}">${kfmt(w.net)}${dots}</div>`;
    }).join("")}<em>${sgn(ws.reduce((a, w) => a + w.net, 0))}</em></div>`).join("");
  }

  // ---------------------------------------------------------------- page
  function render(el) {
    if (!el) return;
    const D = root.OTM_SIGNALS || { rooms: [] };
    const deduct = D.deduct ?? 0.15;
    const hasData = (r) => (r.trades && r.trades.length) || (r.days && r.days.length);
    const rooms = D.rooms.map((r, k) => hasData(r) ? { ...r, real: true } : { ...r, real: false, trades: live ? [] : sample(r, k) });
    let cur = 0, lot = 10; // lot is the slider value: hundredths of a lot (10 = 0.1 lot)

    const lotOut = (s) => {
      const L = lot / 100, v = s.usd1 * L;
      return { big: usd(v), sub: t("ss.lot.sub", { l: num(L, 2), p: num(deduct * 100), w: usd(s.weeks.length ? v / s.weeks.length : 0) }) };
    };

    const draw = () => {
      const r = rooms[cur], isSample = !r.real && !live, s = stats(r, deduct);
      const rail = rooms.map((x, i) => {
        const xs = stats(x, deduct), soon = !x.real;
        return `<button type="button" role="tab" class="ss-room${i === cur ? " on" : ""}" aria-selected="${i === cur}" data-room="${i}">
          <span class="ss-medal">${badge(x)}</span>
          <span><b>${esc(x.name)}${x.flash ? " ⚡" : ""}</b>${soon ? `<span class="ss-pill">${t(live ? "ss.soon" : "sig.sample.pill")}</span>` : `<small class="ss-net">${sgn(xs.net)} pips</small>`}</span></button>`;
      }).join("");

      let body;
      if (!s.days) body = `<p class="sig-soon">${t("sig.soon")}</p>`;
      else {
        const pf = s.pf === Infinity ? "∞" : num(s.pf, s.pf >= 10 ? 0 : 1);
        const rows = [
          [t("sig.d.green"), t("ss.v.days", { a: s.green, b: s.days })],
          s.wr != null ? [t("sig.k.wr"), `${num(s.wr)}% <small>(${s.signals})</small>`] : null,
          [t("sig.d.won"), `<span class="up">${sgn(s.won)}</span>`],
          [t("sig.d.lost"), `<span class="down">${sgn(-s.lost)}</span>`],
          [t("ss.l.sl"), t("ss.v.times", { n: s.sls })],
          [t("sig.k.pf"), pf],
          [t("sig.d.avgWeek"), sgn(s.avgWeek)],
          [t("sig.d.bestWeek"), s.bestWeek ? sgn(s.bestWeek.net) : "–"],
          [t("ss.l.noSl"), t(s.noSl === 1 ? "ss.v.week" : "ss.v.weeks", { n: s.noSl })]
        ].filter(Boolean).map(([k, v]) => `<li><span>${k}</span><i></i><b>${v}</b></li>`).join("");
        const cum = root.OTMCharts ? root.OTMCharts.bars(s.months.map(([m, v]) => ({ label: mShort(m), value: v, sub: "" })), { fmt: (x) => sgn(x) + " pips", short: (x) => kfmt(x), label: t("sig.byMonth"), ...(el.clientWidth < 600 ? { w: 440, h: 250 } : { w: 900, h: 240 }) }) : "";
        const o = lotOut(s);
        body = `
          <div class="ss-top"><div class="ss-card ss-orbit">${orbit(s)}</div><div class="ss-card ss-ledger"><h4>${t("ss.ledger")}</h4><ul>${rows}</ul></div></div>
          <div class="ss-card ss-cum"><h4>${t("sig.byMonth")}</h4>${cum}</div>
          <div class="ss-card"><h4>${t("ss.weeks")}</h4><div class="ss-heat">${heat(s)}</div>
            <div class="ss-legend"><span>${t("ss.legend.gold")}</span><span><span class="ss-dot"></span>${t("ss.legend.sl")}</span></div></div>
          <div class="ss-card ss-lot"><div><h4>${t("sig.benefit")}</h4>
              <input type="range" min="1" max="100" step="1" value="${lot}" id="ss-lot" aria-label="${esc(t("ss.lot"))}">
              <div class="ss-chips">${[1, 10, 50, 100].map((v) => `<button type="button" data-lot="${v}" class="${v === lot ? "on" : ""}">${num(v / 100, v === 100 ? 1 : 2)}${v === 100 ? " lot" : ""}</button>`).join("")}</div></div>
            <div class="ss-out" aria-live="polite"><b id="ss-usd">${o.big}</b><small id="ss-usd-sub">${o.sub}</small></div></div>`;
      }

      el.innerHTML = `<div class="ss">
        <nav class="ss-rail" role="tablist" aria-label="${esc(t("sig.rooms"))}">${rail}</nav>
        <div class="ss-panel">
          ${isSample ? `<div class="sig-sample"><b>${t("sig.sample.t")}</b> ${t("sig.sample.d")}</div>` : ""}
          <div class="ss-head"><h3>${esc(r.name)}</h3><span>${t("sig.source", { s: esc(r.source || "") })}${s.from ? ` · ${dShort(s.from)} – ${dShort(s.to, true)}` : ""}${r.days && r.days.length ? ` · ${t("ss.fromWeekly")}` : ""}</span></div>
          ${body}
          <p class="sig-note">${t(r.days && r.days.length ? "sig.d.note" : "sig.note")}</p>
        </div></div>`;

      el.querySelectorAll("[data-room]").forEach((b) => b.addEventListener("click", () => { cur = +b.dataset.room; draw(); }));
      const range = el.querySelector("#ss-lot");
      if (range) {
        const update = () => {
          const o = lotOut(s);
          el.querySelector("#ss-usd").textContent = o.big;
          el.querySelector("#ss-usd-sub").textContent = o.sub;
          range.value = lot;
          el.querySelectorAll("[data-lot]").forEach((c) => c.classList.toggle("on", +c.dataset.lot === lot));
        };
        range.addEventListener("input", () => { lot = +range.value; update(); });
        el.querySelectorAll("[data-lot]").forEach((c) => c.addEventListener("click", () => { lot = +c.dataset.lot; update(); }));
      }
    };
    draw();
    document.addEventListener("otm:lang", draw);
  }

  root.OTMSignals = { render, stats };
})(window);
