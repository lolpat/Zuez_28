-- Order The Market member portal: database schema for Supabase (PostgreSQL).
-- Run once in Supabase: Dashboard > SQL Editor > paste this file > Run.
--
-- Network rule (from the owner):
--   * a user sees themself and everyone below them, at every level;
--   * a user sees only the NAME (and Telegram) of the person directly above them;
--   * nobody sees anyone above their direct upline, or any branch that is not below them;
--   * the owner sees everyone.
-- These rules are enforced here with row-level security, so they hold even if someone
-- edits the web page or calls the API directly.

create extension if not exists pgcrypto;

-- ---------------------------------------------------------------- tables

create table if not exists public.profiles (
  id             uuid primary key references auth.users (id) on delete cascade,
  email          text not null,
  full_name      text not null default '',
  telegram       text not null default '',
  role           text not null default 'member' check (role in ('member', 'ib', 'owner')),
  status         text not null default 'pending' check (status in ('pending', 'approved', 'rejected')),
  referral_code  text not null unique default upper(substr(encode(gen_random_bytes(6), 'hex'), 1, 8)),
  upline_id      uuid references public.profiles (id) on delete set null,
  language       text not null default 'th' check (language in ('th', 'en')),
  created_at     timestamptz not null default now(),
  constraint no_self_upline check (upline_id is null or upline_id <> id)
);
create index if not exists profiles_upline_idx on public.profiles (upline_id);

create table if not exists public.broker_accounts (
  id              uuid primary key default gen_random_uuid(),
  user_id         uuid not null references public.profiles (id) on delete cascade,
  broker          text not null check (broker in ('vantage', 'puprime', 'vtmarkets')),
  account_number  text not null,
  server          text not null default '',
  platform        text not null default 'MT5' check (platform in ('MT4', 'MT5')),
  currency        text not null default 'USD',
  start_balance   numeric(14, 2) not null default 0,
  created_at      timestamptz not null default now(),
  unique (broker, account_number)
);
create index if not exists broker_accounts_user_idx on public.broker_accounts (user_id);

create table if not exists public.trades (
  id           uuid primary key default gen_random_uuid(),
  user_id      uuid not null references public.profiles (id) on delete cascade,
  account_id   uuid references public.broker_accounts (id) on delete cascade,
  ticket       text not null default '',
  symbol       text not null,
  side         text not null check (side in ('buy', 'sell')),
  volume       numeric(12, 2) not null default 0,
  open_time    timestamptz not null,
  close_time   timestamptz not null,
  open_price   numeric(18, 6),
  close_price  numeric(18, 6),
  sl           numeric(18, 6),
  tp           numeric(18, 6),
  commission   numeric(14, 2) not null default 0,
  swap         numeric(14, 2) not null default 0,
  profit       numeric(14, 2) not null default 0,
  -- journal notes
  note         text not null default '',
  feeling      text not null default '',
  execution    smallint check (execution between 1 and 5),
  tags         text[] not null default '{}',
  lesson       text not null default '',
  created_at   timestamptz not null default now()
);
create unique index if not exists trades_ticket_uq on public.trades (account_id, ticket) where ticket <> '';
create index if not exists trades_user_time_idx on public.trades (user_id, close_time);

-- ---------------------------------------------------------------- helpers

-- true when `ancestor` is somewhere above `target` in the referral tree
create or replace function public.is_ancestor(ancestor uuid, target uuid)
returns boolean language sql stable security definer set search_path = public as $$
  with recursive chain as (
    select upline_id, 1 as depth from profiles where id = target
    union all
    select p.upline_id, c.depth + 1 from profiles p join chain c on p.id = c.upline_id
    where c.depth < 50
  )
  select exists (select 1 from chain where upline_id = ancestor);
$$;

create or replace function public.is_owner(uid uuid)
returns boolean language sql stable security definer set search_path = public as $$
  select exists (select 1 from profiles where id = uid and role = 'owner');
$$;

-- may the caller see this user's data?
create or replace function public.can_view(target uuid)
returns boolean language sql stable security definer set search_path = public as $$
  select target = auth.uid() or public.is_owner(auth.uid()) or public.is_ancestor(auth.uid(), target);
$$;

-- ---------------------------------------------------------------- row-level security

alter table public.profiles        enable row level security;
alter table public.broker_accounts enable row level security;
alter table public.trades          enable row level security;

drop policy if exists profiles_select on public.profiles;
create policy profiles_select on public.profiles for select using (public.can_view(id));

-- users may edit their own name, Telegram and language only (see column grants below)
drop policy if exists profiles_update_self on public.profiles;
create policy profiles_update_self on public.profiles for update
  using (id = auth.uid()) with check (id = auth.uid());

drop policy if exists accounts_select on public.broker_accounts;
create policy accounts_select on public.broker_accounts for select using (public.can_view(user_id));
drop policy if exists accounts_write on public.broker_accounts;
create policy accounts_write on public.broker_accounts for all
  using (user_id = auth.uid()) with check (user_id = auth.uid());

drop policy if exists trades_select on public.trades;
create policy trades_select on public.trades for select using (public.can_view(user_id));
drop policy if exists trades_write on public.trades;
create policy trades_write on public.trades for all
  using (user_id = auth.uid())
  with check (
    user_id = auth.uid()
    and exists (select 1 from public.profiles where id = auth.uid() and status = 'approved')
    and (account_id is null or exists (
      select 1 from public.broker_accounts a where a.id = account_id and a.user_id = auth.uid()))
  );

-- column-level: role, status, upline and referral code cannot be changed by the user
revoke update on public.profiles from anon, authenticated;
grant update (full_name, telegram, language) on public.profiles to authenticated;
revoke insert, delete on public.profiles from anon, authenticated;

-- ---------------------------------------------------------------- functions the app calls

-- the person directly above the caller: name and Telegram only
create or replace function public.my_upline()
returns table (full_name text, telegram text) language sql stable security definer set search_path = public as $$
  select u.full_name, u.telegram
  from profiles me join profiles u on u.id = me.upline_id
  where me.id = auth.uid();
$$;

-- everyone below the caller (the owner gets everyone), with depth and journal summary
create or replace function public.my_downline()
returns table (
  id uuid, full_name text, email text, telegram text, role text, status text,
  upline_id uuid, depth int, created_at timestamptz,
  brokers text, accounts text, trade_count bigint, net_profit numeric, win_rate numeric
) language sql stable security definer set search_path = public as $$
  with recursive tree as (
    select p.id, 1 as depth from profiles p
    where (p.upline_id = auth.uid())
       or (public.is_owner(auth.uid()) and p.upline_id is null and p.id <> auth.uid())
    union all
    select p.id, t.depth + 1 from profiles p join tree t on p.upline_id = t.id where t.depth < 50
  )
  select p.id, p.full_name, p.email, p.telegram, p.role, p.status, p.upline_id, t.depth, p.created_at,
    coalesce((select string_agg(distinct a.broker, ',') from broker_accounts a where a.user_id = p.id), ''),
    coalesce((select string_agg(a.account_number, ',') from broker_accounts a where a.user_id = p.id), ''),
    (select count(*) from trades x where x.user_id = p.id),
    coalesce((select sum(x.profit + x.commission + x.swap) from trades x where x.user_id = p.id), 0),
    (select round(100.0 * count(*) filter (where x.profit + x.commission + x.swap > 0) / nullif(count(*), 0), 1)
       from trades x where x.user_id = p.id)
  from tree t join profiles p on p.id = t.id
  order by t.depth, p.created_at;
$$;

-- approve or reject someone below you
create or replace function public.set_member_status(target uuid, new_status text)
returns void language plpgsql security definer set search_path = public as $$
begin
  if new_status not in ('approved', 'rejected', 'pending') then
    raise exception 'bad status';
  end if;
  if not (public.is_owner(auth.uid()) or (
      public.is_ancestor(auth.uid(), target)
      and exists (select 1 from profiles where id = auth.uid() and role = 'ib' and status = 'approved'))) then
    raise exception 'not allowed';
  end if;
  update profiles set status = new_status where id = target;
end $$;

-- owner only: make someone an IB (or back to member)
create or replace function public.set_member_role(target uuid, new_role text)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not public.is_owner(auth.uid()) then raise exception 'not allowed'; end if;
  if new_role not in ('member', 'ib') then raise exception 'bad role'; end if;
  update profiles set role = new_role where id = target;
end $$;

-- delete every trade in one of your accounts (used before re-importing a report)
create or replace function public.clear_account_trades(acc uuid)
returns void language sql security definer set search_path = public as $$
  delete from trades where account_id = acc and user_id = auth.uid();
$$;

grant execute on function public.my_upline(), public.my_downline(),
  public.set_member_status(uuid, text), public.set_member_role(uuid, text),
  public.clear_account_trades(uuid) to authenticated;
revoke execute on function public.is_ancestor(uuid, uuid), public.is_owner(uuid) from anon;

-- ---------------------------------------------------------------- sign-up

-- a new auth user gets a profile, is placed under the IB whose referral code they used,
-- and gets the broker account they registered with
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path = public as $$
declare
  meta jsonb := coalesce(new.raw_user_meta_data, '{}'::jsonb);
  up uuid;
begin
  select id into up from profiles
   where referral_code = upper(trim(coalesce(meta ->> 'referral_code', '')))
     and role in ('ib', 'owner') and status = 'approved';
  insert into profiles (id, email, full_name, telegram, upline_id, language)
  values (new.id, new.email, coalesce(meta ->> 'full_name', ''),
          coalesce(meta ->> 'telegram', ''), up,
          case when meta ->> 'language' = 'en' then 'en' else 'th' end);
  if coalesce(meta ->> 'broker', '') in ('vantage', 'puprime', 'vtmarkets')
     and coalesce(meta ->> 'account_number', '') <> '' then
    insert into broker_accounts (user_id, broker, account_number, platform)
    values (new.id, meta ->> 'broker', meta ->> 'account_number',
            case when meta ->> 'platform' = 'MT4' then 'MT4' else 'MT5' end)
    on conflict do nothing;
  end if;
  return new;
end $$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users
  for each row execute function public.handle_new_user();

-- ---------------------------------------------------------------- first owner
-- After you register your own account on the site, run this once (with your email):
--   update public.profiles set role = 'owner', status = 'approved' where email = 'you@example.com';

-- ---------------------------------------------------------------- automatic MT4/MT5 history sync
-- Filled in only by the mt-sync Edge Function (supabase/functions/mt-sync), which runs with the
-- service role. The member's investor password is passed to MetaApi once and never stored here.
alter table public.broker_accounts add column if not exists metaapi_id   text;
alter table public.broker_accounts add column if not exists sync_status  text not null default 'off';
alter table public.broker_accounts add column if not exists sync_error   text not null default '';
alter table public.broker_accounts add column if not exists last_sync_at timestamptz;
alter table public.broker_accounts drop constraint if exists broker_accounts_sync_status_check;
alter table public.broker_accounts add constraint broker_accounts_sync_status_check
  check (sync_status in ('off', 'connecting', 'ok', 'error'));
alter table public.trades add column if not exists source text not null default 'manual';
alter table public.trades drop constraint if exists trades_source_check;
alter table public.trades add constraint trades_source_check check (source in ('manual', 'import', 'sync'));

-- members can add and edit their own accounts, but not the sync columns
revoke insert, update on public.broker_accounts from anon, authenticated;
grant insert (user_id, broker, account_number, server, platform, currency, start_balance)
  on public.broker_accounts to authenticated;
grant update (server, platform, currency, start_balance) on public.broker_accounts to authenticated;

-- ---------------------------------------------------------------- leaderboard
-- Members choose to be ranked (leaderboard_opt_in) and the name shown (leaderboard_name).
-- Accounts are live or demo; the leaderboard ranks each kind separately.
alter table public.profiles add column if not exists leaderboard_opt_in boolean not null default false;
alter table public.profiles add column if not exists leaderboard_name text not null default '';
alter table public.profiles drop constraint if exists profiles_leaderboard_name_len;
alter table public.profiles add constraint profiles_leaderboard_name_len check (char_length(leaderboard_name) <= 30);
grant update (leaderboard_opt_in, leaderboard_name) on public.profiles to authenticated;

alter table public.broker_accounts add column if not exists account_type text not null default 'live';
alter table public.broker_accounts drop constraint if exists broker_accounts_type_check;
alter table public.broker_accounts add constraint broker_accounts_type_check check (account_type in ('live', 'demo'));
grant insert (account_type) on public.broker_accounts to authenticated;
grant update (account_type) on public.broker_accounts to authenticated;

-- Ranking for a period ('day' | 'week' | 'month' | 'all', Thai time) and an account type.
-- Only approved members who opted in are counted, and only those in profit are ranked.
-- Returns the top 20, plus the caller's own row if they rank lower.
-- Returns the shown name and aggregates only: no ids, emails or balances.
drop function if exists public.leaderboard(text, text);
create or replace function public.leaderboard(p_period text, p_type text default 'live')
returns table (
  rank int, display_name text, trades int, wins int, losses int, net numeric,
  gross_win numeric, gross_loss numeric, streak int, return_pct numeric, is_me boolean,
  field_size int, in_profit int
)
language sql stable security definer set search_path = public as $$
  with b as (
    select case p_period
      when 'day'   then date_trunc('day',   now() at time zone 'Asia/Bangkok') at time zone 'Asia/Bangkok'
      when 'week'  then date_trunc('week',  now() at time zone 'Asia/Bangkok') at time zone 'Asia/Bangkok'
      when 'month' then date_trunc('month', now() at time zone 'Asia/Bangkok') at time zone 'Asia/Bangkok'
      else '-infinity'::timestamptz end as t0
  ), t as (
    select tr.user_id, tr.close_time, (tr.profit + tr.commission + tr.swap) as n
      from trades tr
      join broker_accounts a on a.id = tr.account_id
      join profiles p on p.id = tr.user_id
     where p.status = 'approved' and p.leaderboard_opt_in
       and a.account_type = p_type
       and tr.close_time >= (select t0 from b)
  ), agg as (
    select user_id, count(*)::int as trades,
           (count(*) filter (where n > 0))::int as wins, (count(*) filter (where n < 0))::int as losses,
           sum(n) as net, coalesce(sum(n) filter (where n > 0), 0) as gross_win,
           coalesce(-sum(n) filter (where n < 0), 0) as gross_loss,
           count(*) over () as field_size
      from t group by user_id
  ), ord as (
    select user_id, n, row_number() over (partition by user_id order by close_time desc) as rn from t
  ), stk as (
    select user_id, coalesce(min(rn) filter (where n <= 0), max(rn) + 1) - 1 as streak from ord group by user_id
  ), bal as (
    select user_id, sum(start_balance) as start_balance from broker_accounts where account_type = p_type group by user_id
  )
  , ranked as (
    select (row_number() over (order by agg.net desc, agg.trades))::int as rank,
           coalesce(nullif(trim(p.leaderboard_name), ''), split_part(p.full_name, ' ', 1)) as display_name,
           agg.trades, agg.wins, agg.losses, round(agg.net, 2) as net, round(agg.gross_win, 2) as gross_win,
           round(agg.gross_loss, 2) as gross_loss, stk.streak::int as streak,
           case when coalesce(bal.start_balance, 0) > 0 then round(agg.net / bal.start_balance * 100, 2) end as return_pct,
           agg.user_id = auth.uid() as is_me, agg.field_size::int as field_size,
           (count(*) over ())::int as in_profit
      from agg
      join profiles p on p.id = agg.user_id
      join stk on stk.user_id = agg.user_id
      left join bal on bal.user_id = agg.user_id
     where agg.net > 0
  )
  select * from ranked where rank <= 20 or is_me order by rank;
$$;
revoke execute on function public.leaderboard(text, text) from public, anon;
grant execute on function public.leaderboard(text, text) to authenticated;

-- ---------------------------------------------------------------- correcting live / demo
-- Some brokers label a real-money account "Demo" (in the server name or what they report). The site
-- owner can correct any account's type; once corrected it is locked, so a sync never flips it back.
-- Members choose the type only when they add an account.
alter table public.broker_accounts add column if not exists type_locked boolean not null default false;
revoke update (account_type) on public.broker_accounts from authenticated;

create or replace function public.set_account_type(p_account uuid, p_type text)
returns void language plpgsql security definer set search_path = public as $$
begin
  if p_type not in ('live', 'demo') then raise exception 'bad-type'; end if;
  if not public.is_owner(auth.uid()) then raise exception 'not-allowed'; end if;
  update broker_accounts set account_type = p_type, type_locked = true where id = p_account;
  if not found then raise exception 'not-found'; end if;
end $$;
revoke execute on function public.set_account_type(uuid, text) from public, anon;
grant execute on function public.set_account_type(uuid, text) to authenticated;

-- ---------------------------------------------------------------- at most 10 broker accounts per member
create or replace function public.limit_accounts()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  perform pg_advisory_xact_lock(hashtext(new.user_id::text));
  if (select count(*) from broker_accounts where user_id = new.user_id) >= 10 then
    raise exception 'account-limit';
  end if;
  return new;
end $$;
drop trigger if exists broker_accounts_limit on public.broker_accounts;
create trigger broker_accounts_limit before insert on public.broker_accounts
  for each row execute function public.limit_accounts();
