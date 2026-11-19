# Credits

"Study the Game": a trading video in the OTM glowing-figure style (about 42 s, Instagram Reels only). It was inspired by
an animated clip about studying "the system" instead of "the book". The clip's message praised cheating; that is left
out completely. This video is only about understanding how the market works. The script is original.

The beats:

1. Most traders study the book: indicators, patterns, the perfect entry (a stack of books).
2. The ones who last study the game (a gold figure, a magnifier and a game board: clock, stops, news).
3. They know when the market is quiet and when it wakes up (a flat line through the quiet hours, then the open: the
   line and the volume come alive).
4. They know where the stop losses sit, because that's where price likes to go (STOP tags under equal lows; price
   wicks into them and reverses: liquidity).
5. They know which news can move price in seconds, and they're not in a trade when it hits (a high-impact news
   countdown, a spike, "no position").
6. Everyone else works hard: hours of charts, a new course every month (screen time 2H to 12H, a pile of courses).
7. The market doesn't hand you a syllabus, and nobody grades your effort (a blank syllabus; "effort A+" crossed out).
8. Stop asking how hard you should work; start asking how the game actually works. Then the outro with the handles
   (no end card).

The Thai version (`otm-game-th`) is built from the same scene file with LANG = "th".

Music: none (voice and soft sound effects only).

Voice: ElevenLabs, "Quentin" (eleven_v4), the same calm, even read as the other OTM videos. Take 2 is used (both takes
followed the script; take 2 keeps the pauses of "Indicators. Patterns. The perfect entry."). Word timings come from
faster-whisper (small.en). Scenes key off word indices of work/words.json (anchor table EN_ANC in work/gen.py).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
