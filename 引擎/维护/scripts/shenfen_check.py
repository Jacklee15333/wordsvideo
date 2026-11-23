# -*- coding: utf-8 -*-
"""身份分工、词缀辨析、辨析列、拉丁语动词变化体检（2026-11 身份分工、辨析列轮，拉丁语动词变化轮，词缀身份辨析轮；project_rules.md 第 65–68、71、83–88 条）。按列名读表，16 / 17 / 22 列都能跑。
  python3 shenfen_check.py <表.xlsx> [每类列几条]
各项都应为 0：
  root_chain     词根列某一行里还有“词根的意思 → 前缀“…”… → 今天的意思”这种链（怎么组合、意思怎么来只写在组合列）
  heqi_in_parts  前缀 / 词根 / 单词部分列里还有讲“合起来是…”的话（应该在组合列第一行下面的“　合起来：”一行）
  var_no_id      写了“词根 X 的另一种写法”，却没有“身份：…。分工：…”
  id_bad         “身份 / 分工”写法不对：缺一半、分工里有句号、写在“；记：”后面（视频读不出记法）
  fam_missing    表里有“词根 X 的另一种写法”，shenfen_data.py 里却没有这个词根族、或没有这个写法的身份
  id_bad 只看词根列的“身份：…。分工：…”；前缀、后缀行 2026-11 词缀身份辨析轮起写成“标签：身份：介绍；记：…。辨析：…”（第 83–88 条），由下面六项查：
  affix_todo     前缀 / 后缀行还没标“身份：”，或者在 cizhui_catalog.py 里查得到辨析却还没挂（新加的词：跑 cizhui.py 看，--write 写回）
  affix_no_id    讲词缀的那一行开头没有“身份：”
  affix_old      还留着上一版的老写法“；身份：…。分工：…”（拿这一版脚本查上一版的表，这几项会报五千多行）
  bianxi_bad     辨析写法不对：不是这一行的最后一段、前面不是句号、里面有句号、写在“；记：”前面、一行两段
  bianxi_diff    辨析的话不是 cizhui_catalog.py 里的句子（手改过表，或者目录改了没重写），或者和目录给这一行挑的那一组不一样
  guanxi_bad     辨析最后的“；关系：…”写法不对（2026-11 词缀关系轮，第 89–92 条）：不是最后一段、一行两段、是空的、哪一条不是词缀打头
  combo_bianxi   有「辨析」列的表，组合列里还有【辨析】段
  ref_old        别处还写着“见【辨析】”（应是“见辨析列”）
  syn_bad        辨析列的【同义词】行写法不对（应是“【同义词】中文意思：词、词…”），或者里面的词不在总表
  heqi_pos       组合列“　合起来：”那一行没紧跟在第一行（和它下面的后缀等式、构词 / 合成规律 / 写法行）后面
  xt_missing   词根族的行还是老写法（“身份：…。分工：…”）：跑 xingtai.py --write
  （2026-11 词根形态轮以前是 verb_missing / verb_diff / verb_bad / verb_stray，查“动词变化：…；规律：…”）
  verb_missing   这一族是 dongbian_data.py 里的拉丁语动词，这一行（写了身份、分工的词根行）却没有“动词变化：…；规律：…”（新加的词：跑 dongbian.py 看，再 --write 写回）
  verb_diff      写了，和 dongbian_data.py 里的不一样（数据改了没重写，或者手改过表）
  verb_bad       “动词变化”写法不对：三个样子不是“原形 / 过去式 / 过去分词 拉丁语“中文””、没紧挨在“身份：”前面、规律里有“意思是 / 意思：”（视频读不出，或把它当成词根的意思）
  verb_stray     不属于这些词根族（或没写身份、分工）的行写了“动词变化”，或者写到了前缀、单词部分、后缀列
另外报个数（不算错）：辨析列有内容的行、有【同义词】行的行、同义词组里辨析文字一个词也没提到的行（--todo 列出来，视频第三部分要人补）"""
import re, sys, collections
import linetools as LT, shenfen, cizhui, bianxi as B, dongbian, xingtai
import shenfen_data as FD
import columns as CO

VARL = shenfen.VARL
SF = re.compile(r'身份：([^。\n]*)。分工：([^。\n]*?)(?=。|；记：|$)')
INLINE_HEQI = re.compile(r'合起来是(“|拉丁语|希腊语|古|中世纪|晚期|俗|法语|意大利语)')
SYN = re.compile(r'^【同义词】([^：]{1,10})：(.+)$')

def check(path):
    hdr, C, data = LT.load_table(path)
    out = collections.defaultdict(list)
    words = {str(r[C['word']]) for r in data}
    info = collections.Counter()
    for n, r in enumerate(data, start=2):
        w = str(r[C['word']]); g = r[C['grp']]; typ = str(r[C['typ']] or '')[:1]
        root = str(r[C['root']] or '')
        if root.strip() not in ('', '-'):
            for li, line in enumerate(root.split('\n')):
                if shenfen.cut(line): out['root_chain'].append((n, w, line[:60]))
                lab = LT.label_body(line)[0]
                if (li > 0 or lab is None) and shenfen.heqi_line(line, w) is not None: out['heqi_in_parts'].append((n, w, line[:60]))
                m = VARL.match(line)
                if m:
                    key = (g, m.group(2)); Y = (lab or '').strip('-')
                    if key not in FD.FAM or (Y not in FD.FAM[key][0] and shenfen.core(lab) not in FD.FAM[key][0]): out['fam_missing'].append((n, w, '%s → %s' % (m.group(2), Y)))
                    if not SF.search(line): out['var_no_id'].append((n, w, line[:60]))
        for col in ('pre', 'root', 'wp', 'suf'):
            for line in str(r[C[col]] or '').split('\n'):
                if col in ('pre', 'root') and INLINE_HEQI.search(line) and typ in ('①', '③'): out['heqi_in_parts'].append((n, w, line[:60]))
                if re.search(r'[；。]身份：|。分工：', line):
                    m = SF.search(line); k = line.find('；记：')
                    if not m or (k >= 0 and line.find('身份：') > k): out['id_bad'].append((n, w, line[max(0, line.find('身份：') - 10):][:60]))
        combo = str(r[C['combo']] or '')
        if 'bx' in C:
            if B.split_bianxi(combo)[1]: out['combo_bianxi'].append((n, w, ''))
            for col in ('combo', 'bg', 'suf', 'wp', 'pre', 'root', 'snd'):
                if '【辨析】' in B.split_bianxi(str(r[C[col]] or ''))[0]: out['ref_old'].append((n, w, hdr[C[col]][:4]))
            bx = str(r[C['bx']] or '')
            if bx:
                info['辨析列有内容'] += 1
                syn = [l for l in bx.split('\n') if l.startswith('【同义词】')]
                rest = '\n'.join(l for l in bx.split('\n') if not l.startswith('【同义词】'))
                if syn: info['有【同义词】行'] += 1
                lone = bool(syn)
                for l in syn:
                    m = SYN.match(l)
                    ws = [re.sub(r'（[^（）]*）', '', x).strip() for x in m.group(2).split('、')] if m else []
                    if not m or len(ws) < 2 or any(x not in words for x in ws): out['syn_bad'].append((n, w, l[:60]))
                    if any(x != w and B._has(x, rest) for x in ws): lone = False
                if lone: info['同义词组里的词辨析文字一个也没提到'] += 1; out['_todo'].append((n, w, syn[0][:50]))
        lines = combo.split('\n')
        for i, l in enumerate(lines):
            if l.startswith('\u3000合起来：'):
                ok = all(lines[j].startswith('\u3000') or (CO.sentence_from_eq(lines[j]) and not CO.STEP.match(lines[j])) for j in range(1, i))
                if not ok or i == 0: out['heqi_pos'].append((n, w, l[:50]))
    ap, st, miss = cizhui.plan(data, C)
    for ri in ap: out['affix_todo'].append((ri + 2, str(data[ri][C['word']]), '、'.join(ap[ri])))
    for k, v in cizhui.problems(data, C).items(): out[k] += v            # 2026-11 词缀身份辨析轮：词缀行的四项
    for k, v in xingtai.problems(data, C).items(): out[k] += v          # 2026-11 词根形态轮（第 107–112 条）：原来的动词变化四项换成形态四项
    info['写了“形态”的词根行'] = sum(1 for r in data for l in str(r[C['root']] or '').split('\n') if xingtai.get(l))
    return out, info, 'bx' in C

def main(path, show=6, todo=False):
    out, info, has_bx = check(path)
    total = 0
    for k in ('root_chain', 'heqi_in_parts', 'var_no_id', 'id_bad', 'fam_missing', 'affix_todo', 'affix_no_id', 'affix_old', 'bianxi_bad', 'bianxi_diff', 'guanxi_bad',
              'combo_bianxi', 'ref_old', 'syn_bad', 'heqi_pos',
              'xt_missing', 'xt_diff', 'xt_bad', 'xt_stray'):
        v = out[k]; total += len(v)
        print('%-14s %d' % (k, len(v)))
        for it in v[:show]: print('     ', it)
    if not has_bx: print('（这张表没有「辨析」列：combo_bianxi、ref_old、syn_bad 没查）')
    for k, v in info.items(): print('%s %d 行' % (k, v))
    if todo:
        for it in out['_todo']: print('   ', it)
    print('合计 %d' % total)
    return total

if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    main(a[0], int(a[1]) if len(a) > 1 else 6, '--todo' in sys.argv)
