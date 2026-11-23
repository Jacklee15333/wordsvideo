# 出题助手（方案 A）· 给 Claude Code 的说明

用户自己在火狐里操作镜像站：登录、一键直达、进号池、挑账号、选模型、附技能、粘贴指令、点“继续”、换对话，这些都由他来点。
你不操作浏览器、不打开镜像站、不截图、不读网页，也不要提出替他去点。

你负责的只有四件事：
- 装好、测好这个文件夹里的助手；
- 用户要开新对话时，跑 `new`；
- 用户问进度时，跑 `status`；
- 收到异常提醒时，帮他判断和处理，尤其是第七节的“被覆盖了怎么恢复”。

旧会话（D:\claude code folder 里那个）已经作废。不要沿用它的脚本，也不要照它记忆里的“镜像站操作规矩”和“账号”条目做事。那些规矩里还有用的部分，已经写进本文件。

## 一、文件夹里有什么

- `chuti_helper.py`：助手本体，只用 Python 标准库。它只读仓库，从不往仓库写东西。命令有：
  - `new`：开新对话前跑；
  - `watch`：看护；
  - `status`：进度；
  - `test-notify`、`test-clipboard`、`check-token`：测试用。
- `config.example.json`：复制成 `config.json` 再改。
- `prompt_template.txt`：发给网页 Claude 的指令模板。
  - 可用的占位符：{done} {next_word} {row} {pos} {prev_word} {last_group} {round_words} {upload_every}。
  - 口令由脚本从令牌文件读出来，接在最后。
- `new.bat`、`status.bat`、`watch_start.bat`：给用户双击用。
- `zongbiao-questions.skill`：出题技能的防覆盖版。和原版相比只改了 setup.py、upload.sh、SKILL.md 三个文件，见第四节第 7 步。

## 二、交接时的进度（2026-11-20 核对，以仓库为准）

- 最后一次数据提交是 67d6b55：题目第 66 批第 1 组（skinny … theatre），累计 6,199 个词有题目。
- 还缺 3,055 行。
- 第一个缺的是 theater（总表第 6232 个词，批次 84 序号 57）。

## 三、阶段 0：旧会话收尾

每一条先问用户，他同意了再做。

1. 停掉旧的 Claude Code 会话并归档。它挂着每 8 分钟一次的心跳，这件由用户在桌面端自己做。
2. 停掉旧的后台。先列出来给用户看，再停：
   - supervisor.py、repo_watch.py、auto.py、watch_mirror.py、mirror.py 等 python 进程；
   - 开着调试端口 9223 的 Chrome（配置目录 D:\chrome-auto）；
   - geckodriver，以及用 D:\ff-auto 配置的 Firefox。
3. 删除下面这些，问过再删：
   - D:\ff-auto、D:\ff-auto2：用户 Firefox 配置的副本，带 cookie 和保存的登录；
   - D:\chrome-auto；
   - `C:\Users\user\.claude\projects\D--claude-code-folder\memory\zidao-ai-account.md`：里面是明文账号密码。删掉后，同目录 MEMORY.md 里指向它的那一行也要去掉；
   - 同目录的 `mirror-ai-operating-rules.md`：改名为 `.bak` 留着就行，里面是“自动操作网页”的旧规矩。
4. 和用户确认三件事：
   - 旧令牌已经作废；
   - 镜像站的密码已经改了；
   - 仓库根目录那个 session-export zip 删不删，由他决定（删了以后，提交历史里也还在）。

## 四、阶段 1：装好、测好

1. 先确认 `python --version` 和 `git --version` 都能用。助手不需要 pip 装任何东西。
2. 新令牌：请用户在 GitHub 新建一个 fine-grained 令牌：
   - 仓库只选 Jacklee15333/ciyuanchaifeng；
   - 权限是 Contents：Read and write；
   - 有效期建议 30 天以内。
   用户用记事本把它存成 `C:\Users\user\.secrets\gh_token.txt`，文件里只有令牌一行。不要让用户把令牌贴进对话；你也不要打开或打印这个文件。
3. 把 config.example.json 复制成 config.json，然后改两处：
   - 要走代理就保留 `git_proxy: http://127.0.0.1:7892`，不需要就改成 null；
   - `skill_file` 指向桌面上实际要附的技能文件。
4. 依次运行下面几条，每条都看结果，失败就按提示修：
   - `python chuti_helper.py check-token`：要显示“有写权限”。
   - `python chuti_helper.py status`：第一次运行会克隆提交记录，需要几十秒；之后应显示累计数和下一个词。
   - `python chuti_helper.py test-clipboard`：请用户在记事本里按 Ctrl+V，中文显示正常才算过。
   - `python chuti_helper.py test-notify`：右下角弹出通知、有提示音才算过。如果通知出不来，看 logs\helper.log 里的报错，并告诉用户：提示音和手机推送还能用。
5. 手机推送（可选）。用户经常不在电脑旁边，建议开。在 config.json 的 notify.webhook 里填，例如：
   - PushPlus：`{"url": "http://www.pushplus.plus/send", "json": {"token": "<用户的 token>", "title": "{title}", "content": "{body}"}}`
   - Server酱：`{"url": "https://sctapi.ftqq.com/<用户的 SendKey>.send", "form": {"title": "{title}", "desp": "{body}"}}`

   字段以服务商的文档为准；{title} 和 {body} 会被换成提醒内容。填好后再跑一次 test-notify。
6. 看护（watch）要一直开着：
   - 现在先双击 watch_start.bat，然后跑 status，应该显示“看护：在运行”；
   - 用户同意的话，在“启动”文件夹（shell:startup）放一个指向 watch_start.bat 的快捷方式，开机就会自己运行。
7. 换上防覆盖版技能（用户同意后再做）：
   - 把本文件夹的 zongbiao-questions.skill 覆盖到桌面“出题”文件夹。原来那份先改名成 `.bak` 留着。
   - 仓库里「总表视频细节数据/出题技能/」的那份要不要也换掉，由用户决定。要换的话，他用 GitHub Desktop 提交，说明写“出题技能：upload.sh 加防覆盖保险”。

   给用户解释改了什么：
   - setup.py 开工时记下仓库当时的版本；
   - upload.sh 每次上传前都对照一下。如果「总表视频细节数据」在这期间被别的对话改过，就不上传，停下来汇报，不会再用自己的旧副本把别人的成果冲掉；
   - SKILL.md 加了一条：遇到这种情况该怎么办；
   - 其他出题规矩一个字没改。

## 五、日常用法

用户的流程，你可以照这个提醒他：

1. 双击 new.bat，或者让你跑 new。它会先拉最新的仓库：
   - 如果 8 分钟内仓库还有上传，就拒绝并说明原因，因为旧对话可能还在写；
   - 否则把整段指令（含口令）放进剪贴板，并列出火狐里要点的 5 步。
2. 在火狐里依次操作：
   - 关掉旧对话的标签；
   - 打开 zd87.com/ai-fleet/claude，点一键直达，进克劳德·号池1；
   - 往下翻，选状态最好的那个，等输入框出来；
   - 模型选 Opus 5.5，Effort 选中等（不要选“最高”）；
   - 附上 zongbiao-questions.skill；
   - Ctrl+V 粘贴指令，发送。
3. 之后就不用管了。看护每 2 分钟看一次仓库，只有需要他去网页上看的时候才会提醒。

你的做法：

- 用户说“开新对话”：跑 `python chuti_helper.py new`。把前两行（仓库进度）和指令有没有放进剪贴板告诉用户，再提醒他照屏幕上的 5 步点。不要把指令全文或口令贴进对话。
- 用户说“看看做到哪了”：只跑 `python chuti_helper.py status`，原样转述，不超过 5 行。不截图、不打开网页、不去读仓库全文。
- 不要在会话里长时间盯着进度，也不要建 cron 心跳。盯进度是看护（watch）的事。

## 六、提醒是什么意思、怎么办

**“N 分钟没有新上传”**：请用户去看网页，按页面情况处理：
- 显示还在写、still writing 或 Checking for a response：等着。正常 30 分钟左右会出结果。等满 15 分钟可以点一次 Retry；点完还是 still writing，就接着等。
- 出现“继续 / Continue”：点。一个对话最多点 2 次，点满 2 次还需要继续，就跑 new 换新对话。
- 出现 5 小时额度提示：这个对话不能再用了。跑 new 开新对话，它会先确认仓库已经安静了 8 分钟。
- 页面白屏，或者对话不见了：先刷新；对话确实没了，就跑 new。

**“新对话还没上传第一组”**：开了 25 分钟还没有上传。请用户看看：
- 附件有没有附上；
- 指令里有没有口令；
- setup.py 有没有报“索引和总表对不上”。报了就停下，交给用户决定；
- 是不是在等“继续”。

**“新对话起点不对”**：新对话的第一组不是从 new 给出的那个词开始的。请用户看它的回复：
- 如果它在重做已经有的词，叫它停下，然后跑 new 重开；
- 如果它跳过了几个词，记下来，之后补上。

**“有题目被覆盖了！”**：按第七节恢复。

**“连不上 GitHub”**：查网络，看代理 127.0.0.1:7892 有没有开着。

## 七、题目被覆盖了怎么恢复

只在用户同意后做。

1. 先请用户停掉所有网页对话，确认仓库已经 10 分钟没有新提交。
2. 在临时文件夹里把仓库完整克隆下来。只检出「总表视频细节数据」就够了。
3. 找到覆盖的那次提交 X（提醒里有提交号）和它的上一次提交 P。丢失的词，就是索引.tsv 里在 P 是“细节数据有”、到 X 变回“缺”的那些行。
4. 逐个恢复丢失的词：
   - 从 P 取回它的 json：`git checkout P -- <细节数据文件>`；
   - 把索引里那一行改回“细节数据有”，并填回文件路径；
   - README 里 P 有、X 没有的进度行，补回去；
   - X 里新加的词要保留，不要把 X 整个撤回。
5. 提交，说明写“总表视频细节数据：恢复被 X 覆盖的 N 个词（a … b）”。用普通 push，绝不 force。最后跑一次 status，看累计数对不对。

仓库历史里的 4628d49 是上次同类事故的恢复记录，可以参考。

## 八、规矩

- 网页上的一切操作，包括登录、选号、选模型、发送、继续、换对话，都由用户自己做。
- 账号密码和令牌：不进对话、不写进任何文件或记忆、不打印出来。
- 不改仓库 `工具/` 里的脚本；不 force push；删除任何东西之前先问用户。
- 回复用中文，简短，带具体数字。

## 九、DeepSeek 接力（方案 C）

用户在电脑前时用网页出题；网页对话停了、或者用户走开了，由 `runner.py` 调用 DeepSeek 自动接着出题。

**它怎么判断该谁写**

- 网页对话的上传（提交正文里没有“Runner: ciyuan-runner”）停了满 `relay.takeover_minutes` 分钟（默认 30），DeepSeek 才接手。这个时长从用户最后一次跑 new 起算，所以刚开的新对话有 30 分钟起步时间。
- 用户跑 new 时，会写一个 runner_pause.json。DeepSeek 手上那组如果还没上传，就作废不传；new 会等它让出来，再按仓库最新进度生成指令。
- DeepSeek 上传前如果发现网页对话刚上传过，这一组也不传，回去等着。
- DeepSeek 只做普通 push，从不 force。

**一次性设置**

1. 防覆盖版技能（第四节第 7 步）现在必须换上。原因是：网页对话卡在 still writing 超过 30 分钟时 DeepSeek 会接手；网页对话醒过来以后，旧版技能的 upload.sh 会把 DeepSeek 的成果冲掉，防覆盖版会拒绝上传。
2. DeepSeek 的 key：请用户存成 `C:\Users\user\Desktop\令牌\deepseek_key.txt`，文件里只有 key 一行。如果用户同意，也可以从他 Claude 桌面端第三方（DeepSeek）的设置里复制过去，但不要打印出来。
3. config.json 里要补上 `llm` 和 `relay` 两段，照 config.example.json 抄：
   - `model`、`base_url`：和用户现在 Claude Code 用的 DeepSeek 设置保持一致。
   - 如果那里用的地址以 `/anthropic` 结尾，就把 `style` 改成 `anthropic`，`base_url` 填同一个地址；否则用 `openai` 和 `https://api.deepseek.com`。
4. 跑 `python runner.py --selftest`，要看到 DeepSeek 回了 OK，并且令牌有写权限。
5. 双击 runner_start.bat 启动。经用户同意后，也可以在“启动”文件夹放一个指向它的快捷方式，开机自动运行。启动后跑 status，应该能看到“DeepSeek 接力：在运行，等着（网页安静 x/30 分钟）”。

**日常**

- status 会多显示一行“DeepSeek 接力”的状态。
- runner 的日志在 logs\runner.log，DeepSeek 每次的原始输出在 logs\drafts\。
- 体检改了 3 次还过不了的词，记在 runner_state\needs_review.json，runner 会先跳过它们。用户在的时候，你按规矩把这些词的简写稿写好，走 compact.py → save_questions.py 存进去，再提交“补题目……”。
- DeepSeek 出的词，json 里“题目生成”一项会写着“DeepSeek（本地接力）”，README 的进度行里也会注明。以后想用网页重出这些词，按这个标记就能挑出来。
- 想让 DeepSeek 停下：在文件夹里新建一个 STOP 文件，它做完手上这组就停；删掉 STOP 后再双击 runner_start.bat，就能重新开起来。
- 出现“DeepSeek 接力停了”的提醒（key 错了、余额不足、索引和总表对不上等）：读 logs\runner.log 最后 20 行，把原因告诉用户，等他决定。
