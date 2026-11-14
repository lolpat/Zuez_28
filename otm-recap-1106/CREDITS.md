# Credits

"Recap order XAUUSD, 6 Nov 2026": an English Instagram Reel (about 64 s) recapping real XAUUSD trades from the trader's
own screenshot (assets/trade.jpg, also kept as work/trade_screenshot.jpg): the MT5 deals list over his 15-minute chart,
with his own OB / SBR / CHoCH markings.

The deals, as shown in the screenshot:
- sell 6 lots 4,133.00 -> 4,036.63, +57,822.00 (closed 2026.11.06 15:31:50), at the order block
- sell 6 lots 4,115.00 -> 4,036.63, +47,022.00 (closed 15:31:50), at the SBR
- buy 6 lots 4,065.00 -> 4,061.00, -2,400.00 (03:30:12), stopped out
- Profit 102,444.00 (swap +371.04, balance 102,815.04)
The stops of the two sells are not in the screenshot, so the video shows no RR.

Layout: modelled on a Thai "Recap order XAUUSD" reel the trader shared (white slides, red italic title, one subtitle
line per beat, markings drawn on the real chart, a numbered summary). The script, voice, markings and layout code are
original; no material from that reel is used. Every chart slide is the trader's screenshot, marked "real trade, my own
screenshot". Overlays are placed in the screenshot's own pixels (price scale calibrated on the live-price line).

Voice: ElevenLabs, "Quentin - Narrator and Educator" (eleven_v4). Timing: work/script.txt [key] marks aligned with
work/align.py. Voice mix (work/mix.sh): light de-esser, gentle compressor, one static gain to -16 LUFS, look-ahead
limiter. Sound effects: the earshot launch kit, soft sounds only (whoosh, swell, bell). Ends on the Order the Market
outro with the handles and the educational-only line.

Rebuild: python3 work/align.py en && python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py, then
npx hyperframes@0.8.214 render

## Instagram captions

1. Recap order XAUUSD 📉 6 Nov: sold gold at the order block (4,133) and again at the SBR (4,115), closed both at
   4,036.63. One buy was stopped out (-2,400). Net +$102,444. Not financial advice.
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

2. Order block. SBR. Wait for the structure. Then let price do the work. My gold sells from 6 Nov, step by step. Past
   results don't guarantee future ones.
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket
