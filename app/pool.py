# -*- coding: utf-8 -*-
"""单词工作台 · 备选单词。

先把这一阵要做的词导进来存着（粘贴，或者从 Excel、txt、csv 里读），再挑着做；
每个词做到哪一步（题目、画面、视频、正在做、没做成）都是现查的，所以不会忘了哪些还没处理。
只存在本机 data/app.db 里，不上传。总表里没有的词不存（做不了），导入时会列出来。
"""
import base64, io, json, re, time

import core as C
import video as V

_SPLIT = re.compile(r"[\n\r,，、;；\t|]+")
_EN_RUN = re.compile(r"^([A-Za-z][A-Za-z'’\-]*(?:\s+[A-Za-z][A-Za-z'’\-]*)*)")


_READY = []


def _db():
    if _READY:
        return
    C.x("CREATE TABLE IF NOT EXISTS pool(word TEXT PRIMARY KEY, tag TEXT DEFAULT '', ts TEXT, ord INTEGER, picked INTEGER DEFAULT 0)")
    if "picked" not in {r["name"] for r in C.q("PRAGMA table_info(pool)")}:     # v1.9.5 建的表没有这一列
        C.x("ALTER TABLE pool ADD COLUMN picked INTEGER DEFAULT 0")
    _READY.append(1)


def _index():
    """总表（索引）里的词：{小写: 总表里的写法}，和每个词的行。"""
    _, rows = C.read_index()
    by_low, by_word = {}, {}
    for r in rows:
        by_low.setdefault(r[2].lower(), r[2])
        by_word.setdefault(r[2], []).append(r)
    return by_low, by_word


def _resolve(cell, by_low):
    """一格（或一行）里的字 → 总表里的词；认不出返回 None。
    “protect” “Protect” 直接认；“protect v. 保护”“look after 照顾”取前面的英文（先试整段，再一个词一个词往短里试）；
    “Unit 5”这种后面跟数字的不认（多半是标题）。"""
    s = re.sub(r"\s+", " ", (cell or "").strip().strip("'\"“”‘’()（）[]【】<>《》*·•-—").strip())
    if not s:
        return None
    if s.lower() in by_low:
        return by_low[s.lower()]
    m = _EN_RUN.match(s)
    if not m or re.search(r"\d", s[m.end():]):
        return None
    parts = m.group(1).split()
    for n in range(len(parts), 0, -1):
        k = " ".join(parts[:n]).lower()
        if k in by_low:
            return by_low[k]
    return None


def parse(text):
    """一段文字 → (总表里有的词（按出现顺序、不重复）, 认不出的那几段)。"""
    by_low, _ = _index()
    found, miss = [], []
    for cell in _SPLIT.split(text or ""):
        if not cell.strip():
            continue
        w = _resolve(cell, by_low)
        if w:
            if w not in found:
                found.append(w)
        elif re.search(r"[A-Za-z]", cell) and cell.strip() not in miss:
            miss.append(cell.strip()[:40])
    return found, miss


def file_text(name, b64):
    """导入的文件 → 一段文字（Excel 每一格一行；txt、csv 原样）。"""
    data = base64.b64decode(b64 or "")
    if len(data) > 20 * 1024 * 1024:
        raise C.Fatal("文件太大了（超过 20 MB）")
    if (name or "").lower().endswith((".xlsx", ".xlsm")):
        import openpyxl
        wb = openpyxl.load_workbook(io.BytesIO(data), read_only=True, data_only=True)
        out, n = [], 0
        for ws in wb.worksheets:
            for row in ws.iter_rows(values_only=True):
                for v in row:
                    if v is None:
                        continue
                    out.append(str(v))
                    n += 1
                    if n >= 50000:
                        break
        return "\n".join(out)
    if (name or "").lower().endswith(".xls"):
        raise C.Fatal("老的 .xls 读不了：在 Excel 里另存为 .xlsx 再导入")
    for enc in ("utf-8-sig", "gbk", "utf-16"):
        try:
            return data.decode(enc)
        except Exception:
            continue
    return data.decode("utf-8", "replace")


def extract(name, b64):
    """从文件里读出总表里有的词，放进导入框给你看一眼再加。"""
    try:
        found, miss = parse(file_text(name, b64))
    except C.Fatal as e:
        return {"ok": False, "msg": str(e)}
    except Exception as e:
        return {"ok": False, "msg": "文件读不出来（%s）：Excel 要是 .xlsx，文字要是 txt / csv" % str(e)[:80]}
    msg = "从「%s」里认出 %d 个总表里有的词" % (name, len(found))
    if miss:
        msg += "；认不出的 %d 段没放进来（比如：%s）" % (len(miss), "、".join(miss[:6]))
    return {"ok": bool(found), "msg": msg if found else "「%s」里没认出总表里有的词" % name, "text": "\n".join(found)}


def status(words):
    """每个词现在的情况：题目（有/没过/没有）、画面（有/没做成/没有）、视频、在不在备选单词里、选上没有。"""
    _db()
    _, by_word = _index()
    pw, vd = V.pic_words(), V.videos()
    man = set(C.manual_words())
    pf = {r["word"] for r in C.q("SELECT word FROM picfail")}
    have = {r["word"]: r for r in C.q("SELECT word, picked FROM pool")}
    out = []
    for w in words:
        rs = by_word.get(w) or []
        f = V.folder_of(w)
        out.append({"word": w, "meaning": rs[0][3] if rs and len(rs[0]) > 3 else "", "q": bool(rs) and all(x[4] != "缺" for x in rs),
                    "manual": w in man, "pic": f in pw, "picfail": w in pf, "video": f in vd,
                    "inPool": w in have, "picked": bool((have.get(w) or {}).get("picked"))})
    return out


def check(text):
    """导入、自己输入的词：先检测（总表里有没有、有没有题目、有没有画面），再决定加哪些。"""
    found, miss = parse(text)
    return {"ok": bool(found), "items": status(found), "miss": miss,
            "msg": "" if found else "没认出总表里有的词" + ("（认不出：%s）" % "、".join(miss[:8]) if miss else "：先粘贴单词或者选文件")}


def add(text, tag="", pick=False):
    _db()
    found, miss = parse(text)
    if not found:
        return {"ok": False, "msg": "没认出总表里有的词" + ("（认不出：%s）" % "、".join(miss[:8]) if miss else "：先粘贴单词或者选文件")}
    have = {r["word"] for r in C.q("SELECT word FROM pool")}
    new = [w for w in found if w not in have]
    top = (C.q("SELECT MAX(ord) AS m FROM pool", one=True) or {}).get("m") or 0
    tag = (tag or "").strip()[:30]
    for i, w in enumerate(new):
        C.x("INSERT OR IGNORE INTO pool(word, tag, ts, ord) VALUES(?,?,?,?)", (w, tag, C.now(), top + i + 1))
    old = [w for w in found if w in have]
    if pick:                                          # 从总表里找来的：加进来就选上
        for w in found:
            C.x("UPDATE pool SET picked=1 WHERE word=?", (w,))
    if tag and old:                                   # 已经有的词也记上这一批的名字
        for w in old:
            C.x("UPDATE pool SET tag=? WHERE word=? AND (tag IS NULL OR tag='')", (tag, w))
    msg = "加了 %d 个" % len(new) + ("，都选上了" if pick else "")
    if old:
        msg += "；%d 个本来就在" % len(old)
    if miss:
        msg += "；总表里没有、没加的 %d 个：%s" % (len(miss), "、".join(miss[:10]) + ("…" if len(miss) > 10 else ""))
    C.log("备选单词：%s" % msg)
    return {"ok": True, "msg": msg, "added": new, "have": old, "miss": miss}


def pick(words, on=True):
    """选上（或者不选）：出题、画面两步给“选上的词”做。"""
    _db()
    words = [w for w in (words or []) if w]
    for w in words:
        C.x("UPDATE pool SET picked=? WHERE word=?", (1 if on else 0, w))
    return {"ok": True, "msg": ("选上了 %d 个" if on else "不选了 %d 个") % len(words)}


def remove(words):
    _db()
    words = [w for w in (words or []) if w]
    for w in words:
        C.x("DELETE FROM pool WHERE word=?", (w,))
    return {"ok": True, "msg": "从备选单词里删掉了 %d 个（只是不在这里列着了，做好的题目和画面都还在）" % len(words)}


def _busy_words():
    """排着队、正在做的任务里点了名的词。暂停着的不算（v1.10.9）：打开软件时上次没做完的会暂停，
    这些词照样能重新开始；重新开始时同一步暂停着的旧任务会自动取消。"""
    out = set()
    for t in C.q("SELECT params FROM tasks WHERE status IN ('运行中','排队')"):
        try:
            out.update(json.loads(t["params"] or "{}").get("words") or [])
        except Exception:
            pass
    return out


ST_NAME = {"todo": "还没做", "needpic": "缺画面", "fail": "没做成", "doing": "正在做", "done": "做好了"}
GROUPS = {"todo": ("todo", "needpic", "fail"), "doing": ("doing",), "done": ("done",)}


def items():
    _db()
    rows = C.q("SELECT word, tag, ts, ord, picked FROM pool ORDER BY ord")
    if not rows:
        return {"items": [], "counts": {"todo": 0, "doing": 0, "done": 0, "all": 0, "picked": 0}, "tags": []}
    by_low, by_word = _index()
    pw, vd = V.pic_words(), V.videos()
    man = set(C.manual_words())
    pf = {r["word"] for r in C.q("SELECT word FROM picfail")}
    busy = _busy_words()
    out = []
    for r in rows:
        w = r["word"]
        rs = by_word.get(w) or []
        f = V.folder_of(w)
        has_q = bool(rs) and all(x[4] != "缺" for x in rs)
        it = {"word": w, "tag": r["tag"] or "", "ts": (r["ts"] or "")[:10], "picked": bool(r["picked"]), "meaning": (rs[0][3] if rs and len(rs[0]) > 3 else ""),
              "q": has_q, "manual": w in man, "pic": f in pw, "video": f in vd, "picfail": w in pf, "inTable": bool(rs)}
        if w in busy:
            st = "doing"
        elif has_q and it["pic"]:
            st = "done"
        elif w in man or w in pf:
            st = "fail"
        elif has_q:
            st = "needpic"
        else:
            st = "todo"
        it["st"], it["stName"] = st, ST_NAME[st]
        out.append(it)
    counts = {g: sum(1 for i in out if i["st"] in sts) for g, sts in GROUPS.items()}
    counts["all"] = len(out)
    counts["picked"] = sum(1 for i in out if i["picked"])
    tags = sorted({i["tag"] for i in out if i["tag"]})
    return {"items": out, "counts": counts, "tags": tags}


def summary():
    """开始页那一行用：存着几个、几个没做完。"""
    try:
        d = items()
        return {"all": d["counts"]["all"], "todo": d["counts"]["todo"], "picked": d["counts"]["picked"]}
    except Exception:
        return {"all": 0, "todo": 0}


def op(b):
    o = b.get("op")
    if o == "add":
        return add(b.get("text") or "", b.get("tag") or "", pick=bool(b.get("pick")))
    if o == "check":
        return check(b.get("text") or "")
    if o == "pick":
        return pick(b.get("words") or [], on=b.get("on", True) is not False)
    if o == "extract":
        return extract(b.get("name") or "", b.get("b64") or "")
    if o == "remove":
        return remove(b.get("words") or [])
    if o == "clearDone":
        done = [i["word"] for i in items()["items"] if i["st"] == "done"]
        r = remove(done)
        r["msg"] = "清掉了 %d 个做好了的（题目和画面都还在）" % len(done)
        return r
    return {"ok": False, "msg": "不认识的操作"}
