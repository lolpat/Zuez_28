-- Broker IB reports (IB Network page > "Reports from the broker"). Run once in the SQL editor, after schema.sql.
-- An approved IB or the owner uploads the report files from the broker's IB portal; the browser reads them
-- and stores the rows here. Each IB sees and changes only their own uploads (ib_id = their profile).
-- Day tables are replaced day by day by the page, so overlapping or repeated uploads never double count.

create table if not exists public.ib_fund (          -- deposits / withdrawals per client account per day
  ib_id uuid not null references public.profiles (id) on delete cascade,
  broker text not null, day date not null, user_id text not null, account text not null,
  deposits numeric not null default 0, withdraw numeric not null default 0,
  primary key (ib_id, broker, day, user_id, account)
);
create table if not exists public.ib_accounts (      -- accounts opened under the IB
  ib_id uuid not null references public.profiles (id) on delete cascade,
  broker text not null, account text not null, user_id text not null, name text, opened_on date,
  account_type text, balance numeric,
  primary key (ib_id, broker, account)
);
create table if not exists public.ib_rclient (       -- lots and rebate per client per day
  ib_id uuid not null references public.profiles (id) on delete cascade,
  broker text not null, day date not null, user_id text not null, name text,
  lots numeric not null default 0, notional numeric not null default 0, rebate numeric not null default 0,
  primary key (ib_id, broker, day, user_id)
);
create table if not exists public.ib_rinstr (        -- lots and rebate per instrument per day
  ib_id uuid not null references public.profiles (id) on delete cascade,
  broker text not null, day date not null, instrument text not null,
  lots numeric not null default 0, rebate numeric not null default 0,
  primary key (ib_id, broker, day, instrument)
);
create table if not exists public.ib_rdaily (        -- total volume and rebate per day
  ib_id uuid not null references public.profiles (id) on delete cascade,
  broker text not null, day date not null, notional numeric not null default 0, rebate numeric not null default 0,
  primary key (ib_id, broker, day)
);
create table if not exists public.ib_subib (         -- sub-IB results for one report period
  ib_id uuid not null references public.profiles (id) on delete cascade,
  broker text not null, aff_id text not null, period_from date not null, period_to date not null,
  user_id text, name text, country text, join_date date,
  registration numeric default 0, opened numeric default 0, ftd numeric default 0,
  gross_dep numeric default 0, withdrawals numeric default 0, net_dep numeric default 0, lots numeric default 0, nv numeric default 0,
  primary key (ib_id, broker, aff_id, period_from, period_to)
);
create table if not exists public.ib_subdaily (      -- sub-IB deposits per day
  ib_id uuid not null references public.profiles (id) on delete cascade,
  broker text not null, day date not null, gross_dep numeric not null default 0, net_dep numeric not null default 0,
  primary key (ib_id, broker, day)
);

-- who may upload: approved IBs and the owner
create or replace function public.is_uploader(uid uuid) returns boolean language sql stable security definer set search_path = public as $$
  select exists (select 1 from profiles where id = uid and role in ('ib', 'owner') and status = 'approved');
$$;
revoke execute on function public.is_uploader(uuid) from public, anon;
grant execute on function public.is_uploader(uuid) to authenticated;

do $$
declare t text;
begin
  foreach t in array array['ib_fund', 'ib_accounts', 'ib_rclient', 'ib_rinstr', 'ib_rdaily', 'ib_subib', 'ib_subdaily'] loop
    execute format('alter table public.%I enable row level security', t);
    execute format('drop policy if exists %I on public.%I', t || '_sel', t);
    execute format('create policy %I on public.%I for select using (ib_id = auth.uid() or public.is_owner(auth.uid()))', t || '_sel', t);
    execute format('drop policy if exists %I on public.%I', t || '_ins', t);
    execute format('create policy %I on public.%I for insert with check (ib_id = auth.uid() and public.is_uploader(auth.uid()))', t || '_ins', t);
    execute format('drop policy if exists %I on public.%I', t || '_upd', t);
    execute format('create policy %I on public.%I for update using (ib_id = auth.uid()) with check (ib_id = auth.uid() and public.is_uploader(auth.uid()))', t || '_upd', t);
    execute format('drop policy if exists %I on public.%I', t || '_del', t);
    execute format('create policy %I on public.%I for delete using (ib_id = auth.uid())', t || '_del', t);
    execute format('revoke all on public.%I from anon', t);
    execute format('grant select, insert, update, delete on public.%I to authenticated', t);
  end loop;
end $$;
