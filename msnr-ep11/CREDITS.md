# Credits

"MSNR STORYLINE 5/5: The mistake + summary": a chart explainer in the OTM glowing style, Instagram Reels only.
English version; the Thai version is `msnr-ep11-th` (same scene code, LANG = "th").

The MSNR series (episodes 0-6: the key levels; 7-11: storyline and timeframe alignment) is based on the ideas in
@x.droi's MSNR KEY guide and Storyline & Timeframe Alignment guide. The scripts, voice, charts and layout are original;
no pages were copied. This part: The mistake: a rejection is often followed by a false breakout; the real breakout has to happen at the candle that tapped the key level first. Summary of what to avoid, and the rule: no storyline, no trade.

Market: XAUUSD (gold) only. Candle colours: up #2962ff (blue), down white; candles are connected (each opens at the
previous close).
Charts: synthetic example data (work/story.py). Not real market data and not a forecast.
Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Quentin - Narrator and Educator" (eleven_v4).
Timing: work/script.txt carries [key] marks; work/align.py matches the script to a faster-whisper transcript and
writes work/words.json and work/marks.json.
Sound effects: the earshot launch kit, soft sounds only (whoosh, swell, bell), low level, short fades.
Voice mix (work/mix.sh): de-esser, gentle compressor, static gain to -16 LUFS, limiter at -1 dBFS.
This is the last part of the whole MSNR series, so it ends on the Order the Market outro with the handles.

Rebuild: python3 work/align.py en && python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py,
then npx hyperframes@0.8.214 render

## Instagram captions

1. XAUUSD · The first break is often a trap 🪤 Wait for the real one. Storyline part 5/5.
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

2. XAUUSD · No storyline, no trade. The 5 mistakes to avoid with key levels 📌
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

Optional credit line for either caption: "Concept: @x.droi's MSNR guide".
