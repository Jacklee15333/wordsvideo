"""LibreOffice 重算后只冻结了第一行（xSplit=0）：直接改 xlsx 里 sheet1.xml 的 pane，冻结 G2（A–F 列和第一行），不动别的内容和缓存值。"""
import re, sys, zipfile, shutil, os
src = sys.argv[1]; tmp = src + '.tmp'
zin = zipfile.ZipFile(src)
zout = zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED)
for item in zin.infolist():
    data = zin.read(item.filename)
    if item.filename == 'xl/worksheets/sheet1.xml':
        s = data.decode('utf-8')
        new_view = ('<pane xSplit="6" ySplit="1" topLeftCell="G2" activePane="bottomRight" state="frozen"/>'
                    '<selection pane="topRight" activeCell="G1" sqref="G1"/>'
                    '<selection pane="bottomLeft" activeCell="A2" sqref="A2"/>'
                    '<selection pane="bottomRight" activeCell="G2" sqref="G2"/>')
        s2, n = re.subn(r'<pane [^>]*/>(?:<selection [^>]*/>)*', new_view, s, count=1)
        assert n == 1
        data = s2.encode('utf-8')
    zout.writestr(item, data)
zout.close(); zin.close()
shutil.move(tmp, src)
print('pane fixed')
