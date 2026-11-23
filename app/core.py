# -*- coding: utf-8 -*-
"""单词工作台 · 核心
仓库副本、总表、索引、体检、出题流水线、任务队列和定时都在这里。界面（server.py）只调这里的函数；视频在 video.py。

数据以 GitHub 仓库 wordsvideo 为准：软件在 data/repo 里放一份「词库」「引擎」「素材」的副本，
出好的题按仓库原来的格式存进 词/<首字母>/<单词>.json、更新 索引.tsv、在 README 进度表记一行，然后提交上传。
体检用的是仓库里 工具/lianxi.py 的正本，规矩和范例从 出题技能/zongbiao-questions.skill 里读。
"""
import base64, datetime, importlib, json, os, pickle, random, re, sqlite3, subprocess, sys
import threading, time, traceback, urllib.request, zipfile
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
    t = load_cfg().get("githubToken") or ""
    s = str(s)
    if t:
        s = s.replace(t, "***")
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
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", LC_ALL="C.UTF-8")
    r = subprocess.run(cmd, cwd=str(cwd or REPO), capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=timeout, env=env, creationflags=NOWIN)
    if check and r.returncode:
        raise Fatal("git %s 失败：%s" % (" ".join(args[:2]), mask((r.stderr or r.stdout).strip()[-800:])))
    return r


def net_git(*args, **kw):
    """要连 GitHub 的 git 命令：连不上就换一种网络（有代理→直连，没代理→不变）再试一次。"""
    try:
        return git(*args, **kw)
    except Fatal as e:
        px = load_cfg().get("gitProxy")
        if px and any(k in str(e) for k in NET_ERR):
            log("GitHub 走代理 %s 连不上，改成直连再试" % px)
            return git(*args, proxy="", **kw)
        raise


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


def _latest_xlsx():
    vers = []
    for p in git("ls-tree", "-d", "--name-only", "HEAD", TABLE_DIR + "/").stdout.splitlines():
        m = re.fullmatch(TABLE_DIR + r"/第(.+)版", p.strip())
        if m and cn2int(m.group(1)) > 0:
            vers.append((cn2int(m.group(1)), p.strip()))
    for n, p in sorted(vers, reverse=True):
        files = [f for f in git("ls-tree", "--name-only", "HEAD", p + "/").stdout.splitlines()
                 if re.search(r"/2词源拆分总表.*\.xlsx$", f)]
        if files:
            return p.split("/")[-1], files[0]
    raise Fatal("仓库「%s」里没找到 第…版/2词源拆分总表*.xlsx" % TABLE_DIR)


def _sparse(xlsx):
    pats = ["/词库/", "/引擎/", "/素材/"]
    for f in git("ls-tree", "-r", "--name-only", "HEAD", D + "/").stdout.splitlines():
        stem = os.path.splitext(os.path.basename(f))[0].lower()
        if stem.split(".")[0] in RESERVED:            # Windows 不能有叫 con 的文件：这类文件不放到磁盘上
            pats.append("!/" + f)
    git("sparse-checkout", "set", "--no-cone", *pats)


STATE = {"repo": "未准备", "version": "", "xlsx": "", "repoError": "", "aligned": None}


def ensure_repo():
    """第一次：克隆稀疏副本（只要「总表视频细节数据」和最新总表）。之后：同步到 GitHub 最新。"""
    with REPO_LOCK:
        cfg = load_cfg()
        if not (REPO / ".git").exists():
            STATE["repo"] = "正在克隆仓库（第一次要一两分钟）"
            log("克隆仓库 %s → %s" % (cfg["repoUrl"], REPO))
            if REPO.exists():
                import shutil
                shutil.rmtree(REPO, ignore_errors=True)
            net_git("clone", "--filter=blob:none", "--no-checkout", "--depth", "1", "--branch", cfg["branch"],
                    "--config", "core.protectNTFS=false", "--config", "core.autocrlf=false",
                    "--config", "core.longpaths=true", cfg["repoUrl"], str(REPO), cwd=DATA, auth=True)
            ver, xlsx = _latest_xlsx()
            _sparse(xlsx)
            git("checkout", "-f", cfg["branch"])
        sync()


def pending_changes():
    if not (REPO / ".git").exists():
        return 0
    out = git("status", "--porcelain", "--", "词库", check=False).stdout
    return len([l for l in out.splitlines() if l.strip()])


def commit_pending(msg):
    with REPO_LOCK:
        git("add", "-A", "--", "词库")
        if git("diff", "--cached", "--quiet", check=False).returncode == 0:
            return ""
        git("commit", "-q", "-m", msg)
        return git("rev-parse", "--short", "HEAD").stdout.strip()


def sync():
    """拉 GitHub 最新：本地没提交的先提交，本地没上传的提交放到最新版本后面；再核对总表和索引。"""
    with REPO_LOCK:
        cfg = load_cfg()
        br = cfg["branch"]
        STATE["repo"] = "正在同步"
        if pending_changes():
            commit_pending("词库：人工修改、视频登记（单词工作台）")
        net_git("fetch", "-q", "origin", br, auth=True)
        ahead = int(git("rev-list", "--count", "origin/%s..HEAD" % br).stdout.strip() or 0)
        behind = int(git("rev-list", "--count", "HEAD..origin/%s" % br).stdout.strip() or 0)
        if behind and ahead:
            r = git("rebase", "origin/" + br, check=False)
            if r.returncode:
                git("rebase", "--abort", check=False)
                STATE["repo"] = "要人工处理"
                raise Fatal("本地有 %d 个没上传的提交，和 GitHub 上别人的新提交冲突（多半是云端也在出题）。"
                            "请先停掉另一边，再在设置里点「重新克隆仓库」。" % ahead)
        elif behind:
            git("merge", "-q", "--ff-only", "origin/" + br)
        ver, xlsx = _latest_xlsx()
        if xlsx != STATE.get("xlsx"):
            _sparse(xlsx)
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
        return bool(d.get("permissions", {}).get("push")), ("有写权限" if d.get("permissions", {}).get("push") else "只有读权限，不能上传")
    except Exception as e:
        return False, "检测失败：%s" % str(e)[:120]


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
    if os.path.splitext(slug)[0].lower() in RESERVED:
        raise Fatal("%s 是 Windows 的保留文件名，存不了，请用云端技能出这个词" % slug)
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


def search_words(text="", status="", page=1, size=60):
    _, rows = read_index()
    man = manual_words()
    seen, out = set(), []
    t = (text or "").strip().lower()
    for r in rows:
        st = "manual" if (r[4] == "缺" and r[2] in man) else {"细节数据有": "done", "缺": "missing"}.get(r[4], "orig")
        if status and st != status:
            continue
        if t and t not in r[2].lower() and t not in r[3]:
            continue
        out.append({"批次": r[0], "序号": r[1], "word": r[2], "meaning": r[3], "status": st})
    n = len(out)
    return {"total": n, "page": page, "items": out[(page - 1) * size: page * size]}


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


def ai_complete(prompt, words, on_progress=None):
    cfg = load_cfg()
    pv = cfg.get("provider", "web")
    if pv == "mock":
        return mock_reply(prompt, words)
    if pv == "api":
        a = cfg["api"]
        url = a["baseUrl"].rstrip("/")
        url = url + ("/chat/completions" if not url.endswith("/chat/completions") else "")
        body = json.dumps({"model": a["model"], "messages": [{"role": "user", "content": prompt}],
                           "temperature": a.get("temperature", 0.3), "max_tokens": a.get("maxTokens", 8000)}).encode()
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json",
                                                               "Authorization": "Bearer " + a.get("key", "")})
        with urllib.request.urlopen(req, timeout=a.get("timeout", 600)) as r:
            d = json.loads(r.read().decode("utf-8"))
        return d["choices"][0]["message"]["content"]
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
KIND_NAMES = {"chuti": "出题", "redo": "重做待人工的词", "push": "上传到 GitHub", "sync": "同步仓库"}


def add_task(kind, params=None, run_after=0, title=""):
    params = params or {}
    if not title:
        if kind == "chuti":
            title = "出题 %s 个词" % (params.get("count") or "全部剩下的")
        elif kind == "redo":
            title = "重做待人工的 %d 个词" % len(params.get("words") or [])
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
        if t["kind"] in ("chuti", "redo") and not in_window():
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
            if not in_window():
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
            try:
                rep = ai_complete(prompt, words, on_progress=lambda m: setattr(self, "stage", "%s：%s" % (kind, m)))
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
        attr = cfg.get("attribution") if cfg.get("provider") != "mock" else "模拟 AI（测试）"
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
            cs = max(1, int(cfg["chunkSize"]))
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
