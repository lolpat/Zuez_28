# otm-promo

The Limitless promo (`../limitless-promo`) as an affiliate video presented by Order The Market:
65.5 seconds, 1920x1080, 30 fps, with voiceover and sound effects. Limitless stays the product;
Order The Market is shown as the presenter, with an affiliate disclosure on the end card.

| Time | What's new |
| --- | --- |
| 0–3.5 s | `otm`: Order The Market logo + "PRESENTS"; voice: "Order The Market presents… Limitless." |
| 3.5–60.5 s | The Limitless promo, unchanged, shifted by 3.5 s |
| 60.5–65.5 s | `end`: Limitless logo, line, "Start your free trial", "Presented by Order The Market" with the mark, and "Order The Market is an independent Limitless affiliate. Trading involves substantial risk of loss."; voice: "Limitless. Start your free trial with Order The Market." |

- `assets/screens/otm-logo.png` and `otm-mark.png` are crops of the supplied Order The Market logo
  (transparent PNG); the "Your profits is our mission" tagline is left off.
- New voice lines (`assets/vo/otm-intro.wav`, `otm-end.wav`) use the same ElevenLabs voice as the rest.
- `tools/gen_promo.py` is this project's own copy of the generator, with the intro, the 3.5 s shift
  and the co-branded end card. Run `python3 tools/gen_promo.py .` after editing it.
- Measured on the render: −16.1 LUFS, true peak −1.5 dB, no clipping.

Render:

```bash
export HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
npx hyperframes check
npx hyperframes render . --fps 30 -o renders/otm-promo.mp4
```
