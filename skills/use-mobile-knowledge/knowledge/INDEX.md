# DJI Osmo Mobile 产品知识库

服务各项目的 Mobile 产品查询、人群心理分析与消费者评论培训，由个人技能 `use-mobile-knowledge` 统一提供。首版重点整理 **Osmo Mobile 8P、8**，以 **7P、7、6、SE、DJI OM 5** 辅助识别和代际比较。默认简体中文与中国大陆资料口径；来源重定向或仅有海外资料时按实际语言、地区标记。

首版实际核验日期为 **2026-09-06**；2026-09-07 新增两条官方事实及卖点层。当前共 **141 条产品事实、51 条兼容记录、37 条官方来源登记、7 张概览场景卡、20 组问答**，另有 **15 类角色心理假设**。另有 **25 张按型号组织的卖点卡**，以及 **48 张详细场景卡、144 个培训选材切入点**，覆盖全部25张卖点。事实与兼容记录合计176条已核、13条待核、3条冲突；重复记录可能指向同一缺口，具体见缺口清单。

## 从这里开始

在op项目的其他对话可直接说“调用Mobile知识库”或“调用Mobile场景卖点库”，也可明确使用 `$use-mobile-knowledge`。`om`产品路径沿项目既有映射进入本库；需要评论时由同一共享写手完成。资料存于文件中，不依赖创建本库的聊天历史。

| 想解决的问题 | 阅读入口 |
|---|---|
| Mobile 是什么、能力由谁提供 | [产品总览](products/overview.md) |
| 产品有哪些卖点，对谁有什么价值 | [按型号选卖点](selling_points/guide.md) |
| 具体场景怎样用卖点、怎样供培训文案选材 | [详细场景库](use_cases/guide.md)、[卖点反查场景](use_cases/selling-point-map.md)、[选材接入](use_cases/WRITER_HANDOFF.md) |
| 同手机拍法怎样变化、真实使用感受与实际接话 | [拍法与表达材料](experience_materials/guide.md)：旧款讨论及[五条新作品材料](experience_materials/cases/materials-20260908.md)，含47条评论、19条直接父句关系、1份8P完整文件与52个离散画面观察；完整连续观看／听音与同手机对照仍缺 |
| 8P、8 与旧款怎么区分 | [代际差异](products/differences.md) |
| 原生相机、Mimo、模块和遥控有什么条件 | [跟随与遥控路径](products/tracking.md) |
| 手机、保护壳、麦克风及配件能否组合 | [兼容与连接记录](compatibility/guide.md) |
| 查安装、拍摄、续航及常见误区 | [常见问题](products/faq.md) |
| 从拍摄任务查资料 | [七类场景解释](scenarios/guide.md) |
| 看潜在人群、使用动机和表达方向 | [角色心理指南](audiences/guide.md) |
| 看主型号是否覆盖各主题 | [主题覆盖](products/topic-coverage.md) |
| 回查官方依据 | [来源台账](sources/README.md) |
| 哪些问题尚未确认 | [缺口与冲突](GAPS.md) |
| 更新或检查资料 | [维护说明](MAINTENANCE.md)、[记录格式](SCHEMA.md)、[变更记录](CHANGELOG.md) |
| 看实际验证 | [当前项目调用验收](evaluation/project-access/acceptance.md)、[首版产品验收](evaluation/acceptance.md)、[跨项目封装验收](evaluation/cross-project/acceptance.md)、[卖点补充验收](evaluation/selling-points/acceptance.md)、[详细场景验收](evaluation/use-cases/acceptance.md) |

## 按型号阅读

| 型号 | 深度 | 事实阅读版 |
|---|---|---|
| Osmo Mobile 8P | 重点 | [8P](products/osmo_mobile_8p.md) |
| Osmo Mobile 8 | 重点 | [8](products/osmo_mobile_8.md) |
| Osmo Mobile 7P | 辅助 | [7P](products/osmo_mobile_7p.md) |
| Osmo Mobile 7 | 辅助 | [7](products/osmo_mobile_7.md) |
| Osmo Mobile 6 | 辅助 | [6](products/osmo_mobile_6.md) |
| Osmo Mobile SE | 辅助 | [SE](products/osmo_mobile_se.md) |
| DJI OM 5 | 辅助 | [OM 5](products/dji_om_5.md) |

“Mobile”“OM”只能确定产品线，不能默认指定最新型号。裸“8”“SE”等数字或后缀需要已有 Mobile 语境才能识别；与 Pocket、Action、RS 等产品线分别核对。

## 本地检索

先从本次发现的技能路径定位本目录，再使用 `rg`。一行 JSONL 保存完整记录，命中后连同型号、组件、条件、限制和来源一起阅读。以下示例在知识库目录运行，或将命令中的路径换成该目录的绝对路径；不依赖任何项目的工作目录。

```sh
# 关键词初查，可能含待核项
rg -n '续航|FrameTap|追踪模块|保护壳' products/*.facts.jsonl compatibility/*.jsonl

# 只查看明确属于8P的已核条目；具体兼容冲突还须查缺口
rg '"models"\s*:\s*\[[^]]*"osmo_mobile_8p"' products/*.facts.jsonl compatibility/*.jsonl | rg '"status"\s*:\s*"verified"'

# 查相关待核与冲突，避免通用结论掩盖特殊组合
rg -n '16e|固件|模块|套装' GAPS.md

# 卖点和用途，命中后继续读取所引事实的完整条件
rg -n 'MOBILE-SELL-001|取景|低机位|续航' selling_points/cards.jsonl

# 角色与心理关键词，只命中编辑假设
rg -n '独自旅行|全家|练习|操作负担' audiences/profiles.jsonl

# 实际材料：命中后读整条范围、型号、来源、日期与未决项
rg -n 'MOBILE-EXP-005|怕买来吃灰|Mimo|咔皮' experience_materials/records.jsonl

# 详细场景与选材，命中后展开依据及该型号的待核/冲突
rg -n '同行|白板|全身|旧款|MOBILE-SELL-001' use_cases/cards.jsonl
python3 scripts/use_cases.py query --id MOBILE-USE-001
python3 scripts/use_cases.py query --model osmo_mobile_8p --keyword 合影

# 精确编号：从阅读版复制ID，匹配完整id字段
rg '"id"\s*:\s*"MOBILE-8P-IDENTITY-001"' products/*.facts.jsonl
```

检索结果不是自动答案。先确认具体型号，再核对用户的手机／系统／App／配件组合，检查相关缺口。无匹配只表示本库未找到依据，不等于设备不支持。新固件可能改变旧资料中的能力限制，核验日期与版本条件必须保留。

## 在写手能力库中使用

1. 先理解真实原帖或明确的训练命题；原帖设备不明时，不用产品知识替作者确定型号。
2. 按当前问题取少量相关事实、兼容记录与场景，按需用卖点卡和[详细场景选材](use_cases/guide.md)连接人物任务与产品价值，核对完整条件及相关缺口。实际写作前回到当前官方依据确认；`pending/conflict` 不作肯定能力依据。场景字段不拼成固定评论句式，具体细节只在当批人物状态中设定或由原帖证实。
3. 按[个人 Mobile 能力入口](../MODULE.md)的写作分支进入共享表达流程；已经从项目或个人写手入口进入时，继续同一流程，不循环加载。
4. 新稿保持 `training_fiction`，产品依据进入既有 `product` 来源与 `product_fact` 断言；假想经历、关系和感受只保存在训练人物状态。

个人技能 `$use-mobile-knowledge`、原 `$write-dji-osmo-mobile-comments` 和共享写手的 Mobile 产品路由均可访问本库；op 原路径保留为指向同一维护源的链接。本库补充产品依据，不复制一套写法，也不改变真实材料核验／旧稿审查分支。Mobile 保留准确的 Osmo 名称，不沿用 Pocket 专属禁词。

## 资料性质

`verified` 表示按记录日期实际读过官方依据，不代表实机测试或永久有效。场景均为 `editorial_synthesis` 编辑推演，不是用户研究或效果承诺。卖点及用户价值是有依据的编辑解释，不是实测收益、价格排名或消费者共识。官方事实不能证明某条原帖使用了该功能。首版未含社媒素材；2026-09-08新增的独立[体验材料](experience_materials/guide.md)仅按实际读取范围保存公开自述、讨论观察及缺口，不作为产品参数或成品评论。

检索辅助：从任意目录运行本库 `scripts/query.py` 的绝对路径，例如 `python3 /实际技能目录/knowledge/scripts/query.py --model osmo_mobile_8 --keyword 模块2`。`--id` 精确匹配，未知型号不会猜为最新款；结果包含完整记录、来源及该型号的待核／冲突。
