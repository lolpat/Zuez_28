# Credits

"Say No": a trading video in the OTM glowing-figure style (about 40 s, Instagram Reels only). It's a new idea built
from the last three OTM videos: "The Last $1,000" (`otm-thousand`), "Stop Strategy Hopping" (`otm-hopping`) and "The
Skill of Doing Nothing" (`otm-nothing`). Their shared lesson: most of trading is about what you refuse to do. The
script is original.

The beats:

1. Most of trading isn't about what you do; it's about what you refuse to do (a calm gold figure, a gold ring).
2. The market will tempt you in three ways (three red cards around the figure).
3. Temptation 1, "risk more, win it back faster" (risk 20%): a gold NO stamp. Risk 1% and stay in the game.
4. Temptation 2, "three losses in a row, try a new strategy": NO. Same setup, same rules, long enough to work.
5. Temptation 3, "bored, just take something" (a pulsing BUY button): NO. Wait for the A+ trade you'd take on your best
   day.
6. No, no and no: that's the job (three NO stamps). Then the outro with the handles (no end card).

The Thai version (`otm-sayno-th`) is built from the same scene file with LANG = "th".

Music: none (voice and soft sound effects only).

Voice: ElevenLabs, "Quentin" (eleven_v4), the same calm, even read as the other OTM videos. Take 1 is used (both takes
followed the script). Word timings come from faster-whisper (small.en). Scenes key off word indices of
work/words.json (anchor table EN_ANC in work/gen.py).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
