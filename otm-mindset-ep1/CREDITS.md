# Credits: OTM Mindset ep1, "A loss is a teacher"

Four Instagram Reels from one original script, in English and Thai and in two looks:

| Folder | Language | Look | Length |
|---|---|---|---|
| otm-mindset-ep1 | English (Quentin) | OTM glowing style | about 33 s |
| otm-mindset-ep1-th | Thai (Patinya) | OTM glowing style | about 36 s |
| otm-mindset-ep1-classic | English (Quentin) | classical paintings | about 33 s |
| otm-mindset-ep1-classic-th | Thai (Patinya) | classical paintings | about 36 s |

Idea: a short motivational TikTok the trader shared (a gold statue over classical paintings, "why is this happening
to me" vs "what is this trying to teach me"). The script here is original and trader-focused (a stop loss is tuition,
journal the mistake, every loss becomes data); no words, images or audio from that video are used.

OTM look (work/mind.py, otm_scenes): an SL-hit chart with "WHY ME?" crossed out for "WHAT IS IT TEACHING ME?", a
stuck loop vs a golden staircase, stop loss -> "IT'S TUITION" -> a PAID receipt, a trade journal with the mistake
circled, the same setup again -> READY, -1R chips -> YOUR EDGE. Phrase captions with the spoken word in gold.
Candles: up #2962ff, down white, connected. Thai visuals keep trading terms in English (stop loss, setup, edge, SL HIT).

Classical look (classic_scenes): seven images generated for this video with Higgsfield (gpt_image_2_6, 9:16, from
original prompts: a gold statue at a falling chart tablet, two stairways, an ancient academy, a gold bust with coins, a
scholar's chart journal, a gold warrior at sunrise, a sword reflecting rising candles), shown full screen with a slow
push-in and one big word at a time, keywords in gold. Stored as assets/c1..c7.jpg in the classic folders.

Voice: ElevenLabs eleven_v4, "Quentin - Narrator and Educator" (EN) and "Patinya - Calm Thai Narrator & Explainer"
(TH). Timing: work/align.py, marks snapped to the real pauses. Mix (work/mix.sh): de-esser, gentle compressor, one
static gain to -16 LUFS, limiter. No music. Soft kit sounds only (whoosh, swell, bell). No end card: each ends on the
Order the Market outro with the handles and the educational-only line.

Rebuild (in each folder): python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py, then
npx hyperframes@0.8.214 render

## Instagram captions (English)

1. Stop asking why the trade lost. Ask what it's teaching you. A stop loss isn't a punishment, it's tuition 📚
   #forex #forextrading #tradingpsychology #tradingmindset #OrderTheMarket

2. Every loss is data. Every mistake is your edge, if you write it down. Not financial advice.
   #forex #forextrading #tradingpsychology #tradingmindset #OrderTheMarket

## Instagram captions (Thai)

1. เลิกถามว่าทำไมเทรดนี้ถึงแพ้ แล้วถามว่าเทรดนี้สอนอะไรเรา Stop loss ไม่ใช่การลงโทษ มันคือค่าเรียน 📚
   #forex #forextrading #tradingpsychology #tradingmindset #OrderTheMarket

2. ทุกการขาดทุนคือข้อมูล ทุกความผิดพลาดคือ edge ของเรา ถ้าเราจดไว้ ไม่ใช่คำแนะนำทางการเงิน
   #forex #forextrading #tradingpsychology #tradingmindset #OrderTheMarket

## TikTok captions

EN: Trading mindset: a stop loss is tuition, not a punishment 📚 Journal it, learn it, be ready next time.
#forex #forextrading #tradingpsychology #OrderTheMarket

TH: Trading mindset: stop loss คือค่าเรียน ไม่ใช่การลงโทษ 📚 จดไว้ เรียนให้คุ้ม แล้วครั้งหน้าเราจะพร้อม
#forex #forextrading #tradingpsychology #OrderTheMarket
