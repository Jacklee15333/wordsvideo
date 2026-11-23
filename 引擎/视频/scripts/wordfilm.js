// 6.33.0（第七十七版）：精简版读音现象只讲现象、不讲原因；考点的短语、用法、易混用 ①②③ 编号，带例句的一条例句另起一行（“例：…”）。
/* 构词动画（6.32.0，第七十六版：「初中含义」列定讲哪几个意思；考点写“protection n.保护”；配音的停顿按标点分长短、换得快的一句一个声音念。之前 6.16.0，第五十三版：练习挪到总结后面、答案前面：…… → 四、考点 → 五、总结 → 六、练习 → 七、答案（“视频里把练习部分放在最后，答案的前面；就是把单词的一套全部讲解完了，再最后做练习”）；
   念单词、句子的时候不画小喇叭（读音拆分念到的那一块、连起来念整词、听力题都不画；“读单词，句子的时候，喇叭不要出现，有点多余”）；
   6.7.0：分段标题下面不画线；“辨析”那一幕每个用法一个小演示“图 + 图 = 画”（演示词是总表辨析里那个用法括号的第一个例词，等式取它自己那一行），
   “名词前 / 动词词根前”的牌子标出加在什么词前面；配合总表“辨析精简演示版”（辨析、关系写简短，例词紧跟在各自的用法后面）；
   6.6.0：音变的原因单独一幕“为什么 p 会变成 f？”（格林定律三对、两块会动的嘴的剖面图讲两个音发音相近、起因、例子）；身份框“表示“向前”和“预先””，“在这个词里”单独一行醒目；
   6.5.0：分段标题带编号（一、读音拆分）；前缀、后缀特写——意思和这一部分写在一行、“前缀”牌子在右上角、不写“来自…”牌子、身份框写“来自…；表示…；也可以表示…”，
   图下面不再写 pro ≈ for / duc ∽ duck；记框里音变下面一行“原因”（总表“；原因：…”，配音单独一句）；词根的字母变化放回特写卡片；
   三个样子和分工合成一幕、一栏一栏画：框里词根字母上色、变了的字母绿色、词尾灰色，规律紧贴在各自的框下面，英语里用这个样子的那一条接在下面；
   6.4.0：画面清爽版——开头只有单词和含义；分段标题只写标题；每一幕左上角的“单词 + 这一幕讲什么”、右上角的牌子不画；
   拆开以后只写“拆成 2 部分”；讲每一部分时上面那一行缩小放在左上角、卡片放大成特写，前缀、后缀的“身份”写在卡片上；
   “辨析”那一幕只讲辨析（标题“辨析”、几个词缀的对比、最下面“关系”）；词根的“字母变化”挪到“身份和分工”那一幕；
   配合总表“专业术语版”（“老祖宗”换成“原始印欧语…”，读法没变）；
   6.3.0：配合总表“词缀关系版”——辨析最后多一段“；关系：…”（同一种语言来的几个词缀彼此是什么关系：-ant / -ent 是同一个现在分词词尾的两种写法，
   pre- / pro- 不是谁变出谁、是一对兄弟），画在“前缀辨析 / 后缀辨析”那一幕下面的“关系”框里，配音多一句“再看它们的关系：…”；
   读音拆分里元辅e 的关键解释（u_e、a_e…）写成规则的名字“元辅e结尾（uce）”；
   6.2.0：配合总表“词缀身份辨析版”——前缀、后缀那一行写成“标签：身份：开头的介绍；记：…。辨析：…”：开头的介绍就是身份，
   “分工”改叫“辨析”、挪到这一行最后；词缀那一幕改叫“前缀辨析 / 后缀辨析”，三条以内的都讲；上一版“…；身份：…。分工：…；记：…”的表照旧能读；
   6.1.0：“身份和分工”那一幕写出拉丁语动词的三个样子——原形、过去式、过去分词——和变化规律；总结放不下就分两页；
   6.0.0：视频分四部分——读音拆分、含义拆分、同义词辨析、总结；词根的几种写法、意思相近的词缀讲“身份和分工”；
   5.1.0：拆开了也不好懂的部分讲“记法”（stat ≈ stand），出来 / 进去等方向动画画清楚；5.0.0：开头加“一、读音拆分”，画面要和讲的内容对得上）
   按词源库里的“拆分、各部分解释、组合 → 现在的含义（构词逻辑、今义）、同一词族”，画一段二三十秒的动画（1280×720）：
     ① 单词出现 → ② 字母分开，按部分上色 → ③ 每个部分一张卡片：图 + 意思，图会动（trans- 越过一条线、ex- 从盒子里出来、un- 被划掉…）
     → ④ 拼起来：trans（到另一边）+ port（搬运）=“搬到另一边” → ⑤ 意思一步步变过来（构词逻辑里“→”的几行）
     → ⑥ 现在的意思 → ⑦ 同一词族（共同的部分标出来）→ ⑧ 一句话总结。
   变体（made ← maked、Wed. ← Wed(nesday)）：字母怎么增减，一个个动给你看；同源（match ≈ make）：两个词并排；
   基础词（make）：讲来历，再讲意思怎么变过来。
   每一帧只由“第几秒”决定（draw(ctx, film, t)），所以能拖进度条，也能一边播一边录成视频。
   图用表情符号（Windows 自带的彩色表情字体），按词根、意思里的关键词自动配；配得不好的，可以在播放器里换，换了会记住。 */
(function (root) {
  'use strict';
  const W = 1280, H = 720;
  const EN = 'Cambria, Georgia, "Noto Serif", "Times New Roman", serif';
  const ZH = '"Microsoft YaHei UI", "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", "Noto Sans SC", "Source Han Sans SC", sans-serif';
  const EMOJI = '"Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", sans-serif';
  const CHALK = '"LXGW WenKai", "霞鹜文楷", KaiTi, STKaiti, "AR PL UKai CN", "Noto Serif CJK SC", serif';      // 小黑板上的粉笔字
  const IPA = '"Segoe UI", "Lucida Sans Unicode", "DejaVu Sans", "Noto Sans", "Arial Unicode MS", sans-serif';     // 音标（ʃ ə ˈ ː 这些字体里都有）
  // 5.0 起：音节表的标注颜色，和表里“说明”一致：红色删除线 = 不发音、蓝色下划线 = 固定组合、绿色 = 读字母音、紫色 = 特殊读音
  const SYL_C = { silent: '#C0392B', combo: '#0070C0', long: '#00A050', special: '#7030A0', hi: '#F0A500' };
  const WALKERS = /^(?:🚶|🏃|🚴|🚵|🏇|🧑‍🦯|👨‍🦯|👩‍🦯|🧑‍🦽|🧑‍🦼)/u;      // 6.18：朝左的走路、跑步表情（往右走时自动翻过来）
  const SEC_C = ['#2D5A4E', '#C2571A', '#6B4FA0', '#2F6FB3', '#B5476B', '#1E7F74', '#2B7A3E'];      // 6.15：答案（绿）      // 6.13：练习（青绿）        // 读音拆分（墨绿）、含义拆分（橙）、同义词辨析（紫）、总结（蓝）、考点（玫红，6.11）
  const SEC_DEF = { '读音拆分': [0, '一块一块读，再连起来'], '含义拆分': [1, '拆开看：它为什么是这个意思'], '同义词辨析': [2, '中文一样，英语不一样：差在哪儿'], '总结': [3, '把重点记下来'], '考点': [4, '考试常考什么'], '练习': [5, '学完做一做'], '答案': [6, '对一对答案'] };
  const SEC_NO = ['一', '二', '三', '四', '五', '六', '七'];
  const C = {
    bg: '#FBF8F1', ink: '#1F2A26', soft: '#56645E', faint: '#98A39D', board: '#2D5A4E', line: '#E4DCCB',
    card: '#FFFFFF', warm: '#F4EDDC', marker: '#FFE04A', green: '#2B7A3E', red: '#C0392B'
  };
  // 每个部分一种颜色（单词里的字母、卡片、等式都用同一种颜色，学生一眼对得上）
  const PART = ['#2F6FB3', '#D9480F', '#2B8A3E', '#7048E8', '#B8860B', '#0B7285'];
  const tint = (hex, a) => {
    const n = parseInt(hex.slice(1), 16), r = n >> 16, g = (n >> 8) & 255, b = n & 255;
    const m = x => Math.round(x + (255 - x) * a);
    return 'rgb(' + m(r) + ',' + m(g) + ',' + m(b) + ')';
  };

  // ---------------------------------------------------------------- 文字
  const clean = s => String(s || '').replace(/\r\n?/g, '\n').trim();
  const oneLine = s => String(s || '').replace(/\s+/g, ' ').trim();
  const hasCjk = s => /[\u3400-\u9fff]/.test(s);
  const PLACE = /^(—+|－+|-+|–+|无|暂无|没有|【待处理】|待处理|n\/a|none|\/)$/i;
  const blank = t => !oneLine(t) || PLACE.test(oneLine(t));
  // 去掉两头成对的引号（“搬到另一边” → 搬到另一边）；只有一头有引号的（动词词尾，“使…、做…”）不动
  const unquote = s => {
    const t = oneLine(s).replace(/[。．]+$/, '');
    const m = /^[“"「『‘]([\s\S]*)[”"」』’]$/.exec(t);
    return m ? m[1].trim() : t;
  };
  const normPart = s => String(s || '').toLowerCase().replace(/[^a-z0-9]/g, '');
  // 括号里还套着括号的（例句里的注释），一层层去掉
  const dropParens = s => { let t = String(s || ''), t2; while ((t2 = t.replace(/（[^（）]*）/g, '').replace(/\([^()]*\)/g, '')) !== t) t = t2; return t.replace(/\s+/g, ' ').trim(); };
  // 短一点：在括号、分号前断开；还长就在逗号前断开
  function brief(s, max) {
    let t = oneLine(s);
    const cut = (re) => { const i = t.search(re); if (i > 0) t = t.slice(0, i); };
    cut(/[；;]/);
    if (t.length > max) cut(/[（(]/);
    if (t.length > max) cut(/[，,]/);
    t = t.trim();
    if (t.length > max) t = t.slice(0, max - 1) + '…';
    // 断在引号里面了（“使…、做…）：从没配对的“前面断开
    const open = t.lastIndexOf('“');
    if (open > 0 && t.indexOf('”', open) < 0) t = t.slice(0, open).replace(/[，、,\s]+$/, '');
    else if (open === 0 && t.indexOf('”') < 0) t = t.slice(1);
    return t;
  }

  // 按【小标题】分段（行首、句号分号后面的才算；“见【辨析】”这种是引用，不分）
  function segments(text) {
    const s = clean(text), out = [], cuts = [];
    const re = /【([^【】\n]{1,10})】/g;
    let m;
    while ((m = re.exec(s))) {
      const ls = s.lastIndexOf('\n', m.index - 1) + 1, head = s.slice(ls, m.index);
      if (/^\s*[\u2460-\u2473]?\s*$/.test(head)) cuts.push({ at: ls, end: m.index + m[0].length, mk: m[1] });
      else if (/[。；;！？!?]\s*$/.test(head)) cuts.push({ at: m.index, end: m.index + m[0].length, mk: m[1] });
    }
    const first = s.slice(0, cuts.length ? cuts[0].at : s.length).trim();
    if (first) out.push({ mk: '', body: first });
    cuts.forEach((c, i) => out.push({ mk: c.mk, body: s.slice(c.end, i + 1 < cuts.length ? cuts[i + 1].at : s.length).trim() }));
    return out;
  }
  const segBody = (list, mk) => (list.find(x => x.mk === mk) || {}).body || '';

  // “各部分解释”里“make：做（见 make）”“-er：…”这样的行
  // 标签可以带括号（al(l)、jack(=jaque)、state（v.）、(s)pect）；“-et、-in”“-ist + -ic”一行写两个的，拆成两条
  const HEAD_RX = /^((?:[^：:\u3400-\u9fff【】（）()]|\([^()：:]{0,24}\)|（[^（）：:]{0,12}）){1,48}?)\s*[：:]\s*(.*)$/;
  const normHead = h => normPart(String(h || '').replace(/（[^（）]*）/g, '').replace(/\(\s*=[^()]*\)/g, '').replace(/\([^()]*\)\s*-?\s*$/, ''));
  // 6.2（总表“词缀身份辨析”版）：前缀、后缀那一行写成“标签：身份：开头的介绍；记：…。辨析：…”——开头的介绍就是这个词缀的身份
  // （意思、作用、来历括号），记法紧跟在后面，辨析（原来的“分工”）在这一行最后、到行末为止、里面没有句号。
  // idNew：是不是这种写法；rest：去掉“身份：”这个记号和辨析以后的话（开头的介绍 + 记法，后面照老办法读）；bx：辨析的话。
  // 写法要和维护技能的 linetools.py（ID_MARK、BX_MARK）、cizhui.py 一起改
  const ID_LEAD_RX = /^身份[：:]\s*/, BX_RX = /。\s*辨析[：:]\s*([^。\n]*)。?\s*$/;
  function bianxiOf(text) {
    const t = String(text || '');
    if (!ID_LEAD_RX.test(t)) return { idNew: false, bx: '', rest: t };
    let rest = t.replace(ID_LEAD_RX, ''), bx = '';
    const m = BX_RX.exec(rest);
    if (m) { bx = m[1].trim(); rest = rest.slice(0, m.index); }
    return { idNew: true, bx, rest };
  }
  // 6.2：“前缀辨析 / 后缀辨析”那一幕上面“身份”小框里写什么：开头的介绍的第一句（括号去掉，太长就在逗号、冒号处截短），
  // 后面接来历括号里的头一句（“来自拉丁语介词 pro”“英语本来就有的后缀”）。没有标准的来历括号就只写第一句——宁可少写，不自己拼
  function idtOf(intro) {
    const t = String(intro || '').trim();
    let d = 0, q = 0, cut = t.length;
    const marks = [];                                                        // 第一句里括号、引号外面的逗号、冒号
    for (let i = 0; i < t.length; i++) {
      const ch = t[i];
      if (ch === '（' || ch === '(') d++; else if (ch === '）' || ch === ')') d = Math.max(0, d - 1);
      else if (ch === '“') q++; else if (ch === '”') q = Math.max(0, q - 1);
      else if (d === 0 && q === 0 && (ch === '；' || ch === '。')) { cut = i; break; }
    }
    const first = t.slice(0, cut);
    let core = first.replace(/（[^（）]*(?:（[^（）]*）[^（）]*)*）/g, '').replace(/[，：、\s]+$/, '').trim();
    if (core.length > 34) {
      q = 0;
      for (let i = 0; i < core.length; i++) { const ch = core[i]; if (ch === '“') q++; else if (ch === '”') q = Math.max(0, q - 1); else if (q === 0 && (ch === '，' || ch === '：') && i >= 6 && i <= 34) marks.push(i); }
      core = marks.length ? core.slice(0, marks[marks.length - 1]) : core.slice(0, 33) + '…';
    }
    let src = '';
    for (const pg of parenGroups(first)) {
      const seg = pg.split('；')[0].trim();
      if (!/^(来自|英语本来就有|英语本族|古英语)/.test(seg)) continue;
      src = seg.split(/[，：]/)[0].replace(/“[^”]*”\s*$/, '').trim();        // “来自拉丁语介词 pro“在前面、向前”，本来是单独的一个词” → “来自拉丁语介词 pro”
      break;
    }
    if (core && src && (core + src).length > 44) src = '';                    // 一行写不下：只写第一句
    return core && src ? core + '，' + src : core || src;
  }
  function partLines(t) {
    const lines = clean(t).split('\n').map(x => x.trim()).filter(Boolean)
      .filter(x => !/^(意思怎么变|用词规律)[：:]/.test(x));          // 总表后来加的“意思怎么变”“用词规律”两行不算部分，也不算进比例
    const list = [];
    for (const ln of lines) {
      const m = HEAD_RX.exec(ln);
      if (!m || !/[A-Za-z0-9]/.test(m[1]) || /^https?$/i.test(m[1].trim())) continue;
      const head = m[1].trim(), b0 = bianxiOf(m[2].trim()), text = b0.rest;          // 6.2：新写法的词缀行，先拿掉“身份：”这个记号和最后的辨析
      const toks = head.split(/\s*(?:、|\s\+\s|，)\s*/).filter(Boolean);
      if (toks.length >= 2 && toks.every(x => /^-?[A-Za-z()=]+-?$/.test(x))) toks.forEach(tk => list.push({ head: tk, norm: normHead(tk), text, multi: true, bx: b0.bx, idNew: b0.idNew }));
      else list.push({ head, norm: normHead(head), text, bx: b0.bx, idNew: b0.idNew });
    }
    return { list, ratio: lines.length ? list.length / lines.length : 0 };
  }
  // 拆分的部分 → 各部分解释的哪一行：先认写法一样的，再认头尾对得上的，同一部分出现两次用同一行；
  // 一个字母的部分（make + r 的 r）只认以它结尾的标签（-er）；最后才按位置配，而且不抢别的部分写法一样的行
  function matchParts(parts, pl) {
    const keys = parts.map(p => normPart(p.text)), res = parts.map(() => null), used = new Set();
    const full = parts.map(p => normPart(p.text + (p.inline && !p.eq && /^[A-Za-z]+$/.test(p.inline) ? p.inline : '')));   // n(e) → ne、v(ideo) → video
    keys.forEach((k, i) => { const j = pl.findIndex((x, jj) => !used.has(jj) && (x.norm === k || x.norm === full[i])); if (j >= 0) { res[i] = j; used.add(j); } });
    keys.forEach((k, i) => {
      if (res[i] != null) return;
      const a = keys.findIndex((kk, ii) => ii < i && kk === k && res[ii] != null);
      if (a >= 0) { res[i] = res[a]; return; }
      let j = -1;
      if (k.length <= 1) j = pl.findIndex((x, jj) => !used.has(jj) && x.norm && x.norm !== k && x.norm.endsWith(k));
      else {
        j = pl.findIndex((x, jj) => !used.has(jj) && x.norm && (x.norm.endsWith(k) || k.endsWith(x.norm) || x.norm.startsWith(k) || k.startsWith(x.norm)));
        if (j < 0) j = pl.findIndex(x => x.norm && x.norm.length > k.length && x.norm.includes(k));
      }
      if (j >= 0) { res[i] = j; used.add(j); }
    });
    keys.forEach((k, i) => {
      if (res[i] != null || k.length <= 1 || i >= pl.length || used.has(i) || keys.includes(pl[i].norm)) return;
      res[i] = i; used.add(i);
    });
    return res;
  }

  // 拆分那一格：parts（trans + port）/ variant（made ← maked）/ related（match ≈ make）/ single（基础词、不好拆分）
  function parseSplit(raw) {
    let s = oneLine(raw);
    if (!s || PLACE.test(s)) return { kind: 'single' };
    s = s.split(/[；;]/)[0].trim();
    s = s.replace(/\s*（[^（）]*[\u3400-\u9fff][^（）]*）/g, '').trim();          // （形容词）这类中文注释
    if (/\s←\s/.test(s)) {
      const [to, from] = s.split(/\s*←\s*/);
      if (to && from && !/\s\+\s/.test(from)) return { kind: 'variant', to: to.trim(), from: from.trim() };
      return { kind: 'single', text: s };
    }
    if (/\s≈\s/.test(s)) return { kind: 'related', items: s.split(/\s*≈\s*/).map(x => x.trim()).filter(Boolean) };
    if (/\s\+\s/.test(s)) {
      const parts = splitTop(s, '+').map(x => {                                    // 括号里的“+”不算（surg(=chir + urg)）
        const m = /^(.*?)\s*\(\s*(=?)\s*([^()]*)\)\s*$/.exec(x.trim());
        return m ? { text: m[1].trim(), inline: m[3].trim(), eq: !!m[2] } : { text: x.trim(), inline: '' };
      }).filter(p => p.text);
      const merged = [];                                                           // plan + n + ed：双写的 n 并进 plan，写成 plan(n)
      parts.forEach(p => {
        const k = normPart(p.text), prev = merged[merged.length - 1];
        if (prev && k.length === 1 && /[a-z]/.test(k) && normPart(prev.text).endsWith(k)) prev.text += '(' + p.text + ')';
        else merged.push(p);
      });
      if (merged.length >= 2) return { kind: 'parts', parts: merged };
    }
    return { kind: 'single', text: s };
  }

  // 在顶层（括号外）按某个符号切开
  function splitTop(s, sep) {
    const out = [];
    let depth = 0, cur = '';
    for (const ch of s) {
      if (ch === '（' || ch === '(') depth++;
      if (ch === '）' || ch === ')') depth = Math.max(0, depth - 1);
      if (ch === sep && depth === 0) { out.push(cur); cur = ''; } else cur += ch;
    }
    out.push(cur);
    return out.map(x => x.trim()).filter(Boolean);
  }
  // “=”右边的字面意思：“搬到另一边”；“不走运的”→“不快乐的”连着几段的用 → 连起来；后面的（注释）不要
  // 5.1 起：等号后面是“写下来”这件事、“一起争取”这件事这种（引号外面还跟着几个字），字面意思带上后面的字（以前只取引号里的，念成“就成了写下来”）
  function literalOf(right) {
    const base = literalOf0(right);
    const m = /^\s*[“"]([^”"]*)[”"]([\u3400-\u9fff]{1,6})(?=$|[；;，,。\s（(])/.exec(String(right || ''));
    return m && base === m[1] ? base + m[2] : base;
  }
  function literalOf0(right) {
    const r = oneLine(right);
    const Q = '“((?:[^“”]|“[^“”]*”)*)”';                 // 引号里可以再套一层引号：“主张“国际”的人”
    const m = new RegExp('^' + Q + '((?:\\s*→\\s*“(?:[^“”]|“[^“”]*”)*”)*)').exec(r);
    if (m) return [m[1]].concat((m[2].match(/“(?:[^“”]|“[^“”]*”)*”/g) || []).map(x => x.slice(1, -1))).join(' → ');
    return unquote(dropParens(r.split(/[，；;。]/)[0]));
  }
  const termOf = x => { const m = /^(.*?)\s*[（(]([^（）()]*)[）)]\s*$/.exec(x); return m ? { text: m[1].trim(), gloss: m[2].trim() } : { text: x.trim(), gloss: '' }; };
  // 派生路线的一步：“unused（没用过的 / 不习惯的），跟着 used …”——词后面第一个括号是意思，后面的说明不要
  const routeTerm = x => { const m = /^([^（(]*?)\s*[（(]([^（）()]*)[）)]/.exec(String(x).trim()); return m ? { text: m[1].trim(), gloss: m[2].trim() } : { text: String(x).trim().split(/[，,；;。：:]/)[0].trim(), gloss: '' }; };
  // 括号、引号外面的第一个“=”（a（= on）+ wake（醒）=“醒起来”里括号中的“=”不算）
  function topEq(s) {
    let d = 0, q = 0;
    for (let i = 0; i < s.length; i++) {
      const ch = s[i];
      if (ch === '（' || ch === '(') d++;
      else if (ch === '）' || ch === ')') d = Math.max(0, d - 1);
      else if (ch === '“') q++;
      else if (ch === '”') q = Math.max(0, q - 1);
      else if (ch === '=' && d === 0 && q === 0) return i;
    }
    return -1;
  }
  // 构词逻辑第一行：“trans（到另一边）+ port（搬运）=“搬到另一边”” → { terms: [{ text, gloss }], literal }；
  //   “派生路线：divide → individual（个体的）→ individualize（使个体化）” → { route: [{ text, gloss }], literal: 最后一步的意思 }
  function parseEquation(line) {
    const s = oneLine(line);
    const rm = /^派生路线[：:]\s*(.*)$/.exec(s);
    if (rm) {
      const route = splitTop(rm[1], '→').map(routeTerm).filter(x => x.text && x.text.length <= 40);
      return route.length >= 2 ? { terms: [], route, literal: route[route.length - 1].gloss || '' } : null;
    }
    const i = topEq(s);
    if (i < 0) return null;
    const left = s.slice(0, i), right = s.slice(i + 1);
    const terms = /\+/.test(left) && !/→/.test(left) ? splitTop(left, '+').map(termOf) : [];
    return { terms, literal: literalOf(right) };
  }
  // 构词逻辑里“→”开头的几行：说明 → 结果
  function stepsOf(logic) {
    return clean(logic).split('\n').map(x => x.trim()).filter(x => /^[→⇒\u2460-\u2473]/.test(x)).map(ln => {
      const marks = [];                                                         // 这一步末尾标的〔用词规律①〕（三列分工后标在组合列）
      ln.replace(/〔用词规律([①②③④⑤⑥⑦⑧⑨⑩]+)〕/g, (_, m) => { marks.push(...m); return ''; });
      ln = ln.replace(/〔用词规律[^〕]*〕/g, '').trim();
      const ps = ln.replace(/^[→⇒]\s*/, '').replace(/^[\u2460-\u2473]\s*(?:[^，。→“”（）]{1,16}[：:])?\s*/, '').split(/\s*→\s*/);
      const result = ps.pop() || '';
      return { text: ps.join(' → '), result, marks };
    }).filter(x => x.result);
  }
  // ---- 清爽格式（总表 2026-11 起）：第一行末尾“；词性变化（-or）：动词 → 名词”，下一行后缀等式“X“…”+ -or（…）=“…””（只在第一行看不到时写），
  //      不编号的“　用词规律：”紧跟在用到它的那一步下面。读之前先还原成融合格式（“词性变化（-or）：A → B。X“…”加上 -or（…），就成了“…””、
  //      “用词规律①：”、步骤末尾〔用词规律①〕），下面的读法都不用改。和维护技能 columns.py 的 parse_I 是同一套规则。
  const TAIL_RX = /；\s*词性变化(（(?:[^（）]|（[^（）]*）)+）[：:].*)$/;
  const RULE_NEW_RX = /^\s*用词规律[：:]\s*(.*)$/;
  const STEP_RX = /^\s*[→⇒\u2460-\u2473]/;
  const CIRC10 = '①②③④⑤⑥⑦⑧⑨⑩';
  function topPositions(s, pat) {                    // 括号、引号外面 pat 出现的位置
    const out = []; let d = 0, q = 0;
    for (let i = 0; i < s.length; i++) {
      const ch = s[i];
      if ('（(〔'.includes(ch)) d++;
      else if ('）)〕'.includes(ch)) d = Math.max(0, d - 1);
      else if (ch === '“') q++;
      else if (ch === '”') q = Math.max(0, q - 1);
      else if (d === 0 && q === 0 && s.startsWith(pat, i)) out.push(i);
    }
    return out;
  }
  // “（-less、-ly）：名词 → 形容词 → 副词”或“（-ic）：名词 → 形容词；（-s）：名词 → 名词（复数）” → [[标签, 词性变化]]
  function parseTail(body) {
    const out = [];
    for (const seg of String(body || '').split(/；(?=（)/)) {
      const m = /^（((?:[^（）]|（[^（）]*）)+)）[：:]\s*(.*)$/.exec(seg.trim());
      if (!m) continue;
      const labs = splitTop(m[1], '、'), chain = m[2].trim();
      if (labs.length === 1) { out.push([labs[0], chain]); continue; }
      const nodes = splitTop(chain, '→');
      if (nodes.length === labs.length + 1) labs.forEach((l, k) => out.push([l, nodes[k] + ' → ' + nodes[k + 1]]));
      else out.push([m[1].trim(), chain]);            // “-et、-in”合写一行的，当一个标签
    }
    return out;
  }
  // 后缀等式“X“…”+ -xx（…）=“…”” → “X“…”加上 -xx（…），就成了“…””；不是后缀等式返回 null
  function sentenceFromEq(line) {
    const s = String(line || '').trim();
    if (!s || '→⇒（(【　'.includes(s[0]) || STEP_RX.test(s) || s.startsWith('用词规律') || !s.includes('+ -')) return null;
    const eqs = topPositions(s, '=');
    if (!eqs.length) return null;
    const right = s.slice(eqs[0] + 1).trimStart();
    if (!right.startsWith('“')) return null;
    let d = 0, j = -1;
    for (let k = 0; k < right.length; k++) {
      if (right[k] === '“') d++;
      else if (right[k] === '”') { d--; if (d === 0) { j = k; break; } }
    }
    if (j < 0) return null;
    const res = right.slice(1, j), tail = right.slice(j + 1);
    const left = s.slice(0, eqs[0]).trimEnd(), ks = topPositions(left, '+ -');
    if (!ks.length) return null;
    const base = left.slice(0, ks[ks.length - 1]).trimEnd(), sufsm = left.slice(ks[ks.length - 1] + 1).trim();
    const m = /^(-[^\s（，,]+)\s*(（(?:[^（）]|（[^（）]*）)*）)?\s*$/.exec(sufsm);
    if (!m || !base) return null;
    return base + (/[”）]$/.test(base) ? '' : ' ') + '加上 ' + m[1] + (m[2] || '') + '，就成了“' + res + '”' + tail;
  }
  const ruleBody = t => { const s = String(t || '').trim(); const m = /（((?:[^（）]|（[^（）]*）)*)）\s*$/.exec(s); return (m ? s.slice(0, m.index) : s).replace(/\s+/g, ''); };
  function topEqParts(first) {                       // 第一行 → [[[部分, 意思]], 字面意思]；派生路线的部分就是路线上的每一步
    const s = String(first || '').replace(/^【构词逻辑】/, '').trim();
    const split = (t, sep) => {
      const out = []; let d = 0, cur = '';
      for (const ch of t) {
        if ('（(“'.includes(ch)) d++; else if ('）)”'.includes(ch)) d = Math.max(0, d - 1);
        if (ch === sep && d === 0) { out.push(cur); cur = ''; } else cur += ch;
      }
      out.push(cur);
      return out.map(x => x.trim()).filter(Boolean);
    };
    const term = x => { const m = /^([^（(]*?)\s*[（(]([^（）()]*)[）)]/.exec(x); return m ? [m[1].trim(), m[2].trim()] : [x.trim(), '']; };
    const rm = /^派生路线[：:]\s*(.*)$/.exec(s);
    if (rm) { const items = split(rm[1], '→').map(term); return [items, items.length ? items[items.length - 1][1] : '']; }
    let d = 0, q = 0;
    for (let k = 0; k < s.length; k++) {
      const ch = s[k];
      if ('（('.includes(ch)) d++;
      else if ('）)'.includes(ch)) d = Math.max(0, d - 1);
      else if (ch === '“') q++;
      else if (ch === '”') q = Math.max(0, q - 1);
      else if (ch === '=' && d === 0 && q === 0) {
        const mm = /^\s*“((?:[^“”]|“[^“”]*”)*)”/.exec(s.slice(k + 1));
        return [split(s.slice(0, k), '+').map(term), mm ? mm[1].trim() : ''];
      }
    }
    return [[], ''];
  }
  function fromQingshuang(logic, word) {
    const L = clean(logic).split('\n');
    const mt = TAIL_RX.exec(L[0] || '');
    if (!mt && !L.slice(1).some(l => RULE_NEW_RX.test(l))) return logic;      // 融合格式和更早的格式：原样读
    const first = mt ? L[0].slice(0, mt.index).trimEnd() : L[0];
    const tail = mt ? parseTail(mt[1]) : [];
    const out = [first], eqs = [], bodies = {};
    let seenStep = false, lastStep = -1, nRule = 0;
    for (const l of L.slice(1)) {
      const nm = RULE_NEW_RX.exec(l);
      if (nm) {                                       // 规律行属于它上面最近的一步；同一条再用到时只给那一步标上编号
        const txt = nm[1].trim(), b = ruleBody(txt);
        let n = bodies[b];
        if (!n) { n = CIRC10[nRule++ % 10]; bodies[b] = n; out.push('　用词规律' + n + '：' + txt); }
        if (lastStep >= 0) {
          const ms = /〔用词规律([①②③④⑤⑥⑦⑧⑨⑩]+)〕\s*$/.exec(out[lastStep]);
          if (!(ms && ms[1].includes(n))) out[lastStep] = ms ? out[lastStep].slice(0, ms.index).trimEnd() + '〔用词规律' + ms[1] + n + '〕' : out[lastStep].trimEnd() + '〔用词规律' + n + '〕';
        }
        continue;
      }
      if (STEP_RX.test(l)) seenStep = true;
      if (mt && !seenStep && sentenceFromEq(l)) { eqs.push(sentenceFromEq(l)); continue; }
      out.push(l);
      if (STEP_RX.test(l)) lastStep = out.length - 1;
    }
    // 后缀等式按顺序配给各个后缀；没单写的（单后缀、第一行就是等式），用第一行的等式拼出那句话（取法和 condense.top_eq_parts 一样）
    const [terms, lit] = topEqParts(first);
    const semi = t => String(t || '').replace(/；/g, '、');
    const pos = tail.map(([lab, head], i) => {
      const suf = lab.split('（')[0];
      let sent = eqs[i] || '';
      if (!sent && !terms.length) sent = (word || '这个词') + ' 加上 ' + suf + '，就成了“' + (lit || word) + '”';
      if (!sent && terms.length && lit) {             // 第一行等号后面不是引号里的字面意思（拉丁语原词之类）：只留词性，不拼这句
        const bt = terms.slice(0, -1);
        const base = bt.length === 1 && bt[0][1] ? bt[0][0] + '“' + semi(bt[0][1]) + '”' : bt.map(t => t[0]).join(' + ');
        const sm = semi(terms[terms.length - 1][1]);
        sent = base + (/[”）]$/.test(base) ? '' : ' ') + '加上 ' + suf + (sm ? '（' + sm + '）' : '') + '，就成了“' + semi(lit) + '”';
      }
      return '词性变化（' + lab + '）：' + head + '。' + sent;
    });
    out.splice(1, 0, ...pos);
    return out.join('\n');
  }
  // 2026-11 起总表「含义」列：同一词性的意思写一行、行首写词性（adj. 受欢迎的；流行的、大众的），例子在「例句」列（受欢迎的：a popular teacher）。
  // 先还原成老写法“（adj.）受欢迎的（a popular teacher）；（adj.）流行的、大众的（popular music）”，后面 meaningOf、sensesOf 照老写法读。
  // 同形词“v. ① 轻拍”还原成“① （v.）轻拍”；modal v. / aux. v. 写成“（v.，情态）”“（v.，助动）”（括号里不能有“字母 空格 字母”，不然会被当成英文例子）。
  const POS_LINE = /^(modal v\.|aux\. v\.|n\.|v\.|adj\.|adv\.|pron\.|prep\.|conj\.|num\.|art\.|int\.|phr\.)\s+(.*)$/;
  const OLD_TAG = { 'modal v.': 'v.，情态', 'aux. v.': 'v.，助动' };
  const keyNorm = k => String(k || '').replace(/[\s，,、。.；;：:“”"‘’'!！?？…]/g, '');
  const keyOf = t => { let s = String(t || ''), s2; while ((s2 = s.replace(/（[^（）]*）|\([^()]*\)/g, '')) !== s) s = s2; return s.replace(/[：:]/g, ' ').replace(/\s+/g, ' ').trim() || String(t || '').trim(); };
  function fromPosLines(text, exText) {
    const lines = clean(text).split('\n').map(x => x.trim()).filter(Boolean);
    if (!lines.some(l => POS_LINE.test(l))) return text;
    const senses = [];
    for (const l of lines) {
      const m = POS_LINE.exec(l);
      if (!m) { splitTop(l, '；').forEach(t => senses.push({ pos: '', circ: '', text: t, ex: [] })); continue; }
      let body = m[2].trim(), circ = '';
      const mc = /^([\u2460-\u2473])\s*/.exec(body);
      if (mc) { circ = mc[1]; body = body.slice(mc[0].length); }
      splitTop(body, '；').forEach((t, k) => senses.push({ pos: m[1], circ: k === 0 ? circ : '', text: t, ex: [] }));
    }
    // 例句列：“意思：例子；例子”，意思前面可以带词性（v. 出口：…）
    const used = new Set();
    for (const l of clean(exText || '').split('\n').map(x => x.trim()).filter(Boolean)) {
      const i = l.indexOf('：');
      if (i < 0) continue;
      let k = l.slice(0, i).trim(), p = '';
      const pm = POS_LINE.exec(k);
      if (pm) { p = pm[1]; k = pm[2]; }
      const exs = splitTop(l.slice(i + 1).trim(), '；');
      const nk = keyNorm(k);
      const cand = senses.filter(s => !used.has(s) && (!p || s.pos === p));
      const hit = cand.find(s => keyNorm(s.text.replace(/[：:]/g, ' ')) === nk) || cand.find(s => keyNorm(keyOf(s.text)) === nk);
      if (hit) { hit.ex = exs; used.add(hit); }
    }
    return senses.map(s => (s.circ ? s.circ + ' ' : '') + (s.pos && s.pos !== 'phr.' ? '（' + (OLD_TAG[s.pos] || s.pos) + '）' : '') + s.text +
      (s.ex.length ? '（' + s.ex.join('；') + '）' : '')).join('；');
  }
  // 今义：“制造者、制造商（a car maker 汽车厂商）；常作复合词的后半…” → 主要意思、第二个意思、例子
  function meaningOf(body) {
    const s = oneLine(body);
    if (!s) return { main: '', second: '', example: '' };
    const parts = splitTop(s, '；');
    const ex = (((parts[0] || '').match(/[（(]([^（）()]*)[）)]/g) || []).map(x => x.slice(1, -1)).find(x => /[A-Za-z]+\s+[A-Za-z]+/.test(x) && !/^\s*=/.test(x))) || '';
    const pick = x => dropParens(x).replace(/^[\u2460-\u2473]\s*/, '').replace(/[：:].*$/, '').trim();
    return { main: pick(parts[0] || ''), second: parts[1] ? pick(parts[1]) : '', example: ex.trim() };
  }

  // ---------------------------------------------------------------- 图：词根、意思里的关键词 → 表情符号；会动的方式
  const MORPH = {
    trans: '🌉', port: '📦', portable: '📦', ex: '📤', export: '📤', import: '📥', re: '🔁', pre: '⏩', pro: '⏩', fore: '⏩', post: '⏪',
    sub: '⬇️', super: '⬆️', sur: '⬆️', over: '⬆️', under: '⬇️', inter: '↔️', tele: '🔭', phone: '🔊', phon: '🔊', graph: '✍️', gram: '✍️',
    scrib: '✍️', script: '✍️', dict: '🗣️', spect: '👀', spec: '👀', vis: '👀', vid: '👀', view: '👀', aud: '👂', duct: '🧭', duc: '🧭',
    ject: '🎯', mit: '📨', miss: '📨', struct: '🧱', form: '🔷', tract: '🧲', press: '✋', cycle: '🚲', bio: '🌱', geo: '🌍', hydr: '💧',
    aqua: '💧', photo: '📷', micro: '🔬', uni: '1️⃣', mono: '1️⃣', bi: '2️⃣', tri: '3️⃣', multi: '🔢', auto: '🤖', anti: '🛡️',
    un: '🚫', dis: '🚫', non: '🚫', mis: '❌', er: '🧑', or: '🧑', ist: '🧑', ian: '🧑', ess: '👩', ee: '🧑', ful: '🫙',
    able: '👍', ible: '👍', man: '🧑', woman: '👩', day: '☀️', night: '🌙', sun: '☀️', moon: '🌙', star: '⭐', water: '💧', fire: '🔥',
    hand: '✋', foot: '🦶', head: '🧠', eye: '👁️', heart: '❤️', book: '📖', house: '🏠', home: '🏠', school: '🏫', car: '🚗', ship: '🚢',
    air: '🌬️', light: '💡', time: '⏰', work: '💼', play: '🎮', sport: '⚽', sea: '🌊', land: '🏞️', snow: '❄️', rain: '🌧️', tree: '🌳',
    flower: '🌸', bird: '🐦', fish: '🐟', dog: '🐶', cat: '🐱', horse: '🐴', shoe: '👟', ball: '⚽', key: '🔑', door: '🚪', way: '🛣️',
    road: '🛣️', make: '🛠️', up: '⬆️', down: '⬇️', out: '📤', in: '📥', back: '🔙', side: '↔️', walk: '🚶', run: '🏃', news: '📰', paper: '📄',
    pass: '🛂', mind: '💭', friend: '🤝', ship2: '🤝', home2: '🏠', cook: '🍳', farm: '🌾', song: '🎵', sing: '🎵', music: '🎵', write: '✍️',
    read: '📖', logy: '🎓', ology: '🎓', scope: '👀', duce: '🧭', tend: '↔️', vent: '🚶', ven: '🚶', gress: '👣', rupt: '💥', flu: '🌊',
    clude: '🔒', cide: '🪓', vers: '🔄', vert: '🔄', spire: '🌬️', cess: '🚶', ceed: '🚶', sequ: '👣', vive: '🌱', vit: '🌱', pend: '🪝', teach: '🧑‍🏫', learn: '🎓', study: '🎓', money: '💰', gold: '🪙', game: '🎮', team: '👥', world: '🌍', earth: '🌍'
  };
  // 意思里的关键词（长的在前）
  const KEYS = [
    ['不快乐', '😢'], ['不高兴', '😢'], ['不开心', '😢'], ['难过', '😢'], ['伤心', '😢'], ['体育', '⚽'], ['缩写', '✂️'], ['缩略', '✂️'], ['首字母', '🔠'],
    ['引导', '🧭'], ['实际', '🔧'], ['实践', '🔧'], ['头发', '💇'], ['美发', '💇'], ['理发', '💇'], ['裁缝', '🧵'], ['服侍', '🛎️'], ['服务', '🛎️'],
    ['职责', '📋'], ['军官', '🎖️'], ['官员', '🎖️'], ['消防', '🧑‍🚒'], ['艺术家', '🧑‍🎨'], ['艺术', '🎨'], ['技艺', '🎨'], ['拍照', '📷'], ['摄影', '📷'],
    ['的人', '🧑'], ['演员', '🎭'], ['机械', '⚙️'], ['机器', '⚙️'], ['工程师', '👷'], ['工程', '👷'], ['为首', '👑'], ['木匠', '🪚'], ['建筑师', '👷'],
    ['建筑', '🏛️'], ['设计', '📐'], ['之间', '↔️'], ['这回事', '名词'], ['镜头', '🎬'], ['场景', '🎬'], ['一场', '🎬'], ['河岸', '🏞️'], ['岸', '🏞️'],
    ['到达', '📍'], ['知识', '📚'], ['训练', '🏋️'], ['培训', '🏋️'], ['品尝', '👅'], ['味道', '👅'], ['尝', '👅'], ['也许', '🤔'], ['大概', '🤔'],
    ['可能', '🤔'], ['你的', '👉'], ['关税', '💰'], ['惯例', '📜'], ['习惯', '📜'], ['顾客', '🛍️'], ['客户', '🛍️'], ['市场', '🏪'], ['集市', '🏪'],
    ['新鲜', '🥬'], ['恢复', '🔋'], ['元气', '🔋'], ['餐馆', '🍽️'], ['饭店', '🍽️'], ['自豪', '😌'], ['骄傲', '😌'], ['饭盒', '🍱'], ['一千', '🔢'],
    ['千米', '📏'], ['公里', '📏'], ['米', '📏'], ['准确', '🎯'], ['正好', '🎯'], ['恰好', '🎯'], ['曾经', '⏳'], ['问候', '👋'], ['打招呼', '👋'],
    ['距离', '📏'], ['方法', '🗺️'], ['办法', '🗺️'], ['层', '📄'], ['简单', '👌'], ['容易', '👌'], ['轨条', '🛤️'], ['铁轨', '🛤️'], ['铁路', '🚆'],
    ['对准', '🎯'], ['地址', '📮'], ['自由', '🕊️'], ['递送', '📨'], ['投递', '📨'], ['有关', '🔗'], ['页', '📄'],
    ['回头', '↩️'], ['捐献', '🎁'], ['贡献', '🎁'], ['进步', '📈'], ['进展', '📈'], ['改进', '📈'], ['改善', '📈'], ['介绍', '🤝'], ['改变', '🔀'], ['改观', '🔀'], ['变化', '🔀'], ['预料', '🔮'], ['预计', '🔮'],
    ['预测', '🔮'], ['预言', '🔮'], ['张望', '👀'], ['期待', '👀'], ['尊敬', '🙇'], ['尊重', '🙇'], ['怀疑', '🤔'], ['幸存', '💪'], ['活下来', '💪'], ['吸引', '🧲'],
    ['打断', '✋'], ['依靠', '🤝'], ['依赖', '🤝'], ['独立', '🧍'], ['许诺', '🤞'], ['负责', '🫡'], ['责任', '🫡'], ['一圈', '⭕'], ['周围', '⭕'], ['环境', '🌳'],
    ['交流', '💬'], ['沟通', '💬'], ['港口', '⚓'], ['机会', '🍀'], ['影响', '🌊'], ['方便', '👌'], ['便利', '👌'], ['许可', '✅'], ['准许', '✅'], ['允许', '✅'],
    ['结论', '🔚'], ['建议', '💡'], ['提议', '💡'], ['宇宙', '🌌'], ['延长', '↔️'], ['出席', '🙋'], ['参加', '🙋'], ['后果', '➡️'], ['结果', '➡️'], ['随之而来', '➡️'],
    ['足够', '✅'], ['充分', '✅'], ['吸收', '🧽'], ['焦虑', '😟'], ['担心', '😟'], ['欣赏', '👍'], ['态度', '🙂'], ['中心', '🎯'], ['集中', '🎯'], ['信任', '🤝'],
    ['自信', '😎'], ['消耗', '🔋'], ['毁坏', '💥'], ['摧毁', '💥'], ['盖子', '🧢'], ['发现', '🔍'], ['感情', '💗'], ['情绪', '💗'], ['感觉', '💗'], ['鼓励', '💪'],
    ['激励', '💪'], ['鼓舞', '💪'], ['勇气', '🦁'], ['大声喊', '📢'], ['探索', '🧭'], ['表达', '💬'], ['非凡', '🌟'], ['频繁', '🔁'], ['毕业', '🎓'], ['感激', '🙏'],
    ['感谢', '🙏'], ['身份', '🪪'], ['印象', '💭'], ['表明', '👉'], ['指出', '👉'], ['吹气', '🌬️'], ['坚持', '💪'], ['指示', '👉'], ['解释', '💬'], ['发明', '💡'],
    ['动机', '🎯'], ['相互', '🔄'], ['互相', '🔄'], ['必要', '❗'], ['必需', '❗'], ['躲不掉', '❗'], ['观察', '🔍'], ['获得', '🎁'], ['得到', '🎁'], ['明显', '👁️'],
    ['反对', '🙅'], ['永久', '♾️'], ['从头到尾', '⏳'], ['说服', '🗣️'], ['拥有', '🤲'], ['珍贵', '💎'], ['宝贵', '💎'], ['准备', '🎒'], ['保护', '🛡️'], ['原则', '📏'],
    ['过程', '➡️'], ['职业', '💼'], ['提升', '⬆️'], ['提供', '🎁'], ['认出', '💡'], ['认识', '💡'], ['反射', '🪞'], ['拒绝', '🙅'], ['剩下', '🧍'], ['移动', '🚶'],
    ['代表', '🧑‍💼'], ['需要', '🙏'], ['抵抗', '🛡️'], ['解开', '🔓'], ['解决', '🔓'], ['资源', '⛲'], ['泉', '⛲'], ['回答', '💬'], ['揭示', '🔍'], ['挑选', '👆'],
    ['选择', '👆'], ['成功', '🏆'], ['维持', '🤲'], ['倾向', '↗️'], ['趋势', '📈'], ['传统', '🏮'], ['意愿', '🙋'], ['自愿', '🙋'], ['独一无二', '1️⃣'],
    ['学问', '🎓'], ['学科', '🎓'], ['喜欢', '❤️'], ['报道', '📰'], ['报告', '📋'], ['支持', '🤝'], ['支撑', '🤝'], ['望远镜', '🔭'],
    ['出生', '👶'], ['大自然', '🌿'], ['自然', '🌿'], ['经验', '🎓'], ['熟练', '🎓'], ['正确', '✅'], ['错误', '❌'],
    ['夫人', '👩'], ['太太', '👩'], ['女士', '👩'], ['先生', '👨'], ['地方', '📍'], ['场所', '📍'], ['欢迎', '👏'], ['名气', '🌟'], ['缪斯', '🎭'],
    ['运输', '🚚'], ['交通', '🚦'], ['旅行', '🧳'], ['护照', '🛂'], ['电话', '☎️'], ['电视', '📺'], ['电脑', '💻'], ['计算机', '💻'], ['照片', '📷'],
    ['词典', '📕'], ['字典', '📕'], ['博物馆', '🏛️'], ['医生', '🩺'], ['老师', '🧑‍🏫'], ['学生', '🧑‍🎓'], ['学校', '🏫'], ['学习', '🎓'], ['教育', '🎓'],
    ['制造', '🏭'], ['工厂', '🏭'], ['污染', '🏭'], ['信息', 'ℹ️'], ['国际', '🌐'], ['世界', '🌍'], ['国家', '🏳️'], ['城市', '🏙️'], ['友谊', '🤝'], ['朋友', '🤝'],
    ['重要', '❗'], ['邀请', '💌'], ['参观', '👀'], ['美丽', '🌸'], ['漂亮', '🌸'], ['仔细', '🔍'], ['小心', '⚠️'], ['善良', '💗'], ['快乐', '😊'], ['开心', '😊'],
    ['高兴', '😊'], ['害怕', '😨'], ['生气', '😠'], ['惊讶', '😮'], ['运动', '⚽'], ['音乐', '🎵'], ['唱歌', '🎵'], ['游戏', '🎮'], ['比赛', '🏆'],
    ['生物', '🌱'], ['地理', '🗺️'], ['历史', '📜'], ['科学', '🔬'], ['数学', '🔢'], ['语言', '🗣️'], ['翻译', '🔄'], ['声音', '🔊'], ['时间', '⏰'], ['星期', '📅'],
    ['日子', '📅'], ['日期', '📅'], ['工作', '💼'], ['公司', '🏢'], ['商店', '🛒'], ['购物', '🛒'], ['食物', '🍽️'], ['吃', '🍽️'], ['喝', '🥤'], ['睡', '😴'],
    ['衣服', '👕'], ['鞋', '👟'], ['房子', '🏠'], ['家', '🏠'], ['门', '🚪'], ['路', '🛣️'], ['桥', '🌉'], ['车', '🚗'], ['船', '🚢'], ['飞机', '✈️'], ['飞', '✈️'],
    ['水', '💧'], ['火', '🔥'], ['光', '💡'], ['电', '⚡'], ['太阳', '☀️'], ['白天', '☀️'], ['月亮', '🌙'], ['夜', '🌙'], ['星', '⭐'], ['地球', '🌍'], ['土地', '🏞️'],
    ['山', '⛰️'], ['海', '🌊'], ['河', '🏞️'], ['树', '🌳'], ['花', '🌸'], ['植物', '🌿'], ['生命', '🌱'], ['生长', '🌱'], ['动物', '🐾'], ['鸟', '🐦'], ['鱼', '🐟'],
    ['心', '❤️'], ['爱', '❤️'], ['头', '🧠'], ['脑', '🧠'], ['想', '💭'], ['思', '💭'], ['知道', '💡'], ['眼', '👁️'], ['看', '👀'], ['见', '👀'], ['视', '👀'],
    ['听', '👂'], ['耳', '👂'], ['说', '🗣️'], ['讲', '🗣️'], ['言', '🗣️'], ['写', '✍️'], ['画', '🎨'], ['读', '📖'], ['书', '📚'], ['手', '✋'], ['脚', '🦶'],
    ['走', '🚶'], ['跑', '🏃'], ['搬', '📦'], ['运', '📦'], ['携带', '📦'], ['拿', '🤲'], ['带', '🤲'], ['给', '🎁'], ['送', '📨'], ['寄', '📨'], ['派', '📨'],
    ['扔', '🎯'], ['投', '🎯'], ['拉', '🧲'], ['推', '✋'], ['压', '✋'], ['建', '🧱'], ['造', '🛠️'], ['做', '🛠️'], ['修', '🔧'], ['转', '🔄'], ['变', '🔀'],
    ['分', '✂️'], ['切', '✂️'], ['合', '🤝'], ['一起', '🤝'], ['共同', '🤝'], ['帮', '🤲'], ['钱', '💰'], ['金', '🪙'], ['价', '💰'], ['买', '🛒'], ['卖', '🛒'],
    ['问', '❓'], ['答', '💬'], ['笑', '😊'], ['哭', '😢'], ['力', '💪'], ['强', '💪'], ['快', '⚡'], ['慢', '🐢'], ['冷', '❄️'], ['热', '🔥'], ['新', '🆕'],
    ['旧', '📜'], ['老', '📜'], ['大', '🐘'], ['小', '🐜'], ['远', '🔭'], ['近', '📍'], ['孩子', '🧒'], ['儿童', '🧒'], ['女', '👩'], ['男', '👨'], ['人', '🧑'],
    ['者', '🧑'], ['越过', '🌉'], ['穿过', '🌉'], ['另一边', '🌉'], ['向外', '📤'], ['出', '📤'], ['外', '📤'], ['进', '📥'], ['入', '📥'], ['里', '📥'],
    ['回', '🔁'], ['再', '🔁'], ['又', '🔁'], ['重新', '🔁'], ['前', '⏩'], ['先', '⏩'], ['后', '⏪'], ['上', '⬆️'], ['下', '⬇️'], ['不', '🚫'], ['非', '🚫'],
    ['无', '🚫'], ['没有', '🚫'], ['错', '❌'], ['坏', '👎'], ['好', '👍'], ['能', '👍'], ['可以', '👍'], ['多', '➕'], ['少', '➖'], ['一', '1️⃣'], ['二', '2️⃣'],
    ['两', '2️⃣'], ['三', '3️⃣'], ['数', '🔢'], ['形', '🔷'], ['满', '🫙'], ['充满', '🫙'],
    ['领', '🧭'], ['来', '🚶'], ['向', '🎯'], ['活', '🌱'], ['断', '💥'], ['挂', '🪝'], ['流', '🌊'], ['关', '🔒'], ['伸', '↔️'], ['跟', '👣'], ['吸', '🧽'], ['吹', '🌬️'],
    ['动', '🏃'], ['坐', '🪑'], ['站', '🧍'], ['握', '✊'], ['盖', '🧢'], ['挑', '👆'], ['圈', '⭕'], ['指', '👉'], ['砍', '🪓'], ['退', '🔙']
  ].sort((a, b) => b[0].length - a[0].length);
  // 抽象的后缀（-tion、-ness、-ly…）不配图，写词性
  const POS = [[/名词/, '名词'], [/形容词/, '形容词'], [/副词/, '副词'], [/动词/, '动词']];
  function iconHit(text, morph) {
    const k = normPart(morph);
    if (k && Object.prototype.hasOwnProperty.call(MORPH, k)) return { ic: MORPH[k], key: k };
    const t = oneLine(text);
    if (!t) return { ic: '', key: '' };
    const short = t.replace(/[…\s“”"、，。（）()]/g, '').length <= 6;
    for (const [key, ic] of KEYS) {
      if (key.length === 1 && !short && !t.startsWith(key)) continue;     // 单个字的关键词只在很短的意思里、或者打头时才算（“大自然”不配大象）
      if (t.includes(key)) return { ic, key };
    }
    const to = /(?:变成|构成|做成|成为)\s*(名词|形容词|副词|动词)/.exec(t);
    if (to) return { ic: to[1], key: to[1] };
    for (const [re, label] of POS) if (re.test(t)) return { ic: label, key: label };
    return { ic: '', key: '' };
  }
  const iconFor = (text, morph) => iconHit(text, morph).ic;
  // 后缀的解释里写着“变成 / 构成 X”：词性牌子写 X（整段解释里找，不能先截短）
  // 后缀变成了什么词：“变成形容词”，或“在这里”开头的“动词 → 形容词。”（精简版总表只写这一句）
  const posTarget = t => {
    const s = oneLine(t), m = /(?:变成|构成|做成|成为)\s*(名词|形容词|副词|动词)/.exec(s);
    if (m) return m[1];
    const h = /在这里：([^。；]*)。/.exec(s), a = h ? /→\s*(名词|形容词|副词|动词)/.exec(h[1]) : null;
    return a ? a[1] : '';
  };
  // “不快乐的”“没礼貌的”：配到的图是“快乐”，要在图上画一道红杠（配到的关键词本身是否定的，比如“难过”，就不用）
  const NEG = /^(不|没有|没|无|非)/;
  function negated(text, key) { return NEG.test(oneLine(text)) && !!key && !NEG.test(key) && !['🚫', '❌'].includes(key); }
  // 部分的意思会怎么动：越过、出去、进来、回来、向前、向上、向下、不（划掉）、一起、分开、人、很多；其余是弹出来
  const MOTIONS = [
    [/越过|穿过|另一边|跨|转移|横/, 'across'], [/向外|出去|出来|往外|离开|^出|外/, 'out'], [/进入|向内|往里|里面|^入|^进/, 'in'],
    [/回|返|再|又|重新|向后/, 'back'], [/向前|往前|预先|^先|^前/, 'forward'], [/向上|往上|超过|^上/, 'up'], [/向下|往下|^下|低/, 'down'],
    [/^不|^非|^无|没有|^反|否/, 'not'], [/一起|共同|合|互相/, 'together'], [/分开|拆|离/, 'apart'], [/的人|者|^人/, 'person'], [/很多|多次|复数/, 'many']
  ];
  function motionFor(text) {
    const t = oneLine(text);
    for (const [re, mo] of MOTIONS) if (re.test(t)) return mo;
    return 'pop';
  }
  // 播放器里换图用的一盘表情
  const PICKER = ['🌉', '➡️', '⬅️', '⬆️', '⬇️', '↔️', '🔁', '🔄', '📤', '📥', '⏩', '⏪', '✂️', '🤝', '🎯', '🧲', '✋', '📨', '📦', '🚚',
    '🧑', '👩', '👨', '🧒', '🧑‍🏫', '🧑‍🎓', '👥', '🛠️', '🏭', '🧱', '🏠', '🏫', '🏛️', '📚', '📖', '✍️', '🗣️', '👀', '👂', '🧠',
    '❤️', '💭', '💡', '🔊', '⏰', '📅', '☀️', '🌙', '⭐', '🌍', '🌊', '⛰️', '🌳', '🌸', '🌱', '💧', '🔥', '⚡', '❄️', '🍽️',
    '🚗', '🚢', '✈️', '⚽', '🎵', '🎮', '💰', '🛒', '🔑', '📷', '☎️', '💻', '👍', '👎', '🚫', '❌', '✅', '❓', '➕', '➖'];

  // ---------------------------------------------------------------- 常用前缀、后缀：来自哪种语言、起什么作用（卡片上的小牌子和配音用）
  // 后缀：[来源, 作用, 词性怎么变, 例词]；前缀：[来源, 作用, 例词]。各部分解释里写得更具体的，卡片下面那段话照样用各部分解释。
  const AFFIX_SUF = {
    ion: ['拉丁语', '加在动词后面，把动作变成名词', '动词 → 名词', 'action、invention'],
    tion: ['拉丁语', '加在动词后面，把动作变成名词', '动词 → 名词', 'action、invention'],
    sion: ['拉丁语', '加在动词后面，把动作变成名词', '动词 → 名词', 'decision、discussion'],
    ation: ['拉丁语', '加在动词后面，把动作变成名词', '动词 → 名词', 'information、invitation'],
    ment: ['拉丁语', '加在动词后面，变成名词，表示这个动作或它的结果', '动词 → 名词', 'movement、agreement'],
    ness: ['英语本族', '加在形容词后面，变成名词，表示一种状态', '形容词 → 名词', 'happiness、kindness'],
    ly: ['英语本族', '加在形容词后面，变成副词，表示怎么样地做', '形容词 → 副词', 'quickly、carefully'],
    er: ['英语本族', '加在动词后面，表示做这件事的人或东西', '动词 → 人', 'teacher、driver'],
    r: ['英语本族', '就是 -er，词尾已经有 e 只加 r，表示做这件事的人或东西', '动词 → 人', 'maker、user'],
    or: ['拉丁语', '加在动词后面，表示做这件事的人或东西', '动词 → 人', 'actor、visitor'],
    ist: ['希腊语', '表示做某种事、研究某种学问的人', '→ 人', 'artist、scientist'],
    ian: ['拉丁语', '表示某种人、某地的人', '→ 人', 'musician、librarian'],
    ee: ['法语', '表示被怎么样的人', '动词 → 人', 'employee、trainee'],
    ess: ['法语', '表示女性', '→ 女性', 'actress、waitress'],
    ful: ['英语本族', '来自 full，加在名词后面，变成形容词，表示充满什么的', '名词 → 形容词', 'careful、helpful'],
    less: ['英语本族', '加在名词后面，变成形容词，表示没有什么的', '名词 → 形容词', 'careless、homeless'],
    able: ['拉丁语', '加在动词后面，变成形容词，表示能被怎么样的', '动词 → 形容词', 'readable、washable'],
    ible: ['拉丁语', '和 -able 一样，表示能被怎么样的', '动词 → 形容词', 'possible、visible'],
    al: ['拉丁语', '变成形容词，表示和什么有关的', '名词 → 形容词', 'national、natural'],
    ial: ['拉丁语', '变成形容词，表示和什么有关的', '名词 → 形容词', 'special、official'],
    ic: ['拉丁语、希腊语', '变成形容词，表示什么样的、和什么有关的', '名词 → 形容词', 'magic、scientific'],
    ical: ['拉丁语、希腊语', '变成形容词，表示和什么有关的', '名词 → 形容词', 'musical、physical'],
    ous: ['拉丁语', '加在名词后面，变成形容词，表示充满什么的', '名词 → 形容词', 'dangerous、famous'],
    ious: ['拉丁语', '加在名词后面，变成形容词，表示充满什么的', '名词 → 形容词', 'curious、delicious'],
    ive: ['拉丁语', '变成形容词，表示有什么性质、爱做什么的', '动词 → 形容词', 'active、creative'],
    ity: ['拉丁语', '加在形容词后面，变成名词，表示性质、状态', '形容词 → 名词', 'ability、activity'],
    ty: ['拉丁语', '加在形容词后面，变成名词，表示性质、状态', '形容词 → 名词', 'safety、loyalty'],
    y: ['英语本族', '加在名词后面，变成形容词，表示有什么的、多什么的', '名词 → 形容词', 'rainy、sunny'],
    ize: ['希腊语', '变成动词，表示使变成什么样', '→ 动词', 'realize、modernize'],
    ise: ['希腊语', '就是 -ize 的英式写法，表示使变成什么样', '→ 动词', 'realise、organise'],
    en: ['英语本族', '加在形容词后面变成动词，表示使变得怎么样', '形容词 → 动词', 'widen、darken'],
    ing: ['英语本族', '加在动词后面，表示正在做，或者这件事本身', '动词 → 名词/形容词', 'reading、interesting'],
    ed: ['英语本族', '加在动词后面，表示过去，或者被怎么样的', '动词 → 形容词', 'interested、tired'],
    d: ['英语本族', '就是 -ed，词尾已经有 e 只加 d，表示过去或者被怎么样的', '动词 → 形容词', 'used、divided'],
    ship: ['英语本族', '加在名词后面，表示身份、关系或状态', '名词 → 名词', 'friendship、leadership'],
    hood: ['英语本族', '表示身份、时期或状态', '名词 → 名词', 'childhood、neighbourhood'],
    dom: ['英语本族', '表示状态或范围', '→ 名词', 'freedom、kingdom'],
    ance: ['拉丁语', '变成名词，表示行为或状态', '→ 名词', 'importance、performance'],
    ence: ['拉丁语', '变成名词，表示行为或状态', '→ 名词', 'difference、silence'],
    ant: ['拉丁语', '变成形容词，或者表示做事的人', '→ 形容词/人', 'important、assistant'],
    ent: ['拉丁语', '变成形容词，或者表示做事的人', '→ 形容词/人', 'different、student'],
    ary: ['拉丁语', '表示和什么有关的人、东西或地方', '→ 名词/形容词', 'library、dictionary'],
    age: ['法语', '变成名词，表示行为、状态或一组东西', '→ 名词', 'package、luggage'],
    ure: ['拉丁语', '变成名词，表示行为或结果', '动词 → 名词', 'culture、pressure'],
    ish: ['英语本族', '变成形容词，表示有点像什么的、哪国的', '→ 形容词', 'childish、English'],
    ward: ['英语本族', '表示朝着什么方向', '→ 方向', 'forward、backward'],
    th: ['英语本族', '加在形容词后面，变成名词', '形容词 → 名词', 'warmth、truth'],
    ate: ['拉丁语', '多半变成动词，表示使怎么样', '→ 动词', 'create、celebrate'],
    fy: ['拉丁语', '变成动词，表示使怎么样', '→ 动词', 'beautify、simplify'],
    ify: ['拉丁语', '变成动词，表示使怎么样', '→ 动词', 'simplify、classify'],
    ism: ['希腊语', '变成名词，表示主义、行为或特点', '→ 名词', 'tourism、heroism'],
    logy: ['希腊语', '表示什么学', '→ 学科', 'biology、technology'],
    ology: ['希腊语', '表示什么学', '→ 学科', 'biology、geology'],
    some: ['英语本族', '变成形容词，表示容易怎么样的', '→ 形容词', 'handsome、lonesome'],
    ery: ['法语', '表示场所、行业或一类东西', '→ 名词', 'bakery、machinery'],
    let: ['法语', '表示小的', '→ 小', 'booklet、piglet'],
    ling: ['英语本族', '表示小的、某种人', '→ 小', 'duckling、darling'],
    ese: ['拉丁语', '表示哪国的、哪国人', '→ 国家', 'Chinese、Japanese'],
    an: ['拉丁语', '表示哪里的、哪里的人', '→ 地方/人', 'American、European']
  };
  const AFFIX_PRE = {
    un: ['英语本族', '加在形容词前表示不，加在动词前表示反过来做', 'unhappy、unlock'],
    re: ['拉丁语', '表示再、又，或者回来', 'redo、return'],
    dis: ['拉丁语', '表示不、相反，或者分开', 'dislike、disappear'],
    mis: ['英语本族', '表示错误地', 'mistake、misunderstand'],
    in: ['拉丁语', '加在形容词前表示不，也可以表示进入', 'incorrect、include'],
    im: ['拉丁语', '就是 in-，在 b、m、p 前面写成 im-', 'impossible、import'],
    il: ['拉丁语', '就是 in-，在 l 前面写成 il-，表示不', 'illegal'],
    ir: ['拉丁语', '就是 in-，在 r 前面写成 ir-，表示不', 'irregular'],
    non: ['拉丁语', '表示不、非', 'nonstop'],
    pre: ['拉丁语', '表示在什么之前、预先', 'preview、prepare'],
    pro: ['拉丁语', '表示向前，或者为了', 'progress、protect'],
    ex: ['拉丁语', '表示向外、出来', 'export、exit'],
    trans: ['拉丁语', '表示越过、到另一边', 'translate、transfer'],
    com: ['拉丁语', '表示一起、共同', 'combine、company'],
    con: ['拉丁语', '就是 com-，在多数辅音前写成 con-，表示一起', 'connect、contact'],
    co: ['拉丁语', '表示一起、共同', 'cooperate、coworker'],
    col: ['拉丁语', '就是 com-，在 l 前面写成 col-，表示一起', 'collect'],
    cor: ['拉丁语', '就是 com-，在 r 前面写成 cor-，表示一起', 'correct'],
    de: ['拉丁语', '表示向下、离开、去掉', 'decrease、defrost'],
    sub: ['拉丁语', '表示在下面', 'subway、submarine'],
    sup: ['拉丁语', '就是 sub-，在 p 前面写成 sup-，表示在下面', 'support、suppose'],
    sur: ['法语', '表示在上面、超过', 'surface、surpass'],
    super: ['拉丁语', '表示在上面、超级', 'supermarket'],
    inter: ['拉丁语', '表示在什么之间、相互', 'international、internet'],
    en: ['法语', '表示使怎么样、放进去', 'enjoy、enlarge'],
    em: ['法语', '就是 en-，在 b、p 前面写成 em-', 'empower'],
    ad: ['拉丁语', '表示向、往', 'advance、adventure'],
    ab: ['拉丁语', '表示离开', 'absent'],
    anti: ['希腊语', '表示反对、对抗', 'antivirus'],
    auto: ['希腊语', '表示自己', 'automatic'],
    tele: ['希腊语', '表示远', 'telephone、television'],
    micro: ['希腊语', '表示小', 'microphone'],
    bi: ['拉丁语', '表示两、双', 'bicycle'],
    tri: ['拉丁语', '表示三', 'triangle'],
    uni: ['拉丁语', '表示一、单一', 'uniform'],
    multi: ['拉丁语', '表示多', 'multiple'],
    over: ['英语本族', '表示在上面、过度', 'overcome、overeat'],
    under: ['英语本族', '表示在下面、不足', 'underground'],
    out: ['英语本族', '表示向外、超过', 'outdoor、outrun'],
    up: ['英语本族', '表示向上', 'upstairs'],
    fore: ['英语本族', '表示前面、预先', 'forecast'],
    post: ['拉丁语', '表示在什么之后', 'postpone'],
    per: ['拉丁语', '表示贯穿、彻底', 'perfect'],
    ob: ['拉丁语', '表示对着、反对', 'object'],
    op: ['拉丁语', '就是 ob-，在 p 前面写成 op-', 'oppose']
  };
  // ---- 总表“各部分解释”里写的来源、词性变化、“在这里”、意思怎么变、用词规律（表里写了的以表为准）----
  const SLANG = '拉丁语|拉丁|希腊语|希腊|古诺尔斯语|古诺斯语|北欧语|古法语|英法语|法兰克语|法语|意大利语|西班牙语|葡萄牙语|普罗旺斯语|荷兰语|德语|阿拉伯语|印地语|日耳曼语|古英语|英语';
  const SPRE = '(?:古|中古|晚期|中世纪|俗|民间|现代|原始)?';
  const PLANGS = /拉丁语|希腊语|古诺尔斯语|古诺斯语|法语|意大利语|西班牙语|葡萄牙语|荷兰语|德语|阿拉伯语|印地语/g;
  const normLang = x => (/英语|日耳曼|本族|lic|leas/.test(x) ? '英语本族' : /拉丁/.test(x) ? '拉丁语' : /希腊/.test(x) ? '希腊语' : /诺尔斯|诺斯|北欧/.test(x) ? '古诺尔斯语' : /法/.test(x) ? '法语' : x);
  // 讲词性的“在这里：……所以 ……”那一段里不找来源
  function stripHere(s) {
    const k = s.indexOf('在这里：');
    if (k < 0) return s;
    const j = s.indexOf('所以', k);
    if (j < 0) return s.slice(0, k);
    const ends = [s.indexOf('；', j), s.indexOf('。', j)].filter(e => e >= 0);
    return s.slice(0, k) + (ends.length ? s.slice(Math.min(...ends)) : '');
  }
  function parenGroups(s) {
    const out = [];
    let d = 0, st = -1;
    for (let i = 0; i < s.length; i++) {
      const ch = s[i];
      if (ch === '（') { if (d === 0) st = i; d++; } else if (ch === '）' && d > 0) { d--; if (d === 0) out.push(s.slice(st + 1, i)); }
    }
    return out;
  }
  const TEXT_SRC = [
    new RegExp('^\\s*(?:是|这是|一个)?' + SPRE + '(' + SLANG + ')'),
    new RegExp('(?:来自|源自|出自|借自|取自|往上是|对应|就是|是|从|同出|出|=)\\s*' + SPRE + '(' + SLANG + ')'),
    new RegExp(SPRE + '(' + SLANG + ')[^，。；]{0,16}?(?:词尾|后缀|成分|标记|形式)'),
    /(拉丁|希腊|法)(?:语)?(?:来的|里的)/,
    /(英语本来就有|英语本族|本族的|本族后缀|本族词尾|古英语|日耳曼语|来自\s*-?lic|-leas)/,
    new RegExp(SPRE + '(拉丁语|希腊语) -?[a-zāēīōū]')
  ];
  // 后缀行的来源：先看括号（“来自拉丁语 -io，经法语进入英语”“英语本来就有的后缀”），再看正文（“它来自古英语 lic”“拉丁语中性名词词尾”）
  function affixSource(line) {
    const s2 = stripHere(oneLine(line));
    for (const p of parenGroups(s2)) {
      if (!/来自|英语本来就有|英语本族|古英语|古诺尔斯语/.test(p)) continue;
      if (/英语本来就有|英语本族|古英语/.test(p) && !/来自(拉丁语|希腊语|法语)/.test(p)) return '英语本族';
      const before = p.split('经')[0];
      const ls = [...new Set((before.match(PLANGS) || []).slice(0, 2).map(normLang))];
      if (ls.length) return ls.join('、');
      const m = new RegExp('(' + SLANG + ')').exec(before);
      if (m) return normLang(m[1]);
    }
    for (const p of parenGroups(s2)) { const m = new RegExp('^\\s*' + SPRE + '(' + SLANG + ')').exec(p); if (m) return normLang(m[1]); }
    const body = s2.replace(/^[^：]*：/, '');
    let best = null;
    for (const rx of TEXT_SRC) { const m = rx.exec(body); if (m && (!best || m.index < best.i)) best = { i: m.index, l: m[1] }; }
    return best ? normLang(best.l) : '';
  }
  function tableAffix(text) {
    const s = oneLine(text || ''), out = { from: '', tag: '', here: '', role: '' };
    out.from = affixSource('x：' + s);
    const m = /在这里：([^。；]*?)。([^；]*)/.exec(s);
    if (m) {
      if (/→|变成(?:动词|名词|形容词|副词)/.test(m[1])) out.tag = m[1].replace(/（[^（）]*）/g, '').trim();
      const body = m[2].replace(/（[^（）]*(?:（[^（）]*）[^（）]*)*）/g, '');
      const h = /加上\s*-[A-Za-z]+\s*[，,]?\s*(.*?)(?:[，,]\s*所以|$)/.exec(body);
      if (h) {
        let t = h[1].split(/[。：]/)[0].trim();
        const g = /“([^”]{1,12})”(?:是一个动作|说的是一个动作|说的是“什么样的”|说东西|说的是一种性质|是一样东西|说的是一样东西)/.exec(body);
        if (g) { const g1 = g[1].split('、')[0]; t = t.replace('把这个动作', '把' + g1 + '这个动作').replace('把这种性质', '把' + g1 + '这种性质'); }
        out.here = t;
      }
    }
    // 母词意思的过渡：“communicate 本义‘使共有’：……，就成了‘传达’。”——先讲本义怎么变成本词用的意思
    const b = /([A-Za-z][A-Za-z-]*)\s*本义“([^”]{1,12})”：(.{2,70}?)，就成了“([^”]{1,12})”。/.exec(s);
    if (b) out.bridge = { w: b[1], orig: b[2], why: b[3], best: b[4] };
    const r = s.split(/[（；]/)[0].trim();
    if (r && r.length <= 40) out.role = r;
    return out;
  }
  const tagTo = t => { const x = String(t || '').split('→').pop().trim(); return /人|名词/.test(x) ? '名词' : /形容词/.test(x) ? '形容词' : /副词/.test(x) ? '副词' : /动词/.test(x) ? '动词' : x; };
  function affRole(aff, tab) {
    if (!tab) return aff.role;
    if (!aff.role) return tab.role;
    if (tab.tag && aff.tag && tagTo(tab.tag) !== tagTo(aff.tag)) return tab.role || aff.role;
    return aff.role;
  }
  // “用词规律：① 规律（例子；例子） ② …” → { '①': { text, ex } }
  function parseRules(line) {
    const s = oneLine(line).replace(/^用词规律[：:]\s*/, ''), out = {};
    if (!s) return out;
    const pieces = [];
    let d = 0, cur = '';
    for (const ch of s) {
      if (ch === '（' || ch === '(') d++;
      else if (ch === '）' || ch === ')') d = Math.max(0, d - 1);
      if (d === 0 && /[①②③④⑤⑥]/.test(ch) && cur.trim()) { pieces.push(cur); cur = ''; }
      cur += ch;
    }
    if (cur.trim()) pieces.push(cur);
    pieces.forEach(p => {
      const m = /^([①②③④⑤⑥])\s*(.*)$/.exec(p.trim()); if (!m) return;
      let body = m[2].trim(), ex = '';
      if (body.endsWith('）')) {
        let d = 0, k = body.length - 1;
        for (; k >= 0; k--) { const ch = body[k]; if (ch === '）') d++; else if (ch === '（') { d--; if (d === 0) break; } }
        if (k > 0) { ex = body.slice(k + 1, -1); body = body.slice(0, k); }
      }
      out[m[1]] = { text: body.trim(), ex: ex.trim() };
    });
    return out;
  }
  // “意思怎么变：从字面的“…”出发：① 说明 → 结果〔用词规律①〕 ② …” → [{ result, marks }]
  function parseEvo(line) {
    const s = oneLine(line).replace(/^意思怎么变[：:]\s*/, '').replace(/^从字面的“[^”]*”出发[：:]\s*/, '');
    if (!s) return [];
    return s.split(/(?=[①②③④⑤⑥]\s)/).map(p => {
      const m = /^([①②③④⑤⑥])\s*(.*?)(?:〔用词规律([①②③④⑤⑥]+)〕)?\s*$/.exec(p.trim());
      if (!m) return null;
      const segs = m[2].split(/\s*→\s*/);
      return { result: (segs.pop() || '').trim(), marks: m[3] ? [...m[3]] : [] };
    }).filter(Boolean);
  }
  // 一个部分是前缀、后缀还是词根：各部分解释里写成 trans- / -ion 的算词缀；没写连字符的，按位置查上面的表
  let ROOT_HEADS = new Set();      // 总表「词根」列里的部分（bio-、-logue 写在词根列的就算词根，不查前缀、后缀表）
  let WORD_HEADS = new Set();      // 总表「单词部分」列里的部分（make、up、match：能单独用的英语单词，卡片标“单词”，也不查前缀、后缀表）
  function affixOf(head, text, i, n) {
    const h = oneLine(head), k = normPart(text) || normPart(h), kh = normPart(h);
    if (ROOT_HEADS.has(kh) || ROOT_HEADS.has(k) || WORD_HEADS.has(kh) || WORD_HEADS.has(k)) return null;
    const pre = /-\s*$/.test(h) && !/^\s*-/.test(h), suf = /^\s*-/.test(h);
    if (suf || (!pre && n > 1 && i === n - 1 && (AFFIX_SUF[k] || AFFIX_SUF[kh]))) {
      const a = AFFIX_SUF[kh] || AFFIX_SUF[k];
      return { kind: 'suf', from: a ? a[0] : '', role: a ? a[1] : '', tag: a ? a[2] : '', ex: a ? a[3] : '' };
    }
    if (pre || (n > 1 && i === 0 && (AFFIX_PRE[k] || AFFIX_PRE[kh]))) {
      const a = AFFIX_PRE[kh] || AFFIX_PRE[k];
      return { kind: 'pre', from: a ? a[0] : '', role: a ? a[1] : '', tag: '', ex: a ? a[2] : '' };
    }
    return null;
  }
  // 词族“背景”里说的来源：“这一家词都来自拉丁语”“这是英语自己的词”
  const ORIGIN_RX = [
    [/英语自己的词|英语本族|本族词/, '英语本族'],
    [/(?:来自|出自|源自|借自|来源于)[^，。；]{0,8}?古诺尔斯语/, '古诺尔斯语'],
    [/(?:来自|出自|源自|借自|来源于)[^，。；]{0,8}?希腊语/, '希腊语'],
    [/(?:来自|出自|源自|借自|来源于)[^，。；]{0,8}?拉丁语/, '拉丁语'],
    [/(?:来自|出自|源自|借自|来源于)[^，。；]{0,8}?法语/, '法语'],
    [/(?:来自|出自|源自|借自|来源于)[^，。；]{0,8}?(意大利语|西班牙语|荷兰语|德语|阿拉伯语|葡萄牙语)/, null]
  ];
  function originOf(text) {
    const t = oneLine(text).replace(/^【背景】/, '');
    let best = null;
    for (const [rx, name] of ORIGIN_RX) { const m = rx.exec(t); if (m && (!best || m.index < best.i)) best = { i: m.index, name: name || m[1] }; }
    return best ? best.name : '';
  }
  // 今义的几个意思：“（v.）运输、运送；（n.，英）交通运输（public transport 公共交通）；（文）狂喜” → [{ text, en, rare }]
  const RARE_TAG = /^(俚|俚语|古|史|文|罕|旧|方|粗|废|诗|古义)$/;
  const POS_TAG = { 'v.': '动词', 'vt.': '动词', 'vi.': '动词', 'n.': '名词', 'adj.': '形容词', 'adv.': '副词', 'prep.': '介词', 'conj.': '连词', 'pron.': '代词', 'int.': '感叹词', 'num.': '数词', 'art.': '冠词' };
  // 5.7 起小结（原来的小黑板）的意思前面写英文词性缩写：名词 → n.（意思卡片上的中文词性也换成缩写）
  const POS_ABBR = { '名词': 'n.', '动词': 'v.', '形容词': 'adj.', '副词': 'adv.', '介词': 'prep.', '连词': 'conj.', '代词': 'pron.', '感叹词': 'int.', '数词': 'num.', '冠词': 'art.' };
  // “public transport 公共交通” → { ex: 'public transport', exzh: '公共交通' }
  function splitExample(s) {
    const m = /^([A-Za-z][^\u3400-\u9fff]*?)\s*([\u3400-\u9fff].*)?$/.exec(oneLine(s));
    return m ? { ex: m[1].trim(), exzh: (m[2] || '').trim() } : { ex: '', exzh: '' };
  }
  function sensesOf(body) {
    const s = oneLine(body);
    if (!s) return [];
    return splitTop(s, '；').map(seg => {
      let t = seg.trim(), m;
      const tags = [];
      t = t.replace(/^[\u2460-\u2473]\s*/, '');                                    // tap 的“① 轻拍；② 水龙头”：两个同形词的编号不算意思
      while ((m = /^[（(]([^（）()]*)[）)]\s*/.exec(t))) { tags.push(...m[1].split(/[，,、\s]+/)); t = t.slice(m[0].length); }
      const en = ((t.match(/[（(]([^（）()]*)[）)]/g) || []).map(x => x.slice(1, -1)).find(x => /[A-Za-z]+\s+[A-Za-z]+/.test(x) && !/^\s*=/.test(x))) || '';
      const text = dropParens(t).replace(/[：:].*$/, '').trim();
      const pos = tags.map(x => POS_TAG[String(x).split('/')[0].toLowerCase()]).find(Boolean) || '';
      const abbr = tags.map(x => String(x).split('/')[0].toLowerCase()).find(x => POS_TAG[x]) || '';
      return Object.assign({ text, en: en.trim(), pos, abbr, rare: tags.some(x => RARE_TAG.test(x)), phrase: /^[A-Za-z]/.test(text) }, splitExample(en));
    }).filter(x => x.text && !x.phrase);
  }

  // ---------------------------------------------------------------- 字母怎么增减（变体）：最长公共子序列
  function diffLetters(from, to) {
    const keep = [];
    let src = '';
    // Wed(nesday)：括号里的字母是去掉的
    let inP = false;
    for (const ch of from) {
      if (ch === '(') { inP = true; continue; }
      if (ch === ')') { inP = false; continue; }
      src += ch;
      keep.push(!inP);
    }
    const a = src.split(''), b = to.split('');
    const L = Array.from({ length: a.length + 1 }, () => new Array(b.length + 1).fill(0));
    for (let i = a.length - 1; i >= 0; i--) {
      for (let j = b.length - 1; j >= 0; j--) {
        L[i][j] = a[i].toLowerCase() === b[j].toLowerCase() && keep[i] ? L[i + 1][j + 1] + 1 : Math.max(L[i + 1][j], L[i][j + 1]);
      }
    }
    const ops = [];
    let i = 0, j = 0;
    while (i < a.length || j < b.length) {
      if (i < a.length && j < b.length && keep[i] && a[i].toLowerCase() === b[j].toLowerCase() && L[i][j] === L[i + 1][j + 1] + 1) { ops.push({ ch: b[j], op: 'keep' }); i++; j++; }
      else if (i < a.length && (j >= b.length || L[i + 1][j] >= L[i][j + 1])) { ops.push({ ch: a[i], op: 'del' }); i++; }
      else { ops.push({ ch: b[j], op: 'ins' }); j++; }
    }
    return ops;
  }

  // 3.5 起（总表“字母变化”轮）：音变列第一行“【字母变化】populus（拉丁语）→ pople（古法语）→ peuple（古法语）→ people（英语）”
  // → { forms: [{ text, lang, guess }], steps: [{ ops }], flags0 }。每个形式后面括号里是语言，* 开头是推出来的形式；
  // 写法不对（第一行带“：”的旧写法、没有“（语言）”）或最后一个不是本词的返回 null。和维护技能 zimu_check.py 同一套规则。
  // ops 里每个字母带 r：是不是源头词根里留下来的字母（画成蓝色，学生看得出 popul 的哪几个字母留到了 people 里）
  function chainOf(line, word, root) {
    const items = String(line || '').replace(/^\s*【字母变化】/, '').split('→').map(s => /^\s*(\*?)([A-Za-z][A-Za-z'’\-]*)\s*（([^（）]+)）\s*$/.exec(s));
    if (items.length < 2 || !items.every(Boolean)) return null;
    const forms = items.map(m => ({ text: m[2], lang: m[3].trim(), guess: m[1] === '*' }));
    if (forms[forms.length - 1].text.toLowerCase() !== String(word || '').toLowerCase()) return null;
    // 源头词根在第一个形式里的那几个字母：popul 在 populus 里；crux 里找不到 cruc，就取开头相同的 cru
    const r = String(root || '').replace(/\(.*?\)/g, '').replace(/[^A-Za-z]/g, '').toLowerCase(), f0 = forms[0].text.toLowerCase();
    let at = r ? f0.indexOf(r) : -1, len = r.length;
    if (at < 0) { at = 0; len = 0; while (len < r.length && len < f0.length && r[len] === f0[len]) len++; if (len < 2) len = 0; }
    let flags = f0.split('').map((_, i) => i >= at && i < at + len);
    const flags0 = flags.slice(), steps = [];
    for (let k = 1; k < forms.length; k++) {
      const ops = diffLetters(forms[k - 1].text, forms[k].text), next = [];
      let i = 0;
      ops.forEach(o => {
        if (o.op === 'ins') { o.r = false; next.push(false); }
        else { o.r = !!flags[i]; if (o.op === 'keep') next.push(o.r); i++; }
      });
      steps.push({ ops });
      flags = next;
    }
    return { forms, steps, flags0 };
  }

  // ---------------------------------------------------------------- 把词条变成一段动画的脚本
  // d：/api/etymology/entry 的结果；prefs：{ icons: { 位置: 表情 }, text: { 位置: 文字 }, pace }，位置是 p0、p1…、combo、origin、final
  // 5.1 起（总表“部分记忆”轮）：前缀、词根、后缀那一行末尾的“；记：stat ≈ stand（站）：stand 是站，stat 就是站住不动；它们本是一家”
  // ≈ 真的是一家（同源）、∽ 只是长得像（帮助记忆，不同源）、← 从它变来。读出来给卡片、配音、小黑板用；这一段不算部分的解释正文
  const MEMO_RX = /[；;，,。]?\s*记[：:]\s*([A-Za-z][A-Za-z()\-]*)\s*([≈∽←])\s*([A-Za-z][A-Za-z'’ \-]*?)\s*[（(]([^（）()]*)[）)]\s*[：:]\s*([^\n]*)$/;
  // 5.11：≈ 两边写法差得多的，记法后面接“音变：f 对 d：同一个老音 dh，拉丁语念成 f，英语念成 d（老祖宗 …）”
  // 或一条链“音变：regula（拉丁语）→ reule（古法语）→ rule（英语）：中间的 g 脱落了”。pairs：谁对谁；chain：一步步的写法；text：那一句话
  function shiftOf(t) {
    t = String(t || '').trim().replace(/[。；]+$/, '');
    let why = '';
    const kw = t.indexOf('；原因：');                    // 6.5：总表音变后面的“；原因：…”（维护技能 yuanyin.py 写的）单拿出来，记框里单独一行“原因”
    if (kw >= 0) { why = t.slice(kw + 4).trim(); t = t.slice(0, kw).trim(); }
    const out = { raw: t, pairs: [], chain: [], text: t, why, wy: whyOf(why) };      // 6.6：原因切成总说、发音、起因、例子（whyOf）
    const mp = /^((?:[A-Za-z]+\s*对\s*[A-Za-z]+)(?:、[A-Za-z]+\s*对\s*[A-Za-z]+)*)[：:]\s*(.*)$/.exec(t);
    if (mp) { out.pairs = mp[1].split('、').map(x => x.split(/\s*对\s*/).map(y => y.trim())); out.text = mp[2]; return out; }
    const mc = /^([^：:]*→[^：:]*)[：:]\s*(.*)$/.exec(t);
    if (mc) {
      out.chain = mc[1].split(/\s*→\s*/).map(x => { const q = /^(\*?[^\s（(]+)\s*[（(]([^（）()]*)[）)]/.exec(x.trim()); return q ? { f: q[1], lang: q[2] } : { f: x.trim(), lang: '' }; });
      out.text = mc[2];
    }
    return out;
  }
  function memoOf(line) {
    const m = MEMO_RX.exec(String(line || ''));
    if (!m) return { memo: null, rest: String(line || '') };
    let why = m[5].trim(), shift = null;
    const k = why.indexOf('音变：');
    if (k >= 0) { shift = shiftOf(why.slice(k + 3)); why = why.slice(0, k); }
    why = why.trim().replace(/[。；]+$/, '');
    const a = m[1].trim(), b = m[3].trim(), zh = m[4].trim(), same = a.toLowerCase() === b.toLowerCase();   // port ≈ port（港口）：词根和单独的词写法一样
    return { memo: { a, sym: m[2], b, zh, why, shift, same, text: a + ' ' + m[2] + ' ' + (same ? '单词 ' : '') + b + '（' + zh + '）' }, rest: line.slice(0, m.index).replace(/[；;，,]\s*$/, '') };
  }
  // 5.11（总表“同一个词根”轮）：词根的另一种写法。“-duct：词根 duc 的另一种写法（同一个词根）。字母变化：duc → duct，ducere 的“被领出来的”形式是 ductus：duc 后面加 t。意思：duc“领着走”…”
  // base：词根本身；forms：字母变化链上的几个写法（最后一个是这个词里的写法）；how：怎么变的；howShort：最后那半句（配音念它）；gloss：词根的意思
  // 老表的“由词根 duc 变来。词形：…”照样认
  // 6.0（总表“身份分工”轮）：词根、前缀、后缀那一行里的“身份：…。分工：…”。身份：这个写法（这个词缀）是什么身份；
  // 分工：同一个词根的几种写法（意思相近的几个词缀）各管什么，“；”隔开一条一条的，括号里是例词。这一段不算解释正文
  const SHENFEN_RX = /(?:[；。]\s*)?身份[：:]([^。\n]*)。分工[：:]([^。\n]*?)(?=。|$)/;
  function shenfenOf(line) {
    const t = String(line || ''), m = SHENFEN_RX.exec(t);
    if (!m) return { idt: '', fg: '', rest: t };
    const rest = (t.slice(0, m.index) + t.slice(m.index + m[0].length)).replace(/^。/, '');
    return { idt: m[1].trim(), fg: m[2].trim(), rest };
  }
  // 6.1（总表“动词变化”版）：词根那一行“身份：”前面的
  //   “动词变化：原形 ducere“领”→ 过去式 duxi“领了”→ 过去分词 ductus“被领的”；规律：过去式是 duc 加 s，c 和 s 合写成 x；过去分词是 duc 加 t。”
  // forms：两三个样子（k 原形 / 过去式 / 过去分词，la 拉丁语，zh 中文）；没有单独过去式的动词（gradi → gressus）只有原形、过去分词两个；
  // rule：规律那句话；rules：按“；”切开的几句（画面上一句一行）。这一段不算解释正文。写法要和维护技能的 dongbian.py 一起改
  const VERB_RX = /(?:[；。]\s*)?动词变化[：:]([^。\n]*?)[；;]\s*规律[：:]([^。\n]*?)(?=。|$)/;
  function verbOf(line) {
    const t = String(line || ''), m = VERB_RX.exec(t);
    if (!m) return { verb: null, rest: t };
    const forms = m[1].split(/\s*→\s*/).map(x => { const q = /^(原形|过去式|过去分词)\s*([A-Za-z\u00C0-\u024F]+)\s*(?:“([^”]*)”)?/.exec(x.trim()); return q ? { k: q[1], la: q[2], zh: q[3] || '' } : null; }).filter(Boolean);
    const rest = (t.slice(0, m.index) + t.slice(m.index + m[0].length)).replace(/^。/, '');
    if (forms.length < 2 || forms[0].k !== '原形' || forms[forms.length - 1].k !== '过去分词') return { verb: null, rest };
    const rule = m[2].trim();
    return { verb: { forms, rule, rules: splitTop(rule, '；').map(x => x.trim()).filter(Boolean) }, rest };
  }
  // 6.8（总表“词根形态版”）：词根那一格“词根 duc-“走在前面、领着走”（来自拉丁语动词 ducere“领”）。形态：原形 duc：来自拉丁语原形 ducere“领”，去掉词尾 -ere；…（produce、reduce）。过去式 dux：…。这个词：用原形，写成 duce：…；记：…”
  // → { root, gloss, src, kind, analogy, forms: [{ k, en, src, la, zh, tail, pre, rule, uses: [{ text, show, ex, me }], note }], meK, here, spelled, short, verb, verbAt }。
  // 写法和维护技能 xingtai.py 的 get 是同一套，两边一起改。sp：这一部分在拆分里的写法（duce）
  const XT_RX = /^词根\s+([A-Za-z]+)-“([^”]*)”（([\s\S]*?)）。形态：([\s\S]*?)这个词：([\s\S]*)$/;
  const XT_NOTE = /^(英语里几乎不用|英语里不单用|写法和原形一样|表里的词|今天不单用)/;
  function xingtaiOf(text, sp) {
    const m = XT_RX.exec(String(text || '').trim());
    if (!m) return null;
    const me = m[5].replace(/；记[：:][\s\S]*$/, '').trim();
    const mine = String(sp || '').replace(/\(.*?\)/g, '').replace(/[()-]/g, '').toLowerCase();
    const wsp = (/写成\s+([A-Za-z()]+)/.exec(me) || [])[1] || '';
    const meK = (/^用([^，；\s]+)/.exec(me) || [])[1] || '';
    const forms = splitTop(m[4], '。').map(x => x.trim()).filter(Boolean).map(sen => {
      const f = /^(\S+?)(?:\s+([A-Za-z()]+))?：([\s\S]*)$/.exec(sen);
      if (!f) return null;
      const parts = splitTop(f[3], '；').map(x => x.trim()).filter(Boolean);
      const s0 = parts[0] || '';
      const lm = /([A-Za-zāēīōūæœ*()]+)“([^”]*)”/.exec(s0);
      const tl = s0.match(/(?:去掉|和)词尾\s*-([A-Za-zāēīōū]+)/g) || [];
      const tail = tl.length ? tl[tl.length - 1].replace(/^.*-/, '') : '';
      const pre = (/去掉前缀\s*([a-z]+)/.exec(s0) || [])[1] || '';
      let rule = lm ? s0.slice(lm.index + lm[0].length).replace(/^[，：\s]+/, '') : s0;
      rule = rule.replace(/[，：]?\s*(?:再|原形)?去掉(?:前缀\s*[a-z]+\s*和)?词尾\s*-[A-Za-zāēīōū]+$/, '').trim();
      const uses = [], notes = [];
      parts.slice(1).forEach(cl => {
        if (XT_NOTE.test(cl)) { notes.push(cl); return; }
        const ex = [];
        const show = cl.replace(/（([^（）]*)）/g, (m0, a) => { if (/^[A-Za-z][A-Za-z'’\-、，, ]*$/.test(a.trim())) { ex.push(...a.split(/[、，,]\s*/).map(y => y.trim()).filter(Boolean)); return ''; } return m0; }).trim();
        uses.push({ text: cl, show, ex, me: false });
      });
      return { k: f[1], en: f[2] || '', src: s0, la: lm ? lm[1] : '', zh: lm ? lm[2] : '', tail, pre, rule, uses, note: notes.join('；') };
    }).filter(Boolean);
    if (!forms.length) return null;
    const hasW = (t, w) => w && new RegExp('(^|[^A-Za-z])' + w.replace(/[()]/g, '') + '(?![A-Za-z])', 'i').test(t);
    const want = (wsp || '').replace(/[()]/g, '').toLowerCase();
    forms.forEach(fm => fm.uses.forEach(u => { u.me = fm.k === meK && (hasW(u.text.replace(/（[^（）]*）/g, ''), want || fm.en) || hasW(u.text.replace(/（[^（）]*）/g, ''), mine)); }));
    forms.forEach(fm => { if (fm.k === meK && fm.uses.length && !fm.uses.some(u => u.me)) fm.uses[0].me = true; });
    const src = m[3], hasK = k => forms.some(x => x.k === k && x.en);
    const kind = /动词/.test(src) && forms.some(x => x.k === '过去分词') ? 'verb' : /形容词/.test(src) ? 'adj' : /名词/.test(src) ? 'noun' : 'other';
    const analogy = kind === 'verb' && hasK('过去式') ? 'do → did → done' : kind === 'adj' && hasK('比较级') ? 'good → better → best' : kind === 'noun' && hasK('所有格') ? 'foot → foot’s' : '';
    let short = '';
    const hm = /写成\s+[A-Za-z()]+[：:]\s*([^；]*)/.exec(me);
    if (hm) { const cs = hm[1].split('，').map(x => x.trim()).filter(Boolean), last = cs[cs.length - 1] || ''; if (/[\u3400-\u9fff]/.test(last) && last.length <= 14) short = last; }
    const fmMe = forms.find(x => x.k === meK);
    const shown = wsp || (fmMe && fmMe.en) || mine;
    const here = shown ? shown + '（' + (meK || '') + (short ? '，' + short : '') + '）' : '';
    const vf = kind === 'verb' ? forms.filter(x => x.la && ['原形', '过去式', '过去分词'].includes(x.k)).map(x => ({ k: x.k, la: x.la, zh: x.zh })) : [];
    return { root: m[1], gloss: m[2], src, kind, analogy, forms, meK, here, spelled: !!wsp, short,
      verb: vf.length >= 2 ? { forms: vf, rule: '', rules: [] } : null, verbAt: meK === '原形' ? 'inf' : meK === '过去分词' ? 'pp' : '' };
  }
  // 6.8：“形态”那一幕一句一步：开头一句 → 每个形态先演示（原词去掉词尾），有英语用法的再一句
  function xtSteps(X) {
    const st = [{ t: 'intro' }];
    X.forms.forEach((fm, j) => { st.push({ t: 'demo', j }); if (fm.uses.length) st.push({ t: 'use', j }); });
    return st;
  }
  // 这一部分的身份对着三个样子里的哪一个：过去分词（含经法语、接在前缀后面弱化了的、-at- 词干）→ pp；动词原形、词根本来的样子、接在前缀后面弱化的原形 → inf；
  // 名词 / 形容词的词干、现在分词、带连接元音、只是经法语磨损的……都不对着哪一个（'')
  function verbSlot(idt) {
    const s = String(idt || '');
    if (/现在分词/.test(s)) return '';
    if (/过去分词/.test(s)) return 'pp';
    if (/动词原形|动词原样|词根本来的样子|接在前缀后面(的样子|弱化)/.test(s)) return 'inf';
    return '';
  }
  // 拉丁语的一个样子里，哪几个字母是词根的（标上词根的颜色）：和词根逐个字母比，两头都最多隔一个字母
  // （fac → feci：a 换成了 e，标 f、c；frag → frangere：中间多一个 n，标 f、r、a、g；隔两个以上就不算同一段——
  //   distinctus 词尾 -us 的 u 不算 stingu 的 u）。比出来一样多时挑挨得最紧的（cecidi 标后面的 c…d，不标开头重复出来的 ce；spopondi 标 pond）
  function rootLetters(root, form) {
    const A = String(root || '').toLowerCase().replace(/[^a-z]/g, ''), B = String(form || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase(), n = A.length, m = B.length;
    const kb = new Array(m).fill(false);
    if (!n || !m) return kb;
    let best = [];
    const better = (x, y) => x.length > y.length || (x.length === y.length && x.length > 0 && x[x.length - 1] - x[0] < y[y.length - 1] - y[0]);
    const go = (i, j, got) => {                          // 词根第 i 个字母起、这个样子第 j 个字母起，已经对上的 got
      if (better(got, best)) best = got.slice();
      if (got.length + Math.min(n - i, m - j) <= best.length - 1) return;
      const iMax = got.length ? Math.min(n - 1, i + 1) : n - 1, jMax = got.length ? Math.min(m - 1, j + 1) : m - 1;
      for (let ii = i; ii <= iMax; ii++) for (let jj = j; jj <= jMax; jj++) if (A[ii] === B[jj]) { got.push(jj); go(ii + 1, jj + 1, got); got.pop(); }
    };
    go(0, 0, []);
    best.forEach(j => { kb[j] = true; });
    return kb;
  }
  // 分工那句话切成一条一条：text 去掉括号的话；ex 括号里的例词；forms 这一条开头说的是哪几个写法；me：说的是不是这一部分自己
  // 6.2：bx = true 是词缀的“辨析”——每一条开头就是它讲的那几个词缀（“pre- 是…”“-al、-ic 也是…”“con-、col-、cor- 都是 com-…”），
  // 直接取开头连着的词缀当 forms（三个以内的右边不再重复写）；没有词缀打头的（“少数短词形容词、副词同形…”）整句照写
  // alias：这一行开头写的“= -ous”“= -al”——辨析里哪一条也没提到这个写法时，讲 -ous、-al 的那一条就是讲它的
  function fengongRows(fg, self, bx, alias) {
    const selfs = (Array.isArray(self) ? self : [self]).map(x => String(x || '').toLowerCase()).filter(Boolean);
    const esc = k => k.replace(/[-()]/g, '\\$&');
    const hit = t => selfs.some(k => new RegExp('(^|[^A-Za-z-])' + esc(k) + '(?![A-Za-z])', 'i').test(t));
    let src = String(fg || ''), lead = '', relSrc = '';
    // 6.3：词缀的辨析最后可以有一段“；关系：…”（同一种语言来的几个词缀彼此是什么关系）——先拿出来，不当辨析的条目；写法和维护技能 linetools.py 的 REL_MARK 是同一套
    if (bx) { const rk = src.indexOf('；关系：'); if (rk >= 0) { relSrc = src.slice(rk + 4); src = src.slice(0, rk); } }
    const lm = /^((?:同样|这几个|这些|这三个)[^；：:]*)[：:]\s*/.exec(src);            // 开头的总说（同样是“在前、预先”：）单拿出来
    if (lm) { lead = lm[1].trim(); src = src.slice(lm[0].length); }
    const rows = splitTop(src, '；').map(x => x.trim()).filter(Boolean).map(cl => {
      const ex = [];
      let text = cl.replace(/（([^（）]*)）/g, (m0, a) => { if (/^[A-Za-z][A-Za-z'’\-、，, ]*$/.test(a.trim())) { ex.push(...a.split(/[、，,]\s*/).map(y => y.trim()).filter(Boolean)); return ''; } return m0; }).trim();
      if (bx) {
        const hm = /^((?:-?[A-Za-z]+-?)(?:\s*、\s*-?[A-Za-z]+-?)*)\s*(?=[\u3400-\u9fff])/.exec(text);
        const fm = hm ? hm[1].split(/\s*、\s*/) : [];
        return { text, show: fm.length && fm.length <= 3 ? text.slice(hm[0].length).trim() : text, ex, forms: fm, me: false, raw: cl, uses: usesOf(cl) };
      }
      // 这一条开头说的是哪几个写法：到第一个“是 / 当 / 只 / 多 / 说 / 接 / 原样 / 经”为止
      const mask = text.replace(/（[^（）]*）/g, m0 => '（' + ' '.repeat(m0.length - 2) + '）');          // 括号里的字不算
      const cut = mask.search(/是|当动词|当名词|只在|只是|多是|多加|原样|说“|接在|接拉丁|接日常|经法语|经意大利|带着/);
      const subj = cut > 0 ? text.slice(0, cut) : '';
      const forms = (subj.replace(/（[^（）]*）/g, '').match(/-?[A-Za-z]+(?:\([a-z]\))?-?/g) || []).filter(x => x.length <= 10);
      const pure = subj && !/[\u3400-\u9fff]/.test(subj.replace(/（[^（）]*）/g, '').replace(/[、和\s]/g, ''));     // 开头只有写法（duce、-ful、-y）：画面上左边写了，右边不再重复
      return { text, show: pure && forms.length && forms.length <= 2 ? text.slice(cut).trim() : text, ex, forms: pure ? forms : [], me: false };
    });
    let mine = rows.findIndex(r => r.forms.some(x => selfs.includes(x.toLowerCase())));
    if (mine < 0) mine = rows.findIndex(r => hit(r.text));
    if (mine < 0 && alias) { const al = String(alias).toLowerCase(); mine = rows.findIndex(r => r.forms.some(x => x.toLowerCase() === al)); }
    if (mine >= 0) rows[mine].me = true;
    rows.lead = lead;
    rows.rel = relSrc ? relRows(relSrc, selfs, alias) : [];
    return rows;
  }
  // 6.7：辨析的一条切成几个用法（总表“辨析精简演示版”：例词紧跟在它说明的那个用法后面——“名词、形容词前是“…之前的”（preschool、prehistoric），动词词根前是“预先做”（predict、prepare）”）。
  //   clause：这个用法前面的话；ex：括号里的例词（第一个是演示词）；tag：“名词、形容词前”“动词词根前”“名词后”这类牌子（加在什么词上，用户：“重点是要说明是加动词还是加名词”）；
  //   at / end：括号在这一条原话里的位置（配音把括号换成“比如 preschool，上学以前的”）
  function usesOf(cl) {
    const out = [], rx = /（([A-Za-z][A-Za-z'’\- 、，,]*)）/g;
    let last = 0, m;
    while ((m = rx.exec(cl))) {
      const clause = cl.slice(last, m.index).replace(/^[，：；\s]+/, '');
      const ex = m[1].split(/[、，,]\s*/).map(y => y.trim()).filter(Boolean);
      const tm = /([\u3400-\u9fff、]{1,10}(?:前|后))是/.exec(clause);
      out.push({ clause, ex, tag: tm ? tm[1] : '', at: m.index, end: m.index + m[0].length });
      last = m.index + m[0].length;
    }
    return out;
  }
  // 6.7：演示词自己那一行组合列第一行“pre（在…之前）+ school（学校）=“上学以前的””→ { terms: [{t, g, icon}], lit }；prefs.demo[词] 可以手写 icons、pic、lit、terms，写 false 不要
  function demoOf(w, mat, pf) {
    pf = pf && typeof pf === 'object' ? pf : {};
    const l1 = String((mat && mat.logic1) || '').replace(/^【构词逻辑】/, '').split('；词性变化')[0];
    const eq = l1.indexOf('=“');
    if (eq < 0 && !Array.isArray(pf.terms)) return null;
    const terms = (Array.isArray(pf.terms) ? pf.terms.map(x => ({ t: String(x.t || ''), g: String(x.g || '') }))
      : splitTop(l1.slice(0, eq), '+').map(x => x.trim()).filter(Boolean).map(x => { const m = /^([^（(]+)[（(](.*)[）)]\s*$/.exec(x); return m ? { t: m[1].trim(), g: m[2].trim() } : { t: x, g: '' }; }))
      .slice(0, 3);
    if (terms.length < 2) return null;
    const qs = (eq >= 0 ? l1.slice(eq + 1).split('（')[0] : '').match(/“([^”]*)”/g) || [];
    const lit = pf.lit != null ? String(pf.lit) : (qs.length ? qs[qs.length - 1].slice(1, -1) : '');
    const icons = Array.isArray(pf.icons) ? pf.icons : [];
    terms.forEach((t, j) => { t.icon = icons[j] != null ? String(icons[j]) : (iconFor(t.g, '') || ''); });
    const m = String((mat && mat.m) || '');
    return { w, terms, lit, m, pic: pf.pic ? normPic(pf.pic) : null, icon: pf.icon != null ? String(pf.icon) : (iconFor(m, '') || iconFor(lit, '') || '') };      // 先按现在的意思配（rainy：下雨的 → 🌧️），再按字面意思
  }
  // 6.3：“关系”那一段切成一条一条。text：原话（括号里的补充——拉丁语原词、老祖宗、例词——照写在画面上，配音不念）；forms：条首讲的是哪几个词缀
  // （“-ant、-ent 是…”“pre- 和 pro- 不是…”）；me：讲的是不是这一部分自己——先看条首有没有它，条首都没有再看哪一条提到它（“-ette 是 -et 的阴性形式”也讲了 -et），
  // 再不行看这一行开头的“= -ize”（-ise 用讲 -ize 的那一条）
  const AFFIX_ONE = '(?:-[A-Za-z]+|[A-Za-z]+-)';
  function relRows(src, selfs, alias) {
    const esc = k => k.replace(/[-()]/g, '\\$&');
    const mention = (t, k) => new RegExp('(^|[^A-Za-z-])' + esc(k) + '(?![A-Za-z-])', 'i').test(t);
    const headRx = new RegExp('^(' + AFFIX_ONE + '(?:\\s*[、和]\\s*' + AFFIX_ONE + ')*)');
    const items = splitTop(String(src || ''), '；').map(x => x.trim()).filter(Boolean).map(text => {
      const hm = headRx.exec(text);
      return { text, forms: hm ? hm[1].match(new RegExp(AFFIX_ONE, 'g')) : [], me: false };
    });
    const keys = (selfs || []).map(k => String(k || '').toLowerCase()).filter(k => /^-|-$/.test(k));
    const al = alias ? [String(alias).toLowerCase()] : [];
    let hit = false;
    for (const ks of [keys, al]) {
      if (hit || !ks.length) continue;
      items.forEach(r => { if (r.forms.some(x => ks.includes(x.toLowerCase()))) { r.me = true; hit = true; } });
      if (!hit) items.forEach(r => { if (ks.some(k => mention(r.text, k))) { r.me = true; hit = true; } });
    }
    return items;
  }
  // 6.3：这一幕写哪几条“关系”：讲这个词缀自己的（最多 2 条写在画面上，配音只念第一条）；没有讲它的就没有“关系”框
  function relPick(p) { return p.bx ? ((p.fgRows && p.fgRows.rel) || []).filter(r => r.me).slice(0, 2) : []; }
  const VAR_RX = /^(?:就是)?词根\s*([A-Za-z]+)\s*的另一种写法|^由词根\s*([A-Za-z-]+)\s*变来/;
  function variantOf(text) {
    const t = String(text || ''), m = VAR_RX.exec(t);
    if (!m) return null;
    const base = (m[1] || m[2] || '').replace(/-/g, '');
    const c = /(?:字母变化|词形)[：:]\s*([^。]*)/.exec(t) || /变来（([^（）]*→[^（）]*)）/.exec(t);
    let forms = [], how = '';
    if (c) {
      const seg = c[1], k = seg.search(/[，：；]/);
      how = k >= 0 ? seg.slice(k + 1).trim() : '';
      forms = (k >= 0 ? seg.slice(0, k) : seg).split(/\s*→\s*/).map(x => x.replace(/[（(“"].*$/, '').replace(/^.*\s/, '').trim()).filter(x => /^[A-Za-zé]+$/.test(x));
    }
    let hs = how.replace(/（[^（）]*）/g, '');
    const c2 = hs.lastIndexOf('：');
    if (c2 >= 0) hs = hs.slice(c2 + 1);
    const cl = hs.split(/[，；]/).map(x => x.trim()).filter(Boolean);
    // 配音念哪半句：先找直接说词根字母的（dic 后面加 t），其次是最后一句讲“加、变、掉、写成”的，再不行就最后半句
    const alone = new RegExp('(^|[^A-Za-z])' + base + '([^A-Za-z]|$)'), chg = /加|变|掉|写成|弱化|磨|并|换|简化|同化/;
    hs = cl.find(x => alone.test(x) && chg.test(x)) || cl.slice().reverse().find(x => chg.test(x)) || (cl.length ? cl[cl.length - 1] : '');
    if (hs.length > 18 || /^(同|见)\s/.test(hs) || !/[\u3400-\u9fff]/.test(hs)) hs = '';
    const g = /意思(?:是|[：:])\s*(?:[A-Za-z]+)?“([^”]+)”/.exec(t);
    return { base, forms, how, howShort: hs, gloss: g ? g[1].split('→').pop().trim() : '' };
  }
  // 两个写法逐个字母比：哪几个字母留着（k = true）、哪几个是新多出来的（最长公共子序列）
  function keptLetters(a, b) {
    const A = String(a).toLowerCase(), B = String(b).toLowerCase(), n = A.length, m = B.length;
    const L = Array.from({ length: n + 1 }, () => new Array(m + 1).fill(0));
    for (let i = n - 1; i >= 0; i--) for (let j = m - 1; j >= 0; j--) L[i][j] = A[i] === B[j] ? L[i + 1][j + 1] + 1 : Math.max(L[i + 1][j], L[i][j + 1]);
    const ka = new Array(n).fill(false), kb = new Array(m).fill(false);
    let i = 0, j = 0;
    while (i < n && j < m) { if (A[i] === B[j]) { ka[i] = kb[j] = true; i++; j++; } else if (L[i + 1][j] >= L[i][j + 1]) i++; else j++; }
    return { ka, kb };
  }
  // 6.0：“身份和分工”那一幕讲哪几条：说这一部分自己的那一条一定讲，再从头补到 3 条（词缀 2 条）；别的条只写在画面上
  function fengongPick(p) {
    const rows = p.fgRows || [], max = p.bx ? 3 : p.kind === 'pre' || p.kind === 'suf' ? 2 : 3;      // 6.2：词缀的辨析讲 3 条（pre- / pro- / fore- 三个都讲到）；上一版的表照旧 2 条
    const pick = [];
    const mine = rows.findIndex(r => r.me);
    if (mine >= 0) pick.push(mine);
    for (let i = 0; i < rows.length && pick.length < max; i++) if (!pick.includes(i)) pick.push(i);
    return pick.sort((a, b) => a - b);
  }
  // 6.0（总表“辨析列”轮）：第三部分“同义词辨析”讲什么。
  // 总表「辨析」列：“【同义词】产品：product、produce（农产品）”几行 + 辨析的话（一句讲一个词：product 是可数的“产品”…）+ 可以有一行“逻辑不同：…”。
  // 挑一组：先看【同义词】行里的词，辨析的话里有没有讲它的那一句；没有【同义词】行的，看辨析的话里每个分句开头拿来比的词（historic / historical）。
  // 每个词一张卡：词、中文意思、区别那一句、字面意思（它自己那一行组合列等号后面的，d.syn 带来的）。prefs.distinguish 手写的为准；写 false 不要这一部分
  // 6.11：「考点」列（总表“考点轮”，维护技能 kaodian.py 写的）：一行一个“【变形】…”“【词性转换】…”“【短语】…”“【用法】…”“【易混】…”。
  // prefs.kaodian === false 不要这一部分；{rows: [{label, items: […]}]} 整段手写；{skip: ['短语']} 去掉某几行
  const KD_LABELS = ['变形', '词性转换', '短语', '用法', '易混'];
  const KD_MAX = { '变形': 4, '词性转换': 4, '短语': 4, '用法': 3, '易混': 2 };      // 6.31：总表考点写详细（第七十五版），短语、用法多放一条
  // 6.31（第七十五版）：考点写详细以后一页放不下就分两页（“考点 1/2”“考点 2/2”）。按估算的高度分（排法和 S.kaodian 一样，
  // 字宽按中文一个字、英文半个多字估）：整页在 26 号字放得下就一页；放不下就找一个分法，让两页里高的那页最矮。prefs.kaodian.pages = 1 硬性一页
  const KD_FIT = 578, KD_Z = 26;
  // 6.33：考点一条里“…：The birds are protected by law.”——冒号后面是整句英文的，当例句另起一行（用户：“上面写考点，再换一行写例句”）
  const KD_NUM = '①②③④⑤⑥⑦⑧⑨';
  function kdEx(it) {
    const m = /^(.*\S)\s*：\s*([A-Z][^\u3400-\u9fff：]*[.?!])\s*$/.exec(String(it));
    return m && !/[（(][^）)]*$/.test(m[1]) ? [m[1], m[2]] : [String(it), ''];
  }
  function kdEst(rows, size) {
    const TW = W - 364, lh = size * 1.42, ch = size * 1.85, PAD = 13, GAP = 12;
    const cw = t => { let n = 0; for (const c of String(t)) n += c.charCodeAt(0) < 0x2E80 ? 0.56 : 1; return n * size; };
    let total = 0;
    rows.forEach(r => {
      if (r.label === '词性转换' || r.label === '变形') {
        let x = 0, line = 0;
        const its = r.label === '变形' ? [].concat(...r.items.map((it, k) => splitTop(it, '；').map((seg, j) => ({ t: String(seg).trim(), br: k > 0 && j === 0 })))) : r.items.map(t => ({ t, br: false }));
        its.forEach(({ t, br }) => { if (br && x > 0) { line++; x = 0; } const w = Math.min(TW, cw(t) + size * 1.2); if (x + w > TW && x > 0) { line++; x = 0; } x += w + size * 0.6; });
        total += (line + 1) * ch + PAD * 2 - (ch - size * 1.6);
      } else {
        const n = r.items.reduce((a, it) => a + Math.min(2, Math.max(1, Math.ceil(cw(it) / (TW - size * 0.9)))), 0);
        total += n * lh + PAD * 2 - (lh - size) * 0.4;
      }
    });
    return total + GAP * Math.max(0, rows.length - 1);
  }
  function kdPages(rows, pk) {
    const all = rows.map((r, i) => i);
    if (rows.length < 2 || (pk && pk.pages === 1) || kdEst(rows, KD_Z) <= KD_FIT) return [all];
    let best = null;
    for (let k = 1; k < rows.length; k++) {
      const h = Math.max(kdEst(rows.slice(0, k), KD_Z), kdEst(rows.slice(k), KD_Z));
      if (!best || h < best.h) best = { k, h };
    }
    return [all.slice(0, best.k), all.slice(best.k)];
  }
  const KD_C = { '变形': '#2F6FB3', '词性转换': '#C2571A', '短语': '#2B8A3E', '用法': '#6B4FA0', '易混': '#B5476B' };
  function kaodianOf(f, prefs) {
    const pk = prefs.kaodian;
    if (pk === false) return null;
    if (pk && Array.isArray(pk.rows) && pk.rows.length) return { rows: pk.rows.map(r => ({ label: String(r.label || ''), items: (r.items || []).map(String).filter(Boolean) })).filter(r => r.items.length) };
    if (!f) return null;
    const skip = new Set((pk && pk.skip) || []);
    const rows = [];
    for (const ln of String(f.t).split('\n')) {
      const m = /^【([^】]+)】\s*(.+)$/.exec(ln.trim());
      if (!m || !KD_LABELS.includes(m[1]) || skip.has(m[1])) continue;
      const items = (m[1] === '变形' ? m[2].split(/\s+\/\s+/) : splitTop(m[2], '；')).map(x => String(x).trim()).filter(Boolean).slice(0, KD_MAX[m[1]]);
      if (items.length) rows.push({ label: m[1], items });
    }
    return rows.length ? { rows } : null;
  }
  // 6.13：练习（5 道题；6.13–6.15 在考点后面、总结前面，6.16 起挪到总结后面、答案前面）。用户：“再考点部分讲完了,然后再出5个练习题让学生做,题目要多样化:选择题,填空题,翻译题都可以,
  // 以及其他题型;要有听力题,让学生能听懂当前学的单词,剩下的专门用来测试考点的题目”。
  // 一道题：{ type 题型, ask 题目要求（中文）, listen 听力念的英文（念两遍）, zh 中文句子, stem 英文题干（“______”是空，“p______”是首字母空），
  //          opts 选项, ans 答案（选择题写字母 A–D；填空写要填的词，几个空用数组）, why 解析（一句）, kd 考的是哪一条考点, wait 想一想的秒数 }
  // prefs.lianxi 手写（数组，最多 5 道）为准；false 不要这一部分；没写就按总表自动起草（auto: true，起草出来的要改成真题的样子，见 SKILL.md 规矩 41）
  const LX_TYPES = { '听力': '#1E7F74', '单项选择': '#6B4FA0', '适当形式填空': '#C2571A', '词形转换': '#C2571A', '首字母填空': '#2F6FB3', '完成句子': '#2B8A3E', '汉译英': '#2B8A3E', '英汉互译': '#2B8A3E', '句型转换': '#B5476B', '同义替换': '#B5476B', '词义选择': '#6B4FA0', '填空': '#2F6FB3', '改错': '#B5476B', '选词填空': '#2F6FB3' };
  const LX_WAIT = q => q.listen ? (q.opts.length ? 4 : 6) : q.opts.length ? 5 : (q.stem ? 6 : 8);
  const LETTERS = 'ABCD';
  const LX_N = 7;                                                           // 6.31（第七十五版）：5 道改 7 道（用户：“由原来的5道题增加到7道题”），第 6、7 题专门考考点
  function lxNorm(q, auto) {
    const opts = (q.opts || []).map(String).filter(Boolean).slice(0, 4);
    let ans = Array.isArray(q.ans) ? q.ans.map(String) : String(q.ans == null ? '' : q.ans);
    if (opts.length && !/^[A-D]$/.test(ans)) { const k = opts.findIndex(o => o.toLowerCase() === String(ans).toLowerCase()); ans = k >= 0 ? LETTERS[k] : 'A'; }
    const out = { type: String(q.type || (q.listen ? '听力' : opts.length ? '单项选择' : '填空')), ask: String(q.ask || ''), listen: String(q.listen || ''), zh: String(q.zh || ''),
      stem: String(q.stem || ''), opts, ans, why: String(q.why || ''), kd: String(q.kd || ''), auto: !!auto };
    out.wait = q.wait != null ? Number(q.wait) : LX_WAIT(out);
    return out;
  }
  // 选项里正确答案放在第几个：按单词和题号定（每次起草一样，不会四道都是 A）
  function lxPlace(word, n, k, total) { let h = k * 7; for (const ch of String(word)) h = (h * 31 + ch.charCodeAt(0)) % 9973; return h % total; }
  function lxChoice(word, k, right, wrongs) {
    const ws = []; wrongs.forEach(x => { if (x && x.toLowerCase() !== right.toLowerCase() && !ws.some(y => y.toLowerCase() === x.toLowerCase())) ws.push(x); });
    const n = Math.min(4, ws.length + 1), at = lxPlace(word, n, k, n), opts = ws.slice(0, n - 1);
    opts.splice(at, 0, right);
    return { opts, ans: LETTERS[at] };
  }
  const POS_ZH = { n: '名词', v: '动词', adj: '形容词', adv: '副词' };
  // 总表里一格一道题，一行一项：【题型】要求 / 听： / 中文： / 题干：（可以两行）/ A. … / 答案： / 解析： / 考点：（和维护技能 lianxi.py 的 parse 一样）
  function lxParse(t) {
    const q = { type: '', ask: '', listen: '', zh: '', stem: [], opts: [], ans: '', why: '', kd: '' };
    const KEY = { '听': 'listen', '中文': 'zh', '题干': 'stem', '答案': 'ans', '解析': 'why', '考点': 'kd' };
    String(t || '').split('\n').map(x => x.trim()).filter(Boolean).forEach(ln => {
      let m;
      if ((m = /^【([^】]+)】\s*(.*)$/.exec(ln))) { q.type = m[1]; q.ask = m[2]; return; }
      if ((m = /^([A-D])[.．]\s*(.*)$/.exec(ln))) { q.opts.push(m[2]); return; }
      if ((m = /^(听|中文|题干|答案|解析|考点)[：:]\s*(.*)$/.exec(ln))) { if (m[1] === '题干') q.stem.push(m[2]); else q[KEY[m[1]]] = m[2]; }
    });
    q.stem = q.stem.join('\n');
    if (!q.opts.length && /；/.test(q.ans)) q.ans = q.ans.split('；').map(x => x.trim());      // 几个空
    return q;
  }
  function lxDaan(t) {
    const out = {}; let cur = 0;
    String(t || '').split('\n').map(x => x.trim()).filter(Boolean).forEach(ln => {
      let m;
      if ((m = /^【(\d)】\s*(.*)$/.exec(ln))) { cur = +m[1]; const c = /^([A-D])(?:（.*）|\(.*\))?$/.exec(m[2].trim()); out[cur] = [c ? c[1] : m[2].trim(), '']; return; }
      if (cur && (m = /^(讲解|解析)[：:]\s*(.*)$/.exec(ln))) out[cur][1] = m[2];
    });
    return out;
  }
  function lianxiOf(d, film, prefs, role) {
    const pl = prefs.lianxi;
    if (pl === false) return null;
    const list = Array.isArray(pl) ? pl : pl && Array.isArray(pl.qs) ? pl.qs : null;
    if (list && list.length) return { qs: list.slice(0, LX_N).map(q => lxNorm(q, false)), manual: true };
    // 6.14：总表「题目1」–「题目5」（维护技能 lianxi.py 写的，第 122 条）——有就照读
    const daan = lxDaan(role('daan') ? role('daan').t : '');                // 6.15：「答案」列（【1】D（牛奶和鸡蛋） / 讲解：…）
    const fromTable = [1, 2, 3, 4, 5, 6, 7].map(k => { const f = role('ti' + k); if (!f) return null; const q = lxParse(f.t); const a = daan[k];
      if (a) { q.ans = q.opts.length ? a[0] : (/；/.test(a[0]) ? a[0].split('；').map(x => x.trim()) : a[0]); q.why = a[1] || q.why; } return q; }).filter(q => q && q.type && q.ans && String(q.ans).length);
    if (fromTable.length) return { qs: fromTable.map(q => lxNorm(q, false)), manual: true, table: true };
    const w = String(d.w || ''), lw = w.toLowerCase();
    const mf = role('meaning'), m1 = mf ? String(mf.t).split('\n')[0] : '';
    const pm = /^\s*((?:n|v|adj|adv|pron|prep|conj|phr|vt|vi)\.\/?)+\s*/i.exec(m1);
    const gloss = String((film.meaning && film.meaning.main) || m1.replace(/^\s*((?:[a-z]+)\.\/?)+\s*/i, '').replace(/（[^（）]*）/g, '').split(/[；;]/)[0]).trim();
    const near = (d.near || []).filter(x => x && x.w && x.w.toLowerCase() !== lw);
    const qs = [];
    // ① 听力：念这个词，选出听到的是哪个（干扰项是拼写、读音最像的词：produce / product / provide）
    let wrong = near.slice(0, 3).map(x => x.w);
    if (wrong.length < 3 && /\s/.test(w)) {                                // 短语：换掉介词、副词（depend on → depend in / depend of）
      const SM = ['on', 'in', 'at', 'of', 'for', 'up', 'off', 'with', 'to', 'from'], ps = w.split(/\s+/);
      const j = ps.findIndex(x => SM.includes(x.toLowerCase()));
      if (j >= 0) SM.filter(x => x !== ps[j].toLowerCase()).slice(0, 3 - wrong.length).forEach(x => wrong.push(ps.slice(0, j).concat([x], ps.slice(j + 1)).join(' ')));
    }
    if (wrong.length >= 2) { const c = lxChoice(w, 0, w, wrong); qs.push({ type: '听力', ask: '听录音，选出你听到的' + (/\s/.test(w) ? '短语' : '单词') + '。', listen: w, opts: c.opts, ans: c.ans, why: w + '：' + gloss + '。', kd: '' }); }
    // ② 考点：每一行出题（同一种最多两道），按考点列的顺序
    const rows = (film.kd && film.kd.rows) || [], used = {};
    const zhOf = t => (String(t).match(/[\u3400-\u9fff][\u3400-\u9fff、，…（）]*$/) || [''])[0].replace(/[（）]/g, '');
    const enOf = t => String(t).replace(/[（(][^（）()]*[）)]/g, '').replace(/[\u3400-\u9fff][\u3400-\u9fff、，：:…]*/g, ' ').replace(/\s+/g, ' ').trim();
    const blankWord = t => { const rx = new RegExp('\\b' + lw.split(/\s+/)[0].replace(/[-]/g, '\\-') + '[a-z]*', 'i'); return rx.test(t) ? t.replace(rx, '______') : ''; };
    const one = (label, it) => {
      let m;
      if (label === '词性转换') {
        it = String(it).replace(/^([A-Za-z][A-Za-z-]*)\s+(n|v|adj|adv)\.\s*/, '$2. $1 ');      // 6.32：新写法 protection n.保护 → 先换回老写法再拆
        if ((m = /^(n|v|adj|adv)\.\s*([A-Za-z][A-Za-z-]*)\s*(.*)$/.exec(it))) return { type: '词形转换', ask: '写出 ' + w + ' 的' + POS_ZH[m[1]] + '（' + m[3] + '）。', stem: w + ' → ______', ans: m[2], why: w + ' 的' + POS_ZH[m[1]] + '是 ' + m[2] + '：' + m[3] + '。', kd: label };
        if ((m = /^([A-Za-z-]+)\s*→\s*([A-Za-z-]+)\s*(?:（([^（）]*)）)?/.exec(it))) return { type: '词形转换', ask: '根据中文，写出 ' + m[1] + ' 变来的词（' + (m[2].toLowerCase() === lw ? gloss : '') + '）。', stem: m[1] + ' → ______', ans: m[2], why: m[1] + ' → ' + m[2] + (m[3] ? '：' + m[3] : '') + '。', kd: label };
      }
      if (label === '变形') {
        const seg = splitTop(it.replace(/^(n|v|adj|adv)\.\s*/, ''), '；').map(x => String(x).trim())[0] || '';
        if ((m = /^([\u3400-\u9fff、]+)\s*([A-Za-z][A-Za-z' -]*[A-Za-z])\s*(?:（([^（）]*)）)?/.exec(seg))) return { type: '词形转换', ask: '写出 ' + w + ' 的' + m[1] + '。', stem: w + ' → ______', ans: m[2], why: w + ' 的' + m[1] + '是 ' + m[2] + (m[3] ? '（' + m[3] + '）' : '') + '。', kd: label };
      }
      if (label === '短语') { const en = enOf(it), zh = zhOf(it); if (en && zh) return { type: '英汉互译', ask: '写出下面中文的英文短语。', zh, stem: '______', ans: en, why: zh + '：' + en + '。', kd: label }; }
      if (label === '用法') {
        if ((m = /^(.*?)（不说\s*([^（）]+)）(.*)$/.exec(it))) { const r = enOf(m[1]), x = m[2].trim(); const c = lxChoice(w, qs.length, r, [x]); return { type: '单项选择', ask: '下面哪个说法是对的？', opts: c.opts, ans: c.ans, why: '说 ' + r + '，不说 ' + x + '。', kd: label }; }
        if ((m = /^(.+?)\s*=\s*([A-Za-z][A-Za-z .…-]*[A-Za-z.])/.exec(it))) { const a = enOf(m[1]); return { type: '同义替换', ask: '保持意思不变，填空。', stem: a + ' = ______', ans: m[2].trim(), why: a + ' 和 ' + m[2].trim() + ' 意思一样，可以互换。', kd: label }; }
        const en = enOf(it), b = blankWord(en);
        if (b) return { type: '填空', ask: '用本课的' + (/\s/.test(w) ? '短语' : '单词') + '填空' + (zhOf(it) ? '（' + zhOf(it) + '）' : '') + '。', stem: b, ans: en.match(new RegExp('\\b' + lw.split(/\s+/)[0] + '[a-z]*', 'i'))[0], why: en + '。', kd: label };
      }
      if (label === '易混' && (m = /^([^（]+)（([^（）]+)）/.exec(it))) {
        const ws = m[1].split('/').map(x => x.trim()).filter(Boolean);
        const cls = m[2].split(/[，；]/).map(x => x.trim());
        let q = null;
        for (const c of cls) {
          let k;
          if ((k = /^(.+?)用\s*([A-Za-z]+)$/.exec(c)) && ws.includes(k[2])) q = q && q.me ? q : { ask: k[1] + '，用哪个？', ans: k[2], me: k[2].toLowerCase() === lw };
          else if ((k = /^([A-Za-z]+)\s*是(.+)$/.exec(c)) && ws.includes(k[1])) q = q && q.me ? q : { ask: '“' + k[2] + '”，用哪个？', ans: k[1], me: k[1].toLowerCase() === lw };
        }
        if (q) { const c = lxChoice(w, qs.length, q.ans, ws); return { type: '单项选择', ask: q.ask, opts: c.opts, ans: c.ans, why: m[2] + '。', kd: label }; }
      }
      return null;
    };
    for (const r of rows) for (const it of r.items) {
      if (qs.length >= LX_N || (used[r.label] || 0) >= 2) break;
      const q = one(r.label, it);
      if (q && !(q.type === '填空' && used['填空'])) { qs.push(q); used[r.label] = (used[r.label] || 0) + 1; used[q.type] = 1; }
    }
    // ③ 不够 5 道：词义选择、首字母填空、拼起来是哪个词（视频前面讲过的）
    const fill = [];
    const bi = t => { const o = new Set(); const z = String(t).replace(/[^\u3400-\u9fff]/g, ''); for (let k = 0; k < z.length - 1; k++) o.add(z.slice(k, k + 2)); for (const ch of z) o.add(ch + '#'); return o; };
    const gb = bi(gloss), far = x => { const b = bi(x); let n = 0; b.forEach(t => { if (gb.has(t) && !/#$/.test(t)) n++; }); return n === 0; };     // 意思相近的不当干扰项（理解、了解 / 懂、理解）
    const nearFar = near.filter(x => x.m && x.m !== gloss && far(x.m));
    if (gloss && nearFar.length >= 2) { const c = lxChoice(w, 2, gloss, nearFar.map(x => x.m)); fill.push({ type: '词义选择', ask: '选出 ' + w + ' 的中文意思。', stem: w, opts: c.opts, ans: c.ans, why: w + '：' + gloss + '。' }); }
    if (!/\s/.test(w)) fill.push({ type: '听力', ask: '听录音，写出你听到的单词。', listen: w, stem: '______', ans: w, why: w + '：' + gloss + '。' });      // 听写
    if (gloss && !/\s/.test(w)) fill.push({ type: '首字母填空', ask: '根据中文和首字母，写出单词。', zh: gloss, stem: w[0] + '______', ans: w, why: gloss + '：' + w + '。' });
    if (gloss && nearFar.length >= 2) { const c = lxChoice(w, 3, w, nearFar.map(x => x.w)); fill.push({ type: '单项选择', ask: '“' + gloss + '”的英文是哪个？', opts: c.opts, ans: c.ans, why: gloss + '：' + w + '。' }); }
    if (film.parts && film.parts.length >= 2 && film.parts.every(p => p.gloss)) {
      const p0 = film.parts[0], wr = film.parts.slice(1).map(p => p.gloss).concat(near.map(x => x.m));
      const c = lxChoice(w, 4, p0.gloss, wr);
      fill.push({ type: '单项选择', ask: w + ' 里的 ' + p0.text + ' 是什么意思？', opts: c.opts, ans: c.ans, why: film.parts.map(p => p.text + '（' + p.gloss + '）').join(' + ') + '。' });
    }
    while (qs.length < LX_N && fill.length) qs.push(fill.shift());
    return qs.length ? { qs: qs.map(q => lxNorm(q, true)), manual: false } : null;
  }
  function distOf(d, film, prefs, role) {
    if (prefs.distinguish === false) return null;
    const word = String(d.w || ''), syn = d.syn || {};
    const lit1 = l => { const e = parseEquation(String(l || '').replace(/^【构词逻辑】/, '').replace(/；\s*词性变化.*$/, '')); return e && e.literal ? e.literal : ''; };
    const norm = it => ({ w: String(it.w || ''), gloss: String(it.gloss || ''), note: String(it.note || ''), ex: String(it.ex || ''), literal: String(it.literal || ''), pos: String(it.pos || ''), pic: it.pic ? normPic(it.pic) : null, me: String(it.w || '').toLowerCase() === word.toLowerCase() });
    if (prefs.distinguish && Array.isArray(prefs.distinguish.items) && prefs.distinguish.items.length >= 2) {
      const pd = prefs.distinguish;
      return { key: String(pd.key || ''), items: pd.items.slice(0, 3).map(norm), logic: String(pd.logic || ''), tip: String(pd.tip || ''), manual: true };
    }
    const f = role('bianxi');
    if (!f) return null;
    const lines = clean(f.t).split('\n').map(x => x.trim()).filter(Boolean);
    const groups = [], body = [];
    let logic = '';
    for (const ln of lines) {
      const m = /^【同义词】([^：:]*)[：:](.*)$/.exec(ln);
      if (m) { groups.push({ key: m[1].trim(), words: m[2].split('、').map(x => { const q = /^([^（(]+)(?:[（(]([^（）()]*)[）)])?/.exec(x.trim()); return q ? { w: q[1].trim(), gloss: (q[2] || '').trim() } : null; }).filter(Boolean) }); continue; }
      const lg = /^逻辑不同[：:]\s*(.*)$/.exec(ln);
      if (lg) { logic = lg[1].trim(); continue; }
      body.push(ln);
    }
    // 辨析的话切成分句；开头是英语词的那一句，就是讲这个词的
    const cut = (lines2, out) => lines2.forEach(ln => splitTop(ln, '；').forEach(a => String(a).split('。').forEach(c => {
      c = c.trim().replace(/^[^A-Za-z：:]{0,24}[：:]\s*(?=(?:(?:a|an|the)\s+)?[A-Za-z])/, '');      // “汉语都叫“问题”：problem 是…”：前面的引子不要
      if (c) out.push(c);
    })));
    const clauses = [];
    cut(body, clauses);
    const noteIn = (cs, w) => {
      const rx = new RegExp('^((?:(?:a|an|the)\\s+)?' + w.replace(/[-()]/g, '\\$&') + ')(?![A-Za-z-])((?:\\s*(?:或|和|与|、|\\/)\\s*[A-Za-z][A-Za-z\'’-]*)*)\\s*(.*)$', 'i');
      for (const c of cs) {
        const m = rx.exec(c);
        if (!m || !/[\u3400-\u9fff]/.test(m[3])) continue;
        return /^[A-Za-z]/.test(m[3]) ? c : m[3].trim();              // a historic event 是…：词后面还是英文，整句留着
      }
      return '';
    };
    const noteOf = w => noteIn(clauses, w);
    const item = (w, gloss, noSyn) => {
      let note = noteOf(w), ex = '';
      const me = w.toLowerCase() === word.toLowerCase();
      // 本行没讲它：它自己那一行的辨析也在比本词（提到了本词）的，借它讲自己的那一句；讲别的意思的不借
      if (!note && !me && syn[w] && syn[w].bianxi && new RegExp('(^|[^A-Za-z-])' + word.replace(/[-()]/g, '\\$&') + '(?![A-Za-z-])', 'i').test(syn[w].bianxi.replace(/^【同义词】.*$/gm, ''))) {
        const cs = [];
        cut(clean(syn[w].bianxi).split('\n').filter(x => !/^【同义词】|^逻辑不同/.test(x.trim())), cs);
        note = noteIn(cs, w);
      }
      const pm = /（([^（）]*[A-Za-z][^（）]*)）\s*$/.exec(note);         // 末尾括号里的英文例子单拿出来
      if (pm) { ex = pm[1].trim(); note = note.slice(0, pm.index).trim(); }
      note = note.replace(/^(是|指|作名词指|当名词是|才是)\s*/, '').replace(/^[：:，]\s*/, '');
      const literal = me ? (film.combo && film.combo.literal) || '' : (syn[w] ? lit1(syn[w].logic1) : '');
      let g = gloss || (me || noSyn ? '' : (syn[w] ? syn[w].m : ''));
      const gq = /^“([^”]{1,10})”\s*[：:，]\s*/.exec(note);                 // “农产品”：地里长出来的…… → 意思写在上面，下面不再重复
      if (gq && (!g || g.includes(gq[1]) || gq[1].includes(g))) { g = gq[1]; note = note.slice(gq[0].length); }
      note = note.replace(/^“([^“”]*)”$/, '$1');                              // 整句就是一个引号：引号不要
      const it = norm({ w, gloss: g, note, ex, literal });
      if (me && g) { const pc = (film.pics || []).find(x => x && x.text && (x.text.includes(g) || g.includes(x.text))); if (pc) it.pic = pc; }      // 本词这个意思的画，拿来放在卡片上
      return it;
    };
    let best = null;
    for (const g of groups) {
      const head = g.words.find(x => x.w.toLowerCase() === word.toLowerCase());
      const others = g.words.filter(x => x.w.toLowerCase() !== word.toLowerCase()).map(x => item(x.w, x.gloss || g.key)).filter(x => x.note);
      if (!others.length) continue;
      const me = item(word, (head && head.gloss) || g.key);
      best = { key: g.key, items: [me].concat(others.slice(0, 2)), logic, tip: '' };
      break;
    }
    if (!best && !groups.length) {                                           // 没有【同义词】行：辨析的话里拿来比的词（表里有的）
      const ws = [];
      clauses.forEach(c => { const m = /^(?:(?:a|an|the)\s+)?([A-Za-z][A-Za-z'’-]*)/.exec(c); if (m && syn[m[1]] && !ws.includes(m[1])) ws.push(m[1]); });
      const others = ws.map(w => item(w, '', true)).filter(x => x.note);
      const me = item(word, '', true);
      if (others.length && me.note) best = { key: '', items: [me].concat(others.slice(0, 2)), logic, tip: '' };
    }
    if (!best) return null;
    // 画：prefs.distinguish.pics（{ 词: 画 }）
    const pp = prefs.distinguish && prefs.distinguish.pics ? prefs.distinguish.pics : {};
    best.items.forEach(it => { if (pp[it.w]) it.pic = normPic(pp[it.w]); });
    if (prefs.distinguish && prefs.distinguish.tip) best.tip = String(prefs.distinguish.tip);
    if (prefs.distinguish && prefs.distinguish.logic != null) best.logic = String(prefs.distinguish.logic);
    return best;
  }
  function build(d, prefs) {
    prefs = prefs || {};
    const icons = prefs.icons || {}, texts = prefs.text || {};
    const word = String(d.w || '');
    const F = d.fields || [];
    const role0 = r => F.find(f => f.role === r && !blank(f.t));
    // 6.32（第七十六版）：总表「初中含义」有字时，视频里讲的意思都照它——封面、意思那一幕、例句、演变、总结（用户：“有的英语单词含义过多，
    // 因为现在的学生是初中生……参考上海初中英语的单词含义，然后把一些稍微含义多的，不常见的去掉”）；画面设置写 "senses": "all" 讲「含义」列的全部意思
    const role = r => (r === 'meaning' && prefs.senses !== 'all' && role0('meaning_cz')) || role0(r);
    // 2026-11 起总表分前缀、词根、后缀三列：词根列里每行的标签都是词根
    ROOT_HEADS = new Set(role('root') ? clean(role('root').t).split('\n').map(l => { const m = /^\s*([^：:]{1,40})[：:]/.exec(l); return m ? normPart(m[1].replace(/\(.*?\)/g, '')) : ''; }).filter(Boolean) : []);
    // 2026-11 单词列轮起：「单词部分」列里每行的标签都是单词（基础词本身、母词、合成词里的词）
    WORD_HEADS = new Set(role('word') ? clean(role('word').t).split('\n').map(l => { const m = /^\s*([^：:]{1,40})[：:]/.exec(l); return m ? normPart(m[1].replace(/\(.*?\)/g, '')) : ''; }).filter(Boolean) : []);
    const bodies = F.filter(f => f.role === 'body' && !blank(f.t));
    const logicF = bodies.find(f => /^\s*【构词逻辑】/.test(f.t)) || bodies.find(f => /(^|\n)\s*【构词逻辑】/.test(f.t)) || bodies.find(f => /(^|\n)\s*→/.test(f.t)) || null;
    const partsF = bodies.find(f => f !== logicF && partLines(f.t).ratio >= 0.5) || null;
    const type = role('type') ? oneLine(role('type').t) : '';
    const sp = parseSplit(role('split') ? role('split').t : '');
    const segs = logicF ? segments(logicF.t) : [];
    const logic = fromQingshuang(segBody(segs, '构词逻辑') || (segs[0] && !segs[0].mk ? segs[0].body : ''), word);   // 清爽格式先还原成融合格式
    // 3.7 起（总表“合成规律”轮）：组合列第一行下面的“　合成规律：规律（本词：短语 → 本词；同 例词）”和“　写法：规律（例子、别的写法）”。
    // 规律那句话照维护技能「合成规律一览」，视频照念；括号里第一段是本词的例子（show 取不是“同 …”的前两段）
    const COMP_RX = /^\s*(合成规律|写法)[：:]\s*(.*)$/;
    const comp = clean(logic).split('\n').map(x => COMP_RX.exec(x)).filter(Boolean).map(m => {
      const body = m[2].trim(), i = body.indexOf('（');
      const text = (i >= 0 ? body.slice(0, i) : body).trim();
      const ex = i >= 0 ? body.slice(i + 1).replace(/）\s*$/, '').trim() : '';
      const segs2 = splitTop(ex, '；').map(x => x.trim()).filter(x => x && !/^同\s/.test(x));
      return { kind: m[1], text, ex, show: segs2.slice(0, 2).join('；'), first: segs2[0] || '' };
    });
    // 4.0 起（总表“过去分词”轮）：名词、形容词接在拉丁语过去分词词干上的词，组合列第一行下面有一行“　构词：…”：
    // 前面几句讲这个词是怎么造的（“不接在动词原形上，而是接在过去分词后面”那句是规律），最后一个“：”后面是一步步的链
    // （competere（一起争取）→ 过去分词 competitus → 词干 competit- → competitio）；英语后来自己用 -ation 造的词没有链
    const GOUCI_RX = /^\s*构词[：:]\s*(.*)$/;
    const gm = clean(logic).split('\n').map(x => GOUCI_RX.exec(x)).find(Boolean);
    let gouci = null;
    if (gm) {
      const body = gm[1].trim(), k = body.lastIndexOf('：');
      const chain = k >= 0 && /→/.test(body.slice(k + 1)) ? body.slice(k + 1).trim() : '';
      const head = chain ? body.slice(0, k).trim() : body;
      const sents = head.split(/(?<=[。；])/).map(x => x.trim().replace(/[。；]$/, '')).filter(Boolean);
      const ri = sents.findIndex(x => /不接在动词原形上/.test(x));
      gouci = ri >= 0
        ? { kind: '构词', body, chain, intro: sents.slice(0, ri).join('。'), text: sents[ri], more: sents.slice(ri + 1).join('；'), show: chain, first: '' }
        : { kind: '构词', body, chain, intro: '', text: head, more: '', show: chain, first: '' };
    }
    const firstLine = clean(logic).split('\n')[0] || '';
    const eq = parseEquation(firstLine);
    const steps = stepsOf(logic).slice(0, 4);
    const nowText = segBody(segs, '今义') || (role('meaning') ? fromPosLines(clean(role('meaning').t), role('examples') ? clean(role('examples').t) : '') : '');   // 2026-11 起今义写在总表「含义」列、例子在「例句」列
    const mean = meaningOf(nowText);
    const pl = partsF ? partLines(partsF.t).list : [];
    // 组合列【词性变化】：每个后缀在这个词里怎么用（“在这里”）。三列分工后写在组合列；老表写在各部分解释的后缀行里，照样认
    // 融合格式：【构词逻辑】里等式下面的“词性变化（-ion）：……”；上一版写成【词性变化】一段；老表写在各部分解释的后缀行里
    const posFused = clean(logic).split('\n').map(x => /^\s*词性变化（((?:[^（）]|（[^（）]*）)+)）[：:]\s*(.*)$/.exec(x)).filter(Boolean)
      .map(m => m[1].trim() + '：' + m[2].trim()).join('\n');
    const posList = partLines(posFused).list.concat(partLines(segBody(segs, '词性变化') || '').list);   // partLines：“-et、-in”这种拆成两条
    // 老表里“在这里”跟在后缀行第一句后面：拼回同样的位置，别的说明照旧在后面
    const withHere = (t, h) => {
      if (!h) return t;
      let d = 0, q = 0;
      for (let i = 0; i < t.length; i++) {
        const ch = t[i];
        if (ch === '（' || ch === '(') d++; else if (ch === '）' || ch === ')') d = Math.max(0, d - 1);
        else if (ch === '“') q++; else if (ch === '”') q = Math.max(0, q - 1);
        else if ((ch === '；' || ch === '。') && d === 0 && q === 0) return t.slice(0, i) + h + t.slice(i);
      }
      return t + h;
    };
    const posOf = ex => {
      if (!ex || /在这里：/.test(ex.text)) return '';
      const hit = posList.find(x => x.head === ex.head) || posList.find(x => x.norm && x.norm === ex.norm);
      return hit ? '；在这里：' + hit.text : '';
    };
    const style = prefs.style === 'core' ? 'core' : 'full';
    const famOrigin = originOf(role('bg') ? role('bg').t : '');
    const film = { word, type, kind: sp.kind, style, famOrigin, scenes: [], slots: [], pace: Math.min(1.5, Math.max(0.7, Number(prefs.pace) || 1)) };
    film.comp = comp;
    film.gouci = gouci;
    film.brief = !!prefs.brief;          // 6.19：精简版（run.py 的 --edition）：卡片上不画音变那一行；不要的几幕在 prefs 里写成 false
    // 5.0 起：读音拆分（视频的第一部分）。run.py 按音节划分表算好放在 d.pron：每一块的字母和标注、音标、配音用的音素词；
    // prefs.pron === false 不要这一部分
    film.pron = d.pron && prefs.pron !== false && Array.isArray(d.pron.chunks) && d.pron.chunks.length ? normPron(d.pron) : null;

    // 每个部分：文字、意思（等式括号里的最短，其次各部分解释）、补充一句、图、动法、颜色
    if (sp.kind === 'parts') {
      const match = matchParts(sp.parts, pl);
      film.parts = sp.parts.map((p, i) => {
        const k = normPart(p.text);
        const ex0 = match[i] != null ? pl[match[i]] : null;
        const mm = ex0 ? memoOf(ex0.text) : { memo: null, rest: '' };
        const vb = verbOf(mm.rest);                                              // 6.1：这一行里的“动词变化：…；规律：…”
        const sf0 = shenfenOf(vb.rest);                                          // 6.0：这一行里的“身份：…。分工：…”（词根行；上一版总表的词缀行）
        // 6.2：新写法的词缀行——身份就是开头的介绍（画面上只写第一句和来历），辨析的话当“分工”一条一条读
        const bxNew = !!(ex0 && ex0.idNew);
        const sf = bxNew ? { idt: idtOf(sf0.rest), fg: ex0.bx || '', rest: sf0.rest } : sf0;
        const ex = ex0 ? Object.assign({}, ex0, { text: sf.rest }) : null;       // 解释正文里不带“记：…”“身份、分工”这两段
        const vr = ex ? variantOf(ex.text) : null;                               // 5.11：词根的另一种写法（duct = duc）
        const xt = ex ? xingtaiOf(ex.text, p.text) : null;                       // 6.8：总表“词根形态版”的词根那一格
        const term = eq && eq.terms.length === sp.parts.length ? eq.terms[i] : (eq ? eq.terms.find(t => normPart(t.text) === k) : null);
        // 后缀的意思：第一行等式括号里的，其次后缀等式“X“…”+ -or（做…的人或东西）=“…””里的（派生路线的词第一行看不到后缀的意思），最后才用各部分解释
        const eqGloss = (() => {
          if (!ex || (term && term.gloss)) return '';
          const hit = posList.find(x => x.head === ex.head) || posList.find(x => x.norm && x.norm === ex.norm);
          const m = hit && /加上\s*-[A-Za-z]+\s*（((?:[^（）]|（[^（）]*）)*)）/.exec(hit.text);
          return m ? m[1].trim() : '';
        })();
        const gloss = (term && term.gloss) || p.inline || eqGloss || (ex ? unquote(brief(ex.text, 14)) : '');
        const slot = 'p' + i;
        const g = texts[slot] != null && texts[slot] !== '' ? texts[slot] : gloss;
        const exFull = ex ? withHere(ex.text, posOf(ex)) : '';
        const ic = icons[slot] != null ? icons[slot] : (iconFor(g, '') || iconFor('', p.text) || (ex ? posTarget(exFull) || iconFor(brief(ex.text, 12), '') : ''));
        film.slots.push({ id: slot, label: p.text, icon: ic, text: g, autoText: gloss });
        const mo = motionFor(g || (ex ? ex.text : ''));
        const head = ex ? ex.head : p.text;
        const aff = affixOf(head, p.text, i, sp.parts.length);
        // 来源只看各部分解释那一行（“在这里”是组合列的，和来源无关）；词性牌、“在这里”看拼上组合列那一句的
        const tab = aff && ex ? Object.assign(tableAffix(exFull), { from: affixSource('x：' + ex.text) }) : null;
        return {
          text: p.text, head, gloss: g, sub: ex ? ex.text : '', icon: ic, iconSet: icons[slot] != null,
          motion: mo === 'not' && ['🚫', '❌'].includes(ic) ? 'pop' : mo, color: PART[i % PART.length],
          kind: aff ? aff.kind : (!ROOT_HEADS.has(normPart(head)) && (WORD_HEADS.has(normPart(head)) || (!ROOT_HEADS.has(k) && WORD_HEADS.has(k))) ? 'word' : 'root'), from: aff ? ((tab && tab.from) || aff.from) : '', role: aff ? affRole(aff, tab) : '', tag: aff ? ((tab && tab.tag) || aff.tag) : '',
          ex: aff ? aff.ex : '', here: tab ? tab.here : '', bridge: tab ? tab.bridge || null : null,
          // 4.0 起：拆分写成 competit(=compete)、说明里讲过去分词的部分，是母词的过去分词词干（配音：“就是 compete 的过去分词形式”）
          pp: !aff && p.eq && p.inline && ex && /过去分词|以 -atus 结尾/.test(ex.text) ? p.inline : '',
          memo: mm.memo,
          // 6.0：身份、分工（一条一条）；why：总表里单独一行的“为什么用 -ous 不用 -ful：…”
          idt: sf.idt, fg: sf.fg, bx: bxNew,                                   // 6.2：bx——这一行是“身份 / 记 / 辨析”的新写法（那一幕叫“前缀辨析 / 后缀辨析”）
          // 6.1：拉丁语动词的三个样子和规律（有“分工”的词根才上画面）；verbAt：这一部分的身份对着哪一个样子（inf / pp / ''）
          verb: vb.verb && sf.fg ? vb.verb : (xt ? xt.verb : null), verbAt: vb.verb && sf.fg ? verbSlot(sf.idt) : (xt ? xt.verbAt : ''), xt,
          // 6.2：开头写“= -ous”“= -al”的写法（-ious、-ial、-ar），辨析里讲 -ous、-al 的那一条就是讲它的
          fgRows: sf.fg ? fengongRows(sf.fg, [p.text.replace(/\(.*?\)/g, ''), head], bxNew, bxNew && /^=\s*(-?[A-Za-z]+-?)(?![A-Za-z])/.test(sf.rest) ? /^=\s*(-?[A-Za-z]+-?)/.exec(sf.rest)[1] : '') : [],
          why: (() => {
            const hd = String(head || '').trim();
            if (!hd || !/^-|-$/.test(hd) || !partsF) return null;
            const rx = new RegExp('^(为什么(?:用|是)\\s*' + hd.replace(/[-()]/g, '\\$&') + '(?![A-Za-z])[^：:]*)[：:]\\s*(.*)$');
            for (const l of clean(partsF.t).split('\n')) { const m = rx.exec(l.trim()); if (m) return { q: m[1].trim(), a: m[2].trim() }; }
            return null;
          })(),
          // 5.11：词根的另一种写法：base 词根本身，forms 字母怎么变过来的，howShort 配音念的那半句，rootGloss 词根的意思；
          // pic：这一部分卡片左边自己的画（prefs.partPics.p1：记法里说的东西、这一部分的意思），不写就用自动配的小动画
          base: vr && normPart(vr.base) !== k ? vr.base : '', forms: vr ? vr.forms : [], how: vr ? vr.how : '', howShort: vr ? vr.howShort : '', rootGloss: vr ? vr.gloss : '',
          pic: prefs.partPics && prefs.partPics[slot] ? normPic(prefs.partPics[slot]) : null
        };
      });
      film.parts.forEach(pt => { if (pt.xt) pt.pp = ''; if (pt.pp && !pt.tag) pt.tag = '过去分词词干'; });
      // 6.7：辨析每个用法的演示（d.demo：ety_table.py 带来的演示词材料；prefs.demo === false 都不要）
      const dmat = prefs.demo === false ? null : (d.demo || {}), dpf = prefs.demo && typeof prefs.demo === 'object' ? prefs.demo : {};
      if (dmat) film.parts.forEach(pt => { if (pt.bx) (pt.fgRows || []).forEach(r => (r.uses || []).forEach(u => { const w = u.ex[0]; if (!w || dpf[w] === false) return; u.demo = demoOf(w, dmat[w], dpf[w]); })); });
      // 词根从哪儿来：只有一个词根时，用词族“背景”里写的；手写的 from、role（p0、p1…）为准
      const roots = film.parts.filter(pt => pt.kind === 'root' || pt.kind === 'word');   // 只有一个主体（词根或单词）时用词族“背景”的来源
      if (roots.length === 1 && famOrigin) roots[0].from = famOrigin;
      film.parts.forEach((pt, i) => {
        const k = 'p' + i;
        if (prefs.from && prefs.from[k] != null) pt.from = String(prefs.from[k]);
        if (prefs.role && prefs.role[k] != null) pt.role = String(prefs.role[k]);
      });
      const autoLit = (eq && eq.literal) || '';
      const lit = texts.combo != null && texts.combo !== '' ? texts.combo : autoLit;
      const mh = iconHit(mean.main, ''), lh = iconHit(lit, '');
      const comboIcon = icons.combo != null ? icons.combo : (mh.ic || lh.ic);
      film.combo = { literal: lit, icon: comboIcon, neg: icons.combo == null && (mh.ic ? negated(mean.main, mh.key) : negated(lit, lh.key)) };
      if (eq && eq.route) film.route = eq.route;
      film.slots.push({ id: 'combo', label: '拼起来', icon: comboIcon, text: lit, autoText: autoLit });
      // 单词里哪几个字母属于哪一部分：拼起来正好是这个词（不算大小写、连字符）才能一个个字母对上
      const letters = word.split('');
      // 3.7 起：e 结尾的词加元音开头的后缀，总表拆分写全（make + er、time + ing、see + en），拼的时候前一部分末尾的 e 去掉，
      // 字母照“mak | er”“tim | ing”对：共用的那个 e 算后缀的
      const target = normPart(word);
      let segs = film.parts.map(p => normPart(p.text));
      if (segs.join('') !== target) {
        const adj = segs.slice();
        let acc = '';
        for (let i = 0; i < adj.length; i++) {
          if (i < adj.length - 1 && /e$/.test(adj[i]) && /^[aeiouy]/.test(adj[i + 1]) && !target.startsWith(acc + adj[i] + adj[i + 1].charAt(0))) adj[i] = adj[i].slice(0, -1);
          acc += adj[i];
        }
        if (adj.join('') === target) { segs = adj; film.dropE = true; }   // 拆开的几幕仍照拆分写 make + er（drawBlocks），只有整词上色用 mak | er
        else {
          // 3.8 起：y 变 i、-le 变 -ly、-nt 变 -nce、d 变 s 这类，只有一部分变了样（happy + ness → happi | ness、silent + ce → silen | ce）：
          // 从左、从右照原样对上其余部分，剩下的字母都算给变了样的那一部分
          const n = segs.length;
          let L = 0, a = 0;
          while (L < n - 1 && segs[L] && target.startsWith(segs[L], a)) { a += segs[L].length; L++; }
          let R = 0, z = target.length;
          while (R < n - 1 - L && segs[n - 1 - R] && target.slice(0, z).endsWith(segs[n - 1 - R]) && z - segs[n - 1 - R].length > a) { z -= segs[n - 1 - R].length; R++; }
          if (L + R === n - 1 && z > a) {
            const fixed = segs.slice(); fixed[L] = target.slice(a, z);
            if (fixed.join('') === target) { segs = fixed; film.dropE = true; }
          }
        }
      }
      const flat = segs.join('');
      if (flat && flat === target) {
        const owner = [];
        let pi = 0, used2 = 0;
        for (const ch of letters) {
          if (/[A-Za-z0-9]/.test(ch)) {
            while (pi < film.parts.length && used2 >= segs[pi].length) { pi++; used2 = 0; }
            owner.push(Math.min(pi, film.parts.length - 1));
            used2++;
          } else owner.push(Math.max(0, pi));          // 连字符、撇号跟着前面那一部分
        }
        film.owner = owner;
      }
    } else if (sp.kind === 'variant') {
      film.variant = { from: sp.from, to: sp.to, ops: diffLetters(sp.from, sp.to.replace(/\s+/g, ' ')) };
      // 3.4 起（总表“源头词根”轮）：外来基础词写成“people ← popul”，箭头后面是「词根」列里的源头词根：带上它的意思、来源，配音和小黑板用
      const rk = normPart(sp.from.replace(/\(.*?\)/g, ''));
      const rl = rk && ROOT_HEADS.has(rk) ? pl.find(x => x.norm === rk) : null;
      if (rl) film.variant.root = { text: sp.from.replace(/[()]/g, ''), gloss: brief(String(rl.text).split(/[（(；;，,。]/)[0].trim(), 16), from: affixSource('x：' + rl.text) };
      // 3.5 起：音变列有【字母变化】链的，“怎么变来的”那一幕照这条链一步步变字母（没有链、链写法不对的照旧：直接从 from 变成 to）
      const zf = bodies.find(x => /(^|\n)\s*【字母变化】/.test(x.t));
      const zl = zf ? clean(zf.t).split('\n').find(l => /^\s*【字母变化】/.test(l)) : '';
      if (zl) film.variant.chain = chainOf(zl, word, sp.from);
    } else if (sp.kind === 'related') {
      film.related = sp.items;
      // 3.6 起（总表“字母变化同源词”轮）：rail ≈ rule 这类，音变列有【字母变化】链的，“和谁是一家”那一幕也照链一步步变字母。
      // 链从本词自己的源头写起（regula → *regla → reille → rail）；源头里标蓝的字母取 ① 那一行写的“词根 X-”（没写就不标）
      const zf = bodies.find(x => /(^|\n)\s*【字母变化】/.test(x.t));
      const zt = zf ? clean(zf.t).split('\n') : [];
      const zl = zt.find(l => /^\s*【字母变化】/.test(l)) || '';
      const z1 = zt.find(l => /^\s*①/.test(l)) || '';
      const zr = /词根\s*([A-Za-z]+)-/.exec(z1);
      if (zl) film.relChain = chainOf(zl, word, zr ? zr[1] : '');
    }
    // 这个词自己的那一行解释（基础词、变体讲来历用）
    const own = pl.find(x => x.norm === normPart(word)) || pl[0] || null;
    if (sp.kind !== 'parts') {
      const originText = texts.origin != null && texts.origin !== '' ? texts.origin : (own ? brief(own.text, 46) : (eq && eq.literal) || '');
      // 5.0 起：来历卡片不再按关键词自动配表情（camera 的“拱顶的屋子”被配成一个走路的人）。要配就写 prefs.originPic：
      // 一幅画的就是来历里说的那样东西（拱顶的屋子）；icons.origin 手写的表情照旧认
      const originIcon = icons.origin != null ? icons.origin : '';
      film.origin = { text: originText, icon: originIcon, literal: eq ? eq.literal : '', pic: prefs.originPic ? normPic(prefs.originPic) : null };
      film.slots.push({ id: 'origin', label: sp.kind === 'variant' ? '怎么变来的' : '来历', icon: originIcon, text: originText, autoText: own ? brief(own.text, 46) : '' });
    }
    film.steps = steps;
    const finalText = texts.final != null && texts.final !== '' ? texts.final : mean.main;
    const fh = iconHit(finalText, '');
    const finalIcon = icons.final != null ? icons.final : (fh.ic || (film.combo ? film.combo.icon : ''));
    film.meaning = { main: finalText, second: prefs.second != null ? prefs.second : mean.second, example: prefs.example != null ? prefs.example : mean.example, icon: finalIcon,
      neg: icons.final == null && (fh.ic ? negated(finalText, fh.key) : !!(film.combo && film.combo.neg)) };
    film.slots.push({ id: 'final', label: '现在的意思', icon: finalIcon, text: finalText, autoText: mean.main });
    // 每个意思一幅画（最多 3 幅）：prefs.pics 手写的；没写就按意思里的关键词配一个图
    film.senses = sensesOf(nowText);
    film.pics = Array.isArray(prefs.pics) ? prefs.pics.map(normPic).filter(Boolean).slice(0, 3) : autoPics(film.senses).map(normPic);
    // 6.32：手写的画（prefs.pics）只留「初中含义」里有的意思——一幅画的意思按“、”“；”分开，有一种说法和初中含义里的一字不差就留；
    // 一幅都对不上就留第一幅。去掉的画，演变那几步、例句、总结的卡片跟着去掉（film.picMap：原来第几幅 → 现在第几幅）
    film.picMap = null; film.czDrop = [];
    {
      const czF = prefs.senses !== 'all' ? role0('meaning_cz') : null;
      if (czF && Array.isArray(prefs.pics) && film.pics.length) {
        const its = t => String(t || '').replace(/^[ \t]*(?:modal |aux\. )?[a-z]+\.(?:\s*\/\s*[a-z]+\.)?[ \t]*/gm, '').split(/[\n；;、，,]/).map(x => x.replace(/[①-⑩\s]/g, '').trim()).filter(Boolean);
        const keep = new Set(its(czF.t));
        let idx = film.pics.map((pc, i) => (its(pc.text).some(x => keep.has(x)) ? i : -1)).filter(i => i >= 0);
        if (!idx.length) idx = [0];
        if (idx.length < film.pics.length) {
          film.czDrop = film.pics.filter((pc, i) => !idx.includes(i)).map(pc => String(pc.text || ''));
          film.picMap = {}; idx.forEach((oi, ni) => { film.picMap[oi] = ni; });
          film.pics = idx.map(i => film.pics[i]);
        }
      }
    }
    if (film.combo) film.combo.pic = prefs.comboPic ? normPic(prefs.comboPic) : (film.pics[0] || null);
    // 意思怎么变过来：没手写 evo 的，按总表“构词逻辑”里 → 开头的几行配（结果里正好写着这个意思的那一行最好）
    film.evolution = segBody(segs, '演变');
    const allSteps = stepsOf(logic), pairs = [];
    // 总表各部分解释里的“意思怎么变”（每步标〔用词规律①〕）和“用词规律”：演变链那一步自动挂上规律，小黑板“重点”也用它
    const hLines = partsF ? clean(partsF.t).split('\n').map(x => x.trim()) : [];
    // 三列分工后：规律写在组合列【用词规律】，每一步的〔用词规律①〕标在组合列 → 行末尾；老表写在各部分解释里，照样认
    // 融合格式：用词规律紧跟在用到它的那一步下面（“　用词规律①：……”）；上一版写成【用词规律】一段
    const ruleLines = clean(logic).split('\n').map(x => /^\s*用词规律([①②③④⑤⑥⑦⑧⑨⑩])[：:]\s*(.*)$/.exec(x)).filter(Boolean).map(m => m[1] + ' ' + m[2].trim());
    const ruleBody = ruleLines.length ? ruleLines.join(' ') : segBody(segs, '用词规律');
    const tRules = parseRules(hLines.find(l => /^用词规律[：:]/.test(l)) || (ruleBody ? '用词规律：' + oneLine(ruleBody) : ''));
    const hEvo = hLines.find(l => /^意思怎么变[：:]/.test(l));
    const tEvo = hEvo ? parseEvo(hEvo) : allSteps.map(st => ({ result: st.result, marks: st.marks || [] }));
    const normRes = t => dropParens(oneLine(t)).replace(/\s+/g, '');
    const ruleFor = pc => {
      if (!pc || pc.stepIdx == null || !allSteps[pc.stepIdx]) return { text: '', ex: '' };
      const res = normRes(allSteps[pc.stepIdx].result), st = tEvo.find(x => normRes(x.result) === res);
      const r = st && st.marks.length ? tRules[st.marks[0]] : null;
      if (!r) return { text: '', ex: '' };
      // 精简版总表：规律挂在这一步下面，括号里只留“同 熟悉的例子”；小黑板上把本词的例子补回来（第一个意思 → 这一步的意思）
      let ex = String(r.ex || '').replace(/^同\s*/, '');
      if (!new RegExp('^' + word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i').test(ex)) {
        const to = dropParens(allSteps[pc.stepIdx].result).split(/[；;]/)[0].trim();
        const from = pc.stepIdx > 0 && allSteps[0] ? dropParens(allSteps[0].result).split(/[；;]/)[0].trim() : (film.combo ? film.combo.literal : '');
        if (from && to && from !== to) ex = word + ' ' + from + ' → ' + to + (ex ? '；' + ex : '');
      }
      return { text: r.text, ex };
    };
    const zhOf = t => new Set([...dropParens(t)].filter(c => /[\u3400-\u9fff]/.test(c)));
    film.pics.forEach((pc, i) => {
      if (pc.evo.length || pc.evoSay || !pc.text) return;
      allSteps.forEach((st, j) => {
        const segsR = splitTop(oneLine(st.result), '；').map(x => dropParens(x).trim());
        const at = segsR.findIndex(x => x && (x === pc.text || x.includes(pc.text) || pc.text.includes(x)));
        const a = zhOf(pc.text), b = zhOf(st.result);
        const ov = [...a].filter(c => b.has(c)).length;
        const score = at >= 0 ? 10 - at : ov >= 2 ? ov : 0;
        if (score > 0 && st.text) pairs.push({ i, j, score });
      });
    });
    pairs.sort((a, b) => b.score - a.score);
    const usedStep = new Set(), gotPic = new Set();
    pairs.forEach(({ i, j }) => { if (!usedStep.has(j) && !gotPic.has(i)) { usedStep.add(j); gotPic.add(i); film.pics[i].evo = [dropParens(allSteps[j].text).trim()]; film.pics[i].evoAuto = true; film.pics[i].stepIdx = j; } });
    // 意思是怎么一步步变过来的：一条链，第一个框是字面意思，后面每一步一个框（via 写在箭头旁边：为什么会这样变）。
    // prefs.flow 手写的为准：[{ node, via, pos, pic, from, say }]；没写就用每个意思的 evo 拼（都从字面意思出发）
    const lit0 = film.combo ? film.combo.literal : (film.origin && film.origin.literal) || '';
    const rootNode = lit0 ? '“' + lit0 + '”' : word, CIRC = ['①', '②', '③'];
    let pflow = Array.isArray(prefs.flow) ? prefs.flow : null;
    if (pflow && film.picMap) {             // 6.32：画去掉了的那几步也去掉；通向留下那几步的中间步留着（画也去掉了的，只留字）；①②③ 重新编
      const st = pflow.map(s0 => (typeof s0 === 'string' ? { node: s0 } : Object.assign({}, s0 || {})));
      const par = k => (st[k].from != null && Number(st[k].from) >= 0 && Number(st[k].from) < k ? Number(st[k].from) : k - 1);
      const keep = st.map((s, k) => k === 0 || (s.pic != null && film.picMap[Number(s.pic)] != null));
      for (let k = st.length - 1; k > 0; k--) if (keep[k]) { let q = par(k); while (q > 0 && !keep[q]) { keep[q] = true; q = par(q); } }
      const nm = {}; let c = 0; st.forEach((s, k) => { if (keep[k]) nm[k] = c++; });
      const nPic = st.filter((s, k) => keep[k] && s.pic != null && film.picMap[Number(s.pic)] != null).length;
      let num = 0;
      pflow = st.map((s, k) => {
        if (!keep[k]) return null;
        const o = Object.assign({}, s);
        if (k > 0) { let q = par(k); while (q > 0 && !keep[q]) q = par(q); o.from = nm[q] != null ? nm[q] : 0; }
        const pk = o.pic != null ? film.picMap[Number(o.pic)] : null;
        o.pic = pk != null ? pk : null;
        if (k > 0 && o.node) { const bare = String(o.node).replace(/^[①-⑩]\s*/, ''); o.node = o.pic != null && nPic > 1 ? '①②③④⑤'[num++] + ' ' + bare : bare; }
        return o;
      }).filter(Boolean);
    }
    if (Array.isArray(pflow) && pflow.length >= 2) {
      film.flow = pflow.map((s0, k) => {
        const s = typeof s0 === 'string' ? { node: s0 } : (s0 || {});
        return { node: String(s.node || (k === 0 ? rootNode : '')), via: String(s.via || ''), pos: String(s.pos || ''), say: Array.isArray(s.say) ? s.say.join('') : String(s.say || ''),
          sayList: Array.isArray(s.say) ? s.say.map(String).filter(Boolean) : null,
          pic: s.pic != null && film.pics[Number(s.pic)] ? Number(s.pic) : null, from: s.from != null ? Number(s.from) : null, root: k === 0,
          icons: String(s.icons || '').trim().split(/\s+/).filter(Boolean).slice(0, 4), rule: String(s.rule || ''), ruleEx: String(s.ruleEx || ''),
          fig: s.fig ? normPic(s.fig) : null, cap: String(s.cap || '') };
      }).filter(s => s.node).slice(0, 7);
    } else if (film.pics.some(pc => pc.evo.length)) {
      const np = film.pics.length;
      film.flow = [{ node: rootNode, via: '', pos: '', say: '', pic: null, from: null, root: true }].concat(film.pics.map((pc, i) => ({
        node: (np > 1 ? CIRC[i] + ' ' : '') + pc.text, via: pc.evo.join('，'), pos: pc.pos, say: pc.evoSay, pic: i, from: 0, root: false, icons: [], rule: ruleFor(pc).text, ruleEx: ruleFor(pc).ex })));
    }
    // 英语的用词规律（“表示动作的词，常常也拿来叫做这件事用的东西”）：flow 里某一步的 rule，加上 prefs.rules；写上小黑板当重点
    film.rules = (film.flow || []).filter(s => s.rule).map(s => ({ text: s.rule, ex: s.ruleEx }))
      .concat((Array.isArray(prefs.rules) ? prefs.rules : []).map(r => (typeof r === 'string' ? { text: r, ex: '' } : { text: String((r || {}).text || ''), ex: String((r || {}).ex || '') })))
      .filter(r => r.text).slice(0, 2);
    // 同一条规律只写一次（手写 flow 的 rule 常带“英语里，”“常常”，总表里的不带）
    // 括号里的举例（“（电脑、法律、体育、音乐……）”）不算：手写 flow 的规律常把它省掉，总表里的带着
    const sameRule = (a, b) => { const n = t => dropParens(String(t || '')).replace(/^英语里[，,]\s*/, '').replace(/常常/g, '').replace(/[\s“”"，,。]/g, ''); return n(a) === n(b); };
    film.rules = film.rules.filter((r, i) => !film.rules.slice(0, i).some(x => sameRule(x.text, r.text)));
    // 6.32：去掉了的意思（初中含义里没有），总表里讲它的用词规律也不上小黑板（规律或例子里有那个意思特有的两个字）
    const dropBi = new Set(), keptTxt = (film.pics || []).map(pc => String(pc.text || '')).join('|');
    (film.czDrop || []).forEach(t => { const z = String(t).replace(/[^\u4e00-\u9fff]/g, ''); for (let k = 0; k < z.length - 1; k++) { const b = z.slice(k, k + 2); if (!keptTxt.includes(b)) dropBi.add(b); } });
    const aboutDropped = r => { const s = String(r.text || '') + String(r.ex || ''); for (const b of dropBi) if (s.includes(b)) return true; return false; };
    Object.values(tRules).forEach(r => { if (film.rules.length < 2 && r.text && !aboutDropped(r) && !film.rules.some(x => sameRule(x.text, r.text))) film.rules.push({ text: r.text, ex: r.ex }); });
    // 3.7 起：合成规律写上小黑板“重点”第一条；带连字符的词（或写法有讲头的：连写分开写意思不同、掉字母）把写法也写上；重点最多两条
    const COMP_PLAIN = /^(合成词常走分开写、加连字符、连写这条路|专有名词首字母大写)/;
    const mainComp = film.comp.find(x => x.kind === '合成规律');
    const spellComp = film.comp.find(x => x.kind === '写法' && (/[-'’]/.test(word) || !COMP_PLAIN.test(x.text)));
    if (prefs.compRules !== false) {
      if (mainComp && !film.rules.some(x => sameRule(x.text, mainComp.text))) film.rules = [{ text: mainComp.text, ex: mainComp.first }].concat(film.rules).slice(0, 2);
      if (spellComp && film.rules.length < 2) film.rules.push({ text: spellComp.text, ex: spellComp.first });
      film.compShow = [mainComp, spellComp].filter(Boolean);
    } else film.compShow = [];
    // 4.0 起：“构词”那一行也上这一幕（一张绿卡“★ 构词”：中间是规律，下面小字是链），并写上小黑板“重点”第一条；prefs 写 "gouci": false 不要
    if (film.gouci && prefs.gouci !== false) {
      film.compShow = [film.gouci].concat(film.compShow || []).slice(0, 2);
      if (!film.rules.some(x => sameRule(x.text, film.gouci.text))) film.rules = [{ text: film.gouci.text, ex: film.gouci.chain }].concat(film.rules).slice(0, 2);
    }
    // 小黑板的扩展词：都在总表里（ety_table.py 挑好、run.py 核对过）；prefs.extend 手写的为准，false 表示不要
    const dext = Array.isArray(d.extend) ? d.extend : [];
    let ext = Array.isArray(prefs.extend) ? prefs.extend.map(x => (typeof x === 'string' ? { w: x } : x || {})) : dext.filter(x => x.pick);
    ext = ext.map(x => {
      const c = dext.find(y => y.w.toLowerCase() === String(x.w || '').toLowerCase());
      return { w: String(x.w || ''), m: x.m || (c && c.m) || (d.family_meanings || {})[x.w] || '', share: x.share != null ? x.share : (c ? c.share : '') };
    }).filter(x => x.w);
    film.extend = prefs.extend === false ? [] : ext.slice(0, 6);
    // 同一词族：挑带着共同部分的词，最多 8 个
    const fam = (d.family || []).filter(w => w !== word);
    if (fam.length) {
      const cands = (film.parts || []).map(p => p.text.toLowerCase().replace(/\([^()]*\)/g, '')).filter(x => x.length >= 3)
        .concat(sp.kind !== 'parts' && d.family[0] ? [String(d.family[0]).toLowerCase()] : []);
      let shared = '', n = 0;
      for (const c of cands) {
        const k = fam.filter(w => w.toLowerCase().includes(c)).length;
        if (k > n || (k === n && c.length > shared.length)) { shared = c; n = k; }
      }
      if (!n) shared = '';
      let sorted = fam.filter(w => shared && w.toLowerCase().includes(shared)).concat(fam.filter(w => !(shared && w.toLowerCase().includes(shared))));
      const ranked = dext.filter(x => x.via === 'group').map(x => x.w).filter(w => fam.includes(w));
      if (ranked.length) sorted = ranked.concat(sorted.filter(w => !ranked.includes(w)));
      const pi = film.parts ? film.parts.findIndex(p => p.text.toLowerCase().replace(/\([^()]*\)/g, '') === shared) : -1;
      film.family = { words: sorted.slice(0, 8), more: Math.max(0, fam.length - 8), total: fam.length, shared, color: pi >= 0 ? film.parts[pi].color : C.board };
      // 换掉自动挑的：给哪几个词、标出哪一段、标题怎么写
      if (Array.isArray(prefs.familyWords) && prefs.familyWords.length) {
        film.family.words = prefs.familyWords.slice(0, 8);
        film.family.more = Math.max(0, fam.length - film.family.words.length);
      }
      if (prefs.familyShared != null) film.family.shared = String(prefs.familyShared).toLowerCase();
      if (prefs.familyTitle) film.family.title = prefs.familyTitle;
    }
    // 来历路线（com + mun → common → communicate → communication）：数据里的“派生路线”，或者自己写的
    if (Array.isArray(prefs.route) && prefs.route.length >= 2) film.route = prefs.route.map(x => ({ text: String(x.text || ''), gloss: String(x.gloss || ''), icon: x.icon != null ? String(x.icon) : undefined }));
    // 小黑板：结尾的总结，方便抄写
    film.dist = distOf(d, film, prefs, role);
    film.kd = kaodianOf(role('kaodian'), prefs);
    if (film.kd) film.kd.pages = kdPages(film.kd.rows, prefs.kaodian);   // 6.31：内容多分两页
    film.lx = lianxiOf(d, film, prefs, role);                               // 6.13：“练习”那一部分（考点后面、总结前面）                           // 6.11：“考点”那一部分（总结前面）                                // 6.0：第三部分“同义词辨析”讲什么（总结页的“辨”一行也用它）
    if (prefs.board) film.board = boardLines(film, d, prefs.board === true ? {} : prefs.board);
    // 6.31（第七十五版，用户：“最后的总结不要一点点的显示出来，直接把画面放出来就可以了”）：总结两页整页一起出来（淡入 0.4 秒），
    // 不再一行一行写、一张一张贴；想要原来一行一行写的，画面设置写 "board": {"reveal": true}
    if (film.board) film.board.whole = !(prefs.board && prefs.board.reveal === true);

    // 时间线（秒）；pace 调快慢
    const skip = new Set(Array.isArray(prefs.skip) ? prefs.skip : []);      // 不要的几幕（steps、family、route…；part1 去掉第二张卡片）
    if (style === 'core') {                                                  // 只讲核心：意思怎么变过来、同一词族不要；来历手写了才要
      skip.add('steps'); skip.add('family');
      if (!(Array.isArray(prefs.route) && prefs.route.length >= 2)) skip.add('route');
    }
    const add = (id, dur, extra) => {
      if (skip.has(id) || (extra && extra.i != null && skip.has(id + extra.i))) return;
      film.scenes.push(Object.assign({ id, dur: dur / film.pace }, extra || {}));
    };
    // 6.0：这段视频分几部分：读音拆分（有读音数据才有）、含义拆分、同义词辨析（辨析列里有能比的词才有）、总结。
    // 只有“含义拆分 + 总结”两部分时和以前一样不出分段标题
    film.sections = [];
    const addSec = name => film.sections.push({ name, sub: SEC_DEF[name][1], color: SEC_C[SEC_DEF[name][0]] });
    if (film.pron) addSec('读音拆分');
    addSec('含义拆分');
    if (film.dist) addSec('同义词辨析');
    if (film.kd) addSec('考点');
    if (film.board) addSec('总结');
    if (film.lx) addSec('练习');                                            // 6.16：练习挪到总结后面、答案前面（用户：“视频里把练习部分放在最后，答案的前面；就是把单词的一套全部讲解完了，再最后做练习”）
    if (film.lx) addSec('答案');                                            // 6.15：练习的答案放在视频最后（总结后面）
    film.sections.forEach((x, i) => { x.no = SEC_NO[i]; });
    film.showSec = !!(film.pron || film.dist || film.kd || film.lx);
    const secI = name => film.sections.findIndex(x => x.name === name);
    const fgOff = i => prefs.fengong === false || (prefs.fengong && prefs.fengong['p' + i] === false);
    film.cover = prefs.cover !== false;                                     // 6.27：开头一幕画成封面（单词 + 含义 + 第一个意思的画）
    film.duyin = film.pron && prefs.duyin !== false ? duyinOf((role('duyin') || {}).t) : [];
    {   // 6.26.2：精简版最多讲 2 个读音现象（用户：“视频里面解释要尽量抓住重点，要不然视频就很长了”），按重要的先留，画面上照字母先后讲
      const cap = Number(prefs.duyinMax) || (prefs.brief ? 2 : 4);
      if (film.duyin.length > cap) {
        const PRI = ['清辅音浊化', '读 /ʃ/', '读 /ʒ/', '读 /dʒ/', '读 /tʃ/', 'x 读', 'n 读', 'ch 读', 'gh 读', '不发音', 'o 读', 'w', 's 读 /z/', '失去爆破'];
        const rank = x => { const k = PRI.findIndex(q => x.tag.includes(q)); return k < 0 ? 99 : k; };
        const keep = film.duyin.map((x, i) => [x, i]).sort((a, b) => rank(a[0]) - rank(b[0]) || a[1] - b[1]).slice(0, cap).map(z => z[1]).sort((a, b) => a - b);
        film.duyin = keep.map(i => film.duyin[i]);
      }
    }
    if (film.pron && film.duyin.length && Array.isArray(film.pron.note)) {    // 6.26：关键解释（d u 读 /dʒu/）和读音现象讲的是同一处，只留读音现象那一条（有“为什么”）
      const keys = film.duyin.map(x => x.letters.replace(/\s+/g, '').toLowerCase());
      film.pron.noteKeep = film.pron.note.map((ln, i) => i).filter(i => !keys.includes(String(film.pron.note[i]).split(/[：:读]/)[0].replace(/[\s_\-]/g, '').toLowerCase()));
      film.pron.note = film.pron.noteKeep.map(i => film.pron.note[i]);
    }
    add('title', 2.6);
    if (film.pron) {                                                         // 5.0 起：一、读音拆分
      const nr = Math.max(1, film.pron.read.length);
      add('sec', 1.9, { i: 0 });
      add('syl', 1.6 + 1.1 * nr + (nr > 1 ? 2.2 : 0.6) + (film.pron.stress >= 0 && nr > 1 ? 1.4 : 0));
      if (film.pron.note.length) add('sylnote', 1.2 + 3.4 * film.pron.note.length);
      film.duyin.forEach((x, i) => add('duyin', film.brief ? 4.5 : 9, { i }));      // 6.33：精简版只讲现象，短一些               // 6.26：读音现象，一个一幕
      add('sec', 1.9, { i: 1 });                                             // 二、含义拆分
    } else if (film.showSec) add('sec', 1.9, { i: secI('含义拆分') });
    if (film.parts) {
      add('split', 2.2);
      film.parts.forEach((p, i) => {
        const shw = p.memo && p.memo.shift && p.memo.shift.why && !prefs.brief ? p.memo.shift : null, yb = shw ? yinbianOf(shw) : null;
        add('part', 3.1 + (shw && !yb ? 3.4 : 0), { i });      // 6.5：音变的原因多一句（6.6：新写法的原因挪到下一幕）
        // 6.6：音变的原因单独一幕“为什么 p 会变成 f？”（总表原因里有“；发音：”的才有）；prefs 写 "yinbian": false 或 {"p0": false} 不要
        if (yb && !(prefs.yinbian === false || (prefs.yinbian && prefs.yinbian['p' + i] === false))) add('yinbian', 3.0 + 4.8 * yb.steps.length, { i });
        // 6.8：词根的“形态”一幕（总表“词根形态版”）；prefs 写 "xingtai": false 或 {"p1": false} 不要
        if (p.xt && p.xt.forms.length >= 2 && !(prefs.xingtai === false || (prefs.xingtai && prefs.xingtai['p' + i] === false))) add('xingtai', 2.6 + p.xt.forms.reduce((a, fm) => a + 3.4 + (fm.uses.length ? 3.0 : 0), 0), { i });
        // 6.0：这一部分有“分工”的（同一个词根的几种写法、意思相近的词缀），卡片后面多一幕“身份和分工”
        if (p.fgRows && p.fgRows.length && !fgOff(i)) {
          p.fgSay = fengongPick(p); p.rel = relPick(p);
          // 6.4：词根的另一种写法（duce = 词根 duc）后面有这一幕的，“字母变化”在这一幕讲，卡片上不写
          const varHere = !!p.base && p.forms.length >= 2 && !p.pp && !(p.bx && (p.kind === 'pre' || p.kind === 'suf')), n0 = film.scenes.length;
          p.vplan = p.verb ? verbPlan(p) : null;                              // 6.5：三个样子一栏一栏讲，分工接在各自那一栏下面
          const nDemo = p.bx ? p.fgSay.reduce((a, k) => a + ((p.fgRows[k].uses || []).filter(u => u.demo).slice(0, 2).length), 0) : 0;      // 6.7：每个演示多 2 秒
          add('fengong', 2.4 + 2.8 * p.fgSay.length + 2.0 * nDemo + (p.rel.length ? 3.6 : 0) + (p.why ? 3.2 : 0) + (p.vplan ? 2.4 * p.vplan.nRules : 0), { i });
          p.varInFg = false && varHere && n0;                                 // 6.5：字母变化放回卡片（用户：“字母变化放到词根特写里面”）
        }   // 6.3：有“关系”的多 3.6 秒   // 6.1：有“三个样子”的多 6 秒
      });
      add('combo', 3.6);
      if (film.route && film.route.length >= 2 && (film.parts.some(pt => pt.gloss) || prefs.route)) add('route', 1.2 + 1.4 * Math.min(4, film.route.length));
    } else if (film.variant) add('variant', film.variant.chain ? 2.6 + 1.6 * film.variant.chain.steps.length : 4.4);   // 3.5 起：有字母变化链的，每一步 1.6 秒
    else if (film.related) add('related', film.relChain ? 2.6 + 1.6 * film.relChain.steps.length : 3.8);   // 3.6 起：≈ 的词有字母变化链的，每一步 1.6 秒
    else add('origin', 4.2);
    if (film.compShow && film.compShow.length) add('rule', 1.6 + 2.8 * film.compShow.length);   // 3.7 起：合成规律、写法，一条一张卡
    if (steps.length) add('steps', 1.3 + 2.0 * steps.length);
    if (film.meaning.main || film.pics.length) add('meaning', 3.6 + 1.4 * Math.max(0, film.pics.length - 1) + (film.pics.some(x => x.diff || x.pos) && film.pics.length > 1 ? 4 : 0));
    if (film.flow && film.flow.length >= 2) add('evolve', 2.0 + 2.6 * (film.flow.length - 1));
    film.pics.forEach((pc, i) => { if (pc.ex) add('example', 5.6, { i }); });
    if (film.family && film.family.words.length) add('family', 3.6);
    if (film.dist) {                                                         // 6.0：三、同义词辨析
      add('sec', 1.9, { i: secI('同义词辨析') });
      add('distinguish', 2.6 + 3.4 * film.dist.items.length + (film.dist.logic ? 4.2 : 0));
    }
    if (film.kd) {                                                           // 6.11：考点（总结前面）
      add('sec', 1.9, { i: secI('考点') });
      if (film.kd.pages.length > 1) film.kd.pages.forEach((pg, i) => add('kaodian', 2.4 + 3.6 * pg.length, { i }));   // 6.31：两页（kaodian0、kaodian1）
      else add('kaodian', 2.4 + 3.6 * film.kd.rows.length);
    }
    if (film.board && film.showSec) add('sec', 1.9, { i: secI('总结') });   // 总结（6.16 起在练习前面）
    if (film.board && film.board.pages === 2) {                              // 6.1：内容多，总结分两页——第一页只写字，第二页每个意思一行；视频停在第二页
      add('board', 4.6 + 0.55 * film.board.lines.length + (film.board.combo && film.combo && film.combo.pic ? 1.2 : 0) + (film.board.lines.some(l => l.hl) ? 1.2 : 0));
      add('board2', 6.4 + 1.7 * (film.board.cards2 || []).length);
    } else if (film.board) add('board', 9.0 + 1.8 * (film.board.cards || []).length + (film.board.combo && film.combo && film.combo.pic ? 1.2 : 0) + (film.board.lines.some(l => l.hl) ? 1.2 : 0)); else add('end', 3.0);
    if (film.lx) {                                                           // 6.13：练习（5 道题，一题一幕）；6.16 起挪到总结后面、答案前面
      add('sec', 1.9, { i: secI('练习') });
      film.lx.qs.forEach((q, i) => add('lianxi', 2.6 + (q.listen ? 5.0 : 0) + q.wait + 0.8, { i }));      // 6.15：只出题，不出答案
    }
    if (film.lx) {                                                           // 6.15：七、答案（视频最后，6.16 起在练习后面；一题一幕：答案 + 讲解）
      add('sec', 1.9, { i: secI('答案') });
      film.lx.qs.forEach((q, i) => add('daan', 6.0 + (q.listen ? 1.0 : 0), { i }));
    }
    let t0 = 0;
    for (const s of film.scenes) { s.t0 = t0; t0 += s.dur; }
    film.total = t0;
    return film;
  }

  // ---------------------------------------------------------------- 画
  const clamp = (x, a, b) => Math.max(a === undefined ? 0 : a, Math.min(b === undefined ? 1 : b, x));
  const span = (p, a, b) => clamp((p - a) / (b - a));
  const lerp = (a, b, k) => a + (b - a) * k;
  const easeOut = k => 1 - Math.pow(1 - k, 3);
  const easeInOut = k => (k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2);
  const easeBack = k => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(k - 1, 3) + c1 * Math.pow(k - 1, 2); };

  function rr(ctx, x, y, w, h, r) {
    r = Math.min(r, w / 2, h / 2);
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
  }
  function setFont(ctx, size, family, weight) { ctx.font = (weight || 'normal') + ' ' + Math.round(size) + 'px ' + family; }
  function txt(ctx, s, x, y, o) {
    o = o || {};
    setFont(ctx, o.size || 32, o.family || ZH, o.weight);
    ctx.fillStyle = o.color || C.ink;
    ctx.textAlign = o.align || 'left';
    ctx.textBaseline = o.base || 'alphabetic';
    const a = ctx.globalAlpha;
    if (o.alpha != null) ctx.globalAlpha = a * o.alpha;
    ctx.fillText(s, x, y);
    ctx.globalAlpha = a;
  }
  // 换行：中文一个字一个字断，英文按词断
  const NO_START = /^[”’）)】」』，。、；：！？…%,.;:!?]/, NO_END = /[“‘（(【「『]$/;
  function wrap(ctx, s, maxW, maxLines) {
    const tokens = String(s || '').match(/[A-Za-z0-9'’.\-]+\s*|[\s\S]/g) || [];
    const lines = [];
    let cur = '';
    for (const tk of tokens) {
      if (tk === '\n') { lines.push(cur); cur = ''; continue; }
      if (ctx.measureText(cur + tk).width > maxW && cur && !NO_START.test(tk)) {
        let carry = '';
        while (cur && NO_END.test(cur)) { carry = cur.slice(-1) + carry; cur = cur.slice(0, -1); }   // “（ 跟着下一行走
        lines.push(cur.trimEnd());
        cur = carry + tk.trimStart();
      } else cur += tk;                 // ）”，。不放到行首：宁可这一行稍微长一点
    }
    if (cur) lines.push(cur);
    if (maxLines && lines.length > maxLines) {
      const kept = lines.slice(0, maxLines);
      let last = kept[maxLines - 1];
      while (last && ctx.measureText(last + '…').width > maxW) last = last.slice(0, -1);
      kept[maxLines - 1] = last + '…';
      return kept;
    }
    return lines;
  }
  function para(ctx, s, x, y, maxW, o) {
    o = o || {};
    setFont(ctx, o.size || 30, o.family || ZH, o.weight);
    const lines = wrap(ctx, s, maxW, o.maxLines || 3);
    const lh = (o.size || 30) * (o.lh || 1.45);
    lines.forEach((ln, i) => txt(ctx, ln, x, y + i * lh, o));
    return lines.length * lh;
  }
  // 字号：放得下为止
  function fit(ctx, s, family, weight, size, maxW, min) {
    let z = size;
    setFont(ctx, z, family, weight);
    while (z > (min || 12) && ctx.measureText(s).width > maxW) { z -= 2; setFont(ctx, z, family, weight); }
    return z;
  }
  // 一行放不下：先缩字号，缩到最小还放不下就在末尾加“…”
  function fitLine(ctx, s, family, weight, size, maxW, min) {
    const z = fit(ctx, s, family, weight, size, maxW, min);
    setFont(ctx, z, family, weight);
    let t = String(s || '');
    if (ctx.measureText(t).width > maxW) { while (t && ctx.measureText(t + '…').width > maxW) t = t.slice(0, -1); t += '…'; }
    return { z, t };
  }
  function emoji(ctx, ic, x, y, size, alpha) {
    if (!ic) return;
    const a = ctx.globalAlpha;
    if (alpha != null) ctx.globalAlpha = a * alpha;
    if (/^[\u3400-\u9fff]+$/.test(ic)) {           // 词性小牌子（名词、形容词…）
      setFont(ctx, size * 0.34, ZH, 'bold');
      const w = ctx.measureText(ic).width + size * 0.3, h = size * 0.56;
      rr(ctx, x - w / 2, y - h / 2, w, h, h * 0.25);
      ctx.fillStyle = C.warm; ctx.fill();
      ctx.lineWidth = 2; ctx.strokeStyle = '#D9C59A'; ctx.stroke();
      txt(ctx, ic, x, y + 1, { size: size * 0.34, weight: 'bold', color: '#6E5520', align: 'center', base: 'middle' });
    } else {
      const im = emojiImg(ic);
      if (im) ctx.drawImage(im, x - size * 0.56, y - size * 0.52, size * 1.12, size * 1.12);
      else {
        setFont(ctx, size, EMOJI);
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillStyle = C.ink;
        ctx.fillText(ic, x, y + size * 0.04);
      }
    }
    ctx.globalAlpha = a;
  }
  // 立体彩色表情图（render.py / preview.py 用 emoji3d.py 下载好，useImages 传进来）；没有就用字体里的表情
  const IMGS = {};
  function emojiImg(ic) {
    const im = IMGS[ic] || IMGS[String(ic).replace(/\uFE0F/g, '')];
    return im && im.complete && im.naturalWidth ? im : null;
  }
  function useImages(map) {
    const jobs = [];
    if (typeof Image === 'undefined') return Promise.resolve();
    for (const [k, url] of Object.entries(map || {})) {
      if (IMGS[k] || !url) continue;
      const im = new Image();
      im.src = url;
      IMGS[k] = im;
      jobs.push(im.decode ? im.decode().catch(() => {}) : new Promise(r => { im.onload = im.onerror = r; }));
    }
    return Promise.all(jobs);
  }
  // 图上画一道红杠（“不快乐的”：笑脸 + 红杠）
  function slash(ctx, x, y, size, k) {
    if (k <= 0) return;
    ctx.save();
    ctx.strokeStyle = C.red; ctx.lineWidth = Math.max(6, size * 0.07); ctx.lineCap = 'round';
    ctx.beginPath(); ctx.arc(x, y, size * 0.6, -Math.PI / 2, -Math.PI / 2 + k * Math.PI * 2); ctx.stroke();
    if (k > 0.6) { const r = size * 0.42, z = span(k, 0.6, 1); ctx.beginPath(); ctx.moveTo(x - r, y - r); ctx.lineTo(lerp(x - r, x + r, z), lerp(y - r, y + r, z)); ctx.stroke(); }
    ctx.restore();
  }
  // 没有图的部分：用这一部分的字母做一个圆牌
  function badge(ctx, s, x, y, size, color, alpha) {
    const a = ctx.globalAlpha;
    if (alpha != null) ctx.globalAlpha = a * alpha;
    ctx.beginPath(); ctx.arc(x, y, size * 0.5, 0, Math.PI * 2);
    ctx.fillStyle = tint(color, 0.85); ctx.fill();
    ctx.lineWidth = 3; ctx.strokeStyle = color; ctx.stroke();
    const z = fit(ctx, s, EN, 'bold', size * 0.42, size * 0.8, 14);
    txt(ctx, s, x, y + 2, { size: z, family: EN, weight: 'bold', color, align: 'center', base: 'middle' });
    ctx.globalAlpha = a;
  }
  function icon(ctx, p, x, y, size, alpha) {
    if (p.flip) {           // 左右翻过来（方向类动作里的小人要朝着走的方向）
      ctx.save(); ctx.translate(x, y); ctx.scale(-1, 1);
      if (p.icon) emoji(ctx, p.icon, 0, 0, size, alpha); else badge(ctx, p.text, 0, 0, size, p.color || C.board, alpha);
      ctx.restore(); return;
    }
    if (p.icon) emoji(ctx, p.icon, x, y, size, alpha); else badge(ctx, p.text, x, y, size, p.color || C.board, alpha);
  }

  // ---------------------------------------------------------------- 一幅画（每个意思一幅、拼起来以后一幅）：画出来的背景 + 会动的角色
  // pic = { text, en, bg, tint, items: [{ e, x, y, s, flip, go: [x2, y2], arc, loop, dur, delay, anim, say, rot }], not, img }
  // x、y 是角色中心在画里的位置（0～1），s 是角色高度占画高的比例；go 是走到哪儿，anim：bob 轻轻上下 / ride 颠簸 /
  // pulse 一大一小 / spin 转圈 / shake 抖动 / swing 摇摆 / none；say：头上冒一个说话的气泡
  function normPic(x) {
    if (!x) return null;
    if (typeof x === 'string') x = { items: x };
    const pic = { text: String(x.text || ''), en: String(x.en || ''), bg: String(x.bg || 'plain'), tint: String(x.tint || ''), not: !!x.not, img: x.img ? String(x.img) : '', auto: !!x.auto,
      pos: String(x.pos || ''), diff: String(x.diff || ''), ex: String(x.ex || ''), exzh: String(x.exzh || ''),
      evo: (Array.isArray(x.evo) ? x.evo : x.evo ? [x.evo] : []).map(String).filter(Boolean), evoSay: String(x.evoSay || '') };
    if (x.exPic) pic.exPic = normPic(x.exPic);
    pic.flash = (Array.isArray(x.flash) ? x.flash : x.flash != null ? [x.flash] : []).map(Number).filter(Number.isFinite);   // 第几秒闪一下（拍照的闪光）
    pic.beat = Number(x.beat) || 0;                                  // 6.25：这幅画的节拍（每分钟几拍）：音箱一鼓一鼓、音符、跳动的柱子都踩它
    let items = x.items;
    if (typeof items === 'string') items = items.trim().split(/\s+/).filter(Boolean);
    if (!Array.isArray(items)) items = [];
    const n = items.length;
    pic.items = items.map((it, i) => {
      if (typeof it === 'string') it = { e: it, x: n === 1 ? 0.5 : 0.22 + 0.56 * i / Math.max(1, n - 1), y: 0.56, s: n === 1 ? 0.6 : n === 2 ? 0.46 : 0.36 };
      return Object.assign({ x: 0.5, y: 0.55, s: 0.34 }, it, { e: String((it && it.e) || '') });
    }).filter(it => it.e || it.svg || it.img || it.ray || it.label != null || it.shape || it.waves || it.eq || it.beam || it.emit || it.sound);   // 6.28：只出声的一条也留着   // 6.25：声波、跳动的柱子、光柱也留着
    return pic;
  }
  // 5.0 起：读音拆分的数据（run.py 用 syllables.py 按音节表算好）：每一块的字母和标注（silent 不发音、u 固定组合、
  // k = long 读字母音 / special 特殊读音）、这一块的音标、配音用的音素词；ok = false 时对不齐，只念整词
  function normPron(p) {
    const chunks = p.chunks.map(c => ({ t: String(c.t || ''), ipa: String(c.ipa || ''), key: String(c.key || ''), mute: !!c.mute, sep: !!c.sep,
      L: (c.L || []).map(x => ({ c: String(x.c || ''), silent: !!x.silent, u: Number(x.u) || 0, k: String(x.k || '') })) }));
    const ok = !!p.ok;
    // 一块一块念：对得齐才念；“不单独发音”的块（mo + re 的 re，英音 r 不读）跟着前一块亮，不单独念
    const read = ok ? chunks.map((c, i) => (!c.sep && !c.mute && c.key ? i : -1)).filter(i => i >= 0) : [];
    return { chunks, ok, read, stress: ok && Number.isFinite(Number(p.stress)) ? Number(p.stress) : -1, ipa: ok ? String(p.ipa || '') : '',
      key: String(p.key || ''), note: (p.note || []).map(String).filter(Boolean).slice(0, 3), marks: p.marks || {}, src: String(p.src || '') };
  }
  function autoPics(senses) {
    const out = [];
    for (const s of senses) {
      if (s.rare) continue;
      const h = iconHit(s.text, '');
      if (!h.ic || /^[\u3400-\u9fff]+$/.test(h.ic) || ['🚫', '❌', '👍', '👎', '➕', '➖'].includes(h.ic) || (h.key.length === 1 && !s.text.startsWith(h.key))) continue;
      out.push({ text: s.text, en: s.en, pos: s.pos, diff: '', ex: s.ex, exzh: s.exzh, bg: 'plain', tint: ['warm', 'blue', 'green'][out.length], not: negated(s.text, h.key), auto: true, items: [{ e: h.ic, x: 0.5, y: 0.56, s: 0.6 }] });
      if (out.length >= 3) break;
    }
    return out;
  }
  const BG = {};
  const TINTS = { warm: ['#FFF6DD', '#FFD9AE'], blue: ['#EAF6FF', '#B9DCF7'], green: ['#EEFBE7', '#C2E8AE'], pink: ['#FFF0F4', '#F9C6D5'], purple: ['#F3EEFF', '#D3C4F6'] };
  function lin(ctx, y0, y1, c0, c1) { const g = ctx.createLinearGradient(0, y0, 0, y1); g.addColorStop(0, c0); g.addColorStop(1, c1); return g; }
  function skyFill(ctx, x, y, w, h, top, bot) { ctx.fillStyle = lin(ctx, y, y + h, top, bot); ctx.fillRect(x, y, w, h); }
  function dot(ctx, cx, cy, r) { ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.fill(); }
  function sunAt(ctx, cx, cy, r) {
    const g = ctx.createRadialGradient(cx, cy, r * 0.3, cx, cy, r * 2.6);
    g.addColorStop(0, 'rgba(255,233,140,.85)'); g.addColorStop(1, 'rgba(255,233,140,0)');
    ctx.fillStyle = g; dot(ctx, cx, cy, r * 2.6);
    ctx.fillStyle = '#FFD23F'; dot(ctx, cx, cy, r);
  }
  function cloudAt(ctx, cx, cy, r) {
    ctx.fillStyle = 'rgba(255,255,255,.95)';
    [[0, 0, 1], [-0.95, 0.3, 0.68], [0.95, 0.3, 0.72], [0.4, -0.4, 0.7], [-0.4, -0.25, 0.62]].forEach(([dx, dy, k]) => dot(ctx, cx + dx * r, cy + dy * r, r * k));
  }
  function hillsAt(ctx, x, y, w, h, gy, c1, c2) {
    ctx.fillStyle = c1;
    ctx.beginPath(); ctx.moveTo(x, y + h * (gy - 0.1));
    ctx.bezierCurveTo(x + w * 0.22, y + h * (gy - 0.3), x + w * 0.42, y + h * (gy - 0.04), x + w * 0.6, y + h * (gy - 0.16));
    ctx.bezierCurveTo(x + w * 0.78, y + h * (gy - 0.3), x + w * 0.92, y + h * (gy - 0.1), x + w, y + h * (gy - 0.18));
    ctx.lineTo(x + w, y + h); ctx.lineTo(x, y + h); ctx.closePath(); ctx.fill();
    ctx.fillStyle = c2;
    ctx.beginPath(); ctx.moveTo(x, y + h * gy);
    ctx.bezierCurveTo(x + w * 0.3, y + h * (gy - 0.08), x + w * 0.65, y + h * (gy + 0.05), x + w, y + h * (gy - 0.04));
    ctx.lineTo(x + w, y + h); ctx.lineTo(x, y + h); ctx.closePath(); ctx.fill();
  }
  function treeAt(ctx, cx, by, s, col) {
    ctx.fillStyle = '#8B5A2B'; ctx.fillRect(cx - s * 0.05, by - s * 0.42, s * 0.1, s * 0.42);
    ctx.fillStyle = col || '#43A047';
    [[0, -0.66, 0.3], [-0.2, -0.5, 0.22], [0.2, -0.5, 0.22]].forEach(([dx, dy, r]) => dot(ctx, cx + dx * s, by + dy * s, r * s));
    ctx.fillStyle = 'rgba(255,255,255,.18)'; dot(ctx, cx - s * 0.08, by - s * 0.74, s * 0.1);
  }
  function outdoor(ctx, x, y, w, h, gy) {
    skyFill(ctx, x, y, w, h, '#6EC3F0', '#DFF3FD');
    sunAt(ctx, x + w * 0.86, y + h * 0.17, h * 0.07);
    cloudAt(ctx, x + w * 0.2, y + h * 0.17, h * 0.055);
    cloudAt(ctx, x + w * 0.58, y + h * 0.1, h * 0.04);
    hillsAt(ctx, x, y, w, h, gy, '#A5DB7E', '#6CBF45');
  }
  BG.plain = (ctx, x, y, w, h, o) => {
    const [c0, c1] = TINTS[o.tint] || TINTS.warm;
    const g = ctx.createRadialGradient(x + w * 0.5, y + h * 0.45, h * 0.1, x + w * 0.5, y + h * 0.5, Math.max(w, h) * 0.75);
    g.addColorStop(0, c0); g.addColorStop(1, c1);
    ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
    const r = seeded(5), cols = ['#FF8A80', '#FFD54F', '#81D4FA', '#A5D6A7', '#CE93D8'], A = ctx.globalAlpha;
    for (let i = 0; i < 28; i++) { ctx.globalAlpha = A * 0.4; ctx.fillStyle = cols[i % 5]; dot(ctx, x + r() * w, y + r() * h, 3 + r() * 6); }
    ctx.globalAlpha = A;
  };
  // 5.0 起：摄影棚——柔和的渐变背景，下面一点地面的影子；主角放在中间特写（照相机、杯子、书……）
  BG.studio = (ctx, x, y, w, h, o) => {
    const T = { gray: ['#FBFBF9', '#D5D9DB'], warm: ['#FFF9EE', '#EBD9BC'], blue: ['#F5F9FD', '#C5D8EA'], green: ['#F5FBF3', '#CBE3C5'], pink: ['#FFF6F8', '#EECCD6'], purple: ['#F8F5FF', '#D5CBEE'] };
    const [c0, c1] = T[o.tint] || T.gray;
    const g = ctx.createRadialGradient(x + w * 0.5, y + h * 0.4, h * 0.05, x + w * 0.5, y + h * 0.5, Math.max(w, h) * 0.78);
    g.addColorStop(0, c0); g.addColorStop(1, c1);
    ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
    const fl = ctx.createLinearGradient(0, y + h * 0.7, 0, y + h);
    fl.addColorStop(0, 'rgba(70,60,50,0)'); fl.addColorStop(1, 'rgba(70,60,50,.10)');
    ctx.fillStyle = fl; ctx.fillRect(x, y + h * 0.7, w, h * 0.3);
  };
  // 白纸：示意图（剖面、原理）用，干净不抢眼
  BG.blank = (ctx, x, y, w, h, o) => { ctx.fillStyle = o.paper || '#FBFAF6'; ctx.fillRect(x, y, w, h); };
  BG.sky = (ctx, x, y, w, h) => outdoor(ctx, x, y, w, h, 0.76);
  BG.park = (ctx, x, y, w, h) => {
    outdoor(ctx, x, y, w, h, 0.76);
    treeAt(ctx, x + w * 0.08, y + h * 0.8, h * 0.44); treeAt(ctx, x + w * 0.93, y + h * 0.82, h * 0.5, '#2E9E4F'); treeAt(ctx, x + w * 0.76, y + h * 0.74, h * 0.3, '#66BB6A');
    const r = seeded(3), A = ctx.globalAlpha;
    for (let i = 0; i < 14; i++) { ctx.globalAlpha = A * 0.9; ctx.fillStyle = ['#FF6F91', '#FFD54F', '#FFFFFF'][i % 3]; dot(ctx, x + r() * w, y + h * (0.84 + r() * 0.14), 2.5 + r() * 2.5); }
    ctx.globalAlpha = A;
  };
  BG.road = (ctx, x, y, w, h) => {
    outdoor(ctx, x, y, w, h, 0.66);
    ctx.fillStyle = '#596270'; ctx.fillRect(x, y + h * 0.66, w, h * 0.24);
    ctx.fillStyle = '#E7EAEE'; ctx.fillRect(x, y + h * 0.665, w, h * 0.012); ctx.fillRect(x, y + h * 0.875, w, h * 0.012);
    ctx.fillStyle = '#FFFFFF'; for (let i = 0; i < 11; i++) ctx.fillRect(x + (i - 0.3) * w / 10, y + h * 0.772, w * 0.05, h * 0.016);
    ctx.fillStyle = '#76C043'; ctx.fillRect(x, y + h * 0.9, w, h * 0.1);
  };
  BG.bridge = (ctx, x, y, w, h) => {
    skyFill(ctx, x, y, w, h, '#6EC3F0', '#DFF3FD');
    sunAt(ctx, x + w * 0.86, y + h * 0.16, h * 0.07);
    cloudAt(ctx, x + w * 0.18, y + h * 0.15, h * 0.055); cloudAt(ctx, x + w * 0.55, y + h * 0.09, h * 0.04);
    hillsAt(ctx, x, y, w, h, 0.62, '#B5E08E', '#8FD16A');
    ctx.fillStyle = lin(ctx, y + h * 0.62, y + h, '#4FB6EA', '#2479B8'); ctx.fillRect(x, y + h * 0.62, w, h * 0.38);
    ctx.strokeStyle = 'rgba(255,255,255,.65)'; ctx.lineWidth = Math.max(2, h * 0.008);
    for (let i = 0; i < 9; i++) { const wx = x + w * (0.08 + (i * 0.37) % 0.86), wy = y + h * (0.74 + (i % 3) * 0.08); ctx.beginPath(); ctx.arc(wx, wy, w * 0.025, Math.PI * 1.1, Math.PI * 1.9); ctx.stroke(); }
    ctx.fillStyle = '#6CBF45';
    ctx.beginPath(); ctx.moveTo(x, y + h * 0.58); ctx.lineTo(x + w * 0.2, y + h * 0.6); ctx.quadraticCurveTo(x + w * 0.24, y + h * 0.8, x + w * 0.18, y + h); ctx.lineTo(x, y + h); ctx.closePath(); ctx.fill();
    ctx.beginPath(); ctx.moveTo(x + w, y + h * 0.58); ctx.lineTo(x + w * 0.8, y + h * 0.6); ctx.quadraticCurveTo(x + w * 0.76, y + h * 0.8, x + w * 0.82, y + h); ctx.lineTo(x + w, y + h); ctx.closePath(); ctx.fill();
    ctx.strokeStyle = '#B9814F'; ctx.lineWidth = h * 0.03;
    ctx.beginPath(); ctx.moveTo(x + w * 0.2, y + h * 0.88); ctx.quadraticCurveTo(x + w * 0.5, y + h * 0.5, x + w * 0.8, y + h * 0.88); ctx.stroke();
    ctx.lineWidth = h * 0.012;
    for (let i = 1; i < 8; i++) { const fx = 0.2 + i * 0.075, ay = 0.88 - 0.38 * (1 - Math.pow((fx - 0.5) / 0.3, 2)) * 0.98; ctx.beginPath(); ctx.moveTo(x + w * fx, y + h * 0.62); ctx.lineTo(x + w * fx, y + h * Math.max(0.62, ay)); ctx.stroke(); }
    ctx.fillStyle = '#C8925E'; ctx.fillRect(x + w * 0.1, y + h * 0.6, w * 0.8, h * 0.05);
    ctx.fillStyle = '#A9744A'; ctx.fillRect(x + w * 0.1, y + h * 0.645, w * 0.8, h * 0.012);
    ctx.strokeStyle = '#8D5E3A'; ctx.lineWidth = Math.max(2, h * 0.008);
    ctx.beginPath(); ctx.moveTo(x + w * 0.1, y + h * 0.545); ctx.lineTo(x + w * 0.9, y + h * 0.545); ctx.stroke();
    for (let i = 0; i <= 16; i++) { ctx.beginPath(); ctx.moveTo(x + w * (0.1 + i * 0.05), y + h * 0.545); ctx.lineTo(x + w * (0.1 + i * 0.05), y + h * 0.6); ctx.stroke(); }
  };
  BG.river = BG.bridge;
  BG.sea = (ctx, x, y, w, h) => {
    skyFill(ctx, x, y, w, h, '#86CFF3', '#E8F8FF');
    sunAt(ctx, x + w * 0.2, y + h * 0.2, h * 0.07); cloudAt(ctx, x + w * 0.68, y + h * 0.16, h * 0.05);
    ctx.fillStyle = lin(ctx, y + h * 0.5, y + h * 0.84, '#3DAAE3', '#1C6FAE'); ctx.fillRect(x, y + h * 0.5, w, h * 0.34);
    ctx.strokeStyle = 'rgba(255,255,255,.7)'; ctx.lineWidth = Math.max(2, h * 0.008);
    for (let i = 0; i < 10; i++) { const wx = x + w * ((i * 0.29) % 1), wy = y + h * (0.57 + (i % 4) * 0.065); ctx.beginPath(); ctx.arc(wx, wy, w * 0.022, Math.PI * 1.1, Math.PI * 1.9); ctx.stroke(); }
    ctx.fillStyle = '#F3D693'; ctx.beginPath(); ctx.moveTo(x, y + h * 0.84); ctx.quadraticCurveTo(x + w * 0.5, y + h * 0.78, x + w, y + h * 0.86); ctx.lineTo(x + w, y + h); ctx.lineTo(x, y + h); ctx.closePath(); ctx.fill();
  };
  BG.city = (ctx, x, y, w, h) => {
    skyFill(ctx, x, y, w, h, '#8FD0F5', '#EAF7FF');
    cloudAt(ctx, x + w * 0.75, y + h * 0.13, h * 0.045);
    const r = seeded(9), cols = ['#F28B82', '#FBBC04', '#81C995', '#78A9F0', '#C58AF9', '#FFAB91', '#4DD0E1'];
    let bx = x - w * 0.02;
    while (bx < x + w) {
      const bw = w * (0.075 + r() * 0.07), bh = h * (0.22 + r() * 0.3), by = y + h * 0.68 - bh;
      ctx.fillStyle = cols[(r() * cols.length) | 0]; ctx.fillRect(bx, by, bw, bh);
      ctx.fillStyle = 'rgba(255,255,255,.72)';
      for (let wy = by + h * 0.035; wy < by + bh - h * 0.04; wy += h * 0.06) for (let wx = bx + bw * 0.16; wx < bx + bw - bw * 0.2; wx += bw * 0.3) ctx.fillRect(wx, wy, bw * 0.16, h * 0.03);
      bx += bw + w * 0.008;
    }
    ctx.fillStyle = '#C9CED6'; ctx.fillRect(x, y + h * 0.68, w, h * 0.05);
    ctx.fillStyle = '#596270'; ctx.fillRect(x, y + h * 0.73, w, h * 0.27);
    ctx.fillStyle = '#FFFFFF'; for (let i = 0; i < 11; i++) ctx.fillRect(x + (i - 0.3) * w / 10, y + h * 0.855, w * 0.05, h * 0.016);
  };
  BG.room = (ctx, x, y, w, h) => {
    ctx.fillStyle = lin(ctx, y, y + h * 0.72, '#FFF1D8', '#FBE0B8'); ctx.fillRect(x, y, w, h * 0.72);
    ctx.fillStyle = '#D9A066'; ctx.fillRect(x, y + h * 0.72, w, h * 0.28);
    ctx.strokeStyle = 'rgba(120,70,30,.25)'; ctx.lineWidth = 2;
    for (let i = 1; i < 4; i++) { ctx.beginPath(); ctx.moveTo(x, y + h * (0.72 + i * 0.07)); ctx.lineTo(x + w, y + h * (0.72 + i * 0.07)); ctx.stroke(); }
    ctx.fillStyle = '#C98B4E'; ctx.fillRect(x, y + h * 0.71, w, h * 0.022);
    const wx = x + w * 0.64, wy = y + h * 0.1, ww = w * 0.26, wh = h * 0.36;
    ctx.fillStyle = lin(ctx, wy, wy + wh, '#7FCBF2', '#D9F1FD'); ctx.fillRect(wx, wy, ww, wh);
    cloudAt(ctx, wx + ww * 0.35, wy + wh * 0.35, wh * 0.12);
    ctx.strokeStyle = '#FFFFFF'; ctx.lineWidth = Math.max(3, h * 0.016); ctx.strokeRect(wx, wy, ww, wh);
    ctx.beginPath(); ctx.moveTo(wx + ww / 2, wy); ctx.lineTo(wx + ww / 2, wy + wh); ctx.moveTo(wx, wy + wh / 2); ctx.lineTo(wx + ww, wy + wh / 2); ctx.stroke();
    ctx.fillStyle = '#FFFFFF'; ctx.fillRect(x + w * 0.1, y + h * 0.16, w * 0.16, h * 0.2);
    ctx.fillStyle = '#9ED67A'; ctx.beginPath(); ctx.moveTo(x + w * 0.11, y + h * 0.34); ctx.lineTo(x + w * 0.16, y + h * 0.24); ctx.lineTo(x + w * 0.2, y + h * 0.3); ctx.lineTo(x + w * 0.22, y + h * 0.27); ctx.lineTo(x + w * 0.25, y + h * 0.34); ctx.closePath(); ctx.fill();
  };
  BG.kitchen = (ctx, x, y, w, h) => {
    ctx.fillStyle = '#E6F5F1'; ctx.fillRect(x, y, w, h);
    ctx.strokeStyle = 'rgba(80,140,130,.18)'; ctx.lineWidth = 2;
    for (let i = 1; i < 12; i++) { ctx.beginPath(); ctx.moveTo(x + i * w / 12, y); ctx.lineTo(x + i * w / 12, y + h * 0.64); ctx.stroke(); }
    for (let j = 1; j < 6; j++) { ctx.beginPath(); ctx.moveTo(x, y + j * h * 0.11); ctx.lineTo(x + w, y + j * h * 0.11); ctx.stroke(); }
    ctx.fillStyle = '#C98B4E'; ctx.fillRect(x, y + h * 0.64, w, h * 0.08);
    ctx.fillStyle = '#A8703F'; ctx.fillRect(x, y + h * 0.72, w, h * 0.28);
    ctx.fillStyle = 'rgba(255,255,255,.25)'; ctx.fillRect(x, y + h * 0.645, w, h * 0.012);
  };
  BG.table = BG.kitchen;
  BG.classroom = (ctx, x, y, w, h) => {
    ctx.fillStyle = '#F4ECDD'; ctx.fillRect(x, y, w, h);
    ctx.fillStyle = '#8A5A33'; ctx.fillRect(x + w * 0.12, y + h * 0.08, w * 0.76, h * 0.46);
    ctx.fillStyle = '#2F5646'; ctx.fillRect(x + w * 0.135, y + h * 0.105, w * 0.73, h * 0.41);
    ctx.strokeStyle = 'rgba(240,240,230,.55)'; ctx.lineWidth = Math.max(2, h * 0.008);
    ctx.beginPath(); ctx.moveTo(x + w * 0.2, y + h * 0.22); ctx.lineTo(x + w * 0.45, y + h * 0.22); ctx.moveTo(x + w * 0.2, y + h * 0.32); ctx.lineTo(x + w * 0.38, y + h * 0.32); ctx.stroke();
    ctx.fillStyle = '#C9A27A'; ctx.fillRect(x, y + h * 0.8, w, h * 0.2);
  };
  BG.night = (ctx, x, y, w, h) => {
    skyFill(ctx, x, y, w, h, '#0D1F3F', '#30467A');
    const r = seeded(13), A = ctx.globalAlpha;
    ctx.fillStyle = '#FFFFFF';
    for (let i = 0; i < 40; i++) { ctx.globalAlpha = A * (0.4 + r() * 0.6); dot(ctx, x + r() * w, y + r() * h * 0.6, 1 + r() * 2); }
    ctx.globalAlpha = A;
    ctx.fillStyle = '#FFF3B0'; dot(ctx, x + w * 0.82, y + h * 0.2, h * 0.08);
    ctx.fillStyle = '#1A3160'; dot(ctx, x + w * 0.85, y + h * 0.18, h * 0.07);
    hillsAt(ctx, x, y, w, h, 0.8, '#1E3B33', '#2B5244');
  };
  BG.space = (ctx, x, y, w, h) => {
    const g = ctx.createRadialGradient(x + w * 0.4, y + h * 0.4, h * 0.1, x + w * 0.5, y + h * 0.5, w * 0.8);
    g.addColorStop(0, '#3A2470'); g.addColorStop(1, '#0B0822'); ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
    const r = seeded(17), A = ctx.globalAlpha;
    ctx.fillStyle = '#FFFFFF';
    for (let i = 0; i < 50; i++) { ctx.globalAlpha = A * (0.3 + r() * 0.7); dot(ctx, x + r() * w, y + r() * h, 0.8 + r() * 1.8); }
    ctx.globalAlpha = A;
    ctx.fillStyle = '#F4A261'; dot(ctx, x + w * 0.82, y + h * 0.26, h * 0.1);
    ctx.strokeStyle = '#FFE0B5'; ctx.lineWidth = Math.max(2, h * 0.012); ctx.beginPath(); ctx.ellipse(x + w * 0.82, y + h * 0.26, h * 0.18, h * 0.05, -0.3, 0, Math.PI * 2); ctx.stroke();
  };
  BG.snow = (ctx, x, y, w, h) => {
    skyFill(ctx, x, y, w, h, '#BFDDF2', '#F2FAFF');
    hillsAt(ctx, x, y, w, h, 0.74, '#E9F2F9', '#FFFFFF');
    const r = seeded(21), A = ctx.globalAlpha;
    ctx.fillStyle = '#FFFFFF';
    for (let i = 0; i < 36; i++) { ctx.globalAlpha = A * 0.9; dot(ctx, x + r() * w, y + r() * h * 0.7, 1.5 + r() * 2.5); }
    ctx.globalAlpha = A;
  };
  // 说话的气泡：(x, y) 是尾巴指着的地方
  function bubble(ctx, s, x, y, size) {
    setFont(ctx, size, hasCjk(s) ? ZH : EN, 'bold');
    const tw = ctx.measureText(s).width, pw = tw + size * 1.1, ph = size * 1.65;
    const bx = x - pw * 0.25, by = y - ph - size * 0.55;
    ctx.fillStyle = '#FFFFFF'; ctx.strokeStyle = '#33413B'; ctx.lineWidth = Math.max(2, size * 0.09);
    rr(ctx, bx, by, pw, ph, ph * 0.42); ctx.fill(); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x - size * 0.15, by + ph - 1); ctx.lineTo(x, y - size * 0.05); ctx.lineTo(x + size * 0.4, by + ph - 1); ctx.fill();
    ctx.beginPath(); ctx.moveTo(x - size * 0.15, by + ph); ctx.lineTo(x, y - size * 0.05); ctx.lineTo(x + size * 0.4, by + ph); ctx.stroke();
    txt(ctx, s, bx + pw / 2, by + ph / 2 + 1, { size, family: hasCjk(s) ? ZH : EN, weight: 'bold', color: '#33413B', align: 'center', base: 'middle' });
  }
  // 画一幅画；st = { q: 出现的进度 0～1, lt: 出现以后过了几秒 }
  // 5.0 起，画里除了表情（e），还可以放：svg 专门画的插图（矢量，放多大都清楚，特写主角用它）、img 照片、
  // ray 一道会“画出来”的光线 / 箭头（示意图）、label 带指示线的标签、shape 方块圆圈（示意图的墙、亮点）；整幅画 flash 闪一下（拍照）
  // ===== 6.25（第六十二版）：画面真的动起来，人和人、人和物、物和物之间有互动 =====
  // 用户：“我希望图片里面要有适当的动图，比如 speaker 画的是人在演讲，那么可以让人物动起来，嘴巴讲起来这样的；大喇叭也是一样，
  // 可以画一下音波这样的，周围有人的话，可以画人在走动。总之要是动态的图”“如果多人同台，或者做事，要增加一些互动，就是人和人，人和物，
  // 物和物这些之间有的时候可以增加一些互动，要根据内容来进行”。做法见 pictures.md 第十八节、规矩 51。
  function hash1(n) { const v = Math.sin(n * 127.1 + 311.7) * 43758.5453; return v - Math.floor(v); }
  // 说话的人一句一句地说：phrase 秒一句（默认 2.4），句末停一小会儿
  function talkPhase(it, tt) {
    const L = Number(it.phrase) || 2.4, k = Math.floor(tt / L), inP = tt - k * L;
    return { on: inP < L - 0.3 - 0.45 * hash1(k + 3.3), k, inP, stop: L - 0.3 - 0.45 * hash1(k + 3.3), L };
  }
  // 轮流（人和人的互动）：turn: [第几个, 一共几个]——两个人对话写 [0, 2]、[1, 2]，每人 turnLen 秒（默认 2.6）轮一次
  function turnInfo(it, lt) {
    const n = Math.max(1, Number(it.turn[1]) || 2), len = Number(it.turnLen) || 2.6, cyc = len * n;
    const full = Math.floor(lt / cyc), inC = lt - full * cyc, my = Number(it.turn[0]) * len;
    const inS = inC - my;
    return { mine: inS >= 0 && inS < len, inS, len, clock: full * len + clamp(inS / len) * len };
  }
  // 这一刻这个人在不在说话（talkWhen / talkUntil 管从什么时候说到什么时候；有 turn 的只在自己那一轮说）
  function talkingNow(it, lt, tt) {
    if (it._tf != null && lt < it._tf) return false;
    if (it._tt != null && lt > it._tt) return false;
    if (Array.isArray(it.turn)) { const T = turnInfo(it, lt); return T.mine && T.inS > 0.2 && T.inS < T.len - 0.35; }
    return talkPhase(it, tt).on;
  }
  // 动图这一刻放第几帧（seq）：loop 循环（默认）；pingpong 来回；talk 说话——frames 是“手势 × 嘴型”的格子（mouths 每个手势几种嘴型），
  // 手势按 gfps 来回慢慢动、嘴型按 mfps 像说话一样一张一合，一句一停；blink 前一半是慢慢动的几帧、后一半是同样的几帧闭着眼，隔三秒左右眨一下
  function frameIndex(it, tt, lt) {
    const n = it._fr.length, seq = it.seq || 'loop', fps = Number(it.fps) || 3;
    const pp = (c, m) => { if (m <= 1) return 0; const k = c % (2 * m - 2); return k < m ? k : 2 * m - 2 - k; };
    if (seq === 'talk') {
      const M = Math.max(1, Number(it.mouths) || 3), G = Math.max(1, Math.floor(n / M));
      const on = talkingNow(it, lt, tt);
      const gt = Array.isArray(it.turn) ? turnInfo(it, lt).clock : tt;          // 轮到别人说时手势停住（在听），不会跳
      const g = pp(Math.floor(gt * (Number(it.gfps) || 2.6)), G);
      let m = 0;
      if (on) { const r = hash1(Math.floor(tt * (Number(it.mfps) || 8)) * 1.913 + 7); m = M === 1 ? 0 : r < 0.2 ? 0 : r < 0.6 ? Math.min(1, M - 1) : M - 1; }
      return Math.min(n - 1, g * M + m);
    }
    let tq = tt;
    if (Array.isArray(it.turn)) { const T = turnInfo(it, lt); if (!T.mine) return seq === 'blink' ? 0 : 0; tq = T.clock; }   // 只在自己那一轮动（比如别人说完了才笑）
    if (seq === 'pingpong') return pp(Math.floor(tq * fps), n);
    if (seq === 'blink') {
      const G = Math.max(1, Math.floor(n / 2)), g = pp(Math.floor(tq * fps), G);
      const per = 3.2, sh = hash1((Number(it.x) || 0) * 17 + (Number(it.y) || 0) * 7) * per, k = Math.floor((tt + sh) / per), inP = tt + sh - k * per, at = 0.8 + 1.8 * hash1(k + 1.7);
      return inP > at && inP < at + 0.14 && n >= 2 * G ? G + g : g;
    }
    return Math.floor(tq * fps) % n;
  }
  // 听的人点头（人和人）：nodWith = 说话的人的 id，那个人每说完一句、停顿的时候点一下头
  function nodAmount(pic, id, lt, jitter) {
    const tk = (pic.items || []).find(z => z.id === id);
    if (!tk || tk._t0 == null) return 0;
    const tp = talkPhase(tk, Math.max(0, lt - tk._t0)), since = tp.inP - tp.stop - (jitter || 0);
    if (tk._tf != null && lt < tk._tf) return 0;
    return since > 0 && since < 0.5 ? Math.sin(since / 0.5 * Math.PI) : 0;
  }
  // 会动的效果：
  //   waves 声波：从 x、y 往 dir（度，0 = 右、90 = 下、180 = 左）一道道往外走，spread 张开几度，n 几道，period 一道走完几秒，r0 / r1 起止半径（占画高），color、lw；
  //         with: 说话的人的 id（人和物：那个人说话时才往外出声波，停顿时不出——喇叭、麦克风、音箱跟着人说话）；both: true 两边都出
  //   emit  一串往外飘的东西（音符、水滴、气泡）：svg 一张图（alt 再几张轮着用），every 几秒出一个，life 飘几秒，to [dx, dy] 飘多远（占画宽、画高），
  //         s 大小（占画高），wobble 左右摆，spin 转；with 同上；beat: true 跟着这幅画的节拍（pic.beat，每分钟几拍）出
  //   eq    放音乐时屏幕上跳动的柱子（x、y 中心，w、h 大小占画宽画高，n 几根）——跟着 pic.beat 跳
  //   beam  舞台的光柱：从灯（x、y）往下照，len 多长（占画高），width 张开几度，swing 左右摆几度，period 摆一次几秒，tilt 往哪边斜
  function drawFx(ctx, it, pic, x, y, w, h, lt, d0, alpha, P, seed) {
    const tt = Math.max(0, lt - d0), p0 = P([Number(it.x), Number(it.y)]);
    const tk = it.with != null ? (pic.items || []).find(z => z.id === it.with) : null;
    const talkAt = tl => !tk || tk._t0 == null || talkingNow(tk, tl, Math.max(0, tl - tk._t0));
    const beat = Number(it.bpm) || Number(pic.beat) || 0;
    ctx.save();
    if (it.waves) {
      const n = Number(it.n) || 3, per = Number(it.period) || 1.3;
      const r0 = (it.r0 != null ? Number(it.r0) : 0.03) * h, r1 = (it.r1 != null ? Number(it.r1) : 0.2) * h;
      const spr = (it.spread != null ? Number(it.spread) : 70) * Math.PI / 180, lw = Math.max(2, (Number(it.lw) || 0.014) * h), col = it.color || '#F59E0B';
      ctx.lineCap = 'round';
      const dirs = [(Number(it.dir) || 0) * Math.PI / 180].concat(it.both ? [(Number(it.dir) || 0) * Math.PI / 180 + Math.PI] : []);
      for (let k = 0; k < n; k++) {
        const ph = ((tt / per) + k / n) % 1;
        if (!talkAt(lt - ph * per)) continue;                   // 这一道发出来的时候人没在说话：不画
        const r = r0 + (r1 - r0) * ph, al = Math.pow(Math.sin(Math.PI * Math.min(1, ph * 1.12)), 0.7) * (1 - ph * 0.3);
        if (al <= 0.02) continue;
        dirs.forEach(dir => {
          ctx.globalAlpha = alpha * al;
          ctx.beginPath(); ctx.arc(p0[0], p0[1], r, dir - spr / 2, dir + spr / 2); ctx.strokeStyle = '#1B1A1F'; ctx.lineWidth = lw + Math.max(2.5, lw * 0.5); ctx.stroke();
          ctx.beginPath(); ctx.arc(p0[0], p0[1], r, dir - spr / 2, dir + spr / 2); ctx.strokeStyle = col; ctx.lineWidth = lw; ctx.stroke();
        });
      }
    }
    if (it.emit) {
      const ims = [it._im].concat((it._alt || []).map(o => o._im)).filter(im => im && im.complete && im.naturalWidth);
      const every = Number(it.every) || (beat ? 120 / beat : 0.7), life = Number(it.life) || 2.0;
      const to = Array.isArray(it.to) ? it.to.map(Number) : [0.05, -0.3];
      const s0 = (Number(it.s) || 0.1) * h, wob = (it.wobble != null ? Number(it.wobble) : 0.02) * w, sp = it.spread != null ? Number(it.spread) : 0.35;
      const off = Number(it.offset) || 0, k1 = Math.floor((tt - off) / every), k0 = Math.max(0, Math.ceil((tt - off - life) / every));
      for (let k = k0; k <= k1 && ims.length; k++) {
        const age = tt - off - k * every;
        if (age < 0 || age > life || !talkAt(lt - age)) continue;
        const u = age / life, r = hash1(k * 1.37 + seed * 7.1), r2 = hash1(k * 2.11 + seed * 3.3);
        const dx = to[0] * w * u * (1 + (r - 0.5) * sp) + Math.sin(age * 3.2 + r * 6) * wob, dy = to[1] * h * u * (1 + (r2 - 0.5) * sp);
        const al = clamp(u / 0.1) * clamp((1 - u) / 0.3), im = ims[k % ims.length];
        const sz = s0 * (0.85 + 0.3 * r) * (0.55 + 0.45 * clamp(u / 0.15)), ww = sz * im.naturalWidth / im.naturalHeight;
        ctx.save(); ctx.globalAlpha = alpha * al; ctx.translate(p0[0] + dx, p0[1] + dy); ctx.rotate(Math.sin(age * 2.4 + r * 5) * (it.spin != null ? Number(it.spin) : 0.25));
        ctx.drawImage(im, -ww / 2, -sz / 2, ww, sz); ctx.restore();
      }
    }
    if (it.eq) {
      const n = Number(it.n) || 7, bw = (Number(it.w) || 0.1) * w, bh = (Number(it.h) || 0.06) * h;
      const gap = bw / n * 0.25, cw = (bw - gap * (n - 1)) / n, bt = beat ? (lt * beat / 60) % 1 : 0;
      const cols = Array.isArray(it.colors) ? it.colors : ['#2FB5A9', '#F2C230', '#F28C28', '#E8407A', '#7B57D6', '#2E6FD9', '#43A047'];
      ctx.globalAlpha = alpha;
      for (let k = 0; k < n; k++) {
        const v = 0.22 + 0.6 * Math.abs(Math.sin(tt * (2.3 + hash1(k + seed) * 2.8) + k * 1.3)) + (beat ? 0.25 * Math.exp(-Math.pow(bt / 0.12, 2)) : 0);
        const hh = Math.min(1, v) * bh, xx = p0[0] - bw / 2 + k * (cw + gap), yy = p0[1] + bh / 2 - hh;
        ctx.fillStyle = cols[k % cols.length]; ctx.fillRect(xx, yy, cw, hh);
      }
    }
    if (it.beam) {
      const len = (Number(it.len) || 0.9) * h, wd = (Number(it.width) || 16) * Math.PI / 180;
      const ang = Math.PI / 2 + ((Number(it.tilt) || 0) + Math.sin(lt * 2 * Math.PI / (Number(it.period) || 5) + seed) * (it.swing != null ? Number(it.swing) : 8)) * Math.PI / 180;
      const col = it.color || '255,244,196', ex = p0[0] + Math.cos(ang) * len, ey = p0[1] + Math.sin(ang) * len;
      const g = ctx.createLinearGradient(p0[0], p0[1], ex, ey);
      g.addColorStop(0, 'rgba(' + col + ',0.6)'); g.addColorStop(1, 'rgba(' + col + ',0)');
      ctx.globalAlpha = alpha * (0.78 + 0.22 * Math.sin(lt * 3.1 + seed));
      ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(p0[0], p0[1]);
      ctx.lineTo(p0[0] + Math.cos(ang - wd / 2) * len, p0[1] + Math.sin(ang - wd / 2) * len);
      ctx.lineTo(p0[0] + Math.cos(ang + wd / 2) * len, p0[1] + Math.sin(ang + wd / 2) * len);
      ctx.closePath(); ctx.fill();
    }
    ctx.restore();
  }
  // 一排人（台下听众、排队的人）：crowd = 几个人，按人切成几条各自轻轻动；nodWith = 台上说话的人——他说完一句停顿时，大家点点头（人和人）
  function drawCrowd(ctx, it, im, size, lt, pic) {
    const n = Math.max(2, Number(it.crowd) || 8), ww = size * im.naturalWidth / im.naturalHeight, bm = rasterOf(ctx, im, ww, size) || im;
    const nw = bm === im ? im.naturalWidth : bm.width, nh = bm === im ? im.naturalHeight : bm.height;
    for (let k = 0; k < n; k++) {
      const r = hash1(k * 3.7 + 1);
      let dy = Math.sin(lt * (1.2 + r * 1.1) + k * 1.9) * size * 0.01;
      if (it.nodWith != null) dy += nodAmount(pic, it.nodWith, lt, r * 0.25) * size * 0.04 * (r > 0.2 ? 1 : 0.35);
      ctx.drawImage(bm, k * nw / n, 0, nw / n, nh, -ww / 2 + k * ww / n - 0.6, -size / 2 + dy, ww / n + 1.2, size);
    }
  }
  // 6.25：svg 插图先按这一刻在屏幕上的像素大小画成位图存起来，同样大小再画就直接贴位图（1080p 下一帧快好几倍）。
  // 同一张图、同样大小连着两帧都要画才存（出场时一点点放大的那几帧不存）；最多存 RC_MAX 个像素，先存的先扔
  const RC = new Map(), RC_MAX = 9e7; let rcPix = 0, rcFrame = 0;
  function rasterOf(ctx, im, w, h) {
    if (typeof document === 'undefined' || !im || !im.naturalWidth || String(im.src).slice(0, 18) !== 'data:image/svg+xml') return null;
    const m = ctx.getTransform(), k = Math.hypot(m.a, m.b) || 1;
    const pw = Math.max(1, Math.round(w * k)), ph = Math.max(1, Math.round(h * k));
    if (pw * ph > 5e6) return null;
    if (!im._rid) im._rid = 'i' + (++rasterOf.n);
    const key = im._rid + ':' + pw + 'x' + ph;
    const hit = RC.get(key);
    if (hit && hit.c) { RC.delete(key); RC.set(key, hit); return hit.c; }
    if (!hit) { RC.set(key, { f: rcFrame, c: null }); return null; }
    if (hit.f === rcFrame) return null;
    const c = document.createElement('canvas'); c.width = pw; c.height = ph;
    c.getContext('2d').drawImage(im, 0, 0, pw, ph);
    hit.c = c; rcPix += pw * ph;
    while (rcPix > RC_MAX && RC.size) { const [k0, v0] = RC.entries().next().value; RC.delete(k0); if (v0.c) rcPix -= v0.c.width * v0.c.height; }
    return c;
  }
  rasterOf.n = 0;
  // 6.28（第七十版）：音效（用户：“可以做一些音效，比如讲车子，可以有车子跑的声音，当然不要太长，不要影响主要的讲解，只是加深一下学生学习的印象；
  // 演讲也可以来一句演讲，扬声器也可以播放一下声音”）。画里一样东西写 sfx: 'meow'（它出现时响一下），或者单独写一条
  // {sound: 'meow', when / cue / delay, vol, times, every}（看不见、只出声）；渲染时记下每个音效在整段视频里的秒数，render.py 混进配音。
  // 只在讲解的几幕出声（部分卡片、拼起来、例句、演变、来历、规律），封面、意思总览、总结、练习、答案不出声
  let SFX_NOW = null, SFX_SCENE = '', SFX_LOG = [], SFX_SEEN = {};
  const SFX_SCENES = { part: 1, combo: 1, example: 1, evolve: 1, origin: 1, rule: 1 };
  function sfxReset() { SFX_LOG = []; SFX_SEEN = {}; }
  function sfxLog() { const o = SFX_LOG; SFX_LOG = []; return o; }
  function drawPic(ctx, pic, x, y, w, h, st) {
    st = st || {};
    const lt = Math.max(0, st.lt || 0), A = ctx.globalAlpha, rad = Math.min(26, h * 0.09);
    ctx.save();
    ctx.shadowColor = 'rgba(60,50,20,.16)'; ctx.shadowBlur = 18; ctx.shadowOffsetY = 5;
    rr(ctx, x, y, w, h, rad); ctx.fillStyle = '#FFFFFF'; ctx.fill();
    ctx.restore();
    ctx.save();
    rr(ctx, x, y, w, h, rad); ctx.clip();
    (BG[pic.bg] || BG.plain)(ctx, x, y, w, h, pic);
    if (pic._im && pic._im.complete && pic._im.naturalWidth) {
      const k = Math.max(w / pic._im.naturalWidth, h / pic._im.naturalHeight);
      ctx.drawImage(rasterOf(ctx, pic._im, pic._im.naturalWidth * k, pic._im.naturalHeight * k) || pic._im, x + (w - pic._im.naturalWidth * k) / 2, y + (h - pic._im.naturalHeight * k) / 2, pic._im.naturalWidth * k, pic._im.naturalHeight * k);
    }
    const order = pic.items.map((it, i) => [it, i]).sort((a, b) => (a[0].z || 0) - (b[0].z || 0));
    const place = {};                         // 每样东西现在画在哪儿（给 on 用）
    const toPx = (it, q) => {                 // 一个点 → 画布上的像素：写了 on 的按那幅插图自己的坐标
      const ref = it.on == null ? null : typeof it.on === 'number' ? place[it.on] : place[pic.items.findIndex(z => z.id === it.on)];
      if (!ref) return [x + Number(q[0]) * w, y + Number(q[1]) * h];
      const vb = ref.vb || [1, 1];
      return [ref.px - ref.ww / 2 + Number(q[0]) / vb[0] * ref.ww, ref.py - ref.hh / 2 + Number(q[1]) / vb[1] * ref.hh];
    };
    const cueT = (c, dl) => (Array.isArray(st.cues) && st.cues[c] != null ? st.cues[c] : 0.9 + 2.6 * c) + (Number(dl) || 0);
    // 5.11：按词出东西。when: "小孔" = 配音说到“小孔”这两个字的时候出来（比按句更准）：在这一步的几句话里找到这个词，
    // 按它在那一句里的位置（中文一个字一份、英文单词按长短折算）和那一句真实的长短，算出说到它的秒数，再提前 0.12 秒。
    // 没写 cue 就在几句里找第一句有这个词的；配音里找不到这个词，就按那一句（或第一句）开头算
    const whenT = (word, c, dl) => {
      const T = Array.isArray(st.cueTexts) ? st.cueTexts.map(String) : [];
      let ci = c != null ? Number(c) : T.findIndex(x => x.includes(String(word)));
      if (ci < 0) ci = 0;
      const t0 = cueT(ci, 0), t1 = Array.isArray(st.cueEnds) && st.cueEnds[ci] != null ? st.cueEnds[ci] : t0 + 2.6;
      const tx = T[ci] || '', at = tx.indexOf(String(word));
      if (at < 0) return t0 + (Number(dl) || 0);
      const wgt = z => (z.match(/[A-Za-z']+|[\u3400-\u9fff]|[，。；、：！？,.;:!?]/g) || []).reduce((n, m) => n + (/[A-Za-z]/.test(m) ? Math.max(1, m.length / 3) : /[\u3400-\u9fff]/.test(m) ? 1 : 0.7), 0);
      return Math.max(t0, t0 + (t1 - t0) * wgt(tx.slice(0, at)) / Math.max(1, wgt(tx)) - 0.12) + (Number(dl) || 0);
    };
    for (const drawNow of [false, true])
    for (const [it, i] of order) {
      if (it.goWhen != null && it._gw == null) it._gw = 1;
      const d0 = it.when != null ? whenT(it.when, it.cue, it.delay) : it.cue != null ? cueT(Number(it.cue), it.delay) : it.delay != null ? Number(it.delay) : i * 0.15;
      if (it.hideWhen != null) it.hide = whenT(it.hideWhen, it.hideCue, it.hideDelay);
      else if (it.hideCue != null) it.hide = cueT(Number(it.hideCue), it.hideDelay);
      it._t0 = d0;                                                   // 6.25：出现的时刻（说话、点头、声波跟着它算）
      if ((it.sound || it.sfx) && !drawNow && SFX_NOW != null && SFX_SCENES[SFX_SCENE] && lt >= d0 && !(it.hide != null && Number(it.hide) <= d0)) {
        const base = SFX_NOW - (lt - d0), nrep = Math.max(1, Number(it.times) || 1), ev = Number(it.every) || 1.2, nm = String(it.sound || it.sfx);
        for (let k = 0; k < nrep; k++) {
          const ta = base + k * ev, key = nm + '@' + Math.round(ta * 20);
          if (k * ev <= lt - d0 + 1e-6 && !SFX_SEEN[key]) { SFX_SEEN[key] = 1; SFX_LOG.push({ t: Math.round(ta * 1000) / 1000, name: nm, vol: it.vol != null ? Number(it.vol) : 1, gap: !!it.gap }); }
        }
      }
      if (it.sound && !it.svg && !it.label && !it.ray && !it.waves && !it.emit && !it.e) continue;   // 6.28：只出声的一条，不画
      it._tf = it.talkWhen != null ? whenT(it.talkWhen, it.talkCue, it.talkDelay) : it.talkFrom != null ? Number(it.talkFrom) : null;
      it._tt = it.talkUntil != null ? whenT(it.talkUntil, it.talkUntilCue, 0) : it.talkTo != null ? Number(it.talkTo) : null;
      if (it.waves || it.emit || it.eq || it.beam) {                // 6.25：声波、飘出来的音符、跳动的柱子、光柱
        if (!drawNow) continue;
        const fv = clamp((lt - d0) / 0.35) * (it.a != null ? Number(it.a) : 1) * (it.hide != null ? clamp(1 - (lt - Number(it.hide)) / 0.3) : 1);
        if (fv > 0) drawFx(ctx, it, pic, x, y, w, h, lt, d0, A * fv, q => toPx(it, q), i);
        continue;
      }
      if ((it.ray || (it.label != null && !it.e && !it.svg && !it.img && !it.shape)) && !drawNow) continue;
      if (it.ray) { drawRay(ctx, it, x, y, w, h, lt, d0, A, q => toPx(it, q)); continue; }
      if (it.label != null && !it.e && !it.svg && !it.img && !it.shape) { drawLabel(ctx, it, x, y, w, h, lt, d0, A, q => toPx(it, q)); continue; }
      if (it.on != null) {
        const q = toPx(it, [it.x, it.y]); it._x = (q[0] - x) / w; it._y = (q[1] - y) / h;
        if (Array.isArray(it.go)) { const g = toPx(it, it.go); it._go = [(g[0] - x) / w, (g[1] - y) / h]; }
      }
      const body = !it.e;                                                   // 插图、照片、形状：默认淡入，不弹
      const a = clamp((lt - d0) / (it.fade != null ? Math.max(0.05, Number(it.fade)) : body ? 0.5 : 0.45));
      if (a <= 0) {
        const im0 = it._im && it._im.complete && it._im.naturalWidth ? it._im : null, sz = (Number(it.s) || 0.34) * h;
        place[i] = { px: x + (it.on != null ? it._x : Number(it.x)) * w, py: y + (it.on != null ? it._y : Number(it.y)) * h, hh: sz, ww: im0 ? sz * im0.naturalWidth / im0.naturalHeight : sz, vb: it._vb || null };
        continue;
      }
      let cx = it.on != null ? it._x : Number(it.x), cy = it.on != null ? it._y : Number(it.y), kk = 0;
      if (Array.isArray(it.go) && it.go.length >= 2) {
        const g0 = it.goWhen != null ? whenT(it.goWhen, it.goCue, it.goDelay) : it.goCue != null ? cueT(Number(it.goCue), it.goDelay) : d0 + (it.wait != null ? Number(it.wait) : 0.35);
        const T = Number(it.dur) || 2.6, k0 = (lt - g0) / T;
        const k = it.loop ? (k0 < 0 ? 0 : (k0 % 1.25) / 1.0) : clamp(k0);
        kk = easeInOut(clamp(k));
        const g = it.on != null && it._go ? it._go : it.go, x0 = it.on != null ? it._x : Number(it.x), y0 = it.on != null ? it._y : Number(it.y);
        cx = lerp(x0, Number(g[0]), kk); cy = lerp(y0, Number(g[1]), kk) - (Number(it.arc) || 0) * Math.sin(kk * Math.PI);
      }
      if (Array.isArray(it.path) && it.path.length) {               // [[秒, x, y], …]：第几秒到哪儿，中间自己走过去
        const P = it.path.map(k => k.map(Number));
        let j = 0;
        while (j < P.length - 1 && lt >= P[j + 1][0]) j++;
        if (lt <= P[0][0]) { cx = P[0][1]; cy = P[0][2]; }
        else if (j === P.length - 1) { cx = P[j][1]; cy = P[j][2]; }
        else { const e = easeInOut(clamp((lt - P[j][0]) / Math.max(0.001, P[j + 1][0] - P[j][0]))); cx = lerp(P[j][1], P[j + 1][1], e); cy = lerp(P[j][2], P[j + 1][2], e); }
      }
      if (it.walk) {    // 6.25：走路的人一直走——walk: {from: [x, y], to: [x, y], speed（每秒走画宽的几分之几，不写就按步子大小算，不会“滑步”）, offset（0～1，错开）}；走出画再从头进来
        const wk = it.walk, f0 = (wk.from || [it.x, it.y]).map(Number), t0 = (wk.to || [f0[0] + 1.2, f0[1]]).map(Number);
        const dist = Math.hypot((t0[0] - f0[0]) * w, (t0[1] - f0[1]) * h);
        const sp = wk.speed != null ? Number(wk.speed) * w : (Number(it.s) || 0.34) * h * 0.62 * (Number(it.fps) || 7) / 7;
        const u = (lt * sp / Math.max(1, dist) + (Number(wk.offset) || 0)) % 1;
        cx = lerp(f0[0], t0[0], u); cy = lerp(f0[1], t0[1], u);
        it._left = t0[0] < f0[0];
      }
      let vis = Math.min(1, a * 1.5) * (it.a != null ? Number(it.a) : 1);
      if (it.hideWhen != null) it.hide = whenT(it.hideWhen, it.hideCue, it.hideDelay);
      else if (it.hideCue != null) it.hide = cueT(Number(it.hideCue), it.hideDelay);
      if (it.hide != null) vis *= clamp(1 - (lt - Number(it.hide)) / 0.3);
      if (it.blink) vis *= Math.floor(Math.max(0, lt - d0) / Number(it.blink)) % 2 === 0 ? 1 : 0.12;     // 一亮一灭（录像的红点）
      if (vis <= 0) continue;
      const ph = lt * 2 + i * 1.7, anim = it.anim || (body ? (it.walk ? 'step' : it.seq === 'talk' || it.seq === 'blink' ? 'breathe' : 'none') : it.go || it.path ? 'ride' : 'bob');
      let dy = 0, rot = (Number(it.rot) || 0) * Math.PI / 180, sc = 1, pivotB = false;
      if (anim === 'bob') dy = Math.sin(ph * 1.6) * 0.012;
      else if (anim === 'ride') dy = -Math.abs(Math.sin(ph * 4.5)) * 0.01;
      else if (anim === 'pulse') sc = 1 + 0.07 * Math.sin(ph * 2.2);
      else if (anim === 'spin') rot += lt * Math.PI;
      else if (anim === 'shake') rot += Math.sin(ph * 9) * 0.14;
      else if (anim === 'swing') rot += Math.sin(ph * 1.8) * 0.18;
      else if (anim === 'click') sc = 1 - 0.05 * Math.exp(-Math.pow((lt - Number(it.at || 0)) / 0.08, 2));    // 按快门：轻轻一沉
      // 6.25：breathe 人轻轻起伏、晃（以脚下为轴）；sway 摇摆；thump 音箱跟着节拍一鼓一鼓（bpm，不写用这幅画的 beat）；step 走路一步一颠；nod 点头
      else if (anim === 'breathe') { dy = Math.sin(lt * 2.0 + i * 1.3) * 0.004; rot += Math.sin(lt * 1.25 + i * 0.7) * 0.012; pivotB = true; }
      else if (anim === 'sway') { rot += Math.sin(lt * 1.7 + i) * 0.04; pivotB = true; }
      else if (anim === 'thump') { const bpm = Number(it.bpm) || Number(pic.beat) || 100, b = (lt * bpm / 60 + (Number(it.beatOff) || 0)) % 1; sc = 1 + 0.035 * (Math.exp(-Math.pow(b / 0.07, 2)) + Math.exp(-Math.pow((1 - b) / 0.07, 2))); }
      else if (anim === 'step') { const nf = it._fr ? it._fr.length : 6; dy = -Math.abs(Math.sin(Math.PI * lt * 2 * (Number(it.fps) || 7) / nf)) * 0.008; }
      else if (anim === 'nod') { rot += Math.sin(lt * 5.5 + i) * 0.02; pivotB = true; }
      if (it.nodWith != null && !it.crowd) { rot += nodAmount(pic, it.nodWith, lt, 0.08) * 0.04; pivotB = true; }      // 听的人：对方说完一句就点点头
      if (Array.isArray(it.turn) && it.seq === 'talk' && it._fr && !talkingNow(it, lt, Math.max(0, lt - d0))) { rot += Math.max(0, Math.sin(lt * 4.6)) * 0.02; pivotB = true; }   // 轮到别人说：边听边点头
      let s0 = Number(it.s) || 0.34;
      if (it.s2 != null) {                                           // 一边走一边变大变小（grow: [开始秒, 结束秒]；没写就跟着 go 走）
        const gw = it.growWhen != null ? whenT(it.growWhen, it.growCue, it.growDelay) : it.growCue != null ? cueT(Number(it.growCue), it.growDelay) : null;
        const gr = gw != null ? [gw, gw + (Number(it.growDur) || 1.2)] : it.grow;
        const g = Array.isArray(gr) ? clamp((lt - Number(gr[0])) / Math.max(0.01, Number(gr[1]) - Number(gr[0]))) : kk;
        s0 = lerp(s0, Number(it.s2), easeInOut(g));
      }
      const pop = it.pop != null ? !!it.pop : !body;
      const size = s0 * h * (pop ? easeBack(a) : 1) * sc;
      const px = x + cx * w, py = y + (cy + dy) * h;
      let im = it._im && it._im.complete && it._im.naturalWidth ? it._im : null;
      if (it._fr && it._fr.length > 1) {                     // 6.24：动图——从出现那一刻起按 fps 轮着换帧（说话张嘴、挥手、听音乐摇头）
        const fi = frameIndex(it, Math.max(0, lt - d0), lt), fo = it._fr[fi]._im;      // 6.25：说话、眨眼、来回（seq）
        if (fo && fo.complete && fo.naturalWidth) im = fo;
      }
      place[i] = { px, py, hh: size, ww: im ? size * im.naturalWidth / im.naturalHeight : size, vb: it._vb || null };
      if (!drawNow) continue;
      if (it.shadow) {                                               // 放在桌上、地上的东西：下面一片柔和的影子
        const sw = size * (im ? im.naturalWidth / im.naturalHeight : 1) * 0.46;
        ctx.save(); ctx.globalAlpha = A * vis * 0.9;
        const g = ctx.createRadialGradient(px, py + size * 0.5, 1, px, py + size * 0.5, sw);
        g.addColorStop(0, 'rgba(40,30,20,.32)'); g.addColorStop(1, 'rgba(40,30,20,0)');
        ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(px, py + size * 0.5, sw, size * 0.075, 0, 0, Math.PI * 2); ctx.fill(); ctx.restore();
      }
      ctx.save();
      if (pivotB) { ctx.translate(px, py + size / 2); if (rot) ctx.rotate(rot); ctx.translate(0, -size / 2); }     // 6.25：以脚下（画的底边）为轴
      else { ctx.translate(px, py); if (rot) ctx.rotate(rot); }
      // 6.18：走路、跑步的小人表情多半朝左；往右走（go 的终点在右边）又没写 flip 的，自动翻过来朝着走的方向（用户：“progress 中 pro 的方向画错了”）
      if (it.walk ? !!it._left !== !!it.flip : (it.flip || (it.flip == null && it.e && WALKERS.test(String(it.e)) && Array.isArray(it.go) && Number(it.go[0]) > Number(it.x)))) ctx.scale(-1, 1);   // 6.25：走路的人画的是往右走，往左走就翻过来
      if (it.flipY) ctx.scale(1, -1);
      ctx.globalAlpha = A * vis;
      if (it.svg || it.img) { if (it.crowd && im) drawCrowd(ctx, it, im, size, lt, pic); else drawArt(ctx, it, im, size, lt - d0); }
      else if (it.shape) drawShape(ctx, it, w, h);
      else emoji(ctx, it.e, 0, 0, size);
      ctx.restore();
      if (it.say && a >= 1) {
        const s0b = Array.isArray(it.sayAt) ? Number(it.sayAt[0]) : d0 + 0.6, s1 = Array.isArray(it.sayAt) ? Number(it.sayAt[1]) : (it.hide != null ? Number(it.hide) : 1e9);
        const sa = Math.min(clamp((lt - s0b) / 0.25), clamp((s1 - lt) / 0.25));
        if (sa > 0) { ctx.save(); ctx.globalAlpha = A * sa * vis; bubble(ctx, String(it.say), px + size * 0.18, py - size * 0.42, Math.max(14, h * 0.06)); ctx.restore(); }
      }
    }
    (pic.flash || []).forEach(t0 => {                                 // 拍照的闪光：一下变白，再慢慢退掉
      const k = lt - t0;
      if (k < -0.06 || k > 0.55) return;
      const a = k < 0.05 ? clamp((k + 0.06) / 0.11) : clamp(1 - (k - 0.05) / 0.5);
      ctx.save(); ctx.globalAlpha = A * 0.85 * a; ctx.fillStyle = '#FFFFFF'; ctx.fillRect(x, y, w, h); ctx.restore();
    });
    if (pic.not) slash(ctx, x + w / 2, y + h / 2, h * 0.62, clamp((lt - 0.6) / 0.6));
    ctx.restore();
    ctx.save(); rr(ctx, x, y, w, h, rad); ctx.lineWidth = 3; ctx.strokeStyle = 'rgba(255,255,255,.9)'; ctx.stroke(); ctx.restore();
    ctx.globalAlpha = A;
  }
  // 插图 / 照片：高 = size，宽按图的比例；reveal 从一边慢慢露出来（倒立的像一点点映出来）；frame 照片加白边
  function drawArt(ctx, it, im, size, t) {
    if (!im) return;
    const hh = size, ww = size * im.naturalWidth / im.naturalHeight;
    ctx.save();
    if (it.reveal) {
      const k = easeInOut(clamp(t / (Number(it.rdur) || 0.9)));
      const d = String(it.reveal);
      ctx.beginPath();
      if (d === 'down') ctx.rect(-ww / 2 - 2, -hh / 2 - 2, ww + 4, (hh + 4) * k);
      else if (d === 'up') ctx.rect(-ww / 2 - 2, hh / 2 + 2 - (hh + 4) * k, ww + 4, (hh + 4) * k);
      else if (d === 'left') ctx.rect(ww / 2 + 2 - (ww + 4) * k, -hh / 2 - 2, (ww + 4) * k, hh + 4);
      else ctx.rect(-ww / 2 - 2, -hh / 2 - 2, (ww + 4) * k, hh + 4);
      ctx.clip();
    }
    if (it.frame) {
      const pad = hh * 0.05;
      ctx.save(); ctx.shadowColor = 'rgba(0,0,0,.25)'; ctx.shadowBlur = hh * 0.06; ctx.shadowOffsetY = hh * 0.02;
      ctx.fillStyle = '#FFFFFF'; ctx.fillRect(-ww / 2 - pad, -hh / 2 - pad, ww + pad * 2, hh + pad * (it.frame === 'polaroid' ? 4 : 2)); ctx.restore();
    }
    if (it.round) { rr(ctx, -ww / 2, -hh / 2, ww, hh, hh * Number(it.round)); ctx.clip(); }
    ctx.drawImage(rasterOf(ctx, im, ww, hh) || im, -ww / 2, -hh / 2, ww, hh);
    ctx.restore();
  }
  // 形状（相对整幅画）：rect（w、h、r 圆角）、circle（r）、ellipse（w、h）；fill、stroke、lw（按画高 400 算的线宽）、glow 发光
  function drawShape(ctx, it, pw, ph) {
    const sh = String(it.shape), k = ph / 400;
    ctx.save();
    if (it.glow) { ctx.shadowColor = it.glowColor || it.fill || it.stroke || '#FFE680'; ctx.shadowBlur = Number(it.glow) * k * 20; }
    ctx.beginPath();
    const ww = (Number(it.w) || 0.2) * pw, hh = (Number(it.h) || 0.2) * ph;
    if (sh === 'poly' && Array.isArray(it.pts)) it.pts.forEach((q, j) => (j ? ctx.lineTo(q[0] * pw, q[1] * ph) : ctx.moveTo(q[0] * pw, q[1] * ph)));
    else if (sh === 'circle') ctx.arc(0, 0, (Number(it.r) || 0.05) * ph, 0, Math.PI * 2);
    else if (sh === 'ellipse') ctx.ellipse(0, 0, ww / 2, hh / 2, 0, 0, Math.PI * 2);
    else rr(ctx, -ww / 2, -hh / 2, ww, hh, (Number(it.r) || 0) * ph);
    if (it.fill) {
      if (Array.isArray(it.fill) && sh === 'poly') { const q = it.pts[Math.floor(it.pts.length / 2)] || [0, 0]; const g = ctx.createLinearGradient(0, 0, q[0] * pw, q[1] * ph); it.fill.forEach((c, j) => g.addColorStop(j / Math.max(1, it.fill.length - 1), c)); ctx.fillStyle = g; }
      else if (Array.isArray(it.fill)) { const g = ctx.createLinearGradient(0, -hh / 2, 0, hh / 2); it.fill.forEach((c, j) => g.addColorStop(j / Math.max(1, it.fill.length - 1), c)); ctx.fillStyle = g; }
      else ctx.fillStyle = it.fill;
      ctx.fill();
    }
    if (it.stroke) { ctx.shadowBlur = 0; ctx.lineWidth = (Number(it.lw) || 3) * k; ctx.strokeStyle = it.stroke; if (it.dash) ctx.setLineDash(it.dash.map(v => v * k)); ctx.stroke(); }
    ctx.restore();
  }
  // 光线 / 箭头：ray = [[x, y], …]（相对整幅画），从第一个点开始，dur 秒画到最后一个点；arrow 画箭头，glow 发光，dash 虚线
  function drawRay(ctx, it, x, y, w, h, lt, d0, A, toPx) {
    const t = lt - d0;
    if (t <= 0 || !Array.isArray(it.ray) || it.ray.length < 2) return;
    let vis = it.a != null ? Number(it.a) : 1;
    if (it.hide != null) vis *= clamp(1 - (lt - Number(it.hide)) / 0.3);
    if (vis <= 0) return;
    const P = it.ray.map(q => (toPx ? toPx(q) : [x + Number(q[0]) * w, y + Number(q[1]) * h]));
    const seg = [];
    let total = 0;
    for (let j = 1; j < P.length; j++) { const d = Math.hypot(P[j][0] - P[j - 1][0], P[j][1] - P[j - 1][1]); seg.push(d); total += d; }
    const k = easeInOut(clamp(t / (Number(it.dur) || 1.2)));
    let left = total * k;
    const lw = Math.max(2, (Number(it.lw) || 0.012) * h), col = it.color || '#FFC928';
    ctx.save();
    ctx.globalAlpha = A * vis;
    ctx.strokeStyle = col; ctx.fillStyle = col; ctx.lineWidth = lw; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    if (it.glow) { ctx.shadowColor = col; ctx.shadowBlur = lw * 2.4; }
    if (it.dash) ctx.setLineDash(it.dash.map(v => v * h));
    ctx.beginPath(); ctx.moveTo(P[0][0], P[0][1]);
    let tip = P[0], dir = [P[1][0] - P[0][0], P[1][1] - P[0][1]];
    for (let j = 1; j < P.length && left > 0; j++) {
      const u = Math.min(1, left / Math.max(0.001, seg[j - 1]));
      tip = [lerp(P[j - 1][0], P[j][0], u), lerp(P[j - 1][1], P[j][1], u)];
      dir = [P[j][0] - P[j - 1][0], P[j][1] - P[j - 1][1]];
      ctx.lineTo(tip[0], tip[1]);
      left -= seg[j - 1];
    }
    ctx.stroke();
    if (it.arrow && k > 0.05) {
      const L = Math.hypot(dir[0], dir[1]) || 1, ux = dir[0] / L, uy = dir[1] / L, z = lw * 3.2;
      ctx.setLineDash([]);
      ctx.beginPath(); ctx.moveTo(tip[0] + ux * z * 0.4, tip[1] + uy * z * 0.4);
      ctx.lineTo(tip[0] - ux * z - uy * z * 0.6, tip[1] - uy * z + ux * z * 0.6);
      ctx.lineTo(tip[0] - ux * z + uy * z * 0.6, tip[1] - uy * z - ux * z * 0.6);
      ctx.closePath(); ctx.fill();
    }
    ctx.restore();
  }
  // 标签：一个白底小牌子写字，to: [x, y] 时拉一条细线指过去（指着小孔、倒立的像、镜头）
  function drawLabel(ctx, it, x, y, w, h, lt, d0, A, toPx) {
    const t = lt - d0;
    let vis = clamp(t / 0.35) * (it.a != null ? Number(it.a) : 1);
    if (it.hide != null) vis *= clamp(1 - (lt - Number(it.hide)) / 0.3);
    if (vis <= 0) return;
    const s = String(it.label), z = Math.max(13, (Number(it.size) || 0.07) * h), fam = hasCjk(s) ? ZH : EN;
    const [lx, ly] = toPx ? toPx([it.x, it.y]) : [x + Number(it.x) * w, y + Number(it.y) * h], col = it.color || '#2B3A34';
    setFont(ctx, z, fam, 'bold');
    const tw = ctx.measureText(s).width, bw = tw + z * 0.9, bh = z * 1.55;
    ctx.save();
    ctx.globalAlpha = A * vis;
    if (Array.isArray(it.to)) {
      const [tx, ty] = toPx ? toPx(it.to) : [x + Number(it.to[0]) * w, y + Number(it.to[1]) * h];
      ctx.strokeStyle = it.line || col; ctx.lineWidth = Math.max(1.5, z * 0.09); ctx.setLineDash([]);
      ctx.beginPath(); ctx.moveTo(lx, ly); ctx.lineTo(tx, ty); ctx.stroke();
      ctx.fillStyle = it.line || col; ctx.beginPath(); ctx.arc(tx, ty, Math.max(2.5, z * 0.16), 0, Math.PI * 2); ctx.fill();
    }
    rr(ctx, lx - bw / 2, ly - bh / 2, bw, bh, bh * 0.32);
    ctx.fillStyle = it.bg || 'rgba(255,255,255,.94)'; ctx.fill();
    ctx.lineWidth = Math.max(1.5, z * 0.08); ctx.strokeStyle = it.border || col; ctx.stroke();
    txt(ctx, s, lx, ly + 1, { size: z, family: fam, weight: 'bold', color: col, align: 'center', base: 'middle' });
    ctx.restore();
  }
  // 一段视频里所有的画（意思的画、例句动画、拼起来那一格、来历的画、演变每一步的示意图）
  function allPics(film) {
    const out = [];
    const add = pc => { if (pc && !out.includes(pc)) { out.push(pc); if (pc.exPic) add(pc.exPic); } };
    (film.pics || []).forEach(add);
    if (film.combo && film.combo.pic) add(film.combo.pic);
    if (film.origin && film.origin.pic) add(film.origin.pic);
    (film.flow || []).forEach(st => add(st.fig));
    (film.parts || []).forEach(pt => add(pt.pic));            // 5.11：每部分卡片自己的画
    if (film.dist) film.dist.items.forEach(it => add(it.pic));  // 6.0：同义词辨析每张卡的画
    demoList(film).forEach(D => add(D.pic));                   // 6.7：辨析里每个用法的演示
    return out;
  }
  function demoList(film) {
    const out = [];
    (film.parts || []).forEach(pt => (pt.fgRows || []).forEach(r => (r.uses || []).forEach(u => { if (u.demo) out.push(u.demo); })));
    return out;
  }
  function glyphs(film) {
    const out = new Set(), add = e => { if (e && !/^[\u3400-\u9fff]+$/.test(e) && !/^[A-Za-z0-9]/.test(e)) out.add(String(e)); };
    (film.parts || []).forEach(p => add(p.icon));
    if (film.combo) add(film.combo.icon);
    if (film.origin) add(film.origin.icon);
    if (film.meaning) add(film.meaning.icon);
    (film.route || []).forEach(r => add(r.icon != null ? r.icon : iconFor(r.gloss, '')));
    allPics(film).forEach(q => (q.items || []).forEach(it => add(it.e)));
    (film.flow || []).forEach(s => (s.icons || []).forEach(add));
    demoList(film).forEach(D => { D.terms.forEach(t => add(t.icon)); add(D.icon); });
    ['🔁', '🧑', '🚶'].forEach(add);
    return Array.from(out);
  }
  // 画里用了自己的图片（img）：等图片读完再开始画
  function ready(film) {
    const jobs = [];
    if (typeof Image === 'undefined') return Promise.resolve();
    const load = (o, src) => {
      const im = new Image();
      im.src = /^\s*<svg/i.test(src) ? 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(src) : src;
      o._im = im;
      jobs.push(im.decode ? im.decode().catch(() => {}) : new Promise(r => { im.onload = im.onerror = r; }));
    };
    allPics(film).forEach(pc => {
      if (pc.img && !pc._im) load(pc, pc.img);
      (pc.items || []).forEach(it => { const src = it.svg || it.img; if (src && !it._im) load(it, String(src)); });   // 5.0 起：画里的插图、照片
      (pc.items || []).forEach(it => {                      // 6.24：动图的几帧
        if (Array.isArray(it.frames) && it.frames.length > 1 && !it._fr) it._fr = it.frames.map(src => { const o = {}; load(o, String(src)); return o; });
        if (Array.isArray(it.alt) && it.alt.length && !it._alt) it._alt = it.alt.map(src => { const o = {}; load(o, String(src)); return o; });   // 6.25：emit 轮着用的几张
      });
    });
    return Promise.all(jobs);
  }

  function background(ctx) {
    ctx.fillStyle = C.bg;
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = C.board;
    ctx.fillRect(0, 0, W, 8);
    const g = ctx.createLinearGradient(0, H - 160, 0, H);
    g.addColorStop(0, 'rgba(244,237,220,0)');
    g.addColorStop(1, 'rgba(244,237,220,.7)');
    ctx.fillStyle = g;
    ctx.fillRect(0, H - 160, W, 160);
  }
  function chip(ctx, s, x, y, o) {
    o = o || {};
    const size = o.size || 24;
    setFont(ctx, size, ZH, 'bold');
    const w = ctx.measureText(s).width + size * 1.1, h = size * 1.6;
    const x0 = o.align === 'center' ? x - w / 2 : o.align === 'right' ? x - w : x;
    const a = ctx.globalAlpha;
    if (o.alpha != null) ctx.globalAlpha = a * o.alpha;
    rr(ctx, x0, y - h / 2, w, h, h / 2);
    ctx.fillStyle = o.bg || '#EADFC4'; ctx.fill();
    txt(ctx, s, x0 + w / 2, y + 1, { size, weight: 'bold', color: o.color || '#6E5520', align: 'center', base: 'middle' });
    ctx.globalAlpha = a;
    return w;
  }
  // 6.4：每一幕左上角的“单词 + 这一幕讲什么”、右上角的“二 含义拆分”“① 词根词缀”牌子都不画了
  // （用户：“视频页面比较花……左上角的 produce 按音节一块一块读、右上角的 一 读音拆分都不要了……不要有多余的内容”）。
  // header / secHeader 这两个函数留着（好几幕还在调），只是不画东西；哪一幕要标题，自己在画面里写（“辨析”）
  function header(ctx, film, label, alpha, sec) {}

  // ---------- 单词的字母：连在一起 / 按部分分开（中间有 +）
  function wordLayout(ctx, film, size, gap) {
    const word = film.word;
    setFont(ctx, size, EN, 'bold');
    const chars = word.split('').map((ch, i) => ({ ch, w: ctx.measureText(ch).width, g: film.owner ? film.owner[i] : 0 }));
    const n = film.parts ? film.parts.length : 1;
    let total = chars.reduce((s, c) => s + c.w, 0) + (gap ? gap * (n - 1) : 0);
    let x = (W - total) / 2;
    const out = [];
    chars.forEach((c, i) => {
      if (gap && i > 0 && chars[i - 1].g !== c.g) x += gap;
      out.push({ ch: c.ch, x, w: c.w, g: c.g });
      x += c.w;
    });
    return out;
  }
  // 画单词（k：0 连在一起 → 1 分开）；hi：哪一部分亮着（-1 全亮），dim：其余部分多淡
  function drawWord(ctx, film, o) {
    const k = o.k || 0, y = o.y, size = o.size;
    const joined = wordLayout(ctx, film, size, 0), apart = wordLayout(ctx, film, size, o.gap || size * 0.62);
    const n = film.parts ? film.parts.length : 1;
    const color = g => (film.parts && o.colored ? film.parts[g].color : C.ink);
    const lit = g => (o.hi == null || o.hi < 0 || o.hi === g ? 1 : (o.dim == null ? 0.28 : o.dim));
    // 每部分一块浅色底
    if (o.blocks && film.parts) {
      for (let g = 0; g < n; g++) {
        const cs = apart.map((c, i) => ({ c, j: joined[i] })).filter(x => x.c.g === g);
        if (!cs.length) continue;
        const x0 = lerp(cs[0].j.x, cs[0].c.x, k), x1 = lerp(cs[cs.length - 1].j.x + cs[cs.length - 1].j.w, cs[cs.length - 1].c.x + cs[cs.length - 1].c.w, k);
        const lift = o.hi === g ? (o.lift || 0) : 0;
        const a = ctx.globalAlpha;
        ctx.globalAlpha = a * o.blocks * lit(g);
        rr(ctx, x0 - size * 0.18, y - size * 0.86 - lift, x1 - x0 + size * 0.36, size * 1.12, size * 0.16);
        ctx.fillStyle = tint(film.parts[g].color, 0.86); ctx.fill();
        if (o.hi === g) { ctx.lineWidth = 4; ctx.strokeStyle = film.parts[g].color; ctx.stroke(); }
        ctx.globalAlpha = a;
      }
    }
    joined.forEach((j, i) => {
      const c = apart[i];
      const lift = o.hi === c.g ? (o.lift || 0) : 0;
      const x = lerp(j.x, c.x, k);
      txt(ctx, j.ch, x, y - lift, { size, family: EN, weight: 'bold', color: color(c.g), alpha: lit(c.g) * (o.alpha == null ? 1 : o.alpha) });
    });
    // 部分之间的 +
    if (o.plus && film.parts && n > 1) {
      for (let g = 1; g < n; g++) {
        const prev = apart.filter(c => c.g === g - 1).pop(), next = apart.find(c => c.g === g);
        if (!prev || !next) continue;
        const cx = (prev.x + prev.w + next.x) / 2;
        txt(ctx, '+', cx, y - size * 0.28, { size: size * 0.5, family: ZH, weight: 'bold', color: C.faint, align: 'center', base: 'middle', alpha: o.plus });
      }
    }
  }
  // 没法一个个字母对上的时候：部分一块一块排开
  function drawBlocks(ctx, film, o) {
    const size = o.size, y = o.y, n = film.parts.length;
    setFont(ctx, size, EN, 'bold');
    const ws = film.parts.map(p => ctx.measureText(p.text).width + size * 0.5);
    const gap = size * 0.7;
    let x = (W - ws.reduce((s, w) => s + w, 0) - gap * (n - 1)) / 2;
    film.parts.forEach((p, g) => {
      const lit = o.hi == null || o.hi < 0 || o.hi === g ? 1 : 0.28;
      const lift = o.hi === g ? (o.lift || 0) : 0;
      const a = ctx.globalAlpha;
      ctx.globalAlpha = a * (o.alpha == null ? 1 : o.alpha) * lit;
      rr(ctx, x, y - size * 0.86 - lift, ws[g], size * 1.12, size * 0.16);
      ctx.fillStyle = tint(p.color, 0.86); ctx.fill();
      if (o.hi === g) { ctx.lineWidth = 4; ctx.strokeStyle = p.color; ctx.stroke(); }
      txt(ctx, p.text, x + ws[g] / 2, y - lift, { size, family: EN, weight: 'bold', color: p.color, align: 'center' });
      if (g < n - 1) txt(ctx, '+', x + ws[g] + gap / 2, y - size * 0.28, { size: size * 0.5, weight: 'bold', color: C.faint, align: 'center', base: 'middle' });
      ctx.globalAlpha = a;
      x += ws[g] + gap;
    });
  }
  function strip(ctx, film, o) {
    if (film.owner && !film.dropE) drawWord(ctx, film, Object.assign({ k: 1, colored: true, blocks: 1, plus: 1 }, o));
    else drawBlocks(ctx, film, o);
  }

  // ---------- 图会动：p 是 0～1
  // 方向类动作（出来、进去、越过、向前、向上、向下、回来）里“动的那个东西”：用全身的小人（不用 📤 这类本身就是箭头的图标，
  // 学生看不出谁在动）；别的动法照旧用配到的图
  const DIR_ICONS = new Set(['📤', '📥', '🌉', '⏩', '⏪', '⬆️', '⬇️', '🔁', '🔙', '↔️', '🎯', '➡️', '⬅️']);
  const moverOf = part => (part.iconSet && part.icon ? part : Object.assign({}, part, { icon: '🚶' }));
  // 粗箭头：从 (x1, y1) 画到 (x2, y2)，k 是画到几分之几（0～1），头在终点
  function arrowTo(ctx, x1, y1, x2, y2, k, color, lw) {
    if (k <= 0) return;
    const ex = lerp(x1, x2, k), ey = lerp(y1, y2, k);
    const ang = Math.atan2(y2 - y1, x2 - x1), hd = lw * 2.6;
    ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = lw; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(ex - Math.cos(ang) * hd * 0.6, ey - Math.sin(ang) * hd * 0.6); ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(ex, ey);
    ctx.lineTo(ex - Math.cos(ang - 0.5) * hd, ey - Math.sin(ang - 0.5) * hd);
    ctx.lineTo(ex - Math.cos(ang + 0.5) * hd, ey - Math.sin(ang + 0.5) * hd);
    ctx.closePath(); ctx.fill();
  }
  // 一间小屋（示意“里面 / 外面”）：墙、屋顶，开口朝 side（'right' / 'left'）那一边
  function house(ctx, x0, y0, w, h, side, color) {       // 左上角 (x0, y0)，宽 w、高 h（不算屋顶）；side 那面墙下半截是门洞
    ctx.lineWidth = 6; ctx.strokeStyle = color; ctx.lineJoin = 'round'; ctx.lineCap = 'round';
    ctx.fillStyle = tint(color, 0.9); ctx.fillRect(x0, y0, w, h);
    ctx.beginPath(); ctx.moveTo(x0 - w * 0.1, y0); ctx.lineTo(x0 + w / 2, y0 - h * 0.42); ctx.lineTo(x0 + w * 1.1, y0); ctx.closePath();
    ctx.fillStyle = tint(color, 0.55); ctx.fill(); ctx.stroke();
    const top = y0 + h * 0.2;                               // 门洞上沿：墙只画到这儿
    const R = side === 'right', wx = R ? x0 + w : x0, ox = R ? x0 : x0 + w;
    ctx.beginPath(); ctx.moveTo(wx, top); ctx.lineTo(wx, y0); ctx.lineTo(ox, y0); ctx.lineTo(ox, y0 + h); ctx.stroke();
    ctx.fillStyle = tint(color, 0.7); ctx.fillRect(R ? wx - 5 : wx - 1, top, 6, 4);       // 门框上沿
  }
  // 卡片左边会动的图。box：画框的半宽、半高（东西不能画出去）；size 是“一格”的大小（主角约 0.7 格）
  function act(ctx, part, cx, cy, size, p, box) {
    const m = part.motion, col = part.color || C.board;
    const hw = (box && box.hw) || size * 1.1, hh = (box && box.hh) || size * 1.1;
    const a = ctx.globalAlpha;
    const k = easeInOut(span(p, 0.12, 0.8));
    ctx.lineCap = 'round';
    if (m === 'across') {                // 越过一条线：小人从左边走到右边，中间一条虚线，上面一道弧形箭头
      const mv = moverOf(part), ms = size * 0.7, reach = Math.min(hw - ms * 0.55, size * 0.95);
      ctx.strokeStyle = tint(col, 0.35); ctx.lineWidth = 6; ctx.setLineDash([14, 12]);
      ctx.beginPath(); ctx.moveTo(cx, cy - hh * 0.72); ctx.lineTo(cx, cy + hh * 0.72); ctx.stroke(); ctx.setLineDash([]);
      txt(ctx, '这边', cx - reach * 0.55, cy + hh * 0.72, { size: 22, color: tint(col, 0.2), align: 'center' });
      txt(ctx, '那边', cx + reach * 0.55, cy + hh * 0.72, { size: 22, color: tint(col, 0.2), align: 'center' });
      const x = lerp(cx - reach, cx + reach, k), y = cy + ms * 0.1 - Math.sin(k * Math.PI) * size * 0.4;
      // 弧形箭头跟着走
      const seg = 14, q = Math.max(0.02, k);
      ctx.strokeStyle = col; ctx.lineWidth = 7;
      ctx.beginPath();
      for (let i = 0; i <= seg; i++) { const t = q * i / seg, px = lerp(cx - reach, cx + reach, t), py = cy - ms * 0.75 - Math.sin(t * Math.PI) * size * 0.4; if (i) ctx.lineTo(px, py); else ctx.moveTo(px, py); }
      ctx.stroke();
      if (k > 0.1) { const t2 = q, px = lerp(cx - reach, cx + reach, t2), py = cy - ms * 0.75 - Math.sin(t2 * Math.PI) * size * 0.4, t1 = q - 0.03, qx = lerp(cx - reach, cx + reach, t1), qy = cy - ms * 0.75 - Math.sin(t1 * Math.PI) * size * 0.4; arrowTo(ctx, qx, qy, px, py, 1, col, 7); }
      icon(ctx, Object.assign({}, mv, { flip: true }), x, y, ms);
    } else if (m === 'out' || m === 'in') { // 从屋里走出来 / 走进屋里：屋子贴着一边，门洞朝另一边，小人穿过门洞，粗箭头指方向，“里 / 外”两个字
      const out = m === 'out', mv = moverOf(part);
      const hwid = Math.min(size * 0.9, hw * 0.86), hhgt = Math.min(size * 0.86, hh * 0.84);
      const gy = cy + hh * 0.6;                                         // 地面
      const x0 = out ? cx - hw + 12 : cx + hw - 12 - hwid, y0 = gy - hhgt;
      const door = out ? x0 + hwid : x0;                                // 门洞那面墙
      const ms = Math.min(size * 0.6, hhgt * 0.72);                     // 小人比门洞矮
      const inside = x0 + hwid / 2, outside = out ? cx + hw - ms * 0.45 - 6 : cx - hw + ms * 0.45 + 6;
      ctx.strokeStyle = tint(col, 0.6); ctx.lineWidth = 3;
      ctx.beginPath(); ctx.moveTo(cx - hw + 4, gy); ctx.lineTo(cx + hw - 4, gy); ctx.stroke();
      house(ctx, x0, y0, hwid, hhgt, out ? 'right' : 'left', col);
      txt(ctx, '里', inside, gy + 30, { size: 24, weight: 'bold', color: tint(col, 0.15), align: 'center' });
      txt(ctx, '外', out ? (door + cx + hw) / 2 : (cx - hw + door) / 2, gy + 30, { size: 24, weight: 'bold', color: tint(col, 0.15), align: 'center' });
      const ay = y0 - hhgt * 0.15;                                      // 箭头在门洞上方，从门指向外面（in：从外面指向门）
      const a0 = out ? door + 6 : outside - ms * 0.3, a1 = out ? outside + ms * 0.3 : door - 6;
      arrowTo(ctx, a0, ay, Math.min(cx + hw - 8, Math.max(cx - hw + 8, a1)), ay, Math.max(0.04, k), col, 8);
      const x = out ? lerp(inside, outside, k) : lerp(outside, inside, k);
      icon(ctx, Object.assign({}, mv, { flip: true }), x, gy - ms * 0.48, ms);
    } else if (m === 'back') {          // 绕一圈回来：小人沿着圆圈走一整圈回到起点，圈上有箭头
      const mv = moverOf(part), ms = size * 0.52, r = Math.min(hw, hh) * 0.5;
      ctx.strokeStyle = tint(col, 0.5); ctx.lineWidth = 6;
      ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.stroke();
      const q = Math.max(0.03, k);
      ctx.strokeStyle = col; ctx.lineWidth = 7;
      ctx.beginPath(); ctx.arc(cx, cy, r, -Math.PI / 2, -Math.PI / 2 + q * Math.PI * 2); ctx.stroke();
      const a2 = -Math.PI / 2 + q * Math.PI * 2, a1 = a2 - 0.06;
      arrowTo(ctx, cx + Math.cos(a1) * r, cy + Math.sin(a1) * r, cx + Math.cos(a2) * r, cy + Math.sin(a2) * r, 1, col, 7);
      txt(ctx, '回来', cx, cy, { size: 24, weight: 'bold', color: tint(col, 0.1), align: 'center', base: 'middle' });
      icon(ctx, Object.assign({}, mv, { flip: Math.cos(a2) >= 0 }), cx + Math.cos(a2) * r, cy + Math.sin(a2) * r, ms);
    } else if (m === 'forward') {       // 向前：小人往右走，身后几道速度线，前面一个粗箭头
      const mv = moverOf(part), ms = size * 0.7, reach = Math.min(hw - ms * 0.55, size * 0.9);
      const x = lerp(cx - reach, cx + reach * 0.55, easeOut(span(p, 0.1, 0.7)));
      ctx.strokeStyle = tint(col, 0.45); ctx.lineWidth = 5;
      for (let i = 0; i < 3; i++) { ctx.beginPath(); ctx.moveTo(x - ms * (0.5 + i * 0.05), cy - ms * 0.25 + i * ms * 0.25); ctx.lineTo(x - ms * (0.85 + i * 0.12), cy - ms * 0.25 + i * ms * 0.25); ctx.stroke(); }
      arrowTo(ctx, cx - reach * 0.2, cy - size * 0.62, Math.min(cx + hw - 16, x + ms * 0.9), cy - size * 0.62, Math.max(0.05, span(p, 0.1, 0.7)), col, 8);
      txt(ctx, '前', cx + reach * 0.78, cy + size * 0.62, { size: 24, weight: 'bold', color: tint(col, 0.2), align: 'center' });
      icon(ctx, Object.assign({}, mv, { flip: true }), x, cy, ms);
    } else if (m === 'up' || m === 'down') {   // 向上 / 向下：小人（或配到的东西）顺着一个粗箭头上去 / 下来
      const dir = m === 'up' ? -1 : 1, mv = moverOf(part), ms = size * 0.66, reach = Math.min(hh - ms * 0.55, size * 0.8);
      arrowTo(ctx, cx + size * 0.7, cy - dir * reach * 0.9, cx + size * 0.7, cy + dir * reach * 0.95, Math.max(0.05, k), col, 8);
      txt(ctx, m === 'up' ? '上' : '下', cx + size * 0.7, cy + dir * reach + (dir > 0 ? 40 : -14), { size: 24, weight: 'bold', color: tint(col, 0.2), align: 'center' });
      icon(ctx, mv, cx - size * 0.2, lerp(cy - dir * reach, cy + dir * reach, k), ms);
    } else if (m === 'not') {           // 出现，再被划掉
      icon(ctx, part, cx, cy, size * 0.9);
      const q = easeOut(span(p, 0.45, 0.75));
      if (q > 0) {
        ctx.strokeStyle = C.red; ctx.lineWidth = 9;
        ctx.beginPath(); ctx.arc(cx, cy, size * 0.62, -Math.PI / 2, -Math.PI / 2 + q * Math.PI * 2); ctx.stroke();
        if (q > 0.6) { const r = size * 0.44, z = span(q, 0.6, 1); ctx.beginPath(); ctx.moveTo(cx - r, cy - r); ctx.lineTo(lerp(cx - r, cx + r, z), lerp(cy - r, cy + r, z)); ctx.stroke(); }
      }
    } else if (m === 'together' || m === 'apart') {
      const d0 = m === 'together' ? size * 0.75 : size * 0.1, d1 = m === 'together' ? size * 0.12 : size * 0.75;
      const d = lerp(d0, d1, k);
      icon(ctx, part, cx - d, cy, size * 0.6);
      icon(ctx, part, cx + d, cy, size * 0.6);
    } else if (m === 'person') {
      icon(ctx, part, cx - size * 0.25, cy, size * 0.85);
      const q = easeBack(span(p, 0.4, 0.7));
      if (q > 0 && part.icon !== '🧑') emoji(ctx, '🧑', cx + size * 0.55, cy + size * 0.15, size * 0.55 * q);
    } else if (m === 'many') {
      for (let i = 0; i < 3; i++) { const q = easeBack(span(p, 0.15 + i * 0.15, 0.45 + i * 0.15)); if (q > 0) icon(ctx, part, cx + (i - 1) * size * 0.6, cy + (i === 1 ? -size * 0.15 : size * 0.1), size * 0.55 * q); }
    } else {                            // 弹出来，轻轻晃
      const q = easeBack(span(p, 0.05, 0.4));
      const bob = Math.sin(p * Math.PI * 3) * size * 0.04 * span(p, 0.4, 0.5);
      if (q > 0) icon(ctx, part, cx, cy + bob, size * q);
    }
    ctx.globalAlpha = a;
  }

  // ---------------------------------------------------------------- 一幕一幕
  const fadeOf = (sc, p) => Math.min(1, span(p * sc.dur, 0, 0.35), span((1 - p) * sc.dur, 0, 0.3));
  const S = {};
  // 6.4：开头只有单词和含义（用户：“第一页只要 produce，然后写上含义就可以了，下面的 1，2，3，4 不要了”）：
  // 上面的“① 词根词缀”、下面的“一 读音拆分 → 二 含义拆分 → …”都不画。含义照总表「含义」列，一个词性一行（最多三行）
  function titleMeaning(film) {
    let groups = posGroups(film);
    if (!groups.length || !groups.some(g => g.ab)) return film.meaning && film.meaning.main ? [{ ab: '', text: film.meaning.main }] : [];
    if (groups.length > 3) groups = groups.slice(0, 2).concat([{ ab: '', items: [].concat(...groups.slice(2).map(g => (g.ab ? [g.ab + ' ' + g.items[0]] : []).concat(g.items.slice(g.ab ? 1 : 0)))) }]);
    return groups.map(g => ({ ab: g.ab, text: g.items.join('；') }));
  }
  // 单词和含义合在一起上下居中：size 单词字号，y 单词的基线，my 第一行含义的基线，mz 含义字号，lh 行距
  function titleLayout(ctx, film) {
    const size = fit(ctx, film.word, EN, 'bold', 150, W - 200, 60);
    const lines = titleMeaning(film);
    let mz = 46;
    lines.forEach(l => {
      setFont(ctx, mz * 0.82, EN, 'bold');
      const aw = l.ab ? ctx.measureText(l.ab + ' ').width : 0;
      mz = Math.min(mz, fit(ctx, l.text, ZH, 'bold', mz, W - 220 - aw, 26));
    });
    const lh = mz * 1.5, wordH = size * 0.74, gapM = lines.length ? size * 0.2 + 14 + 86 : size * 0.2 + 14;
    const total = wordH + gapM + (lines.length ? (lines.length - 1) * lh + mz * 0.25 : 0);
    const top = (H - total) / 2;
    return { size, y: top + wordH, lines, mz, lh, my: top + wordH + gapM };
  }
  // 6.27（第六十七版）：开头一幕就是封面，第一帧就画全——上面单词（大字、按拆分的彩色下划线），下面一行含义，再下面是这个词第一个意思的画（里面的人、东西照样会动）。
  // 用户：“我希望视频第一帧能让电脑，手机或者其他平台能识别出这个单词，让学生不点视频就能知道这个视频讲的是哪个词……不仅能看见单词，也能看见单词对应的画面”。
  // 以前单词一个字母一个字母出来，第一帧是空的，文件夹里的缩略图看不出是哪个词。没有画的词（或者 prefs 写 "cover": false）照旧用原来的样子
  S.title = (ctx, film, p, sc) => {
    // 6.27.1（第六十八版，用户：“不是很清楚，可以左右两排，左边单词加含义；右边是画面；画面要放至少两个含义的画面”）：
    // 左边一栏单词（大字、彩色下划线）+ 每个词性一行含义；右边一栏放前两个意思的画（上下两幅，左上角写“① 演讲人、发言人”），只有一个意思就放一幅大的
    const pics = film.cover && film.pics ? film.pics.filter(q => q && Array.isArray(q.items) && q.items.length).slice(0, 2) : [];
    if (!pics.length) return titleClassic(ctx, film, p, sc);
    const out = span((1 - p) * sc.dur, 0, 0.3), tl = sc.tl != null ? sc.tl : p * sc.dur;
    const LX = 64, LW = 540, RX = 630, RW = W - RX - 40;
    // 左栏：先算高度，再上下居中
    const size = fit(ctx, film.word, EN, 'bold', 150, LW, 50);
    const lines = titleMeaning(film).slice(0, 4);
    // 含义：每个词性一段，长的按“；”折成几行（字不缩得太小）；行数多了整体缩一号
    let mz = 36, rows = [];
    for (; mz >= 24; mz -= 2) {
      rows = [];
      lines.forEach(l => {
        setFont(ctx, mz * 0.82, EN, 'bold'); const aw = l.ab ? ctx.measureText(l.ab + ' ').width : 0;
        setFont(ctx, mz, ZH, 'bold');
        wrap(ctx, l.text, LW - aw, 3).forEach((t, k) => rows.push({ ab: k ? '' : l.ab, aw, t }));
      });
      if (rows.length <= 5 || mz <= 24) break;
    }
    const lh = mz * 1.45, blockH = size * 0.8 + 40 + rows.length * lh;
    const wy = (H - blockH) / 2 + size * 0.8;
    setFont(ctx, size, EN, 'bold');
    let x = LX;
    const lay = film.word.split('').map((ch, k) => { const w0 = ctx.measureText(ch).width, o = { ch, x, w: w0, g: film.owner ? film.owner[k] : 0 }; x += w0; return o; });
    lay.forEach(c => txt(ctx, c.ch, c.x, wy, { size, family: EN, weight: 'bold', color: C.ink, alpha: out }));
    if (film.parts && film.owner) {
      const m = film.parts.length;
      for (let g = 0; g < m; g++) {
        const cs = lay.filter(c => c.g === g);
        if (!cs.length) continue;
        const gx0 = cs[0].x + (g ? 5 : 0), gx1 = cs[cs.length - 1].x + cs[cs.length - 1].w - (g < m - 1 ? 5 : 0);
        ctx.globalAlpha = 0.9 * out; rr(ctx, gx0, wy + 16, gx1 - gx0, 13, 6); ctx.fillStyle = film.parts[g].color; ctx.fill();
      }
    } else {
      ctx.globalAlpha = 0.9 * out; rr(ctx, LX, wy + 16, x - LX, 13, 6); ctx.fillStyle = C.marker; ctx.fill();
    }
    ctx.globalAlpha = 1;
    rows.forEach((r, k) => {
      const y = wy + 40 + mz + k * lh;
      if (r.ab) txt(ctx, r.ab, LX, y, { size: mz * 0.82, family: EN, weight: 'bold', color: C.faint, alpha: out });
      txt(ctx, r.t, LX + r.aw, y, { size: mz, weight: 'bold', color: C.soft, alpha: out });
    });
    // 右栏：两幅画上下放（只有一幅就放大）；比例照“现在的意思”那一幕（约 3 : 2）
    const gap = 18, n = pics.length;
    let ph = n === 2 ? (H - 44 - gap) / 2 : Math.min(H - 120, RW / 1.508), pw = ph * 1.508;
    if (pw > RW) { pw = RW; ph = pw / 1.508; }
    const top = (H - (n * ph + (n - 1) * gap)) / 2, px = RX + (RW - pw) / 2;
    pics.forEach((pc, k) => {
      const py = top + k * (ph + gap);
      ctx.globalAlpha = out;
      drawPic(ctx, pc, px, py, pw, ph, { q: 1, lt: 4 + tl });          // lt 从 4 秒算起：第一帧里人、东西都已经出来了
      const cap = (n > 1 ? '①②③'[k] + ' ' : '') + String(pc.text || '');
      if (pc.text) chip(ctx, cap, px + 14, py + 26, { size: 20, bg: 'rgba(255,255,255,.92)', color: C.ink });
      ctx.globalAlpha = 1;
    });
  };
  function titleClassic(ctx, film, p, sc) {
    const out = span((1 - p) * sc.dur, 0, 0.3);
    const L = titleLayout(ctx, film), size = L.size, wy = L.y;
    const lay = wordLayout(ctx, film, size, 0);
    const n = lay.length;
    lay.forEach(c => txt(ctx, c.ch, c.x, wy, { size, family: EN, weight: 'bold', color: C.ink, alpha: out }));   // 6.27：第一帧就画全（做缩略图认得出）
    const u = 1;
    if (u > 0) {
      ctx.globalAlpha = 0.9 * out;
      if (film.parts && film.owner) {
        const m = film.parts.length;
        for (let g = 0; g < m; g++) {
          const cs = lay.filter(c => c.g === g);
          if (!cs.length) continue;
          const gx0 = cs[0].x + (g ? 5 : 0), gx1 = cs[cs.length - 1].x + cs[cs.length - 1].w - (g < m - 1 ? 5 : 0), ug = clamp(u * m - g);
          if (ug > 0) { rr(ctx, gx0, wy + 18, (gx1 - gx0) * ug, 14, 7); ctx.fillStyle = film.parts[g].color; ctx.fill(); }
        }
      } else {
        const x0 = lay[0].x, x1 = lay[n - 1].x + lay[n - 1].w;
        ctx.fillStyle = C.marker;
        rr(ctx, x0, wy + 18, (x1 - x0) * u, 16, 8); ctx.fill();
      }
      ctx.globalAlpha = 1;
    }
    // 含义：词性（v. / n.）小一号、灰一点，后面是意思；一个词性一行，居中
    const qm = out;
    if (qm > 0) L.lines.forEach((l, i) => {
      const az = L.mz * 0.82, y = L.my + i * L.lh;
      setFont(ctx, az, EN, 'bold');
      const aw = l.ab ? ctx.measureText(l.ab + ' ').width : 0;
      const ft = fitLine(ctx, l.text, ZH, 'bold', L.mz, W - 220 - aw, 24);
      setFont(ctx, ft.z, ZH, 'bold');
      const x = (W - aw - ctx.measureText(ft.t).width) / 2;
      if (l.ab) txt(ctx, l.ab, x, y, { size: az, family: EN, weight: 'bold', color: C.faint, alpha: qm });
      txt(ctx, ft.t, x + aw, y, { size: ft.z, weight: 'bold', color: C.soft, alpha: qm });
    });
  }
  // ---------------------------------------------------------------- 5.0 起：一、读音拆分
  // 进度条、右上角的小牌子：6.4 起不画了（progressPills、secChip 留着没人调）
  function progressPills(ctx, film, k, y, alpha) {
    const secs = film.sections || [], n = secs.length;
    const items = secs.map(x => x.no + ' ' + x.name);
    const size = n >= 4 ? 22 : 24, gap = n >= 4 ? 52 : 76;
    setFont(ctx, size, ZH, 'bold');
    const ws = items.map(t => ctx.measureText(t).width + size * 1.1);
    let x = (W - ws.reduce((a, b) => a + b, 0) - gap * (n - 1)) / 2;
    items.forEach((t, i) => {
      const on = k < 0 || i === k;                     // k = -1：开头那一幕，几部分都亮
      chip(ctx, t, x, y, { size, bg: on ? secs[i].color : '#ECE5D4', color: on ? '#FFFFFF' : '#A0957C', alpha });
      x += ws[i];
      if (i < n - 1) { txt(ctx, '→', x + gap / 2, y + 2, { size: 28, weight: 'bold', color: '#C9BFA6', align: 'center', base: 'middle', alpha }); x += gap; }
    });
  }
  // 右上角的小牌子：现在在第几部分
  function secChip(ctx, film, name, x, y, alpha) {
    const sec = (film.sections || []).find(z => z.name === name);
    if (!sec || !film.showSec) return 0;
    return chip(ctx, sec.no + ' ' + sec.name, x, y, { size: 20, align: 'right', bg: tint(sec.color, 0.84), color: sec.color, alpha });
  }
  // 6.4：分段标题这一幕只写标题四个字（用户：“第二页只写 读音拆分，其他的不要……含义拆分也是一样”）：
  // 上面的单词、圆圈里的“一”、下面那句小字和进度条都不画；标题下面留一道这一部分颜色的线
  S.sec = (ctx, film, p, sc) => {
    const sec = (film.sections || [])[sc.i || 0] || { no: '', name: '', sub: '', color: SEC_C[0] };
    const col = sec.color, f = fadeOf(sc, p), title = (sec.no ? sec.no + '、' : '') + sec.name;      // 6.5：标题前面加编号（用户：“读音拆分前面要加“一、”；其他的也一样”）
    const q2 = easeOut(span(p, 0.04, 0.34)), q3 = easeOut(span(p, 0.24, 0.56));
    const tz = title.length >= 5 ? 116 : 132;
    setFont(ctx, tz, ZH, 'bold');
    // 6.7：标题下面不画线（用户：“一、读音拆分 下面不要画线，二，三，四也是一样”），标题自己上下居中
    const tw = ctx.measureText(title).width, tx = (W - tw) / 2, by = H / 2 + tz * 0.36;
    txt(ctx, title, tx + (1 - q2) * 26, by, { size: tz, weight: 'bold', color: C.ink, alpha: f * q2 });
    void col; void q3;
  };
  function secHeader(ctx, film, k, label, alpha) {}       // 6.4：不画了，见 header
  // 一块一块排开（k = 1，中间放 +）或连成一个词（k = 0）：每一块、每个字母的位置
  function pronLayout(ctx, pron, size, k) {
    setFont(ctx, size, EN, 'bold');
    const gap = size * 0.78;
    const blocks = pron.chunks.map(c => { const letters = c.L.map(x => ({ x, w: ctx.measureText(x.c).width })); return { c, letters, w: letters.reduce((a, l) => a + l.w, 0) }; });
    const n = blocks.length;
    let xx = (W - blocks.reduce((a, b) => a + b.w, 0) - gap * Math.max(0, n - 1) * k) / 2;
    blocks.forEach((b, i) => { b.x = xx; let lx = xx; b.letters.forEach(l => { l.lx = lx; lx += l.w; }); xx += b.w + (i < n - 1 ? gap * k : 0); });
    return blocks;
  }
  function pronSize(ctx, pron, max, maxW) {
    let z = max;
    while (z > 40) {
      const b = pronLayout(ctx, pron, z, 1);
      if (b[b.length - 1].x + b[b.length - 1].w - b[0].x + z * 0.4 < maxW) break;
      z -= 4;
    }
    return z;
  }
  // 字母照音节表的样子画：红色划掉 = 不发音，蓝色下划线 = 固定组合（两组挨着用单线、双线），绿色 = 读字母音，紫色 = 特殊读音
  function sylLetters(ctx, b, y, size, alpha, lift, hi) {
    const a0 = ctx.globalAlpha;
    b.letters.forEach((l, li) => {
      const L = l.x, yy = y - (lift || 0);
      const col = b.c.sep ? C.faint : L.silent ? SYL_C.silent : L.k === 'long' ? SYL_C.long : L.k === 'special' ? SYL_C.special : L.u ? SYL_C.combo : C.ink;
      if (hi && hi.has(li)) { ctx.globalAlpha = a0 * alpha; rr(ctx, l.lx - 4, yy - size * 0.8, l.w + 8, size * 1.02, 10); ctx.fillStyle = '#FFE38A'; ctx.fill(); }
      txt(ctx, L.c, l.lx, yy, { size, family: EN, weight: 'bold', color: col, alpha: alpha * (L.silent ? 0.88 : 1) });
      ctx.globalAlpha = a0 * alpha;
      if (L.silent) { ctx.fillStyle = SYL_C.silent; ctx.fillRect(l.lx - 3, yy - size * 0.33, l.w + 6, Math.max(3, size * 0.05)); }
      if (L.u) {
        ctx.fillStyle = col;
        const th = Math.max(2.5, size * 0.035);
        ctx.fillRect(l.lx, yy + size * 0.12, l.w + 0.5, th);
        if (L.u === 2) ctx.fillRect(l.lx, yy + size * 0.12 + th * 2.2, l.w + 0.5, th);
      }
      ctx.globalAlpha = a0;
    });
  }
  // 小喇叭和声波：6.16 起不画了（用户：“读单词，句子的时候，喇叭不要出现，有点多余”），留着没人调
  function soundWaves(ctx, x, y, r, t, alpha) {
    ctx.save(); ctx.translate(x, y);
    ctx.globalAlpha = alpha; ctx.fillStyle = SYL_C.hi; ctx.strokeStyle = SYL_C.hi; ctx.lineWidth = Math.max(3, r * 0.13); ctx.lineCap = 'round';
    ctx.beginPath(); ctx.moveTo(-r * 0.8, -r * 0.24); ctx.lineTo(-r * 0.5, -r * 0.24); ctx.lineTo(-r * 0.12, -r * 0.55); ctx.lineTo(-r * 0.12, r * 0.55); ctx.lineTo(-r * 0.5, r * 0.24); ctx.lineTo(-r * 0.8, r * 0.24); ctx.closePath(); ctx.fill();
    for (let j = 0; j < 3; j++) { const ph = (t * 1.5 + j / 3) % 1; ctx.globalAlpha = alpha * (1 - ph); ctx.beginPath(); ctx.arc(-r * 0.05, 0, r * (0.3 + 0.75 * ph), -0.75, 0.75); ctx.stroke(); }
    ctx.restore();
  }
  // 图例：这个词用到了哪几种标注，就写哪几种
  // 6.21：图例的示例用这个词自己的字母。以前写死 e / ch / a / u——speaker 下面写着“ch 蓝色下划线：固定组合”，
  // 用户：“为什么会说 ch，难道是和 speech 混淆了？”（speaker 自己的固定组合是 ea、er）。现在取这个词里第一处这样标的字母
  function sylSamples(pr) {
    const out = { silent: '', combo: '', comboPlain: '', long: '', special: '' };
    (pr.chunks || []).forEach(c => {
      if (c.sep) return;
      const run = { silent: '', long: '', special: '', combo: '' };
      let pu = 0, plain = true;
      const flush = k => {
        if (!run[k]) return;
        if (k === 'combo') { if (!out.combo) out.combo = run[k]; if (plain && !out.comboPlain) out.comboPlain = run[k]; }
        else if (!out[k]) out[k] = run[k];
        run[k] = '';
      };
      (c.L || []).forEach(L => {
        const kind = { silent: !!L.silent, long: !L.silent && L.k === 'long', special: !L.silent && L.k === 'special' };
        ['silent', 'long', 'special'].forEach(k => { if (kind[k]) run[k] += L.c; else flush(k); });
        if (L.u && (L.u === pu || !run.combo)) { if (!run.combo) plain = true; run.combo += L.c; if (L.silent || L.k) plain = false; }
        else { flush('combo'); if (L.u) { run.combo = L.c; plain = !(L.silent || L.k); } }
        pu = L.u || 0;
      });
      ['silent', 'long', 'special', 'combo'].forEach(flush);
    });
    return out;
  }
  function sylLegend(ctx, pr, y, alpha) {
    const m = pr.marks || {}, items = [], sm = sylSamples(pr);
    if (m.silent) items.push([sm.silent || 'e', '红色划掉：不发音', SYL_C.silent, 'strike']);
    if (m.combo) items.push([sm.comboPlain || sm.combo || 'ch', '蓝色下划线：固定组合', SYL_C.combo, 'under']);
    if (m.long) items.push([sm.long || 'a', '绿色：读字母音', SYL_C.long, '']);
    if (m.special) items.push([sm.special || 'u', '紫色：特殊读音', SYL_C.special, '']);
    if (!items.length || alpha <= 0) return;
    const gap = 44;
    const ws = items.map(([smp, lab]) => { setFont(ctx, 30, EN, 'bold'); const a = ctx.measureText(smp).width; setFont(ctx, 22, ZH); return a + 10 + ctx.measureText(lab).width; });
    let x = (W - ws.reduce((a, b) => a + b, 0) - gap * (items.length - 1)) / 2;
    const a0 = ctx.globalAlpha;
    items.forEach(([smp, lab, col, st], i) => {
      setFont(ctx, 30, EN, 'bold');
      const sw = ctx.measureText(smp).width;
      txt(ctx, smp, x, y, { size: 30, family: EN, weight: 'bold', color: col, alpha });
      ctx.globalAlpha = a0 * alpha; ctx.fillStyle = col;
      if (st === 'strike') ctx.fillRect(x - 2, y - 10, sw + 4, 3);
      if (st === 'under') ctx.fillRect(x, y + 4, sw, 3);
      ctx.globalAlpha = a0;
      txt(ctx, lab, x + sw + 10, y - 2, { size: 22, color: C.soft, alpha });
      x += ws[i] + gap;
    });
  }
  // 念哪一块时，“不单独发音”的块（mo + re 的 re）跟着前面那一块
  const readOwner = (pr, ci) => { for (let j = ci; j >= 0; j--) if (pr.read.includes(j)) return j; return -1; };
  // 读音拆分：单词分成几块；配音一块一块念（每一块的音），念到的那一块亮起来、往上浮、下面出音标（6.16 起上面不画小喇叭）；
  // 再“连起来”念整词，几块合回一个词，下面写整词的音标；最后说重音在哪一块。
  // marks：每一块一项，“连起来”一项，“重音”一项（单音节的词没有重音这一项；对不齐的词只有“连起来”一项）
  S.syl = (ctx, film, p, sc) => {
    const pr = film.pron, f = fadeOf(sc, p), tl = sc.tl != null ? sc.tl : p * sc.dur;
    const R = pr.read, nr = R.length, real = pr.chunks.filter(c => !c.sep).length, multi = real > 1;
    const hasStress = pr.stress >= 0 && nr > 1;
    const nItems = (pr.ok ? nr : 0) + (multi || !pr.ok ? 1 : 0) + (hasStress ? 1 : 0);
    const mk = sc.marks && sc.marks.length >= nItems ? sc.marks : null;
    const at = i => (mk ? mk[i] : 1.0 + i * 1.1);
    const tMerge = !multi ? 1e9 : pr.ok ? at(nr) : at(0);
    const tStress = hasStress ? at(nr + 1) : 1e9;
    const kSplit = multi ? easeInOut(clamp((tl - 0.25) / 0.5)) : 0;
    const kJoin = multi ? easeInOut(clamp((tl - tMerge) / 0.6)) : 0;
    const k = kSplit * (1 - kJoin);
    const size = pronSize(ctx, pr, 132, W - 220), y = 350;        // 6.4：左上角、右上角的字去掉了，画面上下居中（原来 368）
    const blocks = pronLayout(ctx, pr, size, k);
    let act = -1;
    if (pr.ok) R.forEach((ci, j) => { if (tl >= at(j) - 0.05 && tl < (j + 1 < nr ? at(j + 1) : Math.min(tMerge, at(j) + 1.6)) - 0.05) act = ci; });
    const doneAt = ci => { const j = R.indexOf(readOwner(pr, ci)); return j >= 0 ? at(j) : 1e9; };
    // 重音：重读的那一块底下垫一层黄
    const qs = tl >= tStress ? easeBack(clamp((tl - tStress) / 0.4)) : 0;
    if (qs > 0 && blocks[pr.stress]) {
      const b = blocks[pr.stress];
      ctx.save(); ctx.globalAlpha = f * Math.min(1, qs) * 0.6; rr(ctx, b.x - 10, y - size * 0.86, b.w + 20, size * 1.1, 14); ctx.fillStyle = '#FFE58A'; ctx.fill(); ctx.restore();
    }
    blocks.forEach((b, ci) => {
      if (b.c.sep) { sylLetters(ctx, b, y, size, f, 0); return; }
      const own = readOwner(pr, ci), on = act >= 0 && own === act;
      const lift = on ? 14 * easeOut(clamp((tl - doneAt(ci)) / 0.25)) : 0;
      if (k > 0.01) {
        const pad = size * 0.16;
        ctx.save(); ctx.globalAlpha = f * k;
        rr(ctx, b.x - pad, y - size * 0.92 - lift, b.w + pad * 2, size * 1.26, size * 0.18);
        if (on) { ctx.shadowColor = 'rgba(240,165,0,.45)'; ctx.shadowBlur = 22; }
        ctx.fillStyle = on ? '#FFF6DA' : '#FFFFFF'; ctx.fill();
        ctx.shadowBlur = 0; ctx.lineWidth = on ? 4 : 2; ctx.strokeStyle = on ? SYL_C.hi : C.line; ctx.stroke();
        ctx.restore();
      }
      const waiting = pr.ok && k > 0.5 && !on && tl < doneAt(ci) && tl >= at(0) - 0.05;     // 开始念以后，还没念到的淡一点
      sylLetters(ctx, b, y, size, f * (waiting ? 0.42 : 1), lift);
      if (pr.ok && k > 0.3 && own === ci && b.c.ipa) {
        const qi = clamp((tl - doneAt(ci)) / 0.3);
        const qo = 1 - clamp(kJoin * 2.2);                                   // 合起来时先退掉
        if (qi > 0 && qo > 0) txt(ctx, '/' + b.c.ipa + '/', b.x + b.w / 2, y + size * 0.66, { size: Math.min(46, Math.max(28, size * 0.36)), family: IPA, color: on ? '#A86E00' : C.soft, align: 'center', alpha: f * qi * qo });
      }
      // 6.16：念到的这一块上面不画小喇叭（用户：“读单词，句子的时候，喇叭不要出现，有点多余”）；这一块照旧亮起来、往上浮
    });
    if (k > 0.05) for (let i = 1; i < blocks.length; i++) {
      const a = blocks[i - 1], b = blocks[i];
      if (a.c.sep || b.c.sep) continue;
      txt(ctx, '+', (a.x + a.w + b.x) / 2, y - size * 0.32, { size: size * 0.42, weight: 'bold', color: C.faint, align: 'center', base: 'middle', alpha: f * k });
    }
    // 连起来：整词的音标（一块的词，念完就出来）
    const qj = multi ? clamp(kJoin * 2 - 0.9) : pr.ok ? clamp((tl - at(0)) / 0.4) : 0;
    if (qj > 0 && pr.ipa) {
      txt(ctx, '/' + pr.ipa + '/', W / 2, y + 122, { size: 56, family: IPA, color: C.ink, align: 'center', alpha: f * qj });
      // 6.16：连起来念整词时，单词左边也不画小喇叭
    }
    if (qs > 0 && blocks[pr.stress]) {
      const b = blocks[pr.stress], cx = b.x + b.w / 2, top = y - size * 0.98;
      ctx.save(); ctx.globalAlpha = f * Math.min(1, qs);
      ctx.fillStyle = SYL_C.hi; ctx.beginPath(); ctx.moveTo(cx - 12, top - 22); ctx.lineTo(cx + 12, top - 22); ctx.lineTo(cx, top - 6); ctx.closePath(); ctx.fill();
      ctx.restore();
      chip(ctx, '重音', cx, top - 46, { size: 24, align: 'center', bg: SYL_C.hi, color: '#FFFFFF', alpha: f * Math.min(1, qs) });
    }
    sylLegend(ctx, pr, y + 210, f * clamp((tl - 0.4) / 0.5));
  };
  // 关键解释这一条讲的是哪几个字母（du、tion、a_e…），在上面的单词里标黄
  // 6.26（第六十三版）：「读音现象」列（维护技能 duyin.py，第 124 条）：一行一个现象——【清辅音浊化】sp：s 后面的 p 不送气，听起来像 /b/。为什么：……
  // 用户：“speaker，这里的 p 读成了 b，但是视频没有讲出来……不光要讲出这个现象，还要说为什么会这样”“视频里面就放在读音拆分这部分进行讲解”
  function duyinOf(text) {
    return String(text || '').split(/\n+/).map(z => z.trim()).filter(Boolean).map(z => {
      const m = /^【([^】]+)】([^：:]*)[：:]([\s\S]*)$/.exec(z);
      if (!m) return null;
      // 6.26.2（第六十五版）：一行是“现象。为什么：…。试一试：…。一句话：…。（例词）”——视频念“一句话”（抓重点、视频不拖长），画面上加“试一试”
      const body = m[3], k = body.indexOf('为什么：');
      let why = k >= 0 ? body.slice(k + 4).trim() : '', ex = '';
      const em = /（[^（）]*）$/.exec(why);
      if (em && why.indexOf('一句话：') >= 0) { ex = em[0]; why = why.slice(0, em.index).trim(); }
      const ks = why.indexOf('一句话：'), short = ks >= 0 ? why.slice(ks + 4).trim() : '';
      if (ks >= 0) why = why.slice(0, ks).trim();
      const kt = why.indexOf('试一试：'), tryit = kt >= 0 ? why.slice(kt + 4).trim() : '';
      if (kt >= 0) why = why.slice(0, kt).trim();
      return { tag: m[1].trim(), letters: m[2].trim(), what: (k >= 0 ? body.slice(0, k) : body).trim(), why, tryit, short, ex };
    }).filter(Boolean);
  }
  function noteLetters(pr, line) {
    const m = /^\s*-?([A-Za-z]+)(?:_([A-Za-z]))?/.exec(String(line || ''));
    const out = new Map();
    if (!m) return out;
    const flat = [];
    pr.chunks.forEach((c, ci) => c.L.forEach((x, li) => { if (!c.sep) flat.push({ ci, li, x }); }));
    const s = flat.map(q => q.x.c.toLowerCase()).join(''), g = m[1].toLowerCase();
    const marked = i => flat[i].x.k || flat[i].x.u || flat[i].x.silent;
    let best = -1;
    for (let i = s.indexOf(g); i >= 0; i = s.indexOf(g, i + 1)) {
      if (best < 0) best = i;
      if (flat.slice(i, i + g.length).some((q, j) => marked(i + j))) { best = i; break; }
    }
    if (best < 0) return out;
    const put = i => { const q = flat[i]; if (!out.has(q.ci)) out.set(q.ci, new Set()); out.get(q.ci).add(q.li); };
    for (let j = 0; j < g.length; j++) put(best + j);
    if (m[2]) { const e = s.indexOf(m[2].toLowerCase(), best + g.length + 1); if (e >= 0) put(e); }
    return out;
  }
  // 6.3：元辅e 的关键解释（音节表写“u_e：e 不发音，让 u 读字母音 /juː/”）画面上写规则的名字“元辅e结尾”，括号里是这个词里的那几个字母（uce、ame、ome）
  // ——用户：“对于 uce、name、home 这种元音 + 辅音 + e 结尾的，就写发音规则就可以了，元辅e结尾”。别的解释照旧“冒号前是标题、冒号后是正文”
  function noteShow(pr, ln) {
    const s = String(ln || ''), k2 = s.indexOf('：');
    let head = k2 > 0 ? s.slice(0, k2) : s;
    const body = k2 > 0 ? s.slice(k2 + 1) : '';
    if (/^\s*[aeiouy]_e\s*$/i.test(head)) {
      const hi = noteLetters(pr, ln), flat = [];
      pr.chunks.forEach((c, ci) => c.L.forEach((x, li) => { if (!c.sep) flat.push({ on: !!(hi.get(ci) && hi.get(ci).has(li)), c: x.c }); }));
      let a = -1, b = -1;
      flat.forEach((q, i) => { if (q.on) { if (a < 0) a = i; b = i; } });
      const vce = a >= 0 && b > a && b - a <= 4 ? flat.slice(a, b + 1).map(q => q.c).join('').toLowerCase() : '';
      head = '元辅e结尾' + (vce ? '（' + vce + '）' : '');
    }
    return { head, body };
  }
  // 关键解释（音节表第三列）：上面是分好的块，下面一条一张卡；说到哪一条，哪张卡出来，上面这几个字母标黄
  S.sylnote = (ctx, film, p, sc) => {
    const pr = film.pron, f = fadeOf(sc, p), tl = sc.tl != null ? sc.tl : p * sc.dur;
    const n = pr.note.length, mk = sc.marks && sc.marks.length >= n ? sc.marks : null;
    const at = i => (mk ? mk[i] : 0.5 + i * 3.4);
    let cur = -1;
    for (let i = 0; i < n; i++) if (tl >= at(i) - 0.05) cur = i;
    const hi = cur >= 0 ? noteLetters(pr, pr.note[cur]) : new Map();
    // 6.4：上面分好的块和下面的卡片合在一起上下居中（原来块在 236、卡片从 352 起，上面留着页眉的位置）
    const ch = n === 1 ? 150 : n === 2 ? 124 : 100, gapc = 18, x0 = 130, cw = W - 260;
    const size = pronSize(ctx, pr, 96, W - 300);
    const y = Math.round(Math.max(size * 0.92 + 24, (H - (size * 0.92 + 116 + n * ch + (n - 1) * gapc)) / 2 + size * 0.92));
    const blocks = pronLayout(ctx, pr, size, 1);
    blocks.forEach((b, ci) => {
      if (!b.c.sep) {
        const pad = size * 0.15;
        ctx.save(); ctx.globalAlpha = f; rr(ctx, b.x - pad, y - size * 0.92, b.w + pad * 2, size * 1.26, size * 0.18);
        ctx.fillStyle = '#FFFFFF'; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = C.line; ctx.stroke(); ctx.restore();
      }
      sylLetters(ctx, b, y, size, f, 0, hi.get(ci));
      if (pr.ok && b.c.ipa) txt(ctx, '/' + b.c.ipa + '/', b.x + b.w / 2, y + size * 0.7, { size: Math.min(34, size * 0.34), family: IPA, color: C.soft, align: 'center', alpha: f });
    });
    for (let i = 1; i < blocks.length; i++) {
      const a = blocks[i - 1], b = blocks[i];
      if (!a.c.sep && !b.c.sep) txt(ctx, '+', (a.x + a.w + b.x) / 2, y - size * 0.32, { size: size * 0.42, weight: 'bold', color: C.faint, align: 'center', base: 'middle', alpha: f });
    }
    pr.note.forEach((ln, i) => {
      const q = easeOut(clamp((tl - at(i) + 0.1) / 0.45));
      if (q <= 0) return;
      const yy = y + 116 + i * (ch + gapc) + (1 - q) * 16, on = i === cur;
      ctx.save(); ctx.globalAlpha = f * q;
      ctx.shadowColor = 'rgba(60,50,20,.10)'; ctx.shadowBlur = 16; ctx.shadowOffsetY = 4;
      rr(ctx, x0, yy, cw, ch, 18); ctx.fillStyle = on ? '#FFFBEB' : C.card; ctx.fill();
      ctx.shadowBlur = 0; ctx.lineWidth = on ? 3 : 2; ctx.strokeStyle = on ? '#F0D25A' : C.line; ctx.stroke();
      rr(ctx, x0, yy, 10, ch, 5); ctx.fillStyle = on ? SYL_C.hi : '#D9C59A'; ctx.fill();
      const { head, body } = noteShow(pr, ln);                                  // 6.3：元辅e 的写规则的名字
      const hz = n >= 3 ? 30 : 34;
      txt(ctx, head, x0 + 34, yy + (body ? hz + 18 : ch / 2 + hz * 0.35), { size: hz, weight: 'bold', color: C.ink });
      if (body) para(ctx, body, x0 + 34, yy + hz + 18 + hz * 1.25, cw - 64, { size: n >= 3 ? 24 : 27, color: C.soft, maxLines: n >= 3 ? 1 : 2, lh: 1.4 });
      ctx.restore();
    });
  };
  // 6.26：清辅音浊化的演示——嘴前面挂一张小纸条：词头的 /p/ 送气，纸条一下被吹开；s 后面的 /p/ 不送气，纸条几乎不动（课堂上常做的小实验）
  function aspDemo(ctx, X, x, y, w, h, tl) {
    const v = (/像 \/([bdɡg])\//.exec(X.what) || [])[1] || 'b', st = { b: 'p', d: 't', 'ɡ': 'k', g: 'k' }[v];
    const pw = (w - 16) / 2;
    [[0, true], [1, false]].forEach(([k, asp]) => {
      const px = x + k * (pw + 16), cy = y + h * 0.42, hx = px + pw * 0.22, r = Math.min(26, h * 0.2);
      ctx.save();
      rr(ctx, px, y, pw, h, 12); ctx.fillStyle = asp ? '#FFF4E5' : '#EEF6FF'; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = asp ? '#F5B971' : '#9CC3EE'; ctx.stroke();
      ctx.beginPath(); ctx.arc(hx, cy, r, 0, Math.PI * 2); ctx.fillStyle = '#FBE3CC'; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = '#1B1A1F'; ctx.stroke();
      ctx.beginPath(); ctx.arc(hx + r * 0.2, cy - r * 0.25, r * 0.12, 0, Math.PI * 2); ctx.fillStyle = '#1B1A1F'; ctx.fill();
      const ph = (tl % 1.6) / 1.6, burst = asp ? Math.exp(-Math.pow((ph - 0.18) / 0.07, 2)) : 0;
      ctx.beginPath(); ctx.ellipse(hx + r * 0.9, cy + r * 0.35, r * 0.18, r * (0.1 + 0.18 * burst), 0, 0, Math.PI * 2); ctx.fillStyle = '#C2410C'; ctx.fill();
      const sx = px + pw * 0.62, sy = y + h * 0.16, len = h * 0.5;
      const ang = asp ? 0.75 * Math.max(0, Math.sin(Math.min(1, Math.max(0, (ph - 0.12) / 0.5)) * Math.PI)) : 0.05 * Math.sin(tl * 3);
      ctx.beginPath(); ctx.moveTo(sx - 16, sy); ctx.lineTo(sx + 16, sy); ctx.lineWidth = 4; ctx.strokeStyle = '#6B7280'; ctx.stroke();
      ctx.save(); ctx.translate(sx, sy); ctx.rotate(-ang); ctx.fillStyle = '#FFFFFF'; ctx.fillRect(-5, 0, 10, len); ctx.lineWidth = 2; ctx.strokeStyle = '#1B1A1F'; ctx.strokeRect(-5, 0, 10, len); ctx.restore();
      if (asp && burst > 0.05) {
        ctx.globalAlpha *= Math.min(1, burst * 1.5); ctx.strokeStyle = '#F59E0B'; ctx.lineWidth = 3; ctx.lineCap = 'round';
        for (let j = -1; j <= 1; j++) { ctx.beginPath(); ctx.moveTo(hx + r * 1.25, cy + r * 0.35 + j * 7); ctx.lineTo(hx + r * 1.25 + (sx - hx - r * 1.6) * (0.5 + 0.5 * burst), cy + r * 0.35 + j * 9); ctx.stroke(); }
      }
      ctx.restore();
      txt(ctx, asp ? '词头的 /' + st + '/：送气' : 's 后面的 /' + st + '/：不送气', px + pw / 2, y + h - 14, { size: 17, weight: 'bold', color: asp ? '#B45309' : '#1D4ED8', align: 'center' });
    });
  }
  // 6.26：读音现象——一个现象一幕：上面是分好的块（讲到的字母标黄），下面白卡片“读音现象 · 类别”+ 大字讲现象，
  // 说到“为什么呢”时黄框“为什么”出来（括号里的例词、古英语写法画面上写、配音不念）
  S.duyin = (ctx, film, p, sc) => {
    const pr = film.pron, X = film.duyin[sc.i] || film.duyin[0], f = fadeOf(sc, p), tl = sc.tl != null ? sc.tl : p * sc.dur;
    if (!X) return;
    const mk = sc.marks && sc.marks.length >= 2 ? sc.marks : null, t1 = mk ? mk[1] : sc.dur * 0.42;
    const hi = noteLetters(pr, X.letters.replace(/\s+/g, ''));
    const size = pronSize(ctx, pr, 84, W - 360);
    let y = 132;
    {   // 6.26.2：整幕上下居中（“为什么”框按内容高矮画以后，下面会空一块）
      const cwq = W - 240, mainQ = film.brief ? '' : (X.short || X.why);      // 6.33：精简版没有“为什么”框
      let hq = 0;
      if (mainQ) { setFont(ctx, 30, ZH, 'normal'); hq = 66 + wrap(ctx, mainQ, cwq - 60, 99).length * 30 * 1.42 + (X.tryit ? 62 : 14) + 20; }
      const bottom = y + size * 0.66 + 38 + 150 + hq;
      y += Math.max(0, Math.min(90, (H - 30 - bottom) / 2));
    }
    const blocks = pronLayout(ctx, pr, size, 1);
    blocks.forEach((b, ci) => {
      if (!b.c.sep) {
        const pad = size * 0.15;
        ctx.save(); ctx.globalAlpha = f; rr(ctx, b.x - pad, y - size * 0.92, b.w + pad * 2, size * 1.26, size * 0.18);
        ctx.fillStyle = '#FFFFFF'; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = C.line; ctx.stroke(); ctx.restore();
      }
      sylLetters(ctx, b, y, size, f, 0, hi.get(ci));
      if (pr.ok && b.c.ipa) txt(ctx, '/' + b.c.ipa + '/', b.x + b.w / 2, y + size * 0.66, { size: Math.min(30, size * 0.34), family: IPA, color: C.soft, align: 'center', alpha: f });
    });
    for (let i = 1; i < blocks.length; i++) {
      const a = blocks[i - 1], b = blocks[i];
      if (!a.c.sep && !b.c.sep) txt(ctx, '+', (a.x + a.w + b.x) / 2, y - size * 0.32, { size: size * 0.42, weight: 'bold', color: C.faint, align: 'center', base: 'middle', alpha: f });
    }
    const x0 = 120, cw = W - 240, q0 = easeOut(clamp((tl - 0.15) / 0.45));
    const c1y = y + size * 0.66 + 38 + (1 - q0) * 14, c1h = 150;
    ctx.save(); ctx.globalAlpha = f * q0;
    ctx.shadowColor = 'rgba(60,50,20,.10)'; ctx.shadowBlur = 16; ctx.shadowOffsetY = 4;
    rr(ctx, x0, c1y, cw, c1h, 18); ctx.fillStyle = C.card; ctx.fill(); ctx.shadowBlur = 0;
    ctx.lineWidth = 3; ctx.strokeStyle = '#F0D25A'; ctx.stroke();
    rr(ctx, x0, c1y, 10, c1h, 5); ctx.fillStyle = SYL_C.hi; ctx.fill();
    chip(ctx, '读音现象 · ' + X.tag, x0 + 32, c1y + 30, { size: 21, bg: '#FDE68A', color: '#92400E' });
    const wz = fit(ctx, X.what.replace(/（[^（）]*）/g, ''), ZH, 'bold', 36, cw - 70, 24);
    const demo = X.tag === '清辅音浊化';
    para(ctx, X.what, x0 + 32, c1y + 92, demo ? cw * 0.5 : cw - 64, { size: Math.max(26, Math.min(34, wz)), weight: 'bold', color: C.ink, maxLines: 2, lh: 1.35 });
    if (demo) aspDemo(ctx, X, x0 + cw * 0.53, c1y + 12, cw * 0.45, c1h - 24, tl);
    ctx.restore();
    const q1 = X.why && !film.brief ? easeOut(clamp((tl - t1 + 0.1) / 0.45)) : 0;      // 6.33：原因放到详解版讲
    if (q1 > 0) {
      // 6.26.2：框按内容的高矮来画（不再一直铺到底、下面空一大块）：标题“为什么”、一句话（大字，视频念的）、试一试（绿色牌子 + 一行字，画面上写、不念）
      const main = X.short || X.why, hasTry = !!X.tryit, avail = H - (c1y + c1h + 20) - 26;
      let wsz = 34, lines = [];
      for (; wsz >= 24; wsz -= 1) { setFont(ctx, wsz, ZH, 'normal'); lines = wrap(ctx, main, cw - 60, 99); if (lines.length * wsz * 1.42 + (hasTry ? 64 : 0) + 76 <= avail) break; }
      const mainH = lines.length * wsz * 1.42, c2h = Math.min(avail, 66 + mainH + (hasTry ? 62 : 14));
      const c2y = c1y + c1h + 20 + (1 - q1) * 14;
      ctx.save(); ctx.globalAlpha = f * q1;
      rr(ctx, x0, c2y, cw, c2h, 18); ctx.fillStyle = '#FFF8D6'; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = '#F0D25A'; ctx.stroke();
      txt(ctx, '为什么', x0 + 30, c2y + 40, { size: 26, weight: 'bold', color: '#B7791F' });
      para(ctx, main, x0 + 30, c2y + 80 + (wsz - 25) * 0.4, cw - 60, { size: wsz, color: C.ink, maxLines: lines.length, lh: 1.42 });
      if (hasTry) {
        const ty = c2y + 66 + mainH + 26;
        chip(ctx, '试一试', x0 + 30, ty, { size: 22, bg: '#2F855A', color: '#FFFFFF' });
        const tz = fit(ctx, X.tryit, ZH, 'normal', 25, cw - 180, 17);
        txt(ctx, X.tryit, x0 + 130, ty + 8, { size: tz, color: '#22543D' });
      }
      ctx.restore();
    }
  };
  // 6.4：拆开以后这一行排在画面中间，下面只写“拆成 2 部分”（用户：“下面不要再写小的 pro + duce，因为上面已经有了”）；
  // 讲每一部分时这一行缩小、挪到左上角（miniStrip），把那一部分的卡片放大
  const SPLIT_Y = 334, MINI = { x: 60, y: 72, size: 40 };
  S.split = (ctx, film, p, sc) => {
    const k0 = sc ? film.scenes.findIndex(z => z.t0 === sc.t0) : -1, prev = k0 > 0 ? film.scenes[k0 - 1] : null;
    const y0 = prev && prev.id === 'title' ? titleLayout(ctx, film).y : 384;          // 上一幕就是开头：单词从开头那儿的位置动过来
    if (film.owner && !film.dropE) {
      const k = easeInOut(span(p, 0.05, 0.6));
      const size = lerp(fit(ctx, film.word, EN, 'bold', 150, W - 200, 60), stripSize(ctx, film), k);
      const y = lerp(y0, SPLIT_Y, k);
      drawWord(ctx, film, { k, y, size, colored: span(p, 0.25, 0.55) > 0, blocks: span(p, 0.45, 0.75), plus: span(p, 0.55, 0.8) });
    } else {
      const size = fit(ctx, film.word, EN, 'bold', 150, W - 200, 60);
      txt(ctx, film.word, W / 2, y0, { size, family: EN, weight: 'bold', align: 'center', alpha: 1 - span(p, 0, 0.35) });
      strip(ctx, film, { y: SPLIT_Y, size: stripSize(ctx, film), alpha: span(p, 0.3, 0.65) });
    }
    const q = span(p, 0.68, 0.9);
    if (q > 0) txt(ctx, '拆成 ' + film.parts.length + ' 部分', W / 2, SPLIT_Y + 130, { size: 44, weight: 'bold', color: C.ink, align: 'center', alpha: q });
  };
  // 这一行居中排的时候，最左边在哪儿
  function stripLeft(ctx, film, size) {
    if (film.owner && !film.dropE) { const lay = wordLayout(ctx, film, size, size * 0.62); return lay[0].x - size * 0.18; }
    setFont(ctx, size, EN, 'bold');
    const ws = film.parts.map(pt => ctx.measureText(pt.text).width + size * 0.5), gap = size * 0.7;
    return (W - ws.reduce((a, b) => a + b, 0) - gap * (film.parts.length - 1)) / 2;
  }
  // 6.4：讲每一部分时，“pro + duce”这一行缩小放在左上角；k = 0 还在画面中间（拆开那一幕的位置），k = 1 到了左上角。hi：正在讲的那一部分亮着
  function miniStrip(ctx, film, hi, k) {
    const S0 = stripSize(ctx, film), L = stripLeft(ctx, film, S0);
    const z = lerp(1, MINI.size / S0, k), x = lerp(L, MINI.x, k), y = lerp(SPLIT_Y, MINI.y, k);
    ctx.save();
    ctx.translate(x - z * L, y - z * SPLIT_Y); ctx.scale(z, z);
    strip(ctx, film, { y: SPLIT_Y, size: S0, hi });
    ctx.restore();
  }
  function stripSize(ctx, film) {
    const n = film.parts ? film.parts.length : 1;
    let z = 100;
    while (z > 40) {
      setFont(ctx, z, EN, 'bold');
      const w = ctx.measureText(film.word).width + z * 0.62 * (n - 1) + z * 0.4 * n;
      if (w < W - 160) break;
      z -= 4;
    }
    return z;
  }
  // 5.11：词根的另一种写法那一行“字母变化”：duc → duct，留着的字母照这一部分的颜色，新多出来的字母绿色加粗、下面一道线；后面小字写怎么变的
  // 6.4：z 是放大几倍（卡片放大了、挪到“身份和分工”那一幕以后字也大一点）
  function variantStrip(ctx, part, x, y, w, col, z) {
    z = z || 1;
    const F = part.forms, Z = 30 * z;
    let cx = x + chip(ctx, '字母变化', x, y, { size: 19 * z, bg: '#E2F3E5', color: '#2B7A3E' }) + 14 * z;
    F.forEach((fm, k) => {
      const kept = k ? keptLetters(F[k - 1], fm).kb : null;
      if (k) { txt(ctx, '→', cx + 10 * z, y + 1, { size: 26 * z, weight: 'bold', color: '#B69D62', base: 'middle' }); cx += 46 * z; }
      fm.split('').forEach((ch, i) => {
        const add = kept && !kept[i];
        setFont(ctx, Z, EN, 'bold');
        const cw = ctx.measureText(ch).width;
        txt(ctx, ch, cx, y + 1, { size: Z, family: EN, weight: 'bold', color: add ? '#1E9E4A' : k ? col : C.ink, base: 'middle' });
        if (add) { ctx.save(); ctx.fillStyle = '#1E9E4A'; ctx.fillRect(cx, y + Z * 0.52, cw, 3); ctx.restore(); }
        cx += cw;
      });
    });
    if (part.howShort && cx + 20 < x + w) {
      setFont(ctx, 21 * z, ZH);
      const t = wrap(ctx, part.howShort, x + w - cx - 18 * z, 1)[0] || '';
      txt(ctx, t, cx + 18 * z, y + 1, { size: 21 * z, color: C.soft, base: 'middle' });
    }
  }
  // 5.11：记法里的“音变”：谁对谁画成两个圆牌子中间一个箭头（f → d），一条链就把链写出来；后面是那一句话
  // “音变 p → f”那几个牌子一共多宽（一条链的不算）
  function shiftRowW(ctx, sh, z) {
    const cw = (t, size) => { setFont(ctx, size, ZH, 'bold'); return ctx.measureText(t).width + size * 1.1; };
    let wd = cw('音变', 19 * z) + 12 * z;
    if (!sh.pairs.length) return 1e9;
    sh.pairs.slice(0, 3).forEach(([p1, p2], i) => { wd += (i ? 8 * z : 0) + cw(p1, 22 * z) + 4 * z + 28 * z + cw(p2, 22 * z) + 6 * z; });
    return wd;
  }
  // inline：那一句话接在牌子后面写成一行（6.4：卡片放大以后一行写得下）
  function shiftRow(ctx, sh, x, y, w, z, inline) {
    z = z || 1;
    let cx = x + chip(ctx, '音变', x, y, { size: 19 * z, bg: '#E3EEFA', color: '#2F6FB3' }) + 12 * z;
    if (sh.pairs.length) {
      sh.pairs.slice(0, 3).forEach(([p1, p2], i) => {
        if (i) cx += 8 * z;
        cx += chip(ctx, p1, cx, y, { size: 22 * z, bg: '#FFE0B2', color: '#8A4B00' }) + 4 * z;
        txt(ctx, '→', cx, y + 1, { size: 22 * z, weight: 'bold', color: '#B69D62', base: 'middle' }); cx += 28 * z;
        cx += chip(ctx, p2, cx, y, { size: 22 * z, bg: '#C8E6C9', color: '#1B5E20' }) + 6 * z;
      });
    } else if (sh.chain.length) {
      const line = sh.chain.map(c => c.f).join(' → ');
      const fz = fit(ctx, line, EN, 'bold', 23 * z, w - (cx - x) - 6, 15);
      txt(ctx, line, cx, y + 1, { size: fz, family: EN, weight: 'bold', color: '#2F6FB3', base: 'middle' });
    }
    const body = sh.text.replace(/（[^（）]*）/g, '');
    if (inline && sh.pairs.length) { txt(ctx, body, cx + 10 * z, y + 1, { size: 20 * z, color: '#6E5520', base: 'middle' }); return 0; }
    return para(ctx, body, x, y + 34 * z, w, { size: 20 * z, color: '#6E5520', maxLines: 2, lh: 1.38 });
  }
  // 6.4：每一部分的卡片改成“特写”（用户：“把上面的 pro + duce 缩小，放到左上角，把拆分的部分进行特写，变大一点”）：
  //   上面那一行缩小放在左上角（miniStrip），正在讲的那一部分亮着；卡片几乎占满画面，左边是会动的图，右边从上到下：
  //   这一部分（大字）、意思、小牌子、【前缀 / 后缀】蓝框“身份”（原来在“辨析”那一幕，用户：“身份放在前一页，pro- 专讲这里”）、黄框“记”（带音变）。
  //   词根的另一种写法（duce = 词根 duc）：后面有“身份和分工”那一幕的，“字母变化”那一行不在这儿写（part.varInFg，用户：“后面有专门的 duce 的讲解，放在那里面写比较好”）。
  //   右边的字从大到小试，放得下为止；整块上下居中。右上角的“1 / 2”不写了（左上角那一行已经看得出讲到第几部分）
  S.part = (ctx, film, p, sc) => {
    const part = film.parts[sc.i];
    const tl = sc.tl != null ? sc.tl : p * sc.dur;
    // 讲第一部分时，上面那一行先从画面中间挪到左上角（0.6 秒），卡片等它挪开了再出来
    const f = fadeOf(sc, p) * (sc.i === 0 ? clamp((tl - 0.3) / 0.35) : 1);
    const memo = part.memo, shift = memo && memo.shift && !film.brief ? memo.shift : null, vr = !!part.base && part.forms.length >= 2;      // 6.19：精简版不讲音变
    const showVar = vr && !part.varInFg;
    const affix = part.kind === 'pre' || part.kind === 'suf';
    // 5.11：配音分了句（marks）：第 1 句讲这一部分，后面依次是“在这里写成…”（词根的另一种写法）、记法、音变；说到哪一句，哪一块才出来
    const mk = sc.marks && sc.marks.length >= 2 ? sc.marks : null;
    let mi = 1;
    const tVar = ((vr && !part.pp) || (part.xt && part.xt.spelled)) && mk && mk[mi] != null ? mk[mi++] : null;
    const tMemo = memo && mk && mk[mi] != null ? mk[mi++] : null;
    const tShift = shift && mk && mk[mi] != null ? mk[mi++] : null;
    const oldWhy = !!(shift && shift.why && !yinbianOf(shift));                   // 6.6：新写法的原因（有“发音：”）挪到下一幕“为什么 p 会变成 f？”，记框里只留“音变 p → f”
    const tWhy = oldWhy && mk && mk[mi] != null ? mk[mi++] : null;      // 6.5：音变的原因，配音单独一句
    const on = (t, a, b) => (t != null ? clamp((tl - t + 0.12) / 0.4) : span(p, a, b));
    // 分了句的：第 1 句（“词根是 duc，来自拉丁语，意思是：领着走”）说到几成的时候出来——小牌子跟着“来自…”，意思跟着“意思是：…”
    const e0 = mk && Array.isArray(sc.ends) && sc.ends[0] != null ? sc.ends[0] : null;
    const s1 = (fr, a, b) => (mk && e0 != null ? clamp((tl - (mk[0] + fr * (e0 - mk[0])) + 0.1) / 0.4) : span(p, a, b));
    // 卡片
    const up = (1 - easeOut(span(p, 0, 0.22))) * 30;
    const x0 = 56, y0 = 104 + up, w = W - 112, h = 592;
    ctx.globalAlpha = f;
    ctx.save();
    ctx.shadowColor = 'rgba(60,50,20,.10)'; ctx.shadowBlur = 24; ctx.shadowOffsetY = 6;
    rr(ctx, x0, y0, w, h, 24); ctx.fillStyle = C.card; ctx.fill();
    ctx.restore();
    ctx.globalAlpha = f;
    rr(ctx, x0, y0, w, h, 24); ctx.lineWidth = 2; ctx.strokeStyle = C.line; ctx.stroke();
    rr(ctx, x0, y0, 12, h, 6); ctx.fillStyle = part.color; ctx.fill();
    // 左边：会动的图（有“记”时下面留一行写 pro ≈ for）。prefs.partPics 写了这一部分自己的画就画它
    const PW = 400, labH = 0, pb = Math.min(368, h - labH - 36);                  // 6.5：图下面不再写 pro ≈ for（用户：“在记这个方块里面已经说了”）
    ctx.save();
    rr(ctx, x0 + 12, y0, PW, h - labH, 0); ctx.clip();
    if (part.pic) {
      ctx.globalAlpha = f * easeOut(span(p, 0.02, 0.2));
      drawPic(ctx, part.pic, x0 + 12 + (PW - pb) / 2, y0 + (h - labH - pb) / 2, pb, pb, { q: 1, lt: Math.max(0, tl - 0.3), cues: mk || null, cueEnds: sc.ends || null, cueTexts: sc.texts || null });
    } else act(ctx, part, x0 + 12 + PW / 2, y0 + (h - labH) / 2, memo ? 216 : 232, p, { hw: PW / 2 - 12, hh: (h - labH) / 2 - 18 });
    ctx.restore();
    ctx.globalAlpha = f;
    // 右边要写的东西
    const tx = x0 + 12 + PW + 34, tw = x0 + w - 36 - tx;
    const head = part.xt ? part.xt.root + '-' : part.head && part.head.length <= 16 ? part.head : part.text;      // 各部分解释里的写法（-er、trans-）；6.8：词根形态版写词根本身 duc-
    const gl = part.xt ? part.xt.gloss : vr && part.rootGloss ? part.rootGloss : part.gloss;                 // 词根的另一种写法：写词根本身的意思
    const here = vr && part.gloss && part.gloss !== gl && !String(gl || '').includes(part.gloss) ? '在这里：' + part.gloss : '';
    const idc = affix && part.bx && part.idt ? idCard(part.sub) : part.xt ? { main: part.xt.src, small: '', here: part.xt.here } : null;      // 6.8：词根的蓝框：来源 + “在这个词里 duce（原形，英语加不发音的 e）”           // 6.5：前缀、后缀的身份框：“来自拉丁语介词 pro；表示“向前”；也可以表示“预先””
    const idMain = idc && idc.main ? idc.main : '';
    const idRest = idMain ? idc.small : '';                                        // 小字：介绍里别的话
    const idHere = idMain ? idc.here : '';                                         // 6.6：“这里是…”单独一行、醒目（用户：“这里是“向前、到前面来”变醒目一点，因为是当前词的解释”）
    const more0 = part.sub || part.role, more = !idMain && !vr && more0 && oneLine(more0) !== part.gloss ? String(more0) : '';
    // 6.5：前缀、后缀（新写法）：意思和这一部分写在一行，“前缀 / 后缀”牌子在右上角，不写“来自拉丁语”牌子（用户：“身份里面已经说了”）
    const aNew = !!idMain;
    const kindZh = part.kind === 'pre' ? '前缀' : part.kind === 'suf' ? '后缀' : part.kind === 'word' ? '单词' : '词根';
    const tags = [];
    if (part.from && !aNew) tags.push([part.from === '英语本族' ? '英语本族' : '来自' + part.from, '#E3EEFA', '#2F6FB3']);
    if (!aNew) tags.push([kindZh, '#F1E6CC', '#6E5520']);
    if (part.tag) tags.push([part.tag, '#E2F3E5', '#2B7A3E']);
    if (vr) tags.push(['同一个词根', '#E2F3E5', '#2B7A3E']);
    const shText = shift ? shift.text.replace(/（[^（）]*）/g, '') : '';
    // 排版：z 是字放大几倍，whyMax / restMax 是“记”的道理、身份后面的话最多几行；量出一共多高
    const plan = (z, whyMax, restMax) => {
      const o = { z };
      o.hz = fit(ctx, head, EN, 'bold', 96 * z, vr || aNew ? tw * 0.5 : tw, 36);
      let hgt = o.hz * 0.9;
      o.gIn = false;
      if (aNew && gl) {                                                          // 6.5：意思写在这一部分右边（中间隔着右上角的牌子），写不下才换行
        setFont(ctx, o.hz, EN, 'bold');
        const hw = ctx.measureText(head).width;
        setFont(ctx, 22 * z, ZH, 'bold');
        o.gx = hw + 8 * z + ctx.measureText(kindZh).width + 22 * z * 1.1 + 24 * z;
        o.gz = fit(ctx, gl, ZH, 'bold', 60 * z, tw - o.gx, 26);
        o.gIn = o.gz >= 40 * z;
      }
      if (gl && !o.gIn) {
        o.gz = fit(ctx, gl, ZH, 'bold', 56 * z, tw, 26);
        hgt += 14 * z + o.gz * 1.12;
        if (here) {
          setFont(ctx, o.gz, ZH, 'bold');
          const gw = ctx.measureText(gl).width;
          setFont(ctx, 27 * z, ZH, 'bold');
          o.hereBeside = tw - gw - 22 * z >= ctx.measureText(here).width;
          if (!o.hereBeside) hgt += 6 * z + 34 * z;
        }
      }
      if (tags.length) hgt += 18 * z + 37 * z;
      if (showVar) hgt += 16 * z + 42 * z;
      if (idMain) {
        setFont(ctx, 27 * z, ZH, 'bold');
        o.idm = wrapSegs(ctx, idMain, tw - 128 * z, 2);                          // 6.5：折行先在“；”处折，不把“也可以表示”拆开                               // 第一句长的（最基本的意思是“在…之间”，来自拉丁语介词 inter）折成两行，不缩成小字
        setFont(ctx, 22 * z, ZH, 'normal');
        o.rest = idRest ? wrap(ctx, idRest, tw - 128 * z, restMax) : [];
        o.here = [];
        if (idHere) {                                                            // 6.6：“在这个词里”牌子 + 这一部分颜色的粗字，浅色底
          setFont(ctx, 20 * z, ZH, 'bold'); o.hcw = ctx.measureText('在这个词里').width + 22 * z;
          const hw0 = tw - 92 * z - o.hcw - 44 * z;
          o.hrz = fit(ctx, idHere, ZH, 'bold', 28 * z, hw0, Math.round(22 * z));
          setFont(ctx, o.hrz, ZH, 'bold'); o.here = wrap(ctx, idHere, hw0, 2);
        }
        o.hereH = o.here.length ? o.here.length * o.hrz * 1.32 + 14 * z : 0;
        o.idH = 24 * z + o.idm.length * 38 * z + (o.hereH ? 10 * z + o.hereH + 6 * z : 0) + o.rest.length * 31 * z + (o.rest.length ? 4 * z : 0);
        hgt += 20 * z + o.idH;
      }
      if (more) { setFont(ctx, 24 * z, ZH, 'normal'); o.more = wrap(ctx, more, tw - 26 * z, 3); hgt += 16 * z + o.more.length * 35 * z; }
      if (memo) {
        setFont(ctx, 22 * z, ZH, 'normal');
        o.why = memo.why ? wrap(ctx, memo.why, tw - 60 * z, whyMax) : [];
        o.memoH = 60 * z + o.why.length * 31 * z + 12 * z;
        if (shift) {
          o.shIn = shiftRowW(ctx, shift, z) + 16 * z + (setFont(ctx, 20 * z, ZH, 'normal'), ctx.measureText(shText).width) <= tw - 44 * z;      // 那一句和“p → f”写得下一行
          o.sh = Math.min(2, wrap(ctx, shText, tw - 44 * z, 2).length);
          o.memoH += o.shIn ? 46 * z : 62 * z + (o.sh - 1) * 27.6 * z;
          o.why2 = [];
          if (oldWhy) { setFont(ctx, 20 * z, ZH, 'normal'); o.why2 = wrap(ctx, shift.why, tw - 44 * z - 72 * z, 3); o.memoH += 14 * z + o.why2.length * 27.6 * z; }
        }
        hgt += 18 * z + o.memoH;
      }
      o.total = hgt;
      return o;
    };
    let L = null;
    for (const [z, a, b] of [[1.18, 3, 2], [1.12, 3, 2], [1.06, 3, 2], [1, 3, 2], [0.94, 3, 2], [0.88, 3, 2], [0.94, 2, 1], [0.88, 2, 1], [0.82, 3, 2], [0.82, 2, 1], [0.76, 2, 1], [0.7, 2, 1]]) { L = plan(z, a, b); if (L.total <= h - 44) break; }
    const z = L.z;
    if (film._dbg) film._dbg.push(['part', head, L.z, Math.round(L.total), h - 44, L.why ? L.why.length : 0, L.rest ? L.rest.length : 0]);      // 调版面用：sheet.py 打印
    let y = y0 + Math.max(20, (h - L.total) / 2);
    // 这一部分（大字）
    txt(ctx, head, tx, y + L.hz * 0.8, { size: L.hz, family: EN, weight: 'bold', color: part.color });
    if (aNew) {                                                                    // 6.5：“前缀”牌子在右上角，意思紧跟在右边（同一行）
      setFont(ctx, L.hz, EN, 'bold');
      const hw = ctx.measureText(head).width;
      chip(ctx, kindZh, tx + hw + 8 * z, y + L.hz * 0.3, { size: 22 * z, bg: '#F1E6CC', color: '#6E5520', alpha: s1(0.3, 0.22, 0.42) });
      if (L.gIn) txt(ctx, gl, tx + L.gx, y + L.hz * 0.8, { size: L.gz, weight: 'bold', color: C.ink, alpha: s1(0.6, 0.15, 0.35) });
    }
    if (vr) {                                                                      // duct = 词根 duc：同一个词根，写法变了
      setFont(ctx, L.hz, EN, 'bold');
      const hw = ctx.measureText(head).width;
      const qv = s1(0.1, 0.1, 0.28);                                               // “词根是 duc”一说出来就写上
      txt(ctx, '=', tx + hw + 20 * z, y + L.hz * 0.8 - 4 * z, { size: 44 * z, family: EN, weight: 'bold', color: '#B69D62', alpha: qv });
      chip(ctx, '词根 ' + part.base, tx + hw + 62 * z, y + L.hz * 0.5, { size: 32 * z, bg: tint(part.color, 0.82), color: part.color, alpha: qv });
    }
    y += L.hz * 0.9;
    // 意思
    if (gl && !L.gIn) {
      y += 14 * z;
      txt(ctx, gl, tx, y + L.gz * 0.9, { size: L.gz, weight: 'bold', color: C.ink, alpha: s1(0.6, 0.15, 0.35) });
      if (here && L.hereBeside) {                                                  // 这个词里的意思（被领出来的）：说到“在这里写成…，是…”时写在后面
        setFont(ctx, L.gz, ZH, 'bold');
        txt(ctx, here, tx + ctx.measureText(gl).width + 22 * z, y + L.gz * 0.9 - 2, { size: 27 * z, weight: 'bold', color: part.color, alpha: on(tVar, 0.3, 0.5) });
      }
      y += L.gz * 1.12;
      if (here && !L.hereBeside) { y += 6 * z; txt(ctx, here, tx, y + 26 * z, { size: 27 * z, weight: 'bold', color: part.color, alpha: on(tVar, 0.3, 0.5) }); y += 34 * z; }
    }
    // 小牌子：来自哪种语言 · 前缀 / 后缀 / 词根 · 词性怎么变
    if (tags.length) {
      y += 18 * z;
      let chx = tx;
      tags.forEach(([t, bg, col]) => { chx += chip(ctx, t, chx, y + 18.5 * z, { size: 23 * z, bg, color: col, alpha: s1(0.3, 0.22, 0.42) }) + 10 * z; });
      y += 37 * z;
    }
    // 字母变化（后面没有“身份和分工”那一幕的才在这儿写）
    if (showVar) {
      y += 16 * z;
      ctx.globalAlpha = f * on(tVar, 0.3, 0.5);
      variantStrip(ctx, part, tx, y + 21 * z, tw, part.color, z * 1.08);
      ctx.globalAlpha = f;
      y += 42 * z;
    }
    // 身份（前缀、后缀）：蓝框，第一行是开头的介绍的第一句和来历，下面小字是介绍里后面的话
    if (idMain) {
      y += 20 * z;
      ctx.globalAlpha = f * s1(0.85, 0.28, 0.48);
      rr(ctx, tx, y, tw, L.idH, 16 * z); ctx.fillStyle = '#EEF5FF'; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = '#9CC3EE'; ctx.stroke();
      txt(ctx, '身份', tx + 20 * z, y + 31 * z, { size: 25 * z, weight: 'bold', color: '#2B6CB0', base: 'middle' });
      L.idm.forEach((ln, j) => txt(ctx, ln, tx + 92 * z, y + 31 * z + j * 38 * z, { size: 27 * z, weight: 'bold', color: C.ink, base: 'middle' }));
      let iy = y + 24 * z + L.idm.length * 38 * z;
      if (L.hereH) {                                                             // 6.6：在这个词里 “向前、到前面来”
        iy += 10 * z;
        ctx.save(); if (part.xt && tVar != null) ctx.globalAlpha *= on(tVar, 0.3, 0.5);
        rr(ctx, tx + 84 * z, iy - 6 * z, tw - 84 * z - 14 * z, L.hereH, 12 * z); ctx.fillStyle = tint(part.color, 0.86); ctx.fill();
        chip(ctx, '在这个词里', tx + 98 * z, iy - 6 * z + L.hereH / 2, { size: 20 * z, bg: '#FFFFFF', color: part.color });
        L.here.forEach((ln, j) => txt(ctx, ln, tx + 98 * z + L.hcw + 16 * z, iy - 6 * z + 7 * z + (j + 0.5) * L.hrz * 1.32, { size: L.hrz, weight: 'bold', color: part.color, base: 'middle' }));
        ctx.restore();
        iy += L.hereH + 6 * z;
      }
      L.rest.forEach((ln, j) => txt(ctx, ln, tx + 92 * z, iy + j * 31 * z + 14 * z, { size: 22 * z, color: C.soft }));
      ctx.globalAlpha = f;
      y += L.idH;
    }
    // 词根、单词（和老表的词缀）：解释里的一两句
    if (more) {
      y += 16 * z;
      ctx.globalAlpha = f * span(p, 0.3, 0.5);
      L.more.forEach((ln, j) => txt(ctx, ln, tx, y + 26 * z + j * 35 * z, { size: 24 * z, color: C.soft }));
      ctx.globalAlpha = f;
      y += L.more.length * 35 * z;
    }
    // 黄底的“记”框：第一行 记：pro ≈ for（为了），下面讲为什么这样记（≈ 一家 / ∽ 只是像）；带“音变”的再加一行谁对谁
    if (memo) {
      y += 18 * z;
      const by = y, bh = L.memoH;
      ctx.globalAlpha = f * on(tMemo, 0.38, 0.58);
      rr(ctx, tx, by, tw, bh, 16 * z); ctx.fillStyle = '#FFF6D6'; ctx.fill();
      ctx.lineWidth = 2; ctx.strokeStyle = '#F0D25A'; ctx.stroke();
      rr(ctx, tx, by, 8, bh, 4); ctx.fillStyle = '#E0A800'; ctx.fill();
      const symZh = memo.sym === '∽' ? '记（像）：' : '记：', my = by + 34 * z;
      setFont(ctx, 28 * z, ZH, 'bold');
      const lw = ctx.measureText(symZh).width;
      txt(ctx, symZh, tx + 22 * z, my, { size: 28 * z, weight: 'bold', color: '#7A4E00', base: 'middle' });
      const label = memo.a + ' ' + memo.sym + ' ' + (memo.same ? '单词 ' : '') + memo.b;
      setFont(ctx, 34 * z, memo.same ? ZH : EN, 'bold');
      const lw2 = ctx.measureText(label).width;
      txt(ctx, label, tx + 22 * z + lw + 6, my, { size: 34 * z, family: memo.same ? ZH : EN, weight: 'bold', color: part.color, base: 'middle' });
      txt(ctx, '（' + memo.zh + '）', tx + 22 * z + lw + 6 + lw2 + 4, my, { size: 27 * z, weight: 'bold', color: C.ink, base: 'middle' });
      ctx.globalAlpha = f * on(tMemo, 0.5, 0.7);
      L.why.forEach((ln, j) => txt(ctx, ln, tx + 22 * z, by + 60 * z + j * 31 * z + 22 * z, { size: 22 * z, color: '#6E5520' }));
      if (shift) {
        ctx.globalAlpha = f * on(tShift, 0.6, 0.8);
        const sy = by + 60 * z + L.why.length * 31 * z + 12 * z + 18 * z;
        shiftRow(ctx, shift, tx + 22 * z, sy, tw - 44 * z, z, L.shIn);
        if (L.why2 && L.why2.length) {                                           // 6.5：先说发生了什么音变（p → f），下面一行“原因”说为什么
          ctx.globalAlpha = f * on(tWhy, 0.7, 0.9);
          const wy = sy + (L.shIn ? 46 : 62 + (L.sh - 1) * 27.6) * z - 6 * z;
          chip(ctx, '原因', tx + 22 * z, wy, { size: 19 * z, bg: '#FBE3CF', color: '#B4530F' });
          L.why2.forEach((ln, j) => txt(ctx, ln, tx + 94 * z, wy + 1 + j * 27.6 * z, { size: 20 * z, color: '#6E5520', base: 'middle' }));
        }
      }
    }
    // 上面那一行：缩小、放到左上角（讲第一部分时从画面中间动过去；画在卡片上面）。前一幕 / 后一幕不是讲某一部分的（辨析、合起来），跟着淡入 / 淡出
    const k0 = film.scenes.findIndex(q => q.t0 === sc.t0), pv = k0 > 0 ? film.scenes[k0 - 1] : null, nx = k0 >= 0 ? film.scenes[k0 + 1] : null;
    ctx.globalAlpha = (sc.i === 0 || (pv && (pv.id === 'part' || pv.id === 'yinbian')) ? 1 : span(p * sc.dur, 0, 0.35)) * (nx && (nx.id === 'part' || nx.id === 'yinbian') ? 1 : span((1 - p) * sc.dur, 0, 0.3));      // 6.6：接着讲音变的那一幕，左上角那一行不淡出
    miniStrip(ctx, film, sc.i, sc.i === 0 ? easeInOut(clamp(tl / 0.6)) : 1);
    ctx.globalAlpha = 1;
  };
  // 派生路线：divide → individual（个体的）→ individualize（使个体化），一个接一个出来
  function routeScene(ctx, film, p, f, sc) {
    const items = film.route.slice(-4), n = items.length;
    const mk = sc && sc.marks && sc.marks.length >= n ? sc.marks : null;
    const own = sc && sc.id === 'route';                // 单独的一幕（上面没有分开的单词）：整体往上挪，每一步上面配一张图
    const dy = own ? -60 : 0;
    txt(ctx, own ? '来历：一步一步变成这个词' : '派生路线', W / 2, own ? 150 : 330, { size: 28, weight: 'bold', color: '#8A6A2A', align: 'center', alpha: f });
    const gap = 70, cw = Math.min(300, (W - 120 - gap * (n - 1)) / n);
    let x = (W - cw * n - gap * (n - 1)) / 2;
    items.forEach((it, i) => {
      const at = 0.08 + i * (0.6 / n), q = mk ? easeBack(span(sc.tl, mk[i], mk[i] + 0.5)) : easeBack(span(p, at, at + 0.16));
      const last = i === n - 1, cx = x + cw / 2;
      if (q > 0) {
        ctx.globalAlpha = f * Math.min(1, q);
        if (last) { rr(ctx, x - 8, (own ? 220 : 380) + dy * 0, cw + 16, own ? 330 : 170, 18); ctx.fillStyle = '#FFF8D6'; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = '#F0D25A'; ctx.stroke(); }
        if (own) {
          const ic = it.icon != null ? it.icon : iconFor(it.gloss, '');
          if (ic) emoji(ctx, ic, cx, 300, 96 * Math.min(1, q));
        }
        const z = fit(ctx, it.text, EN, 'bold', 46, cw - 16, 22);
        txt(ctx, it.text, cx, 448 + (own ? 0 : 0), { size: z * Math.min(1, 0.6 + q * 0.4), family: EN, weight: 'bold', color: last ? C.ink : C.soft, align: 'center' });
        if (it.gloss) {
          setFont(ctx, 26, ZH, 'bold');
          wrap(ctx, it.gloss, cw - 16, 2).forEach((ln, j) => txt(ctx, ln, cx, 498 + j * 34, { size: 26, weight: 'bold', color: last ? C.green : C.soft, align: 'center' }));
        }
        ctx.globalAlpha = 1;
      }
      x += cw;
      if (!last) { txt(ctx, '→', x + gap / 2, own ? 380 : 436, { size: 46, weight: 'bold', color: '#B69D62', align: 'center', base: 'middle', alpha: f * (mk ? span(sc.tl, mk[i + 1] - 0.3, mk[i + 1]) : span(p, at + 0.1, at + 0.2)) }); x += gap; }
    });
  }
  S.combo = (ctx, film, p, sc) => {
    const f = fadeOf(sc, p);
    strip(ctx, film, { y: 205, size: stripSize(ctx, film) });
    if (film.route && film.route.length >= 2 && !film.parts.some(pt => pt.gloss)) { routeScene(ctx, film, p, f, sc); return; }
    const n = film.parts.length;
    const items = film.parts.map(pt => ({ p: pt, w: 0 })).concat([{ res: true, w: 0 }]);
    const isz = n >= 4 ? 76 : 96, gz = n >= 4 ? 28 : 34;
    items.forEach(it => {
      const s = it.res ? '“' + (film.combo.literal || film.word) + '”' : it.p.gloss || it.p.text;
      it.label = s;
      setFont(ctx, it.res ? gz + 4 : gz, ZH, 'bold');
      it.w = Math.max(isz * 1.4, Math.min(it.res ? 440 : 280, ctx.measureText(s).width + (it.res ? 40 : 24)));
      if (it.res && film.combo.pic) it.w = Math.max(it.w, 400);
    });
    const sep = 64;
    let total = items.reduce((s, it) => s + it.w, 0) + sep * n;
    const scale = Math.min(1, (W - 120) / total);
    let x = (W - total * scale) / 2;
    const cy = 450;
    ctx.save();
    ctx.translate(W / 2, cy); ctx.scale(scale, scale); ctx.translate(-W / 2, -cy);
    x = W / 2 - total / 2;
    const mk = sc.marks && sc.marks.length >= items.length ? sc.marks : null;
    items.forEach((it, i) => {
      const at = 0.06 + i * (0.5 / items.length);
      const q = mk ? easeBack(span(sc.tl, mk[i], mk[i] + 0.5)) : easeBack(span(p, at, at + 0.14));
      const cx = x + it.w / 2;
      if (q > 0) {
        ctx.globalAlpha = f * Math.min(1, q);
        if (it.res && film.combo.pic) {
          const t0 = mk ? mk[i] : at * sc.dur, by = cy - 182;
          rr(ctx, x - 10, by, it.w + 20, 312, 22); ctx.fillStyle = '#FFF8D6'; ctx.fill();
          ctx.lineWidth = 3; ctx.strokeStyle = '#F0D25A'; ctx.stroke();
          drawPic(ctx, film.combo.pic, x + 4, by + 14, it.w - 8, 214, { q: Math.min(1, q), lt: Math.max(0, (sc.tl || 0) - t0) });
          let lz = gz + 2;                                    // 5.11：折成两行、第二行只剩一两个字的（“…造出来的东 / 西”），字缩小一点放进一行
          setFont(ctx, lz, ZH, 'bold');
          let lns = wrap(ctx, it.label, it.w - 10, 2);
          while (lns.length > 1 && lns[lns.length - 1].length <= 2 && lz > gz - 8) { lz -= 2; setFont(ctx, lz, ZH, 'bold'); lns = wrap(ctx, it.label, it.w - 10, 2); }
          lns.forEach((ln, j) => txt(ctx, ln, cx, by + 268 + j * (lz + 6), { size: lz, weight: 'bold', color: C.ink, align: 'center' }));
        } else if (it.res) {
          rr(ctx, x - 6, cy - 128, it.w + 12, 240, 20); ctx.fillStyle = '#FFF8D6'; ctx.fill();
          ctx.lineWidth = 3; ctx.strokeStyle = '#F0D25A'; ctx.stroke();
          if (film.combo.icon) { emoji(ctx, film.combo.icon, cx, cy - 40, isz * 1.05 * q); if (film.combo.neg) slash(ctx, cx, cy - 40, isz * 1.05, span(p, 0.75, 0.92)); }
          else txt(ctx, film.word, cx, cy - 26, { size: 46 * q, family: EN, weight: 'bold', color: C.ink, align: 'center', base: 'middle' });
          setFont(ctx, gz + 4, ZH, 'bold');
          const lines = wrap(ctx, it.label, it.w - 10, 2);
          lines.forEach((ln, j) => txt(ctx, ln, cx, cy + 62 + j * (gz + 10), { size: gz + 4, weight: 'bold', color: C.ink, align: 'center' }));
        } else {
          icon(ctx, it.p, cx, cy - 40, isz * q);
          setFont(ctx, gz, ZH, 'bold');
          const lines = wrap(ctx, it.label, it.w, 2);
          lines.forEach((ln, j) => txt(ctx, ln, cx, cy + 58 + j * (gz + 8), { size: gz, weight: 'bold', color: it.p.color, align: 'center' }));
          txt(ctx, it.p.text, cx, cy + 58 + lines.length * (gz + 8) + 6, { size: gz - 6, family: EN, weight: 'bold', color: C.faint, align: 'center' });
        }
      }
      x += it.w;
      if (i < items.length - 1) {
        const qq = mk ? span(sc.tl, mk[i + 1] - 0.15, mk[i + 1] + 0.1) : span(p, at + 0.08, at + 0.16);
        txt(ctx, i === items.length - 2 ? '=' : '+', x + sep / 2, cy - 30, { size: 60, weight: 'bold', color: C.faint, align: 'center', base: 'middle', alpha: f * qq });
        x += sep;
      }
    });
    ctx.restore();
    ctx.globalAlpha = 1;
  };
  // 3.7 起：“合成规律”那一幕。合起来以后讲两个词为什么这样排（paper-cutting = cut paper，宾语挪到前面），带连字符的再讲写法；
  // 一条一张卡：上面一行黄字“★ 合成规律”/“★ 写法”，中间是规律那句话，下面一行小字是本词的例子；配音说到哪条，哪张卡浮上来
  S.rule = (ctx, film, p, sc) => {
    const f = fadeOf(sc, p);
    const items = film.compShow || [];
    header(ctx, film, items.length && items.every(x => x.kind === '构词') ? '构词' : '合成规律', f);
    const mk = sc.marks && sc.marks.length >= items.length ? sc.marks : null;
    const bx = 110, bw = W - 220;
    let y = 120;
    items.forEach((it, i) => {
      setFont(ctx, 34, ZH, 'bold');
      const lines = wrap(ctx, it.text, bw - 72, 3);
      setFont(ctx, 26, ZH, 'normal');
      const exl = it.show ? wrap(ctx, it.show, bw - 72, 2) : [];
      const bh = 70 + lines.length * 46 + (exl.length ? 16 + exl.length * 36 : 0) + 18;
      const at = items.length > 1 ? 0.04 + i * 0.46 : 0.06;
      const q = mk ? easeOut(span(sc.tl, mk[i] - 0.1, mk[i] + 0.4)) : easeOut(span(p, at, at + 0.14));
      if (q > 0) {
        const yy = y + (1 - q) * 26, spell = it.kind === '写法', gou = it.kind === '构词';
        ctx.globalAlpha = f * q;
        rr(ctx, bx, yy, bw, bh, 22);
        ctx.fillStyle = gou ? '#EAF7EE' : spell ? '#EEF5FF' : '#FFF8D6'; ctx.fill();
        ctx.lineWidth = 3; ctx.strokeStyle = gou ? '#8CCB9F' : spell ? '#9CC3EE' : '#F0D25A'; ctx.stroke();
        txt(ctx, '★ ' + it.kind, bx + 36, yy + 48, { size: 26, weight: 'bold', color: gou ? '#2B7A3E' : spell ? '#2B6CB0' : '#B7791F' });
        lines.forEach((ln, j) => txt(ctx, ln, bx + 36, yy + 98 + j * 46, { size: 34, weight: 'bold', color: C.ink }));
        exl.forEach((ln, j) => txt(ctx, ln, bx + 36, yy + 98 + lines.length * 46 + 16 + j * 36, { size: 26, color: C.soft }));
      }
      y += bh + 26;
    });
    ctx.globalAlpha = 1;
  };
  // 6.0：“身份和分工”——同一个词根的几种写法（duce / duct）、意思相近的词缀（-ous / -ful / -al）各是什么身份、怎么分工。
  // 上面一行：这一部分 + 它的身份；下面一条一条是分工（讲到哪条哪条亮；说这一部分自己的那一条描边、标“这个词”）；
  // 最下面黄底一条：总表里的“为什么用 -ous 不用 -ful：…”
  // 6.1：词根是拉丁语动词的（总表那一行有“动词变化：…；规律：…”），身份挪到标题右边，中间多一条“拉丁语动词的三个样子”：
  // 原形 → 过去式 → 过去分词三个框（和词根相同的字母上色；这一部分用的那个样子描边，框的右下角写英语里的写法），下面是变化规律；
  // 分工最多留 4 条（上面多了三个框），讲到的几条一定留着
  // 6.5：前缀、后缀卡片上“身份”框写什么（用户：“含义部分方框里面，直接说来自…；表示…；也可以表示…”）：
  //   main：来历括号的头一句（来自拉丁语介词 pro）；表示 + 开头的意思（“向前”）；介绍里“也表示…”那几句写成“也可以表示…”
  //   small：介绍里别的话（这里是“向前、到前面来”）。读不出来历的，main 只写意思
  function wrapSegs(ctx, t, width, max) {
    const segs = splitTop(String(t || ''), '；').map(x => x.trim()).filter(Boolean), out = [];
    let cur = '';
    segs.forEach((x, i) => {
      const s = x + (i < segs.length - 1 ? '；' : '');
      if (cur && ctx.measureText(cur + s).width > width) { out.push(cur); cur = s; } else cur += s;
      if (ctx.measureText(cur).width > width) { const ls = wrap(ctx, cur, width, 9); out.push(...ls.slice(0, -1)); cur = ls[ls.length - 1] || ''; }
    });
    if (cur) out.push(cur);
    return out.length <= max ? out : wrap(ctx, t, width, max);
  }
  // 6.6：身份框第一行写成“来自拉丁语介词 pro；表示“向前”和“预先””（用户：“也可以表示这几个字去掉，省点字”）——介绍里“也表示“预先””这种只是一个意思的，
  //   并到“表示…”后面用“和”连上；不只是一个意思的（也表示“完全”或“反着来”）照写“也表示…”，不加“可以”。
  //   “这里是“向前、到前面来””单拿出来（here），卡片上单独一行、醒目；别的话（small）还是小字
  function idCard(intro) {
    const segs = splitTop(String(intro || '').trim(), '；').map(x => x.trim()).filter(Boolean);
    if (!segs.length) return { main: '', small: '', here: '' };
    const first = segs[0];
    let src = '';
    for (const pg of parenGroups(first)) {
      const seg = pg.split('；')[0].trim();
      if (!/^(来自|英语本来就有|英语本族|古英语)/.test(seg)) continue;
      src = seg.split(/[，：]/)[0].replace(/“[^”]*”\s*$/, '').trim();
      break;
    }
    const core = first.replace(/（[^（）]*(?:（[^（）]*）[^（）]*)*）/g, '').replace(/[，：、\s]+$/, '').trim();
    let mean = core ? (/^“/.test(core) ? '表示' + core : core) : '';
    const one = [], also = [], rest = [];
    let here = '';
    segs.slice(1).forEach(s0 => s0.split('。').forEach(s => {
      const x = s.replace(/（[^（）]*）/g, '').replace(/[。；]+$/, '').trim();
      if (!x) return;
      const m = /^(?:也|还)(?:可以)?(表示|指)([\s\S]*)$/.exec(x);
      if (m) { if (/^“[^“”]*”$/.test(m[2].trim()) && /^表示“/.test(mean)) one.push(m[2].trim()); else also.push('也' + m[1] + m[2]); }
      else if (!here && /^这里/.test(x)) here = x.replace(/^这里(?:是|指|表示|取)?\s*/, '');
      else rest.push(x);
    }));
    if (one.length) mean += (one.length > 1 ? '、' + one.slice(0, -1).join('、') : '') + '和' + one[one.length - 1];
    return { main: [src, mean].concat(also).filter(Boolean).join('；'), small: rest.join('；'), here };
  }
  // 6.5：三个样子和分工合成一幕（用户：“三个样子下面的规律和上面三个方块解释的不配对……要把图像和文字匹配好；看是不是和下面的分工重复了，是否可以合并融合”）：
  //   规律按“；”切成三句，照先后对到原形、过去式、过去分词三栏（57 个词根族都是三句；不是三句的按开头的“原形 / 过去式 / 过去分词”认）；
  //   分工里“X 是…原样 / 动词原形”那一条接在原形一栏下面，“X 是过去分词”那一条接在过去分词一栏下面（每栏一条，说这个词自己的优先），别的放最底下。
  //   steps：配音一句一步——原形的规律 → 原形那一条 → 过去式的规律 → 过去分词的规律 → 过去分词那一条 → 底下讲到的几条（draft_plan.js 的 verbSegs 照它念）
  function verbPlan(part) {
    const V = part.verb, rows = part.fgRows || [], pick = part.fgSay || fengongPick(part);
    const K = ['inf', 'perf', 'pp'], cols = { inf: [], perf: [], pp: [] }, cl = V.rules;
    if (cl.length === 3) cl.forEach((c, i) => cols[K[i]].push(c));
    else cl.forEach((c, i) => { const k = /^原形|原形去掉/.test(c) ? 'inf' : /^过去式/.test(c) ? 'perf' : /^过去分词/.test(c) ? 'pp' : i === 0 ? 'inf' : 'pp'; cols[k].push(c); });
    const kindOf = r => {
      if (!r.forms || !r.forms.length) return '';
      const s = String(r.show || r.text);
      if (/^[^，；]*?是(?:“[^”]*”的)?(?:原样|动词原形)/.test(s)) return 'inf';
      if (/^[^，；]*?是过去分词/.test(s)) return 'pp';
      return '';
    };
    const att = { inf: [], perf: [], pp: [] }, rest = [];
    rows.forEach((r, i) => { const k = kindOf(r); if (k) att[k].push(i); else rest.push(i); });
    ['inf', 'pp'].forEach(k => {
      if (att[k].length < 2) return;
      const me = att[k].find(i => rows[i].me), keep = me != null ? me : att[k][0];
      att[k].forEach(i => { if (i !== keep) rest.push(i); });
      att[k] = [keep];
    });
    rest.sort((a, b) => a - b);
    const steps = [];
    K.forEach(k => {
      if (cols[k].length) steps.push({ t: 'rule', k });
      att[k].forEach(i => { if (pick.includes(i)) steps.push({ t: 'row', k, i }); });
    });
    rest.forEach(i => { if (pick.includes(i)) steps.push({ t: 'row', k: '', i }); });
    return { cols, att, rest, steps, nRules: K.filter(k => cols[k].length).length };
  }
  // 拉丁语一个样子里哪几个字母是词尾（灰色）：原形 -are / -ere / -ire / -re / -i…，过去式 -i，过去分词 -us
  function endMask(la, k) {
    const s = String(la || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
    const m = (k === 'inf' ? /(?:are|ere|ire|ari|eri|iri|re|ri|i)$/ : k === 'perf' ? /i$/ : /(?:us|um)$/).exec(s);
    const n = m ? m[0].length : 0;
    return [...s].map((_, j) => j >= s.length - n);
  }
  // 6.5：三个样子一栏一栏画：框（词根的字母用这一部分的颜色、加上或变了的字母绿色带下划线、词尾灰色）→ 紧贴着的这一栏的规律 →
  //   “英语里 duce …”（分工里用这个样子的那一条）；最底下是别的分工（英语有时直接拿过去分词当动词…、duc 原样留在…）
  function verbCols(ctx, part, x0, y0, w, f, sc, tl, p) {
    const V = part.verb, P = part.vplan, rows = part.fgRows || [], col = part.color;
    const root = part.base || String(part.text || '').replace(/\(.*?\)/g, '');
    const mk = sc.marks && sc.marks.length >= 1 ? sc.marks : null, nS = P.steps.length;
    const st = Math.min(0.16, 0.8 / (nS + 1));
    const at = k => (mk && mk[k] != null ? clamp((tl - mk[k] + 0.12) / 0.4) : span(p, 0.05 + k * st, 0.05 + k * st + 0.08));
    const stepAt = (t, k, i) => { const s = P.steps.findIndex(x => x.t === t && x.k === k && (i == null || x.i === i)); return s >= 0 ? at(1 + s) : at(nS) * 0.72; };
    const get = k => V.forms.find(x => x.k === k) || null;
    const K = ['inf', 'perf', 'pp'], FM = { inf: get('原形'), perf: get('过去式'), pp: get('过去分词') };
    const own = String(part.text || '').replace(/\(.*?\)/g, '').replace(/[()]/g, '');
    const tags = { inf: '', perf: '', pp: '' };
    ['inf', 'pp'].forEach(k => { const i = P.att[k][0]; if (i != null && rows[i].forms.length) tags[k] = rows[i].forms.slice(0, 2).join(' / ').replace(/-/g, ''); });
    if (part.verbAt) tags[part.verbAt] = own;
    // 原形要去掉前缀才是词根的（experiri、defendere）：前缀的字母也是灰的
    const kb0 = FM.inf ? rootLetters(root, FM.inf.la) : [], k0 = kb0.indexOf(true);
    const pre0 = k0 >= 2 ? String(FM.inf.la).slice(0, k0).toLowerCase() : '';
    // 第一行：标题，右边是颜色说明
    ctx.globalAlpha = f * at(1);
    txt(ctx, '拉丁语动词的三个样子', x0, y0 + 18, { size: 25, weight: 'bold', color: '#2B6CB0' });
    setFont(ctx, 25, ZH, 'bold');
    txt(ctx, '像英语的 do → did → done', x0 + ctx.measureText('拉丁语动词的三个样子').width + 18, y0 + 18, { size: 20, color: C.soft });
    let lx = x0 + w;
    [['词尾', '#9A9184', '#EFEBE3'], ['变了的字母', '#1E9E4A', '#DFF3E4'], ['词根', col, tint(col, 0.86)]].forEach(([t, c, bg]) => { lx -= chip(ctx, t, lx, y0 + 10, { size: 18, align: 'right', bg, color: c }) + 10; });
    ctx.globalAlpha = 1;
    const gap = 40, bw = (w - gap * 2) / 3, bh = 112, by = y0 + 40;
    const showRule = (c, k) => String(c).replace(/（[^（）]*→[^（）]*）/g, '').replace(k === 'inf' ? /^原形(?=去掉)/ : k === 'perf' ? /^过去式是\s*/ : /^过去分词是\s*/, '').trim();
    // 量：规律几行（三栏取最多的，下面的卡片对齐）、卡片多高
    let rz = 23, rMax = 0;
    const RL = {};
    for (; rz >= 17; rz -= 1) {
      setFont(ctx, rz, ZH, 'normal'); rMax = 0;
      K.forEach(k => { RL[k] = P.cols[k].length ? wrap(ctx, P.cols[k].map(c => showRule(c, k)).join('；'), bw - 26, 4) : []; rMax = Math.max(rMax, RL[k].length); });
      if (rMax <= 3) break;
    }
    const rlh = rz * 1.38, rTop = by + bh + 10, rH = rMax ? rMax * rlh + 18 : 0, cardY = rTop + rH + 14;      // 规律：浅黄底，紧贴在框下面，三栏一样高
    const cz = 21, clh = cz * 1.4, exz = 18, CARD = {};
    let cMax = 0;
    K.forEach(k => {
      const i = P.att[k] && P.att[k][0];
      if (i == null) return;
      const r = rows[i];
      setFont(ctx, cz, ZH, 'normal');
      const ls = wrap(ctx, String(r.show || r.text).replace(/[。；]+$/, ''), bw - 28, 3);
      const h = 58 + ls.length * clh + (r.ex.length ? exz * 1.6 : 0) + 6;
      CARD[k] = { i, r, ls, h }; cMax = Math.max(cMax, h);
    });
    K.forEach((k, ci) => {
      const fm = FM[k], bx = x0 + ci * (bw + gap), mine = part.verbAt === k, qb = stepAt('rule', k);
      if (ci) txt(ctx, '→', bx - gap / 2, by + bh / 2 + 2, { size: 30, weight: 'bold', color: '#B9AE93', align: 'center', base: 'middle', alpha: f * qb });
      if (qb > 0) {
        ctx.globalAlpha = f * qb;
        if (!fm) {
          ctx.save(); ctx.setLineDash([8, 7]); rr(ctx, bx, by, bw, bh, 14); ctx.lineWidth = 2; ctx.strokeStyle = '#CFC6B0'; ctx.stroke(); ctx.restore();
          txt(ctx, '过去式', bx + 16, by + 26, { size: 18, weight: 'bold', color: '#A79C82' });
          txt(ctx, '没有单独的过去式', bx + bw / 2, by + 64, { size: 21, color: '#A79C82', align: 'center' });
        } else {
          rr(ctx, bx, by, bw, bh, 14); ctx.fillStyle = mine ? tint(col, 0.9) : '#FFFDF6'; ctx.fill();
          ctx.lineWidth = mine ? 3.5 : 1.5; ctx.strokeStyle = mine ? col : C.line; ctx.stroke();
          txt(ctx, fm.k, bx + 16, by + 28, { size: 20, weight: 'bold', color: mine ? col : '#2B6CB0' });
          const kb = rootLetters(root, fm.la), em = endMask(fm.la, k), la = [...fm.la];
          const pm = pre0 && String(fm.la).toLowerCase().startsWith(pre0) ? pre0.length : 0;
          const fz = fit(ctx, fm.la, EN, 'bold', 52, bw - 40, 22);
          setFont(ctx, fz, EN, 'bold');
          let cx = bx + bw / 2 - ctx.measureText(fm.la).width / 2;
          la.forEach((ch, j) => {
            const chg = !kb[j] && !em[j] && j >= pm;
            setFont(ctx, fz, EN, 'bold');
            const cw = ctx.measureText(ch).width;
            txt(ctx, ch, cx, by + 70, { size: fz, family: EN, weight: 'bold', color: kb[j] ? col : chg ? '#1E9E4A' : '#A39A8A' });
            if (chg) { ctx.save(); ctx.fillStyle = '#1E9E4A'; ctx.fillRect(cx, by + 77, cw, 3.5); ctx.restore(); }
            cx += cw;
          });
          const tag = tags[k] ? '英语 → ' + tags[k] : '';
          let tw2 = 0;
          if (tag) tw2 = chip(ctx, tag, bx + bw - 12, by + bh - 17, { size: 16, align: 'right', bg: mine ? col : '#E9EEF3', color: mine ? '#FFFFFF' : '#5B6B78' });
          if (fm.zh) { const g = '“' + fm.zh + '”', gz = fit(ctx, g, ZH, 'normal', 19, bw - 34 - tw2 - (tw2 ? 10 : 0), 13); txt(ctx, g, bx + 16, by + bh - 11, { size: gz, color: C.soft }); }
        }
        ctx.globalAlpha = f * qb;
        if ((RL[k] || []).length) { rr(ctx, bx, rTop, bw, rH, 12); ctx.fillStyle = '#F8F0DC'; ctx.fill(); }
        (RL[k] || []).forEach((ln, j) => txt(ctx, ln, bx + 13, rTop + 9 + rz * 0.92 + j * rlh, { size: rz, color: '#4A3B1A' }));
        ctx.globalAlpha = 1;
      }
      const cd = CARD[k];
      if (cd) {
        const q = stepAt('row', k, cd.i);
        if (q > 0) {
          const r = cd.r, yy = cardY;
          ctx.globalAlpha = f * q;
          rr(ctx, bx, yy, bw, cd.h, 14); ctx.fillStyle = r.me ? tint(col, 0.9) : '#FFFDF6'; ctx.fill();
          ctx.lineWidth = r.me ? 3 : 1.5; ctx.strokeStyle = r.me ? col : C.line; ctx.stroke();
          txt(ctx, '英语里', bx + 14, yy + 34, { size: 19, weight: 'bold', color: '#8A6A2A' });
          setFont(ctx, 19, ZH, 'bold');
          txt(ctx, r.forms.slice(0, 3).join(' '), bx + 24 + ctx.measureText('英语里').width, yy + 35, { size: 28, family: EN, weight: 'bold', color: r.me ? col : C.soft });
          if (r.me) chip(ctx, '这个词', bx + bw - 12, yy + 26, { size: 17, align: 'right', bg: col, color: '#FFFFFF' });
          cd.ls.forEach((ln, j) => txt(ctx, ln, bx + 14, yy + 58 + cz * 0.8 + j * clh, { size: cz, color: C.ink }));
          if (r.ex.length) { const e = r.ex.slice(0, 3).join('　'), ez = fit(ctx, e, EN, 'bold', exz, bw - 28, 12); txt(ctx, e, bx + 14, yy + cd.h - 12, { size: ez, family: EN, weight: 'bold', color: r.me ? col : '#8A7B55' }); }
          ctx.globalAlpha = 1;
        }
      }
    });
    // 最底下：别的分工（讲到的跟着配音出来；没讲到的跟着最后一句一起出来，淡一点；放不下先不写没讲到的例词，再去掉没讲到的条）
    const pickSet = new Set(P.steps.filter(s => s.t === 'row').map(s => s.i));
    let yb = cardY + (cMax ? cMax + 18 : 0), bz = 23, blh = 0, bms = [], noEx = false, shown = P.rest.slice();
    const lay = () => {
      blh = bz * 1.4;
      bms = shown.map(i => { const r = rows[i]; setFont(ctx, bz, ZH, 'normal'); const ex = r.ex.length && !(noEx && !pickSet.has(i));
        const ls = wrap(ctx, String(r.show || r.text), w - (r.forms.length ? 190 : 40) - (r.me && !ex ? 88 : 0), 2);
        return { i, r, ls, ex, h: 14 + ls.length * blh + (ex ? (bz - 4) * 1.45 : 0) }; });
      return yb + bms.reduce((a, m) => a + m.h + 10, 0) <= 704;
    };
    while (!lay() && bz > 17) bz -= 1;
    if (!lay()) { noEx = true; lay(); }
    while (!lay() && shown.some(i => !pickSet.has(i))) { const d = shown.filter(i => !pickSet.has(i)).pop(); shown = shown.filter(i => i !== d); }
    bms.forEach(m => {
      const r = m.r, q = pickSet.has(m.i) ? stepAt('row', '', m.i) : at(nS) * 0.72;
      if (q > 0) {
        ctx.globalAlpha = f * q;
        rr(ctx, x0, yb, w, m.h, 14); ctx.fillStyle = r.me ? tint(col, 0.9) : '#FFFDF6'; ctx.fill();
        ctx.lineWidth = r.me ? 3 : 1.5; ctx.strokeStyle = r.me ? col : C.line; ctx.stroke();
        const tx2 = x0 + (r.forms.length ? 170 : 20);
        if (r.forms.length) { const fmt = r.forms.slice(0, 3).join(' '), fz = fit(ctx, fmt, EN, 'bold', bz + 4, 140, 14); txt(ctx, fmt, x0 + 18, yb + 7 + blh * 0.72, { size: fz, family: EN, weight: 'bold', color: r.me ? col : C.soft }); }
        m.ls.forEach((ln, j) => txt(ctx, ln, tx2, yb + 7 + blh * 0.72 + j * blh, { size: bz, color: C.ink }));
        if (m.ex) txt(ctx, r.ex.slice(0, 6).join('　'), tx2, yb + 7 + m.ls.length * blh + (bz - 4) * 0.9, { size: bz - 4, family: EN, weight: 'bold', color: r.me ? col : '#8A7B55' });
        if (r.me) chip(ctx, '这个词', x0 + w - 14, yb + m.h - 16, { size: 16, align: 'right', bg: col, color: '#FFFFFF' });
        ctx.globalAlpha = 1;
      }
      yb += m.h + 10;
    });
  }
  function fengongShow(part) {
    const rows = part.fgRows || [], pick = part.fgSay || fengongPick(part), max = part.verb ? 4 : rows.length;
    const keep = pick.slice();
    for (let i = 0; i < rows.length && keep.length < max; i++) if (!keep.includes(i)) keep.push(i);
    return keep.sort((x, y) => x - y);
  }
  // 三个样子的框。slots：[{ k, la, zh } 或 null（没有单独的过去式）]；own：这一部分对着哪一个（inf / pp）；tags：{ inf: 'duce', pp: 'duct' } 英语里的写法
  function verbStrip(ctx, part, x0, y0, w, q, f, lt) {
    const V = part.verb, col = part.color, root = part.base || String(part.text || '').replace(/\(.*?\)/g, '');
    const get = k => V.forms.find(x => x.k === k) || null;
    const slots = [['inf', get('原形')], ['perf', get('过去式')], ['pp', get('过去分词')]];
    // 英语里的写法：这一部分自己的写在它对着的那个框上；别的框看分工里哪一条说“动词原形 / 原样”“过去分词”
    const own = String(part.text || '').replace(/\(.*?\)/g, '').replace(/[()]/g, '');
    const tags = { inf: '', perf: '', pp: '' };
    (part.fgRows || []).forEach(r => {
      if (!r.forms || !r.forms.length) return;
      const k = /过去分词/.test(r.text) ? 'pp' : /动词原形|原样/.test(r.text) ? 'inf' : '';
      if (k && !tags[k]) tags[k] = r.forms.slice(0, 2).join(' / ').replace(/-/g, '');
    });
    if (part.verbAt) tags[part.verbAt] = own;
    ctx.globalAlpha = f * q;
    txt(ctx, '拉丁语动词的三个样子', x0, y0 + 16, { size: 21, weight: 'bold', color: '#2B6CB0' });
    setFont(ctx, 21, ZH, 'bold');
    const cw = ctx.measureText('拉丁语动词的三个样子').width;
    txt(ctx, '像英语的 do → did → done', x0 + cw + 18, y0 + 16, { size: 18, color: C.soft });
    const gap = 46, bw = (w - gap * 2) / 3, bh = VERB_BOX_H, by = y0 + 28;
    slots.forEach(([k, fm], i) => {
      const qi = easeOut(clamp((lt - i * 0.22) / 0.4)) * q;            // 三个框挨个出来
      const bx = x0 + i * (bw + gap), mine = part.verbAt === k;
      if (i) txt(ctx, '→', bx - gap / 2, by + bh / 2 + 2, { size: 30, weight: 'bold', color: '#B9AE93', align: 'center', base: 'middle', alpha: f * qi });
      if (qi <= 0) return;
      ctx.globalAlpha = f * qi;
      if (!fm) {                                                       // 没有单独的过去式：虚线的空框
        ctx.save(); ctx.setLineDash([8, 7]); rr(ctx, bx, by, bw, bh, 14); ctx.lineWidth = 2; ctx.strokeStyle = '#CFC6B0'; ctx.stroke(); ctx.restore();
        txt(ctx, '过去式', bx + 16, by + 24, { size: 17, weight: 'bold', color: '#A79C82' });
        txt(ctx, '没有单独的过去式', bx + bw / 2, by + 60, { size: 21, color: '#A79C82', align: 'center' });
        return;
      }
      rr(ctx, bx, by, bw, bh, 14); ctx.fillStyle = mine ? tint(col, 0.9) : '#FFFDF6'; ctx.fill();
      ctx.lineWidth = mine ? 3.5 : 1.5; ctx.strokeStyle = mine ? col : C.line; ctx.stroke();
      txt(ctx, fm.k, bx + 16, by + 24, { size: 17, weight: 'bold', color: mine ? col : '#2B6CB0' });
      // 拉丁语（居中、大字）：和词根相同的字母上色；下面一行左边是中文，右边是英语里的写法
      const kb = rootLetters(root, fm.la), fz = fit(ctx, fm.la, EN, 'bold', 38, bw - 44, 22);
      setFont(ctx, fz, EN, 'bold');
      let lx = bx + bw / 2 - ctx.measureText(fm.la).width / 2;
      [...fm.la].forEach((ch, j) => { setFont(ctx, fz, EN, 'bold'); txt(ctx, ch, lx, by + 54, { size: fz, family: EN, weight: 'bold', color: kb[j] ? col : C.ink }); lx += ctx.measureText(ch).width; });
      const tag = tags[k] ? '英语 → ' + tags[k] : '';
      let tw = 0;
      if (tag) tw = chip(ctx, tag, bx + bw - 12, by + bh - 19, { size: 16, align: 'right', bg: mine ? col : '#E9EEF3', color: mine ? '#FFFFFF' : '#5B6B78' });
      if (fm.zh) { const g = '“' + fm.zh + '”', gz = fit(ctx, g, ZH, 'normal', 20, bw - 34 - tw - (tw ? 10 : 0), 13); txt(ctx, g, bx + 16, by + bh - 13, { size: gz, color: C.soft }); }
    });
    // 规律：一句一行（三句以内）；多了就接着排
    const qr = easeOut(clamp((lt - 0.9) / 0.5)) * q;
    let ry = by + bh + 28;
    if (qr > 0) {
      ctx.globalAlpha = f * qr;
      txt(ctx, '规律', x0, ry, { size: 20, weight: 'bold', color: '#8A6A2A' });
      const rx = x0 + 58, rw = w - 58;
      let lines = [];
      let size = 21;
      for (; size >= 17; size -= 2) {
        setFont(ctx, size, ZH, 'normal');
        lines = [];
        V.rules.forEach((cl, i) => { wrap(ctx, cl + (i < V.rules.length - 1 ? '；' : ''), rw, 2).forEach(ln => lines.push(ln)); });
        if (lines.length <= 3) break;
        const one = wrap(ctx, V.rule, rw, 3);                         // 一句一行排不下：连起来排
        if (one.length <= 3) { lines = one; break; }
      }
      lines = lines.slice(0, 3);
      lines.forEach((ln, i) => txt(ctx, ln, rx, ry + i * (size * 1.36), { size, color: C.ink }));
      ry += (lines.length - 1) * (size * 1.36);
    }
    ctx.globalAlpha = 1;
    return verbStripH(ctx, part, w);
  }
  // 三个样子那一条占多高（不画，只量）：标题 28 + 框 + 规律几行
  const VERB_BOX_H = 96;
  function verbStripH(ctx, part, w) {
    const V = part.verb, rw = w - 58;
    let n = 3, size = 21;
    for (; size >= 17; size -= 2) {
      setFont(ctx, size, ZH, 'normal');
      n = 0;
      V.rules.forEach((cl, i) => { n += wrap(ctx, cl + (i < V.rules.length - 1 ? '；' : ''), rw, 2).length; });
      if (n <= 3) break;
      const one = wrap(ctx, V.rule, rw, 3).length;
      if (one <= 3) { n = one; break; }
    }
    n = Math.min(3, Math.max(1, n));
    return 28 + VERB_BOX_H + 28 + (n - 1) * (size * 1.36) + 12;
  }
  // 6.4：前缀、后缀的“辨析”这一幕只讲辨析（用户：“把左上角的单词 produce 前缀辨析，右上角的 二 含义拆分、词根词缀去掉……身份放在前一页……
  // 辨析的地方就专门讲不同的前缀，只写辨析，然后下面放几个前缀的对比，最下面再写关系”）：
  //   最上面标题“辨析”和开头的总说（同样和“前面”有关）；中间一条一条对比（左边是词缀，右边是怎么用和例词，本词缀那一条描边、标“这个词”）；
  //   有“为什么用 -ous 不用 -ful”的，黄框在对比下面；最下面绿框“关系”。“前缀 pro-”那一行标题和“身份”框不在这一幕（身份在上一幕的卡片上）。
  //   配音的先后跟着画面：总说 → 一条一条 → 为什么用… → 关系
  function bianxiScene(ctx, film, part, p, sc) {
    if ((part.fgSay || fengongPick(part)).some(i => ((part.fgRows || [])[i].uses || []).some(u => u.demo))) { bianxiDemoScene(ctx, film, part, p, sc); return; }
    const f = fadeOf(sc, p), tl = sc.tl != null ? sc.tl : p * sc.dur;
    const rows = part.fgRows || [], pick = part.fgSay || fengongPick(part);
    const hasWhy = !!part.why, rel = part.rel || [], hasRel = rel.length > 0;
    const mk = sc.marks && sc.marks.length >= 1 ? sc.marks : null;
    const steps = 1 + pick.length + (hasWhy ? 1 : 0) + (hasRel ? 1 : 0), st = Math.min(0.2, 0.76 / steps);
    const at = k => (mk && mk[k] != null ? clamp((tl - mk[k] + 0.12) / 0.4) : span(p, 0.05 + k * st, 0.05 + k * st + 0.1));
    const x0 = 64, w = W - 128, TOP = 124, BOT = 694, TX = 196;
    // 最下面：关系（一条一段；字从 23 号往小试，五行以内放得下为止）；它上面：为什么用…
    let bottom = BOT, relBox = null, whyBox = null;
    if (hasRel) {
      const rw = w - 132;
      let rz = 24, lines = [];
      do { rz -= 1; setFont(ctx, rz, ZH, 'normal'); lines = [].concat(...rel.map(r => wrap(ctx, r.text, rw, 3))); } while (lines.length > (rz > 21 ? 5 : 6) && rz > 19);      // 一条一段，另起一行
      const rlh = rz * 1.45, rh = 24 + lines.length * rlh;
      relBox = { y: bottom - rh, h: rh, size: rz, lh: rlh, lines };
      bottom = relBox.y - 12;
    }
    if (hasWhy) {
      setFont(ctx, 23, ZH, 'normal');
      const ls = wrap(ctx, String(part.why.a).replace(/（[^（）]*）/g, ''), w - 48, 2);
      const wh = 56 + ls.length * 33;
      whyBox = { y: bottom - wh, h: wh, lines: ls };
      bottom = whyBox.y - 12;
    }
    // 对比的条目：字号从大到小试，放得下为止
    let show = fengongShow(part);
    let size = 28, lh = 0, exz = 0, ms = [], gap = 10, noEx = false, used = 0;
    const layout = () => {
      lh = size * 1.42; exz = Math.max(16, size - 5);
      ms = show.map(i => { const r = rows[i]; setFont(ctx, size, ZH, 'normal'); const ex = r.ex.length && !(noEx && !pick.includes(i));
        const ls = wrap(ctx, r.show || r.text, w - TX - 24 - (r.me && !ex ? 96 : 0), 3);          // 说自己的那一条右下角有“这个词”的牌子：没有例词那一行时，正文让开它
        return { i, ls, ex, h: 22 + ls.length * lh + (ex ? exz * 1.5 : 0) }; });
      const total = ms.reduce((a, m) => a + m.h, 0);
      gap = Math.max(6, Math.min(16, (bottom - TOP - total) / Math.max(1, ms.length)));
      used = total + gap * (ms.length - 1);
      return used <= bottom - TOP + 0.5;
    };
    // 6.4：字不小于 22 号——22 号还放不下，就去掉没讲到的条（从最后一条去起，右上角注“另有 N 条，见总表”）；只剩讲到的几条还放不下，字才再小
    const fitAt = min => { size = show.length <= 3 ? 29 : show.length === 4 ? 26 : 24; while (!layout() && size > min) size -= 1; return layout(); };
    let fits = fitAt(22);
    while (!fits && show.length > pick.length) { const drop = show.filter(i => !pick.includes(i)).pop(); show = show.filter(i => i !== drop); fits = fitAt(22); }
    if (!fits) fitAt(17);
    if (film._dbg) film._dbg.push(['bianxi', part.head || part.text, size, show.length + '/' + rows.length, layout(), relBox ? relBox.size + 'px×' + relBox.lines.length : '', whyBox ? whyBox.lines.length : 0, Math.round(bottom - TOP - used)]);
    // 标题：辨析 + 开头的总说
    ctx.globalAlpha = f * at(0);
    rr(ctx, x0, 52, 10, 50, 5); ctx.fillStyle = part.color; ctx.fill();
    txt(ctx, '辨析', x0 + 26, 95, { size: 48, weight: 'bold', color: C.ink });
    if (rows.lead) { const lz = fit(ctx, rows.lead, ZH, 'normal', 30, w - 200 - (show.length < rows.length ? 200 : 0), 18); txt(ctx, rows.lead, x0 + 150, 92, { size: lz, color: C.soft }); }
    if (show.length < rows.length) txt(ctx, '（另有 ' + (rows.length - show.length) + ' 条，见总表）', x0 + w, 92, { size: 19, color: C.faint, align: 'right' });
    ctx.globalAlpha = 1;
    let y = TOP + Math.max(0, (bottom - TOP - used) / 2);
    ms.forEach(m => {
      const r = rows[m.i], k = pick.indexOf(m.i), q = k >= 0 ? at(1 + k) : at(pick.length) * 0.72;      // 没讲到的条，跟着最后一条一起出来，淡一点
      if (q > 0) {
        ctx.globalAlpha = f * q;
        rr(ctx, x0, y, w, m.h, 16); ctx.fillStyle = r.me ? tint(part.color, 0.9) : '#FFFDF6'; ctx.fill();
        ctx.lineWidth = r.me ? 3 : 1.5; ctx.strokeStyle = r.me ? part.color : C.line; ctx.stroke();
        const fm = r.forms.slice(0, 3).join(' ') + (r.forms.length > 3 ? ' …' : '');
        if (fm) { const fz = fit(ctx, fm, EN, 'bold', size + 8, TX - 40, 14); txt(ctx, fm, x0 + 22, y + 12 + lh * 0.74, { size: fz, family: EN, weight: 'bold', color: r.me ? part.color : C.soft }); }
        m.ls.forEach((ln, j) => txt(ctx, ln, x0 + TX, y + 12 + lh * 0.74 + j * lh, { size, color: C.ink }));
        if (m.ex) txt(ctx, r.ex.slice(0, 6).join('　'), x0 + TX, y + 12 + m.ls.length * lh + exz * 0.95, { size: exz, family: EN, weight: 'bold', color: r.me ? part.color : '#8A7B55' });
        if (r.me) chip(ctx, '这个词', x0 + w - 14, y + m.h - 18, { size: 17, align: 'right', bg: part.color, color: '#FFFFFF' });
        ctx.globalAlpha = 1;
      }
      y += m.h + gap;
    });
    if (whyBox) {
      const q = at(1 + pick.length);
      if (q > 0) {
        ctx.globalAlpha = f * q;
        rr(ctx, x0, whyBox.y, w, whyBox.h, 16); ctx.fillStyle = '#FFF8D6'; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = '#F0D25A'; ctx.stroke();
        txt(ctx, '★ ' + part.why.q, x0 + 24, whyBox.y + 34, { size: 24, weight: 'bold', color: '#B7791F' });
        whyBox.lines.forEach((ln, j) => txt(ctx, ln, x0 + 24, whyBox.y + 68 + j * 33, { size: 23, color: C.ink }));
        ctx.globalAlpha = 1;
      }
    }
    if (relBox) {
      const q = at(1 + pick.length + (hasWhy ? 1 : 0));
      if (q > 0) {
        ctx.globalAlpha = f * q;
        rr(ctx, x0, relBox.y, w, relBox.h, 16); ctx.fillStyle = '#EEF8F0'; ctx.fill(); ctx.lineWidth = 2.5; ctx.strokeStyle = '#7CC49A'; ctx.stroke();
        txt(ctx, '关系', x0 + 24, relBox.y + 12 + relBox.lh * 0.74, { size: 25, weight: 'bold', color: '#1E7B4A' });
        relBox.lines.forEach((ln, j) => txt(ctx, ln, x0 + 108, relBox.y + 12 + relBox.lh * 0.74 + j * relBox.lh, { size: relBox.size, color: C.ink }));
        ctx.globalAlpha = 1;
      }
    }
  }
  // 6.7：“辨析”那一幕带演示（用户：“我希望这些能有演示，就像后面的组合一样，要不然干讲这个学生不一定理解”
  //   “重点是要说明是加动词还是加名词……加动词的效果和加名词的效果要体现出来，并加以说明”）：
  //   只画讲到的几条（别的右上角注“另有 N 条，见总表”）；每一条：左边词缀，右边简写的说明，下面每个用法一个小演示——
  //   牌子“名词、形容词前 / 动词词根前”+ 图 + 图 = 画 +“上学以前的” preschool；配音说到“比如 preschool”时这个演示一块一块出来。最下面照旧是“关系”
  // 6.18：讲到哪个用法，哪个就圈出来、放大（用户：“辨析里面，讲到那个规律，或者那个和哪个结合的时候，要圈起来变醒目一点，要不然不知道讲的是哪一个，
  //   另外这些图可以画大一点。目前有点小”）：
  //   - 讲到哪一条，那一条展开：它的演示放大（画占小半个画面）；别的条只留一行字、淡一点；
  //   - 这一条里讲到哪个用法，那个用法的演示变大、外面套一圈橙色，上面那行字里的规律（“名词、形容词前是“…之前的””）垫一道黄色；另一个用法缩小；
  //   - 时间跟着配音：说到这个用法的规律那半句（“比如 preschool”前面那一段）时换过去，和画里的 when 一样按字数折算；没配音的预览按比例；
  //   - 几条都讲完、念“为什么用…”“再看它们的关系”时回到总览：每一条的演示都是小图（6.7 的样子），正在念的那个框套一圈。
  const HI = '#F08A24';                                                       // 圈起来的颜色（橙）
  const easeIO = k => (k <= 0 ? 0 : k >= 1 ? 1 : k * k * (3 - 2 * k));
  // 一句配音里说到某个位置大约是几分之几（和 drawPic 的 whenT 一样：中文一个字一份、英文单词按长短折算、标点 0.7 份）
  const sayW = z => (String(z).match(/[A-Za-z']+|[\u3400-\u9fff]|[，。；、：！？,.;:!?]/g) || []).reduce((n, m) => n + (/[A-Za-z]/.test(m) ? Math.max(1, m.length / 3) : /[\u3400-\u9fff]/.test(m) ? 1 : 0.7), 0);
  function demoBox(ctx, part, D, tag, x, y, ww, hh, t0, tl, A, hi) {
    const col = part.color, k = j => clamp((tl - t0 - j * 0.28) / 0.32);
    if (k(0) <= 0) return;
    // 6.18：框高过 124（6.7 的样子）就跟着放大：图标、字、画都按框的高度放大
    const z = clamp(hh / 124, 1, 2.6), zt = Math.min(z, 1.75), zx = Math.min(z, 1.8), zc = Math.min(z, 1.4);
    if (hi > 0) {                                                               // 正在讲的这个用法：外面一圈橙色，带一点光
      ctx.save(); ctx.globalAlpha = A * k(0) * hi; ctx.shadowColor = 'rgba(240,138,36,.55)'; ctx.shadowBlur = 18;
      rr(ctx, x - 5, y - 5, ww + 10, hh + 10, 16); ctx.lineWidth = 5; ctx.strokeStyle = HI; ctx.stroke(); ctx.restore();
    }
    ctx.globalAlpha = A * k(0);
    rr(ctx, x, y, ww, hh, 12); ctx.fillStyle = '#FFFFFF'; ctx.fill(); ctx.lineWidth = 1.5; ctx.strokeStyle = tint(col, 0.66); ctx.stroke();
    const tagH = tag ? 28 * zc : 6;
    if (tag) chip(ctx, '加在' + tag, x + 10 * zc, y + 17 * zc, { size: 15 * zc, bg: hi > 0.5 ? HI : col, color: '#FFFFFF' });
    const n = D.terms.length, cw = (n >= 3 ? 58 : 72) * zt, top = y + tagH, avail = hh - tagH - 6;
    const isz = Math.max(26, Math.min(42 * zt, avail * 0.42)), blk = isz + 40 * zt, iy = top + Math.max(4, (avail - blk) / 2) + isz * 0.55;
    let xx = x + 8 * zt;
    D.terms.forEach((t, j) => {
      const q = k(1 + j);
      ctx.globalAlpha = A * q;
      if (q > 0) {
        if (t.icon) emoji(ctx, t.icon, xx + cw / 2, iy, isz); else badge(ctx, t.t, xx + cw / 2, iy, isz, col);
        const gz = fit(ctx, t.g, ZH, 'bold', 16 * zt, cw + 6, 11);
        txt(ctx, t.g, xx + cw / 2, iy + isz * 0.5 + 18 * zt, { size: gz, weight: 'bold', color: col, align: 'center' });
        txt(ctx, t.t, xx + cw / 2, iy + isz * 0.5 + 36 * zt, { size: 15 * zt, family: EN, weight: 'bold', color: C.faint, align: 'center' });
      }
      xx += cw;
      ctx.globalAlpha = A * k(2 + j);
      txt(ctx, j < n - 1 ? '+' : '=', xx + 9 * zt, iy, { size: 24 * zt, weight: 'bold', color: C.faint, align: 'center', base: 'middle' });
      xx += 18 * zt;
    });
    const q = k(1 + n), pw = Math.min(150 * z, Math.max(96, ww - (xx - x) - 150 * zx)), ph = avail;
    if (q > 0) {
      ctx.globalAlpha = A * q;
      if (D.pic) drawPic(ctx, D.pic, xx + 2, top, pw, ph, { q: 1, lt: Math.max(0, tl - t0) });
      else { rr(ctx, xx + 2, top, pw, ph, 10); ctx.fillStyle = '#FFF8D6'; ctx.fill(); if (D.icon) emoji(ctx, D.icon, xx + 2 + pw / 2, top + ph / 2, Math.min(ph * 0.66, pw * 0.6)); else txt(ctx, D.w, xx + 2 + pw / 2, top + ph / 2, { size: 22 * zx, family: EN, weight: 'bold', color: C.ink, align: 'center', base: 'middle' }); }
      const tx = xx + pw + 12 * zx, tw = x + ww - tx - 8;
      setFont(ctx, 18 * zx, ZH, 'bold');
      const ls = wrap(ctx, '“' + D.lit + '”', tw, 2), tb = 20 * zx + ls.length * 22 * zx + 4 * zx + (D.m ? 21 * zx : 0);
      const ty = z > 1.2 ? top + Math.max(0, (ph - tb) / 2) : top;              // 放大了就和画上下对齐居中
      ls.forEach((ln, j) => txt(ctx, ln, tx, ty + 20 * zx + j * 22 * zx, { size: 18 * zx, weight: 'bold', color: C.ink }));
      const wy = ty + 20 * zx + ls.length * 22 * zx + 4 * zx, wz = fit(ctx, D.w, EN, 'bold', 22 * zx, tw, 14);
      txt(ctx, D.w, tx, wy, { size: wz, family: EN, weight: 'bold', color: col });
      if (D.m) { const mz = fit(ctx, D.m, ZH, 'normal', 15 * zx, tw, 11); txt(ctx, D.m, tx, wy + 21 * zx, { size: mz, color: C.soft }); }
    }
    ctx.globalAlpha = 1;
  }
  // 规律那半句：这个用法前面的话里最后一个“：”后面那段（“名词、形容词前是“…之前的””）
  const ruleOf = u => { let c = String(u.clause || ''); const i = c.lastIndexOf('：'); if (i >= 0) c = c.slice(i + 1); return c.replace(/^[，；、\s]+|[，；、。\s]+$/g, ''); };
  function bianxiDemoScene(ctx, film, part, p, sc) {
    const f = fadeOf(sc, p), tl = sc.tl != null ? sc.tl : p * sc.dur;
    const rows = part.fgRows || [], pick = part.fgSay || fengongPick(part);
    const hasWhy = !!part.why, rel = part.rel || [], hasRel = rel.length > 0;
    const mk = sc.marks && sc.marks.length >= 1 ? sc.marks : null;
    const steps = 1 + pick.length + (hasWhy ? 1 : 0) + (hasRel ? 1 : 0), st = Math.min(0.22, 0.8 / steps);
    const segA = k => (mk && mk[k] != null ? mk[k] : (0.04 + k * st) * sc.dur);
    const segB = k => (mk && mk[k + 1] != null ? mk[k + 1] : mk ? sc.dur : (0.04 + (k + 1) * st) * sc.dur);
    const segE = k => (Array.isArray(sc.ends) && sc.ends[k] != null ? sc.ends[k] : segB(k));
    const at = k => clamp((tl - segA(k) + 0.12) / 0.4);
    const ramp = t0 => easeIO((tl - t0 + 0.2) / 0.45);
    const x0 = 56, w = W - 112, TOP = 100, BOT = 708, TX = 142, sw = w - TX - 18;
    let bottom = BOT, relBox = null, whyBox = null;
    if (hasRel) {
      const rw = w - 120;
      let rz = 22, lines = [];
      do { rz -= 1; setFont(ctx, rz, ZH, 'normal'); lines = [].concat(...rel.map(r => wrap(ctx, r.text, rw, 3))); } while (lines.length > 3 && rz > 17);
      const rlh = rz * 1.42, rh = 18 + lines.length * rlh;
      relBox = { y: bottom - rh, h: rh, size: rz, lh: rlh, lines };
      bottom = relBox.y - 10;
    }
    if (hasWhy) {
      setFont(ctx, 21, ZH, 'normal');
      const ls = wrap(ctx, String(part.why.a).replace(/（[^（）]*）/g, ''), w - 48, 2);
      const wh = 48 + ls.length * 29;
      whyBox = { y: bottom - wh, h: wh, lines: ls };
      bottom = whyBox.y - 10;
    }
    // 总览（6.7 的样子）：几条一起放得下的字号、演示框高
    const show = pick.slice();
    let size = 24, DH = 124, ms = [], gap = 10, used = 0;
    const layout = () => {
      const lh = size * 1.36;
      ms = show.map(i => {
        const r = rows[i]; setFont(ctx, size, ZH, 'normal');
        const ls = wrap(ctx, r.show || r.text, w - TX - 24, 3);
        const us = (r.uses || []).filter(u => u.demo).slice(0, 2);
        return { i, ls, us, lh, h: 14 + ls.length * lh + (us.length ? DH + 10 : 8), th: 14 + ls.length * lh + 8 };
      });
      used = ms.reduce((a, m) => a + m.h, 0);
      gap = Math.max(6, Math.min(14, (bottom - TOP - used) / Math.max(1, ms.length)));
      used += gap * (ms.length - 1);
      return used <= bottom - TOP + 0.5;
    };
    while (!layout() && (size > 19 || DH > 86)) { if (DH > 108) DH -= 4; else if (size > 21) size -= 1; else if (DH > 96) DH -= 4; else if (size > 19) size -= 1; else DH -= 4; }
    // 6.18：展开时的大图：别的条都只剩一行字，剩下的高度给正在讲的这一条（两个用法时：讲到的那个大、另一个小）
    const nR = ms.length, GAPX = 10, SMALL = Math.min(DH, 96);
    const free = BOT - TOP - ms.reduce((a, m) => a + m.th, 0) - GAPX * (nR - 1) - 12;
    ms.forEach(m => {
      const n = m.us.length;
      m.big = n ? Math.max(DH, Math.min(n === 1 ? 330 : 300, free - 2 - (n - 1) * (SMALL + 10))) : 0;
      m.tot = n ? m.big + (n - 1) * (SMALL + 10) : 0;
    });
    const tOv = hasWhy || hasRel ? segA(1 + pick.length) : Infinity, ov = ramp(tOv);
    const T = Array.isArray(sc.texts) ? sc.texts : null;
    ms.forEach((m, kk) => {                                                     // 每个用法从几秒开始讲（规律那半句开头）
      const a0 = segA(1 + kk), b0 = Math.max(a0 + 1, segE(1 + kk)), n = m.us.length, tx = T ? String(T[1 + kk] || '') : '';
      m.u0 = m.us.map((u, j) => {
        const est = a0 + (n === 1 ? 0.15 : j === 0 ? 0.22 : 0.6) * (b0 - a0), ex = (u.ex || [])[0], pos = tx && ex ? tx.indexOf(ex) : -1;
        if (pos < 0) return mk ? est : Math.min(est, sc.dur * 0.8);
        const s = Math.max(tx.lastIndexOf('；', pos), tx.lastIndexOf('：', pos)) + 1;
        return Math.max(a0, a0 + (b0 - a0) * sayW(tx.slice(0, s)) / Math.max(1, sayW(tx)) - 0.1);
      });
    });
    // 展开：讲到这一条第一个用法的规律时展开；下一条讲到它的用法时才收起（下一条开头那半句，这一条还开着、淡一点，画面不空）
    const openT = kk => (ms[kk].u0.length ? ms[kk].u0[0] - 0.25 : segA(1 + kk));
    ms.forEach((m, kk) => {
      m.e = Math.min(ramp(openT(kk)), 1 - ramp(kk + 1 < nR ? openT(kk + 1) : tOv));
      m.fo = Math.min(ramp(segA(1 + kk)), 1 - ramp(kk + 1 < nR ? segA(2 + kk) : tOv));      // 正在念这一条
      m.H = m.th + m.e * (m.tot ? m.tot + 2 : 0) + ov * (m.us.length ? DH + 2 : 0);
    });
    const anyFo = Math.max(0, ...ms.map(m => m.fo));
    if (film._dbg) film._dbg.push(['bianxiDemo', part.head || part.text, size, DH, show.length + '/' + rows.length, layout(), relBox ? relBox.size + 'px×' + relBox.lines.length : '', ms.map(m => Math.round(m.big)).join('/')]);
    ctx.globalAlpha = f * at(0);
    rr(ctx, x0, 40, 10, 46, 5); ctx.fillStyle = part.color; ctx.fill();
    txt(ctx, '辨析', x0 + 24, 80, { size: 44, weight: 'bold', color: C.ink });
    if (rows.lead) { const lz = fit(ctx, rows.lead, ZH, 'normal', 28, w - 380, 18); txt(ctx, rows.lead, x0 + 136, 78, { size: lz, color: C.soft }); }
    if (show.length < rows.length) txt(ctx, '（另有 ' + (rows.length - show.length) + ' 条，见总表）', x0 + w, 78, { size: 18, color: C.faint, align: 'right' });
    ctx.globalAlpha = 1;
    const bot = lerp(BOT, bottom, ov), tot = ms.reduce((a, m) => a + m.H, 0) + GAPX * (nR - 1);
    let y = lerp(TOP, TOP + Math.max(0, (bot - TOP - tot) / 2), ov);            // 一条一条讲的时候从上往下排（收起、展开时上面的不动），总览时上下居中
    ms.forEach((m, kk) => {
      const r = rows[m.i], q = at(1 + kk);
      if (q > 0) {
        const A = f * q * (1 - 0.55 * anyFo * (1 - m.fo));                     // 正在念别的条：这一条淡一点
        ctx.globalAlpha = A;
        rr(ctx, x0, y, w, m.H, 16); ctx.fillStyle = r.me ? tint(part.color, 0.9) : '#FFFDF6'; ctx.fill();
        ctx.lineWidth = r.me ? 3 : 1.5; ctx.strokeStyle = r.me ? part.color : C.line; ctx.stroke();
        const fm = r.forms.slice(0, 3).join(' ') + (r.forms.length > 3 ? ' …' : '');
        if (fm) { const fz = fit(ctx, fm, EN, 'bold', size + 10, TX - 30, 14); txt(ctx, fm, x0 + 18, y + 10 + m.lh * 0.78, { size: fz, family: EN, weight: 'bold', color: r.me ? part.color : C.soft }); }
        // 用法：讲到哪个（hi 0 → 1），哪个大（act）
        const n = m.us.length, nextT = kk + 1 < nR ? segA(2 + kk) : tOv;
        const hiOf = j => ramp(m.u0[j]) * (j + 1 < n ? 1 - ramp(m.u0[j + 1]) : 1) * (1 - ramp(nextT));
        const actOf = j => (n === 1 ? 1 : j === 0 ? 1 - ramp(m.u0[1]) : ramp(m.u0[1]));
        // 规律那半句垫一道黄色（这一条字里找得到才垫）
        const joined = m.ls.join('');
        m.us.forEach((u, j) => {
          const h = hiOf(j), rule = ruleOf(u), s0 = rule ? joined.indexOf(rule) : -1;
          if (h <= 0.01 || s0 < 0) return;
          let off = 0;
          setFont(ctx, size, ZH, 'normal');
          m.ls.forEach((ln, li) => {
            const a = Math.max(s0, off), b = Math.min(s0 + rule.length, off + ln.length);
            if (b > a) {
              const xa = x0 + TX + ctx.measureText(ln.slice(0, a - off)).width, xb = x0 + TX + ctx.measureText(ln.slice(0, b - off)).width, by = y + 10 + m.lh * 0.74 + li * m.lh;
              ctx.save(); ctx.globalAlpha = A * h * 0.85; rr(ctx, xa - 4, by - size * 0.9, xb - xa + 8, size * 1.2, 7); ctx.fillStyle = '#FFE07A'; ctx.fill(); ctx.restore();
            }
            off += ln.length;
          });
        });
        ctx.globalAlpha = A;
        m.ls.forEach((ln, j) => txt(ctx, ln, x0 + TX, y + 10 + m.lh * 0.74 + j * m.lh, { size, color: C.ink }));
        if (r.me) {                                                              // 这个词：展开、总览时在左边词缀下面；只剩一行字时贴在框的上沿
          if (m.H >= m.th + 40) chip(ctx, '这个词', x0 + 18, y + m.H - 22, { size: 16, bg: part.color, color: '#FFFFFF' });
          else chip(ctx, '这个词', x0 + w - 18, y, { size: 15, align: 'right', bg: part.color, color: '#FFFFFF' });      // 贴在框上沿的右头，不压字
        }
        const sy = y + 14 + m.ls.length * m.lh;
        if (n && m.e > 0.01) {                                                   // 展开：上下排，讲到的那个大
          ctx.save(); ctx.beginPath(); ctx.rect(x0, sy - 8, w, m.e * (m.tot + 2) + 8); ctx.clip();
          let yy = sy;
          m.us.forEach((u, j) => {
            const a = actOf(j), hh = lerp(SMALL, m.big, a), ww = lerp(Math.min(sw, 560), sw, a);
            demoBox(ctx, part, u.demo, u.tag, x0 + TX, yy, ww, hh, m.u0[j], tl, A * m.e, hiOf(j));
            yy += hh + 10;
          });
          ctx.restore();
        }
        if (n && ov > 0.01) {                                                    // 总览：左右排、小图（6.7 的样子）
          const by = sy + (m.e > 0.01 ? m.e * (m.tot + 2) : 0), bw = Math.min(560, (sw - 12 * (n - 1)) / n);
          m.us.forEach((u, j) => demoBox(ctx, part, u.demo, u.tag, x0 + TX + j * (bw + 12), by, bw, DH * ov, m.u0[j], tl, A * ov, 0));
        }
        ctx.globalAlpha = 1;
      }
      y += m.H + GAPX;
    });
    const ring = (bx, by, bw, bh, h) => { if (h <= 0.01) return; ctx.save(); ctx.globalAlpha = f * h; ctx.shadowColor = 'rgba(240,138,36,.5)'; ctx.shadowBlur = 16; rr(ctx, bx - 5, by - 5, bw + 10, bh + 10, 18); ctx.lineWidth = 5; ctx.strokeStyle = HI; ctx.stroke(); ctx.restore(); };
    if (whyBox) {
      const q = at(1 + pick.length);
      if (q > 0) {
        ring(x0, whyBox.y, w, whyBox.h, q * (hasRel ? 1 - ramp(segA(2 + pick.length)) : 1));
        ctx.globalAlpha = f * q;
        rr(ctx, x0, whyBox.y, w, whyBox.h, 14); ctx.fillStyle = '#FFF8D6'; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = '#F0D25A'; ctx.stroke();
        txt(ctx, '★ ' + part.why.q, x0 + 22, whyBox.y + 30, { size: 22, weight: 'bold', color: '#B7791F' });
        whyBox.lines.forEach((ln, j) => txt(ctx, ln, x0 + 22, whyBox.y + 60 + j * 29, { size: 21, color: C.ink }));
        ctx.globalAlpha = 1;
      }
    }
    if (relBox) {
      const q = at(1 + pick.length + (hasWhy ? 1 : 0));
      if (q > 0) {
        ring(x0, relBox.y, w, relBox.h, q);
        ctx.globalAlpha = f * q;
        rr(ctx, x0, relBox.y, w, relBox.h, 14); ctx.fillStyle = '#EEF8F0'; ctx.fill(); ctx.lineWidth = 2.5; ctx.strokeStyle = '#7CC49A'; ctx.stroke();
        txt(ctx, '关系', x0 + 22, relBox.y + 9 + relBox.lh * 0.74, { size: 23, weight: 'bold', color: '#1E7B4A' });
        relBox.lines.forEach((ln, j) => txt(ctx, ln, x0 + 96, relBox.y + 9 + relBox.lh * 0.74 + j * relBox.lh, { size: relBox.size, color: C.ink }));
        ctx.globalAlpha = 1;
      }
    }
  }
  // 6.8：词根的“形态”（用户：“先写词根和含义 duc-；形态：原形 duc，来自拉丁语原形 ducere，然后去掉尾部 ere，这里要有去掉尾部的演示，举出例词；过去式 dux……写出怎么变化的，并做演示”）。
  //   上面一行：词根 duc- 和意思，右边“形态 · 像英语的 do → did → done”；下面每个形态一行：左边名字和原词（词根的字母上色、变了的字母绿色带下划线、词尾灰色），
  //   说到这一行时词尾划掉、往下滑走，箭头“去掉 -ere”，右边出英语里的写法；最右边是英语里的用法和例词（说到才出来）。本词用的那一行描边、标“这个词”
  S.xingtai = (ctx, film, p, sc) => {
    const part = film.parts[sc.i], X = part.xt, f = fadeOf(sc, p), tl = sc.tl != null ? sc.tl : p * sc.dur;
    const steps = xtSteps(X), N = steps.length, mk = sc.marks && sc.marks.length ? sc.marks : null;
    const stT = Math.min(0.17, 0.82 / N);
    const t0 = k => (mk && mk[k] != null ? mk[k] : (0.04 + k * stT) * sc.dur);
    const at = k => clamp((tl - t0(k) + 0.12) / 0.4);
    const col = part.color, x0 = 64, w = W - 128;
    // 第一行
    ctx.globalAlpha = f * at(0);
    let tx = x0 + chip(ctx, '词根', x0, 74, { size: 22, bg: tint(col, 0.82), color: col }) + 14;
    const rz = fit(ctx, X.root + '-', EN, 'bold', 48, 260, 30);
    txt(ctx, X.root + '-', tx, 90, { size: rz, family: EN, weight: 'bold', color: col });
    setFont(ctx, rz, EN, 'bold'); tx += ctx.measureText(X.root + '-').width + 18;
    const gz = fit(ctx, X.gloss, ZH, 'bold', 30, 360, 20);
    txt(ctx, X.gloss, tx, 88, { size: gz, weight: 'bold', color: C.ink });
    const an = X.analogy ? '像英语的 ' + X.analogy : '';
    if (an) txt(ctx, an, x0 + w, 88, { size: 20, color: C.soft, align: 'right' });
    setFont(ctx, 20, ZH, 'normal');
    const aw = an ? ctx.measureText(an).width + 16 : 0;
    txt(ctx, '形态', x0 + w - aw, 89, { size: 30, weight: 'bold', color: '#2B6CB0', align: 'right' });
    ctx.globalAlpha = 1;
    // 每个形态一行
    const n = X.forms.length, gap = 12, top = 116, bot = 708;
    const rh = Math.min(184, (bot - top - gap * (n - 1)) / n);
    X.forms.forEach((fm, j) => {
      const sD = steps.findIndex(s => s.t === 'demo' && s.j === j), sU = steps.findIndex(s => s.t === 'use' && s.j === j);
      const q = at(sD);
      if (q <= 0) return;
      const since = tl - t0(sD) + 0.12;
      const y = top + j * (rh + gap) + (1 - easeOut(q)) * 16, mine = fm.k === X.meK;
      ctx.globalAlpha = f * q;
      rr(ctx, x0, y, w, rh, 16); ctx.fillStyle = mine ? tint(col, 0.92) : '#FFFDF6'; ctx.fill();
      ctx.lineWidth = mine ? 3 : 1.5; ctx.strokeStyle = mine ? col : C.line; ctx.stroke();
      if (!fm.en) {                                                         // 没有单独的过去式：虚线、一句话
        ctx.save(); ctx.setLineDash([8, 7]); rr(ctx, x0 + 6, y + 6, w - 12, rh - 12, 12); ctx.lineWidth = 1.5; ctx.strokeStyle = '#CFC6B0'; ctx.stroke(); ctx.restore();
        chip(ctx, fm.k, x0 + 18, y + 30, { size: 20, bg: '#EFEBE3', color: '#8A7F6A' });
        txt(ctx, fm.src, x0 + 130, y + rh / 2 + 8, { size: 23, color: '#A79C82' });
        ctx.globalAlpha = 1; return;
      }
      let cx = x0 + 18 + chip(ctx, fm.k, x0 + 18, y + 30, { size: 20, bg: mine ? col : '#E3EEFA', color: mine ? '#FFFFFF' : '#2F6FB3' }) + 10;
      if (fm.zh) { txt(ctx, '“' + fm.zh + '”', cx, y + 37, { size: 20, color: C.soft }); setFont(ctx, 20, ZH, 'normal'); cx += ctx.measureText('“' + fm.zh + '”').width + 12; }
      if (mine) chip(ctx, '这个词', cx, y + 30, { size: 17, bg: col, color: '#FFFFFF' });
      // 原词：词根的字母上色，变了的字母绿色带下划线，前缀、词尾灰色；说到这一行 0.6 秒后词尾（和前缀）划掉、往下滑走
      const DW = 330, by = y + rh * 0.56;
      const la = fm.la || '', laN = la.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
      const okTail = fm.tail && laN.endsWith(fm.tail.toLowerCase()), okPre = fm.pre && laN.startsWith(fm.pre.toLowerCase());
      const kS = clamp((since - 0.7) / 0.5), kG = clamp((since - 1.2) / 0.5), kR = clamp((since - 1.4) / 0.4);
      if (la) {
        const fz = fit(ctx, la, EN, 'bold', 46, DW - 20, 22);
        const kb = rootLetters(X.root, la);      // 和词根 duc 比：duxi 的 x、ductus 的 t 是变了、加上的字母（绿色）
        setFont(ctx, fz, EN, 'bold');
        let lx = x0 + 22;
        [...la].forEach((ch, i) => {
          const end = (okTail && i >= la.length - fm.tail.length) || (okPre && i < fm.pre.length);
          const chg = !kb[i] && !end;
          setFont(ctx, fz, EN, 'bold');
          const cw = ctx.measureText(ch).width;
          const a = end ? 1 - 0.6 * kG : 1, dy = end ? kG * 8 : 0;
          txt(ctx, ch, lx, by + dy, { size: fz, family: EN, weight: 'bold', color: end ? '#A39A8A' : kb[i] ? col : '#1E9E4A', alpha: a });
          if (chg) { ctx.save(); ctx.globalAlpha *= a; ctx.fillStyle = '#1E9E4A'; ctx.fillRect(lx, by + 7, cw, 3); ctx.restore(); }
          if (end && kS > 0) { ctx.save(); ctx.globalAlpha *= a; ctx.strokeStyle = '#D9480F'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(lx - 1, by - fz * 0.3 + dy); ctx.lineTo(lx - 1 + (cw + 2) * kS, by - fz * 0.3 + dy); ctx.stroke(); ctx.restore(); }
          lx += cw;
        });
      }
      if (fm.rule) { setFont(ctx, 18, ZH, 'normal'); wrap(ctx, fm.rule, DW, 2).forEach((ln, i) => txt(ctx, ln, x0 + 22, by + 34 + i * 24, { size: 18, color: '#6E5520' })); }
      // 箭头和英语里的写法
      const ax = x0 + DW + 12, ex2 = ax + 96;
      const cut = [okPre ? fm.pre + '-' : '', okTail ? '-' + fm.tail : ''].filter(Boolean).join('、');
      ctx.globalAlpha = f * q * (la ? kR : 1);
      if (la) {
        ctx.strokeStyle = '#B69D62'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(ax, by - 14); ctx.lineTo(ex2 - 12, by - 14); ctx.stroke();
        ctx.fillStyle = '#B69D62'; ctx.beginPath(); ctx.moveTo(ex2 - 4, by - 14); ctx.lineTo(ex2 - 16, by - 21); ctx.lineTo(ex2 - 16, by - 7); ctx.closePath(); ctx.fill();
        if (cut) txt(ctx, '去掉 ' + cut, (ax + ex2) / 2 - 4, by - 26, { size: 16, color: '#A0782C', align: 'center' });
      }
      const ez = fit(ctx, fm.en, EN, 'bold', 54, 170, 26);
      txt(ctx, fm.en, ex2 + 4, by, { size: ez, family: EN, weight: 'bold', color: col });
      // 英语里的用法：说到才出来；只有一句话的（英语里几乎不用）跟着演示出来
      const ux = x0 + DW + 300, uw = x0 + w - ux - 16;
      ctx.globalAlpha = f * q * (la ? kR : 1);
      if (!fm.uses.length) {
        if (fm.note) { setFont(ctx, 22, ZH, 'normal'); wrap(ctx, fm.note, uw, 2).forEach((ln, i) => txt(ctx, ln, ux, by - 8 + i * 30, { size: 22, color: '#9A9184' })); }
        ctx.globalAlpha = 1; return;
      }
      const qu = sU >= 0 ? at(sU) : 0;
      if (qu <= 0) { ctx.globalAlpha = 1; return; }
      ctx.globalAlpha = f * q * qu;
      const items = fm.uses.slice().sort((a, b) => (b.me ? 1 : 0) - (a.me ? 1 : 0)).slice(0, 3);
      let sz = 21, L = [];
      const lay = () => { L = items.map(u => { setFont(ctx, sz, ZH, u.me ? 'bold' : 'normal'); return { u, ls: wrap(ctx, u.show, uw, u.me ? 2 : 1) }; }); return L.reduce((a, it) => a + it.ls.length * sz * 1.3 + (it.u.ex.length ? sz * 1.2 : 0) + 6, 0) <= rh - 22; };
      while (!lay() && sz > 15) sz -= 1;
      let uy = y + 14 + sz;
      txt(ctx, '英语里', ux - 2, y + 14 + sz, { size: 16, weight: 'bold', color: '#8A6A2A', align: 'right' });
      L.forEach(it => {
        if (uy > y + rh - 6) return;
        it.ls.forEach(ln => { txt(ctx, ln, ux + 6, uy, { size: sz, weight: it.u.me ? 'bold' : 'normal', color: it.u.me ? col : C.ink }); uy += sz * 1.3; });
        if (it.u.ex.length && uy <= y + rh - 4) { const e = it.u.ex.slice(0, 4).join('　'), ez2 = fit(ctx, e, EN, 'bold', sz - 2, uw, 12); txt(ctx, e, ux + 6, uy - 2, { size: ez2, family: EN, weight: 'bold', color: it.u.me ? col : '#8A7B55' }); uy += sz * 1.2; }
        uy += 6;
      });
      if (fm.uses.length > items.length) txt(ctx, '另有 ' + (fm.uses.length - items.length) + ' 条，见总表', x0 + w - 14, y + rh - 10, { size: 15, color: C.faint, align: 'right' });
      ctx.globalAlpha = 1;
    });
  };
  // 词根的“身份和分工”（6.0）；前缀、后缀新写法的那一幕是上面的 bianxiScene。
  // 6.4：页眉不画了，整幕往上挪 40；词根的另一种写法的“字母变化”（duc → duce　英语加不发音的 e）从上一幕的卡片挪到这儿，
  // 写在标题下面，配音第 2 句讲它（part.varInFg）
  S.fengong = (ctx, film, p, sc) => {
    const part = film.parts[sc.i], f = fadeOf(sc, p), tl = sc.tl != null ? sc.tl : p * sc.dur;
    if (part.bx && (part.kind === 'pre' || part.kind === 'suf')) { bianxiScene(ctx, film, part, p, sc); return; }
    const rows = part.fgRows || [], pick = part.fgSay || fengongPick(part);
    const hasVerb = !!part.verb, off = hasVerb ? 1 : 0, hasWhy = !!part.why, vOff = part.varInFg ? 1 : 0;
    const mk = sc.marks && sc.marks.length >= 1 ? sc.marks : null;
    const steps = 1 + vOff + off + pick.length + (hasWhy ? 1 : 0), st = Math.min(0.2, 0.76 / steps);
    const at = k => (mk && mk[k] != null ? clamp((tl - mk[k] + 0.12) / 0.4) : span(p, 0.05 + k * st, 0.05 + k * st + 0.1));
    const since = k => (mk && mk[k] != null ? tl - mk[k] + 0.12 : (p - (0.05 + k * st)) * sc.dur);      // 这一步开始以后过了几秒
    const x0 = 96, w = W - 192;
    // 标题：duct = 词根 duc 的另一种写法 / 后缀 -ous
    const isRoot = part.kind === 'root' || part.kind === 'word';
    const head = part.head && part.head.length <= 16 ? part.head : part.text;
    const kindZh = part.kind === 'pre' ? '前缀' : part.kind === 'suf' ? '后缀' : '词根';
    const ty = hasVerb ? 96 : 106;
    let tx = x0;
    tx += chip(ctx, kindZh, tx, ty - 18, { size: 24, bg: tint(part.color, 0.82), color: part.color, alpha: f * at(0) }) + 14;
    const hz = fit(ctx, head, EN, 'bold', hasVerb ? 50 : 56, 260, 30);
    txt(ctx, head, tx, ty, { size: hz, family: EN, weight: 'bold', color: part.color, alpha: f * at(0) });
    setFont(ctx, hz, EN, 'bold');
    tx += ctx.measureText(head).width + 18;
    if (isRoot && part.base) { txt(ctx, '= 词根 ' + part.base, tx, ty - 2, { size: 30, weight: 'bold', color: C.soft, alpha: f * at(0) }); setFont(ctx, 30, ZH, 'bold'); tx += ctx.measureText('= 词根 ' + part.base).width + 18; }
    // 身份
    const idt = String(part.idt || '').replace(/（[^（）]*）/g, '');
    ctx.globalAlpha = f * at(0);
    let top;
    if (hasVerb) {                                                       // 6.1：有三个样子的，身份写在标题右边，省出一行
      const ix = Math.max(tx + 6, x0 + 430), iw = x0 + w - ix;
      rr(ctx, ix, ty - 36, iw, 52, 14); ctx.fillStyle = '#EEF5FF'; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = '#9CC3EE'; ctx.stroke();
      txt(ctx, '身份', ix + 18, ty - 10, { size: 22, weight: 'bold', color: '#2B6CB0', base: 'middle' });
      const iz = fit(ctx, idt, ZH, 'bold', 26, iw - 96, 15);
      txt(ctx, idt, ix + 78, ty - 10, { size: iz, weight: 'bold', color: C.ink, base: 'middle' });
      ctx.globalAlpha = 1;
      if (part.vplan) { verbCols(ctx, part, x0, ty + 34, w, f, sc, tl, p); return; }      // 6.5：三个样子和分工合成一幕
      let vy = ty + 34;
      if (vOff) { ctx.globalAlpha = f * at(1); variantStrip(ctx, part, x0, vy + 18, w, part.color, 1.1); ctx.globalAlpha = 1; vy += 46; }
      const vh = verbStrip(ctx, part, x0, vy, w, at(1 + vOff), f, since(1 + vOff));
      top = vy + vh;
    } else if (!idt) {                                                   // 读不出一句身份的，不画这个框，分工往上挪
      ctx.globalAlpha = 1;
      top = 144;
      if (vOff) { ctx.globalAlpha = f * at(1); variantStrip(ctx, part, x0, top + 14, w, part.color, 1.1); ctx.globalAlpha = 1; top += 44; }
    } else {
      rr(ctx, x0, 132, w, 62, 16); ctx.fillStyle = '#EEF5FF'; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = '#9CC3EE'; ctx.stroke();
      txt(ctx, '身份', x0 + 22, 164, { size: 24, weight: 'bold', color: '#2B6CB0', base: 'middle' });
      const iz = fit(ctx, idt, ZH, 'bold', 28, w - 110, 18);
      txt(ctx, idt, x0 + 88, 164, { size: iz, weight: 'bold', color: C.ink, base: 'middle' });
      ctx.globalAlpha = 1;
      top = 212;
      if (vOff) { ctx.globalAlpha = f * at(1); variantStrip(ctx, part, x0, top + 16, w, part.color, 1.1); ctx.globalAlpha = 1; top += 46; }
    }
    // 分工：一条一条
    const bottom = hasWhy ? 590 : 682;
    let show = fengongShow(part);
    // 字号从大到小试，放得下为止；最小的字号还放不下：先不写没讲到那几条的例词，再去掉没讲到的条
    let size = 23, lh = 0, exz = 0, ms = [], gap = 8, noEx = false;
    const layout = () => {
      lh = size * 1.4; exz = Math.max(15, size - 4);
      ms = show.map(i => { const r = rows[i]; setFont(ctx, size, ZH, 'normal'); const ex = r.ex.length && !(noEx && !pick.includes(i));
        const ls = wrap(ctx, r.show || r.text, w - 210 - (r.me && !ex ? 88 : 0), hasVerb ? 2 : 3);          // 说自己的那一条右下角有“这个词”的牌子：没有例词那一行时，正文让开它
        return { i, ls, ex, h: 16 + ls.length * lh + (ex ? exz * 1.45 : 0) }; });
      const total = ms.reduce((a, m) => a + m.h, 0);
      gap = Math.max(5, Math.min(16, (bottom - top - 20 - total) / Math.max(1, ms.length)));
      return total + gap * ms.length + 20 <= bottom - top + 0.5;
    };
    const n0 = show.length;
    size = n0 <= 3 ? 26 : n0 === 4 ? 23 : 21;
    if (hasVerb) size = Math.min(size, 23);
    while (!layout() && size > 17) size -= 1;
    if (!layout()) { noEx = true; layout(); }
    while (!layout() && show.length > pick.length) { const drop = show.filter(i => !pick.includes(i)).pop(); show = show.filter(i => i !== drop); }
    let y = top;
    txt(ctx, '分工' + (rows.lead ? '　' + rows.lead : ''), x0, y + 8, { size: 22, weight: 'bold', color: '#8A6A2A', alpha: f * at(rows.lead ? 0 : 1 + vOff + off) });
    if (show.length < rows.length) txt(ctx, '（另有 ' + (rows.length - show.length) + ' 种写法，见总表）', x0 + w, y + 8, { size: 17, color: C.faint, align: 'right', alpha: f * at(1 + vOff + off) });
    y += 20;
    ms.forEach(m => {
      const r = rows[m.i], k = pick.indexOf(m.i), q = k >= 0 ? at(1 + vOff + off + k) : at(1 + vOff + off + pick.length - 1) * 0.72;      // 没讲到的条，跟着最后一条一起出来，淡一点
      if (q > 0) {
        ctx.globalAlpha = f * q;
        rr(ctx, x0, y, w, m.h, 14); ctx.fillStyle = r.me ? tint(part.color, 0.9) : '#FFFDF6'; ctx.fill();
        ctx.lineWidth = r.me ? 3 : 1.5; ctx.strokeStyle = r.me ? part.color : C.line; ctx.stroke();
        const fm = r.forms.slice(0, 3).join(' ') + (r.forms.length > 3 ? ' …' : '');
        if (fm) { const fz = fit(ctx, fm, EN, 'bold', size + 4, 150, 14); txt(ctx, fm, x0 + 18, y + 10 + lh * 0.72, { size: fz, family: EN, weight: 'bold', color: r.me ? part.color : C.soft }); }
        m.ls.forEach((ln, j) => txt(ctx, ln, x0 + 180, y + 10 + lh * 0.72 + j * lh, { size, color: C.ink }));
        if (m.ex) txt(ctx, r.ex.slice(0, 6).join('　'), x0 + 180, y + 10 + m.ls.length * lh + exz * 0.9, { size: exz, family: EN, weight: 'bold', color: r.me ? part.color : '#8A7B55' });
        if (r.me) chip(ctx, '这个词', x0 + w - 14, y + m.h - 16, { size: 16, align: 'right', bg: part.color, color: '#FFFFFF' });
        ctx.globalAlpha = 1;
      }
      y += m.h + gap;
    });
    if (hasWhy) {
      const q = at(1 + vOff + off + pick.length);
      if (q > 0) {
        ctx.globalAlpha = f * q;
        rr(ctx, x0, 604, w, 86, 16); ctx.fillStyle = '#FFF8D6'; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = '#F0D25A'; ctx.stroke();
        txt(ctx, '★ ' + part.why.q, x0 + 22, 632, { size: 22, weight: 'bold', color: '#B7791F' });
        para(ctx, String(part.why.a).replace(/（[^（）]*）/g, ''), x0 + 22, 664, w - 44, { size: 21, color: C.ink, maxLines: 1 });
        ctx.globalAlpha = 1;
      }
    }
  };
  // 6.0：第三部分“同义词辨析”。上面一句：中文都说“产品”；中间每个词一张卡（词、中文意思、画、区别、字面意思），讲到哪个词哪张卡出来；
  // 下面一条：逻辑不同在哪儿（或者一句话记法）
  S.distinguish = (ctx, film, p, sc) => {
    const D = film.dist, f = fadeOf(sc, p), tl = sc.tl != null ? sc.tl : p * sc.dur;
    header(ctx, film, '同义词辨析', f, '同义词辨析');
    const items = D.items, n = items.length;
    const mk = sc.marks && sc.marks.length >= 1 ? sc.marks : null;
    const at = k => (mk && mk[k] != null ? clamp((tl - mk[k] + 0.12) / 0.45) : span(p, 0.04 + k * (0.7 / (n + 2)), 0.14 + k * (0.7 / (n + 2))));
    const q0 = at(0);
    const title = D.key ? '中文都说“' + D.key + '”，英语不一样' : '这几个词容易混';
    txt(ctx, title, W / 2, n <= 2 ? 128 : 138, { size: 40, weight: 'bold', color: C.ink, align: 'center', alpha: f * q0 });
    const hasLogic = !!(D.logic || D.tip);
    const big = n <= 2;                 // 6.25：两张卡的时候画放大（声波、走路的人看得清），“一句话”压成一行
    const gap = big ? 30 : 26, cw = Math.min(big ? 540 : 520, (W - 140 - gap * (n - 1)) / n), ch = hasLogic ? (big ? 446 : 372) : 470, y0 = big ? 162 : 172;
    let x = (W - cw * n - gap * (n - 1)) / 2;
    items.forEach((it, i) => {
      const q = easeOut(at(1 + i));
      const col = it.me ? '#D9480F' : PART[(i + 2) % PART.length];
      if (q > 0) {
        const yy = y0 + (1 - q) * 24;
        ctx.globalAlpha = f * q;
        ctx.save(); ctx.shadowColor = 'rgba(60,50,20,.10)'; ctx.shadowBlur = 18; ctx.shadowOffsetY = 5;
        rr(ctx, x, yy, cw, ch, 20); ctx.fillStyle = C.card; ctx.fill(); ctx.restore();
        ctx.globalAlpha = f * q;
        rr(ctx, x, yy, cw, ch, 20); ctx.lineWidth = it.me ? 4 : 2; ctx.strokeStyle = it.me ? col : C.line; ctx.stroke();
        rr(ctx, x, yy, cw, 10, 5); ctx.fillStyle = col; ctx.fill();
        // 画（有就放上面）
        let ty = yy + 62;
        const picH = it.pic ? (hasLogic ? (big ? 204 : 118) : 170) : 0;
        if (it.pic) { drawPic(ctx, it.pic, x + 18, yy + 22, cw - 36, picH, { q: 1, lt: Math.max(0, tl - (mk && mk[1 + i] != null ? mk[1 + i] : 0)) }); ty = yy + 22 + picH + (big ? 46 : 50); }
        const wz = fit(ctx, it.w, EN, 'bold', 52, cw - 44, 26);
        txt(ctx, it.w, x + 22, ty, { size: wz, family: EN, weight: 'bold', color: col });
        if (it.me) chip(ctx, '这个词', x + cw - 16, yy + 30, { size: 18, align: 'right', bg: col, color: '#FFFFFF' });
        if (it.gloss) { const gz = fit(ctx, it.gloss, ZH, 'bold', 30, cw - 44, 18); txt(ctx, it.gloss, x + 22, ty + 44, { size: gz, weight: 'bold', color: C.ink }); }
        let ny = ty + (it.gloss ? 84 : 44);
        ny += para(ctx, it.note, x + 22, ny, cw - 44, { size: n >= 3 ? 22 : 24, color: C.ink, maxLines: it.pic ? 2 : 4, lh: 1.42 });
        if (it.ex && ny < yy + ch - 58) { setFont(ctx, 20, EN, 'normal'); wrap(ctx, it.ex, cw - 44, 1).forEach(ln => txt(ctx, ln, x + 22, ny + 2, { size: 20, color: '#8A7B55' })); ny += 30; }
        if (it.literal && ny < yy + ch - 26) {
          const lt = '字面：' + it.literal;
          const lz = fit(ctx, lt, ZH, 'normal', 20, cw - 44, 15);
          txt(ctx, lt, x + 22, yy + ch - 22, { size: lz, color: col });
        }
        ctx.globalAlpha = 1;
      }
      x += cw + gap;
    });
    if (hasLogic) {
      const q = easeOut(at(1 + n));
      if (q > 0) {
        const bx = big ? (W - cw * n - gap * (n - 1)) / 2 : 96, bw = big ? cw * n + gap * (n - 1) : W - 192, by = y0 + ch + (big ? 16 : 22), bh = big ? Math.min(78, H - by - 18) : H - by - 28;
        ctx.globalAlpha = f * q;
        rr(ctx, bx, by, bw, bh, 18); ctx.fillStyle = '#FFF8D6'; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = '#F0D25A'; ctx.stroke();
        const tag = D.logic ? '★ 逻辑不同' : '★ 一句话', body = String(D.logic || D.tip).replace(/（[^（）]*）/g, '');
        if (big) {                       // 一行：牌子 + 这句话
          setFont(ctx, 24, ZH, 'bold'); const tw = ctx.measureText(tag).width;
          txt(ctx, tag, bx + 26, by + bh / 2 + 8, { size: 24, weight: 'bold', color: '#B7791F' });
          const bz = fit(ctx, body, ZH, 'normal', 25, bw - 78 - tw, 16);
          txt(ctx, body, bx + 26 + tw + 26, by + bh / 2 + 8, { size: bz, color: C.ink });
        } else {
          txt(ctx, tag, bx + 24, by + 36, { size: 24, weight: 'bold', color: '#B7791F' });
          para(ctx, body, bx + 24, by + 72, bw - 48, { size: 22, color: C.ink, maxLines: 3, lh: 1.4 });
        }
        ctx.globalAlpha = 1;
      }
    }
  };
  // 6.13：练习。一题一幕：上面“第 1 题 / 共 5 题”、题型牌子、右上角考的是哪一条考点；中间题目要求、听力念到第几遍（6.16 起不画喇叭，只写一行小字“第 1 遍 / 第 2 遍”）、
  // 中文、英文题干（“______”是空）、选项；想一想的时候右上角倒计时；说“答案是…”时对的选项变绿打勾、空里填上绿色的答案，下面黄条出解析。
  // 配音一句一个时间点：0 题目要求，听力念两遍（1、2），然后停 wait 秒（倒计时），再“答案是…”，最后解析
  // 喇叭：6.16 起不画了（用户：“读单词，句子的时候，喇叭不要出现，有点多余”），留着没人调
  function speakerIcon(ctx, x, y, r, col, wave, alpha) {
    ctx.save(); ctx.globalAlpha *= alpha;
    ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fillStyle = tint(col, 0.86); ctx.fill();
    ctx.lineWidth = 3; ctx.strokeStyle = tint(col, 0.5); ctx.stroke();
    const s = r / 40;
    ctx.beginPath(); ctx.moveTo(x - 22 * s, y - 9 * s); ctx.lineTo(x - 10 * s, y - 9 * s); ctx.lineTo(x + 4 * s, y - 22 * s); ctx.lineTo(x + 4 * s, y + 22 * s);
    ctx.lineTo(x - 10 * s, y + 9 * s); ctx.lineTo(x - 22 * s, y + 9 * s); ctx.closePath(); ctx.fillStyle = col; ctx.fill();
    ctx.lineCap = 'round'; ctx.strokeStyle = col;
    for (let k = 0; k < 3; k++) {
      const a = wave >= 0 ? 0.25 + 0.75 * Math.max(0, Math.sin(wave * 6 - k * 1.1)) : (k === 0 ? 0.9 : 0.35);
      ctx.globalAlpha = alpha * a; ctx.lineWidth = 4 * s + 1;
      ctx.beginPath(); ctx.arc(x + 6 * s, y, (14 + k * 9) * s, -0.75, 0.75); ctx.stroke();
    }
    ctx.restore();
  }
  // 英文题干一段一段排：空（______ / p______）画成下划线，答出来以后填上绿色的答案
  function lxStemLayout(ctx, stem, ans, size, maxW) {
    const answers = Array.isArray(ans) ? ans.slice() : [String(ans)];
    const toks = String(stem).match(/[A-Za-z]?_{3,}|\n|—|[^\s\n—]+|[ \t]+/g) || [];      // “\n”另起一行（句型转换：原句一行、要填的一行）
    setFont(ctx, size, EN, 'normal');
    const sp = ctx.measureText(' ').width, out = [];
    setFont(ctx, size, EN, 'bold');
    const bw0 = Math.max(size * 3.4, ...answers.map(x => ctx.measureText(x).width + size * 0.8));      // 空一样宽：不从长短上露出答案
    setFont(ctx, size, EN, 'normal');
    let x = 0, line = 0, bi = 0;
    toks.forEach(tk => {
      if (tk === '\n') { line++; x = 0; return; }
      if (/^\s+$/.test(tk)) { x += sp; return; }
      let w, blank = null;
      if (/_{3,}/.test(tk)) {
        const a = answers[Math.min(bi, answers.length - 1)] || ''; bi++;
        w = bw0;
        blank = { a, first: /^[A-Za-z]/.test(tk) ? tk[0] : '' };
      } else { setFont(ctx, size, /[^\x00-\x7F]/.test(tk) ? ZH : EN, 'normal'); w = ctx.measureText(tk).width; setFont(ctx, size, EN, 'normal'); }     // → 这类符号用中文字体
      if (x + w > maxW && x > 0) { line++; x = 0; }
      out.push({ tk, x, line, w, blank }); x += w;
    });
    const lines = line + 1, widths = [];
    out.forEach(o => { widths[o.line] = Math.max(widths[o.line] || 0, o.x + o.w); });
    return { out, lines, widths };
  }
  S.daan = (ctx, film, p, sc) => S.lianxi(ctx, film, p, Object.assign({}, sc, { daan: true }));      // 6.15：视频最后的“答案”
  S.lianxi = (ctx, film, p, sc) => {
    const LX = film.lx, q = LX.qs[sc.i || 0], f = fadeOf(sc, p), tl = sc.tl != null ? sc.tl : p * sc.dur;
    const col = SEC_C[5], tc = LX_TYPES[q.type] || col, nL = q.listen ? 2 : 0, A = 1 + nL;
    const mk = sc.marks && sc.marks.length ? sc.marks : null, ends = sc.ends || []; void A;
    // 时间点：有配音按每一句开始的秒数；没有（预览）按比例
    // 6.15：练习那一幕只出题（念题、听力念两遍、停 wait 秒倒计时），不出答案；答案在视频最后“答案”那一部分（S.daan 也走这里，sc.daan = true）：
    // 一开始就是做完的样子（对的选项变绿、空里填上答案），配音“第一题，答案是 D …”，第二句讲解时下面黄条出来
    const isAns = !!sc.daan;
    const T = isAns
      ? (() => { const m = sc.marks || []; return { ask: -1, l0: -1, l1: -1, w0: -1, ans: -1, why: m[1] != null ? m[1] : 0.35 * sc.dur, end: Infinity }; })()
      : (() => {
          const m = sc.marks || [], e = sc.ends || [];
          if (m.length > nL) { const w0 = e[nL] != null ? e[nL] : sc.dur - q.wait - 0.7; return { ask: m[0], l0: nL ? m[1] : 0, l1: nL ? e[nL] : 0, w0, ans: w0 + q.wait, why: Infinity }; }
          const D = sc.dur, w0 = D - q.wait - 0.7; return { ask: 0.05 * D, l0: 0.12 * D, l1: q.listen ? w0 : 0, w0, ans: w0 + q.wait, why: Infinity };
        })();
    const on = t0 => clamp((tl - t0 + 0.1) / 0.45), shown = isAns ? 1 : 0, whyQ = isAns ? easeOut(on(T.why)) : 0;
    // 头：第几题、题型、考点
    const hq = easeOut(clamp(tl / 0.5));
    txt(ctx, '第 ' + ((sc.i || 0) + 1) + ' 题' + (isAns ? '' : ''), 80, 82, { size: 40, weight: 'bold', color: col, alpha: f * hq });
    setFont(ctx, 40, ZH, 'bold'); const hx = 80 + ctx.measureText('第 ' + ((sc.i || 0) + 1) + ' 题').width + 18;
    txt(ctx, '/ 共 ' + LX.qs.length + ' 题', hx, 82, { size: 24, color: C.faint, alpha: f * hq });
    setFont(ctx, 24, ZH, 'normal'); let px = hx + ctx.measureText('/ 共 ' + LX.qs.length + ' 题').width + 22;
    setFont(ctx, 26, ZH, 'bold'); const tw = ctx.measureText(q.type).width + 34;
    ctx.globalAlpha = f * hq; rr(ctx, px, 50, tw, 44, 22); ctx.fillStyle = tint(tc, 0.85); ctx.fill(); ctx.globalAlpha = 1;
    txt(ctx, q.type, px + tw / 2, 73, { size: 26, weight: 'bold', color: tc, align: 'center', base: 'middle', alpha: f * hq });
    void px;                                                                 // 6.16：题型牌子“听力”旁边不画小喇叭
    // 右上：倒计时（想一想），答出来以后换成考点牌子
    const wq = q.wait > 0 && tl >= T.w0 && tl < T.ans ? clamp((tl - T.w0) / Math.max(0.5, T.ans - T.w0)) : -1;
    if (isAns) {
      setFont(ctx, 26, ZH, 'bold'); const aw = ctx.measureText('答案').width + 36;
      ctx.globalAlpha = f * hq; rr(ctx, W - 80 - aw, 50, aw, 44, 22); ctx.fillStyle = C.green; ctx.fill(); ctx.globalAlpha = 1;
      txt(ctx, '答案', W - 80 - aw / 2, 73, { size: 26, weight: 'bold', color: '#fff', align: 'center', base: 'middle', alpha: f * hq });
    } else if (wq >= 0) {
      const cx = W - 118, cy = 72, R = 30, left = Math.max(1, Math.ceil((T.ans - tl) - 0.05));
      ctx.save(); ctx.globalAlpha = f;
      ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2); ctx.fillStyle = C.card; ctx.fill(); ctx.lineWidth = 6; ctx.strokeStyle = C.line; ctx.stroke();
      ctx.beginPath(); ctx.arc(cx, cy, R, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * (1 - wq)); ctx.strokeStyle = tc; ctx.lineCap = 'round'; ctx.stroke();
      ctx.restore();
      txt(ctx, String(left), cx, cy + 2, { size: 30, weight: 'bold', family: EN, color: tc, align: 'center', base: 'middle', alpha: f });
      txt(ctx, '想一想', cx - R - 14, cy + 2, { size: 24, color: C.soft, align: 'right', base: 'middle', alpha: f });
    } else if (q.kd) {
      const lab = '考点：' + q.kd; setFont(ctx, 24, ZH, 'bold'); const kw = ctx.measureText(lab).width + 30, kc = KD_C[q.kd] || SEC_C[4];
      const kq = f * hq;
      ctx.globalAlpha = kq; rr(ctx, W - 80 - kw, 52, kw, 40, 20); ctx.fillStyle = tint(kc, 0.88); ctx.fill(); ctx.lineWidth = 1.5; ctx.strokeStyle = tint(kc, 0.55); ctx.stroke(); ctx.globalAlpha = 1;
      txt(ctx, lab, W - 80 - kw / 2, 73, { size: 24, weight: 'bold', color: kc, align: 'center', base: 'middle', alpha: kq });
    }
    // 中间：先量高度，再上下居中
    const X0 = 100, MW = W - 200, TOP = 120, BOT = isAns && q.why ? 586 : 660;      // 出题那一幕没有讲解条，题目放在中间
    const askQ = easeOut(on(T.ask));
    setFont(ctx, 32, ZH, 'normal'); const askL = wrap(ctx, q.ask, MW, 2);
    const listenH = q.listen ? (isAns ? (q.opts.length ? 60 : 0) : 44) : 0;      // 6.16：没有喇叭了——出题时一行小字“第 1 遍 / 第 2 遍”，答案页写听到的那句英文
    setFont(ctx, 38, ZH, 'bold'); const zhL = q.zh ? wrap(ctx, q.zh, MW, 2) : [];
    let sz = 52, st = null;
    const hasStem = !!q.stem, transAns = !q.opts.length && !/_{3,}/.test(q.stem);     // 汉译英整句、改错：题干里没有空，下面一条横线写答案
    if (hasStem) { do { st = lxStemLayout(ctx, q.stem, q.opts.length ? String(q.opts[LETTERS.indexOf(q.ans)] || '').split(/\s*;\s*/) : q.ans, sz, MW); if (st.lines <= 2) break; sz -= 3; } while (sz > 30); }
    // 选项：短的一行四个，长一点的两行两个，再长的一行一个
    let optLay = null;
    if (q.opts.length) {
      setFont(ctx, 36, EN, 'normal');
      const ow = Math.max(...q.opts.map(o => ctx.measureText(o).width)) + 100;
      const perRow = ow * q.opts.length + 24 * (q.opts.length - 1) <= MW ? q.opts.length : ow * 2 + 24 <= MW ? 2 : 1;
      const bw = perRow === q.opts.length ? Math.max(ow, Math.min(300, (MW - 24 * (perRow - 1)) / perRow)) : (MW - 24 * (perRow - 1)) / perRow;
      const rows = Math.ceil(q.opts.length / perRow), bh = 80;
      optLay = { perRow, bw, bh, rows, h: rows * bh + (rows - 1) * 18 };
    }
    const gapA = 26, H_ask = askL.length * 44, H_zh = zhL.length * 52, H_stem = st ? st.lines * sz * 1.7 : 0, H_tr = transAns ? 70 : 0;
    const parts = [H_ask, listenH, H_zh, H_stem, H_tr, optLay ? optLay.h : 0].filter(Boolean);
    const total = parts.reduce((a, b) => a + b, 0) + gapA * (parts.length - 1);
    let y = TOP + Math.max(0, (BOT - TOP - total) / 2);
    askL.forEach((ln, k) => txt(ctx, ln, W / 2, y + 32 + k * 44, { size: 32, color: C.soft, align: 'center', alpha: f * askQ }));
    y += H_ask + gapA;
    if (q.listen && listenH) {                                               // 6.16：中间不画喇叭（用户：“读单词，句子的时候，喇叭不要出现，有点多余”）
      const playing = tl >= T.l0 && tl < T.l1 ? (tl - T.l0) : -1;
      const times = playing >= 0 ? (mk && nL > 1 && mk[2] != null && tl >= mk[2] ? '第 2 遍' : '第 1 遍') : (tl >= T.l1 && shown <= 0 ? '听了两遍' : '');
      if (times) txt(ctx, times, W / 2, y + 31, { size: 26, color: C.soft, align: 'center', alpha: f });
      if (shown > 0 && q.opts.length) { const z = fit(ctx, q.listen, EN, 'bold', 36, MW, 22); txt(ctx, q.listen, W / 2, y + 42, { size: z, family: EN, weight: 'bold', color: tc, align: 'center', alpha: f * shown }); }     // 答案页：把听到的写出来
      y += listenH + gapA;
    }
    if (zhL.length) { zhL.forEach((ln, k) => txt(ctx, ln, W / 2, y + 40 + k * 52, { size: 38, weight: 'bold', color: C.ink, align: 'center', alpha: f * askQ })); y += H_zh + gapA; }
    if (st) {
      const lh = sz * 1.7;
      st.out.forEach(o => {
        const x = (W - st.widths[o.line]) / 2 + o.x, by = y + sz * 1.15 + o.line * lh;
        if (o.blank) {
          ctx.globalAlpha = f * askQ; ctx.fillStyle = C.ink; ctx.fillRect(x + 4, by + 8, o.w - 8, 3); ctx.globalAlpha = 1;
          if (shown > 0 && o.blank.a) {
            ctx.globalAlpha = f * shown * 0.9; rr(ctx, x + 2, by - sz * 0.95, o.w - 4, sz * 1.25, 10); ctx.fillStyle = tint(C.green, 0.86); ctx.fill(); ctx.globalAlpha = 1;
            txt(ctx, o.blank.a, x + o.w / 2, by, { size: sz, family: EN, weight: 'bold', color: C.green, align: 'center', alpha: f * shown });
          } else if (o.blank.first) txt(ctx, o.blank.first, x + 10, by, { size: sz, family: EN, weight: 'bold', color: C.ink, alpha: f * askQ });
        } else txt(ctx, o.tk, x, by, { size: sz, family: /[^\x00-\x7F]/.test(o.tk) ? ZH : EN, color: C.ink, alpha: f * askQ });
      });
      y += H_stem + gapA;
    }
    if (transAns) {
      ctx.globalAlpha = f * askQ; ctx.fillStyle = C.ink; ctx.fillRect(X0 + 40, y + 52, MW - 80, 3); ctx.globalAlpha = 1;
      if (shown > 0) txt(ctx, Array.isArray(q.ans) ? q.ans.join(' ') : q.ans, W / 2, y + 40, { size: fit(ctx, String(q.ans), EN, 'bold', 40, MW - 100, 24), family: /→/.test(String(q.ans)) ? ZH : EN, weight: 'bold', color: C.green, align: 'center', alpha: f * shown });
      y += H_tr + gapA;
    }
    if (optLay) {
      const { perRow, bw, bh } = optLay, rowsW = bw * perRow + 24 * (perRow - 1), ok = LETTERS.indexOf(q.ans);
      q.opts.forEach((o, k) => {
        const r = Math.floor(k / perRow), c = k % perRow, x = (W - rowsW) / 2 + c * (bw + 24), yy = y + r * (bh + 18);
        const oq = easeOut(on(T.ask + 0.3 + k * 0.12)), right = k === ok;
        const dim = shown > 0 && !right ? 1 - 0.55 * shown : 1;
        ctx.save(); ctx.globalAlpha = f * oq * dim;
        ctx.shadowColor = 'rgba(60,50,20,.08)'; ctx.shadowBlur = 10; ctx.shadowOffsetY = 3;
        rr(ctx, x, yy, bw, bh, 16); ctx.fillStyle = right && shown > 0 ? tint(C.green, 0.88 - 0.0 * shown) : C.card; ctx.fill(); ctx.restore();
        ctx.save(); ctx.globalAlpha = f * oq * dim; rr(ctx, x, yy, bw, bh, 16); ctx.lineWidth = right && shown > 0 ? 3 : 2; ctx.strokeStyle = right && shown > 0 ? C.green : C.line; ctx.stroke();
        ctx.beginPath(); ctx.arc(x + 36, yy + bh / 2, 22, 0, Math.PI * 2); ctx.fillStyle = right && shown > 0 ? C.green : tint(tc, 0.85); ctx.fill(); ctx.restore();
        txt(ctx, LETTERS[k], x + 36, yy + bh / 2 + 1, { size: 26, weight: 'bold', family: EN, color: right && shown > 0 ? '#fff' : tc, align: 'center', base: 'middle', alpha: f * oq * dim });
        const fam = hasCjk(o) ? ZH : EN, oz = fit(ctx, o, fam, 'normal', 36, bw - 100, 18);
        txt(ctx, o, x + 72, yy + bh / 2 + 1, { size: oz, family: fam, color: C.ink, base: 'middle', alpha: f * oq * dim });
        if (right && shown > 0) {                                                 // 右上角绿色的勾
          ctx.save(); ctx.globalAlpha = f * shown; ctx.beginPath(); ctx.arc(x + bw - 4, yy + 4, 17, 0, Math.PI * 2); ctx.fillStyle = C.green; ctx.fill(); ctx.restore();
          txt(ctx, '✓', x + bw - 4, yy + 5, { size: 22, weight: 'bold', color: '#fff', align: 'center', base: 'middle', alpha: f * shown });
        }
      });
    }
    // 下面：解析
    if (q.why && whyQ > 0) {
      setFont(ctx, 28, ZH, 'normal'); const wl = wrap(ctx, q.why, W - 160 - 130, 2), hh = 30 + wl.length * 40;
      const yy = H - 34 - hh + (1 - whyQ) * 14;
      ctx.globalAlpha = f * whyQ; rr(ctx, 80, yy, W - 160, hh, 16); ctx.fillStyle = '#FFF6D6'; ctx.fill(); ctx.lineWidth = 1.5; ctx.strokeStyle = '#EED48A'; ctx.stroke();
      rr(ctx, 98, yy + hh / 2 - 19, 82, 38, 19); ctx.fillStyle = '#B8860B'; ctx.fill(); ctx.globalAlpha = 1;
      txt(ctx, '讲解', 139, yy + hh / 2 + 1, { size: 22, weight: 'bold', color: '#fff', align: 'center', base: 'middle', alpha: f * whyQ });
      wl.forEach((ln, k) => txt(ctx, ln, 200, yy + 15 + 29 + k * 40 - (wl.length > 1 ? 0 : 0), { size: 28, color: C.ink, alpha: f * whyQ }));
    }
  };
  // 6.11：考点。上面“考点”两个字，下面一行一张横条：左边牌子（变形 / 词性转换 / 短语 / 用法 / 易混），右边内容；
  // 词性转换画成一个个小块（n. product 产品；考纲外的词是“true → truly（去 e 加 ly，易错）”一块），别的一条一行（放不下折行）。
  // 说到哪一行出哪一行；6.12 起行少字大（1 行 40 号、2 行 36、3 行 32、更多 28），放不下再往小试（最小 17 号）
  S.kaodian = (ctx, film, p, sc) => {
    const K = film.kd, f = fadeOf(sc, p), tl = sc.tl != null ? sc.tl : p * sc.dur;
    const multi = K.pages && K.pages.length > 1 && sc.i != null;               // 6.31：分两页时只画这一页的几行
    const rows = multi ? K.pages[sc.i].map(k => K.rows[k]) : K.rows, n = rows.length, col = SEC_C[4];
    const mk = sc.marks && sc.marks.length >= 1 ? sc.marks : null;
    const at = k => (mk && mk[k] != null ? clamp((tl - mk[k] + 0.12) / 0.45) : span(p, 0.04 + k * (0.8 / (n + 1)), 0.12 + k * (0.8 / (n + 1))));
    const X0 = 80, X1 = W - 80, LW = 156, TX = X0 + LW + 24, TW = X1 - TX - 24, TOP = 118, BOT = H - 24, GAP = 12, PAD = 13;
    const layout = size => {
      const lh = size * 1.42, ch = size * 1.85, out = [];
      let total = 0;
      rows.forEach(r => {
        if (r.label === '词性转换' || r.label === '变形') {
          setFont(ctx, size, ZH, 'bold');
          const chips = [];
          let x = 0, line = 0;
          // 变形：每个词性一组，按“；”切成小块（v. 过去式、过去分词 produced（去 e 加 d）｜现在分词 producing（去 e 加 ing）｜三单 produces），每个词性另起一行
          const its = r.label === '变形' ? [].concat(...r.items.map((it, k) => splitTop(it, '；').map((seg, j) => ({ t: String(seg).trim(), br: k > 0 && j === 0 })))) : r.items.map(t => ({ t, br: false }));
          its.forEach(({ t: it, br }) => {
            if (br && x > 0) { line++; x = 0; }
            const w = Math.min(TW, ctx.measureText(it).width + size * 1.2);
            if (x + w > TW && x > 0) { line++; x = 0; }
            chips.push({ it, x, line, w }); x += w + size * 0.6;
          });
          const h = (line + 1) * ch + PAD * 2 - (ch - size * 1.6);
          out.push({ r, chips, h }); total += h;
        } else {
          setFont(ctx, size, ZH, 'normal');
          const lines = [], multi = r.items.length > 1;
          // 6.33：几条的用 ①②③ 编号（用户：“用了分行符号：点 ； 这个可以换成数字序号”），例句另起一行写“例：…”
          r.items.forEach((it, k) => {
            const [pt, ex] = kdEx(it);
            wrap(ctx, pt, TW - size * 1.35, 2).forEach((t, j) => lines.push({ t, first: j === 0, num: multi && j === 0 ? KD_NUM[k] : '' }));
            if (ex) wrap(ctx, '例：' + ex, TW - size * 1.35, 2).forEach(t => lines.push({ t, ex: true }));
          });
          const h = lines.length * lh + PAD * 2 - (lh - size) * 0.4;
          out.push({ r, lines, h }); total += h;
        }
      });
      return { out, lh, ch, total: total + GAP * (rows.length - 1) };
    };
    // 6.12：考点只写常考的（总表“考纲考点版”），一两行的词居多——行少字就大（1 行 40 号、2 行 36、3 行 32，再多从 28 起），放不下再往小试
    let size = n <= 1 ? 40 : n === 2 ? 36 : n === 3 ? 32 : 28, lay = layout(size);
    while (size > 17 && lay.total > BOT - TOP) { size -= 1; lay = layout(size); }
    if (film._dbg) film._dbg.push(['kaodian', size, Math.round(lay.total), BOT - TOP]);
    // 6.27.2（用户：“做的视频要尽量上下居中”）：标题“考点”跟着下面的几行一起上下居中，行少的时候不再一个在最上面、一个在中间
    const groupTop = Math.max(TOP - 72, (H - lay.total - 72) / 2);
    let y = Math.max(TOP, groupTop + 72);
    txt(ctx, multi ? '考点 ' + (sc.i + 1) + '/' + K.pages.length : '考点', W / 2, y - 28, { size: 46, weight: 'bold', color: col, align: 'center', alpha: f * at(0) });
    lay.out.forEach((R, i) => {
      const q = easeOut(at(1 + i)), c = KD_C[R.r.label] || col, h = R.h;
      if (q > 0) {
        const yy = y + (1 - q) * 18;
        ctx.globalAlpha = f * q;
        ctx.save(); ctx.shadowColor = 'rgba(60,50,20,.08)'; ctx.shadowBlur = 12; ctx.shadowOffsetY = 3;
        rr(ctx, X0, yy, X1 - X0, h, 16); ctx.fillStyle = C.card; ctx.fill(); ctx.restore();
        ctx.globalAlpha = f * q;
        rr(ctx, X0, yy, X1 - X0, h, 16); ctx.lineWidth = 2; ctx.strokeStyle = C.line; ctx.stroke();
        rr(ctx, X0, yy, LW, h, 16); ctx.fillStyle = tint(c, 0.86); ctx.fill();
        const lz = fit(ctx, R.r.label, ZH, 'bold', Math.min(36, size + 6), LW - 20, 16);
        txt(ctx, R.r.label, X0 + LW / 2, yy + h / 2 + 1, { size: lz, weight: 'bold', color: c, align: 'center', base: 'middle' });
        if (R.chips) {
          R.chips.forEach(cp => {
            const cy = yy + PAD + cp.line * lay.ch + size * 0.8;
            rr(ctx, TX + cp.x, cy - size * 0.8, cp.w, size * 1.6, size * 0.8); ctx.fillStyle = tint(c, 0.9); ctx.fill();
            ctx.lineWidth = 1.5; ctx.strokeStyle = tint(c, 0.6); ctx.stroke();
            setFont(ctx, size, ZH, 'bold');
            let t = cp.it; while (t.length > 1 && ctx.measureText(t).width > cp.w - size * 0.8) t = t.slice(0, -1);
            txt(ctx, t, TX + cp.x + cp.w / 2, cy + 1, { size, weight: 'bold', color: C.ink, align: 'center', base: 'middle' });
          });
        } else {
          R.lines.forEach((ln, j) => {
            const ty = yy + PAD + lay.lh * j + size * 0.98;
            if (ln.num) txt(ctx, ln.num, TX + size * 0.05, ty, { size, weight: 'bold', color: c });
            else if (ln.first) { ctx.beginPath(); ctx.arc(TX + size * 0.3, ty - size * 0.34, Math.max(3, size * 0.15), 0, Math.PI * 2); ctx.fillStyle = c; ctx.fill(); }
            txt(ctx, ln.t, TX + size * 1.2, ty, ln.ex ? { size: size * 0.95, color: '#4A6A86' } : { size, color: C.ink });
          });
        }
        ctx.globalAlpha = 1;
      }
      y += h + GAP;
    });
  };
  S.route = (ctx, film, p, sc) => {
    const f = fadeOf(sc, p);
    header(ctx, film, '来历', f);
    routeScene(ctx, film, p, f, sc);
  };
  // 3.5 起：照【字母变化】链一步步变字母。先看第一个形式 1 秒（源头词根的字母标蓝），每一步 1.6 秒：
  // 要掉的字母先标红、划掉，再往上飘走；新来的字母绿色从上面落下；上面的小牌子换成这一步的语言，下面的链亮到这一步；
  // 最后 1.6 秒写“词根 popul（人民、民众）→ people”。基准时长 2.6 + 1.6 × 步数（和 build 里一样；配音长了整体放慢）
  function variantChain(ctx, film, p, sc, f, chain, lastLine) {
    const v = film.variant, ch = chain || v.chain, n = ch.steps.length;
    const T0 = 1.0, D = 1.6, T = T0 + D * n + 1.6, t = p * T;
    const k = Math.max(0, Math.min(n, Math.floor((t - T0) / D) + 1));          // 第 k 步已经开始；0：还在第一个形式上
    const loc = k === 0 ? 0 : clamp((t - T0 - (k - 1) * D) / D);
    let ops, a = 0, b = 0, c = 0;
    if (k === 0) ops = ch.forms[0].text.split('').map((x, i) => ({ ch: x, op: 'keep', r: !!ch.flags0[i] }));
    else { ops = ch.steps[k - 1].ops; a = span(loc, 0, 0.3); b = easeInOut(span(loc, 0.3, 0.8)); c = span(loc, 0.8, 1); }
    // 大字：几个形式里最长的那个也放得下
    const longest = ch.forms.reduce((s, x) => (x.text.length > s.length ? x.text : s), '');
    const size = fit(ctx, longest, EN, 'bold', 124, W - 260, 50);
    setFont(ctx, size, EN, 'bold');
    const y = 370;
    const ws = ops.map(o => ctx.measureText(o.ch).width);
    const cur = ops.map((o, i) => (o.op === 'keep' ? ws[i] : o.op === 'del' ? ws[i] * (1 - b) : ws[i] * b));
    let x = (W - cur.reduce((s, w) => s + w, 0)) / 2;
    ops.forEach((o, i) => {
      let color = o.r ? PART[0] : C.ink, alpha = 1, lift = 0;
      if (o.op === 'del') { if (a > 0.05) color = C.red; alpha = 1 - b; lift = -46 * b; }
      else if (o.op === 'ins') { color = c > 0.6 ? C.ink : C.green; alpha = b; lift = -46 * (1 - b); }
      if (cur[i] > 0.5 && alpha > 0.02) {
        ctx.save();
        ctx.translate(x + cur[i] / 2, y + lift);
        ctx.scale(Math.max(0.05, cur[i] / ws[i]), 1);
        txt(ctx, o.ch, 0, 0, { size, family: EN, weight: 'bold', color, align: 'center', alpha: alpha * f });
        if (o.op === 'del' && a > 0) {
          ctx.strokeStyle = C.red; ctx.lineWidth = 6; ctx.globalAlpha = f * Math.min(a, 1 - b);
          ctx.beginPath(); ctx.moveTo(-ws[i] / 2, -size * 0.32); ctx.lineTo(ws[i] / 2, -size * 0.32); ctx.stroke(); ctx.globalAlpha = 1;
        }
        ctx.restore();
      }
      x += cur[i];
    });
    // 上面的小牌子：这一步在哪种语言里（推出来的形式另写一句）
    const tagOf = j => ch.forms[j].lang + (ch.forms[j].guess ? ' · 推出来的形式' : '');
    const tag = (s, al) => {
      if (al <= 0.01) return;
      setFont(ctx, 28, ZH, 'bold');
      const w = ctx.measureText(s).width + 40;
      ctx.globalAlpha = f * al; rr(ctx, (W - w) / 2, 178, w, 50, 25); ctx.fillStyle = C.warm; ctx.fill(); ctx.globalAlpha = 1;
      txt(ctx, s, W / 2, 213, { size: 28, weight: 'bold', color: C.soft, align: 'center', alpha: f * al });
    };
    if (k === 0) tag(tagOf(0), span(t, 0.1, 0.4)); else { tag(tagOf(k - 1), 1 - b); tag(tagOf(k), b); }
    // 下面的链：走过的灰、这一步的黑（黄底）、还没到的浅；每个形式下面小字写语言
    const cz = 30, gap = 22;
    const items = ch.forms.map(fm => {
      const s = (fm.guess ? '*' : '') + fm.text;
      setFont(ctx, cz, EN, 'bold'); const tw = ctx.measureText(s).width;
      setFont(ctx, 18, ZH); const lw = ctx.measureText(fm.lang).width;
      return { s, tw, w: Math.max(tw, lw) };
    });
    setFont(ctx, cz, ZH, 'bold'); const aw = ctx.measureText('→').width + gap * 2;
    const total = items.reduce((s, it) => s + it.w, 0) + aw * (items.length - 1);
    const sx = Math.min(1, (W - 120) / total);
    const now = k === 0 ? 0 : (b >= 0.5 ? k : k - 1);
    const ya = f * span(t, 0.2, 0.6);
    ctx.save(); ctx.translate((W - total * sx) / 2, 0); ctx.scale(sx, 1);
    let xx = 0;
    items.forEach((it, j) => {
      const col = j < now ? C.soft : j === now ? C.ink : C.faint;
      if (j === now) { ctx.globalAlpha = ya * 0.9; rr(ctx, xx + (it.w - it.tw) / 2 - 8, 488 - cz * 0.82, it.tw + 16, cz * 1.15, 8); ctx.fillStyle = '#FFF0A0'; ctx.fill(); ctx.globalAlpha = 1; }
      txt(ctx, it.s, xx + it.w / 2, 488, { size: cz, family: EN, weight: 'bold', color: col, align: 'center', alpha: ya });
      txt(ctx, ch.forms[j].lang, xx + it.w / 2, 520, { size: 18, color: j === now ? C.soft : C.faint, align: 'center', alpha: ya });
      xx += it.w;
      if (j < items.length - 1) { txt(ctx, '→', xx + aw / 2, 486, { size: cz, family: ZH, weight: 'bold', color: C.faint, align: 'center', alpha: ya }); xx += aw; }
    });
    ctx.restore();
    // 最后：源头词根和它的意思
    const q = span(t, T0 + D * n + 0.1, T0 + D * n + 0.6);
    if (q > 0) line(ctx, lastLine || (v.root ? [['词根 ', C.faint, false, ZH]] : []).concat([[v.from.replace(/[()]/g, ''), PART[0]]])
      .concat(v.root && v.root.gloss ? [['（' + v.root.gloss + '）', C.soft, false, ZH]] : []).concat([['  →  ', C.faint], [v.to, C.ink]]), 610, 34, f * q);
  }
  S.variant = (ctx, film, p, sc) => {
    const f = fadeOf(sc, p);
    header(ctx, film, '怎么变来的', f);
    if (film.variant.chain) return variantChain(ctx, film, p, sc, f);   // 3.5 起：照字母变化链一步步变
    const v = film.variant, ops = v.ops;
    const k = easeInOut(span(p, 0.3, 0.7));
    const size = fit(ctx, v.from.replace(/[()]/g, ''), EN, 'bold', 130, W - 240, 50);
    setFont(ctx, size, EN, 'bold');
    const ws = ops.map(o => ctx.measureText(o.ch).width);
    const cur = ops.map((o, i) => (o.op === 'keep' ? ws[i] : o.op === 'del' ? ws[i] * (1 - k) : ws[i] * k));
    let x = (W - cur.reduce((s, w) => s + w, 0)) / 2;
    const y = 360;
    ops.forEach((o, i) => {
      const color = o.op === 'del' ? C.red : o.op === 'ins' ? C.green : C.ink;
      const alpha = o.op === 'del' ? 1 - k : o.op === 'ins' ? k : 1;
      const lift = o.op === 'del' ? k * 40 : o.op === 'ins' ? (1 - k) * -40 : 0;
      if (cur[i] > 0.5 && alpha > 0.02) {
        ctx.save();
        ctx.translate(x + cur[i] / 2, y + lift);
        ctx.scale(Math.max(0.05, cur[i] / ws[i]), 1);
        txt(ctx, o.ch, 0, 0, { size, family: EN, weight: 'bold', color: p < 0.3 && o.op === 'del' ? C.red : color, align: 'center', alpha: alpha * f });
        if (o.op === 'del' && p < 0.3) { ctx.strokeStyle = C.red; ctx.lineWidth = 6; ctx.globalAlpha = f * span(p, 0.12, 0.25); ctx.beginPath(); ctx.moveTo(-ws[i] / 2, -size * 0.32); ctx.lineTo(ws[i] / 2, -size * 0.32); ctx.stroke(); ctx.globalAlpha = 1; }
        ctx.restore();
      }
      x += cur[i];
    });
    const q = span(p, 0.72, 0.88);
    line(ctx, [[v.from.replace(/[()]/g, ''), C.soft]].concat(v.root && v.root.gloss ? [['（' + v.root.gloss + '）', C.faint, false, ZH]] : []).concat([['  →  ', C.faint], [v.to, C.soft]]), 470, 34, f * q);
    if (film.origin && film.origin.text) {
      ctx.globalAlpha = f * span(p, 0.15, 0.3);
      setFont(ctx, 30, ZH);
      const lines = wrap(ctx, film.origin.text, W - 320, 2);
      lines.forEach((ln, i) => txt(ctx, ln, W / 2, 560 + i * 44, { size: 30, color: C.ink, align: 'center' }));
      ctx.globalAlpha = 1;
    }
  };
  S.related = (ctx, film, p, sc) => {
    const f = fadeOf(sc, p);
    header(ctx, film, '和谁是一家', f);
    // 3.6 起：有字母变化链的，照链一步步变，最后写“rail ≈ rule（同一个来源）”
    if (film.relChain) {
      const segs = [];
      film.related.forEach((s, i) => { if (i) segs.push(['  ≈  ', C.faint]); segs.push([s, i ? PART[0] : C.ink]); });
      segs.push(['（同一个来源）', C.soft, false, ZH]);
      return variantChain(ctx, film, p, sc, f, film.relChain, segs);
    }
    const items = film.related;
    const size = 92;
    setFont(ctx, size, EN, 'bold');
    const ws = items.map(s => ctx.measureText(s).width);
    const gap = 110;
    let x = (W - ws.reduce((s, w) => s + w, 0) - gap * (items.length - 1)) / 2;
    items.forEach((s, i) => {
      const q = easeBack(span(p, 0.08 + i * 0.18, 0.28 + i * 0.18));
      txt(ctx, s, x + ws[i] / 2, 330, { size: size * Math.max(0.01, q), family: EN, weight: 'bold', color: i === 0 ? C.ink : PART[0], align: 'center', alpha: f * Math.min(1, q) });
      x += ws[i];
      if (i < items.length - 1) { txt(ctx, '≈', x + gap / 2, 300, { size: 70, family: ZH, weight: 'bold', color: C.faint, align: 'center', base: 'middle', alpha: f * span(p, 0.2 + i * 0.18, 0.35 + i * 0.18) }); x += gap; }
    });
    txt(ctx, '意思、来历有关系（同源）', W / 2, 430, { size: 30, color: C.soft, align: 'center', alpha: f * span(p, 0.45, 0.6) });
    if (film.origin && film.origin.text) {
      ctx.globalAlpha = f * span(p, 0.55, 0.7);
      setFont(ctx, 30, ZH);
      wrap(ctx, film.origin.text, W - 320, 2).forEach((ln, i) => txt(ctx, ln, W / 2, 530 + i * 44, { size: 30, color: C.ink, align: 'center' }));
      ctx.globalAlpha = 1;
    }
  };
  S.origin = (ctx, film, p, sc) => {
    const f = fadeOf(sc, p), tl = sc.tl != null ? sc.tl : p * sc.dur;
    const o = film.origin || {};
    const size = fit(ctx, film.word, EN, 'bold', o.pic ? 100 : 120, W - 240, 50);
    txt(ctx, film.word, W / 2, o.pic ? 196 : 230, { size, family: EN, weight: 'bold', color: C.ink, align: 'center', alpha: f });
    const x0 = o.pic ? 100 : 150, y0 = o.pic ? 240 : 300, w = W - x0 * 2, h = o.pic ? 400 : 320;
    const up = (1 - easeOut(span(p, 0.05, 0.25))) * 30;
    ctx.globalAlpha = f * span(p, 0.05, 0.2);
    rr(ctx, x0, y0 + up, w, h, 22); ctx.fillStyle = C.card; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = C.line; ctx.stroke();
    rr(ctx, x0, y0 + up, 12, h, 6); ctx.fillStyle = C.board; ctx.fill();
    let tx = x0 + 60;
    if (o.pic) {                                        // 5.0 起：画的就是来历里说的那样东西（camera：拱顶的屋子）
      const pw = 540, ph = h - 44, q = easeOut(span(p, 0.1, 0.3));
      ctx.globalAlpha = f * q;
      drawPic(ctx, o.pic, x0 + 30, y0 + up + 22, pw, ph, { q, lt: tl - 0.35 });
      tx = x0 + 30 + pw + 40;
    } else if (o.icon) {
      const q = easeBack(span(p, 0.15, 0.4));
      ctx.globalAlpha = f * span(p, 0.05, 0.2);
      if (q > 0) emoji(ctx, o.icon, x0 + 180, y0 + up + h / 2, 150 * q);
      tx = x0 + 380;
    }
    ctx.globalAlpha = f * span(p, 0.05, 0.2);
    txt(ctx, '来历', tx, y0 + up + 70, { size: 28, weight: 'bold', color: '#8A6A2A' });
    ctx.globalAlpha = f * span(p, 0.2, 0.4);
    para(ctx, o.text || '', tx, y0 + up + 125, x0 + w - tx - 36, { size: o.pic ? 32 : 34, color: C.ink, maxLines: o.pic ? 6 : 4, lh: 1.5 });
    ctx.globalAlpha = 1;
  };
  S.steps = (ctx, film, p, sc) => {
    const f = fadeOf(sc, p);
    header(ctx, film, '意思一步步变过来', f);
    const steps = film.steps, n = steps.length, ts = sc.marks ? sc.tl : p * sc.dur * film.pace;       // 这一幕的第几秒（不算快慢）
    const lit = (film.combo && film.combo.literal) || (film.origin && film.origin.literal) || '';
    let y = 150;
    if (lit) {
      const q = span(ts, 0.1, 0.5);
      setFont(ctx, 34, ZH, 'bold');
      const s = '“' + lit + '”', w = Math.min(ctx.measureText(s).width, W - 260);
      ctx.globalAlpha = f * q;
      rr(ctx, 96, y + 6, w + 36, 58, 12); ctx.fillStyle = '#FFF4B8'; ctx.fill();
      txt(ctx, s, 114, y + 47, { size: 34, weight: 'bold', color: C.ink });
      ctx.globalAlpha = 1;
      y += 84;
    }
    const rowH = Math.min(118, (H - y - 40) / Math.max(1, n));
    steps.forEach((st, i) => {
      const at = sc.marks && sc.marks[i] != null ? sc.marks[i] : 1.0 + i * 2.0;
      const q = easeOut(span(ts, at, at + 0.45));
      if (q <= 0) return;
      const yy = y + i * rowH + (1 - q) * 20;
      ctx.globalAlpha = f * q;
      txt(ctx, '→', 112, yy + 44, { size: 38, weight: 'bold', color: '#B69D62' });
      const tx = 170, tw = W - 260;
      if (st.text) {
        setFont(ctx, 28, ZH);
        const a = wrap(ctx, st.text, tw, 1)[0] || '';
        txt(ctx, a, tx, yy + 30, { size: 28, color: C.soft });
        const r = fitLine(ctx, st.result, ZH, 'bold', 36, tw, 26);
        txt(ctx, r.t, tx, yy + 76, { size: r.z, weight: 'bold', color: C.green });
      } else {
        const r = fitLine(ctx, st.result, ZH, 'bold', 36, tw, 26);
        txt(ctx, r.t, tx, yy + 46, { size: r.z, weight: 'bold', color: C.green });
      }
      ctx.globalAlpha = 1;
    });
  };
  S.meaning = (ctx, film, p, sc) => {
    const pics = film.pics || [];
    if (!pics.length) return meaningPlain(ctx, film, p, sc);
    const f = fadeOf(sc, p), n = pics.length, tl = sc.tl != null ? sc.tl : p * sc.dur;
    const hasEvo = !film.flow && pics.some(pc => pc.evo && pc.evo.length);
    const lit = (film.combo && film.combo.literal) || '';
    if (hasEvo && n > 1) {
      header(ctx, film, '', f);
      const s0 = lit ? '“' + lit + '”' : film.word, q0 = easeOut(clamp(tl / 0.4));
      setFont(ctx, 32, lit ? ZH : EN, 'bold');
      const bw0 = ctx.measureText(s0).width + 48;
      ctx.globalAlpha = f * q0;
      rr(ctx, W / 2 - bw0 / 2, 44, bw0, 58, 16); ctx.fillStyle = '#FFF4B8'; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = '#F0D25A'; ctx.stroke();
      txt(ctx, s0, W / 2, 84, { size: 32, family: lit ? ZH : EN, weight: 'bold', color: C.ink, align: 'center' });
      if (lit) chip(ctx, '字面意思', W / 2 - bw0 / 2 - 12, 73, { size: 18, align: 'right', bg: '#F1E6CC', color: '#6E5520' });
      ctx.globalAlpha = 1;
    } else {
      const wz = fit(ctx, film.word, EN, 'bold', 64, W - 420, 36);
      if (film.owner) drawWord(ctx, film, { k: 0, y: 104, size: wz, colored: true, alpha: f });
      else txt(ctx, film.word, W / 2, 104, { size: wz, family: EN, weight: 'bold', color: C.ink, align: 'center', alpha: f });
    }
    const mk = sc.marks && sc.marks.length >= n ? sc.marks : null;
    const at = i => (mk ? mk[i] : 0.3 + i * 0.9);
    const label = (pc, i) => (n > 1 ? ['①', '②', '③'][i] + ' ' : '') + (pc.text || (i === 0 ? film.meaning.main : ''));
    if (n === 1) {
      const q = easeOut(clamp((tl - at(0)) / 0.5)), pc = pics[0];
      ctx.globalAlpha = f * q;
      drawPic(ctx, pc, 90, 150 + (1 - q) * 20, 660, 450, { q, lt: tl - at(0) });
      ctx.globalAlpha = f * q;
      const tx = 800, tw = W - tx - 70;
      txt(ctx, '现在的意思', tx, 250, { size: 26, weight: 'bold', color: '#8A6A2A' });
      const t = pc.text || film.meaning.main, mz = fit(ctx, t, ZH, 'bold', 56, tw, 34);
      setFont(ctx, mz, ZH, 'bold');
      const lines = wrap(ctx, t, tw, 3);
      lines.forEach((ln, j) => txt(ctx, ln, tx, 322 + j * (mz + 14), { size: mz, weight: 'bold', color: C.ink }));
      const en = pc.evo && pc.evo.length ? '“' + (lit || film.word) + '” → ' + pc.evo.join(' → ') + ' → ' + t : (pc.ex ? '' : pc.en || film.meaning.example);
      if (en) { ctx.globalAlpha = f * clamp((tl - at(0) - 0.6) / 0.4); para(ctx, en, tx, 340 + lines.length * (mz + 14), tw, { size: pc.evo && pc.evo.length ? 26 : 28, family: pc.evo && pc.evo.length ? ZH : EN, weight: pc.evo && pc.evo.length ? 'normal' : 'italic', color: C.soft, maxLines: 4, lh: 1.4 }); }
      ctx.globalAlpha = 1;
      return;
    }
    const gap = n === 2 ? 46 : 34, pw = (W - 160 - gap * (n - 1)) / n;
    const ph = hasEvo ? (n === 2 ? 262 : 210) : (n === 2 ? 356 : 280), y0 = hasEvo ? 232 : 146;
    const chainAt = i => (mk && mk.length >= 2 * n ? mk[n + i] : at(i) + 0.6);
    pics.forEach((pc, i) => {
      const q = easeOut(clamp((tl - at(i)) / 0.5));
      if (q <= 0) return;
      const x = 80 + i * (pw + gap);
      if (hasEvo && pc.evo && pc.evo.length) {                        // 字面意思 → 这个意思：弯箭头 + 中间几步
        const qc = clamp((tl - chainAt(i) + 0.1) / 0.7);
        if (qc > 0) {
          setFont(ctx, 32, lit ? ZH : EN, 'bold');
          const half = Math.min(ctx.measureText(lit ? '“' + lit + '”' : film.word).width / 2, 130);
          const ax0 = W / 2 + (n > 1 ? (i - (n - 1) / 2) * 2 / (n - 1) * half * 0.7 : 0), ay0 = 104, ax1 = x + pw / 2, ay1 = y0 - 82, cxp = ax1, cyp = ay0 + 8;
          ctx.save(); ctx.globalAlpha = f; ctx.strokeStyle = '#C9A85A'; ctx.lineWidth = 4; ctx.lineCap = 'round';
          ctx.beginPath(); ctx.moveTo(ax0, ay0);
          for (let k = 1; k <= 24; k++) { const u = qc * k / 24, v = 1 - u; ctx.lineTo(v * v * ax0 + 2 * v * u * cxp + u * u * ax1, v * v * ay0 + 2 * v * u * cyp + u * u * ay1); }
          ctx.stroke();
          if (qc >= 1) { ctx.fillStyle = '#C9A85A'; ctx.beginPath(); ctx.moveTo(ax1 - 9, ay1 - 6); ctx.lineTo(ax1 + 9, ay1 - 6); ctx.lineTo(ax1, ay1 + 8); ctx.closePath(); ctx.fill(); }
          ctx.restore();
          const ez = n === 2 ? 25 : 21;
          setFont(ctx, ez, ZH, 'bold');
          const lines2 = wrap(ctx, pc.evo.join(' → ') + ' →', pw - 16, 2);
          ctx.globalAlpha = f * clamp((tl - chainAt(i) - 0.2) / 0.5);
          lines2.forEach((ln, j) => txt(ctx, ln, x + pw / 2, y0 - 46 + (lines2.length === 1 ? 14 : 0) + j * (ez + 9), { size: ez, weight: 'bold', color: '#7A5A10', align: 'center' }));
          ctx.globalAlpha = 1;
        }
      }
      ctx.globalAlpha = f * q;
      drawPic(ctx, pc, x, y0 + (1 - q) * 24, pw, ph, { q, lt: tl - at(i) });
      ctx.globalAlpha = f * q;
      const lz = n === 2 ? 38 : 32, s2 = label(pc, i);
      setFont(ctx, lz, ZH, 'bold');
      const lines = wrap(ctx, s2, pw - 10, 2);
      lines.forEach((ln, j) => txt(ctx, ln, x + pw / 2, y0 + ph + 58 + j * (lz + 10), { size: lz, weight: 'bold', color: C.ink, align: 'center' }));
      const ly = y0 + ph + 58 + lines.length * (lz + 10) + 8;
      if (pc.pos || pc.diff) {
        const ta = chainAt(i);
        const qd = clamp((tl - ta + 0.1) / 0.35);
        if (qd > 0) {
          const dz = n === 2 ? 26 : 22;
          let cw = 0;
          if (pc.pos) { setFont(ctx, dz - 4, ZH, 'bold'); cw = ctx.measureText(pc.pos).width + (dz - 4) * 1.1 + 10; }
          const r = pc.diff ? fitLine(ctx, pc.diff, ZH, 'normal', dz, pw - 20 - cw, 16) : { t: '', z: dz };
          setFont(ctx, r.z, ZH);
          const tw = cw + (r.t ? ctx.measureText(r.t).width : 0);
          let xx = x + pw / 2 - tw / 2;
          ctx.globalAlpha = f * q * qd;
          if (pc.pos) { chip(ctx, pc.pos, xx, ly - dz * 0.36, { size: dz - 4, bg: '#E2F3E5', color: '#2B7A3E' }); xx += cw; }
          if (r.t) txt(ctx, r.t, xx, ly, { size: r.z, color: C.soft });
        }
      } else if (pc.en && !pc.ex) {
        const ez = n === 2 ? 26 : 22, r = fitLine(ctx, pc.en, EN, 'italic', ez, pw - 10, 16);
        txt(ctx, r.t, x + pw / 2, ly, { size: r.z, family: EN, weight: 'italic', color: C.soft, align: 'center' });
      }
      ctx.globalAlpha = 1;
    });
  };
  // 意思是怎么一步步变过来的：竖着一条链，字面意思在最上面；每一步一个框，箭头旁边写为什么会这样变；
  // 现在的意思（pic）那一框右边贴上它的画。讲到哪一步，哪一步的箭头、说明、框才出来（marks：除了第一个框，每一框一句）
  const MEAN_C = ['#2B8A3E', '#7048E8', '#0B7285'];
  function nodeSize(ctx, s) {
    const z = s.root || s.pic != null ? 29 : 25;
    setFont(ctx, z, ZH, 'bold');
    const tw = ctx.measureText(s.node).width;
    let cw = 0;
    if (s.pos) { setFont(ctx, 19, ZH, 'bold'); cw = ctx.measureText(s.pos).width + 19 * 1.1 + 12; }
    return { z, tw, w: tw + 44 + cw };
  }
  function flowNode(ctx, s, cx, y, h, q) {
    const { z, tw, w } = nodeSize(ctx, s), main = s.pic != null;
    const col = main ? MEAN_C[s.pic % MEAN_C.length] : s.root ? '#F0D25A' : '#D9C59A';
    const bg = s.root ? '#FFF4B8' : main ? tint(col, 0.88) : '#FBF5E8';
    const k = 0.6 + 0.4 * Math.min(1.08, q);
    ctx.save();
    ctx.translate(cx, y); ctx.scale(k, k);
    rr(ctx, -w / 2, -h / 2, w, h, h / 2.6); ctx.fillStyle = bg; ctx.fill(); ctx.lineWidth = main ? 3.5 : 2.5; ctx.strokeStyle = col; ctx.stroke();
    txt(ctx, s.node, -w / 2 + 22, 2, { size: z, weight: 'bold', color: C.ink, base: 'middle' });
    if (s.pos) chip(ctx, s.pos, -w / 2 + 22 + tw + 12, 1, { size: 19, bg: '#E2F3E5', color: '#2B7A3E' });
    ctx.restore();
    return w;
  }
  const figOf = (film, s) => s.fig || (s.pic != null && film.pics[s.pic] ? film.pics[s.pic] : null);
  S.evolve = (ctx, film, p, sc) => {
    const st = film.flow || [], n = st.length;
    if (!n) return;
    if (st.some(s => figOf(film, s))) return evolveStage(ctx, film, p, sc);
    const f = fadeOf(sc, p), tl = sc.tl != null ? sc.tl : p * sc.dur;
    header(ctx, film, '意思是怎么一步步变过来的', f);
    const T0 = stepTimes(sc, n);
    const at = k => T0[k].at;
    const picRows = st.map((s, k) => (s.pic != null ? k : -1)).filter(k => k >= 0);
    const cx = picRows.length ? 390 : W / 2, top = 140, bottom = 666, NH = 52;
    const gy = n > 1 ? Math.min(150, (bottom - top) / (n - 1)) : 0;
    const ys = st.map((_, k) => (n > 1 ? top + k * gy : (top + bottom) / 2));
    let dmin = 1e9;
    for (let a = 1; a < picRows.length; a++) dmin = Math.min(dmin, ys[picRows[a]] - ys[picRows[a - 1]]);
    const ph = Math.max(96, Math.min(214, dmin - 14)), pw = Math.min(400, ph * 1.8), px = 1200 - pw;
    st.forEach((s, k) => {
      const t = at(k), y = ys[k];
      if (tl < t) return;
      if (k > 0) {
        const src = s.from != null && s.from >= 0 && s.from < k ? s.from : k - 1;
        const qa = clamp((tl - t) / 0.6), y0 = ys[src] + NH / 2 + 5, y1 = y - NH / 2 - 9;
        ctx.save(); ctx.globalAlpha = f; ctx.strokeStyle = '#C9A85A'; ctx.lineWidth = 4; ctx.lineCap = 'round';
        ctx.beginPath();
        if (src === k - 1) { ctx.moveTo(cx, y0); ctx.lineTo(cx, lerp(y0, y1, qa)); }
        else {                                                    // 从更上面的框来：从左边绕下来
          const sw = nodeSize(ctx, st[src]).w / 2, ex0 = cx - sw - 6, ey0 = ys[src], lx2 = cx - 300;
          for (let j = 0; j <= 30; j++) {
            const u = qa * j / 30, v = 1 - u;
            const bx2 = v * v * v * ex0 + 3 * v * v * u * lx2 + 3 * v * u * u * lx2 + u * u * u * cx, by2 = v * v * v * ey0 + 3 * v * v * u * ey0 + 3 * v * u * u * y1 + u * u * u * y1;
            if (j) ctx.lineTo(bx2, by2); else ctx.moveTo(bx2, by2);
          }
        }
        ctx.stroke();
        if (qa >= 1) { ctx.fillStyle = '#C9A85A'; ctx.beginPath(); ctx.moveTo(cx - 9, y1 - 4); ctx.lineTo(cx + 9, y1 - 4); ctx.lineTo(cx, y1 + 9); ctx.closePath(); ctx.fill(); }
        ctx.restore();
        if (s.via) {
          ctx.globalAlpha = f * clamp((tl - t - 0.15) / 0.45);
          const vx = cx + 24, vw = (picRows.length ? px - 24 : W - 100) - vx;
          setFont(ctx, 22, ZH, 'bold');
          const lns = wrap(ctx, s.via, vw, 2), my = (y0 + y1) / 2;
          if (s.rule) {                                           // 这一步是英语的用词规律：黄底标出来，左边挂个牌子
            const mw = Math.max(...lns.map(ln => ctx.measureText(ln).width));
            rr(ctx, vx - 8, my + 8 - 22 - (lns.length - 1) * 14 - 4, mw + 16, lns.length * 28 + 10, 8); ctx.fillStyle = '#FFE9A8'; ctx.fill();
            chip(ctx, '★ 英语用词规律', cx - 18, my, { size: 18, align: 'right', bg: '#FFD54F', color: '#6B4400' });
            setFont(ctx, 22, ZH, 'bold');
          }
          lns.forEach((ln, j) => txt(ctx, ln, vx, my + 8 + (j - (lns.length - 1) / 2) * 28, { size: 22, weight: 'bold', color: '#7A5A10' }));
          ctx.globalAlpha = 1;
        }
      }
      const qn = easeBack(clamp((tl - t - (k ? 0.5 : 0)) / 0.45));
      if (qn <= 0) return;
      ctx.globalAlpha = f * Math.min(1, qn);
      const w = flowNode(ctx, s, cx, y, NH, qn);
      (s.icons || []).forEach((e, j) => { const qi = easeBack(clamp((tl - t - 0.8 - j * 0.2) / 0.4)); if (qi > 0) { ctx.globalAlpha = f * Math.min(1, qi); emoji(ctx, e, cx + w / 2 + 34 + j * 50, y, 42 * qi); } });
      ctx.globalAlpha = 1;
      if (s.pic != null && film.pics[s.pic]) {
        const qp = clamp((tl - t - 0.8) / 0.5);
        if (qp > 0) {
          const pcy = Math.max(top - 26 + ph / 2, Math.min(H - 14 - ph / 2, y));
          ctx.save(); ctx.globalAlpha = f * qp; ctx.setLineDash([8, 8]); ctx.strokeStyle = '#D9C59A'; ctx.lineWidth = 3;
          ctx.beginPath(); ctx.moveTo(cx + w / 2 + 10, y); ctx.lineTo(px - 12, pcy); ctx.stroke(); ctx.restore();
          ctx.globalAlpha = f * qp;
          drawPic(ctx, film.pics[s.pic], px, pcy - ph / 2, pw, ph, { q: qp, lt: tl - t - 0.8 });
          ctx.globalAlpha = 1;
        }
      }
    });
  };
  // 5.0 起：演变那一幕的新样子。左边竖着一条链（字面意思 → 每一步一个框，箭头旁写为什么这样变），
  // 右边一块大画板：讲到哪一步，画板上放哪一步的示意图（fig；现在的意思那一步没写 fig 就用它的画），下面写这一幅画的是什么。
  // 画和配音永远对得上：说“小孔把屋外的景物映在墙上”的时候，画板上正在演光线穿过小孔、墙上出现倒立的像。
  // 一步拆成几句配音时（plan.json 里 evolve 的 groups，每一步几句）：每一步从它第一句开始，cues 是这一步每一句开始的秒数
  function stepTimes(sc, n) {
    const g = Array.isArray(sc.groups) && sc.groups.length === n - 1 ? sc.groups.map(Number) : null;
    const total = g ? g.reduce((a, b) => a + b, 0) : n - 1;
    const mk = sc.marks && sc.marks.length >= total ? sc.marks : null;
    const en = mk && Array.isArray(sc.ends) && sc.ends.length >= total ? sc.ends : null;      // 5.11：每一句说完的秒数（按词出东西要用）
    const out = [{ at: 0.15, cues: [], ends: [] }];
    let j = 0;
    for (let k = 1; k < n; k++) {
      const m = g ? g[k - 1] : 1, cues = [], ends = [];
      for (let c = 0; c < m; c++) { cues.push(mk ? mk[j + c] : 0.6 + (j + c) * 3.2); ends.push(en ? en[j + c] : cues[c] + 2.9); }
      out.push({ at: cues[0], cues, ends });
      j += m;
    }
    return out;
  }
  function evolveStage(ctx, film, p, sc) {
    const st = film.flow, n = st.length;
    const f = fadeOf(sc, p), tl = sc.tl != null ? sc.tl : p * sc.dur;
    header(ctx, film, '意思是怎么一步步变过来的', f);
    const T = stepTimes(sc, n);
    const at = k => T[k].at;
    const SX = 636, SY = 116, SW = 600, SH = 448;
    // 6.23：左边改成思维导图式的树（用户：“左边的这个演示不是很清楚……那个弯的线条的箭头打的不是很准，我觉得可以用思维导图的形式或更好……要清楚，也要好懂”）。
    // 字面意思在最上面；每个意思占一行，往右缩一级 = 从上一级变来的。从上一级的框底下拉一根竖线（主干），到这一行拐个直角，箭头正好顶在这一框的左边；
    // 为什么这样变，写在这一框的正上方（用词规律那一步先挂“★ 英语用词规律”牌子、字垫黄）。线都是横平竖直的，不绕弯，不压字。
    const NH = 52, L0 = 30, IND = 50, ELB = 34, LH = 26, top0 = 140, bottom = 676, xMax = SX - 24;
    const src = st.map((s, k) => (k ? (s.from != null && s.from >= 0 && s.from < k ? s.from : k - 1) : -1));
    const dep = [];
    st.forEach((s, k) => { dep[k] = k ? dep[src[k]] + 1 : 0; });
    const boxL = st.map((s, k) => L0 + dep[k] * IND + (k ? ELB : 0));
    const fit = st.map((s, k) => Math.min(1, (xMax - boxL[k]) / nodeSize(ctx, s).w));
    const wid = st.map((s, k) => nodeSize(ctx, s).w * fit[k]);
    setFont(ctx, 21, ZH, 'bold');
    const lab = st.map((s, k) => (k && s.via ? { lines: wrap(ctx, s.via, Math.max(120, xMax - boxL[k] - 12), 2), rule: !!s.rule } : { lines: [], rule: false }));
    const labH = lab.map((l, k) => (l.lines.length ? (l.rule ? 34 : 0) + l.lines.length * LH + 6 : 0));
    const rowH = st.map((s, k) => labH[k] + NH + (k < n - 1 ? 30 : 0));
    const total = rowH.reduce((x, y) => x + y, 0);
    const maxR = Math.max(...st.map((s, k) => Math.max(boxL[k] + wid[k], lab[k].lines.length ? boxL[k] + Math.max(...lab[k].lines.map(ln => ctx.measureText(ln).width)) + 8 : 0)));
    const sk = Math.min(1.3, (bottom - top0) / total, (SX - 28) / maxR);    // 整棵树按地方大小放大或缩小：太高、太宽就缩，地方够就放大一点，看得清
    const oy = top0 + Math.max(0, (bottom - top0 - total * sk) / 2);
    const Y = [], LY = [];
    let cur0 = 0;
    st.forEach((s, k) => { LY[k] = cur0; Y[k] = cur0 + labH[k] + NH / 2; cur0 += rowH[k]; });
    const ys = Y.map(y => oy + y * sk);                                     // 画板那根虚线要用真的坐标
    let cur = 0;
    for (let k = 0; k < n; k++) if (tl >= at(k)) cur = k;
    ctx.save();
    ctx.translate(0, oy); ctx.scale(sk, sk);
    const LC = '#C9A85A';
    st.forEach((s, k) => {
      const t = at(k), y = Y[k];
      if (tl < t) return;
      if (k > 0) {
        const pk = src[k], tx = boxL[pk] + 24, y0 = Y[pk] + NH / 2 + 2, x1 = boxL[k] - 3;
        const len1 = Math.max(1, y - y0), len2 = Math.max(1, x1 - tx), qa = clamp((tl - t) / 0.7) * (len1 + len2);
        ctx.save(); ctx.globalAlpha = f; ctx.strokeStyle = LC; ctx.lineWidth = 4; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
        ctx.beginPath(); ctx.moveTo(tx, y0);
        ctx.lineTo(tx, y0 + Math.min(qa, len1));
        if (qa > len1) ctx.lineTo(tx + Math.min(qa - len1, len2 - 12), y);
        ctx.stroke();
        if (qa >= len1 + len2 - 0.5) { ctx.fillStyle = LC; ctx.beginPath(); ctx.moveTo(x1 + 1, y); ctx.lineTo(x1 - 15, y - 9); ctx.lineTo(x1 - 15, y + 9); ctx.closePath(); ctx.fill(); }
        ctx.restore();
        const L = lab[k];
        if (L.lines.length) {
          ctx.globalAlpha = f * clamp((tl - t - 0.15) / 0.45);
          let ly = LY[k];
          if (L.rule) { chip(ctx, '★ 英语用词规律', boxL[k], ly + 15, { size: 17, bg: '#FFD54F', color: '#6B4400' }); ly += 34; }
          setFont(ctx, 21, ZH, 'bold');
          if (L.rule) {
            const mw = Math.max(...L.lines.map(ln => ctx.measureText(ln).width));
            rr(ctx, boxL[k] - 8, ly - 2, mw + 16, L.lines.length * LH + 6, 8); ctx.fillStyle = '#FFE9A8'; ctx.fill();
          }
          L.lines.forEach((ln, j) => txt(ctx, ln, boxL[k], ly + 20 + j * LH, { size: 21, weight: 'bold', color: '#7A5A10' }));
          ctx.globalAlpha = 1;
        }
      }
      const qn = easeBack(clamp((tl - t - (k ? 0.55 : 0)) / 0.45));
      if (qn <= 0) return;
      const ccx = boxL[k] + wid[k] / 2;
      if (k === cur && n > 1) {                                   // 正在讲的那一框：外面一圈光
        ctx.save(); ctx.globalAlpha = f * Math.min(1, qn) * 0.9; ctx.shadowColor = 'rgba(240,165,0,.55)'; ctx.shadowBlur = 20;
        rr(ctx, boxL[k] - 4, y - NH * fit[k] / 2 - 4, wid[k] + 8, NH * fit[k] + 8, (NH * fit[k] + 8) / 2.6); ctx.strokeStyle = 'rgba(240,165,0,.8)'; ctx.lineWidth = 3; ctx.stroke(); ctx.restore();
      }
      ctx.save(); ctx.globalAlpha = f * Math.min(1, qn);
      ctx.translate(ccx, y); ctx.scale(fit[k], fit[k]);
      flowNode(ctx, s, 0, 0, NH, qn);
      ctx.restore();
      ctx.globalAlpha = 1;
    });
    ctx.restore();
    // 画板：现在讲到的这一步（这一步没有画就留着上一幅）；换一幅时上一幅淡出
    let fk = -1, pk = -1;
    for (let k = cur; k >= 0; k--) if (figOf(film, st[k])) { if (fk < 0) fk = k; else { pk = k; break; } }
    if (fk < 0) return;
    const tOf = k => at(k) + (k ? 0.35 : 0);
    const cuesOf = k => T[k].cues.map(c => c - tOf(k));                     // 示意图里按句出东西：每一句开始的秒数（从这一幅出现算起）
    const stOf = (k, q) => ({ q, lt: tl - tOf(k), cues: cuesOf(k), cueEnds: T[k].ends.map(c => c - tOf(k)), cueTexts: [].concat(st[k].sayList || st[k].say || []).map(String) });
    const qf = clamp((tl - tOf(fk)) / 0.45);
    ctx.save();
    if (pk >= 0 && qf < 1) { ctx.globalAlpha = f * (1 - qf); drawPic(ctx, figOf(film, st[pk]), SX, SY, SW, SH, stOf(pk, 1)); }
    ctx.globalAlpha = f * qf;
    drawPic(ctx, figOf(film, st[fk]), SX, SY + (pk < 0 ? (1 - qf) * 16 : 0), SW, SH, stOf(fk, qf));
    ctx.restore();
    const s = st[fk], cap = s.cap || String(s.node).replace(/^[①②③]\s*/, '').replace(/[“”]/g, '');
    const main = s.pic != null, col = main ? MEAN_C[s.pic % MEAN_C.length] : s.root ? '#B8860B' : '#8A6A2A';
    chip(ctx, cap, SX + SW / 2, SY + SH + 40, { size: 26, align: 'center', bg: main ? tint(col, 0.86) : s.root ? '#FFF4B8' : '#F1E6CC', color: col, alpha: f * qf });
    const rx = (boxL[fk] + wid[fk]) * sk + 12;
    if (rx < SX - 30) {                                       // 这一框连到画板的虚线（框很宽、已经挨着画板就不画）
      ctx.save(); ctx.globalAlpha = f * qf * 0.9; ctx.setLineDash([8, 8]); ctx.strokeStyle = '#D9C59A'; ctx.lineWidth = 3;
      ctx.beginPath(); ctx.moveTo(rx, ys[fk]); ctx.lineTo(SX - 10, Math.max(SY + 40, Math.min(SY + SH - 40, ys[fk]))); ctx.stroke(); ctx.restore();
    }
  }
  // 例句：上面一幅大动画演这句话，下面英文（本词标出来）、中文；配音先念英文再念中文，念到哪句哪句出来
  function sentence(ctx, s, word, cx, y, size) {
    const stem = String(word || '').toLowerCase().replace(/(e|y)$/, '');
    const toks = String(s || '').match(/[A-Za-z'’-]+|[^A-Za-z'’-]+/g) || [];
    let z = size;
    setFont(ctx, z, EN, 'bold');
    while (z > 22 && ctx.measureText(s).width > W - 150) { z -= 2; setFont(ctx, z, EN, 'bold'); }
    let x = cx - ctx.measureText(s).width / 2;
    toks.forEach(tk => {
      setFont(ctx, z, EN, 'bold');
      const w = ctx.measureText(tk).width;
      const hit = stem.length >= 3 && /[A-Za-z]/.test(tk) && tk.toLowerCase().startsWith(stem);
      if (hit) { rr(ctx, x - 5, y + z * 0.06, w + 10, z * 0.3, 5); ctx.fillStyle = C.marker; ctx.fill(); }
      txt(ctx, tk, x, y, { size: z, family: EN, weight: 'bold', color: hit ? '#B23A0E' : C.ink });
      x += w;
    });
  }
  S.example = (ctx, film, p, sc) => {
    const pc = (film.pics || [])[sc.i];
    if (!pc) return;
    const f = fadeOf(sc, p), tl = sc.tl != null ? sc.tl : p * sc.dur, n = film.pics.length;
    const mk = sc.marks && sc.marks.length >= 1 ? sc.marks : null;
    ctx.globalAlpha = f;
    let x = 80;
    x += chip(ctx, '例句' + (n > 1 ? ' ' + ['①', '②', '③'][sc.i] : ''), x, 52, { size: 22, bg: '#FFE9A8', color: '#7A5A10' }) + 14;
    if (pc.text) { txt(ctx, pc.text, x, 61, { size: 28, weight: 'bold', color: C.ink }); setFont(ctx, 28, ZH, 'bold'); x += ctx.measureText(pc.text).width + 14; }
    if (pc.pos) chip(ctx, pc.pos, x, 52, { size: 20, bg: '#E2F3E5', color: '#2B7A3E' });
    const q = easeOut(clamp(tl / 0.45));
    ctx.globalAlpha = f * q;
    const a0 = mk ? mk[0] : 0.45, a1 = mk && mk[1] != null ? mk[1] : a0 + 2.4;
    drawPic(ctx, pc.exPic || pc, 80, 84 + (1 - q) * 14, W - 160, 432, { q, lt: tl, cues: [a0, a1],
      cueEnds: mk && Array.isArray(sc.ends) && sc.ends.length >= 2 ? sc.ends.slice(0, 2) : [a1 - 0.36, a1 + 2.4], cueTexts: [String(pc.ex || ''), String(pc.exzh || '')] });
    ctx.globalAlpha = f * clamp((tl - a0 + 0.15) / 0.35);
    sentence(ctx, pc.ex, film.word, W / 2, 586, 40);
    if (pc.exzh) { ctx.globalAlpha = f * clamp((tl - a1 + 0.15) / 0.35); txt(ctx, pc.exzh, W / 2, 648, { size: 31, color: C.soft, align: 'center' }); }
    ctx.globalAlpha = 1;
  };
  function meaningPlain(ctx, film, p, sc) {
    const f = fadeOf(sc, p);
    // 分开的字母合回一个词
    if (film.owner && !film.dropE) {
      const k = 1 - easeInOut(span(p, 0.0, 0.3));
      const size = lerp(fit(ctx, film.word, EN, 'bold', 130, W - 240, 50), stripSize(ctx, film), k);
      drawWord(ctx, film, { k, y: lerp(250, 205, k), size, colored: true, blocks: k, plus: k, alpha: Math.min(1, span((1 - p) * sc.dur, 0, 0.3)) });
    } else {
      const size = fit(ctx, film.word, EN, 'bold', 130, W - 240, 50);
      txt(ctx, film.word, W / 2, 250, { size, family: EN, weight: 'bold', color: C.ink, align: 'center', alpha: f });
    }
    const m = film.meaning;
    const q = span(p, 0.25, 0.45);
    ctx.globalAlpha = f * q;
    const hasIc = !!m.icon;
    const tx = hasIc ? 470 : 200, tw = W - tx - 140;
    if (hasIc) { const z = easeBack(span(p, 0.3, 0.5)); if (z > 0) emoji(ctx, m.icon, 330, 470, 170 * z); if (m.neg) slash(ctx, 330, 470, 170, span(p, 0.5, 0.7)); }
    txt(ctx, '现在的意思', tx, 375, { size: 26, weight: 'bold', color: '#8A6A2A' });
    const mz = fit(ctx, m.main, ZH, 'bold', 54, tw, 30);
    setFont(ctx, mz, ZH, 'bold');
    const mainLines = wrap(ctx, m.main, tw, 2);
    mainLines.forEach((ln, i) => txt(ctx, ln, tx, 445 + i * (mz + 12), { size: mz, weight: 'bold', color: C.ink }));
    let y = 445 + mainLines.length * (mz + 12) + 6;
    if (m.second) { const r = fitLine(ctx, m.second, ZH, 'normal', 32, tw, 24); txt(ctx, r.t, tx, y, { size: r.z, color: C.soft }); y += 50; }
    if (m.example) { const r = fitLine(ctx, m.example, EN, 'italic', 30, tw, 22); txt(ctx, r.t, tx, y, { size: r.z, family: EN, weight: 'italic', color: C.soft }); }
    ctx.globalAlpha = 1;
  }
  S.family = (ctx, film, p, sc) => {
    const f = fadeOf(sc, p);
    header(ctx, film, '', f);
    const fam = film.family;
    const title = fam.title || (fam.shared ? '同一词族：都带着 ' + fam.shared : '同一词族');
    txt(ctx, title, W / 2, 175, { size: 40, weight: 'bold', color: C.ink, align: 'center', alpha: f });
    const words = fam.words, cols = words.length <= 3 ? words.length : 4, rows = Math.ceil(words.length / cols);
    const cw = 250, ch = 116, gx = 26, gy = 26;
    const x0 = (W - cols * cw - (cols - 1) * gx) / 2, y0 = 235 + (rows === 1 ? 70 : 0);
    words.forEach((w, i) => {
      const r = Math.floor(i / cols), c = i % cols;
      const q = easeBack(span(p, 0.1 + i * 0.06, 0.25 + i * 0.06));
      if (q <= 0) return;
      const x = x0 + c * (cw + gx), y = y0 + r * (ch + gy);
      ctx.save();
      ctx.globalAlpha = f * Math.min(1, q);
      ctx.translate(x + cw / 2, y + ch / 2); ctx.scale(q, q); ctx.translate(-(x + cw / 2), -(y + ch / 2));
      rr(ctx, x, y, cw, ch, 16); ctx.fillStyle = C.card; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = C.line; ctx.stroke();
      const size = fit(ctx, w, EN, 'bold', 44, cw - 30, 20);
      setFont(ctx, size, EN, 'bold');
      const tw = ctx.measureText(w).width;
      let xx = x + (cw - tw) / 2;
      const lo = w.toLowerCase(), at = fam.shared ? lo.indexOf(fam.shared) : -1;
      const segs = at >= 0 ? [[w.slice(0, at), C.ink], [w.slice(at, at + fam.shared.length), fam.color], [w.slice(at + fam.shared.length), C.ink]] : [[w, C.ink]];
      segs.forEach(([s, col]) => {
        if (!s) return;
        txt(ctx, s, xx, y + ch / 2 + size * 0.35, { size, family: EN, weight: 'bold', color: col });
        const sw = ctx.measureText(s).width;
        if (col !== C.ink) { ctx.fillStyle = col; ctx.fillRect(xx, y + ch / 2 + size * 0.5, sw, 4); }
        xx += sw;
      });
      ctx.restore();
    });
    if (fam.more) txt(ctx, '还有 ' + fam.more + ' 个', W / 2, Math.min(H - 40, y0 + rows * (ch + gy) + 30), { size: 26, color: C.faint, align: 'center', alpha: f * span(p, 0.6, 0.8) });
  };
  S.end = (ctx, film, p) => {
    const q = easeOut(span(p, 0, 0.25));
    const y = 320;
    if (film.parts) {
      // transport = trans + port
      const segs = [[film.word, C.ink], [' = ', C.faint]];
      film.parts.forEach((pt, i) => { segs.push([pt.text, pt.color]); if (i < film.parts.length - 1) segs.push([' + ', C.faint]); });
      line(ctx, segs, y, 80, q);
    } else if (film.variant) {
      line(ctx, [[film.variant.to, C.ink], [' ← ', C.faint], [film.variant.from.replace(/[()]/g, ''), PART[0]]], y, 80, q);
    } else if (film.related) {
      const segs = [];
      film.related.forEach((s, i) => { if (i) segs.push([' ≈ ', C.faint]); segs.push([s, i ? PART[0] : C.ink]); });
      line(ctx, segs, y, 80, q);
    } else {
      line(ctx, [[film.word, C.ink]], y, 96, q);
    }
    const lit = (film.combo && film.combo.literal) || '';
    const m = film.meaning.main;
    const segs2 = [];
    if (lit) segs2.push(['“' + lit + '”', C.ink, true]);
    if (lit && m) segs2.push(['  →  ', '#B69D62']);
    if (m) segs2.push([m, C.green]);
    if (segs2.length) line(ctx, segs2, 450, 42, span(p, 0.2, 0.45), ZH);
  };
  // 一行几段不同颜色的字，居中；高亮的段下面画一道黄
  // 每段：[文字, 颜色, 是否高亮, 字体]；箭头、≈ 用中文字体画（英文衬线字体里没有，会画成一小横）
  function line(ctx, segs, y, size, alpha, family) {
    family = family || EN;
    let z = size;
    const fam = sg => sg[3] || (/^\s*[→←≈]\s*$/.test(sg[0]) ? ZH : family);
    const width = () => segs.reduce((s, sg) => { setFont(ctx, z, fam(sg), 'bold'); return s + ctx.measureText(sg[0]).width; }, 0);
    while (z > 22 && width() > W - 140) z -= 2;
    let x = (W - width()) / 2;
    segs.forEach(sg => {
      const [s, col, hl] = sg;
      setFont(ctx, z, fam(sg), 'bold');
      const w = ctx.measureText(s).width;
      if (hl) { ctx.globalAlpha = alpha * 0.9; rr(ctx, x - 6, y - z * 0.45, w + 12, z * 0.62, 6); ctx.fillStyle = '#FFF0A0'; ctx.fill(); ctx.globalAlpha = 1; }
      txt(ctx, s, x, y, { size: z, family: fam(sg), weight: 'bold', color: col, alpha });
      x += w;
    });
  }

  // ---------------------------------------------------------------- 小黑板（结尾总结，方便学生停下来抄）
  // 每行 { label 小标题, segs: [[文字, 粉笔色, { size }]…], size }；粉笔色：w 白、y 黄、b 蓝、p 粉、g 绿、o 橙、f 淡白
  const CHALK_C = { w: '#F3F0E4', y: '#F6E27A', b: '#A3D2F3', p: '#F5AFC0', g: '#B8E4A4', o: '#F8C48E', v: '#D3B8F5', f: 'rgba(243,240,228,.6)' };
  const PART_CHALK = ['b', 'o', 'g', 'p', 'y'];
  // 5.7 起结尾的小结默认是一张轻松的笔记纸（浅色点点纸、彩色笔、胶带贴图），不再是黑板（用户觉得黑板“看着有点压力”）；
  // prefs.board.style = 'chalk' 还是原来的黑板。颜色键和黑板一样（w 正文、y 重点、b 蓝……），换成浅底上看得清的深一点的颜色
  const NOTE_C = { w: '#2E3A33', y: '#C2571A', b: '#2F6FA8', p: '#C2456B', g: '#3B8A4C', o: '#B9740F', v: '#7553B5', f: 'rgba(46,58,51,.55)' };
  let BC = CHALK_C;
  // 6.1（用户：“最后的总结部分有溢出；有的内容比较多的，可以分两页进行总结”）：
  //   · 一页放得下（卡片那一块够高）就还是一页，和以前一样（camera）；
  //   · 放不下就分两页：“总结 1/2”只写字（地方大了，多写“变化”“辨”两行，扩展词、重点都留着），“总结 2/2”每个意思一行（左边画，右边意思、例句、中文）；
  //   · 起草阶段卡片上还一个例句都没有：不贴卡片、不分页（只有自动配的小图标，贴上去没有用）。
  // prefs.board.pages = 1 / 2 可以硬性指定。返回 { lines, cards（和字同一页的卡片）, cards2（第二页的卡片）, pages, note, combo, style, title }
  function boardRows(lines, compact, k) {
    const by = 34, n = lines.length, rows = [];
    k = k || 1;
    let y = by + (compact ? 112 : 128 - (1 - k) * 44);
    lines.forEach((ln, i) => {
      const zk = (compact ? (ln.size ? 0.82 : 0.88) : 1) * k, size = (ln.size || 34) * zk;
      if (ln.hl && !(lines[i - 1] && lines[i - 1].hl)) y += 12;                 // 重点框上下留一点空
      rows.push({ y, size, zk });
      y += (compact ? (i === 0 ? size * 1.2 : Math.max(size * 1.38, 42)) : Math.max(size * 1.5, 58 * k) * (n > 6 ? 0.88 : 1)) * (lines[i + 1] && lines[i + 1].gap ? lines[i + 1].gap : 1) + (ln.hl && !(lines[i + 1] && lines[i + 1].hl) ? 8 : 0);
    });
    return { rows, yAfter: y };
  }
  // 只写字的一页（没有卡片）：字从原来的大小往小试，最后一行写得进纸里为止（最小七成）
  function boardFit(lines, note) {
    const limit = 34 + (H - 104) + 14 - (note ? 50 : 0);          // 右下角要写“暂停一下，抄进笔记本”这类提醒的，给它留一行
    for (let k = 1; k > 0.7; k -= 0.02) {
      const { rows } = boardRows(lines, false, k), last = rows[rows.length - 1];
      if (!last || last.y + last.size * 0.45 <= limit) return k;
    }
    return 0.7;
  }
  // 和字同一页时，卡片那一块还剩多高（和 S.board 里算的一样）
  function boardCardRoom(lines, chalk) {
    const by = 34, bh = H - 104, { yAfter } = boardRows(lines, true, 1);
    return (by + bh + (chalk ? -12 : 26)) - (yAfter - 26) - 12;
  }
  function boardLines(film, d, opts) {
    const note = opts.note || '';
    const combo = opts.combo !== false, chalk = opts.style === 'chalk';
    let cards = boardCards(film, opts);
    if (!cards.some(c => c.ex)) cards = [];                                   // 6.1：还没有例句（起草阶段）不贴卡片
    const done = (lines, cap) => {
      // 分不分页：有卡片、又没硬性指定一页时，看卡片那一块够不够高（几张卡竖着排要 240，一张横着排要 180）
      let pages = 1;
      if (cards.length && opts.pages !== 1) {
        // 几张卡竖着排：画至少 110 高 + 下面三行字（例句长、要分两行的再多 18）；一张卡横着排要 180
        const perLine = cards.length === 2 ? 46 : 30;
        const need = cards.length === 1 ? 180 : 244 + (cards.some(c => String(c.ex || '').length > perLine) ? 18 : 0);
        if (opts.pages === 2 || boardCardRoom(lines.slice(0, cap), chalk) < need) pages = 2;
      }
      return { pages, note, combo, style: opts.style || '', title: opts.title || '' };
    };
    if (Array.isArray(opts.lines) && opts.lines.length) {
      const lines = [];
      opts.lines.forEach(ln => { if (ln && ln.extend) lines.push(...extendLines(film)); else if (ln && ln.rules) lines.push(...ruleLines(film, opts)); else if (ln) lines.push(ln); });
      if (!opts.lines.some(ln => ln && ln.rules)) lines.push(...ruleLines(film, opts));
      const r = done(lines, 9);
      return Object.assign(r, { lines: lines.slice(0, r.pages === 2 ? 12 : 9), cards: r.pages === 2 ? [] : cards, cards2: r.pages === 2 ? cards : [] });
    }
    const L = [];
    L.push(...headLines(film, opts));
    if (film.pron) L.push(pronLine(film.pron));
    if (film.parts) {
      const a = [], g = [];
      film.parts.forEach((pt, i) => {
        if (i) { a.push([' + ', 'f']); g.push([' + ', 'f']); }
        a.push([pt.text, PART_CHALK[i % 5]]);
        g.push([pt.gloss || pt.text, PART_CHALK[i % 5]]);
      });
      L.push({ label: '拆', segs: a });
      if (film.combo && film.combo.literal) g.push([' = “' + film.combo.literal + '”', 'w']);
      L.push({ label: '意思', segs: g });
      // 5.1 起：哪个部分有“记：stat ≈ stand（站）”，小黑板写一行“记”
      const memos = film.parts.map((pt, i) => [pt, i]).filter(([pt]) => pt.memo);
      if (memos.length) {
        const segs = [];
        memos.forEach(([pt, i], j) => {
          if (j) segs.push(['    ', 'f']);
          segs.push([pt.memo.a, PART_CHALK[i % 5]], [' ' + pt.memo.sym + ' ', 'f'], [pt.memo.b, 'y'], [' ' + pt.memo.zh, 'w', { size: 28 }]);
        });
        L.push({ label: '记', segs, pri: 5 });
      }
    } else if (film.variant) {
      L.push({ label: '变', segs: [[film.variant.from.replace(/[()]/g, ''), 'b']].concat(film.variant.root && film.variant.root.gloss ? [['（' + film.variant.root.gloss + '）', 'f']] : []).concat([[' → ', 'f'], [film.variant.to, 'y']]) });
      if (film.origin && film.origin.text) L.push({ label: '来历', segs: [[film.origin.text, 'w']] });
    } else if (film.related) {
      const segs = [];
      film.related.forEach((x, i) => { if (i) segs.push([' ≈ ', 'f']); segs.push([x, i ? 'b' : 'y']); });
      L.push({ label: '同源', segs });
    } else if (film.origin && film.origin.text) L.push({ label: '来历', segs: [[film.origin.text, 'w']] });
    if (film.route && film.route.length >= 2) {
      const segs = [];
      film.route.forEach((r, i) => { if (i) segs.push([' → ', 'f']); segs.push([r.text, i === film.route.length - 1 ? 'y' : 'w']); });
      L.push({ label: '来历', segs });
    }
    // 6.1：“变化”一行——拉丁语动词的三个样子（这一部分用的那个样子写成重点色）：ducere 领 → duxi 领了 → ductus 被领的
    const verbLine = () => {
      const i = (film.parts || []).findIndex(pt => pt.verb);
      if (i < 0 || opts.verb === false) return null;
      const pt = film.parts[i], segs = [];
      pt.verb.forms.forEach((fm, j) => {
        if (j) segs.push(['  →  ', 'f']);
        const mine = (pt.verbAt === 'inf' && fm.k === '原形') || (pt.verbAt === 'pp' && fm.k === '过去分词');
        segs.push([fm.la, mine ? 'y' : 'w']);
        if (fm.zh) segs.push([' ' + fm.zh, 'f', { size: 26 }]);
      });
      return { label: '变化', segs, pri: 4 };
    };
    // 6.0：有第三部分“同义词辨析”时一行“辨”：produce 农产品 ≠ product 产品
    const distLine = () => {
      if (!film.dist || opts.dist === false) return null;
      const segs = [];
      const same = film.dist.items.every(it => it.gloss === film.dist.items[0].gloss);        // 中文意思都一样：写在最后“（都说“小心的”）”
      film.dist.items.forEach((it, i) => { if (i) segs.push(['  ≠  ', 'f']); segs.push([it.w, it.me ? 'y' : 'b']); if (it.gloss && !same) segs.push([' ' + it.gloss, 'w', { size: 28 }]); });
      if (same && (film.dist.key || film.dist.items[0].gloss)) segs.push(['  （中文都说“' + (film.dist.key || film.dist.items[0].gloss) + '”）', 'w', { size: 28 }]);
      return { label: '辨', segs, pri: 3 };
    };
    const tail = film.meaning.example && !cards.some(c => c.ex) ? [{ label: '搭配', segs: [[film.meaning.example, 'w']] }] : [];
    // 一页（最多 9 行）：和 6.0 一样——先去掉扩展词的第二行，再从后往前去掉规律下面的例子行，规律本身不去掉；还放得下才写“辨”“变化”
    const onePage = () => {
      const ext = extendLines(film), rul = ruleLines(film, opts), base = L.slice();
      while (base.length + ext.length + rul.length > 9 && ext.length > 1) ext.pop();
      for (let i = rul.length - 1; i >= 0 && base.length + ext.length + rul.length > 9; i--) if (rul[i].label === '' && !String((rul[i].segs[0] || [''])[0]).startsWith('★')) rul.splice(i, 1);
      const dl = distLine(), vl = verbLine();
      if (dl && base.length + ext.length + rul.length < 9) base.push(dl);
      if (vl && base.length + ext.length + rul.length < 9) base.push(vl);
      return base.concat(ext, rul, tail);
    };
    const one = onePage(), r = done(one, 9);
    if (r.pages === 1) return Object.assign(r, { lines: one.slice(0, 9), cards, cards2: [] });
    // 两页：第一页只写字，最多 12 行。“变化”“辨”都写上；超了就按先后去掉：扩展词第二行 → 规律下面的例子 → 辨 → 变化 → 记（重点、扩展词第一行不去）
    const ext = extendLines(film).map((x, i) => Object.assign(x, { pri: i ? 1 : 9 }));
    const rul = ruleLines(film, opts).map(x => Object.assign(x, { pri: x.label === '' && !String((x.segs[0] || [''])[0]).startsWith('★') ? 2 : 9 }));
    const vl = verbLine(), dl = distLine();
    let all = L.concat(vl ? [vl] : [], dl ? [dl] : [], ext, rul);
    for (let pri = 1; pri <= 5 && all.length > 12; pri++) for (let i = all.length - 1; i >= 0 && all.length > 12; i--) if (all[i].pri === pri) all.splice(i, 1);
    return Object.assign(r, { lines: all.slice(0, 12), cards: [], cards2: cards });
  }
  // 5.7 起：第一行单词 + 意思，意思前面写词性（n. 照相机；摄像机）。同一个词性的意思写一行，不同词性换行；
  // 意思少、一行放得下就跟在单词后面写一行（water   n. 水；v. 浇水）。prefs.board.meaning 手写的为准（字符串照写）
  function posGroups(film) {
    const groups = [];
    (film.senses || []).filter(s => s.text && !s.rare).forEach(s => {
      const ab = s.abbr || POS_ABBR[s.pos] || '';
      let g = groups.find(x => x.ab === ab);
      if (!g) groups.push(g = { ab, items: [] });
      if (g.items.length < 5 && !g.items.includes(s.text)) g.items.push(s.text);
    });
    return groups.filter(g => g.items.length);
  }
  function headLines(film, opts) {
    const word = [film.word, 'y'];
    if (typeof opts.meaning === 'string') return [{ size: 66, segs: [word, ['   ' + opts.meaning, 'w', { size: 40 }]] }];
    let groups = posGroups(film);
    if (!groups.length || !groups.some(g => g.ab)) return [{ size: 66, segs: [word, ['   ' + (film.meaning.main || ''), 'w', { size: 40 }]] }];
    if (groups.length > 3) groups = groups.slice(0, 2).concat([{ ab: '', items: [].concat(...groups.slice(2).map(g => (g.ab ? [g.ab + ' ' + g.items[0]] : []).concat(g.items.slice(g.ab ? 1 : 0)))) }]);
    const segsOf = (g, z) => (g.ab ? [[g.ab + ' ', 'b', { size: z * 0.8 }]] : []).concat([[g.items.join('；'), 'w', { size: z }]]);
    const em = t => [...t].reduce((a, ch) => a + (/[\u3400-\u9fff；，、]/.test(ch) ? 1 : 0.55), 0);
    const one = groups.map(g => (g.ab ? g.ab + ' ' : '') + g.items.join('；')).join('；  ');
    const room = film.parts && film.combo && film.combo.pic ? 17 : 23;          // 右上角贴“拼起来”那幅画时窄一点
    if (groups.length <= 2 && em(film.word) * 66 / 40 + 1.5 + em(one) <= room) {
      const segs = [word, ['   ', 'w', { size: 40 }]];
      groups.forEach((g, i) => { if (i) segs.push(['；  ', 'f', { size: 40 }]); segs.push(...segsOf(g, 40)); });
      return [{ size: 66, segs }];
    }
    return [{ size: 66, segs: [word] }].concat(groups.map(g => ({ size: 36, gap: 0.9, segs: segsOf(g, 36) })));      // 词性行和单词左对齐，像词典
  }
  // 5.0 起：小黑板“读”那一行：ca + me + ra   /ˈkæmərə/
  function pronLine(pr) {
    const segs = [];
    pr.chunks.forEach((c, i) => {
      if (i && !c.sep && !pr.chunks[i - 1].sep) segs.push([' + ', 'f']);
      c.L.forEach(x => segs.push([x.c, c.sep ? 'f' : x.silent ? 'p' : x.k === 'long' ? 'g' : x.k === 'special' ? 'v' : x.u ? 'b' : 'w', { strike: x.silent, under: x.u || 0 }]));
    });
    if (pr.ipa) segs.push(['    /' + pr.ipa + '/', 'f', { size: 28, ipa: true }]);
    return { label: '读', segs };
  }
  // 重点：英语的用词规律，一条一行（黄色），下面一行例子；prefs.board.rules = false 不要
  function ruleLines(film, opts) {
    if (opts.rules === false) return [];
    const out = [];
    (film.rules || []).forEach((r, i) => {
      out.push({ label: i ? '' : '重点', hl: true, segs: [['★ ', 'y'], [r.text, 'y']] });
      if (r.ex) out.push({ label: '', hl: true, segs: [[r.ex, 'w', { size: 29 }]] });
    });
    return out;
  }
  // 小黑板下半部分：每个意思一张卡——前面那幅画贴在黑板上，旁边用粉笔写意思、词性、例句（英文、中文）
  // 画用例句的动画（exPic，和例句对得上），没有就用意思那幅；prefs.board.cards = false 不要
  function boardCards(film, opts) {
    if (opts.cards === false) return [];
    return (film.pics || []).filter(pc => pc.text || pc.ex).slice(0, 3)
      .map(pc => ({ pic: pc.exPic || pc, wide: !!pc.exPic, text: pc.text, pos: pc.pos, ab: POS_ABBR[pc.pos] || (/^[a-z]+\.$/.test(pc.pos || '') ? pc.pos : ''), ex: pc.ex, exzh: pc.exzh }));
  }
  // 扩展词一行（放不下就两行）：单词 + 意思，和本词共用的那一段换成那一部分的颜色
  function extendLines(film) {
    const ext = (film.extend || []).slice(0, 4);
    if (!ext.length) return [];
    const colorOf = sh => { const i = (film.parts || []).findIndex(pt => normPart(pt.text) === sh || normPart(pt.head) === sh); return i >= 0 ? PART_CHALK[i % 5] : 'g'; };
    const item = x => {
      const lw = x.w.toLowerCase(), sh = String(x.share || '').toLowerCase(), at = sh ? lw.indexOf(sh) : -1;
      const segs = at >= 0 ? [[x.w.slice(0, at), 'w'], [x.w.slice(at, at + sh.length), colorOf(sh)], [x.w.slice(at + sh.length), 'w']] : [[x.w, 'w']];
      if (x.m) segs.push([' ' + x.m, 'f', { size: 28 }]);
      return segs.filter(sg => sg[0]);
    };
    const em = x => x.w.length * 0.52 + (x.m ? x.m.length * 0.85 + 0.3 : 0);
    const rows = [[]];
    let width = 0;
    ext.forEach(x => { const wdt = em(x) + 1.2; if (rows[rows.length - 1].length && width + wdt > 30) { rows.push([]); width = 0; } rows[rows.length - 1].push(x); width += wdt; });
    return rows.slice(0, 2).map((r, i) => ({ label: i ? '' : '扩展', segs: [].concat(...r.map((x, j) => (j ? [['   ', 'f']] : []).concat(item(x)))) }));
  }
  // 固定种子的随机数：每一帧粉笔灰都一样，不会闪
  function seeded(n) { let x = n >>> 0; return () => ((x = (x * 1664525 + 1013904223) >>> 0) / 4294967296); }
  let chalkLayer = null;
  function chalkCanvas() {
    if (!chalkLayer) {
      chalkLayer = typeof OffscreenCanvas !== 'undefined' ? new OffscreenCanvas(W, H) : Object.assign(document.createElement('canvas'), { width: W, height: H });
    }
    return chalkLayer;
  }
  // 总结页的底：黑板（木框、粉笔槽）或者一张点点纸（上沿贴一条胶带）。两页共用
  function boardBg(ctx, chalk) {
    const bx = 40, by = 34, bw = W - 80, bh = H - 104;
    if (chalk) {
      // 木框
      const wood = ctx.createLinearGradient(0, 0, 0, H);
      wood.addColorStop(0, '#8A5A33'); wood.addColorStop(0.5, '#73492A'); wood.addColorStop(1, '#5E3B22');
      ctx.fillStyle = wood; ctx.fillRect(0, 0, W, H);
      ctx.save();
      ctx.shadowColor = 'rgba(0,0,0,.45)'; ctx.shadowBlur = 14; ctx.shadowOffsetY = 3;
      const board = ctx.createRadialGradient(W * 0.45, H * 0.4, 80, W / 2, H / 2, W * 0.75);
      board.addColorStop(0, '#2F5646'); board.addColorStop(1, '#1D3A2F');
      rr(ctx, bx, by, bw, bh, 6); ctx.fillStyle = board; ctx.fill();
      ctx.restore();
      // 粉笔灰：擦过的痕迹
      const rnd = seeded(7);
      ctx.save();
      rr(ctx, bx, by, bw, bh, 6); ctx.clip();
      for (let i = 0; i < 46; i++) {
        const x = bx + rnd() * bw, y = by + rnd() * bh, w = 120 + rnd() * 380, h = 10 + rnd() * 34;
        ctx.globalAlpha = 0.018 + rnd() * 0.026;
        ctx.fillStyle = '#E8EFE6';
        ctx.beginPath(); ctx.ellipse(x, y, w / 2, h / 2, (rnd() - 0.5) * 0.25, 0, Math.PI * 2); ctx.fill();
      }
      ctx.restore();
      // 粉笔槽和两支粉笔
      ctx.fillStyle = '#4E311B'; ctx.fillRect(bx - 10, by + bh + 14, bw + 20, 16);
      ctx.fillStyle = '#6B4427'; ctx.fillRect(bx - 10, by + bh + 12, bw + 20, 4);
      [[bx + bw - 250, '#F3F0E4'], [bx + bw - 170, '#F6E27A']].forEach(([x, col]) => { rr(ctx, x, by + bh + 2, 62, 12, 5); ctx.fillStyle = col; ctx.fill(); });
    } else {
      // 浅色的桌面 + 一张点点纸（像手账），纸上沿贴一条彩色胶带
      const desk = ctx.createLinearGradient(0, 0, 0, H);
      desk.addColorStop(0, '#F6F1E6'); desk.addColorStop(1, '#ECE4D3');
      ctx.fillStyle = desk; ctx.fillRect(0, 0, W, H);
      ctx.save();
      ctx.shadowColor = 'rgba(90,70,40,.16)'; ctx.shadowBlur = 22; ctx.shadowOffsetY = 6;
      rr(ctx, bx, by, bw, bh + 40, 18); ctx.fillStyle = '#FFFDF8'; ctx.fill();
      ctx.restore();
      ctx.save();
      rr(ctx, bx, by, bw, bh + 40, 18); ctx.clip();
      ctx.fillStyle = 'rgba(120,105,80,.16)';
      for (let yy = by + 26; yy < by + bh + 40; yy += 28) for (let xx = bx + 26; xx < bx + bw; xx += 28) { ctx.beginPath(); ctx.arc(xx, yy, 1.3, 0, Math.PI * 2); ctx.fill(); }
      ctx.restore();
      ctx.save(); ctx.translate(W / 2, by + 2); ctx.rotate(-0.012);
      ctx.fillStyle = 'rgba(167,214,190,.75)'; ctx.fillRect(-70, -12, 140, 26);
      ctx.restore();
    }
  }
  // 左上角“总结”两个字（笔记纸上用荧光笔划一道）；分两页时后面写 1/2、2/2
  function boardTitle(lc, B, chalk, page) {
    const bx = 40, by = 34;
    const t = (chalk ? '小黑板' : (B.title || '总结')) + (B.pages === 2 ? ' ' + page + '/2' : '');
    setFont(lc, 26, CHALK);
    const tw = lc.measureText(t).width;
    if (chalk) {
      txt(lc, t, bx + 36, by + 52, { size: 26, family: CHALK, color: BC.f });
      lc.strokeStyle = BC.f; lc.lineWidth = 2;
      lc.beginPath(); lc.moveTo(bx + 34, by + 62); lc.quadraticCurveTo(bx + 34 + (tw + 4) / 2, by + 68, bx + 38 + tw, by + 61); lc.stroke();
    } else {
      lc.save(); lc.globalAlpha = 0.6; lc.fillStyle = '#FFE08A'; rr(lc, bx + 30, by + 36, tw + 12, 22, 8); lc.fill(); lc.restore();   // 荧光笔划一道
      txt(lc, t, bx + 36, by + 54, { size: 26, family: CHALK, color: BC.w });
    }
  }
  S.board = (ctx, film, p, sc) => {
    const B = film.board, chalk = B.style === 'chalk';
    BC = chalk ? CHALK_C : NOTE_C;
    const f = Math.min(1, span(p * sc.dur, 0, 0.4));
    const bx = 40, by = 34, bw = W - 80, bh = H - 104;
    boardBg(ctx, chalk);
    // 字：先写在一层透明画布上，再“擦掉”一些小点，像粉笔写的；按秒一行一行写出来（不管这一幕多长）
    const tl = (sc.tl != null ? sc.tl : p * sc.dur) + (B.whole ? 60 : 0);      // 6.31：整页直接出来（时间往后挪 60 秒，每一行、每张卡都已经写好、贴好）
    const layer = chalkCanvas(), lc = layer.getContext('2d');
    lc.setTransform(1, 0, 0, 1, 0, 0);
    lc.clearRect(0, 0, W, H);
    boardTitle(lc, B, chalk, 1);
    const lines = B.lines, n = lines.length, cards = B.cards || [], compact = cards.length > 0;
    const lx = bx + 60, cx0 = bx + 168, maxW = bw - (cx0 - bx) - 50;
    // 先排好每一行的位置：右上角要贴“拼起来”那幅图，和它同高的几行写窄一点
    // 6.1：只写字的一页（没有卡片）行数多了字会写出纸外，整页的字按 fitK 缩小一点（boardFit）
    const fitK = compact ? 1 : boardFit(lines, B.note && B.pages !== 2);
    const { rows, yAfter } = boardRows(lines, compact, fitK);
    let y = yAfter;
    // 重点（英语的用词规律）：黄色粉笔框起来
    const hlRows = lines.map((ln, i) => (ln.hl ? i : -1)).filter(i => i >= 0);
    if (hlRows.length) {
      const i0 = hlRows[0], i1 = hlRows[hlRows.length - 1], qh = easeInOut(clamp((tl - (0.3 + i0 * 0.55)) / 0.85));
      if (qh > 0) {
        const y0b = rows[i0].y - rows[i0].size * 0.98 - 6, y1b = rows[i1].y + rows[i1].size * 0.42 + 6;
        lc.save(); lc.globalAlpha = qh * (chalk ? 0.08 : 0.5); lc.fillStyle = chalk ? BC.y : '#FFE9A6';
        rr(lc, lx - 18, y0b, bw - (lx - bx) - 28, y1b - y0b, 12); lc.fill();
        if (chalk) { lc.globalAlpha = qh; lc.strokeStyle = BC.y; lc.lineWidth = 2.5; lc.stroke(); }
        lc.restore();
      }
    }
    let strip = null;
    if (B.combo && film.combo && film.combo.pic && film.parts && rows.length >= 3) {
      const top = rows[0].y - rows[0].size * 0.85, lim = rows[3] ? rows[3].y - rows[3].size - 8 : y - 40;
      const sph = Math.min(compact ? 150 : 172 * Math.max(0.86, fitK), lim - top);
      if (sph >= 96) {
        const isz = Math.round(sph * 0.36), spw = Math.round(sph * 1.75), m = film.parts.length;
        strip = { top, ph: sph, pw: spw, isz, sx0: bx + bw - 30 - (m * isz + (m - 1) * 30 + 46 + spw), cy: top + sph / 2, t: 0.3 + 2 * 0.55 + 0.9 };
      }
    }
    lines.forEach((ln, i) => {
      const base = ln.size || 34, zk = rows[i].zk, size = base * zk;
      y = rows[i].y;
      const q = easeInOut(clamp((tl - (0.3 + i * 0.55)) / 0.85));
      const segs = ln.segs.map(([t, c, o]) => ({ t, c: BC[c] || c, z: ((o && o.size) || base) * zk, o: o || {} }));
      const famOf = g => (g.o.ipa ? IPA : CHALK);
      const total = segs.reduce((s2, g) => { setFont(lc, g.z, famOf(g)); return s2 + lc.measureText(g.t).width; }, 0);
      const lab = ln.label != null;                      // label: '' 是接着上一行写的（和上一行对齐，不写小标题）
      const x0 = lab ? cx0 : lx;
      let avail = lab ? maxW : bw - 120;
      if (strip && y + size * 0.3 > strip.top && y - size < strip.top + strip.ph) avail = Math.min(avail, strip.sx0 - 24 - x0);
      const k = total > avail ? avail / total : 1;
      if (q > 0) {
        lc.save();
        lc.beginPath(); lc.rect(x0 - 10, y - size * 1.2, (total * k + 20) * q, size * 1.6); lc.clip();
        let x = x0;
        segs.forEach(g => {
          const z = g.z * k, fam = famOf(g);
          txt(lc, g.t, x, y, { size: z, family: fam, color: g.c }); setFont(lc, z, fam);
          const gw = lc.measureText(g.t).width;
          lc.fillStyle = g.c;
          if (g.o.strike) lc.fillRect(x - 2, y - z * 0.33, gw + 4, Math.max(2, z * 0.06));
          if (g.o.under) { lc.fillRect(x, y + z * 0.14, gw, Math.max(2, z * 0.05)); if (g.o.under === 2) lc.fillRect(x, y + z * 0.26, gw, Math.max(2, z * 0.05)); }
          x += gw;
        });
        lc.restore();
        if (ln.label) { lc.save(); lc.globalAlpha = q; txt(lc, ln.label, lx, y, { size: compact ? 25 : Math.max(22, 28 * fitK), family: CHALK, color: ln.hl ? BC.y : BC.f }); lc.restore(); }
      }
    });
    y = yAfter;
    // 右上角：部分的图 + 部分的图 = 拼起来那幅画（贴在黑板上）
    if (strip) {
      const m = film.parts.length;
      let sx = strip.sx0;
      film.parts.forEach((pt, j) => {
        const qi = easeBack(clamp((tl - strip.t - j * 0.25) / 0.4));
        if (qi > 0) { ctx.save(); ctx.globalAlpha = f * Math.min(1, qi); icon(ctx, pt, sx + strip.isz / 2, strip.cy, strip.isz * qi); ctx.restore(); }
        sx += strip.isz;
        if (j < m - 1) { if (qi > 0.5) txt(lc, '+', sx + 15, strip.cy + 12, { size: 34, family: CHALK, color: BC.f, align: 'center' }); sx += 30; }
      });
      if (tl > strip.t + m * 0.25) txt(lc, '=', sx + 23, strip.cy + 13, { size: 40, family: CHALK, color: BC.w, align: 'center' });
      sx += 46;
      tapedPic(ctx, film.combo.pic, sx, strip.top, strip.pw, strip.ph, -1.6, clamp((tl - strip.t - m * 0.25 - 0.2) / 0.5), tl - strip.t - m * 0.25 - 0.2, f);
    }
    // 每个意思一张卡：画贴在黑板上（两条胶带），下面（只有一个意思时在右边）粉笔写意思、词性、例句
    let tEnd = 0.3 + n * 0.55 + 0.6;
    if (cards.length) {
      const t0 = 0.3 + n * 0.55 + 0.3 + (strip ? 1.0 : 0), top = y - 26, bottom = by + bh + (chalk ? -12 : 26), m = cards.length, gap = 28;   // 笔记纸比黑板高一点
      const cw = (bw - 80 - gap * (m - 1)) / m, avail = bottom - top - 12;
      const qd = clamp((tl - t0) / 0.6);
      if (qd > 0) { lc.save(); lc.strokeStyle = BC.f; lc.lineWidth = 2; lc.setLineDash([10, 9]); lc.beginPath(); lc.moveTo(bx + 40, top); lc.lineTo(bx + 40 + (bw - 80) * qd, top); lc.stroke(); lc.restore(); }
      // 6.1：画下面那几行字（意思、例句、中文）要多高，先量出来——例句一行放不下会分两行，画就得让出地方，不然中文会写到纸外面
      const textH = Math.max(...cards.map(cd => 42 + (cd.ex ? 38 + chalkSentenceH(lc, cd.ex, cw - 24, 25) : 0) + (cd.exzh ? 8 : 0)));
      cards.forEach((cd, j) => {
        const tc = t0 + 0.4 + j * 1.5, x0 = bx + 40 + j * (cw + gap), horiz = m === 1;
        const ph = horiz ? Math.min(210, avail - 16) : Math.max(64, Math.min(160, avail - 8 - textH));
        const pw = Math.min(horiz ? 440 : cw - 30, ph * (cd.wide ? 2.2 : 1.6));
        const px = horiz ? x0 + 16 : x0 + (cw - pw) / 2, py = top + 18;
        tapedPic(ctx, cd.pic, px, py, pw, ph, j % 2 ? 1.2 : -1.2, clamp((tl - tc) / 0.5), tl - tc, f);
        const tx = horiz ? px + pw + 34 : x0 + cw / 2, tw = horiz ? x0 + cw - tx - 10 : cw - 24, align = horiz ? 'left' : 'center';
        let ty = horiz ? py + 44 : py + ph + 42;
        chalkWrite(lc, [[m > 1 ? ['①', '②', '③'][j] + ' ' : '', BC.y, 28], [cd.ab ? cd.ab + ' ' : '', BC.b, 22], [cd.text || '', BC.y, 28], [cd.pos && !cd.ab ? '  ' + cd.pos : '', BC.f, 20]], tx, ty, tw, align, clamp((tl - tc - 0.3) / 0.6));
        ty += 38;
        if (cd.ex) ty += chalkSentence(lc, cd.ex, film.word, tx, ty, tw, align, 25, clamp((tl - tc - 0.6) / 0.9));
        if (cd.exzh) chalkWrite(lc, [[cd.exzh, BC.f, 22]], tx, ty, tw, align, clamp((tl - tc - 1.1) / 0.6));
        tEnd = tc + 1.8;
      });
    }
    // 提醒暂停：默认不写（到最后了学生知道要抄）；prefs.board.note 写了才有
    const qn = clamp((tl - tEnd - 0.3) / 0.5);
    if (qn > 0 && B.note && B.pages !== 2) {                                  // 分两页时提醒写在第二页（S.board2）
      lc.save(); lc.globalAlpha = qn;
      // 6.1：只写字的一页，提醒写在最后一行的下面（以前固定在纸的右下角，行数多了会压在最后一行上）
      const lastRow = rows[rows.length - 1];
      const nx = bx + bw - 40, ny = cards.length || !lastRow ? by + bh - 34 : Math.min(by + bh + 14, Math.max(by + bh - 34, lastRow.y + lastRow.size * 0.42 + 46));
      setFont(lc, 28, CHALK);
      const tw = lc.measureText(B.note).width;
      txt(lc, B.note, nx, ny, { size: 28, family: CHALK, color: BC.y, align: 'right' });
      lc.fillStyle = BC.y;
      rr(lc, nx - tw - 44, ny - 24, 8, 26, 3); lc.fill();
      rr(lc, nx - tw - 30, ny - 24, 8, 26, 3); lc.fill();
      lc.restore();
    }
    // 粉笔的颗粒：在字上擦掉一些小点
    if (chalk) {
      const r2 = seeded(11);
      lc.save(); lc.globalCompositeOperation = 'destination-out';
      for (let i = 0; i < 5200; i++) { lc.globalAlpha = 0.25 + r2() * 0.5; lc.fillRect(bx + r2() * bw, by + r2() * bh, 1.3, 1.3); }
      lc.restore();
    }
    ctx.globalAlpha = f;
    ctx.drawImage(layer, 0, 0);
    ctx.globalAlpha = 1;
  };
  // 6.1：总结第二页（内容多、一页放不下时才有）——每个意思一行：左边贴那幅画（例句的动画，没有就用意思那幅），
  // 右边写“① v. 生产、制造”、例句（本词标重点色）、中文。一行一行出来；视频停在这一页上
  S.board2 = (ctx, film, p, sc) => {
    const B = film.board, chalk = B.style === 'chalk';
    BC = chalk ? CHALK_C : NOTE_C;
    const f = Math.min(1, span(p * sc.dur, 0, 0.4));
    const bx = 40, by = 34, bw = W - 80, bh = H - 104;
    boardBg(ctx, chalk);
    const tl = (sc.tl != null ? sc.tl : p * sc.dur) + (B.whole ? 60 : 0);      // 6.31：整页直接出来（时间往后挪 60 秒，每一行、每张卡都已经写好、贴好）
    const layer = chalkCanvas(), lc = layer.getContext('2d');
    lc.setTransform(1, 0, 0, 1, 0, 0);
    lc.clearRect(0, 0, W, H);
    boardTitle(lc, B, chalk, 2);
    const cards = B.cards2 || [], m = cards.length;
    // 第一行：单词 + “每个意思一句话”
    const q0 = easeInOut(clamp((tl - 0.25) / 0.7));
    if (q0 > 0) {
      lc.save(); lc.beginPath(); lc.rect(bx + 50, by + 66, (bw - 100) * q0, 70); lc.clip();
      txt(lc, film.word, bx + 60, by + 116, { size: 54, family: CHALK, color: BC.y });
      setFont(lc, 54, CHALK);
      txt(lc, m > 1 ? '每个意思一句话' : '一句话记住它', bx + 60 + lc.measureText(film.word).width + 26, by + 114, { size: 26, family: CHALK, color: BC.f });
      lc.restore();
    }
    if (B.note) {                                                           // 提醒暂停（prefs.board.note 写了才有）：第二页写在右上角，不和下面几行抢地方
      const qn = clamp((tl - (0.9 + m * 1.7) - 0.6) / 0.5);
      if (qn > 0) {
        lc.save(); lc.globalAlpha = qn;
        const nx = bx + bw - 44, ny = by + 112;
        setFont(lc, 28, CHALK);
        const nw = lc.measureText(B.note).width;
        txt(lc, B.note, nx, ny, { size: 28, family: CHALK, color: BC.y, align: 'right' });
        lc.fillStyle = BC.y;
        rr(lc, nx - nw - 44, ny - 24, 8, 26, 3); lc.fill();
        rr(lc, nx - nw - 30, ny - 24, 8, 26, 3); lc.fill();
        lc.restore();
      }
    }
    const top = by + 138, bottom = by + bh + (chalk ? -10 : 22);
    const rh = Math.min(m === 1 ? 300 : 250, (bottom - top) / Math.max(1, m)), y0 = top + (bottom - top - rh * m) / 2 * (m === 1 ? 0.4 : 0);
    const ph = Math.min(m === 1 ? 240 : 200, rh - 30), pwMax = Math.min(430, ph * 2.2);
    cards.forEach((cd, j) => {
      const tc = 0.9 + j * 1.7, ry = y0 + j * rh;
      const qd = clamp((tl - tc + 0.2) / 0.5);
      if (qd > 0) { lc.save(); lc.strokeStyle = BC.f; lc.lineWidth = 2; lc.setLineDash([10, 9]); lc.beginPath(); lc.moveTo(bx + 40, ry); lc.lineTo(bx + 40 + (bw - 80) * qd, ry); lc.stroke(); lc.restore(); }
      const pw = Math.min(pwMax, ph * (cd.wide ? 2.2 : 1.6));
      const px = bx + 64 + (pwMax - pw) / 2, py = ry + (rh - ph) / 2 + 4;
      tapedPic(ctx, cd.pic, px, py, pw, ph, j % 2 ? 1.2 : -1.2, clamp((tl - tc) / 0.5), tl - tc, f);
      const tx = bx + 64 + pwMax + 46, tw = bx + bw - 50 - tx;
      // 三行字在这一行里上下居中：意思 / 例句（这一页地方宽，例句不缩得太小，放不下就分两行）/ 中文。三个意思时字小一号
      const tz = m >= 3 ? 32 : 36, ez = m >= 3 ? 28 : 30, eMin = m >= 3 ? 23 : 26, zz = m >= 3 ? 23 : 26;
      const exH = cd.ex ? chalkSentenceH(lc, cd.ex, tw, ez, eMin) : 0;
      const blockH = tz + 4 + (cd.ex ? exH + 4 : 0) + (cd.exzh ? zz + 6 : 0);
      let ty = ry + (rh - blockH) / 2 + tz;
      chalkWrite(lc, [[m > 1 ? ['①', '②', '③'][j] + ' ' : '', BC.y, tz], [cd.ab ? cd.ab + ' ' : '', BC.b, tz - 8], [cd.text || '', BC.y, tz], [cd.pos && !cd.ab ? '  ' + cd.pos : '', BC.f, 22]], tx, ty, tw, 'left', clamp((tl - tc - 0.3) / 0.6));
      ty += ez + 14;
      if (cd.ex) ty += chalkSentence(lc, cd.ex, film.word, tx, ty, tw, 'left', ez, clamp((tl - tc - 0.6) / 0.9), eMin) + 4;
      if (cd.exzh) chalkWrite(lc, [[cd.exzh, BC.f, zz]], tx, ty, tw, 'left', clamp((tl - tc - 1.1) / 0.6));
    });
    if (chalk) {
      const r2 = seeded(11);
      lc.save(); lc.globalCompositeOperation = 'destination-out';
      for (let i = 0; i < 5200; i++) { lc.globalAlpha = 0.25 + r2() * 0.5; lc.fillRect(bx + r2() * bw, by + r2() * bh, 1.3, 1.3); }
      lc.restore();
    }
    ctx.globalAlpha = f;
    ctx.drawImage(layer, 0, 0);
    ctx.globalAlpha = 1;
  };
  // 一幅画用两条胶带贴在黑板上（稍微歪一点，贴上去时轻轻弹一下）
  function tapedPic(ctx, pic, px, py, pw, ph, deg, qp, lt, f) {
    if (qp <= 0) return;
    ctx.save();
    ctx.globalAlpha = f * Math.min(1, qp * 1.5);
    ctx.translate(px + pw / 2, py + ph / 2);
    ctx.rotate(deg * Math.PI / 180);
    const sk = 0.86 + 0.14 * easeBack(qp);
    ctx.scale(sk, sk);
    drawPic(ctx, pic, -pw / 2, -ph / 2, pw, ph, { q: qp, lt: Math.max(0, lt) });
    ctx.fillStyle = BC === CHALK_C ? 'rgba(236,226,192,.88)' : 'rgba(255,206,120,.8)';     // 黑板上米色胶带；笔记纸上黄色和纸胶带
    [[-pw / 2 + 16, -ph / 2 + 2, -0.55], [pw / 2 - 16, -ph / 2 + 2, 0.55]].forEach(([tx, ty, r]) => { ctx.save(); ctx.translate(tx, ty); ctx.rotate(r); ctx.fillRect(-26, -8, 52, 16); ctx.restore(); });
    ctx.restore();
  }
  // 一行粉笔字（几段不同颜色、大小：[文字, 颜色, 字号]），按 q 从左往右写出来；align: left / center；放不下就整体缩小
  function chalkWrite(lc, segs, x, y, maxW, align, q) {
    segs = segs.filter(sg => sg[0]);
    if (q <= 0 || !segs.length) return;
    let total = segs.reduce((acc, [t, , z]) => { setFont(lc, z, CHALK); return acc + lc.measureText(t).width; }, 0);
    const k = total > maxW ? maxW / total : 1;
    total *= k;
    const x0 = align === 'center' ? x - total / 2 : x, zmax = Math.max(...segs.map(sg => sg[2])) * k;
    lc.save();
    lc.beginPath(); lc.rect(x0 - 6, y - zmax * 1.2, (total + 12) * q, zmax * 1.6); lc.clip();
    let xx = x0;
    segs.forEach(([t, c, z]) => { txt(lc, t, xx, y, { size: z * k, family: CHALK, color: c }); setFont(lc, z * k, CHALK); xx += lc.measureText(t).width; });
    lc.restore();
  }
  // 粉笔写的例句：本词写成黄色；太长先缩小，还放不下就分两行。返回占了多高
  // 例句怎么排：太长先缩小（最小 19），还放不下就从中间的空格分成两行
  function chalkSentenceRows(lc, str, maxW, size, minZ) {
    let z = size;
    setFont(lc, z, CHALK);
    while (z > (minZ || 19) && lc.measureText(str).width > maxW) { z -= 1; setFont(lc, z, CHALK); }
    let rows = [str];
    if (lc.measureText(str).width > maxW) {
      const mid = str.length / 2;
      let cut = -1;
      for (let i = 0; i < str.length; i++) if (str[i] === ' ' && (cut < 0 || Math.abs(i - mid) < Math.abs(cut - mid))) cut = i;
      if (cut > 0) rows = [str.slice(0, cut), str.slice(cut + 1)];
    }
    return { z, rows };
  }
  const chalkSentenceH = (lc, str, maxW, size, minZ) => { const r = chalkSentenceRows(lc, String(str || ''), maxW, size, minZ); return r.rows.length * r.z * 1.3 + 6; };
  function chalkSentence(lc, str, word, x, y, maxW, align, size, q, minZ) {
    const stem = String(word || '').toLowerCase().replace(/(e|y)$/, '');
    const hit = tk => stem.length >= 3 && /[A-Za-z]/.test(tk) && tk.toLowerCase().startsWith(stem);
    const { z, rows } = chalkSentenceRows(lc, str, maxW, size, minZ);
    rows.forEach((row, r) => {
      const segs = (row.match(/[A-Za-z'’-]+|[^A-Za-z'’-]+/g) || []).map(tk => [tk, hit(tk) ? BC.y : BC.w, z]);
      chalkWrite(lc, segs, x, y + r * z * 1.3, maxW, align, clamp(q * rows.length - r));
    });
    return rows.length * z * 1.3 + 6;
  }

  // 一幕比原来长（配音说得久）：动画照原来的速度走完，停在最后的样子等配音，最后 0.45 秒再淡出；
  // 带 marks 的一幕（等式、来历、意思变化、小黑板）按真实的秒数走，每一项在配音说到它的时候出来
  function sceneAt(film, t) {
    t = clamp(t, 0, film.total);
    const last = film.scenes[film.scenes.length - 1];
    for (const s of film.scenes) {
      if (!(t < s.t0 + s.dur || s === last)) continue;
      const tl = t - s.t0, base = s.base || s.dur;
      let p;
      if (s.marks || base >= s.dur - 1e-6) p = tl / s.dur;
      else {
        const hold = Math.max(0, base - 0.45);
        p = tl < hold ? tl / base : tl < s.dur - 0.45 ? hold / base : (hold + (tl - (s.dur - 0.45))) / base;
      }
      return { s, p: clamp(p), tl };
    }
    return { s: film.scenes[0], p: 0, tl: 0 };
  }
  // 6.25：view = {x, y, w, h}（画布像素）：整个画布先铺背景，动画画在这一块里（1080p 视频下面留一条字幕栏，字幕不挡画面）
  function draw(ctx, film, t, view) {
    rcFrame++;
    ctx.save();
    ctx.setTransform(ctx.canvas.width / W, 0, 0, ctx.canvas.height / H, 0, 0);
    ctx.globalAlpha = 1;
    background(ctx);
    if (view) ctx.setTransform(view.w / W, 0, 0, view.h / H, view.x, view.y);
    const { s, p, tl } = sceneAt(film, t);
    const vs = Object.assign({}, s, { dur: s.marks ? s.dur : (s.base || s.dur), tl });
    SFX_NOW = t; SFX_SCENE = s.id;
    try { (S[s.id] || (() => {}))(ctx, film, p, vs); } catch (e) { /* 画坏了一帧也不要停 */ console.error(e); }
    ctx.restore();
  }

  // 6.25：字幕（用户：“下面要有字幕；读英文句子的时候，由于上面本来就有句子了，这时候不需要有字幕”“只要画面里面有字的就不用加了，没有的才加”）。
  // cues = [{t0, t1, text}]（render.py 按配音切好、挑掉画面上已经写着的），band = {y, h}：画在最下面那一条里，深色字、白色描边
  function subtitle(ctx, cues, t, band) {
    if (!Array.isArray(cues) || !band) return;
    const c = cues.find(q => t >= q.t0 && t < q.t1);
    if (!c) return;
    const a = Math.min(1, (t - c.t0) / 0.1, (c.t1 - t) / 0.1);
    if (a <= 0) return;
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
    const cw = ctx.canvas.width, maxW = cw * 0.88;
    let size = Math.round(band.h * 0.46), lines = [String(c.text)];
    ctx.font = '600 ' + size + 'px ' + ZH;
    if (ctx.measureText(lines[0]).width > maxW) {
      const tx = lines[0], mid = tx.length / 2;
      let cut = -1;
      for (let d = 0; d < mid; d++) for (const j of [Math.round(mid + d), Math.round(mid - d)]) if (cut < 0 && /[ ，、；：,;]/.test(tx[j] || '')) cut = j;
      if (cut < 0) cut = Math.round(mid);
      lines = [tx.slice(0, cut + (/[ ]/.test(tx[cut]) ? 0 : 1)).trim(), tx.slice(cut + 1).trim()];
      size = Math.round(band.h * 0.36); ctx.font = '600 ' + size + 'px ' + ZH;
    }
    ctx.globalAlpha = a; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.lineJoin = 'round';
    const lh = size * 1.22, y0 = band.y + band.h / 2 - (lines.length - 1) * lh / 2;
    lines.forEach((ln, k) => {
      ctx.lineWidth = Math.max(4, size * 0.2); ctx.strokeStyle = 'rgba(255,255,255,0.96)'; ctx.strokeText(ln, cw / 2, y0 + k * lh);
      ctx.fillStyle = '#1F2A37'; ctx.fillText(ln, cw / 2, y0 + k * lh);
    });
    ctx.restore();
  }
  // 配好音以后按配音调整每一幕的长短：timing = [{ dur, marks }]（和 film.scenes 一一对应）
  function retime(film, timing) {
    film.scenes.forEach((s, i) => {
      const x = timing[i];
      if (!x) return;
      if (!s.base) s.base = s.dur;
      if (x.dur) s.dur = Math.max(s.base * (x.marks ? 0.6 : 1), x.dur);
      if (x.marks) s.marks = x.marks.slice();
      if (x.groups) s.groups = x.groups.slice();
      if (x.ends) s.ends = x.ends.slice();                 // 5.11：每一句说完的秒数、每一句的字（按词出东西）
      if (x.texts) s.texts = x.texts.slice();
    });
    let t0 = 0;
    for (const s of film.scenes) { s.t0 = t0; t0 += s.dur; }
    film.total = t0;
    return film;
  }

  // ---------------------------------------------------------------- 6.6：音变的原因单独一幕“为什么 p 会变成 f？”
  // 用户：“为什么要这样变最好也说一下，p-f 为什么可以，是发音相似还是什么原因，最好能说明白……然后再举一些例子就更好”。
  // 总表音变后面的原因（维护技能 yuanyin.py 写的，写法两边一起改）：
  //   “；原因：〈总说：英语属于日耳曼语……这叫格林定律，拉丁语没有这样变〉；发音：念 p，…，念 f，…，两个音…，所以 p 容易念成 f；起因：…；例子：拉丁语 piscis 和 fish、…”
  // 画面从上到下：标题“为什么 p 会变成 f？”和右上角格林定律三对（这一对描边）、总说 → 两块嘴的剖面图（念 p、念 f，会动）→ 黄条结论 → 起因 → 例子；一句配音出一块
  function whyOf(why) {
    const out = { gen: '', fa: '', qi: '', li: '' };
    let cur = 'gen';
    splitTop(String(why || ''), '；').forEach(s0 => {
      const s = String(s0).trim();
      if (!s) return;
      const m = /^(发音|起因|例子)[：:]\s*([\s\S]*)$/.exec(s);
      if (m) { cur = { 发音: 'fa', 起因: 'qi', 例子: 'li' }[m[1]]; out[cur] = m[2].trim(); }
      else out[cur] = out[cur] ? out[cur] + '；' + s : s;
    });
    return out;
  }
  const YB = { p: { at: 'lip', stop: 1 }, b: { at: 'lip', stop: 1, voice: 1 }, bh: { at: 'lip', stop: 1, voice: 1, asp: 1 }, f: { at: 'lab' },
    t: { at: 'tip', stop: 1 }, d: { at: 'tip', stop: 1, voice: 1 }, dh: { at: 'tip', stop: 1, voice: 1, asp: 1 }, th: { at: 'dent' },
    k: { at: 'back', stop: 1 }, g: { at: 'back', stop: 1, voice: 1 }, gh: { at: 'back', stop: 1, voice: 1, asp: 1 }, h: { at: 'back' } };
  const YB_AT = { lip: [193, 91], lab: [184, 90], tip: [170, 69], dent: [186, 92], back: [92, 57] };     // 堵住 / 留缝的地方（画虚线圈）
  const YB_CAT = { p: 1, t: 1, k: 1, b: 2, d: 2, g: 2, bh: 3, dh: 3, gh: 3 };
  const YB_PLACE = { p: '嘴唇', b: '嘴唇', bh: '嘴唇', t: '舌尖', d: '舌尖', dh: '舌尖', k: '舌根', g: '舌根', gh: '舌根' };
  const YB_GRIMM = { 1: [['p', 'f'], ['t', 'th'], ['k', 'h']], 2: [['b', 'p'], ['d', 't'], ['g', 'k']], 3: [['bh', 'b'], ['dh', 'd'], ['gh', 'g']] };
  const YB_LA = { p: ['p'], t: ['t'], k: ['c', 'k', 'q'], d: ['d'], g: ['g'], dh: ['th', 'f', 'd'], bh: ['ph', 'f', 'b'], b: ['b'] };
  const YB_EN = { f: ['f'], th: ['th'], h: ['gh', 'h'], t: ['t'], k: ['k', 'c', 'q'], d: ['d'], b: ['b'], p: ['p'], g: ['g'] };
  const YB_FROM = '#C2571A', YB_TO = '#1E7B3C';
  function yinbianOf(sh) {
    if (!sh || !sh.why) return null;
    const wy = sh.wy || whyOf(sh.why);
    if (!wy.fa) return null;
    const m = /^念\s*([a-z]+)，([\s\S]*?)，念\s*([a-z]+)，([\s\S]*?)，(两个音[\s\S]*?)，所以\s*[a-z]+\s*容易念成\s*[a-z]+(?:，另外\s*([\s\S]*))?$/.exec(wy.fa);
    if (!m) return null;
    let lang = '';
    const li = String(wy.li || '').split('、').map(x => {
      const q = /^(?:(拉丁语|希腊语|法语)\s*)?([A-Za-z][A-Za-z\-]*)\s*和\s*([A-Za-z][A-Za-z\-]*)$/.exec(x.trim());
      if (!q) return null;
      if (q[1]) lang = q[1];
      return { lang, la: q[2], en: q[3] };
    }).filter(Boolean);
    const e2 = /^([a-z]+)\s*和\s*([a-z]+)/.exec(m[6] || '');
    const o = { a: m[1], A: m[2], b: m[3], B: m[4], C: m[5], extra: m[6] || '', a2: e2 ? e2[1] : '', b2: e2 ? e2[2] : '', gen: wy.gen, qi: wy.qi, li };
    o.cat = YB_CAT[o.a] || 1;
    o.steps = ['gen', 'a', 'b', 'c'].concat(o.qi ? ['qi'] : [], li.length ? ['li'] : []);
    return o;
  }
  function along(pts, u) {
    const seg = [];
    let L = 0;
    for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); seg.push(d); L += d; }
    let r = clamp(u) * L;
    for (let i = 0; i < seg.length; i++) {
      if (r <= seg[i] || i === seg.length - 1) { const k = seg[i] ? Math.min(1, r / seg[i]) : 0; return [lerp(pts[i][0], pts[i + 1][0], k), lerp(pts[i][1], pts[i + 1][1], k)]; }
      r -= seg[i];
    }
    return pts[pts.length - 1];
  }
  // 嘴的剖面图（朝右）：脸的侧影、上腭、喉咙、舌头、门牙、嘴唇；p 嘴唇闭紧再一下子放开（放开时小线一炸），f 下嘴唇收进去贴着上牙、气从缝里一串串擦出来，
  // t 舌尖顶住上牙床、th 舌尖在上下牙中间，k 舌根顶住软腭、h 舌根抬起不顶住；声带振动的（b、d、g）喉咙前面几道弧线一跳一跳，带一股气的（bh、dh）放开后嘴前一团气
  // view：'front' 只画嘴前半截、放大（p、f、t、th：嘴唇、牙看得清）；'full' 整个剖面（k、h 在舌根；b、d、g 要看到喉咙里的声带）
  function mouth(ctx, X, Y, Wd, Ht, snd, lt, col, view) {
    const A = YB[snd] || YB.p, VB = view === 'front' ? [92, 22, 168, 150] : [16, 0, 244, 210], s = Math.min(Wd / VB[2], Ht / VB[3]), t = Math.max(0, lt || 0);
    const cyc = 1.8, ph = (t % cyc) / cyc;
    const rel = A.stop ? clamp((ph - 0.55) / 0.12) : 1;                          // 堵住（0）→ 放开（1）
    ctx.save();
    ctx.translate(X + (Wd - VB[2] * s) / 2 - VB[0] * s, Y + (Ht - VB[3] * s) / 2 - VB[1] * s); ctx.scale(s, s);
    ctx.beginPath(); ctx.rect(VB[0], VB[1], VB[2], VB[3]); ctx.clip();
    ctx.lineJoin = 'round'; ctx.lineCap = 'round';
    const SKL = '#B9826A';
    ctx.beginPath();
    ctx.moveTo(20, 0); ctx.lineTo(150, 0);
    ctx.bezierCurveTo(176, 2, 198, 22, 214, 46);
    ctx.bezierCurveTo(218, 54, 206, 60, 194, 60);
    ctx.bezierCurveTo(201, 74, 203, 102, 197, 118);
    ctx.bezierCurveTo(204, 136, 195, 152, 178, 158);
    ctx.bezierCurveTo(160, 166, 140, 166, 130, 170);
    ctx.lineTo(126, 210); ctx.lineTo(20, 210); ctx.closePath();
    ctx.fillStyle = '#F6DCCB'; ctx.fill(); ctx.lineWidth = 2.4; ctx.strokeStyle = SKL; ctx.stroke();
    ctx.beginPath();                                                             // 嘴里：上面硬腭、软腭，后面喉咙，下面口底
    ctx.moveTo(197, 90); ctx.lineTo(186, 70); ctx.quadraticCurveTo(178, 63, 168, 64);
    ctx.bezierCurveTo(150, 50, 122, 44, 100, 48);
    ctx.quadraticCurveTo(86, 51, 80, 66);
    ctx.quadraticCurveTo(70, 74, 66, 94);
    ctx.lineTo(64, 210); ctx.lineTo(100, 210);
    ctx.quadraticCurveTo(104, 172, 128, 156); ctx.quadraticCurveTo(166, 134, 176, 112); ctx.lineTo(197, 102); ctx.closePath();
    ctx.fillStyle = '#7A2E3A'; ctx.fill();
    ctx.beginPath(); ctx.moveTo(186, 70); ctx.quadraticCurveTo(178, 63, 168, 64); ctx.bezierCurveTo(150, 50, 122, 44, 100, 48); ctx.quadraticCurveTo(86, 51, 80, 66);
    ctx.lineWidth = 5; ctx.strokeStyle = '#E9B9A6'; ctx.stroke();
    let D = [112, 86], B = [148, 90], T = [172, 98];                             // 舌头：舌根 D、舌面 B、舌尖 T
    if (A.at === 'tip') { const c = 1 - rel; B = [150, lerp(88, 78, c)]; T = [lerp(172, 169, c), lerp(86, 68, c)]; }
    else if (A.at === 'dent') { B = [154, 89]; T = [187, 93]; }
    else if (A.at === 'back') { const c = A.stop ? 1 - rel : 0; D = [93, A.stop ? lerp(66, 54, c) : 62]; B = [140, 86]; }
    ctx.beginPath();
    ctx.moveTo(100, 210);
    ctx.quadraticCurveTo(80, 172, 82, 122);
    ctx.quadraticCurveTo(83, D[1] + 4, D[0], D[1]);
    ctx.quadraticCurveTo((D[0] + B[0]) / 2, Math.min(D[1], B[1]) - 4, B[0], B[1]);
    ctx.quadraticCurveTo((B[0] + T[0]) / 2, Math.min(B[1], T[1]) - 2, T[0], T[1]);
    ctx.quadraticCurveTo(T[0] + 5, T[1] + 7, T[0] - 6, T[1] + 13);
    ctx.quadraticCurveTo(152, 134, 128, 156);
    ctx.quadraticCurveTo(104, 172, 100, 210); ctx.closePath();
    ctx.fillStyle = '#EC8C98'; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = '#B04A58'; ctx.stroke();
    const tooth = (x, y, w, h) => { rr(ctx, x, y, w, h, 3); ctx.fillStyle = '#FFFFFF'; ctx.fill(); ctx.lineWidth = 1.6; ctx.strokeStyle = '#9AA3AD'; ctx.stroke(); };
    tooth(177, 69, 10, 22); tooth(174, 95, 10, 18);                              // 上门牙、下门牙
    const lift = A.at === 'lab' ? -5 : 0, gap = A.at === 'lip' ? 8 * rel : A.at === 'lab' ? 0 : 7;
    const ldx = A.at === 'lab' ? -10 : 0, ldy = A.at === 'lab' ? -3 : gap;
    ctx.lineWidth = 2.2; ctx.strokeStyle = SKL;
    ctx.beginPath(); ctx.moveTo(182, 61); ctx.quadraticCurveTo(207, 64, 204, 83 + lift); ctx.quadraticCurveTo(203, 91 + lift, 192, 91 + lift); ctx.lineTo(184, 90 + lift); ctx.quadraticCurveTo(178, 76, 182, 61); ctx.closePath();
    ctx.fillStyle = '#E39A8E'; ctx.fill(); ctx.stroke();
    ctx.save(); ctx.translate(ldx, ldy);
    ctx.beginPath(); ctx.moveTo(184, 92); ctx.lineTo(193, 92); ctx.quadraticCurveTo(206, 95, 204, 108); ctx.quadraticCurveTo(200, 121, 182, 119); ctx.quadraticCurveTo(177, 105, 184, 92); ctx.closePath();
    ctx.fillStyle = '#E39A8E'; ctx.fill(); ctx.stroke(); ctx.restore();
    const P0 = YB_AT[A.at];
    ctx.save(); ctx.setLineDash([5, 4]); ctx.lineWidth = 2.6; ctx.strokeStyle = col;
    ctx.beginPath(); ctx.arc(P0[0], P0[1], 17, 0, Math.PI * 2); ctx.stroke(); ctx.restore();
    ctx.strokeStyle = '#3F7FD6'; ctx.lineWidth = 3;
    if (!A.stop) {                                                               // 擦出来：一串小短线从缝里不停地往外走，缝那儿几道小折线
      const path = A.at === 'back' ? [[92, 58], [122, 56], [160, 70], [198, 95], [252, 95]] : [[P0[0] + 2, P0[1]], [216, P0[1] + 1], [254, P0[1] + 2]];
      for (let k = 0; k < 7; k++) {
        const u = (k / 7 + t * 0.6) % 1, a = along(path, u), b = along(path, Math.min(1, u + 0.05));
        ctx.globalAlpha = 0.35 + 0.65 * Math.sin(Math.PI * u);
        ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke();
      }
      ctx.globalAlpha = 1;
      const zx = A.at === 'back' ? 98 : P0[0] + 12, zy = A.at === 'back' ? 52 : P0[1] - 14;
      ctx.lineWidth = 2; ctx.beginPath();
      for (let k = 0; k < 5; k++) ctx.lineTo(zx + k * 4, zy + (k % 2 ? -3 : 3) + Math.sin(t * 30) * 1.2);
      ctx.stroke();
    } else if (ph >= 0.55 && ph < 0.9) {                                         // 放开的一下：小线往外一炸，一股气冲出嘴
      const q = clamp((ph - 0.55) / 0.3), B0 = A.at === 'back' ? [94, 62] : A.at === 'tip' ? [172, 74] : [199, 95];
      ctx.globalAlpha = 1 - q * 0.6;
      for (let k = -2; k <= 2; k++) {
        const an = k * 0.42 + (A.at === 'lip' ? 0 : -0.15);
        ctx.beginPath(); ctx.moveTo(B0[0] + Math.cos(an) * (6 + 10 * q), B0[1] + Math.sin(an) * (6 + 10 * q)); ctx.lineTo(B0[0] + Math.cos(an) * (14 + 18 * q), B0[1] + Math.sin(an) * (14 + 18 * q)); ctx.stroke();
      }
      const ox = 208 + 34 * q; ctx.beginPath(); ctx.moveTo(ox, 95); ctx.lineTo(ox + 14, 95); ctx.stroke();
      ctx.globalAlpha = 1;
    }
    if (A.asp && ph >= 0.6) {                                                    // 带一股气：放开以后嘴前面一团气
      const q = clamp((ph - 0.6) / 0.35);
      ctx.fillStyle = 'rgba(120,150,200,' + (0.45 * (1 - q)).toFixed(3) + ')';
      [[0, 0, 7], [9, -5, 6], [10, 5, 6]].forEach(([dx, dy, r]) => { ctx.beginPath(); ctx.arc(214 + 30 * q + dx, 95 + dy, r + 6 * q, 0, Math.PI * 2); ctx.fill(); });
    }
    if (A.voice) {                                                               // 声带振动：喉咙前面几道一跳一跳的弧线
      const v = 0.5 + 0.5 * Math.sin(t * 28);
      ctx.strokeStyle = col; ctx.lineWidth = 2.6;
      for (let k = 0; k < 3; k++) { ctx.globalAlpha = 0.35 + 0.65 * v; ctx.beginPath(); ctx.arc(128, 194, 8 + k * 7, -0.75, 0.75); ctx.stroke(); }
      ctx.globalAlpha = 1;
      ctx.beginPath(); for (let k = 0; k < 6; k++) ctx.lineTo(70 + k * 5, 194 + (k % 2 ? -4 : 4) * v); ctx.strokeStyle = '#F2C94C'; ctx.stroke();
    }
    ctx.restore();
  }
  function firstOf(w, opts) {
    let best = null;
    const lw = String(w).toLowerCase();
    (opts || []).forEach(o => { const i = lw.indexOf(o); if (i >= 0 && (!best || i < best[0] || (i === best[0] && o.length > best[1]))) best = [i, o.length]; });
    return best;
  }
  function exMark(la, en, pairs) {
    for (const [a, b] of pairs) { const x = firstOf(la, YB_LA[a] || [a]), y = firstOf(en, YB_EN[b] || [b]); if (x && y) return { la: x, en: y }; }
    return { la: null, en: null };
  }
  // 一个词，变了的那几个字母上色、下面一道线；返回宽
  function hiWord(ctx, w, mk, x, y, size, col, hcol, weight) {
    setFont(ctx, size, EN, weight || 'bold');
    ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
    const parts = mk ? [w.slice(0, mk[0]), w.slice(mk[0], mk[0] + mk[1]), w.slice(mk[0] + mk[1])] : [w, '', ''];
    let cx = x;
    parts.forEach((s1, k) => {
      if (!s1) return;
      ctx.fillStyle = k === 1 ? hcol : col; ctx.fillText(s1, cx, y);
      const ww = ctx.measureText(s1).width;
      if (k === 1) ctx.fillRect(cx, y + size * 0.14, ww, Math.max(2, size * 0.08));
      cx += ww;
    });
    return cx - x;
  }
  S.yinbian = (ctx, film, p, sc) => {
    const part = film.parts[sc.i], sh = part && part.memo ? part.memo.shift : null, Y = sh ? yinbianOf(sh) : null;
    if (!Y) return;
    const f = fadeOf(sc, p), tl = sc.tl != null ? sc.tl : p * sc.dur;
    const mk = sc.marks && sc.marks.length >= Y.steps.length ? sc.marks : null;
    const FB = { gen: 0.03, a: 0.2, b: 0.34, c: 0.48, qi: 0.6, li: 0.8 }, T = {};
    Y.steps.forEach((k, j) => { T[k] = mk ? mk[j] : FB[k] * sc.dur; });
    const on = k => (T[k] == null ? 0 : clamp((tl - T[k] + 0.12) / 0.45));
    const up = (1 - easeOut(span(p, 0, 0.18))) * 24;
    const x0 = 56, y0 = 104 + up, w = W - 112, h = 592, X = x0 + 40, R = x0 + w - 36;
    ctx.globalAlpha = f;
    ctx.save();
    ctx.shadowColor = 'rgba(60,50,20,.10)'; ctx.shadowBlur = 24; ctx.shadowOffsetY = 6;
    rr(ctx, x0, y0, w, h, 24); ctx.fillStyle = C.card; ctx.fill();
    ctx.restore();
    ctx.globalAlpha = f;
    rr(ctx, x0, y0, w, h, 24); ctx.lineWidth = 2; ctx.strokeStyle = C.line; ctx.stroke();
    rr(ctx, x0, y0, 12, h, 6); ctx.fillStyle = part.color; ctx.fill();
    // 标题：为什么 p 会变成 f？（p 橙色、f 绿色，和卡片上“音变 p → f”的牌子一样）
    let tx = X;
    const ty = y0 + 60;
    const piece = (s1, fam, size, color) => { setFont(ctx, size, fam, 'bold'); ctx.fillStyle = color; ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic'; ctx.fillText(s1, tx, ty); tx += ctx.measureText(s1).width; };
    piece('为什么 ', ZH, 40, C.ink); piece(Y.a, EN, 50, YB_FROM); piece(' 会变成 ', ZH, 40, C.ink); piece(Y.b, EN, 50, YB_TO); piece('？', ZH, 40, C.ink);
    // 右上角：格林定律三对，这一对描边（两对的把另一对也描上）
    const pairs = [[Y.a, Y.b]].concat(Y.a2 ? [[Y.a2, Y.b2]] : []);
    const list = YB_GRIMM[Y.cat].slice();
    if (Y.a2 && YB_CAT[Y.a2] !== Y.cat) list.push([Y.a2, Y.b2]);
    ctx.globalAlpha = f * on('gen');
    const cws = list.map(([a, b]) => { setFont(ctx, 24, EN, 'bold'); const w1 = ctx.measureText(a + ' → ' + b).width; setFont(ctx, 17, ZH, 'bold'); return w1 + ctx.measureText(YB_PLACE[a] || '').width + 34; });
    let cx = R - cws.reduce((s1, v) => s1 + v + 10, 0) + 10;
    setFont(ctx, 18, ZH, 'bold');
    txt(ctx, '格林定律', cx - ctx.measureText('格林定律').width - 12, ty - 10, { size: 18, weight: 'bold', color: '#8A6A2A', base: 'middle' });
    list.forEach(([a, b], k) => {
      const cw = cws[k], hit = pairs.some(q => q[0] === a), cy = ty - 30;
      rr(ctx, cx, cy, cw, 40, 12); ctx.fillStyle = hit ? tint(part.color, 0.84) : '#F4F1EA'; ctx.fill();
      if (hit) { ctx.lineWidth = 2.5; ctx.strokeStyle = part.color; ctx.stroke(); }
      txt(ctx, YB_PLACE[a] || '', cx + 12, cy + 21, { size: 17, weight: 'bold', color: hit ? part.color : C.faint, base: 'middle' });
      setFont(ctx, 17, ZH, 'bold');
      const pw2 = ctx.measureText(YB_PLACE[a] || '').width;
      txt(ctx, a + ' → ' + b, cx + 20 + pw2, cy + 21, { size: 24, family: EN, weight: 'bold', color: hit ? C.ink : C.faint, base: 'middle' });
      cx += cw + 10;
    });
    // 总说
    setFont(ctx, 22, ZH, 'normal');
    const gl = wrap(ctx, Y.gen, R - X, 2);
    gl.forEach((ln, j) => txt(ctx, ln, X, y0 + 102 + j * 31, { size: 22, color: C.soft }));
    // 两块嘴的剖面图：念 p、念 f
    const pTop = y0 + 102 + (gl.length - 1) * 31 + 24, pH = Y.extra ? 176 : 200, gapX = 56, pw = (R - X - gapX) / 2;
    const view = [Y.a, Y.b].some(x => { const q = YB[x] || {}; return q.voice || q.asp || q.at === 'back'; }) ? 'full' : 'front';   // 两块用同一个比例
    [[Y.a, Y.A, 'a', YB_FROM], [Y.b, Y.B, 'b', YB_TO]].forEach(([snd, desc, key, scol], k) => {
      const a0 = on(key);
      if (a0 <= 0) return;
      const px = X + k * (pw + gapX);
      ctx.globalAlpha = f * a0;
      rr(ctx, px, pTop, pw, pH, 18); ctx.fillStyle = '#F8F5EE'; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = '#E4DCCB'; ctx.stroke();
      mouth(ctx, px + 8, pTop + 8, 214, pH - 16, snd, tl - T[key], scol, view);
      const lx = px + 232;
      txt(ctx, '念', lx, pTop + 56, { size: 30, weight: 'bold', color: C.ink });
      setFont(ctx, 30, ZH, 'bold');
      txt(ctx, snd, lx + ctx.measureText('念 ').width, pTop + 58, { size: 50, family: EN, weight: 'bold', color: scol });
      setFont(ctx, 22, ZH, 'normal');
      wrap(ctx, desc, px + pw - lx - 16, 4).forEach((ln, j) => txt(ctx, ln, lx, pTop + 98 + j * 31, { size: 22, color: C.ink }));
    });
    if (on('b') > 0) { ctx.globalAlpha = f * on('b'); txt(ctx, '→', X + pw + gapX / 2, pTop + pH / 2, { size: 40, weight: 'bold', color: '#B69D62', align: 'center', base: 'middle' }); }
    // 黄条：两个音像在哪儿、差在哪儿，所以 p 容易念成 f
    const bTop = pTop + pH + 12, line1 = Y.C + '，所以 ' + Y.a + ' 容易念成 ' + Y.b, line2 = Y.extra ? '另外 ' + Y.extra : '', bH = line2 ? 80 : 50;
    if (on('c') > 0) {
      ctx.globalAlpha = f * on('c');
      rr(ctx, X, bTop, R - X, bH, 14); ctx.fillStyle = '#FFF6D6'; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = '#F0D25A'; ctx.stroke();
      const fz = fit(ctx, line1, ZH, 'bold', 26, R - X - 40, 20);
      txt(ctx, line1, (X + R) / 2, bTop + 26, { size: fz, weight: 'bold', color: '#6E4A00', align: 'center', base: 'middle' });
      if (line2) txt(ctx, line2, (X + R) / 2, bTop + 58, { size: 21, color: '#6E5520', align: 'center', base: 'middle' });
    }
    // 下面左边：日耳曼人为什么这样念（没有定论，一种说法是…）；右边：例子（拉丁语 → 英语，变了的字母上色）
    const rTop = bTop + bH + 12, rH = y0 + h - 18 - rTop, lw = Math.round((R - X - 16) * 0.56), rw = R - X - 16 - lw;
    if (on('qi') > 0) {
      ctx.globalAlpha = f * on('qi');
      rr(ctx, X, rTop, lw, rH, 14); ctx.fillStyle = '#F4F0FA'; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = '#D9CCEE'; ctx.stroke();
      chip(ctx, '日耳曼人为什么这样念？', X + 16, rTop + 24, { size: 19, bg: '#E6DCF5', color: '#5E35B1' });
      setFont(ctx, 21, ZH, 'normal');
      wrap(ctx, Y.qi, lw - 32, Math.max(1, Math.floor((rH - 44) / 29))).forEach((ln, j) => txt(ctx, ln, X + 16, rTop + 66 + j * 29, { size: 21, color: C.ink }));
    }
    if (on('li') > 0) {
      const ex = Y.li.slice(0, 4), rx = X + lw + 16, langs = [...new Set(ex.map(e => e.lang).filter(Boolean))];
      ctx.globalAlpha = f * on('li');
      rr(ctx, rx, rTop, rw, rH, 14); ctx.fillStyle = '#EEF7EF'; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = '#BFE0C4'; ctx.stroke();
      const cw0 = chip(ctx, '例子', rx + 16, rTop + 24, { size: 19, bg: '#D4EDD8', color: '#2B7A3E' });
      txt(ctx, (langs.join('、') || '拉丁语') + ' → 英语', rx + 16 + cw0 + 12, rTop + 25, { size: 17, color: C.soft, base: 'middle' });
      const cols = ex.length > 3 ? 2 : 1, rows = Math.ceil(ex.length / cols), colW = (rw - 28) / cols;     // 两对音变各两个例子：排成两栏
      const rowH = Math.min(38, (rH - 46) / Math.max(1, rows)), ez = Math.min(cols > 1 ? 23 : 27, rowH * 0.8);
      setFont(ctx, ez, EN, 'normal');
      const lw0 = Math.max(cols > 1 ? 40 : 96, ...ex.map(q => ctx.measureText(q.la).width));
      ex.forEach((e, j) => {
        const m = exMark(e.la, e.en, pairs), ex0 = rx + 18 + (cols > 1 ? Math.floor(j / rows) * colW : 4), ey = rTop + 46 + ((cols > 1 ? j % rows : j) + 0.75) * rowH;
        hiWord(ctx, e.la, m.la, ex0, ey, ez, '#8A7F70', YB_FROM, 'normal');
        txt(ctx, '→', ex0 + lw0 + 10, ey - ez * 0.32, { size: ez, weight: 'bold', color: '#B69D62', base: 'middle' });
        hiWord(ctx, e.en, m.en, ex0 + lw0 + 10 + ez * 1.45, ey, ez + 2, C.ink, YB_TO, 'bold');
        if (langs.length > 1 && cols === 1) txt(ctx, e.lang, rx + rw - 14, ey - ez * 0.3, { size: 15, color: C.faint, align: 'right', base: 'middle' });
      });
    }
    // 左上角那一行（缩小的 pro + duce）：从卡片那一幕接着来；后面不是讲某一部分的就跟着淡出
    const k0 = film.scenes.findIndex(q => q.t0 === sc.t0), nx = k0 >= 0 ? film.scenes[k0 + 1] : null;
    ctx.globalAlpha = nx && nx.id === 'part' ? 1 : span((1 - p) * sc.dur, 0, 0.3);
    miniStrip(ctx, film, sc.i, 1);
    ctx.globalAlpha = 1;
  };

  root.WordFilm = { sfxReset, sfxLog, kaodianOf, lianxiOf, lxParse, LX_TYPES, xingtaiOf, xtSteps, whyOf, yinbianOf, mouthDiagram: mouth, relRows, relPick, noteShow, bianxiOf, idtOf, verbOf, verbSlot, rootLetters, shenfenOf, fengongRows, distOf, fromQingshuang, fromPosLines, build, draw, retime, subtitle, ready, duyinOf, useImages, glyphs, sensesOf, originOf, affixOf, normPic, W, H, PICKER, iconFor, parseSplit, parseEquation, diffLetters, chainOf, memoOf, variantOf, shiftOf };
})(window);
