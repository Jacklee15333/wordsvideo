#!/usr/bin/env python3
"""只新增文件到 GitHub（Git Data API，base_tree 保留仓库原有的一切）。
用法: gh_add.py "提交说明" 仓库路径=本地文件 ...   或  仓库路径=@blobsha"""
import sys, os, json, base64, urllib.request, time
T = open(os.path.expanduser('~/gh/token')).read().strip()
R = 'https://api.github.com/repos/Jacklee15333/ciyuanchaifeng'
def api(m, p, d=None):
    for i in range(5):
        try:
            rq = urllib.request.Request(R + p, method=m, data=json.dumps(d).encode() if d is not None else None,
                headers={'Authorization': 'token ' + T, 'Accept': 'application/vnd.github+json', 'Content-Type': 'application/json'})
            return json.load(urllib.request.urlopen(rq, timeout=300))
        except Exception as e:
            err = e; time.sleep(3 + 5 * i)
    raise err
msg = sys.argv[1]; items = []
for a in sys.argv[2:]:
    path, src = a.split('=', 1)
    if src.startswith('@'): sha = src[1:]
    else:
        b = base64.b64encode(open(src, 'rb').read()).decode()
        sha = api('POST', '/git/blobs', {'content': b, 'encoding': 'base64'})['sha']
    items.append({'path': path, 'mode': '100644', 'type': 'blob', 'sha': sha})
ref = api('GET', '/git/ref/heads/master'); head = ref['object']['sha']
base = api('GET', '/git/commits/' + head)['tree']['sha']
tree = api('POST', '/git/trees', {'base_tree': base, 'tree': items})['sha']
c = api('POST', '/git/commits', {'message': msg, 'tree': tree, 'parents': [head]})['sha']
api('PATCH', '/git/refs/heads/master', {'sha': c})
t = api('GET', '/git/trees/' + c + '?recursive=1')
print('提交', c[:8], '文件数', sum(1 for x in t['tree'] if x['type'] == 'blob'))
for it in items:
    print('  ✓' if any(x['path'] == it['path'] and x['sha'] == it['sha'] for x in t['tree']) else '  ✗', it['path'])
