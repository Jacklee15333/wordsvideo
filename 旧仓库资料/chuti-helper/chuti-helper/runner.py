#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek 接力出题（方案 C）：网页对话在写的时候它等着；网页安静够久（默认 30 分钟）就自动接手，
一组 25 个词：取材料 → DeepSeek 写简写稿 → 仓库自带的 compact.py / save_questions.py 体检保存 → 没过的让它改（最多 3 轮）
→ 记 README → 提交（正文带“Runner: ciyuan-runner”）→ 上传。你跑 new 开网页对话时，它做完手上这一组就让出来。

  python runner.py            一直跑（接力模式）；双击 runner_start.bat 就是这个
  python runner.py --selftest 测一下 DeepSeek API 和 GitHub 令牌
  python runner.py --once     不等、马上做一组就停（试跑用；会上传）
停：在文件夹里建一个叫 STOP 的文件（做完手上这组就停），或关掉它的进程。
"""
import argparse, base64, datetime, json, os, re, sys, time, traceback, urllib.error, urllib.request, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import chuti_helper as H     # 同一个 config.json、同一套提醒

D = H.D
TAG = 'Runner: ciyuan-runner'
TYPES = set('听单形选改完')
REPO = os.path.join(HERE, 'runner_repo')
RSTATE = os.path.join(HERE, 'runner_state')
RSTATUS = os.path.join(HERE, 'runner_status.json')
PAUSE = os.path.join(HERE, 'runner_pause.json')
LOCK = os.path.join(HERE, 'runner.lock')
STOP = os.path.join(HERE, 'STOP')
NEEDS = os.path.join(RSTATE, 'needs_review.json')
CFG = {}


class Fatal(Exception):
    """要人来处理：停下并提醒"""


class Yield(Exception):
    """网页那边在写：这一组作废，回去等"""


def log(msg):
    os.makedirs(H.LOGS, exist_ok=True)
    line = '%s %s' % (H.now(), msg)
    print(line, flush=True)
    with open(os.path.join(H.LOGS, 'runner.log'), 'a', encoding='utf-8') as f:
        f.write(line + '\n')


def rstatus(**kw):
    s = H.jload(RSTATUS, {})
    s.update(kw)
    s['updated'] = H.now()
    s['updated_epoch'] = int(time.time())
    s['pid'] = os.getpid()
    H.jsave(RSTATUS, s)


def load_cfg():
    c = H.load_cfg()
    llm = c.setdefault('llm', {})
    for k, v in {'style': 'openai', 'base_url': 'https://api.deepseek.com', 'model': '', 'key_file': '',
                 'max_tokens': 8000, 'temperature': 0.3, 'timeout': 600, 'proxy': None, 'label': 'DeepSeek（本地接力）'}.items():
        llm.setdefault(k, v)
    r = c.setdefault('relay', {})
    for k, v in {'takeover_minutes': 30, 'group_size': 25, 'chunk_size': 5, 'max_fix_rounds': 3, 'check_seconds': 60,
                 'retry_waits': [15, 30, 60, 120, 240, 300, 300]}.items():
        r.setdefault(k, v)
    return c


def run(cmd, check=True, timeout=900):
    r = H.run(cmd, cwd=REPO, check=False, timeout=timeout)
    if check and r.returncode:
        raise Fatal('命令失败：%s\n%s' % (H.mask(' '.join(cmd[:5])), H.mask((r.stderr or r.stdout)[-1200:])))
    return r


# 仓库里有 词/c/con.json（con 是 Windows 保留名）。Windows 上的 git 读树时就会报 invalid path，
# 所以 runner 自己这份副本一律带 core.protectNTFS=false；这个文件本身由 sparse_patterns() 排除，永远不写到磁盘上。
GITC = ['git', '-c', 'core.quotepath=off', '-c', 'core.protectNTFS=false', '-c', 'core.longpaths=true']


def git_r(*args, auth=False, check=True):
    cmd = list(GITC)
    if CFG.get('git_proxy'):
        cmd += ['-c', 'http.proxy=' + CFG['git_proxy']]
    if auth:
        b = base64.b64encode(('x-access-token:' + H.read_token()).encode()).decode()
        cmd += ['-c', 'http.extraHeader=Authorization: Basic ' + b]
    return run(cmd + list(args), check=check)


def git(*args, **kw):
    return git_r(*args, **kw).stdout


RESERVED = {'con', 'prn', 'aux', 'nul'} | {'com%d' % i for i in range(10)} | {'lpt%d' % i for i in range(10)}


def sparse_patterns(extra=()):
    """要检出的路径；Windows 保留名（如 词/c/con.json）不检出，否则 git 在 Windows 上会报 invalid path、整个检出失败"""
    pats = ['/%s/' % D] + list(extra)
    for f in git('ls-tree', '-r', '--name-only', 'HEAD', '--', D + '/词').splitlines():
        if os.path.basename(f).split('.')[0].lower() in RESERVED:
            pats.append('!/' + f)
    return pats


def ensure_clone():
    if os.path.isdir(os.path.join(REPO, '.git')):
        return
    log('第一次运行：克隆仓库到 %s（只检出「%s」和最新总表）' % (REPO, D))
    cmd = list(GITC) + (['-c', 'http.proxy=' + CFG['git_proxy']] if CFG.get('git_proxy') else [])
    r = H.run(cmd + ['clone', '-q', '--filter=blob:none', '--sparse', '--depth', '50', '-b', CFG['branch'], CFG['repo_url'], REPO],
              check=False, timeout=1800)
    if r.returncode:
        raise Fatal('克隆失败：%s' % H.mask(r.stderr[-600:]))
    git('config', 'core.autocrlf', 'true' if os.name == 'nt' else 'input')
    git('config', 'core.protectNTFS', 'false')
    git('config', 'core.longpaths', 'true')
    git('sparse-checkout', 'set', '--no-cone', *sparse_patterns())


def fetch():
    git('fetch', '-q', '--depth', '50', 'origin', CFG['branch'])


def origin():
    return 'origin/' + CFG['branch']


def last_foreign_time():
    """origin 上最近一次“不是 runner 提交的”数据改动的时间（网页对话的上传）"""
    out = git('log', '-n', '50', '--format=%ct%x1f%B%x1e', origin(), '--', D)
    for rec in out.split('\x1e'):
        rec = rec.strip()
        if not rec:
            continue
        ct, body = (rec.split('\x1f', 1) + [''])[:2]
        if TAG not in body:
            return int(ct)
    return 0


def pause_time():
    """你跑 new 的时间（runner_pause.json，以及看护记的新对话时间）"""
    t = int(H.jload(PAUSE, {}).get('time', 0) or 0)
    ses = H.jload(H.STATE, {}).get('session') or {}
    return max(t, int(ses.get('started_at', 0) or 0))


def quiet_minutes():
    return (time.time() - max(last_foreign_time(), pause_time())) / 60


# ---------------------------------------------------------------- 总表、索引
def latest_xlsx():
    NUM = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}

    def cn2int(s):
        total, cur = 0, 0
        for ch in s:
            if ch in NUM:
                cur = NUM[ch]
            elif ch == '十':
                total += (cur or 1) * 10; cur = 0
            elif ch == '百':
                total += (cur or 1) * 100; cur = 0
            else:
                return -1
        return total + cur
    vers = []
    for p in git('ls-tree', '-d', '--name-only', 'HEAD', '最新工作版/').splitlines():
        m = re.fullmatch(r'最新工作版/第(.+)版', p.strip())
        if m and cn2int(m.group(1)) > 0:
            vers.append((cn2int(m.group(1)), p.strip()))
    for n, p in sorted(vers, reverse=True):
        files = [f for f in git('ls-tree', '--name-only', 'HEAD', p + '/').splitlines() if re.search(r'/2词源拆分总表.*\.xlsx$', f)]
        if files:
            want = sparse_patterns(['/' + files[0]])
            have = git('sparse-checkout', 'list', check=False).split('\n')
            if not all(w in have for w in want):
                git('sparse-checkout', 'set', '--no-cone', *want)
            return os.path.join(REPO, files[0]), p.split('/')[-1]
    raise Fatal('仓库「最新工作版」里没找到 2词源拆分总表*.xlsx')


def read_index():
    return [l.split('\t') for l in open(os.path.join(REPO, D, '索引.tsv'), encoding='utf-8').read().splitlines()[1:]]


def verify(xlsx):
    import openpyxl
    ws = openpyxl.load_workbook(xlsx, read_only=True)['拆分结果']
    it = ws.iter_rows(values_only=True)
    h = [str(x) if x else '' for x in next(it)]
    ix = {k: i for i, k in enumerate(h)}
    tab = [(str(r[ix['批次']]), str(r[ix['序号']]), str(r[ix['单词']] or '').strip()) for r in it if r[ix['单词']]]
    idx = read_index()
    bad = [(i + 1, a, b) for i, (a, b) in enumerate(zip(tab, [(c[0], c[1], c[2]) for c in idx])) if a != b]
    if bad or len(tab) != len(idx):
        raise Fatal('索引和总表对不上 %d 处（前 3 处：%s）。总表可能改过顺序或增删了词，先别出题。' % (len(bad) + abs(len(tab) - len(idx)), bad[:3]))
    left = [c for c in idx if c[4] == '缺']
    return {'done': len({c[2] for c in idx if c[4] == '细节数据有'}), 'left': len(left), 'next': left[0][2] if left else None}


def sync():
    fetch()
    if git('status', '--porcelain', '--', D).strip():
        git('checkout', '--', D)
        git('clean', '-fdq', '--', D)
    git('reset', '-q', '--hard', origin())


# ---------------------------------------------------------------- 规矩和提示词
def skill_texts():
    p = os.path.join(REPO, D, '出题技能', 'zongbiao-questions.skill')
    if not os.path.exists(p):
        p = CFG.get('skill_file') or ''
    if not os.path.exists(p):
        raise Fatal('找不到出题技能 zongbiao-questions.skill')
    z = zipfile.ZipFile(p)
    names = z.namelist()
    rd = lambda n: z.read(next(x for x in names if x.endswith('references/' + n))).decode('utf-8')
    return rd('rules.md').split('\n## 五')[0].strip(), rd('example.md').strip()


SYSTEM = """你是中学英语出题员，给词源拆分总表里的单词出练习题。严格按下面的规矩和范例写，只输出简写稿，不要任何解释、标题、编号或代码块。

<规矩>
{rules}
</规矩>

<范例>
{example}
</范例>

输出要求（体检程序会逐条检查，过不了就要重写）：
- 每个词以“@单词”开头（照材料原样，大小写不改），下面正好 7 行，依次是第 1–7 题；第 1 题是“听”。
- 第 2–5 题四种题型互不重复；第 6、7 题行末必须写考点（变形 / 词性转换 / 短语 / 用法 / 易混 之一）。
- 答案就是本词原形的最多 1 道（选择题对的选项、填空答案，整串相同就算）。
- 选择题第一个选项写对的，选项用“ / ”分隔、互不重复、4 个；正文里不能出现“|”。
- 句子 12 个词以内、初中词汇、答案唯一、时态要有标志词。
- 材料里看到总表本身写错的地方：照真实英语出题，不考错的内容；在这个词 7 行后面另起一行写“#问题 单词：哪里不对，正确应是……”。"""

ASK = """下面是按总表顺序取出的 {n} 个词的材料（每个词第一行：@单词｜初中含义｜考点；缩进的行是辨析，或“总表里还有一行”的提示，两个意思都要考到）。
按规矩给每个词出 7 道题，只输出简写稿。

{mat}"""

FIX = """下面这些词的简写稿没通过体检。按“问题”改好，重新输出这几个词完整的 7 行（只输出这几个词）。

{items}"""


# ---------------------------------------------------------------- DeepSeek
def llm(system, user):
    c = CFG['llm']
    if not c.get('model') or not c.get('key_file') or not os.path.exists(c['key_file']):
        raise Fatal('config.json 的 llm 还没配好（model、key_file）')
    key = open(c['key_file'], encoding='utf-8-sig').read().strip()
    base = c['base_url'].rstrip('/')
    if c['style'] == 'anthropic':
        url = base if base.endswith('/messages') else base + ('/messages' if base.endswith('/v1') else '/v1/messages')
        body = {'model': c['model'], 'max_tokens': c['max_tokens'], 'system': system, 'messages': [{'role': 'user', 'content': user}],
                'thinking': {'type': 'disabled'}}
        headers = {'x-api-key': key, 'anthropic-version': '2023-06-01', 'content-type': 'application/json'}
    else:
        url = base if base.endswith('/chat/completions') else base + '/chat/completions'
        body = {'model': c['model'], 'max_tokens': c['max_tokens'],
                'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}]}
        headers = {'Authorization': 'Bearer ' + key, 'content-type': 'application/json'}
    if c.get('temperature') is not None:
        body['temperature'] = c['temperature']
    op = urllib.request.build_opener(*([urllib.request.ProxyHandler({'http': c['proxy'], 'https': c['proxy']})] if c.get('proxy') else []))
    data = json.dumps(body, ensure_ascii=False).encode('utf-8')
    waits = list(CFG['relay']['retry_waits'])
    for i, w in enumerate(waits + [None]):
        try:
            with op.open(urllib.request.Request(url, data=data, headers=headers, method='POST'), timeout=c['timeout']) as r:
                j = json.loads(r.read().decode('utf-8'))
            if c['style'] == 'anthropic':
                text = ''.join(b.get('text', '') for b in j.get('content', []) if b.get('type') == 'text')
                stop = j.get('stop_reason')
            else:
                ch = j['choices'][0]
                text, stop = ch['message'].get('content') or '', ch.get('finish_reason')
            if stop in ('max_tokens', 'length'):
                log('提醒：输出被 max_tokens 截断了（把 relay.chunk_size 调小）')
            return text
        except urllib.error.HTTPError as e:
            msg = H.mask(e.read().decode('utf-8', 'replace')[:300])
            if e.code in (401, 403):
                raise Fatal('DeepSeek 拒绝（%d，key 不对）：%s' % (e.code, msg))
            if e.code == 402:
                raise Fatal('DeepSeek 余额不足（402）')
            if e.code == 400:
                raise Fatal('DeepSeek 说请求不对（400，多半是模型名写错）：%s' % msg)
            err = 'HTTP %d' % e.code
        except Exception as e:
            err = repr(e)[:200]
        if w is None:
            raise Fatal('DeepSeek 连续失败：%s' % err)
        log('DeepSeek 出错，%d 秒后重试（第 %d 次）：%s' % (w, i + 1, err))
        time.sleep(w)


# ---------------------------------------------------------------- 一组
def materials(xlsx, n, skip):
    tool = os.path.join(REPO, D, '工具', 'next_words.py')
    out = run([sys.executable, tool, xlsx, str(n + len(skip)), '--brief']).stdout
    out = re.sub(r'（还缺题目的词.*', '', out)
    res = []
    for b in [b if b.startswith('@') else '@' + b for b in out.split('\n@') if b.strip()]:
        w = b.split('\n')[0][1:].split('｜')[0].strip()
        if w and w not in skip:
            res.append((w, b.rstrip()))
    return res[:n]


def parse_draft(text, wanted):
    low = {w.lower(): w for w in wanted}
    blocks, issues, cur = {}, [], None
    for raw in (text or '').splitlines():
        l = raw.strip()
        if not l or l.startswith('```'):
            continue
        if l.startswith('#'):
            m = re.match(r'#+\s*问题[\s：:]*(.+)', l)
            if m:
                issues.append(m.group(1).strip())
            continue
        m = re.match(r'@\s*([^｜|]+)', l)
        if m:
            cur = low.get(m.group(1).strip().lower())
            if cur:
                blocks[cur] = []
            continue
        if cur:
            l = re.sub(r'^(?:\d+\s*[.、)）]\s*|[-*•]\s+)', '', l)
            if '|' not in l and '｜' in l:
                l = l.replace('｜', '|')
            blocks[cur].append(l)
    return blocks, issues


def shape_errors(lines):
    errs = []
    if len(lines) != 7:
        errs.append('要正好 7 行（7 道题），写了 %d 行' % len(lines))
    for k, l in enumerate(lines[:7]):
        t = l.split('|')[0].strip()
        if t not in TYPES:
            errs.append('第 %d 行开头要是 听/单/形/选/改/完 之一' % (k + 1))
    if lines and lines[0].split('|')[0].strip() != '听':
        errs.append('第 1 题要是“听”')
    return errs


def save_batch(drafts, tag, version):
    gen = os.path.join(RSTATE, 'gen')
    os.makedirs(gen, exist_ok=True)
    src, js = os.path.join(gen, tag + '.txt'), os.path.join(gen, tag + '.json')
    with open(src, 'w', encoding='utf-8', newline='\n') as f:
        for w, lines in drafts.items():
            f.write('@%s\n%s\n' % (w, '\n'.join(lines)))
    tools = os.path.join(REPO, D, '工具')
    r1 = run([sys.executable, os.path.join(tools, 'compact.py'), src, js], check=False)
    if r1.returncode:
        raise Fatal('compact.py 出错：%s' % (r1.stderr or r1.stdout)[-600:])
    errs = {}
    for m in re.finditer(r'第 \d+ 行（(.+?)）写法不对：(.*)', r1.stdout):
        errs.setdefault(m.group(1), []).append('写法不对：' + m.group(2))
    r2 = run([sys.executable, os.path.join(tools, 'save_questions.py'), js, version], check=False)
    if r2.returncode not in (0, 1):
        raise Fatal('save_questions.py 出错：%s' % (r2.stderr or r2.stdout)[-600:])
    for m in re.finditer(r'✗ (.+?)：(.*)', r2.stdout):
        errs.setdefault(m.group(1).strip(), []).append(m.group(2).strip())
    st = {c[2]: c[4] for c in read_index()}
    for w in drafts:
        if st.get(w) != '细节数据有' and w not in errs:
            errs[w] = ['没存上']
    return {w: e for w, e in errs.items() if w in drafts}


def relabel(words):
    label = time.strftime('%Y-%m-%d') + ' ' + CFG['llm']['label']
    rel = {c[2]: c[6] for c in read_index() if c[4] == '细节数据有'}
    for w in words:
        p = os.path.join(REPO, D, rel.get(w, '') or '_none_')
        if os.path.isfile(p):
            rec = json.load(open(p, encoding='utf-8'))
            rec['题目生成'] = label
            json.dump(rec, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def next_group_no(lines):
    gpb = max(1, 100 // CFG['relay']['group_size'])
    prog = [l for l in lines if re.match(r'\| \d{4}-\d\d-\d\d \| 题目第 \d+ 批', l)]
    if not prog:
        return 1, 1
    m = re.search(r'题目第 (\d+) 批(?:第 (\d+) 组)?', prog[-1])
    b, g = int(m.group(1)), int(m.group(2) or gpb)
    return (b, g + 1) if g < gpb else (b + 1, 1)


def write_readme(b, g, words, fixed, failed, issues, done):
    p = os.path.join(REPO, D, 'README.md')
    lines = open(p, encoding='utf-8').read().split('\n')
    note = '体检全部 0 个问题' if not failed else '体检通过的都存了'
    if fixed:
        note += '；%s 体检没过、改过再存' % '、'.join(fixed)
    if failed:
        note += '；%s 改了 %d 次仍没过，没存，留待人工' % ('、'.join(failed), CFG['relay']['max_fix_rounds'])
    note += '；出题：%s' % CFG['llm']['label']
    last = max(i for i, l in enumerate(lines) if re.match(r'\| \d{4}-\d\d-\d\d \| 题目第 \d+ 批', l))
    lines.insert(last + 1, '| %s | 题目第 %d 批第 %d 组 | %d | %s … %s（%s）。累计 %d 个词有题目 |'
                 % (time.strftime('%Y-%m-%d'), b, g, len(words), words[0], words[-1], note, done))
    if issues:
        try:
            head = next(i for i, l in enumerate(lines) if l.startswith('## 总表里看着不对的地方'))
            end = next((i for i in range(head + 1, len(lines)) if lines[i].startswith('## ')), len(lines))
            while end > head + 1 and not lines[end - 1].strip():
                end -= 1
            for k, s in enumerate(issues):
                lines.insert(end + k, '- ' + s.replace('\n', ' '))
        except StopIteration:
            pass
    with open(p, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def one_group(xlsx, version, rules, example):
    R = CFG['relay']
    needs = H.jload(NEEDS, {})
    mats = materials(xlsx, R['group_size'], set(needs))
    if not mats:
        return None
    words = [w for w, _ in mats]
    mat_of = dict(mats)
    b, g = next_group_no(open(os.path.join(REPO, D, 'README.md'), encoding='utf-8').read().split('\n'))
    tag = 'b%d_g%d_%s' % (b, g, time.strftime('%m%d%H%M%S'))
    log('第 %d 批第 %d 组：%s … %s（%d 个词）' % (b, g, words[0], words[-1], len(words)))
    rstatus(state='working', group='题目第 %d 批第 %d 组' % (b, g), first=words[0], last=words[-1])
    system = SYSTEM.format(rules=rules, example=example)
    raw = os.path.join(H.LOGS, 'drafts', tag)
    os.makedirs(raw, exist_ok=True)
    pending, last_draft, last_err, fixed, issues = {}, {}, {}, [], []
    cs = max(1, R['chunk_size'])
    for i in range(0, len(words), cs):
        chunk = words[i:i + cs]
        out = llm(system, ASK.format(n=len(chunk), mat='\n'.join(mat_of[w] for w in chunk)))
        open(os.path.join(raw, 'r0_%02d.txt' % (i // cs)), 'w', encoding='utf-8').write(out)
        bl, iss = parse_draft(out, chunk)
        issues += iss
        for w in chunk:
            pending[w] = bl.get(w, [])
    for rnd in range(R['max_fix_rounds'] + 1):
        good = {w: l for w, l in pending.items() if not shape_errors(l)}
        errs = {w: shape_errors(l) for w, l in pending.items() if shape_errors(l)}
        if good:
            errs.update(save_batch(good, '%s_r%d' % (tag, rnd), version))
        last_draft.update(pending)
        if not errs:
            break
        last_err = errs
        if rnd == R['max_fix_rounds']:
            break
        fixed += [w for w in errs if w not in fixed]
        items = ['=== %s ===\n材料：\n%s\n问题：%s\n原来写的：\n@%s\n%s' % (w, mat_of[w], '；'.join(e), w, '\n'.join(last_draft.get(w) or ['（没写出来）']))
                 for w, e in errs.items()]
        out = llm(system, FIX.format(items='\n\n'.join(items)))
        open(os.path.join(raw, 'fix%d.txt' % (rnd + 1)), 'w', encoding='utf-8').write(out)
        bl, iss = parse_draft(out, list(errs))
        issues += iss
        pending = {w: bl.get(w, []) for w in errs}
    st = {c[2]: c[4] for c in read_index()}
    saved = [w for w in words if st.get(w) == '细节数据有']
    failed = [w for w in words if st.get(w) != '细节数据有']
    fixed = [w for w in fixed if w in saved]
    if failed:
        for w in failed:
            needs[w] = {'errors': last_err.get(w, []), 'last_draft': last_draft.get(w, []), 'when': H.now()}
        os.makedirs(RSTATE, exist_ok=True)
        H.jsave(NEEDS, needs)
        log('%d 个词改了几次仍没过，先跳过，记在 runner_state/needs_review.json：%s' % (len(failed), '、'.join(failed)))
    if not saved:
        raise Fatal('这一组一个词都没存上（%s …），看 logs/drafts/%s' % (words[0], tag))
    relabel(saved)
    done = len({c[2] for c in read_index() if c[4] == '细节数据有'})
    write_readme(b, g, saved, fixed, failed, list(dict.fromkeys(issues)), done)
    git('add', '-A', '--', D)
    msg = '%s：题目第 %d 批第 %d 组（%s … %s %d 个词）；累计 %d 个词' % (D, b, g, saved[0], saved[-1], len(saved), done)
    git('-c', 'user.name=' + CFG.get('git_name', 'Jacklee15333'), '-c', 'user.email=' + CFG.get('git_email', 'Jacklee15333@users.noreply.github.com'),
        'commit', '-q', '-m', msg, '-m', '%s\n出题模型: %s' % (TAG, CFG['llm']['label']))
    return {'group': '题目第 %d 批第 %d 组' % (b, g), 'saved': len(saved), 'failed': failed, 'done': done, 'msg': msg}


def push():
    for attempt in range(3):
        r = git_r('push', '-q', 'origin', 'HEAD:' + CFG['branch'], auth=True, check=False)
        if r.returncode == 0:
            return git('rev-parse', '--short', 'HEAD').strip()
        err = H.mask(r.stderr)
        if not any(k in err for k in ('rejected', 'non-fast-forward', 'fetch first')):
            if any(k in err for k in ('403', '401', 'Authentication', 'denied', 'Permission')):
                raise Fatal('上传被拒（令牌无效、过期或没有写权限）')
            log('上传失败，%d 秒后重试：%s' % (30 * (attempt + 1), err[-200:]))
            time.sleep(30 * (attempt + 1))
            continue
        fetch()
        base = git('merge-base', 'HEAD', origin()).strip()
        if [f for f in git('diff', '--no-renames', '--name-only', base, origin()).splitlines() if f.startswith(D + '/')]:
            raise Yield('网页对话在这期间上传了，这一组不传，让给它')
        git('rebase', '-q', origin())
    raise Fatal('上传重试 3 次都没成功')


# ---------------------------------------------------------------- 主循环
def take_lock():
    pid = int(H.jload(LOCK, {}).get('pid', 0) or 0)
    if H.pid_alive(pid):
        raise SystemExit('runner 已经在运行了（进程 %d）' % pid)
    H.jsave(LOCK, {'pid': os.getpid(), 'since': H.now()})


def relay(once=False):
    R = CFG['relay']
    ensure_clone()
    announced = False
    rstatus(state='starting', note='')
    log('接力开始：网页安静满 %d 分钟就接手；你跑 new 时它让出来' % R['takeover_minutes'])
    while True:
        if os.path.exists(STOP):
            log('看到 STOP 文件，停下')
            rstatus(state='stopped', note='STOP 文件')
            return
        try:
            fetch()
            q = quiet_minutes()
            if not once and q < R['takeover_minutes']:
                if announced:
                    log('网页那边开始写了（或你跑了 new），让出来')
                    announced = False
                rstatus(state='waiting', note='网页安静 %.0f/%d 分钟' % (max(q, 0), R['takeover_minutes']))
                time.sleep(R['check_seconds'])
                continue
            sync()
            xlsx, ver = latest_xlsx()
            v = verify(xlsx)
            if not v['left'] or v['left'] <= len(H.jload(NEEDS, {})):
                log('全部做完了')
                rstatus(state='done', note='没有“缺”的词了')
                H.notify('出题助手：全部做完了', '索引里已经没有“缺”的词了（待人工 %d 个）。' % len(H.jload(NEEDS, {})))
                return
            if not announced:
                H.notify('出题助手：DeepSeek 接手了', '网页安静 %.0f 分钟了，DeepSeek 从 %s 开始接着出题。你回来跑 new 它就让出来。' % (q, v['next']))
                announced = True
            rules, example = skill_texts()
            res = one_group(xlsx, ver, rules, example)
            if res is None:
                continue
            if quiet_minutes() < R['takeover_minutes'] and not once:
                raise Yield('你刚跑了 new（或网页刚上传），这一组不传')
            h = push()
            log('已上传 %s：%s，%d 个词，累计 %d' % (h, res['group'], res['saved'], res['done']))
            rstatus(state='idle', last=res['msg'], last_commit=h, done=res['done'], note='')
            if once:
                return
        except Yield as e:
            log(str(e))
            git('reset', '-q', '--hard', origin(), check=False)
            announced = False
            rstatus(state='waiting', note=str(e))
            time.sleep(R['check_seconds'])
        except Fatal as e:
            log('停下：%s' % e)
            rstatus(state='stopped', note=str(e)[:300])
            H.notify('出题助手：DeepSeek 接力停了', str(e)[:150])
            return
        except Exception as e:
            log('出错，1 分钟后再试：%s' % H.mask(repr(e))[:300])
            log(H.mask(traceback.format_exc()[-800:]))
            rstatus(state='waiting', note='出错后重试：%s' % repr(e)[:120])
            time.sleep(60)


def selftest():
    out = llm('你是测试助手。', '只回复两个字母：OK')
    print('DeepSeek：通了，回复 %r' % out.strip()[:30])
    return H.cmd_check_token(None)


def main():
    ap = argparse.ArgumentParser(description='DeepSeek 接力出题')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--once', action='store_true', help='不等，马上做一组（会上传）就停')
    a = ap.parse_args()
    global CFG
    CFG = load_cfg()
    H.CFG = CFG
    if a.selftest:
        try:
            sys.exit(selftest())
        except Fatal as e:
            print('✗ %s' % e)
            sys.exit(1)
    take_lock()
    try:
        relay(once=a.once)
    except KeyboardInterrupt:
        log('Ctrl+C，停下')
        rstatus(state='stopped', note='Ctrl+C')
    finally:
        if int(H.jload(LOCK, {}).get('pid', 0) or 0) == os.getpid():
            os.remove(LOCK)


if __name__ == '__main__':
    main()
