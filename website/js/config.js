// Order The Market: site settings.
// Leave SUPABASE_URL empty to run the portal in demo mode (sample data, saved in this browser only).
// To go live: create a free Supabase project, run supabase/schema.sql, then paste the two values
// from Supabase > Project Settings > API here. The anon key is safe to publish; the database
// rules in schema.sql decide who can see what.
window.OTM_CONFIG = {
  SUPABASE_URL: "",
  SUPABASE_ANON_KEY: "",

  // Telegram: the main contact channel. PLACEHOLDER until the owner sends the real handle.
  TELEGRAM_URL: "https://t.me/",
  TELEGRAM_HANDLE: "@ordermarket",

  // IB sign-up links per broker. PLACEHOLDER until the owner sends the real links.
  BROKERS: [
    { id: "vantage", name: "Vantage", url: "#" },
    { id: "puprime", name: "PU Prime", url: "#" },
    { id: "vtmarkets", name: "VT Markets", url: "#" }
  ]
};
