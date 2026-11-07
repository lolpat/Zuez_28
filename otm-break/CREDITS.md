# Credits

"The Trendline Break": a chart explainer in the OTM glowing style (same scene system as `otm-chance` and `otm-believe`). It
was inspired by an Elliott Wave update video, but the script and charts are original. The voice walks through how to read a
trend-line break after a complex correction: an impulse, then W-X-Y-X-Z, the line across the falling highs, the break,
the pullback that holds, target 1 at the channel top, the next leg, and the failure case. It then zooms into a 4-hour
chart (A-B-C, then A-B-C with a triangle, joined as W-X-Y) and ends with a question for the comments and the outro (no end
card).

Charts: synthetic example data drawn by work/chart.py (seeded candles through hand-placed pivots). They are not real market
prices and not a forecast; the video labels them "example chart".
Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Quentin" (eleven_v4), clear teaching read (about 2.8 words/s), script written for OTM. Word timings
come from faster-whisper (small.en); scenes key off the words (helpers `A(word, k)` and `ix(i)` in work/gen.py).
Sound effects: earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
