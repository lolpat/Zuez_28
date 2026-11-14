# Credits

"Always Forward" (Thai version): the Thai-language edition of `otm-forward` (about 53 s, Instagram Reels only). It's
built from the same scene file with LANG = "th", so the story, visuals and timing beats match the English version. See
`otm-forward/CREDITS.md` for the beats and the inspiration.

The script is an original Thai adaptation:

> ไปข้างหน้าเสมอ ไม่ถอยหลัง / เลิกเปิดประตูหลังทิ้งไว้ / วางแผนรับการขาดทุน (สต็อปลอส) แต่ไม่ใช่การวางแผนที่จะเลิก / ความอดทนคือการตัดสินใจ /
> ตัดขาดทุน แต่อย่าตัดความฝัน

All on-screen text is Thai. The outro keeps the brand lines in English, with the line under them in Thai.

Music: none (voice and soft sound effects only).

Voice: ElevenLabs, "Patinya – Calm Thai Narrator & Explainer" (eleven_v4), the same Thai voice as `otm-ownseed-th`.

Timing: the script's tokens (work/script.txt) are aligned to the voice with faster-whisper (small, Thai, no initial
prompt) and a character-level difflib match. Scenes key off token indices of work/words.json (anchor table ANC).

Font: Kanit by Cadson Demak, SIL Open Font License 1.1 (assets/fonts; licence in assets/fonts/OFL-Kanit.txt; files from
@fontsource/kanit 5.3.0).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
