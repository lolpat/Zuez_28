# Credits

"CRT series, part 2/5: กวาดจริง กับ กวาดปลอม": a chart explainer in the OTM glowing style, Instagram Reels only.
Thai version: built from the same scene file as `otm-crt-ep2` with LANG = "th". All on-screen text is Thai (the outro keeps the brand lines in English).

The CRT series (5 parts, English and Thai) was inspired by a long candle range theory lesson; the scripts, charts and
layout are original. This part: The sweep is not the signal, the close is. Price drops under the CRT low and either (A) closes back inside: a real sweep, or (B) closes below: price accepting lower prices, and buying it gets stopped out. If neither side is taken there is no trade. The rule: no close back inside, no CRT.

Candle colours: up candles #2962ff (blue), down candles white.

Charts: synthetic example data (work/gen.py, seeded candles through hand-placed pivots). They are not real market data and
not a forecast.
Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Patinya – Calm Thai Narrator & Explainer" (eleven_v4), the same Thai voice as the other Thai OTM videos.
Timing: the script (work/script.txt) carries [key] marks; work/align.py matches the script to a faster-whisper
transcript of the voice (small, best of three decoding setups) and writes work/words.json and work/marks.json;
scenes key off K("key").
Font: Kanit by Cadson Demak, SIL Open Font License 1.1 (assets/fonts; licence in assets/fonts/OFL-Kanit.txt).
Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).
Engine: work/otm.py (shared by all ten CRT projects).

Rebuild: python3 work/align.py th && python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py,
then npx hyperframes@0.8.214 render

## Instagram captions

1. ไส้เทียนไม่ใช่สัญญาณ ราคาปิดต่างหาก กวาดจริง กับ กวาดปลอม ตอนที่ 2/5 📌
   #forex #forextrading #priceaction #smartmoneyconcepts #OrderTheMarket

2. ปิดใต้โลว์ ไม่ใช่การกวาด ไม่ปิดกลับเข้ากรอบ ก็ไม่ใช่ CRT ตอนที่ 2/5
   #forex #forextrading #priceaction #smartmoneyconcepts #OrderTheMarket
