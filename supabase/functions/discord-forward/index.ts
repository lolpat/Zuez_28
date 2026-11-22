// discord-forward: copies new text messages from chosen Discord channels into Telegram (a group topic), every minute.
//
// The Discord bot is added to the server by an admin, with only "View Channel" and "Read Message History" on the channels
// it should copy. Which channel goes where is in public.discord_routes. Text only: images and files are not copied;
// the text of embeds (title, description, fields) is, because signal bots often post that way.
//
// POST { action: "run" }  from the schedule, with header x-cron-secret
//
// Secrets: DISCORD_BOT_TOKEN  the bot's token (Discord Developer Portal > your app > Bot > Reset Token)
//          TG_BOT_TOKEN       the Telegram bot's token (the bot must be allowed to post in the target group)
//          CRON_SECRET        the same value the mt-sync schedule uses
// SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are provided by Supabase.
import { createClient } from "jsr:@supabase/supabase-js@2";

const DISCORD = Deno.env.get("DISCORD_BOT_TOKEN") ?? "";
const TG = Deno.env.get("TG_BOT_TOKEN") ?? "";
const CRON_SECRET = Deno.env.get("CRON_SECRET") ?? "";
const API = "https://discord.com/api/v10";

const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });
const newer = (a: string, b: string) => BigInt(a) > BigInt(b);   // Discord ids grow with time

async function discord(path: string) {
  const r = await fetch(API + path, { headers: { Authorization: `Bot ${DISCORD}` } });
  if (!r.ok) throw new Error(`discord ${r.status}`);
  return r.json();
}

// a Discord message as plain text: mentions and custom emoji made readable, embed text added
export function render(m: any): string {
  const users = new Map<string, string>((m.mentions ?? []).map((u: any) => [u.id, u.global_name || u.username]));
  let t = String(m.content ?? "")
    .replace(/<@!?(\d+)>/g, (_, id) => "@" + (users.get(id) ?? "user"))
    .replace(/<@&\d+>/g, "@role")
    .replace(/<#\d+>/g, "#channel")
    .replace(/<a?:(\w+):\d+>/g, ":$1:")
    .replace(/<t:(\d+)(?::\w)?>/g, (_, s) => new Date(+s * 1000).toISOString().slice(0, 16).replace("T", " ") + " UTC");
  for (const e of m.embeds ?? []) {
    const parts = [e.title, e.description, ...(e.fields ?? []).map((f: any) => `${f.name}: ${f.value}`)].filter(Boolean);
    if (parts.length) t += (t ? "\n\n" : "") + parts.join("\n");
  }
  return t.trim();
}

async function telegram(chat: number, topic: number | null, text: string) {
  for (let i = 0; i < text.length; i += 4000) {   // Telegram's limit is 4096 characters
    const r = await fetch(`https://api.telegram.org/bot${TG}/sendMessage`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_id: chat, ...(topic && topic !== 1 ? { message_thread_id: topic } : {}), text: text.slice(i, i + 4000), disable_web_page_preview: true }),
    });
    if (!r.ok) { const j = await r.json().catch(() => ({})); throw new Error(`telegram ${r.status}${j.description ? ": " + j.description : ""}`); }
  }
}

Deno.serve(async (req) => {
  if (req.method !== "POST") return json({ error: "method" }, 405);
  if (!CRON_SECRET || req.headers.get("x-cron-secret") !== CRON_SECRET) return json({ error: "forbidden" }, 403);
  if (!DISCORD || !TG) return json({ error: "not-configured" }, 503);
  const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });

  const { data: routes } = await db.from("discord_routes").select("*").eq("enabled", true);
  const out: unknown[] = [];
  for (const r of routes ?? []) {
    let last = r.last_message_id as string | null, sent = 0, error = "";
    try {
      if (!last) {
        // first run for this channel: start from now, don't copy the old history
        const latest = await discord(`/channels/${r.channel_id}/messages?limit=1`);
        last = latest[0]?.id ?? "0";
      } else {
        const msgs = (await discord(`/channels/${r.channel_id}/messages?after=${last}&limit=50`))
          .filter((m: any) => newer(m.id, last!))
          .sort((a: any, b: any) => (newer(a.id, b.id) ? 1 : -1));
        for (const m of msgs) {
          if (m.type === 0 || m.type === 19) {   // normal messages and replies only
            const body = render(m);
            if (body) {
              const who = r.show_author ? (m.author?.global_name || m.author?.username || "") : "";
              await telegram(r.tg_chat, r.tg_topic, (r.prefix ? r.prefix + "\n" : "") + (who ? who + ":\n" : "") + body);
              sent++;
            }
          }
          last = m.id;   // only after it was sent (or skipped), so a failure retries it next minute
        }
      }
    } catch (e) { error = String((e as Error).message ?? e).slice(0, 300); }
    await db.from("discord_routes").update({ last_message_id: last, last_run_at: new Date().toISOString(), last_error: error, ...(sent ? { last_sent_at: new Date().toISOString() } : {}) }).eq("channel_id", r.channel_id);
    out.push({ channel: r.channel_id, sent, ...(error ? { error } : {}) });
  }
  return json({ ok: true, routes: out });
});
