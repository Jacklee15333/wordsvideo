#!/usr/bin/env python3
"""第八十三版：浏览器为什么用不上显卡——把 WSL 的显卡通路和浏览器自己报的显卡状态打出来（原样发给 Claude 看）。
用法：~/wf-gpu/bin/python ~/lw/scripts/wsl/gpu_diag.py   （或 python3）"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True, timeout=120)
    return (r.stdout + r.stderr).strip()
print('== WSL 显卡通路 ==')
print('/dev/dxg：', '有' if os.path.exists('/dev/dxg') else '没有（WSL 摸不到 Windows 的显卡）')
print('/usr/lib/wsl/lib：', sh('ls /usr/lib/wsl/lib 2>&1 | tr "\\n" " "')[:300])
print('Mesa D3D12 驱动：', sh('ls /usr/lib/x86_64-linux-gnu/dri/ 2>/dev/null | grep -i d3d12 | tr "\\n" " "') or '没有 d3d12_dri.so')
print('Vulkan：', sh('vulkaninfo --summary 2>/dev/null | grep -i deviceName | tr -s " "') or '（vulkaninfo 没装或没有设备）')
print('WSLg：', '有 /mnt/wslg' if os.path.exists('/mnt/wslg') else '没有 /mnt/wslg', '；DISPLAY=%s' % os.environ.get('DISPLAY', ''))
print('OpenGL（WSLg + d3d12）：', sh('GALLIUM_DRIVER=d3d12 DISPLAY=:0 glxinfo -B 2>&1 | grep -iE "renderer|error" | head -3') or '（glxinfo 没装：apt-get install mesa-utils）')
print('EGL（无界面 + d3d12）：', sh('GALLIUM_DRIVER=d3d12 EGL_PLATFORM=surfaceless eglinfo -B 2>&1 | grep -iE "renderer|error" | head -4') or '（eglinfo 没装：apt-get install mesa-utils-bin）')
from gpu_check import BROWSERS
from playwright.sync_api import sync_playwright
print('== 浏览器自己报的显卡状态（chrome 的 SystemInfo）==')
for name, extra in [('CPU（默认）', {})] + BROWSERS:
    env = dict(os.environ); env.update({k: v for k, v in extra.items() if not k.startswith('WORDFILM_')})
    args = extra.get('WORDFILM_BROWSER_ARGS', '').split()
    o = {'args': args, 'env': env}
    if extra.get('WORDFILM_BROWSER_CHANNEL'):
        o['channel'] = extra['WORDFILM_BROWSER_CHANNEL']
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(**o)
            pg = b.new_page()
            info = pg.context.new_cdp_session(pg).send('SystemInfo.getInfo')
            g = info.get('gpu', {})
            fs = g.get('featureStatus', {})
            aux = g.get('auxAttributes', {})
            print('-- %s' % name)
            print('   2D 画布：%s；光栅化：%s；WebGL：%s' % (fs.get('2d_canvas'), fs.get('rasterization'), fs.get('webgl')))
            print('   GL：%s / %s' % (aux.get('glRenderer', ''), aux.get('glImplementationParts', aux.get('glImplementation', ''))))
            for d in g.get('devices', [])[:2]:
                print('   设备：%s %s（%s）' % (d.get('vendorString', ''), d.get('deviceString', ''), d.get('driverVersion', '')))
            probs = [x.get('description', '') for x in g.get('featureStatus', {}).get('problems', [])] if isinstance(fs.get('problems'), list) else []
            for w in (g.get('driverBugWorkarounds') or [])[:0]:
                pass
            b.close()
    except Exception as e:
        print('-- %s：开不起来：%s' % (name, str(e).splitlines()[0][:200]))
