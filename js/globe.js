"use strict";
/* ═══════════════════════════════════════════════
   機場 3D 地球檢視 — 惰性載入（首次切到地圖模式才拉 Three.js CDN
   與初始化場景），球體貼衛星影像貼圖（assets/earth_daymap.jpg），
   標示目前篩選結果的機場點位（收藏用琥珀色），點擊開詳情面板並飛向
   該點位。拉近到夠近、光點會擠在一起時，改用「小錨點＋牽引線＋大頭針
   ＋代號」的 2D 版面配置分開顯示（svgLabels），避免重疊到點不到。
   沿用 viewer.js 的拖曳旋轉／滾輪縮放／自動旋轉／重置視角手感。
   ═══════════════════════════════════════════════ */
const AptGlobe = (() => {
  let ready = false, loading = null;
  let scene, camera, renderer, canvas, svgLabels, raf = 0;
  const DEF_THETA = 0.6, DEF_PHI = 1.2, DEF_RADIUS = 3.2;
  let theta = DEF_THETA, phi = DEF_PHI, radius = DEF_RADIUS;
  const RAD_MIN = 1.15, RAD_MAX = 6;
  let autoRotate = true;
  let flying = null;       // { fromTheta,fromPhi,fromRadius, toTheta,toPhi,toRadius, start, dur }
  let markers = [];        // { mesh, id, lat, lon, code, fav }
  let markerGroup;
  let onPick = null;       // (id) => void
  let onRotateChange = null;   // (isAutoRotating) => void

  // 標籤模式：夠近、畫面上的候選點數量夠少時，才切換成牽引線版面
  const LABEL_MAX_RADIUS = 2.0, LABEL_MAX_COUNT = 45, LABEL_MIN_DIST = 46, LEADER_LEN = 32;
  let labelPositions = new Map();   // id → { sx, sy }（螢幕座標，label 模式啟用時才有效）
  let labelFrame = 0;

  // 飛到某機場時貼一小塊真實衛星圖磚在該處球面上（沿用機場衛星縮圖同一套
  // Esri World Imagery 圖磚服務），球體本身的貼圖解析度有上限，這塊局部
  // 高解析貼片讓「飛近後看得到地面細節」這件事真的成立，不是整顆球都無限
  // 清晰（那需要完整的多層級圖磚金字塔，超出這裡合理的實作規模）。
  const TILE_ZOOM = 15, TILE_RADIUS = 1;   // 3×3 圖磚
  let groundPatch = null, patchReqId = 0;

  function tileXY(lon, lat, z){
    const n = 2 ** z;
    const x = Math.floor((lon + 180) / 360 * n);
    const latRad = lat * Math.PI / 180;
    const y = Math.floor((1 - Math.log(Math.tan(latRad) + 1 / Math.cos(latRad)) / Math.PI) / 2 * n);
    return { x: ((x % n) + n) % n, y: Math.max(0, Math.min(n - 1, y)) };
  }
  function tileURL(z, x, y){
    return `https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/${z}/${y}/${x}`;
  }

  function disposePatch(){
    if (!groundPatch) return;
    scene.remove(groundPatch);
    groundPatch.geometry.dispose();
    groundPatch.material.map.dispose();
    groundPatch.material.dispose();
    groundPatch = null;
  }
  function clearGroundPatch(){
    patchReqId++;   // 讓還在下載中的舊請求作廢，回來時不會又把貼片加回去
    disposePatch();
  }

  async function showGroundPatch(lat, lon){
    const myReq = ++patchReqId;
    const { x: cx, y: cy } = tileXY(lon, lat, TILE_ZOOM);
    const span = TILE_RADIUS * 2 + 1;
    const tileCanvas = document.createElement("canvas");
    tileCanvas.width = tileCanvas.height = 256 * span;
    const ctx = tileCanvas.getContext("2d");
    const loads = [];
    for (let dy = -TILE_RADIUS; dy <= TILE_RADIUS; dy++){
      for (let dx = -TILE_RADIUS; dx <= TILE_RADIUS; dx++){
        const img = new Image();
        img.crossOrigin = "anonymous";
        const px = (dx + TILE_RADIUS) * 256, py = (dy + TILE_RADIUS) * 256;
        loads.push(new Promise(resolve => {
          img.onload = () => { ctx.drawImage(img, px, py, 256, 256); resolve(); };
          img.onerror = resolve;
          img.src = tileURL(TILE_ZOOM, cx + dx, cy + dy);
        }));
      }
    }
    await Promise.all(loads);
    if (myReq !== patchReqId || !scene) return;   // 期間又飛到別的機場或被取消，這批已經過期

    disposePatch();
    const tex = new THREE.CanvasTexture(tileCanvas);
    tex.encoding = THREE.sRGBEncoding;
    const geo = new THREE.PlaneGeometry(0.1, 0.1);
    // side: DoubleSide 是保險——lookAt() 理論上會讓貼圖正面朝外，但方向算
    // 錯或轉一圈的話單面材質會直接被背面剔除、整塊貼片憑空消失且不報錯，
    // 排查很麻煩，雙面材質從根本排除這整類問題。
    const mat = new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide });
    groundPatch = new THREE.Mesh(geo, mat);
    groundPatch.position.copy(latLonToVec3(lat, lon, 1.01));
    groundPatch.lookAt(0, 0, 0);   // -Z 朝向球心，貼圖正面（+Z）自然朝外
    scene.add(groundPatch);
  }

  function themeColor(varName, fallback){
    const v = getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
    return v || fallback;
  }

  function loadThree(){
    if (window.THREE) return Promise.resolve();
    if (loading) return loading;
    loading = new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js";
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
    return loading;
  }

  function latLonToVec3(lat, lon, r){
    const phi_ = (90 - lat) * Math.PI / 180;
    const theta_ = (lon + 180) * Math.PI / 180;
    return new THREE.Vector3(
      -r * Math.sin(phi_) * Math.cos(theta_),
       r * Math.cos(phi_),
       r * Math.sin(phi_) * Math.sin(theta_)
    );
  }

  // latLonToVec3 反推鏡頭應該對齊的 theta/phi——讓鏡頭與該點位在
  // 同一條從球心出發的射線上，該點才會落在畫面正中央。
  function latLonToCamAngles(lat, lon){
    const phi_ = (90 - lat) * Math.PI / 180;
    const theta_ = (lon + 180) * Math.PI / 180;
    return { theta: Math.PI - theta_, phi: phi_ };
  }

  async function init(container, pickCallback, rotateChangeCallback){
    onPick = pickCallback;
    onRotateChange = rotateChangeCallback || null;
    await loadThree();
    if (ready) return;
    ready = true;

    canvas = document.createElement("canvas");
    canvas.id = "apt-globe-canvas";
    container.appendChild(canvas);

    svgLabels = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svgLabels.id = "apt-globe-labels";
    svgLabels.setAttribute("aria-hidden", "true");
    container.appendChild(svgLabels);

    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.outputEncoding = THREE.sRGBEncoding;

    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);

    scene.add(new THREE.AmbientLight(0xffffff, 1));

    // 實心球體貼衛星影像（NASA Blue Marble 日照面合成圖，經緯度等距投影，4096px）
    const earthTex = new THREE.TextureLoader().load("assets/earth_daymap.jpg");
    earthTex.encoding = THREE.sRGBEncoding;
    earthTex.anisotropy = renderer.capabilities.getMaxAnisotropy();
    earthTex.minFilter = THREE.LinearMipmapLinearFilter;
    const core = new THREE.Mesh(
      new THREE.SphereGeometry(1, 64, 48),
      new THREE.MeshBasicMaterial({ map: earthTex })
    );
    scene.add(core);

    markerGroup = new THREE.Group();
    scene.add(markerGroup);

    resize();
    window.addEventListener("resize", resize);
    wireControls();
    tick();
  }

  function resize(){
    if (!canvas) return;
    const w = canvas.parentElement.clientWidth, h = canvas.parentElement.clientHeight;
    renderer.setSize(w, h, false);
    canvas.style.width = w + "px"; canvas.style.height = h + "px";
    svgLabels.setAttribute("width", w); svgLabels.setAttribute("height", h);
    svgLabels.setAttribute("viewBox", `0 0 ${w} ${h}`);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }

  function applyCamera(){
    phi = Math.max(0.15, Math.min(Math.PI - 0.15, phi));
    radius = Math.max(RAD_MIN, Math.min(RAD_MAX, radius));
    camera.position.set(
      radius * Math.sin(phi) * Math.cos(theta),
      radius * Math.cos(phi),
      radius * Math.sin(phi) * Math.sin(theta)
    );
    camera.lookAt(0, 0, 0);
  }

  // 點擊光點時鏡頭飛向該座標並拉近——取最短角度路徑，避免鏡頭繞遠路旋轉。
  function flyTo(lat, lon, targetRadius){
    const { theta: rawToTheta, phi: toPhi } = latLonToCamAngles(lat, lon);
    let dTheta = rawToTheta - theta;
    dTheta = ((dTheta + Math.PI) % (Math.PI * 2) + Math.PI * 2) % (Math.PI * 2) - Math.PI;
    flying = {
      fromTheta: theta, fromPhi: phi, fromRadius: radius,
      toTheta: theta + dTheta, toPhi, toRadius: targetRadius,
      start: performance.now(), dur: 900,
    };
    autoRotate = false;
  }

  function advanceFlight(){
    const t = Math.min(1, (performance.now() - flying.start) / flying.dur);
    const ease = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;   // easeInOutQuad
    theta = flying.fromTheta + (flying.toTheta - flying.fromTheta) * ease;
    phi = flying.fromPhi + (flying.toPhi - flying.fromPhi) * ease;
    radius = flying.fromRadius + (flying.toRadius - flying.fromRadius) * ease;
    if (t >= 1) flying = null;
  }

  function wireControls(){
    // moved 用「起點到目前位置」的直線距離（淨位移），不要用逐段位移累加——
    // 累加會把滑鼠/觸控自然的細微抖動也算進去，正常點擊也常常一路累加到
    // 超過門檻，導致 pick() 幾乎永遠不會被觸發。
    let dragging = false, moved = 0, startX = 0, startY = 0, lastX = 0, lastY = 0, pinchDist = 0;
    const pointers = new Map();
    canvas.addEventListener("pointerdown", e => {
      pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
      dragging = true; moved = 0;
      startX = lastX = e.clientX; startY = lastY = e.clientY;
      canvas.setPointerCapture(e.pointerId);
      flying = null;
      pauseAutoRotate();
    });
    canvas.addEventListener("pointermove", e => {
      if (pointers.has(e.pointerId)) pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (pointers.size === 2){
        const [a, b] = [...pointers.values()];
        const d = Math.hypot(a.x - b.x, a.y - b.y);
        if (pinchDist > 0) radius *= pinchDist / d;
        pinchDist = d; moved = 99;
        return;
      }
      if (!dragging) return;
      const dx = e.clientX - lastX, dy = e.clientY - lastY;
      theta += dx * 0.006; phi -= dy * 0.006;
      lastX = e.clientX; lastY = e.clientY;
      moved = Math.hypot(e.clientX - startX, e.clientY - startY);
    });
    function endPointer(e){
      pointers.delete(e.pointerId);
      if (pointers.size < 2) pinchDist = 0;
      if (pointers.size === 0){
        dragging = false;
        if (moved < 10) pick(e.clientX, e.clientY);
      }
    }
    canvas.addEventListener("pointerup", endPointer);
    canvas.addEventListener("pointercancel", endPointer);
    canvas.addEventListener("wheel", e => {
      e.preventDefault();
      flying = null;
      radius *= (1 + Math.sign(e.deltaY) * 0.1);
    }, { passive: false });
  }

  function projectMarker(m, rect, camDir){
    const normal = m.mesh.position.clone().normalize();
    if (normal.dot(camDir) < 0.08) return null;   // 背向鏡頭（地球另一面），視為被擋住
    const proj = m.mesh.position.clone().project(camera);
    if (proj.z > 1) return null;
    return { sx: (proj.x * 0.5 + 0.5) * rect.width, sy: (-proj.y * 0.5 + 0.5) * rect.height };
  }

  // 點位判定：用螢幕座標最近點而非 3D 光線投射，因為標記點半徑很小、
  // 縮放時投影尺寸又會跟著變化，光線投射常常「點了但沒中」；
  // 固定像素容許誤差不受縮放影響，點擊手感穩定得多。label 模式下優先比對
  // 牽引線移開後的大頭針位置（使用者實際會去點的地方）。
  function pick(cx, cy){
    if (!markers.length) return;
    const rect = canvas.getBoundingClientRect();
    const localX = cx - rect.left, localY = cy - rect.top;
    const HIT_PX = 16;
    let best = null, bestDist = HIT_PX;

    if (labelPositions.size){
      markers.forEach(m => {
        const lp = labelPositions.get(m.id);
        if (!lp) return;
        const dist = Math.hypot(lp.sx - localX, lp.sy - localY);
        if (dist < bestDist){ bestDist = dist; best = m; }
      });
      if (best){ flyTo(best.lat, best.lon, 1.7); showGroundPatch(best.lat, best.lon); if (onPick) onPick(best.id); return; }
    }

    const camDir = camera.position.clone().normalize();
    markers.forEach(m => {
      const p = projectMarker(m, rect, camDir);
      if (!p) return;
      const dist = Math.hypot(p.sx - localX, p.sy - localY);
      if (dist < bestDist){ bestDist = dist; best = m; }
    });
    if (best){
      flyTo(best.lat, best.lon, 1.7);
      showGroundPatch(best.lat, best.lon);
      if (onPick) onPick(best.id);
    }
  }

  // 拉近到夠近、候選點數量夠少時，切成「小錨點＋牽引線＋大頭針＋代號」
  // 版面：用貪婪演算法把彼此太近的大頭針依序往外挪開，直到不再重疊。
  function updateLabels(){
    const rect = { width: canvas.clientWidth, height: canvas.clientHeight };
    if (!rect.width || !rect.height) return;
    const camDir = camera.position.clone().normalize();
    const cx0 = rect.width / 2, cy0 = rect.height / 2;

    // 45° 視角下，即使拉得很近，前半球絕大多數點還是會投影到畫面裡的
    // 某處（不會被視角邊界裁掉）——不能只靠「有沒有投影在畫面內」篩選，
    // 否則候選數量幾乎不會隨縮放減少。改成：一律先收集全部候選，
    // 再依「離畫面正中央（=目前鏡頭正對的位置）多近」排序，只取最近的
    // 一批做牽引線版面，其餘維持一般小點顯示，不會整批消失。
    const candidates = [];
    markers.forEach(m => {
      const p = projectMarker(m, rect, camDir);
      if (!p) return;
      const centerDist = Math.hypot(p.sx - cx0, p.sy - cy0);
      candidates.push({ m, ax: p.sx, ay: p.sy, centerDist });
    });

    const active = radius < LABEL_MAX_RADIUS && candidates.length > 0;
    labelPositions.clear();

    if (!active){
      if (svgLabels.childElementCount) svgLabels.innerHTML = "";
      return;
    }

    candidates.sort((a, b) => a.centerDist - b.centerDist);
    const nearby = candidates.slice(0, LABEL_MAX_COUNT);
    nearby.sort((a, b) => (b.m.fav ? 1 : 0) - (a.m.fav ? 1 : 0));
    const placed = [];
    nearby.forEach(c => {
      let lx = c.ax, ly = c.ay - LEADER_LEN, tries = 0;
      // 用黃金角螺旋往外找空位，涵蓋整個圓周（不像 abs(sin) 只會往上偏移，
      // 密集區域很容易探不到真正的空位，導致部分大頭針還是疊在一起）。
      while (tries < 24 && placed.some(p => Math.hypot(p.lx - lx, p.ly - ly) < LABEL_MIN_DIST)){
        const ang = tries * 137.5 * Math.PI / 180;
        const dist = LEADER_LEN + tries * 8;
        lx = c.ax + Math.cos(ang) * dist;
        ly = c.ay + Math.sin(ang) * dist;
        tries++;
      }
      placed.push({ lx, ly, c });
      labelPositions.set(c.m.id, { sx: lx, sy: ly });
    });

    const cyan = themeColor("--cyan", "#6fd3ef"), amber = themeColor("--amber", "#ffb547");
    svgLabels.innerHTML = placed.map(({ lx, ly, c }) => {
      const color = c.m.fav ? amber : cyan;
      const code = c.m.code || "";
      return `
        <line x1="${c.ax.toFixed(1)}" y1="${c.ay.toFixed(1)}" x2="${lx.toFixed(1)}" y2="${ly.toFixed(1)}" stroke="${color}" stroke-width="1" opacity="0.65"/>
        <circle cx="${c.ax.toFixed(1)}" cy="${c.ay.toFixed(1)}" r="1.5" fill="${color}"/>
        <circle cx="${lx.toFixed(1)}" cy="${ly.toFixed(1)}" r="6" fill="${color}" stroke="rgba(0,0,0,.4)" stroke-width="1"/>
        <line x1="${(lx - 12).toFixed(1)}" y1="${(ly + 9.5).toFixed(1)}" x2="${(lx + 12).toFixed(1)}" y2="${(ly + 9.5).toFixed(1)}" stroke="${color}" stroke-width="1"/>
        ${code ? `<text x="${lx.toFixed(1)}" y="${(ly + 22).toFixed(1)}" text-anchor="middle" class="apt-globe-label-text" fill="${color}">${code}</text>` : ""}
      `;
    }).join("");
  }

  function tick(){
    raf = requestAnimationFrame(tick);
    if (flying) advanceFlight();
    else if (autoRotate) theta += 0.0015;
    applyCamera();
    // 每個標記點各自的世界座標尺寸依縮放程度微調（不是整組 Group 縮放——
    // 縮放 Group 連子物件的「位置」也會一起被拉向球心，標記點會被拉進
    // 不透明的地球內部而整批消失，這是先前版本點一放大光點就不見的根因）。
    const s = Math.max(0.5, Math.min(1, radius / DEF_RADIUS));
    // 有牽引線標籤的點，3D 世界裡的球體縮到近乎看不見，只留 2D 小錨點代表
    // 真正座標——不然球體本身（半徑再小也還有實體）疊在錨點上會顯得比
    // 牽引線另一端、真正該醒目的大頭針還大，主從順序整個顛倒。
    markers.forEach(m => m.mesh.scale.setScalar(labelPositions.has(m.id) ? 0.05 : s));
    if (++labelFrame % 3 === 0) updateLabels();
    renderer.render(scene, camera);
  }

  function clearMarkers(){
    markers.forEach(m => markerGroup.remove(m.mesh));
    markers = [];
    labelPositions.clear();
    if (svgLabels) svgLabels.innerHTML = "";
  }

  function setMarkers(points){
    // points: [{ id, lat, lon, fav, code }]
    clearMarkers();
    const geo = new THREE.SphereGeometry(0.016, 8, 6);
    const matAmber = new THREE.MeshBasicMaterial({ color: new THREE.Color(themeColor("--amber", "#ffb547")) });
    const matCyan = new THREE.MeshBasicMaterial({ color: new THREE.Color(themeColor("--cyan", "#6fd3ef")) });
    points.forEach(p => {
      if (p.lat == null || p.lon == null) return;
      const mesh = new THREE.Mesh(geo, p.fav ? matAmber : matCyan);
      mesh.position.copy(latLonToVec3(p.lat, p.lon, 1.02));
      mesh.userData.id = p.id;
      markerGroup.add(mesh);
      markers.push({ mesh, id: p.id, lat: p.lat, lon: p.lon, code: p.code, fav: !!p.fav });
    });
  }

  function setAutoRotate(on){
    if (autoRotate === on) return;
    autoRotate = on;
    if (onRotateChange) onRotateChange(autoRotate);
  }
  function pauseAutoRotate(){ setAutoRotate(false); }
  function resumeAutoRotate(){ setAutoRotate(true); }
  function isAutoRotating(){ return autoRotate; }
  function toggleAutoRotate(){ setAutoRotate(!autoRotate); return autoRotate; }
  function resetView(){
    flying = null;
    theta = DEF_THETA; phi = DEF_PHI; radius = DEF_RADIUS;
  }

  function destroy(){
    if (raf) cancelAnimationFrame(raf);
    raf = 0;
    window.removeEventListener("resize", resize);
  }

  return {
    init, setMarkers, resize, destroy, isReady: () => ready,
    pauseAutoRotate, resumeAutoRotate, isAutoRotating, toggleAutoRotate, resetView,
    clearGroundPatch,
  };
})();
