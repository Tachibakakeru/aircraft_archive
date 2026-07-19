# 天空檔案 SKY ARCHIVE

互動式飛行資料庫，涵蓋兩個主題：飛行器（機型列表 → 3D 檢視器，點選機體
部位顯示解說與規格）與機場／跑道（全球機場搜尋、跑道明細、衛星影像）。
首頁 `index.html` 選擇要探索哪一個。純靜態網站，無需後端即可部署。

## 專案結構

```
aircraft-archive/
├── index.html          首頁（模式選擇：飛行器圖鑑 / 機場與跑道）
├── fleet.html           機型列表頁（讀取 data/fleet.json，原 index.html）
├── viewer.html          3D 檢視器頁（viewer.html?model=<id>）
├── compare.html         機型比較頁
├── variants.html        機型家族與次型號對照（靜態參考頁）
├── airports.html        機場與跑道（獨立介面，見下方專節）
├── editor.html          機型資料編輯器
├── css/style.css        共用設計系統
├── js/viewer.js         檢視器邏輯（Three.js r128, 自 cdnjs 載入）
├── data/
│   ├── fleet.json       機隊索引（列表頁卡片內容）
│   ├── <id>.json        各機型的部位文案（名稱/概述/規格/冷知識）
│   ├── airports.json    機場搜尋索引
│   ├── countries.json   國家代碼 → 名稱
│   └── details/         依國家分桶的機場明細＋跑道（airports.html 用）
├── models/
│   └── <id>.json        各機型幾何資料（convert_fr24.py 產出）
├── assets/
│   └── thumb_<id>.png   列表頁側視縮圖（make_thumb.py 產出）
└── tools/
    ├── convert_fr24.py  模型轉換器（glTF 1.0 → 部位分類 JSON）
    ├── build_airports.py 機場資料匯入（OurAirports → data/airports.json 等）
    └── make_thumb.py    縮圖產生器
```

**首頁改版說明**：`index.html` 原本是機型列表頁，現已改為模式選擇首頁；
機型列表移到 `fleet.html`。若你先前分享過指向舊 `index.html`（機型列表）
的連結，該連結現在會導向新的模式選擇首頁而非直接進列表——這是刻意的
架構調整，未做相容轉址。

## 本機測試

瀏覽器會阻擋 `file://` 開啟時的資料讀取，請以本機伺服器測試：

```bash
cd aircraft-archive
python3 -m http.server 8000
# 瀏覽 http://localhost:8000
```

## 編輯機型資料（瀏覽器內建編輯器 · 密碼保護）

網站首頁右上角「✎ 編輯資料」，或每張卡片 hover 時右上的鉛筆圖示，進入
`editor.html`。**首次進入會要求設定編輯密碼**，之後每次進入需輸入密碼。

編輯器功能：
- 逐部位編輯名稱、英文標籤、概述、**條列式重點**、規格表、冷知識
- **加入圖片**：可貼外部圖片網址，或上傳本機圖片（會自動壓縮並內嵌）
- 編輯即時存入瀏覽器 `localStorage`，重整不遺失
- 「預覽檢視器」直接看套用後的效果（檢視器會優先讀取本機暫存）
- 「匯出 JSON」下載 `<機型>.json`，覆蓋 `data/` 內同名檔案後重新部署即上線
- 右上 🔒 鎖定並登出

### 密碼保護的分寸（重要）

這是防止「路人隨手亂改」的柵欄，**不是**防駭客的保險箱：

- 密碼以 SHA-256 雜湊存在瀏覽器 `localStorage`，不存明文
- 但這是純前端驗證，懂技術的人檢視原始碼就能繞過
- **真正的保護在架構上**：編輯結果只存在編輯者自己的瀏覽器，
  必須匯出 JSON 覆蓋檔案並重新部署才會影響線上內容。
  訪客即使繞過密碼、在自己瀏覽器亂改，也動不了其他人看到的網站。
- 密碼需在 HTTPS 或 localhost 下運作（`crypto.subtle` 要求安全環境）；
  Cloudflare Pages 全站 HTTPS，本機測試用 localhost 皆符合。
- 忘記密碼：清除該網站的瀏覽器資料（localStorage）即可重設。

> 若日後要開放多人共編、或要求「連編輯者本地資料都不能被繞過」，
> 就必須改用後端（如 Render）+ 資料庫 + 伺服器端驗證，那是另一個架構層級。

## 模型壓縮格式（v2）

`convert_fr24.py` 輸出的模型 JSON 採壓縮格式（`meta.format = 2`）：

- **頂點去重**：合併位置與 UV 相同的重複頂點（fr24 模型常有 80–90% 冗餘）
- **位置量化**：float32 座標 → uint16（每部位獨立的偏移＋尺度反量化），
  誤差約 0.6 mm，肉眼不可辨
- **材質合併**：同色／同貼圖的 primitive 合併為單一 mesh，減少陣列數量
- **貼圖重編碼**：縮至最長邊 1024px、JPEG 品質 80（需要 Pillow）

整體效果：全 39 型模型由約 68 MB 壓縮至約 17 MB（-75%）。
檢視器 `viewer.js` 同時支援 v2 與舊版 v1 格式，自動判斷。

> 貼圖壓縮需要 Pillow：`pip install pillow --break-system-packages`
> 未安裝時會跳過貼圖壓縮，幾何壓縮仍照常運作。

## 批次處理全部機型

```bash
# 轉換 fr24 倉庫內所有模型
for f in fr24-3d-models/models/*.glb; do
  id=$(basename $f .glb)
  python3 tools/convert_fr24.py "$f" "models/${id}.json"
done

# 為所有模型產生縮圖
for f in models/*.json; do
  id=$(basename $f .json)
  python3 tools/make_thumb.py "$f" "assets/thumb_${id}.png"
done
```

轉換時加 `--views` 參數會額外輸出三視圖 PNG 供目視檢查分類。

## 新增機型 SOP

以新增 A380（id: `a380`）為例：

```bash
# 1. 取得模型（glTF 1.0 binary）
git clone --depth 1 https://github.com/Flightradar24/fr24-3d-models.git

# 2. 轉換 + 自動部位分類（同時輸出三視圖驗證 PNG）
python3 tools/convert_fr24.py fr24-3d-models/models/a380.glb models/a380.json

# 3. 目視檢查三視圖中各部位顏色是否正確
#    （橘=引擎 藍=主翼 琥珀=垂直尾翼 綠=水平尾翼 紫=起落架）
#    分類錯誤時調整 convert_fr24.py 的 NAME_RULES 或 classify() 閾值後重跑

# 4. 產生列表縮圖
python3 tools/make_thumb.py models/a380.json assets/thumb_a380.png

# 5. 撰寫部位文案 data/a380.json（複製 data/a320.json 修改）
#    partOrder 只列該機型實際存在的部位

# 6. 在 data/fleet.json 的 aircraft 陣列加入一筆索引
```

轉換器的部位分類採三層策略，依序：
1. **節點名稱關鍵字**（如 `EngineL`、`rudder`、`slat3`）
2. **父節點繼承**（引擎子零件自動歸引擎）
3. **材質名稱與幾何特徵推斷**（包圍盒位置、展幅、高度）

不同機型的建模結構差異很大，第 3 步的三視圖驗證務必執行。

## 部署（Cloudflare Pages）

1. 將本資料夾推上 GitHub repo
2. Cloudflare Dashboard → Workers & Pages → Create → Pages → 連結該 repo
3. Build settings 全部留空（純靜態，無建置步驟），Deploy
4. 在 Custom domains 綁定你的網域（DNS 已在 Cloudflare 代管會自動配置）

模型 JSON 較大（737 約 4.3 MB），Cloudflare 會自動以 Brotli 壓縮傳輸
（base64 幾何壓縮率約 25%，實際傳輸量小得多）。

> 也可部署至 Render Static Site，但免費方案有休眠冷啟動；
> 純靜態內容建議優先使用 Cloudflare Pages。

## 授權聲明

- 3D 模型來源：[Flightradar24/fr24-3d-models](https://github.com/Flightradar24/fr24-3d-models)，
  採 **GPL-2.0** 授權。本專案對模型的修改（格式轉換、部位分類）依同授權釋出，
  轉換工具 `tools/convert_fr24.py` 即為修改流程的完整原始碼。
- Boeing 707、717、727-200、McDonnell Douglas DC-10-30 模型另行取自
  [FlightGear FGAddon](https://sourceforge.net/p/flightgear/fgaddon/HEAD/tree/trunk/Aircraft/)
  官方機庫（707 為「Lake of Constance Hangar」707，Copyright M.Kraus，GPL-3.0；
  717、727-200、DC-10-30 為 FGAddon 官方機庫，GPL-2.0+）。本專案將原始 AC3D（`.ac`）格式
  轉換為站內部位分件 JSON，共用解析器 `tools/ac3d_lib.py` 與各機型轉換腳本
  `tools/convert_ac3d_*.py` 為完整原始碼；貼圖／識別標誌未沿用來源檔案。
- McDonnell Douglas MD-82、MD-11 模型取自第三方 FlightGear 社群維護專案
  [Octal450/MD-80](https://github.com/Octal450/MD-80)、
  [Octal450/MD-11](https://github.com/Octal450/MD-11)，皆為 **GPL-2.0** 授權
  （非 FGAddon 官方機庫，逐一確認過授權條款；同系列的 DC-9 因僅找到
  CC BY-NC-SA 4.0〔禁止商業使用〕授權的來源模型，故未收錄，僅提供規格資料）。
- 網站程式碼與文案：自行撰寫。
- Three.js：MIT License，經 cdnjs 載入。

## GitHub 直接更新（方案 A）

編輯器的「⚙ GitHub」可設定直接 commit 到 repo，省去手動下載覆蓋：

1. **建立 Personal Access Token**（Fine-grained，推薦）
   - 到 https://github.com/settings/tokens?type=beta
   - Repository access 選 Only select repositories → 你的 repo
   - Permissions → Repository permissions → Contents 設為 **Read and write**
   - 產生後複製（只會顯示一次）
2. 在編輯器「⚙ GitHub」填入 owner、repo、branch（通常 main）、
   資料夾（data）、token，可先「測試連線」確認
3. 之後編輯完點「儲存」→ 直接 commit → Cloudflare Pages 自動重新部署

Token 只存在你的瀏覽器 localStorage，不會上傳到別處。未設定時「儲存」
自動退回下載 JSON 的方式。

### 架構可升級性

儲存邏輯集中在 `js/storage.js`，編輯器只呼叫 `Storage.save(id, data)`，
不直接依賴 GitHub。日後若要改用後端伺服器（方案 C）即時儲存，只需在
`storage.js` 新增一個 ServerStorage（`save` 內改為 POST 到你的 API），
編輯器程式碼完全不必更動。

## 新功能：比較、標註點、主題、詳細規格

### 機型比較（compare.html）
首頁「⇄ 比較」進入。可同時選最多 4 架機型並排比較,規格自動對齊分類,
同一列數值不同時以琥珀色標示差異。網址帶 `?ids=a320,b738` 可分享特定組合。

### 3D 標註點（hotspots）
檢視器的機體部位上直接浮現可點擊的標註點,不必只靠側邊面板。
點標註點等同點該部位;「標註點」按鈕可開關。

### 深/淺色主題
所有頁面右上「◐」切換,偏好記於瀏覽器,首次依系統偏好自動選擇。

### 詳細規格（維基風格分類規格表）
每個機型的 data JSON 新增 `specifications` 欄位,以分類（尺寸/重量/性能/
發動機等）組織詳細規格。檢視器「☰ 規格」開啟左側抽屜檢視;編輯器左側
「詳細規格」項可編輯,支援自訂分類與逐項增刪。目前 A220-100/300、A320、
737-800 已填入完整查證規格,其餘機型為骨架待補。

## 多語言（繁中 / English / 日本語）

所有頁面右上「繁中 / EN / 日本語」按鈕循環切換,偏好記於瀏覽器,首次依
瀏覽器語言自動選擇。

- **介面文字**（按鈕、標題、標籤）：三種語言完整翻譯,字典在 `js/i18n.js`。
- **內容文字**（機型解說、規格）：資料欄位支援 `{zh, en, ja}` 物件格式,
  未填的語言自動回退繁中。舊有的純字串格式仍相容(視為繁中)。

### 內容多語言化的資料格式

原本純字串的欄位可改寫為物件即支援多語言,例如部位名稱:

```json
"name": { "zh": "機身", "en": "Fuselage", "ja": "胴体" }
```

未改寫的欄位（仍是字串）會被當作繁中,在任何語言下都正常顯示。因此
可漸進式翻譯——先讓系統上線,再逐台逐欄補英日內容,不必一次到位。

目前 A320（部分部位）與 A320/737-800/A380/A220 的 tagline 已有英日示範,
其餘內容為繁中,切換語言時自動回退顯示。

## 詳細規格（維基機型規格等級）

737-800 已填入維基百科機型規格等級的完整資料（機組員、載客、尺寸、重量、
容量、性能、發動機共 6 類 29 項），可作為其他機型補完的格式範本。

## 機型家族與次型號對照（variants.html）

靜態參考頁，整理天空檔案 44 個條目所屬的機型家族與完整次型號系譜
（如 737NG 家族的 -600/-700/-800/-900），標出本站收錄哪一型、以及
ICAO/IATA 代號。內容為手動整理的參考資料，非資料驅動；家族說明目前
僅繁中，頁面外框（導覽/語言/主題）維持三語。

## 機場與跑道（airports.html）

獨立於機型頁面之外的第二個頂層介面，從首頁 `index.html` 或任一頁面的
「🏠 首頁」連結進入，不巢狀在機隊列表底下。

資料來源：[OurAirports](https://ourairports.com/data/)（Public Domain，
`davidmegginson/ourairports-data` 每日更新的鏡像）。**全量匯入**，不篩選
機型或代號——OurAirports 收錄的所有機場與跑道（含已關閉、無代號的小型
跑道）全數保留，目前共 **85,716 座機場、48,096 條跑道**。

```
data/
├── airports.json           全量搜尋索引（僅列表需要的欄位，~11 MB）
├── countries.json          國家代碼 → 名稱
└── details/<ISO國碼>.json  依國家分桶的機場明細（座標/標高/行政區碼）
                             ＋跑道清單，點開機場才整批載入該國一次
```

搜尋索引刻意省略座標/標高/跑道等「detail-only」欄位以控制常駐 payload，
這些欄位與跑道清單合併進 `details/<國碼>.json`，開啟任一機場時才連座標
帶跑道一次抓齊，同國其他機場沿用快取不必重抓。

**衛星影像**：機場詳情面板顯示以機場座標為中心、3×3 圖磚拼接的空拍圖，
圖源為 [Esri World Imagery](https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9)
公開圖磚服務（免金鑰，供合理使用；非本專案附屬服務，若圖磚服務調整
政策或流量受限，畫面會單純顯示載入失敗，不影響其餘功能）。縮放級別
依機場類別（大型機場拉遠以涵蓋完整跑道群，小型機場拉近）。

重新匯入最新資料：

```bash
curl -sSL https://davidmegginson.github.io/ourairports-data/airports.csv -o /tmp/airports.csv
curl -sSL https://davidmegginson.github.io/ourairports-data/runways.csv -o /tmp/runways.csv
curl -sSL https://davidmegginson.github.io/ourairports-data/countries.csv -o /tmp/countries.csv
python3 tools/build_airports.py /tmp/airports.csv /tmp/runways.csv /tmp/countries.csv .
```

單一國家最大的明細檔案（美國，32,569 座機場含小型/已關閉）約 6.8 MB，
其餘多在數百 KB 以內，點開機場時才依國家整批載入，不影響列表頁初始
載入速度；但美國等大國第一次點開機場時的載入會明顯慢一些，屬於全量
匯入的既知取捨。
規格分類鍵目前以繁中共用（尺寸/重量/性能等），數值支援多語言物件。
