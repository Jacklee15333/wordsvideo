# -*- coding: utf-8 -*-
"""单词工作台 · 做视频画面（画面设置）
一个词出视频前要有“画面设置”：每个意思一幅会动的生活场景、例句的动画、意思怎么变过来的示意图……
以前是 Claude 一个词一个词手写的，这里交给网页 AI：
  按视频技能的 references/data-format.md、pictures.md 写一份 prefs（JSON），要用到的插图写成 SVG；
  程序检查（JSON 能读、用到的图都有、人物动作是现成的、不用表情图、SVG 能打开），
  这台电脑的出片环境装好了的话，再用视频技能“起草检查”（要“还要补：都齐了”）；没过就带着问题退回去改。
过了就存进：
  词库/画面设置/words/<词>.json + <词>.py（出片流水线读它）、art/<词>/*.svg、<词>ai_art.py（把插图拷进画图文件夹）、清单.tsv；
  词库/总表视频细节数据/词/<首字母>/<词>.json 的「画面」「插图」，索引.tsv 的「画面」列改成“细节数据有”。"""
import json, os, re, time, xml.etree.ElementTree as ET
from pathlib import Path
import core as C
import video as V

VR = "引擎/视频/references"
EXTRA = "词库/画面设置"
END = C.END


def _p(rel):
    return C.REPO / rel


def motions():
    t = _p("引擎/视频/scripts/poses.py").read_text(encoding="utf-8")
    seg = t[t.index("MOTIONS = {"):][:20000]
    # 只要会动的（cn-girl 这种没有动作的名字在出片时画不出来）
    return [n for n in re.findall(r"^\s+'([a-z][a-z0-9-]+)'\s*:", seg, re.M) if n.count("-") >= 2]


def scenes():
    return sorted(p.name for p in _p(VR + "/scenes").glob("*.svg"))


def _sections(md, keep):
    parts = re.split(r"(?m)^(?=## )", md)
    return "\n".join(p for p in parts if any(p.startswith("## " + k) for k in keep))


SKILL = "引擎/视频/SKILL.md"
KIT = "引擎/视频/references/kit-7A-U4"
EXAMPLE_WORD = "stranger"        # kit 里第八十五版刚补好、过了起草检查的词；画面设置的写法最全（partPics、icons、comboPic、distinguish、互动）
# SKILL.md「用户定下的规矩」里和画面有关的（配音、渲染、交付的不放）
PIC_RULES = {3, 4, 6, 13, 14, 15, 16, 17, 18, 21, 24, 28, 29, 34, 44, 46, 47, 48, 50, 51, 56, 57}


def skill_version():
    """视频技能的版本，比如 ("6.41.0", "第八十五版")。"""
    try:
        m = re.search(r"(?m)^当前 (\S+?)（(第[^）]+版)）", _p(SKILL).read_text(encoding="utf-8"))
        return (m.group(1), m.group(2)) if m else ("", "")
    except Exception:
        return ("", "")


def pic_rules():
    t = _p(SKILL).read_text(encoding="utf-8")
    a = t.find("## 用户定下的规矩")
    b = t.find("\n## ", a + 10)
    sec = t[a:b] if a >= 0 else ""
    items = re.split(r"(?m)^(?=\d+\. \*\*)", sec)
    keep = [x.strip() for x in items if re.match(r"(\d+)\. \*\*", x) and int(re.match(r"(\d+)", x).group(1)) in PIC_RULES]
    return "\n\n".join(keep)


_EX = {"key": None, "text": ""}
STUB = r"""import importlib.util, os
_s = importlib.util.spec_from_file_location("_real", os.path.join(os.environ["REALKIT"], "prefkit.py"))
_real = importlib.util.module_from_spec(_s); _s.loader.exec_module(_real)
for _k in dir(_real):
    if not _k.startswith("_"):
        globals()[_k] = getattr(_real, _k)
def actor(name, **kw):
    d = {"actor": name}; d.update(kw); return d
def walker(name, y, s, x0, x1, offset=0.0, z=3):
    return {"actor": name, "x": x0, "y": y - 0.47 * s, "s": s, "z": z, "walk": {"from": [x0, y - 0.47 * s], "to": [x1, y - 0.47 * s], "offset": offset}}
_real.actor = actor; _real.walker = walker
"""


def kit_example():
    """范例：视频技能 kit 里过了起草检查的一个词，跑一遍它的画面设置程序，人物换回 {"actor": 动作名} 的写法（和 AI 要交的一样）。
    技能更新了范例也跟着新。跑不出来就用 references/example-product（老一点，也有 partPics、icons、辨析）。"""
    import subprocess, sys as _sys, tempfile
    src = _p(KIT + "/words/%s.py" % EXAMPLE_WORD)
    key = (src.stat().st_mtime if src.exists() else 0)
    if _EX["key"] == key and _EX["text"]:
        return _EX["text"]
    text = ""
    try:
        with tempfile.TemporaryDirectory() as d:
            Path(d, "prefkit.py").write_text(STUB, encoding="utf-8")
            code = src.read_text(encoding="utf-8").replace("os.path.expanduser('~/kit')", repr(d))
            Path(d, "w.py").write_text(code, encoding="utf-8")
            os.makedirs(os.path.join(d, "art"), exist_ok=True)
            env = dict(os.environ, REALKIT=str(_p(KIT)), WART=os.path.join(d, "art"), PYTHONIOENCODING="utf-8")
            out = os.path.join(d, "out.json")
            r = subprocess.run([_sys.executable, os.path.join(d, "w.py"), out], env=env, capture_output=True, timeout=60,
                               creationflags=C.NOWIN)
            if r.returncode == 0 and os.path.exists(out):
                P = next(iter(json.loads(Path(out).read_text(encoding="utf-8")).values()))
                P = json.loads(json.dumps(P), parse_float=lambda f: round(float(f), 3))
                text = json.dumps(P, ensure_ascii=False, separators=(",", ":"))
    except Exception:
        text = ""
    if not text:
        ex = json.loads(_p(VR + "/example-product/prefs.json").read_text(encoding="utf-8"))
        text = json.dumps(ex, ensure_ascii=False, separators=(",", ":"))[:16000]
    _EX.update(key=key, text=text)
    return text


def docs():
    """给 AI 的视频技能材料（按仓库里最新的视频技能）：和画面有关的规矩、pictures.md 全文、kit 里过了检查的范例。"""
    pm = _p(VR + "/pictures.md").read_text(encoding="utf-8")
    pm = re.sub(r"(?ms)^## 二十一、.*?(?=^## |\Z)", "", pm)          # 每 5 个视频换画风：出片时程序自己转，不用写进画面设置
    return pic_rules(), pm, kit_example()


OUT = """【输出格式（程序按这个格式自动读，请严格照做）】
1. 一个代码块（第一行写 ```json），里面是这个词的画面设置：一个 JSON 对象，写法和上面的范例一样（style、board、pics、originPic、flow、extend…… 用得到的都写）。
2. 画里的人不要自己画，写成 {"actor": "动作名", "x": 0.3, "y": 0.6, "s": 0.9, "z": 3}，程序会换成会动的人。动作名只能用这些：%s。
3. 不许用表情图（"e": "🚗" 这种），东西都用写实插图："svg": "art/名字.svg"。下面这些现成的场景和东西可以直接用：%s。
4. 现成里没有的插图，你自己画成 SVG，每张一块，放在 JSON 代码块后面：
<<<SVG 名字.svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">……</svg>
>>>END
   插图要求：图画书风（黑色勾线、饱和平涂），画成现实生活里的样子；一张图不超过 12 KB。
5. 最后单独一行写：%s"""


def build_prompt(word, fix=None, todo=""):
    rules, pm, ex = docs()
    ver, ed = skill_version()
    rows = C.TABLE["words"].get(word) or [{}]
    mat = C.material(word) + ("\n  拆分：" + rows[0].get("拆分", "") if rows[0].get("拆分") else "") + \
        ("\n  意思怎么变过来（总表）：" + rows[0].get("组合 → 现在的含义", "")[:600].replace("\n", " / ") if rows[0].get("组合 → 现在的含义") else "")
    parts = ["【做画面】你在帮一位中学英语老师给单词 %s 做构词动画视频的“画面设置”。视频的讲解稿由程序从总表生成，你只管画面：每个意思一幅生活场景、例句和例句动画、各部分卡片的画（partPics）和小图标（icons）、拼起来那一格的画（comboPic）、同义词辨析、意思怎么一步步变过来的示意图。练习题不用写，程序会把出好的 7 道题放进去。" % word,
             "【这个词的总表材料】\n" + mat,
             "【视频技能 %s（%s）里和画面有关的规矩：每一条都要做到】\n" % (ver, ed) + rules,
             "【画面怎么画、画面设置怎么写（视频技能 %s 的 pictures.md 全文）】\n" % ver + pm,
             "【范例：%s 的画面设置（视频技能 %s kit 里过了起草检查的，写法和你要交的一样；里面的 art/… 插图是那个词自己画的）】\n" % (EXAMPLE_WORD, ed) + ex,
             OUT % ("、".join(motions()), "、".join("art/" + s for s in scenes()), END)]
    if todo and not fix:
        items = [x.strip() for x in re.split(r"[；;]", todo.split("：", 1)[-1]) if x.strip()]
        parts.insert(1, "【视频技能先给这个词起草了一遍，说画面设置里要写齐下面这些（每一条都要做到，程序会再起草检查一次）】\n- " + "\n- ".join(items))
    if fix:
        parts.insert(1, "【你上次写的没通过检查，请改好后把 JSON 和全部插图重新完整写一遍】\n问题：\n- " + "\n- ".join(fix[1]) +
                     "\n上次的 JSON：\n" + fix[0][:12000])
    return "\n\n".join(parts)


SVG_RE = re.compile(r"<<<SVG\s+([\w.\-]+\.svg)\s*\n(.*?)>>>END", re.S)

# ═══════════ v1.10.9：手动接力一份好几个词 ═══════════
OUT_MULTI = """【输出格式（程序按这个格式自动读，请严格照做）】
0. 一个词一段，按上面的顺序写：每段先单独一行写 @单词（比如 @%s），下面是这个词的全部内容；写完一个词再写下一个。
1. 每个词：一个代码块（第一行写 ```json），里面是这个词的画面设置：一个 JSON 对象，写法和上面的范例一样（style、board、pics、originPic、flow、extend…… 用得到的都写）。
2. 画里的人不要自己画，写成 {"actor": "动作名", "x": 0.3, "y": 0.6, "s": 0.9, "z": 3}，程序会换成会动的人。动作名只能用这些：%s。
3. 不许用表情图（"e": "🚗" 这种），东西都用写实插图："svg": "art/名字.svg"。下面这些现成的场景和东西可以直接用：%s。
4. 现成里没有的插图，你自己画成 SVG，每张一块，放在这个词的 JSON 代码块后面（别的词要用就再画一份，各词的插图分开放）：
<<<SVG 名字.svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">……</svg>
>>>END
   插图要求：图画书风（黑色勾线、饱和平涂），画成现实生活里的样子；一张图不超过 12 KB。
5. 每次上传的内容，最后单独一行写：%s"""


def _mat_short(word, budget):
    """一份好几个词时每个词的总表材料：词多就短一些，免得提示词太长贴不进去。"""
    rows = C.TABLE["words"].get(word) or [{}]
    m = C.material(word)
    m = m[:budget] + ("…" if len(m) > budget else "")
    if rows[0].get("拆分"):
        m += "\n  拆分：" + rows[0]["拆分"]
    if rows[0].get("组合 → 现在的含义"):
        m += "\n  意思怎么变过来（总表）：" + rows[0]["组合 → 现在的含义"][:max(150, budget // 3)].replace("\n", " / ")
    return m


# v1.12.0：交之前自己对一遍——最常漏的几条（一直放），加上最近起草检查最常说的“还要补”（单词工作台统计）
ALWAYS_CHECK = [
    "用到的每张插图（art/名字.svg）：要么在“现成的插图”里，要么在这次回复里画出来（写成 SVG 块）；只写名字不画，程序找不到，整个词作废",
    "同义词辨析：每张卡都要配一幅画（prefs.distinguish.pics 里每个词写一幅），还要写辨析的话（key / items / logic / tip）",
    "同一个人物动作、表情，一个词里只用一次：每幅画换一个动作和表情（动作名只能用列出来的）",
    "读音拆分：要一块一块念的，在 prefs 写 sylIpa（每一块的音标），和拆分一一对上",
    "场景背景要画细：生活场景至少 150 个图形，不能只有几块色块",
]


def _fail_key(it):
    a, _, b = it.partition("：")
    b = re.sub(r"[A-Za-z][A-Za-z0-9'’\-\._/]*", "X", b)
    b = re.sub(r"\d+", "N", b)
    return (a[:30] + "：" + b[:14]) if b else a[:40]


def common_fails(n=6):
    """最近最常没过的地方：[(这一类, 几次, 一个例子)]。"""
    items = []
    try:
        L = json.loads(C.FAIL_LOG.read_text(encoding="utf-8")) if C.FAIL_LOG.exists() else []
    except Exception:
        L = []
    for x in L[-300:]:
        items += _items(x.get("todo", "")) or [x.get("todo", "")]
    for line in todo_all().values():
        items += _items(line)
    cnt, ex = {}, {}
    for it in items:
        it = (it or "").strip()
        if not it or it.startswith("你点了"):
            continue
        k = _fail_key(it)
        cnt[k] = cnt.get(k, 0) + 1
        ex.setdefault(k, it)
    return [(k, cnt[k], ex[k]) for k in sorted(cnt, key=lambda k: -cnt[k])[:n] if cnt[k] >= 2]


def self_check():
    """提示词里的一段：交之前每个词自己对一遍。"""
    out = ["【交之前每个词自己对一遍（这几条最容易没过起草检查；交上去软件马上检查，没过的要回来改）】"]
    out += ["%d. %s" % (i + 1, t) for i, t in enumerate(ALWAYS_CHECK)]
    top = common_fails()
    if top:
        out.append("最近起草检查最常说的“还要补”（单词工作台统计的，后面是次数）：")
        out += ["- %s（%d 次）" % (e[:150], c) for k, c, e in top]
    return "\n".join(out)


def relay_final(tid, kind, allres, t0):
    """v1.13.0：这一轮（这个任务）做完了：一共几个、做好几个、没做成的和原因——黄框没了以后，「这一步的进度」里还看得到。"""
    if not allres:
        return
    bad = [[w, (r.get("detail") or "没做成")[:120]] for w, r in allres.items() if not r.get("ok")]
    C.RELAY["final"] = {"t": time.time(), "t0": t0, "tid": tid, "kind": kind, "n": len(allres), "ok": len(allres) - len(bad), "bad": bad}
    C.log("━━ 本轮任务完成（%s）：一共 %d 个词，做好 %d 个，没做成 %d 个%s ━━" % (
        kind, len(allres), len(allres) - len(bad), len(bad), ("：" + "、".join(w for w, _ in bad[:20])) if bad else ""), tid)


def build_prompt_multi(words, rnd):
    """手动接力：一份好几个词的画面提示词。规矩、pictures.md、范例只放一次，每个词一段材料。"""
    rules, pm, ex = docs()
    ver, ed = skill_version()
    n = len(words)
    budget = max(250, min(1200, 120000 // max(1, n)))
    head = ("【做画面 · 这一批 %d 个词】你在帮一位中学英语老师给下面 %d 个单词各做一份构词动画视频的“画面设置”。视频的讲解稿由程序从总表生成，"
            "你只管画面：每个意思一幅生活场景、例句和例句动画、各部分卡片的画（partPics）和小图标（icons）、拼起来那一格的画（comboPic）、"
            "同义词辨析、意思怎么一步步变过来的示意图。练习题不用写，程序会把出好的 7 道题放进去。\n"
            "按顺序一个接一个写：每写完 %d 个词就上传一次（怎么传看最后），中间不用在聊天里汇报，接着写下一个；这一批全部传完再汇报一次。" % (n, n, rnd))
    return "\n\n".join([
        head,
        "【这一批的词（按这个顺序做）】\n" + "\n".join("%d. %s" % (i + 1, w) for i, w in enumerate(words)),
        self_check(),
        "【每个词的总表材料】\n" + "\n\n".join("@%s\n%s" % (w, _mat_short(w, budget)) for w in words),
        "【视频技能 %s（%s）里和画面有关的规矩：每个词每一条都要做到】\n" % (ver, ed) + rules,
        "【画面怎么画、画面设置怎么写（视频技能 %s 的 pictures.md 全文）】\n" % ver + pm,
        "【范例：%s 的画面设置（视频技能 %s kit 里过了起草检查的，写法和你要交的一样；里面的 art/… 插图是那个词自己画的）】\n" % (EXAMPLE_WORD, ed) + ex,
        OUT_MULTI % (words[0], "、".join(motions()), "、".join("art/" + x for x in scenes()), END)])


_MARK = re.compile(r"^[ \t>*#_]*[@＠]\s*([A-Za-z][A-Za-z0-9'’\- .]*?)\s*[*_]*\s*$", re.M)


def parse_multi(text, words):
    """一轮交回的原文 → {单词: (P, raw, svgs, errs)}：按 @单词 那一行分段，每段照一个词读。没有 @ 行、只要一个词时整段算这个词。"""
    t = (text or "").replace("\r", "")
    low = {w.lower(): w for w in words}
    marks = [(m.start(), m.end(), low.get(m.group(1).strip().lower())) for m in _MARK.finditer(t)]
    marks = [x for x in marks if x[2]]
    out = {}
    if not marks:
        if len(words) == 1:
            out[words[0]] = parse(t.replace(END, ""))
        return out
    for k, (a, b, w) in enumerate(marks):
        sec = t[b:marks[k + 1][0] if k + 1 < len(marks) else len(t)].replace(END, "")
        if w not in out or len(sec) > 200:
            out[w] = parse(sec)
    return out


def _accept(R, tid, w, P, svgs, errs, info=None):
    """手动接力交回的一个词：能用（格式对、该有的都有）就存下；起草检查还想补的记一句。返回 (做好了吗, 一句话, 问题)。"""
    errs = errs or check(w, P, svgs)
    if errs:
        return False, short_why(errs), errs
    C.relay_stage("%s：起草检查（在 WSL 里）…" % w)
    R.stage = "%s：起草检查（在 WSL 里）" % w
    st, line = wsl_draft_safe(w, P, svgs)
    if info is not None:
        info.update(st=st, line=line)
    left = line if st == "todo" else ""
    save(w, P, svgs, st == "ok")
    todo_note(w, left)
    if st in ("env", None):
        C.log("  %s 的起草检查没跑成（%s）：本机检查过了，先存下，出片时再起草检查" % (w, (line or "")[:160]), tid)
    return True, ("出片前还要补 %d 处" % ntodo(left)) if left else "", []


def do_pics_relay(R, tid, total, only):
    """手动接力做画面：选的词按设置分成一份一份（一份 N 个），网页 AI 一轮一轮交回，收到一轮做一轮。"""
    N, rnd = C.relay_size("pic")
    todo = pick(total or 10 ** 6, only)
    if not todo:
        C.log("没有要做画面的词了（要先有题目；做不出来的在“画面没做成”里）", tid)
        return
    nb = (len(todo) + N - 1) // N
    C.log("画面（手动接力）：一共 %d 个词，一份 %d 个，分 %d 份；网页 AI 每写完 %d 个上传一次" % (len(todo), N, nb, rnd), tid)
    done, batch, queue, k = 0, [], list(todo), 0
    allres, t_all = {}, time.time()
    while queue:                    # v1.11.2：每一份开始时按现在的设置分（黄框里改了，下一份就按新的）
        N, rnd = C.relay_size("pic")
        pend, queue = queue[:N], queue[N:]
        k += 1
        nb = k + (len(queue) + N - 1) // N
        chunk, res, t0 = list(pend), {}, time.time()
        C.log("第 %d 份（共 %d 份）：%s … %s，%d 个词" % (k, nb, pend[0], pend[-1], len(pend)), tid)
        while pend:
            C.RELAY_QLEFT[0] = len(queue)
            for part in R.ask_parts(tid, "做画面", build_prompt_multi(pend, min(rnd, len(pend))), pend, min(rnd, len(pend))):
                fx = [w for w in (C.RELAY.get("fixing") or []) if w in chunk and w not in pend]   # v1.12.0：没过、网页 AI 在改的
                got = parse_multi(part, pend + fx)   # v1.11.2：以前这里用 res，把这一批前几个词的结果冲掉了（生成历史里算成没做成）
                if not got:
                    C.RELAY["hint"] = "交回的这个文件里没认出这一批还没做的词（每个词要先写一行 @单词）"
                    continue
                for w, (P, raw, svgs, errs) in got.items():
                    first = w in pend
                    if not first and w not in fx:
                        continue
                    _DONE.add(w)
                    info = {}
                    ok, why, errs2 = _accept(R, tid, w, P, svgs, errs, info)
                    st, line = info.get("st"), info.get("line") or ""
                    good = ok and st != "todo"            # v1.12.0：起草检查说还要补的，不算做好——告诉网页 AI 马上改
                    k = int(((C.RELAY.get("verdict") or {}).get(w) or {}).get("try") or 0) + 1
                    if ok and w not in batch:
                        batch.append(w)
                    if good:
                        C.log("  %s 的画面做好了%s" % (w, "（改了 %d 次）" % (k - 1) if k > 1 else ""), tid)
                    elif ok:
                        C.log("  %s 存下了，起草检查说还要补 %d 处（第 %d 次）：%s" % (w, ntodo(line), k, line[:160]), tid)
                    else:
                        C.x("INSERT OR REPLACE INTO picfail(word, errors, ts) VALUES(?,?,?)", (w, json.dumps(errs2, ensure_ascii=False), C.now()))
                        C.log("  %s 的画面没做成（第 %d 次）：%s" % (w, k, why), tid)
                    gave = C.relay_verdict(w, good, line if ok else "；".join(errs2 or []) or why)
                    if not good and w in (C.RELAY.get("fixing") or []):
                        why = (why or "没过") + "，网页 AI 在改"
                    elif gave and ok:
                        later_op({"op": "add", "words": [w]})     # 改够次数了还没过：先攒着，以后一起补
                        why = (why or "") + "（改了 %d 次，先攒着）" % k
                    C.relay_word(w, good, why or ("做好了" if good else "没做成"))
                    res[w] = {"ok": good, "detail": why or ("做好了" if good else "没做成")}
                    if first:
                        pend.remove(w)
                        done += 1
                        R.progress(tid, processed=done, total=len(todo))
                    if len(batch) >= 5:
                        _commit(tid, batch)
                        batch = []
            why = C.RELAY.get("endReason")
            fx = [w for w in (C.RELAY.get("fixing") or []) if w in chunk and w not in pend]
            if why in ("newchat", "resize") and fx:             # 在改的词也放进新的提示词
                pend += fx
            elif why == "skiprest" and fx:
                later_op({"op": "add", "words": fx})
            if pend and why in ("newchat", "resize"):
                N2, rnd = C.relay_size("pic")
                if len(pend) > N2:                  # 一批改小了：多出来的放回去，排到下一份
                    queue, pend = pend[N2:] + queue, pend[:N2]
                elif len(pend) < N2 and queue:      # v1.11.3：一批改大了，后面排着的拿进来
                    more, queue = queue[:N2 - len(pend)], queue[N2 - len(pend):]
                    pend += more
                    chunk += more
                nb = k + (len(queue) + N2 - 1) // N2
                C.log("  剩下的 %d 个另开对话：出一份新的提示词" % len(pend), tid)
                continue
            for w in pend:                      # 你点了「剩下的先跳过」
                C.x("INSERT OR REPLACE INTO picfail(word, errors, ts) VALUES(?,?,?)",
                    (w, json.dumps(["你点了「剩下的先跳过」"], ensure_ascii=False), C.now()))
                C.relay_word(w, False, "跳过了")
                res[w] = {"ok": False, "detail": "你点了「剩下的先跳过」"}
                done += 1
            if pend:
                C.log("  剩下的 %d 个先跳过了：%s" % (len(pend), "、".join(pend[:20])), tid)
            pend = []
        C.gen_hist_add("pic", [w for w in chunk if w in res], res, tid, "手动接力 · 第 %d 批（共 %d 批）" % (k, nb), t0)
        allres.update(res)
        _commit(tid, batch)
        batch = []
    _commit(tid, batch)
    relay_final(tid, "做画面", allres, t_all)


def parse(reply):
    t = (reply or "").replace("\r", "")
    svgs = {n: b.strip() for n, b in SVG_RE.findall(t)}
    body = SVG_RE.sub("", t)
    m = re.search(r"```(?:json)?\s*\n(\{.*?\})\s*```", body, re.S)
    raw = m.group(1) if m else ""
    if not raw:
        a, b = body.find("{"), body.rfind("}")
        raw = body[a:b + 1] if a >= 0 and b > a else ""
    try:
        P = json.loads(raw) if raw else None
    except Exception as e:
        return None, raw, svgs, ["JSON 读不出来：%s" % str(e)[:120]]
    if isinstance(P, dict) and len(P) == 1 and isinstance(next(iter(P.values())), dict) and "pics" in next(iter(P.values())):
        P = next(iter(P.values()))                     # 写成了 {"单词": {...}}
    return P, raw, svgs, []


def check(word, P, svgs):
    errs = []
    if not isinstance(P, dict):
        return ["没有画面设置的 JSON"]
    pics = P.get("pics")
    if not isinstance(pics, list) or not pics:
        errs.append("pics（每个意思一幅画）没有写")
    else:
        for i, pc in enumerate(pics):
            if not isinstance(pc, dict) or not pc.get("text"):
                errs.append("pics 第 %d 幅缺 text（这幅画讲的意思）" % (i + 1))
            elif not (pc.get("items") or pc.get("img")):
                errs.append("pics 第 %d 幅（%s）没有画东西（items）" % (i + 1, pc.get("text")))
    if not isinstance(P.get("flow"), list) or not P.get("flow"):
        errs.append("flow（意思怎么一步步变过来）没有写")
    s = json.dumps(P, ensure_ascii=False)
    if re.search(r'"e"\s*:', s):
        errs.append("用了表情图（\"e\": …），要换成写实插图 svg")
    have = set(scenes()) | set(svgs)
    miss = sorted({n for n in re.findall(r"art/([\w.\-]+\.svg)", s)} - have)
    if miss:
        errs.append("用到的插图没有：%s（现成的里没有，要画成 SVG 块）" % "、".join(miss[:10]))
    mot = set(motions())
    bad = sorted({a for a in re.findall(r'"actor"\s*:\s*"([^"]+)"', s)} - mot)
    if bad:
        errs.append("人物动作名不对：%s（只能用给出的那些）" % "、".join(bad))
    for n, b in svgs.items():
        if len(b) > 40000:
            errs.append("%s 太大了（%d 字），要简单一些" % (n, len(b)))
            continue
        try:
            root = ET.fromstring(b)
            if not root.tag.endswith("svg"):
                errs.append("%s 不是 SVG" % n)
        except Exception as e:
            errs.append("%s 打不开（SVG 写错了：%s）" % (n, str(e)[:80]))
    return errs


WORD_PY = '''# AI 生成的画面设置（单词工作台）：读同名的 .json，把 {"actor": 动作名} 换成会动的人，交给视频技能
import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/%(folder)s/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE, '%(folder)s.json'), encoding='utf-8'))
def conv(o):
    if isinstance(o, dict):
        if isinstance(o.get('actor'), str):      # 只有值是动作名的才是人；演示词正好叫 actor（值是一幅画）照常往下走
            kw = {k: v for k, v in o.items() if k != 'actor'}
            return actor(o['actor'], **kw)
        return {k: conv(v) for k, v in o.items()}
    if isinstance(o, list):
        return [conv(v) for v in o]
    return o
json.dump({%(word)r: conv(P)}, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok')
'''
ART_PY = '''# AI 画的插图（单词工作台）：把 art/%(folder)s/ 里的 svg 拷进画图文件夹
import os, sys, glob, shutil
src = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'art', '%(folder)s')
for f in glob.glob(os.path.join(src, '*.svg')):
    shutil.copy(f, sys.argv[1])
print('ok')
'''


OLD_CONV = "        if 'actor' in o:\n"
NEW_CONV = "        if isinstance(o.get('actor'), str):      # 只有值是动作名的才是人；演示词正好叫 actor（值是一幅画）照常往下走\n"


def fix_word_pys():
    """v1.11.4：以前存的 words/<词>.py 把所有带 actor 的都当成人，演示词正好叫 actor 时出错（unhashable type: 'dict'）。
    旧的这一行换成新的；起草检查、同步到 WSL 以前都跑一遍，改过的跟着词库提交。返回改了几个。"""
    n = 0
    d = C.REPO / EXTRA / "words"
    if not d.is_dir():
        return 0
    for f in d.glob("*.py"):
        try:
            t = f.read_text(encoding="utf-8")
        except Exception:
            continue
        if t.startswith("# AI 生成的画面设置") and OLD_CONV in t.replace("\r\n", "\n"):
            f.write_text(t.replace("\r\n", "\n").replace(OLD_CONV, NEW_CONV), encoding="utf-8")
            n += 1
    return n


def save(word, P, svgs, checked):
    f = V.folder_of(word)
    base = C.REPO / EXTRA
    with C.REPO_LOCK:
        (base / "words").mkdir(parents=True, exist_ok=True)
        art = base / "art" / f
        if art.exists():
            C.rmtree(art)
        art.mkdir(parents=True)
        for n, b in svgs.items():
            (art / n).write_text(b + "\n", encoding="utf-8")
        lx = lianxi_qs(word)
        (base / "words" / (f + ".json")).write_text(json.dumps(dict(P, lianxi={"qs": lx}) if lx else P, ensure_ascii=False, indent=1),
                                                     encoding="utf-8")
        (base / "words" / (f + ".py")).write_text(WORD_PY % {"folder": f, "word": word}, encoding="utf-8")
        (base / (f + "ai_art.py")).write_text(ART_PY % {"folder": f}, encoding="utf-8")
        lst = base / "清单.tsv"
        lines = lst.read_text(encoding="utf-8").splitlines() if lst.exists() else ["# 画面设置清单"]
        lines = [l for l in lines if not (l.split("\t")[1:2] == [f])]
        lines.append("%02d\t%s\t%sai\tAI 生成 %s" % (len([l for l in lines if not l.startswith("#")]) + 1, f, f, time.strftime("%Y-%m-%d")))
        lst.write_text("\n".join(lines) + "\n", encoding="utf-8")
        # 总表视频细节数据：画面、插图，索引的「画面」列
        head, rows = C.read_index()
        rel = next((r[6] for r in rows if r[2] == word and len(r) > 6 and r[6]), "")
        if not rel:
            slug = word.replace(" ", "_").replace("/", "_")
            slug = slug + "_" if slug.lower() in C.RESERVED else slug
            rel = "词/%s/%s.json" % ((slug[:1].lower() if slug[:1].isalpha() else "_"), slug)
        p = C.REPO / C.D / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        rec = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"单词": word, "题目": None}
        rec.update({"画面": P, "插图": [f + "ai"], "画面生成": time.strftime("%Y-%m-%d") + " " + C.provider_name(),
                    "检查": "还要补：都齐了（起草检查）" if checked else "本机检查通过，出片时再起草检查"})
        p.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        for r in rows:
            if r[2] == word:
                while len(r) < 7:
                    r.append("")
                r[5] = "细节数据有"
                r[6] = r[6] or rel
        C.write_index(head, rows)
    _UC["t"] = 0.0
    C.x("DELETE FROM picfail WHERE word=?", (word,))
    try:                                   # v1.9.9：画面里的图也拷到成果文件夹（画面\<单词>\）
        import results
        results.copy_ai_pics(word)
    except Exception as e:
        C.log("画面的图没拷到成果文件夹（%s）：词库里的照常存好了" % str(e)[:120])


def _rec_path(word):
    _, rows = C.read_index()
    rel = next((r[6] for r in rows if r[2] == word and len(r) > 6 and r[6]), "")
    if not rel:
        slug = word.replace(" ", "_").replace("/", "_")
        slug = slug + "_" if slug.lower() in C.RESERVED else slug
        rel = "词/%s/%s.json" % ((slug[:1].lower() if slug[:1].isalpha() else "_"), slug)
    return C.REPO / C.D / rel


def _rec(word):
    p = _rec_path(word)
    try:
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    except Exception:
        return {}


def lianxi_qs(word):
    """这个词出好的 7 道题（细节数据「题目」那几格）→ 视频技能 prefs.lianxi 的写法（照 wordfilm.js 读总表题目格的方法）。
    这些题还只在细节数据里、总表里没有：不放进画面设置的话，起草检查永远说“练习题还要补”，出片时视频里也是自动凑的题。"""
    t = (_rec(word) or {}).get("题目") or {}
    if not t:
        return []
    L = C.lianxi()
    D = L.parse_daan(t.get("答案", ""))
    out = []
    for k, col in enumerate(L.COLS, 1):
        if not t.get(col):
            continue
        q = L.parse(t[col])
        q.pop("bad", None)
        if not q["opts"] and "；" in str(q.get("ans", "")):
            q["ans"] = [x.strip() for x in q["ans"].split("；")]
        a = D.get(k)
        if a:
            q["ans"] = a[0] if q["opts"] else ([x.strip() for x in a[0].split("；")] if "；" in a[0] else a[0])
            q["why"] = a[1] or q["why"]
        if q.get("type") and q.get("ans"):
            out.append(q)
    return out


def refresh_lianxi(word):
    """题目重出、改过以后，把画面设置里的练习题也换成新的。"""
    pj = C.REPO / EXTRA / "words" / (V.folder_of(word) + ".json")
    if not pj.exists():
        return
    with C.REPO_LOCK:
        P = json.loads(pj.read_text(encoding="utf-8"))
        lx = lianxi_qs(word)
        if lx:
            P["lianxi"] = {"qs": lx}
        else:
            P.pop("lianxi", None)
        pj.write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")


_ENV = {"t": 0.0, "ready": False}


def env_ready():
    """这台电脑的出片环境装好了没（WSL 里有视频技能、声音模型、ffmpeg）；10 分钟内不重复问。"""
    if not V.has_wsl():
        return False
    if time.time() - _ENV["t"] > 600:
        try:
            _ENV.update(t=time.time(), ready=bool(V.env_status().get("ready")))
        except Exception:
            _ENV.update(t=time.time(), ready=False)
    return _ENV["ready"]


DRAFT_SH = r"""set -o pipefail; . ~/.wordfilm-local.env 2>/dev/null
T="${TABLE:-}"; [ -f "$T" ] || T=@TABLE@
SY=""; [ -f "${SYL:-}" ] && SY="$SYL"
S=~/skills/word-construction-video; W=~/wordfilm-work; A="$W/@F@/art"; WK=/tmp/wv-draft-@F@; LOG=/tmp/wv-draft-@F@.log
say() { echo "WVRESULT:$*"; }
echo "WVVER:$(grep -m1 '^当前' "$S/SKILL.md" 2>/dev/null | sed 's/（.*//; s/^当前 *//')"
[ -f "$S/scripts/run.py" ] || { say "检查没跑成：WSL 里没有视频技能（$S），先在「视频」页同步引擎"; exit 0; }
[ -f "$T" ] || { say "检查没跑成：找不到总表（$T）"; exit 0; }
mkdir -p "$W" ~/kit-extra
@MAKE@
rm -rf "$WK/@SAFE@"
cd "$S/scripts" && timeout 600 python3 run.py --table "$T" ${SY:+--syl "$SY"} --words @W@ --number 1 --out /tmp/wv-draft --edits "$E" \
  --edition brief --draft-only --no-preview --work "$WK" > "$LOG" 2>&1
line=$(grep -a '还要补' "$LOG" | tail -1 | sed 's/^ *//')
if [ -n "$line" ]; then say "$line"; else say "检查没跑成：起草没出结果：$(tail -3 "$LOG" | tr '\n' ' ')"; fi
"""
MAKE_FULL = r"""cp -r @SRC@/. ~/kit-extra/ && find ~/kit-extra -name '*.py' -exec sed -i 's/\r$//' {} +
rm -rf "$A"; mkdir -p "$A"; cp "$S/references/scenes/"*.svg "$A/" 2>/dev/null
(cd "$S/scripts" && python3 poses.py "$A" --motion) >/dev/null 2>&1
E="$W/edits_@F@.json"; ERR=/tmp/wv-art-@F@.err
python3 ~/kit-extra/@F@ai_art.py "$A" >/dev/null 2>"$ERR" && python3 ~/kit-extra/words/@F@.py "$E" >/dev/null 2>>"$ERR" \
  || { say "画面设置的程序跑不起来：$(tail -3 "$ERR" | tr '\n' ' ')"; exit 0; }"""
MAKE_PRE = 'E="$W/pre_@F@.json"; printf \'%s\' @EDITS@ > "$E"'
ENV_ERR = ("No such file", "ModuleNotFoundError", "No module named", "ImportError", "Permission denied", "command not found")


def wsl_draft(word, pre=False):
    """在 WSL 里用视频技能起草这个词（只起草、不配音不渲染，几秒钟），返回 (结果, 那一行)：
    "ok"＝还要补：都齐了；"todo"＝还要补别的（交给 AI 改）；"env"＝检查本身没跑成（不是 AI 的问题）；None＝出片环境没装好、跳过。
    pre=True：还没有画面设置，先起草一遍，看这个词要画什么（放进第一次的提示词）。"""
    if not env_ready():
        return None, ""
    try:
        fix_word_pys()
    except Exception:
        pass
    f = V.folder_of(word)
    table = V.to_wsl(C.REPO / C.STATE["xlsx"]) if C.STATE.get("xlsx") else ""
    if pre:
        lx = lianxi_qs(word)
        edits = json.dumps({word: {"lianxi": {"qs": lx}} if lx else {"_空": True}}, ensure_ascii=False)
        make = MAKE_PRE.replace("@EDITS@", V.q(edits))
    else:
        make = MAKE_FULL.replace("@SRC@", V.q(V.to_wsl(C.REPO / EXTRA)))
    sh = DRAFT_SH.replace("@MAKE@", make)
    for k, v in (("@TABLE@", V.q(table)), ("@F@", f), ("@W@", V.q(word)),
                 ("@SAFE@", re.sub(r'[\\/:*?"<>|\s]+', "_", word).strip("._") or "word")):
        sh = sh.replace(k, v)
    rc, t = V.wsl(sh, 900)
    wv = next((l.split("WVVER:", 1)[1].strip() for l in t.splitlines() if "WVVER:" in l), "")
    rv = skill_version()[0]
    if wv and rv and wv != rv and not _ENV.get("warned"):
        _ENV["warned"] = True
        C.log("⚠ WSL 里的视频技能是 %s，仓库里是 %s：起草检查按的是旧版。到「视频」页点同步引擎（没在出片时点）" % (wv, rv))
    if rc == 124:
        return "env", "起草检查超时了"
    res = [l.split("WVRESULT:", 1)[1].strip() for l in t.splitlines() if "WVRESULT:" in l]
    line = res[-1] if res else ""
    if not line:
        return "env", "WSL 没有回应（%s）：%s" % (rc, " ".join(t.split())[-160:])
    if line.startswith("还要补"):
        rest = line.split("：", 1)[1] if "：" in line else line
        rest = re.sub(r"练习题 lianxi（[^）]*）[；;]?", "", rest).strip("；; ")       # 练习题归出题那一步管，画面改不了
        if not rest or "都齐了" in rest:
            return "ok", "还要补：都齐了"
        return "todo", "还要补：" + rest
    if line.startswith("画面设置的程序跑不起来"):
        return ("env" if any(k in line for k in ENV_ERR) else "todo"), line
    return "env", line


def draft_todo(word):
    """还没有画面设置时先起草一遍：这个词要画齐哪些（放进第一次的提示词，少退回几次）。"""
    try:
        st, line = wsl_draft(word, pre=True)
        return line if st == "todo" else ""
    except Exception:
        return ""


def pick(n, only=None):
    import video as V2
    pw = V2.pic_words()
    fail = {r["word"] for r in C.q("SELECT word FROM picfail")}
    _, rows = C.read_index()
    out = []
    for r in rows:
        w = r[2]
        if w in out or r[4] not in ("细节数据有", "总表有"):
            continue
        if only is not None:
            if w not in only or w in _DONE:
                continue
            if V2.folder_of(w) in pw and not (_unchecked(w) and env_ready()):
                continue                   # 已经有画面、也过了起草检查（或者这台电脑查不了）
        elif w in fail or V2.folder_of(w) in pw:
            continue
        out.append(w)
        if len(out) >= n:
            break
    return out


_DONE = set()      # 这个任务里已经做过的词（做指定的词时不再挑它）


def _unchecked(word):
    """词库/画面设置 里存着、还没过起草检查的画面（上次检查没跑成、检查中途停了）：返回 (P, svgs)，否则 None。"""
    f = V.folder_of(word)
    base = C.REPO / EXTRA
    pj = base / "words" / (f + ".json")
    if not pj.exists() or "都齐了" in str((_rec(word) or {}).get("检查", "")):
        return None
    try:
        P = json.loads(pj.read_text(encoding="utf-8"))
    except Exception:
        return None
    P.pop("lianxi", None)
    art = base / "art" / f
    svgs = {x.name: x.read_text(encoding="utf-8").strip() for x in art.glob("*.svg")} if art.exists() else {}
    return P, svgs


def _try(R, tid, w, rounds, force=False):
    """做一个词的画面。返回 (做好了吗, 最后的问题)。
    存着还没过检查的画面先拿去起草检查（不用问 AI）；没有就先起草一遍看要画什么，再问 AI；没过带着问题退回去改。
    起草检查本身没跑成（WSL、文件的问题）不算 AI 的错：本机检查过了就先存下，出片时再起草检查。
    中途停下：临时存的、没过检查的画面清掉，不留下“看着做好了”的半成品。"""
    temp, fix, old = False, None, None
    try:
        old = _unchecked(w)
        if old:
            P, svgs = old
            errs = check(w, P, svgs)
            if not errs:
                st, line = wsl_draft_safe(w, P, svgs)
                temp = True
                if st == "ok":
                    save(w, P, svgs, True)
                    C.log("  %s 存着的画面过了起草检查" % w, tid)
                    return True, []
                if st in ("env", None):
                    C.log("  %s 的起草检查没跑成（%s）：画面先照旧，出片时再起草检查" % (w, line[:160]), tid)
                    save(w, P, svgs, False)
                    return True, []
                if st == "todo" and not force:          # v1.11.1 补画面（force）：带着“还要补”交给 AI 改
                    save(w, P, svgs, False)
                    todo_note(w, line)
                    C.log("  %s 存着的画面能用，留着（出片前还要补 %d 处：%s）" % (w, ntodo(line), line[:160]), tid)
                    return True, []
                errs = ["视频技能起草检查没过：" + line]
            fix = (json.dumps(P, ensure_ascii=False), errs)
            C.log("  %s 存着的画面没过：%s；交给 AI 改" % (w, "；".join(errs)[:200]), tid)
        R.stage = "%s：先起草一遍，看要画什么（在 WSL 里，几秒到一两分钟）" % w
        todo = "" if fix else draft_todo(w)
        if todo:
            C.log("  %s 先起草了一遍：要画齐的已经写进提示词" % w, tid)
        errs = []
        for rnd in range(rounds + 1):
            rep = R.ask(tid, "做画面" if not (rnd or old) else "画面改第 %d 次" % (rnd + (1 if old else 0)), build_prompt(w, fix, todo), [w])
            P, raw, svgs, errs = parse(rep)
            if old and force:                        # 补画面：没重画的插图用上次的
                svgs = dict(old[1], **(svgs or {}))
            C.relay_stage("检查画面设置、插图…")
            errs = errs or check(w, P, svgs)
            checked, left = False, ""
            if not errs:
                C.relay_stage("起草检查：在 WSL 里用视频技能画一遍（几秒钟）…")
                R.stage = "%s：起草检查（在 WSL 里）" % w
                st, line = wsl_draft_safe(w, P, svgs)
                temp = True
                if st == "ok":
                    checked = True
                elif st == "todo":
                    left = line
                    if rnd < rounds:              # 网页镜像、接口 AI 还能自己改（不用你动手）；最后一轮能用就存下
                        errs = ["视频技能起草检查没过：" + line]
                elif st == "env":
                    C.log("  %s 的起草检查没跑成（%s）：这不是 AI 的问题，本机检查过了就先存下，出片时再起草检查" % (w, line[:160]), tid)
            if not errs:
                save(w, P, svgs, checked)
                temp = False
                todo_note(w, left)
                if left:
                    C.log("  %s 的画面存下了：能用（起草检查说出片前还要补 %d 处：%s）" % (w, ntodo(left), left[:160]), tid)
                C.relay_result(True, "做好了" + ("（出片前还要补 %d 处）" % ntodo(left) if left else ""))
                return True, []
            C.relay_result(False, short_why(errs))
            fix = (raw or json.dumps(P or {}, ensure_ascii=False), errs)
            C.log("  %s 的画面没过：%s" % (w, "；".join(errs)[:200]), tid)
        return False, errs
    except BaseException:
        if temp and old and force:                   # 补画面中途停下：上次的画面放回去，不删
            save(w, old[0], old[1], False)
        elif temp:
            unsave(w)
            C.log("  %s 停下了：临时存的画面（还没过检查）清掉了" % w, tid)
        raise


def do_pics(R, tid, p):
    """任务：给有题目、还没有画面的词做画面。R 是 core.RUNNER。"""
    total = int(p.get("count") or 0)
    only = set(p.get("words") or []) or None
    sk = p.get("skipped") or {}                          # v1.10.0：开始时跳过的，记一笔汇报
    for k, why in (("pic", "已经有画面，跳过 %d 个（不重做）：%s"), ("noq", "还没有题目，跳过 %d 个（先到「出题」出题）：%s")):
        if sk.get(k):
            C.log(why % (len(sk[k]), "、".join(sk[k][:40]) + ("…" if len(sk[k]) > 40 else "")), tid)
    if only:
        C.x("DELETE FROM picfail WHERE word IN (%s)" % ",".join("?" * len(only)), list(only))
    _DONE.clear()
    _ENV.update(t=0.0, warned=False)
    ver, ed = skill_version()
    C.log("画面按视频技能 %s（%s）做：和画面有关的规矩、pictures.md 全文、kit 里 %s 的画面设置当范例" % (ver, ed, EXAMPLE_WORD), tid)
    if p.get("fix"):                                      # v1.11.1：补画面
        return do_pics_fix(R, tid, p)
    if C.load_cfg().get("provider") == "relay":           # v1.10.9：一份好几个词，一轮一轮交回
        return do_pics_relay(R, tid, total, only)
    done = 0
    batch = []
    hist, t0h = {}, time.time()
    # v1.10.6：手动接力每改一轮都要你再粘贴一次：不来回改——能用就存下，不能用就记“没做成”、做下一个
    rounds = 0 if C.load_cfg().get("provider") == "relay" else int(C.load_cfg().get("fixRounds", 3))
    while True:
        R.check_stop()
        if not C.in_window() and C.load_cfg().get("provider") != "relay":
            raise C.Stopped("window")
        if total and done >= total:
            break
        if not batch:
            C.sync()
        ws = pick(1, only)
        if not ws:
            C.log("没有要做画面的词了（要先有题目；做不出来的在“画面没做成”里）", tid)
            break
        w = ws[0]
        _DONE.add(w)
        ok, errs = _try(R, tid, w, rounds)
        hist[w] = {"ok": ok, "detail": "" if ok else short_why(errs)}
        if ok:
            batch.append(w)
            C.log("  %s 的画面做好了" % w, tid)
        else:
            unsave(w)
            C.x("INSERT OR REPLACE INTO picfail(word, errors, ts) VALUES(?,?,?)", (w, json.dumps(errs, ensure_ascii=False), C.now()))
        done += 1
        R.progress(tid, processed=done, total=total or None)
        if len(batch) >= 5 or (only is not None and not pick(1, only)):
            _commit(tid, batch)
            batch = []
        if only is not None and not pick(1, only):
            break
    if hist:
        C.gen_hist_add("pic", list(hist), hist, tid, C.provider_name(), t0h)
    _commit(tid, batch)


def unsave(word):
    """起草检查最后也没过（或者检查中途停了）：把临时存的画面设置删掉，免得被当成“能出片”。"""
    f = V.folder_of(word)
    base = C.REPO / EXTRA
    with C.REPO_LOCK:
        for q_ in (base / "words" / (f + ".json"), base / "words" / (f + ".py"), base / (f + "ai_art.py")):
            if q_.exists():
                q_.unlink()
        if (base / "art" / f).exists():
            C.rmtree(base / "art" / f)
        lst = base / "清单.tsv"
        if lst.exists():
            lst.write_text("\n".join(l for l in lst.read_text(encoding="utf-8").splitlines() if l.split("\t")[1:2] != [f]) + "\n", encoding="utf-8")
        head, rows = C.read_index()
        for r in rows:
            if r[2] == word and len(r) > 6 and r[6]:
                p = C.REPO / C.D / r[6]
                if p.exists():
                    rec = json.loads(p.read_text(encoding="utf-8"))
                    if rec.get("画面") or "检查" in rec:
                        rec.update({"画面": None, "插图": []})
                        rec.pop("画面生成", None)
                        rec.pop("检查", None)
                        p.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
                r[5] = "缺"
        C.write_index(head, rows)


def ntodo(line):
    """“还要补：a；b；c” → 3"""
    rest = (line or "").split("：", 1)[1] if "：" in (line or "") else (line or "")
    return len([x for x in re.split(r"[；;]", rest) if x.strip()]) or (1 if line else 0)


def short_why(errs):
    """没做成的原因，一句话。"""
    e = (errs or ["没说原因"])[0]
    e = re.sub(r"^视频技能起草检查没过：(还要补：)?", "", e).split("；")[0]
    return (e[:40] + "…") if len(e) > 40 else e


def todo_note(word, line):
    """能用、但起草检查说出片前还要补的，记在本机 data/pic_todo.json（以后可以再改）。"""
    p = C.DATA / "pic_todo.json"
    try:
        d = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    except Exception:
        d = {}
    if line:
        d[word] = {"todo": line, "t": time.strftime("%Y-%m-%d %H:%M")}
    else:
        d.pop(word, None)
    try:
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    except Exception:
        pass


def wsl_draft_safe(w, P, svgs):
    """先存一份草稿到画面设置文件夹，让 WSL 能读到，再起草检查。返回 (结果, 那一行)，见 wsl_draft；出片环境没装好返回 (None, "")。"""
    try:
        if not env_ready():
            return None, ""
        save(w, P, svgs, False)            # 临时存；没过会被下一次覆盖，最后没过、中途停下都会清掉
        return wsl_draft(w)
    except Exception as e:
        return "env", "起草检查出错（%s）" % str(e)[:100]


def _commit(tid, words, what="画面设置"):
    if not words:
        return
    cid = C.commit_pending("词库：%s %s（%d 个词，%s）" % (what, "、".join(words[:6]) + ("…" if len(words) > 6 else ""), len(words), "网页 AI 改的" if what == "补画面" else "网页 AI 做的"))
    if cid and C.load_cfg().get("autoPush", True):
        try:
            C.log(C.push(), tid)
        except Exception as e:
            C.log("上传没成功（%s），下次一起传" % str(e)[:150], tid)


def mock(prompt, words):
    w = words[0]
    f = V.folder_of(w)
    P = {"style": "core", "board": True,
         "pics": [{"text": "（模拟）%s" % w, "pos": "名词", "diff": "测试用", "bg": "blank", "img": "art/room-bg.svg",
                   "items": [{"svg": "art/%s-main.svg" % f, "x": 0.6, "y": 0.6, "s": 0.4, "z": 2},
                             {"actor": "walk-cn-girl", "x": 0.3, "y": 0.6, "s": 0.9, "z": 3}],
                   "ex": "This is a test.", "exzh": "这是测试。"}],
         "flow": [{"node": "① （模拟）", "pos": "名词", "pic": 0}]}
    return ("```json\n%s\n```\n<<<SVG %s-main.svg\n<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><circle cx=\"50\" cy=\"50\" r=\"40\" fill=\"#4a90d9\" stroke=\"#000\" stroke-width=\"3\"/></svg>\n>>>END\n%s"
            % (json.dumps(P, ensure_ascii=False), f, END))


# ═══════════ v1.11.1：补画面——存下了、可起草检查说还要补的词，带着“还要补什么”和上次的画面设置交给 AI 改好 ═══════════
# 手动接力做画面时（v1.10.6 起）不来回改：能用就存下，起草检查还想补的记一句“出片前还要补 N 处”。可出视频的流水线
# “准备”那一步要“还要补：都齐了”才往下做，所以这些词都卡在准备。这里把它们一批一批交给 AI 补齐；补好一个，批次里马上接着做一个。
_UC = {"t": 0.0, "set": set()}


def unchecked_words():
    """AI 做的画面里，存下了、还没过视频技能起草检查的词（出视频会卡在“准备”）。10 秒内用同一份。"""
    if time.time() - _UC["t"] < 10:
        return set(_UC["set"])
    out = set()
    try:
        folders = {p.stem for p in (C.REPO / EXTRA / "words").glob("*.json")}
        if folders:
            _, rows = C.read_index()
            seen = set()
            for r in rows:
                w = r[2]
                if w in seen or V.folder_of(w) not in folders:
                    continue
                seen.add(w)
                rel = r[6] if len(r) > 6 and r[6] else ""
                p = (C.REPO / C.D / rel) if rel else _rec_path(w)
                try:
                    rec = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
                except Exception:
                    rec = {}
                if "都齐了" not in str(rec.get("检查", "")):
                    out.add(w)
    except Exception:
        pass
    _UC.update(t=time.time(), set=out)
    return set(out)


# ═══════════ v1.11.5：补画面先攒着——点了「暂时忽略」的词记下来，攒够一定数量再一起交给 AI ═══════════
LATER = C.DATA / "pic_later.json"


def later_get():
    """{"later": [先攒着的词（还没补好的）], "all": [库里所有要补画面的词], "at": 攒够几个提醒}。补好了的自动拿掉。"""
    try:
        d = json.loads(LATER.read_text(encoding="utf-8")) if LATER.exists() else {}
    except Exception:
        d = {}
    unc = unchecked_words()
    words = [w for w in (d.get("words") or []) if w in unc]
    if words != (d.get("words") or []):
        d["words"] = words
        _later_save(d)
    return {"later": words, "all": sorted(unc), "at": max(1, int(d.get("at") or 10))}


def _later_save(d):
    try:
        LATER.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def later_op(b):
    try:
        d = json.loads(LATER.read_text(encoding="utf-8")) if LATER.exists() else {}
    except Exception:
        d = {}
    ws = list(d.get("words") or [])
    op = b.get("op")
    if op == "add":                    # 暂时忽略：先攒着
        new = [w for w in (b.get("words") or []) if isinstance(w, str) and w not in ws]
        ws += new
        msg = "先攒着了：%d 个词。攒够 %d 个，这里会提醒你一起补" % (len(new), max(1, int(d.get("at") or 10))) if new else "这些词本来就攒着了"
    elif op == "remove":
        rm = set(b.get("words") or [])
        ws = [w for w in ws if w not in rm]
        msg = "不再攒着了"
    elif op == "at":
        try:
            n = int(b.get("at"))
        except Exception:
            return {"ok": False, "msg": "要填数字"}
        if not 1 <= n <= 1000:
            return {"ok": False, "msg": "要填 1 到 1000 之间的数"}
        d["at"] = n
        msg = "存好了：攒够 %d 个提醒你" % n
    else:
        return {"ok": False, "msg": "认不出要做什么"}
    d["words"] = ws
    _later_save(d)
    r = later_get()
    r.update(ok=True, msg=msg)
    return r


def todo_all():
    p = C.DATA / "pic_todo.json"
    try:
        d = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    except Exception:
        d = {}
    return {w: (v or {}).get("todo", "") for w, v in d.items()}


def _items(line):
    """“还要补：a；b；c” → [a, b, c]（练习题归出题那一步管，不算）。"""
    line = line or ""
    rest = line.split("：", 1)[1] if line.startswith("还要补") and "：" in line else line
    rest = re.sub(r"练习题 lianxi（[^）]*）[；;]?", "", rest)
    return [x.strip() for x in re.split(r"[；;]", rest) if x.strip() and "都齐了" not in x]


def _old_svgs(word):
    art = C.REPO / EXTRA / "art" / V.folder_of(word)
    return {x.name: x.read_text(encoding="utf-8").strip() for x in art.glob("*.svg")} if art.exists() else {}


OUT_FIX = """【输出格式（程序按这个格式自动读，请严格照做）】
0. 一个词一段，按上面的顺序写：每段先单独一行写 @单词（比如 @%s），下面是这个词的全部内容；写完一个词再写下一个。
1. 每个词：一个代码块（第一行写 ```json），里面是这个词改好的画面设置，完整写一遍（没问题的地方照抄上次的，别丢东西；不能只写改的地方）。
2. 画里的人不要自己画，写成 {"actor": "动作名", "x": 0.3, "y": 0.6, "s": 0.9, "z": 3}，程序会换成会动的人。动作名只能用这些：%s。一个词里同一个动作、表情别重复用。
3. 不许用表情图（"e": "🚗" 这种），东西都用写实插图："svg": "art/名字.svg"。下面这些现成的场景和东西可以直接用：%s。
4. 插图只写新画的、要重画的（比如说“画得太简单”的那张，用同一个名字重画）；上次画好、这次不改的不用再写，程序会留着。每张一块，放在这个词的 JSON 代码块后面：
<<<SVG 名字.svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">……</svg>
>>>END
   插图要求：图画书风（黑色勾线、饱和平涂），画成现实生活里的样子；场景背景要详细、具体（这个地方真有的东西都画上，不少于 150 个图形），一张图不超过 30 KB。
5. 每次上传的内容，最后单独一行写：%s"""


def build_prompt_fix_multi(words, todos, rnd):
    """补画面的提示词：每个词写清楚“还要补什么”、附上次的画面设置；规矩、pictures.md、范例只放一次。"""
    rules, pm, ex = docs()
    ver, ed = skill_version()
    n = len(words)
    head = ("【补画面 · 这一批 %d 个词】这些词的“画面设置”以前做好、存下了，可视频技能 %s（%s）的起草检查说还缺东西，出视频时卡在“准备”这一步。"
            "请在上次的基础上，把每个词“还要补”的每一条都改好：\n"
            "- 每个词把改好的 JSON 完整写一遍（没问题的地方照抄上次的）；\n"
            "- 插图只写新画的、要重画的（比如“画得太简单”的场景，用同一个名字重画得详细些）；上次的、不改的不用再写，程序会留着；\n"
            "- 改的时候照着后面的规矩、pictures.md 和范例做。\n"
            "按顺序一个接一个写：每写完 %d 个词就上传一次（怎么传看最后），中间不用在聊天里汇报，接着写下一个；这一批全部传完再汇报一次。" % (n, ver, ed, rnd))
    segs = []
    for w in words:
        f = V.folder_of(w)
        try:
            P = json.loads((C.REPO / EXTRA / "words" / (f + ".json")).read_text(encoding="utf-8"))
        except Exception:
            P = {}
        P.pop("lianxi", None)
        arts = sorted(_old_svgs(w))
        items = _items(todos.get(w, ""))
        segs.append("@%s\n还要补（视频技能起草检查说的，每一条都要做到）：\n%s\n总表材料：%s\n上次已经画好的插图：%s\n上次的画面设置：\n```json\n%s\n```" % (
            w, "\n".join("- " + x for x in items) if items else "- 没记下具体缺什么：照规矩每一条再对一遍，缺的补上",
            _mat_short(w, 500), "、".join("art/" + a for a in arts) or "没有",
            json.dumps(P, ensure_ascii=False, separators=(",", ":"))[:14000]))
    return "\n\n".join([
        head,
        "【这一批的词（按这个顺序做）】\n" + "\n".join("%d. %s" % (i + 1, w) for i, w in enumerate(words)),
        self_check(),
        "【每个词：还要补什么、上次的画面设置】\n" + "\n\n".join(segs),
        "【视频技能 %s（%s）里和画面有关的规矩：每个词每一条都要做到】\n" % (ver, ed) + rules,
        "【画面怎么画、画面设置怎么写（视频技能 %s 的 pictures.md 全文）】\n" % ver + pm,
        "【范例：%s 的画面设置（视频技能 %s kit 里过了起草检查的，写法和你要交的一样；里面的 art/… 插图是那个词自己画的）】\n" % (EXAMPLE_WORD, ed) + ex,
        OUT_FIX % (words[0], "、".join(motions()), "、".join("art/" + x for x in scenes()), END)])


def _after_fix(tid, w, batch):
    """补好的词：画面设置拷进 WSL（流水线读的那一份），批次里让它从卡住的地方接着做。"""
    if not batch:
        return
    try:
        V.sync_pics()
        ok, msg = V.batch_op(batch, "retry", V.folder_of(w))
        C.log("  %s 补好了 → 批次 %s：%s" % (w, batch, msg), tid)
    except Exception as e:
        C.log("  %s 补好了，可批次 %s 没接上（%s）：到「出视频」页点「再试一次」" % (w, batch, str(e)[:100]), tid)


def do_pics_fix(R, tid, p):
    """任务：补画面（见上面）。p = {words: [...], fix: True, batch: 批次名（可以没有）}。"""
    batch = p.get("batch") or ""
    words = [w for w in (p.get("words") or []) if (C.REPO / EXTRA / "words" / (V.folder_of(w) + ".json")).exists()]
    if not words:
        C.log("补画面：这些词都没有 AI 做的画面设置，没什么可补的", tid)
        return
    todos = todo_all()
    if batch:
        try:
            todos.update({w: l for w, l in V.prep_todo(batch, words).items() if l})
        except Exception as e:
            C.log("读批次 %s 的起草检查记录没成功（%s）：用画面那一步记下的" % (batch, str(e)[:100]), tid)
    ask, fine = [], []
    for w in words:                                  # 没记下缺什么的：先在 WSL 里起草检查一遍（几秒钟），过了就不用问 AI
        R.check_stop()
        if _items(todos.get(w, "")):
            ask.append(w)
            continue
        old = _unchecked(w)
        if not old:
            fine.append(w)
            continue
        R.stage = "%s：起草检查（在 WSL 里）" % w
        st, line = wsl_draft_safe(w, *old)
        if st == "ok":
            save(w, old[0], old[1], True)
            todo_note(w, "")
            fine.append(w)
            C.log("  %s 存着的画面过了起草检查，不用改" % w, tid)
        else:
            save(w, old[0], old[1], False)
            if st == "todo":
                todo_note(w, line)
                todos[w] = line
            ask.append(w)
    for w in fine:
        _after_fix(tid, w, batch)
    _UC["t"] = 0.0
    if not ask:
        _commit(tid, fine, "补画面")
        return
    C.log("补画面：%d 个词交给 AI 改%s" % (len(ask), "；补好一个，批次 %s 就接着做一个" % batch if batch else ""), tid)
    if C.load_cfg().get("provider") == "relay":
        return _fix_relay(R, tid, ask, todos, batch)
    rounds = max(1, int(C.load_cfg().get("fixRounds", 3)))
    hist, t0, done, saved = {}, time.time(), 0, []
    for w in ask:
        R.check_stop()
        old, old_line = _unchecked(w), todos.get(w, "")
        ok, errs = _try(R, tid, w, rounds, force=True)
        left = todo_all().get(w, "")
        if not ok and old:                           # 改不好：上次的留着（不删）
            save(w, old[0], old[1], False)
            todo_note(w, old_line)
        good = ok and not left
        hist[w] = {"ok": good, "detail": "补好了" if good else ("还要补 %d 处" % ntodo(left) if ok else short_why(errs))}
        if ok:
            saved.append(w)
        if good:
            _after_fix(tid, w, batch)
        done += 1
        R.progress(tid, processed=done, total=len(ask))
    _UC["t"] = 0.0
    C.gen_hist_add("pic", list(hist), hist, tid, "补画面 · " + C.provider_name(), t0)
    _commit(tid, saved + fine, "补画面")


def _fix_relay(R, tid, words, todos, batch):
    """手动接力补画面：一份几个词（带着上次的画面设置，一份比做新画面少一些），网页 AI 一轮一轮交回。"""
    N, rnd = C.relay_size("fix")
    nb = (len(words) + N - 1) // N
    C.log("补画面（手动接力）：一共 %d 个词，一份 %d 个，分 %d 份；网页 AI 每写完 %d 个上传一次" % (len(words), N, nb, rnd), tid)
    done, saved, queue, k = 0, [], list(words), 0
    allres, t_all = {}, time.time()
    while queue:                    # v1.11.2：每一份开始时按现在的设置分（黄框里改了，下一份就按新的）
        N, rnd = C.relay_size("fix")
        pend, queue = queue[:N], queue[N:]
        k += 1
        nb = k + (len(queue) + N - 1) // N
        chunk, res, t0 = list(pend), {}, time.time()
        C.log("补画面第 %d 份（共 %d 份）：%s … %s，%d 个词" % (k, nb, pend[0], pend[-1], len(pend)), tid)
        while pend:
            C.RELAY_QLEFT[0] = len(queue)
            for part in R.ask_parts(tid, "补画面", build_prompt_fix_multi(pend, todos, min(rnd, len(pend))), pend, min(rnd, len(pend))):
                fx = [w for w in (C.RELAY.get("fixing") or []) if w in chunk and w not in pend]   # v1.12.0：没过、网页 AI 在改的
                got = parse_multi(part, pend + fx)
                if not got:
                    C.RELAY["hint"] = "交回的这个文件里没认出这一批还没补的词（每个词要先写一行 @单词）"
                    continue
                for w, (P, raw, svgs, errs) in got.items():
                    first = w in pend
                    if not first and w not in fx:
                        continue
                    old, old_line = _unchecked(w), todos.get(w, "")
                    info = {}
                    ok, why, errs2 = _accept(R, tid, w, P, dict(_old_svgs(w), **(svgs or {})), errs, info)
                    st, line = info.get("st"), info.get("line") or ""
                    if ok and st == "todo" and old and old_line and ntodo(line) > ntodo(old_line):
                        save(w, old[0], old[1], False)          # 改完反而缺得更多：留着上次的
                        todo_note(w, old_line)
                        ok, why = False, "改完反而要补 %d 处（上次 %d 处）" % (ntodo(line), ntodo(old_line))
                    good = ok and st != "todo"
                    k = int(((C.RELAY.get("verdict") or {}).get(w) or {}).get("try") or 0) + 1
                    if good:
                        if w not in saved:
                            saved.append(w)
                        C.log("  %s 补好了%s%s" % (w, "（起草检查：都齐了）" if st == "ok" else "（这台电脑起草检查不了，出片时再查）",
                                                "（改了 %d 次）" % (k - 1) if k > 1 else ""), tid)
                        _after_fix(tid, w, batch)
                    elif ok:
                        if w not in saved:
                            saved.append(w)
                        todos[w] = line
                        why = "改了，还要补 %d 处" % ntodo(line)
                        C.log("  %s 改了，可起草检查说还要补 %d 处（第 %d 次）：%s" % (w, ntodo(line), k, line[:160]), tid)
                    else:
                        C.log("  %s 这次没补成（第 %d 次）：%s（上次的画面留着）" % (w, k, why), tid)
                    tell = line if (st == "todo" and line) else ("；".join(errs2 or []) or why)
                    if why.startswith("改完反而"):
                        tell = "%s（%s，上次的留着；照下面这几条改）：%s" % (why, "比上次缺得多", line)
                    gave = C.relay_verdict(w, good, tell)
                    if not good and w in (C.RELAY.get("fixing") or []):
                        why = (why or "没补好") + "，网页 AI 在改"
                    elif gave:
                        later_op({"op": "add", "words": [w]})     # 改够次数了还没过：先攒着，以后一起补
                        why = (why or "") + "（改了 %d 次，先攒着）" % k
                    C.relay_word(w, good, why or "补好了")
                    res[w] = {"ok": good, "detail": why or "补好了"}
                    if first:
                        pend.remove(w)
                        done += 1
                        R.progress(tid, processed=done, total=len(words))
                    if len(saved) >= 5:
                        _commit(tid, saved, "补画面")
                        saved = []
            fx = [w for w in (C.RELAY.get("fixing") or []) if w in chunk and w not in pend]
            if C.RELAY.get("endReason") in ("newchat", "resize") and fx:    # 在改的词也放进新的提示词（带着最新的“还要补”）
                pend += fx
            elif C.RELAY.get("endReason") == "skiprest" and fx:
                later_op({"op": "add", "words": fx})
            if pend and C.RELAY.get("endReason") in ("newchat", "resize"):
                N2, rnd = C.relay_size("fix")
                if len(pend) > N2:                  # 一批改小了：多出来的放回去，排到下一份
                    queue, pend = pend[N2:] + queue, pend[:N2]
                elif len(pend) < N2 and queue:      # v1.11.3：一批改大了，后面排着的拿进来
                    more, queue = queue[:N2 - len(pend)], queue[N2 - len(pend):]
                    pend += more
                    chunk += more
                nb = k + (len(queue) + N2 - 1) // N2
                C.log("  剩下的 %d 个另开对话：出一份新的提示词" % len(pend), tid)
                continue
            for w in pend:
                C.relay_word(w, False, "跳过了")
                res[w] = {"ok": False, "detail": "你点了「剩下的先跳过」（上次的画面留着）"}
                done += 1
            if pend:
                C.log("  剩下的 %d 个先跳过了：%s" % (len(pend), "、".join(pend[:20])), tid)
            pend = []
        _UC["t"] = 0.0
        C.gen_hist_add("pic", [w for w in chunk if w in res], res, tid, "补画面 · 第 %d 批（共 %d 批）" % (k, nb), t0)
        allres.update(res)
        _commit(tid, saved, "补画面")
        saved = []
    relay_final(tid, "补画面", allres, t_all)
