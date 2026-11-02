# Credits

Glowing-figure explainer built on the same scene system as `otm-circle` and `otm-anyway` (no end card; the outro
scene carries the handles and the educational-only line).

Music: "Song for Tony (acoustic piano, thoughtful sad hopeful)" by geoffpeters — Attribution (3.0)
(http://creativecommons.org/licenses/by/3.0/) — https://ccmixter.org/files/geoffpeters/48500
Used: 0:00–1:04, about -30 LUFS under the voice, swelling under the outro and fading out.

Voice: Piper TTS (MIT), voice "en_US-john-medium" (dataset: LibriVox, public domain), from work/script.txt.
Used because the ElevenLabs account ran out of credits; swap in Quentin later by replacing work/voice.mp3,
re-running the word timings (faster-whisper, words.json) and the build.
Sound effects: earshot launch kit (code-made, shipped with earshot), placed on the scenes at low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
Social caption credit line: Music: "Song for Tony" by geoffpeters (CC BY 3.0)
