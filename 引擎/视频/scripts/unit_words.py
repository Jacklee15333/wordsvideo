#!/usr/bin/env python3
"""从按册、按单元排的单词表（比如 6A-9A.xlsx）里取出某一册某一单元的单词。

用法：
  python3 unit_words.py <单词表.xlsx> 7A 3                 # 第三单元的单词表部分（默认 main）
  python3 unit_words.py <单词表.xlsx> 7A 3 --section all   # 连“词性转换”“主题词汇”也算上（短语总是跳过）
  python3 unit_words.py <单词表.xlsx> --list               # 列出表里有哪些册、哪些单元
  加 --json out.json 把结果（单词、音标、含义）存下来，run.py 用它在小黑板上写词性和含义

表格的样子：册名一行（“7A-学习版”这类，以 6A～9B 开头），单元一行（“Unit 3 Jobs”“unit1 school life”），
小节一行（“（词性转换）”“（短语）”“（主题词汇）”），列名一行（序号 | 单词 | 音标 | 含义），下面是单词。
同一个词的英式、美式拼写（kilometre（英式）/ kilometer（美式））只留英式；带空格的短语跳过。
"""
import json
import re
import sys


def read(path):
    from openpyxl import load_workbook
    wb = load_workbook(path, read_only=True)
    out = []
    for ws in wb.worksheets:
        book = unit = title = None
        sub = 'main'
        for r in ws.iter_rows(values_only=True):
            r = list(r) + [None] * 4
            a = str(r[0]).strip() if r[0] is not None else ''
            b = str(r[1]).strip() if r[1] is not None else ''
            if a and not b:
                m = re.match(r'^([6-9][AB])\b', a) or re.match(r'^([6-9][AB])[-－—\s]', a)
                if m:
                    book, unit, sub = m.group(1).upper(), None, 'main'
                    continue
                m = re.match(r'(?i)^unit\s*(\d+)\s*(.*)$', a)
                if m:
                    rest = m.group(2).strip()
                    sm = re.search(r'[（(]([^）)]*)[）)]\s*$', rest)      # “Unit 3 Jobs （词性转换）”：同一单元的小节
                    unit, title = int(m.group(1)), re.sub(r'\s*[（(][^）)]*[）)]\s*$', '', rest).strip()
                    sub = sm.group(1).strip() if sm else 'main'
                    continue
                if a[:1] in '（(':
                    sub = a.strip('（）() ')
                    continue
            if a in ('序号',) or b in ('单词',) or not b or not book or unit is None:
                continue
            out.append({'book': book, 'unit': unit, 'title': title, 'section': sub, 'word': b,
                        'phonetic': str(r[2]).strip() if r[2] else '', 'meaning': str(r[3]).strip() if r[3] else ''})
    return out


def clean(items):
    words, seen = [], set()
    for it in items:
        raw = it['word']
        note = ' '.join(re.findall(r'（([^）]*)）|\(([^)]*)\)', raw)[0]) if re.search(r'[（(]', raw) else ''
        w = re.sub(r'\s*[（(][^）)]*[）)]\s*', '', raw).strip()
        if '美式' in note and any('英式' in x.get('note', '') and x['word'][:4].lower() == w[:4].lower() for x in words):
            continue                                   # 美式拼写：和前面的英式是同一个词
        if ' ' in w:
            it = dict(it, skip='短语')
        k = w.lower()
        if k in seen:
            continue
        seen.add(k)
        words.append(dict(it, word=w, note=note))
    return words


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    opts = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    items = read(args[0])
    if '--list' in opts:
        seen = {}
        for it in items:
            seen.setdefault((it['book'], it['unit']), [it['title'], 0])[1] += 1
        for (b, u), (t, n) in seen.items():
            print('%s Unit %d %s：%d 个' % (b, u, t or '', n))
        return
    book, unit = args[1].upper(), int(args[2])
    section = opts[opts.index('--section') + 1] if '--section' in opts else 'main'
    sel = [it for it in items if it['book'] == book and it['unit'] == unit and
           (it['section'] == 'main' if section == 'main' else '短语' not in it['section'])]
    if not sel:
        sys.exit('没找到 %s Unit %d（用 --list 看看表里有哪些）' % (book, unit))
    words = clean(sel)
    keep = [w for w in words if not w.get('skip')]
    print('%s Unit %d %s：%d 个单词（跳过 %s）' % (book, unit, sel[0]['title'] or '', len(keep),
                                         '、'.join(w['word'] + '：' + w['skip'] for w in words if w.get('skip')) or '无'))
    print(','.join(w['word'] for w in keep))
    if '--json' in opts:
        json.dump(keep, open(opts[opts.index('--json') + 1], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
