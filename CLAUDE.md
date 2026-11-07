# SKY ARCHIVE — Claude Code 作業說明

完整專案作業地圖見 `AGENTS.md`；本檔與 `AGENTS.md` 的新增段落保持同步。

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
