# -*- coding: utf-8 -*-
"""单词工作台 · v1.23.0：软件自己控制网页 AI 的浏览器窗口（手动接力用）。

软件用这台电脑上的 Edge（没有就用 Chrome）开一个单独的窗口，带着“遥控口”（--remote-debugging-port），
再用 Playwright 连上去。浏览器资料夹单独放在 data/relay-browser：第一次在这个窗口里登录网页 AI，以后就记住了。
窗口是单独的进程：软件重开、更新都不会关掉它，软件起来以后自己再连上。

连上以后软件能“伸手进去”：
- 发到网页 AI：开一个新对话，把提示词贴进输入框、点发送（黄框第 ② 步）
- 回复中断（This response ended early 旁边的 Continue）：自己点「Continue」
- 这一份还没写完、网页 AI 停下了（页面 20 秒没动静）：把「继续」那段话贴进这一份的对话、发送
  （只在对话里有这一份文件名的那一页发；同一件事最多两次；黄框里能关掉）

点按钮、贴字都用页面里的 JS 和 CDP 的 insertText，不靠鼠标：窗口被挡住、最小化也照样能做。
"""
import os, queue, re, socket, subprocess, sys, threading, time, traceback

import core as C

PROFILE = C.DATA / "relay-browser"
PORT = int(os.environ.get("RELAY_CDP_PORT") or 9333)
IDLE, COOL, MAX_CLICKS = 20, 60, 40          # 页面停稳几秒才发「继续」；两次动作至少隔几秒；一次开窗最多点几次 Continue
_Q = queue.Queue()
_LOCK = threading.Lock()
ST = {"state": "off", "ready": False, "msg": "", "act": "", "t": 0.0, "pages": 0, "err": ""}
_W = {"thr": None, "sig": {}, "idle": {}, "last": 0.0, "clicks": 0, "sent": {}}

# 页面里看一眼：AI 在不在写、有没有“回复中断 + Continue”、输入框在不在、这一页有没有这一份的文件名
_JS = r"""
const vis = el => !!el && el.getClientRects().length > 0 && getComputedStyle(el).visibility !== 'hidden';
const text = el => ((el && (el.innerText || el.textContent)) || '').replace(/\s+/g, ' ').trim();
const label = b => [b.getAttribute('aria-label'), b.getAttribute('title'), text(b)].join(' ');
const buttons = () => [...document.querySelectorAll('button,[role="button"]')].filter(vis);
const busy = () => buttons().some(b => /\bstop\b|停止/i.test(label(b)) && !/sharing|共享/i.test(label(b)));
const EARLY = /ended early|提前结束|tool[- ]use limit|工具.{0,6}(上限|限制)|reached (its|the) (maximum|max|limit)|达到.{0,8}(上限|限制)/i;
function contBtn() {
  for (const b of buttons()) {
    if (b.disabled || !/^(continue|继续|继续生成)$/i.test(text(b))) continue;
    let p = b.parentElement;
    for (let i = 0; i < 6 && p; i++, p = p.parentElement) { const t = text(p); if (t.length > 400) break; if (EARLY.test(t)) return b; }
  }
  return null;
}
const editor = () => [...document.querySelectorAll('div[contenteditable="true"],textarea')].filter(vis).pop();
const sendBtn = () => buttons().filter(b => !b.disabled && /send|发送/i.test(label(b)) && !/stop|停止/i.test(label(b))).pop();
"""
PROBE = "(names) => {" + _JS + """
  const body = document.body ? document.body.innerText : '';
  return { busy: busy(), early: !!contBtn(), composer: !!editor(), has: names.some(n => n && body.includes(n)),
           sig: body.length + ':' + body.slice(-300), url: location.href, title: document.title };
}"""
CLICK_CONT = "() => {" + _JS + " const b = contBtn(); if (!b) return false; b.click(); return true; }"
FOCUS_ED = "() => {" + _JS + """ const e = editor(); if (!e) return false; e.focus();
  if (e.tagName === 'TEXTAREA') e.select(); else { const r = document.createRange(); r.selectNodeContents(e); const s = getSelection(); s.removeAllRanges(); s.addRange(r); }
  return true; }"""
ED_LEN = "() => {" + _JS + " const e = editor(); return e ? (e.value || e.innerText || '').trim().length : -1; }"
CLICK_SEND = "() => {" + _JS + " const b = sendBtn(); if (!b) return false; b.click(); return true; }"
AFTER_SEND = "() => {" + _JS + " const e = editor(); return busy() || !e || (e.value || e.innerText || '').trim().length < 5; }"


def _set(**kw):
    with _LOCK:
        ST.update(t=time.time(), **kw)


def status():
    with _LOCK:
        return dict(ST)


def _exe():
    if os.environ.get("RELAY_BROWSER"):
        return os.environ["RELAY_BROWSER"]
    if sys.platform == "win32":
        pf, pf86, la = os.environ.get("ProgramFiles", r"C:\Program Files"), os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"), \
            os.environ.get("LOCALAPPDATA", "")
        cands = [os.path.join(pf86, r"Microsoft\Edge\Application\msedge.exe"), os.path.join(pf, r"Microsoft\Edge\Application\msedge.exe"),
                 os.path.join(pf, r"Google\Chrome\Application\chrome.exe"), os.path.join(pf86, r"Google\Chrome\Application\chrome.exe"),
                 os.path.join(la, r"Google\Chrome\Application\chrome.exe")]
    else:
        cands = ["/usr/bin/microsoft-edge", "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"]
    return next((p for p in cands if p and os.path.exists(p)), "")


def _port_open():
    try:
        with socket.create_connection(("127.0.0.1", PORT), timeout=0.5):
            return True
    except OSError:
        return False


def can():
    """能不能用：有 Edge / Chrome、装了 Playwright。返回 (能不能, 不能的原因)。"""
    try:
        import playwright.sync_api  # noqa: F401
    except Exception:
        return False, "没装 Playwright（关掉软件，重新双击「启动.bat」会自己装）"
    if not _exe() and not _port_open():
        return False, "这台电脑上没找到 Edge 或 Chrome"
    return True, ""


def _start():
    if _W["thr"] and _W["thr"].is_alive():
        return
    _W["thr"] = threading.Thread(target=_worker, daemon=True, name="relay-browser")
    _W["thr"].start()


def open_ai(url):
    ok, why = can()
    if not ok:
        return False, why
    _start()
    _Q.put(("open", {"url": url}))
    return True, "软件用它自己控制的浏览器窗口打开网页 AI（第一次要在那个窗口里登录一下，以后就记住了）"


def send(url, text):
    ok, why = can()
    if not ok:
        return False, why
    _start()
    _set(msg="正在打开网页 AI、贴提示词…")
    _Q.put(("send", {"url": url, "text": text}))
    return True, "软件正在打开网页 AI、开新对话、贴提示词、发送（第一次要在弹出来的窗口里登录一下）"


def attach_if_running():
    """软件重开以后：上次开的那个窗口还在，就再连上（自动点「继续」接着管）。"""
    if _port_open() and can()[0]:
        _start()
        _Q.put(("attach", {}))


# ─────────────────────────── 下面都在 relay-browser 这个线程里跑（Playwright 只能在一个线程里用） ───────────────────────────
def _worker():
    try:
        from playwright.sync_api import sync_playwright
        pw = sync_playwright().start()
    except Exception as e:
        _set(state="off", msg="浏览器控制没开起来：%s" % str(e)[:160])
        return
    br, last = None, 0.0
    while True:
        try:
            cmd, kw = _Q.get(timeout=1.0)
        except queue.Empty:
            cmd, kw = None, {}
        try:
            if cmd:
                br = _ensure(pw, br, kw.get("url") or (C.load_cfg().get("relayUrl") or ""), launch=cmd != "attach")
                if br and cmd == "open":
                    pg = _pick(br, kw["url"])
                    pg.bring_to_front()
                elif br and cmd == "send":
                    _send_prompt(br, kw["url"], kw["text"])
            if br and not br.is_connected():
                br = None
                _W["sig"].clear(); _W["idle"].clear()
                _set(state="off", ready=False, msg="网页 AI 的窗口关了")
            if br and time.time() - last > 2.5:
                last = time.time()
                _watch(br)
        except Exception as e:
            traceback.print_exc()
            _set(err=str(e)[:200], msg="出错了：%s" % str(e).split("\n")[0][:160])
            try:
                if br and not br.is_connected():
                    br = None
                    _set(state="off", ready=False)
            except Exception:
                br = None


def _ensure(pw, br, url, launch=True):
    if br and br.is_connected():
        return br
    if not _port_open():
        if not launch:
            return None
        exe = _exe()
        if not exe:
            raise RuntimeError("这台电脑上没找到 Edge 或 Chrome")
        PROFILE.mkdir(parents=True, exist_ok=True)
        args = [exe, "--remote-debugging-port=%d" % PORT, "--user-data-dir=" + str(PROFILE), "--no-first-run", "--no-default-browser-check",
                # 窗口被挡住、最小化也照常干活（不然页面冻住，点不动）
                "--disable-background-timer-throttling", "--disable-backgrounding-occluded-windows", "--disable-renderer-backgrounding",
                "--disable-features=CalculateNativeWinOcclusion", "--window-size=1280,900"]
        args += (os.environ.get("RELAY_BROWSER_ARGS") or "").split()
        args.append(url or "about:blank")
        _set(state="starting", msg="正在打开浏览器窗口…")
        kw = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL, "stdin": subprocess.DEVNULL}
        if sys.platform == "win32":
            kw["creationflags"] = 0x00000008 | 0x00000200          # 单独的进程：软件关了它也还在
        else:
            kw["start_new_session"] = True
        subprocess.Popen(args, **kw)
        t0 = time.time()
        while not _port_open():
            if time.time() - t0 > 25:
                raise RuntimeError("浏览器开了，但 25 秒还没连上（端口 %d）" % PORT)
            time.sleep(0.4)
    br = pw.chromium.connect_over_cdp("http://127.0.0.1:%d" % PORT, timeout=20000)
    _set(state="on", msg="网页 AI 的窗口开着（软件控制）", err="")
    C.log("软件连上了网页 AI 的浏览器窗口（能自己贴提示词、自己点「继续」）")
    return br


def _pages(br):
    out = []
    for ctx in br.contexts:
        out += [p for p in ctx.pages if not p.is_closed() and not p.url.startswith(("devtools://", "chrome-extension://", "edge://"))]
    return out


def _probe(pg, names):
    try:
        return pg.evaluate(PROBE, names)
    except Exception:
        return None


def _pick(br, url):
    """有输入框的那一页（最后一个）；没有就用第一页，打开网页 AI。"""
    pages = _pages(br)
    good = [p for p in pages if (_probe(p, []) or {}).get("composer")]
    if good:
        return good[-1]
    pg = pages[0] if pages else (br.contexts[0] if br.contexts else br.new_context()).new_page()
    if url and not pg.url.startswith(url.split("#")[0][:30]):
        pg.goto(url, wait_until="domcontentloaded", timeout=45000)
    return pg


def _wait_composer(pg, sec):
    t0 = time.time()
    while time.time() - t0 < sec:
        if (_probe(pg, []) or {}).get("composer"):
            return True
        time.sleep(1.0)
    return False


def _type_send(pg, text):
    """把字贴进输入框（先选中原来的字，换掉）、点发送。返回 (发出去了没, 一句话)。"""
    if not pg.evaluate(FOCUS_ED):
        return False, "没找到输入框"
    pg.keyboard.insert_text(text)
    time.sleep(0.8)
    n = pg.evaluate(ED_LEN)
    if n < min(10, len(text.strip()) // 2):
        return False, "输入框里没贴进去"
    if not pg.evaluate(CLICK_SEND):
        pg.keyboard.press("Enter")
    for _ in range(8):
        time.sleep(0.8)
        if pg.evaluate(AFTER_SEND):
            return True, "发出去了"
    return False, "点了发送，但输入框里的字还在：看看那个窗口"


def _send_prompt(br, url, text):
    tid = C.RELAY.get("tid")
    pg = _pick(br, url)
    pg.bring_to_front()
    if re.search(r"/chat/", pg.url or ""):                    # 现在是一个旧对话：开个新对话（claude 一类的网页 AI 是 /new）
        m = re.match(r"^(https?://[^/]+)", pg.url)
        try:
            pg.goto(m.group(1) + "/new", wait_until="domcontentloaded", timeout=45000)
        except Exception:
            pass
        if not _wait_composer(pg, 15) and url:
            pg.goto(url, wait_until="domcontentloaded", timeout=45000)
    if not _wait_composer(pg, 30):
        _set(ready=False, msg="网页 AI 的窗口开着，但没找到输入框：在那个窗口里登录一次（以后就记住了），进到能打字的页面，再点「发到网页 AI」")
        C.log("发到网页 AI：窗口开着，没找到输入框——要先在那个窗口里登录一次", tid)
        return
    ok, msg = _type_send(pg, text)
    _W["last"] = time.time()
    if ok:
        _set(ready=True, msg="提示词发出去了（%s）" % time.strftime("%H:%M"), act="")
        C.log("软件把提示词贴进网页 AI、发出去了（%d 字）" % len(text), tid)
    else:
        _set(msg="提示词没发出去：%s（提示词在剪贴板里，可以自己粘贴）" % msg)
        C.log("发到网页 AI 没成：%s" % msg, tid)


def _watch(br):
    st = C.relay_auto({"host": "软件控制的浏览器"})
    names = st.get("names") or []
    infos = [(p, i) for p in _pages(br) for i in [_probe(p, names)] if i]
    _set(ready=any(i["composer"] for _, i in infos), pages=len(infos))
    if not st.get("on"):
        return
    now = time.time()
    for pg, info in infos:                                    # 回复中断：这个窗口只给网页 AI 用，哪一页中断了都点
        if info["early"] and not info["busy"]:
            if now - _W["last"] > min(COOL, 8) and _W["clicks"] < MAX_CLICKS and pg.evaluate(CLICK_CONT):
                _W["clicks"] += 1
                _W["last"] = now
                C.relay_auto({"ev": "continue"})
                _set(act="%s 回复中断了，点了「Continue」" % time.strftime("%H:%M"))
            return
    task = next(((p, i) for p, i in infos if i["has"]), None)
    if not task or not st.get("need") or not st.get("cont"):
        return
    pg, info = task
    k = id(pg)
    if info["busy"]:
        _W["sig"].pop(k, None)
        return
    if _W["sig"].get(k) != info["sig"]:                      # 页面还在变：等它停稳
        _W["sig"][k], _W["idle"][k] = info["sig"], now
        return
    if now - _W["idle"].get(k, now) < IDLE or now - _W["last"] < COOL:
        return
    n, t = _W["sent"].get(st["key"], (0, 0.0))
    if n >= 2 or (n and now - t < 480):                       # 同一件事最多发两次，第二次隔 8 分钟
        return
    ok, msg = _type_send(pg, st["cont"])
    _W["sent"][st["key"]] = (n + 1, now)
    _W["last"] = now
    _W["sig"].pop(k, None)
    if ok:
        C.relay_auto({"ev": "send"})
        _set(act="%s 网页 AI 停下了，发了「继续」" % time.strftime("%H:%M"))
    else:
        _set(act="%s 想发「继续」没发出去：%s" % (time.strftime("%H:%M"), msg))
