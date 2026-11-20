// Leaderboard tab "Autotrade (simulated)": what copying the signal rooms would have made, from the rooms'
// real closed results. Members come from js/autotrade-data.js with their real lot and start day; every
// figure is labelled simulated and is never mixed into the real leaderboard.
(function (root) {
  const I = root.OTMI18n, t = (k, v) => I.t(k, v);
  const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const usd = (v) => (v < 0 ? "−$" : "+$") + Math.abs(Math.round(v)).toLocaleString("en-US");
  const LOTS = [0.03, 0.1, 0.5, 1, 3];
  const ROOM_ICON = { swing: "🥇", scalp: "⚡", rr: "🎯", hype: "₿" };

  // dollars per 1.0 lot, per room per day, before the deduction
  function perDay(rooms) {
    const out = new Map();
    for (const r of rooms) {
      const m = new Map(), pv = r.pipValue || {}, first = Object.values(pv)[0] || 10;
      if (r.days && r.days.length) for (const d of r.days) m.set(d[0], (m.get(d[0]) || 0) + (d[1] - d[2]) * first);
      else for (const x of r.trades || []) m.set(x[0], (m.get(x[0]) || 0) + x[3] * (pv[x[1]] ?? 10));
      out.set(r.id, m);
    }
    return out;
  }
  const sumFrom = (map, ids, from) => { let s = 0; for (const id of ids) for (const [d, v] of map.get(id) || []) if (!from || d >= from) s += v; return s; };

  async function render(el, { period, start }) {
    const A = root.OTM_AUTOTRADE || { rooms: [], members: [], deduct: 0.15 };
    el.innerHTML = `<div class="loading"><img src="assets/img/mark.svg" alt="" width="56" height="56"></div>`;
    const rooms = root.OTMSignals ? await root.OTMSignals.rooms() : [];
    const map = perDay(rooms), ids = A.rooms.filter((id) => map.has(id)), keep = 1 - (A.deduct ?? 0.15);
    // period start as a calendar day (Thai time, like the rest of the leaderboard)
    const from = start ? new Date(start.getTime() + 7 * 3600e3).toISOString().slice(0, 10) : null;
    const last = [...map.values()].flatMap((m) => [...m.keys()]).sort().pop() || "";
    const base = sumFrom(map, ids, from) * keep;
    const members = (A.members || []).filter((m) => m && m.name && +m.lot > 0).map((m) => {
      const rs = (m.rooms || ids).filter((id) => map.has(id)), f = [from, m.start].filter(Boolean).sort().pop() || null;
      return { name: m.name, profit: sumFrom(map, rs, f) * keep * +m.lot };
    }).sort((a, b) => b.profit - a.profit);
    const roomNames = rooms.filter((r) => ids.includes(r.id)).map((r) => `${ROOM_ICON[r.id] || ""} ${esc(r.name)}`).join(" · ");
    el.innerHTML = `
      <div class="at-banner"><span aria-hidden="true">ℹ️</span><div><b>${t("at.banner.t")}</b><p>${t("at.banner.d", { p: Math.round((A.deduct ?? 0.15) * 100) })}</p></div></div>
      <div class="at-kpis">
        <div class="card"><span>${t("at.k.members")}</span><b>${members.length ? members.length : "–"}</b></div>
        <div class="card"><span>${t("at.k.rooms")}</span><b class="at-rooms">${roomNames || "–"}</b></div>
        <div class="card"><span>${t("at.k.updated")}</span><b>${last ? I.fmt.date(last + "T12:00:00") : "–"}</b></div>
      </div>
      ${members.length ? `<section class="card at-list"><table class="table"><thead><tr><th>${t("at.col.rank")}</th><th>${t("at.col.member")}</th><th class="r">${t("at.col.profit")}</th></tr></thead><tbody>
        ${members.map((m, i) => `<tr><td><span class="at-rk ${i < 3 ? "at-rk--" + (i + 1) : ""}">${i + 1}</span></td><td>${esc(m.name)} <span class="at-sim">${t("at.sim")}</span></td>
          <td class="r ${m.profit >= 0 ? "up" : "down"}"><b>${usd(m.profit)}</b></td></tr>`).join("")}</tbody></table></section>`
        : `<p class="card at-empty">${t("at.empty")}</p>`}
      <section class="card at-scn"><h3>${t("at.scn.t")}</h3><p class="card__sub">${t("at.scn.d")}</p>
        <div class="at-scn__grid">${LOTS.map((l) => `<div><span>${l} lot</span><b class="${base >= 0 ? "up" : "down"}">${usd(base * l)}</b><small>${t("at.sim")}</small></div>`).join("")}</div></section>`;
  }

  root.OTMAutotrade = { render, perDay };
})(window);
