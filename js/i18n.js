"use strict";
/* ═══════════════════════════════════════════════
   多語言 i18n（繁體中文 / English / 日本語）
   - 介面文字：完整翻譯
   - 內容文字（機型資料）：支援多語言物件，未填語言回退繁中
   偏好存 localStorage，切換即時更新標記 data-lang 的元素
   ═══════════════════════════════════════════════ */

const I18N_STRINGS = {
  "zh": {
    // 通用
    "fleet.back": "← FLEET / 機隊列表",
    "brand.eyebrow": "HANGAR ARCHIVE / 機庫檔案",
    // 列表頁
    "fleet.title": "機隊總覽",
    "fleet.sub": "FLEET INDEX — 點選機型進入 3D 互動檢視",
    "fleet.search": "搜尋機型 / 廠商…",
    "fleet.compare": "⇄ 比較",
    "fleet.edit": "✎ 編輯資料",
    "fleet.spec.first": "首飛",
    "fleet.spec.span": "翼展",
    "fleet.spec.seats": "座位",
    "fleet.foot": "3D MODELS: Flightradar24 / fr24-3d-models (GPL-2.0)",
    // 檢視器
    "viewer.hint.drag": "拖曳 — 旋轉視角",
    "viewer.hint.zoom": "滾輪 / 雙指 — 縮放",
    "viewer.hint.click": "點擊部位 — 開啟解說",
    "viewer.rotate": "自動旋轉",
    "viewer.reset": "重置視角",
    "viewer.hotspots": "標註點",
    "viewer.theme": "切換主題",
    "viewer.specs": "☰ 規格",
    "viewer.compare": "⇄ 比較",
    "viewer.component": "COMPONENT",
    "viewer.spectitle": "SPECIFICATIONS / 規格",
    "viewer.fact": "DID YOU KNOW / 冷知識",
    "viewer.fullspec": "詳細規格",
    "viewer.loading": "正在載入機體幾何與部位資料……",
    "viewer.spec.empty": "此機型尚未填入詳細規格。可在編輯器中補充。",
    // 比較頁
    "compare.title": "並排比較規格",
    "compare.add": "＋ 加入機型",
    "compare.remove": "移除",
    "compare.empty": "請於上方選擇至少一架機型開始比較。",
    "compare.basic": "基本資訊",
    "compare.mfr": "製造商",
    "compare.category": "類別",
    "compare.firstflight": "首飛年份",
    "compare.seats": "典型座位",
    // 編輯器
    "editor.eyebrow": "DATA EDITOR / 資料編輯器",
    "editor.preview": "預覽",
    "editor.save": "儲存",
    "editor.savegithub": "儲存到 GitHub",
    "editor.exportjson": "匯出 JSON",
  },
  "en": {
    "fleet.back": "← FLEET",
    "brand.eyebrow": "HANGAR ARCHIVE",
    "fleet.title": "Fleet Overview",
    "fleet.sub": "FLEET INDEX — tap an aircraft for 3D interactive view",
    "fleet.search": "Search aircraft / manufacturer…",
    "fleet.compare": "⇄ Compare",
    "fleet.edit": "✎ Edit",
    "fleet.spec.first": "First flight",
    "fleet.spec.span": "Wingspan",
    "fleet.spec.seats": "Seats",
    "fleet.foot": "3D MODELS: Flightradar24 / fr24-3d-models (GPL-2.0)",
    "viewer.hint.drag": "Drag — rotate view",
    "viewer.hint.zoom": "Scroll / pinch — zoom",
    "viewer.hint.click": "Click a part — open info",
    "viewer.rotate": "Auto-rotate",
    "viewer.reset": "Reset view",
    "viewer.hotspots": "Hotspots",
    "viewer.theme": "Toggle theme",
    "viewer.specs": "☰ Specs",
    "viewer.compare": "⇄ Compare",
    "viewer.component": "COMPONENT",
    "viewer.spectitle": "SPECIFICATIONS",
    "viewer.fact": "DID YOU KNOW",
    "viewer.fullspec": "Full Specifications",
    "viewer.loading": "Loading airframe geometry and part data…",
    "viewer.spec.empty": "No detailed specifications yet. Add them in the editor.",
    "compare.title": "Compare Specifications",
    "compare.add": "＋ Add aircraft",
    "compare.remove": "Remove",
    "compare.empty": "Select at least one aircraft above to compare.",
    "compare.basic": "Basic Info",
    "compare.mfr": "Manufacturer",
    "compare.category": "Category",
    "compare.firstflight": "First flight",
    "compare.seats": "Typical seats",
    "editor.eyebrow": "DATA EDITOR",
    "editor.preview": "Preview",
    "editor.save": "Save",
    "editor.savegithub": "Save to GitHub",
    "editor.exportjson": "Export JSON",
  },
  "ja": {
    "fleet.back": "← 機体一覧",
    "brand.eyebrow": "ハンガーアーカイブ",
    "fleet.title": "機体一覧",
    "fleet.sub": "FLEET INDEX — 機種をタップして3Dビューへ",
    "fleet.search": "機種・メーカーを検索…",
    "fleet.compare": "⇄ 比較",
    "fleet.edit": "✎ 編集",
    "fleet.spec.first": "初飛行",
    "fleet.spec.span": "全幅",
    "fleet.spec.seats": "座席数",
    "fleet.foot": "3D MODELS: Flightradar24 / fr24-3d-models (GPL-2.0)",
    "viewer.hint.drag": "ドラッグ — 視点回転",
    "viewer.hint.zoom": "スクロール / ピンチ — ズーム",
    "viewer.hint.click": "部位をクリック — 解説を表示",
    "viewer.rotate": "自動回転",
    "viewer.reset": "視点リセット",
    "viewer.hotspots": "注釈点",
    "viewer.theme": "テーマ切替",
    "viewer.specs": "☰ 諸元",
    "viewer.compare": "⇄ 比較",
    "viewer.component": "COMPONENT",
    "viewer.spectitle": "SPECIFICATIONS / 諸元",
    "viewer.fact": "DID YOU KNOW / 豆知識",
    "viewer.fullspec": "詳細諸元",
    "viewer.loading": "機体形状と部位データを読み込み中……",
    "viewer.spec.empty": "詳細諸元は未登録です。エディタで追加できます。",
    "compare.title": "諸元を並べて比較",
    "compare.add": "＋ 機種を追加",
    "compare.remove": "削除",
    "compare.empty": "上部で機種を1つ以上選んでください。",
    "compare.basic": "基本情報",
    "compare.mfr": "メーカー",
    "compare.category": "カテゴリー",
    "compare.firstflight": "初飛行年",
    "compare.seats": "標準座席数",
    "editor.eyebrow": "DATA EDITOR / データエディタ",
    "editor.preview": "プレビュー",
    "editor.save": "保存",
    "editor.savegithub": "GitHubに保存",
    "editor.exportjson": "JSONを書き出し",
  },
};

const I18N = (() => {
  const KEY = "hangar_lang";
  const SUPPORTED = ["zh", "en", "ja"];
  const LANG_NAMES = { zh: "繁中", en: "EN", ja: "日本語" };

  function detect(){
    const saved = localStorage.getItem(KEY);
    if (saved && SUPPORTED.includes(saved)) return saved;
    const nav = (navigator.language || "zh").toLowerCase();
    if (nav.startsWith("ja")) return "ja";
    if (nav.startsWith("en")) return "en";
    return "zh";   // 預設繁中
  }

  let current = detect();

  // 介面字串翻譯（找不到 key 回退繁中，再回退 key 本身）
  function t(key){
    return (I18N_STRINGS[current] && I18N_STRINGS[current][key])
        || I18N_STRINGS.zh[key] || key;
  }

  // 內容欄位取值：支援字串（舊資料）或 {zh,en,ja} 物件，未填語言回退繁中
  function field(val){
    if (val == null) return "";
    if (typeof val === "string") return val;          // 舊格式：純繁中字串
    return val[current] || val.zh || val.en || val.ja || "";
  }

  function get(){ return current; }
  function set(lang){
    if (!SUPPORTED.includes(lang)) return;
    current = lang;
    localStorage.setItem(KEY, lang);
    document.documentElement.setAttribute("lang", lang === "zh" ? "zh-Hant" : lang);
    apply();
    document.dispatchEvent(new CustomEvent("langchange", { detail: lang }));
  }
  function cycle(){
    const i = SUPPORTED.indexOf(current);
    set(SUPPORTED[(i + 1) % SUPPORTED.length]);
    return current;
  }

  // 套用 data-i18n 屬性的元素
  function apply(){
    document.querySelectorAll("[data-i18n]").forEach(el => {
      el.textContent = t(el.getAttribute("data-i18n"));
    });
    document.querySelectorAll("[data-i18n-ph]").forEach(el => {
      el.setAttribute("placeholder", t(el.getAttribute("data-i18n-ph")));
    });
    document.querySelectorAll("[data-i18n-title]").forEach(el => {
      el.setAttribute("title", t(el.getAttribute("data-i18n-title")));
    });
  }

  return { t, field, get, set, cycle, apply, SUPPORTED, LANG_NAMES };
})();

// 初始化語言標記
document.documentElement.setAttribute("lang", I18N.get() === "zh" ? "zh-Hant" : I18N.get());
