# 阿豹追猎 · DJI AI 技能包

此仓库保存 `阿豹追猎.zip` 中的 `dji-ai-skills-portable-20260915-v1` 技能包，包含 20 个 `MODULE.md` 入口及其知识资料、参考文件和脚本。目录已解压，便于查看和导入。

## 获取文件

- [下载完整 ZIP](https://github.com/ly23055601-glitch/desktop-tutorial1/archive/refs/heads/main.zip)，解压后保留整个目录结构。
- 或使用 Git：`git clone https://github.com/ly23055601-glitch/desktop-tutorial1.git`

## 从这里开始

1. 阅读 [安装说明](INSTALL.md)。
2. 查看 [技能清单](MANIFEST.json)，选择任务需要的技能。
3. 参考 [总提示词](SYSTEM_PROMPT.md)，加载相应知识与写作规则。

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
