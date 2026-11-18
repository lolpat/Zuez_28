# Credits

"The Last $1,000" (Thai version): the Thai-language edition of `otm-thousand` (about 41 s, Instagram Reels only). It's
built from the same scene file with LANG = "th", so the story, visuals and timing beats match the English version. See
`otm-thousand/CREDITS.md` for the beats and the inspiration.

The script is an original Thai adaptation:

> ลองนึกว่าคุณเหลือเงินก้อนสุดท้ายแค่หนึ่งพันดอลลาร์ / หน้าที่แรกของพอร์ตเล็กคือการอยู่รอด / ไม้ละหนึ่งเปอร์เซ็นต์ หรือน้อยกว่านั้น /
> เทรดแค่เซ็ตอัพเดียว ซ้ำแล้วซ้ำเล่า / การโตช้าไม่เคยฆ่าพอร์ตเล็ก ความอยากรวยเร็วต่างหากที่ฆ่า

All on-screen words are Thai; money and numbers stay in Montserrat digits. The outro keeps the brand lines in English,
with the line under them in Thai.

The numbers are an illustration of position sizing, not a promise or a recommended strategy.

Music: none (voice and soft sound effects only).

Voice: ElevenLabs, "Patinya – Calm Thai Narrator & Explainer" (eleven_v4), the same Thai voice as the other Thai OTM
videos. Take 2 is used (in take 1 the "no shortcuts … grow slowly" lines did not come through clearly).

Timing: the script's tokens (work/script.txt) are aligned to the voice with faster-whisper (small, Thai) and a
character-level difflib match. Scenes key off token indices of work/words.json (anchor table TH_ANC).

Font: Kanit by Cadson Demak, SIL Open Font License 1.1 (assets/fonts; licence in assets/fonts/OFL-Kanit.txt; files from
@fontsource/kanit 5.3.0).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
