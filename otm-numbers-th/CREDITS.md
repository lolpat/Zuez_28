# Credits

"Know Your Numbers" (Thai version): the Thai-language edition of `otm-numbers` (about 61 s, Instagram Reels only). It's built from
the same scene file with LANG = "th", so the story, visuals and timing beats match the English version. See
`otm-numbers/CREDITS.md` for the beats and the inspiration.

The script is an original Thai adaptation:

> เทรดเดอร์ส่วนใหญ่มัวแต่ตามหาไม้ที่ชนะ แต่คนที่อยู่รอดกำลังสร้างระบบที่ชนะ / รู้ตัวเลขสามตัว อัตราชนะ กำไรเฉลี่ย
> ขาดทุนเฉลี่ย / สี่สิบคูณสอง ลบหกสิบคูณหนึ่ง ได้บวกยี่สิบอาร์ในหนึ่งร้อยไม้ / มีแค่ตัวเลขที่พิสูจน์ได้ว่าคุณมีความได้เปรียบจริง

All on-screen words are Thai; numbers and the maths stay in Montserrat digits. The outro keeps the brand lines in
English, with the line under them in Thai.

The example numbers are an illustration of expectancy, not a promise or a recommended strategy.

Music: none (voice and soft sound effects only).

Voice: ElevenLabs, "Patinya – Calm Thai Narrator & Explainer" (eleven_v4), the same Thai voice as the other Thai OTM
videos. Take 1 is used (its key words, such as กลยุทธ์ and กดติดตาม, come through more clearly).

Timing: the script's tokens (work/script.txt) are aligned to the voice with faster-whisper (small, Thai) and a
character-level difflib match. Scenes key off token indices of work/words.json (anchor table TH_ANC).

Font: Kanit by Cadson Demak, SIL Open Font License 1.1 (assets/fonts; licence in assets/fonts/OFL-Kanit.txt; files from
@fontsource/kanit 5.3.0).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
