# SKY ARCHIVE — 專案作業地圖

## 這個專案在做什麼

「天空檔案 / SKY ARCHIVE」是部署在 Cloudflare Pages 的純靜態航空資料網站與 PWA。它有四個可獨立瀏覽、可經驗證後編輯並發布的資料庫：

1. **飛行器圖鑑**：184 個機型的資料、規格、家族、比較與可互動的 Three.js 3D 檢視器；本機其中 48 型已有 3D（含協和號試作），136 型待補。
2. **機場與跑道**：85,587 座機場的搜尋、跑道、衛星圖、比較、收藏與資料編輯。
3. **全球航空公司**：目前 594 家航空公司的公司資料、呼號、機隊、樞紐、航線、收藏與航線地圖。
4. **航空小知識**：82 個三語航空知識條目，以座艙／飛航場景的可滑動互動 UI 呈現。

網站介面支援繁中、English、日文；內容欄位通常使用 `{ "zh", "en", "ja" }`，未翻譯時由 `I18N.field()` 回退繁中。

## 執行與部署

- 本機開發：`python server.py`，開啟 `http://localhost:8000`。`server.py` 對所有回應加上 `Cache-Control: no-cache, must-revalidate`，用來避免開發時讀到舊資源。
- 正式部署：GitHub `Tachibakakeru/aircraft_archive` 的 `main` 分支由 Cloudflare Pages 自動部署；無建置步驟。
- PWA：`sw.js` 管理離線快取。頁面採 network-first，資料／靜態檔採 stale-while-revalidate；改共用資源時要同步考量 `?v=N` 與 `CACHE` 名稱。
- 不要提交 `json token/`。該資料夾是使用者的 GitHub Token 備份，已列入 `.gitignore`。

## 主要入口

| 頁面 | 用途 | 主要程式 |
|---|---|---|
| `index.html` | 首頁「出境大廳」：全站搜尋、航線示意、登機證入口、每日出發看板、機長廣播、METAR 狀態列；設計紀錄見 `docs/homepage-concept.md` | `js/home.js`、`css/home.css`、`js/i18n.js`（`home.*`） |
| `fleet.html` | 機型清單、篩選、收藏與最近瀏覽 | 頁面內程式、`js/theme.js` |
| `viewer.html` | Three.js 機型檢視器，網址為 `?model=<id>` | `js/viewer.js` |
| `compare.html` | 最多四架機型比較 | `js/compare.js` |
| `variants.html` | 機型家族與次型號參考 | 頁面靜態內容、`js/i18n.js` |
| `versus.html` | Boeing / Airbus 兩機型部位與規格比較 | `js/versus.js` |
| `airports.html` | 機場、跑道、衛星圖、收藏、比較、編輯 | `js/airports.js` |
| `airlines.html` | 航空公司、機隊、航線圖、收藏、編輯 | `js/airlines.js`、`js/globe.js` |
| `knowledge.html` | 可無限滑動的航空知識互動場景；`?topic=<id>` 直接開啟條目 | `js/knowledge.js` |
| `editor.html` | 機型部位與規格的通用編輯器 | `js/editor.js` |

## 資料與資產

### 飛行器

- `data/fleet.json`：機型清單索引與卡片資料。
- `data/<id>.json`：機型文案、部位、規格、圖片；由 `viewer.html`、`editor.html` 使用。
- `models/<id>.json`：壓縮後 3D 幾何（格式 v2）。
- `assets/thumb_<id>.png`：機型卡片縮圖。
- `data/model_inventory.json`：由盤點工具產生的 3D 模型現況與缺模清單。
- `tools/convert_fr24.py`：glTF 1.0 → 站內 v2 模型格式。
- `tools/ac3d_lib.py` 與 `tools/convert_ac3d_*.py`：FlightGear AC3D 模型的解析與轉換。
- `tools/make_thumb.py`：由 `models/*.json` 產生縮圖。
- `tools/check_model_inventory.py`：依 `data/fleet.json` 與 `models/*.json` 重建 3D 模型盤點。
- `models/blender/concorde.blend`：協和號原創試作，325 個網格物件、12 組鉸鏈；主架先伸縮再旋轉，短艙上方為固定結構，襟副翼不能連動引擎。`tools/build_concorde_blender.py` 以 Blender 重建並匯出 v2 JSON，`tools/check_concorde_model.py` 驗證幾何與收放行程。
- `tools/add_a321_gear.py`：以 Airbus A321 公開技術資料為比例參考，在原 FR24 模型上產生六輪與三組可動起落架，直接輸出站內 v2 JSON；原模型只有輪艙門，腳本可重跑。此為展示用近似模型，不是原廠 CAD。修改後須更新 `viewer.js` 的模型 fetch 版號與 Service Worker 快取。
- `tools/build_a321_gear_blender.py`：使用本機 Blender 5.2（執行檔 `D:\blender.exe`）載入 A321 v2 模型，建立可編輯的 `models/blender/a321_gear.blend`（第 1 格伸出、第 61 格收起），並以機身網格檢查前輪收起後是否露出；新增輪組幾何仍以 `tools/add_a321_gear.py` 為來源。
- v2 的 `surfaces` 可附 `part`、`channel`、`angle`，搭配 `controls` 提供三語可動部位滑桿；未附這些欄位的舊模型沿用原有展開操縱面按鈕。
- 分段收放可用 `surfaces[].start` 延後旋轉，`e[].slide`／`slideEnd` 讓網格先沿母鉸鏈座標伸縮；Blender 與 viewer 必須保持同樣時序。碰撞檢查應涵蓋正負極限與中途姿態，不能只驗靜止幾何。
- `tools/check_knowledge.py`：驗證知識條目 ID 與三語欄位完整性；執行 `python tools/check_knowledge.py`。

### 機場

- `data/airports.json`：全庫搜尋索引（約 11 MB）。
- `data/airport_count.json`：首頁用的輕量機場數量。
- `data/details/<ISO>.json`：依國家分桶的跑道與詳細資料；開啟機場時才載入。
- `data/airport_codes.json`：ICAO/IATA → 機場名稱、城市、座標，用於航空公司編輯時的自動完成與連結。
- `data/countries.json`、`data/city_names.json`：國家與城市本地化。
- `data/airports_custom.json`、`data/airports_data_edits.json`：由站內編輯器發布的自訂機場與既有資料覆寫。
- `tools/build_airports.py`：匯入 OurAirports CSV，生成上述機場資料。

### 航空公司

- `data/airlines.json`：航空公司主資料（含 ICAO、IATA、Aviation Call Sign、機隊、樞紐、航線、三語介紹與 `tier` 分類；`cargo` 為貨運／快遞航空）。
- `data/airline_geo.json`：樞紐／航線文字到 ICAO 與座標的映射；決定是否可連到機場頁與畫在地球上。
- `js/airlines.js`：保留主資料為基底，再疊加本機草稿；不可用整份舊草稿取代伺服器資料。

### 航空小知識

- `data/knowledge.json`：82 筆主題，展示場景為 `instrument`、`runway`、`nav`、`systems`；各條目的 `category` 可為天氣、機場、導航、系統等內容分類。
- `js/knowledge.js`：三份內容複製形成無縫輪轉、覆蓋式詳情與本機／發布編輯。
- `css/knowledge.css`：輪轉、儀表與互動場景外觀。
- 新增知識條目或其他內容頁時，圖片是可選欄位，但編輯器須提供網址加入、本機上傳及逐張移除；引用外部實拍圖時保留來源、作者／授權與三語圖說，不使用生成圖冒充實景。
- 如從多人共用的實拍照片裁出特定部件，須使用原圖像素裁切、標明裁切修改、保留原作者與授權連結，並確認每張裁圖只呈現對應條目。

## 共用核心

- `js/i18n.js`：全站 UI 字典與內容欄位回退。新增介面字串時三種語言都必須新增。
- `js/theme.js`：深淺色主題、Service Worker 註冊，以及回機隊時保留搜尋條件。
- `js/ui.js`：共用 UI 行為，例如最近瀏覽列的拖曳捲動，以及所有自動完成下拉選單的方向鍵／Enter／Esc 操作。
- 介面中所有可捲動區域與下拉選單都必須隱藏原生滾輪軸；保留滑鼠滾輪、拖曳、觸控與鍵盤操作。瀏覽器原生選單若無法隱藏捲軸，改用站內自訂選單，不需再向使用者確認。
- `js/auth.js`：編輯鎖。正式站優先用 `/api/verify` 與 Cloudflare 的 `EDITOR_PASSWORD`；本機才退回瀏覽器 SHA-256 雜湊。
- `js/storage.js`：所有編輯發布均透過 `Storage.save(id, data)`；優先 `/api/gh-save`，再退回使用者瀏覽器內的 GitHub Token，最後下載 JSON。
- `functions/api/verify.js`、`functions/api/gh-save.js`：Cloudflare Pages Functions。Cloudflare 環境變數需有 `EDITOR_PASSWORD`、`GH_OWNER`、`GH_REPO`、`GH_TOKEN`；`GH_BRANCH` 可選（預設 `main`）。
- `functions/api/metar.js`：`/api/metar?ids=RCTP`，轉接 aviationweather.gov 的 METAR／TAF，Cloudflare 快取 5 分鐘；不需環境變數。本機 `server.py` 沒有 `/api`，機場天氣會顯示「需部署到 Cloudflare」。

### 2026-11 全站 UI 改版新增的共用模組（設計紀錄：`docs/homepage-concept.md`、`docs/site-redesign.md`）

- `css/style.css`：子頁設計 token 改為亮藍天空／夜航深藍。**`--amber` 是歷史名稱，現在代表主強調色（天空藍）**；收藏用 `--gold`、警示 `--warn`、天空帶 `--sky-1/2/3`、`--sky-ink`、`--glass*`、標題字 `--display`。也定義 `data-ico="名稱"` 線條圖示系統（CSS mask、跟著文字顏色；**不要再用 emoji 當按鈕圖示**）、跑道進度條樣式。字體（Barlow Condensed、IBM Plex Mono 拉丁子集）自帶在 `assets/fonts/`。
- `css/home.css`＋`js/home.js`：首頁「出境大廳」（不載入 style.css，token 名稱自成一套：`--azure`、`--hero-ink`…）。含我的登機證夾（三種收藏）、翻牌看板（`tileCard`／`flapTo`／`swapRow`，字格 class `tile`＋`tt/tb/tft/tfb`）、看板與機長廣播的自動輪換（`makeAuto()`）。`home.css` 有 reduced-motion 全域關閉動畫的規則，要照常播放的動畫須在檔案末段的 reduced-motion 區塊用 `!important` 排除。
- `js/sitebar.js`（defer）：子頁頂部導覽列，會把頁面的 `#btn-lang`／`#btn-unit`／`#btn-theme` 搬進去；3D 檢視器不插入。
- `js/skytime.js`＋`css/sky.css`（全站）：依所選時區（`hangar_tz`）設定 `<html data-sky="dawn|day|dusk|night">` 改天空漸層；`[data-skyclock]` 時鐘（翻頁式；`compact` 為導覽列縮小版）、`[data-tzpicker]` 站內時區選單；派發 `skychange`、`tzchange`。`sky.css` 必須在 style.css／home.css 之後載入。**sky.css 全站載入，class 一律加前綴**（時鐘卡片是 `sk-flip`；曾因 `.flip` 撞名讓首頁看板代碼消失）。
- `js/transition.js`＋`css/transition.css`（全站，放 `<head>`）：換頁過場。前往左→右、上一頁右→左、下一頁左→右（依歷史紀錄位置判斷；會包裝 `history.replaceState` 保留 `txIdx`）。正式站是乾淨網址（`/airlines`，Cloudflare 會把 `*.html` 308 轉址），頁面判斷一律用去掉 `.html` 的檔名。`localStorage.hangar_tx = "off"` 可關閉。
- `js/extras.js`（defer）：座艙音效（Web Audio、預設關、`hangar_sound`）、首頁航空紀念日橫幅（`?date=MM-DD` 可預覽）、首頁 Logo 飛越、收藏蓋章。
- `js/routemap.js`＋`css/routemap.css`：點陣世界地圖＋大圓航線動畫元件（首頁隨機航線、航線規劃、距離計算共用），`setPlane()` 可換機型剪影。
- `js/runway.js`：大檔下載的跑道進度條（機場頁 `airports.json`；壓縮傳輸時用 `expectedBytes` 估算，資料大幅變動時更新 `js/airports.js` 裡的數值）。
- `js/metar.js`：機場詳情的即時天氣（自行解析 METAR、飛航類別、風向袋、建議跑道）。
- `404.html`：「航班取消」頁，用 `<base href="/">`（Cloudflare 對任何不存在的路徑回應此檔）。
- 新資料與產生工具：`data/route_airports.json`（`tools/build_route_airports.py`，1,172 座大型機場）、`data/landmask.json`（`tools/build_landmask.py`，0.5° 陸地遮罩）、`assets/silhouettes/*.png`＋`data/silhouettes.json`（`tools/build_silhouettes.py`，由 3D 模型產生俯視剪影並對應 184 機型）、`assets/earth_daymap_1k/2k.jpg`（地球漸進貼圖）、`assets/icon*.png`（App 圖示）。新增 3D 模型後要重跑 `build_silhouettes.py`。
- 常用 localStorage 鍵：`hangar_tz`、`hangar_route_speed`、`hangar_route_pin`、`hangar_al_view`、`hangar_vscene`、`hangar_sound`、`hangar_tx`、`hangar_anniv_dismiss`、`hangar_board_auto`、`hangar_pa_auto`（首頁看板／機長廣播自動輪換秒數，0 = 手動）。
- 動畫與「減少動態效果」：使用者明確要求首頁航線與換頁動畫在系統開啟 reduced-motion 時仍要播放（曾因此被誤認為沒有動畫），不要再以 reduced-motion 直接略過。
- Cloudflare Pages 部署偶爾卡在 initialize：先 Cancel 卡住的部署再 Retry；只改文件的提交可在訊息加 `[CF-Pages-Skip]` 避免多佔建置名額。

## 編輯與發布規則

1. 先以本機伺服器測試；不要用 `file://`，否則 `fetch` 會失敗。
2. 使用者要求本地檢查時，**不要 push**，直到明確同意。
3. 資料編輯必須明確按「儲存本機」才寫入草稿；關閉編輯器的未儲存修改應還原。
4. 發布時必須經 `requireAuth()`，並用 `Storage.save()`，不能將 Token 寫入資料檔或前端原始碼。
5. 新增／調整航空公司樞紐或航線後，補 `data/airline_geo.json`；可解析的機場才應產生連結。
6. 改動任何已被快取的 CSS、JS、資料 fetch URL 或 HTML 引用時，更新相關 `?v=N`；改快取策略時同步更新 `sw.js` 的 `CACHE` 名稱。
7. 修改 JSON 後先驗證：`Get-Content -Raw <file> | ConvertFrom-Json | Out-Null`。

## 3D 模型注意事項

- 新增模型的標準流程：來源／授權確認 → 轉換至 `models/<id>.json` → 產生縮圖 → 新增 `data/<id>.json` → 更新 `data/fleet.json` → 實際檢視部位分類與起落架。
- `viewer.js` 同時支援舊格式與 `meta.format = 2` 壓縮格式。
- 來源授權在 `README.md` 有記錄；新增模型不得沿用未取得適當授權的紋理或標誌。

## UI／動畫 Skills（2026-11-07 17:31 新增）

- 來源：[emilkowalski/skills](https://github.com/emilkowalski/skills)（MIT），以 `npx skills@latest add emilkowalski/skills -s <名稱> -a claude-code --copy -y` 安裝到專案層級 `.claude/skills/`；版本鎖定在 `skills-lock.json`，更新用 `npx skills@latest update -p`。
- 已安裝 6 個，處理 UI／動畫時 Claude Code 會自動套用，也可點名使用：

| Skill | 用途 | 本專案適用處 |
|---|---|---|
| `emil-design-eng` | 介面細節與動畫決策總原則 | 全站緩動曲線、時長、陰影 |
| `improve-animations` | 全站動畫稽核，產出 `plans/NNN-*.md` 實作計畫（本身不改程式） | 定期稽核 CSS／JS 動畫 |
| `animation-performance` | 掉幀診斷、只動 transform／opacity | 3D 檢視器、地球儀、機場頁大檔載入時的動畫 |
| `choreograph` | 多元素進場順序與時間差 | 換頁過場、首頁區塊進場、翻牌看板 |
| `mobile-native` | 讓網頁在手機上更像原生 App | PWA、安全區域、觸控 hover |
| `break-ui` | 用極端資料壓力測試版面 | 超長機場名、空搜尋結果、594 家航空公司列表 |

- 套用 skill 建議時，本專案既有決定優先：首頁航線、換頁過場、翻頁時鐘、翻牌看板在 reduced-motion 下**照常播放**（見上方「動畫與減少動態效果」）；過場 0.9／1.0 秒與 `--tx-ease` 是依使用者回饋調整；跑道起飛與翻牌下落的 ease-in 是刻意的物理動作。
- `improve-animations` 的實作計畫放在 `plans/`，`plans/README.md` 為總表；2026-11-07 首次稽核結果記在 `Progress.md`。
- `.claude/skills/`（Claude Code 用）與 `.agents/skills/`（其他代理用，2026-11-07 17:51 出現的同 6 個 skill 複本）已列入 `.gitignore`（2026-11-07 19:13 決定）：skill 檔來自外部 MIT 專案、複本未附授權聲明，且 Cloudflare Pages 會原樣部署 repo 內檔案，故不進版本控制。只提交 `skills-lock.json`；新電腦或檔案遺失時在專案根目錄執行 `npx skills experimental_install` 依 lock 檔裝回同版本。

## 持續紀錄規則

- `Progress.md` 是本專案的工作日誌與待辦單。每次本 task 回答涉及檢查、決策、改動、測試、提交或發現新問題時，都要同步更新。
- 更新時記錄日期、範圍、結果與未解事項；不要記錄 Token、密碼或其他機密。
- 開始新工作前先讀 `Progress.md`，避免覆蓋使用者未提交的資料或重做已完成工作。
