#!/usr/bin/env python3
"""kaogang_raw.json（parse_kaogang.py 的结果）→ kaogang.json：修好 7 个排版特殊的词头，拆开 although/though 这类“两个词一条”的，
补上美式拼写，把附录（代词表、数词表、月份星期、国家和人、学科）也变成词条。键一律小写。"""
import json, re
d = json.load(open('kaogang_raw.json', encoding='utf-8'))
W = {}

def add(key, ent, alias_of=None):
    k = key.strip().lower()
    if not k:
        return
    if k in W:
        # 同一个词出现两次（附录和正文都有）：词性合并
        for p in ent.get('pos', []):
            if p not in W[k]['pos']:
                W[k]['pos'].append(p)
        for kk in ('ordinal', 'cardinal', 'pron', 'pron_base', 'people', 'country'):
            if kk in ent and kk not in W[k]:
                W[k][kk] = ent[kk]
        return
    e = dict(ent); e['w'] = key.strip()
    if alias_of:
        e['alias_of'] = alias_of
    W[k] = e

FIX = {
    'chat      n．&': ('chat', [['n. & v.', '聊天，闲谈']], ''),
    'born': ('born', [['', '出生']], '动词 bear 的过去分词'),
    'far': ('far', [['adj.', '远的'], ['adv.', '远地']], '比较级 farther，最高级 farthest 或比较级 further，最高级 furthest'),
}
for e in d['words']:
    w = e['w']
    if w in FIX:
        nw, pos, note = FIX[w]
        e = dict(e, w=nw, pos=pos, note=note)
        w = nw
    ent = {'pos': [p[:3] for p in e['pos']], 'note': e.get('note', ''), 'page': e['page'], 'raw': e['raw']}
    if w in ('A.M.', 'P.M.', 'P.E.'):
        add(w, ent); continue
    if '/' in w:                                  # although/though、anybody/anyone、bicycle/bike…
        parts = [x.strip() for x in w.split('/')]
        for x in parts:
            add(x, ent)
        continue
    if '=' in w:                                  # exam=examination、grandma=grandmother
        a, b = [x.strip() for x in w.split('=')]
        add(a, ent); add(b, ent, alias_of=a)
        continue
    add(w, ent)
    note = ent['note']
    m = re.search(r'美\s*([A-Za-z]+)', note)       # centre (美 center)
    if m:
        add(m.group(1), ent, alias_of=w)
    m = re.search(r'^=\s*([A-Za-z]+)', note)        # phone (=telephone)、maths (=mathematics，美 math)
    if m:
        add(m.group(1), ent, alias_of=w)
    if w in ('e-mail',):
        add('email', ent, alias_of=w)
    if w == 'manner':
        add('manners', ent, alias_of=w)
    if w == 'toward':
        add('towards', ent, alias_of=w)
    if w == 'television':
        add('TV', ent, alias_of=w)
    if w == 'practice':
        add('practise', ent, alias_of=w)

# 附录：代词
PRON = {
    'I': ('主格', 'I'), 'me': ('宾格', 'I'), 'we': ('主格', 'we'), 'us': ('宾格', 'we'), 'you': ('主格、宾格', 'you'),
    'he': ('主格', 'he'), 'him': ('宾格', 'he'), 'she': ('主格', 'she'), 'her': ('宾格；形容词性物主代词', 'she'),
    'it': ('主格、宾格', 'it'), 'they': ('主格', 'they'), 'them': ('宾格', 'they'),
    'my': ('形容词性物主代词', 'I'), 'your': ('形容词性物主代词', 'you'), 'his': ('形容词性、名词性物主代词', 'he'),
    'its': ('形容词性物主代词', 'it'), 'our': ('形容词性物主代词', 'we'), 'their': ('形容词性物主代词', 'they'),
    'mine': ('名词性物主代词', 'I'), 'yours': ('名词性物主代词', 'you'), 'hers': ('名词性物主代词', 'she'),
    'ours': ('名词性物主代词', 'we'), 'theirs': ('名词性物主代词', 'they'),
    'myself': ('反身代词', 'I'), 'yourself': ('反身代词', 'you'), 'himself': ('反身代词', 'he'), 'herself': ('反身代词', 'she'),
    'itself': ('反身代词', 'it'), 'ourselves': ('反身代词', 'we'), 'yourselves': ('反身代词', 'you'), 'themselves': ('反身代词', 'they'),
}
for w, (kind, base) in PRON.items():
    add(w, {'pos': [['pron.', kind]], 'note': '', 'page': 84, 'raw': '附录·人称代词、物主代词、反身代词', 'pron': kind, 'pron_base': base})
# 附录：数词
CARD = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty'.split()
ORD = 'first second third fourth fifth sixth seventh eighth ninth tenth eleventh twelfth thirteenth fourteenth fifteenth sixteenth seventeenth eighteenth nineteenth twentieth'.split()
TENS = [('thirty', 'thirtieth'), ('forty', 'fortieth'), ('fifty', 'fiftieth'), ('sixty', 'sixtieth'), ('seventy', 'seventieth'),
        ('eighty', 'eightieth'), ('ninety', 'ninetieth'), ('hundred', 'hundredth')]
NUMS = list(zip(CARD, ORD)) + TENS
for i, (c, o) in enumerate(NUMS):
    pg = 85 if i < 19 else 86
    add(c, {'pos': [['num.', '基数词']], 'note': '', 'page': pg, 'raw': '附录·基数词和序数词', 'ordinal': o})
    add(o, {'pos': [['num.', '序数词']], 'note': '', 'page': pg, 'raw': '附录·基数词和序数词', 'cardinal': c})
for c in ('thousand', 'million', 'billion'):
    add(c, {'pos': [['num.', '基数词']], 'note': '', 'page': 86, 'raw': '附录·基数词和序数词'})
for m in 'Monday Tuesday Wednesday Thursday Friday Saturday Sunday January February March April May June July August September October November December'.split():
    if m.lower() in W:            # may（情态动词）、march：不把“月份”合进去
        W[m.lower()]['month'] = m
        continue
    add(m, {'pos': [['n.', '月份、星期']], 'note': '', 'page': 87, 'raw': '附录·月份和星期'})
CTRY = [('America', 'American'), ('Australia', 'Australian'), ('Britain', 'British'), ('Canada', 'Canadian'), ('China', 'Chinese'),
        ('England', 'English'), ('France', 'French'), ('Germany', 'German'), ('Italy', 'Italian'), ('Japan', 'Japanese'),
        ('Asia', 'Asian'), ('Africa', 'African'), ('Europe', 'European')]
for c, p in CTRY:
    pg = 87 if c in ('America', 'Australia', 'Britain', 'Canada') else 88
    add(c, {'pos': [['n.', '国家、大洲']], 'note': '', 'page': pg, 'raw': '附录·国家、大洲及其对应的人', 'people': p})
    add(p, {'pos': [['adj.', '…的'], ['n.', '…人']], 'note': '', 'page': pg, 'raw': '附录·国家、大洲及其对应的人', 'country': c})
add('Briton', {'pos': [['n.', '英国人']], 'note': '', 'page': 87, 'raw': '附录·国家、大洲及其对应的人', 'country': 'Britain'})
for s in ('Biology', 'Physics', 'Chemistry', 'Math', 'Maths'):
    add(s, {'pos': [['n.', '学科']], 'note': '', 'page': 88, 'raw': '附录·常用学科'})

out = {'source': d['source'], 'note': '正文 1724 条（although/though 这类两个词一条的算一条）；键是小写，附录的代词、数词、月份星期、国家和人、学科也收进来了',
       'words': W, 'phrases': d['phrases']}
json.dump(out, open('kaogang.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('词条（含拆开的、美式拼写、附录）', len(W), '词组', len(d['phrases']))
