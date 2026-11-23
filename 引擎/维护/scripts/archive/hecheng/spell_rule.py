import re, json
from gen import CATS, BYW, parts
SUFLIKE = set('like free friendly based related shaped colored coloured powered driven sized style era wide proof scented centered'.split())
OPENUSUAL = set('''dining-room spinning-wheel science-fiction first-aid rush-hour solar-energy power-supply career-exploration social-identity
video-editing time-management video-call time-travel carbon-fiber gold-leaf stained-glass wooden-barrel half-flush full-flush
student-teacher hot-dog sea-crossing language-teaching city-driving line-sharing tree-planting water-testing climate-control
limited-edition high-definition zero-gravity fast-food'''.split())
PAIRS = set('anytime anyone anymore anyway anybody everyday everyone someday sometime somebody someone nobody nothing maybe already altogether onto forever faraway'.split())
DROPS = set('also although almost already altogether alone welfare fulfil until pastime Christmas roommate earring granddaughter nighttime bookkeeper withhold gospel bonfire shepherd'.split())
LETTER = re.compile(r'^(\d|e-|x-|ai-|vr-|3d|wh-|to-)', re.I)
def spell_rule(t):
    w = t['w']; c = CATS[w]; ps = parts(t); pos = t['pos'][0] if t['pos'] else ''
    if "'" in w: return 'W15'
    if c == 'PFX':
        if w in ('peep-peep-peep', 'tuk-tuk'): return 'W14'
        if w.endswith('-like'): return 'W08'
        return 'W13'
    if c == 'H08': return 'W04'
    if '-' in w:
        if c == 'H34': return 'W07'
        if LETTER.match(w): return 'W06'
        if c in ('H19', 'H20'): return 'W05'
        if c == 'H14': return 'W09'
        if len(ps) >= 3 and c == 'H07': return 'W10'
        if c == 'H08': return 'W04'
        if ps[-1].lower() in SUFLIKE: return 'W08'
        if ps[0].lower() in ('highly', 'remotely', 'environmentally'): return 'W18'
        if w in OPENUSUAL: return 'W16'
        if pos in ('adj.', 'adv.'): return 'W03'
        return 'W02'
    if w[0].isupper(): return 'W17'
    if w in PAIRS: return 'W11'
    if w in DROPS: return 'W12'
    return 'W01'
if __name__ == '__main__':
    from collections import Counter
    T = json.load(open('feats.json'))
    print(Counter(spell_rule(t) for t in T))
