# Credits

"OTM × Accurate System": a short collaboration teaser (about 18 s) in the OTM glowing style, on the same scene system as
`otm-chance` and `otm-break`. The OTM emblem lights up and slides aside, then a gold × brings in the Accurate target
icon with "ACCURATE" under it (mirroring "ORDER THE MARKET" under the emblem),
followed by "new collaboration" and "two names, one mission". Three locked tiles and a progress bar reach
"almost ready", then "BIG THINGS ARE COMING", and it ends on the OTM outro with the handles (no end card).

Partner logo: assets/accurate_logo.png, the Accurate logo supplied by the user for this collaboration (its dark background
keyed out to transparency, otherwise unchanged). assets/accurate_icon.png is the target cut from that logo (3x, lightly
sharpened) for the opening lockup. The full logo is used in the small "OTM × Accurate" lockups
(helper `duo` in work/gen.py) and in the outro.
Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Quentin" (eleven_v4), low cinematic teaser read. Word timings come from faster-whisper (small.en).
Sound effects: earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
