# Credits

"Recap order XAUUSD, 6 Nov 2026": an English Instagram Reel (about 59 s) recapping real XAUUSD trades from the trader's
own screenshots: their 15-minute chart (assets/trade.jpg, also kept as work/trade_screenshot.jpg) and their MT5 deals,
with their own SHIFT / FVG / SBR / PDH / IDM / BoS markings.

The deals (assets/deals.jpg, also kept as work/deals_screenshot.jpg; both closed 2026.11.06 15:31:50):
- sell 6 lots 4,133.00 -> 4,036.63, +57,822.00 (sell #1, under the high)
- sell 6 lots 4,115.00 -> 4,036.63, +47,022.00 (sell #2, at their SBR)
- together +104,844.00
The chart (assets/trade.jpg) carries their own SHIFT, FVG, SBR, PDH, IDM and BoS markings. The stops of the two sells are
not given, so the video shows no RR.

Layout: modelled on a Thai "Recap order XAUUSD" reel the trader shared (white slides, red italic title, one subtitle
line per beat, markings drawn on the real chart, a numbered summary). The script, voice, markings and layout code are
original; no material from that reel is used. Every chart slide is the trader's screenshot, marked "real trade, my own
screenshot". Overlays are placed in the screenshot's own pixels (price scale calibrated on the two entry lines).

Voice: ElevenLabs, "Quentin - Narrator and Educator" (eleven_v4). Timing: work/script.txt [key] marks aligned with
work/align.py. Voice mix (work/mix.sh): light de-esser, gentle compressor, one static gain to -16 LUFS, look-ahead
limiter. Sound effects: the earshot launch kit, soft sounds only (whoosh, swell, bell). Ends on the Order the Market
outro with the handles and the educational-only line.

Rebuild: python3 work/align.py en && python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py, then
npx hyperframes@0.8.214 render

## Instagram captions

1. Recap order XAUUSD 📉 6 Nov: sold gold under the high (4,133) and again at the SBR (4,115), closed both at the low,
   4,036.63. Two sells, +$104,844. Not financial advice.
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

2. Shift. SBR. Inducement. Target the low. Then let price do the work. My two gold sells from 6 Nov, step by step. Past
   results don't guarantee future ones.
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket
