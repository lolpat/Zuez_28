# otm-promo

The Limitless promo (`../limitless-promo`) as an affiliate video presented by Order The Market:
57.5 seconds, 1920x1080, 30 fps, with continuous voiceover and sound effects. Limitless stays the product;
Order The Market is shown as the presenter, with an affiliate disclosure on the end card.

The voiceover is one continuous ElevenLabs take (`assets/vo/narration.wav`, voice "Everett – Confident
American Ads", normalised to −16 LUFS) and it is the clock: every scene starts 0.15 s before the first
word of its sentence, using ElevenLabs Scribe word timestamps (`CUES` in `tools/gen_promo.py`). The
longest pause while speaking is about 0.5 s.

Script: "Order The Market presents Limitless. Stop guessing. Start trading gold with a plan. Your
dashboard shows when Asia, London and New York open. Want signals? Join four signal rooms, and pick the
one that fits your style. Rather automate? Connect your account once, and trades copy automatically.
Need a plan? Limitless AI gives you an entry, a stop loss and two targets. And new scanners are on the
way. Ready to learn? Take courses from beginner to advanced. Then trade live with coaches every week.
Track everything. Every trade is logged in your journal. Nova, your AI coach, reviews your trading. Risk
calculators give you the right lot size for your balance. Level up. Climb the monthly leaderboard. And
turn your XP into real rewards. Limitless. Start your free trial with Order The Market."

The end card shows "Presented by Order The Market" and "Order The Market is an independent Limitless
affiliate. Trading involves substantial risk of loss."

- `assets/screens/otm-logo.png` and `otm-mark.png` are crops of the supplied Order The Market logo
  (transparent PNG); the "Your profits is our mission" tagline is left off.
- `tools/gen_promo.py` is this project's own copy of the generator, with the intro, the narration-driven
  timing and the co-branded end card. Run `python3 tools/gen_promo.py .` after editing it.
- Measured on the render: −16.5 LUFS, true peak −1.1 dB, no clipping.

Render:

```bash
export HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
npx hyperframes check
npx hyperframes render . --fps 30 -o renders/otm-promo.mp4
```
