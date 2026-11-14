# Credits

"CRT series, part 4/5: จับคู่ไทม์เฟรม": a chart explainer in the OTM glowing style, Instagram Reels only.
Thai version: built from the same scene file as `otm-crt-ep4` with LANG = "th". All on-screen text is Thai (the outro keeps the brand lines in English).

The CRT series (5 parts, English and Thai) was inspired by a long candle range theory lesson; the scripts, charts and
layout are original. This part: The range and the entry live on different charts: a 4-hour range with a 5- or 15-minute entry, a daily range with a 1-hour entry. Too close and the sweep is noise; too far and you wait days. The classic mistake: on the 1-minute every small dip inside the range looks like a sweep, and buying them gets stopped. Only the sweep of the range's own low matters.

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

1. กรอบ 4H เข้าที่ 5M หรือ 15M กรอบรายวัน เข้าที่ 1H จับคู่ให้ถูก ไม่งั้นทุกการย่อจะดูเหมือนการกวาด CRT ตอนที่ 4/5 📌
   #forex #forextrading #priceaction #smartmoneyconcepts #OrderTheMarket

2. ลงไปดูกราฟ 1 นาที? โลว์เล็กๆ แทบไม่มีสต็อปข้างใต้ สำคัญแค่โลว์ของกรอบ ตอนที่ 4/5
   #forex #forextrading #priceaction #smartmoneyconcepts #OrderTheMarket
