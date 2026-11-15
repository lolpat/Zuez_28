# Credits

"MSNR STORYLINE 3/5: Rejection & breakout": a chart explainer in the OTM glowing style, Instagram Reels only.
Thai version; the English version is `msnr-ep9` (same scene code, LANG = "en").

The MSNR series (episodes 0-6: the key levels; 7-11: storyline and timeframe alignment; 12-15: confirmation and entry)
is based on the ideas in @x.droi's MSNR KEY, Storyline & Timeframe Alignment and Confirmation Entry Model guides. The scripts, voice, charts and layout are original;
no pages were copied. This part: Rejection or breakout: rejection signs (long wick, engulfing, displacement, lower-timeframe shift) and what makes a breakout real (a close beyond the level, many earlier tests, a squeeze first).

Market: XAUUSD (gold) only. Candle colours: up #2962ff (blue), down white; candles are connected (each opens at the
previous close).
Charts: synthetic example data (work/story.py). Not real market data and not a forecast.
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

1. XAUUSD · ที่ระดับราคา จะปฏิเสธหรือเบรก ทั้งคู่ต้องมีหลักฐาน ✅ สตอรี่ไลน์ตอน 3/5
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

2. XAUUSD · 4 สัญญาณการปฏิเสธ 3 สัญญาณเบรกจริง เซฟเช็กลิสต์นี้ไว้ 📌
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

Optional credit line for either caption: "Concept: @x.droi's MSNR guide".
