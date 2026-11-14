# Credits

"Fail Forward": a motivational glowing-figure video in the OTM style (about 55 s), the companion to `otm-mostlosses`. It
tells the same reference idea as general motivation, in original words. The beats:

1. Nobody counts how many times you fell; they remember the day you stood up and stayed up.
2. School taught you to hide mistakes: a red mark, a lower grade.
3. But every "no", closed door and dead end was training.
4. Each failure is one step closer to the way that works.
5. Failure is never final unless you stop.
6. 10 failures = 10 lessons; 0 failures = never tried.
7. Try again, fail smaller, learn faster, keep showing up.
8. The person you're becoming is built from every time you didn't quit. Then the outro with the handles (no end card).

Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Quentin" (eleven_v4), warm, uplifting read. Word timings come from faster-whisper (small.en); scenes
key off word indices of work/words.json (helper `ix(i)` in work/gen.py).
Sound effects: earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
