// Reads signal-room messages: which messages open a trade, and what a reply under a trade says.
// Plain JavaScript (no imports) so the edge function (Deno) and the tests (Node) share one copy.
//
// The rules come from the rooms' real posts (Telegram exports, Jan - Nov 2026):
//   signals:  "🥇 SWING ELITE #XAUUSD BUY ENTRY: 3978//3968 TP1: @ 3982 … SL: @ 3958"
//             "XAUUSD BUY 4261/4251 TP1. @ 4265 … SL @ 4241"
//             "⚡ OTM SCALPING PRO 🟢 BUY NOW 📍 ENTRY ZONE: 4053–4056 🛑 STOP LOSS: 4052"
//             "📊 XAUUSD LONG … ENTRY: 4496 – 4503 🛑 STOP LOSS: 4490 … SL: 500 points / 50 pips"
//             "🪎 XAUUSD 🔹 BUY ENTRY: 4048.13 🛑 STOP LOSS: 4044.54"
//             "BUY GOLD | 4564-63 ▪️SL: 4561.5 ▫️TP: 4580"
//   results:  "#XAUUSD TARGET3 HIT 120+PIPS PROFIT DONE", "GOLD BUY RUNNING 320+Pips Profit" (bold letters),
//             "TP 1 ✔️ +80pips", "+50 pips", "hit sl -40pips", "The stop loss was hit: -30 pips",
//             "Break-even hit.", "Buy +30pips but I will count this as BE", "Cancel"
// A trade counts the furthest profit posted under it; a posted stop loss if no profit was posted;
// break-even as 0. Gold: 1 price unit = 10 pips. BTCUSD / NAS100: 10 points = 1 pip.

const norm = (t) => String(t || "").normalize("NFKC");
const num = (s) => Number(String(s).replace(/,/g, ""));

function symbolOf(t) {
  if (/\bBTC/i.test(t)) return "BTCUSD";
  if (/NAS100|US100|NASDAQ/i.test(t)) return "NAS100";
  if (/XAUUSD|GOLD|SCALPING PRO|SWING ELITE/i.test(t)) return "XAUUSD";
  if (/\b(EUR|GBP|AUD|NZD|CAD|CHF|JPY|USD)(USD|JPY|GBP|EUR|CAD|CHF|AUD|NZD)\b|\bXAG|SILVER|US30|SPX|OIL/i.test(t)) return "OTHER";
  return null;
}
const pipsPerUnit = (sym) => (sym === "XAUUSD" ? 10 : 0.1);
const maxRisk = (sym) => (sym === "XAUUSD" ? 300 : 500);

// "5160-62" means 5160-5162
function expand(a, b) {
  if (b == null || b === "") return null;
  let v = num(b);
  if (v < 100) {
    const s = String(Math.trunc(a)), d = String(Math.trunc(v));
    v = num(s.slice(0, s.length - d.length) + d);
  }
  return v;
}

export function parseSignal(text, room) {
  const t = norm(text);
  if (!/\b(BUY|SELL|LONG|SHORT)\b/i.test(t)) return null;
  if (!/STOP\s*LOSS|\bSL\b/i.test(t)) return null;
  if (/weekly|summary|daily results|\bresults\b/i.test(t)) return null;  // recaps, not new trades
  const sym = symbolOf(t) || (room === "scalp" || room === "swing" || room === "rr" ? "XAUUSD" : null);
  if (!sym || sym === "OTHER") return null;
  const sideM = t.match(/\b(BUY|SELL|LONG|SHORT)\b/i);
  const side = { LONG: "buy", SHORT: "sell" }[sideM[1].toUpperCase()] || sideM[1].toLowerCase();

  // entry: "ENTRY…: a – b", "ENTRY: a//b", "XAUUSD BUY a/b", "BUY GOLD | a-b", "BUY NOW a-b", "BUY LIMIT: a"
  const N = "(\\d[\\d,]*(?:\\.\\d+)?)";
  const R = `${N}(?:\\s*(?:[-–]|\\/{1,2})\\s*${N})?`;
  const em =
    t.match(new RegExp(`(?:ENTRY(?:\\s*ZONE)?|LIMIT|BUY\\s*STOP|SELL\\s*STOP)[^:\\n]*:\\s*(?:(?:BUY|SELL)\\s*NOW|NOW)?\\s*\\(?\\s*${R}`, "i")) ||
    t.match(new RegExp(`\\b(?:BUY|SELL)\\b(?:\\s+(?:GOLD|XAUUSD|BTCUSD|NAS100))?(?:\\s+(?:NOW|LIMIT|STOP|AGAIN|HIGH ?RISK))*\\s*[|:@]?\\s*\\(?\\s*${R}`, "i"));
  const slm = t.match(/(?:STOP\s*LOSS|\bSL\b)\.?\s*[:@]?\s*@?\s*(\d[\d,]*(?:\.\d+)?)/i);
  let e1 = em ? num(em[1]) : null, e2 = em ? expand(e1, em[2]) : null, sl = slm ? num(slm[1]) : null;
  const plausible = (v) => v != null && (sym === "XAUUSD" ? v > 1500 && v < 9000 : v > 1000);
  if (!plausible(e1)) { e1 = null; e2 = null; }
  if (!plausible(e2)) e2 = null;
  if (!plausible(sl)) sl = null;
  if (!/ENTRY|LIMIT|STOP|NOW|\b(BUY|SELL)\b\s*(GOLD|XAUUSD)?\s*[|:@]?\s*\d/i.test(t)) return null;

  // risk in pips: an explicit "SL: 500 points / 50 pips" wins, else the far end of the entry zone to SL
  let risk = null;
  const ex = t.match(/SL:\s*(\d[\d,]*)\s*(?:[–-]\s*\d[\d,]*\s*)?(points|pts|pips)/i);
  if (ex) risk = num(ex[1]) / (/^p(oints|ts)$/i.test(ex[2]) || /pts|points/i.test(ex[2]) ? 10 : 1);
  else if (e1 != null && sl != null) risk = Math.max(Math.abs(e1 - sl), e2 != null ? Math.abs(e2 - sl) : 0) * pipsPerUnit(sym);
  if (risk != null && (risk <= 0 || risk > maxRisk(sym))) risk = null;
  return { symbol: sym, side, entry: e1, entry2: e2, sl, risk: risk == null ? null : Math.round(risk * 10) / 10 };
}

const AMOUNT = /([+-]?)\s*([\d,]+)\s*\+?\s*(pips|pip|points|point|pts)\b/gi;
function amounts(t) {
  const out = [];
  for (const m of t.matchAll(AMOUNT)) {
    let v = num(m[2]);
    if (/^p(oint|ts)/i.test(m[3])) v /= 10;
    out.push(m[1] === "-" ? -v : v);
  }
  return out;
}

// What a reply under a trade says: { kind: "tp" | "run" | "sl" | "be" | "cancel", pips }
export function parseResult(text) {
  const t = norm(text), low = t.toLowerCase();
  if (!t.trim()) return null;
  if (/\bcancel/.test(low)) return { kind: "cancel" };
  const tgt = t.match(/TARGET\s*(\d)\.?\s*HIT\s*(\d+)/i);
  if (tgt) return { kind: "tp", pips: num(tgt[2]) };
  const am = amounts(t);
  const notSl = /set|move|update|tight|keep|hasn|has not|not been|yet|ยังไม่/.test(low);
  if (!notSl && /(hit\s*sl|sl\s*hit|stop[- ]?loss (was )?hit|^\s*sl\s*$|^\s*sl\b.*\d+\s*(pips|pts|points)|sl\s*❌|^\s*❌|\bsl\s*-\s*\d)/m.test(low)) {
    const neg = am.map(Math.abs);
    return { kind: "sl", pips: neg.length ? Math.max(...neg) : null };
  }
  if (/\b(be|break-?even)\b.*\b(hit|count)|count\w*\b.{0,20}\bbe\b|hit\s+be|run\s+and\s+be\b|กินหน้าทุน/.test(low)) return { kind: "be" };
  const pos = am.filter((v) => v > 0);
  if (!pos.length) return null;
  if (/running/i.test(t)) return { kind: "run", pips: Math.max(...pos) };
  if (/\btp\s*\d|take profit|target|hit|done|full\s*tp|✅|✔/i.test(t)) return { kind: "tp", pips: Math.max(...pos) };
  return { kind: "run", pips: Math.max(...pos) };
}

// Fold a trade's replies into one result. trade = { tp, run, loss, be, cancel }
export function applyResult(trade, r) {
  const t = { tp: 0, run: 0, loss: null, be: false, cancel: false, ...trade };
  if (!r) return t;
  if (r.kind === "cancel") t.cancel = true;
  else if (r.kind === "tp") t.tp = Math.max(t.tp, r.pips || 0);
  else if (r.kind === "run") t.run = Math.max(t.run, r.pips || 0);
  else if (r.kind === "be") t.be = true;
  else if (r.kind === "sl") t.loss = r.pips != null ? r.pips : t.loss ?? -1;
  return t;
}

// -> { status: "win" | "loss" | "be" | "cancel" | "open", pips }
export function outcome(t, risk) {
  if (t.tp) return { status: "win", pips: Math.max(t.tp, t.run) };
  if (t.loss != null) return { status: "loss", pips: -(t.loss >= 0 ? t.loss : risk ?? 0) };
  if (t.run) return { status: "win", pips: t.run };
  if (t.be) return { status: "be", pips: 0 };
  if (t.cancel) return { status: "cancel", pips: null };
  return { status: "open", pips: null };
}
