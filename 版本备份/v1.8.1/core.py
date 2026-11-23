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
    "relayChunk": 25,            # 手动接力时一次给几个词（你要复制粘贴，所以一次多给一些）
    "relayUrl": "https://zd87.com/ai-fleet/claude",
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
    return out


def save_cfg(patch):
    c = load_cfg()
    for k, v in (patch or {}).items():
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
FIELDS = ["批次", "序号", "单词", "初中含义", "含义", "考点", "辨析", "拆分", "组合 → 现在的含义"]


def load_table():
    p = REPO / STATE["xlsx"] if STATE.get("xlsx") else None
    if not p or not p.exists():
        raise Fatal("总表文件不在：%s" % p)
    st = p.stat()
    key = (str(p), st.st_size, int(st.st_mtime))
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
        rec.update({"总表版本": version, "题目": dict(zip(L.COLS, cells), 答案=daan), "题目原稿": qs,
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
_RELAY_LOCK = threading.Lock()


# ─────── 手动接力 · 收件箱：网页 AI 自己把回复传到 GitHub ───────
INBOX_SCRIPT = r"""import base64, json, os, urllib.request, urllib.error
TOKEN = "%(token)s"
REPO = "%(repo)s"
BRANCH = "%(branch)s"
PATH = "%(path)s"
FILE = "reply.txt"   # 你把回复写进的文件；放在别处就改成那个路径
for d in ("", "/home/claude/", "/mnt/user-data/outputs/", "/tmp/"):
    if os.path.exists(d + FILE):
        FILE = d + FILE
        break
text = open(FILE, encoding="utf-8").read().replace(TOKEN, "***")   # 令牌别跟着传上去
assert "%(end)s" in text, "文件里没有最后一行 %(end)s：先把回复写完整"
url = "https://api.github.com/repos/%%s/contents/%%s" %% (REPO, PATH)
H = {"Authorization": "Bearer " + TOKEN, "Accept": "application/vnd.github+json", "User-Agent": "wordsvideo-relay"}
body = {"message": "接力回复 " + PATH, "content": base64.b64encode(text.encode("utf-8")).decode(), "branch": BRANCH}
try:
    with urllib.request.urlopen(urllib.request.Request(url + "?ref=" + BRANCH, headers=H), timeout=60) as r:
        body["sha"] = json.load(r)["sha"]
except urllib.error.HTTPError as e:
    if e.code != 404:
        raise
req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=H, method="PUT")
try:
    with urllib.request.urlopen(req, timeout=120) as r:
        print("上传好了", r.status, PATH, len(text), "字")
except urllib.error.HTTPError as e:
    print("上传失败", e.code, e.read().decode("utf-8", "replace")[:300])
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


def inbox_prompt(path):
    ib = inbox_cfg()
    script = INBOX_SCRIPT % {"token": ib["token"], "repo": ib["repo"], "branch": ib["branch"] or "main",
                             "path": path, "end": END}
    return ("【写完以后：你自己把回复上传到 GitHub，不用在聊天里贴全文】\n"
            "1. 把上面要求的完整回复（格式完全一样，最后一行 %s）写进文本文件 reply.txt（用你的建文件工具）。\n"
            "2. 用代码执行工具运行下面这段 Python（只用标准库），它会把 reply.txt 传到 GitHub：\n"
            "```python\n%s```\n"
            "3. 看到“上传好了”以后，在聊天里只回一行：已上传 %s。不要在聊天里再写一遍全文。\n"
            "4. 要是没有代码执行工具、或者上传失败了：就照常把完整回复直接写在聊天里（最后一行 %s），并说明上传失败的原因。"
            % (END, script, path, END))


def inbox_fetch(path):
    """看收件箱里有没有这个文件：有就返回 (全文, sha)，没有返回 None。"""
    ib = inbox_cfg()
    q = "/repos/%s/contents/%s?ref=%s" % (ib["repo"], urllib.parse.quote(path), urllib.parse.quote(ib["branch"] or "main"))
    st, d = _gh("GET", q, ib["token"])
    if st == 404:
        return None
    if st != 200:
        raise RuntimeError("看收件箱出错（%s）：%s" % (st, str(d.get("message", ""))[:120]))
    raw = d.get("content") or ""
    if raw:
        text = base64.b64decode(raw).decode("utf-8", "replace")
    else:                                   # 超过 1 MB：接口不给内容，走下载地址
        req = urllib.request.Request(d.get("download_url") or "", headers={"Authorization": "Bearer " + ib["token"],
                                                                            "User-Agent": "chuti-studio"})
        with urllib.request.urlopen(req, timeout=60) as r:
            text = r.read().decode("utf-8", "replace")
    return text, d.get("sha", "")


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
    if "【做画面】" in t or "【改软件】" in t or "【出题规矩】" in t:     # 复制的是提示词本身
        return False
    return any(("@" + w) in t or ("＠" + w) in t for w in words) or '"pics"' in t


def relay_wait(prompt, words):
    """手动接力：提示词放进剪贴板，等你在网页 AI 里发送；你在网页里点“复制”它的回复，软件看到就自己接着做
    （也可以把回复粘到软件里点「交回给软件」）。最多等 12 小时。"""
    if set(words) <= RELAY_SKIP:            # 这批你点了跳过：改错轮也不再问
        return ""
    RELAY_SKIP.clear()
    import clip
    cfg = load_cfg()
    use_clip = clip.WIN and cfg.get("relayClipboard", True)
    ibox = inbox_on(cfg)
    ib0 = inbox_cfg(cfg)
    if not ibox and cfg.get("provider") == "relay" and ib0.get("enabled") and ib0["token"]:
        log("收件箱令牌像是万能令牌，没写进提示词（这一批照旧要你点「复制」）：「⚙ 设置」里换成「收件箱用」小令牌，点「检测收件箱」",
            (RUNNER.task or {}).get("id"))
    ipath = ""
    if ibox:      # 每一批一个新文件名，旧回复不会被当成这一批的
        ipath = "%s/%s-%s.txt" % (inbox_cfg(cfg)["dir"], time.strftime("%Y%m%d-%H%M%S"), os.urandom(3).hex())
        prompt = prompt.rstrip() + "\n\n" + inbox_prompt(ipath)
    with _RELAY_LOCK:
        RELAY.update(id=RELAY["id"] + 1, status="等你操作", prompt=prompt, words=list(words), kind=AI_LIVE.get("kind", ""),
                     reply="", ts=time.time(), copied=False, hint="", clip=use_clip, inbox=ipath)
        rid = RELAY["id"]
    tid = (RUNNER.task or {}).get("id")
    after = ("写完它会自己把回复传到收件箱 %s，软件看到就接着做" % ipath) if ibox else "写完点它回复下面的「复制」，软件会自己接着做"
    if use_clip and clip.set_text(prompt):
        RELAY["copied"] = True
        log("提示词已经放进剪贴板（%s … %s，%d 个词）：到网页 AI 里粘贴、发送；%s" % (words[0], words[-1], len(words), after), tid)
    else:
        log("要你操作：复制提示词到网页 AI 发送（%s … %s，%d 个词）；%s" % (words[0], words[-1], len(words), after), tid)
    clip.beep()
    last = clip.seq() if use_clip else 0
    poll = max(5, int(inbox_cfg(cfg).get("pollSec") or 15))
    next_ib, ib_err = time.time() + poll, 0
    end = time.time() + 12 * 3600
    try:
        while time.time() < end:
            if ibox and time.time() >= next_ib:
                next_ib = time.time() + poll
                try:
                    got = inbox_fetch(ipath)
                    ib_err = 0
                except Exception as e:
                    got = None
                    ib_err += 1
                    if ib_err in (1, 20):
                        log("看收件箱出错（%s），过一会儿再看" % mask(str(e))[:160], tid)
                if got:
                    t, sha = got
                    if _looks_reply(t, words):
                        with _RELAY_LOCK:
                            if RELAY["id"] == rid and RELAY["status"] == "等你操作":
                                RELAY.update(status="交回了", reply=t, hint="")
                        log("网页 AI 把回复传到收件箱了（%s，%d 字），接着做" % (ipath, len(t)), tid)
                        inbox_delete(ipath, sha)
                        continue
                    RELAY["hint"] = "收件箱里的回复不完整（没有最后一行 ZBQ-END，或者没提到这批词）：在网页里叫它写完整再传一次"
            if RUNNER.stop_req:
                raise Stopped(RUNNER.stop_req)
            with _RELAY_LOCK:
                if RELAY["id"] == rid and RELAY["status"] == "交回了":
                    AI_LIVE["reply"] = RELAY["reply"]
                    return RELAY["reply"]
                if RELAY["id"] == rid and RELAY["status"] == "跳过":
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
        if len((reply or "").strip()) < 50:
            return False, "交回来的太短了：要把网页 AI 的整段回复都复制过来"
        RELAY.update(status="交回了", reply=reply)
    return True, "收到了，程序在检查"


def provider_name(cfg=None):
    cfg = cfg or load_cfg()
    pv = cfg.get("provider", "web")
    if pv == "api":
        return "接口 AI：%s（%s）" % (cfg["api"].get("model") or "?", re.sub(r"^https?://", "", cfg["api"].get("baseUrl", "")).split("/")[0])
    if pv == "mock":
        return "模拟 AI（只测流程，存的是假题）"
    if pv == "relay":
        return "手动接力（你在网页 AI 里粘贴提示词、把回复交回来）"
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
KIND_NAMES = {"words": "做指定的词", "pics": "做视频画面", "selfedit": "改软件", "chuti": "出题", "redo": "重做待人工的词", "push": "上传到 GitHub", "sync": "同步仓库"}


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
        x("UPDATE tasks SET status='排队' WHERE status='运行中'")      # 上次没跑完的（软件被关掉）接着排队
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
            words = self.pick(min(int(load_cfg()["groupSize"]), left))
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
        if "chuti" in steps:
            need = self.pick(10 ** 6, only=set(words))
            have = [w for w in words if w not in need]
            if have:
                log("这些词已经有题目，不重出：%s" % "、".join(have[:30]), tid)
            if need:
                x("DELETE FROM manual WHERE word IN (%s)" % ",".join("?" * len(need)), need)
                log("出题：%d 个词" % len(need), tid)
                gs = int(load_cfg()["groupSize"])
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
        gs = int(load_cfg()["groupSize"])
        for i in range(0, len(words), gs):
            self.check_stop()
            self.run_group(tid, words[i:i + gs])
            self.progress(tid, processed=min(i + gs, len(words)), total=len(words))

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
            for i in range(0, len(words), cs):
                chunk = words[i:i + cs]
                rep = self.ask(tid, "出题", build_prompt(chunk), chunk)
                got, iss = parse_reply(rep, chunk)
                issues += iss
                judge(chunk, got, 0)
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
