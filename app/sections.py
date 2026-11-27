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
import time

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


def _pic(p):
    """一幅画（{bg, img, items, text…}）说成一句话"""
    if not isinstance(p, dict):
        return str(p)[:60]
    bits = []
    img = str(p.get("img") or p.get("bg") or "")
    if img:
        bits.append("背景 " + img.split("/")[-1].replace(".svg", ""))
    its = [str(i.get("svg") or i.get("emoji") or i.get("text") or "").split("/")[-1].replace(".svg", "") for i in (p.get("items") or []) if isinstance(i, dict)]
    its = [i for i in its if i]
    if its:
        bits.append("画了 %d 样：%s" % (len(its), "、".join(its[:6]) + ("…" if len(its) > 6 else "")))
    if p.get("text"):
        bits.append("字：" + str(p["text"])[:30])
    return "；".join(bits) or "（空的）"


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
                v = part.get(k)
                if isinstance(v, dict):
                    for pk, pv in list(v.items())[:4]:
                        L.append("%s %s：%s" % ({"partPics": "画", "icons": "图标"}[k], pk, _pic(pv) if isinstance(pv, dict) else str(pv)[:40]))
                elif v:
                    L.append("%s：%s" % ({"partPics": "每一部分的画", "icons": "小图标"}[k], str(v)[:120]))
        elif sid == "combo":
            L.append("组合 → 现在的含义（总表）：" + (trow.get("组合 → 现在的含义") or "—")[:160])
            if part.get("comboPic"):
                L.append("拼起来那一格的画：" + _pic(part["comboPic"]))
        elif sid == "scene":
            for i, x in enumerate(part.get("pics") or []):
                L.append("第 %d 个意思：%s" % (i + 1, _pic(x)))
        elif sid == "example":
            for i, x in enumerate(part.get("pics") or []):
                if x.get("ex"):
                    L.append("第 %d 个意思的例句：%s　%s%s" % (i + 1, x.get("ex"), x.get("exzh") or "", ("　动画：" + _pic(x["exPic"])) if isinstance(x.get("exPic"), dict) else ""))
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
                     "table": table_lines(s["id"], trow), "pics": pics_struct(s["id"], word, part) if P is not None else [],
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
    pend_add(done or [], sid)
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
                      "table": table_lines(sid, trow), "pics": pics_struct(sid, w, part) if P is not None else [], "pending": sid in pend_get(w),
                      "lines": _brief(s, part, trow, rec)[:4] if P is not None else [], "ts": str((rec or {}).get("画面生成") or "") if P is not None else "",
                      "ver": str((rec or {}).get("画面技能版本") or "") if P is not None else ""})
    for x in items:                                   # v1.33.0：这一块自己记的时间、版本（单独重做过的）
        b = ((_rec_of(x["word"], rows) or {}).get("板块") or {}).get(sid)
        if b:
            x["ts"], x["ver"] = b.get("时间") or x["ts"], b.get("版本") or x["ver"]
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
    pend_add(done, sid)
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
    vr = verify_load()
    for x in items:
        x["verify"] = vr.get(x["word"])
    items.sort(key=lambda x: (not x["flags"], not (x["verify"] and not x["verify"].get("ok")), x["word"].lower()))
    return {"ok": True, "items": items, "version": C.STATE.get("version") or ""}



def clear_block(sid, words):
    """v1.31.0：删掉这几个词的这一块（画面设置里这一块清空），退回「画面」等着重做"""
    s = BY_ID.get(sid)
    if not s or sid not in AI_EDIT:
        return {"ok": False, "msg": "这一块不能在这里删"}
    words = [w for w in (words or []) if isinstance(w, str) and w.strip()]
    done = []
    with C.REPO_LOCK:
        for w in words:
            pp, P = _prefs(w)
            if P is None:
                continue
            for k in s["keys"]:
                if k == "pics" and s.get("fields"):
                    for x in P.get("pics") or []:
                        if isinstance(x, dict):
                            for f in s["fields"]:
                                x.pop(f, None)
                else:
                    P.pop(k, None)
            pp.write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")
            done.append(w)
    if not done:
        return {"ok": False, "msg": "选的词还没有画面设置"}
    import pics
    pics.send_back({w: ["用户删掉了「%s」这一块，要按最新的视频技能重做这一块，别的照旧" % s["name"]] for w in done}, src="「%s」删掉" % s["name"])
    pend_add(done, sid)
    return {"ok": True, "n": len(done), "msg": "删掉了 %d 个词的「%s」：退回去了，到「一次做全」点「补画面」重做这一块" % (len(done), s["name"])}



# ═══════════════ v1.32.0：总表和视频各块的关系；画能点开看 ═══════════════
# 用户：“词根词缀内容要查看仓库中的总表，里面有内容；拼起来也是……意思场景具体画了什么，要有超链接，点击可以查看图片；意思查看也在总表里面有”
TABLE_OF = {   # 视频的块 ← 总表的列
    "pron": ["读音现象"],
    "parts": ["拆分", "前缀", "词根", "单词部分", "后缀", "词根变体处理"],
    "combo": ["组合 → 现在的含义"],
    "scene": ["含义", "初中含义"],
    "evolve": ["组合 → 现在的含义", "新·背景（只写在词族第一个词上）"],
    "example": [],
    "dist": ["辨析"],
    "kaodian": ["考点"],
    "board": ["音变 / 字母变化"],
    "lianxi": [],
}


def table_lines(sid, trow):
    out = []
    for k in TABLE_OF.get(sid, []):
        v = str(trow.get(k) or "").strip()
        if v and v not in ("-", "—"):
            if sid == "combo" and "【演变】" in v:
                v = v.split("【演变】")[0].strip()
            if sid == "evolve" and k.startswith("组合") :
                v = ("【演变】" + v.split("【演变】", 1)[1].strip()) if "【演变】" in v else v
            out.append({"k": k.replace("（只写在词族第一个词上）", ""), "v": v})
    return out


def _art_path(word, rel):
    """画面设置里的 art/xxx.svg → 实际文件：词库/画面设置/art/<词>/xxx.svg，没有再找视频技能自带的场景和 kit"""
    name = str(rel or "").split("/")[-1]
    if not name or ".." in name:
        return None
    f = V.folder_of(word)
    for p in (C.REPO / V.EXTRA / "art" / f / name, C.REPO / "引擎" / "视频" / "references" / "scenes" / name,
              C.REPO / "引擎" / "视频" / "references" / "kit-7A-U4" / "art" / name):
        if p.is_file():
            return p
    return None


def art_file(word, rel):
    p = _art_path(word, rel)
    if not p:
        return None, None
    return p.read_bytes(), "image/svg+xml"


def _pic_struct(word, label, p):
    if not isinstance(p, dict):
        return None
    img = p.get("img") or (("art/%s.svg" % p["bg"]) if p.get("bg") and p.get("bg") not in ("blank",) else "")
    items = []
    for it in p.get("items") or []:
        if not isinstance(it, dict):
            continue
        src = it.get("svg") or ""
        nm = str(src or it.get("emoji") or it.get("text") or it.get("pose") or it.get("actor") or "").split("/")[-1].replace(".svg", "")
        items.append({"name": nm or "（人物）", "src": src if src and _art_path(word, src) else "", "x": it.get("x"), "y": it.get("y"), "s": it.get("s"), "emoji": it.get("emoji") or ""})
    return {"label": label, "bg": str(img).split("/")[-1].replace(".svg", "") if img else "", "bgSrc": img if img and _art_path(word, img) else "",
            "items": items, "text": str(p.get("text") or "")}


def pics_struct(sid, word, part):
    out = []
    if sid == "scene":
        for i, x in enumerate(part.get("pics") or []):
            r = _pic_struct(word, "第 %d 个意思" % (i + 1), x)
            if r:
                out.append(r)
    elif sid == "example":
        for i, x in enumerate(part.get("pics") or []):
            if isinstance(x, dict) and isinstance(x.get("exPic"), dict):
                r = _pic_struct(word, "第 %d 个意思的例句动画" % (i + 1), x["exPic"])
                if r:
                    out.append(r)
    elif sid == "combo" and isinstance(part.get("comboPic"), dict):
        r = _pic_struct(word, "拼起来那一格", part["comboPic"])
        if r:
            out.append(r)
    elif sid == "parts":
        for k in ("partPics",):
            v = part.get(k)
            if isinstance(v, dict):
                for pk, pv in v.items():
                    r = _pic_struct(word, "第 %s 部分的画" % pk.replace("p", ""), pv)
                    if r:
                        out.append(r)
    elif sid == "dist":
        d = part.get("distinguish") or {}
        pics = d.get("pics") if isinstance(d, dict) else None
        if isinstance(pics, dict):
            for k, v in pics.items():
                r = _pic_struct(word, "%s 的画" % k, v)
                if r:
                    out.append(r)
    return out


# ═══════════════ v1.33.0：每一块单独让 AI 做（只改这一块，别的块原样保住）；每一块记自己的时间、版本；AI 核对总表 ═══════════════
_PEND = lambda: C.DATA / "block_redo.json"          # {单词: [要重做的块]}：补画面时只收这几块，别的照旧


def _pend_load():
    try:
        return json.loads(_PEND().read_text(encoding="utf-8"))
    except Exception:
        return {}


def pend_add(words, sid):
    d = _pend_load()
    for w in words:
        if sid not in d.setdefault(w, []):
            d[w].append(sid)
    _PEND().write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def pend_get(word):
    return list(_pend_load().get(word) or [])


def pend_clear(word):
    d = _pend_load()
    if d.pop(word, None) is not None:
        _PEND().write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


BLOCK_TIPS = {
    "parts": "每个部分（前缀、词根、单词部分、后缀）一张卡：partPics 里 p0、p1… 每张一幅小画，icons 里每张一个小图标；画要和这一部分的意思对得上（看总表的前缀、词根、单词部分、后缀）。",
    "combo": "comboPic：几个部分拼起来以后、这个词现在的意思的一幅画（看总表「组合 → 现在的含义」的【构词逻辑】）。",
    "scene": "pics 里每个意思一幅生活场景（bg / img 背景、items 里的东西和人物、text 写这个意思）：一眼能看出是这个意思，东西要摆得像真的场景。",
    "evolve": "flow：意思怎么一步步变过来的几步（node 一步的字、say 念的话、fig 小图），照总表【演变】和【构词逻辑】。",
    "example": "pics 里每个意思的例句：ex 一句简单的英文例句（初中生看得懂，用到这个词），exzh 中文，exPic 例句的动画（背景、东西、人物，和例句说的事对得上）。",
    "dist": "distinguish：同义词辨析——items 里每个词写 m（意思、区别一句话）、ex（一句例句）、exZh（中文）；pics 里每个词一幅画；key、logic、tip 照规矩。",
    "pron": "sylIpa：每一块的音标（和音节表的分块一一对上）。",
    "kaodian": "kaodian：考点（照总表「考点」，可以改写得更适合视频）。",
    "board": "board、extend：总结小黑板、扩展词（扩展词要是总表里有的词）。",
}


def focus_text(word, items):
    """补画面的提示词里：这个词要是只重做某几块，写清楚只改哪几个字段"""
    sids = pend_get(word)
    for it in items or []:
        for m in re.finditer(r"「([^」]+)」这一块", it):
            if m.group(1) in BY_NAME and BY_NAME[m.group(1)] not in sids:
                sids.append(BY_NAME[m.group(1)])
    sids = [x for x in sids if x in BY_ID]
    if not sids:
        return ""
    parts = []
    for x in sids:
        s = BY_ID[x]
        keys = "、".join(s["keys"]) + (("（pics 里只改 %s）" % "、".join(s["fields"])) if s.get("fields") else "")
        parts.append("「%s」——画面设置里的 %s。%s" % (s["name"], keys, BLOCK_TIPS.get(x, "")))
    return ("这一次只重做下面这几块，**别的字段照抄上次的画面设置，一个字都不要改**（程序只收这几块，别的你改了也不会用）：\n"
            + "\n".join("- " + p for p in parts))


def merge_blocks(old, new, sids):
    """只收 sids 这几块：别的照旧"""
    out = json.loads(json.dumps(old or {}))
    for x in sids:
        s = BY_ID.get(x)
        if not s:
            continue
        for k in s["keys"]:
            if k == "pics" and s.get("fields"):
                op, np_ = out.get("pics") or [], (new or {}).get("pics") or []
                for i, nx in enumerate(np_):
                    if not isinstance(nx, dict):
                        continue
                    if i >= len(op):
                        op.append({f: nx[f] for f in nx})
                        continue
                    for f in s["fields"]:
                        if f in nx:
                            op[i][f] = nx[f]
                        else:
                            op[i].pop(f, None)
                out["pics"] = op
            elif k in (new or {}):
                out[k] = new[k]
            else:
                out.pop(k, None)
    return out


def stamp(rec, sids, prov):
    """词库记录里每一块记自己的时间、版本"""
    try:
        import pics
        sv = pics.skill_version()[0]
    except Exception:
        sv = ""
    b = rec.setdefault("板块", {})
    for x in sids:
        b[x] = {"时间": time.strftime("%Y-%m-%d %H:%M"), "版本": ("视频技能 %s" % sv) if sv else "", "来源": prov}


AI_BLOCKS = ["parts", "combo", "scene", "evolve", "example", "dist"]
_VER = lambda: C.DATA / "verify.json"               # AI 核对总表的结果 {单词: {ts, ok, issues, provider}}


def verify_load():
    try:
        return json.loads(_VER().read_text(encoding="utf-8"))
    except Exception:
        return {}


VERIFY_PROMPT = """【核对总表 · %d 个词】你在帮一位初中英语老师核对“词源拆分总表”。下面每个词有总表里的几列（拆分、前缀、词根、单词部分、后缀、组合 → 现在的含义、考点、读音现象）。
请逐个检查：拆分和词源说法对不对（有没有编造、张冠李戴）；各部分的解释和例子对不对；考点（变形、短语、用法）有没有错；对初中生是不是讲得清楚。
只回一段 JSON，不要别的字：[{"word": "单词", "ok": true 或 false, "issues": ["哪一列：什么问题，应该怎么改", …]}]。没问题的 issues 写 []。

%s"""


def do_verify(R, tid, p):
    words = [w for w in (p.get("words") or []) if isinstance(w, str) and w.strip()]
    C.load_table()
    res = verify_load()
    cols = ["拆分", "前缀", "词根", "单词部分", "后缀", "组合 → 现在的含义", "考点", "读音现象"]
    for i in range(0, len(words), 12):
        R.check_stop()
        grp = words[i:i + 12]
        mat = []
        for w in grp:
            r = ((C.TABLE.get("words") or {}).get(w) or [{}])[0]
            mat.append("@%s（%s）\n%s" % (w, r.get("初中含义") or r.get("含义") or "", "\n".join("【%s】%s" % (k, str(r.get(k) or "—")[:500]) for k in cols)))
        rep = R.ask(tid, "核对总表", VERIFY_PROMPT % (len(grp), "\n\n".join(mat)), grp) or ""
        m = re.search(r"\[[\s\S]*\]", rep)
        got = []
        try:
            got = json.loads(m.group(0)) if m else []
        except Exception:
            got = []
        prov = C.provider_name()
        seen = set()
        for x in got if isinstance(got, list) else []:
            if isinstance(x, dict) and x.get("word") in grp:
                iss = [str(t) for t in (x.get("issues") or []) if str(t).strip()]
                res[x["word"]] = {"ts": time.strftime("%Y-%m-%d %H:%M"), "ok": bool(x.get("ok")) and not iss, "issues": iss, "provider": prov}
                seen.add(x["word"])
        miss = [w for w in grp if w not in seen]
        if miss:
            C.log("AI 核对总表：%s 没回结果（回复里没认出来）" % "、".join(miss), tid)
        _VER().write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        C.log("AI 核对总表：%d 个词，%d 个有问题" % (len(seen), sum(1 for w in seen if not res[w]["ok"])), tid)
