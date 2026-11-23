#!/usr/bin/env python3
"""批量出片流水线（调度）。batch.sh 调它：
  pipeline.py <批次文件夹>            跑流水线（后台常驻，做完或都卡住就自己退出）
  pipeline.py --status <批次文件夹>   打印进度表
  pipeline.py --report <批次文件夹>   写 report.md 并打印
  pipeline.py --check <批次文件夹>    开工前体检（清单、画面设置、画图脚本、环境）
批次文件夹（~/wf-batch/<批次>/）：config.env 设置，list.tsv 清单，state.json 进度，logs/ 每个词每个组的日志，cmd/ batch.sh 发来的指令。
每个词按 准备 → 配音 → 渲染 → 质检 → 交付 往下走，几个组同时干活（A 词渲染时，B 词配音、C 词准备）。
组脚本返回 0 = 做完；2 = 要人看（标“要处理”，别的词照做，处理好 batch.sh retry）；别的 = 出错（自动再试，次数用完标“出错”）。
"""
import json, os, signal, subprocess, sys, time

STAGES = ['prep', 'voice', 'render', 'check', 'deliver']
CN = {'prep': '准备', 'voice': '配音', 'render': '渲染', 'check': '质检', 'deliver': '交付', 'done': '完成', 'skipped': '跳过'}
EN = {v: k for k, v in CN.items()}
ST = {'waiting': '排队', 'running': '进行中', 'blocked': '要处理', 'failed': '出错', 'qa': '等人看', '': ''}
HERE = os.path.dirname(os.path.abspath(__file__))


def read_env(p):
    d = {}
    if os.path.exists(p):
        for l in open(p, encoding='utf-8'):
            l = l.strip()
            if l and not l.startswith('#') and '=' in l:
                k, v = l.split('=', 1)
                d[k.strip()] = v.strip().strip('"').strip("'")
    return d


def load_list(p):
    rows = []
    for l in open(p, encoding='utf-8'):
        if not l.strip() or l.lstrip().startswith('#'):
            continue
        c = l.rstrip('\n').replace('\r', '').split('\t')
        if len(c) >= 3 and c[1].strip():
            rows.append({'no': c[0].strip(), 'word': c[1].strip(), 'arts': c[2].strip(), 'note': c[3].strip() if len(c) > 3 else ''})
    return rows


def mem_gb():
    try:
        return next(int(l.split()[1]) for l in open('/proc/meminfo') if l.startswith('MemTotal')) / 1048576
    except Exception:
        return 4


def gpu_info(cfg):
    """第八十版：~/.wordfilm-gpu.env（local-wordfilm 的 04_gpu.sh 测好写的）里哪几样用显卡、显存多大；批次设 GPU=0 = 不用"""
    p = os.path.expanduser('~/.wordfilm-gpu.env')
    if cfg.get('GPU', '1') == '0' or not os.path.exists(p):
        return {}
    d = {}
    for l in open(p, encoding='utf-8'):
        l = l.strip()
        if l.startswith('export '):
            l = l[7:]
        if '=' in l and l.startswith('WORDFILM_'):
            k, v = l.split('=', 1)
            d[k] = v.strip().strip('"').strip("'")
    return d


def plan_resources(cfg):
    """按 CPU、内存、显卡定：准备组同时几个词、配音几个进程、渲染几个浏览器；第八十版起配音组、渲染组同时做几个词（LANE_VOICE、LANE_RENDER）。
    以前两组都只能一次做一个词，配音一个词要 3～8 分钟，整批卡在配音上。配音用上显卡以后快很多、也不太吃 CPU，内存够就两个词一起念；
    画面用显卡编码以后 CPU 都给浏览器画画面，内存够就两个词一起渲染。内存小就不让配音和渲染同时跑"""
    cpu, mem = os.cpu_count() or 1, mem_gb()
    g = gpu_info(cfg)
    voice_gpu = g.get('WORDFILM_ZV_DEVICE') == 'cuda'
    enc_gpu = g.get('WORDFILM_ENCODER') == 'nvenc'
    vram = float(g.get('WORDFILM_GPU_MEM_GB') or 0)
    # 第八十一版：画面用显卡编码时，一个词的渲染用上尽量多的浏览器（RENDER_JOBS=0：render.py 按核数和空闲内存定，最多 16 个），
    #   一次只渲染一个词——比两个词各开几个浏览器先出片；配音用显卡时配音组同时念两个词
    if mem >= 22 and cpu >= 12:
        auto = {'LANE_PREP': 2, 'SYNTH_JOBS': 2 if voice_gpu else 3, 'RENDER_JOBS': 0 if enc_gpu else 5,
                'LANE_VOICE': 2 if voice_gpu and vram >= 10 else 1, 'LANE_RENDER': 1}
    elif mem >= 14 and cpu >= 8:
        auto = {'LANE_PREP': 1, 'SYNTH_JOBS': 2, 'RENDER_JOBS': 0 if enc_gpu else 4,
                'LANE_VOICE': 2 if voice_gpu and vram >= 10 else 1, 'LANE_RENDER': 1}
    else:
        auto = {'LANE_PREP': 1, 'SYNTH_JOBS': 1, 'RENDER_JOBS': 1, 'LANE_VOICE': 1, 'LANE_RENDER': 1}
    r = {k: int(cfg.get(k) or v) for k, v in auto.items()}
    r['GPU'] = '、'.join(x for x, on in (('配音', voice_gpu), ('画面编码', enc_gpu), ('浏览器画画面', g.get('WORDFILM_BROWSER_GPU') == '1'),
                                         ('显卡转 NV12 传帧', g.get('WORDFILM_CAPTURE') == 'nv12')) if on) or '不用'
    r['mem_hint'] = mem < 22 and cpu >= 12
    r['TOGETHER'] = cfg.get('HEAVY_TOGETHER', '1' if mem >= 8 else '0') == '1'
    r['cpu'], r['mem'] = cpu, round(mem, 1)
    return r


def fmt_secs(s):
    s = int(max(0, s))
    return '%d:%02d:%02d' % (s // 3600, s % 3600 // 60, s % 60) if s >= 3600 else '%d:%02d' % (s // 60, s % 60)


class Pipeline:
    def __init__(self, bdir):
        self.bdir = os.path.abspath(bdir)
        self.sp = os.path.join(self.bdir, 'state.json')
        self.procs = {}           # word -> (Popen, stage, logfile)
        self.stopping = False
        self.cfg = read_env(os.path.join(self.bdir, 'config.env'))
        if os.path.exists(self.sp):
            self.state = json.load(open(self.sp, encoding='utf-8'))
        else:
            self.state = {'words': [dict(r, stage='prep', status='waiting', msg='', tries={}, t={}) for r in load_list(os.path.join(self.bdir, 'list.tsv'))]}
        for w in self.state['words']:          # 上次停在半路的（WSL 关了、stop 了）：这一组从头再做（缓存都在，快）
            if w['status'] == 'running':
                w['status'] = 'waiting'

    def save(self):
        self.state['updated'] = time.time()
        tmp = self.sp + '.tmp'
        json.dump(self.state, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        os.replace(tmp, self.sp)

    def find(self, word):
        return next((w for w in self.state['words'] if w['word'] == word), None)

    def env(self, res):
        e = dict(os.environ)
        e.update(self.cfg)
        e.update({'SYNTH_JOBS': str(res['SYNTH_JOBS']), 'RENDER_JOBS': str(res['RENDER_JOBS']), 'UNIT': self.cfg.get('UNIT', 'batch')})
        return e

    def launch(self, w, stage, res):
        os.makedirs(os.path.join(self.bdir, 'logs'), exist_ok=True)
        log = os.path.join(self.bdir, 'logs', '%s.%s.log' % (w['word'], stage))
        f = open(log, 'a', encoding='utf-8')
        f.write('\n===== %s 开始 %s =====\n' % (CN[stage], time.strftime('%m-%d %H:%M:%S')))
        f.flush()
        script = os.path.join(HERE, 'fake_stage.sh' if self.cfg.get('FAKE') == '1' else 'stage_%s.sh' % stage)
        p = subprocess.Popen(['bash', script, w['no'], w['word'], w['arts']], stdout=f, stderr=subprocess.STDOUT,
                             stdin=subprocess.DEVNULL, env=dict(self.env(res), BATCH_STAGE=stage, BATCH_DIR=self.bdir), start_new_session=True)
        self.procs[w['word']] = (p, stage, f)
        w['status'], w['msg'] = 'running', ''
        w['t'][stage] = [time.time(), None]

    def last_msg(self, log_path):
        try:
            lines = [l.strip() for l in open(log_path, encoding='utf-8', errors='replace').read().splitlines() if l.strip()]
        except OSError:
            return ''
        for l in reversed(lines[-80:]):
            if l[:1] in ('⚠', '❌', '✅'):
                return l[:300]
        return lines[-1][:300] if lines else ''

    def finish(self, word, rc):
        p, stage, f = self.procs.pop(word)
        f.write('===== %s 结束（返回码 %s）%s =====\n' % (CN[stage], rc, time.strftime('%m-%d %H:%M:%S')))
        f.close()
        w = self.find(word)
        if w is None or w['stage'] != stage:
            return
        w['t'][stage][1] = time.time()
        msg = self.last_msg(f.name)
        if rc == 0:
            i = STAGES.index(stage)
            stop_after = self.cfg.get('STOP_AFTER', '')
            if i + 1 >= len(STAGES) or stage == EN.get(stop_after, stop_after):
                w['stage'], w['status'], w['msg'] = 'done', '', ''
            else:
                w['stage'] = STAGES[i + 1]
                w['status'] = 'qa' if stage == 'check' and self.cfg.get('HOLD_QA') == '1' else 'waiting'
                w['msg'] = '自动质检过了，等人看关键画面图（batch.sh ok）' if w['status'] == 'qa' else ''
        elif rc == 2:
            w['status'], w['msg'] = 'blocked', msg
        else:
            n = w['tries'].get(stage, 0) + 1
            w['tries'][stage] = n
            if n < int(self.cfg.get('MAX_TRIES', 2)):
                w['status'], w['msg'] = 'waiting', '上一次出错（%s），自动再试' % msg
            else:
                w['status'], w['msg'] = 'failed', msg

    def kill(self, word):
        if word in self.procs:
            p = self.procs[word][0]
            try:
                os.killpg(p.pid, signal.SIGTERM)
            except OSError:
                pass

    def commands(self):
        d = os.path.join(self.bdir, 'cmd')
        if not os.path.isdir(d):
            return
        for name in sorted(os.listdir(d)):
            path = os.path.join(d, name)
            try:
                c = json.load(open(path, encoding='utf-8'))
            except Exception:
                c = {}
            os.remove(path)
            op, w = c.get('op'), self.find(c.get('word', ''))
            if op == 'stop':
                self.stopping = True
            elif op == 'reload':
                have = {x['word'] for x in self.state['words']}
                rows = load_list(os.path.join(self.bdir, 'list.tsv'))
                for r in rows:
                    if r['word'] not in have:
                        self.state['words'].append(dict(r, stage='prep', status='waiting', msg='', tries={}, t={}))
                byw = {r['word']: r for r in rows}
                for x in self.state['words']:          # 清单里改过的序号、画图脚本，下次做这个词时用新的
                    if x['word'] in byw:
                        x.update({k: byw[x['word']][k] for k in ('no', 'arts', 'note')})
            elif w is None:
                continue
            elif op == 'retry':
                self.kill(w['word'])
                st = EN.get(c.get('stage') or '', c.get('stage') or '')
                if st in STAGES:
                    w['stage'] = st
                elif w['stage'] == 'skipped':          # 第八十三版：跳过的词 retry 不带阶段，从准备重做（以前被忽略，流水线一开就退出）
                    w['stage'] = 'prep'
                elif w['stage'] == 'done':
                    continue
                r = next((x for x in load_list(os.path.join(self.bdir, 'list.tsv')) if x['word'] == w['word']), None)
                if r:
                    w.update({k: r[k] for k in ('no', 'arts', 'note')})
                w['status'], w['msg'] = 'waiting', ''
                w['tries'][w['stage']] = 0
            elif op == 'skip':
                self.kill(w['word'])
                w['stage'], w['status'], w['msg'] = 'skipped', '', c.get('why', '')
            elif op == 'ok' and w['status'] == 'qa':
                w['status'], w['msg'] = 'waiting', ''

    def schedule(self, res):
        cap = {'prep': res['LANE_PREP'], 'voice': res.get('LANE_VOICE', 1), 'render': res.get('LANE_RENDER', 1),
               'check': 1, 'deliver': 1}
        busy = {s: sum(1 for _, (p, st, _) in self.procs.items() if st == s) for s in STAGES}
        for stage in reversed(STAGES):            # 先让后面的组接活：做好的尽快交付
            for w in self.state['words']:
                if busy[stage] >= cap[stage]:
                    break
                if w['stage'] != stage or w['status'] != 'waiting' or w['word'] in self.procs:
                    continue
                if stage in ('voice', 'render') and not res['TOGETHER'] and (busy['voice'] or busy['render']):
                    break                          # 内存小：配音、渲染一次只跑一样
                self.launch(w, stage, res)
                busy[stage] += 1

    def run(self):
        pid_p = os.path.join(self.bdir, 'pipeline.pid')
        open(pid_p, 'w').write(str(os.getpid()))
        signal.signal(signal.SIGTERM, lambda *a: setattr(self, 'stopping', True))
        signal.signal(signal.SIGINT, lambda *a: setattr(self, 'stopping', True))
        print('流水线开始 %s（%s）' % (time.strftime('%m-%d %H:%M:%S'), self.bdir), flush=True)
        try:
            while True:
                self.cfg = read_env(os.path.join(self.bdir, 'config.env'))   # set 改的设置马上生效（下一个词开始用）
                res = plan_resources(self.cfg)
                self.state['resources'] = res
                self.commands()
                for word, (p, stage, f) in list(self.procs.items()):
                    rc = p.poll()
                    if rc is not None:
                        self.finish(word, rc)
                if self.stopping:
                    for word in list(self.procs):
                        self.kill(word)
                    time.sleep(3)
                    for word, (p, stage, f) in list(self.procs.items()):
                        f.write('===== 停下（batch.sh stop）=====\n'); f.close()
                        w = self.find(word); w['status'] = 'waiting'; w['msg'] = '停下了，start 以后这一组从头做'
                        self.procs.pop(word)
                    break
                self.schedule(res)
                self.save()
                if not self.procs and not any(w['status'] == 'waiting' for w in self.state['words']):
                    break
                time.sleep(2)
        finally:
            self.save()
            try:
                os.remove(pid_p)
            except OSError:
                pass
            write_report(self.bdir, quiet=True)
            print('流水线停了 %s' % time.strftime('%m-%d %H:%M:%S'), flush=True)


def load_state(bdir):
    p = os.path.join(bdir, 'state.json')
    if os.path.exists(p):
        return json.load(open(p, encoding='utf-8'))
    return {'words': [dict(r, stage='prep', status='waiting', msg='', tries={}, t={}) for r in load_list(os.path.join(bdir, 'list.tsv'))]}


def alive(bdir):
    try:
        os.kill(int(open(os.path.join(bdir, 'pipeline.pid')).read()), 0)
        return True
    except Exception:
        return False


def took(w):
    ts = [v for v in w.get('t', {}).values() if v and v[0]]
    if not ts:
        return ''
    end = max((v[1] or time.time()) for v in ts)
    return fmt_secs(end - min(v[0] for v in ts))


def speed_lines(st):
    """第八十一版：做好的词平均几分钟出一个（从开工到最后一个做好），各组平均用时"""
    done = [w for w in st['words'] if w['stage'] == 'done']
    starts = [v[0] for w in st['words'] for v in w.get('t', {}).values() if v and v[0]]
    if not done or not starts:
        return []
    t1 = max(v[1] for w in done for v in w['t'].values() if v and v[1])
    out = ['速度：做好 %d 个，平均 %.1f 分钟出一个（从开工算）' % (len(done), (t1 - min(starts)) / 60 / len(done))]
    avg = []
    for s in STAGES:
        ds = [w['t'][s][1] - w['t'][s][0] for w in done if w.get('t', {}).get(s) and w['t'][s][1]]
        if ds:
            avg.append('%s %s' % (CN[s], fmt_secs(sum(ds) / len(ds))))
    if avg:
        out.append('各组平均（一个词）：' + '、'.join(avg))
    return out


def status(bdir):
    st = load_state(bdir)
    ws = st['words']
    cnt = {}
    for w in ws:
        k = '完成' if w['stage'] == 'done' else '跳过' if w['stage'] == 'skipped' else ST.get(w['status'], w['status'])
        cnt[k] = cnt.get(k, 0) + 1
    name = os.path.basename(bdir.rstrip('/'))
    print('批次 %s：流水线%s｜%d 个词：%s' % (name, '在跑' if alive(bdir) else '没在跑', len(ws), '、'.join('%s %d' % kv for kv in cnt.items())))
    r = st.get('resources')
    if r:
        print('分工：准备组同时 %d 个词；配音组同时 %d 个词、每个 %d 个进程；渲染组同时 %d 个词、每个 %s 个浏览器；%s；显卡：%s（%d 核、%.0f GB）' % (
            r['LANE_PREP'], r.get('LANE_VOICE', 1), r['SYNTH_JOBS'], r.get('LANE_RENDER', 1), r['RENDER_JOBS'] or '自动（按核数）', '配音和渲染同时跑' if r['TOGETHER'] else '配音和渲染轮流跑',
            r.get('GPU', '不用'), r['cpu'], r['mem']))
        if r.get('mem_hint'):
            print('提示：WSL 只分到 %.0f GB 内存；照 local-wordfilm 的 set_wsl_memory.ps1 调到 24 GB，配音、渲染可以各开两条道' % r['mem'])
    for l in speed_lines(st):
        print(l)
    print('%-4s %-15s %-4s %-6s %-8s %s' % ('序号', '词', '阶段', '状态', '用时', '说明'))
    for w in ws:
        stage = CN.get(w['stage'], w['stage'])
        s = '' if w['stage'] in ('done', 'skipped') else ST.get(w['status'], w['status'])
        print('%-4s %-15s %-4s %-6s %-8s %s' % (w['no'], w['word'], stage, s, took(w), (w.get('msg') or '')[:90]))
    todo = [w for w in ws if w['status'] in ('blocked', 'failed', 'qa') and w['stage'] not in ('done', 'skipped')]
    if todo:
        print('\n要处理（%d 个）：' % len(todo))
        for w in todo:
            print('  %s %s（%s，%s）：%s\n     看日志：batch.sh log %s %s %s' % (w['no'], w['word'], CN[w['stage']], ST[w['status']], w.get('msg', ''),
                                                                         name, w['word'], CN[w['stage']]))


def write_report(bdir, quiet=False):
    st = load_state(bdir)
    name = os.path.basename(bdir.rstrip('/'))
    L = ['# 批次 %s 报告（%s）' % (name, time.strftime('%Y-%m-%d %H:%M')), '',
         '| 序号 | 词 | 结果 | 准备 | 配音 | 渲染 | 质检 | 交付 | 合计 | 说明 |', '|---|---|---|---|---|---|---|---|---|---|']
    for w in st['words']:
        res = '完成' if w['stage'] == 'done' else '跳过' if w['stage'] == 'skipped' else '%s·%s' % (CN.get(w['stage']), ST.get(w['status'], ''))
        cells = []
        for s in STAGES:
            v = w.get('t', {}).get(s)
            cells.append(fmt_secs((v[1] or time.time()) - v[0]) if v and v[0] else '')
        L.append('| %s | %s | %s | %s | %s | %s |' % (w['no'], w['word'], res, ' | '.join(cells), took(w), (w.get('msg') or '').replace('|', '／')[:80]))
    done = [w for w in st['words'] if w['stage'] == 'done']
    L += ['', '完成 %d / %d 个。' % (len(done), len(st['words']))] + speed_lines(st)
    np = os.path.join(bdir, 'notes.md')
    if os.path.exists(np):
        L += ['', '## 制作中替用户做的处理', ''] + open(np, encoding='utf-8').read().strip().splitlines()
    open(os.path.join(bdir, 'report.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    if not quiet:
        print('\n'.join(L))


def check(bdir):
    rows = load_list(os.path.join(bdir, 'list.tsv'))
    home = os.path.expanduser('~')
    kits = [os.path.join(home, 'kit-extra'), os.path.join(home, 'kit')]
    def kfile(rel):
        return next((os.path.join(k, rel) for k in kits if os.path.exists(os.path.join(k, rel))), None)
    bad = 0
    seen = set()
    print('清单 %d 个词：' % len(rows))
    for r in rows:
        probs = []
        if not r['no'].isdigit():
            probs.append('序号不是数字')
        if r['word'] in seen:
            probs.append('重复')
        seen.add(r['word'])
        if not kfile('words/%s.py' % r['word']):
            probs.append('没有画面设置 words/%s.py（画面组先做）' % r['word'])
        miss = [x for x in r['arts'].split(',') if x and not kfile('%s_art.py' % x)]
        if miss:
            probs.append('没有画图脚本 ' + '、'.join(x + '_art.py' for x in miss))
        bad += bool(probs)
        print('  %s %-15s %-34s %s' % (r['no'], r['word'], r['arts'], '；'.join(probs) if probs else 'OK'))
    envf = os.path.join(home, '.wordfilm-local.env')
    e = read_env(envf)
    e.update(read_env(os.path.join(bdir, 'config.env')))
    S = os.path.join(home, 'skills', 'word-construction-video')
    ver = ''
    try:
        ver = next(l.split('（')[0].replace('当前 ', '') for l in open(os.path.join(S, 'SKILL.md'), encoding='utf-8') if l.startswith('当前 6.'))
    except Exception:
        pass
    print('环境：视频技能 %s%s；总表 %s；音节表 %s' % (ver or '没找到', '' if ver >= '6.35' else '（批量要 6.35 / 第七十九版以上：按 local-wordfilm 再跑一次 02_get_repo.sh）',
                                        '有' if os.path.exists(e.get('TABLE', '')) else '没找到', '有' if os.path.exists(e.get('SYL', '')) else '没找到'))
    r = plan_resources(read_env(os.path.join(bdir, 'config.env')))
    print('分工：准备组同时 %d 个词；配音组同时 %d 个词、每个 %d 个进程；渲染组同时 %d 个词、每个 %s 个浏览器；%s；显卡：%s（%d 核、%.0f GB）' % (
        r['LANE_PREP'], r.get('LANE_VOICE', 1), r['SYNTH_JOBS'], r.get('LANE_RENDER', 1), r['RENDER_JOBS'] or '自动（按核数）', '配音和渲染同时跑' if r['TOGETHER'] else '配音和渲染轮流跑',
        r.get('GPU', '不用'), r['cpu'], r['mem']))
    if r.get('mem_hint'):
        print('提示：WSL 只分到 %.0f GB 内存；照 local-wordfilm 的 set_wsl_memory.ps1 调到 24 GB，配音、渲染可以各开两条道' % r['mem'])
    print('体检：%s' % ('有 %d 个词要先处理（见上面）' % bad if bad else '清单都 OK'))


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] in ('--status', '--report', '--check'):
        {'--status': status, '--report': write_report, '--check': check}[sys.argv[1]](sys.argv[2])
    elif len(sys.argv) == 2:
        Pipeline(sys.argv[1]).run()
    else:
        print(__doc__)
