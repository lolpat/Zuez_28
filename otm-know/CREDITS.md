# Credits

Glowing-figure explainer built on the same scene system as `otm-circle` and `otm-anyway` (no end card; the outro
scene carries the handles and the educational-only line).

Music: none. The background piano was taken out at the user's request; the mix is voice plus soft sound effects.

Voice: ElevenLabs, "Quentin" (eleven_v4), script in work/script.txt. Word timings: faster-whisper (small.en), aligned
token by token to the scene layout. (A first cut used a Piper voice while the ElevenLabs credits were out.)
Sound effects: earshot launch kit (code-made, shipped with earshot), placed on the scenes at low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
No music credit is needed in the captions.
