# AI 画的插图（单词工作台）：把 art/wag/ 里的 svg 拷进画图文件夹
import os, sys, glob, shutil
src = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'art', 'wag')
for f in glob.glob(os.path.join(src, '*.svg')):
    shutil.copy(f, sys.argv[1])
print('ok')
