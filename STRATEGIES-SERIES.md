# OTM STRATEGIES series (XAUUSD)

One strategy per episode, on gold, in the OTM glowing style. English (Quentin) and Thai (Patinya) versions.
Ending (changed by the trader, Nov 2026): every episode ends with a short "next episode" teaser and then the Order the
Market outro (FOLLOW FOR MORE, handles, educational-only line), instead of ending on the next-episode card.

| Ep | Strategy | Job | Folder |
|---|---|---|---|
| 0 + 1 | **Posted as one video:** the map + Break of Structure, ending on the outro (about 2:18) | - / WHEN | **otm-strat-ep01 / -th** |
| 0 | Every strategy we'll learn (the map + the 3 jobs), standalone version | - | otm-strat-ep0 / -th |
| 1 | Break of Structure (BOS), standalone version | WHEN | otm-strat-ep1 / -th |
| 2 | Change of Character (CHoCH) | WHEN | next |
| 3 | Liquidity Sweep | WHEN | |
| 4 | Support & Resistance | WHERE | |
| 5 | Supply & Demand | WHERE | |
| 6 | Order Block (mean threshold) | WHERE / ENTRY | |
| 7 | Breaker Block | WHERE | |
| 8 | Fair Value Gap (FVG) | ENTRY | |
| 9 | Inverse FVG | ENTRY | |
| 10 | Optimal Trade Entry (62-79%, 70.5) | ENTRY | |
| 11 | Breakout & Retest | WHEN / ENTRY | |
| 12 | Silver Bullet | WHEN + ENTRY | |
| 13 | Power of Three (AMD) | MODEL | |
| 14 | All together: sweep -> BOS -> FVG (with the outro) | ALL | |

CRT has its own series (CRT + CRT PRO) and is shown on the ep 0 map as "full series". KRM (a paid model from
another channel) is left out.

## Credits

Scenes: work/strat.py in each folder (built on the CRT engine). Original drawings and synthetic XAUUSD charts
(candles up #2962ff, down white, connected); the ep 1 example (last high 3,880, buy 3,866, SL 3,858) is an
illustration, not a real trade, and says so on screen. Thai visuals keep trading terms in English.

References the trader shared (ideas only; no words, images or footage reused): a "every trading strategy" overview
video (the 3-jobs idea: where / when / entry); for BOS, five Market Movers Signals slides and three Thai TikTok lessons
(close vs wick, the swing that made the new high, 5M/15M over 1M/3M, sweep -> BOS -> entry, BOS vs CHoCH).
A YouTube lesson (youtu.be/FE1bgD9N6DM) could not be watched: the Gemini video service was overloaded on every model.

Voice: ElevenLabs eleven_v4, "Quentin - Narrator and Educator" (EN) and "Patinya - Calm Thai Narrator & Explainer"
(TH). Timing: work/align.py, marks snapped to the real pauses. Mix (work/mix.sh): de-esser, gentle compressor, one
static gain to -16 LUFS, limiter. No music. Soft kit sounds only.

Rebuild (in each folder): python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py, then
npx hyperframes@0.8.214 render

## Captions

### Ep 0 + 1 in one video (otm-strat-ep01)

Instagram (EN)
1. Every trading strategy, one by one, on gold 📌 Start here: the 3 jobs every strategy does, then ep 1: Break of Structure. Close, not wick.
   #forex #forextrading #priceaction #technicalanalysis #OrderTheMarket
2. Sweep, then BOS, then buy the pullback. The first lesson of the series. Save it and follow for the rest. Not financial advice.
   #forex #forextrading #priceaction #technicalanalysis #OrderTheMarket

Instagram (TH)
1. ทุกกลยุทธ์เทรด เรียนทีละอัน บนทองคำ 📌 เริ่มที่นี่: 3 หน้าที่ของทุกกลยุทธ์ แล้วตอนที่ 1 Break of Structure ต้องปิดแท่ง ไม่ใช่แค่ไส้
   #forex #forextrading #priceaction #technicalanalysis #OrderTheMarket
2. Sweep แล้ว BOS แล้วเข้าตอน pullback บทเรียนแรกของซีรีส์ เซฟไว้ แล้วกดติดตามตอนต่อไป ไม่ใช่คำแนะนำทางการเงิน
   #forex #forextrading #priceaction #technicalanalysis #OrderTheMarket

TikTok
EN: Trading strategies series ep 0 + 1: every strategy on gold, then Break of Structure 📌 #forex #priceaction #forexeducation #OrderTheMarket
TH: ซีรีส์กลยุทธ์เทรด ตอน 0 + 1: ทุกกลยุทธ์บนทองคำ แล้ว Break of Structure 📌 #forex #priceaction #forexeducation #OrderTheMarket

Hashtags: the Technical set from HASHTAGS.md.

### Ep 0: every strategy we'll learn

Instagram (EN)
1. Every trading strategy, one by one, on gold. Start here 📌 14 episodes: BOS, CHoCH, sweeps, order blocks, FVG, OTE and more.
   #forex #forextrading #priceaction #technicalanalysis #OrderTheMarket
2. Every strategy does one of three jobs: where, when, or the exact entry. A clean trade uses one of each. Save the series.
   #forex #forextrading #priceaction #technicalanalysis #OrderTheMarket

Instagram (TH)
1. ทุกกลยุทธ์เทรด เรียนไปทีละอัน บนทองคำ เริ่มที่นี่ 📌 14 ตอน: BOS, CHoCH, sweep, order block, FVG, OTE และอีกมาก
   #forex #forextrading #priceaction #technicalanalysis #OrderTheMarket
2. ทุกกลยุทธ์ทำหน้าที่แค่หนึ่งในสาม: ที่ไหน เมื่อไหร่ หรือจุดเข้าเป๊ะๆ เทรดที่คลีนใช้อย่างละหนึ่ง เซฟซีรีส์ไว้
   #forex #forextrading #priceaction #technicalanalysis #OrderTheMarket

TikTok
EN: Trading strategies series: every strategy explained on gold, one by one 📌 #forex #priceaction #forexeducation #OrderTheMarket
TH: ซีรีส์กลยุทธ์เทรด: สอนทุกกลยุทธ์บนทองคำ ทีละอัน 📌 #forex #priceaction #forexeducation #OrderTheMarket

### Ep 1: Break of Structure

Instagram (EN)
1. Break of structure (BOS), ep 1: a candle CLOSE beyond the last swing, same direction as the trend. A wick doesn't count.
   #forex #forextrading #priceaction #technicalanalysis #OrderTheMarket
2. Sweep, then BOS, then buy the pullback, not the breakout candle. 3 rules for a real BOS 📌 Not financial advice.
   #forex #forextrading #priceaction #technicalanalysis #OrderTheMarket

Instagram (TH)
1. Break of structure (BOS) ตอนที่ 1: ต้องปิดแท่งเลย swing ล่าสุด ไปทางเดียวกับเทรนด์ แค่ไส้ทะลุไม่นับ
   #forex #forextrading #priceaction #technicalanalysis #OrderTheMarket
2. Sweep แล้ว BOS แล้วเข้าตอน pullback อย่าไล่แท่งใหญ่ 3 กฎของ BOS จริง 📌 ไม่ใช่คำแนะนำทางการเงิน
   #forex #forextrading #priceaction #technicalanalysis #OrderTheMarket

TikTok
EN: Break of structure explained: close, not wick 📌 #forex #priceaction #forexeducation #OrderTheMarket
TH: Break of structure (BOS) คืออะไร: ต้องปิดแท่ง ไม่ใช่แค่ไส้ 📌 #forex #priceaction #forexeducation #OrderTheMarket
