/* ═══════════════════════════════════════════════
   Cloudflare Pages Function — 密碼驗證（不寫入 GitHub）
   ─────────────────────────────────────────────
   讓編輯器解鎖畫面可以直接對伺服器端的 EDITOR_PASSWORD 驗證，
   而不是每台裝置各自比對本機存的密碼雜湊——這樣不同裝置輸入
   同一組密碼時，結果才會一致，不會各裝置各自為政。
   ═══════════════════════════════════════════════ */

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

// GET：健康檢查，回傳伺服器端是否已設定密碼
export async function onRequestGet({ env }) {
  return json({ configured: !!env.EDITOR_PASSWORD });
}

// POST：驗證密碼是否正確
export async function onRequestPost({ request, env }) {
  if (!env.EDITOR_PASSWORD) {
    return json({ ok: false, message: "伺服器尚未設定密碼" }, 500);
  }
  let body;
  try { body = await request.json(); }
  catch { return json({ ok: false, message: "請求格式錯誤" }, 400); }

  const pw = ((body && body.password) || "").trim();
  if (pw !== env.EDITOR_PASSWORD.trim()) {
    return json({ ok: false, message: "密碼錯誤" }, 401);
  }
  return json({ ok: true });
}
