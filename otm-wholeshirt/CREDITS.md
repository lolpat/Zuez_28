# Credits

"The Whole Shirt": a motivation video in the OTM glowing-figure style (about 53 s, Instagram Reels only). It's the
companion to `otm-blackdot` and takes the idea of the "black dot on a white shirt" story. The script is original.

The beats:

1. One bad day, one mistake, one person who let you down, and somehow that's all you can think about (a thought
   cloud filling with one dot).
2. Picture a white shirt with one small black dot. Ask anyone what they see, and they point at the dot. Nobody
   mentions the white.
3. Your mind does the same with your life:
   - a hundred good days, and you replay the one that went wrong
   - a room full of compliments, and you remember the one that stung
4. That's not the whole truth; it's just where your attention landed.
5. When one dot starts to take over, step back and look at the white: the people who stayed, the progress you made,
   the times you got back up.
6. The dot is real, but it's small. Don't let one dot define the whole shirt. Then the outro with the handles (no end
   card).

Music: none (voice and soft sound effects only).

Voice: ElevenLabs, "Quentin" (eleven_v4), the same calm, even read as the other OTM videos. Word timings come from
faster-whisper (small.en). Scenes key off word indices of work/words.json (helper `ix(i)` in work/gen.py).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
