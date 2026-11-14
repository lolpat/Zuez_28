# Credits

"CRT series, part 3/5: Entry, stop, target": a chart explainer in the OTM glowing style, Instagram Reels only.
English version; the Thai version is `otm-crt-ep3-th` (same scene file, LANG = "th").

The CRT series (5 parts, English and Thai) was inspired by a long candle range theory lesson; the scripts, charts and
layout are original. This part: On the 5-minute chart under a 4-hour range: the sweep of the CRT low and the close back inside, the shift above the last lower high, the fair value gap it leaves, the entry at the middle of the gap, the stop under the sweep wick, the target at the CRT high and a partial at the range 50%. Recap: sweep, shift, gap, entry.

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

1. Where does a CRT entry go? The middle of the fair value gap. Stop under the sweep wick, target the CRT high. Part 3/5 📌
   #forex #forextrading #priceaction #smartmoneyconcepts #OrderTheMarket

2. Sweep, shift, gap, entry. One 5-minute chart, the whole CRT trade plan. Part 3/5
   #forex #forextrading #priceaction #smartmoneyconcepts #OrderTheMarket
