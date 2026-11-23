#!/usr/bin/env python3
"""看一眼画好的插图（svg / png / jpg）：每张画在棋盘格上（看得出哪里透明），拼成一张总览。

  python3 artsheet.py ~/wordfilm-work/camera/art/*.svg --out ~/wordfilm-work/camera/art.png

自己画的 svg 一定先用它看一遍再放进视频：东西像不像、比例对不对、有没有画歪、透明的地方是不是该透明。
"""
import argparse, base64, os
from playwright.sync_api import sync_playwright

MIME = {'.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('files', nargs='+')
    ap.add_argument('--out', required=True)
    ap.add_argument('--cell', type=int, default=360, help='每张的高')
    a = ap.parse_args()
    cells = []
    for f in a.files:
        ext = os.path.splitext(f)[1].lower()
        if ext not in MIME or not os.path.exists(f):
            print('跳过：' + f)
            continue
        url = 'data:%s;base64,%s' % (MIME[ext], base64.b64encode(open(f, 'rb').read()).decode())
        cells.append('<figure><div class="ck"><img src="%s"></div><figcaption>%s</figcaption></figure>' % (url, os.path.basename(f)))
    html = '''<html><head><style>
      body{margin:0;padding:10px;background:#777;font:14px DejaVu Sans,sans-serif;display:flex;flex-wrap:wrap;gap:10px;width:1900px}
      figure{margin:0;background:#fff;padding:6px}
      .ck{height:%dpx;display:flex;align-items:center;justify-content:center;
          background:conic-gradient(#e8e8e8 25%%,#fff 0 50%%,#e8e8e8 0 75%%,#fff 0) 0 0/20px 20px}
      img{height:%dpx;width:auto;max-width:720px;object-fit:contain}
      figcaption{text-align:center;padding-top:4px}
    </style></head><body>%s</body></html>''' % (a.cell, a.cell, ''.join(cells))
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1920, 'height': 400})
        pg.set_content(html)
        pg.wait_for_timeout(300)
        pg.screenshot(path=a.out, full_page=True)
        b.close()
    print('插图总览：%s（%d 张）' % (a.out, len(cells)))


if __name__ == '__main__':
    main()
