#!/usr/bin/env python3
"""截几帧看动画中间的样子（不配音、不出视频）：每一帧写成“幕:秒”，秒从这一幕开始算。

  python3 snap.py --details work/details.json --word camera --prefs work/camera/prefs.json \\
      --at syl:0.5,syl:1.6,syl:3.0,evolve:2.5 --out work/camera/snap.png
  做好视频以后，按真实的配音时间截：加 --timing work/camera/timing.json --plan work/camera/plan.json --manifest work/camera/audio/manifest.json

“幕”用 preview.py 打印的名字（title、sec0、syl、sylnote、sec1、origin、meaning、evolve、example0、board…）；
秒可以写成 0.5（第 0.5 秒）或者 50%（这一幕的一半）。一行三张拼成一张图，每张左上角写幕和秒。
"""
import argparse, base64, io, json, os, sys
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from preview import load_prefs, film_in_page  # noqa: E402
LEAD, GAP, TAIL = 0.45, 0.40, 0.7      # 和 render.py 一样（6.10 起句间 0.40 秒）


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--details', required=True)
    ap.add_argument('--word', required=True)
    ap.add_argument('--prefs')
    ap.add_argument('--at', required=True, help='幕:秒，逗号隔开，比如 syl:0.5,evolve:50%')
    ap.add_argument('--out', required=True)
    ap.add_argument('--plan')
    ap.add_argument('--manifest')
    ap.add_argument('--width', type=int, default=640)
    a = ap.parse_args()
    details = json.load(open(a.details, encoding='utf-8'))
    d = details.get(a.word) or next(v for v in details.values() if v['w'].lower() == a.word.lower())
    prefs = load_prefs(a.prefs)
    want = [x.strip() for x in a.at.split(',') if x.strip()]
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        pg.set_content('<html><body style="margin:0"><canvas id=c width=1280 height=720></canvas></body></html>')
        pg.add_script_tag(path=os.path.join(HERE, 'wordfilm.js'))
        scenes = film_in_page(pg, d, prefs)
        if a.plan and a.manifest:                     # 和 render.py 一样按配音调整每一幕的长短
            plan = json.load(open(a.plan, encoding='utf-8'))
            man = json.load(open(a.manifest, encoding='utf-8'))
            timing = []
            for key in scenes:
                segs, spec = man.get(key, []), plan['scenes'].get(key, {})
                if not segs:
                    timing.append(None)
                    continue
                t, marks, ends, texts = LEAD, [], [], []
                waits = spec.get('waits') or {}                      # 6.13：练习题想一想的停顿（和 render.py 一样）
                for j, s in enumerate(segs):
                    extra = 0.0
                    if s['name'] != 'intro':
                        marks.append(round(t, 3))
                        ends.append(round(t + s['dur'], 3))          # 5.11：这一句说完的秒数、这一句的字（画里按词出东西 when 要用）
                        texts.append(s.get('text', ''))
                        extra = float(waits.get(str(len(marks) - 1), 0))
                    t += s['dur'] + (GAP if j < len(segs) - 1 else 0) + extra
                timing.append({'dur': round(t + TAIL + float(spec.get('hold', 0)), 3), 'marks': marks if spec.get('marks') else None, 'groups': spec.get('groups'),
                               'ends': ends if spec.get('marks') else None, 'texts': texts if spec.get('marks') else None})
            pg.evaluate("(tm) => WordFilm.retime(window._f, tm)", timing)
        info = pg.evaluate("() => window._f.scenes.map(s => [s.id + (s.i != null ? s.i : ''), s.t0, s.dur])")
        shots = []
        for w in want:
            name, _, at = w.partition(':')
            hit = next((x for x in info if x[0] == name), None)
            if not hit:
                print('没有这一幕：%s（有：%s）' % (name, ' '.join(x[0] for x in info)))
                continue
            sec = hit[2] * float(at[:-1]) / 100 if at.endswith('%') else float(at or 0)
            t = min(hit[1] + hit[2] - 0.01, hit[1] + sec)
            url = pg.evaluate("(t) => { const c = document.getElementById('c'); WordFilm.draw(c.getContext('2d'), window._f, t); return c.toDataURL('image/png'); }", t)
            im = Image.open(io.BytesIO(base64.b64decode(url.split(',', 1)[1]))).convert('RGB')
            shots.append(('%s %.1fs' % (name, sec), im))
        b.close()
    if not shots:
        return
    W = a.width
    H = int(W * 720 / 1280)
    cols = min(3, len(shots))
    rows = (len(shots) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * (W + 6) + 6, rows * (H + 6) + 6), (120, 130, 125))
    dr = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype('DejaVuSans.ttf', 16)
    except Exception:
        font = ImageFont.load_default()
    for i, (lab, im) in enumerate(shots):
        x, y = 6 + (i % cols) * (W + 6), 6 + (i // cols) * (H + 6)
        sheet.paste(im.resize((W, H)), (x, y))
        dr.rectangle([x, y, x + 9 * len(lab) + 12, y + 22], fill=(0, 0, 0))
        dr.text((x + 6, y + 3), lab, fill=(255, 255, 255), font=font)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    sheet.save(a.out)
    print('截了 %d 帧：%s' % (len(shots), a.out) + ('  页面报错：' + '; '.join(errs[:3]) if errs else ''))


if __name__ == '__main__':
    main()
