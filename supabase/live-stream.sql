-- Live chart stream on the portal's Indicator page. Run once in the SQL editor (safe to run again).
-- The owner streams their TradingView screen to YouTube Live (unlisted) and pastes the link in the portal;
-- approved members watch it inside the Indicator page. One row only.

create table if not exists public.site_live (
  id int primary key default 1 check (id = 1),
  url text,                          -- the YouTube link of the current stream
  title text,
  is_live boolean not null default false,
  updated_at timestamptz not null default now()
);
insert into public.site_live (id) values (1) on conflict (id) do nothing;
alter table public.site_live enable row level security;

drop policy if exists "approved members read the live stream" on public.site_live;
create policy "approved members read the live stream" on public.site_live for select to authenticated
  using (exists (select 1 from public.profiles p where p.id = auth.uid() and p.status = 'approved'));
drop policy if exists "owner updates the live stream" on public.site_live;
create policy "owner updates the live stream" on public.site_live for update to authenticated
  using (public.is_owner(auth.uid())) with check (public.is_owner(auth.uid()));
revoke all on public.site_live from anon;
grant select, update (url, title, is_live, updated_at) on public.site_live to authenticated;
