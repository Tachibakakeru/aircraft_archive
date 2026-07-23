"use strict";
/* ═══════════════════════════════════════════════
   機型比較：選多架 → 抓 specifications → 並排成表
   同一列數值不同時以琥珀色標示差異
   ═══════════════════════════════════════════════ */

let fleet = null;
const dataCache = {};   // id → data json
let selected = [];      // 目前比較的機型 id 陣列

const $ = id => document.getElementById(id);

(async () => {
  fleet = await (await fetch("data/fleet.json?v=118")).json();

  // 初始：網址帶 ?ids=a320,b738 或預設兩架
  const urlIds = (new URLSearchParams(location.search).get("ids") || "").split(",").filter(Boolean);
  selected = urlIds.length ? urlIds : ["a320", "b738"];
  selected = selected.filter(id => fleet.aircraft.some(a => a.id === id));
  if (!selected.length) selected = [fleet.aircraft[0].id];

  await Promise.all(selected.map(loadData));
  I18N.apply();
  renderPickers();
  renderTable();

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
})();

let diffOnly = false;

async function loadData(id){
  if (dataCache[id]) return dataCache[id];
  const d = await (await fetch(`data/${id}.json?v=118`)).json();
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
  history.replaceState(null, "", `?ids=${selected.join(",")}`);
}

// ── 比較表 ──
function renderTable(){
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
