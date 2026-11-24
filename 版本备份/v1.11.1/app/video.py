# -*- coding: utf-8 -*-
"""单词工作台 · 视频
真正出片的还是原来的视频技能和批量流水线（在 WSL 的 Ubuntu 里跑）。这里做三件事：
  1. 把仓库「引擎」里的视频技能、本地出片、批量出片脚本和「词库」里的总表同步进 WSL（代替以前的 02_get_repo.sh）；
  2. 装环境（01 系统软件、03 声音模型、04 显卡）放后台跑，界面看进度；
  3. 选词建批次 → 开工 → 看进度 → 做好的视频拷到 D 盘、登记进「词库/视频清单.tsv」。
v1.11.0：出片前检查一项一项打勾（有问题的那一行就能修）；批次能暂停、停止、删除；在跑的批次实时看每个词、电脑忙不忙；做完出汇报。
视频文件很大（一个 20–45 MB），不进 git，只登记。"""
import base64, json, os, re, subprocess, sys, threading, time, traceback
from pathlib import Path
import core as C

NOWIN = C.NOWIN
KIT_WORDS = "引擎/视频/references/kit-7A-U4/words"
KIT_LIST = "引擎/批量出片/lists/7A-U4.tsv"
EXTRA = "词库/画面设置"                    # 以后 AI 做的画面设置放这里：words/<词>.py、<名字>_art.py、清单.tsv
VLIST = "词库/视频清单.tsv"


def vcfg():
    c = C.load_cfg().get("video") or {}
    return {"distro": c.get("distro") or "Ubuntu-24.04", "winDir": c.get("winDir") or r"D:\构词视频",
            "gpu": c.get("gpu", True), "holdQA": c.get("holdQA", False)}


def _dec(b):
    if not b:
        return ""
    if b.count(b"\x00") > len(b) // 4:            # wsl.exe 自己的提示是 UTF-16
        return b.decode("utf-16-le", "replace").replace("\x00", "")
    return b.decode("utf-8", "replace")


def has_wsl():
    return sys.platform == "win32" and (Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32" / "wsl.exe").exists()


def wsl_argv(cmd):
    """交给 wsl.exe 的参数。脚本先转成 base64：wsl.exe 会让 Linux 的默认 shell 先把命令行过一遍，
    直接把脚本当参数传，里面的 $A、$S、$TABLE 这些在脚本开始前就被换成了空的（v1.9.0 起草检查报
    FileNotFoundError: '' 就是这个原因）。base64 里只有字母、数字和 +/=，过几遍 shell 都不会变。"""
    b64 = base64.b64encode(cmd.encode("utf-8")).decode("ascii")
    return ["wsl", "-d", vcfg()["distro"], "-u", "root", "--", "bash", "-lc", "source <(base64 -d <<<%s)" % b64]


def wsl(cmd, timeout=600):
    """在 WSL 里用 root 跑一段 bash 脚本（原样交给 bash，只解释一遍），返回 (返回码, 输出)。"""
    if not has_wsl():
        return 127, "这台电脑没有 WSL（只能在 Windows 上用）"
    try:
        r = subprocess.run(wsl_argv(cmd), capture_output=True, timeout=timeout, creationflags=NOWIN)
        return r.returncode, (_dec(r.stdout) + _dec(r.stderr)).strip()
    except subprocess.TimeoutExpired:
        return 124, "超时（%d 秒）" % timeout


def to_wsl(p):
    p = str(Path(p).resolve())
    m = re.match(r"^([A-Za-z]):[\\/](.*)$", p)
    if m:
        return "/mnt/%s/%s" % (m.group(1).lower(), m.group(2).replace("\\", "/"))
    return p


def q(s):
    return "'" + str(s).replace("'", "'\"'\"'") + "'"


def keepalive():
    """开着一个不占资源的 wsl 进程，WSL 才不会自己关掉（后台出片要它）。"""
    ps = C.REPO / "引擎" / "本地出片" / "scripts" / "windows" / "keepalive.ps1"
    if has_wsl() and ps.exists():
        subprocess.Popen(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps)], creationflags=NOWIN)


# ═══════════════════════ 环境 ═══════════════════════
def env_status():
    out = {"wsl": has_wsl(), "distro": vcfg()["distro"], "winDir": vcfg()["winDir"]}
    if not out["wsl"]:
        out["msg"] = "这台电脑没有 WSL（视频只能在装了 WSL 的 Windows 上做）"
        return out
    rc, t = wsl("""
      echo "skill=$(grep -m1 '^当前 6\\.' ~/skills/word-construction-video/SKILL.md 2>/dev/null | sed 's/：.*//; s/^当前 *//')"
      echo "lw=$([ -f ~/lw/scripts/wsl/common.sh ] && echo 1)"; echo "lwb=$([ -f ~/lwb/scripts/wsl/batch.sh ] && echo 1)"
      echo "models=$(du -sh ~/wordfilm-models 2>/dev/null | cut -f1)"; echo "gpu=$([ -f ~/.wordfilm-gpu.env ] && echo 1)"
      echo "chrome=$(ls -d ~/.cache/ms-playwright/chromium* 2>/dev/null | head -1)"
      echo "ffmpeg=$(command -v ffmpeg)"; echo "node=$(command -v node)"
      grep -E '^(VER|TABLE|SYL)=' ~/.wordfilm-local.env 2>/dev/null
      echo "batches=$(ls ~/wf-batch 2>/dev/null | tr '\\n' ' ')"
      echo "mem=$(free -g | awk '/Mem/{print $2}')G"; echo "cores=$(nproc)"
    """, 60)
    if rc == 127 or "not found" in t.lower() and "skill=" not in t:
        out["msg"] = "WSL 里没有 %s：先按「引擎/本地出片/SKILL.md」第 1 步装好 Ubuntu" % vcfg()["distro"]
        return out
    for line in t.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    out["ready"] = bool(out.get("skill") and out.get("lwb") and out.get("models") and out.get("ffmpeg"))
    return out


# ═══════════════════════ 开始页「③ 出片环境」的检测：一步一步说，每一步马上显示 ═══════════════════════
def wsl_distros():
    """WSL 里装了哪些 Linux（wsl -l -q）。认不出返回 None。"""
    if not has_wsl():
        return None
    try:
        r = subprocess.run(["wsl", "-l", "-q"], capture_output=True, timeout=20, creationflags=NOWIN)
    except Exception:
        return None
    names = [l.strip().strip("\x00").strip() for l in _dec(r.stdout).splitlines()]
    return [n for n in names if n]


def wsl_stream(cmd, on_line, timeout=120):
    """和 wsl() 一样跑一段脚本，不过每输出一行就交给 on_line（检测详情里一行一行实时出来）。返回 (返回码, 最后几行)。"""
    if not has_wsl():
        return 127, "这台电脑没有 WSL"
    import threading
    try:
        pr = subprocess.Popen(wsl_argv(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, creationflags=NOWIN)
    except Exception as e:
        return 126, str(e)
    killed = []
    timer = threading.Timer(timeout, lambda: (killed.append(1), pr.kill()))
    timer.start()
    raw, tail = b"", []
    try:
        for b in iter(pr.stdout.readline, b""):
            raw += b
            if b.count(b"\x00") > len(b) // 4:            # wsl.exe 自己的提示是 UTF-16，留到最后一起解
                continue
            line = b.decode("utf-8", "replace").rstrip("\r\n")
            tail = (tail + [line])[-6:]
            try:
                on_line(line)
            except Exception:
                pass
        rc = pr.wait()
    finally:
        timer.cancel()
    if killed:
        return 124, "超时（%d 秒）" % timeout
    if rc and not "".join(tail).strip():
        tail = _dec(raw).splitlines()[-6:]
    return rc, "\n".join(tail)


ENV_SH = r"""SK=~/skills/word-construction-video/SKILL.md
echo "up=$(uname -r | cut -c1-40)"
echo "skill=$(grep -m1 '^当前 6\.' "$SK" 2>/dev/null | sed 's/：.*//; s/^当前 *//')"
echo "lw=$([ -f ~/lw/scripts/wsl/common.sh ] && echo 1)"
echo "lwb=$([ -f ~/lwb/scripts/wsl/batch.sh ] && echo 1)"
VER=; TABLE=; SYL=; . ~/.wordfilm-local.env 2>/dev/null
echo "VER=$VER"
echo "TABLE=$([ -n "$TABLE" ] && [ -f "$TABLE" ] && echo 1)"
echo "SYL=$([ -n "$SYL" ] && [ -f "$SYL" ] && echo 1)"
echo "ffmpeg=$(command -v ffmpeg)"
echo "node=$(command -v node)"
echo "chrome=$(ls -d ~/.cache/ms-playwright/chromium* 2>/dev/null | head -1)"
echo "models=$(du -sh ~/wordfilm-models 2>/dev/null | cut -f1)"
echo "gpu=$([ -f ~/.wordfilm-gpu.env ] && echo 1)"
echo "mem=$(free -g | awk '/Mem/{print $2}')G"
echo "cores=$(nproc)"
echo "batches=$(ls ~/wf-batch 2>/dev/null | tr '\n' ' ')"
echo "bg=$(for n in boot models gpu; do [ -f ~/lw-logs/$n.pid ] && kill -0 "$(cat ~/lw-logs/$n.pid)" 2>/dev/null && printf '%s ' $n; done)"
echo "end=1"
"""

def sync_engine():
    """仓库「引擎」→ WSL：~/lw（本地出片）、~/lwb（批量出片）、~/skills/word-construction-video（视频技能）、
    ~/kit（视频技能自带的画面设置）、~/kit-extra（词库/画面设置）；总表、音节表拷到 ~/wv-data，写进 ~/.wordfilm-local.env。"""
    src = to_wsl(C.REPO)
    ver = C.STATE.get("version", "")
    table = to_wsl(C.REPO / C.STATE["xlsx"]) if C.STATE.get("xlsx") else ""
    syl = next(iter(sorted((C.REPO / "词库").glob("音节划分*.xlsx"))), None)
    cmd = """set -e
S=%(src)s
rm -rf ~/lw ~/lwb; cp -r "$S/引擎/本地出片" ~/lw; cp -r "$S/引擎/批量出片" ~/lwb
find ~/lw ~/lwb -type f \\( -name '*.sh' -o -name '*.py' \\) -exec sed -i 's/\\r$//' {} +
rm -rf ~/skills/word-construction-video; mkdir -p ~/skills ~/kit-extra/words ~/wv-data
cp -r "$S/引擎/视频" ~/skills/word-construction-video
find ~/skills/word-construction-video -type f \\( -name '*.sh' -o -name '*.py' \\) -exec sed -i 's/\\r$//' {} +
ln -sfn ~/skills/word-construction-video/references/kit-7A-U4 ~/kit
[ -d "$S/%(extra)s" ] && cp -r "$S/%(extra)s/." ~/kit-extra/ || true
touch ~/.wordfilm-local.env
setv() { sed -i "/^$1=/d" ~/.wordfilm-local.env; printf '%%s=%%s\\n' "$1" "$2" >> ~/.wordfilm-local.env; }
cp -f %(table)s ~/wv-data/总表.xlsx; setv TABLE "$HOME/wv-data/总表.xlsx"; setv VER %(ver)s
%(syl)s
echo "✅ 引擎同步好了：$(grep -m1 '^当前 6\\.' ~/skills/word-construction-video/SKILL.md | cut -c1-30)；总表 %(ver)s"
""" % {"src": q(src), "extra": EXTRA, "table": q(table), "ver": q(ver),
       "syl": ("cp -f %s ~/wv-data/音节划分.xlsx; setv SYL \"$HOME/wv-data/音节划分.xlsx\"" % q(to_wsl(syl))) if syl
       else "grep -q '^SYL=' ~/.wordfilm-local.env && [ -f \"$(grep '^SYL=' ~/.wordfilm-local.env | cut -d= -f2-)\" ] "
            "|| echo '⚠ 仓库「词库」里没有音节划分表（音节划分_总词库7869词_细分版.xlsx），读音拆分会缺：请把它放进「词库」文件夹'"}
    rc, t = wsl(cmd, 900)
    C.log("同步引擎进 WSL：%s" % (t.splitlines()[-1] if t else rc))
    return rc == 0, t[-1500:]


SETUP = {"boot": ("装系统软件、字体、浏览器（10–20 分钟）", "bash ~/lw/scripts/wsl/01_bootstrap.sh"),
         "models": ("装声音模型（约 1.6 GB）", "bash ~/lw/scripts/wsl/03_models.sh"),
         "gpu": ("开显卡（可选，约 2.5 GB）", "bash ~/lw/scripts/wsl/04_gpu.sh")}


def setup_start(step, proxy=""):
    if step not in SETUP:
        return False, "不认识的步骤"
    keepalive()
    extra = (" --proxy " + q(proxy)) if (proxy and step == "boot") else ""
    rc, t = wsl("bash ~/lw/scripts/wsl/bg.sh start %s %s%s" % (step, SETUP[step][1], extra), 120)
    return rc == 0, t[-800:]


def setup_status(step):
    rc, t = wsl("bash ~/lw/scripts/wsl/bg.sh status %s 2>&1 | tail -n 25" % step, 60)
    return t


# ═══════════════════════ 哪些词能出片 ═══════════════════════
def pic_words():
    """有画面设置的词 → 画图脚本（逗号隔开）。kit 里的照批量清单，词库/画面设置 里的照它自己的 清单.tsv。"""
    out = {}
    for rel in (KIT_LIST, EXTRA + "/清单.tsv"):
        p = C.REPO / rel
        if not p.exists():
            continue
        for l in p.read_text(encoding="utf-8").splitlines():
            if l.startswith("#") or not l.strip():
                continue
            f = l.split("\t")
            if len(f) >= 2:
                out[f[1].strip()] = f[2].strip() if len(f) > 2 else ""
    for d in (KIT_WORDS, EXTRA + "/words"):
        p = C.REPO / d
        if p.exists():
            for f in p.glob("*.py"):
                out.setdefault(f.stem, "")
    return out


def folder_of(word):
    return word.replace(" ", "_").replace("/", "_")


def videos():
    """登记过的视频：{文件夹名: {批次, 文件, 时间}}"""
    p = C.REPO / VLIST
    out = {}
    if p.exists():
        for l in p.read_text(encoding="utf-8").splitlines()[1:]:
            f = l.split("\t")
            if len(f) >= 5:
                out[f[0]] = {"word": f[0], "batch": f[1], "file": f[2], "size": f[3], "ts": f[4]}
    return out


def scan_videos():
    """把 D 盘出片文件夹里的 mp4 登记进 词库/视频清单.tsv（只登记，不传视频）。"""
    root = Path(vcfg()["winDir"])
    if not root.exists():
        return 0
    have = videos()
    n = 0
    for mp4 in root.rglob("*.mp4"):
        m = re.match(r"^(?:\d+\s+)?(.+?)(?:_精简版|_详解版)?$", mp4.stem)
        name = m.group(1) if m else mp4.stem
        key = name if "详解" not in mp4.stem else name + "（详解版）"
        rel = str(mp4.relative_to(root))
        if have.get(key, {}).get("file") == rel:
            continue
        have[key] = {"word": key, "batch": mp4.parent.name, "file": rel,
                     "size": "%.1f MB" % (mp4.stat().st_size / 1e6), "ts": time.strftime("%Y-%m-%d %H:%M", time.localtime(mp4.stat().st_mtime))}
        n += 1
    if n:
        p = C.REPO / VLIST
        rows = ["单词\t批次\t文件（相对出片文件夹）\t大小\t时间"] + [
            "\t".join([v["word"], v["batch"], v["file"], v["size"], v["ts"]]) for v in sorted(have.values(), key=lambda v: v["ts"])]
        with C.REPO_LOCK:
            p.write_text("\n".join(rows) + "\n", encoding="utf-8")
        C.log("登记了 %d 个新视频（%s）" % (n, VLIST))
    return n


def video_files(word):
    root = Path(vcfg()["winDir"])
    if not root.exists():
        return []
    f = folder_of(word)
    return [str(p.relative_to(root)) for p in root.rglob("*") if p.is_file() and p.suffix in (".mp4", ".jpg", ".png")
            and re.match(r"^(?:\d+\s+)?%s(?:_|\.|$)" % re.escape(f), p.name)]


# ═══════════════════════ 批次 ═══════════════════════
def batch_cmd(args, timeout=300):
    return wsl("bash ~/lwb/scripts/wsl/batch.sh " + " ".join(q(a) for a in args), timeout)


NAME_RE = re.compile(r"[A-Za-z0-9_\-\u4e00-\u9fff]{1,40}")
STG = ("prep", "voice", "render", "check", "deliver")
STG_CN = {"prep": "准备", "voice": "配音", "render": "渲染", "check": "质检", "deliver": "交付", "done": "完成", "skipped": "跳过"}


def _last_line(t, default=""):
    ls = [l.strip() for l in (t or "").splitlines() if l.strip()]
    return ls[-1] if ls else default


def _check_lines(t):
    """batch.sh new 的体检结果：有问题的词 [“词：问题”]，和最后一句“体检：…”。"""
    probs, summ = [], ""
    for l in (t or "").splitlines():
        s = l.strip()
        if s.startswith("体检："):
            summ = s
        elif l.startswith("  ") and s and not s.endswith("OK"):
            f = s.split()
            if len(f) >= 3 and f[0].isdigit():
                m = re.search(r"(没有|重复|序号).*$", s)
                probs.append("%s：%s" % (f[1], m.group(0) if m else s))
    return probs, summ


def batch_new(name, words):
    """建批次。返回 {ok, msg, n, probs（体检有问题的词）, check（体检那一句）, notes（没放进批次的词）}。"""
    if not NAME_RE.fullmatch(name or ""):
        return {"ok": False, "msg": "批次名只用字母、数字、汉字、- 和 _（40 个字以内）"}
    pw = pic_words()
    hasq = {}                                     # v1.10.0：出视频要题目、画面都有：缺哪样就不放进批次，说去哪一步补
    try:
        for r in C.read_index()[1]:
            hasq[r[2]] = hasq.get(r[2], True) and r[4] != "缺"
    except Exception:
        pass
    try:                                          # v1.11.1：画面还没过起草检查的，放进去也会卡在“准备”
        import pics
        unc = pics.unchecked_words()
    except Exception:
        unc = set()
    rows, noq, nopic, nofix = [], [], [], []
    for w in words:
        f = folder_of(w)
        if not hasq.get(w):
            noq.append(w)
            continue
        if f not in pw:
            nopic.append(w)
            continue
        if w in unc:
            nofix.append(w)
            continue
        rows.append("%02d\t%s\t%s\t出自单词工作台" % (len(rows) + 1, f, pw[f]))
    notes = ([("没有题目、没放进批次（先到「出题」）：" + "、".join(noq[:30]))] if noq else []) + \
            ([("没有画面、没放进批次（先到「画面」）：" + "、".join(nopic[:30]))] if nopic else []) + \
            ([("画面还没过起草检查、没放进批次（先点「补画面」）：" + "、".join(nofix[:30]))] if nofix else [])
    if not rows:
        return {"ok": False, "msg": "这些词都还不能出视频：" + "；".join(notes)}
    sync_pics()                                   # v1.11.1：流水线用最新的画面设置
    lst = C.DATA / "batches" / (name + ".tsv")
    lst.parent.mkdir(exist_ok=True)
    lst.write_text("# 单词工作台建的批次\n" + "\n".join(rows) + "\n", encoding="utf-8")
    wl = to_wsl(lst)
    v = vcfg()
    windir = to_wsl(Path(v["winDir"]) / name) if re.match(r"^[A-Za-z]:", v["winDir"]) else v["winDir"]
    rc, t = wsl("mkdir -p ~/wf-lists && tr -d '\\r' < %s > ~/wf-lists/%s.tsv && bash ~/lwb/scripts/wsl/batch.sh new %s ~/wf-lists/%s.tsv"
                % (q(wl), name, q(name), name), 300)
    if rc != 0:
        last = _last_line(t, "建批次出错了（%s）" % rc)
        if "已经有了" in t:
            last = "批次 %s 已经有了：换个名字，或者先在下面把那一批删掉" % name
        elif rc == 127 or "No such file" in t:
            last = "WSL 里还没有出片脚本：先在「出片前先检查」里点「同步到 WSL」"
        return {"ok": False, "msg": C.mask(last)[:300], "notes": notes}
    sets = ["UPLOAD=0", "WIN_DIR=" + windir, "HOLD_QA=%d" % (1 if v["holdQA"] else 0), "GPU=%d" % (1 if v["gpu"] else 0)]
    batch_cmd(["set", name] + sets, 60)
    with _RS["lock"]:
        _runs().pop(name, None)
    probs, summ = _check_lines(t)
    C.log("建了批次 %s：%d 个词%s" % (name, len(rows), "；" + summ if summ else ""))
    return {"ok": True, "msg": "建好了：批次 %s，%d 个词" % (name, len(rows)), "n": len(rows), "probs": probs,
            "check": summ, "notes": notes}


def batch_list():
    rc, t = wsl("for d in ~/wf-batch/*/; do n=$(basename \"$d\"); "
                "r=$([ -f \"$d/pipeline.pid\" ] && kill -0 $(cat \"$d/pipeline.pid\") 2>/dev/null && echo 1 || echo 0); "
                "echo \"$n|$r|$(grep -c . \"$d/list.tsv\")\"; done 2>/dev/null", 60)
    out = []
    for l in t.splitlines():
        f = l.split("|")
        if len(f) == 3 and f[0] != "*":
            out.append({"name": f[0], "running": f[1] == "1", "n": f[2]})
    return out


# ═══════════════════════ v1.11.0：批次的操作——开工 / 暂停 / 停止 / 删除，卡住的词再试、不做 ═══════════════════════
# 暂停、停止都是让流水线停下（正在做的那一步下次从头做，做好的不重做），只是在批次文件夹里留个记号：
#   paused＝暂停（按钮变「继续」）；stopped＝停止（这一批算结束，出汇报；还能「接着做」）。WSL 里的脚本不用改，不用重新同步
_QUEUE_SH = """python3 - {BD} {OP} {W} {S} <<'PYCMD'
import json, os, sys, time
d, op, w, st = sys.argv[1:5]
os.makedirs(os.path.join(d, "cmd"), exist_ok=True)
open(os.path.join(d, "cmd", str(time.time_ns()) + ".json"), "w", encoding="utf-8").write(json.dumps({"op": op, "word": w, "stage": st}, ensure_ascii=False))
print("QUEUED")
PYCMD
"""
_RETRYALL_SH = """python3 - {BD} <<'PYRA'
import json, os, sys, time
d = sys.argv[1]
s = json.load(open(os.path.join(d, "state.json"), encoding="utf-8"))
os.makedirs(os.path.join(d, "cmd"), exist_ok=True)
n = 0
for w in s.get("words", []):
    m = (w.get("msg") or "").lstrip("⚠❌✅ ")
    if w.get("stage") == "prep" and m.startswith("起草检查没过"):
        continue                                   # 画面的问题：要先补画面，再试也一样
    if w.get("stage") not in ("done", "skipped") and w.get("status") in ("blocked", "failed"):
        n += 1
        open(os.path.join(d, "cmd", str(time.time_ns() + n) + ".json"), "w", encoding="utf-8").write(
            json.dumps({"op": "retry", "word": w["word"], "stage": ""}, ensure_ascii=False))
print("RETRY %d" % n)
PYRA
"""


def _fill(sh, **kw):
    for k, v in kw.items():
        sh = sh.replace("{%s}" % k, v)
    return sh


def batch_op(name, op, word="", stage=""):
    """批次：start 开工 / 继续 / 接着做，pause 暂停，stop 停止，delete 删除，retryall 卡住的都再试一次；
    一个词：retry 再试一次（从卡住的那一步），redo 从头重做，ok 放行，skip 不做了，log 看日志。返回 (成没成, 一句话)。"""
    if not NAME_RE.fullmatch(name or ""):
        return False, "批次名不对"
    if word and (len(word) > 80 or re.search(r"[\x00-\x1f/\\{}]", word)):
        return False, "词不对"
    if stage and stage not in STG_CN.values() and stage not in STG:
        return False, "不认识的步骤：%s" % stage
    stage = STG_CN.get(stage, stage)
    kw = {"BD": '"$HOME/wf-batch/%s"' % name, "N": q(name), "NAME": name, "W": q(word), "S": q(stage)}
    B = "bash ~/lwb/scripts/wsl/batch.sh "
    have = "[ -d {BD} ] || { echo '没有批次 {NAME}（可能已经删掉了）'; exit 3; }\n"
    if op in ("start", "retryall"):
        keepalive()
        sh = have + "rm -f {BD}/paused {BD}/stopped\n" + (_RETRYALL_SH if op == "retryall" else "") + \
            B + "set {N} CONFIRMED=1 >/dev/null\n" + B + "start {N}\n"
        rc, t = wsl(_fill(sh, **kw), 120)
        if rc == 0:
            _note_running(_RS["names"] | {name})
            C.log("批次 %s 开工（%s）" % (name, _last_line(t)))
            return True, "开工了：批次 %s 正在生成" % name
        return False, C.mask(_last_line(t, "开工出错了（%s）" % rc))[:300]
    if op in ("pause", "stop"):
        mark, other = ("paused", "stopped") if op == "pause" else ("stopped", "paused")
        sh = have + "touch {BD}/%s; rm -f {BD}/%s\n" % (mark, other) + B + "stop {N}\n"
        rc, t = wsl(_fill(sh, **kw), 90)
        C.log("批次 %s %s：%s" % (name, "暂停" if op == "pause" else "停止", _last_line(t)))
        if rc == 0:
            return True, ("暂停了：批次 %s，点「继续」接着做" if op == "pause" else "停止了：批次 %s，做好的视频都留着") % name
        return False, C.mask(_last_line(t, "没停下来（%s）" % rc))[:300]
    if op == "delete":
        alive = 'kill -0 "$(cat {BD}/pipeline.pid 2>/dev/null)" 2>/dev/null'
        sh = (have + "if %s; then %sstop {N} >/dev/null 2>&1; fi\n" % (alive, B) +
              "if %s; then echo '还在跑、停不下来：等一会儿再删'; exit 4; fi\n" % alive +
              "rm -rf -- {BD} \"$HOME/wf-lists/{NAME}.tsv\"\necho DELETED\n")
        rc, t = wsl(_fill(sh, **kw), 120)
        if rc in (0, 3):
            (C.DATA / "batches" / (name + ".tsv")).unlink(missing_ok=True)
            with _RS["lock"]:
                _runs().pop(name, None)
                _RS["names"].discard(name)
            _runs_save()
            C.log("删掉了批次 %s" % name)
            return True, "删掉了批次 %s（做好的视频还在出片文件夹里）" % name
        return False, C.mask(_last_line(t, "没删掉（%s）" % rc))[:300]
    if op in ("retry", "redo", "ok"):
        if not word:
            return False, "要写词"
        if op == "redo":
            kw["S"] = q("准备")
        act = "ok" if op == "ok" else "retry"
        sh = have + "if [ -f {BD}/paused ] || [ -f {BD}/stopped ]; then\n" + _QUEUE_SH + "else\n" + B + act + " {N} {W} {S}\nfi\n"
        rc, t = wsl(_fill(sh, OP=q(act), **kw), 90)
        what = {"retry": "再试一次", "redo": "从头重做", "ok": "放行"}[op]
        w = word.replace("_", " ")
        if rc != 0:
            return False, C.mask(_last_line(t, "没做成（%s）" % rc))[:300]
        if "QUEUED" in t:
            return True, "记下了：%s %s——点「继续」或「接着做」以后先做它" % (w, what)
        _note_running(_RS["names"] | {name})
        return True, "%s：%s（流水线接着做）" % (what, w)
    if op == "skip":
        if not word:
            return False, "要写词"
        rc, t = wsl(_fill(have + B + "skip {N} {W} " + q("不做了（单词工作台里点的）") + "\n", **kw), 90)
        return rc == 0, ("%s 不做了" % word.replace("_", " ")) if rc == 0 else C.mask(_last_line(t, "没做成"))[:300]
    if op == "log":
        if not word:
            return False, "要写词"
        rc, t = batch_cmd(["log", name, word] + ([stage] if stage else []) + ["60"], 60)
        return rc == 0, C.mask(t)[-8000:]
    old = {"status": ([["status", name, "full"]]), "report": [["report", name]], "check": [["check", name]]}
    if op not in old:
        return False, "不认识的操作"
    outs, rc = [], 0
    for args in old[op]:
        rc, t = batch_cmd(args, 300)
        outs.append(t)
    if op in ("status", "report"):
        try:
            scan_videos()
        except Exception as e:
            C.log("登记视频出错：%s" % e)
    return rc == 0, "\n".join(outs)[-6000:]


# ═══════════════════════ v1.11.0：出片前检查——一项一项打勾，有问题的那一行后面就是修的按钮 ═══════════════════════
EC_ITEMS = (("wsl", "WSL"), ("skill", "视频技能"), ("scripts", "出片脚本"), ("table", "总表"),
            ("syl", "音节划分表"), ("sys", "系统软件"), ("models", "声音模型"), ("gpu", "显卡"), ("windir", "出片文件夹"))
EC_NAME = dict(EC_ITEMS)
FIX_NAME = {"sync": "同步到 WSL", "boot": "装系统软件", "models": "装声音模型", "gpu": "开显卡"}


def _check_windir(put, c):
    wd = Path(c["winDir"])
    try:
        if wd.exists():
            return put("windir", "ok", str(wd))
        if not wd.anchor or Path(wd.anchor).exists():
            return put("windir", "ok", "%s（还没有，出片时自动建）" % wd)
        put("windir", "bad", "%s：这台电脑没有 %s 盘，出片文件夹用不了" % (wd, wd.anchor.rstrip("\\/")))
    except Exception as e:
        put("windir", "bad", "看不了 %s：%s" % (wd, e))


def _probe_env(on_item):
    """一项一项查这台电脑能不能出片（只看，不装、不同步）。查完一项马上 on_item(键, 状态, 一句话, 修的办法)：
    状态 ok 好了 / bad 有问题 / opt 可选、没开 / skip 前面的没好、没法查 / run 正在查；修的办法是 FIX_NAME 里的键或空。
    返回 (结果 {键: (状态, 一句话, 修的办法)}, {bg: 还在装的, got: WSL 里查到的})。"""
    c = vcfg()
    res, got = {}, {}

    def put(k, st, text, fix=""):
        res[k] = (st, text, fix)
        on_item(k, st, text, fix)

    def run(k, text="正在查…"):
        if k not in res:
            on_item(k, "run", text, "")

    def skip_rest(why):
        for k, _ in EC_ITEMS:
            if k not in res and k != "windir":
                put(k, "skip", why)
        _check_windir(put, c)
        return res, {"bg": [], "got": got}

    run("wsl", "看这台电脑有没有 WSL…")
    if not has_wsl():
        put("wsl", "bad", "这台电脑没有 WSL：视频要在装了 WSL 的 Windows 上做（出题、做画面不受影响）")
        return skip_rest("要先有 WSL")
    names = wsl_distros()
    if names is not None and c["distro"] not in names:
        put("wsl", "bad", "WSL 里没有 %s（现在有：%s）：照「引擎/本地出片/SKILL.md」第 1 步装好" % (
            c["distro"], "、".join(names) or "一个都没有"))
        return skip_rest("要先装好 %s" % c["distro"])
    run("wsl", "打开 %s（没开着的话要十几秒）…" % c["distro"])
    try:
        import pics
        rv, red = pics.skill_version()
    except Exception:
        rv, red = "", ""
    tver = C.STATE.get("version") or ""
    try:
        have_syl = any((C.REPO / "词库").glob("音节划分*.xlsx"))
    except Exception:
        have_syl = False

    def on_line(line):
        if "=" not in line:
            return
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip()
        got[k] = v
        if k == "up":
            put("wsl", "ok", "%s 开着" % c["distro"])
            run("skill")
        elif k == "skill":
            m = re.match(r"(\S+?)（(第[^）]+版)）", v)
            wv = m.group(1) if m else v
            if not v:
                put("skill", "bad", "WSL 里还没有视频技能", "sync")
            elif rv and wv != rv:
                put("skill", "bad", "WSL 里是 %s，仓库里是 %s（%s），要同步" % (v, rv, red), "sync")
            else:
                put("skill", "ok", v + ("，和仓库里的一样" if rv else ""))
            run("scripts")
        elif k == "lwb":
            miss = [n for n, x in (("本地出片", got.get("lw")), ("批量出片", v)) if not x]
            if miss:
                put("scripts", "bad", "缺" + "、".join(miss) + "的脚本", "sync")
            else:
                put("scripts", "ok", "本地出片、批量出片的脚本都在")
            run("table")
        elif k == "TABLE":
            ver = got.get("VER", "")
            if not ver:
                put("table", "bad", "WSL 里还没有总表", "sync")
            elif not v:
                put("table", "bad", "WSL 里的总表文件不在了", "sync")
            elif tver and ver != tver:
                put("table", "bad", "WSL 里是%s，词库是%s，要同步" % (ver, tver), "sync")
            else:
                put("table", "ok", ver + ("，和词库一样" if tver else ""))
            run("syl")
        elif k == "SYL":
            if v:
                put("syl", "ok", "在（读音拆分用）")
            elif have_syl:
                put("syl", "bad", "WSL 里没有（每个词都会卡在“准备”），要同步", "sync")
            else:
                put("syl", "bad", "没有（每个词都会卡在“准备”）：把「音节划分_总词库7869词_细分版.xlsx」放进仓库的「词库」文件夹，再检查")
            run("sys")
        elif k == "chrome":
            lack = [n for n, x in (("ffmpeg", got.get("ffmpeg")), ("node", got.get("node")), ("渲染用的浏览器", v)) if not x]
            if lack:
                put("sys", "bad", "没装齐，缺 " + "、".join(lack) + "（装一次 10–20 分钟）", "boot")
            else:
                put("sys", "ok", "ffmpeg、node、渲染用的浏览器都装好了")
            run("models")
        elif k == "models":
            if v:
                put("models", "ok", "装好了（%s）" % v)
            else:
                put("models", "bad", "还没装（约 1.6 GB）", "models")
            run("gpu")
        elif k == "gpu":
            if v:
                put("gpu", "ok", "开好了：配音、画面编码用显卡，快一些")
            else:
                put("gpu", "opt", "没开（可选：不开也能出片，开了快一些，约 2.5 GB）", "gpu")

    rc, tail = wsl_stream(ENV_SH, on_line, 150)
    if "end" not in got:
        put("wsl", "bad", "WSL 没有回应完（%s）：重开电脑，或者在命令行运行 wsl --shutdown 后再检查" % rc)
        return skip_rest("WSL 没回应，没法查")
    put("wsl", "ok", "%s · %s 核 · 内存 %s" % (c["distro"], got.get("cores") or "?", got.get("mem") or "?"))
    for k, _ in EC_ITEMS:
        if k not in res and k != "windir":
            put(k, "skip", "没查到")
    _check_windir(put, c)
    return res, {"bg": (got.get("bg") or "").split(), "got": got}


def _env_verdict(res):
    """查完以后的结论 (状态, 一句话, 去哪儿修)；做画面的起草检查也按这次的结果。"""
    st = lambda k: (res.get(k) or ("",))[0]
    ready = all(st(k) == "ok" for k in ("skill", "scripts", "table", "sys", "models"))
    try:
        import pics
        pics._ENV.update(t=time.time(), ready=ready)
    except Exception:
        pass
    bad = [EC_NAME[k] for k, _ in EC_ITEMS if st(k) == "bad"]
    if bad:
        if st("wsl") == "bad" and not has_wsl():
            return "bad", "这台电脑没有 WSL，出不了片（出题、做画面不受影响）", ""
        return "bad", "有 %d 项要先处理：%s（「出视频」页那一行后面有按钮）" % (len(bad), "、".join(bad)), "video"
    txt = lambda k: (res.get(k) or ("", ""))[1]
    return "ok", "都好了：视频技能 %s；声音模型%s；显卡%s" % (
        txt("skill").split("，")[0], txt("models").replace("装好了", ""), "开了" if st("gpu") == "ok" else "没开（可选）"), ""


def env_check(say):
    """开始页「② 检测」的出片环境：v1.11.0 起和「出视频」页的检查是同一套，一项一句。返回 (状态, 一句话, 去哪儿修)。"""
    def on_item(k, st, text, fix):
        if st in ("ok", "bad", "opt"):
            say("%s：%s" % (EC_NAME[k], text), True if st == "ok" else False if st == "bad" else None)
    res, meta = _probe_env(on_item)
    return _env_verdict(res)


_EC_LOCK = threading.Lock()
EC = {"state": "idle", "run": 0, "started": 0.0, "finished": 0.0, "items": {}, "fix": {}, "verdict": None}


def envchk_start():
    with _EC_LOCK:
        if EC["state"] == "running":
            return {"ok": True, "msg": "正在检查"}
        EC.update(state="running", run=EC["run"] + 1, started=time.time(), finished=0.0, verdict=None,
                  items={k: {"st": "wait", "text": "", "fix": ""} for k, _ in EC_ITEMS})
    threading.Thread(target=_envchk_run, daemon=True, name="envchk").start()
    return {"ok": True, "msg": "开始检查"}


def _envchk_run():
    def on_item(k, st, text, fix):
        with _EC_LOCK:
            EC["items"][k] = {"st": st, "text": C.mask(str(text))[:300], "fix": fix}
    res, meta = {}, {}
    try:
        res, meta = _probe_env(on_item)
        verdict = _env_verdict(res)
    except Exception as e:
        traceback.print_exc()
        on_item("wsl", "bad", "检查本身出错了：%s" % e, "")
        verdict = ("bad", "检查本身出错了：%s" % str(e)[:120], "")
    with _EC_LOCK:
        EC.update(state="done", finished=time.time(), verdict=list(verdict))
        busy = {k for k, f in EC["fix"].items() if f.get("state") == "running"}
    for step in meta.get("bg") or []:            # 软件重开以前点的“装…”还在装：接着看它，装完再查
        if step in SETUP and step not in busy:
            with _EC_LOCK:
                EC["fix"][step] = {"state": "running", "t": time.time(), "msg": "还在装（软件重开以前开始的）", "end": 0.0}
            threading.Thread(target=_fix_run, args=(step, True), daemon=True).start()
    _share_check(res, verdict)
    C.log("出片前检查：%s" % verdict[1])


def _share_check(res, verdict):
    """「② 检测」页的出片环境也换成这次的结果，两页说的一样。"""
    try:
        import check as CK
        t = time.strftime("%H:%M:%S")
        steps = [{"t": t, "msg": C.mask("%s：%s" % (EC_NAME[k], res[k][1]))[:400],
                  "ok": True if res[k][0] == "ok" else False if res[k][0] == "bad" else None} for k, _ in EC_ITEMS if k in res]
        with CK._LOCK:
            it = CK.CHECK["env"]
            if it["state"] != "running":
                it.update(state=verdict[0], summary=C.mask(verdict[1])[:300], fix=verdict[2] or "", steps=steps,
                          started=EC["started"], finished=time.time(), run=it["run"] + 1)
    except Exception:
        pass


def envchk_get():
    now = time.time()
    with _EC_LOCK:
        d = json.loads(json.dumps(EC, ensure_ascii=False))
    d["secs"] = int((d["finished"] or now) - d["started"]) if d["started"] else 0
    d["ago"] = int(now - d["finished"]) if d["finished"] else None
    for f in d["fix"].values():
        f["secs"] = int((f.get("end") or now) - (f.get("t") or now))
    d["names"], d["fixNames"], d["order"] = EC_NAME, FIX_NAME, [k for k, _ in EC_ITEMS]
    d["winDir"] = vcfg()["winDir"]
    return d


def setup_state(step):
    """装东西的后台任务（bg.sh）现在怎么样：{running 还在装, ok 最后一行是 ✅, last 最后一行, unknown 这次没问到}。"""
    rc, t = wsl("bash ~/lw/scripts/wsl/bg.sh status %s 8" % q(step), 60)
    lines = [l.strip() for l in (t or "").splitlines() if l.strip()]
    head = next((l for l in lines if l.startswith("==")), "")
    body = [l for l in lines if not l.startswith("==")]
    if not head and not any("没有" in l and "日志" in l for l in lines):
        return {"running": False, "ok": False, "last": _last_line(t), "unknown": True}
    running = "正在跑" in head
    return {"running": running, "ok": (not running) and bool(body) and body[-1].startswith("✅"), "last": body[-1] if body else head}


def envfix(what):
    if what not in FIX_NAME:
        return {"ok": False, "msg": "不认识要做什么"}
    if what == "sync" and C.STATE.get("repo") not in ("就绪", "索引和总表对不上"):
        return {"ok": False, "msg": "词库还没准备好：等左下角显示“仓库 就绪”再同步"}
    with _EC_LOCK:
        busy = [k for k, f in EC["fix"].items() if f.get("state") == "running"]
        if busy:
            return {"ok": False, "msg": "正在%s，等它做完再点" % FIX_NAME[busy[0]]}
        EC["fix"][what] = {"state": "running", "t": time.time(), "msg": "开始…", "end": 0.0}
    threading.Thread(target=_fix_run, args=(what,), daemon=True, name="envfix-" + what).start()
    return {"ok": True, "msg": "开始" + FIX_NAME[what]}


def _fix_run(what, attach=False):
    def upd(**kw):
        with _EC_LOCK:
            EC["fix"].setdefault(what, {"t": time.time()}).update(**kw)
    try:
        if what == "sync":
            upd(msg="把仓库里的视频技能、出片脚本、总表拷进 WSL（一两分钟）…")
            ok, t = sync_engine()
            upd(state="ok" if ok else "bad", msg=C.mask(_last_line(t, "同步好了" if ok else "同步出错了"))[:300], end=time.time())
        else:
            if not attach:
                ok, t = setup_start(what)
                if not ok:
                    upd(state="bad", msg=C.mask(_last_line(t, "没开始"))[:300], end=time.time())
                    envchk_start()
                    return
                upd(msg="开始装了")
            miss = 0
            while True:
                time.sleep(4)
                st = setup_state(what)
                if st.get("unknown"):
                    miss += 1
                    if miss < 5:
                        continue
                if st["last"]:
                    upd(msg=C.mask(st["last"])[:300])
                if not st["running"]:
                    upd(state="ok" if st["ok"] else "bad", end=time.time())
                    break
                miss = 0
    except Exception as e:
        traceback.print_exc()
        upd(state="bad", msg=str(e)[:300], end=time.time())
    with _EC_LOCK:
        f = dict(EC["fix"].get(what) or {})
    C.log("出片环境：%s %s %s" % (FIX_NAME[what], "✓" if f.get("state") == "ok" else "✗", f.get("msg", "")))
    envchk_start()                                  # 做完再从头检查一遍，那一行就变绿了


# ═══════════════════════ v1.11.0：电脑忙不忙——CPU、内存、显卡 ═══════════════════════
_M = {"lock": threading.Lock(), "cpu": None, "last": None, "t": 0.0, "smi": None, "smi_t": 0.0, "smi_fail": 0}


def _cpu_times():
    """(总时间, 空闲时间)，两次相减算占用。"""
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes

        class FT(ctypes.Structure):
            _fields_ = [("lo", wintypes.DWORD), ("hi", wintypes.DWORD)]
        i, k, u = FT(), FT(), FT()
        if not ctypes.windll.kernel32.GetSystemTimes(ctypes.byref(i), ctypes.byref(k), ctypes.byref(u)):
            return None
        f = lambda x: (x.hi << 32) | x.lo
        return f(k) + f(u), f(i)                      # 内核时间里已经含着空闲时间
    with open("/proc/stat") as fh:
        v = [int(x) for x in fh.readline().split()[1:9]]
    return sum(v), v[3] + v[4]


def _mem_bytes():
    """(总内存, 已用)，字节。"""
    if sys.platform == "win32":
        import ctypes

        class MS(ctypes.Structure):
            _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong), ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong), ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong), ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong), ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
        m = MS()
        m.dwLength = ctypes.sizeof(MS)
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m)):
            return None
        return m.ullTotalPhys, m.ullTotalPhys - m.ullAvailPhys
    d = {}
    with open("/proc/meminfo") as fh:
        for l in fh:
            k, v = l.split(":", 1)
            d[k] = int(v.split()[0]) * 1024
    return d["MemTotal"], d["MemTotal"] - d.get("MemAvailable", d.get("MemFree", 0))


def _smi_path():
    import shutil
    c = [shutil.which("nvidia-smi")]
    if sys.platform == "win32":
        c += [os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32", "nvidia-smi.exe"),
              os.path.join(os.environ.get("ProgramFiles", r"C:\Program Files"), "NVIDIA Corporation", "NVSMI", "nvidia-smi.exe")]
    return next((p for p in c if p and os.path.exists(p)), None)


def _gpu():
    """NVIDIA 显卡：名字、占用 %、显存（MB）、温度、功耗。没有 NVIDIA 显卡（或没装驱动）返回 None。"""
    p = _smi_path()
    if not p:
        return None
    r = subprocess.run([p, "--query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu,power.draw",
                        "--format=csv,noheader,nounits"], capture_output=True, timeout=8, creationflags=NOWIN)
    lines = _dec(r.stdout).strip().splitlines()
    if r.returncode != 0 or not lines:
        return None
    f = [x.strip() for x in lines[0].split(",")]
    num = lambda s: float(s) if re.fullmatch(r"\d+(\.\d+)?", s or "") else None
    g = {"name": f[0], "util": num(f[1] if len(f) > 1 else ""), "used": num(f[2] if len(f) > 2 else ""),
         "total": num(f[3] if len(f) > 3 else ""), "temp": num(f[4] if len(f) > 4 else ""), "power": num(f[5] if len(f) > 5 else "")}
    for k in ("util", "used", "total", "temp", "power"):
        if g[k] is not None:
            g[k] = round(g[k])
    return g


def machine():
    """这台电脑现在：CPU 占用 %、内存（GB）、显卡。几个地方一起来取时，1.5 秒内用同一份。"""
    with _M["lock"]:
        now = time.time()
        if _M["last"] and now - _M["t"] < 1.5:
            return _M["last"]
        out = {"t": now, "cpu": None, "mem": None, "gpu": None}
        try:
            ct = _cpu_times()
            if ct and (not _M["cpu"] or now - _M["cpu"][2] > 30):          # 第一次（或隔太久）：隔一下再量一次
                _M["cpu"] = (ct[0], ct[1], now)
                time.sleep(0.3)
                ct = _cpu_times()
            if ct and _M["cpu"] and ct[0] > _M["cpu"][0]:
                out["cpu"] = round(max(0.0, min(100.0, 100.0 * (1 - (ct[1] - _M["cpu"][1]) / (ct[0] - _M["cpu"][0])))))
            if ct:
                _M["cpu"] = (ct[0], ct[1], time.time())
        except Exception:
            pass
        try:
            mt = _mem_bytes()
            if mt and mt[0]:
                out["mem"] = {"total": round(mt[0] / 2 ** 30, 1), "used": round(mt[1] / 2 ** 30, 1), "pct": round(100 * mt[1] / mt[0])}
        except Exception:
            pass
        if now - _M["smi_t"] > (60 if _M["smi_fail"] >= 3 else 2):          # 读不到显卡就少读几次
            _M["smi_t"] = now
            try:
                _M["smi"] = _gpu()
            except Exception:
                _M["smi"] = None
            _M["smi_fail"] = 0 if _M["smi"] else _M["smi_fail"] + 1
        out["gpu"] = _M["smi"]
        _M["last"], _M["t"] = out, time.time()
        return out


# ═══════════════════════ v1.11.0：一批在跑的时候记电脑占用（平均 / 最高），做完的汇报里写 ═══════════════════════
RUNS_P = C.DATA / "video_runs.json"
_RS = {"lock": threading.RLock(), "d": None, "names": set(), "seen": 0.0, "thread": None, "saved": 0.0, "wsl": None}


def _runs():
    if _RS["d"] is None:
        try:
            _RS["d"] = json.loads(RUNS_P.read_text(encoding="utf-8"))
        except Exception:
            _RS["d"] = {}
    return _RS["d"]


def _runs_save():
    try:
        with _RS["lock"]:
            s = json.dumps(_runs(), ensure_ascii=False)
        RUNS_P.write_text(s, encoding="utf-8")
        _RS["saved"] = time.time()
    except Exception:
        pass


def _acc(names, m, wm=None):
    with _RS["lock"]:
        d = _runs()
        for nm in names:
            r = d.setdefault(nm, {"n": 0, "t0": m["t"], "t1": m["t"]})
            r["n"] += 1
            r["t1"] = m["t"]

            def add(key, val):
                if val is None:
                    return
                a = r.setdefault(key, [0.0, 0.0, 0])          # [加起来, 最高, 几次]
                a[0] += val
                a[1] = max(a[1], val)
                a[2] += 1
            add("cpu", m.get("cpu"))
            if m.get("mem"):
                add("mem", m["mem"]["pct"])
                add("memGB", m["mem"]["used"])
                r["memTotal"] = m["mem"]["total"]
            g = m.get("gpu") or {}
            add("gpu", g.get("util"))
            add("gtemp", g.get("temp"))
            add("vram", g.get("used"))
            if g.get("total"):
                r["vramTotal"] = g["total"]
            if g.get("name"):
                r["gpuName"] = g["name"]
            if wm and wm[0] is not None:
                add("wslGB", wm[0])
                r["wslTotal"] = wm[1]


def _run_stats(name):
    with _RS["lock"]:
        r = json.loads(json.dumps(_runs().get(name) or {}))
    if not r.get("n"):
        return None
    st = lambda k: {"avg": round(r[k][0] / r[k][2], 1), "max": round(r[k][1], 1)} if r.get(k) and r[k][2] else None
    return {"mins": round(r["n"] * 5 / 60), "cpu": st("cpu"), "mem": st("mem"), "memGB": st("memGB"), "memTotal": r.get("memTotal"),
            "gpu": st("gpu"), "gtemp": st("gtemp"), "vram": st("vram"), "vramTotal": r.get("vramTotal"), "gpuName": r.get("gpuName"),
            "wslGB": st("wslGB"), "wslTotal": r.get("wslTotal")}


def _note_running(names, wm=None):
    """告诉记录的线程：现在哪几批在跑（出视频页每次来取都会说；开工时也说）。有在跑的就开始每 5 秒记一笔。"""
    with _RS["lock"]:
        _RS["names"] = set(names)
        _RS["seen"] = time.time()
        if wm:
            _RS["wsl"] = wm
        t = _RS["thread"]
        if _RS["names"] and not (t and t.is_alive()):
            _RS["thread"] = threading.Thread(target=_sampler, daemon=True, name="video-sampler")
            _RS["thread"].start()


def _sampler():
    last_chk = time.time()
    while True:
        with _RS["lock"]:
            names, seen, wm = set(_RS["names"]), _RS["seen"], _RS["wsl"]
        if not names:
            break
        try:
            _acc(names, machine(), wm)
        except Exception:
            pass
        now = time.time()
        if now - seen > 60 and now - last_chk > 60:        # 出视频页没开着：自己隔一分钟看看还在不在跑
            last_chk = now
            try:
                running = {b["name"] for b in batch_list() if b.get("running")}
            except Exception:
                running = names
            with _RS["lock"]:
                _RS["names"], _RS["seen"] = running, time.time()
        if now - _RS["saved"] > 60:
            _runs_save()
        time.sleep(5)
    _runs_save()


def startup():
    """软件打开时：WSL 开着、有批次在出片，就接着记电脑占用（不为这个去开 WSL）。"""
    def go():
        try:
            if not has_wsl():
                return
            r = subprocess.run(["wsl", "-l", "--running", "-q"], capture_output=True, timeout=20, creationflags=NOWIN)
            if vcfg()["distro"] not in [l.strip().strip("\x00").strip() for l in _dec(r.stdout).splitlines()]:
                return
            running = [b["name"] for b in batch_list() if b.get("running")]
            if running:
                _note_running(running)
        except Exception:
            pass
    t = threading.Timer(15, go)
    t.daemon = True
    t.start()


# ═══════════════════════ v1.11.0：批次的实时情况（出视频页每隔几秒来取） ═══════════════════════
# 直接读 WSL 里流水线自己写的 state.json、pipeline.log（不用 batch.sh 的新功能：软件更新了，WSL 里不用重新同步）
LIVE_PY = r'''
import glob, json, os, re, sys, time
H = os.path.expanduser("~")
B = os.path.join(H, "wf-batch")
want = set(x for x in (sys.argv[1] if len(sys.argv) > 1 else "").split("|") if x)
now = time.time()


def read_env(p):
    d = {}
    try:
        for l in open(p, encoding="utf-8"):
            l = l.strip()
            if l and not l.startswith("#") and "=" in l:
                k, v = l.split("=", 1)
                d[k.strip()] = v.strip().strip('"').strip("'")
    except OSError:
        pass
    return d


def load_list(p):
    rows = []
    try:
        for l in open(p, encoding="utf-8"):
            if not l.strip() or l.lstrip().startswith("#"):
                continue
            c = l.rstrip("\n").replace("\r", "").split("\t")
            if len(c) >= 3 and c[1].strip():
                rows.append({"no": c[0].strip(), "word": c[1].strip()})
    except OSError:
        pass
    return rows


def alive(d):
    try:
        os.kill(int(open(os.path.join(d, "pipeline.pid")).read().strip()), 0)
        return True
    except Exception:
        return False


def events(d):
    ev, y = [], time.localtime().tm_year
    try:
        for l in open(os.path.join(d, "pipeline.log"), encoding="utf-8", errors="replace"):
            m = re.match(r"^流水线(开始|停了) (\d\d-\d\d \d\d:\d\d:\d\d)", l)
            if not m:
                continue
            t = time.mktime(time.strptime("%d-%s" % (y, m.group(2)), "%Y-%m-%d %H:%M:%S"))
            if t > now + 86400:
                t = time.mktime(time.strptime("%d-%s" % (y - 1, m.group(2)), "%Y-%m-%d %H:%M:%S"))
            ev.append([m.group(1) == "开始", t])
    except (OSError, ValueError):
        pass
    return ev[-400:]


def cpu():
    try:
        v = [int(x) for x in open("/proc/stat").readline().split()[1:9]]
        return [sum(v), v[3] + v[4]]
    except Exception:
        return None


def mem():
    d = {}
    try:
        for l in open("/proc/meminfo"):
            k, v = l.split(":", 1)
            d[k] = int(v.split()[0])
    except Exception:
        pass
    return [d.get("MemTotal", 0), d.get("MemAvailable", 0)]


out = {"now": now, "cpu": cpu(), "mem": mem(), "batches": []}
for d in sorted(glob.glob(os.path.join(B, "*", ""))):
    name = os.path.basename(d.rstrip("/"))
    b = {"name": name}
    try:
        lst = os.path.join(d, "list.tsv")
        b["created"] = os.path.getmtime(lst) if os.path.exists(lst) else os.path.getmtime(d)
        b["alive"] = alive(d)
        b["paused"] = os.path.exists(os.path.join(d, "paused"))
        b["stopped"] = os.path.exists(os.path.join(d, "stopped"))
        cfg = read_env(os.path.join(d, "config.env"))
        b["cfg"] = {k: cfg.get(k, "") for k in ("WIN_DIR", "GPU", "UPLOAD", "HOLD_QA", "FAKE")}
        st, sp = None, os.path.join(d, "state.json")
        if os.path.exists(sp):
            try:
                st = json.load(open(sp, encoding="utf-8"))
            except Exception:
                st = None
        b["started"] = st is not None
        ws = (st or {}).get("words") or [dict(r, stage="prep", status="waiting", msg="", tries={}, t={}) for r in load_list(lst)]
        b["n"] = len(ws)
        cnt = {"done": 0, "skipped": 0, "todo": 0, "running": 0, "waiting": 0, "pic": 0}
        for w in ws:
            s, x = w.get("stage"), w.get("status")
            if s == "prep" and x == "blocked" and (w.get("msg") or "").lstrip("\u26a0\u274c\u2705 ").startswith("起草检查没过"):
                cnt["pic"] += 1
            cnt["done" if s == "done" else "skipped" if s == "skipped" else "todo" if x in ("blocked", "failed", "qa")
                else "running" if x == "running" else "waiting"] += 1
        b["counts"] = cnt
        b["res"] = (st or {}).get("resources")
        b["updated"] = (st or {}).get("updated")
        cm = []
        for f in sorted(glob.glob(os.path.join(d, "cmd", "*.json"))):
            try:
                c = json.load(open(f, encoding="utf-8"))
                cm.append({"op": c.get("op", ""), "word": c.get("word", ""), "stage": c.get("stage", "")})
            except Exception:
                pass
        b["cmds"] = cm
        if name in want or b["alive"]:
            b["words"] = [{"no": w.get("no", ""), "word": w.get("word", ""), "stage": w.get("stage", ""),
                           "status": w.get("status", ""), "msg": (w.get("msg") or "")[:400],
                           "tries": (w.get("tries") or {}).get(w.get("stage"), 0), "t": w.get("t") or {}} for w in ws]
            b["ev"] = events(d)
            np_ = os.path.join(d, "notes.md")
            if os.path.exists(np_):
                b["notes"] = open(np_, encoding="utf-8", errors="replace").read()[-3000:]
    except Exception as e:
        b["error"] = str(e)[:300]
    out["batches"].append(b)
print("@@LIVE@@" + json.dumps(out, ensure_ascii=False))
'''

_LV = {"lock": threading.Lock(), "wcpu": None, "done": {}, "scan": None, "scanT": 0.0}


def _plain(msg):
    """日志里的一句话：去掉前面的 ⚠ ❌ ✅、多余的空格。"""
    s = " ".join(str(msg or "").split())
    return re.sub(r"^[⚠❌✅\s]+", "", s)[:300]


def _active_secs(ev, marks, running, now):
    """流水线真正在跑的时间（不算暂停、停下的时间）：pipeline.log 里每一段“流水线开始 … 流水线停了”加起来；
    没写“停了”的（WSL 关了、电脑重启）算到那一段里最后一个动静。"""
    marks = sorted(marks)

    def last_in(a, b):
        xs = [x for x in marks if a <= x <= b]
        return max(xs) if xs else a
    tot, start = 0.0, None
    for is_start, t in ev:
        if is_start:
            if start is not None:
                tot += max(0.0, last_in(start, t) - start)
            start = t
        elif start is not None:
            tot += max(0.0, t - start)
            start = None
    if start is not None:
        tot += max(0.0, (now if running else last_in(start, now)) - start)
    return tot


def _res_text(r):
    try:
        return "WSL 给出片 %d 核、%.0f GB 内存；准备组同时 %d 个词，配音组 %d 个，渲染组 %d 个（%s 个浏览器）；%s；显卡用在：%s" % (
            r["cpu"], r["mem"], r["LANE_PREP"], r.get("LANE_VOICE", 1), r.get("LANE_RENDER", 1), r["RENDER_JOBS"] or "自动",
            "配音和渲染同时跑" if r.get("TOGETHER") else "配音和渲染轮流跑", r.get("GPU", "不用"))
    except Exception:
        return ""


def _win_dir(p, name):
    m = re.match(r"^/mnt/([a-z])/(.*)$", p or "")
    if m:
        return "%s:\\%s" % (m.group(1).upper(), m.group(2).replace("/", "\\"))
    return p or str(Path(vcfg()["winDir"]) / name)


def _bview(b, now):
    """一个批次给界面看的样子：状态、数字、每个词、正在做的、卡住的、用时、汇报用的电脑占用。"""
    name = b.get("name", "")
    if b.get("error"):
        return {"name": name, "state": "error", "error": b["error"], "n": 0, "counts": {}, "cmds": []}
    alive = bool(b.get("alive"))
    c = dict(b.get("counts") or {})
    if not alive:                                   # 流水线没在跑：写着“正在做”的其实停在那一步了
        c["waiting"] = c.get("waiting", 0) + c.get("running", 0)
        c["running"] = 0
    n = b.get("n", 0)
    if alive:
        state = "pausing" if b.get("paused") else "stopping" if b.get("stopped") else "running"
    elif b.get("paused"):
        state = "paused"
    elif b.get("stopped"):
        state = "stopped"
    elif not b.get("started"):
        state = "new"
    elif c.get("done", 0) + c.get("skipped", 0) >= n:
        state = "done"
    elif c.get("waiting", 0):
        state = "halted"
    else:
        state = "stuck"
    v = {"name": name, "n": n, "state": state, "counts": c, "created": b.get("created"), "cfg": b.get("cfg") or {},
         "cmds": b.get("cmds") or [], "winDir": _win_dir((b.get("cfg") or {}).get("WIN_DIR"), name)}
    words = b.get("words")
    if words is None:
        return v
    ws, marks, nowl, todo = [], [], [], []
    for w in words:
        t = w.get("t") or {}
        dur = {}
        for s in STG:
            x = t.get(s)
            if x and x[0]:
                marks.append(x[0])
                if x[1]:
                    marks.append(x[1])
                    dur[s] = round(x[1] - x[0])
        status = w.get("status") or ""
        if not alive and status == "running":
            status = "waiting"
        cur = None
        x = t.get(w.get("stage"))
        if alive and status == "running" and x and x[0]:
            cur = round(now - x[0])
        starts = [y[0] for y in t.values() if y and y[0]]
        ends = [y[1] for y in t.values() if y and y[1]]
        took = round(max(ends) - min(starts)) if w.get("stage") == "done" and starts and ends else None
        it = {"no": w.get("no", ""), "word": w.get("word", ""), "stage": w.get("stage", ""), "status": status,
              "msg": _plain(w.get("msg")), "tries": w.get("tries") or 0, "dur": dur, "cur": cur, "took": took}
        ws.append(it)
        if cur is not None:
            nowl.append({"word": it["word"], "stage": it["stage"], "secs": cur})
        if it["stage"] not in ("done", "skipped") and status in ("blocked", "failed", "qa"):
            todo.append(it)
    act = _active_secs(b.get("ev") or [], marks, alive, now)
    if not act and marks:
        act = (now if alive else max(marks)) - min(marks)
    done_n = c.get("done", 0)
    per = act / done_n if done_n else None
    left = c.get("waiting", 0) + c.get("running", 0)
    starts = [t for s, t in (b.get("ev") or []) if s] + marks
    avg = {}
    for s in STG:
        ds = [x["dur"][s] for x in ws if x["stage"] == "done" and x["dur"].get(s) is not None]
        if ds:
            avg[s] = round(sum(ds) / len(ds))
    v.update(words=ws, now=nowl, todo=todo, active=round(act), per=round(per) if per else None,
             eta=round(per * left) if (alive and per and done_n >= 2 and left) else None,
             first=min(starts) if starts else None, stageAvg=avg, res=_res_text(b.get("res")),
             notes=[l.strip().lstrip("-").strip() for l in (b.get("notes") or "").splitlines() if l.strip().startswith("-")][-30:],
             machine=_run_stats(name))
    return v


def _scan_bg():
    with _LV["lock"]:
        if _LV["scan"] and _LV["scan"].is_alive():
            return
        def go():
            try:
                scan_videos()
            except Exception as e:
                C.log("登记视频出错：%s" % e)
        _LV["scan"] = threading.Thread(target=go, daemon=True)
        _LV["scanT"] = time.time()
        _LV["scan"].start()


def live(open_names=()):
    """出视频页每隔几秒来取一次：每个批次的情况（展开的、在跑的带上每个词），电脑占用，出片的 Linux 用了多少。"""
    out = {"wsl": has_wsl(), "machine": machine(), "batches": []}
    try:
        out["videosN"] = len(videos())
    except Exception:
        out["videosN"] = 0
    if not out["wsl"]:
        out["msg"] = "这台电脑没有 WSL：视频只能在装了 WSL 的 Windows 上做"
        return out
    names = [x for x in open_names if NAME_RE.fullmatch(x or "")][:30]
    rc, t = wsl("python3 - %s <<'PYLIVE'\n%s\nPYLIVE\n" % (q("|".join(names)), LIVE_PY), 60)
    i = t.find("@@LIVE@@")
    if i < 0:
        out["error"] = "读不了 WSL 里的批次（%s）：%s" % (rc, " ".join(t.split())[-200:])
        return out
    try:
        d = json.loads(t[i + 8:].strip().splitlines()[0])
    except Exception as e:
        out["error"] = "读不了批次：%s" % e
        return out
    w = {}
    mt, ma = (d.get("mem") or [0, 0])[:2]
    if mt:
        w["total"], w["used"] = round(mt / 1048576, 1), round((mt - ma) / 1048576, 1)
    cp = d.get("cpu")
    with _LV["lock"]:
        prev, _LV["wcpu"] = _LV["wcpu"], cp
    if cp and prev and cp[0] > prev[0]:
        w["cpu"] = round(max(0.0, min(100.0, 100.0 * (1 - (cp[1] - prev[1]) / (cp[0] - prev[0])))))
    out["wslSys"] = w
    now = d.get("now") or time.time()
    bs = [_bview(b, now) for b in d.get("batches") or []]
    bs.sort(key=lambda b: -(b.get("created") or 0))
    out["batches"] = bs
    running = {b["name"] for b in bs if b["state"] in ("running", "pausing", "stopping")}
    _note_running(running, (w.get("used"), w.get("total")) if w.get("total") else None)
    scan = False                                     # 有词新做好了：登记新视频（后台做，不耽误这一次）
    with _LV["lock"]:
        for b in bs:
            k = b.get("counts", {}).get("done", 0)
            if b["name"] in _LV["done"] and k > _LV["done"][b["name"]]:
                scan = True
            _LV["done"][b["name"]] = k
        if running and time.time() - _LV["scanT"] > 120:
            scan = True
    if scan:
        _scan_bg()
    return out


# ═══════════ v1.11.1：补画面要用的——画面设置拷进 WSL、批次里起草检查说的“还要补”、要补的词 ═══════════
def sync_pics():
    """词库/画面设置 → WSL 的 ~/kit-extra（流水线“准备”读的就是这一份）。几秒钟。"""
    rc, t = wsl("mkdir -p ~/kit-extra && cp -r %s/. ~/kit-extra/ && find ~/kit-extra -name '*.py' -exec sed -i 's/\\r$//' {} +"
                % q(to_wsl(C.REPO / EXTRA)), 120)
    return rc == 0


def prep_todo(batch, words):
    """批次里这些词“准备”那一步起草检查最后一次说的“还要补：…”：{单词: 那一句}（日志里读，比任务里存的那一句全）。"""
    if not NAME_RE.fullmatch(batch or ""):
        return {}
    fm = {folder_of(w): w for w in words}
    rc, t = wsl("cd \"$HOME/wf-batch/%s/logs\" 2>/dev/null || exit 0\n"
                "for f in *.prep.log; do [ -f \"$f\" ] || continue; l=$(grep -a '^还要补' \"$f\" | tail -1); "
                "[ -n \"$l\" ] && printf '%%s\\t%%s\\n' \"${f%%.prep.log}\" \"$l\"; done\n" % batch, 60)
    out = {}
    for line in (t or "").splitlines():
        if "\t" in line:
            f, l = line.split("\t", 1)
            if f in fm:
                out[fm[f]] = l.strip()
    return out


def fix_words(batch="", words=()):
    """要补画面的词：批次里卡在“准备”（起草检查没过）的，加上还没轮到、画面也没过起草检查的；
    或者给的这些词里画面没过起草检查的。"""
    import pics
    unc = pics.unchecked_words()
    out = []
    if batch:
        if not NAME_RE.fullmatch(batch):
            return []
        fm = {}
        try:
            for r in C.read_index()[1]:
                fm.setdefault(folder_of(r[2]), r[2])
        except Exception:
            pass
        b = next((x for x in live([batch]).get("batches") or [] if x.get("name") == batch), None) or {}
        for w in b.get("words") or []:
            if w.get("stage") in ("done", "skipped"):
                continue
            word = fm.get(w["word"], w["word"].replace("_", " "))
            stuck = w.get("stage") == "prep" and w.get("status") == "blocked" and (w.get("msg") or "").startswith("起草检查没过")
            if (stuck or word in unc) and word not in out:
                out.append(word)
    for w in words or []:
        if w in unc and w not in out:
            out.append(w)
    return out
