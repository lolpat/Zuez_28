# Credits

"Know Your Numbers": a trading video in the OTM glowing-figure style (about 54 s, Instagram Reels only). It was inspired by a
trading lecture clip (why most traders keep losing: they can't say whether their strategy even makes money). The
script is original. The speaker in that clip is not shown, and the video doesn't quote the lecture.

The beats:

1. Most traders hunt for a winning trade (a magnifier on one candle). The ones who last build a winning process (a
   turning gear).
2. Ask about their last 100 trades: the journal is blank ("???"). They can't tell you if the strategy makes money.
3. No guesses: know 3 numbers. Win rate 40%, average win 2R, average loss 1R (100 dots: 40 wins, 60 losses).
4. The math over 100 trades: 40 × 2R = +80R, 60 × 1R = −60R, = +20R. A saw-tooth equity curve that still climbs:
   you lose more often and still make money.
5. Stop asking "will my next trade win?" (struck out). Start asking "does my strategy make money over 100 trades?".
6. One winning trade can feel like genius (a crown that falls). Only your numbers prove your edge (+0.2R per trade).
7. The outro with the handles (no end card).

The example numbers are an illustration of expectancy, not a promise or a recommended strategy:
0.4 × 2R − 0.6 × 1R = +0.2R per trade = +20R per 100 trades (before costs).

The Thai version (`otm-numbers-th`) is built from the same scene file with LANG = "th".

Music: none (voice and soft sound effects only).

Voice: ElevenLabs, "Quentin" (eleven_v4), the same calm, even read as the other OTM videos. Take 1 is used (both takes
followed the script; take 1 is the more even read). Word timings come from
faster-whisper (small.en). Scenes key off word indices of work/words.json (anchor table EN_ANC in work/gen.py).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
