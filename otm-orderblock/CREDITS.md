# Credits

"The Order Block": a chart explainer in the OTM glowing style (same scene system as `otm-break` and `otm-chance`), about
44 s, Instagram Reels only. It was inspired by an order-block segment in a trading-strategy explainer reel, but the
script and chart are original. The voice walks through one example:

1. Big money leaves footprints; the order block is one of them.
2. Find a strong push up, then look right before it: the last down candle. That's the order block, where big buyers
   placed their orders.
3. When price comes back to that zone, buyers often defend it. Don't chase the move; let price come to you.
4. Buy limit at the middle of the candle's body, stop under its low. A close below it means the idea is wrong: take the
   small loss and move on.
5. The strongest blocks leave a gap right after them, which shows real urgency. Then the outro with the handles (no end
   card).

Candle colours: up candles #2962ff (blue), down candles white.

Chart: synthetic example data in work/chart.py (a seeded decline, then hand-placed candles for the block, the push, the
pullback and the rally). It is not real market data and not a forecast; the video labels it "example chart".
Music: none (voice and soft sound effects only).
Voice: ElevenLabs, "Quentin - Narrator and Educator" (eleven_v4), the same calm teaching read as the other OTM videos.
Word timings come from faster-whisper (small.en); scenes key off word indices of work/words.json (helper `ix(i)`).
Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py, then npx hyperframes@0.8.214 render

## Instagram captions

1. Order blocks, explained on one chart 📈 The last down candle before a strong push up: buy limit at the middle of its
   body, stop under its low. Save this 📌
   #forex #forextrading #smartmoneyconcepts #priceaction #OrderTheMarket

2. Stop chasing the move. Mark the order block, set your limit, and let price come to you. A close below it means the
   idea is wrong: small loss, next trade.
   #forex #forextrader #smartmoneyconcepts #technicalanalysis #OrderTheMarket
