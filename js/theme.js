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
})();
