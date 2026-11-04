"use strict";
/* ═══════════════════════════════════════════════
   全站頂部導覽列（2026-11 改版，樣式見 css/style.css 的「全站導覽列」）
   - 在子頁最上方插入「SKY ARCHIVE」品牌＋四個資料庫連結，並標出目前所在的資料庫。
   - 把頁面原有的語言（#btn-lang）、單位（#btn-unit）、主題（#btn-theme）按鈕「搬進」導覽列：
     搬移 DOM 節點會保留原本綁定的事件，所以各頁程式不用改。
   - 3D 檢視器（body.viewer）是全螢幕場景，不插入導覽列。
   依賴 js/i18n.js（home.nav.* 與 home.brand 字串）。
   ═══════════════════════════════════════════════ */
(function(){
  const LINKS = [
    { href:"fleet.html",     key:"home.nav.fleet",     pages:["fleet.html","viewer.html","compare.html","versus.html","variants.html","editor.html"] },
    { href:"airports.html",  key:"home.nav.airports",  pages:["airports.html","distance.html"] },
    { href:"airlines.html",  key:"home.nav.airlines",  pages:["airlines.html"] },
    { href:"knowledge.html", key:"home.nav.knowledge", pages:["knowledge.html"] }
  ];
  const LOGO = '<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="18.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M6 25 Q20 6 34 18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="2 3"/><path fill="currentColor" transform="translate(13 9) scale(.6) rotate(55 12 12)" d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/></svg>';
  const t = k => (typeof I18N !== "undefined" ? I18N.t(k) : k);

  function label(bar){
    bar.querySelector(".site-brand small").textContent = t("home.brand");
    bar.querySelectorAll(".site-nav a").forEach((a, i) => { a.textContent = t(LINKS[i].key); });
  }

  function build(){
    if (document.body.classList.contains("viewer") || document.querySelector(".site-bar")) return;
    const page = (location.pathname.split("/").pop() || "index.html").toLowerCase();
    const bar = document.createElement("header");
    bar.className = "site-bar";
    bar.innerHTML = `<div class="site-bar-in">
      <a class="site-brand" href="index.html">${LOGO}<span><b>SKY ARCHIVE</b><small></small></span></a>
      <nav class="site-nav" aria-label="SKY ARCHIVE">${LINKS.map(l =>
        `<a href="${l.href}"${l.pages.includes(page) ? ' aria-current="page"' : ""}></a>`).join("")}</nav>
      <div class="site-tools"><button type="button" class="site-clock" data-skyclock="compact" data-tzpicker></button></div>
    </div>`;
    document.body.prepend(bar);
    document.body.classList.add("has-site-bar");
    label(bar);
    const clk = bar.querySelector(".site-clock");
    clk.title = t("sky.tz.change");
    if (typeof SkyTime !== "undefined") SkyTime.renderClocks();

    const tools = bar.querySelector(".site-tools");
    ["btn-lang", "btn-unit", "btn-theme"].forEach(id => {
      const el = document.getElementById(id);
      if (!el) return;
      const from = el.parentElement;
      el.classList.add("site-tool");
      tools.appendChild(el);
      // 原工具列若只剩空白（例如距離計算頁），整列移除，避免留下空卡片
      if (from && from !== tools && !from.children.length && !from.textContent.trim()) from.remove();
    });
    document.addEventListener("langchange", () => { label(bar); clk.title = t("sky.tz.change"); });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", build);
  else build();
})();
