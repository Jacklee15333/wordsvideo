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
