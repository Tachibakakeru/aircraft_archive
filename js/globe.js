"use strict";
/* ═══════════════════════════════════════════════
   機場 3D 地球檢視 — 惰性載入（首次切到地圖模式才拉 Three.js CDN
   與初始化場景），標示目前篩選結果的機場點位，點擊開詳情面板。
   沿用 viewer.js 的拖曳旋轉／滾輪縮放手感與站台既有的深色科技風格
   （格線球體＋色點），不使用真實地球材質貼圖。
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

    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);

    scene.add(new THREE.AmbientLight(0xffffff, 0.9));

    // 實心暗色球體（機場密度視覺參考底）
    const core = new THREE.Mesh(
      new THREE.SphereGeometry(1, 48, 32),
      new THREE.MeshBasicMaterial({ color: new THREE.Color(themeColor("--bg-1", "#141b2b")) })
    );
    scene.add(core);

    // 格線球體（經緯線，科技感輪廓）—— 用 --cyan 而非 --stroke，
    // 因為 --stroke 是帶 alpha 的 rgba()，THREE.Color 不支援 alpha
    // 通道會發出警告；透明度改用 material 自己的 opacity 控制。
    const grid = new THREE.Mesh(
      new THREE.SphereGeometry(1.001, 24, 16),
      new THREE.MeshBasicMaterial({
        color: new THREE.Color(themeColor("--cyan", "#6fd3ef")),
        wireframe: true, transparent: true, opacity: 0.25,
      })
    );
    scene.add(grid);

    markerGroup = new THREE.Group();
    scene.add(markerGroup);

    raycaster = new THREE.Raycaster();

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

  let raycaster = null;
  function pick(cx, cy){
    if (!raycaster) return;
    const rect = canvas.getBoundingClientRect();
    const ndc = new THREE.Vector2(
      ((cx - rect.left) / rect.width) * 2 - 1,
      -((cy - rect.top) / rect.height) * 2 + 1
    );
    raycaster.setFromCamera(ndc, camera);
    const hits = raycaster.intersectObjects(markerGroup.children);
    if (hits.length && onPick) onPick(hits[0].object.userData.id);
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
    const geo = new THREE.SphereGeometry(0.012, 8, 6);
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
