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
    v = {"by_low": by_low, "by_word": by_word, "pw": V.pic_words(), "vd": V.videos(), "man": set(C.manual_words()),
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
          "picTodo": pic and w in X["unc"], "video": f in X["vd"] or f in X["done"], "inb": X["pend"].get(f, "")}
    d = X["dr"].get(f) or {}
    it["draft"] = d.get("ts", "") if d.get("rc") == 0 else ""
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


def info(words):
    X = _ctx()
    return [_one(w, X) for w in words]


FILTERS = {"all": lambda i: True, "ready": lambda i: i["st"] == "ready", "need": lambda i: i["st"] == "need",
           "noq": lambda i: not i["q"] or i["manual"], "nopic": lambda i: not i["pic"], "fix": lambda i: i["picTodo"],
           "video": lambda i: i["video"], "inb": lambda i: bool(i["inb"])}


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
    s = (qs.get("q") or "").strip().lower()
    f = qs.get("f") or "all"
    b = qs.get("b") or ""
    if qs.get("notpicked"):
        pk = set(picked())
        items = [i for i in items if i["word"] not in pk]
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
            "size": size, "counts": counts, "batches": batches, "picked": len(picked())}


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
    if o == "back":                                    # 送回素材那边补：加进「素材 → 选词」并选上
        import pool
        r = pool.add("\n".join(words), "出片送回来补", True)
        _LOCK_T["v"] = None
        return {"ok": r.get("ok"), "msg": "送回「素材 → 选词」并选上了 %d 个：到题目、画面那几步补齐，齐了再来挑" % len(words) if r.get("ok") else r.get("msg")}
    return {"ok": False, "msg": "不认识的操作"}
