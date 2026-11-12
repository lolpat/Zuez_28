# Order The Market: members' portal

Plain HTML, CSS and JavaScript. No build step, nothing to install. Upload the contents of this
folder to any web host.

## Pages

| File | What it is |
|---|---|
| `index.html` | Public landing page (Thai / English) |
| `register.html` | Sign-up: name, email, Telegram, broker, MT4/MT5 account number, referral code. `register.html?ref=CODE` fills the code in. |
| `login.html` | Log in, forgotten password, and (demo mode only) one-click demo logins |
| `app.html` | The portal: Dashboard, Journal, Tools, IB Network (IBs and owner only), Profile |

## Right now it runs in demo mode

`js/config.js` has no database keys yet, so the portal shows sample members and trades and keeps
every change **in the visitor's own browser only**. Nothing is shared between people. This is for
looking around and testing, not for real members.

Demo logins on the login page: **Member** (Krit T.), **IB** (Somchai K.), **Owner**.
Or type a sample email (`krit@demo`, `somchai@demo`, `nok@demo`, `owner@demo`) with any password.

## Settings (in `js/config.js`)

- `TELEGRAM_URL` / `TELEGRAM_HANDLE`: set to https://t.me/zuez_28. Every "Talk to the team" button and
  the landing page's Telegram button open it. **This is where visitors' questions end up.**
- `BROKERS[]`: your IB sign-up link and broker referral code for Vantage (ZUEZ28), PU Prime
  (OTM2028) and VT Markets (OTM2028). The landing page shows each code with a Copy button next to
  an "Open through our link" button. These broker codes are separate from the portal referral
  codes IBs share for registering on this site.
- `AUTO_SYNC`: shows the "Automatic history" feature (connect an MT4/MT5 account with its investor
  password). Leave it `true` once the steps in "Automatic MT4/MT5 history" below are done; set it to
  `false` to hide the feature until then.

## Going live with real accounts (Supabase, free tier)

1. Create a free project at supabase.com.
2. Supabase > SQL Editor > paste all of `../supabase/schema.sql` > Run.
3. Supabase > Authentication > URL Configuration: set Site URL to your live address.
4. Supabase > Project Settings > API: copy the **Project URL** and the **anon public key** into
   `SUPABASE_URL` and `SUPABASE_ANON_KEY` in `js/config.js`. (The anon key is meant to be public;
   the database rules decide who sees what.)
5. Register your own account on the site, then in the SQL Editor run once:
   `update public.profiles set role = 'owner', status = 'approved' where email = 'you@example.com';`
6. Make your IB partners IBs from the IB Network page (Owner > "Make IB"). Each IB gets a
   referral code and sign-up link.

## Who sees what (enforced by the database, tested)

- A member sees only their own data.
- An IB sees everyone below them at every level (clients and sub-IBs' clients): name, email,
  Telegram, broker account, status and a journal summary (trade count, net profit, win rate). They
  can approve or reject people below them.
- Everyone sees **only the name and Telegram of the person directly above them**. Nobody sees
  anyone higher up, or any other line.
- The owner sees everyone and decides who is an IB.
- New sign-ups wait as "pending" until someone above them approves. Pending members cannot add
  trades. Sign-ups with no valid referral code are visible only to the owner.

The landing page FAQ tells members their IB line can see a summary of their results.

## The journal

- **Import:** MT5 > History tab > right-click > Report > HTML. MT4 > Account History > right-click
  > Save as Detailed Report. CSV exports with Symbol / Type / Volume / Open Time / Close Time /
  Profit columns also work. Re-importing the same report skips trades already there.
- Report times are broker server time (GMT+2, GMT+3 during US summer time) and are converted to
  real time, so the London / New York / Asia session stats are correct.
- **Balance** = the starting balance set per account in Profile + all net profit.
- **Trading score** = average of six 0–100 parts: win rate, profit factor, average win vs average
  loss, recovery (net profit ÷ max drawdown), drawdown control, share of profitable weeks.
- **Accounts:** each member can add up to **10** MT4/MT5 accounts from any of the three brokers
  (`MAX_ACCOUNTS` in `js/config.js`; the database refuses an 11th as well). The journal shows three
  broker tiles (PU Prime, Vantage, VT Markets) with each broker's accounts, trades and P/L combined;
  tap one to see only that broker, then pick one of its accounts. **Add account** is one form: broker,
  account number, server and investor password; it adds the account and pulls its history in one go
  (leave the password empty to add it and import reports instead). Server names typed before are
  offered as choices; you can also list each broker's servers in `servers: []` in `js/config.js`.
  **Profile** shows the same accounts as a compact list (Edit opens Manage account).
- **Broker connections (Profile):** for PU Prime, Vantage and VT Markets the member links their
  **client ID at the broker** (not an MT5 number) to say their account is under our IB. Brokers give
  IBs no API to check this, so the owner or an IB above the member confirms it on the IB Network
  page ("Confirm members' broker IDs": compare with the client list in the broker's IB portal, then
  Confirm or Not ours). A confirmed broker shows a tick and "Connected" with no button; otherwise
  there is a Connect button (with our sign-up link and code, then the ID). A member can't confirm
  their own ID, can't change a confirmed one, and an ID can be linked by one member only.
  The pencil on each account opens
  **Manage account**: fix the broker, number, platform, server or starting balance; connect,
  reconnect (wrong or changed investor password), sync or disconnect automatic history; or remove
  the account and its trades. Profile has the same Edit button. A connected account's broker and
  number are locked until it is disconnected.
- **Layout:** six tiles on top (balance, win rate, net P/L, max drawdown, best day, worst day), then a
  full-width **trading calendar** (Monday first, each day's P/L, trades and win rate, a total for each
  week; tap a day to see its trades), then account balance, results by symbol and daily P/L, then four
  stat cards (quick stats, risk, performance, trading summary), the trading score, weekday and session
  charts, the daily summary table and the trade list.
- **Pick dates** chooses any from–to range. The **Daily summary** table lists every trading day in
  the range: trades, won / lost, win rate, lots, net profit and the running total. Tapping a day
  shows that day's trades.
- **Automatic history** pulls trades in by itself; see the next section. Import still works as a
  fallback, and trades that were imported before are not duplicated by a sync.

## Member wins (home page) and Client Profit (portal)

- Profit screenshots members send in move across the home page in two rows (top to the left, bottom
  to the right; hover pauses them) and fill the **Client Profit** page in the portal, with a gallery
  and a full-size viewer (arrows, Esc).
- Add pictures: put the files in `assets/img/wins/` and list them in `WINS` in `js/config.js`, e.g.
  `WINS: ["assets/img/wins/01.jpg", "assets/img/wins/02.jpg"]`. Until then the demo shows empty
  frames and the live site hides the section.
- Use only pictures members agreed to share, with names, account numbers and faces covered. The
  section carries a line saying past results don't guarantee future results.

## Leaderboard

- Members choose to join (Leaderboard page > Join) and pick the name others see. Nothing else about
  them is shown: no email, account number or balance. They can leave any time.
- Only members **in net profit** (after commission and swap) for the period are ranked, by net
  profit. The top 20 are listed: the first 10 show straight away and "Show ranks 11–20" opens the
  rest. A member ranked lower sees their own row under the list. The table also shows return on the starting balance, win rate, profit factor, average
  win / average loss, the current winning streak and a tier (from win rate, profit factor and
  win/loss size; fewer than 3 trades is "Rookie").
- **Live / Demo** switch at the top right: each account is marked live or demo (Profile > Add account;
  a synced account whose server name contains "Demo" is marked demo automatically), and the two are
  ranked separately. Some brokers label a real-money account "Demo"; the site owner can correct any
  account's type (Profile, Live / Demo next to the account). A corrected type is locked, so a sync
  never changes it back. Members can't change the type after adding an account.
- Daily / Weekly / Monthly / All time, on Thai time (weeks start Monday 00:00), with a countdown to
  the next reset.
- In live mode the ranking comes from the database function `leaderboard()` in
  `../supabase/schema.sql`, so members still can't read anyone else's trades.

## Automatic MT4/MT5 history (investor password)

A member opens Journal or Profile > **Connect account**, enters the MT5 server name and the account's
**investor (read-only) password** once, and their whole history comes in. After that a schedule pulls
new trades every 30 minutes, and **Sync now** pulls them on demand.

How it works and what it needs:

- Brokers don't give IBs an API for their clients' trades, so being under the IB is not enough on its
  own. Reading an account's history needs a MetaTrader login, and the investor password is the safe
  one: it can see trades but cannot trade or withdraw.
- The login is done by **MetaApi** (metaapi.cloud), a paid service that keeps a cloud MT4/MT5 terminal
  connected for each account. **It costs money per connected account while it's connected**; check
  the current price on metaapi.cloud before switching this on. Disconnecting an account in Profile
  removes it from MetaApi and stops the charge.
- The investor password is sent once from the member's browser to our Supabase function and on to
  MetaApi over HTTPS. **It is never stored in our database.**
- The code is `../supabase/functions/mt-sync/index.ts`. It was tested against simulated MetaApi
  replies (connect, wrong password, partial closes, positions opened before the first sync,
  re-sync without duplicates, the schedule's secret). It has not run against a live MetaApi account
  yet: do the first real connection yourself with a demo or small account and check the trades match.

Switching it on (one time, about 20 minutes):

1. Create a MetaApi account and copy an API token from https://app.metaapi.cloud/token.
2. Install the Supabase CLI on a computer (https://supabase.com/docs/guides/cli), then from this
   project's folder:
   ```
   supabase login
   supabase link --project-ref YOUR-PROJECT
   supabase secrets set METAAPI_TOKEN=paste-the-token CRON_SECRET=any-long-random-text
   supabase functions deploy mt-sync
   ```
   (Optional: `METAAPI_REGION=london` if your MetaApi account uses London; the default is new-york.)
3. Run `../supabase/schema.sql` again in the SQL Editor (it only adds the new columns), then open
   `../supabase/sync-schedule.sql`, fill in the three values at the top, and run it. That starts the
   30-minute schedule.
4. Keep `AUTO_SYNC: true` in `js/config.js`.

What members see if something is wrong: a wrong password or server name, an account the broker has
closed, or the broker asking for a password change each get their own plain message, and the account
shows "Problem" in Profile until they reconnect.

## Files

- `css/style.css`: all styles (brand colours at the top)
- `js/config.js`: settings above
- `js/i18n.js`: every Thai and English sentence on the site
- `js/store.js`: data layer (demo or Supabase)
- `js/stats.js`: journal maths
- `js/importer.js`: MT4/MT5 report reader
- `js/charts.js`: the SVG charts
- `js/app.js`: the portal; `js/site.js`: landing, login and sign-up
- `js/worldmap.js`: world outline for the market-hours map (Natural Earth, public domain)
- `../supabase/functions/mt-sync/`: automatic MT4/MT5 history; `../supabase/sync-schedule.sql`: its schedule
- `assets/img/`: logo mark (from `brand/logo/`), app icon, share image
