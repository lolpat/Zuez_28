-- Discord -> Telegram forwarding. Run once in the SQL editor after deploying the discord-forward function.
-- 1. discord_routes: which Discord channel is copied to which Telegram chat and topic (only the function reads it).
-- 2. A schedule that runs the function every minute.
-- Replace the placeholders in the INSERT at the end before running (or add routes later with the same INSERT).

create table if not exists public.discord_routes (
  channel_id text primary key,               -- Discord channel id (Developer Mode on, right-click the channel > Copy Channel ID)
  label text,                                -- a name for you, e.g. 'friend-server #signals'
  tg_chat bigint not null,                   -- Telegram chat id, e.g. the VIP group -1003941112920
  tg_topic int,                              -- topic (thread) id inside that group; null = the main chat
  prefix text,                               -- optional first line on every message, e.g. '📡 Discord'
  show_author boolean not null default false,  -- put the Discord sender's name above the text
  enabled boolean not null default true,
  last_message_id text,                      -- set by the function; empty = start from the next new message
  last_run_at timestamptz, last_sent_at timestamptz, last_error text
);
alter table public.discord_routes enable row level security;   -- no policies: only the function (service role) uses it
revoke all on public.discord_routes from anon, authenticated;

create extension if not exists pg_cron;
create extension if not exists pg_net;
select cron.unschedule('otm-discord-forward') where exists (select 1 from cron.job where jobname = 'otm-discord-forward');
select cron.schedule('otm-discord-forward', '* * * * *', $$
  select net.http_post(
    url     := 'https://YOUR-PROJECT.supabase.co/functions/v1/discord-forward',
    headers := jsonb_build_object(
                 'Content-Type', 'application/json',
                 'Authorization', 'Bearer YOUR-ANON-KEY',
                 'x-cron-secret', 'YOUR-CRON-SECRET'),
    body    := '{"action":"run"}'::jsonb,
    timeout_milliseconds := 50000);
$$);

-- The route: replace DISCORD-CHANNEL-ID and TELEGRAM-TOPIC-ID (one line per channel).
insert into public.discord_routes (channel_id, label, tg_chat, tg_topic, prefix)
values ('DISCORD-CHANNEL-ID', 'Discord', -1003941112920, TELEGRAM-TOPIC-ID, null)
on conflict (channel_id) do update set tg_chat = excluded.tg_chat, tg_topic = excluded.tg_topic, prefix = excluded.prefix, enabled = true;

-- Check it: select label, last_run_at, last_sent_at, last_error from public.discord_routes;
-- Pause it:  update public.discord_routes set enabled = false;
