"""把一个词的分析结果写成含义列的新格式：每个意思一行，行首是词性"""
import re

def line_of(o, pos=None, rest=None):
    p = pos or (o['pos'][0] if o['pos'] else 'n.')
    labs = ''.join('（' + l + '）' for l in o['labels'])
    body = rest if rest is not None else o['rest']
    if not body.strip() and o['labels'] and rest is None:      # 只有“（change 的过去式、过去分词）”：去掉括号当正文
        labs = ''; body = '，'.join(o['labels'])
    circ = (o.get('circ') + ' ') if o.get('circ') else ''
    return (p + ' ' + circ + labs + body).strip()

def render(a, pos_over=None, text_over=None, skip=None):
    lines = []
    for o in a:
        k = o['k']
        if skip and k in skip: continue
        p = (pos_over or {}).get(k)
        if p is None:
            p = '/'.join(o['pos']) if o['pos'] and len(o['pos']) > 1 else (o['pos'][0] if o['pos'] else 'n.')
        lines.append(line_of(o, p, (text_over or {}).get(k)))
    return '\n'.join(lines)
