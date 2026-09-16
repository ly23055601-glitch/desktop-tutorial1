# 安装与接续

版本：2026-09-16-controller-v2。保留20个SKILL，复用原项目写手入口为唯一总控，没有额外添加第21个技能。

## 安装到支持 MODULE.md 的 AI

1. 将本目录整体复制到目标设备。
2. 把 `writer-core/core/write-consumer-comments/MODULE.md` 注册为共享写作技能。
3. 按任务再注册对应 `skills/use-*-knowledge/MODULE.md`；产品写作时先加载产品知识，再加载共享写手。
4. 需要评论培训时加载 `writer-core/adapters/op/` 中的路由说明；需要每日批次时才加载 `skills/run-daily-comment-training/`。
5. 抖音、小红书、B站读取必须由目标设备已有的社媒助手/浏览器连接完成；没有该连接时只使用用户提供的正文、画面、转写和评论材料。

> 调用阿豹追猎总控，按阶段单点触发。目标产品是……；本批完整链接/材料如下……；数量和格式要求是……。全部起草后统一去重质检，再交付。

- 产品问答：`use-<product>-knowledge` → 返回事实、条件、来源和待核项。
- 评论培训：产品知识 → `writer-core/core/write-consumer-comments` → 输出顶部标注 `training_fiction`。
- Pocket：可再加载 `skills/write-pocket-seeding-comments/MODULE.md` 保留 Pocket 型号命名边界。
- 多链接采集：先加载 `skills/read-social-links-with-social-helper/MODULE.md`，一次提交完整链接集合。

本包没有DeepSeek专属运行时、社媒登录或发布工具。skills中的旧KPI、LH13和历史流程仅供明确要求的复盘，不参与新稿默认链。所有当前执行入口见 [MANIFEST.json](MANIFEST.json)。
