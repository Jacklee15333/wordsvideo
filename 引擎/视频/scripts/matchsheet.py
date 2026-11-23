#!/usr/bin/env python3
"""逐句对照图（5.11）：每一句配音截一帧（截在这一句快说完的时候），下面写这一句说的字。
一句一句对着看：这一句说的东西，画面上是不是正好有、够不够大、标签指得对不对。

  python3 matchsheet.py --details work/details.json --word produce --prefs work/produce/prefs.json \\
      --plan work/produce/plan.json --manifest work/produce/audio/manifest.json --out work/produce/match
  → work/produce/match_1.png、match_2.png…（一张 9 格）。用 view 看。

  --scenes part,evolve,example   只看这几种幕（默认：part、fengong、combo、rule、origin、meaning、evolve、example、distinguish；6.1 起默认也截“身份和分工”“同义词辨析”）
  --at 0.82                      每一句截在说到百分之几的时候（默认 0.82：这一句的东西都该出来了）
  还没配音（没有 --manifest）也能跑：按默认的时间截，只能看大概。
"""
import argparse, base64, io, json, os, sys
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from preview import load_prefs, film_in_page  # noqa: E402
LEAD, GAP, TAIL = 0.45, 0.40, 0.7      # 和 render.py 一样（6.10 起句间 0.40 秒）


def cjk_font(size):
    for p in (os.path.expanduser('~/.local/share/fonts/LXGWWenKai-Regular.ttf'), '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
              '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def wrap(dr, text, font, width):
    out, cur = [], ''
    for ch in text:
        if dr.textlength(cur + ch, font=font) > width and cur:
            out.append(cur)
            cur = ch
        else:
            cur += ch
    if cur:
        out.append(cur)
    return out[:3]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--details', required=True)
    ap.add_argument('--word', required=True)
    ap.add_argument('--prefs')
    ap.add_argument('--plan')
    ap.add_argument('--manifest')
    ap.add_argument('--out', required=True, help='输出文件名的前半截（后面自动加 _1.png、_2.png…）')
    ap.add_argument('--scenes', default='part,yinbian,xingtai,fengong,combo,rule,origin,meaning,evolve,example,distinguish')
    ap.add_argument('--at', type=float, default=0.82)
    ap.add_argument('--width', type=int, default=560)
    a = ap.parse_args()
    details = json.load(open(a.details, encoding='utf-8'))
    d = details.get(a.word) or next(v for v in details.values() if v['w'].lower() == a.word.lower())
    prefs = load_prefs(a.prefs)
    want = [x.strip() for x in a.scenes.split(',') if x.strip()]
    plan = json.load(open(a.plan, encoding='utf-8')) if a.plan and os.path.exists(a.plan) else {'scenes': {}}
    man = json.load(open(a.manifest, encoding='utf-8')) if a.manifest and os.path.exists(a.manifest) else {}
    shots = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.set_content('<html><body style="margin:0"><canvas id=c width=1280 height=720></canvas></body></html>')
        pg.add_script_tag(path=os.path.join(HERE, 'wordfilm.js'))
        scenes = film_in_page(pg, d, prefs)
        per = {}                                       # 幕 → [(开始, 结束, 文字)]
        timing = []
        for key in scenes:
            spec = plan['scenes'].get(key, {})
            segs = man.get(key)
            if not segs:                               # 没配音：按稿子的句子估（每个字 0.2 秒）
                texts = ([spec['intro']] if spec.get('intro') else []) + list(map(lambda x: x if isinstance(x, str) else x.get('t', ''), spec.get('segs', [])))
                segs = [{'name': 'intro' if (i == 0 and spec.get('intro')) else 's', 'dur': max(1.0, 0.2 * len(t)), 'text': t} for i, t in enumerate(texts)]
            if not segs:
                timing.append(None)
                continue
            t, marks, ends, texts, rows = LEAD, [], [], [], []
            for j, s in enumerate(segs):
                if s['name'] != 'intro':
                    marks.append(round(t, 3)); ends.append(round(t + s['dur'], 3)); texts.append(s.get('text', ''))
                    rows.append((t, t + s['dur'], s.get('text', '')))
                t += s['dur'] + (GAP if j < len(segs) - 1 else 0)
            per[key] = rows
            timing.append({'dur': round(t + TAIL + float(spec.get('hold', 0)), 3), 'marks': marks if spec.get('marks') else None, 'groups': spec.get('groups'),
                           'ends': ends if spec.get('marks') else None, 'texts': texts if spec.get('marks') else None})
        pg.evaluate("(tm) => WordFilm.retime(window._f, tm)", timing)
        info = pg.evaluate("() => window._f.scenes.map(s => [s.id + (s.i != null ? s.i : ''), s.t0, s.dur])")
        for name, t0, dur in info:
            if not any(name.startswith(w) for w in want) or name not in per:
                continue
            for j, (s0, s1, text) in enumerate(per[name]):
                t = min(t0 + dur - 0.02, t0 + s0 + a.at * (s1 - s0))
                url = pg.evaluate("(t) => { const c = document.getElementById('c'); WordFilm.draw(c.getContext('2d'), window._f, t); return c.toDataURL('image/png'); }", t)
                im = Image.open(io.BytesIO(base64.b64decode(url.split(',', 1)[1]))).convert('RGB')
                shots.append(('%s 第%d句' % (name, j + 1), text, im))
        b.close()
    if not shots:
        print('没有可截的句子（看看 --scenes 写得对不对）')
        return
    W = a.width
    H = int(W * 720 / 1280)
    CAP = 78
    font, small = cjk_font(19), cjk_font(15)
    per_sheet, cols = 9, 3
    os.makedirs(os.path.dirname(os.path.abspath(a.out)) or '.', exist_ok=True)
    files = []
    for k in range(0, len(shots), per_sheet):
        part = shots[k:k + per_sheet]
        rows = (len(part) + cols - 1) // cols
        sheet = Image.new('RGB', (cols * (W + 8) + 8, rows * (H + CAP + 8) + 8), (236, 232, 222))
        dr = ImageDraw.Draw(sheet)
        for i, (lab, text, im) in enumerate(part):
            x, y = 8 + (i % cols) * (W + 8), 8 + (i // cols) * (H + CAP + 8)
            sheet.paste(im.resize((W, H)), (x, y))
            dr.rectangle([x, y + H, x + W, y + H + CAP], fill=(255, 255, 255))
            dr.text((x + 8, y + H + 4), lab, fill=(150, 90, 0), font=small)
            for n, ln in enumerate(wrap(dr, text, font, W - 16)):
                dr.text((x + 8, y + H + 24 + n * 22), ln, fill=(30, 40, 36), font=font)
        fn = '%s_%d.png' % (a.out, k // per_sheet + 1)
        sheet.save(fn)
        files.append(fn)
    print('逐句对照图 %d 句：%s' % (len(shots), '、'.join(files)) + ('  页面报错：' + '; '.join(errs[:3]) if errs else ''))


if __name__ == '__main__':
    main()
