-- Per-signal charts on the portal's signal page: each closed signal drawn as a position (entry, SL, take-profits, exit).
-- Run once in the SQL editor BEFORE updating the tg-signals function (it writes the two new columns). Safe to run again.
--
--   signal_trades.tps        the signal's take-profit prices, in the order posted (the bot fills it from now on)
--   signal_trades.closed_at  when the trade closed: the time of the last reply about its result
--   tg_messages.trade_ref    for a result posted without replying to its signal, the signal it was matched to
--   signal_positions(room)   closed signals with their prices, for APPROVED members only. Open trades stay hidden.
--   price_candles / price_windows   gold candles fetched for those charts by the signal-candles function (Twelve Data)

alter table public.signal_trades add column if not exists tps numeric[];
alter table public.signal_trades add column if not exists closed_at timestamptz;
-- a result posted without replying to its signal: which signal the bot matched it to
alter table public.tg_messages add column if not exists trade_ref bigint;

-- fill tps for the signals already stored (same reading as the bot: TP / TAKE PROFIT / TARGET followed by a price,
-- on the profit side of the entry)
update public.signal_trades t set tps = x.tps
from (
  select st.chat_id, st.message_id,
         array_agg(v order by ord) filter (where v > 1500 and v < 9000
           and (st.entry is null or (st.side = 'buy' and v > st.entry) or (st.side = 'sell' and v < st.entry))) as tps
  from public.signal_trades st
  join public.tg_messages m on m.chat_id = st.chat_id and m.message_id = st.message_id
  cross join lateral regexp_matches(m.text, '(?:\mTP\s*(?:\d{1,2}(?!\d))?|TAKE\s*PROFIT\s*(?:\d{1,2}(?!\d))?|TARGET\s*(?:\d{1,2}(?!\d))?)\s*[.:@=]*\s*@?\s*(\d[\d,]*(?:\.\d+)?)', 'gi')
       with ordinality as r(g, ord)
  cross join lateral (select replace(g[1], ',', '')::numeric as v) n
  where st.symbol = 'XAUUSD'
  group by st.chat_id, st.message_id
) x
where t.chat_id = x.chat_id and t.message_id = x.message_id and t.tps is null;

-- fill closed_at for closed signals: the last reply under the signal that talks about the result
with recursive d as (
  select t.chat_id, t.message_id as root, m.message_id, m.sent_at, m.text
    from public.signal_trades t join public.tg_messages m on m.chat_id = t.chat_id and m.reply_to = t.message_id
  union all
  select d.chat_id, d.root, m.message_id, m.sent_at, m.text
    from d join public.tg_messages m on m.chat_id = d.chat_id and m.reply_to = d.message_id
)
update public.signal_trades t set closed_at = x.last
from (select chat_id, root, max(sent_at) as last from d
       where text ~* '(pips?|points?|\mtp\M|target|take profit|\msl\M|stop ?loss|break.?even|\mbe\M|✅|❌)'
       group by chat_id, root) x
where t.chat_id = x.chat_id and t.message_id = x.root and t.status in ('win', 'loss', 'be') and t.closed_at is null;

-- closed signals with their prices, newest first, for approved members
create or replace function public.signal_positions(p_room text, p_limit int default 60)
returns table (
  id text, room text, symbol text, side text, entry numeric, entry2 numeric, sl numeric, tps numeric[],
  risk numeric, pips numeric, status text, opened_at timestamptz, closed_at timestamptz
)
language sql stable security definer set search_path = public as $$
  select t.chat_id::text || ':' || t.message_id::text, t.room, t.symbol, t.side, t.entry, t.entry2, t.sl, t.tps,
         t.risk, t.pips, t.status, t.opened_at, coalesce(t.closed_at, t.updated_at)
    from signal_trades t
   where t.room = p_room and t.status in ('win', 'loss', 'be')
     and exists (select 1 from profiles p where p.id = auth.uid() and p.status = 'approved')
   order by t.opened_at desc
   limit least(greatest(coalesce(p_limit, 60), 1), 200);
$$;
revoke execute on function public.signal_positions(text, int) from public, anon;
grant execute on function public.signal_positions(text, int) to authenticated;

-- gold candles for the charts (only the signal-candles function reads and writes these)
create table if not exists public.price_candles (
  tf text not null,
  t  timestamptz not null,
  o numeric(12, 3) not null, h numeric(12, 3) not null, l numeric(12, 3) not null, c numeric(12, 3) not null,
  primary key (tf, t)
);
alter table public.price_candles drop constraint if exists price_candles_tf_check;
alter table public.price_candles add constraint price_candles_tf_check check (tf in ('1min', '5min', '15min', '1h', '1day'));
create table if not exists public.price_windows (     -- stretches of history already fetched completely
  tf text not null, t_from timestamptz not null, t_to timestamptz not null,
  primary key (tf, t_from, t_to)
);
alter table public.price_candles enable row level security;
alter table public.price_windows enable row level security;
revoke all on public.price_candles, public.price_windows from anon, authenticated;
