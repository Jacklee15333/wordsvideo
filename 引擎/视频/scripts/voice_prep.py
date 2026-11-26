#!/usr/bin/env python3
"""把一段录音做成配音用的“参考声音”（5.3 起）：降噪、挑一段 6～10 秒的完整句子、听写出文字。

  python3 voice_prep.py 录音.mp3                       # 自动挑一段
  python3 voice_prep.py 录音.mp3 --start 6.1 --end 14.6  # 自己指定从第几秒到第几秒
  python3 voice_prep.py 录音1.mp3 录音2.mp3 --test "前缀是 trans，来自拉丁语，意思是：到另一边。"
  python3 voice_prep.py 长录音.m4a --start 154.3 --end 158.5 --role translate   # 再加一段“念例句翻译”的参考（5.5 起）

5.5 起参考录音可以有几段，按句子的用处挑：不写 --role 是讲解（ref.wav），--role translate 念例句的中文翻译，
--role question 问句。几段最好出自同一次录音（音色一样）。长录音（几分钟的讲课）自动挑讲解那段时，
会挑没有“呃、嗯、啊”、不夹英文的一段（英文现在由英文声音念，参考录音里不需要英文）。

写到 ~/wordfilm-voice（或 --out）：ref.wav（参考片段）、ref.txt（片段里说的话）、noise.wav（录音的底噪样本，合成后降噪用）。
6.45 起 synth.py 先用技能的 assets/voice（仓库里的声音），~/wordfilm-voice 排在后面：做好的三个文件要放进技能的 assets/voice/ 才生效（或者设 WORDFILM_VOICE）。

录音要求：只有一个人说话，安静的屋子，离麦克风一拳多远（别顶满音量），语气就用讲课的语气——合成出来的语气会跟着参考录音走。
ref.txt 必须和录音一字不差：识别模型偶尔会听错，打印出来以后对着录音核一遍，有错就直接改 ref.txt。
"""
import argparse
import os
import re
import subprocess
import sys

import numpy as np
import soundfile as sf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voice_config as VC  # noqa: E402

SR = 24000


def load(path):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float32).copy()


def zh_digits(t):
    """参考文字里的阿拉伯数字写成汉字（“20个” → “二十个”）：声音克隆的分词不认数字，对不上会念歪"""
    d = '零一二三四五六七八九'

    def one(m):
        n = int(m.group(0))
        if n < 10:
            return d[n]
        if n < 100:
            return ('' if n // 10 == 1 else d[n // 10]) + '十' + ('' if n % 10 == 0 else d[n % 10])
        if n < 1000:
            h, r = divmod(n, 100)
            return d[h] + '百' + ('' if r == 0 else '零' + d[r] if r < 10 else d[r // 10] + '十' + ('' if r % 10 == 0 else d[r % 10]))
        return ''.join(d[int(c)] for c in m.group(0))      # 年份这类：二零二六
    return re.sub(r'\d+', one, t)


def phrases(x, gap=0.18, floor_db=-35):
    """按停顿切成一句一句：(开始秒, 结束秒)"""
    k = int(0.02 * SR)
    e = np.array([np.sqrt(np.mean(x[j:j + k] ** 2)) for j in range(0, len(x) - k, k)]) + 1e-9
    loud = 20 * np.log10(e / e.max()) > floor_db
    out, start, run = [], None, 0
    for i, v in enumerate(loud):
        if v:
            start = i if start is None else start
            run = 0
        elif start is not None:
            run += 1
            if run * 0.02 >= gap:
                out.append((start * 0.02, (i - run + 1) * 0.02))
                start = None
    if start is not None:
        out.append((start * 0.02, len(loud) * 0.02))
    return [(a, b) for a, b in out if b - a >= 0.4]


def windows(ph, lo=5.5, hi=10.0, want=7.5):
    """连着的几句凑成 5.5～10 秒的段落，按接近 7.5 秒排好"""
    out = []
    for i in range(len(ph)):
        for j in range(i, len(ph)):
            a, b = ph[i][0], ph[j][1]
            if b - a > hi:
                break
            if b - a >= lo:
                out.append((abs(b - a - want), a, b))
    return [(a, b) for _, a, b in sorted(out)]


def pick(x, ph, transcribe, tries=40):
    """挑一段说得顺的：听写出来没有口头语、不夹英文、没有数字的最好"""
    best = None
    for a, b in windows(ph)[:tries]:
        t = transcribe(x[int(a * SR):int(b * SR)])
        bad = 3 * len(re.findall('[呃嗯啊哦]', t)) + 2 * len(re.findall('[A-Za-z]+', t)) + len(re.findall(r'\d', t))
        if best is None or bad < best[0]:
            best = (bad, (a, b))
        if bad == 0:
            break
    return best[1] if best else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('audio', nargs='+')
    ap.add_argument('--start', type=float)
    ap.add_argument('--end', type=float)
    ap.add_argument('--out', default=os.path.expanduser('~/wordfilm-voice'))
    ap.add_argument('--test', help='做好后用新声音念这一句，存成 test.wav 听听')
    ap.add_argument('--role', choices=['translate', 'question'], help='这一段是“念例句翻译”或“问句”用的参考（不写就是讲解用的）')
    a = ap.parse_args()
    from voice_clean import noise_sample, denoise
    xs = [load(p) for p in a.audio]
    noise = np.concatenate([noise_sample(x, SR) for x in xs])[:8 * SR]      # 底噪样本 8 秒够用
    x = denoise(xs[0], SR, noise)                       # 参考片段取第一段录音
    import synth
    if a.start is not None and a.end is not None:
        seg = (a.start, a.end)
    else:
        seg = pick(xs[0], phrases(xs[0]), lambda y: synth.transcribe_array(y, SR))
        if not seg:
            raise SystemExit('第一段录音里找不到 6～10 秒连着说的话：录长一点（15 秒以上），或者用 --start --end 指定')
    lo, hi = max(0, seg[0] - 0.06), min(len(x) / SR, seg[1] + 0.06)
    y = x[int(lo * SR):int(hi * SR)].copy()
    f = int(0.03 * SR)
    y[:f] *= np.linspace(0, 1, f)
    y[-f:] *= np.linspace(1, 0, f)
    y = np.clip(y / (np.sqrt(np.mean(y ** 2)) + 1e-9) * 0.08, -0.99, 0.99).astype(np.float32)
    os.makedirs(a.out, exist_ok=True)
    base = 'ref' if not a.role else 'ref_' + a.role
    sf.write(os.path.join(a.out, base + '.wav'), y, SR)
    if not a.role or not os.path.exists(os.path.join(a.out, 'noise.wav')):
        sf.write(os.path.join(a.out, 'noise.wav'), noise.astype(np.float32), SR)
    text = zh_digits(synth.transcribe_array(y, SR).strip())
    open(os.path.join(a.out, base + '.txt'), 'w', encoding='utf-8').write(text + '\n')
    print('参考片段：第 %.1f～%.1f 秒（%.1f 秒） -> %s' % (lo, hi, hi - lo, a.out))
    print('听写出来的文字（必须和录音一字不差，有错就改 %s.txt）：\n  ' % base + text)
    if re.search('[呃嗯啊]', text):
        print('提醒：这一段有“呃、嗯、啊”这类口头语，合成时也会被学过去；最好用 --start --end 换一段说得顺的')
    if a.test:
        os.environ['WORDFILM_VOICE'] = a.out
        out = synth.say(a.test, scene='example' if a.role == 'translate' else '')
        sf.write(os.path.join(a.out, 'test.wav'), out, SR)
        print('试念：%s -> %s\n  听成：%s' % (a.test, os.path.join(a.out, 'test.wav'), synth.transcribe_array(out, SR)))


if __name__ == '__main__':
    main()
