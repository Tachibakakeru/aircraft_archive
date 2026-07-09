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
  fleet = await (await fetch("data/fleet.json")).json();

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

  const btnLang = $("btn-lang");
  btnLang.textContent = I18N.LANG_NAMES[I18N.get()];
  btnLang.addEventListener("click", () => {
    btnLang.textContent = I18N.LANG_NAMES[I18N.cycle()];
  });
  document.addEventListener("langchange", () => {
    I18N.apply(); renderPickers(); renderTable();
  });
})();

async function loadData(id){
  if (dataCache[id]) return dataCache[id];
  const d = await (await fetch(`data/${id}.json`)).json();
  dataCache[id] = d;
  return d;
}

function craftMeta(id){ return fleet.aircraft.find(a => a.id === id); }

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
    html += `<tr class="cat-row"><td colspan="${selected.length + 1}">${cat}</td></tr>`;
    catRows[cat].forEach(label => {
      const vals = selected.map(id => (lookup[id][cat] && lookup[id][cat][label]) || null);
      const strVals = vals.map(v => v == null ? null : I18N.field(v));
      const allSame = strVals.every(v => v === strVals[0]);
      html += `<tr><td class="label-cell">${I18N.field(label)}</td>`;
      strVals.forEach(v => {
        if (v == null) html += `<td class="val na">—</td>`;
        else html += `<td class="val${!allSame ? " diff" : ""}">${v}</td>`;
      });
      html += "</tr>";
    });
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
  let html = `<tr class="cat-row"><td colspan="${selected.length + 1}">${catName}</td></tr>`;
  rows.forEach(([label, getter]) => {
    const vals = selected.map(getter);
    const allSame = vals.every(v => v === vals[0]);
    html += `<tr><td class="label-cell">${label}</td>`;
    vals.forEach(v => {
      if (v == null || v === "—") html += `<td class="val na">—</td>`;
      else html += `<td class="val${!allSame ? " diff" : ""}">${v}</td>`;
    });
    html += "</tr>";
  });
  return html;
}
