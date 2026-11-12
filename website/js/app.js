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
    eq: "cum", cal: null, shown: 25, timer: null, netQuery: "", lb: { period: "week", type: "live" }
  };

  const ICON = {
    dashboard: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3.5" y="3.5" width="7" height="8" rx="2"/><rect x="13.5" y="3.5" width="7" height="5" rx="2"/><rect x="13.5" y="11.5" width="7" height="9" rx="2"/><rect x="3.5" y="14.5" width="7" height="6" rx="2"/></svg>',
    journal: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M6 3.5h11a1.5 1.5 0 0 1 1.5 1.5v14a1.5 1.5 0 0 1-1.5 1.5H6z"/><path d="M6 3.5v17M9.5 8h5.5M9.5 11.5h5.5"/><path d="m10 17 2-2.5 2 1.5 2.5-3"/></svg>',
    leaderboard: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M8 4h8v5a4 4 0 0 1-8 0z"/><path d="M8 6H5a3 3 0 0 0 3 4M16 6h3a3 3 0 0 1-3 4M12 13v3.5M8.5 20h7M9.5 20l.5-3.5h4l.5 3.5"/></svg>',
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
  const accName = (a) => `${brokerName(a.broker)} · ${a.account_number}${a.account_type === "demo" ? " · Demo" : ""}`;
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
    const r = [["dashboard", "app.dashboard"], ["journal", "app.journal"], ["leaderboard", "app.leaderboard"], ["tools", "app.tools"]];
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
    ({ dashboard, journal, leaderboard, tools, network, profile })[r](v);
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
  // where each market sits on the map, and its country code for the list
  const PLACES = {
    sydney: { lon: 151.21, lat: -33.87, cc: "AU", side: "left" },
    tokyo: { lon: 139.69, lat: 35.69, cc: "JP", side: "left" },
    london: { lon: -0.13, lat: 51.51, cc: "GB", side: "right" },
    newyork: { lon: -74.0, lat: 40.71, cc: "US", side: "left" }
  };
  const ICON_SUN = `<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M5.3 18.7l1.4-1.4M17.3 6.7l1.4-1.4"/></svg>`;
  const ICON_MOON = `<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg>`;
  const hhmm = (mins) => { const m = ((Math.round(mins) % 1440) + 1440) % 1440; return String(Math.floor(m / 60)).padStart(2, "0") + ":" + String(m % 60).padStart(2, "0"); };

  // where the sun is overhead right now (declination and longitude, in degrees)
  function sunNow(d) {
    const start = Date.UTC(d.getUTCFullYear(), 0, 0), day = (d.getTime() - start) / 864e5;
    const B = (2 * Math.PI * (day - 81)) / 364;
    const eot = 9.87 * Math.sin(2 * B) - 7.53 * Math.cos(B) - 1.5 * Math.sin(B); // minutes
    const utcH = d.getUTCHours() + d.getUTCMinutes() / 60 + d.getUTCSeconds() / 3600;
    const lon = (((-15 * (utcH - 12 + eot / 60)) + 540) % 360) - 180;
    const dec = 23.44 * Math.sin(B);
    return { lon, dec: Math.abs(dec) < 0.2 ? (dec < 0 ? -0.2 : 0.2) : dec };
  }

  function mapSvg(now, rows) {
    const M = window.OTM_WORLD;
    if (!M) return "";
    const X = (lon) => ((lon + 180) / 360) * M.w, Y = (lat) => ((M.top - lat) / 360) * M.w;
    const sun = sunNow(now), rad = Math.PI / 180;
    // night side: for each longitude, the latitude where the sun sets
    const pts = [];
    for (let lon = -180; lon <= 180; lon += 3) {
      const lat = Math.atan(-Math.cos((lon - sun.lon) * rad) / Math.tan(sun.dec * rad)) / rad;
      pts.push(`${X(lon).toFixed(1)},${Math.max(-20, Math.min(M.h + 20, Y(lat))).toFixed(1)}`);
    }
    const edge = sun.dec > 0 ? M.h + 20 : -20;
    const night = `M-2,${edge} L${pts.join(" L")} L${M.w + 2},${edge} Z`;
    const sx = X(sun.lon), sy = Y(sun.dec);
    const cities = rows.map((r) => {
      const pl = PLACES[r.s.id], x = X(pl.lon), y = Y(pl.lat), left = pl.side === "left";
      return `<g class="wmap__city ${r.open ? "is-open" : ""}">
          ${r.open ? `<circle class="wmap__pulse" cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="7"/>` : ""}
          <circle class="wmap__dot" cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${r.open ? 5 : 4}"/>
          <text x="${(x + (left ? -12 : 12)).toFixed(1)}" y="${(y + 5).toFixed(1)}" text-anchor="${left ? "end" : "start"}">${r.s.name}</text>
        </g>`;
    }).join("");
    return `<svg class="wmap" viewBox="0 0 ${M.w} ${M.h}" role="img" aria-label="${esc(t("dash.map"))}" preserveAspectRatio="xMidYMid slice">
        <defs>
          <filter id="wmap-soft" x="-5%" y="-10%" width="110%" height="120%"><feGaussianBlur stdDeviation="9"/></filter>
          <linearGradient id="wmap-sun" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stop-color="#F0D68C" stop-opacity="0"/><stop offset=".5" stop-color="#F0D68C" stop-opacity=".85"/><stop offset="1" stop-color="#F0D68C" stop-opacity="0"/>
          </linearGradient>
          <radialGradient id="wmap-glow"><stop offset="0" stop-color="#F6E4A6"/><stop offset=".35" stop-color="#DCB84A" stop-opacity=".55"/><stop offset="1" stop-color="#DCB84A" stop-opacity="0"/></radialGradient>
        </defs>
        <path class="wmap__land" d="${M.d}"/>
        <path class="wmap__night" d="${night}" filter="url(#wmap-soft)"/>
        <rect x="${(sx - 1).toFixed(1)}" y="0" width="2" height="${M.h}" fill="url(#wmap-sun)"/>
        <circle cx="${sx.toFixed(1)}" cy="${sy.toFixed(1)}" r="30" fill="url(#wmap-glow)"/>
        <circle cx="${sx.toFixed(1)}" cy="${sy.toFixed(1)}" r="4" fill="#FFF3CC"/>
        ${cities}
      </svg>`;
  }

  function hoursHtml() {
    const now = new Date();
    const localOff = -now.getTimezoneOffset();
    const weekend = marketClosed(now);
    const localNow = now.getHours() * 60 + now.getMinutes();
    const rows = SESSIONS.map((s) => {
      const p = tzParts(s.tz, now);
      const cur = p.h * 60 + p.m, o = s.open * 60, c = s.close * 60;
      const open = !weekend && cur >= o && cur < c;
      const until = open ? c - cur : (o - cur + 1440) % 1440;
      const startLocal = ((o - p.offset + localOff) % 1440 + 1440) % 1440;
      const len = c - o;
      const segs = startLocal + len <= 1440 ? [[startLocal, len]] : [[startLocal, 1440 - startLocal], [0, startLocal + len - 1440]];
      return { s, open, until, startLocal, len, segs };
    });
    const nOpen = rows.filter((r) => r.open).length;
    const list = rows.map((r) => `<li class="mk ${r.open ? "is-open" : ""}">
        <span class="mk__icon">${r.open ? ICON_SUN : ICON_MOON}</span>
        <span class="mk__cc">${PLACES[r.s.id].cc}</span>
        <b class="mk__name">${r.s.name}</b>
        <span class="mk__state">${weekend ? t("dash.closed") : r.open ? t("dash.closesIn", { t: dur(r.until) }) : t("dash.opensIn", { t: dur(r.until) })}</span>
        <span class="mk__track" aria-hidden="true">${r.segs.map(([a, l]) => `<i class="mk__seg" style="left:${(a / 14.4).toFixed(2)}%;width:${(l / 14.4).toFixed(2)}%"></i>`).join("")}<i class="mk__now" style="left:${(localNow / 14.4).toFixed(2)}%"></i></span>
        <span class="mk__range">${t("dash.localRange", { a: hhmm(r.startLocal), b: hhmm(r.startLocal + r.len) })}</span>
      </li>`).join("");
    return `<div class="market__head">
        <span class="market__icon"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.6 3.8 5.6 3.8 9s-1.2 6.4-3.8 9c-2.6-2.6-3.8-5.6-3.8-9S9.4 5.6 12 3z"/></svg></span>
        <div><h3>${t("dash.hours")}</h3><p class="card__sub">${t("dash.hours.local")}</p></div>
        <span class="badge ${nOpen ? "badge--gold" : ""}">${weekend ? t("dash.weekendShort") : nOpen ? t("dash.openCount", { n: nOpen }) : t("dash.allClosed")}</span>
      </div>
      <div class="market__body">
        <div class="market__map">${mapSvg(now, rows)}</div>
        <ul class="mk-list">${list}</ul>
      </div>
      ${weekend ? `<p class="muted" style="font-size:.86rem;margin:12px 0 0">${t("dash.weekend")}</p>` : ""}`;
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
      <section class="card market" id="hours">${hoursHtml()}</section>
      <div class="grid grid--21">
        <section class="card kpi--hero">
          <h3>${t("dash.month")} <a class="btn btn--ghost btn--sm" href="#journal">${t("dash.toJournal")}</a></h3>
          ${st.count ? `<div class="score" style="margin-top:6px">${C.gauge(all.score, t("j.score"))}
            <div class="stack" style="--g:0">
              <div><span class="kpi__lbl">${t("j.total")}</span><span class="kpi__val ${cls(st.total)}">${money(st.total)}</span><span class="kpi__sub">${st.count} ${t("dash.trades")}</span></div>
              <div><span class="kpi__lbl">${t("j.wr")}</span><span class="kpi__val">${fmt.num(st.winRate, 1)}%</span></div>
            </div></div>` : `<p class="muted" style="margin-top:12px">${t("dash.noData")}</p>`}
        </section>
        <section class="card">
          <h3>${t("dash.start")} <span class="badge">${t("dash.done", { n: done, m: steps.length })}</span></h3>
          <div class="progress"><i style="width:${(done / steps.length) * 100}%"></i></div>
          <ul class="checklist">${steps.map(([k, ok, href]) => `<li class="${ok ? "done" : ""}"><i class="tick"></i><span>${ok ? t(k) : `<a href="${href}">${t(k)}</a>`}</span></li>`).join("")}</ul>
        </section>
      </div>
      <div class="grid">
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
      ${syncOn() && state.accounts.length ? (() => {
        const on = state.accounts.filter((a) => a.metaapi_id);
        const last = on.map((a) => a.last_sync_at).filter(Boolean).sort().pop();
        const bad = on.find((a) => a.sync_status === "error");
        return on.length
          ? `<div class="sync-bar ${bad ? "is-err" : ""}"><span class="sync-bar__dot" aria-hidden="true"></span><div><b>${t("sync.banner.on")}</b><small>${bad ? esc(syncErrText(bad.sync_error)) : last ? t("sync.last", { t: fmt.dateTime(last) }) : t("sync.connecting")}</small></div><button class="btn btn--ghost btn--sm" type="button" id="sync-now">${t("sync.now")}</button></div>`
          : `<div class="sync-bar is-off"><span class="sync-bar__dot" aria-hidden="true"></span><div><b>${t("sync.title")}</b><small>${t("sync.banner.off")}</small></div><button class="btn btn--gold btn--sm" type="button" id="sync-connect">${t("sync.connect")}</button></div>`;
      })() : ""}
      <div class="filters">
        ${seg("period", [["today", "j.p.today"], ["week", "j.p.week"], ["month", "j.p.month"], ["year", "j.p.year"], ["all", "j.p.all"], ["custom", "j.p.custom"]])}
        ${f.period === "custom" ? `<span class="range">
          <label><span>${t("j.from")}</span><input class="input" type="date" id="f-from" value="${esc(f.from || "")}" max="${esc(f.to || "")}"></label>
          <label><span>${t("j.to")}</span><input class="input" type="date" id="f-to" value="${esc(f.to || "")}" min="${esc(f.from || "")}"></label>
        </span>` : ""}
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
      <section class="card" id="daily-card"></section>
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
      : `<section class="card empty"><h3>${t("j.empty.t")}</h3><p>${t("j.empty.d")}</p><div class="actions" style="margin-top:18px;justify-content:center">${syncOn() && state.accounts.length ? `<button class="btn btn--gold" type="button" id="btn-sync2">${t("sync.connect")}</button>` : ""}<button class="btn ${syncOn() && state.accounts.length ? "btn--ghost" : "btn--gold"}" type="button" id="btn-import2">${t("j.import")}</button></div></section>`}
      ${riskNote()}`;

    // controls
    $$("[data-f]", v).forEach((b) => b.addEventListener("click", () => {
      f[b.dataset.f] = b.dataset.v; state.shown = 25; state.daysShown = 31;
      if (b.dataset.v === "custom" && !f.from) { const d = new Date(); f.from = S.dayKey(new Date(d.getFullYear(), d.getMonth(), 1)); f.to = S.dayKey(d); }
      render();
    }));
    $$(".filters .seg", v).forEach((sg) => { const on = sg.querySelector('[aria-pressed="true"]'); if (on && sg.scrollWidth > sg.clientWidth) sg.scrollLeft = on.offsetLeft - 8; });
    const fFrom = $("#f-from", v), fTo = $("#f-to", v);
    if (fFrom) {
      const setRange = () => { f.from = fFrom.value; f.to = fTo.value; if (f.from && f.to && f.from > f.to) [f.from, f.to] = [f.to, f.from]; state.daysShown = 31; render(); };
      fFrom.addEventListener("change", setRange); fTo.addEventListener("change", setRange);
    }
    $("#acc-pick", v).addEventListener("change", (e) => { f.account = e.target.value; render(); });
    $("#sym-pick", v).addEventListener("change", (e) => { f.symbol = e.target.value; render(); });
    $("#btn-import", v).addEventListener("click", importModal);
    const sn = $("#sync-now", v); if (sn) sn.addEventListener("click", () => runSyncNow(state.accounts.filter((a) => a.metaapi_id).map((a) => a.id), sn));
    const sc = $("#sync-connect", v); if (sc) sc.addEventListener("click", () => connectModal(null));
    const i2 = $("#btn-import2", v); if (i2) i2.addEventListener("click", importModal);
    const s2 = $("#btn-sync2", v); if (s2) s2.addEventListener("click", () => connectModal(null));
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

    // daily summary: one row per trading day, newest first, with a running total
    const drawDaily = () => {
      const days = [...st.byDay.values()].sort((a, b) => a.key.localeCompare(b.key));
      let run = 0; days.forEach((g) => { run += g.net; g.cum = run; });
      const desc = days.slice().reverse(), shown = desc.slice(0, state.daysShown || 31);
      const tot = days.reduce((s, g) => ({ c: s.c + g.count, w: s.w + g.wins, l: s.l + g.losses, v: s.v + g.volume, n: s.n + g.net }), { c: 0, w: 0, l: 0, v: 0, n: 0 });
      const green = days.filter((g) => g.net > 0).length;
      $("#daily-card", v).innerHTML = `<h3>${t("j.daily")} <span class="badge">${t("j.daily.count", { n: days.length, g: green })}</span></h3>
        <p class="card__sub">${t("j.daily.sub")}</p>
        <div class="table-wrap"><table class="table table--click table--daily">
          <thead><tr><th>${t("j.col.day")}</th><th class="r">${t("j.col.trades")}</th><th class="r">${t("j.col.wl")}</th><th class="r">${t("j.col.wr")}</th><th class="r c-lot">${t("j.col.lot")}</th><th class="r">${t("j.col.net")}</th><th class="r c-cum">${t("j.col.cum")}</th></tr></thead>
          <tbody>${shown.map((g) => `<tr data-day="${g.key}" tabindex="0">
            <td>${fmt.date(g.key + "T12:00:00", { weekday: "short", day: "numeric", month: "short", year: "numeric" })}</td>
            <td class="r">${g.count}</td>
            <td class="r"><span class="up">${g.wins}</span> / <span class="down">${g.losses}</span></td>
            <td class="r">${fmt.num(g.winRate, 0)}%</td>
            <td class="r c-lot">${fmt.num(g.volume, 2)}</td>
            <td class="r ${cls(g.net)}"><b>${money(g.net)}</b></td>
            <td class="r c-cum ${cls(g.cum)}">${money(g.cum)}</td></tr>`).join("")}</tbody>
          <tfoot><tr><td>${t("j.daily.total")}</td><td class="r">${tot.c}</td><td class="r"><span class="up">${tot.w}</span> / <span class="down">${tot.l}</span></td><td class="r">${tot.c ? fmt.num((tot.w / tot.c) * 100, 0) : 0}%</td><td class="r c-lot">${fmt.num(tot.v, 2)}</td><td class="r ${cls(tot.n)}"><b>${money(tot.n)}</b></td><td class="r c-cum"></td></tr></tfoot>
        </table></div>
        ${desc.length > shown.length ? `<div style="text-align:center;margin-top:12px"><button class="btn btn--quiet" type="button" id="more-days">${t("j.more")}</button></div>` : ""}`;
      $$("#daily-card [data-day]", v).forEach((tr) => {
        const go = () => { f.period = "custom"; f.from = f.to = tr.dataset.day; state.shown = 25; render(); window.scrollTo({ top: 0, behavior: "smooth" }); };
        tr.addEventListener("click", go); tr.addEventListener("keydown", (e) => { if (e.key === "Enter") go(); });
      });
      const md = $("#more-days", v); if (md) md.addEventListener("click", () => { state.daysShown = (state.daysShown || 31) + 62; drawDaily(); });
    };
    drawDaily();

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

  // ------------------------------------------------------------ leaderboard
  const FLAME = '<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor" aria-hidden="true"><path d="M12.6 2.5c.4 3-1.4 4.6-2.8 6.1C8.4 10.1 7 11.7 7 14.3A5 5 0 0 0 12 19.5a5 5 0 0 0 5-5.2c0-2.3-1.2-3.6-2-4.6-.2 1.3-.8 2.2-1.7 2.6.6-3.6-.2-7.2-.7-9.8z"/></svg>';
  function lbParts(r) {
    const wr = r.trades ? (r.wins / r.trades) * 100 : 0;
    const pfv = r.gross_loss ? r.gross_win / r.gross_loss : (r.gross_win ? Infinity : 0);
    const avgW = r.wins ? r.gross_win / r.wins : 0, avgL = r.losses ? r.gross_loss / r.losses : 0;
    const wl = avgL ? avgW / avgL : (avgW ? Infinity : 0);
    const sc = (v, lo, hi) => Math.max(0, Math.min(100, ((v - lo) / (hi - lo)) * 100));
    const score = (sc(wr, 30, 70) + (pfv === Infinity ? 100 : sc(pfv, 1, 3)) + (wl === Infinity ? 100 : sc(wl, 0.5, 2.5))) / 3;
    const tier = r.trades < 3 ? "rookie" : score >= 75 ? "platinum" : score >= 55 ? "gold" : score >= 35 ? "silver" : "bronze";
    return { wr, pfv, wl, tier };
  }
  function lbReset(period) {
    const { end } = S.lbPeriod(period);
    if (!end) return "";
    const s = Math.max(0, Math.floor((end - Date.now()) / 1000)), d = Math.floor(s / 86400), h = Math.floor((s % 86400) / 3600), m = Math.floor((s % 3600) / 60), sec = s % 60;
    const two = (n) => String(n).padStart(2, "0");
    return t("lb.resets", { t: `${d ? d + (I.lang === "th" ? " วัน " : "d ") : ""}${h}${I.lang === "th" ? " ชม. " : "h "}${two(m)}${I.lang === "th" ? " น. " : "m "}${two(sec)}${I.lang === "th" ? " วิ" : "s"}` });
  }

  async function leaderboard(v) {
    if (!approved()) { v.innerHTML = statusCard() + riskNote(); return; }
    const L = state.lb, m = state.me;
    const seg = (key, opts) => `<div class="seg" role="group">${opts.map(([val, lbl]) => `<button type="button" data-lb="${key}" data-v="${val}" aria-pressed="${L[key] === val}">${t(lbl)}</button>`).join("")}</div>`;
    v.innerHTML = `
      <div class="view-head lb-head">
        <div class="lb-title"><span class="lb-title__icon">${ICON.leaderboard}</span>
          <div><h2>${t("app.leaderboard")}</h2><p class="muted">${t("lb.sub")}${L.period !== "all" ? ` · <span id="lb-reset" class="lb-reset">${lbReset(L.period)}</span>` : ""}</p></div></div>
        <div class="lb-controls">
          ${seg("type", [["live", "lb.live"], ["demo", "lb.demo"]])}
          ${seg("period", [["day", "lb.day"], ["week", "lb.week"], ["month", "lb.month"], ["all", "lb.all"]])}
        </div>
      </div>
      <div id="lb-body"><div class="loading"><img src="assets/img/mark.svg" alt="" width="56" height="56"></div></div>
      ${riskNote()}`;
    $$("[data-lb]", v).forEach((b) => b.addEventListener("click", () => { L[b.dataset.lb] = b.dataset.v; render(); }));
    if (L.period !== "all") state.timer = setInterval(() => { const el = $("#lb-reset"); if (el) el.textContent = lbReset(L.period); }, 1000);

    let rows;
    try { rows = await state.store.leaderboard(L.period, L.type); }
    catch (err) { $("#lb-body", v).innerHTML = `<p class="alert alert--err">${esc(err.message)}</p>`; return; }
    if (currentRoute() !== "leaderboard" || !$("#lb-body", v)) return;

    // my own numbers for this period and account type (from my journal, whether or not I joined)
    const { start } = S.lbPeriod(L.period);
    const types = new Map(state.accounts.map((a) => [a.id, a.account_type || "live"]));
    const mine = S.compute(state.trades.filter((x) => types.get(x.account_id) === L.type && (!start || new Date(x.close_time) >= start)));
    const meRow = rows.find((r) => r.is_me);
    const field = rows.length ? rows[0].field_size : 0;
    const joined = !!m.leaderboard_opt_in;
    const myName = (m.leaderboard_name || "").trim() || String(m.full_name || "").split(" ")[0];

    const avatar = (r, size = "") => `<span class="lb-av ${size}">${esc(initials(r.display_name))}</span>`;
    const podium = rows.length ? [rows[1], rows[0], rows[2]].map((r, i) => {
      if (!r) return `<div class="pod pod--empty"></div>`;
      const place = [2, 1, 3][i], P = lbParts(r);
      return `<div class="pod pod--${place} ${r.is_me ? "is-me" : ""}">
          <div class="pod__medal"><span>${place}</span></div>
          ${avatar(r, "lb-av--lg")}
          <b class="pod__name">${esc(r.display_name)}${r.is_me ? ` <span class="lb-you">${t("lb.you")}</span>` : ""}</b>
          <span class="pod__net up">${money(r.net)}</span>
          <span class="pod__meta">${fmt.num(P.wr, 0)}% WR${r.return_pct != null ? ` · ${r.return_pct >= 0 ? "+" : ""}${fmt.num(r.return_pct, 1)}%` : ""}</span>
          <div class="pod__base"><span>${place}</span></div>
        </div>`;
    }).join("") : "";

    $("#lb-body", v).innerHTML = `
      ${!joined ? `<section class="card lb-join">
          <div><h3>${t("lb.join.t")}</h3><p class="card__sub">${t("lb.join.d")}</p></div>
          <form id="lb-join" class="lb-join__form"><label class="sr-only" for="lb-name">${t("lb.name")}</label>
            <input class="input" id="lb-name" name="name" maxlength="30" value="${esc(myName)}" placeholder="${esc(t("lb.name"))}">
            <button class="btn btn--gold" type="submit">${t("lb.join")}</button></form>
        </section>` : ""}
      <div class="kpis kpis--4">
        <div class="card kpi kpi--hero"><span class="kpi__lbl">${t("lb.myRank")}</span>
          <span class="kpi__val">${meRow ? "#" + meRow.rank : t("lb.unranked")}</span>
          <span class="kpi__sub">${meRow ? t("lb.of", { n: field }) : !joined ? t("lb.notJoined") : t("lb.needProfit")}${field ? ` · ${t("lb.profitable", { n: rows.length, f: field })}` : ""}</span></div>
        <div class="card kpi"><span class="kpi__lbl">${t("j.total")}</span><span class="kpi__val ${cls(mine.total)}">${money(mine.total)}</span><span class="kpi__sub">${t("j.total.sub", { n: mine.count })}</span></div>
        <div class="card kpi"><span class="kpi__lbl">${t("j.wr")}</span><span class="kpi__val">${mine.count ? fmt.num(mine.winRate, 1) + "%" : "–"}</span><span class="kpi__sub">${t("j.wr.sub", { w: mine.wins, l: mine.losses })}</span></div>
        <div class="card kpi"><span class="kpi__lbl">${t("j.pf")}</span><span class="kpi__val">${mine.count ? pf(mine.profitFactor) : "–"}</span><span class="kpi__sub">${t("j.pf.sub")}</span></div>
      </div>
      ${rows.length ? `<section class="podium" aria-label="${esc(t("lb.top3"))}">${podium}</section>
      <section class="card">
        <h3>${t("lb.allTraders")} <span class="badge">${t("lb.count", { n: rows.length })}</span></h3>
        <div class="table-wrap"><table class="table lb-table">
          <thead><tr><th>${t("lb.col.rank")}</th><th>${t("lb.col.trader")}</th><th class="c-tier">${t("lb.col.tier")}</th><th class="r">${t("j.col.trades")}</th><th class="r">${t("lb.col.profit")}</th><th class="r c-ret">${t("lb.col.return")}</th><th class="r">${t("j.col.wr")}</th><th class="r c-pf">P.Factor</th><th class="r c-wl">${t("lb.col.wl")}</th><th class="r">${t("lb.col.streak")}</th></tr></thead>
          <tbody>${rows.map((r) => { const P = lbParts(r); return `<tr class="lb-row ${r.rank <= 3 ? "lb-row--" + r.rank : ""} ${r.is_me ? "is-me" : ""}">
            <td class="lb-rank">${r.rank <= 3 ? `<span class="lb-medal lb-medal--${r.rank}">${r.rank}</span>` : String(r.rank).padStart(2, "0")}</td>
            <td><span class="lb-who">${avatar(r)}<b>${esc(r.display_name)}</b>${r.is_me ? `<span class="lb-you">${t("lb.you")}</span>` : ""}</span></td>
            <td class="c-tier"><span class="tier tier--${P.tier}">${t("lb.tier." + P.tier)}</span></td>
            <td class="r">${r.trades}</td>
            <td class="r up"><b>${money(r.net)}</b></td>
            <td class="r c-ret">${r.return_pct != null ? `${r.return_pct >= 0 ? "+" : ""}${fmt.num(r.return_pct, 1)}%` : "–"}</td>
            <td class="r">${fmt.num(P.wr, 1)}%</td>
            <td class="r c-pf">${pf(P.pfv)}</td>
            <td class="r c-wl">${P.wl === Infinity ? "∞" : fmt.num(P.wl, 2)}</td>
            <td class="r"><span class="lb-streak">${r.streak ? FLAME + r.streak : "–"}</span></td></tr>`; }).join("")}</tbody>
        </table></div>
      </section>` : `<section class="card empty"><h3>${t("lb.empty.t")}</h3><p>${t("lb.empty.d")}</p></section>`}
      <p class="muted lb-foot">${t("lb.foot")}</p>
      ${joined ? `<section class="card lb-me">
          <form id="lb-rename" class="lb-join__form"><label class="field" style="flex:1;min-width:180px"><span>${t("lb.name")}</span><input class="input" name="name" maxlength="30" value="${esc(myName)}"></label>
            <button class="btn btn--ghost" type="submit">${t("app.save")}</button>
            <button class="btn btn--quiet" type="button" id="lb-leave">${t("lb.leave")}</button></form>
        </section>` : ""}`;

    const saveLb = async (f, msg) => {
      try { state.me = await state.store.updateProfile(f); toast(msg); render(); } catch (err) { fail(err); }
    };
    const jf = $("#lb-join", v);
    if (jf) jf.addEventListener("submit", (e) => { e.preventDefault(); saveLb({ leaderboard_opt_in: true, leaderboard_name: jf.name.value.trim().slice(0, 30) }, t("lb.joined")); });
    const rf = $("#lb-rename", v);
    if (rf) rf.addEventListener("submit", (e) => { e.preventDefault(); saveLb({ leaderboard_name: rf.name.value.trim().slice(0, 30) }, t("app.saved")); });
    const lv = $("#lb-leave", v);
    if (lv) lv.addEventListener("click", () => {
      if (!lv.dataset.armed) { lv.dataset.armed = "1"; lv.textContent = t("lb.leaveConfirm"); return; }
      saveLb({ leaderboard_opt_in: false }, t("lb.left"));
    });
  }

  // ------------------------------------------------------------ automatic history (MT4/MT5)
  const syncOn = () => cfg.AUTO_SYNC !== false;
  const syncErrText = (code) => {
    const c = String(code || "").split(":")[0].trim();
    return ["bad-login", "bad-server", "password-change", "account-disabled", "slow", "not-configured", "missing"].includes(c) ? t("sync.err." + c) : t("sync.err.generic", { msg: c || "?" });
  };
  function syncChip(a) {
    const s = a.sync_status || "off";
    const cls = s === "ok" ? "badge--ok" : s === "error" ? "badge--err" : s === "connecting" ? "badge--warn" : "";
    return `<span class="badge ${cls}">${t("sync." + s)}</span>`;
  }
  function syncLine(a) {
    if (a.sync_status === "error") return `<small class="sync-err">${esc(syncErrText(a.sync_error))}</small>`;
    if (a.last_sync_at) return `<small class="muted">${t("sync.last", { t: fmt.dateTime(a.last_sync_at) })}</small>`;
    return "";
  }
  async function runSyncNow(ids, btn) {
    if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = t("sync.running"); }
    let added = 0, err = null;
    for (const id of ids) { try { added += (await state.store.syncNow(id)).added || 0; } catch (e) { err = e; } }
    await reload(["accounts", "trades"]);
    if (err) toast(syncErrText(err.message)); else toast(added ? t("sync.done", { n: added }) : t("sync.nothingNew"));
    render();
  }
  function connectModal(acc) {
    const choices = state.accounts.filter((a) => !a.metaapi_id);
    const pick = acc || choices[0] || state.accounts[0];
    if (!pick) { location.hash = "#profile"; return; }
    openModal(t("sync.modal.title"), `
      <form class="form-grid" id="sync-form" novalidate>
        <p class="muted" style="margin:0">${t("sync.modal.lead")}</p>
        ${acc ? `<p class="sync-acc"><b>${esc(accName(acc))}</b> <span class="badge">${esc(acc.platform || "MT5")}</span></p>`
              : `<label class="field"><span>${t("sync.account")}</span><select class="input" name="acc">${state.accounts.map((a) => `<option value="${a.id}" ${a.id === pick.id ? "selected" : ""}>${esc(accName(a))}</option>`).join("")}</select></label>`}
        <label class="field"><span>${t("sync.server")}</span><input class="input" name="server" value="${esc(pick.server || "")}" autocomplete="off" spellcheck="false" required><small>${t("sync.server.hint")}</small></label>
        <label class="field"><span>${t("sync.password")}</span><input class="input" name="password" type="password" autocomplete="off" required><small>${t("sync.password.hint")}</small></label>
        <p class="alert alert--gold" style="margin:0">${t("sync.master.warn")}</p>
        <label class="check"><input type="checkbox" name="agree"><span>${t("sync.agree")}</span></label>
        <p class="muted" style="font-size:.82rem;margin:0">${state.store.live ? t("sync.privacy") : t("sync.demoHint")}</p>
        <div id="sync-msg"></div>
        <div class="modal__foot"><button type="button" class="btn btn--quiet" data-close>${t("app.cancel")}</button><button class="btn btn--gold" type="submit">${t("sync.submit")}</button></div>
      </form>`, (box) => {
      const F = $("#sync-form", box), msg = $("#sync-msg", box);
      if (F.acc) F.acc.addEventListener("change", () => { const a = state.accounts.find((x) => x.id === F.acc.value); F.server.value = (a && a.server) || ""; });
      F.addEventListener("submit", async (e) => {
        e.preventDefault();
        const id = acc ? acc.id : F.acc.value;
        F.server.setAttribute("aria-invalid", F.server.value.trim() ? "false" : "true");
        F.password.setAttribute("aria-invalid", F.password.value ? "false" : "true");
        if (!F.server.value.trim() || !F.password.value) { msg.innerHTML = `<p class="alert alert--err">${t("auth.err.required")}</p>`; return; }
        if (!F.agree.checked) { msg.innerHTML = `<p class="alert alert--err">${t("sync.err.agree")}</p>`; return; }
        const btn = $("button[type=submit]", F); btn.disabled = true;
        msg.innerHTML = `<p class="alert alert--gold"><span class="spin" aria-hidden="true"></span> ${t("sync.working")}</p>`;
        try {
          const r = await state.store.syncConnect(id, F.server.value.trim(), F.password.value);
          F.password.value = "";
          await reload(["accounts", "trades"]); closeModal();
          toast(r && r.status === "ok" ? t("sync.done", { n: r.added || 0 }) : t("sync.pending"));
          render();
        } catch (err) {
          btn.disabled = false; F.password.value = "";
          msg.innerHTML = `<p class="alert alert--err">${esc(syncErrText(err.message))}</p>`;
          await reload(["accounts"]);
        }
      });
    });
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
          ${state.accounts.length ? `<div class="table-wrap"><table class="table"><thead><tr><th>${t("auth.broker")}</th><th>${t("auth.account")}</th><th class="r">${t("prof.start")}</th><th></th></tr></thead><tbody>
            ${state.accounts.map((a) => `<tr><td>${esc(brokerName(a.broker))} <span class="badge">${esc(a.platform || "MT5")}</span>${a.account_type === "demo" ? ` <span class="badge badge--warn">Demo</span>` : ""}<br><small class="muted">${esc(a.server || "")}</small></td><td>${esc(a.account_number)}</td>
              <td class="r"><input class="input" style="max-width:130px;min-height:40px;text-align:right;display:inline-block" type="number" inputmode="decimal" data-start="${a.id}" value="${+a.start_balance || 0}" aria-label="${esc(t("prof.start"))}"></td>
              <td class="r"><button class="btn btn--danger btn--sm" type="button" data-del-acc="${a.id}">${t("prof.removeAcc")}</button></td></tr>`).join("")}
          </tbody></table></div><p class="muted" style="font-size:.82rem;margin-top:8px">${t("prof.start.hint")}</p>` : `<p class="muted" style="margin-top:12px">${t("prof.noAcc")}</p>`}
        </section>
      </div>
      ${syncOn() && state.accounts.length ? `<section class="card">
        <h3>${t("sync.title")}</h3><p class="card__sub">${t("sync.sub")}</p>
        <ul class="sync-list">${state.accounts.map((a) => `<li>
          <div class="sync-list__who"><b>${esc(accName(a))}</b> ${syncChip(a)}${syncLine(a)}</div>
          <div class="sync-list__act">${a.metaapi_id
            ? `<button class="btn btn--ghost btn--sm" type="button" data-sync-now="${a.id}">${t("sync.now")}</button><button class="btn btn--quiet btn--sm" type="button" data-sync-off="${a.id}">${t("sync.disconnect")}</button>`
            : `<button class="btn btn--gold btn--sm" type="button" data-sync-connect="${a.id}">${t("sync.connect")}</button>`}</div>
        </li>`).join("")}</ul>
      </section>` : ""}
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
    $$("[data-del-acc]", v).forEach((b) => b.addEventListener("click", async () => {
      if (!b.dataset.armed) { b.dataset.armed = "1"; b.textContent = t("prof.removeConfirm"); return; }
      b.disabled = true;
      try {
        await state.store.deleteAccount(b.dataset.delAcc);
        if (state.f.account === b.dataset.delAcc) state.f.account = "all";
        await reload(["accounts", "trades"]); toast(t("prof.removed")); render();
      } catch (err) { b.disabled = false; fail(err); }
    }));
    $("#add-acc", v).addEventListener("click", () => openModal(t("prof.addAcc"), `
      <form class="form-grid form-grid--2" id="acc-form">
        <label class="field"><span>${t("auth.broker")}</span><select class="input" name="broker">${cfg.BROKERS.map((b) => `<option value="${b.id}">${b.name}</option>`).join("")}</select></label>
        <label class="field"><span>${t("auth.platform")}</span><select class="input" name="platform"><option>MT5</option><option>MT4</option></select></label>
        <label class="field span-2"><span>${t("prof.type")}</span><select class="input" name="account_type"><option value="live">${t("lb.live")}</option><option value="demo">${t("lb.demo")}</option></select><small>${t("prof.type.hint")}</small></label>
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
          await state.store.addAccount({ broker: F.broker.value, platform: F.platform.value, account_type: F.account_type.value, account_number: F.account_number.value.trim(), server: F.server.value.trim(), start_balance: +F.start_balance.value || 0 });
          await reload(["accounts"]); closeModal(); toast(t("app.saved")); render();
        } catch (err) { $("#acc-msg", box).innerHTML = `<p class="alert alert--err">${err.message === "account-taken" ? t("prof.taken") : esc(err.message)}</p>`; }
      });
    }));
    $$("[data-sync-connect]", v).forEach((b) => b.addEventListener("click", () => connectModal(state.accounts.find((a) => a.id === b.dataset.syncConnect))));
    $$("[data-sync-now]", v).forEach((b) => b.addEventListener("click", () => runSyncNow([b.dataset.syncNow], b)));
    $$("[data-sync-off]", v).forEach((b) => b.addEventListener("click", async () => {
      if (!b.dataset.armed) { b.dataset.armed = "1"; b.textContent = t("sync.disconnectConfirm"); return; }
      b.disabled = true;
      try { await state.store.syncDisconnect(b.dataset.syncOff); await reload(["accounts"]); toast(t("sync.disconnected")); render(); }
      catch (err) { b.disabled = false; toast(syncErrText(err.message)); }
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
