#!/usr/bin/env python3
"""发布单词工作台新版本（照仓库规矩）：
  1. 旧版本整个 app 文件夹（git HEAD 里的）备份到 版本备份/v旧版本号/app
  2. app/VERSION 升版本（默认 minor；--patch 修小问题；--major 大改）
  3. CHANGELOG.md 最上面加一条（标题 + 几行说明 + “旧版本备份在…”）
  4. 提交“单词工作台 v新版本：标题”，用令牌推到 main（令牌不进任何文件、不打印）
用法：python3 release.py <仓库目录> "标题" "说明1" "说明2" ... [--patch|--major] [--token-file 路径] [--no-push]
令牌：--token-file 指的文件里找 github_pat_…，或者环境变量 GH_TOKEN。"""
import base64, os, re, subprocess, sys, time
args = [a for a in sys.argv[1:] if not a.startswith("--")]
flags = [a for a in sys.argv[1:] if a.startswith("--")]
repo, title, notes = args[0], args[1], args[2:]
tf = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--token-file"), "")
notes = [n for n in notes if n != tf]
part = "patch" if "--patch" in flags else "major" if "--major" in flags else "minor"
def git(*a, **kw):
    return subprocess.run(["git", "-C", repo, "-c", "core.quotepath=off"] + list(a), capture_output=True, text=True, **kw)
old = open(os.path.join(repo, "app", "VERSION"), encoding="utf-8").read().strip()
v = [int(x) for x in old.split(".")] + [0, 0]
v = {"major": [v[0] + 1, 0, 0], "minor": [v[0], v[1] + 1, 0], "patch": [v[0], v[1], v[2] + 1]}[part]
new = "%d.%d.%d" % tuple(v)
bk = os.path.join(repo, "版本备份", "v" + old)
if not os.path.exists(bk):
    os.makedirs(bk)
    arc = subprocess.run(["git", "-C", repo, "archive", "HEAD", "app"], capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", bk], input=arc, check=True)
open(os.path.join(repo, "app", "VERSION"), "w", encoding="utf-8").write(new + "\n")
p = os.path.join(repo, "CHANGELOG.md")
s = open(p, encoding="utf-8").read()
entry = "## v%s（%s）%s\n\n%s\n- 旧版本备份在「版本备份/v%s」\n\n" % (new, time.strftime("%Y-%m-%d"), title, "\n".join("- " + n for n in notes), old)
i = s.find("\n## v")
s = s[:i + 1] + entry + s[i + 1:] if i >= 0 else s + "\n" + entry
open(p, "w", encoding="utf-8").write(s)
git("add", "-A", check=True)
git("-c", "user.name=Jacklee15333", "-c", "user.email=Jacklee15333@users.noreply.github.com", "commit", "-q", "-m", "单词工作台 v%s：%s" % (new, title), check=True)
print("提交好了：v%s（旧版本备份在 版本备份/v%s）" % (new, old))
if "--no-push" in flags:
    sys.exit(0)
tok = os.environ.get("GH_TOKEN", "")
if tf:
    m = re.search(r"github_pat_[A-Za-z0-9_]+|ghp_[A-Za-z0-9]+", open(tf, encoding="utf-8", errors="ignore").read())
    tok = m.group(0) if m else tok
if not tok:
    sys.exit("没有令牌：用 --token-file 或 GH_TOKEN；提交已经在本地")
b = base64.b64encode(("x-access-token:" + tok).encode()).decode()
r = git("-c", "http.extraHeader=Authorization: Basic " + b, "push", "-q", "https://github.com/Jacklee15333/wordsvideo.git", "HEAD:main")
print("推送：" + ("成功" if r.returncode == 0 else "失败 " + r.stderr.replace(tok, "***")[-400:]))
