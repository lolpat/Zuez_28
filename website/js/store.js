// Data layer. Two backends behind one API:
//  - Supabase (real accounts) when js/config.js has SUPABASE_URL and SUPABASE_ANON_KEY;
//  - demo mode otherwise: sample data in this browser's localStorage, same rules as the database.
(function (root) {
  const cfg = root.OTM_CONFIG || {};
  const live = !!(cfg.SUPABASE_URL && cfg.SUPABASE_ANON_KEY);
  let sb = null;

  function loadScript(src) {
    return new Promise((res, rej) => {
      const s = document.createElement("script");
      s.src = src; s.onload = res; s.onerror = () => rej(new Error("script"));
      document.head.appendChild(s);
    });
  }

  // ------------------------------------------------------------ demo backend
  const KEY = "otm_demo_v2";
  const seededRnd = (() => { let s = 20260912; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); })();
  const uid = () => (crypto.randomUUID ? crypto.randomUUID() : "id-" + Math.random().toString(36).slice(2) + Date.now());

  function makeTrades(userId, accountId, count, edge, days, rnd = seededRnd) {
    const syms = [["XAUUSD", 0.5], ["EURUSD", 0.2], ["GBPUSD", 0.15], ["USDJPY", 0.1], ["NAS100", 0.05]];
    const pick = () => { let r = rnd(); for (const [s, w] of syms) { if ((r -= w) <= 0) return s; } return "XAUUSD"; };
    const out = [];
    const now = Date.now();
    for (let i = 0; i < count; i++) {
      const close = new Date(now - rnd() * days * 864e5);
      const wd = close.getDay();
      if (wd === 0 || wd === 6) close.setDate(close.getDate() - (wd === 0 ? 2 : 1));
      close.setUTCHours(6 + Math.floor(rnd() * 14), Math.floor(rnd() * 60));
      const open = new Date(close.getTime() - (10 + rnd() * 240) * 6e4);
      const symbol = pick();
      const vol = [0.01, 0.01, 0.02, 0.03, 0.05][Math.floor(rnd() * 5)];
      const win = rnd() < edge;
      const size = vol * 100 * (symbol === "XAUUSD" ? 1.4 : 1);
      const profit = +(win ? size * (4 + rnd() * 9) : -size * (3 + rnd() * 6)).toFixed(2);
      const side = rnd() < 0.55 ? "buy" : "sell";
      const base = { XAUUSD: 4450, EURUSD: 1.162, GBPUSD: 1.352, USDJPY: 156.1, NAS100: 25400 }[symbol];
      const op = +(base * (1 + (rnd() - 0.5) * 0.02)).toFixed(symbol.includes("JPY") || symbol === "XAUUSD" || symbol === "NAS100" ? 2 : 5);
      out.push({
        id: uid(), user_id: userId, account_id: accountId, ticket: String(48000000 + Math.floor(rnd() * 1e6)),
        symbol, side, volume: vol, open_time: open.toISOString(), close_time: close.toISOString(),
        open_price: op, close_price: op, sl: null, tp: null,
        commission: -+(vol * 7).toFixed(2), swap: rnd() < 0.15 ? -+(rnd() * 2).toFixed(2) : 0, profit,
        note: "", feeling: "", execution: null, tags: [], lesson: ""
      });
    }
    // a few journalled examples
    out.sort((a, b) => new Date(b.close_time) - new Date(a.close_time));
    if (out[0]) Object.assign(out[0], { note: "Waited for the London retest before entering.", feeling: "calm", execution: 5, tags: ["breakout", "plan"], lesson: "Patience paid. Same setup next week." });
    if (out[2]) Object.assign(out[2], { note: "Entered early after a big red candle.", feeling: "fomo", execution: 2, tags: ["early"], lesson: "No entry without the close." });
    return out;
  }

  function seed() {
    const P = (id, full_name, email, role, status, upline_id, telegram, code, daysAgo) => ({
      id, full_name, email, role, status, upline_id, telegram, referral_code: code, language: "th",
      created_at: new Date(Date.now() - daysAgo * 864e5).toISOString()
    });
    const users = [
      P("owner", "Order The Market", "owner@demo", "owner", "approved", null, "@zuez_28", "OTM00001", 400),
      P("ib1", "Somchai K.", "somchai@demo", "ib", "approved", "owner", "@somchai_fx", "SOMCHAI1", 300),
      P("ib2", "Nok P.", "nok@demo", "ib", "approved", "ib1", "@nok_trades", "NOKTRADE", 200),
      P("me", "Krit T.", "krit@demo", "member", "approved", "ib2", "@krit_t", "KRIT0001", 120),
      P("m2", "Ploy S.", "ploy@demo", "member", "approved", "ib2", "@ploy_s", "PLOY0001", 90),
      P("m3", "Arthit W.", "arthit@demo", "member", "pending", "ib2", "@arthit", "ARTH0001", 2),
      P("m4", "Mali R.", "mali@demo", "member", "approved", "ib1", "@mali_r", "MALI0001", 150),
      P("m5", "Tanawat J.", "tanawat@demo", "member", "pending", "ib1", "@tanawat", "TANA0001", 1),
      P("ib3", "James L.", "james@demo", "ib", "approved", "owner", "@james_l", "JAMESL01", 250),
      P("m6", "Wan C.", "wan@demo", "member", "approved", "ib3", "@wan_c", "WANC0001", 60)
    ];
    const A = (id, user_id, broker, account_number, server, start) => ({ id, user_id, broker, account_number, server, platform: "MT5", currency: "USD", start_balance: start, created_at: new Date().toISOString() });
    const accounts = [
      A("a-me1", "me", "vtmarkets", "77012345", "VTMarkets-Live 6", 1000),
      A("a-me2", "me", "vantage", "58003311", "VantageInternational-Live 3", 500),
      A("a-ib1", "ib1", "vantage", "58001234", "VantageInternational-Live 3", 2000),
      A("a-ib2", "ib2", "puprime", "81100221", "PUPrime-Live 2", 1500),
      A("a-m2", "m2", "vtmarkets", "77019876", "VTMarkets-Live 6", 800),
      A("a-m3", "m3", "puprime", "81100998", "PUPrime-Live", 0),
      A("a-m4", "m4", "vantage", "58004455", "VantageInternational-Live 3", 1200),
      A("a-m5", "m5", "vtmarkets", "77015555", "VTMarkets-Live 6", 0),
      A("a-ib3", "ib3", "vtmarkets", "77010001", "VTMarkets-Live 6", 3000),
      A("a-m6", "m6", "puprime", "81107777", "PUPrime-Live 2", 600)
    ];
    const trades = [
      ...makeTrades("me", "a-me1", 150, 0.64, 120),
      ...makeTrades("me", "a-me2", 40, 0.55, 60),
      ...makeTrades("ib1", "a-ib1", 90, 0.6, 120),
      ...makeTrades("ib2", "a-ib2", 70, 0.58, 120),
      ...makeTrades("m2", "a-m2", 55, 0.5, 90),
      ...makeTrades("m4", "a-m4", 80, 0.62, 120),
      ...makeTrades("ib3", "a-ib3", 60, 0.57, 120),
      ...makeTrades("m6", "a-m6", 30, 0.45, 60)
    ];
    return { users, accounts, trades, session: null };
  }

  let db = null;
  function loadDemo() {
    try { db = JSON.parse(localStorage.getItem(KEY)); } catch { db = null; }
    if (!db || !db.users) { db = seed(); saveDemo(); }
    if (!db.lb) addLeaderboardDemo();
    if (db.lb < 2) addMoreDemoMembers();
    if (!db.flags) {   // sample members' countries for the leaderboard flags ("me" picks their own)
      const C = { ib1: "TH", ib2: "TH", m2: "TH", m3: "TH", m4: "TH", m5: "LA", ib3: "MY", m6: "TH" };
      const S = ["TH", "TH", "TH", "LA", "TH", "MY", "TH", "NO", "TH", "SG", "TH", "KH"];
      db.users.forEach((u) => { if ("country" in u) return; const k = /^s(\d+)$/.exec(u.id); if (C[u.id]) u.country = C[u.id]; else if (k) u.country = S[(+k[1] - 1) % 12]; });
      db.flags = 1; saveDemo();
    }
    if (!db.links) {
      const L = (id, user_id, broker, client_id, status, days) => ({ id, user_id, broker, client_id, status, created_at: new Date(Date.now() - days * 864e5).toISOString(), verified_at: status === "verified" ? new Date(Date.now() - (days - 1) * 864e5).toISOString() : null });
      db.links = [
        L("l1", "me", "vtmarkets", "VT1200345", "verified", 30),
        L("l2", "m2", "vtmarkets", "VT1209876", "pending", 1),
        L("l3", "m4", "vantage", "VG5580044", "pending", 2),
        L("l4", "ib2", "puprime", "PU8110221", "verified", 60),
        L("l5", "m6", "puprime", "PU8117777", "pending", 1)
      ];
      saveDemo();
    }
  }
  // demo preview only: extra sample members so ranks 11-20 can be seen. The live site never has these.
  function addMoreDemoMembers() {
    const names = ["Arm S.", "Bank T.", "Beam K.", "Fern P.", "Gun W.", "Ice N.", "Jane M.", "Kao R.", "Mook J.", "Nat C.", "Oil V.", "Pang L.", "Pete D.", "Tae H.", "Tong B.", "View A.", "Win Y.", "Yok F."];
    const uplines = ["ib1", "ib2", "ib3"];
    names.forEach((nm, k) => {
      const id = "s" + (k + 1);
      const ex = db.users.find((u) => u.id === id);
      if (ex) { if (!("country" in ex)) ex.country = ["TH", "TH", "TH", "LA", "TH", "MY", "TH", "NO", "TH", "SG", "TH", "KH"][k % 12]; return; }
      db.users.push({ id, full_name: nm, email: `sample${k + 1}@demo`, role: "member", status: "approved", upline_id: uplines[k % 3], telegram: "", referral_code: "SMPL" + String(k + 1).padStart(4, "0"),
        language: "th", created_at: new Date(Date.now() - (20 + k) * 864e5).toISOString(), leaderboard_opt_in: true, leaderboard_name: nm.split(" ")[0],
        country: ["TH", "TH", "TH", "LA", "TH", "MY", "TH", "NO", "TH", "SG", "TH", "KH"][k % 12] });
      const acc = { id: "a-" + id, user_id: id, broker: ["vantage", "puprime", "vtmarkets"][k % 3], account_number: String(60010000 + k), server: "", platform: "MT5", currency: "USD", start_balance: 500 + (k % 5) * 500, account_type: "live", created_at: new Date().toISOString() };
      db.accounts.push(acc);
      db.trades.push(...makeTrades(id, acc.id, 12 + (k % 7) * 4, 0.5 + (k % 5) * 0.04, 25, Math.random).map((t) => ({ ...t, note: "", feeling: "", execution: null, tags: [], lesson: "" })));
    });
    db.lb = 2; saveDemo();
  }
  // demo leaderboard: some sample members joined, a few demo accounts, and recent trades
  function addLeaderboardDemo() {
    const now = Date.now();
    const recent = (uidv, acc, n, edge) => makeTrades(uidv, acc, n, edge, 6, Math.random).map((t) => {
      const shift = new Date(t.close_time).getTime() > now ? 864e5 : 0;
      return { ...t, open_time: new Date(new Date(t.open_time).getTime() - shift).toISOString(), close_time: new Date(new Date(t.close_time).getTime() - shift).toISOString(), note: "", feeling: "", execution: null, tags: [], lesson: "" };
    });
    const joined = { ib1: "Somchai", ib2: "NokTrade", m2: "PloyFX", m4: "Mali R.", ib3: "James", m6: "WanGold" };
    db.users.forEach((u) => { if (joined[u.id]) Object.assign(u, { leaderboard_opt_in: true, leaderboard_name: joined[u.id] }); });
    const accOf = (u) => db.accounts.find((a) => a.user_id === u && (a.account_type || "live") === "live");
    [["ib1", 14, 0.62], ["ib2", 9, 0.6], ["m2", 11, 0.5], ["m4", 16, 0.66], ["ib3", 8, 0.55], ["m6", 6, 0.42], ["me", 7, 0.6]].forEach(([u, n, e]) => {
      const a = accOf(u); if (a) db.trades.push(...recent(u, a.id, n, e));
    });
    [["m2", "77019001", "VTMarkets-Demo"], ["ib3", "77010009", "VTMarkets-Demo"], ["m6", "81109001", "PUPrime-Demo"], ["m4", "58009001", "VantageInternational-Demo"]].forEach(([u, num, server], i) => {
      const id = "a-demo-" + u;
      if (db.accounts.some((a) => a.id === id)) return;
      db.accounts.push({ id, user_id: u, broker: server.startsWith("VT") ? "vtmarkets" : server.startsWith("PU") ? "puprime" : "vantage", account_number: num, server, platform: "MT5", currency: "USD", start_balance: 10000, account_type: "demo", created_at: new Date().toISOString() });
      db.trades.push(...recent(u, id, 10 + i * 4, 0.55 + i * 0.03));
    });
    db.lb = 1; saveDemo();
  }
  function saveDemo() { try { localStorage.setItem(KEY, JSON.stringify(db)); } catch { /* private mode: keep in memory */ } }
  const me = () => db.users.find((u) => u.id === db.session);
  function isAncestor(a, target) {
    let u = db.users.find((x) => x.id === target);
    for (let i = 0; u && u.upline_id && i < 50; i++) { if (u.upline_id === a) return true; u = db.users.find((x) => x.id === u.upline_id); }
    return false;
  }
  const canManage = (target) => { const m = me(); return m && (m.role === "owner" || (m.role === "ib" && m.status === "approved" && isAncestor(m.id, target))); };

  const demo = {
    async getSession() { return me() || null; },
    async signIn(email) {
      const u = db.users.find((x) => x.email.toLowerCase() === String(email).trim().toLowerCase());
      if (!u) throw new Error("bad-login");
      db.session = u.id; saveDemo(); return u;
    },
    async demoSignIn(who) { db.session = who; saveDemo(); return me(); },
    async signUp(d) {
      if (db.users.some((u) => u.email.toLowerCase() === d.email.toLowerCase())) throw new Error("email-taken");
      const up = db.users.find((u) => u.referral_code === String(d.referral_code || "").trim().toUpperCase() && (u.role === "ib" || u.role === "owner"));
      const u = {
        id: uid(), full_name: d.full_name, email: d.email, role: "member", status: "pending",
        upline_id: up ? up.id : null, telegram: d.telegram, language: d.language || "th",
        referral_code: Math.random().toString(36).slice(2, 10).toUpperCase(), created_at: new Date().toISOString()
      };
      db.users.push(u);
      db.accounts.push({ id: uid(), user_id: u.id, broker: d.broker, account_number: d.account_number, server: "", platform: d.platform || "MT5", currency: "USD", start_balance: 0, created_at: u.created_at });
      db.session = u.id; saveDemo(); return { user: u, needsConfirm: false };
    },
    async signOut() { db.session = null; saveDemo(); },
    async resetPassword() { return true; },
    async updateProfile(f) { const m = me(); ["full_name", "telegram", "language", "leaderboard_opt_in", "leaderboard_name", "country"].forEach((k) => { if (k in f) m[k] = f[k]; }); saveDemo(); return m; },
    // live chart stream (one row; the owner sets it)
    async liveStream() { return { url: "", title: "", is_live: false, ...(db.live || {}) }; },
    async setLiveStream(f) {
      if (me().role !== "owner") throw new Error("forbidden");
      db.live = { ...(db.live || {}), ...f, updated_at: new Date().toISOString() }; saveDemo(); return db.live;
    },
    // the levels panel next to the chart (demo: made-up levels, labelled as a sample on the page)
    // per-signal charts (demo: a few sample signals with made-up candles, labelled as samples on the page)
    async signalPositions(room) {
      const P = (id, side, entry, entry2, sl, tps, pips, risk, opened, mins) => ({ id, room, symbol: "XAUUSD", side, entry, entry2, sl, tps, risk, pips, status: pips > 0 ? "win" : pips < 0 ? "loss" : "be",
        opened_at: opened, closed_at: new Date(Date.parse(opened) + mins * 60e3).toISOString(), sample: true });
      const list = {
        swing: [P("d:1", "sell", 3590, 3600, 3610, [3486, 3582, 3578, 3574, 3570, 3000], 700, 200, "2026-11-20T08:32:22Z", 446),
                P("d:2", "sell", 3612, 3620, 3632, [3608, 3604, 3600, 3596], 160, 200, "2026-11-20T05:55:00Z", 95),
                P("d:3", "buy", 3540, 3532, 3520, [3544, 3548, 3552, 3556, 3560], 370, 200, "2026-11-19T03:39:00Z", 240)],
        scalp: [P("d:4", "buy", 3533, 3534, 3528, [3538], 162, 50, "2026-11-20T01:24:00Z", 70),
                P("d:5", "buy", 3541, 3542, 3537, [3546], -40, 40, "2026-11-20T04:33:00Z", 35)],
        rr: [P("d:6", "sell", 3560, null, 3563.76, [3556, 3552, 3548, 3545], 150, 37.6, "2026-11-20T15:56:13Z", 130),
             P("d:7", "sell", 3575, null, 3578.4, [3570, 3565, 3555], 237, 34.7, "2026-11-19T15:20:00Z", 180)],
      }[room] || [];
      return list;
    },
    async signalCandles(id) {
      const p = Object.values({ swing: 1, scalp: 1, rr: 1 }).length && (await Promise.all(["swing", "scalp", "rr"].map((r) => this.signalPositions(r)))).flat().find((x) => x.id === id);
      if (!p) throw new Error("not-found");
      const o = Date.parse(p.opened_at) / 1000, c = Date.parse(p.closed_at) / 1000, dur = Math.max(c - o, 900);
      const step = dur <= 8 * 3600 ? 300 : dur <= 3 * 86400 ? 900 : 3600, pad = Math.max(dur * .35, step * 24);
      const t0 = Math.floor((o - pad) / step) * step, t9 = Math.ceil((c + pad * .6) / step) * step;
      const ppu = 10, exit = p.side === "sell" ? p.entry - p.pips / ppu : p.entry + p.pips / ppu;
      const approach = p.side === "sell" ? p.entry - 18 : p.entry + 18;
      let seed = Math.round(o) % 9973; const rnd = () => (seed = (seed * 9301 + 49297) % 233280) / 233280;
      const at = (t) => t <= o ? approach + (p.entry - approach) * (t - t0) / (o - t0)
        : t <= c ? p.entry + (exit - p.entry) * Math.pow((t - o) / (c - o), .85) + Math.sin((t - o) / 1800) * Math.abs(exit - p.entry) * .06
        : exit + Math.sin((t - c) / 2400) * 2.5;
      const guard = p.pips >= 0 && p.sl != null ? (p.side === "sell" ? (v) => Math.min(v, p.sl - .4) : (v) => Math.max(v, p.sl + .4)) : (v) => v;
      const out = []; let prev = at(t0);
      for (let t = t0; t <= t9; t += step) {
        const close = at(t + step) + (rnd() - .5) * 1.6, open = prev;
        out.push({ t, o: +open.toFixed(2), h: +guard(Math.max(open, close) + rnd() * 1.3).toFixed(2), l: +guard(Math.min(open, close) - rnd() * 1.3).toFixed(2), c: +close.toFixed(2) });
        prev = close;
      }
      return { tf: step === 300 ? "5min" : step === 900 ? "15min" : "1h", candles: out, sample: true };
    },
    async chartSetup() {
      const last = 3480, r = (x) => +(Math.round(x * 2) / 2).toFixed(1);
      return { sample: true, source: "sample", tf: "15m", side: "buy", entry_lo: r(last - 3), entry_hi: r(last - 1), sl: r(last - 15),
        tp1: r(last + 9), tp2: r(last + 20), tp3: r(last + 31), runner: r(last + 55), created_at: new Date(Date.now() - 50 * 60e3).toISOString() };
    },
    async leaderboard(period, type = "live", verified = false) {
      const { start } = root.OTMStats.lbPeriod(period);
      const typeOf = new Map(db.accounts.map((a) => [a.id, a.account_type || "live"]));
      const n = (t) => (+t.profit || 0) + (+t.commission || 0) + (+t.swap || 0);
      const rows = db.users.filter((u) => u.status === "approved" && u.leaderboard_opt_in !== false).map((u) => {
        const tr = db.trades.filter((t) => t.user_id === u.id && typeOf.get(t.account_id) === type && (!start || new Date(t.close_time) >= start) && (!verified || t.source === "sync"))
          .sort((a, b) => new Date(b.close_time) - new Date(a.close_time));
        if (!tr.length) return null;
        const v = tr.map(n), wins = v.filter((x) => x > 0), losses = v.filter((x) => x < 0);
        let streak = 0; for (const x of v) { if (x > 0) streak++; else break; }
        const bal = db.accounts.filter((a) => a.user_id === u.id && (a.account_type || "live") === type).reduce((s, a) => s + (+a.start_balance || 0), 0);
        const net = v.reduce((a, b) => a + b, 0);
        return { display_name: (u.leaderboard_name || "").trim() || u.full_name.split(" ")[0], country: u.country || null, trades: tr.length, wins: wins.length, losses: losses.length,
          net, gross_win: wins.reduce((a, b) => a + b, 0), gross_loss: -losses.reduce((a, b) => a + b, 0), streak,
          return_pct: bal > 0 ? (net / bal) * 100 : null, is_me: u.id === db.session, verified: tr.every((t) => t.source === "sync") };
      }).filter(Boolean);
      const ranked = rows.filter((r) => r.net > 0).sort((a, b) => b.net - a.net || a.trades - b.trades);
      return ranked.map((r, i) => ({ ...r, rank: i + 1, field_size: rows.length, in_profit: ranked.length })).filter((r) => r.rank <= 20 || r.is_me);
    },
    async listAccounts() { return db.accounts.filter((a) => a.user_id === db.session); },
    async addAccount(a) {
      if (db.accounts.some((x) => x.broker === a.broker && x.account_number === a.account_number)) throw new Error("account-taken");
      if (db.accounts.filter((x) => x.user_id === db.session).length >= (cfg.MAX_ACCOUNTS || 10)) throw new Error("account-limit");
      const acc = { id: uid(), user_id: db.session, server: "", platform: "MT5", currency: "USD", start_balance: 0, created_at: new Date().toISOString(), ...a };
      db.accounts.push(acc); saveDemo(); return acc;
    },
    async updateAccount(id, f) {
      const a = db.accounts.find((x) => x.id === id && x.user_id === db.session);
      if (!a) throw new Error("not-found");
      const broker = f.broker ?? a.broker, num = f.account_number ?? a.account_number;
      if (db.accounts.some((x) => x.id !== id && x.broker === broker && x.account_number === num)) throw new Error("account-taken");
      Object.assign(a, f); saveDemo(); return a;
    },
    async setAccountType(id, type) {
      if (!me() || me().role !== "owner") throw new Error("not-allowed");
      const a = db.accounts.find((x) => x.id === id); if (!a) throw new Error("not-found");
      Object.assign(a, { account_type: type, type_locked: true }); saveDemo(); return a;
    },
    async deleteAccount(id) {
      db.accounts = db.accounts.filter((x) => !(x.id === id && x.user_id === db.session));
      db.trades = db.trades.filter((x) => !(x.account_id === id && x.user_id === db.session)); saveDemo();
    },
    // automatic history: the demo fills in sample trades instead of calling MetaApi
    async syncConnect(id, server, password) {
      const a = db.accounts.find((x) => x.id === id && x.user_id === db.session);
      if (!a) throw new Error("not-found");
      if (!server || !password) throw new Error("missing");
      await new Promise((r) => setTimeout(r, 1200));
      if (/^wrong/i.test(password)) { Object.assign(a, { sync_status: "error", sync_error: "bad-login" }); saveDemo(); throw new Error("bad-login"); }
      const have = new Set(db.trades.filter((t) => t.account_id === id).map((t) => t.ticket));
      const fresh = makeTrades(db.session, id, 45, 0.56, 75, Math.random).filter((r) => !have.has(r.ticket))
        .map((r) => ({ ...r, source: "sync", note: "", feeling: "", execution: null, tags: [], lesson: "" }));
      db.trades.push(...fresh);
      Object.assign(a, { server, metaapi_id: "demo", sync_status: "ok", sync_error: "", last_sync_at: new Date().toISOString(), consent_at: new Date().toISOString() });
      if (!+a.start_balance) a.start_balance = 1000;
      demoInfo(a);
      saveDemo(); return { status: "ok", added: fresh.length };
    },
    async syncNow(id) {
      const a = db.accounts.find((x) => x.id === id && x.user_id === db.session);
      if (!a || !a.metaapi_id) throw new Error("not-connected");
      await new Promise((r) => setTimeout(r, 800));
      const fresh = makeTrades(db.session, id, 2, 0.55, 0.04, Math.random).slice(0, Math.floor(Math.random() * 3))
        .map((r) => ({ ...r, source: "sync", note: "", feeling: "", execution: null, tags: [], lesson: "" }));
      db.trades.push(...fresh);
      Object.assign(a, { sync_status: "ok", sync_error: "", last_sync_at: new Date().toISOString() });
      demoInfo(a);
      saveDemo(); return { status: "ok", added: fresh.length };
    },
    async syncDisconnect(id) {
      const a = db.accounts.find((x) => x.id === id && x.user_id === db.session);
      if (a) Object.assign(a, { metaapi_id: null, sync_status: "off", sync_error: "", consent_at: null });
      saveDemo(); return { status: "off" };
    },
    async listTrades() { return db.trades.filter((t) => t.user_id === db.session); },
    async addTrade(t) {
      if (me().status !== "approved") throw new Error("not-approved");
      const row = { id: uid(), user_id: db.session, note: "", feeling: "", execution: null, tags: [], lesson: "", ticket: "", ...t };
      db.trades.push(row); saveDemo(); return row;
    },
    async updateTrade(id, f) { const t = db.trades.find((x) => x.id === id && x.user_id === db.session); Object.assign(t, f); saveDemo(); return t; },
    async deleteTrade(id) { db.trades = db.trades.filter((x) => !(x.id === id && x.user_id === db.session)); saveDemo(); },
    async importTrades(accountId, rows) {
      if (me().status !== "approved") throw new Error("not-approved");
      const have = new Set(db.trades.filter((t) => t.account_id === accountId).map((t) => t.ticket));
      const fresh = rows.filter((r) => !r.ticket || !have.has(r.ticket));
      fresh.forEach((r) => db.trades.push({ id: uid(), user_id: db.session, account_id: accountId, note: "", feeling: "", execution: null, tags: [], lesson: "", source: "import", ...r }));
      saveDemo(); return { added: fresh.length, skipped: rows.length - fresh.length };
    },
    async myUpline() { const m = me(); const u = m && db.users.find((x) => x.id === m.upline_id); return u ? { full_name: u.full_name, telegram: u.telegram } : null; },
    async myDownline() {
      const m = me(); if (!m) return [];
      const depthOf = (u) => { let d = 0, x = u; while (x && x.id !== m.id && d < 50) { x = db.users.find((y) => y.id === x.upline_id); d++; } return d; };
      const list = db.users.filter((u) => u.id !== m.id && (m.role === "owner" || isAncestor(m.id, u.id)));
      return list.map((u) => {
        const tr = db.trades.filter((t) => t.user_id === u.id);
        const nets = tr.map((t) => t.profit + t.commission + t.swap);
        const accs = db.accounts.filter((a) => a.user_id === u.id);
        return {
          ...u, depth: depthOf(u),
          brokers: [...new Set(accs.map((a) => a.broker))].join(","), accounts: accs.map((a) => a.account_number).join(","),
          trade_count: tr.length, net_profit: nets.reduce((a, b) => a + b, 0),
          win_rate: tr.length ? (nets.filter((v) => v > 0).length / tr.length) * 100 : null,
          synced: accs.some((a) => a.sync_status && a.sync_status !== "off")
        };
      }).sort((a, b) => a.depth - b.depth || new Date(a.created_at) - new Date(b.created_at));
    },
    async setMemberStatus(id, status) { if (!canManage(id)) throw new Error("not-allowed"); db.users.find((u) => u.id === id).status = status; saveDemo(); },
    async setMemberRole(id, role) { if (me().role !== "owner") throw new Error("not-allowed"); db.users.find((u) => u.id === id).role = role; saveDemo(); },
    // broker ID connections
    async listMyLinks() { return db.links.filter((l) => l.user_id === db.session); },
    async saveLink(broker, clientId) {
      const id = String(clientId || "").trim();
      if (id.length < 3) throw new Error("bad-id");
      if (db.links.some((l) => l.broker === broker && l.client_id.toLowerCase() === id.toLowerCase() && l.user_id !== db.session)) throw new Error("id-taken");
      let l = db.links.find((x) => x.user_id === db.session && x.broker === broker);
      if (l && l.status === "verified") throw new Error("not-allowed");
      if (!l) { l = { id: uid(), user_id: db.session, broker }; db.links.push(l); }
      Object.assign(l, { client_id: id, status: "pending", created_at: new Date().toISOString(), verified_at: null });
      saveDemo(); return l;
    },
    async removeLink(id) { db.links = db.links.filter((l) => !(l.id === id && l.user_id === db.session && l.status !== "verified")); saveDemo(); },
    async listTeamLinks() { const m = me(); return db.links.filter((l) => l.user_id !== m.id && (m.role === "owner" || isAncestor(m.id, l.user_id))); },
    async setLinkStatus(id, status) {
      const l = db.links.find((x) => x.id === id); if (!l) throw new Error("not-found");
      if (!canManage(l.user_id)) throw new Error("not-allowed");
      Object.assign(l, { status, verified_at: status === "verified" ? new Date().toISOString() : null }); saveDemo();
    },
    // broker IB reports, kept per IB in this browser (see js/ibreports.js)
    async ibLoad() { try { return JSON.parse(localStorage.getItem("otm_ib_" + db.session)) || root.OTMIB.empty(); } catch (e) { return root.OTMIB.empty(); } },
    async ibSave(batch) {
      const d = root.OTMIB.apply(await this.ibLoad(), batch);
      try { localStorage.setItem("otm_ib_" + db.session, JSON.stringify(d)); } catch (e) { throw new Error("storage-full"); }
      return d;
    },
    async resetDemo() { localStorage.removeItem(KEY); loadDemo(); }
  };

  // demo stand-in for what the sync reads from the broker: balance = start + closed P/L, equity = balance plus open trades
  function demoInfo(a) {
    const closed = db.trades.filter((t) => t.account_id === a.id).reduce((s, t) => s + (+t.profit || 0) + (+t.commission || 0) + (+t.swap || 0), 0);
    const bal = Math.round(((+a.start_balance || 0) + closed) * 100) / 100;
    Object.assign(a, { balance: bal, equity: Math.round((bal + (Math.random() - 0.5) * 40) * 100) / 100, margin: 0,
      broker_mode: /demo/i.test(a.server || "") ? "demo" : "real", info_at: new Date().toISOString() });
  }

  // ------------------------------------------------------------ Supabase backend
  let profileCache = null;
  const must = ({ data, error }) => { if (error) throw new Error(error.message); return data; };
  const sbApi = {
    async getSession() {
      const { data } = await sb.auth.getSession();
      if (!data.session) return null;
      profileCache = must(await sb.from("profiles").select("*").eq("id", data.session.user.id).maybeSingle());
      return profileCache;
    },
    async signIn(email, password) {
      const { error } = await sb.auth.signInWithPassword({ email, password });
      if (error) throw new Error("bad-login");
      return sbApi.getSession();
    },
    async signUp(d) {
      const { data, error } = await sb.auth.signUp({
        email: d.email, password: d.password,
        options: { data: { full_name: d.full_name, telegram: d.telegram, broker: d.broker, account_number: d.account_number, platform: d.platform, referral_code: d.referral_code, language: d.language },
          emailRedirectTo: location.origin + location.pathname.replace(/[^/]*$/, "") + "app.html" }
      });
      if (error) throw new Error(/registered/i.test(error.message) ? "email-taken" : error.message);
      return { user: data.user, needsConfirm: !data.session };
    },
    async signOut() { await sb.auth.signOut(); profileCache = null; },
    async resetPassword(email) {
      const { error } = await sb.auth.resetPasswordForEmail(email, { redirectTo: location.origin + location.pathname.replace(/[^/]*$/, "") + "app.html#profile" });
      if (error) throw new Error(error.message); return true;
    },
    async updateProfile(f) {
      const pick = {}; ["full_name", "telegram", "language", "leaderboard_opt_in", "leaderboard_name", "country"].forEach((k) => { if (k in f) pick[k] = f[k]; });
      must(await sb.from("profiles").update(pick).eq("id", profileCache.id));
      Object.assign(profileCache, pick); return profileCache;
    },
    async listAccounts() { return must(await sb.from("broker_accounts").select("*").eq("user_id", profileCache.id).order("created_at")); },
    async addAccount(a) {
      const { data, error } = await sb.from("broker_accounts").insert({ ...a, user_id: profileCache.id }).select().single();
      if (error) throw new Error(/duplicate/i.test(error.message) ? "account-taken" : /account-limit/.test(error.message) ? "account-limit" : error.message);
      return data;
    },
    async updateAccount(id, f) {
      const { data, error } = await sb.from("broker_accounts").update(f).eq("id", id).select().single();
      if (error) throw new Error(/duplicate/i.test(error.message) ? "account-taken" : error.message);
      return data;
    },
    async setAccountType(id, type) { must(await sb.rpc("set_account_type", { p_account: id, p_type: type })); },
    // through a function: an account's MT5 trades can only be removed together with the account
    async deleteAccount(id) { must(await sb.rpc("delete_account", { acc: id })); },
    async listTrades() {
      const all = []; let from = 0;
      for (;;) {
        const page = must(await sb.from("trades").select("*").eq("user_id", profileCache.id).order("close_time").range(from, from + 999));
        all.push(...page); if (page.length < 1000) break; from += 1000;
      }
      return all.map((t) => ({ ...t, volume: +t.volume, profit: +t.profit, commission: +t.commission, swap: +t.swap }));
    },
    async addTrade(t) { return must(await sb.from("trades").insert({ ...t, user_id: profileCache.id }).select().single()); },
    async updateTrade(id, f) { return must(await sb.from("trades").update(f).eq("id", id).select().single()); },
    async deleteTrade(id) { must(await sb.from("trades").delete().eq("id", id)); },
    async importTrades(accountId, rows) {
      const have = new Set(must(await sb.from("trades").select("ticket").eq("account_id", accountId)).map((r) => r.ticket));
      const fresh = rows.filter((r) => !r.ticket || !have.has(r.ticket)).map((r) => ({ ...r, source: "import", account_id: accountId, user_id: profileCache.id }));
      for (let i = 0; i < fresh.length; i += 500) must(await sb.from("trades").insert(fresh.slice(i, i + 500)));
      return { added: fresh.length, skipped: rows.length - fresh.length };
    },
    // automatic history through the mt-sync Edge Function (supabase/functions/mt-sync)
    async syncConnect(id, server, password) { return syncFn({ action: "connect", account_id: id, server, password, consent: true }); },
    async syncNow(id) { return syncFn({ action: "sync", account_id: id }); },
    async syncDisconnect(id) { return syncFn({ action: "disconnect", account_id: id }); },
    async liveStream() {
      const { data, error } = await sb.from("site_live").select("url,title,is_live,updated_at").eq("id", 1).maybeSingle();
      if (error) return null;   // table not created yet
      return data;
    },
    async setLiveStream(f) {
      const pick = {}; ["url", "title", "is_live"].forEach((k) => { if (k in f) pick[k] = f[k]; });
      pick.updated_at = new Date().toISOString();
      return must(await sb.from("site_live").update(pick).eq("id", 1).select().single());
    },
    async signalPositions(room) {
      const { data, error } = await sb.rpc("signal_positions", { p_room: room, p_limit: 60 });
      if (error) throw new Error(/function|schema cache/i.test(error.message) ? "not-configured" : error.message);
      return (data || []).map((r) => ({ ...numify(r), id: r.id, tps: (r.tps || []).map(Number) }));
    },
    async signalCandles(id) {
      const { data, error } = await sb.functions.invoke("signal-candles", { body: { id } });
      if (error) {
        let code = "not-configured";
        try { const j = await error.context.json(); code = j.error || code; } catch (_) { /* function not deployed or offline */ }
        throw new Error(code);
      }
      return data;
    },
    async chartSetup() {
      const { data, error } = await sb.from("chart_setups").select("*").is("closed_at", null).order("created_at", { ascending: false }).limit(1);
      if (error) return null;   // table not created yet
      return data && data[0] ? numify(data[0]) : null;
    },
    async leaderboard(period, type = "live", verified = false) {
      return (must(await sb.rpc("leaderboard", { p_period: period, p_type: type, p_verified: !!verified })) || []).map((r) => ({
        ...r, net: +r.net, gross_win: +r.gross_win, gross_loss: +r.gross_loss, return_pct: r.return_pct == null ? null : +r.return_pct }));
    },
    async myUpline() { const r = must(await sb.rpc("my_upline")); return r && r[0] ? r[0] : null; },
    async myDownline() { return (must(await sb.rpc("my_downline")) || []).map((r) => ({ ...r, net_profit: +r.net_profit, win_rate: r.win_rate == null ? null : +r.win_rate })); },
    async setMemberStatus(id, status) { must(await sb.rpc("set_member_status", { target: id, new_status: status })); },
    async setMemberRole(id, role) { must(await sb.rpc("set_member_role", { target: id, new_role: role })); },
    async listMyLinks() { return must(await sb.from("broker_links").select("*").eq("user_id", profileCache.id)); },
    async saveLink(broker, clientId) {
      const id = String(clientId || "").trim();
      if (id.length < 3) throw new Error("bad-id");
      const mine = must(await sb.from("broker_links").select("*").eq("user_id", profileCache.id).eq("broker", broker));
      const q = mine.length ? sb.from("broker_links").update({ client_id: id }).eq("id", mine[0].id) : sb.from("broker_links").insert({ user_id: profileCache.id, broker, client_id: id });
      const { data, error } = await q.select().single();
      if (error) throw new Error(/duplicate|unique/i.test(error.message) ? "id-taken" : error.message);
      return data;
    },
    async removeLink(id) { must(await sb.from("broker_links").delete().eq("id", id).eq("user_id", profileCache.id)); },
    async listTeamLinks() { return must(await sb.from("broker_links").select("*").neq("user_id", profileCache.id).order("created_at", { ascending: false })); },
    async setLinkStatus(id, status) { must(await sb.rpc("set_broker_link", { p_link: id, p_status: status })); },

    // broker IB reports (supabase/ib-reports.sql): each IB's own uploads, replaced day by day
    async ibLoad() {
      const out = root.OTMIB.empty();
      for (const k of root.OTMIB.TABLES) {
        for (let from = 0; ; from += 1000) {
          const rows = must(await sb.from("ib_" + k).select("*").eq("ib_id", profileCache.id).range(from, from + 999));
          out[k].push(...rows.map(({ ib_id, ...r }) => numify(r)));
          if (rows.length < 1000) break;
        }
      }
      return out;
    },
    async ibSave(batch) {
      const me = profileCache.id, chunk = async (table, rows, upsert) => {
        for (let i = 0; i < rows.length; i += 500) {
          const part = rows.slice(i, i + 500).map((r) => ({ ...r, ib_id: me }));
          must(await (upsert ? sb.from(table).upsert(part, { onConflict: upsert }) : sb.from(table).insert(part)));
        }
      };
      for (const k of root.OTMIB.DAY_TABLES) {
        const rows = batch[k] || []; if (!rows.length) continue;
        const byBroker = new Map(); rows.forEach((r) => { if (!byBroker.has(r.broker)) byBroker.set(r.broker, new Set()); byBroker.get(r.broker).add(r.day); });
        for (const [b, days] of byBroker) {
          const list = [...days];
          for (let i = 0; i < list.length; i += 200) must(await sb.from("ib_" + k).delete().eq("ib_id", me).eq("broker", b).in("day", list.slice(i, i + 200)));
        }
        await chunk("ib_" + k, rows);
      }
      if ((batch.accounts || []).length) await chunk("ib_accounts", batch.accounts, "ib_id,broker,account");
      if ((batch.subib || []).length) {
        const P = batch.subib[0];
        const periods = must(await sb.from("ib_subib").select("period_from, period_to").eq("ib_id", me).eq("broker", P.broker));
        const inside = periods.some((r) => r.period_from <= P.period_from && r.period_to >= P.period_to && !(r.period_from === P.period_from && r.period_to === P.period_to));
        if (!inside) {
          must(await sb.from("ib_subib").delete().eq("ib_id", me).eq("broker", P.broker).gte("period_from", P.period_from).lte("period_to", P.period_to));
          await chunk("ib_subib", batch.subib);
        }
      }
      return this.ibLoad();
    }
  };
  // numeric columns come back from the database as strings
  const numify = (r) => { const o = {}; for (const [k, v] of Object.entries(r)) o[k] = typeof v === "string" && /^-?\d+(\.\d+)?$/.test(v) && !/(^|_)(id|account|day|date|from|to|on)$/.test(k) ? +v : v; return o; };

  async function syncFn(body) {
    const { data, error } = await sb.functions.invoke("mt-sync", { body });
    if (error) {
      let code = "not-configured";
      try { const j = await error.context.json(); code = j.error || code; } catch (_) { /* function not deployed or offline */ }
      throw new Error(code);
    }
    return data;
  }

  const api = { live };
  api.init = async function () {
    if (live) {
      await loadScript("https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.js");
      sb = root.supabase.createClient(cfg.SUPABASE_URL, cfg.SUPABASE_ANON_KEY);
      Object.assign(api, sbApi);
    } else {
      loadDemo();
      Object.assign(api, demo);
    }
    return api;
  };
  root.OTMStore = api;
})(window);
