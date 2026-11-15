# Credits

"MSNR ENTRY 1/4: Confirmation": a chart explainer in the OTM glowing style, Instagram Reels only.
Thai version; the English version is `msnr-ep12` (same scene code, LANG = "en").

The MSNR series (episodes 0-6: the key levels; 7-11: storyline and timeframe alignment; 12-15: confirmation and entry)
is based on the ideas in @x.droi's MSNR KEY, Storyline & Timeframe Alignment and Confirmation Entry Model guides. The scripts, voice, charts and layout are original;
no pages were copied. This part: Confirmation: every trade is a confirmation plus an entry, kept separate so setups are easy to journal and backtest. The three confirmation types: gap break, market structure shift, trendline break. A confirmation only counts at a fresh key level.

Market: XAUUSD (gold) only. Candle colours: up #2962ff (blue), down white; candles are connected (each opens at the
previous close).
Charts: synthetic example data (work/story.py). Not real market data and not a forecast.
Thai versions keep the trading term names (CLASSIC V, SBR, FRESH, BREAKOUT, LIQUIDITY ...) in English on screen.
Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Patinya – Calm Thai Narrator & Explainer" (eleven_v4).
Timing: work/script.txt carries [key] marks; work/align.py matches the script to a faster-whisper transcript and
writes work/words.json and work/marks.json.
Sound effects: the earshot launch kit, soft sounds only (whoosh, swell, bell), low level, short fades.
Voice mix (work/mix.sh): de-esser, gentle compressor, static gain to -16 LUFS, limiter at -1 dBFS.
It ends on the next-part card (only the last part, msnr-ep15, has the Order the Market outro).

Rebuild: python3 work/align.py th && python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py,
then npx hyperframes@0.8.214 render

## Instagram captions

1. XAUUSD · ยืนยันก่อน แล้วค่อยเข้า ✅ แก๊ปเบรก MSS เบรกเทรนด์ไลน์ MSNR จุดเข้า ตอน 1/4
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

2. XAUUSD · การยืนยันที่ไม่ได้เกิดที่ระดับสำคัญ เป็นแค่สัญญาณรบกวน นี่คือ 3 แบบที่นับได้ 📌
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

Optional credit line for either caption: "Concept: @x.droi's MSNR guide".
