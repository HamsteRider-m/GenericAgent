# Goal Hive Mode SOP

## 定义

Goal Hive = Goal Mode 的多 worker 协作协议
Hive模式单独运行，不要和plan/supervisor/subagent混杂

## 启动

1. 选一个空闲端口 `PORT` 和本次协作 key `BOARD_KEY`。
2. 创建本次 Hive 数据目录：`BBS_CWD=<CodeRoot>/temp/hive_<目标短名>`。
3. 启动 BBS：`start /b python <CodeRoot>/assets/agent_bbs.py --cwd <BBS_CWD> --port <PORT> --key <BOARD_KEY>`。
4. requests访问http://127.0.0.1:<PORT>/readme?key=<BOARD_KEY>。
5. 在bbs发第一个帖子，按照以下“第一帖规范”
6. 后台启动首个worker
7. 询问用户时间预算，按`goal_mode_sop.md`后台启动hive master
8. Hive master，workers都是与你不同的独立进程，你启动它们后应当报告用户并停止

### 第一帖规范

BBS 第一帖必须包含以下四项：
1. 任务目标
2. 「Hive Master 职责」全文（一字不改）
3. 工作目录说明：优先使用 `<BBS_CWD>` 进行文件传输而非BBS文件功能
4. 附加说明（一字不改）：`此为最终目标，worker不要接单，先等hive master拆分子任务。`

### Hive Master 职责
1. 必须阅读记忆中goal_hive_master_duty.md，持续检查问题、寻找改进点
2. 你**负责任务调度和团队组织**，只能干上述duty中提到的内容，不允许亲自干活导致 worker 空转
3. 终极目标是要做到**完美的找不到任何问题的**任务交付结果，保证用户满意，围绕核心产出
4. 如果子任务很多，worker做不过来，可以参照Goal Hive Mode SOP拉起更多worker

## Hive Master

### 恢复中断的 Hive

- 仅在用户明确要求继续时恢复；先检查 `goal_state.json` 的 `objective` 与固定 `done_prompt` 是否仍完整。
- 恢复前重算预算：旧 `start_time` 可能让 master 一启动就判定预算耗尽；按用户新授权刷新预算边界。
- 恢复后以 BBS 最新帖、报告/证据文件和 master 最终收束帖闭环，不以进程仍在/已退单独判定完成。

### goal_state.json 规范

`objective` 必须包含以下几块，缺一不可：
1. 用户目标（简明描述任务与交付物）
2. BBS地址（用requests）：`http://127.0.0.1:<PORT>/readme?key=<BOARD_KEY>`
3. 上方「Hive Master 职责」全文（一字不改）
4. 阅读记忆中goal_hive_master_duty.md了解如何分派和管理工作

`done_prompt` 必须设置为以下固定文本（一字不改）：
`关闭所有你拉起的worker，并在BBS发一条帖子宣告你管理的任务结束，worker除了明确追加任务外，不应再回应。`

启动 master 前必须回读 `goal_state.json`，逐项确认 objective 完整、done_prompt 原文匹配，否则不得启动。

## 拉起 worker

启动 worker：`start /b python <CodeRoot>/agentmain.py --reflect <CodeRoot>/reflect/agent_team_worker.py --base_url http://127.0.0.1:<PORT> --board_key <BOARD_KEY> --name hive-worker-1`。

后续 worker 由 Goal Master 按需要增加（不能超过5个，一般任务2-4个足够）。
