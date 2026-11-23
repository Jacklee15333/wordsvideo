# -*- coding: utf-8 -*-
"""复杂例词的名单（lizi.py 用；project_rules.md 第 76、79–81 条）。单词都用小写。
规则本身在 lizi.py：词缀行的例词在表里带词根就去掉；不在表里的，去掉词缀剩下的是表里的词就留。下面只记逐个看过、和规则不一样的。"""

# 学生认识、总表里却没有单独一行的基础词（判断“去掉词缀剩下的是不是认识的词”时算认识）
BASIC = set('big fast small tall ten mouth brother mother orange bus smoke drunk watt japan america paris murder john tom picture pharmacy muscle'.split())

# 表里带词根、也留着的例词：国名、民族名（English 在表里拆成 Engl(e) + ish，可它是学生最熟的“…国的”，和 Spanish、Danish 一起留）、
# 月份名、数词、不规则的比较级最高级（fifteen、best、inner），和讲“成双的东西用复数”的 scissors——这些例词讲的不是怎么拆
KEEP_IN = set('english irish portuguese australia january fifteen best inner scissors'.split())

# 表里没有、规则判成“复杂”、逐个看过可以留的（简单词 + 词缀，或讲的不是拆分）
OK_OUT = set('''atypical archbishop archenemy semicircle semifinal inactive megawatt minibus non-smoker
american japanese danish parisian elizabethan victorian always quickly taller smaller faster fastest bigger biggest tenth fortieth thirteen
drunkard mouthful brotherhood motherhood cuttings shavings clippings johnny tommy granny doom readable innermost kitchenette epochs john's
islet frankfurter teacher orangeade observatory murderous justice ballot picturesque pharmacist muscular america bulgaria'''.split())

# 表里没有、去掉词缀剩下的碰巧是表里的词、其实还得再拆的（triad 不是 try + ad）
DROP_OUT = set('triad animal hence agile vanilla aspirin canine morphine inferior perish darling saloon duress traverse diffuse maniac solitude partisan module'.split())

# “见 X”的例外：(本词, X) 留着不去
SEE_KEEP = set()

# 个别行的改写：{(单词, 标签): [(原来的半句, 换成)]}
FIX = {
    ('proportion', 'pro-'): [('（不是 progress 里的“向前”）', '（不是“向前”的意思）')],
}

# 词根列：ROOT_KEEP 留着的例词；ROOT_DROP (本词, 例词) 规则认不出、逐个看过要去掉的（表里没有的“前缀 + 这个词根”）
ROOT_KEEP = set("wouldn't alchemy".split())          # 讲的是同一个写法（-n't、阿拉伯语的 al-），不是让学生去拆
ROOT_DROP = set([
    # 表里的词：写法变了、规则对不上的同一个词根
    ('manipulate', 'complete'), ('delay', 'relax'), ('couple', 'adapt'),
    ('fatigue', 'navigate'), ('fatigue', 'mitigate'), ('octopus', 'centipede'), ('reciprocal', 'progress'), ('pilgrim', 'agriculture'),
    ('recognition', 'cognition'), ('millennium', 'anniversary'),
    # 表里没有的词：前缀 + 这个词根、词根 + 词根，规则认不出前缀的
    ('result', 'exult'), ('millennium', 'centennial'), ('mural', 'intramural'), ('monarch', 'hierarchy'), ('refund', 'confound'),
    ('illusion', 'allude'), ('illusion', 'interlude'), ('ancestor', 'predecessor'), ('damage', 'condemn'), ('privilege', 'legislation'),
    ('leukemia', 'leukocyte'), ('leukemia', 'anemia'), ('helicopter', 'pterodactyl'), ('medieval', 'primeval'), ('parent', 'viviparous'),
    ('retrieve', 'contrive'), ('adolescent', 'convalesce'), ('adjust', 'juxtapose'), ('carnival', 'carnivore'), ('enthusiasm', 'theology'),
])
