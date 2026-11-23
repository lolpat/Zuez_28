-- One-time fix (run once AFTER steps 27 and 28): "BTCUSD ENDED WITH 1500points 4.8RR" (message 4269 in the BTCUSD topic)
-- was posted without replying to its signal, so the bot could not tell which signal it closed. This matches it to the
-- newest open BTCUSD signal before it (the same rule the updated bot now uses) and closes that signal at +150 pips.
-- The result lists the signal it changed; no rows means that signal was never recorded (e.g. posted only as a picture).
with m as (
  select chat_id, message_id, sent_at from public.tg_messages where message_id = 4269 and thread_id = 360
), t as (
  select st.chat_id, st.message_id from public.signal_trades st, m
   where st.chat_id = m.chat_id and st.room = 'hype' and st.symbol = 'BTCUSD' and st.status = 'open'
     and st.opened_at < m.sent_at and st.opened_at >= m.sent_at - interval '3 days'
   order by st.opened_at desc limit 1
), linked as (
  update public.tg_messages g set trade_ref = t.message_id from t, m where g.chat_id = m.chat_id and g.message_id = m.message_id
)
update public.signal_trades st set status = 'win', pips = 150, closed_at = (select sent_at from m), updated_at = now()
  from t where st.chat_id = t.chat_id and st.message_id = t.message_id
returning st.opened_at, st.side, st.entry, st.sl, st.pips;
