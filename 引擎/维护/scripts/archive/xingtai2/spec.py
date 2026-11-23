# -*- coding: utf-8 -*-
"""2026-11 词根形态补齐轮：表里只出现一种写法（或从没立过族）的拉丁语动词词根。F 新立一族，C 照搬已有词根族的三个样子，J 已有词根族补写法。
写法代号：B 原样 / E 原形加不发音的 e / W 前面有前缀时元音弱化 / P 过去分词 / PE 过去分词加不发音的 e / F 经法语 / G 现在分词里的样子 / L 带连接元音；
(代号, 一句话) 是这个写法自己的说明。"""
ARE = '-are 这一类动词变得最整齐：过去式是词根加 -avi；过去分词是词根加 -atus'
IRE = '-ire 这一类动词也很整齐：过去式是词根加 -ivi；过去分词是词根加 -itus'
DEP = '这个动词只有被动的样子，没有单独的过去式'
REDUP = '过去式把开头的音重复一遍'
SAME = '过去式不变样，词根直接加词尾'
S = []
def F(g, root, inf, zh, perf, pp, rule, sp, cut=None, gloss=None, pzh=None, ppzh=None, intr=False):
    S.append(dict(t='F', key=(g, root), inf=inf, zh=zh, perf=perf, pp=pp, rule=rule, sp=sp, cut=cut, gloss=gloss, pzh=pzh, ppzh=ppzh, intr=intr))
def C(g, root, src, sp): S.append(dict(t='C', key=(g, root), src=src, sp=sp))
def J(key, sp): S.append(dict(t='J', key=key, sp=sp))
W_A = ('W', '前面有前缀时元音 a 弱化成 i')
F(32,'port','portare','搬运','portavi','portatus',ARE,{'port':'B','porta':('B','意大利语的命令式 porta“拿着！”')})
for g in (55,190,276): C(g,'cap',(370,'cap'),{'cip':W_A})
C(802,'cap',(370,'cap'),{'ce':('W','在 princeps 里 a 弱化成 i，又经法语磨成 ce')})
F(75,'cid','caedere','砍、切','cecidi','caesus',REDUP+'（ce-cid-i），ae 也弱化成了 i；过去分词是 caed 加 t，d 碰上 t 变成 s（写成 caes）',
  {'cide':('W','前面有前缀时 ae 弱化成 i，英语加不发音的 e'),'cise':('PE','前面有前缀时 ae 弱化成 i，英语加不发音的 e'),'sciss':('P','合成词里写成 cis，开头的 sc 是后来加上的'),'ce':('B','caed 在 m 前掉了 d，ae 写成 e')},pzh='砍了',ppzh='被砍的')
F(94,'gno','noscere','认识','novi','notus','过去式是 no 加 v；过去分词是 no 加 t',
  {'not':'P','noti':('P','过去分词 not 带上连接元音 i'),'cogn':('B','co 加 gno（cognoscere），g 还留着'),'gnit':('P','cognoscere 的过去分词 cognitus 里的样子，g 还留着'),'no':'B','quaint':('P','cognitus 经俗拉丁语、古法语磨成的样子')},
  cut='原形去掉词尾 -ere 是 nosc，再去掉表示“开始、渐渐”的 sc 就是 no，古拉丁语开头还有 g（noscere → no）',gloss='知道、认识')
F(96,'sum','sumere','拿、取','sumpsi','sumptus','过去式是 sum 加 s，m 和 s 中间多出一个 p（写成 sumps）；过去分词是 sum 加 t，m 和 t 中间也多出一个 p（写成 sumpt）',{'sume':'E'})
F(96,'em','emere','拿、买','emi','emptus','过去式只把元音 e 念长，写法不变；过去分词是 em 加 t，m 和 t 中间多出一个 p（写成 empt）',{'mpt':('P','pro 和 emere 连在一起时 e 脱落，empt 写成 mpt')})
F(105,'plex','plectere','编','plexi','plexus','过去式、过去分词里 t 掉了，c 和 s 合写成 x（写成 plex）',{'plex':'P'})
F(107,'tect','tegere','盖、遮','texi','tectus','过去式是 teg 加 s，g 和 s 合写成 x（写成 tex）；过去分词是 teg 加 t，g 在 t 前面写成 c（写成 tect）',{'tect':'P'})
F(110,'reg','regere','使直、引导','rexi','rectus','过去式是 reg 加 s，g 和 s 合写成 x（写成 rex）；过去分词是 reg 加 t，g 在 t 前面写成 c（写成 rect）',{'reg':'B','rect':'P'},pzh='引导了',ppzh='被弄直的')
F(112,'leg','legere','拾、读','legi','lectus','过去式只把元音 e 念长，写法不变；过去分词是 leg 加 t，g 在 t 前面写成 c（写成 lect）',
  {'leg':'B','lect':'P','less':('P','过去分词 lect 经法语，ct 并成了 ss'),'lig':('W','前面有前缀时元音 e 弱化成 i')},ppzh='被拾起的')
F(117,'ject','iacere','扔','ieci','iactus','过去式只换元音，a 换成 e；过去分词是 iac 加 t',{'ject':('P','前面有前缀时 a 弱化成 e（proiectus），拉丁语的 i 后来写成 j')},ppzh='被扔出的')
F(122,'ag','agere','做、推动','egi','actus','过去式只换元音，a 换成 e；过去分词是 ag 加 t，g 在 t 前面写成 c（写成 act）',{'ag':'B','actu':('P','过去分词 act 带着名词 actus 里的 u')},ppzh='被做的')
for g in (1126,2079): C(g,'ag',(122,'ag'),{'ig':('W','前面接了别的成分，a 弱化成 i')})
F(123,'fess','fateri','承认、说出来',None,'fassus',DEP+'；过去分词是 fat 加 t，t 碰上 t 变成 ss（写成 fass）',{'fess':('P','前面有前缀时 a 弱化成 e（confessus）')},
  cut='原形去掉词尾 -eri 就是 fat（fateri → fat）',ppzh='承认了的')
for g in (131,158,625): C(g,'fac',(228,'fac'),{'fic':W_A})
F(132,'dat','dare','给','dedi','datus',REDUP+'（de-d-i）；过去分词是 da 加 t',{'dat':'P'},cut='原形去掉词尾 -re 就是 da（dare → da）',ppzh='被给出的')
F(132,'don','donare','赠送','donavi','donatus',ARE,{'don':'B'})
F(132,'vend','vendere','卖','vendidi','venditus','过去式是 vend 再加 id（vendidi，里面藏着 dare“给”的过去式 dedi）；过去分词是 vend 加 it',{'vend':'B'},ppzh='被卖掉的')
F(137,'fin','finire','划定界限','finivi','finitus',IRE,{'fine':'E'},pzh='划定了',ppzh='被划定的')
J((142,'par'),{'pare':'E','per':('W','in 和 parare 合成 imperare，a 弱化成 e'),'pair':('F','reparare 经古法语 reparer 进来，a 写成 ai')})
F(150,'junct','iungere','连接','iunxi','iunctus','过去式是 iung 加 s，g 和 s 合写成 x（写成 iunx）；过去分词是 iung 加 t，g 在 t 前面写成 c（写成 iunct）',{'junct':('P','拉丁语的 i 后来写成 j')})
F(164,'nat','nasci','出生',None,'natus',DEP+'；过去分词是 na 加 t',{'nat':'P','gn':('B','古拉丁语写作 gnasci，开头还有 g；这里只留下 gn'),'naiss':('F','经法语 naître、naissance 变来的样子')},
  cut='原形去掉词尾 -i 是 nasc，再去掉表示“开始、渐渐”的 sc 就是 na（nasci → na）',ppzh='生下来的')
F(172,'clud','claudere','关','clausi','clausus','过去式是 claud 加 s，d 并掉了（写成 claus）；过去分词是 claud 加 t，d 碰上 t 变成 s（写成 claus）',
  {'clude':('W','前面有前缀时 au 变成 u（-cludere），英语加不发音的 e')},ppzh='被关上的')
F(180,'nect','nectere','系、绑','nexui','nexus','过去式里 t 掉了，c 和 s 合写成 x，再加 u（写成 nexu）；过去分词也是 t 掉了，c 和 s 合写成 x（写成 nex）',{'nect':'B'},ppzh='被系上的')
F(189,'cult','colere','耕种、照料','colui','cultus','过去式是 col 加 u；过去分词是 col 加 t，o 变成了 u（写成 cult）',{'cult':'P'})
F(199,'cuss','discutere','打散','discussi','discussus','过去式是 cut 加 s，t 碰上 s 变成 ss（写成 cuss）；过去分词是 cut 加 t，t 碰上 t 也变成 ss（写成 cuss）',
  {'cuss':'P','cue':('F','复合词里写成 -cutere，经古法语变了形')},cut='cut 只接在前缀后面用（就是 quatere“摇”接在前缀后面的样子）：原形去掉前缀 dis 和词尾 -ere 就是 cut（discutere → cut）',gloss='摇、打',ppzh='被打散的')
F(203,'clar','clarare','使清楚','claravi','claratus',ARE,{'clare':'E'},ppzh='被弄清楚的')
F(204,'sed','sedere','坐','sedi','sessus','过去式只把元音 e 念长，写法不变；过去分词是 sed 加 t，d 碰上 t 变成 ss（写成 sess）',{'sess':'P'},ppzh='坐过的')
C(639,'sed',(204,'sed'),{'sid':('W','前面有前缀时 e 弱化成 i'),'side':('W','前面有前缀时 e 弱化成 i，英语加不发音的 e'),'resid':('W','就是 residere 去掉词尾：re 加 sid'),'sess':'P'})
F(214,'it','ire','走','ivi','itus','过去式是 i 加 v；过去分词是 i 加 t',{'it':'P'},cut='原形去掉词尾 -re 只剩 i（ire → i）',ppzh='走过的')
F(218,'solv','solvere','松开','solvi','solutus',SAME+'；过去分词里 v 变成元音 u，再加 t（写成 solut）',{'solve':'E'},ppzh='被松开的')
F(233,'sent','sentire','感觉','sensi','sensus','过去式是 sent 加 s，t 并掉了（写成 sens）；过去分词是 sent 加 t，t 碰上 t 变成 s（写成 sens）',
  {'sent':'B','senti':('G','带着原形里的 i，后面接别的成分')},pzh='感觉到了',ppzh='被感觉到的')
F(238,'scrib','scribere','写','scripsi','scriptus','过去式是 scrib 加 s，b 碰上 s 变成 p（写成 scrips）；过去分词是 scrib 加 t，b 碰上 t 也变成 p（写成 script）',{'scribe':'E','script':'P'},ppzh='被写下的')
C(412,'scrib',(238,'scrib'),{'script':'P'})
F(246,'plor','plorare','哭、大声喊','ploravi','ploratus',ARE,{'plore':'E'},pzh='喊了',ppzh='被喊出的')
F(247,'sequ','sequi','跟随',None,'secutus',DEP+'；过去分词里 qu 写成 c，后面加 ut（写成 secut）',
  {'sequ':'B','ecute':('PE','ex 和 secut 连在一起，s 并进了前面的 x，英语加不发音的 e'),'sue':('F','经古法语 suir 变来的样子')},cut='原形去掉词尾 -i 就是 sequ（sequi → sequ）',ppzh='跟随过的')
F(262,'tend','tendere','伸','tetendi','tentus',REDUP+'（te-tend-i）；过去分词是 ten 加 t，d 掉了（写成 tent），也写作 tensus（tens）',{'tent':'P'},ppzh='被伸出的')
F(264,'cit','citare','叫来、使动起来','citavi','citatus',ARE,{'cite':'E'},pzh='叫来了',ppzh='被叫来的')
F(296,'imit','imitari','模仿',None,'imitatus',DEP+'；过去分词是词根加 -atus',{'imit':'B'},cut='原形去掉词尾 -ari 就是 imit（imitari → imit）',ppzh='模仿过的')
F(297,'hab','habere','拿着、有','habui','habitus','过去式是 hab 加 u；过去分词是 hab 加 i 再加 t',{'hab':'B','hibit':('P','前面有前缀时 a 弱化成 i（prohibitus）')},ppzh='被拿着的')
F(297,'habit','habitare','居住','habitavi','habitatus',ARE,{'habit':'B'},ppzh='居住过的')
F(299,'lut','polluere','弄脏','pollui','pollutus',SAME+'；过去分词是 lu 加 t',{'lute':('PE','过去分词 lut 加不发音的 e')},
  cut='lu 只接在前缀后面用：原形去掉前缀 pol 和词尾 -ere 就是 lu（polluere → lu）',gloss='涂抹、弄脏',ppzh='被弄脏的')
F(307,'mit','mittere','送、放','misi','missus','过去式是 mit 加 s，t 并掉了（写成 mis）；过去分词是 mit 加 t，两个 t 碰在一起变成 ss（写成 miss）',
  {'mit':('B','英语只写一个 t'),'miss':'P','mise':('PE','过去分词 miss 只写一个 s，英语加不发音的 e'),'mess':('P','过去分词到了法语里 i 变成 e')},cut='原形去掉词尾 -ere 就是 mitt（mittere → mitt）',ppzh='被送出的')
F(313,'ten','tenere','握住、拿住','tenui','tentus','过去式是 ten 加 u；过去分词是 ten 加 t',
  {'tin':('W','前面有前缀时 e 弱化成 i'),'tinue':('W','前面有前缀时 e 弱化成 i，后面的 ue 是 continuus“连着的”留下的'),'tent':'P','tain':('F','经古法语进来，重读时 e 变成 ai')},ppzh='被握住的')
C(412,'ten',(313,'ten'),{'tain':('F','经古法语进来，重读时 e 变成 ai')})
C(318,'dic',(467,'dic'),{'dge':('F','iudicem 中间的 dic 到古法语里磨成了 dge')})
F(322,'par','parere','出现、显现','parui',None,'过去式是 par 加 u',{'par':'B','pear':('F','经古法语变了形，a 写成 ea')},pzh='出现了')
F(325,'sal','salire','跳','salui','saltus','过去式是 sal 加 u；过去分词是 sal 加 t',
  {'sili':('W','前面有前缀时 a 弱化成 i（resilire）'),'sult':('P','过去分词 salt 造出“一下下地跳”的 saltare，前面有前缀时 a 弱化成 u')},cut='原形去掉词尾 -ire 就是 sal（salire → sal）',ppzh='跳过的')
F(327,'rat','reri','计算、思考',None,'ratus',DEP+'；过去分词是 r 加 at',{'rat':'P'},cut='原形去掉词尾 -eri 只剩 r（reri → r）',ppzh='算过的')
F(330,'tract','trahere','拉','traxi','tractus','过去式是 trah 加 s，h 和 s 合写成 x（写成 trax）；过去分词是 trah 加 t，h 在 t 前面写成 c（写成 tract）',
  {'tract':'P','tray':('F','经古法语 traire 变来，ai 写成 ay'),'treat':('P','过去分词经古法语磨成了 tret、trait')},ppzh='被拉的')
F(333,'pict','pingere','画','pinxi','pictus','过去式是 ping 加 s，g 和 s 合写成 x（写成 pinx）；过去分词去掉 n，pig 加 t，g 在 t 前面写成 c（写成 pict）',
  {'pict':'P','pig':('B','原形去掉鼻音 n 的样子')},cut='原形去掉词尾 -ere 是 ping，这个 n 在过去分词里没有（pingere → ping）',ppzh='被画的')
J((365,'spir'),{'spire':'E','pire':('B','前面是 ex 时，x 本身就带 s 音，后面的 s 省掉了，英语加不发音的 e')})
F(367,'ced','cedere','走','cessi','cessus','过去式是 ced 加 s，d 和 s 合成 ss（写成 cess）；过去分词是 ced 加 t，d 碰上 t 也变成 ss（写成 cess）',{'cess':'P','ceed':('B','英语把 e 写成 ee')},ppzh='走过的')
C(276,'ced',(367,'ced'),{'cest':('P','过去分词 cess 经古法语，s 和 r 之间多出一个 t')})
F(378,'pon','ponere','放','posui','positus','过去式、过去分词里 n 换成了 s：过去式加 u（写成 posu），过去分词加 it（写成 posit）',
  {'pon':'B','posit':'P','pound':('F','componere 经古法语 compondre 进来，o 写成 ou，词尾的 d 是后来多出来的'),'post':('P','过去分词 posit 经法语磨掉了中间的 i 和词尾')},ppzh='被放下的')
for g in (406,1017): C(g,'vert',(282,'vert'),{'vers':'P'})
F(411,'pat','pati','忍受、承受',None,'passus',DEP+'；过去分词是 pat 加 t，t 碰上 t 变成 ss（写成 pass）',{'pat':'B','pass':'P','pati':('G','原形 pati 整个留着，后面接现在分词的词尾')},
  cut='原形去掉词尾 -i 就是 pat（pati → pat）',ppzh='忍受过的')
F(413,'pet','petere','奔向、去够','petivi','petitus','过去式是 pet 加 iv；过去分词是 pet 加 it',{'pet':'B','pete':'E','peat':('B','拉丁语的 e 在这里写成 ea'),'petit':'P'},pzh='奔向了',ppzh='被追求的')
F(415,'vid','dividere','分','divisi','divisus','过去式是 vid 加 s，d 并掉了（写成 vis）；过去分词是 vid 加 t，d 碰上 t 变成 s（写成 vis）',
  {'vide':'E','vise':('P','俗拉丁语用过去分词 divis 造出 *divisare，经法语变来'),'vice':('P','也是 *divisare 经法语变来的样子')},cut='vid 只接在前缀后面用：原形去掉前缀 di 和词尾 -ere 就是 vid（dividere → vid）',ppzh='被分开的')
F(419,'fund','fundere','倒、浇','fudi','fusus','过去式去掉 n，元音 u 念长（写成 fud）；过去分词去掉 n，fud 加 t，d 碰上 t 变成 s（写成 fus）',
  {'fund':'B','fuse':('PE','过去分词 fus 加不发音的 e')},cut='原形去掉词尾 -ere 是 fund，这个 n 只在原形里有（fundere → fund）',ppzh='被倒出的')
F(444,'man','manere','停留','mansi','mansus','过去式是 man 加 s；过去分词也是 man 加 s',{'man':'B','mans':'P','main':('F','经古法语进来，重读时 a 变成 ai')},ppzh='停留过的')
F(451,'prob','probare','检验、试','probavi','probatus',ARE,{'prob':'B'},pzh='检验了',ppzh='被检验的')
F(453,'pact','pangere','钉牢、固定','pepigi','pactus',REDUP+'（pe-pig-i），n 去掉了，a 也弱化成 i；过去分词去掉 n，pag 加 t，g 在 t 前面写成 c（写成 pact）',{'pact':'P'},
  cut='原形去掉词尾 -ere 是 pang，这个 n 只在原形里有（pangere → pang）',ppzh='被钉牢的')
J((456,'put'),{'pute':'E'})
F(480,'turb','turbare','搅乱','turbavi','turbatus',ARE,{'turb':'B'})
F(519,'pell','pellere','推、赶','pepuli','pulsus',REDUP+'（pe-pul-i），e 也变成了 u；过去分词里 e 变成 u，再加 s（写成 puls）',
  {'pell':'B','puls':'P','peal':('F','appellare 经古法语 apeler 进来，e 写成 ea')},ppzh='被推开的')
F(525,'opin','opinari','认为',None,'opinatus',DEP+'；过去分词是词根加 -atus',{'opin':'B'},cut='原形去掉词尾 -ari 就是 opin（opinari → opin）',ppzh='认为过的')
F(543,'merg','mergere','沉、浸','mersi','mersus','过去式是 merg 加 s，g 并掉了（写成 mers）；过去分词也是 g 并掉，加 s（写成 mers）',
  {'merse':('PE','过去分词 mers 加不发音的 e')},pzh='沉下去了',ppzh='被浸没的')
F(546,'aud','audire','听','audivi','auditus',IRE,{'audi':('G','带着原形里的 i'),'ey':('F','oboedire 经古法语 obeir 进来，d 掉了，只剩 ey')},ppzh='被听到的')
F(550,'rupt','rumpere','打破','rupi','ruptus','过去式去掉 m，元音 u 念长（写成 rup）；过去分词去掉 m，rup 加 t（写成 rupt）',{'rupt':'P'},
  cut='原形去掉词尾 -ere 是 rump，这个 m 只在原形里有（rumpere → rump）',ppzh='被打破的')
F(563,'serv','servare','看守、保住','servavi','servatus',ARE,{'serve':'E'},pzh='保住了',ppzh='被保住的')
F(568,'plang','plangere','击打、捶胸','planxi','planctus','过去式是 plang 加 s，g 和 s 合写成 x（写成 planx）；过去分词是 plang 加 t，g 在 t 前面写成 c（写成 planct）',
  {'plain':('F','经古法语 plaindre 变了形')},pzh='击打了',ppzh='被击打的')
F(589,'nunti','nuntiare','报告、传话','nuntiavi','nuntiatus',ARE,{'nounce':('F','经古法语进来，u 变成 ou，再加不发音的 e')},pzh='报告了',ppzh='被报告的')
F(592,'clin','clinare','弯、斜','clinavi','clinatus',ARE,{'cline':'E'},pzh='弯了',ppzh='被弄弯的')
F(605,'lax','laxare','放松','laxavi','laxatus',ARE,{'lax':'B'})
F(606,'sil','silere','不出声','silui',None,'过去式是 sil 加 u',{'sil':'B'},pzh='不出声了')
F(650,'fict','fingere','捏、塑','finxi','fictus','过去式是 fing 加 s，g 和 s 合写成 x（写成 finx）；过去分词去掉 n，fig 加 t，g 在 t 前面写成 c（写成 fict）',
  {'fict':'P','fig':('B','原形去掉鼻音 n 的样子')},cut='原形去掉词尾 -ere 是 fing，这个 n 在过去分词里没有（fingere → fing）',ppzh='被捏成的')
F(653,'al','alere','滋养、养大','alui','altus','过去式是 al 加 u；过去分词是 al 加 t，也有写成 alit 的',
  {'ult':('P','adolescere“长大”的过去分词 adultus 里的样子'),'olesc':('B','加上 -esc-“渐渐…”，a 在复合词里弱化成 o'),'alit':('P','coalescere 的过去分词 coalitus 里的样子')},gloss='长、养大',ppzh='被养大的')
F(659,'flect','flectere','弯','flexi','flexus','过去式、过去分词里 t 掉了，c 和 s 合写成 x（写成 flex）',{'flect':'B','flex':'P'},ppzh='被弄弯的')
F(675,'her','haerere','粘','haesi','haesus','过去式、过去分词里还是原来的 s（写成 haes）',{'her':('B','拉丁语的 ae 到英语里简化成 e'),'hes':('P','拉丁语的 ae 到英语里简化成 e')},
  cut='原形去掉词尾 -ere 是 haer，词根原来是 haes，s 夹在两个元音中间变成了 r（haerere → haer）',pzh='粘住了',ppzh='被粘住的')
F(689,'sult','consulere','商议','consului','consultus','过去式是 sul 加 u；过去分词是 sul 加 t',{'sult':'P'},cut='sul 只接在前缀后面用：原形去掉前缀 con 和词尾 -ere 就是 sul（consulere → sul）',ppzh='被商议的')
F(702,'test','testari','作证',None,'testatus',DEP+'；过去分词是词根加 -atus',{'test':'B'},cut='原形去掉词尾 -ari 就是 test（testari → test）',ppzh='作过证的')
F(760,'pol','polire','磨光','polivi','politus',IRE,{'pol':'B'})
F(761,'pun','punire','惩罚','punivi','punitus',IRE,{'pun':'B'})
F(762,'mand','mandare','交付、托付','mandavi','mandatus',ARE,{'mand':'B','mend':('W','前面有前缀时 a 弱化成 e（commendare）')})
F(766,'scend','scandere','攀、爬','scandi','scansus',SAME+'；过去分词是 scand 加 t，d 碰上 t 变成 s（写成 scans）',{'scend':('W','前面有前缀时 a 弱化成 e')},pzh='爬上去了',ppzh='被攀上的')
F(791,'ori','oriri','升起',None,'ortus',DEP+'；过去分词是 or 加 t',{'ori':('G','带着原形里的 i，后面接别的成分')},cut='原形去掉词尾 -iri 就是 or（oriri → or）',ppzh='升起了的')
F(820,'lig','ligare','捆、绑','ligavi','ligatus',ARE,{'lige':('F','走法语的写法，g 读 /dʒ/，再加不发音的 e'),'ly':('F','到古法语里 g 掉了'),'loy':('F','到古法语里 g 掉了，i 写成 oy')},pzh='捆上了',ppzh='被捆住的')
F(835,'fund','fundare','打底','fundavi','fundatus',ARE,{'found':('F','经古法语 fonder 进来，u 写成 ou')},pzh='打了底',ppzh='打好底的')
F(839,'cert','certare','较量、争','certavi','certatus',ARE,{'cert':'B'},ppzh='争过的')
F(847,'sculp','sculpere','雕、刻','sculpsi','sculptus','过去式是 sculp 加 s；过去分词是 sculp 加 t',{'sculp':'B'})
F(871,'funct','fungi','履行',None,'functus',DEP+'；过去分词是 fung 加 t，g 在 t 前面写成 c（写成 funct）',{'funct':'P'},cut='原形去掉词尾 -i 就是 fung（fungi → fung）',ppzh='履行过的')
F(891,'vinc','vincere','征服','vici','victus','过去式去掉 n，元音 i 念长（写成 vic）；过去分词去掉 n，vic 加 t（写成 vict）',{'vinc':'B','vince':'E','vict':'P'},
  cut='原形去掉词尾 -ere 是 vinc，这个 n 只在原形里有（vincere → vinc）')
F(892,'flict','fligere','打','flixi','flictus','过去式是 flig 加 s，g 和 s 合写成 x（写成 flix）；过去分词是 flig 加 t，g 在 t 前面写成 c（写成 flict）',{'flict':'P'})
F(903,'tribut','tribuere','分给','tribui','tributus',SAME+'；过去分词是 tribu 加 t',{'tribute':('PE','过去分词 tribut 加不发音的 e')})
F(915,'sect','secare','切','secui','sectus','过去式是 sec 加 u；过去分词是 sec 加 t',{'sect':'P'})
F(955,'cred','credere','相信','credidi','creditus','过去式是 cred 再加 id（credidi）；过去分词是 cred 加 it',{'cred':'B'})
F(956,'und','undare','起浪','undavi','undatus',ARE,{'und':'B','round':('F','superundare 经古法语进来，后来拼写被 round 带偏了')},ppzh='起过浪的')
F(957,'opt','optare','挑选、希望','optavi','optatus',ARE,{'opt':'B'})
F(967,'leg','legare','选派','legavi','legatus',ARE,{'leg':'B','leag':('F','collega 经法语进来，e 写成 ea')})
C(967,'fer',(25,'fer'),{'late':('PE','过去分词 lat 加不发音的 e')})
J((25,'fer'),{'lat':'P','late':('PE','过去分词 lat 加不发音的 e')})
F(1003,'trem','tremere','发抖','tremui',None,'过去式是 trem 加 u',{'trem':'B'})
F(1012,'estim','aestimare','估价','aestimavi','aestimatus',ARE,{'estim':('B','拉丁语的 ae 到英语里简化成 e')},cut='原形去掉词尾 -are 就是 aestim（aestimare → aestim）')
F(1019,'luc','lucere','发光','luxi',None,'过去式是 luc 加 s，c 和 s 合写成 x（写成 lux）',{'luc':'B'})
F(1019,'lustr','lustrare','照亮','lustravi','lustratus',ARE,{'lustr':'B'})
F(1034,'tang','tangere','碰','tetigi','tactus',REDUP+'（te-tig-i），n 去掉了，a 也弱化成 i；过去分词去掉 n，tag 加 t，g 在 t 前面写成 c（写成 tact）',
  {'tang':'B','tact':'P','tag':('B','原形去掉鼻音 n 的样子，是更早的词根'),'teger':('B','in 加 tag 成了 integer，a 弱化成 e'),'tire':('F','integer 里的 tegr 到法语里 g 掉了'),
   'tain':('W','attingere 里 a 弱化成 i，再经古法语 ataindre 变成 tain'),'tamin':('B','tag 加名词词尾 -men（contamen），g 在 m 前掉了')},
  cut='原形去掉词尾 -ere 是 tang，这个 n 只在原形里有（tangere → tang）',ppzh='被碰的')
F(1048,'veh','vehere','运、载','vexi','vectus','过去式是 veh 加 s，h 和 s 合写成 x（写成 vex）；过去分词是 veh 加 t，h 在 t 前面写成 c（写成 vect）',{'vehi':('L','后面接 -cle 时带上连接元音 i')},ppzh='被运走的')
F(1065,'cant','canere','唱','cecini','cantus',REDUP+'（ce-cin-i），a 也弱化成了 i；过去分词是 can 加 t',{'cent':('P','过去分词 cant 前面有前缀时 a 弱化成 e')},ppzh='被唱的')
F(1078,'am','amare','爱','amavi','amatus',ARE,{'amat':'P'})
F(1104,'sorb','sorbere','吸','sorbui','sorptus','过去式是 sorb 加 u；过去分词是 sorb 加 t，b 碰上 t 变成 p（写成 sorpt）',{'sorb':'B'},ppzh='被吸进的')
F(1123,'haust','haurire','汲水、喝干','hausi','haustus','过去式是 haur 去掉 r 再加 s（写成 haus）；过去分词是 haus 加 t（写成 haust）',{'haust':'P'},
  cut='原形去掉词尾 -ire 就是 haur（haurire → haur）',pzh='汲了水',ppzh='被汲干的')
F(1180,'ambul','ambulare','走动','ambulavi','ambulatus',ARE,{'ambul':'B'},ppzh='走动过的')
F(1196,'err','errare','走岔、犯错','erravi','erratus',ARE,{'err':'B'},pzh='走岔了',ppzh='走岔过的')
F(1204,'vest','vestire','给…穿衣','vestivi','vestitus',IRE,{'vest':'B'},pzh='给…穿上了衣服',ppzh='穿好衣服的')
F(1258,'ton','tonare','打雷','tonui','tonitus','过去式是 ton 加 u；过去分词是 ton 加 i 再加 t',{'ton':'B'},ppzh='被雷声震住的')
F(1303,'rad','radere','刮','rasi','rasus','过去式是 rad 加 s，d 并掉了（写成 ras）；过去分词是 rad 加 t，d 碰上 t 变成 s（写成 ras）',{'rase':('PE','过去分词 ras 加不发音的 e')},ppzh='被刮掉的')
F(1341,'vibr','vibrare','颤动','vibravi','vibratus',ARE,{'vibr':'B'},ppzh='被摇动的')
F(1353,'neg','negare','说不、否认','negavi','negatus',ARE,{'negat':'P','ny':('F','denegare 到了古法语，两个元音之间的 g 掉了')},pzh='否认了',ppzh='被否认的')
F(1361,'tu','tueri','照看',None,'tuitus',DEP+'；过去分词是 tu 加 it（写成 tuit），也有只加 t 的短写法（写成 tut）',{'tuit':'P','tut':('P','过去分词的短写法 tutus')},
  cut='原形去掉词尾 -eri 就是 tu（tueri → tu）',ppzh='照看过的')
F(1362,'vulner','vulnerare','使受伤','vulneravi','vulneratus',ARE,{'vulner':'B'},pzh='伤了',ppzh='受了伤的')
F(1381,'carp','carpere','摘','carpsi','carptus','过去式是 carp 加 s；过去分词是 carp 加 t',{'cerpt':('P','过去分词 carpt 前面有前缀时 a 弱化成 e')},ppzh='被摘下的')
F(1423,'fod','fodere','挖','fodi','fossus','过去式只把元音 o 念长，写法不变；过去分词是 fod 加 t，d 碰上 t 变成 ss（写成 foss）',{'foss':'P'})
F(1444,'laps','labi','滑、跌倒',None,'lapsus',DEP+'；过去分词是 lab 加 s，b 碰上 s 变成 p（写成 laps）',{'lapse':('PE','过去分词 laps 加不发音的 e')},
  cut='原形去掉词尾 -i 就是 lab（labi → lab）',ppzh='跌倒了的')
F(1479,'horr','horrere','毛发竖起、发抖','horrui',None,'过去式是 horr 加 u',{'horr':'B'},pzh='发抖了')
F(1527,'pot','potare','喝','potavi','potatus',ARE,{'pot':'B'})
F(1528,'suad','suadere','劝','suasi','suasus','过去式是 suad 加 s，d 并掉了（写成 suas）；过去分词是 suad 加 t，d 碰上 t 变成 s（写成 suas）',{'suade':'E'})
F(1586,'rig','rigare','浇湿','rigavi','rigatus',ARE,{'rig':'B'})
F(1620,'migr','migrare','迁移','migravi','migratus',ARE,{'migr':'B'},ppzh='迁移过的')
F(1629,'luct','luctari','摔跤、挣扎',None,'luctatus',DEP+'；过去分词是词根加 -atus',{'luct':'B'},cut='原形去掉词尾 -ari 就是 luct（luctari → luct）',ppzh='挣扎过的')
F(1642,'sanct','sancire','奉为神圣','sanxi','sanctus','过去式是 sanc 加 s，c 和 s 合写成 x（写成 sanx）；过去分词是 sanc 加 t（写成 sanct）',{'sanctu':('P','过去分词 sanct 带上连接用的 u')},
  cut='原形去掉词尾 -ire 就是 sanc（sancire → sanc）',pzh='奉为神圣了',ppzh='被奉为神圣的')
F(1644,'dorm','dormire','睡','dormivi','dormitus',IRE,{'dormit':'P'},ppzh='睡过的')
F(1664,'serp','serpere','爬','serpsi','serptus','过去式是 serp 加 s；过去分词是 serp 加 t',{'serp':'B'},ppzh='爬过的')
F(1721,'stup','stupere','发呆','stupui',None,'过去式是 stup 加 u',{'stup':'B'})
F(1729,'tort','torquere','拧、扭','torsi','tortus','过去式里 qu 碰上 s 并掉了（写成 tors）；过去分词里 qu 碰上 t 也并掉了（写成 tort）',{'tort':'P'},cut='原形去掉词尾 -ere 就是 torqu（torquere → torqu）',ppzh='被拧过的')
F(1738,'vad','invadere','闯进去','invasi','invasus','过去式是 vad 加 s，d 并掉了（写成 vas）；过去分词是 vad 加 t，d 碰上 t 变成 s（写成 vas）',{'vade':'E','vas':'P'},
  cut='vad 只接在前缀后面用（vadere“走”单用时没有过去式、过去分词）：原形去掉前缀 in 和词尾 -ere 就是 vad（invadere → vad）',gloss='走',ppzh='被闯进的')
F(1743,'fragr','fragrare','散发气味','fragravi','fragratus',ARE,{'fragr':'B'},pzh='散发了气味',ppzh='散发过气味的')
F(1756,'cav','cavere','提防','cavi','cautus','过去式只把元音 a 念长，写法不变；过去分词里 v 变成元音 u，再加 t（写成 caut）',{'caut':'P'},ppzh='提防着的')
F(1762,'mol','moliri','费力地建造',None,'molitus',DEP+'；过去分词是 mol 加 it',{'mol':'B'},cut='原形去掉词尾 -iri 就是 mol（moliri → mol）',ppzh='建造过的')
F(1779,'rod','rodere','啃','rosi','rosus','过去式是 rod 加 s，d 并掉了（写成 ros）；过去分词是 rod 加 t，d 碰上 t 变成 s（写成 ros）',{'rod':'B','rode':'E'})
F(1785,'pat','patere','敞开着','patui',None,'过去式是 pat 加 u',{'pat':'B'},pzh='敞开了')
F(1813,'cal','calare','召唤','calavi','calatus',ARE,{'cil':('W','在复合词里 a 弱化成 i')})
F(1832,'fiss','findere','劈开','fidi','fissus','过去式去掉 n（写成 fid）；过去分词去掉 n，fid 加 t，d 碰上 t 变成 ss（写成 fiss）',{'fiss':'P'},cut='原形去掉词尾 -ere 是 find，这个 n 只在原形里有（findere → find）')
F(1850,'trud','trudere','推、挤','trusi','trusus','过去式是 trud 加 s，d 并掉了（写成 trus）；过去分词是 trud 加 t，d 碰上 t 变成 s（写成 trus）',{'trude':'E'})
F(1933,'par','parere','生、生育','peperi','partus',REDUP+'（pe-per-i），a 弱化成 e；过去分词是 par 加 t',{'par':'B'},ppzh='被生下的')
F(1938,'lid','laedere','撞、伤','laesi','laesus','过去式是 laed 加 s，d 并掉了（写成 laes）；过去分词是 laed 加 t，d 碰上 t 变成 s（写成 laes）',{'lide':('W','前面有前缀时 ae 弱化成 i（collidere），英语加不发音的 e')},ppzh='被撞伤的')
F(1949,'fla','flare','吹','flavi','flatus','过去式是 fla 加 v；过去分词是 fla 加 t',{'flate':('PE','过去分词 flat 加不发音的 e')},cut='原形去掉词尾 -re 就是 fla（flare → fla）',ppzh='被吹起的')
F(2038,'terg','tergere','擦','tersi','tersus','过去式是 terg 加 s，g 并掉了（写成 ters）；过去分词也是 g 并掉，加 s（写成 ters）',{'terg':'B'})
F(2065,'tim','timere','害怕','timui',None,'过去式是 tim 加 u',{'tim':'B'})
F(2111,'rept','repere','爬','repsi','reptus','过去式是 rep 加 s；过去分词是 rep 加 t',{'rept':'P'},ppzh='爬过的')
F(2140,'torr','torrere','烤','torrui','tostus','过去式是 torr 加 u；过去分词里 rr 换成 s，再加 t（写成 tost）',{'torr':'B'},ppzh='被烤过的')
F(2221,'apert','aperire','打开','aperui','apertus','过去式是 aper 加 u；过去分词是 aper 加 t',{'apert':'P'},cut='原形去掉词尾 -ire 就是 aper（aperire → aper）')
F(2222,'ar','arere','干','arui',None,'过去式是 ar 加 u',{'ar':'B'},pzh='干了')
F(2225,'rog','rogare','问、求','rogavi','rogatus',ARE,{'rog':'B'},ppzh='被问的')
F(2278,'sol','solari','安慰',None,'solatus',DEP+'；过去分词是词根加 -atus',{'sole':'E'},cut='原形去掉词尾 -ari 就是 sol（solari → sol）',ppzh='安慰过的')
F(2300,'ed','edere','吃','edi','esus','过去式只把元音 e 念长，写法不变；过去分词是 ed 加 t，d 碰上 t 变成 s（写成 es）',{'ed':'B','ese':('PE','过去分词 es 加不发音的 e')},ppzh='被吃的')
F(2321,'frict','fricare','擦','fricui','frictus','过去式是 fric 加 u；过去分词是 fric 加 t',{'frict':'P'})
F(2363,'lud','ludere','玩','lusi','lusus','过去式是 lud 加 s，d 并掉了（写成 lus）；过去分词是 lud 加 t，d 碰上 t 变成 s（写成 lus）',{'lus':'P'},ppzh='被玩弄的')
F(2365,'cend','incendere','点燃','incendi','incensus',SAME+'；过去分词是 cend 加 t，d 碰上 t 变成 s（写成 cens）',{'cense':('PE','过去分词 cens 加不发音的 e')},
  cut='cend 只接在前缀后面用（就是 candere“发白光”进了复合词的样子）：原形去掉前缀 in 和词尾 -ere 就是 cend（incendere → cend）',ppzh='被点燃的')
F(2367,'vit','vitare','躲开','vitavi','vitatus',ARE,{'vit':'B'})
F(2394,'lav','lavare','洗','lavi','lautus','过去式只把元音 a 念长，写法不变；过去分词里 v 变成元音 u，再加 t（写成 laut）',{'lav':'B'},ppzh='洗过的')
F(2461,'fug','fugere','逃','fugi','fugitus','过去式只把元音 u 念长，写法不变；过去分词是 fug 加 it',{'fug':'B'},ppzh='逃过的')
F(2464,'ver','vereri','敬畏',None,'veritus',DEP+'；过去分词是 ver 加 it',{'vere':'E'},cut='原形去掉词尾 -eri 就是 ver（vereri → ver）',ppzh='敬畏过的')
F(2467,'rid','ridere','笑','risi','risus','过去式是 rid 加 s，d 并掉了（写成 ris）；过去分词是 rid 加 t，d 碰上 t 变成 s（写成 ris）',{'rid':'B'},ppzh='被笑的')
F(2469,'rig','rigere','僵、硬','rigui',None,'过去式是 rig 加 u',{'rig':'B'},pzh='僵了')
F(2519,'splend','splendere','发光','splendui',None,'过去式是 splend 加 u',{'splend':'B'})
F(2557,'toler','tolerare','忍耐','toleravi','toleratus',ARE,{'toler':'B'})
F(2619,'tum','tumere','肿','tumui',None,'过去式是 tum 加 u',{'tum':'B'})
F(182,'sci','scire','知道','scivi','scitus','过去式是 sci 加 v；过去分词是 sci 加 t',{'sci':'B'},cut='原形去掉词尾 -re 就是 sci（scire → sci）',ppzh='被知道的')
F(989,'liqu','liquere','是流动的','licui',None,'过去式里 qu 写成 c，再加 u（写成 licu）',{'liqu':'B'},pzh='流动了')
F(232,'val','valere','强壮、有力','valui',None,'过去式是 val 加 u',{'val':'B','vail':('F','古法语 valoir 的一个变化形式写成 vaill，英语写成 vail')},pzh='有力了')
