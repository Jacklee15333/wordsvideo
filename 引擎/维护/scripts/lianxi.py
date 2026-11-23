# -*- coding: utf-8 -*-
"""第 122 条：练习题「题目1」–「题目5」（接在「考点」后面）+「答案」（第 123 条：答案和讲解放一格）。
第 126 条（第七十五版）：5 道改 7 道——「题目5」后面加「题目6」「题目7」两列（第 24、25 列，「答案」挪到第 26 列、「读音现象」第 27 列），
新加的两道专门考「考点」列（kd 必写：变形 / 词性转换 / 短语 / 用法 / 易混），原来 5 道的出题办法不变；「答案」一格写七道。
视频“练习”那一部分照读题目（只出题），视频最后“答案”那一部分照读答案列（视频第五十二版起）。
  python3 lianxi.py <表> --show produce,suggest      打印这几个词写进表里的样子
  python3 lianxi.py <表> --write <新表>               把 lianxi_data.py 里的题写进五列（没有这五列就加上；表里已有、原稿里没有的词保留原样）
  python3 lianxi.py <表> --check                      体检五列：格式、答案、听力在第 1 题、答案就是本词原形的最多 1 道
一格一道题，一行一项：
  【题型】要求                   第一行，题型是 听力 / 单项选择 / 适当形式填空 / 选词填空 / 完成句子 / 改错 / 句型转换 / 同义替换 / 汉译英 / 首字母填空 …
  听：英文句子                   听力念的（念两遍）
  中文：…                        完成句子、汉译英的中文
  题干：…                        英文题干，“______”是空，“p______”是首字母空；两行写两个“题干：”
  A. … / B. … / C. … / D. …      选项，一行一个
  考点：用法                     考的是「考点」列哪一种（变形 / 词性转换 / 短语 / 用法 / 易混），没有就不写这一行
「答案」一格五道题，每道两行：
  【1】D（牛奶和鸡蛋）            选择写字母，括号里是那个选项；填空写要填的，几个空用“；”隔开；改错写“错的 → 对的”
  讲解：…                        说清是哪儿决定了答案
"""
import argparse, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
COLS = ['题目1', '题目2', '题目3', '题目4', '题目5', '题目6', '题目7']      # 第 126 条：7 道
DAAN = '答案'
KD = {'变形', '词性转换', '短语', '用法', '易混'}
LET = 'ABCD'


def place(word, k, n):
    h = k * 7
    for ch in word:
        h = (h * 31 + ord(ch)) % 9973
    return h % n


def fmt(word, k, q):
    """原稿的一道题 → (题目那一格, 这道题的答案, 这道题的讲解)（选择题 opts[0] 是对的，挪到 A–D 的某一个）"""
    out = ['【%s】%s' % (q['type'], q['ask'])]
    if q.get('listen'):
        out.append('听：' + q['listen'])
    if q.get('zh'):
        out.append('中文：' + q['zh'])
    for s in (q.get('stem') or '').split('\n'):
        if s.strip():
            out.append('题干：' + s.strip())
    ans = q.get('ans', '')
    if q.get('opts'):
        o = list(q['opts'])
        at = place(word, k, len(o))
        right = o.pop(0)
        o.insert(at, right)
        out += ['%s. %s' % (LET[i], x) for i, x in enumerate(o)]
        ans = '%s（%s）' % (LET[at], right)
    if q.get('kd'):
        out.append('考点：' + q['kd'])
    return '\n'.join(out), ans, q['why']


def fmt_word(word, qs):
    """一个词 → (五格题目, 答案那一格)"""
    cells, daan = [], []
    for k, q in enumerate(qs):
        c, a, w = fmt(word, k, q)
        cells.append(c)
        daan.append('【%d】%s\n讲解：%s' % (k + 1, a, w))
    return cells, '\n'.join(daan)


def parse_daan(cell):
    """「答案」那一格 → {1: (答案, 讲解), …}；选择题的答案只留字母"""
    out, cur = {}, None
    for ln in str(cell or '').split('\n'):
        ln = ln.strip()
        m = re.match(r'^【(\d)】\s*(.*)$', ln)
        if m:
            cur = int(m.group(1)); a = m.group(2).strip()
            m2 = re.match(r'^([A-D])(?:（.*）|\(.*\))?$', a)
            out[cur] = [m2.group(1) if m2 else a, '']
            continue
        m = re.match(r'^(讲解|解析)[：:]\s*(.*)$', ln)
        if m and cur:
            out[cur][1] = m.group(2)
    return out


def parse(cell):
    """表格里的一格 → {type, ask, listen, zh, stem, opts, ans, why, kd}（视频技能 wordfilm.js 的 lxParse 照这个读）"""
    q = {'type': '', 'ask': '', 'listen': '', 'zh': '', 'stem': [], 'opts': [], 'ans': '', 'why': '', 'kd': ''}
    for ln in str(cell or '').split('\n'):
        ln = ln.strip()
        if not ln:
            continue
        m = re.match(r'^【([^】]+)】\s*(.*)$', ln)
        if m:
            q['type'], q['ask'] = m.group(1), m.group(2); continue
        m = re.match(r'^([A-D])[.．]\s*(.*)$', ln)
        if m:
            q['opts'].append(m.group(2)); continue
        m = re.match(r'^(听|中文|题干|答案|解析|考点)[：:]\s*(.*)$', ln)
        if m:
            k = {'听': 'listen', '中文': 'zh', '题干': 'stem', '答案': 'ans', '解析': 'why', '考点': 'kd'}[m.group(1)]
            if k == 'stem':
                q['stem'].append(m.group(2))
            else:
                q[k] = m.group(2)
            continue
        q.setdefault('bad', []).append(ln)
    q['stem'] = '\n'.join(q['stem'])
    return q


def check_word(word, cells, daan=''):
    """一个词的五格题目 + 答案格 → 问题列表（空着的词不查）"""
    if not any(cells) and not daan:
        return []
    errs = []
    if not all(cells):
        errs.append('%d 格没写全' % len(cells))
    D = parse_daan(daan)
    base = 0
    for k, c in enumerate(cells):
        if not c:
            continue
        q = parse(c)
        tag = '题目%d' % (k + 1)
        if k + 1 in D:
            q['ans'], q['why'] = D[k + 1][0] or q['ans'], D[k + 1][1] or q['why']
        if q.get('bad'):
            errs.append(tag + ' 认不出的行：' + ' | '.join(q['bad']))
        if not q['type'] or not q['ask']:
            errs.append(tag + ' 第一行要是“【题型】要求”')
        if k == 0 and (q['type'] != '听力' or not q['listen']):
            errs.append(tag + ' 第 1 题要是听力（有“听：”一行）')
        if not q['ans'] or not q['why']:
            errs.append(tag + ' 「答案」列里缺这道题的答案或讲解')
        if q['opts']:
            if len(q['opts']) < 2 or q['ans'] not in LET[:len(q['opts'])]:
                errs.append(tag + ' 选择题的答案要是 A–%s 里的一个' % LET[len(q['opts']) - 1])
            if len(set(x.lower() for x in q['opts'])) < len(q['opts']):
                errs.append(tag + ' 选项有重复')
            right = q['opts'][LET.index(q['ans'])] if q['ans'] in LET[:len(q['opts'])] else ''
        else:
            right = q['ans']
            nb = len(re.findall(r'[A-Za-z]?_{3,}', q['stem']))
            na = len([x for x in q['ans'].split('；') if x.strip()])
            if nb and '→' not in q['ans'] and nb != na:
                errs.append(tag + ' 题干 %d 个空，答案 %d 个' % (nb, na))
        if k >= 5 and not q['kd']:
            errs.append(tag + ' 新加的第 6、7 题专门考考点，要写“考点：”一行')
        if q['kd'] and q['kd'] not in KD:
            errs.append(tag + ' 考点只写 变形 / 词性转换 / 短语 / 用法 / 易混')
        if right.strip().lower() == word.lower():
            base += 1
    if base > 1:
        errs.append('答案就是 %s 本身的有 %d 道（最多 1 道）' % (word, base))
    if any(cells) and len(D) != len([c for c in cells if c]):
        errs.append('「答案」列有 %d 道，题目有 %d 道' % (len(D), len([c for c in cells if c])))
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('table')
    ap.add_argument('--show')
    ap.add_argument('--write')
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    from kaodian import Table
    T = Table(a.table)
    import lianxi_data as D
    have = all(c in T.ix for c in COLS + [DAAN])
    if a.show:
        for w in [x.strip() for x in a.show.split(',') if x.strip()]:
            n = T.words.get(w.lower())
            print('==', w, '' if n is not None else '（表里没有）')
            src = D.Q.get(w) or D.Q.get(w.lower())
            if src:
                cells, daan = fmt_word(w, src)
            elif have and n is not None:
                cells, daan = [T.v(T.data[n], c) for c in COLS], T.v(T.data[n], DAAN)
            else:
                cells, daan = [], ''
            for k, c in enumerate(cells):
                print('--', COLS[k]); print(c)
            print('--', DAAN); print(daan)
        return
    if a.check:
        if not have:
            raise SystemExit('表里还没有「题目1」–「题目7」「答案」八列')
        bad = done = 0
        for r in T.data:
            cells = [T.v(r, c).strip() for c in COLS]
            if any(cells):
                done += 1
            e = check_word(T.v(r, '单词'), cells, T.v(r, DAAN))
            if e:
                bad += 1
                print(T.v(r, '单词') + '：' + '；'.join(e))
        print('有题的词 %d 个，有问题的 %d 个' % (done, bad))
        return
    if a.write:
        import xlsx_write
        table = [[(None if v is None else (v if isinstance(v, (int, float)) else str(v))) for v in row] for row in T.rows]
        new_cols = {}
        for c in COLS + [DAAN]:                            # 没有的列：题目N 插在题目N-1 后面（第 126 条：题目6、题目7 在「答案」前面）；「答案」接在最后一道题后面
            if c not in table[0]:
                prev = COLS[COLS.index(c) - 1] if c in COLS and COLS.index(c) > 0 else (COLS[-1] if c == DAAN else None)
                j = table[0].index(prev) + 1 if prev and prev in table[0] else len(table[0])
                for row in table:
                    row.insert(j, None)
                table[0][j] = c
                new_cols = {(k + 1 if k >= j else k): v for k, v in new_cols.items()}
                src = T.ix.get(prev) if prev in T.ix else T.ix['考点']
                new_cols[j] = (56 if c == DAAN else 46, src)
        ix = {c: table[0].index(c) for c in COLS + [DAAN]}
        miss, n_w, errs = [], 0, 0
        for w, qs in D.Q.items():
            n = T.words.get(w.lower())
            if n is None:
                miss.append(w); continue
            cells, daan = fmt_word(w, qs)
            e = check_word(w, cells, daan)
            if e:
                errs += 1; print(w + '：' + '；'.join(e))
            for c, t in zip(COLS, cells):
                table[n + 1][ix[c]] = t
            table[n + 1][ix[DAAN]] = daan
            n_w += 1
        if errs:
            raise SystemExit('原稿有 %d 个词没过体检，先改 lianxi_data.py' % errs)
        xlsx_write.rebuild(a.table, a.write, table, new_cols)
        print('写好了：%s（%d 个词有练习题%s）' % (a.write, n_w, '；表里没有：' + '、'.join(miss) if miss else ''))
        return
    ap.print_help()


if __name__ == '__main__':
    main()
