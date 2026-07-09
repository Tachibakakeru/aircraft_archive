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
    // 補充：完整頁面翻譯
    "compare.eyebrow": "COMPARE / 機型比較",
    "fleet.edit.title": "編輯",
    "fleet.foot.line2": "新增機型流程請見 README.md — convert_fr24.py 轉換 → 撰寫 data JSON → 註冊至 fleet.json",
    "fleet.error": "無法載入機隊資料（<code>data/fleet.json</code>）。<br>若你是直接雙擊開啟 HTML 檔案（<code>file://</code>），瀏覽器會阻擋資料讀取，請在專案資料夾啟動本機伺服器後再開啟：<br><code>python3 -m http.server 8000</code> → 瀏覽 <code>http://localhost:8000</code>",
    "viewer.chips.aria": "部位快選",
    "viewer.panel.close": "關閉面板",
    "viewer.spec.close": "關閉規格",
    "ui.totop": "回到頂端",
    "fleet.filter.all": "所有類別",
    "fleet.sort.label": "排序方式",
    "fleet.sort.name": "名稱",
    "fleet.sort.first": "首飛年份",
    "fleet.sort.seats": "座位數",
    "fleet.sort.span": "翼展",
    "viewer.keys.title": "鍵盤快捷鍵",
    "viewer.keys.parts": "切換部位",
    "viewer.keys.close": "關閉面板",
    "viewer.keys.rotate": "自動旋轉",
    "viewer.keys.reset": "重置視角",
    "viewer.keys.specs": "詳細規格",
    "viewer.keys.help": "顯示／隱藏本表",
    "viewer.units": "單位",
    "compare.difftoggle": "只顯示差異",
    "lang.name": "繁體中文",
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
    "compare.eyebrow": "COMPARE",
    "fleet.edit.title": "Edit",
    "fleet.foot.line2": "To add an aircraft, see README.md — convert with convert_fr24.py → write the data JSON → register it in fleet.json",
    "fleet.error": "Could not load fleet data (<code>data/fleet.json</code>).<br>If you opened the HTML file directly (<code>file://</code>), the browser blocks data access. Start a local server in the project folder first:<br><code>python3 -m http.server 8000</code> → open <code>http://localhost:8000</code>",
    "viewer.chips.aria": "Quick part select",
    "viewer.panel.close": "Close panel",
    "viewer.spec.close": "Close specifications",
    "ui.totop": "Back to top",
    "fleet.filter.all": "All categories",
    "fleet.sort.label": "Sort by",
    "fleet.sort.name": "Name",
    "fleet.sort.first": "First flight",
    "fleet.sort.seats": "Seats",
    "fleet.sort.span": "Wingspan",
    "viewer.keys.title": "Keyboard shortcuts",
    "viewer.keys.parts": "Switch part",
    "viewer.keys.close": "Close panel",
    "viewer.keys.rotate": "Auto-rotate",
    "viewer.keys.reset": "Reset view",
    "viewer.keys.specs": "Specifications",
    "viewer.keys.help": "Show / hide this list",
    "viewer.units": "Units",
    "compare.difftoggle": "Differences only",
    "lang.name": "English",
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
    "compare.eyebrow": "COMPARE / 機種比較",
    "fleet.edit.title": "編集",
    "fleet.foot.line2": "機種追加は README.md を参照 — convert_fr24.py で変換 → data JSON を作成 → fleet.json に登録",
    "fleet.error": "機体データを読み込めません（<code>data/fleet.json</code>）。<br>HTML ファイルを直接開いた場合（<code>file://</code>）、ブラウザがデータ読み込みをブロックします。プロジェクトフォルダでローカルサーバーを起動してください：<br><code>python3 -m http.server 8000</code> → <code>http://localhost:8000</code> を開く",
    "viewer.chips.aria": "部位クイック選択",
    "viewer.panel.close": "パネルを閉じる",
    "viewer.spec.close": "諸元を閉じる",
    "ui.totop": "トップへ戻る",
    "fleet.filter.all": "すべての分類",
    "fleet.sort.label": "並び替え",
    "fleet.sort.name": "名前",
    "fleet.sort.first": "初飛行",
    "fleet.sort.seats": "座席数",
    "fleet.sort.span": "全幅",
    "viewer.keys.title": "キーボードショートカット",
    "viewer.keys.parts": "部位切替",
    "viewer.keys.close": "パネルを閉じる",
    "viewer.keys.rotate": "自動回転",
    "viewer.keys.reset": "視点リセット",
    "viewer.keys.specs": "詳細諸元",
    "viewer.keys.help": "この表を表示／非表示",
    "viewer.units": "単位",
    "compare.difftoggle": "差異のみ表示",
    "lang.name": "日本語",
  },
};

/* ── 詳細規格：分類與欄位名稱翻譯（值仍為內容資料，回退繁中） ── */
const SPEC_LABELS = {
  // 分類
  "機組員與載客": { en:"Crew & Capacity", ja:"乗員・座席" },
  "尺寸": { en:"Dimensions", ja:"寸法" },
  "重量": { en:"Weights", ja:"重量" },
  "容量": { en:"Capacity", ja:"容量" },
  "性能": { en:"Performance", ja:"性能" },
  "發動機": { en:"Powerplant", ja:"エンジン" },
  // 機組員與載客
  "駕駛艙機組員": { en:"Flight crew", ja:"運航乗員" },
  "典型載客量": { en:"Typical seating", ja:"標準座席数" },
  "最大載客量": { en:"Max seating", ja:"最大座席数" },
  "座位配置": { en:"Seating layout", ja:"座席配置" },
  "座位間距": { en:"Seat pitch", ja:"シートピッチ" },
  "用途": { en:"Role", ja:"用途" },
  "座艙": { en:"Cabin", ja:"キャビン" },
  "外掛酬載": { en:"External payload", ja:"外部搭載量" },
  "機組員": { en:"Crew", ja:"乗員" },
  "結構": { en:"Structure", ja:"構造" },
  "首飛年份": { en:"First flight", ja:"初飛行" },
  "基礎機型": { en:"Base type", ja:"ベース機体" },
  "客艙高度": { en:"Cabin height", ja:"キャビン高さ" },
  "旋翼型式": { en:"Rotor type", ja:"ローター形式" },
  "尾旋翼": { en:"Tail rotor", ja:"テールローター" },
  "進出方式": { en:"Access", ja:"乗降方式" },
  // 尺寸
  "全長": { en:"Length", ja:"全長" },
  "翼展": { en:"Wingspan", ja:"全幅" },
  "機高": { en:"Height", ja:"全高" },
  "機身寬度": { en:"Fuselage width", ja:"胴体幅" },
  "客艙寬度": { en:"Cabin width", ja:"キャビン幅" },
  "翼面積": { en:"Wing area", ja:"主翼面積" },
  "後掠角": { en:"Sweep angle", ja:"後退角" },
  "展弦比": { en:"Aspect ratio", ja:"アスペクト比" },
  "貨艙長度": { en:"Hold length", ja:"貨物室長さ" },
  "貨艙寬度": { en:"Hold width", ja:"貨物室幅" },
  "貨艙直徑": { en:"Hold diameter", ja:"貨物室直径" },
  "機身最大寬度": { en:"Max fuselage width", ja:"胴体最大幅" },
  "客艙長度": { en:"Cabin length", ja:"キャビン長さ" },
  "機身長度": { en:"Fuselage length", ja:"胴体長さ" },
  "主旋翼直徑": { en:"Main rotor diameter", ja:"メインローター直径" },
  "旋翼盤面積": { en:"Rotor disc area", ja:"ローター円板面積" },
  "尾旋翼直徑": { en:"Tail rotor diameter", ja:"テールローター直径" },
  // 重量
  "空重（OEW）": { en:"Empty weight (OEW)", ja:"空虚重量 (OEW)" },
  "最大起飛重量（MTOW）": { en:"Max takeoff (MTOW)", ja:"最大離陸重量 (MTOW)" },
  "最大落地重量（MLW）": { en:"Max landing (MLW)", ja:"最大着陸重量 (MLW)" },
  "最大零燃油重量（MZFW）": { en:"Max zero-fuel (MZFW)", ja:"最大無燃料重量 (MZFW)" },
  "最大酬載": { en:"Max payload", ja:"最大ペイロード" },
  "空重": { en:"Empty weight", ja:"空虚重量" },
  "最大水袋壓艙": { en:"Max water ballast", ja:"最大ウォーターバラスト" },
  "最大吊掛重量": { en:"Max sling load", ja:"最大吊下げ重量" },
  // 容量
  "貨艙容積": { en:"Cargo volume", ja:"貨物室容積" },
  "油箱容量": { en:"Fuel capacity", ja:"燃料容量" },
  "行李容積": { en:"Baggage volume", ja:"手荷物容積" },
  "行李／載重": { en:"Baggage / load", ja:"手荷物・搭載" },
  "客艙容積": { en:"Cabin volume", ja:"キャビン容積" },
  // 性能
  "巡航速度": { en:"Cruise speed", ja:"巡航速度" },
  "最大操作速度（MMO）": { en:"Max operating (MMO)", ja:"最大運用速度 (MMO)" },
  "最大操作速度（VMO）": { en:"Max operating (VMO)", ja:"最大運用速度 (VMO)" },
  "飛行距離（滿載）": { en:"Range (full load)", ja:"航続距離 (満載)" },
  "飛行高度上限": { en:"Service ceiling", ja:"実用上昇限度" },
  "起飛所需跑道長度": { en:"Takeoff distance", ja:"離陸滑走路長" },
  "降落所需跑道長度": { en:"Landing distance", ja:"着陸滑走路長" },
  "爬升率": { en:"Climb rate", ja:"上昇率" },
  "最佳滑翔比": { en:"Best glide ratio", ja:"最良滑空比" },
  "最小下沉率": { en:"Min sink rate", ja:"最小沈下率" },
  "最大速度（VNE）": { en:"Never-exceed (VNE)", ja:"超過禁止速度 (VNE)" },
  "失速速度": { en:"Stall speed", ja:"失速速度" },
  "最大機動速度": { en:"Maneuvering speed", ja:"運動速度" },
  // 發動機
  "型號": { en:"Model", ja:"型式" },
  "型式": { en:"Type", ja:"形式" },
  "單具推力": { en:"Thrust (each)", ja:"推力 (1基)" },
  "旁通比": { en:"Bypass ratio", ja:"バイパス比" },
  "風扇直徑": { en:"Fan diameter", ja:"ファン直径" },
  "單具功率": { en:"Power (each)", ja:"出力 (1基)" },
  "螺旋槳": { en:"Propeller", ja:"プロペラ" },
  "螺旋槳直徑": { en:"Propeller diameter", ja:"プロペラ直径" },
  "起飛方式": { en:"Launch method", ja:"発航方式" },
  "特技能力": { en:"Aerobatic capability", ja:"曲技能力" },
  "備註": { en:"Notes", ja:"備考" },
  "傳動": { en:"Transmission", ja:"トランスミッション" },
  "主旋翼轉速": { en:"Main rotor RPM", ja:"メインローター回転数" },
  // 部位名稱（3D 部位面板／快選）
  "機身": { en:"Fuselage", ja:"胴体" },
  "駕駛艙": { en:"Cockpit", ja:"コックピット" },
  "主翼": { en:"Main wing", ja:"主翼" },
  "引擎": { en:"Engine", ja:"エンジン" },
  "垂直尾翼": { en:"Vertical stabilizer", ja:"垂直尾翼" },
  "水平尾翼": { en:"Horizontal stabilizer", ja:"水平尾翼" },
  "起落架": { en:"Landing gear", ja:"降着装置" },
  // 部位規格欄位
  "操縱面": { en:"Control surface", ja:"操縦翼面" },
  "功能": { en:"Function", ja:"機能" },
  "結構形式": { en:"Structure type", ja:"構造形式" },
  "主要材料": { en:"Primary material", ja:"主要材料" },
  "翼內": { en:"Inside wing", ja:"翼内" },
  "配置": { en:"Configuration", ja:"配置" },
  "機組": { en:"Crew", ja:"乗員" },
  "全機高度": { en:"Overall height", ja:"全高" },
  "主起落架": { en:"Main gear", ja:"主脚" },
  "前起落架": { en:"Nose gear", ja:"前脚" },
  "最大起飛重量": { en:"Max takeoff weight", ja:"最大離陸重量" },
  "特徵": { en:"Feature", ja:"特徴" },
  "機身直徑": { en:"Fuselage diameter", ja:"胴体直径" },
  "典型座位數": { en:"Typical seats", ja:"標準座席数" },
  "飛控": { en:"Flight control", ja:"飛行制御" },
  "操縱": { en:"Controls", ja:"操縦" },
  "儀表": { en:"Instruments", ja:"計器" },
  "材料": { en:"Material", ja:"材料" },
  "配平": { en:"Trim", ja:"トリム" },
  "尾翼翼展": { en:"Tail span", ja:"尾翼スパン" },
  "構型": { en:"Configuration", ja:"構成" },
  "煞車": { en:"Brakes", ja:"ブレーキ" },
  "產量": { en:"Production", ja:"生産数" },
  "引擎數": { en:"Engine count", ja:"エンジン数" },
  "總推力": { en:"Total thrust", ja:"総推力" },
  "總機輪數": { en:"Total wheels", ja:"総車輪数" },
  "位置": { en:"Position", ja:"位置" },
};

/* ── 詳細規格「數值」中的中文註記翻譯（依長度由長至短替換） ── */
const VALUE_PHRASES = [
  // 引擎型式
  ["齒輪傳動高旁通比渦輪扇", "geared high-bypass turbofan", "ギヤード高バイパスターボファン"],
  ["高旁通比渦輪扇", "high-bypass turbofan", "高バイパスターボファン"],
  ["中旁通比渦輪扇", "medium-bypass turbofan", "中バイパスターボファン"],
  ["四缸水平對臥活塞發動機", "4-cyl horizontally-opposed piston", "水平対向4気筒ピストン"],
  ["渦輪軸發動機", "turboshaft engine", "ターボシャフトエンジン"],
  ["渦輪螺旋槳", "turboprop", "ターボプロップ"],
  ["渦輪軸", "turboshaft", "ターボシャフト"],
  ["活塞", "piston", "ピストン"],
  // 用途／機種
  ["超重型戰略運輸機", "super-heavy strategic airlifter", "超大型戦略輸送機"],
  ["超大件貨物運輸", "outsize cargo transport", "大型貨物輸送"],
  ["中型公務噴射機", "midsize business jet", "中型ビジネスジェット"],
  ["中型雙發直升機", "medium twin-engine helicopter", "中型双発ヘリコプター"],
  ["特技教練滑翔機", "aerobatic training glider", "曲技練習グライダー"],
  ["單發活塞教練", "single-engine piston trainer", "単発ピストン練習機"],
  ["通用航空機", "general-aviation aircraft", "ジェネラルアビエーション機"],
  ["教練滑翔機", "training glider", "練習グライダー"],
  ["純滑翔機", "pure glider", "純グライダー"],
  // 座艙／構型
  ["面對面俱樂部式", "face-to-face club seating", "対面クラブ配置"],
  ["玻璃纖維複合材料", "fiberglass composite", "グラスファイバー複合材"],
  ["並列雙座", "side-by-side two seats", "横並び複座"],
  ["後排雙座", "rear two seats", "後席2席"],
  ["雙座配置", "two-seat configuration", "複座構成"],
  ["右側單門", "single door (right side)", "右側シングルドア"],
  ["雙座", "two-seat", "複座"],
  // 旋翼／機翼
  ["葉全鉸接主旋翼", "-blade fully-articulated main rotor", "枚全関節式メインローター"],
  ["含鯊鰭小翼", "with sharklets", "シャークレット付き"],
  ["含翼尖帆片", "with wingtip fences", "ウィングチップフェンス付き"],
  ["含小翼", "with winglets", "ウィングレット付き"],
  ["後掠上單翼", "swept high-wing", "後退高翼"],
  ["平直下單翼", "straight low-wing", "直線低翼"],
  ["平直翼", "straight wing", "直線翼"],
  ["含旋翼", "incl. rotor", "ローター含む"],
  // 載客／艙等
  ["單一經濟艙", "single-class economy", "モノクラス"],
  ["兩艙等級", "2-class", "2クラス"],
  ["三艙等級", "3-class", "3クラス"],
  ["名乘客", " passengers", "名の乗客"],
  ["六排並列", "6-abreast", "6列配置"],
  ["七排並列", "7-abreast", "7列配置"],
  ["八排並列", "8-abreast", "8列配置"],
  ["九排並列", "9-abreast", "9列配置"],
  ["五排並列", "5-abreast", "5列配置"],
  ["四排並列", "4-abreast", "4列配置"],
  // 甲板／位置
  ["主艙", "main deck", "メインデッキ"],
  ["上艙", "upper deck", "アッパーデッキ"],
  ["機艙內", "internal", "機内"],
  ["機背", "on top of fuselage", "胴体上"],
  // 滑翔／操作
  ["部分機型可加裝自力起飛動力套件", "some variants accept a self-launch kit", "一部機体はセルフローンチキット装着可"],
  ["可執行基本特技飛行", "basic aerobatics capable", "基本曲技飛行が可能"],
  ["可加裝壓艙水袋", "water ballast optional", "ウォーターバラスト装着可"],
  ["飛機拖曳", "aerotow", "航空機曳航"],
  ["降落滑跑", "landing roll", "着陸滑走"],
  ["絞盤", "winch", "ウインチ"],
  ["草地", "grass", "草地"],
  // b738 起降條件
  ["安全起飛長度", "safe takeoff length", "安全離陸長"],
  ["安全降落長度", "safe landing length", "安全着陸長"],
  ["標準條件", " conditions", "標準条件"],
  ["襟翼", "flaps ", "フラップ"],
  ["推力", " thrust", "推力"],
  // 動力／傳動
  ["雙發雙冗餘", "twin-engine redundant", "双発冗長"],
  ["雙發", "twin-engine", "双発"],
  ["雙葉定速", "two-blade constant-speed", "2枚定速"],
  ["六葉", "6-blade", "6枚"],
  // 其他
  ["垂直降落", "vertical landing", "垂直着陸"],
  ["不需跑道", "no runway required", "滑走路不要"],
  ["代表型", "representative:", "代表型:"],
  ["衍生", "derivative", "派生"],
  ["含燃油", "incl. fuel", "燃料込み"],
  ["燃油", "fuel", "燃料"],
  ["空載", "empty", "空虚"],
  ["滿載", "full load", "満載"],
  ["貨機", "freighter", "貨物機"],
  ["貨運", "cargo", "貨物"],
  ["不適用", "N/A", "該当なし"],
  ["無動力", "unpowered", "無動力"],
  ["無發動機", "no engine", "エンジンなし"],
  ["外掛", "external", "外部搭載"],
  ["初級", "basic", "初級"],
  ["最多", "up to", "最大"],
  ["海平面", "sea level", "海面高度"],
  ["約", "approx. ", "約"],
  ["吋", "in", "インチ"],
  ["共", "total", "計"],
  ["座", " seats", "席"],
  ["在", "at", "＠"],
  ["名", "", "名"],
  ["人", "", "人"],
  ["葉", "-blade", "枚"],
  ["無", "none", "なし"],
  // 副標題（機種類別 + 提示語）
  ["點擊機體部位查看解說", "click a part for details", "部位をクリックで解説"],
  ["史上最大的飛機", "the largest aircraft ever", "史上最大の航空機"],
  ["窄體客機", "Narrow-body airliner", "ナローボディ旅客機"],
  ["廣體客機", "Wide-body airliner", "ワイドボディ旅客機"],
  ["區域客機", "Regional airliner", "リージョナル旅客機"],
  ["公務機", "Business jet", "ビジネスジェット"],
  ["旋翼機", "Rotorcraft", "回転翼機"],
  ["通用航空", "General aviation", "ジェネラルアビエーション"],
  ["滑翔機", "Glider", "グライダー"],
  ["直升機", "Helicopter", "ヘリコプター"],
  // 部位規格數值
  ["半硬殼式鋁合金", "semi-monocoque aluminum alloy", "セミモノコック・アルミ合金"],
  ["渦輪螺旋槳引擎", "turboprop engine", "ターボプロップエンジン"],
  ["渦輪扇引擎", "turbofan engine", "ターボファンエンジン"],
  ["碳纖維複合材料", "carbon-fiber composite", "炭素繊維複合材"],
  ["數位線傳飛控", "digital fly-by-wire", "デジタルフライバイワイヤ"],
  ["螺桿式全動安定面", "jackscrew all-moving stabilizer", "ジャッキスクリュー式全遊動水平尾翼"],
  ["全動式安定面", "all-moving stabilizer", "全遊動安定板"],
  ["偏航穩定與操縱", "yaw stability & control", "ヨー安定と操縦"],
  ["主輪外露無艙門", "exposed main wheels (no doors)", "主脚露出（扉なし）"],
  ["含背鰭延伸段", "with dorsal fin extension", "ドーサルフィン延長付き"],
  ["可跪姿裝卸貨", "kneeling for cargo loading", "ニーリング荷役対応"],
  ["翼尖擋板構型", "wingtip-fence configuration", "ウイングチップフェンス構成"],
  ["碳纖維多盤式", "carbon multi-disc", "カーボン多板式"],
  ["具液晶顯示器", " LCD displays", " 基の液晶ディスプレイ"],
  ["具整合顯示器", " integrated displays", " 基の統合ディスプレイ"],
  ["型尾翼橫樑", "-type tail beam", "型尾翼ビーム"],
  ["傳統駕駛盤", "conventional yoke", "従来型操縦輪"],
  ["液壓助力", "hydraulic-assisted", "油圧アシスト"],
  ["鋼纜備援", "cable backup", "ケーブルバックアップ"],
  ["俯仰穩定", "pitch stability", "ピッチ安定"],
  ["偏航穩定", "yaw stability", "ヨー安定"],
  ["機尾低置", "low-set tail", "低尾翼配置"],
  ["產生升力", "generates lift", "揚力を発生"],
  ["半硬殼式", "semi-monocoque", "セミモノコック"],
  ["複合材料", "composite", "複合材"],
  ["鋁合金", "aluminum alloy", "アルミ合金"],
  ["主油箱", "main fuel tank", "主燃料タンク"],
  ["前三點式", "tricycle", "前輪式"],
  ["名飛行員", " pilots", "名のパイロット"],
  ["方向舵", "rudder", "ラダー"],
  ["升降舵", "elevator", "エレベーター"],
  ["側桿", "sidestick", "サイドスティック"],
  ["雙垂尾", "twin vertical tail", "双垂直尾翼"],
  ["含背鰭", "with dorsal fin", "ドーサルフィン付き"],
  ["席", " seats", "席"],
  ["輪", " wheels", "輪"],
  ["具", "", " 基"],
  ["架", "", " 機"],
  ["僅", "only ", "のみ "],
  ["至", "–", "～"],
];
const VALUE_PHRASES_SORTED = VALUE_PHRASES.slice().sort((a, b) => b[0].length - a[0].length);

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

  // 詳細規格分類／欄位名稱翻譯（繁中或查無對照時回傳原字串）
  function spec(label){
    if (current === "zh") return label;
    const e = SPEC_LABELS[label];
    return (e && e[current]) || label;
  }

  // 單位模式：both（雙單位）/ metric（公制）/ imperial（英制）
  const UKEY = "hangar_unit";
  let unit = localStorage.getItem(UKEY) || "both";
  const IMP_RE = /\b(ft|in|lb|lbf|nmi|mph|kt|gal|shp|hp)\b|ft²|ft³|°F|US gal/;
  const MET_RE = /\b(mm|cm|km|kg|km\/h|m\/s|m²|m³|kN|kW|rpm|m|t|L|°C)\b/;

  function applyUnits(s){
    if (unit === "both") return s;
    const m = s.match(/^(.*?)\s*[（(]([^（()）]*)[)）]\s*$/);
    if (!m) return s;
    const head = m[1].trim(), inner = m[2].trim();
    if (IMP_RE.test(inner) && MET_RE.test(head))
      return unit === "imperial" ? inner : head;
    return s;
  }

  // 詳細規格「數值」翻譯：替換中文註記並套用單位模式
  function specValue(v){
    if (typeof v !== "string") return v;
    let s = v.replace(/ｍ/g, "m");   // 正規化全形公尺
    if (current !== "zh"){
      const idx = current === "en" ? 1 : 2;
      for (const p of VALUE_PHRASES_SORTED) s = s.split(p[0]).join(p[idx]);
      if (current === "en"){
        s = s.replace(/（/g, " (").replace(/）/g, ")")
             .replace(/／/g, " / ").replace(/[，、]/g, ", ")
             .replace(/ -blade/g, "-blade")
             .replace(/\s+/g, " ")
             .replace(/\( /g, "(").replace(/ \)/g, ")").replace(/ ,/g, ",")
             .trim();
      } else {
        s = s.replace(/，/g, "、");
      }
    }
    return applyUnits(s);
  }

  function getUnit(){ return unit; }
  function setUnit(u){
    unit = u;
    localStorage.setItem(UKEY, u);
    document.dispatchEvent(new CustomEvent("unitchange", { detail: u }));
  }
  function cycleUnit(){
    const order = ["both", "metric", "imperial"];
    setUnit(order[(order.indexOf(unit) + 1) % order.length]);
    return unit;
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
    document.querySelectorAll("[data-i18n-html]").forEach(el => {
      el.innerHTML = t(el.getAttribute("data-i18n-html"));
    });
    document.querySelectorAll("[data-i18n-ph]").forEach(el => {
      el.setAttribute("placeholder", t(el.getAttribute("data-i18n-ph")));
    });
    document.querySelectorAll("[data-i18n-title]").forEach(el => {
      el.setAttribute("title", t(el.getAttribute("data-i18n-title")));
    });
    document.querySelectorAll("[data-i18n-aria]").forEach(el => {
      el.setAttribute("aria-label", t(el.getAttribute("data-i18n-aria")));
    });
  }

  /* 語言選單：點擊按鈕展開，點選項目切換（取代原本點擊輪換） */
  function mountSelector(btn){
    if (!btn || btn.dataset.langMounted) return;
    btn.dataset.langMounted = "1";
    const sync = () => { btn.textContent = LANG_NAMES[current] + " ▾"; };
    sync();

    const menu = document.createElement("div");
    menu.className = "lang-menu";
    menu.setAttribute("role", "listbox");
    menu.hidden = true;
    SUPPORTED.forEach(code => {
      const item = document.createElement("button");
      item.type = "button";
      item.className = "lang-item";
      item.dataset.lang = code;
      item.textContent = (I18N_STRINGS[code] && I18N_STRINGS[code]["lang.name"]) || LANG_NAMES[code];
      item.addEventListener("click", e => {
        e.stopPropagation();
        set(code);
        close();
      });
      menu.appendChild(item);
    });
    document.body.appendChild(menu);

    function mark(){
      menu.querySelectorAll(".lang-item").forEach(it =>
        it.setAttribute("aria-selected", String(it.dataset.lang === current)));
    }
    function place(){
      const r = btn.getBoundingClientRect();
      menu.style.top = (r.bottom + 6) + "px";
      // 靠右對齊按鈕，避免超出視窗
      menu.style.left = Math.max(8, Math.min(r.right - menu.offsetWidth, window.innerWidth - menu.offsetWidth - 8)) + "px";
    }
    function open(){ menu.hidden = false; mark(); place(); document.addEventListener("click", onDoc); }
    function close(){ menu.hidden = true; document.removeEventListener("click", onDoc); }
    function onDoc(e){ if (!menu.contains(e.target) && e.target !== btn) close(); }

    btn.addEventListener("click", e => {
      e.stopPropagation();
      menu.hidden ? open() : close();
    });
    document.addEventListener("langchange", sync);
    window.addEventListener("resize", () => { if (!menu.hidden) place(); });
  }

  const UNIT_NAMES = { both: "m·ft", metric: "m", imperial: "ft" };

  return { t, field, spec, specValue, get, set, cycle, apply, mountSelector,
           getUnit, setUnit, cycleUnit, UNIT_NAMES, SUPPORTED, LANG_NAMES };
})();

// 初始化語言標記
document.documentElement.setAttribute("lang", I18N.get() === "zh" ? "zh-Hant" : I18N.get());
