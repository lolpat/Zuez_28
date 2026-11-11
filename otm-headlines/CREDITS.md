# Credits

"Headlines vs. the Trend": an educational glowing-figure video in the OTM style (about 63 s, Instagram Reels only).
It was inspired by an infographic that put four founders' personal scandals on their companies' stock charts.
The script is original. The beats:

1. Four founders, four personal scandals, four front pages.
2. Four widely reported cases, in neutral wording, each on its own card with an illustrative chart and a red
   "headline" dot:
   - Amazon, 2019
   - Microsoft, 2021
   - SK hynix, 2015
   - Google, 2013
3. "You'd expect the stocks to suffer" (dashed red lines). Years later every one was far higher (gold lines).
4. Not because of the scandal: timing doesn't prove cause. They rose because the businesses kept growing (products,
   customers, earnings).
5. The headline lasted a week; the trend lasted years.
6. When the news is screaming, ask: does this change the business, or just the conversation?
7. Trade the trend, not the gossip. Then the outro with the handles (no end card).

Left out of the video on purpose:
- people's photos and names
- company logos (the company names are plain text)
- the infographic's exact percentages
- the infographic's fifth case, an unconfirmed rumour

The charts are illustrative shapes, not real price data, and are labelled on screen as "ILLUSTRATIVE CHARTS · NOT
ACTUAL PRICES".

Music: none (voice and soft sound effects only).

Voice: ElevenLabs, "Quentin" (eleven_v4), a calm, even read. Word timings come from faster-whisper (small.en). Scenes key
off word indices of work/words.json (helper `ix(i)` in work/gen.py).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
