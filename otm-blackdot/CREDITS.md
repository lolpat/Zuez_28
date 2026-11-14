# Credits

"The Black Dot": a trading video in the OTM glowing-figure style (about 55 s, Instagram Reels only). It's the
companion to `otm-wholeshirt` and takes the idea of the "black dot on a white shirt" story. The script is original.

The beats:

1. 20 trades this month: 14 winners, 6 losers, and the account is up.
2. Ask the trader how the month went, and all they talk about is one trade: the one that hit the stop at the worst
   possible moment, just before price turned.
3. That's a black dot on a white shirt. Everyone stares at the dot; nobody mentions the white.
4. A loss can hurt about twice as much as a win feels good (loss aversion), so one red trade feels like the whole
   story.
5. That's when traders break their own rules: they move the stop, double the size, and try to win it back.
6. Don't judge your trading by one dot. Judge it by the whole shirt: win rate, average win against average loss, and
   discipline over a hundred trades.
7. One loss is a data point, not a verdict. Then the outro with the handles (no end card).

The trade numbers and charts are illustrative.

Music: none (voice and soft sound effects only).

Voice: ElevenLabs, "Quentin" (eleven_v4), the same calm, even read as the other OTM videos. Word timings come from
faster-whisper (small.en). Scenes key off word indices of work/words.json (helper `ix(i)` in work/gen.py).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
