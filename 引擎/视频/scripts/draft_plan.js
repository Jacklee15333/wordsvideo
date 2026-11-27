#!/usr/bin/env node
// 按词条详情起草配音稿（plan.json），补好画面设置（prefs.json）。
// 用法：node draft_plan.js <details.json> <单词> <输出文件夹> [--style core|full] [--list unit.json]
//   core（默认）：只讲核心。开头一句“transport：运输、运送。”，拆开不说话，每个部分一句
//                （前缀、后缀讲清楚来自哪种语言、起什么作用），拼起来一句，现在的意思每个一句，
//                几个意思时再讲区别（词性 + 一句话），每个意思念一个例句（英文、中文各一句，配一段动画），小黑板不说话。
//   full：原来的详细版（来历、意思一步步变过来、同一词族都讲，小黑板照着念）。
//   --list：unit_words.py --json 存下的单词表（有“含义”一列的话，开头和画面用单词表里的意思）
// 输出文件夹里已经有 prefs.json（手写的画 pics、扩展词 extend、图标…）的，原样保留，只补上 style、board。
// 另存一份 plan.auto.json：run.py 看到 plan.json 和它一模一样（没手改过），就会按最新的画面设置重新起草。
'use strict';
const fs = require('fs');
const path = require('path');
global.window = {};
require(path.join(__dirname, 'wordfilm.js'));
const WF = window.WordFilm;

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const [detailsPath, word, outDir] = args.filter((a, i) => !a.startsWith('--') && !(i > 0 && args[i - 1].startsWith('--')));
if (!detailsPath || !word || !outDir) { console.log('用法：node draft_plan.js <details.json> <单词> <输出文件夹> [--style core|full] [--list unit.json]'); process.exit(1); }
const style = opt('--style', 'core') === 'full' ? 'full' : 'core';
const details = JSON.parse(fs.readFileSync(detailsPath, 'utf8'));
const d = details[word] || Object.values(details).find(x => x.w.toLowerCase() === word.toLowerCase());
if (!d) { console.error('details.json 里没有 ' + word); process.exit(2); }
let listMeaning = '';
if (opt('--list')) {
  const L = JSON.parse(fs.readFileSync(opt('--list'), 'utf8'));
  const hit = L.find(x => x.word.toLowerCase() === word.toLowerCase());
  if (hit && hit.meaning) listMeaning = hit.meaning.replace(/^([a-z]+\.\/?)+\s*/i, '').replace(/^(短语|词组)\s*/, '').trim();
}
fs.mkdirSync(outDir, { recursive: true });
const prefsPath = path.join(outDir, 'prefs.json');
let prefs = {};
if (fs.existsSync(prefsPath)) {
  try { prefs = JSON.parse(fs.readFileSync(prefsPath, 'utf8')); } catch (e) { console.error('prefs.json 读不了（' + e.message + '），按默认起草'); prefs = {}; }
}
prefs.style = style;
if (prefs.board == null) prefs.board = true;
if (listMeaning) { prefs.text = prefs.text || {}; if (!prefs.text.final) prefs.text.final = listMeaning; }
const film = WF.build(d, prefs);

// ---------- 念出来的样子
const CN = ['零', '一', '两', '三', '四', '五', '六', '七', '八'];
// 6.17：词根、词缀都当单词念，不再一个字母一个字母念（用户：“前后缀，词根要当作单词来读，不要变成单个字母读”“词根，词缀当单词读，用美语音色”）。
// 词根照写（duc），前缀写成 pro-、后缀写成 -ion：synth.py（readings.py）认连字符，按词缀表念；词典里没有的词根用 espeak-ng 的读音，都是美式女声
const spoken = t => String(t || '').replace(/\([^()]*\)$/, '').replace(/[()（）]/g, '').replace(/^-+|-+$/g, '').trim();
const spokenAs = (t, kind) => { const s = spoken(t); return !s ? '' : kind === 'pre' ? s + '-' : kind === 'suf' ? '-' + s : s; };
// 6.17：音变、“为什么 p 会变成 f？”里的字母讲的是音（用户：“p --- f 这些讲的是发音，不能按字母来读……这些因该是因素，要当作读音来读的”）：
// 换成 /音标/，美式女声念这个音（th 念 /θ/；原始印欧语的 dh、bh、gh 是带气的 /dʰ/ /bʰ/ /ɡʰ/）。别处单独的字母还是字母，用你本人的声音念字母名
const SOUND_IPA = { p: 'p', b: 'b', t: 't', d: 'd', k: 'k', c: 'k', g: 'ɡ', q: 'k', f: 'f', v: 'v', th: 'θ', dh: 'dʰ', bh: 'bʰ', gh: 'ɡʰ', h: 'h', s: 's', z: 'z',
  sh: 'ʃ', ch: 'tʃ', kw: 'kw', qu: 'kw', gw: 'ɡw', hw: 'hw', wh: 'hw', ph: 'f', x: 'ks', w: 'w', l: 'l', r: 'r', m: 'm', n: 'n', j: 'j', y: 'j', a: 'ɑ', e: 'ɛ', i: 'i', o: 'o', u: 'u' };
// 辅音连着写的（sk、str、原始印欧语的 gwh）按字母组拼出音：gwh → /ɡwʰ/；有元音的两三个字母（do、the）不动
const SOUND_DI = ['th', 'dh', 'bh', 'gh', 'sh', 'ch', 'kw', 'qu', 'gw', 'hw', 'wh', 'ph'];
const soundOf = w => {
  const k = w.toLowerCase();
  if (SOUND_IPA[k]) return SOUND_IPA[k];
  if (/[aeiou]/.test(k)) return '';
  let out = '', i = 0;
  while (i < k.length) { const d = SOUND_DI.find(x => k.startsWith(x, i)) || k[i]; if (!SOUND_IPA[d]) return ''; out += d === 'gh' && i ? 'ʰ' : SOUND_IPA[d]; i += d.length; }
  return out;
};
const sounds = t => String(t || '').replace(/(^|[^A-Za-z'’\/-])([A-Za-z]{1,3})(?=$|[^A-Za-z'’\/-])/g, (m0, a, b) => { const x = soundOf(b); return x ? a + ' /' + x + '/ ' : m0; })
  .replace(/\s+/g, ' ').replace(/\s*([，。；、：？！])\s*/g, '$1').trim();
// 括号里的注释、省略号、引号不念；箭头念成停顿；斜杠念“或”；加号念“加”
const say = s => String(s || '')
  .replace(/（[^（）]*）|\([^()]*\)/g, '')
  .replace(/([A-Za-z])\s*[“「『]/g, '$1，')
  .replace(/…+|\.{3,}/g, '')
  .replace(/\s*[→⇒]\s*/g, '，')
  .replace(/\s*[\/／]\s*/g, '或')
  .replace(/\s+\+\s+/g, ' 加 ')
  .replace(/[“”"「」『』]/g, '')
  .replace(/\s+/g, ' ')
  .replace(/^[，、；：,;:\s]+|[，、；：,;:\s]+$/g, '')
  .trim();
const sayExample = s => say(s).replace(/([A-Za-z])['’]s\b/g, '$1').replace(/([A-Za-z.!?])\s*([\u3400-\u9fff])/g, '$1，$2');
function glossSay(g) {
  let t = say(g);
  if (/^=/.test(t)) return { verb: '就是 ', t: t.replace(/^=\s*/, '') };
  if (/^的/.test(t)) return { verb: '表示', t: t.replace(/^的/, '') };
  return { verb: '意思是：', t };
}
const main = say(listMeaning || film.meaning.main);
const lit = film.combo ? say(film.combo.literal) : '';
const fromSay = f => (f === '英语本族' ? '英语本族的' : f);
function sameAs(sub) {
  const m = /同\s*([A-Za-z][A-Za-z-]{2,})\s*([\u3400-\u9fff]{1,6})/.exec(String(sub || ''));
  return m ? '比如 ' + m[1] + '，' + m[2] + '。' : '';
}
// 一个部分怎么讲：前缀、后缀说清楚来自哪种语言、起什么作用；词根、单词说意思（知道来源也带上）。
// 英文放在“前缀是 / 后缀是 / 词根是 / 单词是”后面念最清楚（实测：英文词打头再接逗号和中文常被念糊；“词根 port”的 t 会被吞）
// 6.26.3（第六十六版，用户：“speak，-er 不要说英语本来就有，换成英语本土词……要用更专业的”）：英语词汇学的说法——本族语词（native words），
// 念“英语本族词 / 英语本族前缀 / 英语本族后缀 / 英语本族词根”，和总表（维护技能第 125 条）一样
const BZ_KIND = { pre: '前缀', suf: '后缀', word: '词', root: '词根' };
const fromPhrase = (f, k) => (!f ? '' : f === '英语本族' ? '英语本族' + (BZ_KIND[k] || '词根') + '，' : '来自' + f + '，');
// 6.43（第八十七版）：精简版直接说“英语前缀是 un-”“拉丁语词根是 port”，不说“来自…”（用户：“直接说英语前后缀，词根；拉丁语前后缀，词根就可以了，不用说来自”）。
// 英文照旧放在“是”后面念（实测最清楚，见 narration-guide 第五节）
const LEAN_K = { pre: '前缀', suf: '后缀', word: '单词', root: '词根' };
const leanFrom = f => { const s = String(f || '').replace(/（[^（）]*）|\([^()]*\)/g, '').trim(); return /^(英语本族|英语本来就有|古英语)$/.test(s) ? '英语' : s; };
const leadIn = (p, k, sp) => (prefs.lean ? (k === 'word' ? '' : leanFrom(p.from)) + LEAN_K[k] + '是 ' + sp + '，' : LEAN_K[k] + '是 ' + sp + '，' + fromPhrase(p.from, k));
// 5.1 起：总表那一行末尾的“记：stat ≈ stand（站）：……”念成“记法：stat，约等于 stand，站。……”
// ≈ 念“约等于”（真的是一家），∽ 念“长得像”（只帮助记忆），← 念“来自”
function memoLine(p) {
  const m = p.memo;
  if (!m) return '';
  const link = m.sym === '≈' ? ' 约等于 ' : m.sym === '←' ? ' 来自 ' : ' 长得像 ';
  const why = m.why && !prefs.lean ? say(m.why).replace(/[。]+$/, '') : '';      // 6.43：精简版“记”只念关键的一句，下面的解释不念
  // 5.11：词根和单独的词写法一样（port ≈ port 港口）：不说“port 约等于 port”
  if (m.same) return '记法：' + m.b + ' 单独用也是一个词，意思是' + say(m.zh) + '。' + (why ? why + '。' : '');
  // 5.1 实测：“长得像 roar，吼叫”这种英文后面紧跟逗号的念不清，改成“X 这个词，意思是…”
  return '记法：' + spokenAs(m.a, p.kind) + link + m.b + ' 这个词，意思是' + say(m.zh) + '。' + (why ? why + '。' : '');
}
// 5.11：说明里单独的一两个字母（f、dh、ct）、没有元音的三个字母（gwh、tch）一个字母一个字母念；do、an 这类真单词照常念
const KEEP2 = new Set(['do', 'an', 'is', 'to', 'in', 'on', 'of', 'or', 'as', 'at', 'be', 'by', 'he', 'it', 'me', 'my', 'no', 'so', 'up', 'us', 'we', 'go']);
const letters = t => String(t || '').replace(/(^|[^A-Za-z'’-])([A-Za-z]{1,3})(?=$|[^A-Za-z'’-])/g, (m0, a, b) =>
  (b.length === 1 || (b.length === 2 && !KEEP2.has(b.toLowerCase())) || (b.length === 3 && !/[aeiouy]/i.test(b)) ? a + b.toLowerCase().split('').join(' ') : m0));
// 5.11：记法后面的“音变”：先说谁对谁（f 对 d），再念那一句话（括号里的老祖宗、别的例子不念）；一条链的只念那一句话
function shiftLine(sh) {
  const body = sounds(say(sh.text)).replace(/[。]+$/, '');                  // 6.17：讲的是音，念音（/p/ 对 /f/）
  if (sh.pairs && sh.pairs.length) return '音变：' + sh.pairs.map(([a, b]) => sounds(' ' + a + ' ') + ' 对 ' + sounds(' ' + b + ' ')).join('，') + '。' + (body ? body + '。' : '');
  return '音变：' + (body ? body + '。' : '');
}
// 5.11：一个部分讲几句：第 1 句讲这一部分；词根的另一种写法（duct = duc）先说词根本身，再说“在这里写成 duct”和字母怎么变的；
// 有记法的再加记法一句，记法带音变的再加一句。分了句，卡片上的东西就能“说到才出现”
// 字母怎么变的那半句（“英语加不发音的 e”“d u c 后面加 t”）
// 6.5：音变的原因（总表“；原因：…”）：“为什么英语念成 f 呢？英语属于日耳曼语，……这叫格林定律；拉丁语没有这样变。”
function whyLine(sh) {
  const to = sh.pairs && sh.pairs.length === 1 ? sounds(' ' + sh.pairs[0][1] + ' ') : '';
  return (to ? '为什么英语念成 ' + to + ' 呢？' : '为什么会这样呢？') + sounds(say(sh.why)).replace(/[。]+$/, '') + '。';
}
function howSay(p) {
  const sp = spoken(p.base);
  return p.howShort ? letters(say(p.howShort)).replace(new RegExp('(^|[^A-Za-z])' + p.base + '(?=$|[^A-Za-z])', 'g'), (m0, a) => a + sp).replace(/(^|\s)-([a-z]{1,4})(?=$|[^A-Za-z])/g, '$1$2').replace(/[。]+$/, '') : '';
}
function partSegs(p) {
  const segs = [];
  if (p.xt) {                                       // 6.8：总表“词根形态版”：先说词根本身 duc 和意思，写法不一样的再说“在这里写成 duce”
    segs.push(leadIn(p, 'root', spoken(p.xt.root)) + '意思是：' + say(p.xt.gloss) + '。');
    if (p.xt.spelled) segs.push('在这里写成 ' + spoken(p.text) + '。' + (p.xt.short ? letters(say(p.xt.short)).replace(/[。]+$/, '') + '。' : ''));
  } else if (p.base && !p.pp && (p.kind === 'root' || p.kind === 'word')) {
    const g = glossSay(p.rootGloss || p.gloss), sp = spoken(p.base);
    segs.push(leadIn(p, 'root', sp) + (g.t ? g.verb + g.t : say(p.text)) + '。');
    const hereG = p.gloss && p.rootGloss && !p.rootGloss.includes(p.gloss) && !p.gloss.includes(p.rootGloss) ? '，是' + say(p.gloss) : '';
    const hs = howSay(p);
    // 6.4：后面有“身份和分工”那一幕的（p.varInFg），字母怎么变的挪到那一幕讲，这里只说“在这里写成 duce”
    segs.push('在这里写成 ' + spoken(p.text) + hereG + '。' + (hs && !p.varInFg ? hs + '。' : ''));
  } else segs.push(partLine0(p));
  if (p.memo) {
    segs.push(memoLine(p));
    if (p.memo.shift && !prefs.brief) segs.push(shiftLine(p.memo.shift));          // 6.19：精简版不讲音变（“视频讲解的太复杂了，我希望视频能分成两个版本：一、精简版，放前面：精简版…）
    if (p.memo.shift && p.memo.shift.why && !prefs.brief && !WF.yinbianOf(p.memo.shift)) segs.push(whyLine(p.memo.shift));      // 6.5：音变的原因单独一句（6.6：新写法的原因在下一幕“为什么 p 会变成 f？”讲）
  }
  return segs;
}
const partScene = p => { const segs = partSegs(p); return segs.length > 1 ? { marks: true, segs } : { segs }; };
function partLine(p) { return partSegs(p).join(''); }
function partLine0(p) {
  const g = glossSay(p.gloss), sp = spokenAs(p.head || p.text, p.kind);
  const gl = g.t ? g.verb + g.t : '';
  if (p.kind === 'pre') return leadIn(p, 'pre', sp) + (gl || say(p.role)) + '。';
  if (p.kind === 'suf') {
    let s = leadIn(p, 'suf', sp) + (p.role ? say(p.role) + '。' : '');
    // 总表各部分解释里“在这里：…”讲的词性变化；母词意思有过渡的，先讲本义怎么变成这个意思
    if (p.here) return s + '在这里，' + (p.bridge ? p.bridge.w + ' 本义是' + say(p.bridge.orig) + '，' + say(p.bridge.why) + '，就成了' + say(p.bridge.best) + '。' : '') + say(p.here) + '。';
    const zh = [...(g.t || '')].filter(c => /[\u3400-\u9fff]/.test(c));
    const repeat = p.role && zh.length && zh.filter(c => p.role.includes(c)).length / zh.length >= 0.6;     // 和作用说的是一回事就不再说
    const plain = g.t && !/名词|动词|形容词|副词/.test(g.t) && g.t.length <= 12 && !repeat;
    if (plain) s += (p.role ? '在这里' : '') + gl + '。';
    else if (!p.role && gl) s += gl + '。';
    return s;
  }
  if (p.pp && (p.kind === 'root' || p.kind === 'word')) return '词根是 ' + sp + '，就是 ' + spoken(p.pp) + (/由词根|的另一种写法/.test(p.sub || '') ? ' 在过去分词里的样子，' : ' 的过去分词形式，') + (gl || say(p.text)) + '。';   // 4.0 起：competit(=compete)
  if (p.kind === 'word') return leadIn(p, 'word', sp) + (gl || say(p.text)) + '。';   // 总表「单词部分」列里的词（make、up）
  return leadIn(p, 'root', sp) + (gl || say(p.text)) + '。';
}
// 几个意思的区别：“第一个是动词，指把人或货物运到别的地方；”（pics 里的 pos、diff）
function diffLine(x, i, n) {
  const df = x.diff ? (/^(指|说的是|表示|是|用来)/.test(x.diff) ? x.diff : '指' + x.diff) : '';
  const body = [x.pos ? '是' + x.pos : '', say(df)].filter(Boolean).join('，');
  return body ? ['第一个', '第二个', '第三个'][i] + body + (i === n - 1 ? '。' : '；') : '';
}
// 一个意思是怎么从字面意思变过来的：evoSay 手写的整句；没有就用 evo 的几步拼，最后说出这个意思和词性
function evoLine(x, i, n) {
  let body = '';
  if (x.evoSay) body = say(x.evoSay);
  else if (x.evo && x.evo.length) body = x.evo.map(say).join('，') + '，就是' + say(x.text) + (x.pos ? '，这是' + x.pos : '');
  if (!body) return '';
  return (i === 0 ? '它们是怎么来的呢？' : '') + body + (i === n - 1 ? '。' : '；');
}
// 演变那一幕：除了第一个框（字面意思），每一框一句；手写的 say 为准，没写就“为什么（via），就是这个意思，这是什么词”
const bare = t => say(String(t || '').replace(/^[①②③]\s*/, ''));
function stopSay(s) {
  if (Array.isArray(s.sayList) && s.sayList.length) return s.sayList.map(x => endDot(say(x)));     // 5.0 起：一步拆成几句（示意图按句出东西）
  if (s.say) return endDot(say(s.say));
  if (s.rule) return endDot('英语里，' + say(s.rule) + '。' + (s.via ? say(s.via) + '，' : '') + '就是' + bare(s.node) + (s.pos ? '，这是' + s.pos : ''));   // 总表标了用词规律的一步：先念规律
  return endDot((s.via ? say(s.via) + '，' : '') + '就是' + bare(s.node) + (s.pos ? '，这是' + s.pos : ''));
}
function evolveScene() {
  const st = film.flow || [];
  const per = st.slice(1).map(stopSay);
  const spec = { marks: true, intro: film.pics.filter(x => x.text).length >= 2 ? '它们是怎么来的呢？' : '这个意思是怎么来的呢？', segs: [].concat(...per) };
  if (per.some(x => Array.isArray(x))) spec.groups = per.map(x => (Array.isArray(x) ? x.length : 1));
  return spec;
}
function meaningScene() {
  const ps = film.pics.filter(x => x.text);
  if (ps.length >= 2 && film.flow) {                     // 演变单独一幕讲，这里只说有哪几个意思
    return { marks: true, intro: '现在有' + CN[ps.length] + '个意思：', segs: ps.map((x, i) => ['一是', '二是', '三是'][i] + say(x.text) + (i === ps.length - 1 ? '。' : '，')) };
  }
  if (ps.length >= 2) {
    const segs = ps.map((x, i) => ['一是', '二是', '三是'][i] + say(x.text) + (i === ps.length - 1 ? '。' : '，'));
    const evos = ps.map((x, i) => evoLine(x, i, ps.length));
    const diffs = ps.map((x, i) => diffLine(x, i, ps.length));
    const useful = ps.some(x => x.diff) || new Set(ps.map(x => x.pos)).size > 1;
    if (evos.every(Boolean)) segs.push(...evos);                                     // 讲清楚每个意思怎么变过来（词性也在里面）
    else if (useful && diffs.every(Boolean)) segs.push(...diffs.map((s, i) => (i ? '' : '区别是：') + s));
    return { marks: true, intro: '现在有' + CN[ps.length] + '个意思：', segs };
  }
  if (ps.length === 1 && !film.flow && (ps[0].evoSay || ps[0].evo.length)) return { segs: [evoLine(ps[0], 0, 1).replace(/^它们是怎么来的呢？/, '')] };
  return { segs: ['所以，' + d.w + ' 就是' + (ps.length ? say(ps[0].text) : main) + '。'] };
}
// 例句：先念英文，再念中文
const endDot = t => String(t).replace(/[，、；：,;:\s]+$/, '') + (/[。！？!?]$/.test(t) ? '' : '。');
// 6.28：例句动画里有“要找空当放”的音效（say: 一句话，或写了 gap 的），念完那一句多停一会儿（waits），让它放得下、不压着讲解
const exampleScene = pc => {
  const sc = { marks: true, segs: [String(pc.ex).trim()].concat(pc.exzh ? [endDot(say(pc.exzh))] : []) }, w = {};
  ((pc.exPic || {}).items || []).forEach(it => {
    const nm = String(it.sound || it.sfx || '');
    if (nm && (it.gap || nm.startsWith('say:'))) { const c = String(it.cue != null ? it.cue : 0); w[c] = Math.max(w[c] || 0, Number(it.wait) || 2.0); }      // 6.34：音效最长 1.6 秒，念完那一句停 2 秒才放得下（以前普通音效停 1 秒，1.6 秒的 rain 找不到空当就没放）
  });
  if (Object.keys(w).length) sc.waits = w;
  return sc;
};
// 3.7 起：合成规律那一幕，一条规律一句：先念“英语里，规律”，再念本词的例子（“A → B”念成“A，就成了 B”；-ed 这类词尾一个字母一个字母念）
const sayRule = t => say(t).replace(/(^|[^A-Za-z])-([a-z]+)\b/g, '$1 -$2 ').replace(/\s+/g, ' ').replace(/\s([，。；、：])/g, '$1').trim();      // 6.17：-ed 这类词尾当单词念（词缀表），不再 e d
const sayCompEx = ex => say(String(ex || '').replace(/\s*→\s*/g, '，就成了 '));
// 4.0 起：“构词”那张卡：先念这个词是怎么来的，再念规律，最后把链一步步念出来（competere，一起争取，过去分词是 competitus，词干 competit，就成了 competitio）
const plainZh = t => String(t || '').replace(/（[^（）]*）/g, '');
const sayChain = c => String(c || '').split(/\s*→\s*/).map((x, i, a) => {
  const t = x.trim().replace(/（([^（）]*)）/g, '，$1').replace(/^过去分词\s+/, '过去分词是 ').replace(/^词干\s+(\S+?)-?$/, '词干 $1');
  return i === a.length - 1 && i > 0 ? '就成了 ' + t : t;
}).join('，');
const gouciLine = it => [it.intro ? endDot(sayRule(plainZh(it.intro))) : '', endDot(sayRule(plainZh(it.text).replace(/造“[^”]*”的\s*/g, '的 '))),
  it.chain ? endDot(say(sayChain(it.chain))) : ''].join('');   // 6.17：-ation 这类词尾留着连字符，synth.py 按词缀表念
const ruleScene = () => ({ marks: true, segs: (film.compShow || []).map(it => it.kind === '构词' ? gouciLine(it) : endDot('英语里，' + sayRule(it.text)) + (it.first ? endDot(sayCompEx(it.first)) : '')) });

// 5.0 起：读音拆分。一块一块念（音素词：念出来正好是这一块的音），再“连起来”念整词，最后说重音在第几块；
// 对不齐的词只念整词。音素词的读法写在 plan.json 的 lexicon 里（synth.py 加进配音模型的词典）
const CNB = ['零', '一', '两', '三', '四', '五', '六', '七', '八', '九', '十'];
const ORD = ['第一', '第二', '第三', '第四', '第五', '第六', '第七', '第八', '第九', '第十'];
// 6.26：读音现象的配音：括号里的不念；几个字母连写的（sp、ci、du、ex、ch、gh、ct……）一个个字母念（你本人的声音念字母名），
// 不然英文声音会把 sp 当成一个词去念；/b/ /ʃ/ 这种照旧念音
const DY_VOW = /(?<![A-Za-z\/'’-])(ssi|sci|ssu|wor|qua|ci|ti|si|ce|xi|su|du|tu|di|ex|wa|or)(?![A-Za-z\/'’-])/g;
const DY_CONS = /(?<![A-Za-z\/'’-])([bcdfghjklmnpqrstvwxz]{2,4})(?![A-Za-z\/'’-])/g;
const dySay = z => String(z || '').replace(/（[^（）]*）/g, '').replace(/\([^()]*\)/g, '')
  .replace(DY_VOW, m => m.split('').join(' ')).replace(DY_CONS, m => m.split('').join(' ')).replace(/\s+/g, ' ').replace(/ ([，。；：！？、])/g, '$1').trim();
function duyinScene(x) {
  if (!x) return { marks: true, segs: [] };
  // 6.26.2：念“一句话”（总表第三稿里给视频的重点），没有才念整段“为什么”——视频不拖长
  const what = dySay(x.what), why = dySay(x.short || x.why);
  // 6.33（第七十七版）：精简版只讲现象，不讲原因（用户：“音频变化的原因视频里面就不需要讲了，到时候放在完全版里面再讲，精简版里不用讲”）
  return { marks: true, segs: why && !prefs.brief ? [what, '为什么呢？' + why] : [what] };
}
function sylScene() {
  const pr = film.pron, real = pr.chunks.filter(c => !c.sep), nb = real.length;
  // 6.43（第八十七版，用户：“直接拆分读，不要有男生的解释，把解释部分去掉；比如 unusual：u nu su al 几个部分读完就可以了，最后标出重音部分”）：
  //   精简版只念一块一块（美式女声），不说“分成几块来读”“连起来”“重音在第几块”；合成整词、标重音不说话，hold 留出这几秒
  if (prefs.lean) {
    if (!pr.ok) return { marks: true, segs: [d.w + '。'], hold: pr.stress >= 0 && nb > 1 ? 1.2 : 0.4 };
    const blocks = pr.read.map(ci => pr.chunks[ci].key);
    return nb > 1 ? { marks: true, segs: blocks, hold: pr.stress >= 0 && pr.read.length > 1 ? 1.7 : 1.1 } : { marks: true, segs: blocks };
  }
  if (!pr.ok) return { marks: true, intro: nb > 1 ? '分成' + CNB[nb] + '块：' : '', segs: [d.w + '。'] };
  const segs = pr.read.map(ci => pr.chunks[ci].key);              // 一块一块念：正常语速（放慢了前面会带出气声）
  if (nb > 1) segs.push('连起来：' + pr.key + '。');
  if (pr.stress >= 0 && pr.read.length > 1) segs.push('重音在' + ORD[real.indexOf(pr.chunks[pr.stress])] + '块。');
  return nb > 1 ? { marks: true, intro: '分成' + CNB[nb] + '块来读：', segs } : { marks: true, segs };
}

// 6.3：辨析后面有“关系”的（part.rel），几条辨析讲完再念一句“再看它们的关系：…”（见 fengongScene）。
// 6.2：词缀行是新写法的（part.bx），这一幕叫“前缀辨析 / 后缀辨析”：第 1 句“再来辨析一下。同样…的，有这么几个。”，后面一条辨析一句（最多 3 条）。
// 6.0：“身份和分工”那一幕。第 1 句：这一部分是什么身份；（6.1：词根是拉丁语动词的，第 2 句讲三个样子的变化规律，见 verbSay；）后面一条分工一句（只讲挑出来的几条，括号里的例词念前两个）；
// 最后一句：总表里的“为什么用 -ous 不用 -ful：…”。词缀照写法念：三个字母以内一个字母一个字母念（o u s），长的当单词念（able）
// 6.17：词缀不再一个个字母念，留着连字符（-ous、pre-、-ere）：synth.py 按词缀表当单词念（用户：“前后缀，词根要当作单词来读，不要变成单个字母读”“词根，词缀当单词读，用美语音色”）
const sayAffix = t => String(t || '')
  .replace(/(^|[^A-Za-z])-([a-z]+)(?![a-z-])/g, '$1 -$2 ')
  .replace(/(^|[^A-Za-z])([a-z]+)-(?![a-z])/g, '$1 $2- ')
  .replace(/\s+/g, ' ').replace(/\s([，。；、：])/g, '$1').replace(/([，。；、：])\s/g, '$1').trim();
// 6.6：辨析写成“pre- 拉丁语，表示…”“pro- 也是拉丁语，…”“fore- 英语自己的，…”（用户：“简化成：拉丁语，表示时间、顺序上的“先”…”）：
//   画面照表写，配音补上“来自 / 是”，念着顺（“p r e 来自拉丁语，表示…”“fore 是英语自己的，…”）；老写法“是拉丁语来的”不动
const BX_HEAD = '^((?:-?[a-z]+-?)(?:[、和与\\s]+-?[a-z]+-?)*\\s*)';
// 6.7：总表“辨析精简演示版”：“pre- 拉丁语，…”“-al、-ic 拉丁语、希腊语，…”“inter- 拉丁语：…”“fore- 英语本族，…”——画面照写，配音补“来自 / 是”
const BX_LANG = '((?:拉丁语|希腊语|法语|古法语)(?:、(?:拉丁语|希腊语|法语|古法语))*)';
const bxSay = t => String(t)
  .replace(new RegExp(BX_HEAD + '(也是|是)?' + BX_LANG + '([，：])'), (m0, h, ye, lg, pu) => h + (ye === '也是' ? '也' : '') + '来自' + lg + pu)
  .replace(new RegExp(BX_HEAD + '(英语自己的|英语本族的|英语本族)([，：])'), (m0, h, a, pu) => h + '是' + (a === '英语本族' ? '英语本族的' : a) + pu);
function fgSay(p, r) {
  // “过去分词“被领出来的”，当名词”：引号去掉以后要断一下，不然念成“过去分词被领出来的”
  // 6.2：词缀的辨析里“不…的”“…之前的”这类带省略号的说法，省略号念成“什么”（照老办法去掉就成了“是不的”“是之前的”，听不懂）
  // 6.7：每个用法后面的例词括号换成“比如 preschool，上学以前的”（演示词 + 字面意思，画面上这时出演示）；没有演示的念前两个例词
  let raw = String(r.text);
  if (p.bx && r.uses && r.uses.length && r.raw) {
    let o = '', last = 0;
    r.uses.forEach(u => { o += r.raw.slice(last, u.at) + (u.demo && u.demo.lit ? '，比如 ' + u.ex[0] + '，' + u.demo.lit + '；' : '，比如 ' + u.ex.slice(0, 2).join('、') + '；'); last = u.end; });
    raw = (o + r.raw.slice(last)).replace(/；\s*[，；]/g, '；').replace(/；\s*$/, '');
  }
  const src = p.bx ? bxSay(raw).replace(/…+/g, '什么') : raw;
  const inl = p.bx && r.uses && r.uses.length && r.raw;
  let t = sayAffix(say(src.replace(/(过去分词|现在分词)“([^”]*)”[，]?/g, '$1，$2，')));
  if (p.base && /^[a-z]{1,3}$/i.test(p.base)) t = t.replace(new RegExp('(^|[^A-Za-z])' + p.base + '(?=$|[^A-Za-z])', 'g'), (m0, a) => a + spoken(p.base));
  t = t.replace(/[。]+$/, '');
  return t + (r.ex.length && !inl ? '，比如 ' + r.ex.slice(0, 2).join('、') : '') + '。';
}
// 6.1：“三个样子”那一句。先一句很短的引子（原形、过去式、过去分词画面上三个框写着，不再念一遍；没有单独过去式的动词说“本来有三个样子”，
// 接规律里的“这个动词…没有单独的过去式”），再念规律：括号里的（拉丁语、英语整词）不念，
// 词根三个字母以内的一个字母一个字母念，-avi、-atus 这类词尾照 sayAffix 念
function verbSay(p) {
  const V = p.verb, three = V.forms.length >= 3;
  let t = sayAffix(say(String(V.rule).replace(/(过去分词|现在分词)“([^”]*)”[，]?/g, '$1，$2，')));
  const base = p.base || String(p.text || '').replace(/\(.*?\)/g, '');
  if (base && /^[a-z]{1,3}$/i.test(base)) t = t.replace(new RegExp('(^|[^A-Za-z])' + base + '(?=$|[^A-Za-z])', 'g'), (m0, a) => a + spoken(base));
  t = letters(t).replace(/[。]+$/, '');
  return (three ? '拉丁语动词也有三个样子。' : '拉丁语动词本来有三个样子。') + t + '。';
}
// 6.5：三个样子一句一步（和画面的 verbPlan.steps 一一对上）：第一句先说“拉丁语动词也有三个样子。”再念原形那一栏的规律；
// 规律里括号中的（拉丁语、英语整词）不念，词根三个字母以内的一个字母一个字母念；分工那一条照 fgSay 念
function verbSegs(p) {
  const P = p.vplan, rows = p.fgRows || [], three = p.verb.forms.length >= 3;
  const base = p.base || String(p.text || '').replace(/\(.*?\)/g, '');
  const ruleSay = c => {
    let t = sayAffix(say(String(c).replace(/(过去分词|现在分词)“([^”]*)”[，]?/g, '$1，$2，')));
    if (base && /^[a-z]{1,3}$/i.test(base)) t = t.replace(new RegExp('(^|[^A-Za-z])' + base + '(?=$|[^A-Za-z])', 'g'), (m0, a) => a + spoken(base));
    return letters(t).replace(/[。；]+$/, '');
  };
  let first = true;
  return P.steps.map(s => {
    if (s.t === 'row') return fgSay(p, rows[s.i]);
    const t = P.cols[s.k].map(ruleSay).join('；') + '。';
    if (!first) return t;
    first = false;
    return (three ? '拉丁语动词也有三个样子。' : '拉丁语动词本来有三个样子。') + t;
  });
}
// 6.6：“为什么 p 会变成 f？”那一幕（总表音变后面的“；原因：…；发音：…；起因：…；例子：…”，wordfilm.js 的 yinbianOf 切开）。
//   一句讲一块，和画面一一对上：总说（格林定律）→ 念 p → 念 f → 两个音像在哪儿、差在哪儿 → 日耳曼人为什么这样念 → 例子（只念英语词，拉丁语、希腊语整词只写不念）
function yinbianScene(p) {
  const Y = WF.yinbianOf(p.memo.shift);
  const sp = x => sounds(' ' + x + ' ');                                    // 6.17：p、f、th 讲的是音，念音
  const L = s => sounds(say(s)).replace(/[。；，、]+$/, '');
  const segs = Y.steps.map(k => {
    if (k === 'gen') return '为什么英语念成 ' + sp(Y.b) + ' 呢？' + L(Y.gen) + '。';
    if (k === 'a') return sp(Y.a) + ' 为什么能变成 ' + sp(Y.b) + ' 呢？先看嘴巴。念 ' + sp(Y.a) + '，' + L(Y.A) + '。';
    if (k === 'b') return '再念 ' + sp(Y.b) + '，' + L(Y.B) + '。';
    if (k === 'c') return L(Y.C) + '，所以 ' + sp(Y.a) + ' 容易念成 ' + sp(Y.b) + '。' + (Y.extra ? '另外，' + L(Y.extra) + '。' : '');
    if (k === 'qi') return '日耳曼人为什么会这样念呢？' + L(Y.qi) + '。';
    return '再看几个例子：' + Y.li.map(x => x.en).join('、') + '。';
  });
  return { marks: true, segs };
}
// 6.8：词根的“形态”。开头一句：几个形态（像英语的 do、did、done）；每个形态先一句演示（名字 + 写法 + 从哪来、怎么变、去掉哪个词尾；拉丁语整词只写不念），
// 有英语用法的再一句（讲本词用的那一条，比如前两个例词）；只有一句话的（英语里几乎不用）接在演示那句后面。一句一步，和 wordfilm.js 的 xtSteps 一一对上
function xingtaiScene(p) {
  const X = p.xt, rt = spoken(X.root), names = X.forms.map(f => f.k);
  const an = X.analogy ? '，就像英语的 ' + X.analogy.replace(/\s*→\s*/g, '、') : '';
  const sp = t => String(t).replace(new RegExp('(^|[^A-Za-z])' + X.root + '(?=$|[^A-Za-z])', 'g'), (m0, a) => a + rt);
  const L = t => letters(sp(sayAffix(say(String(t).replace(/(过去分词|现在分词)“([^”]*)”[，]?/g, '$1，$2，'))))).replace(/[。；，]+$/, '');
  const segs = [rt + ' 有' + CN[names.length] + '个形态：' + names.join('、') + an + '。'];
  WF.xtSteps(X).slice(1).forEach(s => {
    const fm = X.forms[s.j];
    if (s.t === 'demo') {
      if (!fm.en) { segs.push(fm.k + '：' + L(fm.src) + '。'); return; }
      let src = fm.src;
      if (fm.la) src = src.replace(fm.la + '“' + fm.zh + '”', '').replace(/来自(拉丁语|希腊语)?(原形|过去式|过去分词|所有格|比较级|最高级|原级)\s*/, '来自$1的$2').replace(/来自(拉丁语|希腊语)?(形容词|名词|动词)\s*/, '来自$1$2');
      src = src.replace(/^[，：\s]+/, '').replace(/，\s*，/g, '，');
      segs.push(fm.k + ' ' + spoken(fm.en) + '，' + L(src) + '。' + (!fm.uses.length && fm.note ? L(fm.note) + '。' : ''));
    } else {
      const u = fm.uses.find(x => x.me) || fm.uses[0];
      segs.push('英语里，' + L(u.show) + (u.ex.length ? '，比如 ' + u.ex.slice(0, 2).join('、') : '') + '。');
    }
  });
  return { marks: true, segs };
}
function fengongScene(p) {
  const rows = p.fgRows || [], pick = p.fgSay || [];
  const isRoot = p.kind === 'root' || p.kind === 'word';
  const idt = sayAffix(say(p.idt)).replace(/[。]+$/, '');
  const sp = spokenAs(p.head || p.text, p.kind);
  // 6.2：词缀的新写法（总表“词缀身份辨析版”）：身份就是卡片上刚讲过的那句介绍，这一幕不再念一遍，直接“再来辨析一下”
  const head0 = p.bx && !isRoot ? '再来辨析一下。' : isRoot
    ? (p.base ? '词根 ' + spoken(p.base) + ' 有几种写法，身份不一样。这里的 ' + spoken(p.text) + '，是' + idt + '。' : '词根 ' + sp + ' 还有别的写法，身份不一样。这里是' + idt + '。')
    : (p.kind === 'pre' ? '前缀 ' : '后缀 ') + sp + ' 的身份：' + idt + '。';
  const lead = rows.lead ? sayAffix(say(p.bx ? String(rows.lead).replace(/…+/g, '什么') : rows.lead)) : '';
  const segs = [head0 + (lead ? (/^同样/.test(lead) ? lead + '的，有这么几个。' : lead + '。') : '')];
  // 6.4：词根的另一种写法的“字母变化”挪到这一幕（画面上标题下面那一行 duc → duce），第 2 句讲它
  if (p.varInFg) { const hs = howSay(p); segs.push(hs ? '从 ' + spoken(p.base) + ' 到 ' + spoken(p.text) + '：' + hs + '。' : spoken(p.base) + ' 在这里写成 ' + spoken(p.text) + '。'); }
  if (p.vplan) segs.push(...verbSegs(p));            // 6.5：三个样子一栏一栏讲（规律 → 英语里用这个样子的那一条），画面照 wordfilm.js 的 verbPlan 一步一步出来
  else {
    if (p.verb) segs.push(verbSay(p));               // 6.1：拉丁语动词的三个样子——只念规律，拉丁语整词画面上写着、不念
    segs.push(...pick.map(i => fgSay(p, rows[i])));
  }
  // 6.4：前缀、后缀的“辨析”那一幕，“关系”画在最下面，配音也放到最后（先“为什么用…”，再“关系”）
  if (p.bx && !isRoot && p.why) segs.push(endDot(sayAffix(say(p.why.q.replace(/\s*[\/／]\s*/g, ' 或 '))).replace(/\s*不用/, '，不用') + '？' + sayAffix(say(p.why.a))));
  // 6.3：总表辨析最后的“；关系：…”——同一种语言来的几个词缀彼此是什么关系。只念讲这个词缀的第一条；括号里的补充（拉丁语原词、例词）不念，
  // 省略号念“什么”，三个字母以内的（at、fic、ns）一个字母一个字母念
  if (p.rel && p.rel.length) segs.push('再看它们的关系：' + letters(sayAffix(say(String(p.rel[0].text).replace(/…+/g, '什么')))).replace(/[。]+$/, '') + '。');
  if (p.why && !(p.bx && !isRoot)) segs.push(endDot(sayAffix(say(p.why.q.replace(/\s*[\/／]\s*/g, ' 或 '))).replace(/\s*不用/, '，不用') + '？' + sayAffix(say(p.why.a))));
  return { marks: true, segs };
}
// 6.0：第三部分“同义词辨析”。第 1 句提出问题；每个词一句（英文放句首，后面接“这个词”念得清楚）；最后一句讲逻辑差在哪儿
function distinguishScene() {
  const D = film.dist, ws = D.items.map(x => x.w);
  // 6.43（第八十七版，用户：“同义词辨析部分直接把单词画面画出来，然后说哪个单词，哪个单词给特写就可以了”）：精简版每个词一句、只念这个词
  //   （纯英文，美式女声）；念完停 1.4 秒看特写（waits），最后缩回去一起看（hold）
  // 6.44（第八十八版，用户：“并没有说区别，我希望要简单说出区别，同时要举个例子”）：每个词先一句“X 这个词，一句话的区别”（老师的声音），
  //   有例句再念例句（纯英文，美式女声）；每个词念完停 1 秒看特写
  if (prefs.lean) {
    const segs = [], waits = {};
    D.items.forEach(it => {
      const d0 = String(it.diff || it.gloss || '').replace(/[。.，,；;]+$/, '');
      segs.push(d0 ? it.w + ' 这个词，' + d0 + '。' : it.w + '.');
      if (it.ex) segs.push(/[.!?]["”’)]?$/.test(it.ex.trim()) ? it.ex.trim() : it.ex.trim() + '.');
      waits[String(segs.length - 1)] = 1.0;
    });
    return { marks: true, segs, waits, hold: 1.2 };
  }
  const list = ws.length > 1 ? ws.slice(0, -1).join('、') + ' 和 ' + ws[ws.length - 1] : ws[0];
  const segs = [D.key ? list + '，中文都可以说' + say(D.key) + '，区别在哪儿呢？' : list + '，这几个词容易混，区别在哪儿呢？'];
  D.items.forEach(it => {
    const g = it.gloss && !String(it.note).includes(it.gloss) ? '是' + say(it.gloss) + '，' : '';
    segs.push(endDot(it.w + ' 这个词，' + (g || (/^“/.test(String(it.note)) ? '是' : '')) + say(it.note)));
  });
  if (D.logic || D.tip) segs.push(endDot((D.logic ? '它们的逻辑不一样：' : '') + say(D.logic || D.tip)));
  return { marks: true, segs };
}

// 6.11：考点（总表「考点」列）：先一句引子，再一行一句。括号里的拼写规则要念（去 e 加 d），所以先换成逗号再交给 say
// 6.12：考点只写常考的（总表“考纲考点版”）——每一条都念（用法、易混以前只念第一条）；“A → B”念成“A 变成 B”；
// sb. / sth. 念 somebody / something，… 念成停顿；只有一行时引子是“考试常考这一点。”
const KD_POS = { 'n.': '名词', 'v.': '动词', 'adj.': '形容词', 'adv.': '副词', 'pron.': '代词', 'prep.': '介词', 'conj.': '连词', 'num.': '数词', 'int.': '感叹词' };
// 6.33（第七十七版）：短语、用法、易混几条的，画面上是 ①②③，配音念“第一，……。第二，……。”（序号前面停得比句号还长，synth.py 的 sentences）；
// 一条后面带例句的（“被动 be protected by …：The birds are protected by law.”），画面上例句另起一行，配音念“例句：”再念英文（美式女声）；
// 省略号当一句话结束念（停得长），不再换成分号
const KD_NUM = '①②③④⑤⑥⑦⑧⑨';
function kdEx(it) {
  const m = /^(.*\S)\s*：\s*([A-Z][^\u3400-\u9fff：]*[.?!])\s*$/.exec(String(it));
  return m && !/[（(][^）)]*$/.test(m[1]) ? [m[1], m[2]] : [String(it), ''];
}
function kdSay(r) {
  const pos = t => String(t).replace(/(^|\s|：)(n|v|adj|adv)\.\s*/g, (m0, a, x) => a + KD_POS[x + '.'] + ' ');
  const paren = t => String(t).replace(/（([^（）]*)）/g, '，$1，').replace(/，，/g, '，');
  const en = t => String(t).replace(/\bsb\.(?=\s|$|[，；、（）()])/g, 'somebody').replace(/\bsth\.(?=\s|$|[，；、（）()])/g, 'something')
    .replace(/\s*(?:…|\.{3})+\s*/g, '⋯').replace(/\s*→\s*/g, ' 变成 ')      /* 6.33：省略号先写成 ⋯（say() 会删掉 …），kaodianScene 最后换回来 */.replace(/\s+=\s+/g, '，等于 ').replace(/\s+↔\s+/g, '，对应 ');
  if (r.label === '变形') return '变形：' + r.items.map(it => paren(pos(en(it)))).join('；');
  const conv = it => {
    if (/→/.test(it)) return paren(en(it));
    const m = /^([A-Za-z][A-Za-z'’\- ]*?)\s+(n|v|adj|adv|pron|prep|conj|num|int)\.\s*(.*)$/.exec(it);
    if (m) return m[1] + '，' + (KD_POS[m[2] + '.'] || m[2]) + '，' + m[3];
    return pos(it).replace(/^(\S+)\s+(\S+)\s+(.*)$/, '$1 $2，$3');
  };
  if (r.label === '词性转换') return '词性转换：' + r.items.map(conv).map(paren).join('；');
  const multi = r.items.length > 1;
  const body = it => r.label === '短语' ? en(it).replace(/^([A-Za-z][^\u3400-\u9fff]*?)\s*([\u3400-\u9fff].*)$/, '$1，$2') : paren(en(it));
  return (r.label === '短语' ? '常考短语：' : r.label + '：') + r.items.map((it, k) => {
    const [pt, ex] = kdEx(it);
    return (multi ? KD_NUM[k] : '') + body(pt).replace(/[。；，、\s]+$/, '') + '。' + (ex ? '例句：' + en(ex).replace(/[.?!]+$/, '') + '。' : '');
  }).join('');
}

// 6.17：拼写规则里“加”的词尾当单词念（加 -ing、加 -ly、加 -es，美式女声，词缀表）；单独的字母还是字母（去 e、加 s、双写 p，你本人的声音）
const kdAffix = t => String(t).replace(/(加|接)\s*([a-z]{2,5})(?![A-Za-z'’-])/g, '$1 -$2');
function kaodianScene(i) {                                                   // 6.31：分两页时 i 是第几页（kaodian0、kaodian1），第二页的引子是“再看这几样。”
  const multi = film.kd.pages && film.kd.pages.length > 1 && i != null;
  const rows = multi ? film.kd.pages[i].map(k => film.kd.rows[k]) : film.kd.rows;
  const intro = multi && i > 0 ? '再看这几样。' : film.kd.rows.length === 1 ? '考试常考这一点。' : '考试常考这几样。';
  return { marks: true, segs: [intro].concat(rows.map(r => endDot(kdAffix(say(kdSay(r))).replace(/，(\s*[，；])+/g, '，').replace(/，(\S)/g, '，$1').replace(/或(?=[A-Za-z])/g, '或 ').replace(/([A-Za-z])\.(?=[，；]|$)/g, '$1').replace(/，\s*：/g, '：').replace(/⋯/g, '…').replace(/…\s*[，；、]+/g, '…').replace(/[，；、]+\s*…/g, '…').replace(/…。/g, '…').replace(/。{2,}/g, '。')))) };      // 6.33：省略号挨着的逗号、分号去掉（“protect；from；，保护”那种）      // 6.31：“by …：The birds” 念成“by：The birds”
}

// 6.13：练习（一题一幕）：“第一题，听力。”+ 题目要求 → 听力念两遍（英文声音，慢一点）→ 停 wait 秒（画面倒计时）→ “答案是 B，produces。” → 解析一句。
// waits：第几句（不算 intro）念完以后多停几秒，render.py 读
const LX_CN = ['一', '二', '三', '四', '五', '六', '七'];      // 6.31：7 道题
function lianxiScene(i) {                                                    // 6.15：只出题——念题、听力念两遍，最后停 wait 秒（倒计时），答案放到视频最后
  const q = film.lx.qs[i], segs = [endDot('第' + LX_CN[i] + '题，' + (q.ask.includes(q.type) ? '' : q.type + '。') + say(q.ask))];
  if (q.listen) segs.push({ t: q.listen, speed: 0.9 }, { t: q.listen, speed: 0.9 });
  const waits = {}; if (q.wait > 0) waits[String(segs.length - 1)] = q.wait;
  return { marks: true, segs, waits };
}
// 6.15：视频最后的“答案”：“第一题，答案是 D，牛奶和鸡蛋。”+ 讲解一句（总表「答案」列）
// 6.17：讲解里的 sb. / sth. 念 somebody / something（以前这两个词配音模型念不出、整个跳过）
const enAbbr = t => String(t || '').replace(/\bsb\.(?=\s|$|[，；、。（）()])/g, 'somebody').replace(/\bsth\.(?=\s|$|[，；、。（）()])/g, 'something');
function daanScene(i) {
  const q = film.lx.qs[i], ans = Array.isArray(q.ans) ? q.ans : [q.ans];
  let a;
  if (q.opts.length) { const o = q.opts['ABCD'.indexOf(q.ans)] || ''; a = '第' + LX_CN[i] + '题，答案是 ' + q.ans + (o && o.length <= 30 ? '，' + say(o).replace(/\s*;\s*/g, '，') : '') + '。'; }
  else a = endDot('第' + LX_CN[i] + '题，答案是：' + ans.join('，').replace(/\s*→\s*/g, ' 改成 '));
  return { marks: true, segs: [a].concat(q.why ? [endDot(say(enAbbr(q.why)))] : []) };
}

const scenes = {};
const key = s => s.id + (s.i != null ? s.i : '');
// 变体：“people，是从拉丁语词根 popul 变来的；popul 的意思是：人民、民众。”（3.4 起，箭头后面是词根列里的源头词根时）；别的照旧“made，是从 maked 变来的。”
const variantLine = () => {
  const v = film.variant, from = v.from.replace(/[()]/g, '');
  if (v.root && v.root.gloss) return v.to + '，是从' + (v.root.from || '') + '词根 ' + spoken(from) + ' 变来的；' + spoken(from) + ' 的意思是：' + say(v.root.gloss) + '。';
  return v.to + '，是从 ' + from + ' 变来的。';
};
for (const s of film.scenes) {
  const k = key(s);
  if (style === 'core') {
    if (s.id === 'title') scenes[k] = { segs: [d.w + '：' + main + '。'] };          // 冒号：英文和中文之间停一下，念得清楚
    else if (s.id === 'part') scenes[k] = partScene(film.parts[s.i]);
    else if (s.id === 'yinbian') scenes[k] = yinbianScene(film.parts[s.i]);      // 6.6
    else if (s.id === 'combo') scenes[k] = { segs: [lit ? '合起来，就是' + lit + '。' : '合起来，就是 ' + d.w + '。'] };
    else if (s.id === 'route') scenes[k] = { segs: ['它的来历：' + film.route.slice(-4).map(r => spoken(r.text) + '，' + say(r.gloss)).join('；') + '。'] };
    else if (s.id === 'variant') scenes[k] = { segs: [variantLine()] };
    else if (s.id === 'related') scenes[k] = { segs: [film.related.join(' 和 ') + '，是同一个来源。'] };
    else if (s.id === 'origin') scenes[k] = { segs: ['它的来历：' + say(String(film.origin ? film.origin.text : '').split(/[。；]/)[0].replace(/([A-Za-z])\s*“/, '$1，意思是“')) + '。'] };
    else if (s.id === 'syl') scenes[k] = sylScene();
    else if (s.id === 'sylnote') scenes[k] = { marks: true, segs: (film.pron.noteKeep ? film.pron.noteKeep.map(i => (d.pron.noteSay || [])[i]).filter(Boolean) : (d.pron.noteSay || [])).slice(0, film.pron.note.length) };
    else if (s.id === 'duyin') scenes[k] = duyinScene(film.duyin[s.i]);       // 6.26：读音现象（现象一句，“为什么呢？”+ 原因一句）
    else if (s.id === 'meaning') scenes[k] = meaningScene();
    else if (s.id === 'evolve') scenes[k] = evolveScene();
    else if (s.id === 'example') scenes[k] = exampleScene(film.pics[s.i]);
    else if (s.id === 'end') scenes[k] = { segs: [d.w + '：' + main + '。'] };
    else if (s.id === 'rule') scenes[k] = ruleScene();
    else if (s.id === 'fengong') scenes[k] = fengongScene(film.parts[s.i]);
    else if (s.id === 'xingtai') scenes[k] = xingtaiScene(film.parts[s.i]);     // 6.8
    else if (s.id === 'distinguish') scenes[k] = distinguishScene();
    else if (s.id === 'kaodian') scenes[k] = kaodianScene(s.i);                 // 6.11
    else if (s.id === 'lianxi') scenes[k] = lianxiScene(s.i);               // 6.13
    else if (s.id === 'daan') scenes[k] = daanScene(s.i);                   // 6.15
    continue;
  }
  // ---------- 详细版
  if (s.id === 'title') {
    scenes[k] = { segs: [film.parts
      ? '同学们好！今天我们来学习这个单词：' + d.w + '，意思是' + main + '。它为什么是这个意思呢？我们把它拆开来看。'
      : '同学们好！今天我们来学习这个单词：' + d.w + '，意思是' + main + '。我们来看看，它是从哪儿来的。'] };
  } else if (s.id === 'split') {
    scenes[k] = { segs: [d.w + ' 可以拆成' + CN[film.parts.length] + '部分：' + film.parts.map(p => spokenAs(p.text, p.kind)).join('，') + '。'] };
  } else if (s.id === 'part') {
    scenes[k] = { segs: [partLine(film.parts[s.i]) + sameAs(film.parts[s.i].sub)] };
  } else if (s.id === 'yinbian') {
    scenes[k] = yinbianScene(film.parts[s.i]);
  } else if (s.id === 'combo') {
    const segs = film.parts.map((p, i) => { const g = glossSay(p.gloss); return (i ? '加上 ' : '') + spokenAs(p.text, p.kind) + '，' + (g.verb === '意思是：' ? '' : g.verb) + g.t + '，'; });
    segs.push(lit ? '合起来，就是：' + lit + '。' : '合起来，就是 ' + d.w + '。');
    scenes[k] = { marks: true, segs };
  } else if (s.id === 'route') {
    scenes[k] = { marks: true, intro: '再往前追一追，看看它的来历。', segs: film.route.slice(-4).map(r => spoken(r.text) + '，' + say(r.gloss) + '。') };
  } else if (s.id === 'variant') {
    scenes[k] = { segs: [variantLine() + (film.origin && film.origin.text ? say(film.origin.text) + '。' : '')] };
  } else if (s.id === 'related') {
    scenes[k] = { segs: [film.related.join(' 和 ') + '，意思和来历都有关系。' + (film.origin && film.origin.text ? say(film.origin.text) + '。' : '')] };
  } else if (s.id === 'origin') {
    scenes[k] = { segs: [d.w + ' 的来历是这样的：' + say(film.origin ? film.origin.text : '') + '。'] };
  } else if (s.id === 'steps') {
    scenes[k] = { marks: true, intro: '它的意思，是这样一步步变过来的：',
      segs: film.steps.map(st => (st.text ? say(st.text) + '，就是' + say(st.result) : say(st.result)) + '。') };
  } else if (s.id === 'meaning') {
    if (film.pics.filter(x => x.text).length >= 2) scenes[k] = meaningScene();
    else {
      let t = '所以，' + d.w + ' 现在的意思是：' + main + '。';
      if (film.meaning.second) t += '也可以指' + say(film.meaning.second) + '。';
      if (film.meaning.example && /[A-Za-z]{2,}/.test(film.meaning.example)) t += '比如：' + sayExample(film.meaning.example) + '。';
      scenes[k] = { segs: [t] };
    }
  } else if (s.id === 'rule') {
    scenes[k] = ruleScene();
  } else if (s.id === 'evolve') {
    scenes[k] = evolveScene();
  } else if (s.id === 'xingtai') {
    scenes[k] = xingtaiScene(film.parts[s.i]);
  } else if (s.id === 'fengong') {
    scenes[k] = fengongScene(film.parts[s.i]);
  } else if (s.id === 'distinguish') {
    scenes[k] = distinguishScene();
  } else if (s.id === 'kaodian') {
    scenes[k] = kaodianScene(s.i);
  } else if (s.id === 'lianxi') {
    scenes[k] = lianxiScene(s.i);
  } else if (s.id === 'daan') {
    scenes[k] = daanScene(s.i);
  } else if (s.id === 'example') {
    scenes[k] = exampleScene(film.pics[s.i]);
  } else if (s.id === 'family') {
    const fm = d.family_meanings || {};
    const pick = film.family.words.filter(w => fm[w]).slice(0, 3);
    scenes[k] = { segs: pick.length
      ? pick.map((w, i) => (i ? '还有 ' : '同一个家族的单词，还有 ') + w + ' 这个词，意思是' + say(fm[w]) + (i === pick.length - 1 ? '。' : '；'))
      : ['同一个家族的单词还有：' + film.family.words.slice(0, 4).join('，') + '。'] };
  } else if (s.id === 'board') {
    scenes[k] = { hold: 6.0, segs: [film.parts
      ? '最后，我们把重点写在小黑板上。' + d.w + '，等于 ' + film.parts.map(p => spokenAs(p.text, p.kind)).join('，加上 ') + (lit ? '，字面意思是' + lit : '') + '，也就是' + main + '。'
      : '最后，我们把重点写在小黑板上。' + d.w + '，意思是' + main + '。'] };
  } else if (s.id === 'end') {
    scenes[k] = { segs: [d.w + '，意思是' + main + '。'] };
  }
}
const old = fs.existsSync(path.join(outDir, 'plan.json')) ? JSON.parse(fs.readFileSync(path.join(outDir, 'plan.json'), 'utf8')) : {};
const plan = { word: d.w, voice: old.voice || 38, speed: old.speed || 0.95, style, scenes };
const lexicon = Object.assign({}, film.pron && d.pron && d.pron.lex ? d.pron.lex : {}, prefs.lexicon || {});
if (Object.keys(lexicon).length) plan.lexicon = lexicon;
const text = JSON.stringify(plan, null, 1);
fs.writeFileSync(path.join(outDir, 'plan.json'), text);
fs.writeFileSync(path.join(outDir, 'plan.auto.json'), text);
fs.writeFileSync(prefsPath, JSON.stringify(prefs, null, 1));

// ---------- 草稿：自动配的画、演变链、扩展词，和总表里的材料。run.py --draft-only 把一批词的拼成 edits_template.json，照着改
const strip = o => JSON.parse(JSON.stringify(o, (k, v) => (k.startsWith('_') || k === 'auto' || k === 'evoAuto' ? undefined : v)));
fs.writeFileSync(path.join(outDir, 'draft.json'), JSON.stringify({
  pics: strip(film.pics), flow: strip(film.flow || []), extend: film.extend.map(x => x.w),
  originPic: film.origin && film.origin.pic ? strip(film.origin.pic) : undefined,
  _总表: {
    今义: film.senses.map(x => (x.pos ? '（' + x.pos + '）' : '') + x.text + (x.en ? '（' + x.en + '）' : '') + (x.rare ? '［少用］' : '')),
    构词逻辑: film.steps.map(st => (st.text ? st.text + ' → ' : '') + st.result), 演变: film.evolution || '',
    辨析: ((d.fields || []).find(f => f.role === 'bianxi') || { t: '' }).t,
    同义词的材料: Object.fromEntries(Object.entries(d.syn || {}).slice(0, 6).map(([w, x]) => [w, [x.meaning, x.split, x.logic1].filter(Boolean).join(' | ')])),
    扩展词候选: (d.extend || []).map(x => x.w + ' ' + x.m)
  }
}, null, 1));
// 还要补什么（每个词都要做到的，见 SKILL.md 的“用户定下的规矩”）
const todo = [];
if (film.lx && !film.lx.manual) todo.push('练习题 lianxi（现在是按总表自动起草的草稿，照 SKILL.md 规矩 41、59 手写 7 道：第 1 题听力念含本词的短句，其余考考点、题型尽量不重复，第 6、7 题专门考考点）');
if (!film.kd) todo.push('考点（6.31 起精简版固定要有这一部分：总表「考点」列这个词是空的，先在总表补上，或者在画面设置里写 kaodian.rows）');      // 6.13
film.pics.forEach((x, i) => {
  const tag = '第' + (i + 1) + '个意思“' + x.text + '”';
  if (x.auto) todo.push(tag + '画成一幅有背景、会动的画');
  if (!x.pos) todo.push(tag + '的词性 pos');
  if (!x.ex) todo.push(tag + '的例句 ex、exzh');
  else if (!x.exPic) todo.push(tag + '的例句动画 exPic');
});
if (!prefs.flow) todo.push('演变链 flow（现在是按总表自动拼的）');
// 6.0：第三部分“同义词辨析”。表里有同义词组、却拼不出这一部分（辨析的话没讲这几个词的区别）的，要手写；拼出来的，每个词配一幅画
{
  const bx = (d.fields || []).find(f => f.role === 'bianxi');
  const syn = bx ? String(bx.t).split('\n').filter(x => x.startsWith('【同义词】')) : [];
  if (film.dist) {
    film.dist.items.forEach(it => { if (!it.pic) todo.push('同义词辨析：' + it.w + ' 那张卡配一幅画（prefs.distinguish.pics 里写 "' + it.w + '": 画）'); if (!it.note) todo.push('同义词辨析：' + it.w + ' 的区别还没有话（prefs.distinguish.items 手写）'); });
    film.dist.items.forEach(it => { if (!it.ex) todo.push('同义词辨析：' + it.w + ' 还没有例句（prefs.distinguish.items 里给这个词写 ex：一句用到它的简单英文例句，exZh：例句的中文；精简版视频里要念）'); });      // 6.44
    if (!film.dist.logic && !film.dist.tip) todo.push('同义词辨析：最后一句“逻辑不同 / 一句话记法”（prefs.distinguish.logic 或 tip；总表辨析列可以加一行“逻辑不同：…”）');
  } else if (syn.length && prefs.distinguish !== false) {
    todo.push('同义词辨析：总表有同义词组（' + syn[0].replace('【同义词】', '') + '），辨析的话却没讲它们的区别——在 prefs.distinguish 里手写 key、items（每个词的 gloss、note），或者写 "distinguish": false 不要这一部分');
  }
}
// 5.0 起：画面检查。用户要的是“讲什么就画什么”：主角放大特写、不用表情人头、每一步都有对得上的示意图
const FACE = cp => (cp >= 0x1F600 && cp <= 0x1F64F) || (cp >= 0x1F910 && cp <= 0x1F92F) || (cp >= 0x1F970 && cp <= 0x1F97A) || cp === 0x1F9D0 ||
  [0x1F466, 0x1F467, 0x1F468, 0x1F469, 0x1F474, 0x1F475, 0x1F476, 0x1F9D1, 0x1F9D2, 0x1F9D3, 0x1F9D4, 0x1F471, 0x1F472, 0x1F473, 0x1F477, 0x1F478,
    0x1F482, 0x1F46E, 0x1F470, 0x1F935, 0x1F934, 0x1F9D5, 0x1F936, 0x1F385, 0x1F481, 0x1F486, 0x1F487, 0x1F926, 0x1F937].includes(cp) || (cp >= 0x1F9D9 && cp <= 0x1F9DD);
const picChecks = (pc, tag) => {
  if (!pc) return;
  const heads = (pc.items || []).filter(it => it.e && FACE(it.e.codePointAt(0))).map(it => it.e);
  if (heads.length) todo.push(tag + '用了表情人头 ' + heads.join('') + '：不要单独一个头，画实际的东西（svg 插图），要人就用全身的人（🚶🧍🏃）');
  const big = Math.max(0, ...(pc.items || []).filter(it => it.e || it.svg || it.img).map(it => Math.max(Number(it.s) || 0.34, Number(it.s2) || 0)));
  if (!pc.img && big < 0.45) todo.push(tag + '主角太小（最大的才占画高 ' + Math.round(big * 100) + '%）：讲的那样东西要放大特写，占画面一半以上');
  // 6.20（用户：“要接近真实的样子，不要太抽象，不要只画一个人头，一个摆件这样的；要尽量体现出现实生活中的样子”）：
  //   ① 画里不再用表情图（3D 表情只是图标，不像真东西）；② 每幅画是一个生活场景：铺一张场景背景（img：屋里、教室、舞台、车站…），
  //   再放用它的人、它旁边的东西。整幅示意图（一张 svg 铺满，s ≥ 0.95）和写了 "diagram": true 的不查第 ②条
  const emo = (pc.items || []).filter(it => it.e && !FACE(it.e.codePointAt(0))).map(it => it.e);
  if (emo.length) todo.push(tag + '还有表情图 ' + emo.join('') + '：6.20 起换成写实插图（references/scenes/ 里的东西、scripts/people.py 的人物，或者自己画 svg）');
  const things = (pc.items || []).filter(it => it.e || it.svg || it.img);
  const fullDiagram = pc.diagram || things.some(it => (Number(it.s) || 0) >= 0.95 && !/audience|desk|loudspeaker/.test(String(it.svg || '')));
  // 6.21（用户：“周围环境还需要再加强一下，比如说车站，车站画的不是很详细，很具体……其他单词，不同的环境都一样”）：
  //   场景背景（整幅铺的 img，或者当背景放的大图：s ≥ 0.95、z < 0）要画得详细、具体——数一数这张 svg 里有多少个图形，不到 150 个的列出来
  const bgFiles = [pc.img].concat((pc.items || []).filter(it => it.svg && (Number(it.s) || 0) >= 0.95 && (Number(it.z) || 0) < 0).map(it => it.svg)).filter(f => f && /\.svg$/i.test(String(f)));
  bgFiles.forEach(f => {
    let n = -1;
    try { const t = fs.readFileSync(path.isAbsolute(f) ? f : path.join(outDir, f), 'utf8'); n = (t.match(/<(path|rect|circle|ellipse|line|polygon|polyline|text)\b/g) || []).length; } catch (e) { n = -1; }
    // 6.22：场景要换成图画书画风（黑色勾线）：墨线不到 60 处的，多半还是写实的原图
    if (n >= 150) {
      let ink = 0;
      try { ink = (fs.readFileSync(path.isAbsolute(f) ? f : path.join(outDir, f), 'utf8').match(/stroke="#(1B1A1F|2E2318)"/g) || []).length; } catch (e) { ink = 0; }   // 6.29：青绿工笔风的墨线是暖墨色 #2E2318（scripts/styles.py）
      if (ink < 60) todo.push(tag + '的场景背景 ' + f + ' 还是写实画法（没有黑色勾线）：6.22 起换成图画书画风——python3 scripts/bookstyle.py stylize 原图.svg art/' + path.basename(String(f)) + ' --bg');
    }
    if (n >= 0 && n < 150) todo.push(tag + '的场景背景 ' + f + ' 画得太简单（只有 ' + n + ' 个图形）：6.21 起场景要详细、具体，这个地方真有的东西都画上（pictures.md 第十五节“场景要详细、具体”的清单），不少于 150 个图形');
  });
  if (!pc.img && !fullDiagram && things.length < 3) todo.push(tag + '只有' + (things.length ? things.length + '样东西' : '字') + '、没有场景：6.20 起画成生活里的样子——img 铺一张场景背景（references/scenes/），再画出谁在用它、它在做什么（pictures.md 第十五节）');
  motionChecks(pc, tag);
};
// 6.25（规矩 51，用户：“我希望图片里面要有适当的动图……总之要是动态的图；这里不是只改 speaker 一个，其他的单词也要做这样的优化”
//   “如果多人同台，或者做事，要增加一些互动，就是人和人，人和物，物和物这些之间有的时候可以增加一些互动，要根据内容来进行”）：
//   ① 每幅画都要有会动的东西；② 画里的人都要动（说话的 seq talk、听的 seq blink…）；③ 会出声的东西要有声波 / 音符；
//   ④ 两个人以上同框要有互动（turn 轮流说、nodWith 点头、with 人说话喇叭才响）；⑤ 车站、街上这种地方要有走动的人（walk）
function motionChecks(pc, tag) {
  if (!pc) return;
  const its = pc.items || [];
  const moving = its.some(it => (Array.isArray(it.frames) && it.frames.length > 1) || it.walk || it.waves || it.emit || it.eq || it.beam || it.crowd || it.go || it.path || (it.anim && it.anim !== 'none') || it.blink);
  if (its.length && !moving) todo.push(tag + '整幅画都是静止的：6.25 起每幅画都要动起来——说话的人动嘴、比划，音箱、喇叭出声波 / 音符（waves、emit），路上有人走（walk），台下听众点头（crowd）（规矩 51，pictures.md 第十八节）');
  const people = its.filter(it => /(^|\/)(cn|west)-[a-z]+-[a-z]+/.test(String(it.svg || '')));
  const still = people.filter(it => !(Array.isArray(it.frames) && it.frames.length > 1));
  if (still.length) todo.push(tag + '里有 ' + still.length + ' 个人是静止的（' + still.map(it => path.basename(String(it.svg))).join('、') + '）：6.25 起人都要动——说话的 seq talk（嘴一张一合、手比划），听的 seq blink（歪头、眨眼），python3 scripts/poses.py art --motion 生成');
  const sounders = its.filter(it => /(speaker|loudspeaker|radio|horn|bell|alarm|tv|phone)/i.test(path.basename(String(it.svg || ''))) && !/icon/.test(String(it.svg || '')));
  if (sounders.length && !its.some(it => it.waves || it.emit)) todo.push(tag + '里有会出声的东西（' + sounders.map(it => path.basename(String(it.svg))).join('、') + '），却没有声波、音符：6.25 起加 waves（一圈圈声波）或 emit（飘出来的音符）');
  if (people.length >= 2 && !its.some(it => Array.isArray(it.turn) || it.nodWith != null || it.with != null)) todo.push(tag + '有 ' + people.length + ' 个人同框却没有互动：6.25 起按内容加——两个人对话写 turn 轮流说，听的人 nodWith 说话的人（说完一句就点头），声波、音符 with 说话的人（人说话喇叭才响）（规矩 51）');
  const bgs = [pc.img].concat(its.filter(it => (Number(it.s) || 0) >= 0.95 && (Number(it.z) || 0) < 0).map(it => it.svg));
  if (bgs.some(f => /(station|street|park|market|square|mall|airport|platform)/i.test(String(f || ''))) && !its.some(it => it.walk)) todo.push(tag + '是车站、街上这种人来人往的地方，却没有走动的人：6.25 起加 walk（poses.py 的 walk-… 走路的人，中外都有）');
}
if (film.dist && Array.isArray(film.dist.items)) film.dist.items.forEach(it => { if (it.pic) motionChecks(it.pic, '同义词辨析 ' + it.w + ' 那张卡的画'); });
film.pics.forEach((x, i) => { picChecks(x, '第' + (i + 1) + '个意思的画'); picChecks(x.exPic, '第' + (i + 1) + '个例句的动画'); });
if (film.origin && film.scenes.some(x => x.id === 'origin')) {         // 只有放来历卡片的词（基础词）才要
  if (!film.origin.pic && !film.origin.icon) todo.push('来历要配一幅画 originPic：画的就是来历里说的那样东西（' + String(film.origin.text).slice(0, 24) + '…）');
  picChecks(film.origin.pic, '来历的画');
}
// 6.20：每部分卡片、拼起来那一格也要生活场景和写实的小图标（自动配的小动画、小图标都是表情）
(film.parts || []).forEach((pt, k) => {
  if (!pt.pic) todo.push('第 ' + (k + 1) + ' 部分（' + pt.text + '）的卡片还是自动配的表情小动画：6.20 起在 partPics.p' + k + ' 画一幅生活里的场景（这一部分的意思正在发生）');
  else picChecks(pt.pic, '第 ' + (k + 1) + ' 部分卡片的画');
  if (!pt.iconSet || !/\.(svg|png|jpe?g|webp)$/i.test(String(pt.icon || ''))) todo.push('拼起来那一格里 ' + pt.text + ' 的小图标还是表情：6.20 起在 icons.p' + k + ' 写自己画的正方形小图（"art/icon-xxx.svg"）');
});
if (film.combo && film.combo.pic) picChecks(film.combo.pic, '拼起来那一格的画');
// 6.22（用户：“人物，环境，建筑，物件这些要中国和欧美相结合，不要全是中国人，也不要全是外国人”）：
//   人物用 bookstyle.py 生成的图画书画风人物，文件名前缀 cn- / west-；一个词的画里两种人都要有。写实的旧人物（teacher-talk.svg、person-*.svg…）列出来换掉
{
  const allPics = [];
  film.pics.forEach(x => { allPics.push(x); if (x.exPic) allPics.push(x.exPic); });
  (film.flow || []).forEach(st => { if (st.fig) allPics.push(st.fig); });
  (film.parts || []).forEach(pt => { if (pt.pic) allPics.push(pt.pic); });
  if (film.combo && film.combo.pic) allPics.push(film.combo.pic);
  const names = [];
  allPics.forEach(pc => (pc.items || []).forEach(it => { if (it.svg) names.push(path.basename(String(it.svg))); }));
  const cn = names.some(n => /^cn-/.test(n)), west = names.some(n => /^west-/.test(n));
  const oldPeople = [...new Set(names.filter(n => /^(teacher|girl|woman|clerk|person)-?[a-z-]*\.svg$/.test(n) || n === 'clerk.svg'))];
  if (oldPeople.length) todo.push('画里还有写实画法的旧人物 ' + oldPeople.join('、') + '：6.22 起换成图画书画风人物（python3 scripts/bookstyle.py people art/，文件名 cn-… / west-…）');
  // 6.24（用户：“人物的动作，表情很单一，几个画面都是一样，姿势，手势都一样，我希望表情，动作，姿势不同画面，场景要做适当切换”）：
  //   同一张人物图（同一个动作、表情）用在 3 幅以上的画里，列出来换；一个人物都没做成动图的，提醒做几帧
  {
    const cnt = {};
    allPics.forEach(pc => { const seen = new Set(); (pc.items || []).forEach(it => { if (it.svg) { const nm = path.basename(String(it.svg)).replace(/_[fmw]\d+\.svg$/, '.svg'); if (/^(cn|west)-/.test(nm) && !seen.has(nm)) { seen.add(nm); cnt[nm] = (cnt[nm] || 0) + 1; } } }); });
    const rep = Object.keys(cnt).filter(k => cnt[k] >= 3);
    if (rep.length) todo.push('同一个动作、表情用了好几次：' + rep.map(k => k + ' ×' + cnt[k]).join('、') + '：6.24 起每幅画的人物换一个动作和表情（scripts/poses.py 的 ACTIONS，规矩 50）');
    const anyPeople = Object.keys(cnt).length > 0;
    const anyAnim = allPics.some(pc => (pc.items || []).some(it => Array.isArray(it.frames) && it.frames.length > 1));
    if (anyPeople && !anyAnim) todo.push('人物都是静止的：6.24 起说话、挥手、听音乐的人做成动图（"frames": [几帧], "fps": 3，规矩 50）');
  }
  // 6.28：不是每幅画都要有人（用户：“不是每个画面都需要有人在里面，要根据当时讲解的内容来定，如果不需要人，就可以不放人在里面”）——
  //   整个词只出现一两个人时，不要求中外都有；三个以上不同的人，才要中外结合
  const pplKinds = new Set(names.filter(n => /^(cn|west)-/.test(n)).map(n => n.replace(/_[fmw]\d+\.svg$/, '').replace(/\.svg$/, '')));
  if (pplKinds.size >= 3 && (cn || west) && !(cn && west)) todo.push('人物只有' + (cn ? '中国人' : '欧美人') + '：6.22 起要中外结合——这个词的画里中国人（cn-…）和欧美人（west-…）都要有（规矩 48）');
}
// 6.28（规矩 56）、6.34（规矩 67）：音效——按内容需要放、不规定个数（用户：“按需求来进行，不需要有规定的数量”），配在最能加深印象的地方（讲到车有车声、讲演讲有一句演讲、音箱放一小段音乐、猫叫一声……），不要每幅画都响
{
  const sp = [];
  film.pics.forEach(x => { if (x.exPic) sp.push(x.exPic); });
  (film.flow || []).forEach(st => { if (st.fig) sp.push(st.fig); });
  (film.parts || []).forEach(pt => { if (pt.pic) sp.push(pt.pic); });
  if (film.combo && film.combo.pic) sp.push(film.combo.pic);
  if (film.origin && film.origin.pic) sp.push(film.origin.pic);
  const snd = [];
  sp.forEach(pc => (pc.items || []).forEach(it => { if (it.sound || it.sfx) snd.push(String(it.sound || it.sfx)); }));
  // 6.34：不再因为个数（没有、超过 8 个）列“还要补”
  if (snd.length) console.log('  音效：' + snd.join('、'));
}
(film.flow || []).forEach((st, k) => {
  if (k && !st.fig && st.pic == null) todo.push('演变第 ' + k + ' 步“' + st.node + '”没有示意图 fig：讲这一步时右边画板要演这一步说的事');
  picChecks(st.fig, '演变第 ' + k + ' 步的示意图');
});
// 5.11：讲的和画的要一句一句对得上（用户：“讲解的文字要和图片能完美匹配上”）。起草时自动查三样：
//   1. 一步讲了几句的，每一句说的时候画面上都要有新出来（或动起来）的东西——不然这一句学生只能干听；
//   2. 写了 when 的东西，那个词必须真的在这一步的配音里（不然出来的时间对不上）；
//   3. 示意图上的标签，写的应该是配音里说到的词（标签是给“正在说的东西”起名字的）。
const cjk2 = t => { const z = String(t || '').replace(/[^\u3400-\u9fff]/g, ''), out = []; for (let i = 0; i + 1 < z.length; i++) out.push(z.slice(i, i + 2)); return out; };
const enWords = t => (String(t || '').match(/[A-Za-z]{3,}/g) || []).map(x => x.toLowerCase());
const mentioned = (label, said) => { const lo = said.toLowerCase(); const c = cjk2(label), e = enWords(label); return (!c.length && !e.length) || c.some(x => said.includes(x)) || e.some(x => lo.includes(x)) || (String(label).replace(/[^\u3400-\u9fff]/g, '').length === 1 && said.includes(String(label).replace(/[^\u3400-\u9fff]/g, ''))); };
const matchCheck = (pc, sents, extra, tag, noCover) => {
  if (!pc || !Array.isArray(pc.items)) return;
  const S = sents.map(String), all = S.join('') + (extra || '');
  const cueOf = it => (it.cue != null ? Number(it.cue) : it.when != null ? Math.max(0, S.findIndex(x => x.includes(String(it.when)))) : null);
  if (S.length >= 2 && !noCover) S.forEach((sn, j) => {
    const has = pc.items.some(it => cueOf(it) === j || (it.goCue != null && Number(it.goCue) === j) || (it.growCue != null && Number(it.growCue) === j) || (it.hideCue != null && Number(it.hideCue) === j) ||
      [it.goWhen, it.growWhen, it.hideWhen].some(w => w != null && sn.includes(String(w))) || (j === 0 && cueOf(it) == null));
    if (!has) todo.push(tag + '：第 ' + (j + 1) + ' 句“' + sn.slice(0, 16) + (sn.length > 16 ? '…' : '') + '”说的时候画面上没有新出来的东西（给这一句说的东西写 cue: ' + j + '，或 when: "这一句里的词"）');
  });
  pc.items.forEach(it => {
    for (const key of ['when', 'goWhen', 'growWhen', 'hideWhen']) if (it[key] != null && !S.some(x => x.includes(String(it[key])))) todo.push(tag + '：写了 ' + key + '“' + it[key] + '”，可是配音里没有这几个字，出来的时间会对不上');
    if (it.label != null && !it.e && !it.svg && !it.img && !it.shape && !mentioned(it.label, all)) todo.push(tag + '：标签“' + it.label + '”配音里没有说到（标签要写配音里说的词，或者把这样东西讲出来）');
  });
};
(film.flow || []).forEach((st, k) => { if (k && st.fig) matchCheck(st.fig, [].concat(st.sayList || st.say || []), (st.node || '') + (st.via || '') + (st.cap || '') + (st.rule || '') + (st.ruleEx || ''), '演变第 ' + k + ' 步的示意图'); });
film.pics.forEach((x, i) => { if (x.exPic) matchCheck(x.exPic, [x.ex || '', x.exzh || ''], x.text || '', '第' + (i + 1) + '个例句的动画'); });
(film.parts || []).forEach((pt, i) => {
  if (pt.memo && !pt.pic && (pt.kind === 'root' || pt.kind === 'word')) todo.push('第 ' + (i + 1) + ' 部分“' + pt.text + '”有记法（' + pt.memo.text + '）：卡片左边画记法里说的东西（prefs.partPics.p' + i + '），不要只用自动配的小图标');
  if (pt.pic) { picChecks(pt.pic, '第 ' + (i + 1) + ' 部分卡片的画'); matchCheck(pt.pic, partSegs(pt), pt.gloss || '', '第 ' + (i + 1) + ' 部分卡片的画', true); }   // 卡片右边自己会按句出字母变化、记框，左边的画不用每句都有新东西
});
// 5.2 起：配音说到某个时代、某种身份的人（古罗马的猎人、古代的画家、士兵），画里的人就要画成那样的人（穿着、发型、拿的东西），
// 不能用现代人的表情（用户看 explore：说的是古罗马猎人，画的却是穿 T 恤的现代人）
const ERA = /古罗马|古希腊|罗马人|希腊人|古埃及|古代|古人|中世纪|原始人|骑士|国王|王后|皇帝|士兵|猎人|农夫|农民|牧人|渔夫|水手|商人|僧侣|修士|画家|工匠|武士|\b(?:Roman|Greek|ancient|knights?|soldiers?|hunters?|farmers?|kings?|queens?)\b/i;   // 6.10：英文要整词（以前 talking 里的 king 也算）
const MODERN_PEOPLE = ['🧍', '🚶', '🏃', '🧍‍♀️', '🧍‍♂️', '🚶‍♀️', '🚶‍♂️', '🏃‍♀️', '🏃‍♂️', '🧎', '🧑', '👩', '👨', '🙋', '💁', '🤷'];
const eraCheck = (pc, said, tag) => {
  if (!pc) return;
  const m = ERA.exec(said || '');
  const used = (pc.items || []).filter(it => it.e && MODERN_PEOPLE.includes(it.e)).map(it => it.e);
  if (m && used.length) todo.push(tag + '讲的是“' + m[0] + '”，画里的人却是现代人的表情 ' + used.join('') + '：要画成那个时代、那种身份的人（svg：衣服、发型、拿的东西对得上，见 pictures.md 第十一节；现成的角色在 references/characters/）');
};
(film.flow || []).forEach((st, k) => { if (k) eraCheck(st.fig, [].concat(st.sayList || st.say || []).join('') + (st.via || '') + (st.node || ''), '演变第 ' + k + ' 步的示意图'); });
film.pics.forEach((x, i) => eraCheck(x.exPic, (x.ex || '') + (x.exzh || ''), '第' + (i + 1) + '个例句的动画'));
if (film.pron && !film.pron.ok) todo.push('读音拆分对不齐，现在只念整词：要一块一块念，在 prefs 写 sylIpa（每一块的音标）');
if (new Set(film.pics.map(x => x.pos).filter(Boolean)).size > 1 && !film.rules.length) todo.push('词性变了：flow 里转变的那一步要写英语的用词规律 rule、ruleEx（会写上小黑板当重点）');

// ---------- 给润色的人看：配音稿、画面要补的东西
console.log('起草好了 ' + d.w + '（' + (style === 'core' ? '只讲核心' : '详细版') + '，' + Object.keys(scenes).length + ' 幕）：' + path.join(outDir, 'plan.json'));
for (const [k, v] of Object.entries(scenes)) console.log('  ' + k.padEnd(9) + (v.intro ? '[' + v.intro + '] ' : '') + v.segs.map(x => (typeof x === 'string' ? x : x.t)).join(' ｜ '));
if (film.parts) console.log('  部分：' + film.parts.map(p => (p.head || p.text) + '（' + ({ pre: '前缀', suf: '后缀', root: '词根', word: '单词' })[p.kind] + (p.from ? '，' + p.from : '，来源没写') + (p.tag ? '，' + p.tag : '') + '）').join('  '));
if (film.pron) console.log('  读音拆分：' + film.pron.chunks.map(c => c.t + (c.ipa ? ' /' + c.ipa + '/' : '')).join(' + ') + (film.pron.ipa ? ' → /' + film.pron.ipa + '/' : '') +
  (film.pron.stress >= 0 && film.pron.read.length > 1 ? '，重音在 ' + film.pron.chunks[film.pron.stress].t : '') + (film.pron.ok ? '' : '［对不齐，只念整词］') + (film.pron.note.length ? '；关键解释 ' + film.pron.note.length + ' 条' : ''));
else console.log('  读音拆分：没有（音节表里没有这个词，或者没给音节表）');
console.log('  今义：' + (film.senses.map(x => x.text + (x.en ? '（' + x.en + '）' : '') + (x.rare ? '［少用］' : '')).join(' ｜ ') || '（没有）'));
const auto = !film.pics.length || film.pics.every(x => x.auto);
console.log('  画：' + (auto ? '还是自动配的单个图标，要在 prefs.json 的 pics 里画成一幅画，写上词性、区别、例句和例句的动画（见 references/pictures.md）'
  : film.pics.map(x => x.text + '［' + x.bg + '：' + x.items.map(i => i.e).join('') + '］' + (x.pos ? x.pos : '') + (x.diff ? '，' + x.diff : '')).join(' ｜ ')));
console.log('  总表里意思怎么变：' + (film.steps.map(st => (st.text ? st.text + ' → ' : '') + st.result).join(' ｜ ') || '（没写）') + (film.evolution ? '；【演变】' + film.evolution.replace(/\s+/g, ' ') : ''));
console.log('  每个意思怎么来：' + (film.pics.map(x => x.text + '：' + (x.evoSay ? x.evoSay : x.evo.length ? x.evo.join(' → ') + (x.evoAuto ? '［按总表自动配，要看对不对］' : '') : '（没有，要在 pics 里写 evo / evoSay）')).join(' ｜ ') || '（没有）'));
console.log('  演变那一幕：' + (film.flow ? film.flow.map((s, k) => (k ? '→' + (s.via ? '（' + s.via + '）' : '') : '') + s.node + (s.pos ? '［' + s.pos + '］' : '')).join(' ') + (prefs.flow ? '' : '［自动拼的，要照总表把转变的道理写清楚，见 references/narration-guide.md 第四节］') : '（没有：pics 里没写 evo，也没写 flow）'));
console.log('  用词规律（小黑板重点）：' + (film.rules.map(r => r.text + (r.ex ? '（' + r.ex + '）' : '')).join(' ｜ ') || '（没有）'));
// 6.1：总结分没分页、“身份和分工”里有没有三个样子，起草时说一声
if (film.board) console.log('  总结：' + (film.board.pages === 2
  ? '两页（内容多，一页放不下）——第一页 ' + film.board.lines.length + ' 行字，第二页 ' + film.board.cards2.length + ' 个意思各一行（画、意思、例句、中文）；想硬性放一页写 "board": {"pages": 1}'
  : '一页（' + film.board.lines.length + ' 行字' + (film.board.cards.length ? '，下面 ' + film.board.cards.length + ' 张例句卡' : '，还没有例句，先不贴卡片') + '）'));
(film.parts || []).forEach((pt, i) => { if (pt.verb) console.log('  三个样子（第 ' + (i + 1) + ' 部分 ' + pt.text + '）：' + pt.verb.forms.map(x => x.k + ' ' + x.la + '“' + x.zh + '”').join(' → ') + '；规律：' + pt.verb.rule + (pt.verbAt ? '［这一部分用的是' + (pt.verbAt === 'pp' ? '过去分词' : '原形') + '］' : '［这一部分不对着哪一个样子］')); });
// 6.7：辨析每个用法的演示：没配画的（只有自动配的小图标）列出来，在 prefs.demo 里配（references/pictures.md 第十四节）
{
  const dw = [];
  (film.parts || []).forEach(pt => { if (!pt.bx) return; (pt.fgSay || []).forEach(i => (((pt.fgRows || [])[i] || {}).uses || []).slice(0, 2).forEach(u => { if (u.demo && !u.demo.pic && !dw.includes(u.demo.w)) dw.push(u.demo.w); })); });
  if (dw.length) todo.push('辨析的演示配画（现在是自动的小图标）：' + dw.join('、'));
  const shown = [];
  (film.parts || []).forEach(pt => { if (!pt.bx) return; (pt.fgSay || []).forEach(i => (((pt.fgRows || [])[i] || {}).uses || []).slice(0, 2).forEach(u => { if (u.demo) shown.push((u.tag ? '加在' + u.tag + '：' : '') + u.demo.terms.map(t => t.t + '（' + t.g + '）').join(' + ') + ' =“' + u.demo.lit + '” ' + u.demo.w); })); });
  if (shown.length) console.log('  辨析的演示：' + shown.join(' ｜ '));
}
// 6.57（第一百零一版）：每一条“还要补”前面标上它属于视频的哪一块（单词工作台按块分到「含义拆分」的小类、「同义词辨析」……只退回那一块）
const BLOCK_OF = [['同义词辨析', /同义词辨析|辨析/], ['读音拆分', /读音|音标|sylIpa/], ['意思演变', /意思怎么|演变|flow/], ['例句动画', /例句/],
  ['拼起来', /拼起来|comboPic|合起来/], ['词根词缀卡', /词缀|词根|partPics|图标|icons|卡片/], ['意思场景', /意思的画|场景|背景|pics|画得太简单/],
  ['考点', /考点/], ['总结小黑板', /小黑板|扩展/], ['练习题', /练习|题目/]];
const tagged = todo.map(t => /^【[^】]+】/.test(t) ? t : (b => b ? '【' + b + '】' + t : t)((BLOCK_OF.find(([, re]) => re.test(t)) || [])[0]));
console.log('  还要补：' + (tagged.join('；') || '都齐了'));
console.log('  例句：' + (film.pics.filter(x => x.ex).map(x => x.ex + (x.exzh ? ' ' + x.exzh : '') + (x.exPic ? '［有动画］' : '［用上面那幅画］')).join(' ｜ ') || '（没有，要在 pics 里写 ex、exzh）'));
console.log('  扩展词（小黑板）：' + (film.extend.map(x => x.w + ' ' + x.m).join(' · ') || '（没有）') +
  ((d.extend || []).filter(x => !x.pick).length ? '；候选还有：' + d.extend.filter(x => !x.pick).slice(0, 8).map(x => x.w).join('、') : ''));
