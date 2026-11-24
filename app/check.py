# -*- coding: utf-8 -*-
"""单词工作台 · 开始页「三样准备好了没」的检测：AI、词库、出片环境。

每样在自己的后台线程里一步一步检测，每一步马上写进 CHECK；界面每秒来取一次，所以能看到正在检测的实时情况。
用网页镜像 ChatGPT 时，界面还会带上浏览器画面（/api/ai/shot）。
检测只看、不改：不提交、不上传、不同步、不装东西（令牌的“真试写入”只建一个不挂在任何提交上的小数据块，仓库里看不到）。
"""
import json, re, threading, time, traceback, urllib.error, urllib.request
from pathlib import Path

import core as C
import video as V

ITEMS = ("ai", "repo", "env")
NAMES = {"ai": "AI", "repo": "词库", "env": "出片环境"}
_LOCK = threading.Lock()
CHECK = {k: {"state": "idle", "summary": "", "fix": "", "steps": [], "started": 0.0, "finished": 0.0, "run": 0}
         for k in ITEMS}
# state：idle 还没测 / running 正在测 / ok 好了 / bad 没好 / warn 能用但要留意（或者这次没法测）
# fix：没好时去哪儿修——gear（AI 设置）、settings（左边「设置」）、video（「出视频」页）


def _say(k, msg, ok=None):
    with _LOCK:
        CHECK[k]["steps"].append({"t": time.strftime("%H:%M:%S"), "msg": C.mask(str(msg))[:400], "ok": ok})
        del CHECK[k]["steps"][:-300]


def _run(k, fn):
    def say(msg, ok=None):
        _say(k, msg, ok)
    try:
        state, summary, fix = fn(say)
    except Exception as e:
        traceback.print_exc()
        say("检测本身出错了：%s" % e, False)
        state, summary, fix = "bad", "检测本身出错了：%s" % str(e)[:120], ""
    with _LOCK:
        CHECK[k].update(state=state, summary=C.mask(summary)[:300], fix=fix or "", finished=time.time())
    C.log("检测%s：%s %s" % (NAMES[k], {"ok": "✓", "bad": "✗", "warn": "!"}.get(state, ""), C.mask(summary)))


def start(what="all"):
    keys = list(ITEMS) if what == "all" else ([what] if what in ITEMS else [])
    if not keys:
        return {"ok": False, "msg": "不认识要检测什么：%s" % what}
    new, busy = [], []
    with _LOCK:
        for k in keys:
            it = CHECK[k]
            if it["state"] == "running":
                busy.append(NAMES[k])
                continue
            it.update(state="running", summary="正在检测…", fix="", steps=[], started=time.time(), finished=0.0,
                      run=it["run"] + 1)
            new.append(k)
    for k in new:
        threading.Thread(target=_run, args=(k, FUNCS[k]), daemon=True, name="check-" + k).start()
    if not new:
        return {"ok": True, "msg": "%s正在检测，看「检测详情」" % "、".join(busy)}
    return {"ok": True, "msg": "开始检测：%s" % "、".join(NAMES[k] for k in new)}


def reset(k):
    """换了用哪个 AI：上一种 AI 的检测结果不算数了，回到“还没检测”（正在测的不动）。"""
    with _LOCK:
        it = CHECK[k]
        if it["state"] != "running":
            it.update(state="idle", summary="", fix="", steps=[], started=0.0, finished=0.0, run=it["run"] + 1)


def snapshot(watch=False):
    """给界面：三样各自的状态和每一步；用网页镜像时带上浏览器的实时状态（watch＝详情开着，接下来几秒要截图）。"""
    now = time.time()
    with _LOCK:
        out = {k: dict(v, steps=list(v["steps"])) for k, v in CHECK.items()}
    for v in out.values():
        v["secs"] = int((v["finished"] or now) - v["started"]) if v["started"] else 0
    cfg = C.load_cfg()
    out["pv"] = cfg.get("provider")
    out["provider"] = C.provider_name(cfg)
    if out["pv"] == "web":
        W = _wm()
        if W:
            try:
                d = W.live_state(watch=watch)
                out["web"] = {k: d.get(k) for k in ("busy", "stage", "has_shot", "shot_ts", "hasBrowser", "visible",
                                                     "headless", "shot_err")}
            except Exception as e:
                out["web"] = {"error": str(e)}
    return out


def _secs(t):
    t = max(0, int(t))
    return "%d 秒" % t if t < 60 else "%d 分 %d 秒" % (t // 60, t % 60)


def _wm():
    try:
        import web_model
        return web_model
    except Exception:
        return None


# ═══════════════════════ ① AI ═══════════════════════
def check_ai(say):
    cfg = C.load_cfg()
    pv = cfg.get("provider")
    say("用的是：" + C.provider_name(cfg))
    return {"web": _ai_web, "relay": _ai_relay, "api": _ai_api, "mock": _ai_mock}.get(pv, _ai_web)(say, cfg)


# 网页镜像的步骤记录里有几句英文、几句程序话，换成能看懂的
_WEB_SAY = [
    (r"^AI 池网络：(.+)$", r"连 sorryios 的网络：\1"),
    (r"^AI 池测通：(.+)$", r"测网络：\1"),
    (r"^starting \(headless=\w+\)\.*$", "启动浏览器…"),
    (r"^launched via (.+)$", r"浏览器打开了（\1）"),
    (r"^try (.+?) failed: (.*)$", r"没用上 \1，换下一个浏览器（\2）"),
    (r"^context ready, savedState=YES$", "浏览器准备好了；有上次存下的登录信息，先试着直接用"),
    (r"^context ready, savedState=NO$", "浏览器准备好了；没有存下的登录信息，要登录"),
    (r"^站点路径=(\S+) 登录页=(\S+) 卡片页=(\S+)$", r"sorryios 登录页：\2"),
    (r"^诊断已保存: (.+) \(\.png/\.json\)$", r"这一刻的网页截图存在 \1.png（发给 Claude 能看出卡在哪）"),
    (r"^尝试复用 session → (.+)$", r"用上次的登录信息直接打开车队页 \1"),
    (r"^✓ session 复用成功，跳过登录$", "✓ 上次的登录还有效，不用再登"),
    (r"^session 已失效或卡片页地址变了 → 走完整登录$", "上次的登录过期了，重新登录"),
    (r"^✓ session 已保存，下次免登录$", "✓ 登录信息存下了，7 天内不用再登"),
    (r"^选 AI 卡片中\.*$", "在车队里挑一辆车…"),
    (r"^空闲(\d+)/正常(\d+)/繁忙(\d+) 张 → 随机选中【(.+?)】: (.+)$", r"车队里空闲 \1 辆、正常 \2 辆、繁忙 \3 辆，挑了一辆\4的：\5"),
    (r"^等聊天页就绪\.*$", "等 GPT 的聊天页打开…"),
    (r"^✓ 聊天页就绪$", "✓ GPT 的聊天页打开了"),
    (r"^还在等聊天页\.\.\. inputCount=(\S+) isCarlist=(\S+)$", r"还在等聊天页（输入框 \1 个，还在车队页：\2）"),
    (r"^✓ 就绪$", "✓ 登录、进车都好了"),
    (r"^发送 prompt \(len=(\d+), 第(\d+)次\)\.*$", r"把这句话填进输入框（\1 个字）"),
]
_WEB_SKIP = re.compile(r"^(Traceback|\s*File \"|job 出错|Skipping host requirements)")


def _web_line(msg):
    """网页镜像的一条步骤记录 → (要显示的话, 好/坏/中性)；不用显示的返回 None。"""
    m = str(msg or "").strip()
    if not m or _WEB_SKIP.search(m) or "\n  File " in m:
        return None
    for pat, rep in _WEB_SAY:
        if re.search(pat, m):
            m = re.sub(pat, rep, m)
            break
    ok = None
    if m.startswith("✓"):
        ok, m = True, m[1:].strip()
    elif m.startswith(("⚠", "⛔")):
        ok, m = False, m[1:].strip()
    elif re.search(r"失败|出错|异常|打不开|找不到|没成功", m) and not re.search(r"换|再试|重试|改用|改为|走完整|重新登录", m):
        ok = False
    return m[:300], ok


def _web_hint(err):
    if re.search(r"登录失败|账号|密码", err):
        return "账号密码对不对？点「去改 AI 设置」重新填、保存；或者在右边点「把浏览器拿到屏幕上」，在里面自己登录一次"
    if re.search(r"打不开|ERR_|net::|Timeout|timeout|超时", err):
        return "sorryios 打不开：先在你平时的浏览器里打开 sorryios.ai 看看。打得开就检查代理（Clash 用「规则」模式，别用海外全局）"
    if re.search(r"卡片|车队|选卡|聊天页", err):
        return "登录好了，但进 GPT 或进车没成功：把 app\\memory\\web_model_diag 里最新那个 png 截图发给 Claude"
    if "Playwright" in err:
        return "关掉软件，重新双击「启动.bat」，它会自己装 Playwright"
    return ""


def _ai_web(say, cfg):
    W = _wm()
    if not W:
        say("网页镜像用的组件（web_model.py）加载不了", False)
        return "bad", "网页镜像用的组件加载不了：把黑色窗口里的报错截图发给 Claude", ""
    if not W.is_available():
        say("没装 Playwright（软件靠它操作浏览器）：%s" % (W.playwright_import_error() or ""), False)
        return "bad", "没装 Playwright：关掉软件，重新双击「启动.bat」会自己装", ""
    say("Playwright 装好了（软件靠它操作浏览器）", True)
    wc = W.load_config()
    if not (wc.get("aiUsername") and wc.get("aiPassword")):
        lack = "账号和密码" if not wc.get("aiUsername") and not wc.get("aiPassword") else (
            "账号" if not wc.get("aiUsername") else "密码")
        say("还没填 sorryios 的%s" % lack, False)
        return "bad", "还没填 sorryios 的%s" % lack, "gear"
    u = wc["aiUsername"]
    say("sorryios 账号 %s，密码也填了" % (u[:3] + "***" + u[-2:] if len(u) > 6 else u[:1] + "***"), True)
    live = W.live_state()
    if live.get("busy"):
        say("网页 AI 正在给任务干活（现在：%s），检测不打断它" % (live.get("stage") or "…"))
        return "warn", "网页 AI 正在给任务干活，这次没测；右边能看到它的画面。任务做完再点「检测」", ""
    say("开始：打开浏览器 → 登录 sorryios → 进 GPT → 挑一辆车 → 问一句话。一般一两分钟；"
        "自动登录不成时会把浏览器拿到屏幕上等你登录，最多 5 分钟")
    t0, seq, box = time.time(), W.live_seq(), {}

    def go():
        try:
            box["r"] = W.test_login()
        except Exception as e:
            box["r"] = {"ok": False, "error": str(e)}
    th = threading.Thread(target=go, daemon=True, name="check-ai-web")
    th.start()
    while True:
        alive = th.is_alive()
        for n, _t, msg in W.live_log_since(seq):
            seq = n
            line = _web_line(msg)
            if line:
                say(*line)
        if not alive:
            break
        time.sleep(0.5)
    r = box.get("r") or {}
    used = _secs(time.time() - t0)
    if r.get("ok"):
        return "ok", "能用：登录、进 GPT、问一句话都通了（用了 %s）" % used, ""
    err = C.mask(str(r.get("error") or r.get("reply") or "没说原因")).split("\n")[0]
    say("没通：" + err, False)
    hint = _web_hint(err)
    if hint:
        say("怎么办：" + hint)
    return "bad", err[:160], "gear" if re.search(r"账号|密码|登录失败", err) else ""


def _reach(url, timeout=8):
    """这台电脑能不能连上这个网址（跟随系统代理）。返回 (能不能, 说明)。"""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return True, "HTTP %d" % r.status
    except urllib.error.HTTPError as e:
        return e.code < 500, "HTTP %d" % e.code
    except Exception as e:
        return False, str(getattr(e, "reason", e))[:80]


def _ai_relay(say, cfg):
    url = (cfg.get("relayUrl") or "").strip()
    if not re.match(r"^https?://", url):
        say("网页 AI 地址不对（要以 http:// 或 https:// 开头）：%s" % (url or "空的"), False)
        return "bad", "网页 AI 地址没填对", "gear"
    say("网页 AI 地址：%s" % url, True)
    host = re.sub(r"^https?://", "", url).split("/")[0]
    ok, why = _reach(url)
    if ok:
        say("这台电脑能连上 %s（%s）" % (host, why), True)
    else:
        say("软件直接连 %s 没连上（%s）。你平时的浏览器打得开就没事" % (host, why))
    ib = C.inbox_cfg(cfg)
    if not ib.get("enabled") or not ib.get("token"):
        say("“网页 AI 写完自己上传”没开：它写完要你点回复下面的「复制」，软件看到剪贴板就接着做")
        return "ok", "能用：在网页 AI 里粘贴、发送，写完点「复制」", ""
    say("“网页 AI 写完自己上传”开着：收件箱 %s 的 %s/ 文件夹" % (ib["repo"], ib["dir"]), True)
    say("检测收件箱令牌：真试一次写入（不会在仓库里留下文件）…")
    ok, msg = C.check_inbox()
    say(msg, ok)
    if ok:
        return "ok", "能用：网页 AI 写完自己把 Excel 传到中转仓库", ""
    return "bad", msg, "gear"


def _ai_api(say, cfg):
    a = cfg.get("api") or {}
    base, model, key = (a.get("baseUrl") or "").strip(), (a.get("model") or "").strip(), (a.get("key") or "").strip()
    say("接口地址 %s，模型 %s" % (base or "（空的）", model or "（空的）"), bool(base and model))
    if not (base and model):
        return "bad", "接口地址或模型名没填", "gear"
    if not key:
        say("还没填密钥", False)
        return "bad", "还没填接口密钥", "gear"
    say("密钥填了", True)
    say("发一句话试试（最多等 60 秒）…")
    url = base.rstrip("/")
    url += "" if url.endswith("/chat/completions") else "/chat/completions"
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": "只回两个字：好的"}],
                       "max_tokens": 16, "temperature": 0}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json", "Authorization": "Bearer " + key})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read().decode("utf-8", "replace"))
        text = (((d.get("choices") or [{}])[0].get("message") or {}).get("content") or "").strip()
        say("接口回了：%s" % (text[:80] or "（只想了没说话，也算通了）"), True)
        return "ok", "能用：%s 回了一句" % model, ""
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:200]
        why = {400: "请求不对（多半是模型名）", 401: "密钥不对或过期了", 402: "余额不足", 403: "没有权限",
               404: "地址或模型名不对", 429: "太频繁或额度用完了"}.get(e.code, "")
        say("接口报错 HTTP %d%s：%s" % (e.code, "（%s）" % why if why else "", detail), False)
        return "bad", "接口报错 %d%s" % (e.code, "：" + why if why else ""), "gear"
    except Exception as e:
        say("连不上接口：%s" % e, False)
        return "bad", "连不上接口：%s" % str(e)[:100], "gear"


def _ai_mock(say, cfg):
    say("模拟 AI 不连真的 AI，出的是假题，只能用来试流程", False)
    return "bad", "现在是模拟 AI，出不了真题：点「换一个」选别的", "gear"


# ═══════════════════════ ② 词库 ═══════════════════════
def check_repo(say):
    cfg = C.load_cfg()
    st = C.STATE
    br = cfg.get("branch") or "main"
    say("词库在 GitHub 仓库 %s（%s 分支）" % (C._main_repo(cfg) or cfg.get("repoUrl"), br))
    bad, notes = [], []
    if not (cfg.get("githubToken") or "").strip():
        say("还没填 GitHub 令牌：左边「设置 → GitHub 仓库」里填，保存后软件自己克隆", False)
        bad.append("没填 GitHub 令牌")
    else:
        say("检测 GitHub 令牌：真试一次写入（不会改仓库里的东西）…")
        ok, msg = C.check_token()
        say("GitHub 令牌：" + msg, ok)
        if not ok:
            bad.append("GitHub 令牌" + ("写不进仓库" if "写不进" in msg else "没测通"))
    rs, err = st.get("repo") or "", st.get("repoError") or ""
    if not (C.REPO / ".git").exists():
        say("本机还没有词库副本（%s）%s" % (rs, "：" + err[:160] if err else ""), False)
        return "bad", "本机还没有词库：" + (err[:120] or rs), "settings"
    say("本机词库副本：%s" % C.REPO, True)
    say("软件里的状态：%s%s" % (rs, "（%s）" % err[:160] if err else ""), True if rs == "就绪" else (None if rs == "正在同步" else False))
    if rs not in ("就绪", "正在同步"):
        bad.append(rs or "仓库没准备好")
    if st.get("offline"):
        say("从 %s 起没连上 GitHub，在用本机的词库；连上后软件会自己同步" % st["offline"])
    try:
        local = C.git("rev-parse", "HEAD", check=False).stdout.strip()
        say("问 GitHub 上最新的是哪一版…")
        r = C.net_git("ls-remote", "origin", "refs/heads/" + br, auth=True, timeout=60)
        remote = (r.stdout.split() or [""])[0]
        if not remote:
            say("GitHub 上没找到 %s 分支" % br, False)
            bad.append("GitHub 上没有 %s 分支" % br)
        elif remote == local:
            say("和 GitHub 上一样新（%s）" % local[:7], True)
        else:
            known = C.git("cat-file", "-e", remote + "^{commit}", check=False).returncode == 0
            ahead = int(C.git("rev-list", "--count", "%s..HEAD" % remote, check=False).stdout.strip() or 0) if known else 0
            if known and ahead:
                say("本机有 %d 个提交还没上传（GitHub 上是 %s，本机 %s）：做完一组会自己上传" % (ahead, remote[:7], local[:7]))
            else:
                say("GitHub 上有更新（%s），本机还是 %s：点「开始准备」时软件会先同步；想马上同步，到左边「设置」点「同步」"
                    % (remote[:7], local[:7]))
                notes.append("GitHub 上有更新，开始准备时会先同步")
    except Exception as e:
        say("没问到 GitHub：%s" % C.mask(str(e))[:200])
        notes.append("这次没问到 GitHub")
    ver, xlsx = st.get("version") or "", st.get("xlsx") or ""
    n_tab = len(C.TABLE.get("order") or [])
    if xlsx and (C.REPO / xlsx).exists():
        say("总表：%s（%s%s）" % (ver, Path(xlsx).name, "，%s 行" % format(n_tab, ",") if n_tab else ""), True)
    else:
        say("总表还没读到（%s）" % (xlsx or "仓库还没准备好"), False)
        bad.append("总表没读到")
    s = {}
    if C.idx_path().exists():
        try:
            _, rows = C.read_index()
            say("索引：%s 行" % format(len(rows), ","), True)
            if n_tab:
                v = C.verify()
                say("索引和总表对得上" if not v else v, not v)
                if v:
                    bad.append("索引和总表对不上")
            s = C.stats()
        except Exception as e:
            say("索引读不出来：%s" % e, False)
            bad.append("索引读不出来")
    else:
        say("还没有索引（%s）" % C.idx_path(), False)
        bad.append("没有索引")
    if s.get("total"):
        say("题目：%s 行有，%s 行还缺，%d 个词待人工%s" % (
            format(s["done"], ","), format(s["missing"], ","), s["manual"],
            "；按顺序下一个要出题的是 %s" % s["next"] if s.get("next") else ""), True)
    try:
        say("画面设置：%d 个词有（kit 里的和「词库/画面设置」里的）" % len(V.pic_words()), True)
    except Exception as e:
        say("画面设置没读出来：%s" % e)
    try:
        import pics
        sv, sed = pics.skill_version()
        if sv:
            same = not ver or not sed or sed == ver
            say("视频技能：%s（%s）%s" % (sv, sed, "，和总表是同一版" if same and ver else ""), True if same else None)
            if not same:
                say("视频技能是%s，总表是%s：两边对不上，画面按视频技能做" % (sed, ver))
                notes.append("视频技能和总表不是同一版")
        else:
            say("仓库里没读到视频技能的版本（引擎/视频/SKILL.md）", False)
            bad.append("没有视频技能")
    except Exception as e:
        say("视频技能的版本没读出来：%s" % e)
    n = C.pending_changes()
    say("%d 处修改还没上传：做完一组会自己上传，也可以在「更多」里点「现在上传」" % n if n else "本机没有没上传的修改",
        None if n else True)
    if bad:
        return "bad", "；".join(dict.fromkeys(bad)), "settings"
    summ = "就绪：总表%s" % ver
    if s.get("total"):
        summ += "，题目 %s 行有、%s 行还缺" % (format(s["done"], ","), format(s["missing"], ","))
    if notes:
        summ += "（%s）" % "；".join(notes)
    return "ok", summ, ""


# ═══════════════════════ ③ 出片环境 ═══════════════════════
def check_env(say):
    return V.env_check(say)


FUNCS = {"ai": check_ai, "repo": check_repo, "env": check_env}
