# Credits

"CRT series, part 4/5: Timeframe pairs": a chart explainer in the OTM glowing style, Instagram Reels only.
English version; the Thai version is `otm-crt-ep4-th` (same scene file, LANG = "th").

The CRT series (5 parts, English and Thai) was inspired by a long candle range theory lesson; the scripts, charts and
layout are original. This part: The range and the entry live on different charts: a 4-hour range with a 5- or 15-minute entry, a daily range with a 1-hour entry. Too close and the sweep is noise; too far and you wait days. The classic mistake: on the 1-minute every small dip inside the range looks like a sweep, and buying them gets stopped. Only the sweep of the range's own low matters.

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

1. XAUUSD · 4H range into 5M or 15M. Daily range into 1H. Pair your timeframes right, or every dip looks like a sweep. CRT part 4/5 📌
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

2. XAUUSD · Dropping to the 1-minute? Those tiny dips have almost no stops under them. Only the range's own low matters. Part 4/5
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket
