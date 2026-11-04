"use strict";
/* ═══════════════════════════════════════════════
   機場即時天氣（2026-11）：在機場詳情面板顯示 METAR／TAF，含白話解讀、風向袋與建議使用的跑道。
   資料：/api/metar（Cloudflare Function，functions/api/metar.js，轉接 aviationweather.gov），5 分鐘快取。
   本檔自己解析 METAR 原文（不依賴上游 JSON 欄位）：風、能見度（含 CAVOK）、天氣現象、雲、溫度露點、QNH，
   並依雲幕高與能見度推算飛航類別（VFR／MVFR／IFR／LIFR）。
   建議跑道：對每條跑道兩端計算逆風／側風分量，選逆風最大者；風小於 3 kt 或風向不定時不建議。
   ※ 內容僅供參考，實際使用跑道由塔台指派。
   ═══════════════════════════════════════════════ */
const AptWeather = (() => {
  const cache = new Map();   // icao → { at, data }
  const t = (k, vars) => { let s = I18N.t("wx." + k); if (vars) for (const [a, b] of Object.entries(vars)) s = s.split(`{${a}}`).join(b); return s; };
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;" }[c]));

  /* ── METAR 解析 ── */
  const WX = { MI:"shallow", PR:"partial", BC:"patches", DR:"drifting", BL:"blowing", SH:"showers", TS:"thunderstorm", FZ:"freezing",
    DZ:"drizzle", RA:"rain", SN:"snow", SG:"snowgrains", IC:"icecrystals", PL:"icepellets", GR:"hail", GS:"smallhail", UP:"unknown",
    BR:"mist", FG:"fog", FU:"smoke", VA:"ash", DU:"dust", SA:"sand", HZ:"haze", PY:"spray", PO:"dustwhirls", SQ:"squalls", FC:"funnel", SS:"sandstorm", DS:"duststorm" };
  function frac(s){ const p = s.split(" "); let v = 0; p.forEach(x => { if (x.includes("/")){ const [a, b] = x.split("/"); v += +a / +b; } else v += +x; }); return v; }
  function parse(raw){
    const r = { raw, wind: null, visM: null, cavok: false, wx: [], clouds: [], temp: null, dew: null, qnh: null, inHg: null, time: null };
    const s = " " + raw.replace(/=+$/, "").split(/ (?:RMK|TEMPO|BECMG|NOSIG) /)[0] + " ";
    let m;
    if ((m = s.match(/ (\d{2})(\d{2})(\d{2})Z /))) r.time = { d: +m[1], h: +m[2], mi: +m[3] };
    if ((m = s.match(/ (\d{3}|VRB)(\d{2,3})(?:G(\d{2,3}))?(KT|MPS|KMH) /))){
      const k = m[4] === "MPS" ? 1.944 : m[4] === "KMH" ? .54 : 1;
      r.wind = { dir: m[1] === "VRB" ? null : +m[1], spd: Math.round(+m[2] * k), gust: m[3] ? Math.round(+m[3] * k) : null };
      const v = s.match(/ (\d{3})V(\d{3}) /);
      if (v) r.wind.vary = [+v[1], +v[2]];
    }
    if (/ CAVOK /.test(s)){ r.cavok = true; r.visM = 10000; }
    else if ((m = s.match(/ (P|M)?(\d+(?: \d\/\d)?|\d\/\d)SM /))) r.visM = Math.round(frac(m[2]) * 1609.34) + (m[1] === "P" ? 1 : 0);
    else if ((m = s.match(/ (\d{4})(?:NDV)? /))) r.visM = +m[1] === 9999 ? 10000 : +m[1];
    s.split(" ").forEach(tok => {
      const w = tok.match(/^(-|\+|VC)?((?:MI|PR|BC|DR|BL|SH|TS|FZ)?)((?:DZ|RA|SN|SG|IC|PL|GR|GS|UP|BR|FG|FU|VA|DU|SA|HZ|PY|PO|SQ|FC|SS|DS)+)$/);
      if (w && tok.length >= 2){
        const parts = (w[2] ? [w[2]] : []).concat(w[3].match(/.{2}/g));
        r.wx.push({ int: w[1] || "", parts });
      }
      const c = tok.match(/^(FEW|SCT|BKN|OVC|VV)(\d{3})(CB|TCU)?$/);
      if (c) r.clouds.push({ cover: c[1], base: +c[2] * 100, type: c[3] || "" });
      if (/^(NSC|NCD|SKC|CLR)$/.test(tok)) r.clouds.push({ cover: tok, base: null, type: "" });
    });
    if ((m = s.match(/ (M?\d{2})\/(M?\d{2})? /))){ r.temp = +m[1].replace("M", "-"); if (m[2]) r.dew = +m[2].replace("M", "-"); }
    if ((m = s.match(/ Q(\d{4}) /))){ r.qnh = +m[1]; r.inHg = +(r.qnh / 33.8639).toFixed(2); }
    else if ((m = s.match(/ A(\d{4}) /))){ r.inHg = +m[1] / 100; r.qnh = Math.round(r.inHg * 33.8639); }
    return r;
  }
  function ceiling(r){ const c = r.clouds.filter(x => /BKN|OVC|VV/.test(x.cover) && x.base != null).map(x => x.base); return c.length ? Math.min(...c) : null; }
  function fltCat(r){
    const ceil = ceiling(r), sm = r.visM != null ? r.visM / 1609.34 : null;
    const lvl = (c, v) => (c != null && c < 500) || (v != null && v < 1) ? "LIFR" : (c != null && c < 1000) || (v != null && v < 3) ? "IFR" : (c != null && c <= 3000) || (v != null && v <= 5) ? "MVFR" : "VFR";
    return lvl(ceil, sm);
  }
  // 依跑道兩端的方位計算逆風、側風；選逆風最大者
  function bestRunway(wind, runways){
    if (!wind || wind.dir == null || wind.spd < 3 || !runways || !runways.length) return null;
    const ends = [];
    runways.filter(rw => !rw.closed).forEach(rw => ["le", "he"].forEach(k => { const e = rw[k]; if (e && e.id && e.hdg != null) ends.push({ id: e.id, hdg: e.hdg }); }));
    if (!ends.length) return null;
    const rad = d => d * Math.PI / 180;
    const scored = ends.map(e => ({ ...e, head: wind.spd * Math.cos(rad(wind.dir - e.hdg)), cross: Math.abs(wind.spd * Math.sin(rad(wind.dir - e.hdg))) }));
    scored.sort((a, b) => b.head - a.head);
    return scored[0].head > 0 ? scored[0] : null;
  }

  /* ── 文字 ── */
  const dirName = deg => t("dir." + ["N","NE","E","SE","S","SW","W","NW"][Math.round(deg / 45) % 8]);
  function windText(w){
    if (!w) return "—";
    if (w.spd === 0) return t("calm");
    const base = w.dir == null ? t("vrb", { spd: w.spd }) : t("wind", { dir: String(w.dir).padStart(3, "0"), name: dirName(w.dir), spd: w.spd });
    return base + (w.gust ? t("gust", { g: w.gust }) : "") + (w.vary ? t("vary", { a: w.vary[0], b: w.vary[1] }) : "");
  }
  const visText = r => r.cavok ? t("cavok") : r.visM == null ? "—" : r.visM >= 10000 ? t("vis10") : r.visM >= 1000 ? `${(r.visM / 1000).toFixed(r.visM % 1000 ? 1 : 0)} km` : `${r.visM} m`;
  function cloudText(r){
    if (r.cavok) return t("cloud.none");
    if (!r.clouds.length) return "—";
    return r.clouds.map(c => c.base == null ? t("cloud." + c.cover) : `${t("cloud." + c.cover)} ${c.base.toLocaleString()} ft${c.type ? " " + t("cloud." + c.type) : ""}`).join("、");
  }
  const wxText = r => r.wx.map(w => (w.int === "-" ? t("int.light") : w.int === "+" ? t("int.heavy") : w.int === "VC" ? t("int.vc") : "") + w.parts.map(p => t("ph." + (WX[p] || p))).join("")).join("、");
  function ago(sec){
    if (!sec) return "";
    const min = Math.max(0, Math.round((Date.now() / 1000 - sec) / 60));
    return min < 60 ? t("ago.min", { n: min }) : t("ago.h", { n: Math.floor(min / 60), m: min % 60 });
  }

  /* ── 風向袋（SVG）：袋口朝風吹來的方向，袋尾指向下風處；風越大袋子越鼓（5 段條紋） ── */
  function sockSVG(w){
    const spd = w ? w.spd : 0, dir = w && w.dir != null ? w.dir : null;
    const fill = Math.max(0, Math.min(5, Math.round(spd / 3)));   // 每 3 kt 撐起一段，15 kt 以上全滿
    // 袋子畫在 +x（東，方位 90°）。風向是「風吹來的方向」，袋尾指向下風處（風向 + 180°），所以轉 dir + 90°
    const rot = dir == null ? 135 : dir + 90;
    const stripes = [0,1,2,3,4].map(i => `<path d="M${14 + i * 11} ${-9 + i * 1.3} L${25 + i * 11} ${-7.7 + i * 1.3} L${25 + i * 11} ${7.7 - i * 1.3} L${14 + i * 11} ${9 - i * 1.3} Z" class="${i % 2 ? "wx-s1" : "wx-s0"}" opacity="${i < fill ? 1 : .3}"/>`).join("");
    return `<svg class="wx-sock" viewBox="-80 -80 160 160" aria-hidden="true">
      <circle r="70" class="wx-ring"/><text y="-56" class="wx-n">N</text><text x="60" y="4" class="wx-n">E</text><text y="66" class="wx-n">S</text><text x="-60" y="4" class="wx-n">W</text>
      <g transform="rotate(${rot})"><line x1="0" y1="0" x2="14" y2="0" class="wx-pole"/>${stripes}</g>
      <circle r="4" class="wx-hub"/></svg>`;
  }

  async function fetchMetar(icao){
    const c = cache.get(icao);
    if (c && Date.now() - c.at < 300000) return c.data;
    const res = await fetch(`/api/metar?ids=${encodeURIComponent(icao)}`);
    if (res.status === 404 || res.status === 405) throw Object.assign(new Error("no-function"), { code: "nofn" });
    if (!res.ok) throw new Error(String(res.status));
    const ct = res.headers.get("content-type") || "";
    if (!ct.includes("json")) throw Object.assign(new Error("no-function"), { code: "nofn" });
    const list = await res.json();
    const data = (Array.isArray(list) ? list : []).find(x => x.icao === icao) || null;
    cache.set(icao, { at: Date.now(), data });
    return data;
  }

  async function render(box, icao, runways, isCurrent){
    if (!box) return;
    if (!icao || !/^[A-Z0-9]{4}$/.test(icao)){ box.innerHTML = `<div class="wx-msg">${esc(t("noicao"))}</div>`; return; }
    box.innerHTML = `<div class="wx-msg">${esc(t("loading"))}</div>`;
    let d;
    try { d = await fetchMetar(icao); }
    catch (e) {
      if (!isCurrent()) return;
      box.innerHTML = `<div class="wx-msg">${esc(t(e.code === "nofn" ? "nofn" : "error"))}</div>`;
      return;
    }
    if (!isCurrent()) return;
    if (!d){ box.innerHTML = `<div class="wx-msg">${esc(t("none", { icao }))}</div>`; return; }
    const r = parse(d.raw);
    const cat = /^(VFR|MVFR|IFR|LIFR)$/.test(d.fltCat) ? d.fltCat : fltCat(r);
    const best = bestRunway(r.wind, runways);
    const rows = [
      ["wind", windText(r.wind)],
      ["vis", visText(r)],
      r.wx.length ? ["wxnow", wxText(r)] : null,
      ["clouds", cloudText(r)],
      ["temp", r.temp == null ? "—" : `${r.temp}°C${r.dew != null ? ` / ${t("dew")} ${r.dew}°C` : ""}`],
      ["qnh", r.qnh == null ? "—" : `${r.qnh} hPa（${r.inHg.toFixed(2)} inHg）`]
    ].filter(Boolean);
    const rwText = best ? t("rwy.best", { id: best.id, head: Math.round(best.head), cross: Math.round(best.cross) })
      : r.wind && r.wind.dir != null && r.wind.spd >= 3 ? "" : t("rwy.calm");
    box.innerHTML = `<div class="wx-card">
      <div class="wx-top">
        ${sockSVG(r.wind)}
        <div class="wx-summary">
          <span class="wx-cat wx-${cat.toLowerCase()}">${cat}</span>
          <span class="wx-cat-name">${esc(t("cat." + cat))}</span>
          <span class="wx-time">${esc(d.time ? ago(d.time) : r.time ? t("obs", { d: r.time.d, h: String(r.time.h).padStart(2, "0"), m: String(r.time.mi).padStart(2, "0") }) : "")}</span>
          ${rwText ? `<span class="wx-rwy">${esc(rwText)}</span>` : ""}
        </div>
      </div>
      <dl class="wx-grid">${rows.map(([k, v]) => `<div><dt>${esc(t("f." + k))}</dt><dd>${esc(v)}</dd></div>`).join("")}</dl>
      <div class="wx-raw"><span>METAR</span><code>${esc(d.raw)}</code></div>
      ${d.taf ? `<details class="wx-taf"><summary>${esc(t("taf"))}</summary><code>${esc(d.taf)}</code></details>` : ""}
      <p class="wx-src">${esc(t("src"))}</p>
    </div>`;
  }

  return { render, parse, fltCat, bestRunway };
})();
