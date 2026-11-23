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

WEB = Path(__file__).resolve().parent / "web"
MIME = {".html": "text/html; charset=utf-8", ".js": "application/javascript; charset=utf-8",
        ".css": "text/css; charset=utf-8", ".png": "image/png", ".svg": "image/svg+xml"}


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
        C.STATE["repo"] = "出错"
        C.STATE["repoError"] = str(e)
        C.log("仓库没准备好：%s" % e)


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
            "logs": C.live_logs(60), "now": C.now()}


def api_settings_get(qs):
    c = C.load_cfg()
    c["githubToken"] = "（已填）" if c.get("githubToken") else ""
    c["api"] = dict(c["api"], key="（已填）" if c["api"].get("key") else "")
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
    C.save_cfg(cfg)
    web = b.get("web") or {}
    m = wm()
    if m and web:
        web = {k: v for k, v in web.items() if k != "playwright"}
        if web.get("aiPassword") in ("（已填）", None):
            web.pop("aiPassword", None)
        m.save_config(web)
    C.RUNNER.wake.set()
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
        import shutil
        with C.REPO_LOCK:
            shutil.rmtree(str(C.REPO), ignore_errors=True)
            C.STATE.update(repo="未准备", xlsx="")
        threading.Thread(target=prepare_repo, daemon=True).start()
    elif op == "token":
        ok, msg = C.check_token()
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


GET = {
    "/api/status": api_status, "/api/settings": api_settings_get, "/api/tasks": api_tasks, "/api/logs": api_logs,
    "/api/word": api_word, "/api/ai/live": api_ai_live,
    "/api/words": lambda qs: C.search_words(qs.get("q", ""), qs.get("status", ""), int(qs.get("page", 1))),
    "/api/map": lambda qs: C.word_map(),
    "/api/manual": lambda qs: {"items": C.q("SELECT * FROM manual ORDER BY ts DESC")},
    "/api/groups": lambda qs: {"items": C.q("SELECT * FROM groups ORDER BY id DESC LIMIT 200")},
    "/api/calls": lambda qs: {"items": C.q("SELECT id,task_id,ts,kind,words,secs,ok,error,provider,length(prompt) AS plen,"
                                           "length(reply) AS rlen FROM calls ORDER BY id DESC LIMIT 200")},
    "/api/call": lambda qs: C.q("SELECT * FROM calls WHERE id=?", (int(qs.get("id", 0)),), one=True) or {},
    "/api/issues": lambda qs: {"readme": C.readme_issues(),
                               "mine": [r["text"] for r in C.q("SELECT text FROM issues")]},
    "/api/video": api_video_get,
    "/api/prompt-preview": lambda qs: {"text": C.build_prompt(C.RUNNER.pick(int(qs.get("n", 3))) or ["make"])},
}
POST = {"/api/settings": api_settings_post, "/api/task": api_task_add, "/api/task/op": api_task_op,
        "/api/schedule": api_sched, "/api/word/check": api_word_check, "/api/manual": api_manual,
        "/api/ai": api_ai, "/api/repo": api_repo, "/api/video": api_video_post}


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
            subprocess.Popen([p, "--app=" + url, "--window-size=1360,900"])
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
    C.RUNNER.start()
    url = "http://127.0.0.1:%d" % port
    print("单词工作台已启动：%s （关掉这个窗口就退出）" % url, flush=True)
    threading.Timer(1.0, open_window, args=(url,)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
