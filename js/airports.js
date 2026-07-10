"use strict";
/* ═══════════════════════════════════════════════
   機場與跑道 — 搜尋、篩選、機場明細（依國家整批載入）
   資料來源：OurAirports（Public Domain），見 tools/build_airports.py
   全量匯入：85,716 座機場、48,096 條跑道，未篩選類別或代號。
   ═══════════════════════════════════════════════ */

const $ = id => document.getElementById(id);
const MAX_RESULTS = 200;

let AIRPORTS = [];
let COUNTRIES = {};
const detailCache = {};   // country code → { ident: {lat,lon,elev,region,runways} }

const FAV_KEY = "hangar_apt_favs";
let FAVS = new Set(JSON.parse(localStorage.getItem(FAV_KEY) || "[]"));
function isFav(id){ return FAVS.has(id); }
function toggleFav(id){
  FAVS.has(id) ? FAVS.delete(id) : FAVS.add(id);
  localStorage.setItem(FAV_KEY, JSON.stringify([...FAVS]));
}

/* ── 機場備註／照片（本機自訂內容，僅存於使用者瀏覽器） ── */
const NOTES_KEY = "hangar_apt_notes";
function loadNotesStore(){
  try { return JSON.parse(localStorage.getItem(NOTES_KEY) || "{}"); } catch { return {}; }
}
function getNotes(id){
  const n = loadNotesStore()[id];
  return n || { text: "", images: [] };
}
function setNotes(id, notes){
  const store = loadNotesStore();
  if (!notes.text && !(notes.images && notes.images.length)) delete store[id];
  else store[id] = notes;
  localStorage.setItem(NOTES_KEY, JSON.stringify(store));
}
function escapeHTML(s){
  return String(s).replace(/[&<>"']/g, c => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;" }[c]));
}

(async () => {
  try {
    const [aRes, cRes] = await Promise.all([
      fetch("data/airports.json?v=34"),
      fetch("data/countries.json?v=34"),
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
  $("apt-fav-only").addEventListener("change", applyAll);
  document.addEventListener("langchange", () => {
    I18N.apply(); applyAll();
    const panel = $("panel");
    if (panel.classList.contains("open") && panel.dataset.id) openAirport(panel.dataset.id);
  });

  I18N.mountSelector($("btn-lang"));
  $("btn-theme").addEventListener("click", () => window.HangarTheme.toggle());
  $("apt-p-close").addEventListener("click", closePanel);
  $("apt-p-fav").addEventListener("click", () => {
    const id = $("panel").dataset.id;
    if (!id) return;
    toggleFav(id);
    syncFavButton();
    applyAll();
  });
  document.addEventListener("keydown", e => {
    if (!$("sat-lightbox").hidden){ if (e.key === "Escape") closeSatLightbox(); return; }
    if (e.key === "Escape") closePanel();
  });
  document.addEventListener("click", e => {
    if (!$("sat-lightbox").hidden) return;
    const panel = $("panel");
    if (panel.classList.contains("open") && !panel.contains(e.target) && !e.target.closest(".apt-row"))
      closePanel();
  });

  // 衛星縮圖點擊 → 放大檢視（事件委派，涵蓋每次重繪的內容）
  document.addEventListener("click", e => {
    const sat = e.target.closest(".apt-sat");
    if (sat) openSatLightbox(parseFloat(sat.dataset.lat), parseFloat(sat.dataset.lon), parseInt(sat.dataset.zoom, 10));
  });
  $("sat-lb-close").addEventListener("click", e => { e.stopPropagation(); closeSatLightbox(); });
  $("sat-lb-in").addEventListener("click", e => { e.stopPropagation(); satState.zoom = Math.min(19, satState.zoom + 1); renderSatLightbox(); });
  $("sat-lb-out").addEventListener("click", e => { e.stopPropagation(); satState.zoom = Math.max(2, satState.zoom - 1); renderSatLightbox(); });
  $("sat-lightbox").addEventListener("click", e => { e.stopPropagation(); if (e.target.id === "sat-lightbox") closeSatLightbox(); });

  // 機場備註／照片編輯
  $("apt-p-edit").addEventListener("click", () => openNotesEditor($("panel").dataset.id));
  $("apt-p-notes-cancel").addEventListener("click", closeNotesEditor);
  $("apt-p-notes-save").addEventListener("click", () => {
    const id = $("panel").dataset.id;
    if (!id) return;
    const text = $("apt-p-notes-text").value.trim();
    try { setNotes(id, { text, images: editingImages }); }
    catch { alert("儲存失敗，圖片可能過大，建議改用圖片網址。"); return; }
    renderNotesView(id);
    closeNotesEditor();
  });
  $("apt-p-notes-publish").addEventListener("click", async () => {
    const id = $("panel").dataset.id;
    if (!id) return;
    const text = $("apt-p-notes-text").value.trim();
    const notes = { text, images: editingImages };
    if (!text && !notes.images.length){ alert("請先輸入內容再發布。"); return; }
    await requireAuth();   // 需通過與資料編輯器共用的密碼驗證，否則只會存在本機
    const btn = $("apt-p-notes-publish");
    const orig = btn.textContent;
    btn.disabled = true;
    btn.textContent = I18N.t("airports.detail.publishing");
    try {
      setNotes(id, notes);
      const result = await Storage.save("airport-notes/" + id, notes);
      alert(result.message);
      if (result.ok) delete publishedCache[id];
    } finally {
      btn.disabled = false;
      btn.textContent = orig;
    }
    renderNotesView(id);
    closeNotesEditor();
  });
  $("apt-p-notes-imgadd").addEventListener("click", () => {
    const input = $("apt-p-notes-imgurl");
    const url = input.value.trim();
    if (!url) return;
    editingImages.push(url);
    input.value = "";
    renderEditingImages();
  });
  $("apt-p-notes-imgfile").addEventListener("click", () => $("apt-p-notes-file").click());
  $("apt-p-notes-file").addEventListener("change", async e => {
    for (const file of e.target.files){
      const dataUrl = await downscaleImg(file, 1200, 0.8);
      if (dataUrl) editingImages.push(dataUrl);
    }
    renderEditingImages();
    e.target.value = "";
  });
})();

function syncFavButton(){
  const id = $("panel").dataset.id;
  const on = id && isFav(id);
  const btn = $("apt-p-fav");
  btn.classList.toggle("on", !!on);
  btn.setAttribute("aria-pressed", String(!!on));
  btn.textContent = on ? "★" : "☆";
}

function countryName(code){ return (COUNTRIES[code] || code || "—"); }

function buildCountrySelect(){
  const counts = {};
  AIRPORTS.forEach(a => { if (a.country) counts[a.country] = (counts[a.country] || 0) + 1; });
  const codes = Object.keys(counts).sort((a, b) => countryName(a).localeCompare(countryName(b)));
  const sel = $("apt-country");
  sel.innerHTML = `<option value="">${I18N.t("airports.filter.allCountries")}</option>` +
    codes.map(c => `<option value="${c}">${countryName(c)} (${counts[c].toLocaleString()})</option>`).join("");
}

function buildTypeSelect(){
  const sel = $("apt-type");
  const types = ["large_airport", "medium_airport", "small_airport", "seaplane_base", "heliport", "balloonport", "closed"];
  sel.innerHTML = `<option value="">${I18N.t("airports.filter.allTypes")}</option>` +
    types.map(t => `<option value="${t}">${I18N.t("airports.type." + t)}</option>`).join("");
}

function applyAll(){
  const q = $("apt-search").value.trim().toLowerCase();
  const country = $("apt-country").value;
  const type = $("apt-type").value;
  const favOnly = $("apt-fav-only").checked;

  let list;
  if (!q && !country && !type && !favOnly){
    list = null;   // 尚未縮小範圍：不渲染，提示使用者搜尋
  } else {
    list = AIRPORTS.filter(a => {
      if (favOnly && !isFav(a.id)) return false;
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
  list = list.slice().sort((a, b) => (isFav(b.id) ? 1 : 0) - (isFav(a.id) ? 1 : 0) || a.name.localeCompare(b.name));
  const shown = list.slice(0, MAX_RESULTS);
  countEl.innerHTML = `${I18N.t("airports.count.showing")} <b>${shown.length.toLocaleString()}</b> / ${list.length.toLocaleString()}`;

  listEl.innerHTML = shown.map(a => {
    const codes = [a.icao, a.iata].filter(Boolean).map(c => `<span>${c}</span>`).join("");
    const loc = [a.city, countryName(a.country)].filter(Boolean).join(", ");
    const fav = isFav(a.id);
    return `<div class="apt-row${a.type === "closed" ? " closed" : ""}" data-id="${a.id}" tabindex="0" role="button">
      <span class="apt-type-dot ${a.type}"></span>
      <span class="apt-main">
        <span class="apt-name">${a.name}</span>
        <span class="apt-loc">${loc}</span>
      </span>
      <button class="apt-row-fav${fav ? " on" : ""}" data-fav-id="${a.id}" aria-pressed="${fav}" title="${I18N.t("fleet.fav")}">${fav ? "★" : "☆"}</button>
      <span class="apt-codes">${codes}</span>
    </div>`;
  }).join("");

  listEl.querySelectorAll(".apt-row").forEach(row => {
    row.addEventListener("click", e => {
      if (e.target.closest(".apt-row-fav")) return;
      openAirport(row.dataset.id);
    });
    row.addEventListener("keydown", e => {
      if (e.key === "Enter" || e.key === " "){ e.preventDefault(); openAirport(row.dataset.id); }
    });
  });
  listEl.querySelectorAll(".apt-row-fav").forEach(btn =>
    btn.addEventListener("click", e => {
      e.stopPropagation();
      toggleFav(btn.dataset.favId);
      applyAll();
    }));

  moreEl.hidden = list.length <= MAX_RESULTS;
  if (!moreEl.hidden) moreEl.textContent = I18N.t("airports.more").replace("{n}", (list.length - MAX_RESULTS).toLocaleString());
}

// 每個國家的機場明細（座標／標高／行政區碼／跑道清單）合併成一檔，
// 點開該國第一座機場時整批載入、快取起來，同國其他機場不必再要求
async function loadDetails(country){
  const key = country || "ZZ";
  if (detailCache[key]) return detailCache[key];
  try {
    const r = await fetch(`data/details/${encodeURIComponent(key)}.json?v=34`);
    const d = r.ok ? await r.json() : {};
    detailCache[key] = d;
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

/* ── 衛星影像（Esri World Imagery，公開免金鑰圖磚服務）──
   依機場類別選縮放級別，組 3×3 圖磚拼成一張置中的空拍圖，
   同時涵蓋機場全貌與跑道配置，不需額外地圖函式庫。 */
const SAT_ZOOM = {
  large_airport: 13, medium_airport: 14, small_airport: 15,
  seaplane_base: 14, heliport: 16, balloonport: 15, closed: 14,
};
function tileXY(lon, lat, z){
  const n = 2 ** z;
  const x = Math.floor((lon + 180) / 360 * n);
  const latRad = lat * Math.PI / 180;
  const y = Math.floor((1 - Math.log(Math.tan(latRad) + 1 / Math.cos(latRad)) / Math.PI) / 2 * n);
  return { x: ((x % n) + n) % n, y: Math.max(0, Math.min(n - 1, y)) };
}
function tileURL(z, x, y){
  return `https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/${z}/${y}/${x}`;
}
function mosaicImgs(lat, lon, z, r){
  const { x: cx, y: cy } = tileXY(lon, lat, z);
  let tiles = "";
  for (let dy = -r; dy <= r; dy++)
    for (let dx = -r; dx <= r; dx++)
      tiles += `<img src="${tileURL(z, cx + dx, cy + dy)}" alt="">`;
  return tiles;
}
function satelliteHTML(lat, lon, type){
  if (lat == null || lon == null) return "";
  const z = SAT_ZOOM[type] || 14;
  return `<div class="apt-sat" role="button" tabindex="0" data-lat="${lat}" data-lon="${lon}" data-zoom="${z}"
      style="grid-template-columns:repeat(3,1fr)">${mosaicImgs(lat, lon, z, 1)}</div>
    <div class="apt-sat-credit">${I18N.t("airports.sat.hint")} · Imagery © Esri, Maxar, Earthstar Geographics</div>`;
}

/* ── 衛星影像放大檢視（點擊縮圖開啟，可再放大/縮小） ── */
let satState = null;
function openSatLightbox(lat, lon, zoom){
  satState = { lat, lon, zoom };
  renderSatLightbox();
  $("sat-lightbox").hidden = false;
}
function renderSatLightbox(){
  const { lat, lon, zoom } = satState;
  $("sat-lightbox-grid").innerHTML = mosaicImgs(lat, lon, zoom, 2);
  $("sat-lightbox-zoom").textContent = "z" + zoom;
}
function closeSatLightbox(){ $("sat-lightbox").hidden = true; satState = null; }

/* ── 機場備註／照片：檢視與編輯 ── */
let editingImages = [];
const publishedCache = {};
async function fetchPublished(id){
  if (id in publishedCache) return publishedCache[id];
  try {
    const r = await fetch(`data/airport-notes/${encodeURIComponent(id)}.json?v=34`);
    publishedCache[id] = r.ok ? await r.json() : null;
  } catch { publishedCache[id] = null; }
  return publishedCache[id];
}
async function renderNotesView(id){
  const view = $("apt-p-notes-view");
  const local = getNotes(id);
  const hasLocal = local.text || (local.images && local.images.length);
  let notes = local, badge = "";
  if (hasLocal){
    badge = `<div class="apt-notes-badge local">${I18N.t("airports.detail.badgeLocal")}</div>`;
  } else {
    const pub = await fetchPublished(id);
    if (pub && (pub.text || (pub.images && pub.images.length))){
      notes = pub;
      badge = `<div class="apt-notes-badge published">${I18N.t("airports.detail.badgePublished")}</div>`;
    }
  }
  if ($("panel").dataset.id !== id) return;   // 使用者已切到別座機場，避免非同步結果寫錯面板
  const text = I18N.field(notes.text);   // 已發布內容為 {zh,en,ja}，本機草稿為純字串，field() 兩者皆可處理
  if (!text && !(notes.images && notes.images.length)){
    view.innerHTML = `<div class="apt-notes-empty">${I18N.t("airports.detail.noNotes")}</div>`;
    return;
  }
  const imgs = (notes.images || []).map(src => `<img src="${escapeHTML(src)}" alt="">`).join("");
  view.innerHTML = badge +
    (text ? `<p class="apt-notes-text">${escapeHTML(text)}</p>` : "") +
    (imgs ? `<div class="apt-notes-gallery">${imgs}</div>` : "");
}
function renderEditingImages(){
  const el = $("apt-p-notes-imgs");
  el.innerHTML = editingImages.map((src, i) =>
    `<div class="apt-notes-imgitem"><img src="${escapeHTML(src)}" alt=""><button type="button" data-i="${i}" class="apt-notes-imgdel" title="移除">✕</button></div>`
  ).join("");
  el.querySelectorAll(".apt-notes-imgdel").forEach(btn =>
    btn.addEventListener("click", () => { editingImages.splice(+btn.dataset.i, 1); renderEditingImages(); }));
}
function openNotesEditor(id){
  if (!id) return;
  const notes = getNotes(id);
  $("apt-p-notes-text").value = notes.text || "";
  editingImages = (notes.images || []).slice();
  renderEditingImages();
  $("apt-p-notes-view").hidden = true;
  $("apt-p-edit").hidden = true;
  $("apt-p-notes-edit").hidden = false;
}
function closeNotesEditor(){
  $("apt-p-notes-edit").hidden = true;
  $("apt-p-notes-view").hidden = false;
  $("apt-p-edit").hidden = false;
}
// 上傳照片先縮圖壓縮，避免 localStorage 塞爆
function downscaleImg(file, maxW, quality){
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

async function openAirport(id){
  const a = AIRPORTS.find(x => x.id === id);
  if (!a) return;
  const panel = $("panel");
  panel.dataset.id = id;
  syncFavButton();
  closeNotesEditor();
  renderNotesView(id);
  $("apt-p-type").textContent = I18N.t("airports.type." + a.type) || a.type;
  $("apt-p-name").textContent = a.name;
  $("apt-p-loc").textContent = [a.city, countryName(a.country)].filter(Boolean).join(", ");

  const badges = [a.icao, a.iata].filter(Boolean).map(c => `<span class="apt-badge">${c}</span>`);
  $("apt-p-badges").innerHTML = badges.join("");

  $("apt-p-info").innerHTML = "";
  $("apt-p-sat").innerHTML = "";
  const rwEl = $("apt-p-runways");
  rwEl.innerHTML = `<div class="apt-empty" style="padding:20px 0">${I18N.t("viewer.loading")}</div>`;
  panel.classList.add("open");
  panel.setAttribute("aria-hidden", "false");

  const byIdent = await loadDetails(a.country);
  const d = byIdent[a.id] || {};

  $("apt-p-sat").innerHTML = satelliteHTML(d.lat, d.lon, a.type);

  const info = $("apt-p-info");
  const rows = [
    [I18N.t("airports.detail.coords"), (d.lat != null && d.lon != null) ? `${d.lat}, ${d.lon}` : "—"],
    [I18N.t("airports.detail.elevation"), d.elev != null ? `${d.elev} ft (${Math.round(d.elev * M_PER_FT)} m)` : "—"],
    [I18N.t("airports.detail.region"), d.region || "—"],
  ];
  rows.forEach(([k, v]) => {
    const row = document.createElement("div"); row.className = "spec-row";
    const dt = document.createElement("dt"); dt.textContent = k;
    const dd = document.createElement("dd"); dd.textContent = v;
    row.append(dt, dd); info.appendChild(row);
  });

  const rws = d.runways || [];
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
