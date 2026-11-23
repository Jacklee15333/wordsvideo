#!/usr/bin/env python3
"""立体彩色表情图：画面里的表情换成微软 Fluent Emoji 的 3D 图（MIT 许可），比字体里的表情更立体、颜色更足。

  python3 emoji3d.py 🚚 📦 🌉        # 下载这几个（已经有的跳过），打印存在哪

图存在 $WORDFILM_MODELS/emoji3d/（默认 ~/wordfilm-models/emoji3d/），下载过的不再下载，每个 3 万～6 万字节。
从 raw.githubusercontent.com 下载；下载不了的表情照样用字体里的画，不影响出视频。
不想用 3D 图：export WORDFILM_EMOJI=font
"""
import base64, json, os, re, sys, urllib.error, urllib.parse, urllib.request

MODELS = os.environ.get('WORDFILM_MODELS', os.path.expanduser('~/wordfilm-models'))
DIR = os.path.join(MODELS, 'emoji3d')
NAMES_URL = 'https://raw.githubusercontent.com/muan/unicode-emoji-json/main/data-by-emoji.json'
BASE = 'https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/'


def _get(url, timeout=20):
    req = urllib.request.Request(url, headers={'User-Agent': 'wordfilm'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _names():
    """表情 → [英文名, 文件名用的写法, 有没有肤色]（Fluent 的文件夹按英文名起）"""
    p = os.path.join(DIR, 'names.json')
    if not os.path.exists(p):
        os.makedirs(DIR, exist_ok=True)
        data = json.loads(_get(NAMES_URL, 60))
        json.dump({k: [v['name'], v.get('slug', ''), bool(v.get('skin_tone_support'))] for k, v in data.items()},
                  open(p, 'w', encoding='utf-8'), ensure_ascii=False)
    return json.load(open(p, encoding='utf-8'))


def _key(e):
    return '-'.join('%x' % ord(c) for c in e if ord(c) != 0xFE0F)


def _urls(name, slug, skin):
    folder = urllib.parse.quote(name[:1].upper() + name[1:])
    s = slug or re.sub(r'[^a-z0-9]+', '_', name.lower()).strip('_')
    a, b = folder + '/Default/3D/' + s + '_3d_default.png', folder + '/3D/' + s + '_3d.png'
    return [BASE + x for x in ((a, b) if skin else (b, a))]


def ensure(glyphs):
    """→ {表情: 图片路径}；下载不了的不在结果里"""
    if os.environ.get('WORDFILM_EMOJI') == 'font':
        return {}
    os.makedirs(DIR, exist_ok=True)
    miss_p = os.path.join(DIR, 'missing.json')
    missing = set(json.load(open(miss_p))) if os.path.exists(miss_p) else set()
    out, names, offline = {}, None, False
    for g in glyphs:
        k = _key(g)
        if not k:
            continue
        p = os.path.join(DIR, k + '.png')
        if os.path.exists(p):
            out[g] = p
            continue
        if k in missing or offline:
            continue
        if names is None:
            try:
                names = _names()
            except Exception as ex:
                print('提醒：拿不到表情名称表（%s），这次用字体里的表情' % ex)
                return out
        info = names.get(g) or names.get(g.replace('\ufe0f', '')) or names.get(g + '\ufe0f')
        found = False
        for url in (_urls(*info) if info else []):
            try:
                data = _get(url)
            except urllib.error.HTTPError as ex:
                if ex.code == 404:
                    continue
                offline = True
                break
            except Exception:
                offline = True
                break
            if data[:8] == b'\x89PNG\r\n\x1a\n':
                open(p, 'wb').write(data)
                out[g] = p
                found = True
                break
        if not found and not offline:
            missing.add(k)
    if offline:
        print('提醒：下载 3D 表情图时网络不通，没下载到的用字体里的表情')
    json.dump(sorted(missing), open(miss_p, 'w'))
    return out


def data_urls(glyphs):
    """→ {表情: data URL}，传给页面里的 WordFilm.useImages"""
    try:
        got = ensure(glyphs)
    except Exception as ex:
        print('提醒：3D 表情图没准备好（%s），用字体里的表情' % ex)
        return {}
    return {g: 'data:image/png;base64,' + base64.b64encode(open(p, 'rb').read()).decode() for g, p in got.items()}


if __name__ == '__main__':
    gs = sys.argv[1:]
    if not gs:
        print(__doc__)
        sys.exit(1)
    got = ensure(gs)
    for g in gs:
        print(g, got.get(g, '没有（用字体里的表情）'))
