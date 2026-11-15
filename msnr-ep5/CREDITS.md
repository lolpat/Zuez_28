# Credits

"MSNR KEY LEVELS 5/6: OCL": a chart explainer in the OTM glowing style, Instagram Reels only.
English version; the Thai version is `msnr-ep5-th` (same scene code, LANG = "th").

The MSNR series (episodes 0-6: the key levels; 7-11: storyline and timeframe alignment) is based on the ideas in
@x.droi's MSNR KEY guide and Storyline & Timeframe Alignment guide. The scripts, voice, charts and layout are original;
no pages were copied. This part: OCL (open close level): the open or close of a significant higher-timeframe candle (daily, session or news) where a major move started; large orders filled there, so price often reacts on the return.

Market: XAUUSD (gold) only. Candle colours: up #2962ff (blue), down white; candles are connected (each opens at the
previous close).
Charts: synthetic example data (work/msnr.py + work/specs.py). Not real market data and not a forecast.
Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Quentin - Narrator and Educator" (eleven_v4).
Timing: work/script.txt carries [key] marks; work/align.py matches the script to a faster-whisper transcript and
writes work/words.json and work/marks.json.
Sound effects: the earshot launch kit, soft sounds only (whoosh, swell, bell), low level, short fades.
Voice mix (work/mix.sh): de-esser, gentle compressor, static gain to -16 LUFS, limiter at -1 dBFS.
It ends on the next-part card (only part 5/5 of the storyline, msnr-ep11, has the Order the Market outro).

Rebuild: python3 work/align.py en && python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py,
then npx hyperframes@0.8.214 render

## Instagram captions

1. XAUUSD · OCL: the candle where the big move started. Price remembers that price 🎯 MSNR part 5/6.
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

2. XAUUSD · The open close level: mark the origin candle's open or close, then wait for the retest 📌
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

Optional credit line for either caption: "Concept: @x.droi's MSNR guide".
