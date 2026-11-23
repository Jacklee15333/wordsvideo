# 生活场景素材（6.20 起；6.21 重画成详细、具体的；6.22 起是图画书画风、中外结合）

用户：“要接近真实的样子，不要太抽象，不要只画一个人头，一个摆件这样的；要尽量体现出现实生活中的样子”“周围环境还需要再加强一下……车站画的不是很详细，很具体”。
每幅画铺一张场景背景，再放人和东西（`pictures.md` 第十五节）。用的时候拷到这个词的 `art/` 里。

## 场景背景（整幅画铺满：`"bg": "blank", "img": "art/room-bg.svg"`；1200 × 700，窄画框会裁掉左右两边）

| 文件 | 画的是 | 用在 |
|---|---|---|
| station-bg.svg | 火车站广场：站房和玻璃幕墙、楼顶“火车站”大字、钟楼、“售票处”“进站口 ENTRANCE”电子屏、“出站口”、玻璃门和雨棚、拖拉杆箱和背包的旅客、花坛、路灯、长椅、树、公交车、出租车、远处的楼（594 个图形） | 公共场所、交通、广播 |
| room-bg.svg | 屋里（书房 / 客厅）：窗外的楼和树、窗帘、窗台盆栽、挂钟、画和照片、搁板、整面书架（书、地球仪、奖杯）、地毯、落地绿植、开关、木地板（313 个） | 家里的东西（音箱、电脑、台灯、闹钟、恒温器…） |
| classroom-bg.svg | 教室：板书、粉笔和板擦、“好好学习 天天向上”、钟、广播喇叭、日光灯、窗户和蓝窗帘、“学习园地”、图书角、讲台和讲桌（306 个）；配 `class-desks.svg`（第一排课桌，放在人前面，挡住腰） | 老师、学生、上课、说话 |
| stage-bg.svg | 礼堂舞台：深蓝后幕、灯架和射灯的光柱、吊着的音箱、两边大幕和金色绑带、横幕和流苏、木地板、台口的花、台阶（392 个）；配 `banner-speech.svg`（横幅“校园演讲比赛”，`scripts/scenes.py` 的 `banner(字, 文件名)` 换字） | 演讲、表演、开会 |

这里的都已经转成图画书画风（黑色勾线、饱和平涂）。屋里加了中式的山水画、青花瓷瓶、中国结，舞台横幅中英双语，听众和旅客中外都有（6.22）。
要重画：`python3 scripts/scenes.py raw/` 生成写实原图，再 `python3 scripts/bookstyle.py stylize raw/x.svg x.svg --bg`（单件东西不加 --bg）。画新地方照 `pictures.md` 第十五节的清单，一张不少于 150 个图形（起草时自动数）。
很扁的画框（辨析卡片）不要用 `img` 铺满，把背景当一样东西放、挑露出哪一条（example-speaker 的 `band`）。

## 东西（底色透明，s 是占画高多少）

desk.svg（书桌，正面；桌面在 viewBox y≈26，东西的底边放在这儿）· podium.svg（讲台）· mic.svg（鹅颈麦克风，底座右下、话筒头左上）· computer.svg（电脑：屏幕上是图表）· computer-music.svg（电脑：屏幕上在放音乐）· speaker.svg（木壳音箱）· loudspeaker.svg（电线杆上的两个大喇叭）· pa-speaker.svg（三脚架上的舞台音箱）· lamp.svg（台灯）· plant.svg（绿植）· books.svg（一摞书）· mug.svg（杯子）· audience-wide.svg（台下一排听众的后脑勺，放最前面）· class-desks.svg（第一排课桌）· banner-speech.svg（横幅）· screen-water.svg（投影幕：水龙头）· drop.svg（水滴）· desk-papers.svg（桌子上一叠写满算式的纸、铅笔）· note.svg / note2.svg（音符）· waves.svg（声波，往右；往左写 flip）· icon-speak.svg（说话的气泡，小图标）

人物在 `../characters/`（`scripts/people.py` 生成）。新画的场景、东西都放进来，以后的词接着用。


6.27–6.28（7A-U4）新加的，都已经是图画书画风：背景 park-bg（公园：亭子、石拱桥、柳树、钟楼）、vault-room（拱顶大厅）、obscura-room（暗室，左边屋外、墙上小孔）、castle-bg（夜里的城墙）、bedroom-bg（卧室）、street-bg（街道：书店、CAFÉ、面馆、BAKERY、红绿灯、斑马线）；东西 camera、flash、photo、tripod-cam（REC 亮 / 灭两帧）、boxcam、rotary-phone、smartphone、thermostat（24° / 26° / 18°）、aircon、heater、thermometer（_f0–_f3 往上升）、sofa、fishtank、fish、cat-lick_f0–3、cat-sit_f0–2、cushion、yarn、mirror、star、bed、nightstand、clock_f0–1（闹钟抖）、bell_f0–1（火警铃摇）、rack（武器架）、spider、drum、map。画法脚本在 ../kit-7A-U4/。
