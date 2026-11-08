# Credits

"OTM × Accurate System": a short collaboration teaser (about 18 s) in the OTM glowing style, on the same scene system as
`otm-chance` and `otm-break`. The OTM emblem lights up and slides aside, then a gold × brings in the ACCURATE SYSTEM
wordmark, followed by "new collaboration" and "two names, one mission". Three locked tiles and a progress bar reach
"almost ready", then "BIG THINGS ARE COMING", and it ends on the OTM outro with the handles (no end card).

Partner mark: plain text wordmark only, because no Accurate System logo was supplied. Swap in their logo
(assets/, then the wordmark group in work/gen.py) when it arrives.
Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Quentin" (eleven_v4), low cinematic teaser read. Word timings come from faster-whisper (small.en).
Sound effects: earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
