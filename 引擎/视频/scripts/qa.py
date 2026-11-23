#!/usr/bin/env python3
"""检查做好的视频：每一幕截一张图拼成一张总览（看画面），再把每一幕的声音转成文字（看配音和画面对不对得上）。

用法：python3 qa.py <work/单词/timing.json> <总览图.png>
看完总览图（用 view 工具打开）再交给用户：字有没有挤、图配得对不对、小黑板写全了没有、配音是不是讲到这一幕的内容。
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))


def frames(video, times, w=640):
    out = []
    for t in times:
        raw = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-ss', '%.2f' % t, '-i', video, '-frames:v', '1', '-vf', 'scale=%d:-1' % w,
                              '-f', 'image2pipe', '-c:v', 'png', '-'], capture_output=True).stdout
        from io import BytesIO
        out.append(Image.open(BytesIO(raw)).convert('RGB'))
    return out


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    tm = json.load(open(sys.argv[1], encoding='utf-8'))
    video, total = tm['video'], tm['total']
    times = []
    for name, t0, dur in tm['scenes']:
        times.append(min(total - 0.2, t0 + dur * (0.97 if name in ('board', 'board2') or name.startswith('yinbian') or name.startswith('xingtai') else 0.92 if name.startswith('fengong') else 0.8)))      # 6.1：总结可能有两页
    ims = frames(video, times)
    W, H = ims[0].size
    cols = 3
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * (W + 6) + 6, rows * (H + 6) + 6), (120, 130, 125))
    for i, im in enumerate(ims):
        sheet.paste(im, (6 + (i % cols) * (W + 6), 6 + (i // cols) * (H + 6)))
    sheet.save(sys.argv[2])
    print('总览图：%s（%d 幕，按顺序从左到右）' % (sys.argv[2], len(ims)))
    has_audio = 'audio' in subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type', '-of', 'csv=p=0', video], capture_output=True, text=True).stdout
    if not has_audio:
        print('（没有配音）')
        return
    sys.path.insert(0, HERE)
    from synth import transcribe_array
    pcm = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', video, '-vn', '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True).stdout
    x = np.frombuffer(pcm, dtype=np.float32)
    for name, t0, dur in tm['scenes']:
        seg = x[int(t0 * 16000): int((t0 + dur) * 16000)]
        print('%-8s %6.1f–%6.1fs  %s' % (name, t0, t0 + dur, transcribe_array(seg, 16000)[:90] if len(seg) else ''))


if __name__ == '__main__':
    main()
