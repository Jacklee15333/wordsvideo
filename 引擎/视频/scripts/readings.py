#!/usr/bin/env python3
"""6.17 起（第五十四版）：配音里英文的四种念法——synth.py 合成之前调 prepare() 把配音稿改成配音模型念得出的样子。

用户：“单个的字母就不要换讲解员了，就用我自己的音色就可以了；然后前后缀，词根要当作单词来读，不要变成单个字母读”
     “p --- f 这些讲的是发音，不能按字母来读。p,t,k 念成 f,th,h 这些也是发音……要当作读音来读的”
     “词根，词缀当单词读，用美语音色”“是发音的一个或两个字母，也要用美语音色”

配音稿（plan.json）里的写法 → 怎么念：
  1. 单独的字母（e、u、加 s、c 和 s 合写成 x、答案是 D、去掉词尾 e r e）→ 你本人的声音念字母名，夹在中文里，不换声音（synth.split_mixed）
  2. /音标/（/p/、/θ/、/juː/）→ 美式女声念这个音（不念字母名）
  3. 词缀写成 pro-（前缀）、-ion（后缀，拉丁语词尾 -ere、-us 也这样写）→ 美式女声当单词念，读音查下面的词缀表，没有再查英文词典、espeak-ng
  4. 词根和别的英文词照写（duc、duce、produce）→ 美式女声当单词念；英文词典里没有的（duc、ject、struct）用 espeak-ng 按拼读规则念，
     不再一个个字母念、也不会被配音模型整个跳过（6.10 以前出空的声音）。plan.json 的 lexicon 手写的读音最优先。

做法：/音标/、词缀、词典里没有的词各换成一个音素词（qzq 开头，和读音拆分的 qz 音素词一样，读音写进配音模型的词典），
只在合成时换；manifest 里的文字还是配音稿原来的样子（画面按它对时间）。
"""
import ctypes, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- 词缀表（美式读音，国际音标）
# 当单词念：念它在单词里的音（-ous 念 /əs/，不念 /uːz/；-tion 念 /ʃən/），单独念时重读，听得清
# 想改哪个的念法：改这里，或者在 plan.json / prefs.json 的 lexicon 里写 qzqp<前缀> / qzqs<后缀> 的音素
PREFIX_IPA = {
    'a': 'ə', 'ab': 'æb', 'abs': 'æbs', 'ac': 'æk', 'ad': 'æd', 'af': 'æf', 'ag': 'æɡ', 'al': 'æl', 'an': 'æn', 'ana': 'ænə',
    'ante': 'ænti', 'anti': 'ænti', 'ap': 'æp', 'ar': 'ɑɹ', 'as': 'æs', 'at': 'æt', 'auto': 'ɔtoʊ', 'be': 'bi', 'bene': 'bɛnə',
    'bi': 'baɪ', 'by': 'baɪ', 'cata': 'kætə', 'centi': 'sɛnti', 'circum': 'sɜɹkəm', 'co': 'koʊ', 'col': 'kɑl', 'com': 'kɑm',
    'con': 'kɑn', 'contra': 'kɑntɹə', 'cor': 'kɔɹ', 'counter': 'kaʊntəɹ', 'de': 'di', 'deca': 'dɛkə', 'di': 'daɪ', 'dia': 'daɪə',
    'dif': 'dɪf', 'dis': 'dɪs', 'du': 'du', 'dys': 'dɪs', 'e': 'i', 'ec': 'ɛk', 'ef': 'ɛf', 'em': 'ɪm', 'en': 'ɪn', 'epi': 'ɛpi',
    'equi': 'ikwi', 'eu': 'ju', 'ex': 'ɛks', 'extra': 'ɛkstɹə', 'fore': 'fɔɹ', 'hemi': 'hɛmi', 'hetero': 'hɛtəɹoʊ', 'homo': 'hoʊmoʊ',
    'hyper': 'haɪpəɹ', 'hypo': 'haɪpoʊ', 'il': 'ɪl', 'im': 'ɪm', 'in': 'ɪn', 'inter': 'ɪntəɹ', 'intra': 'ɪntɹə', 'intro': 'ɪntɹoʊ',
    'ir': 'ɪɹ', 'kilo': 'kɪloʊ', 'mal': 'mæl', 'micro': 'maɪkɹoʊ', 'mid': 'mɪd', 'milli': 'mɪli', 'mis': 'mɪs', 'mono': 'mɑnoʊ',
    'multi': 'mʌlti', 'ne': 'ni', 'neo': 'nioʊ', 'non': 'nɑn', 'ob': 'ɑb', 'oc': 'ɑk', 'of': 'ɑf', 'omni': 'ɑmni', 'op': 'ɑp',
    'out': 'aʊt', 'over': 'oʊvəɹ', 'pan': 'pæn', 'para': 'pæɹə', 'pen': 'pɛn', 'per': 'pɜɹ', 'peri': 'pɛɹi', 'poly': 'pɑli',
    'post': 'poʊst', 'pre': 'pɹi', 'pro': 'pɹoʊ', 're': 'ɹi', 'retro': 'ɹɛtɹoʊ', 'se': 'si', 'semi': 'sɛmi', 'sub': 'sʌb',
    'suc': 'sʌk', 'suf': 'sʌf', 'sug': 'sʌɡ', 'sum': 'sʌm', 'sup': 'sʌp', 'super': 'supəɹ', 'sur': 'sɜɹ', 'sus': 'sʌs',
    'sym': 'sɪm', 'syn': 'sɪn', 'tele': 'tɛlə', 'trans': 'tɹænz', 'tri': 'tɹaɪ', 'twi': 'twaɪ', 'ultra': 'ʌltɹə', 'un': 'ʌn',
    'under': 'ʌndəɹ', 'uni': 'juni', 'up': 'ʌp', 'vice': 'vaɪs', 'with': 'wɪθ',
}
SUFFIX_IPA = {
    'able': 'əbəl', 'ably': 'əbli', 'ac': 'æk', 'acy': 'əsi', 'ade': 'eɪd', 'age': 'ɪdʒ', 'al': 'əl', 'an': 'ən', 'ance': 'əns',
    'ancy': 'ənsi', 'ant': 'ənt', 'ar': 'əɹ', 'ard': 'əɹd', 'ary': 'ɛɹi', 'ate': 'eɪt', 'ation': 'eɪʃən', 'ative': 'ətɪv',
    'cian': 'ʃən', 'cy': 'si', 'dom': 'dəm', 'ed': 'ɪd', 'ee': 'i', 'eer': 'ɪɹ', 'el': 'əl', 'en': 'ən', 'ence': 'əns',
    'ency': 'ənsi', 'ent': 'ənt', 'er': 'əɹ', 'ery': 'əɹi', 'es': 'ɪz', 'ese': 'iz', 'ess': 'əs', 'est': 'ɪst', 'et': 'ɪt',
    'ette': 'ɛt', 'fold': 'foʊld', 'ful': 'fəl', 'fy': 'faɪ', 'hood': 'hʊd', 'ia': 'iə', 'ial': 'iəl', 'ian': 'iən', 'ible': 'əbəl',
    'ibly': 'əbli', 'ic': 'ɪk', 'ied': 'id', 'ies': 'iz', 'iest': 'iɪst', 'ical': 'ɪkəl', 'ics': 'ɪks', 'ide': 'aɪd', 'ie': 'i', 'ier': 'iəɹ', 'ify': 'ɪfaɪ', 'ile': 'aɪl',
    'ine': 'aɪn', 'ing': 'ɪŋ', 'ion': 'ən', 'ior': 'iəɹ', 'ious': 'iəs', 'ise': 'aɪz', 'ish': 'ɪʃ', 'ism': 'ɪzəm', 'ist': 'ɪst',
    'ite': 'aɪt', 'itis': 'aɪtɪs', 'ity': 'ɪti', 'ive': 'ɪv', 'ize': 'aɪz', 'kin': 'kɪn', 'less': 'ləs', 'let': 'lət', 'like': 'laɪk',
    'ling': 'lɪŋ', 'logy': 'lədʒi', 'ly': 'li', 'ment': 'mənt', 'ness': 'nəs', 'ology': 'ɑlədʒi', 'or': 'əɹ', 'ory': 'ɔɹi',
    'ous': 'əs', 'ry': 'ɹi', 's': 'z', 'ship': 'ʃɪp', 'sion': 'ʒən', 'some': 'səm', 'ster': 'stəɹ', 'teen': 'tin', 'th': 'θ',
    'tion': 'ʃən', 'ty': 'ti', 'ual': 'uəl', 'ure': 'əɹ', 'ward': 'wəɹd', 'wards': 'wəɹdz', 'ways': 'weɪz', 'wise': 'waɪz',
    'y': 'i',
    # 拉丁语、希腊语的词尾（“形态”那一幕：ducere 去掉词尾 -ere）：照拉丁语的音念，美式女声
    'a': 'ɑ', 'ae': 'aɪ', 'ans': 'ɑns', 'are': 'ɑɹɛ', 'ari': 'ɑɹi', 'atum': 'ɑtʊm', 'atus': 'ɑtʊs', 'avi': 'ɑvi', 'ens': 'ɛns',
    'ere': 'ɛɹɛ', 'eri': 'ɛɹi', 'evi': 'ɛvi', 'i': 'i', 'io': 'ioʊ', 'ire': 'iɹɛ', 'iri': 'iɹi', 'is': 'ɪs', 'itum': 'itʊm',
    'itus': 'itʊs', 'ivi': 'ivi', 'o': 'oʊ', 'on': 'ɑn', 'os': 'ɑs', 'sus': 'sʊs', 'tum': 'tʊm', 'tus': 'tʊs', 'um': 'ʊm',
    'us': 'ʊs', 'xi': 'ksi',
}


# ---------------------------------------------------------------- 国际音标 → 配音模型（Kokoro）的音素
_MULTI = ['tʃ', 'dʒ', 'eɪ', 'aɪ', 'ɔɪ', 'aʊ', 'oʊ', 'əʊ', 'iː', 'uː', 'ɑː', 'ɔː', 'ɜː', 'ɪə', 'eə', 'ʊə']
_MAP = {'tʃ': 'ʧ', 'dʒ': 'ʤ', 'eɪ': 'A', 'aɪ': 'I', 'ɔɪ': 'Y', 'aʊ': 'W', 'oʊ': 'O', 'əʊ': 'O', 'iː': 'i', 'uː': 'u', 'ɑː': 'ɑ',
        'ɔː': 'ɔ', 'ɜː': 'ɜ', 'ɪə': 'ɪ ɹ', 'eə': 'ɛ ɹ', 'ʊə': 'ʊ ɹ', 'ɚ': 'ə ɹ', 'ɝ': 'ɜ ɹ', 'r': 'ɹ', 'g': 'ɡ', 'ɐ': 'ə',
        'ᵻ': 'ɪ', 'ɾ': 'T', 'x': 'k', 'ɬ': 'l', 'ɒ': 'ɑ', 'e': 'ɛ', 'o': 'O', 'a': 'ɑ', 'ʔ': '', 'ː': '', "'": 'ˈ', ',': 'ˌ'}
_VOWELS = set('aeiouæɑɒɔəɛɪʊʌɜɐᵻAIOWYɚɝ')
_TOKENS = None


def _tokens():
    """配音模型认的音素（Kokoro v1.0 的 tokens.txt）；读不到就不查"""
    global _TOKENS
    if _TOKENS is None:
        _TOKENS = set()
        try:
            import voice_config as VC
            p = os.path.join(os.environ.get('WORDFILM_MODELS', os.path.expanduser('~/wordfilm-models')), VC.EN_MODEL, 'tokens.txt')
            _TOKENS = {ln.split()[0] for ln in open(p, encoding='utf-8') if ln.split()}
        except Exception:
            pass
    return _TOKENS


def ipa_to_tokens(ipa, stress=True):
    """'dˈʌk' / 'pɹoʊ' / 'θ' / 'dʰ' → 'd ˈ ʌ k' / 'p ɹ ˈ O' / 'θ' / 'd ʰ'。stress=True：没写重音的，第一个元音前补 ˈ（单独念一个词缀要重读才听得清）"""
    s = re.sub(r'[\s./\[\]()]', '', str(ipa or '')).replace('ɡ', 'ɡ')
    out, i = [], 0
    while i < len(s):
        m = next((x for x in _MULTI if s.startswith(x, i)), None) or s[i]
        i += len(m)
        t = _MAP.get(m, m)
        if m == 'ɜː' and s.startswith('ɹ', i):
            t = 'ɜ'
        elif m == 'ɜː':
            t = 'ɜ ɹ'
        out += [x for x in t.split() if x]
    if stress and 'ˈ' not in out and 'ˌ' not in out:
        k = next((j for j, x in enumerate(out) if x in _VOWELS), None)
        if k is not None:
            out.insert(k, 'ˈ')
    ok = _tokens()
    if ok:
        out = [x for x in out if x in ok]
    return ' '.join(out)


# ---------------------------------------------------------------- espeak-ng：词典里没有的词，按拼读规则给出读音
_ES = None


def espeak_ipa(word, voice='en-us'):
    """espeak-ng 的国际音标（setup.sh 装 espeakng-loader）；没装返回 None"""
    global _ES
    if _ES is None:
        try:
            import espeakng_loader as L
            lib = ctypes.cdll.LoadLibrary(L.get_library_path())
            lib.espeak_Initialize(0x02, 0, L.get_data_path().encode(), 0)
            lib.espeak_SetVoiceByName.argtypes = [ctypes.c_char_p]
            lib.espeak_TextToPhonemes.restype = ctypes.c_char_p
            lib.espeak_TextToPhonemes.argtypes = [ctypes.POINTER(ctypes.c_char_p), ctypes.c_int, ctypes.c_int]
            _ES = {'lib': lib, 'voice': None}
        except Exception:
            _ES = False
    if not _ES:
        return None
    if _ES['voice'] != voice:
        _ES['lib'].espeak_SetVoiceByName(voice.encode())
        _ES['voice'] = voice
    p, out = ctypes.c_char_p(str(word).encode('utf-8')), []
    while p.value:
        r = _ES['lib'].espeak_TextToPhonemes(ctypes.byref(p), 1, 0x02)
        if r:
            out.append(r.decode('utf-8'))
    return ''.join(out).strip() or None


def have_espeak():
    return espeak_ipa('test') is not None


# ---------------------------------------------------------------- 把配音稿改成念得出的样子
SOUND = re.compile(r'/([^/\s，。、；：！？,;:]{1,16})/')
PREFIX = re.compile(r"(?<![A-Za-z'’/-])([A-Za-z]+)-(?![A-Za-z])")
SUFFIX = re.compile(r"(?<![A-Za-z'’/-])-([A-Za-z]+)(?![A-Za-z'’-])")
WORD = re.compile(r"(?<![A-Za-z'’-])([A-Za-z]{2,})(?![A-Za-z'’-])")


def _alpha(n):
    s, n = '', n + 1
    while n:
        n, r = divmod(n - 1, 26)
        s = 'abcdefghijklmnopqrstuvwxyz'[r] + s
    return s


def prepare(plan, have):
    """plan：配音稿；have：配音模型已经会念的词（英文词典 + plan 的 lexicon，小写）。
    返回 (rewrite, lex, notes)：rewrite = {原文: 合成用的文字}，lex = {音素词: 音素}，notes = 打印给人看的念法"""
    rewrite, lex, notes, sounds = {}, {}, [], {}
    have = {str(w).lower() for w in have}

    def sound(m):
        ipa = m.group(1)
        if ipa not in sounds:
            tok = ipa_to_tokens(ipa, stress=bool(re.search(r'[aeiouæɑɒɔəɛɪʊʌɜ]', ipa)))
            if not tok:
                return m.group(0)
            k = 'qzqf' + _alpha(len(sounds))
            sounds[ipa] = k
            lex[k] = tok
            notes.append('读音 /%s/ → %s（美式女声念这个音）' % (ipa, tok))
        return ' ' + sounds[ipa] + ' '

    def affix(m, kind):
        w = m.group(1).lower()
        k = ('qzqp' if kind == 'pre' else 'qzqs') + w
        if k not in lex:
            if k in have:                              # plan.json / prefs.json 的 lexicon 手写过这个词缀
                notes.append('%s %s → 配音稿词典' % ('前缀' if kind == 'pre' else '后缀', m.group(0)))
                return ' ' + k + ' '
            table = PREFIX_IPA if kind == 'pre' else SUFFIX_IPA
            if w in table:
                tok, src = ipa_to_tokens(table[w]), '词缀表'
            elif w in BASE and len(w) > 1:
                tok, src = BASE[w], '英文词典'
            else:
                e = espeak_ipa(w)
                tok, src = (ipa_to_tokens(e), 'espeak-ng') if e else ('', '')
            if not tok:
                return m.group(0)
            lex[k] = tok
            notes.append('%s %s → %s（%s）' % ('前缀' if kind == 'pre' else '后缀', m.group(0), tok, src))
        return ' ' + k + ' '

    def word(m):
        w = m.group(1)
        lw = w.lower()
        if lw.startswith('qz') or lw in have:
            return w
        k = 'qzqw' + lw
        if k not in lex:
            e = espeak_ipa(lw)
            tok = ipa_to_tokens(e) if e else ''
            if not tok:
                return w
            lex[k] = tok
            notes.append('%s → %s（英文词典里没有，espeak-ng 按拼读规则念）' % (w, tok))
        return k

    texts = []
    for spec in (plan.get('scenes') or {}).values():
        for t in ([spec.get('intro')] if spec.get('intro') else []) + list(spec.get('segs') or []):
            texts.append(str(t.get('t', '')) if isinstance(t, dict) else str(t))
    for t in texts:
        if t in rewrite:
            continue
        s = SOUND.sub(sound, t)
        s = PREFIX.sub(lambda m: affix(m, 'pre'), s)
        s = SUFFIX.sub(lambda m: affix(m, 'suf'), s)
        s = WORD.sub(word, s)
        s = re.sub(r'[ \t]+', ' ', s)
        s = re.sub(r' ?([，。、；：！？])', r'\1', s)
        s = re.sub(r'([，。、；：！？]) ', r'\1', s).strip()
        if s != t:
            rewrite[t] = s
    return rewrite, lex, notes


BASE = {}          # synth.py 填：英文词典（单词 → 音素），词缀表里没有的词缀先查它
