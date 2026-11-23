"""补后缀说明、意思演变（三列分工版的入口）。用法：python3 sense_write.py <源表.xlsx> <新表.xlsx>

总表三列分工以后，“在这里”写在组合列【词性变化】，〔用词规律〕标在组合列的步骤末尾，规律写在【用词规律】。
补内容的老流程（sense_write_core.py）是按旧格式写的（写进各部分解释），所以这里分三步：
  1. columns.py merge：把组合列里的这三样临时搬回各部分解释（老流程据此知道哪些已经写过，跳过）；
  2. sense_write_core.py：老流程照常补（后缀来源、作用、在这里；意思怎么变、用词规律），写 P 列和记录；
  3. columns.py split：再把它们搬回组合列。
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import columns  # noqa: E402

if len(sys.argv) < 3:
    print(__doc__)
    sys.exit(1)
src, out = sys.argv[1], sys.argv[2]
tmp = tempfile.mkdtemp()
a, b = os.path.join(tmp, 'merged.xlsx'), os.path.join(tmp, 'written.xlsx')
columns.run('merge', src, a)
r = subprocess.run([sys.executable, os.path.join(HERE, 'sense_write_core.py'), a, b])
if r.returncode != 0:
    sys.exit(r.returncode)
print('搬回组合列：', columns.run('split', b, out))
