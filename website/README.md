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

## Placeholders to replace (in `js/config.js`)

- `TELEGRAM_URL` / `TELEGRAM_HANDLE`: your real Telegram link. Every "Talk to the team" button and
  the landing page's Telegram button open it. **This is where visitors' questions end up.**
- `BROKERS[].url`: your IB sign-up links for Vantage, PU Prime and VT Markets. Until they are set,
  the landing page shows "Link coming soon".

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
- MT5 auto-sync (pulling trades live with the investor password) is not built yet. It needs a paid
  sync service; see the brand kit for the plan.

## Files

- `css/style.css`: all styles (brand colours at the top)
- `js/config.js`: settings above
- `js/i18n.js`: every Thai and English sentence on the site
- `js/store.js`: data layer (demo or Supabase)
- `js/stats.js`: journal maths
- `js/importer.js`: MT4/MT5 report reader
- `js/charts.js`: the SVG charts
- `js/app.js`: the portal; `js/site.js`: landing, login and sign-up
- `assets/img/`: logo mark (from `brand/logo/`), app icon, share image
