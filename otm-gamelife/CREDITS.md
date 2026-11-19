# Credits

"Study the Game (life + trading)": a motivation + trading video in the OTM glowing-figure style (about 59 s, Instagram
Reels only). It was inspired by an animated clip about studying "the system" instead of "the book". The clip's message
praised cheating; that is left out completely. This video is about understanding how the game works, in life and in
the market. The script is original.

The beats:

1. In school, the kid who memorized the book got the A (a classroom; an A+ paper).
2. But school ends, and nobody hands you a syllabus anymore (caps fly; a blank syllabus with a question mark).
3. Out here, the winners aren't the hardest workers; they understand how the game works (a figure running on a
   treadmill; a gold figure with a map and a route to a star).
4. Who decides? What do they want? Where's the real opportunity? (three question cards)
5. Trading is the same game (a game board with a rising chart).
6. Most traders study the book: indicators, patterns, the perfect entry. The ones who last study the game: quiet hours
   and the open, where the stop losses sit (price likes to go there), which news moves price in seconds (no position
   when it hits).
7. Hard work matters, but effort without understanding is just noise (screen time, a pile of courses, a noisy line).
8. Stop asking how hard you should work; start asking how the game actually works, in the market and in your life.
   Then the outro with the handles (no end card).

The trading-only cut of the same idea is `otm-game` / `otm-game-th`. The Thai version of this video is
`otm-gamelife-th`, built from the same scene file with LANG = "th".

Music: none (voice and soft sound effects only).

Voice: ElevenLabs, "Quentin" (eleven_v4), the same calm, even read as the other OTM videos. Take 1 is used (both takes
followed the script; take 1 keeps the pauses between sentences). Word timings come from faster-whisper (small.en).
Scenes key off word indices of work/words.json (anchor table EN_ANC in work/gen.py).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
