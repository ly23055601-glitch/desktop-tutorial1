# Mobile 产品卖点与用户价值

卖点是把已核能力与拍摄任务连接起来的编辑说明；用户价值是有条件的推演，不是实测结果、购买排名或用户研究。先确认型号，再选与当前人物和任务有关的1—3项。

每张卡区分能力、具体用途、可能价值、适用角色和不可推论。参数条件直接读取产品事实和兼容记录，卖点卡不另存一套参数。

## 按型号选取

| 型号 | 本版卖点 | 阅读入口 |
|---|---:|---|
| Osmo Mobile 8P | 10 | [Osmo Mobile 8P 卖点](osmo_mobile_8p.md) |
| Osmo Mobile 8 | 10 | [Osmo Mobile 8 卖点](osmo_mobile_8.md) |
| Osmo Mobile 7P | 1 | [Osmo Mobile 7P 卖点](osmo_mobile_7p.md) |
| Osmo Mobile 7 | 1 | [Osmo Mobile 7 卖点](osmo_mobile_7.md) |
| Osmo Mobile 6 | 1 | [Osmo Mobile 6 卖点](osmo_mobile_6.md) |
| Osmo Mobile SE | 1 | [Osmo Mobile SE 卖点](osmo_mobile_se.md) |
| DJI OM 5 | 1 | [DJI OM 5 卖点](dji_om_5.md) |

## 具体场景与培训选材

从[详细场景库](../use_cases/guide.md)查看具体时刻、拍摄难点和人物取舍，或用[卖点反查场景](../use_cases/selling-point-map.md)选择用途。表达方向是待校准的培训选项，使用时接入同一共享写手，不逐字段拼成评论。

## 先看这些区别

- 8P 可优先按任务选 FrameTap 远程取景、模块2触屏选物、A/B创意运镜；新增手机夹和三脚架结构也有独立事实。手机投屏与模块图传分别说明。
- 8 可按低机位、摇杆/拨轮操作、不同跟随路径和一代模块收音选材。经适配固件支持模块2，不能因此借用8P触屏和任意物体手动框选。
- 旧款按现有内置杆、内置或外接脚架、滑杆/拨轮及软件路径说明可用价值；不依据型号年份判断当前软件，不编价格或购买排名。

## 检索和写作接入

在本知识库目录用 `rg -n 'MOBILE-SELL-001|取景|低机位|续航' selling_points/cards.jsonl`，或按 `"models": ["osmo_mobile_8p"]` 精确筛选。JSONL保留整卡，但参数条件与来源在所引用的事实记录；可继续用 `scripts/query.py --id 事实编号` 取完整依据及型号缺口。

评论任务仍进入[个人能力入口](../../SKILL.md)指向的同一共享写手。先回应原帖，按当前任务取必要卖点；不强制每条评论展示功能，也不把“能力→用途→价值”变成成稿句式。产品断言绑定产品来源，假想经历留在训练状态。

记录字段见[格式说明](SCHEMA.md)，官方重取与本轮验收见[验收记录](../evaluation/selling-points/acceptance.md)。
