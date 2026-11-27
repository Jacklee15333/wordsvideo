# -*- coding: utf-8 -*-
"""单词工作台 · v1.29.0：单词简历——一个词的视频分成哪几块、每一块从哪来、做好没、什么时候用哪个版本做的；能看、能改、能单独重做。
用户：“每个做好的单词都可以点开，查看做好的结果，就是每个单词都可以有单独的单词简历页面，点击可以查看各个部分的结果，可以进行修改”。

视频的板块（精简版，按出场顺序）和它们的来源：
  一、读音拆分        总表 + 音节表（不用 AI；对不齐时 AI 在画面设置里写 sylIpa）
  二、含义拆分（大类）
      词根词缀卡      字：总表（拆分、各部分解释、记）；画：AI（画面设置 partPics、icons、text）
      拼起来          AI（comboPic、route）
      意思场景        AI（pics 里每个意思的场景：bg、img、text、pos、diff、items）
      意思演变        AI（flow）
      例句动画        AI（pics 里每个意思的例句：ex、exzh、exPic）
  三、同义词辨析      AI（distinguish：每个词的画、意思 m、区别、例句 ex / exZh）；总表「辨析」列参考
  四、考点            总表（画面设置 kaodian 可以改写）
  五、总结小黑板      自动（board、extend 扩展词）
  六、练习 / 七、答案  AI（出题这一步）
画面设置的改动写回 词库/画面设置/words/<词>.json，标成“改过，出片时再起草检查”，提交、上传。"""
import json
import re

import core as C
import video as V

# id, 大类, 名字, 来源, 画面设置里的键（pics 按字段分给“意思场景”“例句动画”）
SECTIONS = [
    {"id": "pron", "cat": "一、读音拆分", "name": "读音拆分", "src": "总表·音节表", "keys": ["sylIpa", "ipa", "pron"]},
    {"id": "parts", "cat": "二、含义拆分", "name": "词根词缀卡", "src": "字：总表；画：AI", "keys": ["partPics", "icons", "text"]},
    {"id": "combo", "cat": "二、含义拆分", "name": "拼起来", "src": "AI", "keys": ["comboPic", "route"]},
    {"id": "scene", "cat": "二、含义拆分", "name": "意思场景", "src": "AI", "keys": ["pics"], "fields": ["bg", "img", "text", "pos", "diff", "items"]},
    {"id": "evolve", "cat": "二、含义拆分", "name": "意思演变", "src": "AI", "keys": ["flow"]},
    {"id": "example", "cat": "二、含义拆分", "name": "例句动画", "src": "AI", "keys": ["pics"], "fields": ["ex", "exzh", "exPic"]},
    {"id": "dist", "cat": "三、同义词辨析", "name": "同义词辨析", "src": "AI（总表「辨析」参考）", "keys": ["distinguish"]},
    {"id": "kaodian", "cat": "四、考点", "name": "考点", "src": "总表", "keys": ["kaodian"]},
    {"id": "board", "cat": "五、总结", "name": "总结小黑板", "src": "自动", "keys": ["board", "extend", "familyWords"]},
    {"id": "lianxi", "cat": "六、练习 / 七、答案", "name": "练习题", "src": "AI（出题）", "keys": []},
]
BY_ID = {s["id"]: s for s in SECTIONS}
AI_EDIT = {"pron", "parts", "combo", "scene", "evolve", "example", "dist", "kaodian", "board"}     # 能在简历页改画面设置的块

# “还要补”的一条归到哪一块（先看前面的）
TODO_MAP = [("dist", r"同义词辨析|辨析"), ("pron", r"读音|音标|sylIpa"), ("evolve", r"意思怎么|演变|flow"),
            ("example", r"例句"), ("combo", r"拼起来|comboPic|合起来"), ("parts", r"词缀|词根|partPics|图标|icons|卡片"),
            ("scene", r"意思的画|场景|背景|pics|画得太简单"), ("kaodian", r"考点"), ("board", r"小黑板|扩展"), ("lianxi", r"练习|题")]


def _prefs(word):
    p = C.REPO / V.EXTRA / "words" / (V.folder_of(word) + ".json")
    try:
        return p, json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return p, None


def _slice(P, sec):
    """这一块在画面设置里的那一部分"""
    out = {}
    for k in sec["keys"]:
        if k not in P:
            continue
        if k == "pics" and sec.get("fields"):
            out["pics"] = [{f: x.get(f) for f in sec["fields"] if isinstance(x, dict) and f in x} for x in (P.get("pics") or [])]
        else:
            out[k] = P[k]
    return out


def _has(v):
    if isinstance(v, list):
        return any(_has(x) for x in v)
    if isinstance(v, dict):
        return any(_has(x) for x in v.values())
    return v not in (None, "", False)


def _brief(sec, part, trow, rec):
    """给人看的几行"""
    L = []
    sid = sec["id"]
    try:
        if sid == "pron":
            if part.get("sylIpa"):
                L.append("每一块的音标（画面设置写的）：" + " + ".join(map(str, part["sylIpa"])))
            L.append("读音拆分照音节表；对不齐时用画面设置里的音标")
        elif sid == "parts":
            L.append("拆分（总表）：" + (trow.get("拆分") or "—"))
            for k in ("partPics", "icons"):
                if part.get(k):
                    L.append("%s：%s" % ({"partPics": "每一部分的画", "icons": "小图标"}[k], "、".join(map(str, (part[k].keys() if isinstance(part[k], dict) else part[k])))[:200]))
        elif sid == "combo":
            L.append("组合 → 现在的含义（总表）：" + (trow.get("组合 → 现在的含义") or "—")[:160])
            if part.get("comboPic"):
                L.append("拼起来那一格的画：" + str(part["comboPic"])[:120])
        elif sid == "scene":
            for i, x in enumerate(part.get("pics") or []):
                L.append("第 %d 个意思：%s%s" % (i + 1, str(x.get("text") or "")[:60], ("（背景 %s）" % x["bg"]) if x.get("bg") else ""))
        elif sid == "example":
            for i, x in enumerate(part.get("pics") or []):
                if x.get("ex"):
                    L.append("第 %d 个意思的例句：%s　%s" % (i + 1, x.get("ex"), x.get("exzh") or ""))
        elif sid == "evolve":
            for i, x in enumerate(part.get("flow") or []):
                L.append("%d. %s" % (i + 1, (x.get("node") or x.get("say") or "") if isinstance(x, dict) else x))
        elif sid == "dist":
            d = part.get("distinguish") or {}
            if isinstance(d, dict):
                for it in d.get("items") or []:
                    if isinstance(it, dict):
                        L.append("%s：%s%s" % (it.get("w", ""), it.get("m") or it.get("note") or "", ("　例：" + it["ex"]) if it.get("ex") else "　（还没有例句）"))
            if trow.get("辨析"):
                L.append("总表「辨析」：" + trow["辨析"][:160])
        elif sid == "kaodian":
            L.append("总表「考点」：" + (trow.get("考点") or "—")[:240])
            if part.get("kaodian"):
                L.append("画面设置改写了考点")
        elif sid == "board":
            if part.get("extend"):
                L.append("扩展词：" + "、".join((x.get("w") if isinstance(x, dict) else str(x)) for x in part["extend"])[:200])
            L.append("小黑板：" + ("不要" if part.get("board") is False else "自动汇总前面的"))
        elif sid == "lianxi":
            qs = (rec or {}).get("题目原稿") or []
            for i, q in enumerate(qs[:7]):
                if isinstance(q, dict):
                    L.append("%d. %s" % (i + 1, str(q.get("stem") or q.get("listen") or q.get("zh") or "")[:90].replace("\n", " ")))
            if not qs and (rec or {}).get("题目"):
                L.append("题库里原来就有的题目")
    except Exception as e:
        L.append("（这一块没读懂：%s）" % str(e)[:80])
    return L


def profile(word):
    word = (word or "").strip()
    if not word:
        return {"ok": False, "msg": "没给单词"}
    try:
        C.load_table()
    except Exception:
        pass
    trows = (C.TABLE.get("words") or {}).get(word) or []
    trow = trows[0] if trows else {}
    det = C.word_detail(word) or {}
    _, rows = C.read_index()
    rel = next((r[6] for r in rows if r[2] == word and len(r) > 6 and r[6]), "")
    rec = None
    if rel:
        try:
            rec = json.loads((C.REPO / C.D / rel).read_text(encoding="utf-8"))
        except Exception:
            rec = None
    pp, P = _prefs(word)
    chk = str((rec or {}).get("检查") or "")
    todo = [x.strip() for x in re.split(r"[；;]", chk.split("还要补：", 1)[1]) if x.strip()] if "还要补：" in chk and "都齐了" not in chk else []
    secs = []
    for s in SECTIONS:
        part = _slice(P, s) if P else {}
        issues = [t for t in todo if _sec_of(t) == s["id"]]
        if s["id"] == "lianxi":
            has = bool((rec or {}).get("题目") or (rec or {}).get("题目原稿"))
            ts, ver = str((rec or {}).get("题目生成") or ""), str((rec or {}).get("题目版本") or "")
        elif s["src"].startswith("总表") and s["id"] in ("kaodian",):
            has = bool(trow.get("考点")) or _has(part)
            ts, ver = "", "总表 " + str(C.STATE.get("version") or "")
        elif s["id"] == "pron":
            has = True
            ts, ver = "", "音节表"
        elif s["id"] == "board":
            has = True
            ts, ver = "", "自动"
        else:
            has = _has(part)
            ts, ver = str((rec or {}).get("画面生成") or ""), str((rec or {}).get("画面技能版本") or "")
        st = "fix" if issues else ("ok" if has else ("none" if P is not None or s["id"] == "lianxi" else "nopic"))
        secs.append({"id": s["id"], "cat": s["cat"], "name": s["name"], "src": s["src"], "status": st, "ts": ts, "ver": ver,
                     "issues": issues, "lines": _brief(s, part, trow, rec), "data": part if s["id"] in AI_EDIT and P is not None else None,
                     "editable": s["id"] in AI_EDIT and P is not None})
    vd = V.videos().get(V.folder_of(word)) or {}
    return {"ok": True, "word": word, "meaning": trow.get("初中含义") or trow.get("含义") or "", "table": {k: trow.get(k, "") for k in C.FIELDS},
            "hasPic": P is not None, "picCheck": chk[:300], "picTs": str((rec or {}).get("画面生成") or ""), "picVer": str((rec or {}).get("画面技能版本") or ""),
            "video": {"file": vd.get("file", ""), "ts": vd.get("ts", ""), "ver": vd.get("ver", ""), "batch": vd.get("batch", "")} if vd else None,
            "sections": secs, "manual": bool(det.get("manual")) if isinstance(det, dict) else False}


def save(word, sid, data):
    """简历页改了一块：写回画面设置（pics 按字段合进去），标成“改过、出片时再起草检查”，提交"""
    s = BY_ID.get(sid)
    if not s or sid not in AI_EDIT:
        return {"ok": False, "msg": "这一块不能在这里改"}
    if not isinstance(data, dict):
        return {"ok": False, "msg": "格式不对：要是一个 JSON 对象（{ … }）"}
    bad = [k for k in data if k not in s["keys"]]
    if bad:
        return {"ok": False, "msg": "这一块只能改这几项：%s（多了 %s）" % ("、".join(s["keys"]), "、".join(bad))}
    with C.REPO_LOCK:
        pp, P = _prefs(word)
        if P is None:
            return {"ok": False, "msg": "这个词还没有画面设置：先到「画面」做"}
        for k, v in data.items():
            if k == "pics" and s.get("fields"):
                old = P.get("pics") or []
                if not isinstance(v, list):
                    return {"ok": False, "msg": "pics 要是一个列表"}
                for i, x in enumerate(v):
                    if i < len(old) and isinstance(old[i], dict) and isinstance(x, dict):
                        for f in s["fields"]:
                            if f in x:
                                old[i][f] = x[f]
                            elif f in old[i]:
                                old[i].pop(f)
                P["pics"] = old
            else:
                P[k] = v
        pp.write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")
        _, rows = C.read_index()
        rel = next((r[6] for r in rows if r[2] == word and len(r) > 6 and r[6]), "")
        if rel:
            p = C.REPO / C.D / rel
            try:
                rec = json.loads(p.read_text(encoding="utf-8"))
                rec["检查"] = "本机检查通过，出片时再起草检查（单词简历里改了「%s」）" % s["name"]
                rec["画面"] = P
                p.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
            except Exception:
                pass
    try:
        import pics
        pics._UC["t"] = 0.0
    except Exception:
        pass
    C.log("单词简历：改了 %s 的「%s」" % (word, s["name"]))
    import threading
    threading.Thread(target=lambda: C.commit_pending("词库：单词简历里改了 %s 的「%s」（单词工作台）" % (word, s["name"])), daemon=True).start()
    return {"ok": True, "msg": "改好了：%s 的「%s」。出片前会再做一次起草检查" % (word, s["name"])}


def redo(word, sid, note=""):
    """只重做这一块：画面的块——退回「画面」，补画面时 AI 只改这一块（别的不动）；练习题——题目删掉，回到「出题」"""
    s = BY_ID.get(sid)
    if not s:
        return {"ok": False, "msg": "不认识这一块"}
    if sid == "lianxi":
        import clear as CL
        return CL.done_op("redo", "q", [word])
    if sid in ("pron", "kaodian", "board") and not note:
        note = ""
    import pics
    item = "用户要重做「%s」这一块：%s只改这一块，别的照旧" % (s["name"], (note.strip().rstrip("。") + "。") if note.strip() else "按最新的视频技能重新做；")
    done = pics.send_back({word: [item]}, src="单词简历")
    if not done:
        return {"ok": False, "msg": "没退回去：这个词还没有画面设置（先到「画面」做）"}
    return {"ok": True, "msg": "退回「画面」了：%s 只重做「%s」（补画面时交给 AI，别的块不动）" % (word, s["name"])}


# ═══════════════ v1.30.0：按块的步骤（「含义拆分」五个小类、「同义词辨析」）和「导入」 ═══════════════
BY_NAME = {s["name"]: s["id"] for s in SECTIONS}


def _sec_of(line):                                   # 视频技能 6.57 起“还要补”每条带【块名】，先认它
    m = re.match(r"\s*【([^】]+)】", line or "")
    if m and m.group(1) in BY_NAME:
        return BY_NAME[m.group(1)]
    for sid, pat in TODO_MAP:
        if re.search(pat, line or ""):
            return sid
    return ""


def _picked():
    import pool
    pool._db()
    return [r["word"] for r in C.q("SELECT word FROM pool WHERE picked=1 ORDER BY ord")]


def _todo_of(rec):
    chk = str((rec or {}).get("检查") or "")
    if "还要补：" not in chk or "都齐了" in chk:
        return []
    return [x.strip() for x in re.split(r"[；;]", chk.split("还要补：", 1)[1]) if x.strip()]


def _rec_of(word, rows):
    rel = next((r[6] for r in rows if r[2] == word and len(r) > 6 and r[6]), "")
    if not rel:
        return None
    try:
        return json.loads((C.REPO / C.D / rel).read_text(encoding="utf-8"))
    except Exception:
        return None


def blocks(sid):
    """一个块的步骤页：选上的词，这一块做好没、要补什么"""
    s = BY_ID.get(sid)
    if not s:
        return {"ok": False, "msg": "不认识这一块"}
    try:
        C.load_table()
    except Exception:
        pass
    _, rows = C.read_index()
    items, cnt = [], {"ok": 0, "fix": 0, "none": 0, "nopic": 0}
    for w in _picked():
        _, P = _prefs(w)
        rec = _rec_of(w, rows)
        trow = ((C.TABLE.get("words") or {}).get(w) or [{}])[0]
        issues = [t for t in _todo_of(rec) if _sec_of(t) == sid]
        part = _slice(P, s) if P else {}
        st = "nopic" if P is None else ("fix" if issues else ("ok" if _has(part) else "none"))
        if st == "none" and sid in ("combo", "parts") and "+" not in (trow.get("拆分") or ""):
            st = "na"                                 # 只有一个部分的词（make）：没有“拼起来”、词根词缀卡也不用画
        cnt[st] = cnt.get(st, 0) + 1
        items.append({"word": w, "meaning": trow.get("初中含义") or "", "status": st, "issues": issues,
                      "lines": _brief(s, part, trow, rec)[:4] if P is not None else [], "ts": str((rec or {}).get("画面生成") or "") if P is not None else "",
                      "ver": str((rec or {}).get("画面技能版本") or "") if P is not None else ""})
    order = {"fix": 0, "none": 1, "nopic": 2, "ok": 3, "na": 4}
    items.sort(key=lambda x: order[x["status"]])
    return {"ok": True, "sec": sid, "name": s["name"], "cat": s["cat"], "items": items, "counts": cnt}


def redo_many(sid, words, note=""):
    s = BY_ID.get(sid)
    if not s or sid not in AI_EDIT:
        return {"ok": False, "msg": "这一块不能在这里重做"}
    words = [w for w in (words or []) if isinstance(w, str) and w.strip()]
    if not words:
        return {"ok": False, "msg": "一个都没选"}
    import pics
    item = "用户要重做「%s」这一块：%s只改这一块，别的照旧" % (s["name"], (note.strip().rstrip("。") + "。") if (note or "").strip() else "按最新的视频技能重新做；")
    done = pics.send_back({w: [item] for w in words}, src="「%s」" % s["name"]) or []
    if not done:
        return {"ok": False, "msg": "没退回去：选的词还没有画面设置"}
    return {"ok": True, "n": len(done), "msg": "%d 个词的「%s」退回去重做了：到「含义拆分 → 一次做全」点「补画面」，AI 只改这一块" % (len(done), s["name"])}


def imp_list():
    """「导入」：不用 AI 的几块——意思、拆分、考点、辨析从总表来；读音拆分从音节表来（出片时起草检查对齐）"""
    try:
        C.load_table()
    except Exception as e:
        return {"ok": False, "msg": "总表没读到（%s）" % str(e)[:120]}
    items = []
    for w in _picked():
        rs = (C.TABLE.get("words") or {}).get(w) or []
        r = rs[0] if rs else {}
        _, P = _prefs(w)
        flags = [x for x, ok in (("总表里没有这个词", bool(rs)), ("缺拆分", bool(r.get("拆分"))), ("缺考点", bool(r.get("考点")))) if not ok]
        items.append({"word": w, "meaning": r.get("初中含义") or r.get("含义") or "", "split": r.get("拆分", ""), "kaodian": r.get("考点", ""),
                      "bianxi": r.get("辨析", ""), "combo": r.get("组合 → 现在的含义", ""), "sylIpa": " + ".join(map(str, (P or {}).get("sylIpa") or [])),
                      "flags": flags, "rows": len(rs)})
    items.sort(key=lambda x: (not x["flags"], x["word"].lower()))
    return {"ok": True, "items": items, "version": C.STATE.get("version") or ""}
