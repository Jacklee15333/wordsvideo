# -*- coding: utf-8 -*-
"""单词工作台 · v1.35.0：起草配音稿（「导入 → 配音稿」）。
用户：“这里还没起草，视频里说的这些是什么意思？是不是这里还需要专门开启一步？需要的话你就直接设计一下”。

“起草”＝视频技能按总表 + 画面设置写出这个词视频里要念的话（精简版配音稿 ~/wordfilm-work/<词>/brief/plan.json），
同时做一遍起草检查（“还要补：…”）。以前只有做画面、单词检测、出片“准备”时顺带起草；这一步可以随时给选上的词起草：
  - 没有画面设置的词也能起草：总表来的几块（词根词缀卡、拼起来、意思、演变、辨析、考点）照样写出来，画面那几块等做了画面再补
  - 画面设置改过（比起草的时候新），标“要重新起草”
不用 AI，在 WSL 里跑视频技能（要先「检测 → 一键修复」同步过），一个词几秒到十几秒。"""
import json
import os
import re
import threading
import time

import core as C
import video as V
import sections as SEC

ST = {"running": False, "stop": False, "done": 0, "total": 0, "cur": "", "started": 0.0, "msg": "", "log": [], "from": ""}
_LOCK = threading.Lock()
_RES = lambda: C.DATA / "draft_results.json"        # {文件夹: {ts, rc, line}}


def _res_load():
    try:
        return json.loads(_RES().read_text(encoding="utf-8"))
    except Exception:
        return {}


def _pic_mtime(word):
    p = C.REPO / V.EXTRA / "words" / (V.folder_of(word) + ".json")
    try:
        return time.strftime("%Y-%m-%d %H:%M", time.localtime(p.stat().st_mtime))
    except Exception:
        return ""


SAY_SECS = ("pron", "parts", "combo", "scene", "evolve", "dist", "kaodian")      # v1.37.0 讲稿：总表来的几块


def _table_mtime():
    try:
        p = C.REPO / C.STATE["xlsx"] if C.STATE.get("xlsx") else None
        return time.strftime("%Y-%m-%d %H:%M", time.localtime(p.stat().st_mtime)) if p else ""
    except Exception:
        return ""


def _todo(line):
    """“还要补：【意思场景】…；【例句动画】…” → [{sec, name, text}]（练习题归出题，不算）"""
    import pics as P
    out = []
    for t in P._items(line or ""):
        sid = SEC._sec_of(t)
        out.append({"sec": sid, "name": (SEC.BY_ID.get(sid) or {}).get("name", ""), "text": re.sub(r"^\s*【[^】]+】", "", t)})
    return out


def status(words=None):
    """v1.37.0：一份配音稿，两处看——
    「导入 → 讲稿」：总表来的几块要说的话（不用画面）；「画面设计 → 定稿」：画面做好以后，把画上的话也写进去，对一遍还要补什么。"""
    import pics as P
    words = SEC._picked() if words is None else words
    try:
        pl = SEC.plans(words)
    except Exception:
        pl = {}
    res = _res_load()
    tm = _table_mtime()
    try:
        ptodo = P.todo_all()
    except Exception:
        ptodo = {}
    items = []
    for w in words:
        f = V.folder_of(w)
        ts, plan = pl.get(f) or ("", None)
        pm = _pic_mtime(w)
        r = res.get(f) or {}
        st = "none" if not plan else ("stale" if pm and ts and pm > ts else "ok")
        n = sum(len(sc.get("segs") or []) for sc in ((plan or {}).get("scenes") or {}).values())
        # 讲稿：总表改过（比写讲稿的时候新）要重写
        ss = "none" if not plan else ("stale" if tm and ts and tm > ts else "ok")
        say = [{"sec": sid, "name": SEC.BY_ID[sid]["name"], "lines": SEC.plan_lines(sid, plan)} for sid in SAY_SECS]
        say = [x for x in say if x["lines"]]
        # 定稿：要有画面；这份稿是带着画面写的才算（在这里写的记着有没有画面；做画面、出片准备时写的都带画面）
        mine = bool(r.get("ts")) and (not ts or r.get("ts", "") >= ts)
        full = bool(plan) and (r.get("pic", True) if mine else bool(pm))
        line = r.get("line", "") if mine else (ptodo.get(w) or "")
        todo = _todo(line) if (r.get("rc") in (0, None) or not mine) else []
        if not pm:
            fs = "nopic"
        elif not full:
            fs = "none"
        elif ts and pm > ts:
            fs = "stale"
        elif mine and r.get("rc") not in (0, None):
            fs = "err"
        else:
            fs = "fix" if todo else "ok"
        items.append({"word": w, "status": st, "ts": ts, "pic": bool(pm), "picTs": pm, "segs": n,
                      "line": r.get("line", ""), "rc": r.get("rc"), "rts": r.get("ts", ""),
                      "sstatus": ss, "say": say, "tableTs": tm, "fstatus": fs, "todo": todo, "mine": mine})
    order = {"none": 0, "stale": 1, "ok": 2}
    items.sort(key=lambda x: order[x["status"]])
    with _LOCK:
        st = {k: v for k, v in ST.items() if k != "log"}
    return {"ok": True, "items": items, "run": st}


# v1.38.0：每一步先打一行 “@@S 步骤 说明”，做完打 “@@D 步骤 结果”；视频技能 run.py 的输出一行一行交给软件，软件照着写成“过程”
SH = r""". ~/lwb/scripts/wsl/bcommon.sh >/dev/null 2>&1
set +o pipefail
st() { echo "@@S $1 ${*:2}"; }; dn() { echo "@@D $1 ${*:2}"; }; sk() { echo "@@K $1 ${*:2}"; }
st prep 找总表、音节表、视频技能
[ -f "${TABLE:-}" ] && [ -f "${SYL:-}" ] || { echo "@@ERR 没找到总表或音节表：先在「检测」页点「一键修复」同步"; exit 0; }
cd "$S/scripts" 2>/dev/null || { echo "@@ERR 视频技能不在 WSL 里：先在「检测」页点「一键修复」同步"; exit 0; }
dn prep "总表 $(basename "$TABLE")；视频技能 $(grep -m1 '^当前' "$S/SKILL.md" 2>/dev/null | sed 's/（.*//; s/^当前 *//')"
w=%(f)s; word="${w//_/ }"; J=$JOBS/$w
mkdir -p "$WORK/$w" "$J" "$HOME/wordfilm-out/draft"; ln -sfn "$WORK/$w" "$J/$w"
E=""
st kit 拿仓库里最新的画面设置
[ -d %(src)s ] && { cp -r %(src)s/. ~/kit-extra/ 2>/dev/null; find ~/kit-extra -name '*.py' -exec sed -i 's/\r$//' {} + 2>/dev/null; }
if wp=$(kitfile "words/$w.py"); then
  dn kit "有这个词的画面设置（$(date -r "${wp%%.py}.json" '+%%m-%%d %%H:%%M' 2>/dev/null || echo 视频技能自带)）"
  A="$WORK/$w/art"; ERR="$J/draft_art.err"
  st art 把这个词要用的图画出来：背景、会动的人物、AI 画的插图
  rm -rf "$A"; mkdir -p "$A"; cp "$S/references/scenes/"*.svg "$A/" 2>/dev/null; nb=$(ls "$A" | wc -l)
  python3 poses.py "$A" --motion >/dev/null 2>"$ERR"; np=$(( $(ls "$A" | wc -l) - nb ))
  ok=1
  if ap=$(kitfile "${w}ai_art.py"); then python3 "$ap" "$A" >/dev/null 2>>"$ERR" || ok=0; fi
  na=$(( $(ls "$A" | wc -l) - nb - np ))
  [ $ok = 1 ] || { echo "@@F art 画图的程序出错：$(tail -3 "$ERR" | tr '\n' ' ')"; printf '@@%%s 9 有画面\n' "$w"; echo "画面设置的程序跑不起来：$(tail -3 "$ERR" | tr '\n' ' ')"; exit 0; }
  dn art "这个词 AI 画的插图 $na 张；现成的背景 $nb 张、会动的人物动作 $np 张"
  st edits 读画面设置
  python3 "$wp" "$WORK/edits_$w.json" >/dev/null 2>>"$ERR" \
    || { echo "@@F edits 读不了：$(tail -3 "$ERR" | tr '\n' ' ')"; printf '@@%%s 9 有画面\n' "$w"; echo "画面设置的程序跑不起来：$(tail -3 "$ERR" | tr '\n' ' ')"; exit 0; }
  dn edits "$(python3 - "$WORK/edits_$w.json" <<'PY' 2>/dev/null
import json, sys
d = json.load(open(sys.argv[1], encoding='utf-8')); P = next(iter(d.values())) if d else {}
pics = P.get('pics') or []; out = []
if pics: out.append('意思 %%d 幅画' %% len(pics))
ex = sum(1 for x in pics if isinstance(x, dict) and x.get('ex'))
if ex: out.append('例句 %%d 句' %% ex)
if P.get('partPics') or P.get('icons'): out.append('词根词缀卡的画')
if P.get('comboPic'): out.append('拼起来的画')
if P.get('flow'): out.append('演变 %%d 步' %% len(P['flow']) if isinstance(P['flow'], list) else '演变')
if P.get('distinguish'): out.append('同义词辨析')
if (P.get('lianxi') or {}).get('qs'): out.append('练习题 %%d 道' %% len(P['lianxi']['qs']))
print('、'.join(out) or '（里面没什么东西）')
PY
)"
  E="--edits $WORK/edits_$w.json"
else
  dn kit "这个词还没做画面"
  sk art "没有画面设置：不画图，只写总表来的几块"
fi
st write 视频技能按总表和画面设置，一幕一幕写要念的话
python3 run.py --table "$TABLE" --syl "$SYL" --words "$word" --number 1 --out "$HOME/wordfilm-out/draft" $E \
    --edition brief --draft-only --no-preview --redraft --work "$J" 2>&1 | tee "$J/draft.log" | sed -u 's/^/@@L /'
rc=${PIPESTATUS[0]}
printf '@@%%s %%s %%s\n' "$w" "$rc" "$([ -n "$E" ] && echo 有画面 || echo 没画面)"
grep -a '还要补' "$J/draft.log" | tail -1 | sed 's/^ *//'
[ $rc = 0 ] || tail -4 "$J/draft.log"
"""

STEP_NAME = {"prep": "准备", "kit": "画面设置", "art": "画图", "edits": "读画面设置", "write": "写配音稿", "check": "起草检查"}
_SCENE_BLK = {k: sid for sid, ks in SEC.SCENE_OF.items() for k in ks}
_SCENE_BLK.update({"title": "", "daan": "lianxi"})


class _Proc:
    """一个词的过程：几步，每一步的状态、用时、细节（像 Claude 做事时列出来的那样）"""

    def __init__(self, word):
        self.w = {"word": word, "status": "run", "t0": time.time(), "t1": 0, "steps": [], "result": "", "todo": []}
        self.phase = "write"

    def step(self, key, title):
        now = time.time()
        for x in self.w["steps"]:
            if x["status"] == "run":
                x["status"], x["t1"] = "ok", now
        x = {"key": key, "name": STEP_NAME.get(key, key), "title": title, "status": "run", "t0": now, "t1": 0, "detail": []}
        self.w["steps"].append(x)
        return x

    def cur(self, key=None):
        for x in reversed(self.w["steps"]):
            if key is None or x["key"] == key:
                return x
        return self.step(key or "write", "")

    def done(self, key, text, status="ok"):
        x = self.cur(key)
        x["status"], x["t1"] = status, time.time()
        if text:
            x["result"] = text

    def feed(self, line):
        if line.startswith("@@S "):
            k, _, t = line[4:].partition(" ")
            self.step(k, t)
        elif line.startswith("@@D "):
            k, _, t = line[4:].partition(" ")
            self.done(k, t)
        elif line.startswith("@@K "):
            k, _, t = line[4:].partition(" ")
            self.step(k, t)
            self.done(k, "", "skip")
        elif line.startswith("@@F "):
            k, _, t = line[4:].partition(" ")
            self.done(k, t, "err")
        elif line.startswith("@@L "):
            self._run_line(line[4:])

    def _run_line(self, l):
        """视频技能 run.py 起草时打出来的话 → 写配音稿、起草检查两步里的细节"""
        s = l.rstrip()
        if not s.strip() or s.startswith("====") or "edits_template" in s or s.startswith("读音拆分用："):
            return
        if s.startswith("找到 "):
            self.cur("write")["detail"].append("在总表里" + s.split("：")[0])
            return
        m = re.match(r"^起草好了 \S+（(.*?)）", s)
        if m:
            self.cur("write")["result"] = "写好了：" + m.group(1)
            return
        m = re.match(r"^  ([a-z]+?)(\d*)\s+(.*)$", s)
        if m and self.phase == "write":
            sid = _SCENE_BLK.get(m.group(1), "")
            name = {"title": "片头", "daan": "答案", "lianxi": "练习"}.get(m.group(1)) or ((SEC.BY_ID.get(sid) or {}).get("name", "") if sid else "")
            self.cur("write")["detail"].append(("【%s】" % name if name else "") + m.group(3).strip())
            return
        if s.startswith("  ") and "：" in s and self.phase == "write":
            self.done("write", self.cur("write").get("result", ""))
            self.phase = "check"
            self.step("check", "对一遍：画和话对不对得上、还缺什么")
        if self.phase == "check":
            t = s.strip()
            if t.startswith("还要补"):
                self.cur("check")["result"] = t
            elif not re.search(r"/root/|/home/|plan\.json", t):
                self.cur("check")["detail"].append(t)
            return
        if s.startswith("读音拆分：") or s.startswith("提醒：") or s.startswith("⚠"):
            self.cur("write")["detail"].append(s.strip())

    def finish(self, status, result, todo):
        now = time.time()
        for x in self.w["steps"]:
            if x["status"] == "run":
                x["status"], x["t1"] = ("ok" if status in ("ok", "fix") else "err"), now
        self.w.update(status=status, t1=now, result=result, todo=todo)


def _run(words):
    res = _res_load()
    try:
        for w in words:
            with _LOCK:
                if ST["stop"]:
                    ST["msg"] = "停了：写了 %d 个" % ST["done"]
                    break
                ST["cur"] = w
                pr = _Proc(w)
                ST["log"].append(pr.w)
            f = V.folder_of(w)
            out = []
            up = ST.get("from") == "upgrade"
            if up:                                     # v1.46.0：按新技能更新——先记下原来的讲稿，写完比一比改了哪几句
                SEC._PL.pop(f, None)
                try:
                    old_plan = SEC.plans([w]).get(f, ("", None))[1]
                except Exception:
                    old_plan = None

            def on_line(l):
                out.append(l)
                with _LOCK:
                    pr.feed(l)
            rc, _ = V.wsl_stream(SH % {"f": V.q(f), "src": V.q(V.to_wsl(C.REPO / V.EXTRA))}, on_line, 300)
            out = [l for l in out if not l.startswith("@@L ") and not l[:4] in ("@@S ", "@@D ", "@@K ", "@@F ")]
            txt = "\n".join(out)
            if "@@ERR" in txt:
                m = txt.split("@@ERR", 1)[1].strip().splitlines()[0]
                with _LOCK:
                    ST["msg"] = m
                    pr.finish("err", m, [])
                break
            i = next((k for k, l in enumerate(out) if l.startswith("@@")), None)
            parts = out[i][2:].split() if i is not None else []
            rest = out[i + 1:] if i is not None else out
            code = int(parts[1]) if len(parts) > 1 and parts[1].lstrip("-").isdigit() else rc
            line = (rest[0] if rest else "") if code == 0 else ("出错：" + " ".join(rest[-3:])[:300])
            pv = next((x.get("result", "") for x in pr.w["steps"] if x["key"] == "prep"), "")
            m = re.search(r"视频技能 (\d+\.\d+\.\d+)", pv)
            res[f] = {"ts": time.strftime("%Y-%m-%d %H:%M"), "rc": code, "line": line[:1500],
                      "pic": len(parts) > 2 and parts[2] == "有画面", "ver": m.group(1) if m else ""}     # v1.41.0：用的哪一版视频技能
            _RES().write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
            SEC._PL.pop(f, None)                      # 配音稿换了，下次重读
            todo = _todo(line) if code == 0 else []
            if up and code == 0:      # v1.42.0：按新技能更新的第 ① 步
                try:
                    import film
                    SEC._PL.pop(f, None)
                    try:
                        new_plan = SEC.plans([w]).get(f, ("", None))[1]
                    except Exception:
                        new_plan = None
                    film.stamp(w, line, res[f].get("ver", ""), old_plan, new_plan)
                except Exception as e:
                    C.log("按新技能更新：%s 记版本没成功（%s）" % (w, str(e)[:120]))
            with _LOCK:
                pr.finish("err" if code else ("fix" if todo else "ok"), line, todo)
                ST["done"] += 1
        else:
            with _LOCK:
                ST["msg"] = "写好了 %d 个词" % ST["done"]
    except Exception as e:
        with _LOCK:
            ST["msg"] = "起草出错：%s" % str(e)[:200]
    finally:
        with _LOCK:
            ST["running"], ST["cur"] = False, ""
            for x in ST["log"]:
                if x["status"] == "run":
                    x["status"], x["t1"] = "err", time.time()
        C.log("起草配音稿：%s" % ST["msg"])


def proc():
    """v1.38.0：这一次（或上一次）写配音稿的过程，界面一秒左右来问一次"""
    with _LOCK:
        st = {k: v for k, v in ST.items() if k != "log"}
        st["log"] = json.loads(json.dumps(ST["log"], ensure_ascii=False))
    st["now"] = time.time()
    return {"ok": True, "run": st}


def start(words, frm=""):
    words = [w for w in (words or []) if isinstance(w, str) and w.strip()]
    if not words:
        return {"ok": False, "msg": "一个都没选"}
    if not V.has_wsl():
        return {"ok": False, "msg": "这台电脑没有 WSL：起草要在 WSL 里跑视频技能"}
    with _LOCK:
        if ST["running"]:
            return {"ok": False, "msg": "正在写配音稿（%d / %d）：等它做完，或者先点「停」" % (ST["done"], ST["total"])}
        ST.update(running=True, stop=False, done=0, total=len(words), cur="", started=time.time(), msg="", log=[], **({"from": frm} if frm else {}))
    threading.Thread(target=_run, args=(words,), daemon=True).start()
    return {"ok": True, "msg": "开始写 %d 个词的配音稿（不用 AI，在 WSL 里跑，一个词几秒到十几秒）" % len(words)}


def stop():
    with _LOCK:
        if not ST["running"]:
            return {"ok": False, "msg": "没有在起草"}
        ST["stop"] = True
    return {"ok": True, "msg": "做完手上这一个就停"}
