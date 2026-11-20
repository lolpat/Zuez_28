# Credits

"Fed Minutes: gold below 3,800" (Thai news reel, about 59 s, Instagram Reels only). The October FOMC minutes
(meeting of 27–28 Oct 2026, released 18 Nov 2026 US time) said almost all participants saw further rate hikes as likely
appropriate; a couple said a move bigger than 25 bp could be considered if inflation data stayed unfavourable. The dollar
and yields stayed firm, and spot gold fell below $3,800 for the first time since September 2025 (a 14-month low), with
lows reported around $3,700 (feeds differ: roughly $3,693–3,757).

The topic came from a Thai news clip the owner shared (another channel's short). The script, layout and graphics here are
original; no footage, images or wording were reused from it.

Script (work/script.txt):

> เฟดส่งสัญญาณแรง ทองคำหลุดสามพันแปดร้อยดอลลาร์ ครั้งแรกในรอบสิบสี่เดือน / เมื่อคืนเฟดเปิดบันทึกการประชุม FOMC
> รอบเดือนตุลาคม / ครั้งนั้นเฟดคงดอกเบี้ยไว้ แต่เกือบทุกคนในห้องประชุม มองว่าน่าจะต้องขึ้นดอกเบี้ยต่อ / … /
> อย่ารีบรับมีด ให้ตลาดยืนยันก่อน / Order the market อย่าให้ตลาดเป็นฝ่ายสั่งคุณ กดติดตามไว้นะครับ

Fact sources (checked 20 Nov 2026):
- CNBC, "Fed minutes October 2026": https://www.cnbc.com/2026/11/18/fed-minutes-october-2026.html
- ABA Banking Journal, "FOMC minutes show 'close call' over possible rate hike": https://bankingjournal.aba.com/2026/11/fomc-minutes-show-close-call-over-possible-rate-hike/
- GoldSilver, "Most of Gold's Drop Came Before the Fed Minutes": https://goldsilver.com/industry-news/goldsilver-news/fed-minutes-gold-december-hike/
- Investing.com, "Spot gold sheds over 3%, drops below $3,800/oz for first time since September 2025": https://in.investing.com/news/commodities-news/gold-falls-toward-3800-as-fed-hawks-reinforce-ratehike-outlook-5711178
- Admiral Markets, "Why Is Gold Going Down? Gold at a 14-Month Low": https://admiralmarkets.com/analytics/traders-blog/why-is-gold-falling-november-2026

Photos (Wikimedia Commons, resized to 1600 px wide in assets/photos):
- eccles.jpg: "Eccles Building (26088200676).jpg", Federal Reserve (Flickr), public domain (U.S. Government work).
  https://commons.wikimedia.org/wiki/File:Eccles_Building_(26088200676).jpg
- fomc2016.jpg: "Federal Open Market Committee (FOMC) in Washington DC April 26-27, 2016.jpg", Federal Reserve, public
  domain (U.S. Government work). https://commons.wikimedia.org/wiki/File:Federal_Open_Market_Committee_(FOMC)_in_Washington_DC_April_26-27,_2016.jpg
- goldbars.jpg: "Gold bullion bars.jpg", Stevebidmead, CC0. https://commons.wikimedia.org/wiki/File:Gold_bullion_bars.jpg
- ingots.jpg: "Gold Ingots on white background.jpg", Szaaman, public domain. https://commons.wikimedia.org/wiki/File:Gold_Ingots_on_white_background.jpg

The candle chart is illustrative (labelled on screen as not a real price chart); only the 3,800 break and the ~3,700 low
follow the reports.

Music: none (voice and soft sound effects only).

Voice: Higgsfield "Text to Speech V2" (ElevenLabs engine), preset voice "John", sped up 1.1x with ffmpeg atempo. This is
NOT the usual Patinya voice: the ElevenLabs account was out of credits, and the owner chose a Higgsfield preset voice. A
Seed Audio take with the same voice was tried first and dropped (poor Thai pronunciation).

Timing: work/align.py aligns the script's tokens to the voice with faster-whisper (small, Thai, word timestamps) and a
character-level difflib match (87% of script characters matched). Scenes key off token indices of work/words.json.

Font: Kanit by Cadson Demak, SIL Open Font License 1.1 (assets/fonts; licence in assets/fonts/OFL-Kanit.txt).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/align.py && python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
Render: npx --yes hyperframes@0.8.214 render -o renders/otm-fedgold-th.mp4

## Instagram captions

1.
เฟดส่งสัญญาณขึ้นดอกเบี้ยต่อ ทองหลุด $3,800 ครั้งแรกในรอบ 14 เดือน 📉
ทองลงขนาดนี้ น่ารับหรือยัง? ดูดอลลาร์กับยีลด์ก่อน อย่าเพิ่งรีบรับมีด
เพื่อการศึกษาเท่านั้น ไม่ใช่คำแนะนำการลงทุน
#xauusd #goldtrading #ลงทุน #การเงิน #OrderTheMarket

2.
บันทึกประชุม FOMC: เกือบทุกคนมองว่าอาจต้องขึ้นดอกเบี้ยอีก 🏛️
ทองโดนกดลงไปแถว $3,700 ให้ตลาดยืนยันก่อน แล้วค่อยมองหาจังหวะ 📌 เซฟไว้
เพื่อการศึกษาเท่านั้น ไม่ใช่คำแนะนำการลงทุน
#xauusd #goldtrading #ลงทุน #การเงิน #OrderTheMarket
