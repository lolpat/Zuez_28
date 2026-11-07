# Credits

Glowing-figure explainer built on the same scene system as `otm-circle`, `otm-anyway`, `otm-know`, `otm-noise` and `otm-vs` (no end card;
the outro scene carries the handles and the educational-only line).

Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Quentin" (eleven_v4), script written for OTM. Word timings: faster-whisper (small.en); scenes key
off the words themselves (helper `A(word, k)` in work/gen.py), so a new take only needs a fresh words.json.
Sound effects: earshot launch kit (code-made, shipped with earshot), placed on the scenes at low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
