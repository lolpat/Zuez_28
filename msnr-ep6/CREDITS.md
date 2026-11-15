# Credits

"MSNR KEY LEVELS 6/6: QM": a chart explainer in the OTM glowing style, Instagram Reels only.
English version; the Thai version is `msnr-ep6-th` (same scene code, LANG = "th").

The MSNR series (episodes 0-6: the key levels; 7-11: storyline and timeframe alignment) is based on the ideas in
@x.droi's MSNR KEY guide and Storyline & Timeframe Alignment guide. The scripts, voice, charts and layout are original;
no pages were copied. This part: QM (Quasimodo): a structural reversal; in a bullish QM price makes a lower low, then breaks above the last high, and the level is the shoulder (the last swing low before that lower low). The bearish QM is the mirror. Ends with a recap of all six levels.

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

1. XAUUSD · Quasimodo: the shoulder price comes back to before it turns 🧠 MSNR part 6/6.
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

2. XAUUSD · Lower low, break of structure, back to the shoulder. That's the QM 📌
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

Optional credit line for either caption: "Concept: @x.droi's MSNR guide".
