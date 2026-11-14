# Credits

"CRT series, part 1/5: What is CRT": a chart explainer in the OTM glowing style, Instagram Reels only.
English version; the Thai version is `otm-crt-ep1-th` (same scene file, LANG = "th").

The CRT series (5 parts, English and Thai) was inspired by a long candle range theory lesson; the scripts, charts and
layout are original. This part: One higher-timeframe candle sets a range (the CRT high and low, with buy stops above and sell stops below). The next candles sweep one side, close back inside and deliver to the other side, fuelled by the trapped breakdown sellers' stops. Recap: range, sweep, delivery.

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

1. XAUUSD · One candle can map the next move 🕯️ Candle Range Theory in 3 steps: range, sweep, delivery. Part 1/5 of the CRT series.
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

2. XAUUSD · Why does price sweep the low and run to the high? Trapped sellers. Their stops are buy orders. CRT part 1/5 📌
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket
