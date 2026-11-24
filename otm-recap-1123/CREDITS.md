# Credits

"Recap order XAUUSD, 23 Nov 2026": an English Instagram Reel (about 82 s) recapping two real XAUUSD trades from the trader's own
screenshots and markings:
- assets/h4.png: their 4H chart: the CRT range candle (CRH 3,587 / CRL 3,520) and the next 4H candle sweeping the
  CRL and closing back inside. They zoomed into the 30M for the entry.
- assets/m30.png: their 30M chart with CRH / CRL, the sweep, a long position tool (entry 3,503.93, SL 3,500.05,
  TP 3,587 = CRH) and a short position tool (entry 3,690, SL 3,697.137, TP 3,630)
- assets/account.jpg: MT5 history, buy 15 @ 3504.00 -> 3587.00, +124,500.00 (closed 2026.11.23 01:31:00), and the
  an earlier account summary (not used).
- assets/account2.jpg: the account summary after both trades: deposit 100.00, credit 20.00, withdrawal -150,000.00,
  profit 285,850.36. Shown at the trader's request, rows Deposit to Profit only: the screenshot's Balance row
  (285,950.36) does not net the withdrawal, so it is cropped out.
- assets/sell.jpg: sell 8 @ 3690.00 -> 3630.00, +48,000.00 (closed 2026.11.23 21:37:41)

Together +172,500.00 on the day. CRL 3,520 is read from the 4H and 30M charts (both put it at 3,520.3).

Layout: same as otm-recap-1106 / 1116 (white slides, red italic "Recap order XAUUSD" title, one subtitle line per beat,
markings drawn on the real chart, a numbered summary). Overlays are placed in the screenshot's own pixels (30M price
scale from the axis: CRH 3,587 at y 1700, 7.186 px per dollar).

Voice: ElevenLabs, "Quentin - Narrator and Educator" (eleven_v4). Timing: work/script.txt [key] marks aligned with
work/align.py (marks snapped to the real pauses). The total-profit line was re-voiced
after the update (same voice and model) and spliced into the take at the same loudness; so were the two lines that
move the CRT to the 4H ("First, a C.R.T. on the four-hour." and "The next four-hour candle swept below the range low,
and closed back inside. So I zoomed into the thirty-minute,"). Voice mix (work/mix.sh): light de-esser, gentle compressor, one static gain to -16 LUFS, look-ahead
limiter. No music. Sound effects: the earshot launch kit, soft sounds only (whoosh, swell, bell). Ends on the Order the
Market outro with the handles and the educational-only line.

Rebuild: python3 work/align.py en && python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py, then
npx hyperframes@0.8.214 render

## Instagram captions

1. Recap order XAUUSD 📈📉 23 Nov: a 4H CRT buy, entry on the 30M, from the sweep below the range low to the range high (+$124,500), then a
   sell from my zone at 3,690 (+$48,000). +$172,500 on the day. Not financial advice.
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

2. Wait for the sweep. Buy the range low. Target the range high. From a $100 deposit to $285K in total profit, with
   $150K already withdrawn. Past results don't guarantee future ones.
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

## TikTok captions

1. Gold 4H CRT trade: sweep below the range low, zoom to the 30M, buy, target the range high. +$172,500 on two trades 📈 Not financial advice.
   #forex #xauusd #goldtrading #OrderTheMarket

2. XAUUSD recap: from a $100 deposit to $285K total profit, $150K withdrawn. Past results don't guarantee future ones.
   #forex #xauusd #goldtrading #OrderTheMarket
