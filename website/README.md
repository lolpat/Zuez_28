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
- **Pick dates** chooses any from–to range. The **Daily summary** table lists every trading day in
  the range: trades, won / lost, win rate, lots, net profit and the running total. Tapping a day
  shows that day's trades.
- **Automatic history** pulls trades in by itself; see the next section. Import still works as a
  fallback, and trades that were imported before are not duplicated by a sync.

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
