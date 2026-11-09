# Credits

"The Trade You Missed": a short glowing-figure story in the OTM style (about 48 s), on the same scene system as
`otm-chance` and `otm-livermore`. It was inspired by a "the delay that saved me" skit and turned into a trading lesson:

1. The perfect setup you've waited all week for.
2. The platform freezes as you click BUY, and price runs without you.
3. "You were right, and you're not in." You're tempted to BUY NOW at any price, but you don't.
4. +10 min: breaking news spikes the market through where your stop would have been, so the trade you missed would
   have been a big loss.
5. A missed trade costs $0; a forced trade can cost everything. Not every setup is yours: let it go.
6. The outro with the handles (no end card).

The script and drawings are original.
Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Quentin" (eleven_v4), calm storytelling read. Word timings come from faster-whisper (small.en); scenes
key off word indices of work/words.json (helper `ix(i)` in work/gen.py).
Sound effects: earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
