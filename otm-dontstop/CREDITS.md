# Credits

"Don't Stop Now": a motivation video for traders in the OTM glowing-figure style (about 48 s, Instagram Reels only).
It was inspired by a motivational talk clip ("you're only one win away... don't stop now"). The script is original. The
speaker in that clip is not shown, and the video doesn't quote the talk.

The video adds a trading twist: you're not one lucky trade away (a dice gets crossed out), you're one habit away, one
rule you finally keep.

The beats:

1. You might be closer than you think: a figure near the top of a staircase, with a gold flag at the top.
2. Not one lucky trade away; one habit away, one rule you finally keep.
3. Whatever you do, don't stop now: a pause sign is crossed out and becomes a play arrow.
4. The hardest part is already behind you: you started (the first step lights up) and kept going, one step at a time.
5. This stretch is hard (a rain cloud; losing weeks, doubt, silence). But that's just a test, and tests are temporary
   (an hourglass flips, the cloud drifts away).
6. Traders who make it don't wait for easy; they find a way (over the wall): +1 chart, +1 lesson, +1 day of discipline.
7. It doesn't matter how long it takes: a calendar counts day 1, 90, 365.
8. Keep stacking the steps, and the future you're building will meet you halfway (a gold future self walks down to
   meet the figure).
9. Don't stop now. Then the outro with the handles (no end card).

The Thai version (`otm-dontstop-th`) is built from the same scene file with LANG = "th".

Music: none (voice and soft sound effects only).

Voice: ElevenLabs, "Quentin" (eleven_v4), the same calm, even read as the other OTM videos. Word timings come from
faster-whisper (small.en). Scenes key off word indices of work/words.json (anchor table ANC in work/gen.py).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
