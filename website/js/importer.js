// Reads MetaTrader history reports into journal trades.
// Supports: MT5 "Report" HTML (History), MT4 "Detailed Statement" HTML, and CSV exports.
(function (root) {
  const num = (s) => {
    if (s == null) return null;
    const v = parseFloat(String(s).replace(/\s| /g, "").replace(/,(?=\d{3}\b)/g, ""));
    return Number.isFinite(v) ? v : null;
  };
  const norm = (s) => String(s || "").toLowerCase().replace(/[^a-z]/g, "");

  // Broker server time is GMT+2, or GMT+3 while New York is on summer time (Vantage, PU Prime,
  // VT Markets all follow this). Report times are converted to real UTC with it.
  function nthSunday(y, m, n) { const d = new Date(Date.UTC(y, m, 1)); d.setUTCDate(1 + ((7 - d.getUTCDay()) % 7) + 7 * (n - 1)); return d; }
  function serverOffsetHours(y, mo, d) {
    const t = Date.UTC(y, mo, d);
    return t >= nthSunday(y, 2, 2).getTime() && t < nthSunday(y, 10, 1).getTime() ? 3 : 2;
  }
  function parseTime(s) {
    const m = String(s || "").trim().match(/(\d{4})[.\-/](\d{1,2})[.\-/](\d{1,2})[ T]+(\d{1,2}):(\d{2})(?::(\d{2}))?/);
    if (!m) return null;
    const [y, mo, d, h, mi, se] = [+m[1], +m[2] - 1, +m[3], +m[4], +m[5], +(m[6] || 0)];
    return new Date(Date.UTC(y, mo, d, h - serverOffsetHours(y, mo, d), mi, se)).toISOString();
  }

  // header text -> field; duplicates (Time, Price) map to open first, close second
  function mapHeader(cells) {
    const idx = {};
    const seen = {};
    cells.forEach((c, i) => {
      const k = norm(c);
      const take = (f) => { if (idx[f] == null) idx[f] = i; };
      if (k === "time" || k === "price") {
        seen[k] = (seen[k] || 0) + 1;
        take((seen[k] === 1 ? "open_" : "close_") + (k === "time" ? "time" : "price"));
      } else if (k === "opentime") take("open_time");
      else if (k === "closetime") take("close_time");
      else if (k === "openprice") take("open_price");
      else if (k === "closeprice") take("close_price");
      else if (k === "symbol" || k === "item") take("symbol");
      else if (k === "type" || k === "side" || k === "direction") take("side");
      else if (k === "volume" || k === "size" || k === "lots" || k === "lot") take("volume");
      else if (k === "sl" || k === "stoploss") take("sl");
      else if (k === "tp" || k === "takeprofit") take("tp");
      else if (k === "commission" || k === "commissions") take("commission");
      else if (k === "swap" || k === "swaps") take("swap");
      else if (k === "profit") take("profit");
      else if (k === "position" || k === "ticket" || k === "order" || k === "deal") take("ticket");
    });
    return idx;
  }
  const isHeader = (cells) => {
    const k = cells.map(norm);
    return k.some((c) => c === "symbol" || c === "item") && k.includes("profit") && k.some((c) => c.includes("time"));
  };

  function rowsToTrades(rows) {
    const trades = [];
    let idx = null;
    for (const cells of rows) {
      if (isHeader(cells)) { idx = mapHeader(cells); continue; }
      if (!idx) continue;
      if (cells.length < 6) { // a section title such as "Orders" or "Deals" ends the table
        if (trades.length) idx = null;
        continue;
      }
      const side = norm(cells[idx.side]);
      if (side !== "buy" && side !== "sell") continue;
      const open = parseTime(cells[idx.open_time]);
      const close = parseTime(cells[idx.close_time]);
      const symbol = String(cells[idx.symbol] || "").trim().toUpperCase();
      if (!open || !close || !symbol) continue;
      trades.push({
        ticket: String(cells[idx.ticket] ?? "").trim(),
        symbol, side,
        volume: num(cells[idx.volume]) || 0,
        open_time: open, close_time: close,
        open_price: num(cells[idx.open_price]), close_price: num(cells[idx.close_price]),
        sl: num(cells[idx.sl]) || null, tp: num(cells[idx.tp]) || null,
        commission: num(cells[idx.commission]) || 0,
        swap: num(cells[idx.swap]) || 0,
        profit: num(cells[idx.profit]) || 0
      });
    }
    return trades;
  }

  function decode(buf) {
    const b = new Uint8Array(buf);
    if (b[0] === 0xff && b[1] === 0xfe) return new TextDecoder("utf-16le").decode(b);
    if (b[0] === 0xfe && b[1] === 0xff) return new TextDecoder("utf-16be").decode(b);
    // MT5 reports are UTF-16 without a BOM on some builds: many zero bytes give it away
    let zeros = 0; for (let i = 1; i < Math.min(b.length, 400); i += 2) if (b[i] === 0) zeros++;
    if (zeros > 100) return new TextDecoder("utf-16le").decode(b);
    return new TextDecoder("utf-8").decode(b);
  }

  function htmlRows(text) {
    const doc = new DOMParser().parseFromString(text, "text/html");
    const rows = [];
    for (const tr of doc.querySelectorAll("tr")) {
      const cells = [];
      for (const td of tr.children) {
        const span = Math.max(1, +td.getAttribute("colspan") || 1);
        const hidden = /display:\s*none/i.test(td.getAttribute("style") || "") || td.classList.contains("hidden");
        if (hidden) continue;
        cells.push(td.textContent.trim());
        for (let i = 1; i < span; i++) cells.push("");
      }
      rows.push(cells);
    }
    return { rows, text: doc.body ? doc.body.textContent : text };
  }

  function csvRows(text) {
    const first = text.split(/\r?\n/)[0] || "";
    const delim = [";", "\t", ","].sort((a, b) => first.split(b).length - first.split(a).length)[0];
    return text.split(/\r?\n/).filter((l) => l.trim()).map((line) => {
      const out = []; let cur = ""; let q = false;
      for (let i = 0; i < line.length; i++) {
        const c = line[i];
        if (c === '"') { if (q && line[i + 1] === '"') { cur += '"'; i++; } else q = !q; }
        else if (c === delim && !q) { out.push(cur.trim()); cur = ""; }
        else cur += c;
      }
      out.push(cur.trim());
      return out;
    });
  }

  function accountInfo(text) {
    const acc = text.match(/Account:\s*([0-9]{4,})/i);
    const server = text.match(/\(\s*[A-Z]{3}\s*,\s*([^,)]+)/) || text.match(/Server:\s*([^\n]+)/i);
    const currency = text.match(/\(\s*([A-Z]{3})\s*,/);
    return {
      account_number: acc ? acc[1] : "",
      server: server ? server[1].trim() : "",
      currency: currency ? currency[1] : ""
    };
  }

  async function parseFile(file) {
    const text = decode(await file.arrayBuffer());
    const looksHtml = /<\s*(html|table|tr)\b/i.test(text.slice(0, 5000)) || /\.html?$/i.test(file.name);
    let rows, info = { account_number: "", server: "", currency: "" };
    if (looksHtml) {
      const r = htmlRows(text);
      rows = r.rows; info = accountInfo(r.text);
    } else {
      rows = csvRows(text);
    }
    const trades = rowsToTrades(rows);
    if (!trades.length) throw new Error("no-trades");
    return { ...info, trades };
  }

  root.OTMImporter = { parseFile, rowsToTrades, parseTime, decode, csvRows };
  if (typeof module !== "undefined") module.exports = root.OTMImporter;
})(typeof window !== "undefined" ? window : globalThis);
