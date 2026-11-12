// Journal maths. Pure functions, no DOM: every number on the Journal page comes from here.
(function (root) {
  const net = (t) => (+t.profit || 0) + (+t.commission || 0) + (+t.swap || 0);
  const pad = (n) => String(n).padStart(2, "0");
  const dayKey = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
  const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
  const scale = (v, lo, hi) => clamp(((v - lo) / (hi - lo)) * 100, 0, 100);

  function weekStart(d) {
    const x = new Date(d.getFullYear(), d.getMonth(), d.getDate());
    const wd = (x.getDay() + 6) % 7; // Monday = 0
    x.setDate(x.getDate() - wd);
    return x;
  }

  // Trading session by the hour the trade was opened (UTC)
  function session(t) {
    const h = new Date(t.open_time).getUTCHours();
    if (h >= 7 && h < 12) return "london";
    if (h >= 12 && h < 21) return "newyork";
    return "asia";
  }

  function filterTrades(trades, f = {}, now = new Date()) {
    let from = null;
    if (f.period === "today") from = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    else if (f.period === "week") from = weekStart(now);
    else if (f.period === "month") from = new Date(now.getFullYear(), now.getMonth(), 1);
    else if (f.period === "year") from = new Date(now.getFullYear(), 0, 1);
    let to = null;
    if (f.period === "custom") {
      if (f.from) from = new Date(f.from + "T00:00:00");
      if (f.to) to = new Date(f.to + "T23:59:59.999");
    }
    return trades.filter((t) => {
      if (f.account && f.account !== "all" && t.account_id !== f.account) return false;
      if (from && new Date(t.close_time) < from) return false;
      if (to && new Date(t.close_time) > to) return false;
      if (f.side && f.side !== "all" && t.side !== f.side) return false;
      if (f.outcome === "win" && !(net(t) > 0)) return false;
      if (f.outcome === "loss" && !(net(t) < 0)) return false;
      if (f.symbol && f.symbol !== "all" && t.symbol !== f.symbol) return false;
      return true;
    });
  }

  function group(trades, keyFn) {
    const m = new Map();
    for (const t of trades) {
      const k = keyFn(t);
      const g = m.get(k) || { key: k, count: 0, wins: 0, losses: 0, net: 0, volume: 0 };
      const n = net(t);
      g.count++; g.net += n; g.volume += +t.volume || 0;
      if (n > 0) g.wins++; else if (n < 0) g.losses++;
      m.set(k, g);
    }
    for (const g of m.values()) { g.winRate = g.count ? (g.wins / g.count) * 100 : 0; g.avg = g.count ? g.net / g.count : 0; }
    return m;
  }

  function compute(tradesIn, startBalance = 0) {
    const trades = [...tradesIn].sort((a, b) => new Date(a.close_time) - new Date(b.close_time));
    const n = trades.length;
    let grossWin = 0, grossLoss = 0, wins = 0, losses = 0;
    for (const t of trades) {
      const v = net(t);
      if (v > 0) { grossWin += v; wins++; } else if (v < 0) { grossLoss += -v; losses++; }
    }
    const total = grossWin - grossLoss;
    const winRate = n ? (wins / n) * 100 : 0;
    const profitFactor = grossLoss ? grossWin / grossLoss : (grossWin ? Infinity : 0);
    const avgWin = wins ? grossWin / wins : 0;
    const avgLoss = losses ? grossLoss / losses : 0;
    const expectancy = n ? total / n : 0;

    // equity, drawdown, streaks
    const base = startBalance > 0 ? startBalance : Math.max(100, grossWin);
    let cum = 0, peak = 0, maxDD = 0, streak = 0, bestStreak = 0, worstStreak = 0;
    let best = null, worst = null;
    const curve = [];
    for (const t of trades) {
      const v = net(t);
      cum += v;
      peak = Math.max(peak, cum);
      maxDD = Math.max(maxDD, peak - cum);
      curve.push({ time: t.close_time, value: cum });
      if (v > 0) streak = streak > 0 ? streak + 1 : 1; else if (v < 0) streak = streak < 0 ? streak - 1 : -1;
      bestStreak = Math.max(bestStreak, streak); worstStreak = Math.min(worstStreak, streak);
      if (!best || v > net(best)) best = t;
      if (!worst || v < net(worst)) worst = t;
    }
    const maxDDPct = (maxDD / (base + peak)) * 100;

    const byDay = group(trades, (t) => dayKey(new Date(t.close_time)));
    const byWeek = group(trades, (t) => dayKey(weekStart(new Date(t.close_time))));
    const bySymbol = group(trades, (t) => t.symbol);
    const bySession = group(trades, session);
    const byWeekday = group(trades, (t) => (new Date(t.close_time).getDay() + 6) % 7);

    let bestSession = null;
    for (const g of bySession.values()) if (!bestSession || g.net > bestSession.net) bestSession = g;

    // performance score: six parts, each 0-100
    const weeks = [...byWeek.values()];
    const parts = n ? {
      winRate: scale(winRate, 30, 70),
      profitFactor: profitFactor === Infinity ? 100 : scale(profitFactor, 1, 3),
      avgWinLoss: avgLoss ? scale(avgWin / avgLoss, 0.5, 2.5) : (avgWin ? 100 : 0),
      recovery: maxDD ? scale(total / maxDD, 0, 5) : (total > 0 ? 100 : 0),
      drawdown: 100 - scale(maxDDPct, 0, 30),
      consistency: weeks.length ? (weeks.filter((w) => w.net > 0).length / weeks.length) * 100 : 0
    } : { winRate: 0, profitFactor: 0, avgWinLoss: 0, recovery: 0, drawdown: 0, consistency: 0 };
    const score = n ? Math.round(Object.values(parts).reduce((a, b) => a + b, 0) / 6) : 0;

    return {
      count: n, wins, losses, total, grossWin, grossLoss, winRate, profitFactor, avgWin, avgLoss,
      expectancy, maxDD, maxDDPct, bestStreak, worstStreak: -worstStreak, best, worst,
      balance: startBalance + total, curve, byDay, byWeek, bySymbol, bySession, byWeekday,
      bestSession, parts, score
    };
  }

  root.OTMStats = { net, compute, filterTrades, session, dayKey, weekStart };
  if (typeof module !== "undefined") module.exports = root.OTMStats;
})(typeof window !== "undefined" ? window : globalThis);
