#!/usr/bin/env python3
"""6.28（第七十版）音效库：全部用程序合成（不下载别人的录音，没有版权问题），第一次用时生成、缓存成 wav。
用户：“可以做一些音效，比如讲车子，可以有车子跑的声音，当然不要太长，不要影响主要的讲解，只是加深一下学生学习的印象；
演讲也可以来一句演讲，扬声器也可以播放一下声音”。
  python3 sfx.py --list            列出所有音效
  python3 sfx.py meow out.wav      生成一个听听
  get(name) -> np.float32（24 kHz，峰值 0.9，最长 1.6 秒）
名字也可以写 "say:Hello, everyone!"（一句英文，Kokoro 男声 am_michael，像演讲、广播里的人在说话）、"say:Good morning!|bf_emma"。"""
import os, sys, math, hashlib
import numpy as np
SR = 24000
CACHE = os.environ.get('WORDFILM_SFX', os.path.expanduser('~/wordfilm-models/sfx'))
MAXLEN = 1.6
R = np.random.default_rng(7)
def _t(d): return np.arange(int(d * SR)) / SR
def _env(n, a=0.005, r=0.08):
    e = np.ones(n); na = max(1, int(a * SR)); nr = max(1, int(r * SR))
    e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr); return e
def _lp(x, fc):
    from scipy.signal import butter, lfilter
    b, a = butter(2, min(0.99, fc / (SR / 2))); return lfilter(b, a, x)
def _hp(x, fc):
    from scipy.signal import butter, lfilter
    b, a = butter(2, fc / (SR / 2), 'high'); return lfilter(b, a, x)
def _bp(x, f1, f2):
    from scipy.signal import butter, lfilter
    b, a = butter(2, [f1 / (SR / 2), min(0.99, f2 / (SR / 2))], 'band'); return lfilter(b, a, x)
def _noise(d): return R.standard_normal(int(d * SR))
def _place(out, x, at):
    i = int(at * SR); n = min(len(x), len(out) - i)
    if n > 0: out[i:i + n] += x[:n]
    return out
def _bellnote(f, d, partials=((1, 1), (2.76, 0.5), (5.4, 0.25), (8.9, 0.12)), decay=4.0):
    t = _t(d); x = sum(a * np.sin(2 * np.pi * f * k * t) * np.exp(-t * decay * (1 + k * 0.3)) for k, a in partials)
    return x * _env(len(t), 0.002, 0.05)
# ---------------- 动物
def meow():
    d = 0.78; t = _t(d); n = len(t)
    u = t / d
    f0 = 520 + 300 * np.sin(np.pi * np.clip(u * 1.25, 0, 1)) ** 1.5 - 120 * np.clip((u - 0.6) / 0.4, 0, 1)
    f0 *= 1 + 0.012 * np.sin(2 * np.pi * 6 * t)
    F1 = np.interp(u, [0, 0.15, 0.5, 1], [350, 500, 950, 700]); F2 = np.interp(u, [0, 0.15, 0.5, 1], [2300, 2000, 1400, 1000])
    ph = 2 * np.pi * np.cumsum(f0) / SR
    x = np.zeros(n)
    for k in range(1, 18):
        fk = k * f0
        amp = (1 / k) * (np.exp(-((fk - F1) / 180) ** 2) * 1.0 + np.exp(-((fk - F2) / 260) ** 2) * 0.6 + 0.04)
        x += amp * np.sin(k * ph)
    x += 0.015 * _hp(_noise(d), 3000)
    e = np.interp(u, [0, 0.08, 0.7, 1], [0, 1, 0.8, 0]); return x * e
def purr():
    d = 1.2; t = _t(d); n = _lp(_noise(d), 400)
    return n * (0.6 + 0.4 * np.sin(2 * np.pi * 25 * t)) ** 2 * _env(len(t), 0.1, 0.3)
def lick():
    out = np.zeros(int(0.75 * SR))
    for k in range(3):
        b = _bp(_noise(0.06), 600, 2500) * np.exp(-_t(0.06) * 60)
        _place(out, b, 0.05 + k * 0.22)
    return out
def bird():
    out = np.zeros(int(1.0 * SR))
    for k, at in enumerate((0.0, 0.18, 0.5, 0.64)):
        d = 0.09; t = _t(d); f = np.linspace(3200, 4800, len(t)) if k % 2 == 0 else np.linspace(4600, 3000, len(t))
        _place(out, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) ** 2, at)
    return out
def dog():
    out = np.zeros(int(0.9 * SR))
    for at in (0.0, 0.38):
        d = 0.22; t = _t(d); f0 = np.interp(t, [0, 0.05, d], [380, 520, 300]); ph = 2 * np.pi * np.cumsum(f0) / SR
        x = sum((1 / k) * np.sin(k * ph) * np.exp(-((k * f0 - 900) / 500) ** 2) for k in range(1, 14)) + 0.15 * _bp(_noise(d), 500, 2500)
        _place(out, x * np.interp(t, [0, 0.02, 0.12, d], [0, 1, 0.7, 0]), at)
    return out
# ---------------- 交通、街上
def car():
    d = 1.5; t = _t(d); u = t / d
    f = 85 * (1.08 - 0.16 * np.tanh((u - 0.5) * 6))        # 开过去：先高后低（多普勒）
    ph = 2 * np.pi * np.cumsum(f) / SR
    eng = sum((1 / k) * np.sin(k * ph + k) for k in range(1, 10))
    tyre = _lp(_noise(d), 900) * 0.5
    e = np.exp(-((u - 0.5) / 0.22) ** 2); return (eng * 0.5 + tyre) * e
def horn():
    t = _t(0.42); x = np.sign(np.sin(2 * np.pi * 415 * t)) * 0.5 + np.sign(np.sin(2 * np.pi * 523 * t)) * 0.5
    return _lp(x, 2500) * _env(len(t), 0.01, 0.06)
def footsteps():
    out = np.zeros(int(1.3 * SR))
    for k in range(4):
        st = _lp(_noise(0.08), 700) * np.exp(-_t(0.08) * 50)
        sc = 0.4 * _hp(_noise(0.03), 2000) * np.exp(-_t(0.03) * 120)
        _place(out, st, 0.05 + k * 0.3); _place(out, sc, 0.05 + k * 0.3)
    return out
def wind():
    d = 1.5; t = _t(d); x = _bp(_noise(d), 250, 900)
    return x * (0.5 + 0.5 * np.sin(np.pi * t / d)) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.8 * t))
# ---------------- 铃、钟、提示音
def bell():          # 学校的电铃 / 火警铃：铃锤很快地敲
    d = 1.4; out = np.zeros(int(d * SR))
    for k in range(int(d * 22)):
        _place(out, _bellnote(2100, 0.25, ((1, 1), (1.47, 0.6), (2.09, 0.4)), 12) * 0.5, k / 22)
    return out * _env(len(out), 0.01, 0.2)
def alarmclock():    # 闹钟：叮铃铃——停——叮铃铃
    d = 1.5; out = np.zeros(int(d * SR))
    for k in range(int(d * 18)):
        if (k // 9) % 2 == 0:
            _place(out, _bellnote(2600, 0.15, ((1, 1), (1.6, 0.5)), 18) * 0.5, k / 18)
    return out
def dingdong():      # 广播、门铃：叮——咚
    out = np.zeros(int(1.5 * SR))
    _place(out, _bellnote(784, 1.0, ((1, 1), (2, 0.3), (3, 0.1)), 3), 0); _place(out, _bellnote(622, 1.0, ((1, 1), (2, 0.3), (3, 0.1)), 3), 0.45)
    return out
def ding():          # 一声清脆的“叮”（想到了、做完了、烤箱好了）
    return _bellnote(1760, 1.2, ((1, 1), (2.0, 0.35), (3.0, 0.12)), 3.2)
def sparkle():       # 亮晶晶（干净、镜子、魔法）
    out = np.zeros(int(1.0 * SR))
    for k, f in enumerate((2093, 2637, 3136, 3951, 3136)):
        _place(out, _bellnote(f, 0.5, ((1, 1), (2, 0.2)), 7) * 0.5, k * 0.08)
    return out
def beep():          # 电子按键“滴滴”（恒温器、空调遥控器）
    out = np.zeros(int(0.5 * SR))
    for at in (0.0, 0.2):
        t = _t(0.1); _place(out, np.sin(2 * np.pi * 1500 * t) * _env(len(t), 0.003, 0.01), at)
    return out
def notify():        # 手机来短信：上行两个音
    out = np.zeros(int(0.7 * SR))
    for at, f in ((0, 1318.5), (0.14, 1975.5)):
        _place(out, _bellnote(f, 0.45, ((1, 1), (2, 0.2)), 8), at)
    return out
def phonering():     # 老式电话铃
    d = 1.4; t = _t(d); x = _bellnote(1400, d, ((1, 1), (1.5, 0.5)), 0.6)
    gate = (np.sin(2 * np.pi * 20 * t) > 0) * ((t % 1.0) < 0.8); return x * gate
def tick():
    out = np.zeros(int(1.4 * SR))
    for k in range(4):
        _place(out, _hp(_noise(0.012), 2500) * (0.8 if k % 2 else 1.0), 0.05 + k * 0.33)
    return out
def shutter():       # 照相机快门：咔嚓
    out = np.zeros(int(0.35 * SR))
    for at, g in ((0.0, 1.0), (0.09, 0.7)):
        c = _bp(_noise(0.03), 1500, 6000) * np.exp(-_t(0.03) * 90); th = np.sin(2 * np.pi * 180 * _t(0.03)) * np.exp(-_t(0.03) * 80)
        _place(out, (c + 0.5 * th) * g, at)
    return out
def click():         # 锁、开关：咔哒
    out = np.zeros(int(0.3 * SR))
    for at, g in ((0.0, 1.0), (0.06, 0.6)):
        _place(out, (_bp(_noise(0.015), 2500, 8000) + 0.3 * np.sin(2 * np.pi * 900 * _t(0.015))) * np.exp(-_t(0.015) * 200) * g, at)
    return out
def knock():
    out = np.zeros(int(0.9 * SR))
    for k in range(3):
        x = np.sin(2 * np.pi * 160 * _t(0.09)) * np.exp(-_t(0.09) * 45) + 0.3 * _lp(_noise(0.09), 1200) * np.exp(-_t(0.09) * 60)
        _place(out, x, 0.03 + k * 0.22)
    return out
def keys():
    out = np.zeros(int(0.8 * SR))
    for k in range(7):
        _place(out, _bellnote(R.uniform(3000, 5200), 0.2, ((1, 1), (1.7, 0.4)), 25) * 0.4, k * 0.07 + R.uniform(0, 0.03))
    return out
# ---------------- 水、家里
def water():         # 水龙头、淋浴哗哗
    d = 1.5; t = _t(d); x = _bp(_noise(d), 800, 6000) * (0.85 + 0.15 * _lp(_noise(d), 8))
    return x * np.interp(t, [0, 0.15, d - 0.3, d], [0, 1, 1, 0])
def drip():
    out = np.zeros(int(1.0 * SR))
    for at in (0.0, 0.45):
        d = 0.08; t = _t(d); f = np.linspace(700, 1700, len(t))
        _place(out, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 45), at)
    return out
def whoosh():        # 空调吹风、东西飞过去
    d = 1.0; t = _t(d); x = _noise(d); fc = np.interp(t, [0, 0.5, d], [400, 2500, 600])
    y = np.zeros_like(x)
    for i in range(0, len(x), 240):
        y[i:i + 240] = _bp(x[i:i + 240 + 200], max(200, fc[i] * 0.6), fc[i] * 1.4)[:len(y[i:i + 240])]
    return y * np.sin(np.pi * t / d) ** 2
def sizzle():        # 锅里煎东西、烤箱里滋滋
    d = 1.3; t = _t(d); x = _hp(_noise(d), 3000) * (0.6 + 0.4 * (R.random(len(t)) > 0.97))
    return x * _env(len(t), 0.1, 0.3)
def heartbeat():
    out = np.zeros(int(1.4 * SR))
    for at in (0.0, 0.7):
        for dt, g in ((0, 1.0), (0.18, 0.7)):
            _place(out, np.sin(2 * np.pi * 55 * _t(0.12)) * np.exp(-_t(0.12) * 30) * g, at + dt)
    return out
def cough():
    out = np.zeros(int(0.9 * SR))
    for at in (0.0, 0.35):
        d = 0.22; x = _bp(_noise(d), 400, 3000) * np.interp(_t(d), [0, 0.01, 0.06, d], [0, 1, 0.5, 0])
        _place(out, x, at)
    return out
def cash():          # 收银机：叮 + 抽屉
    out = np.zeros(int(1.2 * SR)); _place(out, _lp(_noise(0.15), 1500) * np.exp(-_t(0.15) * 20) * 0.6, 0)
    _place(out, _bellnote(2349, 1.0, ((1, 1), (2.4, 0.3)), 4), 0.12); return out
# ---------------- 声音、音乐
def music():         # 音箱里放的一小段音乐（拨弦，C 大调上行）
    out = np.zeros(int(1.6 * SR)); notes = (523.3, 659.3, 784.0, 1046.5, 784.0, 1046.5)
    for k, f in enumerate(notes):
        d = 0.5; t = _t(d); x = (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(4 * np.pi * f * t) + 0.15 * np.sin(6 * np.pi * f * t)) * np.exp(-t * 7)
        _place(out, x * 0.6, k * 0.2)
    bass = np.sin(2 * np.pi * 130.8 * _t(1.2)) * np.exp(-_t(1.2) * 2) * 0.4; _place(out, bass, 0)
    return out
def drum():
    out = np.zeros(int(1.0 * SR))
    for k, at in enumerate((0.0, 0.25, 0.5, 0.62)):
        d = 0.3; t = _t(d); f = np.interp(t, [0, d], [140, 70]); x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14) + 0.2 * _lp(_noise(d), 3000) * np.exp(-t * 40)
        _place(out, x, at)
    return out
def applause():
    d = 1.5; out = np.zeros(int(d * SR))
    for k in range(160):
        _place(out, _bp(_noise(0.02), 800, 5000) * np.exp(-_t(0.02) * 150) * R.uniform(0.3, 1), R.uniform(0, d - 0.05))
    return out * np.interp(_t(d), [0, 0.1, d - 0.4, d], [0, 1, 1, 0])
def pop():
    t = _t(0.12); f = np.linspace(900, 300, len(t)); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 35)
def boing():
    t = _t(0.6); f = 220 + 160 * np.exp(-t * 6) * np.sin(2 * np.pi * 9 * t); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5)
def thud():
    t = _t(0.4); return (np.sin(2 * np.pi * np.cumsum(np.linspace(90, 40, len(t))) / SR) + 0.5 * _lp(_noise(0.4), 500)) * np.exp(-t * 12)
def rocks():          # 石头滚落：几下闷响 + 碎石
    out = np.zeros(int(1.3 * SR))
    for k in range(9):
        _place(out, thud() * R.uniform(0.3, 1), R.uniform(0, 0.9))
    return out
def waves():         # 海浪拍岸：哗——
    d = 1.6; t = _t(d); x = _lp(_noise(d), 1800) * 0.7 + _bp(_noise(d), 1500, 6000) * 0.3
    return x * np.interp(t, [0, 0.35, 0.6, d], [0.05, 1, 0.7, 0])
def splash():        # 石子落水：扑通
    out = np.zeros(int(0.8 * SR)); t = _t(0.25)
    _place(out, np.sin(2 * np.pi * np.cumsum(np.linspace(260, 120, len(t))) / SR) * np.exp(-t * 18), 0)
    _place(out, _bp(_noise(0.5), 800, 5000) * np.exp(-_t(0.5) * 9) * 0.6, 0.02); return out
def rain():          # 下阵雨：沙沙
    d = 1.6; t = _t(d); x = _bp(_noise(d), 1200, 8000) * 0.5
    for k in range(60):
        _place(x, _hp(_noise(0.01), 3000) * R.uniform(0.3, 1), R.uniform(0, d - 0.02))
    return x * np.interp(t, [0, 0.2, d - 0.3, d], [0, 1, 1, 0])
def thunder():
    d = 1.6; t = _t(d); return _lp(_noise(d), 300) * np.interp(t, [0, 0.05, 0.3, d], [0, 1, 0.6, 0]) * (1 + 0.5 * np.sin(2 * np.pi * 3 * t))
LIB = {f.__name__: f for f in (meow, purr, lick, bird, dog, car, horn, footsteps, wind, bell, alarmclock, dingdong, ding, sparkle, beep, notify, phonering,
                               tick, shutter, click, knock, keys, water, drip, whoosh, sizzle, heartbeat, cough, cash, music, drum, applause, pop, boing, thud, rocks, waves, splash, rain, thunder)}
VOICES = {'am_michael': 16, 'am_adam': 11, 'bf_emma': 21, 'af_heart': 3, 'af_bella': 2}
def _say(text, voice='am_michael'):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import kokoro_clean
    x = kokoro_clean.speak(text, sid=VOICES.get(voice, 16), speed=1.0)
    x = np.asarray(x[0] if isinstance(x, tuple) else x, dtype=np.float64)
    # 像在礼堂、广播里：加一点混响
    ir = np.zeros(int(0.25 * SR)); ir[0] = 1
    for k in range(1, 7): ir[int(k * 0.035 * SR)] = 0.45 ** k
    return np.convolve(x, ir)[:len(x) + int(0.2 * SR)]
def get(name):
    """音效 → float32 数组（峰值 0.9；说话的不截短，其余最长 1.6 秒，尾巴淡出）"""
    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.md5(name.encode('utf-8')).hexdigest()[:10]
    fn = os.path.join(CACHE, ('say_' if name.startswith('say:') else name + '_') + key + '.wav')
    import soundfile as sf
    if os.path.exists(fn):
        return sf.read(fn, dtype='float32')[0]
    if name.startswith('say:'):
        text, _, voice = name[4:].partition('|'); x = _say(text.strip(), voice.strip() or 'am_michael')
    else:
        if name not in LIB:
            raise KeyError('没有这个音效：%s（python3 sfx.py --list 看有哪些）' % name)
        x = np.asarray(LIB[name](), dtype=np.float64)
        n = int(MAXLEN * SR)
        if len(x) > n:
            x = x[:n]; x[-int(0.15 * SR):] *= np.linspace(1, 0, int(0.15 * SR))
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.9
    sf.write(fn, x.astype(np.float32), SR)
    return sf.read(fn, dtype='float32')[0]      # 6.37：第一次用也读存好的（16 位），和以后每次一样——以前第一次用的那一下和以后差一点点
if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] == '--list':
        print('音效：' + '、'.join(LIB)); print('说话：say:英文句子（默认 am_michael 男声，|bf_emma 换声音）')
    else:
        import soundfile as sf
        sf.write(sys.argv[2] if len(sys.argv) > 2 else sys.argv[1].replace(':', '_') + '.wav', get(sys.argv[1]), SR)
