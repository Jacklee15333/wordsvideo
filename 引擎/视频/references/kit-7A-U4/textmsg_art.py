import sys, os, json
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
CJK = 'font-family="Noto Sans CJK SC, sans-serif" font-weight="700"'
EN = 'font-family="Noto Sans, DejaVu Sans, sans-serif" font-weight="700"'


def chat(stage):   # 手机聊天界面：0 空的、1 妈妈发来一条、2 我回了一条、3 我正在打字
    s = '<rect x="0" y="0" width="260" height="480" rx="36" fill="#2B2D33"/><rect x="14" y="40" width="232" height="400" rx="8" fill="#EDEFF3"/>'
    s += '<rect x="104" y="16" width="52" height="9" rx="4" fill="#4A4F59"/><circle cx="130" cy="460" r="11" fill="#4A4F59"/>'
    s += '<rect x="14" y="40" width="232" height="54" fill="#F7F9FC"/><path d="M14,94 L246,94" stroke="#D5DAE1" stroke-width="2"/>'
    s += f'<circle cx="46" cy="67" r="17" fill="#F79CBB"/><circle cx="46" cy="62" r="7" fill="#FFFFFF"/><path d="M34,80 C36,70 56,70 58,80" fill="#FFFFFF"/>'
    s += f'<text x="74" y="74" font-size="20" fill="#1B1A1F" {CJK}>妈妈 Mom</text>'
    if stage >= 1:
        s += '<path d="M24,140 L16,150 L30,146 Z" fill="#FFFFFF"/><rect x="24" y="110" width="178" height="46" rx="14" fill="#FFFFFF"/>'
        s += f'<text x="38" y="140" font-size="17" fill="#1B1A1F" {EN}>Dinner is ready!</text>'
        s += f'<text x="30" y="172" font-size="11" fill="#8C939E" {EN}>18:02</text>'
    if stage == 2:
        s += '<path d="M236,214 L244,224 L230,220 Z" fill="#95EC69"/><rect x="110" y="184" width="126" height="46" rx="14" fill="#95EC69"/>'
        s += f'<text x="126" y="214" font-size="17" fill="#1B1A1F" {EN}>OK, Mom!</text>'
    if stage == 3:
        s += '<rect x="160" y="184" width="76" height="40" rx="14" fill="#95EC69"/>' + ''.join(f'<circle cx="{180+k*18}" cy="204" r="5" fill="#3A7D2A"/>' for k in range(3))
    s += '<rect x="22" y="404" width="180" height="28" rx="14" fill="#FFFFFF"/><circle cx="222" cy="418" r="14" fill="#2E6FD9"/><path d="M215,418 L229,418 M223,412 L229,418 L223,424" stroke="#FFFFFF" stroke-width="3" fill="none"/>'
    return svg(260, 480, s)


def phone_hold():   # 拿在手里的小手机（屏幕亮着、有两条消息）
    s = '<rect x="0" y="0" width="90" height="160" rx="14" fill="#2B2D33"/><rect x="6" y="14" width="78" height="132" rx="4" fill="#EDEFF3"/>'
    s += '<rect x="12" y="30" width="52" height="16" rx="6" fill="#FFFFFF"/><rect x="30" y="54" width="48" height="16" rx="6" fill="#95EC69"/><rect x="12" y="78" width="40" height="16" rx="6" fill="#FFFFFF"/>'
    return svg(90, 160, s)


def notebook():   # 摊开的本子：左页标题、几行字，右页横线
    s = '<path d="M10,30 L180,18 L180,222 L10,232 Z" fill="#FFFDF5"/><path d="M180,18 L350,30 L350,232 L180,222 Z" fill="#FFFDF5"/>'
    s += '<path d="M180,18 L180,222" stroke="#C9B48A" stroke-width="4"/>'
    for k in range(7):
        y = 66 + k * 22
        s += f'<path d="M24,{y+2} L168,{y-6}" stroke="#BFD4EA" stroke-width="2"/><path d="M192,{y-6} L338,{y+2}" stroke="#BFD4EA" stroke-width="2"/>'
    return svg(360, 240, s)


def writing():   # 本子上写的字（单独一层，写的时候出来）
    s = f'<text x="40" y="58" font-size="22" fill="#2E6FD9" {EN} transform="rotate(-4 40 58)">My Day</text>'
    for k, t in enumerate(('I get up at 7.', 'I go to school', 'by bike.', 'I like English.')):
        s += f'<text x="30" y="{94+k*22}" font-size="15" fill="#1B3A6B" font-family="Noto Sans, sans-serif" transform="rotate(-4 30 {94+k*22})">{t}</text>'
    for k, t in enumerate(('Aa Bb Cc', 'text = 文字', 'words, words')):
        s += f'<text x="200" y="{70+k*24}" font-size="15" fill="#1B3A6B" font-family="Noto Sans CJK SC, sans-serif" transform="rotate(4 200 {70+k*24})">{t}</text>'
    return svg(360, 240, s)


def pencil():
    s = '<path d="M0,12 L20,4 L20,20 Z" fill="#F4D7A8"/><path d="M0,12 L7,9.5 L7,14.5 Z" fill="#3A3F4B"/><rect x="20" y="4" width="84" height="16" fill="#F2C230"/><rect x="104" y="4" width="16" height="16" fill="#E8407A"/>'
    return svg(120, 24, s)


def msg_bubble():   # 说话的气泡，里面一封信：口信、消息
    s = '<path d="M20,10 L200,10 C212,10 220,18 220,30 L220,120 C220,132 212,140 200,140 L80,140 L44,168 L52,140 L20,140 C8,140 0,132 0,120 L0,30 C0,18 8,10 20,10 Z" fill="#FFFFFF"/>'
    s += '<rect x="50" y="40" width="120" height="76" rx="6" fill="#F2C230"/><path d="M50,42 L110,86 L170,42" fill="none" stroke="#B5832A" stroke-width="5"/><circle cx="110" cy="96" r="10" fill="#E8304A"/>'
    return svg(220, 170, s)


def icon_text():
    s = '<rect x="30" y="16" width="140" height="170" rx="10" fill="#FFFDF5"/><text x="60" y="76" font-size="44" fill="#2E6FD9" ' + EN + '>Aa</text>'
    for k in range(4):
        s += f'<rect x="50" y="{98+k*20}" width="{100 - (k % 2) * 30}" height="8" rx="4" fill="#8C939E"/>'
    return svg(200, 200, s)


def icon_message():
    s = '<path d="M30,30 L170,30 C182,30 190,38 190,50 L190,140 C190,152 182,160 170,160 L80,160 L50,186 L56,160 L30,160 C18,160 10,152 10,140 L10,50 C10,38 18,30 30,30 Z" fill="#FFFFFF"/>'
    s += '<rect x="50" y="58" width="100" height="68" rx="6" fill="#F2C230"/><path d="M50,60 L100,98 L150,60" fill="none" stroke="#B5832A" stroke-width="5"/>'
    return svg(200, 200, s)


for k in range(4):
    write_art(ART, f'chat{k}.svg', chat(k))
write_art(ART, 'notebook.svg', notebook()); write_art(ART, 'writing.svg', writing()); write_art(ART, 'pencil.svg', pencil())
write_art(ART, 'msg-bubble.svg', msg_bubble()); write_art(ART, 'icon-text.svg', icon_text()); write_art(ART, 'icon-message.svg', icon_message())
ph = phone_hold()
A = (20, 100, 120, 70, 'fist')
M = {}
M['cn-boy-type'] = frames_out(ART, 'cn-boy-type', [holding('cn-boy', ph, 322, 262, 86, 150, left=A, right=A, mouth='smile', tilt=-3),
                                               holding('cn-boy', ph, 322, 262, 86, 150, left=A, right=A, mouth='half', tilt=2)], fps=2.5, seq='pingpong')
M['cn-boy-read'] = frames_out(ART, 'cn-boy-read', [holding('cn-boy', ph, 322, 262, 86, 150, left=A, right=A, mouth='o', eyes='wide', brows='up'),
                                               holding('cn-boy', ph, 322, 262, 86, 150, left=A, right=A, mouth='laugh', eyes='happy', tilt=3)], fps=1.2, seq='pingpong')
M['west-girl-text'] = frames_out(ART, 'west-girl-text', [holding('west-girl', ph, 322, 262, 86, 150, left=A, right=A, mouth='open', brows='up', look=1),
                                                     holding('west-girl', ph, 322, 262, 86, 150, left=A, right=A, mouth='half', look=1, tilt=2)], fps=3, seq='pingpong')
M['west-woman-phone'] = frames_out(ART, 'west-woman-phone', [holding('west-woman', ph, 322, 262, 86, 150, left=A, right=A, mouth='smile', eyes='open', tilt=-2),
                                                         holding('west-woman', ph, 322, 262, 86, 150, left=A, right=A, mouth='laugh', eyes='happy', tilt=2)], fps=1.5, seq='pingpong')
M['cn-girl-type'] = frames_out(ART, 'cn-girl-type', [holding('cn-girl', ph, 322, 262, 86, 150, left=A, right=A, mouth='smile', eyes='happy', tilt=3),
                                                 holding('cn-girl', ph, 322, 262, 86, 150, left=A, right=A, mouth='half', eyes='open', look=1, tilt=-1)], fps=2.5, seq='pingpong')
json.dump(M, open(os.path.join(ART, 'word_motions.json'), 'w'), ensure_ascii=False, indent=1)
print(list(M))
