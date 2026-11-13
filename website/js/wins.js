// Member wins: profit screenshots members send in. Two rows drift in opposite directions
// (top to the left, bottom to the right), plus a gallery and a full-size viewer.
// The pictures are listed in js/config.js (WINS) and live in assets/img/wins/.
(function (root) {
  const cfg = root.OTM_CONFIG || {};
  const live = !!(cfg.SUPABASE_URL && cfg.SUPABASE_ANON_KEY);
  const t = (k, v) => (root.OTMI18n ? root.OTMI18n.t(k, v) : k);
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  function items() {
    return (cfg.WINS || []).map((w) => (typeof w === "string" ? { src: w } : w)).filter((w) => w && w.src);
  }
  // until real pictures are added, the demo shows empty frames so the motion can be seen
  const placeholders = (n) => Array.from({ length: n }, (_, i) => ({ ph: true, n: i + 1, w: [210, 250, 180, 270, 230, 200][i % 6] }));

  const isVid = (w) => /\.(mp4|webm|mov)$/i.test(w.src);
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  // videos play muted and looped in the rows; they carry no sound
  function media(w) {
    if (isVid(w)) return `<video src="${esc(w.src)}"${w.poster ? ` poster="${esc(w.poster)}"` : ""} muted loop playsinline preload="metadata"${still ? "" : " autoplay"} aria-label="${esc(w.alt || t("wins.alt"))}"></video><span class="win__play" aria-hidden="true">▶</span>`;
    return `<img src="${esc(w.src)}" alt="${esc(w.alt || t("wins.alt"))}" loading="lazy" decoding="async">`;
  }
  function tile(w, copy) {
    const hide = copy ? ' aria-hidden="true" tabindex="-1"' : "";
    if (w.ph) return `<div class="win win--ph" style="--w:${w.w}px"${copy ? ' aria-hidden="true"' : ""}><span>${esc(t("wins.ph", { n: w.n }))}</span></div>`;
    return `<button type="button" class="win" data-win="${w.k}"${hide}>${media(w)}</button>`;
  }

  function marquee(el) {
    if (!el) return false;
    let list = items().map((w, k) => ({ ...w, k }));
    const ph = !list.length;
    if (ph) {
      if (live) { const sec = el.closest("[data-wins-section]"); if (sec) sec.hidden = true; else el.hidden = true; return false; }
      list = placeholders(12);
    }
    const rows = [[], []];
    list.forEach((w, i) => rows[i % 2].push(w));
    if (!rows[1].length) rows[1] = rows[0].slice().reverse();
    const fill = (r) => { let out = r.slice(); while (out.length < 7) out = out.concat(r); return out; };
    el.innerHTML = rows.map((r, ri) => {
      const f = fill(r), dur = Math.max(36, f.length * 7);
      return `<div class="wins__row wins__row--${ri ? "right" : "left"}" style="--dur:${dur}s">
        <div class="wins__track"><div class="wins__set">${f.map((w) => tile(w, false)).join("")}</div><div class="wins__set" aria-hidden="true">${f.map((w) => tile(w, true)).join("")}</div></div>
      </div>`;
    }).join("") + (ph ? `<p class="wins__phnote">${esc(t("wins.phNote"))}</p>` : "");
    wire(el, list);
    return !ph;
  }

  function grid(el) {
    if (!el) return 0;
    const list = items().map((w, k) => ({ ...w, k }));
    el.innerHTML = list.length
      ? list.map((w) => `<button type="button" class="win win--grid" data-win="${w.k}">${media(w)}</button>`).join("")
      : `<p class="muted">${esc(t("wins.empty"))}</p>`;
    wire(el, list);
    return list.length;
  }

  // full-size viewer: arrows, swipe-free keyboard (← → Esc), closes on backdrop
  let box = null, cur = 0, all = [];
  function open(k) {
    all = items(); if (!all.length) return;
    cur = k;
    if (!box) {
      box = document.createElement("div");
      box.className = "winbox"; box.hidden = true;
      box.setAttribute("role", "dialog"); box.setAttribute("aria-modal", "true"); box.setAttribute("aria-label", t("wins.kicker"));
      box.innerHTML = `<button type="button" class="winbox__x" aria-label="${esc(t("app.close"))}">×</button>
        <button type="button" class="winbox__nav winbox__nav--prev" aria-label="‹">‹</button>
        <figure><img alt=""><video controls playsinline muted loop hidden></video><figcaption></figcaption></figure>
        <button type="button" class="winbox__nav winbox__nav--next" aria-label="›">›</button>`;
      document.body.appendChild(box);
      box.addEventListener("click", (e) => { if (e.target === box) close(); });
      box.querySelector(".winbox__x").addEventListener("click", close);
      box.querySelector(".winbox__nav--prev").addEventListener("click", () => show(cur - 1));
      box.querySelector(".winbox__nav--next").addEventListener("click", () => show(cur + 1));
      document.addEventListener("keydown", (e) => {
        if (box.hidden) return;
        if (e.key === "Escape") close(); else if (e.key === "ArrowLeft") show(cur - 1); else if (e.key === "ArrowRight") show(cur + 1);
      });
    }
    box.hidden = false; document.body.style.overflow = "hidden";
    show(k); box.querySelector(".winbox__x").focus();
  }
  function show(k) {
    cur = (k + all.length) % all.length;
    const w = all[cur], img = box.querySelector("img"), vid = box.querySelector("video");
    if (isVid(w)) { img.hidden = true; img.removeAttribute("src"); vid.hidden = false; vid.src = w.src; if (w.poster) vid.poster = w.poster; vid.play().catch(() => {}); }
    else { vid.pause(); vid.hidden = true; vid.removeAttribute("src"); img.hidden = false; img.src = w.src; img.alt = w.alt || t("wins.alt"); }
    box.querySelector("figcaption").textContent = `${cur + 1} / ${all.length}${w.alt ? " · " + w.alt : ""}`;
  }
  function close() { if (!box) return; const vid = box.querySelector("video"); vid.pause(); box.hidden = true; document.body.style.overflow = ""; }

  function wire(el) {
    el.querySelectorAll("[data-win]").forEach((b) => b.addEventListener("click", () => open(+b.dataset.win)));
  }

  root.OTMWins = { marquee, grid, count: () => items().length };
})(window);
