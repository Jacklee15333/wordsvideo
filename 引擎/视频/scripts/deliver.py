#!/usr/bin/env python3
"""分批交付（6.10 起，第四十七版）：一批词要做好几轮，每一轮只把“这一轮新做好、还没发过”的视频交给用户，最后再打一个总的压缩包。

用户：“每一轮工具用完了，让我点击继续的时候，先把已经生成好的视频发出来，我下载，不要放到最后一起生成出来……
上一轮在点击继续之前发给我的，这一轮就不要发了，要不然越来越多，而且还有重复的；等到最后一个生成完了，可以发一个大的压缩包，把所有的都给我”

  python3 deliver.py new  --out /mnt/user-data/outputs/构词动画      # 打印这一轮新做好、还没发过的视频（一行一个），并记成“已发”
  python3 deliver.py peek --out …                                     # 只看，不记
  python3 deliver.py zip  --out … --words camera,speaker,…  [--details ~/wordfilm-work/details.json]
                                                                      # 全部做完后：按顺序编号打包（附 目录.txt），打印压缩包路径
  python3 deliver.py status --out … --words …                         # 一共几个、做好几个、发过几个、还差哪些

“已发”的记录存在 <work>/已发送.txt（默认 ~/wordfilm-work）：沙盒重启后文件还在，接着记；换了新对话、文件没了，就从头算。
new 打印出来的路径直接交给 present_files；一轮里只调一次 new（调了就算发过了）。
压缩包里视频不再压缩（mp4 本来就压缩过，ZIP_STORED，打包快、Windows / Mac 自带的解压都能开），中文文件名带 UTF-8 标记。
"""
import argparse, json, os, re, sys, zipfile

# 6.19 起一个词两个视频：<单词>_构词动画_1精简版.mp4（放前面）、<单词>_构词动画_2详解版.mp4；以前的 <单词>_构词动画.mp4 也认
VIDEO_RX_OLD = re.compile(r'^(.+?)_构词动画(?:_(1精简版|2详解版))?\.mp4$')
# 6.27：新名字“store.mp4”“32 store.mp4”“store（详解）.mp4”
VIDEO_RX_NEW = re.compile(r'^(?:\d{1,3} )?(.+?)(（详解）)?\.mp4$')


class _RX:
    def match(self, f):
        m = VIDEO_RX_OLD.match(f)
        if m:
            return m
        m = VIDEO_RX_NEW.match(f)
        if not m:
            return None
        class M:
            def __init__(s2, w, ed):
                s2._g = (f, w, ed)
            def group(s2, k):
                return s2._g[k]
        return M(m.group(1), '2详解版' if m.group(2) else '1精简版')


VIDEO_RX = _RX()


def videos(out):
    """做好的视频：{单词: [路径…]}（精简版在前）。大于 100 KB 才算（渲染到一半的不算：render.py 最后一步才写出这个文件）"""
    res = {}
    for f in sorted(os.listdir(out)) if os.path.isdir(out) else []:
        m = VIDEO_RX.match(f)
        p = os.path.join(out, f)
        if m and os.path.getsize(p) > 100_000:
            res.setdefault(m.group(1).replace('_', ' '), []).append(p)
    return res


def sent_file(work):
    return os.path.join(work, '已发送.txt')


def load_sent(work):
    p = sent_file(work)
    return set(x.strip() for x in open(p, encoding='utf-8')) if os.path.exists(p) else set()


def safe(w):
    return re.sub(r'[\\/:*?"<>|\s]+', '_', w).strip('._') or 'word'


def contents_line(w, d):
    """目录.txt 的一行：单词：拆分 → 字面意思 → 现在的意思"""
    if not d:
        return w
    split = str(d.get('split') or d.get('拆分') or '').strip()
    logic = str(d.get('logic') or '')
    lit = ''
    m = re.search(r'=\s*“([^”]+)”', logic)
    if m:
        lit = '“%s”' % m.group(1)
    mean = str(d.get('meaning') or d.get('m') or '').replace('\n', ' / ')
    parts = [x for x in (split if split not in ('—', '-') else '', lit, mean) if x]
    return w + '：' + ' → '.join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['new', 'peek', 'zip', 'status'])
    ap.add_argument('--out', required=True, help='视频文件夹（run.py 的 --out）')
    ap.add_argument('--work', default=os.path.expanduser('~/wordfilm-work'))
    ap.add_argument('--words', help='这一批词，逗号隔开，按用户给的顺序（zip、status 用）')
    ap.add_argument('--details', help='details.json（目录.txt 用；默认 <work>/details.json）')
    ap.add_argument('--name', default='构词动画_全部.zip')
    a = ap.parse_args()
    have = videos(a.out)
    sent = load_sent(a.work)
    if a.cmd in ('new', 'peek'):
        # 6.19：按文件记“已发”（一个词两个视频，可能分两轮做好）；以前按单词记的照样认
        fresh = [p for w in have for p in have[w] if os.path.basename(p) not in sent and not (w in sent and VIDEO_RX.match(os.path.basename(p)).group(2) is None)]
        for p in fresh:
            print(p)
        if a.cmd == 'new' and fresh:
            os.makedirs(a.work, exist_ok=True)
            with open(sent_file(a.work), 'a', encoding='utf-8') as fh:
                fh.write(''.join(os.path.basename(p) + '\n' for p in fresh))
        if not fresh:
            print('（这一轮没有新做好的视频）', file=sys.stderr)
        return
    words = [w.strip() for w in re.split(r'[,，]', a.words or '') if w.strip()] or list(have)
    if a.cmd == 'status':
        done = [w for w in words if w in have]
        print('一共 %d 个词，做好 %d 个（%d 个视频），发过 %d 个视频' % (len(words), len(done), sum(len(have[w]) for w in done),
              len([p for w in done for p in have[w] if os.path.basename(p) in sent or w in sent])))
        miss = [w for w in words if w not in have]
        if miss:
            print('还没做好：' + '、'.join(miss))
        return
    # zip：按 words 的顺序编号，附目录
    det = {}
    dp = a.details or os.path.join(a.work, 'details.json')
    if os.path.exists(dp):
        try:
            det = json.load(open(dp, encoding='utf-8'))
        except Exception:
            det = {}
    zp = os.path.join(a.out, a.name)
    lines, n = [], 0
    with zipfile.ZipFile(zp, 'w', zipfile.ZIP_STORED, allowZip64=True) as z:
        for w in words:
            if w not in have:
                lines.append('（没有视频）' + w)
                continue
            n += 1
            for p in have[w]:                                   # 6.19：精简版在前、详解版在后
                ed = VIDEO_RX.match(os.path.basename(p)).group(2)
                z.write(p, '%02d %s%s.mp4' % (n, w, '（详解）' if ed == '2详解版' else ''))      # 6.27：“32 store.mp4”
            lines.append('%02d  %s' % (n, contents_line(w, det.get(w) or det.get(w.lower()))))
        z.writestr(zipfile.ZipInfo('目录.txt'), ('\r\n'.join(lines) + '\r\n').encode('utf-8-sig'), compress_type=zipfile.ZIP_DEFLATED)
    print(zp)
    print('打包了 %d 个词、%d 个视频（%.0f MB）' % (n, sum(len(have[w]) for w in words if w in have), os.path.getsize(zp) / 1e6), file=sys.stderr)


if __name__ == '__main__':
    main()
