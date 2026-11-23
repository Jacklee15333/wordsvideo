#!/usr/bin/env python3
"""试几种说法（5.1 起）：每一句合成一遍、用识别模型听一遍，打印听成了什么、要学的单词听没听清。
配音稿里有句子“没听清”时，先用它试几种说法，挑听得清的写进 prefs / plan.json，再正式跑（省得一遍遍重跑整段视频）。

  python3 saytest.py thermostat "连起来：thermostat。" "连起来，就读 thermostat。"
  python3 saytest.py product "…也叫 product，就是产品。" "…也叫 product，意思是产品。"
  python3 saytest.py --speed 0.85 thermostat "thermostat 现在的意思是恒温器。"

5.3 起默认用正式配音的声音（声音克隆）；--engine kokoro 试原来的 38 号。
声音克隆每次念得不一样：--times 3 每种说法念 3 遍，看几遍听得清（正式跑会念到听清为止，最多 4 遍）。
要用 plan.json 里的生词读音（lexicon），加 --plan <plan.json>。--save 文件夹：把念出来的存成 wav 听听。"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import soundfile as sf
import synth
import voice_config as VC

ap = argparse.ArgumentParser()
ap.add_argument('word', help='要听清的单词（和配音稿检查时一样，按这个词判断）')
ap.add_argument('texts', nargs='+', help='几种说法')
ap.add_argument('--voice', type=int, default=38)
ap.add_argument('--speed', type=float, default=0.95, help='Kokoro 的语速')
ap.add_argument('--zv-speed', type=float, default=VC.SPEED, help='声音克隆的语速')
ap.add_argument('--engine', choices=['zipvoice', 'kokoro'], default='zipvoice')
ap.add_argument('--times', type=int, default=1)
ap.add_argument('--plan', help='用这份配音稿的 lexicon')
ap.add_argument('--save')
a = ap.parse_args()
if a.plan:
    lex = json.load(open(a.plan, encoding='utf-8')).get('lexicon') or {}
    if lex:
        d = os.path.dirname(os.path.abspath(a.plan))
        lp, zp = os.path.join(d, 'lexicon-saytest.txt'), os.path.join(d, 'lexicon-saytest-ipa.txt')
        with open(lp, 'w', encoding='utf-8') as fh, open(zp, 'w', encoding='utf-8') as fz:
            for k, v in lex.items():
                fh.write('%s %s\n' % (str(k).lower(), ' '.join(str(v).split())))
                fz.write('%s || %s\n' % (str(k).lower(), synth.to_ipa(v)))
        synth.EXTRA_LEX.insert(0, lp)
        synth.EXTRA_ZLEX.insert(0, zp)
plan = {'engine': a.engine, 'voice': a.voice, 'speed': a.speed, 'zvSpeed': a.zv_speed}
print('声音：' + ('声音克隆' if VC.engine(plan) == 'zipvoice' else 'Kokoro %d 号' % a.voice))
if a.save:
    os.makedirs(a.save, exist_ok=True)
for n, t in enumerate(a.texts, 1):
    ok = 0
    for k in range(a.times):
        x = synth.say(t, plan)
        heard = synth.transcribe_array(x, synth.SR)
        miss, _ = synth.check(t, heard, a.word)
        ok += not miss
        if a.save:
            sf.write(os.path.join(a.save, '说法%d_%d.wav' % (n, k + 1)), x, synth.SR)
        print(('✓ ' if not miss else '✗ ') + '%.2fs  %s\n    听成：%s%s' % (len(x) / synth.SR, t, heard, ('\n    没听清：' + '，'.join(miss)) if miss else ''))
    if a.times > 1:
        print('  -> %d 遍里 %d 遍听得清' % (a.times, ok))
