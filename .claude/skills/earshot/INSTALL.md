# earshot skill: how to install it

This folder is the earshot skill: the instructions Claude follows to "hear" audio and the sound of a video. The skill
only tells Claude how to use the earshot tool. The tool does the listening, so install both.

earshot is open source (MIT licence, by Leon Lin): https://github.com/Leonxlnx/earshot. It runs on your own computer's
CPU, and your audio never leaves the machine.

## 1. Install the earshot tool

You need Python 3.10+ and ffmpeg on your PATH. Then run:

```bash
git clone https://github.com/Leonxlnx/earshot && cd earshot
python -m venv .venv
.venv/bin/python -m pip install torch --index-url https://download.pytorch.org/whl/cpu   # Windows: .venv/Scripts/python
.venv/bin/python -m pip install -e ".[mcp,llm,dev]"
.venv/bin/python -m earshot doctor --fetch   # downloads the two listening models once (about 1.1 GB)
```

## 2. Add the skill to Claude Code

Copy this `earshot` folder to `~/.claude/skills/earshot/`, so the file sits at `~/.claude/skills/earshot/SKILL.md`.
Optionally, keep the models loaded between calls by adding the MCP server:

```bash
claude mcp add earshot --scope user -e EARSHOT_THREADS=3 -- /path/to/earshot/.venv/bin/python -m earshot mcp
```

## 3. Commands used on the OTM videos

```bash
earshot measure video.mp4                  # loudness (LUFS), peak, loudness range; reads the audio of an mp4
earshot timeline video.mp4                 # a second-by-second listening transcript of the whole video
earshot describe sound.wav                 # what a sound is, in words
earshot critique video.mp4                 # a scorecard of the soundtrack
```

The OTM videos aim for about -16 LUFS, the level these Reels are mixed to.
