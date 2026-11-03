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
const REDUCED = matchMedia("(prefers-reduced-motion: reduce)").matches;
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
function renderAll(){ applyStatic(); renderChips(); renderPasses(); renderRecent(); renderBoard(false); renderPA(); renderMetar(); updateRouteText(); }

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

/* ═══════════════ 首屏航線示意 ═══════════════ */
const track = $("#track"), flown = $("#flown"), plane = $("#plane");
const LEN = track.getTotalLength();
flown.style.strokeDasharray = `${LEN} ${LEN}`;
let destIdx = 0;
function updateRouteText(){
  const d = POPULAR[destIdx], km = gcKm(TPE, d);
  $("#destCode").textContent = d.iata; $("#destIcao").textContent = d.icao;
  $("#hudDest").textContent = field(d.name);
  $("#hudDist").textContent = `${fmt(Math.round(km))} km`;
  $("#hudTime").textContent = blockTime(km);
  $("#hudFl").textContent = cruiseFl(km);
  $("#routeCap").textContent = t("hud.cap", {name: field(d.name)});
}
function placePlane(p){
  const L = LEN * p, a = track.getPointAtLength(L), b = track.getPointAtLength(Math.min(LEN, L + 1));
  const ang = Math.atan2(b.y - a.y, b.x - a.x) * 180 / Math.PI;
  plane.setAttribute("transform", `translate(${a.x} ${a.y}) rotate(${ang})`);
  flown.style.strokeDashoffset = String(LEN * (1 - p));
}
if (REDUCED) { placePlane(.62); }
else {
  const DUR = 9000, HOLD = 1400; let start = performance.now();
  const loop = now => {
    const el = now - start;
    if (el > DUR + HOLD) { start = now; destIdx = (destIdx + 1) % (POPULAR.length - 1); updateRouteText(); }
    const p = Math.min(1, el / DUR), ease = p < .5 ? 2*p*p : 1 - (-2*p + 2)**2 / 2;
    placePlane(ease); requestAnimationFrame(loop);
  };
  requestAnimationFrame(loop);
}

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
  const now = new Date(); let m = Math.ceil((now.getHours()*60 + now.getMinutes() + 6) / 5) * 5;
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
  if (animate && !REDUCED) document.querySelectorAll("#rows .tiles").forEach((el, i) => setTimeout(() => flapIn(el, flights[i].code), i * 70));
  else if (animate) document.querySelectorAll("#rows .tiles").forEach((el, i) => el.innerHTML = tilesHTML(flights[i].code));
}
$("#shuffle").addEventListener("click", () => { boardSeed = (boardSeed * 31 + 7) % 2147483647; buildFlights(); renderBoard(true); });
function tickClock(){ const d = new Date(); $("#clock").textContent = `${String(d.getHours()).padStart(2,"0")}:${String(d.getMinutes()).padStart(2,"0")}`; }
tickClock(); setInterval(tickClock, 15000);

/* ═══════════════ 機長廣播 ═══════════════ */
let paIdx = -1;
const PA_FALLBACK = [{id:"cavok", category:"weather", name:{zh:"CAVOK",en:"CAVOK",ja:"CAVOK"},
  summary:{zh:"天氣報告中的 CAVOK 代表能見度 10 公里以上、沒有影響飛航的雲與重要天氣。",en:"CAVOK in a weather report means visibility of 10 km or more with no significant cloud or weather.",ja:"CAVOK は視程 10 km 以上で、運航に影響する雲や顕著な気象がないことを示す。"},
  fact:{zh:"讀作「卡夫 OK」，是 Ceiling And Visibility OK 的縮寫。",en:"It stands for Ceiling And Visibility OK.",ja:"Ceiling And Visibility OK の略。"}}];
function renderPA(){
  const list = D.topics.length ? D.topics : PA_FALLBACK;
  if (paIdx < 0) paIdx = Math.floor(rng(boardSeed + 17)() * list.length);
  const k = list[paIdx % list.length], h = new Date().getHours();
  $("#paGreet").textContent = [t(h < 11 ? "pa.morning" : h < 18 ? "pa.afternoon" : "pa.evening"), t("pa.lead")].join(lang === "en" ? " " : "");
  $("#paTopic").textContent = field(k.name);
  $("#paSum").textContent = field(k.summary);
  const fact = field(k.fact);
  $("#paFact").hidden = !fact;
  $("#paFact").innerHTML = `<b>${esc(t("pa.fact"))}</b>${esc(fact)}`;
  $("#paOpen").href = list === D.topics ? `knowledge.html?topic=${encodeURIComponent(k.id)}` : "knowledge.html";
}
$("#paNext").addEventListener("click", () => { paIdx++; renderPA(); });

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
