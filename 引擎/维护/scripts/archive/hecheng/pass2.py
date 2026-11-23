"""第二遍：写法那一行已经讲了、原处还重复的话，逐条删或改（('del', 行开头) / ('sub', 旧, 新) / ('Pdel', 音变列行开头)）"""
EDITS = {
    'altogether': [('del', '【辨析】altogether（完全；总共）≠ all together')],
    'nobody': [('sub', '（no one 必须分写）', '')],
    'ten-dollar': [('del', '【语法】数词 + 名词连成定语时加连字符')],
    'seven-mile': [('del', '【语法】“数词 + 名词”作前置定语时用连字符')],
    'four-day': [('del', '【语法】“数词 + 名词”连成形容词放在名词前时')],
    'two-hour': [('del', '【语法】“数词 + 名词”连成复合形容词放在名词前时')],
    'fifteen-year': [('del', '【语法】连字符复合形容词放在名词前，里面的名词用单数')],
    'pick-up': [('del', '【语法】短语动词连成名词时，常加连字符或干脆连写')],
    'money-making': [('del', '【语法】来自动宾短语 make money')],
    'after-school': [('del', '（放在名词前时加连字符；单说“放学后”不加）')],
    'skipping-beat': [('del', '（连字符的 skipping-beat 一般词典不单收')],
    'horse-hair': [('del', '（也常连写成 horsehair）')],
    'non-migrating': [('del', '（non- 后常加连字符，美式也常连写成 nonmigrating）')],
    'heart-broken': [('del', '【辨析】今天词典多以连写的 heartbroken 为主词条')],
    'penpal': [('sub', '【辨析】词典多写作 pen pal 或 pen-pal，连写 penpal 也常见；英式也说 pen-friend', '【辨析】英式也说 pen-friend')],
    'slam-dunk': [('Pdel', '名词常写成 slam dunk')],
    'auto-location': [('Pdel', '连字符复合词，词典一般不单列')],
    'aqua-classroom': [('del', '【提醒】这类带连字符的新造词多见于具体活动、场馆的名称')],
    'human-tech': [('del', '【提醒】新近的连字符组合，词典一般不单列')],
    'first-ever': [('sub', '（只放在名词前，带连字符）', '（只放在名词前）')],
    'forever': [('sub', '（14 世纪分开写，17 世纪末起常合成一个词）', '')],
    'wasteland': [('sub', '（1825 年起才连写成一个词）', '')],
    'lunchtime': [('sub', '（1821 年就有 lunch-time 的写法，今天多连写）', '')],
    'barcode': [('del', '→ 起初分写成 bar code，后来也常连写')],
    'third-floor': [('sub', '两个词用连字符连起来放在名词前面，', '放在名词前面，')],
    '100-foot-tall': [('sub', '用连字符把几个词连成一个形容词，放在名词前面', '几个词连成一个形容词，放在名词前面')],
    'five-hundred-metre': [('sub', '几个词用连字符连成一个整体，放在名词前面当形容词', '几个词连成一个整体，放在名词前面当形容词')],
    'time-and-money': [('sub', '，用连字符连成一个词', '')],
    'first-aid': [('sub', '放在名词前，用连字符连起来', '放在名词前')],
    'photosynthesis-enhanced': [('sub', '用连字符连成一个形容词，放在名词前（见【语法】）', '连成一个形容词，放在名词前')],
    'right-and-wrong': [('sub', '用连字符放在名词前', '放在名词前')],
    'salty-tasting': [('sub', '，放在名词前要加连字符', '')],
    'black-and-white': [('del', '【辨析】in black and white 不加连字符')],
}
SPELL_MORE = {
    'altogether': 'altogether（一个词）是“完全；总共”，all 掉了一个 l：That\'s altogether wrong.；all together（两个词）是“全都在一起”：We were all together in the room.；OED 指出常有人把该分开写的 all together 错写成 altogether',
    'penpal': '词典多写作 pen pal 或 pen-pal，连写 penpal 也常见',
    'slam-dunk': ('W02', '名词常写成 slam dunk，作动词时多加连字符：slam-dunk the ball；词典里两种写法都见'),
    'auto-location': '新组合，词典一般不单列（auto- 是 automatic 截短来的构词成分）',
    'aqua-classroom': '这类新造的组合多见于具体活动、场馆的名称，词典一般不收',
    'human-tech': '新近的组合，词典一般不单列，意思要看上下文',
    'black-and-white': 'a black-and-white film；不放在名词前时分开写：in black and white 白纸黑字、写成文字（Put it in black and white.）',
}


def apply_edits(word, keep, newP):
    for op in EDITS.get(word, []):
        if op[0] == 'del':
            n = len(keep)
            keep = [l for l in keep if not l.strip().startswith(op[1])]
            assert len(keep) == n - 1, ('del miss', word, op)
        elif op[0] == 'sub':
            hit = [i for i, l in enumerate(keep) if op[1] in l]
            assert len(hit) == 1, ('sub miss', word, op)
            keep[hit[0]] = keep[hit[0]].replace(op[1], op[2]).rstrip()
        elif op[0] == 'Pdel':
            L = [l for l in str(newP or '').split('\n') if l.strip()]
            n = len(L)
            L = [l for l in L if not l.strip().startswith(op[1])]
            assert len(L) == n - 1, ('Pdel miss', word, op)
            newP = '\n'.join(L) if L else None
    return keep, newP
