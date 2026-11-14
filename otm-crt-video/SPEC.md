# SPEC: OTM CRT Theory, "Chart Dive"

GOAL: the viewer learns the CRT rule in one watch and follows @fxzuez_28 / zuez_28 for more.

OUTPUT: HyperFrames, 1080×1920, 30 fps, motion blur on.

TIME: 51.6 s × 30 = 1548 frames. No music: the effects carry the clock.

LOOK: the slides' own world. The ground is a light-grey paper (#f6f7f9 with 1.6 σ grain), black brush titles with
electric-blue type, the blue (#1f5cff) edge brushes, the gold OTM mark, and red (#ff2d3d) and green only where the
slides use them. The end card is black with the gold mark.

OBJECTS: every slide is cut into its own pieces: the title brush, each text line, each candle or diagram, the stamps
(✗ / ✓ / Power of 3 / FOREX / pink sweep box), and the character. The clean plate keeps the brand frame (logo, edge
brushes, handles footer).

MOTION:
- Titles slam: scale 1.75 → 1, blur 14 → 0, 0.34 s `expo.out`, a 22 px camera shake and a white pop.
- Text: a clip wipe left → right, 0.36 s `power3.out`, lines 0.15 s apart.
- Candles and diagrams grow from the bottom, 0.45 s `expo.out`.
- Stamps: scale 2.8 → 1, `back.out(2.2)`, a 14 px shake and 12 sparks.
- The character rises out from behind the footer, 0.62 s `back.out(1.25)`.
- Light sweep over each title, 0.7 s.

SHOTS:
| scene | time | content | exit |
|---|---|---|---|
| s1 | 0–4.6 | cover; the CRT title is already on screen at frame 0 | dive into the CRT candles |
| s2 | 4.6–10.4 | What is CRT; red ring on the sweep wick | glitch (RGB split + jitter) |
| s3 | 10.4–16.2 | valid CRT: ✗ then ✓ stamps | whip left |
| s4 | 16.2–22.4 | Power of 3: three candles build | dive |
| s5 | 22.4–28.6 | four bullets; "close back inside" underlined | glitch |
| s6 | 28.6–34.8 | Time & Price: FOREX / INDEX stamps, icons pop | whip up |
| s7 | 34.8–41.0 | Turtle Soup: the sweep box stamps, five bullets | dive |
| s8 | 41.0–47.6 | Time Frame table builds row by row; the Weekly row is boxed | dive |
| end | 47.6–51.6 | gold mark slams with a shine; FOLLOW FOR MORE; handles footer rises | |

SOUND:
- Effects from the earshot bank (made in code; renders checked clean), mixed by `work/mix.py` to about −17 LUFS with
  peaks ≤ −1.5 dBFS.
- Each sound: title → cut_hit punch, line → hover tick, candle → ui pop, stamp → kick or knock, character → swish,
  dive → fast whoosh (peak one frame after the cut), glitch burst, riser → impact + logo sting on the mark.

BANNED: the character peeking before its rise; a fully blank frame mid-cut; whole-frame colour wash on a glitch.

QA: frame 0 shows the CRT title; every scene's last 0.5 s before its exit equals the original slide; the end card
holds 2 s or more.

Source of truth: `work/gen.py` generates `compositions/*.html`, `index.html` and `work/cues.json`; `work/mix.py`
generates `assets/audio/sfx.wav`. Edit the generator, not the HTML, then re-run both.
