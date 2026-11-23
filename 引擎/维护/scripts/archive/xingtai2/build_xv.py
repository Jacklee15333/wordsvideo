# -*- coding: utf-8 -*-
import sys, re, pickle, collections, unicodedata
sys.path.insert(0, '../maint/etymology-table/scripts')
import linetools as LT, shenfen_data as FD, dongbian_data as DD
import spec as SP
hdr, C, data = pickle.load(open('../tbl.pkl', 'rb'))
PPSTEM = re.compile(r'的过去分词词干[：:]|在这个词里的样子[：:].*过去分词|→\s*过去分词\s+\S+\s*→\s*词干|在过去分词里的样子')
core = lambda s: re.sub(r'[（(][^（）()]*[）)]', '', s or '').strip().strip('-')
bare = lambda s: re.sub(r'[()]', '', s or '')
XT = re.compile(r'^([^：]{1,40})：词根\s+([A-Za-z]+)-“([^”]*)”（')
def norm(s): return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn').replace('j', 'i')
NOTE = {'B': '原样', 'E': '原形加不发音的 e', 'W': '前面有前缀时元音弱化', 'P': '过去分词', 'PE': '过去分词加不发音的 e', 'F': '经法语传进英语，变了形', 'G': '现在分词里的样子', 'L': '带上连接元音'}
# 每组的词根行
lines = collections.defaultdict(list)   # g -> [(行下标, 单词, 标签, 核心, 行)]
for ri, r in enumerate(data):
    for l in str(r[C['root']] or '').split('\n'):
        l = l.strip()
        if not l or l == '-': continue
        lab = LT.label_body(l)[0]
        if not lab: continue
        lines[r[C['grp']]].append((ri, str(r[C['word']]), lab, core(lab).lower(), l))
def gloss_of(key):
    for (ri, w, lab, c, l) in lines.get(key[0], []):
        m = XT.match(l)
        if m and m.group(2) == key[1]: return m.group(3)
    return None
newF = {s['key']: s for s in SP.S if s['t'] == 'F'}
FAM2, VERB2, JOIN, GLOSS = {}, {}, {}, {}
member = collections.defaultdict(list)
rep = []
def cut_of(inf, stem=None):
    for e in ('are', 'ere', 'ire', 'ari', 'eri', 'iri'):
        if inf.endswith(e) and len(inf) > 4: st = inf[:-3]; return '原形去掉词尾 -%s 就是 %s（%s → %s）' % (e, st, inf, st)
    if inf.endswith('re'): st = inf[:-2]; return '原形去掉词尾 -re 就是 %s（%s → %s）' % (st, inf, st)
    st = inf[:-1]; return '原形去掉词尾 -i 就是 %s（%s → %s）' % (st, inf, st)
for s in SP.S:
    key = s['key']; g = key[0]
    sp = s['sp']
    want = {bare(k).lower(): k for k in sp}
    got = collections.defaultdict(list)
    for (ri, w, lab, c, l) in lines.get(g, []):
        if '形态：' in l or '分工：' in l or PPSTEM.search(l): continue
        if c in want:
            got[want[c]].append(w); member[key].append((ri, w, lab, l))
    zero = [k for k in sp if not got.get(k)]
    if s['t'] == 'J':
        JOIN[key] = sp; rep.append((key, 'J', dict(got), zero)); continue
    if s['t'] == 'F':
        g1 = s['zh'].split('、')[0]
        v = dict(inf=(s['inf'], s['zh']), perf=((s['perf'], s['pzh'] or g1 + '了') if s['perf'] else None),
                 pp=((s['pp'], s['ppzh'] or '被' + g1 + '的') if s['pp'] else None), cut=s['cut'] or cut_of(s['inf']), rule=s['rule'])
        gl = s['gloss'] or s['zh']
    else:
        src = s['src']
        v = dict(DD.VERB[src]) if src in DD.VERB else None
        if v is None:
            f = newF[src]; g1 = f['zh'].split('、')[0]
            v = dict(inf=(f['inf'], f['zh']), perf=((f['perf'], f['pzh'] or g1 + '了') if f['perf'] else None),
                     pp=((f['pp'], f['ppzh'] or '被' + g1 + '的') if f['pp'] else None), cut=f['cut'] or cut_of(f['inf']), rule=f['rule'])
            gl = f['gloss'] or f['zh']
        else:
            gl = gloss_of(src) or v['inf'][1]
    ppzh = v['pp'][1] if v.get('pp') else ''
    cls = []
    for k, code in sp.items():
        c, how = (code if isinstance(code, tuple) else (code, ''))
        ex = []
        for w in got.get(k, []):
            if w not in ex: ex.append(w)
        ext = '（%s）' % '、'.join(ex[:4]) if ex else ''
        if not how and c == 'B': cls.append('%s 是“%s”的原样%s' % (k, gl, ext))
        elif not how and c == 'P': cls.append('%s 是过去分词“%s”%s' % (k, ppzh, ext))
        elif not how and c in ('E', 'PE'): cls.append('%s 是%s%s' % (k, NOTE[c], ext))
        else: cls.append('%s：%s%s' % (k, how or NOTE[c], ext))
    FAM2[key] = (sp, '；'.join(cls))
    VERB2[key] = v; GLOSS[key] = gl
    rep.append((key, s['t'], dict(got), zero))
# Whitaker 核对三个样子
W = collections.defaultdict(list)
for ln in open('../ref/DICTLINE.GEN', encoding='latin-1'):
    st = [ln[i:i + 19].strip() for i in (0, 19, 38, 57)]
    rest = ln[76:].split()
    if len(rest) < 3 or rest[0] != 'V': continue
    W[norm(st[1])].append((norm(st[2]), norm(st[3]), rest[1] + rest[2], (rest[3] if len(rest) > 3 else '')))
bad = []
for key, v in VERB2.items():
    inf = norm(v['inf'][0])
    stems = set()
    for e in ('are', 'ere', 'ire', 'ari', 'eri', 'iri', 're', 'i'):
        if inf.endswith(e): stems.add(inf[:-len(e)])
    cands = [x for st in stems for x in W.get(st, [])]
    pf = norm(v['perf'][0])[:-1] if v.get('perf') else None
    pp = re.sub(r'(us|um)$', '', norm(v['pp'][0])) if v.get('pp') else None
    ok = any((pf is None or x[0] in (pf, 'zzz')) and (pp is None or x[1] in (pp, 'zzz')) for x in cands)
    if not ok: bad.append((key, v['inf'][0], pf, pp, [(x[0], x[1], x[2]) for x in cands][:4]))
print('Whitaker 对不上的：', len(bad))
for b in bad: print('   ', b)
tot = 0
for key, t, got, zero in rep:
    n = sum(len(x) for x in got.values()); tot += n
    if zero or n == 0: print('!! 没对上的写法', key, t, zero, '已对上', {k: len(x) for k, x in got.items()})
print('族', len(FAM2), '补写法的已有族', len(JOIN), '要改的行', tot)
# 这些组里没收进来的词根行（看有没有漏）
spec_groups = {s['key'][0] for s in SP.S}
taken = {(ri, l) for k, v in member.items() for (ri, w, lab, l) in v}
left = []
for g in sorted(spec_groups):
    for (ri, w, lab, c, l) in lines[g]:
        if (ri, l) in taken or '形态：' in l or PPSTEM.search(l): continue
        left.append((g, w, lab, l[:70]))
print('这些组里没收的词根行', len(left))
for x in left: print('   ', x)
out = ['# -*- coding: utf-8 -*-',
       '"""2026-11 词根形态补齐轮（project_rules.md 第 113–118 条）：表里只出现一种写法、或者几种写法却没立过族的拉丁语动词词根。',
       '和 shenfen_data.FAM、dongbian_data.VERB 同一个样子，xingtai.py 读的时候合在一起：',
       '  FAM2[(组号, 词根)] = ({写法: 代号或 (代号, 这个写法自己的说明)}, 分工那句话（英语里的用法，切开归到各个形态下）)',
       '  VERB2[(组号, 词根)] = dict(inf, perf, pp, cut, rule)；perf=None 是只有被动样子的动词，pp=None 是没有过去分词的动词',
       '  JOIN[(组号, 词根)] = 已有词根族补进来的写法（这些写法的行上一轮没有“分工”，没排形态）',
       '  GLOSS[(组号, 词根)] = 词根后面引号里的意思',
       '写法代号：B 原样 / E 原形加不发音的 e / W 前面有前缀时元音弱化 / P 过去分词 / PE 过去分词加不发音的 e / F 经法语 / G 现在分词里的样子 / L 带连接元音。',
       '这份数据由 scripts/archive/xingtai2/build_xv.py 照 spec.py 生成（分工那句话的例词取当时表里这一组用这个写法的词）；以后改一族，直接改这里。"""', '']
def lit(x): return repr(x)
out.append('FAM2 = {')
for k in FAM2: out.append(' %r: (%s, %s),' % (k, lit(FAM2[k][0]), lit(FAM2[k][1])))
out.append('}\n\nVERB2 = {')
for k, v in VERB2.items():
    out.append(' %r: dict(inf=%r, perf=%r, pp=%r,\n   cut=%r,\n   rule=%r),' % (k, v['inf'], v.get('perf'), v.get('pp'), v['cut'], v['rule']))
out.append('}\n\nJOIN = {')
for k, v in JOIN.items(): out.append(' %r: %r,' % (k, v))
out.append('}\n\nGLOSS = {')
for k, v in GLOSS.items(): out.append(' %r: %r,' % (k, v))
out.append('}\n')
open('xingtai_verb.py', 'w', encoding='utf-8').write('\n'.join(out))
pickle.dump(dict(member), open('member.pkl', 'wb'))
