# -*- coding: utf-8 -*-
"""单词工作台 · v1.39.0：界面分成「素材」「出片」两部分。
用户：“把整个界面分成两份：出片和素材两部分；素材平时积累，出片就直接从各个素材里面进行导入”。

素材（平时积累）：选词 → 总表 → 讲稿 → 题目 → 画面，做好的存进词库；「素材库」一张表看所有词的素材齐不齐。
出片（从素材里取）：挑词（只挑素材齐了的词，和素材那边的「选词」互不影响）→ 定稿 → 出视频。
这里管：素材库（每个词的素材情况）和出片挑的词（app/data/film_pick.json）。"""
import json
import re
import time

import core as C
import video as V

_F = lambda: C.DATA / "film_pick.json"
_LOCK_T = {"t": 0.0, "v": None}


def picked():
    try:
        d = json.loads(_F().read_text(encoding="utf-8"))
        return [w for w in d.get("words") or [] if isinstance(w, str)]
    except Exception:
        return []


def _save(words):
    seen, out = set(), []
    for w in words:
        if w not in seen:
            seen.add(w)
            out.append(w)
    _F().write_text(json.dumps({"words": out, "ts": C.now()}, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


BLKS = ("parts", "combo", "scene", "evolve", "example", "dist")      # v1.41.0：画面按块列


def _vnum(t):
    m = re.search(r"(\d+)\.(\d+)\.(\d+)", str(t or ""))
    return tuple(int(x) for x in m.groups()) if m else None


def _ctx():
    """算素材情况要用的几样，10 秒内用同一份（素材库有六七千个词）"""
    if _LOCK_T["v"] and time.time() - _LOCK_T["t"] < 10:
        return _LOCK_T["v"]
    import pool
    import pics
    by_low, by_word = pool._index()
    try:
        unc, todo = pics.unchecked_words(), pics.todo_all()
    except Exception:
        unc, todo = set(), {}
    try:
        dr = json.loads((C.DATA / "draft_results.json").read_text(encoding="utf-8"))
    except Exception:
        dr = {}
    try:
        pend, done = V.inbatch()
    except Exception:
        pend, done = {}, set()
    try:
        pf = {r["word"] for r in C.q("SELECT word FROM picfail")}
    except Exception:
        pf = set()
    try:
        sel = {r["word"] for r in C.q("SELECT word FROM pool WHERE picked=1")}
    except Exception:
        sel = set()
    try:
        sv = pics.skill_version()
    except Exception:
        sv = ("", "")
    try:
        C.load_table()
    except Exception:
        pass
    v = {"sv": sv, "cur": _vnum(sv[0]), "sel": sel, "by_low": by_low, "by_word": by_word, "pw": V.pic_words(), "vd": V.videos(), "man": set(C.manual_words()),
         "pf": pf, "unc": unc, "todo": todo, "dr": dr, "pend": pend, "done": done}
    _LOCK_T.update(t=time.time(), v=v)
    return v


def _one(w, X):
    rs = X["by_word"].get(w) or []
    f = V.folder_of(w)
    q = bool(rs) and all(r[4] != "缺" for r in rs)
    pic = f in X["pw"]
    it = {"word": w, "meaning": (rs[0][3] if rs and len(rs[0]) > 3 else "")[:40], "batch": rs[0][0] if rs else "",
          "inTable": bool(rs), "q": q, "manual": w in X["man"], "pic": pic, "picfail": w in X["pf"],
          "picTodo": pic and w in X["unc"], "sel": w in X["sel"], "video": f in X["vd"] or f in X["done"], "inb": X["pend"].get(f, "")}
    d = X["dr"].get(f) or {}
    it["draft"] = d.get("ts", "") if d.get("rc") == 0 else ""
    it["draftVer"] = d.get("ver", "") if it["draft"] else ""
    old = []
    if it["draftVer"] and X["cur"] and _vnum(it["draftVer"]) and _vnum(it["draftVer"]) < X["cur"]:
        old.append("讲稿")
    it["blk"] = _blocks(w, rs, X) if pic else {}
    for sid, b in it["blk"].items():
        if b.get("old"):
            old.append(b["name"])
    it["old"] = old
    miss = []
    if not rs:
        miss.append("总表里没有")
    if not q:
        miss.append("出题没过" if it["manual"] else "还没有题目")
    elif it["manual"]:
        miss.append("题目要改")
    if not pic:
        miss.append("画面上次没做成" if it["picfail"] else "还没有画面")
    elif it["picTodo"]:
        ln = X["todo"].get(w, "")
        n = len([x for x in re.split(r"[；;]", ln.split("：", 1)[-1]) if x.strip()]) if ln else 0
        miss.append(("画面还要补 %d 处" % n) if n else "画面还没过起草检查")
    it["miss"] = miss
    it["ready"] = not miss
    it["st"] = "video" if it["video"] else ("inb" if it["inb"] else ("ready" if it["ready"] else "need"))
    return it


def _blocks(w, rs, X):
    """有画面的词：画面里每一块的情况——ok 做好了 / fix 还要补 / none 还没有 / na 这个词不用；版本比现在的视频技能旧就标 old"""
    import sections as SEC
    _, P = SEC._prefs(w)
    if P is None:
        return {}
    rec = SEC._rec_of(w, [r for r in rs])
    todo = SEC._todo_of(rec)
    trow = ((C.TABLE.get("words") or {}).get(w) or [{}])[0]
    out = {}
    for sid in BLKS:
        sec = SEC.BY_ID[sid]
        issues = [t for t in todo if SEC._sec_of(t) == sid]
        st = "fix" if issues else ("ok" if SEC._has(SEC._slice(P, sec)) else "none")
        if st == "none" and sid in ("combo", "parts") and "+" not in (trow.get("拆分") or ""):
            st = "na"
        if st == "none" and sid == "dist" and not (trow.get("辨析") or "").strip():
            st = "na"                                 # 总表里没有同义词的词：不用辨析
        b = ((rec or {}).get("板块") or {}).get(sid) or {}
        ver = b.get("版本") or str((rec or {}).get("画面技能版本") or "")
        vn = _vnum(ver)
        out[sid] = {"name": sec["name"], "st": st, "ver": "%d.%d.%d" % vn if vn else "", "n": len(issues),
                    "old": bool(st in ("ok", "fix") and vn and X["cur"] and vn < X["cur"])}
    return out


def info(words):
    X = _ctx()
    return [_one(w, X) for w in words]


FILTERS = {"all": lambda i: True, "old": lambda i: bool(i["old"]), "ready": lambda i: i["st"] == "ready", "need": lambda i: i["st"] == "need",
           "noq": lambda i: not i["q"] or i["manual"], "nopic": lambda i: not i["pic"], "fix": lambda i: i["picTodo"],
           "video": lambda i: i["video"], "inb": lambda i: bool(i["inb"])}


def parse_words(text):
    """查看用：逗号、换行、空格都能隔开，按输入的顺序；词组（alarm clock）整个认，认不出的写出来"""
    import pool
    by_low, _ = pool._index()
    found, miss = [], []
    for cell in pool._SPLIT.split(text or ""):
        cell = cell.strip()
        if not cell:
            continue
        if cell.lower() in by_low:
            toks = [cell]
        else:
            toks = cell.split()
        i = 0
        while i < len(toks):
            hit = None
            for j in range(min(len(toks), i + 4), i, -1):          # 先试长的：词组
                k = " ".join(toks[i:j]).lower()
                if k in by_low:
                    hit = (by_low[k], j)
                    break
            if hit:
                if hit[0] not in found:
                    found.append(hit[0])
                i = hit[1]
            else:
                t = toks[i].strip("'\"“”‘’()（）[]【】<>《》*·•.-—")
                if re.search(r"[A-Za-z]", t) and t not in miss:
                    miss.append(t[:40])
                i += 1
    return found, miss


def lib(qs):
    """素材库：所有词（按总表顺序）。q 搜单词或意思，f 筛（见 FILTERS），b 总表批次，page / size 翻页；
    notpicked=1 不列已经挑进出片的（「挑词」页下面那张表用）。"""
    X = _ctx()
    words = list(X["by_word"].keys())
    items = [_one(w, X) for w in words]
    counts = {k: sum(1 for i in items if fn(i)) for k, fn in FILTERS.items()}
    batches = []
    for i in items:
        if i["batch"] and i["batch"] not in batches:
            batches.append(i["batch"])
    # v1.40.0：输入一个或几个单词查看——按输入的顺序列出来，总表里没有的写出来；只有一个词又没对上，就当成搜
    look, nf = [], []
    if (qs.get("words") or "").strip():
        import pool
        look, nf = parse_words(qs.get("words"))
        if not look and len(re.split(r"[\s,，;；、]+", qs["words"].strip())) == 1:
            qs = dict(qs, q=qs["words"].strip())
            nf = []
    s = (qs.get("q") or "").strip().lower()
    f = qs.get("f") or "all"
    b = qs.get("b") or ""
    if qs.get("notpicked"):
        pk = set(picked())
        items = [i for i in items if i["word"] not in pk]
    if look:
        by = {i["word"]: i for i in items}
        items = [by[w] for w in look if w in by]
    else:
        items = [i for i in items if FILTERS.get(f, FILTERS["all"])(i) and (not b or i["batch"] == b)
                 and (not s or s in i["word"].lower() or s in i["meaning"].lower())]
    try:
        size = max(5, min(200, int(qs.get("size") or 50)))
        page = max(1, int(qs.get("page") or 1))
    except Exception:
        size, page = 50, 1
    total = len(items)
    pages = max(1, (total + size - 1) // size)
    page = min(page, pages)
    return {"ok": True, "items": items[(page - 1) * size: page * size], "total": total, "page": page, "pages": pages,
            "size": size, "counts": counts, "batches": batches, "picked": len(picked()), "look": bool(look), "notFound": nf,
            "skill": X["sv"][0], "skillEd": X["sv"][1]}


def pick_info_items():
    """出片挑的词，带素材情况（出视频、定稿用）"""
    return info(picked())


def op(b):
    o = b.get("op")
    words = [w for w in (b.get("words") or []) if isinstance(w, str) and w.strip()]
    cur = picked()
    if o == "add":
        X = _ctx()
        if b.get("text"):                              # 粘贴一串单词
            import pool
            found, miss = pool.parse(b.get("text") or "")
            words += found
        else:
            miss = []
        its = [_one(w, X) for w in words if w in X["by_word"]]
        ok = [i["word"] for i in its if i["ready"] or b.get("force")]
        no = [i for i in its if not (i["ready"] or b.get("force"))]
        new = [w for w in ok if w not in cur]
        _save(cur + new)
        msg = "挑进来 %d 个" % len(new) + ("（%d 个本来就在）" % (len(ok) - len(new)) if len(ok) > len(new) else "")
        if no:
            msg += "；素材还没齐、没挑进来的 %d 个：%s" % (len(no), "、".join("%s（%s）" % (i["word"], "、".join(i["miss"])) for i in no[:8])
                                                    + ("…" if len(no) > 8 else ""))
        if miss:
            msg += "；总表里没有的 %d 个：%s" % (len(miss), "、".join(miss[:8]))
        return {"ok": True, "msg": msg, "notReady": [i["word"] for i in no]}
    if o == "remove":
        _save([w for w in cur if w not in set(words)])
        return {"ok": True, "msg": "不挑了 %d 个（素材都还在）" % len(words)}
    if o == "clear":
        _save([])
        return {"ok": True, "msg": "清空了出片挑的词（%d 个，素材都还在）" % len(cur)}
    if o in ("sel", "make"):                          # v1.40.0：总表里选上做素材（make：点了缺的那一格，选上再去那一步做）
        import pool
        r = pool.add("\n".join(words), "总表里选的", True)
        _LOCK_T["v"] = None
        if not r.get("ok"):
            return r
        return {"ok": True, "msg": ("%d 个加进了这次要做的词，在讲稿、题目、画面几步里做" % len(words)) if o == "sel" else ("%s 加进了这次要做的词，去做" % "、".join(words))}
    if o == "unsel":
        import pool
        pool.pick(words, False)
        _LOCK_T["v"] = None
        return {"ok": True, "msg": "不选了 %d 个（做好的素材都还在）" % len(words)}
    if o == "back":                                    # 送回素材那边补：在总表里选上
        import pool
        r = pool.add("\n".join(words), "出片送回来补", True)
        _LOCK_T["v"] = None
        return {"ok": r.get("ok"), "msg": "送回素材那边、加进这次要做的词 %d 个：到题目、画面那几步补齐，齐了再来挑" % len(words) if r.get("ok") else r.get("msg")}
    return {"ok": False, "msg": "不认识的操作"}
