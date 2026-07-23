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

// 滑鼠拖曳水平捲動（fleet-recent-row 拖曳手勢，觸控原生支援不需處理）
(function(){
  let row = null, startX = 0, startScroll = 0, moved = false;
  document.addEventListener("pointerdown", e => {
    const r = e.target.closest(".fleet-recent-row");
    if (!r || e.pointerType !== "mouse") return;
    row = r; moved = false; startX = e.clientX; startScroll = r.scrollLeft;
  });
  document.addEventListener("pointermove", e => {
    if (!row) return;
    const dx = e.clientX - startX;
    if (!moved && Math.abs(dx) > 4) { moved = true; row.style.cursor = "grabbing"; }
    if (moved) row.scrollLeft = startScroll - dx;
  });
  function end(){ if (row) { row.style.cursor = ""; row = null; } }
  document.addEventListener("pointerup", end);
  document.addEventListener("pointercancel", end);
  document.addEventListener("click", e => {
    if (moved && e.target.closest(".fleet-recent-row")) { e.stopPropagation(); e.preventDefault(); moved = false; }
  }, true);
  // 防止拖曳圖片/連結觸發原生 drag 搶走 pointer capture
  document.addEventListener("dragstart", e => {
    if (e.target.closest(".fleet-recent-row")) e.preventDefault();
  });
})();
