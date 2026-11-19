# Credits

"The Skill of Doing Nothing" (Thai version): the Thai-language edition of `otm-nothing` (about 39 s, Instagram Reels
only). It's built from the same scene file with LANG = "th", so the story, visuals and timing beats match the English
version. See `otm-nothing/CREDITS.md` for the beats and the inspiration.

The script is an original Thai adaptation:

> ทักษะที่หายากที่สุดในการเทรด คือการไม่ทำอะไรเลย / นั่งดูกราฟได้สองชั่วโมง ไม่เจออะไรที่น่าเข้า แล้วก็ปิดจอไป /
> นั่นคือความยุ่ง ไม่ใช่ความก้าวหน้า / ตลาดไม่ได้จ่ายเงินให้คนที่ยุ่ง แต่จ่ายให้คนที่เลือก

All on-screen words are Thai (the BUY button stays in English); numbers stay in Montserrat digits. The outro keeps the
brand lines in English, with the line under them in Thai.

Music: none (voice and soft sound effects only).

Voice: ElevenLabs, "Patinya – Calm Thai Narrator & Explainer" (eleven_v4), the same Thai voice as the other Thai OTM
videos. Take 2 is used (both takes read the script when checked line by line; take 2 aligned better).

Timing: the script's tokens (work/script.txt) are aligned to the voice with faster-whisper (small, Thai) and a
character-level difflib match. Scenes key off token indices of work/words.json (anchor table TH_ANC).

Font: Kanit by Cadson Demak, SIL Open Font License 1.1 (assets/fonts; licence in assets/fonts/OFL-Kanit.txt; files from
@fontsource/kanit 5.3.0).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
