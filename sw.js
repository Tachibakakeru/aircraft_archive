"use strict";
/* 天空檔案 — 離線快取（Service Worker）
   頁面：network-first（在線時永遠拿最新）；靜態資源／資料：
   stale-while-revalidate（先回快取，背景更新）。無版本耦合，
   ?v=N 等查詢字串照樣被當成獨立 URL 快取，部署後自動更新。 */
const CACHE = "hangar-v1";
const SHELL = ["index.html", "viewer.html", "compare.html", "editor.html",
               "airports.html", "variants.html",
               "manifest.json", "assets/icon.svg"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;

  const url = new URL(req.url);
  if (url.protocol !== "http:" && url.protocol !== "https:") return;   // Cache API 不支援 chrome-extension: 等其他協定
  if (url.origin !== self.location.origin) return;   // 只管自己網域的資源；第三方（如衛星圖磚）交給瀏覽器原生快取，
                                                       // 不要塞進我們自己的 Cache——快取一堆跨網域 opaque 回應在手機
                                                       // Safari 這類對 SW 快取容量管理較激進的瀏覽器上，容易在容量
                                                       // 壓力下被部分淘汰、部分保留，造成同一批圖磚新舊混雜的怪異畫面。
  if (url.pathname.startsWith("/api/")) return;   // 即時 API：一律直連網路，不快取、不攔截

  if (req.mode === "navigate"){
    e.respondWith(fetch(req).catch(() => caches.match(req).then(r => r || caches.match("index.html"))));
    return;
  }

  e.respondWith(
    caches.match(req).then(cached => {
      const network = fetch(req).then(res => {
        if (res.ok){
          // 先同步 clone，再進非同步的 caches.open()，避免頁面已讀完本體後才 clone 而噴錯
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(req, copy));
        }
        return res;
      }).catch(() => cached);
      return cached || network;
    })
  );
});
