"use strict";
/* ═══════════════════════════════════════════════
   機型比較：選多架 → 抓 specifications → 並排成表
   同一列數值不同時以琥珀色標示差異
   ═══════════════════════════════════════════════ */

let fleet = null;
const dataCache = {};   // id → data json
let selected = [];      // 目前比較的機型 id 陣列

let mode = "aircraft";   // "aircraft" | "airports"
let AIRPORTS = null, COUNTRIES = {};
let aptSelected = [];     // 目前比較的機場 id 陣列
const aptDetailCache = {};   // country code → { ident: {lat,lon,elev,region,runways} }

const $ = id => document.getElementById(id);

(async () => {
  fleet = await (await fetch("data/fleet.json?v=42")).json();

  const params = new URLSearchParams(location.search);
  mode = params.get("mode") === "airports" ? "airports" : "aircraft";

  // 初始：網址帶 ?ids=a320,b738 或預設兩架
  const urlIds = (params.get("ids") || "").split(",").filter(Boolean);
  selected = urlIds.length ? urlIds : ["a320", "b738"];
  selected = selected.filter(id => fleet.aircraft.some(a => a.id === id));
  if (!selected.length) selected = [fleet.aircraft[0].id];

  await Promise.all(selected.map(loadData));

  if (mode === "airports"){
    await ensureAirportsLoaded();
    const urlApt = urlIds.filter(id => AIRPORTS.some(a => a.id === id));
    aptSelected = urlApt.length ? urlApt : ["RJTT", "KJFK"];
  }

  I18N.apply();
  syncModeUI();
  renderPickers();
  await renderTable();

  $("btn-theme").addEventListener("click", () => window.HangarTheme.toggle());

  I18N.mountSelector($("btn-lang"));
  document.addEventListener("langchange", () => {
    I18N.apply(); renderPickers(); renderTable();
  });

  const btnUnit = $("btn-unit");
  const syncUnit = () => { btnUnit.textContent = I18N.UNIT_NAMES[I18N.getUnit()]; };
  syncUnit();
  btnUnit.addEventListener("click", () => I18N.cycleUnit());
  document.addEventListener("unitchange", () => { syncUnit(); renderTable(); });

  $("cmp-diff").addEventListener("change", e => { diffOnly = e.target.checked; renderTable(); });

  $("cmp-modes").addEventListener("click", async e => {
    const btn = e.target.closest(".cmp-mode-btn");
    if (!btn || btn.dataset.mode === mode) return;
    mode = btn.dataset.mode;
    if (mode === "airports" && !AIRPORTS){
      await ensureAirportsLoaded();
      if (!aptSelected.length) aptSelected = ["RJTT", "KJFK"];
    }
    syncModeUI();
    syncUrl();
    renderPickers();
    await renderTable();
  });
})();

function syncModeUI(){
  document.querySelectorAll(".cmp-mode-btn").forEach(b =>
    b.classList.toggle("active", b.dataset.mode === mode));
  $("cmp-size").style.display = mode === "aircraft" ? "" : "none";
  $("cmp-h1").textContent = I18N.t(mode === "airports" ? "compare.title.airports" : "compare.title");
}

async function ensureAirportsLoaded(){
  if (AIRPORTS) return;
  const [aRes, cRes] = await Promise.all([
    fetch("data/airports.json?v=42"), fetch("data/countries.json?v=42"),
  ]);
  const aData = await aRes.json();
  COUNTRIES = await cRes.json();
  AIRPORTS = aData.airports;
}

async function loadAptDetail(country){
  const key = country || "ZZ";
  if (aptDetailCache[key]) return aptDetailCache[key];
  try {
    const r = await fetch(`data/details/${encodeURIComponent(key)}.json?v=42`);
    const d = r.ok ? await r.json() : {};
    aptDetailCache[key] = d;
    return d;
  } catch { return {}; }
}

let diffOnly = false;

async function loadData(id){
  if (dataCache[id]) return dataCache[id];
  const d = await (await fetch(`data/${id}.json?v=42`)).json();
  dataCache[id] = d;
  return d;
}

function craftMeta(id){ return fleet.aircraft.find(a => a.id === id); }

// 從 specifications.尺寸 取出以公尺為單位的數值
function dimM(id, label){
  const rows = (dataCache[id] && dataCache[id].specifications && dataCache[id].specifications["尺寸"]) || [];
  const r = rows.find(x => x[0] === label);
  if (!r) return null;
  const m = String(r[1]).match(/([\d.]+)\s*m(?![m²³a-z])/);   // 公尺，排除 mm/m²/m³
  return m ? parseFloat(m[1]) : null;
}

// ── 尺寸比例對照（同比例側影，附成人參考） ──
function renderSizeCompare(){
  const host = $("cmp-size");
  const COLORS = ["#6fd3ef", "#ffb547", "#7ecb8f", "#c98bdb"];
  const items = selected.map((id, i) => ({
    id, name: craftMeta(id).name, color: COLORS[i % COLORS.length],
    L: dimM(id, "全長"), H: dimM(id, "機高")
  })).filter(a => a.L && a.H);
  if (items.length < 2){ host.innerHTML = ""; return; }

  const HUMAN = 1.8;
  const maxL = Math.max(...items.map(a => a.L));
  const maxH = Math.max(...items.map(a => a.H));
  const vbW = 960, labelW = 156, padR = 24, drawW = vbW - labelW - padR;
  const pxPerM = Math.min(drawW / maxL, 120 / maxH);   // 長度或高度取較嚴者，兩軸同比例
  const rowSlot = maxH * pxPerM + 30;

  const silhouette = (a, yb) => {
    const w = a.L * pxPerM, h = a.H * pxPerM, x0 = labelW;
    const fb = yb - h * 0.06, ft = fb - Math.max(h * 0.32, 5);   // 機身上下緣
    const finX = x0 + w * 0.80;
    return `
      <path d="M ${x0 + w * 0.03},${fb} Q ${x0},${(fb + ft) / 2} ${x0 + w * 0.11},${ft}
               L ${x0 + w},${ft} L ${x0 + w},${fb} Z" fill="${a.color}" opacity="0.9"/>
      <path d="M ${finX},${ft} L ${x0 + w},${yb - h} L ${x0 + w},${ft} Z" fill="${a.color}" opacity="0.9"/>`;
  };

  let y = 6, body = "";
  items.forEach(a => {
    const yb = y + rowSlot - 22;
    body += `<text x="${labelW - 12}" y="${yb - 8}" text-anchor="end" class="cs-name">${a.name}</text>
             <text x="${labelW - 12}" y="${yb + 8}" text-anchor="end" class="cs-dim">${a.L} m</text>
             ${silhouette(a, yb)}`;
    y += rowSlot;
  });
  // 成人參考
  const yb = y + 30;
  const hh = HUMAN * pxPerM, hw = Math.max(hh * 0.28, 3), hx = labelW;
  body += `<text x="${labelW - 12}" y="${yb - 4}" text-anchor="end" class="cs-dim">${I18N.t("compare.size.human")}</text>
           <circle cx="${hx + hw / 2}" cy="${yb - hh + hw * 0.5}" r="${hw * 0.5}" fill="var(--muted)"/>
           <rect x="${hx + hw * 0.2}" y="${yb - hh + hw}" width="${hw * 0.6}" height="${hh - hw}" rx="${hw * 0.3}" fill="var(--muted)"/>`;

  host.innerHTML = `<div class="cs-head">${I18N.t("compare.size")}</div>
    <svg viewBox="0 0 ${vbW} ${y + 48}" class="cs-svg" preserveAspectRatio="xMidYMid meet">${body}</svg>`;
}

// ── 選擇器 ──
function renderPickers(){
  if (mode === "airports"){ renderAptPickers(); return; }
  const wrap = $("cmp-pickers");
  wrap.innerHTML = "";
  selected.forEach((id, i) => {
    const sel = document.createElement("select");
    fleet.aircraft.forEach(a => {
      const o = document.createElement("option");
      o.value = a.id; o.textContent = a.name;
      if (a.id === id) o.selected = true;
      sel.appendChild(o);
    });
    sel.addEventListener("change", async () => {
      selected[i] = sel.value;
      await loadData(sel.value);
      syncUrl(); renderTable();
    });
    wrap.appendChild(sel);
  });
  if (selected.length < 4){
    const add = document.createElement("button");
    add.className = "cmp-add";
    add.textContent = I18N.t("compare.add");
    add.addEventListener("click", async () => {
      const next = fleet.aircraft.find(a => !selected.includes(a.id));
      if (!next) return;
      selected.push(next.id);
      await loadData(next.id);
      syncUrl(); renderPickers(); renderTable();
    });
    wrap.appendChild(add);
  }
}

function syncUrl(){
  if (mode === "airports"){
    history.replaceState(null, "", `?mode=airports&ids=${aptSelected.filter(Boolean).join(",")}`);
    return;
  }
  history.replaceState(null, "", `?ids=${selected.join(",")}`);
}

// ── 比較表 ──
async function renderTable(){
  if (mode === "airports"){ await renderAptTable(); return; }
  const table = $("cmp-table");
  const empty = $("cmp-empty");
  renderSizeCompare();
  if (!selected.length){ table.innerHTML = ""; empty.style.display = "block"; return; }
  empty.style.display = "none";

  // 收集所有出現過的規格分類與項目（以第一架的順序為主，補上其他架多出的）
  const catOrder = [];
  const catRows = {};   // cat → [label,...]（去重保序）
  selected.forEach(id => {
    const spec = dataCache[id].specifications || {};
    for (const [cat, rows] of Object.entries(spec)){
      if (!catRows[cat]){ catRows[cat] = []; catOrder.push(cat); }
      rows.forEach(([label]) => {
        if (!catRows[cat].includes(label)) catRows[cat].push(label);
      });
    }
  });

  // 快速查表：id → cat → label → value
  const lookup = {};
  selected.forEach(id => {
    lookup[id] = {};
    const spec = dataCache[id].specifications || {};
    for (const [cat, rows] of Object.entries(spec)){
      lookup[id][cat] = {};
      rows.forEach(([label, val]) => { lookup[id][cat][label] = val; });
    }
  });

  // 表頭
  let html = "<thead><tr><th></th>";
  selected.forEach(id => {
    const m = craftMeta(id);
    html += `<th><div class="craft-head">
      <img class="thumb" src="${m.thumb}" alt="${m.name}">
      <h2>${m.name}</h2>
      <div class="mfr">${m.manufacturer.toUpperCase()}</div>
      <div>
        <button class="remove" data-id="${id}">${I18N.t("compare.remove")}</button>
        <a class="view-link" href="viewer.html?model=${id}">3D ↗</a>
      </div>
    </div></th>`;
  });
  html += "</tr></thead><tbody>";

  // 基本資訊列（來自 fleet）
  html += catBlock(I18N.t("compare.basic"), [
    [I18N.t("compare.mfr"), id => craftMeta(id).manufacturer],
    [I18N.t("compare.category"), id => I18N.field(craftMeta(id).category)],
    [I18N.t("compare.firstflight"), id => craftMeta(id).firstFlight],
    [I18N.t("compare.seats"), id => craftMeta(id).seats],
  ], true);

  // 詳細規格各分類
  catOrder.forEach(cat => {
    let rowsHtml = "";
    catRows[cat].forEach(label => {
      const vals = selected.map(id => (lookup[id][cat] && lookup[id][cat][label]) || null);
      const strVals = vals.map(v => v == null ? null : I18N.specValue(I18N.field(v)));
      const allSame = strVals.every(v => v === strVals[0]);
      if (diffOnly && allSame) return;   // 只顯示差異
      rowsHtml += `<tr><td class="label-cell">${I18N.spec(I18N.field(label))}</td>`;
      strVals.forEach(v => {
        if (v == null) rowsHtml += `<td class="val na">—</td>`;
        else rowsHtml += `<td class="val${!allSame ? " diff" : ""}">${v}</td>`;
      });
      rowsHtml += "</tr>";
    });
    if (rowsHtml)
      html += `<tr class="cat-row"><td colspan="${selected.length + 1}">${I18N.spec(cat)}</td></tr>` + rowsHtml;
  });

  html += "</tbody>";
  table.innerHTML = html;

  // 綁定移除
  table.querySelectorAll(".remove").forEach(btn => {
    btn.addEventListener("click", () => {
      selected = selected.filter(x => x !== btn.dataset.id);
      if (!selected.length) selected = [fleet.aircraft[0].id];
      syncUrl(); renderPickers(); renderTable();
    });
  });
}

// 產生一組來自 fleet 的資訊列（getter 版）
function catBlock(catName, rows, alwaysShow){
  let rowsHtml = "";
  rows.forEach(([label, getter]) => {
    const vals = selected.map(getter);
    const allSame = vals.every(v => v === vals[0]);
    if (diffOnly && allSame) return;
    rowsHtml += `<tr><td class="label-cell">${label}</td>`;
    vals.forEach(v => {
      if (v == null || v === "—") rowsHtml += `<td class="val na">—</td>`;
      else rowsHtml += `<td class="val${!allSame ? " diff" : ""}">${v}</td>`;
    });
    rowsHtml += "</tr>";
  });
  if (!rowsHtml) return "";
  return `<tr class="cat-row"><td colspan="${selected.length + 1}">${catName}</td></tr>` + rowsHtml;
}

/* ═══════════════════════════════════════════════
   機場比較（搜尋挑選 → 拉跑道明細 → 並排成表）
   ═══════════════════════════════════════════════ */

// 搜尋排序：代碼完全相符 > 名稱開頭相符 > 一般包含，同層再依機場規模排序，
// 避免搜「Los Angeles」時真正的 LAX 被一堆同名醫院/警局直昇機坪淹沒
const APT_TYPE_RANK = {
  large_airport: 0, medium_airport: 1, small_airport: 2,
  seaplane_base: 3, heliport: 4, balloonport: 5, closed: 6,
};
function aptSearchScore(a, q){
  const typeRank = APT_TYPE_RANK[a.type] ?? 7;
  const name = a.name.toLowerCase();
  if ((a.icao && a.icao.toLowerCase() === q) || (a.iata && a.iata.toLowerCase() === q)) return typeRank;
  if (name.startsWith(q)) return 10 + typeRank;
  return 20 + typeRank;
}

// ── 選擇器：85k+ 筆機場不適合塞進單一 <select>，改搜尋自動完成 ──
function renderAptPickers(){
  const wrap = $("cmp-pickers");
  wrap.innerHTML = "";
  aptSelected.forEach((id, i) => {
    const meta = AIRPORTS.find(a => a.id === id);
    const box = document.createElement("div");
    box.className = "cmp-apt-picker";
    box.innerHTML = `
      <input type="text" class="cmp-apt-search" value="${meta ? meta.name.replace(/"/g, "&quot;") : ""}"
        placeholder="${I18N.t("compare.apt.search")}" autocomplete="off">
      <div class="cmp-apt-suggest" hidden></div>`;
    const input = box.querySelector(".cmp-apt-search");
    const suggest = box.querySelector(".cmp-apt-suggest");
    input.addEventListener("input", () => {
      const q = input.value.trim().toLowerCase();
      if (!q){ suggest.hidden = true; return; }
      const matches = AIRPORTS
        .filter(a =>
          a.name.toLowerCase().includes(q) ||
          (a.icao && a.icao.toLowerCase().includes(q)) ||
          (a.iata && a.iata.toLowerCase().includes(q)))
        .sort((a, b) => aptSearchScore(a, q) - aptSearchScore(b, q))
        .slice(0, 8);
      if (!matches.length){ suggest.hidden = true; return; }
      suggest.innerHTML = matches.map(a =>
        `<div class="cmp-apt-opt" data-id="${a.id}">
          <span class="cmp-apt-opt-name">${a.name}</span>
          <span class="cmp-apt-opt-code">${[a.icao, a.iata].filter(Boolean).join(" · ")}</span>
        </div>`).join("");
      suggest.hidden = false;
    });
    suggest.addEventListener("mousedown", async e => {
      const opt = e.target.closest(".cmp-apt-opt");
      if (!opt) return;
      aptSelected[i] = opt.dataset.id;
      suggest.hidden = true;
      syncUrl(); renderPickers(); await renderTable();
    });
    input.addEventListener("blur", () => setTimeout(() => { suggest.hidden = true; }, 150));
    wrap.appendChild(box);
  });
  if (aptSelected.length < 4){
    const add = document.createElement("button");
    add.className = "cmp-add";
    add.textContent = I18N.t("compare.add");
    add.addEventListener("click", () => {
      aptSelected.push("");
      renderAptPickers();
      const inputs = wrap.querySelectorAll(".cmp-apt-search");
      inputs[inputs.length - 1].focus();
    });
    wrap.appendChild(add);
  }
}

const SURF_NAMES_CMP = {
  ASP: "瀝青", "ASPH-G": "瀝青", CON: "混凝土", TURF: "草地",
  GRVL: "碎石", GRS: "草地", DIRT: "泥地", WATER: "水面", SAND: "沙地",
};
function surfNameCmp(code){
  if (!code) return null;
  return SURF_NAMES_CMP[String(code).toUpperCase()] || code;
}

// ── 機場比較表 ──
async function renderAptTable(){
  const table = $("cmp-table");
  const empty = $("cmp-empty");
  const ids = aptSelected.filter(Boolean);
  if (!ids.length){ table.innerHTML = ""; empty.style.display = "block"; return; }
  empty.style.display = "none";

  const metaOf = {};
  ids.forEach(id => { metaOf[id] = AIRPORTS.find(a => a.id === id); });
  const countries = [...new Set(ids.map(id => metaOf[id] && metaOf[id].country).filter(Boolean))];
  await Promise.all(countries.map(loadAptDetail));
  const detailOf = id => {
    const m = metaOf[id];
    const store = aptDetailCache[(m && m.country) || "ZZ"] || {};
    return store[id] || null;
  };

  let html = "<thead><tr><th></th>";
  ids.forEach(id => {
    const m = metaOf[id];
    html += `<th><div class="craft-head">
      <h2>${m.name}</h2>
      <div class="mfr">${[m.icao, m.iata].filter(Boolean).join(" · ") || "—"}</div>
      <div>
        <button class="remove" data-id="${id}">${I18N.t("compare.remove")}</button>
        <a class="view-link" href="airports.html?icao=${encodeURIComponent(id)}">↗</a>
      </div>
    </div></th>`;
  });
  html += "</tr></thead><tbody>";

  const fmtFt = ft => ft == null ? null : I18N.specValue(`${Math.round(ft * 0.3048)} m (${Math.round(ft)} ft)`);

  html += catBlockApt(I18N.t("compare.basic"), [
    [I18N.t("compare.apt.country"), id => (COUNTRIES[metaOf[id].country] || metaOf[id].country || "—")],
    [I18N.t("compare.apt.city"), id => metaOf[id].city || "—"],
    [I18N.t("compare.apt.type"), id => I18N.t("airports.type." + metaOf[id].type)],
  ], ids);

  html += catBlockApt(I18N.t("compare.apt.location"), [
    [I18N.t("compare.apt.elev"), id => { const d = detailOf(id); return d && d.elev != null ? fmtFt(d.elev) : null; }],
    [I18N.t("compare.apt.coords"), id => { const d = detailOf(id); return d ? `${d.lat.toFixed(4)}, ${d.lon.toFixed(4)}` : null; }],
  ], ids);

  html += catBlockApt(I18N.t("compare.apt.runways"), [
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
      const surfs = [...new Set(d.runways.filter(r => !r.closed).map(r => surfNameCmp(r.surf)).filter(Boolean))];
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
    btn.addEventListener("click", async () => {
      aptSelected = aptSelected.filter(x => x !== btn.dataset.id);
      syncUrl(); renderPickers(); await renderTable();
    });
  });
}

function catBlockApt(catName, rows, ids){
  let rowsHtml = "";
  rows.forEach(([label, getter]) => {
    const vals = ids.map(getter);
    const strVals = vals.map(v => v == null ? null : String(v));
    const allSame = strVals.every(v => v === strVals[0]);
    if (diffOnly && allSame) return;
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
