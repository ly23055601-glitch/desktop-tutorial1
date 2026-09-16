# DJI AI Skills Portable Bundle

版本：2026-09-15-v1。此包来自 op、写手培训、om、dm、ow、oq 六个任务的当前有效入口。

## 安装到支持 MODULE.md 的 AI

1. 将本目录整体复制到目标设备。
2. 把 `writer-core/core/write-consumer-comments/MODULE.md` 注册为共享写作技能。
3. 按任务再注册对应 `skills/use-*-knowledge/MODULE.md`；产品写作时先加载产品知识，再加载共享写手。
4. 需要评论培训时加载 `writer-core/adapters/op/` 中的路由说明；需要每日批次时才加载 `skills/run-daily-comment-training/`。
5. 抖音、小红书、B站读取必须由目标设备已有的社媒助手/浏览器连接完成；没有该连接时只使用用户提供的正文、画面、转写和评论材料。

## 推荐调用顺序

- 产品问答：`use-<product>-knowledge` → 返回事实、条件、来源和待核项。
- 评论培训：产品知识 → `writer-core/core/write-consumer-comments` → 输出顶部标注 `training_fiction`。
- Pocket：可再加载 `skills/write-pocket-seeding-comments/MODULE.md` 保留 Pocket 型号命名边界。
- 多链接采集：先加载 `skills/read-social-links-with-social-helper/MODULE.md`，一次提交完整链接集合。

## 重要边界

本包不包含登录凭据、社媒连接或自动发布能力；不把历史稿、编辑推断或假想人物经历当作真实消费者证据。产品能力在目标设备使用前应按当前官方资料复核。

完整映射、来源任务和校验和见 `MANIFEST.json` 与 `SHA256SUMS`。
