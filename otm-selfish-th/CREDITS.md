# Credits

"Selfish With Your Time" (Thai version): the Thai-language edition of `otm-selfish` (about 49 s, Instagram Reels only).
It's built from the same scene file with LANG = "th", so the story, visuals and timing beats match the English version.
See `otm-selfish/CREDITS.md` for the beats and the inspiration.

The script is an original Thai adaptation:

> เห็นแก่ตัวสักสามปี ไม่ใช่กับคนรอบข้าง แต่กับเวลาของคุณ / ใส่หน้ากากออกซิเจนให้ตัวเองก่อน /
> อย่าทุ่มหมดตัวในไม้เดียว ให้ทุ่มสุดตัวกับกระบวนการ / บอกความจริงกับตัวเอง / สะสมต่อไปทีละวัน

All on-screen text is Thai. The outro keeps the brand lines in English, with the line under them in Thai.

Music: none (voice and soft sound effects only).

Voice: ElevenLabs, "Patinya – Calm Thai Narrator & Explainer" (eleven_v4), the same Thai voice as the other Thai OTM
videos.

Timing: the script's tokens (work/script.txt) are aligned to the voice with faster-whisper (small, Thai) and a
character-level difflib match. Scenes key off token indices of work/words.json (anchor table ANC).

Font: Kanit by Cadson Demak, SIL Open Font License 1.1 (assets/fonts; licence in assets/fonts/OFL-Kanit.txt; files from
@fontsource/kanit 5.3.0).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
