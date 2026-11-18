# Credits

"Stop Strategy Hopping" (Thai version): the Thai-language edition of `otm-hopping` (about 41 s, Instagram Reels only).
It's built from the same scene file with LANG = "th", so the story, visuals and timing beats match the English version.
See `otm-hopping/CREDITS.md` for the beats and the inspiration.

The script is an original Thai adaptation:

> นิสัยที่ทำให้เทรดเดอร์ย่ำอยู่กับที่ คือการเปลี่ยนกลยุทธ์ทุกครั้งที่ขาดทุน / แพ้หนึ่งไม้ เปลี่ยนกลยุทธ์ แพ้สองไม้ เปลี่ยนอินดิเคเตอร์ /
> ทุกกลยุทธ์มีช่วงแพ้ติดกัน / เซ็ตอัพเดิม ความเสี่ยงเดิม กฎเดิม / อยู่กับกลยุทธ์เดียว นานพอให้มันทำงาน

All on-screen words are Thai; numbers stay in Montserrat digits. The outro keeps the brand lines in English, with the
line under them in Thai.

Music: none (voice and soft sound effects only).

Voice: ElevenLabs, "Patinya – Calm Thai Narrator & Explainer" (eleven_v4), the same Thai voice as the other Thai OTM
videos. Take 2 is used (both takes read the script cleanly when checked line by line; take 2 aligned better).

Timing: the script's tokens (work/script.txt) are aligned to the voice with faster-whisper (small, Thai) and a
character-level difflib match. Scenes key off token indices of work/words.json (anchor table TH_ANC).

Font: Kanit by Cadson Demak, SIL Open Font License 1.1 (assets/fonts; licence in assets/fonts/OFL-Kanit.txt; files from
@fontsource/kanit 5.3.0).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
