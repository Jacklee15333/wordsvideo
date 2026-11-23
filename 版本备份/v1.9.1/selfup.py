# -*- coding: utf-8 -*-
"""单词工作台 · 版本、更新、改写软件

· 版本号在 app/VERSION；每次发布新版本：旧的整个 app 文件夹先备份到「版本备份/v旧版本号/」，
  版本号加一，在 CHANGELOG.md 最上面记一条，提交并上传。软件里点「改写」和 AI（Claude）在仓库里直接改，都照这个规矩。
· 检查更新：看 GitHub 上 app/VERSION 比本机新没有；更新＝在软件文件夹里 git pull。
· 改写：在软件里写要改什么 → 网页 AI 先挑要看的文件、再写改动（找到原文 → 换成新文） → 程序检查语法 →
  你看改动、点「应用并发布」→ 备份、改、升版本、上传。重开软件生效。
软件文件夹要是从 GitHub 克隆下来的（GitHub Desktop 克隆的就是），才能检查更新和发布。"""
import datetime, difflib, json, os, re, shutil, subprocess, sys, time
from pathlib import Path
import core as C

ROOT, APPD = C.ROOT, C.APP
BACKUP = "版本备份"
SKIP = {"memory", "__pycache__"}
EDITABLE = re.compile(r"^(app/[\w./-]+\.(py|html|css|js|svg|txt)|README\.md|启动\.bat)$")
END = C.END


def version():
    try:
        return (APPD / "VERSION").read_text(encoding="utf-8").strip()
    except Exception:
        return "0.0.0"


def vt(v):
    return tuple(int(x) for x in re.findall(r"\d+", v or "0")[:3]) or (0,)


def bump(v, part="minor"):
    a = list(vt(v)) + [0, 0, 0]
    a = a[:3]
    if part == "major":
        a = [a[0] + 1, 0, 0]
    elif part == "minor":
        a = [a[0], a[1] + 1, 0]
    else:
        a[2] += 1
    return "%d.%d.%d" % tuple(a)


def is_clone():
    return (ROOT / ".git").exists()


def rg(*args, auth=False, check=True, timeout=600):
    return C.git(*args, auth=auth, check=check, cwd=ROOT, timeout=timeout)


def branch():
    return C.load_cfg().get("branch", "main")


# ═══════════════════════ 检查更新、更新 ═══════════════════════
def check_update():
    out = {"local": version(), "clone": is_clone(), "remote": "", "newer": False, "log": "", "error": ""}
    if not out["clone"]:
        out["error"] = "软件文件夹不是从 GitHub 克隆的（比如是解压的 zip），检查不了更新"
        return out
    try:
        C.net_git("fetch", "-q", "origin", branch(), auth=True, cwd=ROOT, timeout=120)
        r = rg("show", "origin/%s:app/VERSION" % branch(), check=False)
        out["remote"] = r.stdout.strip() if r.returncode == 0 else ""
        out["newer"] = bool(out["remote"]) and vt(out["remote"]) > vt(out["local"])
        out["log"] = rg("show", "origin/%s:CHANGELOG.md" % branch(), check=False).stdout[:4000]
    except Exception as e:
        out["error"] = str(e)[:300]
    return out


def update():
    if not is_clone():
        return False, "软件文件夹不是从 GitHub 克隆的，请到 GitHub 上重新下载"
    dirty = [l for l in rg("status", "--porcelain", check=False).stdout.splitlines() if l.strip()]
    if dirty:
        return False, "软件文件夹里有没提交的改动（%d 处），先在 GitHub Desktop 里提交或放弃，再更新：%s" % (
            len(dirty), "；".join(dirty[:5]))
    r = C.net_git("pull", "-q", "--ff-only", "origin", branch(), auth=True, cwd=ROOT, check=False)
    if r.returncode:
        return False, "更新失败：%s" % C.mask(r.stderr)[-400:]
    return True, "更新好了：现在是 %s。关掉软件窗口、再双击「启动.bat」就用上新版本了" % version()


# ═══════════════════════ 备份、发布 ═══════════════════════
def changelog_add(ver, title, lines):
    p = ROOT / "CHANGELOG.md"
    old = p.read_text(encoding="utf-8") if p.exists() else "# 单词工作台 · 更新记录\n\n每个版本发布前，旧版本整个 app 文件夹备份在「版本备份/v版本号/」。\n"
    head, _, rest = old.partition("\n## ")
    entry = "## v%s（%s）%s\n\n%s\n" % (ver, time.strftime("%Y-%m-%d"), title, "\n".join("- " + l for l in lines if l))
    p.write_text(head.rstrip() + "\n\n" + entry + ("\n## " + rest if rest else ""), encoding="utf-8")


def backup_current():
    """把现在的 app 文件夹整个拷到 版本备份/v现在的版本号/app（已经有就不重复拷）。"""
    v = version()
    dst = ROOT / BACKUP / ("v" + v) / "app"
    if not dst.exists():
        shutil.copytree(str(APPD), str(dst), ignore=shutil.ignore_patterns(*SKIP, "*.pyc"))
    return v


def publish(files, title, lines, part="minor"):
    """files: {相对路径: 新内容}。备份 → 写文件 → 升版本 → 记 CHANGELOG → 提交 → 上传。返回 (成功, 说明)。"""
    if not is_clone():
        return False, "软件文件夹不是从 GitHub 克隆的，改了只能存在本机，没法发布"
    with C.REPO_LOCK:
        old = backup_current()
        for rel, text in files.items():
            if not EDITABLE.match(rel):
                return False, "不许改这个文件：%s" % rel
            p = ROOT / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8", newline="\n" if not rel.endswith(".bat") else "\r\n")
        new = bump(old, part)
        (APPD / "VERSION").write_text(new + "\n", encoding="utf-8")
        changelog_add(new, title, lines + ["旧版本备份在「%s/v%s」" % (BACKUP, old)])
        rg("add", "-A")
        if rg("diff", "--cached", "--quiet", check=False).returncode == 0:
            return False, "没有改动"
        rg("commit", "-q", "-m", "单词工作台 v%s：%s" % (new, title))
        cid = rg("rev-parse", "--short", "HEAD").stdout.strip()
    r = C.net_git("push", "-q", "origin", "HEAD:" + branch(), auth=True, cwd=ROOT, check=False)
    if r.returncode:
        return True, "v%s 已经改好、提交在本机（%s），但上传没成功：%s。可以在 GitHub Desktop 里点 Push" % (
            new, cid, C.mask(r.stderr)[-300:])
    return True, "v%s 发布好了（%s），旧版本备份在「%s/v%s」。关掉软件窗口、再双击「启动.bat」生效" % (new, cid, BACKUP, old)


def backups():
    d = ROOT / BACKUP
    if not d.exists():
        return []
    return sorted([p.name for p in d.iterdir() if p.is_dir()], key=vt, reverse=True)


def rollback(name):
    src = ROOT / BACKUP / name / "app"
    if not src.exists():
        return False, "没有这个备份：%s" % name
    files = {}
    for p in src.rglob("*"):
        if p.is_file() and p.name != "VERSION" and not (set(p.relative_to(src).parts) & SKIP):
            files["app/" + p.relative_to(src).as_posix()] = p.read_text(encoding="utf-8", errors="replace")
    return publish(files, "回退到 %s" % name, ["软件文件内容换回 %s 的样子" % name], part="patch")


# ═══════════════════════ 改写（网页 AI） ═══════════════════════
def app_files():
    out = []
    for p in sorted(APPD.rglob("*")):
        if p.is_file() and not (set(p.relative_to(APPD).parts) & SKIP) and p.suffix in (".py", ".html", ".css", ".js", ".svg"):
            out.append("app/" + p.relative_to(APPD).as_posix())
    return out + ["README.md"]


def outline(rel):
    t = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
    if rel.endswith(".py"):
        items = re.findall(r"^(?:def|class) (\w+)", t, re.M)
    elif rel.endswith(".html"):
        items = re.findall(r'<section id="([\w-]+)"', t) + re.findall(r"(?:async )?function (\w+)", t)
    else:
        items = re.findall(r"^#+ .+$", t, re.M)
    doc = re.search(r'^"""(.+?)(?:\n|""")', t, re.S)
    return "%s（%d 字）%s\n    %s" % (rel, len(t), ("：" + doc.group(1).strip()[:80]) if doc else "", "、".join(items[:80]))


RULES = """规矩：
- 只改完成需求必须改的地方，别的代码一个字不动；别改出题、存盘、体检、git 的已有逻辑，除非需求就是要改它。
- 界面文字用简短的中文；Python 只用标准库（openpyxl、playwright 已经装了）；界面是 app/web/index.html 一个文件（CSS、JS 都在里面），不引用外网的东西。
- 不能出现令牌、密码。
改动的写法（程序按这个格式自动改，请严格照做）：每一处改动写一块——
<<<FILE 文件的相对路径
<<<FIND
原文里要换掉的那几行（一字不差地抄，包括缩进；要在文件里只出现一次，不够独特就多抄几行）
>>>REPLACE
换成的新内容
>>>END
新建文件：FIND 下面空着。一个文件改几处就写几块。所有改动块放在一个代码块里（```text 开头）。
代码块后面写一行“说明：”，接着几行，每行一句话说改了什么（会写进更新记录）。最后单独一行写：""" + END


def _ask(tid, kind, prompt):
    return C.RUNNER.ask(tid, kind, prompt, ["改软件"])


EDIT_RE = re.compile(r"<<<FILE[ \t]+(\S+)[ \t]*\n<<<FIND[ \t]*\n(.*?)>>>REPLACE[ \t]*\n(.*?)>>>END", re.S)


def parse_edits(reply):
    text = (reply or "").replace("\r", "")
    edits = [(f.strip(), a[:-1] if a.endswith("\n") else a, b[:-1] if b.endswith("\n") else b)
             for f, a, b in EDIT_RE.findall(text)]
    m = re.search(r"说明[:：]\s*\n?(.*?)(?:%s|$)" % re.escape(END), text, re.S)
    notes = [re.sub(r"^[-*•\d.、\s]+", "", l).strip() for l in (m.group(1) if m else "").split("\n")]
    return edits, [n for n in notes if n and "```" not in n][:12]


def apply_edits(edits):
    """在内存里改，返回 ({文件: 新内容}, [错误])。"""
    cur, errs = {}, []
    for rel, find, rep in edits:
        rel = rel.strip("`'\" ")
        if not EDITABLE.match(rel):
            errs.append("%s：不许改这个文件（只能改 app 里的 .py/.html/.css/.js/.svg、README.md、启动.bat）" % rel)
            continue
        p = ROOT / rel
        if rel not in cur:
            cur[rel] = p.read_text(encoding="utf-8") if p.exists() else None
        if not find.strip():
            if cur[rel] is not None:
                errs.append("%s：FIND 空着表示新建文件，可这个文件已经有了" % rel)
            else:
                cur[rel] = rep + "\n"
            continue
        if cur[rel] is None:
            errs.append("%s：没有这个文件" % rel)
            continue
        n = cur[rel].count(find)
        if n != 1:
            head = find.strip().split("\n")[0][:80]
            errs.append("%s：要换掉的原文%s（开头是：%s）" % (rel, "找不到，没有一字不差地抄" if n == 0 else "出现了 %d 次，要多抄几行让它独一无二" % n, head))
            continue
        cur[rel] = cur[rel].replace(find, rep)
    return {k: v for k, v in cur.items() if v is not None}, errs


def validate(files):
    errs = []
    for rel, t in files.items():
        if rel.endswith(".py"):
            try:
                compile(t, rel, "exec")
            except SyntaxError as e:
                errs.append("%s 第 %s 行语法错误：%s" % (rel, e.lineno, e.msg))
        elif rel.endswith(".html"):
            if "</html>" not in t or t.count("<script>") != t.count("</script>"):
                errs.append("%s：HTML 不完整（</html> 或 <script> 对不上）" % rel)
            node = shutil.which("node")
            if node:
                js = "\n".join(re.findall(r"<script>(.*?)</script>", t, re.S))
                tmp = C.DATA / "_check.js"
                tmp.write_text("new Function(%s);" % json.dumps(js), encoding="utf-8")
                r = subprocess.run([node, str(tmp)], capture_output=True, text=True, encoding="utf-8", errors="replace",
                                   creationflags=C.NOWIN)
                if r.returncode:
                    errs.append("%s 里的脚本有语法错误：%s" % (rel, (r.stderr.strip().split("\n") or [""])[-1][:200]))
        if re.search(r"github_pat_[A-Za-z0-9_]{20,}|ghp_[A-Za-z0-9]{20,}", t):
            errs.append("%s：里面有令牌，不许写进代码" % rel)
    return errs


def diff_text(files):
    out = []
    for rel, t in files.items():
        p = ROOT / rel
        old = p.read_text(encoding="utf-8").splitlines() if p.exists() else []
        out += list(difflib.unified_diff(old, t.splitlines(), "原来/" + rel, "改后/" + rel, lineterm="", n=2))
    return "\n".join(out)


def do_selfedit(tid, p):
    """任务：按需求让网页 AI 改软件，改好存成“待确认”的改动。"""
    cid = int(p["change"])
    req = C.q("SELECT * FROM changes WHERE id=?", (cid,), one=True)["request"]
    C.x("UPDATE changes SET status='AI 在改' WHERE id=?", (cid,))
    try:
        files = p.get("files") or []
        if not files:
            rep = _ask(tid, "改软件·挑文件", "【改软件】你在帮一位中学英语老师改他自己用的「单词工作台」软件（Python 后台 + 一个网页界面）。\n\n"
                       "他的需求：\n%s\n\n软件的文件（路径、大小、里面的函数或页面）：\n%s\n\n"
                       "先只回答：要完成这个需求，需要看哪几个文件的全文？写一行“FILES: 路径1, 路径2”（越少越好，最多 3 个）。最后单独一行写：%s"
                       % (req, "\n".join(outline(f) for f in app_files()), END))
            m = re.search(r"FILES[:：]\s*(.+)", rep or "")
            files = [f.strip(" `'\"") for f in re.split(r"[,，、\s]+", m.group(1)) if f.strip(" `'\"")] if m else []
            files = [f for f in files if f in app_files()][:3] or ["app/web/index.html"]
        C.log("改软件：AI 要看 %s" % "、".join(files), tid)
        body = "\n\n".join("===== %s 全文 =====\n%s" % (f, (ROOT / f).read_text(encoding="utf-8")) for f in files)
        prompt = ("【改软件】你在帮一位中学英语老师改他自己用的「单词工作台」软件（Python 后台 + 一个网页界面，在 Windows 上跑）。\n\n"
                  "他的需求：\n%s\n\n%s\n\n其他文件（没给全文）：\n%s\n\n%s" % (
                      req, body, "\n".join(outline(f) for f in app_files() if f not in files), RULES))
        rnd = 0
        while True:
            rep = _ask(tid, "改软件" if not rnd else "改软件·修正", prompt)
            edits, notes = parse_edits(rep)
            new, errs = apply_edits(edits) if edits else ({}, ["没找到改动块（<<<FILE … >>>END）"])
            errs += validate(new) if new else []
            if not errs or rnd >= 2:
                break
            rnd += 1
            C.log("改软件：第 %d 次有问题，退回去改：%s" % (rnd, "；".join(errs)[:300]), tid)
            prompt = prompt + "\n\n你上次写的改动有问题，程序没法用：\n- " + "\n- ".join(errs) + \
                "\n请把全部改动重新完整写一遍（还是同样的格式）。"
        st = "待确认" if not errs else "没改成"
        C.x("UPDATE changes SET status=?, files=?, notes=?, diff=?, edits=?, error=? WHERE id=?",
            (st, json.dumps(list(new), ensure_ascii=False), json.dumps(notes, ensure_ascii=False), diff_text(new),
             json.dumps(edits, ensure_ascii=False), "；".join(errs), cid))
        C.log("改软件：%s（%d 个文件）" % (st, len(new)), tid)
        if errs:
            raise C.Fatal("AI 改了 3 次还有问题：%s" % "；".join(errs)[:300])
    except C.Stopped:
        C.x("UPDATE changes SET status='已取消' WHERE id=?", (cid,))
        raise


def apply_change(cid):
    ch = C.q("SELECT * FROM changes WHERE id=?", (cid,), one=True)
    if not ch or ch["status"] != "待确认":
        return False, "这个改动不是“待确认”状态"
    edits = [tuple(e) for e in json.loads(ch["edits"] or "[]")]
    new, errs = apply_edits(edits)          # 按现在的文件重新改一遍（中间软件可能更新过）
    errs += validate(new)
    if errs:
        return False, "现在的文件和 AI 改的时候不一样了，改不上：%s" % "；".join(errs)[:300]
    title = (ch["request"].strip().split("\n")[0])[:40]
    ok, msg = publish(new, title, json.loads(ch["notes"] or "[]") or [ch["request"][:120]])
    C.x("UPDATE changes SET status=? WHERE id=?", ("已发布" if ok else "待确认", cid))
    return ok, msg
