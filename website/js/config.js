// Order The Market: site settings.
// Leave SUPABASE_URL empty to run the portal in demo mode (sample data, saved in this browser only).
// To go live: create a free Supabase project, run supabase/schema.sql, then paste the two values
// from Supabase > Project Settings > API here. The anon key is safe to publish; the database
// rules in schema.sql decide who can see what.
window.OTM_CONFIG = {
  SUPABASE_URL: "https://jfapovqefkcluwmnjxmx.supabase.co",
  SUPABASE_ANON_KEY: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpmYXBvdnFlZmtjbHV3bW5qeG14Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTUxMDE4MjksImV4cCI6MjExMDY3NzgyOX0.BW6th9eQhyoq1teIKtGHqIfUfGHct2bw2JoALT5Fr8k",

  // Member wins: profit screenshots shown on the home page (two moving rows) and on the Client Profit
  // page. Files go in assets/img/wins/; js/wins-data.js lists them ({ src, thumb } or a clip
  // { src: "...mp4", poster }). With an empty list the demo shows empty frames and the live site hides it.
  // The list itself lives in js/wins-data.js.
  WINS: [],

  // Most MT4/MT5 accounts one member can add (keeps the journal quick). The database enforces 10 too.
  MAX_ACCOUNTS: 10,

  // Automatic MT4/MT5 history (members connect an account with its read-only investor password).
  // Needs the mt-sync function and a MetaApi token in Supabase (see README). Set to false to hide it.
  AUTO_SYNC: true,

  // Telegram: the main contact channel (from the owner).
  TELEGRAM_URL: "https://t.me/zuez_28",
  TELEGRAM_HANDLE: "@zuez_28",
  // Free signal room (public Telegram group) and Instagram, shown in the contact section and footer.
  SIGNAL_URL: "https://t.me/+Zyobh3qn3pI1ZmFk",

  // Network total on the home page (from the owner: everyone under the OTM IB at all three brokers).
  // members = everyone in the network, ibs = how many of them are IBs. Update by hand when they change;
  // remove NETWORK to hide the card.
  NETWORK: { members: 489, ibs: 12, date: "2026-11-19" },

  // Telegram member counts on the home page. The bot reads them from Telegram every hour (needs the
  // TG_BOT_TOKEN secret, see README). VIP_CHAT / FREE_CHAT are the chats' ids from public.tg_chats; leave
  // FREE_CHAT null until the bot is in the free room. FALLBACK is shown until the live count loads (and in
  // previews): the real count read by the bot on the date given.
  COMMUNITY: { VIP_CHAT: -1003941112920, FREE_CHAT: null, FALLBACK: { vip: 337, free: null, date: "2026-11-19" } },
  INSTAGRAM_URL: "https://www.instagram.com/fxzuez_28/",
  INSTAGRAM_HANDLE: "@fxzuez_28",

  // IB sign-up links, referral codes and official logos per broker (from the owner; logos from
  // each broker's partner brand kit, used unaltered).
  // servers: the broker's MT5 server names, offered as choices in Add account (fill in the real ones).
  // bonus: deposit bonus shown on the card. first / next = percent on the first and later deposits,
  // firstMax = largest first-deposit bonus in USD, cap = total bonus limit in USD. Leave a field out
  // to hide it, or remove `bonus` to hide the box. Brokers change these by campaign: keep them current.
  BROKERS: [
    { id: "vantage", name: "Vantage", url: "https://vigco.co/la-com-inv/ZUEZ28", code: "ZUEZ28", logo: "assets/img/brokers/vantage.png",
      bonus: { first: 150, firstMax: 1500, next: 50, cap: 3000 }, servers: [] },
    { id: "puprime", name: "PU Prime", url: "https://puvip.co/la-partners/OTM2028", code: "OTM2028", logo: "assets/img/brokers/puprime.jpg",
      bonus: { first: 100, firstMax: 1000, next: 20, cap: 10000 }, servers: [] },
    { id: "vtmarkets", name: "VT Markets", url: "https://vtm.pro/la5-com/global/OTM2028", code: "OTM2028", logo: "assets/img/brokers/vtmarkets.svg",
      bonus: { first: 100, next: 20, cap: 10000 }, servers: [] }
  ]
};
