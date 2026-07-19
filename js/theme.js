"use strict";
/* ═══════════════════════════════════════════════
   主題切換（深色 / 淺色），偏好存 localStorage
   在 <html> 上加 data-theme="light"，CSS 依此覆蓋變數
   ═══════════════════════════════════════════════ */
(function(){
  const KEY = "hangar_theme";
  const saved = localStorage.getItem(KEY);
  // 首次依系統偏好，之後尊重使用者選擇
  const initial = saved || (window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark");
  document.documentElement.setAttribute("data-theme", initial);

  window.HangarTheme = {
    get(){ return document.documentElement.getAttribute("data-theme"); },
    set(t){
      document.documentElement.setAttribute("data-theme", t);
      localStorage.setItem(KEY, t);
    },
    toggle(){
      this.set(this.get() === "light" ? "dark" : "light");
      return this.get();
    }
  };

  // PWA 離線快取（頁面自身路徑作為 scope，避免子路徑部署時跑掉）
  if ("serviceWorker" in navigator)
    navigator.serviceWorker.register("sw.js").catch(() => {});

  // 連回機隊列表的連結（不論是 viewer.html 等頁面的「← FLEET」麵包屑，
  // 還是 distance.html／airlines.html 工具列上的「✈️ 飛行器圖鑑」）原本
  // 都寫死 href="fleet.html"，點回去會遺失離開機隊列表時的搜尋／篩選
  // 狀態（跟瀏覽器「上一頁」不同，這是頁面自己的連結，網址本來就沒有
  // 帶查詢字串可還原）。fleet.html 每次篩選狀態變動時會把查詢字串存進
  // sessionStorage，這裡讀回來接到「所有」連到 fleet.html 的連結後面，
  // 不限定樣式或 class，讓從任何頁面回機隊列表都能停留在原本的搜尋結果。
  function restoreFleetBackLink(){
    const q = sessionStorage.getItem("hangar_fleet_query");
    if (!q) return;
    document.querySelectorAll('a[href="fleet.html"]').forEach(a => {
      a.href = "fleet.html?" + q;
    });
  }
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", restoreFleetBackLink);
  else restoreFleetBackLink();
})();
