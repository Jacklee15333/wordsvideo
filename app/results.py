# -*- coding: utf-8 -*-
"""单词工作台 · 出题、画面的结果：给界面显示，也存成文件。

存成文件的地方＝成果文件夹（就是出片文件夹，设置里的 video.winDir，默认 D:\\构词视频）：
  题目\\<单词>.xlsx                  每个词出好题目就自动存一个（重出会覆盖）
  题目\\题目_<时间>_<N>个词.xlsx      点「合成一个 Excel」时存，选上的词一起
  画面\\<单词>\\*.svg                 画面里的图：AI 做的从词库拷过来；kit 里的在 WSL 里画出来
词库里的原件照旧：题目在 词库/总表视频细节数据/词/<首字母>/<单词>.json，AI 做的画面在 词库/画面设置/，都会上传 GitHub。
"""
import json, os, re, shutil, sys, time
from pathlib import Path

import core as C
import video as V

KIT_DIR = "引擎/视频/references/kit-7A-U4"


def out_root():
    return Path(V.vcfg()["winDir"])


def qdir():
    return out_root() / "题目"


def pdir():
    return out_root() / "画面"


def fname(word):
    """当文件名用：Windows 不许的字符换成 _。"""
    return re.sub(r'[\\/:*?"<>|]+', "_", word).strip(" .") or "word"


def _index():
    _, rows = C.read_index()
    by = {}
    for r in rows:
        by.setdefault(r[2], []).append(r)
    return by


_ORIG = {"key": None, "q": {}}


def _orig(word):
    """“总表有”的词：题目原来就写在总表里（题目1…题目7、答案 这几列），不在细节数据的文件里。读一次记住。"""
    p = C.REPO / C.STATE["xlsx"] if C.STATE.get("xlsx") else None
    if not p or not p.exists():
        return None
    st = p.stat()
    key = (str(p), st.st_size, int(st.st_mtime))
    if _ORIG["key"] != key:
        import openpyxl
        ws = openpyxl.load_workbook(str(p), read_only=True)["拆分结果"]
        it = ws.iter_rows(values_only=True)
        h = [str(v) if v else "" for v in next(it)]
        ix = {k: i for i, k in enumerate(h)}
        cols = ["题目%d" % k for k in range(1, 8)] + ["答案"]
        q = {}
        if all(c in ix for c in cols) and "单词" in ix:
            for r in it:
                w = str(r[ix["单词"]] or "").strip()
                if w and w not in q and r[ix["题目1"]]:
                    q[w] = {c: str(r[ix[c]] or "") for c in cols}
        _ORIG.update(key=key, q=q)
    return _ORIG["q"].get(word)


def _rec(word, by=None):
    """这个词在词库里的记录（题目、画面……）和它的相对路径。题目原来就在总表里的，也拿过来。"""
    rs = (by or _index()).get(word) or []
    rel = next((r[6] for r in rs if len(r) > 6 and r[6]), "")
    rec = {}
    if rel:
        p = C.REPO / C.D / rel
        try:
            rec = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
        except Exception:
            rec = {}
    if not rec.get("题目") and rs and any(r[4] == "总表有" for r in rs):
        try:
            o = _orig(word)
        except Exception:
            o = None
        if o:
            rec = dict(rec, 题目=o, 题目生成=rec.get("题目生成") or "总表里原来就有")
            rel = rel or ("总表（%s）" % C.STATE.get("version", ""))
    return rec, rel


# ═══════════════════════ 题目 ═══════════════════════
def _cell(c):
    o = {"type": "", "ask": "", "listen": "", "zh": "", "stem": [], "opts": [], "kd": ""}
    for ln in str(c or "").split("\n"):
        m = re.match(r"^【([^】]+)】\s*(.*)$", ln)
        if m:
            o["type"], o["ask"] = m.group(1), m.group(2)
            continue
        m = re.match(r"^([A-D])[.．]\s*(.*)$", ln)
        if m:
            o["opts"].append("%s. %s" % (m.group(1), m.group(2)))
            continue
        m = re.match(r"^(听|中文|题干|考点)[：:]\s*(.*)$", ln)
        if m:
            k = {"听": "listen", "中文": "zh", "题干": "stem", "考点": "kd"}[m.group(1)]
            if k == "stem":
                o["stem"].append(m.group(2))
            else:
                o[k] = m.group(2)
    return o


def _answers(c):
    out, k = {}, 0
    for ln in str(c or "").split("\n"):
        m = re.match(r"^【(\d)】\s*(.*)$", ln)
        if m:
            k = int(m.group(1))
            out[k] = {"a": m.group(2), "w": ""}
            continue
        m = re.match(r"^(讲解|解析)[：:]\s*(.*)$", ln)
        if m and k:
            out[k]["w"] = m.group(2)
    return out


def q_rows(word, rec):
    """一个词的题目 → Excel 的行（一题一行）。"""
    t = (rec or {}).get("题目") or {}
    A = _answers(t.get("答案"))
    rows = []
    for k in range(1, 8):
        q = _cell(t.get("题目%d" % k))
        if not q["type"]:
            continue
        a = A.get(k) or {}
        rows.append([word, k, q["type"], q["ask"], q["listen"], q["zh"], "\n".join(q["stem"]), "\n".join(q["opts"]),
                     a.get("a", ""), a.get("w", ""), q["kd"]])
    return rows


HEAD = ["单词", "题号", "题型", "问题", "听力原文", "中文", "题干", "选项", "答案", "讲解", "考点"]
WIDTH = [14, 6, 12, 22, 34, 22, 40, 34, 12, 40, 10]


def write_xlsx(path, pairs):
    """pairs：[(单词, 记录)]。存成一个 Excel：「题目」一页，一题一行。"""
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "题目"
    ws.append(HEAD)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="E8EEF6")
    n = 0
    for word, rec in pairs:
        for r in q_rows(word, rec):
            ws.append(r)
            n += 1
    for i, w in enumerate(WIDTH, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp.xlsx")
    wb.save(str(tmp))
    os.replace(str(tmp), str(path))
    return n


def export_word(word, rec=None):
    """出好题目就调：存 题目\\<单词>.xlsx。没有题目返回 None。"""
    if rec is None:
        rec, _ = _rec(word)
    if not (rec or {}).get("题目"):
        return None
    p = qdir() / (fname(word) + ".xlsx")
    write_xlsx(p, [(word, rec)])
    return p


def export_words(words):
    by = _index()
    pairs = [(w, _rec(w, by)[0]) for w in words]
    pairs = [(w, r) for w, r in pairs if r.get("题目")]
    if not pairs:
        return {"ok": False, "msg": "选上的词里还没有出好题目的"}
    p = qdir() / ("题目_%s_%d个词.xlsx" % (time.strftime("%Y%m%d-%H%M"), len(pairs)))
    try:
        n = write_xlsx(p, pairs)
    except PermissionError:
        return {"ok": False, "msg": "存不进去：%s 是不是在 Excel 里开着？关掉再点" % p}
    except Exception as e:
        return {"ok": False, "msg": "没存成：%s" % e}
    return {"ok": True, "msg": "存好了：%d 个词、%d 道题 → %s" % (len(pairs), n, p), "path": str(p)}


def q_items(words):
    """给「出题结果」显示：每个词的题目、是谁出的、存在哪儿。"""
    by = _index()
    man = set(C.manual_words())
    out = []
    for w in words:
        rs = by.get(w) or []
        rec, rel = _rec(w, by)
        has = bool(rec.get("题目"))
        x = qdir() / (fname(w) + ".xlsx")
        if has and not x.exists():                      # 以前出的题还没存过 Excel：补一个
            try:
                export_word(w, rec)
            except Exception:
                pass
        out.append({"word": w, "meaning": rs[0][3] if rs and len(rs[0]) > 3 else "", "has": has, "manual": w in man,
                    "orig": bool(rs) and not has and all(r[4] == "总表有" for r in rs),
                    "gen": rec.get("题目生成") or "", "rel": ((C.D + "/" + rel) if rel.endswith(".json") else rel) if rel else "",
                    "xlsx": str(x) if x.exists() else "", "rec": {"题目": rec.get("题目")} if has else None})
    return out


# ═══════════════════════ 画面 ═══════════════════════
def _kit_scripts():
    """kit 里的词 → 画图脚本名（不带 _art.py），照批量出片的清单。"""
    out = {}
    p = C.REPO / V.KIT_LIST
    if p.exists():
        for l in p.read_text(encoding="utf-8").splitlines():
            f = l.split("\t")
            if len(f) >= 3 and not l.startswith("#"):
                out[f[1].strip()] = [s.strip() for s in f[2].split(",") if s.strip()]
    return out


def p_items(words):
    by = _index()
    pw = V.pic_words()
    kit = _kit_scripts()
    pf = {r["word"]: r for r in C.q("SELECT word, errors FROM picfail")}
    out = []
    for w in words:
        f = V.folder_of(w)
        rs = by.get(w) or []
        rec, _ = _rec(w, by)
        ai = (C.REPO / V.EXTRA / "words" / (f + ".json")).exists()
        src = "ai" if ai else ("kit" if f in pw else "")
        d = pdir() / fname(w)
        files = sorted(x.name for x in d.glob("*.svg")) if d.exists() else []
        used = files
        if src == "kit" and files:                  # kit 的画图脚本几个词共用：先挑这个词自己的画面设置里点了名的
            try:
                code = (C.REPO / KIT_DIR / "words" / (f + ".py")).read_text(encoding="utf-8")
                used = [n for n in files if re.search(r"['\"/]%s(?:_f\d+)?(?:\.svg)?['\"]" % re.escape(re.sub(r"_f\d+$", "", n[:-4])), code)]
            except Exception:
                used = files
        where = (V.EXTRA + "/words/" + f + ".json") if ai else ((KIT_DIR + "/words/" + f + ".py") if src == "kit" else "")
        err = ""
        if w in pf:
            try:
                err = "；".join(json.loads(pf[w]["errors"] or "[]"))[:300]
            except Exception:
                err = str(pf[w]["errors"])[:300]
        out.append({"word": w, "meaning": rs[0][3] if rs and len(rs[0]) > 3 else "", "q": bool(rec.get("题目")) or (bool(rs) and all(r[4] == "总表有" for r in rs)),
                    "pic": f in pw, "src": src, "where": where, "scripts": kit.get(f, []),
                    "check": rec.get("检查") or "", "gen": rec.get("画面生成") or "", "fail": err,
                    "dir": str(d), "files": files, "used": used or files})
    return out


def copy_ai_pics(word):
    """AI 做的画面：插图（svg）和画面设置拷到 画面\\<单词>\\。返回拷了几个图。"""
    f = V.folder_of(word)
    src = C.REPO / V.EXTRA / "art" / f
    d = pdir() / fname(word)
    d.mkdir(parents=True, exist_ok=True)
    for old in d.glob("*.svg"):
        old.unlink()
    n = 0
    if src.exists():
        for s in src.glob("*.svg"):
            shutil.copy2(str(s), str(d / s.name))
            n += 1
    j = C.REPO / V.EXTRA / "words" / (f + ".json")
    if j.exists():
        shutil.copy2(str(j), str(d / "画面设置.json"))
    return n


DRAW_SH = r"""W=~/wordfilm-work/wv-preview/@F@; rm -rf "$W"; mkdir -p "$W/art"
[ -d ~/kit ] || { echo "WVERR:WSL 里没有视频技能的 kit：先到「出视频」页点「把引擎同步进 WSL」"; exit 0; }
cd ~/kit
for s in @SCRIPTS@; do
  f=~/kit/${s}_art.py; [ -f "$f" ] || f=~/kit-extra/${s}_art.py
  if [ -f "$f" ]; then python3 "$f" "$W/art" >"$W/log.txt" 2>&1 || echo "WVERR:${s}_art.py 没画出来：$(tail -1 "$W/log.txt")"
  else echo "WVERR:找不到画图脚本 ${s}_art.py（先同步引擎）"; fi
done
O=@OUT@; mkdir -p "$O"; rm -f "$O"/*.svg; cp "$W/art/"*.svg "$O"/ 2>/dev/null
echo "WVN:$(ls "$O"/*.svg 2>/dev/null | wc -l)"
"""


def draw(word):
    """把这个词画面里的图存成文件：AI 做的直接拷；kit 里的在 WSL 里用视频技能画出来（几秒钟）。"""
    it = (p_items([word]) or [{}])[0]
    if not it.get("pic"):
        return {"ok": False, "msg": "%s 还没有画面：先做画面" % word}
    if it["src"] == "ai":
        n = copy_ai_pics(word)
        return {"ok": bool(n), "msg": "拷好了 %d 个图 → %s" % (n, it["dir"]) if n else "词库里没有这个词的插图"}
    if not it["scripts"]:
        return {"ok": False, "msg": "清单里没找到 %s 的画图脚本" % word}
    if not V.has_wsl():
        return {"ok": False, "msg": "kit 里的画面要在 WSL 里画：这台电脑没有 WSL"}
    sh = (DRAW_SH.replace("@F@", V.folder_of(word)).replace("@SCRIPTS@", " ".join(V.q(s) for s in it["scripts"]))
          .replace("@OUT@", V.q(V.to_wsl(Path(it["dir"])))))
    rc, t = V.wsl(sh, 300)
    errs = [l.split("WVERR:", 1)[1] for l in t.splitlines() if "WVERR:" in l]
    n = next((int(l.split("WVN:", 1)[1] or 0) for l in t.splitlines() if "WVN:" in l), 0)
    if n:
        return {"ok": True, "msg": "画好了 %d 个图 → %s%s" % (n, it["dir"], ("（有的没画出来：%s）" % "；".join(errs)[:200]) if errs else "")}
    return {"ok": False, "msg": "没画出来：%s" % ("；".join(errs) or " ".join(t.split())[-200:] or "WSL 没有回应")}


# ═══════════════════════ 打开文件夹、给界面读文件 ═══════════════════════
def open_path(what, word=""):
    p = {"qdir": qdir(), "pdir": pdir(), "root": out_root(), "qrepo": C.REPO / C.D / "词",
         "prepo": C.REPO / V.EXTRA, "pword": pdir() / fname(word), "qfile": qdir() / (fname(word) + ".xlsx"),
         "vbatch": out_root() / fname(word)}.get(what)
    if p is None:
        return {"ok": False, "msg": "不认识要打开什么"}
    if what in ("qdir", "pdir", "root", "pword", "vbatch"):
        p.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        return {"ok": False, "msg": "还没有：%s" % p}
    try:
        if sys.platform == "win32":
            os.startfile(str(p))
            return {"ok": True, "msg": "打开了 %s" % p}
        return {"ok": True, "msg": "在这台电脑上的位置：%s" % p}
    except Exception as e:
        return {"ok": False, "msg": "没打开（%s）：%s" % (str(e)[:80], p)}


def res_file(rel):
    """成果文件夹里的文件（给界面显示 svg）。只给成果文件夹里面的。"""
    root = out_root().resolve()
    p = (root / rel).resolve()
    if root not in p.parents or not p.is_file():
        return None, ""
    ct = {".svg": "image/svg+xml", ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
          ".json": "application/json; charset=utf-8"}.get(p.suffix.lower(), "application/octet-stream")
    return p.read_bytes(), ct


def dirs():
    return {"root": str(out_root()), "q": str(qdir()), "p": str(pdir()),
            "qrepo": str(C.REPO / C.D / "词"), "prepo": str(C.REPO / V.EXTRA)}
