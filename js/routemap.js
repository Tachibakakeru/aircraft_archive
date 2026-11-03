"use strict";
/* ═══════════════════════════════════════════════
   航線動畫地圖（首頁右上角「隨機航線」與「航線規劃」畫面共用）

   - 底圖：data/landmask.json（由 tools/build_landmask.py 從 NASA Blue Marble 產生的 0.5° 陸地遮罩）
     畫成點陣世界地圖（canvas）。依每條航線自動取景：以大圓航線的範圍加留白，等距圓柱投影。
   - 航線：沿大圓計算 96 個點，投影到畫面後再往「北側」加一點弧度，看起來像航空公司的航線圖。
   - 一趟的動畫順序：起降機場出現 → 虛線航線從起點畫到終點 → 飛機沿航線飛行，飛過的部分變實線
     → 抵達後終點脈動、停留 → 淡出換下一趟（由呼叫端決定下一趟）。
   - 尊重 prefers-reduced-motion：直接顯示完成狀態（實線＋飛機停在終點前）。

   用法：
     const map = RouteMap.create(containerEl, { dotColor: "--sky-ink", ... });
     await map.play(fromAirport, toAirport);      // 播完一趟（含抵達停留）後 resolve
     map.show(fromAirport, toAirport);            // 不播動畫，直接顯示
     map.stop();
   機場物件需有 { lat, lon, code, label }。
   ═══════════════════════════════════════════════ */
const RouteMap = (() => {
  const REDUCED = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const PLANE = "M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z";
  let maskPromise = null;
  let uid = 0;

  // 陸地遮罩：run-length 解碼成 Uint8Array（1 = 陸地）
  function loadMask(){
    if (maskPromise) return maskPromise;
    maskPromise = fetch("data/landmask.json?v=1").then(r => r.json()).then(m => {
      const bits = new Uint8Array(m.w * m.h);
      m.rows.forEach((row, j) => {
        let x = 0, land = 0;
        row.split(",").forEach(s => {
          const n = parseInt(s, 36);
          if (land) bits.fill(1, j * m.w + x, j * m.w + x + n);
          x += n; land ^= 1;
        });
      });
      return { w: m.w, h: m.h, res: m.res, bits };
    }).catch(() => null);
    return maskPromise;
  }
  const isLand = (mask, lat, lon) => {
    if (!mask || lat > 90 || lat < -90) return false;
    lon = ((lon + 180) % 360 + 360) % 360 - 180;
    const i = Math.min(mask.w - 1, Math.floor((lon + 180) / mask.res));
    const j = Math.min(mask.h - 1, Math.floor((90 - lat) / mask.res));
    return mask.bits[j * mask.w + i] === 1;
  };

  // 大圓距離（km）與沿途點
  const R = 6371, D2R = Math.PI / 180;
  function gcKm(a, b){
    const dLat = (b.lat - a.lat) * D2R, dLon = (b.lon - a.lon) * D2R;
    const h = Math.sin(dLat / 2) ** 2 + Math.cos(a.lat * D2R) * Math.cos(b.lat * D2R) * Math.sin(dLon / 2) ** 2;
    return 2 * R * Math.asin(Math.min(1, Math.sqrt(h)));
  }
  function gcPoints(a, b, n){
    const toV = p => [Math.cos(p.lat * D2R) * Math.cos(p.lon * D2R), Math.cos(p.lat * D2R) * Math.sin(p.lon * D2R), Math.sin(p.lat * D2R)];
    const A = toV(a), B = toV(b);
    const dot = Math.max(-1, Math.min(1, A[0] * B[0] + A[1] * B[1] + A[2] * B[2]));
    const w = Math.acos(dot), out = [];
    let prevLon = a.lon;
    for (let k = 0; k <= n; k++){
      const t = k / n;
      let v;
      if (w < 1e-6) v = A;
      else {
        const s1 = Math.sin((1 - t) * w) / Math.sin(w), s2 = Math.sin(t * w) / Math.sin(w);
        v = [s1 * A[0] + s2 * B[0], s1 * A[1] + s2 * B[1], s1 * A[2] + s2 * B[2]];
      }
      const lat = Math.atan2(v[2], Math.hypot(v[0], v[1])) / D2R;
      let lon = Math.atan2(v[1], v[0]) / D2R;
      while (lon - prevLon > 180) lon -= 360;      // 跨換日線時讓經度連續，不在畫面上折返
      while (lon - prevLon < -180) lon += 360;
      prevLon = lon;
      out.push({ lat, lon });
    }
    return out;
  }
  // 起始真航向（度）
  function bearing(a, b){
    const φ1 = a.lat * D2R, φ2 = b.lat * D2R, Δλ = (b.lon - a.lon) * D2R;
    const y = Math.sin(Δλ) * Math.cos(φ2), x = Math.cos(φ1) * Math.sin(φ2) - Math.sin(φ1) * Math.cos(φ2) * Math.cos(Δλ);
    return (Math.atan2(y, x) / D2R + 360) % 360;
  }

  const css = (el, name, fb) => getComputedStyle(el).getPropertyValue(name).trim() || fb;
  const ease = p => p < .5 ? 2 * p * p : 1 - (-2 * p + 2) ** 2 / 2;
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const frame = () => new Promise(r => requestAnimationFrame(r));

  function create(container, opts = {}){
    const o = Object.assign({
      dotColor: "--sky-ink", dotAlpha: .4, lineColor: "--sky-ink", labelColor: "--sky-ink", subColor: "--sky-muted",
      airportFill: "--sky-1", gap: 9, bulge: .12, minSpan: 34, pad: .2
    }, opts);
    const id = ++uid;
    container.classList.add("routemap");
    container.innerHTML = `<canvas class="rm-dots" aria-hidden="true"></canvas>
      <svg class="rm-svg" aria-hidden="true">
        <defs><mask id="rm-mask-${id}" maskUnits="userSpaceOnUse"><path class="rm-maskpath" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round"/></mask></defs>
        <g class="rm-route">
          <path class="rm-track" fill="none" mask="url(#rm-mask-${id})"/>
          <path class="rm-flown" fill="none"/>
          <g class="rm-apt rm-from"><circle class="rm-ring" r="8"/><circle class="rm-dot" r="6.5"/><text class="rm-code"/><text class="rm-sub"/></g>
          <g class="rm-apt rm-to"><circle class="rm-ring" r="8"/><circle class="rm-dot" r="6.5"/><text class="rm-code"/><text class="rm-sub"/></g>
          <g class="rm-plane"><path d="${PLANE}" transform="translate(-15 -15) scale(1.25) rotate(90 12 12)"/></g>
        </g>
      </svg>`;
    const canvas = container.querySelector("canvas"), svg = container.querySelector("svg");
    const q = s => svg.querySelector(s);
    const track = q(".rm-track"), flown = q(".rm-flown"), maskPath = q(".rm-maskpath"), plane = q(".rm-plane"), route = q(".rm-route");
    let W = 0, H = 0, len = 0, token = 0, current = null, last = [1, 1];

    function measure(){
      const r = container.getBoundingClientRect();
      W = Math.max(200, Math.round(r.width)); H = Math.max(120, Math.round(r.height));
      const dpr = Math.min(2, window.devicePixelRatio || 1);
      canvas.width = W * dpr; canvas.height = H * dpr;
      canvas.style.width = W + "px"; canvas.style.height = H + "px";
      canvas.getContext("2d").setTransform(dpr, 0, 0, dpr, 0, 0);
      svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
    }

    // 取景：依航線範圍決定投影（px/度）與中心
    function frameFor(pts){
      let minLon = Infinity, maxLon = -Infinity, minLat = Infinity, maxLat = -Infinity;
      pts.forEach(p => { minLon = Math.min(minLon, p.lon); maxLon = Math.max(maxLon, p.lon); minLat = Math.min(minLat, p.lat); maxLat = Math.max(maxLat, p.lat); });
      let lonSpan = Math.max(o.minSpan, (maxLon - minLon) * (1 + o.pad * 2));
      let latSpan = Math.max(o.minSpan * H / W, (maxLat - minLat) * (1 + o.pad * 2) + 10);   // 上方多留弧度空間
      const s = Math.min(W / lonSpan, H / latSpan);
      const cLon = (minLon + maxLon) / 2;
      let cLat = (minLat + maxLat) / 2 + 2;
      // 長程航線縮得很小時，畫面上下可能超出 ±85°（那裡沒有陸地，只剩空白），把中心往回推
      const halfLat = H / 2 / s;
      if (halfLat < 85){ cLat = Math.min(cLat, 85 - halfLat); cLat = Math.max(cLat, -85 + halfLat); }
      else cLat = 0;
      return { s, cLon, cLat };
    }
    const proj = (f, p) => ({ x: W / 2 + (p.lon - f.cLon) * f.s, y: H / 2 - (p.lat - f.cLat) * f.s });

    function drawDots(f, mask){
      const ctx = canvas.getContext("2d");
      ctx.clearRect(0, 0, W, H);
      if (!mask) return;
      ctx.fillStyle = css(container, o.dotColor, "#fff");
      ctx.globalAlpha = o.dotAlpha;
      const g = o.gap, rad = Math.max(1, g * .17);
      for (let y = g / 2; y < H; y += g){
        for (let x = g / 2; x < W; x += g){
          const lon = f.cLon + (x - W / 2) / f.s, lat = f.cLat - (y - H / 2) / f.s;
          if (isLand(mask, lat, lon)){ ctx.beginPath(); ctx.arc(x, y, rad, 0, Math.PI * 2); ctx.fill(); }
        }
      }
      ctx.globalAlpha = 1;
    }

    function bulged(f, pts, km = 0){
      const xy = pts.map(p => proj(f, p));
      // 弧度：沿起訖連線的垂直方向（偏北／畫面上方）推出去，中間最高
      const p0 = xy[0], p1 = xy[xy.length - 1];
      const dx = p1.x - p0.x, dy = p1.y - p0.y, L = Math.hypot(dx, dy) || 1;
      let nx = -dy / L, ny = dx / L;
      if (ny > 0){ nx = -nx; ny = -ny; }
      const k = o.bulge * L * (1 - .7 * Math.min(1, km / 12000));   // 長程航線本身就有大圓弧度，少推一點
      xy.forEach((p, i) => { const t = i / (xy.length - 1), h = Math.sin(Math.PI * t) * k; p.x += nx * h; p.y += ny * h; });
      return xy;
    }
    function layout(a, b){
      const pts = gcPoints(a, b, 96), km = gcKm(a, b);
      let f = frameFor(pts);
      let xy = bulged(f, pts, km);
      // 第二次取景：把加上弧度後的航線整條放進畫面（上下左右留邊給機場標籤）
      const mx = 56, my = 52;
      let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
      xy.forEach(p => { x0 = Math.min(x0, p.x); x1 = Math.max(x1, p.x); y0 = Math.min(y0, p.y); y1 = Math.max(y1, p.y); });
      const k = Math.min(1, (W - 2 * mx) / Math.max(1, x1 - x0), (H - 2 * my) / Math.max(1, y1 - y0));
      const bx = (x0 + x1) / 2, by = (y0 + y1) / 2;
      if (k < 1 || x0 < mx || x1 > W - mx || y0 < my || y1 > H - my){
        f = { s: f.s * k, cLon: f.cLon + (bx - W / 2) / f.s, cLat: f.cLat - (by - H / 2) / f.s };
        xy = bulged(f, pts, km);
      }
      // 畫面上緣若超過北緯 90°（上方一片空白），在航線仍完整可見的前提下把畫面往北推回
      const over = f.cLat + H / 2 / f.s - 88;
      if (over > 0){
        const shifted = { ...f, cLat: f.cLat - over };
        const xy2 = bulged(shifted, pts, km);
        if (Math.min(...xy2.map(p => p.y)) >= 14) { f = shifted; xy = xy2; }
      }
      return { f, xy };
    }

    // 標籤放在「航線進出方向的另一側」：航線從上方進來就把文字放下方，反之放上方，避免壓到航線
    function placeLabel(g, p, neighbor){
      const code = g.querySelector(".rm-code"), sub = g.querySelector(".rm-sub");
      let below = neighbor.y < p.y;
      if (p.y < 52) below = true;
      if (p.y > H - 46) below = false;
      const codeY = below ? p.y + 30 : p.y - 30, subY = below ? p.y + 45 : p.y - 15;
      let anchor = "middle";
      if (p.x < 60) anchor = "start"; else if (p.x > W - 60) anchor = "end";
      const tx = anchor === "start" ? p.x - 8 : anchor === "end" ? p.x + 8 : p.x;
      [code, sub].forEach(t => t.setAttribute("text-anchor", anchor));
      code.setAttribute("x", tx); code.setAttribute("y", codeY);
      sub.setAttribute("x", tx); sub.setAttribute("y", subY);
    }

    function render(a, b, mask){
      measure();
      const { f, xy } = layout(a, b);
      drawDots(f, mask);
      const d = "M" + xy.map(p => `${p.x.toFixed(1)} ${p.y.toFixed(1)}`).join(" L");
      [track, flown, maskPath].forEach(p => p.setAttribute("d", d));
      len = flown.getTotalLength();
      const set = (sel, pt, apt, other) => {
        const g = q(sel);
        g.setAttribute("transform", "");
        g.querySelectorAll("circle").forEach(c => { c.setAttribute("cx", pt.x); c.setAttribute("cy", pt.y); });
        g.querySelector(".rm-code").textContent = apt.code || "";
        g.querySelector(".rm-sub").textContent = apt.label || "";
        placeLabel(g, pt, other);
      };
      set(".rm-from", xy[0], a, xy[6]);
      set(".rm-to", xy[xy.length - 1], b, xy[xy.length - 7]);
      const colors = { line: css(container, o.lineColor, "#fff"), label: css(container, o.labelColor, "#fff"), sub: css(container, o.subColor, "#cfe4ff"), fill: css(container, o.airportFill, "#0f5fd0") };
      svg.style.setProperty("--rm-line", colors.line);
      svg.style.setProperty("--rm-label", colors.label);
      svg.style.setProperty("--rm-sub", colors.sub);
      svg.style.setProperty("--rm-fill", colors.fill);
      return xy;
    }

    function setProgress(drawP, flyP){
      last = [drawP, flyP];
      maskPath.style.strokeDasharray = `${len} ${len}`;
      maskPath.style.strokeDashoffset = String(len * (1 - drawP));
      flown.style.strokeDasharray = `${len} ${len}`;
      flown.style.strokeDashoffset = String(len * (1 - flyP));
      const L = Math.max(0, Math.min(len, len * flyP));
      const p = flown.getPointAtLength(L), p2 = flown.getPointAtLength(Math.min(len, L + 1)), pb = flown.getPointAtLength(Math.max(0, L - 1));
      const ang = (L >= len ? Math.atan2(p.y - pb.y, p.x - pb.x) : Math.atan2(p2.y - p.y, p2.x - p.x)) * 180 / Math.PI;
      plane.setAttribute("transform", `translate(${p.x} ${p.y}) rotate(${ang})`);
      plane.style.opacity = drawP >= 1 ? 1 : 0;
    }

    async function tween(ms, fn, my){
      const t0 = performance.now();
      for (;;){
        await frame();
        if (my !== token) return false;
        const p = Math.min(1, (performance.now() - t0) / ms);
        fn(p);
        if (p >= 1) return true;
      }
    }

    async function play(a, b, onShow){
      const my = ++token;
      current = { a, b };
      const mask = await loadMask();
      if (my !== token) return false;
      route.classList.remove("rm-arrived");
      container.classList.add("rm-fading");
      await wait(REDUCED ? 0 : 280);
      if (my !== token) return false;
      render(a, b, mask);
      setProgress(0, 0);
      if (onShow) onShow();
      container.classList.remove("rm-fading");
      if (REDUCED){ setProgress(1, .97); route.classList.add("rm-arrived"); await wait(4000); return my === token; }
      await wait(380);
      if (!await tween(900, p => setProgress(ease(p), 0), my)) return false;
      const km = gcKm(a, b);
      const dur = Math.max(4800, Math.min(9000, 4200 + km * .32));
      if (!await tween(dur, p => setProgress(1, ease(p)), my)) return false;
      route.classList.add("rm-arrived");
      await wait(1600);
      return my === token;
    }

    async function show(a, b){
      const my = ++token;
      current = { a, b };
      const mask = await loadMask();
      if (my !== token) return;
      render(a, b, mask);
      setProgress(1, 1);
      route.classList.add("rm-arrived");
    }

    function stop(){ token++; }
    window.addEventListener("resize", () => {
      if (!current) return;
      loadMask().then(mask => { render(current.a, current.b, mask); setProgress(last[0], last[1]); });
    });

    return { play, show, stop };
  }

  return { create, gcKm, bearing, gcPoints, loadMask };
})();
