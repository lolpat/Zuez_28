// signal-candles: gold candles around one closed signal, for the portal's per-signal chart.
//
// POST { id: "chat:message" }  from an approved member, signed in (Verify JWT on)
//   -> { tf, candles: [{ t (unix seconds, UTC), o, h, l, c }] }
//
// The window is the trade's life plus some room on both sides. The candle size follows how long the trade ran
// (5min up to 8 hours, 15min up to 3 days, 1h after that) so the chart stays readable. Candles come from Twelve Data
// once and are kept in public.price_candles; public.price_windows remembers which stretches are complete, so the
// free plan (800 requests a day) is plenty: each signal's chart costs one request the first time it is opened.
//
// Secret: TWELVEDATA_KEY   free API key from https://twelvedata.com (Sign up > API keys)
// SUPABASE_URL, SUPABASE_ANON_KEY and SUPABASE_SERVICE_ROLE_KEY are provided by Supabase.
import { createClient, type SupabaseClient } from "jsr:@supabase/supabase-js@2";

const KEY = Deno.env.get("TWELVEDATA_KEY") ?? "";
const API = "https://api.twelvedata.com/time_series";
const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status, headers: { ...cors, "Content-Type": "application/json" } });
const SEC: Record<string, number> = { "5min": 300, "15min": 900, "1h": 3600 };
const fmt = (ms: number) => new Date(ms).toISOString().slice(0, 19).replace("T", " ");

// candle size and window for a trade that ran from a to b (ms)
export function plan(openMs: number, closeMs: number) {
  const dur = Math.max(closeMs - openMs, 15 * 60e3);
  const tf = dur <= 8 * 3600e3 ? "5min" : dur <= 3 * 864e5 ? "15min" : "1h";
  const pad = Math.max(dur * 0.35, SEC[tf] * 1000 * 24);
  const sec = SEC[tf] * 1000;
  const from = Math.floor((openMs - pad) / sec) * sec, to = Math.ceil((closeMs + pad * 0.6) / sec) * sec;
  return { tf, from, to };
}

async function fetchWindow(db: SupabaseClient, tf: string, from: number, to: number) {
  const q = new URLSearchParams({ symbol: "XAU/USD", interval: tf, start_date: fmt(from), end_date: fmt(to), timezone: "UTC", order: "asc", outputsize: "5000", apikey: KEY });
  const r = await fetch(`${API}?${q}`);
  const j = await r.json().catch(() => ({}));
  if (j.status === "error" && /no data/i.test(j.message ?? "")) return 0;      // e.g. a weekend: nothing to store
  if (!r.ok || j.status === "error" || !Array.isArray(j.values)) throw new Error(j.code === 429 ? "rate-limited" : "price-feed");
  const rows = j.values.map((v: any) => ({ tf, t: new Date(v.datetime.replace(" ", "T") + "Z").toISOString(), o: +v.open, h: +v.high, l: +v.low, c: +v.close }))
    .filter((x: any) => [x.o, x.h, x.l, x.c].every(Number.isFinite));
  if (rows.length) { const { error } = await db.from("price_candles").upsert(rows, { onConflict: "tf,t" }); if (error) throw new Error("store"); }
  return rows.length;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "POST") return json({ error: "method" }, 405);
  if (!KEY) return json({ error: "not-configured" }, 503);
  const url = Deno.env.get("SUPABASE_URL")!;
  const db = createClient(url, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });

  // approved members only
  const jwt = (req.headers.get("Authorization") ?? "").replace(/^Bearer\s+/i, "");
  const { data: auth } = await createClient(url, Deno.env.get("SUPABASE_ANON_KEY")!).auth.getUser(jwt);
  if (!auth?.user) return json({ error: "signed-out" }, 401);
  const { data: prof } = await db.from("profiles").select("status").eq("id", auth.user.id).single();
  if (prof?.status !== "approved") return json({ error: "not-approved" }, 403);

  let input: any = {};
  try { input = await req.json(); } catch { return json({ error: "bad-request" }, 400); }
  const m = /^(-?\d+):(\d+)$/.exec(String(input.id ?? ""));
  if (!m) return json({ error: "bad-request" }, 400);
  const { data: tr } = await db.from("signal_trades").select("opened_at, closed_at, updated_at, status, symbol")
    .eq("chat_id", m[1]).eq("message_id", m[2]).maybeSingle();
  if (!tr || !["win", "loss", "be"].includes(tr.status)) return json({ error: "not-found" }, 404);   // closed signals only
  if (tr.symbol !== "XAUUSD") return json({ error: "symbol" }, 400);

  const openMs = new Date(tr.opened_at).getTime(), closeMs = new Date(tr.closed_at ?? tr.updated_at).getTime();
  const { tf, from, to } = plan(openMs, closeMs);
  const toCapped = Math.min(to, Date.now());
  const fromIso = new Date(from).toISOString(), toIso = new Date(toCapped).toISOString();

  // fetch once unless a complete stretch already covers this window
  const { data: win } = await db.from("price_windows").select("t_from").eq("tf", tf).lte("t_from", fromIso).gte("t_to", toIso).limit(1);
  let warning: string | undefined;
  if (!win?.length) {
    try {
      await fetchWindow(db, tf, from, toCapped);
      // only remember stretches that are fully in the past (a still-forming last candle would be stale)
      if (toCapped <= Date.now() - SEC[tf] * 1000) await db.from("price_windows").upsert({ tf, t_from: fromIso, t_to: toIso });
    } catch (e) { warning = (e as Error).message; }
  }
  const { data: rows, error } = await db.from("price_candles").select("t,o,h,l,c").eq("tf", tf)
    .gte("t", fromIso).lte("t", toIso).order("t", { ascending: true }).limit(5000);
  if (error) return json({ error: "store" }, 500);
  const candles = (rows ?? []).map((r: any) => ({ t: Math.floor(new Date(r.t).getTime() / 1000), o: +r.o, h: +r.h, l: +r.l, c: +r.c }));
  if (!candles.length) return json({ error: warning ?? "no-data" }, 503);
  return json({ tf, candles, ...(warning ? { warning } : {}) });
});
