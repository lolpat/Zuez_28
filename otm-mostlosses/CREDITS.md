# Credits

"The Trader With the Most Losses": a glowing-figure explainer in the OTM style (about 74 s), on the same scene system as
`otm-chance` and `otm-missed`. It was inspired by an explainer about "the student who fails the most", rewritten for
trading in original words. The beats:

1. In school a mistake cost you points; in the market the rules flip. Losses aren't graded, and what works gets paid,
   over time.
2. Test, lose small, write it down.
3. A new trader's three strategies: stopped out, a slow bleed, then one that works (he doesn't know why yet).
4. His journal of losses, each teaching something about price.
5. A loss only gets expensive when it's big, or when you learn nothing from it.
6. Small, written losses become data, and data is the difference between guessing and an edge.
7. A hundred journaled losses are a hundred lessons; hiding from losses gives none.
8. A small loss is the fee for finding out what works. Then the outro with the handles (no end card).

Companion video: `otm-failforward` (the same idea as general motivation).
Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Quentin" (eleven_v4), calm read. Word timings come from faster-whisper (small.en); scenes key off word
indices of work/words.json (helper `ix(i)` in work/gen.py).
Sound effects: earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
