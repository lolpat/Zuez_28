# Credits

"MSNR ENTRY 3/4: Single fresh": a chart explainer in the OTM glowing style, Instagram Reels only.
Thai version; the English version is `msnr-ep14` (same scene code, LANG = "en").

The MSNR series (episodes 0-6: the key levels; 7-11: storyline and timeframe alignment; 12-15: confirmation and entry)
is based on the ideas in @x.droi's MSNR KEY, Storyline & Timeframe Alignment and Confirmation Entry Model guides. The scripts, voice, charts and layout are original;
no pages were copied. This part: The entry: only trade fresh key levels. With one fresh level on X3, place a limit on it; with none, there is no trade today. Stop placement for a limit versus an X4 confirmation, and why confirmation only counts at the key level.

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

1. XAUUSD · มีระดับสดเดียว? ตั้งลิมิต ไม่มีเลย? วันนี้ไม่เทรด 😌 MSNR จุดเข้า ตอน 3/4
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

2. XAUUSD · ระดับที่ใช้แล้ว ไม่ใช่จุดเข้า อธิบายกฎระดับสดเดียว 📌
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

Optional credit line for either caption: "Concept: @x.droi's MSNR guide".
