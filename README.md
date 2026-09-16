# 阿豹追猎 · 20 Skills 总控版

此仓库保存 `阿豹追猎.zip` 中的 `dji-ai-skills-portable-20260915-v1` 技能包，包含 20 个 `MODULE.md` 入口及其知识资料、参考文件和脚本。目录已解压，便于查看和导入。

```text
总控 S0 → 材料 S1 → 当前品线事实 S2 → 共享写手 S3
                                              ↓
交付 ← 全批主评/回复去重、事实、表达、格式 Q
          └─ 有问题：定点返工 → 全批复检
```

保留原包20个SKILL：1个总控、1个日批规划、1个材料读取、5个知识、1个共享写手、5个只读适配、6个兼容调用名。Q是总控的终审流程，不增加技能数量。

- [安装与DeepSeek使用](INSTALL.md)
- [可粘贴总提示词](SYSTEM_PROMPT.md)
- [总控入口](deepseek/abao-controller/SKILL.md)
- [阶段与返工规则](skills/write-consumer-training-comments/references/stage-contract.md)
- [统一质检](skills/write-consumer-training-comments/references/final-quality.md)
- [全批机器检查脚本](scripts/check_batch_quality.py)及[批次模板](examples/batch.template.json)

脚本检查结构、版本绑定和文本相似候选，语义、事实与自然度仍需逐项审阅。没有脚本运行能力时可以内容复核，但不声称机器检查通过。适配元数据是否生效取决于宿主，不能仅靠上传ZIP保证平台级串行锁。

常用入口：

| 用途 | 文件 |
| --- | --- |
| 共享写作规则 | [MODULE.md](writer-core/core/write-consumer-comments/MODULE.md) |
| Pocket 知识 | [MODULE.md](skills/use-pocket-knowledge/MODULE.md) |
| Osmo Mobile 知识 | [MODULE.md](skills/use-mobile-knowledge/MODULE.md) |
| DJI Mic 知识 | [MODULE.md](skills/use-mic-knowledge/MODULE.md) |
| Osmo Nano 知识 | [MODULE.md](skills/use-nano-knowledge/MODULE.md) |
| Osmo 360 知识 | [MODULE.md](skills/use-osmo360-knowledge/MODULE.md) |

## 在 DeepSeek 中使用

GitHub 用于保存与下载文件；上传到仓库不会自动在 DeepSeek 中完成安装。导入方法取决于使用的 DeepSeek 网页、App 或接入 DeepSeek 模型的智能体客户端。

DeepSeek++ 新人培训请先阅读：[完整安装、导入、分阶段使用和质检手册](DEEPSEEK-PLUS-PLUS-新人培训手册.md)。仓库根目录只导入 `deepseek/abao-controller/SKILL.md`，原 20 个入口已经作为内部 `MODULE.md` 保留。

- 支持 `MODULE.md` 和本地文件读取的客户端：按客户端的技能导入方式注册入口，并保留配套知识目录和相对路径。以 `INSTALL.md` 为准。
- 仅能聊天或上传附件的界面：提供总提示词、所需技能正文及实际引用的知识材料，作为当前对话的上下文；仅发送仓库链接不能保证它读取整个仓库。

社媒读取需要目标设备另行连接浏览器或社媒助手。可选 Python 脚本需要运行环境。本仓库的上传不代表已完成目标客户端的兼容性或运行验证。

包内产品资料的时效和证据边界见 `INSTALL.md` 与各技能说明；评论培训内容须标注为假想培训草稿。
