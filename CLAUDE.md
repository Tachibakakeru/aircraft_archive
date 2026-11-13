# SKY ARCHIVE — Claude Code 作業說明

完整專案作業地圖見 `AGENTS.md`；本檔與 `AGENTS.md` 的新增段落保持同步。

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

- 每次回答都要即時更新本檔，條目標題或內容附日期與時間（YYYY-MM-DD HH:MM）；回答結尾條列本輪改動。`AGENTS.md` 與 `CLAUDE.md` 的新增段落保持同步。
