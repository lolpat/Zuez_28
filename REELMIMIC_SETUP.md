# ReelMimic setup test (Linux cloud container)

Upstream: https://github.com/edenfunf/reelmimic @ d445b23

## Issues found and fixed

1. **`./install.sh` / `./start.sh`: Permission denied.** Both are committed as mode 100644, so they aren't executable.
   Fix: `chmod +x install.sh start.sh` (the patch makes them mode 100755).
2. **Doctor: Chrome/Chromium not found.** The only Chromium here is Playwright's, at a path the doctor doesn't check.
   Fix (configuration, no code change): `~/.reelmimic/secrets.json` →
   `{ "CHROME_PATH": "/opt/pw-browsers/chromium-1243/chrome-linux64/chrome" }`
3. **`npm test`: runner "cancel kills a tool process…" fails.** The grandchild process is killed correctly but
   stays a zombie, because the container's PID 1 doesn't reap orphans, and `kill(pid, 0)` still succeeds on a zombie.
   Fix: the test's `alive()` now treats zombie processes (`/proc/<pid>/stat` state `Z`) as dead.

Apply the code fixes with `git apply reelmimic-linux-fixes.patch` in a reelmimic checkout.

## Results after fixes
- `npm run doctor`: all required items present (Node 22.22, Python 3.13, FFmpeg 6.1, Chrome, Claude Code)
- `npm test`: 106/106 pass; Python skill tests: 71 passed, 2 skipped
- `./start.sh` serves http://localhost:4318; `/api/health` OK, the UI renders with no console errors
- Smoke job: an original 12 s FFmpeg-generated reference plus a one-line brief, submitted through the UI. Not approved,
  so no 1–3.5 h production run was started.
