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

// 機場代碼自動連結：data/airport_codes.json 是 ICAO/IATA 代碼 → 機場名稱／
// 座標的完整索引（涵蓋所有有代碼的機場，19,308 筆）。編輯樞紐／航線時
// 直接輸入代碼（如 "NRT"），不需要等離線腳本重新比對，顯示時就能即時
// 解析出真正的機場名稱並連結到機場頁。
let AIRPORT_CODES = {};
function resolveAirportCode(text){
  const code = text.trim().toUpperCase();
  if (!/^[A-Z0-9]{3,4}$/.test(code)) return null;
  const r = AIRPORT_CODES[code];
  return r ? { id: r.id, name: r.city || r.name, lat: r.lat, lon: r.lon } : null;
}

// 國家名稱中英對照：72 家人工彙整的公司 country.zh 是正確翻譯的中文，
// 但另外 503 家由 OpenFlights 資料批次生成的公司 country.zh/en 目前是
// 同一個英文原文（未翻譯）——搜尋「中國」只會比對到前者，漏掉後者，
// 反之搜尋「China」也漏掉已翻譯成中文的那些。這份對照表讓搜尋時不論
// 用中文或英文輸入國家名稱，都能涵蓋到所有語言版本的資料。
// （只影響「國家」欄位的比對，不會讓航空公司自己的名稱被連帶誤配對。）
const COUNTRY_ZH = {
  "Afghanistan": "阿富汗", "Albania": "阿爾巴尼亞", "Algeria": "阿爾及利亞",
  "Angola": "安哥拉", "Antigua and Barbuda": "安地卡及巴布達", "Argentina": "阿根廷",
  "Armenia": "亞美尼亞", "Aruba": "阿魯巴", "Australia": "澳洲", "Austria": "奧地利",
  "Azerbaijan": "亞塞拜然", "Bahamas": "巴哈馬", "Bahrain": "巴林",
  "Bangladesh": "孟加拉", "Belarus": "白俄羅斯", "Belgium": "比利時",
  "Belize": "貝里斯", "Bhutan": "不丹", "Bolivia": "玻利維亞",
  "Bosnia and Herzegovina": "波士尼亞與赫塞哥維納", "Botswana": "波札那",
  "Brazil": "巴西", "Brunei": "汶萊", "Bulgaria": "保加利亞",
  "Burkina Faso": "布吉納法索", "Burma": "緬甸", "Cambodia": "柬埔寨",
  "Canada": "加拿大", "Cayman Islands": "開曼群島", "Chile": "智利",
  "China": "中國", "Colombia": "哥倫比亞", "Cook Islands": "庫克群島",
  "Costa Rica": "哥斯大黎加", "Croatia": "克羅埃西亞", "Cuba": "古巴",
  "Cyprus": "賽普勒斯", "Czech Republic": "捷克",
  "Democratic People's Republic of Korea": "北韓", "Denmark": "丹麥",
  "Djibouti": "吉布地", "Dominican Republic": "多明尼加", "Ecuador": "厄瓜多",
  "Egypt": "埃及", "Equatorial Guinea": "赤道幾內亞", "Eritrea": "厄利垂亞",
  "Estonia": "愛沙尼亞", "Ethiopia": "衣索比亞", "Faroe Islands": "法羅群島",
  "Fiji": "斐濟", "Finland": "芬蘭", "France": "法國",
  "French Guiana": "法屬圭亞那", "French Polynesia": "法屬玻里尼西亞",
  "Georgia": "喬治亞", "Germany": "德國", "Greece": "希臘", "Haiti": "海地",
  "Hong Kong": "香港", "Hong Kong SAR of China": "香港", "Hungary": "匈牙利",
  "Iceland": "冰島", "India": "印度", "Indonesia": "印尼", "Iran": "伊朗",
  "Iraq": "伊拉克", "Ireland": "愛爾蘭", "Israel": "以色列", "Italy": "義大利",
  "Ivory Coast": "象牙海岸", "Jamaica": "牙買加", "Japan": "日本",
  "Jordan": "約旦", "Kazakhstan": "哈薩克", "Kenya": "肯亞",
  "Kiribati": "吉里巴斯", "Kuwait": "科威特", "Kyrgyzstan": "吉爾吉斯",
  "Lao Peoples Democratic Republic": "寮國", "Latvia": "拉脫維亞",
  "Lebanon": "黎巴嫩", "Libya": "利比亞", "Lithuania": "立陶宛",
  "Luxembourg": "盧森堡", "Macao": "澳門", "Madagascar": "馬達加斯加",
  "Malawi": "馬拉威", "Malaysia": "馬來西亞", "Maldives": "馬爾地夫",
  "Malta": "馬爾他", "Mauritania": "茅利塔尼亞", "Mauritius": "模里西斯",
  "Mexico": "墨西哥", "Moldova": "摩爾多瓦", "Mongolia": "蒙古",
  "Montenegro": "蒙特內哥羅", "Morocco": "摩洛哥", "Mozambique": "莫三比克",
  "Myanmar": "緬甸", "Namibia": "納米比亞", "Nauru": "諾魯", "Nepal": "尼泊爾",
  "Netherlands": "荷蘭", "New Zealand": "紐西蘭", "Nigeria": "奈及利亞",
  "Norway": "挪威", "Oman": "阿曼", "Pakistan": "巴基斯坦", "Panama": "巴拿馬",
  "Papua New Guinea": "巴布亞紐幾內亞", "Paraguay": "巴拉圭", "Peru": "秘魯",
  "Philippines": "菲律賓", "Poland": "波蘭", "Portugal": "葡萄牙",
  "Qatar": "卡達", "Republic of Korea": "韓國", "Romania": "羅馬尼亞",
  "Russia": "俄羅斯", "Russian Federation": "俄羅斯", "Rwanda": "盧安達",
  "Samoa": "薩摩亞", "Sao Tome and Principe": "聖多美普林西比",
  "Saudi Arabia": "沙烏地阿拉伯", "Serbia": "塞爾維亞", "Seychelles": "塞席爾",
  "Singapore": "新加坡", "Slovakia": "斯洛伐克", "Slovenia": "斯洛維尼亞",
  "Solomon Islands": "索羅門群島", "South Africa": "南非", "South Korea": "韓國",
  "Spain": "西班牙", "Sri Lanka": "斯里蘭卡", "Sudan": "蘇丹",
  "Suriname": "蘇利南", "Sweden": "瑞典", "Switzerland": "瑞士",
  "Syrian Arab Republic": "敘利亞", "Taiwan": "台灣", "Tanzania": "坦尚尼亞",
  "Thailand": "泰國", "Trinidad and Tobago": "千里達及托巴哥",
  "Tunisia": "突尼西亞", "Turkey": "土耳其", "Turkmenistan": "土庫曼",
  "Ukraine": "烏克蘭", "United Arab Emirates": "阿聯酋",
  "United Kingdom": "英國", "United States": "美國", "Uzbekistan": "烏茲別克",
  "Vanuatu": "萬那杜", "Venezuela": "委內瑞拉", "Vietnam": "越南",
  "Yemen": "葉門", "Zimbabwe": "辛巴威",
};
const COUNTRY_EN = Object.fromEntries(Object.entries(COUNTRY_ZH).map(([en, zh]) => [zh, en]));
function countryAliases(a){
  const out = [];
  if (COUNTRY_ZH[a.country.en]) out.push(COUNTRY_ZH[a.country.en]);
  if (COUNTRY_EN[a.country.zh]) out.push(COUNTRY_EN[a.country.zh]);
  return out;
}

// 公司在地化名稱：跟機場頁 localName() 同一套邏輯，中文顯示 nameZh、
// 日文顯示 nameJa，兩者都只收錄有公認譯名的公司（見上方常數），沒有的
// 維持英文原名，不機翻猜測。
function localAirlineName(a){
  const cur = I18N.get();
  if (cur === "zh") return a.nameZh || null;
  if (cur === "ja") return a.nameJa || null;
  return null;
}

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
          (a.nameJa && a.nameJa.includes(q)) ||
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
      const res = await fetch("data/airlines.json?v=91");
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
    const geoRes = await fetch("data/airline_geo.json?v=91");
    if (geoRes.ok) AIRLINE_GEO = await geoRes.json();
  } catch { /* 航線地圖為附加功能，載入失敗不影響主要頁面 */ }
  try {
    const codesRes = await fetch("data/airport_codes.json?v=91");
    if (codesRes.ok) AIRPORT_CODES = await codesRes.json();
  } catch { /* 代碼自動連結為附加功能，載入失敗不影響主要頁面 */ }

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
    // 拖曳／點擊地球畫布旋轉視角時，放開滑鼠會在 pointerup 之後多發一個
    // 原生 click 事件——不排除的話，只是想轉一下地球看航線，面板就被這裡
    // 誤判成「點擊面板外」給關掉了，弧線也跟著被清空，整個看不到結果。
    if (e.target.closest("#apt-globe-canvas")) return;
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

// 樞紐／航線座標：優先用離線腳本比對好的 data/airline_geo.json（涵蓋既有
// 描述性文字），查不到的再看是不是直接輸入的 ICAO/IATA 代碼（即時解析，
// 不必等離線腳本重新跑一輪就能馬上在地圖上看到剛編輯好的樞紐／航線）。
function resolveLatLon(texts, geoList){
  const byText = new Map((geoList || []).map(g => [g.text, g]));
  const out = [];
  (texts || []).forEach(t => {
    const g = byText.get(t);
    if (g){ out.push({ lat: g.lat, lon: g.lon }); return; }
    const r = resolveAirportCode(t);
    if (r) out.push({ lat: r.lat, lon: r.lon });
  });
  return out;
}

function showAirlineRoutes(id){
  if (!globeMode || !AptGlobe.isReady()) return;
  const a = AIRLINES.find(x => x.id === id);
  const geo = AIRLINE_GEO[id];
  const hubs = resolveLatLon(a && a.hubs, geo && geo.hubs);
  const routes = resolveLatLon(a && a.routes, geo && geo.routes);
  if (!hubs.length){
    // 沒有可定位的樞紐座標——除了清掉舊航線弧線，也要一併清掉地面貼圖，
    // 否則使用者剛才在地圖上直接點過的機場衛星貼片會卡在原地，換看
    // 下一家沒有樞紐座標的公司時畫面上仍殘留著舊的地面圖磚。
    AptGlobe.setRoutes([]);
    AptGlobe.clearGroundPatch();
    return;
  }
  const arcs = [];
  hubs.forEach(hub => {
    routes.forEach(r => arcs.push({ fromLat: hub.lat, fromLon: hub.lon, toLat: r.lat, toLon: r.lon }));
  });
  AptGlobe.setRoutes(arcs);
  AptGlobe.focusOn(hubs[0].lat, hubs[0].lon);
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
    const hay = [a.name, a.nameZh, a.nameJa, a.icao, a.iata, I18N.field(a.country), a.country.zh, a.country.en, ...countryAliases(a), ...(a.hubs || [])].filter(Boolean).join(" ").toLowerCase();
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
    const localTag = localAirlineName(a) ? ` <span class="al-name-zh">${localAirlineName(a)}</span>` : "";
    return `<div class="al-row" data-id="${a.id}" tabindex="0" role="button">
      <span class="al-logo-slot"></span>
      <span class="al-alliance-dot ${a.alliance}"></span>
      <span class="al-main">
        <span class="al-name">${a.name}${localTag}</span>
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
// &globe=1：從這裡點過去機場頁時，順便切到 3D 地圖並直接飛向該機場，
// 不用使用者自己再手動切換地圖模式、找半天。
function airportLinkHref(icao){
  return `airports.html?icao=${encodeURIComponent(icao)}&globe=1`;
}

function hubsHTML(a){
  if (!a.hubs || !a.hubs.length) return "—";
  const geo = AIRLINE_GEO[a.id];
  const byText = new Map((geo && geo.hubs || []).map(h => [h.text, h.icao]));
  return a.hubs.map(h => {
    const icao = byText.get(h);
    if (icao) return `<a class="al-hub-link" href="${airportLinkHref(icao)}">${escHTML(h)}</a>`;
    const resolved = resolveAirportCode(h);
    if (resolved) return `<a class="al-hub-link" href="${airportLinkHref(resolved.id)}">${escHTML(resolved.name)}</a>`;
    return escHTML(h);
  }).join(" / ");
}

function routesHTML(a){
  if (!a.routes || !a.routes.length) return "";
  const geo = AIRLINE_GEO[a.id];
  const byText = new Map((geo && geo.routes || []).map(r => [r.text, r.icao]));
  return a.routes.map(r => {
    const icao = byText.get(r);
    if (icao) return `<a class="al-route-chip" href="${airportLinkHref(icao)}">${escHTML(r)}</a>`;
    const resolved = resolveAirportCode(r);
    if (resolved) return `<a class="al-route-chip" href="${airportLinkHref(resolved.id)}">${escHTML(resolved.name)}</a>`;
    return `<span class="al-route-chip">${escHTML(r)}</span>`;
  }).join("");
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
  $("al-p-name").textContent = localAirlineName(a) ? `${a.name}（${localAirlineName(a)}）` : a.name;
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

  $("al-p-routes").innerHTML = routesHTML(a);

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
  if (globeMode && typeof AptGlobe !== "undefined" && AptGlobe.isReady()){
    AptGlobe.setRoutes([]);
    AptGlobe.clearGroundPatch();
  }
}

// ── 編輯功能：僅本機暫存，需通過密碼驗證後點「儲存到網站」才會公開 ──
const EDIT_FIELD_IDS = [
  "al-e-name", "al-e-namezh", "al-e-nameja", "al-e-icao", "al-e-iata", "al-e-founded", "al-e-alliance", "al-e-tier",
  "al-e-country-zh", "al-e-country-en", "al-e-country-ja", "al-e-hubs", "al-e-fleettotal",
  "al-e-fleet", "al-e-routes", "al-e-tagline-zh", "al-e-tagline-en", "al-e-tagline-ja",
  "al-e-customlogo", "al-e-photo",
];

function openEditor(id){
  const a = AIRLINES.find(x => x.id === id);
  if (!a) return;
  $("al-e-name").value = a.name || "";
  $("al-e-namezh").value = a.nameZh || "";
  $("al-e-nameja").value = a.nameJa || "";
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
  const nameJa = $("al-e-nameja").value.trim();
  if (nameJa) a.nameJa = nameJa; else delete a.nameJa;
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
