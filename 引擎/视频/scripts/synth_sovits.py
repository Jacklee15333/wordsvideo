#!/usr/bin/env python3
"""用本机的 GPT-SoVITS（api_v2.py）按配音稿合成配音，输出和 synth.py 一模一样（每句一个 24 kHz wav + manifest.json），
render.py / run.py 不用改。放在技能的 scripts/ 文件夹里，和 synth.py 放一起。

先在 GPT-SoVITS 文件夹里开 API（和 WebUI 不是同一个端口）：
    runtime\\python.exe api_v2.py -a 127.0.0.1 -p 9880 -c GPT_SoVITS/configs/tts_infer.yaml
再：
    python synth_sovits.py plan.json 输出文件夹 --ref 我的参考.wav --ref-text "参考音频里说的话"

  讲解句、例句：GPT-SoVITS（有中文的句子 text_lang=zh，中英混读；纯英文句子 text_lang=en）
  只念音节块的句子（qzca 这种音素词）：仍用 Kokoro 38 号（synth.py 那一套，读得准）
  每一句都用 SenseVoice 听一遍，英文词没听清就换个随机种子重念，最多 4 遍，留最好的一遍——规矩和 synth.py 一样。
  --fallback：4 遍都不行的句子改用 Kokoro 38 号念。
  微调过自己的模型：加 --gpt-weights xxx.ckpt --sovits-weights xxx.pth（路径相对 GPT-SoVITS 文件夹）。
"""
import argparse, io, json, os, re, sys, urllib.parse, urllib.request
import numpy as np
import soundfile as sf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import synth  # noqa: E402  Kokoro（音节块）、SenseVoice 识别、检查规则都用它的

SR = 24000
CJK = re.compile(r'[\u3400-\u9fff]')


def api(base, path, payload=None):
    if payload is None:
        with urllib.request.urlopen(base + path, timeout=60) as r:
            return r.read()
    req = urllib.request.Request(base + path, data=json.dumps(payload).encode('utf-8'),
                                 headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        raise RuntimeError('GPT-SoVITS 报错：%s' % e.read().decode('utf-8', 'ignore'))


def to24k(x, sr):
    if x.ndim > 1:
        x = x.mean(1)
    if sr == SR:
        return x.astype(np.float32)
    from math import gcd
    from scipy.signal import resample_poly
    g = gcd(sr, SR)
    return resample_poly(x, SR // g, sr // g).astype(np.float32)


def sovits(a, text, seed):
    body = {
        'text': text,
        'text_lang': 'zh' if CJK.search(text) else 'en',
        'ref_audio_path': os.path.abspath(a.ref),
        'prompt_text': a.ref_text,
        'prompt_lang': a.ref_lang,
        'text_split_method': 'cut0',      # 配音稿已经一句一句分好了，不再切
        'batch_size': 1,
        'speed_factor': a.speed,
        'seed': seed,
        'top_k': a.top_k, 'top_p': 1, 'temperature': a.temperature,
        'media_type': 'wav', 'streaming_mode': False,
    }
    x, sr = sf.read(io.BytesIO(api(a.url, '/tts', body)), dtype='float32')
    return to24k(x, sr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('plan')
    ap.add_argument('out')
    ap.add_argument('--ref', required=True, help='参考音频（3～10 秒，你自己的声音）')
    ap.add_argument('--ref-text', required=True, help='参考音频里说的话，一字不差')
    ap.add_argument('--ref-lang', default='zh')
    ap.add_argument('--url', default='http://127.0.0.1:9880')
    ap.add_argument('--speed', type=float, default=1.0)
    ap.add_argument('--temperature', type=float, default=1.0)
    ap.add_argument('--top-k', type=int, default=15)
    ap.add_argument('--gpt-weights')
    ap.add_argument('--sovits-weights')
    ap.add_argument('--fallback', action='store_true', help='4 遍都没听清的句子改用 Kokoro 38 号')
    a = ap.parse_args()

    if a.gpt_weights:
        api(a.url, '/set_gpt_weights?weights_path=' + urllib.parse.quote(a.gpt_weights))
    if a.sovits_weights:
        api(a.url, '/set_sovits_weights?weights_path=' + urllib.parse.quote(a.sovits_weights))

    plan = json.load(open(a.plan, encoding='utf-8'))
    os.makedirs(a.out, exist_ok=True)
    sid, kspeed = int(plan.get('voice', 38)), float(plan.get('speed', 0.95))
    lex = dict(plan.get('lexicon') or {})
    lex.update(synth.inflect_lex(plan, lex))
    if lex:                                   # 音素词（qzca）给 Kokoro 用
        lp = os.path.join(a.out, 'lexicon-plan.txt')
        with open(lp, 'w', encoding='utf-8') as fh:
            for k, v in lex.items():
                fh.write('%s %s\n' % (str(k).lower(), ' '.join(str(v).split())))
        synth.EXTRA_LEX.insert(0, lp)
    known = {str(k).lower() for k in lex}
    word = str(plan.get('word', ''))

    manifest, flagged = {}, []
    for scene, spec in plan['scenes'].items():
        items = ([('intro', spec['intro'])] if spec.get('intro') else []) + [('seg%d' % i, t) for i, t in enumerate(spec['segs'])]
        manifest[scene] = []
        for name, seg in items:
            text = str(seg.get('t', '')) if isinstance(seg, dict) else str(seg)
            phon = bool(synth.PHON_ONLY.match(text))
            # GPT-SoVITS 不认音素词：句子里夹着整词音素词（“连起来：qzcamera。”）就换回原词
            say = re.sub(r'qz([a-z]+)', lambda m: m.group(1) if len(m.group(1)) > 3 else m.group(0), text)
            best, engine = None, 'kokoro' if phon else 'sovits'
            for attempt in range(1 if phon else 4):
                if phon:
                    x = synth.trim(synth.gen(text, sid, kspeed))
                else:
                    x = sovits(a, say, seed=1234 + attempt * 101)
                x = x / (np.sqrt(np.mean(x ** 2)) + 1e-9) * 0.08
                heard = synth.transcribe_array(x, SR)
                miss, warn = synth.check(text, heard, word, known=known)
                zh = synth.zh_mismatch(text, heard)
                score = (len(miss), zh, len(warn))
                if best is None or score < best[0]:
                    best = (score, x, heard, miss, warn, zh, attempt)
                if not miss and not zh and not warn:
                    break
            _, x, heard, miss, warn, zh, attempt = best
            if miss and a.fallback and not phon:
                x = synth.gen(say, sid, kspeed)
                x = x / (np.sqrt(np.mean(x ** 2)) + 1e-9) * 0.08
                heard = synth.transcribe_array(x, SR)
                miss, warn = synth.check(text, heard, word, known=known)
                engine = 'kokoro（退回）'
            if zh:
                warn = warn + ['中文对不上']
            path = os.path.join(a.out, '%s_%s.wav' % (scene, name))
            sf.write(path, x, SR)
            manifest[scene].append({'name': name, 'path': path, 'dur': round(len(x) / SR, 3), 'text': text,
                                    'heard': heard, 'miss': miss, 'warn': warn, 'engine': engine})
            print('%-8s %-5s %5.2fs [%s] %s%s' % (scene, name, len(x) / SR, engine, heard,
                                                  ('   <-- 没听清：' + ','.join(miss)) if miss else ''), flush=True)
            if miss:
                flagged.append(text)
    json.dump(manifest, open(os.path.join(a.out, 'manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('\n%d 句有要学的单词没听清' % len(flagged))


if __name__ == '__main__':
    main()
