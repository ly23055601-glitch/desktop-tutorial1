# 阶段派单与接续契约

总控持有唯一台账，不在20个入口分别维护完整任务。普通问答可在上下文中简记；批次和跨轮任务保存JSON或Markdown。

最小状态：task_id、mode(training_fiction/review_existing/knowledge_only/read_only)、用户约束、expected_link_ids、输入别名映射、active_stage、executor、input_revision、completed_steps、artifacts、skipped、issues。

派单包含：task_id、stage、executor、work_item_ids、input_revision、当前要解决的问题、所需材料路径、允许输出、返回条件。返回包含：status(ok/partial/blocked)、已处理ID、产物路径或正文、source_scope、issues；返回后把执行权交总控。执行者不把原始用户完整请求再次路由。

S1消费完整新链接集合一次；支持平台批量时在该阶段内按平台分组，已有材料不重采。重复链接保留原始输入位置与canonical_id，不能静默丢项。不能确认短链别名时先保留，读取结果相同才合并。

S2按精确品线/型号/条件/来源版本缓存本轮事实。多产品逐一派单；缓存命中只复用仍适用的事实，不把历史日期改成今天。输出fact_id、claim、model/component、conditions、source、checked_at、status、不可推论、编辑假设。只查知识的任务到此即可返回分析。

S3可把长批次分为G1、G2等，每组调用同一个共享写手。每个canonical link_id只保留一个候选稿及state；revision递增，旧版不混入Q。组完成仅记drafted。用户材料可用material-001等ID；合成材料显式标明，不能伪造真实平台链接。

Q只有在所有组结束或明确登记无法处理项后启动；须处理整个expected_link_ids集合。规范化文字、近似候选和语义审阅覆盖所有主评及回复，不受组界和品线界限制。修改任何稿件后重新计算哈希并使此前Q报告失效，重新检查整批重复。

返工只重开被问题依赖的阶段：文风→S3，产品事实→S2后必要S3，原帖缺失→S1且仅用户新增材料或明确允许重试的问题项。无需改变的材料/事实/好句复用。续跑读取原台账与版本，不重复采集成功项，不重写已通过句子，不重复计数。

状态意义：passed=范围完整且机器检查和语义审阅完成；manual_reviewed=逐项审阅完成但未运行机器检查；partial=只完成可用部分或用户数量超出自动检查器能力；blocked=没有可交付内容或关键材料缺失。状态用于说明本轮审阅，不代表用户已认可或事实永远有效。
