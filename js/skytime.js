"use strict";
/* ═══════════════════════════════════════════════
   天空時間（2026-11）：依所選時區的當地時間切換天空、顯示時鐘與 UTC 偏移，時區可自訂。
   - 時區：localStorage.hangar_tz（IANA 名稱，例如 "Asia/Taipei"）；沒設定時用裝置時區（「自動」）。
   - 天空時段：在 <html> 設 data-sky = dawn（05–07 時）／day（07–17）／dusk（17–19:30）／night，
     CSS（css/style.css、css/home.css）依此換天空漸層，夜間顯示星星。每分鐘檢查一次。
   - 時鐘：頁面上有 [data-skyclock] 的元素會每秒更新「時:分:秒、星期、UTC±X」。
     [data-skyclock="compact"] 只顯示「時:分:秒 UTC±X」（導覽列用）。
   - 時區選單：點 [data-tzpicker] 開啟站內自訂選單（可搜尋，依專案規則不用原生下拉選單）。
   - 事件：時區改變時在 document 派發 "tzchange"（detail = 時區名稱），讓頁面其他時鐘一起更新。
   字串使用 js/i18n.js 的 sky.*；未載入 I18N 時退回繁中。
   ═══════════════════════════════════════════════ */
const SkyTime = (() => {
  const KEY = "hangar_tz";
  const deviceTz = (() => { try { return Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC"; } catch (e) { return "UTC"; } })();
  const store = {
    get(){ try { return localStorage.getItem(KEY); } catch (e) { return null; } },
    set(v){ try { v ? localStorage.setItem(KEY, v) : localStorage.removeItem(KEY); } catch (e) {} }
  };
  const valid = tz => { try { new Intl.DateTimeFormat("en", { timeZone: tz }); return true; } catch (e) { return false; } };
  let chosen = (() => { const v = store.get(); return v && valid(v) ? v : null; })();
  const tz = () => chosen || deviceTz;

  const FALLBACK = {
    "sky.tz.auto": "自動（裝置時區）", "sky.tz.title": "選擇時區", "sky.tz.search": "搜尋城市或時區，例如 Tokyo、UTC+9",
    "sky.tz.none": "找不到符合的時區", "sky.tz.change": "更改時區", "sky.tz.autoShort": "自動"
  };
  const t = k => (typeof I18N !== "undefined" ? I18N.t(k) : (FALLBACK[k] || k));
  const lang = () => (typeof I18N !== "undefined" ? I18N.get() : "zh");
  const locale = () => ({ zh: "zh-TW", en: "en-US", ja: "ja-JP" })[lang()] || "zh-TW";

  // 常用時區的中日文城市名（其餘顯示 IANA 名稱中的城市英文）
  const CITY = {
    "Asia/Taipei": ["臺北", "台北"], "Asia/Tokyo": ["東京", "東京"], "Asia/Seoul": ["首爾", "ソウル"], "Asia/Shanghai": ["上海", "上海"],
    "Asia/Hong_Kong": ["香港", "香港"], "Asia/Singapore": ["新加坡", "シンガポール"], "Asia/Bangkok": ["曼谷", "バンコク"],
    "Asia/Dubai": ["杜拜", "ドバイ"], "Asia/Kolkata": ["加爾各答", "コルカタ"], "Asia/Calcutta": ["加爾各答", "コルカタ"], "Europe/London": ["倫敦", "ロンドン"],
    "Europe/Paris": ["巴黎", "パリ"], "Europe/Berlin": ["柏林", "ベルリン"], "Europe/Amsterdam": ["阿姆斯特丹", "アムステルダム"],
    "Europe/Istanbul": ["伊斯坦堡", "イスタンブール"], "Europe/Moscow": ["莫斯科", "モスクワ"], "America/New_York": ["紐約", "ニューヨーク"],
    "America/Chicago": ["芝加哥", "シカゴ"], "America/Denver": ["丹佛", "デンバー"], "America/Los_Angeles": ["洛杉磯", "ロサンゼルス"],
    "America/Anchorage": ["安克拉治", "アンカレッジ"], "Pacific/Honolulu": ["檀香山", "ホノルル"], "America/Sao_Paulo": ["聖保羅", "サンパウロ"],
    "America/Toronto": ["多倫多", "トロント"], "America/Vancouver": ["溫哥華", "バンクーバー"], "Australia/Sydney": ["雪梨", "シドニー"],
    "Australia/Perth": ["伯斯", "パース"], "Pacific/Auckland": ["奧克蘭", "オークランド"], "Africa/Cairo": ["開羅", "カイロ"],
    "Africa/Johannesburg": ["約翰尼斯堡", "ヨハネスブルグ"], "Asia/Manila": ["馬尼拉", "マニラ"], "Asia/Jakarta": ["雅加達", "ジャカルタ"],
    "Asia/Kuala_Lumpur": ["吉隆坡", "クアラルンプール"], "Asia/Ho_Chi_Minh": ["胡志明市", "ホーチミン"], "UTC": ["協調世界時", "協定世界時"]
  };
  const cityName = z => {
    const c = CITY[z];
    if (c && lang() === "zh") return c[0];
    if (c && lang() === "ja") return c[1];
    if (z === "UTC") return "UTC";
    return z.split("/").pop().replace(/_/g, " ");
  };

  // 取某時區「現在」的時、分、秒、星期與 UTC 偏移（分鐘）
  function parts(zone = tz(), d = new Date()){
    const f = new Intl.DateTimeFormat("en-US", { timeZone: zone, hourCycle: "h23", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit" });
    const o = {};
    f.formatToParts(d).forEach(p => { o[p.type] = p.value; });
    const h = +o.hour % 24, m = +o.minute, s = +o.second;
    const asUTC = Date.UTC(+o.year, +o.month - 1, +o.day, h, m, s);
    const offset = Math.round((asUTC - Math.floor(d.getTime() / 1000) * 1000) / 60000);
    const weekday = new Intl.DateTimeFormat(locale(), { timeZone: zone, weekday: "long" }).format(d);
    return { h, m, s, offset, weekday };
  }
  const fmtOffset = min => {
    const sign = min < 0 ? "−" : "+", a = Math.abs(min), hh = Math.floor(a / 60), mm = a % 60;
    return `UTC${sign}${hh}${mm ? ":" + String(mm).padStart(2, "0") : ""}`;
  };
  const pad = n => String(n).padStart(2, "0");

  // 天空時段
  function phaseOf(h, m){
    const x = h + m / 60;
    if (x >= 5 && x < 7) return "dawn";
    if (x >= 7 && x < 17) return "day";
    if (x >= 17 && x < 19.5) return "dusk";
    return "night";
  }
  function applySky(){
    const p = parts();
    const ph = phaseOf(p.h, p.m);
    if (document.documentElement.dataset.sky !== ph){
      document.documentElement.dataset.sky = ph;
      document.dispatchEvent(new CustomEvent("skychange", { detail: ph }));
    }
  }

  // 時鐘
  function renderClocks(){
    const els = document.querySelectorAll("[data-skyclock]");
    if (!els.length) return;
    const p = parts(), time = `${pad(p.h)}:${pad(p.m)}:${pad(p.s)}`, off = fmtOffset(p.offset);
    els.forEach(el => {
      if (el.dataset.skyclock === "compact"){
        el.innerHTML = `<b>${time}</b><span class="sky-off">${off}</span>`;
      } else {
        renderFlip(el, time, p, off);
      }
    });
  }

  /* 翻頁式時鐘（2026-11）：每個數字是一張翻牌。結構只建一次，之後只翻有變動的數字：
     上半片顯示舊數字往下翻（0 → -90°），下半片帶著新數字接著翻下來（90° → 0）。
     使用者要求動畫在 reduced-motion 下也照常播放，所以不用媒體查詢略過。 */
  const flipCard = d => `<span class="flip" data-v="${d}"><span class="ft"><i>${d}</i></span><span class="fb"><i>${d}</i></span><span class="fft"><i>${d}</i></span><span class="ffb"><i>${d}</i></span></span>`;
  function setFlip(card, d){
    const old = card.dataset.v;
    if (old === d) return;
    card.dataset.v = d;
    const [ft, fb, fft, ffb] = card.children;
    ft.firstChild.textContent = d; fb.firstChild.textContent = old;
    fft.firstChild.textContent = old; ffb.firstChild.textContent = d;
    card.classList.remove("flipping"); void card.offsetWidth; card.classList.add("flipping");
  }
  function settleFlip(e){
    const card = e.target.closest(".flip");
    if (!card || !e.target.classList.contains("ffb")) return;
    const d = card.dataset.v;
    card.children[1].firstChild.textContent = d; card.children[2].firstChild.textContent = d;
    card.classList.remove("flipping");
  }
  function renderFlip(el, time, p, off){
    const digits = time.replace(/:/g, "");
    let wrap = el.querySelector(".flip-clock");
    if (!wrap){
      el.innerHTML = `<span class="flip-clock" aria-hidden="true">${[0, 2, 4].map(i => flipCard(digits[i]) + flipCard(digits[i + 1])).join('<span class="flip-sep">:</span>')}</span><span class="sky-meta"><span class="sky-day"></span><span class="sky-off"></span></span>`;
      el.addEventListener("animationend", settleFlip);
      wrap = el.querySelector(".flip-clock");
    } else {
      wrap.querySelectorAll(".flip").forEach((c, i) => setFlip(c, digits[i]));
    }
    el.querySelector(".sky-day").textContent = p.weekday;
    el.querySelector(".sky-off").textContent = `${off} · ${cityName(tz())}${chosen ? "" : " · " + t("sky.tz.autoShort")}`;
    el.setAttribute("aria-label", `${time} ${p.weekday} ${off}`);
  }

  // 時區選單（站內自訂，可搜尋，↑↓ Enter Esc）
  let menu = null, anchor = null, items = [], act = -1;
  function allZones(){
    let z = [];
    try { z = Intl.supportedValuesOf("timeZone"); } catch (e) { z = Object.keys(CITY); }
    if (!z.includes("UTC")) z = ["UTC", ...z];
    const now = new Date();
    return z.map(name => ({ name, offset: parts(name, now).offset })).sort((a, b) => a.offset - b.offset || a.name.localeCompare(b.name));
  }
  let zoneCache = null;
  function buildMenu(){
    menu = document.createElement("div");
    menu.className = "tz-menu";
    menu.setAttribute("role", "dialog");
    menu.innerHTML = `<div class="tz-head"><b class="tz-title"></b></div><input class="tz-search" type="text" autocomplete="off" role="combobox" aria-expanded="true" aria-controls="tzList"><div class="tz-list" id="tzList" role="listbox"></div>`;
    document.body.appendChild(menu);
    const input = menu.querySelector(".tz-search");
    input.addEventListener("input", () => renderList(input.value));
    input.addEventListener("keydown", e => {
      if (e.key === "ArrowDown"){ e.preventDefault(); act = Math.min(items.length - 1, act + 1); mark(); }
      else if (e.key === "ArrowUp"){ e.preventDefault(); act = Math.max(0, act - 1); mark(); }
      else if (e.key === "Enter"){ e.preventDefault(); if (items[act] !== undefined) choose(items[act]); }
      else if (e.key === "Escape"){ e.preventDefault(); e.stopPropagation(); close(); }
    });
    menu.querySelector(".tz-list").addEventListener("mousedown", e => {
      const o = e.target.closest("[data-tz]"); if (!o) return;
      e.preventDefault(); choose(o.dataset.tz);
    });
    document.addEventListener("mousedown", e => { if (menu && !menu.hidden && !menu.contains(e.target) && !e.target.closest("[data-tzpicker]")) close(); });
    window.addEventListener("resize", () => { if (menu && !menu.hidden) place(); });
  }
  function renderList(q){
    zoneCache = zoneCache || allZones();
    const nq = (q || "").trim().toLowerCase().replace(/\s+/g, "");
    const list = zoneCache.filter(z => !nq || z.name.toLowerCase().replace(/_/g, "").includes(nq) || cityName(z.name).toLowerCase().includes(nq)
      || fmtOffset(z.offset).toLowerCase().replace("−", "-").replace(/\s/g, "").includes(nq.replace("−", "-")));
    items = [""].concat(list.map(z => z.name));   // "" = 自動
    if (nq) items = items.filter(x => x !== "" || t("sky.tz.auto").toLowerCase().includes(nq));
    act = Math.max(0, items.indexOf(chosen || ""));
    const now = new Date();
    menu.querySelector(".tz-list").innerHTML = items.length ? items.map((z, i) => {
      const name = z || deviceTz, off = fmtOffset(parts(name, now).offset);
      const label = z ? cityName(z) : t("sky.tz.auto");
      const sub = z ? z.replace(/_/g, " ") : `${cityName(deviceTz)} · ${deviceTz}`;
      return `<div class="tz-opt" role="option" id="tz-o${i}" data-tz="${z}" aria-selected="${(z || "") === (chosen || "")}"><span class="tz-off">${off}</span><span class="tz-name"><b>${label}</b><small>${sub}</small></span></div>`;
    }).join("") : `<div class="tz-empty">${t("sky.tz.none")}</div>`;
    mark();
  }
  function mark(){
    menu.querySelectorAll(".tz-opt").forEach((el, i) => el.classList.toggle("active", i === act));
    const el = menu.querySelector(`#tz-o${act}`);
    if (el) el.scrollIntoView({ block: "nearest" });
  }
  function place(){
    const r = anchor.getBoundingClientRect(), w = Math.min(360, window.innerWidth - 16);
    menu.style.width = w + "px";
    menu.style.left = Math.max(8, Math.min(r.left, window.innerWidth - w - 8)) + "px";
    const below = r.bottom + 6, maxH = window.innerHeight - below - 12;
    if (maxH > 260){ menu.style.top = below + "px"; menu.style.bottom = "auto"; menu.style.maxHeight = maxH + "px"; }
    else { menu.style.top = "auto"; menu.style.bottom = (window.innerHeight - r.top + 6) + "px"; menu.style.maxHeight = (r.top - 18) + "px"; }
  }
  function open(el){
    if (!menu) buildMenu();
    anchor = el;
    menu.querySelector(".tz-title").textContent = t("sky.tz.title");
    const input = menu.querySelector(".tz-search");
    input.placeholder = t("sky.tz.search"); input.value = "";
    menu.hidden = false;
    place();
    renderList("");
    el.setAttribute("aria-expanded", "true");
    setTimeout(() => input.focus({ preventScroll: true }), 0);
  }
  function close(){
    if (!menu || menu.hidden) return;
    menu.hidden = true;
    if (anchor){ anchor.setAttribute("aria-expanded", "false"); anchor.focus({ preventScroll: true }); }
  }
  function choose(z){
    chosen = z && valid(z) ? z : null;
    store.set(chosen);
    close();
    applySky(); renderClocks();
    document.dispatchEvent(new CustomEvent("tzchange", { detail: tz() }));
  }
  document.addEventListener("click", e => {
    const el = e.target.closest("[data-tzpicker]");
    if (!el) return;
    e.preventDefault(); e.stopPropagation();
    if (menu && !menu.hidden && anchor === el) close(); else open(el);
  });

  applySky();
  const boot = () => { renderClocks(); document.querySelectorAll("[data-tzpicker]").forEach(el => { el.setAttribute("aria-haspopup", "dialog"); el.setAttribute("aria-expanded", "false"); }); };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
  setInterval(renderClocks, 1000);
  setInterval(applySky, 60000);
  document.addEventListener("langchange", () => { renderClocks(); zoneCache = null; });

  return { tz, parts, fmtOffset, phaseOf, cityName, renderClocks, isAuto: () => !chosen };
})();
