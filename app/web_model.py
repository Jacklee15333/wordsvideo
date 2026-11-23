"""
web_model.py — 「伪模型」核心：用 Playwright 操作 sorryios.ai 的网页 ChatGPT。

★ 2026-11 适配改版：站点从 /pastel 迁到 /laike，登录页新增「同意用户协议」勾选框，
  登录后不一定直接落在卡片列表。现在：站点路径可配置（sitePath）并自动回退，
  登录后自动寻找卡片列表并记住其地址，任何一步失败都会把截图+页面结构存到
  memory/web_model_diag/ 便于下次快速对照修复。

这是参考实现 ai/ai-runner.js（Node + Playwright）的 Python 移植，保留它全部
经过实战打磨的健壮性：
  · 单浏览器单例（任一时刻只有一个 Chromium）
  · storageState 登录态持久化（7 天 TTL）
  · 选卡进聊天页（按 空闲 > 正常 > 繁忙 优先级随机选一张 TEAM/PLUS 卡）
  · 发送 prompt（冷启动 hydration 兼容、读回校验、Shift+Enter 换行不误发）
  · ★命门 _wait_for_reply：思考型模型「先预声明→思考N秒→出真答案」的多层答完判定
  · 卡死恢复（STUCK → 换卡重试）、纯思考无输出保护、空回卷保护、总超时兜底

并发模型：后端是多线程 http.server，但 Playwright 同步 API 的对象绑定创建线程。
所以这里起一个【专用 worker 线程】独占浏览器，所有请求经 web_complete() 投递到任务
队列、阻塞等结果——一个 worker 一次只处理一个 job，这本身就是「串行单浏览器」锁。

对外只暴露：
  configure(cfg) / load_config() / save_config(cfg)
  web_complete(prompt, **opts) -> str        # 同步阻塞，返回回复纯文本
  test_login(on_progress=None) -> dict        # 「测试网页模型」用
  get_state() -> dict
  shutdown()
"""

import os
import re
import json
import time
import queue
import random
import threading
import traceback
from pathlib import Path

# —— 解决 Windows 控制台中文乱码（防御性，server.py 已设过；单独跑也安全）——
import sys as _sys
try:
    # line_buffering=True：每行立即刷新，避免日志卡在缓冲区里看不到（排错关键）
    _sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    _sys.stderr.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
except Exception:
    pass
try:
    if _sys.platform == "win32":
        import ctypes as _ctypes
        _ctypes.windll.kernel32.SetConsoleOutputCP(65001)
except Exception:
    pass

try:
    from playwright.sync_api import sync_playwright
    _PW_IMPORT_ERR = None
except Exception as _e:          # 没装 playwright 时不要让 import 崩掉整个后端
    sync_playwright = None
    _PW_IMPORT_ERR = _e

# ─────────────── 常量 ───────────────
SITE_ORIGIN = "https://sorryios.ai"
DEFAULT_SITE_PATH = "laike"              # 2026-11 起的新路径；老路径 pastel 作为自动回退
KNOWN_SITE_PATHS = ["laike", "pastel"]


def _site_base(path):
    return "%s/%s" % (SITE_ORIGIN, (path or DEFAULT_SITE_PATH).strip("/"))


def _login_url_for(path):
    return _site_base(path) + "#/login"


def _carlist_url_for(path):
    return _site_base(path) + "#/carlist"


# 兼容旧代码的模块级常量（实际运行时用 worker 上的 self._login_url / self._carlist_url）
LOGIN_URL = _login_url_for(DEFAULT_SITE_PATH)
CARLIST_URL = _carlist_url_for(DEFAULT_SITE_PATH)

BASE_DIR = Path(__file__).parent
MEMORY_DIR = BASE_DIR / "memory"
MEMORY_DIR.mkdir(exist_ok=True)
CONFIG_PATH = MEMORY_DIR / "web_model.json"
SESSION_PATH = MEMORY_DIR / "web_session.json"
SESSION_TTL_DAYS = 7
ROUTES_PATH = MEMORY_DIR / "web_model_routes.json"   # 自动学到的卡片列表地址
DIAG_DIR = MEMORY_DIR / "web_model_diag"             # 失败时的截图 + 页面结构
IMG_DIR = MEMORY_DIR / "web_model_images"            # AI 回复里的图片（调用方取走后移到笔记目录）
DIAG_KEEP = 10

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")


def _default_config():
    return {
        "aiUsername": "",
        "aiPassword": "",
        "headless": False,        # 默认显示浏览器，便于排错；设 True 后台跑
        # v55：浏览器照常开着、照常工作，只是移到屏幕外看不见（软件里能看实时画面）。
        # 在软件里点「显示浏览器」会移回屏幕上，并记住这个选择。
        "browserHidden": True,
        "cardName": "",           # 想指定的卡名（留空＝任意可用卡，全都是 ChatGPT）
        "enableSearch": True,     # 默认开联网搜索：软件要的就是最新信息，别让用户漏配
        "aiUrl": "https://sorryios.ai/",
        "sitePath": DEFAULT_SITE_PATH,   # 网站路径：sorryios.ai/<sitePath>#/login，改版时改这里
        "serviceName": "ChatGPT",        # 登录后若先进「选服务」页，点这个名字进入卡片列表
        # 每个新任务怎么开始：card＝回首页换一张新的 AI 卡（最干净，默认）；chat＝同一张卡上开新聊天（更快）
        "newTaskMode": "card",
        # 分析类任务（视频总结/思维导图）用哪个模型：留空＝自动选菜单里最高级的；
        # 也可以填模型名里的关键字固定下来，比如 "Pro"、"High"、"Thinking"
        "preferredModel": "",
    }


# ─────────────── 配置读写（人类可读、可手改）───────────────
def load_config():
    if CONFIG_PATH.exists():
        try:
            c = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            merged = {**_default_config(), **c}
            # 迁移：老配置里 enableSearch 可能是 False（早期默认），且用户从没手动设过。
            # 软件目的就是拿最新信息，这里强制兜底为 True，省得用户不知道要去勾。
            # 仅当用户显式写了 enableSearchUserSet=true 才尊重其 False 选择。
            if not c.get("enableSearchUserSet") and merged.get("enableSearch") is not True:
                merged["enableSearch"] = True
            return merged
        except Exception:
            pass
    return _default_config()


def save_config(cfg):
    merged = {**load_config(), **(cfg or {})}
    CONFIG_PATH.write_text(json.dumps(merged, ensure_ascii=False, indent=2),
                           encoding="utf-8")
    # 配置变了（尤其账号），让下次查询重新就位
    _worker().request_restart()
    return merged


# ─────────────── session（storageState）持久化 ───────────────
def _load_session():
    if not SESSION_PATH.exists():
        return None
    try:
        wrapper = json.loads(SESSION_PATH.read_text(encoding="utf-8"))
        if not wrapper or "savedAt" not in wrapper or "state" not in wrapper:
            return None
        age_ms = time.time() * 1000 - wrapper["savedAt"]
        if age_ms > SESSION_TTL_DAYS * 24 * 3600 * 1000:
            return None
        return wrapper["state"]
    except Exception:
        return None


def _save_session(state):
    try:
        SESSION_PATH.write_text(
            json.dumps({"savedAt": time.time() * 1000, "state": state},
                       ensure_ascii=False),
            encoding="utf-8")
    except Exception:
        pass


def _load_routes():
    try:
        return json.loads(ROUTES_PATH.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}


def _save_routes(routes):
    try:
        ROUTES_PATH.write_text(json.dumps(routes, ensure_ascii=False, indent=2),
                               encoding="utf-8")
    except Exception:
        pass


def _clear_session():
    try:
        if SESSION_PATH.exists():
            SESSION_PATH.unlink()
    except Exception:
        pass


# 不用鼠标、不需要窗口在前台，直接把文字写进输入框：
#   · textarea/input：用原生 setter 写值再发 input 事件（React 认得）；
#   · contenteditable（新版 ChatGPT 的 ProseMirror）：选中全部内容后派发一个「粘贴」事件，
#     编辑器自己会把文字插进去；编辑器没接住时再用 execCommand('insertText') 兜底。
_DOM_FILL_JS = r"""(el, text) => {
    try { el.focus({preventScroll: true}); } catch (e) { try { el.focus(); } catch (e2) {} }
    const tag = (el.tagName || '').toUpperCase();
    if (tag === 'TEXTAREA' || tag === 'INPUT') {
        const proto = tag === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
        Object.getOwnPropertyDescriptor(proto, 'value').set.call(el, text);
        el.dispatchEvent(new Event('input', {bubbles: true}));
        return 'value';
    }
    const sel = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(el);
    sel.removeAllRanges(); sel.addRange(range);
    try {
        const dt = new DataTransfer();
        dt.setData('text/plain', text);
        const ev = new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true});
        el.dispatchEvent(ev);
        if (ev.defaultPrevented) return 'paste';
    } catch (e) {}
    return document.execCommand('insertText', false, text) ? 'insertText' : '';
}"""


# ════════ v62：批量分析点「停止」时，让 AI 池马上放下手上这条（不用等它答完）════════
_CANCEL_EVT = threading.Event()
_CANCEL_WHY = [""]
_CANCEL_AT = [0.0]


class _Cancelled(Exception):
    """用户点了停止：这条不再等、也不换卡重试。"""


def cancel_current(why="你点了停止"):
    """让 AI 池马上放下正在做的这一条。等回复的循环每半秒看一次，最多一两秒就停下。"""
    _CANCEL_WHY[0] = why
    _CANCEL_AT[0] = time.time()
    _CANCEL_EVT.set()


def was_cancelled(within=20):
    """刚刚（within 秒内）是不是有人点了停止——上层据此不再「换卡重试」。"""
    return time.time() - _CANCEL_AT[0] < within


def _check_cancel():
    if _CANCEL_EVT.is_set():
        _CANCEL_EVT.clear()
        raise _Cancelled(_CANCEL_WHY[0] or "已取消")


# v121：AI 镜像网站打不开（浏览器报错页 / 网站 5xx / 一直进不到能提问的页面）→ 这条直接算失败，不干等、也不换卡重试
class SiteDown(_Cancelled):
    pass


_READY_LIMIT = 120        # 从「打开网页」到能提问，最多等这么久（秒）
_SITE_ERR_JS = r"""() => {
  const u = location.href || '';
  if (u.startsWith('chrome-error://')) return '浏览器显示「无法访问此网站」';
  const t = (document.title || '').trim();
  if (/^(500|502|503|504|520|521|522|523|524)\b|bad gateway|service unavailable|gateway time-?out|internal server error/i.test(t))
    return '网站报错：' + t.slice(0, 60);
  const b = ((document.body && document.body.innerText) || '').slice(0, 3000);
  if (b.length < 1500 && /无法访问此网站|This site can.t be reached|ERR_(CONNECTION|NAME_NOT_RESOLVED|TIMED_OUT|PROXY|TUNNEL|SSL|CERT|ADDRESS|EMPTY_RESPONSE)|502 Bad Gateway|503 Service|504 Gateway/i.test(b)) {
    const m = b.match(/ERR_[A-Z_]+/);
    return '浏览器报错' + (m ? '：' + m[0] : '');
  }
  return '';
}"""


# v62：输入框里是不是还躺着这段提示词（= 没发出去）。只看可编辑的框，不看已经发出去的提问气泡。
_COMPOSER_HAS_JS = r"""(head) => {
    const norm = (s) => (s || '').replace(/\s+/g, '');
    const h = norm(head).slice(0, 40);
    if (!h) return false;
    const els = document.querySelectorAll('textarea, [contenteditable="true"], [role="textbox"]');
    for (const el of els) {
        const r = el.getBoundingClientRect();
        if (r.width < 20 || r.height < 10) continue;
        const t = norm(el.value !== undefined && el.value !== null && el.tagName === 'TEXTAREA' ? el.value : el.innerText);
        if (t.includes(h)) return true;
    }
    return false;
}"""

# v62：发送键现在能不能点（enabled / disabled / none=没认出来）
_SEND_STATE_JS = r"""() => {
    const sels = ['button[data-testid="send-button"]', '#composer-submit-button',
                  'button[aria-label*="发送"]', 'button[aria-label*="Send" i]'];
    let b = null;
    for (const s of sels) { b = document.querySelector(s); if (b) break; }
    if (!b) {
        const inp = document.querySelector('[data-cx-input="1"]');
        const root = (inp && (inp.closest('form') || inp.parentElement && inp.parentElement.parentElement)) || document;
        b = [...root.querySelectorAll('button')].find(x => /send|发送/i.test(
            (x.getAttribute('aria-label') || '') + ' ' + (x.getAttribute('data-testid') || '') + ' ' + (x.title || '')));
    }
    if (!b) return 'none';
    return (b.disabled || b.getAttribute('aria-disabled') === 'true') ? 'disabled' : 'enabled';
}"""


# ════════════════ 任务栏：只藏 AI 池自己的浏览器窗口 ════════════════
# v67 修好误伤：v62～v66 按「窗口在屏幕外」认 AI 池窗口，可 Windows 里**最小化的窗口都在屏幕外**（-32000），
# 结果你自己最小化着的 Chrome（还有 Edge 等同类窗口）也被从任务栏拿掉了，再最小化就变成屏幕左下角一个个小条。
# 现在只按「进程号」认：只有 AI 池自己启动的那个浏览器的窗口才会被藏；认不出就什么都不做。
_WS_EX_TOOLWINDOW, _WS_EX_APPWINDOW = 0x00000080, 0x00040000
_WS_MINIMIZEBOX, _WS_MAXIMIZEBOX = 0x00020000, 0x00010000


def _win_user32():
    import ctypes
    from ctypes import wintypes
    user32 = ctypes.windll.user32
    get = getattr(user32, "GetWindowLongPtrW", user32.GetWindowLongW)
    setl = getattr(user32, "SetWindowLongPtrW", user32.SetWindowLongW)
    get.restype, get.argtypes = ctypes.c_ssize_t, [wintypes.HWND, ctypes.c_int]
    setl.restype, setl.argtypes = ctypes.c_ssize_t, [wintypes.HWND, ctypes.c_int, ctypes.c_ssize_t]
    return ctypes, wintypes, user32, get, setl


def _enum_windows():
    """所有看得见的顶层窗口：hwnd、进程号、类名、是否最小化、左边位置、有没有主人窗口、样式。"""
    ctypes, wintypes, user32, get, _setl = _win_user32()
    out = []
    proto = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

    def cb(hwnd, _lp):
        try:
            if not user32.IsWindowVisible(hwnd):
                return True
            buf = ctypes.create_unicode_buffer(64)
            user32.GetClassNameW(hwnd, buf, 64)
            pid = wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            r = wintypes.RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(r))
            tb = ctypes.create_unicode_buffer(120)
            user32.GetWindowTextW(hwnd, tb, 120)
            out.append({"hwnd": hwnd, "pid": pid.value, "cls": buf.value, "iconic": bool(user32.IsIconic(hwnd)),
                        "title": tb.value,
                        "left": r.left, "owned": bool(user32.GetWindow(hwnd, 4)),
                        "style": get(hwnd, -16) & 0xFFFFFFFF, "ex": get(hwnd, -20) & 0xFFFFFFFF})
        except Exception:
            pass
        return True
    user32.EnumWindows(proto(cb), 0)
    return out


def _pick_pool_windows(wins, pids, show):
    """AI 池自己的浏览器窗口：只按进程号认。藏的时候还要求它确实被挪到了屏幕外、而且不是最小化。"""
    pids = set(pids or ())
    if not pids:
        return []
    hits = []
    for w in wins:
        if w["pid"] not in pids or w["cls"] != "Chrome_WidgetWin_1" or w["owned"]:
            continue
        if not show and (w["iconic"] or w["left"] > OFFSCREEN_X // 2):
            continue
        hits.append(w["hwnd"])
    return hits


def _pick_broken_windows(wins, skip_pids, names):
    """以前的版本误伤的窗口：Chrome / Edge 的正常窗口（能最小化也能最大化），却被加上了「工具窗口」样式。"""
    out = []
    for w in wins:
        if w["cls"] != "Chrome_WidgetWin_1" or w["owned"] or w["pid"] in skip_pids:
            continue
        if not (w["ex"] & _WS_EX_TOOLWINDOW):
            continue
        if not (w["style"] & _WS_MINIMIZEBOX) or not (w["style"] & _WS_MAXIMIZEBOX):
            continue
        if names.get(w["pid"], "") not in ("chrome.exe", "msedge.exe"):
            continue
        out.append(w["hwnd"])
    return out


def _win_proc_name(pid):
    try:
        import ctypes
        from ctypes import wintypes
        k32 = ctypes.windll.kernel32
        h = k32.OpenProcess(0x1000, False, pid)            # PROCESS_QUERY_LIMITED_INFORMATION
        if not h:
            return ""
        try:
            buf = ctypes.create_unicode_buffer(520)
            n = wintypes.DWORD(520)
            if k32.QueryFullProcessImageNameW(h, 0, buf, ctypes.byref(n)):
                return os.path.basename(buf.value).lower()
        finally:
            k32.CloseHandle(h)
    except Exception:
        pass
    return ""


def _set_toolwindow(hwnds, tool):
    ctypes, wintypes, user32, get, setl = _win_user32()
    flags = 0x1 | 0x2 | 0x4 | 0x10 | 0x20   # 不改大小/位置/层级、不抢焦点，只让新样式生效
    for hwnd in hwnds:
        ex = get(hwnd, -20)
        new = ((ex | _WS_EX_TOOLWINDOW) & ~_WS_EX_APPWINDOW) if tool else ((ex | _WS_EX_APPWINDOW) & ~_WS_EX_TOOLWINDOW)
        if new != ex:
            setl(hwnd, -20, new)
            user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, flags)


def _taskbar_tabs(hwnds, show):
    """用系统的任务栏接口（ITaskbarList）给这些窗口加回 / 删掉任务栏按钮。"""
    try:
        import ctypes
        from ctypes import wintypes
        ole32 = ctypes.windll.ole32

        class _GUID(ctypes.Structure):
            _fields_ = [("a", ctypes.c_ulong), ("b", ctypes.c_ushort), ("c", ctypes.c_ushort),
                        ("d", ctypes.c_ubyte * 8)]

        def guid(t):
            g = _GUID()
            ole32.CLSIDFromString(ctypes.c_wchar_p(t), ctypes.byref(g))
            return g
        ole32.CoInitializeEx(None, 2)
        clsid = guid("{56FDF344-FD6D-11d0-958A-006097C9A090}")     # TaskbarList
        iid = guid("{56FDF342-FD6D-11d0-958A-006097C9A090}")       # ITaskbarList
        ptr = ctypes.c_void_p()
        if ole32.CoCreateInstance(ctypes.byref(clsid), None, 1, ctypes.byref(iid), ctypes.byref(ptr)) == 0 \
                and ptr.value:
            vt = ctypes.cast(ptr, ctypes.POINTER(ctypes.POINTER(ctypes.c_void_p))).contents
            fn = ctypes.WINFUNCTYPE
            hr_init = fn(ctypes.c_long, ctypes.c_void_p)(vt[3])
            add_tab = fn(ctypes.c_long, ctypes.c_void_p, wintypes.HWND)(vt[4])
            del_tab = fn(ctypes.c_long, ctypes.c_void_p, wintypes.HWND)(vt[5])
            release = fn(ctypes.c_ulong, ctypes.c_void_p)(vt[2])
            hr_init(ptr)
            for hwnd in hwnds:
                (add_tab if show else del_tab)(ptr, hwnd)
            release(ptr)
    except Exception:
        pass


def _win_taskbar_set(show, pids=None):
    """把挪到屏幕外的 AI 池浏览器窗口从任务栏拿掉 / 放回来（不碰窗口的显示状态，实时画面照常）。
    v67：pids = AI 池自己启动的浏览器进程。只动这些进程的窗口；没有 pids 就什么都不做。返回动了几个窗口。"""
    import sys as _sys
    if _sys.platform != "win32" or not pids:
        return 0
    try:
        hits = _pick_pool_windows(_enum_windows(), pids, show)
        if hits:
            _set_toolwindow(hits, tool=not show)
            _taskbar_tabs(hits, show)
        return len(hits)
    except Exception:
        return 0


def find_stray_bars():
    """v71：找屏幕左下角那种「小条」：最小化着、却没有标题栏或者没有任务栏按钮的窗口。
    返回 [{hwnd, pid, name, title, cls}]。只用来说明是谁，不去动别的软件的窗口。"""
    import sys as _sys
    if _sys.platform != "win32":
        return []
    out = []
    try:
        for w in _enum_windows():
            if not w["iconic"] or w["owned"]:
                continue
            no_caption = (w["style"] & 0x00C00000) != 0x00C00000
            if not (no_caption or (w["ex"] & _WS_EX_TOOLWINDOW)):
                continue
            out.append({"hwnd": w["hwnd"], "pid": w["pid"], "name": _win_proc_name(w["pid"]),
                        "title": w.get("title") or "", "cls": w["cls"]})
    except Exception:
        pass
    return out


def repair_taskbar(exclude_pids=()):
    """v67：把以前版本误伤的 Chrome / Edge 窗口放回任务栏（软件启动时做一次）。
    不碰 AI 池自己的浏览器（exclude_pids）、不碰本软件自己的窗口。返回修好了几个。"""
    import sys as _sys
    if _sys.platform != "win32":
        return 0
    try:
        wins = _enum_windows()
        skip = set(exclude_pids or ()) | {os.getpid()}
        try:
            skip.add(os.getppid())
        except Exception:
            pass
        names = {}
        for w in wins:
            if w["cls"] == "Chrome_WidgetWin_1" and (w["ex"] & _WS_EX_TOOLWINDOW) and w["pid"] not in names:
                names[w["pid"]] = _win_proc_name(w["pid"])
        hits = _pick_broken_windows(wins, skip, names)
        if hits:
            _set_toolwindow(hits, tool=False)
            _taskbar_tabs(hits, True)
        return len(hits)
    except Exception:
        return 0


def is_available():
    return sync_playwright is not None


def playwright_import_error():
    return str(_PW_IMPORT_ERR) if _PW_IMPORT_ERR else ""


# ════════════════════════════════════════════════════════════════
# Worker：独占浏览器的专用线程。所有浏览器操作只在这个线程里跑。
# ════════════════════════════════════════════════════════════════
# ════════════════════ v55：AI 池实时画面（给软件里的「实时画面」面板用） ════════════════════
# 这些状态由 worker 线程写，HTTP 线程读：
#   stage   最近一步在干什么（打开网页 / 换卡 / 思考中 / 接收回复中…）
#   reply   AI 正在写的回复（边写边更新）
#   shot    浏览器页面的截图（只有软件里打开了实时画面时才截，平时不截，不费资源）
import collections as _collections

_LIVE_LOCK = threading.Lock()
_LIVE = {"busy": False, "job": "", "stage": "", "stage_at": 0.0, "started": 0.0,
         "finished": 0.0, "reply": "", "reply_at": 0.0, "shot": b"", "shot_ts": 0.0,
         "shot_err": "", "watch_until": 0.0, "visible": None}
_LIVE_LOG = _collections.deque(maxlen=80)
_UI_CMDS = queue.Queue()          # 「显示/隐藏浏览器」这类命令，交给 worker 线程去做
OFFSCREEN_X = -12000              # 隐藏＝把窗口挪到屏幕外（不能最小化：最小化后 Chrome 会暂停页面）


# v133：网页上不是回复内容的小字（按钮上的字、读屏用的隐藏标签、思考用时）。整行就是这些时去掉。
_UI_LINE_RE = re.compile(
    r"^\s*(?:#{1,6}\s*)?(?:ChatGPT\s*(?:说|said)\s*[:：]?|你说\s*[:：]?|You said:?|最新一条回复|"
    r"(?:已)?思考了?\s*\d[\dms秒分钟\s]*|思考用时.{0,12}|Thought for .{0,24}|"
    r"重置清单(?:\s*复制清单)?|复制清单|复制代码|显示更多|显示全部|Copy code)\s*$", re.I)


def _clean_reply_text(text):
    """v133：回复里整行是网页小字的（「ChatGPT 说：」「思考了 58s」「重置清单 复制清单」「复制代码」）去掉。"""
    if not text:
        return text or ""
    lines = [ln for ln in str(text).split("\n") if not _UI_LINE_RE.match(ln)]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def _live_set(**kw):
    with _LIVE_LOCK:
        _LIVE.update(kw)


def _live_log(msg):
    with _LIVE_LOCK:
        _LIVE_LOG.append((round(time.time(), 1), str(msg)[:300]))


def _save_pref(**kw):
    """只改配置文件里的几个开关，不触发浏览器重启（save_config 会让浏览器重开）。"""
    try:
        c = json.loads(CONFIG_PATH.read_text(encoding="utf-8")) if CONFIG_PATH.exists() else {}
    except Exception:
        c = {}
    c.update(kw)
    try:
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(json.dumps(c, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


class _WebWorker:
    def __init__(self):
        self._jobs = queue.Queue()
        self._thread = None
        self._lock = threading.Lock()
        self._want_restart = False
        # 以下都只在 worker 线程内访问
        self._pw = None
        self._browser = None
        self._context = None
        self._page = None
        self._state = "idle"   # idle | ready | error | closed
        self._logger = print
        self._site_path = DEFAULT_SITE_PATH
        self._service_name = "ChatGPT"
        self._login_url = LOGIN_URL
        self._carlist_url = CARLIST_URL
        self._landing_url = ""
        self._chat_epoch = 0      # 每进入一个全新的网页对话线程 +1（客户端据此判断能否发增量）
        self._chat_used = True    # 当前对话里是否已经发过东西（刚换卡/开新聊天后为 False）
        self._best_epoch = -1     # 在哪个对话线程上已经切过最高级模型
        self._cur_box = None      # 正在执行的 job 的结果盒（心跳写在里面）
        self._dead = False        # 被看门狗放弃的 worker：跑完手上这条就退出
        self._browser_pids = set()
        # v55：实时画面 / 显示隐藏浏览器
        self._headless = False
        self._in_tick = False
        self._quiet_shots = False   # 正在填字/发送时不截图，免得打乱节奏
        self._last_shot = 0.0
        self._shot_backoff = 0.0
        self._cdp = None
        self._cdp_page = None
        self._win_restore = None    # 隐藏前窗口在屏幕上的位置，显示时放回去

    # ---- 公共：投递一个 job，阻塞等结果 ----
    # timeout 从这个 job【真正开始执行】时算起（排队等前一个 job 的时间不算），
    # 这样前一个分析想得久，后面排队的不会被误判超时。
    # 另有看门狗：job 在跑、但浏览器 WATCHDOG_SEC 秒没有任何动静（页面调用卡死），
    # 就强制关掉浏览器进程、让下一个 job 重新打开，这一条按失败返回，交给上层重试。
    def submit(self, fn_name, kwargs, timeout=720):
        self._ensure_thread()
        result_box = {"queued": time.time()}
        done = threading.Event()
        self._jobs.put((fn_name, kwargs, result_box, done))
        while not done.wait(5):
            started = result_box.get("started")
            if not started:
                continue                      # 还在排队：前一个 job 自己有看门狗管着
            now = time.time()
            quiet = now - (result_box.get("hb") or started)
            why = ""
            if quiet > WATCHDOG_SEC:
                why = "浏览器 %d 秒没有任何反应（页面卡死）" % int(quiet)
            elif now - started > timeout:
                why = "这次任务超过 %d 分钟还没结束" % max(1, int(timeout // 60))
            if why:
                w = result_box.get("worker") or self
                _reset_worker(w, why, result_box, done)
                if done.is_set() and "value" in result_box and "error" not in result_box:
                    return result_box.get("value")
                raise TimeoutError("AI 池%s，已强制重启浏览器（这条会自动重试）" % why)
        if "error" in result_box:
            raise result_box["error"]
        return result_box.get("value")

    def _beat(self):
        """有动静就记一下（看门狗据此判断浏览器是不是卡死了）。"""
        b = self._cur_box
        if b is not None:
            b["hb"] = time.time()

    def request_restart(self):
        self._want_restart = True

    def _ensure_thread(self):
        with self._lock:
            if self._thread and self._thread.is_alive():
                return
            self._thread = threading.Thread(
                target=self._run, name="web-model-worker", daemon=True)
            self._thread.start()

    def set_logger(self, fn):
        self._logger = fn or print

    def _log(self, msg):
        self._beat()
        try:
            self._logger("[web_model] " + str(msg))
            try:
                _sys.stdout.flush()
            except Exception:
                pass
        except Exception:
            pass
        _live_log(msg)
        self._tick()

    # ---- worker 主循环：一次处理一个 job（＝串行单浏览器）----
    def _run(self):
        if sync_playwright is None:
            return
        with sync_playwright() as pw:
            self._pw = pw
            while not self._dead:
                # 空闲时每 0.5 秒醒一次：处理「显示/隐藏浏览器」、给实时画面截图
                job = None
                while job is None and not self._dead:
                    try:
                        job = self._jobs.get(timeout=0.5)
                    except queue.Empty:
                        self._tick(idle=True)
                if job is None:
                    break
                fn_name, kwargs, box, done = job
                if self._dead:                   # 已被放弃：把 job 还给新的 worker
                    _requeue_job((fn_name, kwargs, box, done))
                    break
                box["started"] = box["hb"] = time.time()
                box["worker"] = self
                self._cur_box = box
                self._quiet_shots = False
                _live_set(busy=True, job=fn_name, started=box["started"], finished=0.0,
                          stage="开始处理…", stage_at=box["started"], reply="", reply_at=0.0)
                ok_job = False
                try:
                    fn = getattr(self, fn_name)
                    box["value"] = fn(**(kwargs or {}))
                    ok_job = True
                except Exception as e:        # noqa
                    box["error"] = e
                    self._log("job 出错: " + repr(e))
                    self._log(traceback.format_exc())
                finally:
                    self._cur_box = None
                    self._quiet_shots = False
                    _live_set(busy=False, finished=time.time(),
                              stage="这一条已完成" if ok_job else "这一条出错了（会自动重试）",
                              stage_at=time.time())
                    done.set()
            if self._dead:
                self._safe(self._close)

    # ════════════════════ 浏览器生命周期 ════════════════════
    @staticmethod
    def _cfg_proxy():
        try:
            import web_tools
            return web_tools._read_proxy() or ""
        except Exception:
            return ""

    def _probe_one(self, mode, timeout=9):
        """用 Python 快速访问一次 AI 池首页，测某种网络方式通不通。返回 (通不通, 说明)。"""
        import urllib.request
        import urllib.error
        url = SITE_ORIGIN + "/" + (getattr(self, "_site_path", DEFAULT_SITE_PATH) or "laike") + "/"
        if mode == "direct":
            handler = urllib.request.ProxyHandler({})
        elif mode == "proxy":
            p = self._cfg_proxy()
            if not p:
                return False, "没设置代理"
            handler = urllib.request.ProxyHandler({"http": p, "https": p})
        else:
            try:
                reg = urllib.request.getproxies_registry()
            except Exception:
                reg = {}
            reg = {k: v for k, v in (reg or {}).items() if k in ("http", "https")}
            if not reg:
                return False, "系统没开代理"
            handler = urllib.request.ProxyHandler(reg)
        try:
            import web_tools
            op = urllib.request.build_opener(handler, urllib.request.HTTPSHandler(context=web_tools._ssl_ctx()))
        except Exception:
            op = urllib.request.build_opener(handler)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                                   "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"})
        try:
            with op.open(req, timeout=timeout) as r:
                r.read(2048)
            return True, "通"
        except urllib.error.HTTPError as e:
            return (e.code < 500), "HTTP %d" % e.code      # 403/404 也说明连上了
        except Exception as e:
            s = str(e)
            low = s.lower()
            if "timed out" in low or "timeout" in low:
                return False, "超时"
            if "10054" in s or "reset" in low or "closed" in low or "eof" in low:
                return False, "连接被断开"
            if "10061" in s or "refused" in low:
                return False, "连接被拒绝"
            return False, s.split("\n")[0][:50]

    def _probe_net(self, prefer):
        """按「上次成功的方式 → 代理 → 系统代理 → 直连」测通，返回第一个能连上的。
        全都连不上：直接报一句说得清楚的原因（不再花几分钟一遍遍启动浏览器去试）。"""
        order = [prefer] + [m for m in ("proxy", "system", "direct") if m != prefer]
        results = []
        for m in order:
            ok, why = self._probe_one(m)
            results.append((m, why))
            if ok:
                if m != prefer:
                    self._log("AI 池测通：「%s」连不上，改用「%s」" % (prefer, m))
                return m
        names = {"proxy": "走代理", "system": "系统代理", "direct": "直连"}
        detail = "；".join("%s：%s" % (names.get(m, m), w) for m, w in results)
        raise RuntimeError(
            "AI 池网站（%s）现在打不开（%s）。请先在自己的浏览器里打开它看看：浏览器也打不开 → 网站暂时故障，过会儿再试；"
            "浏览器能打开 → 检查 Clash 是不是开了「全局」模式或换了海外节点（这个网站可能拒绝海外节点），"
            "改回「规则」模式再试。" % (SITE_ORIGIN, detail))

    def _net_args(self):
        mode = getattr(self, "_net_mode", "system")
        if mode == "direct":
            return ["--no-proxy-server"]
        if mode == "proxy" and self._cfg_proxy():
            return ["--proxy-server=%s" % self._cfg_proxy(), "--proxy-bypass-list=<-loopback>"]
        return []        # system：跟随系统代理

    def _launch_browser(self, headless):
        tries = [
            ("Google Chrome", "chrome"),
            ("Microsoft Edge", "msedge"),
            ("Playwright bundled Chromium", None),
        ]
        last_err = None
        for name, channel in tries:
            try:
                hide_args = []
                if not headless and load_config().get("browserHidden", True):
                    hide_args = ["--window-position=%d,0" % OFFSCREEN_X]
                opts = dict(
                    headless=bool(headless),
                    args=self._net_args() + hide_args +
                         ["--disable-blink-features=AutomationControlled",
                          # 窗口被别的程序挡住/最小化时也照常渲染，不然页面「冻住」，
                          # 点击和发送会一直等，非得把鼠标移回浏览器才继续
                          "--disable-background-timer-throttling",
                          "--disable-backgrounding-occluded-windows",
                          "--disable-renderer-backgrounding",
                          "--disable-features=CalculateNativeWinOcclusion",
                          "--no-sandbox", "--disable-dev-shm-usage"],
                )
                if channel:
                    opts["channel"] = channel
                import os as _os
                opts["env"] = {k: v for k, v in _os.environ.items()
                               if k.upper() not in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY")}
                before = _browser_child_pids()
                b = self._pw.chromium.launch(**opts)
                self._browser_pids = _browser_child_pids() - before
                self._log("launched via " + name)
                return b
            except Exception as e:
                last_err = e
                self._log("try %s failed: %s" % (name, str(e).split(chr(10))[0]))
        raise RuntimeError("没有可用浏览器，最后错误: %s" % last_err)

    def _destroy_browser(self, browser):
        if not browser:
            return
        try:
            for c in list(browser.contexts):
                try:
                    c.close()
                except Exception:
                    pass
        except Exception:
            pass
        try:
            browser.close()
        except Exception:
            pass

    def _close(self):
        b = self._browser
        self._cdp = self._cdp_page = None
        _live_set(visible=None)
        self._page = self._context = self._browser = None
        self._state = "closed"
        self._destroy_browser(b)
        self._browser_pids = set()

    def _kill_browser_procs(self):
        """（看门狗用，在别的线程调用）直接结束这个浏览器的进程。卡在页面调用里的
        worker 线程会因此立刻收到「浏览器已关闭」的异常，从卡死中恢复过来。"""
        pids = set(self._browser_pids or ())
        self._want_restart = True
        return _kill_pids(pids)

    def _ensure_started(self):
        """启动 + 登录 + 选卡 + 进聊天页。已就绪则直接返回。"""
        if (self._state == "ready" and self._page and not self._page.is_closed()
                and not self._want_restart):
            return
        # 残留句柄先收掉，保证单浏览器
        if self._browser or self._want_restart:
            self._close()
        self._want_restart = False

        cfg = load_config()
        if not cfg.get("aiUsername") or not cfg.get("aiPassword"):
            self._state = "error"
            raise RuntimeError("请先在「网页大模型」设置里填写 sorryios.ai 账号和密码")

        headless = cfg.get("headless") is True
        self._headless = headless
        self._resolve_routes(cfg)
        # AI 池网络方式：proxy＝走「设置」里的代理 / system＝跟随系统代理 / direct＝直连。
        # 自动模式：用上次成功的方式；没有记录时，sorryios.ai 在境外 → 先走代理。
        mode = (cfg.get("aiPoolProxy") or "auto").lower()
        if mode in ("direct", "system", "proxy"):
            self._net_mode = mode
        elif not getattr(self, "_net_retry", False):
            learned = _load_routes().get("netMode")
            self._net_mode = learned if learned in ("direct", "system", "proxy") else (
                "proxy" if self._cfg_proxy() else "system")
            self._net_tried = set()
        if mode not in ("direct", "system", "proxy") and not getattr(self, "_net_retry", False):
            self._net_mode = self._probe_net(self._net_mode)       # 先用十几秒测通，挑能连上的方式
        self._log("AI 池网络：%s" % {"proxy": "走代理 %s" % self._cfg_proxy(), "system": "跟随系统代理",
                                    "direct": "直连"}.get(self._net_mode, self._net_mode))
        self._state = "starting"
        self._log("starting (headless=%s)..." % headless)
        try:
            self._browser = self._launch_browser(headless)
            saved = _load_session()
            self._context = self._browser.new_context(
                storage_state=saved or None,
                viewport={"width": 1280, "height": 900},
                user_agent=UA,
            )
            self._page = self._context.new_page()
            # v55：默认把浏览器挪到屏幕外（照常工作），软件里看实时画面；点「显示浏览器」再挪回来
            if not headless:
                if cfg.get("browserHidden", True):
                    ok_h, why_h = self._safe(lambda: self._set_window_visible(False), (False, "出错"))
                    self._log("浏览器已移到屏幕外（照常工作，软件里能看实时画面）" if ok_h
                              else "浏览器没能移到屏幕外：%s" % why_h)
                else:
                    _live_set(visible=True)
            # 全局默认超时调短：任何 click/fill 卡住最多 8 秒就抛错，便于快速换方法/诊断
            try:
                self._page.set_default_timeout(8000)
            except Exception:
                pass
            self._log("context ready, savedState=%s" % ("YES" if saved else "NO"))

            need_login = True
            if saved:
                try:
                    self._log("尝试复用 session → " + self._carlist_url)
                    self._page.goto(self._carlist_url, wait_until="domcontentloaded",
                                    timeout=20000)
                    if self._wait_for_cards(8):
                        self._log("✓ session 复用成功，跳过登录")
                        need_login = False
                    else:
                        self._log("session 已失效或卡片页地址变了 → 走完整登录")
                        _clear_session()
                except Exception as e:
                    self._log("session 复用出错: %s → 走完整登录" % e)
                    _clear_session()

            if need_login:
                self._do_login(cfg)
                try:
                    _save_session(self._context.storage_state())
                    self._log("✓ session 已保存，下次免登录")
                except Exception as e:
                    self._log("session 保存失败: %s" % e)

            self._select_card_and_enter_chat()
            self._state = "ready"
            self._log("✓ 就绪")
            try:
                r = _load_routes()
                if r.get("netMode") != self._net_mode:
                    r["netMode"] = self._net_mode
                    _save_routes(r)
            except Exception:
                pass
        except Exception as e:
            self._state = "error"
            self._dump_diag("start", e)
            self._close()
            msg = str(e)
            net_err = any(k in msg for k in ("ERR_", "打开登录页失败", "Timeout", "timeout", "net::"))
            if net_err and (load_config().get("aiPoolProxy") or "auto").lower() == "auto":
                tried = getattr(self, "_net_tried", set())
                tried.add(self._net_mode)
                self._net_tried = tried
                order = (["proxy"] if self._cfg_proxy() else []) + ["system", "direct"]
                nxt = next((m for m in order if m not in tried), None)
                if nxt:
                    self._log("AI 池用「%s」打不开（%s），换「%s」再试" % (
                        self._net_mode, msg.split("\n")[0][:60], nxt))
                    self._net_mode = nxt
                    self._net_retry = True
                    try:
                        return self._ensure_started()
                    finally:
                        self._net_retry = False
            raise

    # ════════════════════ 登录 ════════════════════
    def _human_type(self, locator, text):
        for ch in text:
            delay = 30 + random.randint(0, 49)
            if ch == "\n":
                locator.press("Shift+Enter")     # 换行不触发发送
                time.sleep(delay / 1000)
            elif ch == "\r":
                continue
            else:
                locator.type(ch, delay=delay)

    def _find_button_by_text(self, *keywords):
        for kw in keywords:
            for b in self._page.locator("button").all():
                try:
                    t = ((b.inner_text(timeout=1000) or "").strip().lower())
                    if kw.lower() in t and b.is_visible():
                        return b
                except Exception:
                    pass
        return None

    # ---- 站点路径 / 卡片列表地址 ----
    def _resolve_routes(self, cfg):
        self._site_path = (cfg.get("sitePath") or DEFAULT_SITE_PATH).strip("/")
        self._service_name = (cfg.get("serviceName") or "ChatGPT").strip()
        self._login_url = _login_url_for(self._site_path)
        routes = _load_routes()
        if routes.get("sitePath") == self._site_path and routes.get("carlistUrl"):
            self._carlist_url = routes["carlistUrl"]
        else:
            self._carlist_url = _carlist_url_for(self._site_path)
        self._log("站点路径=%s 登录页=%s 卡片页=%s"
                  % (self._site_path, self._login_url, self._carlist_url))

    def _learn_carlist(self, url):
        url = (url or "").strip()
        if not url or "login" in url:
            return
        if url != self._carlist_url:
            self._log("记住卡片列表地址: " + url)
        self._carlist_url = url
        _save_routes({**_load_routes(), "sitePath": self._site_path, "carlistUrl": url,
                      "learnedAt": time.strftime("%Y-%m-%d %H:%M:%S")})

    _PAGE_STATUS_JS = r"""() => {
        const url = window.location.href;
        const vis = el => { const r = el.getBoundingClientRect();
            return r.width > 0 && r.height > 0 && getComputedStyle(el).visibility !== 'hidden'; };
        const hasPasswordInput = [...document.querySelectorAll('input[type="password"]')].some(vis);
        const bt = document.body ? (document.body.innerText || '') : '';
        const hasCardListMarkers =
            ((bt.includes('空闲') || bt.includes('繁忙') || bt.includes('正常')) &&
             (bt.includes('TEAM') || bt.includes('PLUS') || bt.includes('Plus') || bt.includes('PRO')))
            || /[A-Z]{2}\d{4}-\d{2}/.test(bt);
        return { url, hasPasswordInput, hasCardListMarkers,
                 isLoginPage: url.includes('/login') || hasPasswordInput };
    }"""

    def _page_status(self):
        return self._safe(lambda: self._page.evaluate(self._PAGE_STATUS_JS),
                          {"url": "", "hasPasswordInput": False,
                           "hasCardListMarkers": False, "isLoginPage": False})

    def _wait_for_cards(self, timeout_sec=8):
        end = time.time() + timeout_sec
        self._dismiss_popups(min(1.5, timeout_sec))   # 弹窗会挡住卡片点击，先关掉
        while True:
            st = self._page_status()
            if st.get("hasCardListMarkers") and not st.get("isLoginPage"):
                return True
            if time.time() >= end:
                return False
            time.sleep(0.8)

    def _adopt_new_page(self, before_count):
        """点击后如果弹出了新标签页，就切过去（很多聚合站点会新开标签进聊天）。"""
        try:
            pages = self._context.pages
            if len(pages) > before_count:
                newp = pages[-1]
                try:
                    newp.wait_for_load_state("domcontentloaded", timeout=15000)
                except Exception:
                    pass
                self._safe(lambda: newp.set_default_timeout(8000))
                self._page = newp
                self._log("检测到新标签页，已切换: " + (newp.url or ""))
                return True
        except Exception:
            pass
        return False

    def _click_text(self, text):
        """点击页面上包含 text 的、尽量小的可见可点元素。返回是否点到。"""
        coords = self._safe(lambda: self._page.evaluate(r"""(text) => {
            const cands = [];
            for (const el of document.querySelectorAll('a,button,[role="button"],[role="tab"],[role="menuitem"],li,div,span')) {
                const t = (el.innerText || '').trim();
                if (!t || !t.includes(text) || t.length > text.length + 40) continue;
                const r = el.getBoundingClientRect();
                if (r.width < 8 || r.height < 8 || r.bottom < 0 || r.top > window.innerHeight) continue;
                const clickable = el.matches('a,button,[role="button"],[role="tab"],[role="menuitem"]') ||
                                  getComputedStyle(el).cursor === 'pointer';
                cands.push({ area: r.width * r.height, clickable,
                             cx: Math.round(r.x + r.width / 2), cy: Math.round(r.y + r.height / 2) });
            }
            if (!cands.length) return null;
            cands.sort((a, b) => (b.clickable - a.clickable) || (a.area - b.area));
            return cands[0];
        }""", text), None)
        if not coords:
            return False
        self._page.mouse.click(coords["cx"], coords["cy"])
        return True

    # 公告/提示弹窗按钮：优先「今日不再提示」（当天不再弹），其次「知道了」等
    _POPUP_BTN_TEXTS = ["今日不再提示", "今天不再提示", "不再提示", "知道了", "我知道了",
                        "我已知晓", "关闭公告", "关闭"]
    _POPUP_JS = r"""(texts) => {
        const norm = s => (s || '').replace(/\s+/g, '');
        for (const want of texts) {
            for (const b of document.querySelectorAll('button,[role="button"],a,span,div')) {
                if (norm(b.innerText) !== want) continue;
                const r = b.getBoundingClientRect();
                if (r.width < 10 || r.height < 10 || r.bottom < 0 || r.top > window.innerHeight) continue;
                const cx = r.x + r.width / 2, cy = r.y + r.height / 2;
                // 必须是最上层（真正浮在页面上的弹窗按钮，不是被遮住的普通元素）
                const top = document.elementFromPoint(cx, cy);
                if (!top || !(top === b || b.contains(top) || top.contains(b))) continue;
                return { text: want, cx: Math.round(cx), cy: Math.round(cy) };
            }
        }
        return null;
    }"""

    def _dismiss_popups(self, wait_sec=2.0):
        """关掉网页打开时弹出的公告提示框（如「注册即可免费试用…」→ 知道了）。
        会先等 wait_sec 秒让弹窗出现（多数有延迟/动画），最多连关 3 个。返回关掉的个数。"""
        closed = 0
        end = time.time() + wait_sec
        while closed < 3:
            hit = self._safe(lambda: self._page.evaluate(self._POPUP_JS,
                                                         self._POPUP_BTN_TEXTS), None)
            if not hit:
                if time.time() >= end:
                    break
                time.sleep(0.4)
                continue
            self._page.mouse.click(hit["cx"], hit["cy"])
            closed += 1
            self._log("关闭弹窗提示：点击「%s」" % hit["text"])
            time.sleep(0.8)
            end = time.time() + 0.8      # 关掉一个后再看一眼有没有下一个
        return closed

    def _goto_carlist(self):
        """去卡片列表页。依次尝试：当前页 → 记住的/默认地址 → 「选服务」页里点服务名。"""
        if self._wait_for_cards(1):
            self._learn_carlist(self._page.url)
            return True
        # 刚登录完落在「选服务」页：先在当前页找服务入口，省一次跳转
        if self._try_service_entry():
            return True
        tried = []
        for url in (self._carlist_url, _carlist_url_for(self._site_path)):
            if url in tried:
                continue
            tried.append(url)
            self._log("打开卡片列表 " + url)
            self._safe(lambda u=url: self._page.goto(u, wait_until="domcontentloaded",
                                                     timeout=30000))
            if self._wait_for_cards(10):
                self._learn_carlist(self._page.url)
                return True
            if self._page_status().get("isLoginPage"):
                return False      # 交给上层处理重新登录
        # 新平台是多服务聚合（ChatGPT/Claude/Gemini…），可能要先选服务
        seen = set()
        for url in (self._landing_url, _site_base(self._site_path) + "#/",
                    _site_base(self._site_path) + "/#/"):
            if not url or url in seen or "/login" in url:
                continue
            seen.add(url)
            self._safe(lambda u=url: self._page.goto(u, wait_until="domcontentloaded",
                                                     timeout=30000))
            time.sleep(2)
            if self._page_status().get("isLoginPage"):
                return False
            if self._wait_for_cards(1) or self._try_service_entry():
                self._learn_carlist(self._page.url)
                return True
        self._log("⚠ 没找到卡片列表页（当前 %s）" % self._page.url)
        return False

    def _try_service_entry(self):
        """在当前页点服务名（默认 ChatGPT）进入卡片列表。"""
        before = len(self._context.pages)
        if not self._click_text(self._service_name):
            return False
        self._log("点击服务入口「%s」" % self._service_name)
        time.sleep(2)
        self._adopt_new_page(before)
        if self._wait_for_cards(12):
            self._learn_carlist(self._page.url)
            return True
        return False

    # ---- 登录 ----
    _AGREE_JS = r"""() => {
        const kw = /(阅读|同意).{0,12}(协议|条款|政策|声明)|agree|terms/i;
        const vis = el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
        const near = el => { let n = el;
            for (let i = 0; i < 5 && n; i++) { n = n.parentElement;
                if (n && kw.test(n.innerText || '')) return true; }
            return false; };
        // 1) 原生 checkbox（多数 UI 库会把它藏起来，要点它旁边的可视方框）
        for (const cb of document.querySelectorAll('input[type="checkbox"]')) {
            if (!near(cb)) continue;
            let target = cb;
            const cs = getComputedStyle(cb);
            if (!vis(cb) || cs.opacity === '0' || cs.visibility === 'hidden')
                target = cb.nextElementSibling && vis(cb.nextElementSibling)
                         ? cb.nextElementSibling : cb.parentElement;
            const r = target.getBoundingClientRect();
            return { found: true, checked: cb.checked,
                     cx: Math.round(r.x + Math.min(r.width, 24) / 2), cy: Math.round(r.y + r.height / 2) };
        }
        // 2) 自绘 checkbox
        for (const el of document.querySelectorAll('[role="checkbox"],[class*="checkbox"]')) {
            if (!vis(el) || !near(el)) continue;
            const checked = el.getAttribute('aria-checked') === 'true' ||
                            /(^|\s|-)(is-)?checked(\s|$)/.test(el.className || '');
            const r = el.getBoundingClientRect();
            return { found: true, checked,
                     cx: Math.round(r.x + Math.min(r.width, 24) / 2), cy: Math.round(r.y + r.height / 2) };
        }
        return { found: false };
    }"""

    def _ensure_agreement_checked(self):
        """勾选「我已阅读并同意《用户服务协议》」。只点方框，避免点到协议链接弹窗。"""
        info = self._safe(lambda: self._page.evaluate(self._AGREE_JS), {"found": False})
        if not info.get("found"):
            self._log("未发现协议勾选框（可能不需要）")
            return
        if info.get("checked"):
            self._log("协议已勾选")
            return
        self._page.mouse.click(info["cx"], info["cy"])
        time.sleep(0.4)
        info = self._safe(lambda: self._page.evaluate(self._AGREE_JS), {"found": False})
        if not info.get("checked"):
            # 兜底：直接 check 原生 input
            self._safe(lambda: self._page.locator('input[type="checkbox"]').first.check(
                force=True, timeout=3000))
            time.sleep(0.3)
            info = self._safe(lambda: self._page.evaluate(self._AGREE_JS), {"found": False})
        self._dismiss_agreement_dialog()
        self._log("协议勾选" + ("成功" if info.get("checked") else "可能未成功（继续尝试登录）"))

    def _dismiss_agreement_dialog(self):
        """若弹出了协议/提示弹窗，点里面的「同意/确定」按钮。返回是否点了。"""
        return bool(self._safe(lambda: self._page.evaluate(r"""() => {
            const dlgs = document.querySelectorAll('[role="dialog"],[class*="modal"],[class*="dialog"],[class*="popup"]');
            for (const d of dlgs) {
                const r = d.getBoundingClientRect();
                if (r.width < 50 || r.height < 50) continue;
                for (const b of d.querySelectorAll('button,[role="button"],a')) {
                    const t = (b.innerText || '').trim();
                    const br = b.getBoundingClientRect();
                    if (br.width > 0 && /同意|确定|确认|我知道了|Agree|OK/i.test(t) && !/不同意|取消/.test(t)) {
                        b.click(); return true;
                    }
                }
            }
            return false;
        }"""), False))

    def _find_login_button(self):
        """登录按钮：先找字正好是“登录”的按钮（不会点到“其他登录方式”“立即注册”），再放宽到 role=button、提交按钮、可点的 div/span。"""
        exact = re.compile(r"^\s*(用户)?登\s*录\s*$|^\s*(log\s*in|sign\s*in)\s*$", re.I)
        for sel in ("button", "[role=button]", "input[type=submit]", "a", "div", "span"):
            try:
                for b in self._page.locator(sel).all()[:200]:
                    try:
                        if not b.is_visible():
                            continue
                        t = (b.inner_text(timeout=500) or b.get_attribute("value") or "").strip()
                        if exact.match(t):
                            return b
                    except Exception:
                        pass
            except Exception:
                pass
        return self._find_button_by_text("用户登录", "登录", "登 录", "Login", "Sign in")

    def _wait_left_login(self, secs):
        end = time.time() + secs
        while time.time() < end:
            _check_cancel()
            time.sleep(1)
            st = self._page_status()
            if not st.get("isLoginPage"):
                self._landing_url = st.get("url", "")
                self._log("✓ 登录成功，落地页 " + self._landing_url)
                self._dismiss_popups(2.0)
                return True
        return False

    def _submit_login_other_ways(self, pwd):
        """点了登录还停在登录页、页面上也没报错：换几种提交方法再试（回车、表单提交、用脚本点按钮）。"""
        ways = [("在密码框按回车", lambda: pwd.press("Enter")),
                ("提交登录表单", lambda: self._page.evaluate(
                    "() => { const f = document.querySelector('input[type=password]').closest('form');"
                    " if (f) { f.requestSubmit ? f.requestSubmit() : f.submit(); return true } return false }")),
                ("用脚本点登录按钮", lambda: self._page.evaluate(r"""() => {
                    const els = [...document.querySelectorAll('button,[role=button],input[type=submit],a,div,span')]
                      .filter(e => /^\s*(用户)?登\s*录\s*$/.test(e.innerText || e.value || '') && e.getBoundingClientRect().width > 0);
                    if (!els.length) return false; els[els.length - 1].click(); return true }"""))]
        for name, fn in ways:
            self._log("登录：%s" % name)
            self._safe(fn)
            if self._wait_left_login(6):
                return True
            if self._login_error_text():
                return False
        return False

    def _manual_login(self, hint, wait=300):
        """自动登录没成功（密码不对、要人机验证、页面改版……）：把浏览器拿到屏幕上，等你自己登录一次（最多 5 分钟）。
        登录好了照常接着做，登录信息存下来，7 天内不用再登。"""
        self._log("⚠ 自动登录没成功（%s）：浏览器已经拿到屏幕上，请你在里面登录一次（要验证就完成验证），"
                  "软件看到登录成功就接着做" % (hint or "点了登录还停在登录页"))
        _live_set(stage="等你在弹出的浏览器里登录 sorryios（最多等 5 分钟）", stage_at=time.time())
        self._safe(lambda: self._set_window_visible(True))
        ok = self._wait_left_login(wait)
        if ok:
            self._log("✓ 你登录好了，接着做")
            self._ready_deadline = time.time() + _READY_LIMIT
            if load_config().get("browserHidden", True):
                self._safe(lambda: self._set_window_visible(False))
        return ok

    def _login_error_text(self):
        return self._safe(lambda: self._page.evaluate(r"""() => {
            const out = [];
            for (const el of document.querySelectorAll('[class*="message"],[class*="toast"],[class*="notification"],[class*="error"],[class*="alert"],[role="alert"]')) {
                const r = el.getBoundingClientRect();
                const t = (el.innerText || '').trim();
                if (r.width > 0 && r.height > 0 && t && t.length < 120 && !out.includes(t)) out.push(t);
            }
            const bad = /错误|不正确|失败|不存在|已过期|过期|锁定|冻结|频繁|验证码|人机|请先|禁止|incorrect|invalid|failed/i;
            for (const el of document.querySelectorAll('body *')) {
                if (out.length >= 3) break;
                const t = (el.innerText || '').trim();
                if (!t || t.length > 60 || el.children.length > 2 || !bad.test(t) || out.includes(t)) continue;
                const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
                if (r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none') out.push(t);
            }
            return out.slice(0, 3).join(' / ');
        }"""), "") or ""

    def _open_login_page(self):
        paths = [self._site_path] + [p for p in KNOWN_SITE_PATHS if p != self._site_path]
        for p in paths:
            url = _login_url_for(p)
            self._log("打开登录页 " + url)
            self._safe(lambda u=url: self._page.goto(u, wait_until="domcontentloaded",
                                                     timeout=30000))
            try:
                self._page.wait_for_selector('input[type="password"]', state="visible",
                                             timeout=12000)
            except Exception:
                self._log("  该地址没有出现登录表单")
                continue
            if p != self._site_path:
                self._log("⚠ 配置的路径 /%s 不可用，自动改用 /%s（可在设置里改 sitePath）"
                          % (self._site_path, p))
                self._site_path = p
                self._carlist_url = _carlist_url_for(p)
            self._login_url = url
            return
        raise RuntimeError("打开登录页失败：%s 都没有出现密码框，sorryios.ai 可能又改版了"
                           % "、".join("/" + x for x in paths))

    def _do_login(self, cfg):
        self._open_login_page()
        time.sleep(0.5 + random.random() * 0.5)
        self._dismiss_popups(2.5)       # 登录页打开会弹「注册即可免费试用…」公告

        pwd = self._page.locator('input[type="password"]:visible').first
        user = self._page.locator(
            'input:not([type="password"]):not([type="checkbox"]):not([type="radio"])'
            ':not([type="hidden"]):not([type="submit"]):not([type="button"]):visible').first
        if not self._safe(lambda: user.count(), 0):
            raise RuntimeError("登录页找不到账号输入框，sorryios.ai 可能改版了")

        self._safe(lambda: user.focus()); time.sleep(0.3); user.fill("")
        self._human_type(user, cfg["aiUsername"])
        self._log("已输入账号")
        time.sleep(0.5)
        self._safe(lambda: pwd.focus()); time.sleep(0.3); pwd.fill("")
        self._human_type(pwd, cfg["aiPassword"])
        self._log("已输入密码")
        time.sleep(0.5)

        self._dismiss_popups(0.3)
        self._ensure_agreement_checked()
        time.sleep(0.3)

        btn = self._find_login_button()
        if btn:
            self._safe(lambda: btn.click(timeout=5000))
            self._log("已点击登录")
        else:
            pwd.press("Enter")
            self._log("没找到登录按钮，在密码框里按了回车")

        deadline = time.time() + 20
        nudged = False
        while time.time() < deadline:
            time.sleep(1)
            st = self._page_status()
            if not st.get("isLoginPage"):
                self._log("✓ 登录成功，落地页 " + st.get("url", ""))
                self._landing_url = st.get("url", "")
                self._dismiss_popups(2.0)   # 登录后首页也可能弹公告
                break
            # 没勾协议时有的站会弹框「请先同意…」，点掉后再登一次
            if not nudged and time.time() > deadline - 16:
                nudged = True
                if self._dismiss_agreement_dialog():
                    self._log("点掉了协议提示弹窗，重新登录")
                    time.sleep(0.5)
                    self._ensure_agreement_checked()
                    btn = self._find_button_by_text("用户登录", "登录", "登 录", "Login", "Sign in")
                    if btn:
                        self._safe(lambda: btn.click())
        else:
            hint = self._login_error_text()
            ok = (not hint) and self._submit_login_other_ways(pwd)
            if not ok:
                ok = self._manual_login(hint)
            if not ok:
                raise RuntimeError("登录失败，仍停留在登录页" +
                                   ("：" + hint if hint else "（账号密码错误，或页面又改版了）") +
                                   "；你也没在弹出的浏览器里登录")

        time.sleep(1.5)
        if not self._goto_carlist():
            raise RuntimeError("登录成功了，但找不到卡片列表页（页面结构可能变了，"
                               "诊断截图已保存到 memory/web_model_diag/）")

    # ════════════════════ 选卡 + 进聊天页 ════════════════════
    def _select_card_and_enter_chat(self):
        for attempt in range(3):
            try:
                self._select_random_card()
            except Exception as e:
                self._log("选卡异常: " + str(e))
            ready = self._wait_chat_page_ready(25)
            if ready is True:
                self._chat_epoch += 1
                self._chat_used = False
                return True
            if ready == "login_redirect":
                self._log("↻ session 失效，重新登录...")
                _clear_session()
                self._do_login(load_config())
                try:
                    _save_session(self._context.storage_state())
                except Exception:
                    pass
                continue   # 不消耗 attempt（与参考一致：重登后重选）
            self._log("进入聊天页失败，第 %d 次重试" % (attempt + 1))
            self._safe(lambda: self._page.goto(self._carlist_url,
                       wait_until="domcontentloaded", timeout=30000))
            time.sleep(3)
        raise RuntimeError("选卡进入聊天页失败（已重试 3 次）")

    def _select_random_card(self):
        self._log("选 AI 卡片中...")
        if not self._goto_carlist():
            if self._page_status().get("isLoginPage"):
                return            # 交给 _wait_chat_page_ready 报 login_redirect → 重登
            raise RuntimeError("打不开卡片列表页")
        time.sleep(1.5 + random.random() * 1.5)
        self._dismiss_popups(0.5)

        # 在【当前视口】里扫所有 Plus/Team 卡，返回 [{name, status}]。
        scan_js = """() => {
            const R = [];
            for (const el of document.querySelectorAll('*')) {
                const r = el.getBoundingClientRect();
                if (r.bottom < 0 || r.top > window.innerHeight ||
                    r.width < 150 || r.width > 460 || r.height < 70 || r.height > 280) continue;
                const t = el.innerText || '';
                const m = t.match(/[A-Z]{2}\\d{4}-\\d{2}/);
                const hasTeamOrPlus = t.includes('TEAM') || t.includes('PLUS') ||
                                      t.includes('Plus') || t.includes('PRO') || !!m;
                if (!hasTeamOrPlus) continue;
                let status = '';
                if (t.includes('空闲')) status = '空闲';
                else if (t.includes('繁忙')) status = '繁忙';
                else if (t.includes('正常')) status = '正常';
                else continue;
                if (m) R.push({ name: m[0], status });
            }
            return R;
        }"""

        # 一次滚动整页，收齐所有卡（按卡名去重，保留最优状态）
        buckets = {"空闲": set(), "正常": set(), "繁忙": set()}
        seen = {}
        self._safe(lambda: self._page.evaluate("window.scrollTo(0, 0)"))
        time.sleep(0.6)
        total = self._safe(lambda: self._page.evaluate(
            "() => document.body.scrollHeight"), 3000) or 3000
        vh = self._safe(lambda: self._page.evaluate(
            "() => window.innerHeight"), 800) or 800
        step = int(vh * 0.85) or 600
        y = 0
        for _ in range(50):     # 最多翻 50 屏，覆盖几百张卡
            got = self._safe(lambda: self._page.evaluate(scan_js), []) or []
            for c in got:
                nm, st = c.get("name"), c.get("status")
                if nm and st in buckets:
                    if nm not in seen:
                        seen[nm] = st
                        buckets[st].add(nm)
            if y >= total:
                break
            y += step
            self._safe(lambda yy=y: self._page.evaluate("window.scrollTo(0, %d)" % yy))
            time.sleep(0.3)

        # 优先 Plus/Team 空闲；没有空闲再用正常；都没有再兜底繁忙
        picked, names = "空闲", list(buckets["空闲"])
        if not names:
            picked, names = "正常", list(buckets["正常"])
        if not names:
            picked, names = "繁忙", list(buckets["繁忙"])
        if not names:
            raise RuntimeError("页面上找不到任何 Plus/Team 卡（空闲/正常/繁忙都没有）")

        random.shuffle(names)
        chosen = names[0]
        tag = "【繁忙·兜底】" if picked == "繁忙" else "【%s】" % picked
        self._log("空闲%d/正常%d/繁忙%d 张 → 随机选中%s: %s" % (
            len(buckets["空闲"]), len(buckets["正常"]), len(buckets["繁忙"]), tag, chosen))

        # 按卡名把它滚到视口中央再点
        if not self._click_card_by_name(chosen):
            raise RuntimeError("选中卡 %s 但点击失败（页面结构可能变了）" % chosen)
        time.sleep(2)

    def _click_card_by_name(self, name):
        coords = self._safe(lambda: self._page.evaluate("""(name) => {
            for (const el of document.querySelectorAll('*')) {
                const r = el.getBoundingClientRect();
                if (r.width < 150 || r.width > 460 || r.height < 70 || r.height > 280) continue;
                if ((el.innerText || '').includes(name)) {
                    el.scrollIntoView({block: 'center'});
                    const rr = el.getBoundingClientRect();
                    return { cx: Math.round(rr.x + rr.width/2), cy: Math.round(rr.y + rr.height/2) };
                }
            }
            return null;
        }""", name), None)
        if not coords:
            return False
        time.sleep(0.4)
        before = len(self._context.pages)
        self._page.mouse.click(coords["cx"], coords["cy"])
        time.sleep(1.5)
        self._adopt_new_page(before)
        # ★ 鼠标停在原地，进了聊天页正好压在右下角的悬浮菜单上 → 菜单被悬停展开，
        #   它的半透明遮罩会挡住输入框（之前「卡住不发提示词」就是这个原因）。点完马上挪开。
        self._park_mouse()
        return True

    def _ready_check(self):
        """v121：就位阶段的检查：点了停止就停；网站报错页 / 等太久 → 算 AI 镜像网站打不开。"""
        _check_cancel()
        bad = ""
        try:
            if self._page and not self._page.is_closed():
                bad = self._page.evaluate(_SITE_ERR_JS) or ""
        except Exception:
            bad = ""
        if bad:
            self._ready_deadline = 0
            self._log("⛔ AI 镜像网站打不开：%s" % bad)
            raise SiteDown("AI 镜像网站打不开（%s）" % bad)
        dl = getattr(self, "_ready_deadline", 0)
        if dl and time.time() > dl:
            self._ready_deadline = 0
            self._log("⛔ AI 镜像网站打不开：等了 %d 秒还没进到能提问的页面" % _READY_LIMIT)
            raise SiteDown("AI 镜像网站打不开（等了 %d 秒还没进到能提问的页面）" % _READY_LIMIT)

    def _wait_chat_page_ready(self, timeout_sec=25):
        self._log("等聊天页就绪...")
        carlist_url = self._carlist_url
        start = time.time()
        last_log = 0
        while time.time() - start < timeout_sec:
            time.sleep(2)
            self._ready_check()          # v121
            try:
                info = self._page.evaluate("""(carlistUrl) => {
                    const url = window.location.href;
                    let inputCount = 0;
                    const inputs = [...document.querySelectorAll('textarea'),
                                    ...document.querySelectorAll('[contenteditable="true"]')];
                    for (const el of inputs) {
                        const r = el.getBoundingClientRect();
                        if (r.width > 200 && r.height > 0) inputCount++;
                    }
                    const bt = document.body.innerText || '';
                    const hasPasswordInput = !!document.querySelector('input[type="password"]');
                    return {
                        url, inputCount,
                        hasChatHint: bt.includes('询问任何问题') || bt.includes('有什么可以帮') ||
                                     bt.includes('开始使用') || bt.includes('Send a message'),
                        isCarlist: url.includes('carlist') || url === carlistUrl,
                        isLoginPage: url.includes('/login') || hasPasswordInput,
                    };
                }""", carlist_url)
            except Exception:
                continue
            if info["isLoginPage"]:
                self._log("⚠ 选卡后被重定向到登录页，session 已失效")
                return "login_redirect"
            if (not info["isCarlist"]) and (info["inputCount"] > 0 or info["hasChatHint"]):
                self._log("✓ 聊天页就绪")
                time.sleep(4)     # 冷启动 hydration 缓冲
                self._park_mouse()
                self._close_overlays()
                return True
            if time.time() - last_log > 6:
                self._log("还在等聊天页... inputCount=%s isCarlist=%s"
                          % (info["inputCount"], info["isCarlist"]))
                last_log = time.time()
        return False

    # ════════════════════ 查询 ════════════════════
    def web_complete(self, prompt, on_progress=None, **opts):
        """对外主入口（在 worker 线程内执行）。返回 AI 回复纯文本。"""
        def prog(msg):
            _live_set(stage=str(msg), stage_at=time.time())
            if on_progress:
                self._safe(lambda: on_progress(msg))
        prog("打开网页 / 就位中…")
        _CANCEL_EVT.clear()               # v62：上一条残留的「停止」信号不作数
        self._ready_deadline = time.time() + _READY_LIMIT     # v121：就位最多等这么久
        try:
            self._ensure_started()
        except _Cancelled:
            raise
        except Exception as e:
            m = str(e)
            if any(k in m for k in ("ERR_", "net::", "打开登录页失败", "Timeout", "timeout")):
                self._ready_deadline = 0
                raise SiteDown("AI 镜像网站打不开（%s）" % m.split("\n")[0][:120])
            raise
        self._ready_check()

        # ★ 2026-06 新增：forceNewCard —— 主动换一张新卡再问。
        #   用于 agent 工具循环里碰到「轴卡」（死活不肯输出工具块、一直用文字推辞）时，
        #   由上层（web_model_client）请求换一张卡重抽，直到碰到肯配合的卡。
        if opts.get("newChat") and not opts.get("forceNewCard"):
            if not self._chat_used and not self._has_conversation():
                self._log("[新任务] 当前就是一个刚打开的空白对话，直接用")
            elif opts.get("newTaskCard") or (load_config().get("newTaskMode") or "card") == "card":
                # 用户要求：每个新任务回首页换一张新的 AI，上一个任务的内容一点都带不进来
                self._log("[新任务] 回首页换一张新的 AI 卡")
                prog("新任务：回首页换一张新的 AI…")
                opts = dict(opts, forceNewCard=True)
            else:
                prog("开一个新对话…")
                if not self._new_chat():
                    self._log("[新对话] 页面上开不了新对话，改为回首页换卡")
                    opts = dict(opts, forceNewCard=True)

        if opts.get("forceNewCard"):
            self._log("[换卡] 回首页换一张新卡…")
            prog("换一张 AI 卡片…")
            self._safe(lambda: self._page.goto(self._carlist_url,
                       wait_until="domcontentloaded", timeout=30000))
            time.sleep(3)
            self._select_card_and_enter_chat()
            # 有的卡一进去是上次的对话：再开个新聊天，确保是空白的
            if self._has_conversation():
                self._new_chat()
            self._state = "ready"

        if opts.get("bestModel") and self._best_epoch != self._chat_epoch:
            prog("切换到最高级模型…")
            self._select_best_model()
            self._best_epoch = self._chat_epoch

        self._ready_check()
        self._ready_deadline = 0          # v121：就位完成，下面等回复有自己的看门狗
        disable_switch = bool(opts.get("disableCardSwitch"))
        max_attempts = 1 if disable_switch else 2
        last_err = None
        for attempt in range(1, max_attempts + 1):
            try:
                return self._query_once(prompt, opts, attempt, prog)
            except _Stuck as e:
                last_err = e
                self._state = "ready"
                if attempt < max_attempts and not disable_switch:
                    self._log("[恢复] 卡死，换张卡重试...")
                    prog("上一张卡卡住，换卡重试…")
                    self._safe(lambda: self._page.goto(self._carlist_url,
                               wait_until="domcontentloaded", timeout=30000))
                    time.sleep(3)
                    self._select_card_and_enter_chat()
                    continue
                raise
            except Exception as e:
                self._state = "ready"
                raise e
        raise last_err or RuntimeError("未知错误")

    _HAS_CONVO_JS = r"""() => {
        const sels = ['[data-message-author-role]', '[class*="markdown"]', '[class*="prose"]',
                      '[class*="message-content"]', '[class*="msg-content"]'];
        let n = 0;
        for (const s of sels) {
            for (const el of document.querySelectorAll(s)) {
                const r = el.getBoundingClientRect();
                if (r.width > 100 && r.height > 0 && (el.innerText || '').trim()) n++;
            }
        }
        return n;
    }"""

    def _has_conversation(self):
        return (self._safe(lambda: self._page.evaluate(self._HAS_CONVO_JS), 0) or 0) > 0

    def _new_chat(self):
        """在当前卡上开一个空白新对话，避免不同任务/请求的内容堆在同一个对话线程里互相干扰。
        成功返回 True（并让 chat_epoch +1）。"""
        if not self._page or self._page.is_closed():
            return False
        if not self._has_conversation():
            self._chat_epoch += 1          # 本来就是空对话
            return True

        def ok():
            for _ in range(10):
                time.sleep(0.6)
                if not self._has_conversation() and self._safe(lambda: self._page.evaluate(
                        "() => [...document.querySelectorAll('textarea,[contenteditable=\"true\"]')]"
                        ".some(e => e.getBoundingClientRect().width > 200)"), False):
                    self._chat_epoch += 1
                    self._chat_used = False
                    self._log("✓ 已开新对话")
                    time.sleep(1.0)
                    return True
            return False

        for sel in ('[data-testid="create-new-chat-button"]',
                    'a[aria-label*="New chat" i]', 'button[aria-label*="New chat" i]',
                    'a[aria-label*="新聊天"]', 'button[aria-label*="新聊天"]',
                    'a[aria-label*="新对话"]', 'button[aria-label*="新对话"]'):
            loc = self._page.locator(sel).first
            if self._safe(lambda: loc.count(), 0) and self._safe(lambda: loc.is_visible(), False):
                clicked = self._safe(lambda: (loc.evaluate("el => el.click()"), True)[1], False) \
                    or self._safe(lambda: (loc.click(timeout=3000), True)[1], False)
                if clicked and ok():
                    return True
        for txt in ("新聊天", "新对话", "New chat"):
            if self._click_text(txt) and ok():
                return True
        # ChatGPT 的「新聊天」快捷键
        self._safe(lambda: self._page.keyboard.press("Control+Shift+O"))
        if ok():
            return True
        self._log("⚠ 没能开新对话（找不到「新聊天」入口）")
        return False

    # ──────────── 切换到最高级模型（分析类任务用）────────────
    _MODEL_BTN_JS = r"""() => {
        const re = /(\b\d+(\.\d+)?\b|instant|mini|low|medium|high|pro|thinking|auto|heavy|extended|light|standard|即时|思考|专业|标准|进阶)/i;
        const ins = [...document.querySelectorAll('textarea,[contenteditable="true"]')]
            .filter(e => e.getBoundingClientRect().width > 200);
        let scope = ins.length ? (ins[ins.length - 1].closest('form') || ins[ins.length - 1].parentElement) : null;
        for (let i = 0; i < 5 && scope && scope.parentElement && scope.querySelectorAll('button').length < 3; i++)
            scope = scope.parentElement;
        const cands = [];
        const consider = (b, bonus) => {
            const r = b.getBoundingClientRect();
            const t = (b.innerText || '').trim().split('\n')[0];
            const al = b.getAttribute('aria-label') || '';
            if (r.width === 0 || r.height === 0) return;
            if (/发送|send|附件|attach|语音|voice|dictat|上传|upload|麦克风|mic/i.test(t + ' ' + al)) return;
            if (!(re.test(t) || /model|模型/i.test(al))) return;
            if (t.length > 30) return;
            const pop = b.hasAttribute('aria-haspopup') || b.hasAttribute('aria-expanded');
            cands.push({b, t, score: bonus + (pop ? 5 : 0) + (b.querySelector('svg') ? 1 : 0)});
        };
        document.querySelectorAll('[data-testid*="model-switcher"],[data-testid*="model-picker"],button[aria-label*="模型"],button[aria-label*="model" i]')
            .forEach(b => consider(b, 10));
        if (scope) scope.querySelectorAll('button,[role="button"]').forEach(b => consider(b, 3));
        document.querySelectorAll('[data-cx-model-btn]').forEach(e => e.removeAttribute('data-cx-model-btn'));
        if (!cands.length) return null;
        cands.sort((a, b) => b.score - a.score);
        cands[0].b.setAttribute('data-cx-model-btn', '1');
        return cands[0].t || (cands[0].b.getAttribute('aria-label') || '');
    }"""

    _MODEL_MENU_JS = r"""() => {
        const els = [...document.querySelectorAll('[role="menuitem"],[role="menuitemradio"],[role="option"]')]
            .filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; });
        return els.map((e, i) => {
            e.setAttribute('data-cx-mi', String(i));
            const full = (e.innerText || '').trim().replace(/\s+\n/g, '\n');
            return {i, label: full.split('\n')[0].trim().slice(0, 60), full: full.replace(/\s+/g, ' ').slice(0, 90),
                    disabled: e.getAttribute('aria-disabled') === 'true' || e.hasAttribute('data-disabled'),
                    checked: e.getAttribute('aria-checked') === 'true' || e.getAttribute('data-state') === 'checked'
                             || e.getAttribute('aria-selected') === 'true',
                    sub: e.getAttribute('aria-haspopup') === 'menu' || e.hasAttribute('data-has-submenu')};
        });
    }"""

    @staticmethod
    def _model_rank(label):
        """给菜单里的模型/思考强度打分，越高越强。只看第一行名称，不看说明文字。"""
        import re as _re
        t = (label or "").lower()
        if not t or _re.search(r"upgrade|升级|unavailable|不可用|legacy|旧版|temporary|临时", t):
            return -1
        tiers = [(r"\bpro\b|专业", 100), (r"extra.?high|xhigh|heavy|\bmax\b|extended|极高|超高|深度", 90),
                 (r"\bhigh\b|(?<!极|超)高", 80), (r"thinking|思考|reason|推理", 70),
                 (r"medium|standard|标准|中", 50), (r"\bauto\b|自动", 40),
                 (r"\blow\b|light|低|轻", 20), (r"instant|mini|fast|nano|即时|极速|快", 10)]
        score = 0
        for pat, sc in tiers:
            if _re.search(pat, t):
                score = max(score, sc)
        nums = [float(x) for x in _re.findall(r"(\d+(?:\.\d+)?)", t) if float(x) < 50]
        return score + (max(nums) if nums else 0) / 10.0       # 同档位里版本号大的优先

    _SLIDER_JS = r"""() => {
        const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
        document.querySelectorAll('[data-cx-slider]').forEach(e => e.removeAttribute('data-cx-slider'));
        const out = [];
        for (const s of document.querySelectorAll('[role="slider"], input[type="range"]')) {
            if (!vis(s)) continue;
            const rg = s.tagName === 'INPUT';
            const num = (v, d) => { const x = parseFloat(v); return isNaN(x) ? d : x; };
            s.setAttribute('data-cx-slider', String(out.length));
            out.push({i: out.length, range: rg,
                      min: num(rg ? s.min : s.getAttribute('aria-valuemin'), 0),
                      max: num(rg ? s.max : s.getAttribute('aria-valuemax'), 100),
                      now: num(rg ? s.value : s.getAttribute('aria-valuenow'), 0),
                      step: num(rg ? s.step : null, 1),
                      text: s.getAttribute('aria-valuetext') || ''});
        }
        return out;
    }"""

    _DOM_CLICK_JS = r"""(sel) => {
        const b = document.querySelector(sel); if (!b) return false;
        for (const t of ['pointerdown', 'mousedown', 'pointerup', 'mouseup', 'click'])
            b.dispatchEvent(new (t.startsWith('pointer') ? PointerEvent : MouseEvent)(t,
                {bubbles: true, cancelable: true, button: 0, pointerType: 'mouse'}));
        return true;
    }"""

    def _menu_items(self):
        return self._safe(lambda: self._page.evaluate(self._MODEL_MENU_JS), []) or []

    def _sliders(self):
        return self._safe(lambda: self._page.evaluate(self._SLIDER_JS), []) or []

    def _dom_click(self, selector):
        """页面内触发一次完整点击（按下/抬起/click），不动你的真实鼠标、不需要窗口在前台。"""
        return bool(self._safe(lambda: self._page.evaluate(self._DOM_CLICK_JS, selector), False))

    def _open_model_menu(self):
        """打开聊天框里的模型 / 思考强度面板。先用页面内事件，不行再用虚拟鼠标点一下。"""
        for how in ("dom", "click"):
            if how == "dom":
                self._dom_click('[data-cx-model-btn="1"]')
            else:
                self._safe(lambda: self._page.locator('[data-cx-model-btn="1"]').first.click(timeout=4000))
            for _ in range(8):
                time.sleep(0.25)
                if self._menu_items() or self._sliders():
                    return True
        return False

    def _slider_now(self, i):
        return next((x for x in self._sliders() if x["i"] == i), None)

    def _slider_to_max(self, sl):
        """把「思考强度」滑块拉到最右（最强）。依次试：页面内 End 键 → 键盘 End/→ → 点轨道最右端。"""
        sel = '[data-cx-slider="%d"]' % sl["i"]
        if sl["range"]:
            self._safe(lambda: self._page.evaluate("""(sel) => {
                const s = document.querySelector(sel);
                Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(s, s.max);
                s.dispatchEvent(new Event('input', {bubbles: true}));
                s.dispatchEvent(new Event('change', {bubbles: true}));
            }""", sel))
        else:
            self._safe(lambda: self._page.evaluate("""(sel) => {
                const s = document.querySelector(sel); s.focus();
                s.dispatchEvent(new KeyboardEvent('keydown', {key: 'End', code: 'End', bubbles: true, cancelable: true}));
            }""", sel))
        time.sleep(0.3)
        cur = self._slider_now(sl["i"])
        if cur and cur["now"] >= cur["max"]:
            return cur
        loc = self._page.locator(sel).first
        self._safe(lambda: loc.press("End", timeout=3000))      # 键盘事件只发给这个页面
        time.sleep(0.3)
        cur = self._slider_now(sl["i"])
        if cur and cur["now"] >= cur["max"]:
            return cur
        steps = int(max(1, (sl["max"] - sl["now"]) / max(sl["step"] or 1, 1e-6))) + 1
        for _ in range(min(steps, 50)):
            self._safe(lambda: loc.press("ArrowRight", timeout=2000))
        time.sleep(0.3)
        cur = self._slider_now(sl["i"])
        if cur and cur["now"] >= cur["max"]:
            return cur
        # 最后一招：在滑轨最右端点一下（虚拟鼠标，不会移动你的真实鼠标）
        box = self._safe(lambda: self._page.evaluate("""(sel) => {
            const s = document.querySelector(sel);
            let t = s.closest('[data-orientation]') || s.parentElement;
            for (let k = 0; k < 3 && t && t.getBoundingClientRect().width < 80; k++) t = t.parentElement;
            const r = (t || s).getBoundingClientRect(); return {x: r.right - 3, y: r.top + r.height / 2};
        }""", sel))
        if box:
            self._safe(lambda: self._page.mouse.click(box["x"], box["y"]))
            time.sleep(0.3)
        return self._slider_now(sl["i"])

    @staticmethod
    def _has_effort(label):
        import re as _re
        return bool(_re.search(r"instant|mini|\blow\b|medium|\bhigh\b|\bpro\b|thinking|auto|heavy|extended|"
                               r"light|standard|即时|思考|专业|标准|极高|超高|高|中|低", (label or "").lower()))

    @staticmethod
    def _version(label):
        import re as _re
        nums = [float(x) for x in _re.findall(r"(\d+(?:\.\d+)?)", label or "") if float(x) < 50]
        return max(nums) if nums else None

    def _panel_head(self):
        """面板标题行，如「6 Medium」「6 High」：带版本号又带强度词的那一项。"""
        return next((it["label"] for it in self._menu_items()
                     if self._version(it["label"]) is not None and self._has_effort(it["label"])), "")

    def _select_best_model(self):
        """分析类任务开始前，把 AI 池切到最高级：
          ① 模型：选版本号最高的（或配置 preferredModel 指定的）；
          ② 思考强度：有滑块就拉到最右；是选项列表就选最强的一项。
        找不到就保持原样继续，不影响任务；每一步都写日志，方便对照修。"""
        try:
            self._close_overlays()
            btn = self._safe(lambda: self._page.evaluate(self._MODEL_BTN_JS), None)
            if not btn:
                self._log("[模型] 没找到聊天框里的模型/思考强度按钮，按页面默认继续")
                return False
            if not self._open_model_menu():
                self._log("[模型] 点了「%s」但没弹出面板，按默认继续" % btn)
                return False
            items = self._menu_items()
            head = self._panel_head()
            self._log("[模型] 按钮「%s」，当前「%s」，选项：%s，滑块：%d 个" % (
                btn, head or "-", " / ".join(("✓" if it["checked"] else "") + it["label"]
                                             for it in items if it["label"]) or "-", len(self._sliders())))
            want = (load_config().get("preferredModel") or "").strip().lower()

            # ① 模型：只看「不带强度词」的选项（如「6」「GPT-5.6 Sol」），默认挑版本号最高的
            models = [it for it in items if it["label"] and not it["disabled"]
                      and not self._has_effort(it["label"]) and self._model_rank(it["label"]) >= 0]
            pick = None
            if want:
                pick = next((it for it in models if want in it["label"].lower()), None)
            if not pick and models:
                pick = max(models, key=lambda it: (self._version(it["label"]) or 0, it["checked"]))
            if pick and not pick["checked"]:
                self._dom_click('[data-cx-mi="%d"]' % pick["i"])
                time.sleep(0.6)
                self._log("[模型] 选模型「%s」" % pick["label"])
                if not (self._menu_items() or self._sliders()):     # 选完面板关了：重新打开
                    self._open_model_menu()

            # ② 思考强度
            done = ""
            sliders = self._sliders()
            if sliders:
                sl = sliders[0]
                cur = self._slider_to_max(sl)
                if cur:
                    done = "思考强度滑块 %g→%g（最大 %g）%s" % (
                        sl["now"], cur["now"], cur["max"],
                        "，已拉满" if cur["now"] >= cur["max"] else "，⚠ 没能拉满")
            else:
                items = self._menu_items()
                efforts = [it for it in items if it["label"] and not it["disabled"]
                           and self._has_effort(it["label"]) and self._model_rank(it["label"]) >= 0]
                pure = [it for it in efforts if self._version(it["label"]) is None]
                combos = [it for it in efforts if self._version(it["label"]) is not None]
                cands = pure or (combos if len(combos) >= 2 else [])    # 只有一个「6 Medium」是标题，不算选项
                if want:
                    cands = [it for it in cands if want in it["label"].lower()] or cands
                if cands:
                    best = max(cands, key=lambda it: self._model_rank(it["label"]))
                    if not best["checked"]:
                        self._dom_click('[data-cx-mi="%d"]' % best["i"])
                        time.sleep(0.5)
                    done = "思考强度选「%s」" % best["label"]
            after = self._panel_head()
            if self._menu_items() or self._sliders():
                self._safe(lambda: self._page.keyboard.press("Escape"))
                time.sleep(0.2)
            self._log("[模型] 完成：%s；当前「%s」" % (done or "没有可调的思考强度", after or head or btn))
            return True
        except Exception as e:
            self._log("[模型] 切换出错（%s），按默认继续" % str(e)[:80])
            return False

    def _park_mouse(self):
        """把鼠标挪到页面左上方的空白处，免得悬停触发右下角的悬浮菜单。"""
        try:
            vp = self._page.viewport_size or {"width": 1280, "height": 900}
            self._page.mouse.move(int(vp["width"] * 0.45), 70)
        except Exception:
            pass

    _OVERLAY_OPEN_JS = r"""() => [...document.querySelectorAll(
        '.radial-menu-backdrop.open, #main-menu-backdrop.open')].filter(e => {
            const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; }).length"""

    def _close_overlays(self):
        """关掉 AI 池页面上展开的悬浮菜单（右下角齿轮那一圈按钮）。它展开时会盖一层
        半透明遮罩，挡住输入框和发送键。返回是否处理过。"""
        if not (self._safe(lambda: self._page.evaluate(self._OVERLAY_OPEN_JS), 0) or 0):
            return False
        self._log("检测到悬浮菜单展开（遮挡输入框），正在关闭…")
        self._park_mouse()
        # 1) 点遮罩本身（一般就是「点空白处关闭」）
        self._safe(lambda: self._page.evaluate(r"""() => {
            for (const b of document.querySelectorAll('.radial-menu-backdrop.open, #main-menu-backdrop.open'))
                b.dispatchEvent(new MouseEvent('click', {bubbles: true}));
        }"""))
        time.sleep(0.4)
        # 2) 还开着就按 Esc
        if self._safe(lambda: self._page.evaluate(self._OVERLAY_OPEN_JS), 0):
            self._safe(lambda: self._page.keyboard.press("Escape"))
            time.sleep(0.4)
        # 3) 仍然开着：直接让遮罩失效（不影响页面其它功能）
        if self._safe(lambda: self._page.evaluate(self._OVERLAY_OPEN_JS), 0):
            self._safe(lambda: self._page.evaluate(r"""() => {
                for (const b of document.querySelectorAll('.radial-menu-backdrop, #main-menu-backdrop')) {
                    b.classList.remove('open'); b.style.pointerEvents = 'none';
                }
                for (const c of document.querySelectorAll('.radial-menu-container, #main-menu-container'))
                    c.classList.remove('open');
            }"""))
        return True

    def _click_marked(self):
        """真实点击 _BLOCKER_JS 标记好的按钮；点不动就强制点 / 页面内点。"""
        loc = self._page.locator('[data-cx-click="1"]').first
        for how in ("normal", "force", "js"):
            try:
                if how == "normal":
                    loc.click(timeout=3000)
                elif how == "force":
                    loc.click(timeout=3000, force=True)
                else:
                    loc.evaluate("el => el.click()")
                return True
            except Exception:
                continue
        return False

    def _handle_blockers(self, prompt="", st=None, allow_retry=True):
        """处理会让流程卡住的页面提示。返回 None（没事）或做了什么的说明。
        额度用完 / 反复出错 → 抛 _Stuck，让上层立刻换一张卡。
        st：本次提问共用的状态（重试次数、对比框长度记录）。"""
        st = st if st is not None else {}
        info = self._safe(lambda: self._page.evaluate(_BLOCKER_JS), None) or {}
        if not info:
            return None
        norm = lambda x: re.sub(r"\s+", "", x or "")
        ptxt = norm(prompt)

        def from_prompt(t):          # 提示文字其实是我们自己发的内容（文字稿里的原话）→ 不算
            return bool(t) and len(norm(t)) >= 6 and norm(t) in ptxt

        if info.get("compare"):
            if info.get("click") == "skip":
                self._log("检测到「%s」对比框 → 自动点「跳过」" % (info.get("text") or "你更喜欢哪个"))
                self._click_marked()
                time.sleep(1.5)
                return "skip"
            if info.get("click") == "prefer":
                lens = info.get("lens") or []
                prev = st.get("cmp_lens")
                st["cmp_lens"] = lens
                # 两边都写完（长度不再变）再选，选内容更长的那个
                if prev == lens and lens:
                    self._log("检测到对比框（没有跳过按钮）→ 选内容更长的那个回复（%s 字）" % lens)
                    self._click_marked()
                    st["cmp_lens"] = None
                    time.sleep(1.5)
                    return "prefer"
                return "compare-wait"
            return "compare-wait"
        q = info.get("quota") or ""
        if q and not from_prompt(q):
            self._log("⚠ 这张卡额度用完了（%s）→ 立刻换卡" % q[:60])
            raise _Stuck("这张卡额度用完：%s" % q[:60])
        e = info.get("error") or ""
        if e and allow_retry and not from_prompt(e):
            n = st.get("retries", 0)
            if info.get("click") == "retry" and n < 2:
                st["retries"] = n + 1
                self._log("⚠ AI 池提示「%s」→ 自动点重试（第 %d 次）" % (e[:50], n + 1))
                self._click_marked()
                time.sleep(2)
                return "retry"
            if n >= 2 or not info.get("click"):
                since = st.setdefault("err_since", time.time())
                if n >= 2 or time.time() - since > 30:
                    self._log("⚠ AI 池一直报错（%s）→ 换卡重试" % e[:50])
                    raise _Stuck("AI 池报错：%s" % e[:60])
        else:
            st.pop("err_since", None)
        return None

    def _focus_input(self, inp):
        """聚焦输入框：正常点击 → 关遮挡后再点 → 强制点击 → JS focus，一级级兜底。"""
        try:
            inp.click(timeout=3000)
            return
        except Exception as e:
            self._log("点输入框被挡住（%s），关遮挡后重试" % str(e).split("\n")[0][:80])
        self._close_overlays()
        try:
            inp.click(timeout=3000)
            return
        except Exception:
            pass
        try:
            inp.click(timeout=3000, force=True)
            return
        except Exception:
            pass
        inp.evaluate("el => { el.focus(); }")

    # 本次提问之后的那条助手回复（按页面顺序定位在「我刚发的提问气泡」后面），
    # 用来校验抓到的回复确实属于本次任务，而不是对话里更早的内容。
    _ANCHORED_REPLY_JS = r"""(head) => {
        const norm = s => (s || '').replace(/[\s\u00a0]+/g, '');
        const key = norm(head).slice(0, 30);
        const users = [...document.querySelectorAll('[data-message-author-role="user"]')];
        if (!users.length) return {found: false};
        let anchor = null;
        for (let i = users.length - 1; i >= 0; i--) {
            if (key && norm(users[i].innerText).includes(key)) { anchor = users[i]; break; }
        }
        if (!anchor) return {found: false};
        const outs = [];
        for (const a of document.querySelectorAll('[data-message-author-role="assistant"]')) {
            if (anchor.compareDocumentPosition(a) & Node.DOCUMENT_POSITION_FOLLOWING) {
                const t = (a.innerText || '').trim();
                if (t) outs.push(t);
            }
        }
        return {found: true, text: outs.join('\n\n')};
    }"""

    def _anchored_reply(self, prompt):
        return self._safe(lambda: self._page.evaluate(self._ANCHORED_REPLY_JS, prompt or ""),
                          {"found": False}) or {"found": False}

    def _wait_anchored_stable(self, prompt, timeout_sec, prog=None):
        """等「本次提问之后的回复」出现并且连续几秒不再变化，返回它的文字。"""
        end = time.time() + timeout_sec
        last, same_n = "", 0
        while time.time() < end:
            t = ((self._anchored_reply(prompt) or {}).get("text") or "").strip()
            if t and t == last:
                same_n += 1
                if same_n >= 3:
                    return t
            else:
                same_n = 0
                last = t
            time.sleep(1.5)
        return last

    @staticmethod
    def _same_reply(a, b):
        """两段文字是否像是同一条回复（去掉空白和 Markdown 符号后，开头一段互相包含）。
        v139：行首的序号「1. 」不算——网页上有序列表的序号是画出来的，读纯文字时没有，只有 Markdown 版有。
              以前每条都很短时（贴标签一行一篇），就因为多了「1.」「2.」被认成不是同一条，
              Markdown 版被丢掉、序号也跟着丢了，贴标签就一直「格式不对」。链接后面的网址也不算。"""
        import re as _re

        def norm(s):
            s = _re.sub(r"(?m)^[ \t\u00a0]*\d{1,3}[\.\)．][ \t\u00a0]*", "", s or "")
            s = _re.sub(r"\]\((?:https?:|cx-webimg:)[^)\s]*\)", "]", s)
            return _re.sub(r"[\s\u00a0*_#`>|\-\[\]()!]+", "", s)
        na, nb = norm(a), norm(b)
        if not na or not nb:
            return False
        k = min(40, len(na), len(nb))
        return na[:k] in nb or nb[:k] in na

    def _capture_baseline(self):
        js = """() => {
            const selectors = ['[class*="markdown"]','[class*="prose"]','[class*="message-content"]',
                '[class*="msg-content"]','[class*="assistant"]','[class*="response"]',
                '[class*="reply-content"]','[class*="answer"]','[data-message-author-role="assistant"]'];
            const c = [];
            for (const sel of selectors) {
                let els; try { els = document.querySelectorAll(sel); } catch(e) { continue; }
                for (const el of els) {
                    const r = el.getBoundingClientRect();
                    const t = (el.innerText || '').trim();
                    if (r.width > 200 && t.length > 30) c.push({text:t, bottom:r.bottom, length:t.length});
                }
            }
            if (!c.length) return null;
            c.sort((a,b)=>b.bottom-a.bottom);
            const topY = c[0].bottom;
            const near = c.filter(x=>topY-x.bottom<200);
            near.sort((a,b)=>b.length-a.length);
            return { text: near[0].text, count: c.length };
        }"""
        return self._safe(lambda: self._page.evaluate(js), None)

    def _find_input(self):
        """
        找 AI 输入框。
        ★修复：Playwright Python 的 is_visible() 不接受 timeout 参数（JS 版接受），
          原来写 is_visible(timeout=1000) 会抛 TypeError 被吞掉 → 全部失配。
        做法：先用一组选择器试可见元素；找不到再用 JS 在页面下半部选出最大的
          可编辑元素打标记，回拿 locator。带 ~8 秒重试，兼容冷启动 hydration。
        """
        selectors = [
            'textarea[placeholder*="问" i]', 'textarea[placeholder*="消息" i]',
            'textarea[placeholder*="message" i]', 'textarea[placeholder*="ask" i]',
            '#prompt-textarea', 'div[contenteditable="true"]',
            '[contenteditable="true"]', '[role="textbox"]',
            'textarea:not([readonly])', 'textarea',
        ]
        deadline = time.time() + 8
        while time.time() < deadline:
            # 1) 直接用选择器（注意：is_visible 不传 timeout）
            for sel in selectors:
                try:
                    loc = self._page.locator(sel).last
                    if loc.count() and loc.is_visible():
                        # 打标记，供 _MARK_SEND_JS 按这一行定位发送键
                        self._safe(lambda l=loc: l.evaluate(
                            "el => { document.querySelectorAll('[data-cx-input]')"
                            ".forEach(e=>e.removeAttribute('data-cx-input'));"
                            " el.setAttribute('data-cx-input','1'); }"))
                        return loc
                except Exception:
                    pass
            # 2) JS 兜底：在页面下半部选出面积最大的可编辑框，打标记后回拿
            marked = self._safe(lambda: self._page.evaluate(_FIND_INPUT_JS), None)
            if marked:
                try:
                    loc = self._page.locator('[data-cx-input="1"]').last
                    if loc.count():
                        return loc
                except Exception:
                    pass
            time.sleep(0.5)
        raise RuntimeError("找不到 AI 输入框 — sorryios.ai 页面结构可能变了")

    def _query_once(self, prompt, opts, attempt, prog):
        self._state = "busy"
        self._quiet_shots = True          # 填字/发送这几秒不截图；开始等回复后恢复
        timeout_ms = opts.get("timeout") or 600000
        self._log("发送 prompt (len=%d, 第%d次)..." % (len(prompt), attempt))

        self._park_mouse()
        self._close_overlays()
        # 上一轮留下的「你更喜欢哪个回复」对比框会锁住输入框；额度用完的卡直接换掉
        blk = {}
        for _ in range(4):
            act = self._handle_blockers(prompt, blk, allow_retry=False)
            if not act:
                break
            time.sleep(1.5)
        if self._safe(lambda: self._page.evaluate("() => document.visibilityState"), "visible") == "hidden":
            self._log("⚠ AI 池的浏览器窗口被最小化了。Chrome 会暂停最小化窗口里的页面，回复可能出不来。"
                      "让它待在别的窗口后面没关系，但别最小化；或者在「设置」里取消「显示浏览器窗口」改成后台运行。")
            prog("提示：AI 池窗口被最小化了，可能会变慢")
        baseline = self._capture_baseline()
        inp = self._find_input()
        self._log("已定位输入框，准备填入…")
        time.sleep(1.0)

        pre = self._fill_prompt(inp, prompt)
        _check_cancel()

        # ── 发送 ──
        # ★核心修复★ 发送成功的判定【不再只看输入框是否清空】：
        #   新版 ChatGPT 5.5 的输入区是 ProseMirror contenteditable，发出去后清空有延迟、
        #   还会重建 DOM 节点 —— 于是 _read_input_text 常常读到“旧的 12 个字”，让程序
        #   误判“没发出去”，接着重复点/重复 Enter（这时 UI 已经在生成了），最后抛“发送未触发”。
        #   这正是之前一直发不出去的真凶（交接报告 §6.a）。
        # 现在改成【看页面状态】判断是否真的发出去了（交接报告 §6.4 的首选方案）：
        #   ① 出现“停止■”按钮（genState=generating）＝AI 已收到、正在生成；或
        #   ② 整页文字明显变长（页面上多了你的提问气泡 / 开始出现回复）；或
        #   ③ 输入框确实清空（保留为辅助信号，但不再是唯一依据）。
        #   任一成立即视为发送成功。
        # 发送动作本身优先用“可操作点击”按钮（Playwright 自动滚动入视、等可点、避开悬浮遮挡层，
        #   比裸坐标点击稳得多，对应参考实现 ai-runner.js 的做法），找不到再退到
        #   Enter / 坐标点击 / 指针事件兜底。
        prog("已填好，点击发送…")
        pre_page_len = self._page_text_len()
        self._log("发送前页面文字 %d 字，开始发送…" % pre_page_len)
        sent = False
        for label, action in (
            ("发送按钮·页面直点", lambda: self._dom_click_send()),
            ("发送按钮·可操作点击", lambda: self._click_send_btn()),
            ("Enter", lambda: self._press_send_key(inp)),
            ("发送键·坐标兜底", lambda: self._click_send(mechanism="mouse")),
            ("发送键·指针事件兜底", lambda: self._click_send(mechanism="js_events")),
        ):
            self._log("尝试发送方式：%s" % label)
            self._safe(action)
            if self._wait_send_committed(pre_page_len, inp, pre, label):
                sent = True
                break
        if not sent:
            # 抛 _Stuck，让上层 web_complete 自动换一张卡重试（比直接失败更稳）
            raise _Stuck("发送未触发：按钮/Enter/坐标/指针事件都没把消息发出去（换卡重试）")

        self._chat_used = True
        reply = self._wait_for_reply(timeout_ms, baseline, prompt, opts, prog)
        # ★ 校验：回复必须是「本次提问之后」的那条。对话里有旧内容时，按位置找最底部的块
        #   可能抓到上一个任务的回复（之前视频笔记里出现整篇新闻简报就是这样来的）。
        anc = self._anchored_reply(prompt)
        if anc.get("found"):
            atext = (anc.get("text") or "").strip()
            if not atext or not self._same_reply(reply, atext):
                # 本次提问之后还没有（完整的）回复：多等一会儿，等它写完再取
                atext = self._wait_anchored_stable(prompt, 180, prog) or atext
            if atext and not self._same_reply(reply, atext):
                self._log("⚠ 抓到的回复不是本次提问的（%d 字），改用本次提问之后的回复（%d 字）"
                          % (len(reply or ""), len(atext)))
                reply = atext
        # 把回复重新抓成 Markdown：把 <a href> 还原成可点击链接 [文字](网址)，
        # 并去掉 ChatGPT 的引用角标杂质（如 "OpenAI +1"、"Anthropic +2"）。
        # 仅当抓取结果可信（长度不大幅缩水）才采用，否则保留纯文本。
        imgs = []
        if opts.get("saveImages"):
            imgs = self._safe(lambda: self._page.evaluate(_MARK_IMAGES_JS, prompt), []) or []
        md = self._safe(lambda: self._page.evaluate(_GRAB_MARKDOWN_JS, prompt), "") or ""
        # 只有和刚才确认过的回复是同一条时才用 Markdown 版（之前只比长度，旧的长消息会顶替掉正确回复）
        if md and len(md) >= max(40, int(len(reply or "") * 0.6)) and self._same_reply(md, reply):
            reply = md
        reply = _clean_reply_text(reply)          # v133：「ChatGPT 说：」「思考了 58s」「重置清单 复制清单」这类整行小字
        if imgs:
            prog("保存回复里的 %d 张图片…" % len(imgs))
            reply = self._save_reply_images(reply, imgs)
        self._state = "ready"
        return reply

    def _save_reply_images(self, reply, imgs):
        """把回复里的图片存到 memory/web_model_images/<批次>/，正文里写成
        ![说明](cx-webimg:<批次>/<文件名>)。调用方（视频笔记）再把它们移进笔记自己的图片目录。
        能下载原图就下原图（带登录 cookie 请求 / 页面里读取），都不行就截图那张图。"""
        import base64
        import uuid
        batch = time.strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6]
        d = IMG_DIR / batch
        saved = {}
        for it in imgs:
            i = it.get("i")
            src = it.get("src") or ""
            data, ext = b"", ".png"
            try:
                if src.startswith("data:"):
                    head, _, b64 = src.partition(",")
                    data = base64.b64decode(b64)
                    ext = ".jpg" if "jpeg" in head or "jpg" in head else (".webp" if "webp" in head else ".png")
                elif src.startswith("http"):
                    r = self._context.request.get(src, timeout=30000)
                    if r.ok:
                        data = r.body()
                        ct = (r.headers.get("content-type") or "").lower()
                        ext = ".jpg" if "jpeg" in ct else (".webp" if "webp" in ct else
                                                          (".gif" if "gif" in ct else ".png"))
                        if not ct.startswith("image/"):
                            data = b""
            except Exception as e:
                self._log("图片 %s 直接下载失败：%s" % (i, str(e).split(chr(10))[0][:60]))
                data = b""
            if not data:
                du = self._safe(lambda: self._page.evaluate(_IMG_DATAURL_JS, i), "") or ""
                if du.startswith("data:image"):
                    head, _, b64 = du.partition(",")
                    try:
                        data = base64.b64decode(b64)
                        ext = ".jpg" if "jpeg" in head else (".webp" if "webp" in head else
                                                           (".gif" if "gif" in head else ".png"))
                    except Exception:
                        data = b""
            if not data:
                try:
                    loc = self._page.locator('[data-cx-img="%s"]' % i).first
                    loc.scroll_into_view_if_needed(timeout=5000)
                    data = loc.screenshot(timeout=15000)
                    ext = ".png"
                    self._log("图片 %s 下载不了，改为截图保存" % i)
                except Exception as e:
                    self._log("图片 %s 截图也失败：%s" % (i, str(e).split(chr(10))[0][:60]))
                    data = b""
            if len(data) < 200:
                continue
            try:
                d.mkdir(parents=True, exist_ok=True)
                fn = "ai-%d%s" % (i, ext)
                (d / fn).write_bytes(data)
                saved[i] = (batch + "/" + fn, it.get("alt") or "示意图")
            except Exception:
                pass
        if saved:
            self._log("✓ 已保存回复里的 %d 张图片" % len(saved))

        def _sub(m):
            k = int(m.group(2))
            if k in saved:
                return "![%s](cx-webimg:%s)" % (m.group(1) or saved[k][1], saved[k][0])
            return ""                                   # 没存下来的图就不留占位
        reply = re.sub(r"!\[([^\]]*)\]\(cx-webimg:(\d+)\)", _sub, reply or "")
        # 不在抓到的正文里的图（例如图片挂在回复外层），补到末尾
        missing = [v for v in saved.values() if ("cx-webimg:" + v[0]) not in reply]
        if missing:
            reply = reply.rstrip() + "\n\n" + "\n\n".join(
                "![%s](cx-webimg:%s)" % (alt, rel) for rel, alt in missing) + "\n"
        return reply

    # ──────────── 发送相关小工具（本次修复新增）────────────
    def _page_text_len(self):
        """整页可见文字长度。发送后它会因为多出『提问气泡 + 回复』而变长——用来判断发出去没。"""
        return self._safe(
            lambda: self._page.evaluate("() => (document.body.innerText || '').length"), 0) or 0

    def _press_send_key(self, inp):
        """聚焦输入框后按 Enter 发送（标准 ChatGPT：Enter=发送，Shift+Enter=换行）。"""
        self._focus_input(inp)
        self._page.keyboard.press("Enter")
        return True

    def _dom_click_send(self):
        """在页面里直接触发发送按钮的 click（不动鼠标、不需要窗口在前台）。找不到/按钮不可用返回 False。"""
        return bool(self._safe(lambda: self._page.evaluate(r"""() => {
            const sels = ['button[data-testid="send-button"]', '#composer-submit-button',
                          'button[aria-label*="发送"]', 'button[aria-label*="Send" i]', 'button[type="submit"]'];
            for (const s of sels) {
                for (const b of document.querySelectorAll(s)) {
                    const r = b.getBoundingClientRect();
                    if (r.width > 0 && r.height > 0 && !b.disabled && b.getAttribute('aria-disabled') !== 'true') {
                        b.click(); return true;
                    }
                }
            }
            return false;
        }"""), False))

    def _click_send_btn(self):
        """
        【首选发送方式】用 Playwright 的『可操作点击』点发送按钮 —— 它会自动把按钮滚动到
        可见、等待其可点、并避开悬浮遮挡层（紫色气泡/右侧竖排工具条），比裸坐标点击稳得多。
        选择器同时覆盖参考实现 ai-runner.js 里验证可用的那几个（button[type=submit] /
        button:has(svg[class*=send]) / 文案『发送』『Send』）和新版可能的语义选择器。
        命中不到再用启发式 _MARK_SEND_JS 标出那颗 ↑ 键，仍用可操作点击点它。
        """
        sel = ('button[data-testid="send-button"], #composer-submit-button, '
               'button[type="submit"], button[aria-label*="发送" i], '
               'button[aria-label*="send" i], button:has-text("发送"), '
               'button:has-text("Send"), button:has(svg[class*="send" i])')
        try:
            loc = self._page.locator(sel).first
            if loc.count() and loc.is_visible() and loc.is_enabled():
                loc.click(timeout=4000)
                self._log("  已点击发送按钮（可操作点击，选择器命中）")
                return True
        except Exception as e:
            self._log("  发送按钮可操作点击异常：%s" % e)

        # 选择器没命中 → 启发式定位那颗 ↑ 键，再可操作点击
        res = self._safe(lambda: self._page.evaluate(_MARK_SEND_JS), None)
        if res and res.get("ok"):
            self._log("  发送键候选: %s ｜ 附近按钮: %s"
                      % (res.get("pick") or "", res.get("desc") or ""))
            try:
                loc2 = self._page.locator('[data-cx-send="1"]').last
                if loc2.count() and loc2.is_visible():
                    loc2.click(timeout=4000)
                    self._log("  已点击发送键（启发式定位 + 可操作点击）")
                    return True
            except Exception as e:
                self._log("  启发式发送键点击异常：%s" % e)
        else:
            self._log("  未命中发送按钮选择器。附近按钮: " + ((res or {}).get("desc") or "(无)"))
        return False

    def _send_btn_state(self):
        return self._safe(lambda: self._page.evaluate(_SEND_STATE_JS), "none") or "none"

    def _composer_has(self, text):
        """输入框里是不是还躺着这段文字（= 没发出去）。"""
        return bool(self._safe(lambda: self._page.evaluate(_COMPOSER_HAS_JS, (text or "")[:120]), False))

    def _nudge_input(self, inp):
        """补按一下空格再删掉：让输入框正式触发一次「有人在打字」，页面才会把发送键点亮。"""
        try:
            self._focus_input(inp)
            self._page.keyboard.press("End")
            self._page.keyboard.insert_text(" ")
            self._page.keyboard.press("Backspace")
            time.sleep(0.5)
        except Exception:
            pass

    def _fill_prompt(self, inp, prompt):
        """v62：填入提示词，并确认页面真的「认」到了（发送键亮起来）。返回框里的文字。
        以前先用「页面直写」——字是进了框，但网页自己的编辑器没收到输入事件，发送键一直是灰的，
        点了也发不出去（你截图里那样卡住）。现在先用真正的键盘输入（不需要窗口在前台），
        填完看发送键：还是灰的就补按一下空格再删掉，仍然灰就换下一种填法。"""
        need = min(int(len(prompt) * 0.8), 8)
        last_pre = ""
        for how in ("insert_text", "页面直写", "fill"):
            try:
                if how == "页面直写":
                    if not self._safe(lambda: inp.evaluate(_DOM_FILL_JS, prompt), ""):
                        continue
                else:
                    self._focus_input(inp)
                    self._page.keyboard.press("Control+A")
                    self._page.keyboard.press("Delete")
                    if how == "insert_text":
                        self._page.keyboard.insert_text(prompt)
                    else:
                        inp.fill(prompt, timeout=5000)
                time.sleep(0.6)
                pre = self._read_input_text(inp)
                last_pre = pre or last_pre
                if len(pre) < need:
                    self._log("填入[%s]后框内只有 %d 字，换方式…" % (how, len(pre)))
                    continue
                st = self._send_btn_state()
                if st == "disabled":
                    self._nudge_input(inp)
                    st = self._send_btn_state()
                if st == "disabled":
                    self._log("填入[%s]后发送键还是灰的（网页没认到这段字），换方式…" % how)
                    continue
                self._log("已填入（方式=%s，框内 %d 字，发送键%s）" % (
                    how, len(pre), "已亮" if st == "enabled" else "没认出来，按页面默认"))
                return pre
            except Exception as e:
                self._log("填入[%s]异常：%s" % (how, e))
        raise RuntimeError("prompt 没填进输入框，或者填了发送键一直是灰的（换卡重试）")

    def _resend_if_stuck(self, prompt_text):
        """v62：提示词还躺在输入框里（没发出去）→ 再点一次发送。返回是否还卡着。"""
        if not self._composer_has(prompt_text):
            return False
        try:
            inp = self._find_input()
        except Exception:
            inp = None
        if inp is not None:
            self._nudge_input(inp)
        for act in (self._dom_click_send, self._click_send_btn,
                    (lambda: self._press_send_key(inp)) if inp is not None else None):
            if act is None:
                continue
            self._safe(act)
            time.sleep(1.5)
            if not self._composer_has(prompt_text):
                return False
        return self._composer_has(prompt_text)

    def _wait_send_committed(self, pre_page_len, inp, pre_text, label, max_wait=3.5):
        """
        判断消息是否【真的发出去了】。不再只看输入框清空（ProseMirror 清空有延迟还会重建节点，
        会误判），而是轮询 1~3.5 秒，命中任一即算成功：
          ① genState=generating（出现『停止■』按钮，AI 已收到正在生成）；
          ② 整页文字明显变长（页面多了提问气泡 / 开始出现回复）；
          ③ 输入框确实清空（保留为辅助信号）。
        """
        deadline = time.time() + max_wait
        pre_len = len(pre_text or "")
        clear_thresh = max(3, int(pre_len * 0.4))
        grow_thresh = max(30, pre_len)        # 至少要多出『提问气泡』那么多字
        while time.time() < deadline:
            time.sleep(0.5)
            _check_cancel()
            probe = self._safe(lambda: self._page.evaluate(_PROBE_JS), None)
            if (probe or {}).get("genState") == "generating":
                self._log("✓ 发送成功（方式：%s）：检测到『停止■』，AI 已开始生成" % label)
                return True
            if pre_text and self._composer_has(pre_text):
                continue          # v62：提示词还在输入框里 = 没发出去（别被别的信号骗了）
            grew = self._page_text_len() - pre_page_len
            if grew > grow_thresh:
                self._log("✓ 发送成功（方式：%s）：页面新增 %d 字（出现提问气泡/回复）"
                          % (label, grew))
                return True
            post = self._read_input_text(inp)
            if pre_len and len(post) < clear_thresh:
                self._log("✓ 发送成功（方式：%s）：输入框已清空（剩 %d 字）" % (label, len(post)))
                return True
        self._log("  方式[%s]发送后无明显变化（停止键/页面增长/清空都没出现），换下一种…" % label)
        return False

    def _read_input_text(self, inp):
        try:
            return inp.evaluate(
                "el => (el.value !== undefined && el.value !== null ? el.value : (el.innerText || '')) || ''") or ""
        except Exception:
            return ""

    def _click_send(self, mechanism="mouse"):
        """
        识别并点击发送按钮（输入框右侧圆形 ↑）。mechanism:
          'mouse'     → 坐标鼠标点击（默认，最不易被拦截）
          'js_events' → 在按钮上派发完整指针事件序列（pointerdown/up+click，兼容挑剔的 React 按钮）
        始终把 composer 附近按钮清单打到日志，便于排错。
        """
        # 已知语义选择器先试（命中即点）
        for sel in ('button[data-testid="send-button"]', '#composer-submit-button',
                    'button[aria-label*="发送" i]', 'button[aria-label*="send" i]'):
            try:
                loc = self._page.locator(sel).last
                if loc.count() and loc.is_visible() and loc.is_enabled():
                    loc.click(timeout=3000)
                    self._log("  点击发送键（选择器 %s）" % sel)
                    return True
            except Exception:
                pass

        res = self._safe(lambda: self._page.evaluate(_MARK_SEND_JS), None)
        if not res or not res.get("ok"):
            self._log("  未识别到发送键。附近按钮: " + ((res or {}).get("desc") or "(无)"))
            return False
        self._log("  发送键候选: %s ｜ 附近按钮: %s"
                  % (res.get("pick") or "", res.get("desc") or ""))

        if mechanism == "js_events":
            ok = self._safe(lambda: self._page.evaluate(_DISPATCH_SEND_JS), False)
            self._log("  已派发指针事件到发送键" if ok else "  指针事件派发失败")
            return bool(ok)

        # mouse：坐标点击 → locator 点击 → JS 原生 click
        cx, cy = res.get("cx"), res.get("cy")
        if cx and cy:
            try:
                self._page.mouse.click(cx, cy)
                self._log("  已坐标点击发送键 (%s,%s)" % (cx, cy))
                return True
            except Exception as e:
                self._log("  坐标点击失败: %s" % e)
        try:
            loc = self._page.locator('[data-cx-send="1"]').last
            if loc.count():
                loc.click(timeout=3000)
                self._log("  已 locator 点击发送键")
                return True
        except Exception as e:
            self._log("  locator 点击失败: %s" % e)
        try:
            self._page.evaluate(
                "() => { const e=document.querySelector('[data-cx-send=\"1\"]'); if(e) e.click(); }")
            self._log("  已 JS 原生点击发送键")
            return True
        except Exception:
            return False

    # ════════════════════ ★命门：答完判定 ════════════════════
    def _looks_echo(self, current, prompt_text):
        head = (prompt_text or "").replace(" ", "").replace("\n", "")[:80]
        return bool(head) and head in (current or "").replace(" ", "").replace("\n", "")[:200]

    def _strip_echo(self, current, prompt_text):
        """v69：新页面上，探针往上爬过了头，抓到的是「提问 + 回复」一整块 → 只留后面的回复。
        先看抓到的文字是不是以整段提问开头（最准）；不是的话，在提问那一段范围里找提问的最后 60 个字。
        剩下的如果其实还是提问的一部分，就不算（返回空串）。"""
        p = re.sub(r"\s+", "", prompt_text or "")
        if len(p) < 40 or not current:
            return ""
        idx = [i for i, ch in enumerate(current) if not ch.isspace()]
        norm = "".join(current[i] for i in idx)
        end = -1
        s0 = norm.find(p[:40])
        if s0 >= 0 and norm[s0:s0 + len(p)] == p:
            end = s0 + len(p)
        else:
            tail = p[-60:]
            k = norm[:len(p) + 800].rfind(tail)
            if k >= 0:
                end = k + len(tail)
        if end <= 0 or end >= len(norm):
            return ""
        rest = current[idx[end - 1] + 1:].strip()
        rest = "\n".join(ln for ln in rest.split("\n") if not re.match(
            r"\s*(思考了|已思考|思考用时|Thought for|ChatGPT\s*(说|said)|你说|You said|显示更多|显示全部|收起|Show more|Show less)", ln)).strip()
        return rest if self._not_prompt(rest, prompt_text) else ""

    def _not_prompt(self, text, prompt_text):
        """v69：读到的「回复」其实是提问的一段 → 不算。"""
        t = re.sub(r"\s+", "", text or "")[:60]
        return bool(t) and t not in re.sub(r"\s+", "", prompt_text or "")

    def _dump_reply_diag(self, prompt_text, chosen, why="一直只抓到提问回显"):
        """v69：一直只看到提问回显时，存一份页面结构（不含正文，只有标签、类名、字数），方便找原因。
        v133：也在「停止键一直亮着、回复还很短」时存；看得更深（回复区在第 30 层以下），并记下 data-* 属性。"""
        try:
            outline = self._safe(lambda: self._page.evaluate(r"""() => {
                const out = []; let n = 0;
                const walk = (el, d) => {
                    if (n > 3000 || d > 60) return;
                    const txt = (el.innerText || '').trim();
                    if (!txt) return;
                    const own = [...el.childNodes].filter(x => x.nodeType === 3).map(x => x.textContent).join('').trim();
                    out.push({d, t: el.tagName.toLowerCase(), c: String(el.className && el.className.baseVal !== undefined ? el.className.baseVal : (el.className || '')).slice(0, 80),
                              r: el.getAttribute('data-message-author-role') || el.getAttribute('data-testid') || el.getAttribute('role') || '',
                              n: txt.length, s: own.slice(0, 16), w: Math.round(el.getBoundingClientRect().width),
                              a: [...el.attributes].filter(x => x.name.startsWith('data-') && x.name !== 'data-cx-img').slice(0, 4)
                                   .map(x => x.name.slice(5) + (x.value && x.value.length <= 24 ? '=' + x.value : '')).join(' ')});
                    n++;
                    for (const c of el.children) walk(c, d + 1);
                };
                walk(document.body, 0);
                return out;
            }"""), [])
            d = MEMORY_DIR / "web_model_diag"
            d.mkdir(parents=True, exist_ok=True)
            fn = d / ("%s-reply.json" % time.strftime("%Y%m%d-%H%M%S"))
            fn.write_text(json.dumps({"why": why, "url": self._safe(lambda: self._page.url, ""),
                                      "prompt_head": (prompt_text or "")[:60], "prompt_tail": (prompt_text or "")[-40:],
                                      "chosen_head": (chosen or "")[:120], "chosen_len": len(chosen or ""),
                                      "outline": outline}, ensure_ascii=False), encoding="utf-8")
            self._log("已存一份页面结构到 %s（推送到 GitHub 后可以帮忙看原因）" % fn.name)
        except Exception as e:
            self._log("存页面结构没成功：%s" % e)

    def _structural_reply(self, prompt_text):
        """v68：按页面结构读本轮回复（1.2 秒内重复调用直接用上次的结果，省得太频繁）。"""
        now = time.time()
        if now - self._struct_at < 1.2:
            return self._struct_last
        self._struct_at = now
        r = self._safe(lambda: self._page.evaluate(_STRUCT_REPLY_JS, prompt_text or ""), None) or {}
        t = (r.get("text") or "").strip() if r.get("found") else ""
        self._struct_last = t if self._not_prompt(t, prompt_text) else ""
        return self._struct_last

    def _wait_for_reply(self, timeout_ms, baseline, prompt_text, opts, prog):
        start = time.time()
        self._struct_at, self._struct_last, self._struct_noted = 0, "", False
        self._strip_noted, echo_dumped = False, False
        expects_json = bool(opts.get("expectsJson"))
        min_expected = opts.get("minExpectedLength") or (300 if expects_json else 0)
        required_markers = [m for m in (opts.get("requiredMarkers") or [])
                            if isinstance(m, str) and m]
        markers_min_hits = opts.get("markersMinHits") or min(2, len(required_markers))
        hold_cap_ms = opts.get("holdCapMs") or 180000
        accept_stable = [m for m in (opts.get("acceptStableMarkers") or [])
                         if isinstance(m, str) and m]
        think_noout_fatal_ms = opts.get("thinkNoOutputMs") or 300000
        # v133：回复还很短、停止键还亮着时最多等多久（思考强度拉满时，开场白之后常要想一两分钟）
        LONG_THINK_MS = opts.get("longThinkMs") or 300000
        long_noted, long_dumped = False, False
        # ★短回复模式：调用方明确这是个简短的确定性回复（如"起标题"），
        #   答完判定以「发送按钮恢复可发送」为准，按钮一稳定恢复就算完，不强求长时间空闲。
        short_reply = bool(opts.get("shortReply"))

        first_hold_at = 0
        td_baseline = -1
        td_last_text = ""
        td_since = 0
        EMPTY_ANSWER_GRACE_MS = 25000
        think_since = 0
        idle_confirm = 0
        IDLE_CONFIRM_REPS = 4

        last_text = ""
        last_change = time.time()
        stable = 0
        SETTLE_INTERVAL = 1.5
        SETTLE_REPS = 4
        POLL = 0.5
        STUCK_WARN_MS = 60000
        STUCK_FATAL_MS = opts.get("stuckFatalMs") or 240000
        warned = False
        last_log = time.time()
        last_full_len = 0
        saw_new = baseline is None
        skip_log = 0
        hold_log = 0
        last_prog = 0
        blk_st = {}
        last_blk = 0
        img_wait_since = 0
        IMG_WAIT_CAP = opts.get("imageWaitMs") or 480000      # 生成图片最多多等 8 分钟
        echo_since = 0            # v62：第一次看到「回显」的时间
        last_resend = 0
        resends = 0

        self._quiet_shots = False
        while (time.time() - start) * 1000 < timeout_ms:
            time.sleep(POLL)
            self._tick()
            _check_cancel()           # v62：批量分析点了「停止」→ 马上放下这条

            # 每 2 秒查一次：对比框 / 出错重试 / 额度用完 / 正在生成图片
            if time.time() - last_blk > 2:
                last_blk = time.time()
                act = self._handle_blockers(prompt_text, blk_st)
                if act:
                    last_change = time.time()
                    warned = False
                    stable = 0
                    idle_confirm = 0
                    first_hold_at = 0
                    if act in ("skip", "prefer"):
                        prog("已自动处理「你更喜欢哪个回复」对比框")
                    elif act == "retry":
                        prog("AI 池出错，已自动点重试…")
                        think_since = 0
                        td_since = 0
                    continue
                gen = self._safe(lambda: self._page.evaluate(_IMG_GEN_JS, prompt_text), None) or {}
                if gen.get("busy"):
                    if not img_wait_since:
                        img_wait_since = time.time()
                        self._log("AI 正在生成图片（%s），等图片画完再收尾…" % gen.get("busy"))
                        prog("AI 正在生成示意图…")
                    if (time.time() - img_wait_since) * 1000 < IMG_WAIT_CAP:
                        last_change = time.time()
                        warned = False
                        stable = 0
                        idle_confirm = 0
                        first_hold_at = 0
                        think_since = 0
                        continue
                elif img_wait_since:
                    self._log("✓ 图片已生成完")
                    img_wait_since = 0

            # 卡死信号：整页 innerText 长度
            full_len = self._safe(
                lambda: self._page.evaluate("() => (document.body.innerText || '').length"), 0) or 0
            if full_len != last_full_len and full_len > 0:
                last_full_len = full_len
                last_change = time.time()
                warned = False
            else:
                idle_ms = (time.time() - last_change) * 1000
                if idle_ms > STUCK_FATAL_MS:
                    self._log("[STUCK] AI 已 %ds 无任何响应" % round(idle_ms / 1000))
                    raise _Stuck("AI 卡死")
                if idle_ms > STUCK_WARN_MS and not warned:
                    self._log("[警告] AI 似乎卡住（%ds 无响应），继续等..." % round(idle_ms / 1000))
                    warned = True

            probe = self._safe(lambda: self._page.evaluate(_PROBE_JS), None)

            # AI 还在思考：跳过本轮，但累计「纯思考无输出」时长
            if probe and probe.get("status") == "thinking":
                last_change = time.time()
                warned = False
                if not last_text:
                    if not think_since:
                        think_since = time.time()
                    if (time.time() - think_since) * 1000 > think_noout_fatal_ms:
                        self._log("[STUCK] 一直思考但无输出，判思考卡死")
                        raise _Stuck("AI 一直思考但无输出")
                if time.time() - skip_log > 5:
                    self._log("AI 正在思考中，等待回复出现...")
                    if time.time() - last_prog > 4:
                        prog("思考中…")
                        last_prog = time.time()
                    skip_log = time.time()
                continue

            if probe:
                if probe.get("genState") == "generating" or probe.get("status") == "thinking":
                    idle_confirm = 0
                elif probe.get("genState") == "idle":
                    idle_confirm += 1

            # 「思考结束但交白卷」检测
            if probe and td_baseline < 0:
                td_baseline = probe.get("thinkingDoneCount") or 0
            if probe and (not last_text) and (probe.get("thinkingDoneCount") or 0) > td_baseline:
                td_text = probe.get("thinkingDoneText") or ""
                if td_text != td_last_text:
                    td_last_text = td_text
                    td_since = time.time()
                elif td_since and (time.time() - td_since) * 1000 > EMPTY_ANSWER_GRACE_MS:
                    self._log("⚠ 思考结束但无输出（偷懒），换卡重试")
                    raise _Stuck("AI 思考结束但没有输出任何回答")
            elif last_text and td_since:
                td_since = 0
                td_last_text = ""

            current = ((probe or {}).get("chosen") or {}).get("text") or ""
            # v68：网站改版后，回复区不再带 markdown / assistant 这些标记，探针只能看到自己的提问气泡，
            #      以前就一直当成「AI 还没回」干等。这时改用「提问气泡后面、输入框前面的内容」当回复。
            if prompt_text and len(prompt_text) > 100 and (not current or self._looks_echo(current, prompt_text)):
                alt = self._structural_reply(prompt_text)
                if not alt and current:
                    alt = self._strip_echo(current, prompt_text)     # v69：抓到「提问 + 回复」连在一起 → 去掉提问
                    if alt and not self._strip_noted:
                        self._strip_noted = True
                        self._log("抓到的是「提问 + 回复」连在一起的一整块 → 去掉前面的提问，只读回复")
                if alt:
                    if not self._struct_noted:
                        self._struct_noted = True
                        self._log("页面结构和以前不一样：改用「提问后面的内容」读 AI 回复")
                    current = alt
            if not current:
                continue

            # 防 prompt 回显
            if prompt_text and current and len(prompt_text) > 100:
                head = prompt_text.replace(" ", "").replace("\n", "")[:80]
                cur_head = current.replace(" ", "").replace("\n", "")[:200]
                if head and head in cur_head:
                    last_change = time.time()
                    warned = False
                    if not echo_since:
                        echo_since = time.time()
                    # v62：「回显」持续 15 秒还在，看看是不是提示词根本还在输入框里（没发出去）
                    if time.time() - echo_since > 15 and time.time() - last_resend > 15:
                        last_resend = time.time()
                        if self._composer_has(prompt_text):
                            resends += 1
                            if resends > 2:
                                raise _Stuck("提示词一直停在输入框里没发出去（换卡重试）")
                            self._log("⚠ 提示词还在输入框里，没发出去 → 再点一次发送（第 %d 次）" % resends)
                            prog("提示词没发出去，再点一次发送…")
                            if not self._resend_if_stuck(prompt_text):
                                self._log("✓ 补发成功")
                                echo_since = 0
                            continue
                    if time.time() - skip_log > 5:
                        self._log("抓到的是 prompt 回显，等真实 AI 回复...")
                        skip_log = time.time()
                    if not echo_dumped and time.time() - echo_since > 45:
                        echo_dumped = True
                        self._dump_reply_diag(prompt_text, current)
                    continue

            # 防模板标记
            if any(mark in current for mark in
                   ("═══ 范例", "严格输出", "【判定口诀】", "═══ 演变史格式")):
                last_change = time.time()
                warned = False
                continue

            # 与基线相同＝本轮还没开始
            if baseline and not saw_new and current == baseline.get("text"):
                if time.time() - skip_log > 5:
                    self._log("等待 AI 开始回复中（底部还是上一轮回复）")
                    skip_log = time.time()
                continue
            if not saw_new:
                saw_new = True
                self._log("✓ AI 开始产生本轮回复（%d 字）" % len(current))
                prog("接收回复中…")
            think_since = 0
            _live_set(reply=_clean_reply_text(current), reply_at=time.time())   # v133：实时画面里不显示网页小字

            if current != last_text:
                stable = 0
                last_text = current
                first_hold_at = 0
                if time.time() - last_log > 3:
                    self._log("内容增长中... %d 字" % len(current))
                    if time.time() - last_prog > 4:
                        prog("接收回复中…（%d 字）" % len(current))
                        last_prog = time.time()
                    last_log = time.time()
            elif len(current) >= 1:
                # 短回复（如"起标题"只有十几个字）也要进入完成判定。
                # 之前这里写 len>50，导致短答案永远进不来、卡死到超时。
                # 真正的防误判由 _finalize_if_done 里的「按钮恢复可发送 + 持续空闲」来把关。
                stable += 1
                # 短回复模式下，文本稳定要求放宽到约 2 秒即可进入判定（再由按钮态最终确认）
                settle_need = (SETTLE_INTERVAL * 1.3) if short_reply else (SETTLE_INTERVAL * SETTLE_REPS)
                if stable * POLL >= settle_need:
                    res = self._finalize_if_done(
                        current, probe, idle_confirm, IDLE_CONFIRM_REPS,
                        expects_json, min_expected, required_markers,
                        markers_min_hits, accept_stable, short_reply,
                        stable_secs=stable * POLL)
                    if res["done"]:
                        # 给出明确的完成报告：检查并说明发送按钮状态，让用户/开发者
                        # 清楚知道「AI 已答完、识别完成」，而不是只看到一句模糊的"内容稳定"。
                        gs = (probe or {}).get("genState", "unknown")
                        if gs == "idle":
                            self._log("✓ AI 已生成完毕：发送按钮已恢复『可发送』，"
                                      "识别完成（共 %d 字），交付结果。" % len(current))
                        else:
                            self._log("✓ AI 已生成完毕：文本已稳定（共 %d 字），"
                                      "识别完成，交付结果。" % len(current))
                        return current
                    # 防误判：继续等（带 holdCap 上限）
                    if not first_hold_at:
                        first_hold_at = time.time()
                    held_ms = (time.time() - first_hold_at) * 1000
                    # ★逃生通道：按钮态识别可能因第三方站点的图标结构而失效（发送键被
                    #   误判成停止键 → genState 永远 generating → 死等）。所以只要回复
                    #   文本已经「持续稳定」足够久（默认 12 秒零增长），就判定 AI 答完，
                    #   不再 100% 依赖那个脆弱的按钮信号。短回复模式阈值更短（8 秒）。
                    escape_ms = 8000 if short_reply else 12000
                    # v133：回复还很短（多半只是开场白「我会按你指定的结构整理…」），停止键却还亮着 / 页面显示还在思考
                    #       → AI 还在干活。以前这里 12 秒就把开场白当答案交了，加工就判「回来的不是笔记」、换卡重来。
                    #       现在只认发送键恢复（这个网站上一直认得准）；真等了 5 分钟还这样，才接受现有内容。
                    busy = ((probe or {}).get("genState") == "generating") or res.get("reason") == "AI 仍在思考"
                    long_wait = (not short_reply) and busy and len(_clean_reply_text(current)) < 250
                    if long_wait:
                        escape_ms = max(escape_ms, LONG_THINK_MS)
                        if not long_noted:
                            long_noted = True
                            self._log("回复还很短（%d 字），停止键还亮着：AI 多半还在思考，接着等发送键恢复（最多 %d 分钟）"
                                      % (len(current), LONG_THINK_MS // 60000))
                            prog("AI 还在思考…")
                    if held_ms > escape_ms:
                        self._log("内容已持续稳定 %d 字 / %.0f 秒，按钮态未翻转，"
                                  "按『文本稳定』判定答完" % (len(current), held_ms / 1000))
                        if long_wait and not long_dumped:
                            long_dumped = True
                            self._dump_reply_diag(prompt_text, current, why="停止键一直亮着，回复还很短")
                        return current
                    if held_ms > hold_cap_ms and not long_wait:
                        self._log("⚠ 防误判等待达上限，接受现有 %d 字返回" % len(current))
                        return current
                    last_change = time.time()
                    warned = False
                    stable = 0
                    if time.time() - hold_log > 10:
                        self._log("内容已稳定 %d 字，但 %s，继续等真答案..."
                                  % (len(current), res["reason"]))
                        hold_log = time.time()

        if len(last_text) > 4:
            self._log("[警告] 等待超时，但已有部分内容（%d 字），返回" % len(last_text))
            return last_text
        raise RuntimeError("等待 AI 回复超时")

    @staticmethod
    def _finalize_if_done(current, probe, idle_confirm, idle_reps,
                          expects_json, min_expected, required_markers,
                          markers_min_hits, accept_stable, short_reply=False,
                          stable_secs=0):
        import re
        has_json_fence = bool(re.search(r"```json[\s\S]*?```", current))
        first_b = current.find("{")
        last_b = current.rfind("}")
        opens = current.count("{")
        closes = current.count("}")
        has_braces = (first_b >= 0 and last_b > first_b and opens >= 2
                      and abs(opens - closes) <= 1)
        has_json = has_json_fence or has_braces

        norm = current.replace("：", ":")
        marker_hits = sum(1 for m in required_markers if m in norm) if required_markers else 0
        markers_ok = (not required_markers) or marker_hits >= markers_min_hits

        # ★短回复特别容易被误判★：联网/思考模型常先抛一句"我会先去查…"的开场白，
        #   按钮也会短暂恢复成"可发送"，导致把开场白当成最终答案（就像漏掉新闻联播正文那次）。
        #   所以默认短回复（< SHORT 字）要求"持续空闲更久"才算真答完，跨过开场白与真答案之间的空档。
        #   但若调用方明确这是「短回复任务」(short_reply=True，如起标题)，则信任按钮态：
        #   按钮恢复可发送、稳定约 3 秒即可判完成，不再死等。
        SHORT = 250
        if short_reply:
            need_idle = max(idle_reps, 6)   # ≈ 持续 3s 空闲（按钮恢复）即算完成
        else:
            need_idle = idle_reps if len(current) >= SHORT else max(idle_reps, 14)

        # 按钮已变回「可发送」且持续稳定 ＝ 最可靠的完成信号
        if idle_confirm >= need_idle and markers_ok:
            return {"done": True, "reason": ""}

        # 短答案即完成标记（显式标记优先）
        for m in accept_stable:
            if m in norm:
                return {"done": True, "reason": ""}

        # ★短回复任务：完成判定【只】认"发送按钮恢复可发送"这一个信号。
        #   上面 idle_confirm>=need_idle 没满足 → 说明按钮还在「停止■」（AI 还在生成），
        #   一律继续等，绝不靠"文本稳定"提前收尾，避免把流式中途的停顿当成答完。
        if short_reply:
            return {"done": False, "reason": "等发送按钮恢复可发送"}

        loose_think = bool(probe.get("hasLooseThinking") or probe.get("hasThinkingIndicator"))
        if expects_json and not has_json:
            return {"done": False, "reason": "缺 JSON 块"}
        if len(current) < min_expected:
            return {"done": False, "reason": "低于最小预期 %d 字" % min_expected}
        if not markers_ok:
            return {"done": False, "reason": "必含标记只命中 %d/%d" % (marker_hits, markers_min_hits)}
        if loose_think and len(current) < 500 and (not has_json or expects_json is False):
            return {"done": False, "reason": "AI 仍在思考"}
        # 兜底保险：回复偏短、又没拿到"持续空闲"的确认，多半是开场白/半截话，别急着收尾
        if len(current) < SHORT and idle_confirm < need_idle:
            return {"done": False, "reason": "回复偏短、答完信号不足"}
        return {"done": True, "reason": ""}

    # ════════════════════ 工具 ════════════════════
    def _safe(self, fn, default=None):
        self._beat()
        try:
            return fn()
        except Exception:
            return default
        finally:
            self._beat()

    def _dump_diag(self, stage, err=None):
        """失败现场：整页截图 + 页面结构摘要（不含任何输入框的值）。"""
        try:
            page = self._page
            if not page or page.is_closed():
                return
            DIAG_DIR.mkdir(exist_ok=True)
            ts = time.strftime("%Y%m%d-%H%M%S")
            self._safe(lambda: page.screenshot(path=str(DIAG_DIR / (ts + ".png")),
                                               full_page=True, timeout=10000))
            info = self._safe(lambda: page.evaluate(r"""() => {
                const vis = el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
                return {
                    url: location.href, title: document.title,
                    inputs: [...document.querySelectorAll('input,textarea')].map(i => ({
                        tag: i.tagName, type: i.type, name: i.name, placeholder: i.placeholder,
                        visible: vis(i), checked: i.type === 'checkbox' ? i.checked : undefined })),
                    buttons: [...document.querySelectorAll('button,[role="button"]')]
                        .filter(vis).map(b => (b.innerText || '').trim()).filter(Boolean).slice(0, 40),
                    text: (document.body ? document.body.innerText : '').slice(0, 5000),
                };
            }"""), {}) or {}
            info.update({"stage": stage, "error": str(err) if err else "",
                         "sitePath": self._site_path, "carlistUrl": self._carlist_url,
                         "time": ts})
            (DIAG_DIR / (ts + ".json")).write_text(
                json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
            files = sorted(DIAG_DIR.glob("*.*"))
            for f in files[:-DIAG_KEEP * 2]:
                self._safe(lambda f=f: f.unlink())
            self._log("诊断已保存: %s (.png/.json)" % (DIAG_DIR / ts))
        except Exception:
            pass

    # ════════════════════ v55：实时画面 + 显示/隐藏浏览器（都在 worker 线程里做） ════════════════════
    def _tick(self, idle=False):
        """worker 线程里「顺手」做的事：处理显示/隐藏浏览器的命令；有人在看实时画面时截个图。
        只在 worker 线程、两次网页操作之间调用，不会和别的网页操作打架。"""
        if self._in_tick or threading.current_thread() is not self._thread:
            return
        self._in_tick = True
        try:
            while True:
                try:
                    cmd = _UI_CMDS.get_nowait()
                except queue.Empty:
                    break
                self._apply_ui_cmd(cmd)
            # v62：隐藏状态下每 20 秒看一眼：任务栏按钮被 Chrome 自己加回来了就再拿掉
            if _LIVE.get("visible") is False and time.time() - getattr(self, "_taskbar_check", 0) > 20:
                self._taskbar_check = time.time()
                _win_taskbar_set(False, self._browser_pids)
            if _LIVE.get("visible") is False and not self._headless and time.time() - getattr(self, "_min_check", 0) > 10:
                self._min_check = time.time()
                self._unminimize_if_needed()
            now = time.time()
            if self._quiet_shots or _LIVE["watch_until"] < now:
                return
            if now < self._shot_backoff or now - self._last_shot < (5.0 if idle else 2.0):
                return
            pg = self._page
            if pg is None or self._browser is None:
                return
            try:
                if pg.is_closed():
                    return
            except Exception:
                return
            self._last_shot = now
            try:
                data = pg.screenshot(type="jpeg", quality=60, timeout=3000,
                                     caret="initial", scale="css")
                _live_set(shot=data, shot_ts=time.time(), shot_err="")
            except Exception as e:
                _live_set(shot_err=str(e).split("\n")[0][:160])
                self._shot_backoff = time.time() + 15
        except Exception:
            pass
        finally:
            self._in_tick = False

    def _apply_ui_cmd(self, cmd):
        res = cmd.get("res", {})
        try:
            ok, msg = self._set_window_visible(cmd.get("action") == "show")
        except Exception as e:
            ok, msg = False, "操作浏览器窗口出错：%s" % str(e).split("\n")[0][:120]
        res.update(ok=ok, msg=msg)
        try:
            cmd["done"].set()
        except Exception:
            pass

    def _window_id(self):
        pg = self._page
        if pg is None or self._context is None:
            raise RuntimeError("AI 池浏览器还没打开")
        if pg.is_closed():
            raise RuntimeError("AI 池浏览器的页面已经关了（可能被手动关掉了），下一条任务会自动重新打开")
        if self._cdp is None or self._cdp_page is not pg:
            self._cdp = self._context.new_cdp_session(pg)
            self._cdp_page = pg
        try:
            return self._cdp, self._cdp.send("Browser.getWindowForTarget")["windowId"]
        except Exception:
            self._cdp = self._context.new_cdp_session(pg)        # v69：会话失效了（换过卡 / 页面跳转过）→ 重连一次
            self._cdp_page = pg
            return self._cdp, self._cdp.send("Browser.getWindowForTarget")["windowId"]

    def _visible_bounds(self):
        """显示时放到屏幕中间（隐藏前记下过位置就用原来的位置）。"""
        if self._win_restore:
            return dict(self._win_restore)
        try:
            al, at, aw, ah = self._page.evaluate(
                "() => [screen.availLeft || 0, screen.availTop || 0, screen.availWidth, screen.availHeight]")
            w = int(max(900, min(1340, aw - 40)))
            h = int(max(640, min(1000, ah - 40)))
            return {"left": int(al + max(0, (aw - w) // 2)), "top": int(at + max(0, (ah - h) // 2)),
                    "width": w, "height": h}
        except Exception:
            return {"left": 60, "top": 40, "width": 1320, "height": 980}

    def _unminimize_if_needed(self):
        """v71：AI 池浏览器藏在屏幕外时被最小化了（比如按了 Win+D）：左下角会多一个小条，页面也会暂停、
        回复出不来 → 还原成正常大小，再挪回屏幕外。"""
        try:
            if self._page is None or self._page.is_closed():
                return
            cdp, wid = self._window_id()
            b = cdp.send("Browser.getWindowBounds", {"windowId": wid})["bounds"]
            if b.get("windowState") != "minimized":
                return
            cdp.send("Browser.setWindowBounds", {"windowId": wid, "bounds": {"windowState": "normal"}})
            cdp.send("Browser.setWindowBounds", {"windowId": wid, "bounds": {"left": OFFSCREEN_X, "top": 0}})
            self._log("AI 池浏览器被最小化了（会变成屏幕左下角的小条，页面也会暂停）→ 已还原并挪回屏幕外")
        except Exception:
            pass

    def _set_window_visible(self, visible):
        """显示＝挪回屏幕并放到最前面；隐藏＝挪到屏幕外（不最小化，页面照常工作）。"""
        if self._headless:
            return False, "现在是后台模式（设置里勾了不显示浏览器），没有窗口可显示"
        cdp, wid = self._window_id()

        def bounds():
            return cdp.send("Browser.getWindowBounds", {"windowId": wid})["bounds"]

        def set_b(b):
            cdp.send("Browser.setWindowBounds", {"windowId": wid, "bounds": b})

        cur = bounds()
        if cur.get("windowState", "normal") != "normal":
            set_b({"windowState": "normal"})
            cur = bounds()
        if visible:
            _win_taskbar_set(True, self._browser_pids)        # v62：先放回任务栏（这时窗口还在屏幕外，好认）
            set_b(self._visible_bounds())
            # 先最小化再还原：Windows 会把它放到最上面
            set_b({"windowState": "minimized"})
            time.sleep(0.15)
            set_b({"windowState": "normal"})
            try:
                self._page.bring_to_front()
            except Exception:
                pass
            _live_set(visible=True)
            return True, "已显示 AI 池浏览器"
        if cur.get("left", 0) > OFFSCREEN_X // 2:
            self._win_restore = {k: cur[k] for k in ("left", "top", "width", "height") if k in cur}
        set_b({"left": OFFSCREEN_X, "top": 0})
        after = bounds()
        if after.get("left", 0) > OFFSCREEN_X // 4:
            _live_set(visible=True)
            return False, "系统不允许把窗口挪到屏幕外"
        _live_set(visible=False)
        time.sleep(0.2)
        n_tb = _win_taskbar_set(False, self._browser_pids)    # v62：任务栏和 Alt+Tab 里也不显示
        self._taskbar_check = time.time()
        return True, "已隐藏 AI 池浏览器（挪到屏幕外，任务栏里也不显示，照常在后台工作）" if n_tb else \
            "已隐藏 AI 池浏览器（挪到屏幕外，照常在后台工作）"

    def get_state(self):
        return {"state": self._state, "hasBrowser": bool(self._browser),
                "hasPage": bool(self._page), "available": is_available()}

    def test_login(self, on_progress=None):
        """「测试网页模型」：就位 + 发一句测试，验证选择器与答完判定，并把 AI 回复带回前端展示。"""
        def prog(m):
            _live_set(stage=str(m), stage_at=time.time())
            if on_progress:
                self._safe(lambda: on_progress(m))
        self._ensure_started()
        # 用一句简短的问题（比回复短），让 AI 给出一两句话的回答——这样回复块足够长、
        # 能被答完判定正常抓到，前端就能显示 AI 的真实回复内容。
        test_prompt = "你好，请用一两句话简单介绍一下你能帮我做什么。"
        reply = ""
        try:
            reply = self._query_once(test_prompt, {"timeout": 120000}, 1, prog)
        except Exception as e:
            # 即使「答完判定」超时/异常，只要页面上 AI 已经显示了回复，也尽量抓回来给用户看
            self._log("答完判定异常（%s），尝试直接抓取页面上的回复…" % e)
            reply = self._grab_latest_reply(exclude_text=test_prompt)
            if not (reply or "").strip():
                raise
        if not (reply or "").strip():
            reply = self._grab_latest_reply(exclude_text=test_prompt)
        return {"ok": True, "reply": (reply or "").strip()[:500]}

    def _grab_latest_reply(self, exclude_text=""):
        """
        宽松地抓「页面上最新那条 AI 回复」的文字（最底部、足够宽的文本块＝最新回复气泡），
        容忍很短的回复（如『测试成功。』）。用于测试展示 / 答完判定抓不到时的兜底。
        exclude_text：要排除的文字（通常是刚发出去的提问，避免把自己的提问当成回复）。
        """
        js = r"""(exclude) => {
            const sels = ['[data-message-author-role="assistant"]','[class*="markdown"]',
                '[class*="prose"]','[class*="assistant"]','[class*="answer"]',
                '[class*="response"]','[class*="reply-content"]','[class*="message-content"]',
                '[class*="msg-content"]'];
            const norm = s => (s||'').replace(/\s+/g,'');
            const ex = norm(exclude);
            const items = [];
            const seen = new Set();
            for (const s of sels){
                let els; try{els=document.querySelectorAll(s)}catch(e){continue}
                for(const el of els){
                    const r=el.getBoundingClientRect();
                    const t=(el.innerText||'').trim();
                    if(r.width>180 && t.length>0){
                        const n=norm(t);
                        if(!n || seen.has(n)) continue;
                        if(ex && n===ex) continue;          // 跳过＝刚发的提问
                        seen.add(n);
                        items.push({t, bottom:r.bottom, len:t.length});
                    }
                }
            }
            if(!items.length) return '';
            // 最底部的块＝最新回复；同样靠底时取更长的
            items.sort((a,b)=> (b.bottom-a.bottom) || (b.len-a.len));
            return items[0].t;
        }"""
        return self._safe(lambda: self._page.evaluate(js, exclude_text), "") or ""


# 把"最新一条 AI 回复"抓成 Markdown：保留 <a href> 为可点击链接 [文字](网址)，
# 去掉 ChatGPT 的引用角标/来源芯片（"+1""+2"、citation/footnote 之类）这些杂质。

# 本次提问之后的回复区域（找不到提问气泡就用最后一条助手消息）
_REPLY_SCOPE_JS = r"""
    // v68：按页面结构找「本轮回复」——不靠 class 名字（网站改版后回复区不再带 markdown / assistant 这些标记）。
    // ① 用提问里的 6 段「指纹」找到提问气泡（长提问在页面上会被折叠，所以不只看开头）；
    // ② 回复 = 提问气泡后面、输入框前面的内容。
    const __cxStruct = (prompt) => {
        const N = s => (s || '').replace(/[\s\u00a0]+/g, '');
        const P = N(prompt);
        if (P.length < 30 || !document.body) return null;
        const keys = [];
        for (const f of [0, 0.2, 0.4, 0.6, 0.8]) {
            const i = Math.min(Math.floor(P.length * f), Math.max(0, P.length - 24));
            keys.push(P.slice(i, i + 24));
        }
        keys.push(P.slice(-24));
        const hits = t => keys.reduce((n, k) => n + (k.length >= 12 && t.includes(k) ? 1 : 0), 0);
        const comp = document.querySelector('textarea, [contenteditable="true"], [role="textbox"]');
        const SKIP = {SCRIPT: 1, STYLE: 1, NOSCRIPT: 1, TEXTAREA: 1, SVG: 1, TEMPLATE: 1};
        const UI = /^(显示更多|显示全部|收起|展开|Show more|Show less|编辑|复制|Edit|Copy|你说[：:]?|You said:?)$/i;
        const small = el => { const t = N(el.textContent); return !t || t.length <= 8 || UI.test((el.innerText || '').trim()); };
        const inPrompt = el => { const t = N(el.textContent); return t.length >= 6 && P.includes(t); };   // v69：提问的另一段
        const matched = new Set(), order = [];
        for (const el of document.body.getElementsByTagName('*')) {
            if (SKIP[(el.tagName || '').toUpperCase()]) continue;
            if (comp && (el === comp || comp.contains(el) || el.contains(comp))) continue;
            const raw = el.textContent || '';
            if (raw.length < 24 || raw.length > P.length * 3 + 20000) continue;
            if (!hits(N(raw))) continue;
            matched.add(el); order.push(el);
        }
        // 从最里层含提问的元素往上爬：多出来的只是「显示更多」「编辑」这种小标签，就还算提问气泡
        let user = null, best = 0;
        for (const leaf of order) {
            let isLeaf = true;
            for (const c of leaf.children) if (matched.has(c)) { isLeaf = false; break; }
            if (!isLeaf) continue;
            let bb = leaf;
            while (bb.parentElement && bb.parentElement !== document.body) {
                const par = bb.parentElement;
                if (comp && par.contains(comp)) break;
                let fine = true;
                for (const c of par.children) if (c !== bb && !small(c) && !inPrompt(c)) { fine = false; break; }
                if (!fine) break;
                bb = par;
            }
            const h = hits(N(bb.textContent));
            if (h > best) { user = bb; best = h; }                               // 一样多时取前面的
        }
        if (!user) return null;
        const parts = [], nodes = [];
        let node = user;
        while (node && node !== document.body && !parts.length) {
            for (let sib = node.nextElementSibling; sib; sib = sib.nextElementSibling) {
                if (comp && (sib === comp || sib.contains(comp))) { node = null; break; }
                if (SKIP[(sib.tagName || '').toUpperCase()]) continue;
                const t = (sib.innerText || '').trim();
                if (!t || UI.test(t)) continue;
                if (sib.getBoundingClientRect().width < 120) continue;
                if (hits(N(t)) >= 2 || P.includes(N(t))) continue;              // 还是提问本身（藏着的第二份 / 提问的一段）
                parts.push(t); nodes.push(sib);
            }
            if (node) node = node.parentElement;
        }
        const text = parts.join('\n\n').split('\n')
            .filter(l => !/^\s*(思考了|已思考|思考用时|Thought for|ChatGPT\s*(说|said)|你说|You said)/i.test(l))
            .join('\n').trim();
        return text ? {text, nodes} : null;
    };

    const __norm = s => (s || '').replace(/[\s\u00a0]+/g, '');
    const __scope = (head) => {
        const key = __norm(head).slice(0, 30);
        const users = [...document.querySelectorAll('[data-message-author-role="user"]')];
        let anchor = null;
        for (let i = users.length - 1; i >= 0 && key; i--)
            if (__norm(users[i].innerText).includes(key)) { anchor = users[i]; break; }
        let outs = [...document.querySelectorAll('[data-message-author-role="assistant"]')];
        if (anchor) outs = outs.filter(a => anchor.compareDocumentPosition(a) & Node.DOCUMENT_POSITION_FOLLOWING);
        else outs = outs.slice(-1);
        if (!outs.length) { const sr = __cxStruct(head); if (sr) return sr.nodes; }   // v68：页面改版，按结构找
        // 助手消息外面常包一层「整轮」容器，图片可能挂在那里
        return outs.map(a => a.closest('article, [data-testid^="conversation-turn"]') || a);
    };
"""

# v68：按页面结构读本轮回复的文字（给「等回复」用）
_STRUCT_REPLY_JS = r"""(prompt) => {""" + _REPLY_SCOPE_JS + r"""
    const r = __cxStruct(prompt);
    return r ? {found: true, text: r.text} : {found: false};
}"""

# AI 是否正在生成图片（生成中的提示文字 / 还没加载完或还在模糊渐显的大图）
_IMG_GEN_JS = r"""(head) => {""" + _REPLY_SCOPE_JS + r"""
    const GEN = /正在(创建|生成|绘制|制作)(图片|图像|插图|示意图)|(图片|图像)(正在)?生成中|Creating image|Generating image|Making (your|an) image|Image (is )?(being )?(created|generated)/i;
    let busy = '', imgs = 0;
    for (const root of __scope(head)) {
        for (const el of root.querySelectorAll('span, div, p')) {
            if (el.children.length > 4) continue;
            const t = (el.innerText || '').trim();
            if (t && t.length < 60 && GEN.test(t)) { busy = t.slice(0, 40); break; }
        }
        for (const im of root.querySelectorAll('img')) {
            const r = im.getBoundingClientRect();
            if (r.width < 120 || r.height < 80) continue;
            imgs++;
            const cs = getComputedStyle(im);
            const blur = /blur\((?!0)/.test(cs.filter || '') || parseFloat(cs.opacity || '1') < 0.9;
            if (!im.complete || !im.naturalWidth || blur) busy = busy || '图片还在加载';
        }
        if (busy) break;
    }
    return {busy, imgs};
}"""

# 给回复里的大图编号（data-cx-img），返回它们的信息；_GRAB_MARKDOWN_JS 会把它们写成 cx-webimg:编号
_MARK_IMAGES_JS = r"""(head) => {""" + _REPLY_SCOPE_JS + r"""
    for (const e of document.querySelectorAll('[data-cx-img]')) e.removeAttribute('data-cx-img');
    const out = [], seen = new Set();
    for (const root of __scope(head)) {
        for (const im of root.querySelectorAll('img')) {
            const r = im.getBoundingClientRect();
            const w = im.naturalWidth || r.width, h = im.naturalHeight || r.height;
            if (r.width < 80 || r.height < 60 || w < 120 || h < 80) continue;   // 头像、图标不要
            const src = im.currentSrc || im.getAttribute('src') || '';
            if (!src || seen.has(src)) continue;
            seen.add(src);
            const i = out.length + 1;
            im.setAttribute('data-cx-img', String(i));
            out.push({i, src, alt: (im.getAttribute('alt') || '').trim().slice(0, 60), w, h});
        }
    }
    return out;
}"""

# 在页面里把图片读成 dataURL（blob:/同源图片走这里；跨域失败返回空）
_IMG_DATAURL_JS = r"""async (i) => {
    const im = document.querySelector('[data-cx-img="' + i + '"]');
    if (!im) return '';
    const src = im.currentSrc || im.src;
    try {
        const r = await fetch(src);
        const b = await r.blob();
        if (!b.size) return '';
        return await new Promise(res => { const fr = new FileReader(); fr.onload = () => res(fr.result); fr.onerror = () => res(''); fr.readAsDataURL(b); });
    } catch (e) {}
    try {
        const c = document.createElement('canvas');
        c.width = im.naturalWidth; c.height = im.naturalHeight;
        c.getContext('2d').drawImage(im, 0, 0);
        return c.toDataURL('image/png');
    } catch (e) { return ''; }
}"""

# 页面上会挡住流程的东西：①「你更喜欢哪个回复？」对比框 ② 「出错了 / 重试」 ③ 额度用完。
# 只看「不在 AI 回复正文里、也不在用户提问气泡里」的短文字，免得把回复内容误当成提示。
# 要点击的按钮打上 data-cx-click="1"，由 Python 用真实点击去点。
_BLOCKER_JS = r"""() => {
    const vis = el => {
        if (!el) return false;
        const r = el.getBoundingClientRect();
        if (r.width < 2 || r.height < 2) return false;
        const s = getComputedStyle(el);
        return s.visibility !== 'hidden' && s.display !== 'none' && parseFloat(s.opacity || '1') > 0.05;
    };
    const txt = el => (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim();
    const excluded = el => !!el.closest(
        '.markdown, [class*="prose"], [data-message-author-role="user"], [contenteditable="true"], textarea, input');
    for (const e of document.querySelectorAll('[data-cx-click]')) e.removeAttribute('data-cx-click');
    const btns = [...document.querySelectorAll('button, [role="button"], a[role="button"]')].filter(vis);
    const btnText = b => (txt(b) || b.getAttribute('aria-label') || '').trim();
    const shortHit = (re, maxLen) => {
        let best = null;
        for (const el of document.querySelectorAll('h1,h2,h3,h4,h5,p,span,div,legend,strong,section,[role="alert"]')) {
            if (el.children.length > 8) continue;
            const t = txt(el);
            if (!t || t.length > maxLen || !re.test(t)) continue;
            if (!vis(el) || excluded(el)) continue;
            // 包着提问气泡 / 回复正文的大容器不算，只认提示本身那一小块
            if (el.querySelector('[data-message-author-role], .markdown, [class*="prose"]')) continue;
            if (!best || t.length < best.t.length) best = {el, t};
        }
        return best;
    };
    const out = {compare: false, error: '', quota: '', click: '', lens: []};

    // ① 对比框
    const CMP = /你更喜欢哪(个|一个|条)|更喜欢哪个(回复|回答|选项)|你觉得哪个(回复|回答)更好|Which (response|one|answer) do you prefer|Which response is (better|more helpful)/i;
    const cmp = shortHit(CMP, 160);
    if (cmp) {
        out.compare = true; out.text = cmp.t.slice(0, 80);
        const skip = btns.find(b => /^(跳过|略过|Skip)$/i.test(btnText(b)));
        if (skip) { skip.setAttribute('data-cx-click', '1'); out.click = 'skip'; return out; }
        const prefer = btns.filter(b => /更喜欢这|偏好这|选这个|I prefer this|Prefer this|This one is better|选择此回复/i.test(btnText(b)));
        if (prefer.length) {
            let best = null, bestLen = -1;
            for (const b of prefer) {
                // 往上找到「这一边回复」的容器：文字够多、但不包含另一个「更喜欢这个」按钮
                let box = b, cur = b;
                for (let i = 0; i < 10; i++) {
                    const p = cur.parentElement;
                    if (!p || p === document.body) break;
                    if (prefer.some(o => o !== b && p.contains(o))) break;
                    box = p; cur = p;
                }
                const L = Math.max(0, txt(box).length - btnText(b).length);
                out.lens.push(L);
                if (L > bestLen) { bestLen = L; best = b; }
            }
            if (best) { best.setAttribute('data-cx-click', '1'); out.click = 'prefer'; }
        }
        return out;
    }

    // ② 额度用完（这张卡不能用了 → 直接换卡）
    const QUOTA = /(usage|rate|message)\s*(cap|limit)|You['’]ve (reached|hit) (the|your)|limit reached|Too many requests|已达到.{0,12}(上限|限制)|额度(已)?(用完|用尽|耗尽|不足)|次数(已)?用(完|尽)|超出.{0,8}(限制|额度|上限)|请求过于频繁|今日.{0,8}(已用完|上限)|配额(已)?(用完|用尽)/i;
    const q = shortHit(QUOTA, 220);
    if (q) { out.quota = q.t.slice(0, 120); return out; }

    // ③ 出错了 → 点「重试 / 重新生成」
    const ERR = /Something went wrong|An error occurred|Error in message stream|Network error|network connection|出错了|发生(了)?错误|生成.{0,6}(时)?出错|网络(错误|异常|连接)|连接(已)?中断|请求失败/i;
    const er = shortHit(ERR, 220);
    if (er) {
        out.error = er.t.slice(0, 120);
        const RETRY = /^(重试|重新生成|再试一次|重新尝试|Retry|Regenerate|Try again)$/i;
        let retry = null;
        let anc = er.el;
        for (let i = 0; i < 5 && anc && !retry; i++) {
            retry = [...anc.querySelectorAll('button, [role="button"]')].find(b => vis(b) && RETRY.test(btnText(b)));
            anc = anc.parentElement;
        }
        if (!retry) retry = btns.find(b => RETRY.test(btnText(b)) && !excluded(b));
        if (retry) { retry.setAttribute('data-cx-click', '1'); out.click = 'retry'; }
    }
    return out;
}"""

_GRAB_MARKDOWN_JS = r"""(anchorText) => {
    const __cxStruct = (prompt) => {
        const N = s => (s || '').replace(/[\s\u00a0]+/g, '');
        const P = N(prompt);
        if (P.length < 30 || !document.body) return null;
        const keys = [];
        for (const f of [0, 0.2, 0.4, 0.6, 0.8]) {
            const i = Math.min(Math.floor(P.length * f), Math.max(0, P.length - 24));
            keys.push(P.slice(i, i + 24));
        }
        keys.push(P.slice(-24));
        const hits = t => keys.reduce((n, k) => n + (k.length >= 12 && t.includes(k) ? 1 : 0), 0);
        const comp = document.querySelector('textarea, [contenteditable="true"], [role="textbox"]');
        const SKIP = {SCRIPT: 1, STYLE: 1, NOSCRIPT: 1, TEXTAREA: 1, SVG: 1, TEMPLATE: 1};
        const UI = /^(显示更多|显示全部|收起|展开|Show more|Show less|编辑|复制|Edit|Copy|你说[：:]?|You said:?)$/i;
        const small = el => { const t = N(el.textContent); return !t || t.length <= 8 || UI.test((el.innerText || '').trim()); };
        const inPrompt = el => { const t = N(el.textContent); return t.length >= 6 && P.includes(t); };   // v69：提问的另一段
        const matched = new Set(), order = [];
        for (const el of document.body.getElementsByTagName('*')) {
            if (SKIP[(el.tagName || '').toUpperCase()]) continue;
            if (comp && (el === comp || comp.contains(el) || el.contains(comp))) continue;
            const raw = el.textContent || '';
            if (raw.length < 24 || raw.length > P.length * 3 + 20000) continue;
            if (!hits(N(raw))) continue;
            matched.add(el); order.push(el);
        }
        // 从最里层含提问的元素往上爬：多出来的只是「显示更多」「编辑」这种小标签，就还算提问气泡
        let user = null, best = 0;
        for (const leaf of order) {
            let isLeaf = true;
            for (const c of leaf.children) if (matched.has(c)) { isLeaf = false; break; }
            if (!isLeaf) continue;
            let bb = leaf;
            while (bb.parentElement && bb.parentElement !== document.body) {
                const par = bb.parentElement;
                if (comp && par.contains(comp)) break;
                let fine = true;
                for (const c of par.children) if (c !== bb && !small(c) && !inPrompt(c)) { fine = false; break; }
                if (!fine) break;
                bb = par;
            }
            const h = hits(N(bb.textContent));
            if (h > best) { user = bb; best = h; }                               // 一样多时取前面的
        }
        if (!user) return null;
        const parts = [], nodes = [];
        let node = user;
        while (node && node !== document.body && !parts.length) {
            for (let sib = node.nextElementSibling; sib; sib = sib.nextElementSibling) {
                if (comp && (sib === comp || sib.contains(comp))) { node = null; break; }
                if (SKIP[(sib.tagName || '').toUpperCase()]) continue;
                const t = (sib.innerText || '').trim();
                if (!t || UI.test(t)) continue;
                if (sib.getBoundingClientRect().width < 120) continue;
                if (hits(N(t)) >= 2 || P.includes(N(t))) continue;              // 还是提问本身（藏着的第二份 / 提问的一段）
                parts.push(t); nodes.push(sib);
            }
            if (node) node = node.parentElement;
        }
        const text = parts.join('\n\n').split('\n')
            .filter(l => !/^\s*(思考了|已思考|思考用时|Thought for|ChatGPT\s*(说|said)|你说|You said)/i.test(l))
            .join('\n').trim();
        return text ? {text, nodes} : null;
    };

    // 只看「本次提问气泡」之后的内容：找到最后一个包含提问开头的用户气泡，作为锚点
    let __cxAnchor = null;
    try {
        const __n = s => (s || '').replace(/[\s\u00a0]+/g, '');
        const __k = __n(anchorText || '').slice(0, 30);
        if (__k) {
            const __us = [...document.querySelectorAll('[data-message-author-role="user"]')];
            for (let i = __us.length - 1; i >= 0; i--) {
                if (__n(__us[i].innerText).includes(__k)) { __cxAnchor = __us[i]; break; }
            }
        }
    } catch (e) { __cxAnchor = null; }
    // 同一条回复常被网站拆成多个兄弟块（如正文段落 +（另起的）序号列表）。
    // 从最底部命中块向上爬到「整条回复」的容器，把被拆开的块合起来，但不跨越到上一条消息。
    // v68：页面改版（没有 data-message-author-role）→ 按结构找本轮回复
    let __cxNodes = null;
    if (!__cxAnchor) { try { const sr = __cxStruct(anchorText); if (sr && sr.nodes.length) __cxNodes = sr.nodes; } catch (e) {} }
    const __cxClimb = (el) => {
        if(!el) return el;
        let container = el, cur = el;
        for(let i=0;i<8;i++){
            const p = cur.parentElement;
            if(!p || p===document.body || p===document.documentElement) break;
            const r = p.getBoundingClientRect();
            if(!r || r.width < 200) break;
            let roleCount = 0;
            try { roleCount = p.querySelectorAll('[data-message-author-role]').length; } catch(e){}
            if(roleCount > 1) break;                       // 跨越了多条消息 → 爬过头，停
            const cLen = (container.innerText||'').length;
            const pLen = (p.innerText||'').length;
            if(pLen <= cLen){ cur = p; continue; }         // 纯包裹层，继续往上看
            if(pLen > cLen*2.6) break;                     // 文本暴涨＝并入了别的轮次，停
            container = p; cur = p;
        }
        return container;
    };
    const clsOf = (el) => {
        try { return (el.className && el.className.baseVal!==undefined) ? el.className.baseVal : (el.className||''); }
        catch(e){ return ''; }
    };
    const isCite = (el) => {
        const c = (clsOf(el)+'').toLowerCase();
        if(/citation|footnote|sources?-|cite|reference|annotation/.test(c)) return true;
        const t=(el.innerText||el.textContent||'').replace(/[\s\u00a0]+/g,'');
        if(/^[+＋﹢][\d０-９]+$/.test(t)) return true;   // "+1" "+2"（含全角＋/全角数字/带空格）
        return false;
    };
    // 单元格内联文本（用于表格）：把竖线换成空格，避免撑破 Markdown 表格
    const cellText = (el) => {
        let t=(el.innerText||el.textContent||'').replace(/\s+/g,' ').trim();
        return t.replace(/\|/g,' ').trim();
    };
    // <table> -> Markdown 表格（首行作表头）。ChatGPT 的表格（含「写入/Canvas」里的）都是真实 <table>。
    const tableToMd = (table) => {
        const trs = [...table.querySelectorAll('tr')].filter(tr => tr.querySelector('th,td'));
        if(!trs.length) return '';
        let rows = trs.map(tr => [...tr.children]
            .filter(c => /^(td|th)$/i.test(c.tagName))
            .map(cellText)).filter(r => r.length);
        if(!rows.length) return '';
        const cols = Math.max(...rows.map(r => r.length));
        rows = rows.map(r => { while(r.length<cols) r.push(''); return r; });
        const head = rows[0];
        let md = '\n| ' + head.join(' | ') + ' |\n| ' + head.map(()=>'---').join(' | ') + ' |\n';
        for(const r of rows.slice(1)) md += '| ' + r.join(' | ') + ' |\n';
        return md + '\n';
    };
    // v133：按钮上的字（复制、重置清单、思考了 58s…）不是正文
    const UI_BTN = /^(?:复制|复制代码|复制清单|重置清单|编辑|重试|分享|显示更多|显示全部|收起|展开|下载|Copy|Copy code|Edit|Retry|Share|Show more|Show less|Expand|Collapse|Download|(?:已)?思考了?\s*\d.*|已思考.*|思考用时.*|Thought for.*)$/i;
    const walk = (node) => {
        let out='';
        for(const child of node.childNodes){
            if(child.nodeType===3){ out += child.textContent; continue; }
            if(child.nodeType!==1) continue;
            const el=child, tag=el.tagName.toLowerCase();
            if(tag==='script'||tag==='style'||tag==='svg'||tag==='input'||tag==='select'||tag==='textarea') continue;
            if(/(^|\s)sr-only(\s|$)/.test(clsOf(el)+'')) continue;             // v133：读屏用的隐藏字（「ChatGPT 说：」）
            if(tag==='button' || el.getAttribute('role')==='button'){
                const ims=[...el.querySelectorAll('img[data-cx-img]')];           // 生成的图片有时包在按钮里：图照常要
                if(ims.length){
                    for(const im of ims) out += '\n!['+((im.getAttribute('alt')||'示意图').trim().replace(/[\[\]]/g,'')||'示意图')+'](cx-webimg:'+im.getAttribute('data-cx-img')+')\n';
                    continue;
                }
                const bt=(el.innerText||el.textContent||'').replace(/\s+/g,' ').trim();
                if(!bt || UI_BTN.test(bt)) continue;                               // 正文里可点的人名、地名照常当正文
            }
            if(isCite(el)) continue;
            if(tag==='table'){ out += tableToMd(el); continue; }                   // ★表格整体转 Markdown
            if(/^(thead|tbody|tfoot|tr|td|th|colgroup|col)$/.test(tag)) continue;  // 已由 table 处理，跳过防重复
            if(tag==='img'){                                                       // ★图片
                const src=el.getAttribute('src')||el.currentSrc||'';
                const alt=(el.getAttribute('alt')||'图片').trim().replace(/[\[\]]/g,'');
                const mk=el.getAttribute('data-cx-img');
                if(mk) out += '\n!['+(alt||'示意图')+'](cx-webimg:'+mk+')\n';      // 由程序下载到本地
                else if(src && !/^(data|blob):/.test(src)) out += '\n!['+alt+']('+src+')\n';
                continue;
            }
            if(tag==='a'){
                const href=el.getAttribute('href')||'';
                let txt=(el.innerText||el.textContent||'').trim().replace(/\s*↗\s*$/,'').trim();
                if(/^[+＋﹢][\d０-９]+$/.test(txt.replace(/[\s\u00a0]+/g,'')) || !txt) continue;
                if(/^https?:\/\//i.test(href)) out += '['+txt+']('+href+')';
                else out += txt;
                continue;
            }
            if(tag==='strong'||tag==='b'){ const t=walk(el).trim(); if(t) out+='**'+t+'**'; continue; }
            if(tag==='em'||tag==='i'){ const t=walk(el).trim(); if(t) out+='*'+t+'*'; continue; }
            if(tag==='code'){ const t=(el.innerText||el.textContent||''); if(t) out+='`'+t+'`'; continue; }
            if(tag==='br'){ out+='\n'; continue; }
            if(/^h([1-6])$/.test(tag)){
                const n=parseInt(tag[1],10);
                out += '\n'+'#'.repeat(n)+' '+walk(el).trim()+'\n';
                continue;
            }
            if(tag==='ol'){
                let i=parseInt(el.getAttribute('start')||'1',10);    // v139：中间被别的内容隔开、接着往下编号的列表（start=11）从 11 数
                if(isNaN(i)) i=1;
                for(const li of el.children){
                    if(li.tagName && li.tagName.toLowerCase()==='li')
                        out += (i++)+'. '+walk(li).trim()+'\n';
                }
                out+='\n'; continue;
            }
            if(tag==='ul'){
                for(const li of el.children){
                    if(li.tagName && li.tagName.toLowerCase()==='li')
                        out += '- '+walk(li).trim()+'\n';
                }
                out+='\n'; continue;
            }
            if(tag==='li'){ out += '- '+walk(el).trim()+'\n'; continue; }
            const block=/^(p|div|blockquote|pre|section|article)$/.test(tag);
            out += walk(el);
            if(block) out+='\n';
        }
        return out;
    };
    const sels = ['[data-message-author-role="assistant"]','[class*="markdown"]',
        '[class*="prose"]','[class*="assistant"]','[class*="message-content"]'];
    let best=null, bestBottom=-1;
    for (const s of sels){
        let els; try{els=document.querySelectorAll(s)}catch(e){continue}
        for(const el of els){
            const r=el.getBoundingClientRect();
            const t=(el.innerText||'').trim();
            if(__cxAnchor && !(__cxAnchor.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING)) continue;
            if(r.width>200 && t.length>20 && r.bottom>bestBottom){ best=el; bestBottom=r.bottom; }
        }
    }
    if(!best && !__cxNodes) return '';
    let root, md;
    if (__cxNodes) {
        root = __cxNodes[0].parentElement || document.body;
        md = __cxNodes.map(n => walk(n)).join('\n\n').split('\n')
            .filter(l => !/^\s*(思考了|已思考|思考用时|Thought for|ChatGPT\s*(说|said)|你说|You said)/i.test(l)).join('\n');
    } else {
        root = __cxClimb(best);
        md = walk(root);
    }

    // ★画布 / 侧栏：把「不在回复气泡里」的表格也补抓进来。
    //   ChatGPT 把表格放进「写入 / Canvas」面板时，它是独立的一块 DOM，不在助手气泡里，
    //   上面的 walk 扫不到。这里只补抓表格（最稳、几乎不会误抓别的东西），并按内容去重。
    try {
        const seen = md.replace(/[\s|*_#`-]+/g,'');
        const extra = [];
        for(const tb of document.querySelectorAll('table')){
            if(root.contains(tb)) continue;                 // 已在回复气泡里，跳过
            const r = tb.getBoundingClientRect();
            if(!r || r.width < 120) continue;
            const tmd = tableToMd(tb);
            if(!tmd) continue;
            const key = tmd.replace(/[\s|*_#`-]+/g,'');
            if(key.length < 12) continue;
            if(seen.indexOf(key.slice(0, Math.min(40, key.length))) >= 0) continue;   // 已包含，去重
            extra.push(tmd);
        }
        if(extra.length){
            md = (md.trim() ? md.trim()+'\n\n' : '') + '——— 画布内容 ———\n' + extra.join('\n');
        }
    } catch(e){}

    md = md.replace(/[ \t]+\n/g,'\n').replace(/\n{3,}/g,'\n\n').replace(/[ \t]{2,}/g,' ').trim();
    return md;
}"""


# 找输入框的 JS 兜底：在页面下半部挑最可能的可编辑框，打 data-cx-input 标记
_FIND_INPUT_JS = r"""() => {
    const cands = [...document.querySelectorAll(
        'textarea, [contenteditable="true"], div[contenteditable], [role="textbox"]')];
    let best = null;
    for (const el of cands) {
        const r = el.getBoundingClientRect();
        if (r.width < 150 || r.height < 10 || r.height > 400) continue;
        // 输入框在底部：优先 bottom 最大的那个
        if (!best || r.bottom > best.bottom) best = { el, bottom: r.bottom };
    }
    if (!best) return false;
    document.querySelectorAll('[data-cx-input]').forEach(e => e.removeAttribute('data-cx-input'));
    best.el.setAttribute('data-cx-input', '1');
    return true;
}"""


# 找发送按钮的 JS 兜底：在输入区右下角挑「可点、非停止■方块」的图标键，打 data-cx-send 标记。
# 与 _PROBE_JS 的 SENDBTN1 同源：停止键=SVG 仅含 <rect>（■）；发送键=箭头(path)/语音。
_MARK_SEND_JS = r"""() => {
    const STOP_RE = /(停止|停止生成|中止|stop|stop generating|abort)/i;
    const SEND_RE = /(发送|send|提交|submit|send prompt)/i;
    const input = document.querySelector('[data-cx-input="1"]') ||
                  document.querySelector('textarea, [contenteditable="true"], [role="textbox"], .ProseMirror');
    const inRect = input ? input.getBoundingClientRect() : null;

    const desc = [];
    const cands = [];
    for (const b of document.querySelectorAll('button, [role="button"]')) {
        const r = b.getBoundingClientRect();
        if (r.width < 10 || r.height < 10) continue;
        // 只看输入框那一行附近（垂直接近 input），排除页面右侧那条竖排悬浮工具条
        const nearRow = inRect
            ? (r.top >= inRect.top - 24 && r.top <= inRect.bottom + 100)
            : (r.bottom > window.innerHeight * 0.55);
        if (!nearRow) continue;
        const lab = ((b.getAttribute('aria-label')||'') + ' ' + (b.getAttribute('title')||'') + ' ' +
                     (b.getAttribute('data-testid')||'')).trim();
        const svg = b.querySelector('svg');
        const onlyRect = svg && svg.querySelector('rect') &&
                         svg.querySelectorAll('path, line, polyline, polygon, circle').length === 0;
        const shape = svg ? (onlyRect ? 'rect■' : 'icon') : 'txt';
        const disabled = b.disabled || b.getAttribute('aria-disabled') === 'true';
        desc.push('[' + (lab || '无') + '|' + shape + '|' + (disabled ? '禁' : '可') +
                  '|x' + Math.round(r.right) + ']');
        if (disabled) continue;
        if (STOP_RE.test(lab) || onlyRect) continue;        // 停止键，跳过
        cands.push({ el: b, right: r.right,
                     cx: Math.round(r.x + r.width / 2), cy: Math.round(r.y + r.height / 2),
                     isSend: SEND_RE.test(lab), lab: lab || ('icon@x' + Math.round(r.right)) });
    }
    if (!cands.length) return { ok: false, desc: desc.join(' ') };
    // 语义 send 优先；否则取最靠右的（发送键在最右，+ / 麦克风在其左）
    cands.sort((a, b) => (b.isSend - a.isSend) || (b.right - a.right));
    const pick = cands[0];
    document.querySelectorAll('[data-cx-send]').forEach(e => e.removeAttribute('data-cx-send'));
    pick.el.setAttribute('data-cx-send', '1');
    return { ok: true, desc: desc.join(' '), pick: pick.lab, cx: pick.cx, cy: pick.cy };
}"""


# 在发送键上派发完整指针/鼠标事件序列（兼容只监听 pointerdown/onClick 的 React 按钮）
_DISPATCH_SEND_JS = r"""() => {
    const e = document.querySelector('[data-cx-send="1"]');
    if (!e) return false;
    const r = e.getBoundingClientRect();
    const x = r.x + r.width / 2, y = r.y + r.height / 2;
    const base = { bubbles: true, cancelable: true, composed: true, view: window,
                   clientX: x, clientY: y, button: 0 };
    const seq = ['pointerover','pointerenter','pointerdown','mousedown','pointerup','mouseup','click'];
    for (const t of seq) {
        let ev;
        try {
            ev = t.startsWith('pointer')
                ? new PointerEvent(t, { ...base, pointerId: 1, isPrimary: true })
                : new MouseEvent(t, base);
        } catch (_) {
            ev = new MouseEvent(t === 'pointerdown' ? 'mousedown'
                              : t === 'pointerup' ? 'mouseup' : t, base);
        }
        e.dispatchEvent(ev);
    }
    if (typeof e.click === 'function') { try { e.click(); } catch (_) {} }
    return true;
}"""


# 探测 JS（_wait_for_reply 每轮调用）——思考态识别 + 发送/停止按钮态 + 回复块抓取
_PROBE_JS = r"""() => {
    const __cxClimb = (el) => {
        if(!el) return el;
        let container = el, cur = el;
        for(let i=0;i<8;i++){
            const p = cur.parentElement;
            if(!p || p===document.body || p===document.documentElement) break;
            const r = p.getBoundingClientRect();
            if(!r || r.width < 200) break;
            let roleCount = 0;
            try { roleCount = p.querySelectorAll('[data-message-author-role]').length; } catch(e){}
            if(roleCount > 1) break;
            const cLen = (container.innerText||'').length;
            const pLen = (p.innerText||'').length;
            if(pLen <= cLen){ cur = p; continue; }
            if(pLen > cLen*2.6) break;
            container = p; cur = p;
        }
        return container;
    };
    const bodyText = (document.body.innerText || '').slice(0, 4000);
    const thinkingPatterns = [
        /^\s*正在思考[\s.…]*$/im, /^\s*思考中[\s.…]*$/im,
        /^\s*Thinking[\s.…]*$/im, /^\s*已思考\s*\d*\s*秒?\s*$/im,
    ];
    const hasThinkingIndicator = thinkingPatterns.some(p => p.test(bodyText));
    const looseThinkingPatterns = [
        /已思考\s*\d+\s*秒/, /Thought\s+for\s+\d+\s*[ms]/i, /Thinking\.\.\./,
        /Reasoning\b/i, /正在思考|思考中|正在推理|推理中/, /Working on it/i,
        /正在搜索|搜索中/, /Searching\b/i,
    ];
    const hasLooseThinking = looseThinkingPatterns.some(p => p.test(bodyText));
    const bodyTail = (document.body.innerText || '').slice(-4000);
    let thinkingDoneAll = [];
    try {
        thinkingDoneAll = bodyTail.match(/已思考\s*\d+\s*(?:秒|分钟|[sm]\b)|Thought\s+for\s+\d+\s*(?:seconds?|minutes?|[smh]\b)/gi) || [];
    } catch (e) { thinkingDoneAll = []; }
    const thinkingDoneCount = thinkingDoneAll.length;
    const thinkingDoneText = thinkingDoneAll.join('|');

    let genState = 'unknown';
    try {
        const STOP_RE = /(停止|停止生成|中止|stop|stop generating|abort)/i;
        const SEND_RE = /(发送|send|语音|voice|continue|继续)/i;
        let stopBtn = null, sendBtn = null;
        const btns = document.querySelectorAll('button, [role="button"], [data-testid]');
        for (const b of btns) {
            const r = b.getBoundingClientRect();
            if (r.width < 8 || r.height < 8) continue;
            if (r.bottom < window.innerHeight * 0.45) continue;
            const lab = ((b.getAttribute('aria-label')||'')+' '+(b.getAttribute('title')||'')
                +' '+(b.getAttribute('data-testid')||'')+' '+(b.getAttribute('data-state')||'')).trim();
            if (STOP_RE.test(lab)) { stopBtn = b; break; }
            if (!sendBtn && SEND_RE.test(lab)) sendBtn = b;
        }
        if (!stopBtn) {
            const cands = document.querySelectorAll('button svg, [role="button"] svg');
            for (const svg of cands) {
                const host = svg.closest('button, [role="button"]');
                if (!host) continue;
                const r = host.getBoundingClientRect();
                if (r.width < 8 || r.height < 8) continue;
                if (r.bottom < window.innerHeight * 0.45) continue;
                if (r.right < window.innerWidth * 0.5) continue;
                const hasRect = svg.querySelector('rect');
                const hasOnlyRect = hasRect && svg.querySelectorAll('path, line, polyline, polygon, circle').length === 0;
                // 加严：停止键的 ■ 是个接近正方形、居中的小方块。只有「整个 svg 仅含
                // 一个近正方形 rect」才算停止键，避免把「圆形背景(rect 圆角) + 箭头(实为
                // path)」或「rect 当背景的发送键」误判成停止键 —— 那会导致 AI 答完后
                // genState 一直卡在 generating、完成判定死等。
                let looksLikeStopSquare = false;
                if (hasOnlyRect) {
                    try {
                        const rc = svg.querySelector('rect');
                        const w = parseFloat(rc.getAttribute('width') || '0');
                        const h = parseFloat(rc.getAttribute('height') || '0');
                        // 近正方形（宽高比 0.7~1.4），且不是铺满整个 svg 的大背景块
                        const ratio = (w && h) ? (w / h) : 0;
                        const vb = (svg.getAttribute('viewBox') || '').split(/\s+/);
                        const vbw = vb.length === 4 ? parseFloat(vb[2]) : 0;
                        const fillsAll = vbw && w >= vbw * 0.9;   // 几乎铺满 → 更像背景，不是 ■
                        looksLikeStopSquare = (ratio >= 0.7 && ratio <= 1.4 && !fillsAll);
                        if (!w || !h) looksLikeStopSquare = true;  // 没标 width/height 的，保守仍当停止键
                    } catch (e) { looksLikeStopSquare = true; }
                }
                if (looksLikeStopSquare) { stopBtn = host; break; }
            }
        }
        if (stopBtn) { genState = 'generating'; }
        else {
            const ta = document.querySelector('textarea, [contenteditable="true"], [role="textbox"]');
            const taVisible = ta && ta.getBoundingClientRect && ta.getBoundingClientRect().height > 0;
            if (sendBtn || taVisible) genState = 'idle';
        }
    } catch (e) { genState = 'unknown'; }

    const selectors = ['[class*="markdown"]','[class*="prose"]','[class*="message-content"]',
        '[class*="msg-content"]','[class*="assistant"]','[class*="response"]',
        '[class*="reply-content"]','[class*="answer"]','[data-message-author-role="assistant"]'];
    const candidates = [];
    for (const sel of selectors) {
        let els; try { els = document.querySelectorAll(sel); } catch(e) { continue; }
        for (const el of els) {
            const r = el.getBoundingClientRect();
            const t = (el.innerText || '').trim();
            if (r.width > 200 && t.length > 30)
                candidates.push({ el, text: t, bottom: r.bottom, length: t.length, selector: sel });
        }
    }
    if (candidates.length > 0) {
        candidates.sort((a,b)=>b.bottom-a.bottom);
        const bottomEl = candidates[0].el;
        const topY = candidates[0].bottom;
        const near = candidates.filter(c => topY - c.bottom < 200);
        near.sort((a,b)=>b.length-a.length);
        let chosen = { text: near[0].text, bottom: near[0].bottom,
                       length: near[0].length, selector: near[0].selector };
        // 合并被拆成多个兄弟块的同一条回复（如序号列表），让「完成判定」和最终取文都拿到完整内容
        try {
            const cont = __cxClimb(bottomEl);
            const ct = (cont.innerText||'').trim();
            if (ct.length > chosen.text.length)
                chosen = { text: ct, bottom: cont.getBoundingClientRect().bottom,
                           length: ct.length, selector: 'climbed' };
        } catch(e) {}
        return { chosen, totalCandidates: candidates.length,
                 hasThinkingIndicator, hasLooseThinking, thinkingDoneCount, thinkingDoneText, genState };
    }
    if (hasThinkingIndicator || hasLooseThinking) {
        return { chosen: null, hasThinkingIndicator: true, hasLooseThinking,
                 thinkingDoneCount, thinkingDoneText, genState, status: 'thinking' };
    }
    let best = null;
    for (const el of document.querySelectorAll('div, article, section')) {
        const r = el.getBoundingClientRect();
        if (r.height < 50 || r.width < 200) continue;
        if (r.x < window.innerWidth * 0.15 || r.x > window.innerWidth * 0.85) continue;
        const t = (el.innerText || '').trim();
        if (t.length > 100 && (!best || r.bottom > best.bottom))
            best = { text: t, bottom: r.bottom, length: t.length, selector: 'fallback-div' };
    }
    return { chosen: best, hasThinkingIndicator, hasLooseThinking,
             thinkingDoneCount, thinkingDoneText, genState };
}"""


WATCHDOG_SEC = 300          # 浏览器 5 分钟没有任何动静 → 判定卡死，强制重启


def _browser_child_pids():
    """本进程（含 Playwright 驱动）下面所有浏览器进程的 pid。拿不到就返回空集合。"""
    try:
        import psutil
        out = set()
        for c in psutil.Process().children(recursive=True):
            try:
                n = (c.name() or "").lower()
            except Exception:
                continue
            if any(k in n for k in ("chrome", "msedge", "chromium", "headless_shell")):
                out.add(c.pid)
        return out
    except Exception:
        pass
    if os.name == "nt":
        try:
            import subprocess
            ps = ("$all = Get-CimInstance Win32_Process | Select-Object ProcessId,ParentProcessId,Name;"
                  "$all | ConvertTo-Json -Compress")
            raw = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True,
                                 timeout=20, creationflags=0x08000000).stdout
            rows = json.loads(raw.decode("utf-8", "replace") or "[]")
            kids, me = {}, os.getpid()
            for r in rows:
                kids.setdefault(r.get("ParentProcessId"), []).append(r)
            out, stack = set(), [me]
            while stack:
                for r in kids.get(stack.pop(), []):
                    stack.append(r.get("ProcessId"))
                    if any(k in (r.get("Name") or "").lower() for k in ("chrome", "msedge", "chromium")):
                        out.add(r.get("ProcessId"))
            return out
        except Exception:
            return set()
    return set()


def _kill_pids(pids):
    n = 0
    for pid in pids or ():
        try:
            import psutil
            pr = psutil.Process(pid)
            for c in pr.children(recursive=True):
                try:
                    c.kill()
                except Exception:
                    pass
            pr.kill()
            n += 1
            continue
        except ImportError:
            pass
        except Exception:
            continue
        try:
            if os.name == "nt":
                import subprocess
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], capture_output=True,
                               timeout=15, creationflags=0x08000000)
            else:
                os.kill(pid, 9)
            n += 1
        except Exception:
            pass
    return n


def _requeue_job(job):
    """被放弃的 worker 手里排着的 job，转交给新的 worker（等结果的人不受影响）。"""
    _worker()._ensure_thread()
    _worker()._jobs.put(job)


def _reset_worker(w, why, box=None, done=None):
    """看门狗：强制结束浏览器进程；worker 线程还是回不来，就整个换一个新 worker。"""
    try:
        w._log("⚠ 看门狗：%s → 强制关闭浏览器，下一条会重新打开" % why)
    except Exception:
        pass
    killed = 0
    try:
        killed = w._kill_browser_procs()
    except Exception:
        pass
    if done is not None and done.wait(90 if killed else 15):
        return                                    # worker 已经从卡死中恢复
    global _WORKER
    with _WORKER_LOCK:
        if _WORKER is not w:
            return
        w._dead = True
        nw = _WebWorker()
        nw._logger = w._logger
        _WORKER = nw
    # 旧 worker 队列里还没开始的 job 转给新 worker
    moved = 0
    while True:
        try:
            job = w._jobs.get_nowait()
        except Exception:
            break
        nw._ensure_thread()
        nw._jobs.put(job)
        moved += 1
    nw._ensure_thread()
    try:
        nw._log("⚠ 看门狗：旧的浏览器线程卡死回不来，已换一个新的（转交排队任务 %d 个）" % moved)
    except Exception:
        pass


def probe_pool():
    """（可在任意线程调用）快速测一下 AI 池网站现在能不能连上。返回 (能否连上, 说明)。
    不碰正在用的浏览器。"""
    try:
        w = _WebWorker()
        w._logger = lambda *_a, **_k: None
        cfg = load_config()
        w._resolve_routes(cfg)
        fixed = (cfg.get("aiPoolProxy") or "auto").lower()
        if fixed in ("direct", "system", "proxy"):
            modes = [fixed]
        else:
            modes = []
            learned = _load_routes().get("netMode")
            for m in ([learned] if learned else []) + (["proxy"] if w._cfg_proxy() else []) + ["system", "direct"]:
                if m and m not in modes:
                    modes.append(m)
        names = {"proxy": "走代理", "system": "系统代理", "direct": "直连"}
        errs = []
        for m in modes:
            ok, why = w._probe_one(m)
            if ok:
                return True, names.get(m, m)
            errs.append("%s：%s" % (names.get(m, m), why))
        return False, "；".join(errs)
    except Exception as e:
        return False, str(e)[:120]


class _Stuck(Exception):
    """对应参考代码里 e.code === 'STUCK'：卡死，可换卡重试。"""
    pass


# ─────────────── 单例 worker + 对外薄封装 ───────────────
_WORKER = None
_WORKER_LOCK = threading.Lock()


def _worker():
    global _WORKER
    with _WORKER_LOCK:
        if _WORKER is None:
            _WORKER = _WebWorker()
        return _WORKER


def set_logger(fn):
    _worker().set_logger(fn)


def chat_epoch():
    """当前网页对话线程的编号；变了就说明已经不是之前那个对话了。"""
    try:
        return _worker()._chat_epoch
    except Exception:
        return -1


def web_complete(prompt, on_progress=None, **opts):
    """同步阻塞：把 prompt 发给网页 ChatGPT，返回回复纯文本。"""
    if not is_available():
        raise RuntimeError("Playwright 未安装：pip install playwright && python -m playwright install chromium")
    # 总时限跟着本次要等的时长走（视频分析最多等 40 分钟）：两次尝试 + 换卡/登录的余量。
    # 以前固定 12 分钟，GPT 想久一点就被判失败，而它其实还占着浏览器 → 重试也跟着超时。
    wait_s = (opts.get("timeout") or 600000) / 1000.0
    attempts = 1 if opts.get("disableCardSwitch") else 2
    total = max(720, int(wait_s * attempts + 900))
    return _worker().submit("web_complete",
                            {"prompt": prompt, "on_progress": on_progress, **opts},
                            timeout=total)


def test_login(on_progress=None):
    if not is_available():
        return {"ok": False, "error": "Playwright 未安装"}
    return _worker().submit("test_login", {"on_progress": on_progress}, timeout=180)


def get_state():
    try:
        return _worker().get_state()
    except Exception as e:
        return {"state": "idle", "available": is_available(), "error": str(e)}


# ─────────────── v55：实时画面 / 显示隐藏浏览器（给 server 的接口用） ───────────────
def live_state(watch=False):
    """AI 池现在在干什么。watch=True 表示软件里有人开着实时画面（接下来 8 秒里会截图）。"""
    now = time.time()
    with _LIVE_LOCK:
        if watch:
            _LIVE["watch_until"] = now + 8
        d = {k: v for k, v in _LIVE.items() if k not in ("shot", "reply")}
        reply = _LIVE.get("reply") or ""
        d["reply_len"] = len(reply)
        d["reply_tail"] = reply[-8000:]
        d["has_shot"] = bool(_LIVE.get("shot"))
        d["log"] = list(_LIVE_LOG)[-25:]
    st = get_state()
    d["state"] = st.get("state")
    d["hasBrowser"] = bool(st.get("hasBrowser"))
    cfg = load_config()
    d["hidden_pref"] = bool(cfg.get("browserHidden", True))
    d["headless"] = cfg.get("headless") is True
    d["now"] = now
    return d


def live_shot():
    with _LIVE_LOCK:
        return _LIVE.get("shot") or b"", _LIVE.get("shot_ts") or 0


def request_window(action, wait=6.0):
    """显示 / 隐藏 AI 池浏览器。选择会被记住（下次打开浏览器也照这个来）。返回 (ok, 说明)。"""
    if action not in ("show", "hide"):
        return False, "不认识的操作"
    _save_pref(browserHidden=(action == "hide"))
    if load_config().get("headless") is True:
        return False, "现在是后台模式（设置里勾了不显示浏览器），没有窗口可显示"
    w = _worker()
    if not (w._browser and w._thread and w._thread.is_alive()):
        return True, ("记住了：下次 AI 池打开浏览器时会%s" % ("显示在屏幕上" if action == "show" else "放在屏幕外"))
    cmd = {"action": action, "done": threading.Event(), "res": {}}
    _UI_CMDS.put(cmd)
    if cmd["done"].wait(wait):
        r = cmd["res"]
        return bool(r.get("ok")), r.get("msg") or ""
    return True, "已发出指令，AI 池正忙着一步操作，几秒内就会生效"
