// Small hand-made SVG charts in the brand colours. No chart library needed.
(function (root) {
  const NS = "http://www.w3.org/2000/svg";
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  let gid = 0;

  // gold crescent gauge for a 0-100 score (the site's signature arc)
  function gauge(score, label) {
    const r = 70, cx = 90, cy = 90, a0 = Math.PI * 0.8, a1 = Math.PI * 2.2;
    const pt = (a) => [cx + r * Math.cos(a), cy + r * Math.sin(a)];
    const arc = (from, to) => { const [x0, y0] = pt(from), [x1, y1] = pt(to); return `M${x0.toFixed(2)},${y0.toFixed(2)} A${r},${r} 0 ${to - from > Math.PI ? 1 : 0} 1 ${x1.toFixed(2)},${y1.toFixed(2)}`; };
    const v = Math.max(0, Math.min(100, score));
    const id = "g" + ++gid;
    return `<svg class="gauge" viewBox="0 0 180 160" role="img" aria-label="${esc(label)} ${v}">
      <defs><linearGradient id="${id}" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#E52150"/><stop offset="1" stop-color="#F4EB06"/></linearGradient></defs>
      <path d="${arc(a0, a1)}" fill="none" stroke="var(--line)" stroke-width="10" stroke-linecap="round"/>
      ${v > 0 ? `<path class="gauge__val" d="${arc(a0, a0 + (a1 - a0) * (v / 100))}" fill="none" stroke="url(#${id})" stroke-width="10" stroke-linecap="round"/>` : ""}
      <text x="90" y="98" text-anchor="middle" class="gauge__num">${v}</text>
      <text x="90" y="122" text-anchor="middle" class="gauge__lbl">/ 100</text>
    </svg>`;
  }

  // six-axis radar
  function radar(parts, labels) {
    const keys = Object.keys(parts), n = keys.length, cx = 150, cy = 118, R = 82;
    const pt = (i, v) => { const a = -Math.PI / 2 + (i / n) * Math.PI * 2; return [cx + R * (v / 100) * Math.cos(a), cy + R * (v / 100) * Math.sin(a)]; };
    const ring = (v) => keys.map((_, i) => pt(i, v).map((x) => x.toFixed(1)).join(",")).join(" ");
    const shape = keys.map((k, i) => pt(i, Math.max(4, parts[k])).map((x) => x.toFixed(1)).join(",")).join(" ");
    const lbl = keys.map((k, i) => {
      const [x, y] = pt(i, 122);
      const anchor = Math.abs(x - cx) < 8 ? "middle" : x > cx ? "start" : "end";
      return `<text x="${x.toFixed(1)}" y="${(y + 4).toFixed(1)}" text-anchor="${anchor}" class="radar__lbl">${esc(labels[k])} <tspan class="radar__v">${Math.round(parts[k])}</tspan></text>`;
    }).join("");
    return `<svg class="radar" viewBox="-104 -6 508 248" role="img" aria-label="radar">
      ${[25, 50, 75, 100].map((v) => `<polygon points="${ring(v)}" fill="none" stroke="var(--line)" stroke-width="1"/>`).join("")}
      ${keys.map((_, i) => { const [x, y] = pt(i, 100); return `<line x1="${cx}" y1="${cy}" x2="${x.toFixed(1)}" y2="${y.toFixed(1)}" stroke="var(--line)"/>`; }).join("")}
      <polygon points="${shape}" fill="rgba(244,235,6,.2)" stroke="#F4EB06" stroke-width="2" stroke-linejoin="round"/>
      ${lbl}
    </svg>`;
  }

  // line + area chart. points: [{x: Date|string, y: number}]
  function line(points, opts = {}) {
    const W = opts.w || 900, H = opts.h || 280, P = { l: 84, r: 14, t: 14, b: 28 };
    if (points.length < 2) points = points.length ? [{ x: points[0].x, y: 0 }, points[0]] : [{ x: Date.now(), y: 0 }, { x: Date.now(), y: 0 }];
    const ys = points.map((p) => p.y), min = Math.min(0, ...ys), max = Math.max(0, ...ys), span = max - min || 1;
    const X = (i) => P.l + (i / (points.length - 1)) * (W - P.l - P.r);
    const Y = (v) => P.t + (1 - (v - min) / span) * (H - P.t - P.b);
    const d = points.map((p, i) => `${i ? "L" : "M"}${X(i).toFixed(1)},${Y(p.y).toFixed(1)}`).join("");
    const area = `${d}L${X(points.length - 1).toFixed(1)},${Y(Math.max(min, 0)).toFixed(1)}L${X(0).toFixed(1)},${Y(Math.max(min, 0)).toFixed(1)}Z`;
    const id = "l" + ++gid;
    const ticks = [max, (max + min) / 2, min].map((v) => `<text x="${P.l - 8}" y="${(Y(v) + 4).toFixed(1)}" text-anchor="end" class="axis">${esc(opts.fmt ? opts.fmt(v) : v.toFixed(0))}</text><line x1="${P.l}" x2="${W - P.r}" y1="${Y(v).toFixed(1)}" y2="${Y(v).toFixed(1)}" stroke="var(--line)" stroke-dasharray="${v === 0 ? "" : "3 5"}"/>`).join("");
    const dl = (i) => opts.dateFmt ? opts.dateFmt(points[i].x) : "";
    return `<svg class="linechart" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(opts.label || "chart")}">
      <defs><linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F4EB06" stop-opacity=".32"/><stop offset="1" stop-color="#F4EB06" stop-opacity="0"/></linearGradient></defs>
      ${ticks}
      <path d="${area}" fill="url(#${id})"/>
      <path d="${d}" fill="none" stroke="#F4EB06" stroke-width="2.5" stroke-linejoin="round"/>
      <text x="${P.l}" y="${H - 6}" class="axis">${esc(dl(0))}</text>
      <text x="${W - P.r}" y="${H - 6}" text-anchor="end" class="axis">${esc(dl(points.length - 1))}</text>
    </svg>`;
  }

  // vertical bars, green up / red down. items: [{label, value, sub}]
  function bars(items, opts = {}) {
    const W = opts.w || 640, H = opts.h || 220, P = { l: 12, r: 12, t: 24, b: 40 };
    const vals = items.map((i) => i.value), max = Math.max(0, ...vals), min = Math.min(0, ...vals), span = max - min || 1;
    const bw = (W - P.l - P.r) / Math.max(1, items.length);
    const Y = (v) => P.t + (1 - (v - min) / span) * (H - P.t - P.b);
    const zero = Y(0);
    return `<svg class="barchart" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(opts.label || "bars")}">
      <line x1="${P.l}" x2="${W - P.r}" y1="${zero}" y2="${zero}" stroke="var(--line)"/>
      ${items.map((it, i) => {
        const x = P.l + i * bw + bw * 0.2, w = bw * 0.6, y = Math.min(Y(it.value), zero), h = Math.max(2, Math.abs(Y(it.value) - zero));
        const cls = it.value > 0 ? "bar--up" : it.value < 0 ? "bar--down" : "bar--flat";
        return `<rect class="${cls}" x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${w.toFixed(1)}" height="${h.toFixed(1)}" rx="3"><title>${esc(it.label)}: ${esc(opts.fmt ? opts.fmt(it.value) : it.value)}</title></rect>
          <text x="${(x + w / 2).toFixed(1)}" y="${(it.value >= 0 ? y - 6 : y + h + 13).toFixed(1)}" text-anchor="middle" class="bar__v">${esc(opts.short ? opts.short(it.value) : "")}</text>
          <text x="${(x + w / 2).toFixed(1)}" y="${H - 20}" text-anchor="middle" class="axis axis--strong">${esc(it.label)}</text>
          <text x="${(x + w / 2).toFixed(1)}" y="${H - 6}" text-anchor="middle" class="axis">${esc(it.sub || "")}</text>`;
      }).join("")}
    </svg>`;
  }

  root.OTMCharts = { gauge, radar, line, bars, esc };
})(window);
