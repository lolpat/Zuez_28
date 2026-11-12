-- Run this once in Supabase > SQL Editor AFTER deploying the mt-sync function (see website/README.md).
-- It asks mt-sync to pull new trades for every connected account every 30 minutes.
-- Replace the two placeholders:
--   YOUR-PROJECT    the id in your project URL (https://YOUR-PROJECT.supabase.co)
--   YOUR-CRON-SECRET  the same value you saved with: supabase secrets set CRON_SECRET=...
--   YOUR-ANON-KEY   the anon public key (Project Settings > API); it only gets the request through the gateway
create extension if not exists pg_cron;
create extension if not exists pg_net;

select cron.unschedule('otm-mt-sync') where exists (select 1 from cron.job where jobname = 'otm-mt-sync');
select cron.schedule('otm-mt-sync', '*/30 * * * *', $$
  select net.http_post(
    url     := 'https://YOUR-PROJECT.supabase.co/functions/v1/mt-sync',
    headers := jsonb_build_object(
                 'Content-Type', 'application/json',
                 'Authorization', 'Bearer YOUR-ANON-KEY',
                 'x-cron-secret', 'YOUR-CRON-SECRET'),
    body    := '{"action":"sync_all"}'::jsonb,
    timeout_milliseconds := 150000);
$$);
