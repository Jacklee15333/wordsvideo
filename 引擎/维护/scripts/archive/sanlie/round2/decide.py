"""词根列各行要不要加连字符（自动判断 + 人工核对），以及 28 个构词成分、几个标错列的词缀挪列"""
import re, pickle, sys
sys.path.insert(0, '/home/claude/skills_new/maintain/etymology-table/scripts')
import cols as C
common = pickle.load(open('/home/claude/common_en.pkl', 'rb'))
FOREIGN = re.compile(r'拉丁语|希腊语|古法语|法语|英法语|意大利语|西班牙语|阿拉伯语|古伊朗语|梵语|波斯语|荷兰语|德语|葡萄牙语|凯尔特语|高卢语')
HINT = re.compile(r'^\s*(由词根|词根|本组词根|=\s*(拉丁语|希腊语|古法语|法语|古英语|古诺尔斯语|中古英语|中世纪拉丁语|俗拉丁语|晚期拉丁语|意大利语|西班牙语|阿拉伯语|葡萄牙语|荷兰语|德语|英法语|古高地德语|盖尔语|凯尔特语|梵语))')
# 人工核对：英语里能单独用的词（母词、合成词的词、专有名词），不加连字符
FREE = {(18, 'people'), (25, 'people'), (27, 'people'), (168, 'live'), (169, 'live'), (467, 'in'), (692, 'ball'), (742, 'well'), (756, 'will'),
        (769, 'repeated'), (812, 'nigh'), (838, 'part'), (912, 'standing'), (914, 'stead'), (1065, 'pest'), (1233, 'prior'), (1574, 'medium'),
        (1578, 'medium'), (1640, 'reactive'), (1700, 'their'), (1732, 'light'), (1840, 'finite'), (2043, 'technique'), (2111, 'going'),
        (2113, 'going'), (2119, 'wind'), (2175, 'order'), (2188, 'arm'), (2189, 'arm'), (2462, 'colonise'), (2576, 'potent'), (2864, 'synthesize'),
        (3013, 'consequent'), (3490, 'image'), (3662, 'science'), (3691, 'utter'), (3861, 'mark'), (4074, 'post'), (4356, 'found'), (4607, 'our'),
        (4623, 'helm'), (4776, 'prize'), (4818, 'fleet'), (4877, 'opinionate'), (5204, 'authorize'), (5288, 'therapy'), (5350, 'diversity'),
        (5353, 'fuel'), (6014, 'mobile'), (6465, 'dump'), (7105, 'mine'), (7481, 'her'), (7561, 'cigar'), (7636, 'Hamburg'), (7894, 'Canton'),
        (7970, 'muse'), (7989, 'can'), (8172, 'maid(=mægð)'), (8193, 'bound'), (8258, 'Atlas'), (8355, 'plumb'), (8356, 'plumb'), (8467, 'bid'),
        (8593, 'guise'), (8595, 'gulf'), (8646, 'oil'), (8680, 'bound'), (8861, 'bar'), (8911, 'coca'), (8928, 'cumber'), (8936, 'mantle'),
        (8942, 'bark'), (9082, 'metre'), (9083, 'particle'), (9084, 'technology'), (9201, 'strand'), (9228, 'titan'), (9244, 'ravel'),
        (9270, 'cutler'), (5558, 'morrow'), (6278, 'jean(=Gene)'), (7721, 'trump')}
# 人工核对：不能单独用的词根（自动判断成了单词的），加连字符
BOUND = {(7596, 'vin'), (505, 'port'), (1650, 'min'), (2087, 'lve'), (7879, 'cli'), (5654, 'ni'), (8636, 'mar'), (3522, 'long')}
# 写在词根列、其实是前缀 / 后缀的：挪过去，标签补上连字符
TO_PRE = {(2154, 'de'), (2632, 'be'), (2764, 'en'), (3779, 'in'), (8642, 'ne'), (8665, 'pier')}
TO_SUF = {(5227, 'on'), (8815, 'di'), (2154, 't')}
# 希腊、拉丁构词成分组成的 28 个词（用户定下）：前缀列 / 后缀列 → 词根列，标签原样（bio-、-logue）
PRE_TO_ROOT = {722: 'hydro-', 1560: 'psycho-', 2453: 'thermo-', 4275: 'astro-', 4276: 'astro-', 5278: 'electro-', 5280: 'electr(o)-',
               5347: 'bio-', 5349: 'bio-', 5828: 'archaeo-', 6013: 'aut-', 6501: 'geo-', 6505: 'geo-', 6507: 'geo-', 6570: 'photo-',
               7264: 'rock-', 9112: 'Portugu-', 279: 'uni-', 2080: 'twi-', 5381: 'tri-'}
SUF_TO_ROOT = {1547: '-logy', 1552: '-logue', 1556: '-logue', 1558: '-logue', 1559: '-logue', 1462: '-ple', 5382: '-ple', 4377: '-llion'}


def root_decision(rn, word, typ, split, label, body, words):
    """→ 'bound' / 'free' / None（不是拆分里的部分、不是字母标签：不动）"""
    if label.startswith('-') or label.endswith('-'):
        return None
    base = re.sub(r'\([^)]*\)', '', label).strip()
    if not re.fullmatch("[A-Za-zāæþðēīōūÆǣ'’]+", base) or (len(base) < 2 and not base.islower()) or (len(base) > 1 and base.isupper()):
        return None                     # 缩写里的大写字母（scuba 的 B）不算；连接元音、双写的字母（-i-、-t-）算
    if not C.split_positions(split).get(C._norm(label)):
        return None
    if len(base) == 1: return 'bound'          # 单个小写字母：连接元音、双写的字母、残留的字母，都不是能单独用的词
    if (rn, label) in FREE: return 'free'
    if (rn, label) in BOUND: return 'bound'
    eng = base.lower() in words or base.lower() in common
    if not eng: return 'bound'
    if re.search(r'见\s*(第 \d+ 组 )?' + re.escape(base.lower()[:max(3, len(base) - 1)]), body.lower()): return 'free'
    if HINT.match(body): return 'bound'
    if typ.startswith('③'): return 'free'
    if body.strip().startswith('=') or FOREIGN.search(body) or re.search(r'见 [A-Za-z]', body): return 'bound'
    return 'free'
