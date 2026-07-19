"use strict";
/* ═══════════════════════════════════════════════
   機場與跑道 — 搜尋、篩選、機場明細（依國家整批載入）
   資料來源：OurAirports（Public Domain），見 tools/build_airports.py
   全量匯入：85,716 座機場、48,096 條跑道，未篩選類別或代號。
   ═══════════════════════════════════════════════ */

const $ = id => document.getElementById(id);
const MAX_RESULTS = 200;
const GLOBE_MAX = 3000;   // 地球標點上限，跟清單的 200 筆上限脫鉤（球體上稀疏點位不吃效能）

let AIRPORTS = [];
let COUNTRIES = {};
let CITY_NAMES = {};   // "city|country" → {zh, ja}（見 data/city_names.json 產生腳本）
const detailCache = {};   // country code → { ident: {lat,lon,elev,region,runways} }

// 城市層級的中／日文名稱查詢：城市名稱常見於多國（如 Richmond 美加澳南非
// 都有），一律連同國家代碼比對，避免把美國小鎮誤翻成同名的外國大城市；
// 「小地名, 大地名」寫法（如東京都各區 "Minato, Tokyo"）比對不到完整字串時，
// 退而比對逗號後的部分。只收錄有普遍認定譯名的世界主要城市／各國首都，
// 沒收錄的城市維持原文，不機翻猜測。
function cityLocalName(city, country){
  if (!city) return null;
  let hit = CITY_NAMES[`${city}|${country}`];
  if (!hit && city.includes(",")){
    const tail = city.split(",").pop().trim();
    hit = CITY_NAMES[`${tail}|${country}`];
  }
  return hit || null;
}

/* ── 機場⇄航空公司交叉連結：反查「以此機場為樞紐的航空公司」──
   資料來自 data/airline_geo.json（航空公司頁面用同一份離線比對結果），
   兩份小檔案惰性載入，只有真的開到有對應資料的機場才會抓公司名稱清單。 */
let HUB_INDEX = null;      // icao → [airlineId, ...]
let AIRLINE_NAMES = null;  // airlineId → { name, nameZh }
async function loadHubIndex(){
  if (HUB_INDEX) return HUB_INDEX;
  HUB_INDEX = {};
  try {
    const res = await fetch("data/airline_geo.json?v=96");
    const geo = res.ok ? await res.json() : {};
    Object.entries(geo).forEach(([airlineId, g]) => {
      (g.hubs || []).forEach(h => {
        (HUB_INDEX[h.icao] = HUB_INDEX[h.icao] || []).push(airlineId);
      });
    });
  } catch { /* 交叉連結為附加功能，載入失敗不影響機場頁主要功能 */ }
  return HUB_INDEX;
}
async function loadAirlineNames(){
  if (AIRLINE_NAMES) return AIRLINE_NAMES;
  AIRLINE_NAMES = {};
  try {
    const res = await fetch("data/airlines.json?v=96");
    const data = res.ok ? await res.json() : { airlines: [] };
    data.airlines.forEach(a => { AIRLINE_NAMES[a.id] = a; });
  } catch { /* 同上 */ }
  return AIRLINE_NAMES;
}

const FAV_KEY = "hangar_apt_favs";
let FAVS = new Set(JSON.parse(localStorage.getItem(FAV_KEY) || "[]"));
function isFav(id){ return FAVS.has(id); }
function toggleFav(id){
  FAVS.has(id) ? FAVS.delete(id) : FAVS.add(id);
  localStorage.setItem(FAV_KEY, JSON.stringify([...FAVS]));
}

/* ── 加入比較（最多 4 座，就地開全頁彈窗比較，跟機型比較頁完全分開） ── */
const CMP_KEY = "hangar_apt_compare";
let CMP_LIST = JSON.parse(localStorage.getItem(CMP_KEY) || "[]");
function isInCompare(id){ return CMP_LIST.includes(id); }
function toggleCompare(id){
  if (CMP_LIST.includes(id)) CMP_LIST = CMP_LIST.filter(x => x !== id);
  else if (CMP_LIST.length < 4) CMP_LIST.push(id);
  else { alert(I18N.t("airports.cmp.limit")); return; }
  localStorage.setItem(CMP_KEY, JSON.stringify(CMP_LIST));
  renderCompareTray();
  if (!$("apt-cmp-modal").hidden) renderAptCmpPickers();
}
function renderCompareTray(){
  const tray = $("apt-cmp-tray");
  tray.hidden = !CMP_LIST.length;
  if (!CMP_LIST.length) return;
  $("apt-cmp-chips").innerHTML = CMP_LIST.map(id => {
    const a = AIRPORTS.find(x => x.id === id);
    return `<span class="apt-cmp-chip">${a ? (a.icao || a.iata || a.id) : id}<button data-id="${id}" title="${I18N.t("compare.remove")}">✕</button></span>`;
  }).join("");
  $("apt-cmp-chips").querySelectorAll("button").forEach(b =>
    b.addEventListener("click", () => toggleCompare(b.dataset.id)));
}

let aptCmpDiffOnly = false;
const APT_CMP_TYPE_RANK = {
  large_airport: 0, medium_airport: 1, small_airport: 2,
  seaplane_base: 3, heliport: 4, balloonport: 5, closed: 6,
};
function aptCmpSearchScore(a, q){
  const typeRank = APT_CMP_TYPE_RANK[a.type] ?? 7;
  const name = a.name.toLowerCase();
  if ((a.icao && a.icao.toLowerCase() === q) || (a.iata && a.iata.toLowerCase() === q)) return typeRank;
  if (name.startsWith(q)) return 10 + typeRank;
  return 20 + typeRank;
}

function openAptCmpModal(){
  $("apt-cmp-modal").hidden = false;
  renderAptCmpPickers();
}
function closeAptCmpModal(){ $("apt-cmp-modal").hidden = true; }

function renderAptCmpPickers(){
  const wrap = $("apt-cmp-pickers");
  wrap.innerHTML = "";
  CMP_LIST.forEach((id, i) => {
    const meta = AIRPORTS.find(a => a.id === id);
    const box = document.createElement("div");
    box.className = "apt-cmp-picker";
    box.innerHTML = `
      <input type="text" class="apt-cmp-search" value="${meta ? meta.name.replace(/"/g, "&quot;") : ""}"
        placeholder="${I18N.t("compare.apt.search")}" autocomplete="off">
      <div class="apt-cmp-suggest" hidden></div>`;
    const input = box.querySelector(".apt-cmp-search");
    const suggest = box.querySelector(".apt-cmp-suggest");
    input.addEventListener("input", () => {
      const q = input.value.trim().toLowerCase();
      if (!q){ suggest.hidden = true; return; }
      const matches = AIRPORTS
        .filter(a =>
          a.name.toLowerCase().includes(q) ||
          (a.icao && a.icao.toLowerCase().includes(q)) ||
          (a.iata && a.iata.toLowerCase().includes(q)))
        .sort((a, b) => aptCmpSearchScore(a, q) - aptCmpSearchScore(b, q))
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
      renderCompareTray(); renderAptCmpPickers(); await renderAptCmpTable();
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
      renderAptCmpPickers();
      const inputs = wrap.querySelectorAll(".apt-cmp-search");
      inputs[inputs.length - 1].focus();
    });
    wrap.appendChild(add);
  }
  renderAptCmpTable();
}

async function renderAptCmpTable(){
  const table = $("apt-cmp-table");
  const ids = CMP_LIST.filter(Boolean);
  if (!ids.length){ table.innerHTML = ""; return; }

  const metaOf = {};
  ids.forEach(id => { metaOf[id] = AIRPORTS.find(a => a.id === id); });
  const countries = [...new Set(ids.map(id => metaOf[id] && metaOf[id].country).filter(Boolean))];
  const [, notesArr] = await Promise.all([
    Promise.all(countries.map(loadDetails)),
    Promise.all(ids.map(fetchPublished)),
  ]);
  const detailOf = id => {
    const m = metaOf[id];
    const store = detailCache[(m && m.country) || "ZZ"] || {};
    return store[id] || null;
  };
  const notesOf = {};
  ids.forEach((id, i) => { notesOf[id] = notesArr[i]; });

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

  const fmtFt = ft => ft == null ? null : I18N.specValue(`${Math.round(ft * 0.3048)} m (${Math.round(ft)} ft)`);

  html += catBlockAptCmp(I18N.t("compare.basic"), [
    [I18N.t("compare.apt.country"), id => countryName(metaOf[id].country)],
    [I18N.t("compare.apt.city"), id => metaOf[id].city || "—"],
    [I18N.t("compare.apt.type"), id => I18N.t("airports.type." + metaOf[id].type)],
  ], ids);

  html += catBlockAptCmp(I18N.t("compare.apt.location"), [
    [I18N.t("compare.apt.elev"), id => { const d = detailOf(id); return d && d.elev != null ? fmtFt(d.elev) : null; }],
    [I18N.t("compare.apt.coords"), id => { const d = detailOf(id); return d ? `${d.lat.toFixed(4)}, ${d.lon.toFixed(4)}` : null; }],
  ], ids);

  html += catBlockAptCmp(I18N.t("compare.apt.facilities"), [
    [I18N.t("compare.apt.catIls"), id => (notesOf[id] && notesOf[id].catIls) || null],
    [I18N.t("compare.apt.terminals"), id => (notesOf[id] && notesOf[id].terminals) || null],
  ], ids);

  html += catBlockAptCmp(I18N.t("compare.apt.runways"), [
    [I18N.t("compare.apt.rwCount"), id => {
      const d = detailOf(id);
      return d && d.runways ? d.runways.filter(r => !r.closed).length : null;
    }],
    [I18N.t("compare.apt.rwLongest"), id => {
      const d = detailOf(id);
      if (!d || !d.runways || !d.runways.length) return null;
      const longest = Math.max(0, ...d.runways.filter(r => !r.closed).map(r => r.len || 0));
      return longest ? fmtFt(longest) : null;
    }],
    [I18N.t("compare.apt.rwSurf"), id => {
      const d = detailOf(id);
      if (!d || !d.runways) return null;
      const surfs = [...new Set(d.runways.filter(r => !r.closed && r.surf).map(r => surfName(r.surf)))];
      return surfs.length ? surfs.join(" / ") : null;
    }],
    [I18N.t("compare.apt.rwLit"), id => {
      const d = detailOf(id);
      return d && d.runways ? d.runways.filter(r => !r.closed && r.lit).length : null;
    }],
  ], ids);

  html += "</tbody>";
  table.innerHTML = html;

  table.querySelectorAll(".remove").forEach(btn => {
    btn.addEventListener("click", () => {
      CMP_LIST = CMP_LIST.filter(x => x !== btn.dataset.id);
      localStorage.setItem(CMP_KEY, JSON.stringify(CMP_LIST));
      renderCompareTray(); renderAptCmpPickers();
      if (!CMP_LIST.length) closeAptCmpModal();
    });
  });
}

function catBlockAptCmp(catName, rows, ids){
  let rowsHtml = "";
  rows.forEach(([label, getter]) => {
    const vals = ids.map(getter);
    const strVals = vals.map(v => v == null ? null : String(v));
    const allSame = strVals.every(v => v === strVals[0]);
    if (aptCmpDiffOnly && allSame) return;
    rowsHtml += `<tr><td class="label-cell">${label}</td>`;
    strVals.forEach(v => {
      if (v == null) rowsHtml += `<td class="val na">—</td>`;
      else rowsHtml += `<td class="val${!allSame ? " diff" : ""}">${v}</td>`;
    });
    rowsHtml += "</tr>";
  });
  if (!rowsHtml) return "";
  return `<tr class="cat-row"><td colspan="${ids.length + 1}">${catName}</td></tr>` + rowsHtml;
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
      fetch("data/airports.json?v=96"),
      fetch("data/countries.json?v=96"),
    ]);
    const aData = await aRes.json();
    COUNTRIES = await cRes.json();
    AIRPORTS = aData.airports;
  } catch {
    $("apt-list").innerHTML = "";
    $("apt-empty").hidden = false;
    $("apt-empty").textContent = I18N.t("airports.loaderror");
    return;
  }
  try {
    const res = await fetch("data/city_names.json?v=96");
    if (res.ok) CITY_NAMES = await res.json();
  } catch { /* 城市層級翻譯為附加功能，載入失敗不影響主要頁面 */ }

  buildCountrySelect();
  buildTypeSelect();
  I18N.apply();
  applyAll();
  renderCompareTray();

  // 深連結：?icao=XXXX 直接開啟；帶 &globe=1（從航空公司頁樞紐/航線連結
  // 點過來）時順便切到 3D 地圖並飛向該機場，不用使用者自己再手動切換。
  const params = new URLSearchParams(location.search);
  const wantId = params.get("icao");
  if (wantId && AIRPORTS.some(a => a.id === wantId)){
    if (params.get("globe") === "1" && !globeMode) await toggleGlobeMode();
    openAirport(wantId);
  }

  $("apt-search").addEventListener("input", applyAll);
  wireCountryPicker();
  $("apt-type").addEventListener("change", applyAll);
  $("apt-fav-only").addEventListener("change", applyAll);
  $("apt-view-toggle").addEventListener("click", toggleGlobeMode);
  $("apt-globe-rotate").addEventListener("click", () => {
    const on = AptGlobe.toggleAutoRotate();
    $("apt-globe-rotate").setAttribute("aria-pressed", String(on));
  });
  $("apt-globe-reset").addEventListener("click", () => AptGlobe.resetView());
  document.addEventListener("langchange", () => {
    I18N.apply(); buildCountrySelect(); applyAll();
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
  $("apt-p-share").addEventListener("click", async () => {
    const id = $("panel").dataset.id;
    if (!id) return;
    const a = AIRPORTS.find(x => x.id === id);
    const url = `${location.origin}${location.pathname}?icao=${encodeURIComponent(id)}`;
    if (navigator.share){
      try { await navigator.share({ title: a ? a.name : id, url }); return; }
      catch { return; }   // 使用者取消分享，不當錯誤處理
    }
    try {
      await navigator.clipboard.writeText(url);
      alert(I18N.t("airports.detail.shareCopied"));
    } catch {
      window.prompt(I18N.t("airports.detail.shareCopyManual"), url);
    }
  });
  $("apt-p-cmp").addEventListener("click", () => {
    const id = $("panel").dataset.id;
    if (!id) return;
    toggleCompare(id);
    syncCmpButton();
  });
  $("apt-cmp-go").addEventListener("click", openAptCmpModal);
  $("apt-cmp-open").addEventListener("click", openAptCmpModal);
  $("apt-cmp-modal-close").addEventListener("click", closeAptCmpModal);
  document.addEventListener("keydown", e => {
    if (!$("sat-lightbox").hidden){ if (e.key === "Escape") closeSatLightbox(); return; }
    if (!$("apt-cmp-modal").hidden){ if (e.key === "Escape") closeAptCmpModal(); return; }
    if (e.key === "Escape") closePanel();
  });
  document.addEventListener("click", e => {
    if (!$("sat-lightbox").hidden) return;
    const panel = $("panel");
    // 地球畫布用滑鼠點擊會在 pointerup 之後多發一個原生 click 事件，晚於
    // 我們自己在 pointerup 觸發的 pick() 一拍——不排除的話，滑鼠點光點
    // 開面板後這裡會馬上把它關掉（觸控裝置沒有這個問題，這是「手機正常、
    // PC 沒反應」的根因）。
    if (e.target.closest("#apt-globe-canvas")) return;
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
    catch { alert(I18N.t("airports.notes.savefail")); return; }
    renderNotesView(id);
    closeNotesEditor();
  });
  $("apt-p-notes-publish").addEventListener("click", async () => {
    const id = $("panel").dataset.id;
    if (!id) return;
    const text = $("apt-p-notes-text").value.trim();
    const notes = { text, images: editingImages };
    if (!text && !notes.images.length){ alert(I18N.t("airports.notes.empty")); return; }
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

function syncCmpButton(){
  const id = $("panel").dataset.id;
  const on = id && isInCompare(id);
  const btn = $("apt-p-cmp");
  btn.classList.toggle("on", !!on);
  btn.setAttribute("aria-pressed", String(!!on));
}

// 機場中文／日文名稱：只收錄「有普遍認定譯名」的知名機場（見
// tools 產生腳本），其餘沒有收錄的機場維持原英文名稱，不機翻猜測。
// 機場層級的直接翻譯（見 tools 產生腳本）優先；查不到再退而用城市層級翻譯
// 當作次要參考（顯示「城市中文名」而非正式機場譯名，仍有助於搜尋辨識）。
function localName(a){
  const cur = I18N.get();
  if (cur !== "zh" && cur !== "ja") return null;
  const direct = cur === "zh" ? a.nameZh : a.nameJa;
  if (direct) return direct;
  const city = cityLocalName(a.city, a.country);
  return city ? city[cur] : null;
}
function airportLocalNamePlain(a){
  const local = localName(a);
  return local ? `${a.name}（${local}）` : a.name;
}
function airportLocalName(a){
  const local = localName(a);
  return local ? `${a.name} <span class="apt-name-local">${local}</span>` : a.name;
}

function countryName(code){
  const c = COUNTRIES[code];
  if (!c) return code || "—";
  return c[I18N.get()] || c.en || code;
}

let COUNTRY_COUNTS = {};
function buildCountrySelect(){
  COUNTRY_COUNTS = {};
  AIRPORTS.forEach(a => { if (a.country) COUNTRY_COUNTS[a.country] = (COUNTRY_COUNTS[a.country] || 0) + 1; });
  $("apt-country-suggest").hidden = true;
  const cur = $("apt-country").value;
  const meta = COUNTRIES[cur];
  $("apt-country-input").value = cur && meta ? `${countryName(cur)} (${COUNTRY_COUNTS[cur].toLocaleString()})` : "";
}

// 國家篩選：文字輸入依「目前語言」的國名字首篩選（例：英文介面打 "J" 只列
// J 開頭的國家，"Ja" 再縮小到 Ja 開頭；中日文介面用該語言的國名字首比對）。
function renderCountrySuggest(q){
  const suggest = $("apt-country-suggest");
  const ql = q.trim().toLowerCase();
  const codes = Object.keys(COUNTRY_COUNTS)
    .filter(c => !ql || countryName(c).toLowerCase().startsWith(ql))
    .sort((a, b) => countryName(a).localeCompare(countryName(b)));
  if (!codes.length && ql){ suggest.hidden = true; return; }
  const allOpt = ql ? "" : `<div class="apt-cmp-opt" data-code="">
      <span class="apt-cmp-opt-name">${I18N.t("airports.filter.allCountries")}</span>
    </div>`;
  suggest.innerHTML = allOpt + codes.map(c =>
    `<div class="apt-cmp-opt" data-code="${c}">
      <span class="apt-cmp-opt-name">${countryName(c)}</span>
      <span class="apt-cmp-opt-code">${COUNTRY_COUNTS[c].toLocaleString()}</span>
    </div>`).join("");
  suggest.hidden = false;
}

function wireCountryPicker(){
  const hidden = $("apt-country"), input = $("apt-country-input"), suggest = $("apt-country-suggest");
  input.addEventListener("focus", () => renderCountrySuggest(""));
  input.addEventListener("input", () => renderCountrySuggest(input.value));
  suggest.addEventListener("mousedown", e => {
    const opt = e.target.closest(".apt-cmp-opt");
    if (!opt) return;
    const code = opt.dataset.code;
    hidden.value = code;
    input.value = code ? `${countryName(code)} (${COUNTRY_COUNTS[code].toLocaleString()})` : "";
    suggest.hidden = true;
    applyAll();
  });
  input.addEventListener("blur", () => {
    setTimeout(() => {
      suggest.hidden = true;
      // 使用者打了字但沒有從清單點選，還原成目前實際套用的篩選狀態，
      // 避免輸入框文字跟真正的篩選條件對不上。
      const code = hidden.value;
      input.value = code ? `${countryName(code)} (${(COUNTRY_COUNTS[code] || 0).toLocaleString()})` : "";
    }, 150);
  });
  // 清空文字框＋失焦＝清除篩選（比對照原生 <select> 的「所有國家」選項）
  input.addEventListener("keydown", e => {
    if (e.key === "Escape"){ input.value = ""; suggest.hidden = true; input.blur(); }
  });
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
    // 地圖模式下沒有篩選條件時，預設畫出全球大型機場，
    // 不然切到地圖只會看到一顆空球體；清單模式仍維持「請先搜尋」
    list = globeMode ? AIRPORTS.filter(a => a.type === "large_airport") : null;
  } else {
    list = AIRPORTS.filter(a => {
      if (favOnly && !isFav(a.id)) return false;
      if (country && a.country !== country) return false;
      if (type && a.type !== type) return false;
      if (!q) return true;
      const cityHit = cityLocalName(a.city, a.country);
      const hay = [
        a.name, a.nameZh, a.nameJa, a.city, countryName(a.country), a.icao, a.iata,
        cityHit && cityHit.zh, cityHit && cityHit.ja,
      ].filter(Boolean).join(" ").toLowerCase();
      return hay.includes(q);
    });
  }
  render(list);
}

/* ── 3D 地球檢視：切換時惰性初始化，標示目前篩選結果的機場點位 ── */
let globeMode = false;
let globeReqId = 0;   // 篩選變動很快時，避免舊一批座標請求晚回來蓋掉新結果
async function toggleGlobeMode(){
  globeMode = !globeMode;
  $("apt-view-toggle").classList.toggle("active", globeMode);
  $("apt-globe-wrap").hidden = !globeMode;
  $("apt-list").hidden = globeMode;
  if (globeMode && !AptGlobe.isReady())
    await AptGlobe.init($("apt-globe-wrap"), id => openAirport(id),
      on => $("apt-globe-rotate").setAttribute("aria-pressed", String(on)));
  else if (globeMode) AptGlobe.resize();
  applyAll();   // 重新套用目前篩選條件；render() 會依 globeMode 決定要不要順便更新地球標點
}

async function refreshGlobeMarkers(shown){
  const myReq = ++globeReqId;
  const countries = [...new Set(shown.map(a => a.country).filter(Boolean))];
  await Promise.all(countries.map(loadDetails));
  if (myReq !== globeReqId) return;   // 篩選條件已經又變了，這批結果過期
  const points = shown.map(a => {
    const store = detailCache[a.country || "ZZ"] || {};
    const d = store[a.id];
    return d ? { id: a.id, lat: d.lat, lon: d.lon, fav: isFav(a.id), code: a.icao || a.iata || "", type: a.type } : null;
  }).filter(Boolean);
  AptGlobe.setMarkers(points);
}

function render(list){
  const listEl = $("apt-list"), moreEl = $("apt-more"), emptyEl = $("apt-empty"), countEl = $("apt-count");

  if (list === null){
    listEl.innerHTML = ""; moreEl.hidden = true;
    emptyEl.hidden = false; emptyEl.textContent = I18N.t("airports.prompt");
    countEl.textContent = "";
    if (globeMode) refreshGlobeMarkers([]);
    return;
  }
  if (!list.length){
    listEl.innerHTML = ""; moreEl.hidden = true;
    emptyEl.hidden = false; emptyEl.textContent = I18N.t("airports.empty");
    countEl.textContent = "";
    if (globeMode) refreshGlobeMarkers([]);
    return;
  }
  emptyEl.hidden = true;
  list = list.slice().sort((a, b) => (isFav(b.id) ? 1 : 0) - (isFav(a.id) ? 1 : 0) || a.name.localeCompare(b.name));
  const shown = list.slice(0, MAX_RESULTS);
  countEl.innerHTML = `${I18N.t("airports.count.showing")} <b>${shown.length.toLocaleString()}</b> / ${list.length.toLocaleString()}`;
  if (globeMode) refreshGlobeMarkers(list.slice(0, GLOBE_MAX));

  listEl.innerHTML = shown.map(a => {
    const codes = [a.icao, a.iata].filter(Boolean).map(c => `<span>${c}</span>`).join("");
    const loc = [a.city, countryName(a.country)].filter(Boolean).join(", ");
    const fav = isFav(a.id);
    const cmp = isInCompare(a.id);
    return `<div class="apt-row${a.type === "closed" ? " closed" : ""}" data-id="${a.id}" tabindex="0" role="button">
      <span class="apt-type-dot ${a.type}"></span>
      <span class="apt-main">
        <span class="apt-name">${airportLocalName(a)}</span>
        <span class="apt-loc">${loc}</span>
      </span>
      <button class="apt-row-cmp${cmp ? " on" : ""}" data-cmp-id="${a.id}" aria-pressed="${cmp}" title="${I18N.t("airports.detail.addCompare")}">⇄</button>
      <button class="apt-row-fav${fav ? " on" : ""}" data-fav-id="${a.id}" aria-pressed="${fav}" title="${I18N.t("fleet.fav")}">${fav ? "★" : "☆"}</button>
      <span class="apt-codes">${codes}</span>
    </div>`;
  }).join("");

  listEl.querySelectorAll(".apt-row").forEach(row => {
    row.addEventListener("click", e => {
      if (e.target.closest(".apt-row-fav") || e.target.closest(".apt-row-cmp")) return;
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
  listEl.querySelectorAll(".apt-row-cmp").forEach(btn =>
    btn.addEventListener("click", e => {
      e.stopPropagation();
      toggleCompare(btn.dataset.cmpId);
      btn.classList.toggle("on", isInCompare(btn.dataset.cmpId));
      btn.setAttribute("aria-pressed", String(isInCompare(btn.dataset.cmpId)));
      if ($("panel").dataset.id === btn.dataset.cmpId) syncCmpButton();
    }));

  moreEl.hidden = globeMode || list.length <= MAX_RESULTS;
  if (!moreEl.hidden) moreEl.textContent = I18N.t("airports.more").replace("{n}", (list.length - MAX_RESULTS).toLocaleString());
}

// 每個國家的機場明細（座標／標高／行政區碼／跑道清單）合併成一檔，
// 點開該國第一座機場時整批載入、快取起來，同國其他機場不必再要求
async function loadDetails(country){
  const key = country || "ZZ";
  if (detailCache[key]) return detailCache[key];
  try {
    const r = await fetch(`data/details/${encodeURIComponent(key)}.json?v=96`);
    const d = r.ok ? await r.json() : {};
    detailCache[key] = d;
    return d;
  } catch { return {}; }
}

const M_PER_FT = 0.3048;
const SURF_NAMES = {
  ASP:      { zh: "瀝青", en: "Asphalt", ja: "アスファルト" },
  "ASPH-G": { zh: "瀝青", en: "Asphalt", ja: "アスファルト" },
  CON:      { zh: "混凝土", en: "Concrete", ja: "コンクリート" },
  TURF:     { zh: "草地", en: "Turf", ja: "芝地" },
  GRVL:     { zh: "碎石", en: "Gravel", ja: "砂利" },
  GRS:      { zh: "草地", en: "Turf", ja: "芝地" },
  DIRT:     { zh: "泥地", en: "Dirt", ja: "土" },
  WATER:    { zh: "水面", en: "Water", ja: "水面" },
  SAND:     { zh: "沙地", en: "Sand", ja: "砂地" },
};
function surfName(code){
  if (!code) return "—";
  const key = String(code).toUpperCase();
  return SURF_NAMES[key] ? I18N.field(SURF_NAMES[key]) : code;
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
// 衛星影像改用 Esri World Imagery 的 export 端點：一次回傳「一整張」拼好的
// 影像，而不是抓 N×N 塊圖磚再靠 CSS Grid 對齊。原本的圖磚拼貼在桌機正常，
// 但手機瀏覽器（記憶體壓力大、子像素捨入、retina 縮放）常把 25 塊圖磚排得
// 對不上、看起來整個跑掉；單張影像從根本不可能有「對不齊」的問題。
// span 依 zoom 對應「tilesAcross 塊圖磚」的地面範圍，維持跟舊版一致的框景。
function esriExportURL(lat, lon, z, tilesAcross, px){
  const R = 20037508.34;   // Web Mercator 半週長（公尺）
  const cx = lon * R / 180;
  const cy = Math.log(Math.tan((90 + lat) * Math.PI / 360)) / (Math.PI / 180) * R / 180;
  const half = (40075016.6856 / (2 ** z)) * (tilesAcross / 2);   // tilesAcross 塊圖磚的一半寬（公尺）
  const bbox = [cx - half, cy - half, cx + half, cy + half].map(v => v.toFixed(2)).join(",");
  return `https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export` +
    `?bbox=${bbox}&bboxSR=3857&imageSR=3857&size=${px},${px}&format=jpg&f=image`;
}
function satelliteHTML(lat, lon, type){
  if (lat == null || lon == null) return "";
  const z = SAT_ZOOM[type] || 14;
  return `<div class="apt-sat" role="button" tabindex="0" data-lat="${lat}" data-lon="${lon}" data-zoom="${z}">
      <img src="${esriExportURL(lat, lon, z, 3, 640)}" alt="">
    </div>
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
  $("sat-lightbox-zoom").textContent = "z" + zoom;
  // 單張 export 影像：預載完成才換上，避免放大/縮小切換時看到半張舊半張新；
  // 載入期間保留舊影像不清空，不會閃一下空白。
  const img = new Image();
  img.onload = () => {
    if (!satState || satState.lat !== lat || satState.lon !== lon || satState.zoom !== zoom) return;
    const box = $("sat-lightbox-grid");
    box.innerHTML = "";
    box.appendChild(img);
  };
  img.src = esriExportURL(lat, lon, zoom, 5, 1024);
}
function closeSatLightbox(){ $("sat-lightbox").hidden = true; satState = null; }

/* ── 機場備註／照片：檢視與編輯 ── */
let editingImages = [];
const publishedCache = {};
async function fetchPublished(id){
  if (id in publishedCache) return publishedCache[id];
  try {
    const r = await fetch(`data/airport-notes/${encodeURIComponent(id)}.json?v=96`);
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
  syncCmpButton();
  closeNotesEditor();
  renderNotesView(id);
  $("apt-p-type").textContent = I18N.t("airports.type." + a.type) || a.type;
  $("apt-p-name").textContent = airportLocalNamePlain(a);
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

  if (globeMode && typeof AptGlobe !== "undefined" && AptGlobe.isReady()) AptGlobe.focusOn(d.lat, d.lon);

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
  renderHubAirlines(id);
}

async function renderHubAirlines(id){
  const titleEl = $("apt-p-airlines-title"), listEl = $("apt-p-airlines");
  titleEl.hidden = true;
  listEl.innerHTML = "";
  const hubIndex = await loadHubIndex();
  const airlineIds = hubIndex[id];
  if (!airlineIds || !airlineIds.length) return;
  if ($("panel").dataset.id !== id) return;   // 期間使用者已切到別的機場

  const names = await loadAirlineNames();
  if ($("panel").dataset.id !== id) return;
  titleEl.hidden = false;
  listEl.innerHTML = airlineIds.map(aid => {
    const a = names[aid];
    const label = a ? (I18N.get() === "zh" && a.nameZh ? a.nameZh : a.name) : aid;
    return `<a class="apt-p-airline-chip" href="airlines.html?id=${encodeURIComponent(aid)}">${label}</a>`;
  }).join("");
}

function closePanel(){
  const panel = $("panel");
  panel.classList.remove("open");
  panel.setAttribute("aria-hidden", "true");
  history.replaceState(null, "", location.pathname);
  if (typeof AptGlobe !== "undefined") AptGlobe.clearGroundPatch();
}
