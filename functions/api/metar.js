/* ═══════════════════════════════════════════════
   Cloudflare Pages Function — 機場即時天氣（METAR／TAF）轉接
   ─────────────────────────────────────────────
   GET /api/metar?ids=RCTP[,RJTT…]（最多 4 個 ICAO 代碼）
   向美國航空氣象中心（NOAA Aviation Weather Center，aviationweather.gov）的公開資料 API 取得
   最新 METAR 與 TAF，整理成精簡格式回傳：
     [{ "icao": "RCTP", "raw": "<METAR 原文>", "taf": "<TAF 原文或空字串>", "time": <觀測時間 epoch 秒>, "fltCat": "VFR" }]
   前端（js/metar.js）自己解析 METAR 原文，所以這裡只需要原文，不依賴上游 JSON 的其他欄位。
   - 不需要金鑰；上游請求帶一般用途的 User-Agent。
   - 用 Cloudflare 快取 5 分鐘（METAR 通常每 30–60 分鐘更新一次），減少對上游的請求。
   - JSON 端點失敗時改用 raw 文字端點。
   ═══════════════════════════════════════════════ */

const UPSTREAM = "https://aviationweather.gov/api/data";
const HEADERS = { "User-Agent": "SkyArchive/1.0 (aviation reference site)", "Accept": "application/json, text/plain" };

function reply(body, status = 200) {
  return new Response(typeof body === "string" ? body : JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": status === 200 ? "public, max-age=300" : "no-store",
    },
  });
}

async function fetchJSON(ids) {
  const res = await fetch(`${UPSTREAM}/metar?ids=${ids}&format=json&taf=true`, { headers: HEADERS, cf: { cacheTtl: 300, cacheEverything: true } });
  if (res.status === 204) return [];
  if (!res.ok) throw new Error(`upstream ${res.status}`);
  const list = await res.json();
  if (!Array.isArray(list)) throw new Error("unexpected payload");
  return list.filter(x => x && (x.rawOb || x.rawMetar)).map(x => ({
    icao: String(x.icaoId || x.stationId || "").toUpperCase(),
    raw: String(x.rawOb || x.rawMetar || "").trim(),
    taf: String(x.rawTaf || "").trim(),
    time: Number(x.obsTime) || null,
    fltCat: String(x.fltCat || x.flightCategory || ""),
  }));
}

// 備援：raw 文字端點，一行一筆
async function fetchRaw(ids) {
  const get = async kind => {
    const res = await fetch(`${UPSTREAM}/${kind}?ids=${ids}&format=raw`, { headers: HEADERS, cf: { cacheTtl: 300, cacheEverything: true } });
    return res.ok ? (await res.text()).trim() : "";
  };
  const [metar, taf] = await Promise.all([get("metar"), get("taf")]);
  const out = [];
  metar.split(/\n+/).map(s => s.trim()).filter(Boolean).forEach(line => {
    const m = line.match(/^(?:METAR |SPECI )?([A-Z0-9]{4}) /);
    if (!m) return;
    const icao = m[1];
    const t = taf.split(/\n(?=TAF |[A-Z0-9]{4} \d{6}Z)/).find(x => x.includes(icao)) || "";
    out.push({ icao, raw: line, taf: t.trim(), time: null, fltCat: "" });
  });
  return out;
}

export async function onRequestGet({ request }) {
  const url = new URL(request.url);
  const ids = (url.searchParams.get("ids") || "")
    .toUpperCase().split(",").map(s => s.trim()).filter(s => /^[A-Z0-9]{4}$/.test(s)).slice(0, 4).join(",");
  if (!ids) return reply({ error: "ids 參數需要 1–4 個 ICAO 代碼" }, 400);

  const cache = caches.default;
  const key = new Request(`${url.origin}/api/metar?ids=${ids}`);
  const hit = await cache.match(key);
  if (hit) return hit;

  let data;
  try { data = await fetchJSON(ids); }
  catch (e) {
    try { data = await fetchRaw(ids); }
    catch (e2) { return reply({ error: "暫時無法取得天氣資料" }, 502); }
  }
  const res = reply(data);
  await cache.put(key, res.clone());
  return res;
}
