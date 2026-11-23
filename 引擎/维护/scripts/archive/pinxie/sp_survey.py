import json, re, collections
rows = json.load(open('/home/claude/work/ee_rows.json'))
V = 'aeiouy'
def norm(p):
    p = p.strip()
    p = re.sub(r'\(=[^()]*\)', '', p)          # ar(=ad) -> ar
    p = re.sub(r'\(([^()=]*)\)', '', p)          # dur(e) -> dur ; (r)oll -> oll
    return p.lower().replace('-', '').replace("'", '').replace(' ', '')

def boundary(prev, nxt, rest):
    """prev 原样、nxt 原样、rest = 单词里从这一部分开始的剩余字母；返回 (现象, 前一部分在单词里实际写成的样子)"""
    if rest.startswith(prev + nxt[:1]) or (rest.startswith(prev) and not nxt):
        # 拼得上：再看是不是双写、保留 e
        if len(nxt) >= 2 and nxt[0] == prev[-1:] and nxt[0] not in V and nxt[1] in V + 'r' and len(prev) >= 2:
            return 'double', prev
        if re.search(r'[cg]e$', prev) and nxt[:1] in ('a', 'o') :
            return 'keep_e_soft', prev
        if prev.endswith('e') and nxt[:1] in ('a','e','i','o','u'):
            return 'keep_e_other', prev
        return None, prev
    cand = []
    if prev.endswith('e'):
        cand.append(('drop_e' if nxt[:1] in V else 'drop_e_cons', prev[:-1]))
    if prev.endswith('ie') and nxt.startswith('i'):
        cand.append(('ie_y', prev[:-2] + 'y'))
    if re.search(r'[^aeiou]y$', prev):
        cand.append(('y_i', prev[:-1] + 'i'))
    if prev.endswith('le') and nxt.startswith('ly'):
        cand.append(('le_ly', prev[:-2]))
    if prev.endswith('ble') and nxt.startswith('i'):
        cand.append(('ble_bil', prev[:-2] + 'il'))
    if prev.endswith('ic') and nxt == 'ly':
        cand.append(('ic_ally', prev + 'al'))
    if prev.endswith('our'):
        cand.append(('our_or', prev[:-3] + 'or'))
    if prev.endswith('y') and nxt[:1] == 'i':
        cand.append(('y_drop_before_i', prev[:-1]))
    if prev.endswith('c') and nxt[:1] in 'eiy':
        cand.append(('c_ck', prev + 'k'))
    if prev.endswith('ll'):
        cand.append(('ll_l', prev[:-1]))
    if prev.endswith('f'):
        cand.append(('f_v', prev[:-1] + 'v'))
    if prev.endswith('fe'):
        cand.append(('f_v', prev[:-2] + 'v'))
    for k, p2 in cand:
        if rest.startswith(p2 + nxt[:1]) or (rest.startswith(p2) and not nxt):
            return k, p2
    return 'other', None

def labels(d):
    out = {}
    for col in 'JKLM':
        for l in d[col].split('\n'):
            m = re.match(r'^([^：:]{1,40})[：:]', l)
            if m:
                lab = m.group(1).strip()
                out[lab.strip('-').lower()] = (col, lab)
    return out

res = collections.defaultdict(list)
for d in rows:
    LB = labels(d)
    I = d['I'].split('；')[0]
    if ' + ' not in I or d['typ'].startswith(('④', '⑤')): continue
    I = I.split('← ')[-1]
    parts = [norm(p) for p in I.split(' + ')]
    raw = [p.strip() for p in I.split(' + ')]
    w = d['w'].lower().replace('-', '').replace("'", '').replace(' ', '')
    pos = 0
    for i in range(len(parts) - 1):
        k, p2 = boundary(parts[i], parts[i + 1], w[pos:])
        if k == 'other':
            res['other'].append((d['w'], d['I'])); break
        nx = parts[i + 1]
        suf = nx in LB and LB[nx][0] == 'M'
        if k == 'double':
            if not (nx[1:] in LB and LB[nx[1:]][0] == 'M'): k = None
        elif k in ('keep_e_soft', 'keep_e_other', 'drop_e', 'drop_e_cons', 'y_i', 'y_drop_before_i', 'le_ly', 'ble_bil', 'ic_ally'):
            if not suf: k = (k + '_nonsuf') if k in ('drop_e', 'y_i', 'drop_e_cons') else None
        if k: res[k].append((d['w'], raw[i], raw[i + 1]))
        if len(raw[i + 1]) == 1 and raw[i + 1] == raw[i][-1:] and raw[i + 1] not in 'aeiou': res['double_sep'].append((d['w'], d['I']))
        pos += len(p2)
    # 前缀同化：拆分里的 X(=Y)
    for p in raw:
        m = re.match(r'^([a-z]+)\(=([a-z]+)\)$', p)
        if m and m.group(1) != m.group(2) and m.group(1) in LB and LB[m.group(1)][0] == 'J': res['assim'].append((d['w'], p))
json.dump(res, open('/home/claude/work/sp_res.json', 'w'), ensure_ascii=False)
for k, v in sorted(res.items(), key=lambda x: -len(x[1])):
    print(len(v), k, v[:12] if k != 'other' else '')
print('==== other')
print('；'.join('%s=%s' % x for x in res['other']))
