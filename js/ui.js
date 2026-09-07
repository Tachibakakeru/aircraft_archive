"use strict";
/* ═══════════════════════════════════════════════
   共用 UI 行為：下滑時顯示「回到頂端」按鈕
   在有垂直捲動的頁面（列表 / 比較 / 編輯器）載入即可
   ═══════════════════════════════════════════════ */
(() => {
  let topFrame = 0;
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
    btn.addEventListener("click", () => {
      cancelAnimationFrame(topFrame);
      const start = window.scrollY || document.documentElement.scrollTop;
      const duration = Math.min(900, Math.max(420, start / 2));
      const began = performance.now();
      (function step(now){
        const p = Math.min((now - began) / duration, 1);
        window.scrollTo(0, start * Math.pow(1 - p, 3));
        if (p < 1) topFrame = requestAnimationFrame(step);
      })(began);
    });
    window.addEventListener("scroll", onScroll, { passive: true });
    document.addEventListener("langchange", label);
  }

  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", init);
  else init();
})();

// 機型比較頁共用的可搜尋選單。使用站內 DOM 選單，避免瀏覽器原生
// datalist 的清除叉號與無法隱藏的系統捲軸。
window.AircraftPicker = {
  mount(input, aircraft, currentId, onChoose){
    const root = document.createElement("div");
    root.className = "aircraft-picker apt-cmp-picker";
    input.parentNode.insertBefore(root, input);
    root.appendChild(input);
    input.type = "text";
    input.classList.add("aircraft-picker-input");
    input.setAttribute("role", "combobox");
    input.setAttribute("aria-autocomplete", "list");
    input.setAttribute("aria-expanded", "false");

    const menu = document.createElement("div");
    menu.className = "aircraft-picker-menu apt-cmp-suggest";
    menu.hidden = true;
    root.appendChild(menu);
    let activeId = currentId;

    const meta = a => [a.manufacturer, a.icao].filter(Boolean).join(" · ");
    const find = id => aircraft.find(a => a.id === id);
    function render(showAll = false){
      const q = showAll ? "" : input.value.trim().toLocaleLowerCase();
      const matches = aircraft.filter(a => !q || [a.name, a.manufacturer, a.icao]
        .some(v => String(v || "").toLocaleLowerCase().includes(q)));
      menu.innerHTML = "";
      matches.forEach(a => {
        const option = document.createElement("button");
        option.type = "button";
        option.className = "aircraft-picker-option apt-cmp-opt";
        option.dataset.id = a.id;
        const name = document.createElement("span");
        const details = document.createElement("small");
        name.textContent = a.name;
        details.textContent = meta(a);
        option.append(name, details);
        menu.appendChild(option);
      });
      menu.hidden = !matches.length;
      input.setAttribute("aria-expanded", String(matches.length > 0));
    }
    async function choose(id){
      const a = find(id);
      if (!a) return;
      activeId = id;
      input.value = a.name;
      menu.hidden = true;
      input.setAttribute("aria-expanded", "false");
      await onChoose(id);
    }
    input.addEventListener("focus", () => { input.select(); render(true); });
    input.addEventListener("input", () => render());
    input.addEventListener("blur", () => setTimeout(() => {
      menu.hidden = true;
      input.setAttribute("aria-expanded", "false");
      const a = find(activeId);
      if (a) input.value = a.name;
    }, 120));
    menu.addEventListener("mousedown", e => {
      const option = e.target.closest("[data-id]");
      if (!option) return;
      e.preventDefault();
      choose(option.dataset.id);
    });

    const api = { set(id){ activeId = id; const a = find(id); if (a) input.value = a.name; } };
    api.set(currentId);
    return api;
  }
};

// 共用下拉選單鍵盤操作：自動完成輸入框共用既有 mousedown 選取流程，
// 因此不用為機場、航空公司、距離計算與小知識各寫一份鍵盤狀態。
(function(){
  function listFor(input){
    if (input.id === "apt-country-input") return document.getElementById("apt-country-suggest");
    const scope = input.closest(".apt-cmp-picker,.al-tag-wrap,.kn-search");
    return scope && scope.querySelector(".apt-cmp-suggest,.al-tag-suggest,.kn-search-suggest");
  }
  function options(list){ return [...list.querySelectorAll(".apt-cmp-opt,.al-tag-opt,.kn-search-opt")]; }
  function setActive(list, index){
    const opts = options(list);
    if (!opts.length) return;
    const i = (index + opts.length) % opts.length;
    opts.forEach((opt, n) => opt.classList.toggle("kb-active", n === i));
    opts[i].scrollIntoView({ block:"nearest" });
  }
  document.addEventListener("input", e => {
    const list = e.target instanceof HTMLInputElement && listFor(e.target);
    if (list) list.querySelectorAll(".kb-active").forEach(opt => opt.classList.remove("kb-active"));
  });
  document.addEventListener("keydown", e => {
    const input = e.target instanceof HTMLInputElement && e.target;
    const list = input && listFor(input);
    if (!list || list.hidden) return;
    const opts = options(list);
    if (e.key === "Escape") { e.preventDefault(); e.stopPropagation(); list.hidden = true; input.setAttribute("aria-expanded", "false"); return; }
    if (!opts.length || !["ArrowDown", "ArrowUp", "Enter"].includes(e.key)) return;
    const active = opts.findIndex(opt => opt.classList.contains("kb-active"));
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      e.preventDefault(); e.stopPropagation(); setActive(list, active < 0 ? (e.key === "ArrowDown" ? 0 : -1) : active + (e.key === "ArrowDown" ? 1 : -1));
      return;
    }
    e.preventDefault(); e.stopPropagation();
    (opts[active < 0 ? 0 : active]).dispatchEvent(new MouseEvent("mousedown", { bubbles:true, cancelable:true }));
  }, true);
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
