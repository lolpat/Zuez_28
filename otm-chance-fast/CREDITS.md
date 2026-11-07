# Credits

"Second Chance": the fast version, matching the pace of the reference clip. It has the same script as `otm-chance`, read
with more energy (about 3.35 words/s; the reference is about 3.4). It hard-cuts every two words (90 cuts, about 0.58 s
each) and shows one giant word at a time over a matching glowing-figure picture. Each picture is chosen by a keyword in the
words it covers (the `KW` table in work/gen.py). A whoosh and a short flash mark each new section. The video ends on the
outro scene with the handles and the educational-only line (no end card).

Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Quentin" (eleven_v4), energetic read. Word timings come from faster-whisper (small.en).
Font: Archivo Black for the big words (Google Fonts, SIL Open Font License).
Sound effects: earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
