# Credits

"The Skill of Doing Nothing": a trading video in the OTM glowing-figure style (about 37 s, Instagram Reels only). It
was inspired by an interview clip about profitable traders being able to do nothing. The script is original. The
speaker in that clip is not shown, the video doesn't quote the interview, and the clip's closing promotion is left out.

The beats:

1. The rarest skill in trading: doing nothing (a calm gold figure, "trades today: 0").
2. A good trader can watch the chart for two hours (a clock sweeps two hours over a choppy chart), see nothing worth
   taking and close the screen (the monitor goes dark and the figure walks away).
3. Most traders can't: at the chart they feel they must trade (an urge meter fills and a BUY button pulses).
4. So they force entries, take B-grade setups and trade out of boredom (trades today: 1, 2, 3; each card a losing
   trade).
5. That's activity, not progress (an activity bar at 100%, a progress bar near 0%).
6. The market doesn't pay you for being busy (every setup taken, in red); it pays you for being picky (two setups
   glow gold).
7. Some days the best trade is the one you don't take (a skipped entry; price then falls through it). Then the outro
   with the handles (no end card).

The Thai version (`otm-nothing-th`) is built from the same scene file with LANG = "th".

Music: none (voice and soft sound effects only).

Voice: ElevenLabs, "Quentin" (eleven_v4), the same calm, even read as the other OTM videos. Take 1 is used (both takes
followed the script; take 1 is the more even read). Word timings come from faster-whisper (small.en). Scenes key off
word indices of work/words.json (anchor table EN_ANC in work/gen.py).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
