# Order The Market — brand kit

Everything in the site derives from this file. Owner answers are marked "from the owner";
anything not given is marked PLACEHOLDER and must not be presented as fact.

## 1. Name, description, slogan

- **Name:** Order The Market (short: OTM) — from the owner
- **One line (EN):** The members' portal for traders in the Order The Market IB community.
- **One line (TH):** พื้นที่สมาชิกสำหรับเทรดเดอร์ในคอมมูนิตี้ IB ของ Order The Market
- **Slogan:** Your success is our mission / ความสำเร็จของคุณคือภารกิจของเรา — from the owner (logo)

## 2. Positioning and who it's for

- A private portal, not a public signal shop. Only traders who opened their account under the
  Order The Market IB (or one of its sub-IBs) at **Vantage, PU Prime or VT Markets** get in — from the owner.
- Members: Thai and English-speaking retail traders, beginners to intermediate, who talk to the
  community on **Telegram** — from the owner.
- IB partners: introducers who bring clients in and want to see their own network.
- What members get: a trading journal that turns their history into numbers they can learn from,
  calculators, and a direct line to the team. Free for members; the IB relationship is the business.

## 3. Personality and voice

Disciplined, warm, premium, plain-spoken, encouraging, honest about risk, unhurried.

- Talk like a senior trader mentoring a newer one: short sentences, concrete numbers, no hype.
- Never promise profit. Every page that shows results carries a one-line risk note.
- Thai copy is written natively, not translated word for word; English is the second language
  toggle. Keep trading terms traders actually use (Win Rate, Profit Factor, Lot, SL/TP) in English
  inside Thai text.
- Banned: "guaranteed", "get rich", "100%", hype emojis, the copy-gate words in the recipes.

## 4. Palette and fonts

From `brand/README.md` (the logo):

| Token | Hex | Use |
|---|---|---|
| bg | `#1A0405` | page canvas (maroon pushed darker for long reading; never pure black) |
| surface | `#2A0A0B` | cards, sidebar |
| surface-2 | `#420000` | raised cards, active nav (the logo maroon) |
| text | `#F6EBD3` | body text (warm ivory, tinted toward the gold) |
| muted | `#B9A68A` | labels, secondary text |
| accent | `#EED875` | gold: CTAs, active states, key numbers |
| accent-2 | `#ED2024` | red arrow: losses, alerts, sparingly |
| gold-deep | `#B78E4A` | outlines, chart grid, borders on hover |
| line | `#4A1A17` | dividers |
| profit | `#7BC88F` | positive P/L only (muted green that sits with gold) |

- **Heading font:** Kanit (Thai + Latin), 500/600; wordmark-style headings use wide letter-spacing
  in caps like the logo.
- **Body font:** IBM Plex Sans Thai (Thai + Latin), 400/500; numbers use tabular figures.

## 5. Goal and main call to action

- **Visitors (not logged in):** open an account under our IB link at one of the three brokers,
  then register on the portal. CTA: **"Join Order The Market" / "สมัครสมาชิก"**.
- **Members:** log trades and review them in the Journal every week.
- **IB partners:** watch their network grow and approve new members.

## 6. Pages and sections

The site is a small web app, not a one-page brochure. Phase 1 (this build):

**Public**
1. **Landing** — Hero (logo mark, slogan, Join + Log in) · How it works in 3 steps (open account
   via IB link → register with your MT4/MT5 number → get approved) · What members get (Journal,
   tools, Telegram community) · The three brokers as text with IB links · FAQ · Telegram contact ·
   Footer with risk disclaimer.
2. **Register** — name, email, password, Telegram username, broker, MT account number, referral
   code of the IB who introduced them. Account waits for approval.
3. **Log in** — email + password; forgotten password.

**Member portal** (sidebar layout, TH/EN toggle in the top bar)
4. **Dashboard** — welcome, world market-hours clock (Sydney, Tokyo, London, New York), getting
   started checklist, journal headline numbers.
5. **Journal** — the core page:
   - Account picker, period filters (Today, Week, Month, Year, All), Buy/Sell, Win/Loss, symbol.
   - KPI cards: Balance, Total P/L, Profit Factor, Win Rate, Expectancy, Best Session.
   - P/L calendar heatmap, equity curve (cumulative / daily / weekly).
   - Performance score 0–100 with a radar (win rate, profit factor, avg win/loss, recovery,
     drawdown control, consistency).
   - Performance by symbol, by weekday, by session.
   - Trade list; each trade opens a note: what happened, feeling (Calm, Focused, Confident,
     Anxious, FOMO, Revenge, Tired), execution 1–5 stars, tags, lesson.
   - Data in: import an MT4/MT5 history report (HTML/CSV) + add trade manually. MT5 auto-sync is
     designed in but switched off until the owner approves a sync service and its monthly price.
6. **Tools** — Lot size calculator, compound growth calculator.
7. **Profile** — name, Telegram username, language, linked broker accounts.
8. **Contact** — "Talk to the team on Telegram" (opens Telegram), not a live chat in phase 1.

**IB / Affiliate area** (only for users with the IB role)
9. **My network** — rules from the owner:
   - I see **everyone below me**, at every level (my clients and my sub-IBs' clients), as a tree
     and as a searchable list: name, broker, account number, status, join date, journal summary.
   - I see **who is directly above me** (name only).
   - I **cannot** see anyone above my direct upline, or anyone in a branch that is not below me.
   - My upline can see me and everyone below me; they cannot see their own upline's side either.
   - My referral code + share link, pending members to approve.
10. **Owner admin** — the top account sees the whole tree, approves IBs, sets roles.

Phase 2 (not now): Academy, livestream calendar, signal rooms via Telegram bot, AI journal coach,
MT5 auto-sync, live chat.

## 7. Contact details

- Main channel: **Telegram** — from the owner
- Telegram: https://t.me/zuez_28 (@zuez_28) — from the owner
- Email: PLACEHOLDER
- IB referral links for Vantage, PU Prime, VT Markets: PLACEHOLDER (owner to supply)
- No street address or opening hours (online community).

## 8. Media plan

- **Logo:** `brand/logo/` (the owner's own) — `print_transparent.svg` for the site header and hero,
  `icononly_transparent_nobuffer.png` for favicon/app icon.
- `media/`: empty.
- Hero: typographic hero on the brand palette with the logo mark — owner chose "no pictures,
  use the logo". No generated images or video; Step 2 skipped.
- Broker names appear as plain text only; no broker logos or trademarks.

## 9. Design notes

- **Signature element:** the logo's gold crescent becomes a thin gold arc that frames the key
  number on each page (the Journal's performance score, the hero, the network count).
- Dark, warm, premium: maroon depths, gold reserved for what matters, red only for losses.
- Numbers first: big tabular figures, small labels, no decorative charts.
- Avoid: neon trading-app greens, casino energy, stock photos of traders pointing at screens,
  lambo/luxury imagery, fake testimonials, invented performance figures.
- Technical note: logins and the IB hierarchy rules need a real backend. Phase 1 uses Supabase
  (free tier; plain JavaScript from a CDN, nothing to install) with database row-level security so
  the "see down, not up" rule is enforced on the server, not just hidden in the page. Until the
  owner connects Supabase, the portal runs in a demo mode with sample data.
