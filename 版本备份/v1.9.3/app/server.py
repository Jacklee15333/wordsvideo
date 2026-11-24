# -*- coding: utf-8 -*-
"""单词工作台 · 本地服务。双击「启动.bat」运行；界面在 http://127.0.0.1:8766 。"""
import json, os, re, sys, threading, time, traceback, urllib.parse, webbrowser
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    sys.stderr.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
except Exception:
    pass
sys.path.insert(0, str(Path(__file__).resolve().parent))
import core as C
import video as V
import selfup as SU

WEB = Path(__file__).resolve().parent / "web"
MIME = {".html": "text/html; charset=utf-8", ".js": "application/javascript; charset=utf-8",
        ".css": "text/css; charset=utf-8", ".png": "image/png", ".svg": "image/svg+xml", ".ico": "image/x-icon"}


def wm():
    try:
        import web_model
        return web_model
    except Exception:
        return None


def prepare_repo():
    try:
        C.ensure_repo()
        C.log("仓库就绪：%s，总表 %s" % (C.STATE.get("head"), C.STATE.get("version")))
        C.RUNNER.wake.set()
    except Exception as e:
        if C.STATE.get("repo") != "等令牌":
            C.STATE["repo"] = "出错"
        C.STATE["repoError"] = str(e)
        C.log("仓库没准备好：%s" % e)


def repo_watch():
    """仓库出错（多半是网络）或离线时，每 3 分钟自己再试一次。"""
    while True:
        time.sleep(180)
        if C.RUNNER.task:
            continue
        if C.STATE.get("repo") == "出错" or C.STATE.get("offline"):
            C.log("再试一次连 GitHub…")
            prepare_repo()


# ═══════════════════════ API ═══════════════════════
def api_status(qs):
    r = C.RUNNER
    t = r.task
    cur = None
    if t:
        cur = C.q("SELECT * FROM tasks WHERE id=?", (t["id"],), one=True)
    s = {}
    try:
        s = C.stats()
    except Exception as e:
        s = {"error": str(e)}
    cfg = C.load_cfg()
    return {"repo": C.STATE, "stats": s, "runner": {"state": r.state, "stage": r.stage, "task": cur},
            "pending": C.pending_changes() if C.STATE.get("repo") == "就绪" else 0,
            "provider": cfg.get("provider"), "window": cfg.get("window"), "inWindow": C.in_window(cfg),
            "logs": C.live_logs(60), "now": C.now(), "version": SU.version(),
            "newer": (UPD["info"] or {}).get("remote") if (UPD["info"] or {}).get("newer") else ""}


def api_settings_get(qs):
    c = C.load_cfg()
    c["githubToken"] = "（已填）" if c.get("githubToken") else ""
    c["api"] = dict(c["api"], key="（已填）" if c["api"].get("key") else "")
    c["relayInbox"] = dict(C.inbox_cfg(c), token="（已填）" if C.inbox_cfg(c)["token"] else "")
    w = {}
    m = wm()
    if m:
        wc = m.load_config()
        w = {k: wc.get(k) for k in ("aiUsername", "sitePath", "serviceName", "browserHidden", "headless",
                                    "preferredModel", "aiPoolProxy", "newTaskMode")}
        w["aiPassword"] = "（已填）" if wc.get("aiPassword") else ""
        w["playwright"] = bool(m.is_available())
    return {"cfg": c, "web": w}


def api_settings_post(b):
    cfg = b.get("cfg") or {}
    if cfg.get("githubToken") in ("（已填）",):
        cfg.pop("githubToken")
    if isinstance(cfg.get("api"), dict) and cfg["api"].get("key") == "（已填）":
        cfg["api"].pop("key")
    if isinstance(cfg.get("relayInbox"), dict) and cfg["relayInbox"].get("token") in ("（已填）", None):
        cfg["relayInbox"].pop("token", None)
    C.save_cfg(cfg)
    web = b.get("web") or {}
    m = wm()
    if m and web:
        web = {k: v for k, v in web.items() if k != "playwright"}
        if web.get("aiPassword") in ("（已填）", None):
            web.pop("aiPassword", None)
        m.save_config(web)
    C.RUNNER.wake.set()
    if C.STATE.get("repo") in ("出错", "等令牌", "未准备"):
        C.STATE["repo"], C.STATE["repoError"] = "正在克隆仓库", ""
        threading.Thread(target=prepare_repo, daemon=True).start()
    return {"ok": True}


def api_tasks(qs):
    return {"tasks": C.q("SELECT * FROM tasks ORDER BY CASE status WHEN '运行中' THEN 0 WHEN '排队' THEN 1 "
                         "WHEN '已暂停' THEN 2 ELSE 3 END, id DESC LIMIT 200"),
            "schedules": C.q("SELECT * FROM schedules ORDER BY at")}


def api_task_add(b):
    kind = b.get("kind", "chuti")
    params = b.get("params") or {}
    ra = 0
    if b.get("runAt"):
        ra = time.mktime(time.strptime(b["runAt"].replace("T", " ")[:16], "%Y-%m-%d %H:%M"))
    tid = C.add_task(kind, params, ra)
    C.RUNNER.wake.set()
    return {"id": tid}


def api_task_op(b):
    tid, op = int(b["id"]), b["op"]
    t = C.q("SELECT * FROM tasks WHERE id=?", (tid,), one=True)
    if not t:
        return {"error": "没有这个任务"}
    running = C.RUNNER.task and C.RUNNER.task["id"] == tid
    if op in ("pause", "cancel"):
        if running:
            C.RUNNER.request_stop(op)
        elif t["status"] in ("排队", "已暂停", "失败"):
            C.x("UPDATE tasks SET status=? WHERE id=?", ("已暂停" if op == "pause" else "已取消", tid))
    elif op == "resume":
        C.x("UPDATE tasks SET status='排队', run_after=0 WHERE id=?", (tid,))
    elif op == "delete" and not running:
        C.x("DELETE FROM tasks WHERE id=?", (tid,))
    C.RUNNER.wake.set()
    return {"ok": True}


def api_sched(b):
    op = b.get("op")
    if op == "delete":
        C.x("DELETE FROM schedules WHERE id=?", (int(b["id"]),))
    elif op == "toggle":
        C.x("UPDATE schedules SET enabled=1-enabled WHERE id=?", (int(b["id"]),))
    else:
        C.x("INSERT INTO schedules(name,kind,params,at,days,enabled) VALUES(?,?,?,?,?,1)",
            (b.get("name", ""), b.get("kind", "chuti"), json.dumps(b.get("params") or {}, ensure_ascii=False),
             b.get("at", "23:00"), b.get("days", "1234567")))
    return {"ok": True}


def api_logs(qs):
    tid = qs.get("task")
    if tid:
        return {"logs": C.q("SELECT ts,msg FROM logs WHERE task_id=? ORDER BY id DESC LIMIT 400", (int(tid),))}
    return {"logs": C.q("SELECT ts,msg,task_id FROM logs ORDER BY id DESC LIMIT 400")}


def api_word(qs):
    d = C.word_detail(qs.get("w", ""))
    return d or {"error": "索引里没有这个词"}


def api_word_check(b):
    w = b["word"]
    lines = [l.strip() for l in (b.get("draft") or "").split("\n") if l.strip() and not l.strip().startswith("@")]
    qs_, errs = C.check(w, lines)
    if errs or not b.get("save"):
        if errs and C.q("SELECT 1 FROM manual WHERE word=?", (w,), one=True):
            C.x("UPDATE manual SET draft=?, errors=? WHERE word=?",
                ("\n".join(lines), json.dumps(errs, ensure_ascii=False), w))
        return {"ok": not errs, "errors": errs}
    C.save_word(w, qs_, C.STATE["version"], "人工（单词工作台）")
    C.log("人工保存了 %s（还没上传，点「上传」或等下一组出题时一起传）" % w)
    return {"ok": True, "saved": True}


def api_manual(b):
    op, words = b.get("op"), b.get("words") or []
    if op == "add":
        for w in words:
            C.x("INSERT OR IGNORE INTO manual(word,errors,draft,attempts,ts,source) VALUES(?,?,?,?,?,?)",
                (w, "[]", "", 0, C.now(), "人工标记"))
    elif op == "remove":
        for w in words:
            C.x("DELETE FROM manual WHERE word=?", (w,))
    elif op == "redo":
        C.add_task("redo", {"words": words})
        C.RUNNER.wake.set()
    return {"ok": True}


def api_ai(b):
    op = b.get("op")
    m = wm()
    if not m:
        return {"ok": False, "msg": "web_model 加载失败"}
    if op in ("show", "hide"):
        ok, msg = m.request_window(op)
        return {"ok": ok, "msg": msg}
    if op == "test":
        r = m.test_login()
        return {"ok": bool(r.get("ok")), "msg": r.get("error") or r.get("reply") or json.dumps(r, ensure_ascii=False)[:300]}
    if op == "probe":
        ok, msg = m.probe_pool()
        return {"ok": ok, "msg": msg}
    return {"ok": False, "msg": "不认识的操作"}


def api_ai_live(qs):
    m = wm()
    if not m or C.load_cfg().get("provider") != "web":
        return {"state": "off"}
    try:
        d = m.live_state(watch=qs.get("watch") == "1")
        d.pop("log", None)
        return d
    except Exception as e:
        return {"state": "error", "error": str(e)}


def api_repo(b):
    op = b.get("op")
    if op == "sync":
        C.add_task("sync")
    elif op == "push":
        C.add_task("push")
    elif op == "reclone":
        if C.RUNNER.task:
            return {"ok": False, "msg": "有任务在跑，先停掉"}
        with C.REPO_LOCK:
            try:
                C.rmtree(C.REPO)
                (C.DATA / "repo_ok").unlink(missing_ok=True)
            except Exception as e:
                return {"ok": False, "msg": str(e)}
            C.STATE.update(repo="正在克隆仓库", xlsx="", repoError="")
        threading.Thread(target=prepare_repo, daemon=True).start()
    elif op == "token":
        ok, msg = C.check_token()
        return {"ok": ok, "msg": msg}
    elif op == "inbox":
        ok, msg = C.check_inbox()
        return {"ok": ok, "msg": msg}
    C.RUNNER.wake.set()
    return {"ok": True}


# ═══════════════════════ 视频 ═══════════════════════
def api_video_get(qs):
    what = qs.get("what")
    if what == "env":
        return V.env_status()
    if what == "batches":
        return {"items": V.batch_list()}
    if what == "setup":
        return {"text": V.setup_status(qs.get("step", "boot"))}
    if what == "words":
        pw, vd = V.pic_words(), V.videos()
        idx = {}
        try:
            _, rows = C.read_index()
            idx = {V.folder_of(r[2]): r for r in rows}
        except Exception:
            pass
        items = [{"word": idx[w][2] if w in idx else w, "folder": w, "inTable": w in idx, "video": vd.get(w),
                  "meaning": idx[w][3] if w in idx else ""} for w in sorted(pw)]
        return {"items": items, "videos": list(vd.values()), "nPic": len(pw), "nVideo": len(vd)}
    return {"error": "不认识"}


def api_video_post(b):
    op = b.get("op")
    if op == "sync":
        ok, t = V.sync_engine()
    elif op == "setup":
        ok, t = V.setup_start(b.get("step"), b.get("proxy", ""))
    elif op == "new":
        words = [w.strip() for w in re.split(r"[,，、\n]+", b.get("words") or "") if w.strip()]
        ok, t = V.batch_new(b.get("name", "").strip(), words)
    elif op == "batch":
        ok, t = V.batch_op(b.get("name", ""), b.get("action", ""), b.get("word", ""), b.get("stage", ""))
    elif op == "scan":
        n = V.scan_videos()
        ok, t = True, "新登记了 %d 个视频" % n
    elif op == "keepalive":
        V.keepalive()
        ok, t = True, "开了"
    else:
        return {"ok": False, "msg": "不认识的操作"}
    return {"ok": ok, "msg": C.mask(t)}


def video_file(handler, qs):
    root = Path(V.vcfg()["winDir"]).resolve()
    p = (root / qs.get("p", "")).resolve()
    if root not in p.parents or not p.is_file():
        return handler._send(404, {"error": "没有这个文件"})
    ct = {".jpg": "image/jpeg", ".png": "image/png", ".mp4": "video/mp4"}.get(p.suffix.lower(), "application/octet-stream")
    if p.suffix.lower() == ".mp4":                         # 视频大：分段读，浏览器能拖进度条
        size = p.stat().st_size
        rng = handler.headers.get("Range")
        a, z = 0, size - 1
        if rng:
            m = re.match(r"bytes=(\d*)-(\d*)", rng)
            if m:
                a = int(m.group(1) or 0); z = int(m.group(2) or z)
        z = min(z, a + 8 * 1024 * 1024 - 1, size - 1)
        with open(p, "rb") as f:
            f.seek(a); data = f.read(z - a + 1)
        handler.send_response(206 if rng else 200)
        handler.send_header("Content-Type", ct); handler.send_header("Accept-Ranges", "bytes")
        handler.send_header("Content-Range", "bytes %d-%d/%d" % (a, z, size)); handler.send_header("Content-Length", str(len(data)))
        handler.end_headers(); handler.wfile.write(data)
        return
    return handler._send(200, p.read_bytes(), ct)


# ═══════════════════════ 软件：版本、更新、改写 ═══════════════════════
UPD = {"info": None, "at": 0}


def check_update_bg():
    try:
        UPD["info"], UPD["at"] = SU.check_update(), time.time()
        if UPD["info"].get("newer"):
            C.log("有新版本 v%s（现在 v%s）：到「软件」页点「更新」" % (UPD["info"]["remote"], UPD["info"]["local"]))
    except Exception as e:
        C.log("检查更新出错：%s" % e)


def api_self_get(qs):
    if qs.get("check"):
        check_update_bg()
    p = SU.ROOT / "CHANGELOG.md"
    return {"version": SU.version(), "clone": SU.is_clone(), "update": UPD["info"], "backups": SU.backups(),
            "changelog": p.read_text(encoding="utf-8")[:20000] if p.exists() else "",
            "changes": C.q("SELECT id,request,status,files,notes,error,ts,task_id FROM changes ORDER BY id DESC LIMIT 50"),
            "files": SU.app_files()}


def api_self_post(b):
    op = b.get("op")
    if op == "request":
        text = (b.get("text") or "").strip()
        if len(text) < 4:
            return {"ok": False, "msg": "先写清楚要改什么"}
        cid = C.x("INSERT INTO changes(request,status,ts) VALUES(?,?,?)", (text, "排队", C.now()))
        tid = C.add_task("selfedit", {"change": cid, "files": b.get("files") or []}, title="改软件：" + text.split("\n")[0][:30])
        C.x("UPDATE changes SET task_id=? WHERE id=?", (tid, cid))
        C.RUNNER.wake.set()
        return {"ok": True, "msg": "交给 AI 了（任务 #%d），改好会出现在下面，等你确认" % tid}
    if op == "apply":
        ok, msg = SU.apply_change(int(b["id"]))
    elif op == "discard":
        C.x("UPDATE changes SET status='放弃了' WHERE id=?", (int(b["id"]),))
        ok, msg = True, "放弃了"
    elif op == "update":
        ok, msg = SU.update()
    elif op == "rollback":
        ok, msg = SU.rollback(b.get("name", ""))
    else:
        return {"ok": False, "msg": "不认识的操作"}
    if ok:
        threading.Thread(target=check_update_bg, daemon=True).start()
    return {"ok": ok, "msg": C.mask(msg)}


def api_live(qs):
    """任务页的实时画面：现在在做哪个任务、哪一步、AI 正在写什么、浏览器画面、步骤记录。"""
    r = C.RUNNER
    t = r.task
    cfg = C.load_cfg()
    out = {"relay": C.RELAY.get("status") == "等你操作", "running": bool(t), "provider": C.provider_name(), "pv": cfg.get("provider"),
           "relayUrl": cfg.get("relayUrl", ""), "inbox": C.inbox_on(cfg), "stage": r.stage,
           "state": r.state, "ai": {k: v for k, v in C.AI_LIVE.items()}, "web": None, "logs": []}
    if t:
        out["task"] = C.q("SELECT id,title,kind,progress,started FROM tasks WHERE id=?", (t["id"],), one=True)
        out["logs"] = [l for l in C.live_logs(300) if l.get("task") == t["id"]][-60:]
    out["ai"]["reply"] = (out["ai"].get("reply") or "")[-6000:]
    if out["pv"] == "web":
        m = wm()
        if m:
            try:
                d = m.live_state(watch=qs.get("watch") == "1")
                d.pop("log", None)
                out["web"] = d
            except Exception as e:
                out["web"] = {"error": str(e)}
    return out


def api_relay_get(qs):
    r = dict(C.RELAY)
    if qs.get("full") != "1":
        r["promptLen"] = len(r.get("prompt") or "")
        r["prompt"] = (r.get("prompt") or "")[:600]
    r.pop("reply", None)
    r["url"] = C.load_cfg().get("relayUrl", "")
    return r


def api_open(b):
    """用你平时的浏览器打开网页 AI。软件自己的窗口用的是单独的浏览器资料夹，在那里打开没登录 zd87。"""
    url = (C.load_cfg().get("relayUrl") or "").strip()
    if not re.match(r"^https?://", url):
        return {"ok": False, "msg": "网页 AI 地址要以 http:// 或 https:// 开头：任务页「⚙ 设置」里改"}
    try:
        if sys.platform == "win32":
            os.startfile(url)
        else:
            webbrowser.open(url, new=2)
        return {"ok": True, "msg": "已经用你平时的浏览器打开 " + url}
    except Exception as e:
        return {"ok": False, "msg": "没打开（%s）：请把地址复制到浏览器 %s" % (str(e)[:80], url)}


def api_relay_post(b):
    ok, msg = C.relay_submit(b.get("id", 0), b.get("reply", ""), skip=bool(b.get("skip")))
    return {"ok": ok, "msg": msg}


def next_unready(n):
    """按总表（索引）顺序，接下来还没准备好（缺题目或缺画面）的 n 个词；画面做不成、出题没过的先跳过。"""
    pw = V.pic_words()
    skip = {r["word"] for r in C.q("SELECT word FROM picfail")} | set(C.manual_words())
    _, rows = C.read_index()
    out = []
    for r in rows:
        w = r[2]
        if w in out or w in skip:
            continue
        if r[4] in ("细节数据有", "总表有") and V.folder_of(w) in pw:
            continue
        out.append(w)
        if len(out) >= n:
            break
    return out


def api_prep(b):
    """开始页的大按钮：指定的词，或者按总表顺序接着做 n 个，都是出题 → 画面 → 检查一条龙。"""
    if b.get("mode") == "next":
        ws = next_unready(max(1, min(200, int(b.get("n") or 5))))
        if not ws:
            return {"ok": False, "msg": "总表里的词都准备好了"}
        return api_words_task({"text": ",".join(ws), "steps": ["chuti", "pics"]})
    return api_words_task({"text": b.get("text") or "", "steps": ["chuti", "pics"]})


def api_words_task(b):
    raw = b.get("text") or ""
    ws = [w.strip() for w in re.split(r"[\n,，、;；]+", raw) if w.strip()]
    if not ws:
        return {"ok": False, "msg": "先输入单词"}
    _, rows = C.read_index()
    known = {r[2] for r in rows}
    low = {r[2].lower(): r[2] for r in rows}
    found, miss = [], []
    for w in ws:
        k = w if w in known else low.get(w.lower())
        (found if k else miss).append(k or w)
    found = list(dict.fromkeys(found))
    steps = [x for x in (b.get("steps") or []) if x in ("chuti", "pics")]
    if not found:
        return {"ok": False, "msg": "这些词总表里都没有：%s" % "、".join(miss[:20])}
    if not steps:
        return {"ok": False, "msg": "至少勾一步（出题 / 做视频画面）"}
    tid = C.add_task("words", {"words": found, "steps": steps},
                     title="做指定的 %d 个词：%s" % (len(found), "、".join(found[:5]) + ("…" if len(found) > 5 else "")))
    C.RUNNER.wake.set()
    return {"ok": True, "found": len(found), "miss": miss, "task": tid,
            "msg": "开始了（任务 #%d），%d 个词%s" % (tid, len(found), ("；总表里没有、跳过的：" + "、".join(miss[:20])) if miss else "")}


GET = {
    "/api/status": api_status, "/api/settings": api_settings_get, "/api/tasks": api_tasks, "/api/logs": api_logs,
    "/api/word": api_word, "/api/ai/live": api_ai_live,
    "/api/words": lambda qs: C.search_words(qs.get("q", ""), qs.get("status", ""), int(qs.get("page", 1)), ready=qs.get("ready", "")),
    "/api/map": lambda qs: C.word_map(),
    "/api/manual": lambda qs: {"items": C.q("SELECT * FROM manual ORDER BY ts DESC")},
    "/api/picfail": lambda qs: {"items": C.q("SELECT * FROM picfail ORDER BY ts DESC")},
    "/api/groups": lambda qs: {"items": C.q("SELECT * FROM groups ORDER BY id DESC LIMIT 200")},
    "/api/calls": lambda qs: {"items": C.q("SELECT id,task_id,ts,kind,words,secs,ok,error,provider,length(prompt) AS plen,"
                                           "length(reply) AS rlen FROM calls ORDER BY id DESC LIMIT 200")},
    "/api/call": lambda qs: C.q("SELECT * FROM calls WHERE id=?", (int(qs.get("id", 0)),), one=True) or {},
    "/api/issues": lambda qs: {"readme": C.readme_issues(),
                               "mine": [r["text"] for r in C.q("SELECT text FROM issues")]},
    "/api/video": api_video_get,
    "/api/self": api_self_get,
    "/api/live": api_live,
    "/api/relay": api_relay_get,
    "/api/self/change": lambda qs: C.q("SELECT * FROM changes WHERE id=?", (int(qs.get("id", 0)),), one=True) or {},
    "/api/next": lambda qs: {"words": next_unready(int(qs.get("n", 5)))},
    "/api/prompt-preview": lambda qs: {"text": C.build_prompt(C.RUNNER.pick(int(qs.get("n", 3))) or ["make"])},
}
NEED_REPO = {"/api/next", "/api/picfail", "/api/words", "/api/map", "/api/word", "/api/issues", "/api/prompt-preview", "/api/manual"}
POST = {"/api/settings": api_settings_post, "/api/task": api_task_add, "/api/task/op": api_task_op,
        "/api/schedule": api_sched, "/api/word/check": api_word_check, "/api/manual": api_manual,
        "/api/ai": api_ai, "/api/repo": api_repo, "/api/video": api_video_post,
        "/api/self": api_self_post,
        "/api/relay": api_relay_post,
        "/api/open": api_open,
        "/api/words-task": api_words_task,
        "/api/prep": api_prep,
        "/api/prepare": lambda b: C.prepare(b.get("words") or [])}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        if not isinstance(body, (bytes, bytearray)):
            body = json.dumps(body, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        qs = {k: v[0] for k, v in urllib.parse.parse_qs(u.query).items()}
        try:
            if u.path in NEED_REPO and C.STATE.get("repo") not in ("就绪", "索引和总表对不上"):
                return self._send(200, {"notReady": True, "msg": "仓库还没准备好：%s %s" % (
                    C.STATE.get("repo"), C.STATE.get("repoError") or ""), "items": [], "total": 0, "codes": "", "vcodes": "",
                    "words": [], "readme": [], "mine": [], "counts": {}})
            if u.path in GET:
                return self._send(200, GET[u.path](qs))
            if u.path == "/api/video/file":
                return video_file(self, qs)
            if u.path == "/api/ai/shot":
                m = wm()
                data = m.live_shot()[0] if m else b""
                return self._send(200, data or b"", "image/jpeg")
            p = WEB / ("index.html" if u.path in ("/", "") else u.path.lstrip("/"))
            if p.resolve().parent == WEB.resolve() and p.exists():
                return self._send(200, p.read_bytes(), MIME.get(p.suffix, "application/octet-stream"))
            self._send(404, {"error": "没有这个地址"})
        except Exception as e:
            traceback.print_exc()
            self._send(500, {"error": C.mask(str(e))})

    def do_POST(self):
        u = urllib.parse.urlparse(self.path)
        try:
            n = int(self.headers.get("Content-Length") or 0)
            b = json.loads(self.rfile.read(n).decode("utf-8") or "{}") if n else {}
            if u.path in POST:
                return self._send(200, POST[u.path](b))
            self._send(404, {"error": "没有这个地址"})
        except Exception as e:
            traceback.print_exc()
            self._send(500, {"error": C.mask(str(e))})


def open_window(url):
    if os.environ.get("CHUTI_NO_BROWSER"):
        return
    for p in (r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"):
        if os.path.exists(p):
            import subprocess
            # 用单独的浏览器资料夹：不和平时的 Edge 混在一起、不用 Edge 缓存的旧图标，任务栏上单独一个图标
            subprocess.Popen([p, "--app=" + url, "--window-size=1360,900", "--user-data-dir=" + str(C.DATA / "edge-app"),
                              "--no-first-run", "--no-default-browser-check"])
            return
    webbrowser.open(url)


def main():
    port = int(os.environ.get("CHUTI_PORT") or C.load_cfg().get("port", 8766))
    try:
        srv = ThreadingHTTPServer(("127.0.0.1", port), H)
    except OSError:
        print("端口 %d 已被占用：单词工作台可能已经开着了，直接打开 http://127.0.0.1:%d" % (port, port))
        open_window("http://127.0.0.1:%d" % port)
        return
    m = wm()
    if m:
        m.set_logger(lambda s: print(s, flush=True))
    threading.Thread(target=prepare_repo, daemon=True).start()
    threading.Thread(target=repo_watch, daemon=True).start()
    C.RUNNER.start()
    threading.Timer(20, check_update_bg).start()
    url = "http://127.0.0.1:%d" % port
    print("单词工作台已启动：%s （关掉这个窗口就退出）" % url, flush=True)
    threading.Timer(1.0, open_window, args=(url,)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
