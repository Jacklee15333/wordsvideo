import json, re
from collections import defaultdict
T = json.load(open('feats.json'))
PART = {'up','out','off','down','over','back','in','on','away','by','around','through','about','along','under'}
NUMW = set('one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million first second third fourth fifth sixth seventh eighth ninth tenth half quarter single double triple'.split())
ADV = set('well best better hard hardest easy long never quick far low tight kind strange tired tough professional foolish sweet salty ancient backwards much highly ready fresh new remotely newly good fast slow'.split())
NED = set('hearted minded aged fashioned haired leafed leaved tailed shelled coated skinned tempered sized capped shaped colored coloured hued sided edged necked toed furred sailed eared eyed headed legged handed patterned scented structured'.split())
IRPP = set('made known held lit written borne broken felt driven led bound woven kept worn paid grown built done born found seen swept spent taken given thrown left sung won fed bred dried knitted'.split())
FUNC1 = set('some any every no'.split()); FUNC2 = set('thing one body where time day way more what how'.split())
def isnum(b): return b.lower() in NUMW or bool(re.fullmatch(r'\d+(st|nd|rd|th)?|\d+D', b))
def stem_ok(b):
    return b
def auto(t):
    w = t['w']; ps = [p['b'] for p in t['parts']]; lw = [x.lower() for x in ps]
    pos = t['pos'][0] if t['pos'] else ''
    if t['type'] != '③ 合成词': return 'PFX'
    if len(ps) >= 3:
        if 'and' in lw: return 'H14'
        if lw[-1] in ('ed', 'd'): return 'H12'
        if len(ps) == 3 and lw[0] == lw[2]: return 'H07'
        return '?3'
    a, b = lw[0], lw[-1]
    if isnum(ps[0]) and isnum(ps[1]): return 'H20' if b in ('third','fifth','quarter') else 'H19'
    if lw[0] == 'self': return 'H34'
    if b in ('self','selves'): return 'H24'
    if a in FUNC1 and b in FUNC2: return 'H22'
    if b == 'ever' and a in ('how','when','where','who','whom','what','which'): return 'H23'
    if b in NED: return 'H12'
    if isnum(ps[0]):
        if pos == 'adj.': return 'H13'
        return 'H01'
    if b in PART:
        return 'H08'
    if a in PART and t['parts'][1]['pos'][:1] == ['v.']: return 'H09'
    if pos == 'v.': return 'H17'
    if b.endswith('ing') and b not in ('thing','string','king','ring','wing','sing','evening','spring','sling','swing','sting'):
        return 'H05' if a in ADV or 'adj.' in t['parts'][0]['pos'][:1] else 'H02'
    if b.endswith('ed') or b in IRPP:
        return 'H05' if a in ADV else 'H04'
    if re.search(r'(er|or)$', b) and t['parts'][1]['in'] and 'n.' in t['parts'][1]['pos'] and b[:-2] and any(x in T_WORDS for x in (b[:-2], b[:-1], b[:-3])):
        return 'H02'
    if pos == 'adj.':
        if 'adj.' in t['parts'][1]['pos'][:1]: return 'H06'
        return 'H07'
    return 'H01'
T_WORDS = set()
rows = json.load(open('/home/claude/work/rows.json'))
VERBS = set()
for r in rows:
    if r[6] and re.search(r'(^|\n)v\. ', str(r[6])): VERBS.add(str(r[5]).lower())
T_WORDS = VERBS
if __name__ == '__main__':
    C = defaultdict(list)
    for t in T: C[auto(t)].append(t['w'])
    json.dump({t['w']: auto(t) for t in T}, open('auto_cat.json','w'), ensure_ascii=False, indent=0)
    for k in sorted(C): print(k, len(C[k])); print(' '.join(C[k])); print()
