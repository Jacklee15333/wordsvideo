"""英美写法：含义列（F）标出这是英式还是美式写法，并给出另一边的写法。说法统一写在第一行末尾：
   （英式拼写，美式写作 X）/（美式拼写，英式写作 X）——字母不同（colour / color、metre / meter）
   （英式写法，美式多连写成 X）/（美式写法，英式写作 X）——连字符、连写、分开写不同（make-up / makeup）"""
US = {  # 美式拼写的词 → 英式写法
 'watercolor': 'watercolour', 'neighbor': 'neighbour', 'enroll': 'enrol', 'airplane': 'aeroplane', 'skeptic': 'sceptic', 'skeptical': 'sceptical',
 'skepticism': 'scepticism', 'traveler': 'traveller', 'analog': 'analogue', 'leukemia': 'leukaemia', 'artifact': 'artefact', 'armor': 'armour',
 'fulfillment': 'fulfilment', 'mold': 'mould', 'behavior': 'behaviour', 'behavioral': 'behavioural', 'tumor': 'tumour', 'star-centered': 'star-centred',
 'maneuver': 'manoeuvre', 'colorful': 'colourful', 'colorless': 'colourless', 'favorable': 'favourable', 'honorable': 'honourable',
 'self-centered': 'self-centred', 'self-defense': 'self-defence', 'labor': 'labour', 'counselor': 'counsellor', 'color-coded': 'colour-coded',
 'theatergoer': 'theatregoer', 'carrot-colored': 'carrot-coloured', 'carbon-fiber': 'carbon-fibre', 'defense': 'defence', 'cozy': 'cosy',
 'liter': 'litre', 'humor': 'humour', 'jewelry': 'jewellery', 'jeweler': 'jeweller', 'vapor': 'vapour', 'sand-colored': 'sand-coloured',
 'harbor': 'harbour', 'pajamas': 'pyjamas', 'drafty': 'draughty', 'chili': 'chilli', 'rumor': 'rumour', 'Paleolithic': 'Palaeolithic', 'meter': 'metre',
 'color': 'colour', 'neighboring': 'neighbouring', 'neighborhood': 'neighbourhood', 'colored': 'coloured', 'center': 'centre', 'favor': 'favour',
 'favorite': 'favourite', 'honor': 'honour', 'gray': 'grey', 'theater': 'theatre', 'fiber': 'fibre', 'flavor': 'flavour', 'license': 'licence',
}
UK = {  # 英式拼写的词 → 美式写法
 'visualise': 'visualize', 'neighbour': 'neighbor', 'neighbouring': 'neighboring', 'neighbourhood': 'neighborhood', 'neighbourly': 'neighborly',
 'realise': 'realize', 'realisation': 'realization', 'traveller': 'traveler', 'nationalise': 'nationalize', 'fulfil': 'fulfill', 'modernise': 'modernize',
 'mould': 'mold', 'coloniser': 'colonizer', 'analyse': 'analyze', 'ageing': 'aging', 'anti-ageing': 'anti-aging', 'tumour': 'tumor',
 'mechanisation': 'mechanization', 'colour': 'color', 'coloured': 'colored', 'five-coloured': 'five-colored', 'colourfully': 'colorfully',
 'centre': 'center', 'favour': 'favor', 'favourite': 'favorite', 'honour': 'honor', 'labour': 'labor', 'grey': 'gray', 'counselling': 'counseling',
 'counsellor': 'counselor', 'metre': 'meter', 'five-hundred-metre': 'five-hundred-meter', 'kilometre': 'kilometer', 'centimetre': 'centimeter',
 'millimetre': 'millimeter', 'theatre': 'theater', 'defence': 'defense', 'litre': 'liter', 'humour': 'humor', 'equalise': 'equalize',
 'jeweller': 'jeweler', 'jewellery': 'jewelry', 'summarise': 'summarize', 'savour': 'savor', 'flavour': 'flavor', 'fibre': 'fiber',
 'harbour': 'harbor', 'chilli': 'chili', 'rumour': 'rumor', 'two-storey': 'two-story', 'aeroplane': 'airplane', 'catalogue': 'catalog',
 'colourful': 'colorful', 'favourable': 'favorable', 'honourable': 'honorable', 'characterise': 'characterize', 'ruralise': 'ruralize', 'behaviour': 'behavior', 'programme': 'program', 'licence': 'license',
}
SPECIAL = {
 'mechanization': '（英美都用这个写法；英式也写作 mechanisation）',  # 说法要多一句的，整句手写
 'encyclopedia': '（英美通用；英式也写作 encyclopaedia）',
 'yogurt': '（美式拼写，英式也常写作 yoghurt）',
 'yogurt-based': '（美式拼写，英式也常写作 yoghurt-based）',
 'sulfur': '（美式拼写，英式传统写作 sulphur，今天化学界也统一用 sulfur）',
 'axe': '（英式拼写，美式也写作 ax）',
 'judgement': '（英式两种都用，美式多写作 judgment）',
 'judgment': '（美式多写作 judgment；英式两种都用，也写作 judgement）',
 'license': '（美式名词、动词都写 license；英式名词写作 licence，动词也写 license）',
 'licence': '（英式名词拼写，美式写作 license；动词英美都写 license）',
 'program': '（计算机程序英美都写 program；节目、计划英式写作 programme）',
 'programme': '（英式拼写，美式写作 program；计算机程序英美都写 program）',
 'practice': '（名词英美都写 practice；动词美式也写 practice，英式写作 practise）',
 'practise': '（英式动词拼写，美式写作 practice；名词英美都写 practice）',
 'meter': '（米这个意思美式拼写，英式写作 metre；仪表英美都写 meter）',
 'dialog': '（美式拼写，英式写作 dialogue；电脑“对话框”英美都写 dialog）',
 'catalogue': '（英式拼写，美式也常写作 catalog）',
 'analog': '（美式拼写，英式写作 analogue；电子“模拟”英式也常写 analog）',
}
HY = {  # 连字符、连写不同
 'make-up': '（英式写法，美式多连写成 makeup）', 'makeup': '（美式写法，英式多写作 make-up）',
 'hard-working': '（英式写法，美式多连写成 hardworking）', 'hardworking': '（美式写法，英式写作 hard-working）',
 'life-saving': '（英式写法，美式多连写成 lifesaving）', 'lifesaving': '（美式写法，英式写作 life-saving）',
 'second-hand': '（英式写法，美式多连写成 secondhand）', 'secondhand': '（美式写法，英式写作 second-hand）',
 'clean-up': '（英式写法，美式多连写成 cleanup）', 'cleanup': '（美式写法，英式写作 clean-up）',
 'check-up': '（英式写法，美式多连写成 checkup）', 'check-ups': '（英式写法，美式多连写成 checkups）',
 'takeoff': '（美式写法，英式写作 take-off）', 'setup': '（美式写法，英式多写作 set-up）', 'runoff': '（美式写法，英式写作 run-off）',
 'easy-going': '（英式写法，美式多连写成 easygoing）', 'semi-final': '（英式写法，美式多连写成 semifinal）',
 'quarterfinal': '（美式写法，英式写作 quarter-final）', 'mid-term': '（英式写法，美式多连写成 midterm）', 'mid-air': '（英式写法，美式多连写成 midair）',
 'over-reliance': '（英式写法，美式多连写成 overreliance）', 'pre-order': '（英式写法，美式多连写成 preorder）', 'pre-ordered': '（英式写法，美式多连写成 preordered）',
 'percent': '（美式写法，英式多分开写成 per cent）', 'anytime': '（美式写法，英式多分开写成 any time）', 'anymore': '（美式写法，英式多分开写成 any more）',
 'forever': '（英美都连写；英式传统上“永远”也分开写成 for ever）', 'healthcare': '（英式多连写；美式常分开写成 health care）',
}
for _w in 'non-verbal non-profit non-member non-emergency non-physical non-reactive non-polluting non-voluntary non-alien non-migrating non-pink co-writer co-writing co-author co-authored co-produce co-produced'.split():
    HY[_w] = '（英式写法，美式多连写成 %s）' % _w.replace('-', '')
SKIP = 'filter tire draft connection griffin kilogram gram ton tonne medieval monologue prologue dialogue disc disk likeable woolly glamour cancellation archaeology archaeologist archaeological aesthetic aesthetics install instal unrecognizable'.split()
