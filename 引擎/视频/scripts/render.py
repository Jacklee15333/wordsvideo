#!/usr/bin/env python3
"""渲染构词动画视频（MP4：H.264 画面 + AAC 配音，6.25 起默认 1920×1080、下面一条字幕栏，30 帧）。

有配音：python3 render.py --details work/details.json --word communication --prefs work/communication/prefs.json \
          --plan work/communication/plan.json --manifest work/communication/audio/manifest.json --out 输出.mp4
没配音：python3 render.py --details work/details.json --word communication --out 输出.mp4 --silent [--prefs prefs.json]

有配音时，每一幕的长短按这一幕的配音来：开头空 0.45 秒，句子之间空 0.40 秒（6.10 起），说完再停 0.7 秒；
plan 里 marks: true 的几幕（拼起来、来历、意思一步步变过来），每一项在配音说到它的时候才出来；
小黑板说完再停 hold 秒（默认 6），视频最后停在小黑板上。--work 文件夹里存一份 timing.json（每一幕从第几秒开始），qa.py 用。
"""
import argparse, base64, glob, hashlib, json, math, os, re, shutil, subprocess
import sys
import numpy as np
import soundfile as sf
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from preview import load_prefs, film_in_page  # noqa: E402
SR, FPS, LEAD, GAP, TAIL = 24000, 30, 0.45, 0.40, 0.7      # 5.5 起句子之间停 0.36 秒（用户讲课录音里短句之间停顿的中位数）；6.10 起 0.40：语速放慢以后句间也松一点
# 6.25（第六十二版）：用户“最后我希望能做1080p的，下面要有字幕；当然读英文句子的时候，由于上面本来就有句子了，这时候不需要有字幕”
#   “只要画面里面有字的就不用加了，没有的才加”。画面按 1920×1080 画；动画缩进上面那一块（16:9），最下面留 BAND 像素一条放字幕，字幕不挡画面。
#   字幕按配音一句句切（逗号、句号处断开，按停顿对齐），这一句话画面上已经写着的（例句、例句的中文、题目、讲解条……）不加，英文句子不加。
BAND = 96          # 6.27.2：上、下各留这么高（1080p 像素），下面那条放字幕
CHUNK = 30.0       # 5.11：画面每 30 秒存成一段（<work>/chunks_xxx/part_000.mp4…），中途被停掉，再跑同一条命令从没做完的那一段接着渲染
UNIT = 10.0        # 6.37（第八十一版）：分段改成在幕的开头切、每段 10 秒以上（最长还是 CHUNK）——段从幕的开头开始就不用“重放”，
                   #   段多了几个浏览器分得更匀（5 分钟的视频 30 秒一段只有 11 段，10 个浏览器分不开）


def loudness_filter(wav, target=-16.0):
    """5.3 起：整段只乘一个增益调到 -16 LUFS，峰值用限幅器压住。
    以前单遍 loudnorm 是动态的，会把字和字之间、句尾的底噪往上提，声音克隆的配音听着沙沙响"""
    r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', wav, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json',
                        '-f', 'null', '-'], capture_output=True, text=True)
    try:
        m = json.loads(r.stderr[r.stderr.rindex('{'):r.stderr.rindex('}') + 1])
        gain = max(-20.0, min(20.0, target - float(m['input_i'])))
    except (ValueError, KeyError):
        return 'loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000'
    return 'volume=%.2fdB,alimiter=limit=0.84:attack=5:release=60:level=disabled,aresample=48000' % gain


def mix_sfx(audio, events, work):
    """6.28：音效混进配音。音效比讲解小声（安静处低 6 dB，正在讲解时再压一半），不抢讲解；
    说话的音效（say:…）和写了 gap 的，要找配音停着的空当放（这一刻起 6 秒内），找不到就不放、打印提醒。"""
    import sfx as SFX
    seen, ev = set(), []
    for e in sorted(events, key=lambda e: e['t']):
        k = (e['name'], round(e['t'], 1))
        if k not in seen:
            seen.add(k); ev.append(e)
    voice = audio.copy()
    win = int(0.05 * SR)
    rms = np.sqrt(np.convolve(voice.astype(np.float64) ** 2, np.ones(win) / win, mode='same'))
    act = rms > 0.03 * (rms.max() or 1)
    sp = float(np.sqrt(np.mean(voice[act].astype(np.float64) ** 2))) if act.any() else 0.1
    duck = np.convolve(np.where(act, 0.5, 1.0), np.ones(int(0.12 * SR)) / int(0.12 * SR), mode='same')
    done, skipped = [], []
    for e in ev:
        try:
            x = SFX.get(e['name']).astype(np.float64)
        except Exception as err:
            skipped.append('%s（%s）' % (e['name'], err)); continue
        loud = np.abs(x) > 0.02
        r = float(np.sqrt(np.mean(x[loud] ** 2))) if loud.any() else 0.3
        vol = float(e.get('vol', 1) or 1)
        at, L = int(round(e['t'] * SR)), len(x)
        if e['name'].startswith('say:') or e.get('gap'):
            spot = None
            for s0 in range(at, min(len(act) - L, at + 6 * SR), int(0.05 * SR)):
                if not act[s0:s0 + L].any():
                    spot = s0; break
            if spot is None:
                skipped.append('%s（%.1f 秒附近配音没有停够 %.1f 秒的空当：给这一句后面加 waits 留空，例句里的在这样东西上写 "wait": 秒）' % (e['name'], e['t'], L / SR)); continue
            audio[spot:spot + L] += (x * sp / r * 0.8 * vol).astype(np.float32)
            done.append('%s@%.1f' % (e['name'], spot / SR))
        else:
            n = max(0, min(L, len(audio) - at))
            audio[at:at + n] += (x[:n] * sp * 10 ** (-6 / 20) / r * vol * duck[at:at + n]).astype(np.float32)
            done.append('%s@%.1f' % (e['name'], e['t']))
    json.dump({'placed': done, 'skipped': skipped}, open(os.path.join(work, 'sfx.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('音效：%d 个（%s）%s' % (len(done), '、'.join(done), ('；没放：' + '；'.join(skipped)) if skipped else ''))


def chime():
    """分段标题的提示音：两个音（G5、C6）叮咚一声，轻一点，不抢配音"""
    out = np.zeros(int(1.2 * SR), dtype=np.float32)
    for f0, off in ((784.0, 0.0), (1046.5, 0.16)):
        t = np.arange(int(0.95 * SR)) / SR
        env = np.exp(-t * 5.0) * np.minimum(1, t / 0.006)
        x = (np.sin(2 * np.pi * f0 * t) * 0.7 + np.sin(2 * np.pi * 2 * f0 * t) * 0.2 + np.sin(2 * np.pi * 3 * f0 * t) * 0.1) * env
        a = int(off * SR)
        out[a:a + len(x)] += (x * 0.09).astype(np.float32)[:len(out) - a]
    return out


# ---------- 6.36（第八十版）：画面用显卡编码（NVENC） ----------
# 用户：“在生成图片时，还是在用 CPU，没有用 GPU，导致生成的速度不是很快”。画面一帧帧是浏览器画的（CPU），以前编码（libx264）也在 CPU 上，
# 和浏览器抢 CPU。WORDFILM_ENCODER=nvenc（本地技能测好显卡能编码才设）就把编码交给显卡，CPU 留给浏览器画画面。
#   - 显卡同时编码的路数有限（几个浏览器、几个词一起渲染会超），所以每一段先把帧存成一个文件，画完再交给显卡一口气编码，
#     占着显卡的时间很短；同一时间最多 WORDFILM_NVENC_SLOTS 路（默认 3）。
#   - 编码方式算进 video.sig 和分段文件夹的名字：一个词的各段都是同一种编码，拼起来不会出问题；默认（x264）和第七十九版一模一样。
#   - 显卡编码出错：这个词改用 CPU（libx264）从头渲染画面，提醒一行，不会卡住。

def nvenc_ok():
    import time
    codec = os.environ.get('WORDFILM_NVENC_CODEC', 'h264_nvenc')      # WORDFILM_NVENC_CODEC 只给测试用
    stamp = '/tmp/wordfilm-nvenc-ok.%s' % re.sub(r'\W', '_', codec)
    try:
        if time.time() - os.path.getmtime(stamp) < 3600:
            s = open(stamp).read().strip()
            return s == 'ok', s
    except OSError:
        pass
    try:
        r = subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-f', 'lavfi', '-i', 'color=c=gray:s=1920x1080:r=30', '-frames:v', '15',
                            '-c:v', codec, '-pix_fmt', 'yuv420p', '-f', 'null', '-'], capture_output=True, text=True, timeout=90)
        s = 'ok' if r.returncode == 0 else ((r.stderr.strip().splitlines() or ['返回码 %d' % r.returncode])[-1])[:200]
    except Exception as e:      # noqa: BLE001
        s = str(e)[:200]
    try:
        open(stamp, 'w').write(s)
    except OSError:
        pass
    return s == 'ok', s


def pick_encoder():
    want = (os.environ.get('WORDFILM_ENCODER') or 'x264').strip().lower()
    if want in ('nvenc', 'gpu', 'auto'):
        ok, why = nvenc_ok()
        if ok:
            return 'nvenc'
        print('提醒：显卡编码（NVENC）用不了（%s），这次画面用 CPU 编码（libx264）' % why, flush=True)
    return 'x264'


def nvenc_slot():
    import fcntl, time
    n = max(1, int(os.environ.get('WORDFILM_NVENC_SLOTS') or 3))
    d = '/tmp/wordfilm-nvenc-slots'
    os.makedirs(d, exist_ok=True)
    while True:
        for i in range(n):
            f = open(os.path.join(d, 'slot%d' % i), 'a')
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return f
            except OSError:
                f.close()
        time.sleep(0.2)


# ---------- 6.38（第八十二版）：每一帧在显卡上转成 NV12，原样交给编码器（不再压 JPEG） ----------
# 用户：“浏览器把每一帧压成 JPEG 交出来……这个能想办法用显卡吗？”。以前每一帧：浏览器在 CPU 上压 JPEG → base64 → 一层层传回来 →
# ffmpeg 在 CPU 上解 JPEG、转颜色。云端量过：压 JPEG + 传回来和画这一帧差不多费时。WORDFILM_CAPTURE=nv12 时：
#   画好的一帧交给 WebGL（显卡），用着色器换算成视频编码器要的 NV12（亮度 + 半尺寸的色度，BT.601、电视范围，和以前的片子同一套颜色），
#   读回来（1080p 一帧 3 MB，以前 JPEG 解开再转也是这么多数据），用 fetch 直接发给本进程开的小服务器，写进 ffmpeg（-f rawvideo -pix_fmt nv12），
#   显卡编码（NVENC）直接吃 NV12。CPU 只剩搬数据。少了一道 JPEG，画质还略好一点；所以和 JPEG 那条路不算同一种画面（算进 video.sig）。
#   浏览器没有 WebGL2 / 着色器出错：这个词改回 JPEG 那条路，提醒一行。本地 gpu_check 量过、比 JPEG 快才开。
NV12_JS = r"""
window.WFCap = (function () {
  let gl, W, H, tex, fy, fuv, py, puv, vao, out;
  const VS = '#version 300 es\nvoid main() { vec2 p = vec2((gl_VertexID << 1) & 2, gl_VertexID & 2); gl_Position = vec4(p * 2.0 - 1.0, 0.0, 1.0); }';
  const HEAD = '#version 300 es\nprecision highp float; precision highp int; uniform sampler2D s; out vec4 o;\n' +
    'vec3 px(int x, int y) { return texelFetch(s, ivec2(x, y), 0).rgb; }\n' +
    'float Y(vec3 c) { return (16.0 + 65.481 * c.r + 128.553 * c.g + 24.966 * c.b) / 255.0; }\n' +
    'float U(vec3 c) { return (128.0 - 37.797 * c.r - 74.203 * c.g + 112.0 * c.b) / 255.0; }\n' +
    'float V(vec3 c) { return (128.0 + 112.0 * c.r - 93.786 * c.g - 18.214 * c.b) / 255.0; }\n';
  const FY = HEAD + 'void main() { int x = int(gl_FragCoord.x) * 4, y = int(gl_FragCoord.y);\n' +
    '  o = vec4(Y(px(x, y)), Y(px(x + 1, y)), Y(px(x + 2, y)), Y(px(x + 3, y))); }';
  const FUV = HEAD + 'void main() { int x = int(gl_FragCoord.x) * 4, y = int(gl_FragCoord.y) * 2;\n' +
    '  vec3 a = (px(x, y) + px(x + 1, y) + px(x, y + 1) + px(x + 1, y + 1)) * 0.25;\n' +
    '  vec3 b = (px(x + 2, y) + px(x + 3, y) + px(x + 2, y + 1) + px(x + 3, y + 1)) * 0.25;\n' +
    '  o = vec4(U(a), V(a), U(b), V(b)); }';
  function sh(t, src) { const x = gl.createShader(t); gl.shaderSource(x, src); gl.compileShader(x);
    if (!gl.getShaderParameter(x, gl.COMPILE_STATUS)) throw new Error('shader: ' + gl.getShaderInfoLog(x)); return x; }
  function prog(fs) { const p = gl.createProgram(); gl.attachShader(p, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(p, sh(gl.FRAGMENT_SHADER, fs));
    gl.linkProgram(p); if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error('link: ' + gl.getProgramInfoLog(p)); return p; }
  function target(w, h) { const t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t); gl.texStorage2D(gl.TEXTURE_2D, 1, gl.RGBA8, w, h);
    const f = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, f); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, t, 0); return f; }
  return {
    init(w, h) {
      try {
        W = w; H = h;
        const c = document.createElement('canvas'); c.width = 4; c.height = 4;
        gl = c.getContext('webgl2', { antialias: false, alpha: false, depth: false, stencil: false, powerPreference: 'high-performance' });
        if (!gl) return 'no-webgl2';
        py = prog(FY); puv = prog(FUV);
        tex = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, tex); gl.texStorage2D(gl.TEXTURE_2D, 1, gl.RGBA8, W, H);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
        fy = target(W / 4, H); fuv = target(W / 4, H / 2);
        vao = gl.createVertexArray();
        gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, false); gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false);
        gl.pixelStorei(gl.UNPACK_COLORSPACE_CONVERSION_WEBGL, gl.NONE); gl.pixelStorei(gl.PACK_ALIGNMENT, 1);
        out = new Uint8Array(W * H * 3 / 2);
        return gl.getError() ? 'gl-error' : '';
      } catch (e) { return String(e).slice(0, 200); }
    },
    grab(src) {
      gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, tex);
      gl.texSubImage2D(gl.TEXTURE_2D, 0, 0, 0, W, H, gl.RGBA, gl.UNSIGNED_BYTE, src);
      gl.bindVertexArray(vao);
      gl.useProgram(py); gl.bindFramebuffer(gl.FRAMEBUFFER, fy); gl.viewport(0, 0, W / 4, H); gl.drawArrays(gl.TRIANGLES, 0, 3);
      gl.readPixels(0, 0, W / 4, H, gl.RGBA, gl.UNSIGNED_BYTE, out, 0);
      gl.useProgram(puv); gl.bindFramebuffer(gl.FRAMEBUFFER, fuv); gl.viewport(0, 0, W / 4, H / 2); gl.drawArrays(gl.TRIANGLES, 0, 3);
      gl.readPixels(0, 0, W / 4, H / 2, gl.RGBA, gl.UNSIGNED_BYTE, out, W * H);
      return out;
    }
  };
})();
"""
NV12_LOOP = """async ([a, b, fps]) => { const c = document.getElementById('c'), x = c.getContext('2d');
  for (let i = a; i < b; i++) { const t = Math.min(window._f.total, i / fps); WordFilm.draw(x, window._f, t, window._view);
    WordFilm.subtitle(x, window._subs, t, window._band);
    const r = await fetch('/f?i=' + i, { method: 'POST', body: WFCap.grab(c) });
    if (!r.ok) throw new Error('send ' + r.status); } }"""


def capture_mode():
    return 'nv12' if os.environ.get('WORDFILM_CAPTURE', 'jpeg').strip().lower() == 'nv12' else 'jpeg'


class FrameServer:
    """本进程里的小服务器：页面从这里打开（同源），每一帧 fetch POST 过来，按帧号顺序写进 sink（ffmpeg 的输入）"""
    def __init__(self):
        import http.server, threading
        self.lock = threading.Lock()
        self.sink, self.next, self.pending, self.got, self.err = None, 0, {}, 0, None
        srv = self

        class H(http.server.BaseHTTPRequestHandler):
            protocol_version = 'HTTP/1.1'

            def log_message(self, *a):
                pass

            def do_GET(self):
                b = b'<!doctype html><html><body style="margin:0"></body></html>'
                self.send_response(200); self.send_header('Content-Type', 'text/html'); self.send_header('Content-Length', str(len(b)))
                self.end_headers(); self.wfile.write(b)

            def do_POST(self):
                n = int(self.headers.get('Content-Length') or 0)
                data = self.rfile.read(n)
                try:
                    i = int(self.path.rsplit('=', 1)[1])
                except (IndexError, ValueError):
                    i = -1
                srv.put(i, data)
                self.send_response(204); self.send_header('Content-Length', '0'); self.end_headers()
        self.httpd = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H)
        self.httpd.daemon_threads = True
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.url = 'http://127.0.0.1:%d' % self.httpd.server_address[1]

    def start(self, sink, first):
        with self.lock:
            self.sink, self.next, self.pending, self.got, self.err = sink, first, {}, 0, None

    def put(self, i, data):
        with self.lock:
            if self.sink is None:
                return
            self.pending[i] = data
            while self.next in self.pending:
                d = self.pending.pop(self.next)
                try:
                    self.sink.write(d)
                except Exception as e:      # noqa: BLE001
                    self.err, self.sink = str(e)[:120], None
                    return
                self.next += 1
                self.got += 1

    def stop(self):
        with self.lock:
            self.sink = None
            return self.got


class KeepSome:
    """gpu_check 的样张：只留第几帧"""
    def __init__(self, keep):
        self.keep, self.i, self.kept = set(keep), 0, []

    def write(self, d):
        if self.i in self.keep:
            self.kept.append(bytes(d))
        self.i += 1


def nv12_png(buf, W, H, path):
    import numpy as np
    from PIL import Image
    y = np.frombuffer(buf, np.uint8, W * H).reshape(H, W).astype(np.float32)
    uv = np.frombuffer(buf, np.uint8, W * H // 2, W * H).reshape(H // 2, W // 2, 2).astype(np.float32)
    u = uv[..., 0].repeat(2, 0).repeat(2, 1) - 128
    v = uv[..., 1].repeat(2, 0).repeat(2, 1) - 128
    yy = (y - 16) * 255 / 219
    k = 255 / 224
    rgb = np.stack([yy + 1.402 * k * v, yy - 0.344136 * k * u - 0.714136 * k * v, yy + 1.772 * k * u], -1)
    Image.fromarray(np.clip(rgb + 0.5, 0, 255).astype(np.uint8)).save(path)


def nvenc_args(part):
    return ['-c:v', 'h264_nvenc', '-preset', os.environ.get('WORDFILM_NVENC_PRESET', 'p5'), '-tune', 'hq', '-rc', 'vbr',
            '-cq', os.environ.get('WORDFILM_NVENC_CQ', '19'), '-b:v', '0', '-spatial-aq', '1', '-bf', '2', '-g', '250',
            '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-r', str(FPS), part]


def nv12_unit(pg, fsrv, part, f0, f1, enc, res, RW, RH):
    """6.38：画 f0..f1 这几帧，显卡上转 NV12，直接写进编码器；返回 0 或出错说明"""
    raw = ['-f', 'rawvideo', '-pix_fmt', 'nv12', '-s', '%dx%d' % (RW, RH), '-framerate', str(FPS)]
    if enc == 'x264':
        q = ['-c:v', 'libx264', '-preset', 'faster' if res == 1080 else 'medium', '-crf', '18', '-tune', 'animation', '-pix_fmt', 'yuv420p',
             '-profile:v', 'high', '-level', '4.0', '-r', str(FPS), part]
    else:
        q = nvenc_args(part)
    slot = nvenc_slot() if enc != 'x264' else None
    err, got, rc = '', 0, 1
    try:
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error'] + raw + ['-i', '-'] + q, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            import fcntl
            fcntl.fcntl(ff.stdin, 1031, 1 << 20)          # F_SETPIPE_SZ：管道放大到 1 MB，少来回几次
        except Exception:      # noqa: BLE001
            pass
        fsrv.start(ff.stdin, f0)
        try:
            for i0 in range(f0, f1, 30):
                pg.evaluate(NV12_LOOP, [i0, min(f1, i0 + 30), FPS])
        except Exception as e:      # noqa: BLE001
            err = '页面出错：' + str(e).splitlines()[0][:160]
        got = fsrv.stop()
        try:
            ff.stdin.close()
        except OSError:
            pass
        e2 = ff.stderr.read().decode('utf-8', 'replace').strip()
        rc = ff.wait()
    finally:
        if slot:
            slot.close()
    if rc != 0:
        return ('nvenc：' if enc != 'x264' else 'ffmpeg：') + ((e2.splitlines() or ['返回码 %d' % rc])[-1][:200])
    if err or got != f1 - f0 or fsrv.err:
        return '帧没收全（%d / %d）%s %s' % (got, f1 - f0, err, fsrv.err or '')
    return 0


def nvenc_encode(src, buf, part, res):
    """存好的一段帧交给显卡编码；出错隔几秒再试，3 次都不行返回报错（调用的地方改用 CPU 重做这个词）"""
    import time
    codec = os.environ.get('WORDFILM_NVENC_CODEC', 'h264_nvenc')
    if codec == 'h264_nvenc':
        q = nvenc_args(part)
    else:        # 测试：没有显卡的机器上走同一条“先存帧、再编码”的路
        q = ['-c:v', codec, '-preset', 'faster' if res == 1080 else 'medium', '-crf', '18', '-tune', 'animation', '-pix_fmt', 'yuv420p',
             '-profile:v', 'high', '-level', '4.0', '-r', str(FPS), part]
    last = ''
    for k in range(3):
        slot = nvenc_slot()
        try:
            r = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + src + ['-i', buf] + q, capture_output=True, text=True)
        finally:
            slot.close()
        if r.returncode == 0:
            return 0
        last = (r.stderr.strip().splitlines() or ['返回码 %d' % r.returncode])[-1][:200]
        time.sleep(2 + 3 * k)
    return last or 'ffmpeg 出错'



# ---------- 6.37（第八十一版）：浏览器用显卡画画面（试验，本地 gpu_check 测好才开） ----------
# 用户：“整个过程用 GPU，不要用 CPU，除非必须要用 CPU 时用”。浏览器默认在 CPU 上画（WSL 里没显卡），
# WORDFILM_BROWSER_ARGS 给浏览器加参数（比如用 ANGLE + WSL 的 D3D12 显卡驱动），WORDFILM_BROWSER_GPU=1 表示应该在显卡上画：
# 每个浏览器开起来先查一下 WebGL 用的是什么（SwiftShader / llvmpipe 就是没用上显卡），没用上就这个词改回 CPU 画（显卡、CPU 画出来有极细的差别，
# 一个词里不能混），提醒一行。显卡和 CPU 画的不算同一种画面：算进 video.sig。
def browser_opts():
    args = [x for x in os.environ.get('WORDFILM_BROWSER_ARGS', '').split() if x]
    o = {'args': args} if args else {}
    ch = os.environ.get('WORDFILM_BROWSER_CHANNEL', '').strip()
    if ch:
        o['channel'] = ch
    return o


def browser_gpu():
    return os.environ.get('WORDFILM_BROWSER_GPU', '') == '1'


GL_JS = """() => { try { const g = document.createElement('canvas').getContext('webgl');
  if (!g) return 'no-webgl'; const e = g.getExtension('WEBGL_debug_renderer_info');
  return String(e ? g.getParameter(e.UNMASKED_RENDERER_WEBGL) : g.getParameter(g.RENDERER)); } catch (x) { return 'err:' + x; } }"""


def soft_gl(name):
    return bool(re.search(r'swiftshader|llvmpipe|software|softpipe|no-webgl|^err:', name or '', re.I))


def unit_bounds(n, scene_starts, target, maxlen):
    """6.37：每段从哪一帧开始。在幕的开头切，每段至少 target 帧；太长（超过 maxlen）就在里面最后一个幕开头切，
    里面没有幕开头（一幕本身超过 maxlen）才在幕中间切（那一段要重放，和以前一样）"""
    starts = sorted(set(s for s in scene_starts if 0 < s < n))
    out, cur = [0], 0
    while True:
        nxt = next((s for s in starts if s >= cur + target), n)
        if nxt - cur > maxlen:
            inside = [s for s in starts if cur < s <= cur + maxlen]
            nxt = inside[-1] if inside else cur + maxlen
        if nxt >= n:
            return out
        out.append(nxt)
        cur = nxt


def bench(pg, a, work, total, fsrv=None):
    """gpu_check 用：从视频 40% 处起画 a.bench 帧，量“只画”“画 + 压 JPEG + 传回来”各多快；存 3 张样张；再量 CPU / 显卡编码各多快"""
    import time
    n = a.bench
    f0 = int(total * FPS * 0.4)
    gl = pg.evaluate(GL_JS)
    pg.evaluate("""([a, b, fps]) => { const c = document.getElementById('c'), x = c.getContext('2d');
      for (let i = a; i < b; i++) WordFilm.draw(x, window._f, Math.min(window._f.total, i / fps), window._view); }""", [f0, f0 + 12, FPS])
    t0 = time.time()
    pg.evaluate("""([a, b, fps]) => { const c = document.getElementById('c'), x = c.getContext('2d');
      for (let i = a; i < b; i++) WordFilm.draw(x, window._f, Math.min(window._f.total, i / fps), window._view); x.getImageData(0, 0, 1, 1); }""", [f0, f0 + n, FPS])
    t_draw = time.time() - t0
    frames = []
    t0 = time.time()
    for i0 in range(f0, f0 + n, 12):
        urls = pg.evaluate("""([a, b, fps]) => { const c = document.getElementById('c'), x = c.getContext('2d'), out = [];
          for (let i = a; i < b; i++) { const t = Math.min(window._f.total, i / fps); WordFilm.draw(x, window._f, t, window._view);
            WordFilm.subtitle(x, window._subs, t, window._band); out.push(c.toDataURL('image/jpeg', 0.94)); }
          return out; }""", [i0, min(f0 + n, i0 + 12), FPS])
        frames += [base64.b64decode(u.split(',', 1)[1]) for u in urls]
    t_full = time.time() - t0
    for k, j in enumerate((0, len(frames) // 2, len(frames) - 1)):
        open(os.path.join(work, 'bench_%d.jpg' % k), 'wb').write(frames[j])
    buf = os.path.join(work, 'bench.frames')
    open(buf, 'wb').write(b''.join(frames))
    src = ['-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg']
    enc = {}
    for name, q in (('x264', ['-c:v', 'libx264', '-preset', 'faster' if a.res == 1080 else 'medium', '-crf', '18', '-tune', 'animation', '-pix_fmt', 'yuv420p']),
                    ('nvenc', ['-c:v', 'h264_nvenc', '-preset', 'p5', '-tune', 'hq', '-rc', 'vbr', '-cq', '19', '-b:v', '0', '-pix_fmt', 'yuv420p'])):
        t0 = time.time()
        r = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + src + ['-i', buf] + q + ['-f', 'null', '-'], capture_output=True, text=True)
        enc[name] = round(n / (time.time() - t0), 1) if r.returncode == 0 else None
    os.remove(buf)
    out = {'frames': n, 'draw_fps': round(n / t_draw, 1), 'fps': round(n / t_full, 1), 'encode_fps': enc, 'gl': gl, 'res': a.res}
    why = pg.evaluate("() => window._wfcap_err == null ? 'no-init' : window._wfcap_err") if fsrv is not None else 'no-server'
    if why:
        out['fps_nv12'], out['nv12_err'] = None, why
        return out
    RW, RH = (1920, 1080) if a.res == 1080 else (1280, 720)
    keep = KeepSome([0, n // 2, n - 1])
    fsrv.start(keep, f0)
    t0 = time.time()
    try:
        for i0 in range(f0, f0 + n, 30):
            pg.evaluate(NV12_LOOP, [i0, min(f0 + n, i0 + 30), FPS])
    except Exception as e:      # noqa: BLE001
        out['nv12_err'] = str(e).splitlines()[0][:160]
    got = fsrv.stop()
    out['fps_nv12'] = round(n / (time.time() - t0), 1) if got == n else None
    for k, d in enumerate(keep.kept):
        nv12_png(d, RW, RH, os.path.join(work, 'bench_nv12_%d.png' % k))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--details', required=True)
    ap.add_argument('--word', required=True)
    ap.add_argument('--prefs')
    ap.add_argument('--plan')
    ap.add_argument('--manifest')
    ap.add_argument('--out', required=True)
    ap.add_argument('--silent', action='store_true')
    ap.add_argument('--work', help='放临时文件（配音总轨）和 timing.json 的文件夹，默认和输出视频放一起')
    ap.add_argument('--res', type=int, default=1080, choices=[720, 1080], help='6.25：画面多高（默认 1080 = 1920×1080）')
    ap.add_argument('--no-subs', action='store_true', help='6.25：不要字幕（也不留字幕栏）')
    ap.add_argument('--frame', default='jpeg', choices=['jpeg', 'png'], help='页面交给 ffmpeg 的每一帧用什么格式（jpeg 快很多）')
    ap.add_argument('--jobs', type=int, default=0, help='6.35：几个浏览器一起渲染（0 = 按 CPU、内存自动定；也可以设 WORDFILM_RENDER_JOBS）')
    ap.add_argument('--worker-of', help=argparse.SUPPRESS)       # 6.35：内部用——帮主进程渲染这个文件夹里没人认领的段
    ap.add_argument('--deadline', type=float, default=0, help=argparse.SUPPRESS)
    ap.add_argument('--enc', help=argparse.SUPPRESS)                 # 6.36：内部用——主进程定好的编码方式
    ap.add_argument('--bench', type=int, default=0, help=argparse.SUPPRESS)   # 6.37：gpu_check 用——量画面、编码各多快
    ap.add_argument('--cap', help=argparse.SUPPRESS)                  # 6.38：内部用——主进程定好的传帧方式（jpeg / nv12）
    ap.add_argument('--budget', type=float, default=0, help='这一次最多渲染多少秒钟（0 = 不限）：到点就停在一段的结尾，返回码 3，再跑一次接着做')
    a = ap.parse_args()
    work = a.work or os.path.dirname(os.path.abspath(a.out))
    os.makedirs(work, exist_ok=True)
    details = json.load(open(a.details, encoding='utf-8'))
    detail = details.get(a.word) or next(v for v in details.values() if v['w'].lower() == a.word.lower())
    prefs = load_prefs(a.prefs)        # 画里自己的图片读成 data URL
    narrated = not a.silent
    if narrated:
        plan = json.load(open(a.plan, encoding='utf-8'))
        man = json.load(open(a.manifest, encoding='utf-8'))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    # 5.11：分段渲染，可以接着做。一个词的画面由词条、画面设置、配音稿、每句配音的长短、wordfilm.js 决定：
    # 这些都没变，做好的段就复用；整段视频已经做好的（<work>/video.sig 对得上）直接跳过
    import time as _time
    started = _time.time()
    enc = a.enc or pick_encoder()          # 6.36：x264（CPU，默认）或 nvenc（显卡）
    cap = a.cap or capture_mode()          # 6.38：jpeg（默认）或 nv12（显卡上转好、原样交给编码器）
    sig = hashlib.md5(json.dumps([detail, prefs, plan if narrated else None, [[k, [(x.get('name'), x.get('dur')) for x in v]] for k, v in sorted(man.items())] if narrated else None, FPS, CHUNK, a.res, not a.no_subs, a.frame, 'sub-6.27b', 'sfx-6.28'] + ([enc] if enc != 'x264' else []) + ['units-6.37', UNIT] + (['gpu-raster'] if browser_gpu() else []) + (['nv12-6.38'] if cap == 'nv12' else []),
                                 ensure_ascii=False, sort_keys=True, default=str).encode('utf-8') + open(os.path.join(HERE, 'wordfilm.js'), 'rb').read()).hexdigest()[:12]
    stamp = os.path.join(work, 'video.sig')
    if not a.worker_of and not a.bench and os.path.exists(a.out) and os.path.exists(stamp) and open(stamp).read().strip() == sig and os.path.exists(os.path.join(work, 'timing.json')):
        print('%s：视频已经做好了（画面、配音都没变），跳过 -> %s' % (detail['w'], a.out))
        return
    with sync_playwright() as p:
        b = p.chromium.launch(**browser_opts())
        pg = b.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        RW, RH = (1920, 1080) if a.res == 1080 else (1280, 720)
        fsrv = None
        if cap == 'nv12' or a.bench:      # 6.38：页面从本进程的小服务器打开（同源），每一帧用 fetch 直接传回来
            fsrv = FrameServer()
            pg.goto(fsrv.url + '/')
        pg.set_content('<html><body style="margin:0"><canvas id=c width=%d height=%d></canvas></body></html>' % (RW, RH))
        pg.add_script_tag(path=os.path.join(HERE, 'wordfilm.js'))
        if browser_gpu():                  # 6.37：说好用显卡画，查一下真用上了没有
            gl = pg.evaluate(GL_JS)
            if soft_gl(gl):
                b.close()
                if a.worker_of:
                    open(os.path.join(a.worker_of, 'browsergpu.failed'), 'w').write(gl)
                    return
                print('提醒：浏览器没用上显卡（%s），这个词改回 CPU 画画面' % gl[:120], flush=True)
                env = dict(os.environ, WORDFILM_BROWSER_GPU='0', WORDFILM_BROWSER_ARGS='', WORDFILM_BROWSER_CHANNEL='')
                os.execve(sys.executable, [sys.executable, os.path.abspath(__file__)] + sys.argv[1:], env)
        if fsrv is not None:
            pg.add_script_tag(content=NV12_JS)
            why = pg.evaluate("([w, h]) => (window._wfcap_err = WFCap.init(w, h))", [RW, RH])
            if why and cap == 'nv12':
                b.close()
                if a.worker_of:
                    open(os.path.join(a.worker_of, 'capture.failed'), 'w').write(why)
                    return
                print('提醒：浏览器不能在显卡上转 NV12（%s），这个词改回 JPEG 传帧' % why[:120], flush=True)
                os.execve(sys.executable, [sys.executable, os.path.abspath(__file__)] + sys.argv[1:], dict(os.environ, WORDFILM_CAPTURE='jpeg'))
        # 6.25：记下画面上写了哪些字（字幕只加画面上没写着的话）
        pg.evaluate("""() => { const P = CanvasRenderingContext2D.prototype, f = P.fillText; window._cap = null;
          P.fillText = function (s, x, y, m) { if (window._cap && this.globalAlpha > 0.35) window._cap.push(String(s)); return m === undefined ? f.call(this, s, x, y) : f.call(this, s, x, y, m); }; }""")
        subs_on = narrated and not a.no_subs
        view = band = None
        if not a.no_subs:
            # 6.27.2（第六十九版，用户：“画面不是上下居中；做的视频要尽量上下居中，这样好看一些”）：上下各留一样高的边，
            # 动画正好在整个画面的正中间；下面那条边放字幕（以前只在下面留一条，动画整体偏上）
            bh = int(round(BAND * RH / 1080))
            fh = RH - 2 * bh
            fw = int(round(fh * 16 / 9))
            view, band = {'x': (RW - fw) / 2, 'y': bh, 'w': fw, 'h': fh}, {'y': RH - bh, 'h': bh}
        pg.evaluate("([v, b]) => { window._view = v; window._band = b; window._subs = []; }", [view, band])
        scenes = film_in_page(pg, detail, prefs)          # 搭好动画，读进 3D 表情图
        place = []
        segall = []                                               # 6.25：每一句配音（字幕用）
        if narrated:
            timing = []
            for si, key in enumerate(scenes):
                segs, spec = man.get(key, []), plan['scenes'].get(key, {})
                if not segs:
                    timing.append(None)
                    continue
                t, marks, ends, texts = LEAD, [], [], []
                waits = spec.get('waits') or {}                      # 6.13：练习题念完题目、停几秒让学生想（画面倒计时）
                for j, s in enumerate(segs):
                    extra = 0.0
                    if s['name'] != 'intro':
                        marks.append(round(t, 3))
                        ends.append(round(t + s['dur'], 3))          # 5.11：这一句说完的秒数、这一句的字（画里按词出东西 when 要用）
                        texts.append(s.get('text', ''))
                        extra = float(waits.get(str(len(marks) - 1), 0))
                    place.append((si, t, s['path']))
                    segall.append((si, t, s))
                    t += s['dur'] + (GAP if j < len(segs) - 1 else 0) + extra
                timing.append({'dur': round(t + TAIL + float(spec.get('hold', 0)), 3), 'marks': marks if spec.get('marks') else None, 'groups': spec.get('groups'),
                               'ends': ends if spec.get('marks') else None, 'texts': texts if spec.get('marks') else None})
            missing = [k for k in scenes if k not in man and k in plan['scenes']]
            if missing:
                print('提醒：这几幕没有配音，按默认长度放：' + ', '.join(missing))
            pg.evaluate("(tm) => WordFilm.retime(window._f, tm)", timing)
        info = pg.evaluate("() => ({ total: window._f.total, scenes: window._f.scenes.map(s => [s.id + (s.i != null ? s.i : ''), Math.round(s.t0 * 100) / 100, Math.round(s.dur * 100) / 100]) })")
        total = info['total']
        cues = []
        if a.bench:                        # 6.37：只量速度
            if subs_on:
                pg.evaluate("(c) => { window._subs = c; }", build_cues(segall, info, pg))
            res = bench(pg, a, work, total, fsrv)
            b.close()
            print('BENCH' + json.dumps(res, ensure_ascii=False), flush=True)
            return
        if subs_on and a.worker_of:
            # 6.35：帮忙渲染的进程也照主进程那样排一遍字幕（排字幕时每一幕都画过一次，页面里的图才和主进程一样“画热”了，
            #   第一次画的一帧会有细微差别），但用的字幕照主进程存下的
            build_cues(segall, info, pg)
            pg.evaluate("async () => { await document.fonts.ready; await new Promise(r => setTimeout(r, 300)); }")
            cues = json.load(open(os.path.join(work, 'subs.json'), encoding='utf-8'))
            pg.evaluate("(c) => { window._subs = c; }", cues)
        elif subs_on:
            cues = build_cues(segall, info, pg)
            pg.evaluate("(c) => { window._subs = c; }", cues)
            json.dump(cues, open(os.path.join(work, 'subs.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
            write_srt(cues, os.path.join(work, 'subtitles.srt'))
            print('字幕：%d 条（画面上已经写着的话、英文句子不加）' % len(cues))
        cdir = a.worker_of or os.path.join(work, 'chunks_' + sig)
        if not a.worker_of:
            for old in glob.glob(os.path.join(work, 'chunks_*')):
                if old != cdir:
                    shutil.rmtree(old, ignore_errors=True)
        os.makedirs(cdir, exist_ok=True)
        n = int(math.ceil(total * FPS))
        per = int(CHUNK * FPS)
        # 6.37：段在幕的开头切（每段 UNIT 秒以上、最长 CHUNK 秒）；starts[ci] 是第 ci 段的第一帧
        starts = unit_bounds(n, [int(math.ceil(x[1] * FPS - 1e-6)) for x in info['scenes']], int(UNIT * FPS), per)
        ends = starts[1:] + [n]
        parts = [os.path.join(cdir, 'part_%03d.mp4' % ci) for ci in range(len(starts))]
        stopped = False
        # 6.35（第七十九版）：每段画面只由时间决定（接着渲染本来就靠这一点），所以几段可以由几个浏览器同时渲染：
        # 主进程开几个帮忙的进程，大家按顺序“认领”还没做的段（建 part_xxx.mp4.lock），做完写 .ok；最后由主进程拼起来
        deadline = a.deadline if a.worker_of else (started + a.budget if a.budget else 0)
        workers = []
        if not a.worker_of:
            for lk in glob.glob(os.path.join(cdir, '*.lock')):        # 上次中途停下留下的认领记号
                os.remove(lk)
            todo = [p_ for p_ in parts if not os.path.exists(p_ + '.ok')]
            jobs = render_jobs(a.jobs)
            if jobs > 1 and len(todo) > 1:
                argv = [sys.executable, os.path.abspath(__file__)] + sys.argv[1:] + ['--worker-of', cdir, '--deadline', repr(deadline), '--enc', enc, '--cap', cap]
                workers = [subprocess.Popen(argv) for _ in range(min(jobs, len(todo)) - 1)]
                print('画面：%d 个浏览器一起渲染（还有 %d 段；编码：%s；传帧：%s）' % (len(workers) + 1, len(todo), '显卡 NVENC' if enc != 'x264' else 'CPU libx264',
                      '显卡转 NV12' if cap == 'nv12' else 'JPEG'), flush=True)
            elif enc != 'x264':
                print('画面编码：显卡 NVENC', flush=True)

        def claim(part):
            if os.path.exists(part + '.ok'):
                return False
            try:
                os.close(os.open(part + '.lock', os.O_CREAT | os.O_EXCL | os.O_WRONLY))
                return True
            except FileExistsError:
                return False

        def do_chunk(ci, f0):
            part = parts[ci]
            # 6.35：这一段开头那一幕要是在前一段就开始了，先画一下这一幕开头那一帧（一个浏览器从头做时，这一帧早就画过），
            #   这样不管这一段由哪个浏览器、在什么时候做，画出来都和从头一段段做的一样；在音效清零之前画，不会多记音效
            if f0 > 0:
                st = [x[1] for x in info['scenes'] if x[1] <= f0 / FPS + 1e-6]
                if st:
                    fs = int(math.ceil(st[-1] * FPS - 1e-6))
                    if fs < f0:          # 从这一幕开头重放到这一段之前（只画不存，最多 30 秒），再等字体、图片加载完
                        pg.evaluate("""async ([a, b, fps]) => { const c = document.getElementById('c'), x = c.getContext('2d');
                          for (let i = a; i < b; i++) WordFilm.draw(x, window._f, Math.min(window._f.total, i / fps), window._view);
                          await document.fonts.ready; await new Promise(r => setTimeout(r, 300)); }""", [max(fs, f0 - per), f0, FPS])
            pg.evaluate("() => WordFilm.sfxReset()")              # 6.28：这一段画面里出来的音效，记在 part_xxx.mp4.sfx.json
            if cap == 'nv12':                # 6.38：显卡上转 NV12、原样交给编码器
                rc = nv12_unit(pg, fsrv, part, f0, ends[ci], enc, a.res, RW, RH)
                if rc != 0:
                    print('  这一段没做好：%s' % rc, flush=True)
                    if str(rc).startswith('nvenc'):
                        open(os.path.join(os.path.dirname(part), 'nvenc.failed'), 'w').write(str(rc))
                f1 = ends[ci]
            else:
                src = ['-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg' if a.frame == 'jpeg' else 'png']
                if enc == 'x264':
                    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error'] + src + ['-i', '-',
                                           '-c:v', 'libx264', '-preset', 'faster' if a.res == 1080 else 'medium', '-crf', '18', '-tune', 'animation', '-pix_fmt', 'yuv420p',
                                           '-profile:v', 'high', '-level', '4.0', '-r', str(FPS), part], stdin=subprocess.PIPE)
                    sink = ff.stdin
                else:                       # 6.36：显卡编码——这一段的帧先存成文件，画完再交给显卡一口气编码
                    buf = part + '.frames'
                    sink = open(buf, 'wb')
                f1 = ends[ci]
                for i0 in range(f0, f1, 12):
                    urls = pg.evaluate("""([a, b, fps, fmt]) => { const c = document.getElementById('c'), x = c.getContext('2d'), out = [];
                      for (let i = a; i < b; i++) { const t = Math.min(window._f.total, i / fps); WordFilm.draw(x, window._f, t, window._view);
                        WordFilm.subtitle(x, window._subs, t, window._band); out.push(fmt === 'jpeg' ? c.toDataURL('image/jpeg', 0.94) : c.toDataURL('image/png')); }
                      return out; }""", [i0, min(f1, i0 + 12), FPS, a.frame])
                    for u in urls:
                        sink.write(base64.b64decode(u.split(',', 1)[1]))
                sink.close()
                if enc == 'x264':
                    rc = ff.wait()
                else:
                    rc = nvenc_encode(src, buf, part, a.res)
                    try:
                        os.remove(buf)
                    except OSError:
                        pass
                    if rc != 0:
                        open(os.path.join(os.path.dirname(part), 'nvenc.failed'), 'w').write(str(rc))
            if rc == 0:
                lo, hi = f0 / FPS, f1 / FPS
                evs = [e for e in pg.evaluate("() => WordFilm.sfxLog()") if lo - 0.05 <= e['t'] < hi]
                json.dump(evs, open(part + '.sfx.json', 'w'), ensure_ascii=False)
                open(part + '.ok', 'w').write('ok')
                print('  画面 %d / %d 段' % (ci + 1, len(parts)), flush=True)

        for ci, f0 in enumerate(starts):
            if any(os.path.exists(os.path.join(cdir, x)) for x in ('nvenc.failed', 'browsergpu.failed', 'capture.failed')):
                break
            if os.path.exists(parts[ci] + '.ok'):
                continue
            if deadline and _time.time() > deadline:
                stopped = True
                continue
            if claim(parts[ci]):
                do_chunk(ci, f0)
        if a.worker_of:
            b.close()
            if errs:
                print('页面报错：' + '; '.join(errs))
            return
        for w_ in workers:
            w_.wait()
        for ci, f0 in enumerate(starts):           # 帮忙的进程中途出错：没做好的段主进程补上
            if any(os.path.exists(os.path.join(cdir, x)) for x in ('nvenc.failed', 'browsergpu.failed', 'capture.failed')):
                break
            if os.path.exists(parts[ci] + '.ok'):
                continue
            if deadline and _time.time() > deadline:
                stopped = True
                continue
            if os.path.exists(parts[ci] + '.lock'):
                os.remove(parts[ci] + '.lock')
            if claim(parts[ci]):
                do_chunk(ci, f0)
        b.close()
    if os.path.exists(os.path.join(cdir, 'capture.failed')):           # 6.38：有浏览器不能转 NV12，这个词改回 JPEG 传帧
        print('提醒：有一个浏览器不能在显卡上转 NV12（%s），这个词改回 JPEG 传帧' % open(os.path.join(cdir, 'capture.failed')).read().strip()[:120], flush=True)
        shutil.rmtree(cdir, ignore_errors=True)
        os.execve(sys.executable, [sys.executable, os.path.abspath(__file__)] + sys.argv[1:], dict(os.environ, WORDFILM_CAPTURE='jpeg'))
    if os.path.exists(os.path.join(cdir, 'browsergpu.failed')):        # 6.37：有浏览器没用上显卡，这个词改回 CPU 画（一个词里不能混）
        print('提醒：有一个浏览器没用上显卡（%s），这个词改回 CPU 画画面' % open(os.path.join(cdir, 'browsergpu.failed')).read().strip()[:120], flush=True)
        shutil.rmtree(cdir, ignore_errors=True)
        os.execve(sys.executable, [sys.executable, os.path.abspath(__file__)] + sys.argv[1:],
                  dict(os.environ, WORDFILM_BROWSER_GPU='0', WORDFILM_BROWSER_ARGS='', WORDFILM_BROWSER_CHANNEL=''))
    if enc != 'x264' and os.path.exists(os.path.join(cdir, 'nvenc.failed')):      # 6.36：显卡编码出错，这个词改用 CPU 从头渲染画面
        print('提醒：显卡编码（NVENC）出错了（%s），这个词改用 CPU（libx264）重新渲染画面' % open(os.path.join(cdir, 'nvenc.failed')).read().strip()[:200], flush=True)
        shutil.rmtree(cdir, ignore_errors=True)
        os.execve(sys.executable, [sys.executable, os.path.abspath(__file__)] + sys.argv[1:], dict(os.environ, WORDFILM_ENCODER='x264'))
    missing = [p_ for p_ in parts if not os.path.exists(p_ + '.ok')]
    if missing and not stopped:
        raise SystemExit('%s：有 %d 段画面没做好（看上面 ffmpeg 的报错）' % (detail['w'], len(missing)))
    if stopped:
        print('%s：这一次的时间用完了，画面做到一半（做好的段留着）。再跑同一条命令接着做' % detail['w'])
        raise SystemExit(3)
    # 拼起来：各段画面直接接上（不重新编码），配上声音
    lst = os.path.join(cdir, 'list.txt')
    open(lst, 'w').write(''.join("file '%s'\n" % os.path.abspath(x).replace("'", "'\\''") for x in parts))
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst]
    if narrated:
        audio = np.zeros(int(math.ceil(total * SR)) + SR, dtype=np.float32)
        t0 = [x[1] for x in info['scenes']]
        for si, off, path in place:
            x, sr = sf.read(path, dtype='float32')
            fade = int(0.012 * SR)
            x[:fade] *= np.linspace(0, 1, fade)
            x[-fade:] *= np.linspace(1, 0, fade)
            at = int(round((t0[si] + off) * SR))
            audio[at:at + len(x)] += x[:max(0, len(audio) - at)]
        # 5.0 起：“一、读音拆分”“二、含义拆分”两个分段标题，开头轻轻“叮咚”一声
        for name, t_0, _ in info['scenes']:
            if name.startswith('sec'):
                ch = chime()
                at = int(round((t_0 + 0.1) * SR))
                audio[at:at + len(ch)] += ch[:max(0, len(audio) - at)]
        # 6.28（第七十版）：音效混进去（每一段画面记下的 part_xxx.mp4.sfx.json）
        evs = []
        for part in parts:
            if os.path.exists(part + '.sfx.json'):
                evs += json.load(open(part + '.sfx.json', encoding='utf-8'))
        if evs:
            mix_sfx(audio, evs, work)
        wav = os.path.join(work, 'narration.wav')
        sf.write(wav, audio[:int(round(total * SR))], SR)
        cmd += ['-i', wav, '-map', '0:v', '-map', '1:a', '-af', loudness_filter(wav), '-c:a', 'aac', '-b:a', '160k', '-ac', '2', '-shortest']
    cmd += ['-c:v', 'copy', '-movflags', '+faststart', a.out]
    subprocess.run(cmd, check=True)
    embed_cover(a.out, work)
    shutil.rmtree(cdir, ignore_errors=True)
    open(stamp, 'w').write(sig)
    if narrated:
        os.remove(wav)
    json.dump({'word': detail['w'], 'total': total, 'scenes': info['scenes'], 'video': os.path.abspath(a.out)}, open(os.path.join(work, 'timing.json'), 'w'), ensure_ascii=False)
    print('%s：%.1f 秒，%d 帧%s -> %s%s' % (detail['w'], total, n, '，有配音' if narrated else '，没配音', a.out, ('  页面报错：' + '; '.join(errs)) if errs else ''))


def render_jobs(want=0):
    """6.35：几个浏览器一起渲染。--jobs / WORDFILM_RENDER_JOBS 指定；不指定按 CPU（每个约 3 核）和空闲内存（每个约 1.2 GB）算，最多 6 个；1 核就是 1 个"""
    v = want or int(os.environ.get('WORDFILM_RENDER_JOBS', '0') or 0)
    if v > 0:
        return v
    cpu = os.cpu_count() or 1
    try:
        avail = next(int(l.split()[1]) for l in open('/proc/meminfo') if l.startswith('MemAvailable')) / 1048576
    except Exception:
        avail = 0
    # 6.37：编码交给显卡（nvenc）以后一个浏览器只占 1 个多核，按 1.5 核一个、最多 16 个（WORDFILM_RENDER_MAX）；CPU 编码还是 3 核一个、最多 6 个
    gpu_enc = os.environ.get('WORDFILM_ENCODER', 'x264').strip().lower() in ('nvenc', 'gpu', 'auto')
    cap = int(os.environ.get('WORDFILM_RENDER_MAX', '0') or 0) or (16 if gpu_enc else 6)
    if gpu_enc and capture_mode() == 'nv12':      # 6.38：nv12 这条路每个浏览器一直占着一路显卡编码，不能超过显卡能同时编码的路数
        cap = min(cap, max(1, int(os.environ.get('WORDFILM_NVENC_SLOTS') or 3)))
    return max(1, min(cap, int(cpu // (1.5 if gpu_enc else 3)), int((avail - 1) // 1.2)))


def embed_cover(video, work):
    """6.27：第一帧（封面：单词 + 含义 + 画）另存成 cover.jpg，再作为封面图嵌进 mp4（covr）。
    Windows 资源管理器、手机相册、网盘多半直接拿封面图或第一帧做缩略图，不点开就看得出是哪个词"""
    cover = os.path.join(work, 'cover.jpg')
    try:
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-frames:v', '1', '-q:v', '2', cover], check=True)
        tmp = video + '.cover.mp4'
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-i', cover, '-map', '0', '-map', '1', '-c', 'copy',
                        '-disposition:v:1', 'attached_pic', '-movflags', '+faststart', tmp], check=True)
        os.replace(tmp, video)
    except Exception as e:                       # noqa: BLE001  封面嵌不进去不影响视频本身
        print('提醒：封面图没嵌进去（%s），视频第一帧照样是封面' % e)


# ---------------- 6.25：字幕 ----------------
CJK_RE = re.compile(r'[\u3400-\u9fff]')


def sub_clean(t):
    t = re.sub(r'\bqz([a-z]+)', r'\1', str(t))                 # 读音拆分的音素词（qzspeaker）→ 字母
    return re.sub(r'\s+', ' ', t.replace('todays', "today's")).strip()


def sub_chunks(t):
    """一句配音按标点切成几条字幕（太短的并到前一条，太长的再从顿号、冒号切）"""
    parts, out = [x.strip() for x in re.split(r'(?<=[，。；！？!?;])', t) if x.strip()], []
    for x in parts:
        if out and len(re.sub(r'[^\u3400-\u9fffA-Za-z]', '', out[-1])) < 6 and not re.search(r'[。！？!?]$', out[-1]):
            out[-1] += x
        else:
            out.append(x)
    res = []
    for x in out:
        while len(x) > 26:
            k = max([m.end() for m in re.finditer(r'[、：:，,]', x[:24])] or [0])
            if k <= 6:
                break
            res.append(x[:k]); x = x[k:]
        res.append(x)
    return res


def sub_show(c):
    c = re.sub(r'[，。；、,;]+$', '', c.strip())
    return re.sub(r'\s*[，,]\s*', ' ', c).strip()


def sub_w(c):
    zh = len(CJK_RE.findall(c))
    en = sum(1 + 0.35 * len(w) for w in re.findall(r"[A-Za-z][A-Za-z'-]*", c))
    return max(1.0, zh + en + 1.6 * len(re.findall(r'[，。；：！？,;:!?]', c)))


def sub_pauses(path):
    try:
        x, sr = sf.read(path, dtype='float32')
    except Exception:
        return []
    x = x.mean(1) if x.ndim > 1 else x
    k = int(0.01 * sr); n = len(x) // k
    if n < 5:
        return []
    e = np.sqrt((x[:n * k].reshape(n, k) ** 2).mean(1)); thr = e.max() * 0.05
    out, i = [], 0
    while i < n:
        if e[i] < thr:
            j = i
            while j < n and e[j] < thr:
                j += 1
            if j - i >= 12 and i > 0 and j < n:
                out.append((i + j) / 2 * 0.01)
            i = j
        else:
            i += 1
    return out


ZH_NUM = str.maketrans('一二三四五六七八九', '123456789')


def _norm(s):
    """比的时候去掉标点、空格，“第一题”和画面上的“第 1 题”当成一样"""
    return re.sub(r'[\s，。；：！？、,.;:!?“”"\'（）()\-—…·/]', '', str(s)).lower().translate(ZH_NUM)


def sub_covered(text, screen):
    """这句话画面上写了多少（中文按两个字一组、英文按词数）：0～1"""
    t, sc = _norm(text), _norm(screen)
    zh = ''.join(re.findall(r'[\u3400-\u9fff0-9]', t))
    big = [zh[i:i + 2] for i in range(len(zh) - 1)] or ([zh] if zh else [])
    en = re.findall(r'[a-z]{2,}', t)
    tot = len(big) + len(en)
    if not tot:
        return 1.0
    return (sum(1 for b in big if b in sc) + sum(1 for w in en if w in sc)) / tot


def build_cues(segall, info, pg, keep=0.6):
    t0s = [x[1] for x in info['scenes']]
    sids = [str(x[0]) for x in info['scenes']]
    starts = sorted(t0s[si] + off for si, off, _ in segall)
    raw, nth = [], {}
    for si, off, sg in segall:
        # 6.34（第七十八版）：考点几页念的都是画面上那几行（画面写 sb.、n.、①，配音念 somebody、名词、第一，按字比不上，
        #   以前会漏出“provide somebody with something”这种字幕），只给第一句引子（“考试常考这几样。”）加字幕；
        #   练习、答案几幕念的是题号、题型、题目要求、答案、讲解，都在画面上，一律不加（用户：“只要画面里面有字的就不用加了，没有的才加”）
        k = nth.get(si, 0)
        if sg.get('name') != 'intro':
            nth[si] = k + 1
        sid = sids[si] if si < len(sids) else ''
        if re.match(r'(lianxi|daan)\d*$', sid) or (re.match(r'kaodian\d*$', sid) and sg.get('name') != 'intro' and k > 0):
            continue
        text = sub_clean(sg.get('text', ''))
        if not text or not CJK_RE.search(text):          # 英文句子、单词、音节块：不加字幕
            continue
        st, dur = t0s[si] + off, float(sg['dur'])
        nxt = min([x for x in starts if x > st + 1e-3] or [st + dur + 1.0])
        ch = sub_chunks(text)
        ws = [sub_w(c) for c in ch]
        cum = np.cumsum([0.0] + ws) / max(1e-6, sum(ws)) * dur
        ps = sub_pauses(sg.get('path', ''))
        bounds = [0.0]
        for b in cum[1:-1]:
            near = [p for p in ps if abs(p - b) < 0.8 and p > bounds[-1] + 0.3]
            bounds.append(min(near, key=lambda p: abs(p - b)) if near else max(bounds[-1] + 0.3, b))
        bounds.append(dur)
        for j, c in enumerate(ch):
            if not CJK_RE.search(c):                     # 6.34：中英夹着念的句子切开以后，只有英文的那一截也不加
                continue
            a0, a1 = st + bounds[j], st + bounds[j + 1]
            if j == len(ch) - 1:
                a1 = min(st + dur + 0.3, nxt - 0.03)
            raw.append({'t0': round(a0, 3), 't1': round(max(a0 + 0.5, a1), 3), 'text': sub_show(c), 'say': c})
    if not raw:
        return []
    ts = []
    for c in raw:
        ts += [c['t0'] + 0.6 * (c['t1'] - c['t0']), c['t1'] - 0.05]
    seen = pg.evaluate("""(ts) => { const c = document.getElementById('c'), x = c.getContext('2d'), out = [];
        for (const t of ts) { window._cap = []; WordFilm.draw(x, window._f, Math.min(window._f.total, t), window._view); out.push(window._cap.join('\\n')); }
        window._cap = null; return out; }""", ts)
    out = []
    for k, c in enumerate(raw):
        cov = sub_covered(c['say'], seen[2 * k] + '\n' + seen[2 * k + 1])
        if cov >= keep or not c['text']:
            continue
        out.append({'t0': c['t0'], 't1': c['t1'], 'text': c['text']})
    for k in range(len(out) - 1):
        out[k]['t1'] = min(out[k]['t1'], out[k + 1]['t0'] - 0.02)
    return out


def write_srt(cues, path):
    def ts(x):
        ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s_, ms = divmod(ms, 1000)
        return '%02d:%02d:%02d,%03d' % (h, m, s_, ms)
    with open(path, 'w', encoding='utf-8') as fh:
        for i, c in enumerate(cues, 1):
            fh.write('%d\n%s --> %s\n%s\n\n' % (i, ts(c['t0']), ts(c['t1']), c['text']))


if __name__ == '__main__':
    main()
