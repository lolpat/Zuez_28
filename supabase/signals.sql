-- Live signal results. The Telegram bot's webhook (functions/tg-signals) writes here, the website reads the
-- two views at the bottom. Run this once in the Supabase SQL editor (after schema.sql).
--
-- Who can see what:
--   tables  - nobody but the edge function (service role). Row level security is on with no policies.
--   views   - anyone (the anon key on the website): only CLOSED trades (win / loss / break-even) and a
--             count of open trades per room. Entries, stop losses and open trades never leave the database,
--             so VIP signals show up on the website only after the trade has closed.

-- Which forum topic belongs to which room. chat_id null = any chat the bot is in.
create table if not exists public.signal_rooms (
  id bigint generated always as identity primary key,
  chat_id bigint,
  thread_id bigint not null,          -- the topic's message_thread_id (0 = a chat or channel without topics)
  room text not null check (room in ('swing', 'scalp', 'rr', 'hype')),
  unique nulls not distinct (chat_id, thread_id)
);
-- The VIP group's topics, as found in its export (a topic's id is the id of the message that created it):
--   2571 SWING-ATM -> 🥇 SWING ELITE · 2572 Scalping -> ⚡️Scalping PRO · 3 XAUUSD SIGNALS -> RR High Reward · 360 BTCUSD / NAS100
-- Every room is read from the VIP group: the source channels (@WA:SMT for Scalping PRO, PML VIP SIG POMILON for
-- RR) are forwarded into its topics. Pin the rows to the group's chat id once tg_chats shows it:
--   update public.signal_rooms set chat_id = -1003941112920 where chat_id is null;
insert into public.signal_rooms (chat_id, thread_id, room) values
  (null, 2571, 'swing'), (null, 2572, 'scalp'), (null, 3, 'rr'), (null, 360, 'hype')
on conflict do nothing;

-- Every chat the bot is in, with its id, so the source channels can be mapped above.
create table if not exists public.tg_chats (
  chat_id bigint primary key,
  title text,
  type text,
  last_thread bigint,
  last_seen timestamptz not null default now(),
  members int,                          -- member count from Telegram, refreshed hourly (needs TG_BOT_TOKEN)
  members_at timestamptz
);
alter table public.tg_chats add column if not exists members int, add column if not exists members_at timestamptz;

-- Every message the bot sees in a mapped topic (kept so replies can be traced back to their signal).
create table if not exists public.tg_messages (
  chat_id bigint not null,
  message_id bigint not null,
  thread_id bigint not null default 0,
  reply_to bigint,
  sent_at timestamptz not null,
  author text,
  text text,
  room text,
  edited_at timestamptz,
  primary key (chat_id, message_id)
);
create index if not exists tg_messages_sent on public.tg_messages (chat_id, sent_at);

-- One row per signal; the function re-reads the replies under it and keeps the result up to date.
create table if not exists public.signal_trades (
  chat_id bigint not null,
  message_id bigint not null,
  room text not null,
  opened_at timestamptz not null,
  symbol text not null,
  side text not null check (side in ('buy', 'sell')),
  entry numeric, entry2 numeric, sl numeric,
  risk numeric,                         -- pips from entry to stop loss (1R), null if unknown
  status text not null default 'open' check (status in ('open', 'win', 'loss', 'be', 'cancel')),
  pips numeric,                         -- result in pips (furthest profit posted, or the stop loss)
  updated_at timestamptz not null default now(),
  primary key (chat_id, message_id)
);
create index if not exists signal_trades_room on public.signal_trades (room, opened_at);

alter table public.signal_rooms enable row level security;
alter table public.tg_messages enable row level security;
alter table public.signal_trades enable row level security;
alter table public.tg_chats enable row level security;

-- Public: closed trades only, without entry or stop-loss prices.
create or replace view public.signal_results as
  select room, opened_at, symbol, side, status, pips, risk
  from public.signal_trades
  where status in ('win', 'loss', 'be');

-- Public: how many trades are open right now in each room (no prices).
create or replace view public.signal_open_counts as
  select room, count(*)::int as open from public.signal_trades where status = 'open' group by room;

-- Public: how many members each Telegram chat has (shown on the home page). No titles, no names.
create or replace view public.group_members as
  select chat_id, members, members_at from public.tg_chats where members is not null;

grant select on public.signal_results, public.signal_open_counts, public.group_members to anon, authenticated;
