# -*- coding: utf-8 -*-
"""单词工作台 · v1.48.0：总表放进软件里，软件自己管。
用户：“你先把 excel 总表填进软件里面，用软件自己来管理，不用每次都调取 excel……把 excel 里面的内容先按照软件目前的结构进行分列一下，
把之前放在一个单元格里面的内容进行拆分。你先把软件设置一下，总表部分加一个导入，然后你再给一个导入模版，我发给新的 AI 聊天，把这个总表进行拆分一下”。

存在仓库里：词库/总表数据/批次/<批次>.jsonl（一个批次一个文件，改一个批次只动一个小文件）+ 说明.json（从哪一版 Excel 来的、哪天导入的、批次顺序）。
每一行只存：“原表”（Excel 原来那一行，一格不动，视频技能和软件别的地方照旧读它）+ AI 拆的那几列、例句；
本地能拆的那几列不存，读的时候现拆（规则改了不用重新导入）。
  1. 从 Excel 导入：原样存进来；能一眼拆开的先在本地拆（考点按【变形】【短语】…，组合按【构词逻辑】→【演变】…，辨析的【同义词】组，背景，不拆的词的来历）
  2. 要动脑子的几列（每部分卡片：身份、来源、意思、记法……；辨析里每个词的区别）交给 AI：导出“要拆的表”，连同模板、说明发给 AI 聊天，拆好再导入
  3. 导入拆好的表：先预览（改了几行、哪些可能丢了内容），确认了才写进去，提交、上传
"""
import base64
import hashlib
import io
import json
import re
import time

import core as C

DIR = "词库/总表数据"
BDIR = lambda: C.REPO / DIR / "批次"
META = lambda: C.REPO / DIR / "说明.json"
PEND = lambda: C.DATA / "tabledb_pending.json"
OLD_COLS = ["批次", "序号", "组号", "小类号", "单词", "含义", "类型", "拆分", "前缀", "词根", "单词部分", "后缀", "组合 → 现在的含义", "辨析",
            "新·背景（只写在词族第一个词上）", "音变 / 字母变化", "词根变体处理", "考点", "题目1", "题目2", "题目3", "题目4", "题目5", "题目6",
            "题目7", "答案", "读音现象", "初中含义"]

# 新的分列：(列名, 哪一组, 放什么, 本地拆 / AI 拆 / 原样)
_P = []
for i in range(1, 5):
    _P += [("部分%d" % i, "词根词缀卡", "第 %d 部分的写法，前缀后面带 -、后缀前面带 -、词根后面带 -（re-、popul-、-ar、match）" % i, "AI"),
           ("部分%d 身份" % i, "词根词缀卡", "前缀 / 词根 / 后缀 / 单词（这一部分本身是个词）", "AI"),
           ("部分%d 来源" % i, "词根词缀卡", "拉丁语 / 希腊语 / 法语 / 英语本族……（原文写了才填）", "AI"),
           ("部分%d 意思" % i, "词根词缀卡", "这一部分的意思，短（再、又；人民、民众；…的、属于…的）", "AI"),
           ("部分%d 记法" % i, "词根词缀卡", "原文“记：”后面那一句（popul ≈ people……）", "AI"),
           ("部分%d 音变" % i, "词根词缀卡", "原文“音变：”后面那一句（这一部分自己的字母、读音怎么变的）", "AI"),
           ("部分%d 补充" % i, "词根词缀卡", "这一部分别的说明：本义、出处、只用在词前、同 rewrite 重写……", "AI")]
COLS = [
    ("单词", "基本", "单词，原样", "原样"), ("批次", "基本", "原样", "原样"), ("序号", "基本", "原样", "原样"),
    ("组号", "基本", "原样", "原样"), ("小类号", "基本", "原样", "原样"), ("类型", "基本", "原样（① 词根词缀、⑤ 基础词……）", "原样"),
    ("初中含义", "基本", "原样", "原样"), ("含义", "基本", "原样（一行一个词性）", "原样"),
    ("读音现象", "读音拆分", "原样", "原样"),
    ("拆分", "词根词缀卡", "原样（re + match；不拆的写 —）", "原样"),
] + _P + [
    ("来历", "词根词缀卡", "不拆开的词（make、match ≈ make）：原来「单词部分」那一格，就是视频里那张“来历”卡片", "本地"),
    ("词缀辨析", "词根词缀卡", "前缀、后缀那一格里“辨析：同样是……”那一整段（视频里单独一幕“辨析”讲几个词缀的区别）", "AI"),
    ("为什么用这个词缀", "词根词缀卡", "“为什么用 -ar 不用 -al：……”那一句", "AI"),
    ("词根变体", "词根词缀卡", "原来「词根变体处理」，原样", "原样"),
    ("构词逻辑", "拼起来", "【构词逻辑】那一行等号以前的部分到等式（re（再）+ match（比赛）=“再比一场”），不带后面的“词性变化”", "本地"),
    ("词性变化", "拼起来", "“词性变化（-ar）：名词 → 形容词”那一截", "本地"),
    ("演变步骤", "意思演变", "【构词逻辑】下面 → 、①② 开头的几行，一行一步，原样", "本地"),
    ("演变史", "意思演变", "【演变】那一段，原样", "本地"),
    ("背景", "意思演变", "原来「新·背景」去掉【背景】两个字", "本地"),
    ("趣闻", "意思演变", "组合那一格里【趣】那一段", "本地"),
    ("语法", "意思演变", "组合那一格里【语法】那一段", "本地"),
    ("提醒", "意思演变", "组合那一格里【提醒】那一段", "本地"),
    ("例子", "意思演变", "组合那一格里【例】那一段", "本地"),
    ("组合其他", "意思演变", "组合那一格里别的【…】段（【联想】【易混】【同形异义】……），带着标签原样放", "本地"),
    ("例句", "例句", "一行一个意思：意思｜英文例句｜中文。总表原来没有，这一次空着，以后单独补", "以后"),
    ("同义词组", "同义词辨析", "【同义词】那几行，一行一组：中文意思：词1、词2（去掉【同义词】几个字）", "本地"),
    ("区别", "同义词辨析", "一行一个词：词｜它的区别（从辨析的话里拆出来，原话不改）", "AI"),
    ("辨析说明", "同义词辨析", "辨析那一格除了【同义词】那几行，剩下的话，原样", "本地"),
    ("变形", "考点", "考点里【变形】那一段", "本地"), ("短语", "考点", "考点里【短语】那一段", "本地"),
    ("用法", "考点", "考点里【用法】那一段", "本地"), ("易混", "考点", "考点里【易混】那一段", "本地"),
    ("词性转换", "考点", "考点里【词性转换】那一段", "本地"), ("其他考点", "考点", "考点里别的【…】段，带着标签原样放", "本地"),
    ("同源和字母变化", "总结小黑板", "原来「音变 / 字母变化」，原样", "原样"),
] + [("题目%d" % i, "练习题", "原样", "原样") for i in range(1, 8)] + [("答案", "练习题", "原样", "原样")] + [
    ("没放进去的", "其他", "拆的时候不知道放哪一列的原话，原样放这里（一个字都不要丢）", "AI"),
]
NAMES = [c[0] for c in COLS]
AI_COLS = [c[0] for c in COLS if c[3] == "AI"]
KEEP = set(AI_COLS + ["例句"])                     # 存进文件的（别的读的时候从原表现拆）
SAME = {"单词": "单词", "批次": "批次", "序号": "序号", "组号": "组号", "小类号": "小类号", "类型": "类型", "初中含义": "初中含义", "含义": "含义",
        "读音现象": "读音现象", "拆分": "拆分", "词根变体": "词根变体处理", "同源和字母变化": "音变 / 字母变化", "答案": "答案",
        **{"题目%d" % i: "题目%d" % i for i in range(1, 8)}}


def _s(v):
    return "" if v is None else str(v).strip()


def _tags(text):
    """“【A】…【B】…” → [(A, 内容), …]；最前面没有标签的一段标签是空"""
    out, cur, buf = [], "", []
    for part in re.split(r"(【[^】]{1,8}】)", text or ""):
        m = re.fullmatch(r"【([^】]{1,8})】", part)
        if m:
            if buf and "".join(buf).strip():
                out.append((cur, "".join(buf).strip()))
            cur, buf = m.group(1), []
        else:
            buf.append(part)
    if buf and "".join(buf).strip():
        out.append((cur, "".join(buf).strip()))
    return out


def local_split(o):
    """能一眼拆开的，本地先拆（不要 AI）"""
    r = {k: _s(o.get(v)) for k, v in SAME.items()}
    for k in ("拆分",):
        r[k] = _s(o.get(k))
    if r["拆分"] in ("", "-", "—") or "+" not in r["拆分"]:
        r["来历"] = "" if _s(o.get("单词部分")) in ("", "-", "—") else _s(o.get("单词部分"))
    bg = _s(o.get("新·背景（只写在词族第一个词上）"))
    r["背景"] = re.sub(r"^【背景】\s*", "", bg)
    # 组合 → 现在的含义
    other = []
    for tag, body in _tags(_s(o.get("组合 → 现在的含义"))):
        if tag == "构词逻辑":
            first, _, rest = body.partition("\n")
            m = re.search(r"[；;]\s*(词性变化.*)$", first)
            if m:
                r["词性变化"] = re.sub(r"^词性变化", "", m.group(1)).strip("：: ")
                first = first[:m.start()]
            r["构词逻辑"] = first.strip()
            steps = [l.strip() for l in rest.split("\n") if l.strip()]
            r["演变步骤"] = "\n".join(steps)
        elif tag == "演变":
            r["演变史"] = body
        elif tag == "趣":
            r["趣闻"] = body
        elif tag == "语法":
            r["语法"] = body
        elif tag == "提醒":
            r["提醒"] = body
        elif tag == "例":
            r["例子"] = body
        elif tag == "背景" and not r["背景"]:
            r["背景"] = body
        else:
            other.append(("【%s】" % tag if tag else "") + body)
    r["组合其他"] = "\n".join(other)
    # 辨析
    bx = _s(o.get("辨析"))
    syn = [re.sub(r"^【同义词】\s*", "", l.strip()) for l in bx.split("\n") if l.strip().startswith("【同义词】")]
    r["同义词组"] = "\n".join(syn)
    r["辨析说明"] = "\n".join(l.strip() for l in bx.split("\n") if l.strip() and not l.strip().startswith("【同义词】"))
    # 考点
    oth = []
    for tag, body in _tags(_s(o.get("考点"))):
        if tag in ("变形", "短语", "用法", "易混", "词性转换"):
            r[tag] = (r.get(tag, "") + "\n" + body).strip()
        else:
            oth.append(("【%s】" % tag if tag else "") + body)
    r["其他考点"] = "\n".join(oth)
    return r


def _key(rec):
    return (str(rec.get("批次", "")), str(rec.get("序号", "")), str(rec.get("单词", "")))


def _hash(o):
    return hashlib.md5(json.dumps({k: _s(o.get(k)) for k in OLD_COLS}, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:12]


def _bfile(b):
    return BDIR() / ("%s.jsonl" % (re.sub(r"[^\w\-]+", "_", str(b)) or "_"))


_LOAD = {"key": None, "val": []}


def load():
    m = meta()
    if not m:
        return []
    key = META().stat().st_mtime
    if _LOAD["key"] == key:
        return [dict(r) for r in _LOAD["val"]]
    out = []
    for b in m.get("批次顺序") or []:
        try:
            lines = _bfile(b).read_text(encoding="utf-8").splitlines()
        except Exception:
            continue
        for l in lines:
            if not l.strip():
                continue
            d = json.loads(l)
            o = d.get("原表") or {}
            r = local_split(o)
            r.update({k: v for k, v in d.items() if k in KEEP and v})
            r["原表"], r["原表hash"] = o, _hash(o)
            out.append(r)
    _LOAD.update(key=key, val=out)
    return [dict(r) for r in out]


def meta():
    try:
        return json.loads(META().read_text(encoding="utf-8"))
    except Exception:
        return {}


def _write(recs, m):
    """一个批次一个文件；内容没变的文件不重写（git 里只多改了的那几个）"""
    BDIR().mkdir(parents=True, exist_ok=True)
    order, by = [], {}
    for r in recs:
        b = str(r.get("批次", ""))
        if b not in by:
            order.append(b)
            by[b] = []
        d = {"原表": r.get("原表") or {}}
        d.update({k: r[k] for k in KEEP if r.get(k)})
        by[b].append(json.dumps(d, ensure_ascii=False, separators=(",", ":")))
    keep = set()
    for b in order:
        f = _bfile(b)
        keep.add(f.name)
        t = "\n".join(by[b]) + "\n"
        if not f.exists() or f.read_text(encoding="utf-8") != t:
            f.write_text(t, encoding="utf-8")
    for f in BDIR().glob("*.jsonl"):
        if f.name not in keep:
            f.unlink()
    m["批次顺序"] = order
    META().write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
    _CACHE["key"] = None
    _LOAD["key"] = None


def _read_xlsx(data_or_path, sheet=None):
    import openpyxl
    wb = openpyxl.load_workbook(data_or_path if isinstance(data_or_path, str) else io.BytesIO(data_or_path), read_only=True, data_only=True)
    ws = wb[sheet] if sheet and sheet in wb.sheetnames else (wb["拆分结果"] if "拆分结果" in wb.sheetnames else wb.worksheets[0])
    it = ws.iter_rows(values_only=True)
    h = [_s(v) for v in next(it)]
    rows = []
    for r in it:
        d = {h[i]: r[i] for i in range(min(len(h), len(r))) if h[i]}
        if _s(d.get("单词")):
            rows.append(d)
    return h, rows


def _ai_done(r):
    """这一行要 AI 拆的拆过没有"""
    if r.get("拆分") and "+" in r.get("拆分", ""):
        return bool(r.get("部分1"))
    return True


def import_excel():
    """从仓库里最新的 Excel 总表导入：原样存进来，能拆的本地先拆；以前 AI 拆过、这一行 Excel 又没变的，AI 拆的留着"""
    if not C.STATE.get("xlsx"):
        return {"ok": False, "msg": "仓库还没准备好，找不到 Excel 总表"}
    t0 = time.time()
    h, rows = _read_xlsx(str(C.REPO / C.STATE["xlsx"]), "拆分结果")
    old = {_key(r): r for r in load()}
    recs, kept, changed = [], 0, 0
    for o in rows:
        o = {k: _s(o.get(k)) for k in OLD_COLS}
        r = local_split(o)
        r["原表"] = o
        r["原表hash"] = _hash(o)
        p = old.get(_key(r))
        if p and p.get("原表hash") == r["原表hash"]:
            for k in AI_COLS + ["例句"]:
                if p.get(k):
                    r[k] = p[k]
            if any(p.get(k) for k in AI_COLS):
                kept += 1
        elif p:
            changed += 1
        recs.append(r)
    m = {"来源": C.STATE["xlsx"], "版本": C.STATE.get("version", ""), "导入": time.strftime("%Y-%m-%d %H:%M"), "行数": len(recs),
         "词数": len({r["单词"] for r in recs})}
    _write(recs, m)
    _commit("词库：总表放进软件（%s，%d 行），能拆的本地先拆了" % (m["版本"], len(recs)))
    msg = "导入了 %d 行（%d 个词），来自 %s，用了 %.1f 秒；考点、演变、同义词组、背景、来历已经在本地拆好" % (len(recs), m["词数"], m["版本"], time.time() - t0)
    if kept:
        msg += "；%d 行以前 AI 拆过、Excel 没改，留着" % kept
    if changed:
        msg += "；%d 行 Excel 改过了，AI 拆的那几列要重拆" % changed
    C.log("总表导入：" + msg)
    return {"ok": True, "msg": msg}


def _commit(msg):
    try:
        cid = C.commit_pending(msg)
        if cid and C.load_cfg().get("autoPush", True):
            import threading
            threading.Thread(target=lambda: C.log(C.push()), daemon=True).start()
    except Exception as e:
        C.log("总表数据存下了，提交没成功（%s）：下次一起传" % str(e)[:120])


def status():
    recs, m = load(), meta()
    need = [r for r in recs if not _ai_done(r)]
    split = [r for r in recs if r.get("拆分") and "+" in r.get("拆分", "")]
    cnt = lambda k: sum(1 for r in recs if r.get(k))
    batches = []
    for r in recs:
        b = str(r.get("批次", ""))
        if b and b not in batches:
            batches.append(b)
    try:
        pend = json.loads(PEND().read_text(encoding="utf-8"))
    except Exception:
        pend = None
    return {"ok": True, "has": bool(recs), "meta": m, "rows": len(recs), "words": len({r["单词"] for r in recs}),
            "excel": C.STATE.get("xlsx", ""), "excelVer": C.STATE.get("version", ""),
            "stale": bool(recs) and m.get("来源") != C.STATE.get("xlsx"),
            "split": len(split), "splitDone": len(split) - len(need), "needAI": len(need),
            "cnt": {k: cnt(k) for k in ("来历", "构词逻辑", "演变步骤", "演变史", "同义词组", "区别", "辨析说明", "变形", "易混", "例句", "词缀辨析")},
            "batches": batches, "pending": {k: pend.get(k) for k in ("files", "rows", "match", "changed", "warn", "unknownCols", "notFound")} if pend else None}


# ── 导出：模板、要拆的表、说明 ──
EXAMPLES = {
    "make": {"来历": "make：英语本族的基础词（古英语 macian），最早的意思是“揉捏成形 → 做出来”",
             "区别": "make｜重“造出东西、产生结果”（make a cake / a mistake / a decision）\ndo｜重“从事一项活动”（do homework / do the dishes）"},
    "rematch": {"部分1": "re-", "部分1 身份": "前缀", "部分1 来源": "拉丁语", "部分1 意思": "再、又",
                "部分1 补充": "本义“往回”，往回再来一次就是“再”；只用在词前，不单独成词；同 rewrite 重写、replay 重放",
                "部分2": "match", "部分2 身份": "单词", "部分2 意思": "比赛", "部分2 补充": "见 match",
                "区别": "rematch｜同一对对手“再交手一次”\nreplay｜多指因平局等原因“重赛一场”，也指“重播”"},
    "popular": {"部分1": "popul-", "部分1 身份": "词根", "部分1 来源": "拉丁语", "部分1 意思": "人民、民众",
                "部分1 记法": "popul ≈ people（人民）：people 是人民，popul 也是人民；people 就是从它变来的",
                "部分1 音变": "populus（拉丁语）→ pople（古法语）→ peuple（古法语）→ people（英语）：中间的 u 被吞掉，开头的 o 拉长写成 eu，英语写成 eo",
                "部分1 补充": "拉丁语 populus“一国的全体人民”；people 是它经法语变来的样子（见 people）",
                "部分2": "-ar", "部分2 身份": "后缀", "部分2 来源": "拉丁语", "部分2 意思": "= -al，形容词词尾“…的、属于…的”",
                "部分2 补充": "来自拉丁语形容词词尾 -aris，就是 -alis，前面有 l 时写成 -aris",
                "词缀辨析": None, "为什么用这个词缀": "词干里已经有 l 时，拉丁语常把 -al 换成 -ar，免得两个 l 音重复（同 singular 单一的、solar 太阳的）",
                "区别": "popular｜“很多人喜欢”\nfamous｜“很多人知道”，出名不等于受欢迎"},
}


def _example_rows():
    recs = {r["单词"]: r for r in load()}
    out = []
    for w, ex in EXAMPLES.items():
        r = dict(recs.get(w) or {})
        if not r:
            continue
        for k, v in ex.items():
            if k == "词缀辨析":
                suf = r.get("原表", {}).get("后缀", "")
                m = re.search(r"辨析[:：](.*?)(?:\n为什么用|$)", suf, re.S)
                v = ("同样" + m.group(1).strip().split("同样", 1)[-1]) if m else ""
            r[k] = v
        out.append(r)
    return out


def _sheet_rows(recs):
    return [[r.get(k, "") or "" for k in NAMES] for r in recs]


def _xlsx(sheets):
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    color = {"本地": "E8F3EC", "AI": "FFF2CC", "原样": "EEF2F6", "以后": "F3E8FF"}
    kind = {c[0]: c[3] for c in COLS}
    for name, head, rows, widths in sheets:
        ws = wb.create_sheet(name)
        ws.append(head)
        for r in rows:
            ws.append([str(v)[:32000] if v is not None else "" for v in r])
        for i, h in enumerate(head, 1):
            c = ws.cell(row=1, column=i)
            c.font = Font(bold=True)
            if name != "列说明" and h in kind:
                c.fill = PatternFill("solid", fgColor=color[kind[h]])
            ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = widths(h) if callable(widths) else widths[i - 1]
        for row in ws.iter_rows(min_row=2):
            for c in row:
                c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.freeze_panes = "B2"
    b = io.BytesIO()
    wb.save(b)
    return b.getvalue()


def _w(h):
    return 34 if h in ("演变步骤", "演变史", "背景", "辨析说明", "区别", "词缀辨析", "没放进去的", "来历") or h.endswith("补充") else (12 if h in ("批次", "序号", "组号", "小类号") else 18)


def _doc_rows():
    return [[c[0], c[1], {"本地": "软件自己拆（导出时已经填好）", "AI": "要你拆（黄色）", "原样": "照抄原表", "以后": "这一次空着"}[c[3]], c[2]] for c in COLS]


def template():
    return _xlsx([("拆分结果", NAMES, _sheet_rows(_example_rows()), _w),
                  ("列说明", ["列名", "哪一块", "谁来填", "放什么"], _doc_rows(), [18, 12, 22, 90])])


def export_for_ai(frm="", to="", only_need=True, limit=400):
    """导出要 AI 拆的行（模板格式，本地能拆的已经填好）。frm、to 是批次；only_need：只要还没拆的"""
    recs = load()
    bs = []
    for r in recs:
        b = str(r.get("批次", ""))
        if b not in bs:
            bs.append(b)
    lo = bs.index(frm) if frm in bs else 0
    hi = bs.index(to) if to in bs else len(bs) - 1
    keep = set(bs[lo:hi + 1])
    sel = [r for r in recs if str(r.get("批次", "")) in keep and (not only_need or not _ai_done(r))][:max(1, int(limit))]
    # “原表”那几格附在最后几列，AI 对着拆
    head = NAMES + ["【原表】" + k for k in ("拆分", "前缀", "词根", "单词部分", "后缀", "辨析", "词根变体处理")]
    rows = [[r.get(k, "") or "" for k in NAMES] + [(r.get("原表") or {}).get(k, "") for k in ("拆分", "前缀", "词根", "单词部分", "后缀", "辨析", "词根变体处理")]
            for r in sel]
    name = "总表要拆的-第%s到%s批-%d行.xlsx" % (bs[lo] if bs else "", bs[hi] if bs else "", len(sel))
    return name, _xlsx([("拆分结果", head, rows, lambda h: 30 if h.startswith("【原表】") else _w(h)),
                        ("列说明", ["列名", "哪一块", "谁来填", "放什么"], _doc_rows(), [18, 12, 22, 90])]), len(sel)


# ── 导入拆好的表 ──
def _blob(r):
    return "".join(_s(r.get(k)) for k in ("拆分", "前缀", "词根", "单词部分", "后缀", "辨析", "词根变体处理"))


def preview(files):
    """files: [{name, b64}]。读出来、对上软件里的行、算出改了什么，先存着等你确认"""
    recs = load()
    if not recs:
        return {"ok": False, "msg": "软件里还没有总表：先点「从 Excel 总表导入」"}
    idx = {}
    for i, r in enumerate(recs):
        idx.setdefault(_key(r), i)
        idx.setdefault(("", "", r["单词"]), i)
    changes, warn, unknown, notfound, nrows = {}, [], set(), [], 0
    for f in files or []:
        try:
            h, rows = _read_xlsx(base64.b64decode(f.get("b64") or ""))
        except Exception as e:
            return {"ok": False, "msg": "%s 读不了：%s" % (f.get("name"), str(e)[:120])}
        unknown |= {x for x in h if x and x not in NAMES and not x.startswith("【原表】")}
        cols = [x for x in h if x in KEEP]          # 只收 AI 拆的那几列和例句；本地拆的、原样的照软件里的
        for d in rows:
            nrows += 1
            k = (_s(d.get("批次")), _s(d.get("序号")), _s(d.get("单词")))
            i = idx.get(k, idx.get(("", "", k[2])))
            if i is None:
                notfound.append(k[2])
                continue
            r = recs[i]
            new = {c: _s(d.get(c)) for c in cols}
            diff = {c: v for c, v in new.items() if v != (r.get(c) or "")}
            if not diff:
                continue
            changes[i] = new
            # 有没有丢内容：原表那几格的字，拆完以后在不在
            orig = _blob(r.get("原表") or {})
            got = "".join(new.get(c, r.get(c, "")) or "" for c in NAMES if c not in ("单词", "批次", "序号"))
            miss = [x for x in re.findall(r"[\u4e00-\u9fff]{4,}", orig) if x not in got]
            if miss and len("".join(miss)) > 0.15 * max(1, len(re.sub(r"[^\u4e00-\u9fff]", "", orig))):
                warn.append({"word": r["单词"], "why": "原表里有些话拆完找不到了：" + "、".join(miss[:3])})
            if new.get("没放进去的"):
                warn.append({"word": r["单词"], "why": "有放不进去的：" + new["没放进去的"][:60]})
    pend = {"t": time.time(), "files": [f.get("name") for f in files or []], "rows": nrows, "match": nrows - len(notfound),
            "changed": len(changes), "warn": warn[:200], "unknownCols": sorted(unknown), "notFound": notfound[:50],
            "changes": {str(i): v for i, v in changes.items()}}
    PEND().write_text(json.dumps(pend, ensure_ascii=False), encoding="utf-8")
    return {"ok": True, **{k: v for k, v in pend.items() if k != "changes"},
            "sample": [{"word": recs[i]["单词"], "cols": [c for c in v if v[c] != (recs[i].get(c) or "")][:8]} for i, v in list(changes.items())[:20]]}


def apply():
    try:
        pend = json.loads(PEND().read_text(encoding="utf-8"))
    except Exception:
        return {"ok": False, "msg": "没有等着导入的：先选文件，看过预览"}
    recs = load()
    for i, v in (pend.get("changes") or {}).items():
        i = int(i)
        if i < len(recs):
            recs[i].update(v)
    m = meta()
    m["拆分导入"] = time.strftime("%Y-%m-%d %H:%M")
    _write(recs, m)
    PEND().unlink()
    _commit("词库：总表导入拆好的 %d 行（%s）" % (len(pend.get("changes") or {}), "、".join(pend.get("files") or [])[:80]))
    return {"ok": True, "msg": "导入了 %d 行拆好的内容，存进软件、上传了" % len(pend.get("changes") or {})}


def cancel():
    try:
        PEND().unlink()
    except Exception:
        pass
    return {"ok": True, "msg": "不导入了"}


# ── 软件别的地方读总表：软件里有、而且和仓库里的 Excel 是同一版，就读软件里的，不再打开 Excel ──
_CACHE = {"key": None, "val": None}


def table_for_core():
    m = meta()
    if not m or m.get("来源") != C.STATE.get("xlsx"):
        return None
    key = ("db", META().stat().st_mtime)
    if _CACHE["key"] == key:
        return _CACHE["val"]
    words, order = {}, []
    for r in load():
        o = r.get("原表") or {}
        w = _s(o.get("单词"))
        if not w:
            continue
        rec = {f: _s(o.get(f)) for f in C.FIELDS}
        words.setdefault(w, []).append(rec)
        order.append((rec["批次"], rec["序号"], w))
    _CACHE.update(key=key, val=(key, words, order))
    return _CACHE["val"]
