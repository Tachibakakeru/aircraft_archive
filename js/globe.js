"use strict";
/* ═══════════════════════════════════════════════
   機場 3D 地球檢視 — 惰性載入（首次切到地圖模式才拉 Three.js CDN
   與初始化場景），球體貼衛星影像貼圖（assets/earth_daymap.jpg），
   標示目前篩選結果的機場點位（收藏用琥珀色），點擊開詳情面板。
   沿用 viewer.js 的拖曳旋轉／滾輪縮放手感。
   ═══════════════════════════════════════════════ */
const AptGlobe = (() => {
  let ready = false, loading = null;
  let scene, camera, renderer, canvas, raf = 0;
  let theta = 0.6, phi = 1.2, radius = 3.2;
  const RAD_MIN = 1.6, RAD_MAX = 6;
  let autoRotate = true;
  let markers = [];        // { mesh, id }
  let markerGroup;
  let onPick = null;       // (id) => void

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

  async function init(container, pickCallback){
    onPick = pickCallback;
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

    // 實心球體貼衛星影像（NASA Blue Marble 日照面合成圖，經緯度等距投影）
    const earthTex = new THREE.TextureLoader().load("assets/earth_daymap.jpg");
    earthTex.encoding = THREE.sRGBEncoding;
    const core = new THREE.Mesh(
      new THREE.SphereGeometry(1, 48, 32),
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

  function wireControls(){
    let dragging = false, moved = 0, lastX = 0, lastY = 0, pinchDist = 0;
    const pointers = new Map();
    canvas.addEventListener("pointerdown", e => {
      pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
      dragging = true; moved = 0; lastX = e.clientX; lastY = e.clientY;
      canvas.setPointerCapture(e.pointerId);
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
      moved += Math.abs(dx) + Math.abs(dy);
      theta += dx * 0.006; phi -= dy * 0.006;
      lastX = e.clientX; lastY = e.clientY;
    });
    function endPointer(e){
      pointers.delete(e.pointerId);
      if (pointers.size < 2) pinchDist = 0;
      if (pointers.size === 0){
        dragging = false;
        if (moved < 6) pick(e.clientX, e.clientY);
      }
    }
    canvas.addEventListener("pointerup", endPointer);
    canvas.addEventListener("pointercancel", endPointer);
    canvas.addEventListener("wheel", e => {
      e.preventDefault();
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
    if (best && onPick) onPick(best.id);
  }

  function tick(){
    raf = requestAnimationFrame(tick);
    if (autoRotate) theta += 0.0015;
    applyCamera();
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
      markers.push({ mesh, id: p.id });
    });
  }

  function pauseAutoRotate(){ autoRotate = false; }
  function resumeAutoRotate(){ autoRotate = true; }

  function destroy(){
    if (raf) cancelAnimationFrame(raf);
    raf = 0;
    window.removeEventListener("resize", resize);
  }

  return { init, setMarkers, resize, pauseAutoRotate, resumeAutoRotate, destroy, isReady: () => ready };
})();
