"""配音用哪个声音、模型放在哪（5.3 起，第二十五版）。synth.py、saytest.py、voice_prep.py、run.py 共用，不引入大模型，导入很快。

讲解句、例句：ZipVoice 声音克隆，照着“参考录音”的嗓音念（中英混读）。
只念音节块的句子（qzca 这种音素词）：Kokoro 38 号（plan.json 的 voice、speed）。

参考录音（ref.wav + ref.txt，另有 noise.wav 是录音里的底噪样本）按这个顺序找，找到就用：
  1. 环境变量 $WORDFILM_VOICE 指的文件夹
  2. 技能自带的 assets/voice（用户本人的声音；6.45 起取自仓库「素材/音色/5音色.m4a」第 41.7～49.5 秒，6音色是同一次讲课）
  3. ~/wordfilm-voice（voice_prep.py 默认写到这里）
"""
import hashlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
MODELS = os.environ.get('WORDFILM_MODELS', os.path.expanduser('~/wordfilm-models'))

# 优先用 fp32 版（456 MB）：比 int8 版干净一点（DNSMOS 总分 3.37 比 3.24），慢一倍；没下载就用 int8 版（104 MB）
_FP32 = ('sherpa-onnx-zipvoice-distill-fp32-zh-en-emilia', 'encoder.onnx', 'decoder.onnx')
_INT8 = ('sherpa-onnx-zipvoice-distill-int8-zh-en-emilia', 'encoder.int8.onnx', 'decoder.int8.onnx')
DONE_DIR = os.path.join(MODELS, '.done')     # 6.9 起：setup.sh 装完整一样东西才在这里写一个同名的标记


def _done(name):
    return os.path.exists(os.path.join(DONE_DIR, name))


def _pick_zv():
    """装完整（有标记）的优先：fp32 解压到一半、int8 是好的，就用 int8"""
    for m in (_FP32, _INT8):
        if _done(m[0]) and os.path.exists(os.path.join(MODELS, m[0], m[2])):
            return m
    return next((m for m in (_FP32, _INT8) if os.path.exists(os.path.join(MODELS, m[0], m[2]))), _FP32)


ZIPVOICE_NAME, ZV_ENCODER, ZV_DECODER = _pick_zv()
ZIPVOICE_DIR = os.path.join(MODELS, ZIPVOICE_NAME) + '/'
VOCODER = os.path.join(MODELS, 'vocos_24khz.onnx')
EN_LEXICON = os.path.join(MODELS, 'lexicon-en-us.txt')     # 没有它，sherpa-onnx 会把英文单词悄悄跳过

# ZipVoice 蒸馏模型要配 guidance 3.0（推荐值）。sherpa-onnx 默认 1.0，实测底噪、刺耳的电流声明显。
# 用户录音实测（DNSMOS，1～5 分越高越好；4 句平均）：
#   默认 4 步 + 1.0：总分 2.62、背景噪声 3.12；8 步 + 1.0：2.73、3.47
#   4 步 + 3.0 + 参考录音先降噪：总分 3.27、背景噪声 4.08（8 步反而不更好，还慢一倍）
STEPS = 4
GUIDANCE = 3.0               # 6.50：2.0 → 3.0（回到 ZipVoice 蒸馏模型的推荐值）。6.45 改成 2.0 时的测试没生效（模型第一次念就建好、后面改引导不变），实际测的都是 3.0。
                             #   6.50 每种设置都重建模型重测：混进同样响的噪声再让识别模型听，两组句子：2.0 听错 6.7%、6.2%，3.0 4.5%、4.2%（两组都少），2.5 4.2%、7.5%（不稳）；
                             #   3.0 音质分 OVRL 3.32～3.33、像不像本人 0.81～0.82，和 2.0 差不多。放慢语速（0.85）反而更差（8～12%）
# 6.10 起（第四十七版）中文语速 0.95（以前 1.0）。用户：“声音有点快，不是很自然，让我的声音慢一点点，再自然一点”。
# 换了参考录音（见 assets/voice、SKILL.md“这一版改了什么（6.10.0）”）以后，三句讲解实测每秒 5.9 字（1.0）/ 5.3 字（0.93）；
# 第四十六版是 6.25 字。0.95 约 5.5 字，慢一成多，又不至于拖。plan.json 的 zvSpeed 照旧可以整段改，一句单独的写 {"t": "…", "zvSpeed": 0.9}
SPEED = 0.95
VERSION = '6.25-a'            # 改了合成设置或清理做法就改这里：run.py 会把旧配音重新合成（6.25：英文换成干净念法）
REF_DENOISE = 0              # 6.45：不再给参考录音二次降噪（6.44 的 0.9 让声音发“电子”、不像本人：像不像本人 0.80 → 0.74）；新参考录音做的时候已经轻降过
OUT_DENOISE = 0              # 6.47：不降噪了（参考录音干净，念出来的底噪本来就低；降噪会让人声发虚）
GATE = False                 # 6.47：不用静音门——实测它让停顿、字尾的声音忽大忽小（10 ms 跳 6 dB 以上的 10% → 17%），听着是“弱弱的震动”
# 6.46：音色校正（用户：“发闷、发尖有点重”）。实测 6.45 合成的声音和真人录音（5音色、6音色）比，以 200～4000 Hz 的平均为准：
#   160～400 Hz 多了 3～4 dB（发闷），2.5～6.3 kHz 多了 4～6 dB、8～10 kHz 多了 3 dB（发尖）。照差值反过来补（三档平滑）
EQ_BANDS = [(100, 0.0), (125, 0.0), (160, 0.6), (200, -1.2), (250, -0.9), (315, -2.5), (400, -0.6), (500, 1.8), (630, 3.2),
            (800, 3.3), (1000, 1.5), (1250, 1.0), (1600, 0.9), (2000, 0.4), (2500, -2.2), (3150, -4.5), (4000, -3.8),
            (5000, -2.5), (6300, -1.5), (8000, -1.4), (10000, -0.4)]
# 6.50：引导 2.0 → 3.0 声音亮了一点（2.5～6.3 kHz +0.9 dB、8～10 kHz +1.3 dB），这几档相应压下去，音色和 6.49 一样
# 6.47：用户：“闷和尖都有，但是比 6.45 弱一些了”——把 6.46 补完还差的再补上（中频 500～1000 Hz 再提，2.5～4 kHz 再压），和真人偏差 1.3 → 1.0 dB
ROUGH_MAX = 3.0              # 6.49：最后一个字“发颤”分超过这个就再念一遍（voice_clean.final_rough）
ROUGH_RETRY = 1              # 6.49：最多再念几遍，挑最不颤的那一遍（再念两遍中文配音慢五成多，一遍慢两成左右）
TAIL_TAME = (12.0, 80)       # 6.49：最后一个字落下 12 dB 以后 80 毫秒淡出（None 不做）
PRON_RETRY = 1               # 6.50：念完用识别模型对着拼音核一遍（不算声调），有字没念出来就再念一遍，挑念全的
CLONE_VERSION = '6.50-a'     # 只管中文克隆那部分：没变就复用缓存里念好的中文（audio/cache），不重念

# 5.7 起配音分三种声音（用户定的）：
#   1. 中文讲解：用户本人的声音（ZipVoice 声音克隆，上面那些设置）
#   2. 读音拆分的音节块（qzca 这种音素词，ca + me + ra）：Kokoro v1.1 的 38 号（plan.json 的 voice、speed），只有它念拆开的半个音节准
#   3. 其余英文（单词、前缀词根、“连起来”的整词、例句）：Kokoro v1.0 的 af_heart（3 号，美式女声，Kokoro 里公认最自然的英文声音）
#      实测：5 句例句识别全对，单独念的词 6/6 听对（camera、transport、thermostat、mouse、camera obscura、cover），DNSMOS 3.25。
#      对比过：af_bella（2 号）也全对但稍毛（3.11）；af_nicole 气声重（2.48）；bf_emma 英式，单词 4/6。
#      5.5 用过的 Kokoro v1.1 的 2 号 bf_vale（有噪音、不好听）、5.6 的“38 号音色 + 母语语调”（38 号念英文差）都不用了。
# 5.10 起读音拆分的音节块也用 af_heart（用户听过 7 个声音挑的）：单念音节时它比 38 号稳得多
#   （“不自然分”平均 2.7，38 号 12.3；DNSMOS 3.23，38 号 3.05）。音素照旧按配音稿 lexicon 里音节表的音标。
#   SYL_VOICE = 38 回到原来的 38 号（单念一遍）；'en' 用念英文的那个声音（EN_SID）
SYL_VOICE = 'en'
SYL_SPEED = 0.9
# 5.9 试过的两种 38 号优化（几种念法挑最稳的 / PSOLA 拉平），用户听了都不如原来，不再用：SYL_PICK、SYL_FLATTEN
SYL_PICK = False
SYL_FLATTEN = False
EN_MODEL = 'kokoro-multi-lang-v1_0'
EN_SID = 3
EN_ACCENT = 'us'             # af_heart 是美式：按美式词典（lexicon-us-en.txt）；换英式声音（bf_emma 21 号）时改成 'gb'
EN_WORD_SPEED = 0.88         # 单独念的单词、词根、音节块：慢一点，念清楚
EN_SENT_SPEED = 0.92         # 整句例句
EN_CLEAN = True              # 6.25：英文前面垫“okay,”一起合成再切掉，开头不多出 e / ai 的音（kokoro_clean.py）；False 回到老念法
# 中文和插进来的英文之间留多长：边界上有标点（，：、。）就按句中停顿，没有就短一点。
# 用户 7 分钟讲课录音里，短句之间的停顿中位数 0.36 秒（四分之一 0.24，四分之三 0.56）
PAUSE_PUNCT = 0.30
PAUSE_TIGHT = 0.12

# 参考录音可以有几段，按句子的用处挑（同一次录音，音色一样，语气更贴）：
#   ref.wav / ref.txt                 讲解（默认）
#   ref_translate.wav / .txt          念例句的中文翻译（可选；6.10 起技能里没有这一段：实测讲解那段念翻译也最像本人，见 SKILL.md）
#   ref_question.wav / .txt           问句（可选）
ROLES = ('translate', 'question')


def threads():
    v = os.environ.get('WORDFILM_THREADS')          # 6.35：并行配音时每个进程分到的线程数（synth.py 设）
    if v and v.isdigit() and int(v) > 0:
        return int(v)
    return max(1, min(8, os.cpu_count() or 2))


def voice_dir():
    # 6.45：技能自带的（仓库「素材/音色」里的录音做的）排在 ~/wordfilm-voice 前面：仓库里换了声音，同步到 WSL 就生效
    for d in (os.environ.get('WORDFILM_VOICE'), os.path.join(SKILL, 'assets', 'voice'), os.path.expanduser('~/wordfilm-voice')):
        if d and os.path.exists(os.path.join(d, 'ref.wav')) and os.path.exists(os.path.join(d, 'ref.txt')):
            return d
    return None


def ref(role=None):
    """(参考录音路径, 录音里说的话, 底噪样本路径或 None)；没有就 None。role：translate / question，没有那一段就用讲解的"""
    d = voice_dir()
    if not d:
        return None
    base = 'ref' if role not in ROLES or not os.path.exists(os.path.join(d, 'ref_%s.wav' % role)) else 'ref_%s' % role
    if not os.path.exists(os.path.join(d, base + '.txt')):
        base = 'ref'
    text = open(os.path.join(d, base + '.txt'), encoding='utf-8').read().strip()
    noise = os.path.join(d, 'noise.wav')
    return os.path.join(d, base + '.wav'), text, (noise if os.path.exists(noise) else None)


def role_of(scene, text):
    """这一句用哪段参考录音：例句的中文翻译用“念翻译”的，问句用“问句”的，其余用讲解的"""
    if scene.startswith('example') and not any('A' <= c <= 'z' and c.isalpha() for c in text):
        return 'translate'
    if text.rstrip().endswith(('？', '?')):
        return 'question'
    return None


def _missing(folder, names):
    return [n for n in names if not os.path.exists(os.path.join(folder, n))]


def voice_problems(plan=None):
    """6.9 起：配音用不了“中文 = 你本人的声音（声音克隆），英文 = af_heart”的原因，一条一句；空的 = 都齐了。
    setup.sh 最后的检查、run.py 开工前、synth.py 合成前都用这一个函数，三处说法一致（第四十五版以前 setup.sh 只看
    decoder.onnx 在不在，解压到一半的模型它也说“准备好了”，合成时却悄悄退回 38 号）。"""
    out = []
    miss = _missing(ZIPVOICE_DIR, (ZV_ENCODER, ZV_DECODER, 'tokens.txt', 'lexicon.txt', 'espeak-ng-data'))
    if miss:
        out.append('声音克隆模型 %s 缺 %s' % (ZIPVOICE_NAME, '、'.join(miss)))
    elif not _done(ZIPVOICE_NAME):
        out.append('声音克隆模型 %s 没有“装完整”的标记（多半是解压到一半停了）' % ZIPVOICE_NAME)
    for p in (VOCODER, EN_LEXICON):
        n = os.path.basename(p)
        if not os.path.exists(p):
            out.append('缺 %s' % n)
        elif not _done(n):
            out.append('%s 没有“下载完整”的标记' % n)
    if ref() is None:
        out.append('没找到参考录音（技能的 assets/voice 或 ~/wordfilm-voice 里的 ref.wav + ref.txt）')
    en = os.path.join(MODELS, EN_MODEL)
    miss = _missing(en, ('model.onnx', 'voices.bin', 'tokens.txt', 'espeak-ng-data', 'lexicon-us-en.txt'))
    if miss:
        out.append('英文声音 af_heart（%s）缺 %s' % (EN_MODEL, '、'.join(miss)))
    elif not _done(EN_MODEL):
        out.append('英文声音 af_heart（%s）没有“装完整”的标记' % EN_MODEL)
    return out


def allow38(plan=None):
    """只有明说要 38 号才用它：plan.json 写 "engine": "kokoro"，或者环境变量 WORDFILM_ALLOW_38=1"""
    return str((plan or {}).get('engine', '')).lower() == 'kokoro' or os.environ.get('WORDFILM_ALLOW_38') == '1'


def describe():
    """一行说清这次配音用的是什么声音（run.py、setup.sh 打印）"""
    r = ref()
    who = '参考录音 %s：“%s”' % (os.path.join(os.path.basename(os.path.dirname(r[0])), os.path.basename(r[0])), r[1][:24] + ('…' if len(r[1]) > 24 else '')) if r else '没有参考录音'
    return '中文 = 你本人的声音（声音克隆，%s）；英文、音节块 = af_heart 美式女声（%s 的 %d 号）' % (who, EN_MODEL, EN_SID)


def zipvoice_ready():
    """声音克隆那一半齐不齐（英文 af_heart 另算，见 voice_problems）"""
    return not [p for p in voice_problems() if '英文声音' not in p]


def engine(plan):
    """plan.json 写 "engine": "kokoro" 就用原来的 38 号；默认用声音克隆。模型或参考录音不全时这里返回 kokoro，
    但 6.9 起 synth.py / run.py 看到没明说要 38 号就停下来，不会再悄悄用 38 号出片"""
    want = str(plan.get('engine') or 'zipvoice').lower()
    if want == 'zipvoice' and zipvoice_ready():
        return 'zipvoice'
    return 'kokoro'


def signature(plan):
    """配音用的声音和设置：变了 run.py 就重新合成（只看稿子 md5 的话，换了声音也会复用旧配音）"""
    e = engine(plan)
    if e == 'kokoro':
        return 'kokoro|%s|%s' % (plan.get('voice', 38), plan.get('speed', 0.95))
    m = hashlib.md5()
    for role in (None,) + ROLES:
        wav, text, _ = ref(role)
        m.update(open(wav, 'rb').read() + text.encode('utf-8'))
    en = '%s|%s|%s|%s|%s|%s|%s|%s' % (SYL_VOICE, SYL_SPEED, SYL_PICK, EN_MODEL, plan.get('enVoice', EN_SID), EN_ACCENT, EN_WORD_SPEED, EN_SENT_SPEED)
    return 'zipvoice|%s|%s|%s|%s|%s|%s|%s' % (m.hexdigest()[:10], ZV_DECODER, STEPS, GUIDANCE, plan.get('zvSpeed', SPEED), en, VERSION)


# 6.32（第七十六版）：句子里的停顿照中文朗读的规矩分长短——顿号 < 逗号 < 冒号 < 分号、省略号 < 句号、问号、叹号（逗号“表示小于分号大于顿号的停顿”）；
# 中英之间只有空格的停得最短；换行没有标点的不停（synth.norm_text）。用户：“顿号，逗号，空格停顿要短一点，因为不是一句话结束了；
# 句号，分号，省略号中间停顿要稍微长一点，因为一句话结束了；换行的时候，如果没有标点符号就按正常来读，没标点符号不需要停顿”。
# 一句里先按句末标点（。！？；…）切开分别念，中间停 PAUSE_OF；一句里面中英拼接的地方按交界的标点停（synth.compose）；句子和句子之间还是 render.py 的 0.40 秒
# 6.33（第七十七版）：照朗读的停顿规范重排（顿号最短 < 逗号 < 分号、冒号 < 句号、问号、叹号、省略号 < 换段 / 序号）。
# 用户：“对于序号来说，也是分段，这里停顿时间要更长一点；冒号说明后面是要讲的完整内容，冒号也要做稍长的停顿，让学生有时间做好听后面内容的准备；省略号也算一个句号，也要停顿长一点”。
# 冒号、序号 6.33 起也是切开念的地方（synth.sentences），所以这几个数真的会停出来；一句里面的顿号、逗号还是交给声音模型自己停（短，语气连着）
PAUSE_OF = {'、': 0.15, '，': 0.30, ',': 0.28, '；': 0.45, ';': 0.42, '：': 0.45, ':': 0.42,
            '。': 0.60, '！': 0.60, '!': 0.60, '？': 0.60, '?': 0.60, '…': 0.60,
            '¶': 0.85}      # ¶ = 换段、①②③ 序号前面
PAUSE_TIGHT = 0.06       # 中英之间只有空格、没有标点
PAUSE_PUNCT = 0.22       # 老代码“有标点”的停顿（现在按 PAUSE_OF 分）
# 6.32：中英切换很快的一句（考点那几行；英文后面不加标点直接接中文；来回切了三次以上、中间的中文很短）整句用念英文的声音（af_heart）念，中文也是它念，
# 不来回换人（用户：“单词后面紧接着中文，这种就不要切换音色了，就用美语来读中文……对于这个切换很快的现象，就让一个人来读，避免学生反应不过来”）
ONE_VOICE = True
MIX_SPEED = 0.9          # af_heart 念整句中英混合的语速
SHORT_ZH = 6             # 夹在两段英文中间、不超过这么多个汉字的中文算“很短”
# 6.32 实测：af_heart 念中文听不清（语音识别把“保护”听成 Pahu、“词性转换”听成 Xing Zhuanghuan），所以“一个人念”默认用你本人的声音：
# 声音克隆模型（ZipVoice 中英双语）英文也念得出来，中文清楚。想照原话用美式女声念整句，改成 'en'（中文会念不清）
ONE_VOICE_WHO = 'clone'



# 6.36（第八十版）：用显卡（CUDA）念。用户：“在生成的时候还是在用 CPU，没有用 GPU，导致生成的速度不是很快”。
#   哪一路用显卡由环境变量定（本地技能 local-wordfilm 的 gpu_check.py 在用户电脑上逐项测好、写进 ~/.wordfilm-gpu.env）：
#   WORDFILM_ZV_DEVICE = 声音克隆 + 声码器；WORDFILM_EN_DEVICE = 英文 af_heart、38 号；WORDFILM_ASR_DEVICE = 识别检查；值 cpu / cuda；
#   WORDFILM_DEVICE 一次设全部。不设就是 cpu（云端沙盒、没装显卡版的电脑和第七十九版完全一样）。
#   设了 cuda 但装的不是显卡版（sherpa-onnx 版本号里没有 cuda、onnxruntime 没有 CUDAExecutionProvider）：这一路用 CPU，提醒一次。
#   显卡和 CPU 念出来的声音是同一个模型，只有算术上极小的差别；所以设备不算进 signature()，换设备不会把念好的配音全部重念。
_WARNED = set()


def _want_cuda(part):
    v = (os.environ.get('WORDFILM_%s_DEVICE' % part.upper()) or os.environ.get('WORDFILM_DEVICE') or 'cpu').strip().lower()
    return v in ('cuda', 'gpu')


def provider(part):
    """sherpa-onnx 的 provider：part = 'zv'（声音克隆）、'en'（英文）、'asr'（识别）"""
    if not _want_cuda(part):
        return 'cpu'
    try:
        import sherpa_onnx
        ok = 'cuda' in str(getattr(sherpa_onnx, '__version__', ''))
    except Exception:          # noqa: BLE001
        ok = False
    if ok:
        os.environ.setdefault('CUDA_CACHE_MAXSIZE', '4294967296')     # 6.39：见 ort_providers
    if not ok and part not in _WARNED:
        _WARNED.add(part)
        print('提醒：设了用显卡念（%s），但装的 sherpa-onnx 不是显卡版（本地技能 04_gpu.sh 会装），这一路先用 CPU' % part, flush=True)
    return 'cuda' if ok else 'cpu'


def ort_providers(part='en'):
    """kokoro_clean.py（直接用 onnxruntime）的 providers"""
    if _want_cuda(part):
        try:
            import onnxruntime as ort
            if 'CUDAExecutionProvider' in ort.get_available_providers():
                # 6.39：句子长短每次不一样，onnxruntime 默认每遇到一种新长度就把卷积算法全试一遍（EXHAUSTIVE），用户电脑上英文 3 句要 43 秒（CPU 3 秒）。
                #   改成 HEURISTIC（直接挑），显存按需要申请；新显卡的 CUDA 程序第一次要现编译，缓存放大到 4 GB（默认 256 MB 装不下，每个进程都重新编译）
                os.environ.setdefault('CUDA_CACHE_MAXSIZE', '4294967296')
                return [('CUDAExecutionProvider', {'cudnn_conv_algo_search': 'HEURISTIC', 'arena_extend_strategy': 'kSameAsRequested',
                                                   'do_copy_in_default_stream': '1'}), 'CPUExecutionProvider']
        except Exception:      # noqa: BLE001
            pass
        if 'ort-' + part not in _WARNED:
            _WARNED.add('ort-' + part)
            print('提醒：设了用显卡念英文，但 onnxruntime 没有 CUDA，英文先用 CPU', flush=True)
    return ['CPUExecutionProvider']


def devices():
    return '声音克隆 %s；英文 %s；识别检查 %s' % (provider('zv'), provider('en'), provider('asr'))


def extra_tries():
    """6.36：整句用你的声音念（切换很快）的一句，要学的单词 4 遍都没听清，再多念几遍（只这一句，换一点语速），默认 8 遍；0 = 不多念"""
    v = os.environ.get('WORDFILM_EXTRA_TRIES', '')
    return max(0, int(v)) if v.strip().isdigit() else 8


def mix_fallback(plan=None):
    """6.36：上面多念了还是没听清，把这一句改成“中文你的声音、英文美式女声”拼接着念（和平常中英拼接一样）。
    6.37（第八十一版）起默认改（用户 2026-11-19：“一句多念了还是没听清时……改成女生念”）；
    plan.json 写 "mixFallback": false 或环境变量 WORDFILM_MIX_FALLBACK=0 才不改（照第七十七版的规矩标“没听清”）"""
    v = (plan or {}).get('mixFallback')
    if v is not None:
        return bool(v)
    return os.environ.get('WORDFILM_MIX_FALLBACK', '').strip().lower() not in ('0', 'no', 'false', 'off')
