// Broker IB reports on the IB Network page. An IB drops the report files from the broker's IB portal
// (several at once, any order, overlapping dates are fine); they are read in the browser, stored for that
// IB, and shown as totals, monthly charts, a client table and a sub-IB table. Members whose broker
// client ID appears in a report are confirmed automatically.
//
// Supported now: Vantage (ib_report = fund report + opened accounts, rebate_report by day or by client,
// Sub_IB_Report by IB or by day). Each table is replaced day by day: a newer file's days replace the
// stored rows for those days, so re-uploading or overlapping ranges never double count.
(function (root) {
  const I = root.OTMI18n, C = root.OTMCharts, cfg = root.OTM_CONFIG;
  const t = (k, v) => I.t(k, v);
  const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const num = (v, d = 0) => Number(v || 0).toLocaleString("en-US", { minimumFractionDigits: d, maximumFractionDigits: d });
  const usd = (v, d = 0) => (v < 0 ? "−$" : "$") + num(Math.abs(v), d);
  const n = (v) => (v === "***" || v == null || v === "" ? 0 : +v || 0);
  const TABLES = ["fund", "accounts", "rclient", "rinstr", "rdaily", "subib", "subdaily"];
  const DAY_TABLES = ["fund", "rclient", "rinstr", "rdaily", "subdaily"];

  // ---------------------------------------------------------------- reading files
  function day(v) {
    if (v == null) return null;
    if (typeof v === "number") return new Date(Math.round((v - 25569) * 864e5)).toISOString().slice(0, 10); // Excel serial
    const s = String(v).trim();
    let m = s.match(/^(\d{4})-(\d{2})-(\d{2})/); if (m) return `${m[1]}-${m[2]}-${m[3]}`;
    m = s.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})/); if (m) return `${m[3]}-${m[2].padStart(2, "0")}-${m[1].padStart(2, "0")}`;
    return null;
  }
  const idx = (hdr) => { const o = {}; hdr.forEach((h, i) => { o[String(h || "").trim()] = i; }); return o; };
  const empty = () => Object.fromEntries(TABLES.map((k) => [k, []]));
  const instr = (s) => String(s || "").replace(/[._-](s|std|ecn|pro|m|raw)$/i, "").toUpperCase();

  // one workbook -> { kind, batch } or null when the file isn't a supported report
  function parseWorkbook(sheets, fileName) {
    const B = "vantage", out = empty(), names = Object.keys(sheets);
    const first = (sh) => (sheets[sh] || [])[0] || [];
    // ib_report: fund report + opened accounts
    if (sheets["fund report"] || sheets["opened accounts"]) {
      const f = sheets["fund report"] || [], h = idx(f[0] || []), agg = new Map();
      for (const r of f.slice(1)) {
        const d = day(r[h["Date"]]); if (!d) continue;
        const k = [d, r[h["User ID"]], r[h["Account"]]].join("|"), g = agg.get(k) || { broker: B, day: d, user_id: String(r[h["User ID"]]), account: String(r[h["Account"]]), deposits: 0, withdraw: 0 };
        g.deposits += n(r[h["Deposits"]]); g.withdraw += n(r[h["Withdraw"]]); agg.set(k, g);
      }
      out.fund = [...agg.values()];
      const o = sheets["opened accounts"] || [], ho = idx(o[0] || []);
      out.accounts = o.slice(1).filter((r) => r[ho["Account"]] != null).map((r) => ({ broker: B, account: String(r[ho["Account"]]), user_id: String(r[ho["User ID"]]),
        name: r[ho["Name"]] || "", opened_on: day(r[ho["Date"]]), account_type: r[ho["Account Type"]] || "", balance: n(r[ho["Available Balance"]]) }));
      return { kind: "ib", batch: out };
    }
    // rebate_report by client (two sheets: per account, and per account per day per instrument)
    if (sheets["account rebate"]) {
      const a = sheets["account rebate"], h = idx(a[0]), cl = new Map(), ins = new Map(), dl = new Map();
      for (const r of a.slice(1)) {
        const d = day(r[h["Date"]]); if (!d) continue;
        const lots = n(r[h["Total Volume"]]), nv = n(r[h["Notional ValueUSD"]]), rb = n(r[h["Rebate(USD)"]]), u = String(r[h["User ID"]]);
        const kc = d + "|" + u, c = cl.get(kc) || { broker: B, day: d, user_id: u, name: r[h["Name"]] || "", lots: 0, notional: 0, rebate: 0 };
        c.lots += lots; c.notional += nv; c.rebate += rb; cl.set(kc, c);
        const s = instr(r[h["Instrument"]]), ki = d + "|" + s, x = ins.get(ki) || { broker: B, day: d, instrument: s, lots: 0, rebate: 0 };
        x.lots += lots; x.rebate += rb; ins.set(ki, x);
      }
      // this file's dates run one day behind the "by day" report (broker server time), so it never writes the daily totals
      Object.assign(out, { rclient: [...cl.values()], rinstr: [...ins.values()] });
      return { kind: "rebateClient", batch: out };
    }
    const h0 = first(names[0]).map((x) => String(x || "").trim());
    // rebate_report by day
    if (h0[0] === "Day" && h0[1] === "Notional Value") {
      out.rdaily = sheets[names[0]].slice(1).map((r) => ({ broker: B, day: day(r[0]), notional: n(r[1]), rebate: n(r[2]) })).filter((r) => r.day);
      return { kind: "rebateDay", batch: out };
    }
    // Sub_IB_Report by IB (no dates inside: the period comes from the file name)
    if (h0[0] === "Aff ID") {
      const p = String(fileName || "").match(/(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})/);
      if (!p) return { kind: "subibNoDate", batch: out };
      const s = sheets[names[0]], h = idx(s[0]);
      out.subib = s.slice(1).filter((r) => r[h["Aff ID"]] != null).map((r) => ({ broker: B, aff_id: String(r[h["Aff ID"]]), period_from: p[1], period_to: p[2],
        user_id: String(r[h["User ID"]] ?? ""), name: r[h["Name"]] || "", country: r[h["Country"]] || "", join_date: day(r[h["Join Date"]]),
        registration: n(r[h["Registration"]]), opened: n(r[h["Opened Account"]]), ftd: n(r[h["FTD"]]), gross_dep: n(r[h["Gross Deposits (USD)"]]),
        withdrawals: n(r[h["Withdrawals (USD)"]]), net_dep: n(r[h["Net Deposit (USD)"]]), lots: n(r[h["Volume (Lots)"]]), nv: n(r[h["Volume (NV) (USD)"]]) }));
      return { kind: "subib", batch: out };
    }
    // Sub_IB_Report by day
    if (h0[0] === "Day" && h0.includes("Gross Deposit (USD)")) {
      const s = sheets[names[0]], h = idx(s[0]), agg = new Map();
      for (const r of s.slice(1)) { const d = day(r[h["Day"]]); if (!d) continue; const g = agg.get(d) || { broker: B, day: d, gross_dep: 0, net_dep: 0 }; g.gross_dep += n(r[h["Gross Deposit (USD)"]]); g.net_dep += n(r[h["Net Deposit (USD)"]]); agg.set(d, g); }
      out.subdaily = [...agg.values()];
      return { kind: "subDay", batch: out };
    }
    return null;
  }

  // apply a batch onto stored data (same rules as the database version in store.js)
  function apply(data, batch) {
    const D = { ...empty(), ...(data || {}) };
    for (const k of DAY_TABLES) {
      if (!batch[k] || !batch[k].length) continue;
      const days = new Set(batch[k].map((r) => r.broker + "|" + r.day));
      D[k] = D[k].filter((r) => !days.has(r.broker + "|" + r.day)).concat(batch[k]);
    }
    if (batch.accounts && batch.accounts.length) {
      const m = new Map(D.accounts.map((r) => [r.broker + "|" + r.account, r]));
      batch.accounts.forEach((r) => m.set(r.broker + "|" + r.account, r)); D.accounts = [...m.values()];
    }
    if (batch.subib && batch.subib.length) {
      const P = batch.subib[0], key = (r) => r.broker + "|" + r.period_from + "|" + r.period_to;
      const inside = D.subib.some((r) => r.broker === P.broker && r.period_from <= P.period_from && r.period_to >= P.period_to && key(r) !== key(P));
      if (!inside) D.subib = D.subib.filter((r) => !(r.broker === P.broker && r.period_from >= P.period_from && r.period_to <= P.period_to)).concat(batch.subib);
    }
    return D;
  }

  async function readFiles(files) {
    const report = { ok: [], skipped: [] }; let batch = empty();
    for (const f of files) {
      try {
        const res = parseWorkbook(await root.OTMXlsx.read(f), f.name);
        if (!res || res.kind === "subibNoDate") { report.skipped.push(f.name); continue; }
        batch = apply(batch, res.batch); report.ok.push({ name: f.name, kind: res.kind });
      } catch (e) { report.skipped.push(f.name); }
    }
    return { batch, report };
  }

  // ---------------------------------------------------------------- numbers
  const month = (d) => d.slice(0, 7);
  function summary(D, links) {
    const fund = D.fund || [], rc = D.rclient || [], rd = D.rdaily || [];
    const dep = fund.reduce((s, r) => s + r.deposits, 0), wd = fund.reduce((s, r) => s + r.withdraw, 0);
    // totals come from the "by day" report; with only the "by client" files, from those instead
    const src = rd.length ? rd : rc;
    const rebate = src.reduce((s, r) => s + r.rebate, 0), notional = src.reduce((s, r) => s + r.notional, 0), lots = rc.reduce((s, r) => s + r.lots, 0);
    const nowM = new Date().toISOString().slice(0, 7);
    const months = new Map(), mk = (m) => { if (!months.has(m)) months.set(m, { m, net: 0, rebate: 0, opened: 0 }); return months.get(m); };
    fund.forEach((r) => { mk(month(r.day)).net += r.deposits - r.withdraw; });
    src.forEach((r) => { mk(month(r.day)).rebate += r.rebate; });
    (D.accounts || []).forEach((r) => { if (r.opened_on) mk(month(r.opened_on)).opened++; });
    // clients: everyone seen in any report
    const cl = new Map(), c = (b, u) => { const k = b + "|" + u; if (!cl.has(k)) cl.set(k, { broker: b, user_id: u, name: "", accounts: new Set(), dep: 0, wd: 0, lots: 0, rebate: 0 }); return cl.get(k); };
    fund.forEach((r) => { const x = c(r.broker, r.user_id); x.dep += r.deposits; x.wd += r.withdraw; x.accounts.add(r.account); });
    (D.accounts || []).forEach((r) => { const x = c(r.broker, r.user_id); x.accounts.add(r.account); if (r.name) x.name = r.name; });
    rc.forEach((r) => { const x = c(r.broker, r.user_id); x.lots += r.lots; x.rebate += r.rebate; if (r.name && !x.name) x.name = r.name; });
    const byLink = new Map((links || []).map((l) => [l.broker + "|" + String(l.client_id).trim(), l]));
    const clients = [...cl.values()].map((x) => ({ ...x, accounts: x.accounts.size, net: x.dep - x.wd, link: byLink.get(x.broker + "|" + x.user_id) || null }));
    const ins = new Map(); (D.rinstr || []).forEach((r) => { const g = ins.get(r.instrument) || { instrument: r.instrument, lots: 0, rebate: 0 }; g.lots += r.lots; g.rebate += r.rebate; ins.set(r.instrument, g); });
    const sub = new Map(); (D.subib || []).forEach((r) => {
      const g = sub.get(r.broker + "|" + r.aff_id) || { aff_id: r.aff_id, name: r.name, country: r.country, join_date: r.join_date, registration: 0, opened: 0, ftd: 0, gross_dep: 0, net_dep: 0, lots: 0 };
      ["registration", "opened", "ftd", "gross_dep", "net_dep", "lots"].forEach((k) => { g[k] += r[k]; }); sub.set(r.broker + "|" + r.aff_id, g);
    });
    const days = [...fund.map((r) => r.day), ...rd.map((r) => r.day)].sort();
    return {
      dep, wd, net: dep - wd, rebate, notional, lots, opened: (D.accounts || []).length,
      active: new Set(fund.map((r) => r.broker + "|" + r.user_id)).size,
      rebateMonth: src.filter((r) => month(r.day) === nowM).reduce((s, r) => s + r.rebate, 0),
      months: [...months.values()].sort((a, b) => a.m.localeCompare(b.m)),
      clients, instruments: [...ins.values()].sort((a, b) => b.rebate - a.rebate),
      subibs: [...sub.values()].sort((a, b) => b.lots - a.lots || b.net_dep - a.net_dep),
      subNet: (D.subdaily || []).reduce((s, r) => s + r.net_dep, 0),
      from: days[0] || null, to: days[days.length - 1] || null
    };
  }

  // ---------------------------------------------------------------- page section
  function render(el, ctx) {
    let data = null, sortBy = "rebate", showAll = false, note = "";
    const mLabel = (m) => new Date(m + "-15T12:00:00").toLocaleDateString(I.lang === "th" ? "th-TH" : "en-GB", { month: "short" });
    const bars = (rows, key, fmtv) => C && rows.length ? C.bars(rows.map((g) => ({ label: mLabel(g.m), value: g[key], sub: "" })),
      { fmt: fmtv, short: (x) => (Math.abs(x) >= 1000 ? (x < 0 ? "−" : "") + num(Math.abs(x) / 1000, 1) + "k" : num(x)), label: "", w: 420, h: 210 }) : `<p class="muted">${t("ibr.none")}</p>`;
    const status = (c) => !c.link ? `<span class="ibr-st ibr-st--no">${t("ibr.st.no")}</span>`
      : c.link.status === "verified" ? `<span class="ibr-st ibr-st--ok">✓ ${t("ibr.st.ok")}</span>`
      : c.link.status === "rejected" ? `<span class="ibr-st ibr-st--no">${t("ibr.st.rej")}</span>` : `<span class="ibr-st ibr-st--new">${t("ibr.st.pend")}</span>`;

    const draw = () => {
      const S = data ? summary(data, ctx.links()) : null, has = S && (S.clients.length || S.rebate || S.subibs.length);
      const list = has ? S.clients.slice().sort((a, b) => (b[sortBy] || 0) - (a[sortBy] || 0)) : [];
      const shown = showAll ? list : list.slice(0, 25);
      const memberName = (c) => { const u = c.link && ctx.people().get(c.link.user_id); return u ? u.full_name : ""; };
      el.innerHTML = `
        <section class="card ibr-imp">
          <div><h3>${t("ibr.title")}</h3><p class="card__sub">${t("ibr.lead")}</p>
            ${S && S.from ? `<p class="ibr-range">${t("ibr.range", { a: S.from, b: S.to })}</p>` : ""}</div>
          <label class="ibr-drop" tabindex="0">
            <input type="file" accept=".xlsx" multiple hidden>
            <b>⤓ ${t("ibr.drop")}</b><small>${t("ibr.drop.d")}</small>
          </label>
          ${note ? `<div class="ibr-note">${note}</div>` : ""}
        </section>
        ${has ? `
        <div class="ibr-kpis">
          <div class="card"><span>${t("ibr.k.dep")}</span><b class="up">${usd(S.dep)}</b></div>
          <div class="card"><span>${t("ibr.k.wd")}</span><b class="down">${usd(-S.wd)}</b></div>
          <div class="card"><span>${t("ibr.k.net")}</span><b class="gold">${usd(S.net)}</b></div>
          <div class="card"><span>${t("ibr.k.opened")}</span><b>${num(S.opened)}</b></div>
          <div class="card"><span>${t("ibr.k.rebate")}</span><b class="gold">${usd(S.rebate, 2)}</b></div>
          <div class="card"><span>${t("ibr.k.lots")}</span><b>${num(S.lots, 2)}</b></div>
          <div class="card"><span>${t("ibr.k.volume")}</span><b>$${num(S.notional / 1e6, 1)}M</b></div>
          <div class="card"><span>${t("ibr.k.month")}</span><b class="gold">${usd(S.rebateMonth, 2)}</b></div>
        </div>
        <div class="ibr-charts">
          <section class="card"><h3>${t("ibr.c.net")}</h3>${bars(S.months, "net", (x) => usd(x))}</section>
          <section class="card"><h3>${t("ibr.c.rebate")}</h3>${bars(S.months, "rebate", (x) => usd(x, 2))}</section>
          <section class="card"><h3>${t("ibr.c.opened")}</h3>${bars(S.months, "opened", (x) => num(x))}</section>
        </div>
        ${S.instruments.length ? `<section class="card"><h3>${t("ibr.instr")}</h3><ul class="ibr-ins">${S.instruments.slice(0, 8).map((x) => `<li><b>${esc(x.instrument)}</b>
          <span class="ibr-ins__bar"><i style="width:${(x.rebate / Math.max(1, S.instruments[0].rebate)) * 100}%"></i></span><span>${usd(x.rebate, 2)} · ${num(x.lots, 2)} lot</span></li>`).join("")}</ul></section>` : ""}
        <section class="card">
          <h3>${t("ibr.clients", { n: list.length })}
            <span class="ibr-tools"><select class="input" data-sort>${["rebate", "lots", "net", "dep"].map((k) => `<option value="${k}" ${k === sortBy ? "selected" : ""}>${t("ibr.sort." + k)}</option>`).join("")}</select>
            <button class="btn btn--ghost btn--sm" type="button" data-csv>${t("ibr.csv")}</button></span></h3>
          <div class="table-wrap"><table class="table ibr-table"><thead><tr><th>${t("ibr.col.client")}</th><th>User ID</th><th class="r">${t("ibr.col.acc")}</th><th class="r">${t("ibr.col.dep")}</th>
            <th class="r">${t("ibr.col.wd")}</th><th class="r">${t("ibr.col.net")}</th><th class="r">Lot</th><th class="r">${t("ibr.col.rebate")}</th><th>${t("ibr.col.st")}</th></tr></thead>
            <tbody>${shown.map((c) => `<tr><td>${esc(c.name || memberName(c) || "–")}${memberName(c) && c.name && memberName(c) !== c.name ? `<small class="muted"> · ${esc(memberName(c))}</small>` : ""}</td><td>${esc(c.user_id)}</td>
              <td class="r">${c.accounts}</td><td class="r">${usd(c.dep)}</td><td class="r ${c.wd ? "down" : ""}">${c.wd ? usd(-c.wd) : "$0"}</td>
              <td class="r ${c.net >= 0 ? "up" : "down"}">${usd(c.net)}</td><td class="r">${num(c.lots, 2)}</td><td class="r gold">${usd(c.rebate, 2)}</td><td>${status(c)}</td></tr>`).join("")}</tbody></table></div>
          ${list.length > 25 ? `<button class="btn btn--quiet btn--sm" type="button" data-all style="margin-top:12px">${t(showAll ? "ibr.less" : "ibr.all", { n: list.length })}</button>` : ""}
        </section>
        ${S.subibs.length ? `<section class="card"><h3>${t("ibr.sub", { n: S.subibs.length })}</h3>
          <div class="table-wrap"><table class="table ibr-table"><thead><tr><th>Sub-IB</th><th>Aff ID</th><th class="r">${t("ibr.col.reg")}</th><th class="r">${t("ibr.col.opened")}</th>
          <th class="r">FTD</th><th class="r">${t("ibr.col.dep")}</th><th class="r">${t("ibr.col.net")}</th><th class="r">Lot</th></tr></thead>
          <tbody>${S.subibs.map((s) => `<tr><td>${esc(s.name)}<small class="muted"> · ${esc(s.country)}</small></td><td>${esc(s.aff_id)}</td><td class="r">${num(s.registration)}</td><td class="r">${num(s.opened)}</td>
            <td class="r">${num(s.ftd)}</td><td class="r">${usd(s.gross_dep)}</td><td class="r ${s.net_dep >= 0 ? "up" : "down"}">${usd(s.net_dep)}</td><td class="r">${num(s.lots, 2)}</td></tr>`).join("")}</tbody></table></div></section>` : ""}
        ` : data ? `<p class="muted">${t("ibr.empty")}</p>` : `<p class="muted">${t("ibr.loading")}</p>`}`;
      wire();
    };

    const wire = () => {
      const inp = el.querySelector("input[type=file]"), drop = el.querySelector(".ibr-drop");
      inp.addEventListener("change", () => upload([...inp.files]));
      drop.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); inp.click(); } });
      ["dragenter", "dragover"].forEach((ev) => drop.addEventListener(ev, (e) => { e.preventDefault(); drop.classList.add("is-over"); }));
      ["dragleave", "drop"].forEach((ev) => drop.addEventListener(ev, (e) => { e.preventDefault(); drop.classList.remove("is-over"); }));
      drop.addEventListener("drop", (e) => upload([...e.dataTransfer.files].filter((f) => /\.xlsx$/i.test(f.name))));
      const s = el.querySelector("[data-sort]"); if (s) s.addEventListener("change", () => { sortBy = s.value; draw(); });
      const a = el.querySelector("[data-all]"); if (a) a.addEventListener("click", () => { showAll = !showAll; draw(); });
      const c = el.querySelector("[data-csv]"); if (c) c.addEventListener("click", csv);
    };

    async function upload(files) {
      if (!files.length) return;
      note = t("ibr.reading", { n: files.length }); draw();
      try {
        const { batch, report } = await readFiles(files);
        if (!report.ok.length) { note = `<b class="down">${t("ibr.bad")}</b> ${esc(report.skipped.join(", "))}`; draw(); return; }
        data = await ctx.store.ibSave(batch);
        const done = await autoConfirm();
        const rows = DAY_TABLES.concat(["accounts", "subib"]).reduce((s, k) => s + (batch[k] || []).length, 0);
        note = `✅ <b>${t("ibr.done", { f: report.ok.length, r: num(rows) })}</b>${done ? " · " + t("ibr.confirmed", { n: done }) : ""}${report.skipped.length ? `<br><span class="muted">${t("ibr.skip")} ${esc(report.skipped.join(", "))}</span>` : ""}`;
      } catch (e) { note = `<b class="down">${t("app.error", { msg: e.message })}</b>`; }
      draw();
    }

    // members whose pending broker ID shows up in a report get confirmed
    async function autoConfirm() {
      if (!data) return 0;
      const ids = new Set([...(data.fund || []), ...(data.accounts || []), ...(data.rclient || [])].map((r) => r.broker + "|" + r.user_id));
      const todo = (ctx.links() || []).filter((l) => l.status === "pending" && ids.has(l.broker + "|" + String(l.client_id).trim()));
      let n = 0;
      for (const l of todo) { try { await ctx.store.setLinkStatus(l.id, "verified"); l.status = "verified"; n++; } catch (e) { /* not allowed for this member */ } }
      if (n && ctx.onConfirm) ctx.onConfirm();
      return n;
    }

    function csv() {
      const S = summary(data, ctx.links());
      const rows = [["client", "user_id", "accounts", "deposits", "withdrawals", "net", "lots", "rebate", "portal_status"]].concat(
        S.clients.map((c) => [c.name, c.user_id, c.accounts, c.dep.toFixed(2), c.wd.toFixed(2), c.net.toFixed(2), c.lots.toFixed(2), c.rebate.toFixed(2), c.link ? c.link.status : "not_in_portal"]));
      const blob = new Blob(["﻿" + rows.map((r) => r.map((x) => `"${String(x ?? "").replace(/"/g, '""')}"`).join(",")).join("\n")], { type: "text/csv" });
      const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "ib-clients.csv"; a.click();
    }

    draw();
    ctx.store.ibLoad().then(async (d) => { data = d; const n = await autoConfirm(); if (n) note = "✅ " + t("ibr.confirmed", { n }); draw(); })
      .catch((e) => { data = empty(); note = `<b class="down">${t("app.error", { msg: e.message })}</b>`; draw(); });
  }

  root.OTMIB = { parseWorkbook, apply, readFiles, summary, render, empty, TABLES, DAY_TABLES };
})(window);
