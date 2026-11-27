# -*- coding: utf-8 -*-
"""单词工作台 · 核心
仓库副本、总表、索引、体检、出题流水线、任务队列和定时都在这里。界面（server.py）只调这里的函数；视频在 video.py。

数据以 GitHub 仓库 wordsvideo 为准：软件在 data/repo 里放一份「词库」「引擎」「素材」的副本，
出好的题按仓库原来的格式存进 词/<首字母>/<单词>.json、更新 索引.tsv、在 README 进度表记一行，然后提交上传。
体检用的是仓库里 工具/lianxi.py 的正本，规矩和范例从 出题技能/zongbiao-questions.skill 里读。
"""
import base64, datetime, importlib, json, os, pickle, random, re, sqlite3, subprocess, sys
import threading, time, traceback, urllib.error, urllib.parse, urllib.request, zipfile
from pathlib import Path

APP = Path(__file__).resolve().parent
ROOT = APP.parent
DATA = ROOT / "data"
REPO = DATA / "repo"
DATA.mkdir(exist_ok=True)
CFG_PATH = DATA / "config.json"
DB_PATH = DATA / "app.db"
D = "词库/总表视频细节数据"
TABLE_DIR = "词库/总表"
END = "ZBQ-END"
TYPES = "听单形选改完"
KDS = {"变形", "词性转换", "短语", "用法", "易混"}
RESERVED = {"con", "prn", "aux", "nul"} | {"com%d" % i for i in range(1, 10)} | {"lpt%d" % i for i in range(1, 10)}
NOWIN = 0x08000000 if sys.platform == "win32" else 0
REPO_LOCK = threading.RLock()

DEFAULT_CFG = {
    "repoUrl": "https://github.com/Jacklee15333/wordsvideo.git",
    "branch": "main",
    "gitProxy": "",              # 例如 http://127.0.0.1:7892；空＝直连。连不上时会自动换另一种再试
    "githubToken": "",
    "gitName": "Jacklee15333",
    "gitEmail": "Jacklee15333@users.noreply.github.com",
    "provider": "web",           # web＝网页镜像 AI（sorryios）；api＝OpenAI 兼容接口（DeepSeek 等）；mock＝模拟（试用）
    "aiProxy": "",               # 网页镜像 AI 走的代理（空＝自动：系统代理 / 直连）
    "bestModel": True,           # 每次都切到菜单里最高级的模型、思考强度拉满
    "replyTimeoutMin": 30,
    "api": {"baseUrl": "https://api.deepseek.com", "key": "", "model": "deepseek-chat",
            "temperature": 0.3, "maxTokens": 8000, "timeout": 600},
    "groupSize": 25,             # 一组＝README 里一行、一次提交
    "chunkSize": 10,             # 一次发给 AI 几个词
    "fixRounds": 3,
    "maxWords": 12,              # 句子最多几个词（规矩：12 个词以内）
    "strictChecks": True,        # 在仓库体检之外，再查 4 个选项、2–5 题型不重复、句子长度
    "autoPush": True,
    "recordIssues": True,        # AI 指出的总表问题记进 README
    "attribution": "ChatGPT（网页镜像·单词工作台）",
    "video": {"distro": "Ubuntu-24.04", "winDir": "D:\\构词视频", "gpu": True, "holdQA": False},
    "window": {"enabled": False, "start": "22:00", "end": "07:00"},
    "promptExtra": "",
    "relayChunk": 25,            # 手动接力·出题：一份给网页 AI 几个词（选的词多，软件自动分成几份）
    "relayRound": 25,            # 手动接力·出题：网页 AI 每写完几个词上传一次
    "relayPicChunk": 10,         # 手动接力·画面：一份给网页 AI 几个词
    "relayPicRound": 1,          # 手动接力·画面：网页 AI 每写完几个词上传一次（一个词三四万字，一个一个传最稳）
    "relayFixChunk": 8,          # 手动接力·补画面：一份几个词（带着上次的画面设置，提示词长，一份少一些）
    "relayFixRound": 1,          # 手动接力·补画面：每写完几个词上传一次
    "relayTries": 3,             # v1.12.0：画面没过起草检查，网页 AI 在同一个对话里最多改几次（含第一次）
    "relayUrl": "https://zd87.com/ai-fleet/claude",
    "autoCont": True,          # v1.22.0：浏览器小助手自动点「Continue」、自动发「继续」
    "relayClipboard": True,      # 手动接力：自动把提示词放进剪贴板；你在网页里点“复制”回复，软件看到就自己接着做
    # 手动接力 · 收件箱：网页 AI 写完自己把回复传到 GitHub（不用你复制）；软件隔一会儿去看，看到就接着做。
    # 收件箱就用中转仓库 files-transfer-and-receive 的 inbox/ 文件夹。令牌会写进发给网页 AI 的提示词里，
    # 所以这里只能填“只给中转仓库”的小令牌（GitHub 上叫「收件箱用」）；能写所有仓库的万能令牌填进来会被拦下
    "relayInbox": {"enabled": False, "repo": "Jacklee15333/files-transfer-and-receive", "branch": "main", "token": "",
                   "dir": "inbox", "pollSec": 15},
    "port": 8766,
}


# ═══════════════════════ 配置 ═══════════════════════
def load_cfg():
    c = {}
    if CFG_PATH.exists():
        try:
            c = json.loads(CFG_PATH.read_text(encoding="utf-8"))
        except Exception:
            c = {}
    out = json.loads(json.dumps(DEFAULT_CFG))
    for k, v in c.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k].update(v)
        else:
            out[k] = v
    if out.get("provider") not in PROVIDERS:
        # v1.8.1 以前：左边「设置」的下拉框里没有“手动接力”，在那里保存一次就把 relay 存成了空的。空的就是原来的手动接力
        out["provider"] = "relay" if out.get("provider") == "" else "web"
    return out


PROVIDERS = ("web", "api", "relay", "mock")


def save_cfg(patch):
    c = load_cfg()
    patch = dict(patch or {})
    if "provider" in patch and patch["provider"] not in PROVIDERS:      # 认不出的不存，保留原来的
        patch.pop("provider")
    for k, v in patch.items():
        if isinstance(v, dict) and isinstance(c.get(k), dict):
            c[k].update(v)
        else:
            c[k] = v
    CFG_PATH.write_text(json.dumps(c, ensure_ascii=False, indent=1), encoding="utf-8")
    return c


def now():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def mask(s):
    cfg = load_cfg()
    s = str(s)
    for t in (cfg.get("githubToken") or "", (cfg.get("relayInbox") or {}).get("token") or ""):
        if t.strip():
            s = s.replace(t.strip(), "***")
    return re.sub(r"(gh[pousr]_|github_pat_)[A-Za-z0-9_]{8,}", r"\1***", s)


# ═══════════════════════ 数据库 ═══════════════════════
_DB_LOCK = threading.RLock()
_DB = None


def db():
    global _DB
    if _DB is None:
        _DB = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        _DB.row_factory = sqlite3.Row
        _DB.execute("PRAGMA journal_mode=WAL")
        _DB.executescript("""
        CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY, kind TEXT, title TEXT, params TEXT, status TEXT,
            created TEXT, run_after REAL DEFAULT 0, started TEXT, finished TEXT, progress TEXT, summary TEXT, error TEXT);
        CREATE TABLE IF NOT EXISTS schedules(id INTEGER PRIMARY KEY, name TEXT, kind TEXT, params TEXT, at TEXT,
            days TEXT, enabled INTEGER DEFAULT 1, last_date TEXT);
        CREATE TABLE IF NOT EXISTS logs(id INTEGER PRIMARY KEY, task_id INTEGER, ts TEXT, msg TEXT);
        CREATE TABLE IF NOT EXISTS calls(id INTEGER PRIMARY KEY, task_id INTEGER, ts TEXT, kind TEXT, words TEXT,
            prompt TEXT, reply TEXT, secs REAL, ok INTEGER, error TEXT, provider TEXT);
        CREATE TABLE IF NOT EXISTS manual(word TEXT PRIMARY KEY, errors TEXT, draft TEXT, attempts INTEGER, ts TEXT, source TEXT);
        CREATE TABLE IF NOT EXISTS groups(id INTEGER PRIMARY KEY, task_id INTEGER, label TEXT, words TEXT, saved TEXT,
            failed TEXT, fixed TEXT, commit_id TEXT, pushed INTEGER, ts TEXT, provider TEXT);
        CREATE TABLE IF NOT EXISTS changes(id INTEGER PRIMARY KEY, request TEXT, status TEXT, files TEXT, notes TEXT,
            diff TEXT, edits TEXT, error TEXT, ts TEXT, task_id INTEGER);
        CREATE TABLE IF NOT EXISTS picfail(word TEXT PRIMARY KEY, errors TEXT, ts TEXT);
        CREATE TABLE IF NOT EXISTS issues(id INTEGER PRIMARY KEY, word TEXT, text TEXT, ts TEXT, task_id INTEGER);
        """)
        _DB.commit()
    return _DB


def q(sql, args=(), one=False):
    with _DB_LOCK:
        cur = db().execute(sql, args)
        rows = [dict(r) for r in cur.fetchall()]
    return (rows[0] if rows else None) if one else rows


def x(sql, args=()):
    with _DB_LOCK:
        cur = db().execute(sql, args)
        db().commit()
        return cur.lastrowid


_LIVE = []          # 最近的日志（给界面滚动显示）
_LIVE_LOCK = threading.Lock()


def log(msg, task_id=None):
    msg = mask(msg)
    line = "%s %s" % (now(), msg)
    print(line, flush=True)
    with _LIVE_LOCK:
        _LIVE.append({"ts": now(), "msg": msg, "task": task_id})
        del _LIVE[:-300]
    try:
        x("INSERT INTO logs(task_id, ts, msg) VALUES(?,?,?)", (task_id, now(), msg))
    except Exception:
        pass


def live_logs(n=80):
    with _LIVE_LOCK:
        return list(_LIVE[-n:])


def manual_words():
    return {r["word"] for r in q("SELECT word FROM manual")}


# ═══════════════════════ git ═══════════════════════
class Fatal(Exception):
    """要人来处理的问题：任务停下"""


GITC = ["git", "-c", "core.quotepath=off", "-c", "core.protectNTFS=false", "-c", "core.longpaths=true",
        "-c", "core.autocrlf=false", "-c", "advice.detachedHead=false"]
NET_ERR = ("Failed to connect", "Could not resolve", "timed out", "Connection reset", "proxy", "Proxy",
           "unable to access", "SSL", "Couldn't connect", "early EOF", "RPC failed")


def git(*args, auth=False, check=True, cwd=None, timeout=900, proxy=None):
    cfg = load_cfg()
    cmd = list(GITC)
    px = cfg.get("gitProxy") if proxy is None else proxy
    if px:
        cmd += ["-c", "http.proxy=" + px, "-c", "https.proxy=" + px]
    if auth and cfg.get("githubToken"):
        b = base64.b64encode(("x-access-token:" + cfg["githubToken"].strip()).encode()).decode()
        cmd += ["-c", "http.extraHeader=Authorization: Basic " + b]
    cmd += ["-c", "user.name=" + cfg["gitName"], "-c", "user.email=" + cfg["gitEmail"]]
    cmd += list(args)
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="never")
    if cwd is None:
        # 只在 data\repo 里找仓库：副本坏了也绝不往上找到软件所在的那个仓库（你 GitHub Desktop 克隆的那个）
        env["GIT_CEILING_DIRECTORIES"] = str(DATA)
    r = subprocess.run(cmd, cwd=str(cwd or REPO), capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=timeout, env=env, creationflags=NOWIN)
    if check and r.returncode:
        err = mask((r.stderr or r.stdout).strip()[-800:])
        if re.search(r"Authentication failed|could not read Username|403|401|Repository not found", err):
            err = "GitHub 不让进：令牌不对、过期了，或者没给这个仓库的权限（设置里重新填令牌、点「检测令牌」）。原话：" + err[-200:]
        raise Fatal("git %s 失败：%s" % (" ".join(args[:2]), err))
    return r


def _is_net(e):
    t = str(e)
    return any(k in t for k in NET_ERR) and not re.search(r"returned error|Authentication|不让进|not found", t)


def _proxy_candidates():
    """连不上 GitHub 时挨个试：直连、Windows 系统代理、本机常见的代理端口（Clash 7890/7892/7897，v2rayN 10809…）。"""
    import socket
    out = [""]
    try:
        sp = urllib.request.getproxies().get("https") or urllib.request.getproxies().get("http")
        if sp:
            out.append(sp if "://" in sp else "http://" + sp)
    except Exception:
        pass
    for port in (7890, 7892, 7897, 7891, 10809, 10808, 1080, 8080):
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.3):
                out.append("http://127.0.0.1:%d" % port)
        except Exception:
            pass
    return out


def net_git(*args, **kw):
    """要连 GitHub 的 git 命令：连不上就换网络方式再试（设置里的代理 → 直连 → 系统代理 → 本机代理端口），
    试通了就记进设置，下次直接用。"""
    first = load_cfg().get("gitProxy") or ""
    try:
        return git(*args, **kw)
    except Fatal as e:
        if not _is_net(e):
            raise
        last = e
    for px in _proxy_candidates():
        if px == first:
            continue
        log("GitHub %s连不上，改用%s再试" % ("走代理 %s " % first if first else "直连", ("代理 " + px) if px else "直连"))
        try:
            r = git(*args, proxy=px, **kw)
            if r.returncode == 0:
                save_cfg({"gitProxy": px})
                log("这样能连上 GitHub，记进设置了：git 代理 = %s" % (px or "直连"))
            return r
        except Fatal as e:
            if not _is_net(e):
                raise
            last = e
    raise Fatal("连不上 GitHub（直连、系统代理、本机代理端口都试过了）。打开 Clash 之类的代理再试；或者在「设置 → git 代理」里填代理地址。最后一次：%s" % str(last)[-200:])


NUM = {"零": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}


def cn2int(s):
    total, cur = 0, 0
    for ch in s:
        if ch in NUM:
            cur = NUM[ch]
        elif ch == "十":
            total += (cur or 1) * 10; cur = 0
        elif ch == "百":
            total += (cur or 1) * 100; cur = 0
        else:
            return -1
    return total + cur


def _all_files():
    """仓库里所有文件（-z：不加引号、不转义；也不往 git 传中文路径参数，Windows 上最稳）。"""
    return [f for f in git("ls-tree", "-r", "-z", "--name-only", "HEAD").stdout.split("\0") if f]


def _latest_xlsx():
    files = _all_files()
    vers = {}
    for f in files:
        m = re.fullmatch(re.escape(TABLE_DIR) + r"/第([^/]+)版/(2词源拆分总表[^/]*\.xlsx)", f)
        if m and cn2int(m.group(1)) > 0:
            vers.setdefault(cn2int(m.group(1)), ("第%s版" % m.group(1), f))
    if not vers:
        near = [f for f in files if f.endswith(".xlsx")][:5]
        raise Fatal("仓库「%s」里没找到 第…版/2词源拆分总表*.xlsx（仓库里共 %d 个文件，xlsx 有：%s）" % (
            TABLE_DIR, len(files), "、".join(near) or "没有"))
    return vers[max(vers)]


def _sparse(xlsx):
    """只放「词库」「引擎」「素材」到磁盘上；Windows 不许的文件名（con 这类）不放。规则直接写文件，不用中文命令行参数。"""
    pats = ["/词库/", "/引擎/", "/素材/"]
    for f in _all_files():
        if os.path.splitext(os.path.basename(f))[0].split(".")[0].lower() in RESERVED:
            pats.append("!/" + f)
    git("config", "core.sparseCheckout", "true")
    git("config", "core.sparseCheckoutCone", "false")
    info = REPO / ".git" / "info"
    info.mkdir(parents=True, exist_ok=True)
    (info / "sparse-checkout").write_text("\n".join(pats) + "\n", encoding="utf-8")
    if git("rev-parse", "--verify", "-q", "HEAD", check=False).returncode == 0 and (REPO / D).exists():
        git("sparse-checkout", "reapply", check=False)


def rmtree(path):
    """删文件夹。Windows 上 git 的对象文件是只读的，普通删法删不掉、还不报错，所以先去掉只读再删。"""
    import shutil, stat
    def onerr(fn, p, _e):
        try:
            os.chmod(p, stat.S_IWRITE)
            fn(p)
        except Exception:
            pass
    if Path(path).exists():
        shutil.rmtree(str(path), onerror=onerr)
    if Path(path).exists():
        raise Fatal("删不掉旧的仓库副本 %s：关掉占用它的程序（资源管理器、GitHub Desktop 打开的这个文件夹），或者手动删掉再重开软件" % path)


STATE = {"repo": "未准备", "version": "", "xlsx": "", "repoError": "", "aligned": None}


def _repo_ok():
    """data\repo 是不是一个完整的、自己的仓库（不是半截、也不是借了上一层的仓库）。"""
    if not (REPO / ".git" / "HEAD").exists():
        return False
    r = git("rev-parse", "--show-toplevel", check=False)
    return r.returncode == 0 and Path(r.stdout.strip()).resolve() == REPO.resolve()


def _fix_root_sparse():
    """以前的版本副本坏了时，可能把“只放一部分文件”的设置写进了软件所在的仓库：发现了就关掉。"""
    if not (ROOT / ".git").exists():
        return
    r = git("config", "--get", "core.sparseCheckout", cwd=ROOT, check=False)
    if r.stdout.strip() == "true":
        git("sparse-checkout", "disable", cwd=ROOT, check=False)
        git("config", "--unset", "core.sparseCheckout", cwd=ROOT, check=False)
        log("软件所在的仓库被误设成了只放一部分文件，已经改回来（文件会全部回来）")


def ensure_repo(_again=True):
    """第一次：克隆稀疏副本（只要「总表视频细节数据」和最新总表）。之后：同步到 GitHub 最新。"""
    with REPO_LOCK:
        cfg = load_cfg()
        ok_mark = DATA / "repo_ok"
        if (REPO / ".git").exists() and not ok_mark.exists() and (REPO / D / "索引.tsv").exists():
            ok_mark.write_text(now(), encoding="utf-8")
        _fix_root_sparse()
        if REPO.exists() and (not ok_mark.exists() or not _repo_ok()):   # 半截的、坏的副本：删掉重来
            log("本机的仓库副本不完整，删掉重新克隆")
            ok_mark.unlink(missing_ok=True) if ok_mark.exists() else None
            rmtree(REPO)
        if not (REPO / ".git").exists():
            STATE["repo"] = "正在克隆仓库（第一次要一两分钟）"
            log("克隆仓库 %s → %s" % (cfg["repoUrl"], REPO))
            if REPO.exists():
                rmtree(REPO)
            if not cfg.get("githubToken") and cfg["repoUrl"].startswith("https://github.com/"):
                STATE["repo"] = "等令牌"
                raise Fatal("wordsvideo 是私有仓库：先到「设置 → GitHub 仓库」填令牌、点「保存设置」，软件会自动接着克隆")
            net_git("clone", "--filter=blob:none", "--no-checkout", "--depth", "1", "--branch", cfg["branch"],
                    "--config", "core.protectNTFS=false", "--config", "core.autocrlf=false",
                    "--config", "core.longpaths=true", cfg["repoUrl"], str(REPO), cwd=DATA, auth=True)
            ver, xlsx = _latest_xlsx()
            _sparse(xlsx)
            git("checkout", "-f", cfg["branch"])
            ok_mark.write_text(now(), encoding="utf-8")
        try:
            sync()
        except Fatal as e:
            if _again and "共 0 个文件" in str(e):
                log("本机的仓库副本是空的，删掉重新克隆")
                ok_mark.unlink(missing_ok=True)
                rmtree(REPO)
                return ensure_repo(_again=False)
            raise


def pending_changes():
    if not (REPO / ".git").exists():
        return 0
    out = git("status", "--porcelain", check=False).stdout
    return len([l for l in out.splitlines() if l.strip()])


def commit_pending(msg):
    with REPO_LOCK:
        git("add", "-A")
        if git("diff", "--cached", "--quiet", check=False).returncode == 0:
            return ""
        git("commit", "-q", "-m", msg)
        return git("rev-parse", "--short", "HEAD").stdout.strip()


def sync():
    """拉 GitHub 最新：本地没提交的先提交，本地没上传的提交放到最新版本后面；再核对总表和索引。"""
    with REPO_LOCK:
        cfg = load_cfg()
        br = cfg["branch"]
        if STATE.get("repo") != "就绪":       # 已经就绪的，同步时界面照常能用
            STATE["repo"] = "正在同步"
        if pending_changes():
            commit_pending("词库：人工修改、视频登记（单词工作台）")
        try:
            net_git("fetch", "-q", "origin", br, auth=True, timeout=120)
            STATE["offline"] = ""
        except Fatal as e:
            # 连不上 GitHub：本机已经有词库就先用本机的（出题会先存在本机，连上后再一起上传）
            if "连不上 GitHub" in str(e) and git("rev-parse", "--verify", "-q", "HEAD", check=False).returncode == 0 \
                    and (REPO / D / "索引.tsv").exists():
                STATE["offline"] = time.strftime("%H:%M")
                log("没连上 GitHub，先用本机的词库；连上以后会自动同步")
                ver, xlsx = _latest_xlsx()
                STATE.update(version=ver, xlsx=xlsx)
                load_table()
                bad = verify()
                STATE.update(aligned=not bad, repoError=bad, head=git("rev-parse", "--short", "HEAD").stdout.strip(),
                             repo="就绪" if not bad else "索引和总表对不上")
                return STATE
            raise
        if git("rev-parse", "--verify", "-q", "HEAD", check=False).returncode:
            ahead = behind = 0                    # 本地还没有任何提交（上次克隆没做完）：直接取远端
            git("checkout", "-q", "-f", "-B", br, "origin/" + br)
        else:
            ahead = int(git("rev-list", "--count", "origin/%s..HEAD" % br).stdout.strip() or 0)
            behind = int(git("rev-list", "--count", "HEAD..origin/%s" % br).stdout.strip() or 0)
        if not ahead:                             # 本地没有要上传的：和 GitHub 完全对齐（也修好半截的副本）
            git("checkout", "-q", "-f", "-B", br, "origin/" + br)
            behind = 0
        if behind and ahead:
            r = git("rebase", "origin/" + br, check=False)
            if r.returncode:
                git("rebase", "--abort", check=False)
                STATE["repo"] = "要人工处理"
                raise Fatal("本地有 %d 个没上传的提交，和 GitHub 上别人的新提交冲突（多半是云端也在出题）。"
                            "请先停掉另一边，再在设置里点「重新克隆仓库」。" % ahead)
        ver, xlsx = _latest_xlsx()
        if xlsx != STATE.get("xlsx") or not (REPO / D / "索引.tsv").exists():
            _sparse(xlsx)
            git("checkout", "-q", "-f", br, check=False)
        STATE.update(version=ver, xlsx=xlsx, ahead=ahead if not behind or not ahead else ahead)
        load_table()
        bad = verify()
        STATE["aligned"] = not bad
        STATE["repo"] = "就绪" if not bad else "索引和总表对不上"
        STATE["repoError"] = bad
        STATE["head"] = git("rev-parse", "--short", "HEAD").stdout.strip()
        STATE["synced"] = now()
        return STATE


def push():
    """上传：先提交没提交的，再推；被拒（GitHub 上有新提交）就先同步再推。"""
    with REPO_LOCK:
        commit_pending("词库：人工修改、视频登记（单词工作台）")
        br = load_cfg()["branch"]
        ahead = int(git("rev-list", "--count", "origin/%s..HEAD" % br).stdout.strip() or 0)
        if not ahead:
            return "没有要上传的"
        if not load_cfg().get("githubToken"):
            log("设置里没填 GitHub 令牌，试试用电脑上 git 自己记住的登录")
        for i in range(2):
            r = net_git("push", "-q", "origin", "HEAD:" + br, auth=True, check=False)
            if r.returncode == 0:
                STATE["head"] = git("rev-parse", "--short", "HEAD").stdout.strip()
                return "已上传 %d 个提交（%s）" % (ahead, STATE["head"])
            err = mask(r.stderr)
            if i == 0 and re.search(r"rejected|fetch first|non-fast-forward", err):
                log("GitHub 上有新提交，先同步再上传")
                sync()
                continue
            raise Fatal("上传失败：%s" % err.strip()[-500:])
        return ""


def check_token():
    cfg = load_cfg()
    tok = (cfg.get("githubToken") or "").strip()
    if not tok:
        return False, "还没填令牌"
    m = re.search(r"github\.com[/:]([^/]+)/([^/.]+)", cfg["repoUrl"])
    if not m:
        return False, "仓库地址认不出"
    req = urllib.request.Request("https://api.github.com/repos/%s/%s" % m.groups(),
                                 headers={"Authorization": "Bearer " + tok, "User-Agent": "chuti-studio"})
    hs = [urllib.request.ProxyHandler({"http": cfg["gitProxy"], "https": cfg["gitProxy"]})] if cfg.get("gitProxy") else []
    try:
        with urllib.request.build_opener(*hs).open(req, timeout=20) as r:
            d = json.loads(r.read().decode("utf-8"))
    except Exception as e:
        return False, "检测失败：%s" % str(e)[:120]
    w = can_write("%s/%s" % m.groups(), tok)       # 公开仓库的 permissions 会误报，真试一下
    if w is None:
        return bool(d.get("permissions", {}).get("push")), "能看到仓库，写权限没测出来（网络问题），上传时再看"
    return w, ("有写权限" if w else "这个令牌写不进 %s/%s：GitHub 令牌设置里要选上这个仓库，Contents 给 Read and write" % m.groups())


# ═══════════════════════ 总表、索引、README ═══════════════════════
TABLE = {"key": None, "words": {}, "order": []}
FIELDS = ["批次", "序号", "单词", "初中含义", "含义", "考点", "辨析", "拆分", "组合 → 现在的含义",
          "类型", "前缀", "词根", "单词部分", "后缀", "新·背景（只写在词族第一个词上）", "音变 / 字母变化", "词根变体处理", "读音现象"]      # v1.32.0：单词简历、各块的页面看总表


def load_table():
    p = REPO / STATE["xlsx"] if STATE.get("xlsx") else None
    if not p or not p.exists():
        raise Fatal("总表文件不在：%s" % p)
    try:                                              # v1.48.0：软件里有这一版总表就读软件里的，不再打开 Excel
        import tabledb
        v = tabledb.table_for_core()
        if v:
            if TABLE["key"] != v[0]:
                TABLE.update(key=v[0], words=v[1], order=v[2])
            return TABLE
    except Exception:
        pass
    st = p.stat()
    key = (str(p), st.st_size, int(st.st_mtime), "列v2")      # v1.32.0：多读了几列，旧缓存不用
    if TABLE["key"] == key:
        return TABLE
    cache = DATA / "table_cache.pkl"
    if cache.exists():
        try:
            c = pickle.loads(cache.read_bytes())
            if c.get("key") == key:
                TABLE.update(c)
                return TABLE
        except Exception:
            pass
    log("读总表 %s …" % STATE["xlsx"])
    import openpyxl
    ws = openpyxl.load_workbook(str(p), read_only=True)["拆分结果"]
    it = ws.iter_rows(values_only=True)
    h = [str(v) if v else "" for v in next(it)]
    ix = {k: i for i, k in enumerate(h)}
    words, order = {}, []
    for r in it:
        w = str(r[ix["单词"]] or "").strip()
        if not w:
            continue
        rec = {f: (str(r[ix[f]]).strip() if f in ix and r[ix[f]] is not None else "") for f in FIELDS}
        words.setdefault(w, []).append(rec)
        order.append((rec["批次"], rec["序号"], w))
    TABLE.update(key=key, words=words, order=order)
    try:
        cache.write_bytes(pickle.dumps({"key": key, "words": words, "order": order}))
    except Exception:
        pass
    return TABLE


def idx_path():
    return REPO / D / "索引.tsv"


def read_index():
    lines = idx_path().read_text(encoding="utf-8").splitlines()
    return lines[0], [l.split("\t") for l in lines[1:] if l.strip()]


def write_index(head, rows):
    idx_path().write_text(head + "\n" + "\n".join("\t".join(r) for r in rows) + "\n", encoding="utf-8")


def verify():
    _, rows = read_index()
    tab = TABLE["order"]
    bad = [i + 1 for i, (a, b) in enumerate(zip(tab, [(r[0], r[1], r[2]) for r in rows])) if a != b]
    if bad or len(tab) != len(rows):
        return "索引和总表对不上 %d 处（第 %s 行起）。总表可能改了顺序或增删了词，要先用维护技能更新索引，软件不会出题。" % (
            len(bad) + abs(len(tab) - len(rows)), bad[0] if bad else min(len(tab), len(rows)) + 1)
    return ""


def stats():
    if STATE.get("repo") not in ("就绪", "索引和总表对不上", "正在同步") or not idx_path().exists():
        return {}
    _, rows = read_index()
    man = manual_words()
    s = {"total": len(rows), "done": 0, "missing": 0, "manual": 0, "orig": 0}
    for r in rows:
        if r[4] == "细节数据有":
            s["done"] += 1
        elif r[4] == "缺":
            if r[2] in man:
                s["manual"] += 1
            else:
                s["missing"] += 1
        else:
            s["orig"] += 1
    s["words"] = len({r[2] for r in rows if r[4] == "细节数据有"})
    nxt = next((r for r in rows if r[4] == "缺" and r[2] not in man), None)
    s["next"] = nxt[2] if nxt else ""
    return s


def word_map():
    _, rows = read_index()
    man = manual_words()
    code = {"细节数据有": "h", "缺": "m"}
    import video as V
    pw, vd = V.pic_words(), V.videos()
    return {"codes": "".join(("r" if r[2] in man else "m") if r[4] == "缺" else code.get(r[4], "t") for r in rows),
            "vcodes": "".join("v" if V.folder_of(r[2]) in vd else ("p" if V.folder_of(r[2]) in pw else "n") for r in rows),
            "words": [r[2] for r in rows]}


def readme_path():
    return REPO / D / "README.md"


def next_group_label():
    lines = readme_path().read_text(encoding="utf-8").split("\n")
    last = [l for l in lines if re.match(r"\| \d{4}-\d\d-\d\d \| 题目第 \d+ 批", l)]
    if not last:
        return 1, 1
    m = re.search(r"题目第 (\d+) 批(?:第 (\d+) 组)?", last[-1])
    n, k = int(m.group(1)), int(m.group(2) or 4)
    return (n, k + 1) if k < 4 else (n + 1, 1)


def readme_log(label, first, last, saved, note, done):
    p = readme_path()
    lines = p.read_text(encoding="utf-8").split("\n")
    idx = [i for i, l in enumerate(lines) if re.match(r"\| \d{4}-\d\d-\d\d \| 题目第 \d+ 批", l)]
    note = note.replace("|", "／")
    row = "| %s | %s | %d | %s … %s（%s）。累计 %d 个词有题目 |" % (time.strftime("%Y-%m-%d"), label, saved, first, last, note, done)
    lines.insert((idx[-1] + 1) if idx else len(lines), row)
    p.write_text("\n".join(lines), encoding="utf-8")


def readme_issues():
    t = readme_path().read_text(encoding="utf-8")
    m = re.search(r"## 总表里看着不对的地方[^\n]*\n(.*?)(?=\n## |\Z)", t, re.S)
    return [l[2:].strip() for l in (m.group(1) if m else "").split("\n") if l.startswith("- ")]


def readme_add_issue(text):
    p = readme_path()
    lines = p.read_text(encoding="utf-8").split("\n")
    if ("- " + text) in lines:
        return False
    head = next((i for i, l in enumerate(lines) if l.startswith("## 总表里看着不对的地方")), None)
    if head is None:
        return False
    end = next((i for i in range(head + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    while end > head + 1 and not lines[end - 1].strip():
        end -= 1
    lines.insert(end, "- " + text)
    p.write_text("\n".join(lines), encoding="utf-8")
    return True


# ═══════════════════════ 简写稿 ↔ 原稿、体检 ═══════════════════════
_LX = {"mod": None, "mt": 0}


def lianxi():
    p = REPO / D / "工具" / "lianxi.py"
    mt = p.stat().st_mtime
    if _LX["mod"] is None or _LX["mt"] != mt:
        sys.path.insert(0, str(p.parent))
        import lianxi as L
        _LX.update(mod=importlib.reload(L), mt=mt)
    return _LX["mod"]


T = {"听": "听力", "单": "单项选择", "形": "适当形式填空", "选": "选词填空", "改": "改错", "完": "完成句子"}
ASK = {"单项选择": "选出最恰当的一项。", "适当形式填空": "用所给单词的适当形式填空。",
       "改错": "句子里有一处错误，找出来并改正。", "完成句子": "根据中文完成句子，每空一词。"}


def _opts(s):
    return [v.strip() for v in re.split(r"\s+/\s+", s.strip())]


def compact_line(l):
    """一行简写稿 → 原稿里的一道题（照仓库 工具/compact.py 的写法）。写法不对抛 ValueError。"""
    f = [v.strip() for v in l.split("|")]
    t = T.get(f[0])
    if not t:
        raise ValueError("开头要是 听/单/形/选/改/完 之一")
    kd = lambda i: f[i] if len(f) > i and f[i] else ""
    need = {"听力": 5, "单项选择": 4, "适当形式填空": 4, "选词填空": 5, "改错": 4, "完成句子": 5}[t]
    if len(f) < need:
        raise ValueError("「%s」题至少要 %d 段（用 | 分开），这一行只有 %d 段" % (f[0], need, len(f)))
    if t == "听力":
        qd = {"type": t, "ask": "听录音，回答问题：" + f[1], "listen": f[2], "opts": _opts(f[3]), "why": f[4]}
    elif t == "单项选择":
        qd = {"type": t, "ask": ASK[t], "stem": f[1].replace("⏎", "\n"), "opts": _opts(f[2]), "why": f[3], "kd": kd(4)}
    elif t == "适当形式填空":
        qd = {"type": t, "ask": ASK[t], "stem": f[1], "ans": f[2], "why": f[3], "kd": kd(4), "zh": ""}
    elif t == "选词填空":
        qd = {"type": t, "ask": "从 %s 中选一个，用适当形式填空。" % f[1], "stem": f[2], "ans": f[3], "why": f[4], "kd": kd(5), "zh": ""}
    elif t == "改错":
        qd = {"type": t, "ask": ASK[t], "stem": f[1], "ans": f[2], "why": f[3], "kd": kd(4), "zh": ""}
    else:
        qd = {"type": t, "ask": ASK[t], "zh": f[1], "stem": f[2].replace("⏎", "\n"), "ans": f[3], "why": f[4], "kd": kd(5)}
    if not qd.get("kd"):
        qd.pop("kd", None)
    return qd


def to_compact(qs):
    """原稿 → 简写稿（界面里改题用）。认不出的题型返回 None。"""
    out = []
    for qd in qs:
        t, kd = qd.get("type"), qd.get("kd", "")
        st = (qd.get("stem") or "").replace("\n", "⏎")
        o = " / ".join(qd.get("opts") or [])
        if t == "听力":
            out.append("听|%s|%s|%s|%s" % (qd["ask"].replace("听录音，回答问题：", ""), qd.get("listen", ""), o, qd["why"]))
        elif t == "单项选择":
            out.append("单|%s|%s|%s|%s" % (st, o, qd["why"], kd))
        elif t == "适当形式填空":
            out.append("形|%s|%s|%s|%s" % (st, qd["ans"], qd["why"], kd))
        elif t == "选词填空":
            m = re.match(r"从 (.+) 中选一个", qd["ask"])
            out.append("选|%s|%s|%s|%s|%s" % (m.group(1) if m else "", st, qd["ans"], qd["why"], kd))
        elif t == "改错":
            out.append("改|%s|%s|%s|%s" % (st, qd["ans"], qd["why"], kd))
        elif t == "完成句子":
            out.append("完|%s|%s|%s|%s|%s" % (qd.get("zh", ""), st, qd["ans"], qd["why"], kd))
        else:
            return None
    return out


_WORD_RE = re.compile(r"[A-Za-z]_{2,}|_{2,}|[A-Za-z]+(?:['’\-][A-Za-z]+)*")


def check(word, lines):
    """一个词的 7 行简写稿 → (原稿, 错误列表)。仓库 lianxi.py 的体检 + 几条附加检查。"""
    errs, qs = [], []
    if len(lines) != 7:
        errs.append("要正好 7 行（7 道题），写了 %d 行" % len(lines))
    for k, l in enumerate(lines):
        try:
            qs.append(compact_line(l))
        except Exception as e:
            errs.append("第 %d 行写法不对：%s" % (k + 1, e))
    if errs:
        return qs, errs
    L = lianxi()
    cells, daan = L.fmt_word(word, qs)
    errs += L.check_word(word, cells, daan)
    cfg = load_cfg()
    if cfg.get("strictChecks", True):
        ts = [qd["type"] for qd in qs[1:5]]
        if len(set(ts)) < 4:
            errs.append("第 2–5 题题型要互不相同（现在是 %s）" % "、".join(ts))
        for k, qd in enumerate(qs):
            if qd.get("opts") and len(qd["opts"]) != 4:
                errs.append("第 %d 题要正好 4 个选项" % (k + 1))
            for s in [qd.get("listen", "")] + (qd.get("stem") or "").split("\n"):
                n = len(_WORD_RE.findall(s))
                if n > int(cfg.get("maxWords", 12)):
                    errs.append("第 %d 题句子有 %d 个词（要 %d 个以内）" % (k + 1, n, cfg.get("maxWords", 12)))
            if "|" in json.dumps(qd, ensure_ascii=False):
                errs.append("第 %d 题正文里有“|”" % (k + 1))
    return qs, errs


def save_word(word, qs, version, attribution):
    """照仓库 工具/save_questions.py 的写法存一个词（已经体检过）。返回相对路径。"""
    L = lianxi()
    cells, daan = L.fmt_word(word, qs)
    slug = word.replace(" ", "_").replace("/", "_")
    rel = "词/%s/%s.json" % ((slug[:1].lower() if slug[:1].isalpha() else "_"), slug)
    p = REPO / D / rel
    if slug.lower() in RESERVED:
        slug += "_"                    # Windows 不许叫 con 这类名字：存成 con_.json（和 工具/save_questions.py 一样）
        rel = "词/%s/%s.json" % (slug[:1].lower(), slug)
        p = REPO / D / rel
    with REPO_LOCK:
        p.parent.mkdir(parents=True, exist_ok=True)
        rec = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"单词": word, "画面": None, "插图": []}
        try:
            av = (Path(__file__).parent / "VERSION").read_text(encoding="utf-8").strip()
        except Exception:
            av = ""
        rec.update({"总表版本": version, "题目": dict(zip(L.COLS, cells), 答案=daan), "题目原稿": qs,
                    "题目版本": ("单词工作台 v%s（出题规矩）、总表%s" % (av, version)) if av else "",      # v1.28.0：「做好的」里看用的哪个版本
                    "题目生成": time.strftime("%Y-%m-%d") + " " + attribution,
                    "题目检查": "维护技能 lianxi.py 体检 0 个问题"})
        p.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        head, rows = read_index()
        for r in rows:
            if r[2] == word:
                while len(r) < 7:
                    r.append("")
                r[4], r[6] = "细节数据有", rel
        write_index(head, rows)
    x("DELETE FROM manual WHERE word=?", (word,))
    try:                                   # 这个词已经有画面设置：里面的练习题也换成新出的
        import pics
        pics.refresh_lianxi(word)
    except Exception as e:
        log("画面设置里的练习题没更新（%s）" % str(e)[:100])
    try:                                   # v1.9.9：题目也存一个 Excel 在成果文件夹（题目\<单词>.xlsx）
        import results
        results.export_word(word, rec)
    except Exception as e:
        log("题目的 Excel 没存上（%s）：词库里的照常存好了" % str(e)[:120])
    return rel


def word_detail(word):
    _, rows = read_index()
    ir = [r for r in rows if r[2] == word]
    if not ir:
        return None
    rel = ir[0][6] if len(ir[0]) > 6 else ""
    rec = None
    if rel and (REPO / D / rel).exists():
        rec = json.loads((REPO / D / rel).read_text(encoding="utf-8"))
    m = q("SELECT * FROM manual WHERE word=?", (word,), one=True)
    draft = ""
    if m and m.get("draft"):
        draft = m["draft"]
    elif rec and rec.get("题目原稿"):
        c = to_compact(rec["题目原稿"])
        draft = "\n".join(c) if c else ""
    import video as V
    vinfo = {"pic": V.folder_of(word) in V.pic_words(), "video": V.videos().get(V.folder_of(word)),
             "files": V.video_files(word)}
    return {"word": word, "video": vinfo, "rows": [{"批次": r[0], "序号": r[1], "初中含义": r[3], "题目": r[4]} for r in ir],
            "table": TABLE["words"].get(word, []), "record": rec, "manual": m, "draft": draft}


def word_rows():
    """总词库每一行 + 准备情况：题目（有/缺/待人工/总表原有）、画面设置、视频。"""
    import video as V
    _, rows = read_index()
    man, pw, vd = manual_words(), V.pic_words(), V.videos()
    out = []
    for r in rows:
        st = "manual" if (r[4] == "缺" and r[2] in man) else {"细节数据有": "done", "缺": "missing"}.get(r[4], "orig")
        f = V.folder_of(r[2])
        q_ok, pic, vid = st in ("done", "orig"), f in pw, f in vd
        ready = "video" if vid else ("ready" if (q_ok and pic) else ("needpic" if q_ok else "needq"))
        out.append({"批次": r[0], "序号": r[1], "word": r[2], "meaning": r[3], "status": st,
                    "pic": pic, "video": vid, "ready": ready})
    return out


READY_NAMES = {"video": "有视频", "ready": "准备好了，可以出片", "needpic": "缺视频画面", "needq": "缺题目"}


def search_words(text="", status="", page=1, size=60, ready=""):
    rows = word_rows()
    t = (text or "").strip().lower()
    counts = {k: 0 for k in READY_NAMES}
    for r in rows:
        counts[r["ready"]] += 1
    out = [r for r in rows if (not status or r["status"] == status) and (not ready or r["ready"] == ready)
           and (not t or t in r["word"].lower() or t in r["meaning"])]
    return {"total": len(out), "page": page, "items": out[(page - 1) * size: page * size],
            "counts": counts, "all": [r["word"] for r in out] if len(out) <= 3000 else []}


def prepare(words):
    """准备出片：缺题目的排进出题；缺画面设置的先记下（自动写画面设置是下一步的功能）。"""
    rows = {r["word"]: r for r in word_rows()}
    needq = [w for w in words if w in rows and rows[w]["status"] in ("missing", "manual")]
    needpic = [w for w in words if w in rows and not rows[w]["pic"]]
    tid = None
    if needq:
        x("DELETE FROM manual WHERE word IN (%s)" % ",".join("?" * len(needq)), needq)
        tid = add_task("redo", {"words": needq}, title="准备出片：给 %d 个词出题" % len(needq))
        RUNNER.wake.set()
    pic_ok = [w for w in needpic if rows[w]["status"] in ("done", "orig")]
    ptid = None
    if needpic:
        # 缺题目的先出题，题目好了再做画面：所以画面任务排在出题后面
        ptid = add_task("pics", {"words": needpic}, title="准备出片：给 %d 个词做视频画面" % len(needpic))
        RUNNER.wake.set()
    return {"task": tid, "ptask": ptid, "needq": len(needq), "needpic": len(needpic), "picNow": len(pic_ok),
            "ready": len([w for w in words if w in rows and rows[w]["ready"] == "ready"])}


# ═══════════════════════ 提示词 ═══════════════════════
def skill_texts():
    p = REPO / D / "出题技能" / "zongbiao-questions.skill"
    with zipfile.ZipFile(str(p)) as z:
        names = z.namelist()
        get = lambda end: z.read(next(n for n in names if n.endswith(end))).decode("utf-8")
        rules, example = get("references/rules.md"), get("references/example.md")
    rules = rules.split("## 五")[0]
    rules = re.sub(r"并用 `log\.py issue[^`]*` 记下来", "并在回复最后的「总表问题」里写出来", rules)
    rules = re.sub(r"[（(]?save\.py 会列出来，改好再存[）)]?", "（程序会自动检查，没过的会退回给你改）", rules)
    return rules.strip(), example.strip()


def material(word):
    rows = TABLE["words"].get(word) or [{}]
    c = lambda r, k, n: (r.get(k) or "").replace("\n", " / ")[:n]
    r = rows[0]
    out = ["@%s｜%s｜%s" % (word, c(r, "初中含义", 80), c(r, "考点", 700) or "（总表没写考点：考意思、搭配、和形近词的区别）")]
    if r.get("含义"):
        out.append("  含义：" + c(r, "含义", 200))
    for r2 in rows[1:]:
        out.append("  【总表里还有一行，两个意思都要考】%s｜%s" % (c(r2, "初中含义", 80), c(r2, "考点", 300)))
    if r.get("辨析"):
        out.append("  辨析：" + c(r, "辨析", 300))
    return "\n".join(out)


CHECKS = """- 每个词正好 7 行；第 1 行是“听”；第 2–5 行四种题型互不相同（从 单 / 形 / 选 / 改 / 完 里挑）；第 6、7 行行末必须写考点（变形 / 词性转换 / 短语 / 用法 / 易混 之一）。
- 听力题和单项选择题正好 4 个选项，第一个写对的，选项不能重复（只差大小写也算重复）。
- 答案就是本词原形的最多 1 道（选择题看对的那个选项，填空看答案，整串相同才算）。
- 空格写成 6 个下划线 ______；几个空就几个答案，用中文分号“；”隔开；改错的答案写“错的 → 对的”。
- 每个英语句子不超过 {maxw} 个词；正文里不能出现“|”。"""

OUTFMT = """【输出格式（程序按这个格式自动读，请严格照做）】
1. 只输出一个代码块（第一行写 ```text），里面按顺序写全部 {n} 个词：每个词先一行“@单词”（和上面写的一字不差），接着 7 行题目。
2. 代码块外面不要写任何解释。
3. 代码块后面：如果总表材料里有明显写错的地方（编造的变形、可数不可数写反、含义残缺等），写一行“总表问题：”，下面每处一行“- 单词：哪里不对，正确应是……”；没有就不写这部分。
4. 最后单独一行写：{end}"""


def build_prompt(words):
    rules, example = skill_texts()
    cfg = load_cfg()
    return "\n\n".join(filter(None, [
        "你是一位中学英语老师的出题助手。下面按「词源拆分总表」的顺序给你 %d 个单词的材料，请给每个词出 7 道练习题和答案，写成“简写稿”。" % len(words),
        "【出题规矩】\n" + rules,
        "【简写稿范例（都通过了程序体检）】\n" + example,
        "【程序会自动体检，没过的会退回重写】\n" + CHECKS.format(maxw=cfg.get("maxWords", 12)),
        cfg.get("promptExtra", "").strip(),
        "【材料】（每个词第一行：@单词｜初中含义｜考点；下面是含义、辨析）\n" + "\n".join(material(w) for w in words),
        OUTFMT.format(n=len(words), end=END)]))


def build_fix_prompt(items):
    """items: [(word, lines, errors)]"""
    rules, example = skill_texts()
    cfg = load_cfg()
    parts = []
    for w, lines, errs in items:
        parts.append("%s\n  上次写的：\n%s\n  体检报错：%s" % (
            material(w), "\n".join("    " + l for l in lines) or "    （没写出来）", "；".join(errs)))
    return "\n\n".join(filter(None, [
        "你是一位中学英语老师的出题助手。下面 %d 个词的简写稿没通过程序体检。请按报错改好，每个词重新写完整的“@单词 + 7 行”（没报错的题也要照写）。" % len(items),
        "【出题规矩】\n" + rules,
        "【简写稿范例】\n" + example,
        "【程序体检的要求】\n" + CHECKS.format(maxw=cfg.get("maxWords", 12)),
        cfg.get("promptExtra", "").strip(),
        "【要改的词：材料、上次写的稿、报错】\n" + "\n\n".join(parts),
        OUTFMT.format(n=len(items), end=END)]))


def parse_reply(text, wanted):
    """AI 回复 → ({单词: [题目行]}, [总表问题])。宽松：代码块有没有都行，编号、全角竖线、多余空格都容忍。"""
    text = (text or "").replace("\r", "")
    want = {w: w for w in wanted}
    low = {w.lower(): w for w in wanted}
    got, cur = {}, None
    issues, in_iss = [], False
    for raw in text.split("\n"):
        l = raw.strip().strip("`").strip()
        if not l:
            continue
        if re.match(r"^总表问题[:：]?", l):
            in_iss, cur = True, None
            continue
        if in_iss:
            m = re.match(r"^[-*•]\s*(.+?)[:：]\s*(.+)$", l)
            if m and END not in l:
                issues.append("%s：%s" % (m.group(1).strip(), m.group(2).strip()))
            continue
        m = re.match(r"^(?:\d+[.、)]\s*)?[@＠]\s*(.+?)\s*$", l.strip("*#>_ "))
        if m:
            name = re.split(r"[｜|]", m.group(1))[0].strip().strip("*_ ")
            cur = want.get(name) or low.get(name.lower())
            if cur:
                got[cur] = []
            continue
        l2 = re.sub(r"^(?:\d+[.、)]\s*|[-*•]\s*)", "", l)
        m = re.match(r"^([听单形选改完])\s*[|｜]", l2)
        if m and cur is not None:
            l2 = l2.replace("｜", "|")
            l2 = re.sub(r"\s*\|\s*", "|", l2)
            got[cur].append(l2)
    return got, issues


# ═══════════════════════ AI ═══════════════════════
class Stopped(Exception):
    pass


def _web():
    import web_model
    return web_model


AI_LIVE = {"reply": "", "provider": "", "kind": "", "words": [], "started": 0.0, "done": 0.0, "secs": 0}


RELAY_SKIP = set()
RELAY = {"id": 0, "status": "", "prompt": "", "words": [], "kind": "", "reply": "", "ts": 0.0}
# v1.10.3：这一批每一轮的经过（提示词 → 收到回复 → 检查过了/没过），黄框里一步一步显示；换一批词就重新记
RELAY_HIST = []
INBOX_LAST = {"files": [], "ts": 0.0}        # 最近一次看中转仓库 inbox/ 里有哪些文件


def _say(msg):
    """只在黑色窗口里显示（不进步骤记录，免得每十几秒一行把记录刷满）。"""
    try:
        print("%s %s" % (now(), mask(msg)), flush=True)
    except Exception:
        pass


def _dur(s):
    s = max(0, int(s))
    return "%d 秒" % s if s < 60 else "%d 分 %d 秒" % (s // 60, s % 60)


HIST_FILE = DATA / "relay_hist.json"


def _hist_save():
    try:
        HIST_FILE.write_text(json.dumps(RELAY_HIST, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def _hist_load(tid, words):
    """软件重开、同一个任务接着做同一批词：把重开前的几轮接上（没等到的标成“软件重开了”）。"""
    try:
        h = json.loads(HIST_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []
    if not h or h[-1].get("tid") != tid or h[-1].get("words") != list(words):
        return []
    for x in h:
        if not x.get("res"):
            x.update(res="gone", detail="软件关掉重开了，这一轮没等到回复（重开后重新出了提示词）")
    return h


def _iso(ts):
    import calendar
    try:
        return float(calendar.timegm(time.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")))
    except Exception:
        return 0.0


def inbox_uploads(n=6):
    """中转仓库里网页 AI 最近几次上传（它的提交说明是“接力回复 文件路径”）：[{ts, path}]，新的在前。"""
    ib = inbox_cfg()
    st, d = _gh("GET", "/repos/%s/commits?per_page=20&sha=%s" % (ib["repo"], urllib.parse.quote(ib["branch"] or "main")), ib["token"])
    if st != 200 or not isinstance(d, list):
        return None
    out = []
    for c in d:
        cm = c.get("commit") or {}
        m = (cm.get("message") or "").strip()
        if m.startswith("接力回复 "):
            out.append({"ts": _iso((cm.get("author") or {}).get("date") or ""), "path": m[5:].strip()})
    return out[:n]


GEN_HIST = DATA / "gen_hist.json"


def gen_hist_add(kind, words, results, tid=None, src="", t0=0.0):
    """生成历史（v1.10.11）：一批做完记一行——哪些词、每个词做好了没有（没做成的一句原因）。kind：pic / q。"""
    try:
        h = json.loads(GEN_HIST.read_text(encoding="utf-8")) if GEN_HIST.exists() else []
    except Exception:
        h = []
    t = time.time()
    h.append({"id": int(t * 1000), "kind": kind, "t": t, "t0": t0 or t, "tid": tid, "src": src, "words": list(words),
              "res": {w: {"ok": bool((results.get(w) or {}).get("ok")), "detail": str((results.get(w) or {}).get("detail") or "")[:200]}
                      for w in words}})
    del h[:-500]
    try:
        GEN_HIST.write_text(json.dumps(h, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def gen_hist_list(kind):
    """生成历史，新的在前。以前做完、还没记历史的任务（v1.10.11 以前）照任务记录补上：词现在有没有画面/题目就是结果。"""
    try:
        h = [x for x in json.loads(GEN_HIST.read_text(encoding="utf-8")) if x.get("kind") == kind] if GEN_HIST.exists() else []
    except Exception:
        h = []
    have = {x.get("tid") for x in h}
    if kind == "pic":
        import video as V
        pw = V.pic_words()
        fail = {r["word"]: r["errors"] for r in q("SELECT word, errors FROM picfail")}
        for t in q("SELECT id, params, started, finished, status FROM tasks WHERE kind='pics' AND status IN ('已完成','已取消','出错') ORDER BY id"):
            if t["id"] in have:
                continue
            try:
                ws = json.loads(t["params"] or "{}").get("words") or []
            except Exception:
                ws = []
            if not ws:
                continue
            res = {}
            for w in ws:
                ok = V.folder_of(w) in pw
                why = ""
                if not ok:
                    try:
                        e = json.loads(fail.get(w) or "[]")
                        why = "；".join(e) if isinstance(e, list) else str(e)
                    except Exception:
                        why = str(fail.get(w) or "")
                    why = why or ("没做到（任务%s）" % t["status"].replace("已", "") if t["status"] != "已完成" else "没做成")
                res[w] = {"ok": ok, "detail": why[:200]}
            tt = t["finished"] or t["started"] or ""
            try:
                ts = time.mktime(time.strptime(tt[:19], "%Y-%m-%d %H:%M:%S"))
            except Exception:
                ts = 0.0
            h.append({"id": t["id"], "kind": kind, "t": ts, "t0": ts, "tid": t["id"], "src": "任务 #%d" % t["id"], "words": ws, "res": res})
    return sorted(h, key=lambda x: x.get("t") or 0, reverse=True)


def q_hist():
    """v1.20.1：出题的记录——一个任务一行：任务名、哪些词、出好几个、没过几个（照每一组的结果；没轮到的写“没做到”），
    开始时跳过的（已经有题目）。和「画面」的生成历史一样，新的在前。"""
    def fam(kind, p):
        return kind in ("chuti", "redo") or (kind == "words" and "chuti" in (p.get("steps") or ["chuti", "pics"]))
    man = {r["word"]: r["errors"] for r in q("SELECT word, errors FROM manual")}
    try:
        _, rows = read_index()
        hasq = {}
        for r in rows:
            hasq[r[2]] = hasq.get(r[2], True) and r[4] != "缺"
    except Exception:
        hasq = {}
    groups = {}
    for g in q("SELECT task_id, words, saved, fixed, failed, ts FROM groups ORDER BY id"):
        groups.setdefault(g["task_id"], []).append(g)
    L = lambda s: json.loads(s or "[]") if isinstance(s, str) else (s or [])
    out = []
    for t in q("SELECT id, kind, title, params, status, created, started, finished, error FROM tasks ORDER BY id DESC LIMIT 300"):
        try:
            p = json.loads(t["params"] or "{}")
        except Exception:
            p = {}
        if not fam(t["kind"], p):
            continue
        words, res = [], {}
        for g in groups.get(t["id"], []):
            ok = set(L(g["saved"])) | set(L(g["fixed"]))
            bad = set(L(g["failed"]))
            for w in L(g["words"]):
                if w not in words:
                    words.append(w)
                if w in ok:
                    res[w] = {"ok": True, "detail": "出好了" + ("（改过再存）" if w in set(L(g["fixed"])) else "")}
                elif w in bad or w in man:
                    try:
                        e = L(man.get(w)) if w in man else []
                    except Exception:
                        e = [str(man.get(w))]
                    res[w] = {"ok": False, "detail": ("没过：" + "；".join(map(str, e)))[:200] if e else "没过检查（在「没过的词」里）"}
        for w in p.get("words") or []:                 # 点了名、没轮到的词
            if w not in words and w not in ((p.get("skipped") or {}).get("q") or []):
                words.append(w)
                res[w] = {"ok": bool(hasq.get(w)), "detail": "出好了" if hasq.get(w) else
                          ("没做到（任务%s）" % t["status"].replace("已", "") if t["status"] in ("已取消", "失败", "已暂停") else "还没做到")}
        tt = t["finished"] or t["started"] or t["created"] or ""
        try:
            ts = time.mktime(time.strptime(tt[:19], "%Y-%m-%d %H:%M:%S"))
        except Exception:
            ts = 0.0
        out.append({"tid": t["id"], "title": t["title"] or "出题", "status": t["status"], "t": ts, "started": t["started"] or "",
                    "finished": t["finished"] or "", "words": words, "res": res, "error": (t["error"] or "")[:300],
                    "skipped": list((p.get("skipped") or {}).get("q") or [])[:300]})
    return out


def group_size():
    """出题一组几个词：手动接力时一组至少一份那么大（一份 300 个就一组 300 个，不再切成 25 个一份）。"""
    cfg = load_cfg()
    gs = int(cfg.get("groupSize") or 25)
    return max(gs, int(cfg.get("relayChunk") or 25)) if cfg.get("provider") == "relay" else gs


RELAY_ACT = {"rid": 0, "act": ""}
RELAY_QLEFT = [0]        # 这一批后面还排着几个词（调用方出提示词前填上；改“每批几个词”时用）


def relay_act(rid, act):
    """黄框里点的：newchat（剩下的另开对话继续）/ skiprest（剩下的先跳过）。"""
    with _RELAY_LOCK:
        if RELAY.get("id") != int(rid or 0) or not RELAY.get("multi") or RELAY.get("status") not in ("等你操作", "交回了"):
            return False, "这一批已经不在等了，刷新一下"
        RELAY_ACT.update(rid=int(rid), act=act)
    return True, {"newchat": "好：剩下的词马上出一份新的提示词（会自动复制），开一个新对话粘贴",
                  "skiprest": "剩下的这些词先跳过了"}.get(act, "")


def relay_poll_now():
    """黄框里点「立即查看仓库」：马上看一次中转仓库，看完从这一刻起重新数 15 秒。"""
    with _RELAY_LOCK:
        if RELAY.get("status") not in ("等你操作", "交回了") or not RELAY.get("inbox"):
            return False, "现在没有在等中转仓库"
        RELAY["pollNow"] = time.time()
    return True, "正在看中转仓库…"


# 黄框里能直接改的：一批几个词、每写完几个传一次（kind：q 出题 / pic 画面 / fix 补画面）
SIZE_KEYS = {"q": ("relayChunk", "relayRound"), "pic": ("relayPicChunk", "relayPicRound"), "fix": ("relayFixChunk", "relayFixRound")}
KIND_SIZE = {"出题": "q", "做画面": "pic", "补画面": "fix"}


def relay_size(kind, cfg=None):
    """这一种活现在的设置：(一批几个词, 每写完几个传一次)。"""
    cfg = cfg or load_cfg()
    a, b = SIZE_KEYS.get(kind, SIZE_KEYS["pic"])
    return max(1, int(cfg.get(a) or DEFAULT_CFG[a])), max(1, int(cfg.get(b) or DEFAULT_CFG[b]))


def relay_url_set(url):
    url = str(url or "").strip()
    if not re.match(r"^https?://[^\s]+$", url):
        return False, "要填 http:// 或 https:// 开头的网址"
    save_cfg({"relayUrl": url})
    return True, "存好了：点「手动发送」打开 " + url


def relay_size_set(kind, chunk, rnd):
    if kind not in SIZE_KEYS:
        return False, "认不出是哪一步"
    try:
        chunk, rnd = int(chunk), int(rnd)
    except Exception:
        return False, "要填数字"
    if not (1 <= chunk <= 1000 and 1 <= rnd <= 1000):
        return False, "要填 1 到 1000 之间的数"
    rnd = min(rnd, chunk)
    a, b = SIZE_KEYS[kind]
    save_cfg({a: chunk, b: rnd})
    tid = (RUNNER.task or {}).get("id")
    log("手动接力设置改了（%s）：一批 %d 个词，每写完 %d 个传一次" % ({"q": "出题", "pic": "画面", "fix": "补画面"}[kind], chunk, rnd), tid)
    # v1.11.3：正在等的这一批马上按新的来——这一批还没做的词 + 后面排着的，按新的数重新出一份提示词
    with _RELAY_LOCK:
        live = (RELAY.get("multi") and RELAY.get("status") in ("等你操作", "交回了") and KIND_SIZE.get(RELAY.get("kind")) == kind
                and RELAY.get("tid") == tid and RELAY.get("pending"))
        if live:
            pend = len(RELAY["pending"])
            n2 = min(chunk, pend + int(RELAY.get("qLeft") or 0))
            if n2 == pend and min(rnd, n2) == int(RELAY.get("round") or 0):
                live = False
        if live:
            RELAY_ACT.update(rid=RELAY["id"], act="resize")
    if live:
        return True, "已保存：这一批马上按新的来（%d 个词，每写完 %d 个传一次），提示词重新出了、会自动复制，到网页 AI 开个新对话粘贴" % (n2, min(rnd, n2))
    return True, "已保存：一批 %d 个词，每写完 %d 个传一次" % (chunk, rnd)


# ═══════════ v1.12.0：检查结果送回给网页 AI——它在同一个对话里马上改，不用你回来补 ═══════════
# 软件每检查完一个词，把结果写进中转仓库的 outbox/<这一份的名字>.json；网页 AI 的上传脚本传完就等这个文件，
# 打印【起草检查结果】：✓ 的不用管，✗ 的照“还要补”改好再传一次（每个词最多 relayTries 次），改好了再接着写。
OUTBOX = "outbox"
FAIL_LOG = DATA / "pic_fail_log.json"
RELAY_SAVE = DATA / "relay_batch.json"     # v1.15.0：这一份叫什么、是哪些词、检查结果——软件重开了接着用同一份
RELAY_RAW = []                             # 最近收到的网页 AI 原文（「看网页 AI 原文」用）
SESSION = os.urandom(4).hex()              # 这一次开着的软件（重开以后就不一样了）
_BASE_RE = re.compile(r"^(.+?)-\d{6}(?:-end)?\.(?:xlsx|txt)$|^(.+?)-(?:report|stop)\.json$")
KIND_CODE = {"做画面": "pic", "补画面": "fix", "出题": "q"}
CODE_KIND = {v: k for k, v in KIND_CODE.items()}


def batch_name(kind, words):
    """v1.16.0：这一份的名字一看就懂：哪一步-日期-时间-第一个词，比如 fix-20261125-131906-saturday（以前是 20261125-131906-be04d5）。"""
    w = re.sub(r"[^a-z0-9]+", "-", str((words or [""])[0]).lower()).strip("-")[:16] or "x"
    return "%s-%s-%s" % (KIND_CODE.get(kind, "ai"), time.strftime("%Y%m%d-%H%M%S"), w)


def base_of(fname):
    """中转仓库里一个文件是哪一份的（名字去掉后面的上传时间、-end、扩展名）。新旧两种名字都认。"""
    m = _BASE_RE.match(str(fname).rsplit("/", 1)[-1])
    return (m.group(1) or m.group(2)) if m else ""


def batch_label(ipath):
    """给人看的名字：fix-20261125-131906-saturday → 11月25日 13:19 · saturday；旧名字 → 11月25日 13:19。"""
    b = str(ipath).rsplit("/", 1)[-1]
    m = re.match(r"^(?:([a-z]+)-)?(\d{4})(\d{2})(\d{2})-(\d{2})(\d{2})\d{2}(?:-(.+))?$", b)
    if not m:
        return b
    k, _, mo, d, hh, mm, rest = m.groups()
    word = rest if k and rest and rest != "x" else ""
    return "%d月%d日 %s:%s%s" % (int(mo), int(d), hh, mm, (" · " + word) if word else "")


def _relay_load():
    try:
        return json.loads(RELAY_SAVE.read_text(encoding="utf-8")) if RELAY_SAVE.exists() else {}
    except Exception:
        return {}


def _relay_store(d):
    try:
        RELAY_SAVE.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def relay_raw_add(f, text):
    RELAY_RAW.append({"t": time.time(), "f": str(f).rsplit("/", 1)[-1], "text": str(text)[:400000]})
    del RELAY_RAW[:-12]


def relay_tries(cfg=None):
    return max(1, min(9, int((cfg or load_cfg()).get("relayTries") or 3)))


def relay_verdict(w, ok, todo=""):
    """一个词检查完（第一次，或者网页 AI 改过再交的）：记下结果；没过、还能改的放进“在改”。返回 True＝改够次数了还没过（先放着）。"""
    mx = relay_tries()
    with _RELAY_LOCK:
        V = RELAY.setdefault("verdict", {})
        v = dict(V.get(w) or {"try": 0})
        v["try"] = int(v.get("try") or 0) + 1
        v.update(ok=bool(ok), todo="" if ok else mask(str(todo or ""))[:1500], t=time.time())
        V[w] = v
        fx = RELAY.setdefault("fixing", [])
        loop = bool(RELAY.get("loop"))
        if ok or not loop or v["try"] >= mx:
            if w in fx:
                fx.remove(w)
        elif w not in fx:
            fx.append(w)
        RELAY["vdirty"] = True
        gave = (not ok) and loop and v["try"] >= mx
    if not ok and todo:
        _fail_log(w, todo)
    return gave


def _fail_log(w, todo):
    """没过的原因记一笔（最近 400 条）：出提示词时统计“最容易没过的地方”。"""
    try:
        L = json.loads(FAIL_LOG.read_text(encoding="utf-8")) if FAIL_LOG.exists() else []
    except Exception:
        L = []
    L.append({"t": time.time(), "w": w, "todo": str(todo)[:600]})
    try:
        FAIL_LOG.write_text(json.dumps(L[-400:], ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def outbox_push(ipath, done=False):
    """把这一份到现在的检查结果写进中转仓库 outbox/<名字>.json（网页 AI 的上传脚本读它）。出错不要紧，下次再写。"""
    if not ipath:
        return
    ib = inbox_cfg()
    base0 = ipath.rsplit("/", 1)[-1]
    with _RELAY_LOCK:
        names = [base0] + [a for a in (RELAY.get("aliases") or []) if a != base0]
        V = {k: dict(v) for k, v in (RELAY.get("verdict") or {}).items()}
        RELAY["vdirty"] = False
    sv = _relay_load()
    if sv.get("ipath") == ipath:
        sv["verdict"] = V
        _relay_store(sv)
    for base in names:                       # v1.15.0：网页 AI 用的是哪个名字（软件重开以前的也算），就写在哪个名字下
        _outbox_put(ib, base, {"name": base, "max": relay_tries(), "words": V, "done": bool(done), "t": time.time()})


def _outbox_put(ib, base, body):
    path = "%s/%s.json" % (OUTBOX, base)
    shas = RELAY.setdefault("outboxShas", {})
    sha = shas.get(base, "")
    data = {"message": "检查结果 " + base, "branch": ib.get("branch") or "main",
            "content": base64.b64encode(json.dumps(body, ensure_ascii=False).encode("utf-8")).decode()}
    url = "/repos/%s/contents/%s" % (ib["repo"], urllib.parse.quote(path))
    try:
        for k in range(2):
            if sha:
                data["sha"] = sha
            st, d = _gh("PUT", url, ib["token"], data)
            if st in (200, 201) and isinstance(d, dict):
                shas[base] = ((d.get("content") or {}).get("sha")) or ""
                return
            if st in (409, 422) and k == 0:          # sha 对不上：先读一下现在的再写
                st2, d2 = _gh("GET", url + "?ref=" + urllib.parse.quote(ib.get("branch") or "main"), ib["token"])
                sha = (d2 or {}).get("sha", "") if st2 == 200 and isinstance(d2, dict) else ""
                continue
            log("检查结果没写进中转仓库（%s）：%s" % (st, str((d or {}).get("message", ""))[:120] if isinstance(d, dict) else ""))
            return
    except Exception as e:
        log("检查结果没写进中转仓库：%s" % mask(str(e))[:120])


def report_grace(ipath, tid, secs=240):
    """一份做完了：网页 AI 最后的汇报一般晚几秒才传上来——再等一会儿，收到就记进步骤记录、删掉。"""
    ib = inbox_cfg()
    br = urllib.parse.quote(ib.get("branch") or "main")
    end = time.time() + secs
    while time.time() < end:
        time.sleep(10)
        for suf in ("-report.json", "-stop.json"):
            try:
                st, d = _gh("GET", "/repos/%s/contents/%s?ref=%s" % (ib["repo"], urllib.parse.quote(ipath + suf), br), ib["token"])
                if st == 200 and isinstance(d, dict):
                    info = json.loads(base64.b64decode(d.get("content") or "").decode("utf-8"))
                    info.setdefault("state", "stop" if suf == "-stop.json" else "")
                    relay_ai_report(info, tid=tid)
                    inbox_delete(ipath + suf, d.get("sha"))
                    return
            except Exception:
                pass


def outbox_clean():
    """中转仓库 outbox/ 里两个小时以前的检查结果删掉（文件名开头就是时间）。"""
    try:
        ib = inbox_cfg()
        br = urllib.parse.quote(ib.get("branch") or "main")
        st, d = _gh("GET", "/repos/%s/contents/%s?ref=%s" % (ib["repo"], OUTBOX, br), ib["token"])
        if st != 200 or not isinstance(d, list):
            d = []
        cut = time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time() - 7200))
        st3, d3 = _gh("GET", "/repos/%s/contents/%s?ref=%s" % (ib["repo"], ib.get("dir") or "inbox", br), ib["token"])
        if st3 == 200 and isinstance(d3, list):        # inbox/ 里两个小时以前的汇报（没人读的）也清掉
            d = d + [x for x in d3 if str(x.get("name", "")).endswith(("-report.json", "-stop.json"))]
        for x in d:
            n = x.get("name") or ""
            mt = re.search(r"(\d{8}-\d{6})", n)
            if mt and mt.group(1) < cut:
                _gh("DELETE", "/repos/%s/contents/%s" % (ib["repo"], urllib.parse.quote(x.get("path") or "")), ib["token"],
                    {"message": "检查结果：清掉旧的 " + n, "sha": x.get("sha"), "branch": ib.get("branch") or "main"})
    except Exception:
        pass


REPORT_TAG = re.compile(r"【单词工作台·汇报】\s*状态[:：]\s*(写完了|停下了|等检查结果)")


def relay_ai_report(info, pasted=False, tid=None):
    """v1.14.0：网页 AI 这一轮回复结束时的汇报（脚本传上来的，或者你粘贴的）：记下它说的进度，黄框照这个判断该不该“继续”。
    tid 给了＝这一份已经结束了（它最后的汇报晚到几秒）：只记进那个任务的步骤记录，不动现在这一份。"""
    state = str(info.get("state") or "")
    text = mask(str(info.get("text") or ""))[:3000]
    why = mask(str(info.get("why") or ""))[:300]
    if tid is not None:
        log("网页 AI 汇报（%s）：%s" % ({"done": "写完了", "stop": "停下了", "wait": "等检查结果"}.get(state, state or "说了一句"),
                                    (text.split("\n", 1)[-1] if text.startswith("【单词工作台·汇报】") else text)[:600] or why), tid)
        F = RELAY.get("final") or {}
        if F.get("tid") == tid:                  # v1.18.0：“本轮任务完成”那张卡片写上：网页 AI 也汇报了
            F["aiSaid"] = {"t": time.time(), "state": state}
        return
    with _RELAY_LOCK:
        RELAY["aiReport"] = {"t": time.time(), "state": state, "text": text, "why": why, "pasted": pasted,
                             "done": list(info.get("done") or [])[:500], "left": list(info.get("left") or [])[:500]}
        if state == "stop":
            RELAY["aiStop"] = {"t": time.time(), "done": list(info.get("done") or [])[:500],
                               "left": list(info.get("left") or [])[:500], "why": why}
        elif state == "done":
            RELAY["aiDone"] = True
        tid = RELAY.get("tid")
    log("网页 AI 汇报（%s%s）：%s" % ({"done": "写完了", "stop": "停下了", "wait": "等检查结果"}.get(state, state or "说了一句"),
                                  "，你粘贴的" if pasted else "", (text.split("\n", 1)[-1] if text.startswith("【单词工作台·汇报】") else text)[:600] or why), tid)


def relay_cont_msg():
    """「在这个对话里接着写」：一句短话，粘贴到同一个对话里（不用再贴整份提示词）。"""
    with _RELAY_LOCK:
        pend = list(RELAY.get("pending") or [])
        rnd = int(RELAY.get("round") or 1)
        fx = [(w, (RELAY.get("verdict") or {}).get(w, {}).get("todo", "")) for w in (RELAY.get("fixing") or [])]
    waiting = (RELAY.get("aiReport") or {}).get("state") == "wait"
    if not pend and not fx:
        return ("看结果：单词工作台的检查结果已经写好了。运行 python upload.py 看结果（或者把 MODE 改成 \"看结果\" 运行），照它说的做："
                "没过的照“还要补”改好再传，全部过了再把【单词工作台·汇报】那几行回给我。") if waiting else ""
    fix = ("先改这 %d 个没过起草检查的词（照“还要补”的每一条改，把这个词完整重写一遍，插图只写新画的），改好一个传一个：\n%s\n"
           % (len(fx), "\n".join("- %s：%s" % (w, t[:400]) for w, t in fx))) if fx else ""
    if waiting:
        fix = "先运行一次 python upload.py 看结果（单词工作台的检查结果已经写好了），照它说的改。\n" + fix
    if not pend:
        return fix + "改完运行同一段上传脚本（MODE 保持 \"上传\"），它会告诉你检查结果。"
    return fix + ("继续：接着写这一批还没写的 %d 个词，按顺序：%s。\n"
            "规矩和上面一样：每写完 %d 个就写进 reply.txt、运行同一段上传脚本（MODE 保持 \"上传\"）；中间不用在聊天里汇报，一直写到全部传完，"
            "脚本打印【最后汇报】时再汇报一次。这次回复写不下了，就先传好已经写的，运行 python upload.py 汇报 停下。"
            % (len(pend), "、".join(pend), rnd))



# ═══════════════════════ v1.22.0：自动继续（浏览器小助手） ═══════════════════════
# 网页 AI 那一页里装的用户脚本（app/web/autocont.tpl.js，Tampermonkey 装）每几秒来问一次 /api/relay/auto：
# 开没开、这一份还要不要网页 AI 接着写、发什么、这个对话里认哪几个文件名；它点了「Continue」、发了「继续」也来说一声，写进步骤记录。
HELPER = {"seen": 0.0, "host": "", "rid": 0, "clicks": 0, "sends": 0}
AUTO_MAX_SENDS = 15          # 一份最多自动发几次「继续」（防止来回空转）


def _bare(n):
    n = n if isinstance(n, str) else (n or {}).get("inbox", "") if isinstance(n, dict) else ""
    return n.rsplit("/", 1)[-1].rsplit(".", 1)[0] if n else ""


def relay_auto(qs):
    on = load_cfg().get("autoCont", True) is not False
    with _RELAY_LOCK:
        rid = RELAY.get("id", 0)
        if HELPER["rid"] != rid:
            HELPER.update(rid=rid, clicks=0, sends=0)
        HELPER.update(seen=time.time(), host=str(qs.get("host") or HELPER["host"])[:80])
        active = RELAY.get("status") == "等你操作" and bool(RELAY.get("inbox"))
        names = []
        if active:
            names = [_bare(RELAY["inbox"])] + [_bare(a) for a in (RELAY.get("aliases") or [])] + [_bare(h) for h in RELAY_HIST]
        key = "%s-%d-%d-%s-%d" % (rid, len(RELAY.get("pending") or []), len(RELAY.get("fixing") or []),
                                  (RELAY.get("aiReport") or {}).get("state", ""), len(RELAY.get("gotFiles") or []))
        checking, tid = RELAY.get("phase") == "checking", RELAY.get("tid")
    ev = qs.get("ev")
    if ev == "continue":
        HELPER["clicks"] += 1
        log("网页 AI 的回复中断了：软件自动点了「Continue」（这一份第 %d 次）" % HELPER["clicks"], tid)
        return {"ok": True}
    if ev == "send":
        HELPER["sends"] += 1
        log("网页 AI 停下了、这一份还没写完：软件自动发了「继续」那段话（这一份第 %d 次）" % HELPER["sends"], tid)
        return {"ok": True}
    cont = relay_cont_msg() if (on and active and not checking) else ""
    need = bool(cont) and HELPER["sends"] < AUTO_MAX_SENDS
    return {"on": on, "active": active, "need": need, "cont": cont if need else "", "key": key,
            "names": [n for n in dict.fromkeys(names) if len(n) >= 6], "idleSec": 20, "coolSec": 60, "maxClicks": 40}


def helper_info():
    """黄框里那一行：小助手来没来过、这一份点了几次、发了几次。"""
    h = dict(HELPER)
    return {"on": load_cfg().get("autoCont", True) is not False, "ago": (time.time() - h["seen"]) if h["seen"] else None,
            "clicks": h["clicks"] if h["rid"] == RELAY.get("id") else 0, "sends": h["sends"] if h["rid"] == RELAY.get("id") else 0,
            "host": h["host"]}


def relay_word(w, ok, detail=""):
    """一份好几个词时，一个词做完（做好了 / 没做成）：从“还剩”里拿掉，记进做完的列表（黄框、汇报用）。"""
    with _RELAY_LOCK:
        if w in (RELAY.get("pending") or []):
            RELAY["pending"].remove(w)
        if w not in (RELAY.get("doneIn") or []):
            RELAY.setdefault("doneIn", []).append(w)
        tid = RELAY.get("tid")
        RELAY["last"] = {"words": [w], "ok": bool(ok), "detail": mask(str(detail or ""))[:200], "t": time.time(),
                         "got": time.time(), "glen": 0, "multi": True}
        if RELAY.get("doneTid") != tid:
            RELAY["done"], RELAY["doneTid"] = [], tid
        D = RELAY.setdefault("done", [])
        D[:] = [x for x in D if x.get("words") != [w]]      # v1.12.0：改过再交的词，换掉上一次的结果（不算两次）
        D.append(dict(RELAY["last"]))
        del D[:-2000]
    _say("  %s %s%s" % (w, "✓ 做好了" if ok else "✗ 没做成", ("：" + str(detail)[:120]) if detail else ""))


def _inbox_parts(ipath, seen, pending, t0):
    """中转仓库里这一批传上来的文件：名字以这一批的名字开头的；名字对不上、但这一批开始以后传的、内容是这一批的词，也收。
    返回 [(原文, 路径, 是不是这一批最后一个)]，收下的都从中转仓库删掉。"""
    ib = inbox_cfg()
    br = urllib.parse.quote(ib["branch"] or "main")
    folder, base = ipath.rsplit("/", 1)
    st, d = _gh("GET", "/repos/%s/contents/%s?ref=%s" % (ib["repo"], urllib.parse.quote(folder), br), ib["token"])
    if st == 404:
        INBOX_LAST.update(files=[], ts=time.time())
        return []
    if st != 200:
        raise RuntimeError("看收件箱出错（%s）：%s" % (st, str((d or {}).get("message", ""))[:120]))
    files = [x.get("path") for x in d if x.get("path")] if isinstance(d, list) else []
    INBOX_LAST.update(files=sorted(f.rsplit("/", 1)[-1] for f in files), ts=time.time())
    names = (base,) + tuple(RELAY.get("aliases") or [])     # v1.15.0：网页 AI 认的名字（软件重开以前的也算）
    for f in [f for f in files if base_of(f) in names and (f.endswith("-stop.json") or f.endswith("-report.json"))]:
        files.remove(f)        # v1.11.4 停下了 / v1.14.0 这一轮回复结束时的汇报（写完了、停下了、等检查结果）
        try:
            st2, d2 = _gh("GET", "/repos/%s/contents/%s?ref=%s" % (ib["repo"], urllib.parse.quote(f), br), ib["token"])
            if st2 == 200 and isinstance(d2, dict):
                info = json.loads(base64.b64decode(d2.get("content") or "").decode("utf-8"))
                if f.endswith("-stop.json"):
                    info.setdefault("state", "stop")
                relay_ai_report(info)
                inbox_delete(f, d2.get("sha"))
        except Exception as e:
            log("读网页 AI 的汇报出错：%s" % str(e)[:120])
    mine = [f for f in files if base_of(f) in names and f not in seen]
    others = [f for f in files if f not in seen and f not in mine]
    if others:
        try:
            ups = inbox_uploads(20) or []
            INBOX_LAST["uploads"] = ups
        except Exception:
            ups = []
        fresh = {u["path"] for u in ups if u["ts"] >= t0 - 5}
        mine += [f for f in others if f in fresh]
    out = []
    for f in sorted(mine):
        got = inbox_fetch(f.rsplit(".", 1)[0])
        seen.add(f)
        if not got:
            continue
        text, sha, gpath = got
        ours = base_of(f) == base          # 名字是这一份的：短一点、写坏了也收下，交给检查去判（会记“没做成”和原因）
        if _looks_reply(text, pending) or (ours and END in text and any(
                re.search(r"[@＠]\s*" + re.escape(w) + r"(?![A-Za-z'’\-])", text) for w in pending)):
            inbox_delete(gpath, sha)
            ab = base_of(f)
            if not ours and ab and ab != base and ab not in (RELAY.get("aliases") or []):     # v1.15.0：网页 AI 用的是别的名字（软件重开以前的）
                RELAY.setdefault("aliases", []).append(ab)
                try:                     # 那个名字下面原来的检查结果接过来（第几次、过没过），网页 AI 那边接着数
                    st4, d4 = _gh("GET", "/repos/%s/contents/%s/%s.json?ref=%s" % (ib["repo"], OUTBOX, ab, br), ib["token"])
                    if st4 == 200 and isinstance(d4, dict):
                        oldv = (json.loads(base64.b64decode(d4.get("content") or "").decode("utf-8")) or {}).get("words") or {}
                        with _RELAY_LOCK:
                            V = RELAY.setdefault("verdict", {})
                            for w, v in oldv.items():
                                if int((v or {}).get("try") or 0) > int((V.get(w) or {}).get("try") or 0):
                                    V[w] = dict(v)
                        RELAY.setdefault("outboxShas", {})[ab] = d4.get("sha") or ""
                except Exception:
                    pass
                sv = _relay_load()
                if sv.get("ipath") == ipath:
                    sv["aliases"] = list(RELAY["aliases"])
                    _relay_store(sv)
                log("网页 AI 用的是以前那份提示词（%s）：收下了，检查结果也写回那个名字，它那边看得到" % batch_label(ab),
                    RELAY.get("tid"))
            nm = gpath.rsplit("/", 1)[-1]
            out.append((text, gpath, nm.rsplit(".", 1)[0].endswith("-end") or "【这一批最后一个】" in text))
        elif ours:
            RELAY["hint"] = "收到 %s，但里面没有这一批还没做的词（或者没有最后一行 %s）" % (gpath.rsplit("/", 1)[-1], END)
            inbox_delete(gpath, sha)
    return out


def relay_parts(prompt, words, kind, rnd):
    """手动接力 · 一份好几个词（v1.10.9）：提示词放进剪贴板；网页 AI 每写完 rnd 个词就上传一次（文件名都以这一份的名字开头），
    收到一个就 yield 出去处理，处理完的词由调用方用 relay_word() 记下。全部做完，或者你点了「剩下的另开对话继续」「剩下的先跳过」
    就结束，原因放在 RELAY["endReason"]：all / newchat / skiprest。剪贴板、手动粘贴交回的也一样一轮一轮收。"""
    import clip
    words = list(words)        # 自己留一份：调用方做完一个词会从它的列表里删，不能跟着变（v1.10.10：以前一批做完会出错停下）
    cfg = load_cfg()
    ibox = inbox_on(cfg)
    use_clip = clip.WIN and cfg.get("relayClipboard", True) and not ibox   # v1.18.0：网页 AI 自己上传时不看剪贴板（复制提示词会被当成回复）
    tid = (RUNNER.task or {}).get("id")
    ipath, resumed, sv = "", False, _relay_load()
    if ibox:
        ipath = "%s/%s" % (inbox_cfg(cfg)["dir"], batch_name(kind, words))
        if (sv.get("tid") == tid and sv.get("kind") == kind and sv.get("ipath") and set(words) <= set(sv.get("words") or [])
                and time.time() - float(sv.get("t0") or 0) < 2 * 86400):
            ipath = sv["ipath"]                     # v1.15.0：同一份：网页 AI 原来的对话接着传就行，检查结果也写回它认的名字
            resumed = sv.get("session") != SESSION  # 软件重开过（同一次开着里“开新对话”也用同一个名字，但不用提醒）
            sv["session"] = SESSION
            _relay_store(sv)
            sv["_same"] = True
        else:
            sv = {"tid": tid, "kind": kind, "ipath": ipath, "words": list(words), "t0": time.time(), "verdict": {}, "aliases": [],
                  "session": SESSION}
            _relay_store(sv)
        info = batch_info(words, kind)
        info["round"] = rnd
        prompt = prompt.rstrip() + "\n\n" + inbox_prompt(ipath, info)
    with _RELAY_LOCK:
        RELAY.update(id=RELAY["id"] + 1, status="等你操作", prompt=prompt, words=list(words), kind=kind, reply="", ts=time.time(),
                     copied=False, hint="", clip=use_clip, inbox=(ipath + ".xlsx") if ipath else "", phase="send", tid=tid,
                     polls=0, lastPoll=0.0, stage="", multi=True, pending=list(words), doneIn=[], parts=0, endReason="", round=rnd,
                     aiDone=False, pollNow=0.0, nextPoll=0.0, pollBy="", pollGot=0, qLeft=RELAY_QLEFT[0], aiStop=None, gotFiles=[],
                     verdict=dict(sv.get("verdict") or {}) if sv.get("_same") else {}, fixing=[], vdirty=False, outboxShas={},
                     loop=bool(ibox), tries=relay_tries(cfg), resumed=resumed, aliases=list(sv.get("aliases") or []) if sv.get("_same") else [],
                     turn=1, aiReport=None)
        rid = RELAY["id"]
        RELAY_ACT.update(rid=0, act="")
        RELAY_HIST.clear()
        RELAY_HIST.append({"id": rid, "kind": kind, "words": list(words), "tid": tid, "t0": time.time(),
                           "inbox": RELAY["inbox"], "got": 0.0, "glen": 0, "res": "", "detail": "", "t1": 0.0})
        t0 = time.time()
    after = ("网页 AI 每写完 %d 个词就自己传一次到中转仓库（文件名以 %s 开头），软件收到一轮做一轮" % (rnd, ipath.rsplit("/", 1)[-1])) if ibox \
        else "它写完一轮，点它回复下面的「复制」，软件收到一轮做一轮"
    if use_clip and clip.set_text(prompt):
        RELAY["copied"] = True
        log("提示词已经放进剪贴板（%s：一份 %d 个词，%s … %s）：到网页 AI 里粘贴、发送；%s" % (kind, len(words), words[0], words[-1], after), tid)
    else:
        log("要你操作：复制提示词到网页 AI 发送（%s：一份 %d 个词，%s … %s）；%s" % (kind, len(words), words[0], words[-1], after), tid)
    _say("━━━━ 手动接力：%s 一份 %d 个词（%s … %s），网页 AI 每写完 %d 个上传一次 ━━━━" % (kind, len(words), words[0], words[-1], rnd))
    if resumed:
        log("接着上次那一份（文件名以 %s 开头，还剩 %d 个词）：网页 AI 原来的对话接着写、接着传就行，不用重新粘贴；那个对话没了，再粘贴这份提示词"
            % (ipath.rsplit("/", 1)[-1], len(words)), tid)
    clip.beep()
    if ibox:
        threading.Thread(target=outbox_clean, daemon=True).start()
    last = clip.seq() if use_clip else 0
    poll = max(5, int(inbox_cfg(cfg).get("pollSec") or 15))
    next_ib, ib_err, seen = time.time() + poll, 0, set()
    RELAY["nextPoll"] = next_ib
    end = time.time() + 24 * 3600
    try:
        while time.time() < end:
            with _RELAY_LOCK:
                if not RELAY["pending"] and not RELAY.get("fixing"):     # 这一批都收到、都做完了（没过的也改好了，或者改够次数了）
                    RELAY["endReason"] = "all"
                    res = {x["words"][0]: x["ok"] for x in (RELAY.get("done") or []) if x.get("words")}
                    nok = len([w for w in words if res.get(w)])
                    RELAY["lastBatch"] = {"words": list(words), "ok": nok, "bad": len(words) - nok, "t": time.time(), "kind": kind}
                    _say("━━━━ 这一批 %d 个词已经生成完（%s … %s）：做好了 %d 个，没做成 %d 个 ━━━━" % (len(words), words[0], words[-1], nok, len(words) - nok))
                    log("这一批 %d 个词已经生成完：做好了 %d 个，没做成 %d 个" % (len(words), nok, len(words) - nok), tid)
                    return
                act = RELAY_ACT["act"] if RELAY_ACT["rid"] == rid else ""
            if act:
                RELAY["endReason"] = act
                return
            if RUNNER.stop_req:
                raise Stopped(RUNNER.stop_req)
            texts = []
            by_you = bool(RELAY.get("pollNow"))
            if ibox and (time.time() >= next_ib or by_you):
                RELAY["pollNow"] = 0.0
                perr = ""
                try:
                    texts += _inbox_parts(ipath, seen, list(RELAY["pending"]) + list(RELAY.get("fixing") or []), t0)
                    ib_err = 0
                except ExcelBad as e:
                    RELAY["hint"] = perr = str(e) + "：在网页里叫它把这一轮重新传一次，或者照常把全文写在聊天里、点「复制」"
                except Exception as e:
                    ib_err += 1
                    perr = "看中转仓库出错：%s" % mask(str(e))[:120]
                    if ib_err in (1, 20) or by_you:
                        log("看收件箱出错（%s），过一会儿再看" % mask(str(e))[:160], tid)
                next_ib = time.time() + poll           # 看完（不管是到点了还是你点的）从现在起重新数
                with _RELAY_LOCK:
                    RELAY["polls"] += 1
                    RELAY.update(lastPoll=time.time(), nextPoll=next_ib, pollBy="you" if by_you else "auto",
                                 pollGot=len(texts), pollErr=perr)
                if by_you:
                    fs = INBOX_LAST.get("files") or []
                    _say("你点了「立即查看仓库」：inbox/ 里现在 %s；%s" % (
                        ("、".join(fs[:6]) + ("…" if len(fs) > 6 else "")) if fs else "空的",
                        ("收下 %d 个文件，接着做" % len(texts)) if texts else (perr or "没有这一批的新文件")))
                if not texts and (RELAY["polls"] <= 4 or RELAY["polls"] % max(1, 60 // poll) == 0):
                    fs = INBOX_LAST.get("files") or []
                    _say("中转仓库 第 %d 次看：这一批 %d 个词，收到 %d 个文件，做完 %d 个，还剩 %d 个，还在生成（等了 %s）；inbox/ 里现在：%s" % (
                        RELAY["polls"], len(words), RELAY["parts"], len(RELAY["doneIn"]), len(RELAY["pending"]),
                        _dur(time.time() - t0), "、".join(fs[:6]) + ("…" if len(fs) > 6 else "") if fs else "空的"))
            with _RELAY_LOCK:
                if RELAY["id"] == rid and RELAY["status"] == "交回了":
                    texts.append((RELAY["reply"], "你粘贴的", "【这一批最后一个】" in RELAY["reply"]))
                    RELAY.update(status="等你操作", reply="")
            if use_clip:
                sq = clip.seq()
                if sq != last:
                    last = sq
                    t = clip.get_text()
                    if t and t.strip() != prompt.strip() and _looks_reply(t, list(RELAY["pending"])):
                        texts.append((t, "剪贴板", "【这一批最后一个】" in t))
            if texts:
                RELAY["aiStop"] = None          # 又传上来了：它接着写了
                RELAY["aiDone"] = False         # v1.15.0：“说写完了”以后又传了，就不算写完；这一回带 -end 再算
                rep0 = RELAY.get("aiReport") or {}
                if rep0.get("state") in ("stop", "wait") and rep0.get("t", 0) > max([0] + [g.get("t", 0) for g in RELAY.get("gotFiles") or []]):
                    RELAY["turn"] = int(RELAY.get("turn") or 1) + 1
                    log("网页 AI 接着写了（第 %d 轮对话）" % RELAY["turn"], tid)
            for t, src, lastp in texts:
                if lastp:
                    RELAY["aiDone"] = True
                with _RELAY_LOCK:
                    RELAY["parts"] += 1
                    k = RELAY["parts"]
                    RELAY.update(phase="checking", stage="收到第 %d 轮，在看、存…" % k)
                    RELAY.setdefault("gotFiles", []).append({"t": time.time(), "f": src.rsplit("/", 1)[-1], "len": len(t)})   # v1.11.6：第 ③ 步的动态
                    if RELAY_HIST and not RELAY_HIST[-1]["got"]:
                        RELAY_HIST[-1].update(got=time.time(), glen=len(t))
                relay_raw_add(src, t)
                log("网页 AI 交回了第 %d 轮（%s，%d 字），接着做" % (k, src.rsplit("/", 1)[-1], len(t)), tid)
                AI_LIVE["reply"] = t
                yield t
                if ibox and RELAY.get("vdirty"):         # v1.12.0：检查结果马上送回给网页 AI
                    outbox_push(ipath)
                with _RELAY_LOCK:
                    RELAY["phase"] = "send" if (RELAY["pending"] or RELAY.get("fixing")) else "ok"
                    RELAY["stage"] = ""
                    miss = list(RELAY["pending"]) if RELAY.get("aiDone") else []
                if miss:                         # 网页 AI 说这一批写完了，可还有词没收到
                    RELAY["hint"] = "网页 AI 说这一批写完了，但还有 %d 个没收到：%s——点黄框里的「继续」" % (len(miss), "、".join(miss[:12]))
                    _say("网页 AI 说这一批写完了，但还有 %d 个没收到：%s" % (len(miss), "、".join(miss[:12])))
            time.sleep(1)
        raise Fatal("等了 24 小时，先停下")
    finally:
        fin = RELAY.get("endReason") in ("all", "skiprest")
        if ibox and RELAY["id"] == rid and RELAY.get("verdict") and fin:    # v1.12.0：告诉网页 AI 这一份结束了（脚本别再等）
            try:
                outbox_push(ipath, done=True)
            except Exception:
                pass
        if ibox and RELAY["id"] == rid and fin and _relay_load().get("ipath") == ipath:
            _relay_store({})
        if ibox and RELAY["id"] == rid and RELAY.get("endReason") in ("all", "newchat", "resize", "skiprest"):
            threading.Thread(target=report_grace, args=(ipath, tid), daemon=True).start()
        with _RELAY_LOCK:
            if RELAY["id"] == rid:
                RELAY["status"] = ""


def relay_stage(text):
    """检查进行到哪儿了（黄框第 4 步下面那行）。"""
    RELAY["stage"] = str(text)[:200]


def relay_result(ok, detail=""):
    """这一轮交回的回复检查完了：过了还是没过（黄框第 4 步打勾或者打叉，记进这一批的经过）。"""
    with _RELAY_LOCK:
        if not RELAY_HIST or RELAY.get("phase") != "checking":
            return
        RELAY_HIST[-1].update(res="ok" if ok else "fail", detail=mask(str(detail))[:400], t1=time.time())
        RELAY["phase"], RELAY["stage"] = ("ok" if ok else "fail"), ""
        h = RELAY_HIST[-1]
        RELAY["last"] = {"words": list(h["words"]), "ok": bool(ok), "detail": mask(str(detail))[:200], "t": time.time(),
                         "got": h.get("got", 0.0), "glen": h.get("glen", 0), "t0": h.get("t0", 0.0)}
        if RELAY.get("doneTid") != h.get("tid"):       # 这个任务做完的词（一个一个列着，能点开看）
            RELAY["done"], RELAY["doneTid"] = [], h.get("tid")
        RELAY.setdefault("done", []).append(dict(RELAY["last"]))
        del RELAY["done"][:-200]
        n = len(RELAY_HIST)
        _hist_save()
    _say("手动接力 第 %d 轮：%s%s" % (n, "✓ 检查过了" if ok else "✗ 没过", ("：" + str(detail)[:160]) if detail else ""))
_RELAY_LOCK = threading.Lock()


# ─────── 手动接力 · 收件箱：网页 AI 自己把回复传到 GitHub ───────
INBOX_SCRIPT = r"""import base64, io, json, os, re, urllib.request, urllib.error, zipfile
from xml.sax.saxutils import escape
TOKEN = "__TOKEN__"
REPO = "__REPO__"
BRANCH = "__BRANCH__"
NAME = "__NAME__"          # 收件箱里的文件名（不带扩展名）
WORDS = __WORDS__          # 这一份是哪些词
REPORT = __REPORT__        # 上传好以后在聊天里回的汇报
PARTS = __PARTS__          # 一份好几个词、写完一轮传一轮
ROUND = __ROUND__          # 每一轮几个词
LASTONE = __LASTONE__      # 这一批是不是这次的最后一批
PARTIAL = __PARTIAL__      # 写不下了、要停下时的汇报
MODE = "上传"              # 对话太长写不下、要停下的时候：把这里改成 "汇报" 再运行一次（只打印汇报，不上传）；"看结果"：只看检查结果
import sys as _s
if any(a in ("汇报", "report") for a in _s.argv[1:]):
    MODE = "汇报"
if any(a in ("看结果", "check") for a in _s.argv[1:]):
    MODE = "看结果"
MEM = "." + NAME.rsplit("/", 1)[-1] + ".done.json"   # 这一批已经传了哪些词（记在你这边）
_H = {"Authorization": "Bearer " + TOKEN, "Accept": "application/vnd.github+json", "User-Agent": "wordsvideo-relay"}
_OB = "https://api.github.com/repos/%s/contents/outbox/%s.json?ref=%s" % (REPO, NAME.rsplit("/", 1)[-1], BRANCH)


def _sent():
    try:
        return json.load(open(MEM, encoding="utf-8"))
    except Exception:
        return {"k": 0, "w": []}


def _report(state, why="", text=""):   # 这一轮回复结束时告诉单词工作台：写完了 / 停下了 / 等检查结果（软件按这个判断进度）
    s1 = _sent()
    left = [w for w in WORDS if w not in s1["w"]]
    tag = "【单词工作台·汇报】状态：%s｜已传 %d/%d 个%s%s" % (
        {"done": "写完了", "stop": "停下了", "wait": "等检查结果"}.get(state, state), len(s1["w"]), len(WORDS),
        "｜还剩 %d 个" % len(left) if left else "", ("｜" + why if state == "done" else "｜原因：" + why) if why else "")
    print(tag)
    try:
        u = "https://api.github.com/repos/%s/contents/%s-report.json" % (REPO, NAME)
        b = {"message": "接力：汇报 " + state, "branch": BRANCH, "content": base64.b64encode(json.dumps(
            {"state": state, "done": s1["w"], "left": left, "why": why, "text": (tag + "\n" + text).strip()[:3000]},
            ensure_ascii=False).encode()).decode()}
        try:
            with urllib.request.urlopen(urllib.request.Request(u + "?ref=" + BRANCH, headers=_H), timeout=60) as r:
                b["sha"] = json.load(r)["sha"]
        except urllib.error.HTTPError:
            pass
        urllib.request.urlopen(urllib.request.Request(u, data=json.dumps(b).encode(), headers=_H, method="PUT"), timeout=60)
        print("（这几行也告诉单词工作台了）")
    except Exception as e:
        print("（没告诉上单词工作台：%s，不要紧）" % str(e)[:120])


def _outbox():             # 单词工作台写回来的检查结果（每个词：过了没有、第几次、还要补什么）
    try:
        with urllib.request.urlopen(urllib.request.Request(_OB, headers=_H), timeout=30) as r:
            return json.loads(base64.b64decode(json.load(r)["content"]).decode("utf-8"))
    except Exception:
        return None


def _need(V, mx, w, n):    # 这个词传上去的最新一次，还没有检查结果
    v = (V or {}).get(w) or {}
    k = int(v.get("try") or 0)
    if v.get("ok") or k >= mx:
        return False
    return k < n.get(w, 0)


def _wait(words, n, limit=150):
    import time as _tm
    t0, said, ob = _tm.time(), 0, None
    print("等单词工作台检查（在老师的电脑上用视频技能起草检查，一般半分钟到两分钟）…")
    while True:
        ob = _outbox() or ob
        V, mx = (ob or {}).get("words") or {}, int((ob or {}).get("max") or 3)
        left = [w for w in words if _need(V, mx, w, n)]
        if not left or (ob or {}).get("done") or _tm.time() - t0 > limit:
            return ob or {}, left
        if _tm.time() - t0 > said + 30:
            said += 30
            print("  还在等：%s（已经 %d 秒）" % ("、".join(left[:8]), _tm.time() - t0))
        _tm.sleep(6)


def _next(s0, n):          # 传完（或者“看结果”）：打印检查结果，告诉你接下来做什么
    ob, slow = _wait([w for w in WORDS if n.get(w)], n)
    V, mx = ob.get("words") or {}, int(ob.get("max") or 3)
    seen = s0.setdefault("seen", {})
    new = [w for w in WORDS if int((V.get(w) or {}).get("try") or 0) > int(seen.get(w) or 0)]
    out = []
    for w in new:
        v = V[w]
        k = int(v.get("try") or 0)
        seen[w] = k
        if v.get("ok"):
            out.append("✓ %s：都齐了%s" % (w, "（改了 %d 次）" % (k - 1) if k > 1 else ""))
        elif k >= mx:
            out.append("✗ %s：改了 %d 次还没过，先放着（单词工作台记下了，以后一起补；不用再改）" % (w, k))
        else:
            out.append("✗ %s（第 %d 次没过，还能改 %d 次）：%s" % (w, k, mx - k, v.get("todo") or "照规矩每一条再对一遍"))
    json.dump(s0, open(MEM, "w", encoding="utf-8"), ensure_ascii=False)
    if out:
        print()
        print("【起草检查结果】（单词工作台检查的）")
        print("\n".join(out))
    fixes = [w for w in WORDS if V.get(w) and not V[w].get("ok") and int(V[w].get("try") or 0) < mx
             and n.get(w, 0) <= int(V[w].get("try") or 0)]
    left = [w for w in WORDS if w not in s0["w"]]
    if slow and not ob.get("done"):
        print("（%s 还没检查完：先接着做；下次上传完会一起告诉你结果）" % "、".join(slow[:8]))
    if fixes:
        print()
        print("→ 先改上面 ✗ 的 %d 个：%s。照“还要补”的每一条改，把这个词的 @单词 那一段完整重写一遍（JSON 写全；插图只写新画的、要重画的），"
              "写进 reply.txt，运行同一段脚本传上去（几个词可以写在一起传）。改好了再接着写%s。不用在聊天里汇报。"
              % (len(fixes), "、".join(fixes), ("下一个：" + "、".join(left[:ROUND])) if left else "（这一批别的词都传完了）"))
        return
    if left:
        print("不用在聊天里汇报，直接接着写下一个：%s" % "、".join(left[:ROUND]))
        return
    if slow and not ob.get("done"):
        print("这一批都传完了，还有 %d 个在等检查结果：过一两分钟运行一次 python upload.py 看结果（或者把 MODE 改成 \"看结果\" 运行），照它说的做。" % len(slow))
        print("要是这一轮回复只能先停在这里：把下面几行原样回在聊天里")
        _report("wait", "", "还有 %d 个在等单词工作台的检查结果：%s" % (len(slow), "、".join(slow[:20])))
        return
    bad = [w for w in WORDS if not (V.get(w) or {"ok": True}).get("ok")]
    txt = REPORT.replace("{k}", str(s0["k"])).replace("{list}", "、".join(w + (" ✗" if w in bad else " ✓") for w in WORDS))
    print()
    print("【最后汇报：这一批全部传完了，把下面几行原样回在聊天里】")
    _report("done", ("没过 %d 个：%s" % (len(bad), "、".join(bad))) if bad else "", txt)
    print(txt)


if PARTS and MODE == "汇报":
    _s0 = _sent()
    _left = [w for w in WORDS if w not in _s0["w"]]
    _why = " ".join(a for a in _s.argv[1:] if a not in ("汇报", "report"))[:300]
    _txt = (PARTIAL.replace("{cum}", str(len(_s0["w"]))).replace("{done}", "、".join(w + " ✓" for w in _s0["w"]) or "还没有")
            .replace("{left}", str(len(_left))).replace("{rest}", "、".join(_left[:30]) + ("…" if len(_left) > 30 else "")))
    print("【汇报：把下面几行原样回在聊天里】")
    _report("stop", _why, _txt)
    print(_txt)
    raise SystemExit


if PARTS and MODE == "看结果":
    _s1 = _sent()
    _n1 = _s1.setdefault("n", {})
    for _w in _s1["w"]:
        _n1.setdefault(_w, 1)
    _next(_s1, _n1)
    raise SystemExit



FILE = "reply.txt"         # 你把回复写进的文件；放在别处就改成那个路径
_c = [d + FILE for d in ("", "/home/claude/", "/mnt/user-data/outputs/", "/tmp/") if os.path.exists(d + FILE)]
if _c:
    FILE = max(_c, key=os.path.getmtime)    # 好几个 reply.txt 时用最新写的那个（别把上一轮的传上去）
text = open(FILE, encoding="utf-8").read().replace("\r", "").replace(TOKEN, "***")   # 令牌别跟着传上去
assert "__END__" in text, "文件里没有最后一行 __END__：先把回复写完整"
IS_LAST = False
if PARTS:                  # 这次传的是哪几个词（看 @单词 那一行）；传完这次，这一批是不是全传完了
    here = [w for w in WORDS if re.search(r"[@＠]\s*" + re.escape(w) + r"(?![A-Za-z'’\-])", text)]
    s0 = _sent()
    after = [w for w in WORDS if w in set(s0["w"]) | set(here)]
    IS_LAST = len(after) == len(WORDS)
    if IS_LAST and "【这一批最后一个】" not in text:
        text = text.rstrip() + "\n【这一批最后一个】\n"      # 告诉单词工作台：这一批写完了

# 整理成 Excel：「题目」一题一行（给人看），「原文」一行一格原样放着（给软件读）
TYPES = {"听": "听力", "单": "单项选择", "形": "适当形式填空", "选": "选词填空", "改": "改错", "完": "完成句子"}
HEAD = ["单词", "题号", "题型", "中文/问题", "题目", "听力原文", "选项", "答案", "解析", "考点"]
WHERE = {"听": {3: 1, 5: 2, 6: 3, 8: 4}, "单": {4: 1, 6: 2, 8: 3, 9: 4}, "选": {6: 1, 4: 2, 7: 3, 8: 4, 9: 5},
         "形": {4: 1, 7: 2, 8: 3, 9: 4}, "改": {4: 1, 7: 2, 8: 3, 9: 4}, "完": {3: 1, 4: 2, 7: 3, 8: 4, 9: 5}}
qs, iss, src, word, n, in_iss = [HEAD], [["单词", "总表哪里不对"]], [["回复原文（软件从这一页读，别改）", "接下一行"]], "", 0, False
for line in text.split("\n"):
    rest = line
    while len(rest) > 30000:
        src.append([rest[:30000], "接"])
        rest = rest[30000:]
    src.append([rest, ""])
    l = line.strip().strip("`").strip()
    if l.startswith("总表问题"):
        in_iss = True
    elif in_iss:
        m = re.match(r"^[-*•]\s*(.+?)[:：]\s*(.+)$", l)
        if m:
            iss.append([m.group(1), m.group(2)])
    elif re.match(r"^(?:\d+[.、)]\s*)?[@＠]", l.strip("*#>_ ")):
        word, n = re.split(r"[|｜]", re.sub(r"^(?:\d+[.、)]\s*)?[@＠]\s*", "", l.strip("*#>_ ")))[0].strip(), 0
    else:
        m = re.match(r"^(?:\d+[.、)]\s*|[-*•]\s*)?([听单形选改完])\s*[|｜](.*)$", l)
        if m and word:
            f, n = [m.group(1)] + [v.strip() for v in re.split(r"[|｜]", m.group(2))], n + 1
            r = [word, n, TYPES[f[0]]] + [""] * 7
            for c, i in WHERE[f[0]].items():
                r[c] = f[i].replace("⏎", "\n") if i < len(f) else ""
            if f[0] in "听单" and r[6]:
                r[7] = re.split(r"\s+/\s+", r[6])[0]
            qs.append(r)
if len(qs) == 1:
    qs.append(["（这一批没有题目行，比如做画面的回复：内容在「原文」那一页）"])
BAD = re.compile("[\x00-\x08\x0b\x0c\x0e-\x1f\ufffe\uffff]")


def col(i):
    s, i = "", i + 1
    while i:
        i, k = divmod(i - 1, 26)
        s = chr(65 + k) + s
    return s


def sheet(rows, widths, keep=False):
    x = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<worksheet xmlns="http://schemas.openxmlformats.org/'
         'spreadsheetml/2006/main"><sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" '
         'activePane="bottomLeft" state="frozen"/></sheetView></sheetViews><cols>']
    x += ['<col min="%d" max="%d" width="%d" customWidth="1"/>' % (i + 1, i + 1, w) for i, w in enumerate(widths)]
    x.append("</cols><sheetData>")
    for r, row in enumerate(rows, 1):
        x.append('<row r="%d">' % r)
        for c, v in enumerate(row):
            s = 1 if r == 1 else 2
            if isinstance(v, int):
                x.append('<c r="%s%d" s="%d"><v>%d</v></c>' % (col(c), r, 3 if r > 1 else 1, v))
            elif v or keep:
                x.append('<c r="%s%d" s="%d" t="inlineStr"><is><t xml:space="preserve">%s</t></is></c>'
                         % (col(c), r, s, escape(BAD.sub("", str(v)))))
        x.append("</row>")
    return "".join(x) + "</sheetData></worksheet>"


def xlsx(sheets):
    R, P = "http://schemas.openxmlformats.org/officeDocument/2006/relationships", "http://schemas.openxmlformats.org/package/2006/"
    T, H = "application/vnd.openxmlformats-officedocument.spreadsheetml.", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    k = range(1, len(sheets) + 1)
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", H + '<Types xmlns="%scontent-types"><Default Extension="rels" ContentType="application/'
                   'vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
                   '<Override PartName="/xl/workbook.xml" ContentType="%ssheet.main+xml"/><Override PartName="/xl/styles.xml" '
                   'ContentType="%sstyles+xml"/>%s</Types>' % (P, T, T, "".join(
                       '<Override PartName="/xl/worksheets/sheet%d.xml" ContentType="%sworksheet+xml"/>' % (i, T) for i in k)))
        z.writestr("_rels/.rels", H + '<Relationships xmlns="%srelationships"><Relationship Id="rId1" Type="%s/officeDocument" '
                   'Target="xl/workbook.xml"/></Relationships>' % (P, R))
        z.writestr("xl/workbook.xml", H + '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                   'xmlns:r="%s"><sheets>%s</sheets></workbook>' % (R, "".join(
                       '<sheet name="%s" sheetId="%d" r:id="rId%d"/>' % (sheets[i - 1][0], i, i) for i in k)))
        z.writestr("xl/_rels/workbook.xml.rels", H + '<Relationships xmlns="%srelationships">%s<Relationship Id="rId%d" '
                   'Type="%s/styles" Target="styles.xml"/></Relationships>' % (P, "".join(
                       '<Relationship Id="rId%d" Type="%s/worksheet" Target="worksheets/sheet%d.xml"/>' % (i, R, i) for i in k),
                       len(sheets) + 1, R))
        z.writestr("xl/styles.xml", H + '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts '
                   'count="2"><font><sz val="11"/><name val="等线"/></font><font><b/><sz val="11"/><name val="等线"/></font></fonts>'
                   '<fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/>'
                   '</fill></fills><borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
                   '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs '
                   'count="4"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/><xf numFmtId="0" fontId="1" '
                   'fillId="0" borderId="0" xfId="0" applyFont="1"/><xf numFmtId="0" fontId="0" fillId="0" borderId="0" '
                   'xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf><xf numFmtId="0" fontId="0" '
                   'fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment horizontal="center" vertical="top"/></xf>'
                   '</cellXfs><cellStyles count="1">'
                   '<cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>')
        for i in k:
            z.writestr("xl/worksheets/sheet%d.xml" % i, sheets[i - 1][1])
    return b.getvalue()


try:
    sh = [("题目", sheet(qs, [14, 6, 12, 22, 40, 34, 34, 18, 40, 10]))]
    if len(iss) > 1:
        sh.append(("总表问题", sheet(iss, [16, 80])))
    sh.append(("原文", sheet(src, [120, 10], keep=True)))
    import time as _t
    STEM = NAME + ("-" + _t.strftime("%H%M%S") + ("-end" if IS_LAST else "") if PARTS else "")   # 一个一个传：每次一个文件，名字都以 NAME 开头；最后一个带 -end
    data, path = xlsx(sh), STEM + ".xlsx"
except Exception as e:
    print("做 Excel 出错（%s），改传文本文件" % e)
    data, path = text.encode("utf-8"), STEM + ".txt"
url = "https://api.github.com/repos/%s/contents/%s" % (REPO, path)
H = {"Authorization": "Bearer " + TOKEN, "Accept": "application/vnd.github+json", "User-Agent": "wordsvideo-relay"}
body = {"message": "接力回复 " + path, "content": base64.b64encode(data).decode(), "branch": BRANCH}
try:
    try:
        with urllib.request.urlopen(urllib.request.Request(url + "?ref=" + BRANCH, headers=H), timeout=60) as r:
            body["sha"] = json.load(r)["sha"]          # 同名文件已经有了（重传）：覆盖它
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
    with urllib.request.urlopen(urllib.request.Request(url, data=json.dumps(body).encode(), headers=H, method="PUT"), timeout=120) as r:
        nq = len(qs) - 1 if len(qs) > 1 and qs[1][1:] else 0
        print("上传好了", r.status, path, ("（%d 道题）" % nq) if nq else "")
    if PARTS:              # 记下传到第几个；等单词工作台检查，没过的马上改；全部传完、都检查过才打印【最后汇报】
        s0["k"] += 1
        s0["w"] = after
        n0 = s0.setdefault("n", {})
        for w in here:
            n0[w] = int(n0.get(w) or 0) + 1
        json.dump(s0, open(MEM, "w", encoding="utf-8"), ensure_ascii=False)
        print("上传好了（第 %d 次）：这次 %s；这一批已经传了 %d/%d 个。"
              % (s0["k"], "、".join(here) or "（没认出词：每个词前面要有 @单词 那一行）", len(after), len(WORDS)))
        _next(s0, n0)
        raise SystemExit
    found = [w for w in WORDS if w in text]
    miss = [w for w in WORDS if w not in text]
    print()
    print("【汇报：把下面这几行原样回在聊天里】")
    print(REPORT.replace("{path}", path).replace("{found}", "、".join(w + " ✓" for w in found) or "（一个词都没找到）")
          .replace("{miss}", ("；没找到：" + "、".join(w + " ✗" for w in miss)) if miss else "").replace("{chars}", "{:,}".format(len(text))))
except urllib.error.HTTPError as e:
    print("上传失败", e.code, e.read().decode("utf-8", "replace")[:300])
except Exception as e:
    print("上传失败（可能连不上 api.github.com）", repr(e)[:300])
"""


def inbox_cfg(cfg=None):
    cfg = cfg or load_cfg()
    ib = dict(DEFAULT_CFG["relayInbox"], **(cfg.get("relayInbox") or {}))
    ib["token"] = (ib.get("token") or "").strip()
    ib["repo"] = re.sub(r"^https?://github\.com/|\.git$|/+$", "", (ib.get("repo") or "").strip())
    ib["dir"] = (ib.get("dir") or "inbox").strip("/ ") or "inbox"
    if ib["repo"].lower() in ("", "jacklee15333/wordsvideo-inbox"):     # v1.8.0 的默认值（这个仓库没建过）
        ib["repo"] = DEFAULT_CFG["relayInbox"]["repo"]
    return ib


def _main_repo(cfg=None):
    m = re.search(r"github\.com[/:]([^/]+/[^/.]+)", (cfg or load_cfg()).get("repoUrl", ""))
    return m.group(1) if m else ""


def _same_as_master(cfg=None):
    """收件箱令牌和左边「设置」里的 GitHub 令牌是同一个：那是万能令牌，不能写进提示词。"""
    cfg = cfg or load_cfg()
    a, b = inbox_cfg(cfg)["token"], (cfg.get("githubToken") or "").strip()
    return bool(a) and a == b


def inbox_on(cfg=None):
    cfg = cfg or load_cfg()
    ib = inbox_cfg(cfg)
    return (cfg.get("provider") == "relay" and bool(ib.get("enabled")) and bool(ib["token"]) and "/" in ib["repo"]
            and not _same_as_master(cfg) and not INBOX_BAD.get(ib["token"]))


INBOX_BAD = {}      # 检测出能写主仓库的收件箱令牌：这次开着软件期间不往提示词里写


def _gh(method, path, token, body=None, timeout=30):
    """调 GitHub 接口；连不上就换网络方式（设置里的代理 → 直连 → 系统代理 → 本机代理端口）。返回 (状态码, 内容)。"""
    first = load_cfg().get("gitProxy") or ""
    tried, last = [], None
    for px in [first] + _proxy_candidates():
        if px in tried:
            continue
        tried.append(px)
        req = urllib.request.Request("https://api.github.com" + path, method=method,
                                     data=json.dumps(body).encode() if body is not None else None,
                                     headers={"Authorization": "Bearer " + token, "User-Agent": "chuti-studio",
                                              "Accept": "application/vnd.github+json", "Content-Type": "application/json"})
        hs = [urllib.request.ProxyHandler({"http": px, "https": px} if px else {})]
        try:
            with urllib.request.build_opener(*hs).open(req, timeout=timeout) as r:
                raw = r.read().decode("utf-8", "replace")
                return r.status, (json.loads(raw) if raw.strip() else {})
        except urllib.error.HTTPError as e:
            try:
                d = json.loads(e.read().decode("utf-8", "replace") or "{}")
            except Exception:
                d = {}
            return e.code, d
        except Exception as e:          # 网络不通：换下一种
            last = e
    raise RuntimeError("连不上 GitHub：%s" % str(last)[:160])


def can_write(repo, token):
    """真试一下能不能写：在仓库里建一个不挂在任何提交上的小数据块（仓库里看不到，GitHub 过段时间自己清掉）。
    不看接口返回的 permissions：公开仓库对令牌没给的仓库也显示“能推”，会误报。返回 True / False / None（连不上）。"""
    try:
        st, d = _gh("POST", "/repos/%s/git/blobs" % repo, token, {"content": "wordsvideo-check", "encoding": "utf-8"})
    except Exception:
        return None
    if st == 201:
        return True
    if st in (403, 404):
        return False
    return None


def check_inbox():
    cfg = load_cfg()
    ib = inbox_cfg(cfg)
    if not ib["token"]:
        return False, "还没填收件箱令牌（填 GitHub 上叫「收件箱用」的那个小令牌）"
    if "/" not in ib["repo"]:
        return False, "收件箱仓库要写成 用户名/仓库名"
    if _same_as_master(cfg):
        return False, "这里填的是万能令牌（和左边「设置」里的 GitHub 令牌一样）。它会被写进发给网页 AI 的提示词，不能用：换成「收件箱用」那个小令牌"
    try:
        st, d = _gh("GET", "/repos/" + ib["repo"], ib["token"])
    except Exception as e:
        return False, str(e)
    if st == 404:
        return False, "找不到仓库 %s：检查仓库名，令牌要给这个仓库的权限" % ib["repo"]
    if st != 200:
        return False, "GitHub 不让进（%s）：令牌不对或过期了" % st
    w = can_write(ib["repo"], ib["token"])
    if w is None:
        return False, "连不上 GitHub，没测出来：检查网络或左边「设置」里的代理，再点一次"
    if not w:
        return False, "这个令牌写不进 %s：GitHub 令牌设置里要选这个仓库，Contents 给 Read and write" % ib["repo"]
    main = _main_repo(cfg)
    if main and main.lower() != ib["repo"].lower():
        mw = can_write(main, ib["token"])
        if mw:
            INBOX_BAD[ib["token"]] = True
            return False, ("这个令牌还能改主仓库 %s，像是万能令牌：它会写进发给网页 AI 的提示词，别人拿到就能改你的词库。"
                           "换成只选了 %s 的「收件箱用」小令牌" % (main, ib["repo"]))
    elif main:
        return True, "有写权限（注意：收件箱填的就是存题目的主仓库，建议改回 %s）" % DEFAULT_CFG["relayInbox"]["repo"]
    INBOX_BAD.pop(ib["token"], None)
    return True, "有写权限，而且只能写收件箱，不能动主仓库 ✓ 可以用了"


def batch_info(words, kind):
    """这一份在这一批里的位置：这一批几个词、已经做完几个（同一个词改错几轮只算一次）。"""
    t = RUNNER.task or {}
    try:
        tp = json.loads(t.get("params") or "{}")
    except Exception:
        tp = {}
    total = len(tp.get("words") or []) or int(tp.get("count") or 0)
    done = len({w for x in (RELAY.get("done") or []) if x.get("ok") is not None for w in (x.get("words") or [])}) \
        if RELAY.get("doneTid") == t.get("id") else 0
    return {"kind": kind or "", "words": list(words), "total": total, "done": done}


def relay_report(name, info):
    """网页 AI 上传好以后在聊天里回的汇报（{path} {found} {miss} {chars} 由上传脚本填；
    一份好几个词、一轮一轮传时还有 {k} {nf} {cum} {left} {next}）。"""
    ws = info.get("words") or []
    if info.get("round") and len(ws) > 1:      # v1.10.10：一批好几个词——一个一个传，全部传完才汇报一次
        tot, dn, n = int(info.get("total") or 0), int(info.get("done") or 0), len(ws)
        lines = ["✅ 这一批 %d 个词都写完、上传好了（一共传了 {k} 次）" % n,
                 "%s：{list}" % (info.get("kind") or "这一批")]
        if tot:
            lines.append("这一批是这次 %d 个词里的第 %d–%d 个" % (tot, dn + 1, min(tot, dn + n)))
        lines.append("→ 这次的词就都做完了" if tot and dn + n >= tot else
                     "→ 回到单词工作台：它收下、检查以后会给下一批新的提示词，要再粘贴过来")
        return "\n".join(lines)
    ws = info.get("words") or []
    n, kind = len(ws), info.get("kind") or "这一批"
    fix = "改" in kind
    lines = ["✅ 已上传 {path}",
             "这次：%s · %d 个词：%s" % (kind, n, "、".join(ws[:12]) + ("…（共 %d 个）" % n if n > 12 else "")),
             "文件里有：{found}{miss}（{chars} 字）"]
    tot, dn = int(info.get("total") or 0), int(info.get("done") or 0)
    left = None
    if fix:
        lines.append("这是改错：这些词上次没过检查，这次重新写")
    elif tot:
        a, b = dn + 1, min(tot, dn + n)
        left = tot - b
        lines.append("这次进度：%d 个词里的第 %s 个（这份交回去，就做完 %d 个，还剩 %d 个）"
                     % (tot, ("%d" % a) if a == b else "%d–%d" % (a, b), b, left))
    lines.append("这是这次的最后一份：交回去、单词工作台检查完，这次的词就都做完了。" if left == 0 else
                 "⚠ 这次还没做完：回到单词工作台，它收下、检查以后会给下一份新的提示词，要再粘贴过来。")
    return "\n".join(lines)


def relay_partial(info):
    """写到一半对话写不下了、要停下时的汇报（{cum} {done} {left} {rest} 由上传脚本填）。"""
    n = len(info.get("words") or [])
    return ("⏸ 这一批 %d 个词：已经上传 {cum} 个（{done}），还没写 {left} 个：{rest}\n"
            "→ 停下了：单词工作台黄框第 ③ 步会出「继续」——对话还能写，点「在原来的对话里接着写」；写不下了，点「开新对话」" % n)


def inbox_prompt(name, info=None):
    """name：收件箱里的文件名，不带扩展名（网页 AI 传上来的是 name.xlsx；做不成 Excel 时是 name.txt）。
    info：这一份是哪些词、这一批做到第几个了（写进汇报，网页 AI 上传好以后原样回在聊天里）。"""
    ib = inbox_cfg()
    info = info or {"words": [], "kind": ""}
    ws = list(info.get("words") or [])
    parts = bool(info.get("round")) and len(ws) > 1
    tot, dn = int(info.get("total") or 0), int(info.get("done") or 0)
    lastone = bool(tot) and dn + len(ws) >= tot
    script = INBOX_SCRIPT.replace("__WORDS__", repr(ws)).replace("__REPORT__", repr(relay_report(name, info))) \
        .replace("__PARTS__", "True" if parts else "False").replace("__ROUND__", str(int(info.get("round") or 0))) \
        .replace("__LASTONE__", "True" if lastone else "False").replace("__PARTIAL__", repr(relay_partial(info)))
    for k, v in (("__TOKEN__", ib["token"]), ("__REPO__", ib["repo"]), ("__BRANCH__", ib["branch"] or "main"),
                 ("__NAME__", name), ("__END__", END)):
        script = script.replace(k, v)
    if parts:
        rnd = int(info.get("round") or 1)
        return ("【写完一个就上传一个：你自己传到 GitHub；中间不用在聊天里汇报，全部写完再汇报一次】\n"
                "这一批 %d 个词，按顺序一个接一个写。每写完 %d 个词（%d 个 @单词 段），就：\n"
                "1. 把刚写的这几个词（格式完全一样，最后一行 %s）写进文本文件 reply.txt（用你的建文件工具，覆盖上一次的）。\n"
                "2. 用代码执行工具运行下面这段 Python（只用标准库，不用装任何东西）：它把 reply.txt 整理成 Excel 传到 GitHub，自己记着传到第几个了；"
                "传的是这一批最后一个词时，它会自动告诉单词工作台“这一批写完了”。文件名、记数都不用你管。\n"
                "```python\n%s```\n"
                "3. 传完以后，脚本会等单词工作台检查（它在老师的电脑上用视频技能起草检查，一般半分钟到两分钟），打印【起草检查结果】："
                "✓ 的不用管；✗ 的**马上改**：照“还要补”的每一条改好，把这个词完整重写一遍，再写进 reply.txt 运行同一段脚本传上去（每个词最多改 %d 次）。"
                "改好了再接着写下一个。这样每个词交出去就是过了检查的，老师不用回来补。\n"
                "4. 上传好了、改好了都**不用在聊天里汇报**，一直写到这一批 %d 个词全部传完、都过了检查（不用等我说“继续”）。"
                "全部做完时，脚本会打印【最后汇报】（第一行是【单词工作台·汇报】）：这时才在聊天里把那几行原样回给我——整批只汇报这一次。"
                "**每一轮回复结束前，最后一件事都是运行脚本、把它打印的【单词工作台·汇报】那几行原样回给我**（写完了脚本自己会打印；要停下就用下面第 5 条）；"
                "脚本同时会把这几行告诉单词工作台，软件靠它知道你写到哪儿、是写完了还是停下了。\n"
                "5. 写到一半对话太长、写不下了（或者这一次回复写不下了、要停下）：先把已经写好的传上去，再把脚本里的 MODE 改成 \"汇报\" 运行一次"
                "（或者运行 python upload.py 汇报 一句话原因），它会告诉单词工作台你停在哪儿；把它打印的几行回给我。我会让你接着写，或者开新对话把剩下的词给你。\n"
                "6. 没有代码执行工具、或者上传失败了：就照常把写好的完整回复直接写在聊天里（最后一行 %s），并说明上传失败的原因，我会点「复制」交回。"
                % (len(ws), rnd, rnd, END, script, relay_tries(), len(ws), END))
    return ("【写完以后：你自己把回复整理成 Excel 传到 GitHub，不用在聊天里贴全文】\n"
            "1. 把上面要求的完整回复（格式完全一样，最后一行 %s）写进文本文件 reply.txt（用你的建文件工具）。\n"
            "2. 用代码执行工具运行下面这段 Python（只用标准库，不用装任何东西）：它会把 reply.txt 整理成 Excel（.xlsx）传到 GitHub。\n"
            "```python\n%s```\n"
            "3. 上传好了，脚本最后会打印【汇报】几行：把这几行原样回在聊天里（写清楚这次传的是哪几个词、这一批做到第几个、还剩几个）。"
            "不要只写一行“已上传 %s.xlsx”，也不要在聊天里再写一遍全文。（文件名一定用上面脚本里的 NAME，不要用以前的；每一份的名字都不一样）\n"
            "4. 要是没有代码执行工具、或者上传失败了：就照常把完整回复直接写在聊天里（最后一行 %s），并说明上传失败的原因。"
            % (END, script, name, END))


def xlsx_reply_text(data):
    """收件箱里的 Excel → 回复原文：「原文」那一页一行一格，太长的行拆成几格、B 列写“接”。"""
    import io
    import openpyxl
    wb = openpyxl.load_workbook(io.BytesIO(data), data_only=True)
    if "原文" not in wb.sheetnames:
        raise ValueError("Excel 里没有「原文」这一页")
    lines, join = [], False
    for a, b in wb["原文"].iter_rows(min_row=2, max_col=2, values_only=True):
        a = "" if a is None else str(a)
        if join and lines:
            lines[-1] += a
        else:
            lines.append(a)
        join = (b == "接")
    return "\n".join(lines)


def inbox_fetch(name, alts=()):
    """看收件箱里有没有这一批的回复（name.xlsx，或者做不成 Excel 时的 name.txt）：有就返回 (原文, sha, 文件路径)，没有返回 None。"""
    ib = inbox_cfg()
    br = urllib.parse.quote(ib["branch"] or "main")
    folder = name.rsplit("/", 1)[0] if "/" in name else ""
    st, d = _gh("GET", "/repos/%s/contents/%s?ref=%s" % (ib["repo"], urllib.parse.quote(folder), br), ib["token"])
    if st == 404:                           # inbox 文件夹还没有：还没传上来
        INBOX_LAST.update(files=[], ts=time.time())
        return None
    if st != 200:
        raise RuntimeError("看收件箱出错（%s）：%s" % (st, str((d or {}).get("message", ""))[:120]))
    have = {x.get("path") for x in d} if isinstance(d, list) else set()
    INBOX_LAST.update(files=sorted(p.rsplit("/", 1)[-1] for p in have if p), ts=time.time())
    path = next((n + e for n in (name,) + tuple(alts or ()) for e in (".xlsx", ".txt") if n + e in have), "")
    if not path:
        return None
    st, d = _gh("GET", "/repos/%s/contents/%s?ref=%s" % (ib["repo"], urllib.parse.quote(path), br), ib["token"])
    if st == 404:
        return None
    if st != 200:
        raise RuntimeError("看收件箱出错（%s）：%s" % (st, str(d.get("message", ""))[:120]))
    raw = d.get("content") or ""
    if raw:
        data = base64.b64decode(raw)
    else:                                   # 超过 1 MB：接口不给内容，走下载地址
        req = urllib.request.Request(d.get("download_url") or "", headers={"Authorization": "Bearer " + ib["token"],
                                                                            "User-Agent": "chuti-studio"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
    if path.endswith(".xlsx"):
        try:
            text = xlsx_reply_text(data)
        except Exception as e:
            raise ExcelBad("收件箱里的 Excel 读不出来（%s）" % str(e)[:100])
    else:
        text = data.decode("utf-8", "replace")
    return text, d.get("sha", ""), path


class ExcelBad(Exception):
    pass


def inbox_delete(path, sha):
    ib = inbox_cfg()
    try:
        _gh("DELETE", "/repos/%s/contents/%s" % (ib["repo"], urllib.parse.quote(path)), ib["token"],
            {"message": "收件箱：取走了 " + path, "sha": sha, "branch": ib["branch"] or "main"})
    except Exception as e:
        log("收件箱里的 %s 没删掉（不要紧，下次不会再用它）：%s" % (path, str(e)[:120]))


def _looks_reply(text, words):
    """剪贴板里这段是不是这一批的回复：有结束标记，而且提到了这一批的词（出题）或者有画面设置的 JSON（做画面）。"""
    t = text or ""
    if END not in t or len(t) < 80:
        return False
    if any(k in t for k in ("【做画面", "【补画面", "【改软件】", "【出题规矩】", "【这一段就是要你复制", "【写完一个就上传一个", 'NAME = "inbox/')):
        return False             # 复制的是提示词本身（v1.18.0：以前只认“【做画面】”，提示词开头其实是“【做画面 · 这一批…】”，被当成了回复）
    return any(("@" + w) in t or ("＠" + w) in t for w in words) or '"pics"' in t


def relay_wait(prompt, words):
    """手动接力：提示词放进剪贴板，等你在网页 AI 里发送；你在网页里点“复制”它的回复，软件看到就自己接着做
    （也可以把回复粘到软件里点「交回给软件」）。最多等 12 小时。"""
    if set(words) <= RELAY_SKIP:            # 这批你点了跳过：改错轮也不再问
        return ""
    RELAY_SKIP.clear()
    import clip
    cfg = load_cfg()
    ibox = inbox_on(cfg)
    use_clip = clip.WIN and cfg.get("relayClipboard", True) and not ibox   # v1.18.0：网页 AI 自己上传时不看剪贴板（复制提示词会被当成回复）
    ib0 = inbox_cfg(cfg)
    if not ibox and cfg.get("provider") == "relay" and ib0.get("enabled") and ib0["token"]:
        log("收件箱令牌像是万能令牌，没写进提示词（这一批照旧要你点「复制」）：「⚙ 设置」里换成「收件箱用」小令牌，点「检测收件箱」",
            (RUNNER.task or {}).get("id"))
    ipath = ""
    if ibox:      # 每一批一个新文件名，旧回复不会被当成这一批的
        ipath = "%s/%s" % (inbox_cfg(cfg)["dir"], batch_name("", words))
        prompt = prompt.rstrip() + "\n\n" + inbox_prompt(ipath, batch_info(words, AI_LIVE.get("kind", "")))
    with _RELAY_LOCK:
        tid = (RUNNER.task or {}).get("id")
        RELAY.update(id=RELAY["id"] + 1, status="等你操作", prompt=prompt, words=list(words), kind=AI_LIVE.get("kind", ""),
                     reply="", ts=time.time(), copied=False, hint="", clip=use_clip, inbox=(ipath + ".xlsx") if ipath else "",
                     phase="send", tid=tid, polls=0, lastPoll=0.0, stage="", multi=False, pollNow=0.0, nextPoll=0.0, pollBy="", pollGot=0)
        rid = RELAY["id"]
        if not RELAY_HIST:
            RELAY_HIST.extend(_hist_load(tid, words))   # 软件重开：接上重开前的几轮
        if RELAY_HIST and (RELAY_HIST[-1].get("words") != list(words) or RELAY_HIST[-1].get("tid") != tid):
            RELAY_HIST.clear()                       # 换了一批词（或者换了任务）：重新记
        RELAY_HIST.append({"id": rid, "kind": RELAY["kind"], "words": list(words), "tid": tid, "t0": time.time(),
                           "inbox": RELAY["inbox"], "got": 0.0, "glen": 0, "res": "", "detail": "", "t1": 0.0})
        del RELAY_HIST[:-10]
        _hist_save()
        alts = [h["inbox"][:-5] for h in RELAY_HIST[:-1] if h.get("inbox")]      # 前几轮的文件名：网页 AI 用了旧名字也认
        t0 = RELAY_HIST[-1]["t0"]
    if len(RELAY_HIST) > 1 and RELAY_HIST[-2].get("res") in ("fail", "gone"):
        pv = RELAY_HIST[-2]
        _say("━━━━ 第 %d 轮%s → 现在是第 %d 轮：新的提示词已经复制好了，请到网页 AI 里重新粘贴、发送（最好开新对话）%s ━━━━" % (
            len(RELAY_HIST) - 1, "收到了、检查没过" if pv.get("res") == "fail" else "没等到回复（软件重开过）", len(RELAY_HIST),
            ("；网页 AI 说的“已上传 %s”是第 %d 轮的，已经用过了" % (pv["inbox"].rsplit("/", 1)[-1], len(RELAY_HIST) - 1)) if pv.get("got") and pv.get("inbox") else ""))
    _say("手动接力 第 %d 轮（%s）：%s … %s，%d 个词，等你在网页 AI 里粘贴、发送%s" % (
        len(RELAY_HIST), RELAY["kind"] or "提示词", words[0], words[-1], len(words), ("；写完它会传 %s.xlsx" % ipath) if ipath else ""))
    after = ("写完它会自己把回复整理成 Excel 传到中转仓库（%s.xlsx），软件看到就接着做" % ipath) if ibox else "写完点它回复下面的「复制」，软件会自己接着做"
    if use_clip and clip.set_text(prompt):
        RELAY["copied"] = True
        log("提示词已经放进剪贴板（%s … %s，%d 个词）：到网页 AI 里粘贴、发送；%s" % (words[0], words[-1], len(words), after), tid)
    else:
        log("要你操作：复制提示词到网页 AI 发送（%s … %s，%d 个词）；%s" % (words[0], words[-1], len(words), after), tid)
    clip.beep()
    last = clip.seq() if use_clip else 0
    poll = max(5, int(inbox_cfg(cfg).get("pollSec") or 15))
    next_ib, ib_err = time.time() + poll, 0
    RELAY["nextPoll"] = next_ib
    end = time.time() + 12 * 3600
    try:
        while time.time() < end:
            by_you = bool(RELAY.get("pollNow"))
            if ibox and (time.time() >= next_ib or by_you):
                RELAY["pollNow"] = 0.0
                next_ib = time.time() + poll
                try:
                    got = inbox_fetch(ipath, alts)
                    ib_err = 0
                    with _RELAY_LOCK:
                        RELAY["polls"] = RELAY.get("polls", 0) + 1
                        RELAY.update(lastPoll=time.time(), nextPoll=time.time() + poll, pollBy="you" if by_you else "auto",
                                     pollGot=1 if got else 0, pollErr="")
                    if not got:
                        try:
                            ups = inbox_uploads()
                        except Exception:
                            ups = None
                        if ups is not None:
                            INBOX_LAST["uploads"] = ups
                            fs0 = set(INBOX_LAST.get("files") or [])
                            for u in ups:                  # 这一轮开始以后传的、还在 inbox/ 里、名字对不上的
                                p0 = u["path"]
                                if u["ts"] >= t0 - 5 and p0.rsplit("/", 1)[-1] in fs0 and not p0.startswith(ipath) \
                                        and not any(p0.startswith(a) for a in alts):
                                    try:
                                        g2 = inbox_fetch(p0.rsplit(".", 1)[0])
                                    except Exception:
                                        g2 = None
                                    if g2 and _looks_reply(g2[0], words) and any(w in g2[0] for w in words):
                                        got = g2
                                        log("网页 AI 传上来的文件名和这一轮的不一样（%s，这一轮要的是 %s.xlsx）：看内容是这一批的，收下了" % (p0, ipath), tid)
                                        break
                    if not got and (RELAY["polls"] <= 4 or RELAY["polls"] % max(1, 60 // poll) == 0):
                        fs = INBOX_LAST.get("files") or []
                        up = (INBOX_LAST.get("uploads") or [None])[0]
                        lab = ""
                        if up:
                            b0 = up["path"].rsplit(".", 1)[0]
                            k = next((i for i, h in enumerate(RELAY_HIST[:-1]) if h.get("inbox") and h["inbox"].rsplit(".", 1)[0] == b0), None)
                            lab = "（就是这一轮的）" if b0 == ipath else ("（第 %d 轮的，已经收下用过了）" % (k + 1)) if k is not None else \
                                ("（这一轮开始以前传的）" if up["ts"] < t0 else "")
                        _say("中转仓库 第 %d 次看：还没有第 %d 轮的 %s.xlsx（等了 %s）；inbox/ 里现在：%s；网页 AI 最近一次上传：%s%s" % (
                            RELAY["polls"], len(RELAY_HIST), ipath.rsplit("/", 1)[-1], _dur(time.time() - RELAY["ts"]),
                            "、".join(fs[:6]) + ("…" if len(fs) > 6 else "") if fs else "空的",
                            ("%s %s" % (time.strftime("%H:%M:%S", time.localtime(up["ts"])), up["path"].rsplit("/", 1)[-1])) if up else "没有记录", lab))
                except ExcelBad as e:
                    got = None
                    if RELAY.get("hint") != str(e) + "：点网页里回复下面的「复制」交回，或者叫它照常把全文写在聊天里":
                        log(str(e), tid)
                    RELAY["hint"] = str(e) + "：点网页里回复下面的「复制」交回，或者叫它照常把全文写在聊天里"
                except Exception as e:
                    got = None
                    ib_err += 1
                    if ib_err in (1, 20):
                        log("看收件箱出错（%s），过一会儿再看" % mask(str(e))[:160], tid)
                if got:
                    t, sha, gpath = got
                    if _looks_reply(t, words):
                        with _RELAY_LOCK:
                            if RELAY["id"] == rid and RELAY["status"] == "等你操作":
                                RELAY.update(status="交回了", reply=t, hint="")
                        log("网页 AI 把回复传到中转仓库了（%s，%d 字%s），接着做" % (
                            gpath, len(t), "；文件名是上一轮的，也收下了" if not gpath.startswith(ipath) else ""), tid)
                        inbox_delete(gpath, sha)
                        continue
                    RELAY["hint"] = "收件箱里的回复不完整（没有最后一行 ZBQ-END，或者没提到这批词）：在网页里叫它写完整再传一次"
            if RUNNER.stop_req:
                raise Stopped(RUNNER.stop_req)
            with _RELAY_LOCK:
                if RELAY["id"] == rid and RELAY["status"] == "交回了":
                    AI_LIVE["reply"] = RELAY["reply"]
                    RELAY.update(phase="checking", stage="检查格式、规矩…")
                    if RELAY_HIST and RELAY_HIST[-1]["id"] == rid:
                        RELAY_HIST[-1].update(got=time.time(), glen=len(RELAY["reply"]))
                        _hist_save()
                    return RELAY["reply"]
                if RELAY["id"] == rid and RELAY["status"] == "跳过":
                    RELAY["phase"] = ""
                    if RELAY_HIST and RELAY_HIST[-1]["id"] == rid:
                        RELAY_HIST[-1].update(res="skip", detail="你点了「这一批先跳过」", t1=time.time())
                        _hist_save()
                    return ""
            if use_clip:
                sq = clip.seq()
                if sq != last:
                    last = sq
                    t = clip.get_text()
                    if t and t.strip() != prompt.strip():
                        if _looks_reply(t, words):
                            with _RELAY_LOCK:
                                if RELAY["id"] == rid and RELAY["status"] == "等你操作":
                                    RELAY.update(status="交回了", reply=t, hint="")
                            log("从剪贴板收到了网页 AI 的回复（%d 字），接着做" % len(t), tid)
                            continue
                        if any(("@" + w) in t for w in words) or '"pics"' in t:
                            RELAY["hint"] = "剪贴板里的回复没有最后一行 ZBQ-END：可能还没写完，等它写完再点一次「复制」"
            time.sleep(1)
        raise Fatal("等了 12 小时没交回回复，先停下")
    finally:
        with _RELAY_LOCK:
            if RELAY["id"] == rid:
                RELAY["status"] = "" if RELAY["status"] != "交回了" else "用完了"


def relay_submit(rid, reply, skip=False):
    with _RELAY_LOCK:
        if RELAY["id"] != int(rid) or RELAY["status"] != "等你操作":
            return False, "这一批已经不在等了（可能任务停了），刷新一下"
        if skip:
            RELAY["status"] = "跳过"
            RELAY_SKIP.update(RELAY["words"])
            return True, "跳过了这一批（这些词算没过，会进“没过的词”）"
        m = REPORT_TAG.search(reply or "")
        is_report = bool(m) and not re.search(r"^[ \t>*#_]*[@＠]\s*[A-Za-z]", reply or "", re.M)
        if not is_report and len((reply or "").strip()) < 50:
            return False, "交回来的太短了：要把网页 AI 的整段回复都复制过来"
        if not is_report:
            RELAY.update(status="交回了", reply=reply)
    if is_report:
        st = {"写完了": "done", "停下了": "stop", "等检查结果": "wait"}[m.group(1)]
        w = re.search(r"原因[:：]\s*([^\n｜]+)", reply)
        relay_ai_report({"state": st, "text": reply[m.start():].strip(), "why": w.group(1).strip() if w else ""}, pasted=True)
        return True, "认出来了：这是网页 AI 的汇报（%s），黄框照这个判断进度" % m.group(1)
    return True, "收到了，程序在检查"


def provider_name(cfg=None):
    cfg = cfg or load_cfg()
    pv = cfg.get("provider", "web")
    if pv == "api":
        return "接口 AI：%s（%s）" % (cfg["api"].get("model") or "?", re.sub(r"^https?://", "", cfg["api"].get("baseUrl", "")).split("/")[0])
    if pv == "mock":
        return "模拟 AI（只测流程，存的是假题）"
    if pv == "relay":
        return ("手动接力（你在网页 AI 里粘贴、发送；它写完自己把 Excel 传到中转仓库）" if inbox_on(cfg)
                else "手动接力（你在网页 AI 里粘贴、发送，写完点「复制」）")
    return "网页镜像 ChatGPT（sorryios）"


def ai_complete(prompt, words, on_progress=None):
    cfg = load_cfg()
    pv = cfg.get("provider", "web")
    if pv == "mock":
        r = mock_reply(prompt, words)
        dl = float(os.environ.get("CHUTI_MOCK_DELAY", "0"))      # 测实时画面用：模拟一边写一边出来
        for k in range(1, 11):
            AI_LIVE["reply"] = r[:len(r) * k // 10]
            time.sleep(dl / 10)
        return r
    if pv == "relay":
        if os.environ.get("CHUTI_RELAY_AUTO"):           # 自测用：模拟一个人过几秒交回
            threading.Timer(3, lambda: relay_submit(RELAY["id"], mock_reply(prompt, words))).start()
        return relay_wait(prompt, words)
    if pv == "api":
        a = cfg["api"]
        if not a.get("key"):
            raise Fatal("用的是接口 AI，可还没填密钥：任务页「⚙ 设置」里填")
        url = a["baseUrl"].rstrip("/")
        url = url + ("/chat/completions" if not url.endswith("/chat/completions") else "")
        body = json.dumps({"model": a["model"], "messages": [{"role": "user", "content": prompt}], "stream": True,
                           "temperature": a.get("temperature", 0.3), "max_tokens": a.get("maxTokens", 8000)}).encode()
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json",
                                                               "Authorization": "Bearer " + a.get("key", "")})
        out = []
        with urllib.request.urlopen(req, timeout=a.get("timeout", 600)) as r:      # 一边写一边收，实时画面看得到
            for raw in r:
                line = raw.decode("utf-8", "replace").strip()
                if not line.startswith("data:"):
                    continue
                data = line[5:].strip()
                if data == "[DONE]":
                    break
                try:
                    dl = json.loads(data)["choices"][0].get("delta") or {}
                except Exception:
                    continue
                piece = dl.get("content") or ""
                if piece:
                    out.append(piece)
                    AI_LIVE["reply"] = "".join(out)
                if on_progress and len(out) % 40 == 1:
                    on_progress("接收回复中…（%d 字）" % len(AI_LIVE["reply"]))
        return "".join(out)
    wm = _web()
    if not wm.is_available():
        raise Fatal("没装 Playwright：在命令行运行  python -m pip install playwright")
    tmo = int(cfg.get("replyTimeoutMin", 30)) * 60000
    return wm.web_complete(prompt, on_progress=on_progress, newChat=True, bestModel=bool(cfg.get("bestModel", True)),
                           requiredMarkers=[END], markersMinHits=1, minExpectedLength=200, timeout=tmo,
                           thinkNoOutputMs=max(300000, int(tmo * 0.8)), stuckFatalMs=max(300000, int(tmo * 0.5)),
                           longThinkMs=600000)


def mock_reply(prompt, words):
    """模拟 AI（试用和自测用）：写出格式对的稿；第一次故意让一部分词漏写考点，测“退回重写”。"""
    time.sleep(0.3)
    if "【做画面】" in prompt:
        import pics
        return pics.mock(prompt, words)
    if "【改软件】" in prompt:                 # 模拟改软件：挑 core.py，改它开头那句说明
        if "全文 =====" not in prompt:
            return "FILES: app/core.py\n" + END
        old = "单词工作台 · " + "核心"            # 拼起来写，免得这句原文在本文件里出现两次
        return ("```text\n<<<FILE app/core.py\n<<<FIND\n" + old + "\n>>>REPLACE\n" + old + "（模拟改写测试）\n>>>END\n```\n"
                "说明：\n- 模拟：改了 core.py 开头的说明\n" + END)
    fix = "没通过程序体检" in prompt
    out = ["```text"]
    for i, w in enumerate(words):
        out += ["@" + w,
                "听|说话人提到了哪个词？|I heard the word %s today.|%s / apple / river / pencil|句子里说的是 %s。" % (w, w, w),
                "单|She ______ to school every day.|walks / walk / walking / walked|主语 she、every day，用三单 walks。|",
                "形|He is good at ______. (swim)|swimming|介词 at 后面用动名词 swimming。|变形",
                "改|They is my good friends.|is → are|主语 they 是复数，用 are。|",
                "完|我们去公园吧。|Let's go to the ______.|park|去公园 go to the park。|",
                "选|tall、high|The tree is very ______.|tall|说树高用 tall。|易混",
                "单|I have ______ apple.|an / a / the / some|apple 以元音音素开头，用 an。|" +
                ("" if ((not fix and i % 4 == 1) or w.startswith("theat")) else "用法")]
    out += ["```", "总表问题：", "- %s：（模拟）这只是测试用的问题，不是真的" % words[0], END]
    return "\n".join(out)


# ═══════════════════════ 任务 ═══════════════════════
KIND_NAMES = {"words": "做指定的词", "pics": "做视频画面", "verify": "AI 核对总表", "selfedit": "改软件", "chuti": "出题", "redo": "重做待人工的词", "push": "上传到 GitHub", "sync": "同步仓库"}


def add_task(kind, params=None, run_after=0, title=""):
    params = params or {}
    if not title:
        if kind == "chuti":
            title = "出题 %s 个词" % (params.get("count") or "全部剩下的")
        elif kind == "redo":
            title = "重做待人工的 %d 个词" % len(params.get("words") or [])
        elif kind == "pics":
            title = ("做视频画面：%d 个指定的词" % len(params["words"])) if params.get("words") else \
                "做视频画面 %s 个词" % (params.get("count") or "全部能做的")
        else:
            title = KIND_NAMES.get(kind, kind)
    return x("INSERT INTO tasks(kind,title,params,status,created,run_after,progress) VALUES(?,?,?,?,?,?,?)",
             (kind, title, json.dumps(params, ensure_ascii=False), "排队", now(), float(run_after or 0), "{}"))


def in_window(cfg=None):
    w = (cfg or load_cfg()).get("window") or {}
    if not w.get("enabled"):
        return True
    t = time.strftime("%H:%M")
    a, b = w.get("start", "00:00"), w.get("end", "23:59")
    return (a <= t < b) if a <= b else (t >= a or t < b)


class Runner:
    def __init__(self):
        self.task = None
        self.state = "空闲"
        self.stage = ""
        self.stop_req = None          # None / "pause" / "cancel"
        self.wake = threading.Event()
        self.thread = None

    def start(self):
        # v1.10.6：上次没做完的（软件被关掉）先暂停，不自己接着做——你点开始才做；要接着做，在那一步点「继续」
        for t in q("SELECT id,title FROM tasks WHERE status='运行中' OR (status='排队' AND run_after<=?)", (time.time(),)):
            log("上次没做完的任务 #%d 暂停了：%s（要接着做，到那一步的进度里点「继续」；也可以直接重新开始）" % (t["id"], t["title"]), t["id"])
        x("UPDATE tasks SET status='已暂停' WHERE status='运行中' OR (status='排队' AND run_after<=?)", (time.time(),))
        self.thread = threading.Thread(target=self.loop, name="runner", daemon=True)
        self.thread.start()

    # ---- 外部控制 ----
    def request_stop(self, how):
        self.stop_req = how
        if self.task and load_cfg().get("provider") == "web":
            try:
                _web().cancel_current("在单词工作台点了%s" % ("暂停" if how == "pause" else "停止"))
            except Exception:
                pass

    def check_stop(self):
        if self.stop_req:
            raise Stopped(self.stop_req)

    def sleep(self, secs):
        end = time.time() + secs
        while time.time() < end:
            self.check_stop()
            time.sleep(1)

    # ---- 主循环 ----
    def loop(self):
        while True:
            try:
                self.fire_schedules()
                t = self.next_task()
                if t:
                    self.run_task(t)
                    continue
            except Exception as e:
                log("调度出错：%s" % e)
            self.wake.wait(10)
            self.wake.clear()

    def fire_schedules(self):
        today, hm, wd = time.strftime("%Y-%m-%d"), time.strftime("%H:%M"), str(datetime.date.today().isoweekday())
        for s in q("SELECT * FROM schedules WHERE enabled=1"):
            if s["last_date"] == today or hm < (s["at"] or "99:99") or wd not in (s["days"] or "1234567"):
                continue
            x("UPDATE schedules SET last_date=? WHERE id=?", (today, s["id"]))
            add_task(s["kind"], json.loads(s["params"] or "{}"), title="%s（定时：%s）" % (
                KIND_NAMES.get(s["kind"]), s["name"] or s["at"]))
            log("定时「%s」到点，加了一个任务" % (s["name"] or s["at"]))

    def next_task(self):
        if STATE.get("repo") != "就绪":
            self.state = "等仓库就绪（%s）" % STATE.get("repo")
            return None
        t = q("SELECT * FROM tasks WHERE status='排队' AND run_after<=? ORDER BY run_after>0, id LIMIT 1", (time.time(),), one=True)
        if not t:
            self.state = "空闲"
            return None
        if t["kind"] in ("chuti", "redo", "pics", "words") and not in_window() and load_cfg().get("provider") != "relay":
            w = load_cfg()["window"]
            self.state = "等时间窗口（%s–%s）" % (w["start"], w["end"])
            return None
        return t

    def run_task(self, t):
        self.task, self.stop_req = t, None
        tid = t["id"]
        AI_LIVE.update(reply="", kind="", words=[], started=0.0, done=0.0)
        x("UPDATE tasks SET status='运行中', started=COALESCE(started, ?), error='' WHERE id=?", (now(), tid))
        self.state = "运行中：" + t["title"]
        log("开始任务 #%d：%s" % (tid, t["title"]), tid)
        st, err = "已完成", ""
        try:
            p = json.loads(t["params"] or "{}")
            if t["kind"] == "chuti":
                self.do_chuti(tid, p)
            elif t["kind"] == "redo":
                self.do_redo(tid, p)
            elif t["kind"] == "words":
                self.do_words(tid, p)
            elif t["kind"] == "pics":
                import pics
                pics.do_pics(self, tid, p)
            elif t["kind"] == "verify":                       # v1.33.0：AI 核对总表（「导入」页）
                import sections
                sections.do_verify(self, tid, p)
            elif t["kind"] == "selfedit":
                import selfup
                selfup.do_selfedit(tid, p)
            elif t["kind"] == "push":
                log(push(), tid)
            elif t["kind"] == "sync":
                sync()
                log("同步好了：%s" % STATE.get("head"), tid)
        except Stopped as e:
            how = str(e)
            st = {"pause": "已暂停", "cancel": "已取消", "window": "排队"}.get(how, "已暂停")
            log("任务 #%d %s" % (tid, {"pause": "暂停了", "cancel": "停止了", "window": "到了时间窗口外，先停下，下次窗口打开时接着做"}.get(how, how)), tid)
        except Fatal as e:
            st, err = "失败", str(e)
            log("任务 #%d 停下：%s" % (tid, e), tid)
        except Exception as e:
            st, err = "失败", "%s\n%s" % (e, traceback.format_exc()[-1500:])
            log("任务 #%d 出错：%s" % (tid, e), tid)
        finally:
            x("UPDATE tasks SET status=?, finished=?, error=? WHERE id=?",
              (st, now() if st in ("已完成", "失败", "已取消") else None, mask(err), tid))
            self.task, self.stop_req, self.stage = None, None, ""
            self.state = "空闲"

    def progress(self, tid, **kw):
        t = q("SELECT progress FROM tasks WHERE id=?", (tid,), one=True)
        p = json.loads((t or {}).get("progress") or "{}")
        p.update(kw)
        x("UPDATE tasks SET progress=? WHERE id=?", (json.dumps(p, ensure_ascii=False), tid))
        return p

    # ---- 出题 ----
    def pick(self, n, only=None):
        _, rows = read_index()
        man = manual_words()
        out = []
        for r in rows:
            w = r[2]
            if r[4] != "缺" or w in out:
                continue
            if only is not None:
                if w not in only:
                    continue
            elif w in man:
                continue
            out.append(w)
            if len(out) >= n:
                break
        return out

    def do_chuti(self, tid, p):
        total = int(p.get("count") or 0)
        prog = json.loads(q("SELECT progress FROM tasks WHERE id=?", (tid,), one=True)["progress"] or "{}")
        done = prog.get("processed", 0)
        while True:
            self.check_stop()
            if not in_window() and load_cfg().get("provider") != "relay":
                raise Stopped("window")
            left = (total - done) if total else 10 ** 9
            if left <= 0:
                break
            sync()
            words = self.pick(min(group_size(), left))
            if not words:
                log("没有要出题的词了（剩下的都在待人工里）", tid)
                break
            self.run_group(tid, words)
            done += len(words)
            self.progress(tid, processed=done, total=total)
        log("任务 #%d 做完了：处理了 %d 个词" % (tid, done), tid)

    def do_words(self, tid, p):
        """做指定的词：按勾的步骤（出题、做视频画面）走一遍。"""
        words = [w for w in (p.get("words") or []) if w]
        steps = p.get("steps") or ["chuti", "pics"]
        sync()
        sk = (p.get("skipped") or {}).get("q") or []        # v1.10.0：选上的词里已经有题目的，开始时就跳过了，记一笔汇报
        if sk:
            log("已经有题目，跳过 %d 个（不重出）：%s" % (len(sk), "、".join(sk[:40]) + ("…" if len(sk) > 40 else "")), tid)
        if "chuti" in steps:
            need = self.pick(10 ** 6, only=set(words))
            have = [w for w in words if w not in need]
            if have:
                log("这些词已经有题目，不重出：%s" % "、".join(have[:30]), tid)
            if need:
                x("DELETE FROM manual WHERE word IN (%s)" % ",".join("?" * len(need)), need)
                log("出题：%d 个词" % len(need), tid)
                gs = group_size()
                for i in range(0, len(need), gs):
                    self.check_stop()
                    self.run_group(tid, need[i:i + gs])
                    self.progress(tid, processed=min(i + gs, len(need)), total=len(need), step="出题")
        if "pics" in steps:
            import pics
            log("做视频画面：%d 个词（没有题目的会跳过）" % len(words), tid)
            pics.do_pics(self, tid, {"words": words})

    def do_redo(self, tid, p):
        words = [w for w in (p.get("words") or []) if w]
        if not words:
            words = sorted(manual_words())
        sync()
        words = self.pick(10 ** 6, only=set(words))
        x("DELETE FROM manual WHERE word IN (%s)" % ",".join("?" * len(words)), words) if words else None
        gs = group_size()
        for i in range(0, len(words), gs):
            self.check_stop()
            self.run_group(tid, words[i:i + gs])
            self.progress(tid, processed=min(i + gs, len(words)), total=len(words))

    def ask_parts(self, tid, kind, prompt, words, rnd):
        """手动接力、一份好几个词：网页 AI 交回一轮就给一轮（见 relay_parts）。"""
        self.check_stop()
        self.stage = "%s：一份 %d 个词（%s … %s），等网页 AI 一轮一轮交回" % (kind, len(words), words[0], words[-1])
        AI_LIVE.update(reply="", provider=provider_name(), kind=kind, words=list(words), started=time.time(), done=0.0, prompt_len=len(prompt))
        for t in relay_parts(prompt, words, kind, rnd):
            try:
                x("INSERT INTO calls(task_id,ts,kind,words,prompt,reply,secs,ok,provider) VALUES(?,?,?,?,?,?,?,1,?)",
                  (tid, now(), kind, "、".join(words), prompt if not RELAY.get("parts", 0) > 1 else "（同上一轮）", t, 0, "relay"))
            except Exception:
                pass
            yield t
        AI_LIVE.update(done=time.time())

    def ask(self, tid, kind, prompt, words):
        waits = [30, 60, 120, 300, 600]
        pv = load_cfg().get("provider")
        for i in range(len(waits) + 1):
            self.check_stop()
            t0 = time.time()
            self.stage = "%s：%s … %s（%d 个词）等 AI 回复" % (kind, words[0], words[-1], len(words))
            AI_LIVE.update(reply="", provider=provider_name(), kind=kind, words=list(words), started=t0, done=0.0, prompt_len=len(prompt))
            try:
                rep = ai_complete(prompt, words, on_progress=lambda m: setattr(self, "stage", "%s：%s" % (kind, m)))
                AI_LIVE.update(reply=rep or AI_LIVE.get("reply", ""), done=time.time())
                x("INSERT INTO calls(task_id,ts,kind,words,prompt,reply,secs,ok,provider) VALUES(?,?,?,?,?,?,?,1,?)",
                  (tid, now(), kind, "、".join(words), prompt, rep, round(time.time() - t0, 1), pv))
                return rep
            except Fatal:
                raise
            except Exception as e:
                x("INSERT INTO calls(task_id,ts,kind,words,prompt,reply,secs,ok,error,provider) VALUES(?,?,?,?,?,?,?,0,?,?)",
                  (tid, now(), kind, "、".join(words), prompt, "", round(time.time() - t0, 1), mask(str(e))[:800], pv))
                if self.stop_req:
                    raise Stopped(self.stop_req)
                if i == len(waits):
                    raise Fatal("AI 连续 %d 次出错，最后一次：%s" % (i + 1, str(e)[:300]))
                log("AI 出错（%s），%d 秒后重试" % (str(e).split("\n")[0][:160], waits[i]), tid)
                self.sleep(waits[i])

    def run_group(self, tid, words):
        cfg = load_cfg()
        b, g = next_group_label()
        label = "题目第 %d 批第 %d 组" % (b, g)
        ver = STATE["version"]
        attr = {"mock": "模拟 AI（测试）", "api": "%s（接口·单词工作台）" % cfg["api"].get("model", "接口 AI"),
                "relay": "网页 AI 手动接力（单词工作台）"}.get(
            cfg.get("provider"), cfg.get("attribution"))
        log("%s：%s … %s（%d 个词）" % (label, words[0], words[-1], len(words)), tid)
        saved, fixed, issues = [], [], []
        bad = {}                       # word -> (lines, errors)
        tries = {w: 0 for w in words}
        gid = x("INSERT INTO groups(task_id,label,words,ts,provider) VALUES(?,?,?,?,?)",
                (tid, label, json.dumps(words, ensure_ascii=False), now(), cfg.get("provider")))

        def judge(batch, got, rnd):
            for w in batch:
                lines = got.get(w, [])
                tries[w] += 1
                qs, errs = check(w, lines)
                if not errs:
                    save_word(w, qs, ver, attr)
                    saved.append(w)
                    if rnd:
                        fixed.append(w)
                    bad.pop(w, None)
                else:
                    bad[w] = (lines, errs)

        try:
            cs = max(1, int(cfg["relayChunk"] if cfg.get("provider") == "relay" else cfg["chunkSize"]))
            relay = cfg.get("provider") == "relay"
            queue = list(words)
            while queue:
                if relay:                  # v1.11.2：每一份开始时按现在的设置分（黄框里改了，下一份就按新的）
                    cs, rq = relay_size("q")
                chunk, queue = queue[:cs], queue[cs:]
                if relay:                  # v1.10.9：一份好几个词，网页 AI 写完一轮传一轮，收到一轮判一轮
                    pend = list(chunk)
                    while pend:
                        RELAY_QLEFT[0] = len(queue)
                        for part in self.ask_parts(tid, "出题", build_prompt(pend), pend, min(rq, len(pend))):
                            got, iss = parse_reply(part, pend)
                            issues += iss
                            gw = [w for w in pend if got.get(w)]
                            if not gw:
                                RELAY["hint"] = "交回的这个文件里没有这一批还没做的词（要有 @单词 那一行）"
                                continue
                            judge(gw, got, 0)
                            for w in gw:
                                relay_word(w, w in saved, "" if w in saved else "；".join(bad.get(w, ([], ["没过"]))[1])[:80])
                                pend.remove(w)
                        why = RELAY.get("endReason")
                        if pend and why in ("newchat", "resize"):
                            cs, rq = relay_size("q")
                            if len(pend) > cs:     # 一批改小了：多出来的放回去，排到下一份
                                queue, pend = pend[cs:] + queue, pend[:cs]
                                chunk = [w for w in chunk if w not in queue]
                            elif len(pend) < cs and queue:     # 一批改大了：后面排着的拿进来
                                more, queue = queue[:cs - len(pend)], queue[cs - len(pend):]
                                pend += more
                                chunk += more
                            log("  剩下的 %d 个另开对话：出一份新的提示词" % len(pend), tid)
                            continue
                        for w in pend:          # 你点了「剩下的先跳过」
                            tries[w] = tries.get(w, 0)
                            bad[w] = ([], ["这一批交回以前你点了「剩下的先跳过」"])
                            relay_word(w, False, "跳过了")
                        pend = []
                    log("  %s … %s：过了 %d 个，没过 %d 个" % (chunk[0], chunk[-1], len([w for w in chunk if w in saved]),
                                                         len([w for w in chunk if w in bad])), tid)
                    continue
                rep = self.ask(tid, "出题", build_prompt(chunk), chunk)
                got, iss = parse_reply(rep, chunk)
                issues += iss
                judge(chunk, got, 0)
                nb = [w for w in chunk if w in bad]
                relay_result(not nb, "过了 %d 个，没过 %d 个%s" % (len(chunk) - len(nb), len(nb), ("：" + "；".join(
                    "%s %s" % (w, "；".join(bad[w][1])[:80]) for w in nb[:3])) if nb else ""))
                log("  %s … %s：过了 %d 个，没过 %d 个" % (chunk[0], chunk[-1], len([w for w in chunk if w in saved]),
                                                     len([w for w in chunk if w in bad])), tid)
            for rnd in range(1, int(cfg["fixRounds"]) + 1):
                if not bad:
                    break
                todo = list(bad)
                for i in range(0, len(todo), cs):
                    chunk = todo[i:i + cs]
                    rep = self.ask(tid, "改错第 %d 轮" % rnd, build_fix_prompt([(w,) + bad[w] for w in chunk]), chunk)
                    got, iss = parse_reply(rep, chunk)
                    issues += iss
                    judge(chunk, got, rnd)
                    nb = [w for w in chunk if w in bad]
                    relay_result(not nb, "过了 %d 个，没过 %d 个%s" % (len(chunk) - len(nb), len(nb), ("：" + "；".join(
                        "%s %s" % (w, "；".join(bad[w][1])[:80]) for w in nb[:3])) if nb else ""))
                log("  改错第 %d 轮后还有 %d 个没过" % (rnd, len(bad)), tid)
        finally:
            for w, (lines, errs) in bad.items():
                x("INSERT OR REPLACE INTO manual(word,errors,draft,attempts,ts,source) VALUES(?,?,?,?,?,?)",
                  (w, json.dumps(errs, ensure_ascii=False), "\n".join(lines), tries.get(w, 0), now(), label))
            self.finish_group(tid, gid, label, words, saved, fixed, list(bad), issues, attr)

    def finish_group(self, tid, gid, label, words, saved, fixed, failed, issues, attr):
        cfg = load_cfg()
        if not saved:              # 一个都没存：README 和仓库都不动，没过的已经在待人工里
            x("UPDATE groups SET saved='[]', failed=?, fixed='[]' WHERE id=?", (json.dumps(failed, ensure_ascii=False), gid))
            log("%s：这一组一个都没过，没记 README、没提交" % label, tid)
            return
        attempted = [w for w in words if w in saved or w in failed]
        notes = []
        notes.append("体检全部 0 个问题" if not failed else "体检通过的都存了")
        if fixed:
            notes.append("%s 体检没过、改过再存" % "、".join(fixed))
        if failed:
            notes.append("%s 改了 %d 次仍没过，没存，留待人工" % ("、".join(failed), int(cfg["fixRounds"])))
        notes.append("出题：" + attr)
        added = 0
        with REPO_LOCK:
            if cfg.get("recordIssues", True) and cfg.get("provider") != "mock":
                for it in issues:
                    if readme_add_issue(it):
                        added += 1
                        x("INSERT INTO issues(word,text,ts,task_id) VALUES(?,?,?,?)", (it.split("：")[0], it, now(), tid))
            done = stats().get("words", 0)
            readme_log(label, attempted[0], attempted[-1], len(saved), "；".join(notes), done)
            cid = commit_pending("词库：%s（%s … %s %d 个词）；累计 %d 个词" % (
                label, attempted[0], attempted[-1], len(saved), done))
        pushed = 0
        if cfg.get("autoPush", True) and cid:
            try:
                log(push(), tid)
                pushed = 1
            except Exception as e:
                log("上传没成功（%s），提交留在本地，下次上传时一起传" % str(e)[:200], tid)
        x("UPDATE groups SET saved=?, failed=?, fixed=?, commit_id=?, pushed=? WHERE id=?",
          (json.dumps(saved, ensure_ascii=False), json.dumps(failed, ensure_ascii=False),
           json.dumps(fixed, ensure_ascii=False), cid, pushed, gid))
        log("%s 收尾：存了 %d 个，待人工 %d 个，记了 %d 处总表问题，提交 %s%s" % (
            label, len(saved), len(failed), added, cid or "无", "，已上传" if pushed else ""), tid)


RUNNER = Runner()
