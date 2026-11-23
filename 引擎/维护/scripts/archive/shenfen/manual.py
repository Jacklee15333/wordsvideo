# -*- coding: utf-8 -*-
"""第 34 轮手工定的几处（自动规则办不了的）"""
HEQI_FIX = {
 'gesture': ['拉丁语 gestus“举止、姿态”'],
 'except': ['拉丁语 excipere“拿出来”（“拿出来了”的形式是 exceptus）'],
 'concept': ['拉丁语 concipere“收在里面”（“抓住了”的形式是 conceptum）'],
 'perceive': ['拉丁语 percipere“彻底抓住”'],
 'circuit': ['拉丁语 circuitus“绕着走一圈”'],
 'construct': ['拉丁语 constructus“垒到一起的”（直接拿来当英语动词）'],
 'commotion': ['拉丁语 commovere“一起动、彻底地动”（“被…了的”词干是 commot-）'],
 'fluorescent': [],
 'provoke': ['拉丁语 provocare“叫出来、向前叫”'],
}
PRE_SKIP = {'survey'}
# 词根列：整格手改（原文里的一段 → 新的一段），再加“合起来”
ROOT_PATCH = {
 'commit': [('-mit：放、送；拉丁语 committere =“放到一起、连接”→ 交到别人手里', '-mit：放、送（拉丁语 mittere）', '拉丁语 committere =“放到一起、连接”→ 交到别人手里')],
 'arrogant': [('；ad + rogare = arrogare“朝自己这边要” → 替自己要、据为己有', '', '拉丁语 ad + rogare = arrogare“朝自己这边要”→ 替自己要、据为己有')],
 'intrigue': [('；intricāre =“使缠在里面”→ 缠住、弄糊涂、使为难（同 intricate 错综复杂的）', '', '拉丁语 intricāre =“使缠在里面”→ 缠住、弄糊涂、使为难（同 intricate 错综复杂的）')],
}
ROOT_AFTER = {   # 方案生成以后再补一句（词根本身的事，留在词根行）
 'fluorescent': ('意思：flu“流”（拉丁语 fluere）', '意思：flu“流”（拉丁语 fluere）；这里的 fluor 指萤石：萤石容易熔化、常拿来作助熔剂，所以叫 fluor（fluorspar）'),
}
PRE_PATCH = {
 'relevant': ('；re + lev 合起来是“把重担举起来 → 减轻”', '', 're + lev =“把重担举起来”→ 减轻'),
 'compulsory': ('；拉丁语 compellere“赶到一起”→“强迫”', '', '拉丁语 compellere“赶到一起”→“强迫”'),
}
WP_MOVE = {'impromptu', 'discount', 'account', 'amount', 'enchant'}      # 单词部分列里单独一行讲“合起来”的，挪到组合列
# 辨析列：手写的样板（视频第三部分照它讲）
BIANXI = {
 'produce': '''【同义词】产品：produce（农产品）、product
【同义词】制造：produce、make
【同义词】产生：produce、generate
produce 当名词是“农产品”：地里长出来的蔬菜、水果，是一大类东西，不可数（fresh produce 新鲜农产品）
product 是“产品”：工厂造出来、拿去卖的东西，可以一件一件数（a new product 一件新产品）
逻辑不同：produce 用的是动词原形 duce，是把动词“生产”直接当名词用，说的是“地里产出来的那一类东西”；product 用的是过去分词 duct“被领出来的”，说的是“已经造好的一件东西”
make 是最普通的“做、制造”；produce 多指成批地造出来，或者自然地长出、带来（produce cars 生产汽车、produce milk 产奶）
generate 多说产生电、热、想法、收入（generate electricity 发电）
produce evidence / a passport 是“拿出来给人看”，正是“领到前面来”的本义''',
 'product': '''【同义词】产品：product、produce（农产品）
【同义词】结果：product、result、outcome、consequence、effect
product 是可数的“产品”：工厂造出来、拿去卖的一件件东西（a new product 一件新产品）
produce 是不可数的“农产品”：地里长出来的蔬菜、水果（fresh produce 新鲜农产品）
逻辑不同：product 用的是过去分词 duct“被领出来的”，说的是“已经造好的一件东西”；produce 用的是动词原形 duce，是把动词“生产”直接当名词用，说的是“地里产出来的那一类东西”
production 是“生产（过程）、产量、作品”
说“结果”时，result 最普通；product 强调“是某个过程造出来的”（the product of hard work 努力的结果）''',
}
