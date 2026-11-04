"use strict";
/* ═══════════════════════════════════════════════
   換頁過場動畫（2026-11 試作）：點站內連結時，一架飛機從左側飛過、身後拉出天空布幕蓋住畫面，
   中央顯示「前往 ○○」；新頁面載入時，布幕跟著第二架飛機往右滑開，露出新頁面。
   - 只攔截同網站、同分頁的一般連結；新分頁、下載、外部連結、#錨點、按住 Ctrl／⌘／Shift／中鍵都不攔截。
   - 布幕顏色用當下的天空變數（--sky-1/2/3），所以會跟著時段（js/skytime.js）與深淺色變化。
   - 抵達動畫：前一頁在 sessionStorage 留下標記（3 秒內有效），新頁面在 <head> 執行本檔時就先蓋上布幕，
     避免新頁面先閃一下再被蓋住。
   - 設定：localStorage.hangar_tx = "off" 可關閉（之後可做成開關）。
   樣式在 css/transition.css。本檔請放在 <head>、各頁 CSS 之後。
   ═══════════════════════════════════════════════ */
(function(){
  const KEY = "hangar_tx_arrive", OFF = (() => { try { return localStorage.getItem("hangar_tx") === "off"; } catch (e) { return false; } })();
  const OUT_MS = 520, IN_MS = 620;
  const PLANE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/></svg>';
  const html = document.documentElement;

  // 抵達：一進頁面就先蓋上（CSS 以 html.tx-arriving::before 畫出布幕）
  let arriving = null;
  try {
    const v = JSON.parse(sessionStorage.getItem(KEY) || "null");
    sessionStorage.removeItem(KEY);
    if (v && Date.now() - v.t < 3000 && !OFF){ arriving = v; html.classList.add("tx-arriving"); }
  } catch (e) {}

  const t = (k, fb) => (typeof I18N !== "undefined" ? I18N.t(k) : fb);
  function overlay(label){
    const el = document.createElement("div");
    el.className = "tx";
    el.setAttribute("aria-hidden", "true");
    el.innerHTML = `<div class="tx-curtain"><div class="tx-label"><span class="tx-kicker"></span><b></b></div></div><div class="tx-plane">${PLANE}</div><div class="tx-trail"></div>`;
    el.querySelector(".tx-kicker").textContent = label.kicker;
    el.querySelector("b").textContent = label.name;
    document.body.appendChild(el);
    return el;
  }
  // 依目標頁決定要顯示的名稱
  function nameFor(url, a){
    const page = (url.pathname.split("/").pop() || "index.html").toLowerCase();
    const map = { "index.html": ["home.pass.from", "首頁"], "": ["home.pass.from", "首頁"], "fleet.html": ["home.nav.fleet", "飛行器圖鑑"],
      "airports.html": ["home.nav.airports", "機場與跑道"], "airlines.html": ["home.nav.airlines", "航空公司"], "knowledge.html": ["home.nav.knowledge", "小知識"],
      "distance.html": ["nav.distance", "距離計算"], "compare.html": ["home.tool.compare", "機型比較"], "versus.html": ["nav.versus", "機型對比"],
      "variants.html": ["nav.variants", "機型家族"], "viewer.html": ["tx.viewer", "3D 檢視器"], "editor.html": ["fleet.edit", "編輯資料"] };
    const m = map[page];
    if (m) return t(m[0], m[1]);
    return (a.textContent || "").trim().slice(0, 24) || url.pathname;
  }

  function depart(a, url){
    const name = nameFor(url, a);
    const el = overlay({ kicker: t("tx.departing", "前往"), name });
    requestAnimationFrame(() => el.classList.add("tx-out"));
    if (window.HangarSound) window.HangarSound.chime();   // 座艙音效開啟時播放「叮－咚」
    try { sessionStorage.setItem(KEY, JSON.stringify({ t: Date.now(), name })); } catch (e) {}
    setTimeout(() => { location.href = url.href; }, OUT_MS);
  }

  document.addEventListener("click", e => {
    if (OFF || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    const a = e.target.closest("a[href]");
    if (!a || a.target && a.target !== "_self" || a.hasAttribute("download") || a.dataset.noTx !== undefined) return;
    let url;
    try { url = new URL(a.getAttribute("href"), location.href); } catch (err) { return; }
    if (url.origin !== location.origin) return;
    if (url.pathname === location.pathname && url.search === location.search && url.hash) return;   // 同頁錨點
    if (!/\.html$|\/$/.test(url.pathname)) return;                                                // 只處理頁面，不攔截圖片、JSON 等
    e.preventDefault();
    depart(a, url);
  });

  function arrive(){
    if (!arriving) return;
    const el = overlay({ kicker: t("tx.arrived", "抵達"), name: arriving.name });
    el.classList.add("tx-covered");
    html.classList.remove("tx-arriving");
    requestAnimationFrame(() => requestAnimationFrame(() => el.classList.add("tx-in")));
    setTimeout(() => el.remove(), IN_MS + 80);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", arrive); else arrive();
  // 從上一頁返回（bfcache）時移除殘留的布幕
  window.addEventListener("pageshow", e => { if (e.persisted) document.querySelectorAll(".tx").forEach(x => x.remove()); html.classList.remove("tx-arriving"); });
})();
