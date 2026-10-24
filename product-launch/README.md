# product-launch

PROMPT 09 from the Motion Graphics starter kit: a 12-second, 1920x1080, 30 fps launch video for Tally,
an app that shows what an online shop really earns after fees. No product.png was given, so the
logo and app screens are built in HTML and CSS. There was no STYLE section, so it uses white frosted
cards on a soft light gradient.

| Time | Scene file | What happens |
| --- | --- | --- |
| 0–2 s | `compositions/intro.html` | Logo: four tally strokes draw up, a slash crosses them, "Tally" writes in |
| 2–4.4 s | `compositions/connect.html` | Cursor clicks "Connect store", it turns to "Connected", 1,284 orders sync |
| 4.4–6.8 s | `compositions/profit.html` | Fees, ad spend and refunds drop in; profit falls from $48,200 to $34,820 |
| 6.8–9 s | `compositions/morning.html` | A 7:00 lock-screen notification: "Yesterday you kept $1,146" |
| 9–12 s | `compositions/endcard.html` | Logo, "Know what your shop really earns.", Join the waitlist |

`compositions/bg.html` is the gradient behind every scene. Fonts are Inter from the kit;
GSAP 3.14.2 is in `assets/vendor/` because the render browser here can't reach the CDN.

Render (in a Claude Code cloud container, point HyperFrames at the preinstalled headless Chromium):

```bash
export HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
npx hyperframes check
npx hyperframes render . --fps 30 -o renders/product.mp4
```
