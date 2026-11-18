# Credits

"The Last $1,000": a trading video in the OTM glowing-figure style (about 38 s, Instagram Reels only). It was inspired
by a street-interview clip ("if you had only $1,000 left, how would you trade?"). The script is original. The speaker in
that clip is not shown, and the video doesn't quote the interview.

The beats:

1. Imagine you're down to your last $1,000 (a glowing account card). How would you trade it?
2. Not by trying to double it (a ×2 arrow, struck out). The first job of a small account is to survive (a shield).
3. Risk so little that one bad week can't knock you out: five losing days at $10 each, the balance only drops from
   $1,000 to $950 (−5%), still standing. One percent a trade or less (1 red dot in 100).
4. Trade one setup, again and again (the same setup tile fills a 4 × 3 grid while a skill bar fills), until you know it
   better than anyone.
5. No shortcuts (a rocket, crossed out), no hero trades (an all-in chip stack, crossed out). Protect, repeat, grow
   slowly (a slow staircase).
6. Slow growth never killed a small account. Big ambition does (a "get rich fast" block crushes the account card).
7. The outro with the handles (no end card).

The numbers are an illustration of position sizing, not a promise or a recommended strategy.

The Thai version (`otm-thousand-th`) is built from the same scene file with LANG = "th".

Music: none (voice and soft sound effects only).

Voice: ElevenLabs, "Quentin" (eleven_v4), the same calm, even read as the other OTM videos. Take 1 is used (take 2 read
"one percent of trade"). Word timings come from faster-whisper (small.en). Scenes key off word indices of
work/words.json (anchor table EN_ANC in work/gen.py).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
