"use strict";
/* ═══════════════════════════════════════════════
   編輯器密碼保護（純前端，防路人誤改用）
   - 密碼以 SHA-256 雜湊儲存，不存明文
   - 首次使用時設定密碼；之後需驗證才能進入編輯
   - 通過後於本頁 sessionStorage 記住，重整不必再輸入
   ─────────────────────────────────────────────
   安全性聲明：這是「柵欄」不是「保險箱」。任何人檢視原始碼
   都能繞過前端驗證。真正的保護在於——編輯結果僅存於編輯者自己
   的瀏覽器，必須匯出 JSON 覆蓋檔案並重新部署才會影響線上內容。
   訪客即使繞過此關卡，也無法改動其他人看到的網站。
   ═══════════════════════════════════════════════ */

const HANGAR_AUTH = (() => {
  const HASH_KEY = "hangar_pw_hash";   // localStorage：密碼雜湊
  const SESSION_KEY = "hangar_authed"; // sessionStorage：本次已驗證

  async function sha256(text){
    const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
    return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, "0")).join("");
  }

  const hasPassword = () => !!localStorage.getItem(HASH_KEY);
  const isAuthed = () => sessionStorage.getItem(SESSION_KEY) === "1";

  async function setPassword(pw){
    localStorage.setItem(HASH_KEY, await sha256(pw));
    sessionStorage.setItem(SESSION_KEY, "1");
  }

  async function verify(pw){
    const stored = localStorage.getItem(HASH_KEY);
    if (!stored) return false;
    const ok = (await sha256(pw)) === stored;
    if (ok) sessionStorage.setItem(SESSION_KEY, "1");
    return ok;
  }

  function changePassword(){
    localStorage.removeItem(HASH_KEY);
    sessionStorage.removeItem(SESSION_KEY);
  }

  function logout(){ sessionStorage.removeItem(SESSION_KEY); }

  return { hasPassword, isAuthed, setPassword, verify, changePassword, logout };
})();

/* 在頁面掛上一個全螢幕鎖，通過後才 resolve */
function requireAuth(){
  return new Promise(resolve => {
    if (HANGAR_AUTH.isAuthed()) { resolve(); return; }

    const firstTime = !HANGAR_AUTH.hasPassword();
    const gate = document.createElement("div");
    gate.className = "auth-gate";
    gate.innerHTML = `
      <div class="auth-box">
        <div class="eyebrow">${firstTime ? "SET PASSWORD / 設定密碼" : "EDITOR LOCKED / 編輯已鎖定"}</div>
        <h2>${firstTime ? "首次使用，請設定編輯密碼" : "請輸入編輯密碼"}</h2>
        <p class="auth-desc">${firstTime
          ? "這組密碼保存在你的瀏覽器，用來防止他人隨手修改資料。忘記可清除瀏覽器資料重設。"
          : "此密碼保護編輯功能。訪客仍可正常瀏覽所有內容。"}</p>
        <input type="password" id="auth-input" placeholder="${firstTime ? "設定一組密碼…" : "密碼…"}" autocomplete="off">
        ${firstTime ? '<input type="password" id="auth-confirm" placeholder="再次輸入確認…" autocomplete="off">' : ''}
        <div class="auth-err" id="auth-err"></div>
        <div class="auth-actions">
          <a href="index.html" class="auth-cancel">← 返回列表</a>
          <button id="auth-submit">${firstTime ? "設定並進入" : "解鎖"}</button>
        </div>
      </div>`;
    document.body.appendChild(gate);

    const input = gate.querySelector("#auth-input");
    const confirm = gate.querySelector("#auth-confirm");
    const err = gate.querySelector("#auth-err");
    input.focus();

    async function submit(){
      const pw = input.value;
      if (!pw){ err.textContent = "請輸入密碼"; return; }
      if (firstTime){
        if (pw.length < 4){ err.textContent = "密碼至少 4 個字元"; return; }
        if (pw !== confirm.value){ err.textContent = "兩次輸入不一致"; return; }
        await HANGAR_AUTH.setPassword(pw);
        gate.remove(); resolve();
      } else {
        if (await HANGAR_AUTH.verify(pw)){ gate.remove(); resolve(); }
        else { err.textContent = "密碼錯誤"; input.value = ""; input.focus(); }
      }
    }

    gate.querySelector("#auth-submit").addEventListener("click", submit);
    gate.addEventListener("keydown", e => { if (e.key === "Enter") submit(); });
  });
}
