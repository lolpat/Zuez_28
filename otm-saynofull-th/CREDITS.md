# Credits

"Say No (full)" (Thai version): the Thai-language edition of `otm-saynofull` (about 91 s, Instagram Reels only). It's
built from the same scene file with LANG = "th", so the story, visuals and timing beats match the English version.
See `otm-saynofull/CREDITS.md` for the chapters and where the idea comes from.

The script is an original Thai adaptation:

> การเทรดส่วนใหญ่ไม่ได้อยู่ที่สิ่งที่คุณทำ แต่อยู่ที่สิ่งที่คุณปฏิเสธ / แบบแรก เสี่ยงเยอะขึ้น บอกว่าไม่ / แบบที่สอง ลองระบบใหม่ดู บอกว่าไม่ /
> แบบที่สาม เบื่อแล้ว เข้าสักไม้เถอะ บอกว่าไม่ / ไม่ ไม่ แล้วก็ไม่ นั่นแหละคืองาน

All on-screen words are Thai (the stamp reads ไม่; the BUY button stays in English); money and numbers stay in
Montserrat digits. The outro keeps the brand lines in English, with the line under them in Thai.

The numbers are an illustration of position sizing, not a promise or a recommended strategy.

Music: none (voice and soft sound effects only).

Voice: ElevenLabs, "Patinya – Calm Thai Narrator & Explainer" (eleven_v4), the same Thai voice as the other Thai OTM
videos. Take 1 is used (the recogniser lost a long middle stretch of take 2; take 1 checks out line by line).

Timing: the script's tokens (work/script.txt) are aligned to the voice with faster-whisper (small, Thai) and a
character-level difflib match. Scenes key off token indices of work/words.json (anchor table TH_ANC).

Font: Kanit by Cadson Demak, SIL Open Font License 1.1 (assets/fonts; licence in assets/fonts/OFL-Kanit.txt; files from
@fontsource/kanit 5.3.0).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
