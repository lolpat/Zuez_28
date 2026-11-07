# Credits

Glowing-figure explainer built on the same scene system as `otm-circle` and `otm-anyway` (no end card; the outro
scene carries the handles and the educational-only line).

Music: "Song for Tony (acoustic piano, thoughtful sad hopeful)" by geoffpeters — Attribution (3.0)
(http://creativecommons.org/licenses/by/3.0/) — https://ccmixter.org/files/geoffpeters/48500
Used: 0:00–1:04, about -30 LUFS under the voice, swelling under the outro and fading out.

Voice: ElevenLabs, "Quentin" (eleven_v4), script in work/script.txt. Word timings: faster-whisper (small.en), aligned
token by token to the scene layout. (A first cut used a Piper voice while the ElevenLabs credits were out.)
Sound effects: earshot launch kit (code-made, shipped with earshot), placed on the scenes at low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
Social caption credit line: Music: "Song for Tony" by geoffpeters (CC BY 3.0)
