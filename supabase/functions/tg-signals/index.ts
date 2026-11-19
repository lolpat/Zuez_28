// tg-signals: the Telegram bot's webhook. Reads the signal rooms' topics and keeps public.signal_trades current,
// so the website's signal results update by themselves.
//
// Telegram sends every new or edited message in the VIP group here (the bot must be an admin of the group).
//   - a message in a topic listed in public.signal_rooms is stored in public.tg_messages
//   - a signal (BUY/SELL with an entry and a stop loss) opens a row in public.signal_trades
//   - a reply under a signal (TARGET HIT, +pips, hit sl, BE, cancel) updates that row's result
// The reading rules live in parse.js, the same file that built the history on the website.
//
// Secrets (Supabase dashboard -> Edge Functions -> Secrets):
//   TG_WEBHOOK_SECRET   any long random string; Telegram sends it back in X-Telegram-Bot-Api-Secret-Token
// SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are provided by Supabase.
// The bot token itself is not needed here: Telegram pushes the messages to this function.
import { createClient } from "jsr:@supabase/supabase-js@2";
import { parseSignal, parseResult, applyResult, outcome } from "./parse.js";

const SECRET = Deno.env.get("TG_WEBHOOK_SECRET") ?? "";
const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const ok = () => new Response("ok");

type Msg = {
  message_id: number; date: number; edit_date?: number; chat: { id: number; title?: string; type?: string };
  message_thread_id?: number; is_topic_message?: boolean; reply_to_message?: { message_id: number };
  text?: string; caption?: string; from?: { first_name?: string; username?: string }; sender_chat?: { title?: string };
};

async function roomFor(chatId: number, threadId: number): Promise<string | null> {
  const { data } = await db.from("signal_rooms").select("chat_id, room").eq("thread_id", threadId);
  const rows = data ?? [];
  return (rows.find((r) => r.chat_id === chatId) ?? rows.find((r) => r.chat_id === null))?.room ?? null;
}

// Walk reply_to up the chain until it reaches a signal.
async function rootTrade(chatId: number, replyTo: number | null) {
  let r = replyTo;
  for (let i = 0; r != null && i < 30; i++) {
    const { data: t } = await db.from("signal_trades").select("*").eq("chat_id", chatId).eq("message_id", r).maybeSingle();
    if (t) return t;
    const { data: m } = await db.from("tg_messages").select("reply_to").eq("chat_id", chatId).eq("message_id", r).maybeSingle();
    r = m?.reply_to ?? null;
  }
  return null;
}

// Re-read every reply under a trade, in order, and store the result.
async function recompute(trade: Record<string, any>) {
  const until = new Date(new Date(trade.opened_at).getTime() + 30 * 864e5).toISOString();
  const { data } = await db.from("tg_messages").select("message_id, reply_to, text")
    .eq("chat_id", trade.chat_id).gt("sent_at", trade.opened_at).lte("sent_at", until)
    .order("sent_at").order("message_id").limit(5000);
  const rows = data ?? [];
  const parent = new Map(rows.map((m) => [m.message_id, m.reply_to]));
  const { data: others } = await db.from("signal_trades").select("message_id").eq("chat_id", trade.chat_id)
    .gt("opened_at", trade.opened_at).lte("opened_at", until);
  const otherTrades = new Set((others ?? []).map((t) => t.message_id));
  const belongs = (id: number) => {
    let r = parent.get(id) ?? null;
    for (let i = 0; r != null && i < 30; i++) {
      if (r === trade.message_id) return true;
      if (otherTrades.has(r)) return false;
      r = parent.get(r) ?? null;
    }
    return false;
  };
  let st = {};
  for (const m of rows) if (belongs(m.message_id)) st = applyResult(st, parseResult(m.text ?? ""));
  const o = outcome(st, trade.risk, trade.entry, trade.symbol);
  await db.from("signal_trades").update({ status: o.status, pips: o.pips, updated_at: new Date().toISOString() })
    .eq("chat_id", trade.chat_id).eq("message_id", trade.message_id);
}

Deno.serve(async (req) => {
  if (req.method !== "POST") return new Response("tg-signals is running", { status: 200 });
  if (!SECRET || req.headers.get("x-telegram-bot-api-secret-token") !== SECRET) return new Response("forbidden", { status: 401 });
  let update: Record<string, any>;
  try { update = await req.json(); } catch { return ok(); }
  const msg: Msg | undefined = update.message ?? update.edited_message ?? update.channel_post ?? update.edited_channel_post;
  if (!msg) return ok();

  try {
    const chatId = msg.chat.id, threadId = msg.is_topic_message ? msg.message_thread_id ?? 0 : 0;
    // remember every chat the bot is in (its id is what public.signal_rooms maps to a room)
    await db.from("tg_chats").upsert({ chat_id: chatId, title: msg.chat.title ?? null, type: msg.chat.type ?? null, last_thread: threadId, last_seen: new Date().toISOString() });
    const room = await roomFor(chatId, threadId);
    if (!room) return ok();                                   // not a signal room: ignore
    const text = msg.text ?? msg.caption ?? "";
    const replyTo = msg.reply_to_message?.message_id ?? null;
    const sentAt = new Date(msg.date * 1000).toISOString();
    await db.from("tg_messages").upsert({
      chat_id: chatId, message_id: msg.message_id, thread_id: threadId, reply_to: replyTo, sent_at: sentAt, room,
      author: msg.sender_chat?.title ?? msg.from?.username ?? msg.from?.first_name ?? null, text,
      edited_at: msg.edit_date ? new Date(msg.edit_date * 1000).toISOString() : null,
    });

    const sig = parseSignal(text, room);
    if (sig) {
      // the same signal reposted in another chat (e.g. the source channel and the VIP copy) counts once
      const near = (a: number | null, b: number | null) => a != null && b != null && Math.abs(a - b) <= 0.6;
      const from = new Date(msg.date * 1000 - 2 * 3600e3).toISOString(), to = new Date(msg.date * 1000 + 2 * 3600e3).toISOString();
      const { data: twins } = await db.from("signal_trades").select("chat_id, entry, sl")
        .eq("room", sig.symbol === "XAUUSD" ? room : "hype").eq("side", sig.side)
        .gte("opened_at", from).lte("opened_at", to);
      if ((twins ?? []).some((x) => x.chat_id !== chatId && (near(x.sl, sig.sl) || near(x.entry, sig.entry)))) return ok();
      const trade = {
        chat_id: chatId, message_id: msg.message_id, opened_at: sentAt,
        room: sig.symbol === "XAUUSD" ? room : "hype", symbol: sig.symbol, side: sig.side,
        entry: sig.entry, entry2: sig.entry2, sl: sig.sl, risk: sig.risk,
      };
      await db.from("signal_trades").upsert(trade, { onConflict: "chat_id,message_id", ignoreDuplicates: false });
      const { data: t } = await db.from("signal_trades").select("*").eq("chat_id", chatId).eq("message_id", msg.message_id).single();
      if (t) await recompute(t);                              // an edited signal may already have replies
      return ok();
    }
    const trade = await rootTrade(chatId, replyTo);
    if (trade) await recompute(trade);
  } catch (e) {
    console.error("tg-signals", e);                           // still 200, so Telegram doesn't resend forever
  }
  return ok();
});
