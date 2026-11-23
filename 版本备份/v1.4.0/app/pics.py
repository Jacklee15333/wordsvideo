# -*- coding: utf-8 -*-
"""单词工作台 · 做视频画面（画面设置）
一个词出视频前要有“画面设置”：每个意思一幅会动的生活场景、例句的动画、意思怎么变过来的示意图……
以前是 Claude 一个词一个词手写的，这里交给网页 AI：
  按视频技能的 references/data-format.md、pictures.md 写一份 prefs（JSON），要用到的插图写成 SVG；
  程序检查（JSON 能读、用到的图都有、人物动作是现成的、不用表情图、SVG 能打开），
  这台电脑的出片环境装好了的话，再用视频技能“起草检查”（要“还要补：都齐了”）；没过就带着问题退回去改。
过了就存进：
  词库/画面设置/words/<词>.json + <词>.py（出片流水线读它）、art/<词>/*.svg、<词>ai_art.py（把插图拷进画图文件夹）、清单.tsv；
  词库/总表视频细节数据/词/<首字母>/<词>.json 的「画面」「插图」，索引.tsv 的「画面」列改成“细节数据有”。"""
import json, re, time, xml.etree.ElementTree as ET
from pathlib import Path
import core as C
import video as V

VR = "引擎/视频/references"
EXTRA = "词库/画面设置"
END = C.END


def _p(rel):
    return C.REPO / rel


def motions():
    t = _p("引擎/视频/scripts/poses.py").read_text(encoding="utf-8")
    seg = t[t.index("MOTIONS = {"):][:20000]
    # 只要会动的（cn-girl 这种没有动作的名字在出片时画不出来）
    return [n for n in re.findall(r"^\s+'([a-z][a-z0-9-]+)'\s*:", seg, re.M) if n.count("-") >= 2]


def scenes():
    return sorted(p.name for p in _p(VR + "/scenes").glob("*.svg"))


def _sections(md, keep):
    parts = re.split(r"(?m)^(?=## )", md)
    return "\n".join(p for p in parts if any(p.startswith("## " + k) for k in keep))


def docs():
    df = _p(VR + "/data-format.md").read_text(encoding="utf-8")[:26000]
    pm = _p(VR + "/pictures.md").read_text(encoding="utf-8")
    pm = _sections(pm, ["一、", "三、", "四、", "五、", "六、", "七、", "九、", "十二、", "十五、", "十八、", "十九、", "二十、"])[:20000]
    ex = json.loads(_p(VR + "/example-camera/prefs.json").read_text(encoding="utf-8"))
    ex = json.dumps(ex, ensure_ascii=False, separators=(",", ":"))[:9000]
    return df, pm, ex


OUT = """【输出格式（程序按这个格式自动读，请严格照做）】
1. 一个代码块（第一行写 ```json），里面是这个词的画面设置：一个 JSON 对象，写法和上面的范例一样（style、board、pics、originPic、flow、extend…… 用得到的都写）。
2. 画里的人不要自己画，写成 {"actor": "动作名", "x": 0.3, "y": 0.6, "s": 0.9, "z": 3}，程序会换成会动的人。动作名只能用这些：%s。
3. 不许用表情图（"e": "🚗" 这种），东西都用写实插图："svg": "art/名字.svg"。下面这些现成的场景和东西可以直接用：%s。
4. 现成里没有的插图，你自己画成 SVG，每张一块，放在 JSON 代码块后面：
<<<SVG 名字.svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">……</svg>
>>>END
   插图要求：图画书风（黑色勾线、饱和平涂），画成现实生活里的样子；一张图不超过 12 KB。
5. 最后单独一行写：%s"""


def build_prompt(word, fix=None):
    df, pm, ex = docs()
    rows = C.TABLE["words"].get(word) or [{}]
    mat = C.material(word) + ("\n  拆分：" + rows[0].get("拆分", "") if rows[0].get("拆分") else "") + \
        ("\n  意思怎么变过来（总表）：" + rows[0].get("组合 → 现在的含义", "")[:600].replace("\n", " / ") if rows[0].get("组合 → 现在的含义") else "")
    parts = ["【做画面】你在帮一位中学英语老师给单词 %s 做构词动画视频的“画面设置”。视频的讲解稿由程序从总表生成，你只管画面：每个意思一幅生活场景、例句和例句动画、意思怎么一步步变过来的示意图。" % word,
             "【这个词的总表材料】\n" + mat,
             "【画面设置的格式（视频技能 data-format.md）】\n" + df,
             "【画面怎么画（视频技能 pictures.md 摘要）】\n" + pm,
             "【范例：camera 的画面设置（JSON）】\n" + ex,
             OUT % ("、".join(motions()), "、".join("art/" + s for s in scenes()), END)]
    if fix:
        parts.insert(1, "【你上次写的没通过检查，请改好后把 JSON 和全部插图重新完整写一遍】\n问题：\n- " + "\n- ".join(fix[1]) +
                     "\n上次的 JSON：\n" + fix[0][:12000])
    return "\n\n".join(parts)


SVG_RE = re.compile(r"<<<SVG\s+([\w.\-]+\.svg)\s*\n(.*?)>>>END", re.S)


def parse(reply):
    t = (reply or "").replace("\r", "")
    svgs = {n: b.strip() for n, b in SVG_RE.findall(t)}
    body = SVG_RE.sub("", t)
    m = re.search(r"```(?:json)?\s*\n(\{.*?\})\s*```", body, re.S)
    raw = m.group(1) if m else ""
    if not raw:
        a, b = body.find("{"), body.rfind("}")
        raw = body[a:b + 1] if a >= 0 and b > a else ""
    try:
        P = json.loads(raw) if raw else None
    except Exception as e:
        return None, raw, svgs, ["JSON 读不出来：%s" % str(e)[:120]]
    if isinstance(P, dict) and len(P) == 1 and isinstance(next(iter(P.values())), dict) and "pics" in next(iter(P.values())):
        P = next(iter(P.values()))                     # 写成了 {"单词": {...}}
    return P, raw, svgs, []


def check(word, P, svgs):
    errs = []
    if not isinstance(P, dict):
        return ["没有画面设置的 JSON"]
    pics = P.get("pics")
    if not isinstance(pics, list) or not pics:
        errs.append("pics（每个意思一幅画）没有写")
    else:
        for i, pc in enumerate(pics):
            if not isinstance(pc, dict) or not pc.get("text"):
                errs.append("pics 第 %d 幅缺 text（这幅画讲的意思）" % (i + 1))
            elif not (pc.get("items") or pc.get("img")):
                errs.append("pics 第 %d 幅（%s）没有画东西（items）" % (i + 1, pc.get("text")))
    if not isinstance(P.get("flow"), list) or not P.get("flow"):
        errs.append("flow（意思怎么一步步变过来）没有写")
    s = json.dumps(P, ensure_ascii=False)
    if re.search(r'"e"\s*:', s):
        errs.append("用了表情图（\"e\": …），要换成写实插图 svg")
    have = set(scenes()) | set(svgs)
    miss = sorted({n for n in re.findall(r"art/([\w.\-]+\.svg)", s)} - have)
    if miss:
        errs.append("用到的插图没有：%s（现成的里没有，要画成 SVG 块）" % "、".join(miss[:10]))
    mot = set(motions())
    bad = sorted({a for a in re.findall(r'"actor"\s*:\s*"([^"]+)"', s)} - mot)
    if bad:
        errs.append("人物动作名不对：%s（只能用给出的那些）" % "、".join(bad))
    for n, b in svgs.items():
        if len(b) > 40000:
            errs.append("%s 太大了（%d 字），要简单一些" % (n, len(b)))
            continue
        try:
            root = ET.fromstring(b)
            if not root.tag.endswith("svg"):
                errs.append("%s 不是 SVG" % n)
        except Exception as e:
            errs.append("%s 打不开（SVG 写错了：%s）" % (n, str(e)[:80]))
    return errs


WORD_PY = '''# AI 生成的画面设置（单词工作台）：读同名的 .json，把 {"actor": 动作名} 换成会动的人，交给视频技能
import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/%(folder)s/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE, '%(folder)s.json'), encoding='utf-8'))
def conv(o):
    if isinstance(o, dict):
        if 'actor' in o:
            kw = {k: v for k, v in o.items() if k != 'actor'}
            return actor(o['actor'], **kw)
        return {k: conv(v) for k, v in o.items()}
    if isinstance(o, list):
        return [conv(v) for v in o]
    return o
json.dump({%(word)r: conv(P)}, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok')
'''
ART_PY = '''# AI 画的插图（单词工作台）：把 art/%(folder)s/ 里的 svg 拷进画图文件夹
import os, sys, glob, shutil
src = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'art', '%(folder)s')
for f in glob.glob(os.path.join(src, '*.svg')):
    shutil.copy(f, sys.argv[1])
print('ok')
'''


def save(word, P, svgs, checked):
    f = V.folder_of(word)
    base = C.REPO / EXTRA
    with C.REPO_LOCK:
        (base / "words").mkdir(parents=True, exist_ok=True)
        art = base / "art" / f
        if art.exists():
            C.rmtree(art)
        art.mkdir(parents=True)
        for n, b in svgs.items():
            (art / n).write_text(b + "\n", encoding="utf-8")
        (base / "words" / (f + ".json")).write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")
        (base / "words" / (f + ".py")).write_text(WORD_PY % {"folder": f, "word": word}, encoding="utf-8")
        (base / (f + "ai_art.py")).write_text(ART_PY % {"folder": f}, encoding="utf-8")
        lst = base / "清单.tsv"
        lines = lst.read_text(encoding="utf-8").splitlines() if lst.exists() else ["# 画面设置清单"]
        lines = [l for l in lines if not (l.split("\t")[1:2] == [f])]
        lines.append("%02d\t%s\t%sai\tAI 生成 %s" % (len([l for l in lines if not l.startswith("#")]) + 1, f, f, time.strftime("%Y-%m-%d")))
        lst.write_text("\n".join(lines) + "\n", encoding="utf-8")
        # 总表视频细节数据：画面、插图，索引的「画面」列
        head, rows = C.read_index()
        rel = next((r[6] for r in rows if r[2] == word and len(r) > 6 and r[6]), "")
        if not rel:
            slug = word.replace(" ", "_").replace("/", "_")
            slug = slug + "_" if slug.lower() in C.RESERVED else slug
            rel = "词/%s/%s.json" % ((slug[:1].lower() if slug[:1].isalpha() else "_"), slug)
        p = C.REPO / C.D / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        rec = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"单词": word, "题目": None}
        rec.update({"画面": P, "插图": [f + "ai"], "画面生成": time.strftime("%Y-%m-%d") + " " + C.load_cfg().get("attribution", ""),
                    "检查": "还要补：都齐了（起草检查）" if checked else "本机检查通过，出片时再起草检查"})
        p.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        for r in rows:
            if r[2] == word:
                while len(r) < 7:
                    r.append("")
                r[5] = "细节数据有"
                r[6] = r[6] or rel
        C.write_index(head, rows)
    C.x("DELETE FROM picfail WHERE word=?", (word,))


def wsl_draft(word):
    """出片环境装好了：在 WSL 里用视频技能起草这个词，返回“还要补：……”那一行；没装好返回 None。"""
    if not V.has_wsl():
        return None
    env = V.env_status()
    if not env.get("ready"):
        return None
    f = V.folder_of(word)
    cmd = """set -o pipefail; . ~/.wordfilm-local.env 2>/dev/null
mkdir -p ~/kit-extra && cp -r %(src)s/. ~/kit-extra/ && find ~/kit-extra -name '*.py' -exec sed -i 's/\\r$//' {} +
A=~/wordfilm-work/%(f)s/art; rm -rf "$A"; mkdir -p "$A"; S=~/skills/word-construction-video
cp "$S/references/scenes/"*.svg "$A/"; cd "$S/scripts" && python3 poses.py "$A" --motion >/dev/null 2>&1
python3 ~/kit-extra/%(f)sai_art.py "$A" >/dev/null && python3 ~/kit-extra/words/%(f)s.py ~/wordfilm-work/edits_%(f)s.json >/dev/null || { echo '还要补：画面设置的程序跑不起来'; exit 0; }
timeout 600 python3 run.py --table "$TABLE" ${SYL:+--syl "$SYL"} --words %(w)s --number 1 --out /tmp/wv-draft --edits ~/wordfilm-work/edits_%(f)s.json \\
  --edition brief --draft-only --no-preview --work /tmp/wv-draft-%(f)s 2>&1 | grep -a '还要补' | tail -1
""" % {"src": V.q(V.to_wsl(C.REPO / EXTRA)), "f": f, "w": V.q(word)}
    rc, t = V.wsl(cmd, 900)
    line = (t.strip().splitlines() or [""])[-1].strip()
    return line or "还要补：起草没跑出结果（%s）" % t[-200:]


def pick(n, only=None):
    import video as V2
    pw = V2.pic_words()
    fail = {r["word"] for r in C.q("SELECT word FROM picfail")}
    _, rows = C.read_index()
    out = []
    for r in rows:
        w = r[2]
        if w in out or V2.folder_of(w) in pw or r[4] not in ("细节数据有", "总表有"):
            continue
        if only is not None:
            if w not in only:
                continue
        elif w in fail:
            continue
        out.append(w)
        if len(out) >= n:
            break
    return out


def do_pics(R, tid, p):
    """任务：给有题目、还没有画面的词做画面。R 是 core.RUNNER。"""
    total = int(p.get("count") or 0)
    only = set(p.get("words") or []) or None
    if only:
        C.x("DELETE FROM picfail WHERE word IN (%s)" % ",".join("?" * len(only)), list(only))
    done = 0
    batch = []
    rounds = int(C.load_cfg().get("fixRounds", 3))
    while True:
        R.check_stop()
        if not C.in_window():
            raise C.Stopped("window")
        if total and done >= total:
            break
        if not batch:
            C.sync()
        ws = pick(1, only)
        if not ws:
            C.log("没有要做画面的词了（要先有题目；做不出来的在“画面没做成”里）", tid)
            break
        w = ws[0]
        fix, ok = None, False
        for rnd in range(rounds + 1):
            rep = R.ask(tid, "做画面" if not rnd else "画面改第 %d 次" % rnd, build_prompt(w, fix), [w])
            P, raw, svgs, errs = parse(rep)
            errs = errs or check(w, P, svgs)
            checked = False
            if not errs:
                line = wsl_draft_safe(w, P, svgs)
                if line is not None:
                    checked = "都齐了" in line
                    if not checked:
                        errs = ["视频技能起草检查没过：" + line]
            if not errs:
                save(w, P, svgs, checked)
                ok = True
                break
            fix = (raw or json.dumps(P or {}, ensure_ascii=False), errs)
            C.log("  %s 的画面没过：%s" % (w, "；".join(errs)[:200]), tid)
        if ok:
            batch.append(w)
            C.log("  %s 的画面做好了" % w, tid)
        else:
            unsave(w)
            C.x("INSERT OR REPLACE INTO picfail(word, errors, ts) VALUES(?,?,?)", (w, json.dumps(errs, ensure_ascii=False), C.now()))
        done += 1
        R.progress(tid, processed=done, total=total or None)
        if len(batch) >= 5 or (only is not None and not pick(1, only)):
            _commit(tid, batch)
            batch = []
        if only is not None and not pick(1, only):
            break
    _commit(tid, batch)


def unsave(word):
    """起草检查最后也没过：把临时存的画面设置删掉，免得被当成“能出片”。"""
    f = V.folder_of(word)
    base = C.REPO / EXTRA
    with C.REPO_LOCK:
        for q_ in (base / "words" / (f + ".json"), base / "words" / (f + ".py"), base / (f + "ai_art.py")):
            if q_.exists():
                q_.unlink()
        if (base / "art" / f).exists():
            C.rmtree(base / "art" / f)
        lst = base / "清单.tsv"
        if lst.exists():
            lst.write_text("\n".join(l for l in lst.read_text(encoding="utf-8").splitlines() if l.split("\t")[1:2] != [f]) + "\n", encoding="utf-8")
        head, rows = C.read_index()
        for r in rows:
            if r[2] == word and len(r) > 6 and r[6]:
                p = C.REPO / C.D / r[6]
                if p.exists():
                    rec = json.loads(p.read_text(encoding="utf-8"))
                    if rec.get("画面"):
                        rec.update({"画面": None, "插图": []})
                        rec.pop("画面生成", None)
                        p.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
                r[5] = "缺"
        C.write_index(head, rows)


def wsl_draft_safe(w, P, svgs):
    """先存一份草稿到画面设置文件夹，让 WSL 能读到，再起草检查；没装好出片环境就跳过（返回 None）。"""
    try:
        if not (V.has_wsl() and V.env_status().get("ready")):
            return None
        save(w, P, svgs, False)            # 临时存，检查没过会被下一次覆盖；最后没过会清掉
        return wsl_draft(w)
    except Exception as e:
        return "还要补：起草检查出错（%s）" % str(e)[:100]


def _commit(tid, words):
    if not words:
        return
    cid = C.commit_pending("词库：画面设置 %s（%d 个词，网页 AI 做的）" % ("、".join(words[:6]) + ("…" if len(words) > 6 else ""), len(words)))
    if cid and C.load_cfg().get("autoPush", True):
        try:
            C.log(C.push(), tid)
        except Exception as e:
            C.log("上传没成功（%s），下次一起传" % str(e)[:150], tid)


def mock(prompt, words):
    w = words[0]
    f = V.folder_of(w)
    P = {"style": "core", "board": True,
         "pics": [{"text": "（模拟）%s" % w, "pos": "名词", "diff": "测试用", "bg": "blank", "img": "art/room-bg.svg",
                   "items": [{"svg": "art/%s-main.svg" % f, "x": 0.6, "y": 0.6, "s": 0.4, "z": 2},
                             {"actor": "walk-cn-girl", "x": 0.3, "y": 0.6, "s": 0.9, "z": 3}],
                   "ex": "This is a test.", "exzh": "这是测试。"}],
         "flow": [{"node": "① （模拟）", "pos": "名词", "pic": 0}]}
    return ("```json\n%s\n```\n<<<SVG %s-main.svg\n<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><circle cx=\"50\" cy=\"50\" r=\"40\" fill=\"#4a90d9\" stroke=\"#000\" stroke-width=\"3\"/></svg>\n>>>END\n%s"
            % (json.dumps(P, ensure_ascii=False), f, END))
