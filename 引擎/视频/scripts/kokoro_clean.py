#!/usr/bin/env python3
"""6.25（第六十二版）：念英文（af_heart）不再在开头多出一个 e / ai 的音。

用户：“现在的英语读音开都会带一个e，或者 ai 这样的声音，比如 speaker， loudspeaker。s前面有一个e的音，
l前面有个e的音……我希望不要有这样的音，单词发音要准确”。

查出来的原因（第六十一版的配音逐个测过）：
  1. 单独念一个词、一个音节块时，Kokoro 在开头自己多念出一个很短的元音——识别模型把 speaker 听成“A speaker”，
     loudspeaker 听成“A loudspeaker”，store 听成“I store / A store”。整句话开头也一样。
     原因是一段话一开头、前面没有别的音，模型会先“起一个音”。
  2. 读音拆分里只有辅音的块（speaker 的 s、loudspeaker 的 d、understand 的 d、throat 的 th、t）单独念，
     模型念不出一个光秃秃的辅音，念成了元音（s 念成“诶斯”）。

现在的做法（念英文的地方都走这里：单词、词根词缀、音节块、整句例句、听力题）：
  - 前面先垫一个词“okay,”（逗号让它和后面隔开一小段静音），整段一起合成；
  - 模型同时给出每个音素念了多长（durations），算出要念的词从第几秒开始，在逗号那一小段静音里下刀，
    只留后面要念的部分——开头不会再多出元音（垫的词在前面把“起音”吃掉了）；
  - 只有辅音的音节块：s、f、th、sh 这种擦音念成一段“嘶——”（两个 s 连着念，长一点听得清）；
    m、n、l、r 这种念成拖长的 /n/、/l/；p、t、k、b、d、g 这种爆破音念成“爆破 + 极短的一点尾音”，
    像老师单独示范辅音那样，不念成字母名（d 不念“迪”，s 不念“诶斯”）。

读音照旧查：配音稿的词典（plan.json 的 lexicon、readings.py 改好的音素词）> 模型自带的美式词典 > espeak-ng。
查不到的词、数字（很少见）退回原来的念法，日志会打印“提醒：…退回原来的念法”。
"""
import os, re
import numpy as np

SR = 24000
HOP = 600                 # Kokoro：一个时长单位 = 600 个采样点（25 毫秒）
LEAD = 0.075              # 实测：声音比时长算出来的位置早 0.06～0.095 秒
MODELS = os.environ.get('WORDFILM_MODELS', os.path.expanduser('~/wordfilm-models'))
CARRIER = 'okay ,'        # 垫在前面的词（逗号 = 一小段静音，好下刀）

_SESS = _TOK = _VOI = None
_LEX = {}
_LEX_FILES = ()

VOWELS = set('aeiouæɑɒɔəɛɪʊʌɜɐᵻAIOWYɚɝᵊQ')
FRIC = set('szfvθðʃʒh')
SON = set('mnŋlɹwjr')
STOP = set('pbtdkɡgʧʤ') | {'ʧ', 'ʤ'}
MARKS = set('ˈˌː')
PUNCT = {',': ',', '.': '.', '!': '!', '?': '?', ';': ';', ':': ':', '…': '…', '—': '—'}
ABBR = {'mr', 'mrs', 'ms', 'dr', 'st'}


def _dir(model):
    return os.path.join(MODELS, model) + '/'


def _tokens(model):
    global _TOK
    if _TOK is None:
        _TOK = {}
        for line in open(_dir(model) + 'tokens.txt', encoding='utf-8'):
            line = line.rstrip('\n')
            if not line.strip():
                continue
            sym, idx = line.rsplit(' ', 1)
            _TOK[sym if sym else ' '] = int(idx)
    return _TOK


def _providers():
    try:
        import voice_config as VC
        return VC.ort_providers('en')
    except Exception:          # noqa: BLE001
        return ['CPUExecutionProvider']


def _session(model):
    global _SESS, _VOI
    if _SESS is None:
        import onnxruntime as ort
        so = ort.SessionOptions()
        so.intra_op_num_threads = max(1, min(2, os.cpu_count() or 1))
        so.log_severity_level = 3
        _SESS = ort.InferenceSession(_dir(model) + 'model.onnx', so, providers=_providers())      # 6.36：设了 WORDFILM_EN_DEVICE=cuda 就用显卡（voice_config.ort_providers）
        n = np.fromfile(_dir(model) + 'voices.bin', dtype=np.float32)
        _VOI = n.reshape(-1, 510, 256)
    return _SESS


def _load_lex(files):
    """词典按顺序查，前面的优先（配音稿自己的词典在最前面）"""
    global _LEX, _LEX_FILES
    files = tuple(f for f in files if f and os.path.exists(f))
    if files == _LEX_FILES and _LEX:
        return _LEX
    lex = {}
    for f in files:
        for ln in open(f, encoding='utf-8'):
            k, _, v = ln.rstrip('\n').partition(' ')
            k = k.strip().lower()
            if k and v.strip() and k not in lex and '||' not in v:
                lex[k] = v.split()
    _LEX, _LEX_FILES = lex, files
    return lex


def _espeak(word):
    try:
        import readings as RD
        e = RD.espeak_ipa(word)
        return RD.ipa_to_tokens(e).split() if e else None
    except Exception:
        return None


def g2p(text, lex, tok):
    """一段英文 → Kokoro 的音素列表（词和词之间一个空格，标点照放）。查不到的词抛 KeyError"""
    t = str(text).replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    out = []
    for m in re.finditer(r"[A-Za-z][A-Za-z']*|[,.!?;:…—]|-", t):
        s = m.group(0)
        if s in PUNCT:
            if out and out[-1] == ' ':
                out.pop()
            if PUNCT[s] in tok and not (s == '.' and out and out[-1] == '§'):
                out.append(PUNCT[s])
            if out and out[-1] == '§':
                out.pop()
            continue
        if s == '-':
            continue
        w = s.lower().strip("'")
        ph = lex.get(w)
        if ph is None and w.endswith("'s"):
            ph = lex.get(w[:-2])
            ph = ph + ['z'] if ph else None
        if ph is None:
            ph = _espeak(w)
        if not ph:
            raise KeyError(w)
        if out and out[-1] not in (' ',):
            out.append(' ')
        out += [p for p in ph if p in tok]
        if w in ABBR and t[m.end():m.end() + 1] == '.':
            out.append('§')                     # Mr. 后面的点不是句号
    out = [p for p in out if p != '§']
    while out and out[0] == ' ':
        out.pop(0)
    while out and out[-1] == ' ':
        out.pop()
    return out


def _env(x, ms=5):
    k = max(1, int(ms / 1000 * SR))
    n = len(x) // k
    return np.sqrt(np.mean(x[:n * k].reshape(n, k) ** 2, axis=1)) if n else np.zeros(0)


def _run(seq, sid, speed, model):
    tok = _tokens(model)
    ids = [tok[p] for p in seq]
    s = _session(model)
    style = _VOI[int(sid), min(509, len(ids))][None, :]
    out = s.run(None, {'tokens': np.array([[0] + ids + [0]], dtype=np.int64), 'style': style,
                       'speed': np.array([float(speed)], dtype=np.float32)})
    return out[0].astype(np.float32), np.asarray(out[1]).reshape(-1)


def _cut_point(a, d, n_before):
    """要念的部分从第几个采样点开始：时长算出大概位置，再在它前面那段静音的末尾下刀"""
    est = int(np.sum(d[:1 + n_before])) * HOP / SR - LEAD
    e = _env(a, 5)
    if not len(e):
        return 0
    thr = e.max() * 0.025
    i_est = int(est / 0.005)
    lo, hi = max(0, i_est - 50), min(len(e) - 1, i_est + 6)
    quiet = [i for i in range(lo, hi + 1) if e[i] < thr]
    if quiet:
        j = quiet[-1]
        # 往后再确认：下刀以后 30 毫秒内要有声音起来（不是静音段中间）
        return int(max(0, (j - 1) * 0.005) * SR)
    return int(max(0, est - 0.02) * SR)


def _fade(x, a_ms=6, b_ms=12):
    x = x.copy()
    a, b = min(len(x) // 3, int(a_ms / 1000 * SR)), min(len(x) // 3, int(b_ms / 1000 * SR))
    if a > 1:
        x[:a] *= np.linspace(0, 1, a)
    if b > 1:
        x[-b:] *= np.linspace(1, 0, b)
    return x


def consonant_only(ph):
    core = [p for p in ph if p not in MARKS and p != ' ']
    return bool(core) and not any(p in VOWELS for p in core)


def speak(text, sid=3, speed=0.9, model='kokoro-multi-lang-v1_0', lex_files=()):
    """念一段英文，开头不带多出来的元音。返回 numpy 数组（24 kHz）；查不到读音返回 None（调用的地方退回原来的念法）"""
    tok = _tokens(model)
    lex = _load_lex(list(lex_files) + [_dir(model) + 'lexicon-us-en.txt'])
    try:
        ph = g2p(text, lex, tok)
    except KeyError:
        return None
    if not ph:
        return None
    car = g2p(CARRIER, lex, tok) + [' ']
    tail = None
    one = str(text).strip().rstrip('.,!?')
    if re.fullmatch(r'qz[a-z]+', one) and not any(p in ('ˈ', 'ˌ') for p in ph) and not consonant_only(ph):
        # 读音拆分的一块（音素词）没标重音：单独念时念清楚，按重读念（不然末尾的 /ə/ 念得很虚）
        k = next(i for i, p in enumerate(ph) if p in VOWELS)
        ph = ph[:k] + ['ˈ'] + ph[k:]
    if consonant_only(ph):
        core = [p for p in ph if p not in MARKS]
        last = core[-1]
        if last in STOP:                        # 爆破音：后面带一点点 /ə/，只留爆破和最开头一小段
            ph = core + ['ə']
            tail = 0.075
        elif all(p in ('s', 'ʃ', 'f') for p in core):   # 强的擦音：三个连着念，“嘶——”长一点、听得清
            ph = core + core + core
        elif all(p in FRIC for p in core):      # th、h 这种弱的擦音：念一个（连着念会冒出元音）
            ph = core
        else:                                   # m、n、l、r：拖长
            ph = core + ['ː']
    a, d = _run(car + ph, sid, speed, model)
    st = _cut_point(a, d, len(car))
    if tail is not None:
        t_schwa = int(np.sum(d[:1 + len(car) + len(ph) - 1])) * HOP / SR - LEAD
        end = int(min(len(a), (t_schwa + tail) * SR))
        x = _fade(a[st:max(st + int(0.05 * SR), end)], 4, 30)
    else:
        x = _fade(a[st:], 6, 12)
    return x
