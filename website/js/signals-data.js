// Signal results: the trade log of each signal room. Every number in the "Signal results" section is
// worked out from these lists, so keep them complete (losses included).
//
// One trade per line: [date "YYYY-MM-DD", symbol, "buy" | "sell", pips]   (pips: + for TP, - for SL)
// pipValue: US$ per pip for 1.0 lot, per symbol (gold 10 = $0.10 per pip at 0.01 lot).
// While a room's list is empty, the demo preview shows clearly labelled sample numbers and the live
// site shows "results coming soon".
window.OTM_SIGNALS = {
  updated: "",            // date of the last check, e.g. "2026-11-13"
  deduct: 0.15,           // spread / commission taken off the "if you had followed" money figures
  rooms: [
    { id: "swing", name: "Swing Elite", medal: 1, source: "Gold (XAUUSD)", pipValue: { XAUUSD: 10 }, trades: [] },
    { id: "scalp", name: "Scalping Pro", medal: 2, flash: true, source: "Gold (XAUUSD)", pipValue: { XAUUSD: 10 }, trades: [] },
    { id: "rr", name: "RR High Reward", medal: 3, source: "Gold (XAUUSD)", pipValue: { XAUUSD: 10 }, trades: [] },
    { id: "hype", name: "BTCUSD / NAS100", hype: true, source: "BTCUSD, NAS100", pipValue: { BTCUSD: 1, NAS100: 1 }, trades: [] }
  ]
};
