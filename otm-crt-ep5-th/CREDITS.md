# Credits

"CRT series, part 5/5: เช็กลิสต์ CRT": a chart explainer in the OTM glowing style, Instagram Reels only.
Thai version: built from the same scene file as `otm-crt-ep5` with LANG = "th". All on-screen text is Thai (the outro keeps the brand lines in English).

The CRT series (5 parts, English and Thai) was inspired by a long candle range theory lesson; the scripts, charts and
layout are original. This part: Five boxes before every CRT trade: a higher-timeframe candle sets the range, price sweeps one side, a candle closes back inside, the lower timeframe shifts with the entry at the middle of the fair value gap, stop beyond the wick and target the other side. Miss one box and there's no trade. Save it, and tell me which pair you use in the comments.

Market: XAUUSD (gold) only; the series tag and the opening badge say so, and the prices on the level lines are
illustrative gold prices.
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

1. XAUUSD · เช็กลิสต์ CRT 5 ข้อ ก่อนเข้าเทรดทุกครั้ง ขาดข้อไหน ไม่มีเทรด เซฟไว้ 📌 ตอนที่ 5/5
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

2. XAUUSD · คุณใช้คู่ไหน 4H กับ 5M หรือรายวันกับ 1H? บอกกันในคอมเมนต์ 👇 ซีรีส์ CRT ตอนที่ 5/5
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket
