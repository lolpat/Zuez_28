-- Live Trading Leaderboard with verified MT5 results. Run once in the SQL editor after schema.sql (safe to run again).
--
-- What it adds:
--   1. broker_accounts: balance, equity, margin, the broker's own live/demo flag, when they were read, and when the
--      owner of the account agreed to read-only access. Only the mt-sync function (service role) writes these.
--   2. Trades read from MT5 (source = 'sync') can't be faked or edited by members: they can't insert them, can only
--      change their journal notes on them, and can't delete them.
--   3. leaderboard(period, type, verified): with verified = true only MT5-synced trades count, and each row says
--      whether its result is fully verified.

-- ---------------------------------------------------------------- 1. account figures from the broker
alter table public.broker_accounts add column if not exists balance     numeric(16, 2);
alter table public.broker_accounts add column if not exists equity      numeric(16, 2);
alter table public.broker_accounts add column if not exists margin      numeric(16, 2);
alter table public.broker_accounts add column if not exists broker_mode text;          -- 'real' | 'demo' | 'contest', as the broker reports it
alter table public.broker_accounts add column if not exists info_at     timestamptz;   -- when balance / equity were read
alter table public.broker_accounts add column if not exists consent_at  timestamptz;   -- when the owner allowed read-only access
-- (members' column grants on broker_accounts stay as in schema.sql: none of these columns are writable by them)

-- ---------------------------------------------------------------- 2. MT5 trades stay as the broker reported them
-- "clear this account's trades" keeps the MT5 history (it can only be removed by disconnecting and deleting the account)
create or replace function public.clear_account_trades(acc uuid)
returns void language sql security definer set search_path = public as $$
  delete from trades where account_id = acc and user_id = auth.uid() and source <> 'sync';
$$;

-- deleting an account removes its MT5 trades too (the owner's own decision), through this function only
create or replace function public.delete_account(acc uuid)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not exists (select 1 from broker_accounts where id = acc and user_id = auth.uid()) then raise exception 'not-found'; end if;
  perform set_config('otm.allow_sync_delete', 'on', true);
  delete from trades where account_id = acc and user_id = auth.uid();
  delete from broker_accounts where id = acc and user_id = auth.uid();
end $$;
revoke execute on function public.delete_account(uuid) from public, anon;
grant execute on function public.delete_account(uuid) to authenticated;

-- the guard: the mt-sync function and the database owner pass; delete_account may remove MT5 trades
create or replace function public.guard_synced_trades_allowed() returns boolean language sql stable as $$
  select coalesce(current_setting('otm.allow_sync_delete', true), '') = 'on';
$$;
create or replace function public.guard_synced_trades()
returns trigger language plpgsql as $$
begin
  if coalesce(auth.role(), '') = 'service_role' or (auth.uid() is null and current_user in ('postgres', 'supabase_admin')) then
    return coalesce(new, old);
  end if;
  if tg_op = 'INSERT' then
    if new.source = 'sync' then raise exception 'sync-only'; end if;
    return new;
  end if;
  if tg_op = 'DELETE' then
    if old.source = 'sync' and not public.guard_synced_trades_allowed() then raise exception 'sync-locked'; end if;
    return old;
  end if;
  if old.source = 'sync' and (
       new.source is distinct from old.source or new.user_id is distinct from old.user_id or new.account_id is distinct from old.account_id
    or new.ticket is distinct from old.ticket or new.symbol is distinct from old.symbol or new.side is distinct from old.side
    or new.volume is distinct from old.volume or new.open_time is distinct from old.open_time or new.close_time is distinct from old.close_time
    or new.open_price is distinct from old.open_price or new.close_price is distinct from old.close_price
    or new.sl is distinct from old.sl or new.tp is distinct from old.tp
    or new.commission is distinct from old.commission or new.swap is distinct from old.swap or new.profit is distinct from old.profit) then
    raise exception 'sync-locked';
  end if;
  if new.source = 'sync' and old.source <> 'sync' then raise exception 'sync-only'; end if;
  return new;
end $$;

drop trigger if exists guard_synced_trades on public.trades;
create trigger guard_synced_trades before insert or update or delete on public.trades
  for each row execute function public.guard_synced_trades();

-- ---------------------------------------------------------------- 3. leaderboard with verified results
drop function if exists public.leaderboard(text, text);
drop function if exists public.leaderboard(text, text, boolean);
create function public.leaderboard(p_period text, p_type text default 'live', p_verified boolean default false)
returns table (
  rank int, display_name text, trades int, wins int, losses int, net numeric,
  gross_win numeric, gross_loss numeric, streak int, return_pct numeric, is_me boolean,
  field_size int, in_profit int, verified boolean
)
language sql stable security definer set search_path = public as $$
  with b as (
    select case p_period
      when 'day'   then date_trunc('day',   now() at time zone 'Asia/Bangkok') at time zone 'Asia/Bangkok'
      when 'week'  then date_trunc('week',  now() at time zone 'Asia/Bangkok') at time zone 'Asia/Bangkok'
      when 'month' then date_trunc('month', now() at time zone 'Asia/Bangkok') at time zone 'Asia/Bangkok'
      else '-infinity'::timestamptz end as t0
  ), t as (
    select tr.user_id, tr.close_time, (tr.profit + tr.commission + tr.swap) as n, tr.source = 'sync' as v
      from trades tr
      join broker_accounts a on a.id = tr.account_id
      join profiles p on p.id = tr.user_id
     where p.status = 'approved' and p.leaderboard_opt_in
       and a.account_type = p_type
       and tr.close_time >= (select t0 from b)
       and (not p_verified or tr.source = 'sync')
  ), agg as (
    select user_id, count(*)::int as trades,
           (count(*) filter (where n > 0))::int as wins, (count(*) filter (where n < 0))::int as losses,
           sum(n) as net, coalesce(sum(n) filter (where n > 0), 0) as gross_win,
           coalesce(-sum(n) filter (where n < 0), 0) as gross_loss,
           bool_and(v) as verified,
           count(*) over () as field_size
      from t group by user_id
  ), ord as (
    select user_id, n, row_number() over (partition by user_id order by close_time desc) as rn from t
  ), stk as (
    select user_id, coalesce(min(rn) filter (where n <= 0), max(rn) + 1) - 1 as streak from ord group by user_id
  ), bal as (
    select user_id, sum(start_balance) as start_balance from broker_accounts
     where account_type = p_type and (not p_verified or metaapi_id is not null) group by user_id
  ), ranked as (
    select (row_number() over (order by agg.net desc, agg.trades))::int as rank,
           coalesce(nullif(trim(p.leaderboard_name), ''), split_part(p.full_name, ' ', 1)) as display_name,
           agg.trades, agg.wins, agg.losses, round(agg.net, 2) as net, round(agg.gross_win, 2) as gross_win,
           round(agg.gross_loss, 2) as gross_loss, stk.streak::int as streak,
           case when coalesce(bal.start_balance, 0) > 0 then round(agg.net / bal.start_balance * 100, 2) end as return_pct,
           agg.user_id = auth.uid() as is_me, agg.field_size::int as field_size,
           (count(*) over ())::int as in_profit, agg.verified
      from agg
      join profiles p on p.id = agg.user_id
      join stk on stk.user_id = agg.user_id
      left join bal on bal.user_id = agg.user_id
     where agg.net > 0
  )
  select * from ranked where rank <= 20 or is_me order by rank;
$$;
revoke execute on function public.leaderboard(text, text, boolean) from public, anon;
grant execute on function public.leaderboard(text, text, boolean) to authenticated;
