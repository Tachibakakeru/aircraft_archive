"use strict";
/* ═══════════════════════════════════════════════
   機庫檔案 — 資料編輯器
   讀取 data/<id>.json，於瀏覽器編輯部位文案（含條列與圖片），
   以 localStorage 暫存，匯出為可覆蓋原檔的 JSON。
   ═══════════════════════════════════════════════ */

const LS_PREFIX = "hangar_edit_";
let fleet = null;
let currentId = null;
let data = null;         // 目前機型的完整資料物件
let currentPart = null;  // 目前編輯的部位 id

const $ = id => document.getElementById(id);

// ── 初始化 ──
(async () => {
  await requireAuth();   // 未驗證會顯示鎖定畫面，通過才繼續

  try {
    fleet = await (await fetch("data/fleet.json")).json();
  } catch {
    $("ed-note").innerHTML = "無法載入 <code>data/fleet.json</code>，請以本機伺服器開啟（<code>python3 -m http.server</code>）。";
    return;
  }

  const sel = $("model-select");
  fleet.aircraft.forEach(a => {
    const o = document.createElement("option");
    o.value = a.id; o.textContent = a.name;
    sel.appendChild(o);
  });

  const urlId = new URLSearchParams(location.search).get("model");
  sel.value = (urlId && fleet.aircraft.some(a => a.id === urlId)) ? urlId : fleet.aircraft[0].id;
  sel.addEventListener("change", () => loadModel(sel.value));
  refreshSaveButton();
  await loadModel(sel.value);
})();

// ── 載入機型（優先本機暫存）──
async function loadModel(id){
  currentId = id;
  currentPart = null;
  const local = localStorage.getItem(LS_PREFIX + id);
  if (local){
    try { data = JSON.parse(local); }
    catch { data = await fetchModel(id); }
  } else {
    data = await fetchModel(id);
  }
  renderPartList();
  $("ed-fields").style.display = "none";
  $("ed-empty").style.display = "";
  history.replaceState(null, "", `?model=${id}`);
}

async function fetchModel(id){
  const d = await (await fetch(`data/${id}.json`)).json();
  // 確保每個部位都有 bullets / images 欄位
  for (const p of Object.values(d.parts || {})){
    p.bullets = p.bullets || [];
    p.images = p.images || [];
  }
  d.specifications = d.specifications || {};
  return d;
}

// ── 左側部位清單 ──
function renderPartList(){
  const wrap = $("ed-parts");
  wrap.innerHTML = "";

  // 詳細規格入口（機型層級，置頂）
  const specBtn = document.createElement("button");
  specBtn.dataset.part = "__specs__";
  const specCount = Object.values(data.specifications || {}).reduce((n, r) => n + r.length, 0);
  specBtn.innerHTML = `詳細規格${specCount ? '<span class="dot"></span>' : ''}<span class="en">SPECIFICATIONS · ${specCount} 項</span>`;
  specBtn.addEventListener("click", () => selectSpecs());
  if (currentPart === "__specs__") specBtn.classList.add("active");
  wrap.appendChild(specBtn);

  const divider = document.createElement("div");
  divider.className = "ed-parts-divider";
  wrap.appendChild(divider);

  (data.partOrder || Object.keys(data.parts)).forEach(pid => {
    const p = data.parts[pid];
    if (!p) return;
    const btn = document.createElement("button");
    btn.dataset.part = pid;
    const filled = (p.summary && p.summary.length > 0) || (p.bullets && p.bullets.length);
    btn.innerHTML = `${p.name || pid}${filled ? '<span class="dot"></span>' : ''}<span class="en">${p.en || ""}</span>`;
    btn.addEventListener("click", () => selectPart(pid));
    if (pid === currentPart) btn.classList.add("active");
    wrap.appendChild(btn);
  });
}

// ── 選取部位 → 填入表單 ──
function selectPart(pid){
  currentPart = pid;
  const p = data.parts[pid];
  $("ed-empty").style.display = "none";
  $("ed-fields").style.display = "";
  $("ed-specs").style.display = "none";

  $("f-name").value = p.name || "";
  $("f-en").value = p.en || "";
  $("f-summary").value = p.summary || "";
  $("f-bullets").value = (p.bullets || []).join("\n");
  $("f-specs").value = (p.specs || []).map(([k, v]) => `${k}：${v}`).join("\n");
  $("f-fact").value = p.fact || "";
  renderImageList();

  document.querySelectorAll(".ed-parts button").forEach(b =>
    b.classList.toggle("active", b.dataset.part === pid));
}

// ── 選取「詳細規格」→ 顯示規格編輯器 ──
function selectSpecs(){
  currentPart = "__specs__";
  $("ed-empty").style.display = "none";
  $("ed-fields").style.display = "none";
  $("ed-specs").style.display = "";
  renderSpecEditor();
  document.querySelectorAll(".ed-parts button").forEach(b =>
    b.classList.toggle("active", b.dataset.part === "__specs__"));
}

// 渲染詳細規格編輯器（分類 → textarea）
function renderSpecEditor(){
  const wrap = $("spec-cats");
  wrap.innerHTML = "";
  const spec = data.specifications || (data.specifications = {});
  for (const cat of Object.keys(spec)){
    wrap.appendChild(specCatBlock(cat, spec[cat]));
  }
}

function specCatBlock(catName, rows){
  const box = document.createElement("div");
  box.className = "spec-cat-edit";
  box.innerHTML = `
    <div class="spec-cat-head">
      <input type="text" class="cat-name" value="${escAttr(catName)}" placeholder="分類名稱">
      <button class="cat-del tiny" title="刪除分類">✕</button>
    </div>
    <textarea class="cat-rows" rows="4" placeholder="項目：數值"></textarea>`;
  const nameInput = box.querySelector(".cat-name");
  const rowsInput = box.querySelector(".cat-rows");
  rowsInput.value = (rows || []).map(([k, v]) => `${k}：${v}`).join("\n");

  // 分類改名
  nameInput.addEventListener("input", () => {
    const spec = data.specifications;
    const oldKeys = Object.keys(spec);
    // 重建物件以保留順序
    const rebuilt = {};
    oldKeys.forEach(k => {
      if (k === catName){ rebuilt[nameInput.value] = spec[k]; }
      else rebuilt[k] = spec[k];
    });
    data.specifications = rebuilt;
    catName = nameInput.value;
    persist();
  });
  // 內容編輯
  rowsInput.addEventListener("input", () => {
    data.specifications[catName] = rowsInput.value.split("\n").map(line => {
      const m = line.split(/：|:|\t/);
      if (m.length < 2) return null;
      return [m[0].trim(), m.slice(1).join("").trim()];
    }).filter(Boolean);
    persist();
    updateSpecCount();
  });
  // 刪除分類
  box.querySelector(".cat-del").addEventListener("click", () => {
    if (!confirm(`刪除分類「${catName}」？`)) return;
    delete data.specifications[catName];
    persist(); renderSpecEditor(); updateSpecCount();
  });
  return box;
}

function updateSpecCount(){
  const btn = document.querySelector('.ed-parts button[data-part="__specs__"]');
  if (!btn) return;
  const n = Object.values(data.specifications || {}).reduce((s, r) => s + r.length, 0);
  btn.querySelector(".en").textContent = `SPECIFICATIONS · ${n} 項`;
}

// ── 表單即時寫回 data + 暫存 ──
function bindField(elId, apply){
  $(elId).addEventListener("input", () => {
    if (!currentPart) return;
    apply(data.parts[currentPart], $(elId).value);
    persist();
  });
}
bindField("f-name",    (p, v) => { p.name = v; updateListLabel(); });
bindField("f-en",      (p, v) => { p.en = v; });
bindField("f-summary", (p, v) => { p.summary = v; });
bindField("f-fact",    (p, v) => { p.fact = v; });
bindField("f-bullets", (p, v) => {
  p.bullets = v.split("\n").map(s => s.trim()).filter(Boolean);
});
bindField("f-specs", (p, v) => {
  p.specs = v.split("\n").map(line => {
    const m = line.split(/：|:|\t/);   // 全形冒號 / 半形冒號 / Tab
    if (m.length < 2) return null;
    return [m[0].trim(), m.slice(1).join("").trim()];
  }).filter(Boolean);
});

function updateListLabel(){
  const btn = document.querySelector(`.ed-parts button[data-part="${currentPart}"]`);
  if (btn) btn.childNodes[0].textContent = data.parts[currentPart].name || currentPart;
}

// ── 圖片管理 ──
function renderImageList(){
  const wrap = $("img-list");
  wrap.innerHTML = "";
  const imgs = data.parts[currentPart].images || [];
  imgs.forEach((img, i) => {
    const row = document.createElement("div");
    row.className = "img-row";
    const isData = (img.src || "").startsWith("data:");
    row.innerHTML = `
      <img src="${img.src}" alt="" onerror="this.style.opacity=.2">
      <div class="img-fields">
        <span class="src-label">${isData ? "內嵌圖片（本機上傳）" : "圖片網址"}</span>
        ${isData ? "" : `<input type="text" class="i-src" value="${escAttr(img.src)}" placeholder="https://...">`}
        <input type="text" class="i-cap" value="${escAttr(img.caption || "")}" placeholder="圖說（選填）">
      </div>
      <button class="del" title="刪除">✕</button>`;
    const srcInput = row.querySelector(".i-src");
    if (srcInput) srcInput.addEventListener("input", () => {
      imgs[i].src = srcInput.value; row.querySelector("img").src = srcInput.value; persist();
    });
    row.querySelector(".i-cap").addEventListener("input", e => {
      imgs[i].caption = e.target.value; persist();
    });
    row.querySelector(".del").addEventListener("click", () => {
      imgs.splice(i, 1); renderImageList(); persist();
    });
    wrap.appendChild(row);
  });
}

$("btn-add-url").addEventListener("click", () => {
  if (!currentPart) return;
  data.parts[currentPart].images.push({ src: "", caption: "" });
  renderImageList(); persist();
});

$("btn-add-file").addEventListener("click", () => $("file-input").click());
$("file-input").addEventListener("change", async e => {
  if (!currentPart) return;
  for (const file of e.target.files){
    const dataUrl = await downscale(file, 1400, 0.82);
    data.parts[currentPart].images.push({ src: dataUrl, caption: file.name.replace(/\.[^.]+$/, "") });
  }
  renderImageList(); persist();
  e.target.value = "";
});

// 上傳圖片壓縮，避免 JSON 過大
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

// ── 本機暫存 ──
function persist(){
  try { localStorage.setItem(LS_PREFIX + currentId, JSON.stringify(data)); }
  catch (err){ toast("暫存失敗：圖片可能過大，建議改用圖片網址"); }
}

$("btn-clear-local").addEventListener("click", async () => {
  if (!confirm("確定清除此機型的本機暫存？將還原成網站原始資料。")) return;
  localStorage.removeItem(LS_PREFIX + currentId);
  await loadModel(currentId);
  toast("已清除本機暫存");
});

// ── 儲存（依 Storage 設定：GitHub 直接 commit 或下載）──
$("btn-save").addEventListener("click", async () => {
  const btn = $("btn-save");
  const original = btn.textContent;
  btn.disabled = true;
  btn.textContent = Storage.mode() === "github" ? "推送中…" : "下載中…";
  try {
    const result = await Storage.save(currentId, data);
    toast(result.message);
    if (result.ok && Storage.mode() === "github"){
      // 推送成功後清掉本機暫存（線上已是最新）
      localStorage.removeItem(LS_PREFIX + currentId);
    }
  } catch (e){
    toast("儲存失敗：" + e.message);
  } finally {
    btn.disabled = false;
    btn.textContent = original;
  }
});

function refreshSaveButton(){
  const btn = $("btn-save");
  if (Storage.mode() === "github"){
    btn.textContent = "儲存到 GitHub";
    btn.title = "直接 commit 到 GitHub，自動觸發部署";
  } else {
    btn.textContent = "匯出 JSON";
    btn.title = "下載 JSON，需手動覆蓋 data/ 後重新部署";
  }
  $("btn-github").classList.toggle("configured", Storage.isConfigured());
}

$("btn-preview").addEventListener("click", () => {
  // 預覽前先確保暫存為最新，檢視器會讀原始檔——提示使用者
  window.open(`viewer.html?model=${currentId}`, "_blank");
});

$("btn-lock").addEventListener("click", () => {
  if (confirm("鎖定編輯器並登出？下次進入需再次輸入密碼。")) {
    HANGAR_AUTH.logout();
    location.href = "fleet.html";
  }
});

// ── GitHub 設定對話框 ──
const ghModal = $("gh-modal");

$("btn-github").addEventListener("click", () => {
  const cfg = Storage.github.getCfg() || {};
  $("gh-owner").value = cfg.owner || "";
  $("gh-repo").value = cfg.repo || "";
  $("gh-branch").value = cfg.branch || "main";
  $("gh-path").value = cfg.path || "data";
  $("gh-token").value = cfg.token || "";
  $("gh-status").textContent = "";
  $("gh-status").className = "gh-status";
  ghModal.style.display = "flex";
});

function readGhForm(){
  return {
    owner: $("gh-owner").value.trim(),
    repo: $("gh-repo").value.trim(),
    branch: $("gh-branch").value.trim() || "main",
    path: $("gh-path").value.trim() || "data",
    token: $("gh-token").value.trim(),
  };
}

function ghStatus(msg, ok){
  const el = $("gh-status");
  el.textContent = msg;
  el.className = "gh-status " + (ok ? "ok" : "err");
}

$("gh-test").addEventListener("click", async () => {
  const cfg = readGhForm();
  if (!cfg.owner || !cfg.repo || !cfg.token){ ghStatus("請先填寫 owner、repo 與 token", false); return; }
  ghStatus("測試中…", true);
  const r = await Storage.github.test(cfg);
  ghStatus(r.message, r.ok);
});

$("gh-save").addEventListener("click", () => {
  const cfg = readGhForm();
  if (!cfg.owner || !cfg.repo || !cfg.token){ ghStatus("請填寫 owner、repo 與 token", false); return; }
  Storage.github.setCfg(cfg);
  ghModal.style.display = "none";
  refreshSaveButton();
  toast("GitHub 設定已儲存");
});

$("gh-clear").addEventListener("click", () => {
  if (!confirm("清除 GitHub 設定？「儲存」將退回下載 JSON 方式。")) return;
  Storage.github.clearCfg();
  ghModal.style.display = "none";
  refreshSaveButton();
  toast("已清除 GitHub 設定");
});

$("gh-cancel").addEventListener("click", () => { ghModal.style.display = "none"; });
ghModal.addEventListener("click", e => { if (e.target === ghModal) ghModal.style.display = "none"; });

// ── 新增規格分類 ──
$("add-cat").addEventListener("click", () => {
  data.specifications = data.specifications || {};
  let name = "新分類";
  let i = 1;
  while (data.specifications[name]) name = `新分類 ${++i}`;
  data.specifications[name] = [];
  persist();
  renderSpecEditor();
  updateSpecCount();
});

// ── 工具 ──
function escAttr(s){ return String(s).replace(/"/g, "&quot;").replace(/</g, "&lt;"); }

let toastTimer = null;
function toast(msg){
  let t = document.querySelector(".toast");
  if (!t){ t = document.createElement("div"); t.className = "toast"; document.body.appendChild(t); }
  t.textContent = msg;
  t.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove("show"), 2200);
}
