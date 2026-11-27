# SKY ARCHIVE — Claude Code 作業說明

完整專案作業地圖見 `AGENTS.md`；本檔與 `AGENTS.md` 的新增段落保持同步。

## Antonov 與 C-5 家族（2026-11-27）

- 飛行圖鑑收錄 Antonov 歷史型錄的 23 個主要動力機型，以及 Lockheed C-5A／B／C／M。安特諾夫各設計支系及 C-5 主要改型在機型家族頁可直接點開詳情。以機型頁的來源及次型號條件為準，C-5C 的 1989 財政年度是交付時間。
- 本輪新增 26 個純資料條目。圖鑑共 210 個機型，50 個有 3D、160 個待補。使用 `python tools/check_model_inventory.py` 重建盤點。

## Blender 補建飛機模型備忘（2026-11-16）

- 協和號、Dreamlifter、A321neo 的可編輯來源在 `models/blender/`。可攜檔在 `models/glb/`，由 `tools/export_blender_glb.py` 從對應的 `.blend` 重建，保留分件、材質與一段示範動畫。若更新其中一架的來源，對應 GLB 與站內 JSON 一併重匯出。
- 獨立引擎轉子沿用 v2 `surfaces[]` 樞紐，`rpm` 為展示轉速。短艙和風道保持固定，Blender 與 GLB 示範時間軸需保留可動轉子。
- 預覽驗證只用 Codex 的內建網頁分頁，沿用既有的本機預覽。使用者要求停止擷取 Windows 桌面或操作其桌面視窗。
- 舵面驗收同時檢查滑桿數值與模型實際轉角。`Surface.hinged()` 接收弧度，呼叫端以 `rad()` 轉換度數。A321neo v3 的五個副翼、升降舵及方向舵鉸鏈均有角度回歸檢查。
- 現行範例：Dreamlifter 與 A321neo Cabin Flex／LEAP-1A 以 `surfaces[].motion` 安排輪艙門先打開、輪組移動、門再關閉。`tools/check_gear_clearance_blender.py` 在兩架的 `.blend` 抽樣 401 個姿態檢查門與輪組；A321neo v2 同時檢查輪胎對外殼、襟翼對滑軌整流罩的干涉，以及收輪後輪胎是否露出腹部。官方參考、重建指令與展示近似事項見 `models/blender/README.md`。

- 來源：[arjun988/blender-skills](https://github.com/arjun988/blender-skills/tree/904f095d8f36a6e72adaebb08d07f884a074743d)（MIT，已核對此版）。開始補建缺少的機型、重做外型或調整可動部位時，先從 `data/model_inventory.json` 確認缺模，讀本節與 `models/blender/README.md`，按任務查上游對應技能。本節已整理成可直接採用的流程。
- **比例先行｜`blender-director` 的 [reference-image-match](https://github.com/arjun988/blender-skills/blob/904f095d8f36a6e72adaebb08d07f884a074743d/.claude/skills/references/reference-image-match.md)、`vehicle-artist`**：確認實際次型號，優先用原廠尺寸、三視圖及多角度實拍。以公尺建立機身站位，先對準翼展、機鼻、翼根、垂尾、引擎和接地姿態，再做細節。以正投影側／頂／正面比比例，以同角度斜視照片核對曲面；先校正視角，再判斷形狀誤差。標記資料不足的部位與示意尺寸。
- **幾何與材質｜`hard-surface`、`asset-optimization`，有貼圖時再用 `uv-workflow`／`materials`**：分開機身、玻璃、短艙、輪組與各可動面。沿用協和號與 Dreamlifter 的截面放樣和對稱產生方法；左右動作有差異時分開處理。接縫、門框和整流罩以版型特徵及可辨識度決定細節量。只簡化不影響輪廓、部位點選或鉸鏈的網格，檢查退化面、非預期開口、法線、三角面數、材質數與匯出大小。
- **機械動作｜`rigging`、`animation`**：用 Empty、局部旋轉軸及父子鉸鏈表示組件，對應站內 `surfaces[].parent`、`start`、`e[].slide`／`slideEnd`。依可查證的機構設定方向與先後順序；輪艙門只在輪組有足夠淨空時讓輪組進出。逐段檢查端點與多個中途姿態，尤其在輪艙門與起落架交會時；示意角度明確標註。
- **匯出與驗收｜`export-pipeline`、`qa-review`**：優先沿用本機 Blender 背景模式與現有 Python 建模腳本，保留可編輯的 `.blend`，交付原生 v2 JSON、縮圖與剪影並更新圖鑑索引及盤點。Blender 使用公尺、機鼻 +X、Z 向上；網站為機鼻 +X、Y 向上、機長正規化為 12。除檢查比例、接地、索引及鉸鏈外，須在原本機預覽分頁檢查多角度成品、部位點選、滑桿全行程及適用的起飛示範。上游遊戲引擎／FBX 設定不直接套用；MCP 有可用連線時可輔助預覽，現有建模管線可獨立執行。

## UI／動畫 Skills（2026-11-07 17:31 新增）

- 來源為 [emilkowalski/skills](https://github.com/emilkowalski/skills)（MIT）與 `modern-web-guidance`（見表）。專案安裝記錄在 `skills-lock.json`，更新專案技能用 `npx skills@latest update -p`。
- 在此專案的 Codex 或 Claude Code 對話中，直接寫「用 `技能名稱` 檢查／修正某個頁面，交付某種結果」。已安裝的技能也可由代理依任務選用。Codex 可讀 `.agents/skills/<名稱>/SKILL.md`，Claude Code 可讀 `.claude/skills/<名稱>/SKILL.md`。

| Skill | 用途 | 本專案適用處 |
|---|---|---|
| `emil-design-eng` | 介面細節與動畫決策總原則 | 全站緩動曲線、時長、陰影 |
| `improve-animations` | 全站動畫稽核，產出 `plans/NNN-*.md` 實作計畫（本身不改程式） | 定期稽核 CSS／JS 動畫 |
| `animation-performance` | 掉幀診斷、只動 transform／opacity | 3D 檢視器、地球儀、機場頁大檔載入時的動畫 |
| `choreograph` | 多元素進場順序與時間差 | 換頁過場、首頁區塊進場、翻牌看板 |
| `mobile-native` | 讓網頁在手機上更像原生 App | PWA、安全區域、觸控 hover |
| `break-ui` | 用極端資料壓力測試版面 | 超長機場名、空搜尋結果、594 家航空公司列表 |
| `modern-web-guidance` | Chrome／Edge／Firefox／MDN 維護的現代網頁寫法指引（2026-11-14 新增，來源 [GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance)，Apache-2.0） | 改 HTML／CSS／前端 JS 前查最新寫法；`npx -y modern-web-guidance@latest legacy-scan .` 掃過時寫法 |

- 稽核範例：「用 `improve-animations quick` 檢查全站動畫，先列優先順序」或「用 `improve-animations plan` 為跑道進度條寫一份效能改善計畫」。計畫放在 `plans/`，`plans/README.md` 為總表。要改程式時，可另請代理依指定計畫實作。2026-11-07 的首次稽核記在 `Progress.md`。
- 單點任務範例：「用 `animation-performance` 診斷機場頁載入時的掉幀」；「用 `choreograph` 安排首頁看板的進場順序」；「用 `mobile-native` 檢查 iPhone 點擊後的 hover 殘留」；「用 `break-ui` 在本機預覽測試超長機場名和空結果，先列問題」；「用 `emil-design-eng` 評估搜尋面板的開關速度」。
- 套用技能時以本專案既有決定為準。首頁航線、換頁過場、翻頁時鐘與翻牌看板在 reduced-motion 下照常播放。過場保留既定的 0.9／1.0 秒及 `--tx-ease`，跑道起飛與翻牌下落沿用現有 ease-in。詳見 `AGENTS.md` 的共用核心說明。
- `.claude/skills/` 與 `.agents/skills/` 已列入 `.gitignore`，Git 只追蹤 `skills-lock.json`。可在專案根目錄用 `npx skills list` 查看安裝狀態。換電腦時用 `npx skills experimental_install --frozen-lockfile` 從鎖定檔還原至 `.agents/skills/` 並驗證內容雜湊。Claude Code 若需要自己的安裝目錄，可用 `npx skills@latest add emilkowalski/skills -s <名稱> -a claude-code --copy -y`，並檢查這次安裝是否更新鎖定檔。詳見 [Skills CLI 指令文件](https://github.com/vercel-labs/skills/blob/main/docs/commands.md)。

## 持續紀錄規則（2026-11-14 新增）

- 每次回答都要即時更新 `Progress.md`，條目標題或內容附日期與時間（YYYY-MM-DD HH:MM）；回答結尾條列本輪改動。`AGENTS.md` 與 `CLAUDE.md` 的新增段落保持同步。

- An-225 可動版的來源、授權、重建與限制見 models/blender/README.md。tools/build_an225.py 轉換指定版本的 FlightGear 機模，tools/build_an225_blender.py 同步產生可編輯 Blender 與 GLB。改動後執行 check_an225_model.py 與 check_an225_clearance_blender.py 檢查機體尺寸、裝載接地與輪胎對艙門的淨空。
