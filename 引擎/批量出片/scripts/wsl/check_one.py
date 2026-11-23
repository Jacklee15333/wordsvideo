#!/usr/bin/env python3
"""check_one.py 视频 brief文件夹：自动质检；通过返回 0，有问题返回 2（要人看）"""
import json, os, re, subprocess, sys
video, P = sys.argv[1:3]
bad = []
r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_type', '-of', 'json', video], capture_output=True, text=True)
info = json.loads(r.stdout or '{}')
types = [s.get('codec_type') for s in info.get('streams', [])]
dur = float(info.get('format', {}).get('duration', 0) or 0)
print('文件：%s，%.1f 秒，%s' % (os.path.basename(video), dur, '有画面、有声音' if 'video' in types and 'audio' in types else '缺画面或声音'))
if dur < 30 or 'audio' not in types:
    bad.append('时长不对或没有声音')
e = subprocess.run(['ffmpeg', '-v', 'error', '-i', video, '-map', '0:v:0', '-map', '0:a:0', '-f', 'null', '-'], capture_output=True, text=True).stderr.strip()
print('解码：' + ('有错误：' + e.splitlines()[0] if e else '从头到尾没有错误'))
if e:
    bad.append('解码有错误')
try:
    man = json.load(open(P + '/audio/manifest.json', encoding='utf-8'))
    k38 = sum(1 for v in man.values() for s in v if s.get('engine') == 'kokoro')
    miss = sum(1 for v in man.values() for s in v if s.get('miss'))
    print('配音：%d 句，退回 38 号 %d 句，没听清 %d 句' % (sum(len(v) for v in man.values()), k38, miss))
    if k38 or miss:
        bad.append('配音有退回 38 号或没听清的句子')
except OSError:
    bad.append('没有配音记录 manifest.json')
try:
    blocks = [b.split('\n')[2:] for b in open(P + '/subtitles.srt', encoding='utf-8').read().replace('\r', '').strip().split('\n\n')]
    lines = [' '.join(b) for b in blocks if b]
    en = [l for l in lines if not re.search(r'[\u3400-\u9fff]', l)]
    print('字幕：%d 条，只有英文的 %d 条' % (len(lines), len(en)) + ('：' + ' | '.join(en[:3]) if en else ''))
    if en:
        bad.append('有只有英文的字幕')
except OSError:
    print('字幕：没有字幕文件')
sheet = video[:-4] + '_关键画面.jpg'
r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frames.py'), video, P + '/timing.json', sheet], capture_output=True, text=True)
print('关键画面图：' + (sheet if r.returncode == 0 else '没拼出来：' + r.stderr.strip()[-200:]))
if bad:
    print('⚠ 质检没过：' + '；'.join(bad)); sys.exit(2)
print('✅ 自动质检通过（人再看一眼关键画面图）')
