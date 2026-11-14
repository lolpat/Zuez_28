# Credits

"Trade recap, 12 Nov 2026": an English Instagram Reel (about 65 s) recapping a real XAUUSD sell from the trader's own
screenshot (work/trade_screenshot.jpg): 3.8 lots, sold 3,953.83, stop 3,958.28, closed 3,938.83 at 14:33 on the 5-minute
chart, +15.00 per ounce = +$5,700, about 3.4R.

The idea, in the trader's words for this video: old support became resistance (SBR); a small dip on the way back up was
the inducement (IDM), with buyers' stops under it; the sell came where price stalled at the SBR line, the stop went
above the line, and price took out the IDM low and kept falling. The format was inspired by a Thai "Recap order XAUUSD"
reel; the script, chart and layout are original, and no material from that reel is used.

Chart: the entry, stop and close are the real prices. The candles between them are a simplified illustration of the move
(the video says "real entry, stop and close · candles simplified"). Candle colours: up #2962ff, down white.
Voice: ElevenLabs, "Quentin - Narrator and Educator" (eleven_v4). Timing: work/script.txt [key] marks aligned with
work/align.py. Voice mix (work/mix.sh): light de-esser, gentle compressor, one static gain to -16 LUFS, look-ahead
limiter. Sound effects: the earshot launch kit, soft sounds only (whoosh, swell, bell). Engine: work/otm.py (the CRT
series engine). Ends on the Order the Market outro with the handles and the educational-only line.

Rebuild: python3 work/align.py en && python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py, then
npx hyperframes@0.8.214 render

## Instagram captions

1. XAUUSD trade recap 📉 Sold gold at 3,953.83, stop 3,958.28, closed 3,938.83: +15.00, about 3.4R. Old support turned
   resistance, one inducement dip, then the drop. Not financial advice.
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

2. Level. Inducement. Entry. Stop. Then let price do the work. My gold sell from 12 Nov, step by step. Past results don't
   guarantee future ones.
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket
