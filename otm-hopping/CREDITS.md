# Credits

"Stop Strategy Hopping": a trading video in the OTM glowing-figure style (about 39 s, Instagram Reels only). It was
inspired by an interview clip about traders who change strategy every time they lose. The script is original. The
speaker in that clip is not shown, the video doesn't quote the interview, and the clip's closing promotion is left out.

The beats:

1. A habit that keeps traders stuck (a figure running on a treadmill): changing strategy every time they lose (a
   strategy card flipping A, B, C, D).
2. One loss, new strategy. Two losses, new indicator. Three losses, new mentor (three rows, then a loop arrow).
3. Nothing ever works: strategies A to E each get a few trades and are dropped, far short of the 100-trade mark.
4. Every strategy has losing streaks, even a good one (a rising equity curve with its drawdowns marked in red).
5. Profitable trading looks boring: same setup, same risk, same rules, trade after trade (a row of identical checks).
6. The edge isn't in a new strategy (ghost "new" cards drift away); it's in sticking with one long enough to let it work
   (a gold figure and a slow rising curve). Then the outro with the handles (no end card).

The Thai version (`otm-hopping-th`) is built from the same scene file with LANG = "th".

Music: none (voice and soft sound effects only).

Voice: ElevenLabs, "Quentin" (eleven_v4), the same calm, even read as the other OTM videos. Take 1 is used (both takes
followed the script; take 1 has the cleaner noise floor). Word timings come from faster-whisper (small.en). Scenes key
off word indices of work/words.json (anchor table EN_ANC in work/gen.py).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
