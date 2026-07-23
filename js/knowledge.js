"use strict";
/* ═══════════════════════════════════════════════
   航空小知識 — 互動座艙儀表面板 + 補充知識卡片
   資料來源 data/knowledge.json（單一檔案，topics 陣列）。
   內容欄位（name/summary/fact）沿用機型 parts 相同的
   {zh,en,ja} 物件格式，I18N.field() 解析；編輯機制沿用
   airports.js 的「本機草稿 + 密碼發布」模式，共用
   auth.js / storage.js，不另建後端。
   ═══════════════════════════════════════════════ */

const $ = id => document.getElementById(id);
const F = v => I18N.field(v);

// 每個場景是一整排連續可橫向捲動的主題（不分頁、不分組），
// 同一類別以後加新主題時，只要在對應陣列多加一筆即可，會自動排進同一行。
// 捲動與收尾相接（最後一個接續回到第一個）交給原生 CSS scroll-snap + 內容
// 三倍複製處理（見 renderTrack／wireLoop），滑鼠則用簡單拖曳改 scrollLeft。

const INSTRUMENT_TOPICS = [
  { id: "asi", label: "ASI" },
  { id: "ai",  label: "AI" },
  { id: "alt", label: "ALT" },
  { id: "tc",  label: "TC" },
  { id: "hdg", label: "HDG" },
  { id: "vsi", label: "VSI" },
  { id: "adf",     label: "ADF" },
  { id: "dme",     label: "DME" },
  { id: "radalt",  label: "RA" },
  { id: "standby", label: "STBY" },
  { id: "efis",    label: "EFIS" },
];

const RUNWAY_TOPICS = [
  { id: "runway-numbering", label: "RWY 27" },
  { id: "v-speeds",         label: "V1 VR V2" },
  { id: "wake",              label: "WAKE" },
  { id: "windshear",         label: "SHEAR" },
  { id: "decision-height",  label: "DA(H)" },
  { id: "weight-balance",   label: "W&B" },
  { id: "mtow",              label: "MTOW" },
  { id: "thrust-reverser",  label: "REV" },
  { id: "flaps-slats",      label: "FLAP" },
  { id: "crosswind",        label: "XWIND" },
  { id: "rvr",               label: "RVR" },
];
const NAV_TOPICS = [
  { id: "ils",          label: "ILS" },
  { id: "holding",      label: "HOLD" },
  { id: "flight-level", label: "FL" },
  { id: "jetstream",    label: "JET" },
  { id: "vor",                  label: "VOR" },
  { id: "rnav",                 label: "RNAV" },
  { id: "transition-altitude",  label: "TA/TL" },
  { id: "airspace-class",       label: "A-G" },
  { id: "notam",                label: "NOTAM" },
  { id: "great-circle",         label: "GC" },
  { id: "adsb",                 label: "ADS-B" },
];
const SYSTEMS_TOPICS = [
  { id: "squawk", label: "SQUAWK" },
  { id: "stall",  label: "STALL" },
  { id: "mach",   label: "MACH" },
  { id: "etops",  label: "ETOPS" },
  { id: "pressurization", label: "PRESS" },
  { id: "deicing",        label: "DE-ICE" },
  { id: "apu",             label: "APU" },
  { id: "fuel-dumping",   label: "DUMP" },
  { id: "pitot-static",   label: "PITOT" },
  { id: "edto",            label: "EDTO" },
  { id: "fdr-cvr",         label: "FDR/CVR" },
];

let TOPICS = [];
let byId = {};
let currentTopicId = null;
let editingImages = [];
let isNewTopic = false;
let newTopicScene = null;

const LOCAL_KEY = "hangar_knowledge_local";
function loadLocal(){ try { return JSON.parse(localStorage.getItem(LOCAL_KEY) || "{}"); } catch { return {}; } }
function getLocalOverride(id){ return loadLocal()[id] || null; }
function saveLocalOverride(id, override){
  const store = loadLocal();
  store[id] = override;
  localStorage.setItem(LOCAL_KEY, JSON.stringify(store));
}

const CUSTOM_TOPICS_KEY = "hangar_knowledge_custom";
function loadCustomTopics(){ try { return JSON.parse(localStorage.getItem(CUSTOM_TOPICS_KEY) || "[]"); } catch { return []; } }
function saveCustomTopics(arr){ try { localStorage.setItem(CUSTOM_TOPICS_KEY, JSON.stringify(arr)); } catch { alert("暫存失敗：資料可能過大"); } }
function mergedTopic(id){
  const base = byId[id];
  if (!base) return null;
  const local = getLocalOverride(id);
  return local ? { ...base, ...local, _local: true } : base;
}
// 保留其他語言：只替換目前語言那一格，其餘沿用原物件
function nextFieldValue(baseVal, plainText){
  const lang = I18N.get();
  if (baseVal && typeof baseVal === "object") return { ...baseVal, [lang]: plainText };
  return { zh: plainText };
}

/* ── polar / arc 小工具 ── */
function polar(cx, cy, r, deg){
  const rad = (deg - 90) * Math.PI / 180;
  return { x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad) };
}
function arcPath(cx, cy, r, a1, a2){
  const p1 = polar(cx, cy, r, a1), p2 = polar(cx, cy, r, a2);
  const large = (a2 - a1) % 360 > 180 ? 1 : 0;
  return `M ${p1.x.toFixed(1)} ${p1.y.toFixed(1)} A ${r} ${r} 0 ${large} 1 ${p2.x.toFixed(1)} ${p2.y.toFixed(1)}`;
}
function ticks(cx, cy, r1, r2, count){
  let s = "";
  for (let i = 0; i < count; i++){
    const deg = (360 / count) * i;
    const a = polar(cx, cy, r1, deg), b = polar(cx, cy, r2, deg);
    const major = i % 3 === 0;
    s += `<line x1="${a.x.toFixed(1)}" y1="${a.y.toFixed(1)}" x2="${b.x.toFixed(1)}" y2="${b.y.toFixed(1)}" class="kn-tick${major ? " major" : ""}"/>`;
  }
  return s;
}
function needle(cx, cy, r, deg, cls){
  const p = polar(cx, cy, r, deg);
  return `<line x1="${cx}" y1="${cy}" x2="${p.x.toFixed(1)}" y2="${p.y.toFixed(1)}" class="${cls}"/>`;
}
// 準星（targeting reticle）：非儀表場景的通用可點擊圖示外框
function reticle(cx, cy, r){
  let s = `<circle cx="${cx}" cy="${cy}" r="${r}" class="kn-hs-ring"/>`;
  [0, 90, 180, 270].forEach(deg => {
    const a = polar(cx, cy, r - 7, deg), b = polar(cx, cy, r + 3, deg);
    s += `<line x1="${a.x.toFixed(1)}" y1="${a.y.toFixed(1)}" x2="${b.x.toFixed(1)}" y2="${b.y.toFixed(1)}" class="kn-hs-tick"/>`;
  });
  return s;
}

/* ── 每具儀表的裝飾內容（示意用，非真實連動數值）── */
function gaugeDecor(id, cx, cy){
  const r = 74;
  switch (id){
    case "asi":
      return `
        <path d="${arcPath(cx, cy, r - 8, 40, 210)}" class="kn-arc kn-arc-green"/>
        <path d="${arcPath(cx, cy, r - 8, 210, 250)}" class="kn-arc kn-arc-yellow"/>
        ${needle(cx, cy, r - 14, 155, "kn-needle kn-needle-long")}
        <text x="${cx}" y="${cy - r + 20}" class="kn-g-unit">KT</text>`;
    case "ai":
      return `
        <clipPath id="kn-clip-${id}"><circle cx="${cx}" cy="${cy}" r="${r - 6}"/></clipPath>
        <g clip-path="url(#kn-clip-${id})">
          <rect x="${cx - r}" y="${cy - r}" width="${r * 2}" height="${r}" class="kn-ai-sky"/>
          <rect x="${cx - r}" y="${cy}" width="${r * 2}" height="${r}" class="kn-ai-ground"/>
          <line x1="${cx - r}" y1="${cy}" x2="${cx + r}" y2="${cy}" class="kn-ai-horizon"/>
        </g>
        <path d="M ${cx - 26} ${cy} h 16 M ${cx + 10} ${cy} h 16 M ${cx - 4} ${cy} l 4 6 l 4 -6" class="kn-ai-wings"/>`;
    case "alt":
      return `
        ${needle(cx, cy, r - 10, 300, "kn-needle kn-needle-long")}
        ${needle(cx, cy, r - 30, 60, "kn-needle kn-needle-short")}
        <rect x="${cx - 24}" y="${cy + r - 26}" width="48" height="17" rx="2" class="kn-kollsman"/>
        <text x="${cx}" y="${cy + r - 13}" class="kn-kollsman-txt">29.92</text>`;
    case "tc":
      return `
        <path d="M ${cx - 30} ${cy - 4} L ${cx + 30} ${cy + 6} M ${cx - 4} ${cy - 14} L ${cx - 30} ${cy - 4} M ${cx + 4} ${cy + 16} L ${cx + 30} ${cy + 6}" class="kn-tc-wing"/>
        <circle cx="${cx}" cy="${cy}" r="4" class="kn-tc-body"/>
        <rect x="${cx - 26}" y="${cy + r - 24}" width="52" height="14" rx="7" class="kn-tc-tube"/>
        <circle cx="${cx - 4}" cy="${cy + r - 17}" r="4.5" class="kn-tc-ball"/>`;
    case "hdg":
      return `
        <text x="${cx}" y="${cy - r + 22}" class="kn-hdg-letter">N</text>
        <text x="${cx + r - 18}" y="${cy + 5}" class="kn-hdg-letter">E</text>
        <text x="${cx}" y="${cy + r - 12}" class="kn-hdg-letter">S</text>
        <text x="${cx - r + 18}" y="${cy + 5}" class="kn-hdg-letter">W</text>
        <path d="M ${cx} ${cy - r + 4} l -6 12 h12 z" class="kn-hdg-lubber"/>`;
    case "vsi":
      return `
        <text x="${cx}" y="${cy - r + 20}" class="kn-g-unit">UP</text>
        <text x="${cx}" y="${cy + r - 10}" class="kn-g-unit">DN</text>
        ${needle(cx, cy, r - 14, 335, "kn-needle kn-needle-long")}`;
    case "adf":
      return `
        <text x="${cx}" y="${cy - r + 22}" class="kn-hdg-letter">N</text>
        ${needle(cx, cy, r - 16, 110, "kn-needle kn-needle-long")}
        <circle cx="${cx}" cy="${cy}" r="4" class="kn-g-hub"/>`;
    case "dme":
      return `
        <rect x="${cx - 26}" y="${cy - 14}" width="52" height="24" rx="2" class="kn-kollsman"/>
        <text x="${cx}" y="${cy + 4}" class="kn-kollsman-txt">42.3</text>
        <text x="${cx}" y="${cy + r - 14}" class="kn-g-unit">NM</text>`;
    case "radalt":
      return `
        <rect x="${cx - 22}" y="${cy - r + 14}" width="44" height="20" rx="2" class="kn-kollsman"/>
        <text x="${cx}" y="${cy - r + 29}" class="kn-kollsman-txt">50</text>
        <path d="M ${cx - 4} ${cy - 6} L ${cx} ${cy + 16} L ${cx + 4} ${cy - 6}" class="kn-needle kn-needle-short" fill="none"/>
        <line x1="${cx - 26}" y1="${cy + r - 16}" x2="${cx + 26}" y2="${cy + r - 16}" class="kn-fl-line major"/>`;
    case "standby":
      return `
        <circle cx="${cx - 18}" cy="${cy}" r="22" class="kn-g-face"/>
        <circle cx="${cx + 18}" cy="${cy}" r="22" class="kn-g-face"/>
        ${needle(cx - 18, cy, 15, 140, "kn-needle kn-needle-short")}
        ${needle(cx + 18, cy, 15, 320, "kn-needle kn-needle-short")}`;
    case "efis":
      return `
        <rect x="${cx - 34}" y="${cy - 30}" width="68" height="60" rx="4" class="kn-squawk-box"/>
        <line x1="${cx - 26}" y1="${cy}" x2="${cx + 26}" y2="${cy}" class="kn-ai-horizon"/>
        <path d="M ${cx - 12} ${cy} l 12 -8 l 12 8" class="kn-ai-wings"/>`;
    default: return "";
  }
}
// 每格獨立一顆 svg（座標系只服務自己這一格），可以單純排成一整行橫向捲動
// 儀表面板上的縮寫（ASI、AI…）是真實座艙慣用代碼，刻意不隨語言翻譯；
// 下方另外加一行當前語言的正式名稱，隨切換語言即時更新（見 renderTrack）。
function topicName(id){
  const base = byId[id];
  return (base && F(base.name)) || "";
}
function buildGaugeItem(t){
  const cx = 95, cy = 95;
  const name = topicName(t.id);
  return `
    <div class="kn-item" data-topic="${t.id}" tabindex="0" role="button" aria-label="${name || t.label}">
      <svg viewBox="0 0 190 190" class="kn-gauge kn-hotspot">
        <circle cx="${cx}" cy="${cy}" r="82" class="kn-g-bezel"/>
        <circle cx="${cx}" cy="${cy}" r="74" class="kn-g-face"/>
        ${ticks(cx, cy, 66, 74, 24)}
        ${gaugeDecor(t.id, cx, cy)}
        <circle cx="${cx}" cy="${cy}" r="6" class="kn-g-hub"/>
        <text x="${cx}" y="${cy + 62}" class="kn-g-label">${t.label}</text>
        <ellipse cx="${cx - 22}" cy="${cy - 30}" rx="30" ry="16" class="kn-g-glare"/>
      </svg>
      <div class="kn-item-name">${name}</div>
    </div>`;
}
/* ── 其餘三個場景：每個主題各自的示意圖示（準星 + 圖形 + 標籤）── */
const RUNWAY_DECOR = {
  "runway-numbering": (cx, cy) => `
    <rect x="${cx - 11}" y="${cy - 34}" width="22" height="68" class="kn-rwy-strip"/>
    <line x1="${cx}" y1="${cy - 28}" x2="${cx}" y2="${cy - 12}" class="kn-rwy-dash"/>
    <line x1="${cx}" y1="${cy - 4}" x2="${cx}" y2="${cy + 12}" class="kn-rwy-dash"/>
    <text x="${cx}" y="${cy + 26}" class="kn-rwy-num">27</text>`,
  "v-speeds": (cx, cy) => `
    <path d="M ${cx - 22} ${cy + 12} L ${cx + 6} ${cy - 4} L ${cx + 22} ${cy - 16} L ${cx + 10} ${cy - 6} L ${cx - 4} ${cy - 2} Z" class="kn-vspeed-plane"/>
    <path d="M ${cx + 18} ${cy - 24} l 8 -6 m -8 6 l 1 -9 m -1 9 l 9 1" class="kn-vspeed-arrow"/>`,
  wake: (cx, cy) => `
    <line x1="${cx - 26}" y1="${cy}" x2="${cx - 4}" y2="${cy}" class="kn-wake-wing"/>
    <path d="${arcPath(cx + 6, cy, 8, 0, 300)}" class="kn-wake-spiral"/>
    <path d="${arcPath(cx + 6, cy, 15, 40, 320)}" class="kn-wake-spiral"/>
    <path d="${arcPath(cx + 6, cy, 22, 80, 340)}" class="kn-wake-spiral"/>`,
  windshear: (cx, cy) => `
    <circle cx="${cx - 12}" cy="${cy - 14}" r="10" class="kn-cloud"/>
    <circle cx="${cx}" cy="${cy - 18}" r="13" class="kn-cloud"/>
    <circle cx="${cx + 14}" cy="${cy - 13}" r="10" class="kn-cloud"/>
    <path d="M ${cx - 8} ${cy - 2} l -4 14 l 6 -4 l -3 14" class="kn-shear-arrow"/>
    <path d="M ${cx + 10} ${cy - 2} l -4 14 l 6 -4 l -3 14" class="kn-shear-arrow"/>`,
  "decision-height": (cx, cy) => `
    <line x1="${cx}" y1="${cy - 22}" x2="${cx}" y2="${cy + 10}" class="kn-vspeed-arrow"/>
    <path d="M ${cx - 6} ${cy + 2} L ${cx} ${cy + 12} L ${cx + 6} ${cy + 2}" class="kn-vspeed-arrow"/>
    <line x1="${cx - 20}" y1="${cy + 18}" x2="${cx + 20}" y2="${cy + 18}" class="kn-fl-line major" stroke-dasharray="4 3"/>`,
  "weight-balance": (cx, cy) => `
    <line x1="${cx - 22}" y1="${cy - 6}" x2="${cx + 22}" y2="${cy - 6}" class="kn-fl-line major"/>
    <path d="M ${cx} ${cy - 6} L ${cx - 8} ${cy + 14} L ${cx + 8} ${cy + 14} Z" class="kn-tc-wing"/>
    <circle cx="${cx - 18}" cy="${cy + 2}" r="4" class="kn-g-hub"/>
    <circle cx="${cx + 18}" cy="${cy + 2}" r="4" class="kn-g-hub"/>`,
  mtow: (cx, cy) => `
    <rect x="${cx - 16}" y="${cy - 4}" width="32" height="18" class="kn-rwy-strip"/>
    <path d="M ${cx} ${cy - 24} L ${cx} ${cy - 8} M ${cx - 6} ${cy - 14} L ${cx} ${cy - 8} L ${cx + 6} ${cy - 14}" class="kn-vspeed-arrow"/>`,
  "thrust-reverser": (cx, cy) => `
    <circle cx="${cx}" cy="${cy}" r="10" class="kn-etops-ring"/>
    <path d="M ${cx - 6} ${cy - 14} q -14 0 -14 14" class="kn-jet-arrow"/>
    <path d="M ${cx + 6} ${cy - 14} q 14 0 14 14" class="kn-jet-arrow"/>
    <path d="M ${cx - 24} ${cy} l -6 -4 l 2 8" class="kn-jet-arrow"/>
    <path d="M ${cx + 24} ${cy} l 6 -4 l -2 8" class="kn-jet-arrow"/>`,
  "flaps-slats": (cx, cy) => `
    <path d="M ${cx - 22} ${cy - 4} Q ${cx - 4} ${cy - 14} ${cx + 10} ${cy - 6}" class="kn-stall-wing"/>
    <path d="M ${cx + 10} ${cy - 6} L ${cx + 22} ${cy + 10}" class="kn-stall-wing"/>`,
  crosswind: (cx, cy) => `
    <path d="M ${cx} ${cy - 16} L ${cx + 6} ${cy + 12} L ${cx} ${cy + 6} L ${cx - 6} ${cy + 12} Z" class="kn-vspeed-plane"/>
    <path d="M ${cx - 26} ${cy - 2} L ${cx - 10} ${cy - 2} M ${cx - 14} ${cy - 6} L ${cx - 10} ${cy - 2} L ${cx - 14} ${cy + 2}" class="kn-wake-wing" fill="none"/>`,
  rvr: (cx, cy) => `
    <line x1="${cx - 22}" y1="${cy - 10}" x2="${cx + 22}" y2="${cy - 10}" class="kn-fl-line"/>
    <line x1="${cx - 22}" y1="${cy}" x2="${cx + 22}" y2="${cy}" class="kn-fl-line major"/>
    <line x1="${cx - 22}" y1="${cy + 10}" x2="${cx + 22}" y2="${cy + 10}" class="kn-fl-line"/>
    <circle cx="${cx}" cy="${cy}" r="26" class="kn-cloud" opacity="0.35"/>`,
};
const NAV_DECOR = {
  ils: (cx, cy) => `
    <path d="M ${cx - 20} ${cy + 20} l 6 -16 l 6 16 z" class="kn-ils-mast"/>
    <path d="M ${cx - 14} ${cy + 4} L ${cx + 22} ${cy - 22}" class="kn-ils-beam"/>
    <circle cx="${cx + 22}" cy="${cy - 22}" r="3.5" class="kn-ils-plane"/>`,
  holding: (cx, cy) => `
    <rect x="${cx - 22}" y="${cy - 12}" width="44" height="24" rx="12" class="kn-holding-track"/>
    <path d="M ${cx + 20} ${cy - 14} l 6 3 l -5 5" class="kn-holding-arrow"/>`,
  "flight-level": (cx, cy) => `
    <line x1="${cx - 22}" y1="${cy - 18}" x2="${cx + 18}" y2="${cy - 18}" class="kn-fl-line"/>
    <line x1="${cx - 22}" y1="${cy}" x2="${cx + 18}" y2="${cy}" class="kn-fl-line major"/>
    <line x1="${cx - 22}" y1="${cy + 18}" x2="${cx + 18}" y2="${cy + 18}" class="kn-fl-line"/>
    <text x="${cx + 22}" y="${cy - 15}" class="kn-fl-text">390</text>
    <text x="${cx + 22}" y="${cy + 3}" class="kn-fl-text">350</text>
    <text x="${cx + 22}" y="${cy + 21}" class="kn-fl-text">290</text>`,
  jetstream: (cx, cy) => `
    <path d="M ${cx - 24} ${cy} q 8 -14 16 0 t 16 0 t 16 0" class="kn-jet-ribbon"/>
    <path d="M ${cx + 20} ${cy - 4} l 8 4 l -8 4" class="kn-jet-arrow"/>`,
  vor: (cx, cy) => `
    <circle cx="${cx}" cy="${cy}" r="16" class="kn-holding-track"/>
    <line x1="${cx}" y1="${cy - 22}" x2="${cx}" y2="${cy - 10}" class="kn-fl-line major"/>
    <line x1="${cx + 19}" y1="${cy - 11}" x2="${cx + 11}" y2="${cy - 6}" class="kn-fl-line major"/>
    <line x1="${cx + 19}" y1="${cy + 11}" x2="${cx + 11}" y2="${cy + 6}" class="kn-fl-line major"/>
    <line x1="${cx}" y1="${cy + 22}" x2="${cx}" y2="${cy + 10}" class="kn-fl-line major"/>
    <line x1="${cx - 19}" y1="${cy + 11}" x2="${cx - 11}" y2="${cy + 6}" class="kn-fl-line major"/>
    <line x1="${cx - 19}" y1="${cy - 11}" x2="${cx - 11}" y2="${cy - 6}" class="kn-fl-line major"/>`,
  rnav: (cx, cy) => `
    <circle cx="${cx - 16}" cy="${cy - 16}" r="5" class="kn-ils-plane"/>
    <path d="M ${cx - 16} ${cy - 16} L ${cx + 16} ${cy + 12}" class="kn-ils-beam"/>
    <path d="M ${cx + 16} ${cy + 6} l 6 6 l -6 6 l -6 -6 z" class="kn-holding-arrow"/>`,
  "transition-altitude": (cx, cy) => `
    <line x1="${cx - 20}" y1="${cy - 14}" x2="${cx + 20}" y2="${cy - 14}" class="kn-fl-line"/>
    <line x1="${cx - 20}" y1="${cy + 14}" x2="${cx + 20}" y2="${cy + 14}" class="kn-fl-line"/>
    <path d="M ${cx} ${cy + 16} L ${cx} ${cy - 16} M ${cx - 5} ${cy - 10} L ${cx} ${cy - 16} L ${cx + 5} ${cy - 10}" class="kn-jet-arrow"/>`,
  "airspace-class": (cx, cy) => `
    <path d="${arcPath(cx, cy, 10, 0, 300)}" class="kn-arc kn-arc-green"/>
    <path d="${arcPath(cx, cy, 18, 40, 320)}" class="kn-arc kn-arc-yellow"/>
    <path d="${arcPath(cx, cy, 26, 80, 340)}" class="kn-holding-arrow"/>`,
  notam: (cx, cy) => `
    <path d="M ${cx} ${cy - 18} L ${cx + 16} ${cy + 12} L ${cx - 16} ${cy + 12} Z" class="kn-tc-wing"/>
    <line x1="${cx}" y1="${cy - 8}" x2="${cx}" y2="${cy + 2}" class="kn-vspeed-arrow"/>
    <circle cx="${cx}" cy="${cy + 7}" r="1.6" class="kn-tc-ball"/>`,
  "great-circle": (cx, cy) => `
    <circle cx="${cx}" cy="${cy}" r="18" class="kn-etops-ring"/>
    <path d="M ${cx - 16} ${cy + 6} Q ${cx} ${cy - 18} ${cx + 16} ${cy + 6}" class="kn-jet-ribbon"/>`,
  adsb: (cx, cy) => `
    <circle cx="${cx}" cy="${cy}" r="3" class="kn-etops-plane"/>
    <path d="${arcPath(cx, cy, 12, 200, 340)}" class="kn-wake-spiral"/>
    <path d="${arcPath(cx, cy, 20, 200, 340)}" class="kn-wake-spiral"/>`,
};
const SYSTEMS_DECOR = {
  squawk: (cx, cy) => `
    <rect x="${cx - 24}" y="${cy - 12}" width="48" height="24" rx="3" class="kn-squawk-box"/>
    <text x="${cx}" y="${cy + 6}" class="kn-squawk-text">7700</text>`,
  stall: (cx, cy) => `
    <path d="M ${cx - 24} ${cy + 6} Q ${cx - 6} ${cy - 14} ${cx + 22} ${cy}" class="kn-stall-wing"/>
    <path d="M ${cx - 22} ${cy - 10} Q ${cx - 4} ${cy - 20} ${cx + 18} ${cy - 10}" class="kn-stall-flow"/>
    <path d="M ${cx - 6} ${cy + 2} q 4 6 -2 8 q 6 2 0 8" class="kn-stall-flow-bad"/>`,
  mach: (cx, cy) => `
    <path d="${arcPath(cx, cy, 28, 20, 340)}" class="kn-arc kn-arc-green"/>
    ${needle(cx, cy, 22, 250, "kn-needle kn-needle-short")}
    <circle cx="${cx}" cy="${cy}" r="3" class="kn-g-hub"/>`,
  etops: (cx, cy) => `
    <circle cx="${cx}" cy="${cy}" r="24" class="kn-etops-ring"/>
    <circle cx="${cx - 10}" cy="${cy + 4}" r="5" class="kn-etops-engine"/>
    <circle cx="${cx + 10}" cy="${cy + 4}" r="5" class="kn-etops-engine"/>
    <circle cx="${cx}" cy="${cy - 6}" r="2.5" class="kn-etops-plane"/>`,
  pressurization: (cx, cy) => `
    <path d="${arcPath(cx, cy, 26, 30, 330)}" class="kn-arc kn-arc-green"/>
    ${needle(cx, cy, 20, 200, "kn-needle kn-needle-short")}
    <circle cx="${cx}" cy="${cy}" r="3" class="kn-g-hub"/>`,
  deicing: (cx, cy) => `
    <line x1="${cx - 22}" y1="${cy + 10}" x2="${cx + 22}" y2="${cy + 4}" class="kn-wake-wing"/>
    <path d="M ${cx} ${cy - 18} l 0 16 M ${cx - 8} ${cy - 14} l 16 8 M ${cx + 8} ${cy - 14} l -16 8" class="kn-jet-arrow"/>`,
  apu: (cx, cy) => `
    <circle cx="${cx}" cy="${cy}" r="14" class="kn-etops-ring"/>
    <path d="M ${cx + 3} ${cy - 10} l -8 12 h6 l -3 10 l 9 -13 h-6 z" class="kn-tc-ball"/>`,
  "fuel-dumping": (cx, cy) => `
    <line x1="${cx - 20}" y1="${cy - 14}" x2="${cx + 20}" y2="${cy - 14}" class="kn-wake-wing"/>
    <path d="M ${cx} ${cy - 4} q -7 10 0 18 q 7 -8 0 -18 z" class="kn-shear-arrow"/>`,
  "pitot-static": (cx, cy) => `
    <rect x="${cx - 20}" y="${cy - 4}" width="40" height="8" rx="4" class="kn-squawk-box"/>
    <path d="M ${cx + 18} ${cy} l 10 0 M ${cx + 24} ${cy - 5} l 6 5 l -6 5" class="kn-vspeed-arrow"/>`,
  edto: (cx, cy) => `
    <circle cx="${cx}" cy="${cy}" r="26" class="kn-etops-ring"/>
    <circle cx="${cx - 14}" cy="${cy}" r="4" class="kn-etops-engine"/>
    <circle cx="${cx + 14}" cy="${cy}" r="4" class="kn-etops-engine"/>
    <circle cx="${cx}" cy="${cy}" r="4" class="kn-etops-engine"/>`,
  "fdr-cvr": (cx, cy) => `
    <rect x="${cx - 16}" y="${cy - 10}" width="32" height="22" rx="4" class="kn-squawk-box"/>
    <line x1="${cx}" y1="${cy - 10}" x2="${cx}" y2="${cy - 18}" class="kn-vspeed-arrow"/>
    <circle cx="${cx}" cy="${cy - 20}" r="2" class="kn-tc-ball"/>`,
};
function buildHotspotItem(t, decorFn){
  const cx = 85, cy = 85, r = 42;
  const name = topicName(t.id);
  return `
    <div class="kn-item" data-topic="${t.id}" tabindex="0" role="button" aria-label="${name || t.label}">
      <svg viewBox="0 0 170 170" class="kn-hotspot">
        ${reticle(cx, cy, r)}
        ${decorFn ? decorFn(cx, cy) : ""}
        <text x="${cx}" y="${cy + r + 18}" class="kn-hs-label">${t.label}</text>
      </svg>
      <div class="kn-item-name">${name}</div>
    </div>`;
}
/* ── 連續橫向捲動場景：每個場景一整排項目，內容三倍複製做無限循環捲動，
   原生 CSS scroll-snap 負責觸控滑動與吸附動畫；滑鼠則用簡單拖曳改 scrollLeft。 ── */
const SCENES = {
  instrument: { topics: INSTRUMENT_TOPICS, renderItem: buildGaugeItem },
  runway:     { topics: RUNWAY_TOPICS,     renderItem: t => buildHotspotItem(t, RUNWAY_DECOR[t.id]) },
  nav:        { topics: NAV_TOPICS,        renderItem: t => buildHotspotItem(t, NAV_DECOR[t.id]) },
  systems:    { topics: SYSTEMS_TOPICS,    renderItem: t => buildHotspotItem(t, SYSTEMS_DECOR[t.id]) },
};
function trackEl(key){ return document.querySelector(`[data-track="${key}"]`); }
// 目前置中（最接近視窗中央）的主題 id，用於切換語言重繪後回到原本瀏覽位置
function centeredItemEl(key){
  const track = trackEl(key);
  const centerX = track.clientWidth / 2;
  let best = null, bestDist = Infinity;
  for (const item of track.children){
    const itemCenter = item.offsetLeft - track.scrollLeft + item.offsetWidth / 2;
    const dist = Math.abs(itemCenter - centerX);
    if (dist < bestDist){ bestDist = dist; best = item; }
  }
  return best;
}
function centeredTopicId(key){
  const el = centeredItemEl(key);
  return el ? el.dataset.topic : null;
}
function scrollToTopic(key, id){
  const s = SCENES[key];
  const track = trackEl(key);
  const idx = s.topics.findIndex(t => t.id === id);
  if (idx < 0) return;
  const itemWidth = track.children[0].offsetWidth;   // offsetWidth：不受 coverflow transform:scale 影響的真實版面寬度
  const oneSetWidth = itemWidth * s.topics.length;
  track.style.scrollSnapType = "none";
  track.scrollLeft = oneSetWidth + idx * itemWidth + itemWidth / 2 - track.clientWidth / 2;
  track.style.scrollSnapType = "";
}
// 點旁邊項目時，平滑捲動把它帶到置中。scrollIntoView 在有 scroll-snap-type
// 的容器上，各瀏覽器行為不一致（常常直接被 snap 蓋過、動畫不完整），
// 改成自己算目標位置＋暫時關閉 snap，動畫結束（或逾時保險）再恢復。
function centerItem(key, item){
  const track = trackEl(key);
  const targetLeft = item.offsetLeft + item.offsetWidth / 2 - track.clientWidth / 2;
  track.style.scrollSnapType = "none";
  track.scrollTo({ left: targetLeft, behavior: "smooth" });
  let done = false;
  function finish(){
    if (done) return;
    done = true;
    clearTimeout(fallback);
    track.removeEventListener("scrollend", finish);
    track.style.scrollSnapType = "";
  }
  track.addEventListener("scrollend", finish, { once: true });
  const fallback = setTimeout(finish, 500);
}

// 內容複製三份（前／中／後），一開始捲到中間那份，並讓第一項置中對齊
// （呼應轉盤選取器置中的選取項）；捲動靜止後若落在頭尾複製區，悄悄把
// 捲動位置跳回中間對應處——視覺上完全相同，看起來就是無限循環。
function renderTrack(key){
  const s = SCENES[key];
  const track = trackEl(key);
  const one = s.topics.map(s.renderItem).join("");
  track.innerHTML = one + one + one;
  const oneSetWidth = track.scrollWidth / 3;
  const itemWidth = track.children[0].offsetWidth;   // offsetWidth：不受 coverflow transform:scale 影響的真實版面寬度
  // scroll-snap-type 在場的話，直接設 scrollLeft 常被瀏覽器忽略／吸附掉，
  // 要先暫時關閉才能精準跳到目標位置，設完再恢復。
  track.style.scrollSnapType = "none";
  track.scrollLeft = oneSetWidth + itemWidth / 2 - track.clientWidth / 2;
  track.style.scrollSnapType = "";
  updateCoverflow(key);
}
function wireLoop(key){
  const track = trackEl(key);
  let settleTimer;
  track.addEventListener("scroll", () => {
    clearTimeout(settleTimer);
    settleTimer = setTimeout(() => {
      const oneSetWidth = track.scrollWidth / 3;
      if (track.scrollLeft < oneSetWidth * 0.5 || track.scrollLeft > oneSetWidth * 1.5){
        const delta = track.scrollLeft < oneSetWidth * 0.5 ? oneSetWidth : -oneSetWidth;
        track.style.scrollSnapType = "none";
        track.scrollLeft += delta;
        track.style.scrollSnapType = "";
      }
    }, 120);
  }, { passive: true });
}

/* ── 轉盤風格：置中那項清晰、原尺寸，離中心越遠越縮小越淡，
   隨捲動即時連續變化（不是切到才變），呼應 iOS 選取轉盤的視覺語言。 ── */
function updateCoverflow(key){
  const track = trackEl(key);
  const centerX = track.clientWidth / 2;
  for (const item of track.children){
    const itemCenter = item.offsetLeft - track.scrollLeft + item.offsetWidth / 2;
    const norm = Math.min(1, Math.abs(itemCenter - centerX) / centerX);
    item.style.transform = `scale(${(1 - norm * 0.3).toFixed(3)})`;
    item.style.opacity = (1 - norm * 0.6).toFixed(3);
  }
}
function wireCoverflow(key){
  const track = trackEl(key);
  let ticking = false;
  track.addEventListener("scroll", () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => { ticking = false; updateCoverflow(key); });
  }, { passive: true });
}

/* ── 滑鼠拖曳捲動（觸控／觸控板本身就有原生左右滑動，不需要額外處理）── */
function wireMouseDrag(key){
  const track = trackEl(key);
  let down = false, moved = false, startX = 0, startScroll = 0, pointerId = null;

  track.addEventListener("pointerdown", e => {
    if (e.pointerType !== "mouse") return;
    down = true; moved = false;
    startX = e.clientX; startScroll = track.scrollLeft;
    pointerId = e.pointerId;
    // 注意：這裡刻意不馬上 setPointerCapture——一旦 capture，連後續的 click
    // 事件 target 都會被強制改成 track 本身，導致單純點擊命中不到裡面的項目。
    // 要等 pointermove 真的判斷出是拖曳手勢才補抓，單純點擊完全不會走到這裡。
  });
  track.addEventListener("pointermove", e => {
    if (!down) return;
    const dx = e.clientX - startX;
    if (!moved && Math.abs(dx) > 4){
      moved = true;
      track.setPointerCapture(pointerId);
      track.classList.add("kn-dragging");
    }
    if (moved) track.scrollLeft = startScroll - dx;
  });
  function up(){
    if (!down) return;
    down = false;
    track.classList.remove("kn-dragging");
  }
  track.addEventListener("pointerup", up);
  track.addEventListener("pointercancel", up);
  // 拖曳放開後緊接的 click 視為滑動手勢的一部分，攔截掉避免誤開啟圖示解說
  track.addEventListener("click", e => {
    if (moved){ e.stopPropagation(); e.preventDefault(); moved = false; }
  }, true);
}

/* ── 詳情彈窗 ── */
function openDetail(id){
  const t = mergedTopic(id);
  if (!t) return;
  currentTopicId = id;
  $("kn-view-badge").textContent = t._local ? I18N.t("knowledge.badge.local") : "";
  $("kn-view-badge").hidden = !t._local;
  $("kn-view-name").textContent = F(t.name);
  $("kn-view-summary").textContent = F(t.summary);
  $("kn-view-fact").textContent = F(t.fact) ? `💡 ${F(t.fact)}` : "";
  const imgs = (t.images || []).filter(im => im.src);
  $("kn-view-gallery").innerHTML = imgs.map(im =>
    `<img src="${im.src}" alt="${F(im.caption) || F(t.name)}" loading="lazy">`).join("");
  $("kn-edit").hidden = true;
  $("kn-view").hidden = false;
  $("kn-overlay").hidden = false;
}
function closeDetail(){
  $("kn-overlay").hidden = true;
  currentTopicId = null;
}

/* ── 編輯（本機草稿 / 發布）── */
function openEditor(){
  const t = mergedTopic(currentTopicId);
  $("kn-edit-name").value = F(t.name) || "";
  $("kn-edit-summary").value = F(t.summary) || "";
  $("kn-edit-fact").value = F(t.fact) || "";
  editingImages = (t.images || []).filter(im => im.src).map(im => im.src);
  renderEditingImages();
  $("kn-new-fields").hidden = true;
  $("kn-view").hidden = true;
  $("kn-edit").hidden = false;
}
function closeEditor(){
  $("kn-edit").hidden = true;
  $("kn-view").hidden = false;
  $("kn-new-fields").hidden = true;
  isNewTopic = false;
}

function openNewTopic(sceneKey){
  isNewTopic = true;
  newTopicScene = sceneKey;
  currentTopicId = null;
  editingImages = [];
  $("kn-edit-label").value = "";
  $("kn-edit-name").value = "";
  $("kn-edit-summary").value = "";
  $("kn-edit-fact").value = "";
  $("kn-edit-imgs").innerHTML = "";
  $("kn-edit-scene").value = sceneKey;
  $("kn-new-fields").hidden = false;
  $("kn-view").hidden = true;
  $("kn-edit").hidden = false;
  $("kn-overlay").hidden = false;
}

function addNewTopic(){
  const nameText = $("kn-edit-name").value.trim();
  if (!nameText){ alert("請填入知識名稱"); return null; }
  const sceneKey = $("kn-edit-scene").value || newTopicScene || "instrument";
  const rawLabel = $("kn-edit-label").value.trim().toUpperCase();
  const label = rawLabel || nameText.slice(0, 8).toUpperCase();
  const id = "custom-" + Date.now();
  const lang = I18N.get();
  const topic = {
    id, label, sceneKey,
    category: sceneKey, hotspot: sceneKey,
    name:    { zh: "", en: "", ja: "", [lang]: nameText },
    summary: { zh: "", en: "", ja: "" },
    fact:    { zh: "", en: "", ja: "" },
    images:  editingImages.map(src => ({ src, caption: "" })),
    _custom: true,
  };
  const summaryText = $("kn-edit-summary").value.trim();
  if (summaryText) topic.summary[lang] = summaryText;
  const factText = $("kn-edit-fact").value.trim();
  if (factText) topic.fact[lang] = factText;

  byId[id] = topic;
  TOPICS.push(topic);
  if (SCENES[sceneKey]) SCENES[sceneKey].topics.push({ id, label });

  const customs = loadCustomTopics();
  customs.push(topic);
  saveCustomTopics(customs);

  renderTrack(sceneKey);
  isNewTopic = false;
  currentTopicId = id;
  closeEditor();
  scrollToTopic(sceneKey, id);
  openDetail(id);
  return topic;
}
function renderEditingImages(){
  $("kn-edit-imgs").innerHTML = editingImages.map((src, i) =>
    `<div class="kn-edit-imgitem"><img src="${src}" alt=""><button type="button" data-i="${i}" class="kn-edit-imgdel" title="✕">✕</button></div>`).join("");
  $("kn-edit-imgs").querySelectorAll(".kn-edit-imgdel").forEach(btn =>
    btn.addEventListener("click", () => { editingImages.splice(+btn.dataset.i, 1); renderEditingImages(); }));
}
function buildOverride(){
  const base = byId[currentTopicId];
  const nameText = $("kn-edit-name").value.trim();
  const summaryText = $("kn-edit-summary").value.trim();
  const factText = $("kn-edit-fact").value.trim();
  return {
    name: nameText ? nextFieldValue(base.name, nameText) : base.name,
    summary: summaryText ? nextFieldValue(base.summary, summaryText) : base.summary,
    fact: factText ? nextFieldValue(base.fact, factText) : base.fact,
    images: editingImages.map(src => ({ src, caption: "" })),
  };
}
// 縮圖壓縮後再存，避免 localStorage 塞爆（與 airports.js 相同做法）
function downscaleImg(file, maxW, quality){
  return new Promise(resolve => {
    const img = new Image();
    img.onload = () => {
      const scale = Math.min(1, maxW / img.width);
      const c = document.createElement("canvas");
      c.width = Math.round(img.width * scale);
      c.height = Math.round(img.height * scale);
      c.getContext("2d").drawImage(img, 0, 0, c.width, c.height);
      resolve(c.toDataURL("image/jpeg", quality));
    };
    img.onerror = () => resolve("");
    img.src = URL.createObjectURL(file);
  });
}

async function boot(){
  let data;
  try {
    const res = await fetch("data/knowledge.json?v=118");
    if (!res.ok) throw new Error();
    data = await res.json();
  } catch {
    $("kn-empty").hidden = false;
    I18N.apply();
    return;
  }
  TOPICS = data.topics;
  byId = Object.fromEntries(TOPICS.map(t => [t.id, t]));

  // 合併本機自訂知識條目
  const existingIds = new Set(TOPICS.map(t => t.id));
  loadCustomTopics().forEach(t => {
    if (existingIds.has(t.id)) return;   // 已發布到 server 就不重複加
    byId[t.id] = t;
    TOPICS.push(t);
    if (SCENES[t.sceneKey]) SCENES[t.sceneKey].topics.push({ id: t.id, label: t.label });
  });

  I18N.apply();
  Object.keys(SCENES).forEach(renderTrack);

  // 點置中項目才開解說；點旁邊（未置中）的項目先把它捲到置中，
  // 呼應轉盤選取器「先選中再確認」的手感，也避免手滑點到旁邊卻誤開解說。
  function wireHotspots(key){
    const trackElement = trackEl(key);
    function activate(item){
      // 用主題 id（不是 DOM 節點）比對是否已置中：wireLoop 的無縫跳位可能讓
      // 「置中的那個節點」換成內容三倍複製中的另一份拷貝，但主題其實沒變。
      if (item.dataset.topic === centeredTopicId(key)) openDetail(item.dataset.topic);
      else centerItem(key, item);
    }
    trackElement.addEventListener("click", e => {
      const item = e.target.closest("[data-topic]");
      if (item) activate(item);
    });
    trackElement.addEventListener("keydown", e => {
      if (e.key !== "Enter" && e.key !== " ") return;
      const item = e.target.closest("[data-topic]");
      if (item){ e.preventDefault(); activate(item); }
    });
  }
  Object.keys(SCENES).forEach(key => { wireHotspots(key); wireLoop(key); wireMouseDrag(key); wireCoverflow(key); });

  $("kn-modal-close").addEventListener("click", closeDetail);
  $("kn-overlay").addEventListener("click", e => { if (e.target === $("kn-overlay")) closeDetail(); });
  document.addEventListener("keydown", e => { if (e.key === "Escape" && !$("kn-overlay").hidden) closeDetail(); });

  $("kn-view-edit").addEventListener("click", openEditor);
  $("kn-edit-cancel").addEventListener("click", () => {
    if (isNewTopic){ closeEditor(); $("kn-overlay").hidden = true; }
    else closeEditor();
  });

  $("kn-edit-save").addEventListener("click", () => {
    if (isNewTopic){ addNewTopic(); return; }
    const override = buildOverride();
    saveLocalOverride(currentTopicId, override);
    closeEditor();
    openDetail(currentTopicId);
  });

  $("kn-edit-publish").addEventListener("click", async () => {
    if (isNewTopic){
      const topic = addNewTopic();
      if (!topic) return;
      // 繼續發布到 server
      await requireAuth();
      const btn = $("kn-edit-publish");
      const orig = btn.textContent;
      btn.disabled = true; btn.textContent = I18N.t("knowledge.edit.publishing");
      try {
        const result = await Storage.save("knowledge", { topics: TOPICS.map(t => byId[t.id]) });
        if (result.ok){
          // 發布成功後清除本機自訂（已進入 server 資料）
          saveCustomTopics(loadCustomTopics().filter(c => c.id !== topic.id));
          delete byId[topic.id]._custom;
        }
        alert(result.message);
      } catch { alert(I18N.t("knowledge.edit.savefail")); }
      finally { btn.disabled = false; btn.textContent = orig; }
      return;
    }
    const hasAny = $("kn-edit-name").value.trim() || $("kn-edit-summary").value.trim() || editingImages.length;
    if (!hasAny){ alert(I18N.t("knowledge.edit.empty")); return; }
    await requireAuth();
    const btn = $("kn-edit-publish");
    const orig = btn.textContent;
    btn.disabled = true;
    btn.textContent = I18N.t("knowledge.edit.publishing");
    try {
      const override = buildOverride();
      saveLocalOverride(currentTopicId, override);
      byId[currentTopicId] = { ...byId[currentTopicId], ...override };
      const result = await Storage.save("knowledge", { topics: TOPICS.map(t => byId[t.id]) });
      alert(result.message);
    } catch {
      alert(I18N.t("knowledge.edit.savefail"));
    } finally {
      btn.disabled = false;
      btn.textContent = orig;
    }
    closeEditor();
    openDetail(currentTopicId);
  });

  document.addEventListener("click", e => {
    const btn = e.target.closest(".kn-add-btn");
    if (btn) openNewTopic(btn.dataset.scene);
  });

  $("kn-edit-imgadd").addEventListener("click", () => {
    const input = $("kn-edit-imgurl");
    const url = input.value.trim();
    if (!url) return;
    editingImages.push(url);
    input.value = "";
    renderEditingImages();
  });
  $("kn-edit-imgfile").addEventListener("click", () => $("kn-edit-file").click());
  $("kn-edit-file").addEventListener("change", async e => {
    for (const file of e.target.files){
      const dataUrl = await downscaleImg(file, 1200, 0.8);
      if (dataUrl) editingImages.push(dataUrl);
    }
    renderEditingImages();
    e.target.value = "";
  });

  $("btn-theme").addEventListener("click", () => window.HangarTheme.toggle());
  I18N.mountSelector($("btn-lang"));
  document.addEventListener("langchange", () => {
    I18N.apply();
    Object.keys(SCENES).forEach(key => {
      const centered = centeredTopicId(key);
      renderTrack(key);
      if (centered) scrollToTopic(key, centered);
    });
    if (currentTopicId && !$("kn-overlay").hidden) openDetail(currentTopicId);
  });
}
boot();
