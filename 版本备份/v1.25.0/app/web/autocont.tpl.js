// ==UserScript==
// @name         单词工作台 · 网页 AI 自动继续
// @namespace    wordsvideo
// @version      __VER__
// @description  网页 AI 回复中断（This response ended early）时自动点「Continue」；单词工作台这一份还没写完、网页 AI 停下来时，自动把「继续」那段话发过去（只在这一份任务的对话里发）。
__MATCHES__
// @grant        GM_xmlhttpRequest
// @connect      127.0.0.1
// @connect      localhost
// @run-at       document-idle
// @noframes
// ==/UserScript==
/* 单词工作台 v1.22.0：浏览器小助手。每 2.5 秒看一眼网页 AI 这一页：
   1. 回复中断了（“This response ended early” 旁边有「Continue」）→ 点「Continue」
   2. 单词工作台说这一份还没写完、网页 AI 已经停下（没有“停止”按钮、页面 20 秒没变）、这个对话里有这一份的文件名
      → 把「继续」那段话（和黄框里「继续：在原来的对话里接着写」复制的一样）贴进输入框、发送
   同一件事最多发两次（第二次隔 8 分钟），软件收到新的一轮才算新的事。软件没开、黄框里关掉了，它什么都不做。 */
(function () {
  'use strict';
  const APP = 'http://127.0.0.1:__PORT__';
  const S = { st: null, stAt: 0, clicks: 0, lastAct: 0, sent: {}, idleAt: 0, sig: '', busy: false };
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  function app(q) {
    return new Promise(res => {
      try {
        GM_xmlhttpRequest({ method: 'GET', url: APP + '/api/relay/auto?' + q, timeout: 6000,
          onload: r => { try { res(JSON.parse(r.responseText)); } catch (e) { res(null); } },
          onerror: () => res(null), ontimeout: () => res(null) });
      } catch (e) { res(null); }
    });
  }
  const vis = el => !!el && el.getClientRects().length > 0 && getComputedStyle(el).visibility !== 'hidden';
  const text = el => ((el && (el.innerText || el.textContent)) || '').replace(/\s+/g, ' ').trim();
  const label = b => [b.getAttribute('aria-label'), b.getAttribute('title'), text(b)].join(' ');
  const buttons = () => [...document.querySelectorAll('button,[role="button"]')].filter(vis);
  // AI 正在写：有“停止”按钮（Stop response / 停止）
  const busy = () => buttons().some(b => /\bstop\b|停止/i.test(label(b)) && !/sharing|共享/i.test(label(b)));
  const EARLY = /ended early|提前结束|tool[- ]use limit|工具.{0,6}(上限|限制)|reached (its|the) (maximum|max|limit)|达到.{0,8}(上限|限制)/i;
  function continueBtn() {
    for (const b of buttons()) {
      if (b.disabled || !/^(continue|继续|继续生成)$/i.test(text(b))) continue;
      let p = b.parentElement;
      for (let i = 0; i < 6 && p; i++, p = p.parentElement) {      // 往上找那句“回复中断了”，只看短的那一小块
        const t = text(p);
        if (t.length > 400) break;
        if (EARLY.test(t)) return b;
      }
    }
    return null;
  }
  const input = () => [...document.querySelectorAll('div[contenteditable="true"],textarea')].filter(vis).pop();
  const sendBtn = () => buttons().filter(b => !b.disabled && /send|发送/i.test(label(b)) && !/stop|停止/i.test(label(b))).pop();
  async function fill(el, t) {
    el.focus();
    if (el.tagName === 'TEXTAREA') {
      Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set.call(el, t);
      el.dispatchEvent(new Event('input', { bubbles: true }));
      return;
    }
    try {
      const dt = new DataTransfer(); dt.setData('text/plain', t);
      el.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true }));
    } catch (e) { /* 有的浏览器不让造粘贴：下面换一种 */ }
    await sleep(300);
    if (text(el).length < Math.min(20, t.length / 2)) {
      document.execCommand('selectAll', false, null);
      document.execCommand('insertText', false, t);
    }
  }
  async function tick() {
    const now = Date.now();
    if (!S.st || now - S.stAt > 6000) { S.st = await app('ping=1&host=' + encodeURIComponent(location.host)); S.stAt = Date.now(); }
    const st = S.st;
    if (!st || !st.on) return;
    if (busy()) { S.idleAt = 0; S.sig = ''; return; }
    const cool = (st.coolSec || 60) * 1000;
    const b = continueBtn();
    if (b) {                                                       // 1. 回复中断：点「Continue」
      if (now - S.lastAct > Math.min(cool, 8000) && S.clicks < (st.maxClicks || 40)) {
        b.click(); S.clicks++; S.lastAct = now; S.sig = '';
        app('ev=continue');
      }
      return;
    }
    if (!st.need || !st.cont || !(st.names || []).length) return;  // 2. 这一份还没写完、AI 停下了：发「继续」
    const body = document.body ? document.body.innerText : '';
    if (!st.names.some(n => body.includes(n))) return;             // 只在这一份任务的对话里发
    const sig = body.length + ':' + body.slice(-300);
    if (sig !== S.sig) { S.sig = sig; S.idleAt = now; return; }    // 页面还在变：等它停稳
    if (now - S.idleAt < (st.idleSec || 20) * 1000 || now - S.lastAct < cool) return;
    const k = S.sent[st.key] || { n: 0, t: 0 };
    if (k.n >= 2 || (k.n && now - k.t < 8 * 60000)) return;        // 同一件事最多发两次，第二次隔 8 分钟
    const el = input();
    if (!el) return;
    await fill(el, st.cont);
    await sleep(700);
    const sb = sendBtn();
    if (sb) sb.click();
    else el.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }));
    S.sent[st.key] = { n: k.n + 1, t: now }; S.lastAct = now; S.stAt = 0; S.sig = '';
    app('ev=send&key=' + encodeURIComponent(st.key));
  }
  setInterval(() => {
    if (S.busy) return;
    S.busy = true;
    tick().catch(() => {}).finally(() => { S.busy = false; });
  }, 2500);
})();
