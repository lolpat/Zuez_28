# Credits

"MSNR PRO 2/7: The 50% wick": a chart explainer in the OTM glowing style, Instagram Reels only.
Thai version; the English version is `msnr-pro-ep2` (same scene code, LANG = "en").

MSNR PRO is a 7-part follow-up to the OTM MSNR series, based on the ideas in a 7-lecture MSNR course on YouTube
(WINZWIK FX). The scripts, voice, charts and layout are original; nothing was copied from the lectures. This part: When the level's candle has a long wick, mark the wick's 50% and place the stop just beyond it instead of beyond the tip; same entry and target, about 1:1.9 becomes about 1:3.6 in the example.

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

1. XAUUSD · WICK ยาว SL กว้าง? ใช้ 50% ของ WICK ✂️ MSNR PRO 2/7
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

2. XAUUSD · ENTRY เดิม TARGET เดิม SL ครึ่งเดียว เทคนิค 50% WICK 📌
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket
