#!/usr/bin/env python3
"""第八十版：逐项测配音的三路（声音克隆、英文、识别检查）在显卡和 CPU 上各要多久、显卡上念出来对不对，再试画面的显卡编码（NVENC），
测好写 ~/.wordfilm-gpu.env（出片脚本自动读）。04_gpu.sh 最后一步自动跑；重测：bash ~/lw/scripts/wsl/04_gpu.sh --check
规矩：显卡上念得出来、声音正常、而且比 CPU 快 15% 以上才用显卡；三路放在同一个进程里再一起试一遍（两套 onnxruntime 同时用显卡，
万一冲突就把英文那一路退回 CPU 再试）。每一项都在单独的进程里测，显卡出问题崩了也不影响别的。"""
import json, os, re, subprocess, sys, tempfile, time
os.environ.setdefault('CUDA_CACHE_MAXSIZE', '4294967296')     # 第八十三版：新显卡的 CUDA 程序现编译，缓存放大
S = os.path.expanduser('~/skills/word-construction-video/scripts')
ZH = ['这个词的意思是保护，就是挡住危险，不让它受到伤害。', '考试常考这几样，我们一个一个来看。', '这三个词中文都可以说建议，区别在哪儿呢？']
EN = ['The birds are protected by law.', 'protect', 'Dad turned up the thermostat because it was cold.']
NAMES = {'zv': '声音克隆（中文）', 'en': '英文 af_heart', 'asr': '识别检查'}


def sane(x):
    import numpy as np
    x = np.asarray(x, dtype=np.float32)
    return len(x) > 2400 and bool(np.isfinite(x).all()) and float(np.sqrt(np.mean(x ** 2))) > 1e-3


def one(parts):
    """在这个进程里按 parts（{'zv': 'cuda', ...}）测，打印一行 JSON"""
    for p, d in parts.items():
        os.environ['WORDFILM_%s_DEVICE' % p.upper()] = d
    sys.path.insert(0, S)
    import synth as Y
    Y.CACHE = tempfile.mkdtemp()
    out = {}
    for p in parts:
        t0 = time.time()
        if p == 'zv':
            Y.zipvoice(); Y.gen_voice('热身一下。', None, None, fresh=True); t1 = time.time()      # 第八十三版：先念一句热身再计时
            xs = [Y.gen_voice(t, None, None, fresh=True) for t in ZH]
            ok = all(sane(x) for x in xs)
            info = Y.VC.provider('zv')
        elif p == 'en':
            import kokoro_clean as KC
            Y.tts_en(); KC._session(Y.VC.EN_MODEL); Y.gen_en('warm up'); Y.gen_en('Warm up the model.'); t1 = time.time()
            xs = [Y.gen_en(t) for t in EN]
            ok = all(sane(x) for x in xs)
            info = '%s / %s' % (Y.VC.provider('en'), KC._SESS.get_providers()[0])
        else:
            import soundfile as sf
            wav, text = Y.VC.ref()[:2]
            x, sr = sf.read(wav, dtype='float32')
            if x.ndim > 1:
                x = x.mean(axis=1)
            Y.asr(); Y.transcribe_array(x, sr); t1 = time.time()
            heard = [Y.transcribe_array(x, sr) for _ in range(3)][-1]
            a, b = set(re.sub(r'\W', '', text)), set(re.sub(r'\W', '', heard))
            ok = len(a & b) >= 0.6 * max(1, len(a))
            info = '%s：%s' % (Y.VC.provider('asr'), heard[:16])
        out[p] = {'ok': bool(ok), 'load': round(t1 - t0, 2), 'run': round(time.time() - t1, 2), 'info': info}
    print('JSON' + json.dumps(out, ensure_ascii=False), flush=True)


def run(parts):
    arg = ','.join('%s=%s' % kv for kv in parts.items())
    try:
        r = subprocess.run([sys.executable, os.path.abspath(__file__), '--one', arg], capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired:
        return {p: {'ok': False, 'err': '超时'} for p in parts}
    for l in reversed(r.stdout.splitlines()):
        if l.startswith('JSON'):
            return json.loads(l[4:])
    err = (r.stderr.strip().splitlines() or ['返回码 %d' % r.returncode])[-1][:160]
    return {p: {'ok': False, 'err': err} for p in parts}


# 第八十一版：浏览器画画面能不能用显卡。WSL 里浏览器要借 Windows 的 D3D12 才摸得到显卡，有好几种接法，挨个试；
#   电脑有两块显卡（Intel 核显 + NVIDIA），MESA_D3D12_DEFAULT_ADAPTER_NAME 让它先挑 NVIDIA。
_G = ' --ignore-gpu-blocklist --enable-gpu --enable-gpu-rasterization --disable-gpu-sandbox'
_WSL = {'LD_LIBRARY_PATH': '/usr/lib/wsl/lib:' + os.environ.get('LD_LIBRARY_PATH', ''), 'MESA_D3D12_DEFAULT_ADAPTER_NAME': 'NVIDIA'}
BROWSERS = [         # 第八十二版：加了 --enable-gpu、--disable-gpu-sandbox（GPU 进程要能打开 /dev/dxg）、/usr/lib/wsl/lib
    ('显卡 A（ANGLE + Vulkan）', dict(_WSL, WORDFILM_BROWSER_CHANNEL='chromium', WORDFILM_BROWSER_ARGS='--use-angle=vulkan --enable-features=Vulkan' + _G)),
    ('显卡 B（ANGLE + OpenGL，D3D12）', dict(_WSL, WORDFILM_BROWSER_CHANNEL='chromium', GALLIUM_DRIVER='d3d12',
                                         WORDFILM_BROWSER_ARGS='--use-gl=angle --use-angle=gl-egl' + _G)),
    ('显卡 C（精简浏览器 + OpenGL，D3D12）', dict(_WSL, GALLIUM_DRIVER='d3d12', WORDFILM_BROWSER_ARGS='--use-angle=gl-egl' + _G)),
    ('显卡 D（ANGLE + 原生 EGL）', dict(_WSL, WORDFILM_BROWSER_CHANNEL='chromium', GALLIUM_DRIVER='d3d12', WORDFILM_BROWSER_ARGS='--use-gl=egl' + _G)),
    # 第八十三版：借 WSLg 的显示（Windows 自带的图形转接），Mesa 走 D3D12 摸到 Windows 上的显卡
    ('显卡 E（WSLg + OpenGL，D3D12）', dict(_WSL, WORDFILM_BROWSER_CHANNEL='chromium', GALLIUM_DRIVER='d3d12', DISPLAY=':0', WAYLAND_DISPLAY='wayland-0',
                                         XDG_RUNTIME_DIR='/mnt/wslg/runtime-dir', WORDFILM_BROWSER_ARGS='--use-gl=angle --use-angle=gl' + _G)),
    ('显卡 F（WSLg + 无界面 EGL，D3D12）', dict(_WSL, WORDFILM_BROWSER_CHANNEL='chromium', GALLIUM_DRIVER='d3d12', EGL_PLATFORM='surfaceless',
                                           WORDFILM_BROWSER_ARGS='--use-gl=angle --use-angle=gl-egl' + _G)),
]


def nvenc_sessions():
    """第八十二版：显卡最多能同时编码几路（GeForce 有上限）。2、4、6…一起开，开到出错为止"""
    best = 0
    for k in (2, 4, 6, 8, 10, 12):
        ps = [subprocess.Popen(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-f', 'lavfi', '-i', 'testsrc2=s=1920x1080:r=30', '-t', '3',
                                '-c:v', 'h264_nvenc', '-preset', 'p5', '-f', 'null', '-'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) for _ in range(k)]
        if not all(p.wait() == 0 for p in ps):
            break
        best = k
    return best


def bench(extra):
    """用 render.py --bench 在 protect 上量：只画多快、画 + 压 JPEG + 传回来多快、CPU / 显卡编码多快"""
    D = os.path.expanduser('~/wf-jobs/protect/details.json'); P = os.path.expanduser('~/wordfilm-work/protect/brief/prefs.json')
    if not (os.path.exists(D) and os.path.exists(P)):
        return None, None
    work = tempfile.mkdtemp(prefix='wfbench_')
    env = dict(os.environ)
    for k in ('WORDFILM_BROWSER_GPU', 'WORDFILM_CAPTURE', 'WORDFILM_BROWSER_ARGS', 'WORDFILM_BROWSER_CHANNEL'):
        env.pop(k, None)
    env.update(extra)
    try:
        r = subprocess.run([sys.executable, S + '/render.py', '--details', D, '--word', 'protect', '--prefs', P, '--silent', '--res', '1080',
                            '--out', work + '/x.mp4', '--work', work, '--bench', '240'], env=env, capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired:
        return {'err': '超时'}, work
    for l in r.stdout.splitlines():
        if l.startswith('BENCH'):
            return json.loads(l[5:]), work
    return {'err': ((r.stderr or r.stdout).strip().splitlines() or ['返回码 %d' % r.returncode])[-1][:120]}, work


def psnr(a, b):
    import numpy as np
    from PIL import Image
    x = np.asarray(Image.open(a).convert('RGB'), dtype=np.float32); y = np.asarray(Image.open(b).convert('RGB'), dtype=np.float32)
    if x.shape != y.shape:
        return 0.0
    m = float(np.mean((x - y) ** 2))
    return 99.0 if m == 0 else 10 * float(np.log10(255.0 ** 2 / m))


def soft(gl):
    return bool(re.search(r'swiftshader|llvmpipe|software|softpipe|no-webgl|^err', gl or '', re.I))


def nvenc():
    r = subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-f', 'lavfi', '-i', 'testsrc2=s=1920x1080:r=30', '-t', '4',
                        '-c:v', 'h264_nvenc', '-preset', 'p5', '-tune', 'hq', '-rc', 'vbr', '-cq', '19', '-b:v', '0', '-pix_fmt', 'yuv420p', '-f', 'null', '-'],
                       capture_output=True, text=True)
    return r.returncode == 0, (r.stderr.strip().splitlines() or [''])[-1][:160]


def main():
    a = sys.argv
    if '--one' in a:
        return one(dict(x.split('=') for x in a[a.index('--one') + 1].split(',')))
    envf = a[a.index('--write') + 1]; venv = a[a.index('--venv') + 1]; libs = a[a.index('--libs') + 1]
    g = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader,nounits'], capture_output=True, text=True).stdout.strip().splitlines()
    name, mem = (g[0].split(', ') + ['', '0'])[:2] if g else ('', '0')
    use, rows = {}, []
    for p in ('zv', 'en', 'asr'):
        c, d = run({p: 'cpu'})[p], run({p: 'cuda'})[p]
        faster = d.get('ok') and (not c.get('ok') or d['run'] < c['run'] * 0.85)
        use[p] = 'cuda' if faster else 'cpu'
        rows.append((NAMES[p], ('%.1f 秒' % c['run']) if c.get('ok') else '出错', ('%.1f 秒' % d['run']) if d.get('ok') else ('出错：' + d.get('err', '念得不对'))[:40],
                     '显卡' if faster else 'CPU', d.get('info', '')))
    combo = 'cpu'
    if any(v == 'cuda' for v in use.values()):          # 三路放一个进程一起跑（和真出片一样），冲突了先把英文退回 CPU
        for attempt in range(3):
            res = run(dict(use))
            if all(r.get('ok') for r in res.values()):
                combo = '正常'; break
            back = 'en' if use.get('en') == 'cuda' else 'asr' if use.get('asr') == 'cuda' else 'zv'
            use[back] = 'cpu'; combo = '冲突，%s 退回 CPU' % NAMES[back]
            if not any(v == 'cuda' for v in use.values()):
                break
    ok_nv, why_nv = nvenc()
    # 第八十一、八十二版：浏览器画画面、传帧。每种浏览器接法（CPU + 四种显卡接法）各量一次，每次量两条传帧的路：
    #   JPEG（浏览器压 JPEG 传回来，老办法）和 NV12（显卡上转好、原样交给编码器，第八十二版）。画出来要和 CPU + JPEG 的几乎一样才算数；
    #   再按这台电脑能开几个浏览器（核数、内存；NV12 + 显卡编码时还不能超过显卡能同时编码的路数）估每种组合一秒能出多少帧，挑最快的
    slots = max(1, nvenc_sessions() - 1) if ok_nv else 0
    base, bdir = bench({})
    brows, combos = [], []
    sys.path.insert(0, S)
    import render as R

    def browsers_for(capture):
        os.environ['WORDFILM_ENCODER'] = 'nvenc' if ok_nv else 'x264'
        os.environ['WORDFILM_CAPTURE'] = capture
        os.environ['WORDFILM_NVENC_SLOTS'] = str(slots or 1)
        return R.render_jobs()
    if base and base.get('fps'):
        for name, extra in [('CPU（默认）', {})] + BROWSERS:
            r, d = (base, bdir) if not extra else bench(extra)
            if not r or r.get('err'):
                brows.append((name, '出错', '', (r or {}).get('err', '')[:50])); continue
            hw = not soft(r.get('gl'))
            qj = min(psnr(os.path.join(bdir, 'bench_%d.jpg' % k), os.path.join(d, 'bench_%d.jpg' % k)) for k in range(3))
            qn = min(psnr(os.path.join(bdir, 'bench_%d.jpg' % k), os.path.join(d, 'bench_nv12_%d.png' % k)) for k in range(3)) if r.get('fps_nv12') else 0
            okb = (not extra) or (hw and qj >= 35)
            brows.append((name, '%.0f' % r['fps'], '%.0f' % r['fps_nv12'] if r.get('fps_nv12') else '不行', ('显卡' if hw else 'CPU') + '：' + (r.get('gl') or '')[:40]))
            if okb:
                combos.append((r['fps'] * browsers_for('jpeg') * 0.75, name, 'jpeg', extra, browsers_for('jpeg'), r['fps']))
                if r.get('fps_nv12') and qn >= 33:
                    combos.append((r['fps_nv12'] * browsers_for('nv12') * 0.75, name, 'nv12', extra, browsers_for('nv12'), r['fps_nv12']))
    best = max(combos, key=lambda c: c[0]) if combos else None
    pick = (best[1], {'fps': best[5]}, best[3]) if best and best[3] else None
    L = ['# local-wordfilm 的 04_gpu.sh / gpu_check.py 测好写的（%s，%s）。删掉这个文件（或 bash 04_gpu.sh --off）= 出片全用 CPU' % (time.strftime('%Y-%m-%d %H:%M'), name)]
    if any(v == 'cuda' for v in use.values()):
        L += ['export PATH="%s/bin:$PATH"' % venv, 'export LD_LIBRARY_PATH="%s${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"' % libs]
    L += ['export WORDFILM_ZV_DEVICE=%s' % use['zv'], 'export WORDFILM_EN_DEVICE=%s' % use['en'], 'export WORDFILM_ASR_DEVICE=%s' % use['asr'],
          'export CUDA_CACHE_MAXSIZE=4294967296', 'export WORDFILM_ENCODER=%s' % ('nvenc' if ok_nv else 'x264'), 'export WORDFILM_GPU_MEM_GB=%d' % round(float(mem or 0) / 1024)]
    if pick:
        L += ['export WORDFILM_BROWSER_GPU=1'] + ["export %s='%s'" % kv for kv in pick[2].items()]
    if best:
        L += ['export WORDFILM_CAPTURE=%s' % best[2]]
    if slots:
        L += ['export WORDFILM_NVENC_SLOTS=%d' % slots]
    open(envf, 'w').write('\n'.join(L) + '\n')
    print('显卡：%s（%s GB）' % (name, round(float(mem or 0) / 1024)))
    print('%-12s %-8s %-22s %s' % ('', 'CPU', '显卡', '用'))
    for r in rows:
        print('%-12s %-8s %-22s %s   %s' % r)
    print('%-12s %s' % ('三路一起跑', combo))
    print('%-12s %s' % ('画面编码', '显卡 NVENC 能用' if ok_nv else 'NVENC 用不了，用 CPU（%s）' % why_nv))
    if brows:
        print('浏览器画画面（protect 中间 240 帧，1080p；一个浏览器每秒几帧）：')
        print('  %-26s %-8s %-8s %s' % ('', 'JPEG', 'NV12', '实际用的'))
        for r in brows:
            print('  %-26s %-8s %-8s %s' % r)
        enc = base.get('encode_fps') or {}
        print('编码速度（一路）：CPU libx264 %s 帧/秒；显卡 NVENC %s 帧/秒；显卡最多同时编码 %s 路' % (enc.get('x264') or '—', enc.get('nvenc') or '用不了', slots + 1 if slots else '—'))
        if best:
            print('选了：%s + %s 传帧，%d 个浏览器一起画' % (best[1], '显卡转 NV12' if best[2] == 'nv12' else 'JPEG', best[4]))
            print('估计：一个 5 分钟的视频（9000 帧），画面大约 %d 秒' % round(9000 / best[0] + 20))
    else:
        print('浏览器画画面：没量（protect 还没准备好：先跑 make_word.sh protect 16 explore,shower,itself,protect --no-run）')
    zv = [r for r in rows if r[0] == NAMES['zv']]
    on = [NAMES[p] for p in use if use[p] == 'cuda'] + (['画面编码'] if ok_nv else []) + (['浏览器画画面'] if pick else []) + (['显卡转 NV12 传帧'] if best and best[2] == 'nv12' else [])
    print('✅ 04 完成：用显卡的有 %s；写好了 %s' % ('、'.join(on) if on else '（没有，全用 CPU）', envf))


if __name__ == '__main__':
    main()
