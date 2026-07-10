/* ═══════════════════════════════════════════════
   Cloudflare Pages Function — 代管 GitHub 寫入
   ─────────────────────────────────────────────
   讓瀏覽器端不必再持有 GitHub Personal Access Token：
   token 只設定在 Cloudflare 後台的環境變數，任何裝置只要輸入
   站台密碼（與編輯器解鎖用的同一組）即可透過本函式寫入 repo。

   需要在 Cloudflare Pages → Settings → Environment variables 設定：
     EDITOR_PASSWORD  站台編輯密碼（與瀏覽器解鎖畫面設定的密碼一致）
     GH_OWNER         GitHub 使用者名稱
     GH_REPO          repository 名稱
     GH_TOKEN         Personal Access Token（Fine-grained，僅需此 repo 的 Contents: Read and write）
     GH_BRANCH        分支名稱，選填，預設 main
   ═══════════════════════════════════════════════ */

function utf8ToBase64(str) {
  const bytes = new TextEncoder().encode(str);
  let binary = "";
  for (const b of bytes) binary += String.fromCharCode(b);
  return btoa(binary);
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

// GET：健康檢查，回傳伺服器端是否已設定好（不洩漏任何機密內容）
export async function onRequestGet({ env }) {
  const configured = !!(env.EDITOR_PASSWORD && env.GH_OWNER && env.GH_REPO && env.GH_TOKEN);
  return json({ configured });
}

// POST：實際寫入 GitHub
export async function onRequestPost({ request, env }) {
  if (!env.EDITOR_PASSWORD || !env.GH_OWNER || !env.GH_REPO || !env.GH_TOKEN) {
    return json({ ok: false, message: "伺服器尚未設定完成（缺少環境變數），請聯絡站主。" }, 500);
  }

  let body;
  try { body = await request.json(); }
  catch { return json({ ok: false, message: "請求格式錯誤" }, 400); }

  const { password, path, content, message } = body || {};
  if ((password || "").trim() !== (env.EDITOR_PASSWORD || "").trim()) {
    return json({ ok: false, message: "密碼錯誤，請重新登入編輯器後再試。" }, 401);
  }
  if (!path || typeof content !== "string" || path.includes("..")) {
    return json({ ok: false, message: "缺少必要參數或路徑不合法" }, 400);
  }

  const owner = env.GH_OWNER, repo = env.GH_REPO, branch = env.GH_BRANCH || "main";
  const apiUrl = `https://api.github.com/repos/${owner}/${repo}/contents/${path}`;
  const ghHeaders = {
    Authorization: `Bearer ${env.GH_TOKEN}`,
    Accept: "application/vnd.github+json",
    "User-Agent": "sky-archive-pages-function",
  };

  let sha;
  const getRes = await fetch(`${apiUrl}?ref=${encodeURIComponent(branch)}`, { headers: ghHeaders });
  if (getRes.status === 200) sha = (await getRes.json()).sha;
  else if (getRes.status !== 404) {
    return json({ ok: false, message: `讀取檔案狀態失敗（${getRes.status}）` }, 502);
  }

  const putBody = {
    message: message || `更新 ${path}（天空檔案編輯器）`,
    content: utf8ToBase64(content),
    branch,
  };
  if (sha) putBody.sha = sha;

  const putRes = await fetch(apiUrl, {
    method: "PUT",
    headers: { ...ghHeaders, "Content-Type": "application/json" },
    body: JSON.stringify(putBody),
  });

  if (putRes.ok) {
    return json({ ok: true, message: `已推送到 GitHub（${sha ? "更新" : "新建"} ${path}）`, pushed: true });
  }
  const err = await putRes.json().catch(() => ({}));
  if (putRes.status === 401) return json({ ok: false, message: "伺服器端 Token 無效或已過期，請聯絡站主更新。" }, 502);
  if (putRes.status === 403) return json({ ok: false, message: "伺服器端 Token 權限不足（需要 contents 寫入權限）" }, 502);
  if (putRes.status === 404) return json({ ok: false, message: "找不到 repo，請確認 GH_OWNER / GH_REPO 設定正確" }, 502);
  return json({ ok: false, message: `GitHub 錯誤：${err.message || putRes.status}` }, 502);
}
