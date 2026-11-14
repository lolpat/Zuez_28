# Credits

"CRT series, part 2/5: Real sweep vs fake": a chart explainer in the OTM glowing style, Instagram Reels only.
English version; the Thai version is `otm-crt-ep2-th` (same scene file, LANG = "th").

The CRT series (5 parts, English and Thai) was inspired by a long candle range theory lesson; the scripts, charts and
layout are original. This part: The sweep is not the signal, the close is. Price drops under the CRT low and either (A) closes back inside: a real sweep, or (B) closes below: price accepting lower prices, and buying it gets stopped out. If neither side is taken there is no trade. The rule: no close back inside, no CRT.

Market: XAUUSD (gold) only; the series tag and the opening badge say so, and the prices on the level lines are
illustrative gold prices.
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

1. XAUUSD · The wick is not the signal. The close is. Real sweep vs fake sweep in CRT. Part 2/5 📌
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

2. XAUUSD · Closed below the low? That's not a sweep, that's acceptance. No close back inside, no CRT. Part 2/5
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket
