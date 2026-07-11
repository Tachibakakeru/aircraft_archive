"use strict";
/* 天空檔案 — 離線快取（Service Worker）
   頁面：network-first（在線時永遠拿最新）；靜態資源／資料：
   stale-while-revalidate（先回快取，背景更新）。無版本耦合，
   ?v=N 等查詢字串照樣被當成獨立 URL 快取，部署後自動更新。
   衛星圖磚另外走獨立的 cache-first 快取（見下方 TILE_CACHE），
   跟主要快取分開，容量壓力互不影響。 */
const CACHE = "hangar-v1";
const TILE_CACHE = "hangar-tiles-v1";
const TILE_HOSTS = ["server.arcgisonline.com"];
const TILE_LIMIT = 800;   // 圖磚快取上限筆數，超過時淘汰最舊的（Cache.keys() 近似插入序）
const SHELL = ["index.html", "viewer.html", "compare.html", "editor.html",
               "airports.html", "variants.html",
               "manifest.json", "assets/icon.svg"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE && k !== TILE_CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

async function trimTileCache(){
  const c = await caches.open(TILE_CACHE);
  const keys = await c.keys();
  const over = keys.length - TILE_LIMIT;
  if (over > 0) await Promise.all(keys.slice(0, over).map(k => c.delete(k)));
}

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;

  const url = new URL(req.url);
  if (url.protocol !== "http:" && url.protocol !== "https:") return;   // Cache API 不支援 chrome-extension: 等其他協定

  // 衛星圖磚：獨立的 cache-first 快取，圖磚內容不會變，不需 revalidate，
  // 也不進主要 Cache，跟一般資源的容量壓力互不影響（見檔頭說明）。
  if (TILE_HOSTS.includes(url.hostname)){
    e.respondWith(
      caches.open(TILE_CACHE).then(async c => {
        const cached = await c.match(req);
        if (cached) return cached;
        try {
          const res = await fetch(req);
          if (res.ok){
            c.put(req, res.clone());
            trimTileCache();
          }
          return res;
        } catch { return cached || Response.error(); }
      })
    );
    return;
  }

  if (url.origin !== self.location.origin) return;   // 其餘第三方資源交回瀏覽器原生快取，不進我們自己的 Cache
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
