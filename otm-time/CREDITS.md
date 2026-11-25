# Credits: OTM "Not much time" (general motivation)

Two Instagram Reels from one original script, in the OTM glowing style:
- otm-time: English, Quentin (about 42 s)
- otm-time-th: Thai, Patinya (about 43 s)

Idea: a motivational TikTok the trader shared (time is short, did you get better today, start now). The script here is
original; no words, footage, images or audio from that video are used (it was cut from film and interview clips of real
people, which are not reused).

Scenes (work/timeviz.py): an hourglass running out; a grid of about 4,000 week-dots with the used part turning red
("ALREADY GONE"); "someday / later / next year" while a gold dream-star fades; "quit everything" struck out for
"1 thing today" -> "future you"; a crescent moon and "DID I GET BETTER TODAY?" with a +1% step; gold blocks
"BUILDING" vs a TODAY card falling away ("GONE", "IT NEVER COMES BACK"); "the perfect moment" struck out, a clock hand
sweeping to NOW. Phrase captions with the spoken word in gold (work/mind.py). Thai visuals in Thai.

Voice: ElevenLabs eleven_v4, "Quentin - Narrator and Educator" (EN) and "Patinya - Calm Thai Narrator & Explainer"
(TH). Timing: work/align.py, marks snapped to the real pauses. Mix (work/mix.sh): de-esser, gentle compressor, one static
gain to -16 LUFS, limiter. No music. Soft kit sounds only (whoosh, swell, bell). No end card: ends on the Order the
Market outro with the handles and the educational-only line.

Rebuild (in each folder): python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py, then
npx hyperframes@0.8.214 render

## Instagram captions (English)

1. You don't have as much time as you think. About 4,000 weeks, if you're lucky ⏳ Do one thing today your future self will thank you for.
   #forex #forextrading #tradingpsychology #tradingmindset #OrderTheMarket

2. Every night, ask: did I get a little better today? If yes, you're building. If no, that day is gone.
   #forex #forextrading #tradingpsychology #tradingmindset #OrderTheMarket

## Instagram captions (Thai)

1. เรามีเวลาน้อยกว่าที่คิด ประมาณ 4,000 สัปดาห์ ถ้าโชคดี ⏳ ทำอะไรสักอย่างวันนี้ ที่ตัวเราในอนาคตจะขอบคุณ
   #forex #forextrading #tradingpsychology #tradingmindset #OrderTheMarket

2. ทุกคืน ถามตัวเองว่า วันนี้เราเก่งขึ้นอีกนิดไหม ถ้าใช่ เรากำลังสร้าง ถ้าไม่ วันนั้นก็หายไป
   #forex #forextrading #tradingpsychology #tradingmindset #OrderTheMarket

## TikTok captions

EN: Motivation: about 4,000 weeks if you're lucky ⏳ Did you get better today? #forex #forextrading #tradingpsychology #OrderTheMarket

TH: แรงบันดาลใจ: เรามีประมาณ 4,000 สัปดาห์ ⏳ วันนี้เราเก่งขึ้นไหม? #forex #forextrading #tradingpsychology #OrderTheMarket

Hashtags: HASHTAGS.md has no general-motivation set, so these use its Mindset / psychology set, which keeps the post
tied to the trading channel.
