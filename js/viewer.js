"use strict";
/* ═══════════════════════════════════════════════
   天空檔案 — 3D 檢視器
   依 ?model=<id> 載入 data/<id>.json（部位文案）
   與 models/<id>.json（convert_fr24.py 產出的幾何）
   ═══════════════════════════════════════════════ */

const MODEL_ID = new URLSearchParams(location.search).get("model") || "a320";
const overlay = document.getElementById("overlay");
const overlayMsg = document.getElementById("overlay-msg");
const overlayTag = document.querySelector("#overlay .tag");

function fail(html){
  overlayTag.textContent = "LOAD ERROR";
  overlayTag.style.animation = "none";
  overlayMsg.innerHTML = html;
}

function loadData(){
  // 編輯器的本機暫存優先（讓「預覽」即時反映編輯結果）
  const local = localStorage.getItem("hangar_edit_" + MODEL_ID);
  if (local){
    try { return Promise.resolve(JSON.parse(local)); } catch {}
  }
  return fetch(`data/${MODEL_ID}.json?v=51`).then(r => { if(!r.ok) throw 0; return r.json(); });
}

Promise.all([
  loadData(),
  fetch(`models/${MODEL_ID}.json?v=51`).then(r => { if(!r.ok) throw 0; return r.json(); })
]).then(([DATA, MODEL]) => init(DATA, MODEL))
  .catch(() => fail(
    `無法載入 <code>data/${MODEL_ID}.json</code> 或 <code>models/${MODEL_ID}.json</code>。<br>` +
    `請確認機型 ID 正確；若以 <code>file://</code> 開啟，請改用本機伺服器：<br>` +
    `<code>python3 -m http.server 8000</code>`
  ));

function init(DATA, MODEL){
  const PARTS = DATA.parts;
  const PART_ORDER = DATA.partOrder || Object.keys(PARTS);

  // 記錄最近瀏覽（供列表頁顯示），最多保留 10 筆、最新在前
  try {
    const recent = JSON.parse(localStorage.getItem("hangar_recent") || "[]")
      .filter(id => id !== MODEL_ID);
    recent.unshift(MODEL_ID);
    localStorage.setItem("hangar_recent", JSON.stringify(recent.slice(0, 10)));
  } catch {}
  const F = v => I18N.field(v);   // 內容欄位多語言取值

  document.title = `${I18N.specValue(I18N.field(DATA.title))} — SKY ARCHIVE`;
  document.getElementById("craft-title").textContent = I18N.specValue(I18N.field(DATA.title));
  document.getElementById("craft-sub").textContent = I18N.specValue(I18N.field(DATA.sub)) || "";
  document.getElementById("credit").textContent =
    (MODEL.meta && MODEL.meta.source) ? `3D MODEL: ${MODEL.meta.source}` : "";
  I18N.apply();

  /* ── Three.js 場景 ── */
  const canvas = document.getElementById("scene");
  const renderer = new THREE.WebGLRenderer({canvas, antialias:true, alpha:true, preserveDrawingBuffer:true});
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 200);

  scene.add(new THREE.HemisphereLight(0xcfe4ff, 0x1a2436, 0.9));
  const key = new THREE.DirectionalLight(0xfff2df, 0.95);
  key.position.set(6, 9, 5);
  scene.add(key);
  const rim = new THREE.DirectionalLight(0x6fd3ef, 0.35);
  rim.position.set(-7, 4, -6);
  scene.add(rim);

  function themeColor(varName, fallback){
    const v = getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
    return v || fallback;
  }
  const grid = new THREE.PolarGridHelper(9, 16, 5, 48,
    new THREE.Color(themeColor("--scene-grid", "#24344d")),
    new THREE.Color(themeColor("--scene-grid2", "#1a2740")));
  scene.add(grid);

  const shadow = new THREE.Mesh(
    new THREE.CircleGeometry(4.8, 48),
    new THREE.MeshBasicMaterial({color:0x000000, transparent:true, opacity:0.28})
  );
  shadow.rotation.x = -Math.PI/2;
  shadow.position.y = 0.015;
  shadow.scale.set(1.35, 1, 1);
  scene.add(shadow);

  /* ── 建立模型 ── */
  function b64ToArray(b64, Type){
    const bin = atob(b64);
    const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    return new Type(bytes.buffer);
  }

  let liveryTex = null;
  if (MODEL.texture){
    liveryTex = new THREE.TextureLoader().load(MODEL.texture);
    liveryTex.flipY = false;          // glTF UV 原點在左上
    liveryTex.anisotropy = 4;
  }

  const airplane = new THREE.Group();
  scene.add(airplane);
  const partGroups = {};

  // 單一 entry → THREE.Mesh（部位與操縱面共用）
  function makeMesh(e){
    const geo = new THREE.BufferGeometry();
    if (e.q){   // v2 量化格式：uint16 位置 → 反量化
      const q = b64ToArray(e.q, Uint16Array);
      const n = q.length / 3;
      const pos = new Float32Array(q.length);
      const [ox, oy, oz] = e.qo, [sx, sy, sz] = e.qs;
      for (let i = 0; i < n; i++){
        pos[i*3]   = q[i*3]   * sx + ox;
        pos[i*3+1] = q[i*3+1] * sy + oy;
        pos[i*3+2] = q[i*3+2] * sz + oz;
      }
      geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
      if (e.u){   // UV 也是 uint16 量化（0..65535 → 0..1）
        const qu = b64ToArray(e.u, Uint16Array);
        const uv = new Float32Array(qu.length);
        for (let i = 0; i < qu.length; i++) uv[i] = qu[i] / 65535;
        geo.setAttribute("uv", new THREE.BufferAttribute(uv, 2));
      }
    } else {   // v1 舊格式（float32 位置）
      geo.setAttribute("position", new THREE.BufferAttribute(b64ToArray(e.p, Float32Array), 3));
      if (e.u) geo.setAttribute("uv", new THREE.BufferAttribute(b64ToArray(e.u, Float32Array), 2));
    }
    geo.setIndex(new THREE.BufferAttribute(b64ToArray(e.i, e.iw === 4 ? Uint32Array : Uint16Array), 1));
    geo.computeVertexNormals();
    const alpha = e.c[3] !== undefined ? e.c[3] : 1;
    const m = new THREE.MeshStandardMaterial({
      color: new THREE.Color(e.c[0], e.c[1], e.c[2]),
      map: (e.t && liveryTex) ? liveryTex : null,
      metalness: 0.15, roughness: 0.55, side: THREE.DoubleSide,
      transparent: alpha < 1, opacity: alpha, depthWrite: alpha >= 1
    });
    return new THREE.Mesh(geo, m);
  }

  for (const [pid, entries] of Object.entries(MODEL.parts)){
    const g = new THREE.Group();
    g.userData.partId = pid;
    g.userData.anchor = new THREE.Vector3(...(MODEL.anchors[pid] || [0,1,0]));
    for (const e of entries) g.add(makeMesh(e));
    airplane.add(g);
    partGroups[pid] = g;
  }

  // ── 可動操縱面：各片建鉸鏈 pivot，掛在主翼群組下（拾取／高亮歸主翼）──
  const surfaces = [];
  if (MODEL.surfaces && partGroups.wing){
    for (const s of MODEL.surfaces){
      const pivot = new THREE.Group();
      pivot.position.set(s.pv[0], s.pv[1], s.pv[2]);
      pivot.userData = { type: s.t, side: s.sd,
        axis: new THREE.Vector3(s.ax[0], s.ax[1], s.ax[2]).normalize(),
        base: new THREE.Vector3(s.pv[0], s.pv[1], s.pv[2]) };
      for (const e of s.e){
        const mesh = makeMesh(e);
        mesh.position.set(-s.pv[0], -s.pv[1], -s.pv[2]);   // 幾何相對樞紐
        pivot.add(mesh);
      }
      partGroups.wing.add(pivot);
      surfaces.push(pivot);
    }
  }

  // 展開角度：取材自 FlightGear 737NG 開源機模的實際操縱面偏轉角（GPL-2.0）
  // https://github.com/omega13a/737-Next-Generation Models/LWing.xml
  const DEPLOY = { flap: 0.52, slat: -0.44, spoiler: -0.79, aileron: 0.35 };
  // Fowler 平移：襟翼隨展開往後（-X）並略下（-Y）滑出、縫翼往前（+X）下伸
  const FOWLER = { flap: [-0.22, -0.05, 0], slat: [0.10, -0.05, 0] };
  let deployTarget = 0, deployNow = 0;
  function applyDeploy(){
    for (const pv of surfaces){
      const type = pv.userData.type;
      let ang = (DEPLOY[type] || 0) * deployNow;
      if (type !== "aileron") ang *= pv.userData.side;
      pv.quaternion.setFromAxisAngle(pv.userData.axis, ang);
      const f = FOWLER[type], b = pv.userData.base;
      if (f) pv.position.set(b.x + f[0] * deployNow, b.y + f[1] * deployNow, b.z + f[2] * deployNow);
    }
  }

  /* ── 視角控制 ── */
  const target = new THREE.Vector3(0, 1.1, 0);
  let theta = 0.9, phi = 1.15, radius = 13;
  const RAD_MIN = 5, RAD_MAX = 26;
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let autoRotate = !reducedMotion;

  function applyCamera(){
    phi = Math.max(0.25, Math.min(Math.PI - 0.35, phi));
    radius = Math.max(RAD_MIN, Math.min(RAD_MAX, radius));
    camera.position.set(
      target.x + radius * Math.sin(phi) * Math.cos(theta),
      target.y + radius * Math.cos(phi),
      target.z + radius * Math.sin(phi) * Math.sin(theta)
    );
    camera.lookAt(target);
  }

  let dragging = false, moved = 0, lastX = 0, lastY = 0, pinchDist = 0;
  const pointers = new Map();

  canvas.addEventListener("pointerdown", e => {
    pointers.set(e.pointerId, {x:e.clientX, y:e.clientY});
    dragging = true; moved = 0;
    lastX = e.clientX; lastY = e.clientY;
    canvas.classList.add("dragging");
    canvas.setPointerCapture(e.pointerId);
  });
  canvas.addEventListener("pointermove", e => {
    if (pointers.has(e.pointerId)) pointers.set(e.pointerId, {x:e.clientX, y:e.clientY});

    if (pointers.size === 2){
      const [a, b] = [...pointers.values()];
      const d = Math.hypot(a.x-b.x, a.y-b.y);
      if (pinchDist > 0) radius *= pinchDist / d;
      pinchDist = d;
      moved = 99;
      return;
    }
    if (!dragging) { hoverCheck(e); return; }

    const dx = e.clientX - lastX, dy = e.clientY - lastY;
    moved += Math.abs(dx) + Math.abs(dy);
    theta += dx * 0.0055;
    phi   -= dy * 0.0055;
    lastX = e.clientX; lastY = e.clientY;
  });
  function endPointer(e){
    pointers.delete(e.pointerId);
    if (pointers.size < 2) pinchDist = 0;
    if (pointers.size === 0){
      dragging = false;
      canvas.classList.remove("dragging");
      if (moved < 7) pickAt(e.clientX, e.clientY);
      else { camDirty = true; updateURL(); }
    }
  }
  canvas.addEventListener("pointerup", endPointer);
  canvas.addEventListener("pointercancel", endPointer);
  let wheelTimer = 0;
  canvas.addEventListener("wheel", e => {
    e.preventDefault();
    radius *= (1 + Math.sign(e.deltaY) * 0.08);
    camDirty = true;
    clearTimeout(wheelTimer); wheelTimer = setTimeout(updateURL, 260);
  }, {passive:false});

  /* ── 點選 / 懸停 ── */
  const raycaster = new THREE.Raycaster();
  const ndc = new THREE.Vector2();

  function partAt(cx, cy){
    ndc.set((cx / innerWidth) * 2 - 1, -(cy / innerHeight) * 2 + 1);
    raycaster.setFromCamera(ndc, camera);
    const hits = raycaster.intersectObjects(airplane.children, true);
    for (const h of hits){
      let o = h.object;
      while (o && !o.userData.partId) o = o.parent;
      if (o) return o;
    }
    return null;
  }

  let selected = null;
  let hovered = null;

  function setEmissive(group, hex, intensity){
    group.traverse(o => {
      if (o.isMesh){
        o.material.emissive = new THREE.Color(hex);
        o.material.emissiveIntensity = intensity;
      }
    });
  }

  function hoverCheck(e){
    const p = partAt(e.clientX, e.clientY);
    if (p !== hovered){
      if (hovered && hovered !== selected) setEmissive(hovered, 0x000000, 0);
      hovered = p;
      if (hovered && hovered !== selected) setEmissive(hovered, 0xffb547, 0.12);
      canvas.classList.toggle("hovering", !!hovered);
    }
  }

  function pickAt(cx, cy){
    const p = partAt(cx, cy);
    if (p) selectPart(p.userData.partId);
    else   deselect();
  }

  /* ── 選取 → 面板 + 標註線 ── */
  const panel   = document.getElementById("panel");
  const chipsEl = document.getElementById("chips");
  const coDot   = document.getElementById("co-dot");
  const coLine  = document.getElementById("co-line");
  const coLabel = document.getElementById("callout-label");

  PART_ORDER.forEach(id => {
    if (!partGroups[id] || !PARTS[id]) return;   // 該機型缺此部位則不顯示
    const b = document.createElement("button");
    b.className = "chip";
    b.textContent = I18N.spec(F(PARTS[id].name));
    b.dataset.part = id;
    b.addEventListener("click", () => selectPart(id));
    chipsEl.appendChild(b);
  });

  function selectPart(id){
    if (!PARTS[id]) return;
    if (selected) setEmissive(selected, 0x000000, 0);
    selected = partGroups[id];
    setEmissive(selected, 0xffb547, 0.4);

    const d = PARTS[id];
    document.getElementById("p-title").textContent = I18N.spec(F(d.name));
    document.getElementById("p-en").textContent = d.en || "";
    document.getElementById("p-summary").textContent = F(d.summary) || "";

    // 條列式重點
    const ul = document.getElementById("p-bullets");
    ul.innerHTML = "";
    const bullets = d.bullets || [];
    if (bullets.length){
      bullets.forEach(b => {
        const li = document.createElement("li");
        li.textContent = F(b);
        ul.appendChild(li);
      });
      ul.style.display = "";
    } else {
      ul.style.display = "none";
    }

    // 圖片
    const gal = document.getElementById("p-images");
    gal.innerHTML = "";
    if (d.images && d.images.length){
      d.images.forEach(img => {
        const fig = document.createElement("figure");
        const el = document.createElement("img");
        el.src = img.src; el.alt = F(img.caption) || F(d.name); el.loading = "lazy";
        el.addEventListener("error", () => { fig.style.display = "none"; });
        fig.appendChild(el);
        const cap = F(img.caption);
        if (cap){
          const c = document.createElement("figcaption");
          c.textContent = cap;
          fig.appendChild(c);
        }
        gal.appendChild(fig);
      });
      gal.style.display = "";
    } else {
      gal.style.display = "none";
    }

    // 規格表
    const dl = document.getElementById("p-specs");
    const specTitle = document.getElementById("p-spec-title");
    dl.innerHTML = "";
    if (d.specs && d.specs.length){
      d.specs.forEach(([k, v]) => {
        const row = document.createElement("div");
        row.className = "spec-row";
        const dt = document.createElement("dt"); dt.textContent = I18N.spec(F(k));
        const dd = document.createElement("dd"); dd.textContent = I18N.specValue(F(v));
        row.append(dt, dd);
        dl.appendChild(row);
      });
      dl.style.display = ""; specTitle.style.display = "";
    } else {
      dl.style.display = "none"; specTitle.style.display = "none";
    }

    // 冷知識
    const factbox = document.getElementById("p-factbox");
    const fact = F(d.fact);
    if (fact){
      document.getElementById("p-fact").textContent = fact;
      factbox.style.display = "";
    } else {
      factbox.style.display = "none";
    }

    panel.classList.add("open");
    panel.setAttribute("aria-hidden", "false");
    coLabel.textContent = d.en;
    coLabel.style.display = "block";
    coDot.style.display = coLine.style.display = "";

    document.querySelectorAll(".chip").forEach(c =>
      c.classList.toggle("active", c.dataset.part === id));

    updateURL();
  }

  function deselect(){
    if (selected) setEmissive(selected, 0x000000, 0);
    selected = null;
    panel.classList.remove("open");
    panel.setAttribute("aria-hidden", "true");
    coLabel.style.display = "none";
    coDot.style.display = coLine.style.display = "none";
    document.querySelectorAll(".chip").forEach(c => c.classList.remove("active"));
    updateURL();
  }

  document.getElementById("panel-close").addEventListener("click", deselect);

  const anchorWorld = new THREE.Vector3();
  function updateCallout(){
    if (!selected) return;
    anchorWorld.copy(selected.userData.anchor).applyMatrix4(airplane.matrixWorld);
    const v = anchorWorld.clone().project(camera);
    const x = ( v.x + 1) / 2 * innerWidth;
    const y = (-v.y + 1) / 2 * innerHeight;
    const lx = Math.min(Math.max(x + 70, 90), innerWidth - 90);
    const ly = Math.max(y - 70, 60);
    coDot.setAttribute("cx", x);  coDot.setAttribute("cy", y);
    coLine.setAttribute("x1", x); coLine.setAttribute("y1", y);
    coLine.setAttribute("x2", lx);coLine.setAttribute("y2", ly);
    coLabel.style.left = lx + "px";
    coLabel.style.top  = (ly - 6) + "px";
  }

  /* ── 控制按鈕 ── */
  const btnRotate = document.getElementById("btn-rotate");
  btnRotate.setAttribute("aria-pressed", String(autoRotate));
  btnRotate.addEventListener("click", () => {
    autoRotate = !autoRotate;
    btnRotate.setAttribute("aria-pressed", String(autoRotate));
  });
  document.getElementById("btn-reset").addEventListener("click", () => {
    theta = 0.9; phi = 1.15; radius = 13;
    airplane.rotation.y = 0;
  });

  /* ── 3D 標註點（hotspots）── */
  const hotspotLayer = document.getElementById("hotspots");
  let showHotspots = true;
  const hotspots = {};   // partId → DOM 元素

  PART_ORDER.forEach(id => {
    if (!partGroups[id] || !PARTS[id]) return;
    const el = document.createElement("div");
    el.className = "hotspot";
    el.innerHTML = `<span class="dot"></span><span class="tag">${I18N.spec(F(PARTS[id].name))}</span>`;
    el.addEventListener("click", () => selectPart(id));
    hotspotLayer.appendChild(el);
    hotspots[id] = el;
  });

  const btnHotspots = document.getElementById("btn-hotspots");
  btnHotspots.addEventListener("click", () => {
    showHotspots = !showHotspots;
    btnHotspots.setAttribute("aria-pressed", String(showHotspots));
    hotspotLayer.style.display = showHotspots ? "" : "none";
  });

  const _hsVec = new THREE.Vector3();
  function updateHotspots(){
    if (!showHotspots) return;
    for (const [id, el] of Object.entries(hotspots)){
      const g = partGroups[id];
      _hsVec.copy(g.userData.anchor).applyMatrix4(airplane.matrixWorld);
      const v = _hsVec.clone().project(camera);
      if (v.z > 1){ el.style.display = "none"; continue; }   // 在相機後方
      el.style.display = "";
      el.style.left = ((v.x + 1) / 2 * innerWidth) + "px";
      el.style.top  = ((-v.y + 1) / 2 * innerHeight) + "px";
      el.classList.toggle("active", selected === g);
      el.classList.toggle("dimmed", selected && selected !== g);
    }
  }

  /* ── 詳細規格抽屜 ── */
  const specDrawer = document.getElementById("spec-drawer");
  const specBody = document.getElementById("spec-body");
  document.getElementById("spec-craft-name").textContent = I18N.specValue(I18N.field(DATA.title));

  function buildSpecs(){
    const spec = DATA.specifications;
    if (!spec || !Object.keys(spec).length){
      specBody.innerHTML = `<div class="spec-empty">${I18N.t("viewer.spec.empty")}</div>`;
      return;
    }
    specBody.innerHTML = "";
    for (const [cat, rows] of Object.entries(spec)){
      const box = document.createElement("div");
      box.className = "spec-cat";
      const h = document.createElement("h3");
      h.textContent = I18N.spec(cat);   // 分類名稱翻譯
      box.appendChild(h);
      rows.forEach(([k, v]) => {
        const row = document.createElement("div");
        row.className = "spec-row";
        const dt = document.createElement("dt"); dt.textContent = I18N.spec(F(k));
        const dd = document.createElement("dd"); dd.textContent = I18N.specValue(F(v));
        row.append(dt, dd);
        box.appendChild(row);
      });
      specBody.appendChild(box);
    }
  }
  buildSpecs();

  document.getElementById("btn-specs").addEventListener("click", () => {
    const open = specDrawer.classList.toggle("open");
    specDrawer.setAttribute("aria-hidden", String(!open));
  });
  document.getElementById("spec-close").addEventListener("click", () => {
    specDrawer.classList.remove("open");
    specDrawer.setAttribute("aria-hidden", "true");
  });

  /* ── 主題切換 ── */
  document.getElementById("btn-theme").addEventListener("click", () => {
    const t = window.HangarTheme.toggle();
    // 場景網格顏色即時更新
    grid.material.color.set(themeColor("--scene-grid", "#24344d"));
  });

  /* ── 語言選擇（點擊選擇） ── */
  I18N.mountSelector(document.getElementById("btn-lang"));
  document.addEventListener("langchange", () => {
    I18N.apply();
    const tTitle = I18N.specValue(I18N.field(DATA.title));
    document.title = `${tTitle} — SKY ARCHIVE`;
    document.getElementById("craft-title").textContent = tTitle;
    document.getElementById("craft-sub").textContent = I18N.specValue(I18N.field(DATA.sub)) || "";
    document.getElementById("spec-craft-name").textContent = tTitle;
    document.querySelectorAll("#chips .chip").forEach(c => {
      const id = c.dataset.part;
      if (PARTS[id]) c.textContent = I18N.spec(F(PARTS[id].name));
    });
    for (const [id, el] of Object.entries(hotspots)){
      const tag = el.querySelector(".tag");
      if (tag && PARTS[id]) tag.textContent = I18N.spec(F(PARTS[id].name));
    }
    buildSpecs();
    if (selected && selected.userData.partId) selectPart(selected.userData.partId);
  });

  /* ── 單位切換（雙單位 / 公制 / 英制） ── */
  const btnUnit = document.getElementById("btn-unit");
  const syncUnit = () => { btnUnit.textContent = I18N.UNIT_NAMES[I18N.getUnit()]; };
  syncUnit();
  btnUnit.addEventListener("click", () => I18N.cycleUnit());
  document.addEventListener("unitchange", () => {
    syncUnit();
    buildSpecs();
    if (selected && selected.userData.partId) selectPart(selected.userData.partId);
  });

  /* ── 鍵盤操作 ── */
  const visibleParts = () => PART_ORDER.filter(id => partGroups[id] && PARTS[id]);
  function stepPart(dir){
    const list = visibleParts();
    if (!list.length) return;
    const cur = selected && selected.userData.partId;
    let i = list.indexOf(cur);
    i = i < 0 ? (dir > 0 ? 0 : list.length - 1) : (i + dir + list.length) % list.length;
    selectPart(list[i]);
  }
  const keysHelp = document.createElement("div");
  keysHelp.id = "keys-help"; keysHelp.hidden = true;
  keysHelp.addEventListener("click", () => { keysHelp.hidden = true; });
  document.body.appendChild(keysHelp);
  function buildKeysHelp(){
    keysHelp.innerHTML = `<div class="kh-box"><h3>${I18N.t("viewer.keys.title")}</h3><dl>
      <dt>← →</dt><dd>${I18N.t("viewer.keys.parts")}</dd>
      <dt>+ −</dt><dd>${I18N.t("viewer.keys.zoom")}</dd>
      <dt>Esc</dt><dd>${I18N.t("viewer.keys.close")}</dd>
      <dt>R</dt><dd>${I18N.t("viewer.keys.rotate")}</dd>
      <dt>0</dt><dd>${I18N.t("viewer.keys.reset")}</dd>
      <dt>S</dt><dd>${I18N.t("viewer.keys.specs")}</dd>
      <dt>?</dt><dd>${I18N.t("viewer.keys.help")}</dd></dl></div>`;
  }
  document.addEventListener("langchange", buildKeysHelp);
  document.addEventListener("keydown", e => {
    const tgt = e.target;
    if (tgt && tgt.closest && tgt.closest("input, textarea, select")) return;
    if (e.altKey || e.ctrlKey || e.metaKey) return;
    switch (e.key){
      case "ArrowRight": stepPart(1);  e.preventDefault(); break;
      case "ArrowLeft":  stepPart(-1); e.preventDefault(); break;
      case "Escape":
        if (!keysHelp.hidden) keysHelp.hidden = true;
        else if (specDrawer.classList.contains("open")){
          specDrawer.classList.remove("open"); specDrawer.setAttribute("aria-hidden", "true");
        } else deselect();
        break;
      case "r": case "R": btnRotate.click(); break;
      case "0": document.getElementById("btn-reset").click(); break;
      case "s": case "S": document.getElementById("btn-specs").click(); break;
      case "?": buildKeysHelp(); keysHelp.hidden = !keysHelp.hidden; break;
      case "+": case "=":
        radius *= 0.92; camDirty = true;
        clearTimeout(wheelTimer); wheelTimer = setTimeout(updateURL, 260);
        e.preventDefault(); break;
      case "-": case "_":
        radius *= 1.08; camDirty = true;
        clearTimeout(wheelTimer); wheelTimer = setTimeout(updateURL, 260);
        e.preventDefault(); break;
    }
  });

  /* ── 相機深連結 ── */
  let camDirty = false;
  function camStr(){
    const y = ((airplane.rotation.y % (Math.PI * 2)) + Math.PI * 2) % (Math.PI * 2);
    return [theta.toFixed(2), phi.toFixed(2), radius.toFixed(1), y.toFixed(2)].join(",");
  }
  function updateURL(){
    const p = new URLSearchParams();
    p.set("model", MODEL_ID);
    if (selected && selected.userData.partId) p.set("part", selected.userData.partId);
    if (camDirty) p.set("cam", camStr());
    history.replaceState(null, "", `?${p.toString()}`);
  }

  /* ── 導覽模式（自動輪播部位） ── */
  const btnTour = document.getElementById("btn-tour");
  let tourTimer = 0;
  function stopTour(){
    if (!tourTimer) return;
    clearInterval(tourTimer); tourTimer = 0;
    btnTour.setAttribute("aria-pressed", "false");
    btnTour.textContent = I18N.t("viewer.tour");
  }
  function startTour(){
    const list = visibleParts();
    if (!list.length) return;
    autoRotate = false; btnRotate.setAttribute("aria-pressed", "false");
    let i = Math.max(0, list.indexOf(selected && selected.userData.partId));
    selectPart(list[i]);
    btnTour.setAttribute("aria-pressed", "true");
    btnTour.textContent = I18N.t("viewer.tour.stop");
    tourTimer = setInterval(() => {
      i = (i + 1) % list.length;
      selectPart(list[i]);
    }, 4200);
  }
  btnTour.addEventListener("click", () => tourTimer ? stopTour() : startTour());
  // 手動操作時停止導覽
  canvas.addEventListener("pointerdown", stopTour);
  document.getElementById("chips").addEventListener("click", stopTour);

  /* ── 截圖匯出 ── */
  document.getElementById("btn-shot").addEventListener("click", () => {
    renderer.render(scene, camera);
    const a = document.createElement("a");
    a.download = `${MODEL_ID}-${I18N.field(DATA.title)}.png`.replace(/[\\/:*?"<>|]/g, "");
    a.href = canvas.toDataURL("image/png");
    a.click();
  });

  /* ── 展開操縱面（襟翼／縫翼／擾流板／副翼） ── */
  const btnDeploy = document.getElementById("btn-deploy");
  if (surfaces.length){
    btnDeploy.hidden = false;
    const syncDeploy = () => {
      const on = deployTarget > 0.5;
      btnDeploy.setAttribute("aria-pressed", String(on));
      btnDeploy.textContent = I18N.t(on ? "viewer.deploy.stow" : "viewer.deploy");
    };
    btnDeploy.addEventListener("click", () => {
      deployTarget = deployTarget > 0.5 ? 0 : 1;
      syncDeploy();
    });
    document.addEventListener("langchange", syncDeploy);
  }

  /* ── 深連結：載入時自動選取部位、還原相機 ── */
  const params = new URLSearchParams(location.search);
  const camParam = params.get("cam");
  if (camParam){
    const [t, p, r, y] = camParam.split(",").map(Number);
    if ([t, p, r, y].every(n => !Number.isNaN(n))){
      theta = t; phi = p; radius = r; airplane.rotation.y = y;
      autoRotate = false; btnRotate.setAttribute("aria-pressed", "false");
      camDirty = true;
    }
  }
  const wantPart = params.get("part");
  if (wantPart && PARTS[wantPart] && partGroups[wantPart]) selectPart(wantPart);

  /* ── 渲染迴圈 ── */
  function resize(){
    renderer.setSize(innerWidth, innerHeight, false);
    camera.aspect = innerWidth / innerHeight;
    camera.updateProjectionMatrix();
  }
  window.addEventListener("resize", resize);
  resize();

  function tick(){
    requestAnimationFrame(tick);
    if (autoRotate && !dragging) airplane.rotation.y += 0.0022;
    if (Math.abs(deployNow - deployTarget) > 0.0015){
      deployNow += (deployTarget - deployNow) * 0.12;   // 平滑展開／收回
      applyDeploy();
    }
    applyCamera();
    updateCallout();
    updateHotspots();
    renderer.render(scene, camera);
  }
  tick();

  overlay.classList.add("hidden");
}
