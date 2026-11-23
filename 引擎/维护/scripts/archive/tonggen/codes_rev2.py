# 其余规律的逐条复核（= 不动；x 去掉；别的字母是换成哪一条）
TOOL = """
c c c c b x = = f x
x x x x b = x x x x
x = x r x x = x x f
x x x x = x = x = x
= x x x = = = = x b
= c = = x x = x x x
m = = x x a x r x =
= x x x x x s x x x
= r r f x x x x x x
= x = h x x = = x x
x x x = x x f x x x
s f x x x f x x x x
x = x x x = s x x
""".split()
RESULT = """
= = = = = x = x x x
= = x = = = x = x x
x x x x x x x = = =
= x = x x x = x = =
x x x x = x x x = =
= x = x x x x = x x
x = = = x x x = = x
x x x x = = = x x x
= = = = x x = x = s
x x = m = = x x x x
= = = = x x
""".split()
SMALL1 = {0:'x',4:'x',7:'b',11:'h',14:'h',23:'x',24:'x',27:'x',40:'h',48:'x',49:'h',50:'h',51:'x',73:'x',77:'x',81:'h',90:'x',91:'x',95:'b',
          104:'h',105:'x',123:'h',125:'x',126:'h',129:'x',135:'x',137:'x',141:'x',142:'x',143:'b',146:'x',147:'x',153:'x',156:'x',157:'x',164:'x',
          166:'x',167:'x',171:'x',172:'x',173:'x',184:'h',200:'x',207:'x',210:'x',212:'x',213:'x',215:'x'}
V2N = {w:'x' for w in 'no nowhere while forever if meanwhile plus underneath aside must club worth south ceasefire percent item third acid sea-crossing she yes dusk farewell lullaby'.split()}
V2N.update({w:'h' for w in 'still plain prime right safe international grown-up green not-for-profit antique cold hollow blank single throw-away blind young saltwater sore mini sweet fat swift'.split()})
V2N['behind'] = 'e'
HOLDER = {'vegetable':'x','cereal':'x','manuscript':'x','panic':'x','numeral':'x','crook':'x','mimic':'j'}
N2V = {w:'x' for w in 'while issue except club bit blueprint concert lap dine'.split()}
N2ADJ = {w:'x' for w in 'through well together exact then up sometime just own upstream downstream random'.split()}
if __name__=='__main__': print(len(TOOL),len(RESULT))
