"use strict";
/* 天空檔案 — 離線快取（Service Worker）
   頁面：network-first（在線時永遠拿最新）；靜態資源／資料：
   stale-while-revalidate（先回快取，背景更新）。無版本耦合，
   ?v=N 等查詢字串照樣被當成獨立 URL 快取，部署後自動更新。 */
const CACHE = "hangar-v1";
const SHELL = ["index.html", "viewer.html", "compare.html", "editor.html",
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

  if (req.mode === "navigate"){
    e.respondWith(fetch(req).catch(() => caches.match(req).then(r => r || caches.match("index.html"))));
    return;
  }

  e.respondWith(
    caches.match(req).then(cached => {
      const network = fetch(req).then(res => {
        if (res.ok) caches.open(CACHE).then(c => c.put(req, res.clone()));
        return res;
      }).catch(() => cached);
      return cached || network;
    })
  );
});
