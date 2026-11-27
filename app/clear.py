# -*- coding: utf-8 -*-
"""单词工作台 · v1.27.0：清除做好的题目、画面、视频。
用户：“生成好的题目，画面，视频部分要有清除按钮，因为有时候改版了，那么这些旧版的就不能再有了，继续放在这里会污染新的版本”。

- 题目：只清单词工作台 AI 出的（词库记录里有「题目生成」的）；原来题库里就有的（从老仓库搬来的六千多个词）不动。清掉＝词库里这个词的「题目」「题目原稿」…删掉、索引改回“缺”、
  成果文件夹里的 题目\\<词>.xlsx 删掉。这个词回到「出题」要做的列表。
- 画面：只清「词库/画面设置」里 AI 做的（清单.tsv 里的）；视频技能自带的 kit 不动。清掉＝words/<词>.json/.py、<词>ai_art.py、art/<词>/、
  清单那一行、词库记录里的「画面」「插图」，WSL 里同步过去的那一份也删。这个词回到「画面」要做的列表。
- 视频：出片文件夹里的视频和关键画面图、视频清单的登记、WSL 里的成片（和「删掉旧版」一样，只是不管新旧）。
词库的改动照常提交、上传 GitHub（以前的在 GitHub 历史里还找得到）；视频删了找不回来。"""
import json
import shutil
import threading
from pathlib import Path

import core as C
import video as V

NAMES = {"q": "题目", "p": "画面", "v": "视频"}


def _rec(rel):
    p = C.REPO / C.D / rel
    try:
        return p, json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return p, None


def _q_words():
    _, rows = C.read_index()
    out = {}
    for r in rows:
        if len(r) > 4 and r[4] == "细节数据有":
            out.setdefault(r[2], r[6] if len(r) > 6 else "")
    return out


def _p_rows():
    lst = C.REPO / V.EXTRA / "清单.tsv"
    out = []
    if lst.exists():
        for l in lst.read_text(encoding="utf-8").splitlines():
            f = l.split("\t")
            if l.startswith("#") or len(f) < 2 or not f[1].strip():
                continue
            out.append((f[1].strip(), [a for a in (f[2].split(",") if len(f) > 2 else []) if a.strip()], f[3].strip() if len(f) > 3 else ""))
    return out


def listing(what):
    try:
        if what == "q":
            items = []
            for w, rel in sorted(_q_words().items(), key=lambda x: x[0].lower()):
                rec = _rec(rel)[1] if rel else None
                if not (rec or {}).get("题目生成"):
                    continue                     # 题库里原来就有的（从老仓库搬来的那六千多个词）不列：只列单词工作台 AI 出的
                items.append({"word": w, "info": str(rec.get("题目生成") or "")[:40]})
            return {"ok": True, "items": items}
        if what == "p":
            return {"ok": True, "items": [{"word": f, "info": info[:40]} for f, _, info in sorted(_p_rows(), key=lambda x: x[0].lower())]}
        if what == "v":
            return {"ok": True, "items": [{"word": k, "info": "%s · %s%s" % (v.get("batch", ""), v.get("ts", ""), " · 旧版" if v.get("old") else "")}
                                          for k, v in sorted(V.videos().items(), key=lambda x: x[0].lower())]}
    except Exception as e:
        return {"ok": False, "msg": "没读到（%s）" % str(e)[:120]}
    return {"ok": False, "msg": "不认识要清什么"}


def _clear_q(words):
    done = []
    with C.REPO_LOCK:
        head, rows = C.read_index()
        have = {}
        for r in rows:
            if len(r) > 4 and r[4] == "细节数据有" and r[2] in words:
                have.setdefault(r[2], r[6] if len(r) > 6 else "")
        for w, rel in list(have.items()):
            p, rec = _rec(rel) if rel else (None, None)
            if not (rec or {}).get("题目生成"):          # 原来题库里的不清（只清单词工作台 AI 出的）
                have.pop(w)
                continue
            if rel:
                if rec is not None:
                    for k in ("题目原稿", "题目生成", "题目检查"):
                        rec.pop(k, None)
                    rec["题目"] = None
                    p.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
            done.append(w)
        for r in rows:
            if r[2] in done and len(r) > 4 and r[4] == "细节数据有":
                r[4] = "缺"
        C.write_index(head, rows)
    try:
        import results as RS
        qd = Path(RS.qdir())
        for w in done:
            (qd / (w + ".xlsx")).unlink(missing_ok=True)
    except Exception:
        pass
    return done


def _clear_p(words):
    base = C.REPO / V.EXTRA
    done, sh = [], []
    with C.REPO_LOCK:
        lst = base / "清单.tsv"
        lines = lst.read_text(encoding="utf-8").splitlines() if lst.exists() else []
        keep = []
        for l in lines:
            f = l.split("\t")
            fo = f[1].strip() if len(f) >= 2 else ""
            if l.startswith("#") or not fo or fo not in words:
                keep.append(l)
                continue
            arts = [a.strip() for a in (f[2].split(",") if len(f) > 2 else []) if a.strip()]
            for p in [base / "words" / (fo + ".json"), base / "words" / (fo + ".py")] + [base / (a + "_art.py") for a in arts]:
                p.unlink(missing_ok=True)
            shutil.rmtree(base / "art" / fo, ignore_errors=True)
            done.append(fo)
            sh.append("rm -f -- ~/kit-extra/words/%s ~/kit-extra/words/%s %s; rm -rf -- ~/kit-extra/art/%s" % (
                V.q(fo + ".json"), V.q(fo + ".py"), " ".join("~/kit-extra/" + V.q(a + "_art.py") for a in arts), V.q(fo)))
        if lst.exists():
            lst.write_text("\n".join(keep) + "\n", encoding="utf-8")
        head, rows = C.read_index()
        for r in rows:
            if V.folder_of(r[2]) in done and len(r) > 5:
                r[5] = "缺"
                rel = r[6] if len(r) > 6 else ""
                if rel:
                    p, rec = _rec(rel)
                    if rec is not None:
                        for k in ("画面生成", "检查"):
                            rec.pop(k, None)
                        rec["画面"], rec["插图"] = None, []
                        p.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        C.write_index(head, rows)
    for w in done:
        try:
            C.x("DELETE FROM picfail WHERE word=?", (w,))
        except Exception:
            pass
    try:
        import pics
        pics._UC["t"] = 0.0
    except Exception:
        pass
    if sh:
        threading.Thread(target=V._try_wsl, args=("; ".join(sh),), daemon=True).start()
    return done


def clear(what, words):
    words = [w for w in (words or []) if isinstance(w, str) and w.strip()]
    if what not in NAMES:
        return {"ok": False, "msg": "不认识要清什么"}
    if not words:
        return {"ok": False, "msg": "一个都没选"}
    if what == "v":
        r = V.delete_old(words, only_old=False)
        return r
    done = _clear_q(set(words)) if what == "q" else _clear_p(set(words))
    if not done:
        return {"ok": False, "msg": "选的词没有能清的%s" % NAMES[what]}
    C.log("清除了 %d 个词做好的%s（%s）：这些词回到「%s」要做的列表" % (len(done), NAMES[what], "、".join(done[:6]) + (" 等" if len(done) > 6 else ""),
                                                          "出题" if what == "q" else "画面"))
    threading.Thread(target=lambda: C.commit_pending("词库：清除做好的%s（%d 个词，单词工作台）" % (NAMES[what], len(done))), daemon=True).start()
    return {"ok": True, "n": len(done), "msg": "清除了 %d 个词做好的%s：这些词回到「%s」要做的列表，按新版重做" % (len(done), NAMES[what], "出题" if what == "q" else "画面")}


# ═══════════════════════ v1.28.0：「做好的」标签（出题、画面、出视频三步各一个） ═══════════════════════
# 用户：“这几个部分都要有一个标签：做好的……可以单个点击重做，也可以批量点击重做，也可以点击删除单个，也可以点击清空，批量删除……
#   每个单词列表里面要列举这个单词的题目，画面是什么时候生成的，用的是哪个版本的技能”
def _index_maps():
    _, rows = C.read_index()
    meaning, rel, word_of = {}, {}, {}
    for r in rows:
        w = r[2]
        meaning.setdefault(w, r[3] if len(r) > 3 else "")
        if len(r) > 6 and r[6]:
            rel.setdefault(w, r[6])
        word_of.setdefault(V.folder_of(w), w)
    return meaning, rel, word_of


def done_list(what):
    try:
        if what == "q":
            meaning, _, _ = _index_maps()
            items = []
            for w, rl in _q_words().items():
                rec = _rec(rl)[1] if rl else None
                if not (rec or {}).get("题目生成"):
                    continue
                items.append({"word": w, "meaning": meaning.get(w, ""), "ts": str(rec.get("题目生成") or ""), "ver": str(rec.get("题目版本") or ""),
                              "note": str(rec.get("题目检查") or "")[:40]})
            items.sort(key=lambda x: x["ts"], reverse=True)
            return {"ok": True, "items": items}
        if what == "p":
            meaning, rel, word_of = _index_maps()
            items = []
            for f, _, info in _p_rows():
                w = word_of.get(f, f)
                rec = _rec(rel[w])[1] if rel.get(w) else None
                rec = rec or {}
                items.append({"word": f, "show": w, "meaning": meaning.get(w, ""), "ts": str(rec.get("画面生成") or info or ""),
                              "ver": str(rec.get("画面技能版本") or ""), "note": str(rec.get("检查") or "")[:40]})
            items.sort(key=lambda x: x["ts"], reverse=True)
            return {"ok": True, "items": items}
        if what == "v":
            return {"ok": True, "items": [{"word": k, "ts": v.get("ts", ""), "ver": ("视频技能 " + v["ver"]) if v.get("ver") else "", "batch": v.get("batch", ""),
                                           "file": v.get("file", ""), "old": bool(v.get("old"))} for k, v in V.videos().items()]}
    except Exception as e:
        return {"ok": False, "msg": "没读到（%s）" % str(e)[:120]}
    return {"ok": False, "msg": "不认识要列什么"}


def done_op(op, what, words, find="", picked=False):
    if op == "clearall":                                 # v1.31.0：清空（按现在的搜索、筛选，服务器上算出是哪些词）
        words, op = done_all_words(what, find, picked), "delete"
    words = [w for w in (words or []) if isinstance(w, str) and w.strip()]
    if op not in ("redo", "delete"):
        return {"ok": False, "msg": "不认识要做什么"}
    r = clear(what, words)
    if op == "redo" and r.get("ok"):
        import pool
        pool._db()
        inpool = [x["word"] for x in C.q("SELECT word FROM pool")]
        want = set(words) | {V.folder_of(w) for w in words}
        real = [w for w in inpool if w in want or V.folder_of(w) in want]
        if real:
            pool.pick(real, True)
        page = {"q": "出题", "p": "画面", "v": "出视频"}[what]
        r["msg"] = "重做 %d 个：现在的%s删掉了，这些词回到「%s」要做的列表（选上了），按新的技能做" % (r.get("n", len(real)), NAMES[what], page)
    return r



# ═══════════════ v1.31.0：「做好的」列表——单词、内容（能改）、时间、版本、备注、操作；分页、搜索 ═══════════════
# 用户：“我希望每个列表都要有具体的内容……单词：显示单词和含义；题目内容……还可以进行修改；做好的时间，用的版本，备注这些放后面去……所有做好的界面都要这样”
def _q_lines(qs):
    out = []
    for i, q in enumerate(qs or []):
        if not isinstance(q, dict):
            continue
        stem = str(q.get("stem") or q.get("zh") or "").replace("\n", " / ")
        lis = str(q.get("listen") or "")
        opts = q.get("opts") or []
        ans = q.get("answer") or q.get("ans") or ""
        t = "%d. %s%s%s%s" % (i + 1, ("（%s）" % q["type"]) if q.get("type") else "", ("听：" + lis + "　") if lis else "", stem,
                              ("　" + "　".join("%s. %s" % ("ABCD"[j] if j < 4 else j + 1, o) for j, o in enumerate(opts))) if opts else "")
        if ans:
            t += "　答案：%s" % ans
        out.append(t)
    return out


def done_page(what, find="", page=1, size=50, picked=False):
    r = done_list(what)
    if not r.get("ok"):
        return r
    items = r["items"]
    if picked:
        try:
            import pool
            pool._db()
            ps = {x["word"] for x in C.q("SELECT word FROM pool WHERE picked=1")}
            items = [x for x in items if x.get("show", x["word"]) in ps or x["word"] in ps or V.folder_of(x.get("show", x["word"])) in {V.folder_of(p) for p in ps}]
        except Exception:
            pass
    f = (find or "").strip().lower()
    if f:
        items = [x for x in items if f in (str(x.get("show") or x["word"]) + " " + str(x.get("meaning") or "")).lower()]
    total = len(items)
    size = max(10, min(200, int(size or 50)))
    pages = max(1, (total + size - 1) // size)
    page = max(1, min(pages, int(page or 1)))
    cut = items[(page - 1) * size: page * size]
    meaning, rel, _ = _index_maps()
    if what == "q":
        for x in cut:
            rec = _rec(rel[x["word"]])[1] if rel.get(x["word"]) else None
            qs = (rec or {}).get("题目原稿") or []
            x["lines"] = _q_lines(qs)
            try:
                x["draft"] = "\n".join(C.to_compact(qs) or [])
            except Exception:
                x["draft"] = ""
    elif what == "p":
        import sections as SEC
        for x in cut:
            w = x.get("show") or x["word"]
            _, P = SEC._prefs(w)
            rec = _rec(rel[w])[1] if rel.get(w) else None
            todo = SEC._todo_of(rec)
            line = []
            for s in SEC.SECTIONS:
                if s["id"] not in ("parts", "combo", "scene", "evolve", "example", "dist"):
                    continue
                part = SEC._slice(P, s) if P else {}
                iss = [t for t in todo if SEC._sec_of(t) == s["id"]]
                line.append("%s %s" % (s["name"], "⚠" if iss else ("✓" if SEC._has(part) else "—")))
            x["lines"] = ["　".join(line)] + (["要补：" + "；".join(todo)[:300]] if todo else [])
    elif what == "v":
        for x in cut:
            x["meaning"] = meaning.get(x["word"].replace("_", " "), "") or meaning.get(x["word"], "")
            x["lines"] = ["批次 %s · %s" % (x.get("batch", ""), str(x.get("file", "")).replace("\\", "/").split("/")[-1])]
    return {"ok": True, "items": cut, "total": total, "page": page, "pages": pages, "size": size, "all": len(r["items"])}


def done_all_words(what, find="", picked=False):
    r = done_page(what, find, 1, 200, picked)
    if not r.get("ok"):
        return []
    out, pg = [], 1
    while True:
        out += [x["word"] for x in r["items"]]
        if pg >= r["pages"]:
            break
        pg += 1
        r = done_page(what, find, pg, 200, picked)
    return out
