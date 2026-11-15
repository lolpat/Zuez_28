# Credits

"MSNR PRO 7/7: Trendlines + recap": a chart explainer in the OTM glowing style, Instagram Reels only.
Thai version; the English version is `msnr-pro-ep7` (same scene code, LANG = "en").

MSNR PRO is a 7-part follow-up to the OTM MSNR series, based on the ideas in a 7-lecture MSNR course on YouTube
(WINZWIK FX). The scripts, voice, charts and layout are original; nothing was copied from the lectures. This part: A trendline is only a confirmation at a key level: swing one with an engulfing candle, swing two with another engulfing candle and a break of structure, entry on the third touch; a broken line's retest is a trade too, and flat swings are drawn body to body. Ends with a recap and the Order the Market outro.

Market: XAUUSD (gold) only. Candle colours: up #2962ff (blue), down white; candles are connected (each opens at the
previous close). Thai versions keep the trading term names in English on screen.
Charts: synthetic example data (work/pro.py). Not real market data and not a forecast.
Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Patinya – Calm Thai Narrator & Explainer" (eleven_v4).
Timing: work/script.txt carries [key] marks; work/align.py (faster-whisper) writes work/words.json and work/marks.json,
with work/snapalign.py (pause-based) as the fallback when the transcript is unreliable.
Sound effects: the earshot launch kit, soft sounds only (whoosh, swell, bell), low level, short fades.
Voice mix (work/mix.sh): de-esser, gentle compressor, static gain to -16 LUFS, limiter at -1 dBFS.
This is the last part of MSNR PRO, so it ends on the Order the Market outro with the handles.

Rebuild: python3 work/align.py th && python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py,
then npx hyperframes@0.8.214 render

## Instagram captions

1. XAUUSD · เทรนด์ไลน์ไม่ใช่ ENTRY ด้วยตัวเอง แตะครั้งที่ 3 ที่ KEY LEVEL 📐 MSNR PRO 7/7 ตอนจบ
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

2. XAUUSD · ระดับแข็งแรง SL แคบ REFINE เส้นเดียว ENTRY ที่ยืนยันแล้ว นี่คือ MSNR PRO 📌
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket
