"use strict";
/* ═══════════════════════════════════════════════
   機場與跑道 — 搜尋、篩選、跑道明細（依需求載入）
   資料來源：OurAirports（Public Domain），見 tools/build_airports.py
   ═══════════════════════════════════════════════ */

const $ = id => document.getElementById(id);
const MAX_RESULTS = 200;

let AIRPORTS = [];
let COUNTRIES = {};
const runwayCache = {};   // country code → { ident: [runway,...] }

(async () => {
  try {
    const [aRes, cRes] = await Promise.all([
      fetch("data/airports.json?v=23"),
      fetch("data/countries.json?v=23"),
    ]);
    const aData = await aRes.json();
    COUNTRIES = await cRes.json();
    AIRPORTS = aData.airports;
  } catch {
    $("apt-list").innerHTML = "";
    $("apt-empty").hidden = false;
    $("apt-empty").textContent = "無法載入機場資料（data/airports.json）。";
    return;
  }

  buildCountrySelect();
  buildTypeSelect();
  I18N.apply();
  applyAll();

  // 深連結：?icao=XXXX 直接開啟
  const wantId = new URLSearchParams(location.search).get("icao");
  if (wantId && AIRPORTS.some(a => a.id === wantId)) openAirport(wantId);

  $("apt-search").addEventListener("input", applyAll);
  $("apt-country").addEventListener("change", applyAll);
  $("apt-type").addEventListener("change", applyAll);
  document.addEventListener("langchange", () => { I18N.apply(); applyAll(); });

  I18N.mountSelector($("btn-lang"));
  $("btn-theme").addEventListener("click", () => window.HangarTheme.toggle());
  $("apt-p-close").addEventListener("click", closePanel);
  document.addEventListener("keydown", e => { if (e.key === "Escape") closePanel(); });
  document.addEventListener("click", e => {
    const panel = $("panel");
    if (panel.classList.contains("open") && !panel.contains(e.target) && !e.target.closest(".apt-row"))
      closePanel();
  });
})();

function countryName(code){ return (COUNTRIES[code] || code || "—"); }

function buildCountrySelect(){
  const counts = {};
  AIRPORTS.forEach(a => { if (a.country) counts[a.country] = (counts[a.country] || 0) + 1; });
  const codes = Object.keys(counts).sort((a, b) => countryName(a).localeCompare(countryName(b)));
  const sel = $("apt-country");
  sel.innerHTML = `<option value="">${I18N.t("airports.filter.allCountries")}</option>` +
    codes.map(c => `<option value="${c}">${countryName(c)} (${counts[c]})</option>`).join("");
}

function buildTypeSelect(){
  const sel = $("apt-type");
  const types = ["large_airport", "medium_airport", "small_airport", "seaplane_base", "heliport"];
  sel.innerHTML = `<option value="">${I18N.t("airports.filter.allTypes")}</option>` +
    types.map(t => `<option value="${t}">${I18N.t("airports.type." + t)}</option>`).join("");
}

function applyAll(){
  const q = $("apt-search").value.trim().toLowerCase();
  const country = $("apt-country").value;
  const type = $("apt-type").value;

  let list;
  if (!q && !country && !type){
    list = null;   // 尚未縮小範圍：不渲染，提示使用者搜尋
  } else {
    list = AIRPORTS.filter(a => {
      if (country && a.country !== country) return false;
      if (type && a.type !== type) return false;
      if (!q) return true;
      const hay = [a.name, a.city, countryName(a.country), a.icao, a.iata].filter(Boolean).join(" ").toLowerCase();
      return hay.includes(q);
    });
  }
  render(list);
}

function render(list){
  const listEl = $("apt-list"), moreEl = $("apt-more"), emptyEl = $("apt-empty"), countEl = $("apt-count");

  if (list === null){
    listEl.innerHTML = ""; moreEl.hidden = true;
    emptyEl.hidden = false; emptyEl.textContent = I18N.t("airports.prompt");
    countEl.textContent = "";
    return;
  }
  if (!list.length){
    listEl.innerHTML = ""; moreEl.hidden = true;
    emptyEl.hidden = false; emptyEl.textContent = I18N.t("airports.empty");
    countEl.textContent = "";
    return;
  }
  emptyEl.hidden = true;
  list.sort((a, b) => a.name.localeCompare(b.name));
  const shown = list.slice(0, MAX_RESULTS);
  countEl.innerHTML = `${I18N.t("airports.count.showing")} <b>${shown.length}</b> / ${list.length}`;

  listEl.innerHTML = shown.map(a => {
    const codes = [a.icao, a.iata].filter(Boolean).map(c => `<span>${c}</span>`).join("");
    const loc = [a.city, countryName(a.country)].filter(Boolean).join(", ");
    return `<button class="apt-row" data-id="${a.id}">
      <span class="apt-type-dot ${a.type}"></span>
      <span class="apt-main">
        <span class="apt-name">${a.name}</span>
        <span class="apt-loc">${loc}</span>
      </span>
      <span class="apt-codes">${codes}</span>
    </button>`;
  }).join("");

  listEl.querySelectorAll(".apt-row").forEach(row =>
    row.addEventListener("click", () => openAirport(row.dataset.id)));

  moreEl.hidden = list.length <= MAX_RESULTS;
  if (!moreEl.hidden) moreEl.textContent = I18N.t("airports.more").replace("{n}", list.length - MAX_RESULTS);
}

async function loadRunways(country){
  if (!country) return {};
  if (runwayCache[country]) return runwayCache[country];
  try {
    const r = await fetch(`data/runways/${encodeURIComponent(country)}.json?v=23`);
    const d = r.ok ? await r.json() : {};
    runwayCache[country] = d;
    return d;
  } catch { return {}; }
}

const M_PER_FT = 0.3048;
const SURF_NAMES = {
  ASP: "瀝青 Asphalt", "ASPH-G": "瀝青 Asphalt", CON: "混凝土 Concrete", TURF: "草地 Turf",
  GRVL: "碎石 Gravel", GRS: "草地 Turf", DIRT: "泥地 Dirt", WATER: "水面 Water", SAND: "沙地 Sand",
};
function surfName(code){
  if (!code) return "—";
  const key = String(code).toUpperCase();
  return SURF_NAMES[key] || code;
}

function compassSVG(le, he){
  const hdg = (le && le.hdg != null) ? le.hdg : (he && he.hdg != null ? (he.hdg + 180) % 360 : null);
  if (hdg == null) return "";
  const cx = 40, cy = 40, r = 30;
  const rad = (hdg - 90) * Math.PI / 180;
  const x1 = cx - Math.cos(rad) * r, y1 = cy - Math.sin(rad) * r;
  const x2 = cx + Math.cos(rad) * r, y2 = cy + Math.sin(rad) * r;
  return `<svg class="rw-compass" viewBox="0 0 80 80">
    <circle class="ring" cx="${cx}" cy="${cy}" r="${r}"/>
    <text class="n-label" x="${cx}" y="8" text-anchor="middle">N</text>
    <line class="strip" x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}"/>
  </svg>`;
}

function runwayCardHTML(rw){
  const idents = [rw.le && rw.le.id, rw.he && rw.he.id].filter(Boolean).join(" / ") || "—";
  const lenM = rw.len != null ? Math.round(rw.len * M_PER_FT) : null;
  const widM = rw.wid != null ? Math.round(rw.wid * M_PER_FT) : null;
  const dims = rw.len != null
    ? `${rw.len} × ${rw.wid || "—"} ft　(${lenM} × ${widM || "—"} m)`
    : I18N.t("airports.detail.nodims");
  return `<div class="rw-card${rw.closed ? " closed" : ""}">
    ${compassSVG(rw.le, rw.he)}
    <div class="rw-head"><span class="rw-idents">${idents}</span><span class="rw-surf">${surfName(rw.surf)}</span></div>
    <div class="rw-dims">${dims}</div>
    <div class="rw-flags">
      <span class="rw-flag${rw.lit ? " on" : ""}">${I18N.t("airports.flag.lit")}</span>
      <span class="rw-flag${rw.closed ? " on" : ""}">${I18N.t("airports.flag.closed")}</span>
    </div>
  </div>`;
}

async function openAirport(id){
  const a = AIRPORTS.find(x => x.id === id);
  if (!a) return;
  const panel = $("panel");
  $("apt-p-type").textContent = I18N.t("airports.type." + a.type) || a.type;
  $("apt-p-name").textContent = a.name;
  $("apt-p-loc").textContent = [a.city, countryName(a.country)].filter(Boolean).join(", ");

  const badges = [a.icao, a.iata].filter(Boolean).map(c => `<span class="apt-badge">${c}</span>`);
  $("apt-p-badges").innerHTML = badges.join("");

  const info = $("apt-p-info");
  info.innerHTML = "";
  const rows = [
    [I18N.t("airports.detail.coords"), (a.lat != null && a.lon != null) ? `${a.lat}, ${a.lon}` : "—"],
    [I18N.t("airports.detail.elevation"), a.elev != null ? `${a.elev} ft (${Math.round(a.elev * M_PER_FT)} m)` : "—"],
    [I18N.t("airports.detail.region"), a.region || "—"],
  ];
  rows.forEach(([k, v]) => {
    const row = document.createElement("div"); row.className = "spec-row";
    const dt = document.createElement("dt"); dt.textContent = k;
    const dd = document.createElement("dd"); dd.textContent = v;
    row.append(dt, dd); info.appendChild(row);
  });

  const rwEl = $("apt-p-runways");
  rwEl.innerHTML = `<div class="apt-empty" style="padding:20px 0">${I18N.t("viewer.loading")}</div>`;
  panel.classList.add("open");
  panel.setAttribute("aria-hidden", "false");

  const byIdent = await loadRunways(a.country);
  const rws = byIdent[a.id] || [];
  rwEl.innerHTML = rws.length
    ? rws.map(runwayCardHTML).join("")
    : `<div class="apt-empty" style="padding:20px 0">${I18N.t("airports.detail.norunways")}</div>`;

  history.replaceState(null, "", `?icao=${encodeURIComponent(id)}`);
}

function closePanel(){
  const panel = $("panel");
  panel.classList.remove("open");
  panel.setAttribute("aria-hidden", "true");
  history.replaceState(null, "", location.pathname);
}
