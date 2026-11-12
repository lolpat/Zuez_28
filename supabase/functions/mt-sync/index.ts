// mt-sync: pulls MT4/MT5 trade history into the journal automatically, through MetaApi.
//
// A member gives their account's INVESTOR (read-only) password once. This function hands it to
// MetaApi, which keeps the terminal connection; the password is never stored in our database.
// After that, closed trades are copied into public.trades on every sync.
//
// Actions (POST JSON):
//   { action: "connect", account_id, server, password }   member, signed in
//   { action: "sync", account_id }                          member, signed in
//   { action: "disconnect", account_id }                    member, signed in
//   { action: "sync_all" }                                  the schedule, with header x-cron-secret
//
// Secrets (supabase secrets set ...):
//   METAAPI_TOKEN    API token from https://app.metaapi.cloud/token
//   METAAPI_REGION   optional, default "new-york" (MetaApi's public regions: new-york, london)
//   CRON_SECRET      any long random string; the schedule sends it in x-cron-secret
// SUPABASE_URL, SUPABASE_ANON_KEY and SUPABASE_SERVICE_ROLE_KEY are provided by Supabase.
import { createClient, type SupabaseClient } from "jsr:@supabase/supabase-js@2";

const PROVISIONING = "https://mt-provisioning-api-v1.agiliumtrade.agiliumtrade.ai";
const clientApi = (region: string) => `https://mt-client-api-v1.${region}.agiliumtrade.ai`;
const TOKEN = Deno.env.get("METAAPI_TOKEN") ?? "";
const REGION = Deno.env.get("METAAPI_REGION") ?? "new-york";
const CRON_SECRET = Deno.env.get("CRON_SECRET") ?? "";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-cron-secret",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...cors, "Content-Type": "application/json" } });
const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));
const txId = () => Array.from(crypto.getRandomValues(new Uint8Array(16)), (b) => b.toString(16).padStart(2, "0")).join("");

class SyncError extends Error {
  constructor(public code: string, message?: string) { super(message ?? code); }
}

async function metaapi(url: string, init: RequestInit = {}) {
  const res = await fetch(url, { ...init, headers: { "auth-token": TOKEN, "Content-Type": "application/json", ...(init.headers ?? {}) } });
  const text = await res.text();
  let body: any = null;
  try { body = text ? JSON.parse(text) : null; } catch { body = { message: text }; }
  return { res, body };
}

// MetaApi error codes -> short codes the site translates
function mapError(body: any): SyncError {
  const raw = String(body?.details?.code ?? body?.details ?? body?.error ?? "");
  const msg = String(body?.message ?? "MetaApi error");
  if (/E_AUTH/.test(raw) || /auth/i.test(msg) && /fail|invalid/i.test(msg)) return new SyncError("bad-login", msg);
  if (/E_SRV_NOT_FOUND/.test(raw)) return new SyncError("bad-server", msg);
  if (/E_PASSWORD_CHANGE_REQUIRED/.test(raw)) return new SyncError("password-change", msg);
  if (/E_TRADING_ACCOUNT_DISABLED/.test(raw)) return new SyncError("account-disabled", msg);
  return new SyncError("provider", msg);
}

// ------------------------------------------------------------------ connect
async function createMetaApiAccount(acc: any, server: string, password: string) {
  const transaction = txId();
  const body = JSON.stringify({
    login: String(acc.account_number).replace(/\D/g, ""),
    password, server,
    name: `OTM ${acc.broker} ${acc.account_number}`.slice(0, 60),
    platform: acc.platform === "MT4" ? "mt4" : "mt5",
    magic: 0, type: "cloud-g2", region: REGION, reliability: "regular",
  });
  // MetaApi may answer 202 while it detects the broker's settings; re-send with the same transaction id
  for (let i = 0; i < 6; i++) {
    const { res, body: out } = await metaapi(`${PROVISIONING}/users/current/accounts`, {
      method: "POST", body, headers: { "transaction-id": transaction },
    });
    if (res.status === 201 || res.status === 200) return out.id as string;
    if (res.status === 202) {
      const wait = Math.min(12, Number(res.headers.get("retry-after")) || 10);
      await sleep(wait * 1000);
      continue;
    }
    throw mapError(out);
  }
  throw new SyncError("slow", "MetaApi is still checking the broker server. Try again in a minute.");
}

// ------------------------------------------------------------------ deals -> trades
type Deal = {
  id: string; type: string; entryType?: string; symbol?: string; time: string; volume?: number; price?: number;
  profit: number; commission?: number; swap?: number; positionId?: string; stopLoss?: number; takeProfit?: number;
};
const isTrade = (d: Deal) => d.type === "DEAL_TYPE_BUY" || d.type === "DEAL_TYPE_SELL";
const isClose = (d: Deal) => isTrade(d) && ["DEAL_ENTRY_OUT", "DEAL_ENTRY_OUT_BY", "DEAL_ENTRY_INOUT"].includes(d.entryType ?? "");
const isOpen = (d: Deal) => isTrade(d) && (d.entryType === "DEAL_ENTRY_IN" || d.entryType === "DEAL_ENTRY_INOUT");
const round = (n: number, p = 2) => Math.round((n || 0) * 10 ** p) / 10 ** p;

async function readDeals(region: string, metaId: string, from: Date, to: Date) {
  const all: Deal[] = [];
  for (let offset = 0; ; offset += 1000) {
    const url = `${clientApi(region)}/users/current/accounts/${metaId}/history-deals/time/${from.toISOString()}/${to.toISOString()}?offset=${offset}&limit=1000`;
    const { res, body } = await metaapi(url);
    if (!res.ok) throw mapError(body);
    all.push(...(body as Deal[]));
    if ((body as Deal[]).length < 1000) break;
  }
  return all;
}

async function readPositionDeals(region: string, metaId: string, positionId: string) {
  const { res, body } = await metaapi(`${clientApi(region)}/users/current/accounts/${metaId}/history-deals/position/${positionId}`);
  return res.ok ? (body as Deal[]) : [];
}

async function dealsToTrades(deals: Deal[], region: string, metaId: string) {
  const byPos = new Map<string, Deal[]>();
  for (const d of deals) if (isTrade(d) && d.positionId) {
    const list = byPos.get(d.positionId) ?? []; list.push(d); byPos.set(d.positionId, list);
  }
  const rows: any[] = [];
  for (const [pos, list] of byPos) {
    const closes = list.filter(isClose).sort((a, b) => a.time.localeCompare(b.time));
    if (!closes.length) continue; // still open
    let open = list.find(isOpen);
    if (!open) open = (await readPositionDeals(region, metaId, pos)).find(isOpen); // opened before the window
    const openVol = open?.volume || closes.reduce((s, c) => s + (c.volume || 0), 0) || 1;
    for (const c of closes) {
      const share = (c.volume || 0) / openVol;
      rows.push({
        ticket: closes.length === 1 ? pos : `${pos}-${c.id}`,
        symbol: (c.symbol || open?.symbol || "").toUpperCase(),
        side: open ? (open.type === "DEAL_TYPE_BUY" ? "buy" : "sell") : (c.type === "DEAL_TYPE_SELL" ? "buy" : "sell"),
        volume: round(c.volume || 0),
        open_time: open?.time ?? c.time, close_time: c.time,
        open_price: open?.price ?? null, close_price: c.price ?? null,
        sl: open?.stopLoss ?? null, tp: open?.takeProfit ?? null,
        commission: round((c.commission || 0) + (open?.commission || 0) * share),
        swap: round((c.swap || 0) + (open?.swap || 0) * share),
        profit: round(c.profit),
        source: "sync",
      });
    }
  }
  return rows;
}

// ------------------------------------------------------------------ sync one account
async function syncAccount(db: SupabaseClient, acc: any) {
  const setAcc = (f: Record<string, unknown>) => db.from("broker_accounts").update(f).eq("id", acc.id);
  try {
    const { res, body: meta } = await metaapi(`${PROVISIONING}/users/current/accounts/${acc.metaapi_id}`);
    if (!res.ok) throw mapError(meta);
    if (meta.state !== "DEPLOYED") {
      await metaapi(`${PROVISIONING}/users/current/accounts/${acc.metaapi_id}/deploy`, { method: "POST" });
      await setAcc({ sync_status: "connecting", sync_error: "" });
      return { status: "connecting", added: 0 };
    }
    if (meta.connectionStatus && meta.connectionStatus !== "CONNECTED") {
      await setAcc({ sync_status: "connecting", sync_error: String(meta.connectionStatus) });
      return { status: "connecting", added: 0 };
    }
    const region = meta.region || REGION;
    const firstRun = !acc.last_sync_at;
    // re-read a week before the last sync so late partial closes are not missed; tickets dedupe it
    const from = firstRun ? new Date("2000-01-01T00:00:00Z") : new Date(new Date(acc.last_sync_at).getTime() - 7 * 864e5);
    const to = new Date(Date.now() + 864e5);
    const deals = await readDeals(region, acc.metaapi_id, from, to);
    const rows = await dealsToTrades(deals, region, acc.metaapi_id);

    const { data: prof } = await db.from("profiles").select("status").eq("id", acc.user_id).single();
    let added = 0;
    if (prof?.status === "approved" && rows.length) {
      const { data: have } = await db.from("trades").select("ticket").eq("account_id", acc.id);
      const known = new Set((have ?? []).map((r: any) => r.ticket));
      const fresh = rows.filter((r) => !known.has(r.ticket)).map((r) => ({ ...r, user_id: acc.user_id, account_id: acc.id }));
      for (let i = 0; i < fresh.length; i += 500) {
        const { error } = await db.from("trades").insert(fresh.slice(i, i + 500));
        if (error) throw new SyncError("db", error.message);
      }
      added = fresh.length;
    }
    const patch: Record<string, unknown> = { sync_status: "ok", sync_error: "", last_sync_at: new Date().toISOString() };
    // first full read: deposits minus withdrawals become the starting balance, if the member left it at 0
    if (firstRun && !(+acc.start_balance)) {
      const net = deals.filter((d) => d.type === "DEAL_TYPE_BALANCE").reduce((s, d) => s + (d.profit || 0), 0);
      if (net > 0) patch.start_balance = round(net);
    }
    await setAcc(patch);
    return { status: "ok", added };
  } catch (e) {
    const err = e instanceof SyncError ? e : new SyncError("provider", String(e));
    await setAcc({ sync_status: "error", sync_error: `${err.code}: ${err.message}`.slice(0, 300) });
    return { status: "error", error: err.code, added: 0 };
  }
}

// ------------------------------------------------------------------ handler
Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "POST") return json({ error: "method" }, 405);
  if (!TOKEN) return json({ error: "not-configured" }, 503);

  const url = Deno.env.get("SUPABASE_URL")!;
  const db = createClient(url, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
  let input: any = {};
  try { input = await req.json(); } catch { return json({ error: "bad-request" }, 400); }

  // the schedule
  if (input.action === "sync_all") {
    if (!CRON_SECRET || req.headers.get("x-cron-secret") !== CRON_SECRET) return json({ error: "forbidden" }, 403);
    const { data: accs } = await db.from("broker_accounts").select("*").not("metaapi_id", "is", null);
    const started = Date.now(), results: unknown[] = [];
    for (const acc of accs ?? []) {
      if (Date.now() - started > 120_000) break; // stay inside the function time limit; the rest go next run
      results.push({ id: acc.id, ...(await syncAccount(db, acc)) });
    }
    return json({ ok: true, results });
  }

  // a signed-in member, acting on their own account only
  const jwt = (req.headers.get("Authorization") ?? "").replace(/^Bearer\s+/i, "");
  const { data: auth } = await createClient(url, Deno.env.get("SUPABASE_ANON_KEY")!).auth.getUser(jwt);
  const user = auth?.user;
  if (!user) return json({ error: "signed-out" }, 401);
  const { data: acc } = await db.from("broker_accounts").select("*").eq("id", input.account_id).eq("user_id", user.id).single();
  if (!acc) return json({ error: "not-found" }, 404);

  try {
    if (input.action === "connect") {
      const server = String(input.server ?? "").trim(), password = String(input.password ?? "");
      if (!server || !password) return json({ error: "missing" }, 400);
      if (acc.metaapi_id) await metaapi(`${PROVISIONING}/users/current/accounts/${acc.metaapi_id}`, { method: "DELETE" });
      const metaId = await createMetaApiAccount(acc, server, password);
      await metaapi(`${PROVISIONING}/users/current/accounts/${metaId}/deploy`, { method: "POST" });
      // a server named like "...-Demo" is a demo account; it goes on the demo leaderboard
      // ...unless the site owner has corrected this account's type (brokers sometimes mislabel)
      const account_type = acc.type_locked ? acc.account_type : /demo/i.test(server) ? "demo" : (acc.account_type ?? "live");
      await db.from("broker_accounts").update({ server, account_type, metaapi_id: metaId, sync_status: "connecting", sync_error: "", last_sync_at: null }).eq("id", acc.id);
      // give the terminal a moment to log in, then try a first read
      // (kept short: the whole call must finish inside Supabase's function time limit)
      for (let i = 0; i < 4; i++) {
        await sleep(8_000);
        const r = await syncAccount(db, { ...acc, server, metaapi_id: metaId, last_sync_at: null });
        if (r.status !== "connecting") return json(r, r.status === "error" ? 400 : 200);
      }
      return json({ status: "connecting", added: 0 });
    }
    if (input.action === "sync") {
      if (!acc.metaapi_id) return json({ error: "not-connected" }, 400);
      const r = await syncAccount(db, acc);
      return json(r, r.status === "error" ? 400 : 200);
    }
    if (input.action === "disconnect") {
      if (acc.metaapi_id) await metaapi(`${PROVISIONING}/users/current/accounts/${acc.metaapi_id}`, { method: "DELETE" });
      await db.from("broker_accounts").update({ metaapi_id: null, sync_status: "off", sync_error: "" }).eq("id", acc.id);
      return json({ status: "off" });
    }
    return json({ error: "bad-request" }, 400);
  } catch (e) {
    const err = e instanceof SyncError ? e : new SyncError("provider", String(e));
    await db.from("broker_accounts").update({ sync_status: "error", sync_error: `${err.code}: ${err.message}`.slice(0, 300) }).eq("id", acc.id);
    return json({ error: err.code, message: err.message }, 400);
  }
});
