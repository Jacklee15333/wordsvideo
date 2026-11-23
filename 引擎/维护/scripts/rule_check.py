"""用词规律体检（rule_check.py）：规律的前提（“表示动作的词…”“表示东西、性质的词…”）和这个词本身的词性对不对得上；“某一行”“英美”“复数”规律那一步有没有对应标记；“做…的人”后来指机器还没标规律的。
用法：python3 rule_check.py <总表.xlsx> [每类列几条]。各类的正常基线见 references/audit_checklist.md。"""
import re, sys, json, collections
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import columns as C
KEYS = {
 '一个词用进某一行': 'domain', '同一个词，英国、美国': 'region', '不好直说的事': 'euphem', '说“可怕、厉害、真的”': 'degree', '东西变了，旧名字': 'oldname',
 '东西换了代': 'oldname', '词的核心意思不变': 'core', '作用、做法像什么': 'likefunc',      # 2026-11 用词规律轮：新说法（上一行前两条、“东西变了”是取消了的旧说法，表里不该再有）
 '表示材料的词': 'material', '表示动物、植物的词': 'animal', '表示东西的词，也拿来说这种东西的颜色': 'color', '样子、形状像什么': 'shape', '说动物、东西的词，也拿来比喻人': 'people',
 '说冷热、软硬': 'feel', '说空间、位置的词': 'time', '表示地方、建筑的词': 'place', '表示容器的词': 'container', '装东西的容器、身体部位': 'unit', '名词用复数时': 'plural',
 '表示动作的词，也拿来叫做这件事用的东西': 'tool', '表示动作的词，也拿来叫这个动作做出来': 'result', '表示动作、东西的词，也拿来叫做这件事的人': 'person',
 '表示性质、状态的词，也拿来叫有这种性质': 'holder', '表示东西、性质的词，也能直接当动词用': 'n2v', '名词放在别的名词前面': 'n2adj', '表示动作的词，也能直接当名词用': 'v2n',
 '具体的意思，慢慢用到': 'abstract', '一个词的褒贬会变': 'value', '一个词的意思越用越窄': 'narrow', '一个词的意思越用越宽': 'widen', '表示“做这件事的人”的词': 'agent2tool'}
def key_of(text):
    return next((v for k, v in KEYS.items() if text.startswith(k)), '?')
DOM = r'法律|医学|医|计算机|电脑|网络|互联网|体育|篮球|足球|网球|棒球|音乐|化学|物理|数学|生物|航海|军事|宗教|商业|金融|经济|影视|电影|摄影|戏剧|语法|语言学|教学|科幻|天文|地理|建筑|艺术|新闻|印刷|农业|烹饪|美术|心理|电子|机械|游戏|植物学|动物学|解剖|统计|会计|政治|外交|天主教|基督教|赛车|拳击|高尔夫|板球'
DEVICE = re.compile(r'机器|装置|设备|仪器|仪|器$|器[、；（]|机$|机[、；（]|软件|程序|工具')
def word_pos(d, H):
    pos = d.get('pos', [])
    if pos:
        lab, txt = pos[-1]
        head = txt.split('。')[0]
        m = re.search(r'(?:→\s*|变成)(名词|形容词|动词|副词)', head)
        p = m.group(1) if m else ''
        if p == '名词' and re.search(r'（人', head): return 'agent'
        if p == '名词' and re.match(r'\s*形容词', head): return 'statenoun'
        if p == '名词' and re.match(r'\s*动词', head): return 'actnoun'
        return {'名词': 'noun', '形容词': 'adj', '动词': 'verb', '副词': 'adv'}.get(p, '')
    return 'base'
def load(path):
    from openpyxl import load_workbook
    import cols
    return [(i, cols.legacy(r)) for i, r in enumerate(load_workbook(path, read_only=True)['拆分结果'].iter_rows(values_only=True), start=1) if i > 1]   # 前缀、词根、单词部分、后缀合成一格，列号照旧
def audit(rows):
    out = collections.defaultdict(list)
    for rn, r in rows:
        w = str(r[4]); d = C.parse_I(r[10])
        if 'raw' in d or not d.get('rules'): continue
        cat = word_pos(d, r[9])
        steps = [l for l in d['logic'][1:] if C.STEP.match(l)]
        for st in steps:
            marks = ''.join(C.MARK.findall(st))
            res = re.split(r'\s*→\s*', C.MARK.sub('', st))[-1].strip()
            for n in marks:
                t = d['rules'].get(n, ''); k = key_of(t)
                item = (rn, w, cat, n, k, st.strip()[:110], t[:60])
                if k in ('tool', 'result', 'v2n') and cat == 'agent':
                    out['A 做…的人的词，套了“表示动作的词…”' + ('（这一步是机器）' if DEVICE.search(res) else '')].append(item)
                elif k in ('tool', 'result', 'v2n') and cat in ('adj', 'adv'):
                    out['B 形容词/副词，套了“表示动作的词…”'].append(item)
                elif k in ('tool', 'result') and cat == 'statenoun':
                    out['C 性质名词（-ness/-ity…），套了“表示动作的词…”'].append(item)
                elif k == 'v2n' and cat in ('actnoun', 'statenoun', 'noun'):
                    out['D 本来就是名词，套了“动作直接当名词用”'].append(item)
                elif k == 'n2v' and cat == 'verb':
                    out['E 本来就是动词，套了“东西、性质直接当动词用”'].append(item)
                elif k == 'n2adj' and cat in ('adj', 'verb', 'adv'):
                    out['F 不是名词，套了“名词当形容词用”'].append(item)
                # 2026-11 用词规律轮：这两条说法（和“东西变了，旧名字还接着用”的旧写法）已经取消，表里不该再有——
                # 它们只说了“有了专门意思”“两边不一样”，没讲出意思是怎么来的。再出现就逐条换成真规律（core / likefunc / narrow…），找不到的去掉
                if k in ('domain', 'region') or t.startswith('东西变了，旧名字'):
                    out['G 取消了的空洞说法（用进某一行 / 英美不一样 / 东西变了）还在表里'].append(item)
                if k == 'plural' and '复数' not in st:
                    out['I “复数”，这一步没写复数'].append(item)
                if k == '?':
                    out['J 规律认不出'].append(item)
    # K：规律说“表示动作的词…”，本词原来的意思（规律例子里本词 → 前面那半）却是个东西
    NOUNISH = re.compile(r'(器|物|品|者|人|员|家|机|具|子|头|所|处|场|馆|室|院|会|局|队|团|书|图|表|单|卡|票|证|车|船|机构|系统|工具|装置|琴|针|刀|杆|板|门|墙|甲|服|衣|帽|鞋|袋|盒|箱|瓶|杯|碗|桌|椅|床|屋|房|城|山|河|海|树|花|草|鸟|鱼|虫|兽|马|牛|羊|猪|狗|猫)$')
    seen = {(it[0], it[3], it[5]) for v in out.values() for it in v}
    for rn, r in rows:
        w = str(r[4]); d = C.parse_I(r[10])
        if 'raw' in d or not d.get('rules'): continue
        cat = word_pos(d, r[9])
        for st in [l for l in d['logic'][1:] if C.STEP.match(l)]:
            for n in ''.join(C.MARK.findall(st)):
                t = d['rules'].get(n, ''); k = key_of(t)
                if k not in ('tool', 'result', 'v2n') or (rn, n, st.strip()[:110]) in seen: continue
                m = re.search(r'（' + re.escape(w) + r'[：:]?\s*([^→（）]*?)\s*→', t)
                src = m.group(1).strip() if m else ''
                if src and NOUNISH.search(re.split(r'[、；/]', src)[0].strip()):
                    out['K 规律说“表示动作的词”，本词原来的意思却是个东西'].append((rn, w, cat, n, k, st.strip()[:110], t[:60]))
    # L：“做…的人”的词，后来指机器、工具，那一步还没标规律
    for rn, r in rows:
        d = C.parse_I(r[10])
        if 'raw' in d or word_pos(d, r[9]) != 'agent': continue
        steps = [l for l in d['logic'][1:] if C.STEP.match(l)]
        res = [re.split(r'\s*→\s*', C.MARK.sub('', s))[-1] for s in steps]
        person = [i for i, x in enumerate(res) if re.search(r'(人|者|员|工|手|家|师|商)([、；（]|$)', x)]
        for i, (s, x) in enumerate(zip(steps, res)):
            if person and i > person[0] and DEVICE.search(x) and not re.search(r'(人|者|员|师|手|家)([、；（]|$)', x) and not C.MARK.search(s):
                out['L 做…的人的词，后来指机器、工具，还没标规律'].append((rn, str(r[4]), 'agent', '', '', s.strip()[:110], ''))
    return out
if __name__ == '__main__':
    rows = load(sys.argv[1])
    out = audit(rows)
    tot = 0
    for k in sorted(out):
        v = out[k]; tot += len(v)
        print('=====', k, len(v))
        for it in v[:int(sys.argv[2]) if len(sys.argv) > 2 else 4]: print('  ', it[1], it[2], it[3], '|', it[5], '|', it[6])
    print('合计', tot)
