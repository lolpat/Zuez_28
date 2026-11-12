// Public pages: landing, log in, register.
(function () {
  const { t, apply, setLang } = window.OTMI18n;
  const cfg = window.OTM_CONFIG;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];

  function common() {
    apply();
    $$("[data-lang-toggle]").forEach((b) => b.addEventListener("click", () => setLang(window.OTMI18n.lang === "th" ? "en" : "th")));
    $$("[data-telegram]").forEach((a) => { a.href = cfg.TELEGRAM_URL; a.target = "_blank"; a.rel = "noopener"; });
    $$("[data-year]").forEach((el) => { el.textContent = new Date().getFullYear(); });

    // entrances
    if (!matchMedia("(prefers-reduced-motion: reduce)").matches && "IntersectionObserver" in window) {
      document.documentElement.classList.add("js-ready");
      const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }), { rootMargin: "0px 0px -8% 0px" });
      $$(".reveal").forEach((el) => io.observe(el));
    }
  }

  // ------------------------------------------------------------ landing
  function landing() {
    const box = $("#brokers");
    if (box) {
      box.innerHTML = cfg.BROKERS.map((b) => {
        const ready = b.url && b.url !== "#";
        return `<article class="broker reveal">
          <h3>${b.name}</h3>
          ${ready ? `<a class="btn btn--ghost" href="${b.url}" target="_blank" rel="noopener" data-i18n="brokers.open"></a>`
                  : `<span class="badge" data-i18n="brokers.soon"></span>`}
        </article>`;
      }).join("");
      apply(box);
    }
    // sample journal preview (made-up numbers, labelled as such)
    const pv = $("#preview-chart");
    if (pv) {
      let v = 0; const pts = [];
      const steps = [12, -6, 18, 9, -11, 22, 14, -4, 26, 8, -9, 31, 17, -7, 24, 19, -12, 28, 16, 21];
      steps.forEach((s, i) => { v += s; pts.push({ x: i, y: v }); });
      pv.innerHTML = window.OTMCharts.line(pts, { fmt: (x) => "$" + x.toFixed(0), label: "sample equity curve" });
    }
  }

  // ------------------------------------------------------------ auth
  function setError(form, msg) {
    const box = $(".form-msg", form);
    box.hidden = !msg; box.className = "alert alert--err form-msg"; box.textContent = msg || "";
  }
  function setOk(form, msg) {
    const box = $(".form-msg", form);
    box.hidden = false; box.className = "alert alert--ok form-msg"; box.textContent = msg;
  }
  function require(form, names) {
    let ok = true;
    names.forEach((n) => {
      const el = form.elements[n];
      const bad = !String(el.value || "").trim();
      el.setAttribute("aria-invalid", bad ? "true" : "false");
      if (bad && ok) { el.focus(); ok = false; }
    });
    return ok;
  }
  const errText = (e) => e.message === "bad-login" ? t("auth.err.login") : e.message === "email-taken" ? t("auth.err.taken") : t("auth.err.generic", { msg: e.message });

  async function authPages(store) {
    const demo = $("#demo-box");
    if (demo) {
      demo.hidden = store.live;
      $$("[data-demo]", demo).forEach((b) => b.addEventListener("click", async () => {
        await store.demoSignIn(b.dataset.demo);
        location.href = "app.html";
      }));
    }
    if (await store.getSession()) { if ($("#login-form") || $("#register-form")) location.replace("app.html"); }

    const login = $("#login-form");
    if (login) {
      login.addEventListener("submit", async (e) => {
        e.preventDefault(); setError(login, "");
        if (!require(login, ["email", "password"])) return setError(login, t("auth.err.required"));
        const btn = $("button[type=submit]", login); btn.disabled = true;
        try { await store.signIn(login.email.value.trim(), login.password.value); location.href = "app.html"; }
        catch (err) { setError(login, errText(err)); btn.disabled = false; }
      });
      $("#forgot").addEventListener("click", async () => {
        if (!require(login, ["email"])) return setError(login, t("auth.err.required"));
        try { await store.resetPassword(login.email.value.trim()); setOk(login, t("auth.sent")); }
        catch (err) { setError(login, errText(err)); }
      });
    }

    const reg = $("#register-form");
    if (reg) {
      const ref = new URLSearchParams(location.search).get("ref");
      if (ref) reg.referral_code.value = ref.toUpperCase();
      reg.broker.innerHTML = `<option value="" data-i18n="auth.broker.pick"></option>` + cfg.BROKERS.map((b) => `<option value="${b.id}">${b.name}</option>`).join("");
      apply(reg);
      reg.addEventListener("submit", async (e) => {
        e.preventDefault(); setError(reg, "");
        if (!require(reg, ["full_name", "email", "telegram", "broker", "account_number", "password"])) return setError(reg, t("auth.err.required"));
        if (reg.password.value.length < 8) { reg.password.setAttribute("aria-invalid", "true"); return setError(reg, t("auth.err.short")); }
        if (!reg.agree.checked) return setError(reg, t("auth.err.agree"));
        const btn = $("button[type=submit]", reg); btn.disabled = true;
        let tg = reg.telegram.value.trim(); if (tg && !tg.startsWith("@")) tg = "@" + tg;
        try {
          const r = await store.signUp({
            full_name: reg.full_name.value.trim(), email: reg.email.value.trim(), password: reg.password.value,
            telegram: tg, broker: reg.broker.value, platform: reg.platform.value,
            account_number: reg.account_number.value.trim(), referral_code: reg.referral_code.value.trim().toUpperCase(),
            language: window.OTMI18n.lang
          });
          if (r.needsConfirm) { setOk(reg, t("auth.confirm")); btn.disabled = false; }
          else location.href = "app.html";
        } catch (err) { setError(reg, errText(err)); btn.disabled = false; }
      });
    }
  }

  document.addEventListener("DOMContentLoaded", async () => {
    common();
    landing();
    if ($("#login-form") || $("#register-form")) {
      const store = await window.OTMStore.init();
      authPages(store);
    }
  });
})();
