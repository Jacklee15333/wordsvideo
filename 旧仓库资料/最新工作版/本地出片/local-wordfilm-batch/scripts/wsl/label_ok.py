#!/usr/bin/env python3
"""第八十版：起草检查的“还要补”只剩“标签‘X’配音里没有说到”，而精简版稿子（brief/plan.json）里都说到了 X → 返回 0（放行），否则 1。
用法：label_ok.py "<还要补 这一行>" <精简版 plan.json>"""
import json, re, sys
line, plan_p = sys.argv[1], sys.argv[2]
body = re.sub(r'^\s*还要补[:：]\s*', '', line.strip())
items = [x for x in re.split(r'[；;]', body) if x.strip()]
labels = [re.search(r'标签“(.+?)”配音里没有说到', x) for x in items]
if not items or not all(labels):
    sys.exit(1)
try:
    plan = json.load(open(plan_p, encoding='utf-8'))
except Exception:
    sys.exit(1)
said = json.dumps(plan.get('scenes', {}), ensure_ascii=False)
missing = [m.group(1) for m in labels if m.group(1) not in said]
if missing:
    print('精简版稿子里也没说到：' + '、'.join(missing))
    sys.exit(1)
print('起草检查只差标签（%s），精简版稿子里都说到了：放行（kit README 写明的情况）' % '、'.join(m.group(1) for m in labels))
