// Autotrade members shown on the Leaderboard's "Autotrade (simulated)" tab.
// Each line must be the member's REAL Autotrade settings: the lot they copy with and the day they started.
// The page multiplies the signal rooms' real closed results by that lot from that day on, and labels every
// figure as simulated. Do not invent lots or dates: a member without real settings stays off this list.
//   { name: "Somchai K.", lot: 0.5, start: "2026-09-01", rooms: ["swing", "scalp", "rr", "hype"] }
// rooms is optional (default: the rooms below).
window.OTM_AUTOTRADE = {
  rooms: ["swing", "scalp", "rr", "hype"],   // rooms the group's Autotrade copies
  deduct: 0.15,                              // spread / commission taken off, as on the signal results
  members: []
};
