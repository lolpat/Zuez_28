# Credits

"Second Chance": the normal-pace version. A glowing-figure explainer on the same scene system as `otm-believe`, `otm-vs` and
`otm-know`, with one scene per sentence (about 66 s). There is no end card: the outro scene carries the handles and the
educational-only line. The fast-cut version of the same script is in `otm-chance-fast`.

Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Quentin" (eleven_v4), calm read (about 2.9 words/s), script written for OTM. Word timings come from
faster-whisper (small.en). Scenes key off the words themselves (helper `A(word, k)` in work/gen.py), so a new take only
needs a fresh words.json.
Sound effects: earshot launch kit (code-made, shipped with earshot), placed on the scenes at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
