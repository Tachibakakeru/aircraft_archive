"use strict";
/* ═══════════════════════════════════════════════
   小彩蛋與座艙音效（2026-11）
   1. 航空紀念日：首頁 #anniv 在對應日期（依 js/skytime.js 選的時區）顯示一行橫幅，例如
      「今天是 Boeing 747 首飛 57 週年」，可連到 3D 模型；按 × 當天不再顯示。網址加 ?date=MM-DD 可預覽。
   2. Logo 飛越：在首頁點左上角 SKY ARCHIVE 標誌，一架小飛機拖著凝結尾從畫面飛過（不換頁）。
   3. 座艙音效：用 Web Audio 合成「叮－咚」提示音（不下載音檔），預設關閉；
      開關按鈕放在首頁右上與子頁導覽列，設定存在 localStorage.hangar_sound。
      換頁（js/transition.js）時若開啟會播放。
   以 defer 載入，放在 js/sitebar.js 之後（子頁的開關要放進導覽列）。
   ═══════════════════════════════════════════════ */
(function(){
  const t = (k, fb) => (typeof I18N !== "undefined" ? I18N.t(k) : fb);
  const lang = () => (typeof I18N !== "undefined" ? I18N.get() : "zh");

  /* ── 座艙音效 ── */
  let ctx = null;
  const soundOn = () => { try { return localStorage.getItem("hangar_sound") === "on"; } catch (e) { return false; } };
  // 「叮－咚」：兩個音都有短起音與自然衰減，最後再由總音量淡出到 0，不會突然斷掉。
  // within（毫秒）：必須在多久內結束（例如換頁前的離開動畫時間），會把兩個音靠近一點並提早淡出。
  function chime({ within = 0 } = {}){
    if (!soundOn()) return;
    try {
      ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
      if (ctx.state === "suspended") ctx.resume();
      const now = ctx.currentTime + .02;
      const total = within ? Math.max(.6, within / 1000 - .05) : 1.9;   // 整段聲音長度（秒）
      const gap = within ? Math.min(.32, total * .3) : .38;              // 第二聲「咚」的起點
      const master = ctx.createGain();
      master.gain.setValueAtTime(1, now);
      master.gain.setValueAtTime(1, now + total * .55);
      master.gain.linearRampToValueAtTime(0, now + total);               // 最後 45% 時間淡出到靜音
      master.connect(ctx.destination);
      [[880, 0], [698.5, gap]].forEach(([f, at]) => {                    // A5 → F5，類似客艙廣播前的雙音
        const o = ctx.createOscillator(), o2 = ctx.createOscillator(), g = ctx.createGain(), g2 = ctx.createGain();
        o.type = "sine"; o.frequency.value = f;
        o2.type = "sine"; o2.frequency.value = f * 2.01;                 // 一點泛音，聽起來像金屬鐘
        g2.gain.value = .16;
        o2.connect(g2).connect(g);
        o.connect(g).connect(master);
        const st = now + at, end = now + total;
        g.gain.setValueAtTime(0, st);
        g.gain.linearRampToValueAtTime(.2, st + .02);
        g.gain.exponentialRampToValueAtTime(.02, Math.max(st + .1, end - .05));
        g.gain.linearRampToValueAtTime(0, end);
        o.start(st); o2.start(st); o.stop(end + .05); o2.stop(end + .05);
      });
    } catch (e) {}
  }
  window.HangarSound = { chime, on: soundOn };
  const BELL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15zM10 20.5a2.2 2.2 0 0 0 4 0"/></svg>';
  const BELL_OFF = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15zM10 20.5a2.2 2.2 0 0 0 4 0M3 3l18 18"/></svg>';
  function soundButton(cls){
    const b = document.createElement("button");
    b.type = "button"; b.className = cls + " snd-btn";
    const sync = () => {
      const on = soundOn();
      b.innerHTML = on ? BELL : BELL_OFF;
      b.setAttribute("aria-pressed", String(on));
      const label = t(on ? "extras.sound.on" : "extras.sound.off", on ? "座艙音效：開（點一下關閉）" : "座艙音效：關（點一下開啟）");
      b.title = label; b.setAttribute("aria-label", label);
    };
    b.addEventListener("click", () => {
      try { localStorage.setItem("hangar_sound", soundOn() ? "off" : "on"); } catch (e) {}
      sync(); chime();
    });
    document.addEventListener("langchange", sync);
    sync();
    return b;
  }
  const homeSwitches = document.querySelector(".top .switches");
  if (homeSwitches) homeSwitches.insertBefore(soundButton("icon-btn"), homeSwitches.querySelector("#theme"));
  const siteTools = document.querySelector(".site-bar .site-tools");
  if (siteTools) siteTools.appendChild(soundButton("site-tool"));

  /* ── 航空紀念日 ── */
  const ANNIV = [
    { d: "12-17", y: 1903, link: "knowledge.html", t: { zh: "萊特兄弟「飛行者一號」完成首次有動力、可操控的飛行", en: "the Wright Flyer’s first powered, controlled flight", ja: "ライト兄弟「フライヤー号」初の動力・操縦飛行" } },
    { d: "07-27", y: 1949, link: "", t: { zh: "世界第一款噴射客機 de Havilland Comet 首飛", en: "the first flight of the de Havilland Comet, the first jet airliner", ja: "世界初のジェット旅客機デ・ハビランド コメット初飛行" } },
    { d: "04-09", y: 1967, link: "viewer.html?model=b737", t: { zh: "Boeing 737 首飛", en: "the Boeing 737’s first flight", ja: "ボーイング 737 初飛行" } },
    { d: "02-09", y: 1969, link: "viewer.html?model=b744", t: { zh: "Boeing 747 首飛", en: "the Boeing 747’s first flight", ja: "ボーイング 747 初飛行" } },
    { d: "03-02", y: 1969, link: "viewer.html?model=concorde", t: { zh: "協和號首飛", en: "Concorde’s first flight", ja: "コンコルド初飛行" } },
    { d: "02-22", y: 1987, link: "viewer.html?model=a320", t: { zh: "Airbus A320 首飛", en: "the Airbus A320’s first flight", ja: "エアバス A320 初飛行" } },
    { d: "06-12", y: 1994, link: "viewer.html?model=b772", t: { zh: "Boeing 777 首飛", en: "the Boeing 777’s first flight", ja: "ボーイング 777 初飛行" } },
    { d: "12-07", y: 1944, link: "knowledge.html", t: { zh: "國際民航日（1944 年《芝加哥公約》簽署）", en: "International Civil Aviation Day (Chicago Convention signed in 1944)", ja: "国際民間航空デー（1944 年シカゴ条約署名）" } },
    { d: "04-27", y: 2005, link: "viewer.html?model=a380", t: { zh: "Airbus A380 首飛", en: "the Airbus A380’s first flight", ja: "エアバス A380 初飛行" } },
    { d: "10-25", y: 2007, link: "viewer.html?model=a380", t: { zh: "A380 首次載客商業飛行（新加坡航空 新加坡–雪梨）", en: "the A380’s first commercial flight (Singapore Airlines, Singapore–Sydney)", ja: "A380 初の商業運航（シンガポール航空 シンガポール–シドニー）" } },
    { d: "12-15", y: 2009, link: "viewer.html?model=b788", t: { zh: "Boeing 787 首飛", en: "the Boeing 787’s first flight", ja: "ボーイング 787 初飛行" } },
    { d: "06-14", y: 2013, link: "viewer.html?model=a359", t: { zh: "Airbus A350 XWB 首飛", en: "the Airbus A350 XWB’s first flight", ja: "エアバス A350 XWB 初飛行" } }
  ];
  function todayInZone(){
    const tz = typeof SkyTime !== "undefined" ? SkyTime.tz() : undefined;
    const o = {};
    new Intl.DateTimeFormat("en-US", { timeZone: tz, year: "numeric", month: "2-digit", day: "2-digit" }).formatToParts(new Date()).forEach(p => { o[p.type] = p.value; });
    return { md: `${o.month}-${o.day}`, y: +o.year, ymd: `${o.year}-${o.month}-${o.day}` };
  }
  function renderAnniv(){
    const box = document.getElementById("anniv");
    if (!box) return;
    const today = todayInZone();
    const forced = new URLSearchParams(location.search).get("date");
    const md = forced && /^\d\d-\d\d$/.test(forced) ? forced : today.md;
    const hit = ANNIV.find(x => x.d === md);
    let dismissed = null;
    try { dismissed = localStorage.getItem("hangar_anniv_dismiss"); } catch (e) {}
    if (!hit || (!forced && dismissed === today.ymd)){ box.hidden = true; return; }
    const years = today.y - hit.y;
    const text = (hit.t[lang()] || hit.t.zh);
    const line = t("extras.anniv", "今天是{event} {n} 週年（{y} 年）").replace("{event}", text).replace("{n}", years).replace("{y}", hit.y);
    box.innerHTML = `<span class="anniv-ic" aria-hidden="true">✦</span><span class="anniv-text"></span>${hit.link ? `<a class="anniv-go" href="${hit.link}"></a>` : ""}<button type="button" class="anniv-x" aria-label="">×</button>`;
    box.querySelector(".anniv-text").textContent = line;
    if (hit.link) box.querySelector(".anniv-go").textContent = t(hit.link.startsWith("viewer") ? "extras.anniv.model" : "extras.anniv.more", "看 3D 模型 →");
    const x = box.querySelector(".anniv-x");
    x.setAttribute("aria-label", t("extras.anniv.close", "今天不再顯示"));
    x.title = x.getAttribute("aria-label");
    x.addEventListener("click", () => { try { localStorage.setItem("hangar_anniv_dismiss", today.ymd); } catch (e) {} box.hidden = true; });
    box.hidden = false;
  }
  renderAnniv();
  document.addEventListener("langchange", renderAnniv);
  document.addEventListener("tzchange", renderAnniv);

  /* ── 收藏蓋章（2026-11）：按下收藏星號（原本未收藏）時，在按鈕上蓋一個「已收藏」登機章 ──
     各頁的收藏按鈕都帶 data-ico="star"（機隊卡片、機場／航空公司列表與詳情、機尾牆）；
     「只看收藏」篩選是 <label> 裡的文字，不是按鈕，不會觸發。點擊前判斷狀態，因為列表會在點擊後重畫。 */
  document.addEventListener("click", e => {
    const b = e.target.closest('button[data-ico="star"], a[data-ico="star"]');
    if (!b) return;
    const wasOn = b.classList.contains("on") || b.getAttribute("aria-pressed") === "true";
    if (wasOn) return;
    const r = b.getBoundingClientRect();
    const st = document.createElement("div");
    st.className = "fav-stamp";
    st.setAttribute("aria-hidden", "true");
    st.innerHTML = `<span>${t("bp.saved", "已收藏")}</span><small>SKY ARCHIVE</small>`;
    st.style.left = (r.left + r.width / 2) + "px";
    st.style.top = (r.top + r.height / 2) + "px";
    document.body.appendChild(st);
    requestAnimationFrame(() => requestAnimationFrame(() => st.classList.add("in")));
    setTimeout(() => st.classList.add("out"), 750);
    setTimeout(() => st.remove(), 1250);
  }, true);

  /* ── Logo 飛越（只在首頁） ── */
  const brand = document.querySelector(".top .brand");
  if (brand){
    const PLANE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/></svg>';
    let busy = false;
    brand.addEventListener("click", e => {
      e.preventDefault();
      if (busy) return;
      busy = true;
      chime();
      const el = document.createElement("div");
      el.className = "flyby";
      el.setAttribute("aria-hidden", "true");
      // 飛行路線：整條路線（.flyby-path）稍微傾斜，飛機在路線上平移，凝結尾是飛機的子元素，永遠接在機尾
      const top = 18 + Math.random() * 30;
      el.innerHTML = `<div class="flyby-path" style="top:${top}vh"><div class="flyby-plane"><div class="flyby-trail"></div>${PLANE}</div></div>`;
      document.body.appendChild(el);
      requestAnimationFrame(() => requestAnimationFrame(() => el.classList.add("flyby-on")));
      const plane = el.querySelector(".flyby-plane");
      const finish = () => { if (!el.isConnected) return; el.remove(); busy = false; };
      plane.addEventListener("transitionend", e => { if (e.propertyName === "transform") finish(); });
      setTimeout(finish, 3200);   // 保底
    });
  }
})();
