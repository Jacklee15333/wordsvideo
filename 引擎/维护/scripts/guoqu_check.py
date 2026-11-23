"""过去分词体检（2026-11 过去分词轮，project_rules.md 第 54 条、writing_guide.md 第 13 节）。
整个从拉丁语借来、接在过去分词词干上的名词、形容词，拆分写“过去分词词干(=母词) + 后缀”（competit(=compete) + ion），
词根列有讲过去分词的那一行，组合列第一行下面紧接“　构词：”一行；英语（或法语）后来自己用现成的 -ation / -ative 造的词（KEEP）拆分照旧、也写构词行。

用法：python3 guoqu_check.py <xlsx> [--show 类别 [N]]
  old_suffix     拆分还写着 -ition / -ation / -itive / -ative / -itor / -ator / -atory / -ature 这种后缀、又不在 KEEP 里的（应为 0）
  no_gouci       拆分写了过去分词词干（X(=Y)，词根列那一行讲过去分词）、组合列却没有“构词”行的（应为 0）
  gouci_bad      构词行写法不对：带链的要至少四步“原形（意思）→ 过去分词 X → 词干 Y- → 拉丁原词”、有“词干 Y-”、最后一个是一个词；
                 不能有“+ -”；要紧接在第一行（和后缀等式）下面（应为 0）
  stem_no_line   构词行带链，拆分里却没有在词根列讲过去分词的词干（应为 0）
  keep_no_gouci  KEEP 里的词没有构词行（应为 0）
  no_chain       写成过去分词词干的词，音变列第一行没有【字母变化】链、或链和步骤写法不对（照 zimu_check.py 的规则；第 55 条，应为 0）
新补的词照这条写；是英语后来自己造的，把词加进 KEEP 并写明理由。
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from openpyxl import load_workbook
import cols as C
from parse import parse_split
try:
    from zimu_check import problems as chain_problems
except Exception:                                      # 没有 zimu_check 时只查第一行
    chain_problems = None

OLD = ('ition', 'ation', 'itive', 'ative', 'itor', 'ator', 'atory', 'ature')
# 英语（或法语）后来自己用现成的 -ation / -ative 造的：etymonline 写“noun of action from X (v.)”“from French …”“from X + -ation”
KEEP = {'transportation', 'classification', 'civilization', 'civilisation', 'experimentation', 'realization', 'realisation',
        'internationalization', 'reforestation', 'deforestation', 'digitalisation', 'digitalization', 'mechanisation', 'mechanization',
        'commercialization', 'industrialization', 'identification', 'globalization', 'orientation', 'acidification', 'urbanization',
        'aviation', 'sanitation', 'vaccination', 'synchronization', 'talkative', 'commentative'}
SKIP = {'escalator'}                                   # 拼缀词：-ator 取自 elevator，不是过去分词
# 过去分词轮以前就写成过去分词词干的老行，经法语磨得看不出原样（season ← 拉丁语 sationem“播种”），字母变化在音变列讲，不写构词行
OLD_PP = {'season'}
GOUCI = re.compile(r'^\s*构词[：:]\s*(.*)$')
PP = re.compile(r'的过去分词词干|→ 过去分词 [a-z]|以 -atus 结尾')
SUFEQ = re.compile(r'^\s*[A-Za-z][^：\n]*“[^”]*”\s*\+\s*-')


def check(path):
    ws = load_workbook(path, read_only=True)['拆分结果']
    out = {k: [] for k in ('old_suffix', 'no_gouci', 'gouci_bad', 'stem_no_line', 'keep_no_gouci', 'no_chain')}
    n_pp = n_keep = 0
    for r, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        w = str(row[C.WORD - 1] or '').strip()
        sp = str(row[C.SPLIT - 1] or '')
        combo = str(row[C.COMBO - 1] or '').split('\n')
        root = [l for l in str(row[C.ROOT - 1] or '').split('\n') if l.strip()]
        ps = parse_split(sp) or []
        gl = [i for i, l in enumerate(combo) if GOUCI.match(l)]
        if w in KEEP:
            n_keep += 1
            if not gl:
                out['keep_no_gouci'].append((r, w, sp))
        elif len(ps) >= 2 and ps[-1]['surface'].strip().lower() in OLD and w not in SKIP:
            out['old_suffix'].append((r, w, sp))
        stems = []
        for p in ps[:-1]:
            if not p['eqs']:
                continue
            line = next((l for l in root if (C.label_of(l) or '').strip('-').lower() == p['surface'].strip().lower()), None)
            if line and PP.search(C.strip_meta(line)):      # “身份、分工”那一段讲的是别的写法、“动词变化”那一段讲的是整个动词的三个样子，都不算
                stems.append(p['surface'])
        if stems:
            n_pp += 1
            if not gl and w not in OLD_PP:
                out['no_gouci'].append((r, w, sp))
            P = str(row[C.SOUND - 1] or '')
            if w not in OLD_PP:
                pr = ['音变列第一行不是【字母变化】链'] if not P.startswith('【字母变化】') else (chain_problems(w, P) if chain_problems else [])
                if pr:
                    out['no_chain'].append((r, w, '；'.join(pr)))
        for i in gl:
            body = GOUCI.match(combo[i]).group(1)
            bad = []
            if '+ -' in body:
                bad.append('有“+ -”')
            k = body.rfind('：')
            chain = body[k + 1:] if k >= 0 and '→' in body[k + 1:] else ''
            if chain:
                steps = [x.strip() for x in chain.split('→')]
                if len(steps) < 4:
                    bad.append('链不到四步')
                if not any(x.startswith('词干 ') and x.endswith('-') for x in steps):
                    bad.append('链里没有“词干 X-”')
                if not re.fullmatch(r'[a-z]+', steps[-1]):
                    bad.append('链的最后一个不是一个词')
                if not stems:
                    out['stem_no_line'].append((r, w, sp))
            elif w not in KEEP:
                bad.append('没有链（不是 KEEP 里的词）')
            if not all(SUFEQ.match(combo[j]) for j in range(1, i)):
                bad.append('没有紧接在第一行下面')
            if bad:
                out['gouci_bad'].append((r, w, '；'.join(bad)))
    return n_pp, n_keep, out


if __name__ == '__main__':
    path = sys.argv[1]
    show = sys.argv[sys.argv.index('--show') + 1] if '--show' in sys.argv else None
    n = int(sys.argv[sys.argv.index('--show') + 2]) if show and len(sys.argv) > sys.argv.index('--show') + 2 else 30
    n_pp, n_keep, out = check(path)
    print(f'写成过去分词词干的行 {n_pp}；英语后来自己造的、拆分照旧的（KEEP）{n_keep}')
    for k, v in out.items():
        print(f'{k:14s} {len(v)}' + ('  ' + '、'.join(str(x[1]) for x in v[:12]) if v else ''))
    if show:
        for x in out[show][:n]:
            print('  ', *x)
