# Credits

"Own the Seed": a glowing-figure video in the OTM style (about 62 s, Instagram Reels only) on why the rich keep
getting richer. It was inspired by a short about US farmers who can't replant patented seeds. The script is original.

The beats:

1. Why the rich keep getting richer: a gold figure's coins stack up beside a white figure.
2. A farmer buys seeds, grows a crop and sells the whole harvest. But if he saves the seeds and plants them again, he
   can be sued.
3. The company that made the seed owns the patent. The farmer owns the crop; the company owns the recipe. So every
   season the farmer pays again.
4. That's the whole game. Most people sell the crop (their hours, their effort): paid once, then back to zero.
5. The rich own the seed (shares, businesses, patents): things that pay them again and again, every season.
6. A crop gets eaten. A seed makes more crops.
7. The real question isn't how hard you work; it's what you own. Every month, take part of your harvest and turn it
   into seed.
8. Own the recipe, not just the crop. Then the outro with the handles (no end card).

The seed story is told in general terms. A farmer who replants patented seed can be sued for patent infringement; the
US Supreme Court upheld this in Bowman v. Monsanto (2013). The video shows no company names, logos or people.

Music: none (voice and soft sound effects only).

Voice: ElevenLabs, "Quentin" (eleven_v4), the same calm, even read as the other OTM videos. Word timings come from
faster-whisper (small.en). Scenes key off word indices of work/words.json (helper `ix(i)` in work/gen.py).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
