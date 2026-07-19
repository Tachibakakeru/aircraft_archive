"use strict";
/* ═══════════════════════════════════════════════
   距離與飛行時間計算器 — 選兩座機場與一款機型，算大圓距離
   （haversine 公式）與粗估飛行時間（距離 / 巡航速度 + 30 分鐘
   滑行／爬升／下降緩衝）。純前端運算，不依賴外部 API。
   機場座標沿用 airports.js 同一套「機場清單 + 按國家分檔的
   經緯度明細」資料來源；機型巡航速度取自各機型詳情頁
   specifications 的「性能／巡航速度」欄位（自由格式文字，
   用正規表示式取出 km/h 數字）。
   ═══════════════════════════════════════════════ */

const $ = id => document.getElementById(id);

let AIRPORTS = [];
let FLEET = [];
const detailCache = {};   // country(ISO2) → { airportId: {lat,lon,...} }
const speedCache = {};    // aircraftId → 巡航速度 km/h

let fromId = null, toId = null;

async function loadDetails(country){
  if (!country || detailCache[country]) return detailCache[country] || {};
  try {
    const res = await fetch(`data/details/${country}.json?v=98`);
    detailCache[country] = res.ok ? await res.json() : {};
  } catch { detailCache[country] = {}; }
  return detailCache[country];
}

async function airportCoords(id){
  const meta = AIRPORTS.find(a => a.id === id);
  if (!meta) return null;
  const store = await loadDetails(meta.country);
  const d = store[id];
  return d ? { lat: d.lat, lon: d.lon, meta } : null;
}

// 巡航速度取自 specifications 裡標籤含「速度」或數值含 km/h 的第一筆，
// 跟每款機型自己詳情頁使用的資料完全同一份，不重複維護一套數字。
async function cruiseSpeedKmh(id){
  if (speedCache[id] != null) return speedCache[id];
  try {
    const res = await fetch(`data/${id}.json?v=98`);
    if (!res.ok) throw new Error();
    const d = await res.json();
    let kmh = null;
    for (const rows of Object.values(d.specifications || {})){
      for (const [k, v] of rows){
        if (typeof v !== "string") continue;
        if (v.includes("km/h") || k.includes("速度")){
          const m = v.match(/([\d,]+)\s*km\/h/);
          if (m){ kmh = parseInt(m[1].replace(/,/g, ""), 10); break; }
        }
      }
      if (kmh) break;
    }
    speedCache[id] = kmh;
    return kmh;
  } catch {
    speedCache[id] = null;
    return null;
  }
}

function haversineKm(lat1, lon1, lat2, lon2){
  const R = 6371;
  const toRad = d => d * Math.PI / 180;
  const dLat = toRad(lat2 - lat1), dLon = toRad(lon2 - lon1);
  const a = Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

// 噴射氣流粗估模型：中緯度（南北緯約 30–60 度）高空盛行西風，順著風向飛
// （由西向東）較快、頂風飛（由東向西）較慢，同一條航線兩個方向的實際飛行
// 時間常常差 30 分鐘以上。這裡用「大圓路徑起始方位角的東西分量」×「緯度
// 權重（在中緯度最強、赤道與極區趨近於零）」估出順風／頂風分量，屬簡化
// 概算，不是真實氣象資料——真實噴流強度隨季節、高度、當年天氣系統變動
// 極大（範圍大致 50～400+ km/h）。
const JET_STREAM_KMH = 130;   // 中緯度巡航高度的概估平均風速
function initialBearingRad(lat1, lon1, lat2, lon2){
  const toRad = d => d * Math.PI / 180;
  const φ1 = toRad(lat1), φ2 = toRad(lat2), Δλ = toRad(lon2 - lon1);
  const y = Math.sin(Δλ) * Math.cos(φ2);
  const x = Math.cos(φ1) * Math.sin(φ2) - Math.sin(φ1) * Math.cos(φ2) * Math.cos(Δλ);
  return Math.atan2(y, x);
}
function windComponentKmh(lat1, lon1, lat2, lon2){
  const bearing = initialBearingRad(lat1, lon1, lat2, lon2);
  const eastComponent = Math.sin(bearing);   // 正東 = 1（順風）、正西 = -1（頂風）
  const avgAbsLat = Math.min(90, (Math.abs(lat1) + Math.abs(lat2)) / 2);
  const latFactor = Math.sin(avgAbsLat * Math.PI / 90);   // 中緯度（約45°）最強，赤道／極區趨近 0
  return JET_STREAM_KMH * eastComponent * latFactor;
}
function effectiveSpeedKmh(cruiseKmh, lat1, lon1, lat2, lon2){
  const wind = windComponentKmh(lat1, lon1, lat2, lon2);
  return Math.max(cruiseKmh * 0.5, cruiseKmh + wind);   // 極端頂風時設下限，避免算出離譜的龜速
}

function fmtHours(h){
  const totalMin = Math.round(h * 60);
  const hh = Math.floor(totalMin / 60), mm = totalMin % 60;
  return `${hh}${I18N.t("distance.hUnit")} ${mm}${I18N.t("distance.minUnit")}`;
}

(async () => {
  try {
    const [aRes, fRes] = await Promise.all([
      fetch("data/airports.json?v=98"),
      fetch("data/fleet.json?v=98"),
    ]);
    AIRPORTS = (await aRes.json()).airports;
    FLEET = (await fRes.json()).aircraft;
  } catch {
    $("dist-empty").textContent = I18N.t("distance.loaderror");
    return;
  }

  I18N.apply();
  buildAircraftSelect();
  wirePicker($("dist-from-picker"), $("dist-from-input"), id => { fromId = id; recalc(); });
  wirePicker($("dist-to-picker"), $("dist-to-input"), id => { toId = id; recalc(); });
  $("dist-aircraft").addEventListener("change", recalc);
  $("dist-swap-btn").addEventListener("click", () => {
    [fromId, toId] = [toId, fromId];
    const fromMeta = AIRPORTS.find(a => a.id === fromId), toMeta = AIRPORTS.find(a => a.id === toId);
    $("dist-from-input").value = fromMeta ? fromMeta.name : "";
    $("dist-to-input").value = toMeta ? toMeta.name : "";
    recalc();
  });

  I18N.mountSelector($("btn-lang"));
  $("btn-theme").addEventListener("click", () => window.HangarTheme.toggle());
  document.addEventListener("langchange", () => { I18N.apply(); recalc(); });

  const p = new URLSearchParams(location.search);
  if (p.get("from") && AIRPORTS.some(a => a.id === p.get("from"))){
    fromId = p.get("from");
    $("dist-from-input").value = AIRPORTS.find(a => a.id === fromId).name;
  }
  if (p.get("to") && AIRPORTS.some(a => a.id === p.get("to"))){
    toId = p.get("to");
    $("dist-to-input").value = AIRPORTS.find(a => a.id === toId).name;
  }
  recalc();
})();

function buildAircraftSelect(){
  const sel = $("dist-aircraft");
  sel.innerHTML = `<option value="">${I18N.t("distance.chooseAircraft")}</option>` +
    FLEET.map(a => `<option value="${a.id}">${a.name}</option>`).join("");
}

function searchScore(a, q){
  const name = a.name.toLowerCase();
  if (a.icao && a.icao.toLowerCase() === q) return 0;
  if (a.iata && a.iata.toLowerCase() === q) return 0;
  if (name.startsWith(q)) return 1;
  return 2;
}

function wirePicker(box, input, onSelect){
  const suggest = box.querySelector(".apt-cmp-suggest");
  input.addEventListener("input", () => {
    const q = input.value.trim().toLowerCase();
    if (!q){ suggest.hidden = true; onSelect(null); return; }
    const matches = AIRPORTS
      .filter(a =>
        a.name.toLowerCase().includes(q) ||
        (a.city && a.city.toLowerCase().includes(q)) ||
        (a.icao && a.icao.toLowerCase().includes(q)) ||
        (a.iata && a.iata.toLowerCase().includes(q)))
      .sort((a, b) => searchScore(a, q) - searchScore(b, q))
      .slice(0, 8);
    if (!matches.length){ suggest.hidden = true; return; }
    suggest.innerHTML = matches.map(a =>
      `<div class="apt-cmp-opt" data-id="${a.id}">
        <span class="apt-cmp-opt-name">${a.name}</span>
        <span class="apt-cmp-opt-code">${[a.icao, a.iata].filter(Boolean).join(" · ")}</span>
      </div>`).join("");
    suggest.hidden = false;
  });
  suggest.addEventListener("mousedown", e => {
    const opt = e.target.closest(".apt-cmp-opt");
    if (!opt) return;
    const meta = AIRPORTS.find(a => a.id === opt.dataset.id);
    input.value = meta.name;
    suggest.hidden = true;
    onSelect(meta.id);
  });
  input.addEventListener("blur", () => setTimeout(() => { suggest.hidden = true; }, 150));
}

async function recalc(){
  const aircraftId = $("dist-aircraft").value;
  const resultEl = $("dist-result"), emptyEl = $("dist-empty");
  if (!fromId || !toId || !aircraftId){
    resultEl.hidden = true;
    emptyEl.hidden = false;
    return;
  }
  if (fromId === toId){
    resultEl.hidden = true;
    emptyEl.hidden = false;
    emptyEl.textContent = I18N.t("distance.sameAirport");
    return;
  }
  emptyEl.hidden = true;

  const [from, to, kmh] = await Promise.all([
    airportCoords(fromId), airportCoords(toId), cruiseSpeedKmh(aircraftId),
  ]);
  if (!from || !to){
    resultEl.hidden = true;
    emptyEl.hidden = false;
    emptyEl.textContent = I18N.t("distance.noCoords");
    return;
  }

  const km = haversineKm(from.lat, from.lon, to.lat, to.lon);
  const nmi = km / 1.852;

  $("dist-route").textContent =
    `${from.meta.name} (${from.meta.icao || from.meta.iata || ""}) → ${to.meta.name} (${to.meta.icao || to.meta.iata || ""})`;
  $("dist-km").textContent = `${Math.round(km).toLocaleString()} km ／ ${Math.round(nmi).toLocaleString()} nmi`;

  if (kmh){
    const outboundKmh = effectiveSpeedKmh(kmh, from.lat, from.lon, to.lat, to.lon);
    const returnKmh = effectiveSpeedKmh(kmh, to.lat, to.lon, from.lat, from.lon);
    const outboundH = km / outboundKmh + 0.5;   // +30 分鐘滑行／爬升／下降緩衝
    const returnH = km / returnKmh + 0.5;
    $("dist-time").textContent = fmtHours(outboundH);
    $("dist-time-return").textContent = fmtHours(returnH);
    $("dist-speed").textContent = `${Math.round(outboundKmh).toLocaleString()} km/h`;
  } else {
    $("dist-time").textContent = "—";
    $("dist-time-return").textContent = "—";
    $("dist-speed").textContent = "—";
  }
  resultEl.hidden = false;
}
