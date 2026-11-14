# REVIEW: OTM CRT Theory v1 (renders/OTM_CRT_Theory.mp4)

## The film
- **File:** 51.6 s, 1080×1920, 30 fps, H.264, 25.6 MB.
- **Audio:** AAC, −17.0 LUFS integrated, sample peak −1.4 dBFS (measured with ffmpeg's ebur128).

## Creative calls
- Built storyline **A, Chart Dive**. Not built: B, Beat Slam, and C, The Trader's Floor (see STORYLINES.md).
- Every slide is cut into its own pieces and rebuilt on a clean plate. The finished frame of each scene equals the
  original slide, so no artwork was redrawn.
- **Six transition kinds:** zoom-dive into a candle, RGB glitch, whip left, whip up, white flash and a zoom out into the
  end card.
- **Hand-drawn accents I added** (not on the slides):
  - a red ring on the sweep wick (s2);
  - a blue underline on "close back inside" (s5);
  - a red box on the Weekly row (s8).
- The end card is black with the gold mark, "FOLLOW FOR MORE" and the handles footer from the slides.

## Checked and how
- **Checker:** `hyperframes check` reported zero errors and zero warnings in its runtime, layout, craft and audio passes.
- **Visual review:** `snapshot --review` (beats, seams and phone sheets) found three faults, all fixed:
  - the character peeked up before its rise;
  - a blank white frame mid-whip;
  - a heavy green wash on the glitch cut.
- **Final file:** I looked at 14 frames from the rendered MP4.

## Not checked
- The sound was measured, not heard. The effects are earshot-bank sounds made in code; each render reported "clean".
- There is no music: the music library is blocked in this container.

## Weakest shots and what I'd change
- **The first 0.6 s:** only the CRT title shows on a white plate before the chart wipes in. Starting the chart wipe at
  0.2 s would make a stronger thumbnail.
- **The glitch cuts (s2→s3, s5→s6):** the RGB copies tint the whole frame; a real per-channel shader would be cleaner.
- **Text-heavy slides (s5, s6, s8):** they hold about 3.5 s fully built, which is short for reading every line; viewers
  will pause.

## Kept on purpose
- The `duplicate_media_discovery_risk` lint notes: the glitch copies reuse each slide image deliberately.
- Effects beyond the skill's defaults (light sweeps, sparks, shakes): the person asked for "massive animation, a lot of
  effects".
