"use strict";
/* ═══════════════════════════════════════════════
   儲存層抽象 Storage Abstraction Layer
   ─────────────────────────────────────────────
   編輯器只依賴這個介面，不直接碰任何後端細節：
     Storage.save(id, dataObj)   → Promise<{ok, message}>
     Storage.mode()              → "github" | "download"
     Storage.isConfigured()      → bool（github 模式是否已設定）

   目前提供兩種後端：
     • GitHubStorage  —— 直接 commit 到 repo（方案 A）
     • DownloadStorage —— 匯出 JSON 檔（原本的方式，永遠可用的後備）

   ★ 未來升級到方案 C（後端伺服器）時，只要在此檔新增一個
     ServerStorage（save 內改成 fetch POST 到你的 API），
     並在 Storage 的選擇邏輯加一項即可——editor.js 完全不用改。
   ═══════════════════════════════════════════════ */

/* ---- 後端一：GitHub Contents API ---- */
const GitHubStorage = (() => {
  const CFG_KEY = "hangar_github_cfg";   // {owner, repo, branch, path, token}

  const getCfg = () => {
    try { return JSON.parse(localStorage.getItem(CFG_KEY) || "null"); }
    catch { return null; }
  };
  const setCfg = (cfg) => localStorage.setItem(CFG_KEY, JSON.stringify(cfg));
  const clearCfg = () => localStorage.removeItem(CFG_KEY);
  const isConfigured = () => {
    const c = getCfg();
    return !!(c && c.owner && c.repo && c.token);
  };

  // 取得檔案現有 sha（更新既有檔案時必填）
  async function getSha(cfg, filePath){
    const url = `https://api.github.com/repos/${cfg.owner}/${cfg.repo}/contents/${filePath}?ref=${cfg.branch||"main"}`;
    const res = await fetch(url, {
      headers: { Authorization: `Bearer ${cfg.token}`, Accept: "application/vnd.github+json" }
    });
    if (res.status === 200) return (await res.json()).sha;
    if (res.status === 404) return null;      // 檔案不存在→新建
    throw new Error(`讀取檔案狀態失敗（${res.status}）`);
  }

  // UTF-8 安全的 base64（GitHub 要求 content 為 base64）
  function toB64(str){
    return btoa(unescape(encodeURIComponent(str)));
  }

  async function save(id, dataObj){
    const cfg = getCfg();
    if (!cfg) return { ok:false, message:"尚未設定 GitHub" };
    const dir = (cfg.path || "data").replace(/\/$/, "");
    const filePath = `${dir}/${id}.json`;
    const content = JSON.stringify(dataObj, null, 2);

    try {
      const sha = await getSha(cfg, filePath);
      const url = `https://api.github.com/repos/${cfg.owner}/${cfg.repo}/contents/${filePath}`;
      const body = {
        message: `更新 ${id} 資料（天空檔案編輯器）`,
        content: toB64(content),
        branch: cfg.branch || "main",
      };
      if (sha) body.sha = sha;   // 更新既有檔案
      const res = await fetch(url, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${cfg.token}`,
          Accept: "application/vnd.github+json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });
      if (res.ok){
        return { ok:true, message:`已推送到 GitHub（${sha ? "更新" : "新建"} ${filePath}）`, pushed:true };
      }
      const err = await res.json().catch(() => ({}));
      if (res.status === 401) return { ok:false, message:"Token 無效或已過期" };
      if (res.status === 403) return { ok:false, message:"權限不足（Token 需要 contents 寫入權限）" };
      if (res.status === 404) return { ok:false, message:"找不到 repo（檢查 owner/repo 是否正確、Token 是否有此 repo 權限）" };
      return { ok:false, message:`GitHub 錯誤：${err.message || res.status}` };
    } catch (e){
      return { ok:false, message:`網路或設定錯誤：${e.message}` };
    }
  }

  // 驗證設定是否可用（讀 repo 根目錄）
  async function test(cfg){
    try {
      const url = `https://api.github.com/repos/${cfg.owner}/${cfg.repo}`;
      const res = await fetch(url, {
        headers: { Authorization: `Bearer ${cfg.token}`, Accept: "application/vnd.github+json" }
      });
      if (res.ok) return { ok:true, message:"連線成功" };
      if (res.status === 401) return { ok:false, message:"Token 無效" };
      if (res.status === 404) return { ok:false, message:"找不到 repo 或 Token 無此 repo 權限" };
      return { ok:false, message:`錯誤 ${res.status}` };
    } catch (e){
      return { ok:false, message:e.message };
    }
  }

  return { save, getCfg, setCfg, clearCfg, isConfigured, test };
})();

/* ---- 後端二：下載 JSON（永遠可用的後備）---- */
const DownloadStorage = {
  async save(id, dataObj){
    const blob = new Blob([JSON.stringify(dataObj, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = `${id}.json`;
    a.click();
    URL.revokeObjectURL(url);
    return { ok:true, message:`已下載 ${id}.json（請覆蓋 data/ 後重新部署）`, pushed:false };
  }
};

/* ---- 後端三：Cloudflare Pages Function 代管（不需在瀏覽器存 Token）----
   /api/gh-save 由伺服器端持有真正的 GitHub Token，瀏覽器只送出站台密碼
   （與編輯器解鎖同一組，存在 sessionStorage，見 auth.js）。換新裝置只要
   輸入密碼即可，不必再複製/輸入 Personal Access Token。
   若該路由不存在（本機開發、或尚未部署 Functions），save() 回傳 null，
   由上層自動退回舊有的 GitHubStorage／DownloadStorage。 ---- */
const ServerStorage = {
  async checkAvailable(){
    try {
      const res = await fetch("/api/gh-save");
      if (!res.ok) return false;
      const data = await res.json().catch(() => ({}));
      return !!data.configured;
    } catch { return false; }
  },
  async save(id, dataObj){
    try {
      const res = await fetch("/api/gh-save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          password: (typeof HANGAR_AUTH !== "undefined") ? HANGAR_AUTH.sessionPassword() : "",
          path: `data/${id}.json`,
          content: JSON.stringify(dataObj, null, 2),
          message: `更新 ${id} 資料（天空檔案編輯器）`,
        }),
      });
      // 只信任「長得像我們自己函式回應」的內容（有 ok 布林欄位）；
      // 404／501（本機開發伺服器對未知路由的常見回應）或任何非預期格式，
      // 一律視為「這條路由不存在」，交給下一層後備，而不是把伺服器雜訊
      // 誤判成真正的錯誤訊息丟給使用者。
      let data;
      try { data = await res.json(); } catch { return null; }
      if (typeof data.ok !== "boolean") return null;
      return data;
    } catch {
      return null;   // 網路層完全失敗（如本機 file:// 或無 Functions 執行環境），交給下一層後備
    }
  },
};

/* ---- 統一入口：優先走伺服器代管，其次個人 GitHub 設定，最後下載 ---- */
const Storage = {
  mode(){
    return GitHubStorage.isConfigured() ? "github" : "download";
  },
  isConfigured(){
    return GitHubStorage.isConfigured();
  },
  async save(id, dataObj){
    const serverResult = await ServerStorage.save(id, dataObj);
    if (serverResult) return serverResult;
    const backend = this.mode() === "github" ? GitHubStorage : DownloadStorage;
    return backend.save(id, dataObj);
  },
  github: GitHubStorage,
  server: ServerStorage,
};
