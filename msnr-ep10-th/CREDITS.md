# Credits

"MSNR STORYLINE 4/5: Four timeframes": a chart explainer in the OTM glowing style, Instagram Reels only.
Thai version; the English version is `msnr-ep10` (same scene code, LANG = "en").

The MSNR series (episodes 0-6: the key levels; 7-11: storyline and timeframe alignment; 12-15: confirmation and entry)
is based on the ideas in @x.droi's MSNR KEY, Storyline & Timeframe Alignment and Confirmation Entry Model guides. The scripts, voice, charts and layout are original;
no pages were copied. This part: The four timeframes: X1 finds the fresh level and the rejection, X2 the breakout and entry level, X3 refines the setup, X4 (optional) tightens the entry. When X1-X3 line up, a limit order can sit at the X3 level.

Market: XAUUSD (gold) only. Candle colours: up #2962ff (blue), down white; candles are connected (each opens at the
previous close).
Charts: synthetic example data (work/story.py). Not real market data and not a forecast.
Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Patinya – Calm Thai Narrator & Explainer" (eleven_v4).
Timing: work/script.txt carries [key] marks; work/align.py matches the script to a faster-whisper transcript and
writes work/words.json and work/marks.json.
Sound effects: the earshot launch kit, soft sounds only (whoosh, swell, bell), low level, short fades.
Voice mix (work/mix.sh): de-esser, gentle compressor, static gain to -16 LUFS, limiter at -1 dBFS.
It ends on the next-part card (only the last part, msnr-ep15, has the Order the Market outro).

Rebuild: python3 work/align.py th && python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py,
then npx hyperframes@0.8.214 render

## Instagram captions

1. XAUUSD · X1 X2 X3 X4: หนึ่งสตอรี่ไลน์ บนสี่ไทม์เฟรม ⏱️ สตอรี่ไลน์ตอน 4/5
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

2. XAUUSD · รายสัปดาห์ปฏิเสธ รายวันเบรก 4H เซ็ตอัพ แล้วค่อยตั้งลิมิต 📌
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

Optional credit line for either caption: "Concept: @x.droi's MSNR guide".
