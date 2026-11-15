# Credits

"MSNR PRO 5/7: Storyline road map": a chart explainer in the OTM glowing style, Instagram Reels only.
English version; the Thai version is `msnr-pro-ep5-th` (same scene code, LANG = "th").

MSNR PRO is a 7-part follow-up to the OTM MSNR series, based on the ideas in a 7-lecture MSNR course on YouTube
(WINZWIK FX). The scripts, voice, charts and layout are original; nothing was copied from the lectures. This part: Price moves from one higher-timeframe key level to the next. A level counts once a timeframe one or two steps lower shows a market structure shift (monthly: weekly or daily; weekly: daily or 4H; daily: 4H or 1H). Then trade only that direction to the next level; levels in between are road blocks.

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

1. XAUUSD · Key level to key level. Read the road map before you trade 🗺️ MSNR PRO 5/7.
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket

2. XAUUSD · Monthly level held, daily shifted, price ran to the next level 📌
   #forex #xauusd #goldtrading #priceaction #OrderTheMarket
