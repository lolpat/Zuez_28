# Credits

"Say No (full)": the full-length version of `otm-sayno` (about 86 s, Instagram Reels only), one video that brings the
last three OTM videos together. Most of trading is what you refuse to do: the market tempts you three ways, and each
temptation is a chapter that says no and shows why. The script is original.

1. Intro: most of trading isn't what you do; it's what you refuse to do. The market will tempt you three ways.
2. Chapter 1, "risk more, win it back faster" (NO), from "The Last $1,000" (`otm-thousand`): down to your last $1,000,
   the urge to double it (×2, struck out), survive first (a shield); risk 1% a trade or less (1 red dot in 100), five
   losses cost $50 and you're still standing; slow growth never killed a small account, big ambition does (a "get
   rich fast" block crushes the account card).
3. Chapter 2, "three losses in a row, try a new strategy" (NO), from "Stop Strategy Hopping" (`otm-hopping`): one
   loss, new strategy; two, new indicator; three, new mentor; strategies A to E never reach 100 trades; every strategy
   has losing streaks (a rising curve with red drawdowns); keep it boring: same setup, same risk, same rules.
4. Chapter 3, "you're bored, just take something" (NO), from "The Skill of Doing Nothing" (`otm-nothing`): watch two
   hours, see nothing worth taking and close the screen; forced entries and B-grade setups feel like progress but
   are just activity; the market pays for being picky, not busy (two setups glow gold out of twenty).
5. No, no and no: that's the job (three NO stamps). Then the outro with the handles (no end card).

The numbers ($1,000, 1% = $10, five losses = $50) are an illustration of position sizing, not a promise or a
recommended strategy.

The Thai version (`otm-saynofull-th`) is built from the same scene file with LANG = "th".

Music: none (voice and soft sound effects only).

Voice: ElevenLabs, "Quentin" (eleven_v4), the same calm, even read as the other OTM videos. Take 1 is used (both takes
followed the script). Word timings come from faster-whisper (small.en). Scenes key off word indices of
work/words.json (anchor table EN_ANC in work/gen.py).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
