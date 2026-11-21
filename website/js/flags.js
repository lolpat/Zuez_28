// Country flags for the leaderboard. Flag images: assets/flags (flag-icons, MIT licence, see LICENSE.txt there).
// Country names come from the browser (Intl.DisplayNames), in the page language.
(function (root) {
  const CODES = "AD AE AF AG AI AL AM AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BJ BL BM BN BO BQ BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CP CR CU CV CW CX CY CZ DE DG DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT HU IC ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RE RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR SS ST SV SX SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI VN VU WF WS XK YE YT ZA ZM ZW".split(" ");
  const ok = (c) => typeof c === "string" && CODES.includes(c.toUpperCase());
  const name = (c, lang) => {
    try { return new Intl.DisplayNames([lang === "th" ? "th" : "en"], { type: "region" }).of(c.toUpperCase()); } catch (e) { return c; }
  };
  // a flag image, or "" when no country is set
  const img = (c, lang, cls = "flag") => ok(c)
    ? '<img class="' + cls + '" src="assets/flags/' + c.toLowerCase() + '.svg" alt="' + String(name(c, lang)).replace(/"/g, "") + '" title="' + String(name(c, lang)).replace(/"/g, "") + '" width="24" height="18" loading="lazy" decoding="async">'
    : "";
  // <option>s sorted by name, with the most common countries for this community first
  const TOP = ["TH", "LA", "MM", "KH", "MY", "SG", "VN", "NO"];
  const options = (sel, lang, noneLabel) => {
    const byName = CODES.filter((c) => !TOP.includes(c)).map((c) => [c, name(c, lang)]).filter(([c, n]) => n && n !== c)
      .sort((a, b) => a[1].localeCompare(b[1], lang === "th" ? "th" : "en"));
    const o = ([c, n]) => '<option value="' + c + '"' + (sel === c ? " selected" : "") + ">" + n + "</option>";
    return '<option value="">' + noneLabel + "</option>" + TOP.map((c) => o([c, name(c, lang)])).join("") + '<option disabled>──────────</option>' + byName.map(o).join("");
  };
  // a flag that fails to load is removed, so the initials underneath show instead
  document.addEventListener("error", (e) => { const el = e.target; if (el && el.classList && (el.classList.contains("lb-flag") || el.classList.contains("pod__flag"))) el.remove(); }, true);
  root.OTMFlags = { CODES, ok, name, img, options };
})(window);
