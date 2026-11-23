#!/usr/bin/env python3
"""几秒钟看一眼画面：每一幕截一张静止图拼成总览（不配音、不出视频）。

  python3 preview.py --details work/details.json --word transport --prefs work/transport/prefs.json --out work/transport/preview.png
  多个词：--word a,b,c（默认读 --work/<单词>/prefs.json，每个词一张图，文件名后面加单词）

渲染整段视频之前先用它检查：每个意思的画、拼起来以后的画、卡片上的来源牌子、小黑板的扩展词；改了 prefs.json 再跑一次。
"""
import re
import argparse, base64, io, json, os, sys
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import emoji3d  # noqa: E402

MIME = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.svg': 'image/svg+xml'}


def load_prefs(path):
    if not path or not os.path.exists(path):
        return {'board': True}
    prefs = json.load(open(path, encoding='utf-8'))
    return embed_images(prefs, os.path.dirname(os.path.abspath(path)))


def _all_pics(prefs):
    """prefs 里所有的画：每个意思的画和例句动画、拼起来那一格、来历的画（originPic）、演变每一步的示意图（flow[].fig）、同义词辨析每张卡的画"""
    out = []

    def add(pc):
        if isinstance(pc, dict) and not any(pc is x for x in out):
            out.append(pc)
            add(pc.get('exPic'))
    for pc in prefs.get('pics') or []:
        add(pc)
    add(prefs.get('comboPic'))
    add(prefs.get('originPic'))
    for pc in (prefs.get('partPics') or {}).values():      # 5.11：每部分卡片自己的画
        add(pc)
    for st in prefs.get('flow') or []:
        if isinstance(st, dict):
            add(st.get('fig'))
    dm = prefs.get('demo')                                    # 6.7：辨析里每个用法的演示
    if isinstance(dm, dict):
        for x in dm.values():
            if isinstance(x, dict):
                add(x.get('pic'))
    dg = prefs.get('distinguish')                             # 6.0：第三部分“同义词辨析”每张卡的画
    if isinstance(dg, dict):
        for pc in (dg.get('pics') or {}).values():
            add(pc)
        for it in dg.get('items') or []:
            if isinstance(it, dict):
                add(it.get('pic'))
    return out


def _svg_sized(text):
    """svg 没写 width / height 的，按 viewBox 补上（宽至少 1200），画在画布上才清楚、比例才对"""
    import re
    m = re.search(r'<svg\b[^>]*>', text)
    if not m:
        return text
    tag = m.group(0)
    if re.search(r'\swidth\s*=', tag) and re.search(r'\sheight\s*=', tag):
        return text
    vb = re.search(r'viewBox\s*=\s*["\']\s*([-\d.]+)[\s,]+([-\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)', tag)
    if not vb:
        return text
    w, h = float(vb.group(3)), float(vb.group(4))
    k = max(1.0, 1200.0 / max(w, h))
    tag2 = re.sub(r'\s(width|height)\s*=\s*["\'][^"\']*["\']', '', tag)
    tag2 = tag2[:-1].rstrip('/') + ' width="%d" height="%d"%s>' % (round(w * k), round(h * k), '/' if tag.endswith('/>') else '')
    return text.replace(tag, tag2, 1)


def _viewbox(src, base):
    """svg 的 viewBox 宽高（标签、光线用插图自己的坐标时要用）"""
    import re
    src = str(src or '').strip()
    if not src:
        return None
    if src.startswith('data:'):
        if ';base64,' not in src:
            return None
        text = base64.b64decode(src.split(',', 1)[1]).decode('utf-8', 'ignore')
    elif src.startswith('<'):
        text = src
    else:
        p = os.path.expanduser(src)
        p = p if os.path.isabs(p) else os.path.join(base, p)
        if not os.path.exists(p):
            return None
        text = open(p, encoding='utf-8').read()
    m = re.search(r'viewBox\s*=\s*["\']\s*([-\d.]+)[\s,]+([-\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)', text)
    return [float(m.group(3)), float(m.group(4))] if m else None


def _to_url(src, base, kind):
    """图片文件（png / jpg / webp / svg，相对 prefs.json 的路径）或者直接写在 prefs 里的 <svg…> → data URL；不行返回 None"""
    src = str(src or '').strip()
    if not src:
        return None
    if src.startswith('data:'):
        return src
    if src.startswith('<svg') or src.startswith('<?xml'):
        return 'data:image/svg+xml;base64,' + base64.b64encode(_svg_sized(src).encode('utf-8')).decode()
    p = os.path.expanduser(src)
    p = p if os.path.isabs(p) else os.path.join(base, p)
    ext = os.path.splitext(p)[1].lower()
    if not (os.path.exists(p) and ext in MIME):
        print('提醒：找不到图片 %s（只认 png / jpg / webp / svg），这一样不画' % p)
        return None
    if ext == '.svg':
        return 'data:image/svg+xml;base64,' + base64.b64encode(_svg_sized(open(p, encoding='utf-8').read()).encode('utf-8')).decode()
    return 'data:%s;base64,%s' % (MIME[ext], base64.b64encode(open(p, 'rb').read()).decode())


def embed_images(prefs, base):
    """画里写了图片文件的（整幅画的 img、画里的 svg 插图和 img 照片），读进来变成 data URL，页面里才画得出来"""
    for pic in _all_pics(prefs):
        if pic.get('img'):
            u = _to_url(pic['img'], base, 'img')
            if u:
                pic['img'] = u
            else:
                pic.pop('img', None)
        for it in pic.get('items') or []:
            if not isinstance(it, dict):
                continue
            if isinstance(it.get('frames'), list) and it['frames']:   # 6.24：动图——几张图轮着放（fps 张 / 秒）
                if not it.get('svg') and not it.get('img'):
                    it['svg'] = it['frames'][0]
                fr = [_to_url(f, base, 'svg') for f in it['frames']]
                it['frames'] = [u for u in fr if u]
            if isinstance(it.get('alt'), list) and it['alt']:            # 6.25：emit 轮着用的几张图
                it['alt'] = [u for u in (_to_url(f, base, 'svg') for f in it['alt']) if u]
            vb = _viewbox(it.get('svg'), base)
            if vb:
                it['_vb'] = vb
            for key in ('svg', 'img'):
                if it.get(key):
                    u = _to_url(it[key], base, key)
                    if u:
                        it[key] = u
                    else:
                        it.pop(key, None)
    # 6.20：小图标也可以是自己画的图（icons 里写 "art/xxx.svg"，正方形最好）：读成 data URL，页面里按这个名字取图
    icon_urls = {}
    def _icon(v):
        v = str(v or '').strip()
        if re.search(r'\.(svg|png|jpe?g|webp)$', v, re.I) and v not in icon_urls:
            u = _to_url(v, base, 'icon')
            if u:
                icon_urls[v] = u
    for v in (prefs.get('icons') or {}).values():
        _icon(v)
    for st in prefs.get('flow') or []:
        if isinstance(st, dict):
            for v in str(st.get('icons') or '').split():
                _icon(v)
    for dm in (prefs.get('demo') or {}).values() if isinstance(prefs.get('demo'), dict) else []:
        if isinstance(dm, dict):
            for v in dm.get('icons') or []:
                _icon(v)
    if icon_urls:
        prefs['_iconUrls'] = icon_urls
    return prefs


def film_in_page(pg, d, prefs):
    """在页面里搭好这段动画（window._f），读进画里用到的 3D 表情图和自己的图片；返回每一幕的名字"""
    pg.evaluate("document.fonts.load('40px \"LXGW WenKai\"')")
    names = pg.evaluate("""async ([d, pr]) => { window._f = WordFilm.build(d, pr); await WordFilm.ready(window._f);
        return window._f.scenes.map(s => s.id + (s.i != null ? s.i : '')); }""", [d, prefs])
    urls = dict(emoji3d.data_urls([g for g in pg.evaluate("() => WordFilm.glyphs(window._f)") if g not in (prefs.get('_iconUrls') or {})]) or {})
    urls.update(prefs.get('_iconUrls') or {})       # 6.20：自己画的小图标
    if urls:
        pg.evaluate("(m) => WordFilm.useImages(m)", urls)
    return names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--details', required=True)
    ap.add_argument('--word', required=True)
    ap.add_argument('--prefs', help='一个词时用；多个词时默认读 --work/<单词>/prefs.json')
    ap.add_argument('--work', default=os.path.expanduser('~/wordfilm-work'))
    ap.add_argument('--out', required=True)
    ap.add_argument('--cell', type=int, default=640, help='每一格的宽度（像素）。默认 640；想看清小字（辨析、总结）用 960，原大是 1280')
    ap.add_argument('--only', help='只画这几幕（逗号隔开的幕名，如 part0,fengong1；改一两幕时几秒出图）')
    a = ap.parse_args()
    only = [x.strip() for x in (a.only or '').split(',') if x.strip()]
    cw = max(320, min(1280, a.cell)); chh = cw * 9 // 16
    details = json.load(open(a.details, encoding='utf-8'))
    words = [w.strip() for w in a.word.replace('，', ',').split(',') if w.strip()]
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        pg.set_content('<html><body style="margin:0"><canvas id=c width=1280 height=720></canvas></body></html>')
        pg.add_script_tag(path=os.path.join(HERE, 'wordfilm.js'))
        for w in words:
            d = details.get(w) or next((v for v in details.values() if v['w'].lower() == w.lower()), None)
            if not d:
                print('details.json 里没有 ' + w)
                continue
            prefs = load_prefs(a.prefs if len(words) == 1 and a.prefs else os.path.join(a.work, w, 'prefs.json'))
            film_in_page(pg, d, prefs)
            urls = pg.evaluate("""(only) => { const f = window._f, c = document.getElementById('c'), x = c.getContext('2d'), out = [];
                for (const s of f.scenes) {
                  if (only.length && !only.includes(s.id + (s.i != null ? s.i : ''))) continue;
                  const at = s.id === 'board' || s.id === 'board2' || s.id === 'yinbian' || s.id === 'xingtai' ? 0.97 : s.id === 'meaning' || s.id === 'combo' || s.id === 'fengong' ? 0.92 : s.id === 'part' ? Math.max(0.8, 1 - 1.3 / s.dur) : 0.8;      // 6.5：特写卡片取结束前 1.3 秒（最后一句“原因”也看得到，后面接别的幕时卡片还没开始淡出）
                  WordFilm.draw(x, f, s.t0 + s.dur * at);
                  out.push([s.id + (s.i != null ? s.i : ''), c.toDataURL('image/png')]);
                }
                return out; }""", only)
            ims = [Image.open(io.BytesIO(base64.b64decode(u.split(',', 1)[1]))).convert('RGB').resize((cw, chh), Image.LANCZOS) for _, u in urls]
            cols = 3 if len(ims) > 2 else max(1, len(ims))
            rows = (len(ims) + cols - 1) // cols
            sheet = Image.new('RGB', (cols * (cw + 6) + 6, rows * (chh + 6) + 6), (120, 130, 125))
            for i, im in enumerate(ims):
                sheet.paste(im, (6 + (i % cols) * (cw + 6), 6 + (i // cols) * (chh + 6)))
            out = a.out if len(words) == 1 else os.path.splitext(a.out)[0] + '_' + w + '.png'
            os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
            sheet.save(out)
            print('%s：%s（%s）' % (w, out, ' '.join(k for k, _ in urls)))
        b.close()
    if errs:
        print('页面报错：' + '; '.join(errs[:5]))


if __name__ == '__main__':
    main()
