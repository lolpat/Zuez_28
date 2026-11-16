# Credits

"Recap order XAUUSD, 16 Nov 2026": an English Instagram Reel (about 80 s) recapping a real XAUUSD buy, from a plan made
on 12 Nov, built from the trader's own screenshots and their own markings:
- assets/plan2h.jpg: the 2H plan, 12/11/2026 (BSL 3,955.50, SSL 3,866.37, BUY ZONE 3,847.65 / 3,843.64 OC / 3,840.52, SL 3,830.72)
- assets/h4.png: the 4H, 16/11/2026 (SSL swept, price into the zone, 50% wick 3,841.99)
- assets/m5.jpg: the 5M, 16/11/2026 (the tap of the 50% wick at 3,842.33 and the run back up to the SSL)
- assets/positions.jpg: MT5 positions, still open at 3,865.92

The positions (floating, not closed):
- buy 3 lots @ 3,851.99, +4,179.00
- buy 4.8 lots @ 3,846.61, +9,268.80
- buy 4.8 lots @ 3,842.50 (main, on the 50% wick), +11,241.60
- together +24,689.40 floating; target BSL 3,955.50, SL 3,830.72
The trader missed their CRT fib entry (asleep) and used three buy limits around the 50% wick instead.

Layout: same as otm-recap-1106 (white slides, red italic "Recap order XAUUSD" title, one subtitle line per beat,
markings drawn on the real charts, a numbered summary). Every chart slide is the trader's screenshot, marked "real
trade, my own screenshot and markings". Overlays are placed in each screenshot's own pixels (price scale calibrated on
two drawn level lines per screenshot). The buy-limit ladder slide is drawn from the position prices.

Voice: ElevenLabs, "Quentin - Narrator and Educator" (eleven_v4). Timing: work/script.txt [key] marks aligned with
work/align.py (l1, l2 and pnl snapped to the real pauses). Voice mix (work/mix.sh): light de-esser, gentle compressor,
one static gain to -16 LUFS, look-ahead limiter. No music. Sound effects: the earshot launch kit, soft sounds only
(whoosh, swell, bell). Ends on the Order the Market outro with the handles and the educational-only line.

Rebuild: python3 work/align.py en && python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py, then
npx hyperframes@0.8.214 render

## Instagram captions

1. Recap order XAUUSD 📈 Planned on 12 Nov, filled on 16 Nov: three buy limits in my 2H OC zone, the main one on the
   50% wick. +$24,689 floating, target still above. Not financial advice.
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

2. Missed my CRT fib entry (I was asleep 😅), so I let buy limits do the work instead. Plan early. Mark the zone. Set
   your limits. Past results don't guarantee future ones.
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

## TikTok captions

1. Gold trade recap: plan on the 2H, buy limits at the 50% wick, +$24,689 floating 📈 Not financial advice.
   #forex #xauusd #goldtrading #OrderTheMarket

2. XAUUSD buy limits: I slept through my entry, my limits didn't 😅 Plan early, let price come to you.
   #forex #xauusd #goldtrading #OrderTheMarket
