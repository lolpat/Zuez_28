# Work in progress: "Know Your Numbers" (English and Thai)

Everything except the narration is ready. The ElevenLabs connector failed to connect in the session that prepared
this, so there is no voice yet and nothing has been rendered.

What's here:

- `otm-numbers/work/script_en.txt`: the English narration prompt (ElevenLabs "Quentin", eleven_v4).
- `otm-numbers-th/work/script_prompt.txt`: the Thai narration prompt ("Patinya", eleven_v4). `script.txt` is the same
  text without the tag; its 38 whitespace tokens are the Thai anchors.
- `otm-numbers/work/numbers_scenes.py`: the shared scenes (7 scenes, LANG "en" or "th"). TH_ANC is filled; EN_ANC is
  empty until the English voice exists and its words.json gives the word indices.
- `work/build.sh` in each project: assembles work/gen.py from doc.txt, the scene-system head of
  otm-missed/work/gen.py, `_scenes.py` (`LANG = "en"` or `"th"` followed by numbers_scenes.py) and the shared tail.

Next steps:

1. Generate the two narrations (2 takes each), keep the take that follows the script.
2. Word timings: faster-whisper small.en for English; for Thai, align the script tokens to the voice
   (faster-whisper small, Thai, plus a character-level difflib match).
3. Fill EN_ANC, write `_scenes.py` for each language, run build.sh and gen.py.
4. Copy the assets (kit, vendor, emblem, logo; Kanit fonts for Thai) from otm-selfish / otm-selfish-th.
5. `npx hyperframes check`, snapshots, render, Reels conversion, loudness check (about -16 LUFS).
