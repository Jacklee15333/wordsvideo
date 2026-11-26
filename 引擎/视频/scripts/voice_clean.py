"""声音清理（5.3 起）：参考录音降噪；合成出来的句子去底噪、压刺耳高频。只用 numpy、scipy、noisereduce。"""
import numpy as np
from scipy.signal import butter, sosfilt, sosfiltfilt


def noise_sample(x, sr, frac=0.12):
    """录音里最安静的 12% 小片段拼起来，当作底噪样本"""
    k = int(0.03 * sr)
    fr = [x[i:i + k] for i in range(0, len(x) - k, k)]
    e = np.array([np.sqrt(np.mean(f ** 2)) for f in fr])
    idx = np.argsort(e)[:max(8, int(len(fr) * frac))]
    return np.concatenate([fr[i] for i in sorted(idx)]).astype(np.float32)


def hpf(x, sr, fc=70):
    """去掉 70 Hz 以下的嗡声、桌面震动"""
    return sosfiltfilt(butter(4, fc, 'highpass', fs=sr, output='sos'), x).astype(np.float32)


def denoise(x, sr, noise=None, amount=0.85, stationary=True):
    """谱减降噪（noisereduce）。noise：底噪样本；不给就按非平稳方式自己估"""
    import noisereduce as nr
    kw = dict(y=x, sr=sr, prop_decrease=amount, n_fft=1024, freq_mask_smooth_hz=300, time_mask_smooth_ms=60,
              stationary=stationary)
    if noise is not None:
        kw['y_noise'] = noise
    return hpf(nr.reduce_noise(**kw).astype(np.float32), sr)


def high_shelf(x, sr, f0=7000.0, gain_db=-4.0, q=0.7):
    """高架滤波（RBJ）：f0 以上整体降 gain_db，刺耳的电流声、齿音柔和一点"""
    A = 10 ** (gain_db / 40)
    w = 2 * np.pi * f0 / sr
    alpha = np.sin(w) / (2 * q)
    c = np.cos(w)
    b0 = A * ((A + 1) + (A - 1) * c + 2 * np.sqrt(A) * alpha)
    b1 = -2 * A * ((A - 1) + (A + 1) * c)
    b2 = A * ((A + 1) + (A - 1) * c - 2 * np.sqrt(A) * alpha)
    a0 = (A + 1) - (A - 1) * c + 2 * np.sqrt(A) * alpha
    a1 = 2 * ((A - 1) - (A + 1) * c)
    a2 = (A + 1) - (A - 1) * c - 2 * np.sqrt(A) * alpha
    sos = np.array([[b0 / a0, b1 / a0, b2 / a0, 1.0, a1 / a0, a2 / a0]])
    if len(x) == 0:
        return np.zeros(0, np.float32)
    return sosfilt(sos, x).astype(np.float32)


def lpf(x, sr, fc=10500):
    """10.5 kHz 以上（声码器最容易出“沙沙”“滋滋”假音的地方）切掉"""
    if len(x) < 64:
        return np.asarray(x, np.float32)
    return sosfiltfilt(butter(6, fc, 'lowpass', fs=sr, output='sos'), x).astype(np.float32)



def pitch_shape(x, sr, target=230.0):
    """一段声音的音高走向（相对 target 的半音）：rng 起伏范围、start 开头、end 结尾、med 中位、vd 有声多长；清辅音（没有音高）返回 None"""
    try:
        import parselmouth
    except ImportError:
        return None
    import numpy as np
    if len(x) < int(0.08 * sr):
        return None
    p = parselmouth.Sound(x.astype(np.float64), sr).to_pitch(time_step=0.01, pitch_floor=120, pitch_ceiling=450)
    f = p.selected_array['frequency']
    v = np.where(f > 0)[0]
    if len(v) < 4:
        return None
    st = 12 * np.log2(f[v] / target)
    return dict(rng=float(np.percentile(st, 95) - np.percentile(st, 5)), start=float(st[:3].mean()), end=float(st[-3:].mean()),
                med=float(np.median(st)), vd=len(v) * 0.01)


def syllable_cost(x, sr):
    """单独念的一个音节自不自然（越小越好）：音高别乱跳（起伏 4 个半音以内）、别太高太低（中位离 230 Hz 两个半音以内）、
    像老师念一个音节那样平着或轻轻往下落（不往上翘、也别一下掉七八个半音）、元音别拖（有声 0.22～0.45 秒）"""
    dur = len(x) / sr
    if dur < 0.12:
        return 99.0
    s = pitch_shape(x, sr)
    if s is None:                                   # 清辅音块（s、t）：只看长短
        return 1.0 + abs(dur - 0.3) * 4
    d = s['end'] - s['start']
    return (max(0.0, s['rng'] - 4) + max(0.0, abs(s['med']) - 2) * 0.8 + max(0.0, d - 0.5) * 0.8 + max(0.0, -6 - d) * 0.6
            + max(0.0, s['vd'] - 0.45) * 8 + max(0.0, 0.22 - s['vd']) * 8 + max(0.0, dur - 0.75) * 3)


def flatten_syllable(x, sr, keep=0.5, target=230.0, maxshift=4.0, fall=-3.0):
    """（备选，默认不用）把音节块的音高拉平一些：起伏只留一半，整体靠到 230 Hz（最多挪 4 个半音），轻轻往下落 3 个半音。
    用 Praat 的 PSOLA（parselmouth）改音高，不改音色；但会带一点加工的毛刺（DNSMOS 低 0.2～0.3），所以默认不开：
    voice_config.SYL_FLATTEN = True 才用"""
    try:
        import parselmouth
        from parselmouth.praat import call
    except ImportError:
        return x
    import numpy as np
    snd = parselmouth.Sound(x.astype(np.float64), sr)
    dur = snd.get_total_duration()
    man = call(snd, 'To Manipulation', 0.01, 120, 450)
    pt = call(man, 'Extract pitch tier')
    n = call(pt, 'Get number of points')
    if n < 4:
        return x
    T = np.array([call(pt, 'Get time from index', i + 1) for i in range(n)])
    F = np.array([call(pt, 'Get value at index', i + 1) for i in range(n)])
    st = 12 * np.log2(F / np.median(F))
    med = np.median(F)
    shift = np.clip(12 * np.log2(target / med), -maxshift, maxshift)
    u = (T - T[0]) / max(1e-3, T[-1] - T[0])
    trend = 1.0 + (fall - 1.0) * u
    new = med * 2 ** ((shift + trend + keep * (st - np.median(st))) / 12)
    call(pt, 'Remove points between', 0, dur)
    for t, f in zip(T, new):
        call(pt, 'Add point', float(t), float(f))
    call([pt, man], 'Replace pitch tier')
    return np.array(call(man, 'Get resynthesis (overlap-add)').values[0], dtype=np.float32)


def gate(x, sr, depth_db=-20.0):
    """6.44：静音门——字和字、句子前后的停顿里只剩底噪的地方压低 20 dB（提前 20 ms 打开、慢慢 100 ms 关上，不切字尾）。
    门限：最静的 15% 再高 8 dB，和最响的往下 42 dB，取高的。"""
    x = np.asarray(x, dtype=np.float32)
    fr = int(0.01 * sr)
    n = len(x) // fr
    if n < 5:
        return x
    e = np.sqrt(np.mean(x[:n * fr].reshape(n, fr) ** 2, axis=1)) + 1e-9
    db = 20 * np.log10(e)
    thr = max(np.percentile(db, 15) + 8, np.max(db) - 42)
    g = np.where(db > thr, 1.0, 10 ** (depth_db / 20))
    for i in range(1, n):
        if g[i] < g[i - 1]:
            g[i] = max(g[i], g[i - 1] * 0.9)
    for i in range(n - 2, -1, -1):
        g[i] = max(g[i], g[i + 1] * 0.6)
    gs = np.repeat(g, fr)
    gs = np.concatenate([gs, np.full(len(x) - len(gs), gs[-1])])
    return (x * gs).astype(np.float32)


def match_eq(x, sr, bands, taps=1023):
    """6.46：音色校正——把合成出来的声音的高低音比例往真人录音（仓库「素材/音色」）上靠。
    bands：[(中心频率 Hz, 增益 dB)]，在对数频率上连成一条线；线性相位 FIR，不挪时间；做完音量调回原来那么响。"""
    from scipy.signal import firwin2
    x = np.asarray(x, dtype=np.float32)
    if not bands or len(x) < taps:
        return x
    fs, gs = [b[0] for b in bands], [b[1] for b in bands]
    grid = np.linspace(0, sr / 2, 1025)
    gi = np.interp(np.log10(np.maximum(grid, 20.0)), np.log10(fs), gs)        # 两头按最边上的那一档
    h = firwin2(taps, grid, 10 ** (gi / 20.0), fs=sr)
    y = np.convolve(x, h, mode='same').astype(np.float32)
    r0, r1 = float(np.sqrt(np.mean(x ** 2))), float(np.sqrt(np.mean(y ** 2)))
    return (y * (r0 / r1) if r1 > 1e-9 else y).astype(np.float32)


def _last_syllable(x, sr):
    """最后一个字：从最后一个能量低谷（比全句最响低 12 dB 以上）到声音落到全句最响 -30 dB 的地方。返回 (开头, 结尾) 样本号"""
    fr = int(0.01 * sr)
    n = len(x) // fr
    if n < 12:
        return None
    e = 20 * np.log10(np.sqrt((x[:n * fr].reshape(n, fr) ** 2).mean(1)) + 1e-9)
    end = np.where(e > e.max() - 30)[0][-1]
    es = np.convolve(e, np.ones(3) / 3, 'same')
    i = end - 5
    while i > 5 and not (es[i] < es[i - 1] and es[i] < es[i + 1] and es[i] < e.max() - 12):
        i -= 1
    return max(0, i) * fr, (end + 1) * fr


def final_rough(x, sr):
    """6.49：最后一个字后一半“发颤”的分数——周期乱（%）+ 3 ×（一顿一顿的 dB − 0.7）。
    实测（同六句话念多遍）：多数句子 0～2，发颤的 3 以上（约两成），最怪的 13、27。0 = 量不出来"""
    x = np.asarray(x, dtype=np.float32)
    ab = _last_syllable(x, sr)
    if not ab:
        return 0.0
    a, b = ab
    seg = x[a + (b - a) // 2:b]
    fr, hop = int(0.03 * sr), int(0.005 * sr)
    if len(seg) < fr + 4 * hop:
        return 0.0
    per, amp = [], []
    lo, hi = int(sr / 350), int(sr / 60)
    for i in range(0, len(seg) - fr, hop):
        w = seg[i:i + fr]
        r = float(np.sqrt(np.mean(w ** 2)))
        if r < 1e-3:
            continue
        ac = np.correlate(w, w, 'full')[fr - 1:]
        ac = ac / (ac[0] + 1e-9)
        k = lo + int(np.argmax(ac[lo:hi]))
        if ac[k] > 0.4:
            per.append(k)
            amp.append(r)
    if len(per) < 4:
        return 0.0
    per, amp = np.array(per, float), np.array(amp)
    jit = float(np.median(np.abs(np.diff(per)) / per[1:]) * 100)
    shim = float(np.median(np.abs(np.diff(20 * np.log10(amp + 1e-9)))))
    return jit + 3 * max(0.0, shim - 0.7)


def tail_tame(x, sr, drop_db=12.0, fade_ms=80):
    """6.49：最后一个字念到尾巴上会发颤（实测后一半的周期乱比前一半高一倍多）：从最后一个字最响的地方往后，
    落下 drop_db 的地方开始升余弦淡出 fade_ms，后面静音（长度不变）"""
    x = np.asarray(x, dtype=np.float32)
    fr = int(0.01 * sr)
    n = len(x) // fr
    if n < 12:
        return x
    e = 20 * np.log10(np.sqrt((x[:n * fr].reshape(n, fr) ** 2).mean(1)) + 1e-9)
    end = np.where(e > e.max() - 30)[0][-1]
    a = max(0, end - 25)
    pk = a + int(np.argmax(e[a:end + 1]))
    after = np.where(e[pk:end + 1] < e[pk] - drop_db)[0]
    if not len(after):
        return x
    s = (pk + int(after[0])) * fr
    k = min(int(fade_ms / 1000 * sr), len(x) - s)
    y = x.copy()
    if k > 1:
        y[s:s + k] *= (0.5 + 0.5 * np.cos(np.linspace(0, np.pi, k))).astype(np.float32)
    y[s + k:] = 0
    return y
