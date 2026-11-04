"use strict";
/* ═══════════════════════════════════════════════
   跑道進度條（2026-11）：大檔載入時，飛機沿跑道依下載進度滑行，載完時加速、拉起離場。
   樣式在 css/style.css「跑道進度條」段落。

   用法：
     const rw = Runway.mount(el, { label: "下載機場資料" });
     const json = await Runway.fetchJSON(url, rw, { expectedBytes });   // 邊下載邊更新進度
     rw.takeoff();                                                      // 起飛動畫後自動隱藏
     rw.fail(message);                                                  // 失敗時顯示訊息

   進度：瀏覽器讀取回應串流的位元組數。Cloudflare 會壓縮傳輸，此時 Content-Length 是壓縮後大小、
   串流讀到的是解壓後大小，所以有壓縮時改用呼叫端提供的 expectedBytes（解壓後大小）估算，最多顯示 98%，
   載完才跳到 100% 起飛。瀏覽器不支援串流讀取時退回一般 fetch（進度條改為緩慢前進的估計）。
   ═══════════════════════════════════════════════ */
const Runway = (() => {
  const PLANE = "M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z";
  const mb = n => (n / 1048576).toFixed(1);

  function mount(el, { label = "" } = {}){
    el.classList.add("rwy");
    el.removeAttribute("data-ico");
    el.hidden = false;
    el.setAttribute("role", "progressbar");
    el.setAttribute("aria-valuemin", "0"); el.setAttribute("aria-valuemax", "100"); el.setAttribute("aria-valuenow", "0");
    el.innerHTML = `<div class="rwy-strip">
        <span class="rwy-num rwy-num-a">09</span><span class="rwy-num rwy-num-b">27</span>
        <span class="rwy-center"></span><span class="rwy-roll"></span>
        <span class="rwy-plane"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="${PLANE}"/></svg></span>
      </div>
      <div class="rwy-text"><b class="rwy-label"></b><span class="rwy-stat"></span></div>`;
    const plane = el.querySelector(".rwy-plane"), roll = el.querySelector(".rwy-roll");
    el.querySelector(".rwy-label").textContent = label;
    let shown = 0, target = 0, raf = 0, stat = "", lastB = 0, lastT = 0;
    // 平滑跟上實際進度，不會一格一格跳
    const step = () => {
      shown += (target - shown) * .18;
      if (Math.abs(target - shown) < .001) shown = target;
      const pct = shown * 100;
      plane.style.left = `calc(${(4 + pct * .86).toFixed(2)}% )`;
      roll.style.width = `${(4 + pct * .86).toFixed(2)}%`;
      raf = shown !== target ? requestAnimationFrame(step) : 0;
    };
    const api = {
      set(p, bytes, total){
        target = Math.max(target, Math.min(1, p));
        el.setAttribute("aria-valuenow", String(Math.round(target * 100)));
        if (total){ lastB = bytes; lastT = total; }
        if (target >= 1 && lastT) lastB = lastT;
        stat = lastT ? `${mb(lastB)} / ${mb(lastT)} MB · ${Math.round(target * 100)}%` : `${Math.round(target * 100)}%`;
        el.querySelector(".rwy-stat").textContent = stat;
        if (!raf) raf = requestAnimationFrame(step);
      },
      label(text){ el.querySelector(".rwy-label").textContent = text; },
      // 起飛：衝到跑道尾端、機頭上仰、爬升淡出，然後整個進度條收起
      takeoff(){
        return new Promise(resolve => {
          api.set(1);
          setTimeout(() => {
            el.classList.add("rwy-takeoff");
            setTimeout(() => { el.classList.add("rwy-gone"); setTimeout(() => { el.hidden = true; el.classList.remove("rwy-takeoff", "rwy-gone"); resolve(); }, 380); }, 900);
          }, 380);
        });
      },
      fail(msg){
        cancelAnimationFrame(raf);
        el.classList.add("rwy-fail");
        el.querySelector(".rwy-label").textContent = msg;
        el.querySelector(".rwy-stat").textContent = "";
      }
    };
    return api;
  }

  async function fetchJSON(url, rw, { expectedBytes = 0 } = {}){
    const res = await fetch(url);
    if (!res.ok) throw new Error(res.status);
    const enc = res.headers.get("content-encoding");
    const len = +res.headers.get("content-length") || 0;
    const total = (!enc || enc === "identity") && len ? len : (expectedBytes || len);
    if (!res.body || !res.body.getReader || !total){
      // 無法讀串流：用時間估計慢慢前進到 90%
      let fake = 0;
      const tm = setInterval(() => { fake += (0.9 - fake) * .08; rw && rw.set(fake); }, 200);
      try { return await res.json(); } finally { clearInterval(tm); }
    }
    const reader = res.body.getReader(), chunks = [];
    let got = 0;
    for (;;){
      const { done, value } = await reader.read();
      if (done) break;
      chunks.push(value); got += value.length;
      if (rw) rw.set(Math.min(.98, got / total), got, Math.max(total, got));
    }
    const buf = new Uint8Array(got);
    let off = 0;
    for (const c of chunks){ buf.set(c, off); off += c.length; }
    if (rw) rw.set(.99, got, got);
    return JSON.parse(new TextDecoder("utf-8").decode(buf));
  }

  return { mount, fetchJSON };
})();
