#!/usr/bin/env python3
"""frames.py 视频 timing.json 输出.jpg：从成片里按几幕关键画面截 9 帧，拼成一张 3×3 的图（左上角写是哪一幕、第几秒）"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
video, timing, out = sys.argv[1:4]
t = json.load(open(timing, encoding='utf-8'))
S = {n: (s, d) for n, s, d in t['scenes']}
def first(prefix):
    return next((n for n, _, _ in t['scenes'] if n.startswith(prefix)), None)
def last(prefix):
    return next((n for n, _, _ in reversed(t['scenes']) if n.startswith(prefix)), None)
picks = [('封面（第一帧）', 0.0)]
for lab, key, at in (('读音现象', 'duyin0', 'end'), ('词缀卡片', 'part0', 0.6), ('例句', 'example0', 'end'),
                     ('同义词辨析', 'distinguish', 'end'), ('考点 1', 'kaodian0', 'end'), ('考点 2', 'kaodian1', 'end'),
                     ('总结（出现 1 秒）', 'board', 'start1'), ('最后一题答案', last('daan'), 'end')):
    if key in S:
        s, d = S[key]
        ts = s + 1.0 if at == 'start1' else s + d - 0.6 if at == 'end' else s + d * at
        picks.append((lab, max(0.0, ts)))
picks = picks[:9]
try:
    font = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 26)
except OSError:
    font = ImageFont.load_default()
sheet = Image.new('RGB', (1920, 1080), 'white')
tmp = out + '.tmp.png'
for i, (lab, ts) in enumerate(picks):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '%.2f' % ts, '-i', video, '-frames:v', '1', tmp], check=True)
    im = Image.open(tmp).convert('RGB').resize((640, 360))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 640, 36), fill=(0, 0, 0))
    d.text((8, 2), f'{lab}  {ts:.1f}s', fill=(255, 220, 0), font=font)
    sheet.paste(im, ((i % 3) * 640, (i // 3) * 360))
os.remove(tmp)
sheet.save(out, quality=85)
print(out)
