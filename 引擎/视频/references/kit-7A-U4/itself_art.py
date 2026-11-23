import sys, os, math
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
def cat(paw=0, tail=0, tongue=False, eyes='open'):
    s = f'<path d="M210,250 C{270+tail*20},{240-tail*10} {290+tail*10},{170} {250+tail*25},{140}" fill="none" stroke="#F28C28" stroke-width="18" stroke-linecap="round"/>'
    s += '<ellipse cx="160" cy="210" rx="78" ry="62" fill="#F28C28"/><ellipse cx="150" cy="232" rx="44" ry="34" fill="#FFE2B8"/>'
    for i in range(3):
        s += f'<path d="M{170+i*22},158 C{176+i*22},180 {176+i*22},200 {168+i*22},220" fill="none" stroke="#C25E12" stroke-width="7"/>'
    s += '<ellipse cx="118" cy="268" rx="22" ry="12" fill="#FFE2B8"/><ellipse cx="196" cy="268" rx="22" ry="12" fill="#F28C28"/>'
    hx, hy = (110, 120) if paw < 2 else (114, 128)
    s += f'<path d="M{hx-42},{hy-20} L{hx-36},{hy-70} L{hx-8},{hy-40} Z" fill="#F28C28"/><path d="M{hx+42},{hy-20} L{hx+36},{hy-70} L{hx+8},{hy-40} Z" fill="#F28C28"/>'
    s += f'<path d="M{hx-34},{hy-30} L{hx-32},{hy-58} L{hx-14},{hy-38} Z" fill="#FF9EB5"/><path d="M{hx+34},{hy-30} L{hx+32},{hy-58} L{hx+14},{hy-38} Z" fill="#FF9EB5"/>'
    s += f'<circle cx="{hx}" cy="{hy}" r="50" fill="#F28C28"/><path d="M{hx-10},{hy-48} L{hx-6},{hy-30} M{hx+10},{hy-48} L{hx+6},{hy-30}" stroke="#C25E12" stroke-width="5"/>'
    s += f'<ellipse cx="{hx}" cy="{hy+22}" rx="26" ry="18" fill="#FFE2B8"/>'
    if eyes == 'open':
        s += f'<ellipse cx="{hx-20}" cy="{hy-4}" rx="8" ry="11" fill="#2E7D32"/><ellipse cx="{hx+20}" cy="{hy-4}" rx="8" ry="11" fill="#2E7D32"/><circle cx="{hx-18}" cy="{hy-8}" r="3" fill="#FFF"/><circle cx="{hx+22}" cy="{hy-8}" r="3" fill="#FFF"/>'
    else:
        s += f'<path d="M{hx-28},{hy-2} q8,8 16,0 M{hx+12},{hy-2} q8,8 16,0" fill="none" stroke="#1B1A1F" stroke-width="4"/>'
    s += f'<path d="M{hx-5},{hy+12} L{hx+5},{hy+12} L{hx},{hy+18} Z" fill="#E8407A"/>'
    for d in (-1, 1):
        for k in (-1, 0, 1):
            s += f'<path d="M{hx+d*20},{hy+20} L{hx+d*58},{hy+14+k*9}" stroke="#7A4A20" stroke-width="2"/>'
    if tongue:
        s += f'<ellipse cx="{hx+4}" cy="{hy+32}" rx="7" ry="9" fill="#FF6F91"/>'
    if paw == 0:
        s += '<rect x="106" y="230" width="26" height="40" rx="12" fill="#F28C28"/>'
    elif paw == 1:
        s += f'<path d="M150,236 C150,200 {hx+30},{hy+60} {hx+16},{hy+40}" fill="none" stroke="#F28C28" stroke-width="26" stroke-linecap="round"/><circle cx="{hx+16}" cy="{hy+40}" r="15" fill="#FFE2B8"/>'
    else:
        s += f'<path d="M150,236 C150,206 {hx+34},{hy+66} {hx+12},{hy+46}" fill="none" stroke="#F28C28" stroke-width="26" stroke-linecap="round"/><circle cx="{hx+12}" cy="{hy+46}" r="15" fill="#FFE2B8"/>'
    return svg(320, 290, s)
def cushion():
    return svg(320, 90, '<ellipse cx="160" cy="45" rx="150" ry="38" fill="#9B5DE5"/><ellipse cx="160" cy="36" rx="128" ry="24" fill="#B98AF0"/>')
def yarn():
    return svg(100, 100, '<circle cx="50" cy="50" r="40" fill="#E8304A"/><path d="M18,40 C40,30 70,60 84,46 M20,62 C44,50 66,78 82,64 M34,16 C50,40 46,70 60,90" fill="none" stroke="#FFFFFF" stroke-width="4"/>')
for i, (p, t, tg, e) in enumerate(((0, 0, False, 'open'), (1, 1, False, 'closed'), (2, 1, True, 'closed'), (1, 0, True, 'closed'))):
    write_art(ART, f'cat-lick_f{i}.svg', cat(p, t, tg, e))
write_art(ART, 'cat-sit_f0.svg', cat(0, 0)); write_art(ART, 'cat-sit_f1.svg', cat(0, 1)); write_art(ART, 'cat-sit_f2.svg', cat(0, 0, eyes='closed'))
write_art(ART, 'cushion.svg', cushion()); write_art(ART, 'yarn.svg', yarn())
M = {}
SELF = (8, 96, -78, 84, 'point')
M['cn-boy-self'] = frames_out(ART, 'cn-boy-self', [person('cn-boy', right=SELF, mouth='open', brows='up', tilt=-3), person('cn-boy', right=SELF, mouth='half', brows='up', tilt=2)], fps=3, seq='pingpong')
M['west-boy-laugh'] = frames_out(ART, 'west-boy-laugh', [person('west-boy', left='chest', mouth='laugh', eyes='happy', tilt=4), person('west-boy', left='chest', mouth='smile', eyes='happy', tilt=-2)], fps=2.5, seq='pingpong')
M['west-woman-show'] = frames_out(ART, 'west-woman-show', [person('west-woman', left='present', right='present2', mouth='open', brows='up'), person('west-woman', left='present2', right='present', mouth='half', tilt=3)], fps=2.6)
M['cn-girl-point'] = frames_out(ART, 'cn-girl-point', [person('cn-girl', right='point', mouth='open', look=1, brows='up'), person('cn-girl', right='point', mouth='half', look=1, tilt=2)], fps=3)
json.dump(M, open(os.path.join(ART, 'word_motions.json'), 'w'), ensure_ascii=False, indent=1)
open(os.path.join(ART, 'icon-it.svg'), 'w').write(svg(200, 200, nest(open(os.path.join(ART, 'cat-sit_f0.svg')).read(), 10, 20, 180, 163)))
open(os.path.join(ART, 'icon-self.svg'), 'w').write(svg(200, 200, nest(person('cn-boy', right=SELF, mouth='open'), -20, 0, 240, 190)))
print(list(M))
