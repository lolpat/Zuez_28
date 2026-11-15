# Credits

"MSNR ENTRY 4/4: Multi fresh": a chart explainer in the OTM glowing style, Instagram Reels only.
Thai version; the English version is `msnr-ep15` (same scene code, LANG = "en").

The MSNR series (episodes 0-6: the key levels; 7-11: storyline and timeframe alignment; 12-15: confirmation and entry)
is based on the ideas in @x.droi's MSNR KEY, Storyline & Timeframe Alignment and Confirmation Entry Model guides. The scripts, voice, charts and layout are original;
no pages were copied. This part: Multi fresh: with more than one fresh level, wait for an X4 confirmation or place a limit at the apex. The priority: QM, then the apex (Classic V or A), then SBR, RBS and OCL (equal). A gold example where the used QM is removed and the fresh RBS gives the entry.

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
This is the last part of the whole MSNR series, so it ends on the Order the Market outro with the handles.

Rebuild: python3 work/align.py th && python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py,
then npx hyperframes@0.8.214 render

## Instagram captions

1. XAUUSD · มีระดับสดสองระดับ เลือกอันไหน? QM ก่อน แล้วเอเพ็กซ์ 🎯 MSNR จุดเข้า ตอน 4/4 ตอนจบของซีรีส์
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

2. XAUUSD · พลาดเพราะรอยืนยัน? พอร์ตยังอยู่สำหรับเทรดถัดไป 📌
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

Optional credit line for either caption: "Concept: @x.droi's MSNR guide".
