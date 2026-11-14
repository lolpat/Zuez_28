# Credits

"Don't Stop Now" (Thai version): the Thai-language edition of `otm-dontstop` (about 52 s, Instagram Reels only). It's
built from the same scene file with LANG = "th", so the story, visuals and timing beats match the English version. See
`otm-dontstop/CREDITS.md` for the beats and the inspiration.

The script is an original Thai adaptation:

> คุณอาจใกล้กว่าที่คิด / ไม่ใช่ห่างแค่เทรดดวงดีไม้เดียว แต่ห่างแค่นิสัยเดียว / อย่าหยุดตอนนี้ / บททดสอบเป็นเรื่องชั่วคราว /
> แล้วอนาคตที่คุณสร้าง จะเดินมาเจอคุณครึ่งทาง

All on-screen text is Thai. The outro keeps the brand lines in English, with the line under them in Thai.

Music: none (voice and soft sound effects only).

Voice: ElevenLabs, "Patinya – Calm Thai Narrator & Explainer" (eleven_v4), the same Thai voice as the other Thai OTM
videos. Take 2 is used, because take 1's ending did not transcribe completely.

Timing: the script's tokens (work/script.txt) are aligned to the voice with faster-whisper (small, Thai) and a
character-level difflib match. Scenes key off token indices of work/words.json (anchor table ANC).

Font: Kanit by Cadson Demak, SIL Open Font License 1.1 (assets/fonts; licence in assets/fonts/OFL-Kanit.txt; files from
@fontsource/kanit 5.3.0).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
