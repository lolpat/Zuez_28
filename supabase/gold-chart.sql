-- Gold chart on the portal's Indicator page. Run once in the SQL editor (safe to run again).
--
--   price_candles  gold (XAU/USD) candles, filled by the gold-candles function from Twelve Data. The page reads them
--                  through that function only, so members never see the API key.
--   price_fetches  when each timeframe was last fetched (the function refreshes at most every few minutes, which keeps
--                  Twelve Data's free plan, 800 requests a day, comfortably enough).
--   chart_setups   the levels drawn on the chart (entry zone, SL, TP1-3, runner). Filled by the indicator feed once
--                  Candle2Cash's signals are connected; until then the owner can add one by hand (example at the end).

create table if not exists public.price_candles (
  tf text not null check (tf in ('1min', '15min', '1h')),
  t  timestamptz not null,
  o numeric(12, 3) not null, h numeric(12, 3) not null, l numeric(12, 3) not null, c numeric(12, 3) not null,
  primary key (tf, t)
);
create table if not exists public.price_fetches (
  tf text primary key,
  fetched_at timestamptz not null
);
alter table public.price_candles enable row level security;   -- no policies: only the function (service role) reads and writes
alter table public.price_fetches enable row level security;

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
