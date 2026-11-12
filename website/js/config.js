// Order The Market: site settings.
// Leave SUPABASE_URL empty to run the portal in demo mode (sample data, saved in this browser only).
// To go live: create a free Supabase project, run supabase/schema.sql, then paste the two values
// from Supabase > Project Settings > API here. The anon key is safe to publish; the database
// rules in schema.sql decide who can see what.
window.OTM_CONFIG = {
  SUPABASE_URL: "",
  SUPABASE_ANON_KEY: "",

  // Telegram: the main contact channel (from the owner).
  TELEGRAM_URL: "https://t.me/zuez_28",
  TELEGRAM_HANDLE: "@zuez_28",

  // IB sign-up links and referral codes per broker (from the owner).
  BROKERS: [
    { id: "vantage", name: "Vantage", url: "https://vigco.co/la-com-inv/ZUEZ28", code: "ZUEZ28" },
    { id: "puprime", name: "PU Prime", url: "https://puvip.co/la-partners/OTM2028", code: "OTM2028" },
    { id: "vtmarkets", name: "VT Markets", url: "https://vtm.pro/la5-com/global/OTM2028", code: "OTM2028" }
  ]
};
