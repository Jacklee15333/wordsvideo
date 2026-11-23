# 逐条人工判断结果（每行 10 条）。代码：
# c 核心不变换对象  f 作用像  s 样子像  n 专指  w 越用越宽  a 做事的人→东西/程序  p 比喻人  l 地方→那儿的人
# b 具体→抽象  o 换代沿用旧名  r 动作→做出来的东西  t 动作→用的东西  h 性质→有这性质的东西  m 材料→用它做的东西
# j 动作/东西→做这事的人  e 委婉  k 感觉→性格  g 夸张→程度  q 计量单位  v 东西→当动词  x 不标
DOM = """
w f h c n x c b c c
c c c c c x x c c f
x f c x n c c f f x
x c c c n n c w f n
c c c c x n n n c c
c x c c x s f x c t
c c c l c x c c c t
c c h c c n x c c f
x x x c b c c c c x
n x c c n c c c x c
n x f c c c c b x c
n x c x n h x f c c
c x x x c c c x c s
c c x c c c r a x n
c f f l x x c c x x
c c c f f w c x c x
c x r c c c x c x a
x c c c x x x w x c
x c c c c c c x x x
c c c c c x f c c a
c c c x c c c c c c
x x c c c c c c c c
x x f c f f x x c x
c n x s x x x c a c
f f c r r c x c c x
x x a c n c x x c c
c x c x n c x b c c
x x x x n c c f x f
c c c c c x c c c c
x c c c x c x f f c
x f c c c c c x c c
n a m x c c c n x x
f c f x s s c w c c
c c c f x n o x f l
l t a a c f x x x x
c c c c c x c c c c
w f c c x c c c c c
c c c c f x a x x c
f f c x c x c c c c
c c f c c x x c x s
c f f c f n c x n x
n x x f c f c x c x
x x m c f c c c c r
c c w x c x c c f x
f c f n c c c c f w
c c c f c x s c f x
c c x s x c f c c c
n c c x w x x x x f
x x w f s x f c f c
x x x c f x f x n c
c c c x f f f c x x
c p f c f c c a c x
x c f c w p f m c w
c f f c x c f x x x
c c c f x c s c c x
c c r x n c x c c c
c f x f f x x x c c
x
""".split()
REG = """
c c c x c c o o c c
c c c h c c c n x x
c c e h k c c x x x
x x x c c c x c c c
s x c n h h x c x x
x c c c j x x c x x
c c c h x c f o x f
c c c c c x x c n n
h r c x c x c c c t
x x v t c x x x c x
x x s c c x x x n f
b c c c c c c c p c
x c x g q f c w c w
c c c n c n f p c j
c s o o a
c c c x x x s c x c
c s x x c x c c h n
s f x c h j x x n t
x x x x x x x x n c
x c x x x s o h s x
x x c s b o w x h c
c f c x x x x n x x
x m h x f h x e x x
c x s n x c c s c c
m x x x c s x r f x
c o x x h x x p x x
x x x b w w x x x x
c s c n s x x x x s
c x x x x x x s c c
k x x x x
""".split()
if __name__=='__main__':
    import collections
    print(len(DOM),len(REG)); print(collections.Counter(DOM)); print(collections.Counter(REG))
