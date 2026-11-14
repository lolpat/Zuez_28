# Credits

"Be the Drop": a motivational glowing-figure video in the OTM style (about 52 s), the companion to `otm-dropstone`. It
tells the same water-and-stone idea as general motivation, in original words. The beats:

1. Not the strongest person in the room; the one who's still there.
2. Hammer-style starts (a huge start, a burst of energy) fade to nothing: big plans on Monday, gone by Friday.
3. The things that change your life are small: one page a day, one workout, one honest hour.
4. Day 1 nothing happens; day 30 nothing you can see; around day 200 the stone cracks open and shows the person
   you're becoming.
5. Water carves stone with repetition, not force.
6. Stop waiting for one big breakthrough. Be the drop, and show up again tomorrow.
7. The outro with the handles (no end card).

Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Quentin" (eleven_v4), warm, uplifting read. Word timings come from faster-whisper (small.en); scenes
key off word indices of work/words.json (helper `ix(i)` in work/gen.py).
Sound effects: earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
