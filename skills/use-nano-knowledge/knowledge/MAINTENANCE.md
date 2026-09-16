# Nano 知识库维护

## 哪份数据负责什么

- `products/facts.jsonl`：事实唯一数据源，一行一个可核查结论；阅读版`products/guide.md`与FAQ通过ID对应，不另立事实。
- `sources/official.jsonl`：来源唯一台账；官方原件和摘录留存在`sources/`，SHA256绑定此次读取内容。
- `scenarios/cards.jsonl`：场景与事实的关联；阅读版为`scenarios/guide.md`。事实更新后要检查关联场景是否仍成立。
- `selling-points/cards.jsonl`：卖点与使用价值的编辑解释，不建立另一套产品事实；阅读版为`selling-points/guide.md`。
- `scenarios/training-*.jsonl`：细场景、需求假设与选材角度；原有日常／活动文件之外，2026-09-08 新增关系与轻型工作补充文件。阅读版为`scenarios/training-guide.md`。具体人物、评论与教学示例仍存`outputs/`。
- `selling-points/scenario-map.md`：由所有细场景的卖点引用生成反查表；按卖点选择片段时使用，不另维护一套场景关系。

## 字段约定

| 数据 | 必须保留的字段 |
|---|---|
| 事实 | `id`、`models`、`components`、`topic`、`title`、`fact`、`conditions`、`not_infer`、`source_refs`、`checked_at`、`status`、`tags` |
| 来源引用 | `source_id`与`locator`；PDF用从1开始的物理页码，网页用章节与完整问题标题 |
| 来源 | `id`、`title`、`url`、`type`、`language`、`region`、`document_version`、`firmware_scope`、`published_at`、`checked_at`、`read_scope`、`local_path`、`sha256` |
| 场景 | `id`、`title`、`target_models`、`basis`、`basis_note`、`task`、`possible_concerns`、`product_connections`、`conditions`、`not_infer`、`open_question_ids`、`checked_at` |

`models`/`target_models`当前为`["osmo_nano"]`；组件单独记录。事实状态为`verified`或`pending`。`topic`采用`form / mounting / imaging / stabilization / audio / controls / power / protection / storage / app_accessories`。场景基底当前为`editorial_hypothesis`；`product_connections`每项保存`fact_id`和它对任务的具体意义`relevance`。

文档日期不明填null；下载中心日期可另用`download_page_date`，不据URL路径或PDF元数据猜发布日期。网页可能无版本号，记录实际语言、地区及阅读范围。各来源版本不自动等于功能最低固件。

## 更新方式

1. 在写作引用、新版本出现、用户提出事实问题或资料冲突时触发人工核验。对当前需要的官方页面/PDF进行实际阅读，检查脚注及表格对应列。
2. 同一事实的修正保留原ID，在变更记录注明旧结论、变化及来源。新增独立能力分配新ID。发现无法消解的冲突，设为pending并同时保留双方定位。
3. 来源内容更新时保存新日期命名的快照或原件，更新台账和SHA256，在变更记录保留旧版本的路径。不能只改核验日期。
4. 同步事实阅读版、FAQ、场景关联、主题覆盖和缺口；不要把新事实写进场景而漏掉事实库。
5. 检查JSONL可解析、ID唯一、来源与事实引用存在、来源文件哈希一致；逐条检查变更内容是否保留组件和使用条件，再运行相关验收问题。

卖点与细场景改动后，从项目根目录运行以下命令同步阅读版并验证引用；脚本不联网重核事实，也不代替语义审阅或用户校准：

```sh
python3 .agents/skills/use-nano-knowledge/scripts/build_material_views.py
python3 .agents/skills/use-nano-knowledge/scripts/validate_package.py
```

卖点用`basis: editorial_interpretation`，细场景用`basis: editorial_hypothesis`；两者保留`review_status`、`prepared_at`与关联`fact_ids`。细场景另用`selling_point_ids`和`why_these_points`连接卖点，其中每项为`selling_point_id`与`value_reason`。`prepared_at`只记录编辑日期，实际产品核验日期从关联事实读取。新增卡片继续使用唯一`NANO-SP-`或`NANO-TRAIN-`编号，不覆盖7张基础卡或旧验收记录。

价格、套装、固件与兼容性在每次实际使用当日复核；稳定硬件条目被用于正文时也回到现有官方来源确认。本库没有后台自动刷新或定时任务。

2026-09-08 深化字段均为可选选材，不是新写作格式：卖点的 `value_facets` 保存 `focus`、`viewer_or_user_value`、`material_cue`；新增场景的 `viewer_payoff` 说明拍后观看价值，`usage_stage_angles` 保存不同熟悉程度的关注。实际事实沿用原引用与日期；`deepened_at` 只标卖点解释的编辑日期。生成、检索与验证都读取 `training-*.jsonl`，新增文件不会只出现在阅读版而漏出验证范围。

官方资料、原帖内容与独立假想人物分别保存。新事实不能证明原帖已经使用该功能，训练经历不能给未知性能补证。共享写法反馈仍由共用写手库维护，不写入本产品事实库。

## 真实体验材料

`experience/`保存作品原话、原始来源定位和阅读范围；产品官方事实仍在原台账。现有`source-register.jsonl`用于维护者追溯16件材料，不要求用户填写结构表。公开正文、未经润色口述、实际评论回复、编辑理解和用户表达判断分别标明。用户反馈仅按原消息实际作用范围保存，不把独立审稿变成用户认可。

新增材料先沿用共享帖子类型，保留完整作品路径及必要设备/处理说明；不足按件标注。新的社媒读取仅走统一技能，复用成功证据，按既有完整集合续接，不另建采集办法。状态、补读和验收证据在本轮`outputs/nano/2026-09-08-experience-materials/`；只有取得实际原句、回复和对应上下文后才更新缺口。
