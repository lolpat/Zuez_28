// gold-candles: gold (XAU/USD) candles for the portal's chart, from Twelve Data, cached in public.price_candles.
//
// POST { tf: "3m" | "15m" | "1h" }  from an approved member, signed in (Verify JWT on)
//   -> { tf, candles: [{ t (unix seconds, UTC), o, h, l, c }], fetched_at }
//
// Each base timeframe is fetched from Twelve Data at most once per REFRESH window, whoever asks, so the free plan
// (800 requests a day, 8 a minute) is enough: 1min every 4 min + 15min every 5 min + 1h every 15 min stays under 750
// a day even if someone has the chart open all day. 3m candles are built from 1min ones.
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
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...cors, "Content-Type": "application/json" } });

// page timeframe -> [base timeframe stored, how many base candles to fetch, refresh seconds, base candles per page candle, page candles to return]
const TF: Record<string, { base: string; size: number; refresh: number; group: number; keep: number }> = {
  "3m":  { base: "1min",  size: 900, refresh: 240, group: 3, keep: 300 },
  "15m": { base: "15min", size: 400, refresh: 300, group: 1, keep: 400 },
  "1h":  { base: "1h",    size: 400, refresh: 900, group: 1, keep: 400 },
};
const SECONDS: Record<string, number> = { "1min": 60, "15min": 900, "1h": 3600 };

async function refresh(db: SupabaseClient, base: string, size: number) {
  const q = new URLSearchParams({ symbol: "XAU/USD", interval: base, outputsize: String(size), timezone: "UTC", order: "asc", apikey: KEY });
  const r = await fetch(`${API}?${q}`);
  const j = await r.json().catch(() => ({}));
  if (!r.ok || j.status === "error" || !Array.isArray(j.values)) throw new Error(j.code === 429 ? "rate-limited" : "price-feed");
  const rows = j.values.map((v: any) => ({
    tf: base, t: new Date(v.datetime.replace(" ", "T") + "Z").toISOString(),
    o: +v.open, h: +v.high, l: +v.low, c: +v.close,
  })).filter((x: any) => [x.o, x.h, x.l, x.c].every(Number.isFinite));
  if (rows.length) {
    const { error } = await db.from("price_candles").upsert(rows, { onConflict: "tf,t" });
    if (error) throw new Error("store");
  }
  await db.from("price_fetches").upsert({ tf: base, fetched_at: new Date().toISOString() });
  // keep the table small: about two weeks of 1min candles, a few months of the others
  const keepDays = base === "1min" ? 14 : 120;
  await db.from("price_candles").delete().eq("tf", base).lt("t", new Date(Date.now() - keepDays * 864e5).toISOString());
}

// 1min -> 3m (or any group of n base candles), aligned to the clock
function group(rows: { t: number; o: number; h: number; l: number; c: number }[], n: number, sec: number) {
  if (n === 1) return rows;
  const out: typeof rows = [];
  for (const x of rows) {
    const start = Math.floor(x.t / (sec * n)) * sec * n, last = out[out.length - 1];
    if (last && last.t === start) { last.h = Math.max(last.h, x.h); last.l = Math.min(last.l, x.l); last.c = x.c; }
    else out.push({ t: start, o: x.o, h: x.h, l: x.l, c: x.c });
  }
  return out;
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
  try { input = await req.json(); } catch { /* default timeframe */ }
  const spec = TF[input.tf] ?? TF["15m"], tf = TF[input.tf] ? input.tf : "15m";

  const { data: last } = await db.from("price_fetches").select("fetched_at").eq("tf", spec.base).maybeSingle();
  const age = last ? (Date.now() - new Date(last.fetched_at).getTime()) / 1000 : Infinity;
  let warning: string | undefined;
  if (age > spec.refresh) {
    try { await refresh(db, spec.base, spec.size); } catch (e) { warning = (e as Error).message; }   // serve what we have
  }

  const { data: rows, error } = await db.from("price_candles").select("t,o,h,l,c").eq("tf", spec.base)
    .order("t", { ascending: false }).limit(spec.keep * spec.group);
  if (error) return json({ error: "store" }, 500);
  const base = (rows ?? []).reverse().map((r: any) => ({ t: Math.floor(new Date(r.t).getTime() / 1000), o: +r.o, h: +r.h, l: +r.l, c: +r.c }));
  const candles = group(base, spec.group, SECONDS[spec.base]).slice(-spec.keep);
  const { data: f } = await db.from("price_fetches").select("fetched_at").eq("tf", spec.base).maybeSingle();
  if (!candles.length) return json({ error: warning ?? "no-data" }, 503);
  return json({ tf, candles, fetched_at: f?.fetched_at ?? null, ...(warning ? { warning } : {}) });
});
