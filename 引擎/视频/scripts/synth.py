#!/usr/bin/env python3
"""按配音稿（plan.json）合成配音，每一句都用语音识别听一遍，英文单词没被认出来的标出来。

用法：python3 synth.py <plan.json> <输出文件夹>
输出：每一句一个 wav（24 kHz），manifest.json（每一幕的每一句：文件、时长、文字、没听清的英文词 miss、用的声音 engine）。
模型放在 $WORDFILM_MODELS（默认 ~/wordfilm-models），由 setup.sh 下载。

5.3 起（第二十五版）——配音用你本人的声音：
  讲解句、例句：ZipVoice 声音克隆，照着参考录音（voice_config.py：$WORDFILM_VOICE → ~/wordfilm-voice → 技能自带 assets/voice）的嗓音念，中英混读。
  只念音节块的句子（qzca 这种音素词）：仍用 Kokoro 38 号（ZipVoice 念不了单独的半个音节：要么只出 0.04 秒，要么乱念）。
  句子里夹着的整词音素词（“连起来：qzcamera。”）ZipVoice 也认：plan 的 lexicon 换成国际音标写进它的词典。
  合成设置：4 步、guidance 3.0（ZipVoice 蒸馏模型的推荐值）。sherpa-onnx 默认 guidance 1.0，实测底噪、电流声明显（DNSMOS 总分 2.62 → 3.27）。
  参考录音先降噪（voice_prep.py 做好），合成后再清理一遍（clean_out）：轻度降噪、去 70 Hz 以下嗡声、7 kHz 以上降 4 dB、10.5 kHz 以上切掉。
  ZipVoice 每次念得不一样：没听清就重念，最多 4 遍；4 遍都不行退回 Kokoro 38 号再试（manifest 的 engine 写 kokoro-退回）。
  plan.json 写 "engine": "kokoro" 就整段用原来的 38 号女声。6.9 起：没下载全 ZipVoice、af_heart，没有参考录音时停下来说缺什么（不再自动用 38 号）。
  plan.json 的 "zvSpeed"：克隆声音的语速（默认 1.0）；voice、speed 只管 Kokoro（音节块）。

5.0 起：
  plan.json 的 "lexicon"：{"qzca": "k ˈ æ", "obscura": "ɒ b s k j ˈ ʊ ə ɹ ə"}——临时加进配音模型词典的词（音素用 Kokoro 的写法，空格隔开）。
    读音拆分念每一块用的“音素词”（qz 开头）就靠它：念出来正好是这一块的音（camera 的 me 念 /mə/，不会念成 /miː/）；
    词典里没有的生词（obscura）也可以这样加。
  一句可以写成 {"t": "qzca", "speed": 0.85}：这一句单独的语速。
  只有音素词的句子（念一块的音）：前后的空白剪掉，念起来一块接一块；不用语音识别检查（识别模型认不出半个词）。
"""
import hashlib, json, os, re, shutil, sys
import numpy as np
import soundfile as sf
import sherpa_onnx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voice_config as VC  # noqa: E402
import readings as RD  # noqa: E402      6.17：英文的四种念法（字母 / 读音 / 词缀 / 词根），见 readings.py

MODELS = os.environ.get('WORDFILM_MODELS', os.path.expanduser('~/wordfilm-models'))
EXTRA_LEX = []          # 配音稿自己的词典（plan.json 的 lexicon），在模型建好之前写好
KOKORO = os.path.join(MODELS, 'kokoro-multi-lang-v1_1') + '/'
SENSE = os.path.join(MODELS, 'sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17') + '/'
SR = 24000
_tts = _asr = None


def tts():
    global _tts
    if _tts is None:
        M = KOKORO
        cfg = sherpa_onnx.OfflineTtsConfig(
            model=sherpa_onnx.OfflineTtsModelConfig(
                kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
                    model=M + 'model.onnx', voices=M + 'voices.bin', tokens=M + 'tokens.txt',
                    data_dir=M + 'espeak-ng-data', dict_dir=M + 'dict',
                    lexicon=','.join(EXTRA_LEX + [x for x in (M + 'lexicon-extra.txt',) if os.path.exists(x)]
                                      + [M + 'lexicon-us-en.txt', M + 'lexicon-zh.txt'])),
                num_threads=2, provider=VC.provider('en')),
            rule_fsts=M + 'phone-zh.fst,' + M + 'date-zh.fst,' + M + 'number-zh.fst',
            max_num_sentences=1)
        _tts = sherpa_onnx.OfflineTts(cfg)
    return _tts


_tts_en = None


def tts_en():
    """5.7 起：念英文单词、例句的声音（Kokoro v1.0 的 af_heart）。没下载就退回 v1.1（38 号），日志会提醒"""
    global _tts_en
    if _tts_en is None:
        M = os.path.join(MODELS, VC.EN_MODEL) + '/'
        if not os.path.exists(M + 'model.onnx'):
            print('提醒：没找到 %s（setup.sh 会下载），英文先用 38 号念' % VC.EN_MODEL)
            _tts_en = False
            return None
        lex = M + ('lexicon-gb-en.txt' if VC.EN_ACCENT == 'gb' else 'lexicon-us-en.txt')
        cfg = sherpa_onnx.OfflineTtsConfig(
            model=sherpa_onnx.OfflineTtsModelConfig(
                kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
                    model=M + 'model.onnx', voices=M + 'voices.bin', tokens=M + 'tokens.txt',
                    data_dir=M + 'espeak-ng-data', dict_dir=M + 'dict',
                    lexicon=','.join(EXTRA_LEX + [lex, M + 'lexicon-us-en.txt', M + 'lexicon-zh.txt'])),
                num_threads=VC.threads(), provider=VC.provider('en')),
            max_num_sentences=1)
        _tts_en = sherpa_onnx.OfflineTts(cfg)
    return _tts_en or None


def asr():
    global _asr
    if _asr is None:
        _asr = sherpa_onnx.OfflineRecognizer.from_sense_voice(model=SENSE + 'model.int8.onnx', tokens=SENSE + 'tokens.txt', use_itn=True, num_threads=2, provider=VC.provider('asr'))
    return _asr


def gen(text, sid, speed):
    a = tts().generate(text, sid=sid, speed=speed)
    return np.array(a.samples, dtype=np.float32)


# ---------- 5.3 起：声音克隆（ZipVoice） ----------
EXTRA_ZLEX = []         # 配音稿词典的国际音标版（ZipVoice 用），在模型建好之前写好
_zv = _ref = None
# Kokoro 词典里的几个缩写记号（misaki）换成 ZipVoice 认的国际音标
MISAKI = {'A': 'eɪ', 'I': 'aɪ', 'O': 'oʊ', 'W': 'aʊ', 'Y': 'ɔɪ', 'Q': 'əʊ', 'ʤ': 'dʒ', 'ʧ': 'tʃ', 'ᵊ': 'ə', 'ᵻ': 'ɪ'}


def to_ipa(ph):
    return ' '.join(MISAKI.get(p, p) for p in str(ph).split())


def zipvoice():
    global _zv
    if _zv is None:
        Z = VC.ZIPVOICE_DIR
        cfg = sherpa_onnx.OfflineTtsConfig(
            model=sherpa_onnx.OfflineTtsModelConfig(
                zipvoice=sherpa_onnx.OfflineTtsZipvoiceModelConfig(
                    tokens=Z + 'tokens.txt', encoder=Z + VC.ZV_ENCODER, decoder=Z + VC.ZV_DECODER, vocoder=VC.VOCODER,
                    data_dir=Z + 'espeak-ng-data', lexicon=','.join(EXTRA_ZLEX + [Z + 'lexicon.txt', VC.EN_LEXICON]),
                    guidance_scale=VC.GUIDANCE),
                num_threads=VC.threads(), provider=VC.provider('zv')),
            max_num_sentences=1)
        _zv = sherpa_onnx.OfflineTts(cfg)
    return _zv


def ref_voice(role=None):
    """(参考录音样本, 采样率, 录音里说的话)：role 是 translate / question，没有那一段就用讲解的"""
    global _ref
    if _ref is None:
        _ref = {}
    wav, text, noise = VC.ref(role)
    if wav not in _ref:
        x, sr = sf.read(wav, dtype='float32')
        x = x.mean(1) if x.ndim > 1 else x
        if noise and VC.REF_DENOISE:            # 6.44：参考录音里的底噪会被一起学去：先用 noise.wav 降一遍（实测句中停顿的底噪低 9 dB）
            try:
                from voice_clean import denoise
                nz, nsr = sf.read(noise, dtype='float32')
                nz = nz.mean(1) if nz.ndim > 1 else nz
                if nsr == sr:
                    x = denoise(x, sr, nz, VC.REF_DENOISE, stationary=True)
            except Exception as e:
                print('提醒：参考录音降噪没做（%s）' % e)
        _ref[wav] = (x, sr, text)
    return _ref[wav]


def clean_out(x):
    """合成出来的句子再清理一遍：轻度降噪（非平稳）、去低频嗡声、压 7 kHz 以上的刺耳高频、切掉 10.5 kHz 以上的假音"""
    from voice_clean import denoise, high_shelf, lpf, gate
    try:
        x = denoise(x, SR, None, VC.OUT_DENOISE, stationary=False)     # 6.44：0.5 → 0.75
    except Exception as e:                      # 没装 noisereduce 也能出声音，只是少一道降噪
        print('提醒：降噪没做（%s）' % e)
    return gate(lpf(high_shelf(x, SR, 7000.0, -4.0), SR, 10500), SR)      # 6.44：字和字之间的底噪压下去


CACHE = None            # synth() 设成 <输出文件夹>/cache：念好的中文按（文字、参考录音、设置）存下来，稿子改一句只重念那一句


def _ckey(text, speed, role):
    import hashlib
    wav, ptext, _ = VC.ref(role)
    h = hashlib.md5()
    h.update(open(wav, 'rb').read())
    h.update(('|'.join(map(str, (ptext, text, float(speed or VC.SPEED), VC.STEPS, VC.GUIDANCE, VC.ZV_DECODER, VC.CLONE_VERSION)))).encode('utf-8'))
    return h.hexdigest()[:16]


def cache_put(key, x):
    if CACHE and key:
        os.makedirs(CACHE, exist_ok=True)
        p = os.path.join(CACHE, key + '.wav')
        tmp = '%s.%d.tmp' % (p, os.getpid())          # 6.35：几个进程一起念时，先写临时文件再换名，别人读不到写了一半的
        sf.write(tmp, x.astype(np.float32), SR, format='WAV')
        os.replace(tmp, p)


def gen_voice(text, speed=None, role=None, fresh=True, keys=None):
    """用参考录音的嗓音念一句中文（24 kHz），已经清理过。fresh=False 时先看缓存；keys 收集（缓存名, 声音）"""
    key = _ckey(text, speed, role) if CACHE else None
    p = os.path.join(CACHE, key + '.wav') if key else None
    if not fresh and p and os.path.exists(p):
        x = sf.read(p, dtype='float32')[0]
    else:
        x0, sr0, ptext = ref_voice(role)
        a = zipvoice().generate(text, ptext, x0.tolist(), sr0, speed=float(speed or VC.SPEED), num_steps=VC.STEPS)
        x = np.array(a.samples, dtype=np.float32)
        if a.sample_rate != SR:
            from math import gcd
            from scipy.signal import resample_poly
            g = gcd(a.sample_rate, SR)
            x = resample_poly(x, SR // g, a.sample_rate // g).astype(np.float32)
        x = clean_out(x)
    if keys is not None:
        keys.append((key, x))
    return x


# ---------- 5.5 起：念英文的地方换成念得准的英文声音 ----------
EN_RUN = re.compile(r"[A-Za-z][A-Za-z'’\-]*(?:[ \t]+[A-Za-z][A-Za-z'’\-]*)*")
# 6.17：单独的字母（e、u、加 s、c 和 s 合写成 x、答案是 D、词尾 e r e）用你本人的声音念字母名，夹在中文里，不换讲解员
# （用户：“单个的字母就不要换讲解员了，就用我自己的音色就可以了”）。实测声音克隆念得清：英语加不发音的 e、答案是 D 都听得出来
LETTERS_ONLY = re.compile(r'^[A-Za-z](?:[ \t]+[A-Za-z])*$')


def en_runs(text):
    """要用英文声音念的几段（单独的字母不算）"""
    return [m.group(0) for m in EN_RUN.finditer(text) if not LETTERS_ONLY.match(m.group(0))]
CJK = re.compile(r'[\u3400-\u9fff]')
PUNCT = '，。：；、！？,.:;!?'


def split_mixed(text):
    """一句拆成中文段、英文段：'这种屋子叫 camera obscura，就是黑屋子' ->
    [('zh', '这种屋子叫'), ('en', 'camera obscura'), ('zh', '，就是黑屋子')]"""
    out, i = [], 0
    for m in EN_RUN.finditer(text):
        if LETTERS_ONLY.match(m.group(0)):          # 6.17：单独的字母留在中文段里，克隆的声音念
            continue
        if m.start() > i:
            out.append(('zh', text[i:m.start()]))
        out.append(('en', m.group(0)))
        i = m.end()
    if i < len(text):
        out.append(('zh', text[i:]))
    return [(k, t) for k, t in out if t.strip()]


def gen_en(text, sid=None, speed=None):
    """英文（单词、词根、音素词、整句）用念得准的英文声音；单独的词剪掉前后的空白"""
    sid = VC.EN_SID if sid is None else int(sid)
    word = len(text.split()) <= 3 and not re.search(r'[.!?]\s*$', text)
    sp = float(speed or (VC.EN_WORD_SPEED if word else VC.EN_SENT_SPEED))
    # 6.25：先垫一个词“okay,”一起合成、按音素时长在逗号的静音里下刀——开头不再多出 e / ai 的音（kokoro_clean.py）
    if VC.EN_CLEAN and os.path.exists(os.path.join(MODELS, VC.EN_MODEL, 'model.onnx')):
        try:
            import kokoro_clean as KC
            y = KC.speak(text, sid, sp, VC.EN_MODEL, EXTRA_LEX + ([os.path.join(MODELS, VC.EN_MODEL, 'lexicon-gb-en.txt')] if VC.EN_ACCENT == 'gb' else []))
        except Exception as e:                       # noqa: BLE001
            print('  提醒：英文“%s”用干净念法出错（%s），退回原来的念法' % (text, e))
            y = None
        if y is not None and len(y) >= int(0.05 * SR):
            y = trim_end(y)
            from voice_clean import high_shelf, lpf
            return lpf(high_shelf(y, SR, 7000.0, -4.0), SR, 10500)
        print('  提醒：英文“%s”查不到读音，退回原来的念法（开头可能多一个音）' % text)
    t = tts_en()
    x = np.array(t.generate(text, sid=sid, speed=sp).samples, dtype=np.float32) if t else gen(text, 38, sp)
    if len(x) < int(0.05 * SR) and t:
        # 6.10：词典里没有的词（拉丁语词尾 arius 这种）Kokoro 会整个跳过、出空的声音，以前在这里报错停下。
        # 改成一个字母一个字母念（和三个字母以内的词缀同一个念法），再不行就留 0.3 秒空白
        spelled = re.sub(r"[A-Za-z]{2,}", lambda m: ' '.join(m.group(0)), text)
        x = np.array(t.generate(spelled, sid=sid, speed=sp).samples, dtype=np.float32)
        print('  提醒：英文“%s”词典里没有，改成一个个字母念（%s）——6.17 起应该已经换成 espeak-ng 的读音了，看看 espeak-ng 装好没有（bash setup.sh）' % (text, spelled))
        if len(x) < int(0.05 * SR):
            return np.zeros(int(0.3 * SR), np.float32)
    x = trim(x) if word else x
    from voice_clean import high_shelf, lpf
    return lpf(high_shelf(x, SR, 7000.0, -4.0), SR, 10500)      # 和中文一样压一点刺耳的高频（不降噪：Kokoro 本来就干净，降了反而毛）


SYL_TPL = ('{k}', '{k}.', '{k}!', '{k}?', '{k}…', '…{k}.')


def syllable38(text, sid, speed):
    """5.9 起：读音拆分的音节块（qzca）。单独念一个音节，模型没有上下文，音高常常乱跳、元音拖长，听着怪。
    同一个声音（38 号）、同样的读音，换几种念法（后面加句号、感叹号、问号、省略号，语速快慢一点）各念一遍，
    挑音高最稳、最像老师单独念一个音节的那一遍（voice_clean.syllable_cost）。不改声音本身，所以没有加工的杂音。
    返回 (声音, 用的念法)"""
    from voice_clean import syllable_cost
    k = text.strip().rstrip('。，、！!.,')
    if not re.fullmatch(r'qz[a-z]+', k):
        return trim(gen(text, sid, speed)), 'plain'
    best = None
    for t in SYL_TPL:
        for sp in (speed, speed * 0.9, speed * 1.1):
            x = gen(t.format(k=k), sid, sp)
            if len(x) < int(0.1 * SR):
                continue
            x = trim(x)
            c = syllable_cost(x, SR)
            if best is None or c < best[0]:
                best = (c, x, '%s@%.2f' % (t.format(k=''), sp))
    return (best[1], best[2]) if best else (trim(gen(text, sid, speed)), 'plain')


def syllable(text, sid=38, speed=0.95, en_sid=None):
    """读音拆分单念的音节块（qzca 这种音素词）。5.10 起默认用念英文的声音 af_heart（VC.SYL_VOICE = 'en'）；
    SYL_VOICE = 38 回到原来的 38 号单念一遍（SYL_PICK / SYL_FLATTEN 是 5.9 试过的 38 号优化，默认不开）"""
    from voice_clean import high_shelf, lpf, flatten_syllable
    k = text.strip().rstrip('。，、！!.,')
    if VC.SYL_VOICE == 'en':
        return gen_en(k, en_sid, VC.SYL_SPEED)
    x = syllable38(text, int(VC.SYL_VOICE), speed)[0] if VC.SYL_PICK else trim(gen(text, int(VC.SYL_VOICE), speed))
    if VC.SYL_FLATTEN:
        x = flatten_syllable(x, SR)
    return lpf(high_shelf(x, SR, 7000.0, -4.0), SR, 10500)


def gen_en_checked(text, sid=None):
    """5.6 起：英文段先单独听一遍——念得准不准由识别模型判断，没认出来就换个语速再念（0.88 → 0.95 → 0.8），都不行用第一种。
    返回 (声音, 没认出来的词)。音素词（qz 开头）识别不了，不查"""
    words = [w for w in re.findall(r"[A-Za-z][A-Za-z'’-]*", text) if len(w) >= 3 and not w.lower().startswith('qz')]
    first, sp = None, (None, 0.95, 0.8)
    for s in sp:
        x = gen_en(text, sid, s)
        if not words:
            return x, []
        pad = np.zeros(int(0.3 * SR), np.float32)
        heard = transcribe_array(np.concatenate([pad, x, pad]), SR)
        bad = [w for w in words if not heard_ok(re.sub(r"['’-]", '', w.lower()), heard)]
        if first is None:
            first = (x, bad)
        if not bad:
            return x, []
    return first


def _edge_trim(x, keep=0.04):
    """剪掉一段中文前后的空白（只剪真正安静的地方，留一点气口）"""
    k = int(0.01 * SR)
    if len(x) < 4 * k:
        return x
    fr = np.array([np.abs(x[i:i + k]).max() for i in range(0, len(x) - k, k)])
    on = np.where(fr > fr.max() * 0.04)[0]
    if not len(on):
        return x
    a, b = max(0, on[0] * k - int(keep * SR)), min(len(x), (on[-1] + 1) * k + int(keep * SR))
    return x[a:b]


def _level(x):
    v = x[np.abs(x) > np.abs(x).max() * 0.05] if len(x) else x
    return x / (np.sqrt(np.mean(v ** 2)) + 1e-9) * 0.1 if len(v) else x


def _fade(x, ms=10):
    k = min(len(x) // 2, int(ms / 1000 * SR))
    if k > 1:
        x = x.copy()
        x[:k] *= np.linspace(0, 1, k)
        x[-k:] *= np.linspace(1, 0, k)
    return x


def compose(text, role=None, zv_speed=None, en_sid=None, cache=None, fresh=True, keys=None):
    """中英混着的一句：中文用克隆的声音，英文用英文声音，按标点留停顿接起来。cache 存英文段（每次都一样，不用重念）"""
    parts, pieces = split_mixed(text), []
    cache = {} if cache is None else cache
    for n, (kind, t) in enumerate(parts):
        if kind == 'en':
            if t not in cache:
                x, bad = gen_en_checked(t, en_sid)
                cache[t] = (_level(x), bad)
                if bad:
                    print('  提醒：英文“%s”单独念时识别模型没认出 %s（单独的词常这样；发音按词典，没问题就不用管）' % (t, '、'.join(bad)))
            pieces.append(('en', t, cache[t][0]))
            continue
        say_t = t.strip().lstrip(PUNCT).strip()
        if not CJK.search(say_t):
            pieces.append(('zh', t, np.zeros(0, np.float32)))          # 只有标点：只算停顿
            continue
        if n + 1 < len(parts) and say_t[-1] not in PUNCT:
            say_t += '，'                                              # 后面接英文：念成没说完的语气
        pieces.append(('zh', t, _level(_edge_trim(gen_voice(say_t, zv_speed, role, fresh, keys)))))
    out, last, pend = [], '', ''
    for n, (kind, t, x) in enumerate(pieces):
        if not len(x):                                 # 只有标点的一段：算进下一处停顿，不另停一次（以前一个逗号停两遍）
            pend += t
            continue
        if out:
            # 6.32：交界处按标点分长短（VC.PAUSE_OF）：顿号最短，逗号、冒号、分号、省略号、句号依次长；只有空格的最短
            out.append(np.zeros(int(pause_for(last.rstrip()[-1:] + pend + t.lstrip()[:1]) * SR), np.float32))
        out.append(_fade(x.astype(np.float32)))        # 5.6 起每一段两头淡入淡出，接口不“咔哒”
        last, pend = t, ''
    return np.concatenate(out) if out else np.zeros(int(0.2 * SR), np.float32)


def pause_for(b):
    """交界处的几个字符 → 停多久：取里面最长的那个标点；没有标点（中英之间只有空格）停 VC.PAUSE_TIGHT"""
    ps = [VC.PAUSE_OF[ch] for ch in str(b) if ch in VC.PAUSE_OF]
    return max(ps) if ps else VC.PAUSE_TIGHT


# ---------------------------------------------------------------- 6.32（第七十六版）：停顿、一个声音念
LONG_P = '。！？；…!?;：'      # 6.33：冒号也切开（后面停 PAUSE_OF['：']）；英文的 ':' 只在后面是空格时切（9:15 不切）


def norm_text(t):
    """省略号统一成一个“…”；换行没有标点就接着念（汉字和汉字之间不留空，挨着英文的留一个空格）"""
    t = re.sub(r'\.{3,}', '…', str(t))
    t = re.sub(r'…+', '…', t)
    t = re.sub(r'(?<=[\u3400-\u9fff])[ \t]*\n[ \t]*(?=[\u3400-\u9fff])', '', t)
    t = re.sub(r'[ \t]*\n[ \t]*', ' ', t)
    return t.strip()


NUM_CIRC = '①②③④⑤⑥⑦⑧⑨⑩'
NUM_SAY = ['第一', '第二', '第三', '第四', '第五', '第六', '第七', '第八', '第九', '第十']


def sentences(t):
    """按句末标点（。！？；…）和冒号切开：[(这一句, 后面停多久)]。只有标点的并到前一句；最后一句后面不停（句子和句子之间 render.py 管）。
    6.33：①②③ 是新的一段——前面停 PAUSE_OF['¶']（比句号长），念成“第一，”“第二，”"""
    out, cur = [], ''

    def flush(pause):
        nonlocal cur
        if re.search(r'[A-Za-z0-9\u3400-\u9fff]', cur):
            out.append([cur.strip(), pause])
        else:
            if out:
                out[-1][0] += cur.strip()
                out[-1][1] = max(out[-1][1], pause)
        cur = ''
    for k, ch in enumerate(t):
        if ch in NUM_CIRC:
            flush(VC.PAUSE_OF.get('¶', 0.85))
            if out:
                out[-1][1] = max(out[-1][1], VC.PAUSE_OF.get('¶', 0.85))
            cur = NUM_SAY[NUM_CIRC.index(ch)] + '，'
            continue
        cur += ch
        if ch == ':' and not (k + 1 < len(t) and t[k + 1] in ' \t'):
            continue                                   # 9:15、http: 这种不切
        if ch in LONG_P:
            flush(VC.PAUSE_OF.get(ch, 0.0))
    flush(0.0)
    res = [(x, pz) for x, pz in out if x]
    if res:
        res[-1] = (res[-1][0], 0.0)
    return res


def clone_text(s):
    """6.33：给你本人的声音念的字：词缀的连字符去掉（pro- → pro，-er → er），英文句末的中文句号换成英文句号"""
    s = re.sub(r'(?<![A-Za-z])-(?=[A-Za-z])', '', str(s))
    s = re.sub(r'(?<=[A-Za-z])-(?![A-Za-z])', '', s)
    return s


def by_sentence(text, fn):
    """一句一句念（fn 念一句），中间按句末标点停：句号、问号、叹号 0.5 秒，分号、省略号 0.42 秒"""
    parts = []
    for s, pause in sentences(text):
        x = fn(s)
        if x is None or not len(x):
            continue
        parts.append(_fade(_edge_trim(np.asarray(x, dtype=np.float32))))
        if pause:
            parts.append(np.zeros(int(pause * SR), np.float32))
    return np.concatenate(parts) if parts else np.zeros(int(0.2 * SR), np.float32)


def lang_runs(text):
    """一句里中文段、英文段的先后（单独的字母算中文——你本人的声音念；只有标点的不算）：[['zh', '…'], ['en', '…'], …]"""
    runs = []
    for kind, t in split_mixed(text):
        if kind == 'zh' and not CJK.search(t) and not re.search(r'[A-Za-z0-9]', t):
            continue
        if runs and runs[-1][0] == kind:
            runs[-1][1] += t
        else:
            runs.append([kind, t])
    return runs


def rapid(text, scene=''):
    """中英切换很快的一句，整句一个声音念：考点那几行；英文后面不加标点、空一格就接中文（protect the environment 保护环境）；
    来回切了三次以上、夹在两段英文中间的中文不超过 VC.SHORT_ZH 个字"""
    if not getattr(VC, 'ONE_VOICE', False):
        return False
    runs = lang_runs(text)
    if len(runs) < 2:
        return False
    if str(scene).startswith('kaodian'):
        return True
    # 6.33（第七十七版）：讲词缀、词根的那几幕（pro- 后面跟着一大段中文讲解），整句用你本人的声音念，不为一个 pro- 换成美式女声
    # （用户：“像这个 pro-前缀和后面有大量的中文讲解，那么这个前缀就用我自己的音色来读，不要用英文音色来读，要不然学生也反应不过来”）。
    # 讲读音的句子（/p/、/f/ 这种要念音的，改写成了 qzqf 音素词）不算：克隆的声音念不出单独的音
    if re.match(r'(part|fengong|xingtai|variant|related|rule)\d*$', str(scene)) and not re.search(r'qzqf|/[^/\s]{1,8}/', text) \
            and len(CJK.findall(text)) >= 8:
        return True
    parts = split_mixed(text)
    for a, b in zip(parts, parts[1:]):
        if a[0] == 'en' and b[0] == 'zh' and re.match(r'^[ \t]*[\u3400-\u9fff]', b[1]):
            return True
    if len(runs) >= 4:
        mids = [r for i, r in enumerate(runs) if 0 < i < len(runs) - 1 and r[0] == 'zh']
        if any(len(CJK.findall(r[1])) <= VC.SHORT_ZH for r in mids):
            return True
    return False


def _cut_after_lead(y):
    """垫在前面的“okay,”后面那段静音的结尾（10 毫秒一帧，从 0.15 秒起找连续 60 毫秒以上的静音）；找不到返回 0"""
    k = int(0.01 * SR)
    if len(y) < 20 * k:
        return 0
    fr = np.array([np.abs(y[i:i + k]).max() for i in range(0, len(y) - k, k)])
    thr, run = fr.max() * 0.03, 0
    for i in range(15, min(len(fr), 120)):
        if fr[i] < thr:
            run += 1
        else:
            if run >= 6:
                return max(0, i - 2) * k
            run = 0
    return 0


def one_voice(s, zs, role, fresh, keys, en_sid):
    """6.33：“一个人念”的一小句。整句英文（三个词以上、没有中文：考点里另起一行的例句 The birds are protected by law.）前面停得长，照旧美式女声念；别的你本人的声音念"""
    if not CJK.search(s) and len(re.findall(r"[A-Za-z]+", s)) >= 3:
        return gen_en(re.sub(r'[。；，：]+$', '.', s.strip()), en_sid)
    return gen_voice(clone_text(s), zs, role, fresh=fresh, keys=keys)


def gen_mix1(text, sid=None, speed=None):
    """切换很快的一句：英文、中文都用念英文的声音（af_heart，Kokoro 多语种模型带中文词典）念；前面垫“okay,”再剪掉（开头不多出音）"""
    sid = VC.EN_SID if sid is None else int(sid)
    sp = float(speed or VC.MIX_SPEED)
    t = tts_en()
    if t is None:
        return gen(text, 38, sp)
    y = np.array(t.generate('okay, ' + text, sid=sid, speed=sp).samples, dtype=np.float32)
    cut = _cut_after_lead(y)
    x = y[cut:] if cut else np.array(t.generate(text, sid=sid, speed=sp).samples, dtype=np.float32)
    from voice_clean import high_shelf, lpf
    return lpf(high_shelf(x, SR, 7000.0, -4.0), SR, 10500)


def say(text, plan=None, scene=''):
    """按配音稿的设置念一句（saytest.py、voice_prep.py 用），和正式配音走同一条路"""
    plan = plan or {}
    en_sid = plan.get('enVoice', VC.EN_SID)
    if PHON_ONLY.match(text):
        return syllable(text, int(plan.get('voice', 38)), float(plan.get('speed', 0.95)), en_sid)
    if VC.engine(plan) == 'zipvoice' and not CJK.search(text):
        return gen_en(text, en_sid)
    if VC.engine(plan) == 'zipvoice':
        return compose(text, VC.role_of(scene, text), plan.get('zvSpeed'), en_sid)
    return gen(text, int(plan.get('voice', 38)), float(plan.get('speed', 0.95)))


def transcribe_array(x, sr):
    r = asr()
    s = r.create_stream()
    s.accept_waveform(sr, x)
    r.decode_stream(s)
    return s.result.text


def lev(a, b):
    d = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        p, d[0] = d[0], i
        for j, cb in enumerate(b, 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (ca != cb))
    return d[len(b)]


_ONES = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
_TENS = {2: 'twenty', 3: 'thirty', 4: 'forty', 5: 'fifty', 6: 'sixty', 7: 'seventy', 8: 'eighty', 9: 'ninety'}
_ORD = {'one': 'first', 'two': 'second', 'three': 'third', 'five': 'fifth', 'eight': 'eighth', 'nine': 'ninth', 'twelve': 'twelfth'}


def _say_int(n):
    """6.42：整数念成英文（到十亿以内）：5000 → five thousand，2024 → two thousand twenty four"""
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ('' if n % 10 == 0 else ' ' + _ONES[n % 10])
    if n < 1000:
        return _ONES[n // 100] + ' hundred' + ('' if n % 100 == 0 else ' ' + _say_int(n % 100))
    for k, name in ((10 ** 9, 'billion'), (10 ** 6, 'million'), (1000, 'thousand')):
        if n >= k:
            return _say_int(n // k) + ' ' + name + ('' if n % k == 0 else ' ' + _say_int(n % k))
    return str(n)


def _ordinal(words):
    head, _, last = words.rpartition(' ')
    last = _ORD.get(last) or (last[:-1] + 'ieth' if last.endswith('y') else last + 'th')
    return (head + ' ' + last).strip()


def _num_words(m):
    """识别结果里的一串数字 → 英文：5,000、3rd、50%、$5、3.5 都换"""
    cur, num, dec, suf, pct = m.group(1), m.group(2).replace(',', ''), m.group(3), (m.group(4) or '').lower(), m.group(5)
    try:
        n = int(num)
    except ValueError:
        return m.group(0)
    if n >= 10 ** 12:
        return m.group(0)
    w = _say_int(n)
    if suf in ('st', 'nd', 'rd', 'th') and not dec:
        w = _ordinal(w)
    if dec:
        w += ' point ' + ' '.join(_ONES[int(c)] for c in dec[1:])
    if pct:
        w += ' percent'
    if cur:
        w += ' dollars' if n != 1 else ' dollar'
    return ' ' + w + ' '


_NUM_RE = re.compile(r'(\$)?(\d{1,3}(?:,\d{3})+|\d+)(\.\d+)?(st|nd|rd|th)?(%)?', re.I)


def spell_numbers(heard):
    return _NUM_RE.sub(_num_words, heard)

def heard_ok(w, heard):
    """识别结果里有这个词就算听清：同音的拼法（tailor / taylor）、差一两个字母也算。
    5.1 起：识别模型把念出来的数字写成阿拉伯数字（“three and four is twelve”→“3 and 4 is 12”），先换回英文再比。
    6.42 起：大数、带逗号的数（five thousand → 5,000）、3rd、50%、$5、3.5 也换回英文（以前只换一两位的数，publisher 的例句
    “printed five thousand copies” 被算成 thousand 没听清，卡在配音）"""
    heard = spell_numbers(heard)
    flat = heard.lower().replace(' ', '')
    if w in flat:
        return True
    for t in re.findall(r'[a-z]+', heard.lower()):
        if t[:1] == w[:1] and lev(t, w) <= (1 if len(w) <= 6 else 2):
            return True
    return False


def check(text, heard, word='', known=()):
    """返回 (miss, warn)：
    miss —— 五个字母以上的单词没听清（学生要学的词，必须改）；
    warn —— 短词、一个个念的字母没听清（多半是识别模型听不准短的英文，画面上有字，可以不管）
    音素词（qz 开头）：念一块的不查；整词的（qzcamera）按 camera 查"""
    miss, warn = [], []
    # 6.43：单独念的一个英文词（精简版同义词辨析只念单词）：识别模型听单个词常听岔，没听清只提醒、不卡（同一个词在别的句子里照样查）
    single = re.fullmatch(r"\s*[A-Za-z][A-Za-z'’-]*\s*[.!?。！？]?\s*", text or '') is not None
    for w in re.findall(r"[A-Za-z][A-Za-z'’-]*", text):
        k = re.sub(r"['’]s$", '', w.lower()).replace('-', '')
        if k.startswith('qz'):
            if not word or k[2:] != re.sub(r'[^a-z]', '', word.lower()):
                continue
            k = k[2:]
        elif k in known:                 # 配音稿词典里手加读音的生词（obscura）：识别模型多半不认识，不算没听清
            continue
        if len(k) < 3 or heard_ok(k, heard):
            continue
        (miss if len(k) >= 5 and not single else warn).append(k)
    for m in re.findall(r'\b(?:[a-z] ){1,5}[a-z]\b', text):
        k = m.replace(' ', '')
        if k[:1] not in heard.lower():
            warn.append(k)
    return miss, warn


def zh_mismatch(text, heard):
    """中文念糊了（“拆开”被念成 Checkive 这种）：原句的汉字一半以上没出现在识别结果里"""
    cs = {c for c in text if '\u3400' <= c <= '\u9fff'}
    return len(cs) >= 2 and sum(1 for c in cs if c in heard) / len(cs) < 0.5


def zh_err(text, heard):
    """5.5 起：中文念错了几成——原句和听写都换成不带声调的拼音再比（“暗箱”听成“暗香”不算错，“我”念成“不”算错）。
    没装 pypinyin 就不查（返回 0）"""
    try:
        from pypinyin import lazy_pinyin
    except ImportError:
        return 0.0
    heard = ''.join('零一二三四五六七八九'[int(c)] if c.isdigit() else c for c in heard)
    a = lazy_pinyin(''.join(re.findall(r'[\u4e00-\u9fff]', text)))
    b = lazy_pinyin(''.join(re.findall(r'[\u4e00-\u9fff]', heard)))
    return lev(a, b) / len(a) if a else 0.0


ZH_OK = 0.08          # 拼音错一成以内算念对（识别模型偶尔听错一个字）


PHON_ONLY = re.compile(r'^\s*(?:qz[a-z]+[。，、！!.,\s]*)+$')


def trim_end(x, keep=0.06):
    """6.25：只剪结尾的空白（干净念法的开头已经切在声音起来的地方，不再动）"""
    k = int(0.005 * SR)
    if len(x) < 4 * k:
        return x
    fr = np.array([np.abs(x[i:i + k]).max() for i in range(0, len(x) - k, k)])
    if fr.max() <= 0:
        return x
    b = (np.where(fr > fr.max() * 0.05)[0][-1] + 1) * k
    return x[:min(len(x), b + int(keep * SR * 1.5))]


def trim(x, keep=0.06):
    """剪掉前后的空白（念一块音节的句子），两头各留一点。单独念一个音节时，前面常有半秒很轻的气声（识别会听成 in），
    按 5 毫秒一格的包络找：开头从超过峰值 9% 的地方算，结尾到最后一格超过 5% 的地方"""
    k = int(0.005 * SR)
    if len(x) < 4 * k:
        return x
    fr = np.array([np.abs(x[i:i + k]).max() for i in range(0, len(x) - k, k)])
    if fr.max() <= 0:
        return x
    core = np.where(fr > fr.max() * 0.25)[0][0]                # 声音最响的那段从哪儿起
    a = max(np.where(fr > fr.max() * 0.09)[0][0], core - int(0.12 / 0.005)) * k   # 往前最多 0.12 秒（辅音的开头），再前面的气声不要
    b = (np.where(fr > fr.max() * 0.05)[0][-1] + 1) * k
    return x[max(0, a - int(keep * SR)): min(len(x), b + int(keep * SR * 1.5))]


_BASE = None
def _base_lex():
    """配音模型自带的英语词典：单词 → 音素（空格隔开）"""
    global _BASE
    if _BASE is None:
        _BASE = {}
        try:
            with open(KOKORO + 'lexicon-us-en.txt', encoding='utf-8') as fh:
                for ln in fh:
                    k, _, v = ln.rstrip('\n').partition(' ')
                    if k and v and k not in _BASE:
                        _BASE[k] = v
        except OSError:
            pass
    return _BASE

_EN_BASE = None


def _en_base_lex():
    """6.17：念英文的声音（af_heart，VC.EN_MODEL）自己的词典：单词 → 音素。readings.py 拿它判断哪些词念得出、哪些要 espeak-ng"""
    global _EN_BASE
    if _EN_BASE is None:
        _EN_BASE = {}
        M = os.path.join(MODELS, VC.EN_MODEL) + '/'
        for f in (['lexicon-gb-en.txt'] if VC.EN_ACCENT == 'gb' else []) + ['lexicon-us-en.txt']:
            try:
                with open(M + f, encoding='utf-8') as fh:
                    for ln in fh:
                        k, _, v = ln.rstrip('\n').partition(' ')
                        if k and v and k.lower() not in _EN_BASE:
                            _EN_BASE[k.lower()] = v
            except OSError:
                pass
    return _EN_BASE


def inflect_lex(plan, have):
    """5.1 实测：词典里只有原形（product、make、degree），没有 products、makes、degrees，配音会把它们吞掉或念糊
    （“This factory makes new products.”念成“This factory knew.”）。照原形补上：-s 清辅音后念 s、咝音后念 ɪz、其余念 z；-ed 念 t / d / ɪd；-ing 念 ɪŋ。"""
    base, out = _base_lex(), {}
    if not base:
        return out
    words = set()
    for spec in plan.get('scenes', {}).values():
        for t in ([spec.get('intro')] if spec.get('intro') else []) + list(spec.get('segs') or []):
            t = t.get('t', '') if isinstance(t, dict) else str(t)
            words.update(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", t))
    VL, SIB = {'p', 't', 'k', 'f', 'θ'}, {'s', 'z', 'ʃ', 'ʒ', 'ʧ', 'ʤ', 'tʃ', 'dʒ'}
    last = lambda ph: [x for x in ph.split() if x not in ('ˈ', 'ˌ')][-1] if ph.split() else ''
    for w in words:
        if w in base or w in have or w.startswith('qz') or len(w) < 4:
            continue
        ph = None
        if w.endswith('ies') and w[:-3] + 'y' in base:
            ph = base[w[:-3] + 'y'] + ' z'
        elif w.endswith('es') and w[:-2] in base and last(base[w[:-2]]) in SIB:
            ph = base[w[:-2]] + ' ɪ z'
        elif w.endswith('s') and w[:-1] in base:
            b = base[w[:-1]]; l = last(b)
            ph = b + (' ɪ z' if l in SIB else ' s' if l in VL else ' z')
        elif w.endswith('ed') and (w[:-2] in base or w[:-1] in base):
            b = base[w[:-2]] if w[:-2] in base else base[w[:-1]]; l = last(b)
            ph = b + (' ɪ d' if l in ('t', 'd') else ' t' if l in VL | {'s', 'ʃ', 'ʧ', 'tʃ'} else ' d')
        elif w.endswith('ing') and (w[:-3] in base or w[:-3] + 'e' in base):
            ph = (base[w[:-3]] if w[:-3] in base else base[w[:-3] + 'e']) + ' ɪ ŋ'
        if ph:
            out[w] = ph
    return out

# ---------- 6.36（第八十版）：一句一句的结果缓存 ----------
# 以前改了稿子、重跑配音，每一句都要再听一遍（识别检查）、英文再念一遍；现在稿子、声音、念法都没变而且上次听清了的句子直接用上次的结果，
# 只念改过的和上次没听清的几句。缓存在 <配音文件夹>/cache/sent/
SENT_VER = 'sent-6.36'
EXTRA_SPEED = (1.0, 0.95, 0.9)      # 多念的几遍：原速、慢 5%、慢 10% 轮着来（念慢一点英文单词常常就清楚了）


def _skey(plan, *parts):
    norm_parts = [sorted(p) if isinstance(p, (set, frozenset)) else (sorted(p.items()) if isinstance(p, dict) else p) for p in parts]
    raw = json.dumps([SENT_VER, VC.signature(plan), getattr(VC, 'ONE_VOICE_WHO', '')] + norm_parts, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.md5(raw.encode('utf-8')).hexdigest()[:20]


def sent_get(key):
    p = os.path.join(CACHE, 'sent', key)
    try:
        meta = json.load(open(p + '.json', encoding='utf-8'))
        n = sf.info(p + '.wav').frames
    except Exception:          # noqa: BLE001
        return None, None
    best = ((0, bool(meta.get('zh')), len(meta.get('warn', [])), False, 0.0), np.zeros(n, np.float32), meta.get('heard', ''), [],
            list(meta.get('warn', [])), bool(meta.get('zh')), int(meta.get('attempt', 0)), meta.get('engine', ''))
    return best, p + '.wav'


def sent_put(key, path, meta):
    d = os.path.join(CACHE, 'sent')
    os.makedirs(d, exist_ok=True)
    tmp = os.path.join(d, '%s.%d.tmp' % (key, os.getpid()))
    shutil.copyfile(path, tmp)
    os.replace(tmp, os.path.join(d, key + '.wav'))
    json.dump(meta, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False)
    os.replace(tmp, os.path.join(d, key + '.json'))


def synth(plan, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    sid, speed = int(plan.get('voice', 38)), float(plan.get('speed', 0.95))
    engine = VC.engine(plan)                     # 5.3 起：默认用你本人的声音（声音克隆）
    zv_speed = float(plan.get('zvSpeed', VC.SPEED))
    probs = VC.voice_problems(plan)
    if probs and not VC.allow38(plan):           # 6.9 起：缺东西就停，不再悄悄整段改用 38 号
        raise SystemExit('不能配音：声音没准备好（不会再悄悄改用 38 号念）\n' + '\n'.join('  - ' + p for p in probs)
                         + '\n先跑 bash scripts/setup.sh（没装完的会接着装），看到“声音：✅”再合成；真要用 38 号，plan.json 写 "engine": "kokoro"')
    if engine == 'zipvoice':
        print('配音：中文用声音克隆（参考录音 %s：“%s”）；音节块用 %s；其余英文用 %s 的 %d 号' % (
            VC.ref()[0], VC.ref()[1][:24], '和英文同一个声音' if VC.SYL_VOICE == 'en' else 'Kokoro v1.1 的 %s 号' % VC.SYL_VOICE,
            VC.EN_MODEL, int(plan.get('enVoice', VC.EN_SID))))
    else:
        why = '' if str(plan.get('engine', '')).lower() == 'kokoro' else '（没找到声音克隆的模型或参考录音，先跑 setup.sh）'
        print('配音：Kokoro %d 号%s' % (sid, why))
    lex = dict(plan.get('lexicon') or {})
    auto = inflect_lex(plan, lex)                # 5.1 起：词典里没有的 -s / -es / -ed / -ing 形式，照原形补上读音
    if auto:
        print('自动补了读音（词典里只有原形）：' + '、'.join(sorted(auto)))
        lex.update(auto)
    # 6.17：英文的四种念法——/音标/ 念音、pro- / -ion 当单词念（词缀表）、词典里没有的词根用 espeak-ng 的读音；单独的字母留给克隆的声音（readings.py）
    RD.BASE = _en_base_lex()
    rewrite, extra, notes = RD.prepare(plan, set(RD.BASE) | {str(k).lower() for k in lex})
    if extra:
        lex.update(extra)
    if notes:
        print('念法（6.17）：\n' + '\n'.join('  ' + n for n in notes))
    if not RD.have_espeak():
        print('提醒：没装 espeak-ng（bash setup.sh 会装），英文词典里没有的词根（duc、ject）只能一个个字母念')
    if lex:                                     # 配音稿自己的词典：音素词、生词（要在建模型之前写好）
        tag = os.environ.get('WF_SYNTH_TAG', '')        # 6.35：并行配音时每个进程各写一份词典，不互相覆盖
        lp = os.path.join(out_dir, 'lexicon-plan%s.txt' % ('.' + tag if tag else ''))
        zp = os.path.join(out_dir, 'lexicon-plan-ipa%s.txt' % ('.' + tag if tag else ''))
        with open(lp, 'w', encoding='utf-8') as fh, open(zp, 'w', encoding='utf-8') as fz:
            for k, v in lex.items():
                if re.fullmatch(r"[a-z][a-z'-]*", str(k).lower()) and str(v).strip():
                    fh.write('%s %s\n' % (str(k).lower(), ' '.join(str(v).split())))
                    fz.write('%s || %s\n' % (str(k).lower(), to_ipa(v)))
        if lp not in EXTRA_LEX:
            if _tts is not None:
                print('提醒：配音模型已经建好了，这一份词典要下次运行才用得上')
            EXTRA_LEX.insert(0, lp)
        if zp not in EXTRA_ZLEX:
            EXTRA_ZLEX.insert(0, zp)
    word = str(plan.get('word', ''))
    known = {str(x).lower() for x in lex}
    manifest, flagged, fell, fell_en = {}, [], [], []
    print('设备（6.36）：' + VC.devices(), flush=True)
    # 6.40（第八十四版）：sherpa-onnx 用显卡时，一开始就先把它的显卡模型建好，再碰 onnxruntime（kokoro_clean 念英文）。
    #   顺序反了（先念英文、后建声音克隆）同一个进程里两套 onnxruntime 打架，用户电脑上批量配音段错误（返回码 139 / -11）；
    #   gpu_check 先建声音克隆、后念英文，所以测的时候没事
    if VC.provider('zv') == 'cuda' and VC.engine(plan) == 'zipvoice':
        zipvoice()
    if VC.provider('asr') == 'cuda':
        asr()
    if VC.provider('en') == 'cuda':
        tts_en()

    def norm(x):
        v = x[np.abs(x) > np.abs(x).max() * 0.05] if len(x) else x     # 只按有声音的地方算（句子里插了停顿也一样响）
        return x / (np.sqrt(np.mean(v ** 2)) + 1e-9) * 0.08 if len(v) else x   # 每一句一样响（RMS ≈ -22 dBFS），最后整体再做响度标准化

    def judge(x, text):
        heard = transcribe_array(x, SR)
        miss, warn = check(text, heard, word, known=known)
        zh = zh_mismatch(text, heard)
        e = zh_err(text, heard)
        return (len(miss), zh, len(warn), e > ZH_OK, round(e, 2)), heard, miss, warn, zh

    en_sid = int(plan.get('enVoice', VC.EN_SID))
    en_cache = {}
    global CACHE
    CACHE = os.path.join(out_dir, 'cache')
    chosen = []
    only = set(filter(None, os.environ.get('WF_SYNTH_SCENES', '').split(',')))     # 6.35：并行配音时这个进程只念这几幕
    for scene, spec in plan['scenes'].items():
        if only and scene not in only:
            continue
        items = ([('intro', spec['intro'])] if spec.get('intro') else []) + [('seg%d' % i, t) for i, t in enumerate(spec['segs'])]
        manifest[scene] = []
        for name, seg in items:
            orig = str(seg.get('t', '')) if isinstance(seg, dict) else str(seg)
            text = rewrite.get(orig, orig)              # 6.17：合成用改好的（音素词）；manifest 里还写原文，画面按它对时间
            sp = float(seg.get('speed', speed)) if isinstance(seg, dict) else speed
            zs = float(seg.get('zvSpeed', zv_speed)) if isinstance(seg, dict) else zv_speed
            phon = bool(PHON_ONLY.match(text))
            if not phon:
                text = norm_text(text)                   # 6.32：省略号统一、换行没有标点就接着念
            # 5.5 起：念英文的地方（音节块、单词、整句例句）用英文声音；中文用克隆的声音；中英混着的拆开接起来
            if engine == 'zipvoice':
                if phon:
                    how = 'syl'                  # 读音拆分的音节块：5.10 起 af_heart（voice_config.SYL_VOICE）
                elif not CJK.search(text) and en_runs(text):
                    how = 'en'
                elif en_runs(text):
                    how = 'mix1' if rapid(text, scene) else 'clone+en'      # 6.32：切换很快的一句，一个声音念
                else:
                    how = 'clone'
            else:
                how = 'kokoro'
            role = VC.role_of(scene, text)
            best = None
            tries = 4 if how in ('clone', 'clone+en') or (how == 'mix1' and getattr(VC, 'ONE_VOICE_WHO', 'clone') != 'en') else 2 if how == 'mix1' else 1    # 克隆每次念得不一样：没听清就重念，最多 4 遍，留最好的一遍
            # 6.36：稿子、声音、念法都没变、上次听清了的句子直接用上次的结果（不再听一遍、不再念一遍）
            skey = _skey(plan, text, orig, how, sp, zs, role, en_sid, sid, word, known, lex)
            best, hit_wav = sent_get(skey)
            if hit_wav:
                chosen = []
            # 6.36：整句你的声音念的一句（切换很快），要学的单词 4 遍都没听清：只这一句再多念几遍（语速轮着放慢一点），不用整个词重来
            more = VC.extra_tries() if how == 'mix1' and getattr(VC, 'ONE_VOICE_WHO', 'clone') != 'en' else 0
            limit, attempt = (0 if hit_wav else tries), 0
            while attempt < limit:
                zs_try = zs * EXTRA_SPEED[(attempt - tries) % len(EXTRA_SPEED)] if attempt >= tries else zs
                keys = []                                    # 这一遍念的中文段（存缓存用）
                if how == 'syl':
                    x = syllable(text, sid, sp, en_sid)
                elif how == 'en':
                    x = gen_en(text, en_sid, float(seg['enSpeed']) if isinstance(seg, dict) and 'enSpeed' in seg else None)
                elif how == 'clone':          # 6.32：按句末标点一句一句念，中间的停顿照标点分长短
                    x = by_sentence(text, lambda s: gen_voice(s, zs_try, role, fresh=attempt > 0, keys=keys))       # 第一遍先用缓存里念好的
                elif how == 'clone+en':
                    x = by_sentence(text, lambda s: compose(s, role, zs_try, en_sid, en_cache, fresh=attempt > 0, keys=keys))
                elif how == 'mix1':           # 6.32：整句一个声音念。默认你本人的声音（克隆模型中英都能念）；VC.ONE_VOICE_WHO = 'en' 换成 af_heart
                    if getattr(VC, 'ONE_VOICE_WHO', 'clone') == 'en':
                        x = by_sentence(text, lambda s: gen_mix1(s, en_sid, VC.MIX_SPEED - 0.05 * attempt))
                    else:
                        x = by_sentence(norm_text(orig), lambda s: one_voice(s, zs_try, role, attempt > 0, keys, en_sid))      # 6.33：用原文（不用改写成音素词的），词缀去掉连字符；单独成句的整句英文例句照旧美式女声
                else:
                    x = gen(text, sid, sp)
                    if phon:
                        x = trim(x)
                x = norm(x)
                score, heard, miss, warn, zh = judge(x, text)
                if how == 'clone+en':
                    # 英文段是英文声音念的、单独听过了；拼起来以后识别模型常把插进来的英文听岔，整句只看中文念得对不对
                    miss, warn = [], []
                    score = (0, zh, 0) + score[3:]
                if best is None or score < best[0]:
                    best = (score, x, heard, miss, warn, zh, attempt, how)
                    chosen = keys
                if score[:4] == (0, False, 0, False):
                    break
                attempt += 1
                if attempt == limit == tries and more and best[0][0]:
                    limit = tries + more
                    print('%-8s %-5s 要学的单词没听清（%s），这一句再念最多 %d 遍' % (scene, name, ','.join(best[3]), more), flush=True)
            if how in ('clone', 'clone+en') and best[0][0] and plan.get('fallback38'):   # 5.6 起默认不退回（中文都用你的声音）；plan 写 "fallback38": true 才退回 38 号
                for attempt in range(2):
                    x = norm(gen(text, sid, sp))
                    score, heard, miss, warn, zh = judge(x, text)
                    if score < best[0]:
                        best = (score, x, heard, miss, warn, zh, attempt, 'kokoro-退回')
                    if not score[0]:
                        break
                if best[7] == 'kokoro-退回':
                    fell.append('%s/%s' % (scene, name))
            if how == 'mix1' and best[3] and VC.mix_fallback(plan):
                # 6.36：开了 mixFallback（用户同意）：多念了还是没听清，这一句改成中文你的声音、英文美式女声拼着念（和平常中英拼接一样）
                keys = []
                x = norm(by_sentence(text, lambda s: compose(s, role, zs, en_sid, en_cache, fresh=False, keys=keys)))
                score, heard, miss, warn, zh = judge(x, text)
                best = ((0, zh, 0) + score[3:], x, heard, [], [], zh, 0, 'clone+en-退回')
                chosen = keys
                fell_en.append('%s/%s' % (scene, name))
            _, x, heard, miss, warn, zh, attempt, used = best
            if used in ('clone', 'clone+en', 'clone+en-退回'):
                for k, a in chosen:                           # 留下来的那一遍存进缓存，下次稿子没改这一句就不重念
                    cache_put(k, a)
            if zh:
                warn = warn + ['中文对不上']
            path = os.path.join(out_dir, '%s_%s.wav' % (scene, name))
            if hit_wav:
                shutil.copyfile(hit_wav, path)               # 6.36：上次的结果原样拿来（不重新写，一个字节都不变）
            else:
                sf.write(path, x.astype(np.float32), SR)
                if not miss:
                    sent_put(skey, path, {'heard': heard, 'warn': [w for w in warn if w != '中文对不上'], 'zh': bool(zh), 'attempt': attempt, 'engine': used})
            manifest[scene].append({'name': name, 'path': path, 'dur': round(len(x) / SR, 3), 'text': orig, 'heard': heard,
                                    **({'said': text} if text != orig else {}),
                                    'miss': miss, 'warn': warn, 'engine': used})
            mark = ('   <-- 没听清：' + ','.join(miss) if miss else '') + ('   （可能没听清：' + ','.join(warn) + '）' if warn else '') \
                + ('   [第 %d 遍]' % (attempt + 1) if attempt and not hit_wav else '') + ('   [退回 38 号]' if used == 'kokoro-退回' else '') \
                + ('   [英文改美式女声念]' if used == 'clone+en-退回' else '') + ('   （上次念好的）' if hit_wav else '')
            print('%-8s %-5s %5.2fs [%s] %s%s' % (scene, name, len(x) / SR, used, heard, mark), flush=True)
            if miss:
                flagged.append({'scene': scene, 'name': name, 'text': orig, 'heard': heard, 'miss': miss})
    if fell_en:
        print('这几句整句你的声音念、多念了还是没听清，改成了中文你的声音 + 英文美式女声（开了 mixFallback）：' + '、'.join(fell_en))
    if fell:
        print('这几句声音克隆 4 遍都没念清，用了 38 号：' + '、'.join(fell) + '（plan 写了 fallback38；想全用自己的声音就去掉它，或按 narration-guide.md 第五节换个说法）')
    tag = os.environ.get('WF_SYNTH_TAG', '')
    json.dump(manifest, open(os.path.join(out_dir, 'manifest.%s.json' % tag if tag else 'manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return manifest, flagged


def synth_jobs():
    """6.35（第七十九版）：几个进程一起念。WORDFILM_SYNTH_JOBS 指定；不指定按 CPU 和空闲内存算（每个进程约 3 GB），最多 3 个；1 核的沙盒就是 1 个"""
    v = os.environ.get('WORDFILM_SYNTH_JOBS')
    if v and v.isdigit():
        return max(1, int(v))
    cpu = os.cpu_count() or 1
    try:
        avail = next(int(l.split()[1]) for l in open('/proc/meminfo') if l.startswith('MemAvailable')) / 1048576
    except Exception:
        avail = 0
    return max(1, min(3, cpu // 6, int((avail - 2) // 3)))


def merge_parts(plan, out_dir, tags):
    """6.35：把各进程的 manifest.<tag>.json 按稿子里幕的顺序合成 manifest.json，返回没听清的句子"""
    parts = {}
    for t in tags:
        p = os.path.join(out_dir, 'manifest.%s.json' % t)
        parts.update(json.load(open(p, encoding='utf-8')))
        os.remove(p)
    manifest = {k: parts[k] for k in plan['scenes'] if k in parts}
    json.dump(manifest, open(os.path.join(out_dir, 'manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return [{'scene': k, 'name': s['name'], 'text': s['text'], 'heard': s['heard'], 'miss': s['miss']}
            for k, segs in manifest.items() for s in segs if s.get('miss')]


def synth_parallel(plan_path, plan, out_dir, jobs):
    """6.35：按幕分成几份（按字数分得差不多重），每份一个进程念（看的是整份稿子，词典、念法和一个一个念完全一样），念完按原来的顺序合成 manifest.json。
    有一份出错就改成一个一个念（念好的中文在缓存里，直接用）"""
    import subprocess
    os.makedirs(out_dir, exist_ok=True)
    def size(v):
        items = ([v['intro']] if v.get('intro') else []) + list(v.get('segs', []))
        return 1 + sum(len(str(x.get('t', '')) if isinstance(x, dict) else str(x)) for x in items)
    w = {k: size(v) for k, v in plan['scenes'].items()}
    groups, load = [[] for _ in range(jobs)], [0] * jobs
    for k in sorted(w, key=w.get, reverse=True):
        i = load.index(min(load))
        groups[i].append(k)
        load[i] += w[k]
    th = max(1, min(8, (os.cpu_count() or 1) // jobs))
    print('配音：%d 个进程一起念（每个 %d 个线程）' % (jobs, th), flush=True)
    procs = []
    for i, g in enumerate(groups):
        if g:
            env = dict(os.environ, WF_SYNTH_SCENES=','.join(g), WF_SYNTH_TAG='p%d' % i, WORDFILM_THREADS=str(th))
            procs.append((i, subprocess.Popen([sys.executable, os.path.abspath(__file__), plan_path, out_dir], env=env)))
    codes = {i: p.wait() for i, p in procs}
    bad = {i: c for i, c in codes.items() if c != 0}
    if bad:
        print('并行配音有 %d 份出错了（返回码 %s；-9 多半是内存不够：设 WORDFILM_SYNTH_JOBS=1，或少开几个词一起做），改成一个一个念（念好的中文直接用缓存）'
              % (len(bad), '、'.join(str(c) for c in bad.values())), flush=True)
        if any(c in (-11, -6, -4, 139, 134, 132) for c in bad.values()) and 'cuda' in (VC.provider('zv'), VC.provider('en'), VC.provider('asr')):
            # 6.40：显卡配音崩了（段错误）——这个词改用 CPU 念（主进程还没碰过显卡，改环境变量就生效），不卡住
            for k in ('WORDFILM_ZV_DEVICE', 'WORDFILM_EN_DEVICE', 'WORDFILM_ASR_DEVICE', 'WORDFILM_DEVICE'):
                os.environ[k] = 'cpu'
            print('提醒：显卡配音崩了，这个词改用 CPU 念', flush=True)
        return synth(plan, out_dir)[1]
    return merge_parts(plan, out_dir, ['p%d' % i for i, _ in procs])


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    plan = json.load(open(sys.argv[1], encoding='utf-8'))
    child = bool(os.environ.get('WF_SYNTH_SCENES'))
    jobs = 1 if child else synth_jobs()
    if jobs > 1 and len(plan.get('scenes', {})) > 1:
        flagged = synth_parallel(sys.argv[1], plan, sys.argv[2], jobs)
    else:
        _, flagged = synth(plan, sys.argv[2])
    if child:
        sys.exit(0)
    print('\n%d 句有要学的单词没听清%s' % (len(flagged), '：改 plan.json 里这几句的说法再合成（见 references/narration-guide.md 第五节）' if flagged else '，可以渲染了'))
