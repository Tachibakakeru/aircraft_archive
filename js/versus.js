"use strict";
/* ═══════════════════════════════════════════════
   波音 vs 空巴：兩架機型逐部位並排對比
   直接讀取既有 data/<id>.json 的 parts（name/summary/fact/images），
   不另建資料結構——編輯照片/文字沿用 editor.html 既有機制。
   ═══════════════════════════════════════════════ */

const PART_ORDER = ["fuselage", "cockpit", "wing", "engine", "vstab", "hstab", "gear"];
const $ = id => document.getElementById(id);
const F = v => I18N.field(v);

let fleet = null;
const dataCache = {};
let idA = "b738", idB = "a320";

(async () => {
  fleet = await (await fetch("data/fleet.json?v=97")).json();

  const params = new URLSearchParams(location.search);
  const pa = params.get("a"), pb = params.get("b");
  if (pa && fleet.aircraft.some(x => x.id === pa)) idA = pa;
  if (pb && fleet.aircraft.some(x => x.id === pb)) idB = pb;
  if (!fleet.aircraft.some(x => x.id === idA)) idA = fleet.aircraft[0].id;
  if (!fleet.aircraft.some(x => x.id === idB)) idB = fleet.aircraft[1] ? fleet.aircraft[1].id : fleet.aircraft[0].id;

  await Promise.all([loadData(idA), loadData(idB)]);
  I18N.apply();
  renderPickers();
  render();

  $("btn-theme").addEventListener("click", () => window.HangarTheme.toggle());
  I18N.mountSelector($("btn-lang"));
  document.addEventListener("langchange", () => { I18N.apply(); renderPickers(); render(); });
})();

async function loadData(id){
  if (dataCache[id]) return dataCache[id];
  const d = await (await fetch(`data/${id}.json?v=97`)).json();
  dataCache[id] = d;
  return d;
}

function craftMeta(id){ return fleet.aircraft.find(a => a.id === id); }

function syncUrl(){
  history.replaceState(null, "", `?a=${idA}&b=${idB}`);
}

function renderPickers(){
  for (const [selId, current] of [["vs-pick-a", idA], ["vs-pick-b", idB]]){
    const sel = $(selId);
    sel.innerHTML = "";
    fleet.aircraft.forEach(a => {
      const o = document.createElement("option");
      o.value = a.id; o.textContent = a.name;
      if (a.id === current) o.selected = true;
      sel.appendChild(o);
    });
  }
  $("vs-pick-a").onchange = async e => { idA = e.target.value; await loadData(idA); syncUrl(); render(); };
  $("vs-pick-b").onchange = async e => { idB = e.target.value; await loadData(idB); syncUrl(); render(); };
}

function craftHeadHtml(id){
  const m = craftMeta(id);
  return `<div class="vs-head">
    <img class="vs-head-thumb" src="${m.thumb}" alt="${m.name}">
    <h2>${m.name}</h2>
    <div class="vs-head-mfr">${m.manufacturer.toUpperCase()}</div>
    <a class="vs-head-link" href="viewer.html?model=${id}">3D ↗</a>
  </div>`;
}

function partCardHtml(id, pid){
  const d = dataCache[id];
  const part = d.parts && d.parts[pid];
  if (!part){
    return `<div class="vs-card vs-card-empty">
      <div class="vs-empty-msg">${I18N.t("versus.noparts")}</div>
      <a class="vs-card-edit" href="editor.html?model=${id}">${I18N.t("versus.edit")}</a>
    </div>`;
  }
  const img = part.images && part.images[0];
  const imgHtml = img
    ? `<figure class="vs-card-fig"><img src="${img.src}" alt="${F(img.caption) || F(part.name)}" loading="lazy"></figure>`
    : `<div class="vs-card-fig vs-card-fig-empty">${I18N.t("versus.noimage")}</div>`;
  const summary = F(part.summary) || "";
  const fact = F(part.fact) || "";
  return `<div class="vs-card">
    ${imgHtml}
    <p class="vs-card-summary">${summary}</p>
    ${fact ? `<p class="vs-card-fact">💡 ${fact}</p>` : ""}
    <a class="vs-card-edit" href="editor.html?model=${id}">${I18N.t("versus.edit")}</a>
  </div>`;
}

function partNameFor(pid){
  const da = dataCache[idA], db = dataCache[idB];
  const pa = da.parts && da.parts[pid], pb = db.parts && db.parts[pid];
  return F((pa && pa.name) || (pb && pb.name)) || pid;
}

function render(){
  $("vs-heads").innerHTML = `<div class="vs-head-spacer"></div>${craftHeadHtml(idA)}${craftHeadHtml(idB)}`;

  let html = "";
  PART_ORDER.forEach(pid => {
    const da = dataCache[idA].parts, db = dataCache[idB].parts;
    if (!(da && da[pid]) && !(db && db[pid])) return;   // 兩邊都沒有這個部位就整列略過
    html += `<div class="vs-row">
      <div class="vs-row-label">${partNameFor(pid)}</div>
      ${partCardHtml(idA, pid)}
      ${partCardHtml(idB, pid)}
    </div>`;
  });
  $("vs-rows").innerHTML = html;
}
