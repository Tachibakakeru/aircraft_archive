"use strict";
/* ═══════════════════════════════════════════════
   全球航空公司 — 獨立於飛行器圖鑑（機型）與機場跑道之外的第三個資料庫
   資料來源：data/airlines.json（手動彙整的概估資料，非即時營運資料）
   ═══════════════════════════════════════════════ */

const $ = id => document.getElementById(id);

let AIRLINES = [];

const FAV_KEY = "hangar_airline_favs";
let FAVS = new Set(JSON.parse(localStorage.getItem(FAV_KEY) || "[]"));
function isFav(id){ return FAVS.has(id); }
function toggleFav(id){
  FAVS.has(id) ? FAVS.delete(id) : FAVS.add(id);
  localStorage.setItem(FAV_KEY, JSON.stringify([...FAVS]));
}

const ALLIANCE_KEYS = ["star", "skyteam", "oneworld", "none"];

(async () => {
  try {
    const res = await fetch("data/airlines.json?v=51");
    if (!res.ok) throw new Error(res.status);
    const data = await res.json();
    AIRLINES = data.airlines;
  } catch {
    $("al-list").innerHTML = "";
    $("al-empty").hidden = false;
    $("al-empty").textContent = "無法載入航空公司資料（data/airlines.json）。";
    return;
  }

  buildAllianceSelect();
  I18N.apply();
  applyAll();

  const wantId = new URLSearchParams(location.search).get("id");
  if (wantId && AIRLINES.some(a => a.id === wantId)) openAirline(wantId);

  $("al-search").addEventListener("input", applyAll);
  $("al-alliance").addEventListener("change", applyAll);
  $("al-fav-only").addEventListener("change", applyAll);
  document.addEventListener("langchange", () => {
    I18N.apply(); buildAllianceSelect(); applyAll();
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
  document.addEventListener("keydown", e => { if (e.key === "Escape") closePanel(); });
  document.addEventListener("click", e => {
    const panel = $("panel");
    if (panel.classList.contains("open") && !panel.contains(e.target) && !e.target.closest(".al-row"))
      closePanel();
  });
})();

function buildAllianceSelect(){
  const sel = $("al-alliance");
  const cur = sel.value;
  sel.innerHTML = `<option value="">${I18N.t("airlines.filter.all")}</option>` +
    ALLIANCE_KEYS.map(k => `<option value="${k}">${I18N.t("airlines.alliance." + k)}</option>`).join("");
  sel.value = cur;
}

function applyAll(){
  const q = $("al-search").value.trim().toLowerCase();
  const alliance = $("al-alliance").value;
  const favOnly = $("al-fav-only").checked;

  const list = AIRLINES.filter(a => {
    if (favOnly && !isFav(a.id)) return false;
    if (alliance && a.alliance !== alliance) return false;
    if (!q) return true;
    const hay = [a.name, a.icao, a.iata, I18N.field(a.country), a.country.zh, ...(a.hubs || [])].filter(Boolean).join(" ").toLowerCase();
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
    return `<div class="al-row" data-id="${a.id}" tabindex="0" role="button">
      <span class="al-alliance-dot ${a.alliance}"></span>
      <span class="al-main">
        <span class="al-name">${a.name}</span>
        <span class="al-loc">${I18N.field(a.country)} · ${I18N.t("airlines.founded")} ${a.founded}</span>
      </span>
      <button class="apt-row-fav${fav ? " on" : ""}" data-fav-id="${a.id}" aria-pressed="${fav}" title="${I18N.t("fleet.fav")}">${fav ? "★" : "☆"}</button>
      <span class="al-codes"><span>${a.icao}</span><span>${a.iata}</span></span>
    </div>`;
  }).join("");

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

function openAirline(id){
  const a = AIRLINES.find(x => x.id === id);
  if (!a) return;
  const panel = $("panel");
  panel.dataset.id = id;
  syncFavButton();

  $("al-p-codes").textContent = [a.icao, a.iata].filter(Boolean).join(" · ");
  $("al-p-name").textContent = a.name;
  $("al-p-sub").textContent = `${I18N.field(a.country)} · ${I18N.t("airlines.founded")} ${a.founded}`;

  const info = $("al-p-info");
  info.innerHTML = "";
  const rows = [
    [I18N.t("airlines.detail.alliance"), I18N.t("airlines.alliance." + a.alliance)],
    [I18N.t("airlines.detail.hubs"), (a.hubs || []).join(" / ") || "—"],
    [I18N.t("airlines.detail.fleetTotal"), a.fleetTotal != null ? `≈ ${a.fleetTotal.toLocaleString()}` : "—"],
  ];
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

  $("al-p-tagline").textContent = I18N.field(a.tagline) || "";

  panel.classList.add("open");
  panel.setAttribute("aria-hidden", "false");
  history.replaceState(null, "", `?id=${encodeURIComponent(id)}`);
}

function closePanel(){
  const panel = $("panel");
  panel.classList.remove("open");
  panel.setAttribute("aria-hidden", "true");
  history.replaceState(null, "", location.pathname);
}
