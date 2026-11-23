#!/usr/bin/env python3
"""missing_art.py 文件夹名：画面设置里用到的图有没有都画出来；缺的提示可能是哪个画图脚本画的。
缺的是“会动的人”（cn-boy-xxx 这种，由 poses.py 和画图脚本的 *motions.json 定义）时，列出这个人现有的动作，画面组从里面挑一个换上"""
import glob, json, os, re, sys
w = sys.argv[1]; work = os.path.expanduser('~/wordfilm-work'); art = f'{work}/{w}/art'
s = open(f'{work}/edits_{w}.json', encoding='utf-8').read()
miss = sorted(set(f for f in re.findall(r'art/([^"\s]+?\.(?:svg|png))', s) if not os.path.exists(f'{art}/{f}')))
print('缺图：' + ('、'.join(miss) if miss else '无'))
motions = set()
for p in glob.glob(art + '/*motions.json'):
    try:
        motions |= set(json.load(open(p, encoding='utf-8')))
    except Exception:
        pass
for f in miss:
    stem = re.sub(r'(_f\d+)?\.(svg|png)$', '', f)
    who = sorted({os.path.basename(x)[:-7] for d in ('~/kit-extra', '~/kit') for x in glob.glob(os.path.expanduser(d) + '/*_art.py')
                  if stem in open(x, encoding='utf-8').read()})
    if who:
        print(f'  {f}：可能要加画图脚本 ' + '、'.join(who))
        continue
    head = stem.rsplit('-', 1)[0]
    same = sorted(m for m in motions if m.startswith(head + '-'))
    if same:
        print(f'  {f}：这是会动的人“{head}”的一个动作，现在的动作表里没有它（kit 的画面设置过时了）。'
              f'画面组在 words/{w}.py 里换成现有的动作之一：' + '、'.join(same[:20]))
    else:
        print(f'  {f}：没找到是哪个画图脚本画的（看 ~/kit/README.md）')
sys.exit(1 if miss else 0)
