# Credits

"Drop by Drop": a trading parable in the OTM glowing-figure style (about 58 s), on the same scene system as
`otm-chance` and `otm-missed`. It's built on the old idea that dripping water wears away stone, inspired by a short
line-drawn parable video. The script and drawings are original. The beats:

1. Traders hammer at the wall between them and consistent trading (bigger lots, higher leverage, win it all back).
   They swing harder for a few weeks, blow up and walk away.
2. One trader finds one small edge and takes it the same way every day: same risk, same rules, same journal.
3. Day 1 nothing changes; day 100 a crack; day 300 the stone splits and shows "consistency" behind it.
4. The traders who swung hardest have left the game.
5. Water breaks stone by showing up, drop after drop: consistency beats force.
6. The outro with the handles (no end card).

Companion video: `otm-bethedrop` (the same idea as general motivation).
Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Quentin" (eleven_v4), calm storytelling read. Word timings come from faster-whisper (small.en); scenes
key off word indices of work/words.json (helper `ix(i)` in work/gen.py).
Sound effects: earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
