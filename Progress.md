# SKY ARCHIVE — 進度與維護紀錄

> 此檔由協作 task 持續更新。記錄實際變更、驗證結果與待處理事項；不記錄密碼、Token 或其他機密。

## 目前狀態（2026-08-24）

- 專案：Cloudflare Pages 靜態/PWA 航空資料庫，正式分支為 `main`。
- 資料庫現況：52 機型、47 個 3D 模型 JSON、85,587 座機場、594 家航空公司、45 筆航空小知識。
- 最近已推送 commit：`b87532f`（新增貨運航空分類與航空知識搜尋功能）。
- 工作目錄發現未追蹤檔案：`data/korean_airlines_debug.json`。它是除錯輸出，暫不刪除、不提交，待確認是否仍需保留。

## 已完成

### 資料庫與功能

- 建立機型 3D 轉換管線，並補上 B707、B717、B727、DC-9、DC-10、MD-80、MD-11 等 FlightGear／開源授權來源模型。
- 新增 Boeing / Airbus 比較頁、Dreamlifter 規格資料、機型家族多語系修正與動態首頁統計。
- 新增「航空小知識」：44 筆中英日內容、四類互動場景、無縫橫向輪轉、觸控／滑鼠拖曳、可編輯與發布。
- 機場：全庫搜尋、跑道、衛星圖、收藏／比較、台／臺搜尋相容、自訂機場及資料編輯／發布；移除 129 筆名稱帶 `[Duplicate]` 的重複資料。
- 航空公司：Call Sign 顯示／搜尋／編輯、樞紐與航線機場自動完成、可點擊機場連結、收藏按國家排序、Logo 本機上傳、封面圖殘留修正。
- 完成韓國與日本航空公司的補資料；日本新增公司之樞紐與代表航線已補齊 `airline_geo.json` 對應並完成本機驗證。

### 編輯、發布與快取

- 編輯權限整合 Cloudflare Pages Functions：`/api/verify` 驗證站台密碼，`/api/gh-save` 代管 GitHub 寫入，避免把 GitHub Token 放入前端。
- 保留瀏覽器 GitHub Token／下載 JSON 的後備機制。
- 航空公司編輯改為只有按「儲存本機」才寫入 localStorage；離開未儲存的表單會還原，避免意外覆寫。
- 修正舊版全量 localStorage 草稿遮蔽伺服器新版航空公司資料的問題：以伺服器主資料為底，逐筆套用本機覆寫。
- 新增 `server.py` 的 no-cache 本機伺服器，Service Worker cache 升為 `hangar-v3`，並持續用 `?v=N` 避免部署後讀到舊資源。

## 待處理／注意事項

1. **清理或忽略除錯檔**：`data/korean_airlines_debug.json` 尚未追蹤；確認不再需要後再由使用者授權移除，或明確加入忽略規則。
2. **README 對齊現況**：README 仍有歷史數字與舊的頁面描述（例如機場數、機型家族內容語系、首頁範圍），應在下一次文件整理時更新；不影響目前功能。
3. **資源版本一致性**：HTML／JS 中存在不同 `?v=` 數字。修改共用資源時需同批更新直接引用與內部 `fetch` URL，並視情況更新 `sw.js` 的 cache 名稱，避免再次出現瀏覽器舊快取。
4. **航空公司資料品質**：航空公司機隊與航線是人工彙整的非即時資料。新增或修訂時應使用官方網站、ICAO／IATA 或維基的可核對資料，並同步補 `airline_geo.json`。
5. **大檔載入**：`data/airports.json` 約 11 MB，部分裝置首次解析會有明顯等待；目前已加入載入提示。若未來成為效能瓶頸，再考慮搜尋索引分片，而非預先複雜化。

## 本次紀錄（2026-08-24）

- 已讀取並確認完整專案架構、主要資料檔、Cloudflare Functions、快取機制與目前 Git 狀態。
- 新增 `AGENTS.md`：記錄系統概覽、入口、資料流、編輯／發布、安全、3D 模型與維護規則。
- 新增本 `Progress.md`：建立後續改動、驗證與待辦的唯一持續紀錄。
- 未修改網站功能或資料；未提交、未推送任何變更。

### 航空小知識搜尋與高旁通比引擎（本機待提交）

- 新增「高旁通比渦扇發動機」三語條目，置於「系統與航機性能」輪轉場景；內容涵蓋 BPR 定義、推力近似式、理想推進效率、整體效率與設計取捨。
- 新增航空小知識搜尋，可跨中英日名稱、內容、縮寫與公式搜尋；選擇結果會平滑定位到對應場景並開啟解說。
- 將方向鍵、Enter、Esc 的下拉選單操作集中在 `js/ui.js`，套用既有的航空公司、機場、距離計算與新增知識搜尋；以 capture 階段攔截 Enter／Esc，避免既有標籤輸入的 Enter 邏輯重複選取。
- 全站隱藏原生捲軸軸線，但保留滑鼠滾輪、觸控拖曳、鍵盤與程式捲動。
- 新增 `tools/check_knowledge.py`；已通過 JSON／三語完整性、JavaScript 語法、快取版本與本機 HTTP smoke test。資源版本升為 v=134，Service Worker cache 升為 `hangar-v4`。
- 此批變更尚未 commit 或 push；本機伺服器已啟動於 `http://localhost:8000`。
- 使用者要求先維持本機檢查；已確認 `knowledge.html` 本機回應正常，後續須待明確指示才可 commit／push。
- 修正舊本機草稿覆蓋知識三語欄位時可能只留下日文的問題：`mergedTopic()` 現在逐語言合併 `name`／`summary`／`fact`。搜尋與側邊節點選取改為等待轉盤完成置中後才開啟詳情，確保選取節點先轉到正面。`knowledge.js` 升為 v=135；未推送。
- 搜尋與側邊節點選取現在也會平滑捲動頁面，將對應知識區塊帶到視窗中央；`knowledge.js` 升為 v=136，僅本機。
- 共用「回到頂端」改為逐幀緩動捲動，不再依賴可能被瀏覽器縮短的原生 smooth 動畫；所有載入 `ui.js` 的頁面已改用 v=137，本機待檢查。
- 核對首頁與知識資料檔：正式清單均為 45 筆，原本已由 `knowledge.topics.length` 動態顯示。首頁現在也合併本機尚未發布的 `hangar_knowledge_custom` 條目並監聽跨分頁更新，確保自行新增後首頁圖卡仍與清單一致；`index.html` 資源版本升為 v=138，僅本機。

### 貨運／快遞航空分類（本機待確認）

- 新增航空公司 `tier: "cargo"`，在清單篩選、詳情標籤、編輯表單與中／英／日介面均可使用；目前共有 18 筆貨運／快遞條目。
- 新增／補強 FedEx Express、UPS Airlines、ASL Airlines Belgium（前 TNT Airways）、European Air Transport Leipzig、DHL Air UK、Air Hong Kong、Cargolux、Atlas Air，以及 USPS 航空郵件網路。USPS 明確標示為委託航空運能的郵政事業，未虛構 ICAO／IATA 或自有機隊。
- 補入 `data/airline_geo.json` 的樞紐／航線座標，FedEx 的 5 個樞紐與 3 個代表目的地已本機驗證可連到機場頁；貨運條目搜尋亦納入三語簡介，輸入 `TNT` 可找到 ASL Airlines Belgium。
- 可核對的時點資料：UPS 2026-03-31 官方機隊表（272 架）、FedEx FY26 公開值（約 700 架）、DHL EAT 官方介紹（35 架）、Air Hong Kong 2025 DHL 公告（14 架 A330）、Cargolux 官方機隊頁（30 架 747）、Atlas 2025 資料（113 架）、ASL 官方機隊介紹。日期敏感的機隊數均在條目簡介中標註來源時點或變動性。
- 新增 `tools/update_cargo_airlines.py` 作為可重跑的標準庫更新與完整性檢查；已通過 JSON、JavaScript 語法、篩選、搜尋、詳細資訊與機場連結測試。相關資料 fetch 升為 v=139。
- 本機預覽已開啟於 `http://localhost:8000/airlines.html`，目前選定「貨運／快遞航空」篩選並開啟 FedEx 詳情；尚未 commit、未 push。
- 已再次核對首頁：`data/airlines.json` 與航空公司頁均為 594 筆，首頁透過同一份 `data/airlines.json?v=139` 動態讀取，實際本機渲染為 `594 AIRLINES`；數字已對齊，未推送。
- 貨運分類數量比對：本次實際新增 8 家（FedEx Express、UPS Airlines、ASL Airlines Belgium、DHL Air UK、European Air Transport Leipzig、Air Hong Kong、Cargolux、USPS）。18 家貨運／快遞分類 = 8 家新資料 + 原有 9 家名稱含 Cargo 的資料 + 原有 Atlas Air；Atlas Air 本次僅補強並改列 `cargo`，不是新增公司。
- 使用者已同意發布目前本機改動；發布前已通過 `check_knowledge.py`、貨運資料完整性檢查、四份前端 JavaScript 語法檢查與 `git diff --check`。推送前發現遠端已有站內編輯器寫入的機場／航空公司資料，已以遠端最新版重建貨運集合並完成 rebase；`data/korean_airlines_debug.json` 維持未追蹤並排除於提交外。

### 737-800 / A320 實機部位辨識比較（本機待確認）

- 沿用 `data/<id>.json` 的 `parts.images`，沒有另建重複的比較圖片資料庫；同一張部位照片會同時供單一機型檢視器與 Boeing / Airbus 比較頁使用。
- Boeing 737-800 與 Airbus A320 各新增 9 個辨識類別：整體外型、駕駛艙、機身／艙門、引擎、翼尖小翼、主翼、垂直尾翼、水平尾翼、起落架；共 18 張不同的實機照片與三語圖說／辨識重點。
- 照片均下載自 Wikimedia Commons，不含 AI 生成或繪圖；本機檔案置於 `assets/reference/{b738,a320}/`，原始頁、作者與授權完整記錄於 `assets/reference/ATTRIBUTION.md`，各圖片資料也保留 `source` 連結。
- `viewer.js` 支援沒有對應 3D 網格的照片節點，因此「整體外型」與「翼尖小翼」仍可從下方部位列選取、深連結與鍵盤導覽；有 3D 網格的部位維持點擊高亮並同步顯示照片。
- `versus.js` 比較順序擴充為 9 類，會呈現所有部位照片、外型辨識重點、設計說明、來源授權與回到單一機型部位頁的連結。
- 機型編輯器補上多語物件的中文欄位相容與圖片來源／授權網址欄位，避免既有 `{zh,en,ja}` 值顯示為 `[object Object]`，也方便後續補真實照片來源。
- 新增可重跑工具 `tools/download_reference_photos.ps1` 與 `tools/update_aircraft_reference_images.py`；後者會檢查 2 架 × 9 部位、三語圖說、來源網址與本機檔案是否齊全。
- 已通過 Python 自我檢查、4 份 JavaScript 語法檢查、JSON 解析、18 張圖片尺寸／檔案檢查、`git diff --check` 與本地瀏覽器互動驗證。比較頁實測 9 列、18 張照片、18 組辨識重點、18 個來源連結；單機頁實測引擎與翼尖節點均能一次點選後顯示正確照片。
- 本地中文預覽已開啟：`http://localhost:8000/versus.html?a=b738&b=a320&local=142`。目前未 commit、未 push，等待使用者檢查。
- 尚未批次擴充其餘 50 架機型；應依家族逐批找可確認機型與授權的實機照片，避免大量自動配圖造成錯型或授權錯誤。

### 駕駛艙外窗辨識補充（2026-08-25，本機待確認）

- 依使用者附圖需求，將「駕駛艙外窗」從駕駛艙內部布局拆成獨立比較類別；附圖僅作需求示意，未直接收錄未知來源圖片。
- Boeing 737-800 與 Airbus A320 各新增正面、側面兩張實機窗型照片；均由 Wikimedia Commons 授權照片裁切，不含 AI 生成或繪圖，裁切與來源／作者／授權已記錄於 `assets/reference/ATTRIBUTION.md`。
- 新增三語辨識說明，重點比較正面風擋高寬比、中央接縫、外側窗收尖方向、窗框折角，以及窗帶如何包覆機鼻；並明確提醒不能只靠窗片數判型。
- 比較頁順序擴充為 10 類；「駕駛艙外窗」列會同時顯示正面與側面照片，單一機型頁也能以獨立照片節點開啟兩張圖。
- 照片下載／資料更新工具已擴充並通過自我檢查：2 架 × 10 類、共 22 張照片；資料 fetch 與檢視器／比較頁資源升為 v=142。尚未 commit、未 push。
- 本地瀏覽器已驗證比較頁共 10 列，「駕駛艙外窗」列含 4 張照片、4 個來源連結與兩組三語辨識重點；單一 737-800 頁以 `?part=windshield` 開啟時會選中外窗節點並顯示正面／側面兩圖。無破圖，中文預覽停留在外窗比較列供使用者檢查。
- 使用者已確認目前樣式並同意先發布；本批將提交 737-800／A320 的 10 類實機辨識比較，再以相同格式於本機繼續製作 777-300／A350-900。
