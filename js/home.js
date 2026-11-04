"use strict";
/* ═══════════════════════════════════════════════
   首頁「出境大廳」：訂票式全站搜尋、航線示意、登機證入口、
   每日出發看板、機長廣播（小知識）、METAR 資料庫狀態。
   依賴 js/i18n.js（home.* 字串）與 js/theme.js（HangarTheme）。
   設計紀錄：docs/homepage-concept.md
   ═══════════════════════════════════════════════ */
/* 熱門航點：首屏航線示意與看板用，避免一開始就下載 1.9 MB 的全球代碼表 */
const POPULAR = [
  ["RJTT","HND",35.5523,139.7798,"東京羽田","Tokyo Haneda","東京羽田"],
  ["RJAA","NRT",35.7647,140.3864,"東京成田","Tokyo Narita","東京成田"],
  ["RJBB","KIX",34.4273,135.2440,"大阪關西","Osaka Kansai","関西"],
  ["VHHH","HKG",22.3089,113.9146,"香港","Hong Kong","香港"],
  ["WSSS","SIN",1.3502,103.9944,"新加坡樟宜","Singapore Changi","シンガポール・チャンギ"],
  ["RKSI","ICN",37.4691,126.4505,"首爾仁川","Seoul Incheon","ソウル仁川"],
  ["VTBS","BKK",13.6811,100.7473,"曼谷蘇凡納布","Bangkok Suvarnabhumi","バンコク・スワンナプーム"],
  ["OMDB","DXB",25.2528,55.3644,"杜拜","Dubai","ドバイ"],
  ["EGLL","LHR",51.4706,-0.4619,"倫敦希斯洛","London Heathrow","ロンドン・ヒースロー"],
  ["LFPG","CDG",49.0128,2.5500,"巴黎戴高樂","Paris Charles de Gaulle","パリ・シャルル・ド・ゴール"],
  ["EDDF","FRA",50.0333,8.5706,"法蘭克福","Frankfurt","フランクフルト"],
  ["KSFO","SFO",37.6190,-122.3750,"舊金山","San Francisco","サンフランシスコ"],
  ["KLAX","LAX",33.9425,-118.4081,"洛杉磯","Los Angeles","ロサンゼルス"],
  ["KJFK","JFK",40.6398,-73.7789,"紐約甘迺迪","New York JFK","ニューヨーク JFK"],
  ["YSSY","SYD",-33.9461,151.1772,"雪梨","Sydney","シドニー"],
  ["RCSS","TSA",25.0694,121.5525,"臺北松山","Taipei Songshan","台北松山"]
].map(([icao,iata,lat,lon,zh,en,ja]) => ({icao,iata,lat,lon,name:{zh,en,ja}}));
const TPE = {icao:"RCTP",iata:"TPE",lat:25.0777,lon:121.2330};

/* 讀不到資料時（例如離線）仍能完整呈現的後備數字 */
const FALLBACK = {aircraft:184, models:48, airports:85587, airlines:594, cargo:18, alliances:3, topics:82};

/* ═══════════════ 小工具 ═══════════════ */
const $ = s => document.querySelector(s);
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const store = {
  get(k){ try { return localStorage.getItem(k); } catch (e) { return null; } },
  set(k,v){ try { localStorage.setItem(k,v); } catch (e) {} }
};
let lang = I18N.get();
/* 首頁字串都在 js/i18n.js 的 home.* 命名空間；{name} 形式的變數在這裡代入 */
const t = (k, vars) => {
  let s = I18N.t("home." + k);
  if (vars) for (const [a,b] of Object.entries(vars)) s = s.split(`{${a}}`).join(b);
  return s;
};
const field = v => I18N.field(v);
const catName = c => { const s = I18N.t("home.cat." + c); return s.startsWith("home.") ? (c || "") : s; };
const fmt = n => Number(n).toLocaleString(lang === "zh" ? "zh-TW" : lang);
const airlineName = a => (lang === "zh" && a.nameZh) || (lang === "ja" && a.nameJa) || a.name;
function rng(seed){ return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let x = Math.imul(seed ^ seed >>> 15, 1 | seed); x = x + Math.imul(x ^ x >>> 7, 61 | x) ^ x; return ((x ^ x >>> 14) >>> 0) / 4294967296; }; }
function gcKm(a, b){
  const R = 6371, r = Math.PI / 180;
  const dLat = (b.lat - a.lat) * r, dLon = (b.lon - a.lon) * r;
  const h = Math.sin(dLat/2)**2 + Math.cos(a.lat*r) * Math.cos(b.lat*r) * Math.sin(dLon/2)**2;
  return 2 * R * Math.asin(Math.sqrt(h));
}
function blockTime(km){ const min = Math.round(km / 830 * 60 + 30); return t("hours", {h: Math.floor(min/60), m: String(min%60).padStart(2,"0")}); }
function cruiseFl(km){ return km < 900 ? "FL280" : km < 2500 ? "FL350" : km < 6000 ? "FL370" : "FL390"; }
async function getJSON(path, v){
  for (const url of (v ? [`${path}?v=${v}`, path] : [path])) {
    try { const r = await fetch(url); if (r.ok) return await r.json(); } catch (e) {}
  }
  return null;
}

/* ═══════════════ 資料 ═══════════════ */
const D = {fleet:[], airlines:[], topics:[], airportCount:FALLBACK.airports, codes:null};
const counts = () => ({
  aircraft: D.fleet.length || FALLBACK.aircraft,
  models: D.fleet.length ? D.fleet.filter(a => !/nomodel/.test(a.thumb || "")).length : FALLBACK.models,
  airports: D.airportCount,
  airlines: D.airlines.length || FALLBACK.airlines,
  cargo: D.airlines.length ? D.airlines.filter(a => a.tier === "cargo").length : FALLBACK.cargo,
  alliances: D.airlines.length ? new Set(D.airlines.map(a => a.alliance).filter(x => ["star","oneworld","skyteam"].includes(x))).size : FALLBACK.alliances,
  topics: D.topics.length || FALLBACK.topics
});

/* ═══════════════ 介面字串 ═══════════════ */
function applyStatic(){
  lang = I18N.get();
  I18N.apply();
  $("#theme").setAttribute("aria-label", t("theme"));
  document.querySelectorAll("#lang button").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.lang === lang)));
  setPlaceholder();
}
function renderAll(){ applyStatic(); renderChips(); renderPasses(); renderRecent(); renderWallet(); renderBoard(false); renderPA(); renderMetar(); updateRouteText(); }

/* ═══════════════ 登機證 ═══════════════ */
const GATES = [
  {k:"fleet", href:"fleet.html", to:"ACF", gate:"A", seat:"3D", f:c => [fmt(c.aircraft), fmt(c.models), fmt(c.aircraft - c.models)], d:c => ({n:fmt(c.aircraft), m:fmt(c.models)})},
  {k:"airports", href:"airports.html", to:"APT", gate:"B", seat:"RWY", f:c => [fmt(c.airports), "ICAO·IATA", t("p.airports.v3")], d:c => ({n:fmt(c.airports)})},
  {k:"airlines", href:"airlines.html", to:"ALN", gate:"C", seat:"HUB", f:c => [fmt(c.airlines), fmt(c.cargo), fmt(c.alliances)], d:c => ({n:fmt(c.airlines)})},
  {k:"knowledge", href:"knowledge.html", to:"KNW", gate:"D", seat:"PA", f:c => [fmt(c.topics), "4", "3"], d:c => ({n:fmt(c.topics)})}
];
const PLANE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/></svg>';
function renderPasses(){
  const c = counts();
  $("#passes").innerHTML = GATES.map((g, i) => {
    const f = g.f(c);
    return `<a class="pass" data-k="${g.k}" href="${g.href}">
      <div class="pm">
        <div class="ptop"><span class="label">${esc(t("pass.label"))}</span><span class="cls">GATE ${g.gate}</span></div>
        <div class="proute">
          <div class="c"><b>SKY</b><span>${esc(t("pass.from"))}</span></div>
          <div class="pline">${PLANE}</div>
          <div class="c to"><b>${g.to}</b><span>${esc(t(`p.${g.k}.t`))}</span></div>
        </div>
        <p class="pdesc">${esc(t(`p.${g.k}.d`, g.d(c)))}</p>
        <div class="pfields">
          ${[1,2,3].map(n => `<div><span class="label">${esc(t(`p.${g.k}.f${n}`))}</span><b>${esc(f[n-1])}</b></div>`).join("")}
        </div>
      </div>
      <div class="ps">
        <div><span class="label">${esc(t("pass.gate"))}</span><div class="gate">${g.gate}${i+1}</div></div>
        <div><span class="label">${esc(t("pass.seat"))}</span><div class="seat">${g.seat}</div></div>
        <div class="barcode" aria-hidden="true"></div>
        <span class="board-cta">${esc(t("pass.board"))}<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>
      </div>
    </a>`;
  }).join("");
}

/* ═══════════════ 最近看過（沿用 viewer.js 的 hangar_recent） ═══════════════ */
function renderRecent(){
  let ids = [];
  try { ids = JSON.parse(store.get("hangar_recent") || "[]"); } catch (e) {}
  const items = ids.map(id => D.fleet.find(a => a.id === id)).filter(Boolean).slice(0, 8);
  $("#recentWrap").hidden = !items.length;
  $("#recent").innerHTML = items.map(a => `<a class="rc" href="viewer.html?model=${encodeURIComponent(a.id)}"><img src="${esc(a.thumb)}" alt="" loading="lazy">${esc(a.name)}</a>`).join("");
}

/* ═══════════════ 我的登機證夾（2026-11） ═══════════════
   讀各頁的收藏（機型 hangar_favs、機場 hangar_apt_favs、航空公司 hangar_airline_favs），每一筆做成一張小登機證，
   最新收藏的排在最前面；可依類別切換。其他分頁改了收藏時（storage 事件）即時更新。 */
const WALLET_KEYS = { fleet: "hangar_favs", airports: "hangar_apt_favs", airlines: "hangar_airline_favs" };
let walletTab = "all";
const readFavs = key => { try { const v = JSON.parse(store.get(key) || "[]"); return Array.isArray(v) ? v : []; } catch (e) { return []; } };
async function walletItems(){
  const out = [];
  readFavs(WALLET_KEYS.fleet).slice().reverse().forEach(id => {
    const a = D.fleet.find(x => x.id === id); if (!a) return;
    out.push({ k: "fleet", code: a.icao || id.toUpperCase(), name: a.name, sub: `${a.manufacturer} · ${field(a.category)}`, seat: a.seats || "—", href: `viewer.html?model=${encodeURIComponent(id)}` });
  });
  const aptIds = readFavs(WALLET_KEYS.airports).slice().reverse();
  if (aptIds.length) await ensureCodesPool();
  aptIds.forEach(id => {
    const a = (codesPool || []).find(x => x.id === id);
    out.push({ k: "airports", code: a ? aptCode(a) : id, name: a ? a.name : id, sub: a ? [aptCity(a), aptCountry(a)].filter(Boolean).join(" · ") : "", seat: id, href: `airports.html?icao=${encodeURIComponent(id)}` });
  });
  readFavs(WALLET_KEYS.airlines).slice().reverse().forEach(id => {
    const a = D.airlines.find(x => x.id === id); if (!a) return;
    out.push({ k: "airlines", code: a.iata || a.icao || id.toUpperCase(), name: airlineName(a), sub: [a.callsign, field(a.country)].filter(Boolean).join(" · "), seat: a.icao || "—", href: `airlines.html?id=${encodeURIComponent(id)}` });
  });
  return out;
}
async function renderWallet(){
  const all = await walletItems();
  const counts = { all: all.length, fleet: 0, airports: 0, airlines: 0 };
  all.forEach(x => counts[x.k]++);
  $("#walletTabs").innerHTML = ["all", "fleet", "airports", "airlines"].map(k =>
    `<button type="button" role="tab" aria-selected="${k === walletTab}" data-tab="${k}">${esc(t(k === "all" ? "tab.all" : "kind." + k))}<span>${counts[k]}</span></button>`).join("");
  const list = walletTab === "all" ? all : all.filter(x => x.k === walletTab);
  if (!list.length){
    $("#wallet").innerHTML = `<div class="wp wp-empty"><div class="wp-main"><span class="label">${esc(t("wallet.emptyK"))}</span><b>${esc(t("wallet.empty"))}</b><span class="wp-sub">${esc(t("wallet.how"))}</span></div><div class="wp-stub"><span class="label">GATE</span><b>—</b><div class="barcode" aria-hidden="true"></div></div></div>`;
    return;
  }
  $("#wallet").innerHTML = list.map(x => `<a class="wp" data-k="${x.k}" href="${x.href}">
      <div class="wp-main">
        <span class="label">BOARDING PASS · ${esc(t("kind." + x.k))}</span>
        <b>${esc(x.code)}</b>
        <span class="wp-name">${esc(x.name)}</span>
        <span class="wp-sub">${esc(x.sub)}</span>
      </div>
      <div class="wp-stub"><span class="label">${esc(t(x.k === "fleet" ? "wallet.seats" : "wallet.icao"))}</span><b>${esc(x.seat)}</b><div class="barcode" aria-hidden="true"></div></div>
    </a>`).join("");
}
$("#walletTabs").addEventListener("click", e => { const b = e.target.closest("[data-tab]"); if (!b) return; walletTab = b.dataset.tab; renderWallet(); });
window.addEventListener("storage", e => { if (Object.values(WALLET_KEYS).includes(e.key)) renderWallet(); });

/* ═══════════════ 熱門航點 chips ═══════════════ */
const CHIP_KEYS = [["RCTP","airports"],["RJTT","airports"],["A350","fleet"],["EVA","airlines"],["CAVOK","knowledge"],["V1","knowledge"]];
function renderChips(){
  const label = `<span class="label">${esc(t("chips.label"))}</span>`;
  const names = {RCTP:{zh:"桃園",en:"Taoyuan",ja:"桃園"},RJTT:{zh:"羽田",en:"Haneda",ja:"羽田"},A350:{zh:"空巴 A350",en:"Airbus A350",ja:"エアバス A350"},
    EVA:{zh:"長榮航空",en:"EVA Air",ja:"エバー航空"},CAVOK:{zh:"天氣良好",en:"Weather OK",ja:"好天"},V1:{zh:"起飛決斷速度",en:"Takeoff speeds",ja:"離陸決心速度"}};
  $("#chips").innerHTML = label + CHIP_KEYS.map(([q,s]) => `<button type="button" class="chip" data-q="${q}" data-s="${s}"><b>${q}</b>${esc(field(names[q]))}</button>`).join("");
}
$("#chips").addEventListener("click", e => {
  const b = e.target.closest(".chip"); if (!b) return;
  setScope(b.dataset.s); const q = $("#q"); q.value = b.dataset.q; q.focus(); runSearch();
});

/* ═══════════════ 全站搜尋 ═══════════════ */
let scope = "all", hits = [], active = -1;
function setPlaceholder(){ $("#q").placeholder = t(scope === "all" ? "search.ph" : `search.ph.${scope}`); }
function setScope(s){
  scope = s;
  document.querySelectorAll("#tabs button").forEach(b => b.setAttribute("aria-checked", String(b.dataset.scope === s)));
  setPlaceholder();
}
$("#tabs").addEventListener("click", e => { const b = e.target.closest("button"); if (!b) return; setScope(b.dataset.scope); $("#q").focus(); runSearch(); });
$("#tabs").addEventListener("keydown", e => {
  if (!["ArrowLeft","ArrowRight"].includes(e.key)) return;
  const bs = [...document.querySelectorAll("#tabs button")], i = bs.findIndex(b => b.dataset.scope === scope);
  const n = bs[(i + (e.key === "ArrowRight" ? 1 : bs.length - 1)) % bs.length]; setScope(n.dataset.scope); n.focus(); runSearch();
});
const norm = s => String(s || "").toLowerCase().replace(/[\s\-_/·．.]/g, "");
const wordStart = (raw, q) => String(raw || "").toLowerCase().split(/[\s\-_/·．.,:：（）()]+/).some(w => w && norm(w).startsWith(q));
function score(q, codes, names){
  let best = 0;
  for (const c of codes) { const v = norm(c); if (!v) continue; if (v === q) best = Math.max(best, 100); else if (v.startsWith(q)) best = Math.max(best, 80); }
  for (const n of names) {
    const v = norm(n); if (!v) continue;
    if (v.startsWith(q)) best = Math.max(best, 60);
    else if (wordStart(n, q)) best = Math.max(best, 55);
    else if (v.includes(q)) best = Math.max(best, 40);
  }
  return best;
}
async function ensureCodes(){
  if (D.codes) return D.codes;
  const raw = await getJSON("data/airport_codes.json", 138) || {};
  const byId = new Map();
  for (const [code, a] of Object.entries(raw)) {
    const e = byId.get(a.id) || {id:a.id, name:a.name, city:a.city, codes:new Set([a.id])};
    e.codes.add(code); byId.set(a.id, e);
  }
  D.codes = [...byId.values()];
  return D.codes;
}
function searchAll(q){
  const groups = [], want = k => scope === "all" || scope === k, cap = scope === "all" ? 4 : 10;
  const push = (k, list) => { const g = list.filter(x => x.s > 0).sort((a,b) => b.s - a.s).slice(0, cap).map(x => ({...x, k})); if (g.length) groups.push(g); };
  if (want("fleet")) push("fleet", D.fleet.map(a => ({s:score(q,[a.icao,a.id,a.name.replace(/^(Airbus|Boeing)\s*/,"")],[a.name,a.manufacturer]),
    code:a.icao || a.id.toUpperCase(), n:a.name, sub:`${a.manufacturer} · ${field(a.category)}`, href:`viewer.html?model=${encodeURIComponent(a.id)}`})));
  if (want("airports")) {
    const pop = new Map(POPULAR.map(p => [p.icao, p]));
    const list = (D.codes || POPULAR.map(p => ({id:p.icao, name:p.name.en, city:"", codes:new Set([p.icao,p.iata])}))).map(a => {
      const p = pop.get(a.id), local = p ? [p.name.zh, p.name.ja, p.name.en] : [];
      let s = score(q, [...a.codes], [a.name, a.city, ...local]); if (s && p) s += 5;
      return {s, code:[...a.codes].find(c => c.length === 3) || a.id, n:p ? field(p.name) : a.name, sub:`${a.id}${a.city ? " · " + a.city : ""}`, href:`airports.html?icao=${encodeURIComponent(a.id)}`};
    });
    push("airports", list);
  }
  if (want("airlines")) push("airlines", D.airlines.map(a => { const b = score(q,[a.icao,a.iata,a.callsign],[a.name,a.nameZh,a.nameJa]); return {s:b && a.tier ? b + 3 : b,
    code:a.iata || a.icao, n:airlineName(a), sub:`${a.icao || ""}${a.callsign ? " · " + a.callsign : ""} · ${field(a.country)}`, href:`airlines.html?id=${encodeURIComponent(a.id)}`}; }));
  if (want("knowledge")) push("knowledge", D.topics.map(k => ({s:score(q,[k.id],[k.name?.zh,k.name?.en,k.name?.ja]),
    code:k.id.replace(/-/g,"").toUpperCase().slice(0,6), n:field(k.name), sub:catName(k.category), href:`knowledge.html?topic=${encodeURIComponent(k.id)}`})));
  /* 最相關的類別排最前面，例如輸入 EVA 時航空公司優先於機場 */
  return groups.sort((a,b) => b[0].s - a[0].s).flat();
}
let searchToken = 0;
async function runSearch(){
  const qRaw = $("#q").value.trim(), q = norm(qRaw), box = $("#results"), my = ++searchToken;
  if (!q) return closeResults();
  if (!D.codes && (scope === "all" || scope === "airports")) {
    if (scope === "airports") { box.innerHTML = `<div class="rmsg">${esc(t("search.loading"))}</div>`; openResults(); }
    await ensureCodes(); if (my !== searchToken) return;
  }
  hits = searchAll(q); active = hits.length ? 0 : -1;
  if (!hits.length) { box.innerHTML = `<div class="rmsg">${esc(t("search.empty", {q:qRaw}))}</div>`; openResults(); return; }
  let html = "", last = "";
  hits.forEach((h, i) => {
    if (h.k !== last) { html += `<div class="rg">${esc(t("kind." + h.k))}</div>`; last = h.k; }
    html += `<a class="ri" role="option" id="opt${i}" data-i="${i}" href="${h.href}" aria-selected="${i === active}"><span class="code">${esc(h.code)}</span><span style="min-width:0"><span class="n">${esc(h.n)}</span><span class="s">${esc(h.sub)}</span></span><span class="k">${esc(t("kind." + h.k))}</span></a>`;
  });
  box.innerHTML = html + `<div class="rhint">${esc(t("search.hint"))}</div>`;
  openResults(); markActive();
}
function openResults(){ $("#results").hidden = false; $("#q").setAttribute("aria-expanded","true"); }
function closeResults(){ $("#results").hidden = true; $("#q").setAttribute("aria-expanded","false"); active = -1; }
function markActive(){
  document.querySelectorAll("#results .ri").forEach(el => el.setAttribute("aria-selected", String(+el.dataset.i === active)));
  const el = document.getElementById("opt" + active);
  if (el) { el.scrollIntoView({block:"nearest"}); $("#q").setAttribute("aria-activedescendant", el.id); }
}
let debounce;
$("#q").addEventListener("input", () => { clearTimeout(debounce); debounce = setTimeout(runSearch, 90); });
$("#q").addEventListener("focus", () => { if ($("#q").value.trim()) runSearch(); if (scope === "all" || scope === "airports") ensureCodes(); });
$("#q").addEventListener("keydown", e => {
  if (e.key === "ArrowDown" && hits.length) { e.preventDefault(); active = (active + 1) % hits.length; markActive(); }
  else if (e.key === "ArrowUp" && hits.length) { e.preventDefault(); active = (active - 1 + hits.length) % hits.length; markActive(); }
  else if (e.key === "Escape") { closeResults(); }
});
$("#results").addEventListener("mousemove", e => { const r = e.target.closest(".ri"); if (r && +r.dataset.i !== active) { active = +r.dataset.i; markActive(); } });
$("#booker").addEventListener("submit", async e => {
  e.preventDefault();
  if ($("#results").hidden) await runSearch();
  const h = hits[active] || hits[0]; if (h) go(h.href);
});
document.addEventListener("click", e => { if (!e.target.closest("#booker") && !e.target.closest(".chip")) closeResults(); });

/* ═══════════════ 首屏隨機航線＋航線規劃 ═══════════════
   - 首屏右上角：每飛完一趟，從大型機場清單（data/route_airports.json，1,172 座有 IATA 的
     large_airport）隨機挑一組起降機場（距離 800–15,500 km）。清單載入前先用內建的熱門機場。
   - 動畫由 js/routemap.js 負責：虛線航線從起點畫到終點 → 飛機飛過處變實線 → 抵達後換下一趟。
   - 點這個區塊開啟「航線規劃」：可自己搜尋起降機場（大型機場＋全球機場代碼表）、交換、隨機、熱門航線，
     並顯示距離、預估航時、巡航高度、起始航向、航程分類與最高緯度。 */
const toApt = r => ({ id:r[0], iata:r[1], name:r[2], city:r[3], country:r[4], lat:r[5], lon:r[6], cityZh:r[7], cityJa:r[8] });
const POP_APTS = [TPE, ...POPULAR].map(p => ({ id:p.icao, iata:p.iata, name:p.name ? p.name.en : "Taiwan Taoyuan International Airport",
  city:p.name ? p.name.en : "Taoyuan", country:"", lat:p.lat, lon:p.lon,
  cityZh:p.name ? p.name.zh : "臺灣桃園", cityJa:p.name ? p.name.ja : "台湾桃園" }));
let routePool = POP_APTS, codesPool = null, countryNames = null;
const aptCity = a => (lang === "zh" && a.cityZh) || (lang === "ja" && a.cityJa) || a.city || a.name;
const aptCode = a => a.iata || a.id;
const aptCountry = a => (countryNames && countryNames[a.country] && (countryNames[a.country][lang] || countryNames[a.country].en)) || a.country || "";
const mapApt = a => ({ lat:a.lat, lon:a.lon, code:aptCode(a), label:aptCity(a) });
function pickPair(pool = routePool){
  for (let i = 0; i < 60; i++){
    const a = pool[Math.floor(Math.random() * pool.length)], b = pool[Math.floor(Math.random() * pool.length)];
    if (a === b) continue;
    const km = gcKm(a, b);
    if (km >= 800 && km <= 15500) return { a, b };
  }
  return { a: POP_APTS[0], b: POP_APTS[1] };
}
async function loadRoutePool(){
  const [r, c] = await Promise.all([getJSON("data/route_airports.json", 1), getJSON("data/countries.json", 138)]);
  if (r && r.airports && r.airports.length) routePool = r.airports.map(toApt);
  if (c) countryNames = c;
}

/* 飛行速度：以「每 1 小時航程播放幾秒」表示，航線越長飛越久，飛到終點才換下一條。
   設定存在 localStorage（hangar_route_speed），首屏與航線規劃共用。 */
const SPEEDS = [ { k:"xslow", sec:8 }, { k:"slow", sec:5 }, { k:"normal", sec:3 }, { k:"fast", sec:1.5 }, { k:"xfast", sec:.75 } ];
let speedKey = (() => { const v = store.get("hangar_route_speed"); return SPEEDS.some(x => x.k === v) ? v : "normal"; })();
const speedSec = () => SPEEDS.find(x => x.k === speedKey).sec;
const cruiseHours = km => km / 830;
const flyMs = km => Math.max(3000, Math.min(150000, cruiseHours(km) * speedSec() * 1000));
const fmtSec = ms => { const s = Math.round(ms / 1000); return s >= 60 ? t("rp.minsec", { m: Math.floor(s / 60), s: s % 60 }) : t("rp.sec", { s }); };

/* 套用到首頁：在航線規劃按「套用到首頁」後，首屏改為重複飛這一條（存在 localStorage.hangar_route_pin，
   重新整理後仍保留），直到按「恢復隨機」。只存畫面需要的欄位，所以小機場也能套用。 */
const PIN_KEY = "hangar_route_pin";
const slimApt = a => ({ id:a.id, iata:a.iata || "", name:a.name || "", city:a.city || "", country:a.country || "", lat:a.lat, lon:a.lon, cityZh:a.cityZh || "", cityJa:a.cityJa || "" });
let pinned = (() => { try { const v = JSON.parse(store.get(PIN_KEY) || "null"); return v && v.a && v.b && isFinite(v.a.lat) && isFinite(v.b.lat) ? v : null; } catch (e) { return null; } })();
const nextPair = () => pinned ? { a: pinned.a, b: pinned.b } : pickPair();
const samePair = (p, q) => !!(p && q && p.a.id === q.a.id && p.b.id === q.b.id);

/* 首屏 */
const heroMap = RouteMap.create($("#heroMap"));
let heroPair = nextPair(), heroPaused = false, heroResume = null;
function updatePinUI(){
  $("#heroBadge").textContent = t(pinned ? "route.badge.pinned" : "route.badge");
  $("#heroUnpin").hidden = !pinned;
  $("#routeCap").textContent = t(pinned ? "hud.cap.pinned" : "hud.cap");
}
function setPinned(pair){
  pinned = pair ? { a: slimApt(pair.a), b: slimApt(pair.b) } : null;
  if (pinned) store.set(PIN_KEY, JSON.stringify(pinned)); else { try { localStorage.removeItem(PIN_KEY); } catch (e) {} }
  updatePinUI();
}
function updateHeroText(){
  if (!heroPair) return;
  updatePinUI();
  const { a, b } = heroPair, km = gcKm(a, b);
  $("#hudRoute").textContent = `${aptCode(a)} → ${aptCode(b)}`;
  $("#hudDist").textContent = `${fmt(Math.round(km))} km`;
  $("#hudTime").textContent = blockTime(km);
  $("#hudFl").textContent = cruiseFl(km);
  $("#routeCard").setAttribute("aria-label", `${t("route.open")}: ${aptCity(a)} → ${aptCity(b)}`);
}
const updateRouteText = updateHeroText;   // renderAll() 換語言時呼叫
async function heroLoop(){
  for (;;){
    if (heroPaused) await new Promise(r => { heroResume = r; });
    const done = await heroMap.play(mapApt(heroPair.a), mapApt(heroPair.b), updateHeroText, { flyMs: flyMs(gcKm(heroPair.a, heroPair.b)) });
    if (done && !heroPaused) heroPair = nextPair();
  }
}
heroLoop();
$("#heroUnpin").addEventListener("click", e => {
  e.stopPropagation();          // 不要同時打開航線規劃
  setPinned(null);
  heroPair = pickPair(); heroMap.stop();   // 立刻換成隨機航線
});
$("#heroUnpin").addEventListener("keydown", e => e.stopPropagation());
const routePoolReady = new Promise(res => (window.requestIdleCallback || (fn => setTimeout(fn, 1500)))(() => loadRoutePool().then(res, res)));

/* 航線規劃 */
const RP_PRESETS = [["RCTP","RJTT"],["RCTP","KLAX"],["EGLL","KJFK"],["WSSS","YSSY"],["OMDB","EGLL"],["RJAA","LFPG"],["KJFK","VHHH"]];
let rpMap = null, rpA = null, rpB = null, rpOpener = null;
const findApt = id => routePool.find(a => a.id === id) || POP_APTS.find(a => a.id === id) || (codesPool && codesPool.find(a => a.id === id));
async function ensureCodesPool(){
  if (codesPool) return codesPool;
  const [raw] = await Promise.all([getJSON("data/airport_codes.json", 138), routePoolReady]);
  const byId = new Map(routePool.map(a => [a.id, { ...a }]));
  // 代碼表裡同一座機場會以 IATA、ICAO 各出現一次：以 id 合併，3 碼代碼補成 IATA
  for (const [code, a] of Object.entries(raw || {})){
    if (a.lat == null) continue;
    let e = byId.get(a.id);
    if (!e) { e = { id:a.id, iata:"", name:a.name, city:a.city || "", country:"", lat:a.lat, lon:a.lon, small:true }; byId.set(a.id, e); }
    if (code.length === 3 && !e.iata) e.iata = code;
  }
  // 熱門機場另有中日文全名（例如「羽田」「成田」），加進搜尋別名
  POP_APTS.forEach(p => { const e = byId.get(p.id); if (e) e.alias = [p.cityZh, p.cityJa, p.city]; });
  codesPool = [...byId.values()];
  return codesPool;
}
function aptSearch(q){
  const nq = norm(q);
  if (!nq) return [];
  const list = codesPool || routePool;
  return list.map(a => {
    let sc = score(nq, [a.iata, a.id], [a.name, a.city, a.cityZh, a.cityJa, ...(a.alias || [])]);
    if (sc && !a.small) sc += 6;
    return { a, sc };
  }).filter(x => x.sc > 0).sort((x, y) => y.sc - x.sc).slice(0, 8).map(x => x.a);
}
function rpLabel(a){ return a ? `${aptCode(a)} · ${aptCity(a)}` : ""; }
function compass(deg){ return t("rp.dir." + ["N","NE","E","SE","S","SW","W","NW"][Math.round(deg / 45) % 8]); }
function renderRpInfo(){
  const a = rpA, b = rpB;
  $("#rpFrom").value = rpLabel(a); $("#rpTo").value = rpLabel(b);
  if (!a || !b) return;
  const km = gcKm(a, b), course = RouteMap.bearing(a, b);
  const pts = RouteMap.gcPoints(a, b, 96);
  const top = pts.reduce((m, p) => Math.abs(p.lat) > Math.abs(m) ? p.lat : m, 0);
  const kind = km < 1500 ? "short" : km < 4000 ? "medium" : km < 11000 ? "long" : "ultra";
  $("#rpFromCode").textContent = aptCode(a); $("#rpToCode").textContent = aptCode(b);
  $("#rpFromName").textContent = [a.name, [aptCity(a), aptCountry(a)].filter(Boolean).join(", ")].filter(Boolean).join(" · ");
  $("#rpToName").textContent = [b.name, [aptCity(b), aptCountry(b)].filter(Boolean).join(", ")].filter(Boolean).join(" · ");
  const rows = [
    ["rp.dist", `${fmt(Math.round(km))} km`, `${fmt(Math.round(km / 1.852))} nm · ${fmt(Math.round(km / 1.609))} mi`],
    ["rp.time", blockTime(km), ""],
    ["rp.fl", cruiseFl(km), ""],
    ["rp.course", `${Math.round(course).toString().padStart(3, "0")}°`, compass(course)],
    ["rp.kind", t("rp.kind." + kind), { short: "< 1,500 km", medium: "1,500–4,000 km", long: "4,000–11,000 km", ultra: "> 11,000 km" }[kind]],
    ["rp.maxlat", `${Math.abs(top).toFixed(1)}°${top >= 0 ? "N" : "S"}`, ""]
  ];
  renderSpeed(km);
  $("#rpStats").innerHTML = rows.map(([k, v, sub]) => `<div><dt>${esc(t(k))}</dt><dd><b>${esc(v)}</b>${sub ? `<span>${esc(sub)}</span>` : ""}</dd></div>`).join("");
  const arrow = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
  const applied = samePair(pinned, { a, b });
  $("#rpApplyBar").innerHTML = `<button type="button" class="btn pri rp-apply" id="rpApply"${applied ? " disabled" : ""}>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>${esc(t(applied ? "rp.applied" : "rp.apply"))}</button>
    ${pinned ? `<button type="button" class="btn" id="rpUnpin">${esc(t("route.unpin"))}</button>` : ""}
    <p class="rp-apply-hint">${esc(t(applied ? "rp.applied.hint" : "rp.apply.hint"))}</p>`;
  $("#rpApply").addEventListener("click", () => {
    setPinned({ a: rpA, b: rpB });
    heroPair = { a: pinned.a, b: pinned.b };
    closePlanner();               // 關閉後首屏立刻從起點飛這條航線
  });
  if ($("#rpUnpin")) $("#rpUnpin").addEventListener("click", () => { setPinned(null); heroPair = pickPair(); renderRpInfo(); });
  $("#rpActions").innerHTML = `<button type="button" class="btn" id="rpReplay">${esc(t("rp.replay"))}</button>
    <a class="btn" href="airports.html?icao=${encodeURIComponent(a.id)}">${esc(t("rp.fromApt"))} ${arrow}</a>
    <a class="btn" href="airports.html?icao=${encodeURIComponent(b.id)}">${esc(t("rp.toApt"))} ${arrow}</a>
    <a class="btn" href="distance.html?from=${encodeURIComponent(a.id)}&to=${encodeURIComponent(b.id)}">${esc(t("rp.calc"))} ${arrow}</a>`;
  $("#rpReplay").addEventListener("click", rpPlay);
}
async function rpPlay(){
  if (!rpA || !rpB || !rpMap) return;
  const done = await rpMap.play(mapApt(rpA), mapApt(rpB), null, { flyMs: flyMs(gcKm(rpA, rpB)), holdMs: 600 });
  if (done) rpMap.show(mapApt(rpA), mapApt(rpB));   // 播完停在抵達畫面，不自動換航線
}
function rpSet(a, b, play = true){
  if (a && b && a.id === b.id) { $("#rpStats").innerHTML = `<div class="rp-warn">${esc(t("rp.same"))}</div>`; return; }
  rpA = a || rpA; rpB = b || rpB;
  renderRpInfo();
  if (play) rpPlay();
}
function renderSpeed(km){
  $("#rpSpeedOpts").innerHTML = SPEEDS.map(x => `<button type="button" role="radio" aria-checked="${x.k === speedKey}" data-speed="${x.k}">${esc(t("rp.speed." + x.k))}</button>`).join("");
  $("#rpSpeedHint").textContent = t("rp.speed.hint", { s: String(speedSec()), t: fmtSec(flyMs(km)) });
}
$("#rpSpeedOpts").addEventListener("click", e => {
  const b = e.target.closest("[data-speed]"); if (!b) return;
  speedKey = b.dataset.speed; store.set("hangar_route_speed", speedKey);
  if (rpA && rpB) { renderSpeed(gcKm(rpA, rpB)); rpPlay(); }   // 立刻用新速度重飛一次
});
$("#rpSpeedOpts").addEventListener("keydown", e => {
  if (!["ArrowLeft", "ArrowRight"].includes(e.key)) return;
  const i = SPEEDS.findIndex(x => x.k === speedKey), n = SPEEDS[(i + (e.key === "ArrowRight" ? 1 : SPEEDS.length - 1)) % SPEEDS.length];
  speedKey = n.k; store.set("hangar_route_speed", speedKey);
  if (rpA && rpB) { renderSpeed(gcKm(rpA, rpB)); rpPlay(); }
  $(`#rpSpeedOpts [data-speed="${n.k}"]`).focus();
});
function renderPresets(){
  $("#rpPresets").innerHTML = `<span class="label">${esc(t("rp.presets"))}</span>` + RP_PRESETS.map(([x, y]) => {
    const a = findApt(x), b = findApt(y);
    return a && b ? `<button type="button" class="chip-lite" data-a="${x}" data-b="${y}">${esc(aptCode(a))} → ${esc(aptCode(b))}</button>` : "";
  }).join("");
}
$("#rpPresets").addEventListener("click", e => { const c = e.target.closest("[data-a]"); if (c) rpSet(findApt(c.dataset.a), findApt(c.dataset.b)); });
function openPlanner(){
  rpOpener = document.activeElement;
  heroPaused = true; heroMap.stop();
  $("#planner").hidden = false;
  document.body.classList.add("rp-open");
  if (!rpMap) rpMap = RouteMap.create($("#rpMap"), { gap: 10, bulge: .1, minSpan: 30 });
  renderPresets();
  rpSet(heroPair.a, heroPair.b);
  ensureCodesPool();
  // 觸控裝置不自動聚焦輸入框（否則一打開就跳出鍵盤），改聚焦對話框本身
  setTimeout(() => (matchMedia("(pointer: fine)").matches ? $("#rpFrom") : $(".rp-sheet")).focus({ preventScroll: true }), 50);
}
function closePlanner(){
  $("#planner").hidden = true;
  document.body.classList.remove("rp-open");
  if (rpMap) rpMap.stop();
  heroPaused = false;
  if (heroResume) { const r = heroResume; heroResume = null; r(); }
  if (rpOpener && rpOpener.focus) rpOpener.focus({ preventScroll: true });
}
$("#routeCard").addEventListener("click", openPlanner);
$("#routeCard").addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openPlanner(); } });
$("#rpClose").addEventListener("click", closePlanner);
$("#planner").addEventListener("click", e => { if (e.target.id === "planner") closePlanner(); });
document.addEventListener("keydown", e => { if (e.key === "Escape" && !$("#planner").hidden && !document.querySelector(".rp-list:not([hidden])")) closePlanner(); });
$("#rpSwap").addEventListener("click", () => { if (rpA && rpB) rpSet(rpB, rpA); });
$("#rpRandom").addEventListener("click", () => { const p = pickPair(); rpSet(p.a, p.b); });

/* 機場搜尋選單（出發／抵達共用；↑↓ Enter Esc） */
function wirePicker(input, list, which){
  let items = [], act = -1;
  const close = () => { list.hidden = true; input.setAttribute("aria-expanded", "false"); act = -1; };
  const mark = () => list.querySelectorAll(".rp-opt").forEach((el, i) => {
    el.setAttribute("aria-selected", String(i === act));
    if (i === act) { el.scrollIntoView({ block: "nearest" }); input.setAttribute("aria-activedescendant", el.id); }
  });
  const choose = i => { const a = items[i]; if (!a) return; close(); which === "from" ? rpSet(a, null) : rpSet(null, a); input.blur(); };
  const render = async () => {
    const q = input.value.trim();
    if (!q) { close(); return; }
    if (!codesPool) { list.innerHTML = `<div class="rp-msg">${esc(t("rp.loading"))}</div>`; list.hidden = false; await ensureCodesPool(); if (input.value.trim() !== q) return; }
    items = aptSearch(q); act = items.length ? 0 : -1;
    list.innerHTML = items.length ? items.map((a, i) => `<div class="rp-opt" role="option" id="${input.id}-o${i}" data-i="${i}">
        <b>${esc(aptCode(a))}</b><span><span class="n">${esc(a.name)}</span><span class="s">${esc([a.id, aptCity(a), aptCountry(a)].filter(Boolean).join(" · "))}</span></span></div>`).join("")
      : `<div class="rp-msg">${esc(t("rp.empty", { q }))}</div>`;
    list.hidden = false; input.setAttribute("aria-expanded", "true"); mark();
  };
  let tm;
  input.addEventListener("focus", () => input.select());
  input.addEventListener("input", () => { clearTimeout(tm); tm = setTimeout(render, 80); });
  input.addEventListener("keydown", e => {
    if (list.hidden) return;
    if (e.key === "ArrowDown" && items.length) { e.preventDefault(); act = (act + 1) % items.length; mark(); }
    else if (e.key === "ArrowUp" && items.length) { e.preventDefault(); act = (act - 1 + items.length) % items.length; mark(); }
    else if (e.key === "Enter") { e.preventDefault(); choose(act < 0 ? 0 : act); }
    else if (e.key === "Escape") { e.preventDefault(); e.stopPropagation(); close(); input.value = rpLabel(which === "from" ? rpA : rpB); }
  });
  list.addEventListener("mousedown", e => { const o = e.target.closest(".rp-opt"); if (o) { e.preventDefault(); choose(+o.dataset.i); } });
  input.addEventListener("blur", () => setTimeout(() => { if (!list.hidden) { close(); input.value = rpLabel(which === "from" ? rpA : rpB); } }, 150));
}
wirePicker($("#rpFrom"), $("#rpFromList"), "from");
wirePicker($("#rpTo"), $("#rpToList"), "to");
document.addEventListener("langchange", () => { if (!$("#planner").hidden) { renderPresets(); renderRpInfo(); } });

/* ═══════════════ 出發看板 ═══════════════ */
const POOL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
let boardSeed = Number(new Date().toISOString().slice(0,10).replace(/-/g,""));
let flights = [];
function buildFlights(){
  const r = rng(boardSeed), pick = arr => arr[Math.floor(r() * arr.length)];
  const used = new Set(), uniq = (arr, key) => { for (let i = 0; i < 20; i++) { const x = pick(arr); if (x && !used.has(key(x))) { used.add(key(x)); return x; } } return pick(arr); };
  const withModel = D.fleet.filter(a => !/nomodel/.test(a.thumb || ""));
  const carriers = D.airlines.filter(a => ["mainline","lcc","cargo","regional"].includes(a.tier));
  const out = [];
  const ac = a => a && out.push({k:"fleet", code:a.icao || a.id.toUpperCase(), n:a.name, sub:`${a.manufacturer} · ${field(a.category)}`,
    gate:"A", st:/nomodel/.test(a.thumb||"") ? "spec" : "3d", href:`viewer.html?model=${encodeURIComponent(a.id)}`});
  const ap = p => out.push({k:"airports", code:p.iata, n:field(p.name), sub:t("sub.airport",{icao:p.icao, d:fmt(Math.round(gcKm(TPE,p)))}),
    gate:"B", st:"ontime", href:`airports.html?icao=${p.icao}`});
  const al = a => a && out.push({k:"airlines", code:`${a.iata || a.icao}${100 + Math.floor(r()*900)}`, n:airlineName(a), sub:t("sub.airline",{country:field(a.country), n:fmt(a.fleetTotal || 0)}),
    gate:"C", st:"boarding", href:`airlines.html?id=${encodeURIComponent(a.id)}`});
  const kn = k => k && out.push({k:"knowledge", code:k.id.replace(/-/g,"").toUpperCase().slice(0,7), n:field(k.name), sub:catName(k.category),
    gate:"D", st:"new", href:`knowledge.html?topic=${encodeURIComponent(k.id)}`});
  const pops = POPULAR.filter(p => p.icao !== "RCSS");
  ac(uniq(withModel.length ? withModel : D.fleet, a => a.id)); ap(uniq(pops, p => p.icao)); al(uniq(carriers, a => a.id));
  kn(uniq(D.topics, k => k.id)); ac(uniq(D.fleet, a => a.id)); ap(uniq(pops, p => p.icao));
  const now = zoneNow(); let m = Math.ceil((now.h*60 + now.m + 6) / 5) * 5;
  out.forEach(f => { f.time = `${String(Math.floor(m/60)%24).padStart(2,"0")}:${String(m%60).padStart(2,"0")}`; f.gate += 1 + Math.floor(r()*24); m += 5 + Math.floor(r()*3)*5; });
  flights = out;
}
function tilesHTML(code){ return [...code.padEnd(7," ").slice(0,7)].map(ch => `<span class="tile"><span>${ch === " " ? "" : esc(ch)}</span></span>`).join(""); }
function flapIn(container, code){
  const finals = [...code.padEnd(7," ").slice(0,7)];
  container.querySelectorAll(".tile").forEach((tile, i) => {
    const span = tile.firstChild; let n = 0; const max = 4 + i * 2 + Math.floor(Math.random()*3);
    const tick = () => {
      tile.classList.remove("flip"); void tile.offsetWidth; tile.classList.add("flip");
      if (n++ >= max) { span.textContent = finals[i] === " " ? "" : finals[i]; return; }
      span.textContent = finals[i] === " " ? "" : POOL[Math.floor(Math.random() * POOL.length)];
      setTimeout(tick, 55);
    };
    tick();
  });
}
function renderBoard(animate){
  if (!flights.length) buildFlights();
  $("#rows").innerHTML = flights.map(f => `<a class="brow" href="${f.href}" data-name="${esc(f.n)}">
      <span class="btime">${f.time}</span>
      <span class="tiles" aria-label="${esc(f.code)}">${tilesHTML(animate ? "" : f.code)}</span>
      <span class="bdest"><b>${esc(f.n)}</b><span>${esc(t("kind." + f.k))} · ${esc(f.sub)}</span></span>
      <span class="bgate">${f.gate}</span>
      <span class="bstat ${f.st === "3d" ? "go3d" : f.st}">${esc(t("st." + f.st))}</span>
    </a>`).join("");
  if (animate) document.querySelectorAll("#rows .tiles").forEach((el, i) => setTimeout(() => flapIn(el, flights[i].code), i * 70));
}
$("#shuffle").addEventListener("click", () => { boardSeed = (boardSeed * 31 + 7) % 2147483647; buildFlights(); renderBoard(true); });
// 看板時鐘、班次時間、機長問候都跟著 js/skytime.js 選的時區（預設裝置時區）
const zoneNow = () => (typeof SkyTime !== "undefined" ? SkyTime.parts() : (d => ({ h: d.getHours(), m: d.getMinutes() }))(new Date()));
function tickClock(){ const z = zoneNow(); $("#clock").textContent = `${String(z.h).padStart(2,"0")}:${String(z.m).padStart(2,"0")}`; }
tickClock(); setInterval(tickClock, 15000);
document.addEventListener("tzchange", () => { tickClock(); flights = []; renderBoard(false); renderPA(); });

/* ═══════════════ 機長廣播 ═══════════════ */
let paIdx = -1;
const PA_FALLBACK = [{id:"cavok", category:"weather", name:{zh:"CAVOK",en:"CAVOK",ja:"CAVOK"},
  summary:{zh:"天氣報告中的 CAVOK 代表能見度 10 公里以上、沒有影響飛航的雲與重要天氣。",en:"CAVOK in a weather report means visibility of 10 km or more with no significant cloud or weather.",ja:"CAVOK は視程 10 km 以上で、運航に影響する雲や顕著な気象がないことを示す。"},
  fact:{zh:"讀作「卡夫 OK」，是 Ceiling And Visibility OK 的縮寫。",en:"It stands for Ceiling And Visibility OK.",ja:"Ceiling And Visibility OK の略。"}}];
function renderPA(){
  const list = D.topics.length ? D.topics : PA_FALLBACK;
  if (paIdx < 0) paIdx = Math.floor(rng(boardSeed + 17)() * list.length);
  const k = list[paIdx % list.length], h = zoneNow().h;
  $("#paGreet").textContent = [t(h < 11 ? "pa.morning" : h < 18 ? "pa.afternoon" : "pa.evening"), t("pa.lead")].join(lang === "en" ? " " : "");
  $("#paTopic").textContent = field(k.name);
  $("#paSum").textContent = field(k.summary);
  const fact = field(k.fact);
  $("#paFact").hidden = !fact;
  $("#paFact").innerHTML = `<b>${esc(t("pa.fact"))}</b>${esc(fact)}`;
  $("#paOpen").href = list === D.topics ? `knowledge.html?topic=${encodeURIComponent(k.id)}` : "knowledge.html";
}
$("#paNext").addEventListener("click", () => { paIdx++; swapPA(); });

/* ═══════════════ 自動輪換：今日出發、機長廣播（2026-11） ═══════════════
   每個區塊各自一個「手動／每 N 秒自動」選單（站內自訂選單，不用原生 select），選擇存在 localStorage
   （hangar_board_auto、hangar_pa_auto，單位秒，0 = 手動）。自動時區塊頂端有倒數細條；
   滑鼠停在區塊上、鍵盤焦點在區塊內、選單開著或分頁在背景時暫停，手動按「換一批／換一則」會重新倒數。 */
const AUTO_PRESETS = [0, 10, 20, 30, 60, 180, 300, 600];
const autoClosers = [];
const fmtDur = sec => sec < 60 ? t("auto.sec", { n: sec }) : sec % 60 ? t("auto.minSec", { m: Math.floor(sec / 60), s: sec % 60 }) : t("auto.min", { n: sec / 60 });
function makeAuto({ host, card, key, run }){
  let sec = Math.max(0, parseInt(store.get(key), 10) || 0), left = sec, last = performance.now(), hover = false;
  host.innerHTML = `<button type="button" class="auto-btn" aria-haspopup="menu" aria-expanded="false"><span class="auto-ico" aria-hidden="true"></span><span class="auto-lbl"></span></button>
    <div class="auto-menu" role="menu" hidden></div>`;
  const btn = host.querySelector(".auto-btn"), menu = host.querySelector(".auto-menu");
  const bar = document.createElement("div"); bar.className = "auto-bar"; bar.innerHTML = "<i></i>"; card.prepend(bar);
  const paint = () => {
    host.classList.toggle("on", sec > 0); card.classList.toggle("auto-on", sec > 0);
    host.querySelector(".auto-lbl").textContent = sec ? t("auto.every", { t: fmtDur(sec) }) : t("auto.manual");
    btn.title = sec ? t("auto.hint") : t("auto.title");
  };
  const renderMenu = () => {
    const custom = !AUTO_PRESETS.includes(sec);
    menu.innerHTML = `<div class="auto-mh">${esc(t("auto.title"))}</div>` + AUTO_PRESETS.map(v =>
      `<button type="button" role="menuitemradio" aria-checked="${v === sec}" data-v="${v}">${esc(v ? fmtDur(v) : t("auto.manual"))}</button>`).join("") +
      `<label class="auto-custom${custom ? " on" : ""}"><span>${esc(t("auto.custom"))}</span><input type="number" min="5" max="3600" step="5" inputmode="numeric" value="${custom ? sec : ""}" placeholder="45"><span>${esc(t("auto.unit"))}</span><button type="button" class="auto-ok">OK</button></label>`;
  };
  const set = v => { sec = Math.max(0, Math.min(3600, v | 0)); if (sec && sec < 5) sec = 5; store.set(key, String(sec)); left = sec; paint(); close(); };
  // 選單預設對齊按鈕右緣；窄螢幕若超出畫面左右邊界就改貼另一邊，避免撐寬頁面
  const place = () => {
    menu.style.left = ""; menu.style.right = "";
    const r = menu.getBoundingClientRect(), vw = document.documentElement.clientWidth;
    if (r.left < 8) { menu.style.right = "auto"; menu.style.left = `${Math.min(0, 8 - host.getBoundingClientRect().left)}px`; }
    else if (r.right > vw - 8) { menu.style.right = `${r.right - vw + 8}px`; }
  };
  const open = () => { autoClosers.forEach(c => c !== close && c()); renderMenu(); menu.hidden = false; place(); btn.setAttribute("aria-expanded", "true"); (menu.querySelector('[aria-checked="true"]') || menu.querySelector("button")).focus(); };
  const close = () => { if (menu.hidden) return; menu.hidden = true; btn.setAttribute("aria-expanded", "false"); };
  autoClosers.push(close);
  btn.addEventListener("click", e => { e.stopPropagation(); menu.hidden ? open() : (close(), btn.focus()); });
  menu.addEventListener("click", e => {
    e.stopPropagation();
    const b = e.target.closest("button[data-v]"); if (b) { set(+b.dataset.v); btn.focus(); return; }
    if (e.target.closest(".auto-ok")) { const v = +menu.querySelector("input").value; if (v > 0) { set(v); btn.focus(); } }
  });
  menu.addEventListener("keydown", e => {
    const items = [...menu.querySelectorAll("button[data-v], input")], i = items.indexOf(document.activeElement);
    if (e.key === "Escape") { e.preventDefault(); close(); btn.focus(); }
    else if (e.key === "ArrowDown" || e.key === "ArrowUp") { e.preventDefault(); items[(i + (e.key === "ArrowDown" ? 1 : -1) + items.length) % items.length].focus(); }
    else if (e.key === "Enter" && e.target.tagName === "INPUT") { e.preventDefault(); const v = +e.target.value; if (v > 0) { set(v); btn.focus(); } }
  });
  document.addEventListener("click", e => { if (!host.contains(e.target)) close(); });
  card.addEventListener("pointerenter", () => hover = true);
  card.addEventListener("pointerleave", () => hover = false);
  setInterval(() => {
    const now = performance.now(), dt = (now - last) / 1000; last = now;
    const f = document.activeElement, paused = !sec || hover || !menu.hidden || document.hidden || (card.contains(f) && !host.contains(f));
    card.classList.toggle("auto-paused", !!sec && paused);
    if (!sec) { bar.firstChild.style.transform = "scaleX(0)"; return; }
    if (!paused) left -= dt;
    if (left <= 0) { left = sec; run(); }
    bar.firstChild.style.transform = `scaleX(${Math.min(1, Math.max(0, 1 - left / sec))})`;
  }, 200);
  paint();
  document.addEventListener("langchange", () => { paint(); if (!menu.hidden) renderMenu(); });
  return { reset: () => { left = sec; } };
}
// 自動換的時候用隨機種子（手動「換一批」維持原本的種子序列）
const boardAuto = makeAuto({ host: $("#boardAuto"), card: $(".board"), key: "hangar_board_auto",
  run: () => { boardSeed = Math.floor(Math.random() * 2147483646) + 1; buildFlights(); renderBoard(true); } });
const paAuto = makeAuto({ host: $("#paAuto"), card: $(".pa"), key: "hangar_pa_auto",
  run: () => { const n = (D.topics.length || 1); if (n > 1) paIdx = (paIdx + 1 + Math.floor(Math.random() * (n - 1))) % n; swapPA(); } });
$("#shuffle").addEventListener("click", () => boardAuto.reset());
$("#paNext").addEventListener("click", () => paAuto.reset());
function swapPA(){
  const pa = $(".pa"); pa.classList.remove("pa-swap"); void pa.offsetWidth;
  renderPA(); pa.classList.add("pa-swap");
}

/* ═══════════════ METAR 頁尾 ═══════════════ */
function renderMetar(){
  const c = counts(), d = new Date();
  const z = `${String(d.getUTCDate()).padStart(2,"0")}${String(d.getUTCHours()).padStart(2,"0")}${String(d.getUTCMinutes()).padStart(2,"0")}Z`;
  $("#metar").textContent = `METAR SKYA ${z} AC${c.aircraft}/${c.models}3D AP${c.airports} AL${c.airlines} KN${c.topics} CAVOK Q1013 NOSIG`;
  $("#metarDecode").textContent = t("foot.decode", {a:fmt(c.aircraft), m:fmt(c.models), p:fmt(c.airports), l:fmt(c.airlines), k:fmt(c.topics)});
}

/* ═══════════════ 語言、主題 ═══════════════ */
$("#lang").addEventListener("click", e => { const b = e.target.closest("button"); if (b) I18N.set(b.dataset.lang); });
document.addEventListener("langchange", () => { flights = []; renderAll(); });
$("#theme").addEventListener("click", () => window.HangarTheme.toggle());
function go(href){ location.href = href; }

/* ═══════════════ 啟動 ═══════════════ */
renderAll();
(async () => {
  const [fleet, airlines, count, knowledge] = await Promise.all([
    getJSON("data/fleet.json", 182), getJSON("data/airlines.json", 139),
    getJSON("data/airport_count.json", 138), getJSON("data/knowledge.json", 192)
  ]);
  if (fleet) D.fleet = fleet.aircraft || [];
  if (airlines) D.airlines = airlines.airlines || [];
  if (count) D.airportCount = count.count;
  if (knowledge) {
    const ids = new Set(knowledge.topics.map(k => k.id)); D.topics = knowledge.topics.slice();
    try { JSON.parse(store.get("hangar_knowledge_custom") || "[]").forEach(k => { if (k && k.id && !ids.has(k.id)) { ids.add(k.id); D.topics.push(k); } }); } catch (e) {}
  }
  flights = []; paIdx = -1;
  renderAll();
})();
