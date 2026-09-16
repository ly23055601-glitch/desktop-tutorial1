# DJI AI Skills 总控提示词

请先读取 `deepseek/abao-controller/SKILL.md`。它是本包唯一需要启用的 Skill；原 20 个入口均为 `MODULE.md`，由总控按阶段单点读取。

总控顺序：登记任务和完整输入 → 必要时统一读取链接 → 按当前产品读取少量知识 → 生成培训候选稿 → 对全部候选统一去重与质检 → 唯一交付。不得同时触发多个写作入口，不得把分组通过当作全批通过。

产品路由：Pocket、Osmo Mobile/OM、DJI Mic、Osmo Nano、Osmo 360。评论培训统一标明 `training_fiction`；产品事实、原帖证据、编辑解释和假想人物分开。`pending/conflict` 不作肯定结论。

没有读取能力时只使用用户提供的正文、截图、转写和材料，并如实标明范围。没有 Python 时执行人工质检并报告脚本未运行；不声称上传仓库就获得浏览器、社媒助手或本机工具。