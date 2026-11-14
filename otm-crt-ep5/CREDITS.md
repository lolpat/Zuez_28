# Credits

"CRT series, part 5/5: The CRT checklist": a chart explainer in the OTM glowing style, Instagram Reels only.
English version; the Thai version is `otm-crt-ep5-th` (same scene file, LANG = "th").

The CRT series (5 parts, English and Thai) was inspired by a long candle range theory lesson; the scripts, charts and
layout are original. This part: Five boxes before every CRT trade: a higher-timeframe candle sets the range, price sweeps one side, a candle closes back inside, the lower timeframe shifts with the entry at the middle of the fair value gap, stop beyond the wick and target the other side. Miss one box and there's no trade. Save it, and tell me which pair you use in the comments.

Candle colours: up candles #2962ff (blue), down candles white.

Charts: synthetic example data (work/gen.py, seeded candles through hand-placed pivots). They are not real market data and
not a forecast.
Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Quentin - Narrator and Educator" (eleven_v4), the same calm teaching read as the other OTM videos.
Timing: the script (work/script.txt) carries [key] marks; work/align.py matches the script to a faster-whisper
transcript of the voice (small.en, best of three decoding setups) and writes work/words.json and work/marks.json;
scenes key off K("key").
Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).
Engine: work/otm.py (shared by all ten CRT projects).

Rebuild: python3 work/align.py en && python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py,
then npx hyperframes@0.8.214 render

## Instagram captions

1. The CRT checklist: 5 boxes before every trade. Miss one, no trade. Save this 📌 Part 5/5
   #forex #forextrading #priceaction #smartmoneyconcepts #OrderTheMarket

2. Which pair do you use: 4H into 5M, or daily into 1H? Tell me in the comments 👇 CRT series, part 5/5
   #forex #forextrading #priceaction #smartmoneyconcepts #OrderTheMarket
