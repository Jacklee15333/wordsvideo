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
import threading
import time

import core as C
import video as V
import sections as SEC

ST = {"running": False, "stop": False, "done": 0, "total": 0, "cur": "", "started": 0.0, "msg": ""}
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


def status():
    words = SEC._picked()
    try:
        pl = SEC.plans(words)
    except Exception:
        pl = {}
    res = _res_load()
    items = []
    for w in words:
        f = V.folder_of(w)
        ts, plan = pl.get(f) or ("", None)
        pm = _pic_mtime(w)
        r = res.get(f) or {}
        st = "none" if not plan else ("stale" if pm and ts and pm > ts else "ok")
        n = sum(len(sc.get("segs") or []) for sc in ((plan or {}).get("scenes") or {}).values())
        items.append({"word": w, "status": st, "ts": ts, "pic": bool(pm), "picTs": pm, "segs": n,
                      "line": r.get("line", ""), "rc": r.get("rc"), "rts": r.get("ts", "")})
    order = {"none": 0, "stale": 1, "ok": 2}
    items.sort(key=lambda x: order[x["status"]])
    with _LOCK:
        st = dict(ST)
    return {"ok": True, "items": items, "run": st}


SH = r""". ~/lwb/scripts/wsl/bcommon.sh >/dev/null 2>&1
set +o pipefail
[ -f "${TABLE:-}" ] && [ -f "${SYL:-}" ] || { echo "@@ERR 没找到总表或音节表：先在「检测」页点「一键修复」同步"; exit 0; }
cd "$S/scripts" 2>/dev/null || { echo "@@ERR 视频技能不在 WSL 里：先在「检测」页点「一键修复」同步"; exit 0; }
w=%(f)s; word="${w//_/ }"; J=$JOBS/$w
mkdir -p "$WORK/$w" "$J" "$HOME/wordfilm-out/draft"; ln -sfn "$WORK/$w" "$J/$w"
E=""
if wp=$(kitfile "words/$w.py"); then python3 "$wp" "$WORK/edits_$w.json" >/dev/null 2>&1 && E="--edits $WORK/edits_$w.json"; fi
python3 run.py --table "$TABLE" --syl "$SYL" --words "$word" --number 1 --out "$HOME/wordfilm-out/draft" $E \
    --edition brief --draft-only --no-preview --redraft --work "$J" > "$J/draft.log" 2>&1
rc=$?
printf '@@%%s %%s %%s\n' "$w" "$rc" "$([ -n "$E" ] && echo 有画面 || echo 没画面)"
grep -a '还要补' "$J/draft.log" | tail -1 | sed 's/^ *//'
[ $rc = 0 ] || tail -4 "$J/draft.log"
"""


def _run(words):
    res = _res_load()
    try:
        for w in words:
            with _LOCK:
                if ST["stop"]:
                    ST["msg"] = "停了：起草了 %d 个" % ST["done"]
                    break
                ST["cur"] = w
            f = V.folder_of(w)
            rc, out = V.wsl(SH % {"f": V.q(f)}, 300)
            if "@@ERR" in out:
                with _LOCK:
                    ST["msg"] = out.split("@@ERR", 1)[1].strip().splitlines()[0]
                break
            lines = out.splitlines()
            i = next((k for k, l in enumerate(lines) if l.startswith("@@")), None)
            parts = lines[i][2:].split() if i is not None else []
            rest = lines[i + 1:] if i is not None else lines
            code = int(parts[1]) if len(parts) > 1 and parts[1].lstrip("-").isdigit() else rc
            line = (rest[0] if rest else "") if code == 0 else ("起草出错：" + " ".join(rest[-3:])[:300])
            res[f] = {"ts": time.strftime("%Y-%m-%d %H:%M"), "rc": code, "line": line[:1500]}
            _RES().write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
            SEC._PL.pop(f, None)                      # 配音稿换了，下次重读
            with _LOCK:
                ST["done"] += 1
        else:
            with _LOCK:
                ST["msg"] = "起草好了 %d 个词" % ST["done"]
    except Exception as e:
        with _LOCK:
            ST["msg"] = "起草出错：%s" % str(e)[:200]
    finally:
        with _LOCK:
            ST["running"], ST["cur"] = False, ""
        C.log("起草配音稿：%s" % ST["msg"])


def start(words):
    words = [w for w in (words or []) if isinstance(w, str) and w.strip()]
    if not words:
        return {"ok": False, "msg": "一个都没选"}
    if not V.has_wsl():
        return {"ok": False, "msg": "这台电脑没有 WSL：起草要在 WSL 里跑视频技能"}
    with _LOCK:
        if ST["running"]:
            return {"ok": False, "msg": "正在起草（%d / %d）：等它做完，或者先点「停」" % (ST["done"], ST["total"])}
        ST.update(running=True, stop=False, done=0, total=len(words), cur="", started=time.time(), msg="")
    threading.Thread(target=_run, args=(words,), daemon=True).start()
    return {"ok": True, "msg": "开始起草 %d 个词的配音稿（不用 AI，在 WSL 里跑，一个词几秒到十几秒）" % len(words)}


def stop():
    with _LOCK:
        if not ST["running"]:
            return {"ok": False, "msg": "没有在起草"}
        ST["stop"] = True
    return {"ok": True, "msg": "做完手上这一个就停"}
