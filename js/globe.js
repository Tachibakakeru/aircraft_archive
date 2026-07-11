"use strict";
/* ═══════════════════════════════════════════════
   機場 3D 地球檢視 — 惰性載入（首次切到地圖模式才拉 Three.js CDN
   與初始化場景），球體貼衛星影像貼圖（assets/earth_daymap.jpg），
   標示目前篩選結果的機場點位（收藏用琥珀色），點擊開詳情面板並飛向
   該點位。沿用 viewer.js 的拖曳旋轉／滾輪縮放／自動旋轉／重置視角手感。
   ═══════════════════════════════════════════════ */
const AptGlobe = (() => {
  let ready = false, loading = null;
  let scene, camera, renderer, canvas, raf = 0;
  const DEF_THETA = 0.6, DEF_PHI = 1.2, DEF_RADIUS = 3.2;
  let theta = DEF_THETA, phi = DEF_PHI, radius = DEF_RADIUS;
  const RAD_MIN = 1.15, RAD_MAX = 6;
  let autoRotate = true;
  let flying = null;       // { fromTheta,fromPhi,fromRadius, toTheta,toPhi,toRadius, start, dur }
  let markers = [];        // { mesh, id, lat, lon }
  let markerGroup;
  let onPick = null;       // (id) => void
  let onRotateChange = null;   // (isAutoRotating) => void

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
    // 超過門檻，導致 pick() 幾乎永遠不會被觸發（點光點沒反應的根因之一）。
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

  // 點位判定：用螢幕座標最近點而非 3D 光線投射，因為標記點半徑很小、
  // 縮放時投影尺寸又會跟著變化，光線投射常常「點了但沒中」；
  // 固定像素容許誤差不受縮放影響，點擊手感穩定得多。
  function pick(cx, cy){
    if (!markers.length) return;
    const rect = canvas.getBoundingClientRect();
    const camDir = camera.position.clone().normalize();
    const HIT_PX = 16;
    let best = null, bestDist = HIT_PX;
    markers.forEach(m => {
      const normal = m.mesh.position.clone().normalize();
      if (normal.dot(camDir) < 0.08) return;   // 背向鏡頭（地球另一面），視為被擋住
      const proj = m.mesh.position.clone().project(camera);
      if (proj.z > 1) return;
      const sx = rect.left + (proj.x * 0.5 + 0.5) * rect.width;
      const sy = rect.top + (-proj.y * 0.5 + 0.5) * rect.height;
      const dist = Math.hypot(sx - cx, sy - cy);
      if (dist < bestDist){ bestDist = dist; best = m; }
    });
    if (best){
      flyTo(best.lat, best.lon, 1.7);
      if (onPick) onPick(best.id);
    }
  }

  function tick(){
    raf = requestAnimationFrame(tick);
    if (flying) advanceFlight();
    else if (autoRotate) theta += 0.0015;
    applyCamera();
    // 縮放時標記點跟著等比縮小/放大：拉近時同一批機場間的螢幕間距會自然
    // 變大，藉此把原本擠在一起看不清楚的光點分開；縮放同時稍微限制點的
    // 世界座標尺寸，避免拉到很近時光點膨脹成一大坨。
    const s = Math.max(0.35, Math.min(1, (radius - 1) / (DEF_RADIUS - 1)));
    markerGroup.scale.setScalar(s);
    renderer.render(scene, camera);
  }

  function clearMarkers(){
    markers.forEach(m => markerGroup.remove(m.mesh));
    markers = [];
  }

  function setMarkers(points){
    // points: [{ id, lat, lon, fav }]
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
      markers.push({ mesh, id: p.id, lat: p.lat, lon: p.lon });
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
  };
})();
