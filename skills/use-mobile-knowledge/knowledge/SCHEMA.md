# Mobile 知识记录约定

UTF-8 JSONL 是事实维护源，Markdown 是带编号引用的阅读版。型号 ID 为 `osmo_mobile_8p`、`osmo_mobile_8`、`osmo_mobile_7p`、`osmo_mobile_7`、`osmo_mobile_6`、`osmo_mobile_se`、`dji_om_5`。不把裸“Mobile”“OM”自动判为某一代。

## 官方来源

`sources/*.jsonl` 每条必含：`id`、`title`、`url`、`type`（specs/faq/manual/compatibility/firmware/store/support）、`language`、`region`、`document_version`（未知 null）、`published_at`（未明示 null）、`checked_at`（实际读取日期）、`read_scope`、`local_path`（库内相对路径）、`sha256`。

只登记实际读过的官方资料，原件或读取快照保存在 `sources/originals/` 或 `sources/snapshots/`。网页保留实际响应的语言和地区，不能按请求 URL 猜；网页跳转、读不到正文和仅找到下载条目不是读过资料。离线保存的工具可读文本须标明提取方式，不能冒充原始 HTML。表格、图示和脚注需要按版面核对。发布日期不明不能用路径或读取日期代填。

若原件与提取文本都保存，额外登记 `snapshot_path`、`snapshot_sha256` 和 `extraction`；目视核对的图像可另用 `visual_paths` 记录。审计同时检查原件和提取快照的哈希。

## 产品事实

`products/*.facts.jsonl` 每条必含：`id`、`models`（型号 ID 数组）、`component`、`topic`、`statement`、`conditions`（数组）、`limitations`（数组，含不可推论）、`source_refs`（`[{"source_id":"…","locator":"章节、问题标题或从1开始的PDF物理页码"}]`）、`checked_at`、`status`（verified/pending/conflict）、`keywords`（数组）。

主题为 `identity`、`stabilization`、`controls`、`tracking`、`compatibility`、`audio`、`power`、`kits`、`maintenance`、`software`。一条记录对应一个可核查结论，型号共用结论必须逐款有依据。

`verified` 表示在核验日期实际读过官方依据，不表示实机测过或永久有效。`pending/conflict` 必须写 `gap_reason`，不进入肯定回答。没有证据不能改写成“不支持”。来源冲突未消解时保留双方定位。

## 兼容记录

`compatibility/*.jsonl` 使用事实的全部字段，额外必含：`gimbal_model`（单个型号 ID）、`devices`（准确的手机/配件名称数组）、`method`（连接或跟随路径）、`support`（supported/not_supported/conditional/unconfirmed）、`features`（具体功能数组）。`models` 与云台型号一致。

条件按资料需要保留手机系统、App、固件、地区、套装、线材和组合方式。连接关系有方向，不自动对称或传递；能夹住、能连接、能控制快门、能取景和能跟随是不同结论。`verified` 不能搭配 `unconfirmed`。

## 型号和场景

`products/models.jsonl` 保存 `id`、`official_name`、`aliases`（无歧义简称）、`priority`（primary/basic）、`fact_ids`。

`scenarios/cards.jsonl` 保存 `id`、`title`、`models`、`kind`（固定 editorial_synthesis）、`task`、`possible_concerns`（数组）、`guidance`、`conditions`（数组）、`limitations`（数组）、`fact_ids`、`compatibility_ids`。场景只是编辑推演，所有产品能力和操作步骤须可回到已核记录，不代表真实用户反馈、原帖内容或实拍效果。

## 文件责任和检索

8P、8 和辅助型号分别维护事实文件及来源台账，跨型号阅读表引用各自编号。产品/兼容条目是事实源，场景只解释已有依据。`rg` 命中一整行即完整记录；先确认型号与状态，再读取全部条件、限制和来源。未核条目只提示缺口，无匹配不代表设备不支持。

## 独立角色心理记录

`audiences/profiles.jsonl` 保存 `editorial_hypothesis`，不混入 verified/pending/conflict 产品结论。字段及表达示例状态见 [人群格式](audiences/SCHEMA.md)。`scripts/maintain.py audit` 也校验这些记录的ID、引用与性质；`render` 从记录及其引用事实重建角色指南。

## 卖点与用户价值

`selling_points/cards.jsonl`（目录名为 selling_points）独立维护编辑卖点，字段见[卖点格式](selling_points/SCHEMA.md)。`editorial_synthesis`与`hypothesis_not_measured`不能改标为官方事实或实测效果，引用只使用本型号已核能力。

## 详细使用场景与培训选材

`use_cases/cards.jsonl`按具体时刻与单一型号关联卖点、角色、事实及兼容条件，字段见[详细场景格式](use_cases/SCHEMA.md)。情境与心理为编辑假设，选材保留`training_fiction/pending_calibration`；它不是产品事实或原帖来源。场景查询展开完整依据及型号缺口，受影响的待核材料隔离在`blocked`。
