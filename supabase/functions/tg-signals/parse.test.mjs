// node supabase/functions/tg-signals/parse.test.mjs  — checks the reader against the rooms' real message formats.
import assert from "node:assert/strict";
import { parseSignal, parseResult, applyResult, outcome, parseTargets, mentionedSymbol } from "./parse.js";

const sig = (t, room = "rr") => parseSignal(t, room);
const res = (t) => parseResult(t);

// signals
assert.deepEqual(sig("🥇 SWING ELITE\n\n#XAUUSD BUY\nENTRY: 3978//3968\n\n🎯 TP1: @ 3982\nTP6: @ 4900\n\n🛑 SL: @ 3958", "swing"),
  { symbol: "XAUUSD", side: "buy", entry: 3978, entry2: 3968, sl: 3958, risk: 200 });
assert.equal(sig("XAUUSD BUY 4261/4251\n\nTP1. @ 4265\nTP6. @ 4800\n\nSL     @ 4241", "swing").risk, 200);
assert.equal(sig("⚡ OTM SCALPING PRO\n\n🟢 BUY NOW\n\n📍 ENTRY ZONE: 4053–4056\n🛑 STOP LOSS: 4052\n\n🎯 TAKE PROFIT: 4063", "scalp").risk, 40);
assert.equal(sig("📊 XAUUSD SHORT\n⏰ Timeframe: 30M\n\n🔻 SHORT/SELL ENTRY: 4097\n🛑 STOP LOSS: 4102\n\nSL: 500 points / 50 pips").side, "sell");
assert.equal(sig("📊 XAUUSD SHORT\n🔻 SHORT/SELL ENTRY: 4097\n🛑 STOP LOSS: 4102\nSL: 500 points / 50 pips").risk, 50);
assert.equal(sig("🪎 XAUUSD\n\n🔹 BUY ENTRY: 4048.13\n🛑 STOP LOSS: 4044.54").risk, 35.9);
assert.equal(sig("SELL NOW 5160-62 SL 5164 TP 5155 TP 5152", "scalp").entry2, 5162);
assert.equal(sig("BUY GOLD | 4564-63 ▪️SL: 4561.5 ▫️TP: 4580", "scalp").risk, 25);
assert.equal(sig("💰 BTCUSD 💰SHORT🔽\n🔽SHORT/SELL ENTRY: 84740\n🛑 STOP LOSS: 85600\nSL: 860 points").symbol, "BTCUSD");
assert.equal(sig("1. BUY EURUSD NOW 1.18700 SL 1.18525 TP 1.19150", "scalp"), null);          // not a room instrument
assert.equal(sig("✨ OTM 🥇 SWING ELITE WEEKLY SUMMARY\n#MONDAY\n💰 Won: +650 PIPS\n❌ SL: -0 PIPS", "swing"), null);
assert.equal(sig("GOLD BUY RUNNING 320+Pips Profit", "swing"), null);

// results
assert.deepEqual(res("#XAUUSD\nTARGET3 HIT 120+PIPS PROFIT DONE"), { kind: "tp", pips: 120 });
assert.deepEqual(res("𝗚𝗢𝗟𝗗 BUY 𝗥𝗨𝗡𝗡𝗜𝗡𝗚 320+𝗣𝗶𝗽𝘀 𝗣𝗿𝗼𝗳𝗶𝘁"), { kind: "run", pips: 320 });
assert.deepEqual(res("TP 1 ✔️ +80pips"), { kind: "tp", pips: 80 });
assert.deepEqual(res("+50 pips"), { kind: "run", pips: 50 });
assert.deepEqual(res("hit sl -40pips"), { kind: "sl", pips: 40 });
assert.deepEqual(res("The stop loss was hit: -30 pips."), { kind: "sl", pips: 30 });
assert.deepEqual(res("✅ +600 POINTS TP1 — Confidently hit with OTM 💸"), { kind: "tp", pips: 60 });
assert.equal(res("Break-even hit.").kind, "be");
assert.equal(res("Buy +30pips but I will count this as BE").kind, "be");
assert.equal(res("Cancel").kind, "cancel");
assert.equal(res("SL hasn’t been hit yet."), null);
assert.equal(res("Set Breakeven now at lower part"), null);

// folding a trade
let t = {};
for (const m of ["+28pips", "ไม่TP ผมนับ SLนะ", "SL hit -30pips"]) t = applyResult(t, res(m));
assert.deepEqual(outcome(t, 40), { status: "loss", pips: -30 });               // floating profit, then SL: a loss
t = {};
for (const m of ["TARGET1 HIT 40+PIPS PROFIT DONE", "GOLD BUY RUNNING 110+Pips Profit", "BE HIT"]) t = applyResult(t, res(m));
assert.deepEqual(outcome(t, 200), { status: "win", pips: 110 });                // TP reached first, then BE: a win
assert.deepEqual(outcome(applyResult({}, res("Cancel")), 50), { status: "cancel", pips: null });
// Pomilon PML Lab format
assert.equal(sig("[ 17-11-2026 ] 📉SELL XAUUSD | Now SL: 3877.42 [ 345 POINTs ] TP 3868.80").risk, 34.5);
assert.deepEqual(res("✅+1,380 POINTs TP1/2 แบ่งค้าบ"), { kind: "tp", pips: 138 });
assert.equal(res("แหก❌").kind, "sl");
assert.equal(res("ไม้นี้ไม่เอานะครับยกเลย").kind, "cancel");
assert.deepEqual(outcome(applyResult({}, res("เก็บ Full Tp 3812")), 35.8, 3865.04), { status: "win", pips: 530 });
assert.deepEqual(res("✅+2700 แล้วTP1/2/3"), { kind: "tp", pips: 270 });
// take-profit prices
const tps = (t, room = "rr") => parseTargets(t, parseSignal(t, room));
assert.deepEqual(tps("🥇 SWING ELITE\n\n#XAUUSD Sell\nENTRY: 3590//3600\n\n🎯 TP1: @ 3486\nTP2: @ 3582\nTP3: @ 3578\nTP4: @ 3574\nTP5: @ 3570\nTP6: @ 3000\n\n🛑 SL: @ 3610", "swing"),
  [3486, 3582, 3578, 3574, 3570, 3000]);
assert.deepEqual(tps("XAUUSD BUY 4261/4251\n\nTP1. @ 4265\nTP6. @ 4800\n\nSL     @ 4241", "swing"), [4265, 4800]);
assert.deepEqual(tps("⚡ OTM SCALPING PRO\n\n🟢 BUY NOW\n\n📍 ENTRY ZONE: 4053–4056\n🛑 STOP LOSS: 4052\n\n🎯 TAKE PROFIT: 4063", "scalp"), [4063]);
assert.deepEqual(tps("SELL NOW 5160-62 SL 5164 TP 5155 TP 5152", "scalp"), [5155, 5152]);
assert.deepEqual(tps("BUY GOLD | 4564-63 ▪️SL: 4561.5 ▫️TP: 4580", "scalp"), [4580]);
assert.deepEqual(tps("[ 17-11-2026 ] 📉SELL XAUUSD | Now SL: 3877.42 [ 345 POINTs ] TP 3868.80"), [3868.8]);   // no entry price: TP kept as posted
assert.deepEqual(parseTargets("BUY GOLD 4000 SL 3990 TP 3980 TP 4010", parseSignal("BUY GOLD 4000 SL 3990", "scalp")), [4010]);   // wrong-side TP dropped
// "Stop Loss (SL): …" (BTCUSD room)
const btc = sig("🚨 BTCUSD SELL SIGNAL 🔴\n\n🔴 Direction: SELL NOW\n💰 Entry: 61,300\n🛑 Stop Loss (SL): 61,800\n\n🎯 Take Profit: 60,500", "hype");
assert.equal(btc.sl, 61800); assert.equal(btc.entry, 61300); assert.equal(btc.risk, 50);
assert.equal(sig("🚨 BTCUSD SELL SIGNAL 🔴\n\n🔴 Direction: SELL\n💰 Entry: 60,260\n🛑 SL: 60,570\n\n🎯 Take Profit: 59,000", "hype").risk, 31);
// "hit -50pips" (no "SL" in the text) is a stop loss
assert.deepEqual(res("hit -50pips"), { kind: "sl", pips: 50 });
assert.deepEqual(res("+43pips"), { kind: "run", pips: 43 });
// a missed entry counts as cancelled; a TP posted before it still wins
assert.deepEqual(res("Missed entry"), { kind: "cancel" });
assert.deepEqual(res("Fuck we missed 😭"), { kind: "cancel" });
assert.deepEqual(res("Lottery — not in time, 10 sec SL"), { kind: "cancel" });
assert.deepEqual(res("เข้าไม่ทัน"), { kind: "cancel" });
assert.deepEqual(outcome(applyResult(applyResult({}, res("✅ +600 POINTS TP1")), res("Missed entry")), 35), { status: "win", pips: 60 });
// results posted on their own
assert.deepEqual(res("BTCUSD ENDED WITH 1500points 4.8RR"), { kind: "run", pips: 150 });
assert.equal(mentionedSymbol("BTCUSD ENDED WITH 1500points 4.8RR"), "BTCUSD");
assert.equal(mentionedSymbol("Full TP let's close 50%"), null);
// the OTM SCALPING PRO format from the Junction forwarder: every TP in a list, short TPs expanded
{
  const otm = "⚡ OTM SCALPING PRO\n🏆 | XAUUSD\n\n🔴 SELL NOW\n\n📍 ENTRY ZONE: 3785–3786\n🛑 STOP LOSS: 3789\n\n🎯 TAKE PROFIT: 3780 / 3774 / 3765\n🚀 RUNNER: Let profits run\n\nFor educational purposes only.";
  const s = parseSignal(otm);
  assert.equal(s.side, "sell"); assert.equal(s.sl, 3789);
  assert.deepEqual(parseTargets(otm, s), [3780, 3774, 3765]);
  const short = "SELL NOW 3785-86 / SL 3789 / TP 3780-74-65 / RUN";
  assert.deepEqual(parseTargets(short, parseSignal(short, "scalp")), [3780, 3774, 3765]);
}
assert.deepEqual(res("Break-even"), { kind: "be" });
assert.deepEqual(res("BE hit"), { kind: "be" });
assert.equal(res("Move SL to break-even"), null);
assert.deepEqual(res("SL hit -50 pips"), { kind: "sl", pips: 50 });
{
  const b = "🚨 BTCUSD SELL SIGNAL 🔴\n🔴 Direction: SELL NOW\n💰 Entry: 61,300\n🛑 Stop Loss (SL): 61,800\n🎯 Take Profit (TP): 59,000\n";
  assert.deepEqual(parseTargets(b, parseSignal(b, "hype")), [59000]);
}
console.log("parse.js: all checks passed");
