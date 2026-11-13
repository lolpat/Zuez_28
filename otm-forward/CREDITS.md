# Credits

"Always Forward": a motivation video for traders in the OTM glowing-figure style (about 52 s, Instagram Reels only).
It was inspired by a motivational talk clip ("always forward, never backward"). The script is original. The speaker in
that clip is not shown, and the video doesn't quote the talk.

The video adds a trading twist to the talk's advice. The talk says never consider failure; this video says you DO plan
for losses (the stop loss), but planning for a loss is not planning to quit.

The beats:

1. Always forward, never backward: a figure walks forward and the backward arrow is crossed out.
2. Once you've chosen your goal, stop leaving the back door open (the back door shuts and locks).
3. "Maybe I'll quit if this month goes badly": that thought is already a plan to fail.
4. In trading you do plan for losses (entry, stop loss), but planning for a loss is not planning to quit.
5. Every trader who made it had a month that almost broke them: a losing streak, a blown account, a day they wanted to
   walk away. The difference? They didn't (the walls fall, the figure reaches the flag).
6. Persistence isn't a mood (a wavy line); it's a decision (a straight gold arrow).
7. The market tests you from the outside (arrows); whether you keep going is decided inside (a gold core).
8. Cut the loss, keep the dream. Always forward, never backward. Then the outro with the handles (no end card).

The Thai version (`otm-forward-th`) is built from the same scene file with LANG = "th".

Music: none (voice and soft sound effects only).

Voice: ElevenLabs, "Quentin" (eleven_v4), the same calm, even read as the other OTM videos. Word timings come from
faster-whisper (small.en). Scenes key off word indices of work/words.json (anchor table ANC in work/gen.py).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
