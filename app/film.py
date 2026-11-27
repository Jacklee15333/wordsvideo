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
    for sid in ("pron", "kaodian", "board"):           # 不在画面那几列里、可也要在画面设置里补的（比如读音拆分的音标 sylIpa）
        n = len([t for t in todo if SEC._sec_of(t) == sid])
        if n:
            out[sid] = {"name": SEC.BY_ID[sid]["name"], "st": "fix", "ver": "", "n": n, "old": False, "extra": True}
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


# ═══════════ v1.42.0：按现在的视频技能更新——① 本地（不用 AI）重写讲稿、逐块检查，对得上的块直接记成新版本；② 没过的块交给 AI 只补那几块 ═══════════
_UPLOG = lambda: C.DATA / "upgrade_log.json"


def _say_flat(plan):
    """配音稿 → {块名: [“卡 1：……”, …]}"""
    import sections as SEC
    out = {}
    for sid in ("pron", "parts", "combo", "scene", "evolve", "example", "dist", "kaodian", "board"):
        ls = []
        for g in SEC.plan_lines(sid, plan):
            ls.append(("%s：" % g["label"] if g["label"] else "") + " ".join(g["say"]))
        if ls:
            out[SEC.BY_ID[sid]["name"]] = ls
    return out


def _draft_diff(old, new):
    """讲稿哪几块改了：[{name, old:[…], new:[…]}]；原来没有讲稿就是 None"""
    if not old:
        return None
    a, b = _say_flat(old), _say_flat(new or {})
    out = []
    for name in list(dict.fromkeys(list(a) + list(b))):
        if a.get(name) != b.get(name):
            oa, nb = a.get(name) or [], b.get(name) or []
            out.append({"name": name, "old": [x for x in oa if x not in nb][:6], "new": [x for x in nb if x not in oa][:6]})
    return out


def uplog(words):
    try:
        d = json.loads(_UPLOG().read_text(encoding="utf-8"))
    except Exception:
        d = {}
    return {w: d.get(w) for w in words if d.get(w)}


def _uplog_put(w, v):
    try:
        d = json.loads(_UPLOG().read_text(encoding="utf-8"))
    except Exception:
        d = {}
    d[w] = v
    _UPLOG().write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def skill_changes(old_vers):
    """视频技能从这几个旧版本到现在，中间每一版改了什么（读 SKILL.md 的“这一版改了什么”）"""
    import pics
    try:
        t = pics._p(pics.SKILL).read_text(encoding="utf-8")
    except Exception:
        return []
    lo = min([v for v in (_vnum(x) for x in old_vers) if v] or [None]) if old_vers else None
    out = []
    for m in re.finditer(r"(?m)^## 这一版改了什么（(\d+\.\d+\.\d+)，(第[^：）]+版)[：:]?([^）]*)）\n(.*?)(?=^## |\Z)", t, re.S):
        v = _vnum(m.group(1))
        if lo and v and v > lo:
            pts = [re.sub(r"`", "", x.strip()[2:]) for x in m.group(4).splitlines() if x.strip().startswith("- ")]
            out.append({"ver": m.group(1), "ed": m.group(2), "title": m.group(3).strip(), "points": [p[:160] for p in pts if "打包存档" not in p][:5]})
    return out


def stamp(w, line, ver, old_plan=None, new_plan=None):
    """第 ① 步每写好一个词调一次：line 是这次起草检查的“还要补：…”，ver 是这次用的视频技能版本；
    v1.46.0：同时记下这个词改了什么（每一块从哪一版到哪一版、检查过了还是要补；讲稿哪几句变了），弹框里给你看"""
    import sections as SEC
    import pics
    if not ver:
        return
    diff = _draft_diff(old_plan, new_plan)
    _, P = SEC._prefs(w)
    log = {"ts": C.now(), "ver": ver, "blocks": [], "draft": diff, "pic": P is not None}
    if P is None:                                      # 视频技能自带的画面、还没画面：只记讲稿
        _uplog_put(w, log)
        return
    import drafts as DR
    todo = [t for t in DR._todo(line)]                 # [{sec, name, text}]（练习题已经去掉）
    bad = {t["sec"] for t in todo}
    p = pics._rec_path(w)
    with C.REPO_LOCK:
        try:
            rec = json.loads(p.read_text(encoding="utf-8")) if p.exists() else None
        except Exception:
            rec = None
        if rec is None:
            return
        bk = rec.setdefault("板块", {})
        now = C.now()
        for sid in BLKS:                               # 记下每一块：原来是哪一版、这次怎样
            sec = SEC.BY_ID[sid]
            has = SEC._has(SEC._slice(P, sec))
            was = _vnum((bk.get(sid) or {}).get("版本") or rec.get("画面技能版本"))
            its = [t["text"] for t in todo if t["sec"] == sid]
            if has or its:
                log["blocks"].append({"sid": sid, "name": sec["name"], "from": "%d.%d.%d" % was if was else "",
                                      "st": "fix" if its else "ok", "issues": its[:4]})
        for t in todo:
            if t["sec"] not in BLKS:
                log["blocks"].append({"sid": t["sec"], "name": t["name"] or "其他", "from": "", "st": "fix", "issues": [t["text"]]})
        for sid in BLKS:
            sec = SEC.BY_ID[sid]
            if sid not in bad and SEC._has(SEC._slice(P, sec)):
                b = bk.setdefault(sid, {})
                b.update({"时间": b.get("时间") or str(rec.get("画面生成") or "")[:16], "版本": "视频技能 %s" % ver,
                          "检查": "%s 用视频技能 %s 本地检查过了" % (now[:16], ver)})
        if not todo:
            rec["检查"] = "还要补：都齐了（%s 用视频技能 %s 本地检查）" % (now[:16], ver)
            rec["画面技能版本"] = "视频技能 %s" % ver
        p.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    _uplog_put(w, log)
    if todo:                                           # 没过的块：记下还要补什么（画面页、补画面的提示词都看它），先不交给 AI
        pics.send_back({w: [("【%s】" % t["name"] if t["name"] else "") + t["text"] for t in todo]}, src="视频技能 %s 本地检查" % ver)
    else:
        pics._UC["t"] = 0.0
        try:
            C.commit_pending("词库：%s 按视频技能 %s 本地检查过了，画面不用重做" % (w, ver))
        except Exception:
            pass
    _LOCK_T["v"] = None


def upgrade_ai(words):
    """第 ② 步：第 ① 步查出来要补的块，退回给 AI，只收这几块"""
    import sections as SEC
    import pics
    X = _ctx()
    rs_all = X["by_word"]
    out = {}
    for w in words:
        rec = SEC._rec_of(w, rs_all.get(w) or [])
        sids = {SEC._sec_of(t) for t in SEC._todo_of(rec)} & SEC.AI_EDIT
        if sids:
            out[w] = sorted(sids)
    for w, sids in out.items():
        for sid in sids:
            SEC.pend_add([w], sid)
    pics._UC["t"] = 0.0
    _LOCK_T["v"] = None
    n = sum(len(v) for v in out.values())
    return {"ok": bool(out), "words": list(out), "n": n,
            "msg": ("%d 个词、%d 块交给 AI 补，AI 只改这几块" % (len(out), n)) if out else "没有要 AI 补的块"}
