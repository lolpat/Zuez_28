# Credits

"MSNR PRO 1/7: Strong A & V": a chart explainer in the OTM glowing style, Instagram Reels only.
English version; the Thai version is `msnr-pro-ep1-th` (same scene code, LANG = "th").

MSNR PRO is a 7-part follow-up to the OTM MSNR series, based on the ideas in a 7-lecture MSNR course on YouTube
(WINZWIK FX). The scripts, voice, charts and layout are original; nothing was copied from the lectures. This part: Classic A and V levels are marked at the body close of the first candle (wicks ignored, so a gap on the second candle never moves the level). A strong A has a second candle that closes below the first candle's open; the strongest sweeps the first candle's high first. The V is the mirror.

Market: XAUUSD (gold) only. Candle colours: up #2962ff (blue), down white; candles are connected (each opens at the
previous close). Thai versions keep the trading term names in English on screen.
Charts: synthetic example data (work/pro.py). Not real market data and not a forecast.
Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Quentin - Narrator and Educator" (eleven_v4).
Timing: work/script.txt carries [key] marks; work/align.py (faster-whisper) writes work/words.json and work/marks.json,
with work/snapalign.py (pause-based) as the fallback when the transcript is unreliable.
Sound effects: the earshot launch kit, soft sounds only (whoosh, swell, bell), low level, short fades.
Voice mix (work/mix.sh): de-esser, gentle compressor, static gain to -16 LUFS, limiter at -1 dBFS.
It ends on the next-part card (only part 7/7 has the Order the Market outro).

Rebuild: python3 work/align.py en && python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py,
then npx hyperframes@0.8.214 render

## Instagram captions

1. XAUUSD · Not every Classic A or V is worth trading. Body close, engulf, sweep 🕯️ MSNR PRO 1/7.
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

2. XAUUSD · Strong A held, weak A broke. Here's how to tell them apart before the retest 📌
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket
