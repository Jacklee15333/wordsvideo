# -*- coding: utf-8 -*-
"""单词工作台 · 视频
真正出片的还是原来的视频技能和批量流水线（在 WSL 的 Ubuntu 里跑）。这里做三件事：
  1. 把仓库「引擎」里的视频技能、本地出片、批量出片脚本和「词库」里的总表同步进 WSL（代替以前的 02_get_repo.sh）；
  2. 装环境（01 系统软件、03 声音模型、04 显卡）放后台跑，界面看进度；
  3. 选词建批次 → 开工 → 看进度 → 做好的视频拷到 D 盘、登记进「词库/视频清单.tsv」。
v1.11.0：出片前检查一项一项打勾（有问题的那一行就能修）；批次能暂停、停止、删除；在跑的批次实时看每个词、电脑忙不忙；做完出汇报。
v1.19.0：开工分三步——① 出片前检查 ② 单词检测（照“准备”起草检查、纯英文句子先念一遍听一遍）③ 开工；有问题的词说清楚怎么办。
v1.20.0：能做的就做，不能做的退回去——选词只列能出视频的；单词检测、出片中画面有问题的词自动拿出这一批、退回「画面」，别的照常做；每一批一份汇报。
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


def wsl_stream(cmd, on_line, timeout=120, stop=None):
    """和 wsl() 一样跑一段脚本，不过每输出一行就交给 on_line（检测详情里一行一行实时出来）。返回 (返回码, 最后几行)。
    v1.19.0：stop() 返回 True 就停下（比如单词检测查到一半，又点了别的批次的「开工」）。"""
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
            raw = (raw + b)[-20000:]
            if stop and stop():
                killed.append(0)
                pr.kill()
                break
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
    if killed == [0]:
        return 130, "停下了"
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
echo "voice=$(md5sum ~/skills/word-construction-video/assets/voice/ref.wav 2>/dev/null | cut -c1-32)"
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
rm -rf ~/kit-extra; mkdir -p ~/kit-extra/words; [ -d "$S/%(extra)s" ] && cp -r "$S/%(extra)s/." ~/kit-extra/ || true
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
                ver = f[5].strip() if len(f) >= 6 else ""
                out[f[0]] = {"word": f[0], "batch": f[1], "file": f[2], "size": f[3], "ts": f[4], "ver": ver, "old": is_old(ver)}
    return out


# v1.21.0：视频技能 6.43.0 起精简版再精简（读音拆分只念一块一块、词缀词根直接说“英语前缀”、同义词辨析只念单词给特写）。
#   这以前做的视频叫“旧版”：「做好的视频」里标出来，能一起删掉、按新版重做。登记时记下当时的视频技能版本（视频清单第 6 列；以前的行没有＝旧版）
LEAN_VER = (6, 51, 0)                 # v1.25.8：用户“还是用 6.51”——6.53 的声音就是 6.51；6.51 以前的和 6.52 做的算旧版
VDEL_P = C.DATA / "video_deleted.json"     # 删掉了旧版视频的词 {文件夹名: {t 几点删的, b 当时“做好了”的批次}}：这些批次里的“做好了”不再算数（见 inbatch）


def _vt(v):
    return tuple(int(x) for x in re.findall(r"\d+", v or "")[:3])


def is_old(ver):
    t = _vt(ver)
    if t and (6, 52, 0) <= t < (6, 53, 0):          # v1.25.8：6.52 的声音用户不要，算旧版；6.51 和 6.53 声音一样，不算
        return True
    return not t or t < LEAN_VER


def _cur_skill():
    try:
        import pics
        return pics.skill_version()[0]
    except Exception:
        return ""


def _write_vlist(have):
    rows = ["单词\t批次\t文件（相对出片文件夹）\t大小\t时间\t视频技能"] + [
        "\t".join([v["word"], v["batch"], v["file"], v["size"], v["ts"], v.get("ver", "")]) for v in sorted(have.values(), key=lambda v: v["ts"])]
    with C.REPO_LOCK:
        (C.REPO / VLIST).write_text("\n".join(rows) + "\n", encoding="utf-8")


def _vdel():
    try:
        d = json.loads(VDEL_P.read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def _vdel_save(d):
    VDEL_P.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def _try_wsl(sh):
    try:
        wsl(sh, 120)
    except Exception:
        pass


def delete_old(words=None, only_old=True):
    """v1.21.0：删掉旧版视频（视频技能 6.43.0 以前做的）——出片文件夹里的 mp4 和关键画面图、视频清单里的登记，WSL 里的成片也删。
    这些词回到「出视频」的选词列表（当时批次里“做好了”的记号不再算数）；批次的生成历史留着。words 不给就删全部旧版。"""
    have = videos()
    pick = [k for k, v in have.items() if (v.get("old") or not only_old) and (not words or k in words)]      # v1.27.0：only_old=False 不管新旧（「清除视频」）
    if not pick:
        return {"ok": False, "msg": "没有旧版视频了" if only_old else "选的视频都没登记"}
    root = Path(vcfg()["winDir"])
    with _INB["lock"]:
        inb = {n: [x[0] for x in ws if len(x) > 1 and x[1] == "done"] for n, ws in _inb().items()}
    gone, bad, rm = [], [], []
    bat = {k: have[k]["batch"] for k in pick}
    for k in pick:
        v = have[k]
        mp4 = root / v["file"].replace("\\", "/")
        try:
            sib = [x for x in mp4.parent.iterdir() if x.is_file() and x.name.startswith(mp4.stem + "_")] if mp4.parent.is_dir() else []
            for x in [mp4] + sib:
                x.unlink(missing_ok=True)
        except Exception as e:
            bad.append("%s（%s）" % (k, str(e)[:80]))
            continue
        gone.append(k)
        have.pop(k, None)
        rm.append("%s/%s" % (mp4.parent.name, mp4.stem))
    if gone:
        _write_vlist(have)
        d, now = _vdel(), time.strftime("%Y-%m-%d %H:%M")
        for k in gone:
            f = k.replace("（详解版）", "")
            d[f] = {"t": now, "b": sorted({bat[k]} | {n for n, ws in inb.items() if f in ws})}
        _vdel_save(d)
        sh = "; ".join("rm -f -- ~/wordfilm-out/%s ~/wordfilm-out/%s" % (q(x + ".mp4"), q(x + "_关键画面.jpg")) for x in rm)
        threading.Thread(target=_try_wsl, args=(sh,), daemon=True).start()      # WSL 里的成片也删（不等它）
        C.log("删掉了 %d 个旧版视频（%s）：这些词回到「出视频」的选词列表" % (len(gone), "、".join(gone[:6]) + (" 等" if len(gone) > 6 else "")))
    msg = ("删掉了 %d 个%s视频：这些词回到「出视频」的选词列表了，建批次、开工就是新版" % (len(gone), "旧版" if only_old else "")) if gone else ""
    if bad:
        msg += ("；" if msg else "") + "%d 个没删掉（可能正在播放）：%s" % (len(bad), "、".join(bad[:3]))
    return {"ok": bool(gone) and not bad, "n": len(gone), "msg": msg}


def scan_videos():
    """把 D 盘出片文件夹里的 mp4 登记进 词库/视频清单.tsv（只登记，不传视频）。"""
    root = Path(vcfg()["winDir"])
    if not root.exists():
        return 0
    have = videos()
    cur, vd = _cur_skill(), _vdel()
    n = 0
    for mp4 in root.rglob("*.mp4"):
        m = re.match(r"^(?:\d+\s+)?(.+?)(?:_精简版|_详解版)?$", mp4.stem)
        name = m.group(1) if m else mp4.stem
        key = name if "详解" not in mp4.stem else name + "（详解版）"
        rel = str(mp4.relative_to(root))
        if have.get(key, {}).get("file") == rel:
            continue
        have[key] = {"word": key, "batch": mp4.parent.name, "file": rel,
                     "size": "%.1f MB" % (mp4.stat().st_size / 1e6), "ts": time.strftime("%Y-%m-%d %H:%M", time.localtime(mp4.stat().st_mtime)), "ver": cur}
        vd.pop(key, None)                         # v1.21.0：删过旧版的词又有了新视频
        n += 1
    if n:
        _write_vlist(have)
        if vd != _vdel():
            _vdel_save(vd)
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
    """建批次。words：选词列表里勾上的词。v1.20.0：只放现在就能出视频的；选上的别的词（已经有视频、在别的批次里、
    要退回「画面」「出题」的）写进这一批的汇报。返回 {ok, msg, n}。"""
    if not NAME_RE.fullmatch(name or ""):
        return {"ok": False, "msg": "批次名只用字母、数字、汉字、- 和 _（40 个字以内）"}
    pw = pic_words()
    info = pick_info()
    ready = [r["word"] for r in info["ready"]]
    want = set(words or [])
    put = [w for w in ready if w in want and folder_of(w) in pw]
    if not put:
        return {"ok": False, "msg": "勾上的词现在都不能出视频了（刚刚有变化）：页面刷新一下再勾"}
    rows = ["%02d\t%s\t%s\t出自单词工作台" % (i + 1, folder_of(w), pw[folder_of(w)]) for i, w in enumerate(put)]
    pre = {"video": info["video"], "inb": info["inb"], "pic": info["pic"], "q": info["q"], "left": [w for w in ready if w not in put]}
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
            last = "WSL 里还没有出片脚本：先到「出片环境」里点「同步到 WSL」"
        return {"ok": False, "msg": C.mask(last)[:300]}
    sets = ["UPLOAD=0", "WIN_DIR=" + windir, "HOLD_QA=%d" % (1 if v["holdQA"] else 0), "GPU=%d" % (1 if v["gpu"] else 0)]
    batch_cmd(["set", name] + sets, 60)
    with _RS["lock"]:
        _runs().pop(name, None)
    ack_set(name, False)
    probs, summ = _check_lines(t)
    rep_drop(name)

    def setup(r):
        r.update(t=time.time(), picked=info["n"], put=[folder_of(w) for w in put], pre=pre, out={}, lx=[])
    rep_edit(name, setup)
    with _INB["lock"]:                            # 选词列表马上不再列这些词（不用等下一次读 WSL）
        _inb()[name] = [[folder_of(w), "prep", "waiting"] for w in put]
    C.log("建了批次 %s：%d 个词%s" % (name, len(rows), "；" + summ if summ else ""))
    return {"ok": True, "msg": "建好了：批次 %s，%d 个词" % (name, len(rows)), "n": len(rows), "probs": probs, "check": summ}


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
    if w.get("stage") == "voice" and w.get("status") == "blocked" and "没听清" in m:
        continue                                   # v1.19.0：例句配音听不清——英文念法是固定的，再念一遍也一样，要重新做画面（换例句）
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


def batch_op(name, op, word="", stage="", why=""):
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
            ack_set(name, False)                    # v1.19.0：又开工了，做完以后先留在「出视频」里给你看汇报
            C.log("批次 %s 开工（%s）" % (name, _last_line(t)))
            return True, "开工了：批次 %s 正在生成" % name
        return False, C.mask(_last_line(t, "开工出错了（%s）" % rc))[:300]
    if op in ("pause", "stop"):
        mark, other = ("paused", "stopped") if op == "pause" else ("stopped", "paused")
        sh = have + "touch {BD}/%s; rm -f {BD}/%s\n" % (mark, other) + B + "stop {N}\n"
        rc, t = wsl(_fill(sh, **kw), 90)
        C.log("批次 %s %s：%s" % (name, "暂停" if op == "pause" else "停止", _last_line(t)))
        if op == "stop":
            go_clear(name)                          # v1.19.0：开工三步还在等的，不等了
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
            go_clear(name)
            ack_set(name, False)
            rep_drop(name)
            with _INB["lock"]:
                _inb().pop(name, None)
            C.log("删掉了批次 %s" % name)
            return True, "删掉了批次 %s（做好的视频还在出片文件夹里）" % name
        return False, C.mask(_last_line(t, "没删掉（%s）" % rc))[:300]
    if op in ("retry", "redo", "ok"):
        if not word:
            return False, "要写词"
        if op == "redo":
            kw["S"] = q("准备")
        act = "ok" if op == "ok" else "retry"
        # v1.19.0：还没开过工的批次（没有 state.json）也只记下，不替你开工——以前补画面补好一个词，会把整个批次开起来
        sh = have + "if [ -f {BD}/paused ] || [ -f {BD}/stopped ] || [ ! -f {BD}/state.json ]; then\n" + _QUEUE_SH + "else\n" + B + act + " {N} {W} {S}\nfi\n"
        rc, t = wsl(_fill(sh, OP=q(act), **kw), 90)
        what = {"retry": "再试一次", "redo": "从头重做", "ok": "放行"}[op]
        w = word.replace("_", " ")
        if rc != 0:
            return False, C.mask(_last_line(t, "没做成（%s）" % rc))[:300]
        if "QUEUED" in t:
            return True, "记下了：%s %s——点「开工」「继续」或「接着做」以后先做它" % (w, what)
        _note_running(_RS["names"] | {name})
        return True, "%s：%s（流水线接着做）" % (what, w)
    if op == "skip":
        if not word:
            return False, "要写词"
        rc, t = wsl(_fill(have + B + "skip {N} {W} " + q((why or "不做了（单词工作台里点的）")[:200]) + "\n", **kw), 90)
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
            ("syl", "音节划分表"), ("sys", "系统软件"), ("models", "声音模型"), ("voice", "男声"), ("gpu", "显卡"), ("windir", "出片文件夹"))
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
            run("voice")
        elif k == "voice":                     # v1.26.0：男声用的是哪个录音（用户：“你先检查一下你用的是什么音色”）
            want, lab = _voice_ref()
            if not v:
                put("voice", "bad", "WSL 里没有男声的参考录音：要同步", "sync")
            elif want and v != want:
                put("voice", "bad", "WSL 里的男声参考录音和仓库里的不一样：要同步", "sync")
            else:
                put("voice", "ok", "你的声音：" + lab)
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
        return "bad", "有 %d 项要先处理：%s（「出视频」页的「出片环境」里，那一行后面有按钮）" % (len(bad), "、".join(bad)), "video"
    txt = lambda k: (res.get(k) or ("", ""))[1]
    return "ok", "都好了：视频技能 %s；声音模型%s；显卡%s" % (
        txt("skill").split("，")[0], txt("models").replace("装好了", ""), "开了" if st("gpu") == "ok" else "没开（可选）"), ""


def _voice_ref():
    """v1.26.0：仓库里男声参考录音的 md5，和它从哪儿来（视频技能 assets/voice/来源.md 第一行）"""
    import hashlib
    d = C.REPO / "引擎" / "视频" / "assets" / "voice"
    try:
        h = hashlib.md5((d / "ref.wav").read_bytes()).hexdigest()
    except Exception:
        h = ""
    try:
        first = (d / "来源.md").read_text(encoding="utf-8").splitlines()[0].replace("当前：", "").strip()
        lab = "取自「素材/音色」" + first
    except Exception:
        lab = "技能自带的参考录音"
    return h, lab


def env_check(say, acts=None):
    """开始页「② 检测」的出片环境：v1.11.0 起和「出视频」页的检查是同一套，一项一句。返回 (状态, 一句话, 去哪儿修)。
    v1.21.1：acts 给了一个列表，就把没好的几项能自动修的办法（sync、boot、models、gpu）按先后记进去（「一键修复」用）"""
    def on_item(k, st, text, fix):
        if st == "bad" and fix in FIX_NAME and acts is not None and fix not in acts:
            acts.append(fix)
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
    with _EC_LOCK:                                  # v1.19.0：开工三步走到哪儿了、单词检测的结果
        g = dict(GO)
    g.pop("tok", None)
    g["secs"] = int((g.get("end") or now) - g["t"]) if g.get("t") else 0
    d["go"] = g
    d["wc"] = wc_get()
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
    with _EC_LOCK:
        g = dict(GO)
    if g.get("name") and g.get("state") == "bad" and g.get("step") == "env":
        go_start(g["name"], g.get("nocheck"))       # v1.19.0：开工时检查出来、点了修的：修好了再走一遍开工三步
    else:
        envchk_start()                              # 做完再从头检查一遍，那一行就变绿了


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
        watch_start()                              # v1.20.0：每分钟看一次有没有卡在画面问题上的词（WSL 没开着就不看）
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
            if s == "prep" and x == "blocked":     # v1.20.0：准备卡住的都是画面的事（起草检查没过、没有画面设置、图没画出来）
                cnt["pic"] += 1
            elif s == "voice" and x == "blocked" and "没听清" in (w.get("msg") or ""):
                cnt["pic"] += 1                    # v1.19.0：例句配音听不清——也是画面设置的事（换例句）
            cnt["done" if s == "done" else "skipped" if s == "skipped" else "todo" if x in ("blocked", "failed", "qa")
                else "running" if x == "running" else "waiting"] += 1
        b["counts"] = cnt
        b["ws"] = [[w.get("word", ""), w.get("stage", ""), w.get("status", "")] for w in ws]   # v1.20.0：每个词在哪一步（选词列表用）
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
            for w in b["words"]:                   # v1.19.0：例句配音听不清的：是哪一句、听成了什么（manifest.json）
                if w["stage"] == "voice" and w["status"] == "blocked" and "没听清" in w["msg"]:
                    try:
                        man = json.load(open(os.path.join(H, "wordfilm-work", w["word"], "brief", "audio", "manifest.json"), encoding="utf-8"))
                        w["miss"] = [{"scene": k, "text": (x.get("text") or "")[:200], "heard": (x.get("heard") or "")[:200],
                                      "miss": x.get("miss") or []} for k, xs in man.items() for x in xs if x.get("miss")][:4]
                    except Exception:
                        pass
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
         "cmds": b.get("cmds") or [], "winDir": _win_dir((b.get("cfg") or {}).get("WIN_DIR"), name),
         "ack": name in _acks(),                   # v1.19.0：做完、停止的点了「知道了」，收进「生成历史」
         "rep": rep_get(name)}                     # v1.20.0：这一批的汇报（建批次时没放进去的、退回去的）
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
        if w.get("miss"):
            it["miss"] = w["miss"]
            it["why"] = "；".join(_wc_voice(m)[2] for m in w["miss"])[:600]      # 界面上看的一句话（交给 AI 的那几条更长）
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


def live(open_names=(), auto=True):
    """出视频页每隔几秒来取一次：每个批次的情况（展开的、在跑的带上每个词），电脑占用，出片的 Linux 用了多少。
    v1.20.0：顺便记下每个批次里每个词在哪一步（选词列表用）；有卡在画面问题上的词，后台退回「画面」。"""
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
    _inb_note(d.get("batches") or [])
    bs = [_bview(b, now) for b in d.get("batches") or []]
    if auto:
        stuck = [b["name"] for b in bs if (b.get("counts") or {}).get("pic")]
        if stuck:
            _auto_back_bg(stuck)
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
    try:
        import pics
        n = pics.fix_word_pys()
        if n:
            C.log("画面设置程序修了 %d 个（演示词叫 actor 时不再出错）" % n)
    except Exception:
        pass
    rc, t = wsl("mkdir -p ~/kit-extra && cp -r %s/. ~/kit-extra/ && find ~/kit-extra -name '*.py' -exec sed -i 's/\\r$//' {} +"
                % q(to_wsl(C.REPO / EXTRA)), 120)
    return rc == 0


def prep_todo(batch, words):
    """批次里这些词“准备”那一步起草检查最后一次说的“还要补：…”：{单词: 那一句}（日志里读，比任务里存的那一句全）。
    v1.19.0：卡在“配音”、例句听不清的，也写成一条“还要补”（是哪一句、听成了什么、怎么改）。"""
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
    # v1.19.0：卡在“配音”、例句听不清的：从这个词的 manifest.json 读出是哪一句、听成了什么，也写进“还要补”
    rc, t = wsl("python3 - %s %s <<'PYTODO'\n%s\nPYTODO\n" % (q(batch), q("|".join(fm)), _VTODO_PY), 60)
    i = (t or "").find("@@TODO@@")
    if i >= 0:
        try:
            vt = json.loads(t[i + 8:].strip().splitlines()[0])
        except Exception:
            vt = {}
        for f, ms in vt.items():
            items = [_wc_voice(m)[1] for m in ms or []]
            if f in fm and items:
                old = out.get(fm[f], "")
                body = old.split("：", 1)[1] if old.startswith("还要补") and "：" in old else ""
                body = "" if "都齐了" in body else body
                out[fm[f]] = "还要补：" + "；".join([x for x in [body] if x] + items)
    return out


_VTODO_PY = r'''
import json, os, sys
H = os.path.expanduser("~")
bd, want = os.path.join(H, "wf-batch", sys.argv[1]), set(sys.argv[2].split("|"))
out = {}
try:
    st = json.load(open(os.path.join(bd, "state.json"), encoding="utf-8"))
except Exception:
    st = {"words": []}
for w in st.get("words") or []:
    f = w.get("word")
    if f in want and w.get("stage") == "voice" and w.get("status") == "blocked" and "没听清" in (w.get("msg") or ""):
        try:
            man = json.load(open(os.path.join(H, "wordfilm-work", f, "brief", "audio", "manifest.json"), encoding="utf-8"))
        except Exception:
            man = {}
        out[f] = [{"scene": k, "name": s.get("name", ""), "text": (s.get("text") or "")[:300], "heard": (s.get("heard") or "")[:300],
                   "miss": s.get("miss") or []} for k, ss in man.items() for s in ss if s.get("miss")][:6]
print("@@TODO@@" + json.dumps(out, ensure_ascii=False))
'''


def _voice_stuck(w):
    """v1.19.0：卡在“配音”、因为要学的单词没听清（例句是画面设置里写的，英文念法是固定的，再试也一样）"""
    return w.get("stage") == "voice" and w.get("status") == "blocked" and "没听清" in (w.get("msg") or "")


def fix_words(batch="", words=()):
    """要补画面的词：批次里卡在“准备”（起草检查没过）、卡在“配音”（例句听不清）的，加上还没轮到、画面也没过起草检查的；
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
            stuck = stuck or _voice_stuck(w)         # v1.19.0：例句配音听不清的，也要重新做画面（换例句）
            if (stuck or word in unc) and word not in out:
                out.append(word)
    for w in words or []:
        if w in unc and w not in out:
            out.append(w)
    return out


# ═══════════ v1.19.0：开工分三步——① 出片前检查 ② 单词检测 ③ 开工 ═══════════
# 点「开工」（「继续」「接着做」也一样）：先检查这台电脑（和「出片环境」里的是同一个检查）；再把这一批还没做过“准备”的词，
# 照流水线“准备”那一步起草检查一遍，纯英文的句子（例句、听力题）先念一遍、听一遍。都没问题才真的开工。
# 有问题的词一个一行，写清楚原因和怎么办：「重新做画面」「更新练习题」「不做这个词」，或者「这几个先不做，开工」。
GO = {"name": "", "state": "", "step": "", "t": 0.0, "end": 0.0, "msg": "", "tok": 0, "nocheck": False}
#   state：env 正在检查电脑 / words 正在检测单词 / bad 有问题、等你处理（step 是 env 或 words）/ start 正在开工 / ok 开工了 / err 开工出错了
_WC_LOCK = threading.Lock()
WC = {"name": "", "tok": 0, "state": "idle", "phase": "", "n": 0, "pn": 0, "pd": 0, "vn": 0, "cur": "", "cached": 0,
      "items": {}, "order": [], "started": 0.0, "finished": 0.0, "error": "", "vwarn": ""}
#   每个词 items[文件夹名] = {st, probs, cached}；st：wait 还没查 / vwait 画面查完、等试听 / ok / bad / err 检查出错 /
#   skipped 这一批不做了 / fixing 交给 AI 在改（tid）/ fixed 改好了（再点「开工」会再查）
WC_P = C.DATA / "word_check.json"            # 查过、没问题的词的“指纹”：画面设置、插图、版本都没变的，下次不再查
WC_VER = "1"
ACK_P = C.DATA / "video_ack.json"            # 做完、停止的批次点了「知道了」（收进「生成历史」）
_ACK = {"d": None}


def _acks():
    if _ACK["d"] is None:
        try:
            _ACK["d"] = json.loads(ACK_P.read_text(encoding="utf-8"))
        except Exception:
            _ACK["d"] = {}
    return _ACK["d"]


def ack_set(name, on=True):
    d = _acks()
    if bool(on) == (name in d):
        return
    if on:
        d[name] = time.time()
    else:
        d.pop(name, None)
    try:
        ACK_P.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def _go_set(tok, **kw):
    with _EC_LOCK:
        if GO["tok"] == tok:
            GO.update(**kw)


def go_clear(name):
    """停止、删除批次时：这一批的开工三步不等了。"""
    with _EC_LOCK:
        if GO["name"] == name:
            GO.update(name="", state="", step="", msg="", tok=GO["tok"] + 1)
    with _WC_LOCK:
        if WC["name"] == name:
            WC.update(name="", state="idle", items={}, order=[], tok=-1)


def go_start(name, nocheck=False):
    """「开工」「继续」「接着做」：后台按 ① ② ③ 走，界面每秒来看一次走到哪儿了。"""
    if not NAME_RE.fullmatch(name or ""):
        return {"ok": False, "msg": "批次名不对"}
    with _EC_LOCK:
        tok = GO["tok"] + 1
        GO.update(name=name, state="env", step="env", t=time.time(), end=0.0, msg="", tok=tok, nocheck=bool(nocheck))
    threading.Thread(target=_go_run, args=(name, tok, bool(nocheck)), daemon=True, name="go-" + name).start()
    return {"ok": True, "msg": "先检查这台电脑和这一批的词，都没问题就开工"}


def _go_run(name, tok, nocheck):
    alive = lambda: GO["tok"] == tok
    try:
        with _EC_LOCK:
            fr = next((k for k, f in EC["fix"].items() if f.get("state") == "running"), "")
        if fr:                                   # 正在装、正在同步：做完 _fix_run 会再叫一次 go_start
            _go_set(tok, state="bad", step="env", msg="正在%s，做完会再检查一遍、接着开工" % FIX_NAME.get(fr, fr))
            return
        envchk_start()                           # ① 出片前检查（正在查的话就等这一次的结果）
        while alive() and EC["state"] == "running":
            time.sleep(0.5)
        if not alive():
            return
        v = EC.get("verdict") or ["bad", "检查没做完"]
        if v[0] != "ok":
            _go_set(tok, state="bad", step="env", msg=v[1])
            return
        if not nocheck:                          # ② 单词检测
            _go_set(tok, state="words", step="words")
            for rnd in range(2):                 # v1.20.0：有问题的词自动处理，不停下来等你：练习题对不上的自动更新、再查一遍
                skip = set(rep_get(name).get("out") or {})
                r = _wordchk(name, tok, alive, skip)
                if not alive():
                    return
                if r.get("error"):
                    _go_set(tok, state="bad", step="words", msg=r["error"])
                    return
                again = _wc_settle(name, tok, rnd)      # 画面的问题退回「画面」，练习题配音听不清退回「出题」
                if not again or not alive():
                    break
            if not alive():
                return
        left = _left_words(name)
        if left is not None and not left:
            _go_set(tok, state="ok", step="start", msg="这一批的词都退回去了，没有要出片的词", end=time.time())
            ack_set(name, False)
            return
        _go_set(tok, state="start", step="start")    # ③ 开工
        ok, msg = batch_op(name, "start")
        _go_set(tok, state="ok" if ok else "err", step="start", msg=msg, end=time.time())
    except Exception as e:
        traceback.print_exc()
        _go_set(tok, state="err", msg="开工出错了：%s" % str(e)[:200], end=time.time())


def _wc_cache():
    try:
        return json.loads(WC_P.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _list_arts(name):
    """这一批清单里每个词的画图脚本（建批次时存在 data/batches/<批次>.tsv）。"""
    out = {}
    try:
        for l in (C.DATA / "batches" / (name + ".tsv")).read_text(encoding="utf-8").splitlines():
            f = l.split("\t")
            if len(f) >= 3 and not l.startswith("#"):
                out[f[1].strip()] = f[2].strip()
    except OSError:
        pass
    if not out:
        try:
            out = pic_words()
        except Exception:
            pass
    return out


def _wc_fp(folder, arts):
    """这个词的“指纹”：画面设置、插图、画图脚本，加上视频技能、总表的版本。都没变、上次查过没问题的，不再查。"""
    import hashlib
    h = hashlib.md5()
    base = C.REPO / EXTRA
    files = [base / "words" / (folder + ".json"), base / "words" / (folder + ".py")]
    files += [base / (a + "_art.py") for a in (arts or "").split(",") if a]
    art = base / "art" / folder
    if art.is_dir():
        files += sorted(art.glob("*.svg"))
    for f in files:
        h.update(f.name.encode("utf-8"))
        try:
            h.update(f.read_bytes())
        except OSError:
            h.update(b"-")
    try:
        import pics
        sv = pics.skill_version()[0]
    except Exception:
        sv = ""
    h.update(("|%s|%s|%s|%s" % (arts, sv, C.STATE.get("version") or "", WC_VER)).encode("utf-8"))
    return h.hexdigest()


def _wc_short(text, n=70):
    t = str(text or "").split("：")[0].strip()
    return t if len(t) <= n else t[:n] + "…"


def _wc_prob(kind, text, short="", extra=None):
    kind = kind if kind in ("pic", "lianxi", "voice", "qvoice", "err") else "pic"
    t = re.sub(r"\s+", " ", str(text or "")).replace("；", "，").strip()[:900]
    d = {"kind": kind, "text": t, "short": short or _wc_short(t)}
    if extra:
        d.update(extra)                         # v1.20.0：听不清的句子：原句 said、听成了 heard、没听出来的词 miss（界面上显示）
    return d


def _wc_voice(m):
    """一句“没听清”→ (种类, 交给 AI 的一条“还要补”, 界面上的一句话, {原句, 听成了, 没听出来的词})。
    例句、句子里的词是画面设置写的；听力题是题目里的。
    v1.20.0：界面上写成“第 1 个例句没听出 populous”；交给 AI 的不再说“别把单词放在句末”（不准：放在句中也会听不清，要换说法）"""
    sc = str(m.get("scene") or "")
    text = re.sub(r"\s+", " ", str(m.get("text") or "")).strip()
    heard = re.sub(r"\s+", " ", str(m.get("heard") or "")).strip()
    miss = [str(x) for x in m.get("miss") or []]
    mw = "、".join(miss) or "要学的单词"
    hd = heard or "（什么都没听出来）"
    ex = {"said": text[:300], "heard": heard[:300], "miss": miss[:6]}
    if sc.startswith("example"):
        k = int(re.sub(r"\D", "", sc) or 0) + 1
        return ("voice", "第 %d 个例句配音听不清：“%s”念出来，语音识别听成了“%s”，%s 没听出来（英文是美式女声念的，同一句每次念得都一样，"
                "再念也不行）。换一个例句：用更常见、更简短的说法，让 %s 念得清楚，英文 ex、中文 exzh 和例句动画也跟着改"
                % (k, text, hd, mw, miss[0] if miss else "这个词"), "第 %d 个例句没听出 %s" % (k, mw), ex)
    if sc.startswith(("lianxi", "daan")):
        return ("qvoice", "练习题里的英文句子配音听不清：“%s”，语音识别听成了“%s”，%s 没听出来。要改题目里的这一句" % (text, hd, mw),
                "练习题的英文句子没听出 %s" % mw, ex)
    return ("voice", "配音里这一句听不清：“%s”，语音识别听成了“%s”，%s 没听出来。换个说法（意思不变）" % (text, hd, mw),
            "有一句没听出 %s" % mw, ex)


def _wc_line(tok, tag, b, seen_end):
    with _WC_LOCK:
        if WC["tok"] != tok:
            return
        it = WC["items"].get(str(b.get("word") or ""))
        if tag == "W" and it is not None:
            probs = [_wc_prob(p.get("kind"), p.get("text")) for p in b.get("probs") or []]
            if b.get("err"):
                probs.append(_wc_prob("err", b["err"]))
            it["probs"] = probs
            it["st"] = "vwait" if (b.get("plan") and not b.get("err")) else ("bad" if probs else "ok")
            WC["pd"] += 1
            WC["cur"] = b.get("word") or ""
        elif tag == "V":
            WC.update(phase="voice", vn=int(b.get("n") or 0))
        elif tag == "VW" and it is not None:
            seen = {p["text"] for p in it["probs"]}
            for m in b.get("miss") or []:
                k, t, sh, ex = _wc_voice(m)
                p = _wc_prob(k, t, sh, ex)
                if p["text"] not in seen:               # 听力题那一句念两遍：只记一次
                    seen.add(p["text"])
                    it["probs"].append(p)
            it["st"] = "bad" if it["probs"] else "ok"
        elif tag == "VERR":
            WC["vwarn"] = str(b.get("msg") or "")[:300]
        elif tag == "ERR":
            WC["error"] = str(b.get("msg") or "")[:300]
        elif tag == "END":
            seen_end.append(1)


def _wordchk(name, tok, alive=lambda: True, skip=()):
    """② 单词检测。返回 {bad: 有问题的词数, error: 检测本身没跑成的原因}。skip：已经退回去的词（不再查）。"""
    try:
        d = live([name])
    except Exception as e:
        d = {"error": str(e)}
    b = next((x for x in d.get("batches") or [] if x.get("name") == name), None)
    if not b or b.get("state") == "error" or b.get("words") is None:
        return {"error": "读不了批次 %s 的词：%s" % (name, (b or {}).get("error") or d.get("error") or d.get("msg") or "WSL 里没有这一批")}
    arts = _list_arts(name)
    skip = set(skip or ())
    pw = [w["word"] for w in b["words"] if w.get("stage") == "prep" and w["word"] not in skip]     # 还没做过“准备”的：从头查
    vw = [w["word"] for w in b["words"] if w.get("stage") == "voice" and w["word"] not in skip]    # 准备好了、还没配音的：只试听
    order = [w["word"] for w in b["words"] if w["word"] in pw or w["word"] in vw]
    # 别的批次正在做的同一个词：画图的文件夹是同一个，这次先不查（查的时候要重画，会打扰它）
    busy = {w["word"] for x in d.get("batches") or [] if x.get("name") != name and x.get("state") in ("running", "pausing", "stopping")
            for w in x.get("words") or [] if w.get("stage") not in ("done", "skipped")}
    fps = {w: _wc_fp(w, arts.get(w, "")) for w in order}
    cache = _wc_cache()
    same = {w for w in order if cache.get(w) == fps[w]}
    tp = [w for w in pw if w not in same and w not in busy]
    tv = [w for w in vw if w not in same and w not in busy]
    with _WC_LOCK:
        WC.update(name=name, tok=tok, state="running", phase="pic" if tp else "voice", n=len(order), pn=len(tp), pd=0, vn=0, cur="",
                  cached=len(same), order=order, started=time.time(), finished=0.0, error="", vwarn="",
                  items={w: {"st": "ok" if w in same else "wait", "probs": [], "cached": w in same} for w in order})
        for w in order:
            if w in busy and w not in same:
                WC["items"][w].update(st="ok", unv=True, note="别的批次正在做这个词：这次没查，开工后照常检查")
    seen_end = []
    if tp or tv:
        try:
            sync_pics()                           # 流水线用的是 WSL 里那一份画面设置：先拷最新的进去
        except Exception:
            pass
        jobs = 3 if len(tp) > 6 else 2
        sh = _fill(WC_SH, NAME=name, P=q("|".join(tp)), V=q("|".join(tv)), J=str(jobs)).replace("@@WC_PY@@", WC_PY)

        def on_line(line):
            m = re.match(r"^@@(\w+)@@ ?(.*)$", line.strip())
            if m:
                try:
                    body = json.loads(m.group(2) or "{}")
                except Exception:
                    body = {}
                _wc_line(tok, m.group(1), body, seen_end)
        rc, tail = wsl_stream(sh, on_line, timeout=min(3600, 240 + 12 * len(tp) + 4 * len(tv)), stop=lambda: not alive())
        if not alive():
            return {"error": "停下了"}
        if not seen_end:
            with _WC_LOCK:
                if not WC["error"]:
                    WC["error"] = "单词检测没跑完（%s）：%s" % (rc, C.mask(" ".join(str(tail).split()))[-300:])
    cache_new = dict(cache)
    with _WC_LOCK:
        if WC["tok"] != tok:
            return {"error": "停下了"}
        for w, it in WC["items"].items():
            if seen_end and it["st"] in ("wait", "vwait"):            # 试听没跑成（vwarn）：画面查过了，配音开工后照常查
                it["st"] = "bad" if it["probs"] else "ok"
                it["unv"] = bool(WC["vwarn"])
            if it["st"] == "ok" and not it.get("cached") and not it.get("unv") and seen_end:
                cache_new[w] = fps[w]
            elif it["st"] in ("bad", "err"):
                cache_new.pop(w, None)
        nbad = sum(1 for it in WC["items"].values() if it["st"] in ("bad", "err"))
        err = WC["error"]
        WC.update(state="error" if err else "done", finished=time.time(), phase="")
    try:
        WC_P.write_text(json.dumps(cache_new, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass
    C.log("单词检测（批次 %s）：%d 个词，%s%s" % (name, len(order), "%d 个要先处理" % nbad if nbad else "都没问题",
                                         "；" + err if err else ("；例句没能先试听：" + WC["vwarn"] if WC["vwarn"] else "")))
    if err:
        return {"error": err, "bad": nbad}
    return {"bad": nbad}


def wc_get():
    """界面要的单词检测情况：交给 AI 改的词，那个任务已经结束、却没改好的，算回“要处理”。"""
    with _WC_LOCK:
        d = json.loads(json.dumps(WC, ensure_ascii=False, default=str))
    tids = {it.get("tid") for it in d["items"].values() if it.get("st") == "fixing" and it.get("tid")}
    if tids:
        live_ids = set()
        try:
            for t in C.q("SELECT id FROM tasks WHERE status IN ('运行中','已暂停','排队')"):
                live_ids.add(t["id"])
        except Exception:
            live_ids = tids
        for w, it in d["items"].items():
            if it.get("st") == "fixing" and it.get("tid") not in live_ids:
                it["st"], it["note"] = "bad", "交给 AI 的那一次没改好（「画面」页的生成历史里看原因），可以再交一次"
                with _WC_LOCK:
                    if w in WC["items"] and WC["items"][w].get("st") == "fixing":
                        WC["items"][w].update(st="bad", note=it["note"])
    d.pop("tok", None)
    d["secs"] = int((d["finished"] or time.time()) - d["started"]) if d["started"] else 0
    return d


def wc_mark(name, words, st, **kw):
    with _WC_LOCK:
        if WC["name"] != name:
            return
        for f in words:
            if f in WC["items"]:
                WC["items"][f].update(st=st, **kw)


def wc_fixed(batch, word):
    """补画面补好了一个词（pics._after_fix 叫）：单词检测里这个词标成“改好了”，再点「开工」会再查一遍。"""
    wc_mark(batch, [folder_of(word)], "fixed", note="改好了")


def wc_lianxi(name, words):
    """「更新练习题」：题目已经出好了，画面设置里的练习题还是旧的（或者没写进去）——换成题目里的那几道，提交、拷进 WSL。"""
    import pics
    fm = {}
    try:
        for r in C.read_index()[1]:
            fm.setdefault(folder_of(r[2]), r[2])
    except Exception:
        pass
    done, noq = [], []
    for f in words:
        w = fm.get(f, f.replace("_", " "))
        if pics.lianxi_qs(w):
            pics.refresh_lianxi(w)
            done.append(w)
        else:
            noq.append(w)
    if done:
        try:
            cid = C.commit_pending("词库：练习题换成题目里的 %s（%d 个词，单词工作台）" % ("、".join(done[:6]), len(done)))
            if cid and C.load_cfg().get("autoPush", True):
                threading.Thread(target=lambda: C.log(C.push()), daemon=True).start()
        except Exception as e:
            C.log("练习题改好了，提交没成功（%s）：下次一起传" % str(e)[:120])
        try:
            sync_pics()
        except Exception:
            pass
        wc_mark(name, [folder_of(w) for w in done], "fixed", note="练习题换成了题目里的")
    msg = ("练习题更新好了：%s" % "、".join(done)) if done else ""
    if noq:
        msg += ("；" if msg else "") + "%s 的题目还不全：先到「出题」把题目出好" % "、".join(noq)
    return {"ok": bool(done), "msg": msg}


WC_SH = r"""BD="$HOME/wf-batch/{NAME}"
[ -f "$BD/list.tsv" ] || { echo '@@ERR@@ {"msg": "WSL 里没有批次 {NAME}（可能已经删掉了）"}'; exit 3; }
[ -f "$HOME/lwb/scripts/wsl/bcommon.sh" ] || { echo '@@ERR@@ {"msg": "WSL 里没有批量出片的脚本：到「出片环境」点「同步到 WSL」"}'; exit 3; }
set -a; eval "$(grep -E '^(GPU|VOICE_GPU|MIX_FALLBACK)=[0-9]+$' "$BD/config.env" 2>/dev/null)"; set +a
. "$HOME/lwb/scripts/wsl/bcommon.sh"
export TABLE SYL PYTHONUNBUFFERED=1 WORDFILM_ZV_DEVICE=cpu
python3 - "$BD" {P} {V} {J} <<'PYWC'
@@WC_PY@@
PYWC
"""

WC_PY = r'''
# 单词工作台 v1.19.0：开工前的单词检测（只看，不改流水线的进度）
import glob, json, os, re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
bd = sys.argv[1]
PW = [x for x in sys.argv[2].split('|') if x]
VW = [x for x in sys.argv[3].split('|') if x]
JN = max(1, min(4, int(sys.argv[4] or 2)))
H = os.path.expanduser('~')
S = os.environ.get('S') or os.path.join(H, 'skills', 'word-construction-video')
LWB = os.environ.get('LWB') or os.path.join(H, 'lwb')
WORK = os.environ.get('WORK') or os.path.join(H, 'wordfilm-work')
JOBS = os.environ.get('JOBS') or os.path.join(H, 'wf-jobs')
TABLE, SYL = os.environ.get('TABLE') or '', os.environ.get('SYL') or ''
PC = os.path.join(H, 'wf-precheck', os.path.basename(bd.rstrip('/')))
os.makedirs(PC, exist_ok=True)


def say(tag, **kw):
    print('@@%s@@ %s' % (tag, json.dumps(kw, ensure_ascii=False)), flush=True)


def tail(p, n=3):
    try:
        ls = [l.strip() for l in open(p, encoding='utf-8', errors='replace').read().splitlines() if l.strip()]
    except OSError:
        return ''
    return ' '.join(ls[-n:])[-400:]


def kitfile(rel):
    for d in (os.path.join(H, 'kit-extra'), os.path.join(H, 'kit')):
        f = os.path.join(d, rel)
        if os.path.isfile(f):
            return f
    return None


rows = {}
for l in open(os.path.join(bd, 'list.tsv'), encoding='utf-8'):
    if not l.strip() or l.lstrip().startswith('#'):
        continue
    c = l.rstrip('\n').replace('\r', '').split('\t')
    if len(c) >= 3 and c[1].strip():
        rows[c[1].strip()] = {'no': c[0].strip() or '1', 'arts': c[2].strip()}


def prep(w):
    """和流水线“准备”那一步一样：画图 → 画面设置 → 缺图 → 起草检查（不转画风、不改配音稿）"""
    r = rows.get(w) or {'no': '1', 'arts': ''}
    out = {'word': w, 'probs': [], 'plan': False}

    def P(kind, text):
        out['probs'].append({'kind': kind, 'text': str(text)[:900]})
    try:
        J, A = os.path.join(JOBS, w), os.path.join(WORK, w, 'art')
        os.makedirs(os.path.join(WORK, w), exist_ok=True)
        os.makedirs(J, exist_ok=True)
        link = os.path.join(J, w)
        if os.path.islink(link) or not os.path.exists(link):
            if os.path.islink(link):
                os.remove(link)
            os.symlink(os.path.join(WORK, w), link)
        log = os.path.join(J, 'precheck.log')
        open(log, 'w').close()

        def run(cmd, f=log):
            with open(f, 'a', encoding='utf-8') as fh:
                return subprocess.run(cmd, cwd=os.path.join(S, 'scripts'), stdout=fh, stderr=subprocess.STDOUT,
                                      stdin=subprocess.DEVNULL).returncode
        wp = kitfile('words/%s.py' % w)
        if not wp:
            P('pic', '没有画面设置（words/%s.py）：这个词要先做画面' % w)
            return out
        shutil.rmtree(A, ignore_errors=True)
        os.makedirs(A)
        for f in glob.glob(os.path.join(S, 'references', 'scenes', '*.svg')):
            shutil.copy(f, A)
        if run(['python3', 'poses.py', A, '--motion']):
            out['err'] = '画会动的人出错（poses.py）：' + tail(log)
            return out
        for x in [a for a in r['arts'].split(',') if a]:
            ap = kitfile(x + '_art.py')
            if not ap:
                P('pic', '没有画图脚本 %s_art.py' % x)
                return out
            if run(['python3', ap, A]):
                P('pic', '画图脚本 %s_art.py 跑不起来：%s' % (x, tail(log)))
                return out
        edits = os.path.join(WORK, 'edits_%s.json' % w)
        if run(['python3', wp, edits]):
            P('pic', '画面设置的程序跑不起来：' + tail(log))
            return out
        m = subprocess.run(['python3', os.path.join(LWB, 'scripts', 'wsl', 'missing_art.py'), w], capture_output=True, text=True)
        if m.returncode:
            P('pic', '画面设置里用到的图没画出来：' + '，'.join(l.strip() for l in m.stdout.splitlines() if l.strip())[:700])
        dl = os.path.join(J, 'precheck_draft.log')
        open(dl, 'w').close()
        cmd = ['python3', 'run.py', '--table', TABLE] + (['--syl', SYL] if SYL and os.path.isfile(SYL) else []) + \
            ['--words', w.replace('_', ' '), '--number', r['no'], '--out', os.path.join(PC, 'out'), '--edits', edits,
             '--edition', 'brief', '--draft-only', '--no-preview', '--work', J]
        if run(cmd, dl):
            out['err'] = '起草出错：' + tail(dl)
            return out
        line = ''
        for l in open(dl, encoding='utf-8', errors='replace'):
            if '还要补' in l:
                line = l.strip()
        plan = os.path.join(WORK, w, 'brief', 'plan.json')
        out['plan'] = os.path.isfile(plan)
        if not line:
            out['err'] = '起草检查没出结果：' + tail(dl, 2)
        elif '都齐了' not in line:
            ok = subprocess.run(['python3', os.path.join(LWB, 'scripts', 'wsl', 'label_ok.py'), line, plan],
                                capture_output=True).returncode == 0
            if not ok:
                body = re.sub(r'^\s*还要补[:：]\s*', '', line)
                for it in [x.strip() for x in re.split(r'[；;]', body) if x.strip()]:
                    P('lianxi' if it.startswith('练习题') else 'pic', it)
    except Exception as e:
        out['err'] = '检查本身出错了：%s' % e
    return out


def voice(words):
    """纯英文的句子（例句、听力题）先念一遍、听一遍：和配音那一步一样，五个字母以上的单词没听出来就记下。
    中英混着的句子不用查：配音时拼着念、念不清会自动换念法，不会停下来。"""
    sys.path.insert(0, os.path.join(S, 'scripts'))
    try:
        import synth
    except BaseException as e:
        say('VERR', msg='配音的程序打不开（%s）' % str(e)[:200])
        return
    segs, lex, base, who = {}, {}, None, {}
    for w in words:
        try:
            plan = json.load(open(os.path.join(WORK, w, 'brief', 'plan.json'), encoding='utf-8'))
        except Exception:
            continue
        if base is None:
            base = {k: v for k, v in plan.items() if k not in ('scenes', 'word', 'lexicon')}
        for k, v in (plan.get('lexicon') or {}).items():
            lex.setdefault(k, v)
        who[w] = str(plan.get('word') or w.replace('_', ' '))
        wl = re.sub(r'[^a-z]', '', who[w].lower())
        for sc, spec in (plan.get('scenes') or {}).items():
            items = ([('intro', spec['intro'])] if spec.get('intro') else []) + \
                [('seg%d' % i, t) for i, t in enumerate(spec.get('segs') or [])]
            for name, seg in items:
                t = str(seg.get('t', '')) if isinstance(seg, dict) else str(seg)
                if synth.PHON_ONLY.match(t):
                    if 'qz' + wl not in re.sub(r'[^a-z]', '', t.lower()):
                        continue                  # 念一块的音：不查；只查整个词
                elif synth.CJK.search(t) or not re.search(r'[A-Za-z]{5,}', t):
                    continue
                segs['%s@@%s@@%s' % (w, sc, name)] = {'segs': [seg]}
    say('V', n=len(segs))
    got = {}
    if segs:
        od = os.path.join(PC, 'voice')
        shutil.rmtree(od, ignore_errors=True)
        try:
            man, _ = synth.synth(dict(base or {}, word='', lexicon=lex, scenes=segs), od)
        except BaseException as e:
            say('VERR', msg='例句没能先念一遍（%s）' % str(e)[:300])
            return
        for key, ss in (man or {}).items():
            try:
                w, sc, name = key.split('@@')
            except ValueError:
                continue
            for s in ss:
                said = s.get('said') or s.get('text') or ''
                miss = list(s.get('miss') or [])
                if synth.PHON_ONLY.match(said):
                    try:
                        miss = synth.check(said, s.get('heard') or '', who.get(w, w))[0]
                    except Exception:
                        miss = []
                if miss:
                    got.setdefault(w, []).append({'scene': sc, 'name': name, 'text': s.get('text') or '',
                                                  'heard': s.get('heard') or '', 'miss': miss})
    for w in words:
        say('VW', word=w, miss=got.get(w, []))


say('N', pic=len(PW), voice=len(VW))
good = set(VW)
if PW:
    with ThreadPoolExecutor(max_workers=JN) as ex:
        futs = {ex.submit(prep, w): w for w in PW}
        for f in as_completed(futs):
            try:
                res = f.result()
            except Exception as e:
                res = {'word': futs[f], 'probs': [], 'err': '检查本身出错了：%s' % e}
            if res.get('plan') and not res.get('err'):
                good.add(res['word'])
            say('W', **res)
voice([w for w in PW + VW if w in good])
say('END')
'''


# ═══════════ v1.20.0：能做的就做，不能做的退回去——没有“等你选”的中间状态 ═══════════
# 选词：只列现在就能出视频的词（选上的、题目画面都好了、还没有视频、也不在别的批次里）。别的写进建批次时的汇报。
# 开工前单词检测、出片中卡在“准备”“配音”（画面的问题）：自动从这一批拿掉、退回「画面」（或「出题」），别的词照常做。
# 每一批一份汇报（data/video_reports.json）：建批次时没放进去的词、检测时和出片时退回去的词，一个一行写原因。
REP_P = C.DATA / "video_reports.json"
INB_P = C.DATA / "video_inbatch.json"        # {批次: [[文件夹名, 阶段, 状态], ...]}：最近一次读到的每个批次里每个词在哪一步
_REP = {"lock": threading.RLock(), "d": None}
_INB = {"lock": threading.Lock(), "d": None}


def _reps():
    if _REP["d"] is None:
        try:
            _REP["d"] = json.loads(REP_P.read_text(encoding="utf-8"))
        except Exception:
            _REP["d"] = {}
    return _REP["d"]


def rep_get(name):
    with _REP["lock"]:
        return json.loads(json.dumps(_reps().get(name) or {}, ensure_ascii=False))


def rep_edit(name, fn):
    with _REP["lock"]:
        r = _reps().setdefault(name, {"t": time.time(), "out": {}})
        r.setdefault("out", {})
        fn(r)
        try:
            REP_P.write_text(json.dumps(_reps(), ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass


def rep_drop(name):
    with _REP["lock"]:
        if _reps().pop(name, None) is not None:
            try:
                REP_P.write_text(json.dumps(_reps(), ensure_ascii=False), encoding="utf-8")
            except Exception:
                pass


def _inb():
    if _INB["d"] is None:
        try:
            _INB["d"] = json.loads(INB_P.read_text(encoding="utf-8"))
        except Exception:
            _INB["d"] = {}
    return _INB["d"]


def _inb_note(raw_batches):
    """live() 每次读到所有批次：记下每个批次里每个词在哪一步（WSL 没开时，选词列表照最后一次的算）。"""
    d = {b["name"]: b.get("ws") or [] for b in raw_batches if b.get("name") and "ws" in b}
    with _INB["lock"]:
        if d != _inb():
            _INB["d"] = d
            try:
                INB_P.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
            except Exception:
                pass


def inbatch():
    """(在批次里、还没做完的词 {文件夹名: 批次}, 在批次里做好了的词 {文件夹名})"""
    pend, done = {}, set()
    with _INB["lock"]:
        d = dict(_inb())
    ign = _vdel()                                   # v1.21.0：旧版视频删掉了的词，当时那几个批次里的“做好了”不算数
    for name, ws in d.items():
        for x in ws:
            f, st = x[0], x[1] if len(x) > 1 else ""
            if st == "done":
                if name not in ((ign.get(f) or {}).get("b") or []):
                    done.add(f)
            elif st != "skipped":
                pend.setdefault(f, name)
    return pend, done


def pick_info():
    """出视频的选词：ready 现在就能出视频的（列出来、默认全勾）；别的分好类，建批次时写进汇报。"""
    import pool
    try:
        import pics
        todo = pics.todo_all()
    except Exception:
        todo = {}
    items = [i for i in pool.items()["items"] if i.get("picked")]
    pend, done = inbatch()
    out = {"n": len(items), "ready": [], "video": [], "inb": [], "pic": [], "q": []}
    for i in items:
        w, f = i["word"], folder_of(i["word"])
        if i.get("video") or f in done:
            out["video"].append(w)
        elif f in pend:
            out["inb"].append([w, pend[f]])
        elif not i.get("q"):
            out["q"].append([w, "出题没过" if i.get("manual") else "还没有题目"])
        elif i.get("manual"):
            out["q"].append([w, "题目要改（在「出题」的「没过的词」里）"])
        elif not i.get("pic"):
            out["pic"].append([w, "上次没做成" if i.get("picfail") else "还没有画面"])
        elif i.get("picTodo"):
            ln = todo.get(w, "")
            n = len([x for x in re.split(r"[；;]", ln.split("：", 1)[-1]) if x.strip()]) if ln else 0
            out["pic"].append([w, ("画面还要补 %d 处" % n) if n else "画面还没过起草检查"])
        else:
            out["ready"].append({"word": w, "meaning": (i.get("meaning") or "")[:40]})
    return out


def _real_words():
    fm = {}
    try:
        for r in C.read_index()[1]:
            fm.setdefault(folder_of(r[2]), r[2])
    except Exception:
        pass
    return fm


_MARK_PY = r'''
import json, os, sys, time
bd, data = sys.argv[1], json.loads(sys.argv[2])
def alive():
    try:
        os.kill(int(open(os.path.join(bd, "pipeline.pid")).read().strip()), 0)
        return True
    except Exception:
        return False
if alive():
    os.makedirs(os.path.join(bd, "cmd"), exist_ok=True)
    for i, (w, why) in enumerate(data.items()):
        open(os.path.join(bd, "cmd", "%d.json" % (time.time_ns() + i)), "w", encoding="utf-8").write(
            json.dumps({"op": "skip", "word": w, "why": why}, ensure_ascii=False))
    print("MARKED cmd")
else:
    sp = os.path.join(bd, "state.json")
    if os.path.exists(sp):
        st = json.load(open(sp, encoding="utf-8"))
    else:
        rows = []
        for l in open(os.path.join(bd, "list.tsv"), encoding="utf-8"):
            if not l.strip() or l.lstrip().startswith("#"):
                continue
            c = l.rstrip("\n").replace("\r", "").split("\t")
            if len(c) >= 3 and c[1].strip():
                rows.append({"no": c[0].strip(), "word": c[1].strip(), "arts": c[2].strip(), "note": c[3].strip() if len(c) > 3 else ""})
        st = {"words": [dict(r, stage="prep", status="waiting", msg="", tries={}, t={}) for r in rows]}
    for w in st["words"]:
        if w["word"] in data:
            w["stage"], w["status"], w["msg"] = "skipped", "", data[w["word"]]
    st["updated"] = time.time()
    json.dump(st, open(sp + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(sp + ".tmp", sp)
    print("MARKED state")
'''


def _mark_out(name, whys):
    """这一批里这些词不做了（{文件夹名: 为什么}）：流水线在跑就发指令，没在跑就直接写进 state.json（没开过工的也建一份）。"""
    if not whys:
        return True
    rc, t = wsl("BD=\"$HOME/wf-batch/%s\"; [ -d \"$BD\" ] || exit 3\npython3 - \"$BD\" %s <<'PYMARK'\n%s\nPYMARK\n"
                % (name, q(json.dumps(whys, ensure_ascii=False)), _MARK_PY), 90)
    return rc == 0 and "MARKED" in t


def send_out(name, groups, when):
    """把词从批次 name 里拿掉、退回去。groups：[(文件夹名, 去哪儿 pic/q, 界面上一句话, 交给 AI 的几条, 卡在哪一步)]。
    pic：画面那一步记成“还要补”（补画面时 AI 拿到这几条）；q：放进「出题」的「没过的词」（写清原因）。"""
    if not groups:
        return
    fm = _real_words()
    groups = [tuple(g) + ((),) * (6 - len(g)) for g in groups]
    whys, back = {}, {}
    for f, to, short, items, stage, voice in groups:
        w = fm.get(f, f.replace("_", " "))
        whys[f] = ("退回「画面」：" if to == "pic" else "退回「出题」：") + short[:160]
        if to == "pic":
            back[w] = list(dict.fromkeys(items or [short]))
        else:
            try:
                C.x("INSERT OR REPLACE INTO manual(word,errors,draft,attempts,ts,source) VALUES(?,?,?,?,?,?)",
                    (w, json.dumps(items or [short], ensure_ascii=False), "", 0, C.now(), "出视频退回"))
            except Exception:
                pass
    if back:
        try:
            import pics
            pics.send_back(back, "批次 %s %s" % (name, "单词检测" if when == "check" else "出片时"))
        except Exception as e:
            C.log("退回「画面」没记上（%s）" % str(e)[:120])
    _mark_out(name, whys)

    def upd(r):
        for f, to, short, items, stage, voice in groups:
            r["out"][f] = {"word": fm.get(f, f.replace("_", " ")), "to": to, "why": short[:200], "when": when,
                           "stage": stage, "t": time.time(), "items": list(dict.fromkeys(str(x)[:400] for x in (items or [])))[:8],
                           "voice": [{"said": v.get("said", ""), "heard": v.get("heard", ""), "miss": v.get("miss") or []}
                                     for v in (voice or []) if v.get("said")][:6]}
    rep_edit(name, upd)
    C.log("批次 %s：%d 个词退回去了（%s）：%s" % (name, len(groups), "单词检测" if when == "check" else "出片时卡住",
                                          "；".join("%s %s" % (fm.get(g[0], g[0]), g[2][:40]) for g in groups[:12])))


def _prob_route(probs):
    """单词检测查出来的问题 → (去哪儿 pic / q / lx（练习题自动更新） / None（检测没跑成，开工后照常查）, 一句话, 交给 AI 的几条, 听不清的句子)"""
    kinds = {p.get("kind") for p in probs}
    pic = [p for p in probs if p.get("kind") in ("pic", "voice")]
    if pic:
        return "pic", pic[0].get("short") or _wc_short(pic[0]["text"]), [p["text"] for p in pic], [p for p in pic if p.get("said")]
    qv = [p for p in probs if p.get("kind") == "qvoice"]
    if qv:
        return "q", qv[0].get("short") or "练习题的英文句子听不清", [p["text"] for p in qv], qv
    if "lianxi" in kinds:
        return "lx", "练习题和题目对不上", [p["text"] for p in probs if p.get("kind") == "lianxi"], []
    return None, "", [], []


def _wc_settle(name, tok, rnd):
    """单词检测完了：练习题对不上、题目有了的——自动更新练习题、再查一遍；画面的问题——退回「画面」；练习题配音听不清——退回「出题」。
    返回要再查一遍的词（练习题刚更新的）。"""
    fm = _real_words()
    with _WC_LOCK:
        if WC["tok"] != tok:
            return []
        bad = [(f, list(it.get("probs") or [])) for f, it in WC["items"].items() if it.get("st") in ("bad", "err")]
    groups, lx, again, noq = [], [], [], []
    import pics
    for f, probs in bad:
        to, short, items, voice = _prob_route(probs)
        if to is None:
            wc_mark(name, [f], "ok", unv=True, note="检测没跑成（%s），开工后照常检查" % _wc_short(probs[0]["text"] if probs else "", 40))
            continue
        if to == "lx":
            w = fm.get(f, f.replace("_", " "))
            if rnd == 0 and pics.lianxi_qs(w):
                lx.append(w)
                again.append(f)
                continue
            to, short = "q", "题目还不全：先把题目出好" if not pics.lianxi_qs(w) else "练习题更新了还是对不上"
        groups.append((f, to, short, items, "", voice))
    if lx:
        for w in lx:
            pics.refresh_lianxi(w)
        try:
            cid = C.commit_pending("词库：练习题换成题目里的 %s（%d 个词，开工前单词检测自动更新）" % ("、".join(lx[:6]), len(lx)))
            if cid and C.load_cfg().get("autoPush", True):
                threading.Thread(target=lambda: C.log(C.push()), daemon=True).start()
        except Exception as e:
            C.log("练习题改好了，提交没成功（%s）：下次一起传" % str(e)[:120])
        rep_edit(name, lambda r: r.__setitem__("lx", sorted(set((r.get("lx") or []) + lx))))
        C.log("批次 %s：练习题和题目对不上，自动换成题目里的：%s；再查一遍" % (name, "、".join(lx)))
    if groups:
        send_out(name, groups, "check")
        wc_mark(name, [g[0] for g in groups], "out")
    return again


def _left_words(name):
    """这一批还要做的词（不算做好的、退回去的）。读不了返回 None。"""
    try:
        d = live([name])
    except Exception:
        return None
    b = next((x for x in d.get("batches") or [] if x.get("name") == name), None)
    if not b or b.get("words") is None:
        return None
    out = set(rep_get(name).get("out") or {})
    return [w["word"] for w in b["words"] if w.get("stage") not in ("done", "skipped") and w["word"] not in out]


# 出片中卡住、是画面的问题（准备卡住；配音时例句听不清）：自动拿出这一批、退回「画面」，别的词接着做
_AB = {"lock": threading.Lock(), "busy": False, "thread": None}


def _pic_stuck(w):
    m = w.get("msg") or ""
    return w.get("status") == "blocked" and (w.get("stage") == "prep" or (w.get("stage") == "voice" and "没听清" in m))


def auto_back(batches):
    """batches：live() 给界面的批次（带 words）。卡在画面问题上的词退回去。"""
    for b in batches:
        ws = [w for w in b.get("words") or [] if _pic_stuck(w)]
        if not ws:
            continue
        name = b["name"]
        done = set(rep_get(name).get("out") or {})
        ws = [w for w in ws if w["word"] not in done]
        if not ws:
            continue
        try:
            todo = prep_todo(name, [w["word"] for w in ws])
        except Exception:
            todo = {}
        fm = _real_words()
        groups = []
        for w in ws:
            f, real = w["word"], fm.get(w["word"], w["word"].replace("_", " "))
            stage = STG_CN.get(w.get("stage"), "")
            if w.get("stage") == "voice":
                ms = w.get("miss") or []
                vs = [_wc_voice(m) for m in ms]
                if vs and all(v[0] == "qvoice" for v in vs):
                    groups.append((f, "q", vs[0][2], [v[1] for v in vs], stage, [v[3] for v in vs]))
                    continue
                items = [v[1] for v in vs if v[0] != "qvoice"] or pics_items(todo.get(real, "")) or ["例句配音有要学的单词没听清：换一个说法"]
                short = (vs[0][2] if vs else "例句配音没听清")
            else:
                vs = []
                line = todo.get(real, "")
                items = pics_items(line)
                msg = _plain(w.get("msg"))
                if not items:
                    items = [re.sub(r"^起草检查没过[:：]\s*", "", msg)[:400] or "准备那一步卡住了"]
                short = ("画面还要补 %d 处" % len(items)) if msg.startswith("起草检查没过") else _wc_short(msg, 60)
            groups.append((f, "pic", short, items, stage, [v[3] for v in vs if v[0] != "qvoice"]))
        send_out(name, groups, "run")


def pics_items(line):
    try:
        import pics
        return pics._items(line)
    except Exception:
        return []


def _auto_back_bg(names):
    with _AB["lock"]:
        if _AB["busy"]:
            return
        _AB["busy"] = True

    def go():
        try:
            d = live(names, auto=False)
            auto_back([b for b in d.get("batches") or [] if b.get("name") in names])
        except Exception:
            traceback.print_exc()
        finally:
            with _AB["lock"]:
                _AB["busy"] = False
    threading.Thread(target=go, daemon=True, name="video-autoback").start()


def _wsl_up():
    """WSL 里出片的 Linux 现在开着没有（不为这个去开它）。"""
    if not has_wsl():
        return False
    try:
        r = subprocess.run(["wsl", "-l", "--running", "-q"], capture_output=True, timeout=20, creationflags=NOWIN)
        return vcfg()["distro"] in [l.strip().strip("\x00").strip() for l in _dec(r.stdout).splitlines()]
    except Exception:
        return False


def _watcher():
    """你不在「出视频」页时，软件自己每分钟看一次：有卡在画面问题上的词就退回去。"""
    while True:
        time.sleep(60)
        try:
            with _INB["lock"]:
                have = bool(_inb())
            if have and _wsl_up():
                live([])
        except Exception:
            pass


def watch_start():
    with _AB["lock"]:
        t = _AB["thread"]
        if t and t.is_alive():
            return
        _AB["thread"] = threading.Thread(target=_watcher, daemon=True, name="video-watch")
        _AB["thread"].start()
