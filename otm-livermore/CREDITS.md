# Credits

"The $100 Million Lesson": a story of Jesse Livermore (1877–1940) in the OTM glowing-figure style, on the same scene
system as `otm-chance` and `otm-break`. Livermore is the figure in the fedora, and a timeline across the top lights each
year as the story reaches it (1891 to 1934). The beats:

- The hook: $100,000,000, then buried in debt.
- Boston at 14, chalking prices on the quote board and seeing patterns.
- His first $5 trade at 15, and trading paying more than his job by 16.
- The 1907 panic: about $1,000,000 in a day.
- The 1908 cotton tip, then bankruptcy in 1915.
- The comeback (creditors repaid) and 1929 (about $100,000,000).
- Drifting from his rules, then bankrupt again in 1934.
- His rules, paraphrased: cut losses fast; never add to a loser; let the market prove you right; trust your own plan.
- The lesson: rules only work if you follow them every day.

It was inspired by a Thai-language TikTok on the same story. The script, wording and drawings are original. The facts
are the widely documented outline of Livermore's career, rounded the way they're usually told.

Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Quentin" (eleven_v4), calm storytelling read. Word timings come from faster-whisper (small.en); scenes
key off the words (helper `A(word, k)` in work/gen.py).
Sound effects: earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
