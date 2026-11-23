"""加词缀时拼写有变化的：逐个边界认出是哪种现象，写一句说明（补在那个词缀那一行末尾）。"""
import re
V = 'aeiou'
DONE = re.compile(r'去掉 ?e|去 ?e[^a-z]|e 去掉|省掉|省去|丢掉|e 不写|脱落|只写一个|就去掉|拿掉|y ?(变|改|换)成? ?i|y ?→ ?i|变成 i|双写|重写|写两个|两个 [a-z]|-bil-|bility|le 换|换成 -?ly|变成 -?ly|不去 e|保留 e|留着 e|e 留着|变成 -?ss|变成 s|变成 v|变成 y|t 换成|te 换成|-fication|元音去掉|元音也变|元音变|e 常去掉|同化|变成 [a-z]{1,3}-')
NOT_STRESS_FINAL_L = None
STRESS_FINAL = set('compel excel expel propel rebel repel dispel fulfil instil distil control patrol enrol extol begin forget occur prefer refer transfer admit permit commit emit omit submit equip regret'.split())

def norm(p):
    p = p.strip()
    p = re.sub(r'\(=[^()]*\)', '', p)
    p = re.sub(r'\(([^()=]*)\)', '', p)
    return p.lower().replace('-', '').replace("'", '').replace(' ', '')

def labels(d):
    out = {}
    for col in 'JKLM':
        for i, l in enumerate(d[col].split('\n')):
            m = re.match(r'^([^：:]{1,40})[：:]', l)
            if m:
                out.setdefault(m.group(1).strip().strip('-').lower(), (col, i))
    return out

def classify(prev, nxt, rest, word, raw_prev):
    """返回 (类, 说明)；说明里 {b} 前一部分、{s} 后缀、{w} 单词"""
    b, s, w = raw_prev, nxt, word
    exact = rest.startswith(prev + nxt[:1]) or (rest.startswith(prev) and not nxt)
    if exact:
        if re.search(r'[cg]e$', prev) and nxt[:1] in ('a', 'o'):
            snd = '/s/' if prev[-2] == 'c' else '/dʒ/'
            hard = '/k/' if prev[-2] == 'c' else '/g/'
            return 'keep_e_soft', (prev, '%s 末尾的 e 这里不去掉：%s 后面直接跟 %s 会读成 %s，留着 e 才读 %s：%s + %s → %s' % (b, prev[-2], nxt[0], hard, snd, b, s, w))
        return None, prev
    tries = []
    if prev.endswith('ce') and nxt == 'tion':
        tries.append(('ce_ct', prev[:-2] + 'c', '%s 的 ce 遇到 -tion 变成 c：%s → %s（照拉丁语过去分词词干 -duct-；同 reduce → reduction、produce → production）' % (b, b, w)))
    if prev.endswith(('or', 'er')) and nxt == 'ess':
        tries.append(('ess', prev[:-2] + 'r', '%s 加 -ess 时，%s 里的元音去掉：%s + ess → %s（同 actor → actress、waiter → waitress）' % (b, prev[-2:], b, w)))
    if prev.endswith('e'):
        if nxt[:1] in V or nxt[:1] == 'y':
            if nxt in ('er', 'ed', 'en', 'est'):
                tries.append(('drop_e_done', prev[:-1], None))
            elif nxt[:1] == 'y':
                tries.append(('drop_e', prev[:-1], '%s 末尾的 e 遇到 -y 也要去掉（y 在这里当元音用）：%s + %s → %s' % (b, b, s, w)))
            else:
                tries.append(('drop_e', prev[:-1], '%s 末尾的 e 遇到元音开头的 -%s 就去掉：%s + %s → %s' % (b, s, b, s, w)))
        else:
            tries.append(('drop_e_cons', prev[:-1], '%s 末尾的 e 遇到辅音开头的 -%s 一般不去（useful、lovely），%s 是例外：%s + %s → %s' % (b, s, w, b, s, w)))
    if prev.endswith('ie') and nxt.startswith('i'):
        tries.append(('ie_y', prev[:-2] + 'y', '%s 的 ie 遇到 -%s 变成 y：%s + %s → %s（同 lie → lying、tie → tying）' % (b, s, b, s, w)))
    if re.search(r'[^aeiou]y$', prev) and nxt[:1] != 'i':
        tries.append(('y_i', prev[:-1] + 'i', '%s 末尾的 y 前面是辅音，加 -%s 时 y 变成 i：%s + %s → %s' % (b, s, b, s, w)))
    if prev.endswith('y') and nxt[:1] == 'i':
        tries.append(('y_drop', prev[:-1], '%s 末尾的 y 遇到 i 开头的 -%s 就去掉：%s + %s → %s' % (b, s, b, s, w)))
    if prev.endswith('le') and nxt == 'ly':
        tries.append(('le_ly', prev[:-2], '%s 以 -le 结尾，加 -ly 时把 le 换成 ly，不写成 %sly：%s + ly → %s' % (b, b, b, w)))
    if prev.endswith('ble') and nxt[:1] == 'i':
        tries.append(('ble_bil', prev[:-2] + 'il', '%s 末尾的 -ble 遇到 -%s 变成 -bil-：%s + %s → %s（同 able → ability、possible → possibility）' % (b, s, b, s, w)))
    if prev.endswith('le') and nxt[:1] in 'a':
        tries.append(('le_ul', prev[:-2] + 'ul', '%s 末尾的 -le 加 -%s 时变成 -ul-：%s → %s（拉丁语原词就是 -ulus，同 circle → circular、single → singular）' % (b, s, b, w)))
    if prev.endswith('nt') and nxt in ('ce', 'cy'):
        tries.append(('nt_nce', prev[:-1], '-nt 结尾的形容词变名词，t 换成 -%s：%s → %s（同 silent → silence、frequent → frequency）' % (s, b, w)))
    if prev.endswith('te') and nxt == 'cy':
        tries.append(('te_cy', prev[:-2], '-ate 结尾的形容词变名词，te 换成 -cy：%s → %s（同 private → privacy、accurate → accuracy）' % (b, w)))
    if prev.endswith('ous') and nxt == 'ity':
        tries.append(('ous_os', prev[:-3] + 'os', '-ous 加 -ity 变成 -osity：%s → %s（同 generous → generosity、curious → curiosity）' % (b, w)))
    if prev.endswith('fy') and nxt == 'ation':
        tries.append(('fy_fic', prev[:-1] + 'ic', '-fy 结尾的动词变名词是 -fication（y 变 i，再多一个 c，照拉丁语 -ficatio）：%s → %s（同 qualify → qualification、notify → notification）' % (b, w)))
    if prev == 'apply':
        tries.append(('fy_fic', 'applic', 'apply 的 y 变成 i，还多出一个 c（来自拉丁语 applicare）：apply → %s（同 application、applicable、applicant）' % w))
    if prev.endswith('er') and (nxt[:1] in V or nxt[:1] == 'y'):
        tries.append(('er_r', prev[:-2] + 'r', '%s 末尾的 -er 加元音开头的 -%s 时，er 里的 e 常去掉：%s → %s（同 hunger → hungry、enter → entry、disaster → disastrous）' % (b, s, b, w)))
    if prev.endswith(('or', 'er')) and nxt == 'ess':
        tries.append(('ess', prev[:-2] + 'r', '%s 加 -ess 时，%s 里的元音去掉：%s + ess → %s（同 actor → actress、waiter → waitress）' % (b, prev[-2:], b, w)))
    if prev[-1:] in 'aoi' and (nxt[:1] in V):
        tries.append(('vowel_drop', prev[:-1], '%s 末尾的元音 %s 遇到元音开头的 -%s 就去掉：%s + %s → %s' % (b, prev[-1], s, b, s, w)))
    if re.search(r'de?$', prev) and nxt in ('ion', 'ive', 'ible'):
        stem = re.sub(r'de?$', '', prev)
        tries.append(('d_s', stem + 's', '%s 的 d(e) 遇到 -%s 变成 s：%s → %s（照拉丁语过去分词的拼法；同 decide → decision、divide → division、include → inclusion）' % (b, s, b, w)))
        tries.append(('d_t', stem + 't', '%s 的 d 遇到 -%s 变成 t：%s → %s（照拉丁语过去分词的拼法，同 attend → attention）' % (b, s, b, w)))
    if prev.endswith('t') and nxt in ('ion', 'ible'):
        tries.append(('t_ss', prev[:-1] + 'ss', '%s 末尾的 t 遇到 -%s 变成 ss：%s → %s（照拉丁语过去分词的拼法；同 permit → permission、admit → admission）' % (b, s, b, w)))
    if prev.endswith('ceive'):
        tries.append(('ceive', prev[:-5] + 'cep', '-ceive 的名词是 -ception：%s → %s（同 receive → reception、perceive → perception）' % (b, w)))
    if prev.endswith('scribe'):
        tries.append(('scribe', prev[:-6] + 'scrip', '-scribe 的名词、形容词是 -scription、-scriptive：%s → %s（同 describe → description、subscribe → subscription）' % (b, w)))
    if prev.endswith('tain'):
        tries.append(('tain', prev[:-4] + 'ten', '-tain 的名词是 -tention / -tenance：%s → %s（同 retain → retention、maintain → maintenance）' % (b, w)))
    if prev.endswith('sume'):
        tries.append(('sume', prev[:-4] + 'sump', '-sume 的名词是 -sumption：%s → %s（同 consume → consumption、assume → assumption）' % (b, w)))
    if prev.endswith('olve'):
        tries.append(('olve', prev[:-4] + 'olu', '-solve、-volve 的名词是 -solution、-volution（v 变回拉丁语的 u）：%s → %s（同 solve → solution、evolve → evolution）' % (b, w)))
    if prev.endswith('ai' + prev[-1:]) and len(prev) > 3:
        tries.append(('ai_a', prev[:-3] + 'a' + prev[-1], '%s 的 ai 加 -%s 时变成 a：%s → %s（同 explain → explanation、exclaim → exclamation）' % (b, s, b, w)))
    if prev.endswith('ounce'):
        tries.append(('ou_u', prev[:-5] + 'unci', 'pronounce 的 ou 在名词里变成 u：pronounce → pronunciation（拼法照拉丁语 pronuntiatio；读音 /prəˌnʌnsiˈeɪʃn/，不读 pro-NOUN-）'))
    if prev.endswith('ce') and nxt == 'tion':
        tries.append(('ce_ct', prev[:-2] + 'c', '%s 的 ce 遇到 -tion 变成 c：%s → %s（照拉丁语过去分词词干 -duct-；同 reduce → reduction、produce → production）' % (b, b, w)))
    if prev == 'destroy':
        tries.append(('destroy', 'destru', 'destroy 的名词、形容词照拉丁语 destructus 拼：destroy → %s（同 destruction、destructive）' % w))
    if prev.endswith('isfy'):
        tries.append(('fy_fac', prev[:-1] + 'ac', '-fy 有的变 -faction：satisfy → %s（照拉丁语 satisfactio）' % w))
    if nxt in ('th', 't') and len(prev) >= 3:
        for k in range(1, len(prev)):
            tries.append(('th_vowel', None, '%s 加 -%s 变名词时元音也变了：%s → %s（同 long → length、strong → strength、deep → depth）' % (b, s, b, w)))
            break
    if prev.endswith('ll'):
        tries.append(('ll_l', prev[:-1], None))
    if prev.endswith('f'):
        tries.append(('f_v', prev[:-1] + 'v', '%s 的 f 加 -%s 变成 v：%s → %s（同 leaf → leaves）' % (b, s, b, w)))
    if prev.endswith('our'):
        tries.append(('our_or', prev[:-3] + 'or', '%s 的 -our 加 -%s 时变成 -or-：%s → %s（同 humour → humorous、vigour → vigorous）' % (b, s, b, w)))
    # 没写出来的双写
    if prev[-1:] not in V + 'wxy' and nxt[:1] in V + 'y':
        tries.append(('double_hidden', prev + prev[-1], None))
    for k, p2, note in tries:
        if p2 is None:
            if k == 'th_vowel' and rest.endswith(nxt):
                return k, (rest[:len(rest) - len(nxt)], note)
            continue
        if rest.startswith(p2 + nxt[:1]) or (rest.startswith(p2) and not nxt):
            return k, (p2, note)
    return 'other', None
