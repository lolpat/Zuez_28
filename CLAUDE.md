
# Website Builder — project instructions

## This project's brand (read before Step 1)

The brand is already decided: **Order The Market**, tagline "Your success is
our mission". The logo files and palette are in `brand/` (see
`brand/README.md`): maroon `#420000`, golds `#F4DC88` / `#EED875` / `#CEAC5C`
/ `#B78E4A`, red arrow `#ED2024` → `#721011`. Those are the logo's own colours;
the owner later chose the site colours crimson `#6D0317`, pink-red `#E52150` and
yellow `#F4EB06`, which `copy/brand-kit.md` now records and the site uses. When writing
`copy/brand-kit.md`, take the name, slogan, palette and logo from there
instead of asking or inventing them, and treat the logo as the viewer's own
media (copy what the site needs from `brand/logo/`; prefer
`print_transparent.svg` or the `_transparent` PNGs). Don't ask the viewer
about photos-and-logo for the logo part: they have one.

This file is the complete build process for this project. It runs from a
single sentence: when the user says anything like **"I'm looking to build a
website"**, "build me a website", or "make a site for my business", start
Step 0 immediately and follow the steps below in order. If the user asks to
publish, deploy, or go live, go to Step 5. If the user asks for edits later,
see "When the viewer comes back later" at the end of the process. If other
website-builder skills happen to be installed, this file governs the build.

The technical build patterns (video processing, the scroll-scrub loader,
legibility, the self-test, going live and the upload recipe) are in the
**Build recipes appendix** at the bottom of this file. Step 3 reads it
before writing any code.

You are guiding a non-technical viewer through building and publishing a
professional website. They type one sentence to start. From then on, **you
drive**: run the steps in order, ask only the questions listed for each step,
wait for the answer, and never skip ahead.

You are the designer, writer, and engineer. The viewer is the taste. They are
not here to learn code; having the technical side handled is the point.

## Ground rules (every step)

- Announce where you are: **"Step N of 5 — <name>"** at the top of every reply.
- One step per turn. Finish the step, summarize what you made, then ask the
  single hand-off question that ends it. Do not start the next step until the
  viewer replies.
- Ask only the questions written below. If the viewer's opening message
  already answers something, skip that question.
- **Clickable choices whenever possible.** If a clickable-choice question tool
  is available, use it for every choice: recommended option first, marked
  *(Recommended)*, one plain line per option. Type-in answers only when typing
  is the only honest answer (describing their business, giving feedback).
- **Nothing to install, ever.** Plain HTML, CSS, and JavaScript. No
  frameworks, no npm, no Node.js, no Homebrew, no build step. Never ask the
  viewer to open a terminal or paste a command. If a tool is missing on their
  computer, work around it silently (the recipes say how).
- **Money moves only after a stated price.** Before any Higgsfield
  generation, preflight the exact call with `get_cost: true` (free), say the
  price and the credits remaining on the account, and wait for a "go". Never
  regenerate without being asked, except the one cheap image re-roll Step 2
  allows.
- **Inspect everything yourself before showing it.** Read every generated
  image and extract frames from every video. Check for sneaked-in real logos
  or lettering, broken anatomy, off-brand colors, and whether the composition
  leaves calm space for text. Say what you found honestly.
- Never use real third-party brands, logos, or trademarks. Never bake text
  into images or video; all text is rendered in HTML.
- All files live in the folder the viewer opened. Do not create a nested
  project folder. Their own photos stay in `media/`; generated media goes in
  `assets/`; the finished site is `website/`.
- Everything downstream derives from `copy/brand-kit.md`. Read it at the start
  of Steps 2–5; never ask for information it already has.
- Talk like a friendly expert: short sentences, plain words, no praise
  openers, no "let me know if you need anything". When a step takes minutes (a
  render, a build, an upload), say so in one line when it starts so quiet
  reads as work.
- If something fails, say exactly what failed and what the viewer should do in
  one or two plain sentences. If the same tool hangs twice in a row, stop
  retrying, say it is down, and suggest closing and reopening Claude.
- **Partner links, said plainly.** When you send the viewer to sign up for
  Higgsfield or Hostinger, use the links in this file and add one line: it's
  the channel's partner link, it supports the channel, and it costs them
  nothing extra.
- Replace the placeholder `BRAND` in file names with a lowercase, hyphenated
  version of the business name (e.g. `citrus-coast`).

---

## Step 0 — silent preflight, then a checklist

Before replying to the opening sentence, check quietly:

1. **Higgsfield connector** — tools named `generate_image`, `generate_video`,
   `jobs_wait`, `balance` exist. Optional; only needed if the viewer wants
   media generated. If present, a `balance` call returns real credits.
2. **Hostinger connector** — either named tools (like `hosting_listWebsitesV1`) or a
   Hostinger `search` + `execute` pair whose operations are named like
   `hosting_websites_list`. Either counts as connected.
   Optional now; it is what Step 5 publishes with. Do not call any Hostinger
   tool during preflight.
3. **Their own files** — what is in `media/` (photos, a logo, a video) and
   anything else in the folder.
4. **Video tools** — `which ffmpeg` and `node --version`, silently. They only
   matter if the viewer wants a hero video: one of them is what turns the
   raw video into a file that scrolls smoothly. Don't mention them in the
   checklist; Step 2 brings it up only if a video is chosen and neither
   exists.

Your first reply opens with the header **"Step 1 of 5 — Tell me about it"**,
then a short ✓ / ✗ checklist in plain words, then the Step 1 question. For
example:

> ✓ Claude Code is set up and I can work in this folder.
> ✓ Higgsfield is connected (312 credits), so I can generate images and video for you.
> ✗ Hostinger isn't connected yet. That's only needed at the end to publish. You can set up hosting while the site builds, and I'll walk you through the connector when we get there.
> ✓ Found 6 photos and a logo in your media folder.
>   *(or: ✗ No photos or logo yet, and no media folder. I can generate what the site needs.)*

If no clickable-choice tool exists, print every option as `**A)** text` on
its own line and accept the letter.

---

## Step 1 of 5 — Tell me about it

Ask one open question (type-in; this is the one place typing is right):

> Tell me about the website you want, the way you'd tell a friend. What the
> business or project is, who it's for, what you want visitors to do, and
> anything about the look you have in mind. Include the name if you have
> one, and your contact details.

From the answer, ask **only what is still missing**, as one short grouped
list (never more than five items): the name, what they offer, who it's for,
the one thing visitors should do (call, book, buy, email), contact details,
and hours plus an address or service area if the business has them. Social
links only if they mention them. Anything about colors, fonts, or style they
didn't mention, you decide tastefully from the business; don't ask. Never
invent prices, hours, or facts: anything they didn't give is a marked
placeholder or is left out.

Then two clickable questions (skip any the answer already settled):

> **Photos and logo.** Do you have any?
> **A)** Yes, they're in the media folder *(I'll use them first)*
> **B)** No, generate what the site needs *(Recommended if you have none)*
> **C)** No, and keep it simple without pictures for now

If Step 0 found no media folder (or an empty one), or they already said they
have no photos, drop option A and say so in one line ("I didn't find any
photos in the folder"). If they want to sell
online, don't ask anything more about it: the site gets an Order button that
emails the order to them (or links to a store they already have) until a
real store is connected, and the README says so.

If B (or A plus "make more"):

> **What should I generate?**
> **A)** Images plus a short hero video that plays as visitors scroll *(Recommended)*
> **B)** Images only
> **C)** Nothing, I'll add my own later

**Then write `copy/brand-kit.md`** with these sections, filled from the
answers (invent tastefully for anything left open; mark invented contact
details as placeholders):

1. Name, one-line description, slogan
2. Positioning and who it's for
3. Personality (5–8 adjectives) and voice notes for the copy
4. Palette (hex codes: background, surface, text, muted, one accent, one
   optional second accent, line) and two Google Fonts (heading, body)
5. The goal of the site and its main call to action
6. Pages and sections, in order, with one line each on what goes there
   (default for a local business: Hero · trust line · Services · About / why
   us · Work or gallery only if there are images · Testimonials only if they
   gave real ones · Contact with form, phone, address or service area, hours ·
   Footer)
7. Contact details and hours, each line marked "from the owner" or "PLACEHOLDER"
8. Media plan: what exists in `media/`, what will be generated (shot list),
   and the hero: video or image
9. Design notes: one signature element unique to this site, what to avoid

Create the folders `media/ assets/images/ assets/videos/ assets/references/ copy/ website/`
(`media/` is where the viewer drops their own photos later).

Show the viewer a short summary (name, look in one sentence, the section
list, the media plan) and ask (clickable):

> **A)** Looks good, keep going *(Recommended)*  **B)** Change something

End the step with one line on what happens next: media (if any), then the
build, and that hosting gets sorted while the site builds. If the media plan
is none, that line also says Step 2 is skipped, and their "looks good"
answer starts Step 3 directly in your next turn.

---

## Step 2 of 5 — Media

Skip this step entirely if the media plan says none: Step 1's closing line
already said so, and the viewer's "looks good" starts Step 3 in the same
turn. No extra hand-off question in between.

**If media is wanted and the Higgsfield tools are missing**, say exactly this
and stop:

> To generate images and video I need the Higgsfield connector. It takes two
> minutes:
> 1. Create a free Higgsfield account here: https://createaprowebsite.com/Higgsfield
>    (that's the channel's partner link; it supports the channel at no extra
>    cost to you, and the free plan is enough to start).
> 2. In Claude: Customize → Connectors → Add custom connector. Name it
>    Higgsfield, paste `https://mcp.higgsfield.ai/mcp`, click Connect, and
>    sign in.
> 3. Close Claude completely, open it again, come back to this same chat, and
>    say "continue". Everything here is saved. Connectors only load when the
>    app starts, so this restart is expected.
>
> Or, if you'd rather skip it: say "use my own photos" and drop them into the
> media folder, or "no pictures for now".

When they come back and say "continue", check for the tools again and carry
on. Never try to work around the restart; a chat that is already running
cannot see a connector added during it.

**If a hero video was chosen and Step 0 found neither ffmpeg nor Node.js**,
say this once, before any generation:

> One small thing for the video: to make it scroll smoothly I need a free
> tool called Node.js on your computer. Download it from https://nodejs.org
> (the LTS version), run the installer with the defaults, then come back
> here and say "continue". No restart of Claude needed. If you'd rather
> skip it, say "skip" and I'll use the video as-is; it'll still work, just a
> little less smooth.

**If the tools are present:**

1. Credits: reuse the Step 0 balance unless something has been generated
   since; say the number in one line.
2. **Images first.** Plan the shots from the brand kit: a hero image (16:9,
   the subject on one side with calm space for the headline), then one
   supporting image per section that shows a product, place, process, or
   people (skip the trust line, contact, and footer), 3–6 in total, all in
   the same lighting and palette, no text, no logos, no real brands. Model:
   the connector's default general image model (`gpt_image_2` or its newer
   version); hero at the highest quality tier and 2k, supporting images one
   tier down. Preflight every image call with `get_cost: true`, state the
   total, wait for a go, generate, then read every image. One unrequested
   re-roll per image is allowed if it costs under 5 credits; say so when you
   do it. Save to `assets/images/` with clear names.
3. **Then the hero video, if chosen.** Propose ONE film concept in three or
   four sentences: one continuous, slow camera move; the subject stays
   centered; the shot starts calm (the hero text sits over the first frame)
   and ends resting; 10 seconds. Offer clickable: **A)** Go with this
   *(Recommended)* **B)** Different idea. Now that the hero image exists,
   preflight the real video call with it as the reference, state the price,
   and wait for a second go. Model: `seedance_2_5` with
   `mode: "omni_reference"`, the hero image job id as the image reference,
   `resolution: "1080p"`, `bitrate_mode: "high"`, no audio. If that model is
   gone, use the connector's default video model that accepts a start image,
   pass 1080p and its highest quality option, and name it. Never generate
   720p; it has to be regenerated later. Save to
   `assets/videos/BRAND-hero.mp4`, extract start / mid / end frames, look at
   them, and have the viewer watch the file before anything is built around
   it. Offer your honest critique. If they reject it, take their feedback and
   re-roll once (cost stated); if a concept fails three times, change the
   concept, not the prompt.
4. Update the media plan in the brand kit with the filenames.

End with a two-line recap of what was made and what it cost, then:

> Step 2 of 5 done. Next I build the site, which takes about 10–15 minutes.
> Say "go" and feel free to leave it running.

---

## Step 3 of 5 — Build

Read `copy/brand-kit.md` and the **Build recipes appendix** at the bottom of this file before writing code. No questions in this step. Tell the viewer
roughly how long it takes (10–15 minutes with media, a few minutes without)
and that they can leave it running.

**Order of work:**

1. **Media in.** Hero video (if any): process it per the recipes into
   `website/assets/bg.mp4` plus `poster.jpg` and `ending.jpg`. All images
   (theirs and generated): compressed copies into `website/assets/img/`.
2. **Scaffold** `website/index.html`, `style.css`, `main.js`, and
   `website/README.md`. Plain files, relative paths, CDN scripts only if
   there is a hero video.
3. **The hero.** Video: the fixed-background layer stack, Blob loader, and
   gated scroll scrub from the recipes; poster on phones. Image: the
   full-bleed image hero with the slow drift. No media: a typographic hero on
   the brand palette with the signature element.
4. **Sections** in the brand kit's order. Copy is real, specific, and short,
   in the brand's voice, using the viewer's own words where they gave them.
   No lorem ipsum, no stock filler, no invented testimonials.
5. **Design.** CSS variables from the palette; Google Fonts trimmed to the
   weights used; the accent only on CTAs and highlights; one signature
   element; no two adjacent sections sharing the same layout skeleton;
   generous spacing; real `<title>`, meta description, Open Graph tags,
   `theme-color`, an inline SVG favicon.
6. **Motion.** Entrances on scroll; one living detail per section at whisper
   level; scroll scrub only if there is a video; everything visible at rest;
   reduced-motion respected.
7. **The details people forget** (recipes §10): the form's `mailto:` and real
   success state, `tel:` links, the map link, hours as text, alt text on
   every image, lazy loading below the fold, a working mobile menu, 44px tap
   targets.
8. **Mobile first.** Check 375px before desktop. No horizontal scroll, hero
   copy readable on a phone.
9. **Self-test** per the recipes, including the copy gate. You start the
   local server yourself, in the background, and keep it running; the viewer
   only ever clicks a link. If there is no image at all for `og:image`, make
   a simple one from the wordmark on the brand background (recipes §10) or
   leave the tag out; never point it at a file that doesn't exist.

Finish with the exact preview URL and one line on how to open it (the Preview
button in Claude Code, or the localhost link in a real browser, which is the
true preview for scroll-video pages). Then:

> Step 3 of 5 done. The site is running at <url>. Scroll all the way through
> on your computer and on your phone if you can, then tell me everything
> you'd like changed. Big changes first, small ones after.

---

## Step 4 of 5 — Go back and forth

This step repeats until the viewer says they are happy.

- Take feedback as a batch. Restate it as a numbered list, make all the
  changes, and report what changed in plain words. Casual notes like "this
  part feels boring" are good bug reports; translate them yourself.
- Structural changes (sections, layout, hero) before cosmetic ones (colors,
  copy, spacing).
- If they select an element or attach a drawing in Claude Code, target
  exactly that element.
- If they ask for new pictures, run only the relevant part of Step 2 (cost
  stated, go, inspect) and come back here. Never regenerate otherwise.
- Before finishing, re-check the things people forget: real contact details,
  working CTA links, social links, `<title>` and meta description, favicon,
  the mobile view, and the copy gate.

When the viewer is happy, ask (clickable):

> Ready to put it live on the internet? **Yes, publish it** / Not yet

---

## Step 5 of 5 — Publish

Runs when the viewer says yes above, or any time they say "publish",
"deploy", "put it live", or "push it to Hostinger". The site goes live on
Hostinger through the Hostinger connector, in this same chat.

**Check the connector first.** Look for Hostinger tools: either named tools
(like `hosting_listWebsitesV1`) or a Hostinger `search` + `execute` pair. With
the pair, find each operation by keyword with `search` (it returns the exact
operation name and input schema) and run it with `execute`.

- **Connected** → go straight to the publish steps. The first Hostinger call
  may open a browser login; warn the viewer before that call: *"A browser
  window may open for you to sign in to Hostinger and click Allow."*
- **Not connected** → say this and stop:

  > Publishing needs a Hostinger hosting plan and the Hostinger connector.
  > If you haven't already, claim your hosting plan here:
  > https://www.hostg.xyz/aff_c?offer_id=519&aff_id=108612&url_id=6771
  > That's the channel's partner link with the current discount; it supports
  > the channel at no extra cost. Grab your free domain while you're there.
  > Then add the connector inside Claude: Customize → Connectors → search
  > "Hostinger Connector" → add it → sign in with your Hostinger login → Allow.
  > On that same screen, set the read-only tools to Allow so publishing
  > doesn't stop to ask on every step.
  > Last step: close Claude completely, open it again, come back to this
  > same chat, and say "continue". Everything here is saved. Connectors only
  > load when the app starts, so this restart is expected, not a problem.

  Then wait. Setting up hosting can take them away for a while. Do not fill
  the wait with more hosting questions. Never skip the restart or try to work
  around it: a chat that is already running cannot see a connector added
  during it. When they come back and say "continue", check for the tools
  again and follow **Connected**.

**Publish steps:**

1. **Pick the address.** List the account's websites and domains. If a
   domain clearly matches the business, propose it (clickable): *"I can see
   <domain> on your account. Put the site there, or on a free temporary
   address first?"* Never assume the match. If the domain they just bought
   isn't listed yet, wait a minute and list again. If nothing fits, offer a
   free temporary subdomain; it's a real option and a custom domain can be
   connected later.
2. **Set up the website** on that domain if it isn't set up on the hosting
   plan yet. A domain registered at Hostinger points itself; nothing to
   configure. A new website shows up in the list before its setup
   finishes: poll the website setups (`hosting_websites_list-setups`) until
   `completed` before uploading anything.
3. **Patch the live URL** into `og:url` and `og:image` in `index.html` (use
   the editor, never a shell find-and-replace).
4. **Deploy** the CONTENTS of `website/`: `index.html` must be at the top
   level of what's uploaded, never nested in a folder. Their `media/` and the
   raw `assets/` never ship. Two routes; pick by what is connected, and never
   tell the viewer a deploy tool is "missing":
   - **A folder-deploy tool exists** (`hosting_deployStaticWebsite`) → point
     it at `website/`.
   - **No folder-deploy tool** (the hosted connector from Claude's
     Connectors directory) → follow the upload recipe in the going-live
     section of the build recipes: zip the contents of `website/`, request an
     upload URL, push the zip with curl, then deploy the archive. Say the
     upload takes a few seconds per handful of MB. This route is normal.
5. **Verify it yourself** before telling the viewer: the live URL returns 200
   over HTTPS and contains the brand name, the hero media URL itself serves,
   the browser console is clean, the video scrubs if there is one. A
   brand-new domain's certificate can take a few minutes; if the browser
   shows a security warning right after the first deploy, say so, wait, and
   re-check.
6. **Hand it over** with the live URL and ask them to open it on their phone
   as well as their computer.
7. **Turn on auto-deploy.** Say it out loud and then honor it: *"From now on,
   every time you approve a change here, I'll publish it to the live site
   automatically and confirm with the URL. You never have to ask."*

Close with:

> Your site is live at <url>. Any change you want, describe it here and I'll
> update the live site. The files stay in this folder.

---

## When the viewer comes back later

If `copy/brand-kit.md` and `website/` already exist, do **not** restart the
steps. If they ask to publish, deploy, or go live, go straight to Step 5. If
the site is already live, every approved change gets deployed again (Step 5,
item 7). Otherwise read the brand kit and the Build recipes appendix, and
treat the request as a Step 4 revision. If they ask for new media, run only
the relevant part of Step 2 (cost stated, go, inspect) and return to Step 4.

---

## Build recipes appendix

### Stack

- Plain HTML, CSS, and vanilla JavaScript in `website/`:
  `index.html`, `style.css`, `main.js`, `assets/img/`, and (only if there is a
  hero video) `assets/bg.mp4`.
- Libraries only when there is a hero video, loaded from a CDN with pinned
  versions, placed before `main.js`:
  ```html
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js"></script>
  ```
  A site with no hero video needs no library at all: IntersectionObserver and
  CSS do the entrances.
- Google Fonts with `preconnect`, only the weights used.
- Preview over HTTP, never `file://` (the Blob loader is blocked on `file://`):
  the Preview button in Claude Code, or a server *you* start in the background
  from inside `website/` and leave running: `python3 -m http.server 4173` →
  http://localhost:4173. macOS ships python3. The viewer only clicks the link.
- Images: compress copies into `website/assets/img/` at about 1920px wide,
  one quality pass. On a Mac with no ffmpeg:
  `sips -Z 1920 -s format jpeg -s formatOptions 82 in.png --out website/assets/img/name.jpg`.
  Keep the originals in `assets/`.

### 1. Process the hero video (only if there is one; do it first)

Raw AI video seeks badly when scrubbed. Re-encode to all-keyframe H.264, no
audio, then pull the poster and ending frames.

With system ffmpeg (`which ffmpeg`):

```bash
mkdir -p website/assets/img
ffmpeg -y -i "assets/videos/BRAND-hero.mp4" -an \
  -c:v libx264 -preset slow -crf 18 -g 1 -keyint_min 1 -sc_threshold 0 \
  -pix_fmt yuv420p -movflags +faststart website/assets/bg.mp4
ffmpeg -y -i website/assets/bg.mp4 -frames:v 1 -q:v 2 website/assets/img/poster.jpg
ffmpeg -y -sseof -0.1 -i website/assets/bg.mp4 -update 1 -frames:v 1 -q:v 2 website/assets/img/ending.jpg
```

Size target: roughly 6–12 MB for a 10-second 1080p clip. If it lands far
above that, first try `-g 8 -keyint_min 8` (a keyframe every 8 frames still
scrubs cleanly), then raise `-crf` toward 22, then downscale
(`-vf scale=1728:-2`). Change one variable at a time and judge by scrubbing.

Without system ffmpeg: if `node --version` works, use the `ffmpeg-static`
binary in a throwaway `tools/` folder (nothing global, nothing the viewer has
to do):

```bash
mkdir -p tools && cd tools && npm init -y >/dev/null 2>&1 && npm install ffmpeg-static >/dev/null 2>&1 && cd ..
node -e 'const f=require("./tools/node_modules/ffmpeg-static");const {execFileSync:x}=require("child_process");
const r=a=>x(f,a,{stdio:"inherit"});const i=process.argv[1];
r(["-y","-i",i,"-an","-c:v","libx264","-preset","slow","-crf","18","-g","1","-keyint_min","1","-sc_threshold","0","-pix_fmt","yuv420p","-movflags","+faststart","website/assets/bg.mp4"]);
r(["-y","-i","website/assets/bg.mp4","-frames:v","1","-q:v","2","website/assets/img/poster.jpg"]);
r(["-y","-sseof","-0.1","-i","website/assets/bg.mp4","-update","1","-frames:v","1","-q:v","2","website/assets/img/ending.jpg"]);' "assets/videos/BRAND-hero.mp4"
```

If neither ffmpeg nor Node exists and the viewer chose "skip" when Step 2
offered the Node.js installer, copy the raw mp4 to `website/assets/bg.mp4`
as-is, make the poster with the first frame Higgsfield returned (or the hero
image), and say in one line that scrubbing may feel slightly less smooth
than it could. Don't bring the install up again.

#### Inspect frames before building

```bash
mkdir -p assets/review
ffmpeg -y -ss 0 -i raw.mp4 -frames:v 1 -q:v 2 assets/review/start.jpg
ffmpeg -y -ss 5 -i raw.mp4 -frames:v 1 -q:v 2 assets/review/mid.jpg
ffmpeg -y -sseof -0.1 -i raw.mp4 -update 1 -frames:v 1 -q:v 2 assets/review/end.jpg
```

Read all three. The hero text sits over the start frame, so it needs calm
space; the end frame should be resting, not mid-drift.

#### The tail trim (cheaper than a re-roll)

If the shot is strong until the subject drifts near the end, cut at the last
steady frame instead of regenerating. The page maps scroll to *progress*, not
seconds, so a shorter clip costs nothing:

```bash
ffmpeg -y -i raw.mp4 -t 8.4 -an -c:v libx264 -preset slow -crf 18 -g 1 -keyint_min 1 \
  -sc_threshold 0 -pix_fmt yuv420p -movflags +faststart website/assets/bg.mp4
```

Re-extract the poster and ending frames afterward.

### 2. Layer architecture (hero video sites)

| Element | z-index | Role |
|---|---:|---|
| `#bgv` `.bg-video` | 0 | fixed, full-screen, `object-fit: cover`, scrubbed by scroll |
| `.mobile-poster` | 0 | poster image, shown on phones and until the video is ready |
| `.bg-tint` | 1 | radial darkening + gradients for readability |
| `#page` | 10 | all sections |

```html
<video id="bgv" class="bg-video" muted playsinline preload="none" aria-hidden="true" tabindex="-1"></video>
<div class="mobile-poster" aria-hidden="true"></div>
<div class="bg-tint"></div>
<main id="page"> …sections… </main>
```

No `src` and no `poster` in the HTML. Both are set from JavaScript inside the
gated path below, so phones never download the video.

```css
.bg-video { position: fixed; inset: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0; will-change: transform; }
.bg-tint  { position: fixed; inset: 0; z-index: 1; pointer-events: none;
  background: radial-gradient(120% 90% at 50% 45%, rgba(0,0,0,.25), rgba(0,0,0,.75) 100%); }
#page     { position: relative; z-index: 10; }
html, body { overflow-x: hidden; overflow-x: clip; }
```

The video is the single background for the whole page, never an embedded
player or a small section video. The page must be complete and beautiful if
the video never loads.

### 3. Image hero (sites with no video)

A full-bleed hero image with the same legibility system (§7): the image as a
`background-image` on the hero section (or an `<img>` with `object-fit: cover`
behind the copy), a scrim, the text-shadow token, and the copy placed on the
image's calm side. Add a slow 12–20 s `transform: scale(1 → 1.06)` drift on
the image (paused for reduced motion) so the hero feels alive without a video.
Below the hero, sections sit on the brand's surface colors, not on imagery.

### 4. Brand tokens

```css
:root {
  --bg: …; --surface: …; --surface-2: …; --text: …; --muted: …;
  --accent: …; --accent-rgb: r, g, b; --accent-2: …; --line: …;
  --font: "Body Font", system-ui, sans-serif;
  --font-head: "Heading Font", var(--font);
  --tshadow: 0 1px 2px rgba(5,5,10,.9), 0 3px 12px rgba(5,5,10,.7), 0 10px 44px rgba(5,5,10,.7);
}
```

Accent only on CTAs, active states, highlights, and small glows. The canvas is
never pure `#000` or `#fff`; tint it toward the imagery. Heading font on: nav
wordmark, hero title, section headings, feature titles, CTA title, footer
wordmark. Load only the font weights used, with `preconnect`.

### 5. Load the video as a Blob, scrub it with gated seeks (main.js core)

Two rules from real deployments. **Blob:** many hosts (shared hosting
included) lack HTTP Range support, so `currentTime` seeks clamp to zero on
the live site while working perfectly on localhost. Fetching the whole file as
a Blob and playing the object URL works everywhere. **Gated seeks:** never
write `currentTime` while a seek is in flight; piled-up seeks are the
difference between smooth and choppy in Chrome.

```js
// CDN globals: gsap, ScrollTrigger, Lenis (scripts loaded before this file)
gsap.registerPlugin(ScrollTrigger);

const lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
lenis.on("scroll", ScrollTrigger.update);
gsap.ticker.add((t) => lenis.raf(t * 1000));
gsap.ticker.lagSmoothing(0);

const bgVideo = document.getElementById("bgv");
const STATIC_HERO = matchMedia("(max-width: 768px), (hover: none), (prefers-reduced-motion: reduce)");

// ---- gated seeks (deadlock-safe) ----
let seekBusy = false, pendingTime = null, lastVideoT = -1;
function requestSeek(t) {
  if (!bgVideo.duration) return;
  if (Math.abs(t - lastVideoT) < 0.008) return;     // write only on change
  if (seekBusy) { pendingTime = t; return; }        // coalesce to newest
  seekBusy = true; lastVideoT = t; bgVideo.currentTime = t;
}
bgVideo.addEventListener("seeked", () => {
  seekBusy = false;
  if (pendingTime !== null) { const t = pendingTime; pendingTime = null; requestSeek(t); }
});
bgVideo.addEventListener("error", () => {           // the deadlock escape + fallback
  seekBusy = false; pendingTime = null;
  document.body.classList.add("video-failed");     // CSS shows the poster layer
});

// ---- scroll → video time ----
function scrubVideo() {
  if (!bgVideo.duration) return;
  const p = gsap.utils.clamp(0, 1, window.scrollY / Math.max(1, lenis.limit));
  requestSeek(p * (bgVideo.duration - 0.05));
}

// ---- load only on scrub-capable screens, as a Blob ----
async function initVideo() {
  document.querySelector(".mobile-poster").style.backgroundImage = "url('assets/img/poster.jpg')";
  if (STATIC_HERO.matches) return;                  // phones / reduced motion: poster only
  try {
    const res = await fetch("assets/bg.mp4");
    bgVideo.src = URL.createObjectURL(await res.blob());
    bgVideo.load();
    bgVideo.addEventListener("loadedmetadata", () => { scrubVideo(); document.body.classList.add("video-ready"); }, { once: true });
    lenis.on("scroll", scrubVideo);
  } catch { document.body.classList.add("video-failed"); }
}
initVideo();
window.__bgv = bgVideo; window.__lenis = lenis;   // for the self-test
```

```css
.mobile-poster { position: fixed; inset: 0; z-index: 0; background: center / cover no-repeat; opacity: 1; transition: opacity .6s ease; }
body.video-ready .mobile-poster { opacity: 0; }
body.video-failed .bg-video { display: none; }
@media (max-width: 768px), (hover: none), (prefers-reduced-motion: reduce) {
  .bg-video { display: none; }
  body.video-ready .mobile-poster { opacity: 1; }
}
```

Relative paths (`assets/bg.mp4`, not `/bg.mp4`) so the site works at a domain
root and in a subfolder alike. The CSS media query and the JS `STATIC_HERO`
string must match exactly. For a video over ~15 MB, stream the Blob with a
progress ring instead of a bare `await res.blob()` so the page is usable while
it downloads.

### 6. Pinned impact statement (optional, hero-video sites)

One pinned section after the hero where a short statement reveals word by
word as the viewer scrolls (ScrollTrigger `pin: true`, `scrub: true`, stagger
the words' opacity over the pin distance, `invalidateOnRefresh: true`). Pace
it in scroll distance so a line survives several normal scroll flicks. One to
three pins per site at most; none on phones.

### 7. Legibility over imagery

Every text block over the video or hero image gets all three: the global
`.bg-tint` (or hero scrim), a local scrim behind the block, and the
text-shadow token. Tune against the *busiest* frame the text sits over, not
the average.

```css
.hero__copy { text-shadow: var(--tshadow); position: relative; }
.hero__copy::before { content: ""; position: absolute; inset: -8% -6%; z-index: -1; pointer-events: none;
  background: radial-gradient(ellipse 74% 62% at 50% 50%, rgba(5,5,10,.62) 0%, rgba(5,5,10,.4) 46%, rgba(5,5,10,0) 76%); }
.btn { text-shadow: none; }
```

Small labels over imagery get a chip instead of a big scrim:
`background: rgba(8,8,15,.55); backdrop-filter: blur(10px); border-radius: 10px`.

### 8. Glass panels and buttons

```css
.glass { position: relative; overflow: hidden;
  background: rgba(18,19,25,.46);
  border: 1px solid color-mix(in srgb, var(--line) 75%, transparent);
  backdrop-filter: blur(22px) saturate(1.18); -webkit-backdrop-filter: blur(22px) saturate(1.18);
  box-shadow: 0 24px 80px rgba(0,0,0,.32); border-radius: 24px; }
.glass::before { content: ""; position: absolute; inset: 0; pointer-events: none;
  background: linear-gradient(135deg, rgba(255,255,255,.08), transparent 38%, rgba(var(--accent-rgb), .05)); }
.glass > * { position: relative; z-index: 2; }
.btn--primary { background: linear-gradient(135deg, var(--accent), color-mix(in srgb, var(--accent) 70%, #fff 20%)); color: var(--bg); }
@media (pointer: coarse) { .btn { min-height: 44px; display: inline-flex; align-items: center; justify-content: center; } }
```

For a light brand, invert: `rgba(255,255,255,.55)` background, dark text, and a
lighter tint layer. Not everything is a glass card; use it where readability
over imagery needs it, plain surfaces elsewhere.

### 9. Entrances and living details

- IntersectionObserver adds `.in`; children stagger in 60–150 ms apart. Prefix
  start and end states with the container class (`.card .part`, `.card.in .part`)
  so a later rule can't cancel them, and zero the stagger delays after the
  entrance so hovers don't lag. Everything is visible at rest if JS fails.
- One living element per section at whisper level (a slow glow or drift, 4 s or
  longer, negative `animation-delay` so it is mid-cycle at first paint).
- Animate only `transform` and `opacity`. Never tween `filter` on large layers.
- Reduced motion: show final states, kill transitions, never load the video.

### 10. The contact form and the details people forget

- The form posts nowhere by default: on submit, open a `mailto:` to the brand
  kit's email with the fields in the body, and show a real success state.
  Say plainly in `website/README.md` where a visitor's message ends up. If the
  contact details are placeholders, say so there too.
- Phone numbers are `tel:` links; the address links to Google Maps (a mobile
  business links its service area instead, or skips the map link); hours are
  real text, not an image.
- `og:image` with no photos: render a 1200×630 SVG of the wordmark on the
  brand background to `website/assets/img/og.jpg` (`qlmanage -t -s 1200
  og.svg -o .` then `sips -s format jpeg`), or leave the tag out. Never point
  it at a file that doesn't exist.
- `<title>`, meta description, `og:title`, `og:description`, `og:image`,
  `og:url`, `theme-color`, an inline SVG favicon, one `<h1>`, alt text on
  every image, `loading="lazy"` below the fold.
- Mobile first: a working hamburger menu, 44px tap targets, no horizontal
  scroll at 375px, hero copy readable on a phone.

### 11. Self-test (before showing the viewer)

1. Serve over HTTP; console has zero errors at desktop and 375px widths.
2. Hero video sites: `window.__bgv.readyState === 4`; scrub at top, middle,
   bottom, then fast. Phone width: poster shows, no video request.
3. Every button and link works; the form's success state is real; `tel:` and
   `mailto:` are correct.
4. Hero text readable over the busiest frame; cards legible.
5. Rename `bg.mp4` temporarily: page still complete over the poster.
6. Copy gate (site copy only; the step labels in the chat keep their dashes): `grep -nE "—|leverage|seamless|empower|unlock|robust|actionable|data-driven|solutions|elevate|delve|lorem" website/index.html` → rewrite every hit.
7. Fresh-eyes pass: does anything float unexplained, or read as filler?

### 12. Going live (Hostinger)

- Deploy the **contents** of `website/` (with `index.html` at the top level of
  the zip), never the folder itself, or the live site shows a directory
  listing. Raw media in `assets/` and the viewer's `media/` never ship; only
  `website/` does.
- `og:url` and `og:image` need absolute URLs; patch them with the live domain
  before zipping. Use the editor, not a shell one-liner (encoding damage is a
  real failure).
- Verify the live URL yourself: HTTPS 200, the hero video or image URL itself
  serves, console clean, scrub works. A brand-new domain's certificate can take
  a few minutes.

#### Two deploy routes; pick by what is connected

- **A folder-deploy tool exists** (`hosting_deployStaticWebsite`, provided by
  the locally installed connector): point it at `website/` and let it upload.
- **No folder-deploy tool** (the hosted connector at `mcp.hostinger.com`,
  which Claude's Connectors directory and the Hostinger plugin add): that
  server cannot see this computer's files, so use the upload recipe below.
  This route is normal, not a fallback. Never tell the viewer a tool is
  "missing".

#### Upload recipe for the hosted connector

The current hosted connector is a `search` + `execute` pair: find each
operation below with `search` (it returns the exact name and input schema)
and run it with `execute`. Older versions exposed the same steps as named
tools, so both names are given.

1. List the websites filtered by the domain (`hosting_websites_list`, or the
   older `hosting_listWebsitesV1`) → note `username`. If the site was just
   created, poll `hosting_websites_list-setups` until `completed` first
   (uploads return 409 while setup runs).
2. Zip the contents of `website/` from inside it so `index.html` sits at the
   zip's top level, and keep the zip outside the folder:
   `cd website && zip -qr ../site.zip . -x "*.DS_Store"`
3. Generate the upload URL (`hosting_files_generate-upload-url`, or the
   older `hosting_generateUploadURLV1`) with `{ "username", "domain" }` →
   `url`, `auth_key`, `rest_auth_key`.
4. Push the zip with plain curl (a TUS upload; it uses the two keys from
   step 3, not the login). Say in one line that a hero-video zip takes a few
   seconds per handful of MB, so the wait reads as work:
   ```bash
   FILE=site.zip; SIZE=$(wc -c < "$FILE")
   curl -sS -i -X POST "${url}/${FILE}?override=true" \
     -H "X-Auth: ${auth_key}" -H "X-Auth-Rest: ${rest_auth_key}" \
     -H "Tus-Resumable: 1.0.0" -H "Upload-Length: ${SIZE}" -H "Upload-Offset: 0"
   # expect 201 Created
   curl -sS -i -X PATCH "${url}/${FILE}?override=true" \
     -H "X-Auth: ${auth_key}" -H "X-Auth-Rest: ${rest_auth_key}" \
     -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" \
     -H "Upload-Offset: 0" --data-binary "@${FILE}"
   # expect 204; the Upload-Offset response header equals SIZE when done
   ```
   `override=true` means a retry of the same filename replaces it, so a
   failed upload is safe to run again.
5. Deploy the archive (`hosting_websites_deploy-static-site-archive`, or
   the older `hosting_deployStaticSiteArchiveV1`) with
   `{ "username", "domain", "archive_path": "site.zip" }` — the bare
   filename, no folder. This wipes the site root before unpacking, which is
   right for a fresh site and is the normal update on a re-deploy. Never
   point it at a website that isn't this project's.
6. Verify harder than a 200: a fresh or failed deploy can still serve a
   parking page. Fetch the live HTML and grep for a string you know is in
   this build (the brand name in the `<title>`). If it doesn't match, clear the cache
   (`hosting_cache_clear-website`, or the older `hosting_clearWebsiteCacheV1`) and re-check once before reporting failure.

### Gotchas

1. Raw AI video scrubs badly → re-encode (all-keyframe, or `-g 8`) when a
   tool for it exists.
2. Scrubbing works locally but not live → the host lacks Range support; the
   Blob loader fixes it.
3. Choppy at the top and bottom of the hero in Chrome → un-gated seeks or
   per-frame DOM writes; the patterns above fix it.
4. Readability beats the imagery. Deepen the scrim, or move copy to the calm side.
5. Pins shift later triggers → `invalidateOnRefresh: true`, call
   `ScrollTrigger.refresh()` after layout changes.
6. Claude's built-in preview pane struggles with scroll-video pages → the
   browser at the localhost link is the true preview.
7. Never open the site via `file://` — `fetch` is blocked, so the Blob loader
   falls back to the poster on purpose.
8. Keep motion slow — fast motion is unpleasant when scrubbed by hand.
9. Absolute paths (`/assets/...`) break when the site lives in a subfolder;
   use relative paths everywhere.
