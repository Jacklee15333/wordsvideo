"""每个词用哪一条合成规律（auto.py 判不准的，这里逐个定）。代码见 catalog.py。"""

def _many(code, words):
    return {w: code for w in words.split()}

CAT = {}
# 外语里就合成好的
CAT.update(_many('H27', '''republic surgery platform helicopter carnival alarm agriculture encyclopedia kindergarten madam maneuver manuscript
privilege tragedy comedy alchemy algebra dinosaur malaria octopus atmosphere legislator leopard pharaoh slogan terracotta vinegar rosemary
vintage tsunami karate emoji ketchup alligator chameleon ostrich caterpillar cobalt protocol denim picnic squirrel pajamas standard allergy
medieval artifact longevity manufacture centipede pedestal melody bankrupt deluxe maintain legislate gallop alphabet petroleum Vietnam ad-lib'''))
# 拼缀词
CAT.update(_many('H28', 'smog metaverse happenstance vlog podcast escalator pixel Paralympic oxide radiocarbon polyester epipen infographic vitamin trashcapes'))
# 老合成词
CAT.update(_many('H26', '''world gospel neighbour neighbor which such each every none alone lady husband woman window orchard barn harness harbour harbor
fellow nightingale island elbow garlic shepherd Halloween Christmas bonfire Wednesday Tuesday Thursday Friday Monday Saturday thousand hundred
yes unless England Norway mermaid sandwich together'''))
# 像一句命令（动词在前）
CAT.update(_many('H11', 'scarecrow breakfast pastime ceasefire makeshift farewell Shakespeare passport portfolio wardrobe kowtow'))
# 小词合成小词
CAT.update(_many('H25', 'whereas therefore furthermore moreover without within upon onto throughout another nearby overall'))
# 介词短语连成一个词
CAT.update(_many('H10', '''upstairs downstairs downtown online offline off-stage off-course off-key off-ice after-school instead indeed tonight tomorrow
behalf alongside forever perhaps nowadays percent'''))
# 并列
CAT.update(_many('H14', '''southeast southwest northwest northeast compound-complex teacher-director giant-king giant-prince stem-art human-tech
problem-solution science-music urban-rural parent-teacher white-yellow golden-brown singer-actor-dancer give-and-take cause-and-effect
right-and-wrong hide-and-seek black-and-white time-and-money blue-and-white ping-pong lullaby quack-quack-quack'''))
# 近义叠用、加类名
CAT.update(_many('H15', 'courtyard pathway until underneath reindeer chestnut peafowl charcoal alleyway'))
# 有这个特点的人或东西
CAT.update(_many('H16', 'humpback Bluetooth high-five high-rise barefoot freelance'))
# 主语 + 动词
CAT.update(_many('H18', '''sunrise sunset sunshine sundown earthquake heartbeat rainfall snowfall waterfall snowmelt airflow landslide frostbite
headache stomachache toothache sunstroke'''))
# 名词、形容词 + 动词 = 动词
CAT.update(_many('H17', '''hand-wash air-draw deep-fry stir-fry double-check cross-check double-click safe-keep dive-bombed headbutt whitewash
homebake slam-dunk video-called fulfil livestreamed'''))
# 宾语提前
CAT.update(_many('H02', '''dishwasher blockbuster carpooling tear-jerking anteater rock-eater tongue-twister newscaster nutcracker fundraiser hairdresser
skyscraper screwdriver air-conditioned lifeguard cowherd windbreak shot-put role-play haircut chimney-sweep climate-control time-management
proofread troubleshoot kidnap career-exploration power-supply eldercare childcare healthcare gameplay'''))
# 用什么、在哪儿、由谁提前
CAT.update(_many('H03', '''sword-fighting skydiving scuba-diving handwriting typewriter typewrite city-driving water-living windsurfing windsurf
crowdfunding concertgoer theatergoer grasshopper spacewalk time-travel wordplay'''))
# 名词 + 过去分词
CAT.update(_many('H04', 'typewritten 3D-printed heartbroken heart-broken heartfelt'))
# 副词提前
CAT.update(_many('H05', 'remotely-operated widespread broadcast easy-going ready-made hard-earned best-preserved well-shaped well-tempered'))
# 名词 + 形容词
CAT.update(_many('H06', '''waterproof fire-resistant lightning-fast fire-proof rainproof rust-proof movie-like human-like countryside-like real-life-like
brush-like bowl-like umbrella-like eagle-like harp-like cat-like diamond-like dog-like flame-red rose-red peacock-blue chestnut-brown
water-related dehydration-related job-related career-related math-related Christmas-related nutrition-balanced brand-new waist-deep'''))
# 短语整个当一个词
CAT.update(_many('H07', '''never-ending never-smiling never-seen-before much-anticipated newfound fresh-cut highly-skilled environmentally-friendly
decade-old century-old year-round half-full faraway far-off hands-on thumbs-up head-on lightweight open-weight teenage first-ever second-hand
secondhand second-longest single-file up-to-date upside-down one-size-fits-all not-for-profit out-of-tune kick-the-can bean-to-bar
rivals-turned-ally maybe goodnight barefoot-style countryside-style wholesale freshwater saltwater worthwhile must-visit must-have
lithium-ion zero-gravity'''))
# 小词在前
CAT.update(_many('H09', 'upcoming download upload outlook outfit'))
# 主体在后（auto 判成别的）
CAT.update(_many('H01', '''cyberbullying well-being plaything shoestring watershed dataset mindset shortcut paper-cut riverbed woodshed seaweed
horseback upbeat backflip firecracker loudspeaker breakdancer houseworker newcomer honeyguide sunflower wildflower top-tier quarter-hour
quarterfinal half-life halfway first-aid half-flush full-flush homesickness video-call evergreen yesterday spinning-wheel handicraft
x-ray student-teacher'''))
# 数词 + 名词当定语
CAT.update(_many('H13', '100-foot-tall five-hundred-metre three-dimensional'))
# 十几
CAT.update(_many('H21', 'fourteen seventeen'))
# 词尾加在整个短语上
CAT.update(_many('H33', '6th-grader 6th-graders 7th-grader 7th-graders sixth-grader seventh-grader eighth-grader ninth-grader four-poster year-old'))
# 动词短语变名词（auto 判成别的或三段的）
CAT.update(_many('H08', 'self-check-out'))
CAT['self-check-out'] = 'H34'
CAT['wouldn\'t'] = 'X15'

# ---------------------------------------------------------------- 第二行合成规律（特殊规则），可以有几条
EXTRA = {}
def _extra(code, words):
    for w in words.split():
        EXTRA.setdefault(w, []).append(code)
_extra('H29', '''sportsman sportsmen nobleman middleman middlemen gentleman gentlemen repairman weatherman freshman freshmen fireman postwoman
fisherman cameraman salesgirl saleswoman salesperson businessman businessmen businessperson businesswoman footman footmen mailman Frenchman
Englishman craftsman craftsmen craftsperson craftspeople craftswoman snowmen policewoman policewomen policemen postman postmen boatman
boatmen spokesman''')
_extra('H30', 'craftsman craftsmen craftsperson craftspeople craftswoman salesgirl saleswoman salesperson spokesman')
_extra('H31', 'passer-by passers-by grown-ups check-ups trade-offs 6th-graders 7th-graders')
_extra('H32', 'greenhouse hot-dog deadline highlight blueprint hotline software hardware blacklist')
CAT.update({'spokesman': 'H01', 'top-tier': 'H07', 'first-aid': 'H07', 'high-speed': 'H07', 'brainstorm': 'H01', 'skyrocket': 'H01'})
CAT.update({'check-ups': 'H08', 'grown-ups': 'H08', 'trade-offs': 'H08', 'first-aid': 'H01'})

CAT.update({'giant-king': 'H01', 'giant-prince': 'H01'})
