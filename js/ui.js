"use strict";
/* ═══════════════════════════════════════════════
   共用 UI 行為：下滑時顯示「回到頂端」按鈕
   在有垂直捲動的頁面（列表 / 比較 / 編輯器）載入即可
   ═══════════════════════════════════════════════ */
(() => {
  const btn = document.createElement("button");
  btn.id = "to-top";
  btn.type = "button";
  btn.setAttribute("aria-hidden", "true");
  btn.innerHTML = "↑";

  const label = () => {
    const txt = (typeof I18N !== "undefined") ? I18N.t("ui.totop") : "回到頂端";
    btn.title = txt;
    btn.setAttribute("aria-label", txt);
  };

  function onScroll(){
    const show = (window.scrollY || document.documentElement.scrollTop) > 320;
    btn.classList.toggle("show", show);
    btn.setAttribute("aria-hidden", String(!show));
  }

  function init(){
    document.body.appendChild(btn);
    label();
    onScroll();
    btn.addEventListener("click", () =>
      window.scrollTo({ top: 0, behavior: "smooth" }));
    window.addEventListener("scroll", onScroll, { passive: true });
    document.addEventListener("langchange", label);
  }

  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", init);
  else init();
})();

// 滑鼠滾輪 → 水平捲動（適用所有 overflow-x 橫列）
document.addEventListener("wheel", e => {
  const el = e.target.closest(".fleet-recent-row, .cmp-table-wrap, .ed-parts");
  if (!el) return;
  e.preventDefault();
  // deltaMode: 0=px, 1=line(≈40px), 2=page
  const delta = e.deltaMode === 1 ? e.deltaY * 40 : e.deltaMode === 2 ? e.deltaY * el.clientWidth : e.deltaY;
  el.scrollLeft += delta;
}, { passive: false });
