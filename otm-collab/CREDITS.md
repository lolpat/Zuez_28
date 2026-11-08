# Credits

"OTM × Accurate": a collaboration teaser (about 38 s) in the OTM glowing style, on the same scene system as `otm-chance`
and `otm-break`. The structure:

1. The OTM emblem lights up and slides aside, and a gold × brings in the Accurate target icon with "ACCURATE" under it
   (mirroring "ORDER THE MARKET" under the emblem). Then "new collaboration" and "two names, one mission".
2. "Something is being built… here's a first look": the bar fills and the three locks turn gold.
3. A tour of Accurate's platform: ten of their own app screens, each in a glowing card under a numbered caption that
   matches the voice (one platform, market hours, market updates, filtered and organized, signal rooms, live calendar,
   learning, MetaTrader sync, position-size calculator, AI assistant). Then "FREE · NO SUBSCRIPTION NEEDED", which is
   their reel's own closing claim.
4. "This is only the beginning", then "BIGGER THINGS ARE COMING", and the OTM outro with the handles (no end card).

Partner material (supplied by the user for this collaboration):
- assets/accurate_logo.png: the Accurate logo, with its dark background keyed out to transparency (otherwise unchanged).
- assets/accurate_icon.png: the target cut from that logo, 3x and lightly sharpened.
- work/src/*.mp4: silent crops of their app screens, cut from Accurate's own promo reel. The times and crop boxes are in
  work/src/segs.txt. Their captions and their music are left out. work/clips.py re-times the crops to the voice and
  writes assets/clips/*.mp4.

Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Quentin" (eleven_v4), cinematic teaser read. Word timings come from faster-whisper (small.en).
Sound effects: earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/clips.py --sizes-only && python3 work/gen.py && python3 work/clips.py && bash work/mix.sh && python3 work/mix_sfx.py
