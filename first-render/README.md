# first-render

PROMPT 02 from the Motion Graphics starter kit: a 6-second, 1920x1080, 30 fps HyperFrames video.
A frosted-glass card rises in, a number counts from 0 to 100, and a green pill pops in at 4 s.

- `index.html` mounts the scene; `compositions/card.html` holds the card and its animation.
- `assets/fonts/` has Inter from the kit (SIL OFL). `assets/vendor/gsap.min.js` is GSAP 3.14.2,
  kept locally because the render browser here can't reach the CDN.
- Output: `renders/first.mp4`.

Render (in a Claude Code cloud container, point HyperFrames at the preinstalled headless Chromium):

```bash
export HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
npx hyperframes check
npx hyperframes render . --fps 30 -o renders/first.mp4
```

On a Mac or PC with Chrome installed, skip the `export` line.
