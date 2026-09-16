# Nano 产品与人群能力封装验收

验收日期：2026-09-06。封装范围：本项目本地目录中的产品问答、潜在人群与心理表达分析，以及经共享写手完成的评论培训。产品事实与人群心理资料分别维护。

## 直接调用

在本项目其他对话中可直接输入：

- `调用 Nano 能力库，分析还有哪些潜在人群。`
- `调用 Nano 能力库，深入分析异地生活者的使用心理与可能表达。`
- `使用 $use-nano-knowledge，查清 Nano 的存储和分体监看条件。`
- `调用 $write-dji-nano-comments，结合当前材料写培训评论。`

[项目 AGENTS](../../../AGENTS.md)、[项目写手入口](../../../.agents/skills/write-consumer-training-comments/SKILL.md)均指向[新 Nano 入口](../../../.agents/skills/use-nano-knowledge/SKILL.md)。原个人 Nano 技能调用名继续可用；真实材料核验与旧稿审查保留原分支。

## 验收范围与证据

产品基础材料已独立检查：80 条事实（78 已核、2 待核）、7 个官方来源文件及其 SHA256、7 张场景卡、14 组 FAQ。阅读版与 JSONL 内容一致，事实条件与来源定位可追溯。本轮封装未全面重新联网核验官方资料；历史核验日期保持不变。

人群部分新增 10 条可检索的需求假设，21 个关联事实 ID 均存在且已核。分析方法支持按当前命题扩展角色，具体人物与例句保留在训练输出。全部心理种子仍为 `editorial_hypothesis` / `pending_user_calibration`。

独立运行的 Codex `skills/list` 已在项目根目录及 `knowledge/nano/` 子目录发现唯一、启用的 `use-nano-knowledge`，作用域为 `repo`，界面名称为“Nano产品与人群能力库”。本次发现过程未创建新对话或执行模型任务。

无历史上下文的调用测试已通过：

| 测试 | 实际结果 | 证据 |
|---|---|---|
| 自然语言“调用 Nano 能力库” | 自行从项目约定找到新入口；用既有需求种子分析异地生活，再扩展出业余旧家具修复情境；未读取旧例句或历史验收，无循环加载 | [独立调用报告](../../../outputs/nano/2026-09-06-package-acceptance/fresh-context.json) |
| 存储与分体监看问答 | 答对卡用于导出、不能直录；兼容无线麦连接且分体时录像中不能监看，并区分固件增加的录像前构图 | 同上；本次实际读取当前官方 FAQ、下载列表、中文手册和固件说明 |
| 原 `$write-dji-nano-comments` 调用 | 从项目 Nano 入口取用产品、场景与人群资料，完成 2 条主评、0 回复；正式批次走共享写手训练契约 | [写作调用报告](../../../outputs/nano/2026-09-06-package-acceptance/writing-route/README.md) |
| 培训结构与表达检查 | 共享检查器退出码 0；人工逐句复核两条动机不同，没有同义劝购、心理研究伪装或未核功能保证；样稿仍待用户校准 | [实际检查输出](../../../outputs/nano/2026-09-06-package-acceptance/writing-route/training-check.json)、[语义复核](../../../outputs/nano/2026-09-06-package-acceptance/writing-route/semantic-review.md) |
| 技能与静态结构 | 新技能及项目写手入口通过 `quick_validate.py`；JSONL、哈希、引用及文件链接检查通过 | [结构记录](packaging-structure.json) |
| 运行时发现 | 根目录、子目录均发现唯一且启用的项目技能，UI 元数据正确 | [实际运行时返回](packaging-runtime.json) |

两次独立调用均使用无历史上下文的执行代理，并由主任务读取实际产物复核。原始训练与心理例句未因验收变为用户认可案例。实时产品核验遇到中文网页跳转英文站时已在报告标明语言，另直接读取中文手册；只复核了测试涉及的断言，不扩大为全部 80 条的重新认证。

## 维护时复查

从项目根目录运行：

```sh
python3 .agents/skills/use-nano-knowledge/scripts/validate_package.py
```

脚本检查 JSONL 字段、唯一 ID、来源文件哈希、事实引用、角色来源与本地文件链接；它不联网重核产品、不判断句子自然度、不检查 Markdown 锚点，也不授予用户认可。产品真实性按[维护规则](../MAINTENANCE.md)复核；新写批次仍用共享写手检查器，不借用本次验收结果。

## 调用范围

本封装按项目目录发现，适用于该目录及其子目录中的本地对话，无需建库聊天。Codex 支持从项目 `.agents/skills` 发现技能，并可显式或按描述调用；若已打开的界面列表未刷新，可新开本项目对话或重启应用后再查看。[官方技能说明](https://learn.chatgpt.com/docs/build-skills)

项目指令在会话启动时读取；已有对话可用上述显式调用，要求读取最新项目入口。单独复制技能目录不包含产品知识、训练原件和共享写手依赖；本轮未验证其他项目、独立检出目录、其他电脑或云端的自动可用性。[官方项目指令说明](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

仍待核的产品问题为 `NANO-MAN-023`（休眠按键流程）与 `NANO-MAN-024`（清洁液适用范围）。封装完成和技术检查通过均不会把它们变成已核，也不会把训练示例变成用户认可范文。
