# 封装与迁移

`references/knowledge/` 是完整独立快照，包含产品、兼容、官方证据、场景、角色心理资料及检索测试。`manifest.json` 记录版本、维护源与发布文件的 SHA-256；`scripts/mic.py audit` 检查结构与发布文件完整性，不联网确认最新状态。

同一账户在其他项目中直接调用 `$use-mic-knowledge` 或说“调用 Mic 产品与人群能力库”。发现位置为用户目录 `.agents/skills/use-mic-knowledge`，可指向个人安装目录；不需要复制到每个项目。如当前会话尚未刷新技能目录，新开会话或重新加载后调用。

迁移到另一台机器：完整复制 `use-mic-knowledge` 目录到该机器的个人技能发现目录，保留内部相对路径，再用新绝对路径运行 `scripts/mic.py audit`。不要只复制 SKILL.md。包内检索只用 Python 3.9+ 标准库，无网络服务、API 密钥或 op 项目依赖。

评论写作还需同目录相邻的 `write-consumer-comments` 和 `write-dji-mic-comments`；需要实时读取社媒时再依共享层配置统一读取技能。缺少这些依赖时产品检索和心理分析仍可用，但不能宣称已按共享写手规范验收新稿。

这是显式发布的快照，不后台同步、不定时更新。维护源变化后，应重新运行维护项目的 `knowledge/mic/scripts/package_skill.py`，安装新快照并复验。`evaluation/` 中原产品验收属于历史核验记录；其中的维护项目路径不是运行依赖。跨项目验收另存于维护项目的 `packaging/acceptance.md`。


`materials/`另含历史体验候选和原话范围，`training/experience-materials.md`说明如何补实际声音与讨论。它们是材料索引，不宣称已经听过所列视频；原始媒体和历史原帖证据留在原位置，未随本包迁移。跨机可以阅读方法、盘点与摘录，若需重新看听作品，须另外取得对应文件或按统一技能读取。产品与场景检索不依赖这些外部素材路径。
