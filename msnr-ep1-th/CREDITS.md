# Credits

"MSNR KEY LEVELS 1/6: Classic V": a chart explainer in the OTM glowing style, Instagram Reels only.
Thai version; the English version is `msnr-ep1` (same scene code, LANG = "en").

The MSNR series (episodes 0-6: the key levels; 7-11: storyline and timeframe alignment) is based on the ideas in
@x.droi's MSNR KEY guide and Storyline & Timeframe Alignment guide. The scripts, voice, charts and layout are original;
no pages were copied. This part: Classic V: a support level; price drops, sweeps the liquidity below and snaps back up in a V. The key level is the close of the last bearish candle and the open of the first bullish candle.

Market: XAUUSD (gold) only. Candle colours: up #2962ff (blue), down white; candles are connected (each opens at the
previous close).
Charts: synthetic example data (work/msnr.py + work/specs.py). Not real market data and not a forecast.
Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Patinya – Calm Thai Narrator & Explainer" (eleven_v4).
Timing: work/script.txt carries [key] marks; work/align.py matches the script to a faster-whisper transcript and
writes work/words.json and work/marks.json.
Sound effects: the earshot launch kit, soft sounds only (whoosh, swell, bell), low level, short fades.
Voice mix (work/mix.sh): de-esser, gentle compressor, static gain to -16 LUFS, limiter at -1 dBFS.
It ends on the next-part card (only part 5/5 of the storyline, msnr-ep11, has the Order the Market outro).

Rebuild: python3 work/align.py th && python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py,
then npx hyperframes@0.8.214 render

## Instagram captions

1. XAUUSD · Classic V: จุดที่ราคากลับตัว ระดับคือราคาปิด ไม่ใช่ไส้ 🕯️ MSNR ตอน 1/6
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

2. XAUUSD · วิธีวาดระดับ Classic V ในสิบวินาที เซฟไว้ใช้ครั้งหน้า 📌
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

Optional credit line for either caption: "Concept: @x.droi's MSNR guide".
