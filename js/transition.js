"use strict";
/* ═══════════════════════════════════════════════
   換頁過場動畫（2026-11）：點站內連結時，一架飛機飛過、身後拉出天空布幕蓋住畫面，
   中央顯示「前往 ○○」；新頁面載入時，布幕跟著第二架飛機滑開，露出新頁面。
   - 方向：一般前往是「左 → 右」；回到上一頁是「右 → 左」飛回去，包括
       ・瀏覽器的返回鍵／手勢（新頁面以 navigation type = back_forward 或 bfcache 還原判斷），
       ・站內的「← 返回」連結（class="back"、rel="prev"，或目標就是 document.referrer 那一頁）。
   - 飛機與凝結尾走畫面上方約 30% 的高度，不經過中央的目的地文字。
   - 只攔截同網站、同分頁的一般 .html 連結；新分頁、下載、外部連結、#錨點、按住 Ctrl／⌘／Shift／中鍵都不攔截。
   - 布幕顏色用當下的天空變數（--sky-1/2/3），會跟著時段（js/skytime.js）與深淺色變化。
   - 抵達：前一頁在 sessionStorage 留下標記（3 秒內有效；點連結時在 click，按返回鍵時在 pagehide），
     新頁面在 <head> 執行本檔時就先蓋上布幕，避免新頁面先閃一下再被蓋住。重新整理不播放。
   - 座艙音效（js/extras.js）開啟時，離開動畫期間播放「叮－咚」，並在換頁前淡出，不會突然斷掉。
   - 設定：localStorage.hangar_tx = "off" 可關閉。
   樣式在 css/transition.css。本檔請放在 <head>、各頁 CSS 之後。
   ═══════════════════════════════════════════════ */
(function(){
  const KEY = "hangar_tx_arrive", OFF = (() => { try { return localStorage.getItem("hangar_tx") === "off"; } catch (e) { return false; } })();
  const OUT_MS = 900, IN_MS = 1000;   // 離開／抵達動畫長度（與 css/transition.css 的 transition 時間一致）
  const PLANE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/></svg>';
  const html = document.documentElement;
  const t = (k, fb) => (typeof I18N !== "undefined" ? I18N.t(k) : fb);
  const navType = (() => { try { return (performance.getEntriesByType("navigation")[0] || {}).type || ""; } catch (e) { return ""; } })();

  function readFlag(){
    try {
      const v = JSON.parse(sessionStorage.getItem(KEY) || "null");
      sessionStorage.removeItem(KEY);
      return v && Date.now() - v.t < 3000 ? v : null;
    } catch (e) { return null; }
  }
  const setFlag = v => { try { sessionStorage.setItem(KEY, JSON.stringify(v)); } catch (e) {} };

  // 頁面代號：Cloudflare Pages 會把 /airlines.html 轉址成 /airlines，兩種寫法都要認得
  const pageKey = path => { const k = (path.split("/").pop() || "index").replace(/\.html$/i, "").toLowerCase(); return k || "index"; };
  const samePage = (a, b) => a.origin === b.origin && pageKey(a.pathname) === pageKey(b.pathname) && a.search === b.search;
  // 正式站用乾淨網址時，直接前往去掉 .html 的網址，省掉一次 308 轉址（本機 server.py 不支援乾淨網址，維持原樣）
  const cleanUrls = !/\.html$/i.test(location.pathname) && location.pathname !== "/" && !/^(localhost|127\.)/.test(location.hostname);
  function targetHref(url){
    if (!cleanUrls || !/\.html$/i.test(url.pathname)) return url.href;
    const u = new URL(url.href);
    u.pathname = /\/index\.html$/i.test(u.pathname) ? u.pathname.replace(/index\.html$/i, "") : u.pathname.replace(/\.html$/i, "");
    return u.href;
  }
  // 依頁面決定要顯示的名稱
  function nameFor(url, a){
    const map = { "index": ["home.pass.from", "首頁"], "fleet": ["home.nav.fleet", "飛行器圖鑑"],
      "airports": ["home.nav.airports", "機場與跑道"], "airlines": ["home.nav.airlines", "航空公司"], "knowledge": ["home.nav.knowledge", "小知識"],
      "distance": ["nav.distance", "距離計算"], "compare": ["home.tool.compare", "機型比較"], "versus": ["nav.versus", "機型對比"],
      "variants": ["nav.variants", "機型家族"], "viewer": ["tx.viewer", "3D 檢視器"], "editor": ["fleet.edit", "編輯資料"] };
    const m = map[pageKey(url.pathname)];
    if (m) return t(m[0], m[1]);
    return ((a && a.textContent) || "").trim().slice(0, 24) || "SKY ARCHIVE";
  }

  // 抵達：一進頁面就先蓋上（CSS 以 html.tx-arriving::before 畫出布幕）
  let arriving = null;
  const flag = readFlag();
  if (!OFF && navType !== "reload"){
    if (flag && flag.click) arriving = { name: flag.name, back: !!flag.back };
    else if (flag && navType === "back_forward") arriving = { name: nameFor(location), back: true };
  }
  if (arriving) html.classList.add("tx-arriving");

  function overlay(label, back){
    const el = document.createElement("div");
    el.className = "tx" + (back ? " tx-rev" : "");
    el.setAttribute("aria-hidden", "true");
    el.innerHTML = `<div class="tx-curtain"><div class="tx-label"><span class="tx-kicker"></span><b></b></div></div><div class="tx-plane"><div class="tx-trail"></div>${PLANE}</div>`;
    el.querySelector(".tx-kicker").textContent = label.kicker;
    el.querySelector("b").textContent = label.name;
    document.body.appendChild(el);
    return el;
  }

  function isBack(a, url){
    if (a.classList.contains("back") || /\bprev\b/.test(a.rel || "")) return true;
    try { return samePage(new URL(document.referrer), url); } catch (e) { return false; }
  }

  let leaving = false;
  function depart(a, url){
    leaving = true;
    const back = isBack(a, url), name = nameFor(url, a);
    const el = overlay({ kicker: t(back ? "tx.returning" : "tx.departing", back ? "返回" : "前往"), name }, back);
    requestAnimationFrame(() => requestAnimationFrame(() => el.classList.add("tx-out")));
    if (window.HangarSound) window.HangarSound.chime({ within: OUT_MS });   // 開啟音效時播放，換頁前淡出
    setFlag({ t: Date.now(), name, back, click: true });
    setTimeout(() => { location.href = targetHref(url); }, OUT_MS);
  }

  document.addEventListener("click", e => {
    if (OFF || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    const a = e.target.closest("a[href]");
    if (!a || a.target && a.target !== "_self" || a.hasAttribute("download") || a.dataset.noTx !== undefined) return;
    let url;
    try { url = new URL(a.getAttribute("href"), location.href); } catch (err) { return; }
    if (url.origin !== location.origin) return;
    if (url.pathname === location.pathname && url.search === location.search && url.hash) return;   // 同頁錨點
    const last = url.pathname.split("/").pop();
    if (last.includes(".") && !/\.html$/i.test(last)) return;                                    // 只處理頁面，不攔截圖片、JSON 等
    e.preventDefault();
    if (!leaving) depart(a, url);
  });

  // 用瀏覽器返回鍵／手勢離開時沒有 click 可攔，只留下標記，讓上一頁抵達時「右 → 左」飛回來
  window.addEventListener("pagehide", () => { if (!leaving) setFlag({ t: Date.now() }); });

  function arrive(a){
    if (!a) return;
    const el = overlay({ kicker: t(a.back ? "tx.returned" : "tx.arrived", a.back ? "返回" : "抵達"), name: a.name }, a.back);
    el.classList.add("tx-covered");
    html.classList.remove("tx-arriving");
    requestAnimationFrame(() => requestAnimationFrame(() => el.classList.add("tx-in")));
    // 布幕滑完就整個移除（含凝結尾），不留殘線；頁面忙碌時計時器可能延遲，所以兩者都設
    const done = () => el.remove();
    el.querySelector(".tx-curtain").addEventListener("transitionend", e => { if (e.propertyName === "transform") setTimeout(done, 60); }, { once: true });
    setTimeout(done, IN_MS + 400);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", () => arrive(arriving)); else arrive(arriving);

  // 從 bfcache 還原（多半是按了返回鍵）：清掉殘留的離開布幕，播放「右 → 左」的抵達動畫
  window.addEventListener("pageshow", e => {
    if (!e.persisted) return;
    leaving = false;
    document.querySelectorAll(".tx").forEach(x => x.remove());
    html.classList.remove("tx-arriving");
    readFlag();
    if (!OFF) arrive({ name: nameFor(location), back: true });   // bfcache 還原只會發生在上一頁／下一頁，一律右 → 左
  });
})();
