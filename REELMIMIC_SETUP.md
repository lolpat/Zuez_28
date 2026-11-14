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

## Issues hit during a real production run
4. **Wrong crop on a full-frame vertical reference.** The analyzer treated a 720×1280 reel as a phone screen
   recording and cropped it to a 720×508 band, so the first plan was 1440×1016. Fix used: a chat message asking for
   1080×1920 full frame. The planner re-ran the analysis without the crop.
5. **A review step fails as "Missing output" when the reviewer keeps an existing file.** `turn.ts` requires each
   output's mtime to be newer than the turn start. A reviewer that agrees with an existing, valid `review_*.json`
   leaves it untouched, and the step fails. Fix used: "Retry this step" (`POST /api/projects/<id>/retry`), which
   accepts existing outputs.
6. **The plan usage limit isn't recognised.** Claude Code now says "You've hit your session limit", which the
   `LIMIT` regex in `turn.ts` doesn't match. The job shows "The agent turn failed" instead of the usage-limit message.
   Fix used: wait for the reset, then retry.
7. **Nested agents inherit the parent Claude Code session.** If `start.sh` is launched from inside a Claude Code
   session, every agent ReelMimic spawns inherits `CLAUDE_CODE_SESSION_ID` (and the related remote-session variables).
   All of them then report the same session ID, and builders "resume" the wrong conversation. Fix: start the server
   with those variables unset, e.g.
   `env -u CLAUDE_CODE_SESSION_ID -u CLAUDE_CODE_REMOTE_SESSION_ID -u CLAUDE_CODE_REMOTE_SDK_URL -u CLAUDE_CODE_CHILD_SESSION -u CLAUDECODE -u CLAUDE_CODE_MESSAGING_SOCKET -u CLAUDE_CODE_MESSAGING_TOKEN -u CLAUDE_CODE_SESSION_ATTENDED ./start.sh`,
   then clear `sessionId`/`sessions` in the project's `job.json`.
