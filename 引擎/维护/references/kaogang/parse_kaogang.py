#!/usr/bin/env python3
"""把《2020年上海市初中英语课程终结性评价指南词汇表》（上海市教育考试院）PDF 整理成 JSON。
words：单词（词头、括号里的不规则形式 / 比较级 / 复数、每个词性一行的中文）；phrases：词组；
appendix：人称代词、物主代词、反身代词、基数词和序数词、月份星期、国家和人、学科（表最后几页）。
页码用词汇表自己印的页码（PDF 第 2 页印的是 1）。"""
import json, re, subprocess, sys

POS = r'(?:n\.\s*&\s*adj\.|n\.\s*&\s*v\.|n\.\s*&\s*num\.|v\.\s*&\s*n\.|v\.\s*&\s*aux\.|v\.\s*&\s*link|vt\.\s*&\s*n\.|adj\.\s*&\s*adv\.|adj\.\s*&\s*pron\.|adj\.\s*&\s*n\.|adj\.\s*&\s*prep\.|adv\.\s*&\s*n\.|adv\.\s*&\s*prep\.|adv\.\s*&\s*conj\.\s*&\s*n\.|conj\.\s*&\s*prep\.|conj\.\s*&\s*adv\.|prep\.\s*&\s*adj\.|prep\.\s*&\s*conj\.|aux\.\s*v\.|aux\s*\.v\.|aux\.|n\.|v\.|vt\.|vi\.|adj\.|adv\.|prep\.|conj\.|pron\.|int\.|num\.|art\.|link)'
POS_RX = re.compile(r'^\s*(' + POS + r')\s*(.*)$')


def norm_pos(p):
    p = re.sub(r'\s+', ' ', p.strip()).replace('aux .v.', 'aux. v.').replace('n．& v.', 'n. & v.')
    return p


def pages(pdf):
    txt = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
    return txt.split('\f')


def parse(pdf):
    pg = pages(pdf)
    words, phrases, cur = [], [], None
    mode = None
    appendix_text = []
    for pno, page in enumerate(pg):
        printed = pno            # PDF 第 1 页是封面；第 2 页印 1
        for raw in page.split('\n'):
            line = raw.replace('\u3000', ' ').rstrip()
            s = line.strip()
            if not s:
                continue
            if '单词(Vocabulary)' in s:
                mode = 'w'; continue
            if '词组(Phrases and Expressions)' in s:
                mode = 'p'; cur = None; continue
            if s.startswith('人称代词、物主代词、反身代词'):
                mode = 'a'
            if mode is None:
                continue
            if re.fullmatch(r'\d{1,3}', s):
                continue                      # 页码
            if mode == 'a':
                appendix_text.append((printed, s)); continue
            if mode == 'w':
                if re.fullmatch(r'[A-Z]', s):
                    continue                  # 字母分节
                m = POS_RX.match(line) if line[:1].isspace() or POS_RX.match(s) and not re.match(r'^[A-Za-z]', s) else None
                if line[:1].isspace() and cur is not None:
                    mm = POS_RX.match(s)
                    if mm:
                        cur['pos'].append([norm_pos(mm.group(1)), mm.group(2).strip()])
                    else:
                        # 中文续行（接到上一行的意思后面）
                        if cur['pos']:
                            cur['pos'][-1][1] += s
                        else:
                            cur['tail'] = (cur.get('tail', '') + s)
                    continue
                # 新词头：词头 +（可选的括号）+ 词性 + 中文
                ent = parse_head(s)
                ent['page'] = printed
                words.append(ent); cur = ent
            elif mode == 'p':
                m = re.match(r"^(.*?[A-Za-z.)’'/…])\s{2,}(\S.*)$", s) or re.match(r"^([A-Za-z][^\u3400-\u9fff（(]*?[A-Za-z.)’'/…])\s*([\u3400-\u9fff(（].*)$", s)
                if m:
                    phrases.append({'p': m.group(1).strip(), 'zh': m.group(2).strip(), 'page': printed})
                elif phrases and not re.match(r'^[A-Za-z]', s):
                    phrases[-1]['zh'] += s
                else:
                    phrases.append({'p': s, 'zh': '', 'page': printed})
    return words, phrases, appendix_text


def parse_head(s):
    """'begin (began, begun)   v.  开始' → w=begin forms='began, begun' pos=[['v.','开始']]"""
    ent = {'raw': s, 'w': '', 'note': '', 'pos': []}
    # 词头到第一个词性（前面是空格）或第一个汉字为止
    m = re.match(r'^(.*?)\s+(' + POS + r')\s*(.*)$', s)
    if m and not re.search(r'[\u3400-\u9fff]', m.group(1).split('(')[0]):
        head, p, rest = m.group(1), m.group(2), m.group(3)
        ent['pos'].append([norm_pos(p), rest.strip()])
    else:
        m2 = re.match(r'^([^\u3400-\u9fff]*?)\s*([\u3400-\u9fff(（].*)$', s)
        head, rest = (m2.group(1), m2.group(2)) if m2 else (s, '')
        if rest:
            ent['pos'].append(['', rest.strip()])
    head = head.strip()
    mm = re.match(r'^([^()]*?)\s*\((.*)\)\s*(.*)$', head)
    if mm:
        ent['w'] = (mm.group(1) + (' ' + mm.group(3) if mm.group(3) and not mm.group(3).startswith(('can', 'aux')) else '')).strip()
        ent['note'] = mm.group(2).strip()
        if mm.group(3):
            ent['extra'] = mm.group(3).strip()
    else:
        ent['w'] = head
    # “v. (lay, lain) 躺”“v. (meant, meant) 意思是”：括号在词性后面
    for pl in ent['pos']:
        q = re.match(r'^\(([^()\u3400-\u9fff]+)\)\s*(.*)$', pl[1])
        if q and re.search(r'[a-z]', q.group(1)):
            pl.append(q.group(1).strip()); pl[1] = q.group(2).strip()
    return ent


if __name__ == '__main__':
    pdf, out = sys.argv[1], sys.argv[2]
    words, phrases, app = parse(pdf)
    json.dump({'source': '上海市教育考试院《2020年上海市初中英语课程终结性评价指南词汇表》（https://www.shmeea.edu.cn/download/20190926/07.pdf）',
               'words': words, 'phrases': phrases, 'appendix': [{'page': p, 'text': t} for p, t in app]},
              open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('单词', len(words), '词组', len(phrases), '附录行', len(app))
