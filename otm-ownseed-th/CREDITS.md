# Credits

"Own the Seed" (Thai version): the Thai-language edition of `otm-ownseed` (about 70 s, Instagram Reels only). It's a
glowing-figure video in the OTM style on why the rich keep getting richer. The story and visuals match the English
version, with Thai narration and Thai on-screen text. The outro keeps the brand lines in English: "ORDER THE MARKET",
"FOLLOW FOR MORE" and "EDUCATIONAL ONLY · NOT FINANCIAL ADVICE". The line under them is in Thai.

The script is an original Thai adaptation. The beats:

1. ทำไมคนรวยถึงรวยขึ้นเรื่อยๆ (why the rich keep getting richer).
2. A farmer buys seed, grows and sells the harvest, but can be sued for replanting patented seed.
3. The company holds the patent: the farmer owns the crop, the company owns the recipe, so every season the farmer
   pays again.
4. That's the whole game. Most people sell the crop (their time and labour), get paid once, then start again from
   zero.
5. The rich own the seed (shares, businesses, patents) that pays them again and again.
6. A crop gets eaten; one seed grows into many crops.
7. The real question is not how hard you work but what you own. Every month, turn part of your harvest into seed.
8. Own the recipe, not just the crop. Then the outro with the handles (no end card).

The seed story is told in general terms. A farmer who replants patented seed can be sued for patent infringement; the
US Supreme Court upheld this in Bowman v. Monsanto (2013). The video shows no company names, logos or people.

Music: none (voice and soft sound effects only).

Voice: ElevenLabs, "Patinya – Calm Thai Narrator & Explainer" (eleven_v4), a calm Thai read.

Timing: the script's tokens (work/script.txt) are aligned to the voice with faster-whisper (small, Thai) and a
character-level difflib match; scenes key off token indices of work/words.json.

Font: Kanit by Cadson Demak, SIL Open Font License 1.1 (assets/fonts, licence in assets/fonts/OFL-Kanit.txt). The files
come from the @fontsource/kanit 5.3.0 package (Thai and Latin subsets, weights 600 / 700 / 800).

Sound effects: the earshot launch kit (code-made, shipped with earshot), at a low level (work/cues.json).

Rebuild: python3 work/gen.py && bash work/mix.sh && python3 work/mix_sfx.py
