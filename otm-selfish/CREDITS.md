# Credits

"Selfish With Your Time": a motivation video for traders in the OTM glowing-figure style (about 47 s, Instagram Reels
only). It was inspired by a motivational talk clip ("be selfish for the next three years... put your own oxygen mask
on"). The script is original. The speaker in that clip is not shown, and the video doesn't quote the talk.

The talk's money advice ("go all in", "be greedy") was rewritten for trading. Be selfish with your time, not with
people. Never go all in on one position; go all in on the process.

The beats:

1. Be selfish for the next 3 years: a 36-month grid fills in.
2. Not with people (they keep a heart), but with your time (a locked clock).
3. Put your own oxygen mask on first: build your skill, savings and discipline (three rising bars).
4. In trading, never go all in on one position (a chip stack on one trade, crossed out). Go all in on the process
   (plan, execute, journal, review).
5. Tell yourself the truth, "I'm not where I want to be": then check off study more, journal every trade, follow
   your rules even on the hard days.
6. Do that for 3 years, and what you can do in 5, 7, 12 years is hard to imagine (a compounding curve).
7. Stay focused, stay humble, stay grounded.
8. Keep stacking one day at a time, no matter what anyone around you says. Then the outro with the handles (no end
   card).

The Thai version (`otm-selfish-th`) is built from the same scene file with LANG = "th".

Music: none (voice and soft sound effects only).

Voice: ElevenLabs, "Quentin" (eleven_v4), the same calm, even read as the other OTM videos. Take 2 is used; take 1
added a word. Word timings come from faster-whisper (small.en). Scenes key off word indices of work/words.json
(anchor table ANC in work/gen.py).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
