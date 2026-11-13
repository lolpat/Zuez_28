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
  const usd = (n) => "$" + Number(n).toLocaleString("en-US");
  function bonusBox(x) {
    if (!x || (!x.first && !x.next)) return "";
    const cell = (key, pct, sub) => pct ? `<div class="bonus__cell">
        <span class="bonus__lbl" data-i18n="${key}"></span>
        <b class="bonus__pct">${pct}%</b>
        ${sub || ""}
      </div>` : "";
    // the small lines are always there (blank when a broker has no limit), so all three boxes line up
    const firstSub = x.firstMax ? `<small><span data-i18n="bonus.upto"></span> ${usd(x.firstMax)}</small>` : `<small aria-hidden="true">&nbsp;</small>`;
    return `<div class="bonus">
      <p class="bonus__kicker" data-i18n="bonus.kicker"></p>
      <div class="bonus__row">${cell("bonus.first", x.first, firstSub)}${cell("bonus.next", x.next, `<small aria-hidden="true">&nbsp;</small>`)}</div>
      <p class="bonus__cap">${x.cap ? `<span data-i18n="bonus.cap"></span> ${usd(x.cap)}` : `<span data-i18n="bonus.noCap"></span>`}</p>
    </div>`;
  }
  // first-deposit bonus panel: pick a broker, see what a deposit turns into
  function bonusCalc() {
    const box = $("#bonus-calc");
    if (!box) return;
    const list = cfg.BROKERS.filter((b) => b.bonus && b.bonus.first);
    if (!list.length) { box.remove(); return; }
    let cur = list[0].id;
    const shield = `<svg class="calc__icon" viewBox="0 0 24 24" width="26" height="26" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7.5 3v5.6c0 4.6-3.2 8.3-7.5 9.4-4.3-1.1-7.5-4.8-7.5-9.4V6z"/><path d="M8.6 12.2l2.4 2.4 4.5-4.8"/></svg>`;
    const draw = () => {
      const b = list.find((o) => o.id === cur), x = b.bonus;
      const mult = String(+(1 + x.first / 100).toFixed(2));
      const tiles = [300, 500, 1000].map((d) => {
        const bonus = Math.min(d * x.first / 100, x.firstMax || Infinity);
        return `<div class="calc__tile">
            <span class="calc__dep">${usd(d)} <i aria-hidden="true">→</i></span>
            <b class="calc__bal">${usd(d + bonus)}</b>
            <small>+${usd(bonus)} <span data-i18n="calc.credit"></span></small>
          </div>`;
      }).join("");
      const ready = b.url && b.url !== "#";
      box.innerHTML = `
        <div class="calc__head">${shield}<h3 data-i18n="calc.title"></h3></div>
        <div class="calc__tabs" role="tablist" data-i18n-aria="calc.pick">
          ${list.map((o) => `<button type="button" role="tab" class="calc__tab" aria-selected="${o.id === cur}" data-b="${o.id}">${o.name} <em>${o.bonus.first}%</em></button>`).join("")}
        </div>
        <p class="calc__lead">${t("calc.lead", { name: b.name, pct: x.first, mult })}${x.firstMax ? " " + t("calc.max", { max: usd(x.firstMax) }) : ""}</p>
        <ol class="calc__steps"><li data-i18n="calc.s1"></li><li data-i18n="calc.s2"></li><li data-i18n="calc.s3"></li></ol>
        <div class="calc__tiles">${tiles}</div>
        ${ready ? `<a class="btn btn--gold calc__cta" href="${b.url}" target="_blank" rel="noopener sponsored">${t("calc.cta", { name: b.name, pct: x.first })}
            <svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg></a>` : ""}
        ${b.code ? `<p class="calc__code"><span data-i18n="brokers.code"></span> <b>${b.code}</b></p>` : ""}`;
      apply(box);
      box.querySelectorAll("[data-b]").forEach((btn) => btn.addEventListener("click", () => { cur = btn.dataset.b; draw(); box.querySelector(`[data-b="${cur}"]`).focus(); }));
    };
    draw();
    document.addEventListener("otm:lang", draw);
  }
  function landing() {
    bonusCalc();
    if (window.OTMWins) window.OTMWins.marquee($("[data-wins]"));
    const box = $("#brokers");
    if (box) {
      box.innerHTML = cfg.BROKERS.map((b) => {
        const ready = b.url && b.url !== "#";
        return `<article class="broker reveal">
          ${b.logo ? `<img class="broker__logo" src="${b.logo}" alt="${b.name}" width="200" height="80" loading="lazy">` : ""}
          <h3 ${b.logo ? 'class="sr-only"' : ""}>${b.name}</h3>
          ${bonusBox(b.bonus)}
          ${b.code ? `<div class="broker__code"><span class="broker__codelbl" data-i18n="brokers.code"></span><b>${b.code}</b>
            <button class="btn btn--quiet btn--sm" type="button" data-copy="${b.code}" data-i18n="app.copy"></button></div>` : ""}
          ${ready ? `<a class="btn btn--gold" href="${b.url}" target="_blank" rel="noopener sponsored" data-i18n="brokers.open"></a>`
                  : `<span class="badge" data-i18n="brokers.soon"></span>`}
        </article>`;
      }).join("");
      box.querySelectorAll("[data-copy]").forEach((btn) => btn.addEventListener("click", async () => {
        try { await navigator.clipboard.writeText(btn.dataset.copy); } catch { const el = btn.previousElementSibling, r = document.createRange(); r.selectNodeContents(el); getSelection().removeAllRanges(); getSelection().addRange(r); return; }
        btn.textContent = t("app.copied");
        setTimeout(() => { btn.textContent = t("app.copy"); }, 1600);
      }));
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
      $("#broker-pick", reg).innerHTML = cfg.BROKERS.map((b) => `<label class="broker-opt">
          <input type="radio" name="broker" value="${b.id}">
          ${b.logo ? `<img src="${b.logo}" alt="${b.name}" width="150" height="60">` : `<span>${b.name}</span>`}
        </label>`).join("");
      $("#broker-pick", reg).addEventListener("change", () => { $("#broker-pick", reg).setAttribute("aria-invalid", "false"); setError(reg, ""); });
      apply(reg);
      reg.addEventListener("submit", async (e) => {
        e.preventDefault(); setError(reg, "");
        if (!require(reg, ["full_name", "email", "telegram"])) return setError(reg, t("auth.err.required"));
        const pick = $("#broker-pick", reg);
        pick.setAttribute("aria-invalid", reg.broker.value ? "false" : "true");
        if (!reg.broker.value) { pick.querySelector("input").focus(); return setError(reg, t("auth.err.broker")); }
        if (!require(reg, ["account_number", "password"])) return setError(reg, t("auth.err.required"));
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
    landing();
    common();
    if ($("#login-form") || $("#register-form")) {
      const store = await window.OTMStore.init();
      authPages(store);
    }
  });
})();
