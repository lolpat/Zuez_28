// Partner indicator cards (affiliate links). Used by the home page and the portal.
(function (root) {
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const ICON = '<svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19h16"/><path d="M7 15V9M7 9V6M12 16v-5M12 11V8M17 13V5"/><rect x="5.6" y="9" width="2.8" height="5" rx=".6"/><rect x="10.6" y="10" width="2.8" height="5" rx=".6"/><rect x="15.6" y="6" width="2.8" height="6" rx=".6"/></svg>';
  const EXT = '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>';
  function cards(t) {
    const list = (root.OTM_CONFIG && root.OTM_CONFIG.INDICATORS) || [];
    return list.map((x) => {
      const ready = x.url && /^https:\/\//.test(x.url);
      return `<article class="ind-card">
        <div class="ind-card__head"><span class="ind-card__ic">${ICON}</span>
          <div><h3>${esc(x.name)}</h3><p class="ind-card__by">${t("ind.by", { n: esc(x.by) })}</p></div>
          ${x.platforms ? `<span class="ind-card__plat">${esc(x.platforms)}</span>` : ""}</div>
        <p class="ind-card__desc">${t("ind." + x.id + ".desc")}</p>
        <ul class="ind-card__pts"><li>${t("ind.pt.own")}</li><li>${t("ind.pt.whop")}</li></ul>
        ${ready ? `<a class="btn btn--gold ind-card__go" href="${esc(x.url)}" target="_blank" rel="sponsored noopener">${t("ind.go")} ${EXT}</a>`
                : `<button class="btn btn--ghost ind-card__go" type="button" disabled>${t("ind.soon")}</button>`}
        <p class="ind-card__note">${t("ind.note", { n: esc(x.by) })}</p>
      </article>`;
    }).join("");
  }
  root.OTMIndicators = { cards, has: () => !!((root.OTM_CONFIG && root.OTM_CONFIG.INDICATORS) || []).length };
})(window);
