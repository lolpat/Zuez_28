// Order The Market: site settings.
// Leave SUPABASE_URL empty to run the portal in demo mode (sample data, saved in this browser only).
// To go live: create a free Supabase project, run supabase/schema.sql, then paste the two values
// from Supabase > Project Settings > API here. The anon key is safe to publish; the database
// rules in schema.sql decide who can see what.
window.OTM_CONFIG = {
  SUPABASE_URL: "",
  SUPABASE_ANON_KEY: "",

  // Member wins: profit screenshots shown on the home page (two moving rows) and on the Client Profit
  // page. Put the files in assets/img/wins/ and list them here, e.g.
  //   WINS: ["assets/img/wins/01.jpg", { src: "assets/img/wins/02.jpg", alt: "XAUUSD +$118" }],
  // With an empty list the demo shows empty frames; the live site hides the section.
  WINS: [
    "assets/img/wins/win-01.jpg",
    "assets/img/wins/win-02.jpg",
    "assets/img/wins/win-03.jpg",
    { src: "assets/img/wins/clip-01.mp4", poster: "assets/img/wins/clip-01.jpg" },
    "assets/img/wins/win-04.jpg",
    "assets/img/wins/win-05.jpg",
    "assets/img/wins/win-06.jpg",
    "assets/img/wins/win-07.jpg",
    "assets/img/wins/win-08.jpg",
    "assets/img/wins/win-09.jpg",
    "assets/img/wins/win-10.jpg",
    "assets/img/wins/win-11.jpg",
    "assets/img/wins/win-12.jpg",
    "assets/img/wins/win-13.jpg",
    { src: "assets/img/wins/clip-02.mp4", poster: "assets/img/wins/clip-02.jpg" },
    "assets/img/wins/win-14.jpg",
    "assets/img/wins/win-15.jpg",
    "assets/img/wins/win-16.jpg",
    "assets/img/wins/win-17.jpg",
    "assets/img/wins/win-18.jpg",
    "assets/img/wins/win-19.jpg",
    "assets/img/wins/win-20.jpg",
    "assets/img/wins/win-21.jpg",
    "assets/img/wins/win-22.jpg"
  ],

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
      bonus: { first: 150, next: 50 }, servers: [] },
    { id: "puprime", name: "PU Prime", url: "https://puvip.co/la-partners/OTM2028", code: "OTM2028", logo: "assets/img/brokers/puprime.jpg",
      bonus: { first: 100, firstMax: 1000, next: 20, cap: 10000 }, servers: [] },
    { id: "vtmarkets", name: "VT Markets", url: "https://vtm.pro/la5-com/global/OTM2028", code: "OTM2028", logo: "assets/img/brokers/vtmarkets.svg",
      bonus: { first: 100, next: 20, cap: 10000 }, servers: [] }
  ]
};
