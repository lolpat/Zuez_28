// Member portal: dashboard, journal, tools, IB network, profile.
(function () {
  const I = window.OTMI18n, S = window.OTMStats, C = window.OTMCharts, cfg = window.OTM_CONFIG;
  const { t, fmt } = I;
  const esc = C.esc;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];

  const state = {
    store: null, me: null, accounts: [], trades: [], upline: null, downline: null,
    f: { account: "all", period: "month", side: "all", outcome: "all", symbol: "all" },
    eq: "cum", cal: null, shown: 25, timer: null, netQuery: ""
  };

  const ICON = {
    dashboard: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3.5" y="3.5" width="7" height="8" rx="2"/><rect x="13.5" y="3.5" width="7" height="5" rx="2"/><rect x="13.5" y="11.5" width="7" height="9" rx="2"/><rect x="3.5" y="14.5" width="7" height="6" rx="2"/></svg>',
    journal: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M6 3.5h11a1.5 1.5 0 0 1 1.5 1.5v14a1.5 1.5 0 0 1-1.5 1.5H6z"/><path d="M6 3.5v17M9.5 8h5.5M9.5 11.5h5.5"/><path d="m10 17 2-2.5 2 1.5 2.5-3"/></svg>',
    tools: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="4.5" y="3" width="15" height="18" rx="3"/><path d="M8 7h8M8 11h1.5M11.3 11h1.5M14.6 11H16M8 14.5h1.5M11.3 14.5h1.5M14.6 14.5H16M8 18h8"/></svg>',
    network: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><circle cx="12" cy="19" r="2.5"/><circle cx="19" cy="19" r="2.5"/><path d="M12 7.5v9M12 12H5v4.5M12 12h7v4.5"/></svg>',
    profile: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="8.5" r="3.8"/><path d="M4.5 20c1.4-3.6 4.3-5.2 7.5-5.2s6.1 1.6 7.5 5.2"/></svg>'
  };

  // ------------------------------------------------------------ helpers
  const money = (v, signed = true) => fmt.money(v, signed);
  const cls = (v) => (v > 0 ? "up" : v < 0 ? "down" : "");
  const pf = (v) => (v === Infinity ? "∞" : fmt.num(v, 2));
  const initials = (n) => String(n || "?").trim().split(/\s+/).map((w) => w[0]).slice(0, 2).join("").toUpperCase();
  const brokerName = (id) => (cfg.BROKERS.find((b) => b.id === id) || { name: id }).name;
  const isIB = () => state.me && (state.me.role === "ib" || state.me.role === "owner");
  const approved = () => state.me && state.me.status === "approved";
  const accName = (a) => `${brokerName(a.broker)} · ${a.account_number}`;
  const dur = (mins) => { const h = Math.floor(mins / 60), m = Math.round(mins % 60); if (!h) return I.lang === "th" ? `${m} นาที` : `${m}m`; return I.lang === "th" ? `${h} ชม. ${m} นาที` : `${h}h ${m}m`; };

  function toast(msg) {
    const el = $("#toast"); el.textContent = msg; el.classList.add("show");
    clearTimeout(toast.t); toast.t = setTimeout(() => el.classList.remove("show"), 2600);
  }
  const fail = (e) => toast(t("app.error", { msg: e && e.message ? e.message : String(e) }));

  // ------------------------------------------------------------ modal
  let lastFocus = null;
  function openModal(title, html, onMount) {
    const m = $("#modal");
    lastFocus = document.activeElement;
    $("#modal-title").textContent = title;
    $("#modal-body").innerHTML = html;
    m.hidden = false; requestAnimationFrame(() => m.classList.add("show"));
    document.body.style.overflow = "hidden";
    if (onMount) onMount($("#modal-body"));
    const first = $("#modal-body input, #modal-body select, #modal-body textarea, #modal-body button");
    (first || $(".modal__x")).focus();
  }
  function closeModal() {
    const m = $("#modal"); m.classList.remove("show");
    setTimeout(() => { m.hidden = true; $("#modal-body").innerHTML = ""; }, 220);
    document.body.style.overflow = "";
    if (lastFocus) lastFocus.focus();
  }

  // ------------------------------------------------------------ shell
  const routes = () => {
    const r = [["dashboard", "app.dashboard"], ["journal", "app.journal"], ["tools", "app.tools"]];
    if (isIB()) r.push(["network", "app.network"]);
    r.push(["profile", "app.profile"]);
    return r;
  };
  function renderShell() {
    const m = state.me;
    const roleBadge = { member: "", ib: "badge--gold", owner: "badge--gold" }[m.role];
    $("#me").innerHTML = `<span class="avatar">${esc(initials(m.full_name))}</span>
      <div><b>${esc(m.full_name || m.email)}</b><span class="badge ${roleBadge}">${t("app.role." + m.role)}</span></div>`;
    const cur = currentRoute();
    $("#nav").innerHTML = routes().map(([id, key]) => `<a href="#${id}" ${id === cur ? 'aria-current="page"' : ""}>${ICON[id]}<span>${t(key)}</span></a>`).join("");
    $("#demo-badge").hidden = state.store.live;
    const r = routes().find(([id]) => id === cur);
    $("#page-title").textContent = r ? t(r[1]) : "";
    document.title = `${r ? t(r[1]) : ""} | Order The Market`;
    I.apply($(".sidebar"));
    I.apply($(".topbar"));
  }
  function currentRoute() {
    const h = location.hash.replace("#", "") || "dashboard";
    return routes().some(([id]) => id === h) ? h : "dashboard";
  }
  function setMenu(open) {
    $("#sidebar").classList.toggle("open", open);
    $("#scrim").classList.toggle("show", open);
    $("#menu-btn").setAttribute("aria-expanded", String(open));
  }

  function render() {
    clearInterval(state.timer);
    renderShell();
    const v = $("#view");
    const r = currentRoute();
    ({ dashboard, journal, tools, network, profile })[r](v);
    v.focus({ preventScroll: true });
  }

  async function reload(what = ["accounts", "trades"]) {
    const st = state.store;
    const jobs = [];
    if (what.includes("accounts")) jobs.push(st.listAccounts().then((a) => { state.accounts = a; }));
    if (what.includes("trades")) jobs.push(st.listTrades().then((tr) => { state.trades = tr; }));
    if (what.includes("upline")) jobs.push(st.myUpline().then((u) => { state.upline = u; }));
    if (what.includes("downline") && isIB()) jobs.push(st.myDownline().then((d) => { state.downline = d; }));
    await Promise.all(jobs);
  }

  const riskNote = () => `<p class="risk-note">${t("app.risk")}</p>`;

  function statusCard() {
    if (approved()) return "";
    const rej = state.me.status === "rejected";
    return `<section class="card kpi--hero">
      <h3>${t(rej ? "rejected.title" : "pending.title")} <span class="badge ${rej ? "badge--bad" : "badge--warn"}">${t("net.status." + state.me.status)}</span></h3>
      <p class="muted" style="margin-top:8px">${t(rej ? "rejected.lead" : "pending.lead")}</p>
      ${!rej ? `<p style="margin-top:10px">${state.upline ? esc(t("pending.upline", { name: state.upline.full_name })) : t("pending.noupline")}</p>` : ""}
      <a class="btn btn--ghost btn--sm" style="margin-top:14px" href="${esc(cfg.TELEGRAM_URL)}" target="_blank" rel="noopener">${t("app.contact")}</a>
    </section>`;
  }

  // ------------------------------------------------------------ dashboard
  const SESSIONS = [
    { id: "sydney", name: "Sydney", tz: "Australia/Sydney", open: 7, close: 16 },
    { id: "tokyo", name: "Tokyo", tz: "Asia/Tokyo", open: 9, close: 18 },
    { id: "london", name: "London", tz: "Europe/London", open: 8, close: 17 },
    { id: "newyork", name: "New York", tz: "America/New_York", open: 8, close: 17 }
  ];
  function tzParts(tz, d) {
    const p = Object.fromEntries(new Intl.DateTimeFormat("en-US", { timeZone: tz, hourCycle: "h23", weekday: "short", year: "numeric", month: "numeric", day: "numeric", hour: "numeric", minute: "numeric" }).formatToParts(d).map((x) => [x.type, x.value]));
    return { wd: p.weekday, h: +p.hour, m: +p.minute, offset: (Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour, +p.minute) - Math.floor(d.getTime() / 6e4) * 6e4) / 6e4 };
  }
  function marketClosed(now) {
    const ny = tzParts("America/New_York", now);
    const mins = ny.h * 60 + ny.m;
    return ny.wd === "Sat" || (ny.wd === "Fri" && mins >= 17 * 60) || (ny.wd === "Sun" && mins < 17 * 60);
  }
  function hoursHtml() {
    const now = new Date();
    const localOff = -now.getTimezoneOffset();
    const weekend = marketClosed(now);
    const nowPct = ((now.getHours() * 60 + now.getMinutes()) / 1440) * 100;
    const rows = SESSIONS.map((s) => {
      const p = tzParts(s.tz, now);
      const cur = p.h * 60 + p.m, o = s.open * 60, c = s.close * 60;
      const open = !weekend && cur >= o && cur < c;
      const until = open ? c - cur : (o - cur + 1440) % 1440;
      const startLocal = ((o - p.offset + localOff) % 1440 + 1440) % 1440;
      const len = c - o;
      const segs = startLocal + len <= 1440 ? [[startLocal, len]] : [[startLocal, 1440 - startLocal], [0, startLocal + len - 1440]];
      return `<div class="hours__row ${open ? "is-open" : ""}">
        <span>${s.name}</span>
        <div class="hours__track">${segs.map(([a, l]) => `<i class="hours__seg" style="left:${(a / 14.4).toFixed(2)}%;width:${(l / 14.4).toFixed(2)}%"></i>`).join("")}<i class="hours__now" style="left:${nowPct.toFixed(2)}%"></i></div>
        <span class="hours__state">${weekend ? t("dash.closed") : open ? t("dash.open") + " · " + t("dash.closesIn", { t: dur(until) }) : t("dash.opensIn", { t: dur(until) })}</span>
      </div>`;
    }).join("");
    return `${rows}<div class="hours__scale"><span></span><div><span>00:00</span><span>06:00</span><span>12:00</span><span>18:00</span><span>24:00</span></div></div>
      ${weekend ? `<p class="muted" style="font-size:.86rem">${t("dash.weekend")}</p>` : ""}`;
  }

  function dashboard(v) {
    const m = state.me;
    const month = S.filterTrades(state.trades, { period: "month" });
    const st = S.compute(month);
    const all = S.compute(state.trades);
    const steps = [
      ["dash.step.tg", !!m.telegram, "#profile"],
      ["dash.step.acc", state.accounts.length > 0, "#profile"],
      ["dash.step.import", state.trades.length > 0, "#journal"],
      ["dash.step.note", state.trades.some((x) => x.note || x.feeling || x.lesson), "#journal"]
    ];
    if (isIB()) steps.push(["dash.step.share", (state.downline || []).length > 0, "#network"]);
    const done = steps.filter((s) => s[1]).length;

    v.innerHTML = `
      <div class="view-head"><div><p class="muted">${t("dash.welcome")}</p><h2>${esc(m.full_name || m.email)}</h2></div></div>
      ${statusCard()}
      <div class="grid grid--21">
        <section class="card">
          <h3>${t("dash.hours")}</h3><p class="card__sub">${t("dash.hours.local")}</p>
          <div class="hours" id="hours">${hoursHtml()}</div>
        </section>
        <section class="card kpi--hero">
          <h3>${t("dash.month")} <a class="btn btn--ghost btn--sm" href="#journal">${t("dash.toJournal")}</a></h3>
          ${st.count ? `<div class="score" style="margin-top:6px">${C.gauge(all.score, t("j.score"))}
            <div class="stack" style="--g:0">
              <div><span class="kpi__lbl">${t("j.total")}</span><span class="kpi__val ${cls(st.total)}">${money(st.total)}</span><span class="kpi__sub">${st.count} ${t("dash.trades")}</span></div>
              <div><span class="kpi__lbl">${t("j.wr")}</span><span class="kpi__val">${fmt.num(st.winRate, 1)}%</span></div>
            </div></div>` : `<p class="muted" style="margin-top:12px">${t("dash.noData")}</p>`}
        </section>
      </div>
      <div class="grid grid--2">
        <section class="card">
          <h3>${t("dash.start")} <span class="badge">${t("dash.done", { n: done, m: steps.length })}</span></h3>
          <div class="progress"><i style="width:${(done / steps.length) * 100}%"></i></div>
          <ul class="checklist">${steps.map(([k, ok, href]) => `<li class="${ok ? "done" : ""}"><i class="tick"></i><span>${ok ? t(k) : `<a href="${href}">${t(k)}</a>`}</span></li>`).join("")}</ul>
        </section>
        <section class="card">
          <h3>${t("dash.upline")}</h3>
          ${state.upline ? `<div class="net-row__who" style="margin-top:14px"><span class="avatar">${esc(initials(state.upline.full_name))}</span><div><b>${esc(state.upline.full_name)}</b><small>${esc(state.upline.telegram || "")}</small></div></div>
            ${state.upline.telegram ? `<a class="btn btn--ghost btn--sm" style="margin-top:14px" target="_blank" rel="noopener" href="https://t.me/${esc(state.upline.telegram.replace(/^@/, ""))}">Telegram</a>` : ""}`
          : `<p class="muted" style="margin-top:10px">${t(m.role === "owner" ? "net.upline.none" : "pending.noupline")}</p>`}
        </section>
      </div>
      ${riskNote()}`;
    state.timer = setInterval(() => { const h = $("#hours"); if (h) h.innerHTML = hoursHtml(); }, 30000);
  }

  // ------------------------------------------------------------ journal
  function journal(v) {
    if (!approved()) { v.innerHTML = statusCard() + riskNote(); return; }
    const f = state.f;
    const base = state.trades.filter((x) => f.account === "all" || x.account_id === f.account);
    const symbols = [...new Set(base.map((x) => x.symbol))].sort();
    if (f.symbol !== "all" && !symbols.includes(f.symbol)) f.symbol = "all";
    const list = S.filterTrades(state.trades, f);
    const st = S.compute(list);
    const accs = state.accounts.filter((a) => f.account === "all" || a.id === f.account);
    const balance = accs.reduce((s, a) => s + (+a.start_balance || 0), 0) + base.reduce((s, x) => s + S.net(x), 0);
    const seg = (key, opts) => `<div class="seg" role="group">${opts.map(([val, lbl]) => `<button type="button" data-f="${key}" data-v="${val}" aria-pressed="${f[key] === val}">${t(lbl)}</button>`).join("")}</div>`;
    const sess = st.bestSession;

    v.innerHTML = `
      <div class="view-head">
        <h2>Trading Journal</h2>
        <div class="actions">
          <select class="input" id="acc-pick" aria-label="account" style="width:auto;min-height:44px">
            <option value="all">${t("j.allAccounts")}</option>
            ${state.accounts.map((a) => `<option value="${a.id}" ${f.account === a.id ? "selected" : ""}>${esc(accName(a))}</option>`).join("")}
          </select>
          <button class="btn btn--ghost" type="button" id="btn-import">${t("j.import")}</button>
          <button class="btn btn--gold" type="button" id="btn-add">${t("j.add")}</button>
        </div>
      </div>
      <div class="filters">
        ${seg("period", [["today", "j.p.today"], ["week", "j.p.week"], ["month", "j.p.month"], ["year", "j.p.year"], ["all", "j.p.all"]])}
        ${seg("side", [["all", "j.side.all"], ["buy", "j.side.buy"], ["sell", "j.side.sell"]])}
        ${seg("outcome", [["all", "j.out.all"], ["win", "j.out.win"], ["loss", "j.out.loss"]])}
        <select class="input" id="sym-pick" aria-label="symbol"><option value="all">${t("j.sym.all")}</option>${symbols.map((s) => `<option ${f.symbol === s ? "selected" : ""}>${esc(s)}</option>`).join("")}</select>
      </div>

      <div class="kpis">
        <div class="card kpi kpi--hero"><span class="kpi__lbl">${t("j.balance")}</span><span class="kpi__val">${money(balance, false)}</span><span class="kpi__sub">${t("j.balance.sub")}</span></div>
        <div class="card kpi"><span class="kpi__lbl">${t("j.total")}</span><span class="kpi__val ${cls(st.total)}">${money(st.total)}</span><span class="kpi__sub">${t("j.total.sub", { n: st.count })}</span></div>
        <div class="card kpi"><span class="kpi__lbl">${t("j.pf")}</span><span class="kpi__val">${st.count ? pf(st.profitFactor) : "–"}</span><span class="kpi__sub">${t("j.pf.sub")}</span></div>
        <div class="card kpi"><span class="kpi__lbl">${t("j.wr")}</span><span class="kpi__val">${st.count ? fmt.num(st.winRate, 1) + "%" : "–"}</span><span class="kpi__sub">${t("j.wr.sub", { w: st.wins, l: st.losses })}</span></div>
        <div class="card kpi"><span class="kpi__lbl">${t("j.exp")}</span><span class="kpi__val ${cls(st.expectancy)}">${st.count ? money(st.expectancy) : "–"}</span><span class="kpi__sub">${t("j.exp.sub")}</span></div>
        <div class="card kpi"><span class="kpi__lbl">${t("j.session")}</span><span class="kpi__val">${sess ? t("j.session." + sess.key) : "–"}</span><span class="kpi__sub">${sess ? t("j.session.sub", { v: money(sess.net), n: sess.count }) : ""}</span></div>
      </div>

      ${st.count ? `
      <div class="grid grid--2">
        <section class="card" id="cal-card"></section>
        <section class="card">
          <h3>${t("j.score")}</h3><p class="card__sub">${t("j.score.sub")}</p>
          <div class="score">${C.gauge(st.score, t("j.score"))}${C.radar(st.parts, Object.fromEntries(Object.keys(st.parts).map((k) => [k, t("j.part." + k)])))}</div>
          <p class="muted" style="font-size:.86rem;margin-top:6px">${t("j.maxdd")}: <b class="down">${money(-st.maxDD)}</b> (${fmt.num(st.maxDDPct, 1)}%) · ${t("j.streak")}: <b>${st.bestStreak}</b></p>
        </section>
      </div>
      <section class="card">
        <h3>${t("j.equity")} ${seg("eq", [["cum", "j.eq.cum"], ["day", "j.eq.day"], ["week", "j.eq.week"]]).replace(/data-f="eq"/g, 'data-eq="1"').replace(/aria-pressed="(true|false)"/g, "")}</h3>
        <div id="eq-chart"></div>
      </section>
      <div class="grid grid--3">
        <section class="card"><h3>${t("j.bySymbol")}</h3>
          <div class="table-wrap"><table class="table"><thead><tr><th>${t("j.col.symbol")}</th><th class="r">${t("j.col.trades")}</th><th class="r">${t("j.col.wr")}</th><th class="r">${t("j.col.net")}</th></tr></thead>
          <tbody>${[...st.bySymbol.values()].sort((a, b) => b.net - a.net).map((g) => `<tr><td>${esc(g.key)}</td><td class="r">${g.count}</td><td class="r">${fmt.num(g.winRate, 0)}%</td><td class="r ${cls(g.net)}">${money(g.net)}</td></tr>`).join("")}</tbody></table></div>
        </section>
        <section class="card"><h3>${t("j.byDay")}</h3>${C.bars([0, 1, 2, 3, 4, 5, 6].filter((d) => d < 5 || st.byWeekday.has(d)).map((d) => { const g = st.byWeekday.get(d); return { label: t("wd." + d), value: g ? g.net : 0, sub: g ? fmt.num(g.winRate, 0) + "%" : "" }; }), { fmt: (x) => money(x), short: (x) => (x ? (x > 0 ? "+" : "−") + Math.abs(x).toFixed(0) : ""), label: t("j.byDay"), w: 300, h: 210 })}</section>
        <section class="card"><h3>${t("j.bySession")}</h3>${C.bars(["asia", "london", "newyork"].map((k) => { const g = st.bySession.get(k); return { label: t("j.session." + k), value: g ? g.net : 0, sub: g ? `${g.count} · ${fmt.num(g.winRate, 0)}%` : "" }; }), { fmt: (x) => money(x), short: (x) => (x ? (x > 0 ? "+" : "−") + Math.abs(x).toFixed(0) : ""), label: t("j.bySession"), w: 300, h: 210 })}</section>
      </div>
      <section class="card">
        <h3>${t("j.trades")} <span class="badge">${st.count}</span></h3>
        <div class="table-wrap"><table class="table table--click table--trades">
          <thead><tr><th>${t("j.col.date")}</th><th>${t("j.col.symbol")}</th><th>${t("j.col.side")}</th><th class="r">${t("j.col.lot")}</th><th class="r">${t("j.col.net")}</th><th class="r">${t("j.col.note")}</th></tr></thead>
          <tbody id="trade-rows"></tbody>
        </table></div>
        <div style="text-align:center;margin-top:14px"><button class="btn btn--quiet" type="button" id="more">${t("j.more")}</button></div>
      </section>`
      : `<section class="card empty"><h3>${t("j.empty.t")}</h3><p>${t("j.empty.d")}</p><button class="btn btn--gold" style="margin-top:18px" type="button" id="btn-import2">${t("j.import")}</button></section>`}
      ${riskNote()}`;

    // controls
    $$("[data-f]", v).forEach((b) => b.addEventListener("click", () => { f[b.dataset.f] = b.dataset.v; state.shown = 25; render(); }));
    $("#acc-pick", v).addEventListener("change", (e) => { f.account = e.target.value; render(); });
    $("#sym-pick", v).addEventListener("change", (e) => { f.symbol = e.target.value; render(); });
    $("#btn-import", v).addEventListener("click", importModal);
    const i2 = $("#btn-import2", v); if (i2) i2.addEventListener("click", importModal);
    $("#btn-add", v).addEventListener("click", () => addTradeModal());
    if (!st.count) return;

    // equity
    const eqBox = $("#eq-chart", v);
    const drawEq = () => {
      $$("[data-eq]", v).forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.v === state.eq)));
      const dateFmt = (x) => fmt.date(x, { day: "numeric", month: "short" });
      if (state.eq === "cum") eqBox.innerHTML = C.line(st.curve.map((p) => ({ x: p.time, y: p.value })), { fmt: (x) => money(x), dateFmt, label: t("j.equity") });
      else {
        const src = state.eq === "day" ? st.byDay : st.byWeek;
        const items = [...src.values()].sort((a, b) => a.key.localeCompare(b.key)).slice(state.eq === "day" ? -30 : -16);
        eqBox.innerHTML = C.bars(items.map((g) => ({ label: fmt.date(g.key + "T12:00:00", { day: "numeric", month: "numeric" }), value: g.net })), { fmt: (x) => money(x), label: t("j.equity") });
      }
    };
    $$("[data-eq]", v).forEach((b) => b.addEventListener("click", () => { state.eq = b.dataset.v; drawEq(); }));
    drawEq();

    // calendar
    const calList = S.filterTrades(state.trades, { ...f, period: "all" });
    if (!state.cal) { const last = list.length ? new Date(Math.max(...list.map((x) => +new Date(x.close_time)))) : new Date(); state.cal = new Date(last.getFullYear(), last.getMonth(), 1); }
    const drawCal = () => {
      const byDay = S.compute(calList).byDay;
      const first = state.cal, y = first.getFullYear(), mo = first.getMonth();
      const start = new Date(y, mo, 1 - ((first.getDay() + 6) % 7));
      const today = S.dayKey(new Date());
      const days = [];
      for (let i = 0; i < 42; i++) {
        const d = new Date(start.getFullYear(), start.getMonth(), start.getDate() + i);
        if (i >= 35 && d.getMonth() !== mo) break;
        const k = S.dayKey(d), g = byDay.get(k);
        const a = g ? Math.min(1, Math.abs(g.net) / 60) : 0;
        const bg = g ? (g.net >= 0 ? `rgba(123,200,143,${0.12 + a * 0.45})` : `rgba(240,87,90,${0.12 + a * 0.45})`) : "";
        days.push(`<div class="cal__d ${d.getMonth() !== mo ? "cal__d--out" : ""} ${k === today ? "cal__d--today" : ""}" ${bg ? `style="background:${bg}"` : ""} title="${g ? `${k}: ${money(g.net)} · ${g.count}` : k}"><i>${d.getDate()}</i>${g ? `<b>${g.net >= 0 ? "+" : "−"}${Math.abs(g.net) >= 1000 ? (Math.abs(g.net) / 1000).toFixed(1) + "k" : Math.abs(g.net).toFixed(0)}</b>` : ""}</div>`);
      }
      const monthTotal = [...byDay.values()].filter((g) => g.key.startsWith(`${y}-${String(mo + 1).padStart(2, "0")}`)).reduce((s, g) => s + g.net, 0);
      $("#cal-card", v).innerHTML = `<h3>${t("j.calendar")} <span class="${cls(monthTotal)}" style="font-size:.95rem">${money(monthTotal)}</span></h3>
        <div class="cal__head" style="margin-top:10px"><button class="cal__nav" type="button" data-cal="-1" aria-label="previous month">‹</button><b>${fmt.date(first, { month: "long", year: "numeric" })}</b><button class="cal__nav" type="button" data-cal="1" aria-label="next month">›</button></div>
        <div class="cal">${[0, 1, 2, 3, 4, 5, 6].map((d) => `<span class="cal__wd">${t("wd." + d)}</span>`).join("")}${days.join("")}</div>`;
      $$("[data-cal]", v).forEach((b) => b.addEventListener("click", () => { state.cal = new Date(y, mo + +b.dataset.cal, 1); drawCal(); }));
    };
    drawCal();

    // trade rows
    const sorted = [...list].sort((a, b) => new Date(b.close_time) - new Date(a.close_time));
    const drawRows = () => {
      $("#trade-rows", v).innerHTML = sorted.slice(0, state.shown).map((x) => {
        const n = S.net(x), noted = x.note || x.feeling || x.lesson || (x.tags && x.tags.length);
        return `<tr data-id="${esc(x.id)}" tabindex="0">
          <td class="c-date">${fmt.dateTime(x.close_time)}</td><td class="c-sym">${esc(x.symbol)}</td>
          <td class="c-side side-${x.side}">${x.side === "buy" ? "Buy" : "Sell"}</td><td class="r c-lot">${fmt.num(x.volume, 2)}</td>
          <td class="r c-net ${cls(n)}">${money(n)}</td><td class="r c-note">${noted ? '<span class="dot" title="note"></span>' : '<span class="muted">+</span>'}</td></tr>`;
      }).join("");
      $("#more", v).hidden = state.shown >= sorted.length;
      $$("#trade-rows tr", v).forEach((tr) => {
        const open = () => noteModal(state.trades.find((x) => x.id === tr.dataset.id));
        tr.addEventListener("click", open);
        tr.addEventListener("keydown", (e) => { if (e.key === "Enter") open(); });
      });
    };
    $("#more", v).addEventListener("click", () => { state.shown += 50; drawRows(); });
    drawRows();
  }

  const FEELINGS = ["calm", "focused", "confident", "anxious", "fomo", "revenge", "tired"];
  function noteModal(tr) {
    if (!tr) return;
    const n = S.net(tr);
    let tags = [...(tr.tags || [])], exec = tr.execution || 0, feel = tr.feeling || "";
    openModal(t("note.title"), `
      <p class="muted" style="margin-top:-8px"><b class="${tr.side === "buy" ? "side-buy" : "side-sell"}">${tr.side === "buy" ? "Buy" : "Sell"}</b> ${esc(tr.symbol)} · ${fmt.num(tr.volume, 2)} lot · ${fmt.dateTime(tr.open_time)} → ${fmt.dateTime(tr.close_time)} · <b class="${cls(n)}">${money(n)}</b></p>
      <form class="form-grid" id="note-form" style="margin-top:18px">
        <label class="field"><span>${t("note.what")}</span><textarea class="input" name="note" placeholder="${esc(t("note.what.ph"))}">${esc(tr.note || "")}</textarea></label>
        <div class="field"><span>${t("note.feel")}</span><div class="chips" id="feel">${FEELINGS.map((k) => `<button type="button" class="chip" data-v="${k}" aria-pressed="${feel === k}">${t("feel." + k)}</button>`).join("")}</div></div>
        <div class="field"><span>${t("note.exec")}</span><div class="stars" id="stars">${[1, 2, 3, 4, 5].map((i) => `<button type="button" data-v="${i}" aria-label="${i}/5">★</button>`).join("")}</div></div>
        <div class="field"><span>${t("note.tags")}</span><div class="tags" id="tags"></div><input class="input" id="tag-in" placeholder="${esc(t("note.tags.ph"))}" enterkeyhint="done"></div>
        <label class="field"><span>${t("note.lesson")}</span><textarea class="input" name="lesson" placeholder="${esc(t("note.lesson.ph"))}">${esc(tr.lesson || "")}</textarea></label>
        <div class="modal__foot" style="justify-content:space-between">
          <button type="button" class="btn btn--danger btn--sm" id="del">${t("app.delete")}</button>
          <span style="display:flex;gap:10px"><button type="button" class="btn btn--quiet" data-close>${t("app.cancel")}</button><button class="btn btn--gold" type="submit">${t("app.save")}</button></span>
        </div>
      </form>`, (box) => {
      const drawStars = () => $$("#stars button", box).forEach((b) => b.classList.toggle("on", +b.dataset.v <= exec));
      const drawTags = () => {
        $("#tags", box).innerHTML = tags.map((g, i) => `<span class="tag">${esc(g)}<button type="button" data-i="${i}" aria-label="remove">×</button></span>`).join("");
        $$("#tags button", box).forEach((b) => b.addEventListener("click", () => { tags.splice(+b.dataset.i, 1); drawTags(); }));
      };
      $$("#feel .chip", box).forEach((b) => b.addEventListener("click", () => { feel = feel === b.dataset.v ? "" : b.dataset.v; $$("#feel .chip", box).forEach((c) => c.setAttribute("aria-pressed", String(c.dataset.v === feel))); }));
      $$("#stars button", box).forEach((b) => b.addEventListener("click", () => { exec = exec === +b.dataset.v ? 0 : +b.dataset.v; drawStars(); }));
      $("#tag-in", box).addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === ",") {
          e.preventDefault();
          const v = e.target.value.trim().replace(/,$/, "");
          if (v && !tags.includes(v) && tags.length < 12) tags.push(v.slice(0, 30));
          e.target.value = ""; drawTags();
        }
      });
      drawStars(); drawTags();
      $("#note-form", box).addEventListener("submit", async (e) => {
        e.preventDefault();
        const pending = $("#tag-in", box).value.trim(); if (pending && !tags.includes(pending)) tags.push(pending.slice(0, 30));
        const fields = { note: e.target.note.value.trim(), lesson: e.target.lesson.value.trim(), feeling: feel, execution: exec || null, tags };
        try { await state.store.updateTrade(tr.id, fields); Object.assign(tr, fields); closeModal(); toast(t("app.saved")); render(); } catch (err) { fail(err); }
      });
      $("#del", box).addEventListener("click", async (e) => {
        const btn = e.currentTarget;
        if (!btn.dataset.armed) { btn.dataset.armed = "1"; btn.textContent = t("app.confirmDelete"); return; }
        try { await state.store.deleteTrade(tr.id); state.trades = state.trades.filter((x) => x.id !== tr.id); closeModal(); render(); } catch (err) { fail(err); }
      });
    });
  }

  function importModal() {
    if (!state.accounts.length) {
      openModal(t("imp.title"), `<p class="alert alert--gold">${t("imp.needAcc")}</p><div class="modal__foot"><a class="btn btn--gold" href="#profile" data-close>${t("prof.addAcc")}</a></div>`);
      return;
    }
    let parsed = null;
    openModal(t("imp.title"), `
      <p class="muted" style="font-size:.88rem;margin-top:-6px">${t("imp.how")}</p>
      <form class="form-grid" id="imp-form" style="margin-top:18px">
        <label class="field"><span>${t("imp.account")}</span><select class="input" name="acc">${state.accounts.map((a) => `<option value="${a.id}" ${state.f.account === a.id ? "selected" : ""}>${esc(accName(a))}</option>`).join("")}</select></label>
        <label class="field"><span>${t("imp.file")}</span><input class="input" type="file" name="file" accept=".html,.htm,.csv,text/html,text/csv"></label>
        <div id="imp-msg"></div>
        <div class="modal__foot"><button type="button" class="btn btn--quiet" data-close>${t("app.cancel")}</button><button class="btn btn--gold" type="submit" disabled id="imp-go">${t("imp.go")}</button></div>
      </form>`, (box) => {
      const form = $("#imp-form", box), msg = $("#imp-msg", box), go = $("#imp-go", box);
      const check = () => {
        if (!parsed) return;
        const acc = state.accounts.find((a) => a.id === form.acc.value);
        const times = parsed.trades.map((x) => +new Date(x.close_time));
        let html = `<p class="alert alert--ok">${t("imp.found", { n: parsed.trades.length, from: fmt.date(Math.min(...times)), to: fmt.date(Math.max(...times)) })}</p>`;
        if (parsed.account_number && acc && parsed.account_number !== String(acc.account_number)) html += `<p class="alert alert--err" style="margin-top:10px">${esc(t("imp.mismatch", { file: parsed.account_number, acc: acc.account_number }))}</p>`;
        msg.innerHTML = html; go.disabled = false;
      };
      form.file.addEventListener("change", async () => {
        parsed = null; go.disabled = true; msg.innerHTML = "";
        const file = form.file.files[0]; if (!file) return;
        try { parsed = await window.OTMImporter.parseFile(file); check(); }
        catch { msg.innerHTML = `<p class="alert alert--err">${t("imp.none")}</p>`; }
      });
      form.acc.addEventListener("change", check);
      form.addEventListener("submit", async (e) => {
        e.preventDefault(); if (!parsed) return;
        go.disabled = true;
        try {
          const acc = state.accounts.find((a) => a.id === form.acc.value);
          if (acc && parsed.server && !acc.server) await state.store.updateAccount(acc.id, { server: parsed.server });
          const r = await state.store.importTrades(form.acc.value, parsed.trades);
          await reload(["accounts", "trades"]);
          state.f.account = form.acc.value; state.f.period = "all"; state.cal = null;
          closeModal(); toast(t("imp.done", { a: r.added, s: r.skipped })); render();
        } catch (err) { go.disabled = false; fail(err); }
      });
    });
  }

  function addTradeModal() {
    if (!state.accounts.length) return importModal();
    const now = new Date(); const local = (d) => new Date(d.getTime() - d.getTimezoneOffset() * 6e4).toISOString().slice(0, 16);
    openModal(t("add.title"), `
      <form class="form-grid form-grid--2" id="add-form">
        <label class="field span-2"><span>${t("imp.account")}</span><select class="input" name="acc">${state.accounts.map((a) => `<option value="${a.id}">${esc(accName(a))}</option>`).join("")}</select></label>
        <label class="field"><span>${t("add.symbol")}</span><input class="input" name="symbol" value="XAUUSD" required style="text-transform:uppercase"></label>
        <label class="field"><span>${t("add.side")}</span><select class="input" name="side"><option value="buy">Buy</option><option value="sell">Sell</option></select></label>
        <label class="field"><span>${t("add.volume")}</span><input class="input" name="volume" type="number" step="0.01" min="0.01" value="0.01" inputmode="decimal" required></label>
        <label class="field"><span>${t("add.profit")}</span><input class="input" name="profit" type="number" step="0.01" inputmode="decimal" required></label>
        <label class="field"><span>${t("add.open")}</span><input class="input" name="open" type="datetime-local" value="${local(new Date(now - 36e5))}" required></label>
        <label class="field"><span>${t("add.close")}</span><input class="input" name="close" type="datetime-local" value="${local(now)}" required></label>
        <label class="field"><span>${t("add.openPrice")}</span><input class="input" name="open_price" type="number" step="any" inputmode="decimal"></label>
        <label class="field"><span>${t("add.closePrice")}</span><input class="input" name="close_price" type="number" step="any" inputmode="decimal"></label>
        <label class="field"><span>${t("add.commission")}</span><input class="input" name="commission" type="number" step="0.01" value="0" inputmode="decimal"></label>
        <label class="field"><span>${t("add.swap")}</span><input class="input" name="swap" type="number" step="0.01" value="0" inputmode="decimal"></label>
        <div class="modal__foot span-2"><button type="button" class="btn btn--quiet" data-close>${t("app.cancel")}</button><button class="btn btn--gold" type="submit">${t("app.save")}</button></div>
      </form>`, (box) => {
      $("#add-form", box).addEventListener("submit", async (e) => {
        e.preventDefault();
        const F = e.target;
        if (!F.profit.value || !F.symbol.value.trim()) { (F.profit.value ? F.symbol : F.profit).setAttribute("aria-invalid", "true"); return; }
        const n = (x) => (x.value === "" ? null : +x.value);
        const row = {
          account_id: F.acc.value, symbol: F.symbol.value.trim().toUpperCase(), side: F.side.value, volume: +F.volume.value || 0,
          open_time: new Date(F.open.value).toISOString(), close_time: new Date(F.close.value).toISOString(),
          open_price: n(F.open_price), close_price: n(F.close_price), commission: +F.commission.value || 0, swap: +F.swap.value || 0, profit: +F.profit.value
        };
        try { const saved = await state.store.addTrade(row); state.trades.push(saved); closeModal(); toast(t("app.saved")); render(); } catch (err) { fail(err); }
      });
    });
  }

  // ------------------------------------------------------------ tools
  const PIP = { EURUSD: 10, GBPUSD: 10, AUDUSD: 10, NZDUSD: 10, USDJPY: 6.4, XAUUSD: 10, NAS100: 1, US30: 1 };
  function tools(v) {
    v.innerHTML = `
      <div class="grid grid--2">
        <section class="card">
          <h3>${t("tools.lot")}</h3><p class="card__sub">${t("tools.lot.lead")}</p>
          <form class="form-grid form-grid--2" id="lot" style="margin-top:18px">
            <label class="field"><span>${t("tools.balance")}</span><input class="input" name="bal" type="number" inputmode="decimal" value="1000" min="0"></label>
            <label class="field"><span>${t("tools.risk")}</span><input class="input" name="risk" type="number" inputmode="decimal" value="1" step="0.1" min="0"></label>
            <label class="field"><span>${t("tools.symbol")}</span><select class="input" name="sym">${Object.keys(PIP).map((s) => `<option>${s}</option>`).join("")}</select></label>
            <label class="field"><span>${t("tools.sl")}</span><input class="input" name="sl" type="number" inputmode="decimal" value="30" min="0"></label>
            <label class="field span-2"><span>${t("tools.pipValue")}</span><input class="input" name="pip" type="number" inputmode="decimal" value="10" step="0.1" min="0"><small>${t("tools.pipValue.hint")}</small></label>
          </form>
          <div class="grid grid--2" style="margin-top:18px">
            <div class="card kpi"><span class="kpi__lbl">${t("tools.riskAmt")}</span><span class="kpi__val" id="lot-risk"></span></div>
            <div class="card kpi kpi--hero"><span class="kpi__lbl">${t("tools.lots")}</span><span class="kpi__val" id="lot-out"></span><span class="kpi__sub" id="lot-note"></span></div>
          </div>
        </section>
        <section class="card">
          <h3>${t("tools.compound")}</h3><p class="card__sub">${t("tools.compound.lead")}</p>
          <form class="form-grid form-grid--2" id="cmp" style="margin-top:18px">
            <label class="field"><span>${t("tools.start")}</span><input class="input" name="start" type="number" inputmode="decimal" value="1000" min="0"></label>
            <label class="field"><span>${t("tools.monthly")}</span><input class="input" name="rate" type="number" inputmode="decimal" value="5" step="0.5"></label>
            <label class="field"><span>${t("tools.deposit")}</span><input class="input" name="dep" type="number" inputmode="decimal" value="100" min="0"></label>
            <label class="field"><span>${t("tools.months")}</span><input class="input" name="months" type="number" inputmode="numeric" value="12" min="1" max="120"></label>
          </form>
          <div class="kpis" style="grid-template-columns:repeat(3,1fr);margin-top:18px" id="cmp-out"></div>
          <div id="cmp-chart"></div>
          <p class="muted" style="font-size:.84rem">${t("tools.note")}</p>
        </section>
      </div>${riskNote()}`;
    const lot = $("#lot", v), cmp = $("#cmp", v);
    lot.sym.addEventListener("change", () => { lot.pip.value = PIP[lot.sym.value]; calcLot(); });
    const calcLot = () => {
      const riskAmt = (+lot.bal.value || 0) * (+lot.risk.value || 0) / 100;
      const lots = riskAmt / ((+lot.sl.value || 0) * (+lot.pip.value || 0) || Infinity);
      const floored = Math.floor(lots * 100) / 100;
      $("#lot-risk", v).textContent = money(riskAmt, false);
      $("#lot-out", v).textContent = floored >= 0.01 ? fmt.num(floored, 2) : "0.00";
      $("#lot-note", v).textContent = floored < 0.01 && riskAmt > 0 ? t("tools.lots.min") : "";
    };
    const calcCmp = () => {
      let bal = +cmp.start.value || 0; const r = (+cmp.rate.value || 0) / 100, dep = +cmp.dep.value || 0, n = Math.min(120, Math.max(1, +cmp.months.value || 1));
      const pts = [{ x: 0, y: bal }]; let deposited = bal;
      for (let i = 1; i <= n; i++) { bal = bal * (1 + r) + dep; deposited += dep; pts.push({ x: i, y: bal }); }
      $("#cmp-out", v).innerHTML = `<div class="card kpi kpi--hero"><span class="kpi__lbl">${t("tools.final")}</span><span class="kpi__val">${money(bal, false)}</span></div>
        <div class="card kpi"><span class="kpi__lbl">${t("tools.profit")}</span><span class="kpi__val ${cls(bal - deposited)}">${money(bal - deposited)}</span></div>
        <div class="card kpi"><span class="kpi__lbl">${t("tools.deposited")}</span><span class="kpi__val">${money(deposited, false)}</span></div>`;
      $("#cmp-chart", v).innerHTML = C.line(pts, { fmt: (x) => money(x, false), dateFmt: (x) => (I.lang === "th" ? `เดือน ${x}` : `Month ${x}`), label: t("tools.compound") });
    };
    lot.addEventListener("input", calcLot); cmp.addEventListener("input", calcCmp);
    calcLot(); calcCmp();
  }

  // ------------------------------------------------------------ IB network
  function network(v) {
    const me = state.me, list = state.downline || [];
    const owner = me.role === "owner";
    const link = location.href.replace(/app\.html.*$/, "") + "register.html?ref=" + encodeURIComponent(me.referral_code || "");
    const pend = list.filter((u) => u.status === "pending");
    const teamNet = list.reduce((s, u) => s + (+u.net_profit || 0), 0);
    const byId = new Map(list.map((u) => [u.id, u]));
    const upName = (u) => (u.upline_id === me.id ? me.full_name : byId.get(u.upline_id) ? byId.get(u.upline_id).full_name : "");

    // depth-first order so each person sits under their upline
    const kids = new Map();
    list.forEach((u) => { const k = byId.has(u.upline_id) ? u.upline_id : "root"; if (!kids.has(k)) kids.set(k, []); kids.get(k).push(u); });
    const ordered = []; const walk = (k, d) => (kids.get(k) || []).forEach((u) => { ordered.push({ u, d }); walk(u.id, d + 1); });
    walk("root", 0);

    const row = ({ u, d }) => {
      const st = { pending: "badge--warn", approved: "badge--ok", rejected: "badge--bad" }[u.status];
      return `<div class="net-row" data-search="${esc([u.full_name, u.email, u.telegram, u.accounts].join(" ").toLowerCase())}">
        <div class="net-row__who">
          <span class="net-indent">${"<i></i>".repeat(Math.min(d, 6))}</span>
          <span class="avatar">${esc(initials(u.full_name))}</span>
          <div><b>${esc(u.full_name || u.email)} ${u.role !== "member" ? `<span class="badge badge--gold">${t("app.role." + u.role)}</span>` : ""}</b>
          <small>${esc(u.telegram || "")} · ${esc(u.email || "")}</small></div>
        </div>
        <div class="net-row__meta"><span class="badge ${st}">${t("net.status." + u.status)}</span><span>${esc((u.brokers || "").split(",").filter(Boolean).map(brokerName).join(", "))} ${esc(u.accounts || "")}</span><span>${t("net.joined", { d: fmt.date(u.created_at) })}</span>${upName(u) ? `<span>${esc(t("net.under", { name: upName(u) }))}</span>` : ""}</div>
        <div class="net-row__meta">${u.trade_count ? `<span>${u.trade_count} ${t("dash.trades")}</span><b class="${cls(u.net_profit)}">${money(+u.net_profit)}</b><span>${t("net.wr", { v: fmt.num(u.win_rate || 0, 0) })}</span>` : `<span>${t("net.noTrades")}</span>`}</div>
        <div class="net-row__act">
          ${u.status !== "approved" ? `<button class="btn btn--gold btn--sm" data-st="approved" data-id="${u.id}">${t("net.approve")}</button>` : ""}
          ${u.status === "pending" ? `<button class="btn btn--quiet btn--sm" data-st="rejected" data-id="${u.id}">${t("net.reject")}</button>` : ""}
          ${owner && u.status === "approved" ? `<button class="btn btn--ghost btn--sm" data-role="${u.role === "ib" ? "member" : "ib"}" data-id="${u.id}">${t(u.role === "ib" ? "net.makeMember" : "net.makeIb")}</button>` : ""}
        </div>
      </div>`;
    };

    v.innerHTML = `
      <div class="view-head"><h2>${t("app.network")}</h2></div>
      <div class="grid grid--2">
        <section class="card">
          <h3>${t("net.upline")}</h3>
          ${state.upline ? `<div class="net-row__who" style="margin-top:14px"><span class="avatar">${esc(initials(state.upline.full_name))}</span><div><b>${esc(state.upline.full_name)}</b><small>${esc(state.upline.telegram || "")}</small></div></div>` : `<p class="muted" style="margin-top:10px">${t("net.upline.none")}</p>`}
          <p class="muted" style="font-size:.86rem;margin-top:14px">${t(owner ? "net.rule.owner" : "net.rule")}</p>
        </section>
        <section class="card kpi--hero">
          <h3>${t("net.code")}</h3>
          <div class="code-box"><span class="code">${esc(me.referral_code || "")}</span><button class="btn btn--ghost btn--sm" type="button" data-copy="${esc(me.referral_code || "")}">${t("app.copy")}</button></div>
          <p class="kpi__lbl" style="margin-top:14px">${t("net.link")}</p>
          <div class="code-box"><span class="code-link">${esc(link)}</span><button class="btn btn--ghost btn--sm" type="button" data-copy="${esc(link)}">${t("app.copy")}</button></div>
        </section>
      </div>
      <div class="kpis" style="grid-template-columns:repeat(2,1fr)">
        <div class="card kpi"><span class="kpi__lbl">${t("net.total")}</span><span class="kpi__val">${list.length}</span></div>
        <div class="card kpi"><span class="kpi__lbl">${t("net.pending")}</span><span class="kpi__val">${pend.length}</span></div>
        <div class="card kpi"><span class="kpi__lbl">${t("net.ibs")}</span><span class="kpi__val">${list.filter((u) => u.role === "ib").length}</span></div>
        <div class="card kpi"><span class="kpi__lbl">${t("net.net")}</span><span class="kpi__val ${cls(teamNet)}">${money(teamNet)}</span></div>
      </div>
      ${pend.length ? `<section class="card"><h3>${t("net.pendingList")} <span class="badge badge--warn">${pend.length}</span></h3>${pend.map((u) => row({ u, d: 0 })).join("")}</section>` : ""}
      <section class="card">
        <h3>${t("net.tree")} <span class="badge">${list.length}</span></h3>
        <input class="input" id="net-q" type="search" style="margin-top:12px" placeholder="${esc(t("net.search"))}" value="${esc(state.netQuery)}">
        <div id="net-list">${ordered.length ? ordered.map(row).join("") : `<p class="empty">${t("net.empty")}</p>`}</div>
      </section>`;
    const kpiGrid = $(".kpis", v); if (matchMedia("(min-width: 900px)").matches) kpiGrid.style.gridTemplateColumns = "repeat(4,1fr)";

    $$("[data-copy]", v).forEach((b) => b.addEventListener("click", async () => {
      try { await navigator.clipboard.writeText(b.dataset.copy); toast(t("app.copied")); } catch { const r = document.createRange(); const el = b.previousElementSibling; if (el) { r.selectNodeContents(el); getSelection().removeAllRanges(); getSelection().addRange(r); } }
    }));
    const q = $("#net-q", v);
    const filter = () => { state.netQuery = q.value; const s = q.value.trim().toLowerCase(); $$("#net-list .net-row", v).forEach((r) => { r.hidden = s && !r.dataset.search.includes(s); }); };
    q.addEventListener("input", filter); filter();
    $$("[data-st]", v).forEach((b) => b.addEventListener("click", async () => {
      b.disabled = true;
      try { await state.store.setMemberStatus(b.dataset.id, b.dataset.st); await reload(["downline"]); render(); } catch (err) { b.disabled = false; fail(err); }
    }));
    $$("[data-role]", v).forEach((b) => b.addEventListener("click", async () => {
      b.disabled = true;
      try { await state.store.setMemberRole(b.dataset.id, b.dataset.role); await reload(["downline"]); render(); } catch (err) { b.disabled = false; fail(err); }
    }));
  }

  // ------------------------------------------------------------ profile
  function profile(v) {
    const m = state.me;
    v.innerHTML = `
      <div class="view-head"><h2>${t("app.profile")}</h2></div>
      ${statusCard()}
      <div class="grid grid--2">
        <section class="card">
          <h3>${t("prof.title")}</h3>
          <form class="form-grid" id="prof" style="margin-top:16px">
            <label class="field"><span>${t("auth.name")}</span><input class="input" name="full_name" value="${esc(m.full_name || "")}" autocomplete="name"></label>
            <label class="field"><span>${t("auth.email")}</span><input class="input" value="${esc(m.email || "")}" disabled></label>
            <label class="field"><span>${t("auth.telegram")}</span><input class="input" name="telegram" value="${esc(m.telegram || "")}" placeholder="@"><small>${t("auth.telegram.hint")}</small></label>
            <label class="field"><span>${t("prof.lang")}</span><select class="input" name="language"><option value="th" ${I.lang === "th" ? "selected" : ""}>ไทย</option><option value="en" ${I.lang === "en" ? "selected" : ""}>English</option></select></label>
            <button class="btn btn--gold" type="submit" style="justify-self:start">${t("app.save")}</button>
          </form>
        </section>
        <section class="card">
          <h3>${t("prof.accounts")} <button class="btn btn--ghost btn--sm" type="button" id="add-acc">${t("prof.addAcc")}</button></h3>
          ${state.accounts.length ? `<div class="table-wrap"><table class="table"><thead><tr><th>${t("auth.broker")}</th><th>${t("auth.account")}</th><th class="r">${t("prof.start")}</th></tr></thead><tbody>
            ${state.accounts.map((a) => `<tr><td>${esc(brokerName(a.broker))} <span class="badge">${esc(a.platform || "MT5")}</span><br><small class="muted">${esc(a.server || "")}</small></td><td>${esc(a.account_number)}</td>
              <td class="r"><input class="input" style="max-width:130px;min-height:40px;text-align:right;display:inline-block" type="number" inputmode="decimal" data-start="${a.id}" value="${+a.start_balance || 0}" aria-label="${esc(t("prof.start"))}"></td></tr>`).join("")}
          </tbody></table></div><p class="muted" style="font-size:.82rem;margin-top:8px">${t("prof.start.hint")}</p>` : `<p class="muted" style="margin-top:12px">${t("prof.noAcc")}</p>`}
        </section>
      </div>
      ${!state.store.live ? `<section class="card"><h3>${t("prof.demoReset")}</h3><p class="card__sub">${t("prof.demoReset.d")}</p><button class="btn btn--ghost btn--sm" style="margin-top:12px" type="button" id="demo-reset">${t("prof.demoReset")}</button></section>` : ""}
      ${riskNote()}`;
    $("#prof", v).addEventListener("submit", async (e) => {
      e.preventDefault();
      let tg = e.target.telegram.value.trim(); if (tg && !tg.startsWith("@")) tg = "@" + tg;
      try {
        state.me = await state.store.updateProfile({ full_name: e.target.full_name.value.trim(), telegram: tg, language: e.target.language.value });
        if (e.target.language.value !== I.lang) I.setLang(e.target.language.value); else render();
        toast(t("app.saved"));
      } catch (err) { fail(err); }
    });
    $$("[data-start]", v).forEach((inp) => inp.addEventListener("change", async () => {
      try { await state.store.updateAccount(inp.dataset.start, { start_balance: +inp.value || 0 }); await reload(["accounts"]); toast(t("app.saved")); } catch (err) { fail(err); }
    }));
    $("#add-acc", v).addEventListener("click", () => openModal(t("prof.addAcc"), `
      <form class="form-grid form-grid--2" id="acc-form">
        <label class="field"><span>${t("auth.broker")}</span><select class="input" name="broker">${cfg.BROKERS.map((b) => `<option value="${b.id}">${b.name}</option>`).join("")}</select></label>
        <label class="field"><span>${t("auth.platform")}</span><select class="input" name="platform"><option>MT5</option><option>MT4</option></select></label>
        <label class="field span-2"><span>${t("auth.account")}</span><input class="input" name="account_number" inputmode="numeric" required><small>${t("auth.account.hint")}</small></label>
        <label class="field"><span>${t("prof.server")}</span><input class="input" name="server" placeholder="${esc(t("prof.server.ph"))}"></label>
        <label class="field"><span>${t("prof.start")}</span><input class="input" name="start_balance" type="number" inputmode="decimal" value="0"></label>
        <div id="acc-msg" class="span-2"></div>
        <div class="modal__foot span-2"><button type="button" class="btn btn--quiet" data-close>${t("app.cancel")}</button><button class="btn btn--gold" type="submit">${t("app.save")}</button></div>
      </form>`, (box) => {
      $("#acc-form", box).addEventListener("submit", async (e) => {
        e.preventDefault(); const F = e.target;
        if (!F.account_number.value.trim()) { F.account_number.setAttribute("aria-invalid", "true"); return; }
        try {
          await state.store.addAccount({ broker: F.broker.value, platform: F.platform.value, account_number: F.account_number.value.trim(), server: F.server.value.trim(), start_balance: +F.start_balance.value || 0 });
          await reload(["accounts"]); closeModal(); toast(t("app.saved")); render();
        } catch (err) { $("#acc-msg", box).innerHTML = `<p class="alert alert--err">${err.message === "account-taken" ? t("prof.taken") : esc(err.message)}</p>`; }
      });
    }));
    const dr = $("#demo-reset", v);
    if (dr) dr.addEventListener("click", async () => { await state.store.resetDemo(); location.reload(); });
  }

  // ------------------------------------------------------------ boot
  document.addEventListener("DOMContentLoaded", async () => {
    I.apply();
    $$("[data-telegram]").forEach((a) => { a.href = cfg.TELEGRAM_URL; a.target = "_blank"; a.rel = "noopener"; });
    $$("[data-lang-toggle]").forEach((b) => b.addEventListener("click", () => I.setLang(I.lang === "th" ? "en" : "th")));
    document.addEventListener("otm:lang", () => { if (state.me) render(); });
    $("#menu-btn").addEventListener("click", () => setMenu(!$("#sidebar").classList.contains("open")));
    $("#scrim").addEventListener("click", () => setMenu(false));
    $("#nav").addEventListener("click", (e) => { if (e.target.closest("a")) setMenu(false); });
    $("#modal").addEventListener("click", (e) => { if (e.target.id === "modal" || e.target.closest("[data-close]")) closeModal(); });
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") { if (!$("#modal").hidden) closeModal(); else setMenu(false); } });
    $("#view").setAttribute("tabindex", "-1");

    try {
      state.store = await window.OTMStore.init();
      state.me = await state.store.getSession();
      if (!state.me) { location.replace("login.html"); return; }
      let saved = null; try { saved = localStorage.getItem("otm_lang"); } catch { /* blocked */ }
      if (state.me.language && !saved) I.setLang(state.me.language);
      await reload(["accounts", "trades", "upline", "downline"]);
    } catch (err) {
      $("#view").innerHTML = `<p class="alert alert--err">${esc(t("app.error", { msg: err.message }))}</p>`;
      return;
    }
    $("#signout").addEventListener("click", async () => { await state.store.signOut(); location.href = "index.html"; });
    window.addEventListener("hashchange", () => { state.shown = 25; render(); window.scrollTo(0, 0); });
    render();
  });
})();
