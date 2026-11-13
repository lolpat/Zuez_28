// Order The Market: site settings.
// Leave SUPABASE_URL empty to run the portal in demo mode (sample data, saved in this browser only).
// To go live: create a free Supabase project, run supabase/schema.sql, then paste the two values
// from Supabase > Project Settings > API here. The anon key is safe to publish; the database
// rules in schema.sql decide who can see what.
window.OTM_CONFIG = {
  SUPABASE_URL: "",
  SUPABASE_ANON_KEY: "",

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
