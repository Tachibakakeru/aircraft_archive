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
    const res = await fetch(`data/details/${country}.json?v=76`);
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
    const res = await fetch(`data/${id}.json?v=76`);
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

function fmtHours(h){
  const totalMin = Math.round(h * 60);
  const hh = Math.floor(totalMin / 60), mm = totalMin % 60;
  return `${hh}${I18N.t("distance.hUnit")} ${mm}${I18N.t("distance.minUnit")}`;
}

(async () => {
  try {
    const [aRes, fRes] = await Promise.all([
      fetch("data/airports.json?v=76"),
      fetch("data/fleet.json?v=76"),
    ]);
    AIRPORTS = (await aRes.json()).airports;
    FLEET = (await fRes.json()).aircraft;
  } catch {
    $("dist-empty").textContent = "資料載入失敗，請確認以本機伺服器開啟。";
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
    const hours = km / kmh + 0.5;   // +30 分鐘滑行／爬升／下降緩衝
    $("dist-time").textContent = fmtHours(hours);
    $("dist-speed").textContent = `${kmh.toLocaleString()} km/h`;
  } else {
    $("dist-time").textContent = "—";
    $("dist-speed").textContent = "—";
  }
  resultEl.hidden = false;
}
