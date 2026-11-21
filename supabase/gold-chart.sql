-- Setup levels for the portal's Indicator page. Run once in the SQL editor (safe to run again).
-- The chart itself is TradingView's widget (live prices from TradingView); this table holds the levels shown next to it
-- (entry zone, SL, TP1-3, runner). It is filled by the indicator feed once Candle2Cash's signals are connected; until
-- then the owner can add one by hand (example at the end). Only approved members can read it.

create table if not exists public.chart_setups (
  id bigint generated always as identity primary key,
  source text not null default 'candle2cash',
  symbol text not null default 'XAUUSD',
  tf text,                                   -- the timeframe the setup came from, e.g. '15m'
  side text not null check (side in ('buy', 'sell')),
  entry_lo numeric(12, 3), entry_hi numeric(12, 3),
  sl numeric(12, 3), tp1 numeric(12, 3), tp2 numeric(12, 3), tp3 numeric(12, 3), runner numeric(12, 3),
  created_at timestamptz not null default now(),
  closed_at timestamptz                      -- set when the setup is finished; the chart shows the newest open one
);
create index if not exists chart_setups_open on public.chart_setups (symbol, created_at desc) where closed_at is null;
alter table public.chart_setups enable row level security;
drop policy if exists "approved members read setups" on public.chart_setups;
create policy "approved members read setups" on public.chart_setups for select to authenticated
  using (exists (select 1 from public.profiles p where p.id = auth.uid() and p.status = 'approved'));
grant select on public.chart_setups to authenticated;

-- Adding a setup by hand (SQL editor), until the feed is connected:
--   insert into public.chart_setups (side, tf, entry_lo, entry_hi, sl, tp1, tp2, tp3, runner)
--   values ('buy', '15m', 3520, 3522, 3508, 3530, 3540, 3550, 3570);   -- example prices only
-- Finishing it:
--   update public.chart_setups set closed_at = now() where closed_at is null;
