-- my_downline() also says whether a member's history comes from MT5 auto-sync (the IB report's profit
-- column labels it "MT5", otherwise "Journal"). Run once in the SQL editor (safe to run again).
-- schema.sql ends with the same definition, so new projects get it from there.
drop function if exists public.my_downline();
create function public.my_downline()
returns table (
  id uuid, full_name text, email text, telegram text, role text, status text,
  upline_id uuid, depth int, created_at timestamptz,
  brokers text, accounts text, trade_count bigint, net_profit numeric, win_rate numeric, synced boolean
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
       from trades x where x.user_id = p.id),
    exists (select 1 from broker_accounts a where a.user_id = p.id and a.sync_status <> 'off')
  from tree t join profiles p on p.id = t.id
  order by t.depth, p.created_at;
$$;
revoke execute on function public.my_downline() from public, anon;
grant execute on function public.my_downline() to authenticated;
