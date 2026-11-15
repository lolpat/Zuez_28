# Credits

"MSNR PRO 6/7: The entry model": a chart explainer in the OTM glowing style, Instagram Reels only.
Thai version; the English version is `msnr-pro-ep6` (same scene code, LANG = "en").

MSNR PRO is a 7-part follow-up to the OTM MSNR series, based on the ideas in a 7-lecture MSNR course on YouTube
(WINZWIK FX). The scripts, voice, charts and layout are original; nothing was copied from the lectures. This part: Tap a higher-timeframe key level, drop exactly two timeframes lower, wait for a market structure shift closed by a candle body, mark and refine the levels of that leg to one, then a limit entry with the stop beyond the wick and the target at the next key level or liquidity; repeat on a new shift for a re-entry.

Market: XAUUSD (gold) only. Candle colours: up #2962ff (blue), down white; candles are connected (each opens at the
previous close). Thai versions keep the trading term names in English on screen.
Charts: synthetic example data (work/pro.py). Not real market data and not a forecast.
Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Patinya – Calm Thai Narrator & Explainer" (eleven_v4).
Timing: work/script.txt carries [key] marks; work/align.py (faster-whisper) writes work/words.json and work/marks.json,
with work/snapalign.py (pause-based) as the fallback when the transcript is unreliable.
Sound effects: the earshot launch kit, soft sounds only (whoosh, swell, bell), low level, short fades.
Voice mix (work/mix.sh): de-esser, gentle compressor, static gain to -16 LUFS, limiter at -1 dBFS.
It ends on the next-part card (only part 7/7 has the Order the Market outro).

Rebuild: python3 work/align.py th && python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py,
then npx hyperframes@0.8.214 render

## Instagram captions

1. XAUUSD · ENTRY MODEL 5 ขั้น: แตะ, ลง 2 TF, MSS, REFINE, LIMIT 🎯 MSNR PRO 6/7
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

2. XAUUSD · WICK ทะลุ ไม่ใช่ MSS รอปิดด้วยเนื้อเทียน 📌
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket
