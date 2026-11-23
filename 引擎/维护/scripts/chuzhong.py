# -*- coding: utf-8 -*-
"""第 127 条（第七十六版，初中含义轮）：「初中含义」列（加在最后，第 28 列）——视频里讲的意思照这一列。
用户：“有的英语单词含义过多，因为现在的学生是初中生，有的时候不需要很多含义的，你参考一下上海初中英语的单词含义，
然后把一些稍微含义多的，不常见的去掉；还有一些单词含义相似的，也可以取最常见的含义，比如 protect，你说了三个含义：
保护，防护，保护本国产业；其实意思差不多，直接说保护就可以了”。
写法和「含义」一样：一个词性一行，行首写词性，几个意思用“；”，同一个意思的两种说法用“、”。
三档：
  ① 单元表 40 个词（7A-U4）手写（HAND_CZ），写法和视频画面设置里每幅画的意思一字不差（视频按它挑画、挑例句、挑演变那几步）；
  ② 考纲里的词：照考纲词汇表的中文（references/kaogang/kaogang.json）——“；”隔开的是几个意思，每个意思取第一种说法，
     一个词性最多 2 个意思、全部最多 3 个、最多 2 个词性；意思相近的（有同一个实词字：保护 / 防护）只留前一个；
     考纲写的是“主格、宾格”“…的”这种说明的（代词、国家和人），照③从「含义」取；
  ③ 考纲外的词：从「含义」取，每个词性取前两个意思（带“（经济）”“（the Speaker）”这种领域、专名标记的不要），全部最多 3 个。
  python3 chuzhong.py <表> --show protect,produce,order    看几个词
  python3 chuzhong.py <表> --write <新表>                  写（没有这一列就加在最后；有就整列重写）
  python3 chuzhong.py <表> --check                         体检：每个词都有、每行行首是词性、意思不超过 3 个
"""
import argparse, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
COL = '初中含义'
HAND_CZ = {
    'camera': 'n. 照相机；摄像机', 'speaker': 'n. 演讲人、发言人；扬声器、音箱', 'thermostat': 'n. 恒温器', 'itself': 'pron. 它自己',
    'alarm': 'n. 警报、警报器；闹钟', 'stranger': 'n. 陌生人', 'lock': 'n. 锁\nv. 锁上', 'explore': 'v. 探索、探险', 'rock': 'n. 岩石；摇滚乐',
    'shower': 'n. 淋浴；阵雨', 'mode': 'n. 方式；模式', 'text message': 'n. 短信', 'bedroom': 'n. 卧室', 'bathroom': 'n. 浴室；卫生间、厕所',
    'suggest': 'v. 建议、提议', 'protect': 'v. 保护', 'review': 'v. 复习\nn. 评论、书评', 'heating': 'n. 供暖、暖气',
    'guide': 'n. 导游、向导\nv. 引导、带领', 'personal': 'adj. 个人的、私人的', 'owner': 'n. 物主、所有者', 'alarm clock': 'n. 闹钟',
    'keep track of': 'phr. 记录、掌握…的情况', 'schedule': 'n. 日程表、计划表；时刻表\nv. 安排、预定', 'health care': 'n. 医疗保健、卫生保健',
    'order': 'n. 顺序；命令\nv. 订购、点菜', 'signal': 'n. 信号\nv. 发信号、示意', 'sense': 'n. 感觉；…感、意识；道理、明智',
    'manage': 'v. 设法做到；管理、经营', 'remind': 'v. 提醒；使想起', 'produce': 'v. 生产、制造\nn. 农产品', 'store': 'n. 商店\nv. 储存',
    'sore': 'adj. 疼痛的', 'throat': 'n. 喉咙', 'understand': 'v. 理解、懂', 'already': 'adv. 已经', 'depend': 'v. 依靠、依赖；取决于',
    'depend on': 'phr. 依靠；取决于', 'truly': 'adv. 真正地、的确', 'oven': 'n. 烤箱',
}
STOP = set('的地得了着人者性化物事东西子儿一不是有在上下中大小等之为与和或使被所以可')
LABEL = re.compile(r'^（[^（）]*）|^\([^()]*\)')


def clean(t):
    t = re.sub(r'[（(][^（）()]*[)）]', '', t).strip()
    return re.sub(r'\s+', '', t).strip('，、；;,. ')


def similar(a, b):
    sa = set(ch for ch in a if '\u4e00' <= ch <= '\u9fff') - STOP
    sb = set(ch for ch in b if '\u4e00' <= ch <= '\u9fff') - STOP
    return bool(sa & sb)


def pick(lines, per=2, total=3, npos=2):
    """[(词性, [意思…])] → 每个词性 ≤ per 个、全部 ≤ total 个、≤ npos 个词性；意思相近的只留前一个"""
    out, kept, n = [], [], 0
    for pos, senses in lines:
        got = []
        for s in senses:
            if not s or n >= total or len(got) >= per:
                continue
            if any(similar(s, k) for k in kept + got):
                continue
            got.append(s); n += 1
        if got:
            out.append((pos, got)); kept += got
        if len(out) >= npos:
            break
    return out


def from_kg(e):
    lines = []
    for p in e.get('pos', []):
        pos = p[0].strip()
        if '&' in pos:
            pos = pos.split('&')[-1].strip() if 'v.' in pos else pos.split('&')[0].strip()
        tags = re.findall(r'(?:aux\. )?[a-z]+\.', pos)              # link v. → v.；词性没写的跳过
        if not tags:
            continue
        pos = 'v.' if tags[-1] in ('link.',) else tags[-1]
        zh = p[1]
        if '…' in zh or re.search(r'主格|宾格|物主|反身', zh):
            return None
        senses = []
        for sense in re.split(r'[；;]', zh):
            first = re.split(r'[，,、]', sense.strip())[0].strip()
            par = re.search(r'[（(]([^（）()]*)[)）]', first)
            base = clean(first)
            if len(base) == 1 and par:
                base += re.split(r'[、，,]', par.group(1))[0]
            if base and not re.search(r'[A-Za-z]', base):
                senses.append(base)
        lines.append((pos, senses))
    return lines


def from_meaning(text, phrase=False, loose=False):
    """loose=True：带“（经济）”这种标记的意思也要（去掉标记），给每个意思都带标记的词用"""
    lines = []
    for ln in str(text or '').split('\n'):
        m = re.match(r'^\s*((?:modal |aux\. )?[a-z]+\.(?:\s*/\s*[a-z]+\.)?)\s*(.+)$', ln.strip())
        if not m:
            continue
        pos, body = m.group(1), m.group(2)
        if pos == 'phr.' and not phrase:
            continue
        senses = []
        for sense in re.split(r'[；;]', body):
            sense = sense.strip()
            if not sense or (LABEL.match(sense) and not loose) or sense.startswith('…'):
                continue
            core = re.sub(r'[（(][^（）()]*[)）]', '', sense)          # 括号里的（领域、对象说明）整个去掉再分
            syn = [clean(x) for x in core.split('、')]
            syn = [x for x in syn if '…' not in x] or syn
            syn = [x for x in syn if x and len(x) <= 10 and not re.search(r'[A-Za-z]', x)][:2]
            if syn:
                senses.append('、'.join(syn))
        lines.append((pos, senses))
    return lines


def chuzhong(T, K, n):
    w0 = T.v(T.data[n], '单词').strip()
    w = w0.lower()
    if not w:
        return ''
    if w in HAND_CZ:
        return HAND_CZ[w]
    e = K.get(w) if not (w0[:1].isupper() and w0 != 'I') else None
    lines = from_kg(e) if e else None
    if lines and not any(s for _, s in lines):
        lines = None
    if not lines:
        lines = from_meaning(T.v(T.data[n], '含义'), phrase=' ' in w)
    got = pick(lines)
    if not got:
        got = pick(from_meaning(T.v(T.data[n], '含义'), phrase=True, loose=True))
    if not got:
        first = [x for x in T.v(T.data[n], '含义').split('\n') if x.strip()]
        return re.split(r'[；;]', first[0].strip())[0] if first else ''
    return '\n'.join('%s %s' % (pos, '；'.join(s)) for pos, s in got)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('table'); ap.add_argument('--show'); ap.add_argument('--write'); ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    from kaodian import Table, KG
    T, K = Table(a.table), KG()
    if a.show:
        for w in [x.strip().lower() for x in a.show.split(',') if x.strip()]:
            n = T.words.get(w)
            if n is None:
                print('==', w, '（表里没有）'); continue
            print('==', w, '｜考纲' if K.get(w) else '｜考纲外', '｜含义：' + T.v(T.data[n], '含义').replace('\n', ' / ')[:90])
            print('   初中含义：' + chuzhong(T, K, n).replace('\n', ' / '))
        return
    if a.check:
        if COL not in T.ix:
            raise SystemExit('表里没有「初中含义」列')
        bad = empty = many = 0
        for r in T.data:
            t = T.v(r, COL).strip()
            if not T.v(r, '单词').strip():
                continue
            if not t:
                empty += 1; continue
            for ln in t.split('\n'):
                if not re.match(r'^(?:modal |aux\. )?[a-z]+\.', ln.strip()):
                    bad += 1
            if sum(len(re.split(r'[；;]', re.sub(r'^\S+\s*', '', ln))) for ln in t.split('\n')) > 3:
                many += 1
        print('初中含义：空的 %d 个，行首不是词性的行 %d，超过 3 个意思的 %d' % (empty, bad, many))
        return
    if a.write:
        import xlsx_write
        table = [[(None if v is None else (v if isinstance(v, (int, float)) else str(v))) for v in row] for row in T.rows]
        new_cols = {}
        if COL not in table[0]:
            for row in table:
                row.append(None)
            j = len(table[0]) - 1
            table[0][j] = COL
            new_cols[j] = (30, T.ix['含义'])
        j = table[0].index(COL)
        vals = [chuzhong(T, K, n) for n in range(len(T.data))]
        for k, v in enumerate(vals):
            table[k + 1][j] = v or None
        xlsx_write.rebuild(a.table, a.write, table, new_cols)
        print('写好了：%s（%d 个词有初中含义）' % (a.write, sum(1 for v in vals if v)))
        return
    ap.print_help()


if __name__ == '__main__':
    main()
