# -*- coding: utf-8 -*-
"""单词工作台 · v1.47.0：视频图片的每一块，单独让 AI 做（像「出题」那样）。
用户：“现在是在做词根词缀卡，你看提示词对吗，我希望做词根词缀卡时，只专注做词根词缀卡，不要做其他的，就像题目哪个板块一样”。

以前“只重做一块”走的是补画面：提示词里是整份画面设置、全部规矩、pictures.md 全文、整个范例，还要 AI 把整份 JSON 重写一遍，
检查没过的又是整个词的“还要补”（别的块的问题也让 AI 改）。现在这一块自己一份提示词：
  - 只讲这一块：视频里这一块是什么、这个词这一块念的话（配音稿）、总表里和这一块有关的那几列、这一块上次的设置、要补的
  - 规矩、pictures.md 只放和这一块有关的几条 / 几节；范例只放范例词的这一块
  - AI 只写这一块的几项（比如 partPics、icons），程序合进原来的画面设置，别的块一个字不动
  - 检查只看这一块：起草检查里这一块没有要补的就算过；别的块的问题照旧记着，不让 AI 改
"""
import json
import re
import time

import core as C
import video as V
import pics as PX
import sections as SEC

# 每一块：AI 写画面设置里的哪几项；配哪几条规矩、pictures.md 哪几节；视频里这一块是什么
AI_KEYS = {"parts": ["partPics", "icons", "originPic"], "combo": ["comboPic"], "scene": ["pics"], "evolve": ["flow"],
           "example": ["pics"], "dist": ["distinguish"]}
RULES = {"parts": {13, 14, 16, 17, 21, 46, 47, 48, 50, 51, 57}, "combo": {3, 13, 14, 17, 21, 46, 47, 48, 50, 51, 57},
         "scene": {3, 13, 14, 21, 46, 47, 48, 50, 51, 56, 57}, "evolve": {4, 13, 15, 18, 21, 46, 47, 48, 50, 51, 56, 57},
         "example": {6, 13, 21, 46, 47, 48, 50, 51, 56, 57}, "dist": {24, 46, 47, 48, 50, 51, 57}}
MD = {"parts": ["一、", "三、", "五、", "六、", "十二、", "十三、", "十五、", "十六、", "十七、", "十八、", "二十、"],
      "combo": ["一、", "三、", "五、", "六、", "八、", "十二、", "十五、", "十六、", "十七、", "十八、", "二十、"],
      "scene": ["一、", "三、", "四、", "五、", "六、", "八、", "十二、", "十五、", "十六、", "十七、", "十八、", "十九、", "二十、"],
      "evolve": ["一、", "三、", "五、", "六、", "七、", "十一、", "十二、", "十五、", "十六、", "十七、", "十八、", "十九、", "二十、"],
      "example": ["一、", "三、", "五、", "六、", "九、", "十二、", "十五、", "十六、", "十七、", "十八、", "十九、", "二十、"],
      "dist": ["一、", "三、", "六、", "十四、同义词辨析", "十五、", "十六、", "十七、", "十八、", "二十、"]}
WHAT = {
    "parts": "视频「含义拆分」一开始，单词拆成几部分（前缀、词根、单词部分、后缀），每部分一张卡片。**卡片上的字、念的话，程序已经从总表提取好了（下面每个词写着），你不用写字，只画画**："
             "每部分卡片左边一幅会动的小画（partPics 里 p0、p1…，第几部分就是 p 几，从 p0 开始），后面“拼起来”那一格里每部分一个小图标（icons 里 p0、p1…，写自己画的正方形小图 art/icon-….svg）。"
             "不拆开的词（make 这种基础词、match ≈ make 这种）只有一张“来历”卡片：画写在 originPic（一幅），不用写 partPics、icons。",
    "combo": "拆开讲完每部分以后，“拼起来”那一格：几部分合起来的字面意思，一幅画（comboPic）。画字面意思，不画现在的意思。",
    "scene": "讲完拼起来，每个现在的意思一幅会动的生活场景（pics 里第 i 个意思一幅）：bg / img 背景、items 里的东西和人物，text 写这个意思、pos 词性、diff 一句话区别。",
    "evolve": "意思是怎么一步步变过来的（flow）：每一步 node 一步的字、say 念的话（一句讲一件画得出来的事）、fig 那一步的示意图，讲道理的那一步配音拆几句、图按句出东西。",
    "example": "每个意思一个例句，配一段把例句演出来的动画：pics 里第 i 个意思的 ex（英文例句，初中生看得懂、用到这个词）、exzh（中文）、exPic（例句动画）。",
    "dist": "同义词辨析：中文意思一样、英语不一样的几个词，每个词一张卡（一幅画、一句区别、一句例句），最后讲逻辑差在哪儿（distinguish：key、items、logic、tip、pics）。",
}


def _rules(keep):
    t = PX._p(PX.SKILL).read_text(encoding="utf-8")
    a = t.find("## 用户定下的规矩")
    b = t.find("\n## ", a + 10)
    sec = t[a:b] if a >= 0 else ""
    items = re.split(r"(?m)^(?=\d+\. \*\*)", sec)
    return "\n\n".join(x.strip() for x in items if re.match(r"(\d+)\. \*\*", x) and int(re.match(r"(\d+)", x).group(1)) in keep)


def _md(keep):
    pm = PX._p(PX.VR + "/pictures.md").read_text(encoding="utf-8")
    return PX._sections(pm, keep)


def _only(sid, P):
    """画面设置里这一块的几项（例句、意思场景只要 pics 里那几个字段）"""
    s = SEC.BY_ID[sid]
    P = P or {}
    if s.get("fields"):
        return {"pics": [{f: x.get(f) for f in s["fields"] if isinstance(x, dict) and f in x} for x in (P.get("pics") or [])]}
    return {k: P[k] for k in AI_KEYS[sid] if k in P}


def merge(sid, old, new):
    """把 AI 写的这一块合进原来的画面设置：只换这一块的几项，别的一个字不动（AI 没写的项也不删）"""
    out = json.loads(json.dumps(old or {}))
    s = SEC.BY_ID[sid]
    new = new or {}
    if s.get("fields"):
        op, np_ = out.get("pics") or [], new.get("pics") or []
        for i, nx in enumerate(np_):
            if isinstance(nx, dict) and i < len(op) and isinstance(op[i], dict):
                for f in s["fields"]:
                    if f in nx:
                        op[i][f] = nx[f]
        out["pics"] = op
    else:
        for k in AI_KEYS[sid]:
            if k in new:
                out[k] = new[k]
    return out


def _example(sid):
    try:
        ex = json.loads(PX.kit_example())
    except Exception:
        return ""
    return json.dumps(_only(sid, ex), ensure_ascii=False, separators=(",", ":"))[:9000]


def _clean(v):
    """总表一格 → 只留这一部分自己的那一句：去掉“辨析：…”“背景…”这些后面讲的长段，括号里的出处留短"""
    v = re.split(r"[；;]\s*(?:辨析|【背景】|背景|【辨析】)[:：]", str(v))[0]
    v = re.sub(r"\s+", " ", v).strip()
    return v[:160] + ("…" if len(v) > 160 else "")


def _issues(sid, w):
    """这个词这一块要补的（起草检查记下的、你点「只重做」时写的那句）"""
    line = PX.todo_all().get(w, "")
    out = []
    for x in PX._items(line):
        if SEC._sec_of(x) != sid:
            continue
        x = re.sub(r"^【[^】]+】", "", x)
        m = re.match(r"^用户要重做「[^」]+」这一块：(.*)$", x)
        if m:                                          # 点「让 AI 做」时写的那句
            x = re.sub(r"只改这一块，别的照旧[。；]?$", "", m.group(1)).strip().rstrip("；;。")
            x = ("老师的要求：" + x) if x and not x.startswith("按最新的视频技能重新做") else "按现在的视频技能把这一块重新做好"
        x = re.sub(r"（[^（）]*退回）$", "", x)
        if x not in out:
            out.append(x)
    return out


def _seg(sid, w, plans):
    s = SEC.BY_ID[sid]
    _, P = SEC._prefs(w)
    C.load_table()
    trow = ((C.TABLE.get("words") or {}).get(w) or [{}])[0]
    tl = SEC.table_lines(sid, trow) or SEC.table_lines("parts", trow)
    say = SEC.plan_lines(sid, (plans.get(V.folder_of(w)) or ("", None))[1])
    if sid == "parts":                                 # 总表原文里混着辨析、背景、记法以外的长段：只留这一部分自己的那一句
        tl = [dict(t, v=_clean(t["v"])) for t in tl if t["k"] in ("拆分", "前缀", "词根", "单词部分", "后缀", "词根变体处理")]
    cur = _only(sid, P)
    arts = sorted(set(re.findall(r"art/([\w.\-]+\.svg)", json.dumps(cur, ensure_ascii=False))) & set(PX._old_svgs(w)))
    iss = _issues(sid, w)
    out = ["@%s　%s" % (w, trow.get("初中含义") or "")]
    if sid == "parts":
        sp = str(trow.get("拆分") or "").strip()
        n = len([x for x in re.split(r"\s*\+\s*", sp) if x.strip()]) if "+" in sp else 1
        out.append("拆分：%s（%s）" % (sp or "不拆", "%d 部分：partPics、icons 写 p0…p%d" % (n, n - 1) if n > 1 else "不拆开：只有一张“来历”卡片，画写在 originPic"))
    if say:
        out.append("卡片上讲的（程序从总表提取好的，就是视频里念的；画要画这里说的东西，写 when 就用这里的词）：\n" +
                   "\n".join("- %s%s" % ((g["label"] + "：") if g["label"] else "", " ".join(g["say"])) for g in say))
    else:
        out.append("卡片上讲的（还没写讲稿，先看总表；视频里只念每部分的意思和记法）：\n" + ("\n".join("- %s：%s" % (t["k"], t["v"]) for t in tl) or "- （总表这几列是空的）"))
    out.append("要补的：\n" + ("\n".join("- " + x for x in iss) if iss else "- 没记下具体的：按现在的视频技能，把这一块重新做好"))
    out.append("上次这一块的设置（在它的基础上改；整块重写一遍）：\n```json\n%s\n```" % json.dumps(cur, ensure_ascii=False, separators=(",", ":"))[:6000])
    out.append("上次这一块用到、已经画好的插图（不改就不用再写）：%s" % ("、".join("art/" + a for a in arts) or "没有"))
    return "\n".join(out)


def build_prompt(sid, words, rnd):
    s = SEC.BY_ID[sid]
    ver, ed = PX.skill_version()
    try:
        plans = SEC.plans(words)
    except Exception:
        plans = {}
    keys = "、".join(AI_KEYS[sid]) + (("（pics 里每个意思只写 %s）" % "、".join(s["fields"])) if s.get("fields") else "")
    head = ("【只做「%s」· 这一批 %d 个词】你在帮一位中学英语老师给单词视频做画面（视频技能 %s，%s）。"
            "**这一次只做「%s」这一块**：只写画面设置里的 %s。别的块（%s）都不用管、不用写——写了程序也不收。\n"
            "这一块在视频里是什么：%s\n"
            "按顺序一个接一个写：每写完 %d 个词就上传一次（怎么传看最后），中间不用在聊天里汇报；这一批全部传完再汇报一次。"
            % (s["name"], len(words), ver, ed, s["name"], keys,
               "、".join(x["name"] for x in SEC.SECTIONS if x["id"] in SEC.AI_BLOCKS and x["id"] != sid), WHAT[sid], rnd))
    chk = ["用到的每张插图（art/名字.svg）：要么在“现成的插图”里，要么这个词上次画过（列在下面），要么这次画出来（写成 SVG 块）；只写名字不画，整个词作废",
           "讲什么就画什么：画里的东西和这一块念的话对得上，写 when 的词要真在念的话里",
           "主角要大（占画高一半左右），画成生活里的场景（有背景），不要表情图",
           "画里有人：动作名只能用列出来的，一个词里同一个动作别重复用；人要有动作、有互动"]
    if sid == "parts":
        chk.insert(1, "每部分一幅（partPics 的 p0、p1…和拆分的部分一一对上），每部分一个小图标（icons，自己画的正方形小图）；画的是这一部分的意思（词根要画记法里说的东西）")
    if sid == "dist":
        chk.insert(1, "每个词一张卡都要配画（distinguish.pics），items 里每个词写 m、ex、exZh")
    if sid in ("scene", "example"):
        chk.insert(1, "pics 的个数、顺序和上次一样（第几个意思就是第几项），只写 %s 这几个字段" % "、".join(s["fields"]))
    out_fmt = ("【输出格式（程序按这个格式自动读，请严格照做）】\n"
               "0. 一个词一段，按上面的顺序写：每段先单独一行写 @单词（比如 @%s），下面是这个词的内容。\n"
               "1. 每个词：一个代码块（第一行写 ```json），里面**只写这一块的 %s**，比如 %s。别的项一个都不要写。\n"
               "2. 画里的人不要自己画，写成 {\"actor\": \"动作名\", \"x\": 0.3, \"y\": 0.6, \"s\": 0.9, \"z\": 3}，程序会换成会动的人。动作名只能用这些：%s。\n"
               "3. 不许用表情图（\"e\": \"🚗\" 这种），东西都用写实插图：\"svg\": \"art/名字.svg\"。现成的场景和东西可以直接用：%s。\n"
               "4. 插图只写新画的、要重画的；每张一块，放在这个词的 JSON 代码块后面：\n<<<SVG 名字.svg\n<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 400 300\">……</svg>\n>>>END\n"
               "   插图要求：图画书风（黑色勾线、饱和平涂），画成现实生活里的样子；场景背景要详细、具体（不少于 150 个图形），一张图不超过 30 KB。\n"
               "5. 每次上传的内容，最后单独一行写：%s"
               % (words[0], keys, json.dumps({k: "…" for k in AI_KEYS[sid]}, ensure_ascii=False), "、".join(PX.motions()),
                  "、".join("art/" + x for x in PX.scenes()), C.END))
    return "\n\n".join([
        head,
        "【这一批的词（按这个顺序做）】\n" + "\n".join("%d. %s" % (i + 1, w) for i, w in enumerate(words)),
        "【交之前每个词自己对一遍（交上去软件马上起草检查「%s」这一块，没过的要回来改）】\n" % s["name"] + "\n".join("%d. %s" % (i + 1, x) for i, x in enumerate(chk)),
        "【每个词的材料】\n" + "\n\n".join(_seg(sid, w, plans) for w in words),
        "【视频技能 %s 里和「%s」有关的规矩】\n" % (ver, s["name"]) + _rules(RULES[sid]),
        "【pictures.md 里和「%s」有关的几节】\n" % s["name"] + _md(MD[sid]),
        "【范例：%s 的「%s」（过了起草检查的，写法和你要交的一样）】\n" % (PX.EXAMPLE_WORD, s["name"]) + (_example(sid) or "（范例没有这一块）"),
        out_fmt])


def accept(R, tid, sid, w, Pai, svgs, errs):
    """交回的一个词：合进原来的画面设置，起草检查；只看这一块。返回 (这一块过了吗, 告诉 AI 的话, 这一块要补的几条)"""
    _, old = SEC._prefs(w)
    if old is None:
        return False, "这个词还没有视频图片，先整套做", []
    if not Pai:
        return False, "；".join(errs or []) or "没读到 JSON", errs or []
    old.pop("lianxi", None)
    P = merge(sid, old, Pai)
    allsvg = dict(PX._old_svgs(w), **(svgs or {}))
    e2 = PX.check(w, P, allsvg)
    if e2:
        return False, PX.short_why(e2), e2
    C.relay_stage("%s：起草检查「%s」（在 WSL 里）…" % (w, SEC.BY_ID[sid]["name"]))
    R.stage = "%s：起草检查（在 WSL 里）" % w
    st, line = PX.wsl_draft_safe(w, P, allsvg)
    mine = [x for x in PX._items(line) if SEC._sec_of(x) == sid] if st == "todo" else []
    PX.save(w, P, allsvg, st == "ok")
    PX.todo_note(w, line if st == "todo" else "")
    if st in ("env", None):
        C.log("  %s 的起草检查没跑成（%s）：本机检查过了，先存下" % (w, (line or "")[:160]), tid)
    return (not mine), ("还要补：" + "；".join(mine)) if mine else "", mine


def run(R, tid, p):
    """任务：只做一块。p = {words, block, fix: True}"""
    sid = p.get("block")
    s = SEC.BY_ID.get(sid)
    words = [w for w in (p.get("words") or []) if SEC._prefs(w)[1] is not None]
    if not s or not words:
        C.log("只做一块：没有能做的词（要先有视频图片）", tid)
        return
    for w in words:
        SEC.pend_add([w], sid)
    name = "做「%s」" % s["name"]
    C.log("%s：%d 个词，AI 只做这一块（提示词只讲这一块，交回来只收这一块，检查也只看这一块）" % (name, len(words)), tid)
    res, saved, t0 = {}, [], time.time()
    if C.load_cfg().get("provider") == "relay":
        N, rnd = C.relay_size("fix")
        queue = list(words)
        while queue:
            pend, queue = queue[:N], queue[N:]
            chunk = list(pend)
            while pend:
                for part in R.ask_parts(tid, name, build_prompt(sid, pend, min(rnd, len(pend))), pend, min(rnd, len(pend))):
                    fx = [w for w in (C.RELAY.get("fixing") or []) if w in chunk and w not in pend]
                    got = PX.parse_multi(part, pend + fx)
                    if not got:
                        C.RELAY["hint"] = "交回的这个文件里没认出这一批的词（每个词要先写一行 @单词）"
                        continue
                    for w, (Pai, raw, svgs, errs) in got.items():
                        first = w in pend
                        if not first and w not in fx:
                            continue
                        good, tell, mine = accept(R, tid, sid, w, Pai, svgs, errs if not Pai else [])
                        k = int(((C.RELAY.get("verdict") or {}).get(w) or {}).get("try") or 0) + 1
                        C.log("  %s 的「%s」%s（第 %d 次）%s" % (w, s["name"], "过了" if good else "没过", k, ("：" + tell[:160]) if tell else ""), tid)
                        if good and w not in saved:
                            saved.append(w)
                        gave = C.relay_verdict(w, good, tell)
                        why = "做好了" if good else (tell or "没过") + ("（改了 %d 次还没过，先放着）" % k if gave else "")
                        C.relay_word(w, good, why)
                        res[w] = {"ok": good, "detail": why}
                        if first:
                            pend.remove(w)
                            R.progress(tid, processed=len(res), total=len(words))
                if C.RELAY.get("endReason") in ("newchat", "resize") and pend:
                    continue
                for w in pend:
                    res[w] = {"ok": False, "detail": "跳过了"}
                pend = []
        PX.relay_final(tid, name, res, t0)
    else:
        rounds = max(1, int(C.load_cfg().get("fixRounds", 3)))
        for w in words:
            R.check_stop()
            good, tell = False, ""
            for k in range(rounds):
                prompt = build_prompt(sid, [w], 1) + (("\n\n【上次交的没过，照这几条改】\n" + tell) if tell else "")
                rep = R.ask(tid, name if not k else "%s · 改第 %d 次" % (name, k), prompt, [w])
                got = PX.parse_multi(rep, [w])
                Pai, raw, svgs, errs = got.get(w) or (None, "", {}, ["没读到这个词"])
                good, tell, mine = accept(R, tid, sid, w, Pai, svgs, errs if not Pai else [])
                if good:
                    break
            res[w] = {"ok": good, "detail": "做好了" if good else tell}
            if good:
                saved.append(w)
            R.progress(tid, processed=len(res), total=len(words))
    C.gen_hist_add("pic", list(res), res, tid, name + " · " + C.provider_name(), t0)
    PX._UC["t"] = 0.0
    PX._commit(tid, saved, name)
