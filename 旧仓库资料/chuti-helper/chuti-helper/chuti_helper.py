#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
出题助手（方案 A：网页上的操作由你自己点，其余自动）。它不碰浏览器、不碰镜像站，只看 GitHub 仓库。

  python chuti_helper.py new            开新对话前跑：确认旧对话已经停了，算出从哪个词开始，把整段指令放进剪贴板
  python chuti_helper.py watch          一直盯着仓库（开一个窗口放着，或开机自动跑）；该你去看网页时发提醒
  python chuti_helper.py status         几行字说清做到哪了（给你或 Claude Code 看）
  python chuti_helper.py test-notify    试一下提醒能不能收到
  python chuti_helper.py test-clipboard 试一下剪贴板（之后在记事本里 Ctrl+V 看看）
  python chuti_helper.py check-token    查 GitHub 令牌有没有效、有没有写权限

配置在同文件夹的 config.json（照 config.example.json 改）；指令模板在 prompt_template.txt。
"""
import argparse, base64, datetime, json, os, re, subprocess, sys, tempfile, time, urllib.error, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
D = '总表视频细节数据'
IDX = D + '/索引.tsv'
README = D + '/README.md'
REPO = os.path.join(HERE, 'repo')
LOGS = os.path.join(HERE, 'logs')
STATE = os.path.join(HERE, 'state.json')
STATUS = os.path.join(HERE, 'status.json')
LOCK = os.path.join(HERE, 'watch.lock')
RTAG = 'Runner: ciyuan-runner'                       # DeepSeek 接力（runner.py）的提交正文里带这一句
RSTATUS = os.path.join(HERE, 'runner_status.json')
RPAUSE = os.path.join(HERE, 'runner_pause.json')
RLOCK = os.path.join(HERE, 'runner.lock')
NO_WINDOW = 0x08000000 if os.name == 'nt' else 0

DEFAULTS = {
    'repo_url': 'https://github.com/Jacklee15333/ciyuanchaifeng.git',
    'branch': 'master',
    'git_proxy': None,
    'github_token_file': r'C:\Users\user\.secrets\gh_token.txt',
    'skill_file': r'C:\Users\user\Desktop\出题\zongbiao-questions.skill',
    'template_file': 'prompt_template.txt',
    'round_words': 300,
    'upload_every': 25,
    'poll_seconds': 120,
    'quiet_minutes': 8,
    'warn_minutes': 8,
    'first_commit_minutes': 25,
    'max_reminders': 3,
    'notify': {'toast': True, 'beep': True, 'webhook': None, 'webhook_proxy': None},
}

DEFAULT_TEMPLATE = ('按附件里的 zongbiao-questions 技能继续出题。以仓库为准：目前已有 {done} 个词有题目，第一个缺的词是 {next_word}'
                    '（总表第 {row} 个词，{pos}），它前面一个是 {prev_word}；README 进度表最后一行是“{last_group}”。'
                    '开工先跑 setup.py 核对索引和总表，然后从 {next_word} 开始接着做。每一轮尽量多做，争取一次 {round_words} 个词；'
                    '每 {upload_every} 个词上传一次；中途不要问我问题，这一轮做完直接汇报，并写明下一个从哪个词开始。')

TOKEN_BLOCK = ('\n\nGitHub 口令：{token}\n（fine-grained，只对 ciyuanchaifeng 仓库有 Contents 读写权限；每次上传前写进 /home/claude/.gh_token，'
               'upload.sh 用完会删掉；不要把口令打印出来，也不要写进任何文件或提交。）')

STALL_TIP = '去看网页：还在写就等；有“继续”就点（一个对话最多 2 次）；撞到 5 小时额度就跑 new 换对话。'

CFG = {}


# ---------------------------------------------------------------- 小工具
def now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def log(msg, echo=True):
    os.makedirs(LOGS, exist_ok=True)
    line = '%s %s' % (now(), msg)
    if echo:
        print(line, flush=True)
    with open(os.path.join(LOGS, 'helper.log'), 'a', encoding='utf-8') as f:
        f.write(line + '\n')


def jload(p, default):
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception:
        return default


def jsave(p, obj):
    tmp = p + '.tmp'
    json.dump(obj, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    os.replace(tmp, p)


def load_cfg():
    c = json.loads(json.dumps(DEFAULTS))
    p = os.path.join(HERE, 'config.json')
    if os.path.exists(p):
        user = json.load(open(p, encoding='utf-8-sig'))
        n = user.pop('notify', None) or {}
        c.update(user)
        c['notify'].update(n)
    return c


def mask(s):
    return re.sub(r'(github_pat_|ghp_)([A-Za-z0-9_]{4})[A-Za-z0-9_]+', r'\1\2…（已打码）', s or '')


def read_token(required=True):
    p = CFG.get('github_token_file')
    if p and os.path.exists(p):
        t = open(p, encoding='utf-8-sig').read().strip()
        if t:
            return t
    if required:
        raise SystemExit('✗ 找不到 GitHub 令牌文件：%s（新令牌存进这个文件，只写令牌一行）' % p)
    return None


def run(cmd, cwd=None, check=True, timeout=300, env_extra=None):
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0', PYTHONIOENCODING='utf-8')
    env.update(env_extra or {})
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=timeout,
                       env=env, stdin=subprocess.DEVNULL, creationflags=NO_WINDOW)
    if check and r.returncode:
        raise RuntimeError('%s 失败：%s' % (' '.join(cmd[:4]), mask((r.stderr or r.stdout).strip())[-600:]))
    return r


def git(*args, check=True, auth=False, timeout=300):
    cmd = ['git', '-c', 'core.quotepath=off']
    if CFG.get('git_proxy'):
        cmd += ['-c', 'http.proxy=' + CFG['git_proxy']]
    if auth:
        b = base64.b64encode(('x-access-token:' + read_token()).encode()).decode()
        cmd += ['-c', 'http.extraHeader=Authorization: Basic ' + b]
    return run(cmd + list(args), cwd=REPO, check=check, timeout=timeout).stdout


# ---------------------------------------------------------------- 仓库（只读：不在本地改任何东西，也不往仓库推任何东西）
def ensure_clone():
    if os.path.isdir(os.path.join(REPO, '.git')):
        return
    print('第一次运行：把仓库的提交记录拉到 %s（不下载视频等大文件，几十秒）…' % REPO, flush=True)
    cmd = ['git', '-c', 'core.quotepath=off'] + (['-c', 'http.proxy=' + CFG['git_proxy']] if CFG.get('git_proxy') else [])
    run(cmd + ['clone', '-q', '--filter=blob:none', '--no-checkout', '--depth', '100', '-b', CFG['branch'], CFG['repo_url'], REPO], timeout=900)


def fetch():
    r = None
    for auth in (False, True):        # 公开仓库不需要令牌；改成私有以后自动带上令牌
        if auth and not read_token(required=False):
            break
        r = run(['git', '-c', 'core.quotepath=off'] + (['-c', 'http.proxy=' + CFG['git_proxy']] if CFG.get('git_proxy') else [])
                + (['-c', 'http.extraHeader=Authorization: Basic ' + base64.b64encode(('x-access-token:' + read_token()).encode()).decode()] if auth else [])
                + ['fetch', '-q', '--depth', '100', 'origin', CFG['branch']], cwd=REPO, check=False, timeout=600)
        if r.returncode == 0:
            return
    raise RuntimeError('拉取仓库失败：%s' % mask((r.stderr or r.stdout).strip())[-400:])


def show(spec):
    try:
        return git('show', spec)
    except RuntimeError:
        if not read_token(required=False):
            raise
        return git('show', spec, auth=True)


_cache = {}


def snapshot():
    """仓库现在的样子：最新提交、最近一次数据提交、索引里做了哪些词、下一个词、README 最后一组"""
    ref = 'origin/' + CFG['branch']
    head = git('rev-parse', ref).strip()
    if head in _cache:
        return _cache[head]
    out = git('log', '-1', '--format=%h%x1f%ct%x1f%s%x1f%b', ref, '--', D).strip()
    h, ct, subj, body = (out.split('\x1f') + ['', '0', '', ''])[:4]
    web_ct = 0
    for rec in git('log', '-n', '50', '--format=%ct%x1f%B%x1e', ref, '--', D).split('\x1e'):
        rec = rec.strip()
        if rec and RTAG not in rec:
            web_ct = int(rec.split('\x1f')[0]); break
    rows = [l.split('\t') for l in show('%s:%s' % (ref, IDX)).splitlines()[1:]]
    done = {c[2] for c in rows if len(c) > 4 and c[4] == '细节数据有'}
    done_rows = frozenset((i, c[2]) for i, c in enumerate(rows) if len(c) > 4 and c[4] == '细节数据有')   # 按行比，重复词也查得出
    gaps = [i for i, c in enumerate(rows) if len(c) > 4 and c[4] == '缺']
    k = gaps[0] if gaps else None
    readme = show('%s:%s' % (ref, README)).split('\n')
    prog = [l for l in readme if re.match(r'\| \d{4}-\d\d-\d\d \| 题目第 \d+ 批', l)]
    lg = re.search(r'题目第 \d+ 批(?:第 \d+ 组)?', prog[-1]).group(0) if prog else ''
    s = {
        'head': head, 'commit': h, 'commit_time': int(ct or 0), 'subject': subj, 'by_runner': RTAG in body, 'web_time': web_ct,
        'done_rows': done_rows, 'done': len(done), 'left': len(gaps),
        'next_word': rows[k][2] if k is not None else None,
        'row': k + 1 if k is not None else None,
        'pos': '批次 %s 序号 %s' % (rows[k][0], rows[k][1]) if k is not None else '',
        'prev_word': rows[k - 1][2] if k else '',
        'last_group': lg,
    }
    _cache.clear()
    _cache[head] = s
    return s


def age_min(s):
    return (time.time() - s['commit_time']) / 60 if s['commit_time'] else 1e9


def subj_short(s):
    return re.sub(r'^总表视频细节数据：', '', s['subject'])[:60]


# ---------------------------------------------------------------- 提醒（不弹对话框，不等你回复）
def toast(title, body):
    q = lambda x: x.replace("'", "''")
    ps = ("$ErrorActionPreference='Stop';"
          "[void][Windows.UI.Notifications.ToastNotificationManager,Windows.UI.Notifications,ContentType=WindowsRuntime];"
          "[void][Windows.Data.Xml.Dom.XmlDocument,Windows.Data.Xml.Dom.XmlDocument,ContentType=WindowsRuntime];"
          "$t=[Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02);"
          "$n=$t.GetElementsByTagName('text');"
          "[void]$n.Item(0).AppendChild($t.CreateTextNode('%s'));"
          "[void]$n.Item(1).AppendChild($t.CreateTextNode('%s'));"
          "$id='{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\\WindowsPowerShell\\v1.0\\powershell.exe';"
          "[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($id).Show([Windows.UI.Notifications.ToastNotification]::new($t))"
          % (q(title), q(body)))
    enc = base64.b64encode(ps.encode('utf-16-le')).decode()
    run(['powershell.exe', '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-EncodedCommand', enc], timeout=60)


def fill(v, title, body, quote=False):
    if isinstance(v, dict):
        return {k: fill(x, title, body, quote) for k, x in v.items()}
    if isinstance(v, str):
        f = (lambda x: urllib.parse.quote(x, safe='')) if quote else (lambda x: x)
        return v.replace('{title}', f(title)).replace('{body}', f(body))
    return v


def webhook(title, body):
    w = CFG['notify']['webhook']
    url = fill(w['url'], title, body, quote=True)
    headers, data = {'User-Agent': 'chuti-helper'}, None
    if w.get('query'):
        url += ('&' if '?' in url else '?') + urllib.parse.urlencode(fill(w['query'], title, body))
    if w.get('json') is not None:
        data = json.dumps(fill(w['json'], title, body), ensure_ascii=False).encode('utf-8')
        headers['Content-Type'] = 'application/json; charset=utf-8'
    elif w.get('form') is not None:
        data = urllib.parse.urlencode(fill(w['form'], title, body)).encode('utf-8')
        headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=utf-8'
    px = CFG['notify'].get('webhook_proxy')
    op = urllib.request.build_opener(*([urllib.request.ProxyHandler({'http': px, 'https': px})] if px else []))
    req = urllib.request.Request(url, data=data, headers=headers, method=w.get('method') or ('POST' if data else 'GET'))
    with op.open(req, timeout=20) as r:
        return r.status


def notify(title, body):
    log('提醒：%s｜%s' % (title, body))
    st = jload(STATUS, {})
    st.setdefault('alerts', []).append({'time': now(), 'title': title, 'body': body})
    st['alerts'] = st['alerts'][-10:]
    jsave(STATUS, st)
    n, errs = CFG['notify'], []
    if os.name == 'nt' and n.get('beep'):
        try:
            import winsound
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        except Exception as e:
            errs.append('响声：%r' % e)
    if os.name == 'nt' and n.get('toast'):
        try:
            toast(title, body)
        except Exception as e:
            errs.append('通知：%s' % str(e)[-200:])
    if n.get('webhook'):
        try:
            webhook(title, body)
        except Exception as e:
            errs.append('手机推送：%r' % e)
    for e in errs:
        log('提醒没发出去（%s）' % e)
    return errs


# ---------------------------------------------------------------- 剪贴板
def clip_windows(text):
    import ctypes
    from ctypes import wintypes
    u32 = ctypes.WinDLL('user32', use_last_error=True)
    k32 = ctypes.WinDLL('kernel32', use_last_error=True)
    u32.OpenClipboard.argtypes = [wintypes.HWND]; u32.OpenClipboard.restype = wintypes.BOOL
    u32.EmptyClipboard.restype = wintypes.BOOL
    u32.SetClipboardData.argtypes = [wintypes.UINT, wintypes.HANDLE]; u32.SetClipboardData.restype = wintypes.HANDLE
    u32.CloseClipboard.restype = wintypes.BOOL
    k32.GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]; k32.GlobalAlloc.restype = wintypes.HANDLE
    k32.GlobalLock.argtypes = [wintypes.HANDLE]; k32.GlobalLock.restype = ctypes.c_void_p
    k32.GlobalUnlock.argtypes = [wintypes.HANDLE]; k32.GlobalUnlock.restype = wintypes.BOOL
    data = text.encode('utf-16-le') + b'\x00\x00'
    for _ in range(20):
        if u32.OpenClipboard(None):
            break
        time.sleep(0.1)
    else:
        return False
    try:
        u32.EmptyClipboard()
        h = k32.GlobalAlloc(0x0002, len(data))
        p = k32.GlobalLock(h)
        ctypes.memmove(p, data, len(data))
        k32.GlobalUnlock(h)
        return bool(u32.SetClipboardData(13, h))
    finally:
        u32.CloseClipboard()


def set_clipboard(text):
    if os.name == 'nt':
        try:
            if clip_windows(text):
                return True
        except Exception as e:
            log('剪贴板（方法一）没成功：%r' % e, echo=False)
        fd, p = tempfile.mkstemp(suffix='.txt')
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                f.write(text)
            run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command',
                 "Get-Content -Raw -Encoding UTF8 -LiteralPath '%s' | Set-Clipboard" % p.replace("'", "''")], timeout=60)
            return True
        except Exception as e:
            log('剪贴板（方法二）没成功：%s' % str(e)[-200:], echo=False)
            return False
        finally:
            os.remove(p)
    for cmd in (['pbcopy'], ['wl-copy'], ['xclip', '-selection', 'clipboard']):
        try:
            if subprocess.run(cmd, input=text.encode('utf-8'), timeout=10).returncode == 0:
                return True
        except Exception:
            pass
    return False


# ---------------------------------------------------------------- 看护的锁（同一时间只开一个 watch）
def pid_alive(pid):
    if pid <= 0:
        return False
    if os.name == 'nt':   # Windows 上 os.kill(pid, 0) 会直接杀掉进程，不能用
        import ctypes
        k = ctypes.windll.kernel32
        h = k.OpenProcess(0x1000, False, pid)
        if not h:
            return False
        code = ctypes.c_ulong()
        k.GetExitCodeProcess(h, ctypes.byref(code))
        k.CloseHandle(h)
        return code.value == 259
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def runner_pid():
    pid = int(jload(RLOCK, {}).get('pid', 0) or 0)
    return pid if pid_alive(pid) else 0


def runner_line():
    pid = runner_pid()
    if not pid:
        return 'DeepSeek 接力：没在运行'
    r = jload(RSTATUS, {})
    st = {'working': '正在出 %s（%s … %s）' % (r.get('group', ''), r.get('first', ''), r.get('last', '')),
          'waiting': '等着（%s）' % r.get('note', ''), 'idle': '刚传完 %s' % r.get('last_commit', ''),
          'starting': '刚启动', 'stopped': '停了：%s' % r.get('note', ''), 'done': '全部做完'}.get(r.get('state'), r.get('state', ''))
    return 'DeepSeek 接力：在运行，%s' % st


def wait_runner_yield():
    """跑 new 时：告诉 DeepSeek 让出来；它手上有一组在做，就等它传完（最多 25 分钟）"""
    jsave(RPAUSE, {'time': int(time.time()), 'when': now()})
    if not runner_pid():
        return True
    t0 = time.time()
    while time.time() - t0 < 25 * 60:
        r = jload(RSTATUS, {})
        if r.get('state') != 'working' or not runner_pid():
            return True
        if time.time() - t0 < 5:
            print('DeepSeek 正在做 %s，等它传完这一组再开网页（一般几分钟）…' % r.get('group', '这一组'), flush=True)
        time.sleep(10)
    return False


def watcher_pid():
    pid = int(jload(LOCK, {}).get('pid', 0) or 0)
    return pid if pid_alive(pid) else 0


# ---------------------------------------------------------------- 命令
def cmd_new(a):
    ensure_clone()
    if not wait_runner_yield():
        print('✗ DeepSeek 这一组 25 分钟还没传完，先别开网页。看 logs\\runner.log，或者过一会儿再跑 new。')
        return 2
    fetch()
    s = snapshot()
    if not s['left']:
        print('全部做完了：索引里已经没有“缺”的词。')
        return 0
    age = (time.time() - s['web_time']) / 60 if s['web_time'] else 1e9     # 只看网页对话的上传；DeepSeek 已经让出来了
    print('仓库：已有 %s 个词有题目，还缺 %s 行；第一个缺的是 %s（总表第 %s 个词，%s）。'
          % (format(s['done'], ','), format(s['left'], ','), s['next_word'], s['row'], s['pos']))
    print('最近一次上传：%s，%.0f 分钟前（%s%s）。' % (s['commit'], age_min(s), subj_short(s), '，DeepSeek 传的' if s['by_runner'] else ''))
    if age < CFG['quiet_minutes'] and not a.force:
        print('\n✗ 先别开新对话：网页对话 %.0f 分钟前还有上传，旧对话可能还在写。两个对话一起写会互相覆盖。' % age)
        print('  去看旧对话：显示还在写、Checking for a response 就继续等；有“继续”而且还没点满 2 次就点“继续”。')
        print('  确认它停了，等仓库安静满 %d 分钟再跑 new（确实没问题也可以加 --force）。' % CFG['quiet_minutes'])
        return 2
    tp = os.path.join(HERE, CFG['template_file'])
    tpl = open(tp, encoding='utf-8-sig').read().strip() if os.path.exists(tp) else DEFAULT_TEMPLATE
    vals = {'done': format(s['done'], ','), 'left': format(s['left'], ','), 'next_word': s['next_word'], 'row': s['row'],
            'pos': s['pos'], 'prev_word': s['prev_word'], 'last_group': s['last_group'],
            'round_words': CFG['round_words'], 'upload_every': CFG['upload_every']}
    text = tpl
    for k, v in vals.items():
        text = text.replace('{%s}' % k, str(v))
    text += TOKEN_BLOCK.replace('{token}', read_token())
    ok = set_clipboard(text)
    os.makedirs(LOGS, exist_ok=True)
    open(os.path.join(LOGS, 'prompt_last.txt'), 'w', encoding='utf-8').write(mask(text) + '\n')
    st = jload(STATE, {})
    st['session'] = {'started_at': int(time.time()), 'started': now(), 'expect_first': s['next_word'],
                     'done_at_start': s['done'], 'head_at_start': s['head'], 'first_seen': False, 'first_warned': False}
    st['chats'] = int(st.get('chats', 0)) + 1
    jsave(STATE, st)
    log('new：第 %d 个对话，从 %s 开始（仓库已有 %d 个词）' % (st['chats'], s['next_word'], s['done']), echo=False)
    print('\n' + ('✓ 下一轮的整段指令已经放进剪贴板（含 GitHub 口令）。下面是打码后的样子：' if ok else
                  '✗ 剪贴板没放进去。打开 logs\\prompt_last.txt 复制（那里口令打了码，口令要从令牌文件里另外复制）：'))
    print('-' * 60 + '\n' + mask(text) + '\n' + '-' * 60)
    skill = CFG.get('skill_file') or ''
    print('\n接下来在火狐里（这些由你来点）：')
    print(' 1. 关掉旧对话的标签')
    print(' 2. 打开 zd87.com/ai-fleet/claude → 一键直达 → 克劳德·号池1 → 往下翻，选状态最好的那个')
    print(' 3. 等输入框出来；模型选 Opus 5.5，Effort 选“中等”（不要“最高”）')
    print(' 4. 附件加上 %s%s' % (skill, '' if not skill or os.path.exists(skill) else '（✗ 这个文件现在不在，先放好）'))
    print(' 5. 在输入框按 Ctrl+V，发送')
    print('这个对话最多点 2 次“继续”；要换新对话时，再跑一次 new。')
    if not watcher_pid():
        print('\n提示：看护（watch）没在运行，出问题不会提醒你。双击 watch_start.bat，或运行 python chuti_helper.py watch。')
    return 0


def cmd_status(a):
    st = jload(STATUS, {})
    pid = watcher_pid()
    fresh = pid and st.get('updated_epoch', 0) > time.time() - 3 * CFG['poll_seconds']
    if not fresh:
        ensure_clone(); fetch()
        s = snapshot()
        st.update({'done': s['done'], 'left': s['left'], 'next_word': s['next_word'], 'commit': s['commit'],
                   'commit_time': s['commit_time'], 'subject': s['subject']})
    age = (time.time() - st.get('commit_time', 0)) / 60
    print('累计 %s 个词有题目，还缺 %s 行；下一个是 %s。' % (format(st.get('done', 0), ','), format(st.get('left', 0), ','), st.get('next_word')))
    print('最近一次上传：%.0f 分钟前（%s %s）。' % (age, st.get('commit', ''), re.sub(r'^总表视频细节数据：', '', st.get('subject', ''))[:50]))
    print('看护：%s。' % ('在运行（每 %d 秒看一次）' % CFG['poll_seconds'] if pid else '没在运行'))
    print(runner_line() + '。')
    al = st.get('alerts') or []
    print('最近一条提醒：%s' % ('%s %s' % (al[-1]['time'][5:16], al[-1]['title']) if al else '无'))
    return 0


def cmd_watch(a):
    if watcher_pid():
        print('看护已经在运行了（进程 %d），不用再开。' % watcher_pid())
        return 0
    jsave(LOCK, {'pid': os.getpid(), 'since': now()})
    poll = a.poll or CFG['poll_seconds']
    try:
        ensure_clone(); fetch()
        s = snapshot()
        prev_head, prev_rows = s['head'], s['done_rows']
        stall_key, reminders, net_fail_since, cycles = None, 0, None, 0
        log('开始看护：每 %d 秒看一次仓库。现在累计 %d 个词，下一个 %s，最近上传 %.0f 分钟前。' % (poll, s['done'], s['next_word'], age_min(s)))
        while True:
            cycles += 1
            try:
                if cycles > 1:
                    fetch()
                s = snapshot()
                if net_fail_since and time.time() - net_fail_since > 1800:
                    log('网络恢复了')
                net_fail_since = None
            except Exception as e:
                net_fail_since = net_fail_since or time.time()
                log('看仓库失败（%s）' % str(e)[-150:], echo=False)
                if time.time() - net_fail_since > 1800 and not getattr(cmd_watch, 'net_warned', False):
                    notify('出题助手：连不上 GitHub', '已经 30 分钟连不上仓库了。看看网络和代理（127.0.0.1:7892）。')
                    cmd_watch.net_warned = True
                s = None
            if s:
                cmd_watch.net_warned = False
                st = jload(STATE, {})
                ses = st.get('session') or {}
                if s['head'] != prev_head:
                    lost = sorted({w for i, w in prev_rows - s['done_rows']})
                    gained = {w for i, w in s['done_rows'] - prev_rows}
                    if lost:
                        notify('出题助手：有题目被覆盖了！',
                               '%s 让 %d 个词变回了“缺”（如 %s）。多半是两个对话在同时写：马上停掉旧的那个，再让 Claude Code 帮你恢复。'
                               '（如果是你自己有意改回“缺”的，忽略这条）' % (s['commit'], len(lost), '、'.join(lost[:4])))
                    if gained:
                        log('上传：+%d 个词（%s），累计 %d，下一个 %s' % (len(gained), subj_short(s), s['done'], s['next_word']))
                        if ses and not ses.get('first_seen') and not s['by_runner'] and s['commit_time'] >= ses.get('started_at', 0) - 60:
                            ses['first_seen'] = True
                            if ses.get('expect_first') in gained:
                                log('新对话的第一组从 %s 开始，位置对' % ses['expect_first'])
                            else:
                                notify('出题助手：新对话起点不对', '应该从 %s 开始，第一次上传却是“%s”。去看看它是不是从错的地方开始了。'
                                       % (ses.get('expect_first'), subj_short(s)))
                            st['session'] = ses
                            jsave(STATE, st)
                    prev_head, prev_rows = s['head'], s['done_rows']
                if not s['left']:
                    notify('出题助手：全部做完了', '索引里已经没有“缺”的词了，累计 %d 个。' % s['done'])
                    return 0
                age = age_min(s)
                if age >= CFG['warn_minutes']:
                    if stall_key != s['commit']:
                        stall_key, reminders = s['commit'], 0
                        while reminders + 1 < CFG['max_reminders'] and age >= CFG['warn_minutes'] * 3 ** (reminders + 1):
                            reminders += 1      # 已经过了的几档只提醒最近的一次，免得一开就连响几条
                    due = CFG['warn_minutes'] * (3 ** reminders)
                    if reminders < CFG['max_reminders'] and age >= due:
                        relay = ('不在电脑旁也没关系：网页安静满 %d 分钟，DeepSeek 会自动接手。' % (CFG.get('relay') or {}).get('takeover_minutes', 30)) if runner_pid() else ''
                        notify('出题助手：%.0f 分钟没有新上传' % age, '最后一次：%s。%s%s' % (subj_short(s), STALL_TIP, relay))
                        reminders += 1
                if (ses and not ses.get('first_seen') and not ses.get('first_warned') and not s['by_runner']
                        and time.time() - ses.get('started_at', 0) > CFG['first_commit_minutes'] * 60):
                    notify('出题助手：新对话还没上传第一组', '开了 %d 分钟还没有上传。看看是不是卡在开头（没附技能、没发口令、setup 报错、在等“继续”）。'
                           % ((time.time() - ses.get('started_at', 0)) // 60))
                    ses['first_warned'] = True
                    st['session'] = ses
                    jsave(STATE, st)
                stj = jload(STATUS, {})
                stj.update({'updated': now(), 'updated_epoch': int(time.time()), 'done': s['done'], 'left': s['left'],
                            'next_word': s['next_word'], 'commit': s['commit'], 'commit_time': s['commit_time'], 'subject': s['subject'],
                            'watcher_pid': os.getpid()})
                jsave(STATUS, stj)
            if a.cycles and cycles >= a.cycles:
                return 0
            time.sleep(poll)
    except KeyboardInterrupt:
        log('看护停了（Ctrl+C）')
        return 0
    finally:
        if int(jload(LOCK, {}).get('pid', 0) or 0) == os.getpid():
            os.remove(LOCK)


def cmd_test_notify(a):
    errs = notify('出题助手：测试提醒', '收到这条，说明提醒能用。')
    print('发出去了' if not errs else '有的方式没发出去：%s' % '；'.join(errs))
    return 0 if not errs else 1


def cmd_test_clipboard(a):
    ok = set_clipboard('出题助手剪贴板测试：中文、English、“引号”都正常 ✓')
    print('已放进剪贴板，到记事本里 Ctrl+V 看看。' if ok else '✗ 剪贴板放不进去')
    return 0 if ok else 1


def cmd_check_token(a):
    tok = read_token()
    m = re.search(r'github\.com[/:]([^/]+/[^/.]+)', CFG['repo_url'])
    if not m:
        print('repo_url 不是 GitHub 地址，跳过'); return 0
    px = CFG.get('git_proxy')
    op = urllib.request.build_opener(*([urllib.request.ProxyHandler({'http': px, 'https': px})] if px else []))
    req = urllib.request.Request('https://api.github.com/repos/' + m.group(1),
                                 headers={'Authorization': 'Bearer ' + tok, 'User-Agent': 'chuti-helper'})
    try:
        with op.open(req, timeout=30) as r:
            j = json.loads(r.read().decode('utf-8'))
        push = j.get('permissions', {}).get('push')
        print('令牌有效；对 %s %s写权限。' % (j.get('full_name'), '有' if push else '没有（网页那边会传不上去）'))
        return 0 if push else 1
    except urllib.error.HTTPError as e:
        print('✗ 令牌不能用（HTTP %d）：过期、被作废，或者复制错了。' % e.code)
        return 1


def main():
    ap = argparse.ArgumentParser(description='出题助手（网页由你点，其余自动）')
    ap.add_argument('cmd', choices=['new', 'watch', 'status', 'test-notify', 'test-clipboard', 'check-token'])
    ap.add_argument('--force', action='store_true', help='new：不管“仓库刚才还有上传”的提醒')
    ap.add_argument('--poll', type=int, default=0, help='watch：几秒看一次（默认看配置）')
    ap.add_argument('--cycles', type=int, default=0, help='watch：看几次就退出（测试用）')
    a = ap.parse_args()
    global CFG
    CFG = load_cfg()
    f = {'new': cmd_new, 'watch': cmd_watch, 'status': cmd_status, 'test-notify': cmd_test_notify,
         'test-clipboard': cmd_test_clipboard, 'check-token': cmd_check_token}[a.cmd]
    try:
        sys.exit(f(a) or 0)
    except RuntimeError as e:
        log('✗ %s' % e)
        sys.exit(1)


if __name__ == '__main__':
    main()
