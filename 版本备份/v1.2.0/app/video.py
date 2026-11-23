# -*- coding: utf-8 -*-
"""单词工作台 · 视频
真正出片的还是原来的视频技能和批量流水线（在 WSL 的 Ubuntu 里跑）。这里做三件事：
  1. 把仓库「引擎」里的视频技能、本地出片、批量出片脚本和「词库」里的总表同步进 WSL（代替以前的 02_get_repo.sh）；
  2. 装环境（01 系统软件、03 声音模型、04 显卡）放后台跑，界面看进度；
  3. 选词建批次 → 开工 → 看进度 → 做好的视频拷到 D 盘、登记进「词库/视频清单.tsv」。
视频文件很大（一个 20–45 MB），不进 git，只登记。"""
import json, os, re, subprocess, sys, time
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


def wsl(cmd, timeout=600):
    """在 WSL 里用 root 跑一条 bash 命令，返回 (返回码, 输出)。"""
    if not has_wsl():
        return 127, "这台电脑没有 WSL（只能在 Windows 上用）"
    try:
        r = subprocess.run(["wsl", "-d", vcfg()["distro"], "-u", "root", "--", "bash", "-lc", cmd],
                           capture_output=True, timeout=timeout, creationflags=NOWIN)
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
      echo "skill=$(grep -m1 '^当前 6\\.' ~/skills/word-construction-video/SKILL.md 2>/dev/null | cut -c1-40)"
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


def batch_new(name, words):
    if not re.fullmatch(r"[A-Za-z0-9_\-\u4e00-\u9fff]{1,40}", name or ""):
        return False, "批次名只用字母、数字、汉字、- 和 _"
    pw = pic_words()
    rows, miss = [], []
    for i, w in enumerate(words, 1):
        f = folder_of(w)
        if f not in pw:
            miss.append(w)
            continue
        rows.append("%02d\t%s\t%s\t出自单词工作台" % (i, f, pw[f]))
    if not rows:
        return False, "这些词都还没有画面设置，做不了视频：%s" % "、".join(miss[:20])
    lst = C.DATA / "batches" / (name + ".tsv")
    lst.parent.mkdir(exist_ok=True)
    lst.write_text("# 单词工作台建的批次\n" + "\n".join(rows) + "\n", encoding="utf-8")
    wl = to_wsl(lst)
    v = vcfg()
    windir = to_wsl(Path(v["winDir"]) / name) if re.match(r"^[A-Za-z]:", v["winDir"]) else v["winDir"]
    rc, t = wsl("mkdir -p ~/wf-lists && tr -d '\\r' < %s > ~/wf-lists/%s.tsv && bash ~/lwb/scripts/wsl/batch.sh new %s ~/wf-lists/%s.tsv"
                % (q(wl), name, q(name), name), 300)
    if rc != 0:
        return False, t[-1500:]
    sets = ["UPLOAD=0", "WIN_DIR=" + windir, "HOLD_QA=%d" % (1 if v["holdQA"] else 0), "GPU=%d" % (1 if v["gpu"] else 0)]
    batch_cmd(["set", name] + sets, 60)
    note = ("；没有画面设置、没放进批次：%s" % "、".join(miss[:30])) if miss else ""
    return True, t[-1500:] + note


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


def batch_op(name, op, word="", stage=""):
    ops = {"start": (["set", name, "CONFIRMED=1"], ["start", name]), "stop": (["stop", name],),
           "status": (["status", name, "full"],), "report": (["report", name],), "check": (["check", name],),
           "retry": (["retry", name, word] + ([stage] if stage else []),), "skip": (["skip", name, word],),
           "ok": (["ok", name, word],), "log": (["log", name, word] + ([stage] if stage else []) + ["40"],)}
    if op not in ops:
        return False, "不认识的操作"
    if op == "start":
        keepalive()
    outs = []
    rc = 0
    for args in ops[op]:
        rc, t = batch_cmd(args, 300)
        outs.append(t)
    if op in ("status", "report"):
        try:
            scan_videos()
        except Exception as e:
            C.log("登记视频出错：%s" % e)
    return rc == 0, "\n".join(outs)[-6000:]
