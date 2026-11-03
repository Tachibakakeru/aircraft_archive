# 全站 UI 改版紀錄（首頁以外的頁面）

> 給後續 session 的交接文件，隨工作進度持續更新。
> 開始日期：2026-11-03。
> 使用者要求：首頁已改成「出境大廳」亮藍風格，其他頁面也要跟進；**處理完先不推送**，先給使用者預覽檢查，確認後才推送。
> 首頁的設計來源與 token 定義見 `docs/homepage-concept.md`。

## 目前狀態

- [x] 盤點各頁現況
- [x] 共用設計系統（`css/style.css` token、字體、元件）
- [x] 共用頂部導覽列（`js/sitebar.js`）
- [x] 各頁修正（第一輪）
- [x] 版本號與 Service Worker
- [x] 截圖預覽給使用者（第一輪，2026-11-03）
- [ ] 使用者檢查回饋與調整
- [x] 推送到工作分支 `claude/eager-euler-euibb4` 存檔並產生 Cloudflare 預覽（使用者要求，2026-11-03）；**尚未合併到 `main`**
- [x] 第二輪：說明 emoji 位置、新 Logo、地圖加速（2026-11-03，推送到工作分支供預覽）
- [x] 第三輪：所有 emoji 改為自繪線條圖示（2026-11-03，推送到工作分支供預覽）
- [x] 使用者回覆「PUSH」，合併到 `main` 正式上線（2026-11-03，快轉合併）

## 1. 現況盤點（改版前）

- 所有子頁共用 `css/style.css`，token 名稱為 `--bg-0`、`--bg-1`、`--panel`、`--stroke`、`--text`、`--muted`、`--amber`（主強調色）、`--amber-soft`、`--cyan`、`--on-amber`、`--bg-glow`、`--scene-*`。深色是 `:root` 預設，淺色在 `:root[data-theme="light"]`（`js/theme.js` 一定會設定 `data-theme`）。
- 主強調色是琥珀色，和新首頁的亮藍不一致；`--amber` 在各頁 CSS 共被引用上百次。
- 頁首有三種寫法：
  - `.fleet-head`（eyebrow 連結＋h1＋副標）：`fleet`、`airlines`、`airports`、`distance`、`knowledge`、`variants`。
  - 頂部工具列 `.cmp-topbar`／`.vs-topbar`／`.ed-topbar`：`compare`、`versus`、`editor`。
  - 全螢幕 3D 場景＋浮動 `.v-header`：`viewer`。
- 工具列擠滿導覽按鈕，且多數帶 emoji（例如 `fleet.html` 一列有 16 個按鈕，其中 6 個只是連到其他頁）。
- 改版前截圖：`fleet`、`airlines`、`airports`、`distance`、`knowledge`、`variants` 都是「淡灰藍底＋小字琥珀 eyebrow＋大標題＋一排按鈕」，和舊首頁一樣偏死板。

## 2. 設計方向

和首頁同一套語彙，但子頁是「工作頁面」，所以只借用首頁的骨架，不搬首頁的裝飾（不放登機證、看板等）：

1. **同一組顏色**：沿用首頁的亮藍天空（淺色）／夜航深藍（深色），主強調色從琥珀改成天空藍。
2. **同一條導覽列**：每個子頁最上方都有和首頁一樣的深藍導覽列（品牌＋四個資料庫＋語言／主題），並標出目前所在的資料庫。取代原本散在各頁工具列裡、帶 emoji 的「首頁／航空公司／小知識」按鈕。
3. **天空頁首**：有 `.fleet-head` 的頁面，標題區變成滿版天空帶，白字大標題用首頁的窄體字；下方的搜尋／篩選工具列變成白色浮動卡片，壓在天空與頁面的交界，對應首頁的訂票框。
4. **頂部工具列頁**（比較、對比、編輯器）：工具列改成天空藍帶，按鈕改玻璃質感，主要按鈕改白底藍字。
5. **3D 檢視器**：維持全螢幕，不加導覽列；場景背景改成天空藍漸層（淺色）／夜空藍（深色）。
6. **收藏星號**維持金色（`--gold`），不跟著變藍，保留「收藏」的直覺。

## 3. 實作細節

### 3.1 色彩 token（`css/style.css` 開頭）

為了不改寫各頁上百處 `var(--amber)`，**沿用舊 token 名稱，改它的值**：

| Token | 深色（`:root`） | 淺色（`[data-theme="light"]`） | 說明 |
|---|---|---|---|
| `--bg-0` / `--bg-1` | `#061730` / `#0a2244` | `#eef6ff` / `#f7fbff` | 頁面底色 |
| `--panel` / `--panel-solid`（新增） | 半透明深藍 / `#0d284d` | 白 / `#ffffff` | 卡片、面板 |
| `--stroke` | 淡藍線 | `#cde0f7` | 邊框 |
| `--text` / `--muted` | `#e4f0ff` / `#93b3db` | `#0b2a55` / `#4f6d96` | 文字 |
| `--amber` | `#4ea4ff` | `#1a73f0` | **主強調色（天空藍）**，名稱是歷史包袱 |
| `--amber-2`（新增） | `#7cbcff` | `#3d95ff` | 強調色 hover |
| `--on-amber` | `#04152b` | `#ffffff` | 強調色底上的文字（原本很多地方寫 `color:var(--bg-0)`，淺色主題會變成淺藍字配藍底，已全部改用 `--on-amber`） |
| `--cyan` | `#4fd3ff` | `#0b8fc0` | 次要色 |
| `--gold`（新增） | `#ffc24d` | `#e8930c` | 收藏星號（列表、詳情、地球儀上的收藏點） |
| `--warn`（新增） | `#ff8a65` | `#d9480f` | 錯誤、刪除 hover |
| `--sky-1/2/3`、`--sky-ink`、`--sky-muted`、`--glass`、`--glass-line`（新增） | 夜空 | 晴空 | 導覽列與天空帶，數值和首頁 `css/home.css` 相同 |
| `--shadow` / `--shadow-hi`（新增） | | | 卡片陰影 |
| `--thumb-bg`（新增） | 深藍 | 飽和天空藍 `#3b86ea→#1456b8` | 機型縮圖底（縮圖多是淺色機體，太淺的底會讓飛機看不清楚；第一版用淡藍底，截圖後改深） |
| `--display`（新增） | | | Barlow Condensed＋系統中文字體，標題用 |
| `--scene-*` | 夜空藍 | 天空藍 | 3D 檢視器背景與格線 |

字體：`style.css` 也宣告 Barlow Condensed／IBM Plex Mono 的 `@font-face`（檔案同首頁，`assets/fonts/`），`--mono` 改為 IBM Plex Mono 優先。

### 3.2 全站導覽列 `js/sitebar.js`

- 以 `defer` 載入（在各頁 `js/i18n.js` 之後），DOM 解析完後在 `<body>` 最前面插入 `<header class="site-bar">`，並在 body 加 `has-site-bar`。
- 連結與標示：飛行器圖鑑（fleet／viewer／compare／versus／variants／editor 都算在這一區）、機場與跑道（含 distance）、航空公司、小知識；目前所在區加 `aria-current="page"`（白底藍字）。
- 文字沿用首頁已有的 `home.nav.*`、`home.brand` 字串，所以**各頁都要載入新版 `js/i18n.js?v=200`**（編輯器原本沒有載入 i18n.js，已補上）。語言切換時（`langchange`）會更新文字。
- 把頁面原有的 `#btn-lang`、`#btn-unit`、`#btn-theme` 按鈕節點**搬進**導覽列右側。搬移節點會保留原本的事件，所以各頁程式不用改；若原工具列因此變空（距離計算頁），整列移除。
- `body.viewer`（3D 檢視器）不插入。
- 樣式在 `style.css` 的「全站導覽列」段落；760px 以下導覽連結換到第二行。
- `#panel`（機場／航空公司詳情、檢視器解說面板）的 z-index 從 6 提高到 40，否則頂端會被導覽列（z-index 30）蓋住。

### 3.3 天空頁首與工具列（`style.css` 末段）

- `.fleet-head::before` 用 `100vw` 寬、`top:-160px` 的漸層做滿版天空，往上延伸到導覽列下方；`::after` 在底部漸層接回頁面底色。`body` 加 `overflow-x:clip` 防止 100vw 造成橫向捲動。
- `.fleet-head h1` 用 `--display` 窄體、白字；eyebrow、副標改 `--sky-muted`。
- `.fleet-toolbar` 改成白色浮動卡片（`margin-top:-34px`、圓角 18、`--shadow-hi`）。
- `.ed-entry` 改成膠囊按鈕、一般字體；搜尋框圓角 12、聚焦時有淡藍光圈。
- `.craft-card` 圓角 18、陰影、標題窄體字；製造商小字改主色。

### 3.4 各頁修改

| 頁面 | 修改 |
|---|---|
| `fleet.html` | 移除工具列中重複的「距離計算／航空公司／小知識／首頁」連結（保留比較、機型對比、機型家族、編輯資料） |
| `airlines.html` | 移除「飛行器圖鑑／機場與跑道／距離計算／小知識／首頁」連結；貨運標籤顏色改用 token |
| `airports.html` | 移除「航空公司／小知識／首頁」連結（保留距離計算） |
| `distance.html` | 工具列只剩導覽連結與語言／主題，全部由導覽列取代，工具列自動移除 |
| `knowledge.html` | 移除「首頁」連結；座艙儀表維持深色（真實座艙配色） |
| `variants.html` | 保留「← FLEET」返回 |
| `compare.html`、`versus.html`、`editor.html` | 頂部工具列改天空帶（樣式寫在各自 CSS 末段，因為它們在 `style.css` 之後載入，寫在 style.css 會被覆蓋）；比較圖的第一個分類色改主色藍 `#3d95ff`，其餘（琥珀、綠、紫）保留以維持辨識度 |
| `viewer.html` | 不加導覽列；標題改窄體字；場景背景由 token 決定 |
| `css/editor.css` | 寫死的 `#0e1729` 深色輸入框底、`#ffc266`、`#ff7850` 等改用 token，並移除只在淺色主題補丁的規則 |
| `js/globe.js` | 地球儀上收藏的機場／航空公司改讀 `--gold`（原本讀 `--amber`，改版後會變藍） |

### 3.5 版本號

- 所有子頁：`css/style.css?v=200`、`js/i18n.js?v=200`、`js/sitebar.js?v=200`，以及有改到的頁面 CSS（airlines、airports、compare、distance、editor、knowledge、variants、versus）`?v=200`；`js/compare.js?v=200`、`js/globe.js?v=200`。
- `sw.js`：`CACHE` 由 `hangar-v50` 升為 `hangar-v51`。
- 首頁 `index.html` 本輪沒有修改（仍引用 `i18n.js?v=193`，內容一樣適用）。

## 4. 驗證（第一輪）

- 本機 `server.py`＋Playwright，十個子頁在 1280×800 淺色與深色各截一張：無 page error、無橫向溢出。
- 機場搜尋 `RCTP` 開詳情、航空公司搜尋 `EVA` 開詳情：面板頂端不再被導覽列蓋住。
- 390px 手機寬度：機隊、航空公司頁無橫向溢出，導覽列換成兩行。
- `knowledge.html?topic=cavok` 深連結仍正常開啟詳情。
- 編輯器以本機測試密碼登入後的畫面正常（測試用 localStorage，不影響正式資料）。
- 測試機的限制：沙盒連不到 cdnjs（Three.js）、Wikimedia、ArcGIS 衛星圖。3D 檢視器截圖時用 Playwright 把 cdnjs 的 Three.js r128 轉到本機副本；衛星圖與部分照片在截圖中是空白，屬測試環境限制，與改版無關。

預覽截圖（給使用者，非版本控制）：scratchpad 的 `preview-light.png`、`preview-dark.png`、`preview-details.png`。

## 5. 未解事項／可再討論

- 工具列按鈕文字仍帶 emoji（⭐ 只看收藏、🌐 地圖、⇄ 比較、📋 機型家族…），首頁已不使用 emoji；是否全部改成線條圖示或純文字，待使用者決定。
- `.fleet-head` 裡的「SKY ARCHIVE / 天空檔案」eyebrow 和導覽列品牌重複，可考慮改成麵包屑（例如「機場與跑道 / 距離計算」）。
- 詳情面板、比較表、編輯器表單內部只做了換色，版面沒有重新設計。
- `editor.html` 原本只有中文介面，本輪只補上 i18n.js 讓導覽列能顯示，編輯器本身仍未多語化。

## 6. 第二輪（2026-11-03）：emoji 說明、新 Logo、地圖加速

### 6.1 使用者問「emoji 指哪個部分」

指的是子頁按鈕文字前面的表情符號，都來自 `js/i18n.js` 的字串（三種語言都有）。主要出現在：

| 位置 | 字串 key | 目前文字（繁中） |
|---|---|---|
| 機隊／機場／航空公司工具列 | `fleet.favonly`、`airports.favonly` | ⭐ 只看收藏 |
| 機場工具列 | `airports.view.globe` | 🌐 地圖 |
| 航空公司工具列 | `airlines.view.map` | 🌐 航線地圖 |
| 機隊工具列 | `nav.versus`、`nav.variants`、`fleet.edit` | ⚔ 機型對比、📋 機型家族、✎ 編輯資料 |
| 機場工具列 | `nav.distance` | 📏 距離計算 |
| 多處 | `fleet.compare`、`viewer.compare`、`viewer.specs` | ⇄ 比較、☰ 規格 |
| 機場詳情／編輯 | `airports.detail.uploadImage`、`airports.detail.publish`、`airports.detail.editBtn` | 📁 上傳圖片、☁ 發布到網站、✎ 編輯 |
| 小知識編輯 | `knowledge.edit.fact`、`knowledge.edit.imgfile`、`knowledge.edit.publish` | 💡 冷知識、📁 上傳、🚀 發布 |
| 資料編輯器頂部 | `editor.html` 寫死 | 🔒、🔑、⚙ GitHub |

（第三輪已依使用者決定全部改為線條圖示，見第 7 節。）

### 6.2 新 Logo（`assets/icon.svg`）

- 舊版：深色 `#0b1220` 圓角方塊＋琥珀色飛機。
- 新版：天空藍漸層圓角方塊（`#0f5fd0 → #2f8cf5 → #6db8ff`）、白色圓框、白色虛線航跡與起點圓點、沿航跡爬升的白色飛機；與首頁／導覽列的品牌標誌同一造型。主要圖形在中央安全區內，可當 maskable 圖示。
- 新增 PNG：`assets/icon-180.png`（`apple-touch-icon`，iPhone 加到主畫面用）、`icon-192.png`、`icon-512.png`（PWA，含 maskable）。以 Playwright 由 SVG 輸出。
- `manifest.json`：圖示改為 SVG＋PNG，`theme_color` `#1565d8`、`background_color` `#eef6ff`，描述補上航空公司與小知識。
- 所有頁面：`<link rel="icon" href="assets/icon.svg?v=2">`、新增 `apple-touch-icon`、`manifest.json?v=2`，避免瀏覽器沿用舊圖示快取。

### 6.3 地圖加速

**(a) 機場衛星圖（詳情面板縮圖與放大檢視）**

- 歷史：最早用多張 `<img>` 圖磚以 CSS Grid 拼貼，桌機正常，但**手機上常錯位亂拼**（子像素捨入、retina 縮放、記憶體壓力）。後來改用 Esri `export` 端點一次取整張影像解決錯位，但 export 每次由伺服器即時繪製、CDN 與瀏覽器都無法快取，一張常要 1 秒以上。
- 現在（`js/airports.js` 的 `buildSatCanvas()`／`mountSat()`）：改回讀**圖磚**（CDN 快取、`sw.js` 的 `TILE_CACHE` 也會 cache-first 保存），平行下載後以**整數像素座標畫進同一張 `<canvas>`**。畫面上只有一張點陣圖、沒有任何 CSS 拼接，所以不可能出現舊版的錯位；圖磚一到就畫上（漸進顯示），第二次打開同一座機場直接讀快取。
  - 先四捨五入視窗左上角的全域像素座標，再算每塊圖磚的位移，所有位移都是整數。
  - 經度跨換日線時圖磚 x 取模環繞；緯度超出 Web Mercator 範圍時夾在 ±85.05°。
  - 圖磚先以 CORS 載入（Service Worker 才能快取；地球檢視的地面貼片原本就以 CORS 讀同一服務，證實 Esri 有提供 CORS），失敗再以一般模式載入。
  - 任何一塊圖磚失敗，就退回原本的 export 單張影像。
  - 放大檢視切換縮放時，舊影像保留到新影像全部畫好才換，不會出現半新半舊。
  - 框景與舊版一致：縮圖寬 3 塊圖磚（768px canvas），放大檢視寬 5 塊（1280px）。
- `airports.html`、`airlines.html` 加 `preconnect` 到 `server.arcgisonline.com`（CORS）與 `cdnjs.cloudflare.com`。

**(b) 機場／航空公司的 3D 地球（地圖模式）**

- Three.js 原本要等按下「地圖」才開始下載。現在 `AptGlobe.preload()` 會在頁面閒置時（`requestIdleCallback`，省流量模式或 2G 除外），以及手指碰到／滑鼠移到地圖按鈕時，先下載 Three.js 和小張地球貼圖。
- 地球貼圖改為漸進：先貼 `assets/earth_daymap_1k.jpg`（1024×512，約 63 KB），再換高解析——桌機且顯示卡支援 4096 用原本 `earth_daymap.jpg`（4096×2048，約 473 KB），手機／小螢幕／省流量用新增的 `earth_daymap_2k.jpg`（2048×1024，約 225 KB），也減少手機的顯示記憶體用量。貼圖到之前球體先用海洋藍，不會出現白球。

**版本**：`js/airports.js`、`js/airlines.js`、`js/globe.js`、`css/airports.css` 升 `v=201`；Service Worker `hangar-v52`。

### 6.4 驗證

- 沙盒連不到 Esri，測試時由 Playwright 回傳「帶邊框、十字線與 z/y/x 編號的 SVG 測試圖磚」（含 CORS 標頭），在 **iPhone 13 模擬**下打開 RCTP：縮圖為 768×768 canvas、放大檢視 1280px canvas，所有圖磚邊框與十字線連續對齊、編號依序正確，中心落在桃園機場所在圖磚。
- 地圖：閒置後已預載 Three.js 與 1k 貼圖；切到地圖時依序載入 1k → 2k（手機）。無 page error。
- 實際 Esri 影像的載入速度要在預覽或正式站上確認（沙盒無法連線）。

## 7. 第三輪（2026-11-03）：emoji 全部改成線條圖示

### 7.1 方案比較與選擇

使用者決定「emoji 全部改掉」並詢問推薦方案。考慮過三種：

| 方案 | 優點 | 缺點 |
|---|---|---|
| **A. 自繪線條 SVG 圖示＋文字（採用）** | 風格與首頁「機上工具」、導覽列標誌一致；跟著文字顏色自動適應深淺色；各平台顯示一致（emoji 在 Windows／Android／iOS 長得都不一樣）；無外部依賴、可離線 | 需要自己畫一組圖示 |
| B. 純文字 | 最簡單 | 工具列一長串文字，較難一眼辨識；只有圖示的小按鈕（收藏、編輯、關閉）無法只用文字 |
| C. 外部圖示庫（字型或 CDN） | 圖示多 | 多一個外部依賴、離線 PWA 要另外處理、檔案大 |

### 7.2 做法

- `css/style.css` 末段新增圖示系統：元素加 `data-ico="名稱"`，圖示用 `::before` 的 CSS mask 畫出、顏色取 `currentColor`。好處是 `I18N.apply()` 改寫 `textContent` 時不會把圖示洗掉，切換語言不用額外處理；深淺色也自動跟著文字顏色。
- 只有圖示、沒有文字的按鈕（內容為空）不留右側間距，並補上 `aria-label` 讓螢幕閱讀器讀得到。
- 收藏星號：`data-ico="star"`，元素有 `.on` 或 `aria-pressed="true"` 時自動變實心。原本 JS 用 `textContent = "★"/"☆"` 切換的程式已移除（`js/airports.js`、`js/airlines.js` 的 `syncFavButton()`，以及列表列與 `fleet.html` 卡片模板）。
- 27 個自繪 24×24 線條圖示（2px 圓角線），沒有引用外部圖示庫：

| 名稱 | 用途（取代） |
|---|---|
| `star`／`star-fill` | 只看收藏、收藏按鈕（⭐ ☆ ★） |
| `globe` | 地圖、航線地圖（🌐） |
| `compare` | 比較、加入比較、開始比較、距離頁的交換（⇄） |
| `versus` | 機型對比（⚔） |
| `family` | 機型家族（📋） |
| `route` | 距離計算（📏） |
| `edit` | 編輯（✎） |
| `cloud-up` | 發布到網站、儲存到網站、小知識發布（☁ 🚀） |
| `upload`／`download` | 上傳圖片（📁）、貼上設定碼（📥） |
| `link` | 分享連結（🔗） |
| `cube` | 航空公司機隊的「3D」連結（🔗 3D） |
| `x` | 所有關閉／移除按鈕（✕） |
| `clock`／`grid` | 機隊頁「時間軸／卡片」切換（🕒 ▤）、機場資料載入中（⏳） |
| `list` | 3D 檢視器的規格（☰） |
| `lock`／`key`／`gear`／`copy` | 編輯器的鎖定、變更密碼、GitHub 設定、複製設定碼（🔒 🔑 ⚙ 📋） |
| `eye`／`eye-off` | 密碼欄位的顯示／隱藏（👁 🙈，`js/auth.js`） |
| `bulb` | 小知識「冷知識」、對比頁的補充說明（💡） |
| `save`、`zoom` | 預留：本機草稿標示、放大（衛星圖 hover 的 🔍 改為 CSS 背景 SVG） |
| `sun` | 子頁的主題切換按鈕（原本是 ◐，改成和首頁一樣的太陽） |

- `js/i18n.js`：28 個 key × 3 種語言共 84 個字串移除開頭的 emoji（例如 `fleet.favonly`、`nav.*`、`airports.detail.*`、`knowledge.edit.*`）；`versus.sub` 句中的「✎ 編輯」改成「編輯」。
- 保留的一般符號：↗（外部連結）、▾（下拉）、✓（語言選單已選）、← →（返回／流程），它們是排版符號，不是 emoji。

### 7.3 版本與驗證

- 版本：所有頁面 `css/style.css?v=201`、`js/i18n.js?v=201`；`js/airports.js`／`js/airlines.js` `v=202`、`css/airports.css` `v=202`；`js/auth.js`、`js/knowledge.js`、`js/versus.js`、`js/editor.js` `v=201`；Service Worker `hangar-v53`。
- 掃描所有 HTML／JS／CSS，除上述保留符號外已無 emoji。
- 截圖確認：機隊（淺色／深色）、機場、航空公司工具列，機場與航空公司詳情面板頂端按鈕，3D 檢視器頂部，編輯器頂部，圖示都正確顯示、大小一致；所有 JS 語法檢查通過、無 page error。
