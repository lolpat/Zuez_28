# Credits

"The $100 Million Lesson": the story of Jesse Livermore (1877–1940), full version (about 2 minutes 50 seconds, under the 3-minute Reels limit). It's in the OTM
glowing-figure style, on the same scene system as `otm-chance` and `otm-break`. Livermore is the figure in the fedora, and
a timeline across the top lights each year as the story reaches it (1891 to 1940). The 24 scenes:

- The hook: $100,000,000, then buried in debt.
- Taken out of school for the farm, he leaves for Boston with $5.
- Paine Webber: chalking prices for $5 a week, and a notebook of patterns.
- The bucket shop: no real stock, just a bet on up or down.
- His first $5 bet on a railroad stock, and a win.
- About $200 a week by 16; he quits his job.
- Banned from the shops: "the Boy Plunger".
- 1900, New York: real orders fill slower than bucket-shop bets, he loses everything, and he adapts.
- 1907: too much borrowed money, so he bets against the market and makes about $1,000,000 in a day. J.P. Morgan
  sends word asking him to stop selling, and he does.
- The 1908 cotton tip, then bankruptcy in 1915.
- The Bethlehem Steel comeback, with every creditor repaid although the law didn't require it.
- The 1920s borrowing boom, then 1929 (about $100,000,000): "the Great Bear of Wall Street".
- The rules slipping: buying back too early, an expensive divorce, bigger bets.
- 1934: over $2,000,000 in debt with under $200,000 left.
- His rules, put in his 1940 book "How to Trade in Stocks" (paraphrased here, not quoted): cut losses fast, never
  more than 10%; never add to a loser; let the market prove you right; trust your own plan.
- Rule 3 broken after 1929. "His rules never failed him. He failed his rules." Then every day, and the outro.

It was inspired by a Thai-language TikTok on the same story. The script, wording and drawings are original. The facts
and figures are the widely documented outline of Livermore's career, rounded the way they're usually told.

Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Quentin" (eleven_v4), calm storytelling read. Word timings come from faster-whisper (small.en); scenes
key off word indices of work/words.json (helper `ix(i)` in work/gen.py). For a new take, run
`python3 work/remap.py OLD_words.json NEW_words.json`: it aligns the two transcripts and rewrites the indices.
Sound effects: earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
