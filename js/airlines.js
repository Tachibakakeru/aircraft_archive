"use strict";
/* ═══════════════════════════════════════════════
   全球航空公司 — 獨立於飛行器圖鑑（機型）與機場跑道之外的第三個資料庫
   資料來源：data/airlines.json（手動彙整的概估資料，非即時營運資料）
   ═══════════════════════════════════════════════ */

const $ = id => document.getElementById(id);

let AIRLINES = [];
let FULL_DATA = null;
const EDIT_LS_KEY = "hangar_edit_airlines";

// 航線地圖：機場座標由 data/airline_geo.json 提供（離線腳本比對 hubs/routes
// 的自由格式文字與 data/airports.json，非每一筆都能對應到，查不到的公司
// 開啟航線地圖時就沒有弧線，見 meta.note 說明）。
let AIRLINE_GEO = {};
let globeMode = false;

const FAV_KEY = "hangar_airline_favs";
let FAVS = new Set(JSON.parse(localStorage.getItem(FAV_KEY) || "[]"));
function isFav(id){ return FAVS.has(id); }
function toggleFav(id){
  FAVS.has(id) ? FAVS.delete(id) : FAVS.add(id);
  localStorage.setItem(FAV_KEY, JSON.stringify([...FAVS]));
}

/* ── 加入比較（最多 4 家，就地開全頁彈窗比較，沿用機場比較頁同一套 CSS） ── */
const CMP_KEY = "hangar_airline_compare";
let CMP_LIST = JSON.parse(localStorage.getItem(CMP_KEY) || "[]");
function isInCompare(id){ return CMP_LIST.includes(id); }
function toggleCompare(id){
  if (CMP_LIST.includes(id)) CMP_LIST = CMP_LIST.filter(x => x !== id);
  else if (CMP_LIST.length < 4) CMP_LIST.push(id);
  else { alert("最多同時比較 4 家航空公司，請先移除一家再加入。"); return; }
  localStorage.setItem(CMP_KEY, JSON.stringify(CMP_LIST));
  renderCompareTray();
  if (!$("al-cmp-modal").hidden) renderAlCmpPickers();
}
function renderCompareTray(){
  const tray = $("al-cmp-tray");
  tray.hidden = !CMP_LIST.length;
  if (!CMP_LIST.length) return;
  $("al-cmp-chips").innerHTML = CMP_LIST.map(id => {
    const a = AIRLINES.find(x => x.id === id);
    return `<span class="apt-cmp-chip">${a ? (a.icao || a.iata || a.id) : id}<button data-id="${id}" title="移除">✕</button></span>`;
  }).join("");
  $("al-cmp-chips").querySelectorAll("button").forEach(b =>
    b.addEventListener("click", () => toggleCompare(b.dataset.id)));
}

function openAlCmpModal(){
  $("al-cmp-modal").hidden = false;
  renderAlCmpPickers();
}
function closeAlCmpModal(){ $("al-cmp-modal").hidden = true; }

function renderAlCmpPickers(){
  const wrap = $("al-cmp-pickers");
  wrap.innerHTML = "";
  CMP_LIST.forEach((id, i) => {
    const meta = AIRLINES.find(a => a.id === id);
    const box = document.createElement("div");
    box.className = "apt-cmp-picker";
    box.innerHTML = `
      <input type="text" class="apt-cmp-search" value="${meta ? meta.name.replace(/"/g, "&quot;") : ""}"
        placeholder="${I18N.t("airlines.compare.search")}" autocomplete="off">
      <div class="apt-cmp-suggest" hidden></div>`;
    const input = box.querySelector(".apt-cmp-search");
    const suggest = box.querySelector(".apt-cmp-suggest");
    input.addEventListener("input", () => {
      const q = input.value.trim().toLowerCase();
      if (!q){ suggest.hidden = true; return; }
      const matches = AIRLINES
        .filter(a =>
          a.name.toLowerCase().includes(q) ||
          (a.nameZh && a.nameZh.includes(q)) ||
          (a.icao && a.icao.toLowerCase().includes(q)) ||
          (a.iata && a.iata.toLowerCase().includes(q)))
        .slice(0, 8);
      if (!matches.length){ suggest.hidden = true; return; }
      suggest.innerHTML = matches.map(a =>
        `<div class="apt-cmp-opt" data-id="${a.id}">
          <span class="apt-cmp-opt-name">${a.name}</span>
          <span class="apt-cmp-opt-code">${[a.icao, a.iata].filter(Boolean).join(" · ")}</span>
        </div>`).join("");
      suggest.hidden = false;
    });
    suggest.addEventListener("mousedown", async e => {
      const opt = e.target.closest(".apt-cmp-opt");
      if (!opt) return;
      CMP_LIST[i] = opt.dataset.id;
      localStorage.setItem(CMP_KEY, JSON.stringify(CMP_LIST));
      suggest.hidden = true;
      renderCompareTray(); renderAlCmpPickers();
    });
    input.addEventListener("blur", () => setTimeout(() => { suggest.hidden = true; }, 150));
    wrap.appendChild(box);
  });
  if (CMP_LIST.length < 4){
    const add = document.createElement("button");
    add.className = "cmp-add";
    add.textContent = I18N.t("compare.apt.add");
    add.addEventListener("click", () => {
      CMP_LIST.push("");
      renderAlCmpPickers();
      const inputs = wrap.querySelectorAll(".apt-cmp-search");
      inputs[inputs.length - 1].focus();
    });
    wrap.appendChild(add);
  }
  renderAlCmpTable();
}

function renderAlCmpTable(){
  const table = $("al-cmp-table");
  const ids = CMP_LIST.filter(Boolean);
  if (!ids.length){ table.innerHTML = ""; return; }
  const metaOf = {};
  ids.forEach(id => { metaOf[id] = AIRLINES.find(a => a.id === id); });

  let html = "<thead><tr><th></th>";
  ids.forEach(id => {
    const m = metaOf[id];
    html += `<th><div class="craft-head">
      <h2>${m.name}</h2>
      <div class="mfr">${[m.icao, m.iata].filter(Boolean).join(" · ") || "—"}</div>
      <div><button class="remove" data-id="${id}">${I18N.t("compare.remove")}</button></div>
    </div></th>`;
  });
  html += "</tr></thead><tbody>";

  html += catBlockAlCmp(I18N.t("compare.basic"), [
    [I18N.t("airlines.compare.country"), id => I18N.field(metaOf[id].country)],
    [I18N.t("airlines.founded"), id => metaOf[id].founded],
    [I18N.t("airlines.compare.tier"), id => metaOf[id].tier ? I18N.t("airlines.tier." + metaOf[id].tier) : null],
    [I18N.t("airlines.detail.alliance"), id => I18N.t("airlines.alliance." + metaOf[id].alliance)],
  ], ids);

  html += catBlockAlCmp(I18N.t("airlines.detail.fleet"), [
    [I18N.t("airlines.detail.fleetTotal"), id => metaOf[id].fleetTotal != null ? `≈ ${metaOf[id].fleetTotal.toLocaleString()}` : null],
    [I18N.t("airlines.compare.fleetTypes"), id => (metaOf[id].fleet || []).length || null],
    [I18N.t("airlines.compare.mainType"), id => {
      const fleet = metaOf[id].fleet || [];
      if (!fleet.length) return null;
      return fleet.slice().sort((a, b) => b.count - a.count)[0].type;
    }],
  ], ids);

  html += catBlockAlCmp(I18N.t("airlines.detail.hubs"), [
    [I18N.t("airlines.compare.hubCount"), id => (metaOf[id].hubs || []).length || null],
    [I18N.t("airlines.detail.hubs"), id => (metaOf[id].hubs || []).join(" / ") || null],
    [I18N.t("airlines.detail.routes"), id => (metaOf[id].routes || []).length || null],
  ], ids);

  html += "</tbody>";
  table.innerHTML = html;

  table.querySelectorAll(".remove").forEach(btn => {
    btn.addEventListener("click", () => {
      CMP_LIST = CMP_LIST.filter(x => x !== btn.dataset.id);
      localStorage.setItem(CMP_KEY, JSON.stringify(CMP_LIST));
      renderCompareTray(); renderAlCmpPickers();
      if (!CMP_LIST.length) closeAlCmpModal();
    });
  });
}

function catBlockAlCmp(catName, rows, ids){
  let rowsHtml = "";
  rows.forEach(([label, getter]) => {
    const vals = ids.map(getter);
    const strVals = vals.map(v => v == null ? null : String(v));
    const allSame = strVals.every(v => v === strVals[0]);
    rowsHtml += `<tr><td class="label-cell">${label}</td>`;
    strVals.forEach(v => {
      if (v == null) rowsHtml += `<td class="val na">—</td>`;
      else rowsHtml += `<td class="val${!allSame ? " diff" : ""}">${v}</td>`;
    });
    rowsHtml += "</tr>";
  });
  if (!rowsHtml) return "";
  return `<tr class="cat-row"><td colspan="${ids.length + 1}">${catName}</td></tr>${rowsHtml}`;
}

const ALLIANCE_KEYS = ["star", "skyteam", "oneworld", "none"];
const TIER_KEYS = ["mainline", "regional", "lcc"];

// 尾翼 logo 來源：Jxck-S/airline-logos（README 明載 Fair Use，供辨識用途，
// 非商業性彙整）。少數查不到圖或圖片本身載入失敗時，退回用代號決定顏色的
// 徽章，至少每家都有自己專屬、穩定不變的識別色塊。
const LOGO_BASE = "https://raw.githubusercontent.com/Jxck-S/airline-logos/main/";
function logoColor(id){
  let hash = 0;
  for (let i = 0; i < id.length; i++) hash = (hash * 31 + id.charCodeAt(i)) >>> 0;
  return `hsl(${hash % 360}, 60%, 42%)`;
}
function makeBadgeEl(a, big){
  const span = document.createElement("span");
  span.className = big ? "al-logo al-logo-big" : "al-logo";
  span.textContent = a.iata || a.icao || a.name.slice(0, 2).toUpperCase();
  span.style.background = logoColor(a.id);
  return span;
}
function makeLogoEl(a, big){
  if (!(a.customLogo || (a.icao && a.logoSrc))) return makeBadgeEl(a, big);
  const img = document.createElement("img");
  img.className = big ? "al-logo-img al-logo-img-big" : "al-logo-img";
  img.src = a.customLogo || `${LOGO_BASE}${a.logoSrc}/${a.icao}.png`;
  img.alt = a.name;
  img.loading = "lazy";
  img.addEventListener("error", () => img.replaceWith(makeBadgeEl(a, big)), { once: true });
  return img;
}

(async () => {
  const local = localStorage.getItem(EDIT_LS_KEY);
  if (local){
    try { FULL_DATA = JSON.parse(local); } catch { FULL_DATA = null; }
  }
  if (!FULL_DATA){
    try {
      const res = await fetch("data/airlines.json?v=76");
      if (!res.ok) throw new Error(res.status);
      FULL_DATA = await res.json();
    } catch {
      $("al-list").innerHTML = "";
      $("al-empty").hidden = false;
      $("al-empty").textContent = "無法載入航空公司資料（data/airlines.json）。";
      return;
    }
  }
  AIRLINES = FULL_DATA.airlines;
  try {
    const geoRes = await fetch("data/airline_geo.json?v=76");
    if (geoRes.ok) AIRLINE_GEO = await geoRes.json();
  } catch { /* 航線地圖為附加功能，載入失敗不影響主要頁面 */ }

  buildAllianceSelect();
  buildTierSelect();
  I18N.apply();
  applyAll();

  const wantId = new URLSearchParams(location.search).get("id");
  if (wantId && AIRLINES.some(a => a.id === wantId)) openAirline(wantId);

  $("al-search").addEventListener("input", applyAll);
  $("al-alliance").addEventListener("change", applyAll);
  $("al-tier").addEventListener("change", applyAll);
  $("al-fav-only").addEventListener("change", applyAll);
  document.addEventListener("langchange", () => {
    I18N.apply(); buildAllianceSelect(); buildTierSelect(); applyAll();
    const panel = $("panel");
    if (panel.classList.contains("open") && panel.dataset.id) openAirline(panel.dataset.id);
  });

  I18N.mountSelector($("btn-lang"));
  $("btn-theme").addEventListener("click", () => window.HangarTheme.toggle());
  $("al-p-close").addEventListener("click", closePanel);
  $("al-p-fav").addEventListener("click", () => {
    const id = $("panel").dataset.id;
    if (!id) return;
    toggleFav(id);
    syncFavButton();
    applyAll();
  });
  $("al-p-cmp").addEventListener("click", () => {
    const id = $("panel").dataset.id;
    if (!id) return;
    toggleCompare(id);
    syncCmpButton();
    applyAll();
  });
  renderCompareTray();
  $("al-cmp-open").addEventListener("click", openAlCmpModal);
  $("al-cmp-go").addEventListener("click", openAlCmpModal);
  $("al-cmp-modal-close").addEventListener("click", closeAlCmpModal);
  document.addEventListener("keydown", e => { if (e.key === "Escape") closePanel(); });
  document.addEventListener("click", e => {
    const panel = $("panel");
    if (panel.classList.contains("open") && !panel.contains(e.target) && !e.target.closest(".al-row") && !e.target.closest(".auth-gate"))
      closePanel();
  });

  $("al-p-edit").addEventListener("click", async () => {
    const id = $("panel").dataset.id;
    if (!id) return;
    await requireAuth();
    openEditor(id);
  });
  wireEditForm();

  $("al-view-toggle").addEventListener("click", toggleGlobeMode);
  $("al-globe-reset").addEventListener("click", () => AptGlobe.resetView());
  $("al-globe-rotate").addEventListener("click", () => {
    const on = AptGlobe.toggleAutoRotate();
    $("al-globe-rotate").setAttribute("aria-pressed", String(on));
  });
})();

async function toggleGlobeMode(){
  globeMode = !globeMode;
  $("al-view-toggle").classList.toggle("active", globeMode);
  $("al-globe-wrap").hidden = !globeMode;
  if (!globeMode) return;
  if (!AptGlobe.isReady()){
    await AptGlobe.init($("al-globe-wrap"), () => {},
      on => $("al-globe-rotate").setAttribute("aria-pressed", String(on)));
  } else {
    AptGlobe.resize();
  }
  refreshHubMarkers();
  const panel = $("panel");
  if (panel.classList.contains("open") && panel.dataset.id) showAirlineRoutes(panel.dataset.id);
}

// 地球上顯示所有「查得到座標」的航空公司樞紐機場——每座機場一個點，
// 不分屬哪家公司；點選左側清單的航空公司時，另外用 setRoutes() 疊上
// 該公司專屬的航線弧線（見 showAirlineRoutes）。
function refreshHubMarkers(){
  const seen = new Map();
  Object.values(AIRLINE_GEO).forEach(g => {
    (g.hubs || []).forEach(h => { if (!seen.has(h.icao)) seen.set(h.icao, h); });
  });
  const points = [...seen.values()].map(h => ({ id: h.icao, lat: h.lat, lon: h.lon, code: h.icao, type: "large_airport" }));
  AptGlobe.setMarkers(points);
}

function showAirlineRoutes(id){
  if (!globeMode || !AptGlobe.isReady()) return;
  const geo = AIRLINE_GEO[id];
  if (!geo || !geo.hubs.length){ AptGlobe.setRoutes([]); return; }
  const arcs = [];
  geo.hubs.forEach(hub => {
    (geo.routes || []).forEach(r => {
      arcs.push({ fromLat: hub.lat, fromLon: hub.lon, toLat: r.lat, toLon: r.lon });
    });
  });
  AptGlobe.setRoutes(arcs);
  AptGlobe.focusOn(geo.hubs[0].lat, geo.hubs[0].lon);
}

function buildAllianceSelect(){
  const sel = $("al-alliance");
  const cur = sel.value;
  sel.innerHTML = `<option value="">${I18N.t("airlines.filter.all")}</option>` +
    ALLIANCE_KEYS.map(k => `<option value="${k}">${I18N.t("airlines.alliance." + k)}</option>`).join("");
  sel.value = cur;
}

function buildTierSelect(){
  const sel = $("al-tier");
  const cur = sel.value;
  sel.innerHTML = `<option value="">${I18N.t("airlines.filter.allTiers")}</option>` +
    TIER_KEYS.map(k => `<option value="${k}">${I18N.t("airlines.tier." + k)}</option>`).join("");
  sel.value = cur;
}

function applyAll(){
  const q = $("al-search").value.trim().toLowerCase();
  const alliance = $("al-alliance").value;
  const tier = $("al-tier").value;
  const favOnly = $("al-fav-only").checked;

  const list = AIRLINES.filter(a => {
    if (favOnly && !isFav(a.id)) return false;
    if (alliance && a.alliance !== alliance) return false;
    if (tier && a.tier !== tier) return false;
    if (!q) return true;
    const hay = [a.name, a.nameZh, a.icao, a.iata, I18N.field(a.country), a.country.zh, ...(a.hubs || [])].filter(Boolean).join(" ").toLowerCase();
    return hay.includes(q);
  }).sort((a, b) => (isFav(b.id) ? 1 : 0) - (isFav(a.id) ? 1 : 0) || a.name.localeCompare(b.name));

  render(list);
}

function render(list){
  const listEl = $("al-list"), emptyEl = $("al-empty"), countEl = $("al-count");
  countEl.innerHTML = `${I18N.t("airlines.count")} <b>${list.length}</b> / ${AIRLINES.length}`;
  if (!list.length){
    listEl.innerHTML = "";
    emptyEl.hidden = false;
    return;
  }
  emptyEl.hidden = true;

  listEl.innerHTML = list.map(a => {
    const fav = isFav(a.id);
    const cmp = isInCompare(a.id);
    const tierTag = a.tier ? `<span class="al-tier-tag al-tier-${a.tier}">${I18N.t("airlines.tier." + a.tier)}</span>` : "";
    const founded = a.founded ? ` · ${I18N.t("airlines.founded")} ${a.founded}` : "";
    const nameZh = (a.nameZh && I18N.get() === "zh") ? ` <span class="al-name-zh">${a.nameZh}</span>` : "";
    return `<div class="al-row" data-id="${a.id}" tabindex="0" role="button">
      <span class="al-logo-slot"></span>
      <span class="al-alliance-dot ${a.alliance}"></span>
      <span class="al-main">
        <span class="al-name">${a.name}${nameZh}</span>
        ${tierTag}
        <span class="al-loc">${I18N.field(a.country)}${founded}</span>
      </span>
      <button class="apt-row-cmp${cmp ? " on" : ""}" data-cmp-id="${a.id}" aria-pressed="${cmp}" title="${I18N.t("airports.detail.addCompare")}">⇄</button>
      <button class="apt-row-fav${fav ? " on" : ""}" data-fav-id="${a.id}" aria-pressed="${fav}" title="${I18N.t("fleet.fav")}">${fav ? "★" : "☆"}</button>
      <span class="al-codes"><span>${a.icao || ""}</span><span>${a.iata || ""}</span></span>
    </div>`;
  }).join("");

  listEl.querySelectorAll(".al-row").forEach((row, i) => {
    row.querySelector(".al-logo-slot").replaceWith(makeLogoEl(list[i]));
  });
  listEl.querySelectorAll(".apt-row-cmp").forEach(btn =>
    btn.addEventListener("click", e => {
      e.stopPropagation();
      toggleCompare(btn.dataset.cmpId);
      applyAll();
    }));
  listEl.querySelectorAll(".al-row").forEach(row => {
    row.addEventListener("click", e => {
      if (e.target.closest(".apt-row-fav")) return;
      openAirline(row.dataset.id);
    });
    row.addEventListener("keydown", e => {
      if (e.key === "Enter" || e.key === " "){ e.preventDefault(); openAirline(row.dataset.id); }
    });
  });
  listEl.querySelectorAll(".apt-row-fav").forEach(btn =>
    btn.addEventListener("click", e => {
      e.stopPropagation();
      toggleFav(btn.dataset.favId);
      applyAll();
    }));
}

function syncFavButton(){
  const id = $("panel").dataset.id;
  const on = id && isFav(id);
  const btn = $("al-p-fav");
  btn.classList.toggle("on", !!on);
  btn.setAttribute("aria-pressed", String(!!on));
  btn.textContent = on ? "★" : "☆";
}

function syncCmpButton(){
  const id = $("panel").dataset.id;
  const on = id && isInCompare(id);
  const btn = $("al-p-cmp");
  btn.classList.toggle("on", !!on);
  btn.setAttribute("aria-pressed", String(!!on));
}

function escHTML(s){
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// 樞紐機場：查得到對應機場座標時（見 data/airline_geo.json）連結到機場頁，
// 查不到就純文字顯示——不是每筆都保證能對應到，見 meta.note 說明。
function hubsHTML(a){
  if (!a.hubs || !a.hubs.length) return "—";
  const geo = AIRLINE_GEO[a.id];
  const byText = new Map((geo && geo.hubs || []).map(h => [h.text, h.icao]));
  return a.hubs.map(h => {
    const icao = byText.get(h);
    return icao
      ? `<a class="al-hub-link" href="airports.html?icao=${encodeURIComponent(icao)}">${escHTML(h)}</a>`
      : escHTML(h);
  }).join(" / ");
}

function openAirline(id){
  const a = AIRLINES.find(x => x.id === id);
  if (!a) return;
  const panel = $("panel");
  panel.dataset.id = id;
  syncFavButton();
  syncCmpButton();
  $("al-edit").hidden = true;

  const photo = $("al-p-photo");
  if (a.photo){ photo.src = a.photo; photo.hidden = false; }
  else photo.hidden = true;

  $("al-p-logo").replaceWith(Object.assign(makeLogoEl(a, true), { id: "al-p-logo" }));
  $("al-p-codes").textContent = [a.icao, a.iata].filter(Boolean).join(" · ");
  $("al-p-name").textContent = (a.nameZh && I18N.get() === "zh") ? `${a.name}（${a.nameZh}）` : a.name;
  $("al-p-sub").textContent = a.founded
    ? `${I18N.field(a.country)} · ${I18N.t("airlines.founded")} ${a.founded}`
    : I18N.field(a.country);
  if (a.tier){
    $("al-p-tier").textContent = I18N.t("airlines.tier." + a.tier);
    $("al-p-tier").className = "al-tier-tag al-tier-" + a.tier;
    $("al-p-tier").hidden = false;
  } else {
    $("al-p-tier").hidden = true;
  }

  const info = $("al-p-info");
  info.innerHTML = "";
  const rows = [
    [I18N.t("airlines.detail.alliance"), I18N.t("airlines.alliance." + a.alliance)],
    [I18N.t("airlines.detail.fleetTotal"), a.fleetTotal != null ? `≈ ${a.fleetTotal.toLocaleString()}` : "—"],
  ];
  const hubRow = document.createElement("div"); hubRow.className = "spec-row";
  const hubDt = document.createElement("dt"); hubDt.textContent = I18N.t("airlines.detail.hubs");
  const hubDd = document.createElement("dd"); hubDd.innerHTML = hubsHTML(a);
  hubRow.append(hubDt, hubDd); info.appendChild(hubRow);
  rows.forEach(([k, v]) => {
    const row = document.createElement("div"); row.className = "spec-row";
    const dt = document.createElement("dt"); dt.textContent = k;
    const dd = document.createElement("dd"); dd.textContent = v;
    row.append(dt, dd); info.appendChild(row);
  });

  $("al-p-fleet").innerHTML = (a.fleet || []).map(f => `
    <div class="al-fleet-row">
      <span class="al-fleet-type">${f.type}</span>
      <span class="al-fleet-count">×${f.count.toLocaleString()}</span>
      ${f.fleetId ? `<a class="al-fleet-3d" href="viewer.html?model=${encodeURIComponent(f.fleetId)}">🔗 3D</a>` : ""}
    </div>`).join("") || `<div class="al-empty-inline">—</div>`;

  $("al-p-routes").innerHTML = (a.routes || []).map(r => `<span class="al-route-chip">${r}</span>`).join("");

  $("al-p-tagline").textContent = I18N.field(a.tagline) || I18N.t("airlines.detail.noData");

  panel.classList.add("open");
  panel.setAttribute("aria-hidden", "false");
  history.replaceState(null, "", `?id=${encodeURIComponent(id)}`);
  showAirlineRoutes(id);
}

function closePanel(){
  const panel = $("panel");
  panel.classList.remove("open");
  panel.setAttribute("aria-hidden", "true");
  history.replaceState(null, "", location.pathname);
  if (globeMode && typeof AptGlobe !== "undefined" && AptGlobe.isReady()) AptGlobe.setRoutes([]);
}

// ── 編輯功能：僅本機暫存，需通過密碼驗證後點「儲存到網站」才會公開 ──
const EDIT_FIELD_IDS = [
  "al-e-name", "al-e-namezh", "al-e-icao", "al-e-iata", "al-e-founded", "al-e-alliance", "al-e-tier",
  "al-e-country-zh", "al-e-country-en", "al-e-country-ja", "al-e-hubs", "al-e-fleettotal",
  "al-e-fleet", "al-e-routes", "al-e-tagline-zh", "al-e-tagline-en", "al-e-tagline-ja",
  "al-e-customlogo", "al-e-photo",
];

function openEditor(id){
  const a = AIRLINES.find(x => x.id === id);
  if (!a) return;
  $("al-e-name").value = a.name || "";
  $("al-e-namezh").value = a.nameZh || "";
  $("al-e-icao").value = a.icao || "";
  $("al-e-iata").value = a.iata || "";
  $("al-e-founded").value = a.founded != null ? a.founded : "";
  $("al-e-alliance").value = a.alliance || "none";
  $("al-e-tier").value = a.tier || "";
  $("al-e-country-zh").value = (a.country && a.country.zh) || "";
  $("al-e-country-en").value = (a.country && a.country.en) || "";
  $("al-e-country-ja").value = (a.country && a.country.ja) || "";
  $("al-e-hubs").value = (a.hubs || []).join(", ");
  $("al-e-fleettotal").value = a.fleetTotal != null ? a.fleetTotal : "";
  $("al-e-fleet").value = (a.fleet || []).map(f => [f.type, f.count, f.fleetId || ""].join("：")).join("\n");
  $("al-e-routes").value = (a.routes || []).join(", ");
  $("al-e-tagline-zh").value = (a.tagline && a.tagline.zh) || "";
  $("al-e-tagline-en").value = (a.tagline && a.tagline.en) || "";
  $("al-e-tagline-ja").value = (a.tagline && a.tagline.ja) || "";
  $("al-e-customlogo").value = a.customLogo || "";
  $("al-e-photo").value = a.photo || "";
  $("al-edit").hidden = false;
  $("al-edit").scrollIntoView({ block: "nearest" });
}

function currentEditTarget(){
  const id = $("panel").dataset.id;
  return AIRLINES.find(x => x.id === id);
}

function applyEditForm(a){
  a.name = $("al-e-name").value.trim() || a.name;
  const nameZh = $("al-e-namezh").value.trim();
  if (nameZh) a.nameZh = nameZh; else delete a.nameZh;
  a.icao = $("al-e-icao").value.trim().toUpperCase() || null;
  a.iata = $("al-e-iata").value.trim().toUpperCase() || null;
  const founded = parseInt($("al-e-founded").value, 10);
  a.founded = Number.isFinite(founded) ? founded : null;
  a.alliance = $("al-e-alliance").value;
  a.tier = $("al-e-tier").value || null;
  a.country = {
    zh: $("al-e-country-zh").value.trim(),
    en: $("al-e-country-en").value.trim(),
    ja: $("al-e-country-ja").value.trim(),
  };
  a.hubs = $("al-e-hubs").value.split(",").map(s => s.trim()).filter(Boolean);
  const fleetTotal = parseInt($("al-e-fleettotal").value, 10);
  a.fleetTotal = Number.isFinite(fleetTotal) ? fleetTotal : null;
  a.fleet = $("al-e-fleet").value.split("\n").map(line => {
    const parts = line.split("：").map(s => s.trim());
    if (!parts[0] || !parts[1]) return null;
    const count = parseInt(parts[1], 10);
    if (!Number.isFinite(count)) return null;
    return { type: parts[0], count, ...(parts[2] ? { fleetId: parts[2] } : {}) };
  }).filter(Boolean);
  a.routes = $("al-e-routes").value.split(",").map(s => s.trim()).filter(Boolean);
  a.tagline = {
    zh: $("al-e-tagline-zh").value.trim(),
    en: $("al-e-tagline-en").value.trim(),
    ja: $("al-e-tagline-ja").value.trim(),
  };
  const customLogo = $("al-e-customlogo").value.trim();
  if (customLogo) a.customLogo = customLogo; else delete a.customLogo;
  const photo = $("al-e-photo").value.trim();
  if (photo) a.photo = photo; else delete a.photo;
}

function persistDraft(){
  try { localStorage.setItem(EDIT_LS_KEY, JSON.stringify(FULL_DATA)); }
  catch { toast("暫存失敗：資料可能過大"); }
}

function wireEditForm(){
  EDIT_FIELD_IDS.forEach(id => {
    $(id).addEventListener("input", () => {
      const a = currentEditTarget();
      if (!a) return;
      applyEditForm(a);
      persistDraft();
      openAirline(a.id);
      $("al-edit").hidden = false;
    });
  });

  $("al-e-photo-file").addEventListener("change", async e => {
    const a = currentEditTarget();
    const file = e.target.files[0];
    if (!a || !file) return;
    $("al-e-photo").value = await downscale(file, 1400, 0.82);
    applyEditForm(a);
    persistDraft();
    openAirline(a.id);
    $("al-edit").hidden = false;
    e.target.value = "";
  });

  $("al-edit-save").addEventListener("click", async () => {
    const btn = $("al-edit-save");
    const original = btn.textContent;
    btn.disabled = true;
    btn.textContent = "儲存中…";
    try {
      const result = await Storage.save("airlines", FULL_DATA);
      toast(result.message);
      if (result.ok && result.pushed) localStorage.removeItem(EDIT_LS_KEY);
      applyAll();
    } catch (e){
      toast("儲存失敗：" + e.message);
    } finally {
      btn.disabled = false;
      btn.textContent = original;
    }
  });

  $("al-edit-clear").addEventListener("click", () => {
    if (!confirm("確定清除所有航空公司的本機暫存編輯？將還原成網站原始資料。")) return;
    localStorage.removeItem(EDIT_LS_KEY);
    location.reload();
  });
}

// 上傳圖片壓縮，避免 JSON 過大（與 editor.js 同一手法）
function downscale(file, maxW, quality){
  return new Promise(resolve => {
    const img = new Image();
    img.onload = () => {
      const scale = Math.min(1, maxW / img.width);
      const c = document.createElement("canvas");
      c.width = Math.round(img.width * scale);
      c.height = Math.round(img.height * scale);
      c.getContext("2d").drawImage(img, 0, 0, c.width, c.height);
      resolve(c.toDataURL("image/jpeg", quality));
    };
    img.onerror = () => resolve("");
    img.src = URL.createObjectURL(file);
  });
}

let toastTimer = null;
function toast(msg){
  let t = document.querySelector(".toast");
  if (!t){ t = document.createElement("div"); t.className = "toast"; document.body.appendChild(t); }
  t.textContent = msg;
  t.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove("show"), 2200);
}
