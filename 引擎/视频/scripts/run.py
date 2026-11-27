#!/usr/bin/env python3
"""一条命令做一批构词动画：读词源总表 → 起草配音稿 → 核对扩展词 → 合成配音并逐句检查发音 → 渲染视频 → 截图检查。

  python3 run.py --table 词源总表.xlsx --words transport,communication --out /mnt/user-data/outputs/构词动画
  python3 run.py --table 词源总表.xlsx --unit-list 6A-9A.xlsx --book 7A --unit 3 --out /mnt/user-data/outputs/构词动画_7A_Unit3

选项：
  --syl 音节表.xlsx       音节划分表（“音节划分_总词库7869词_细分版.xlsx”这种）：视频开头做“一、读音拆分”。
                         不写的话，在总表旁边和 /mnt/user-data/uploads/ 里找文件名带“音节”的 xlsx；--no-syl 不要读音拆分
  --style core|full      core（默认，只讲核心，半分钟到一分钟）/ full（详细版，两三分钟，讲来历、意思怎么变过来、同一词族）
  --draft-only           只起草、出预览图（每个词 <work>/<单词>/preview.png），不配音不渲染：先看画、补 pics，再正式跑
  --edits edits.json     一批词要改的画面设置：{"单词": {"pics": [...], "extend": [...], "icons": {...}, ...}}，合并进各自的 prefs.json
  --pool 表              扩展词还必须在这张表里（默认只要在词源总表里）；--prefer 表：这张表里的词排前面（给了 --unit-list 时默认用它）
  --silent               不要配音（快，适合先看画面）
  --redraft              重新起草配音稿（默认：plan.json 手改过就不动；没手改过的会跟着最新的画面设置重新起草）
  --force                有没听清的句子、不在总表里的扩展词也照样渲染
  --work 文件夹           中间文件放哪（默认 ~/wordfilm-work）：每个词一个文件夹，里面 plan.json、prefs.json、audio/、preview.png、qa.png
  --no-qa                不做截图检查

一条命令最多跑 5 分钟，要放后台跑，而且要用 setsid（只用 nohup 的话，命令一结束进程可能被停掉）：
  setsid nohup python3 run.py … > ~/wordfilm-work/run.log 2>&1 < /dev/null &      然后隔一会儿  tail ~/wordfilm-work/run.log
"""
import argparse, hashlib, json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import voice_config  # noqa: E402  （5.3 起）配音用哪个声音


def sh(cmd, quiet=False):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 3 and 'render.py' in ' '.join(cmd[:2]):      # 5.11：渲染到一半时间用完了（--budget），做好的段留着
        print(r.stdout.rstrip())
        raise SystemExit('==== 还没做完：再跑同一条命令接着做（配好的音、渲染好的段都会复用）====')
    if r.returncode != 0:
        print(r.stdout[-2000:], r.stderr[-3000:])
        raise SystemExit('出错了：' + ' '.join(cmd[:3]))
    if not quiet and r.stdout.strip():
        print(r.stdout.rstrip())
    return r.stdout


def safe(w):
    return re.sub(r'[\\/:*?"<>|\s]+', '_', w).strip('._') or 'word'


def load(p, dflt=None):
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception:
        return dflt


def drop_unknown(t, i, prefs, pool):
    """6.56：扩展词、同族词、小黑板“扩展”那一行里不在总表的词，去掉（画面设置里 AI 多写的），返回去掉了哪些。
    用户的批次 1127-1：make 卡在“渲染：先不渲染”，日志里看不到是哪个词——这些词少了也不影响视频，去掉接着做"""
    from ety_table import key_of
    ok = lambda w: key_of(w) in t.by_key and (pool is None or key_of(w) in pool)
    gone = []
    if isinstance(prefs.get('extend'), list):
        _, bad = t.normalize_extend(i, prefs['extend'], pool)
        if bad:
            bset = {key_of(b) for b in bad}
            keep = [x for x in prefs['extend'] if key_of(x.get('w', '') if isinstance(x, dict) else str(x)) not in bset]
            gone += list(bad)
            prefs['extend'] = keep
    if isinstance(prefs.get('familyWords'), list):
        bad = [w for w in prefs['familyWords'] if not ok(w)]
        if bad:
            gone += bad
            prefs['familyWords'] = [w for w in prefs['familyWords'] if ok(w)]
    board = prefs.get('board')
    if isinstance(board, dict) and isinstance(board.get('lines'), list):
        keep = []
        for ln in board['lines']:
            if isinstance(ln, dict) and str(ln.get('label', '')) in ('扩展', '扩展词', '同根', '同族'):
                text = ' '.join(str(sg[0]) for sg in ln.get('segs') or [] if sg)
                bad = [w for w in re.findall(r"[A-Za-z][A-Za-z'-]+", text) if not ok(w)]
                if bad:
                    gone += bad
                    continue
            keep.append(ln)
        board['lines'] = keep
    return gone


def check_words(t, i, prefs, pool, prefer):
    """扩展词、同一词族手写的词都要在总表（和 --pool）里。返回（要不要写回 prefs，问题列表）"""
    from ety_table import key_of
    probs, changed = [], False
    ok = lambda w: key_of(w) in t.by_key and (pool is None or key_of(w) in pool)
    if isinstance(prefs.get('extend'), list):
        norm, bad = t.normalize_extend(i, prefs['extend'], pool)
        if bad:
            probs.append('扩展词不在总表里：' + '、'.join(bad))
        elif norm != prefs['extend']:
            prefs['extend'], changed = norm, True        # 补上意思、共用的部分
    bad = [w for w in prefs.get('familyWords') or [] if not ok(w)]
    if bad:
        probs.append('同一词族手写的词不在总表里：' + '、'.join(bad))
    board = prefs.get('board')
    if isinstance(board, dict):
        for ln in board.get('lines') or []:
            if isinstance(ln, dict) and str(ln.get('label', '')) in ('扩展', '扩展词', '同根', '同族'):
                text = ' '.join(str(sg[0]) for sg in ln.get('segs') or [] if sg)
                bad = [w for w in re.findall(r"[A-Za-z][A-Za-z'-]+", text) if not ok(w)]
                if bad:
                    probs.append('小黑板手写的扩展词不在总表里：' + '、'.join(bad))
    if probs:
        probs.append('可以换成：' + '、'.join(r['w'] + ' ' + r['m'] for r in t.related(i, pool, prefer)[:8]))
    return changed, probs


def find_syl_table(table):
    """没写 --syl：在总表旁边、上传文件夹里找文件名带“音节”的 xlsx（最新的那个）"""
    import glob
    cands = []
    for d in {os.path.dirname(os.path.abspath(table)), '/mnt/user-data/uploads'}:
        cands += [p for p in glob.glob(os.path.join(d, '*.xlsx')) if '音节' in os.path.basename(p)]
    return max(cands, key=os.path.getmtime) if cands else None


def attach_pron(entry, w, syl_data, prefs, unit_ipa):
    """这个词的读音拆分 → entry['pron']；prefs 里 "pron": false 不要，"ipa" 整词音标、"sylIpa" 每一块的音标（手写为准）"""
    import syllables
    entry.pop('pron', None)
    if prefs.get('pron') is False:
        return '读音拆分：prefs 写了 "pron": false，不做'
    e, how = syllables.find(syl_data, entry.get('w') or w)
    if not e:
        return '读音拆分：%s，这个视频没有读音拆分那一部分' % how
    ipa = prefs.get('ipa') or unit_ipa.get(w.lower()) or unit_ipa.get(str(entry.get('w', '')).lower())
    pr = syllables.pron(e, entry.get('w') or w, ipa=ipa, chunk_ipa=prefs.get('sylIpa'))
    entry['pron'] = pr
    return '读音拆分：' + syllables.describe(pr) + (('（' + how + '）') if how else '')


T0 = time.time()



# 6.19：两个版本——精简版放前面（文件名 _1精简版，排在前面），详解版就是原来的视频（_2详解版）
EDITIONS = {'both': ['brief', 'detail'], 'brief': ['brief'], 'detail': ['detail']}
EDITION_FILE = {'brief': '_构词动画_1精简版.mp4', 'detail': '_构词动画_2详解版.mp4'}      # 6.26 以前的名字（deliver.py 还认）
# 6.27（第六十七版，用户：“视频的名字要简化一下：32_store_构词动画_精简版 变成：32 store”）：精简版就叫“单词.mp4”，详解版“单词（详解）.mp4”；
# 一个单元一批做（--unit-list）或者写了 --numbered，前面加单元里的序号：“32 store.mp4”“12 text message.mp4”
EDITION_NAME_FMT = {'brief': '%s.mp4', 'detail': '%s（详解）.mp4'}


def video_name(w, ed, num=None):
    base = re.sub(r'[\\/:*?"<>|]+', ' ', w).strip() or 'word'
    return ('%02d ' % num if num else '') + EDITION_NAME_FMT[ed] % base
EDITION_NAME = {'brief': '精简版', 'detail': '详解版'}


def brief_prefs(p):
    """精简版的画面设置：详解版的 prefs，再加上不讲的几样（用户：“精简版词根词缀的各种音变，各种形态这些不讲，直降关键的部分”）：
    音变（卡片上那一行、配音那一句，“为什么 p 会变成 f？”那一幕）、形态、辨析 / 身份和分工、总结里“变化”那一行。
    6.31 起考点固定要讲：详解版的 prefs 写了 "kaodian": false，精简版也照讲（总表「考点」列空着的，起草的“还要补”会列出来）。
    想在精简版里留下哪一样，在这个词的 prefs.json 写 "brief": {"fengong": true} 这样的覆盖"""
    q = json.loads(json.dumps(p or {}))
    over = q.get('brief') if isinstance(q.get('brief'), dict) else {}
    q.update({'yinbian': False, 'xingtai': False, 'fengong': False})
    if q.get('board') is not False:
        b = dict(q['board']) if isinstance(q.get('board'), dict) else {}
        b['verb'] = False
        q['board'] = b
    q['lean'] = True      # 6.43（第八十七版）：精简版再精简——读音拆分只念块、词缀词根直接说“英语前缀”、同义词辨析只念单词给特写；某个词想要原来的精简版，prefs 写 "brief": {"lean": false}
    q.update(over)
    if q.get('kaodian') is False:                       # 6.31（第七十五版，用户：“我希望能在做精简版的视频时，也要把考点给加上去”）：精简版固定带考点
        q.pop('kaodian')
    q['brief'] = True
    return q


def make_brief(wdir, prefs_p, details, w, style, list_json, redraft):
    """<work>/<单词>/brief/：精简版的 prefs.json、配音稿；art 和配音缓存连到详解版那一份"""
    ew = os.path.join(wdir, 'brief')
    os.makedirs(os.path.join(ew, 'audio'), exist_ok=True)
    for src, dst in ((os.path.join(wdir, 'art'), os.path.join(ew, 'art')), (os.path.join(wdir, 'audio', 'cache'), os.path.join(ew, 'audio', 'cache'))):
        if src.endswith('cache'):
            os.makedirs(src, exist_ok=True)
        src = os.path.realpath(src)              # 6.55：连到真的文件夹，不经过 ~/wf-jobs/<词>/<词> 这种中转链接（中转的删了，这里就悬空：配音崩“File exists”）
        if os.path.islink(dst) and (not os.path.exists(dst) or os.path.realpath(dst) != src):
            os.remove(dst)                       # 6.55：悬空的、连错的，换掉
        if os.path.isdir(src) and not os.path.lexists(dst):
            os.symlink(src, dst)
    bp = os.path.join(ew, 'prefs.json')
    json.dump(brief_prefs(load(prefs_p, {})), open(bp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    plan_p, auto_p = os.path.join(ew, 'plan.json'), os.path.join(ew, 'plan.auto.json')
    untouched = os.path.exists(plan_p) and os.path.exists(auto_p) and open(plan_p, 'rb').read() == open(auto_p, 'rb').read()
    if redraft or not os.path.exists(plan_p) or untouched:
        cmd = ['node', os.path.join(HERE, 'draft_plan.js'), details, w, ew, '--style', style] + (['--list', list_json] if list_json else [])
        sh(cmd, quiet=True)
    plan = load(plan_p, {}) or {}
    print('精简版：配音稿 %s（%d 幕，详解版 %d 幕）' % (plan_p, len(plan.get('scenes') or {}), len((load(os.path.join(wdir, 'plan.json'), {}) or {}).get('scenes') or {})))
    return ew, plan_p, bp

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--table', required=True, help='词源总表 xlsx')
    ap.add_argument('--syl', help='音节划分表 xlsx（读音拆分）')
    ap.add_argument('--no-syl', action='store_true')
    ap.add_argument('--words', help='逗号隔开的单词')
    ap.add_argument('--unit-list', help='按册、单元排的单词表 xlsx（6A-9A.xlsx 这种）')
    ap.add_argument('--book')
    ap.add_argument('--unit', type=int)
    ap.add_argument('--section', default='main')
    ap.add_argument('--out', required=True)
    ap.add_argument('--work', default=os.path.expanduser('~/wordfilm-work'))
    ap.add_argument('--style', default='core', choices=['core', 'full', 'compact'])
    ap.add_argument('--edits')
    ap.add_argument('--pool')
    ap.add_argument('--prefer')
    ap.add_argument('--draft-only', action='store_true')
    ap.add_argument('--no-preview', action='store_true', help='--draft-only 时不出预览图（只看配音稿和“还要补”，一个词一两秒）')
    ap.add_argument('--preview-cell', type=int, default=640, help='--draft-only 出的预览图每一格的宽度（像素）：默认 640；只看图不做视频时用 960，小字看得清')
    ap.add_argument('--silent', action='store_true')
    ap.add_argument('--redraft', action='store_true')
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--no-qa', action='store_true')
    ap.add_argument('--edition', default='both', choices=['both', 'brief', 'detail'],
                    help='6.19：出哪个版本：both（默认，两个都出：<单词>_构词动画_1精简版.mp4、_2详解版.mp4）、brief（只出精简版）、detail（只出详解版）')
    ap.add_argument('--numbered', action='store_true', help='6.27：文件名前面加序号（按 --words 里的先后：01 camera.mp4、02 speaker.mp4…）；--unit-list 做一个单元时自动加')
    ap.add_argument('--number', help='6.27：只做一个词时指定它的序号（--words store --number 32 → 32 store.mp4）')
    ap.add_argument('--budget', type=float, default=0, help='这一条命令最多跑多少秒（0 = 不限）。沙盒里一条命令最多 5 分钟、后台进程也可能被停掉：写 --budget 240 放前台跑，没做完就再跑一次，接着做')
    a = ap.parse_args()
    style = 'core' if a.style == 'compact' else a.style
    os.makedirs(a.work, exist_ok=True)
    os.makedirs(a.out, exist_ok=True)
    t_start = time.time()

    # 1. 词源总表 → ety.json（表改过才重读）
    ety = os.path.join(a.work, 'ety.json')
    if not os.path.exists(ety) or os.path.getmtime(ety) < os.path.getmtime(a.table):
        sh(['python3', os.path.join(HERE, 'ety_table.py'), 'build', a.table, ety])

    # 2. 要做哪些词
    list_json = None
    if a.unit_list:
        list_json = os.path.join(a.work, 'unit_%s_%d.json' % (a.book, a.unit))
        out = sh(['python3', os.path.join(HERE, 'unit_words.py'), a.unit_list, a.book, str(a.unit), '--section', a.section, '--json', list_json])
        words = out.strip().splitlines()[-1].split(',')
    else:
        words = [w.strip() for w in re.split(r'[,，]', a.words or '') if w.strip()]
    if not words:
        raise SystemExit('没有要做的单词：用 --words 或者 --unit-list/--book/--unit')
    order = {w: i + 1 for i, w in enumerate(words)} if (a.unit_list or a.numbered) else {}      # 6.27：文件名前面的序号
    prefer = a.prefer or a.unit_list
    details = os.path.join(a.work, 'details.json')
    cmd = ['python3', os.path.join(HERE, 'ety_table.py'), 'detail', ety, ','.join(words), details]
    if a.pool:
        cmd += ['--pool', a.pool]
    if prefer:
        cmd += ['--prefer', prefer]
    sh(cmd)
    found = load(details, {})
    from ety_table import Table, load_words
    table = Table(ety)
    pool = load_words(a.pool) if a.pool else None
    prefer_set = load_words(prefer) if prefer else None
    edits = load(a.edits, {}) if a.edits else {}
    if a.edits and not edits:
        raise SystemExit('读不了 ' + a.edits + '（要是 {"单词": {...}} 这样的 json）')

    # 5.0 起：音节划分表 → syl.json（表改过才重读）；每个词的读音拆分放进 details.json 的 pron
    syl_data, syl_path = None, None
    if not a.no_syl:
        syl_path = a.syl or find_syl_table(a.table)
        if syl_path:
            sj = os.path.join(a.work, 'syl.json')
            if not os.path.exists(sj) or os.path.getmtime(sj) < os.path.getmtime(syl_path):
                sh(['python3', os.path.join(HERE, 'syllables.py'), 'build', syl_path, sj])
            syl_data = load(sj, None)
            print('读音拆分用：' + syl_path)
        else:
            print('没找到音节划分表：视频没有“读音拆分”那一部分（用 --syl 指定）')
    unit_ipa = {}
    if list_json:
        for it in load(list_json, []) or []:
            if it.get('phonetic'):
                unit_ipa[str(it.get('word', '')).lower()] = it['phonetic']

    done, flagged_all, warned_all, word_probs = [], {}, {}, {}
    missing = [w for w in words if w not in found]
    if not a.draft_only and not a.silent:              # 6.9 起：开工前先看声音齐不齐，缺了就停（不再悄悄用 38 号念整段）
        probs = voice_config.voice_problems()
        if probs and not voice_config.allow38():
            print('配音的声音没准备好，先不做视频：')
            for p in probs:
                print('  - ' + p)
            raise SystemExit('先跑 bash %s（没装完的会接着装），看到“声音：✅”再跑这一条' % os.path.join(HERE, 'setup.sh'))
        print('配音：' + voice_config.describe())
    for w in [w for w in words if w in found]:
        wdir = os.path.join(a.work, safe(w))
        os.makedirs(wdir, exist_ok=True)
        plan_p, prefs_p, auto_p = (os.path.join(wdir, x) for x in ('plan.json', 'prefs.json', 'plan.auto.json'))
        print('\n==== %s ====' % w)
        # 3. 一批词的画面设置合并进 prefs.json
        e = edits.get(w) or edits.get(w.lower())
        if e:
            prefs = load(prefs_p, {}) or {}
            prefs.update({k: v for k, v in e.items() if not k.startswith('_')})      # _总表 这类参考材料不写进去
            json.dump(prefs, open(prefs_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        # 3.5 读音拆分（音节表）：写进 details.json，起草、渲染都用它
        if syl_data is not None:
            prefs0 = load(prefs_p, {}) or {}
            dd = load(details, {})
            entry = dd.get(w)
            if entry is not None:
                note = attach_pron(entry, w, syl_data, prefs0, unit_ipa)
                json.dump(dd, open(details, 'w', encoding='utf-8'), ensure_ascii=False)
                if note:
                    print(note)
        # 4. 配音稿：没有、要求重写、或者没手改过（和 plan.auto.json 一样）就起草
        untouched = os.path.exists(plan_p) and os.path.exists(auto_p) and open(plan_p, 'rb').read() == open(auto_p, 'rb').read()
        if a.redraft or not os.path.exists(plan_p) or untouched:
            cmd = ['node', os.path.join(HERE, 'draft_plan.js'), details, w, wdir, '--style', style]
            if list_json:
                cmd += ['--list', list_json]
            out = sh(cmd, quiet=True)
            print(out.rstrip() if (a.draft_only or not untouched) else '起草了配音稿：' + plan_p)
        # 5. 扩展词都要在总表里
        prefs = load(prefs_p, {}) or {}
        i, _ = table.find(found[w]['w'])
        changed, probs = check_words(table, i, prefs, pool, prefer_set)
        if changed:
            json.dump(prefs, open(prefs_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        if probs and not a.force:                   # 6.56：不在总表的扩展词先去掉，接着做（不卡住）
            gone = drop_unknown(table, i, prefs, pool)
            changed2, probs2 = check_words(table, i, prefs, pool, prefer_set)
            if gone and not probs2:
                json.dump(prefs, open(prefs_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
                print('提醒：扩展词不在总表里，去掉了：%s（画面设置里可以换成总表里有的词）' % '、'.join(dict.fromkeys(gone)))
                probs = []
        if probs:
            word_probs[w] = probs
            print('；'.join(probs))
            if not a.force:
                print('先不渲染：%s。改 %s 再跑（或者加 --force）' % ('；'.join(probs)[:200], prefs_p))
                continue
        # 6.19：两个版本（用户：“视频讲解的太复杂了，我希望视频能分成两个版本：一、精简版，放前面：精简版词根词缀的各种音变，各种形态这些不讲，直降关键的部分；二、详解版，让学生选看，就是现在的版本”）。
        #   精简版：<work>/<单词>/brief/ 里一份自己的画面设置（详解版的 prefs + 不讲音变、形态、辨析，见 brief_prefs）和配音稿，
        #   配音缓存和详解版共用（一样的句子不再念一遍）；先出精简版，再出详解版（就是原来的视频）
        for ed in EDITIONS[a.edition]:
          ew, eplan, eprefs = wdir, plan_p, prefs_p
          if ed == 'brief':
            ew, eplan, eprefs = make_brief(wdir, prefs_p, details, w, style, list_json, a.redraft)
          if a.draft_only and a.no_preview:
            continue
          if a.draft_only:
            sh(['python3', os.path.join(HERE, 'preview.py'), '--details', details, '--word', w, '--prefs', eprefs, '--out', os.path.join(ew, 'preview.png'), '--cell', str(a.preview_cell)])
            continue
          video = os.path.join(a.out, video_name(w, ed, order.get(w) or (int(a.number) if a.number else None)))   # 6.27：“32 store.mp4”
          rcmd = ['python3', os.path.join(HERE, 'render.py'), '--details', details, '--word', w, '--prefs', eprefs, '--out', video, '--work', ew]
          if a.silent:
              rcmd.append('--silent')
          else:
              # 6. 配音（稿子变了才重新合成）
              audio = os.path.join(ew, 'audio')
              # 5.3 起：声音（参考录音、合成设置）也算进来——换了声音、改了设置，旧配音会重新合成
              digest = hashlib.md5(open(eplan, 'rb').read() + voice_config.signature(load(eplan, {}) or {}).encode('utf-8')).hexdigest()
              stamp = os.path.join(audio, 'plan.md5')
              _man0 = load(os.path.join(audio, 'manifest.json'), {})
              _miss0 = any(s.get('miss') for segs in _man0.values() for s in segs)      # 6.36：上次有没听清的，再跑就再念那几句（别的句子用上次的结果）
              if _miss0 or not (os.path.exists(stamp) and open(stamp).read() == digest and os.path.exists(os.path.join(audio, 'manifest.json'))):
                  sh(['python3', os.path.join(HERE, 'synth.py'), eplan, audio])
                  open(stamp, 'w').write(digest)
              man = load(os.path.join(audio, 'manifest.json'), {})
              used38 = ['%s/%s' % (k, s.get('name')) for k, segs in man.items() for s in segs if s.get('engine') == 'kokoro']
              if used38 and not voice_config.allow38(load(eplan, {}) or {}):       # 6.9 起：38 号念的配音不出片
                  print('这个词有 %d 句是 38 号念的（%s…），不是你本人的声音：先不渲染。跑 setup.sh 装好声音克隆，删掉 %s 再跑' % (len(used38), '、'.join(used38[:3]), audio))
                  continue
              bad = [dict(s, scene=k) for k, segs in man.items() for s in segs if s.get('miss')]
              warns = [dict(s, scene=k) for k, segs in man.items() for s in segs if s.get('warn')]
              if warns:
                  warned_all[w] = warns
              if bad:
                  flagged_all[w] = bad
                  if not a.force:
                      print('有 %d 句英文没听清，先不渲染（改 %s 再跑；或加 --force）' % (len(bad), eplan))
                      continue
              rcmd += ['--plan', eplan, '--manifest', os.path.join(audio, 'manifest.json')]
          # 7. 渲染、截图检查（5.11：分段渲染；--budget 秒数用完就停在一段的结尾，下次接着做）
          if a.budget:
              rcmd += ['--budget', str(max(20.0, a.budget - (time.time() - T0)))]
          sh(rcmd)
          if not a.no_qa:
              sh(['python3', os.path.join(HERE, 'qa.py'), os.path.join(ew, 'timing.json'), os.path.join(ew, 'qa.png')])
          done.append((w + ('（' + EDITION_NAME[ed] + '）' if len(EDITIONS[a.edition]) > 1 else ''), video))

    if a.draft_only:
        tpl = {}
        for w in [w for w in words if w in found]:
            dj = load(os.path.join(a.work, safe(w), 'draft.json'))
            if dj:
                tpl[w] = dj
        if tpl:
            tp = os.path.join(a.work, 'edits_template.json')
            json.dump(tpl, open(tp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            print('\n一批词的画面设置草稿：%s（每个词的画、演变链、扩展词，附总表材料；照着改好存成 edits.json，再加 --edits 跑）' % tp)
        print('\n==== 起草好了（%.0f 秒）：预览图在 %s/<单词>/preview.png ====' % (time.time() - t_start, a.work))
    else:
        print('\n==== 做好了 %d 个（%.0f 秒）====' % (len(done), time.time() - t_start))
        for w, v in done:
            print('  %s  ->  %s' % (w, v))
    if missing:
        print('词源表里没有：' + '，'.join(missing))
    if word_probs:
        print('扩展词要改的：')
        for w, ps in word_probs.items():
            print('  %s：%s' % (w, '；'.join(ps)))
    if warned_all:
        print('短词、拼读的字母可能没听清（多半是识别模型的毛病，不挡渲染；觉得有问题可以改说法）：')
        for w, ws in warned_all.items():
            print('  %s：%s' % (w, '；'.join('%s/%s %s' % (x['scene'], x['name'], ','.join(x['warn'])) for x in ws)))
    if flagged_all:
        print('要改配音稿的（英文没听清，改好后用 --words 只跑这几个）：')
        for w, bad in flagged_all.items():
            for s in bad:
                print('  %s / %s / %s：“%s” 听成了 “%s”（没听清：%s）' % (w, s['scene'], s['name'], s['text'], s['heard'], ','.join(s['miss'])))


if __name__ == '__main__':
    main()
