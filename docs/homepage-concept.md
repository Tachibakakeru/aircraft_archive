# 首頁新 UI 概念稿：設計紀錄與交接說明

> 給後續 session 的交接文件。說明 `home-concept.html` 的來由、設計想法、實作細節、驗證結果，以及正式採用前要做的事。
> 建立日期：2026-11-03。
> **狀態更新（2026-11-03）：使用者要求「套用到正式首頁」，已正式採用。** 概念頁 `home-concept.html` 已刪除，內容拆成 `index.html`＋`css/home.css`＋`js/home.js`，字串併入 `js/i18n.js` 的 `home.*`。第 1～8 節保留概念階段的想法與紀錄；正式套用的實際做法見第 11 節。

---

## 1. 需求來源

使用者原話：

> 首頁的 UI 幫我構思怎麼樣才可以不要這麼死板，包含文字的搭配，選項的使用等等……你先構想一個完整的新 UI 給我看，我再決定要不要使用，要跟航空有關，盡量使用亮色的藍色系。

整理後的要求：

| 要求 | 對應做法 |
|---|---|
| 不要死板 | 捨棄「置中標題＋四張相同卡片」，改成有敘事順序的長頁面，加入能互動、會變化的區塊 |
| 文字搭配 | 標題改成提問句，描述改用具體例子與數字，各區塊用航空情境的口吻 |
| 選項的使用 | 加入全站搜尋（含分類單選）、熱門航點、出發看板、工具入口，讓首頁本身就能操作 |
| 跟航空有關 | 整頁以「出境大廳」為主題：訂票表單、登機證、翻牌出發看板、機長廣播、METAR |
| 亮色藍色系 | 淺色主題以飽和天空藍為主；深色主題也維持藍色系（夜航） |
| 先給我看再決定 | 另開獨立檔案，不動 `index.html`；另發布 Artifact 預覽 |

## 2. 原本首頁的問題（改版前診斷）

原 `index.html`（87 行）與 `css/home.css`：

- 全部置中，只有大標題、副標題、2×2 四張相同樣式的卡片、頁尾一行字。
- 卡片用 emoji（✈️🛬🏢💡）當圖示，四張只有文字不同，缺乏層次。
- 文案偏公式化：「歡迎光臨天空檔案」「選擇要探索的資料庫」。
- 首頁本身沒有可操作的東西；要找特定機場或機型，得先進到子頁面再搜尋。
- 機型比較、Boeing/Airbus 對照、機型家族、距離計算等工具在首頁看不到。
- 色彩沿用全站深色琥珀色系（`--amber`），與「亮藍」的需求不符。

## 3. 設計概念：出境大廳

整頁依旅客的動線排列，每個區塊都借用一個真實的航空物件：

```
天空主視覺（頂部導覽＋標題＋訂票式搜尋＋熱門航點 ｜ 航線示意動畫）
   ↓
選擇登機門：四張登機證（Gate A–D = 四個資料庫）
   ↓
最近看過的機型（有瀏覽紀錄才顯示）
   ↓
今日出發：翻牌出發看板 ｜ 機長廣播（小知識）
   ↓
機上工具：比較／Boeing 對 Airbus／機型家族／航線距離
   ↓
METAR 格式的資料庫狀態頁尾
```

選擇這些物件的理由：

- **訂票表單**：每個人都用過，「出發 → 目的地」的格式一看就懂是搜尋框。
- **登機證**：天然有「目的地代碼、登機門、座位、條碼、撕線存根」等欄位，剛好可以放各資料庫的名稱、數字和入口按鈕；又能讓四個入口外觀一致但不呆板。
- **翻牌出發看板**：機場最有代表性的動態元素，適合做「每日推薦」，翻牌動畫是整頁主要的動態亮點。
- **機長廣播**：把小知識包裝成廣播口吻，讓知識內容有個人味。
- **METAR**：航空天氣報告是只有這個主題才有的格式，用來呈現資料庫數量，是給航空迷的小彩蛋，下方附白話解讀。

刻意避免的東西：emoji 當圖示、所有卡片同一個圓角陰影、紫藍漸層 hero、Inter／Space Grotesk 這類通用字體、無意義的 01／02／03 編號。

## 4. 視覺系統

### 4.1 色彩 token（寫在 `home-concept.html` 的 `:root`）

淺色（預設）：

| Token | 值 | 用途 |
|---|---|---|
| `--bg` | `#eef6ff` | 頁面底色，淡天空藍 |
| `--bg-2` | `#e2efff` | 次要底色（METAR、補充說明框） |
| `--card` | `#ffffff` | 卡片、登機證、搜尋框 |
| `--ink` | `#0b2a55` | 主文字，深海軍藍 |
| `--muted` | `#4f6d96` | 次要文字 |
| `--line` | `#cde0f7` | 分隔線 |
| `--azure` | `#1a73f0` | 主色（按鈕、連結、Gate A） |
| `--cyan` | `#0b9fd0` | Gate B 機場 |
| `--indigo` | `#3456e6` | Gate C 航空公司 |
| `--teal` | `#0e8fb0` | Gate D 小知識 |
| `--sky-1/2/3` | `#0f5fd0` → `#2f8cf5` → `#5aa9fb` | Hero 天空漸層 |
| `--board-*` | 深海軍藍底＋淡藍字 | 出發看板（兩種主題都是深色面板） |

深色主題用同一組 token 名稱重新定義（夜航：`--bg:#061730`、`--azure:#4ea4ff` 等），並開啟 `--stars:1` 顯示星點。四個資料庫的強調色都在藍色範圍內（藍／青／靛／藍綠），以色相微差區分。

主題切換有三種狀態，CSS 都已涵蓋：
- 有 `data-theme="dark"` 或 `"light"`：依使用者選擇。
- 沒有 `data-theme`：依 `prefers-color-scheme`。
- 主題鍵沿用全站的 `localStorage.hangar_theme`，所以和其他頁面同步。

> 註：Hero 底部原本漸層到很淡的藍，白字與玻璃面板對比不足；第一次截圖後已把 `--sky-3` 調深為 `#5aa9fb`，再用 `.sky::after` 另做一段漸層接到頁面底色。

### 4.2 字體

| 角色 | 字體 | 用途 |
|---|---|---|
| Display | Barlow Condensed（中文回退 Noto Sans TC） | 標題、機場代碼、登機門字母、數字。窄體字接近機場指標與航班看板的字感 |
| Body | Noto Sans TC | 內文，三語都能顯示 |
| Utility | IBM Plex Mono | 小標籤、時間、METAR、提示文字 |

字體由 Google Fonts 載入。**這是新的外部依賴**，正式採用前要讓使用者決定接受或改用系統字體。

### 4.3 其他規則

- 依 `AGENTS.md`：全頁隱藏原生捲軸，滾輪、觸控、鍵盤仍可捲動。
- 有 `prefers-reduced-motion` 時關閉所有動畫：飛機固定在航線 62% 處，看板不翻牌。
- 左右邊距使用 `max(20px, env(safe-area-inset-*))`，可在手機瀏海與系統列旁正常顯示。
- 斷點：980px（hero 改單欄、隱藏頂部導覽文字連結）、760px（登機證單欄、看板隱藏時間與登機門欄）、520px（搜尋框隱藏「出發」欄、登機證存根縮窄）。

## 5. 各區塊細節

### 5.1 頂部導覽
- 自繪 SVG 標誌（圓框＋虛線航跡＋飛機），「SKY ARCHIVE／天空檔案」，旁邊一個「概念稿」小標籤（正式採用時移除）。
- 四個資料庫文字連結；語言切換改成三段式按鈕（繁中／EN／日本語），不是原本的循環按鈕；主題切換為太陽圖示。

### 5.2 Hero 與文案
| 語言 | 標題 | 副標 |
|---|---|---|
| 繁中 | 今天，<br>想往哪裡飛？ | 機型、機場、航空公司與飛航知識都在這裡。輸入一個代碼，就能起飛。 |
| EN | Where are we<br>flying today? | Aircraft, airports, airlines and flight know-how in one place. Type a code and take off. |
| 日本語 | 今日は、<br>どこへ飛びますか？ | 機種、空港、航空会社、そして飛行の知識をひとつに。コードを入れれば、すぐに離陸。 |

標題用 `\n`＋`white-space:pre-line` 手動斷行，因為自動斷行曾出現「今天，想／往哪裡飛？」這種不自然的切法。

### 5.3 訂票式全站搜尋
- 版面：`出發：天空檔案` ✈ `目的地：[輸入框]` `[搜尋]`。
- 分類單選（`role="radiogroup"`）：全部／機型／機場／航空公司／知識；左右方向鍵可切換；每個分類有自己的 placeholder 範例。
- 資料來源與連結：

| 類別 | 資料 | 比對欄位 | 連結 |
|---|---|---|---|
| 機型 | `data/fleet.json` | `icao`、`id`、去掉 Airbus/Boeing 前綴的名稱、`name`、`manufacturer` | `viewer.html?model=<id>` |
| 機場 | `data/airport_codes.json`（約 1.9 MB，**第一次 focus 才載入**），依 `id` 合併 IATA/ICAO 兩個 key | 所有代碼、`name`、`city`；熱門機場另有中日文別名 | `airports.html?icao=<id>` |
| 航空公司 | `data/airlines.json` | `icao`、`iata`、`callsign`、`name`、`nameZh`、`nameJa` | `airlines.html?id=<id>` |
| 知識 | `data/knowledge.json`＋本機 `hangar_knowledge_custom` | `id`、三語 `name` | `knowledge.html`（**目前無法直接開單一條目**） |

- 評分（`score()`）：代碼完全相符 100 → 代碼開頭相符 80 → 名稱開頭相符 60 → 名稱中某個詞開頭相符 55 → 名稱包含 40。有 `tier` 的航空公司加 3 分（讓主流公司排在已停飛的舊公司前面）。
- 「全部」時每類最多 4 筆，單一分類最多 10 筆；**分類依該類最高分排序**（例如輸入 `EVA`，長榮航空排在 EVAD 等機場前面）。
- 「詞開頭 55 分」是為了修正 `v1` 先命中「Van's RV-10」（`rv10` 包含 `v1`）的問題，現在會先出現「起飛速度 V1/VR/V2」。
- 鍵盤：↑↓ 移動、Enter 前往目前項目（或第一筆）、Esc 關閉；使用 `aria-activedescendant`。正式站的 `js/ui.js` 已集中處理下拉鍵盤操作，採用時可以考慮改用它。
- 下拉選單原本被 `.sky` 的 `overflow:hidden` 裁切，已改成只裁切裝飾層 `.sky-bg`，`.sky` 本身設 `z-index:2`，讓選單蓋在下方區塊之上。

### 5.4 熱門航點 chips
`RCTP 桃園`、`RJTT 羽田`、`A350`、`EVA 長榮航空`、`CAVOK`、`V1`。點擊會切換到對應分類、填入關鍵字並直接搜尋，也同時示範搜尋框的用法。

### 5.5 航線示意（hero 右側）
- SVG 曲線航跡＋經緯線；飛機沿 `getPointAtLength()` 移動並依切線旋轉；已飛段為實線，未飛段為虛線。
- 每圈 9 秒、停 1.4 秒後換下一個目的地（`POPULAR` 清單，16 座熱門機場，座標內建，所以不必為此載入 1.9 MB 的代碼表）。
- 下方四格讀數：目的地、**大圓距離**（haversine）、預估航時（距離 ÷ 830 km/h ＋ 30 分鐘）、巡航高度（依距離給 FL280／350／370／390）。這些是示意估算，圖說有寫明距離的計算方式。

### 5.6 登機證（Gate A–D）
每張證件的欄位：

| Gate | 目的地代碼 | 三個欄位 | 描述（繁中） |
|---|---|---|---|
| A 飛行器圖鑑 | ACF | 機型／3D 模型／待補模型 | 從 A220 到協和號，翻開 {n} 個機型；其中 {m} 架可以直接 360° 轉著看。 |
| B 機場與跑道 | APT | 機場／代碼 ICAO·IATA／檢視 衛星圖 | {n} 座機場，跑道長度、方位與衛星圖一次看齊。用 ICAO 或 IATA 代碼直接找。 |
| C 全球航空公司 | ALN | 航空公司／貨運快遞／三大聯盟 | {n} 家航空公司的呼號、機隊與樞紐，還能把航線畫在地球上。 |
| D 航空小知識 | KNW | 主題／互動場景 4／語言 3 | CAVOK 是什麼？為什麼過了 V1 就不能停？{n} 個主題，在座艙場景裡點一點就懂。 |

- 數字全部即時計算：3D 數＝`fleet.json` 中縮圖不是 `nomodel` 的機型；貨運數＝`tier === "cargo"`；聯盟數**只計 star／oneworld／skyteam**（資料中還有 `none`、`value`、`ufly`，第一次截圖曾誤顯示 6）。
- 讀不到資料時改用後備數字（184／48／85,587／594／18／3／82），頁面不會出現空白。
- 撕線存根：右側虛線分隔，上下兩個與頁面底色相同的圓形做出缺口效果；存根有登機門號、座位、條碼（CSS 漸層畫的）和「登機 →」。
- Hover：證件上浮，路線上的小飛機從左滑到右。

### 5.7 最近看過
讀取 `viewer.js` 已在寫的 `localStorage.hangar_recent`，顯示最多 8 個機型縮圖 chip；沒有紀錄時整個區塊隱藏。

### 5.8 出發看板
- 每日固定一組推薦（以日期 `YYYYMMDD` 當亂數種子），「換一批」會換種子。
- 每組 6 列：3D 機型、熱門機場、航空公司（限 mainline／lcc／cargo／regional）、知識、任一機型、熱門機場。
- 欄位：時間（現在時間往後每 5～15 分鐘）、班次（機型 ICAO／機場 IATA／航空公司代碼＋隨機班號／知識 ID）、目的地（名稱＋類別與補充資訊）、登機門（A–D＋號碼）、狀態（3D 可看／規格齊全／準時／登機中閃爍／新知）。
- 班次欄是 7 格翻牌字元；換一批時每格先跑隨機字元再停在正確字元，逐列錯開。
- 看板在淺色與深色主題都是深藍面板，模擬真實機場看板。

### 5.9 機長廣播
- 依當地時間問候（早安 <11 時、午安 <18 時、晚安），接「今天想跟大家聊聊：」＋知識標題、摘要、補充（`fact`）。
- 「換一則」切換條目；「看完整解說」連到 `knowledge.html`。
- 有 `aria-live="polite"`。

### 5.10 機上工具
四個線條 SVG 圖示的工具卡：`compare.html` 機型比較、`versus.html` Boeing 對 Airbus、`variants.html` 機型家族、`distance.html` 航線距離。原首頁沒有這些入口。

### 5.11 METAR 頁尾
範例：`METAR SKYA 031601Z AC184/483D AP85587 AL594 KN82 CAVOK Q1013 NOSIG`
下方附白話：「解讀：184 個機型（48 個 3D）、85,587 座機場、594 家航空公司、82 個知識主題。能見度良好，全部資料庫可正常起降。」時間戳用 UTC 的 日時分＋Z。

### 5.12 預覽模式
頁面載入時對 `fleet.html` 發 HEAD 請求；若不存在（例如在 Artifact 裡單獨預覽），站內連結改成顯示提示「概念預覽：正式套用後，這裡會前往『…』」，不會跳到 404。在正式站或 `server.py` 下會正常跳頁。

## 6. 檔案與技術說明

| 檔案 | 說明 |
|---|---|
| `home-concept.html` | 單一檔案（約 1,000 行），CSS、JS、三語字串都寫在裡面，不依賴 `css/style.css`、`js/i18n.js`、`js/theme.js` |
| `docs/homepage-concept.md` | 本文件 |
| `Progress.md` | 已新增「首頁新 UI 概念稿」紀錄 |

- 資料 fetch 使用和 `index.html` 相同的版本鍵（fleet `v=182`、airlines `v=139`、airport_count `v=138`、knowledge `v=192`、airport_codes `v=138`）；若帶版本鍵的請求失敗會改試不帶版本鍵的路徑（`getJSON()`）。
- 語言鍵沿用 `localStorage.hangar_lang`，主題鍵沿用 `hangar_theme`；所有 localStorage 讀寫都包在 try/catch 中。
- 概念頁沒有載入 `theme.js`，所以不會註冊 Service Worker；也沒有改 `sw.js`。
- 三語字串集中在檔案內的 `STR` 物件，key 命名大致對應未來要加入 `i18n.js` 的鍵。

## 7. 驗證紀錄

在本機 `python server.py` 下用 Playwright 測試：

- 桌面 1360px 淺色、桌面深色、手機 390px：`scrollWidth - innerWidth = 0`，沒有橫向溢出；沒有 console 錯誤或 page error。
- 搜尋：`eva` 第一筆是 EVA Air；`羽田` 找到 HND／RJTT；`v1` 第一筆是「Takeoff Speeds: V1 / VR / V2」。
- 繁中深色主題截圖確認：標題斷行、下拉選單沒被裁切、登機證缺口顏色正確。

第一次截圖後修正的問題（已全部處理）：
1. 搜尋下拉被 hero 裁切。
2. 下拉中名稱與副標黏在同一行。
3. 分類固定順序，導致 `eva` 先列出機場。
4. `v1` 命中 RV-10。
5. 聯盟數顯示 6。
6. 英文的彎引號（’）在 Noto Sans TC 中是全形，造成 `can’ t` 的空隙，已改為直引號；英文問候與「Today's topic」之間補空格。
7. hero 下半部太淡，白字對比不足。
8. 手機上「日本語」按鈕換行。

## 8. 預覽位置

- Artifact（私人，只有擁有者能開）：https://claude.ai/artifact/XRnht3NarATR1KHbxQ53yQ
  內含 `data/fleet.json`、`airlines.json`、`airport_count.json`、`knowledge.json`、`airport_codes.json`、`assets/icon.svg`，搜尋可用真實資料；站內連結為預覽模式。
- 本機：`python server.py` → `http://localhost:8000/home-concept.html`（連結可正常跳頁）。

## 9. 若決定採用：建議步驟

1. 先問使用者要保留或調整哪些區塊（色調、登機證樣式、文案語氣、是否要出發看板與機長廣播）。
2. 決定字體：接受 Google Fonts，或改回全站的系統字體堆疊（`--sans`、`--mono`）。
3. 把 `STR` 的三語字串搬進 `js/i18n.js`（三種語言都要加，`AGENTS.md` 規定），頁面改用 `I18N.t()`、`I18N.field()`、`I18N.apply()`。
4. 以概念頁內容取代 `index.html`；CSS 拆到 `css/home.css`（或新檔），色彩 token 的命名要和 `css/style.css` 協調。注意全站目前預設偏深色琥珀，首頁改亮藍後，要確認其他頁面的視覺是否也需要跟進，或接受首頁獨立風格。
5. 恢復載入 `js/theme.js`（Service Worker 註冊、回機隊時保留搜尋條件）。
6. 搜尋下拉改用 `js/ui.js` 的共用鍵盤操作，避免重複實作。
7. 補小知識深連結：在 `js/knowledge.js` 支援 `knowledge.html?topic=<id>`（轉到該節點並開啟詳情），再讓首頁搜尋、看板、機長廣播連過去。
8. 更新所有受影響資源的 `?v=N`，並更新 `sw.js` 的 `CACHE` 名稱。
9. 移除導覽列的「概念稿」標籤與預覽模式程式（或保留但無害）。
10. 刪除或保留 `home-concept.html`（建議採用後刪除，避免兩份首頁）。
11. 依 `AGENTS.md`：先在本機給使用者檢查，**使用者明確同意後才 push 到 `main`**；更新 `Progress.md`。

## 10. 未解事項

- 使用者尚未決定是否採用，也還沒給任何修改意見。
- 小知識沒有單一條目的深連結。
- Google Fonts 外部依賴尚未確認。
- 出發看板的「時間、班號、登機門」是裝飾性的隨機值，不是真實航班；若使用者在意誤解，可改成更明確的「今日推薦」標示。
- 航線示意的航時與巡航高度是粗略估算，僅供視覺效果。

## 11. 正式套用紀錄（2026-11-03）

使用者看過 Artifact 預覽後要求「套用到正式首頁」。依第 9 節步驟處理：

| 項目 | 做法 |
|---|---|
| 頁面結構 | `index.html` 改為概念稿的版面；移除「概念稿」標籤與預覽模式（不再對 `fleet.html` 發 HEAD 請求、不再攔截連結）。 |
| 樣式 | 全部移到 `css/home.css`（首頁不載入 `css/style.css`，所以 token 名稱不會互相衝突）。 |
| 程式 | 移到 `js/home.js`；改用 `I18N.t("home.*")`、`I18N.field()`、`I18N.set()`、`HangarTheme.toggle()`；重新載入 `js/theme.js`（Service Worker 註冊、回機隊保留搜尋條件）。 |
| 三語字串 | 113 個 key／語言併入 `js/i18n.js`，全部在 `home.` 命名空間（例如 `home.hero.title`、`home.p.fleet.d`、`home.cat.weather`）；舊的 `home.title`、`home.fleet.desc` 等已移除（只有舊首頁使用）。帶變數的字串用 `{n}`、`{name}`，由 `home.js` 的 `t(k, vars)` 代入。 |
| 字體 | **不使用 Google Fonts**。Barlow Condensed（500/600/700）與 IBM Plex Mono（400/500/600）的拉丁子集 woff2 放在 `assets/fonts/`（共約 110 KB，SIL OFL 1.1，授權檔一併收錄，README 已註記）；中日文改用系統字體堆疊（PingFang TC → Noto Sans TC → Hiragino Sans → Microsoft JhengHei）。這樣不依賴外部服務，PWA 離線也能顯示。 |
| 小知識深連結 | `js/knowledge.js` 新增 `knowledge.html?topic=<id>`：資料載入後轉盤轉到該條目並開啟詳情（不在場景中的條目直接開詳情）。首頁搜尋、出發看板、機長廣播「看完整解說」都改連到條目。 |
| 搜尋鍵盤操作 | 仍由 `home.js` 自己處理（↑↓／Enter／Esc）。`js/ui.js` 的共用處理是以 mousedown 選取「選項按鈕」為前提，首頁搜尋結果是一般連結，硬套會讓 Enter 行為不一致，所以沒有改用；首頁也沒有載入 `ui.js`。 |
| 版本與快取 | `css/home.css`、`js/home.js`、首頁的 `js/i18n.js` 用 `v=193`；`knowledge.html` 的 `js/knowledge.js` 升為 `v=193`；`sw.js` 的 `CACHE` 由 `hangar-v49` 升為 `hangar-v50`。資料 fetch 的版本鍵沿用（fleet 182、airlines 139、airport_count／airport_codes 138、knowledge 192）。其他頁面仍引用舊版 `i18n.js?v=…`，它們不需要新的 `home.*` 字串，所以不受影響。 |
| 文件 | `AGENTS.md` 首頁與小知識列已更新；`README.md` 加字體授權；`Progress.md` 已記錄。 |

驗證（本機 `server.py`＋Playwright）：
- 繁中淺色、英文深色桌面 1360px、日文 390px 手機：無橫向溢出、無 console／page error；Barlow Condensed 確認已載入。
- 首頁搜尋 `cavok` 按 Enter → `knowledge.html?topic=cavok`，轉盤定位並開啟「CAVOK：雲與能見度良好」詳情。
- 語言切換會寫入 `hangar_lang`、更新 `<html lang>` 與全部文字；主題切換寫入 `hangar_theme`。
- 有 `hangar_recent` 紀錄時「最近看過的機型」正確顯示縮圖。
- 測試環境中只有小知識詳情的 Wikimedia 外部照片因沙盒網路無法載入，與本次改動無關。

Artifact 預覽（https://claude.ai/artifact/XRnht3NarATR1KHbxQ53yQ）仍是概念階段版本（含預覽模式與 Google Fonts），不會自動同步正式首頁。
