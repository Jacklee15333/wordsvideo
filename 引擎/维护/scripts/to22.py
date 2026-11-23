# -*- coding: utf-8 -*-
"""把 16 / 17 列的精简表补回 22 列的老样子，存成临时 xlsx，给按 22 列写的体检脚本用（project_rules.md 第 57 条）。
  python3 to22.py <精简表.xlsx> <临时.xlsx>
video_check.py、hecheng_check.py、guoqu_check.py、zimu_check.py、pinxie_check.py、root_check.py、rule_check.py、yingmei_check.py 都对着临时文件跑；
tonggen_check.py、part_memo.py --check、shenfen_check.py 按列名读，直接对着精简表跑。
例句、核对结果这些精简表里没有的列留空；辨析列（17 列表才有）不在 22 列里，体检脚本不看它，这里不带过去。"""
import sys
from openpyxl import Workbook
from linetools import load_table
HEAD22 = ['批次', '序号', '组号', '小类号', '单词', '含义', '例句', '类型', '拆分', '前缀', '词根', '单词部分', '后缀', '组合 → 现在的含义',
          '新·背景（只写在词族第一个词上）', '音变 / 字母变化', '核对结果', '核对依据', '来源链接', '原表备注', '本次调整', '词根变体处理']
def main(src, dst):
    hdr, C, rows = load_table(src)
    col = {h: i for i, h in enumerate(hdr)}
    wb = Workbook(write_only=True); ws = wb.create_sheet('拆分结果')
    ws.append(HEAD22)
    for r in rows:
        ws.append([('' if col.get(h) is None or r[col[h]] is None else r[col[h]]) for h in HEAD22])      # 空格写成 ''：只读方式读回来每行才都是 22 格
    wb.save(dst)
    print('存好了 %s（%d 行）' % (dst, len(rows)))
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
